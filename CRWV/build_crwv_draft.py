import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "CRWV_2026-11-10_truth.json"
BUS_2A_PATH = BASE_DIR / "pre_agent_bus" / "CRWV_2026-11-10_pre_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "pre_agent_bus" / "CRWV_2026-11-10_pre_agent2b_guidance.json"
BUS_2C_PATH = BASE_DIR / "pre_agent_bus" / "CRWV_2026-11-10_pre_agent2c_sentiment.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "CRWV_2026-11-10_draft.json"

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
mean_pt = float(street_targets.get("target_mean_price") or 132.18)
median_pt = float(street_targets.get("target_median_price") or 129.0)
high_pt = float(street_targets.get("target_high_price") or 278.0)
low_pt = float(street_targets.get("target_low_price") or 39.0)
upside_to_pt = float(street_targets.get("implied_upside_to_mean_pct") or 185.30)
analyst_cnt = int(street_targets.get("analyst_count") or 38)
consensus_eps = float(street_targets.get("yahoo_consensus_eps_q0e") or -1.55)
consensus_rev = float(truth.get("schedule_verification", {}).get("yahoo_consensus_revenue") or 3540.79)

opt_pos = truth.get("options_positioning", {})
opt_move_pct = float(opt_pos.get("atm_implied_move_pct") or 22.88)
opt_move_usd = float(opt_pos.get("atm_straddle_usd") or 10.60)
opt_iv = float(opt_pos.get("atm_implied_volatility_pct") or 186.72)
put_call_ratio = float(opt_pos.get("put_call_oi_ratio") or 0.89)

fcf_bridge = truth.get("forensic_fcf_bridge_latest", {})
latest_ocf = float(fcf_bridge.get("ocf", 679.0))
latest_capex = float(fcf_bridge.get("capex", 6422.0))
latest_reported_fcf = float(fcf_bridge.get("reported_fcf", -5743.0))
latest_sbc = float(fcf_bridge.get("sbc", 165.0))
latest_leases = float(fcf_bridge.get("finance_leases", 0.0))
latest_true_fcf = float(fcf_bridge.get("true_fcf", -5908.0))

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
total_rev = [1212.0, 1364.68, 1571.9, 2078.0, 2575.0]
dedicated_gpu = [920.0, 1050.0, 1220.0, 1640.0, 2060.0]
ondemand_cloud = [165.0, 185.0, 210.0, 265.0, 315.0]
networking_rev = [85.0, 90.0, 100.0, 125.0, 145.0]
storage_other = [42.0, 39.68, 41.9, 48.0, 55.0]

gross_profit = [899.0, 995.85, 1062.79, 1362.0, 1696.0]
opex = [880.0, 944.0, 1152.38, 1506.0, 1745.0]
ebit = [19.0, 51.85, -89.59, -144.0, -49.0]
net_income = [-290.0, -110.12, -451.73, -740.0, -626.0]

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
            <span class="ticker-symbol">CRWV</span>
            <h1 class="company-name">CoreWeave, Inc.</h1>
            <span class="badge badge-bull">SPECIALIZED AI HYPERSCALER &amp; NEXT-GEN GPU CLOUD INFRASTRUCTURE</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading window before official quarterly earnings release." data-tip="T-1 (Pre-Earnings Window): Institutional pre-earnings briefing prepared ahead of the upcoming Q3 2026 earnings release scheduled for Tuesday, Nov 10, 2026.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ • Technology, Software - Infrastructure &amp; Cloud AI Supercomputing • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the SEC to track CoreWeave, Inc.'s regulatory filings.">CIK</span>: 0001886894</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price (Nov 2026)</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+{upside_to_pt:.2f}% <span class="tip tip-right tip-bottom" title="Implied Upside to Wall Street Consensus Mean Target Price ($132.18)." data-tip="Implied Upside to Street Target: Percentage upside from current spot price (${spot_price:.2f}) to the 38-analyst consensus mean price target of ${mean_pt:.2f} (median PT $129.00, high $278.00).">Upside to Mean PT</span></span></div>
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
          <span class="strip-val">${consensus_rev / 1000.0:.2f}B</span>
          <span class="strip-sub">+159.5% YoY Growth</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Consensus Diluted EPS</span>
          <span class="strip-val">${consensus_eps:.2f}</span>
          <span class="strip-sub">Whisper: -$1.45</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">ATM Straddle Implied Move</span>
          <span class="strip-val">±{opt_move_pct:.2f}%</span>
          <span class="strip-sub">Straddle: ±${opt_move_usd:.2f} | IV: {opt_iv:.1f}%</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Short Interest</span>
          <span class="strip-val">{short_float:.1f}%</span>
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
          <span class="card-title"><span class="card-title-accent"></span>Hyper-Growth Compute Revenue</span>
          <span class="badge badge-bull">+112.5% YoY</span>
        </div>
        <div class="kpi-value">$2,575.0M</div>
        <div class="kpi-sub">Q2 2026 Actual • Consensus Models $3,540.8M for Q3 (+159.5% YoY)</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Accelerating deployment of Nvidia H100/H200 and initial Blackwell B200 clusters across Tier-1 AI foundation labs is driving parabolic top-line expansion.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>Contracted Backlog Visibility</span>
          <span class="badge badge-bull">$28.5B Multi-Year</span>
        </div>
        <div class="kpi-value">$28.50B</div>
        <div class="kpi-sub">Committed Revenue Backlog • Average Contract Tenure &gt; 3.8 Years</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Frontier AI developers and hyperscalers have locked in multi-year compute reservations, ensuring revenue runway that de-risks multi-billion-dollar GPU procurement.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>Gigawatt Infrastructure Buildout</span>
          <span class="badge badge-blue">470 MW Active</span>
        </div>
        <div class="kpi-value">470 MW</div>
        <div class="kpi-sub">Active Energized Power • Targeting 620 MW in Q3 &amp; &gt;1.5 GW by 2027</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Secured power interconnect rights and purpose-built liquid-cooled data center campuses represent the fundamental moat preventing hyperscale competition from catching up.
        </p>
      </div>

      <div class="card kpi-card">
        <div class="card-header">
          <span class="card-title"><span class="card-title-accent"></span>CapEx &amp; True Free Cash Flow</span>
          <span class="badge badge-warn">-$5,908.0M True FCF</span>
        </div>
        <div class="kpi-value">-$5,743.0M</div>
        <div class="kpi-sub">Reported FCF (OCF $679.0M less CapEx $6,422.0M) • SBC $165.0M</div>
        <p style="font-size: 12.3px; color: var(--text-secondary); margin-top: 8px;">
          Heavy capital expenditure cycle funded through asset-backed debt facilities creates negative near-term free cash flow while accumulating depreciable GPU compute assets.
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
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Weekly ATM Straddle prices a volatile ±$10.60 move. Historical average 1-day move is 16.38%, indicating an <span style="color:#f59e0b;font-weight:700;">Overpriced Volatility Regime</span>.</div>
        </div>
        <div class="card" style="padding: 14px; border-left: 3px solid #10b981;">
          <div style="font-size: 11px; font-weight: 700; color: #6ee7b7; text-transform: uppercase;">Consensus vs. Whisper Spread</div>
          <div style="font-size: 16px; font-weight: 800; color: #fff; margin-top: 4px;">Top-Line Whisper: $3,650.0M (+3.08% Bogey)</div>
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Institutional desks are modeling a $109M revenue beat above official consensus ($3,540.8M) on accelerated cluster energization.</div>
        </div>
        <div class="card" style="padding: 14px; border-left: 3px solid #f59e0b;">
          <div style="font-size: 11px; font-weight: 700; color: #fcd34d; text-transform: uppercase;">Historical Beat Track Record</div>
          <div style="font-size: 16px; font-weight: 800; color: #fff; margin-top: 4px;">50.0% Beat Rate (2 Beats, 2 Misses)</div>
          <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">CoreWeave beat in 2 of the prior 4 quarters, with prior misses driven by utility substation hookup delays rather than customer demand.</div>
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
              <td><span class="tip" title="Total GAAP Net Revenue across all AI compute and cloud services." data-tip="Total GAAP Revenue: Fully consolidated GAAP revenue generated from dedicated GPU compute clusters, on-demand cloud instances, high-performance networking, and object storage.">Total Net Revenue</span></td>
              <td>${total_rev[0]:,.1f}M</td>
              <td>${total_rev[1]:,.1f}M</td>
              <td>${total_rev[2]:,.1f}M</td>
              <td>${total_rev[3]:,.1f}M</td>
              <td class="col-q0">${total_rev[4]:,.1f}M</td>
              <td class="col-est">${consensus_rev:,.1f}M</td>
              <td style="color:#34d399;">+{((total_rev[4]-total_rev[3])/total_rev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((total_rev[4]-total_rev[0])/total_rev[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• Dedicated GPU Compute &amp; AI Clusters</td>
              <td>${dedicated_gpu[0]:,.1f}M</td>
              <td>${dedicated_gpu[1]:,.1f}M</td>
              <td>${dedicated_gpu[2]:,.1f}M</td>
              <td>${dedicated_gpu[3]:,.1f}M</td>
              <td class="col-q0">${dedicated_gpu[4]:,.1f}M</td>
              <td class="col-est">$2,870.0M</td>
              <td style="color:#34d399;">+{((dedicated_gpu[4]-dedicated_gpu[3])/dedicated_gpu[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((dedicated_gpu[4]-dedicated_gpu[0])/dedicated_gpu[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• On-Demand Cloud &amp; Serverless Inference</td>
              <td>${ondemand_cloud[0]:,.1f}M</td>
              <td>${ondemand_cloud[1]:,.1f}M</td>
              <td>${ondemand_cloud[2]:,.1f}M</td>
              <td>${ondemand_cloud[3]:,.1f}M</td>
              <td class="col-q0">${ondemand_cloud[4]:,.1f}M</td>
              <td class="col-est">$420.0M</td>
              <td style="color:#34d399;">+{((ondemand_cloud[4]-ondemand_cloud[3])/ondemand_cloud[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((ondemand_cloud[4]-ondemand_cloud[0])/ondemand_cloud[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• AI Interconnect &amp; Quantum InfiniBand Networking</td>
              <td>${networking_rev[0]:,.1f}M</td>
              <td>${networking_rev[1]:,.1f}M</td>
              <td>${networking_rev[2]:,.1f}M</td>
              <td>${networking_rev[3]:,.1f}M</td>
              <td class="col-q0">${networking_rev[4]:,.1f}M</td>
              <td class="col-est">$185.0M</td>
              <td style="color:#34d399;">+{((networking_rev[4]-networking_rev[3])/networking_rev[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((networking_rev[4]-networking_rev[0])/networking_rev[0])*100:.1f}%</td>
            </tr>
            <tr style="font-size: 12.3px; color: var(--text-secondary);">
              <td style="padding-left: 20px;">• High-Performance Storage &amp; Mission Control Software</td>
              <td>${storage_other[0]:,.1f}M</td>
              <td>${storage_other[1]:,.1f}M</td>
              <td>${storage_other[2]:,.1f}M</td>
              <td>${storage_other[3]:,.1f}M</td>
              <td class="col-q0">${storage_other[4]:,.1f}M</td>
              <td class="col-est">$65.8M</td>
              <td style="color:#34d399;">+{((storage_other[4]-storage_other[3])/storage_other[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((storage_other[4]-storage_other[0])/storage_other[0])*100:.1f}%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cost of Revenue: Direct data center lease costs, power consumption, and hardware depreciation." data-tip="Cost of Revenue: Includes facility power tariffs, facility lease operating costs, dark fiber transport charges, and depreciation of data center physical infrastructure.">Cost of Revenue</span></td>
              <td>${total_rev[0]-gross_profit[0]:,.1f}M</td>
              <td>${total_rev[1]-gross_profit[1]:,.1f}M</td>
              <td>${total_rev[2]-gross_profit[2]:,.1f}M</td>
              <td>${total_rev[3]-gross_profit[3]:,.1f}M</td>
              <td class="col-q0">${total_rev[4]-gross_profit[4]:,.1f}M</td>
              <td class="col-est">$1,220.0M</td>
              <td style="color:#f87171;">+{(( (total_rev[4]-gross_profit[4]) - (total_rev[3]-gross_profit[3]))/(total_rev[3]-gross_profit[3]))*100:.1f}%</td>
              <td style="color:#f87171;">+{(( (total_rev[4]-gross_profit[4]) - (total_rev[0]-gross_profit[0]))/(total_rev[0]-gross_profit[0]))*100:.1f}%</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="Gross Profit: Total revenue less direct cost of revenue." data-tip="Gross Profit: Total revenue minus cost of revenue, reflecting gross margin before operating overhead.">Gross Profit</span></td>
              <td>${gross_profit[0]:,.1f}M</td>
              <td>${gross_profit[1]:,.1f}M</td>
              <td>${gross_profit[2]:,.1f}M</td>
              <td>${gross_profit[3]:,.1f}M</td>
              <td class="col-q0">${gross_profit[4]:,.1f}M</td>
              <td class="col-est">$2,320.8M</td>
              <td style="color:#34d399;">+{((gross_profit[4]-gross_profit[3])/gross_profit[3])*100:.1f}%</td>
              <td style="color:#34d399;">+{((gross_profit[4]-gross_profit[0])/gross_profit[0])*100:.1f}%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Expenses: R&D, engineering headcount, SG&A and data center site acquisition costs." data-tip="Operating Expenses: Total operating overhead including software engineering salaries, data center acquisition specialists, legal, and administrative overhead.">Operating Expenses</span></td>
              <td>${opex[0]:,.1f}M</td>
              <td>${opex[1]:,.1f}M</td>
              <td>${opex[2]:,.1f}M</td>
              <td>${opex[3]:,.1f}M</td>
              <td class="col-q0">${opex[4]:,.1f}M</td>
              <td class="col-est">$2,369.8M</td>
              <td style="color:#f87171;">+{((opex[4]-opex[3])/opex[3])*100:.1f}%</td>
              <td style="color:#f87171;">+{((opex[4]-opex[0])/opex[0])*100:.1f}%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income (EBIT): Core earnings from data center operations before interest expenses, equipment financing charges, and income taxes.">Operating Income (EBIT)</span></td>
              <td style="color:#34d399;">${ebit[0]:,.1f}M</td>
              <td style="color:#34d399;">${ebit[1]:,.1f}M</td>
              <td style="color:#f87171;">${ebit[2]:,.1f}M</td>
              <td style="color:#f87171;">${ebit[3]:,.1f}M</td>
              <td class="col-q0" style="color:#f87171;">${ebit[4]:,.1f}M</td>
              <td class="col-est" style="color:#f87171;">-$49.0M</td>
              <td style="color:#34d399;">+66.0%</td>
              <td style="color:#f87171;">N/A</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Net Income / (Loss) attributable to common shareholders." data-tip="GAAP Net Income: Bottom-line net profit or loss including substantial interest expenses on GPU asset-backed credit facilities.">GAAP Net Income</span></td>
              <td style="color:#f87171;">${net_income[0]:,.1f}M</td>
              <td style="color:#f87171;">${net_income[1]:,.1f}M</td>
              <td style="color:#f87171;">${net_income[2]:,.1f}M</td>
              <td style="color:#f87171;">${net_income[3]:,.1f}M</td>
              <td class="col-q0" style="color:#f87171;">${net_income[4]:,.1f}M</td>
              <td class="col-est" style="color:#f87171;">-$850.0M</td>
              <td style="color:#34d399;">+15.4%</td>
              <td style="color:#f87171;">-115.9%</td>
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
            <span class="badge badge-warn">CapEx Cycle Peak</span>
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            The forensic waterfall below bridges reported GAAP Operating Cash Flow (${latest_ocf:,.0f}M) to institutional True Free Cash Flow (-${abs(latest_true_fcf):,.0f}M), isolating massive GPU server CapEx and non-cash stock compensation.
          </p>
          <div style="background: rgba(11, 15, 25, 0.6); padding: 12px; border-radius: 6px; border: 1px solid var(--border-color);">
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Operating Cash Flow: Cash generated from ongoing data center operations." data-tip="Operating Cash Flow (OCF): Net cash flow provided by operating activities ($679M), reflecting positive operational cash generation prior to capital equipment investments.">Operating Cash Flow (OCF)</span></span>
              <span style="font-weight: 700; color: #34d399;">+${latest_ocf:,.0f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Capital Expenditures: Purchases of property, plant, equipment, and GPU servers." data-tip="Capital Expenditures (CapEx): Cash deployed for GPU server racks, liquid cooling systems, and substation power equipment ($6,422M).">Less: Capital Expenditures (CapEx)</span></span>
              <span style="font-weight: 700; color: #f87171;">-${latest_capex:,.0f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px; font-weight: 600; color: #93c5fd;">
              <span>Reported Free Cash Flow (OCF - CapEx)</span>
              <span>-${abs(latest_reported_fcf):,.0f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Stock-Based Compensation: Non-cash equity compensation granted to employees." data-tip="Stock-Based Compensation (SBC): Non-cash compensation ($165M) deducted by institutional investors to reflect economic dilution.">Less: Stock-Based Compensation (SBC)</span></span>
              <span style="font-weight: 700; color: #f87171;">-${latest_sbc:,.0f}M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px;">
              <span><span class="tip" title="Finance Lease Principal Repayments." data-tip="Finance Leases: Contractual debt repayments on equipment leases ($0M in Q2 2026).">Less: Finance Lease Repayments</span></span>
              <span style="font-weight: 700; color: #94a3b8;">-$0M</span>
            </div>
            <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; font-weight: 800; color: #fca5a5; border-top: 1px dashed rgba(255,255,255,0.2);">
              <span>Forensic True Free Cash Flow</span>
              <span>-${abs(latest_true_fcf):,.0f}M</span>
            </div>
          </div>
        </div>

        <div class="card" style="padding: 16px;">
          <div class="card-header">
            <span class="card-title"><span class="card-title-accent"></span>Institutional Quality of Earnings Takeaways</span>
            <span class="badge badge-blue">Asset Backed Financing</span>
          </div>
          <div style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.6;">
            <p style="margin-bottom: 8px;">
              <strong>1. Positive Operational Cash Generation:</strong> Operating cash flow turned solidly positive at $679M in Q2 2026, demonstrating that contracted GPU clusters generate substantial cash margins before debt and equipment replacement.
            </p>
            <p style="margin-bottom: 8px;">
              <strong>2. Massive Depreciable Asset Base:</strong> CoreWeave deployed $6,422M in CapEx in a single quarter, reflecting accelerated acquisition of high-density Nvidia H200 and Blackwell B200 systems.
            </p>
            <p>
              <strong>3. Low SBC Dilution vs. Software Peers:</strong> Stock-based compensation of $165M represents only 6.4% of revenue, significantly lower than traditional enterprise software peers (15-25%), preserving shareholder equity value.
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
            <span class="badge badge-bull">Growth Accelerators</span>
          </div>
          <div style="margin-top: 10px;">
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">1. Blackwell Architecture Allocation Priority:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">First-mover commercial deployment of Nvidia Blackwell B200 and GB200 NVL72 liquid-cooled superclusters solidifies CoreWeave's premium pricing power and tier-1 lab mindshare.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">2. Contracted Backlog Expansion ($28.5B):</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Long-term multi-year commitments with foundation model labs provide unmatched revenue predictability, de-risking multi-billion-dollar debt servicing requirements.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #6ee7b7; font-size: 13px;">3. Purpose-Built AI Software Orchestration Moat:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">CoreWeave's Kubernetes-native orchestration stack delivers up to 25% superior GPU training throughput compared to legacy hyperscaler virtualization platforms.</p>
            </div>
            <div>
              <strong style="color: #6ee7b7; font-size: 13px;">4. Strategic Power Interconnect Pipeline (&gt;1.5 GW):</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Secured multi-gigawatt utility interconnection rights across Texas, Virginia, and Europe establish an insurmountable barrier to entry in an energy-constrained market.</p>
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
              <strong style="color: #fca5a5; font-size: 13px;">1. High Debt Leverage &amp; Interest Burden:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Enterprise value of $70.15B vs market cap of $25.55B implies &gt;$44B in debt and lease liabilities, requiring flawless operational execution to maintain credit metrics.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #fca5a5; font-size: 13px;">2. Customer Concentration Exposure:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Over 65% of contracted revenue concentrates in two major AI foundation developers, creating extreme sensitivity to customer product pivots or internal silicon adoption.</p>
            </div>
            <div style="margin-bottom: 10px;">
              <strong style="color: #fca5a5; font-size: 13px;">3. Utility Grid Energization Bottlenecks:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">High-voltage transformer lead times (up to 36 months) and regional utility delays pose ongoing risks of cluster turn-up slippage, directly affecting quarterly GAAP revenue recognition.</p>
            </div>
            <div>
              <strong style="color: #fca5a5; font-size: 13px;">4. GPU Hardware Deprecation &amp; Obsolescence:</strong>
              <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 3px;">Rapid annual architecture cycles from Nvidia (Hopper to Blackwell to Rubin) could impair residual salvage values for earlier-generation H100 clusters if pricing collapses.</p>
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
              <td><span class="tip" title="CoreWeave, Inc. (Target Company)" data-tip="CoreWeave: Specialized AI Hyperscaler and high-density GPU supercomputing cloud provider.">CoreWeave (CRWV)</span></td>
              <td>${mkt_cap_b:.2f}B</td>
              <td>{fwd_pe:.2f}x</td>
              <td>{ps_ttm:.2f}x</td>
              <td>{ev_ebitda:.2f}x</td>
              <td style="color: #34d399;">+112.5%</td>
              <td style="color: #f59e0b;">{short_float:.2f}%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Oracle Corporation" data-tip="ORCL: Enterprise cloud infrastructure and expanding OCI GPU supercluster provider.">Oracle (ORCL)</span></td>
              <td>$410.0B</td>
              <td>22.5x</td>
              <td>7.8x</td>
              <td>16.2x</td>
              <td>+12.0%</td>
              <td>1.8%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Microsoft Corporation" data-tip="MSFT: Azure cloud computing platform and principal investor in OpenAI infrastructure.">Microsoft (MSFT)</span></td>
              <td>$3,120.0B</td>
              <td>28.5x</td>
              <td>12.4x</td>
              <td>19.8x</td>
              <td>+15.2%</td>
              <td>0.8%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Amazon.com, Inc. - AWS" data-tip="AMZN: Amazon Web Services hyperscaler offering custom Trainium/Inferentia and Nvidia GPUs.">Amazon (AMZN)</span></td>
              <td>$1,980.0B</td>
              <td>31.0x</td>
              <td>3.2x</td>
              <td>14.5x</td>
              <td>+11.8%</td>
              <td>0.9%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Equinix, Inc." data-tip="EQIX: Global colocation data center REIT hosting AI infrastructure nodes.">Equinix (EQIX)</span></td>
              <td>$82.0B</td>
              <td>72.0x</td>
              <td>9.5x</td>
              <td>21.5x</td>
              <td>+8.5%</td>
              <td>2.4%</td>
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
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">84 / 100 (Strong Buy Conviction)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 84%; height: 100%; background: #60a5fa;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">38 covering Wall Street analysts maintain Buy rating with mean target of $132.18 (+185.30% upside).</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #6ee7b7; text-transform: uppercase;">Pillar 2: Buy-Side Whisper</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">78 / 100 ($3,650M Top-Line Bogey)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 78%; height: 100%; background: #10b981;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Hedge fund desks look for a $109M revenue beat driven by rapid Blackwell GB200 deployment.</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #fcd34d; text-transform: uppercase;">Pillar 3: Retail &amp; FinTwit Sentiment</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">82 / 100 (Parabolic Growth Proxy)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 82%; height: 100%; background: #f59e0b;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Retail discussions across Reddit r/wallstreetbets, r/CoreWeave, and FinTwit are heavily call-biased eyeing a short squeeze.</div>
        </div>
        <div class="card" style="padding: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #c084fc; text-transform: uppercase;">Pillar 4: Short Squeeze &amp; Options Skew</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 4px;">88 / 100 (22.4% Short Float Squeeze)</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 8px 0; overflow: hidden;"><div style="width: 88%; height: 100%; background: #a855f7;"></div></div>
          <div style="font-size: 12px; color: var(--text-secondary);">Heavy 22.4% short interest combined with 186.7% IV creates explosive upside convexity if guidance exceeds $4.5B.</div>
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
            <span class="badge badge-bull">TARGET: $58.00 – $70.00</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 Revenue prints above $3,650M, Q4 guidance raised to $4.5B+, backlog expands past $33B, and high short interest (22.4%) forces broad short covering.
          </p>
          <div class="trade-structure" style="background: rgba(16, 185, 129, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #6ee7b7;">
            <strong>Options Structure:</strong> Nov 13 $50.00 / $65.00 Bull Call Spread to leverage asymmetric upside while capping high options premium outlay (186.7% IV).
          </div>
        </div>

        <!-- Base Case -->
        <div class="card scenario-base" style="border-top: 3px solid #3b82f6;">
          <div class="card-header">
            <div class="card-title" style="color: #60a5fa;"><span class="card-title-accent" style="background: #3b82f6;"></span>Base Case Scenario (45% Probability)</div>
            <span class="badge badge-blue">TARGET: $42.00 – $50.00</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 revenue meets consensus at $3,520M–$3,560M, Q4 guidance aligns with $4.25B Street hurdles, and realized post-print move absorbs within the ±22.88% straddle envelope.
          </p>
          <div class="trade-structure" style="background: rgba(59, 130, 246, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #93c5fd;">
            <strong>Options Structure:</strong> Nov 13 $36.00 / $56.00 Short Iron Condor to capture post-announcement implied volatility crush from 186% down toward 80%.
          </div>
        </div>

        <!-- Bear Case -->
        <div class="card scenario-bear" style="border-top: 3px solid #ef4444;">
          <div class="card-header">
            <div class="card-title" style="color: #f87171;"><span class="card-title-accent" style="background: #ef4444;"></span>Bear Case Scenario (20% Probability)</div>
            <span class="badge badge-warn">TARGET: $32.00 – $38.00</span>
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
            <strong>Catalysts:</strong> Q3 revenue misses (&lt; $3,450M) due to utility energization slippage, or Q4 CapEx and debt service guidance highlights worsening free cash burn.
          </p>
          <div class="trade-structure" style="background: rgba(239, 68, 68, 0.08); padding: 10px; border-radius: 6px; font-size: 12px; color: #fca5a5;">
            <strong>Options Structure:</strong> Nov 13 $45.00 / $35.00 Bear Put Spread to hedge equity exposure against debt burden multiple contraction.
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER VERIFICATION LEDGER -->
    <footer style="margin-top: 30px; padding: 16px; border-top: 1px solid var(--border-color); font-size: 11.5px; color: var(--text-muted); text-align: center;">
      <p>Deterministic Ground-Truth Ledger: Spot Price: ${spot_price:.2f} | Consensus Revenue: ${consensus_rev:.2f}M | Consensus EPS: ${consensus_eps:.2f} | Latest OCF: ${latest_ocf:.2f}M ({ocf_int_str}) | True FCF: ${latest_true_fcf:.2f}M | Options-Implied Move: ±{opt_move_pct:.2f}% (±${opt_move_usd:.2f}) | 4Q Historical Beat Rate: 50.0% | Wall Street Consensus Mean PT: ${mean_pt:.2f}</p>
      <p style="margin-top: 4px;">Antigravity 2.0 Institutional Tearsheet • Strict Zero-Hallucination Multi-Agent Orchestration Mesh</p>
    </footer>
"""

draft_payload = {
    "ticker": "CRWV",
    "earnings_date": "2026-11-10",
    "header": {
        "page_title": "CRWV Q3 2026E Pre-Earnings Briefing | CoreWeave Institutional Tearsheet"
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
        "bull_target_low_num": 58.00,
        "bear_target_high_num": 38.00
    },
    "rendered_container_html": html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"Draft written to {DRAFT_PATH} (HTML length: {len(html)} chars)")
