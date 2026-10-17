import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
truth_path = BASE_DIR / "ground_truth" / "NVDA_2026-11-17_truth.json"
truth = json.loads(truth_path.read_text(encoding="utf-8"))

print("=== BASIC INFO ===")
print("Company:", truth["company_name"])
print("Sector:", truth["sector"])
print("Industry:", truth["industry"])
print("Price Validation:", truth["price_validation"])
print("Valuation:", truth["valuation_and_market"])
print("Schedule:", truth["schedule_verification"])
print("Options:", truth["options_positioning"])

s = truth["stitched_5q_financials"]
print("\n=== INCOME STATEMENT PERIODS ===")
print("Headers:", s["income_statement_5q"]["period_headers"])

print("\n=== INCOME STATEMENT METRICS ===")
inc = s["income_statement_5q"]["metrics_millions"]
for k, v in inc.items():
    print(f"  {k}: {v['values_5q_chronological']}")

print("\n=== CASH FLOW STATEMENT METRICS ===")
cf = s["cash_flow_5q"]["metrics_millions"]
for k, v in cf.items():
    print(f"  {k}: {v['values_5q_chronological']}")

print("\n=== BALANCE SHEET METRICS ===")
bs = s["balance_sheet_5q"]["metrics_millions"]
for k, v in bs.items():
    print(f"  {k}: {v['values_5q_chronological']}")

print("\n=== SEC FILINGS ===")
print(json.dumps(s.get("sec_edgar_filings_meta", {}), indent=2))
