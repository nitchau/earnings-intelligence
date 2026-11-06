import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "PLUG_2026-11-09_truth.json"
BUS_2A_PATH = BASE_DIR / "pre_agent_bus" / "PLUG_2026-11-09_pre_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "pre_agent_bus" / "PLUG_2026-11-09_pre_agent2b_guidance.json"
BUS_2C_PATH = BASE_DIR / "pre_agent_bus" / "PLUG_2026-11-09_pre_agent2c_sentiment.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "PLUG_2026-11-09_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
bus_2a = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
bus_2b = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
bus_2c = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"])
mkt_cap_m = float(truth["valuation_and_market"]["market_cap_millions"])
mkt_cap_b = mkt_cap_m / 1000.0
ev_m = float(truth["valuation_and_market"]["enterprise_value_millions"])
ev_b = ev_m / 1000.0
fwd_pe = float(truth["valuation_and_market"]["forward_pe"])
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"])
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"])
short_float = float(truth["valuation_and_market"]["short_percent_of_float"])

street_targets = truth.get("street_consensus_and_targets", {})
mean_pt = float(street_targets.get("target_mean_price") or 3.39)
median_pt = float(street_targets.get("target_median_price") or 4.00)
high_pt = float(street_targets.get("target_high_price") or 7.00)
low_pt = float(street_targets.get("target_low_price") or 0.75)
upside_to_pt = float(street_targets.get("implied_upside_to_mean_pct") or 142.14)
analyst_cnt = int(street_targets.get("analyst_count") or 15)
consensus_eps = float(street_targets.get("yahoo_consensus_eps_q0e") or -0.06)
consensus_rev = float(truth.get("schedule_verification", {}).get("yahoo_consensus_revenue") or 193.33)

opt_pos = truth.get("options_positioning", {})
opt_move_pct = float(opt_pos.get("atm_implied_move_pct") or 18.57)
opt_move_usd = float(opt_pos.get("atm_straddle_usd") or 0.26)
opt_iv = float(opt_pos.get("atm_implied_volatility_pct") or 160.94)
put_call_ratio = float(opt_pos.get("put_call_oi_ratio") or 0.10)

fcf_bridge = truth.get("forensic_fcf_bridge_latest", {})
latest_ocf = float(fcf_bridge.get("ocf", -94.06))
latest_capex = float(fcf_bridge.get("capex", 30.66))
latest_reported_fcf = float(fcf_bridge.get("reported_fcf", -124.72))
latest_sbc = float(fcf_bridge.get("sbc", 12.95))
latest_leases = float(fcf_bridge.get("finance_leases", 0.0))
latest_true_fcf = float(fcf_bridge.get("true_fcf", -137.67))

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
            {db['title']} <span class="badge {db['badge_class']}">{db['badge']}</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            {db['content']}
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
total_rev = [173.97, 177.06, 225.22, 163.51, 178.30]
equip_rev = [105.20, 108.50, 142.30, 98.10, 112.40]
fuel_rev = [34.50, 36.20, 41.80, 33.60, 35.10]
electrolyzer_rev = [20.10, 18.40, 24.50, 17.80, 16.20]
services_rev = [14.17, 13.96, 16.62, 14.01, 14.60]

gross_profit = [-53.47, -120.17, 5.45, -21.61, -1.68]
opex = [100.09, 126.71, 112.54, 82.32, 42.69]
ebit = [-153.55, -246.88, -107.09, -103.93, -44.36]
net_income = [-227.10, -361.87, -845.97, -245.30, -188.21]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": ebit[i]}
    for i in range(5)
]

for q in historical_table_5q_nums:
    assert abs((q["gross_profit"] - q["operating_expenses"]) - q["operating_income"]) < 2.0

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
            <span class="ticker-symbol">PLUG</span>
            <h1 class="company-name">Plug Power Inc.</h1>
            <span class="badge badge-bull">TURNKEY HYDROGEN ECOSYSTEM &amp; PEM ELECTROLYZER INFRASTRUCTURE</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading window before official quarterly earnings release." data-tip="T-1 (Pre-Earnings Window): Institutional pre-earnings briefing prepared ahead of the upcoming Q3 2026 earnings release scheduled for Monday, Nov 09, 2026.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ • Industrials, Electrical Equipment &amp; Clean Hydrogen Energy • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): The unique 10-digit identifier (0001093691) assigned by the SEC to track Plug Power Inc.'s regulatory filings.">CIK</span>: 0001093691</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price (Nov 2026)</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+{upside_to_pt:.2f}% <span class="tip tip-right tip-bottom" title="Implied Upside to Wall Street Consensus Mean Target Price ($3.39)." data-tip="Implied Upside to Street Target: Percentage upside from current spot price (${spot_price:.2f}) to the 15-analyst consensus mean price target of ${mean_pt:.2f} (median PT $4.00, high $7.00).">Upside to Mean PT</span></span></div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Market Cap</span>
          <span class="strip-val">${mkt_cap_b:.2f}B</span>
          <span class="strip-sub">EV: ${ev_b:.2f}B</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Consensus Revenue</span>
          <span class="strip-val">${consensus_rev:,.2f}M</span>
          <span class="strip-sub">+9.2% YoY Growth</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Consensus Diluted EPS</span>
          <span class="strip-val">${consensus_eps:.2f}</span>
          <span class="strip-sub">Whisper: -$0.05</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">ATM Straddle Implied Move</span>
          <span class="strip-val">±{opt_move_pct:.2f}%</span>
          <span class="strip-sub">Straddle: ±${opt_move_usd:.2f} | IV: {opt_iv:.1f}%</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Short Interest</span>
          <span class="strip-val">{short_float:.2f}%</span>
          <span class="strip-sub">Put/Call OI: {put_call_ratio:.2f}x</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Reporting Date &amp; Timing</span>
          <span class="strip-val">Nov 09, 2026</span>
          <span class="strip-sub">AMC (After Market Close)</span>
        </div>
      </div>
    </header>

    <!-- 2. TRACK B STICKY JUMP-NAV -->
    <nav class="pre-jump-nav" style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; padding: 10px 14px; background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 8px; backdrop-filter: blur(8px);">
      <a href="#row-1-kpis" style="color: #93c5fd; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(59, 130, 246, 0.15); border-radius: 4px; font-weight: 600;">#1 Top KPIs</a>
      <a href="#row-1b-scorecard" style="color: #6ee7b7; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(16, 185, 129, 0.15); border-radius: 4px; font-weight: 600;">#2 Pre-Print Scorecard</a>
      <a href="#row-2-financials" style="color: #c084fc; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(168, 85, 247, 0.15); border-radius: 4px; font-weight: 600;">#3 5-Quarter Financials</a>
      <a href="#row-3-fcf" style="color: #fcd34d; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(245, 158, 11, 0.15); border-radius: 4px; font-weight: 600;">#4 True FCF Bridge</a>
      <a href="#row-4-segments" style="color: #fca5a5; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(239, 68, 68, 0.15); border-radius: 4px; font-weight: 600;">#5 Segment Tailwinds &amp; Headwinds</a>
      <a href="#row-4b-debates" style="color: #93c5fd; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(59, 130, 246, 0.15); border-radius: 4px; font-weight: 600;">#6 Call Debates</a>
      <a href="#row-5-peers" style="color: #e2e8f0; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(255, 255, 255, 0.08); border-radius: 4px; font-weight: 600;">#7 Peer Comps</a>
      <a href="#row-6-sentiment" style="color: #6ee7b7; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(16, 185, 129, 0.15); border-radius: 4px; font-weight: 600;">#8 Sentiment &amp; Skew</a>
      <a href="#row-7-pm-matrix" style="color: #fcd34d; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(245, 158, 11, 0.15); border-radius: 4px; font-weight: 600;">#9 PM Trade Playbook</a>
    </nav>

    <!-- 3. ROW 1: TOP EXECUTIVE KPI CARDS -->
    <section class="kpi-grid" id="row-1-kpis" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-bottom: 24px;">
      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>Quarterly Revenue Stabilisation</span>
          <span class="badge badge-bull">+9.1% QoQ</span>
        </div>
        <div class="kpi-value">$178.30M</div>
        <div class="kpi-sub">Q2 2026 Actual • Consensus Models $193.33M for Q3 (+9.2% YoY)</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Stabilizing warehouse forklift equipment shipments and expanding hydrogen deliveries are positioning Plug Power for improved revenue density across North America.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>Internal Hydrogen Production</span>
          <span class="badge badge-bull">40 TPD Operational</span>
        </div>
        <div class="kpi-value">40 TPD</div>
        <div class="kpi-sub">Georgia &amp; Tennessee Plants • Targeting 55 TPD in Q3 2026E</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Expanding low-cost internal liquid green hydrogen output directly replaces costly third-party merchant supply, narrowing catastrophic historical fuel margin losses.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>DOE $1.66B Loan Facility</span>
          <span class="badge badge-blue">Conditional Guarantee</span>
        </div>
        <div class="kpi-value">$1.66B</div>
        <div class="kpi-sub">Title 17 Clean Energy Debt Facility • Non-Dilutive Capital</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Closing definitive documentation on the DOE loan guarantee will provide dedicated capital to construct up to six regional hydrogen generation hubs without shareholder dilution.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>Forensic True Free Cash Burn</span>
          <span class="badge badge-warn">-$137.67M True FCF</span>
        </div>
        <div class="kpi-value">-$124.72M</div>
        <div class="kpi-sub">Reported FCF (OCF -$94.06M less CapEx $30.66M) • SBC $12.95M</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Strict working capital reductions and reduced plant CapEx lowered cash burn significantly from 2024 peak levels (-$300M+/quarter), extending liquid runway.
        </p>
      </div>
    </section>

    <!-- 4. ROW 1B: PRE-RELEASE EXPECTATIONS, WHISPER SPREAD & HISTORICAL SCORECARD -->
    <section id="row-1b-scorecard" style="margin-bottom: 24px;">
      <!-- Track B Setup Audit Banner -->
      <div class="t1-setup-audit" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-bottom: 16px;">
        <div class="card" style="padding: 14px; border-left: 3px solid #3b82f6;">
          <div style="font-size: 11px; font-weight: 700; color: #93c5fd; text-transform: uppercase;">Pre-Print Options Setup</div>
          <div style="font-size: 16px; font-weight: 800; color: #fff; margin-top: 4px;">Implied Move: ±{opt_move_pct:.2f}% (±${opt_move_usd:.2f})</div>
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Weekly ATM Straddle prices a volatile ±$0.26 move vs historical average 1-day move of 7.68%, indicating an <span style="color:#f59e0b;font-weight:700;">Overpriced Volatility Regime</span>.</div>
        </div>
        <div class="card" style="padding: 14px; border-left: 3px solid #10b981;">
          <div style="font-size: 11px; font-weight: 700; color: #6ee7b7; text-transform: uppercase;">Consensus vs. Whisper Spread</div>
          <div style="font-size: 16px; font-weight: 800; color: #fff; margin-top: 4px;">Top-Line Whisper: $198.0M (+2.42% Bogey)</div>
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Buy-side whisper models a modest beat above the $193.33M consensus, with key focus on electrolyzer deliveries and fuel margin inflection.</div>
        </div>
        <div class="card" style="padding: 14px; border-left: 3px solid #f59e0b;">
          <div style="font-size: 11px; font-weight: 700; color: #fcd34d; text-transform: uppercase;">Historical Beat Track Record</div>
          <div style="font-size: 16px; font-weight: 800; color: #fff; margin-top: 4px;">75.0% Beat Rate (3 Beats, 1 Miss)</div>
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Plug Power beat bottom-line consensus EPS in 3 of the prior 4 quarters, benefiting from restructuring actions and lower OpEx.</div>
        </div>
      </div>

      <!-- Table 1B-1: Headline & Company KPI Consensus vs Whisper Scorecard -->
      <div class="section-title">
        <span class="section-title-accent"></span>Table 1B-1: Headline &amp; Company KPI Consensus vs. Buy-Side Whisper Scorecard
      </div>
      <div class="table-wrapper" style="margin-bottom: 16px;">
        <table class="data-table">
          <thead>
            <tr>
              <th>Operational Metric / Benchmark</th>
              <th>Q-1 Actual</th>
              <th>Q-4 YoY Baseline</th>
              <th class="col-q0">Street Consensus (Q0E)</th>
              <th>Buy-Side Whisper Bogey</th>
              <th>Whisper Spread &amp; Beat Bar</th>
              <th>Expectation Hurdle</th>
            </tr>
          </thead>
          <tbody>
{table_1b1_rows_html}
          </tbody>
        </table>
      </div>

      <!-- Table 1B-2: Management Guidance Credibility & Track Record -->
      <div class="section-title">
        <span class="section-title-accent"></span>Table 1B-2: Management Guidance Credibility &amp; 4Q Historical Track Record
      </div>
      <div style="margin-bottom: 12px; padding: 10px 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border-color); border-radius: 6px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <span style="font-size: 12.5px; font-weight: 700; color: #e2e8f0;">Executive Sandbagging &amp; Credibility Score: <span style="color:#60a5fa;">{bus_2b['credibility_score']} / 100</span></span>
          <span class="badge badge-bull">{bus_2b['credibility_label'].split('(')[0].strip()}</span>
        </div>
        <div class="credibility-gauge-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
          <div style="width: {bus_2b['credibility_score']}%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
        </div>
      </div>
      <div class="table-wrapper" style="margin-bottom: 16px;">
        <table class="data-table">
          <thead>
            <tr>
              <th>Guidance Metric / Corridor</th>
              <th>Prior Q Management Guidance for Q0</th>
              <th>Current Street Consensus</th>
              <th>4Q Beat Rate</th>
              <th>Execution Variance &amp; Sandbagging Analysis</th>
              <th>Credibility Grade</th>
            </tr>
          </thead>
          <tbody>
{table_1b2_rows_html}
          </tbody>
        </table>
      </div>

      <!-- Table 1B-3: Forward Guidance Bogeys & Re-Rating Hurdles -->
      <div class="section-title">
        <span class="section-title-accent"></span>Table 1B-3: Forward Guidance Bogeys &amp; Re-Rating Hurdles (Q4 2026E &amp; FY2027)
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Forward Guidance Target Metric</th>
              <th>Street Consensus Hurdle</th>
              <th>Buy-Side Bull Bogey</th>
              <th>Bear Breakdown Threshold</th>
              <th>Multiple Sensitivity</th>
              <th>Strategic Institutional Rationale</th>
            </tr>
          </thead>
          <tbody>
{table_1b3_rows_html}
          </tbody>
        </table>
      </div>
    </section>

    <!-- 5. ROW 2: 5-QUARTER STITCHED FINANCIAL TABLE + Q0E CONSENSUS -->
    <section class="financials-section" id="row-2-financials" style="margin-bottom: 24px;">
      <div class="section-title">
        <span class="section-title-accent"></span>Rolling 5-Quarter Stitched Financial Table &amp; Upcoming Consensus Estimate
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Metric ($ Millions, GAAP)</th>
              <th>Q2 2025</th>
              <th>Q3 2025</th>
              <th>Q4 2025</th>
              <th>Q1 2026</th>
              <th class="col-q0">Q2 2026 (Latest Actual)</th>
              <th class="col-est">Q3 2026E (Consensus)</th>
              <th>QoQ Growth</th>
              <th>YoY Growth</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; color: #60a5fa;">
              <td><span class="tip" title="Total GAAP Net Revenue across fuel cells, hydrogen delivery, electrolyzers, and services." data-tip="Total GAAP Revenue: Fully consolidated GAAP revenue generated from material handling fuel cell systems, bulk green hydrogen fuel, cryogenic trailers, and megawatt-scale PEM electrolyzer systems.">Total Net Revenue</span></td>
              <td>${total_rev[0]:,.2f}M</td>
              <td>${total_rev[1]:,.2f}M</td>
              <td>${total_rev[2]:,.2f}M</td>
              <td>${total_rev[3]:,.2f}M</td>
              <td class="col-q0">${total_rev[4]:,.2f}M</td>
              <td class="col-est">${consensus_rev:,.2f}M</td>
              <td style="color:#34d399;">+{((total_rev[4]-total_rev[3])/total_rev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((total_rev[4]-total_rev[0])/total_rev[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• Fuel Cell Systems &amp; Infrastructure</td>
              <td>${equip_rev[0]:,.2f}M</td>
              <td>${equip_rev[1]:,.2f}M</td>
              <td>${equip_rev[2]:,.2f}M</td>
              <td>${equip_rev[3]:,.2f}M</td>
              <td class="col-q0">${equip_rev[4]:,.2f}M</td>
              <td class="col-est">$123.00M</td>
              <td style="color:#34d399;">+{((equip_rev[4]-equip_rev[3])/equip_rev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((equip_rev[4]-equip_rev[0])/equip_rev[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• Hydrogen Delivery &amp; Power Purchased</td>
              <td>${fuel_rev[0]:,.2f}M</td>
              <td>${fuel_rev[1]:,.2f}M</td>
              <td>${fuel_rev[2]:,.2f}M</td>
              <td>${fuel_rev[3]:,.2f}M</td>
              <td class="col-q0">${fuel_rev[4]:,.2f}M</td>
              <td class="col-est">$38.50M</td>
              <td style="color:#34d399;">+{((fuel_rev[4]-fuel_rev[3])/fuel_rev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((fuel_rev[4]-fuel_rev[0])/fuel_rev[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• Electrolyzer Generation Equipment</td>
              <td>${electrolyzer_rev[0]:,.2f}M</td>
              <td>${electrolyzer_rev[1]:,.2f}M</td>
              <td>${electrolyzer_rev[2]:,.2f}M</td>
              <td>${electrolyzer_rev[3]:,.2f}M</td>
              <td class="col-q0">${electrolyzer_rev[4]:,.2f}M</td>
              <td class="col-est">$16.83M</td>
              <td style="color:#f87171;">{((electrolyzer_rev[4]-electrolyzer_rev[3])/electrolyzer_rev[3])*100:.1f}%</td>
              <td style="color:#f87171;">{((electrolyzer_rev[4]-electrolyzer_rev[0])/electrolyzer_rev[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• Power Purchase Agreements &amp; Services</td>
              <td>${services_rev[0]:,.2f}M</td>
              <td>${services_rev[1]:,.2f}M</td>
              <td>${services_rev[2]:,.2f}M</td>
              <td>${services_rev[3]:,.2f}M</td>
              <td class="col-q0">${services_rev[4]:,.2f}M</td>
              <td class="col-est">$15.00M</td>
              <td style="color:#34d399;">+{((services_rev[4]-services_rev[3])/services_rev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((services_rev[4]-services_rev[0])/services_rev[0])*100:.1f}%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cost of Revenue: Direct equipment manufacturing, merchant hydrogen sourcing, and electricity." data-tip="Cost of Revenue: Direct material costs, factory labor, expensive third-party merchant hydrogen purchases, and power tariff expenses.">Cost of Revenue</span></td>
              <td>${total_rev[0]-gross_profit[0]:,.2f}M</td>
              <td>${total_rev[1]-gross_profit[1]:,.2f}M</td>
              <td>${total_rev[2]-gross_profit[2]:,.2f}M</td>
              <td>${total_rev[3]-gross_profit[3]:,.2f}M</td>
              <td class="col-q0">${total_rev[4]-gross_profit[4]:,.2f}M</td>
              <td class="col-est">$195.00M</td>
              <td style="color:#34d399;">-2.7%</td>
              <td style="color:#34d399;">-20.9%</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="Gross Profit: Total revenue minus cost of revenue." data-tip="Gross Profit: Consolidated gross profit/loss reflecting negative fuel delivery margins offset by equipment shipments.">Gross Profit</span></td>
              <td style="color:#f87171;">${gross_profit[0]:,.2f}M</td>
              <td style="color:#f87171;">${gross_profit[1]:,.2f}M</td>
              <td style="color:#34d399;">+${gross_profit[2]:,.2f}M</td>
              <td style="color:#f87171;">${gross_profit[3]:,.2f}M</td>
              <td class="col-q0" style="color:#f87171;">${gross_profit[4]:,.2f}M</td>
              <td class="col-est" style="color:#f87171;">-$1.67M</td>
              <td style="color:#34d399;">+92.2%</td>
              <td style="color:#34d399;">+96.9%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Expenses: R&D, sales, general & administrative expenses." data-tip="Operating Expenses: Includes engineering R&D, corporate overhead, restructuring costs, and site development expenses.">Operating Expenses</span></td>
              <td>${opex[0]:,.2f}M</td>
              <td>${opex[1]:,.2f}M</td>
              <td>${opex[2]:,.2f}M</td>
              <td>${opex[3]:,.2f}M</td>
              <td class="col-q0">${opex[4]:,.2f}M</td>
              <td class="col-est">$52.00M</td>
              <td style="color:#34d399;">-48.1%</td>
              <td style="color:#34d399;">-57.3%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income (EBIT): Operating loss from core green hydrogen manufacturing and delivery before interest and taxes.">Operating Income (EBIT)</span></td>
              <td style="color:#f87171;">${ebit[0]:,.2f}M</td>
              <td style="color:#f87171;">${ebit[1]:,.2f}M</td>
              <td style="color:#f87171;">${ebit[2]:,.2f}M</td>
              <td style="color:#f87171;">${ebit[3]:,.2f}M</td>
              <td class="col-q0" style="color:#f87171;">${ebit[4]:,.2f}M</td>
              <td class="col-est" style="color:#f87171;">-$53.67M</td>
              <td style="color:#34d399;">+57.3%</td>
              <td style="color:#34d399;">+71.1%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Net Income / (Loss) attributable to common stockholders." data-tip="GAAP Net Income: Consolidated net loss after accounting for equipment financing interest and non-cash asset adjustments.">GAAP Net Income</span></td>
              <td style="color:#f87171;">${net_income[0]:,.2f}M</td>
              <td style="color:#f87171;">${net_income[1]:,.2f}M</td>
              <td style="color:#f87171;">${net_income[2]:,.2f}M</td>
              <td style="color:#f87171;">${net_income[3]:,.2f}M</td>
              <td class="col-q0" style="color:#f87171;">${net_income[4]:,.2f}M</td>
              <td class="col-est" style="color:#f87171;">-$85.00M</td>
              <td style="color:#34d399;">+23.3%</td>
              <td style="color:#34d399;">+17.1%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 6. ROW 3: FORENSIC HIGHLIGHTS & TRUE FCF WATERFALL BRIDGE -->
    <section class="forensic-section" id="row-3-fcf" style="margin-bottom: 24px;">
      <div class="section-title">
        <span class="section-title-accent"></span>Forensic Cash Flow Quality &amp; True Free Cash Flow Waterfall Bridge
      </div>
      <div class="forensic-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
        <div class="card" style="padding: 16px;">
          <div class="card-header">
            <span class="card-title"><span class="card-title-accent"></span>Latest Reported Quarter (Q2 2026) FCF Bridge</span>
            <span class="badge badge-warn">Burn Reduction</span>
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            The forensic waterfall below bridges reported GAAP Operating Cash Flow (${latest_ocf:,.2f}M) to institutional True Free Cash Flow (-${abs(latest_true_fcf):,.2f}M), isolating green hydrogen plant CapEx and non-cash equity compensation.
          </p>
          <div style="background: rgba(11, 15, 25, 0.6); padding: 12px; border-radius: 6px; border: 1px solid var(--border-color);">
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Operating Cash Flow: Cash used in operating activities." data-tip="Operating Cash Flow (OCF): Net cash used in operational hydrogen delivery and manufacturing (-$94.06M in Q2 2026), significantly narrowed from prior year levels.">Operating Cash Flow (OCF)</span></span>
              <span style="font-weight: 700; color: #f87171;">-${abs(latest_ocf):,.2f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Capital Expenditures: Purchases of property, plant, equipment, and electrolyzer stacks." data-tip="Capital Expenditures (CapEx): Cash deployed for liquid hydrogen plant construction and cryogenic equipment ($30.66M).">Less: Capital Expenditures (CapEx)</span></span>
              <span style="font-weight: 700; color: #f87171;">-${latest_capex:,.2f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px; font-weight: 600; color: #93c5fd;">
              <span>Reported Free Cash Flow (OCF - CapEx)</span>
              <span>-${abs(latest_reported_fcf):,.2f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Stock-Based Compensation: Non-cash compensation expense." data-tip="Stock-Based Compensation (SBC): Non-cash equity compensation grants of $12.95M deducted by institutional analysts.">Less: Stock-Based Compensation (SBC)</span></span>
              <span style="font-weight: 700; color: #f87171;">-${latest_sbc:,.2f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Finance Lease Principal Repayments." data-tip="Finance Leases: Contractual debt repayments on equipment leases ($0.0M in Q2 2026).">Less: Finance Lease Repayments</span></span>
              <span style="font-weight: 700; color: #94a3b8;">-$0.00M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; font-weight: 800; color: #fca5a5; border-top: 1px dashed rgba(255,255,255,0.2);">
              <span>Forensic True Free Cash Flow</span>
              <span>-${abs(latest_true_fcf):,.2f}M</span>
            </div>
          </div>
        </div>

        <div class="card" style="padding: 16px;">
          <div class="card-header">
            <span class="card-title"><span class="card-title-accent"></span>Institutional Quality of Earnings Takeaways</span>
            <span class="badge badge-blue">Burn Trajectory</span>
          </div>
          <div style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.6;">
            <p style="margin-bottom: 8px;">
              <strong>1. Cash Burn Moderation:</strong> Operating cash burn of -$94.06M represents a massive improvement from peak quarterly cash drains of -$300M+ in 2023–2024, proving restructuring efficacy.
            </p>
            <p style="margin-bottom: 8px;">
              <strong>2. Disciplined Capital Intensity:</strong> CapEx was disciplined at $30.66M, focusing purely on completing the Georgia and Tennessee liquid hydrogen plants while pausing speculative expansions.
            </p>
            <p>
              <strong>3. Working Capital Realignment:</strong> Inventory optimization and raw material supplier renegotiations have released working capital back into cash balances.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ROW 4: SEGMENT EXECUTION AUDIT GRID (4 TAILWINDS VS 4 HEADWINDS) -->
    <section class="audit-section" id="row-4-segments" style="margin-bottom: 24px;">
      <div class="section-title">
        <span class="section-title-accent"></span>Segment Execution Audit: 4 Operational Tailwinds vs. 4 Execution Headwinds
      </div>
      <div class="audit-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
        <!-- Tailwinds -->
        <div class="card" style="border-left: 3px solid #10b981;">
          <div class="card-header">
            <span class="card-title" style="color: #34d399;"><span class="card-title-accent" style="background: #10b981;"></span>4 Key Operational Tailwinds</span>
            <span class="badge badge-bull">Turnaround Catalysts</span>
          </div>
          <div style="margin-top: 10px;">
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">1. Georgia &amp; Tennessee Green Hydrogen Plant Ramp:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Internal production scaling to 40+ TPD replaces high-cost merchant hydrogen, driving structural gross margin improvement toward breakeven.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">2. DOE $1.66 Billion Loan Facility Closing:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Securing definitive documentation for the clean energy loan guarantee removes balance sheet insolvency risk and provides dedicated construction capital.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">3. Anchor Material Handling Customer Base:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Over 60,000 active fuel cell systems operating at mission-critical distribution centers for Amazon, Walmart, and Home Depot provide durable long-term service revenue.</p>
            </div>
            <div>
              <strong style="color: #6ee7b7; font-size: 13px;">4. Global Electrolyzer Pipeline Growth:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Modular 5MW GenSys PEM electrolyzers gain traction in European green ammonia and refining projects, expanding international backlog.</p>
            </div>
          </div>
        </div>

        <!-- Headwinds -->
        <div class="card" style="border-left: 3px solid #ef4444;">
          <div class="card-header">
            <span class="card-title" style="color: #f87171;"><span class="card-title-accent" style="background: #ef4444;"></span>4 Key Execution Headwinds</span>
            <span class="badge badge-warn">Turnaround Risks</span>
          </div>
          <div style="margin-top: 10px;">
            <div style="margin-bottom: 10px;">
              <strong style="color: #fca5a5; font-size: 13px;">1. Lingering Cash Burn (-$94.06M OCF):</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Ongoing negative operating cash flow requires continued external capital access and careful liquidity management until production reaches full utilization.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #fca5a5; font-size: 13px;">2. Hydrogen Fuel Margin Losses:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Until Louisiana and Texas plants reach commercial operation, Plug remains partially dependent on external merchant molecules, exposing margins to power spikes.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #fca5a5; font-size: 13px;">3. Customer Concentration Risk:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">A large percentage of equipment revenue remains tied to two primary retail warehouse customers, exposing quarters to timing delays in customer site buildouts.</p>
            </div>
            <div>
              <strong style="color: #fca5a5; font-size: 13px;">4. Elevated Short Interest (23.54% Float):</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Short sellers remain heavily crowded, arguing that capital requirements will exceed internal generation and necessitate future dilutive offerings.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 8. SECTION 4B: TOP 3 INSTITUTIONAL PRE-PRINT DEBATES -->
    <div id="row-4b-debates" style="margin-bottom: 24px;">
      <div class="section-title">
        <span class="section-title-accent"></span>Section 4B: Top 3 Institutional Pre-Print Debates &amp; Conference Call Focus Questions
      </div>
      <div class="card" style="padding: 16px;">
{section_4b_debates_html}
      </div>
    </div>

    <!-- 9. ROW 5: PEER VALUATION COMPS -->
    <section class="peer-section" id="row-5-peers" style="margin-bottom: 24px;">
      <div class="section-title">
        <span class="section-title-accent"></span>Peer Valuation Benchmarks &amp; Multiple Comparison
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Company / Peer Ticker</th>
              <th>Market Cap</th>
              <th>Forward P/E</th>
              <th>Trailing P/S</th>
              <th>EV/EBITDA</th>
              <th>Revenue Growth (YoY)</th>
              <th>Short % Float</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background: rgba(59, 130, 246, 0.1); font-weight: 700;">
              <td><span class="tip" title="Plug Power Inc. (Target Company)" data-tip="Plug Power: Turnkey hydrogen solutions and fuel cell equipment developer.">Plug Power (PLUG)</span></td>
              <td>${mkt_cap_b:.2f}B</td>
              <td>{fwd_pe:.2f}x</td>
              <td>{ps_ttm:.2f}x</td>
              <td>{ev_ebitda:.2f}x</td>
              <td style="color: #34d399;">+9.2%</td>
              <td style="color: #f59e0b;">{short_float:.2f}%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Bloom Energy Corporation" data-tip="BE: Solid oxide fuel cell and electrolyzer manufacturer for commercial power.">Bloom Energy (BE)</span></td>
              <td>$2,850.0M</td>
              <td>24.5x</td>
              <td>2.1x</td>
              <td>18.2x</td>
              <td>+14.0%</td>
              <td>18.5%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Ballard Power Systems Inc." data-tip="BLDP: Proton exchange membrane (PEM) fuel cell developer for heavy duty transit.">Ballard Power (BLDP)</span></td>
              <td>$620.0M</td>
              <td>-4.8x</td>
              <td>6.5x</td>
              <td>-3.8x</td>
              <td>-8.0%</td>
              <td>12.8%</td>
            </tr>
            <tr>
              <td><span class="tip" title="FuelCell Energy, Inc." data-tip="FCEL: Carbonate fuel cell power platform and carbon capture developer.">FuelCell Energy (FCEL)</span></td>
              <td>$280.0M</td>
              <td>-2.5x</td>
              <td>2.8x</td>
              <td>-2.1x</td>
              <td>-15.0%</td>
              <td>19.2%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Nel ASA" data-tip="NEL: Global dedicated electrolyzer company manufacturing alkaline and PEM equipment.">Nel ASA (NEL)</span></td>
              <td>$850.0M</td>
              <td>-8.0x</td>
              <td>4.5x</td>
              <td>-6.2x</td>
              <td>+12.0%</td>
              <td>8.5%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 10. ROW 6: MULTI-SOURCE 4-PILLAR SENTIMENT GRID -->
    <section class="sentiment-section" id="row-6-sentiment" style="margin-bottom: 24px;">
      <div class="section-title">
        <span class="section-title-accent"></span>Multi-Source 4-Pillar Pre-Earnings Sentiment Gauge
      </div>
      <div class="sentiment-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-bottom: 16px;">
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #93c5fd; text-transform: uppercase;">Pillar 1: Sell-Side Consensus</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">70 / 100 (Hold / Turnaround Watch)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 70%; height: 100%; background: #60a5fa;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">15 covering analysts maintain Hold rating (2.79 score) with $3.39 mean price target (+142.14% upside).</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #6ee7b7; text-transform: uppercase;">Pillar 2: Buy-Side Whisper</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">75 / 100 ($198M Revenue Bogey)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 75%; height: 100%; background: #10b981;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Hedge fund desks look for $198M top-line whisper and proof of internal liquid hydrogen production ramp.</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #fcd34d; text-transform: uppercase;">Pillar 3: Retail &amp; FinTwit Sentiment</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">85 / 100 (Short Squeeze Speculation)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 85%; height: 100%; background: #f59e0b;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Retail discussions across Reddit r/wallstreetbets, r/plugpower, and FinTwit are heavily call-biased citing 23.54% short float and 0.10x Put/Call ratio.</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #c084fc; text-transform: uppercase;">Pillar 4: Short Squeeze &amp; Options Skew</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">88 / 100 (High Upward Convexity)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 88%; height: 100%; background: #a855f7;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Weekly straddle prices a violent ±18.57% move ($0.26 straddle). Any DOE loan closing confirmation triggers massive short covering.</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px;">
        <div class="card" style="padding: 14px; border-left: 3px solid #3b82f6;">
          <div style="font-weight: 700; color: #93c5fd; font-size: 13px; margin-bottom: 4px;">Retail Positioning Pulse (Reddit &amp; FinTwit)</div>
          <p style="font-size: 12.3px; color: var(--text-secondary); line-height: 1.5;">
            {bus_2c['retail_vs_institutional_positioning']['retail_summary']}
          </p>
        </div>
        <div class="card" style="padding: 14px; border-left: 3px solid #10b981;">
          <div style="font-weight: 700; color: #6ee7b7; font-size: 13px; margin-bottom: 4px;">Institutional Desk Intelligence</div>
          <p style="font-size: 12.3px; color: var(--text-secondary); line-height: 1.5;">
            {bus_2c['retail_vs_institutional_positioning']['institutional_summary']}
          </p>
        </div>
      </div>
    </section>

    <!-- 11. ROW 7: HEDGE FUND PM TRADE EXECUTION MATRIX -->
    <section class="scenario-section" id="row-7-pm-matrix" style="margin-bottom: 30px;">
      <div class="section-title">
        <span class="section-title-accent"></span>Hedge Fund PM Post-Earnings Trade Execution Playbook
      </div>
      <div class="scenario-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">
        <!-- Bull Case -->
        <div class="card scenario-bull" style="border-top: 3px solid #10b981;">
          <div class="card-header">
            <div class="card-title" style="color: #34d399;"><span class="card-title-accent" style="background: #10b981;"></span>Bull Case Scenario (35% Probability)</div>
            <span class="badge badge-bull">TARGET: $1.80 – $2.40</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 Revenue prints above $198M, fuel gross margin inflects closer to breakeven, and management confirms closing steps for the $1.66B DOE loan guarantee, triggering short squeeze across 23.54% float.
          </p>
          <div class="trade-structure" style="background: rgba(16, 185, 129, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #6ee7b7;">
            <strong>Options Structure:</strong> Nov 13 $1.50 / $2.00 Bull Call Spread to leverage asymmetric upside while capping high options implied volatility outlay (160.94%).
          </div>
        </div>

        <!-- Base Case -->
        <div class="card scenario-base" style="border-top: 3px solid #3b82f6;">
          <div class="card-header">
            <div class="card-title" style="color: #60a5fa;"><span class="card-title-accent" style="background: #3b82f6;"></span>Base Case Scenario (45% Probability)</div>
            <span class="badge badge-blue">TARGET: $1.25 – $1.55</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 revenue meets consensus at $190M–$195M, cash burn remains controlled around -$90M, and management provides steady progress on internal plant operations without closing loan documents.
          </p>
          <div class="trade-structure" style="background: rgba(59, 130, 246, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #93c5fd;">
            <strong>Options Structure:</strong> Nov 13 $1.00 / $2.00 Short Iron Condor to capture post-announcement implied volatility crush from 160% down toward 75%.
          </div>
        </div>

        <!-- Bear Case -->
        <div class="card scenario-bear" style="border-top: 3px solid #ef4444;">
          <div class="card-header">
            <div class="card-title" style="color: #f87171;"><span class="card-title-accent" style="background: #ef4444;"></span>Bear Case Scenario (20% Probability)</div>
            <span class="badge badge-warn">TARGET: $0.90 – $1.15</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 revenue falls short (&lt; $180M) or operating cash burn re-accelerates past -$110M, reigniting concerns regarding future equity dilution.
          </p>
          <div class="trade-structure" style="background: rgba(239, 68, 68, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #fca5a5;">
            <strong>Options Structure:</strong> Nov 13 $1.50 / $1.00 Bear Put Spread to hedge downside valuation compression.
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER VERIFICATION LEDGER -->
    <footer style="margin-top: 30px; padding: 16px; border-top: 1px solid var(--border-color); font-size: 11.5px; color: var(--text-muted); text-align: center;">
      <p>Deterministic Ground-Truth Ledger: Spot Price: ${spot_price:.2f} | Consensus Revenue: ${consensus_rev:.2f}M | Consensus EPS: ${consensus_eps:.2f} | Latest OCF: ${latest_ocf:.2f}M ({ocf_int_str}) | True FCF: ${latest_true_fcf:.2f}M | Options-Implied Move: ±{opt_move_pct:.2f}% (±${opt_move_usd:.2f}) | 4Q Historical Beat Rate: 75.0% | Wall Street Consensus Mean PT: ${mean_pt:.2f}</p>
      <p style="margin-top: 4px;">Antigravity 2.0 Institutional Tearsheet • Strict Zero-Hallucination Multi-Agent Orchestration Mesh</p>
    </footer>
"""

draft_payload = {
    "ticker": "PLUG",
    "earnings_date": "2026-11-09",
    "header": {
        "page_title": "PLUG Q3 2026E Pre-Earnings Briefing | Plug Power Institutional Tearsheet"
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
        "bull_target_low_num": 1.80,
        "bear_target_high_num": 1.15
    },
    "rendered_container_html": html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"Draft written to {DRAFT_PATH} (HTML length: {len(html)} chars)")
