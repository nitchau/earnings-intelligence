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
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent.resolve()
BUS_DIR = BASE_DIR / "post_agent_bus"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
DRAFTS_DIR = BASE_DIR / "drafts"
AUDIT_DIR = BASE_DIR / "audit_logs"


def _parse_html_num(cell_text: str, target_scale_millions: bool = True) -> float | None:
    """Parse a financial table cell such as '$127,577.0M', '-$9,065.0M', '($8,221M)', '$30.71B', '$2.12'."""
    if not cell_text:
        return None
    s = cell_text.strip()
    if s in ("—", "-", "N/A", "NM", ""):
        return None
    # Detect parenthetical negative e.g. ($9,065.0M) or (€253M)
    is_paren_neg = bool(re.match(r"^\(\s*[$€]?\s*[\d,.]+", s))
    m = re.search(r"([+\-])?\s*[$€]?\s*([+\-])?\s*(\d[\d,]*(?:\.\d+)?)\s*([BMK%])?(?![A-Za-z])", s)
    if not m:
        return None
    if m.group(4) == "%":
        return None
    sign = -1.0 if (is_paren_neg or m.group(1) == "-" or m.group(2) == "-") else 1.0
    val = float(m.group(3).replace(",", "")) * sign
    unit = m.group(4) or ""
    if target_scale_millions:
        if unit == "B":
            val *= 1000.0
        elif unit == "K":
            val /= 1000.0
    return val


def _close_num(actual: float | None, expected: float | None, rel_tol: float = 0.015, abs_tol: float = 3.0) -> bool:
    if actual is None or expected is None:
        return True
    diff = abs(actual - expected)
    if diff <= abs_tol:
        return True
    denom = max(abs(expected), 1e-6)
    return (diff / denom) <= rel_tol


def _canonical_seg_key(label: str) -> str | None:
    l = re.sub(r"^[\s↳•\-]+", "", label.lower())
    if "google cloud" in l and "margin" not in l and "operating income" not in l and "backlog" not in l:
        return "google_cloud"
    if "google search" in l and "margin" not in l:
        return "google_search"
    if "youtube" in l and ("ad" in l or "revenue" in l):
        return "youtube_ads"
    if "subscription revenue" in l and "margin" not in l and "growth" not in l:
        return "subscription_revenue"
    if "product revenue" in l and "margin" not in l and "growth" not in l:
        return "product_revenue"
    if ("service revenue" in l or "services revenue" in l) and "margin" not in l and "google" not in l:
        return "service_revenue"
    if "americas" in l and "margin" not in l and "growth" not in l:
        return "americas_sales"
    if ("apac" in l or "asia pacific" in l) and "margin" not in l and "growth" not in l:
        return "apac_sales"
    if "emea" in l and "margin" not in l and "growth" not in l:
        return "emea_sales"
    return None


def audit_rendered_tables_against_truth(html_body: str, truth: dict) -> list[str]:
    """
    Deep HTML <table> cell parity audit across:
    - Dynamic fiscal period headers (period_labels[-1] & next_quarter_estimate_label)
    - Table 1B-1 (#sec-scorecard): Headline Revenue, EPS, Q-1, Q-4, Consensus, and Q0 Actual cells
    - Row 2 (#sec-5q): All 5 quarters of Revenue + Q0 Gross Profit, OpEx, R&D/S&M/G&A sub-rows, EBIT, GAAP/Non-GAAP EPS
    - Cross-table consistency between Table 1B-1 and #sec-5q for shared KPIs/segments
    - Row 3 (#sec-fcf): Q0 OCF, CapEx, Reported FCF, SBC, and True FCF grounding
    """
    errs = []
    soup = BeautifulSoup(html_body, "html.parser")
    s5q = truth.get("stitched_5q_chronological", {})
    scorecard = truth.get("beat_miss_scorecard", {})
    rev_sc = scorecard.get("revenue", {})
    eps_ng_sc = scorecard.get("eps_nongaap", {})
    eps_g_sc = scorecard.get("eps_gaap", {})
    fcf_q0 = truth.get("forensic_fcf_bridge_q0", {})
    facts = truth.get("company_specific_facts", {})

    q0_rev = rev_sc.get("reported_actual_millions")
    cons_rev = rev_sc.get("street_consensus_millions")
    q0_eps_ng = eps_ng_sc.get("reported_actual")
    cons_eps_ng = eps_ng_sc.get("street_consensus")
    q0_eps_g = eps_g_sc.get("reported_actual")
    cons_eps_g = eps_g_sc.get("street_consensus")

    # 1. Dynamic Fiscal Period Header Verification
    period_labels = s5q.get("period_labels") or []
    expected_q0_hdr = period_labels[-1] if period_labels else "Q3 2026 (Actual)"
    next_est_raw = s5q.get("next_quarter_estimate_label") or "Q4 2026E"
    expected_est_prefix = next_est_raw.split("(")[0].strip()
    stale_q0e_prefix = expected_q0_hdr.split("(")[0].strip() + "E"

    sec_5q = soup.find(id="sec-5q")
    if sec_5q:
        ths_q0 = [th.get_text(" ", strip=True) for th in sec_5q.find_all("th", class_="col-q0")]
        ths_est = [th.get_text(" ", strip=True) for th in sec_5q.find_all("th", class_="col-est")]
        if not any(expected_q0_hdr in t for t in ths_q0):
            errs.append(f"Row 2 5-Quarter Table Error: <th class='col-q0'> must contain '{expected_q0_hdr}' (found {ths_q0}).")
        if not any(expected_est_prefix in t for t in ths_est):
            errs.append(f"Row 2 5-Quarter Table Error: <th class='col-est'> must start with '{expected_est_prefix}' (found {ths_est}).")
        if any(stale_q0e_prefix in t for t in ths_est):
            errs.append(f"Stale T-1 Table Header Found: '<th class=\"col-est\">{stale_q0e_prefix}' is still present in Row 2.")
    else:
        errs.append("Missing id='sec-5q' on Row 2 5-Quarter Financials section.")

    # 2. Parse Row 2 (#sec-5q) Table Cells
    sec_5q_segments: dict[str, dict[str, float | None]] = {}
    if sec_5q:
        tbl_5q = sec_5q.find("table")
        if tbl_5q:
            for tr in tbl_5q.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 6:
                    continue
                lbl = tds[0].get_text(" ", strip=True)
                ll = lbl.lower()
                is_sub = "sub-row" in (tr.get("class") or []) or lbl.strip().startswith("↳")

                seg_k = _canonical_seg_key(lbl)
                if seg_k:
                    sec_5q_segments[seg_k] = {
                        "q_minus_4": _parse_html_num(tds[1].get_text(" ", strip=True)),
                        "q_minus_1": _parse_html_num(tds[4].get_text(" ", strip=True)),
                        "q0": _parse_html_num(tds[5].get_text(" ", strip=True)),
                    }

                # Headline Total Revenue row in 5Q table
                if not is_sub and any(k in ll for k in ("total revenue", "total consolidated revenue", "total net revenue", "consolidated net sales", "net sales", "revenues ($m)", "revenue ($m)")) and not any(x in ll for x in ("cost", "margin", "growth", "yoy", "qoq", "per share")):
                    rev_arr = s5q.get("total_revenue") or []
                    if len(rev_arr) == 5:
                        for idx in range(5):
                            c_val = _parse_html_num(tds[idx + 1].get_text(" ", strip=True))
                            if rev_arr[idx] is not None and c_val is not None and not _close_num(c_val, rev_arr[idx], rel_tol=0.012, abs_tol=2.0):
                                errs.append(f"Row 2 (#sec-5q) Revenue Mismatch at col {idx+1} ({period_labels[idx] if idx < len(period_labels) else idx}): HTML has {c_val}M vs Ground Truth {rev_arr[idx]}M.")

                # Gross Profit row
                elif not is_sub and "gross profit" in ll and "margin" not in ll and "yoy" not in ll:
                    gp_q0 = (s5q.get("gross_profit") or [None]*5)[-1]
                    c_val = _parse_html_num(tds[5].get_text(" ", strip=True))
                    if gp_q0 is not None and c_val is not None and not _close_num(c_val, gp_q0, rel_tol=0.015, abs_tol=5.0):
                        errs.append(f"Row 2 (#sec-5q) Q0 Gross Profit Mismatch: HTML has {c_val}M vs Ground Truth {gp_q0}M.")

                # Total Operating Expenses row
                elif not is_sub and ("operating expense" in ll or "total opex" in ll) and "margin" not in ll and "%" not in ll:
                    opex_q0 = (s5q.get("operating_expenses") or [None]*5)[-1]
                    c_val = _parse_html_num(tds[5].get_text(" ", strip=True))
                    if opex_q0 is not None and c_val is not None and not _close_num(c_val, opex_q0, rel_tol=0.015, abs_tol=5.0):
                        errs.append(f"Row 2 (#sec-5q) Q0 Operating Expenses Mismatch: HTML has {c_val}M vs Ground Truth {opex_q0}M.")

                # OpEx Component Sub-Rows (R&D, S&M, G&A) against Exhibit 99.1 facts
                elif ("research & development" in ll or "research and development" in ll or re.search(r"\br&d\b", ll)) and "%" not in ll:
                    if facts.get("rd_q0") is not None:
                        c_val = _parse_html_num(tds[5].get_text(" ", strip=True))
                        if c_val is not None and not _close_num(c_val, facts["rd_q0"], rel_tol=0.015, abs_tol=3.0):
                            errs.append(f"Row 2 (#sec-5q) Q0 R&D Mismatch: HTML has {c_val}M vs SEC Exhibit 99.1 {facts['rd_q0']}M.")
                elif ("sales & marketing" in ll or "sales and marketing" in ll) and "%" not in ll:
                    if facts.get("sm_q0") is not None:
                        c_val = _parse_html_num(tds[5].get_text(" ", strip=True))
                        if c_val is not None and not _close_num(c_val, facts["sm_q0"], rel_tol=0.015, abs_tol=3.0):
                            errs.append(f"Row 2 (#sec-5q) Q0 Sales & Marketing Mismatch: HTML has {c_val}M vs SEC Exhibit 99.1 {facts['sm_q0']}M.")
                elif ("general & administrative" in ll or "general and administrative" in ll) and "%" not in ll:
                    if facts.get("ga_q0") is not None:
                        c_val = _parse_html_num(tds[5].get_text(" ", strip=True))
                        if c_val is not None and not _close_num(c_val, facts["ga_q0"], rel_tol=0.015, abs_tol=3.0):
                            errs.append(f"Row 2 (#sec-5q) Q0 G&A Mismatch: HTML has {c_val}M vs SEC Exhibit 99.1 {facts['ga_q0']}M.")

                # GAAP Operating Income / EBIT row
                elif not is_sub and any(k in ll for k in ("operating income", "operating profit", "income from operations")) and not any(x in ll for x in ("non-gaap", "adjusted", "adj.", "margin", "%")):
                    ebit_q0 = (s5q.get("operating_income") or [None]*5)[-1]
                    c_val = _parse_html_num(tds[5].get_text(" ", strip=True))
                    if ebit_q0 is not None and c_val is not None and not _close_num(c_val, ebit_q0, rel_tol=0.015, abs_tol=5.0):
                        errs.append(f"Row 2 (#sec-5q) Q0 Operating Income Mismatch: HTML has {c_val}M vs Ground Truth {ebit_q0}M.")

                # EPS rows in #sec-5q
                elif "eps" in ll or "earnings per share" in ll or "loss per share" in ll:
                    c_val = _parse_html_num(tds[5].get_text(" ", strip=True), target_scale_millions=False)
                    if any(x in ll for x in ("non-gaap", "adjusted", "adj.")):
                        if q0_eps_ng is not None and c_val is not None and abs(c_val - q0_eps_ng) > 0.02:
                            errs.append(f"Row 2 (#sec-5q) Q0 Non-GAAP EPS Mismatch: HTML has ${c_val:.2f} vs Ground Truth ${q0_eps_ng:.2f}.")
                    else:
                        if q0_eps_g is not None and c_val is not None and abs(c_val - q0_eps_g) > 0.02:
                            errs.append(f"Row 2 (#sec-5q) Q0 GAAP Diluted EPS Mismatch: HTML has ${c_val:.2f} vs Ground Truth ${q0_eps_g:.2f}.")

    # 3. Parse Table 1B-1 (#sec-scorecard first table)
    sec_sc = soup.find(id="sec-scorecard")
    if sec_sc:
        tbl_1b1 = sec_sc.find("table")
        if tbl_1b1:
            for tr in tbl_1b1.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 5:
                    continue
                lbl = tds[0].get_text(" ", strip=True)
                ll = lbl.lower()

                # Total Consolidated Revenue / Net Sales row in Table 1B-1
                is_total_rev_row = (
                    any(k in ll for k in ("total consolidated revenue", "total net revenue", "total revenue", "consolidated net sales", "net sales ($m)", "net sales / revenue"))
                    and not any(x in ll for x in ("subscription", "cloud", "product", "service", "margin", "growth", "americas", "amer", "apac", "asia", "emea", "europe", "north america", "international", "regional", "segment"))
                )
                if is_total_rev_row:
                    c_qm1 = _parse_html_num(tds[1].get_text(" ", strip=True))
                    c_qm4 = _parse_html_num(tds[2].get_text(" ", strip=True))
                    c_cons = _parse_html_num(tds[3].get_text(" ", strip=True))
                    c_q0 = _parse_html_num(tds[4].get_text(" ", strip=True))
                    rev_arr = s5q.get("total_revenue") or []
                    if q0_rev is not None and c_q0 is not None and not _close_num(c_q0, q0_rev, rel_tol=0.01, abs_tol=2.0):
                        errs.append(f"Table 1B-1 Total Revenue Q0 Actual ({c_q0}M) contradicts Ground Truth Q0 Revenue ({q0_rev}M)!")
                    if cons_rev is not None and c_cons is not None and not _close_num(c_cons, cons_rev, rel_tol=0.01, abs_tol=2.0):
                        errs.append(f"Table 1B-1 Street Consensus Revenue ({c_cons}M) contradicts Ground Truth Consensus ({cons_rev}M)!")
                    if len(rev_arr) == 5:
                        if rev_arr[3] is not None and c_qm1 is not None and not _close_num(c_qm1, rev_arr[3], rel_tol=0.015, abs_tol=3.0):
                            errs.append(f"Table 1B-1 Q-1 Revenue ({c_qm1}M) contradicts 5Q Historical Q-1 Revenue ({rev_arr[3]}M)!")
                        if rev_arr[0] is not None and c_qm4 is not None and not _close_num(c_qm4, rev_arr[0], rel_tol=0.015, abs_tol=3.0):
                            errs.append(f"Table 1B-1 Q-4 Revenue ({c_qm4}M) contradicts 5Q Historical Q-4 Revenue ({rev_arr[0]}M)!")

                # EPS row in Table 1B-1
                if "eps" in ll or "earnings per share" in ll:
                    c_cons_eps = _parse_html_num(tds[3].get_text(" ", strip=True), target_scale_millions=False)
                    c_q0_eps = _parse_html_num(tds[4].get_text(" ", strip=True), target_scale_millions=False)
                    if any(x in ll for x in ("non-gaap", "adjusted", "adj.")) or (q0_eps_ng is not None and "gaap" not in ll):
                        if q0_eps_ng is not None and c_q0_eps is not None and abs(c_q0_eps - q0_eps_ng) > 0.02:
                            errs.append(f"Table 1B-1 Reported Non-GAAP EPS (${c_q0_eps:.2f}) contradicts Ground Truth (${q0_eps_ng:.2f})!")
                        if cons_eps_ng is not None and c_cons_eps is not None and abs(c_cons_eps - cons_eps_ng) > 0.02:
                            errs.append(f"Table 1B-1 Consensus EPS (${c_cons_eps:.2f}) contradicts Ground Truth (${cons_eps_ng:.2f})!")
                    else:
                        if q0_eps_g is not None and c_q0_eps is not None and abs(c_q0_eps - q0_eps_g) > 0.02:
                            errs.append(f"Table 1B-1 Reported GAAP EPS (${c_q0_eps:.2f}) contradicts Ground Truth (${q0_eps_g:.2f})!")
                        if cons_eps_g is not None and c_cons_eps is not None and abs(c_cons_eps - cons_eps_g) > 0.02:
                            errs.append(f"Table 1B-1 Consensus GAAP EPS (${c_cons_eps:.2f}) contradicts Ground Truth (${cons_eps_g:.2f})!")

                # Cross-table segment consistency (Table 1B-1 vs Row 2 #sec-5q)
                seg_k = _canonical_seg_key(lbl)
                if seg_k and seg_k in sec_5q_segments:
                    s5 = sec_5q_segments[seg_k]
                    c_qm1 = _parse_html_num(tds[1].get_text(" ", strip=True))
                    c_qm4 = _parse_html_num(tds[2].get_text(" ", strip=True))
                    c_q0 = _parse_html_num(tds[4].get_text(" ", strip=True))
                    if not _close_num(c_q0, s5["q0"], rel_tol=0.015, abs_tol=5.0):
                        errs.append(f"Cross-Table Segment Mismatch ({lbl} Q0): Table 1B-1 has {c_q0}M vs Row 2 (#sec-5q) {s5['q0']}M!")
                    if not _close_num(c_qm1, s5["q_minus_1"], rel_tol=0.015, abs_tol=5.0):
                        errs.append(f"Cross-Table Segment Mismatch ({lbl} Q-1): Table 1B-1 has {c_qm1}M vs Row 2 (#sec-5q) {s5['q_minus_1']}M!")
                    if not _close_num(c_qm4, s5["q_minus_4"], rel_tol=0.015, abs_tol=5.0):
                        errs.append(f"Cross-Table Segment Mismatch ({lbl} Q-4): Table 1B-1 has {c_qm4}M vs Row 2 (#sec-5q) {s5['q_minus_4']}M!")

    # 4. Row 3 (#sec-fcf) Ground-Truth Cash Flow Waterfall Parity
    sec_fcf = soup.find(id="sec-fcf")
    if sec_fcf:
        fcf_text = sec_fcf.get_text(" ", strip=True)
        for m_name, m_val in [("OCF", fcf_q0.get("ocf")), ("CapEx", fcf_q0.get("capex")), ("True FCF", fcf_q0.get("true_fcf"))]:
            if m_val is not None:
                av = abs(float(m_val))
                candidates = [f"{av:,.0f}", f"{av:,.1f}", f"{av:,.2f}", f"{av}"]
                if av >= 10000:
                    candidates.extend([f"{av/1000:,.2f}B", f"{av/1000:,.1f}B"])
                if not any(tok in fcf_text for tok in candidates):
                    errs.append(f"Row 3 (#sec-fcf) Cash Flow Bridge Mismatch: Ground-Truth Q0 {m_name} ({m_val}M) missing from #sec-fcf section!")

    return errs

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

    # Guardrail 11: Dynamic Rolling 5Q Table, Deep HTML Cell Parity & Track B Enhancements Verification
    for tb_class in ["post-jump-nav", "t1-vs-t0-audit", "beat-bar-track", "credibility-gauge-bar"]:
        if tb_class not in html_body:
            errors.append(f"Missing Track B Product Enhancement Component: '{tb_class}' missing from rendered HTML.")

    table_parity_errors = audit_rendered_tables_against_truth(html_body, truth)
    errors.extend(table_parity_errors)

    # Guardrail 12: Table 1B-1 Column Semantics & Anti-Leak Check
    # Ensure Q-1 Actual and Q-4 YoY columns do not carry identical revenue numbers or prior-year leaks
    s5q_rev = truth.get("stitched_5q_chronological", {}).get("total_revenue", [])
    if len(s5q_rev) == 5:
        q_minus_1_rev = s5q_rev[3]
        q_minus_4_rev = s5q_rev[0]
        # In Table 1B-1, Q-1 Actual and Q-4 YoY must be distinct for growing companies
        if q_minus_1_rev and q_minus_4_rev and abs(q_minus_1_rev - q_minus_4_rev) > 10.0:
            bad_dup_cell = f"${q_minus_4_rev:,.1f}M</td>\n                <td>${q_minus_4_rev:,.1f}M"
            if bad_dup_cell in html_body:
                errors.append(f"Table 1B-1 Semantic Error: Q-1 Actual and Q-4 YoY both contain identical prior-year revenue (${q_minus_4_rev:,.1f}M)!")

    # Guardrail 13: Segment Sum Cross-Footing Integrity Check
    # Revenue segment components in #sec-5q (and revenue-only rows in Table 1B-1) must not exceed Total Revenue
    # and #sec-5q revenue sub-rows must cross-foot to Total Revenue (excluding non-revenue KPIs like Billings/RPO/Backlog).
    if q0_rev and q0_rev > 0:
        soup_g13 = BeautifulSoup(html_body, "html.parser")
        sec_5q_g13 = soup_g13.find(id="sec-5q")
        if sec_5q_g13:
            tbl_5q_g13 = sec_5q_g13.find("table")
            if tbl_5q_g13:
                rev_seg_vals = []
                in_rev_block = False
                for tr in tbl_5q_g13.find_all("tr"):
                    tds = tr.find_all("td")
                    if len(tds) < 6:
                        continue
                    lbl_l = tds[0].get_text(" ", strip=True).lower()
                    is_sub = "sub-row" in (tr.get("class") or []) or tds[0].get_text(strip=True).startswith("↳")
                    if not is_sub and ("revenue" in lbl_l or "net sales" in lbl_l) and "cost" not in lbl_l:
                        in_rev_block = True
                        continue
                    if not is_sub and in_rev_block:
                        break
                    if is_sub and in_rev_block and "%" not in lbl_l:
                        v = _parse_html_num(tds[5].get_text(" ", strip=True))
                        if v is not None:
                            rev_seg_vals.append(v)
                if rev_seg_vals:
                    if max(rev_seg_vals) > q0_rev * 1.05:
                        errors.append(f"Segment Math Error: Individual revenue segment (${max(rev_seg_vals):,.1f}M) exceeds Total Reported Revenue (${q0_rev:,.1f}M)!")
                    if len(rev_seg_vals) >= 2 and abs(sum(rev_seg_vals) - q0_rev) > max(q0_rev * 0.03, 5.0):
                        errors.append(f"Segment Cross-Footing Error: Row 2 (#sec-5q) revenue segments sum to ${sum(rev_seg_vals):,.1f}M vs Total Revenue ${q0_rev:,.1f}M!")

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
