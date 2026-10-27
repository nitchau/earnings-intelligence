from edgar import Company, set_identity

set_identity('PortfolioResearch research@local.dev')
c = Company('INTC')
filings = c.get_filings(form='10-Q')
f = filings[0]
doc = f.obj()
df = doc.financials.income_statement().to_dataframe()
print("Columns:", df.columns.tolist())
for idx, r in df.iterrows():
    lbl = r.get('label')
    m_lbl = r.get('dimension_member_label')
    cols_vals = {c: r[c] for c in df.columns if '2026' in str(c) or '2025' in str(c)}
    print(f"{str(lbl):35s} | member: {str(m_lbl):25s} | {cols_vals}")
