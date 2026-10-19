from edgar import Company, set_identity
from bs4 import BeautifulSoup
import re

set_identity('AntigravityResearch research@agentic.com')
comp = Company('LRCX')
f = comp.get_filings(form=['10-Q', '10-K']).latest(1)
print("Filing:", f.form, f.filing_date)
soup = BeautifulSoup(f.html(), 'html.parser')
for table in soup.find_all('table'):
    t = table.get_text()
    if 'Systems' in t and ('Customer Support' in t or 'CSBG' in t or 'Memory' in t or 'Foundry' in t):
        for r in table.find_all('tr'):
            cols = [c.get_text().strip() for c in r.find_all(['td', 'th']) if c.get_text().strip()]
            if cols:
                print(' | '.join(cols[:6]))
        break
