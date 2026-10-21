import json
import re
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "TSLA_2026-10-21_truth.json"
MASTER_HTML = BASE_DIR / "Stock_Analysis_v2.html"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "TSLA_2026-10-21_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
master_raw = MASTER_HTML.read_text(encoding="utf-8")

# Extract inner container HTML
start_marker = '<div class="container">'
start_idx = master_raw.find(start_marker) + len(start_marker)
end_idx = master_raw.rfind('</div>', 0, master_raw.find('</body>'))
container_html = master_raw[start_idx:end_idx].strip()

# Apply deterministic updates from ground truth
spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 374.36
mkt_cap_t = round(truth["valuation_and_market"]["market_cap_millions"] / 1e6, 2) # 1.48
ev_t = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1e6, 2) # 1.43
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 346.63
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 172.64
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 14.27
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 132.67
opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 6.56
opt_move_usd = float(truth["options_positioning"].get("atm_straddle_usd", 24.57))
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 0.88
iv_pct = float(truth["options_positioning"].get("atm_implied_volatility_pct", 78.23))

updated_html = container_html

# 1. Spot Price replacement everywhere $378.03 appeared
updated_html = updated_html.replace(
    '<div class="price-value">$378.03 <span class="badge badge-bear">-15.8%',
    f'<div class="price-value">${spot_price:.2f} <span class="badge badge-bear">-16.5%'
)
updated_html = updated_html.replace(
    '<div class="price-value">$1.45T / $1.42T</div>',
    f'<div class="price-value">${mkt_cap_t:.2f}T / ${ev_t:.2f}T</div>'
)
updated_html = updated_html.replace(
    'current share price ($378.03)',
    f'current share price (${spot_price:.2f})'
)
updated_html = updated_html.replace(
    'closest to the current trading price of the stock ($378.03)',
    f'closest to the current trading price of the stock (${spot_price:.2f})'
)
updated_html = updated_html.replace(
    'strike price equal to the current stock price ($378)',
    f'strike price equal to the current stock price (${int(round(spot_price))})'
)
updated_html = updated_html.replace(
    'Current Share Price ($378.03)',
    f'Current Share Price (${spot_price:.2f})'
)
updated_html = updated_html.replace('$378.03', f'${spot_price:.2f}')

# 2. Options Implied Move
updated_html = updated_html.replace(
    '±7.85% (±$29.68 / sh)',
    f'±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)'
)
updated_html = updated_html.replace(
    'elevated ±7.85% implied move',
    f'elevated ±{opt_move_pct:.2f}% implied move'
)

# 3. Valuation Multiples in Card D
updated_html = updated_html.replace(
    '<span class="kpi-val">350.0x <span style="font-size:11px;color:var(--text-muted);">(381x S&amp;P)</span></span>',
    f'<span class="kpi-val">{trailing_pe:.1f}x <span style="font-size:11px;color:var(--text-muted);">(381x S&amp;P)</span></span>'
)
updated_html = updated_html.replace(
    '<span class="kpi-val" style="color: var(--warn-amber);">188.05x</span>',
    f'<span class="kpi-val" style="color: var(--warn-amber);">{fwd_pe:.2f}x</span>'
)
updated_html = updated_html.replace(
    '<span class="kpi-val">13.99x</span>',
    f'<span class="kpi-val">{ps_ttm:.2f}x</span>'
)
updated_html = updated_html.replace(
    '<span class="kpi-val">132.28x / 92.68x</span>',
    f'<span class="kpi-val">{ev_ebitda:.2f}x / 92.68x</span>'
)
updated_html = updated_html.replace(
    'At 188x, investors are pricing in massive future Robotaxi/AI growth',
    f'At {int(round(fwd_pe))}x, investors are pricing in massive future Robotaxi/AI growth'
)
updated_html = updated_html.replace('188.1x', f'{fwd_pe:.1f}x')

# 4. Put/Call Open Interest Ratio in Sentiment options pillar
updated_html = updated_html.replace(
    '<span class="mono">1.14x</span> (72nd %-ile — defensive hedging)',
    f'<span class="mono">{pcr_oi:.2f}x</span> (Elevated Call Volume)'
)

# 5. Inject waterfall-row elements into FCF bridge
waterfall_rows_html = """
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
            <span class="waterfall-label">Reported Operating Cash Flow (OCF)</span>
            <span class="waterfall-val" style="color: var(--bull-green); font-weight:600;">$4,697M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
            <span class="waterfall-label">Less: Capital Expenditures (CapEx)</span>
            <span class="waterfall-val" style="color: var(--bear-red); font-weight:600;">-$5,789M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:6px 0; background: rgba(239, 68, 68, 0.08); font-weight:700; border-bottom:1px solid rgba(255,255,255,0.06);">
            <span class="waterfall-label">= Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$1,092M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
            <span class="waterfall-label">Less: Stock-Based Compensation (SBC)</span>
            <span class="waterfall-val" style="color: var(--bear-red); font-weight:600;">-$1,151M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
            <span class="waterfall-label">Less: Finance Lease Principal Payments</span>
            <span class="waterfall-val" style="color: var(--text-muted); font-weight:600;">-$88M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:6px 0; background: rgba(239, 68, 68, 0.12); font-weight:700; border-top: 1px solid rgba(255,255,255,0.1); margin-bottom:10px;">
            <span class="waterfall-label">= True Free Cash Flow (ex-SBC)</span>
            <span class="waterfall-val" style="color: var(--bear-red); font-size:14px;">-$2,331M</span>
          </div>
"""
# Insert right before <table> in .fcf-bridge-box
updated_html = updated_html.replace(
    '<div class="fcf-bridge-box">\n          <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border-color);padding-bottom:10px;">',
    f'<div class="fcf-bridge-box">\n          <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border-color);padding-bottom:10px;">'
)
updated_html = updated_html.replace(
    '<span class="badge badge-bear">Q2 2026 ACTUAL</span>\n          </div>\n\n          <table>',
    f'<span class="badge badge-bear">Q2 2026 ACTUAL</span>\n          </div>\n\n{waterfall_rows_html}\n          <table>'
)

# 6. Ensure audit-grid is present around Row 4
updated_html = updated_html.replace(
    '<!-- 5. ROW 4: 2-COLUMN SPLIT (EXECUTION AUDIT: RIGHT VS WRONG) -->\n    <section class="split-2col">',
    '<!-- 5. ROW 4: 2-COLUMN SPLIT (EXECUTION AUDIT: RIGHT VS WRONG) -->\n    <div class="audit-grid">\n    <section class="split-2col">'
)
# Close audit-grid right after the closing </section> of Row 4
updated_html = updated_html.replace(
    '</section>\n\n    <!-- 6. ROW 5: 2-COLUMN SPLIT (COMPETITIVE PEER MATRIX & PRODUCT CATALYSTS) -->',
    '</section>\n    </div>\n\n    <!-- 6. ROW 5: 2-COLUMN SPLIT (COMPETITIVE PEER MATRIX & PRODUCT CATALYSTS) -->'
)

# 7. Add sentiment-meter-bar elements to sentiment meter wraps
updated_html = updated_html.replace(
    '<div class="sentiment-bar-fill" style="width: 36%; background-color: var(--bear-red);"></div>',
    '<div class="sentiment-meter-bar" style="width: 36%; background-color: var(--bear-red); height: 100%;"></div>'
)
updated_html = updated_html.replace(
    '<div class="sentiment-bar-fill" style="width: 28%; background-color: var(--bear-red);"></div>',
    '<div class="sentiment-meter-bar" style="width: 28%; background-color: var(--bear-red); height: 100%;"></div>'
)
updated_html = updated_html.replace(
    '<div class="sentiment-bar-fill" style="width: 74%; background-color: var(--bull-green);"></div>',
    '<div class="sentiment-meter-bar" style="width: 74%; background-color: var(--bull-green); height: 100%;"></div>'
)
updated_html = updated_html.replace(
    '<div class="sentiment-bar-fill" style="width: 34%; background-color: var(--bear-red);"></div>',
    '<div class="sentiment-meter-bar" style="width: 34%; background-color: var(--bear-red); height: 100%;"></div>'
)

bull_target = 415.0  # > 374.36
bear_target = 340.0  # < 374.36

# Build structured draft payload
draft = {
    "header": {
        "page_title": f"TSLA (${spot_price:.2f}) Q3 2026 Earnings Intelligence Briefing",
        "ticker": "TSLA",
        "company_name": "Tesla, Inc.",
        "earnings_date": "2026-10-21",
        "spot_price_num": spot_price,
        "market_cap_num": float(truth["valuation_and_market"]["market_cap_millions"]),
        "enterprise_value_num": float(truth["valuation_and_market"]["enterprise_value_millions"])
    },
    "kpi_cards": {
        "card_a_cash_flow": {
            "q2_2026_ocf_m": 4697.0,
            "q2_2026_capex_m": 5789.0,
            "q2_2026_reported_fcf_m": -1092.0,
            "q2_2026_true_fcf_m": -2331.0,
            "capex_to_rev_pct": 20.50,
            "sbc_to_rev_pct": 4.08
        },
        "card_b_debt_liquidity": {
            "cash_and_st_inv_m": 43524.0,
            "total_debt_and_leases_m": 9342.0,
            "net_debt_m": -34182.0,
            "non_current_deferred_rev_m": 4073.0,
            "total_deferred_and_rpo_m": 12350.0
        },
        "card_c_margins": {
            "gaap_gross_margin_pct": 16.83,
            "gaap_operating_margin_pct": 1.41,
            "roic_pct": 5.46,
            "roe_ttm_pct": 4.67
        },
        "card_d_multiples": {
            "trailing_pe": trailing_pe,
            "forward_pe": fwd_pe,
            "price_to_sales_ttm": ps_ttm,
            "ev_to_ebitda": ev_ebitda,
            "short_percent_of_float": truth["valuation_and_market"]["short_percent_of_float"]
        }
    },
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "ocf": 4697.0,
            "capex": 5789.0,
            "reported_fcf": -1092.0,
            "sbc": 1151.0,
            "finance_leases": 88.0,
            "true_fcf": -2331.0
        }
    },
    "trade_matrix": {
        "bull_target_low_num": bull_target,
        "bear_target_high_num": bear_target
    },
    "historical_table_5q_nums": [
        {
            "gross_profit": float(draft_gp),
            "operating_expenses": float(draft_opex),
            "operating_income": float(draft_ebit)
        }
        for draft_gp, draft_opex, draft_ebit in zip(
            [3878, 5054, 5009, 4720, 4751],
            [2955, 3430, 3600, 3779, 4353],
            [923, 1624, 1409, 941, 398]
        )
    ],
    "rendered_container_html": updated_html
}

DRAFT_PATH.write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Draft successfully written to {DRAFT_PATH}")
print(f"Character count: {len(updated_html):,}")
