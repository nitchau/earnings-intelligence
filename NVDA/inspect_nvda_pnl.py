import json
from pathlib import Path

truth = json.loads(Path("ground_truth/NVDA_2026-11-17_truth.json").read_text(encoding="utf-8"))
s = truth["stitched_5q_financials"]
print("=== BASIC INFO ===")
print("Price:", truth["price_validation"])
print("Valuation:", truth["valuation_and_market"])
print("Options:", truth["options_positioning"])
print("Headers:", s["income_statement_5q"]["period_headers"])
inc = s["income_statement_5q"]["metrics_millions"]
for k in ["Total Revenue", "Operating Revenue", "Gross Profit", "Cost Of Revenue", "Operating Expense", "Research And Development", "Selling General And Administration", "Operating Income", "EBIT", "Net Income", "Diluted EPS", "Basic EPS"]:
    if k in inc:
        print(f"{k}: {inc[k]['values_5q_chronological']}")

print("\n=== CASH FLOW ===")
cf = s["cash_flow_5q"]["metrics_millions"]
for k in ["Operating Cash Flow", "Capital Expenditure", "Purchase Of PPE", "Stock Based Compensation", "Repayment Of Debt", "Issuance Of Debt"]:
    if k in cf:
        print(f"{k}: {cf[k]['values_5q_chronological']}")

print("\n=== BALANCE SHEET ===")
bs = s["balance_sheet_5q"]["metrics_millions"]
for k in ["Cash Cash Equivalents And Short Term Investments", "Total Debt", "Long Term Debt", "Current Debt", "Stockholders Equity"]:
    if k in bs:
        print(f"{k}: {bs[k]['values_5q_chronological']}")
