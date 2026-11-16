import json
from pathlib import Path

truth = json.loads(Path("ground_truth/PANW_2026-11-18_truth.json").read_text(encoding="utf-8"))
f5q = truth["stitched_5q_financials"]["income_statement_5q"]
headers = f5q["period_headers"]
metrics = f5q["metrics_millions"]

print("Headers:", headers)
for k in ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Operating Expense", "Research And Development", "Selling General And Administration", "Selling And Marketing Expense", "General And Administrative Expense", "Operating Income", "Net Income", "Diluted EPS", "Diluted Average Shares"]:
    if k in metrics:
        vals = metrics[k]["values_5q_chronological"]
        print(f"{k:35s}: {vals} | latest={metrics[k]['q0_latest']} | QoQ={metrics[k]['qoq_change_pct']}% | YoY={metrics[k]['yoy_change_pct']}%")

print("\n--- Check P&L Math (GP - OpEx == OpInc) ---")
gps = metrics["Gross Profit"]["values_5q_chronological"]
opexs = metrics["Operating Expense"]["values_5q_chronological"]
opincs = metrics["Operating Income"]["values_5q_chronological"]
for i in range(5):
    gp = gps[i]
    opex = opexs[i]
    opinc = opincs[i]
    diff = (gp - opex) - opinc
    print(f"Q{i+1} ({headers[i]}): GP={gp}, OpEx={opex}, OpInc={opinc}, Diff={diff:.2f}")
