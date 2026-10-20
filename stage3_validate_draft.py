import sys
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

def validate_draft(ticker: str, earnings_date: str) -> dict:
    truth_path = BASE_DIR / "ground_truth" / f"{ticker}_{earnings_date}_truth.json"
    draft_path = BASE_DIR / "drafts" / f"{ticker}_{earnings_date}_draft.json"

    if not truth_path.exists() or not draft_path.exists():
        return {"passed": False, "errors": ["Missing truth or draft JSON file."]}

    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    errors = []

    html_body = draft.get("rendered_container_html", "")
    if not html_body:
        errors.append("Missing 'rendered_container_html' in draft JSON.")
        return {"ticker": ticker, "earnings_date": earnings_date, "passed": False, "errors": errors}

    # =========================================================================
    # GUARDRAIL 1: Minimum HTML Content Length & Truncation Detector
    # =========================================================================
    MIN_CHAR_COUNT = 45000
    if len(html_body) < MIN_CHAR_COUNT:
        errors.append(
            f"TRUNCATED REPORT DETECTED: Inner HTML is only {len(html_body):,} characters "
            f"(minimum requirement: {MIN_CHAR_COUNT:,} chars). Must include full 8-card depth."
        )

    # =========================================================================
    # GUARDRAIL 2: Mandatory 8-Card Institutional Structure (Matching Stock_Analysis_v2.html)
    # =========================================================================
    required_structural_components = [
        ("header-banner", "Section 1: Header Banner (<header class='header-banner'>)"),
        ("header-strip", "Section 1: Header Strip with key metrics (<div class='header-strip'>)"),
        ("kpi-grid", "Section 2: Row 1 Top KPI Grid (<section class='kpi-grid'>) with 4 metric cards"),
        ("table-wrapper", "Section 3: Row 2 5-Quarter Stitched Financial Table (<div class='table-wrapper'>)"),
        ("forensic-grid", "Section 4: Row 3 Forensic Highlights & True FCF Bridge (<div class='forensic-grid'>)"),
        ("waterfall-row", "Section 4: True FCF Waterfall Bridge rows (<div class='waterfall-row'>)"),
        ("audit-grid", "Section 5: Row 4 Segment Execution Audit Grid (<div class='audit-grid'>)"),
        ("sentiment-grid", "Section 7: Row 6 Multi-Source 4-Pillar Sentiment Grid (<div class='sentiment-grid'>)"),
        ("sentiment-meter-bar", "Section 7: Visual Sentiment Meter Bars (<div class='sentiment-meter-bar'>)"),
        ("scenario-grid", "Section 8: Row 7 Hedge Fund PM Trade Execution Matrix (<div class='scenario-grid'>)"),
        ("scenario-bull", "Section 8: Bull Case Scenario Card (<div class='scenario-bull'>)"),
        ("scenario-base", "Section 8: Base Case / Rangebound Scenario Card (<div class='scenario-base'>)"),
        ("scenario-bear", "Section 8: Bear Case / Hedge Scenario Card (<div class='scenario-bear'>)"),
        ("trade-structure", "Section 8: Concrete Options Trade Structure (<div class='trade-structure'>)")
    ]

    for tag, desc in required_structural_components:
        if tag not in html_body:
            errors.append(f"Missing Required Section: {desc} is missing from rendered HTML.")

    # Disallow unauthorized shorthand templates
    disallowed_shorthand_tags = ["class=\"grid-2\"", "class=\"grid-4\"", "<section class=\"section\">"]
    for stag in disallowed_shorthand_tags:
        if stag in html_body:
            errors.append(f"Unauthorized Shorthand Template Found ('{stag}'): Must use master design system CSS classes.")

    # =========================================================================
    # GUARDRAIL 3: Interactive Tooltip (.tip) & Data-Tip Preservation
    # =========================================================================
    tip_count = html_body.count('class="tip')
    datatip_count = html_body.count('data-tip="')
    MIN_TOOLTIPS = 20
    if tip_count < MIN_TOOLTIPS or datatip_count < MIN_TOOLTIPS:
        errors.append(
            f"Interactive tooltips missing: Found only {tip_count} '.tip' classes and {datatip_count} 'data-tip' definitions "
            f"(require >= {MIN_TOOLTIPS})."
        )

    # =========================================================================
    # GUARDRAIL 4: Segment Leak Detector (Zero Hardcoded Foreign Symbol Terms)
    # =========================================================================
    if ticker != "TSLA":
        tesla_leaks = ["Automotive Regulatory Credits", "Cybercab", "Megapack", "Optimus"]
        for term in tesla_leaks:
            if term.lower() in html_body.lower():
                errors.append(f"Hardcoded Tesla term '{term}' found in {ticker} report! Must map {ticker}'s actual segments.")

    # =========================================================================
    # GUARDRAIL 5: Deterministic 5-Quarter P&L Math
    # =========================================================================
    table_5q = draft.get("historical_table_5q_nums", [])
    if len(table_5q) != 5:
        errors.append("Draft must include 'historical_table_5q_nums' array for all 5 historical quarters.")
    for q_idx, q_data in enumerate(table_5q):
        gp = q_data.get("gross_profit")
        opex = q_data.get("operating_expenses")
        ebit = q_data.get("operating_income")
        if None not in (gp, opex, ebit) and abs((gp - opex) - ebit) > 2.0:
            errors.append(f"Quarter {q_idx+1} P&L Math Error: Gross Profit ({gp}) - OpEx ({opex}) != Operating Income ({ebit})")

    # =========================================================================
    # GUARDRAIL 6: Deterministic Cash Flow Bridge Math
    # =========================================================================
    bridge = draft.get("forensic_callout", {}).get("fcf_bridge_q0_nums", {})
    if not bridge:
        errors.append("Missing 'forensic_callout.fcf_bridge_q0_nums' dictionary.")
    else:
        ocf = bridge.get("ocf", 0)
        capex = abs(bridge.get("capex", 0))
        rep_fcf = bridge.get("reported_fcf", 0)
        sbc = abs(bridge.get("sbc", 0))
        leases = abs(bridge.get("finance_leases", 0))
        true_fcf = bridge.get("true_fcf", 0)

        if abs((ocf - capex) - rep_fcf) > 2.0:
            errors.append(f"FCF Bridge Math Error: OCF ({ocf}) - CapEx ({capex}) != Reported FCF ({rep_fcf})")
        if abs((rep_fcf - sbc - leases) - true_fcf) > 2.0:
            errors.append(f"True FCF Math Error: Reported FCF ({rep_fcf}) - SBC ({sbc}) - Leases ({leases}) != True FCF ({true_fcf})")

    # =========================================================================
    # GUARDRAIL 7: Prose-to-Table Anchor Checks (Spot Price, OCF)
    # =========================================================================
    gt_price = truth["price_validation"]["yahoo_spot_price"]
    if gt_price and f"{gt_price:.2f}" not in html_body and str(gt_price) not in html_body:
        errors.append(f"Ground truth spot price (${gt_price}) does not appear in rendered HTML.")

    if bridge.get("ocf"):
        ocf_int_str = f"{int(round(bridge['ocf'])):,}"
        if ocf_int_str not in html_body and str(int(round(bridge["ocf"]))) not in html_body:
            errors.append(f"Latest Operating Cash Flow (${ocf_int_str}M) missing or mismatched between FCF bridge and HTML.")

    # =========================================================================
    # GUARDRAIL 8: Trade Matrix Strike Sanity vs Spot Price
    # =========================================================================
    tm = draft.get("trade_matrix", {})
    if gt_price and tm:
        bull_target = tm.get("bull_target_low_num")
        bear_target = tm.get("bear_target_high_num")
        if bull_target and float(bull_target) <= float(gt_price):
            errors.append(f"Bull Case target ({bull_target}) must be strictly above spot price ({gt_price}).")
        if bear_target and float(bear_target) >= float(gt_price):
            errors.append(f"Bear Case target ({bear_target}) must be strictly below spot price ({gt_price}).")

    result = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "passed": len(errors) == 0,
        "errors": errors
    }
    audit_path = BASE_DIR / "audit_logs" / f"{ticker}_{earnings_date}_validation.json"
    audit_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

if __name__ == "__main__":
    sym, dt = sys.argv[1].upper(), sys.argv[2]
    res = validate_draft(sym, dt)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["passed"] else 1)
