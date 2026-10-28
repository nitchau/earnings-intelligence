import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')
text = Path("HOOD/exhibit_99_1.txt").read_text(encoding="utf-8")

# Let's inspect the statement of operations around character 14000 to 22000
print("=== STATEMENT OF OPERATIONS & CASH FLOWS ===")
print(text[14000:23000])
