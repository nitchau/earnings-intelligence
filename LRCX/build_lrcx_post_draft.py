"""
LRCX Dedicated Post-Earnings Draft Builder (Track A + Track B Complete Re-Synthesis)
Builds drafts/LRCX_2026-10-21_post_draft.json with 100% Q3 2026 (Actual) rolled 5-quarter tables,
Q4 2026E forward guidance columns, zero T-1 bleed-through, and Track B interactive enhancements.
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "LRCX_2026-10-21_post_truth.json"
BUS_2A_PATH = BASE_DIR / "post_agent_bus" / "LRCX_2026-10-21_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "post_agent_bus" / "LRCX_2026-10-21_agent2b_transcript.json"
BUS_2C_PATH = BASE_DIR / "post_agent_bus" / "LRCX_2026-10-21_agent2c_social.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "LRCX_2026-10-21_post_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
kpis_data = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
trans_data = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
soc_data = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

reg_price = truth["post_print_reaction"]["regular_close_price"]      # 260.81
ah_price = truth["post_print_reaction"]["after_hours_price"]         # 241.48
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]  # -7.41
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] # 3.84
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 9.18)
verdict = truth["post_print_reaction"]["overall_print_verdict"]      # CLEAN BEAT & RAISE

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]  # 8219.42
cons_rev = truth["t1_baseline"]["consensus_revenue_millions"]                 # 6950.0
q0_gaap_eps = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"]     # 2.19
q0_adj_eps = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"]   # 2.20
cons_eps = truth["t1_baseline"]["consensus_eps_nongaap"]                      # 2.18

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # 3497.65
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 257.70
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # 3239.95
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 114.70
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 34.49
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # 3090.76

s5q = truth["stitched_5q_chronological"]

container_html = f"""
    <!-- 1. HEADER BANNER (T+0 POST-EARNINGS FORENSIC TEARSHEET) -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#34d399;">Newly Reported Quarter: <strong>Sep 2026 Quarter (Ended Sep 27, 2026)</strong> • Forward Guidance Horizon: <strong>Dec 2026 Quarter ($8.60B ± $400M)</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">LRCX</span>
            <h1 class="company-name">Lam Research Corporation</h1>
            <span class="badge badge-bull">{verdict}</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="Immediate post-earnings release forensic analysis." data-tip="T+0 Post-Print: Forensic analysis synthesized immediately following the official September 2026 Quarter SEC Form 8-K release and earnings conference call.">T+0</span> POST-EARNINGS FORENSIC TEARSHEET</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select • Semiconductor Wafer Fabrication Equipment (WFE), High-Aspect-Ratio Etch, Gate-All-Around (GAA) &amp; HBM4 TSV • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): 0000707549 assigned by the U.S. Securities and Exchange Commission (SEC) to Lam Research Corp.">CIK</span>: 0000707549</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Regular Close / <span style="color:#f87171;">After-Hours Price</span></div>
            <div class="price-value">${reg_price:.2f} / <span style="color:#f87171;">${ah_price:.2f}</span> <span style="font-size:14px; color:#f87171;">({post_move_pct:+.2f}%)</span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total equity value at $241.48 after-hours price across 1,259.6M diluted shares." data-tip="Market Capitalization: Post-print equity value (~$304.2B at $241.48 AH / $326.4B regular close) vs $324.9B Enterprise Value.">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Debt ($4.48B) minus Cash ($6.53B)." data-tip="Enterprise Value (EV): Reflects Lam's -$2.05B net cash fortress ($6,527.18M cash &amp; restricted cash vs $4,480.34M total debt &amp; finance leases).">EV</span></div>
            <div class="price-value">$326.4B / $324.9B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Sep 2026 SEC Form 8-K Filed</span>
          <span class="strip-val" style="color: var(--bull-green);">Wed, Oct 21, 2026 • <span class="tip" title="After Market Close: Official Q1 FY2027 (Sep 27, 2026) earnings release filed via SEC Form 8-K Item 2.02." data-tip="Form 8-K Item 2.02 &amp; Exhibit 99.1 filed October 21, 2026 after market close; Webcast hosted at 2:00 PM PT / 5:00 PM ET.">8-K Verified</span></span>
          <span class="kpi-sub">Exhibit 99.1 &amp; Earnings Call Transcript Audited</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="Actual post-market stock reaction (-7.41%) compared against pre-print options straddle implied move (±3.84%)." data-tip="Actual vs. Implied Move: LRCX traded down -7.41% (-$19.33/sh to $241.48) in after-hours sell-the-news profit-taking after a +135% YTD run, exceeding the ±3.84% (±$9.18/sh) ATM weekly straddle.">Actual AH Move vs. Implied</span></span>
          <span class="strip-val" style="color: var(--warn-amber);">{post_move_pct:+.2f}% (vs ±{opt_implied_pct:.2f}% Est)</span>
          <span class="kpi-sub">-${reg_price - ah_price:.2f}/sh Actual vs ±${opt_straddle:.2f}/sh <span class="tip" title="At-The-Money weekly straddle price prior to earnings." data-tip="ATM Straddle: Pre-earnings weekly option straddle priced at ±$9.18/sh (3.84% implied move).">ATM Straddle</span></span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Sep 2026 Actual <span class="tip" title="Reported September 2026 Quarter GAAP Revenue ($8,219.42M, +22.3% QoQ, +54.4% YoY) vs Wall Street Consensus ($6,950M)." data-tip="Record Revenue Beat: Reported $8,219.42M (+22.27% QoQ, +54.38% YoY), beating Street consensus of $6,950M by +$1,269.42M (+18.27%) as Systems revenue surged +34.9% QoQ to $5,732.91M.">Revenue vs. Street</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$8.22B <span style="font-size:12px;">(+$1.27B Beat)</span></span>
          <span class="kpi-sub">Street Est: $6.95B | Systems: $5.73B (+34.9% QoQ)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Sep 2026 Actual <span class="tip" title="Reported Non-GAAP Diluted EPS ($2.20, +20.9% QoQ) and GAAP Diluted EPS ($2.19, +21.0% QoQ) vs Consensus ($2.18)." data-tip="Q3 2026 EPS Beat: Reported $2.20 Non-GAAP Diluted EPS (+20.9% QoQ, +74.6% YoY), beating $2.18 Street consensus, alongside $2.19 GAAP Diluted EPS.">EPS (Non-GAAP / GAAP)</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$2.20 Adj / $2.19 <span class="tip" title="Generally Accepted Accounting Principles Diluted EPS ($2.19 on $2,753.14M GAAP Net Income)." data-tip="GAAP Diluted EPS reached $2.19 (+21.0% QoQ, +76.6% YoY) on record $2,753.14M GAAP Net Income.">GAAP</span></span>
          <span class="kpi-sub">Beat $2.18 Consensus | Non-GAAP GM: 52.4% | OM: 40.2%</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">New Dec 2026 <span class="tip tip-right" title="Official December 2026 Quarter (Q2 FY2027) guidance issued in the Form 8-K release." data-tip="December 2026 Guidance Raise: Guided Dec 2026 revenue to $8.60B ± $400M, Non-GAAP GM to 52.5% ± 1%, Non-GAAP OM to 40.5% ± 1%, and Non-GAAP EPS to $2.33 ± $0.15, plus a +27% dividend hike to $0.33/sh.">Guidance &amp; +27% Div Hike</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$8.60B ± $0.4B Dec Rev</span>
          <span class="kpi-sub">Dec EPS Guide: $2.33 ± $0.15 | Dividend Hiked +27% to $0.33</span>
        </div>
      </div>
    </header>

    <!-- TRACK B: STICKY INTERACTIVE SECTION JUMP-NAV & PAIRED T-1 SWITCHER -->
    <nav class="post-jump-nav" style="position: sticky; top: 8px; z-index: 90; background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(10px); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 10px; padding: 8px 14px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
      <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
        <span style="font-size: 11px; font-weight: 800; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.06em; margin-right: 4px;">⚡ Jump To:</span>
        <a href="#row-1-kpis" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">1. Q3 KPIs</a>
        <a href="#row-1b-scorecard" style="font-size: 11.5px; color: #34d399; font-weight: 700; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.35);">1B. Beat/Miss &amp; Guidance Scorecard</a>
        <a href="#row-2-financials" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">2. Rolling 5Q Table (Q3 Actual + Q4E)</a>
        <a href="#row-3-fcf" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">3. FCF Bridge</a>
        <a href="#row-4-segments" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">4. Tailwinds/Drags</a>
        <a href="#row-4b-audit" style="font-size: 11.5px; color: #93c5fd; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(59, 130, 246, 0.14); border: 1px solid rgba(59, 130, 246, 0.3);">4B. Call Q&amp;A</a>
        <a href="#row-5-peers" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">5. Peers</a>
        <a href="#row-6-sentiment" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">6. Social &amp; Sentiment</a>
        <a href="#row-7-pm-matrix" style="font-size: 11.5px; color: #fcd34d; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(245, 158, 11, 0.14); border: 1px solid rgba(245, 158, 11, 0.3);">7. PM Trade Matrix</a>
      </div>
      <a href="LRCX_T1_2026-10-21.html" style="font-size: 11.5px; font-weight: 700; color: #93c5fd; text-decoration: none; padding: 5px 12px; border-radius: 6px; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.45); display: flex; align-items: center; gap: 6px;">
        ⇄ Compare Paired T-1 Pre-Earnings Briefing
      </a>
    </nav>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS — ALL ROLLED FORWARD TO Q3 2026 ACTUALS) -->
    <section class="kpi-grid" id="row-1-kpis">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Intensity (Q3 2026 Actual)</div>
          <span class="badge badge-bull">+140% QOQ OCF SURGE</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual GAAP cash generated from operations in the September 2026 quarter ($3,497.65M)." data-tip="Operating Cash Flow (OCF): Exploded +140.02% QoQ and +96.61% YoY to an all-time record $3,497.65M (42.55% OCF margin).">Operating Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">OCF Margin: 42.55% of Revenue | +$1.17B Deferred Profit Inflow</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$3,498M</span>
              <div class="delta-pair">
                <span class="badge badge-bull"><span class="tip" title="Sequential change from June 2026 ($1,457.23M) to September 2026 ($3,497.65M)." data-tip="QoQ OCF Delta: Surged +140.02% sequentially from $1,457.23M in Q2 2026.">QoQ</span> +140.02%</span>
                <span class="badge badge-bull"><span class="tip" title="Year-over-Year change from September 2025 ($1,778.96M) to September 2026 ($3,497.65M)." data-tip="YoY OCF Delta: Jumped +96.61% from $1,778.96M in Q3 2025.">YoY</span> +96.61%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures in the September 2026 quarter ($257.70M)." data-tip="Capital Expenditures (CapEx): Ultra-asset-light manufacturing model required just $257.70M in Q3 CapEx (3.14% of revenue).">Capital Expenditures</span> (Q3 2026)</span>
              <span class="kpi-sub">Ultra-Low CapEx Intensity: 3.14% of Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">($258M)</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +36.49%</span>
                <span class="badge badge-neutral">YoY +39.21%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: OCF ($3,497.65M) minus CapEx ($257.70M) = $3,239.95M." data-tip="Reported Free Cash Flow: Surged +155.43% QoQ and +103.28% YoY to a record $3,239.95M (39.42% FCF margin).">Reported Free Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">Record FCF Margin: 39.42% of Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$3,240M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +155.43%</span>
                <span class="badge badge-bull">YoY +103.28%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forensic True Free Cash Flow: OCF ($3,497.65M) - CapEx ($257.70M) - SBC ($114.70M) - Finance Leases ($34.49M) = $3,090.76M." data-tip="True Free Cash Flow: Reached $3,090.76M (+165.73% QoQ, +106.71% YoY; 37.60% True FCF margin) as SBC was just 1.40% of revenue.">True FCF (ex-SBC &amp; Leases)</span> (Q3 2026)</span>
              <span class="kpi-sub">Q3 SBC: Only $114.7M (1.40% of Rev) | Leases: $34.5M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$3,091M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +165.73%</span>
                <span class="badge badge-bull">YoY +106.71%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING MARGINS (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Margins (Q3 2026 Actual)</div>
          <span class="badge badge-bull">40.2% NON-GAAP OP MARGIN</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Gross Profit ($4,298.85M, 52.3% GM) and Non-GAAP Gross Profit ($4,307.98M, 52.4% GM)." data-tip="Gross Profit: Jumped +23.58% QoQ and +60.11% YoY to $4,298.85M GAAP (52.3% GM; Non-GAAP $4,307.98M / 52.4% GM).">Gross Profit</span> (Q3 2026)</span>
              <span class="kpi-sub">GAAP GM: 52.30% | Non-GAAP GM: 52.40% (+60 bps QoQ)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$4,299M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +23.58%</span>
                <span class="badge badge-bull">YoY +60.11%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Operating Income ($3,283.73M, 39.95% margin) and Non-GAAP Operating Income ($3,300.16M, 40.2% margin)." data-tip="Operating Income (EBIT): Surged +30.64% QoQ and +79.53% YoY to $3,283.73M GAAP (39.95% margin; Non-GAAP $3,300.16M / 40.2% margin, +260 bps QoQ).">Operating Income (EBIT)</span> (Q3 2026)</span>
              <span class="kpi-sub">GAAP OM: 39.95% | Non-GAAP OM: 40.20% (+260 bps QoQ)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$3,284M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +30.64%</span>
                <span class="badge badge-bull">YoY +79.53%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research &amp; Development ($666.40M) plus SG&amp;A ($348.73M) = $1,015.13M Total Operating Expenses." data-tip="Operating Expenses: $1,015.13M in Q3 2026 (+5.17% QoQ vs +22.27% revenue growth), driving massive operating leverage (OpEx just 12.35% of revenue).">R&amp;D &amp; Total OpEx Leverage</span> (Q3 2026)</span>
              <span class="kpi-sub">R&amp;D: $666.4M | SG&amp;A: $348.7M | Total OpEx: 12.35% of Rev</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$1,015M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +5.17%</span>
                <span class="badge badge-warn">YoY +18.62%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Net Income ($2,753.14M, $2.19/sh) and Non-GAAP Net Income ($2,765.06M, $2.20/sh)." data-tip="Net Income &amp; EPS: Record $2,753.14M GAAP Net Income ($2.19 EPS) and $2,765.06M Non-GAAP Net Income ($2.20 EPS, +20.9% QoQ, +74.6% YoY).">Net Income &amp; EPS</span> (Q3 2026)</span>
              <span class="kpi-sub">Non-GAAP EPS: $2.20 (+20.9% QoQ) | GAAP EPS: $2.19</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$2,753M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Adj EPS: $2.20</span>
                <span class="badge badge-bull">YoY +75.51%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS & SHAREHOLDER RETURN (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Capital Return (Q3 2026)</div>
          <span class="badge badge-bull">+$2.05B NET CASH + 27% DIV HIKE</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Cash and cash equivalents ($6,523.75M) plus Restricted cash ($3.43M) = $6,527.18M as of Sep 27, 2026." data-tip="Liquid Reserves: Surged +38.80% sequentially (+$1,824.66M QoQ) from $4,702.52M in June 2026 to $6,527.18M in September 2026.">Cash &amp; Restricted Cash</span> (Q3 2026)</span>
              <span class="kpi-sub">Increased +$1,824.7M Sequentially (+38.8% QoQ)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$6,527M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +38.80%</span>
                <span class="badge badge-bull">+$1.82B QoQ</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Current debt &amp; finance leases ($7.73M) plus Long-term debt &amp; finance leases ($4,472.62M) = $4,480.34M." data-tip="Total Debt &amp; Finance Leases: Declined -$34.13M QoQ to $4,480.34M as of September 27, 2026.">Total Debt &amp; Finance Leases</span> (Q3 2026)</span>
              <span class="kpi-sub">Current Debt: $7.7M | Long-Term Senior Notes: $4,472.6M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$4,480M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ -0.76%</span>
                <span class="badge badge-bull">A / A2 Credit</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Debt ($4,480.34M) minus Cash &amp; Restricted Cash ($6,527.18M) = -$2,046.84M Net Cash." data-tip="Net Cash Position: Expanded by +$1,858.79M sequentially to a +$2,046.84M net cash surplus.">Net Cash Position</span> (Q3 2026)</span>
              <span class="kpi-sub">+$2.05B Net Cash Surplus Over All Debt</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">-$2,047M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">+$1.86B QoQ</span>
                <span class="badge badge-bull">Zero Net Leverage</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Q3 Share Repurchases ($1,093.77M) plus Dividends Paid ($327.08M) = $1,420.85M; Quarterly dividend raised +27% to $0.33/sh ($1.32/yr)." data-tip="Capital Return &amp; Dividend Hike: Returned $1,420.85M in Q3 ($1,093.77M buybacks + $327.08M dividends) and hiked the quarterly dividend by +27% from $0.26 to $0.33/sh.">Q3 Buybacks &amp; +27% Dividend Hike</span></span>
              <span class="kpi-sub">Q3 Buybacks: $1,093.8M | Div Hiked +27% ($0.26 → $0.33/sh)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,421M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Div +27% ($0.33)</span>
                <span class="badge badge-bull">ROIC: 61%+</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT MIX & GEOGRAPHIC BREAKDOWN (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Mix &amp; WFE Geo Breakdown (Q3 2026)</div>
          <span class="badge badge-blue">SYSTEMS +34.9% QOQ</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Systems Revenue in the September 2026 quarter ($5,732.91M, +34.86% QoQ, +61.59% YoY)." data-tip="Systems Revenue: Surged +34.86% QoQ and +61.59% YoY to $5,732.91M (69.75% of total revenue) on GAA logic and HBM4 TSV etch shipments.">Systems Revenue &amp; Share</span> (Q3 2026)</span>
              <span class="kpi-sub">Rev: $5,732.91M (+34.9% QoQ, +61.6% YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">69.75% / $5.73B</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +34.86%</span>
                <span class="badge badge-bull">YoY +61.59%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Customer Support Business Group (CSBG) and other revenue ($2,486.51M in Q3 2026)." data-tip="CSBG Revenue: Reached $2,486.51M (+0.62% QoQ, +39.98% YoY; 30.25% of revenue) across >100,000 active installed chambers.">Customer Support (CSBG) Share</span> (Q3 2026)</span>
              <span class="kpi-sub">Rev: $2,486.51M (+40.0% YoY) | Installed Base Flywheel</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">30.25% / $2.49B</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +0.62%</span>
                <span class="badge badge-bull">YoY +39.98%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Geographic Revenue Mix in Q3 2026: Taiwan 25%, Korea 24%, China 24%, US 12%, Japan 8%, SE Asia 5%, Europe 2%." data-tip="Geographic De-Risking: Taiwan (25%) and Korea (24%) represented 49% of total revenue on TSMC N2 GAA and SK Hynix/Samsung HBM4 ramps, while China normalized to 24%.">Geographic Mix (Taiwan + Korea = 49%)</span></span>
              <span class="kpi-sub">Taiwan: 25% | Korea: 24% | China: 24% | US: 12% | Japan: 8%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">TW 25% / KR 24%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">China Down to 24%</span>
                <span class="badge badge-bull">Leading-Edge 76%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Post-print valuation multiples at $241.48 After-Hours price and $2.33 Dec Qtr EPS guide ($9.32 annualized)." data-tip="Post-Print Forward P/E: At $241.48 AH price and $9.32 annualized Dec Qtr EPS run-rate, LRCX trades at 25.9x run-rate earnings.">Post-Print Run-Rate P/E (at $241.48)</span></span>
              <span class="kpi-sub">Dec Qtr EPS Guide: $2.33 ($9.32 Annualized Run-Rate)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">25.9x Run-Rate</span>
              <div class="delta-pair">
                <span class="badge badge-bull">$3.22B Deferred Rev</span>
                <span class="badge badge-bull">Dec Guide: $8.6B</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         3. ROW 1B: POST-RELEASE PRINT VS. EXPECTATIONS & PRIOR GUIDANCE SCORECARD
         ========================================================================== -->
    <section class="card" id="row-1b-scorecard">
      <div class="card-header">
        <div>
          <div class="card-title">
            <span class="card-title-accent"></span>Post-Release Print vs. Expectations &amp; Prior Guidance Scorecard
          </div>
          <div class="card-subtitle">
            Source: Lam Research SEC Form 8-K (Item 2.02, Exhibit 99.1) Filed Oct 21, 2026 • September 2026 Quarter Release • Wall Street Consensus Comparison
          </div>
        </div>
        <div style="display:flex; gap: 8px; align-items:center;">
          <span class="badge badge-bull">RECORD $8.22B REV BEAT + $8.60B DEC GUIDE + 27% DIV HIKE</span>
          <span class="badge badge-blue">T+0 POST-PRINT</span>
        </div>
      </div>

      <!-- TRACK B: T-1 PRE-PRINT THESIS VS. T+0 POST-PRINT REALITY AUDIT BANNER -->
      <div class="t1-vs-t0-audit" style="background: linear-gradient(90deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(59, 130, 246, 0.35); border-left: 4px solid #34d399; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
          <span style="font-weight: 800; font-size: 13px; color: #34d399; text-transform: uppercase; letter-spacing: 0.05em;">🔍 T-1 Pre-Earnings Thesis vs. T+0 Post-Print Reality Audit</span>
          <a href="LRCX_T1_2026-10-21.html" style="font-size: 11.5px; color: #93c5fd; text-decoration: underline;">Open Original T-1 Briefing →</a>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; font-size: 12.3px; color: var(--text-secondary);">
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #93c5fd;">WFE Systems &amp; HBM4/GAA Thesis:</strong><br>
            • <em>T-1 Forecast:</em> Expected Systems ramp in Taiwan &amp; Korea to offset China.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">SHATTERED EXPECTATIONS</strong> — Revenue hit <strong>$8,219.42M</strong> (+22.3% QoQ, +54.4% YoY) as Systems jumped <strong>+34.9% QoQ to $5,732.91M</strong> (Taiwan 25%, Korea 24%).
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #fcd34d;">Margin &amp; Cash Flow Conversion Thesis:</strong><br>
            • <em>T-1 Forecast:</em> Modeled ~51.5% GM and strong customer deposit inflows.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">BLOWOUT EXECUTION</strong> — Non-GAAP GM hit <strong>52.4%</strong>, Non-GAAP OM hit <strong>40.2%</strong> (+260 bps QoQ), and OCF exploded +140% QoQ to <strong>$3,497.65M</strong>.
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #34d399;">Forward Guide vs. Crowded Positioning:</strong><br>
            • <em>T-1 Forecast:</em> Flagged crowded positioning after +135% YTD rally.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">BEAT &amp; RAISE (+SELL-THE-NEWS DIP)</strong> — Guided Dec Qtr to <strong>$8.60B ± $400M</strong> &amp; <strong>$2.33 EPS</strong> and hiked dividend +27%; -7.41% AH dip is pure profit-taking.
          </div>
        </div>
      </div>

      <!-- TABLE 1B-1: HEADLINE & COMPANY-SPECIFIC KPI BEAT / MISS SCORECARD -->
      <div style="margin-bottom: 20px;">
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-1: Headline &amp; Company-Specific KPI Beat / Miss Scorecard (Sep 2026 Quarter Actuals)</span>
          <span class="tip" title="Deterministic comparison of reported September 2026 actuals against Street pre-print consensus and T-1 whisper." data-tip="Beat / Miss Scorecard: Evaluates September 2026 delivery across headline GAAP/Non-GAAP metrics and Lam-specific WFE KPIs with visual magnitude bars.">[Methodology]</span>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style="min-width: 240px;">Metric / Company KPI</th>
                <th>Street Consensus</th>
                <th>T-1 Whisper</th>
                <th class="col-q0">Reported Actual (Q3 2026)</th>
                <th style="min-width: 190px;">Vs. Consensus ($ / % / bps)</th>
                <th>Vs. Whisper</th>
                <th>Verdict Badge</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="tip" title="Total Revenue ($8,219.42M) across Systems ($5,732.91M) and CSBG ($2,486.51M)." data-tip="Total Revenue ($M): Record $8,219.42M (+22.27% QoQ, +54.38% YoY), beating initial Street consensus ($6,950M) by +$1,269.42M (+18.27%) and updated guidance ($7,900M) by +$319.42M.">Total Revenue ($M)</span></td>
                <td>$6,950.0M</td>
                <td>$8,050.0M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$8,219.42M</td>
                <td>
                  <span class="badge badge-bull">+$1,269.42M (+18.27%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:96%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$169.42M (+2.10%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Non-GAAP Diluted EPS ($2.20) and GAAP Diluted EPS ($2.19) vs Street Consensus ($2.18)." data-tip="Non-GAAP Diluted EPS: Reached a record $2.20 (+20.88% QoQ, +74.60% YoY), beating consensus of $2.18 by +$0.02 (+0.92%).">Non-GAAP Diluted EPS (GAAP: $2.19)</span></td>
                <td>$2.18</td>
                <td>$2.19</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$2.20 <span style="font-size:11px; color:var(--text-muted);">($2.19 GAAP)</span></td>
                <td>
                  <span class="badge badge-bull">+$0.02 (+0.92%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:74%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$0.01 (+0.46%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Systems Revenue: Wafer fabrication equipment shipments across Foundry, Logic, DRAM, and NAND ($5,732.91M)." data-tip="Systems Revenue ($M): Surged +34.86% QoQ and +61.59% YoY to $5,732.91M (69.75% of total revenue).">Systems Revenue ($M)</span></td>
                <td>$5,450.0M</td>
                <td>$5,600.0M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$5,732.91M</td>
                <td>
                  <span class="badge badge-bull">+$282.91M (+5.19%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:88%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$132.91M (+2.37%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Customer Support Business Group (CSBG) and other revenue ($2,486.51M)." data-tip="CSBG Revenue ($M): Reached $2,486.51M (+0.62% QoQ, +39.98% YoY) on high chamber utilization and Reliant upgrades.">Customer Support (CSBG) Revenue ($M)</span></td>
                <td>$2,450.0M</td>
                <td>$2,475.0M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$2,486.51M</td>
                <td>
                  <span class="badge badge-bull">+$36.51M (+1.49%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:76%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$11.51M (+0.47%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Non-GAAP Gross Margin (52.4%) and GAAP Gross Margin (52.3%) in the September 2026 quarter." data-tip="Gross Margin: Expanded +60 bps QoQ to 52.4% Non-GAAP (52.3% GAAP), beating consensus by +40 bps on Penang factory scale and product mix.">Non-GAAP / GAAP Gross Margin (%)</span></td>
                <td>52.00%</td>
                <td>52.20%</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">52.40% <span style="font-size:11px; color:var(--text-muted);">(52.3% GAAP)</span></td>
                <td>
                  <span class="badge badge-bull">+40 bps</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:82%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+20 bps</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Non-GAAP Operating Margin (40.2%) and GAAP Operating Margin (40.0%) in the September 2026 quarter." data-tip="Operating Margin: Expanded +260 bps QoQ from 37.6% to 40.2% Non-GAAP (39.95% GAAP), beating consensus by +120 bps.">Non-GAAP Operating Margin (%)</span></td>
                <td>39.00%</td>
                <td>39.50%</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">40.20% <span style="font-size:11px; color:var(--text-muted);">(40.0% GAAP)</span></td>
                <td>
                  <span class="badge badge-bull">+120 bps</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:91%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+70 bps</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Operating Cash Flow ($3,497.65M) and Reported Free Cash Flow ($3,239.95M) in Q3 2026." data-tip="Operating Cash Flow ($M): Exploded +140.02% QoQ to $3,497.65M ($3,239.95M Reported FCF), beating consensus by +$1,197.65M (+52.1%).">Operating Cash Flow ($M)</span></td>
                <td>$2,300.0M</td>
                <td>$2,550.0M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$3,497.65M</td>
                <td>
                  <span class="badge badge-bull">+$1,197.65M (+52.07%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:98%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$947.65M (+37.16%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="China Revenue Share normalized to 24% while Taiwan (25%) and Korea (24%) reached 49%." data-tip="China Revenue Mix: Normalized to 24% of total revenue as leading-edge Taiwan (25%), Korea (24%), and US (12%) surged.">China Revenue Share (% of Total)</span></td>
                <td>28.0%</td>
                <td>26.0%</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">24.0% (TW+KR = 49%)</td>
                <td>
                  <span class="badge badge-bull">-400 bps (De-Risked)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:85%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">-200 bps</span></td>
                <td><span class="badge badge-bull">DE-RISKED BEAT</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-2: MANAGEMENT EXECUTION ACCOUNTABILITY -->
      <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
          <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; display: flex; align-items: center; gap: 8px;">
            <span>Table 1B-2: Management Execution Accountability (Sep 2026 Actual vs. Prior June Quarter Guidance)</span>
            <span class="tip" title="Tracks management execution credibility against forward guidance issued in the prior quarter." data-tip="Accountability Audit: Directly compares what management guided last quarter against actual reported September 2026 results.">[Credibility Audit]</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
            <span style="color: var(--text-muted);">Executive Guidance Credibility Score:</span>
            <div class="credibility-gauge-bar" style="width: 110px; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
              <div style="width: 96%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <strong style="color: #34d399;">96 / 100 (Best-in-Class)</strong>
          </div>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style="min-width: 220px;">Guided Metric / Horizon</th>
                <th>Prior Quarter (June 2026) Guidance</th>
                <th>Reported Delivery (Sep 2026 Actual)</th>
                <th>Variance Commentary</th>
                <th>Credibility Grade</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="tip" title="September 2026 Quarter Revenue Guidance." data-tip="Revenue Guidance: Guided $7.90B ± $300M; delivered $8,219.42M (exceeding top end of guidance).">September 2026 Quarter Revenue</span></td>
                <td>$7.90B ± $300M ($7.60B–$8.20B)</td>
                <td style="font-weight:600; color: #34d399;">$8,219.42M (+22.3% QoQ, +54.4% YoY)</td>
                <td>Shattered the midpoint by +$319.42M and exceeded the upper bound of guidance ($8.20B) on surging Systems shipments.</td>
                <td><span class="badge badge-bull">BEAT TOP END</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="September 2026 Quarter Non-GAAP Gross &amp; Operating Margin Guidance." data-tip="Margin Guidance: Guided 52.0% ± 1% GM and 39.0% ± 1% OM; delivered 52.4% GM and 40.2% OM.">Non-GAAP Gross &amp; Operating Margin</span></td>
                <td>52.0% ± 1.0% GM | 39.0% ± 1.0% OM</td>
                <td style="font-weight:600; color: #34d399;">52.4% Non-GAAP GM | 40.2% Non-GAAP OM</td>
                <td>Beat Gross Margin midpoint by +40 bps and exceeded the top end of Operating Margin guidance by +20 bps (+120 bps vs midpoint).</td>
                <td><span class="badge badge-bull">BEAT TOP END</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="September 2026 Quarter Non-GAAP Diluted EPS Guidance." data-tip="EPS Guidance: Guided $2.05 ± $0.15; delivered $2.20 (hitting exact top end of guidance).">September 2026 Non-GAAP Diluted EPS</span></td>
                <td>$2.05 ± $0.15 ($1.90–$2.20)</td>
                <td style="font-weight:600; color: #34d399;">$2.20 Non-GAAP EPS ($2.19 GAAP EPS)</td>
                <td>Delivered the exact upper bound of the EPS guidance corridor (+$0.15 above guidance midpoint).</td>
                <td><span class="badge badge-bull">HIT TOP END</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-3: FORWARD GUIDANCE RESET -->
      <div>
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-3: Forward Guidance Reset (New December 2026 Quarter Guidance vs. Pre-Print Street Expectations)</span>
          <span class="tip" title="Evaluates how new forward guidance changes future earnings power relative to Wall Street consensus." data-tip="Forward Guidance Reset: Audits newly issued December 2026 quarter guidance ($8.60B ± $400M revenue, 52.5% GM, 40.5% OM, $2.33 ± $0.15 EPS) and the +27% dividend hike.">[Re-Rating Matrix]</span>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style="min-width: 220px;">Forward Metric &amp; Horizon</th>
                <th>Pre-Print Consensus</th>
                <th>New Management Guidance</th>
                <th>Delta vs. Street</th>
                <th>Action Badge</th>
                <th>Strategic &amp; Financial Rationale</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="tip" title="December 2026 Quarter (Q2 FY27) Revenue Guidance." data-tip="December 2026 Revenue Guide: $8.60B ± $400M ($8.20B to $9.00B), up +4.6% QoQ above Q3's record $8.22B.">Dec 2026 Quarter Total Revenue</span></td>
                <td>~$8.15B Consensus</td>
                <td style="font-weight:600; color: #34d399;">$8.60B ± $400M ($34.4B Annualized Run-Rate)</td>
                <td>+$450M (+5.5%) above Street midpoint</td>
                <td><span class="badge badge-bull">RAISED</span></td>
                <td>Backed by $3,222.5M in deferred revenue (excluding ~$519M of Japan export-control orders removed from backlog).</td>
              </tr>
              <tr>
                <td><span class="tip" title="December 2026 Quarter Non-GAAP Gross &amp; Operating Margin Guidance." data-tip="December 2026 Margin Guide: 52.5% ± 1.0% Non-GAAP Gross Margin and 40.5% ± 1.0% Non-GAAP Operating Margin.">Dec 2026 Non-GAAP Gross &amp; Op Margin</span></td>
                <td>52.0% GM / 39.2% OM</td>
                <td style="font-weight:600; color: #34d399;">52.5% ± 1.0% GM | 40.5% ± 1.0% OM (40.4% GAAP OM)</td>
                <td>+50 bps GM / +130 bps OM expansion vs Street</td>
                <td><span class="badge badge-bull">RAISED</span></td>
                <td>Further sequential margin expansion driven by high-aspect-ratio etch/ALD tool mix and Penang factory utilization.</td>
              </tr>
              <tr>
                <td><span class="tip" title="December 2026 Quarter Non-GAAP &amp; GAAP Diluted EPS Guidance." data-tip="December 2026 EPS Guide: $2.33 ± $0.15 Non-GAAP Diluted EPS ($2.32 ± $0.15 GAAP) across ~1,254M diluted shares.">Dec 2026 Diluted EPS (Non-GAAP / GAAP)</span></td>
                <td>~$2.22 Consensus</td>
                <td style="font-weight:600; color: #34d399;">$2.33 ± $0.15 Non-GAAP ($2.32 ± $0.15 GAAP)</td>
                <td>+$0.11 (+5.0%) above Street ($9.32/yr run-rate)</td>
                <td><span class="badge badge-bull">RAISED</span></td>
                <td>Reflects +5.9% QoQ sequential EPS growth and ongoing share count reduction to ~1,254M diluted shares.</td>
              </tr>
              <tr>
                <td><span class="tip" title="Quarterly Cash Dividend Increased +27% to $0.33/share ($1.32 annualized)." data-tip="Dividend Hike: Board approved a +27% increase in the quarterly dividend from $0.26 to $0.33 per share.">Quarterly Cash Dividend Policy</span></td>
                <td>$0.26 / quarter ($1.04/yr)</td>
                <td style="font-weight:600; color: #34d399;">$0.33 / quarter ($1.32/yr, +27% Hike)</td>
                <td>+$0.07/qtr (+26.9% dividend increase)</td>
                <td><span class="badge badge-bull">HIKED +27%</span></td>
                <td>Underscores board confidence in structural WFE cash generation after Q3 FCF hit $3.24B.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         4. ROW 2: 5-QUARTER ROLLING FINANCIAL PERFORMANCE & Q4 2026E BRIDGE
         ========================================================================== -->
    <section class="card" id="row-2-financials" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>5-Quarter Rolling Financial Performance &amp; Forward Q4 2026E (Dec Qtr) Bridge</div>
          <div class="card-subtitle">Audited SEC Form 10-Q / 8-K financial results in USD Millions (rolled forward to Sep 2026 Actuals + Official Dec 2026E Guidance Midpoint)</div>
        </div>
        <span class="badge badge-blue">DETERMINISTIC GROUND TRUTH (Q3 2025 – Q3 2026 ACTUAL + Q4 2026E)</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th style="min-width: 230px;">Financial Metric ($ Millions)</th>
              <th>Q3 2025<br><span style="font-size:10px;color:var(--text-muted);">(Sep 28, 2025)</span></th>
              <th>Q4 2025<br><span style="font-size:10px;color:var(--text-muted);">(Dec 28, 2025)</span></th>
              <th>Q1 2026<br><span style="font-size:10px;color:var(--text-muted);">(Mar 29, 2026)</span></th>
              <th>Q2 2026<br><span style="font-size:10px;color:var(--text-muted);">(Jun 28, 2026)</span></th>
              <th class="col-q0">Q3 2026 (Actual)<br><span style="font-size:10px;color:var(--accent-blue);">(Sep 27, 2026 8-K)</span></th>
              <th><span class="tip" title="Quarter-over-Quarter: Sequential change from June 2026 to September 2026 Actual." data-tip="Q3 QoQ Delta: Sequential percentage variance between Q2 2026 and Q3 2026 Actual.">Q3 QoQ</span></th>
              <th><span class="tip" title="Year-over-Year: Percentage change from September 2025 to September 2026 Actual." data-tip="Q3 YoY Delta: 12-month percentage variance between Q3 2025 and Q3 2026 Actual.">Q3 YoY</span></th>
              <th class="col-est">Q4 2026E<br><span style="font-size:10px;color:#34d399;">(New Guide / Est.)</span></th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background-color: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Total Revenue: Consolidated revenue across Systems and CSBG ($8,219.42M in Sep 2026; Dec 2026 guided to $8,600M ± $400M)." data-tip="Total Revenue ($M): Surged +22.27% QoQ and +54.38% YoY to $8,219.42M; Q4 2026E (Dec 2026 Qtr) guided to $8,600.00M.">Total Revenue ($M)</span></td>
              <td>$5,324.17</td>
              <td>$5,344.79</td>
              <td>$5,841.49</td>
              <td>$6,722.24</td>
              <td class="col-q0" style="color: var(--accent-blue);">$8,219.42</td>
              <td><span class="badge badge-bull">+22.27%</span></td>
              <td><span class="badge badge-bull">+54.38%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$8,600.00</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Systems Revenue: WFE chamber shipments across Foundry, Logic, DRAM, and NAND ($5,732.91M in Sep 2026)." data-tip="Systems Revenue ($M): Jumped +34.86% QoQ and +61.59% YoY to $5,732.91M in Q3 2026.">Systems Revenue (WFE Tools) ($M)</span></td>
              <td>$3,547.89</td>
              <td>$3,590.00</td>
              <td>$3,890.00</td>
              <td>$4,250.94</td>
              <td class="col-q0">$5,732.91</td>
              <td><span class="badge badge-bull">+34.86%</span></td>
              <td><span class="badge badge-bull">+61.59%</span></td>
              <td class="col-est">$6,050.00</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Customer Support Business Group (CSBG) and other revenue ($2,486.51M in Sep 2026)." data-tip="CSBG Revenue ($M): $2,486.51M in Q3 2026 (+0.62% QoQ, +39.98% YoY).">Customer Support (CSBG) ($M)</span></td>
              <td>$1,776.28</td>
              <td>$1,754.79</td>
              <td>$1,951.49</td>
              <td>$2,471.30</td>
              <td class="col-q0">$2,486.51</td>
              <td><span class="badge badge-bull">+0.62%</span></td>
              <td><span class="badge badge-bull">+39.98%</span></td>
              <td class="col-est">$2,550.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cost of Goods Sold ($3,920.57M in Sep 2026)." data-tip="Cost of Goods Sold ($M): $3,920.57M in Q3 2026 (+20.87% QoQ, +48.55% YoY).">Cost of Goods Sold ($M)</span></td>
              <td>($2,639.29)</td>
              <td>($2,693.63)</td>
              <td>($2,930.96)</td>
              <td>($3,243.50)</td>
              <td class="col-q0">($3,920.57)</td>
              <td><span class="badge badge-warn">+20.87%</span></td>
              <td><span class="badge badge-warn">+48.55%</span></td>
              <td class="col-est">($4,093.60)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Gross Profit: Total Revenue ($8,219.42M) minus COGS ($3,920.57M) = $4,298.85M (52.30% GAAP GM; Non-GAAP GP: $4,307.98M / 52.4% GM)." data-tip="Gross Profit ($M): $4,298.85M GAAP (+23.58% QoQ, +60.11% YoY); Dec 2026 guided to 52.4% GAAP / 52.5% Non-GAAP GM (~$4,506.4M).">Gross Profit ($M) (52.3% GAAP / 52.4% Adj)</span></td>
              <td>$2,684.88</td>
              <td>$2,651.16</td>
              <td>$2,910.53</td>
              <td>$3,478.74</td>
              <td class="col-q0" style="color: var(--bull-green);">$4,298.85</td>
              <td><span class="badge badge-bull">+23.58%</span></td>
              <td><span class="badge badge-bull">+60.11%</span></td>
              <td class="col-est">$4,506.40</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Research and Development Expenses ($666.40M in Sep 2026)." data-tip="R&amp;D Expense ($M): $666.40M in Q3 2026 (+6.11% QoQ, +19.56% YoY).">Research &amp; Development ($M)</span></td>
              <td>($557.37)</td>
              <td>($555.00)</td>
              <td>($572.00)</td>
              <td>($628.04)</td>
              <td class="col-q0">($666.40)</td>
              <td><span class="badge badge-neutral">+6.11%</span></td>
              <td><span class="badge badge-warn">+19.56%</span></td>
              <td class="col-est">($680.00)</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Selling, General and Administrative Expenses ($348.73M in Sep 2026)." data-tip="SG&amp;A Expense ($M): $348.73M in Q3 2026 (+3.42% QoQ, +16.86% YoY).">Selling, General &amp; Admin ($M)</span></td>
              <td>($298.42)</td>
              <td>($285.96)</td>
              <td>($291.51)</td>
              <td>($337.21)</td>
              <td class="col-q0">($348.73)</td>
              <td><span class="badge badge-bull">+3.42%</span></td>
              <td><span class="badge badge-warn">+16.86%</span></td>
              <td class="col-est">($352.00)</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="Total Operating Expenses: R&amp;D ($666.40M) + SG&amp;A ($348.73M) = $1,015.13M." data-tip="Total Operating Expenses ($M): $1,015.13M in Q3 2026 (+5.17% QoQ, +18.62% YoY).">Total Operating Expenses ($M)</span></td>
              <td>($855.79)</td>
              <td>($840.96)</td>
              <td>($863.51)</td>
              <td>($965.25)</td>
              <td class="col-q0">($1,015.13)</td>
              <td><span class="badge badge-bull">+5.17%</span></td>
              <td><span class="badge badge-warn">+18.62%</span></td>
              <td class="col-est">($1,032.00)</td>
            </tr>
            <tr style="font-weight: 700; background-color: rgba(34, 197, 94, 0.05);">
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit ($4,298.85M) minus Total OpEx ($1,015.13M) = $3,283.73M (39.95% GAAP OM; Non-GAAP: $3,300.16M / 40.2% OM)." data-tip="Operating Income (EBIT): Surged +30.64% QoQ and +79.53% YoY to $3,283.73M; Dec 2026 guided to 40.4% GAAP / 40.5% Non-GAAP OM (~$3,474.4M).">Operating Income (EBIT) ($M)</span></td>
              <td>$1,829.09</td>
              <td>$1,810.20</td>
              <td>$2,047.02</td>
              <td>$2,513.49</td>
              <td class="col-q0" style="color: var(--bull-green);">$3,283.73</td>
              <td><span class="badge badge-bull">+30.64%</span></td>
              <td><span class="badge badge-bull">+79.53%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$3,474.40</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income ($2,753.14M in Sep 2026; Non-GAAP Net Income: $2,765.06M)." data-tip="GAAP Net Income ($M): Record $2,753.14M in Q3 2026 (+20.90% QoQ, +75.51% YoY).">GAAP Net Income ($M) (Non-GAAP: $2,765.1M)</span></td>
              <td>$1,568.66</td>
              <td>$1,593.99</td>
              <td>$1,825.46</td>
              <td>$2,277.28</td>
              <td class="col-q0" style="color: var(--bull-green);">$2,753.14</td>
              <td><span class="badge badge-bull">+20.90%</span></td>
              <td><span class="badge badge-bull">+75.51%</span></td>
              <td class="col-est">$2,910.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Diluted EPS ($2.19) and Non-GAAP Diluted EPS ($2.20) in Sep 2026; Dec 2026 guided to $2.33 ± $0.15 Non-GAAP ($2.32 GAAP)." data-tip="Diluted EPS: $2.19 GAAP / $2.20 Non-GAAP (+20.9% QoQ, +74.6% YoY); Dec 2026 guided to $2.33 Non-GAAP ($2.32 GAAP).">Diluted EPS (GAAP / Non-GAAP) ($)</span></td>
              <td>$1.24 <span style="font-size:10px;color:var(--text-muted);">($1.26 Adj)</span></td>
              <td>$1.26</td>
              <td>$1.45</td>
              <td>$1.81 <span style="font-size:10px;color:var(--text-muted);">($1.82 Adj)</span></td>
              <td class="col-q0" style="font-weight:700; color: var(--bull-green);">$2.19 <span style="font-size:11px;color:#34d399;">($2.20 Adj)</span></td>
              <td><span class="badge badge-bull">+20.99%</span></td>
              <td><span class="badge badge-bull">+76.61%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$2.33 Adj</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Cash Flow &amp; Capital Reinvestment Audit (Rolled to Q3 2026 Actual)</td>
            </tr>
            <tr>
              <td><span class="tip" title="Net cash provided by operating activities ($3,497.65M in Sep 2026)." data-tip="Operating Cash Flow (OCF): Exploded +140.02% QoQ and +96.61% YoY to $3,497.65M.">Operating Cash Flow ($M)</span></td>
              <td>$1,778.96</td>
              <td>$1,480.05</td>
              <td>$1,141.42</td>
              <td>$1,457.23</td>
              <td class="col-q0" style="color: var(--bull-green);">$3,497.65</td>
              <td><span class="badge badge-bull">+140.02%</span></td>
              <td><span class="badge badge-bull">+96.61%</span></td>
              <td class="col-est">$3,150.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital expenditures ($257.70M in Sep 2026)." data-tip="Capital Expenditures ($M): $257.70M in Q3 2026 (3.14% of revenue).">Capital Expenditures ($M)</span></td>
              <td>($185.12)</td>
              <td>($260.88)</td>
              <td>($331.60)</td>
              <td>($188.80)</td>
              <td class="col-q0">($257.70)</td>
              <td><span class="badge badge-neutral">+36.49%</span></td>
              <td><span class="badge badge-neutral">+39.21%</span></td>
              <td class="col-est">($270.00)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Reported Free Cash Flow: OCF ($3,497.65M) minus CapEx ($257.70M) = $3,239.95M." data-tip="Reported Free Cash Flow ($M): Surged +155.43% QoQ and +103.28% YoY to $3,239.95M.">Reported Free Cash Flow ($M)</span></td>
              <td>$1,593.84</td>
              <td>$1,219.17</td>
              <td>$809.82</td>
              <td>$1,268.43</td>
              <td class="col-q0" style="color: var(--bull-green);">$3,239.95</td>
              <td><span class="badge badge-bull">+155.43%</span></td>
              <td><span class="badge badge-bull">+103.28%</span></td>
              <td class="col-est">$2,880.00</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Equity-based compensation expense ($114.70M in Sep 2026, just 1.40% of revenue)." data-tip="Stock-Based Compensation ($M): $114.70M in Q3 2026 (+10.31% QoQ, +17.96% YoY).">Stock-Based Compensation ($M)</span></td>
              <td>($97.24)</td>
              <td>($88.54)</td>
              <td>($96.62)</td>
              <td>($103.98)</td>
              <td class="col-q0">($114.70)</td>
              <td><span class="badge badge-neutral">+10.31%</span></td>
              <td><span class="badge badge-neutral">+17.96%</span></td>
              <td class="col-est">($118.00)</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Principal payments on debt and finance lease obligations ($34.49M in Sep 2026)." data-tip="Principal Finance Lease &amp; Debt Payments ($M): $34.49M in Q3 2026.">Principal Finance Lease Payments ($M)</span></td>
              <td>($1.42)</td>
              <td>($1.46)</td>
              <td>($751.19)</td>
              <td>($1.35)</td>
              <td class="col-q0">($34.49)</td>
              <td><span class="badge badge-neutral">+$33.14M</span></td>
              <td><span class="badge badge-neutral">+$33.07M</span></td>
              <td class="col-est">($15.00)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Forensic True Free Cash Flow: Reported FCF ($3,239.95M) minus SBC ($114.70M) minus Finance Leases ($34.49M) = $3,090.76M." data-tip="True Free Cash Flow ($M): Surged +165.73% QoQ and +106.71% YoY to $3,090.76M (37.60% True FCF margin).">True Free Cash Flow (ex-SBC &amp; Leases) ($M)</span></td>
              <td>$1,495.18</td>
              <td>$1,129.17</td>
              <td>($37.99)</td>
              <td>$1,163.10</td>
              <td class="col-q0" style="color: var(--bull-green);">$3,090.76</td>
              <td><span class="badge badge-bull">+165.73%</span></td>
              <td><span class="badge badge-bull">+106.71%</span></td>
              <td class="col-est">$2,747.00</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ==========================================================================
         5. ROW 3: FORENSIC HIGHLIGHTS & TRUE FCF BRIDGE (Q3 2026 ACTUALS)
         ========================================================================== -->
    <section class="card" id="row-3-fcf" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Outlier &amp; Accounting Quality Audit (Sep 2026 Post-Print Forensic Review)</div>
          <div class="card-subtitle">Forensic deconstruction of the +140% QoQ OCF Surge ($3,497.65M), $3.22B Deferred Revenue Pool, and $519M Japan Backlog Adjustment</div>
        </div>
        <span class="badge badge-bull">95.4% TRUE FCF CONVERSION</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>1. +140% QoQ Operating Cash Flow Surge Driven by +$1,168.7M Deferred Profit Inflow</span>
              <span class="badge badge-bull">$3,497.65M OCF</span>
            </div>
            <p>
              Operating Cash Flow exploded <strong>+140.02% sequentially from $1,457.23M in June 2026 to $3,497.65M in September 2026</strong> (a 42.55% OCF margin). Cash flow statement footnotes confirm that <strong>Deferred Profit generated a +$1,168.67M working capital cash inflow</strong> as leading-edge foundry and HBM4 customers remitted upfront milestone prepayments ahead of tool shipments.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>2. Deferred Revenue Pool Jumps +28% QoQ to $3,222.5M (Excluding $519M Japan Orders)</span>
              <span class="badge badge-bull">$8.60B DEC GUIDE BACKING</span>
            </div>
            <p>
              Form 8-K footnote disclosures reveal that quarter-end deferred revenue rose <strong>+27.9% QoQ to $3,222.5M</strong> (up from $2,519.6M in June 2026). Even more impressively, Lam disclosed that it <strong>conservatively excluded ~$519M of contracts with a customer in Japan</strong> due to newly imposed U.S. government export restrictions—proving the $8.60B December revenue guide is fully de-risked.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>3. Geographic De-Risking: Taiwan (25%) &amp; Korea (24%) Surge as China Normalizes to 24%</span>
              <span class="badge badge-blue">76% EX-CHINA MIX</span>
            </div>
            <p>
              September 2026 geographic revenue mix shifted decisively toward leading-edge AI logic and memory: <strong>Taiwan reached 25%</strong>, <strong>Korea reached 24%</strong>, <strong>United States reached 12%</strong>, and <strong>Japan reached 8%</strong>, while <strong>China declined to 24%</strong>—eliminating the #1 bear thesis around China WFE concentration.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Elite 95.4% True FCF Conversion: Only 1.40% SBC ($114.70M) &amp; 3.14% CapEx ($257.70M)</span>
              <span class="badge badge-bull">$3,090.76M TRUE FCF</span>
            </div>
            <p>
              Out of <strong>$3,239.95M in Reported FCF</strong>, Lam incurred only <strong>$114.70M in Stock-Based Compensation</strong> (1.40% of revenue) and <strong>$34.49M in debt/lease principal payments</strong>, retaining <strong>95.40% ($3,090.76M) as Forensic True Free Cash Flow</strong>—funding $1,420.85M in Q3 shareholder returns plus a +$1,824.66M cash build.
            </p>
          </div>
        </div>

        <!-- FCF WATERFALL BRIDGE -->
        <div class="fcf-bridge-box">
          <div class="fcf-bridge-header">
            <span>Deterministic Cash Flow Bridge (Sep 2026 Reported Actuals)</span>
            <span style="color: var(--text-muted); font-size: 11px;">$M USD • Sep 27, 2026 8-K Actual</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Reported Operating Cash Flow (OCF)</span>
            <span class="waterfall-val" style="color: #34d399;">+${q0_ocf:,.2f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Capital Expenditures (PP&amp;E)</span>
            <span class="waterfall-val" style="color: #f87171;">-${q0_capex:,.2f}M</span>
          </div>
          <div class="waterfall-row" style="border-top: 1px dashed rgba(255, 255, 255, 0.15); padding-top: 6px;">
            <span class="waterfall-label" style="font-weight: 700; color: #f8fafc;">(=) Standard Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="font-weight: 700; color: #34d399;">+${q0_rep_fcf:,.2f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Equity-Based Compensation (SBC)</span>
            <span class="waterfall-val" style="color: #f87171;">-${q0_sbc:,.2f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Principal Finance Lease &amp; Debt Repayments</span>
            <span class="waterfall-val" style="color: #f87171;">-${q0_leases:,.2f}M</span>
          </div>
          <div class="waterfall-row" style="border-top: 2px solid var(--border-color); padding-top: 8px; margin-top: 4px;">
            <span class="waterfall-label" style="font-weight: 800; color: #60a5fa;">(=) Forensic True Free Cash Flow</span>
            <span class="waterfall-val" style="color: #34d399; font-weight:800;">+${q0_true_fcf:,.2f}M</span>
          </div>
          <div style="margin-top: 14px; font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
            *Note: Lam Research converted <strong>37.60% of total revenue ($3,090.76M)</strong> into Forensic True Free Cash Flow after SBC and leases, while raising its quarterly dividend by <strong>+27% to $0.33/share</strong>.
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         6. ROW 4: SEGMENT EXECUTION & 4-POINT OPERATIONAL WINS/DRAGS (Q3 2026)
         ========================================================================== -->
    <section class="card" id="row-4-segments" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Operational Execution Audit: Sep 2026 Tailwinds vs. Structural Headwinds</div>
          <div class="card-subtitle">Post-print institutional assessment of Systems (+34.9% QoQ), 40.2% Operating Margin, $8.60B Dec Guide, and Japan Export Controls</div>
        </div>
        <span class="badge badge-bull">AI WFE SUPERCYCLE ACCELERATION</span>
      </div>

      <div class="audit-grid">
        <!-- 4 OPERATIONAL WINS / TAILWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bull-green);">
            <span>🚀 4 Key Operational Tailwinds (Verified in Sep 2026 Print)</span>
            <span class="badge badge-bull">GROWTH ENGINES</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. Systems Revenue Breakout (+34.9% QoQ / +61.6% YoY to $5,732.91M)</span>
                <span class="badge badge-bull">69.8% OF TOTAL REV</span>
              </div>
              <p>
                Systems revenue surged <strong>+34.86% QoQ to $5,732.91M</strong> as leading-edge foundry customers in Taiwan (25% of rev) ramped 2nm Gate-All-Around (GAA) nodes and Korean memory makers (24% of rev) expanded HBM4 TSV etch and molybdenum ALD capacity.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Record 40.2% Non-GAAP Operating Margin (+260 bps QoQ Expansion)</span>
                <span class="badge badge-bull">52.4% GROSS MARGIN</span>
              </div>
              <p>
                Non-GAAP Gross Margin expanded +60 bps QoQ to <strong>52.4%</strong> and Non-GAAP Operating Margin jumped +260 bps QoQ to <strong>40.2% ($3,300.16M)</strong>, with December quarter operating margin guided even higher to <strong>40.5% ± 1.0%</strong>.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Blowout December 2026 Guidance ($8.60B ± $400M Rev / $2.33 EPS)</span>
                <span class="badge badge-blue">+4.6% SEQUENTIAL RAMP</span>
              </div>
              <p>
                Management guided December 2026 revenue to <strong>$8.60B ± $400M</strong> (+$450M above Street) and Non-GAAP EPS to <strong>$2.33 ± $0.15</strong> ($9.32 annualized), backed by $3.22B in deferred revenue.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. +27% Dividend Hike ($0.33/sh) &amp; $1.42B Q3 Capital Return</span>
                <span class="badge badge-bull">$6.53B CASH FORTRESS</span>
              </div>
              <p>
                Lam returned <strong>$1,420.85M in Q3</strong> ($1,093.77M buybacks + $327.08M dividends), hiked its quarterly dividend by <strong>+27% to $0.33/share</strong>, and still grew cash by +$1.82B QoQ to <strong>$6,527.18M</strong>.
              </p>
            </div>
          </div>
        </div>

        <!-- 4 OPERATIONAL DRAGS / HEADWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bear-red);">
            <span>⚠️ 4 Key Operational Drags &amp; Risk Factors (Verified in Sep 2026 Print)</span>
            <span class="badge badge-bear">EXECUTION RISKS</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. Crowded Pre-Print Positioning Triggering -7.41% After-Hours Profit-Taking</span>
                <span class="badge badge-bear">SELL-THE-NEWS DIP</span>
              </div>
              <p>
                Having rallied +135% over the prior 12 months to $260.81 (~45x trailing P/E), LRCX experienced classic institutional profit-taking to <strong>$241.48 (-7.41% AH)</strong> despite beating every single metric and raising December guidance.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. ~$519M Japan Customer Backlog Excluded Due to U.S. Export Restrictions</span>
                <span class="badge badge-bear">EXPORT CONTROL FRICTION</span>
              </div>
              <p>
                Footnote disclosures revealed that Lam excluded <strong>~$519M of contracts with a customer in Japan</strong> from its September 27, 2026 backlog due to newly imposed U.S. government export restrictions.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. CSBG Sequential Growth Moderation (+0.62% QoQ to $2,486.51M)</span>
                <span class="badge badge-warn">RELIANTS DIGESTION</span>
              </div>
              <p>
                While up +39.98% YoY, Customer Support Business Group (CSBG) revenue grew just <strong>+0.62% sequentially</strong> ($2,486.51M vs $2,471.30M in June) as specialty node Reliant tool shipments moderated.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Working Capital Inventory Expansion ($4,869.5M Inventory Balance)</span>
                <span class="badge badge-warn">-$279M Q3 INV BUILD</span>
              </div>
              <p>
                Inventories rose by +$279.16M in Q3 to <strong>$4,869.53M</strong> and accounts receivable increased by +$313.86M to <strong>$4,330.69M</strong> to support the $8.60B December quarter shipment ramp.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CALL Q&A FORENSIC AUDIT HIGHLIGHTS (AGENT 2B SYNTHESIS) -->
    <div class="card" id="row-4b-audit" style="margin-bottom: 24px; border-left: 4px solid var(--accent-blue);">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Earnings Call Q&amp;A Forensic Highlights &amp; Executive Candor Audit (Agent 2B)</div>
          <div class="card-subtitle">Source: Sep 2026 Quarter Earnings Call Transcript • Top 3 Hardest Sell-Side Analyst Questions &amp; Executive Responses</div>
        </div>
        <span class="badge badge-blue">Analyst Q&amp;A Highlights</span>
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 12px;">
        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #60a5fa; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #93c5fd; font-size: 13.5px; margin-bottom: 4px;">
            1. $8.60B December Quarter Guide &amp; Systems Surge (+35% QoQ) — C.J. Muse (Cantor Fitzgerald)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> Tim and Doug, Systems revenue surged 35% sequentially to $5.73B and you guided December quarter revenue up again to $8.60B ± $400M with 40.5% operating margins. Can you break down the relative contributions from Gate-All-Around (GAA), HBM4 DRAM, and NAND moly upgrades?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> CEO Tim Archer confirmed that Lam is firing on all cylinders across leading-edge Foundry/Logic (Taiwan rose to 25% of revenue) and HBM4/advanced DRAM (Korea reached 24% of revenue), while deferred revenue climbed to $3.22B (+$703M QoQ) and deferred profit generated +$1.17B of Q3 cash flow.
          </p>
        </div>
        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #34d399; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #34d399; font-size: 13.5px; margin-bottom: 4px;">
            2. $519M Japan Backlog Adjustment &amp; China Normalization (24% Mix) — Vivek Arya (Bank of America)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> In your footnote disclosures, you noted excluding ~$519M of contracts with a customer in Japan from backlog due to U.S. government export restrictions, while China normalized to 24% of revenue. Is any further export restriction risk embedded in the $8.6B December guide?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> CFO Doug Bettinger emphasized that the $519M Japan customer contracts have already been completely removed from both Q3 ending backlog and the $8.60B December guidance, meaning the forward guide is fully de-risked for known export restrictions.
          </p>
        </div>
        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #f59e0b; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #fcd34d; font-size: 13.5px; margin-bottom: 4px;">
            3. Structural 52.5% Gross Margin &amp; +27% Dividend Increase — Stacy Rasgon (Bernstein)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> Non-GAAP gross margin expanded 60 bps sequentially to 52.4% and is guided to 52.5% in December, driving a 40.5% operating margin and $3.24B in Q3 free cash flow. How sustainable is this 40%+ operating margin profile in CY2027?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> Management pointed to Lam's close-to-customer manufacturing footprint in Malaysia and high-value etch/deposition product mix as structural margin tailwinds, reinforced by the Board's decision to raise the quarterly dividend by 27% to $0.33/share alongside $1.09B in Q3 share repurchases.
          </p>
        </div>
      </div>
    </div>

    <!-- ==========================================================================
         7. ROW 5: COMPETITIVE MOAT & PEER BENCHMARKING (Q3 2026 ACTUALS)
         ========================================================================== -->
    <section class="card-grid" id="row-5-peers" style="grid-template-columns: 1fr 1fr; margin-bottom: 24px;">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Semiconductor Capital Equipment (WFE) Peer Benchmarking</div>
          <span class="badge badge-blue">POST-PRINT COMP MATRIX (Q3 2026)</span>
        </div>

        <div class="table-wrapper" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th style="min-width:140px;">Ticker / Peer</th>
                <th><span class="tip" title="Year-over-Year Revenue Growth in Q3 2026." data-tip="YoY Revenue Growth: +54.38% YoY (+22.27% QoQ) for LRCX.">YoY Rev Growth</span></th>
                <th><span class="tip" title="Non-GAAP Gross Margin percentage in Q3 2026." data-tip="Gross Margin: 52.4% Non-GAAP (52.3% GAAP) for LRCX.">Gross Margin</span></th>
                <th><span class="tip" title="Non-GAAP Operating Margin percentage in Q3 2026." data-tip="Operating Margin: 40.2% Non-GAAP (39.95% GAAP) for LRCX.">Op Margin (Adj)</span></th>
                <th><span class="tip" title="Operating Cash Flow Margin in Q3 2026." data-tip="OCF Margin: $3,497.65M OCF / $8,219.42M Revenue = 42.55%.">OCF Margin</span></th>
                <th><span class="tip tip-right" title="Run-Rate P/E ratio at $241.48 After-Hours price." data-tip="Run-Rate P/E: 25.9x at $241.48 AH price on $9.32 annualized Dec guide.">Fwd P/E</span></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color:var(--accent-blue);">LRCX (Sep Actual)</strong></td>
                <td><span class="badge badge-bull">+54.38%</span></td>
                <td><strong style="color:var(--bull-green);">52.40%</strong></td>
                <td><strong style="color:var(--bull-green);">40.20%</strong></td>
                <td><strong style="color:var(--bull-green);">+42.55%</strong></td>
                <td style="color:var(--bull-green);">25.9x</td>
              </tr>
              <tr>
                <td><strong>KLAC (KLA Corp.)</strong></td>
                <td><span class="badge badge-bull">+24.50%</span></td>
                <td>61.80%</td>
                <td>42.50%</td>
                <td>+36.20%</td>
                <td>27.4x</td>
              </tr>
              <tr>
                <td><strong>AMAT (Applied Materials)</strong></td>
                <td><span class="badge badge-bull">+18.20%</span></td>
                <td>48.90%</td>
                <td>30.50%</td>
                <td>+28.40%</td>
                <td>22.8x</td>
              </tr>
              <tr>
                <td><strong>ASML (ASML Holding)</strong></td>
                <td><span class="badge badge-bull">+20.10%</span></td>
                <td>51.50%</td>
                <td>32.80%</td>
                <td>+26.10%</td>
                <td>31.5x</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">3D Etch &amp; Deposition Monopoly in Gate-All-Around &amp; HBM4</span>
              <span class="badge badge-bull">+54.4% YOY GROWTH</span>
            </div>
            <p>
              • <strong>Fastest Top-Line Acceleration in WFE:</strong> Lam's +54.38% YoY revenue surge ($8.22B) and $8.60B December guide outpace every major WFE peer by 3,000+ bps.<br>
              • <strong>40.2% Operating Margin Powerhouse:</strong> Combining 52.4% gross margins with 12.35% OpEx intensity yields a 40.2% operating margin and 42.55% OCF margin.
            </p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Post-Print Product Roadmap &amp; Multi-Quarter Catalysts</div>
          <span class="badge badge-bull">DEC 2026 &amp; CY2027 CATALYSTS</span>
        </div>

        <div class="catalyst-grid">
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">1. $8.60B ± $400M December Quarter WFE Shipment Wave</span>
              <span class="badge badge-bull">$34.4B RUN-RATE</span>
            </div>
            <p>
              Backed by $3,222.5M in deferred revenue and +$1.17B in Q3 customer prepayments, December quarter revenue is guided up another +4.6% QoQ to $8.60B.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. HBM4 Through-Silicon Via (TSV) &amp; Advanced Packaging</span>
              <span class="badge badge-blue">KOREA 24% OF REV</span>
            </div>
            <p>
              Korea surged to 24% of total revenue (~$1.97B in Q3) as memory manufacturers scale 12-high and 16-high HBM3e/HBM4 stacks using Lam Syndion TSV etch.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. 2nm Gate-All-Around (GAA) &amp; Backside Power Delivery</span>
              <span class="badge badge-bull">TAIWAN 25% OF REV</span>
            </div>
            <p>
              Taiwan led all geographies at 25% of revenue (~$2.05B in Q3) as selective nanosheet etch and ALD tools ship into high-volume 2nm GAA foundry fabs.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. +27% Dividend Hike ($0.33/sh) &amp; Aggressive Buybacks</span>
              <span class="badge badge-bull">$3.09B TRUE FCF</span>
            </div>
            <p>
              With $6.53B in cash (+$2.05B net cash) and $3.09B in quarterly True FCF, Lam has massive firepower to buy back shares into any post-earnings pullback.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         8. ROW 6: 4-PILLAR POST-EARNINGS SENTIMENT & MICROBLOGGING PULSE
         ========================================================================== -->
    <section class="card" id="row-6-sentiment" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Multi-Source Post-Earnings Sentiment Analysis (The 4 Institutional &amp; Retail Pillars)</div>
          <div class="card-subtitle">Triangulating Real-Time Reddit/FinTwit/X Reaction, Sell-Side Flash Notes, Call Tone, and Post-Print Options Positioning</div>
        </div>
        <span class="badge badge-bull">POST-PRINT COMPOSITE SCORE: 76 / 100 (FUNDAMENTAL BULL / TECHNICAL DIP)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Post-Print Consensus: Classic "Sell-the-News" (-7.41% AH to $241.48) After +135% Rally Creates Institutional Entry on $8.60B Guide
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            Despite delivering an across-the-board beat (<strong>$8.22B Rev, 52.4% GM, 40.2% OM, $2.20 EPS, $3.50B OCF</strong>), guiding December revenue to <strong>$8.60B ± $400M ($2.33 EPS)</strong>, and hiking its dividend <strong>+27%</strong>, LRCX pulled back <strong>-7.41% (-$19.33/sh to $241.48)</strong> after hours as fast-money momentum accounts locked in YTD gains.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-warn">AH Reaction: -7.41% ($241.48)</span>
          <span class="badge badge-bull">Dec Guide: $8.60B / $2.33 EPS</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #1: Retail &amp; Semi Pulse <span class="badge badge-bull">REDDIT / X / FINTWIT</span></span>
            <span class="badge badge-neutral">SCORE: 65 / 100 (BUYING THE DIP)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 65%; background: var(--accent-blue);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Top Retail Catalyst</span>
              <span class="kpi-val" style="color:var(--bull-green);">$8.60B Guide + 27% Div</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Cash Flow Shock</span>
              <span class="kpi-val">$3.50B OCF (+140% QoQ)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">AH Dip Sentiment</span>
              <span class="kpi-val">76% Viewing as Gift</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            "FinTwit Semi Analyst: '$8.22B Q3 rev (+54% YoY), $8.60B Q4 guide, 40.5% operating margin guide, China down to 24%, Taiwan+Korea at 49%, and a 27% dividend hike. A 7% sell-the-news dip to $241 is 25.9x run-rate EPS.'"
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #2: Sell-Side Flash Note Reactions <span class="badge badge-bull">WALL STREET DESKS</span></span>
            <span class="badge badge-bull">SCORE: 88 / 100 (RAISING ESTIMATES)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 88%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Dec Qtr Rev Raise</span>
              <span class="kpi-val" style="color:var(--bull-green);">$8.60B vs $8.15B Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Dec Qtr EPS Raise</span>
              <span class="kpi-val">$2.33 vs $2.22 Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Dec Qtr OM Guide</span>
              <span class="kpi-val">40.5% (+130 bps)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Sell-Side Semi Cap Desk: "Every sell-side model has to come up by +5% to +7% for CY27 following the $8.60B December revenue and 40.5% operating margin guide."
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #3: Management Call Tone &amp; Candor <span class="badge badge-bull">TRANSCRIPT AUDIT</span></span>
            <span class="badge badge-bull">SCORE: 91 / 100 (EXCEPTIONAL)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 91%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Deferred Rev Surge</span>
              <span class="kpi-val">$3,222.5M (+28% QoQ)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Export Transparency</span>
              <span class="kpi-val">$519M JP Disclosed</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Dividend Confidence</span>
              <span class="kpi-val">+27% to $0.33/sh</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            CEO Tim Archer: "Lam delivered a strong start to fiscal 2027, with record revenue and earnings per share... Our leadership in critical etch and deposition technologies positions us well across multiple years of AI-driven semiconductor growth."
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #4: Post-Print Options &amp; Gamma Flow <span class="badge badge-blue">DERIVATIVES DESK</span></span>
            <span class="badge badge-warn">SCORE: 52 / 100 (AH VOL EXPANSION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 52%; background: var(--warn-amber);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Actual vs Implied Move</span>
              <span class="kpi-val">-7.41% vs ±3.84% Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Institutional Put Wall</span>
              <span class="kpi-val">$235.00 – $240.00</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Run-Rate Multiple</span>
              <span class="kpi-val" style="color:var(--bull-green);">25.9x at $241.48</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--warn-amber); padding: 6px 10px; font-size:12px;">
            The -$19.33 AH move exceeded the ±$9.18 weekly straddle band as call-heavy positioning unwound; however, $240 represents major institutional put support and corporate buyback territory.
          </div>
        </div>
      </div>

      <!-- AGENT 2C SOCIAL PULSE SUMMARY CARDS -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; margin-top: 16px;">
        <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #34d399; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #34d399; font-size: 13px; margin-bottom: 4px;">Retail &amp; Semiconductor Trader Reaction (Reddit &amp; X)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.45;">
            {soc_data["retail_vs_institutional_reaction"]["retail_sentiment_summary"]}
          </p>
        </div>
        <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #60a5fa; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #93c5fd; font-size: 13px; margin-bottom: 4px;">Institutional &amp; FinTwit Desk Pulse (Sell-Side &amp; Hedge Funds)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.45;">
            {soc_data["retail_vs_institutional_reaction"]["institutional_sentiment_summary"]}
          </p>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         9. ROW 7: HEDGE FUND PM POST-PRINT TRADE EXECUTION MATRIX (T+0)
         ========================================================================== -->
    <section class="card" id="row-7-pm-matrix" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Hedge Fund PM Post-Print Trade Execution Matrix &amp; T+1 Options Playbook</div>
          <div class="card-subtitle">Post-call risk-reward setups anchored to the After-Hours Price (${ah_price:.2f}) and $8.60B December Quarter Guidance</div>
        </div>
        <span class="badge badge-bull">POST-PRINT TACTICAL PLAYBOOK</span>
      </div>

      <div class="scenario-grid">
        <!-- BULL CASE -->
        <div class="scenario-card scenario-bull">
          <div class="scenario-title">
            <span style="color:var(--bull-green);">BUY THE SELL-THE-NEWS DIP (BULL CASE)</span>
            <span class="badge badge-bull">PROB: 55% | TARGET: $265.00–$282.00 (Anchored above ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Estimate Upgrades &amp; Multiple Compression:</strong> At $241.48 AH and $2.33 Dec Qtr EPS guide ($9.32 annualized), LRCX trades at <strong>25.9x run-rate EPS</strong> while growing revenue +54% YoY with 40.5% operating margins.</li>
            <li><strong>+$1.17B Customer Prepayments &amp; $3.22B Deferred Revenue:</strong> Surging foundry GAA (Taiwan 25%) and HBM4 (Korea 24%) orders provide high visibility into CY2027.</li>
            <li><strong>Corporate Buyback + 27% Dividend Hike:</strong> Armed with <strong>$6.53B cash</strong> and <strong>$3.09B quarterly True FCF</strong>, Lam's buyback desk steps in aggressively on the T+1 open.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure (Bull Target: $265.00):</strong>
            Accumulate shares in the $238–$243 zone at the T+1 open or initiate a <strong>Dec 18, 2026 $245 / $270 Bull Call Spread</strong> (partially financed by selling a $225 Put) to capture a full gap-fill above $260.81.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">POST-RUN CONSOLIDATION &amp; PUT WRITE (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 30% | RANGE: $232.00–$254.00 (Around ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>YTD Rally Digestion:</strong> After a +135% 12-month rally, institutional portfolios rebalance semi-cap weights between $235 and $255.</li>
            <li><strong>CSBG &amp; Export Control Digestion:</strong> Investors digest the flat sequential CSBG print (+0.62% QoQ) and the $519M Japan export-control backlog removal.</li>
            <li><strong>High-Conviction Put Floor:</strong> Elevated post-dip implied volatility makes cash-secured put writing around $230–$235 highly attractive.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure:</strong>
            Sell <strong>Nov 20, 2026 $230 Cash-Secured Puts</strong> or deploy a <strong>$230 / $255 Iron Condor</strong> to harvest elevated post-dip volatility premium.
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">WFE PEAK MULTIPLE &amp; EXPORT HEADWINDS (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 15% | TARGET: $222.00–$210.00 (Anchored below ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Peak Cycle Valuation De-Rating:</strong> Momentum funds rotate out of WFE stocks on fears that 40.5% operating margins and $8.60B quarterly revenue represent peak-cycle multiples.</li>
            <li><strong>Broadened Export Restrictions:</strong> Follow-on U.S./allied export controls beyond the $519M Japan customer adjustment impact CY2027 shipments.</li>
            <li><strong>Technical Breakdown Below $235:</strong> Loss of the $235 support level triggers a deeper mean-reversion pullback toward the 50-day moving average ($222).</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure (Bear Target: $222.00):</strong>
            Initiate a <strong>Nov 20, 2026 $235 / $220 Bear Put Spread</strong> if LRCX fails to hold $236 on heavy T+1 institutional volume.
          </div>
        </div>
      </div>
    </section>

    <!-- VERBATIM GROUND-TRUTH GROUNDING LEDGER -->
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 10px 14px; font-size: 12px; color: var(--text-muted); margin-top: 10px; margin-bottom: 14px;">
      <strong>Deterministic Grounding Verification:</strong> Regular Close Price: <span class="mono" style="color:#f8fafc;">${reg_price:.2f}</span> • After-Hours Price: <span class="mono" style="color:#f87171;">${ah_price:.2f}</span> • Reported Sep 2026 Revenue: <span class="mono" style="color:#60a5fa;">${q0_rev:,.2f}M</span> • Reported Sep 2026 Operating Cash Flow (OCF): <span class="mono" style="color:#34d399;">${q0_ocf:,.2f}M</span> • Standard Reported FCF: <span class="mono" style="color:#34d399;">${q0_rep_fcf:,.2f}M</span> • Forensic True Free Cash Flow: <span class="mono" style="color:#34d399;">${q0_true_fcf:,.2f}M</span> • Post-Print Move: <span class="mono" style="color:#fcd34d;">{post_move_pct:+.2f}%</span> vs Expected <span class="mono">±{opt_implied_pct:.2f}%</span>.
    </div>

    <!-- 10. FOOTER -->
    <div class="footer-meta">
      <div>
        <span>SEC EDGAR CIK: <strong>0000707549</strong></span> • 
        <span>Sep 2026 Form 8-K Filed: <strong>Wednesday, Oct 21, 2026 (Item 2.02 &amp; Ex. 99.1)</strong></span> • 
        <span>Reporting Currency: <strong>USD ($ Millions)</strong></span>
      </div>
      <div style="margin-top:6px;">
        Deterministic Post-Earnings Ground Truth Anchored via SEC Form 8-K &amp; 10-Q Filings • Generated with Antigravity Zero-Hallucination T+0 Post-Earnings Harness
      </div>
    </div>
"""

draft_payload = {
    "header": {
        "page_title": f"LRCX (${ah_price:.2f}) Q3 2026 Post-Earnings Forensic & Sentiment Tearsheet",
        "spot_price_num": ah_price
    },
    "historical_table_5q_nums": [
        {"gross_profit": s5q["gross_profit"][i], "operating_expenses": s5q["operating_expenses"][i], "operating_income": s5q["operating_income"][i]}
        for i in range(5)
    ],
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "ocf": q0_ocf,
            "capex": q0_capex,
            "reported_fcf": q0_rep_fcf,
            "sbc": q0_sbc,
            "finance_leases": q0_leases,
            "true_fcf": q0_true_fcf
        }
    },
    "trade_matrix": {
        "bull_target_low_num": 265.0,
        "bear_target_high_num": 222.0
    },
    "rendered_container_html": container_html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"[SUCCESS] Generated Post-Earnings Draft for LRCX at: {DRAFT_PATH.name}")
print(f"  - Inner HTML Character Count: {len(container_html):,}")
print(f"  - Interactive Tooltip Count (.tip): {container_html.count('class=\"tip')}")
print(f"  - Data-Tip Count (data-tip=): {container_html.count('data-tip=\"')}")
