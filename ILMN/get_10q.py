from edgar import Company, set_identity

set_identity('PortfolioResearch research@local.dev')
c = Company('ILMN')
filings = c.get_filings(form='10-Q')
f = filings[0]
doc = f.obj()
df = doc.financials.income_statement().to_dataframe()
print("Columns:", df.columns.tolist())
for idx, r in df.iterrows():
    print(r['label'], "-->", {col: r[col] for col in df.columns if '2026' in str(col) or '2025' in str(col)})
