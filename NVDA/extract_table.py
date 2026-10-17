from pathlib import Path
from edgar import Company, set_identity

set_identity("PortfolioResearch research@local.dev")
c = Company("NVDA")
filing = c.get_filings(form="10-Q")[0]
text = filing.text()

idx = text.find("Revenue by Market Platform")
Path("NVDA/market_platforms_table.txt").write_text(text[idx:idx+2500], encoding="utf-8")
print("Saved market platforms table")
