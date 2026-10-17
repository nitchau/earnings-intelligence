import json
from pathlib import Path

truth_path = Path("ground_truth/AEVA_2026-11-04_truth.json")
data = json.loads(truth_path.read_text(encoding="utf-8"))

print("Ticker:", data.get("ticker"))
print("Earnings Date:", data.get("schedule_verification", {}).get("earnings_date"))
print("Spot Price:", data.get("price_validation", {}).get("yahoo_spot_price"))
print("Options:", data.get("options_positioning"))

inc = data["stitched_5q_financials"]["income_statement_5q"]
print("\nHeaders:", inc["period_headers"])

for k in ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Research And Development", "Selling General And Administration", "Operating Expense", "Operating Income", "Net Income"]:
    v = inc["metrics_millions"].get(k, {})
    print(f"{k}: {v.get('values_5q_chronological')} (Latest: {v.get('q0_latest')})")

cf = data["stitched_5q_financials"]["cash_flow_5q"]
for k in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Stock Based Compensation"]:
    v = cf["metrics_millions"].get(k, {})
    print(f"{k}: {v.get('values_5q_chronological')} (Latest: {v.get('q0_latest')})")

bs = data["stitched_5q_financials"]["balance_sheet_5q"]
for k in ["Cash And Cash Equivalents", "Other Short Term Investments", "Total Debt", "Net Debt", "Stockholders Equity"]:
    v = bs["metrics_millions"].get(k, {})
    print(f"{k}: {v.get('values_5q_chronological')} (Latest: {v.get('q0_latest')})")
