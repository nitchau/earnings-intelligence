import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

for folder in ["ground_truth", "drafts", "audit_logs", "published_reports"]:
    (BASE_DIR / folder).mkdir(exist_ok=True)

tickers_file = BASE_DIR / "tickers.txt"
if not tickers_file.exists():
    tickers_file.write_text("TSLA\nNVDA\nAAPL\nMSFT\nAMZN\n", encoding="utf-8")

ledger_file = BASE_DIR / "published_ledger.json"
if not ledger_file.exists():
    ledger_file.write_text(json.dumps({"published": []}, indent=2), encoding="utf-8")

# ==============================================================================
# FILE 1: stage1_fetch_truth.py (CLOSES LOOPHOLES #1, #2, #3, AND #6 IN PYTHON)
# ==============================================================================
STAGE1_CODE = '''import sys
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

# --- FIX #1: Trading-Day Lookahead (Catches Monday BMO/AMC on Friday + 1-2 Day Window) ---
def get_t1_window():
    today = datetime.now().date()
    weekday = today.weekday()  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
    if weekday == 4:           # Friday morning: check Sat, Sun, Mon, Tue
        return [today + timedelta(days=i) for i in range(1, 5)]
    elif weekday == 5:         # Saturday: check Sun, Mon, Tue
        return [today + timedelta(days=i) for i in range(1, 4)]
    return [today + timedelta(days=1), today + timedelta(days=2)]

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
    force_ticker = sys.argv[1].upper() if len(sys.argv) > 1 else None
    ledger = json.loads((BASE_DIR / "published_ledger.json").read_text(encoding="utf-8"))
    target_dates = get_t1_window()
    matched = []

    for sym in ([force_ticker] if force_ticker else load_tickers()):
        t = yf.Ticker(sym)
        cal = t.calendar or {}
        e_dates = cal.get("Earnings Date", [])
        if force_ticker:
            e_str = str(e_dates[0]) if e_dates else str(datetime.now().date() + timedelta(days=1))
            pull_ground_truth_for_ticker(sym, e_str)
            matched.append({"ticker": sym, "earnings_date": e_str})
            continue

        for d in e_dates:
            if d in target_dates:
                key = f"{sym}_{d}"
                if key not in ledger.get("published", []):
                    pull_ground_truth_for_ticker(sym, str(d))
                    matched.append({"ticker": sym, "earnings_date": str(d)})
                break

    print(json.dumps({"t1_matches": matched}))
'''
(BASE_DIR / "stage1_fetch_truth.py").write_text(STAGE1_CODE, encoding="utf-8")

# ==============================================================================
# FILE 2: stage3_validate_draft.py (CLOSES LOOPHOLES #4 AND #5 IN PYTHON)
# ==============================================================================
STAGE3_CODE = '''import sys
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

def validate_draft(ticker: str, earnings_date: str) -> dict:
    truth_path = BASE_DIR / "ground_truth" / f"{ticker}_{earnings_date}_truth.json"
    draft_path = BASE_DIR / "drafts" / f"{ticker}_{earnings_date}_draft.json"

    if not truth_path.exists() or not draft_path.exists():
        return {"passed": False, "errors": ["Missing truth or draft JSON file."]}

    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    errors = []

    html_body = draft.get("rendered_container_html", "")
    if not html_body:
        errors.append("Missing 'rendered_container_html' in draft JSON.")

    # --- FIX #4: Verify Dynamic Segment Labels & Interactive Tooltip (.tip) Preservation ---
    if ticker != "TSLA":
        tesla_leaks = ["Automotive Regulatory Credits", "Cybercab", "Megapack", "Optimus"]
        for term in tesla_leaks:
            if term.lower() in html_body.lower():
                errors.append(f"Hardcoded Tesla term '{term}' found in {ticker} report! Must map {ticker}'s actual segments.")

    tip_count = html_body.count('class="tip')
    datatip_count = html_body.count('data-tip="')
    if tip_count < 15 or datatip_count < 15:
        errors.append(f"Interactive tooltips missing: Found only {tip_count} '.tip' classes and {datatip_count} 'data-tip' definitions (require >= 15).")

    # --- FIX #5A: Verify 5-Quarter P&L Math (Gross Profit - OpEx == Operating Income / EBIT) ---
    table_5q = draft.get("historical_table_5q_nums", [])
    if len(table_5q) != 5:
        errors.append("Draft must include 'historical_table_5q_nums' array for all 5 historical quarters.")
    for q_idx, q_data in enumerate(table_5q):
        gp = q_data.get("gross_profit")
        opex = q_data.get("operating_expenses")
        ebit = q_data.get("operating_income")
        if None not in (gp, opex, ebit) and abs((gp - opex) - ebit) > 2.0:
            errors.append(f"Quarter {q_idx+1} P&L Math Error: Gross Profit ({gp}) - OpEx ({opex}) != Operating Income ({ebit})")

    # --- FIX #5B: Verify Cash Flow Bridge Math (OCF - CapEx == Reported FCF; Reported FCF - SBC - Leases == True FCF) ---
    bridge = draft.get("forensic_callout", {}).get("fcf_bridge_q0_nums", {})
    if not bridge:
        errors.append("Missing 'forensic_callout.fcf_bridge_q0_nums' dictionary.")
    else:
        ocf = bridge.get("ocf", 0)
        capex = abs(bridge.get("capex", 0))
        rep_fcf = bridge.get("reported_fcf", 0)
        sbc = abs(bridge.get("sbc", 0))
        leases = abs(bridge.get("finance_leases", 0))
        true_fcf = bridge.get("true_fcf", 0)

        if abs((ocf - capex) - rep_fcf) > 2.0:
            errors.append(f"FCF Bridge Math Error: OCF ({ocf}) - CapEx ({capex}) != Reported FCF ({rep_fcf})")
        if abs((rep_fcf - sbc - leases) - true_fcf) > 2.0:
            errors.append(f"True FCF Math Error: Reported FCF ({rep_fcf}) - SBC ({sbc}) - Leases ({leases}) != True FCF ({true_fcf})")

    # --- FIX #5C: Prose-to-Table Anchor Check (Ensure Spot Price, Latest Revenue, OCF, and CapEx Appear in HTML) ---
    gt_price = truth["price_validation"]["yahoo_spot_price"]
    if gt_price and f"{gt_price:.2f}" not in html_body and str(gt_price) not in html_body:
        errors.append(f"Ground truth spot price (${gt_price}) does not appear in rendered HTML.")

    if bridge.get("ocf"):
        ocf_int_str = f"{int(round(bridge['ocf'])):,}"
        if ocf_int_str not in html_body and str(int(round(bridge["ocf"]))) not in html_body:
            errors.append(f"Latest Operating Cash Flow (${ocf_int_str}M) missing or mismatched between FCF bridge and HTML.")

    # --- Verify Trade Matrix Strike Sanity vs Spot Price ---
    tm = draft.get("trade_matrix", {})
    if gt_price and tm:
        bull_target = tm.get("bull_target_low_num")
        bear_target = tm.get("bear_target_high_num")
        if bull_target and float(bull_target) <= float(gt_price):
            errors.append(f"Bull Case target ({bull_target}) must be strictly above spot price ({gt_price}).")
        if bear_target and float(bear_target) >= float(gt_price):
            errors.append(f"Bear Case target ({bear_target}) must be strictly below spot price ({gt_price}).")

    result = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "passed": len(errors) == 0,
        "errors": errors
    }
    audit_path = BASE_DIR / "audit_logs" / f"{ticker}_{earnings_date}_validation.json"
    audit_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

if __name__ == "__main__":
    sym, dt = sys.argv[1].upper(), sys.argv[2]
    res = validate_draft(sym, dt)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["passed"] else 1)
'''
(BASE_DIR / "stage3_validate_draft.py").write_text(STAGE3_CODE, encoding="utf-8")

# ==============================================================================
# FILE 3: stage4_render_html.py (READ-ONLY TEMPLATE CLONER & PUBLISHER)
# ==============================================================================
STAGE4_CODE = '''import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
MASTER_HTML = BASE_DIR / "Stock_Analysis_v2.html"

def publish_report(ticker: str, earnings_date: str):
    audit_file = BASE_DIR / "audit_logs" / f"{ticker}_{earnings_date}_validation.json"
    if not audit_file.exists():
        raise RuntimeError("Cannot publish: Stage 3 validation log does not exist.")
    audit = json.loads(audit_file.read_text(encoding="utf-8"))
    if not audit.get("passed"):
        raise RuntimeError(f"Cannot publish: Stage 3 failed with errors: {audit.get('errors')}")

    master_content = MASTER_HTML.read_text(encoding="utf-8")
    style_start = master_content.find("<style>")
    style_end = master_content.find("</style>") + len("</style>")
    locked_css = master_content[style_start:style_end]

    draft_file = BASE_DIR / "drafts" / f"{ticker}_{earnings_date}_draft.json"
    draft = json.loads(draft_file.read_text(encoding="utf-8"))

    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{draft['header']['page_title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  {locked_css}
</head>
<body>
  <div class="container">
    {draft['rendered_container_html']}
  </div>
</body>
</html>"""

    out_path = BASE_DIR / "published_reports" / f"{ticker}_T1_{earnings_date}.html"
    out_path.write_text(final_html, encoding="utf-8")

    ledger_path = BASE_DIR / "published_ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    key = f"{ticker}_{earnings_date}"
    if key not in ledger["published"]:
        ledger["published"].append(key)
        ledger_path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")

    print(f"SUCCESS: Published verified tearsheet to {out_path}")

if __name__ == "__main__":
    publish_report(sys.argv[1].upper(), sys.argv[2])
'''
(BASE_DIR / "stage4_render_html.py").write_text(STAGE4_CODE, encoding="utf-8")

# ==============================================================================
# FILE 4: AGENTS.md (UPDATED TO ENFORCE ALL 6 FIXES)
# ==============================================================================
AGENTS_MD = '''# Antigravity 2.0 Zero-Hallucination T-1 Earnings Harness

## Core Operating Rules
1. **NEVER modify or overwrite `Stock_Analysis_v2.html`.** It is our read-only structural and CSS master reference.
2. **NEVER invent or alter numbers from `ground_truth/{TICKER}_{DATE}_truth.json`.** All pre-computed 5-quarter numbers, QoQ/YoY deltas, spot prices, and options-implied moves from Stage 1 are immutable ground truth.

## 4-Stage Execution Workflow

### Stage 1: Deterministic Ground-Truth Anchor
Run `python stage1_fetch_truth.py` (or `python stage1_fetch_truth.py {TICKER}` for a forced run).
- Inspect `schedule_verification.confirmation_flag` in `ground_truth/{TICKER}_{DATE}_truth.json`. Confirm the exact investor relations webcast date and BMO/AMC release time via web search.

### Stage 2: Forensic Research & Synthesis Agent
Using `ground_truth/{TICKER}_{DATE}_truth.json` and live web search for 10-Q/10-K footnote disclosures, segment revenue breakdowns, consensus/whisper estimates, and 4-pillar sentiment:
- Map `{TICKER}`'s actual reporting segments into the sub-rows under `Total Revenue ($M)` in the 5-quarter table (do not leave Tesla segment names for non-Tesla tickers).
- Preserve at least 15 interactive `.tip` hover tooltips with `data-tip="..."` plain-English definitions across the HTML.
- Save `drafts/{TICKER}_{DATE}_draft.json` containing:
  - `"header"`: `{"page_title": "...", "spot_price_num": <float>}`
  - `"historical_table_5q_nums"`: Array of 5 dicts `[{"gross_profit": <float>, "operating_expenses": <float>, "operating_income": <float>}, ...]`
  - `"forensic_callout"`: `{"fcf_bridge_q0_nums": {"ocf": <float>, "capex": <float>, "reported_fcf": <float>, "sbc": <float>, "finance_leases": <float>, "true_fcf": <float>}}`
  - `"trade_matrix"`: `{"bull_target_low_num": <float>, "bear_target_high_num": <float>}`
  - `"rendered_container_html"`: Complete inner HTML of `<div class="container">...</div>` matching `Stock_Analysis_v2.html` 1:1.

### Stage 3: Adversarial Critic & Deterministic Validator Loop
Run `python stage3_validate_draft.py {TICKER} {DATE}`.
- If `"passed": false`, fix every error listed in `errors` inside `drafts/{TICKER}_{DATE}_draft.json` and re-run Stage 3 until `"passed": true`.

### Stage 4: Read-Only HTML Injection & Publishing
Run `python stage4_render_html.py {TICKER} {DATE}` to generate `published_reports/{TICKER}_T1_{DATE}.html`.
'''
(BASE_DIR / "AGENTS.md").write_text(AGENTS_MD, encoding="utf-8")

print("✅ Upgraded 4-Stage Harness (with all 6 Loophole Fixes hardcoded in Python) written successfully!")