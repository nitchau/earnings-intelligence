import json
from pathlib import Path
from edgar import set_identity, Company

set_identity("Antigravity Research research@antigravity.ai")
company = Company("RIVN")
filings = company.get_filings(form="10-Q")
print(f"Total 10-Q filings: {len(filings)}")

latest_10q = filings[0]
print(f"Filing Date: {latest_10q.filing_date}, Period: {latest_10q.period_of_report}")

obj = latest_10q.obj()
statements = obj.statements
for s in statements:
    name = getattr(s, "name", str(s))
    if any(w in name.lower() for w in ["operations", "income", "revenue", "segment"]):
        print(f"Statement: {name}")

for s in statements:
    name = getattr(s, "name", str(s))
    if "operations" in name.lower() or "income" in name.lower():
        df = s.to_dataframe()
        print(f"\n--- {name} ---")
        print(df.head(20).to_string())
        break
