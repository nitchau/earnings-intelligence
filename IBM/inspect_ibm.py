import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
with open(BASE_DIR / 'ground_truth' / 'IBM_2026-10-21_truth.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("HEADERS:", d['stitched_5q_financials']['income_statement_5q']['period_headers'])
inc = d['stitched_5q_financials']['income_statement_5q']['metrics_millions']
cf = d['stitched_5q_financials']['cash_flow_5q']['metrics_millions']
bs = d['stitched_5q_financials']['balance_sheet_5q']['metrics_millions']

print("\n--- INCOME STATEMENT KEYS ---")
for k, v in inc.items():
    if any(term in k.lower() for term in ['revenue', 'profit', 'expense', 'income', 'eps']):
        print(f"  {k}: {v['values_5q_chronological']}")

print("\n--- CASH FLOW KEYS ---")
for k, v in cf.items():
    if any(term in k.lower() for term in ['cash', 'capex', 'capital', 'stock', 'lease']):
        print(f"  {k}: {v['values_5q_chronological']}")

print("\n--- BALANCE SHEET KEYS ---")
for k, v in bs.items():
    if any(term in k.lower() for term in ['debt', 'cash', 'asset', 'liability']):
        print(f"  {k}: {v['values_5q_chronological']}")
