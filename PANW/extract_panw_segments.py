from edgar import Company, set_identity
set_identity("PortfolioResearch research@local.dev")
c = Company("PANW")
filing_10k = c.get_filings(form="10-K")[0]
doc = filing_10k.obj()
print("10-K financial statements:")
try:
    income_stmt = doc.income_statement
    print(income_stmt)
except Exception as e:
    print("Error:", e)
