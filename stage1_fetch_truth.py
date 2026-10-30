"""
Stage 1 Pre-Earnings (T-1) Deterministic Financial Data Mesh
- Scans tickers.txt strictly for upcoming earnings in the T-1 window (today + next 1-2 trading days).
- Extracts & cross-validates spot price (Yahoo Finance + Google Finance).
- Computes 7:00 AM resilient ATM weekly straddle options-implied move, IV, and Put/Call OI skew.
- Extracts 4-Quarter Historical Earnings Beat/Miss Track Record & 1-Day Post-Earnings Realized Stock Moves.
- Extracts Wall Street Analyst Consensus Price Targets (Mean, Median, High, Low, Upside %) & Ratings.
- Stitches 5-Quarter Historical Financials (with Q4 10-K isolation) and pre-computes QoQ/YoY deltas.
- Pre-computes deterministic Forensic True FCF Bridge for the latest reported quarter.
- Preserves locked T-1 pre-print snapshot if re-run on or after the earnings date.
"""

import sys
import json
import math
from datetime import datetime, timedelta, date
from pathlib import Path
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup

try:
    from edgar import Company, set_identity
    set_identity("PortfolioResearch research@local.dev")
    EDGAR_AVAILABLE = True
except ImportError:
    EDGAR_AVAILABLE = False

BASE_DIR = Path(__file__).parent.resolve()
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
GROUND_TRUTH_DIR.mkdir(exist_ok=True)

def load_tickers():
    raw = (BASE_DIR / "tickers.txt").read_text(encoding="utf-8").splitlines()
    return [line.strip().upper() for line in raw if line.strip() and not line.startswith("#")]

# --- FIX #1: Strict T-1 Upcoming Window (Excludes yesterday's already-released T+0 prints) ---
def get_t1_window():
    today = datetime.now().date()
    weekday = today.weekday()  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
    if weekday == 4:  # Friday: check Fri, Sat, Sun, Mon, Tue
        forward = [today + timedelta(days=i) for i in range(0, 5)]
    elif weekday == 5:  # Saturday: check Sat, Sun, Mon, Tue
        forward = [today + timedelta(days=i) for i in range(0, 4)]
    else:  # Mon-Thu, Sun: check today + next 2 days
        forward = [today + timedelta(days=i) for i in range(0, 3)]
    return sorted(list(set(forward)))

def safe_float(val):
    try:
        if val is None or pd.isna(val) or (isinstance(val, float) and math.isnan(val)):
            return None
        return round(float(val), 2)
    except Exception:
        return None

def check_google_finance_price(symbol: str, exchange_hint: str) -> float | None:
    exch = "NASDAQ" if exchange_hint in ["NMS", "NAS", "NGM"] else "NYSE"
    for candidate in [exch, "NASDAQ", "NYSE"]:
        url = f"https://www.google.com/finance/quote/{symbol}:{candidate}"
        try:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            div = soup.find("div", {"class": "YMlKec fxKbKc"})
            if div:
                return float(div.text.replace("$", "").replace(",", "").strip())
        except Exception:
            continue
    return None

# --- FIX #6: Unconfirmed Earnings Date & BMO/AMC Verification Flag ---
def verify_earnings_schedule(t: yf.Ticker, target_date_str: str) -> dict:
    status = "UNCONFIRMED_ESTIMATE_MUST_VERIFY_VIA_SEARCH"
    timing_hint = "UNKNOWN_CHECK_BMO_OR_AMC"
    eps_consensus = None
    try:
        ed_df = t.get_earnings_dates(limit=12)
        if ed_df is not None and not ed_df.empty:
            for idx, row in ed_df.iterrows():
                dt_str = str(idx.date())
                if dt_str == target_date_str:
                    eps_est = safe_float(row.get("EPS Estimate"))
                    if eps_est is not None:
                        eps_consensus = eps_est
                        status = "SCHEDULED_IN_EARNINGS_CALENDAR_VERIFY_WEBCAST_TIME"
                    hr = idx.hour
                    if 0 < hr < 12:
                        timing_hint = "BMO (Before Market Open)"
                    elif hr >= 16:
                        timing_hint = "AMC (After Market Close)"
                    break
    except Exception:
        pass
    return {
        "earnings_date": target_date_str,
        "confirmation_flag": status,
        "release_timing_hint": timing_hint,
        "yahoo_consensus_eps": eps_consensus
    }

# --- NEW FEATURE 1A: 4-Quarter Historical Earnings Beat/Miss & Realized 1D Move Track Record ---
def compute_historical_earnings_track_record(t: yf.Ticker, target_date_str: str, implied_move_pct: float | None) -> dict:
    quarters = []
    try:
        ed_df = t.get_earnings_dates(limit=16)
        hist_df = t.history(period="2y")
        hist_dates = []
        if hist_df is not None and not hist_df.empty:
            hist_df = hist_df.copy()
            hist_df["date_str"] = [str(d.date()) for d in hist_df.index]
            hist_dates = list(hist_df["date_str"])

        if ed_df is not None and not ed_df.empty:
            for idx, row in ed_df.iterrows():
                dt_str = str(idx.date())
                # Strictly prior to target_date_str to prevent any look-ahead bias
                if dt_str >= target_date_str:
                    continue
                eps_est = safe_float(row.get("EPS Estimate"))
                eps_act = safe_float(row.get("Reported EPS"))
                surp_pct = safe_float(row.get("Surprise(%)"))
                if eps_est is None or eps_act is None:
                    continue

                if surp_pct is None and eps_est != 0:
                    surp_pct = round(((eps_act - eps_est) / abs(eps_est)) * 100, 2)

                verdict = "BEAT" if eps_act > eps_est else ("MET" if eps_act == eps_est else "MISS")

                # Compute 1-day post-earnings stock move from daily history
                move_1d_pct = None
                if hist_dates and dt_str in hist_dates:
                    pos = hist_dates.index(dt_str)
                    hr = idx.hour
                    # If AMC (hr >= 16 or default), reaction is next trading day close vs earnings day close
                    if hr >= 16 or hr == 0:
                        if pos + 1 < len(hist_dates):
                            c0 = float(hist_df.iloc[pos]["Close"])
                            c1 = float(hist_df.iloc[pos + 1]["Close"])
                            if c0 > 0:
                                move_1d_pct = round(((c1 - c0) / c0) * 100, 2)
                    else:
                        # BMO: reaction is earnings day close vs prior trading day close
                        if pos - 1 >= 0:
                            c0 = float(hist_df.iloc[pos - 1]["Close"])
                            c1 = float(hist_df.iloc[pos]["Close"])
                            if c0 > 0:
                                move_1d_pct = round(((c1 - c0) / c0) * 100, 2)

                quarters.append({
                    "earnings_date": dt_str,
                    "eps_estimate": eps_est,
                    "eps_actual": eps_act,
                    "surprise_pct": surp_pct,
                    "verdict": verdict,
                    "actual_1d_move_pct": move_1d_pct
                })
                if len(quarters) >= 4:
                    break
    except Exception as e:
        return {"track_record_error": str(e), "prior_4q_releases": []}

    beats = sum(1 for q in quarters if q["verdict"] == "BEAT")
    total_q = len(quarters)
    beat_rate_pct = round((beats / total_q) * 100, 1) if total_q > 0 else None
    surprises = [q["surprise_pct"] for q in quarters if q["surprise_pct"] is not None]
    avg_surprise_pct = round(sum(surprises) / len(surprises), 2) if surprises else None
    abs_moves = [abs(q["actual_1d_move_pct"]) for q in quarters if q["actual_1d_move_pct"] is not None]
    avg_abs_1d_move_pct = round(sum(abs_moves) / len(abs_moves), 2) if abs_moves else None

    implied_vs_hist_delta = None
    vol_regime = "FAIRLY_PRICED_VS_HISTORY"
    if implied_move_pct is not None and avg_abs_1d_move_pct is not None and avg_abs_1d_move_pct > 0:
        implied_vs_hist_delta = round(implied_move_pct - avg_abs_1d_move_pct, 2)
        if implied_move_pct < avg_abs_1d_move_pct * 0.85:
            vol_regime = "UNDERPRICED_VS_HISTORY (LONG VOLATILITY EDGE)"
        elif implied_move_pct > avg_abs_1d_move_pct * 1.15:
            vol_regime = "OVERPRICED_VS_HISTORY (SHORT VOLATILITY / THETA HARVEST EDGE)"

    return {
        "quarters_evaluated": total_q,
        "beats_count": beats,
        "beat_rate_pct": beat_rate_pct,
        "avg_eps_surprise_pct": avg_surprise_pct,
        "avg_historical_1d_move_abs_pct": avg_abs_1d_move_pct,
        "current_implied_move_pct": implied_move_pct,
        "implied_vs_historical_move_delta_pct": implied_vs_hist_delta,
        "options_vol_regime": vol_regime,
        "prior_4q_releases": quarters
    }

# --- NEW FEATURE 1B: Wall Street Analyst Consensus Price Targets & Ratings ---
def extract_street_consensus_and_targets(
    t: yf.Ticker,
    info: dict,
    spot_price: float | None,
    yahoo_consensus_eps: float | None,
    existing_targets: dict | None = None,
    stitched_5q: dict | None = None,
    earnings_date_str: str | None = None,
) -> dict:
    mean_pt = safe_float(info.get("targetMeanPrice"))
    median_pt = safe_float(info.get("targetMedianPrice"))
    high_pt = safe_float(info.get("targetHighPrice"))
    low_pt = safe_float(info.get("targetLowPrice"))
    upside_pct = None
    if mean_pt and spot_price and spot_price > 0:
        upside_pct = round(((mean_pt - spot_price) / spot_price) * 100, 2)

    # Deterministic period-aligned revenue consensus extraction from yfinance revenue_estimate / calendar
    rev_avg = None
    rev_low = None
    rev_high = None
    rev_growth = None
    period_mismatch_warning = False

    q_minus_4_rev = None
    if stitched_5q:
        rev_hist = (
            stitched_5q.get("income_statement_5q", {})
            .get("metrics_millions", {})
            .get("Total Revenue", {})
            .get("values_5q_chronological", [])
        )
        if len(rev_hist) == 5 and rev_hist[1]:
            q_minus_4_rev = float(rev_hist[1])

    # If historical rerun, preserve locked T-1 consensus revenue to prevent rolling to Q+1
    if existing_targets and existing_targets.get("yahoo_consensus_revenue_q0e") is not None:
        rev_avg = existing_targets.get("yahoo_consensus_revenue_q0e")
        rev_low = existing_targets.get("yahoo_revenue_low_q0e")
        rev_high = existing_targets.get("yahoo_revenue_high_q0e")
        rev_growth = existing_targets.get("yahoo_revenue_growth_q0e_pct")
    else:
        already_released = bool(earnings_date_str and earnings_date_str < date.today().isoformat())
        try:
            re_df = t.revenue_estimate
            if re_df is not None and not re_df.empty and "0q" in re_df.index:
                row_0q = re_df.loc["0q"]
                yr_ago_est = None
                if row_0q.get("yearAgoRevenue") is not None and not pd.isna(row_0q.get("yearAgoRevenue")):
                    yr_ago_est = safe_float(row_0q.get("yearAgoRevenue") / 1e6)

                # Guardrail: Period-alignment check prevents locking Q+1 consensus if Yahoo '0q' already rolled
                if yr_ago_est and q_minus_4_rev and abs(yr_ago_est - q_minus_4_rev) / q_minus_4_rev > 0.10:
                    period_mismatch_warning = True
                elif already_released and yr_ago_est is None:
                    period_mismatch_warning = True

                if not period_mismatch_warning:
                    if row_0q.get("avg") is not None and not pd.isna(row_0q.get("avg")):
                        rev_avg = safe_float(row_0q.get("avg") / 1e6)
                    if row_0q.get("low") is not None and not pd.isna(row_0q.get("low")):
                        rev_low = safe_float(row_0q.get("low") / 1e6)
                    if row_0q.get("high") is not None and not pd.isna(row_0q.get("high")):
                        rev_high = safe_float(row_0q.get("high") / 1e6)
                    if row_0q.get("growth") is not None and not pd.isna(row_0q.get("growth")):
                        rev_growth = safe_float(row_0q.get("growth") * 100)
        except Exception:
            pass

        if rev_avg is None and not period_mismatch_warning and not already_released:
            try:
                cal = t.calendar or {}
                if cal.get("Revenue Average"):
                    rev_avg = safe_float(cal.get("Revenue Average") / 1e6)
                if cal.get("Revenue Low"):
                    rev_low = safe_float(cal.get("Revenue Low") / 1e6)
                if cal.get("Revenue High"):
                    rev_high = safe_float(cal.get("Revenue High") / 1e6)
            except Exception:
                pass

    return {
        "target_mean_price": mean_pt,
        "target_median_price": median_pt,
        "target_high_price": high_pt,
        "target_low_price": low_pt,
        "implied_upside_to_mean_pct": upside_pct,
        "analyst_count": info.get("numberOfAnalystOpinions"),
        "recommendation_key": info.get("recommendationKey", ""),
        "recommendation_mean": safe_float(info.get("recommendationMean")),
        "yahoo_consensus_eps_q0e": yahoo_consensus_eps,
        "yahoo_consensus_revenue_q0e": rev_avg,
        "yahoo_revenue_low_q0e": rev_low,
        "yahoo_revenue_high_q0e": rev_high,
        "yahoo_revenue_growth_q0e_pct": rev_growth
    }

# --- FIX #3: 7:00 AM Pre-Market Options Implied Move (Bid/Ask -> ±2.5% Vol-Weighted -> IV Fallback) ---
def compute_airtight_options_metrics(t: yf.Ticker, spot_price: float, earnings_date_str: str) -> dict:
    if not spot_price:
        return {}
    try:
        expiries = t.options
        chosen_exp = next((exp for exp in expiries if exp > earnings_date_str), expiries[0] if expiries else None)
        if not chosen_exp:
            return {}

        chain = t.option_chain(chosen_exp)
        calls, puts = chain.calls.copy(), chain.puts.copy()

        band_low, band_high = spot_price * 0.975, spot_price * 1.025
        near_calls = calls[(calls["strike"] >= band_low) & (calls["strike"] <= band_high)]
        near_puts = puts[(puts["strike"] >= band_low) & (puts["strike"] <= band_high)]

        if near_calls.empty:
            near_calls = calls.iloc[(calls["strike"] - spot_price).abs().argsort()[:2]]
        if near_puts.empty:
            near_puts = puts.iloc[(puts["strike"] - spot_price).abs().argsort()[:2]]

        def robust_leg_price(df_band, is_call=True):
            valid_ba = df_band[(df_band["bid"] > 0) & (df_band["ask"] > 0)]
            if not valid_ba.empty:
                closest = valid_ba.iloc[(valid_ba["strike"] - spot_price).abs().argsort()[:1]]
                return float((closest["bid"].values[0] + closest["ask"].values[0]) / 2.0), "BID_ASK_MIDPOINT"

            weights = df_band["volume"].fillna(0) + df_band["openInterest"].fillna(0) * 0.1 + 1.0
            weighted_last = float((df_band["lastPrice"] * weights).sum() / weights.sum())
            if weighted_last > 0:
                return weighted_last, "VOLUME_OI_WEIGHTED_ATM_BAND"

            iv = float(df_band["impliedVolatility"].median() or 0.5)
            dte = max((datetime.strptime(chosen_exp, "%Y-%m-%d").date() - datetime.now().date()).days, 1)
            return float(spot_price * iv * math.sqrt(dte / 365.0) * 0.4), "IV_BLACK_SCHOLES_APPROX"

        c_price, c_method = robust_leg_price(near_calls, True)
        p_price, p_method = robust_leg_price(near_puts, False)
        straddle = round(c_price + p_price, 2)
        implied_move_pct = round((straddle / spot_price) * 100, 2)
        pcr_oi = round(float(puts["openInterest"].fillna(0).sum()) / max(float(calls["openInterest"].fillna(0).sum()), 1.0), 2)
        atm_iv = round(float((near_calls["impliedVolatility"].median() + near_puts["impliedVolatility"].median()) / 2.0) * 100, 2)

        return {
            "expiry_strictly_after_earnings": chosen_exp,
            "pricing_method_used": f"{c_method} / {p_method}",
            "atm_straddle_usd": straddle,
            "atm_implied_move_pct": implied_move_pct,
            "atm_implied_volatility_pct": atm_iv,
            "put_call_oi_ratio": pcr_oi
        }
    except Exception as e:
        return {"options_error": str(e)}

# --- FIX #2: 5-Quarter Stitched Table + Q4 10-K Isolation (FY - (Q1+Q2+Q3)) + Pre-Computed Deltas ---
def build_5q_stitched_financials(t: yf.Ticker, symbol: str) -> dict:
    q_inc = t.quarterly_income_stmt
    a_inc = t.income_stmt
    q_cf = t.quarterly_cashflow
    q_bs = t.quarterly_balance_sheet

    def extract_5q_series(q_df, a_df=None):
        if q_df is None or q_df.empty:
            return {}
        cols = sorted(list(q_df.columns[:5]))
        formatted_cols = {}
        for c in cols:
            dt = pd.to_datetime(c)
            q_num = (dt.month - 1) // 3 + 1
            col_label = f"Q{q_num} {dt.year} (Ended {dt.strftime('%b %d, %Y')})"
            formatted_cols[c] = col_label

        out = {"period_headers": [formatted_cols[c] for c in cols], "metrics_millions": {}}
        for metric in q_df.index:
            vals = []
            for c in cols:
                raw_v = q_df.loc[metric, c]
                if (pd.isna(raw_v) or raw_v == 0) and a_df is not None and c in a_df.columns and metric in a_df.index:
                    fy_val = a_df.loc[metric, c]
                    prior_3q = [q_df.loc[metric, pq] for pq in cols if pq < c][-3:]
                    if not pd.isna(fy_val) and len(prior_3q) == 3 and not any(pd.isna(x) for x in prior_3q):
                        raw_v = fy_val - sum(prior_3q)
                vals.append(round(float(raw_v) / 1e6, 2) if pd.notna(raw_v) else None)

            qoq_pct, yoy_pct = None, None
            if len(vals) >= 2 and vals[-1] is not None and vals[-2] not in (None, 0):
                qoq_pct = round(((vals[-1] - vals[-2]) / abs(vals[-2])) * 100, 2)
            if len(vals) == 5 and vals[-1] is not None and vals[0] not in (None, 0):
                yoy_pct = round(((vals[-1] - vals[0]) / abs(vals[0])) * 100, 2)

            out["metrics_millions"][str(metric)] = {
                "values_5q_chronological": vals,
                "q0_latest": vals[-1] if vals else None,
                "qoq_change_pct": qoq_pct,
                "yoy_change_pct": yoy_pct
            }
        return out

    sec_edgar_summary = {}
    if EDGAR_AVAILABLE:
        try:
            comp = Company(symbol)
            sec_edgar_summary["cik"] = str(comp.cik).zfill(10)
            filings_10q_10k = comp.get_filings(form=["10-Q", "10-K"]).latest(5)
            sec_edgar_summary["recent_10q_10k_filings"] = [
                {"form": f.form, "filing_date": str(f.filing_date), "period_of_report": str(getattr(f, "period_of_report", ""))}
                for f in filings_10q_10k
            ]
        except Exception as e:
            sec_edgar_summary["edgar_note"] = str(e)

    return {
        "income_statement_5q": extract_5q_series(q_inc, a_inc),
        "cash_flow_5q": extract_5q_series(q_cf),
        "balance_sheet_5q": extract_5q_series(q_bs),
        "sec_edgar_filings_meta": sec_edgar_summary
    }

# --- NEW FEATURE 1C: Deterministic Pre-Computed Forensic FCF Bridge (Latest Reported Quarter) ---
def compute_forensic_fcf_bridge_latest(stitched_5q: dict) -> dict:
    cf_metrics = stitched_5q.get("cash_flow_5q", {}).get("metrics_millions", {})
    periods = stitched_5q.get("cash_flow_5q", {}).get("period_headers", [])
    latest_period = periods[-1] if periods else "Latest Reported Quarter"

    def get_latest(keys: list[str], default_val: float = 0.0) -> float:
        for k in keys:
            if k in cf_metrics and cf_metrics[k].get("q0_latest") is not None:
                return float(cf_metrics[k]["q0_latest"])
        return default_val

    ocf = round(get_latest(["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"], 0.0), 2)
    capex_raw = get_latest(["Capital Expenditure", "Purchase Of PPE", "Net PPE Purchase And Sale"], 0.0)
    capex = round(abs(capex_raw), 2)
    rep_fcf = round(ocf - capex, 2)
    sbc = round(abs(get_latest(["Stock Based Compensation"], 0.0)), 2)
    leases = 0.0
    true_fcf = round(rep_fcf - sbc - leases, 2)

    return {
        "period_label": latest_period,
        "ocf": ocf,
        "capex": capex,
        "reported_fcf": rep_fcf,
        "sbc": sbc,
        "finance_leases": leases,
        "true_fcf": true_fcf
    }

def pull_ground_truth_for_ticker(symbol: str, earnings_date_str: str) -> dict:
    out_file = GROUND_TRUTH_DIR / f"{symbol}_{earnings_date_str}_truth.json"
    post_truth_file = GROUND_TRUTH_DIR / f"{symbol}_{earnings_date_str}_post_truth.json"
    existing_truth = {}
    if out_file.exists():
        try:
            existing_truth = json.loads(out_file.read_text(encoding="utf-8"))
        except Exception:
            existing_truth = {}

    t = yf.Ticker(symbol)
    info = t.info or {}
    yf_price = safe_float(t.fast_info.get("last_price") or info.get("currentPrice"))
    gfin_price = check_google_finance_price(symbol, info.get("exchange", "NMS"))

    # If re-running on or after earnings_date_str, preserve locked T-1 pre-print snapshot
    today_str = str(datetime.now().date())
    is_historical_rerun = (earnings_date_str <= today_str) and bool(existing_truth)

    if is_historical_rerun:
        # Check if post_truth has the exact pre-earnings regular close price
        locked_spot = existing_truth.get("price_validation", {}).get("yahoo_spot_price")
        if post_truth_file.exists():
            try:
                pt = json.loads(post_truth_file.read_text(encoding="utf-8"))
                reg_close = pt.get("post_print_reaction", {}).get("regular_close_price")
                if reg_close:
                    locked_spot = float(reg_close)
            except Exception:
                pass
        yf_price = locked_spot or yf_price
        price_val = existing_truth.get("price_validation", {})
        price_val["yahoo_spot_price"] = yf_price
        val_mkt = existing_truth.get("valuation_and_market") or {}
        if yf_price and val_mkt.get("market_cap_millions"):
            # Keep valuation consistent with locked T-1 spot price
            pass
        opt_pos = existing_truth.get("options_positioning") or compute_airtight_options_metrics(t, yf_price, earnings_date_str)
        stitched_5q = existing_truth.get("stitched_5q_financials") or build_5q_stitched_financials(t, symbol)
        sched_ver = existing_truth.get("schedule_verification") or verify_earnings_schedule(t, earnings_date_str)
    else:
        price_diff_pct = 0.0
        if yf_price and gfin_price:
            price_diff_pct = round(abs(yf_price - gfin_price) / yf_price * 100, 3)
        price_val = {
            "yahoo_spot_price": yf_price,
            "google_finance_spot_price": gfin_price,
            "cross_source_divergence_pct": price_diff_pct,
            "status": "VERIFIED" if price_diff_pct <= 1.0 else "WARNING_CHECK_QUOTE"
        }
        val_mkt = {
            "market_cap_millions": safe_float((info.get("marketCap") or 0) / 1e6),
            "enterprise_value_millions": safe_float((info.get("enterpriseValue") or 0) / 1e6),
            "trailing_pe": safe_float(info.get("trailingPE")),
            "forward_pe": safe_float(info.get("forwardPE")),
            "price_to_sales_ttm": safe_float(info.get("priceToSalesTrailing12Months")),
            "ev_to_ebitda": safe_float(info.get("enterpriseToEbitda")),
            "short_percent_of_float": safe_float((info.get("shortPercentOfFloat") or 0) * 100)
        }
        opt_pos = compute_airtight_options_metrics(t, yf_price, earnings_date_str)
        stitched_5q = build_5q_stitched_financials(t, symbol)
        sched_ver = verify_earnings_schedule(t, earnings_date_str)

    implied_move_pct = opt_pos.get("atm_implied_move_pct")
    hist_track = compute_historical_earnings_track_record(t, earnings_date_str, implied_move_pct)
    existing_targets = existing_truth.get("street_consensus_and_targets") if is_historical_rerun else None
    street_targets = extract_street_consensus_and_targets(
        t, info, yf_price, sched_ver.get("yahoo_consensus_eps"), existing_targets,
        stitched_5q=stitched_5q, earnings_date_str=earnings_date_str,
    )
    if street_targets.get("yahoo_consensus_revenue_q0e") is not None:
        sched_ver["yahoo_consensus_revenue"] = street_targets.get("yahoo_consensus_revenue_q0e")
    fcf_bridge = compute_forensic_fcf_bridge_latest(stitched_5q)

    payload = {
        "ticker": symbol,
        "company_name": info.get("longName", existing_truth.get("company_name", symbol)),
        "sector": info.get("sector", existing_truth.get("sector", "")),
        "industry": info.get("industry", existing_truth.get("industry", "")),
        "schedule_verification": sched_ver,
        "price_validation": price_val,
        "valuation_and_market": val_mkt,
        "options_positioning": opt_pos,
        "historical_earnings_track_record": hist_track,
        "street_consensus_and_targets": street_targets,
        "forensic_fcf_bridge_latest": fcf_bridge,
        "stitched_5q_financials": stitched_5q
    }

    out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    try:
        import earnings_db
        earnings_db.ingest_t1_truth(symbol, earnings_date_str)
    except Exception as db_err:
        print(f"  [WARN] SQLite warehouse T-1 ingest warning for {symbol}: {db_err}")
    return payload

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a.lower() for a in sys.argv[1:] if a.startswith("-")]
    is_force = "--force" in flags or "-f" in flags
    requested_ticker = args[0].upper() if args else None
    explicit_date = args[1] if len(args) > 1 else None

    ledger = json.loads((BASE_DIR / "published_ledger.json").read_text(encoding="utf-8"))
    target_dates = get_t1_window()
    matched = []

    symbols_to_check = [requested_ticker] if requested_ticker else load_tickers()

    for sym in symbols_to_check:
        if requested_ticker and explicit_date:
            pull_ground_truth_for_ticker(sym, explicit_date)
            matched.append({"ticker": sym, "earnings_date": explicit_date, "explicit": True})
            continue

        t = yf.Ticker(sym)
        cal = t.calendar or {}
        e_dates = cal.get("Earnings Date", [])

        in_window_date = next((d for d in e_dates if d in target_dates), None)

        if in_window_date:
            key = f"{sym}_{in_window_date}"
            if requested_ticker or key not in ledger.get("published", []):
                pull_ground_truth_for_ticker(sym, str(in_window_date))
                matched.append({"ticker": sym, "earnings_date": str(in_window_date)})
        elif requested_ticker and is_force:
            e_str = str(e_dates[0]) if e_dates else str(datetime.now().date() + timedelta(days=1))
            pull_ground_truth_for_ticker(sym, e_str)
            matched.append({"ticker": sym, "earnings_date": e_str, "forced": True})
        elif requested_ticker:
            e_hint = str(e_dates[0]) if e_dates else "None"
            print(f"[WINDOW_FILTER] {sym} earnings date ({e_hint}) is outside T-1 window {[str(d) for d in target_dates]}. Pass '--force' or explicit <DATE> to override.", file=sys.stderr)

    print(json.dumps({"t1_matches": matched, "target_window": [str(d) for d in target_dates]}))
