import json
from pathlib import Path

data = json.loads(Path("ground_truth/HOOD_2026-10-27_truth.json").read_text(encoding="utf-8"))
inc = data.get("stitched_5q_financials", {}).get("income_statement_5q", {})
print("Period headers:", inc.get("period_headers"))
metrics = inc.get("metrics_millions", {})
for k in ["Total Revenue", "Operating Revenue", "Gross Profit", "Operating Expense", "Operating Income", "Net Income Common Stockholders", "Diluted EPS", "Basic EPS"]:
    if k in metrics:
        print(f"{k}: {metrics[k].get('values_5q_chronological')}")

cf = data.get("stitched_5q_financials", {}).get("cash_flow_5q", {})
print("\nCF Period headers:", cf.get("period_headers"))
cf_metrics = cf.get("metrics_millions", {})
for k in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Stock Based Compensation", "Repayment Of Debt"]:
    if k in cf_metrics:
        print(f"{k}: {cf_metrics[k].get('values_5q_chronological')}")
