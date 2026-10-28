from edgar import Company, set_identity
from bs4 import BeautifulSoup
from pathlib import Path

set_identity('PortfolioResearch research@local.dev')
c = Company('HOOD')
filings = c.get_filings(form=['8-K']).latest(5)
f0 = filings[0]
print(f"Filing: {f0.form}, Date: {f0.filing_date}, Accession: {f0.accession_no}")

ex_text = ""
for att in getattr(f0, "attachments", []):
    desc = getattr(att, "description", "").lower()
    doc_name = att.document.lower()
    if "99.1" in desc or "exhibit99" in doc_name or "ex-99" in doc_name or "991" in doc_name or "press" in desc:
        print(f"Found Exhibit 99.1: {att.document} ({desc})")
        raw = att.download()
        soup = BeautifulSoup(raw, "html.parser")
        ex_text = soup.get_text("\n", strip=True)
        break

if not ex_text:
    ex_text = f0.text()

out_path = Path("HOOD/exhibit_99_1.txt")
out_path.write_text(ex_text, encoding="utf-8")
print(f"Saved {len(ex_text)} bytes to {out_path}")
