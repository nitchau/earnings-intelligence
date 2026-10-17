import json
from pathlib import Path

truth = json.loads(Path("ground_truth/NVDA_2026-11-17_truth.json").read_text(encoding="utf-8"))
cf = truth["stitched_5q_financials"]["cash_flow_5q"]["metrics_millions"]
for k, v in cf.items():
    val = v["values_5q_chronological"][-1]
    if val is not None and val != 0:
        print(f"{k}: {val}")
