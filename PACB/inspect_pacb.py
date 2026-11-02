import json
from pathlib import Path

truth_file = Path("ground_truth/PACB_2026-11-04_truth.json")
data = json.loads(truth_file.read_text(encoding="utf-8"))

is_5q = data["stitched_5q_financials"]["income_statement_5q"]
headers = is_5q["period_headers"]
metrics = is_5q["metrics_millions"]

print("=== PACB SCHEDULE VERIFICATION ===")
print(json.dumps(data.get("schedule_verification"), indent=2))

print("\n=== PERIOD HEADERS ===")
print(headers)

print("\n=== INCOME STATEMENT 5Q ===")
for key in ["Total Revenue", "Cost Of Revenue", "Reconciled Cost Of Revenue", "Gross Profit", "Operating Expense", "Operating Income", "EBIT", "Normalized EBITDA", "EBITDA", "Net Income Common Stockholders", "Diluted EPS", "Basic EPS"]:
    if key in metrics:
        vals = metrics[key]["values_5q_chronological"]
        print(f"{key}: {vals}")

cf = data.get("forensic_fcf_bridge_latest", {})
print("\n=== FORENSIC FCF BRIDGE LATEST ===")
print(json.dumps(cf, indent=2))

print("\n=== VALUATION AND MARKET ===")
print(json.dumps(data.get("valuation_and_market"), indent=2))

print("\n=== PRICE VALIDATION ===")
print(json.dumps(data.get("price_validation"), indent=2))

print("\n=== OPTIONS POSITIONING ===")
print(json.dumps(data.get("options_positioning"), indent=2))

print("\n=== HISTORICAL TRACK RECORD ===")
print(json.dumps(data.get("historical_earnings_track_record"), indent=2))

print("\n=== STREET CONSENSUS & TARGETS ===")
print(json.dumps(data.get("street_consensus_and_targets"), indent=2))
