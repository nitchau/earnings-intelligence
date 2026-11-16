import json
from pathlib import Path

truth_file = Path("ground_truth/PANW_2026-11-18_truth.json")
if not truth_file.exists():
    print("Truth file not found!")
    exit(1)

truth = json.loads(truth_file.read_text(encoding="utf-8"))
print("=== COMPANY INFO ===")
print("Ticker:", truth.get("ticker"))
print("Company Name:", truth.get("company_name"))
print("Sector:", truth.get("sector"))
print("Industry:", truth.get("industry"))

print("\n=== SCHEDULE & PRICING ===")
print("Schedule:", truth.get("schedule_verification"))
print("Price Validation:", truth.get("price_validation"))
print("Valuation & Market:", truth.get("valuation_and_market"))
print("Options Positioning:", truth.get("options_positioning"))
print("Historical Track Record:", truth.get("historical_earnings_track_record"))
print("Street Consensus & Targets:", truth.get("street_consensus_and_targets"))

print("\n=== LATEST FCF BRIDGE ===")
print(json.dumps(truth.get("forensic_fcf_bridge_latest"), indent=2))

print("\n=== 5Q FINANCIALS SUMMARY ===")
f5q = truth.get("stitched_5q_financials", {})
print("Periods:", [p.get("period_label") for p in f5q.get("quarters", [])])
for q in f5q.get("quarters", []):
    print(f"Period: {q.get('period_label')} | Rev: {q.get('total_revenue')} | GP: {q.get('gross_profit')} | OpEx: {q.get('operating_expenses')} | OpInc: {q.get('operating_income')} | NetInc: {q.get('net_income')} | EPS: {q.get('diluted_eps')}")
