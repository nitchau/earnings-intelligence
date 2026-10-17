import re
from pathlib import Path
from edgar import Company, set_identity

set_identity("PortfolioResearch research@local.dev")
c = Company("NVDA")
filing = c.get_filings(form="10-Q")[0]
text = filing.text()

idx = text.lower().find("revenue by reportable segment")
if idx == -1:
    idx = text.lower().find("revenue by market platform")
if idx == -1:
    idx = text.lower().find("compute & networking")

out_text = text[idx:idx+4000] if idx != -1 else "NOT FOUND"
Path("NVDA/segment_raw.txt").write_text(out_text, encoding="utf-8")
print("Saved segment snippet to NVDA/segment_raw.txt")
