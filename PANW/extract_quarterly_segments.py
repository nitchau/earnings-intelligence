from edgar import Company, set_identity
import pandas as pd

set_identity("PortfolioResearch research@local.dev")
c = Company("PANW")
filings = c.get_filings(form=["10-K", "10-Q"])

print("Processing filings...")
for f in filings[:6]:
    doc = f.obj()
    print(f"\n--- Filing: {f.filing_date} {f.form} ---")
    try:
        inc = doc.income_statement
        # print first few rows of income statement
        df = inc.to_dataframe()
        for idx, row in df.iterrows():
            lbl = str(row.get("label", ""))
            if any(term in lbl.lower() for term in ["revenue", "product", "subscription"]):
                print(f"  {lbl}: {dict(row)}")
    except Exception as e:
        print("Error reading income statement:", e)
