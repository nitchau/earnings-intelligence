import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
truth = json.loads((BASE_DIR / "ground_truth" / "LIDR_2026-11-05_truth.json").read_text(encoding="utf-8"))
stitched = truth.get("stitched_5q_financials", {})
inc = stitched.get("income_statement_5q", {})
print("Income Statement Metrics:")
for k, v in inc.items():
    if isinstance(v, dict):
        print(f"  {k}:", v)
    elif isinstance(v, list):
        print(f"  {k} (len {len(v)}):", v[:2])
    else:
        print(f"  {k}:", type(v))
