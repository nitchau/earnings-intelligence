import json

with open("ground_truth/U_2026-11-05_truth.json") as f:
    d = json.load(f)

print("Company:", d.get("company_name"))
f5q = d.get("stitched_5q_financials", {})
print("5Q Keys:", list(f5q.keys()))

inc = f5q.get("income_statement_5q", [])
print(f"Income statement quarters: {len(inc)}")
for q in inc:
    print(q.get("fiscal_period"), q.get("date"), "Rev:", q.get("total_revenue"), "Gross:", q.get("gross_profit"), "EBIT:", q.get("operating_income"), "Net:", q.get("net_income"))

cf = f5q.get("cash_flow_5q", [])
print(f"Cash flow quarters: {len(cf)}")
for q in cf:
    print(q.get("fiscal_period"), q.get("date"), "OCF:", q.get("operating_cash_flow"), "CapEx:", q.get("capital_expenditures"), "FCF:", q.get("free_cash_flow"))

bs = f5q.get("balance_sheet_5q", [])
print(f"Balance sheet quarters: {len(bs)}")
for q in bs:
    print(q.get("fiscal_period"), q.get("date"), "Cash:", q.get("cash_and_equivalents"), "Total Debt:", q.get("total_debt"))
