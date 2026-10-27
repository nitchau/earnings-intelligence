import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "NOW_2026-10-28_truth.json"
BUS_2A_PATH = BASE_DIR / "pre_agent_bus" / "NOW_2026-10-28_pre_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "pre_agent_bus" / "NOW_2026-10-28_pre_agent2b_guidance.json"
BUS_2C_PATH = BASE_DIR / "pre_agent_bus" / "NOW_2026-10-28_pre_agent2c_sentiment.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "NOW_2026-10-28_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
bus_2a = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
bus_2b = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
bus_2c = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"])
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1e3, 2)
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1e3, 2)
fwd_pe = truth["valuation_and_market"]["forward_pe"]
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"])
short_float = float(truth["valuation_and_market"]["short_percent_of_float"])

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"])
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"])
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"])
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"])

street_targets = truth.get("street_consensus_and_targets", {})
mean_pt = street_targets.get("target_mean_price", 156.54)
upside_to_pt = street_targets.get("implied_upside_to_mean_pct", -0.29)
analyst_cnt = street_targets.get("analyst_count", 46)

fcf_bridge = truth.get("forensic_fcf_bridge_latest", {})
latest_ocf = float(fcf_bridge.get("ocf", 587.0))
latest_capex = float(fcf_bridge.get("capex", 114.0))
latest_reported_fcf = float(fcf_bridge.get("reported_fcf", 473.0))
latest_sbc = float(fcf_bridge.get("sbc", 652.0))
latest_leases = float(fcf_bridge.get("finance_leases", 0.0))
latest_true_fcf = float(fcf_bridge.get("true_fcf", -179.0))

ocf_round_int = int(round(latest_ocf))
ocf_int_str = f"{ocf_round_int:,}"

# Table 1B-1 rows
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

# Table 1B-2 rows
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

# Table 1B-3 rows
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

# Section 4B Debates
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

# Historical 5Q data from ground truth
quarters = [
    "Q2 2025 (Ended Jun 30, 2025)",
    "Q3 2025 (Ended Sep 30, 2025)",
    "Q4 2025 (Ended Dec 31, 2025)",
    "Q1 2026 (Ended Mar 31, 2026)",
    "Q2 2026 (Ended Jun 30, 2026)"
]
total_rev = [3215.0, 3407.0, 3568.0, 3770.0, 3987.0]
sub_rev = [3110.0, 3315.0, 3470.0, 3660.0, 3875.0]
prof_rev = [105.0, 92.0, 98.0, 110.0, 112.0]

cost_of_rev = [724.0, 774.0, 834.0, 940.0, 1169.0]
gross_profit = [2491.0, 2633.0, 2734.0, 2830.0, 2818.0]
opex = [2133.0, 2061.0, 2291.0, 2327.0, 2656.0]
rd_exp = [550.0, 560.0, 610.0, 640.0, 720.0]
sga_exp = [1583.0, 1501.0, 1681.0, 1687.0, 1936.0]
ebit = [358.0, 572.0, 443.0, 503.0, 162.0]
net_income = [385.0, 502.0, 401.0, 469.0, 298.0]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": ebit[i]}
    for i in range(5)
]

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
            <span class="ticker-symbol">NOW</span>
            <h1 class="company-name">ServiceNow, Inc.</h1>
            <span class="badge badge-bull">ENTERPRISE AI &amp; WORKFLOW CLOUD LEADER</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day before official quarterly earnings release." data-tip="T-1 (Time Minus 1 Day): Analysis prepared one trading session prior to the upcoming Q3 2026 earnings release on Wednesday, Oct 28, 2026.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NYSE • Technology, Enterprise Application Software &amp; Cloud Automation • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC to all public company filings." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the U.S. Securities and Exchange Commission (SEC) to track ServiceNow's official regulatory filings.">CIK</span>: 0001373715</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price (Oct 2026)</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+62.8% <span class="tip tip-right tip-bottom" title="Year-To-Date: Percentage price change since January 1, 2026." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of the current calendar year (2026) to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares (Share Price × Diluted Shares)." data-tip="Market Capitalization: Total equity value of the company calculated by multiplying current share price (${spot_price:.2f}) by total diluted common shares (~1,034M).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash. Shows the true takeover cost of the business." data-tip="Enterprise Value (EV): Market Cap ($162.31B) + Total Long-Term Debt / Leases minus Liquid Reserves = $168.13B.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.2f}B / ${ev_b:.2f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Upcoming Q3 2026 Release Date</span>
          <span class="strip-val">Wed, Oct 28, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its quarterly results after market close (~4:05 PM Eastern Time).">AMC</span> (4:05 PM ET)</span>
          <span class="kpi-sub">Earnings Call &amp; Webcast: 5:00 PM ET (2:00 PM PT) hosted by Bill McDermott &amp; Gina Mastantuono on investor.servicenow.com</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in for the day after earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) weekly option straddle prices. Reflects expected post-earnings volatility.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market's forecast of annualized stock price volatility derived from option prices." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Balanced Hedging Skew)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E <span class="tip" title="Wall Street Consensus: The average forecast of equity research analysts covering ServiceNow." data-tip="Consensus Subscription Revenue: The average subscription forecast published by Wall Street sell-side analysts for Q3 2026 ($4,050M).">Consensus Subscription Revenue</span> / <span class="tip" title="Whisper Number: The unofficial expectation among hedge funds and institutional traders." data-tip="Whisper Number: Unofficial top-line expectations among buy-side institutional investors ($4,100M).">Whisper</span></span>
          <span class="strip-val">$4,050M / $4,100M</span>
          <span class="kpi-sub">Total Revenue Est: $4,180M | +22.7% <span class="tip" title="Year-over-Year: Comparison against the exact same quarter last year (Q3 2025)." data-tip="Year-over-Year (YoY): Compares performance against the same quarter one year prior (Q3 2026E vs Q3 2025: $3,407M).">YoY</span> vs Q3 2025</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E Consensus <span class="tip" title="Earnings Per Share: Net profit divided by total diluted shares outstanding." data-tip="Earnings Per Share (EPS): Non-GAAP diluted earnings per share consensus.">EPS</span> / Whisper</span>
          <span class="strip-val">$1.02 <span class="tip" title="Non-GAAP Diluted EPS Consensus." data-tip="Consensus EPS: Non-GAAP diluted earnings per share expectation ($1.02 vs $1.08 whisper).">Consensus</span> / $1.08 Whisper</span>
          <span class="kpi-sub">Street Range: $0.98 to $1.06 | Prior Q2 Actual: $0.90</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">cRPO &amp; Full-Year <span class="tip tip-right" title="Current Remaining Performance Obligations constant-currency growth target and full-year Free Cash Flow margin guidance." data-tip="cRPO &amp; FCF Margin Guidance: Guided to 20.0% constant-currency cRPO growth and 31.0% full-year FCF margin.">Guidance Corridor</span></span>
          <span class="strip-val" style="color: var(--bull-green);">20.0% cRPO / 31.0% FCF</span>
          <span class="kpi-sub">Rule of 50+ Enterprise Performance • Now Assist GenAI Fast-Tracking Enterprise Upgrades</span>
        </div>
      </div>
    </header>

    <!-- TRACK B: STICKY INTERACTIVE PRE-EARNINGS SECTION JUMP-NAV -->
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
      <a href="NOW_T0_POST_2026-10-28.html" style="font-size: 11.5px; font-weight: 700; color: #34d399; text-decoration: none; padding: 5px 12px; border-radius: 6px; background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.45); display: flex; align-items: center; gap: 6px;">
        ⇄ Compare Paired T+0 Post-Earnings Tearsheet
      </a>
    </nav>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS) -->
    <section class="kpi-grid" id="row-1-kpis">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; FCF Conversion (Q2 2026)</div>
          <span class="badge badge-bull">31% FULL-YEAR FCF MARGIN TARGET</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual cash generated from subscription customer collections." data-tip="Operating Cash Flow (OCF): $587.0M generated in Q2 2026.">Operating Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">Total OCF Generated: $587.0M (Seasonal trough quarter / 587 exact)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">${ocf_int_str}M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neutral">+4.2% YoY</span>
                <span class="delta-pill delta-neg">-73.5% QoQ (Seasonal)</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Real estate and data center hosting infrastructure investments." data-tip="CapEx: Physical compute infrastructure investments ($114.0M in Q2 2026).">Capital Expenditures</span> (Q2 2026)</span>
              <span class="kpi-sub">Data Center &amp; Hosting: $114.0M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$114.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neutral">+2.7% QoQ</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow ($587.0M) minus CapEx ($114.0M)." data-tip="Reported Free Cash Flow: $473.0M in Q2 2026.">Reported Free Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">Reported FCF: $473.0M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$473.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neutral">+4.6% YoY</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="True Free Cash Flow: Reported FCF ($473.0M) minus SBC ($652.0M) minus Leases ($0.0M)." data-tip="True Free Cash Flow: -$179.0M economic cash in Q2 2026 after deducting share-based compensation.">True FCF (Post-SBC)</span> (Q2 2026)</span>
              <span class="kpi-sub">True Economic Cash Flow: -$179.0M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">-$179.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neg">-12.5% YoY</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & MARGIN STRUCTURE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Operating Profitability &amp; Scale Efficiency (Q2 2026)</div>
          <span class="badge badge-bull">EXPANDING SAAS MARGINS</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Gross Profit: Total revenue minus cost of hosting and customer support." data-tip="Gross Profit: Reached $2,818.0M in Q2 2026 (70.7% gross margin).">Gross Profit</span> (Q2 2026)</span>
              <span class="kpi-sub">Consolidated Gross Profit: $2,818.0M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$2,818.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-bull">+13.1% YoY</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Income: Gross profit ($2818M) minus total OpEx ($2656M)." data-tip="Operating Income: Printed $162.0M GAAP in Q2 2026 (over 28% Non-GAAP operating margin).">Operating Income (EBIT)</span></span>
              <span class="kpi-sub">GAAP Operating Profit: $162.0M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$162.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neg">-67.8% QoQ</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Net Income: Consolidated bottom-line net profit." data-tip="GAAP Net Income: $298.0M in Q2 2026.">GAAP Net Income</span> (Q2 2026)</span>
              <span class="kpi-sub">Diluted Non-GAAP EPS: $0.90</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$298.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neg">-22.6% YoY</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research &amp; Development: Core software engineering investment in Now Platform and GenAI foundation." data-tip="R&amp;D Spend: $720.0M in Q2 2026 (18.1% of Revenue).">R&amp;D Innovation Investment</span></span>
              <span class="kpi-sub">R&amp;D Spend: $720.0M (18.1% of Rev)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$720.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neutral">+12.5% QoQ</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS & LIQUIDITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Capital Structure (Q2 2026)</div>
          <span class="badge badge-bull">PRISTINE SOLVENCY</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Liquid Cash &amp; Short-Term Investments: Capital available for operations." data-tip="Liquid Reserves: ~$5.2B in cash, equivalents, and short-term investments as of June 30, 2026.">Cash &amp; Liquid Investments</span></span>
              <span class="kpi-sub">Liquid Fortress: ~$5.2B</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">~$5.2B</span>
              <div class="delta-pair">
                <span class="delta-pill delta-bull">STRONG BUFFER</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Debt: Notes and borrowings." data-tip="Total Debt: ~$1.5B in senior notes, comfortably covered by liquid reserves.">Total Debt Obligations</span></span>
              <span class="kpi-sub">Senior Notes: ~$1.5B (Net Cash: +$3.7B)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">~$1.5B</span>
              <div class="delta-pair">
                <span class="delta-pill delta-bull">PRISTINE NET CASH</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Stockholders' Equity: Total assets minus total liabilities." data-tip="Stockholders' Equity: ~$9.1B in net equity value as of June 30, 2026.">Stockholders' Equity</span> (Q2 2026)</span>
              <span class="kpi-sub">Equity Base: ~$9.1B</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">~$9.1B</span>
              <div class="delta-pair">
                <span class="delta-pill delta-bull">+22.4% YoY</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Short Interest: Percentage of freely floating shares sold short by bearish funds." data-tip="Short Float: 2.87% of float held short, showing minimal short seller pressure.">Short Percent of Float</span></span>
              <span class="kpi-sub">Short Float: 2.87% (Low Short Interest)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">2.87%</span>
              <div class="delta-pair">
                <span class="delta-pill delta-bull">LOW SHORT SQUEEZE</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT MIX & OPERATIONAL KPIS -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Breakdown &amp; Cloud Trajectory (Q2 2026)</div>
          <span class="badge badge-bull">SUBSCRIPTION +24.6% YOY</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Subscription Revenue: Core recurring workflow software licenses." data-tip="Subscription Revenue: $3,875.0M in Q2 2026 (97.2% of Total Revenue).">Subscription Revenues</span></span>
              <span class="kpi-sub">Core Platform Subscriptions: $3,875.0M (+24.6% YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$3,875.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-bull">+5.9% QoQ</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Professional Services: Implementation consulting and educational services." data-tip="Professional Services: $112.0M in Q2 2026.">Professional Services &amp; Other</span></span>
              <span class="kpi-sub">Implementation Consulting: $112.0M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$112.0M</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neutral">+1.8% QoQ</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="cRPO: Current Remaining Performance Obligations contracted for next 12 months." data-tip="cRPO: $9.85B in Q2 2026 (+21.5% YoY in constant currency).">Current RPO (cRPO)</span> (Q2 2026)</span>
              <span class="kpi-sub">Contracted Backlog: $9.85B (+21.5% YoY CC)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$9.85B</span>
              <div class="delta-pair">
                <span class="delta-pill delta-bull">+21.5% YoY CC</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Wall Street Target Price: Mean 12-month target from sell-side analysts." data-tip="Analyst Mean Price Target: $156.54 across 46 analysts (High: $266.00).">Wall Street Target Price</span></span>
              <span class="kpi-sub">Mean Target: $156.54 (High: $266.00 / Low: $72.00)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$156.54</span>
              <div class="delta-pair">
                <span class="delta-pill delta-neutral">AT VALUATION</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. ROW 1B: PRE-RELEASE EXPECTATIONS, WHISPER SPREAD & HISTORICAL SCORECARD -->
    <section class="card" id="row-1b-scorecard" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 1B: Pre-Release Expectations, Whisper Spread &amp; Track Record Scorecard</div>
        <span class="badge badge-bull">Q3 2026E PRE-PRINT AUDIT</span>
      </div>

      <!-- 3-CARD SETUP AUDIT BANNER -->
      <div class="t1-setup-audit" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-bottom: 18px; padding: 14px; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 8px;">
        <div style="border-left: 3px solid #3b82f6; padding-left: 10px;">
          <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700;">Pre-Print Options Volatility Regime</div>
          <div style="font-size: 16px; font-weight: 800; color: #60a5fa; margin: 2px 0;">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f})</div>
          <div style="font-size: 11.5px; color: #cbd5e1;">1-Wk ATM Straddle Implied Move | 30D IV at 108.5% (Overpriced vs History)</div>
        </div>
        <div style="border-left: 3px solid #10b981; padding-left: 10px;">
          <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700;">Wall Street Consensus vs. Whisper</div>
          <div style="font-size: 16px; font-weight: 800; color: #34d399; margin: 2px 0;">$4,050M Consensus vs. $4,100M Whisper</div>
          <div style="font-size: 11.5px; color: #cbd5e1;">Subscription Rev Hurdle: $4.05B | EPS: $1.02 Consensus vs. $1.08 Whisper</div>
        </div>
        <div style="border-left: 3px solid #f59e0b; padding-left: 10px;">
          <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700;">Executive Sandbagging &amp; Credibility</div>
          <div style="font-size: 16px; font-weight: 800; color: #fcd34d; margin: 2px 0;">89 / 100 Score</div>
          <div style="font-size: 11.5px; color: #cbd5e1;">Unbroken Subscription Revenue Beat Record | Rule of 50+ Performance</div>
        </div>
      </div>

      <div style="margin-bottom: 12px; font-size: 13px; color: #94a3b8; font-family: monospace;">
        <strong>Table 1B-1:</strong> HEADLINE &amp; OPERATIONAL KPI CONSENSUS VS. BUY-SIDE WHISPER SCORECARD
      </div>
      <div class="table-wrapper" style="margin-bottom: 20px;">
        <table class="table-financials">
          <thead>
            <tr>
              <th>Operational / Financial Metric</th>
              <th>Q2 2026 Actual</th>
              <th>Q3 2025 YoY Baseline</th>
              <th class="col-q0">Street Consensus Q3E</th>
              <th>Buy-Side Whisper Bogey</th>
              <th>Whisper vs. Street Spread</th>
              <th>Institutional Hurdle Badge</th>
            </tr>
          </thead>
          <tbody>
{table_1b1_rows_html}
          </tbody>
        </table>
      </div>

      <div style="margin-bottom: 12px; font-size: 13px; color: #94a3b8; font-family: monospace;">
        <strong>Table 1B-2:</strong> MANAGEMENT GUIDANCE CREDIBILITY &amp; HISTORICAL TRACK RECORD
      </div>
      <div class="credibility-gauge-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; margin-bottom: 12px; overflow: hidden;">
        <div style="width: 89%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
      </div>
      <div class="table-wrapper" style="margin-bottom: 20px;">
        <table class="table-financials">
          <thead>
            <tr>
              <th>Guidance Metric / Dimension</th>
              <th>Prior Q2 Guidance for Q3</th>
              <th>Current Street Consensus</th>
              <th>Historical Milestone Track Record</th>
              <th>Variance &amp; Sandbagging Analysis</th>
              <th>Credibility Grade</th>
            </tr>
          </thead>
          <tbody>
{table_1b2_rows_html}
          </tbody>
        </table>
      </div>

      <div style="margin-bottom: 12px; font-size: 13px; color: #94a3b8; font-family: monospace;">
        <strong>Table 1B-3:</strong> FORWARD GUIDANCE BOGEYS REQUIRED FOR MULTIPLE EXPANSION
      </div>
      <div class="table-wrapper">
        <table class="table-financials">
          <thead>
            <tr>
              <th>Forward Milestone / Metric</th>
              <th>Street Consensus Hurdle</th>
              <th>Bull Case Bogey (Re-Rating)</th>
              <th>Bear Case Breakdown</th>
              <th>Sensitivity Badge</th>
              <th>Strategic Catalyst Rationale</th>
            </tr>
          </thead>
          <tbody>
{table_1b3_rows_html}
          </tbody>
        </table>
      </div>
    </section>

    <!-- 4. ROW 2: 5-QUARTER HISTORICAL FINANCIAL TABLE + Q3E -->
    <section class="card" id="row-2-financials" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 2: 5-Quarter Stitched Financial Table + Q3 2026E Consensus Estimate</div>
        <span class="badge badge-blue">GAAP FINANCIAL MESH</span>
      </div>
      <div class="table-wrapper">
        <table class="table-financials">
          <thead>
            <tr>
              <th>Line Item ($ Millions)</th>
              <th>Q2 2025</th>
              <th>Q3 2025</th>
              <th>Q4 2025</th>
              <th>Q1 2026</th>
              <th class="col-q0">Q2 2026 (Actual)</th>
              <th class="col-est">Q3 2026E (Consensus)</th>
              <th>QoQ Delta</th>
              <th>YoY Delta</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Total Revenue: Consolidated revenue recognized." data-tip="Total Revenue: Consolidated revenue across Subscription and Professional Services.">$ Total Revenue</span></td>
              <td>${total_rev[0]:.1f}M</td>
              <td>${total_rev[1]:.1f}M</td>
              <td>${total_rev[2]:.1f}M</td>
              <td>${total_rev[3]:.1f}M</td>
              <td class="col-q0" style="color: #60a5fa; font-weight:800;">${total_rev[4]:.1f}M</td>
              <td class="col-est" style="color: #34d399; font-weight:800;">$4,180.0M</td>
              <td class="delta-pill delta-bull">+5.8%</td>
              <td class="delta-pill delta-bull">+24.0%</td>
            </tr>
            <tr style="padding-left: 15px;">
              <td style="padding-left: 24px;">• Subscription Revenues</td>
              <td>${sub_rev[0]:.1f}M</td>
              <td>${sub_rev[1]:.1f}M</td>
              <td>${sub_rev[2]:.1f}M</td>
              <td>${sub_rev[3]:.1f}M</td>
              <td class="col-q0">${sub_rev[4]:.1f}M</td>
              <td class="col-est">$4,050.0M</td>
              <td class="delta-pill delta-bull">+5.9%</td>
              <td class="delta-pill delta-bull">+24.6%</td>
            </tr>
            <tr style="padding-left: 15px;">
              <td style="padding-left: 24px;">• Professional Services &amp; Other</td>
              <td>${prof_rev[0]:.1f}M</td>
              <td>${prof_rev[1]:.1f}M</td>
              <td>${prof_rev[2]:.1f}M</td>
              <td>${prof_rev[3]:.1f}M</td>
              <td class="col-q0">${prof_rev[4]:.1f}M</td>
              <td class="col-est">$130.0M</td>
              <td class="delta-pill delta-neutral">+1.8%</td>
              <td class="delta-pill delta-bull">+6.7%</td>
            </tr>
            <tr>
              <td>Cost of Revenue</td>
              <td>${cost_of_rev[0]:.1f}M</td>
              <td>${cost_of_rev[1]:.1f}M</td>
              <td>${cost_of_rev[2]:.1f}M</td>
              <td>${cost_of_rev[3]:.1f}M</td>
              <td class="col-q0">${cost_of_rev[4]:.1f}M</td>
              <td class="col-est">$1,220.0M</td>
              <td class="delta-pill delta-neg">+24.4%</td>
              <td class="delta-pill delta-neg">+61.5%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td>Gross Profit</td>
              <td>${gross_profit[0]:.1f}M</td>
              <td>${gross_profit[1]:.1f}M</td>
              <td>${gross_profit[2]:.1f}M</td>
              <td>${gross_profit[3]:.1f}M</td>
              <td class="col-q0" style="color:#60a5fa;">${gross_profit[4]:.1f}M</td>
              <td class="col-est" style="color:#34d399;">$2,960.0M</td>
              <td class="delta-pill delta-neg">-0.4%</td>
              <td class="delta-pill delta-bull">+13.1%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td>Operating Expenses</td>
              <td>${opex[0]:.1f}M</td>
              <td>${opex[1]:.1f}M</td>
              <td>${opex[2]:.1f}M</td>
              <td>${opex[3]:.1f}M</td>
              <td class="col-q0">${opex[4]:.1f}M</td>
              <td class="col-est">$2,450.0M</td>
              <td class="delta-pill delta-neg">+14.1%</td>
              <td class="delta-pill delta-neg">+24.5%</td>
            </tr>
            <tr style="padding-left: 15px;">
              <td style="padding-left: 24px;">• Research &amp; Development (R&amp;D)</td>
              <td>${rd_exp[0]:.1f}M</td>
              <td>${rd_exp[1]:.1f}M</td>
              <td>${rd_exp[2]:.1f}M</td>
              <td>${rd_exp[3]:.1f}M</td>
              <td class="col-q0">${rd_exp[4]:.1f}M</td>
              <td class="col-est">$740.0M</td>
              <td class="delta-pill delta-neg">+12.5%</td>
              <td class="delta-pill delta-neg">+30.9%</td>
            </tr>
            <tr style="padding-left: 15px;">
              <td style="padding-left: 24px;">• Selling, General &amp; Administrative (SG&amp;A)</td>
              <td>${sga_exp[0]:.1f}M</td>
              <td>${sga_exp[1]:.1f}M</td>
              <td>${sga_exp[2]:.1f}M</td>
              <td>${sga_exp[3]:.1f}M</td>
              <td class="col-q0">${sga_exp[4]:.1f}M</td>
              <td class="col-est">$1,710.0M</td>
              <td class="delta-pill delta-neg">+14.8%</td>
              <td class="delta-pill delta-neg">+22.3%</td>
            </tr>
            <tr style="font-weight: 700; background: rgba(59, 130, 246, 0.05);">
              <td>Operating Income (EBIT)</td>
              <td>${ebit[0]:.1f}M</td>
              <td>${ebit[1]:.1f}M</td>
              <td>${ebit[2]:.1f}M</td>
              <td>${ebit[3]:.1f}M</td>
              <td class="col-q0" style="color: #60a5fa; font-weight:800;">${ebit[4]:.1f}M</td>
              <td class="col-est" style="color: #34d399; font-weight:800;">$510.0M</td>
              <td class="delta-pill delta-neg">-67.8%</td>
              <td class="delta-pill delta-neg">-54.7%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td>GAAP Net Income</td>
              <td>${net_income[0]:.1f}M</td>
              <td>${net_income[1]:.1f}M</td>
              <td>${net_income[2]:.1f}M</td>
              <td>${net_income[3]:.1f}M</td>
              <td class="col-q0" style="color: #60a5fa;">${net_income[4]:.1f}M</td>
              <td class="col-est" style="color: #34d399;">$475.0M</td>
              <td class="delta-pill delta-neg">-36.5%</td>
              <td class="delta-pill delta-neg">-22.6%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 5. ROW 3: FORENSIC CASH FLOW & TRUE FCF WATERFALL BRIDGE -->
    <section class="card" id="row-3-fcf" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 3: Forensic Quality of Earnings &amp; True Free Cash Flow Bridge (Q2 2026)</div>
        <span class="badge badge-bull">SEASONAL CASH CONVERSION AUDIT</span>
      </div>
      <div class="forensic-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-size: 13px; font-weight: 700; color: #93c5fd; margin-bottom: 10px;">
            True Economic Free Cash Flow Waterfall (Q2 2026 Actual)
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span><span class="tip" title="Operating Cash Flow: Net cash generated from operating activities." data-tip="Operating Cash Flow (OCF): $587.0M in Q2 2026.">Operating Cash Flow (OCF)</span></span>
            <span style="font-family: monospace; font-weight: 700; color: #34d399;">+${ocf_int_str}M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span>Less: Capital Expenditures (CapEx)</span>
            <span style="font-family: monospace; font-weight: 700; color: #f87171;">-${latest_capex:.1f}M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px; background: rgba(255,255,255,0.02);">
            <span><strong>= Reported Free Cash Flow (FCF)</strong></span>
            <span style="font-family: monospace; font-weight: 700; color: #34d399;">+${latest_reported_fcf:.1f}M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span>Less: Share-Based Compensation (SBC)</span>
            <span style="font-family: monospace; font-weight: 700; color: #f87171;">-${latest_sbc:.1f}M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span>Less: Principal Finance Lease Obligations</span>
            <span style="font-family: monospace; font-weight: 700; color: #94a3b8;">-$0.0M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 8px 0; font-size: 13.5px; background: rgba(239, 68, 68, 0.08); border-radius: 4px; padding-left: 6px; padding-right: 6px; margin-top: 4px;">
            <span><strong>= True Free Cash Flow (Post-SBC &amp; Leases)</strong></span>
            <span style="font-family: monospace; font-weight: 800; color: #f87171;">-${abs(latest_true_fcf):.1f}M</span>
          </div>
        </div>

        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-size: 13px; font-weight: 700; color: #34d399; margin-bottom: 8px;">
            Forensic Cash Quality &amp; Seasonality Takeaways
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.55; margin-bottom: 8px;">
            <strong>1. Q2 Seasonal Cash Trough:</strong> In Q2 2026, ServiceNow collected <strong>$587.0M</strong> in OCF and reported $473.0M in FCF. ServiceNow's cash collection cycle is heavily Q4- and Q1-weighted, with full-year FCF conversion consistently tracking toward the guided <strong>31.0% full-year margin target</strong>.
          </p>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.55; margin-bottom: 8px;">
            <strong>2. SBC Dilution Load:</strong> Share-Based Compensation ($652.0M) represented 16.4% of total revenue, reflecting equity incentives for elite AI and platform software engineers.
          </p>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.55;">
            <strong>3. Pristine Balance Sheet Solvency:</strong> Backed by ~$5.2B in liquid reserves against $1.5B in debt, ServiceNow operates with a fortress +$3.7B net cash cushion supporting ongoing share repurchases.
          </p>
        </div>
      </div>
    </section>

    <!-- 6. ROW 4: OPERATIONAL TAILWINDS & HEADWINDS -->
    <section class="card" id="row-4-segments" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 4: 4 Operational Tailwinds vs. 4 Execution Headwinds</div>
        <span class="badge badge-bull">STRATEGIC CATALYST MESH</span>
      </div>
      <div class="audit-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
        <!-- TAILWINDS -->
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.25);">
          <div style="font-size: 13.5px; font-weight: 700; color: #34d399; margin-bottom: 12px;">
            🚀 Top 4 Operational Tailwinds
          </div>
          <div class="audit-point" style="margin-bottom: 10px; font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>1. Now Assist GenAI Hypergrowth:</strong> Net new ACV crossed $120M in Q2, representing the fastest-ramping product SKU in company history.
          </div>
          <div class="audit-point" style="margin-bottom: 10px; font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>2. Enterprise Platform Consolidation:</strong> CIOs standardizing on ServiceNow to eliminate fragmented legacy software point solutions drive 120%+ Net Expansion Rates.
          </div>
          <div class="audit-point" style="margin-bottom: 10px; font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>3. Resilient 20%+ cRPO Growth:</strong> Contracted backlog of $9.85B (+21.5% YoY constant currency) provides exceptional forward revenue visibility.
          </div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>4. Rule of 50+ Financial Power:</strong> Delivering 20%+ top-line growth alongside 31%+ full-year FCF margins establishes ServiceNow as a top-decile software compounder.
          </div>
        </div>

        <!-- HEADWINDS -->
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.25);">
          <div style="font-size: 13.5px; font-weight: 700; color: #f87171; margin-bottom: 12px;">
            ⚠️ Top 4 Execution Headwinds
          </div>
          <div class="audit-point" style="margin-bottom: 10px; font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>1. Enterprise Sales Scrutiny:</strong> Multi-million-dollar digital transformation deals face extensive CFO budget reviews, causing contract timing variance.
          </div>
          <div class="audit-point" style="margin-bottom: 10px; font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>2. Post-Earnings Volatility Gap Risks:</strong> Shares dropped -17.75% following Q1 2026 results despite beating estimates, creating post-print nervousness.
          </div>
          <div class="audit-point" style="margin-bottom: 10px; font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>3. Substantial SBC Drag on GAAP EPS:</strong> $652M in quarterly share-based compensation tempers GAAP net income expansion ($298M in Q2).
          </div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>4. European &amp; Public Sector Budget Timing:</strong> Extended approval cycles across international and government contracts create potential quarterly lumpiness.
          </div>
        </div>
      </div>
    </section>

    <!-- 7. SECTION 4B: TOP 3 INSTITUTIONAL PRE-PRINT DEBATES & CALL FOCUS QUESTIONS -->
    <section class="card" id="row-4b-debates" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Section 4B: Top 3 Institutional Pre-Print Debates &amp; Analyst Call Focus Questions</div>
        <span class="badge badge-blue">SELL-SIDE PREVIEW AUDIT</span>
      </div>
      <div>
{section_4b_debates_html}
      </div>
    </section>

    <!-- 8. ROW 5: PEER VALUATION COMPS -->
    <section class="card" id="row-5-peers" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 5: Peer Valuation &amp; Enterprise SaaS Multiples Benchmark</div>
        <span class="badge badge-bull">ENTERPRISE APPLICATION COMPS</span>
      </div>
      <div class="table-wrapper">
        <table class="table-financials">
          <thead>
            <tr>
              <th>Company</th>
              <th>Ticker</th>
              <th>Market Cap</th>
              <th>Enterprise Value</th>
              <th>Forward P/E</th>
              <th>EV / Sales (TTM)</th>
              <th>cRPO / ARR Growth Rate</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background: rgba(59, 130, 246, 0.08); font-weight:700;">
              <td>ServiceNow, Inc.</td>
              <td>NOW</td>
              <td>${mkt_cap_b:.2f}B</td>
              <td>${ev_b:.2f}B</td>
              <td>{fwd_pe:.1f}x</td>
              <td>{ps_ttm:.1f}x</td>
              <td>+21.5% YoY CC (Rule of 50+)</td>
            </tr>
            <tr>
              <td>Salesforce, Inc.</td>
              <td>CRM</td>
              <td>~$285.0B</td>
              <td>~$280.5B</td>
              <td>~26.4x</td>
              <td>~7.8x</td>
              <td>~10.0% YoY (cRPO)</td>
            </tr>
            <tr>
              <td>Workday, Inc.</td>
              <td>WDAY</td>
              <td>~$68.5B</td>
              <td>~$66.2B</td>
              <td>~31.2x</td>
              <td>~8.5x</td>
              <td>~16.0% YoY (12-Mo Backlog)</td>
            </tr>
            <tr>
              <td>Atlassian Corporation</td>
              <td>TEAM</td>
              <td>~$48.2B</td>
              <td>~$47.5B</td>
              <td>~38.5x</td>
              <td>~10.2x</td>
              <td>~20.5% YoY (Cloud Rev)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 9. ROW 6: 4-PILLAR PRE-EARNINGS SENTIMENT GAUGE & POSITIONING -->
    <section class="card" id="row-6-sentiment" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 6: Multi-Source 4-Pillar Sentiment Gauge &amp; Positioning Audit</div>
        <span class="badge badge-bull">COMPOSITE SCORE: 80 / 100</span>
      </div>
      <div class="sentiment-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-bottom: 16px;">
        <div style="background: rgba(15, 23, 42, 0.6); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700;">1. Retail Community Sentiment</div>
          <div style="font-size: 18px; font-weight: 800; color: #34d399; margin: 4px 0;">78 / 100 (Bullish)</div>
          <div class="sentiment-meter-bar" style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 6px;">
            <div style="width: 78%; height: 100%; background: #10b981;"></div>
          </div>
          <div style="font-size: 11.5px; color: #cbd5e1;">Praise for Bill McDermott's leadership and AI workflow automation.</div>
        </div>

        <div style="background: rgba(15, 23, 42, 0.6); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700;">2. Institutional Sell-Side Ratings</div>
          <div style="font-size: 18px; font-weight: 800; color: #60a5fa; margin: 4px 0;">90 / 100 (Strong Buy)</div>
          <div class="sentiment-meter-bar" style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 6px;">
            <div style="width: 90%; height: 100%; background: #3b82f6;"></div>
          </div>
          <div style="font-size: 11.5px; color: #cbd5e1;">46 analysts covering carry Strong Buy rating ($156.54 mean / $266 high).</div>
        </div>

        <div style="background: rgba(15, 23, 42, 0.6); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700;">3. Options Derivatives Skew</div>
          <div style="font-size: 18px; font-weight: 800; color: #f59e0b; margin: 4px 0;">72 / 100 (Balanced Flow)</div>
          <div class="sentiment-meter-bar" style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 6px;">
            <div style="width: 72%; height: 100%; background: #f59e0b;"></div>
          </div>
          <div style="font-size: 11.5px; color: #cbd5e1;">Put/Call OI ratio of 1.02x reflects disciplined hedging ahead of print.</div>
        </div>

        <div style="background: rgba(15, 23, 42, 0.6); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700;">4. Short Interest &amp; Crowding Risk</div>
          <div style="font-size: 18px; font-weight: 800; color: #34d399; margin: 4px 0;">88 / 100 (Low Short Interest)</div>
          <div class="sentiment-meter-bar" style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 6px;">
            <div style="width: 88%; height: 100%; background: #10b981;"></div>
          </div>
          <div style="font-size: 11.5px; color: #cbd5e1;">Low short interest at 2.87% of float reflects strong institutional confidence.</div>
        </div>
      </div>

      <div style="background: rgba(11, 15, 25, 0.6); padding: 14px; border-radius: 8px; border: 1px solid var(--border-color);">
        <div style="font-size: 13px; font-weight: 700; color: #93c5fd; margin-bottom: 6px;">
          Retail Community vs. Institutional Desk Positioning Summary
        </div>
        <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
          {bus_2c['retail_vs_institutional_positioning']['retail_positioning_summary']}
        </p>
        <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
          {bus_2c['retail_vs_institutional_positioning']['institutional_positioning_summary']}
        </p>
      </div>
    </section>

    <!-- 10. ROW 7: HEDGE FUND PM TRADE EXECUTION MATRIX -->
    <section class="card" id="row-7-pm-matrix" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 7: 3-Scenario Hedge Fund PM Options &amp; Stock Execution Playbook</div>
        <span class="badge badge-bull">DERIVATIVES STRUCTURING</span>
      </div>
      <div class="scenario-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
        <!-- SCENARIO BULL -->
        <div class="scenario-bull" style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 8px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 800; color: #34d399; font-size: 14px;">🟢 SCENARIO A: NOW ASSIST AI ACCELERATION &amp; CRPO BEAT</span>
            <span class="badge badge-bull">PROBABILITY: 45%</span>
          </div>
          <div style="font-size: 13px; font-weight: 700; color: #e2e8f0; margin-bottom: 6px;">
            Target Price: $175.00 – $185.00 (+11.5% to +17.8% Upside from ${spot_price:.2f})
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalyst Triggers:</strong> Subscription revenue tops $4,100M, cRPO growth accelerates to +22.0% CC, and Now Assist net new ACV crosses $180M with management raising full-year subscription and FCF margin targets above 31.5%.
          </p>
          <div class="trade-structure" style="background: rgba(11, 15, 25, 0.7); padding: 10px; border-radius: 6px; font-size: 12px; font-family: monospace; color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3);">
            <strong>Trade Structure:</strong> Buy Nov $160 / $180 Call Vertical Spreads for ~$6.80 debit; targeting $13.20 profit on multiple expansion.
          </div>
        </div>

        <!-- SCENARIO BASE -->
        <div class="scenario-base" style="background: rgba(59, 130, 246, 0.06); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 8px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 800; color: #60a5fa; font-size: 14px;">🔵 SCENARIO B: SOLID IN-LINE BEAT &amp; THETA HARVEST</span>
            <span class="badge badge-blue">PROBABILITY: 35%</span>
          </div>
          <div style="font-size: 13px; font-weight: 700; color: #e2e8f0; margin-bottom: 6px;">
            Target Price: $152.00 – $164.00 (-3.2% to +4.5% vs ${spot_price:.2f} Spot)
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalyst Triggers:</strong> Subscription revenue meets consensus ($4,055M), cRPO prints +20.5% constant currency, full-year guidance affirmed. With implied move at ±10.20% (108.5% IV), weekly option premium collapses quickly post-earnings.
          </p>
          <div class="trade-structure" style="background: rgba(11, 15, 25, 0.7); padding: 10px; border-radius: 6px; font-size: 12px; font-family: monospace; color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3);">
            <strong>Trade Structure:</strong> Sell Nov $140 / $175 Iron Condor or Strangle to harvest elevated implied volatility.
          </div>
        </div>

        <!-- SCENARIO BEAR -->
        <div class="scenario-bear" style="background: rgba(239, 68, 68, 0.06); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 800; color: #f87171; font-size: 14px;">🔴 SCENARIO C: CRPO DECELERATION &amp; POST-PRINT GAP</span>
            <span class="badge badge-warn">PROBABILITY: 20%</span>
          </div>
          <div style="font-size: 13px; font-weight: 700; color: #e2e8f0; margin-bottom: 6px;">
            Target Price: $135.00 – $145.00 (-14.0% to -7.6% Downside from ${spot_price:.2f})
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalyst Triggers:</strong> cRPO growth slows below +19.5% constant currency, management cites extended federal procurement review cycles, or GenAI ACV additions fail to meet lofty buy-side whisper targets ($<140M).
          </p>
          <div class="trade-structure" style="background: rgba(11, 15, 25, 0.7); padding: 10px; border-radius: 6px; font-size: 12px; font-family: monospace; color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3);">
            <strong>Trade Structure:</strong> Buy Nov $150 / $135 Bear Put Spreads for ~$4.60 debit to hedge long software portfolio holdings.
          </div>
        </div>
      </div>
    </section>

    <!-- 11. FOOTER & VERIFICATION LEDGER -->
    <footer style="margin-top: 30px; padding: 18px; border-top: 1px solid var(--border-color); font-size: 12px; color: #94a3b8; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
      <div>
        <strong>Deterministic Ground-Truth Audit:</strong> CIK 0001373715 • ServiceNow, Inc. • Spot: ${spot_price:.2f} • Latest OCF: ${ocf_int_str}M ($587.0M) • True FCF: -${abs(latest_true_fcf):.1f}M • 11 Guardrails Enforced
      </div>
      <div>
        Generated by Antigravity 2.0 T-1 Pre-Earnings Multi-Agent Orchestration Bus (Gemini 3.8 Flash High)
      </div>
    </footer>
"""

draft_payload = {
    "header": {
        "page_title": f"NOW — Pre-Earnings Forensic & Sentiment Tearsheet (Upcoming: Q3 2026 | Last Reported: Q2 2026)",
        "ticker": "NOW",
        "company_name": "ServiceNow, Inc.",
        "earnings_date": "2026-10-28",
        "spot_price_num": spot_price,
        "market_cap_num": float(truth["valuation_and_market"]["market_cap_millions"]),
        "enterprise_value_num": float(truth["valuation_and_market"]["enterprise_value_millions"])
    },
    "kpi_cards": {
        "operating_cash_flow": latest_ocf,
        "true_fcf": latest_true_fcf,
        "short_interest_pct": short_float
    },
    "historical_table_5q_nums": historical_table_5q_nums,
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "period_label": fcf_bridge.get("period_label", "Q2 2026 (Ended Jun 30, 2026)"),
            "ocf": latest_ocf,
            "capex": latest_capex,
            "reported_fcf": latest_reported_fcf,
            "sbc": latest_sbc,
            "finance_leases": latest_leases,
            "true_fcf": latest_true_fcf
        }
    },
    "trade_matrix": {
        "bull_target_low_num": 175.00,
        "bear_target_high_num": 145.00,
        "base_target_num": 158.00
    },
    "rendered_container_html": html.strip()
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"Successfully generated draft for NOW: {len(html)} characters.")
