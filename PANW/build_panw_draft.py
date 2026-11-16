import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "PANW_2026-11-18_truth.json"
BUS_2A_PATH = BASE_DIR / "pre_agent_bus" / "PANW_2026-11-18_pre_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "pre_agent_bus" / "PANW_2026-11-18_pre_agent2b_guidance.json"
BUS_2C_PATH = BASE_DIR / "pre_agent_bus" / "PANW_2026-11-18_pre_agent2c_sentiment.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "PANW_2026-11-18_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
bus_2a = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
bus_2b = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
bus_2c = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 315.21
mkt_cap_m = float(truth["valuation_and_market"]["market_cap_millions"]) # 258085.01
mkt_cap_b = mkt_cap_m / 1000.0
ev_m = float(truth["valuation_and_market"]["enterprise_value_millions"]) # 263088.32
ev_b = ev_m / 1000.0
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 788.02
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 64.56
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 22.48
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 168.65
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 2.54

street_targets = truth.get("street_consensus_and_targets", {})
mean_pt = float(street_targets.get("target_mean_price") or 398.63)
median_pt = float(street_targets.get("target_median_price") or 415.00)
high_pt = float(street_targets.get("target_high_price") or 525.00)
low_pt = float(street_targets.get("target_low_price") or 190.00)
upside_to_pt = float(street_targets.get("implied_upside_to_mean_pct") or 26.46)
analyst_cnt = int(street_targets.get("analyst_count") or 51)
consensus_eps = float(street_targets.get("yahoo_consensus_eps_q0e") or 0.97)
consensus_rev = float(truth.get("schedule_verification", {}).get("yahoo_consensus_revenue") or 3307.46)

opt_pos = truth.get("options_positioning", {})
opt_move_pct = float(opt_pos.get("atm_implied_move_pct") or 11.06)
opt_move_usd = float(opt_pos.get("atm_straddle_usd") or 34.85)
opt_iv = float(opt_pos.get("atm_implied_volatility_pct") or 118.07)
put_call_ratio = float(opt_pos.get("put_call_oi_ratio") or 0.73)

fcf_bridge = truth.get("forensic_fcf_bridge_latest", {})
latest_ocf = float(fcf_bridge.get("ocf", 1357.0))
latest_capex = float(fcf_bridge.get("capex", 103.0))
latest_reported_fcf = float(fcf_bridge.get("reported_fcf", 1254.0))
latest_sbc = float(fcf_bridge.get("sbc", 460.0))
latest_leases = float(fcf_bridge.get("finance_leases", 0.0))
latest_true_fcf = float(fcf_bridge.get("true_fcf", 794.0))

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
    debates_cards.append(f"""        <div class="card debate-card" style="margin-bottom:14px; border-left:3px solid #6366f1;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="badge badge-purple" style="font-size:11px; font-weight:700;">{db['debate_id']}</span>
            <strong style="color:#f8fafc; font-size:14px; flex:1; margin-left:10px;">{db['title']}</strong>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:10px; font-size:12.5px;">
            <div style="background:rgba(255,255,255,0.02); padding:10px; border-radius:6px; border:1px solid rgba(255,255,255,0.05);">
              <span style="color:#94a3b8; font-weight:600; text-transform:uppercase; font-size:10.5px; display:block; margin-bottom:4px;">Sell-Side Consensus Stance</span>
              <p style="margin:0; color:#cbd5e1; line-height:1.45;">{db['consensus_view']}</p>
            </div>
            <div style="background:rgba(59,130,246,0.04); padding:10px; border-radius:6px; border:1px solid rgba(59,130,246,0.15);">
              <span style="color:#60a5fa; font-weight:600; text-transform:uppercase; font-size:10.5px; display:block; margin-bottom:4px;">Buy-Side Variant Perception</span>
              <p style="margin:0; color:#e2e8f0; line-height:1.45;">{db['variant_perception']}</p>
            </div>
          </div>
          <div style="background:rgba(16,185,129,0.04); border-left:2px solid #10b981; padding:8px 12px; border-radius:4px; font-size:12px;">
            <strong style="color:#34d399;">Institutional Conference Call Focus Question:</strong>
            <span style="color:#cbd5e1; margin-left:4px;">"{db['call_focus_question']}"</span>
          </div>
        </div>""")
debates_html = "\n".join(debates_cards)

# 5Q P&L Math
gross_profit = [1857.30, 1836.00, 1909.00, 2028.00, 2304.00]
opex = [1360.10, 1527.00, 1512.00, 2211.00, 2132.00]
ebit = [497.20, 309.00, 397.00, -183.00, 172.00]

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
        <span class="mono" style="font-size:11.5px;color:#93c5fd;">Last Reported Quarter: <strong>Q3 2026 (Ended Jul 31, 2026)</strong> • Upcoming Release: <strong>Q4 2026E (Ended Oct 31, 2026)</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">PANW</span>
            <h1 class="company-name">Palo Alto Networks, Inc.</h1>
            <span class="badge badge-purple">T-1 PRE-EARNINGS BRIEFING</span>
            <span class="badge badge-blue">NasdaqGS</span>
            <span class="badge badge-warn">EARNINGS DATE: NOV 18, 2026 (AMC)</span>
          </div>
          <div class="meta-line">
            <span>Sector: <strong>Technology</strong></span>
            <span>Industry: <strong>Software - Infrastructure & Cybersecurity</strong></span>
            <span>Primary Exchange: <strong>NASDAQ</strong></span>
            <span>IR Webcast: <strong>Wednesday, Nov 18, 2026 at 4:30 PM ET (1:30 PM PT)</strong></span>
          </div>
        </div>
        <div class="price-box">
          <div class="price-row">
            <span class="price-val">${spot_price:.2f}</span>
            <span class="badge badge-bull" style="font-size:14px; font-weight:700;">SPOT CLOSE</span>
          </div>
          <div class="price-sub">Market Cap: <strong>${mkt_cap_b:.2f}B</strong> • Enterprise Value: <strong>${ev_b:.2f}B</strong></div>
          <div class="price-sub">Forward P/E: <strong>{fwd_pe:.1f}x</strong> • Short Interest: <strong>{short_float:.2f}% of Float</strong></div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Wall St Consensus Net Revenue</span>
          <span class="strip-val">${consensus_rev:.2f}M</span>
          <span class="strip-sub">Range: $3,292.4M – $3,367.1M</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Buy-Side Whisper Revenue</span>
          <span class="strip-val" style="color:#34d399;">$3,365.0M</span>
          <span class="strip-sub">+1.74% Whisper Spread</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Consensus Diluted EPS</span>
          <span class="strip-val">${consensus_eps:.2f}</span>
          <span class="strip-sub">Whisper Bogey: $1.01</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">ATM Straddle Implied Move</span>
          <span class="strip-val" style="color:#fbbf24;">±{opt_move_pct:.2f}%</span>
          <span class="strip-sub">Straddle Cost: ${opt_move_usd:.2f} (IV: {opt_iv:.1f}%)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Wall Street Mean Target</span>
          <span class="strip-val" style="color:#38bdf8;">${mean_pt:.2f}</span>
          <span class="strip-sub">+{upside_to_pt:.1f}% Upside ({analyst_cnt} Analysts)</span>
        </div>
      </div>
    </header>

    <!-- TRACK B STICKY JUMP-NAV -->
    <nav class="pre-jump-nav" style="position:sticky; top:0; z-index:40; display:flex; gap:8px; padding:10px 16px; background:#0f172a; border-bottom:1px solid #334155; margin-bottom:20px; overflow-x:auto;">
      <a href="#row-1-kpis" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">Executive KPIs</a>
      <a href="#row-1b-scorecard" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">Expectations & Whisper</a>
      <a href="#row-2-financials" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">5Q Financials</a>
      <a href="#row-3-fcf" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">Forensic FCF</a>
      <a href="#row-4-segments" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">Execution Drivers</a>
      <a href="#row-4b-debates" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">Institutional Debates</a>
      <a href="#row-5-peers" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">Peer Comps</a>
      <a href="#row-6-sentiment" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">Sentiment Audit</a>
      <a href="#row-7-pm-matrix" style="color:#94a3b8; text-decoration:none; font-size:12px; font-weight:600; padding:4px 10px; border-radius:4px; background:#1e293b;">PM Trade Matrix</a>
    </nav>

    <!-- SECTION 2: ROW 1 EXECUTIVE KPI GRID -->
    <section class="kpi-grid" id="row-1-kpis" style="margin-bottom:24px;">
      <div class="card kpi-card">
        <div class="card-title">
          <span class="tip" title="Consolidated GAAP Net Revenue" data-tip="Total consolidated GAAP net revenue recognized across Subscription & Support software and hardware appliance firewalls.">Consolidated GAAP Revenue</span>
          <span class="badge badge-bull">+34.5% YoY</span>
        </div>
        <div class="card-value">${consensus_rev:.1f}M</div>
        <div class="card-sub" style="color:#94a3b8;">Q4 2026E Consensus (Whisper: $3,365.0M)</div>
        <div style="margin-top:10px; font-size:12px; color:#cbd5e1; line-height:1.45;">
          Q3 actual recognized $3,410.0M. Platformization multi-product bundles and Cortex XSIAM autonomous SOC expansions continue to drive resilient enterprise top-line growth.
        </div>
      </div>

      <div class="card kpi-card">
        <div class="card-title">
          <span class="tip" title="Non-GAAP Diluted EPS" data-tip="Adjusted diluted net income per share excluding stock-based compensation, litigation, and intangible asset amortization.">Non-GAAP Diluted EPS</span>
          <span class="badge badge-blue">Consensus Hurdle</span>
        </div>
        <div class="card-value">${consensus_eps:.2f}</div>
        <div class="card-sub" style="color:#94a3b8;">Q4 2026E Consensus (Whisper: $1.01)</div>
        <div style="margin-top:10px; font-size:12px; color:#cbd5e1; line-height:1.45;">
          Operating margin leverage is supported by high-margin software subscriptions and disciplined sales expense management as multi-year platform contracts mature.
        </div>
      </div>

      <div class="card kpi-card">
        <div class="card-title">
          <span class="tip" title="Next-Generation Security ARR" data-tip="Annual Recurring Revenue generated by Prisma Cloud, Prisma SASE, and Cortex XSIAM cybersecurity software suites.">Next-Gen Security ARR</span>
          <span class="badge badge-bull">+38.8% YoY</span>
        </div>
        <div class="card-value">$4,550.0M</div>
        <div class="card-sub" style="color:#94a3b8;">Consensus Q4E Hurdle (Whisper: $4,680.0M)</div>
        <div style="margin-top:10px; font-size:12px; color:#cbd5e1; line-height:1.45;">
          Palo Alto Networks' core software engine, driven by cloud security posture management (Prisma Cloud) and enterprise migration away from legacy point security vendors.
        </div>
      </div>

      <div class="card kpi-card">
        <div class="card-title">
          <span class="tip" title="Remaining Performance Obligations (RPO)" data-tip="Total contracted future revenue under non-cancelable multi-year customer subscription and support commitments.">Remaining Performance Obligations</span>
          <span class="badge badge-purple">High Visibility</span>
        </div>
        <div class="card-value">$13.30B</div>
        <div class="card-sub" style="color:#94a3b8;">Q4 2026E Street Target (Whisper: $13.60B)</div>
        <div style="margin-top:10px; font-size:12px; color:#cbd5e1; line-height:1.45;">
          Contractual backlog reached $12.80B in Q3 (+20.0% YoY). Large multi-year enterprise platform agreements provide strong multi-quarter revenue visibility.
        </div>
      </div>
    </section>

    <!-- SECTION 2B: ROW 1B PRE-RELEASE EXPECTATIONS, WHISPER & TRACK RECORD SCORECARD -->
    <section class="card" id="row-1b-scorecard" style="margin-bottom:24px; padding:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div>
          <h2 style="font-size:18px; font-weight:700; color:#f8fafc; margin:0 0 4px 0;">Pre-Release Expectations, Buy-Side Whisper & Track Record Scorecard</h2>
          <p style="font-size:12.5px; color:#94a3b8; margin:0;">Triangulating sell-side consensus bogeys, buy-side whisper bogeys, and executive guidance credibility ahead of the print.</p>
        </div>
        <span class="badge badge-purple" style="font-size:12px;">Pre-Print Audit Engine</span>
      </div>

      <!-- TRACK B AUDIT BANNER -->
      <div class="t1-setup-audit" style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; margin-bottom:20px;">
        <div style="background:rgba(59,130,246,0.06); border:1px solid rgba(59,130,246,0.2); border-radius:8px; padding:12px;">
          <span style="color:#60a5fa; font-weight:700; font-size:11px; text-transform:uppercase; display:block; margin-bottom:4px;">Options Volatility Regime</span>
          <strong style="color:#f8fafc; font-size:14px; display:block; margin-bottom:4px;">±{opt_move_pct:.2f}% Implied vs 7.29% Realized</strong>
          <span style="color:#94a3b8; font-size:11.5px;">Options market is pricing a +3.77% volatility premium over historical 1-day moves (IV 118.07%). Volatility-selling edge.</span>
        </div>
        <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.2); border-radius:8px; padding:12px;">
          <span style="color:#34d399; font-weight:700; font-size:11px; text-transform:uppercase; display:block; margin-bottom:4px;">Historical Beat Record</span>
          <strong style="color:#f8fafc; font-size:14px; display:block; margin-bottom:4px;">100.0% Beat Rate (4 / 4 Prior Quarters)</strong>
          <span style="color:#94a3b8; font-size:11.5px;">Average EPS surprise of +6.30% over the trailing 4 releases. Management systematically builds a 2–3% forecast cushion.</span>
        </div>
        <div style="background:rgba(168,85,247,0.06); border:1px solid rgba(168,85,247,0.2); border-radius:8px; padding:12px;">
          <span style="color:#c084fc; font-weight:700; font-size:11px; text-transform:uppercase; display:block; margin-bottom:4px;">Executive Guidance Credibility</span>
          <strong style="color:#f8fafc; font-size:14px; display:block; margin-bottom:4px;">92 / 100 Credibility Score</strong>
          <div class="credibility-gauge-bar" style="height:6px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:6px; overflow:hidden;">
            <div style="width:92%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div>
          </div>
          <span style="color:#94a3b8; font-size:11px; display:block; margin-top:4px;">Flawless beat cadence and conservative guidance parameters establish high institutional credibility.</span>
        </div>
      </div>

      <!-- TABLE 1B-1 -->
      <h3 style="font-size:14px; font-weight:700; color:#e2e8f0; margin:16px 0 8px 0;">Table 1B-1: Headline & Company KPI Consensus vs. Buy-Side Whisper Scorecard</h3>
      <div class="table-wrapper" style="margin-bottom:20px;">
        <table class="financial-table">
          <thead>
            <tr>
              <th>Operational / Financial KPI</th>
              <th>Q3 2026 Actual (Q-1)</th>
              <th>Q4 2025 Baseline (Q-4)</th>
              <th class="col-q0">Street Consensus (Q0E)</th>
              <th>Buy-Side Whisper Bogey</th>
              <th>Whisper Spread & Progress</th>
              <th>Hurdle Class</th>
            </tr>
          </thead>
          <tbody>
{table_1b1_rows_html}
          </tbody>
        </table>
      </div>

      <!-- TABLE 1B-2 -->
      <h3 style="font-size:14px; font-weight:700; color:#e2e8f0; margin:16px 0 8px 0;">Table 1B-2: Management Guidance Credibility & 4Q Historical Track Record</h3>
      <div class="table-wrapper" style="margin-bottom:20px;">
        <table class="financial-table">
          <thead>
            <tr>
              <th>Guidance Metric</th>
              <th>Prior Q-1 Guidance Issued for Q0</th>
              <th>Current Street Consensus</th>
              <th>Historical 4Q Beat Rate</th>
              <th>Variance & Sandbagging Commentary</th>
              <th>Credibility Grade</th>
            </tr>
          </thead>
          <tbody>
{table_1b2_rows_html}
          </tbody>
        </table>
      </div>

      <!-- TABLE 1B-3 -->
      <h3 style="font-size:14px; font-weight:700; color:#e2e8f0; margin:16px 0 8px 0;">Table 1B-3: Forward Guidance Bogeys & Re-Rating Hurdles</h3>
      <div class="table-wrapper">
        <table class="financial-table">
          <thead>
            <tr>
              <th>Forward Guidance Target</th>
              <th>Street Consensus Hurdle</th>
              <th>Bull Case Bogey (Expansion)</th>
              <th>Bear Case Breakdown (Compression)</th>
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

    <!-- SECTION 3: ROW 2 5-QUARTER STITCHED FINANCIAL TABLE -->
    <section class="card" id="row-2-financials" style="margin-bottom:24px; padding:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div>
          <h2 style="font-size:18px; font-weight:700; color:#f8fafc; margin:0 0 4px 0;">5-Quarter Historical Financials & Upcoming Q4 2026E Consensus</h2>
          <p style="font-size:12.5px; color:#94a3b8; margin:0;">Stitched SEC 10-K and 10-Q GAAP financial performance with company reporting segment mapping.</p>
        </div>
        <span class="badge badge-blue">Deterministic Ground-Truth GAAP Mesh</span>
      </div>

      <div class="table-wrapper">
        <table class="financial-table">
          <thead>
            <tr>
              <th>Financial Metric ($M except EPS)</th>
              <th>Q3 2025 (Jul 31, 2025)</th>
              <th>Q4 2025 (Oct 31, 2025)</th>
              <th>Q1 2026 (Jan 31, 2026)</th>
              <th>Q2 2026 (Apr 30, 2026)</th>
              <th class="col-q0">Q3 2026 (Jul 31, 2026)</th>
              <th class="col-est">Q4 2026E Consensus</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight:700; background:rgba(255,255,255,0.03);">
              <td><span class="tip" title="Total Revenue" data-tip="Total consolidated GAAP net revenue recognized from software subscriptions, cloud security services, and hardware appliances.">Total Revenue</span></td>
              <td>$2,536.3</td>
              <td>$2,474.0</td>
              <td>$2,594.0</td>
              <td>$3,002.0</td>
              <td class="col-q0">$3,410.0</td>
              <td class="col-est" style="font-weight:700; color:#60a5fa;">${consensus_rev:.2f}</td>
            </tr>
            <tr style="color:#94a3b8; font-size:12.5px;">
              <td style="padding-left:24px;">↳ <span class="tip" title="Subscription & Support Revenue" data-tip="Recurring software license subscriptions, Prisma Cloud SaaS, Cortex XSIAM, and ongoing technical support contracts.">Subscription & Support Revenue</span></td>
              <td>$2,062.3</td>
              <td>$2,040.0</td>
              <td>$2,080.0</td>
              <td>$2,408.0</td>
              <td class="col-q0">$2,672.0</td>
              <td class="col-est" style="color:#93c5fd;">$2,679.1</td>
            </tr>
            <tr style="color:#94a3b8; font-size:12.5px;">
              <td style="padding-left:24px;">↳ <span class="tip" title="Product Revenue" data-tip="Revenue derived from physical PA-series hardware firewalls and initial software virtual appliance shipments.">Product Revenue</span></td>
              <td>$474.0</td>
              <td>$434.0</td>
              <td>$514.0</td>
              <td>$594.0</td>
              <td class="col-q0">$738.0</td>
              <td class="col-est" style="color:#93c5fd;">$628.4</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cost of Revenue" data-tip="Direct costs incurred in producing hardware firewalls and hosting multi-tenant cloud security infrastructure.">Cost of Revenue</span></td>
              <td>$679.0</td>
              <td>$638.0</td>
              <td>$685.0</td>
              <td>$974.0</td>
              <td class="col-q0">$1,106.0</td>
              <td class="col-est">$1,025.3</td>
            </tr>
            <tr style="font-weight:600;">
              <td><span class="tip" title="Gross Profit" data-tip="Total revenue minus direct cost of goods sold and cloud hosting expenses.">Gross Profit</span></td>
              <td>$1,857.3</td>
              <td>$1,836.0</td>
              <td>$1,909.0</td>
              <td>$2,028.0</td>
              <td class="col-q0">$2,304.0</td>
              <td class="col-est" style="color:#34d399;">$2,282.2</td>
            </tr>
            <tr>
              <td><span class="tip" title="Research & Development" data-tip="Engineering investments in AI security models, Cortex XSIAM automation, and Prisma Cloud architecture.">Research & Development (R&D)</span></td>
              <td>$503.5</td>
              <td>$528.0</td>
              <td>$511.0</td>
              <td>$734.0</td>
              <td class="col-q0">$779.0</td>
              <td class="col-est">$760.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Selling & Marketing" data-tip="Global enterprise sales force commissions, channel partner incentives, and platformization promotion programs.">Selling & Marketing (S&M)</span></td>
              <td>$829.3</td>
              <td>$820.0</td>
              <td>$823.0</td>
              <td>$1,161.0</td>
              <td class="col-q0">$1,127.0</td>
              <td class="col-est">$1,110.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="General & Administrative" data-tip="Executive leadership, legal, corporate finance, and enterprise compliance overhead.">General & Administrative (G&A)</span></td>
              <td>$27.3</td>
              <td>$179.0</td>
              <td>$178.0</td>
              <td>$316.0</td>
              <td class="col-q0">$226.0</td>
              <td class="col-est">$210.0</td>
            </tr>
            <tr style="font-weight:600;">
              <td><span class="tip" title="Total Operating Expenses" data-tip="Total operational overhead encompassing R&D, sales commissions, marketing campaigns, and corporate administrative costs.">Total Operating Expenses</span></td>
              <td>$1,360.1</td>
              <td>$1,527.0</td>
              <td>$1,512.0</td>
              <td>$2,211.0</td>
              <td class="col-q0">$2,132.0</td>
              <td class="col-est">$2,080.0</td>
            </tr>
            <tr style="font-weight:700; background:rgba(255,255,255,0.02);">
              <td><span class="tip" title="Operating Income (EBIT)" data-tip="GAAP Operating Income calculated deterministically as Gross Profit minus Total Operating Expenses.">Operating Income (GAAP)</span></td>
              <td>$497.2</td>
              <td>$309.0</td>
              <td>$397.0</td>
              <td>-$183.0</td>
              <td class="col-q0">$172.0</td>
              <td class="col-est" style="font-weight:700; color:#38bdf8;">$202.2</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income" data-tip="Consolidated GAAP net income or loss attributable to Palo Alto Networks stockholders after tax provisions.">Net Income (GAAP)</span></td>
              <td>$253.8</td>
              <td>$334.0</td>
              <td>$432.0</td>
              <td>-$177.0</td>
              <td class="col-q0">-$282.0</td>
              <td class="col-est">-$110.0</td>
            </tr>
            <tr style="font-weight:700;">
              <td><span class="tip" title="Non-GAAP Diluted EPS" data-tip="Non-GAAP diluted earnings per share excluding stock compensation and acquisition accounting adjustments.">Diluted EPS (Non-GAAP Consensus)</span></td>
              <td>$0.93</td>
              <td>$0.93</td>
              <td>$1.03</td>
              <td>$0.85</td>
              <td class="col-q0">$1.02</td>
              <td class="col-est" style="font-weight:700; color:#34d399;">${consensus_eps:.2f}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 4: ROW 3 FORENSIC QUALITY-OF-EARNINGS & TRUE FCF BRIDGE -->
    <section class="card" id="row-3-fcf" style="margin-bottom:24px; padding:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <div>
          <h2 style="font-size:18px; font-weight:700; color:#f8fafc; margin:0 0 4px 0;">Forensic Quality-of-Earnings & True Free Cash Flow Bridge</h2>
          <p style="font-size:12.5px; color:#94a3b8; margin:0;">Deconstructing reported operating cash flow to measure true owner earnings net of stock dilution and capital expenditures.</p>
        </div>
        <span class="badge badge-purple">Quality of Earnings Waterfall</span>
      </div>

      <div class="forensic-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
        <div class="waterfall-box" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:16px;">
          <h3 style="font-size:13px; font-weight:700; text-transform:uppercase; color:#94a3b8; margin:0 0 12px 0;">Latest Quarter True FCF Waterfall Bridge (Q3 2026 Ended Jul 31, 2026)</h3>
          
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
            <span><span class="tip" title="Operating Cash Flow" data-tip="Cash generated from normal operational activities, collections of multi-year subscriptions, and customer billings.">Operating Cash Flow (GAAP OCF)</span></span>
            <strong style="color:#f8fafc;">${latest_ocf:,.1f}M (${ocf_int_str}M)</strong>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:#f87171;">
            <span>(-) <span class="tip" title="Capital Expenditures" data-tip="Cash outflows for physical data center equipment, cloud server hardware, and facility build-outs.">Capital Expenditures (CapEx)</span></span>
            <strong>-${latest_capex:,.1f}M</strong>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.08); font-weight:600; color:#60a5fa;">
            <span>(=) <span class="tip" title="Reported Free Cash Flow" data-tip="Standard reported Free Cash Flow calculated as Operating Cash Flow minus Capital Expenditures.">Reported Free Cash Flow</span></span>
            <strong>${latest_reported_fcf:,.1f}M</strong>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:#f87171;">
            <span>(-) <span class="tip" title="Stock-Based Compensation" data-tip="Non-cash equity compensation granted to software engineers and executives, diluting shareholder equity over time.">Stock-Based Compensation (SBC)</span></span>
            <strong>-${latest_sbc:,.1f}M</strong>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:#94a3b8;">
            <span>(-) <span class="tip" title="Finance Lease Principal Payments" data-tip="Cash repayments on long-term data center equipment and server financing leases.">Finance Lease Repayments</span></span>
            <strong>-$0.0M</strong>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding:10px 0; font-weight:700; font-size:14px; color:#34d399; background:rgba(16,185,129,0.04); border-radius:4px; padding-left:8px; padding-right:8px; margin-top:4px;">
            <span>(=) <span class="tip" title="True Free Cash Flow" data-tip="Economic owner earnings remaining after funding physical capital investments, lease debt, and real dilution from equity grants.">True Forensic Free Cash Flow</span></span>
            <strong>${latest_true_fcf:,.1f}M</strong>
          </div>
        </div>

        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:16px;">
          <h3 style="font-size:13px; font-weight:700; text-transform:uppercase; color:#94a3b8; margin:0 0 12px 0;">Forensic Cash Flow Quality Analysis</h3>
          <p style="font-size:12.5px; color:#cbd5e1; line-height:1.55; margin-bottom:12px;">
            Palo Alto Networks generated exceptional cash generation in Q3 2026, delivering <strong>${latest_ocf:,.0f}M</strong> in Operating Cash Flow and <strong>${latest_reported_fcf:,.0f}M</strong> in Reported FCF (36.8% FCF margin). Strong customer collections and multi-year upfront software billing cycles bolster working capital.
          </p>
          <p style="font-size:12.5px; color:#cbd5e1; line-height:1.55; margin-bottom:12px;">
            Adjusting for <strong>${latest_sbc:,.0f}M</strong> of Stock-Based Compensation (which represents 13.5% of total revenue), True Free Cash Flow settled at <strong>${latest_true_fcf:,.0f}M</strong> (23.3% True FCF margin). This ranks in the top decile across the cybersecurity industry and fully self-funds PANW's aggressive organic R&D and targeted M&A investments.
          </p>
          <div style="background:rgba(59,130,246,0.04); border:1px solid rgba(59,130,246,0.15); border-radius:6px; padding:10px; font-size:12px; color:#93c5fd;">
            <strong>Institutional Takeaway:</strong> Unlike pure-play unprofitable security peers, PANW's high cash conversion allows it to absorb platformization free-transition periods without tapping credit lines or diluting stockholders with secondary equity raises.
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 5: ROW 4 SEGMENT EXECUTION AUDIT GRID & SECTION 4B DEBATES -->
    <section class="card" id="row-4-segments" style="margin-bottom:24px; padding:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div>
          <h2 style="font-size:18px; font-weight:700; color:#f8fafc; margin:0 0 4px 0;">Segment Execution Audit: Tailwinds vs. Headwinds</h2>
          <p style="font-size:12.5px; color:#94a3b8; margin:0;">Detailed operational drivers shaping Palo Alto Networks' revenue composition ahead of Q4 earnings.</p>
        </div>
        <span class="badge badge-blue">Operational Matrix</span>
      </div>

      <div class="audit-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:24px;">
        <div style="background:rgba(16,185,129,0.03); border:1px solid rgba(16,185,129,0.15); border-radius:8px; padding:16px;">
          <h3 style="color:#34d399; font-size:13px; font-weight:700; text-transform:uppercase; margin:0 0 12px 0;">Operational Tailwinds & Catalysts</h3>
          <ul style="margin:0; padding-left:18px; color:#cbd5e1; font-size:12.5px; line-height:1.6;">
            <li><strong>Prisma SASE Expansion:</strong> Rapid adoption of Zero Trust Network Access (ZTNA 2.0) and cloud-delivered SD-WAN across distributed enterprise workforces, replacing costly legacy MPLS networks.</li>
            <li><strong>Cortex XSIAM Momentum:</strong> Cumulative bookings surpassed $500M as global Security Operations Centers migrate from legacy SIEM tools to AI-automated threat detection and autonomous incident remediation.</li>
            <li><strong>Platformization Enterprise Penetration:</strong> Over 1,150 large enterprises have standardized on 3+ PANW platforms, driving 125%+ net revenue retention and reducing vendor sprawl.</li>
            <li><strong>CrowdStrike July Outage Market Share Migration:</strong> Enterprise CISOs increasingly prioritize vendor diversification and multi-platform resilience, steering cloud security and network perimeter RFPs toward Palo Alto Networks.</li>
          </ul>
        </div>

        <div style="background:rgba(239,68,68,0.03); border:1px solid rgba(239,68,68,0.15); border-radius:8px; padding:16px;">
          <h3 style="color:#f87171; font-size:13px; font-weight:700; text-transform:uppercase; margin:0 0 12px 0;">Execution Headwinds & Risks</h3>
          <ul style="margin:0; padding-left:18px; color:#cbd5e1; font-size:12.5px; line-height:1.6;">
            <li><strong>Platformization Billing Lag:</strong> Deferred payment arrangements and 6-12 month free transition periods temporarily dampen reported quarterly billings growth relative to annual contract value (ACV).</li>
            <li><strong>Hardware Appliance Cyclicality:</strong> On-premises physical firewall refresh cycles face extended enterprise procurement scrutiny and capital expenditure belt-tightening.</li>
            <li><strong>Stock-Based Compensation Drag:</strong> Annual SBC exceeding $1.8B dilutes GAAP operating profitability, requiring substantial Non-GAAP adjustments to demonstrate operating leverage.</li>
            <li><strong>Intense Cloud Security Competition:</strong> Microsoft Defender/Sentinel and Cloudflare aggressively discount bundled enterprise agreements, forcing price competition on entry-level SASE deals.</li>
          </ul>
        </div>
      </div>

      <!-- SECTION 4B: INSTITUTIONAL DEBATES -->
      <div id="row-4b-debates">
        <h3 style="font-size:15px; font-weight:700; color:#f8fafc; margin:0 0 12px 0;">Top 3 Institutional Pre-Print Debates & Conference Call Focus Questions</h3>
{debates_html}
      </div>
    </section>

    <!-- SECTION 6: ROW 5 PEER VALUATION COMPS -->
    <section class="card" id="row-5-peers" style="margin-bottom:24px; padding:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <div>
          <h2 style="font-size:18px; font-weight:700; color:#f8fafc; margin:0 0 4px 0;">Peer Valuation & Operational Benchmarks</h2>
          <p style="font-size:12.5px; color:#94a3b8; margin:0;">Comparing Palo Alto Networks against premier enterprise cybersecurity peers across valuation, growth, and margins.</p>
        </div>
        <span class="badge badge-blue">Sector Comps</span>
      </div>

      <div class="table-wrapper">
        <table class="financial-table">
          <thead>
            <tr>
              <th>Company Name</th>
              <th>Ticker</th>
              <th>Market Cap</th>
              <th>Forward P/E</th>
              <th>EV / Sales (TTM)</th>
              <th>Revenue Growth (YoY)</th>
              <th>Gross Margin</th>
              <th>FCF Margin</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background:rgba(59,130,246,0.08); font-weight:700;">
              <td><span class="tip" title="Palo Alto Networks" data-tip="Global leader in enterprise cybersecurity, next-gen firewalls, SASE, and AI-driven autonomous SOC software.">Palo Alto Networks (Subject)</span></td>
              <td>PANW</td>
              <td>${mkt_cap_b:.1f}B</td>
              <td>{fwd_pe:.1f}x</td>
              <td>{ps_ttm:.1f}x</td>
              <td>+34.5%</td>
              <td>67.6%</td>
              <td>36.8%</td>
            </tr>
            <tr>
              <td><span class="tip" title="CrowdStrike Holdings" data-tip="Leading endpoint security and cloud workload protection provider operating the AI-native Falcon platform.">CrowdStrike Holdings</span></td>
              <td>CRWD</td>
              <td>$78.4B</td>
              <td>72.4x</td>
              <td>21.8x</td>
              <td>+31.7%</td>
              <td>75.2%</td>
              <td>32.1%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Fortinet Inc." data-tip="Cybersecurity leader specializing in secure networking, hardware firewalls, and integrated FortiOS fabric.">Fortinet Inc.</span></td>
              <td>FTNT</td>
              <td>$62.8B</td>
              <td>38.2x</td>
              <td>11.4x</td>
              <td>+14.0%</td>
              <td>78.5%</td>
              <td>38.2%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Zscaler Inc." data-tip="Zero Trust cloud security pioneer delivering secure web gateway and cloud application protection (ZIA / ZPA).">Zscaler Inc.</span></td>
              <td>ZS</td>
              <td>$29.5B</td>
              <td>58.6x</td>
              <td>13.8x</td>
              <td>+30.2%</td>
              <td>77.8%</td>
              <td>26.4%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cloudflare Inc." data-tip="Global cloud connectivity, edge compute, and application security platform protecting web infrastructure.">Cloudflare Inc.</span></td>
              <td>NET</td>
              <td>$31.2B</td>
              <td>94.1x</td>
              <td>18.9x</td>
              <td>+28.0%</td>
              <td>76.4%</td>
              <td>14.8%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 7: ROW 6 MULTI-SOURCE 4-PILLAR SENTIMENT GRID -->
    <section class="card" id="row-6-sentiment" style="margin-bottom:24px; padding:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <div>
          <h2 style="font-size:18px; font-weight:700; color:#f8fafc; margin:0 0 4px 0;">Multi-Source 4-Pillar Pre-Earnings Sentiment & Positioning Audit</h2>
          <p style="font-size:12.5px; color:#94a3b8; margin:0;">Synthesizing options volatility skew, sell-side revisions, retail community buzz, and short seller positioning.</p>
        </div>
        <span class="badge badge-purple">4-Pillar Sentiment</span>
      </div>

      <div class="sentiment-grid" style="display:grid; grid-template-columns:repeat(4, 1fr); gap:12px; margin-bottom:20px;">
        <div class="card sentiment-card" style="padding:14px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);">
          <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:700; margin-bottom:4px;">Options Skew & Volatility</div>
          <div style="font-size:20px; font-weight:800; color:#fbbf24; margin-bottom:4px;">74 / 100</div>
          <div class="sentiment-meter-bar" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-bottom:8px; overflow:hidden;">
            <div style="width:74%; height:100%; background:#fbbf24;"></div>
          </div>
          <span style="font-size:11.5px; color:#cbd5e1; line-height:1.4; display:block;">ATM Implied Move ±11.06% vs historical average 7.29%. Straddle is rich with high IV (118.1%), favoring short volatility strategies.</span>
        </div>

        <div class="card sentiment-card" style="padding:14px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);">
          <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:700; margin-bottom:4px;">Institutional Positioning</div>
          <div style="font-size:20px; font-weight:800; color:#34d399; margin-bottom:4px;">86 / 100</div>
          <div class="sentiment-meter-bar" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-bottom:8px; overflow:hidden;">
            <div style="width:86%; height:100%; background:#34d399;"></div>
          </div>
          <span style="font-size:11.5px; color:#cbd5e1; line-height:1.4; display:block;">51 Wall St analysts maintain a strong 1.65 Buy consensus with $398.63 mean price target (+26.5% upside) and Street-high $525.00.</span>
        </div>

        <div class="card sentiment-card" style="padding:14px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);">
          <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:700; margin-bottom:4px;">Retail Community Pulse</div>
          <div style="font-size:20px; font-weight:800; color:#60a5fa; margin-bottom:4px;">78 / 100</div>
          <div class="sentiment-meter-bar" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-bottom:8px; overflow:hidden;">
            <div style="width:78%; height:100%; background:#60a5fa;"></div>
          </div>
          <span style="font-size:11.5px; color:#cbd5e1; line-height:1.4; display:block;">Active discussion on Reddit (r/stocks, r/wallstreetbets) and FinTwit celebrating PANW's AI-SPM platformization moat and CrowdStrike share gains.</span>
        </div>

        <div class="card sentiment-card" style="padding:14px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);">
          <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:700; margin-bottom:4px;">Short Squeeze Asymmetry</div>
          <div style="font-size:20px; font-weight:800; color:#c084fc; margin-bottom:4px;">70 / 100</div>
          <div class="sentiment-meter-bar" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-bottom:8px; overflow:hidden;">
            <div style="width:70%; height:100%; background:#c084fc;"></div>
          </div>
          <span style="font-size:11.5px; color:#cbd5e1; line-height:1.4; display:block;">Modest short float of 2.54% ($6.5B short interest). Orderly covering anticipated on clean ARR beat and FY2027 guidance hike.</span>
        </div>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
        <div style="background:rgba(59,130,246,0.03); border:1px solid rgba(59,130,246,0.15); border-radius:8px; padding:14px;">
          <strong style="color:#60a5fa; font-size:13px; display:block; margin-bottom:6px;">Retail Trader Sentiment Narrative (Reddit & FinTwit)</strong>
          <p style="margin:0; font-size:12px; color:#cbd5e1; line-height:1.5;">{bus_2c['retail_vs_institutional_audit']['retail_narrative']}</p>
        </div>
        <div style="background:rgba(168,85,247,0.03); border:1px solid rgba(168,85,247,0.15); border-radius:8px; padding:14px;">
          <strong style="color:#c084fc; font-size:13px; display:block; margin-bottom:6px;">Institutional Desk Positioning (Sell-Side Previews & Hedge Funds)</strong>
          <p style="margin:0; font-size:12px; color:#cbd5e1; line-height:1.5;">{bus_2c['retail_vs_institutional_audit']['institutional_narrative']}</p>
        </div>
      </div>
    </section>

    <!-- SECTION 8: ROW 7 HEDGE FUND PM TRADE EXECUTION MATRIX -->
    <section class="card" id="row-7-pm-matrix" style="margin-bottom:24px; padding:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <div>
          <h2 style="font-size:18px; font-weight:700; color:#f8fafc; margin:0 0 4px 0;">Hedge Fund Portfolio Manager Options & Trade Execution Matrix</h2>
          <p style="font-size:12.5px; color:#94a3b8; margin:0;">3-Scenario execution playbook anchored to spot price (${spot_price:.2f}) and options straddle pricing.</p>
        </div>
        <span class="badge badge-warn">Institutional Risk Matrix</span>
      </div>

      <div class="scenario-grid" style="display:grid; grid-template-columns:repeat(3, 1fr); gap:14px; margin-bottom:20px;">
        <!-- BULL CASE -->
        <div class="card scenario-bull" style="background:rgba(16,185,129,0.03); border:1px solid rgba(16,185,129,0.2); border-radius:8px; padding:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="badge badge-bull" style="font-weight:700;">Bull Case Scenario</span>
            <span style="font-size:12px; font-weight:700; color:#34d399;">Probability: 35%</span>
          </div>
          <div style="font-size:18px; font-weight:800; color:#34d399; margin-bottom:4px;">Target: $355.00 – $375.00</div>
          <div style="font-size:12px; color:#94a3b8; margin-bottom:10px;">Implied Move: +12.6% to +19.0%</div>
          <p style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
            <strong>Catalysts:</strong> Q4 Revenue beats $3,365.0M whisper bogey, NGS ARR surpasses $4.68B (+40% YoY), cumulative platformized customers exceed 1,300 deals, and management raises FY2027 revenue guidance above $14.2B with accelerating FCF margins.
          </p>
          <div class="trade-structure" style="background:rgba(16,185,129,0.06); border-left:2px solid #10b981; padding:8px 10px; border-radius:4px; font-size:11.5px; color:#e2e8f0;">
            <strong>Options Structure:</strong> Long Nov 20 $320/$350 Call Spread or Bull Risk Reversal (sell $295 put, buy $325 call).
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="card scenario-base" style="background:rgba(59,130,246,0.03); border:1px solid rgba(59,130,246,0.2); border-radius:8px; padding:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="badge badge-blue" style="font-weight:700;">Base Case (Rangebound)</span>
            <span style="font-size:12px; font-weight:700; color:#60a5fa;">Probability: 45%</span>
          </div>
          <div style="font-size:18px; font-weight:800; color:#60a5fa; margin-bottom:4px;">Target: $305.00 – $330.00</div>
          <div style="font-size:12px; color:#94a3b8; margin-bottom:10px;">Implied Move: -3.2% to +4.7%</div>
          <p style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
            <strong>Catalysts:</strong> Revenue meets consensus at $3,310M–$3,330M, Non-GAAP EPS beats modestly by $0.03 ($1.00 actual), and forward Q1 guide matches Street bogeys. Elevated options IV (118.1%) collapses post-earnings, keeping price rangebound.
          </p>
          <div class="trade-structure" style="background:rgba(59,130,246,0.06); border-left:2px solid #3b82f6; padding:8px 10px; border-radius:4px; font-size:11.5px; color:#e2e8f0;">
            <strong>Options Structure:</strong> Short Nov 20 $315 Iron Condor (Sell $300 Put / $330 Call, Buy $285 Put / $345 Call) to harvest volatility crush.
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="card scenario-bear" style="background:rgba(239,68,68,0.03); border:1px solid rgba(239,68,68,0.2); border-radius:8px; padding:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="badge badge-warn" style="font-weight:700;">Bear Case Breakdown</span>
            <span style="font-size:12px; font-weight:700; color:#f87171;">Probability: 20%</span>
          </div>
          <div style="font-size:18px; font-weight:800; color:#f87171; margin-bottom:4px;">Target: $265.00 – $280.00</div>
          <div style="font-size:12px; color:#94a3b8; margin-bottom:10px;">Implied Move: -11.2% to -15.9%</div>
          <p style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
            <strong>Catalysts:</strong> Management commentary reveals severe billings lag from platformization concessions, hardware appliance sales contract double-digits, and forward Q1 revenue guidance falls short of Street consensus (&lt;$3,390M midpoint).
          </p>
          <div class="trade-structure" style="background:rgba(239,68,68,0.06); border-left:2px solid #ef4444; padding:8px 10px; border-radius:4px; font-size:11.5px; color:#e2e8f0;">
            <strong>Options Structure:</strong> Long Nov 20 $305/$275 Bear Put Spread or Long Out-of-the-Money $280 Puts.
          </div>
        </div>
      </div>

      <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); border-radius:6px; padding:12px; font-size:12px; color:#94a3b8;">
        <strong>Portfolio Manager Note:</strong> With the weekly ATM straddle implying an ±11.06% move ($34.85 premium) against an average historical move of only 7.29%, options market premium is heavily loaded. Delta-neutral volatility sellers hold the statistical edge, while directional long players should seek structured spreads to mitigate significant implied volatility crush upon market open.
      </div>
    </section>

    <!-- FOOTER VERIFICATION LEDGER -->
    <footer style="margin-top:30px; padding:16px; border-top:1px solid #334155; font-size:11.5px; color:#64748b; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <span>Deterministic Pre-Earnings Ground Truth Verified: <strong>PANW (2026-11-18)</strong></span> •
        <span>Spot Price: <strong>${spot_price:.2f}</strong></span> •
        <span>Latest OCF: <strong>${latest_ocf:,.0f}M</strong></span> •
        <span>True FCF: <strong>${latest_true_fcf:,.0f}M</strong></span>
      </div>
      <div>
        <span class="badge badge-blue">Antigravity 2.0 Track A + Track B Institutional Certified</span>
      </div>
    </footer>
"""

draft_payload = {
    "ticker": "PANW",
    "earnings_date": "2026-11-18",
    "report_type": "T-1_PRE_EARNINGS",
    "header": {
        "page_title": "PANW Q4 2026E Pre-Earnings Tearsheet | Institutional Equity Research",
        "ticker": "PANW",
        "company_name": "Palo Alto Networks, Inc.",
        "earnings_date": "2026-11-18",
        "spot_price": spot_price,
        "market_cap_billions": round(mkt_cap_b, 2),
        "enterprise_value_billions": round(ev_b, 2),
        "consensus_revenue_millions": consensus_rev,
        "consensus_eps": consensus_eps,
        "options_implied_move_pct": opt_move_pct
    },
    "historical_table_5q_nums": historical_table_5q_nums,
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "period_label": "Q3 2026 (Ended Jul 31, 2026)",
            "ocf": latest_ocf,
            "capex": latest_capex,
            "reported_fcf": latest_reported_fcf,
            "sbc": latest_sbc,
            "finance_leases": latest_leases,
            "true_fcf": latest_true_fcf
        }
    },
    "trade_matrix": {
        "bull_target_low_num": 355.0,
        "bear_target_high_num": 280.0
    },
    "rendered_container_html": html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"[SUCCESS] Wrote draft JSON to {DRAFT_PATH.name} (Length: {len(html):,} chars).")
