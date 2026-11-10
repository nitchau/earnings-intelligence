import json

truth = json.load(open("ground_truth/CBRS_2026-11-12_truth.json"))
s5q = truth.get("stitched_5q_financials", {})
is_dict = s5q.get("income_statement_5q", {})
print("IS Headers:", is_dict.get("period_headers"))

for metric, data in is_dict.get("metrics_millions", {}).items():
    vals = data.get("values_5q_chronological", [])
    if any(v is not None and v != 0 for v in vals):
        print(f"  {metric}: {vals}")

cf_dict = s5q.get("cash_flow_statement_5q", {})
print("\nCF Headers:", cf_dict.get("period_headers"))
for metric, data in cf_dict.get("metrics_millions", {}).items():
    vals = data.get("values_5q_chronological", [])
    if any(v is not None and v != 0 for v in vals):
        print(f"  {metric}: {vals}")
