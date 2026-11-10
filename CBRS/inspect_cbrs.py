import json
from pathlib import Path

truth_path = Path("ground_truth/CBRS_2026-11-12_truth.json")
data = json.loads(truth_path.read_text(encoding="utf-8"))

print("=== COMPANY ===")
print("Ticker:", data.get("ticker"))
print("Name:", data.get("company_name"))
print("Sector:", data.get("sector"))
print("Industry:", data.get("industry"))

print("\n=== SCHEDULE VERIFICATION ===")
print(json.dumps(data.get("schedule_verification"), indent=2))

print("\n=== PRICE VALIDATION ===")
print(json.dumps(data.get("price_validation"), indent=2))

print("\n=== VALUATION & MARKET ===")
print(json.dumps(data.get("valuation_and_market"), indent=2))

print("\n=== OPTIONS POSITIONING ===")
print(json.dumps(data.get("options_positioning"), indent=2))

print("\n=== HISTORICAL EARNINGS TRACK RECORD ===")
print(json.dumps(data.get("historical_earnings_track_record"), indent=2))

print("\n=== STREET CONSENSUS & TARGETS ===")
print(json.dumps(data.get("street_consensus_and_targets"), indent=2))

print("\n=== FORENSIC FCF BRIDGE LATEST ===")
print(json.dumps(data.get("forensic_fcf_bridge_latest"), indent=2))

print("\n=== 5Q PERIOD HEADERS ===")
is_headers = data.get("stitched_5q_financials", {}).get("income_statement_5q", {}).get("period_headers", [])
print("Income Statement Headers:", is_headers)
cf_headers = data.get("stitched_5q_financials", {}).get("cash_flow_statement_5q", {}).get("period_headers", [])
print("Cash Flow Headers:", cf_headers)

metrics = data.get("stitched_5q_financials", {}).get("income_statement_5q", {}).get("metrics_millions", {})
print("\n=== KEY IS METRICS ===")
for k in ["Total Revenue", "Operating Revenue", "Gross Profit", "Operating Income", "Operating Expense", "Net Income", "Diluted EPS"]:
    if k in metrics:
        print(f"{k}:", metrics[k].get("values_5q_chronological"))

cf_metrics = data.get("stitched_5q_financials", {}).get("cash_flow_statement_5q", {}).get("metrics_millions", {})
print("\n=== KEY CF METRICS ===")
for k in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Stock Based Compensation"]:
    if k in cf_metrics:
        print(f"{k}:", cf_metrics[k].get("values_5q_chronological"))
