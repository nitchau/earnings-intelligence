import json
from pathlib import Path

truth = json.loads(Path("ground_truth/ISRG_2026-10-20_truth.json").read_text(encoding="utf-8"))
s = truth["stitched_5q_financials"]
headers = s["income_statement_5q"]["period_headers"]
print("Headers:", headers)

print("\n--- Income Statement ---")
inc = s["income_statement_5q"]["metrics_millions"]
for k in ["Total Revenue", "Operating Revenue", "Gross Profit", "Cost Of Revenue", "Operating Expense", "Research And Development", "Selling General And Administration", "Operating Income", "EBIT", "Net Income", "Diluted EPS", "Basic EPS", "EBITDA"]:
    if k in inc:
        print(f"{k}: {inc[k]['values_5q_chronological']}")

print("\n--- Cash Flow Statement ---")
cf = s["cash_flow_5q"]["metrics_millions"]
for k in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Stock Based Compensation", "Net PPE Purchase And Sale", "Purchase Of PPE"]:
    if k in cf:
        print(f"{k}: {cf[k]['values_5q_chronological']}")

print("\n--- Balance Sheet ---")
bs = s["balance_sheet_5q"]["metrics_millions"]
for k in ["Cash Cash Equivalents And Short Term Investments", "Cash And Cash Equivalents", "Other Short Term Investments", "Total Debt", "Long Term Debt", "Capital Lease Obligations", "Working Capital", "Stockholders Equity"]:
    if k in bs:
        print(f"{k}: {bs[k]['values_5q_chronological']}")

if "sec_edgar_filings_meta" in s:
    print("\n--- SEC EDGAR Meta ---")
    print(json.dumps(s["sec_edgar_filings_meta"], indent=2)[:500])
