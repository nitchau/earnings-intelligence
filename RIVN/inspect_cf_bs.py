import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "RIVN_2026-10-29_truth.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
cf = truth["stitched_5q_financials"]["cash_flow_5q"]["metrics_millions"]
bs = truth["stitched_5q_financials"]["balance_sheet_5q"]["metrics_millions"]

print("--- Cash Flow ---")
for k in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Stock Based Compensation"]:
    if k in cf:
        print(f"{k}: {cf[k]['values_5q_chronological']}")

print("\n--- Balance Sheet ---")
for k in ["Cash Cash Equivalents And Short Term Investments", "Total Debt", "Net Debt", "Ordinary Shares Number"]:
    if k in bs:
        print(f"{k}: {bs[k]['values_5q_chronological']}")
