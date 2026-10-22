"""
Stage 4 Post-Earnings (T+0) Deterministic Validator & Critic Gatekeeper
Validates drafts/{TICKER}_{DATE}_post_draft.json against:
1. File existence (post_draft.json and all 3 bus files in post_agent_bus/)
2. Inner HTML length >= 45,000 characters
3. Mandatory 9 sections (Header, Row 1B Scorecard with 3 sub-tables, 5Q Table, FCF Bridge,
   Audit Grid, Peer Benchmarks, Sentiment Grid, PM Scenario Matrix, Citations)
4. Template purity (zero shorthand classes)
5. Interactive tooltips (>= 18 .tip and data-tip definitions)
6. Segment leak prevention (zero Tesla terms if ticker != TSLA)
7. Deterministic Accounting Math (Gross Profit - OpEx = EBIT, OCF - CapEx = Rep FCF, True FCF balance)
8. Prose and value grounding (verbatim After-Hours price, Close price, Revenue, OCF)
9. PM Strike Sanity (Bull target > After-Hours price > Bear target)
10. Track A & Track B Guardrails (Rolled Q3 2026 Actual + Q4 2026E headers, zero T-1 bleed-through, Track B widgets)
Writes audit_logs/{TICKER}_{DATE}_post_validation.json
"""

import sys
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
BUS_DIR = BASE_DIR / "post_agent_bus"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
DRAFTS_DIR = BASE_DIR / "drafts"
AUDIT_DIR = BASE_DIR / "audit_logs"

def validate_post_draft(ticker: str, earnings_date: str) -> dict:
    ticker = ticker.upper()
    errors = []

    truth_file = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date}_post_truth.json"
    draft_file = DRAFTS_DIR / f"{ticker}_{earnings_date}_post_draft.json"
    bus_2a = BUS_DIR / f"{ticker}_{earnings_date}_agent2a_kpis.json"
    bus_2b = BUS_DIR / f"{ticker}_{earnings_date}_agent2b_transcript.json"
    bus_2c = BUS_DIR / f"{ticker}_{earnings_date}_agent2c_social.json"

    # Guardrail 0: Existence of all bus files & draft
    if not truth_file.exists():
        errors.append(f"Missing deterministic ground truth file: {truth_file.name}")
    if not draft_file.exists():
        errors.append(f"Missing post draft JSON file: {draft_file.name}")
    if not bus_2a.exists():
        errors.append(f"Missing Layer 2 bus file from Agent 2A: {bus_2a.name}")
    if not bus_2b.exists():
        errors.append(f"Missing Layer 2 bus file from Agent 2B: {bus_2b.name}")
    if not bus_2c.exists():
        errors.append(f"Missing Layer 2 bus file from Agent 2C: {bus_2c.name}")

    if errors:
        result = {"ticker": ticker, "earnings_date": earnings_date, "passed": False, "errors": errors}
        out_log = AUDIT_DIR / f"{ticker}_{earnings_date}_post_validation.json"
        out_log.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

    truth = json.loads(truth_file.read_text(encoding="utf-8"))
    draft = json.loads(draft_file.read_text(encoding="utf-8"))
    html_body = draft.get("rendered_container_html", "")

    # Guardrail 1: Content Depth (>= 45,000 characters)
    MIN_CHAR_COUNT = 45000
    if len(html_body) < MIN_CHAR_COUNT:
        errors.append(
            f"TRUNCATED REPORT: Inner HTML length is {len(html_body):,} characters "
            f"(minimum requirement: {MIN_CHAR_COUNT:,} chars)."
        )

    # Guardrail 2: 9-Section Institutional Structure
    required_structural_components = [
        ("header-banner", "Section 1: Header Banner (<header class='header-banner'>)"),
        ("header-strip", "Section 1: Header Strip with key metrics (<div class='header-strip'>)"),
        ("kpi-grid", "Section 1: Executive KPI Grid (<section class='kpi-grid'>)"),
        ("scorecard", "Section 2: Row 1B Post-Release Expectations & Guidance Scorecard"),
        ("table-wrapper", "Section 3: Row 2 5-Quarter Stitched Financial Table (<div class='table-wrapper'>)"),
        ("forensic-grid", "Section 4: Row 3 Forensic Quality & True FCF Bridge (<div class='forensic-grid'>)"),
        ("waterfall-row", "Section 4: Row 3 FCF Waterfall Bridge rows (<div class='waterfall-row'>)"),
        ("audit-grid", "Section 5: Row 4 What Management Did Right vs Wrong + Q&A (<div class='audit-grid'>)"),
        ("sentiment-grid", "Section 7: Row 6 Multi-Source 4-Pillar Sentiment Grid (<div class='sentiment-grid'>)"),
        ("sentiment-meter-bar", "Section 7: Visual Sentiment Meter Bars (<div class='sentiment-meter-bar'>)"),
        ("scenario-grid", "Section 8: Row 7 Hedge Fund PM Trade Execution Matrix (<div class='scenario-grid'>)"),
        ("scenario-bull", "Section 8: Bull Case Scenario Card (<div class='scenario-bull'>)"),
        ("scenario-base", "Section 8: Base Case Scenario Card (<div class='scenario-base'>)"),
        ("scenario-bear", "Section 8: Bear Case Scenario Card (<div class='scenario-bear'>)"),
        ("trade-structure", "Section 8: Concrete Options Trade Structure (<div class='trade-structure'>)")
    ]
    for tag, desc in required_structural_components:
        if tag not in html_body:
            errors.append(f"Missing Required Section: {desc} is missing from rendered HTML.")

    # Guardrail 2B: Row 1B Sub-Tables (Table 1B-1, Table 1B-2, Table 1B-3)
    if "Table 1B-1" not in html_body and "Beat / Miss Scorecard" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-1 Headline & Company KPI Beat/Miss Scorecard.")
    if "Table 1B-2" not in html_body and "Management Execution Accountability" not in html_body and "Prior Quarter" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-2 Management Execution Accountability (Q0 Actual vs Q-1 Guidance).")
    if "Table 1B-3" not in html_body and "Forward Guidance Reset" not in html_body and "New Management Guidance" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-3 Forward Guidance Reset (New Guidance vs Street Expectations).")

    # Guardrail 3: Template Purity
    disallowed_shorthand_tags = ['class="grid-2"', 'class="grid-4"', '<section class="section">']
    for stag in disallowed_shorthand_tags:
        if stag in html_body:
            errors.append(f"Unauthorized Shorthand Template Found ('{stag}'): Must use master design system CSS classes.")

    # Guardrail 4: Interactive Tooltips (>= 18)
    tip_count = html_body.count('class="tip')
    datatip_count = html_body.count('data-tip="')
    MIN_TOOLTIPS = 18
    if tip_count < MIN_TOOLTIPS or datatip_count < MIN_TOOLTIPS:
        errors.append(f"Interactive tooltips missing: Found {tip_count} '.tip' and {datatip_count} 'data-tip' definitions (require >= {MIN_TOOLTIPS}).")

    # Guardrail 5: Segment Leak Prevention
    if ticker != "TSLA":
        tesla_leaks = ["Automotive Regulatory Credits", "Cybercab", "Megapack", "Optimus"]
        for term in tesla_leaks:
            if term.lower() in html_body.lower():
                errors.append(f"Hardcoded Tesla term '{term}' found in {ticker} report! Must map {ticker}'s actual segments.")

    # Guardrail 6: Deterministic 5-Quarter P&L Math
    table_5q = draft.get("historical_table_5q_nums", [])
    if len(table_5q) == 5:
        for q_idx, q_data in enumerate(table_5q):
            gp = q_data.get("gross_profit")
            opex = q_data.get("operating_expenses")
            ebit = q_data.get("operating_income")
            if None not in (gp, opex, ebit) and abs((gp - opex) - ebit) > 2.0:
                errors.append(f"Quarter {q_idx+1} P&L Math Error: Gross Profit ({gp}) - OpEx ({opex}) != Operating Income ({ebit})")

    # Guardrail 7: Deterministic Cash Flow Bridge Math
    bridge = draft.get("forensic_callout", {}).get("fcf_bridge_q0_nums", {})
    if bridge:
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

    # Guardrail 8: Prose and Value Grounding
    ah_price = truth.get("post_print_reaction", {}).get("after_hours_price")
    reg_price = truth.get("post_print_reaction", {}).get("regular_close_price")
    q0_rev = truth.get("beat_miss_scorecard", {}).get("revenue", {}).get("reported_actual_millions")
    q0_ocf = truth.get("forensic_fcf_bridge_q0", {}).get("ocf")

    if ah_price and f"{ah_price:.2f}" not in html_body and f"{ah_price}" not in html_body:
        errors.append(f"Ground-Truth After-Hours Price (${ah_price}) does not appear in rendered HTML.")
    if reg_price and f"{reg_price:.2f}" not in html_body and f"{reg_price}" not in html_body:
        errors.append(f"Ground-Truth Regular Close Price (${reg_price}) does not appear in rendered HTML.")
    if q0_rev and f"{q0_rev:,.0f}" not in html_body and f"{q0_rev}" not in html_body and f"{q0_rev:,.2f}" not in html_body:
        errors.append(f"Ground-Truth Q0 Revenue (${q0_rev}M) does not appear in rendered HTML.")
    if q0_ocf and f"{q0_ocf:,.0f}" not in html_body and f"{q0_ocf}" not in html_body and f"{q0_ocf:,.2f}" not in html_body:
        errors.append(f"Ground-Truth Q0 OCF (${q0_ocf}M) does not appear in rendered HTML.")

    # Guardrail 9: PM Strike Sanity
    trade_matrix = draft.get("trade_matrix", {})
    bull_target = trade_matrix.get("bull_target_low_num")
    bear_target = trade_matrix.get("bear_target_high_num")
    ref_price = ah_price or reg_price or 100.0

    if bull_target and bull_target <= ref_price:
        errors.append(f"PM Trade Logic Error: Bull target (${bull_target}) must be higher than After-Hours reference price (${ref_price}).")
    if bear_target and bear_target >= ref_price:
        errors.append(f"PM Trade Logic Error: Bear target (${bear_target}) must be lower than After-Hours reference price (${ref_price}).")

    # Guardrail 10: Placeholder Detector & T-1 Bleed-Through Prevention (Track A + Track B)
    for bad_token in ["NaN", "undefined", "TODO", "PLACEHOLDER", "T-1 PRE-EARNINGS", "VERSION COMPARISON BANNER"]:
        if bad_token in html_body:
            errors.append(f"Illegal Placeholder or T-1 Bleed-Through Found: '{bad_token}' appears in rendered inner HTML.")

    # Guardrail 11: Rolling 5Q Table & Track B Enhancements Verification
    if '<th class="col-q0">Q3 2026 (Actual)' not in html_body:
        errors.append("Row 2 5-Quarter Table Error: <th class='col-q0'> must be rolled forward to 'Q3 2026 (Actual)'.")
    if '<th class="col-est">Q4 2026E' not in html_body:
        errors.append("Row 2 5-Quarter Table Error: <th class='col-est'> must be rolled forward to 'Q4 2026E'.")
    if '<th class="col-est">Q3 2026E' in html_body:
        errors.append("Stale T-1 Table Header Found: '<th class=\"col-est\">Q3 2026E' is still present in Row 2.")

    for tb_class in ["post-jump-nav", "t1-vs-t0-audit", "beat-bar-track", "credibility-gauge-bar"]:
        if tb_class not in html_body:
            errors.append(f"Missing Track B Product Enhancement Component: '{tb_class}' missing from rendered HTML.")

    passed = len(errors) == 0
    result = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "passed": passed,
        "character_count": len(html_body),
        "tooltips_count": tip_count,
        "errors": errors
    }

    out_log = AUDIT_DIR / f"{ticker}_{earnings_date}_post_validation.json"
    out_log.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python stage4_validate_post.py <TICKER> <EARNINGS_DATE>", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2]
    res = validate_post_draft(t, d)
    if res["passed"]:
        print(f"[PASS] Stage 4 validation passed for {t} ({d}). Length: {res['character_count']:,} chars.")
        sys.exit(0)
    else:
        print(f"[FAIL] Stage 4 validation failed for {t} ({d}):", file=sys.stderr)
        for err in res["errors"]:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
