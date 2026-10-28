import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')
text = Path("HOOD/exhibit_99_1.txt").read_text(encoding="utf-8")

# Let's search for guidance, outlook, segment, transaction-based, net interest, other
print("=== GUIDANCE & OUTLOOK ===")
m_guidance = re.finditer(r"(guidance|outlook|full year|financial outlook|q4 2026)", text, re.IGNORECASE)
for m in m_guidance:
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 300)
    print(f"--- MATCH at {m.start()} ---")
    print(text[start:end])

print("\n=== REVENUE & SEGMENT BREAKDOWN ===")
m_seg = re.search(r"Transaction-based revenues.*?(?=Total operating expenses)", text, re.DOTALL)
if m_seg:
    print(m_seg.group(0)[:1500])
