import json
from pathlib import Path

truth_file = Path("ground_truth/TEM_2026-11-02_truth.json")
data = json.loads(truth_file.read_text(encoding="utf-8"))

is_5q = data["stitched_5q_financials"]["income_statement_5q"]
headers = is_5q["period_headers"]
metrics = is_5q["metrics_millions"]

print("Period Headers:", headers)
for key in ["Total Revenue", "Cost Of Revenue", "Reconciled Cost Of Revenue", "Gross Profit", "Operating Expense", "Operating Income", "EBIT", "Normalized EBITDA", "EBITDA", "Net Income Common Stockholders", "Diluted EPS", "Basic EPS"]:
    if key in metrics:
        vals = metrics[key]["values_5q_chronological"]
        print(f"{key}: {vals}")

cf = data.get("forensic_fcf_bridge_latest", {})
print("\nForensic FCF Bridge Latest:")
print(json.dumps(cf, indent=2))

print("\nValuation and Market:")
print(json.dumps(data.get("valuation_and_market"), indent=2))

print("\nPrice Validation:")
print(json.dumps(data.get("price_validation"), indent=2))

print("\nOptions Positioning:")
print(json.dumps(data.get("options_positioning"), indent=2))

print("\nHistorical Track Record:")
print(json.dumps(data.get("historical_earnings_track_record"), indent=2))

print("\nStreet Consensus & Targets:")
print(json.dumps(data.get("street_consensus_and_targets"), indent=2))
