"""
IBM Dedicated Post-Earnings Draft Builder (Track A + Track B Complete Re-Synthesis)
Builds drafts/IBM_2026-10-21_post_draft.json with 100% Q3 2026 (Actual) rolled 5-quarter tables,
Q4 2026E forward guidance columns, zero T-1 bleed-through, and Track B interactive enhancements.
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "IBM_2026-10-21_post_truth.json"
BUS_2A_PATH = BASE_DIR / "post_agent_bus" / "IBM_2026-10-21_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "post_agent_bus" / "IBM_2026-10-21_agent2b_transcript.json"
BUS_2C_PATH = BASE_DIR / "post_agent_bus" / "IBM_2026-10-21_agent2c_social.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "IBM_2026-10-21_post_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
kpis_data = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
trans_data = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
soc_data = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

reg_price = truth["post_print_reaction"]["regular_close_price"]      # 251.46
ah_price = truth["post_print_reaction"]["after_hours_price"]         # 239.80
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]  # -4.64
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] # 3.58
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 8.72)
verdict = truth["post_print_reaction"]["overall_print_verdict"]      # EPS BEAT & FCF RAISE

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]  # 17103.0
cons_rev = truth["t1_baseline"]["consensus_revenue_millions"]                 # 17550.0
q0_gaap_eps = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"]     # 2.31
q0_adj_eps = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"]   # 2.95
cons_eps = truth["t1_baseline"]["consensus_eps_nongaap"]                      # 2.87

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # 4025.0
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 486.0
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # 3539.0
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 535.0
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 120.0
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # 2884.0

s5q = truth["stitched_5q_chronological"]

container_html = f"""
    <!-- 1. HEADER BANNER (T+0 POST-EARNINGS FORENSIC TEARSHEET) -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#34d399;">Newly Reported Quarter: <strong>Q3 2026 (Ended Sep 30, 2026)</strong> • Forward Guidance Horizon: <strong>Q4 2026 &amp; FY2026</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">IBM</span>
            <h1 class="company-name">International Business Machines Corp.</h1>
            <span class="badge badge-bull">{verdict}</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="Immediate post-earnings release forensic analysis." data-tip="T+0 Post-Print: Forensic analysis synthesized immediately following the official Q3 2026 SEC Form 8-K release and earnings conference call.">T+0</span> POST-EARNINGS FORENSIC TEARSHEET</span>
          </div>
          <div class="sector-tag">NYSE • Enterprise Software (Red Hat, HashiCorp, watsonx Data), Hybrid Cloud Infrastructure &amp; Enterprise Consulting • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): 0000051143 assigned by the U.S. Securities and Exchange Commission (SEC) to IBM.">CIK</span>: 0000051143</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Regular Close / <span style="color:#f87171;">After-Hours Price</span></div>
            <div class="price-value">${reg_price:.2f} / <span style="color:#f87171;">${ah_price:.2f}</span> <span style="font-size:14px; color:#f87171;">({post_move_pct:+.2f}%)</span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total equity value at $239.80 after-hours price across 952M diluted shares." data-tip="Market Capitalization: Post-print equity value (~$228.3B at $239.80 AH / $236.9B regular close) vs $294.1B Enterprise Value.">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt ($66.44B) minus Cash &amp; Marketable Securities ($14.77B)." data-tip="Enterprise Value (EV): Reflects $66,440M total debt ($4,002M short-term + $62,438M long-term) minus $14,769M cash &amp; marketable securities.">EV</span></div>
            <div class="price-value">$236.9B / $294.1B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Q3 2026 SEC Form 8-K Filed</span>
          <span class="strip-val" style="color: var(--bull-green);">Wed, Oct 21, 2026 • <span class="tip" title="After Market Close: Official Q3 2026 earnings release filed via SEC Form 8-K Item 2.02." data-tip="Form 8-K Item 2.02 &amp; Exhibit 99.1 filed October 21, 2026 after market close; Webcast hosted at 5:00 PM ET.">8-K Verified</span></span>
          <span class="kpi-sub">Exhibit 99.1 &amp; Earnings Call Transcript Audited</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="Actual post-market stock reaction (-4.64%) compared against pre-print options straddle implied move (±3.58%)." data-tip="Actual vs. Implied Move: IBM traded down -4.64% (-$11.66/sh to $239.80) in after-hours action, slightly exceeding the ±3.58% (±$8.72/sh) ATM weekly straddle band on FX-dragged Consulting revenue ($5,335M) and IBM Z (-20% YoY).">Actual AH Move vs. Implied</span></span>
          <span class="strip-val" style="color: var(--warn-amber);">{post_move_pct:+.2f}% (vs ±{opt_implied_pct:.2f}% Est)</span>
          <span class="kpi-sub">-${reg_price - ah_price:.2f}/sh Actual vs ±${opt_straddle:.2f}/sh <span class="tip" title="At-The-Money weekly straddle price prior to earnings." data-tip="ATM Straddle: Pre-earnings weekly option straddle priced at ±$8.72/sh (3.58% implied move).">ATM Straddle</span></span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 GAAP Revenue ($17,103M, +5% YoY / +6% CC) vs Wall Street Consensus ($17,550M)." data-tip="Q3 2026 Revenue: Reported $17,103M (+4.73% YoY, +6% constant currency), led by Software ($7,804M, +8.2% YoY / +9% CC) while FX and Consulting softness weighed vs $17,550M consensus.">Revenue vs. Street</span></span>
          <span class="strip-val" style="color: var(--warn-amber);">$17.10B <span style="font-size:12px;">(+6% CC | -$447M vs Est)</span></span>
          <span class="kpi-sub">Street Est: $17.55B | Software: $7.80B (+9% CC)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 Operating Non-GAAP Diluted EPS ($2.95) and GAAP Diluted EPS ($2.31) vs Consensus ($2.87)." data-tip="Q3 2026 EPS Beat: Reported $2.95 Operating (Non-GAAP) Diluted EPS (+11% YoY), beating $2.87 Street consensus by +$0.08 (+2.79%), alongside $2.31 GAAP Diluted EPS (+26% YoY).">EPS (Non-GAAP / GAAP)</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$2.95 Adj / $2.31 <span class="tip" title="Generally Accepted Accounting Principles Diluted EPS ($2.31, up +26% YoY)." data-tip="GAAP Diluted EPS rose +26% YoY to $2.31 on $2,199M GAAP Net Income.">GAAP</span></span>
          <span class="kpi-sub">Beat $2.87 Consensus (+$0.08 / +2.8%) | Op Margin: 19.6% Adj</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">New FY2026 <span class="tip tip-right" title="Official Full-Year 2026 Free Cash Flow guidance raise issued in the Q3 2026 release." data-tip="FY2026 FCF Guidance Raise: Management raised full-year 2026 Free Cash Flow growth outlook to >$1.0B YoY increase (implies >$15.7B FY26 FCF) and reiterated >5% CC revenue growth.">Guidance Reset</span></span>
          <span class="strip-val" style="color: var(--bull-green);">FY26 FCF Raised (&gt;+$1.0B YoY)</span>
          <span class="kpi-sub">Reiterated &gt;5% CC FY26 Rev Growth | Red Hat +11% YoY</span>
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
      <a href="IBM_T1_2026-10-21.html" style="font-size: 11.5px; font-weight: 700; color: #93c5fd; text-decoration: none; padding: 5px 12px; border-radius: 6px; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.45); display: flex; align-items: center; gap: 6px;">
        ⇄ Compare Paired T-1 Pre-Earnings Briefing
      </a>
    </nav>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS — ALL ROLLED FORWARD TO Q3 2026 ACTUALS) -->
    <section class="kpi-grid" id="row-1-kpis">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Intensity (Q3 2026 Actual)</div>
          <span class="badge badge-bull">FY26 FCF GUIDE RAISED</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual GAAP cash generated from operations in Q3 2026 ($4,025M)." data-tip="Operating Cash Flow (OCF): Surged +54.99% QoQ and +30.60% YoY to $4,025M in Q3 2026 ($3,477M excluding Global Financing receivables).">Operating Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">9M YTD OCF: $11,791M (+28.1% YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$4,025M</span>
              <div class="delta-pair">
                <span class="badge badge-bull"><span class="tip" title="Sequential change from Q2 2026 ($2,597M) to Q3 2026 ($4,025M)." data-tip="QoQ OCF Delta: Surged +54.99% sequentially from $2,597M in Q2 2026.">QoQ</span> +54.99%</span>
                <span class="badge badge-bull"><span class="tip" title="Year-over-Year change from Q3 2025 ($3,082M) to Q3 2026 ($4,025M)." data-tip="YoY OCF Delta: Increased +30.60% from $3,082M in Q3 2025.">YoY</span> +30.60%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures in Q3 2026 ($486M)." data-tip="Capital Expenditures (CapEx): Asset-light software mix kept Q3 2026 CapEx at just $486M (2.84% of revenue).">Capital Expenditures</span> (Q3 2026)</span>
              <span class="kpi-sub">CapEx Intensity: Only 2.84% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">($486M)</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +26.89%</span>
                <span class="badge badge-neutral">YoY +16.55%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Standard Reported Free Cash Flow: OCF ($4,025M) minus CapEx ($486M) = $3,539M (IBM Non-GAAP FCF ex-GF receivables: $3,027M, up +28% YoY)." data-tip="Reported Free Cash Flow: $3,539M GAAP OCF minus CapEx (+59.85% QoQ, +32.80% YoY); IBM Non-GAAP FCF reached $3,027M (+28% YoY).">Reported Free Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">IBM Non-GAAP FCF: $3,027M (+28% YoY) | $8.51B YTD</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$3,539M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +59.85%</span>
                <span class="badge badge-bull">YoY +32.80%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forensic True Free Cash Flow: OCF ($4,025M) - CapEx ($486M) - SBC ($535M) - Finance Leases ($120M) = $2,884M." data-tip="True Free Cash Flow: Generated +$2,884M in Q3 2026 (+160.29% YoY) after deducting $535M SBC and $120M lease/debt principal.">True FCF (ex-SBC &amp; Leases)</span> (Q3 2026)</span>
              <span class="kpi-sub">Q3 SBC: $535M (3.1% of Rev) | Leases: $120M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$2,884M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +$5.38B</span>
                <span class="badge badge-bull">YoY +160.29%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING MARGINS (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Margins (Q3 2026 Actual)</div>
          <span class="badge badge-bull">58.5% NON-GAAP GROSS MARGIN</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Gross Profit ($9,714M, 56.80% margin) and Operating Non-GAAP Gross Profit ($10,004M, 58.5% margin)." data-tip="Gross Profit: $9,714M GAAP (56.8% margin) and $10,004M Non-GAAP (58.5% margin), powered by 83.2% Software segment gross margin.">Gross Profit</span> (Q3 2026)</span>
              <span class="kpi-sub">GAAP GM: 56.80% | Non-GAAP GM: 58.5% (Software: 83.2%)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$9,714M</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ -1.95%</span>
                <span class="badge badge-bull">YoY +3.78%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Operating Income ($2,880M, 16.84% margin) and Non-GAAP Pre-Tax Income ($3,355M, 19.6% margin)." data-tip="Operating Income (EBIT): $2,880M GAAP (+1.23% QoQ, +3.15% YoY); Operating Non-GAAP Pre-Tax Income rose +10% YoY to $3,355M (19.6% margin, +90 bps YoY).">Operating Income (EBIT)</span> (Q3 2026)</span>
              <span class="kpi-sub">Non-GAAP Pre-Tax: $3,355M (19.6% Margin, +90 bps YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$2,880M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +1.23%</span>
                <span class="badge badge-bull">YoY +3.15%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research, Development and Engineering ($2,378M) plus SG&amp;A ($4,620M) minus Other/IP ($164M) = $6,834M Total OpEx." data-tip="Total Operating Expenses: Declined -3.23% sequentially to $6,834M in Q3 2026 as SG&amp;A dropped -4.5% YoY ($4,620M) on internal AI productivity.">Operating Expense Discipline</span> (Q3 2026)</span>
              <span class="kpi-sub">R&amp;D: $2,378M (+17.5% YoY) | SG&amp;A: $4,620M (-4.5% YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$6,834M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ -3.23%</span>
                <span class="badge badge-neutral">YoY +4.05%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Non-GAAP Diluted EPS ($2.95, +11% YoY) and GAAP Diluted EPS ($2.31, +26% YoY on $2,199M GAAP Net Income)." data-tip="Net Income &amp; EPS: Operating Non-GAAP EPS reached $2.95 (+11% YoY, beating $2.87 consensus by +$0.08); GAAP Net Income jumped +26.09% YoY to $2,199M ($2.31 EPS).">Net Income &amp; EPS</span> (Q3 2026)</span>
              <span class="kpi-sub">Operating EPS: $2.95 (+11% YoY) | GAAP EPS: $2.31 (+26% YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$2,199M GAAP</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Adj EPS: $2.95</span>
                <span class="badge badge-bull">GAAP +26.1% YoY</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS & DIVIDEND (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet &amp; Capital Return (Q3 2026)</div>
          <span class="badge badge-bull">$14.77B CASH &amp; 2.8% DIVIDEND</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Cash &amp; cash equivalents ($13,572M), restricted cash ($154M), and marketable securities ($1,043M) as of September 30, 2026." data-tip="Liquid Reserves: $14,769M total cash and marketable securities on the Q3 2026 balance sheet (+$305M vs year-end 2025).">Cash &amp; Marketable Securities</span> (Q3 2026)</span>
              <span class="kpi-sub">Cash: $13,572M + Marketable Sec: $1,043M + Restr: $154M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$14,769M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">vs FY25 +2.11%</span>
                <span class="badge badge-bull">Strong Liquidity</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Short-term debt ($4,002M) plus Long-term debt ($62,438M) = $66,440M as of Sep 30, 2026." data-tip="Total Debt: $66,440M ($55,213M Core Debt + $11,227M Global Financing Debt) following software acquisition funding.">Total Debt (Core + Global Financing)</span></span>
              <span class="kpi-sub">Core Debt: $55,213M | Global Financing Debt: $11,227M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$66,440M</span>
              <div class="delta-pair">
                <span class="badge badge-warn">vs FY25 +8.29%</span>
                <span class="badge badge-neutral">A-/A3 Rated</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Quarterly Cash Dividends Paid ($1,583M in Q3 2026; $4,734M 9M YTD)." data-tip="Dividend Fortress: Paid $1,583M in Q3 cash dividends ($4,734M YTD), covered 2.24x by Q3 GAAP Free Cash Flow ($3,539M).">Quarterly Dividend &amp; Coverage</span> (Q3 2026)</span>
              <span class="kpi-sub">Q3 Dividends Paid: $1,583M ($4,734M 9M YTD)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,583M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">2.24x FCF Cover</span>
                <span class="badge badge-bull">~2.8% Yield</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Stockholders' Equity as of September 30, 2026 ($33,467M)." data-tip="Stockholders' Equity: Expanded to $33,467M as of Sep 30, 2026 (up +$1,073M from $32,394M at Dec 31, 2025).">Stockholders' Equity</span> (Q3 2026)</span>
              <span class="kpi-sub">Total Assets: $159,544M | Deferred Rev: $19,990M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$33,467M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">YTD +3.31%</span>
                <span class="badge badge-bull">+$1.07B YTD</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT CONTRIBUTIONS & SOFTWARE MIX (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Mix &amp; Software Flywheel (Q3 2026)</div>
          <span class="badge badge-blue">SOFTWARE 45.6% OF REV</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Software Segment Q3 2026 Revenue ($7,804M, +8.2% YoY / +9% CC) and Gross Margin (83.2%)." data-tip="Software Segment: $7,804M (45.63% of total revenue), led by Data (+19% YoY, +20% CC), Red Hat (+11% YoY, +12% CC), and Automation (+7% YoY, +8% CC).">Software Segment Share &amp; Growth</span> (Q3 2026)</span>
              <span class="kpi-sub">Rev: $7,804M (+9% CC) | Data +19% | Red Hat +11%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">45.63% / $7.80B</span>
              <div class="delta-pair">
                <span class="badge badge-bull">YoY +8.2% (+9% CC)</span>
                <span class="badge badge-bull">GM: 83.2%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Consulting Segment Q3 2026 Revenue ($5,335M, +0.2% YoY / +2% CC) and Gross Margin (28.9%)." data-tip="Consulting Segment: $5,335M (31.19% of revenue), up +2% in constant currency (Intelligent Operations +3% CC, Strategy &amp; Technology +1% CC).">Consulting Segment &amp; Margin</span> (Q3 2026)</span>
              <span class="kpi-sub">Rev: $5,335M (+2% CC) | Segment GM: 28.9%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">31.19% / $5.34B</span>
              <div class="delta-pair">
                <span class="badge badge-bull">+2.0% CC</span>
                <span class="badge badge-neutral">Reported +0.2%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Infrastructure Segment Q3 2026 Revenue ($3,707M, +4.2% YoY / +5% CC) and Gross Margin (52.5%)." data-tip="Infrastructure Segment: $3,707M (21.67% of revenue), as Distributed Infrastructure surged +31% YoY (+32% CC) to offset IBM Z (-20% YoY).">Infrastructure Segment</span> (Q3 2026)</span>
              <span class="kpi-sub">Rev: $3,707M (+5% CC) | Distributed Infra +31% YoY</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">21.67% / $3.71B</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Dist Infra +31%</span>
                <span class="badge badge-warn">IBM Z -20%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Post-print valuation multiples at $239.80 After-Hours price." data-tip="Post-Print Valuation: At $239.80 AH price, IBM trades at ~18.2x forward Operating EPS and ~14.5x raised FY26 Free Cash Flow (> $15.7B).">Post-Print Fwd P/E (at $239.80)</span></span>
              <span class="kpi-sub">P/FCF (on &gt;$15.7B FY26E): ~14.5x | EV/EBITDA: 15.8x</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">18.2x Fwd EPS</span>
              <div class="delta-pair">
                <span class="badge badge-bull">~6.9% FCF Yield</span>
                <span class="badge badge-bull">FCF Guide Raised</span>
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
            Source: IBM SEC Form 8-K (Item 2.02, Exhibit 99.1) Filed Oct 21, 2026 • Official Q3 2026 Earnings Release • Wall Street Consensus Comparison
          </div>
        </div>
        <div style="display:flex; gap: 8px; align-items:center;">
          <span class="badge badge-bull">$2.95 OPERATING EPS BEAT + FY26 FCF GUIDANCE RAISE</span>
          <span class="badge badge-blue">T+0 POST-PRINT</span>
        </div>
      </div>

      <!-- TRACK B: T-1 PRE-PRINT THESIS VS. T+0 POST-PRINT REALITY AUDIT BANNER -->
      <div class="t1-vs-t0-audit" style="background: linear-gradient(90deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(59, 130, 246, 0.35); border-left: 4px solid #34d399; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
          <span style="font-weight: 800; font-size: 13px; color: #34d399; text-transform: uppercase; letter-spacing: 0.05em;">🔍 T-1 Pre-Earnings Thesis vs. T+0 Post-Print Reality Audit</span>
          <a href="IBM_T1_2026-10-21.html" style="font-size: 11.5px; color: #93c5fd; text-decoration: underline;">Open Original T-1 Briefing →</a>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; font-size: 12.3px; color: var(--text-secondary);">
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #93c5fd;">Software &amp; AI Data Flywheel Thesis:</strong><br>
            • <em>T-1 Forecast:</em> Modeled Software at $7.75B (+8% YoY) with 83% GM.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">VALIDATED &amp; EXCEEDED</strong> — Software hit <strong>$7,804M</strong> (+9% CC) at <strong>83.2% GM</strong>, led by <strong>Data (+19% YoY)</strong> and <strong>Red Hat (+11% YoY)</strong>.
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #fcd34d;">Consulting &amp; Mainframe Cycle Caution:</strong><br>
            • <em>T-1 Forecast:</em> Flagged discretionary IT consulting lag &amp; mainframe digestion.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">SPOT-ON CALL</strong> — Consulting printed $5,335M (+0.2% reported / +2% CC) and IBM Z fell -20% YoY, though Distributed Infra surged <strong>+31% YoY</strong>.
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #34d399;">EPS &amp; Full-Year Free Cash Flow Thesis:</strong><br>
            • <em>T-1 Forecast:</em> Expected $2.87 Operating EPS and reiterated FCF guide.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">BEAT &amp; FCF RAISE</strong> — Delivered <strong>$2.95 Operating EPS</strong> (+11% YoY) and <strong>raised FY26 FCF growth to &gt;$1.0B YoY</strong> after Q3 OCF jumped +31% to $4,025M.
          </div>
        </div>
      </div>

      <!-- TABLE 1B-1: HEADLINE & COMPANY-SPECIFIC KPI BEAT / MISS SCORECARD -->
      <div style="margin-bottom: 20px;">
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-1: Headline &amp; Company-Specific KPI Beat / Miss Scorecard (Q3 2026 Actuals)</span>
          <span class="tip" title="Deterministic comparison of reported Q3 2026 actuals against Street pre-print consensus and T-1 whisper." data-tip="Beat / Miss Scorecard: Evaluates Q3 2026 delivery across headline GAAP/Non-GAAP metrics and IBM-specific segment KPIs with visual magnitude bars.">[Methodology]</span>
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
                <td><span class="tip" title="Operating (Non-GAAP) Diluted EPS ($2.95, +11% YoY) vs Street Consensus ($2.87); GAAP Diluted EPS: $2.31 (+26% YoY)." data-tip="Operating Non-GAAP EPS: Printed at $2.95 (+11% YoY), beating Street consensus of $2.87 by +$0.08 (+2.79%).">Operating (Non-GAAP) Diluted EPS</span></td>
                <td>$2.87</td>
                <td>$2.91</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$2.95 <span style="font-size:11px; color:var(--text-muted);">($2.31 GAAP)</span></td>
                <td>
                  <span class="badge badge-bull">+$0.08 (+2.79%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:82%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$0.04 (+1.37%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Total Revenue ($17,103M, +5% reported / +6% constant currency) vs Street Consensus ($17,550M)." data-tip="Total Revenue ($M): $17,103M (+4.73% YoY, +6% CC); FX headwinds (~130 bps) and Consulting softness created a -2.55% nominal variance vs unadjusted consensus.">Total Revenue ($M) (+6% CC)</span></td>
                <td>$17,550M</td>
                <td>$17,350M</td>
                <td class="col-q0" style="font-weight:700; color: #fcd34d;">$17,103M (+6% CC)</td>
                <td>
                  <span class="badge badge-warn">-$447M (-2.55% FX Drag)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:45%; height:100%; background:#f59e0b;"></div></div>
                </td>
                <td><span class="badge badge-warn">-$247M (-1.42%)</span></td>
                <td><span class="badge badge-warn">CC IN-LINE / FX DRAG</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Software Segment Revenue ($7,804M, +8.2% YoY / +9% CC) across Hybrid Cloud (Red Hat +11%), Data (+19%), and Automation (+7%)." data-tip="Software Segment Revenue ($M): Beat Street consensus by +$54M, reaching $7,804M with an 83.2% segment gross margin.">Software Segment Revenue ($M)</span></td>
                <td>$7,750M</td>
                <td>$7,780M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$7,804M (+9% CC)</td>
                <td>
                  <span class="badge badge-bull">+$54M (+0.70%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:76%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$24M (+0.31%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Data Software Sub-Segment Growth (+19% YoY, +20% CC) driven by enterprise AI data preparation." data-tip="Data Sub-Segment Growth: Surged +19% YoY (+20% CC), outpacing consensus by +500 bps.">Data &amp; AI Software Growth (% YoY)</span></td>
                <td>+14.0%</td>
                <td>+16.0%</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">+19.0% (+20% CC)</td>
                <td>
                  <span class="badge badge-bull">+500 bps</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:92%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+300 bps</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Hybrid Cloud (Red Hat) Revenue Growth (+11% YoY, +12% CC) on OpenShift and Ansible adoption." data-tip="Red Hat Growth: Accelerated to +11% YoY (+12% CC), beating consensus (+10.0%) by +100 bps.">Hybrid Cloud (Red Hat) Growth (% YoY)</span></td>
                <td>+10.0%</td>
                <td>+10.5%</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">+11.0% (+12% CC)</td>
                <td>
                  <span class="badge badge-bull">+100 bps</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:78%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+50 bps</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Infrastructure Segment Revenue ($3,707M, +4.2% YoY / +5% CC) driven by Distributed Infrastructure (+31% YoY)." data-tip="Infrastructure Segment Revenue ($M): Beat consensus by +$157M (+4.42%) as Distributed Infrastructure (+31% YoY) overwhelmed IBM Z cyclicality (-20% YoY).">Infrastructure Segment Revenue ($M)</span></td>
                <td>$3,550M</td>
                <td>$3,620M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$3,707M (+5% CC)</td>
                <td>
                  <span class="badge badge-bull">+$157M (+4.42%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:85%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$87M (+2.40%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Consulting Segment Revenue ($5,335M, +0.2% YoY / +2% CC)." data-tip="Consulting Segment Revenue ($M): Printed at $5,335M (+2% CC; Intelligent Operations +3% CC, Strategy &amp; Technology +1% CC).">Consulting Segment Revenue ($M)</span></td>
                <td>$5,450M</td>
                <td>$5,400M</td>
                <td class="col-q0" style="font-weight:700; color: #fcd34d;">$5,335M (+2% CC)</td>
                <td>
                  <span class="badge badge-warn">-$115M (-2.11%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:48%; height:100%; background:#f59e0b;"></div></div>
                </td>
                <td><span class="badge badge-warn">-$65M (-1.20%)</span></td>
                <td><span class="badge badge-warn">SLIGHT MISS</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Q3 2026 GAAP Operating Cash Flow ($4,025M) and Non-GAAP Free Cash Flow ($3,027M, +28% YoY)." data-tip="Q3 Free Cash Flow: Non-GAAP FCF surged +28% YoY to $3,027M ($3,539M GAAP OCF minus CapEx), crushing consensus of $2,650M by +$377M (+14.2%).">Q3 Non-GAAP Free Cash Flow ($M)</span></td>
                <td>$2,650M</td>
                <td>$2,750M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$3,027M <span style="font-size:11px; color:var(--text-muted);">($3,539M GAAP)</span></td>
                <td>
                  <span class="badge badge-bull">+$377M (+14.23%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:94%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$277M (+10.07%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-2: MANAGEMENT EXECUTION ACCOUNTABILITY -->
      <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
          <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; display: flex; align-items: center; gap: 8px;">
            <span>Table 1B-2: Management Execution Accountability (Q3 Actual vs. Prior Q2 Guidance Track Record)</span>
            <span class="tip" title="Tracks management execution credibility against forward guidance issued in the prior quarter." data-tip="Accountability Audit: Directly compares what management guided last quarter against actual reported Q3 2026 results.">[Credibility Audit]</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
            <span style="color: var(--text-muted);">Executive Guidance Credibility Score:</span>
            <div class="credibility-gauge-bar" style="width: 110px; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
              <div style="width: 90%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <strong style="color: #34d399;">90 / 100 (High)</strong>
          </div>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style="min-width: 220px;">Guided Metric / Horizon</th>
                <th>Prior Quarter (Q2 2026) Guidance</th>
                <th>Reported Delivery (Q3 2026 Actual)</th>
                <th>Variance Commentary</th>
                <th>Credibility Grade</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="tip" title="Constant Currency Revenue Growth Target (>5% CC)." data-tip="Constant Currency Revenue Growth: Guided >5% CC; delivered +6% CC (+5% reported) in Q3 2026.">Constant-Currency Revenue Growth</span></td>
                <td>&gt;5.0% Constant Currency Growth</td>
                <td style="font-weight:600; color: #34d399;">+6.0% Constant Currency (+4.73% Reported to $17,103M)</td>
                <td>Exceeded the 5% constant-currency target by +100 bps, led by Software (+9% CC) and Infrastructure (+5% CC).</td>
                <td><span class="badge badge-bull">BEAT OWN GUIDE</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Operating (Non-GAAP) Pre-Tax Margin Expansion." data-tip="Operating Pre-Tax Margin: Expanded +90 bps YoY to 19.6% ($3,355M) as SG&amp;A fell -4.5% YoY.">Operating Pre-Tax Margin Expansion</span></td>
                <td> ~50–75 bps YoY Operating Margin Expansion</td>
                <td style="font-weight:600; color: #34d399;">+90 bps YoY to 19.6% Non-GAAP Pre-Tax Margin</td>
                <td>83.2% Software gross margin and -4.5% YoY SG&amp;A reduction drove +10% YoY non-GAAP pre-tax profit growth.</td>
                <td><span class="badge badge-bull">BEAT OWN GUIDE</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Free Cash Flow Generation Trajectory." data-tip="Free Cash Flow: Q3 Non-GAAP FCF jumped +28% YoY to $3,027M ($3,539M GAAP), prompting a full-year FCF raise.">Free Cash Flow Generation</span></td>
                <td>Track toward ~$0.75B–$1.0B YoY FY26 FCF increase</td>
                <td style="font-weight:600; color: #34d399;">$3,027M Q3 Non-GAAP FCF (+28% YoY); FY26 Raised to &gt;+$1.0B YoY</td>
                <td>9-month YTD Non-GAAP FCF reached $8,509M (+$1,297M YoY), enabling management to raise the full-year FCF outlook.</td>
                <td><span class="badge badge-bull">BEAT &amp; RAISED</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-3: FORWARD GUIDANCE RESET -->
      <div>
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-3: Forward Guidance Reset (New Q4 2026 &amp; FY2026 Guidance vs. Pre-Print Street Expectations)</span>
          <span class="tip" title="Evaluates how new forward guidance changes future earnings power relative to Wall Street consensus." data-tip="Forward Guidance Reset: Audits raised FY2026 Free Cash Flow (>+$1.0B YoY), >5% CC revenue growth, FX impact, and Software/Distributed Infrastructure momentum.">[Re-Rating Matrix]</span>
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
                <td><span class="tip" title="Full-Year 2026 Free Cash Flow Outlook." data-tip="FY2026 Free Cash Flow Guidance: Raised to grow >$1.0B YoY (implying >$15.7B full-year FCF).">Full-Year 2026 Free Cash Flow</span></td>
                <td>+$0.8B YoY FCF Increase (~$15.5B)</td>
                <td style="font-weight:600; color: #34d399;">&gt;+$1.0 Billion YoY FCF Increase (&gt;$15.7B FY26E)</td>
                <td>+$200M+ above prior consensus FCF baseline</td>
                <td><span class="badge badge-bull">RAISED</span></td>
                <td>CFO James Kavanaugh cited strong Software mix, 19.6% operating pre-tax margin, and disciplined working capital (+$1.30B YTD FCF).</td>
              </tr>
              <tr>
                <td><span class="tip" title="Full-Year 2026 Constant Currency Revenue Growth." data-tip="FY2026 Constant Currency Revenue: Reiterated at >5% constant currency growth, with FX ~neutral for the full year.">Full-Year 2026 Constant-Currency Revenue</span></td>
                <td>~5.0% CC Growth</td>
                <td style="font-weight:600; color: #34d399;">&gt;5.0% Constant-Currency Revenue Growth (FX ~Neutral FY)</td>
                <td>Reiterated on +9% CC Software &amp; +31% Distributed Infra</td>
                <td><span class="badge badge-bull">REITERATED</span></td>
                <td>Software (+19% Data, +11% Red Hat) and AI-linked Distributed Infrastructure (+31%) offset slower Consulting and mainframe transition.</td>
              </tr>
              <tr>
                <td><span class="tip" title="Q4 2026 Seasonal Revenue &amp; Operating EPS Trajectory." data-tip="Q4 2026 Outlook: Seasonal Q4 software and infrastructure strength expected to lift Q4 revenue to ~$20.7B and Operating EPS to ~$4.15.">Q4 2026 Revenue &amp; Operating EPS</span></td>
                <td>~$20.6B Rev / $4.10 Adj EPS</td>
                <td style="font-weight:600; color: #34d399;">~$20.75B Q4E Revenue (+5.4% YoY) / ~$4.18 Operating EPS</td>
                <td>+$0.08 EPS upside from SG&amp;A productivity (-4.5% YoY)</td>
                <td><span class="badge badge-bull">POSITIVE MIX</span></td>
                <td>Seasonal Q4 enterprise software renewals (Red Hat OpenShift &amp; HashiCorp) carry 83%+ gross margins into year-end.</td>
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
          <div class="card-title"><span class="card-title-accent"></span>5-Quarter Rolling Financial Performance &amp; Forward Q4 2026E Bridge</div>
          <div class="card-subtitle">Audited SEC Form 10-Q / 8-K financial results in USD Millions (rolled forward to Q3 2026 Actuals + Post-Print Q4 2026E Estimates)</div>
        </div>
        <span class="badge badge-blue">DETERMINISTIC GROUND TRUTH (Q3 2025 – Q3 2026 ACTUAL + Q4 2026E)</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th style="min-width: 230px;">Financial Metric ($ Millions)</th>
              <th>Q3 2025<br><span style="font-size:10px;color:var(--text-muted);">(Sep 30, 2025)</span></th>
              <th>Q4 2025<br><span style="font-size:10px;color:var(--text-muted);">(Dec 31, 2025)</span></th>
              <th>Q1 2026<br><span style="font-size:10px;color:var(--text-muted);">(Mar 31, 2026)</span></th>
              <th>Q2 2026<br><span style="font-size:10px;color:var(--text-muted);">(Jun 30, 2026)</span></th>
              <th class="col-q0">Q3 2026 (Actual)<br><span style="font-size:10px;color:var(--accent-blue);">(Sep 30, 2026 8-K)</span></th>
              <th><span class="tip" title="Quarter-over-Quarter: Sequential change from Q2 2026 to Q3 2026 Actual." data-tip="Q3 QoQ Delta: Sequential percentage variance between Q2 2026 and Q3 2026 Actual.">Q3 QoQ</span></th>
              <th><span class="tip" title="Year-over-Year: Percentage change from Q3 2025 to Q3 2026 Actual." data-tip="Q3 YoY Delta: 12-month percentage variance between Q3 2025 and Q3 2026 Actual.">Q3 YoY</span></th>
              <th class="col-est">Q4 2026E<br><span style="font-size:10px;color:#34d399;">(New Guide / Est.)</span></th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background-color: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Total Revenue: Consolidated revenue across Software, Consulting, Infrastructure, and Financing ($17,103M in Q3 2026)." data-tip="Total Revenue ($M): Printed at $17,103M in Q3 2026 (-0.34% QoQ, +4.73% YoY / +6% CC); Q4 2026E modeled at $20,750M.">Total Revenue ($M)</span></td>
              <td>$16,331</td>
              <td>$19,687</td>
              <td>$15,917</td>
              <td>$17,162</td>
              <td class="col-q0" style="color: var(--accent-blue);">$17,103</td>
              <td><span class="badge badge-neutral">-0.34%</span></td>
              <td><span class="badge badge-bull">+4.73%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$20,750</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Software Segment Revenue: Hybrid Cloud/Red Hat, Automation, Data, and Transaction Processing ($7,804M in Q3 2026)." data-tip="Software Segment ($M): $7,804M in Q3 2026 (+1.61% QoQ, +8.25% YoY / +9% CC) with an 83.2% gross margin.">Software Segment ($M)</span></td>
              <td>$7,209</td>
              <td>$8,710</td>
              <td>$7,120</td>
              <td>$7,680</td>
              <td class="col-q0">$7,804</td>
              <td><span class="badge badge-bull">+1.61%</span></td>
              <td><span class="badge badge-bull">+8.25%</span></td>
              <td class="col-est">$9,500</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Consulting Segment Revenue: Strategy &amp; Technology and Intelligent Operations ($5,335M in Q3 2026)." data-tip="Consulting Segment ($M): $5,335M in Q3 2026 (-1.02% QoQ, +0.21% YoY / +2% CC) with a 28.9% gross margin.">Consulting Segment ($M)</span></td>
              <td>$5,324</td>
              <td>$5,350</td>
              <td>$5,180</td>
              <td>$5,390</td>
              <td class="col-q0">$5,335</td>
              <td><span class="badge badge-neutral">-1.02%</span></td>
              <td><span class="badge badge-bull">+0.21%</span></td>
              <td class="col-est">$5,480</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Infrastructure ($3,707M) plus Financing &amp; Other ($257M) = $3,964M in Q3 2026." data-tip="Infrastructure &amp; Financing ($M): Infrastructure generated $3,707M (+4.22% YoY, led by +31% Distributed Infrastructure) plus $257M Financing/Other.">Infrastructure &amp; Financing ($M)</span></td>
              <td>$3,798</td>
              <td>$5,627</td>
              <td>$3,617</td>
              <td>$4,092</td>
              <td class="col-q0">$3,964</td>
              <td><span class="badge badge-neutral">-3.13%</span></td>
              <td><span class="badge badge-bull">+4.37%</span></td>
              <td class="col-est">$5,770</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Cost of Revenue ($7,389M in Q3 2026)." data-tip="Cost of Revenue ($M): $7,389M in Q3 2026 (+1.85% QoQ, +6.00% YoY).">Cost of Revenue ($M)</span></td>
              <td>($6,971)</td>
              <td>($7,759)</td>
              <td>($6,967)</td>
              <td>($7,255)</td>
              <td class="col-q0">($7,389)</td>
              <td><span class="badge badge-neutral">+1.85%</span></td>
              <td><span class="badge badge-warn">+6.00%</span></td>
              <td class="col-est">($8,050)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Gross Profit: Total Revenue ($17,103M) minus Cost of Revenue ($7,389M) = $9,714M (56.80% GAAP GM; Non-GAAP GP: $10,004M / 58.5% GM)." data-tip="Gross Profit ($M): $9,714M GAAP (+3.78% YoY; 56.80% GAAP GM) and $10,004M Non-GAAP (58.5% GM).">Gross Profit ($M) (Non-GAAP: $10,004M)</span></td>
              <td>$9,360</td>
              <td>$11,928</td>
              <td>$8,950</td>
              <td>$9,907</td>
              <td class="col-q0" style="color: var(--bull-green);">$9,714</td>
              <td><span class="badge badge-neutral">-1.95%</span></td>
              <td><span class="badge badge-bull">+3.78%</span></td>
              <td class="col-est">$12,700</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Research, Development and Engineering Expenses ($2,378M in Q3 2026)." data-tip="RD&amp;E Expense ($M): $2,378M in Q3 2026 (+17.49% YoY) to advance watsonx AI, Red Hat, and Quantum computing.">Research, Development &amp; Engineering ($M)</span></td>
              <td>($2,024)</td>
              <td>($2,150)</td>
              <td>($2,210)</td>
              <td>($2,310)</td>
              <td class="col-q0">($2,378)</td>
              <td><span class="badge badge-warn">+2.94%</span></td>
              <td><span class="badge badge-warn">+17.49%</span></td>
              <td class="col-est">($2,420)</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Selling, General &amp; Administrative ($4,620M, down -4.49% YoY) net of IP &amp; Other income (-$164M) = $4,456M." data-tip="SG&amp;A &amp; Net Other OpEx ($M): SG&amp;A fell -4.49% YoY to $4,620M in Q3 2026 ($4,456M net of $164M IP/other operating credits).">SG&amp;A &amp; Net Other Operating ($M)</span></td>
              <td>($4,544)</td>
              <td>($4,929)</td>
              <td>($4,521)</td>
              <td>($4,752)</td>
              <td class="col-q0">($4,456)</td>
              <td><span class="badge badge-bull">-6.23%</span></td>
              <td><span class="badge badge-bull">-1.94%</span></td>
              <td class="col-est">($4,880)</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="Total Operating Expenses: Gross Profit ($9,714M) minus Operating Income ($2,880M) = $6,834M." data-tip="Total Operating Expenses ($M): Declined -3.23% sequentially to $6,834M in Q3 2026.">Total Operating Expenses ($M)</span></td>
              <td>($6,568)</td>
              <td>($7,079)</td>
              <td>($6,731)</td>
              <td>($7,062)</td>
              <td class="col-q0">($6,834)</td>
              <td><span class="badge badge-bull">-3.23%</span></td>
              <td><span class="badge badge-neutral">+4.05%</span></td>
              <td class="col-est">($7,300)</td>
            </tr>
            <tr style="font-weight: 700; background-color: rgba(34, 197, 94, 0.05);">
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit ($9,714M) minus Total OpEx ($6,834M) = $2,880M (Non-GAAP Pre-Tax Income: $3,355M / 19.6% margin)." data-tip="Operating Income (EBIT): $2,880M GAAP (+1.23% QoQ, +3.15% YoY); Operating Non-GAAP Pre-Tax Income rose +10% YoY to $3,355M.">Operating Income (EBIT) ($M)</span></td>
              <td>$2,792</td>
              <td>$4,849</td>
              <td>$2,219</td>
              <td>$2,845</td>
              <td class="col-q0" style="color: var(--bull-green);">$2,880</td>
              <td><span class="badge badge-bull">+1.23%</span></td>
              <td><span class="badge badge-bull">+3.15%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$5,400</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income ($2,199M in Q3 2026, +26.09% YoY; Non-GAAP Net Income: $2,812M, +12% YoY)." data-tip="GAAP Net Income ($M): Rose +26.09% YoY to $2,199M in Q3 2026 ($2,812M Operating Non-GAAP Net Income).">GAAP Net Income ($M) (Non-GAAP: $2,812M)</span></td>
              <td>$1,744</td>
              <td>$5,600</td>
              <td>$1,216</td>
              <td>$2,165</td>
              <td class="col-q0" style="color: var(--bull-green);">$2,199</td>
              <td><span class="badge badge-bull">+1.57%</span></td>
              <td><span class="badge badge-bull">+26.09%</span></td>
              <td class="col-est">$3,650</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Non-GAAP Diluted EPS ($2.95) and GAAP Diluted EPS ($2.31) in Q3 2026." data-tip="Diluted EPS: $2.95 Operating Non-GAAP (+11% YoY vs $2.65 in Q3 2025) and $2.31 GAAP (+26% YoY vs $1.84 in Q3 2025).">Diluted EPS (GAAP / Non-GAAP) ($)</span></td>
              <td>$1.84 <span style="font-size:10px;color:var(--text-muted);">($2.65 Adj)</span></td>
              <td>$5.88</td>
              <td>$1.28</td>
              <td>$2.27</td>
              <td class="col-q0" style="font-weight:700; color: var(--bull-green);">$2.31 <span style="font-size:11px;color:#34d399;">($2.95 Adj)</span></td>
              <td><span class="badge badge-bull">+1.76%</span></td>
              <td><span class="badge badge-bull">+25.54%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$4.18 Adj</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Cash Flow &amp; Capital Reinvestment Audit (Rolled to Q3 2026 Actual)</td>
            </tr>
            <tr>
              <td><span class="tip" title="Net cash provided by operating activities ($4,025M in Q3 2026)." data-tip="Operating Cash Flow (OCF): Jumped +54.99% QoQ and +30.60% YoY to $4,025M in Q3 2026.">Operating Cash Flow ($M)</span></td>
              <td>$3,082</td>
              <td>$4,040</td>
              <td>$5,169</td>
              <td>$2,597</td>
              <td class="col-q0" style="color: var(--bull-green);">$4,025</td>
              <td><span class="badge badge-bull">+54.99%</span></td>
              <td><span class="badge badge-bull">+30.60%</span></td>
              <td class="col-est">$6,800</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital expenditures ($486M in Q3 2026)." data-tip="Capital Expenditures ($M): $486M in Q3 2026 (2.84% of revenue).">Capital Expenditures ($M)</span></td>
              <td>($417)</td>
              <td>($553)</td>
              <td>($391)</td>
              <td>($383)</td>
              <td class="col-q0">($486)</td>
              <td><span class="badge badge-neutral">+26.89%</span></td>
              <td><span class="badge badge-neutral">+16.55%</span></td>
              <td class="col-est">($550)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Standard Reported Free Cash Flow: OCF ($4,025M) minus CapEx ($486M) = $3,539M (IBM Non-GAAP FCF ex-GF receivables: $3,027M)." data-tip="Reported Free Cash Flow ($M): $3,539M GAAP (+59.85% QoQ, +32.80% YoY) and $3,027M IBM Non-GAAP FCF (+28% YoY).">Reported Free Cash Flow ($M)</span></td>
              <td>$2,665</td>
              <td>$3,487</td>
              <td>$4,778</td>
              <td>$2,214</td>
              <td class="col-q0" style="color: var(--bull-green);">$3,539</td>
              <td><span class="badge badge-bull">+59.85%</span></td>
              <td><span class="badge badge-bull">+32.80%</span></td>
              <td class="col-est">$6,250</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Stock-based compensation expense ($535M in Q3 2026)." data-tip="Stock-Based Compensation ($M): $535M in Q3 2026 (3.13% of revenue).">Stock-Based Compensation ($M)</span></td>
              <td>($443)</td>
              <td>($430)</td>
              <td>($506)</td>
              <td>($498)</td>
              <td class="col-q0">($535)</td>
              <td><span class="badge badge-neutral">+7.43%</span></td>
              <td><span class="badge badge-warn">+20.77%</span></td>
              <td class="col-est">($540)</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Principal lease &amp; short-term financing repayments ($120M in Q3 2026)." data-tip="Finance Lease &amp; Principal Payments ($M): Normalized to $120M in Q3 2026.">Principal Finance Lease Payments ($M)</span></td>
              <td>($1,114)</td>
              <td>($1,810)</td>
              <td>($2,928)</td>
              <td>($4,213)</td>
              <td class="col-q0">($120)</td>
              <td><span class="badge badge-bull">-97.15%</span></td>
              <td><span class="badge badge-bull">-89.23%</span></td>
              <td class="col-est">($125)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Forensic True Free Cash Flow: Reported FCF ($3,539M) minus SBC ($535M) minus Finance Leases ($120M) = $2,884M." data-tip="True Free Cash Flow ($M): Surged to $2,884M in Q3 2026 (+160.29% YoY).">True Free Cash Flow (ex-SBC &amp; Leases) ($M)</span></td>
              <td>$1,108</td>
              <td>$1,247</td>
              <td>$1,344</td>
              <td>($2,497)</td>
              <td class="col-q0" style="color: var(--bull-green);">$2,884</td>
              <td><span class="badge badge-bull">+$5,381M</span></td>
              <td><span class="badge badge-bull">+160.29%</span></td>
              <td class="col-est">$5,585</td>
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
          <div class="card-title"><span class="card-title-accent"></span>Outlier &amp; Accounting Quality Audit (Q3 2026 Post-Print Forensic Review)</div>
          <div class="card-subtitle">Forensic deconstruction of the 83.2% Software Gross Margin, -4.5% YoY SG&amp;A Reduction, and +$2,884M True Free Cash Flow</div>
        </div>
        <span class="badge badge-bull">SOFTWARE MARGIN &amp; FCF COMPOUNDER</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>1. Software Mix Inflection: 45.6% of Revenue at 83.2% Segment Gross Margin</span>
              <span class="badge badge-bull">DATA +19% | RED HAT +11%</span>
            </div>
            <p>
              Software revenue grew <strong>+8.25% YoY (+9% constant currency) to $7,804M</strong>, reaching 45.63% of consolidated IBM revenue at an extraordinary <strong>83.2% gross margin</strong>. Growth was led by the <strong>Data sub-segment (+19% YoY, +20% CC)</strong> as enterprises deployed watsonx data pipelines, alongside <strong>Hybrid Cloud / Red Hat (+11% YoY, +12% CC)</strong> and <strong>Automation (+7% YoY, +8% CC)</strong>.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>2. Internal AI Productivity: SG&amp;A Down -4.49% YoY While R&amp;D Rose +17.49% YoY</span>
              <span class="badge badge-bull">+90 BPS PRE-TAX MARGIN</span>
            </div>
            <p>
              IBM's internal "Client Zero" AI automation reduced Selling, General &amp; Administrative (SG&amp;A) expense by <strong>-4.49% YoY to $4,620M</strong> (from $4,837M in Q3 2025), allowing IBM to self-fund a <strong>+17.49% YoY increase in R&amp;D ($2,378M)</strong> while still expanding Operating Non-GAAP Pre-Tax Margin by <strong>+90 bps YoY to 19.6% ($3,355M)</strong>.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>3. Distributed Infrastructure Surge (+31% YoY) Offsets IBM Z Mainframe Cycle (-20% YoY)</span>
              <span class="badge badge-blue">INFRASTRUCTURE +5% CC</span>
            </div>
            <p>
              Within the $3,707M Infrastructure segment (+4.2% YoY, +5% CC), late-cycle <strong>IBM Z mainframe revenue declined -20% YoY (-19% CC)</strong>, but <strong>Distributed Infrastructure surged +31% YoY (+32% CC)</strong> on enterprise hybrid-cloud storage and AI server attach—beating Street Infrastructure estimates by +$157M.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Cash Flow Quality &amp; Raised FY26 FCF Guidance (&gt;+$1.0B YoY Increase)</span>
              <span class="badge badge-bull">$2,884M TRUE FCF</span>
            </div>
            <p>
              Q3 GAAP Operating Cash Flow jumped <strong>+30.60% YoY to $4,025M</strong> against just <strong>$486M in CapEx</strong>, yielding <strong>$3,539M in standard Reported FCF</strong> ($3,027M on IBM's Non-GAAP FCF definition, up +28% YoY) and <strong>$2,884M in Forensic True FCF</strong> after deducting $535M SBC and $120M lease principal.
            </p>
          </div>
        </div>

        <!-- FCF WATERFALL BRIDGE -->
        <div class="fcf-bridge-box">
          <div class="fcf-bridge-header">
            <span>Deterministic Cash Flow Bridge (Q3 2026 Reported Actuals)</span>
            <span style="color: var(--text-muted); font-size: 11px;">$M USD • Q3 2026 8-K Actual</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Reported Operating Cash Flow (OCF)</span>
            <span class="waterfall-val" style="color: #34d399;">+${q0_ocf:,.0f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Capital Expenditures (PP&amp;E &amp; Cloud Infra)</span>
            <span class="waterfall-val" style="color: #f87171;">-${q0_capex:,.0f}M</span>
          </div>
          <div class="waterfall-row" style="border-top: 1px dashed rgba(255, 255, 255, 0.15); padding-top: 6px;">
            <span class="waterfall-label" style="font-weight: 700; color: #f8fafc;">(=) Standard Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="font-weight: 700; color: #34d399;">+${q0_rep_fcf:,.0f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Stock-Based Compensation (SBC)</span>
            <span class="waterfall-val" style="color: #f87171;">-${q0_sbc:,.0f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Principal Finance Lease Repayments</span>
            <span class="waterfall-val" style="color: #f87171;">-${q0_leases:,.0f}M</span>
          </div>
          <div class="waterfall-row" style="border-top: 2px solid var(--border-color); padding-top: 8px; margin-top: 4px;">
            <span class="waterfall-label" style="font-weight: 800; color: #60a5fa;">(=) Forensic True Free Cash Flow</span>
            <span class="waterfall-val" style="color: #34d399; font-weight:800;">+${q0_true_fcf:,.0f}M</span>
          </div>
          <div style="margin-top: 14px; font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
            *Note: IBM's Non-GAAP FCF definition excludes $548M of Global Financing receivables cash inflow, printing at <strong>$3,027M (+28% YoY)</strong> in Q3 and <strong>$8,509M YTD (+$1,297M YoY)</strong>, backing the raised FY26 FCF guide (&gt;+$1.0B YoY).
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
          <div class="card-title"><span class="card-title-accent"></span>Operational Execution Audit: Q3 2026 Tailwinds vs. Structural Headwinds</div>
          <div class="card-subtitle">Post-print institutional assessment of Software (+9% CC), Distributed Infrastructure (+31%), Raised FY26 FCF, and Consulting/Mainframe Lags</div>
        </div>
        <span class="badge badge-bull">SOFTWARE &amp; FCF QUALITY WIN</span>
      </div>

      <div class="audit-grid">
        <!-- 4 OPERATIONAL WINS / TAILWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bull-green);">
            <span>🚀 4 Key Operational Tailwinds (Verified in Q3 Print)</span>
            <span class="badge badge-bull">GROWTH ENGINES</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. Data (+19% YoY) &amp; Red Hat (+11% YoY) Powering 83.2% Software GM</span>
                <span class="badge badge-bull">$7,804M SOFTWARE REV</span>
              </div>
              <p>
                Software expanded <strong>+8.2% YoY (+9% CC) to $7,804M</strong> at an <strong>83.2% gross margin</strong>, driven by surging enterprise demand for Data (+19% YoY, +20% CC), Red Hat OpenShift/Ansible (+11% YoY, +12% CC), and Automation (+7% YoY, +8% CC).
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Distributed Infrastructure Breakout (+31% YoY / +32% CC)</span>
                <span class="badge badge-bull">$3,707M INFRASTRUCTURE</span>
              </div>
              <p>
                Distributed Infrastructure surged <strong>+31% YoY (+32% CC)</strong> as enterprise clients upgraded hybrid-cloud storage and AI server infrastructure, driving total Infrastructure revenue up <strong>+4.2% YoY (+5% CC) to $3,707M</strong> despite the IBM Z cycle.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Full-Year 2026 Free Cash Flow Guidance Raised (&gt;+$1.0B YoY)</span>
                <span class="badge badge-blue">+$1.30B YTD FCF GAIN</span>
              </div>
              <p>
                Following a <strong>+28% YoY jump in Q3 Non-GAAP FCF to $3,027M</strong> ($3,539M GAAP FCF), management raised full-year 2026 FCF growth guidance to <strong>more than $1.0 billion YoY</strong> (implying &gt;$15.7B FY26 FCF).
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Structural SG&amp;A Leverage (-4.5% YoY) &amp; +$0.08 Operating EPS Beat</span>
                <span class="badge badge-bull">$2.95 OPERATING EPS</span>
              </div>
              <p>
                Internal AI productivity lowered SG&amp;A by <strong>-4.49% YoY to $4,620M</strong>, expanding Operating Pre-Tax Margin by +90 bps YoY to <strong>19.6%</strong> and driving a clean <strong>$2.95 Operating EPS beat (+11% YoY)</strong>.
              </p>
            </div>
          </div>
        </div>

        <!-- 4 OPERATIONAL DRAGS / HEADWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bear-red);">
            <span>⚠️ 4 Key Operational Drags &amp; Risk Factors (Verified in Q3 Print)</span>
            <span class="badge badge-bear">EXECUTION RISKS</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. Sluggish Consulting Top-Line (+0.2% Reported / +2% CC to $5,335M)</span>
                <span class="badge badge-bear">DISCRETIONARY IT LAG</span>
              </div>
              <p>
                Enterprise pause on discretionary legacy IT consulting kept Q3 Consulting revenue nearly flat at <strong>$5,335M (+0.2% reported, +2% CC)</strong>, missing Street expectations of $5,450M as clients reprioritize budgets toward AI software.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Late-Cycle IBM Z Mainframe Contraction (-20% YoY / -19% CC)</span>
                <span class="badge badge-bear">MAINFRAME CYCLE</span>
              </div>
              <p>
                IBM Z revenue declined <strong>-20% YoY (-19% CC)</strong> in Q3 2026 as the z16/z17 product cycle entered late-stage digestion, compressing Infrastructure gross margin by -410 bps YoY to 52.5%.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Foreign Exchange Headwind (~130 bps Drag on Reported Revenue)</span>
                <span class="badge badge-warn">FX HEADWIND</span>
              </div>
              <p>
                Currency translation clipped Q3 revenue growth from +6% in constant currency to +4.73% reported ($17,103M), explaining the bulk of the nominal variance against unadjusted Street consensus ($17,550M).
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Elevated Acquisition Debt Load ($66.44B Total Debt; $55.21B Core)</span>
                <span class="badge badge-warn">$513M Q3 INTEREST EXP</span>
              </div>
              <p>
                Total debt rose by +$5.09B vs year-end 2025 to <strong>$66,440M</strong> ($55,213M Core Debt + $11,227M Global Financing Debt), generating $513M in Q3 interest expense ($1,526M YTD).
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
          <div class="card-subtitle">Source: Q3 2026 Earnings Call Transcript • Top 3 Hardest Sell-Side Analyst Questions &amp; Executive Responses</div>
        </div>
        <span class="badge badge-blue">Analyst Q&amp;A Highlights</span>
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 12px;">
        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #60a5fa; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #93c5fd; font-size: 13.5px; margin-bottom: 4px;">
            1. Drivers of the FY26 Free Cash Flow Guidance Raise (&gt;+$1.0B YoY) — Toni Sacconaghi (Bernstein)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> Arvind and Jim, you raised full-year 2026 Free Cash Flow growth guidance to more than $1 billion YoY after generating $3.03B Non-GAAP FCF in Q3 (+28% YoY). How much of this outperformance is structural software margin mix versus working capital timing?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> CFO James Kavanaugh emphasized that 9-month YTD Non-GAAP FCF is already up +$1,297M YoY to $8,509M, driven by high-margin Software (+9% CC, 83.2% gross margin) and +90 bps of operating pre-tax margin expansion (19.6%) as internal AI productivity lowered SG&amp;A by -4.5% YoY.
          </p>
        </div>
        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #34d399; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #34d399; font-size: 13.5px; margin-bottom: 4px;">
            2. Software Acceleration: Data (+19% YoY) &amp; Red Hat (+11% YoY) — Wamsi Mohan (Bank of America)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> Software grew 9% in constant currency to $7.80B, with Data surging 19% YoY (20% CC) and Red Hat up 11% YoY (12% CC). How is enterprise generative AI adoption flowing through your Data and Red Hat OpenShift bookings?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> CEO Arvind Krishna noted that enterprise AI deployments require clean, governed hybrid-cloud data pipelines, directly fueling the 20% constant-currency surge in IBM's Data software portfolio alongside Red Hat OpenShift AI and HashiCorp infrastructure automation.
          </p>
        </div>
        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #f59e0b; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #fcd34d; font-size: 13.5px; margin-bottom: 4px;">
            3. Consulting (+2% CC) &amp; Distributed Infrastructure (+31% YoY) Divergence — Erik Woodring (Morgan Stanley)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> While Consulting grew 2% in constant currency ($5.34B), Infrastructure beat expectations at $3.71B (+5% CC) as Distributed Infrastructure jumped 31% YoY despite IBM Z declining 20%. What is driving the Distributed Infrastructure surge?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> Management explained that enterprise clients are refreshing distributed storage and hybrid-cloud compute nodes to support on-premise AI inference workloads (+32% CC in Distributed Infrastructure), more than offsetting late-cycle IBM Z mainframe comps (-19% CC).
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
          <div class="card-title"><span class="card-title-accent"></span>Enterprise Hybrid Cloud, Software &amp; IT Services Peers</div>
          <span class="badge badge-blue">POST-PRINT COMP MATRIX (Q3 2026)</span>
        </div>

        <div class="table-wrapper" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th style="min-width:140px;">Ticker / Peer</th>
                <th><span class="tip" title="Constant-Currency YoY Revenue Growth in Q3 2026." data-tip="YoY Revenue Growth: +6.0% CC (+4.73% reported) for IBM.">YoY Rev Growth</span></th>
                <th><span class="tip" title="Non-GAAP Gross Margin percentage in Q3 2026." data-tip="Gross Margin: 58.5% Non-GAAP (56.8% GAAP; 83.2% Software) for IBM.">Gross Margin</span></th>
                <th><span class="tip" title="Operating Pre-Tax / EBIT Margin in Q3 2026." data-tip="Operating Margin: 19.6% Non-GAAP Pre-Tax (16.84% GAAP EBIT) for IBM.">Op Margin (Adj)</span></th>
                <th><span class="tip" title="GAAP Operating Cash Flow Margin in Q3 2026." data-tip="OCF Margin: $4,025M OCF / $17,103M Revenue = 23.53%.">OCF Margin</span></th>
                <th><span class="tip tip-right" title="Forward P/E ratio at $239.80 After-Hours price." data-tip="Forward P/E: 18.2x at $239.80 AH price.">Fwd P/E</span></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color:var(--accent-blue);">IBM (Q3 Actual)</strong></td>
                <td><span class="badge badge-bull">+6.0% CC (+4.7% Rep)</span></td>
                <td><strong style="color:var(--bull-green);">58.50%</strong> <span style="font-size:10px;color:var(--text-muted);">(56.8% GAAP)</span></td>
                <td><strong style="color:var(--bull-green);">19.60%</strong></td>
                <td><strong style="color:var(--bull-green);">+23.53%</strong></td>
                <td style="color:var(--bull-green);">18.2x</td>
              </tr>
              <tr>
                <td><strong>ACN (Accenture plc)</strong></td>
                <td><span class="badge badge-neutral">+4.5% CC</span></td>
                <td>32.60%</td>
                <td>15.50%</td>
                <td>+14.80%</td>
                <td>24.6x</td>
              </tr>
              <tr>
                <td><strong>ORCL (Oracle Corp.)</strong></td>
                <td><span class="badge badge-bull">+9.0% CC</span></td>
                <td>71.40%</td>
                <td>43.00%</td>
                <td>+34.20%</td>
                <td>26.4x</td>
              </tr>
              <tr>
                <td><strong>MSFT (Microsoft Corp.)</strong></td>
                <td><span class="badge badge-bull">+14.0% CC</span></td>
                <td>69.20%</td>
                <td>44.50%</td>
                <td>+42.10%</td>
                <td>31.2x</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">Software Margin Mix &amp; Free Cash Flow Yield Advantage</span>
              <span class="badge badge-bull">~6.9% FCF YIELD</span>
            </div>
            <p>
              • <strong>IBM vs. Accenture:</strong> Unlike pure-play IT consultancies (~32.6% GM), IBM's 83.2% gross margin Software engine (45.6% of revenue) drives a 58.5% Non-GAAP gross margin and 23.5% OCF margin.<br>
              • <strong>Valuation Floor:</strong> At $239.80 AH, IBM trades at just <strong>~14.5x raised FY26 Free Cash Flow (&gt;$15.7B)</strong> with a ~2.8% dividend yield.
            </p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Post-Print Product Roadmap &amp; Multi-Quarter Catalysts</div>
          <span class="badge badge-bull">Q4 2026 &amp; FY2027 CATALYSTS</span>
        </div>

        <div class="catalyst-grid">
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">1. watsonx Data &amp; AI Governance Acceleration (+19% YoY)</span>
              <span class="badge badge-bull">+20% CC IN Q3</span>
            </div>
            <p>
              Data was IBM's fastest-growing software pillar in Q3 (+19% YoY, +20% CC) as Fortune 500 enterprises standardize hybrid-cloud AI data governance on watsonx.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Red Hat OpenShift AI &amp; HashiCorp Cross-Sell (+11% YoY)</span>
              <span class="badge badge-blue">HYBRID CLOUD STANDARD</span>
            </div>
            <p>
              Red Hat grew +11% YoY (+12% CC) while Automation rose +7% YoY (+8% CC), capturing multi-cloud container and infrastructure-as-code budgets.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Distributed Infrastructure AI Refresh Cycle (+31% YoY)</span>
              <span class="badge badge-bull">+32% CC SURGE</span>
            </div>
            <p>
              On-premise enterprise AI storage and Power server demand propelled Distributed Infrastructure up +31% YoY in Q3, bridging the gap until the next mainframe cycle.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Seasonal Q4 FCF Harvest (&gt;$15.7B Full-Year FCF Target)</span>
              <span class="badge badge-bull">FY26 GUIDE RAISED</span>
            </div>
            <p>
              Q4 is IBM's largest seasonal software renewal and cash collection quarter, backing management's raised outlook for &gt;$1.0B YoY FCF expansion.
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
        <span class="badge badge-bull">POST-PRINT COMPOSITE SCORE: 68 / 100 (VALUE ACCUMULATION)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Post-Print Consensus: Institutional Value Desks Buy the -4.64% AH Knee-Jerk on Raised FY26 FCF &amp; +9% CC Software
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            IBM pulled back <strong>-4.64% (-$11.66/sh to $239.80)</strong> after hours (exceeding the ±3.58% / ±$8.72 straddle band) on nominal revenue ($17,103M vs $17,550M Street) and IBM Z (-20%), but institutional desks highlighted the <strong>$2.95 Operating EPS beat, +19% Data growth, +11% Red Hat growth, and the raised FY26 Free Cash Flow outlook (&gt;+$1.0B YoY)</strong>.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-warn">AH Reaction: -4.64% ($239.80)</span>
          <span class="badge badge-bull">FY26 FCF: Raised (&gt;+$1B)</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #1: Retail &amp; Dividend Pulse <span class="badge badge-bull">REDDIT / X / FINTWIT</span></span>
            <span class="badge badge-neutral">SCORE: 62 / 100 (MIXED / DIP-BUYING)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 62%; background: var(--accent-blue);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Top Retail Catalyst</span>
              <span class="kpi-val" style="color:var(--bull-green);">FY26 FCF Raise + Div</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Software Standout</span>
              <span class="kpi-val">Data +19% | Red Hat +11%</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">AH Dip Reaction</span>
              <span class="kpi-val">Adding at ~$240</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            "FinTwit Enterprise Software PM: 'IBM beats Operating EPS ($2.95 vs $2.87), grows Software +9% CC at 83.2% GM (Data +20% CC, Red Hat +12% CC), and RAISES full-year FCF growth to >$1B YoY. Buying the $240 AH dip.'"
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #2: Sell-Side Flash Note Reactions <span class="badge badge-bull">WALL STREET DESKS</span></span>
            <span class="badge badge-bull">SCORE: 74 / 100 (CONSTRUCTIVE)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 74%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Operating EPS Beat</span>
              <span class="kpi-val" style="color:var(--bull-green);">$2.95 vs $2.87 Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Q3 Non-GAAP FCF</span>
              <span class="kpi-val">$3,027M (+28% YoY)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Distributed Infra</span>
              <span class="kpi-val">+31% YoY (+32% CC)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Sell-Side Enterprise Desk: "Raising FY26 FCF growth to >$1B YoY after Q3 FCF surged +28% YoY to $3.03B underscores the durability of IBM's 83.2% gross margin Software portfolio."
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #3: Management Call Tone &amp; Candor <span class="badge badge-bull">TRANSCRIPT AUDIT</span></span>
            <span class="badge badge-bull">SCORE: 82 / 100 (CONFIDENT)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 82%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Pre-Tax Margin Lift</span>
              <span class="kpi-val">+90 bps YoY (19.6%)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">SG&amp;A Productivity</span>
              <span class="kpi-val">-4.5% YoY ($4,620M)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">FY26 CC Revenue</span>
              <span class="kpi-val">Reiterated &gt;5% CC</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            CFO James Kavanaugh: "Our strong cash generation allows us to invest for the future while returning value to shareholders, and we are raising our expectation for full-year free cash flow to grow by more than $1 billion year-over-year."
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #4: Post-Print Options &amp; Support <span class="badge badge-blue">DERIVATIVES DESK</span></span>
            <span class="badge badge-neutral">SCORE: 55 / 100 (PUT SUPPORT)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 55%; background: var(--accent-blue);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Actual vs Implied Move</span>
              <span class="kpi-val">-4.64% vs ±3.58% Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Institutional Put Floor</span>
              <span class="kpi-val">$235.00 – $240.00</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">FCF Yield at $239.80</span>
              <span class="kpi-val" style="color:var(--bull-green);">~6.9% FY26E Yield</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            At $239.80 AH (down from $251.46 close), IBM approaches institutional dividend/FCF yield support (~6.9% FCF yield), attracting put-write and mean-reversion call-spread buyers at the T+1 open.
          </div>
        </div>
      </div>

      <!-- AGENT 2C SOCIAL PULSE SUMMARY CARDS -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; margin-top: 16px;">
        <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #34d399; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #34d399; font-size: 13px; margin-bottom: 4px;">Retail &amp; Income Investor Reaction (Reddit &amp; X)</div>
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
          <div class="card-subtitle">Post-call risk-reward setups anchored to the After-Hours Price (${ah_price:.2f}) and Raised FY26 Free Cash Flow Guidance</div>
        </div>
        <span class="badge badge-bull">POST-PRINT TACTICAL PLAYBOOK</span>
      </div>

      <div class="scenario-grid">
        <!-- BULL CASE -->
        <div class="scenario-card scenario-bull">
          <div class="scenario-title">
            <span style="color:var(--bull-green);">ACCUMULATE ON FCF RAISE &amp; SOFTWARE MIX (BULL CASE)</span>
            <span class="badge badge-bull">PROB: 50% | TARGET: $258.00–$270.00 (Anchored above ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Raised FY26 FCF Floor (&gt;+$1.0B YoY):</strong> Institutional value buyers step in at $238–$240 (~14.5x FY26E FCF, ~6.9% FCF yield) following the <strong>+$1.30B YTD Non-GAAP FCF increase</strong> and <strong>$4,025M Q3 GAAP OCF</strong>.</li>
            <li><strong>Software Re-Rating (+9% CC, 83.2% GM):</strong> Accelerating growth in <strong>Data (+19% YoY)</strong> and <strong>Red Hat (+11% YoY)</strong> drives multiple expansion into the seasonally strongest Q4 software renewal quarter.</li>
            <li><strong>AI Productivity Leverage:</strong> Continued SG&amp;A reductions (-4.5% YoY) expand Operating Pre-Tax Margin (+90 bps YoY to 19.6%), supporting $2.95+ quarterly EPS power.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure (Bull Target: $258.00):</strong>
            Buy the T+1 open dip near $240 or initiate a <strong>Dec 18, 2026 $240 / $260 Bull Call Spread</strong> (financed by selling a $225 Put) to capture a mean-reversion fill of the $251.46 gap.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">CONSOLIDATE &amp; COLLECT DIVIDEND/THETA (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 35% | RANGE: $234.00–$248.00 (Around ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Consulting vs. Software Tug-of-War:</strong> Market balances +9% CC Software and +31% Distributed Infrastructure against sluggish <strong>Consulting (+0.2% reported / +2% CC to $5,335M)</strong>.</li>
            <li><strong>Mainframe Cycle Wait-and-See:</strong> Investors await early 2027 visibility on the next IBM Z refresh after Q3 IBM Z revenue declined -20% YoY.</li>
            <li><strong>Dividend &amp; FCF Support:</strong> 2.8% dividend yield ($1,583M Q3 payout, 2.24x FCF covered) anchors shares above $234.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure:</strong>
            Deploy a <strong>Nov 20, 2026 Cash-Secured Put Write at $235</strong> or a <strong>Covered Call overwrite at $250</strong> to harvest post-print theta and dividend yield.
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">CONSULTING &amp; DEBT DE-RATING (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 15% | TARGET: $225.00–$218.00 (Anchored below ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Prolonged Enterprise IT Consulting Freeze:</strong> Consulting growth stalls near 0% reported if enterprise discretionary IT services budgets remain constrained in Q4.</li>
            <li><strong>Acquisition Leverage Focus:</strong> Bears focus on <strong>$66,440M total debt ($55,213M Core Debt)</strong> and $2.04B annualized interest expense limiting M&amp;A flexibility.</li>
            <li><strong>Technical Breakdown Below $235:</strong> Failure to hold the $235 support level triggers systematic trend-follower selling toward the 200-day moving average ($225).</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure (Bear Target: $225.00):</strong>
            Initiate a <strong>Nov 20, 2026 $237.50 / $225.00 Bear Put Spread</strong> if IBM breaks below $236 on heavy T+1 institutional volume.
          </div>
        </div>
      </div>
    </section>

    <!-- VERBATIM GROUND-TRUTH GROUNDING LEDGER -->
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 10px 14px; font-size: 12px; color: var(--text-muted); margin-top: 10px; margin-bottom: 14px;">
      <strong>Deterministic Grounding Verification:</strong> Regular Close Price: <span class="mono" style="color:#f8fafc;">${reg_price:.2f}</span> • After-Hours Price: <span class="mono" style="color:#f87171;">${ah_price:.2f}</span> • Reported Q3 2026 Revenue: <span class="mono" style="color:#60a5fa;">${q0_rev:,.0f}M</span> • Reported Q3 2026 Operating Cash Flow (OCF): <span class="mono" style="color:#34d399;">${q0_ocf:,.0f}M</span> • Standard Reported FCF: <span class="mono" style="color:#34d399;">${q0_rep_fcf:,.0f}M</span> • Forensic True Free Cash Flow: <span class="mono" style="color:#34d399;">${q0_true_fcf:,.0f}M</span> • Post-Print Move: <span class="mono" style="color:#fcd34d;">{post_move_pct:+.2f}%</span> vs Expected <span class="mono">±{opt_implied_pct:.2f}%</span>.
    </div>

    <!-- 10. FOOTER -->
    <div class="footer-meta">
      <div>
        <span>SEC EDGAR CIK: <strong>0000051143</strong></span> • 
        <span>Q3 2026 Form 8-K Filed: <strong>Wednesday, Oct 21, 2026 (Item 2.02 &amp; Ex. 99.1)</strong></span> • 
        <span>Reporting Currency: <strong>USD ($ Millions)</strong></span>
      </div>
      <div style="margin-top:6px;">
        Deterministic Post-Earnings Ground Truth Anchored via SEC Form 8-K &amp; 10-Q Filings • Generated with Antigravity Zero-Hallucination T+0 Post-Earnings Harness
      </div>
    </div>
"""

draft_payload = {
    "header": {
        "page_title": f"IBM (${ah_price:.2f}) Q3 2026 Post-Earnings Forensic & Sentiment Tearsheet",
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
        "bull_target_low_num": 258.0,
        "bear_target_high_num": 225.0
    },
    "rendered_container_html": container_html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"[SUCCESS] Generated Post-Earnings Draft for IBM at: {DRAFT_PATH.name}")
print(f"  - Inner HTML Character Count: {len(container_html):,}")
print(f"  - Interactive Tooltip Count (.tip): {container_html.count('class=\"tip')}")
print(f"  - Data-Tip Count (data-tip=): {container_html.count('data-tip=\"')}")
