from edgar import Company, set_identity
from bs4 import BeautifulSoup
import json

set_identity('PortfolioResearch research@local.dev')
c = Company('HOOD')
filings = c.get_filings(form=['8-K']).latest(5)
f0 = filings[0]
print(f"Form: {f0.form}, Date: {f0.filing_date}, Accession: {f0.accession_no}")
print("Items:", getattr(f0, "items", []))
print("Attachments:")
for att in getattr(f0, "attachments", []):
    desc = getattr(att, "description", "")
    doc = getattr(att, "document", "")
    print(f"  Doc: {doc}, Desc: {desc}")

# Find exhibit 99.1
ex_text = None
for att in getattr(f0, "attachments", []):
    desc = getattr(att, "description", "").lower()
    doc_name = att.document.lower()
    if "99.1" in desc or "exhibit99" in doc_name or "ex-99" in doc_name or "991" in doc_name or "press" in desc:
        print(f"Downloading {att.document}...")
        raw = att.download()
        soup = BeautifulSoup(raw, "html.parser")
        ex_text = soup.get_text("\n", strip=True)
        break

if not ex_text:
    ex_text = f0.text()

print(f"Exhibit length: {len(ex_text) if ex_text else 0}")
print("Preview:")
print(ex_text[:1000] if ex_text else "None")
