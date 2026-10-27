from edgar import Company, set_identity
import pandas as pd

set_identity('PortfolioResearch research@local.dev')
c = Company('COIN')
filings = c.get_filings(form='10-Q')
f = filings[0]
doc = f.obj()
df = doc.financials.income_statement().to_dataframe()
for idx, r in df.iterrows():
    val = r.get('2026-06-30 (Q2)')
    val_m = val / 1e6 if pd.notnull(val) else None
    print(f"{r['label']:45s} | {r.get('dimension_member_label')} | {val_m}")
