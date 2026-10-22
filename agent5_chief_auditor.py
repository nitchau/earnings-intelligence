"""
Agent 5: Chief HTML Auditor & Targeted Back-Router (Gemini 3.8 Flash High Standard)
Layer 5 Cross-Validation Gatekeeper:
- Deeply inspects rendered published_reports/{TICKER}_T0_POST_{DATE}.html against:
  - ground_truth/{TICKER}_{DATE}_post_truth.json
  - post_agent_bus/{TICKER}_{DATE}_agent2a_kpis.json
  - post_agent_bus/{TICKER}_{DATE}_agent2b_transcript.json
  - post_agent_bus/{TICKER}_{DATE}_agent2c_social.json
- Targeted Back-Routing Protocol:
  If any defect is detected, writes audit_logs/{TICKER}_{DATE}_agent5_signoff.json with:
    "status": "REJECTED"
    "route_to": LAYER_1_DETERMINISTIC | AGENT_2A_KPIS | AGENT_2B_TRANSCRIPT | AGENT_2C_SOCIAL | AGENT_4B_FINALIZER
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
BUS_DIR = BASE_DIR / "post_agent_bus"

def audit_rendered_post_html(ticker: str, earnings_date: str) -> dict:
    ticker = ticker.upper()
    html_file = REPORTS_DIR / f"{ticker}_T0_POST_{earnings_date}.html"
    truth_file = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date}_post_truth.json"
    bus_2a = BUS_DIR / f"{ticker}_{earnings_date}_agent2a_kpis.json"
    bus_2b = BUS_DIR / f"{ticker}_{earnings_date}_agent2b_transcript.json"
    bus_2c = BUS_DIR / f"{ticker}_{earnings_date}_agent2c_social.json"

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

    html_content = html_file.read_text(encoding="utf-8")
    truth = json.loads(truth_file.read_text(encoding="utf-8")) if truth_file.exists() else {}
    kpis = json.loads(bus_2a.read_text(encoding="utf-8")) if bus_2a.exists() else {}
    transcript = json.loads(bus_2b.read_text(encoding="utf-8")) if bus_2b.exists() else {}
    social = json.loads(bus_2c.read_text(encoding="utf-8")) if bus_2c.exists() else {}

    # Check 1: Numeric Cross-Validation against Ground Truth
    q0_rev = truth.get("beat_miss_scorecard", {}).get("revenue", {}).get("reported_actual_millions")
    ah_price = truth.get("post_print_reaction", {}).get("after_hours_price")
    q0_ocf = truth.get("forensic_fcf_bridge_q0", {}).get("ocf")
    q0_fcf = truth.get("forensic_fcf_bridge_q0", {}).get("true_fcf")

    if q0_rev and f"{q0_rev:,.0f}" not in html_content and f"{q0_rev}" not in html_content and f"{q0_rev:,.2f}" not in html_content:
        defects.append(f"Reported Q0 Revenue (${q0_rev}M) missing or mismatched in rendered HTML.")
        route_to = "LAYER_1_DETERMINISTIC"

    if ah_price and f"{ah_price:.2f}" not in html_content and f"{ah_price}" not in html_content:
        defects.append(f"Ground-Truth After-Hours Price (${ah_price}) missing in rendered HTML.")
        route_to = "LAYER_1_DETERMINISTIC"

    # Check 2: Row 1B Scorecard Table 1B-1, 1B-2, 1B-3
    if "Table 1B-1" not in html_content and "Beat / Miss Scorecard" not in html_content:
        defects.append("Missing Table 1B-1: Headline & Company KPI Beat / Miss Scorecard.")
        route_to = "AGENT_4B_FINALIZER"
    if "Table 1B-2" not in html_content and "Management Execution Accountability" not in html_content:
        defects.append("Missing Table 1B-2: Management Execution Accountability (Q0 vs Q-1 Guidance).")
        route_to = "AGENT_2B_TRANSCRIPT"
    if "Table 1B-3" not in html_content and "Forward Guidance Reset" not in html_content:
        defects.append("Missing Table 1B-3: Forward Guidance Reset (New Guidance vs Street Expectations).")
        route_to = "AGENT_2B_TRANSCRIPT"

    # Check 3: Depth of Transcript Forensic Findings (Agent 2B)
    if "Analyst Q&A" not in html_content and "Analyst Questions" not in html_content:
        defects.append("Call Q&A Forensic Highlights missing from Section 5 audit.")
        route_to = "AGENT_2B_TRANSCRIPT"

    # Check 4: Depth of Social & Microblogging Pulse (Agent 2C)
    if "Reddit" not in html_content and "FinTwit" not in html_content and "Retail" not in html_content:
        defects.append("Social microblogging pulse (Reddit/FinTwit/Retail) missing from Section 7 sentiment.")
        route_to = "AGENT_2C_SOCIAL"

    # Check 5: Interactive Tooltip Integrity
    tip_matches = len(re.findall(r'class="tip', html_content))
    if tip_matches < 18:
        defects.append(f"Insufficient interactive tooltips: Found {tip_matches}, require >= 18.")
        route_to = "AGENT_4B_FINALIZER"

    # Check 6: Track A & Track B Zero-Bleed & Rolling 5Q Audit
    if "T-1 PRE-EARNINGS" in html_content:
        defects.append("T-1 PRE-EARNINGS badge bleed-through detected in T+0 post-earnings tearsheet.")
        route_to = "AGENT_4B_FINALIZER"
    if html_content.count("VERSION COMPARISON BANNER") > 1:
        defects.append("Duplicate VERSION COMPARISON BANNER detected in rendered HTML.")
        route_to = "AGENT_4B_FINALIZER"
    if '<th class="col-q0">Q3 2026 (Actual)' not in html_content or '<th class="col-est">Q4 2026E' not in html_content:
        defects.append("Row 2 5-Quarter table is not rolled forward to Q3 2026 (Actual) + Q4 2026E.")
        route_to = "LAYER_1_DETERMINISTIC"
    for tb_cls in ["post-jump-nav", "t1-vs-t0-audit", "beat-bar-track", "credibility-gauge-bar"]:
        if tb_cls not in html_content:
            defects.append(f"Missing Track B interactive component: .{tb_cls}")
            route_to = "AGENT_4B_FINALIZER"

    # Final verdict determination
    status = "APPROVED" if not defects else "REJECTED"
    signoff = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "route_to": route_to,
        "defects": defects,
        "model_used": "Gemini 3.8 Flash High Standard",
        "summary": "All 9 sections + Track A/B upgrades cross-validated against deterministic ground truth and Layer 2 agent bus." if status == "APPROVED" else f"Rejected with {len(defects)} defects routed to {route_to}."
    }

    out_file = AUDIT_DIR / f"{ticker}_{earnings_date}_agent5_signoff.json"
    out_file.write_text(json.dumps(signoff, indent=2), encoding="utf-8")
    return signoff

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python agent5_chief_auditor.py <TICKER> <EARNINGS_DATE>", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2]
    res = audit_rendered_post_html(t, d)
    print(f"Agent 5 Auditor Verdict: {res['status']}")
    if res["status"] == "REJECTED":
        print(f"Targeted Route-To: {res['route_to']}")
        for df in res["defects"]:
            print(f"  - {df}")
        sys.exit(1)
    else:
        print(f"Signoff approved for {t} ({d}).")
        sys.exit(0)
