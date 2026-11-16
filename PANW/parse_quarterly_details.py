from edgar import Company, set_identity

set_identity("PortfolioResearch research@local.dev")
c = Company("PANW")
filings = c.get_filings(form=["10-K", "10-Q"])

for f in filings[:5]:
    doc = f.obj()
    df = doc.income_statement.to_dataframe()
    cols = [col for col in df.columns if any(y in str(col) for y in ["2025", "2026"])]
    print(f"\nFiling {f.form} on {f.filing_date}, columns: {cols}")
    for idx, row in df.iterrows():
        lbl = str(row.get("label", ""))
        if "product revenue" in lbl.lower() or "subscription" in lbl.lower():
            vals = {c: row[c] for c in cols}
            print(f"  {lbl} ({row.get('dimension_member_label')}): {vals}")
