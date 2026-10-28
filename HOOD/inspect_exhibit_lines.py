import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')
text = Path("HOOD/exhibit_99_1.txt").read_text(encoding="utf-8")
print(f"Total characters: {len(text)}")

# Search for statements of operations / income
sections = re.findall(r"(CONDENSED CONSOLIDATED STATEMENTS OF [^\n]+)", text, re.IGNORECASE)
print("Sections found:", sections)

# Search for revenues, net income, EPS, cash flow
patterns = [
    r"Total net revenues?",
    r"Revenues were a record",
    r"Diluted EPS",
    r"Adjusted EPS",
    r"Net income",
    r"Operating income",
    r"Income before income taxes",
    r"Net cash provided by",
    r"Capital expenditures",
    r"Share-based compensation",
    r"Transaction-based revenues",
    r"Net interest revenues",
    r"Other revenues"
]

for p in patterns:
    matches = list(re.finditer(p, text, re.IGNORECASE))
    print(f"\nPattern '{p}': {len(matches)} match(es)")
    for m in matches[:3]:
        start = max(0, m.start() - 100)
        end = min(len(text), m.end() + 200)
        snippet = text[start:end].replace('\n', ' ')
        print(f"  [{m.start()}]: {snippet}")
