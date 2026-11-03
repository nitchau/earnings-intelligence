import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
truth = json.loads((BASE_DIR / "ground_truth" / "TXG_2026-11-05_truth.json").read_text(encoding="utf-8"))

print("=== TXG GROUND TRUTH INSPECTION ===")
print("Ticker:", truth.get("ticker"))
print("Company:", truth.get("company_name"))
print("Sector:", truth.get("sector"), "| Industry:", truth.get("industry"))
print("Schedule:", truth.get("schedule_verification"))
print("Price:", truth.get("price_validation"))
print("Valuation:", truth.get("valuation_and_market"))
print("Options:", truth.get("options_positioning"))
print("Historical Track Record:", truth.get("historical_earnings_track_record"))
print("Street Targets:", truth.get("street_consensus_and_targets"))
print("FCF Bridge:", truth.get("forensic_fcf_bridge_latest"))

stitched = truth.get("stitched_5q_financials", {})
inc = stitched.get("income_statement_5q", {})
print("\nPeriod Headers:", inc.get("period_headers", []))
for k in ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Operating Expense", "Operating Income", "EBITDA", "Net Income"]:
    v = inc.get("metrics_millions", {}).get(k, {})
    print(f"  {k}:", v.get("values_5q_chronological"), "Latest:", v.get("q0_latest"))
