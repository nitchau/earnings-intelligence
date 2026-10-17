import re
from pathlib import Path
from edgar import Company, set_identity

set_identity("PortfolioResearch research@local.dev")
c = Company("NVDA")
filing = c.get_filings(form="10-Q")[0]
text = filing.text()

res = []
for kw in ["Market Platform", "Data Center revenue", "Gaming revenue"]:
    idx = text.lower().find(kw.lower())
    if idx != -1:
        res.append(f"Found {kw}:\n" + text[idx:idx+1500] + "\n" + "="*40)

Path("NVDA/platforms_raw.txt").write_text("\n".join(res), encoding="utf-8")
print("Saved platforms to NVDA/platforms_raw.txt")
