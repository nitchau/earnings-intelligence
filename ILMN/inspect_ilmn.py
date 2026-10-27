import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
truth_path = BASE_DIR / "ground_truth" / "ILMN_2026-10-29_truth.json"
truth = json.loads(truth_path.read_text(encoding="utf-8"))

print("=== ILMN GROUND TRUTH SUMMARY ===")
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

inc = truth["stitched_5q_financials"]["income_statement_5q"]
cf = truth["stitched_5q_financials"]["cash_flow_5q"]
headers = inc["period_headers"]
print("\nHeaders:", headers)

for name, m_dict in inc["metrics_millions"].items():
    if name in ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Operating Expense", "Operating Income", "Net Income", "Diluted EPS", "Diluted Average Shares"]:
        print(f"{name:25s}: {m_dict.get('values_5q_chronological')}")

for name, m_dict in cf["metrics_millions"].items():
    if name in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Stock Based Compensation"]:
        print(f"{name:25s}: {m_dict.get('values_5q_chronological')}")
