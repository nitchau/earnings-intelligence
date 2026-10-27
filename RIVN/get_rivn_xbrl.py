import json
from pathlib import Path
from edgar import set_identity, Company

set_identity("Antigravity Research research@antigravity.ai")
company = Company("RIVN")
filings = company.get_filings(form="10-Q")
latest_10q = filings[0]
x = latest_10q.xbrl()
if x:
    stmts = x.statements
    for s in stmts:
        print(getattr(s, 'title', getattr(s, 'statement_name', str(s))))
        if "operations" in str(s).lower():
            df = s.to_dataframe()
            print(df.to_string())
            break
