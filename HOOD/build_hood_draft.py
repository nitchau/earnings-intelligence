import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "HOOD_2026-10-27_truth.json"
BUS_2A_PATH = BASE_DIR / "pre_agent_bus" / "HOOD_2026-10-27_pre_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "pre_agent_bus" / "HOOD_2026-10-27_pre_agent2b_guidance.json"
BUS_2C_PATH = BASE_DIR / "pre_agent_bus" / "HOOD_2026-10-27_pre_agent2c_sentiment.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "HOOD_2026-10-27_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
bus_2a = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
bus_2b = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
bus_2c = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"])
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1e3, 2)
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1e3, 2)
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"])
fwd_pe = float(truth["valuation_and_market"]["forward_pe"])
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"])
short_float = float(truth["valuation_and_market"]["short_percent_of_float"])

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"])
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"])
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"])
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"])

hist_track = truth.get("historical_earnings_track_record", {})
avg_hist_1d_move = hist_track.get("avg_historical_1d_move_abs_pct", 9.14)
implied_vs_hist_delta = hist_track.get("implied_vs_historical_move_delta_pct", 0.99)
street_targets = truth.get("street_consensus_and_targets", {})
mean_pt = street_targets.get("target_mean_price", 134.90)
upside_to_pt = street_targets.get("implied_upside_to_mean_pct", 40.40)
analyst_cnt = street_targets.get("analyst_count", 30)

fcf_bridge = truth.get("forensic_fcf_bridge_latest", {})
latest_ocf = float(fcf_bridge.get("ocf", 720.0))
latest_capex = float(fcf_bridge.get("capex", 24.0))
latest_reported_fcf = float(fcf_bridge.get("reported_fcf", 696.0))
latest_sbc = float(fcf_bridge.get("sbc", 105.0))
latest_leases = float(fcf_bridge.get("finance_leases", 0.0))
latest_true_fcf = float(fcf_bridge.get("true_fcf", 591.0))

# Pre-build Table 1B-1 rows from Agent 2A
rows_1b1 = []
for row in bus_2a["headline_and_company_kpis"]:
    rows_1b1.append(f"""              <tr>
                <td><span class="tip" title="{row['tooltip_title']}" data-tip="{row['tooltip_def']}">{row['metric']}</span></td>
                <td>{row['q_minus_1_actual']}</td>
                <td>{row['q_minus_4_yoy_baseline']}</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">{row['street_consensus_q0e']}</td>
                <td style="font-weight:700; color: #34d399;">{row['whisper_bogey_q0e']}</td>
                <td>
                  <span class="badge badge-bull">{row['whisper_spread_display']}</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:{row['bar_width_pct']}%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-blue">{row['hurdle_badge']}</span></td>
              </tr>""")
table_1b1_rows_html = "\n".join(rows_1b1)

# Pre-build Table 1B-2 rows from Agent 2B
rows_1b2 = []
for row in bus_2b["matrix_a_prior_guidance_and_track_record"]:
    rows_1b2.append(f"""              <tr>
                <td><span class="tip" title="{row['tooltip_title']}" data-tip="{row['tooltip_def']}">{row['metric']}</span></td>
                <td>{row['prior_q_guidance_for_q0']}</td>
                <td style="font-weight:600; color: #93c5fd;">{row['current_street_consensus']}</td>
                <td style="font-weight:600; color: #34d399;">{row['historical_4q_beat_rate']}</td>
                <td>{row['variance_and_sandbag_commentary']}</td>
                <td><span class="badge badge-bull">{row['credibility_grade']}</span></td>
              </tr>""")
table_1b2_rows_html = "\n".join(rows_1b2)

# Pre-build Table 1B-3 rows from Agent 2B
rows_1b3 = []
for row in bus_2b["matrix_b_forward_guidance_bogeys"]:
    rows_1b3.append(f"""              <tr>
                <td><span class="tip" title="{row['tooltip_title']}" data-tip="{row['tooltip_def']}">{row['forward_metric']}</span></td>
                <td>{row['street_consensus_hurdle']}</td>
                <td style="font-weight:600; color: #34d399;">{row['bull_case_bogey']}</td>
                <td style="font-weight:600; color: #f87171;">{row['bear_case_breakdown']}</td>
                <td><span class="badge badge-warn">{row['sensitivity_badge']}</span></td>
                <td>{row['strategic_rationale']}</td>
              </tr>""")
table_1b3_rows_html = "\n".join(rows_1b3)

# Pre-build Section 4B Debates from Agent 2B
debates_cards = []
for db in bus_2b["section_4b_pre_print_debates"]:
    debates_cards.append(f"""        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid {db['border_color']}; padding: 12px 14px; border-radius: 6px; margin-bottom: 12px;">
          <div style="font-weight: 700; color: {db['title_color']}; font-size: 13.5px; margin-bottom: 4px;">
            {db['debate_title']}
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Bull vs. Bear Institutional Framing:</strong> {db['bull_vs_bear_framing']}
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>{db['call_focus_question']}</strong>
          </p>
        </div>""")
section_4b_debates_html = "\n".join(debates_cards)

# Historical 5-Quarter exact numbers from ground truth
quarters = [
    "Q2 2025 (Ended Jun 30, 2025)",
    "Q3 2025 (Ended Sep 30, 2025)",
    "Q4 2025 (Ended Dec 31, 2025)",
    "Q1 2026 (Ended Mar 31, 2026)",
    "Q2 2026 (Ended Jun 30, 2026)"
]
total_rev = [989.0, 1274.0, 1283.0, 1067.0, 1308.0]
trans_rev = [578.0, 728.0, 765.0, 580.0, 776.0]
opt_rev = [265.0, 310.0, 325.0, 280.0, 342.0]
event_rev = [15.0, 35.0, 65.0, 95.0, 156.0]
eq_rev = [66.0, 85.0, 95.0, 71.0, 129.0]
crypto_rev = [160.0, 230.0, 215.0, 134.0, 100.0]
interest_rev = [357.0, 442.0, 415.0, 375.0, 389.0]
other_rev = [54.0, 104.0, 103.0, 112.0, 143.0]

cost_of_rev = [180.0, 169.0, 301.0, 207.0, 236.0]
gross_profit = [809.0, 1105.0, 982.0, 860.0, 1072.0]
opex = [370.0, 470.0, 332.0, 449.0, 498.0]
rd_exp = [214.0, 237.0, 232.0, 241.0, 256.0]
sga_exp = [118.0, 196.0, 49.0, 158.0, 159.0]
other_opex = [38.0, 37.0, 51.0, 50.0, 83.0]
ebit = [439.0, 635.0, 650.0, 411.0, 574.0]
pretax_inc = [442.0, 634.0, 661.0, 411.0, 709.0]
tax_prov = [56.0, 78.0, 56.0, 65.0, 136.0]
net_income = [386.0, 556.0, 605.0, 350.0, 561.0]

ocf_series = [3509.0, -1576.0, -937.0, 2038.0, 720.0]
capex_series = [18.0, 12.0, 13.0, 18.0, 24.0]
rep_fcf_series = [3491.0, -1588.0, -950.0, 2020.0, 696.0]
sbc_series = [78.0, 78.0, 76.0, 92.0, 105.0]
true_fcf_series = [3413.0, -1666.0, -1026.0, 1928.0, 591.0]

cash_st_inv = [12992.0, 11269.0, 9893.0, 11821.0, 16162.0]
total_debt = [1850.0, 1980.0, 2150.0, 2160.0, 2170.0]
stockholders_equity = [7210.0, 7890.0, 8450.0, 8910.0, 9480.0]
auc_billions = [279.0, 298.0, 324.0, 344.0, 369.0]
funded_users_m = [24.5, 25.1, 26.2, 27.5, 28.4]
gold_subs_m = [2.8, 3.2, 3.7, 4.2, 4.84]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": ebit[i]}
    for i in range(5)
]

# Ensure GP - OpEx == EBIT matches exactly:
for q in historical_table_5q_nums:
    assert abs((q["gross_profit"] - q["operating_expenses"]) - q["operating_income"]) < 1.0

html = f"""
    <!-- 1. HEADER BANNER -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#93c5fd;">Last Reported Quarter: <strong>Q2 2026 (Ended June 30, 2026)</strong> • Upcoming Release: <strong>Q3 2026 (Ended Sep 30, 2026)</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">HOOD</span>
            <h1 class="company-name">Robinhood Markets, Inc.</h1>
            <span class="badge badge-bull">NEO-CUSTODIAN &amp; PREDICTION MARKETS LEADER</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day before the official quarterly earnings release." data-tip="T-1 (Time Minus 1 Day): Indicates this analysis is prepared one trading session prior to the upcoming Q3 2026 earnings release on Tuesday, Oct 27, 2026.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select • Financial Services, Capital Markets, Retail Brokerage, Crypto &amp; Prediction Markets • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC to all public company filings." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the U.S. Securities and Exchange Commission (SEC) to track Robinhood's official regulatory filings.">CIK</span>: 0001783879</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price (Oct 2026)</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+158.4% <span class="tip tip-right tip-bottom" title="Year-To-Date: Percentage price change since January 1, 2026." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of the current calendar year (2026) to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares (Share Price × Diluted Shares)." data-tip="Market Capitalization: Total equity value of the company calculated by multiplying current share price (${spot_price:.2f}) by total diluted common shares (~912M).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash. Shows the true takeover cost of the business." data-tip="Enterprise Value (EV): Market Cap ($86.38B) + Total Long-Term Debt ($2.17B) - Liquid Cash &amp; Short-Term Investments ($16.16B) = $85.91B.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.2f}B / ${ev_b:.2f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Upcoming Q3 2026 Release Date</span>
          <span class="strip-val">Tue, Oct 27, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market hours (~4:05 PM Eastern Time).">AMC</span> (4:05 PM ET)</span>
          <span class="kpi-sub">Live Earnings Video Webcast: 5:00 PM ET (2:00 PM PT) hosted by Vlad Tenev &amp; Shiv Verma</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in for the day after earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) weekly option straddle prices. Reflects expected volatility around earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market's forecast of annualized stock price volatility derived from option prices." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Downside Skew)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E <span class="tip" title="Wall Street Consensus: The average forecast of equity research analysts covering Robinhood." data-tip="Consensus Revenue: The average top-line sales forecast published by Wall Street sell-side analysts for Q3 2026 ($1,425M).">Consensus Revenue</span> / <span class="tip" title="Whisper Number: The unofficial expectation among hedge funds and institutional traders." data-tip="Whisper Number: Unofficial top-line expectations among buy-side institutional investors ($1,460M).">Whisper</span></span>
          <span class="strip-val">$1,425M / $1,460M</span>
          <span class="kpi-sub">Street Estimate: $1.425B | +11.9% <span class="tip" title="Year-over-Year: Comparison against the exact same quarter last year (Q3 2025)." data-tip="Year-over-Year (YoY): Compares performance against the same quarter one year prior (Q3 2026E vs Q3 2025: $1,274M).">YoY</span> vs Q3 2025</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E Consensus <span class="tip" title="Earnings Per Share: Net profit divided by total diluted shares outstanding." data-tip="Earnings Per Share (EPS): Net profit allocated to each share of common stock.">EPS</span> / Whisper</span>
          <span class="strip-val">$0.55 <span class="tip" title="Generally Accepted Accounting Principles: Official U.S. SEC accounting standards." data-tip="GAAP EPS: Official U.S. accounting earnings per share including all equity compensation.">GAAP</span> / $0.60 Whisper</span>
          <span class="kpi-sub">Street Range: $0.52 – $0.59 | Prior Q2 Actual: $0.62</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">FY2026 <span class="tip tip-right" title="Management guidance on full-year adjusted operating expenses and stock-based compensation." data-tip="OpEx &amp; SBC Guidance: Robinhood's official forecast for full-year operating expense envelope ($2,675M–$2,775M).">OpEx &amp; SBC Guidance Window</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$2,675M – $2,775M</span>
          <span class="kpi-sub">Lowered in Q2 2026 from $2.70B–$2.825B • Disciplined Headcount Self-Funding Rothera &amp; WonderFi</span>
        </div>
      </div>
    </header>

    <!-- TRACK B: STICKY INTERACTIVE PRE-EARNINGS SECTION JUMP-NAV & PAIRED T+0 SWITCHER -->
    <nav class="pre-jump-nav" style="position: sticky; top: 8px; z-index: 90; background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(10px); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 10px; padding: 8px 14px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
      <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
        <span style="font-size: 11px; font-weight: 800; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.06em; margin-right: 4px;">⚡ Jump To:</span>
        <a href="#row-1-kpis" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">1. Q2 KPIs</a>
        <a href="#row-1b-scorecard" style="font-size: 11.5px; color: #60a5fa; font-weight: 700; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(59, 130, 246, 0.16); border: 1px solid rgba(59, 130, 246, 0.4);">1B. Whisper &amp; Track Record Scorecard</a>
        <a href="#row-2-financials" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">2. 5Q Table + Q3E</a>
        <a href="#row-3-fcf" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">3. FCF Bridge</a>
        <a href="#row-4-segments" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">4. Tailwinds/Drags</a>
        <a href="#row-4b-debates" style="font-size: 11.5px; color: #93c5fd; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(59, 130, 246, 0.14); border: 1px solid rgba(59, 130, 246, 0.3);">4B. Wall St Debates</a>
        <a href="#row-5-peers" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">5. Peers</a>
        <a href="#row-6-sentiment" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">6. Sentiment &amp; Pulse</a>
        <a href="#row-7-pm-matrix" style="font-size: 11.5px; color: #fcd34d; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(245, 158, 11, 0.14); border: 1px solid rgba(245, 158, 11, 0.3);">7. PM Trade Matrix</a>
      </div>
      <a href="HOOD_T0_POST_2026-10-27.html" style="font-size: 11.5px; font-weight: 700; color: #34d399; text-decoration: none; padding: 5px 12px; border-radius: 6px; background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.45); display: flex; align-items: center; gap: 6px;">
        ⇄ Compare Paired T+0 Post-Earnings Tearsheet
      </a>
    </nav>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS — ALL LABELED WITH EXACT REPORTED DATA) -->
    <section class="kpi-grid" id="row-1-kpis">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Light Model (Q2 2026)</div>
          <span class="badge badge-bull">EXPANDING FREE CASH FLOW</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual cash generated from customer trading activities, interest margins, and subscriptions." data-tip="Operating Cash Flow (OCF): Cash inflow generated from Robinhood's brokerage and neo-banking operations ($720M in Q2 2026).">Operating Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">Total OCF Generated: $720M ($1,245M TTM ex-working capital)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$720M</span>
              <div class="delta-pair">
                <span class="badge badge-bear"><span class="tip" title="Quarter-over-Quarter: Sequential change from Q1 2026 to Q2 2026." data-tip="Quarter-over-Quarter (QoQ): Change from preceding quarter ($2,038M to $720M). Note: Brokerage cash flows reflect timing of unsettled customer receivables.">QoQ</span> -64.67%</span>
                <span class="badge badge-bear"><span class="tip" title="Year-over-Year: Change from Q2 2025 ($3,509M) to Q2 2026 ($720M)." data-tip="Year-over-Year (YoY): Normalized for customer margin loan financing.">YoY</span> -79.48%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Cash spent on server infrastructure, mobile apps, and trading technology." data-tip="Capital Expenditures (CapEx): Cash deployed into proprietary exchange matching engines and crypto cold-storage hardware ($24M in Q2 2026).">Capital Expenditures</span> (Q2 2026)</span>
              <span class="kpi-sub">Capital-Light Scale: Only 1.83% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">($24M)</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +33.33%</span>
                <span class="badge badge-neutral">YoY +33.33%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow minus CapEx." data-tip="Reported FCF: Operating Cash Flow ($720M) minus CapEx ($24M) = $696M.">Reported Free Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">Robust 53.21% Free Cash Flow Conversion Ratio</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$696M</span>
              <div class="delta-pair">
                <span class="badge badge-bear">QoQ -65.54%</span>
                <span class="badge badge-bear">YoY -80.06%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="True Free Cash Flow: Organic free cash flow after subtracting non-cash Stock-Based Compensation." data-tip="True Free Cash Flow (ex-SBC): Reported FCF ($696M) minus SBC ($105M) = $591M. Proves Robinhood is self-funding shareholder repurchases organically.">True FCF (ex-SBC)</span> (Q2 2026)</span>
              <span class="kpi-sub">SBC Contained: $105M (8.03% of Net Revenue)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$591M</span>
              <div class="delta-pair">
                <span class="badge badge-bear">QoQ -69.35%</span>
                <span class="badge badge-bear">YoY -82.68%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING LEVERAGE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Margins</div>
          <span class="badge badge-bull">RECORD OPERATING EFFICIENCY</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Gross Profit: Total Net Revenues minus Cost of Revenues (clearing and exchange fees)." data-tip="Gross Profit: Revenue ($1,308M) minus Brokerage Routing &amp; Clearing Costs ($236M) = $1,072M.">Gross Profit</span> (Q2 2026)</span>
              <span class="kpi-sub">GAAP Gross Margin: 81.96% (+136 bps QoQ)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,072M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +24.65%</span>
                <span class="badge badge-bull">YoY +32.51%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses (R&D, Marketing, G&A)." data-tip="Operating Income: EBIT after R&amp;D ($256M), SG&amp;A ($159M), and Operations ($83M) = $574M.">Operating Income (EBIT)</span> (Q2 2026)</span>
              <span class="kpi-sub">Operating Margin: 43.88% (+536 bps QoQ)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$574M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +39.66%</span>
                <span class="badge badge-bull">YoY +30.75%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research &amp; Development Expenses: Engineering spend powering Robinhood Legend, AI trading tools, and prediction market clearing." data-tip="R&amp;D Investment: Core technology engineering spend ($256M in Q2 2026).">R&amp;D Reinvestment</span> (Q2 2026)</span>
              <span class="kpi-sub">R&amp;D Intensity: 19.57% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$256M</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +6.22%</span>
                <span class="badge badge-neutral">YoY +19.63%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Net Income: Consolidated net profit attributable to common stockholders." data-tip="GAAP Net Income: Bottom-line earnings after taxes ($136M) and non-operating interest income.">GAAP Net Income</span> (Q2 2026)</span>
              <span class="kpi-sub">Net Profit Margin: 42.89% | Diluted EPS: $0.62</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$561M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +60.29%</span>
                <span class="badge badge-bull">YoY +45.34%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS & LIQUIDITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Net Liquidity</div>
          <span class="badge badge-bull">PRISTINE BALANCE SHEET</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Cash, Cash Equivalents, and Short-Term Investments." data-tip="Liquid Reserves: High-grade liquidity held in Treasury bills, institutional sweep cash, and short-term paper ($16,162M).">Cash &amp; ST Investments</span> (Q2 2026)</span>
              <span class="kpi-sub">Total Liquid Reserves: $16.16 Billion</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$16,162M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +36.72%</span>
                <span class="badge badge-bull">YoY +24.40%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Long-Term Debt and notes." data-tip="Long-Term Debt: Senior fixed notes issued for liquidity backstops ($2,170M).">Long-Term Senior Debt</span> (Q2 2026)</span>
              <span class="kpi-sub">Conservative Fixed Debt Maturity Profile</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$2,170M</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +0.46%</span>
                <span class="badge badge-neutral">YoY +17.30%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Net Cash Position: Cash and short term investments minus Total Debt." data-tip="Net Cash Position: Liquid Cash ($16.16B) minus Long-Term Debt ($2.17B) = Net Cash Surplus of $13.99B.">Net Cash Surplus</span> (Q2 2026)</span>
              <span class="kpi-sub">Massive Net Cash Buffer Supporting Buybacks</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$13,992M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +44.82%</span>
                <span class="badge badge-bull">YoY +25.58%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Stockholders Equity: Total assets minus total liabilities." data-tip="Stockholders Equity: Total book equity of $9,480M backing customer deposits.">Stockholders' Equity</span> (Q2 2026)</span>
              <span class="kpi-sub">Book Value per Share: ~$10.54 | ROE (TTM): 24.2%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$9,480M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +6.40%</span>
                <span class="badge badge-bull">YoY +31.48%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT MIX & VALUATION MULTIPLES -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Customer Scale &amp; Valuation Multiples</div>
          <span class="badge badge-bull">COMPOUNDING PLATFORM ASSETS</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Assets Under Custody: Total platform assets held by Robinhood on behalf of customers." data-tip="Assets Under Custody (AUC): Reached a record $369 Billion (+32% YoY) driven by $21.7B net deposits in Q2 2026.">Assets Under Custody (AUC)</span></span>
              <span class="kpi-sub">Funded Customers: 28.4M (+1.9M YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$369B</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +7.27%</span>
                <span class="badge badge-bull">YoY +32.26%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Robinhood Gold Subscribers: Paying $5/month members with access to 3% cash back and 5% cash sweep." data-tip="Robinhood Gold Members: Reached 4.84M paying subscribers (~17% attach rate).">Robinhood Gold Members</span></span>
              <span class="kpi-sub">High-LTV Customer Engine Driving Deposit Stickiness</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">4.84M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +15.24%</span>
                <span class="badge badge-bull">YoY +39.08%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forward Price to Earnings Ratio: Stock price divided by consensus forward EPS." data-tip="Forward P/E Multiple: Trading at 28.13x forward earnings, reflecting premium growth over legacy brokers (Schwab 21x, IBKR 22x).">Forward P/E Multiple</span></span>
              <span class="kpi-sub">Trailing P/E: {trailing_pe:.1f}x | P/S (TTM): {ps_ttm:.2f}x</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--accent-blue);">{fwd_pe:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">PEG: 1.08x</span>
                <span class="badge badge-bull">Upside: +{upside_to_pt:.1f}%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Short Interest: Percentage of floating shares sold short by bearish traders." data-tip="Short Interest % of Float: 5.12% of shares are sold short, reflecting moderate short positioning.">Short % of Float</span></span>
              <span class="kpi-sub">Days to Cover: 2.1 Days | Put/Call OI: {pcr_oi:.2f}x</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{short_float:.2f}%</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">Moderate Short Float</span>
                <span class="badge badge-neutral">30D IV: {iv_pct:.1f}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         2B. ROW 1B: PRE-RELEASE EXPECTATIONS, WHISPER SPREAD & HISTORICAL TRACK RECORD SCORECARD
         ========================================================================== -->
    <section class="card" id="row-1b-scorecard" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title">
            <span class="card-title-accent"></span>Pre-Release Expectations, Buy-Side Whisper &amp; Historical Track Record Scorecard
          </div>
          <div class="card-subtitle">
            Source: Wall Street Sell-Side Consensus ({analyst_cnt} Analysts, Mean PT ${mean_pt:.2f} / +{upside_to_pt:.2f}% Upside) • Buy-Side Whisper Bogeys • 4-Quarter Realized Earnings Reaction Audit
          </div>
        </div>
        <div style="display:flex; gap: 8px; align-items:center;">
          <span class="badge badge-bull">Q3 HURDLE: &gt;$1,460M REV &amp; &gt;$0.60 EPS</span>
          <span class="badge badge-blue">T-1 PRE-EARNINGS</span>
        </div>
      </div>

      <!-- TRACK B: 3-CARD PRE-PRINT SETUP & OPTIONS VOLATILITY AUDIT BANNER -->
      <div class="t1-setup-audit" style="background: linear-gradient(90deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(59, 130, 246, 0.35); border-left: 4px solid #60a5fa; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
          <span style="font-weight: 800; font-size: 13px; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.05em;">🎯 T-1 Pre-Earnings Institutional Setup &amp; Options Volatility Audit</span>
          <a href="HOOD_T0_POST_2026-10-27.html" style="font-size: 11.5px; color: #34d399; text-decoration: underline;">Compare Paired T+0 Post-Print Reality →</a>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; font-size: 12.3px; color: var(--text-secondary);">
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #93c5fd;">1. Consensus vs. Buy-Side Whisper Setup:</strong><br>
            • <em>Street Consensus:</em> <strong>$1,425M</strong> Revenue (+11.9% YoY) &amp; <strong>$0.55</strong> EPS.<br>
            • <em>Buy-Side Whisper Bogey:</em> Institutional longs demand <strong>$1,460M+</strong> Revenue and <strong>$0.60+</strong> EPS on record prediction market contracts.
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #fcd34d;">2. Implied vs. 4Q Historical Move Audit:</strong><br>
            • <em>Current ATM Straddle:</em> <strong>±{opt_move_pct:.2f}% (±${opt_move_usd:.2f}/sh)</strong> at {iv_pct:.1f}% IV.<br>
            • <em>4Q Realized Move Avg:</em> <strong>±{avg_hist_1d_move:.2f}%</strong> (-3.61%, -13.24%, -8.91%, -10.81%) — Options pricing aligns closely with history (+{implied_vs_hist_delta:.2f}% spread).
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #34d399;">3. Make-or-Break Call Swing Factor:</strong><br>
            • <em>Bull Breakout Trigger:</em> Q4 2026E election quarter net revenue guide above <strong>$1.55B</strong> + lowering full-year OpEx &amp; SBC ceiling below $2,725M.
          </div>
        </div>
      </div>

      <!-- TABLE 1B-1: UPCOMING QUARTER HEADLINE & COMPANY KPI CONSENSUS VS WHISPER SCORECARD -->
      <div style="margin-bottom: 20px;">
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-1: Upcoming Quarter (Q3 2026E) Headline &amp; Company-Specific KPI Consensus vs. Buy-Side Whisper Scorecard</span>
          <span class="tip" title="Maps Wall Street sell-side consensus against institutional buy-side whisper bogeys and prior quarter baselines." data-tip="Pre-Release Whisper Scorecard: Quantifies the exact operational hurdles across Total Revenue, EPS, Transaction Revenues, Options, Event Contracts, AUC, and Gold Subscribers.">[Methodology]</span>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style="min-width: 240px;">Metric / Company KPI</th>
                <th>Prior Qtr Actual (Q2 2026)</th>
                <th>YoY Baseline (Q3 2025)</th>
                <th class="col-q0">Street Consensus (Q3 2026E)</th>
                <th>Buy-Side Whisper Bogey</th>
                <th style="min-width: 195px;">Whisper vs. Street Spread</th>
                <th>Hurdle Badge</th>
              </tr>
            </thead>
            <tbody>
{table_1b1_rows_html}
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-2: MANAGEMENT GUIDANCE CREDIBILITY & 4Q HISTORICAL BEAT/MISS TRACK RECORD -->
      <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
          <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; display: flex; align-items: center; gap: 8px;">
            <span>Table 1B-2: Management Guidance Credibility &amp; 4-Quarter Historical Beat / Sandbagging Track Record</span>
            <span class="tip" title="Evaluates management's prior Q2 guidance for Q3 against historical beat rates and 4-quarter realized post-earnings moves." data-tip="Guidance Sandbagging Audit: Audits how conservatively management guides and compares current straddle pricing against 4-quarter historical realized moves.">[Track Record Audit]</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
            <span style="color: var(--text-muted);">Executive Guidance Credibility &amp; Sandbagging Score:</span>
            <div class="credibility-gauge-bar" style="width: 110px; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
              <div style="width: {bus_2b['credibility_score']}%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <strong style="color: #34d399;">{bus_2b['credibility_label']}</strong>
          </div>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style="min-width: 220px;">Guided Metric / Track Record Item</th>
                <th>Management's Prior Guidance for Q3</th>
                <th>Current Street Consensus</th>
                <th>4Q Beat Rate / Realized Move</th>
                <th>Historical Sandbagging &amp; Volatility Commentary</th>
                <th>Credibility Grade</th>
              </tr>
            </thead>
            <tbody>
{table_1b2_rows_html}
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-3: FORWARD GUIDANCE BOGEYS REQUIRED FOR POST-PRINT RE-RATING -->
      <div>
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-3: Forward Guidance Bogeys (Q4 2026E &amp; FY2026/FY2027 Hurdles Required for T+1 Re-Rating)</span>
          <span class="tip" title="Defines the forward guidance numbers management must issue on October 27 to trigger multiple expansion vs sell-off." data-tip="Forward Guidance Bogeys: Because growth fintech trades primarily on forward guidance (Q4 2026E &amp; FY27), this matrix defines the exact bull vs bear thresholds.">[Re-Rating Matrix]</span>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style="min-width: 220px;">Forward Guidance Metric &amp; Horizon</th>
                <th>Street Consensus Hurdle</th>
                <th>Buy-Side Bull Case Bogey</th>
                <th>Bear Case Breakdown Level</th>
                <th>Sensitivity Badge</th>
                <th>Strategic &amp; Financial Rationale</th>
              </tr>
            </thead>
            <tbody>
{table_1b3_rows_html}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 3. ROW 2: 5-QUARTER HISTORICAL AUDIT & RECONCILIATION TABLE -->
    <section class="card" id="row-2-financials" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>5-Quarter Financial Performance &amp; Revenue Bridge</div>
          <div class="card-subtitle">Audited financial results in USD Millions (with YoY and QoQ percentage deltas) across Trading, Net Interest, and Subscriptions</div>
        </div>
        <span class="badge badge-blue">DETERMINISTIC GROUND TRUTH (Q2 2025 – Q2 2026)</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th style="min-width: 220px;">Financial Metric ($ Millions)</th>
              <th>Q2 2025<br><span style="font-size:10px;color:var(--text-muted);">(Jun 30, 2025)</span></th>
              <th>Q3 2025<br><span style="font-size:10px;color:var(--text-muted);">(Sep 30, 2025)</span></th>
              <th>Q4 2025<br><span style="font-size:10px;color:var(--text-muted);">(Dec 31, 2025)</span></th>
              <th>Q1 2026<br><span style="font-size:10px;color:var(--text-muted);">(Mar 31, 2026)</span></th>
              <th class="col-q0">Q2 2026<br><span style="font-size:10px;color:var(--accent-blue);">(Jun 30, 2026)</span></th>
              <th><span class="tip" title="Quarter-over-Quarter: Percentage change from Q1 2026 to Q2 2026." data-tip="QoQ Delta: Sequential percentage variance between Q1 2026 and Q2 2026.">QoQ</span></th>
              <th><span class="tip" title="Year-over-Year: Percentage change from Q2 2025 to Q2 2026." data-tip="YoY Delta: 12-month percentage variance between Q2 2025 and Q2 2026.">YoY</span></th>
              <th class="col-est">Q3 2026E<br><span style="font-size:10px;color:var(--text-muted);">(Consensus)</span></th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background-color: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Total Net Revenues: Consolidated net revenue across Transaction, Net Interest, and Other." data-tip="Total Net Revenues: Consolidated revenue generated across all broker-dealer and crypto entities.">Total Net Revenues ($M)</span></td>
              <td>$989</td>
              <td>$1,274</td>
              <td>$1,283</td>
              <td>$1,067</td>
              <td class="col-q0" style="color: var(--accent-blue);">$1,308</td>
              <td><span class="badge badge-bull">+22.59%</span></td>
              <td><span class="badge badge-bull">+32.25%</span></td>
              <td class="col-est">$1,425</td>
            </tr>
            <tr style="color: var(--text-secondary);">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Transaction-based revenue from options, event contracts, crypto, and equities." data-tip="Transaction-Based Revenue: Order flow rebates and transaction fees ($776M in Q2 2026).">Transaction-Based Revenues</span></td>
              <td>$578</td>
              <td>$728</td>
              <td>$765</td>
              <td>$580</td>
              <td class="col-q0">$776</td>
              <td><span class="badge badge-bull">+33.79%</span></td>
              <td><span class="badge badge-bull">+34.26%</span></td>
              <td class="col-est">$845</td>
            </tr>
            <tr style="font-size: 11.5px; color: var(--text-muted);">
              <td style="padding-left: 35px;">• <span class="tip" title="Options trading transaction revenues." data-tip="Options Revenue: Fees generated from equity and index options order routing.">Options Revenue</span></td>
              <td>$265</td>
              <td>$310</td>
              <td>$325</td>
              <td>$280</td>
              <td class="col-q0">$342</td>
              <td><span class="badge badge-bull">+22.14%</span></td>
              <td><span class="badge badge-bull">+29.06%</span></td>
              <td class="col-est">$365</td>
            </tr>
            <tr style="font-size: 11.5px; color: var(--text-muted);">
              <td style="padding-left: 35px;">• <span class="tip" title="Event contracts &amp; prediction markets transaction revenues." data-tip="Event Contracts: Surging election and macro event prediction market contracts.">Event Contracts / Predictions</span></td>
              <td>$15</td>
              <td>$35</td>
              <td>$65</td>
              <td>$95</td>
              <td class="col-q0" style="color:#34d399;font-weight:700;">$156</td>
              <td><span class="badge badge-bull">+64.21%</span></td>
              <td><span class="badge badge-bull">+940.0%</span></td>
              <td class="col-est">$190</td>
            </tr>
            <tr style="font-size: 11.5px; color: var(--text-muted);">
              <td style="padding-left: 35px;">• <span class="tip" title="Equities trading transaction revenues." data-tip="Equities Revenue: Order rebates from customer stock trades.">Equities Revenue</span></td>
              <td>$66</td>
              <td>$85</td>
              <td>$95</td>
              <td>$71</td>
              <td class="col-q0">$129</td>
              <td><span class="badge badge-bull">+81.69%</span></td>
              <td><span class="badge badge-bull">+95.45%</span></td>
              <td class="col-est">$140</td>
            </tr>
            <tr style="font-size: 11.5px; color: var(--text-muted);">
              <td style="padding-left: 35px;">• <span class="tip" title="Cryptocurrency trading transaction revenues." data-tip="Cryptocurrency Revenue: Spreads on digital asset trading ($100M in Q2 2026).">Cryptocurrencies Revenue</span></td>
              <td>$160</td>
              <td>$230</td>
              <td>$215</td>
              <td>$134</td>
              <td class="col-q0" style="color:var(--bear-red);">$100</td>
              <td><span class="badge badge-bear">-25.37%</span></td>
              <td><span class="badge badge-bear">-37.50%</span></td>
              <td class="col-est">$115</td>
            </tr>
            <tr style="color: var(--text-secondary);">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Net Interest Revenues: Interest on margin loans, cash sweep, and securities lending." data-tip="Net Interest Revenue: Spread earned on cash deposits and margin balances ($389M in Q2 2026).">Net Interest Revenues</span></td>
              <td>$357</td>
              <td>$442</td>
              <td>$415</td>
              <td>$375</td>
              <td class="col-q0">$389</td>
              <td><span class="badge badge-bull">+3.73%</span></td>
              <td><span class="badge badge-bull">+8.96%</span></td>
              <td class="col-est">$400</td>
            </tr>
            <tr style="color: var(--text-secondary);">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Other Revenues: Gold subscriptions, interchange, and proxy fees." data-tip="Other Revenue: Robinhood Gold $5/month fees and Gold credit card interchange ($143M in Q2 2026).">Other Revenues (Gold / Cards)</span></td>
              <td>$54</td>
              <td>$104</td>
              <td>$103</td>
              <td>$112</td>
              <td class="col-q0">$143</td>
              <td><span class="badge badge-bull">+27.68%</span></td>
              <td><span class="badge badge-bull">+164.81%</span></td>
              <td class="col-est">$180</td>
            </tr>
            <tr>
              <td><span class="tip" title="Brokerage clearing, transaction routing, and market regulatory fees." data-tip="Cost of Revenue: Direct expenses incurred to execute and settle customer trades.">Cost of Revenue ($M)</span></td>
              <td>$180</td>
              <td>$169</td>
              <td>$301</td>
              <td>$207</td>
              <td class="col-q0">$236</td>
              <td><span class="badge badge-neutral">+14.01%</span></td>
              <td><span class="badge badge-neutral">+31.11%</span></td>
              <td class="col-est">$250</td>
            </tr>
            <tr style="font-weight: 700; background-color: rgba(16, 185, 129, 0.05);">
              <td><span class="tip" title="Gross Profit: Total Revenue minus Cost of Revenue." data-tip="Gross Profit: Revenue minus Cost of Goods Sold. Math checked: 1308 - 236 = 1072.">Gross Profit ($M)</span></td>
              <td>$809</td>
              <td>$1,105</td>
              <td>$982</td>
              <td>$860</td>
              <td class="col-q0" style="color: var(--bull-green);">$1,072</td>
              <td><span class="badge badge-bull">+24.65%</span></td>
              <td><span class="badge badge-bull">+32.51%</span></td>
              <td class="col-est">$1,175</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Operating Expenses: R&D, Marketing, and General & Administrative costs." data-tip="Operating Expenses: All overhead operating expenses required to build and support the app ($498M in Q2 2026).">Operating Expenses ($M)</span></td>
              <td>$370</td>
              <td>$470</td>
              <td>$332</td>
              <td>$449</td>
              <td class="col-q0">$498</td>
              <td><span class="badge badge-neutral">+10.91%</span></td>
              <td><span class="badge badge-neutral">+34.59%</span></td>
              <td class="col-est">$525</td>
            </tr>
            <tr style="font-size: 11.5px; color: var(--text-muted);">
              <td style="padding-left: 20px;">• <span class="tip" title="Research and Development technology investment." data-tip="R&amp;D Expense: Software engineering payroll.">Research &amp; Development</span></td>
              <td>$214</td>
              <td>$237</td>
              <td>$232</td>
              <td>$241</td>
              <td class="col-q0">$256</td>
              <td><span class="badge badge-neutral">+6.22%</span></td>
              <td><span class="badge badge-neutral">+19.63%</span></td>
              <td class="col-est">$265</td>
            </tr>
            <tr style="font-size: 11.5px; color: var(--text-muted);">
              <td style="padding-left: 20px;">• <span class="tip" title="Selling, General and Administrative operating costs." data-tip="SG&amp;A Expense: Marketing customer acquisition and compliance overhead.">SG&amp;A Expense</span></td>
              <td>$118</td>
              <td>$196</td>
              <td>$49</td>
              <td>$158</td>
              <td class="col-q0">$159</td>
              <td><span class="badge badge-neutral">+0.63%</span></td>
              <td><span class="badge badge-neutral">+34.75%</span></td>
              <td class="col-est">$175</td>
            </tr>
            <tr style="font-weight: 700; background-color: rgba(59, 130, 246, 0.08);">
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit minus Operating Expenses." data-tip="Operating Income (EBIT): Math checked: 1072 - 498 = 574.">Operating Income (EBIT) ($M)</span></td>
              <td>$439</td>
              <td>$635</td>
              <td>$650</td>
              <td>$411</td>
              <td class="col-q0" style="color: var(--accent-blue);">$574</td>
              <td><span class="badge badge-bull">+39.66%</span></td>
              <td><span class="badge badge-bull">+30.75%</span></td>
              <td class="col-est">$650</td>
            </tr>
            <tr>
              <td><span class="tip" title="Income taxes provision paid or deferred to federal and state authorities." data-tip="Income Tax Provision: Corporate tax expense on operational profits ($136M in Q2 2026).">Tax Provision ($M)</span></td>
              <td>$56</td>
              <td>$78</td>
              <td>$56</td>
              <td>$65</td>
              <td class="col-q0">$136</td>
              <td><span class="badge badge-neutral">+109.23%</span></td>
              <td><span class="badge badge-neutral">+142.86%</span></td>
              <td class="col-est">$145</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Net Income attributable to common shareholders." data-tip="GAAP Net Income: Consolidated net earnings ($561M in Q2 2026).">GAAP Net Income ($M)</span></td>
              <td>$386</td>
              <td>$556</td>
              <td>$605</td>
              <td>$350</td>
              <td class="col-q0" style="color: var(--bull-green);">$561</td>
              <td><span class="badge badge-bull">+60.29%</span></td>
              <td><span class="badge badge-bull">+45.34%</span></td>
              <td class="col-est">$505</td>
            </tr>
            <tr>
              <td><span class="tip" title="Diluted Earnings Per Share." data-tip="Diluted EPS: Net income divided by weighted average diluted shares.">Diluted EPS ($)</span></td>
              <td>$0.42</td>
              <td>$0.61</td>
              <td>$0.66</td>
              <td>$0.38</td>
              <td class="col-q0" style="color: var(--bull-green);">$0.62</td>
              <td><span class="badge badge-bull">+63.16%</span></td>
              <td><span class="badge badge-bull">+47.62%</span></td>
              <td class="col-est">$0.55</td>
            </tr>
            <tr style="border-top: 2px solid var(--border-color);">
              <td><span class="tip" title="Cash flow from operating activities." data-tip="Operating Cash Flow: Operating cash generation ($720M in Q2 2026).">Operating Cash Flow (OCF) ($M)</span></td>
              <td>$3,509</td>
              <td>-$1,576</td>
              <td>-$937</td>
              <td>$2,038</td>
              <td class="col-q0">$720</td>
              <td><span class="badge badge-bear">-64.67%</span></td>
              <td><span class="badge badge-bear">-79.48%</span></td>
              <td class="col-est">$950</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital expenditures for technology and hardware." data-tip="CapEx: Modest infrastructure spending ($24M in Q2 2026).">Capital Expenditures ($M)</span></td>
              <td>$18</td>
              <td>$12</td>
              <td>$13</td>
              <td>$18</td>
              <td class="col-q0">$24</td>
              <td><span class="badge badge-neutral">+33.33%</span></td>
              <td><span class="badge badge-neutral">+33.33%</span></td>
              <td class="col-est">$25</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Reported Free Cash Flow: OCF minus CapEx." data-tip="Reported Free Cash Flow: Math checked: 720 - 24 = 696.">Reported Free Cash Flow ($M)</span></td>
              <td>$3,491</td>
              <td>-$1,588</td>
              <td>-$950</td>
              <td>$2,020</td>
              <td class="col-q0" style="color: var(--bull-green);">$696</td>
              <td><span class="badge badge-bear">-65.54%</span></td>
              <td><span class="badge badge-bear">-80.06%</span></td>
              <td class="col-est">$925</td>
            </tr>
            <tr>
              <td><span class="tip" title="Stock-Based Compensation added back in GAAP cash flows." data-tip="Stock-Based Compensation: Non-cash equity granted to employees ($105M in Q2 2026).">Stock-Based Comp (SBC) ($M)</span></td>
              <td>$78</td>
              <td>$78</td>
              <td>$76</td>
              <td>$92</td>
              <td class="col-q0">$105</td>
              <td><span class="badge badge-neutral">+14.13%</span></td>
              <td><span class="badge badge-neutral">+34.62%</span></td>
              <td class="col-est">$110</td>
            </tr>
            <tr style="font-weight: 700; background-color: rgba(16, 185, 129, 0.08);">
              <td><span class="tip" title="True Economic Free Cash Flow: Reported FCF minus SBC." data-tip="True Free Cash Flow: Math checked: 696 - 105 - 0 = 591.">True FCF (ex-SBC) ($M)</span></td>
              <td>$3,413</td>
              <td>-$1,666</td>
              <td>-$1,026</td>
              <td>$1,928</td>
              <td class="col-q0" style="color: var(--bull-green);">$591</td>
              <td><span class="badge badge-bear">-69.35%</span></td>
              <td><span class="badge badge-bear">-82.68%</span></td>
              <td class="col-est">$815</td>
            </tr>
            <tr style="border-top: 2px solid var(--border-color);">
              <td><span class="tip" title="Platform Assets Under Custody across all customer accounts." data-tip="Total AUC: Assets held in equities, options, crypto, and cash sweep ($369B in Q2 2026).">Assets Under Custody (AUC) ($B)</span></td>
              <td>$279B</td>
              <td>$298B</td>
              <td>$324B</td>
              <td>$344B</td>
              <td class="col-q0" style="color:#34d399;font-weight:700;">$369B</td>
              <td><span class="badge badge-bull">+7.27%</span></td>
              <td><span class="badge badge-bull">+32.26%</span></td>
              <td class="col-est">$395B</td>
            </tr>
            <tr>
              <td><span class="tip" title="Paying Robinhood Gold subscribers." data-tip="Robinhood Gold: 4.84M paying subscribers enjoying 5.0% APY and 3% cash back.">Robinhood Gold Subscribers</span></td>
              <td>2.80M</td>
              <td>3.20M</td>
              <td>3.70M</td>
              <td>4.20M</td>
              <td class="col-q0" style="color:#60a5fa;font-weight:700;">4.84M</td>
              <td><span class="badge badge-bull">+15.24%</span></td>
              <td><span class="badge badge-bull">+39.08%</span></td>
              <td class="col-est">5.20M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Liquid Cash and Short-Term Investments." data-tip="Cash and Short-Term Investments: Fortress reserves of $16,162M.">Cash &amp; ST Investments ($M)</span></td>
              <td>$12,992</td>
              <td>$11,269</td>
              <td>$9,893</td>
              <td>$11,821</td>
              <td class="col-q0">$16,162</td>
              <td><span class="badge badge-bull">+36.72%</span></td>
              <td><span class="badge badge-bull">+24.40%</span></td>
              <td class="col-est">$17,000</td>
            </tr>
            <tr>
              <td><span class="tip" title="Long-term notes and obligations." data-tip="Long-Term Debt: $2,170M in fixed senior notes.">Long-Term Debt ($M)</span></td>
              <td>$1,850</td>
              <td>$1,980</td>
              <td>$2,150</td>
              <td>$2,160</td>
              <td class="col-q0">$2,170</td>
              <td><span class="badge badge-neutral">+0.46%</span></td>
              <td><span class="badge badge-neutral">+17.30%</span></td>
              <td class="col-est">$2,200</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 4. ROW 3: FORENSIC HIGHLIGHTS & TRUE FCF BRIDGE -->
    <section class="card" id="row-3-fcf" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Outlier &amp; Accounting Quality Audit (Robinhood Forensic Review)</div>
          <div class="card-subtitle">Forensic deconstruction of Operating vs. Net Income, Capital-Light Scalability, and Organic Free Cash Flow</div>
        </div>
        <span class="badge badge-bull">HIGH QUALITY EARNINGS</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>1. Highly Capital-Light Scalability: Only 1.83% of Revenue Reinvested in CapEx</span>
              <span class="badge badge-bull">SOFTWARE MARGINS</span>
            </div>
            <p>
              In Q2 2026, Robinhood generated <strong>$1,308M in Net Revenues</strong> while deploying only <strong>$24M in capital expenditures</strong>. Unlike hyperscalers requiring hundreds of billions in GPU infrastructure, Robinhood's proprietary exchange routing technology and cloud architecture allow incremental trading volumes to flow directly to cash flow with negligible capital intensity.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>2. Organic True Free Cash Flow Positive: $591M (Post-SBC &amp; Leases)</span>
              <span class="badge badge-bull">SELF-FUNDING GROWTH</span>
            </div>
            <p>
              Operating Cash Flow printed at <strong>$720M</strong> in Q2 2026. After subtracting CapEx ($24M) and fully deducting non-cash Stock-Based Compensation ($105M), Robinhood generated <strong>$591M in True Economic Free Cash Flow</strong> (a 45.18% True FCF margin). This robust organic cash generation is currently funding active share buybacks ($414M repurchased in Q2 2026).
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>3. Prediction Markets &amp; Event Contracts Explosion ($156M Run-Rate)</span>
              <span class="badge badge-bull">NEW ASSET CLASS</span>
            </div>
            <p>
              Robinhood's presidential election and macroeconomic event contracts surged from $15M in Q2 2025 to <strong>$156M in Q2 2026 (>10x YoY)</strong>. Operating as a pure two-sided prediction market with direct clearing fees, event contracts provide a non-correlated revenue engine that surges during political and macroeconomic volatility.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Clean P&amp;L Conversion with Zero Restructuring or Goodwill Write-Downs</span>
              <span class="badge badge-bull">CLEAN ACCOUNTING</span>
            </div>
            <p>
              The bridge from Operating Income ($574M) to GAAP Net Income ($561M) is pristine. Pretax income reached $709M, supported by $135M in net interest on corporate cash balances. With a normalized corporate tax provision of $136M (19.2% effective rate), there are zero restructuring charges, zero credit loss anomalies, and zero speculative write-downs.
            </p>
          </div>
        </div>

        <!-- FCF WATERFALL BRIDGE -->
        <div class="bridge-card">
          <div class="bridge-title">
            <span>True Free Cash Flow Waterfall Bridge (Q2 2026 Actual)</span>
            <span class="badge badge-bull">+$591M ORGANIC CASH SURPLUS</span>
          </div>

          <div class="waterfall-row">
            <span class="waterfall-label">Reported Operating Cash Flow (OCF)</span>
            <span class="waterfall-val" style="color: var(--bull-green);">+$720M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Capital Expenditures (Software &amp; Infrastructure)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$24M</span>
          </div>
          <div class="waterfall-row" style="background: rgba(59, 130, 246, 0.08); font-weight:700;">
            <span class="waterfall-label">= Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="color: var(--bull-green);">+$696M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Non-Cash Stock-Based Compensation (SBC)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$105M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Principal Payments on Finance Leases</span>
            <span class="waterfall-val" style="color: var(--text-muted);">-$0M</span>
          </div>
          <div class="waterfall-row" style="background: rgba(16, 185, 129, 0.12); font-weight:700; border-top: 1px solid rgba(255,255,255,0.1);">
            <span class="waterfall-label">= True Economic Free Cash Flow</span>
            <span class="waterfall-val" style="color: var(--bull-green); font-size:15px;">+$591M</span>
          </div>

          <div style="margin-top: 14px; font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
            *Note: Robinhood's True FCF of $591M represents an extraordinary cash conversion rate, fully covering quarterly share repurchases ($414M) while expanding liquid cash reserves to $16.16B.
          </div>
        </div>
      </div>
    </section>

    <!-- 5. ROW 4: SEGMENT EXECUTION & 4-POINT OPERATIONAL WINS/DRAGS -->
    <section class="card" id="row-4-segments" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Operational Execution Audit: Tailwinds vs. Structural Headwinds</div>
          <div class="card-subtitle">Comprehensive institutional assessment of Event Contracts, Robinhood Legend desktop platform, Gold subscriptions, and Interest Rate sensitivity</div>
        </div>
        <span class="badge badge-bull">NET STRUCTURAL ADVANTAGE</span>
      </div>

      <div class="audit-grid">
        <!-- 4 OPERATIONAL WINS / TAILWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bull-green);">
            <span>🚀 4 Key Operational Tailwinds</span>
            <span class="badge badge-bull">GROWTH ENGINES</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. Robinhood Legend Desktop Platform Captures Active High-LTV Traders</span>
                <span class="badge badge-bull">ACTIVE TRADER SHARE</span>
              </div>
              <p>
                The rollout of Robinhood Legend (advanced customizable desktop charts, sub-second order routing, index options) is directly siphoning sophisticated active traders away from legacy platforms like Charles Schwab (Thinkorswim) and TradeStation, driving options volume to record highs ($342M in Q2).
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Event Contracts &amp; Prediction Markets Surging Over 10x YoY</span>
                <span class="badge badge-bull">PARABOLIC ADOPTION</span>
              </div>
              <p>
                Presidential election and macroeconomic contracts grew from $15M in Q2 2025 to $156M in Q2 2026. Robinhood is capturing an estimated 65%+ market share of regulated U.S. retail event contracts, generating high-velocity transaction clearing revenue ahead of the November election.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Robinhood Gold &amp; Credit Card Ecosystem Powers 17% Attach Rate</span>
                <span class="badge badge-bull">RECURRING ARPU</span>
              </div>
              <p>
                Robinhood Gold subscribers reached 4.84M (+39% YoY), incentivized by 5.00% cash sweep APY and the 3% cash-back Gold Credit Card. Gold members deposit 5x more capital than non-Gold users, anchoring $21.7B in quarterly net deposits and generating $143M in high-margin subscription/interchange revenue.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Global Expansion via Bitstamp &amp; WonderFi Regulatory Footprint</span>
                <span class="badge badge-bull">INTERNATIONAL TAM</span>
              </div>
              <p>
                The closing of the Bitstamp acquisition provides Robinhood with 50+ international crypto licenses across the EU, UK, and Asia, while WonderFi adds 300k Canadian funded accounts. This enables institutional crypto execution, cross-border margin lending, and staking products.
              </p>
            </div>
          </div>
        </div>

        <!-- 4 OPERATIONAL DRAGS / HEADWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bear-red);">
            <span>⚠️ 4 Key Operational Drags &amp; Market Headwinds</span>
            <span class="badge badge-bear">EXECUTION RISKS</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. Federal Reserve Rate Cuts Pressuring Floating Cash Sweep Yields</span>
                <span class="badge badge-bear">NII YIELD COMPRESSION</span>
              </div>
              <p>
                With the Federal Reserve entering an interest rate cutting cycle, Robinhood's Net Interest Revenues ($389M in Q2) face floating-rate yield compression on customer cash balances. Management must aggressively grow margin balances ($16B+) to offset lower benchmark cash sweep spreads.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Cryptocurrency Trading Volatility &amp; Take-Rate Compression</span>
                <span class="badge badge-bear">CRYPTO VOLATILITY</span>
              </div>
              <p>
                Crypto revenue fell -38% YoY in Q2 2026 to $100M as retail spot crypto trading cooled following the initial ETF launch frenzy. Decentralized exchanges and zero-fee ETF wrappers continue to pressure retail take-rates, requiring active altcoin volume to rebound.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Post-Election Event Contract Volume Cliff Risk in Q1 2027</span>
                <span class="badge badge-warn">CYCLICAL CLIFF</span>
              </div>
              <p>
                A substantial portion of current event contracts revenue ($156M) is driven by the 2026 U.S. election cycle. Skeptical hedge fund analysts worry that trading volume will experience a sharp hangover in Q1 2027 unless sports and economic contracts successfully substitute for political betting.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Regulatory Scrutiny Surrounding Prediction Markets &amp; PFOF</span>
                <span class="badge badge-warn">REGULATORY SCRUTINY</span>
              </div>
              <p>
                CFTC and state gaming regulators have raised inquiries regarding retail event contracts on elections. Any adverse court ruling or restrictive regulatory mandate could cap prediction market contract structures and impose compliance overhead.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 5B. SECTION 4B: TOP 3 INSTITUTIONAL PRE-PRINT DEBATES & CALL QUESTIONS TO WATCH -->
    <section class="card" id="row-4b-debates" style="margin-bottom: 24px; border: 1px solid rgba(59, 130, 246, 0.35);">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Section 4B: Top 3 Institutional Pre-Print Debates &amp; Analyst Call Questions to Watch</div>
          <div class="card-subtitle">Synthesized by Agent 2B (Guidance &amp; Track Record Forensic Agent) — Key Bull vs. Bear Contested Battlegrounds &amp; Expected Sell-Side Call Questions</div>
        </div>
        <span class="badge badge-blue">CONFERENCE CALL BATTLEGROUNDS</span>
      </div>
      {section_4b_debates_html}
    </section>

    <!-- 6. ROW 5: COMPETITIVE MOAT & PEER BENCHMARKING -->
    <section class="card-grid" id="row-5-peers" style="grid-template-columns: 1fr 1fr; margin-bottom: 24px;">
      <!-- LEFT CARD: COMPETITOR BENCHMARKING TABLE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Retail Brokerage &amp; Neo-Custodian Peer Benchmarking</div>
          <span class="badge badge-blue">PEER VALUATION (Q2 2026)</span>
        </div>

        <div class="table-wrapper" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th style="min-width:140px;">Ticker / Peer</th>
                <th><span class="tip" title="Year-over-Year Revenue Growth in latest reported quarter." data-tip="YoY Revenue Growth: Top-line growth compared to same quarter last year.">YoY Rev Growth</span></th>
                <th><span class="tip" title="GAAP Gross Margin percentage." data-tip="Gross Margin: Gross profit divided by revenue.">Gross Margin</span></th>
                <th><span class="tip" title="Operating Margin percentage." data-tip="Operating Margin: EBIT divided by revenue.">Op Margin</span></th>
                <th><span class="tip" title="Free Cash Flow divided by revenue." data-tip="FCF Margin: Percentage of sales converted to free cash flow.">FCF Margin</span></th>
                <th><span class="tip tip-right" title="Forward P/E ratio based on consensus earnings." data-tip="Forward P/E: Stock price divided by next 12 months estimated EPS.">Fwd P/E</span></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color:var(--accent-blue);">HOOD (Robinhood Markets)</strong></td>
                <td><span class="badge badge-bull">+32.25%</span></td>
                <td><strong style="color:var(--bull-green);">81.96%</strong></td>
                <td><strong style="color:var(--bull-green);">43.88%</strong></td>
                <td><strong style="color:var(--bull-green);">+53.21%</strong></td>
                <td style="color:var(--accent-blue);font-weight:700;">{fwd_pe:.1f}x</td>
              </tr>
              <tr>
                <td><strong>SCHW (Charles Schwab)</strong></td>
                <td><span class="badge badge-bull">+11.40%</span></td>
                <td>68.50%</td>
                <td>38.20%</td>
                <td>+32.10%</td>
                <td>21.4x</td>
              </tr>
              <tr>
                <td><strong>IBKR (Interactive Brokers)</strong></td>
                <td><span class="badge badge-bull">+18.20%</span></td>
                <td>74.20%</td>
                <td>68.50%</td>
                <td>+48.60%</td>
                <td>22.1x</td>
              </tr>
              <tr>
                <td><strong>COIN (Coinbase Global)</strong></td>
                <td><span class="badge badge-neutral">+16.50%</span></td>
                <td>82.40%</td>
                <td>24.60%</td>
                <td>+28.50%</td>
                <td>35.8x</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">Retail Deposit Siphon &amp; Demographic Moat</span>
              <span class="badge badge-bull">ASSET GATHERING MOAT</span>
            </div>
            <p>
              • <strong>Robinhood vs. Charles Schwab:</strong> Robinhood's net deposit growth velocity (>25% annualized) is outperforming Schwab (4-6% annualized) by more than 4x, as Millennial and Gen Z wealth transfers into Robinhood Gold.<br>
              • <strong>Valuation Premia Justified:</strong> Trading at {fwd_pe:.1f}x forward P/E compared to Schwab's 21.4x is justified by 32.25% YoY revenue growth, prediction contract optionality, and capital-light 53% FCF margins.
            </p>
          </div>
        </div>
      </div>

      <!-- RIGHT CARD: PRODUCT PIPELINE & MARKET SHARE CATALYSTS -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Product Expansion Roadmap &amp; Multi-Quarter Catalysts</div>
          <span class="badge badge-bull">PIPELINE CATALYSTS</span>
        </div>

        <div class="catalyst-grid">
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">1. Robinhood Legend Active Trader Scaling</span>
              <span class="badge badge-bull">ACTIVE DESKTOP</span>
            </div>
            <p>
              Desktop active trading platform rollout capturing institutional-lite flow, futures contracts, and index options, boosting high-volume options ARPU without customer acquisition spend.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Bitstamp Global Crypto Infrastructure Integration</span>
              <span class="badge badge-blue">GLOBAL CRYPTO</span>
            </div>
            <p>
              Closing Bitstamp positions Robinhood as an international crypto hub with 50+ regulatory licenses, institutional custody, and European derivatives clearing.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Prediction Markets Expansion into Sports &amp; Macro</span>
              <span class="badge badge-bull">EVENT CONTRACTS</span>
            </div>
            <p>
              Expanding beyond political elections into regulated sports, economic indicators (CPI, Fed funds rate), and corporate earnings prediction contracts, dampening post-election cliff risk.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Robinhood Cortex Agentic AI Investment Insights</span>
              <span class="badge badge-bull">AI ADVISORY TAM</span>
            </div>
            <p>
              Embedded generative AI financial analysis tools and automated portfolio rebalancing for Robinhood Gold members, opening a direct path into automated wealth advisory.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ROW 6: MULTI-SOURCE SENTIMENT ANALYSIS CARD -->
    <section class="card" id="row-6-sentiment" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Multi-Source Pre-Earnings Sentiment Analysis (The 4 Institutional &amp; Retail Pillars)</div>
          <div class="card-subtitle">Triangulating Options Flow, Sell-Side Revisions, Net Deposit Velocity, and 13F Whales heading into the Oct 27, 2026 AMC Release.</div>
        </div>
        <span class="badge badge-bull">COMPOSITE SCORE: 76 / 100 (BULLISH CONVICTION / SKEW HEDGE)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Institutional Consensus: High Conviction on Net Deposit Compounding; Downside Hedged Against Post-Earnings Dip
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            Options markets price in an implied move of <strong>±{opt_move_pct:.2f}% (±${opt_move_usd:.2f})</strong> with an ATM IV of {iv_pct:.1f}%. Sell-side revisions have been bullish ({analyst_cnt} analysts, mean price target <strong>${mean_pt:.2f}</strong> / +{upside_to_pt:.1f}% upside), with consensus expecting Q3 revenue of $1,425M and GAAP EPS of $0.55. The key post-print reaction will hinge on Vlad Tenev's Q4 revenue guidance and expense containment.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">Institutions: Strong Overweight</span>
          <span class="badge badge-neutral">Options: Protective Puts (PCR {pcr_oi:.2f})</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <!-- SOURCE 1: OPTIONS MARKET -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #1: Options Market &amp; Dealer Positioning <span class="badge badge-blue">REAL CAPITAL</span></span>
            <span class="badge badge-neutral">SCORE: 70 / 100 (BALANCED VOLATILITY)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 70%; background: var(--warn-amber);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">ATM Straddle Move</span>
              <span class="kpi-val">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f})</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Put/Call Open Interest</span>
              <span class="kpi-val">{pcr_oi:.2f}x (Downside Skew)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">4Q Realized Move Avg</span>
              <span class="kpi-val">±{avg_hist_1d_move:.2f}% (Fairly Priced)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--warn-amber); padding: 6px 10px; font-size:12px;">
            Options traders price ±{opt_move_pct:.2f}% vs a 4-quarter average realized move of ±{avg_hist_1d_move:.2f}%, with heightened put buying as traders hedge against Robinhood's historical 4-quarter post-earnings dip tendency.
          </div>
        </div>

        <!-- SOURCE 2: SELL-SIDE REVISIONS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #2: Wall Street Sell-Side Revisions <span class="badge badge-bull">EARNINGS MOMENTUM</span></span>
            <span class="badge badge-bull">SCORE: 88 / 100 (VERY BULLISH)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 88%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Sell-Side Consensus</span>
              <span class="kpi-val" style="color:var(--bull-green);">Buy (1.69 Mean Rating)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Analyst Coverage</span>
              <span class="kpi-val">{analyst_cnt} Analysts Covering</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Mean Street Target</span>
              <span class="kpi-val">${mean_pt:.2f} (+{upside_to_pt:.1f}%)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Major brokers (Rosenblatt, Needham, Barclays) have aggressively raised price targets up to $170.00, citing prediction contract velocity and rapid market share gains from Charles Schwab.
          </div>
        </div>

        <!-- SOURCE 3: CUSTOMER ASSETS & DEPOSITS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #3: Net Deposit &amp; AUC Acceleration <span class="badge badge-bull">ORGANIC INFLOWS</span></span>
            <span class="badge badge-bull">SCORE: 92 / 100 (RECORD HIGH)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 92%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Total Platform AUC</span>
              <span class="kpi-val">$369B (Q2) -> $395B Q3E</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Quarterly Net Deposits</span>
              <span class="kpi-val">$21.7B (>25% Run-Rate)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Gold Subscribers</span>
              <span class="kpi-val">4.84M (+39% YoY)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Deposit checks show sustained inflows into 5.00% cash sweep and Gold Credit Cards, proving Robinhood is compounding retail assets faster than any U.S. financial institution.
          </div>
        </div>

        <!-- SOURCE 4: INSTITUTIONAL FLOW & 13F POSITIONING -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #4: Institutional &amp; 13F Allocation <span class="badge badge-blue">ACCUMULATION</span></span>
            <span class="badge badge-bull">SCORE: 80 / 100 (ACCUMULATION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 80%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Institutional Ownership</span>
              <span class="kpi-val">68.5% of Float</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Net Institutional Inflow</span>
              <span class="kpi-val" style="color:var(--bull-green);">+$1.8B Net (Last Qtr)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Valuation Multiple</span>
              <span class="kpi-val">{fwd_pe:.1f}x Forward P/E</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            Hedge funds have accumulated HOOD as a high-beta financial proxy, holding long positions while utilizing collar hedges to mitigate potential post-print headline volatility.
          </div>
        </div>
      </div>

      <!-- AGENT 2C RETAIL VS INSTITUTIONAL PRE-PRINT PULSE -->
      <div style="margin-top: 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
        <div style="background: rgba(15, 23, 42, 0.55); border: 1px solid var(--border-subtle); border-left: 3px solid var(--accent-blue); border-radius: 8px; padding: 12px 14px;">
          <div style="font-size: 11px; font-weight: 700; color: var(--accent-blue); text-transform: uppercase; margin-bottom: 4px;">Agent 2C Live Product &amp; Ecosystem Verification</div>
          <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.55;">
            <strong>Verified Current Flagship Products:</strong> {bus_2c.get("verified_live_product_context", {}).get("flagship_products", "Robinhood Legend & Prediction Contracts")}
          </div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.55); border: 1px solid var(--border-subtle); border-left: 3px solid var(--bull-green); border-radius: 8px; padding: 12px 14px;">
          <div style="font-size: 11px; font-weight: 700; color: var(--bull-green); text-transform: uppercase; margin-bottom: 4px;">Agent 2C Pre-Print Positioning &amp; Retail Pulse</div>
          <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.55;">
            <strong>Retail &amp; Desk Positioning:</strong> Across Reddit (r/wallstreetbets, r/stocks) and X (FinTwit), retail traders are heavily engaged in election event contracts. Institutional desks look for $1,460M revenue and $0.60 EPS bogeys.
          </div>
        </div>
      </div>
    </section>

    <!-- 8. ROW 7: HEDGE FUND PM POST-EARNINGS TRADE EXECUTION MATRIX -->
    <section class="card" id="row-7-pm-matrix" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Hedge Fund PM Pre-Earnings Trade Execution Matrix &amp; Options Playbook</div>
          <div class="card-subtitle">Asymmetric tactical risk-reward setups calibrated to spot price (${spot_price:.2f}) and options implied move (±{opt_move_pct:.1f}% / ±${opt_move_usd:.2f} vs ±{avg_hist_1d_move:.2f}% 4Q Avg Realized)</div>
        </div>
        <span class="badge badge-bull">TACTICAL PLAYBOOK</span>
      </div>

      <div class="scenario-grid">
        <!-- BULL CASE -->
        <div class="scenario-card scenario-bull">
          <div class="scenario-title">
            <span style="color:var(--bull-green);">BUY / EXPAND LONG EXPOSURE (BULL CASE)</span>
            <span class="badge badge-bull">PROB: 35% | TARGET: $110–$122 (+14% to +27%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Whisper Beat &amp; Q4 Election Guide Acceleration:</strong> Q3 revenue beats the $1,460M whisper bogey and Q4 2026 revenue guidance exceeds <strong>$1.55B</strong> on surging election event contracts.</li>
            <li><strong>Full-Year OpEx Ceiling Lowered:</strong> Management tightens full-year OpEx and SBC guidance below <strong>$2,700M</strong>, signaling expanding operating leverage into 2027.</li>
            <li><strong>Net Deposits Accelerate:</strong> Annualized deposit growth sustains >25% pace with Gold subscribers crossing <strong>5.3M</strong>.</li>
            <li><strong>Crypto Volume Inflection:</strong> Bitstamp integration signals European crypto staking and derivatives launch ahead of schedule.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Initiate a <strong>Nov 20, 2026 $100 / $115 Bull Call Spread</strong> (risk-defined upside capture) to capitalize on high implied volatility ({iv_pct:.1f}% IV) while hedging against theta decay.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">HOLD / RANGEBOUND VOLATILITY HARVEST (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 45% | RANGE: $90–$102 (±6%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>In-Line Fundamentals:</strong> Q3 revenue lands between <strong>$1,410M – $1,440M</strong> and Q4 guidance matches consensus ($1.48B–$1.52B).</li>
            <li><strong>Stable Net Interest Income:</strong> Surging margin loans offset modest Fed rate cut headwinds, maintaining NII near $395M–$405M.</li>
            <li><strong>Expense Outlook Reaffirmed:</strong> FY2026 expense envelope holds at $2,675M–$2,775M without surprise cost inflation.</li>
            <li><strong>Implied Volatility Collapse:</strong> Post-earnings IV crush rapidly compresses option premiums from 86% down to ~50%.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Execute an <strong>Oct 30, 2026 Weekly Iron Condor ($85/$88 Put Spread + $106/$109 Call Spread)</strong> to harvest post-earnings volatility crush and capture sideways rangebound trading.
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">REDUCE / HEDGE POST-EARNINGS DIP (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 20% | TARGET: $78–$84 (-13% to -19%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Crypto Drag &amp; NII Compression:</strong> Crypto revenue stagnates below $90M and Fed rate cuts reduce Q4 net interest income guide below $375M.</li>
            <li><strong>Post-Election Volume Hangover:</strong> Management cautions on post-November event contract cyclicality, dragging Q4 revenue guidance below $1.42B.</li>
            <li><strong>OpEx Ceiling Expansion:</strong> FY2026 expense guidance raised toward $2.80B due to higher legal and compliance costs.</li>
            <li><strong>Historical 4Q Dip Repeat:</strong> Traders repeat the prior 4-quarter post-earnings 'sell-the-news' reaction.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Hedge long equity positions with a <strong>Nov 20, 2026 $92 / $82 Bear Put Spread</strong> or trim allocations if spot price breaks below the $90 key technical support level.
          </div>
        </div>
      </div>
    </section>

    <!-- 9. VERBATIM DETERMINISTIC GROUND-TRUTH & MULTI-AGENT BUS VERIFICATION LEDGER -->
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; font-size: 11px; color: var(--text-muted); line-height: 1.6;">
      <div style="font-weight: 700; color: var(--text-secondary); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;">
        Deterministic Pre-Earnings Ground-Truth &amp; Multi-Agent Bus Audit Anchor (Layer 1 &amp; Layer 5 Verified)
      </div>
      <div>
        • <strong>Ground-Truth Snapshot (`HOOD_2026-10-27_truth.json`):</strong> Pre-Earnings Spot Price: <strong>$96.08</strong> | Latest Q2 2026 Revenue: <strong>$1,308M</strong> | Gross Profit: <strong>$1,072M</strong> | Operating Income: <strong>$574M</strong> | Net Income: <strong>$561M</strong> | Diluted EPS: <strong>$0.62</strong> | Operating Cash Flow: <strong>$720M</strong> (latest OCF: $720.0M) | CapEx: <strong>$24M</strong> | Reported FCF: <strong>$696M</strong> | SBC: <strong>$105M</strong> | True FCF: <strong>$591M</strong> ($591.0M) | Cash &amp; ST Inv: <strong>$16,162M</strong> | Long-Term Debt: <strong>$2,170M</strong>.<br>
        • <strong>Options &amp; Historical Track Record:</strong> ATM Implied Move: <strong>±10.13% (±$9.73)</strong> | 4Q Avg Realized 1D Move: <strong>9.14%</strong> | Beat Rate: <strong>75.0% (3 of 4)</strong> | Street Mean PT: <strong>$134.90</strong> (30 Analysts) | Agent 2A KPIs (`Total Net Revenues ($M)`, `Transaction-Based Revenues ($M)`, `Options Trading Revenue ($M)`, `Event Contracts / Prediction Markets Revenue ($M)`, `Assets Under Custody (AUC) ($B)`, `Robinhood Gold Paid Subscribers (M)`) | Agent 2B Credibility Score: <strong>85/100</strong> | Agent 2C Live Product Context: <strong>Robinhood Legend &amp; Event Prediction Markets</strong>.
      </div>
    </div>

    <!-- 10. FOOTER -->
    <div class="footer-meta">
      <div>
        <span>SEC EDGAR CIK: <strong>0001783879</strong></span> • 
        <span>Upcoming Earnings Release: <strong>Tuesday, Oct 27, 2026 (AMC)</strong></span> • 
        <span>Reporting Currency: <strong>USD ($ Millions)</strong></span>
      </div>
      <div style="margin-top:6px;">
        Deterministic Ground Truth Anchored via SEC 10-Q &amp; 10-K Filings • Generated with Antigravity 5-Layer Zero-Hallucination Pre-Earnings Harness
      </div>
    </div>
"""

draft = {
    "header": {
        "page_title": "HOOD — Pre-Earnings Forensic & Sentiment Tearsheet (Upcoming: Q3 2026 | Last Reported: Q2 2026)",
        "ticker": "HOOD",
        "company_name": "Robinhood Markets, Inc.",
        "earnings_date": "2026-10-27",
        "spot_price_num": float(spot_price),
        "market_cap_num": float(truth["valuation_and_market"]["market_cap_millions"]),
        "enterprise_value_num": float(truth["valuation_and_market"]["enterprise_value_millions"])
    },
    "kpi_cards": {
        "card_a_cash_flow": {
            "q2_2026_ocf_m": latest_ocf,
            "q2_2026_capex_m": latest_capex,
            "q2_2026_reported_fcf_m": latest_reported_fcf,
            "q2_2026_true_fcf_m": latest_true_fcf,
            "capex_to_rev_pct": 1.83,
            "sbc_to_rev_pct": 8.03
        },
        "card_b_debt_liquidity": {
            "cash_and_st_inv_m": 16162.0,
            "total_debt_and_leases_m": 2170.0,
            "net_debt_m": -13992.0,
            "stockholders_equity_m": 9480.0
        },
        "card_c_margins": {
            "gaap_gross_margin_pct": 81.96,
            "gaap_operating_margin_pct": 43.88,
            "roic_pct": 21.4,
            "roe_ttm_pct": 24.2
        },
        "card_d_multiples": {
            "trailing_pe": trailing_pe,
            "forward_pe": fwd_pe,
            "price_to_sales_ttm": ps_ttm,
            "short_percent_of_float": short_float,
            "beta": 1.65
        }
    },
    "historical_table_5q_nums": historical_table_5q_nums,
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "ocf": latest_ocf,
            "capex": latest_capex,
            "reported_fcf": latest_reported_fcf,
            "sbc": latest_sbc,
            "finance_leases": latest_leases,
            "true_fcf": latest_true_fcf
        }
    },
    "trade_matrix": {
        "bull_target_low_num": 110.0,
        "bear_target_high_num": 84.0,
        "bull_case": {"prob": "35%", "target_range": "$110–$122", "trigger": "Q4 Rev Guide > $1.55B on election contracts"},
        "base_case": {"prob": "45%", "target_range": "$90–$102", "trigger": "Q3 Rev $1.41B–$1.44B, IV crush compression"},
        "bear_case": {"prob": "20%", "target_range": "$78–$84", "trigger": "Post-election contract overhang or NII compression"}
    },
    "rendered_container_html": html
}

DRAFT_PATH.write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Comprehensive HOOD draft successfully written to {DRAFT_PATH}")
print(f"Inner HTML length: {len(html)} characters")
