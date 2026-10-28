import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
text = Path("HOOD/exhibit_99_1.txt").read_text(encoding="utf-8")
print("=== NON-GAAP RECONCILIATIONS ===")
print(text[22000:32000])
