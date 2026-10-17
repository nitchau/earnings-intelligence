import json
from pathlib import Path
try:
    from edgar import Company, set_identity
    set_identity("PortfolioResearch research@local.dev")
    c = Company("NVDA")
    filings = c.get_filings(form="10-Q")
    latest = filings[0]
    doc = latest.obj()
    print("Filing period:", latest.period_of_report)
    print("Found 10-Q successfully")
except Exception as e:
    print("EDGAR error:", e)
