import json
from pathlib import Path

truth_path = Path("c:/Users/nitin/.earningreport/ground_truth/HOOD_2026-10-27_truth.json")
truth = json.loads(truth_path.read_text(encoding="utf-8"))

print("=== SUMMARY METRICS ===")
print("Ticker:", truth["ticker"])
print("Company:", truth["company_name"])
print("Spot Price:", truth["price_validation"]["yahoo_spot_price"])
print("Market Cap ($M):", truth["valuation_and_market"]["market_cap_millions"])
print("Enterprise Value ($M):", truth["valuation_and_market"]["enterprise_value_millions"])
print("Trailing P/E:", truth["valuation_and_market"]["trailing_pe"])
print("Forward P/E:", truth["valuation_and_market"]["forward_pe"])
print("P/S TTM:", truth["valuation_and_market"]["price_to_sales_ttm"])
print("Short Float %:", truth["valuation_and_market"]["short_percent_of_float"])

print("\n=== OPTIONS POSITIONING ===")
print("Expiry strictly after earnings:", truth["options_positioning"]["expiry_strictly_after_earnings"])
print("ATM Straddle USD:", truth["options_positioning"]["atm_straddle_usd"])
print("ATM Implied Move %:", truth["options_positioning"]["atm_implied_move_pct"])
print("ATM IV %:", truth["options_positioning"]["atm_implied_volatility_pct"])
print("Put/Call OI Ratio:", truth["options_positioning"]["put_call_oi_ratio"])

print("\n=== HISTORICAL EARNINGS TRACK RECORD ===")
ht = truth["historical_earnings_track_record"]
print("Beats:", ht["beats_count"], "/", ht["quarters_evaluated"], f"({ht['beat_rate_pct']}%)")
print("Avg EPS Surprise %:", ht["avg_eps_surprise_pct"])
print("Avg Hist 1D Move %:", ht["avg_historical_1d_move_abs_pct"])
print("Implied vs Hist Delta %:", ht["implied_vs_historical_move_delta_pct"])
print("Vol Regime:", ht["options_vol_regime"])
for q in ht["prior_4q_releases"]:
    print(" ", q)

print("\n=== STREET CONSENSUS & TARGETS ===")
st = truth["street_consensus_and_targets"]
print("Mean PT:", st["target_mean_price"])
print("Median PT:", st["target_median_price"])
print("High PT:", st["target_high_price"])
print("Low PT:", st["target_low_price"])
print("Upside to Mean %:", st["implied_upside_to_mean_pct"])
print("Analyst Count:", st["analyst_count"])
print("Consensus EPS Q0E:", st["yahoo_consensus_eps_q0e"])

print("\n=== FORENSIC FCF BRIDGE LATEST ===")
fcf = truth["forensic_fcf_bridge_latest"]
for k, v in fcf.items():
    print(f" {k}: {v}")

print("\n=== 5Q FINANCIALS QUARTERS ===")
s5 = truth["stitched_5q_financials"]
inc = s5["income_statement_5q"]
cf = s5["cash_flow_5q"]
bs = s5["balance_sheet_5q"]
q_names = list(inc.get("Total Revenue", {}).keys())
print("Quarters found:", q_names)
for metric in ["Total Revenue", "Operating Revenue", "Gross Profit", "Operating Expense", "Operating Income", "Net Income"]:
    if metric in inc:
        print(f"{metric}:", inc[metric])

print("\n=== CASH FLOW METRICS ===")
for metric in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Stock Based Compensation"]:
    if metric in cf:
        print(f"{metric}:", cf[metric])

print("\n=== BALANCE SHEET METRICS ===")
for metric in ["Cash And Cash Equivalents", "Cash Financial", "Total Debt", "Stockholders Equity"]:
    if metric in bs:
        print(f"{metric}:", bs[metric])
