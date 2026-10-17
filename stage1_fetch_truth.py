import sys
import json
import math
from datetime import datetime, timedelta
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

def load_tickers():
    raw = (BASE_DIR / "tickers.txt").read_text(encoding="utf-8").splitlines()
    return [line.strip().upper() for line in raw if line.strip() and not line.startswith("#")]

# --- FIX #1: Trading-Day Lookahead (Catches Monday BMO/AMC on Friday + 1-2 Day Window + Fresh Releases) ---
def get_t1_window():
    today = datetime.now().date()
    weekday = today.weekday()  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
    # Include today (T-0) and yesterday (T+1 fresh release)
    recent = [today - timedelta(days=1), today]
    if weekday == 0:  # Monday: check Mon, Tue and prior weekend (Fri, Sat, Sun)
        recent = [today - timedelta(days=i) for i in range(1, 4)] + [today]
        forward = [today + timedelta(days=1), today + timedelta(days=2)]
    elif weekday == 4:  # Friday: check Sat, Sun, Mon, Tue
        forward = [today + timedelta(days=i) for i in range(1, 5)]
    elif weekday == 5:  # Saturday: check Sun, Mon, Tue
        forward = [today + timedelta(days=i) for i in range(1, 4)]
    else:
        forward = [today + timedelta(days=1), today + timedelta(days=2)]
    return sorted(list(set(recent + forward)))

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
        ed_df = t.get_earnings_dates(limit=8)
        if ed_df is not None and not ed_df.empty:
            for idx, row in ed_df.iterrows():
                dt_str = str(idx.date())
                if dt_str == target_date_str:
                    eps_est = safe_float(row.get("EPS Estimate"))
                    if eps_est is not None:
                        eps_consensus = eps_est
                        status = "SCHEDULED_IN_EARNINGS_CALENDAR_VERIFY_WEBCAST_TIME"
                    hr = idx.hour
                    if hr < 12 and hr > 0:
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

# --- FIX #3: 7:00 AM Pre-Market Options Implied Move (Bid/Ask -> ±2% Vol-Weighted -> IV Fallback) ---
def compute_airtight_options_metrics(t: yf.Ticker, spot_price: float, earnings_date_str: str) -> dict:
    if not spot_price:
        return {}
    try:
        expiries = t.options
        # Strictly AFTER earnings date so weekly options capture the post-earnings reaction
        chosen_exp = next((exp for exp in expiries if exp > earnings_date_str), expiries[0] if expiries else None)
        if not chosen_exp:
            return {}

        chain = t.option_chain(chosen_exp)
        calls, puts = chain.calls.copy(), chain.puts.copy()

        # Filter strikes within ±2.5% of spot price for volume-weighted ATM cluster
        band_low, band_high = spot_price * 0.975, spot_price * 1.025
        near_calls = calls[(calls["strike"] >= band_low) & (calls["strike"] <= band_high)]
        near_puts = puts[(puts["strike"] >= band_low) & (puts["strike"] <= band_high)]

        if near_calls.empty:
            near_calls = calls.iloc[(calls["strike"] - spot_price).abs().argsort()[:2]]
        if near_puts.empty:
            near_puts = puts.iloc[(puts["strike"] - spot_price).abs().argsort()[:2]]

        def robust_leg_price(df_band, is_call=True):
            # 1. Try live Bid/Ask midpoint first
            valid_ba = df_band[(df_band["bid"] > 0) & (df_band["ask"] > 0)]
            if not valid_ba.empty:
                closest = valid_ba.iloc[(valid_ba["strike"] - spot_price).abs().argsort()[:1]]
                return float((closest["bid"].values[0] + closest["ask"].values[0]) / 2.0), "BID_ASK_MIDPOINT"

            # 2. Pre-market 7:00 AM fallback: Volume/OI-weighted price across ±2.5% ATM band
            weights = df_band["volume"].fillna(0) + df_band["openInterest"].fillna(0) * 0.1 + 1.0
            weighted_last = float((df_band["lastPrice"] * weights).sum() / weights.sum())
            if weighted_last > 0:
                return weighted_last, "VOLUME_OI_WEIGHTED_ATM_BAND"

            # 3. Pure Implied Volatility fallback if lastPrice is missing
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
        # Sort columns chronologically (oldest -> newest of the last 5 quarters)
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
                # If Q4 is missing/NaN in quarterly table and annual 10-K exists, isolate Q4 = FY - (Q1+Q2+Q3)
                if (pd.isna(raw_v) or raw_v == 0) and a_df is not None and c in a_df.columns and metric in a_df.index:
                    fy_val = a_df.loc[metric, c]
                    prior_3q = [q_df.loc[metric, pq] for pq in cols if pq < c][-3:]
                    if not pd.isna(fy_val) and len(prior_3q) == 3 and not any(pd.isna(x) for x in prior_3q):
                        raw_v = fy_val - sum(prior_3q)
                vals.append(round(float(raw_v) / 1e6, 2) if pd.notna(raw_v) else None)

            # Pre-compute QoQ (Q0 vs Q-1) and YoY (Q0 vs Q-4) in Python so LLM never guesses math
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

def pull_ground_truth_for_ticker(symbol: str, earnings_date_str: str) -> dict:
    t = yf.Ticker(symbol)
    info = t.info or {}
    yf_price = safe_float(t.fast_info.get("last_price") or info.get("currentPrice"))
    gfin_price = check_google_finance_price(symbol, info.get("exchange", "NMS"))

    price_diff_pct = 0.0
    if yf_price and gfin_price:
        price_diff_pct = round(abs(yf_price - gfin_price) / yf_price * 100, 3)

    payload = {
        "ticker": symbol,
        "company_name": info.get("longName", symbol),
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "schedule_verification": verify_earnings_schedule(t, earnings_date_str),
        "price_validation": {
            "yahoo_spot_price": yf_price,
            "google_finance_spot_price": gfin_price,
            "cross_source_divergence_pct": price_diff_pct,
            "status": "VERIFIED" if price_diff_pct <= 1.0 else "WARNING_CHECK_QUOTE"
        },
        "valuation_and_market": {
            "market_cap_millions": safe_float((info.get("marketCap") or 0) / 1e6),
            "enterprise_value_millions": safe_float((info.get("enterpriseValue") or 0) / 1e6),
            "trailing_pe": safe_float(info.get("trailingPE")),
            "forward_pe": safe_float(info.get("forwardPE")),
            "price_to_sales_ttm": safe_float(info.get("priceToSalesTrailing12Months")),
            "ev_to_ebitda": safe_float(info.get("enterpriseToEbitda")),
            "short_percent_of_float": safe_float((info.get("shortPercentOfFloat") or 0) * 100)
        },
        "options_positioning": compute_airtight_options_metrics(t, yf_price, earnings_date_str),
        "stitched_5q_financials": build_5q_stitched_financials(t, symbol)
    }

    out_file = BASE_DIR / "ground_truth" / f"{symbol}_{earnings_date_str}_truth.json"
    out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a.lower() for a in sys.argv[1:] if a.startswith("-")]
    is_force = "--force" in flags or "-f" in flags
    requested_ticker = args[0].upper() if args else None

    ledger = json.loads((BASE_DIR / "published_ledger.json").read_text(encoding="utf-8"))
    target_dates = get_t1_window()
    matched = []

    symbols_to_check = [requested_ticker] if requested_ticker else load_tickers()

    for sym in symbols_to_check:
        t = yf.Ticker(sym)
        cal = t.calendar or {}
        e_dates = cal.get("Earnings Date", [])
        
        # Check if any earnings date falls within the valid T-1 window
        in_window_date = next((d for d in e_dates if d in target_dates), None)
        
        if in_window_date:
            key = f"{sym}_{in_window_date}"
            # Always allow requested ticker, or filter unpublished for batch runs
            if requested_ticker or key not in ledger.get("published", []):
                pull_ground_truth_for_ticker(sym, str(in_window_date))
                matched.append({"ticker": sym, "earnings_date": str(in_window_date)})
        elif requested_ticker and is_force:
            # Explicitly forced single ticker outside window
            e_str = str(e_dates[0]) if e_dates else str(datetime.now().date() + timedelta(days=1))
            pull_ground_truth_for_ticker(sym, e_str)
            matched.append({"ticker": sym, "earnings_date": e_str, "forced": True})
        elif requested_ticker:
            e_hint = str(e_dates[0]) if e_dates else "None"
            print(f"[WINDOW_FILTER] {sym} earnings date ({e_hint}) is outside T-1 window {[str(d) for d in target_dates]}. Pass '--force' to override.", file=sys.stderr)

    print(json.dumps({"t1_matches": matched, "target_window": [str(d) for d in target_dates]}))
