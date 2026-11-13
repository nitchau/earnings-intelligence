import json
from pathlib import Path

truth_path = Path("ground_truth/NVDA_2026-11-17_truth.json")
data = json.loads(truth_path.read_text(encoding="utf-8"))

cf_data = data["stitched_5q_financials"]["cash_flow_5q"]
print("=== CASH FLOW METRICS ===")
for k, v in cf_data["metrics_millions"].items():
    print(f"{k}: {v['values_5q_chronological']}")

bs_data = data["stitched_5q_financials"]["balance_sheet_5q"]
print("\n=== BALANCE SHEET METRICS ===")
for k, v in bs_data["metrics_millions"].items():
    print(f"{k}: {v['values_5q_chronological']}")
