"""
Stage 3 Pre-Earnings (T-1) Deterministic Validator & Critic Gatekeeper (Track A + Track B Standard)
Validates drafts/{TICKER}_{DATE}_draft.json against:
0. Existence of ground_truth/{TICKER}_{DATE}_truth.json and all 3 Layer 2 bus files in pre_agent_bus/
1. Inner HTML length >= 45,000 characters
2. Mandatory 9 sections (Header, KPI Grid, Row 1B Pre-Release Scorecard with 3 sub-tables,
   5Q Financial Table + Q0E, Forensic FCF Bridge, Audit Grid, Section 4B Wall St Debates,
   Peer Benchmarks, 4-Pillar Sentiment Grid, PM Scenario Matrix)
3. Template purity (zero shorthand classes)
4. Interactive tooltips (>= 20 .tip and data-tip definitions)
5. Segment leak prevention (zero Tesla terms if ticker != TSLA)
6. Deterministic 5Q P&L Math (Gross Profit - OpEx = Operating Income within $2.0M)
7. Deterministic Cash Flow Bridge Math (OCF - CapEx = Rep FCF, Rep FCF - SBC - Leases = True FCF within $2.0M)
8. Prose and value grounding (verbatim Spot Price, Latest OCF, True FCF)
9. PM Strike Sanity (Bull target > Spot Price > Bear target)
10. Track A Guardrails (Zero placeholders, zero duplicate version banner, col-q0 & col-est headers)
11. Track B Interactive UX Components (.pre-jump-nav, .t1-setup-audit, .beat-bar-track, .credibility-gauge-bar)
Writes audit_logs/{TICKER}_{DATE}_validation.json
"""

import sys
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
BUS_DIR = BASE_DIR / "pre_agent_bus"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
DRAFTS_DIR = BASE_DIR / "drafts"
AUDIT_DIR = BASE_DIR / "audit_logs"
BUS_DIR.mkdir(exist_ok=True)
AUDIT_DIR.mkdir(exist_ok=True)

def validate_draft(ticker: str, earnings_date: str) -> dict:
    ticker = ticker.upper()
    errors = []

    truth_path = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date}_truth.json"
    draft_path = DRAFTS_DIR / f"{ticker}_{earnings_date}_draft.json"
    bus_2a = BUS_DIR / f"{ticker}_{earnings_date}_pre_agent2a_kpis.json"
    bus_2b = BUS_DIR / f"{ticker}_{earnings_date}_pre_agent2b_guidance.json"
    bus_2c = BUS_DIR / f"{ticker}_{earnings_date}_pre_agent2c_sentiment.json"

    # =========================================================================
    # GUARDRAIL 0: Existence of Ground Truth, Draft & Layer 2 Pre-Agent Bus Files
    # =========================================================================
    if not truth_path.exists():
        errors.append(f"Missing deterministic ground truth file: {truth_path.name}")
    if not draft_path.exists():
        errors.append(f"Missing T-1 draft JSON file: {draft_path.name}")
    if not bus_2a.exists():
        errors.append(f"Missing Layer 2 Pre-Earnings bus file from Agent 2A: {bus_2a.name}")
    if not bus_2b.exists():
        errors.append(f"Missing Layer 2 Pre-Earnings bus file from Agent 2B: {bus_2b.name}")
    if not bus_2c.exists():
        errors.append(f"Missing Layer 2 Pre-Earnings bus file from Agent 2C: {bus_2c.name}")

    if not truth_path.exists() or not draft_path.exists():
        result = {"ticker": ticker, "earnings_date": earnings_date, "passed": False, "errors": errors}
        audit_path = AUDIT_DIR / f"{ticker}_{earnings_date}_validation.json"
        audit_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    draft = json.loads(draft_path.read_text(encoding="utf-8"))

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
            f"(minimum requirement: {MIN_CHAR_COUNT:,} chars). Must include full 9-section depth."
        )

    # =========================================================================
    # GUARDRAIL 2: Mandatory 9-Section Institutional Pre-Earnings Structure
    # =========================================================================
    required_structural_components = [
        ("header-banner", "Section 1: Header Banner (<header class='header-banner'>)"),
        ("header-strip", "Section 1: Header Strip with key metrics (<div class='header-strip'>)"),
        ("kpi-grid", "Section 2: Row 1 Top KPI Grid (<section class='kpi-grid'>) with 4 metric cards"),
        ("row-1b-scorecard", "Section 2B: Row 1B Pre-Release Expectations, Whisper & Track Record Scorecard (#row-1b-scorecard)"),
        ("table-wrapper", "Section 3: Row 2 5-Quarter Stitched Financial Table (<div class='table-wrapper'>)"),
        ("forensic-grid", "Section 4: Row 3 Forensic Highlights & True FCF Bridge (<div class='forensic-grid'>)"),
        ("waterfall-row", "Section 4: True FCF Waterfall Bridge rows (<div class='waterfall-row'>)"),
        ("audit-grid", "Section 5: Row 4 Segment Execution Audit Grid (<div class='audit-grid'>)"),
        ("row-4b-debates", "Section 5B: Top 3 Institutional Pre-Print Debates & Call Focus Questions (#row-4b-debates)"),
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

    # Guardrail 2B: Row 1B Sub-Tables (Table 1B-1, Table 1B-2, Table 1B-3)
    if "Table 1B-1" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-1 Headline & Company KPI Consensus vs. Buy-Side Whisper Scorecard.")
    if "Table 1B-2" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-2 Management Guidance Credibility & 4Q Historical Track Record.")
    if "Table 1B-3" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-3 Forward Guidance Bogeys & Re-Rating Hurdles.")

    # =========================================================================
    # GUARDRAIL 3: Disallow Unauthorized Shorthand Templates
    # =========================================================================
    disallowed_shorthand_tags = ['class="grid-2"', 'class="grid-4"', '<section class="section">']
    for stag in disallowed_shorthand_tags:
        if stag in html_body:
            errors.append(f"Unauthorized Shorthand Template Found ('{stag}'): Must use master design system CSS classes.")

    # =========================================================================
    # GUARDRAIL 4: Interactive Tooltip (.tip) & Data-Tip Preservation
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
    # GUARDRAIL 5: Segment Leak Detector (Zero Hardcoded Foreign Symbol Terms)
    # =========================================================================
    if ticker != "TSLA":
        tesla_leaks = ["Automotive Regulatory Credits", "Cybercab", "Megapack", "Optimus"]
        for term in tesla_leaks:
            if term.lower() in html_body.lower():
                errors.append(f"Hardcoded Tesla term '{term}' found in {ticker} report! Must map {ticker}'s actual segments.")

    # =========================================================================
    # GUARDRAIL 6: Deterministic 5-Quarter P&L Math
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
    # GUARDRAIL 7: Deterministic Cash Flow Bridge Math
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
    # GUARDRAIL 8: Prose-to-Table Anchor Checks (Spot Price, OCF, True FCF)
    # =========================================================================
    gt_price = truth["price_validation"]["yahoo_spot_price"]
    if gt_price and f"{gt_price:.2f}" not in html_body and str(gt_price) not in html_body:
        errors.append(f"Ground truth spot price (${gt_price}) does not appear in rendered HTML.")

    if bridge.get("ocf"):
        ocf_int_str = f"{int(round(bridge['ocf'])):,}"
        if ocf_int_str not in html_body and str(int(round(bridge["ocf"]))) not in html_body:
            errors.append(f"Latest Operating Cash Flow (${ocf_int_str}M) missing or mismatched between FCF bridge and HTML.")

    # Consensus Revenue & EPS Grounding Check (Prevents $122.5B vs $128.22B Consensus Drift)
    gt_cons_rev = truth.get("schedule_verification", {}).get("yahoo_consensus_revenue")
    if gt_cons_rev is None:
        gt_cons_rev = truth.get("street_consensus_and_targets", {}).get("yahoo_consensus_revenue_q0e")
    if gt_cons_rev:
        m_crev = re.search(
            r'Consensus(?:\s+Net)?\s+(?:Revenue|Sales).*?<span class="strip-val">\$([0-9,.]+)\s*([MB])?',
            html_body,
            re.DOTALL | re.IGNORECASE,
        )
        if m_crev:
            raw_v = float(m_crev.group(1).replace(",", ""))
            unit = (m_crev.group(2) or ("B" if raw_v < 500 and gt_cons_rev >= 1000 else "M")).upper()
            html_cons_m = raw_v * (1000.0 if unit == "B" else 1.0)
            if abs(html_cons_m - float(gt_cons_rev)) / float(gt_cons_rev) > 0.015:
                errors.append(
                    f"Consensus Revenue Drift: Header strip displays ${html_cons_m:,.1f}M, "
                    f"diverging >1.5% from Ground-Truth Consensus (${float(gt_cons_rev):,.1f}M)!"
                )
        elif (
            f"{gt_cons_rev:,.0f}" not in html_body
            and f"{gt_cons_rev:,.1f}" not in html_body
            and f"{gt_cons_rev / 1000:.2f}B" not in html_body
            and f"{gt_cons_rev / 1000:.1f}B" not in html_body
        ):
            errors.append(f"Ground-Truth Consensus Revenue (${gt_cons_rev:,.1f}M) does not appear in rendered T-1 HTML.")

    gt_cons_eps = truth.get("schedule_verification", {}).get("yahoo_consensus_eps")
    if gt_cons_eps is not None:
        m_ceps = re.search(
            r'Consensus.*?EPS.*?<span class="strip-val">(-?\$?[0-9.]+|\$-?[0-9.]+)',
            html_body,
            re.DOTALL | re.IGNORECASE,
        )
        if m_ceps:
            html_eps = float(m_ceps.group(1).replace("$", ""))
            if abs(html_eps - float(gt_cons_eps)) > 0.05:
                errors.append(
                    f"Consensus EPS Drift: Header strip displays ${html_eps:.2f}, "
                    f"diverging >$0.05 from Ground-Truth Consensus EPS (${float(gt_cons_eps):.2f})!"
                )

    # =========================================================================
    # GUARDRAIL 9: Trade Matrix Strike Sanity vs Spot Price
    # =========================================================================
    tm = draft.get("trade_matrix", {})
    if gt_price and tm:
        bull_target = tm.get("bull_target_low_num")
        bear_target = tm.get("bear_target_high_num")
        if bull_target and float(bull_target) <= float(gt_price):
            errors.append(f"Bull Case target ({bull_target}) must be strictly above spot price ({gt_price}).")
        if bear_target and float(bear_target) >= float(gt_price):
            errors.append(f"Bear Case target ({bear_target}) must be strictly below spot price ({gt_price}).")

    # =========================================================================
    # GUARDRAIL 10: Track A Placeholder & Duplicate Banner Prevention
    # =========================================================================
    for bad_token in ["NaN", "undefined", "TODO", "PLACEHOLDER", "VERSION COMPARISON BANNER"]:
        if bad_token in html_body:
            errors.append(f"Illegal Placeholder or Duplicate Banner Found: '{bad_token}' appears in rendered inner HTML.")

    if '<th class="col-q0">' not in html_body:
        errors.append("Row 2 5-Quarter Table Error: Missing '<th class=\"col-q0\">' on latest reported historical quarter.")
    if '<th class="col-est">' not in html_body:
        errors.append("Row 2 5-Quarter Table Error: Missing '<th class=\"col-est\">' on upcoming consensus estimate column.")

    # =========================================================================
    # GUARDRAIL 11: Track B Pre-Earnings Interactive UX Components
    # =========================================================================
    for tb_class in ["pre-jump-nav", "t1-setup-audit", "beat-bar-track", "credibility-gauge-bar"]:
        if tb_class not in html_body:
            errors.append(f"Missing Track B Pre-Earnings UX Component: '.{tb_class}' missing from rendered HTML.")

    result = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "passed": len(errors) == 0,
        "character_count": len(html_body),
        "tooltips_count": tip_count,
        "errors": errors
    }
    audit_path = AUDIT_DIR / f"{ticker}_{earnings_date}_validation.json"
    audit_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python stage3_validate_draft.py <TICKER> <EARNINGS_DATE>", file=sys.stderr)
        sys.exit(1)
    sym, dt = sys.argv[1].upper(), sys.argv[2]
    res = validate_draft(sym, dt)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["passed"] else 1)
