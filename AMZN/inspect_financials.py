import json
from pathlib import Path

truth = json.loads(Path("ground_truth/AMZN_2026-10-29_truth.json").read_text(encoding="utf-8"))
inc = truth["stitched_5q_financials"]["income_statement_5q"]
cf = truth["stitched_5q_financials"]["cash_flow_5q"]
headers = inc["period_headers"]
print("Headers:", headers)

for name, m_dict in inc["metrics_millions"].items():
    if name in ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Operating Expense", "Operating Income", "Net Income", "Diluted EPS", "Diluted Average Shares"]:
        print(f"{name:25s}: {m_dict.get('values_5q_chronological')}")

for name, m_dict in cf["metrics_millions"].items():
    if name in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Stock Based Compensation"]:
        print(f"{name:25s}: {m_dict.get('values_5q_chronological')}")

print("\nFCF Bridge:", truth["forensic_fcf_bridge_latest"])
