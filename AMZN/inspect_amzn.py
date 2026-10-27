import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
truth_path = BASE_DIR / "ground_truth" / "AMZN_2026-10-29_truth.json"
truth = json.loads(truth_path.read_text(encoding="utf-8"))

print("=== AMZN GROUND TRUTH SUMMARY ===")
print("Company:", truth.get("company_name"))
print("Sector:", truth.get("sector"))
print("Industry:", truth.get("industry"))
print("Schedule:", truth.get("schedule_verification"))
print("Spot Price:", truth.get("price_validation"))
print("Valuation:", truth.get("valuation_and_market"))
print("Options:", truth.get("options_positioning"))
print("Historical Track Record:", truth.get("historical_earnings_track_record"))
print("Street Consensus & Targets:", truth.get("street_consensus_and_targets"))
print("Forensic FCF Bridge Latest:", truth.get("forensic_fcf_bridge_latest"))

print("\n=== STITCHED 5Q FINANCIALS ===")
for q in truth.get("stitched_5q_financials", []):
    print(f"Quarter: {q.get('quarter_label')}")
    print(f"  Revenue: {q.get('total_revenue')}")
    print(f"  Gross Profit: {q.get('gross_profit')}")
    print(f"  OpEx: {q.get('operating_expenses')}")
    print(f"  Op Income: {q.get('operating_income')}")
    print(f"  Net Income: {q.get('net_income')}")
    print(f"  OCF: {q.get('operating_cash_flow')}")
    print(f"  CapEx: {q.get('capital_expenditures')}")
    print(f"  FCF: {q.get('free_cash_flow')}")
