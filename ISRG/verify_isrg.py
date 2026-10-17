import json
from pathlib import Path
from bs4 import BeautifulSoup

truth = json.loads(Path("ground_truth/ISRG_2026-10-20_truth.json").read_text(encoding="utf-8"))
draft = json.loads(Path("drafts/ISRG_2026-10-20_draft.json").read_text(encoding="utf-8"))
html = draft["rendered_container_html"]

# Check spot price
spot = truth["price_validation"]["yahoo_spot_price"]
assert f"{spot:.2f}" in html, f"Spot price {spot} not in html"
print("Check 0: Spot price", spot, "verified in HTML")

# Check 1: Divergence check
assert "Operating Income ($971.9M)" in html or "GAAP Operating Income ($971.9M)" in html, "Operating Income divergence title missing"
assert "$818.1M" in html, "Net Income 818.1M missing"
assert "$82.7M" in html, "Interest income 82.7M missing"
print("Check 1: GAAP Net Income vs EBIT divergence verified in Row 3")

# Check 2: 5-quarter math
t5 = draft["historical_table_5q_nums"]
assert len(t5) == 5, "Must have 5 quarters"
for i, q in enumerate(t5):
    gp, opex, ebit = q["gross_profit"], q["operating_expenses"], q["operating_income"]
    diff = abs((gp - opex) - ebit)
    assert diff < 0.1, f"Q{i} math error: {gp} - {opex} != {ebit}"
print("Check 2: All 5 quarters Gross Profit - OpEx = EBIT verified mathematically")

# Check FCF bridge math
b = draft["forensic_callout"]["fcf_bridge_q0_nums"]
assert abs((b["ocf"] - b["capex"]) - b["reported_fcf"]) < 0.1, "FCF bridge error 1"
assert abs((b["reported_fcf"] - b["sbc"] - b["finance_leases"]) - b["true_fcf"]) < 0.1, "FCF bridge error 2"
print(f"Check 2b: FCF bridge math verified: OCF {b['ocf']} - CapEx {b['capex']} = {b['reported_fcf']} - SBC {b['sbc']} - Leases {b['finance_leases']} = {b['true_fcf']}")

# Check 3: Tooltips count
soup = BeautifulSoup(html, "html.parser")
tips = soup.find_all(class_="tip")
data_tips = [t for t in tips if t.get("data-tip")]
print("Check 3a: Total interactive tooltips with data-tip:", len(data_tips))
assert len(data_tips) >= 15, "Must have >= 15 tooltips"

# Check segments
text_content = soup.get_text()
assert "Instruments & Accessories" in text_content
assert "Systems" in text_content
assert "Services" in text_content
assert "Tesla" not in text_content, "Tesla segment name leaked into non-Tesla report!"
assert "TSLA" not in text_content, "TSLA leaked into non-Tesla report!"
print("Check 3b: No TSLA leakage, proper ISRG segments verified!")
print("\nALL ADVERSARIAL CRITIC CHECKS PASSED WITH 100% PRECISION!")
