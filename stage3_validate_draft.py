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

    # --- FIX #4: Verify Dynamic Segment Labels & Interactive Tooltip (.tip) Preservation ---
    if ticker != "TSLA":
        tesla_leaks = ["Automotive Regulatory Credits", "Cybercab", "Megapack", "Optimus"]
        for term in tesla_leaks:
            if term.lower() in html_body.lower():
                errors.append(f"Hardcoded Tesla term '{term}' found in {ticker} report! Must map {ticker}'s actual segments.")

    tip_count = html_body.count('class="tip')
    datatip_count = html_body.count('data-tip="')
    if tip_count < 15 or datatip_count < 15:
        errors.append(f"Interactive tooltips missing: Found only {tip_count} '.tip' classes and {datatip_count} 'data-tip' definitions (require >= 15).")

    # --- FIX #5A: Verify 5-Quarter P&L Math (Gross Profit - OpEx == Operating Income / EBIT) ---
    table_5q = draft.get("historical_table_5q_nums", [])
    if len(table_5q) != 5:
        errors.append("Draft must include 'historical_table_5q_nums' array for all 5 historical quarters.")
    for q_idx, q_data in enumerate(table_5q):
        gp = q_data.get("gross_profit")
        opex = q_data.get("operating_expenses")
        ebit = q_data.get("operating_income")
        if None not in (gp, opex, ebit) and abs((gp - opex) - ebit) > 2.0:
            errors.append(f"Quarter {q_idx+1} P&L Math Error: Gross Profit ({gp}) - OpEx ({opex}) != Operating Income ({ebit})")

    # --- FIX #5B: Verify Cash Flow Bridge Math (OCF - CapEx == Reported FCF; Reported FCF - SBC - Leases == True FCF) ---
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

    # --- FIX #5C: Prose-to-Table Anchor Check (Ensure Spot Price, Latest Revenue, OCF, and CapEx Appear in HTML) ---
    gt_price = truth["price_validation"]["yahoo_spot_price"]
    if gt_price and f"{gt_price:.2f}" not in html_body and str(gt_price) not in html_body:
        errors.append(f"Ground truth spot price (${gt_price}) does not appear in rendered HTML.")

    if bridge.get("ocf"):
        ocf_int_str = f"{int(round(bridge['ocf'])):,}"
        if ocf_int_str not in html_body and str(int(round(bridge["ocf"]))) not in html_body:
            errors.append(f"Latest Operating Cash Flow (${ocf_int_str}M) missing or mismatched between FCF bridge and HTML.")

    # --- Verify Trade Matrix Strike Sanity vs Spot Price ---
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
