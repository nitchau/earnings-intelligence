from edgar import Company, set_identity
from bs4 import BeautifulSoup
import re

set_identity('AntigravityResearch research@agentic.com')
comp = Company('IBM')

# 10-Q 2026-04-23 (Q1 2026)
f_q1 = comp.get_filings(form='10-Q').latest(2)[1]
soup = BeautifulSoup(f_q1.html(), 'html.parser')
for table in soup.find_all('table'):
    t = table.get_text()
    if 'Software' in t and 'Consulting' in t and 'Infrastructure' in t:
        for r in table.find_all('tr'):
            cols = [c.get_text().strip() for c in r.find_all(['td', 'th']) if c.get_text().strip()]
            if any(term in ' '.join(cols) for term in ['Total Software', 'Total Consulting', 'Total Infrastructure', 'Financing', 'Total revenue']):
                print("Q1 2026:", ' | '.join(cols))
        break
