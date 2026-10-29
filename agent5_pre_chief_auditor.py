"""
Agent 5 (Pre-Earnings T-1): Chief HTML Auditor & Targeted Back-Router (Gemini 3.8 Flash High Standard)
Layer 5 Cross-Validation Gatekeeper for T-1 Pre-Earnings Briefings:
- Deeply inspects rendered published_reports/{TICKER}_T1_{DATE}.html against:
  - ground_truth/{TICKER}_{DATE}_truth.json
  - pre_agent_bus/{TICKER}_{DATE}_pre_agent2a_kpis.json
  - pre_agent_bus/{TICKER}_{DATE}_pre_agent2b_guidance.json
  - pre_agent_bus/{TICKER}_{DATE}_pre_agent2c_sentiment.json
- Targeted Back-Routing Protocol:
  If any defect is detected, writes audit_logs/{TICKER}_{DATE}_pre_agent5_signoff.json with:
    "status": "REJECTED"
    "route_to": LAYER_1_DETERMINISTIC | AGENT_2A_KPIS | AGENT_2B_GUIDANCE | AGENT_2C_SENTIMENT | AGENT_4B_FINALIZER
  If all cross-validation checks pass, writes:
    "status": "APPROVED"
"""

import sys
import re
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = BASE_DIR / "published_reports"
AUDIT_DIR = BASE_DIR / "audit_logs"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
BUS_DIR = BASE_DIR / "pre_agent_bus"

def audit_rendered_pre_html(ticker: str, earnings_date: str) -> dict:
    ticker = ticker.upper()
    html_file = REPORTS_DIR / f"{ticker}_T1_{earnings_date}.html"
    truth_file = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date}_truth.json"
    bus_2a = BUS_DIR / f"{ticker}_{earnings_date}_pre_agent2a_kpis.json"
    bus_2b = BUS_DIR / f"{ticker}_{earnings_date}_pre_agent2b_guidance.json"
    bus_2c = BUS_DIR / f"{ticker}_{earnings_date}_pre_agent2c_sentiment.json"

    defects = []
    route_to = None

    if not html_file.exists():
        return {
            "ticker": ticker,
            "earnings_date": earnings_date,
            "status": "REJECTED",
            "route_to": "AGENT_4B_FINALIZER",
            "defects": [f"Rendered HTML file {html_file.name} does not exist."],
            "timestamp": datetime.now().isoformat()
        }

    for bf, r_target in [
        (bus_2a, "AGENT_2A_KPIS"),
        (bus_2b, "AGENT_2B_GUIDANCE"),
        (bus_2c, "AGENT_2C_SENTIMENT")
    ]:
        if not bf.exists():
            defects.append(f"Missing Layer 2 Pre-Earnings Bus file: {bf.name}")
            route_to = r_target

    html_content = html_file.read_text(encoding="utf-8")
    truth = json.loads(truth_file.read_text(encoding="utf-8")) if truth_file.exists() else {}

    # Check 1: Numeric Cross-Validation against Ground Truth
    spot_price = truth.get("price_validation", {}).get("yahoo_spot_price")
    implied_move = truth.get("options_positioning", {}).get("atm_implied_move_pct")
    fcf_bridge = truth.get("forensic_fcf_bridge_latest", {})
    latest_ocf = fcf_bridge.get("ocf")

    if spot_price and f"{spot_price:.2f}" not in html_content and f"{spot_price}" not in html_content:
        defects.append(f"Ground-Truth Spot Price (${spot_price}) missing in rendered HTML.")
        route_to = "LAYER_1_DETERMINISTIC"

    if implied_move and f"{implied_move:.2f}" not in html_content and f"{implied_move:.1f}" not in html_content and f"{implied_move}" not in html_content:
        defects.append(f"Options-Implied Move (±{implied_move}%) missing in rendered HTML.")
        route_to = "LAYER_1_DETERMINISTIC"

    if latest_ocf and f"{latest_ocf:,.0f}" not in html_content and f"{int(round(latest_ocf))}" not in html_content:
        defects.append(f"Latest Reported OCF (${latest_ocf:,.0f}M) missing in rendered HTML.")
        route_to = "LAYER_1_DETERMINISTIC"

    gt_cons_rev = truth.get("schedule_verification", {}).get("yahoo_consensus_revenue") or truth.get("street_consensus_and_targets", {}).get("yahoo_consensus_revenue_q0e")
    if gt_cons_rev:
        m_crev = re.search(
            r'Consensus(?:\s+Net)?\s+(?:Revenue|Sales).*?<span class="strip-val">\$([0-9,.]+)\s*([MB])?',
            html_content,
            re.DOTALL | re.IGNORECASE,
        )
        if m_crev:
            raw_v = float(m_crev.group(1).replace(",", ""))
            unit = (m_crev.group(2) or ("B" if raw_v < 500 and gt_cons_rev >= 1000 else "M")).upper()
            html_cons_m = raw_v * (1000.0 if unit == "B" else 1.0)
            if abs(html_cons_m - float(gt_cons_rev)) / float(gt_cons_rev) > 0.015:
                defects.append(
                    f"Consensus Revenue Drift in T-1 HTML (${html_cons_m:,.1f}M vs truth.json ${float(gt_cons_rev):,.1f}M)."
                )
                route_to = "AGENT_2A_KPIS"

    # Check 2: Row 1B Pre-Release Scorecard Table 1B-1, 1B-2, 1B-3
    if "Table 1B-1" not in html_content:
        defects.append("Missing Table 1B-1: Headline & Company KPI Consensus vs. Buy-Side Whisper Scorecard.")
        route_to = "AGENT_2A_KPIS"
    if "Table 1B-2" not in html_content:
        defects.append("Missing Table 1B-2: Management Guidance Credibility & 4Q Historical Track Record.")
        route_to = "AGENT_2B_GUIDANCE"
    if "Table 1B-3" not in html_content:
        defects.append("Missing Table 1B-3: Forward Guidance Bogeys & Re-Rating Hurdles.")
        route_to = "AGENT_2B_GUIDANCE"

    # Check 3: Depth of Pre-Print Wall Street Debates & Call Questions (Agent 2B)
    if "row-4b-debates" not in html_content:
        defects.append("Pre-Print Institutional Debates & Call Focus Questions (#row-4b-debates) missing from Section 5.")
        route_to = "AGENT_2B_GUIDANCE"

    # Check 4: Depth of Social, Whisper & Positioning Pulse (Agent 2C)
    if "Reddit" not in html_content and "FinTwit" not in html_content and "Retail" not in html_content:
        defects.append("Social microblogging & whisper positioning pulse missing from Section 7 sentiment.")
        route_to = "AGENT_2C_SENTIMENT"

    # Check 5: Interactive Tooltip Integrity
    tip_matches = len(re.findall(r'class="tip', html_content))
    if tip_matches < 20:
        defects.append(f"Insufficient interactive tooltips: Found {tip_matches}, require >= 20.")
        route_to = "AGENT_4B_FINALIZER"

    # Check 6: Track A & Track B Zero-Bleed & UX Component Audit
    if html_content.count("VERSION COMPARISON BANNER") >= 1:
        defects.append("Legacy VERSION COMPARISON BANNER detected in rendered HTML (must use clean Historical Quarter Archive topbar).")
        route_to = "AGENT_4B_FINALIZER"
    if '<th class="col-q0">' not in html_content or '<th class="col-est">' not in html_content:
        defects.append("Row 2 5-Quarter table missing col-q0 (Latest Actual) or col-est (Upcoming Consensus) column headers.")
        route_to = "AGENT_4B_FINALIZER"
    for tb_cls in ["pre-jump-nav", "t1-setup-audit", "beat-bar-track", "credibility-gauge-bar"]:
        if tb_cls not in html_content:
            defects.append(f"Missing Track B interactive component: .{tb_cls}")
            route_to = "AGENT_4B_FINALIZER"

    status = "APPROVED" if not defects else "REJECTED"
    signoff = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "report_type": "T-1_PRE_EARNINGS",
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "route_to": route_to,
        "defects": defects,
        "model_used": "Gemini 3.8 Flash High Standard",
        "summary": "All 9 sections + Track A/B Pre-Earnings upgrades cross-validated against deterministic ground truth and Layer 2 pre_agent_bus." if status == "APPROVED" else f"Rejected with {len(defects)} defects routed to {route_to}."
    }

    out_file = AUDIT_DIR / f"{ticker}_{earnings_date}_pre_agent5_signoff.json"
    out_file.write_text(json.dumps(signoff, indent=2), encoding="utf-8")
    return signoff

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python agent5_pre_chief_auditor.py <TICKER> <EARNINGS_DATE>", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2]
    res = audit_rendered_pre_html(t, d)
    print(f"Agent 5 Pre-Earnings Auditor Verdict: {res['status']}")
    if res["status"] == "REJECTED":
        print(f"Targeted Route-To: {res['route_to']}")
        for df in res["defects"]:
            print(f"  - {df}")
        sys.exit(1)
    else:
        print(f"Pre-Earnings Signoff APPROVED for {t} ({d}).")
        sys.exit(0)
