import json
from pathlib import Path
from edgar import set_identity, Company

set_identity("Antigravity Research research@antigravity.ai")
company = Company("RIVN")
filings = company.get_filings(form="10-Q")
latest_10q = filings[0]
x = latest_10q.xbrl()
for s in x.statements:
    if "operations" in str(s).lower():
        df = s.to_dataframe()
        for i, r in df.iloc[:15].iterrows():
            print(f"{r.get('label', '')} | {r.get('concept', '')}")
            # print all columns ending in 2026 or 2025
            for col in df.columns:
                if "2026" in str(col) or "2025" in str(col):
                    print(f"  {col}: {r[col]}")
        break
