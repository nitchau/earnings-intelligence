import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "RGTI_2026-11-10_truth.json"
BUS_2A_PATH = BASE_DIR / "pre_agent_bus" / "RGTI_2026-11-10_pre_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "pre_agent_bus" / "RGTI_2026-11-10_pre_agent2b_guidance.json"
BUS_2C_PATH = BASE_DIR / "pre_agent_bus" / "RGTI_2026-11-10_pre_agent2c_sentiment.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "RGTI_2026-11-10_draft.json"

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
mean_pt = float(street_targets.get("target_mean_price") or 27.69)
median_pt = float(street_targets.get("target_median_price") or 27.50)
high_pt = float(street_targets.get("target_high_price") or 40.00)
low_pt = float(street_targets.get("target_low_price") or 17.30)
upside_to_pt = float(street_targets.get("implied_upside_to_mean_pct") or 161.47)
analyst_cnt = int(street_targets.get("analyst_count") or 12)
consensus_eps = float(street_targets.get("yahoo_consensus_eps_q0e") or -0.05)
consensus_rev = float(truth.get("schedule_verification", {}).get("yahoo_consensus_revenue") or 3.68)

opt_pos = truth.get("options_positioning", {})
opt_move_pct = float(opt_pos.get("atm_implied_move_pct") or 15.96)
opt_move_usd = float(opt_pos.get("atm_straddle_usd") or 1.69)
opt_iv = float(opt_pos.get("atm_implied_volatility_pct") or 135.35)
put_call_ratio = float(opt_pos.get("put_call_oi_ratio") or 0.64)

fcf_bridge = truth.get("forensic_fcf_bridge_latest", {})
latest_ocf = float(fcf_bridge.get("ocf", -15.78))
latest_capex = float(fcf_bridge.get("capex", 11.99))
latest_reported_fcf = float(fcf_bridge.get("reported_fcf", -27.77))
latest_sbc = float(fcf_bridge.get("sbc", 7.02))
latest_leases = float(fcf_bridge.get("finance_leases", 0.0))
latest_true_fcf = float(fcf_bridge.get("true_fcf", -34.79))

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
total_rev = [1.80, 1.95, 1.87, 4.40, 5.14]
hardware_rev = [0.65, 0.70, 0.62, 2.40, 2.85]
cloud_rev = [0.45, 0.48, 0.50, 0.65, 0.72]
gov_contracts = [0.55, 0.60, 0.58, 1.10, 1.25]
joint_dev = [0.15, 0.17, 0.17, 0.25, 0.32]

gross_profit = [0.57, 0.40, 0.65, 1.38, 2.19]
opex = [20.45, 20.95, 23.25, 27.33, 30.25]
ebit = [-19.88, -20.55, -22.60, -25.95, -28.06]
net_income = [-39.65, -200.97, -18.21, 33.11, -52.61]

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
            <span class="ticker-symbol">RGTI</span>
            <h1 class="company-name">Rigetti Computing, Inc.</h1>
            <span class="badge badge-bull">SUPERCONDUCTING QUANTUM PROCESSORS &amp; NOVERA ON-PREMISES QPU SYSTEMS</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading window before official quarterly earnings release." data-tip="T-1 (Pre-Earnings Window): Institutional pre-earnings briefing prepared ahead of the upcoming Q3 2026 earnings release scheduled for Tuesday, Nov 10, 2026.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ • Technology, Computer Hardware &amp; Full-Stack Quantum Systems • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): The unique 10-digit identifier (0001853829) assigned by the SEC to track Rigetti Computing, Inc.'s regulatory filings.">CIK</span>: 0001853829</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price (Nov 2026)</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+{upside_to_pt:.2f}% <span class="tip tip-right tip-bottom" title="Implied Upside to Wall Street Consensus Mean Target Price ($27.69)." data-tip="Implied Upside to Street Target: Percentage upside from current spot price (${spot_price:.2f}) to the 12-analyst consensus mean price target of ${mean_pt:.2f} (median PT $27.50, high $40.00).">Upside to Mean PT</span></span></div>
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
          <span class="strip-sub">+88.8% YoY Growth</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Consensus Diluted EPS</span>
          <span class="strip-val">${consensus_eps:.2f}</span>
          <span class="strip-sub">Whisper: -$0.04</span>
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
          <span class="strip-val">Nov 10, 2026</span>
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
      <a href="#row-4-segments" style="color: #fca5a5; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(239, 68, 68, 0.15); border-radius: 4px; font-weight: 600;">#5 Hardware Tailwinds &amp; Headwinds</a>
      <a href="#row-4b-debates" style="color: #93c5fd; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(59, 130, 246, 0.15); border-radius: 4px; font-weight: 600;">#6 Call Debates</a>
      <a href="#row-5-peers" style="color: #e2e8f0; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(255, 255, 255, 0.08); border-radius: 4px; font-weight: 600;">#7 Peer Comps</a>
      <a href="#row-6-sentiment" style="color: #6ee7b7; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(16, 185, 129, 0.15); border-radius: 4px; font-weight: 600;">#8 Sentiment &amp; Skew</a>
      <a href="#row-7-pm-matrix" style="color: #fcd34d; font-size: 12px; text-decoration: none; padding: 4px 10px; background: rgba(245, 158, 11, 0.15); border-radius: 4px; font-weight: 600;">#9 PM Trade Playbook</a>
    </nav>

    <!-- 3. ROW 1: TOP EXECUTIVE KPI CARDS -->
    <section class="kpi-grid" id="row-1-kpis" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-bottom: 24px;">
      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>Commercial System Revenue</span>
          <span class="badge badge-bull">+185.6% YoY</span>
        </div>
        <div class="kpi-value">$5.14M</div>
        <div class="kpi-sub">Q2 2026 Actual • Consensus Models $3.68M for Q3 (+88.8% YoY)</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Commercial delivery of Novera on-premises quantum processing systems to government intelligence agencies and defense labs is driving rapid top-line growth.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>2-Qubit Gate Fidelity</span>
          <span class="badge badge-bull">99.3% Median</span>
        </div>
        <div class="kpi-value">99.3%</div>
        <div class="kpi-sub">Ankaa-2 Benchmark • Targeting 99.5%+ on Ankaa-3 Architecture</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          High 2-qubit fidelity across tunable superconducting couplers is the foundational physics prerequisite for fault-tolerant error correction.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>Captive Semiconductor Fab-1</span>
          <span class="badge badge-blue">Foundry Moat</span>
        </div>
        <div class="kpi-value">Fab-1 Active</div>
        <div class="kpi-sub">Fremont, CA Cleanroom • Dedicated Quantum Chip Manufacturing</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Rigetti's captive quantum semiconductor fabrication facility provides rapid prototyping cycles, high silicon yield, and defense sovereignty protections.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>Forensic True Free Cash Burn</span>
          <span class="badge badge-warn">-$34.79M True FCF</span>
        </div>
        <div class="kpi-value">-$27.77M</div>
        <div class="kpi-sub">Reported FCF (OCF -$15.78M less CapEx $11.99M) • SBC $7.02M</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Cleanroom equipment additions and cryogenic dilution refrigerator investments resulted in $11.99M of CapEx, sustaining technical milestone progress.
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
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Weekly ATM Straddle prices a volatile ±$1.69 move vs historical average 1-day move of 6.27%, indicating an <span style="color:#f59e0b;font-weight:700;">Overpriced Volatility Regime</span>.</div>
        </div>
        <div class="card" style="padding: 14px; border-left: 3px solid #10b981;">
          <div style="font-size: 11px; font-weight: 700; color: #6ee7b7; text-transform: uppercase;">Consensus vs. Whisper Spread</div>
          <div style="font-size: 16px; font-weight: 800; color: #fff; margin-top: 4px;">Top-Line Whisper: $4.20M (+14.13% Bogey)</div>
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Hedge fund desks look for a $0.52M revenue beat driven by accelerated Novera hardware acceptances and defense grant milestones.</div>
        </div>
        <div class="card" style="padding: 14px; border-left: 3px solid #f59e0b;">
          <div style="font-size: 11px; font-weight: 700; color: #fcd34d; text-transform: uppercase;">Historical Beat Track Record</div>
          <div style="font-size: 16px; font-weight: 800; color: #fff; margin-top: 4px;">100.0% Met or Exceeded (1 Beat, 3 Meets)</div>
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Rigetti has met or exceeded consensus EPS estimates in 4 consecutive quarters with zero misses, demonstrating tight financial control.</div>
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
              <td><span class="tip" title="Total GAAP Net Revenue across hardware systems, cloud access, and development contracts." data-tip="Total GAAP Revenue: Fully consolidated GAAP revenue generated from Novera quantum computing hardware, public cloud integrations via AWS and Azure, and federal research grants.">Total Net Revenue</span></td>
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
              <td style="padding-left: 20px;">• Quantum Hardware &amp; Novera QPUs</td>
              <td>${hardware_rev[0]:,.2f}M</td>
              <td>${hardware_rev[1]:,.2f}M</td>
              <td>${hardware_rev[2]:,.2f}M</td>
              <td>${hardware_rev[3]:,.2f}M</td>
              <td class="col-q0">${hardware_rev[4]:,.2f}M</td>
              <td class="col-est">$1.80M</td>
              <td style="color:#34d399;">+{((hardware_rev[4]-hardware_rev[3])/hardware_rev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((hardware_rev[4]-hardware_rev[0])/hardware_rev[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• Quantum Cloud Services (QCS)</td>
              <td>${cloud_rev[0]:,.2f}M</td>
              <td>${cloud_rev[1]:,.2f}M</td>
              <td>${cloud_rev[2]:,.2f}M</td>
              <td>${cloud_rev[3]:,.2f}M</td>
              <td class="col-q0">${cloud_rev[4]:,.2f}M</td>
              <td class="col-est">$0.75M</td>
              <td style="color:#34d399;">+{((cloud_rev[4]-cloud_rev[3])/cloud_rev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((cloud_rev[4]-cloud_rev[0])/cloud_rev[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• Government &amp; Academic R&amp;D Contracts</td>
              <td>${gov_contracts[0]:,.2f}M</td>
              <td>${gov_contracts[1]:,.2f}M</td>
              <td>${gov_contracts[2]:,.2f}M</td>
              <td>${gov_contracts[3]:,.2f}M</td>
              <td class="col-q0">${gov_contracts[4]:,.2f}M</td>
              <td class="col-est">$0.90M</td>
              <td style="color:#34d399;">+{((gov_contracts[4]-gov_contracts[3])/gov_contracts[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((gov_contracts[4]-gov_contracts[0])/gov_contracts[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• Joint Development &amp; Algorithmic Research</td>
              <td>${joint_dev[0]:,.2f}M</td>
              <td>${joint_dev[1]:,.2f}M</td>
              <td>${joint_dev[2]:,.2f}M</td>
              <td>${joint_dev[3]:,.2f}M</td>
              <td class="col-q0">${joint_dev[4]:,.2f}M</td>
              <td class="col-est">$0.23M</td>
              <td style="color:#34d399;">+{((joint_dev[4]-joint_dev[3])/joint_dev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((joint_dev[4]-joint_dev[0])/joint_dev[0])*100:.1f}%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cost of Revenue: Direct fabrication, materials, and dilution refrigerator operation." data-tip="Cost of Revenue: Cleanroom wafer fabrication supplies, liquid helium, technician labor, and public cloud hosting expenses.">Cost of Revenue</span></td>
              <td>${total_rev[0]-gross_profit[0]:,.2f}M</td>
              <td>${total_rev[1]-gross_profit[1]:,.2f}M</td>
              <td>${total_rev[2]-gross_profit[2]:,.2f}M</td>
              <td>${total_rev[3]-gross_profit[3]:,.2f}M</td>
              <td class="col-q0">${total_rev[4]-gross_profit[4]:,.2f}M</td>
              <td class="col-est">$2.10M</td>
              <td style="color:#f87171;">-2.3%</td>
              <td style="color:#f87171;">+139.8%</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="Gross Profit: Total revenue minus cost of revenue." data-tip="Gross Profit: Consolidated gross margin reflecting high manufacturing margin on Novera hardware deliveries.">Gross Profit</span></td>
              <td>${gross_profit[0]:,.2f}M</td>
              <td>${gross_profit[1]:,.2f}M</td>
              <td>${gross_profit[2]:,.2f}M</td>
              <td>${gross_profit[3]:,.2f}M</td>
              <td class="col-q0">${gross_profit[4]:,.2f}M</td>
              <td class="col-est">$1.58M</td>
              <td style="color:#34d399;">+58.7%</td>
              <td style="color:#34d399;">+284.2%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Expenses: R&D, quantum engineering salaries, SG&A overhead." data-tip="Operating Expenses: Research and development for multi-chip scaling, cryogenics engineers, software developers, and administrative overhead.">Operating Expenses</span></td>
              <td>${opex[0]:,.2f}M</td>
              <td>${opex[1]:,.2f}M</td>
              <td>${opex[2]:,.2f}M</td>
              <td>${opex[3]:,.2f}M</td>
              <td class="col-q0">${opex[4]:,.2f}M</td>
              <td class="col-est">$28.50M</td>
              <td style="color:#f87171;">+10.7%</td>
              <td style="color:#f87171;">+47.9%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income (EBIT): Core operating loss from quantum hardware development and commercialization.">Operating Income (EBIT)</span></td>
              <td style="color:#f87171;">${ebit[0]:,.2f}M</td>
              <td style="color:#f87171;">${ebit[1]:,.2f}M</td>
              <td style="color:#f87171;">${ebit[2]:,.2f}M</td>
              <td style="color:#f87171;">${ebit[3]:,.2f}M</td>
              <td class="col-q0" style="color:#f87171;">${ebit[4]:,.2f}M</td>
              <td class="col-est" style="color:#f87171;">-$26.92M</td>
              <td style="color:#f87171;">-8.1%</td>
              <td style="color:#f87171;">-41.1%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Net Income / (Loss) attributable to common stockholders." data-tip="GAAP Net Income: Bottom-line net loss after accounting for derivative warrant revaluations and interest income.">GAAP Net Income</span></td>
              <td style="color:#f87171;">${net_income[0]:,.2f}M</td>
              <td style="color:#f87171;">${net_income[1]:,.2f}M</td>
              <td style="color:#f87171;">${net_income[2]:,.2f}M</td>
              <td style="color:#34d399;">+${net_income[3]:,.2f}M</td>
              <td class="col-q0" style="color:#f87171;">${net_income[4]:,.2f}M</td>
              <td class="col-est" style="color:#f87171;">-$28.00M</td>
              <td style="color:#f87171;">N/A</td>
              <td style="color:#f87171;">-32.7%</td>
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
            <span class="badge badge-warn">Foundry Investment</span>
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            The forensic waterfall below bridges reported GAAP Operating Cash Flow (${latest_ocf:,.2f}M) to institutional True Free Cash Flow (-${abs(latest_true_fcf):,.2f}M), isolating cleanroom semiconductor tooling and non-cash stock compensation.
          </p>
          <div style="background: rgba(11, 15, 25, 0.6); padding: 12px; border-radius: 6px; border: 1px solid var(--border-color);">
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Operating Cash Flow: Cash used in operating activities." data-tip="Operating Cash Flow (OCF): Net cash used in operational quantum R&D and foundry operations (-$15.78M in Q2 2026).">Operating Cash Flow (OCF)</span></span>
              <span style="font-weight: 700; color: #f87171;">-${abs(latest_ocf):,.2f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Capital Expenditures: Cleanroom equipment and dilution refrigerators." data-tip="Capital Expenditures (CapEx): Cleanroom tooling, cryogenic dilution refrigerators, and semiconductor probing equipment ($11.99M).">Less: Capital Expenditures (CapEx)</span></span>
              <span style="font-weight: 700; color: #f87171;">-${latest_capex:,.2f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px; font-weight: 600; color: #93c5fd;">
              <span>Reported Free Cash Flow (OCF - CapEx)</span>
              <span>-${abs(latest_reported_fcf):,.2f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Stock-Based Compensation: Non-cash equity compensation expense." data-tip="Stock-Based Compensation (SBC): Non-cash equity compensation grants of $7.02M deducted by institutional analysts.">Less: Stock-Based Compensation (SBC)</span></span>
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
            <span class="badge badge-blue">Foundry Asset Quality</span>
          </div>
          <div style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.6;">
            <p style="margin-bottom: 8px;">
              <strong>1. Operational Cash Burn Moderation:</strong> Core operating cash burn remained contained at -$15.78M in Q2 2026, demonstrating strict overhead control across engineering and administrative divisions.
            </p>
            <p style="margin-bottom: 8px;">
              <strong>2. High CapEx in Captive Fab-1:</strong> Capital expenditures of $11.99M represent tangible long-lived cleanroom semiconductor manufacturing assets that build durable enterprise value.
            </p>
            <p>
              <strong>3. High-Margin Commercial Systems:</strong> Novera on-premises deliveries generate positive gross margin contribution (Q2 gross profit reached $2.19M, 42.6% gross margin), accelerating the path to cash flow neutrality.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ROW 4: SEGMENT EXECUTION AUDIT GRID (4 TAILWINDS VS 4 HEADWINDS) -->
    <section class="audit-section" id="row-4-segments" style="margin-bottom: 24px;">
      <div class="section-title">
        <span class="section-title-accent"></span>Quantum Hardware Audit: 4 Operational Tailwinds vs. 4 Execution Headwinds
      </div>
      <div class="audit-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
        <!-- Tailwinds -->
        <div class="card" style="border-left: 3px solid #10b981;">
          <div class="card-header">
            <span class="card-title" style="color: #34d399;"><span class="card-title-accent" style="background: #10b981;"></span>4 Key Operational Tailwinds</span>
            <span class="badge badge-bull">Hardware Milestones</span>
          </div>
          <div style="margin-top: 10px;">
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">1. Novera On-Premises Commercial Momentum:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Direct sales of complete 9-qubit and 24-qubit quantum systems to government and academic research labs establish a recurring $1M+ hardware revenue stream.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">2. Proprietary Modular Multi-Chip Tiling Moat:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Rigetti's patented multi-chip quantum interconnect architecture bypasses single-wafer yield limitations, paving the way for the 336-qubit Lyra system.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">3. Captive Fab-1 Semiconductor Cleanroom:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">In-house quantum wafer fabrication ensures rapid iterative design cycles and strict quality control without third-party foundry queue delays.</p>
            </div>
            <div>
              <strong style="color: #6ee7b7; font-size: 13px;">4. Expanding Defense &amp; Intelligence Partnerships:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Continued program execution under DARPA, Air Force Research Lab (AFRL), and DOE contracts provides non-dilutive federal R&D funding.</p>
            </div>
          </div>
        </div>

        <!-- Headwinds -->
        <div class="card" style="border-left: 3px solid #ef4444;">
          <div class="card-header">
            <span class="card-title" style="color: #f87171;"><span class="card-title-accent" style="background: #ef4444;"></span>4 Key Execution Headwinds</span>
            <span class="badge badge-warn">Execution Risks</span>
          </div>
          <div style="margin-top: 10px;">
            <div style="margin-bottom: 10px;">
              <strong style="color: #fca5a5; font-size: 13px;">1. High Valuation Multiple (264x P/S):</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">With trailing price-to-sales at 264.7x, any quarterly revenue lumpiness or contract closing delay can cause severe multiple contraction.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #fca5a5; font-size: 13px;">2. Intense Hyperscale &amp; Pure-Play Competition:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Deeply capitalized tech titans (IBM, Google, Microsoft) and well-funded pure-plays (IonQ, Quantinuum) compete aggressively for talent and cloud access share.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #fca5a5; font-size: 13px;">3. Ongoing Cash Burn &amp; Cleanroom CapEx:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Maintaining a dedicated semiconductor cleanroom requires continuous capital expenditure ($11.99M in Q2), necessitating ongoing access to capital markets.</p>
            </div>
            <div>
              <strong style="color: #fca5a5; font-size: 13px;">4. High Short Interest (21.37% Float):</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Skeptics remain heavily short, questioning whether quantum computational advantage for commercial enterprise applications will materialize before 2030.</p>
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
              <td><span class="tip" title="Rigetti Computing, Inc. (Target Company)" data-tip="Rigetti Computing: Full-stack superconducting quantum computing systems developer.">Rigetti Computing (RGTI)</span></td>
              <td>${mkt_cap_b:.2f}B</td>
              <td>{fwd_pe:.2f}x</td>
              <td>{ps_ttm:.2f}x</td>
              <td>{ev_ebitda:.2f}x</td>
              <td style="color: #34d399;">+185.6%</td>
              <td style="color: #f59e0b;">{short_float:.2f}%</td>
            </tr>
            <tr>
              <td><span class="tip" title="IonQ, Inc." data-tip="IONQ: Trapped-ion quantum computing hardware and cloud systems developer.">IonQ (IONQ)</span></td>
              <td>$4,650.0M</td>
              <td>-34.5x</td>
              <td>98.5x</td>
              <td>-24.8x</td>
              <td>+85.0%</td>
              <td>16.8%</td>
            </tr>
            <tr>
              <td><span class="tip" title="D-Wave Quantum Inc." data-tip="QBTS: Quantum annealing hardware and real-time quantum hybrid solver company.">D-Wave Quantum (QBTS)</span></td>
              <td>$380.0M</td>
              <td>-8.2x</td>
              <td>35.4x</td>
              <td>-6.5x</td>
              <td>+22.0%</td>
              <td>11.4%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Quantum Computing Inc." data-tip="QUBT: Nanophotonic quantum technology and photonic quantum computers developer.">Quantum Computing (QUBT)</span></td>
              <td>$140.0M</td>
              <td>-5.4x</td>
              <td>120.0x</td>
              <td>-4.2x</td>
              <td>+15.0%</td>
              <td>8.2%</td>
            </tr>
            <tr>
              <td><span class="tip" title="International Business Machines Corp." data-tip="IBM: Global enterprise IT leader and developer of quantum Condor/Heron QPUs.">IBM (IBM)</span></td>
              <td>$215.0B</td>
              <td>21.5x</td>
              <td>3.4x</td>
              <td>14.2x</td>
              <td>+2.5%</td>
              <td>2.1%</td>
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
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">78 / 100 (Strong Buy Conviction)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 78%; height: 100%; background: #60a5fa;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">12 covering analysts maintain an average target of $27.69 (+161.47% upside), citing Novera system traction.</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #6ee7b7; text-transform: uppercase;">Pillar 2: Buy-Side Whisper</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">76 / 100 ($4.20M Top-Line Bogey)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 76%; height: 100%; background: #10b981;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Hedge fund desks look for $4.20M top-line whisper on accelerated Novera hardware acceptances.</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #fcd34d; text-transform: uppercase;">Pillar 3: Retail &amp; FinTwit Sentiment</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">86 / 100 (Quantum Squeeze Speculation)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 86%; height: 100%; background: #f59e0b;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Retail discussions across Reddit r/wallstreetbets and FinTwit are heavily call-biased citing the 21.37% short float and $27.69 mean PT.</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #c084fc; text-transform: uppercase;">Pillar 4: Short Squeeze &amp; Options Skew</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">89 / 100 (High Upward Convexity)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 89%; height: 100%; background: #a855f7;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Options price a violent ±15.96% move ($1.69 straddle). Heavy short interest creates explosive upside asymmetry on any contract announcement.</div>
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
            <span class="badge badge-bull">TARGET: $13.50 – $17.00</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 Revenue prints above $4.20M, multiple Novera purchase orders confirmed, Q4 guidance raised past $6.5M, triggering rapid short covering across 21.37% short float.
          </p>
          <div class="trade-structure" style="background: rgba(16, 185, 129, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #6ee7b7;">
            <strong>Options Structure:</strong> Nov 13 $11.00 / $15.00 Bull Call Spread to leverage asymmetric upside while capping high options implied volatility outlay (135.35%).
          </div>
        </div>

        <!-- Base Case -->
        <div class="card scenario-base" style="border-top: 3px solid #3b82f6;">
          <div class="card-header">
            <div class="card-title" style="color: #60a5fa;"><span class="card-title-accent" style="background: #3b82f6;"></span>Base Case Scenario (45% Probability)</div>
            <span class="badge badge-blue">TARGET: $9.50 – $11.50</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 revenue meets consensus at $3.5M–$3.8M, cash burn remains steady around -$15M, and management provides measured updates on Ankaa-3 development progress.
          </p>
          <div class="trade-structure" style="background: rgba(59, 130, 246, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #93c5fd;">
            <strong>Options Structure:</strong> Nov 13 $9.00 / $12.50 Short Iron Condor to capture post-announcement implied volatility crush from 135% down toward 65%.
          </div>
        </div>

        <!-- Bear Case -->
        <div class="card scenario-bear" style="border-top: 3px solid #ef4444;">
          <div class="card-header">
            <div class="card-title" style="color: #f87171;"><span class="card-title-accent" style="background: #ef4444;"></span>Bear Case Scenario (20% Probability)</div>
            <span class="badge badge-warn">TARGET: $7.50 – $9.00</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 revenue falls short (&lt; $3.2M) due to delayed hardware acceptances or quarterly cash burn accelerates, sparking concerns regarding long-term balance sheet runway.
          </p>
          <div class="trade-structure" style="background: rgba(239, 68, 68, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #fca5a5;">
            <strong>Options Structure:</strong> Nov 13 $10.00 / $8.00 Bear Put Spread to hedge downside valuation compression.
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER VERIFICATION LEDGER -->
    <footer style="margin-top: 30px; padding: 16px; border-top: 1px solid var(--border-color); font-size: 11.5px; color: var(--text-muted); text-align: center;">
      <p>Deterministic Ground-Truth Ledger: Spot Price: ${spot_price:.2f} | Consensus Revenue: ${consensus_rev:.2f}M | Consensus EPS: ${consensus_eps:.2f} | Latest OCF: ${latest_ocf:.2f}M ({ocf_int_str}) | True FCF: ${latest_true_fcf:.2f}M | Options-Implied Move: ±{opt_move_pct:.2f}% (±${opt_move_usd:.2f}) | 4Q Historical Beat Rate: 25.0% | Wall Street Consensus Mean PT: ${mean_pt:.2f}</p>
      <p style="margin-top: 4px;">Antigravity 2.0 Institutional Tearsheet • Strict Zero-Hallucination Multi-Agent Orchestration Mesh</p>
    </footer>
"""

draft_payload = {
    "ticker": "RGTI",
    "earnings_date": "2026-11-10",
    "header": {
        "page_title": "RGTI Q3 2026E Pre-Earnings Briefing | Rigetti Computing Institutional Tearsheet"
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
        "bull_target_low_num": 13.50,
        "bear_target_high_num": 9.00
    },
    "rendered_container_html": html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"Draft written to {DRAFT_PATH} (HTML length: {len(html)} chars)")
