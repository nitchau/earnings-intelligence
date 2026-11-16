import json
try:
    from edgar import Company, set_identity
    set_identity("PortfolioResearch research@local.dev")
    c = Company("PANW")
    filings = c.get_filings(form=["10-K", "10-Q"])
    print("Latest filings:")
    for f in filings[:5]:
        print(f.filing_date, f.form, f.accession_no)
except Exception as e:
    print("Error fetching EDGAR:", e)
