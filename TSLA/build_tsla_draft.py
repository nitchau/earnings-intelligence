import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

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
end_marker = '</div>\n</body>'
start_idx = master_raw.find(start_marker) + len(start_marker)
end_idx = master_raw.rfind('</div>', 0, master_raw.find('</body>'))
container_html = master_raw[start_idx:end_idx].strip()

# Apply deterministic updates from ground truth
spot_price = truth["price_validation"]["yahoo_spot_price"] # 362.44
mkt_cap_t = round(truth["valuation_and_market"]["market_cap_millions"] / 1e6, 2) # 1.43
ev_t = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1e6, 2) # 1.42
trailing_pe = truth["valuation_and_market"]["trailing_pe"] # 341.92
fwd_pe = truth["valuation_and_market"]["forward_pe"] # 167.15
ps_ttm = truth["valuation_and_market"]["price_to_sales_ttm"] # 13.81
ev_ebitda = truth["valuation_and_market"]["ev_to_ebitda"] # 132.34
opt_move_pct = truth["options_positioning"]["atm_implied_move_pct"] # 7.46
opt_move_usd = truth["options_positioning"].get("atm_straddle_usd", 27.05)
pcr_oi = truth["options_positioning"]["put_call_oi_ratio"] # 0.66

updated_html = container_html

# 1. Spot Price replacement
updated_html = updated_html.replace(
    '<div class="price-value">$378.03 <span class="badge badge-bear">-15.8%',
    f'<div class="price-value">${spot_price:.2f} <span class="badge badge-bear">-19.2%'
)

# 2. Market Cap / EV replacement
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

# 3. Options Implied Move
updated_html = updated_html.replace(
    '±7.85% (±$29.68 / sh)',
    f'±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)'
)
updated_html = updated_html.replace(
    'elevated ±7.85% implied move',
    f'elevated ±{opt_move_pct:.2f}% implied move'
)

# 4. Valuation Multiples in Card D
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
updated_html = updated_html.replace(
    '188.1x',
    f'{fwd_pe:.1f}x'
)

# 5. Put/Call Open Interest Ratio in Sentiment options pillar
updated_html = updated_html.replace(
    '<span class="mono">1.14x</span> (72nd %-ile — defensive hedging)',
    f'<span class="mono">{pcr_oi:.2f}x</span> (Bullish/Speculative Calls Heavy)'
)
updated_html = updated_html.replace(
    'At 1.14x, there is heavier positioning in downside puts than upside calls.',
    f'At {pcr_oi:.2f}x, call volume significantly exceeds put open interest.'
)

# Build structured draft payload
draft = {
    "header": {
        "page_title": "TSLA — Pre-Earnings Forensic & Sentiment Tearsheet (Upcoming: Q3 2026 | Last Reported: Q2 2026)",
        "ticker": "TSLA",
        "company_name": "Tesla, Inc.",
        "earnings_date": "2026-10-21",
        "spot_price_num": float(spot_price),
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
            "short_percent_of_float": truth["valuation_and_market"]["short_percent_of_float"],
            "beta": truth["valuation_and_market"].get("beta", 2.30)
        }
    },
    "historical_table": {
        "quarters": ["Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026 (Actual)", "Q3 2026E (Est)"],
        "revenue_m": [22496, 28095, 24901, 22387, 28236, 27850],
        "gross_profit_m": [3878, 5054, 5009, 4720, 4751, 4957],
        "operating_expenses_m": [2955, 3430, 3600, 3779, 4353, 3955],
        "operating_income_ebit_m": [923, 1624, 1409, 941, 398, 1002],
        "net_income_common_m": [1172, 1373, 840, 477, 1114, 1295],
        "ocf_m": [2540, 6238, 3813, 3937, 4697, 5450],
        "capex_m": [2394, 2248, 2393, 2493, 5789, 6200],
        "reported_fcf_m": [146, 3990, 1420, 1444, -1092, -750],
        "sbc_m": [635, 663, 954, 1030, 1151, 1120],
        "true_fcf_m": [-584, 3235, 374, 324, -2331, -1960]
    },
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "ocf": 4697.0,
            "capex": 5789.0,
            "reported_fcf": -1092.0,
            "sbc": 1151.0,
            "finance_leases": 88.0,
            "true_fcf": -2331.0
        },
        "critical_flags": [
            "GAAP Net Income ($1,114M) vs. GAAP EBIT ($398M) Inversion via $1.0B SpaceX mark-to-market and CA DTA release",
            "Front-Loaded Physical AI & Silicon CapEx Surge ($5,789M in Q2 2026; >$25B FY26 guide)",
            "Warranty Reserve Adjustments & Regulatory Credit Cliff (-66.7% YoY in Q2 2026)",
            "Stock-Based Compensation Escalation (+81.3% YoY to $1,151M in Q2 2026)"
        ]
    },
    "execution_audit": {
        "wins": [
            "Record Q2 2026 Vehicle Deliveries (480,126 units) & >$100B TTM Revenue",
            "Services & Other Margin Breakout ($4.58B Rev, Record 14.1% Gross Margin)",
            "Commercial Unsupervised Robotaxi Live in 7 U.S. Metros",
            "Working Capital Discipline & Operating Cash Conversion ($8.63B H1 OCF)"
        ],
        "drags": [
            "Uncontrolled OpEx & R&D Burn Crushed Q2 2026 Operating Margin to 1.41% (-57% YoY EBIT)",
            "Quality Control & Warranty Reserve Blowout in Energy (-1,910 bps QoQ) & Auto",
            "Unmonetized Mega-CapEx Cycle (>$25B FY26 Guide) & Scope Creep into Semi Fabs",
            "Governance & Capital Allocation Friction ($2B SpaceX Stake, $1.95B AI Acq, $1.15B/qtr SBC)"
        ]
    },
    "peer_and_catalysts": {
        "peers": {
            "TSLA": {"rev_growth": "+25.5%", "gross_margin": "16.83%", "fcf_margin": "-3.87%", "capex_to_rev": "20.50%", "fwd_pe": f"{fwd_pe:.1f}x"},
            "BYD": {"rev_growth": "+19.4%", "gross_margin": "18.90%", "fcf_margin": "+6.40%", "capex_to_rev": "8.70%", "fwd_pe": "17.8x"},
            "RIVN": {"rev_growth": "+27.0%", "gross_margin": "10.80%", "fcf_margin": "-51.21%", "capex_to_rev": "21.83%", "fwd_pe": "N/M"},
            "GM": {"rev_growth": "+4.8%", "gross_margin": "13.60%", "fcf_margin": "+5.90%", "capex_to_rev": "5.80%", "fwd_pe": "6.4x"}
        },
        "catalysts": [
            "Unsupervised Robotaxi Fleet Expansion & Cybercab Volume Ramp (>1M paid miles target)",
            "Cortex 1 (>90 MW) & Cortex 2 (>115 MW) AI Compute in Texas",
            "Megapack 3 at Houston Megafactory & 4680/LFP Cell Ramp (22.3 GWh H1 deployed)",
            "Optimus Gen-1 Production Lines at Fremont & Tesla Semi SOP in Nevada"
        ]
    },
    "sentiment_analysis": {
        "composite_score": 43,
        "pillars": {
            "options": {"score": 36, "pcr_oi": pcr_oi, "implied_move_pct": opt_move_pct, "implied_move_usd": opt_move_usd},
            "revisions": {"score": 28, "up_vs_down": "6 Up vs 24 Down", "mean_target": 345.00},
            "retail": {"score": 74, "bull_bear_ratio": "74/26", "inflow_10d": "+$640M"},
            "insider_whale": {"score": 34, "insider_buys_vs_sales": "0 Buys vs $184M Sales"}
        }
    },
    "trade_matrix": {
        "bull_target_low_num": 415.0,
        "bear_target_high_num": 340.0,
        "bull_case": {"prob": "25%", "target_range": "$415–$430", "trigger": "Q3 Rev > $28.40B, Non-GAAP EPS >= $0.50, Auto ex-credits GM >= 17.8%"},
        "base_case": {"prob": "45%", "target_range": "$358–$388", "trigger": "Q3 Rev $27.40B–$28.10B, Non-GAAP EPS $0.41–$0.47, GM 17.2%–17.7%"},
        "bear_case": {"prob": "30%", "target_range": "$325–$340", "trigger": "Q3 Non-GAAP EPS <= $0.38, EBIT < $650M, CapEx > $6.3B"}
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
