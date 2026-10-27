import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "RIVN_2026-10-29_truth.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
income_stmt = truth["stitched_5q_financials"]["income_statement_5q"]
periods = income_stmt["period_headers"]
metrics = income_stmt["metrics_millions"]

print("Periods:", periods)
for k, v in metrics.items():
    print(f"{k}: {v['values_5q_chronological']}")

gp = metrics["gross_profit"]["values_5q_chronological"]
opex = metrics["operating_expenses"]["values_5q_chronological"]
ebit = metrics["operating_income"]["values_5q_chronological"]

for i, p in enumerate(periods):
    diff = (gp[i] - opex[i]) - ebit[i]
    print(f"{p}: GP={gp[i]}, OpEx={opex[i]}, EBIT={ebit[i]} | (GP - OpEx) - EBIT = {diff:.2f}")

cash_flow = truth["stitched_5q_financials"].get("cash_flow_5q", {})
if cash_flow:
    print("\nCash Flow Metrics:")
    for k, v in cash_flow.get("metrics_millions", {}).items():
        print(f"{k}: {v['values_5q_chronological']}")

balance_sheet = truth["stitched_5q_financials"].get("balance_sheet_5q", {})
if balance_sheet:
    print("\nBalance Sheet Metrics:")
    for k, v in balance_sheet.get("metrics_millions", {}).items():
        print(f"{k}: {v['values_5q_chronological']}")
