"""
NOK Dedicated Post-Earnings Draft Builder (Track A + Track B Complete Re-Synthesis)
Builds drafts/NOK_2026-10-22_post_draft.json with 100% Q3 2026 (Actual) rolled 5-quarter tables,
Q4 2026E forward guidance columns, zero T-1 bleed-through, and Track B interactive enhancements.
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "NOK_2026-10-22_post_truth.json"
BUS_2A_PATH = BASE_DIR / "post_agent_bus" / "NOK_2026-10-22_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "post_agent_bus" / "NOK_2026-10-22_agent2b_transcript.json"
BUS_2C_PATH = BASE_DIR / "post_agent_bus" / "NOK_2026-10-22_agent2c_social.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "NOK_2026-10-22_post_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
kpis_data = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
trans_data = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
soc_data = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

reg_price = truth["post_print_reaction"]["regular_close_price"]      # 7.88
ah_price = truth["post_print_reaction"]["after_hours_price"]         # 7.91
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]  # 0.38
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] # 4.15
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 0.35)
verdict = truth["post_print_reaction"]["overall_print_verdict"]      # BEAT & RAISE (CAPEX SURGE)

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]  # 5154.0
cons_rev = truth["t1_baseline"]["consensus_revenue_millions"]                 # 4980.0
q0_gaap_eps = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"]     # 0.03
q0_adj_eps = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"]   # 0.09
cons_eps = truth["t1_baseline"]["consensus_eps_nongaap"]                      # 0.07

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # 95.0
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 194.0
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # -99.0
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 104.0
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 50.0
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # -253.0

s5q = truth["stitched_5q_chronological"]

bull_target = 8.80
bear_target = 6.80

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
            <span class="ticker-symbol">NOK</span>
            <h1 class="company-name">Nokia Corporation (Nokia Oyj)</h1>
            <span class="badge badge-bull">{verdict}</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="Immediate post-earnings release forensic analysis." data-tip="T+0 Post-Print: Forensic analysis synthesized immediately following the official Q3 2026 SEC Form 6-K stock exchange release and earnings conference call.">T+0</span> POST-EARNINGS FORENSIC TEARSHEET</span>
          </div>
          <div class="sector-tag">NYSE ADR (NOK) • Nasdaq Helsinki (NOKIA) • Optical Networks, AI &amp; Cloud Data Center Interconnect, Mobile Radio &amp; Technology Standards • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): 0000924621 assigned by the U.S. Securities and Exchange Commission (SEC) to Nokia.">CIK</span>: 0000924621</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Regular Close / <span style="color:#34d399;">After-Hours Price</span></div>
            <div class="price-value">${reg_price:.2f} / <span style="color:#34d399;">${ah_price:.2f}</span> <span style="font-size:14px; color:#34d399;">({post_move_pct:+.2f}%)</span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total equity value at $7.91 after-hours price across 5.58B diluted shares." data-tip="Market Capitalization: Post-print equity value (~$44.1B at $7.91 AH / $44.1B regular close) vs $50.1B Enterprise Value.">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt ($2.44B) minus Liquid Cash &amp; Investments ($4.67B)." data-tip="Enterprise Value (EV): Reflects ultra-strong liquidity with €2,584M net cash and interest-bearing financial investments on balance sheet.">EV</span></div>
            <div class="price-value">$44.1B / $50.1B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Q3 2026 SEC Form 6-K Filed</span>
          <span class="strip-val" style="color: var(--bull-green);">Thu, Oct 22, 2026 • <span class="tip" title="Before Market Open: Official Q3 2026 interim report released at 8:00 AM EEST." data-tip="Form 6-K stock exchange release filed October 22, 2026 before market open; Webcast hosted at 8:00 AM ET / 3:00 PM EET.">6-K Verified</span></span>
          <span class="kpi-sub">Interim Report Attachment &amp; Webcast Audited</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="Actual post-market stock reaction (+0.38%) compared against pre-print options straddle implied move (±4.15%)." data-tip="Actual vs. Implied Move: NOK traded tightly at $7.91 (+0.38%) in after-hours action, well within the ±4.15% (±$0.35/sh) ATM weekly straddle band on solid top-line execution offset by working capital inventory investment.">Actual AH Move vs. Implied</span></span>
          <span class="strip-val" style="color: var(--bull-green);">{post_move_pct:+.2f}% (vs ±{opt_implied_pct:.2f}% Est)</span>
          <span class="kpi-sub">+${ah_price - reg_price:.2f}/sh Actual vs ±${opt_straddle:.2f}/sh <span class="tip" title="At-The-Money weekly straddle price prior to earnings." data-tip="ATM Straddle: Pre-earnings weekly option straddle priced at ±$0.35/sh (4.15% implied move).">ATM Straddle</span></span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 Net Sales (€5,154M, +10% reported / +9% CC) vs Wall Street Consensus (€4,980M)." data-tip="Q3 2026 Net Sales: Reported €5,154M (+10% YoY reported, +9% constant currency), beating €4,980M consensus by +€174M (+3.49%) led by Network Infrastructure (+15% CC) and AI &amp; Cloud (+123%).">Net Sales vs. Street</span></span>
          <span class="strip-val" style="color: var(--bull-green);">€5,154M <span style="font-size:12px;">(+9% CC | +€174M Beat)</span></span>
          <span class="kpi-sub">Street Est: €4,980M ($5.42B USD) | Beat: +3.49%</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 Comparable Diluted EPS (€0.09) and Reported GAAP Diluted EPS (€0.03) vs Consensus (€0.07)." data-tip="Q3 2026 EPS Beat: Reported €0.09 Comparable Diluted EPS (+50% YoY), beating €0.07 Street consensus by +€0.02 (+28.57%), alongside €0.03 Reported Diluted EPS (+200% YoY).">EPS (Comparable / Reported)</span></span>
          <span class="strip-val" style="color: var(--bull-green);">€0.09 Comp / €0.03 <span class="tip" title="Reported diluted EPS from continuing operations under IFRS (€0.03, up +200% YoY)." data-tip="Reported Diluted EPS rose to €0.03 on €176M profit from continuing operations.">Reported</span></span>
          <span class="kpi-sub">Beat €0.07 Consensus (+€0.02 / +28.6%) | Comp Op Margin: 11.7%</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">FY2026 <span class="tip tip-right" title="Official Full-Year 2026 guidance assumptions updated in the Q3 2026 release." data-tip="FY2026 Guidance Reaffirmed: Comparable operating profit of €2.1B–€2.6B tracking above midpoint; Network Infrastructure growth upgraded to 12%-14% CC; CapEx lowered to €750M-€850M.">Guidance Stance</span></span>
          <span class="strip-val" style="color: var(--bull-green);">Comp Op Profit: €2.1B–€2.6B</span>
          <span class="kpi-sub">Network Infra Guide Raised (12%-14% CC) | CapEx Lowered</span>
        </div>
      </div>
    </header>

    <!-- TRACK B: STICKY SECTION JUMP-NAV & PAIRED T-1 SWITCHER -->
    <nav class="post-jump-nav" style="position: sticky; top: 8px; z-index: 90; background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(10px); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 10px; padding: 8px 14px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
      <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
        <span style="font-size: 11px; font-weight: 800; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.06em; margin-right: 4px;">⚡ Jump To:</span>
        <a href="#row-1-kpis" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">1. Q3 KPIs</a>
        <a href="#row-1b-scorecard" style="font-size: 11.5px; color: #34d399; font-weight: 700; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.35);">1B. Beat/Miss &amp; Guidance Scorecard</a>
        <a href="#row-2-financials" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">2. Rolling 5Q Table (Q3 Actual + Q4E)</a>
        <a href="#row-3-fcf" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">3. Forensic FCF Bridge</a>
        <a href="#row-4-segments" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">4. Wins/Drags &amp; Call Audit</a>
        <a href="#row-5-peers" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">5. Comps &amp; Valuation</a>
        <a href="#row-6-sentiment" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">6. 4-Pillar Sentiment</a>
        <a href="#row-7-pm-matrix" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">7. PM Trade Matrix</a>
      </div>
      <div>
        <a href="NOK_T1_2026-10-22.html" style="font-size: 11.5px; color: #93c5fd; text-decoration: none; padding: 4px 10px; border-radius: 6px; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); display: flex; align-items: center; gap: 4px;">
          <span>📄 View Pre-Earnings T-1 Briefing</span>
        </a>
      </div>
    </nav>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS — ALL ROLLED FORWARD TO Q3 2026 ACTUALS) -->
    <section class="kpi-grid" id="row-1-kpis">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Working Capital (Q3 2026 Actual)</div>
          <span class="badge badge-warn">WORKING CAPITAL INVESTMENT</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Cash generated from operations before investing and financing." data-tip="Operating Cash Flow: In Q3 2026, Nokia generated €95M in net cash from operating activities against €744M adjusted operational profit, due to €560M net working capital outflow.">Operating Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">Adjusted Op Profit: €744M | Working Cap Outflow: €560M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">€95M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +€715M</span>
                <span class="badge badge-warn">YoY -84.09%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Purchase of property, plant, equipment and intangible assets (€194M in Q3 2026)." data-tip="Capital Expenditures: €194M deployed into optical test facilities, fab tooling, and software integration (+15.48% YoY); FY26 guide lowered to €750M-€850M.">Capital Expenditures (CapEx)</span></span>
              <span class="kpi-sub">CapEx Intensity: 3.76% of Net Sales | FY26 Lowered</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">(€194M)</span>
              <div class="delta-pair">
                <span class="badge badge-warn">QoQ +50.39%</span>
                <span class="badge badge-warn">YoY +15.48%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Standard Reported Free Cash Flow: Operating Cash Flow (€95M) minus CapEx (€194M) = -€99M." data-tip="Reported Free Cash Flow: -€99M in Q3 2026 as comparable operating profit was absorbed by €560M working capital investments to buffer optical transceivers for 2027.">Reported Free Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">Comparable Op Profit (€605M) offset by NWC &amp; Restructuring</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">(€99M)</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +€650M</span>
                <span class="badge badge-warn">YoY -€528M</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forensic True Free Cash Flow: Reported FCF (-€99M) minus SBC (€104M) minus Lease payments (€50M) = -€253M." data-tip="True Free Cash Flow: Total cash burn of -€253M in Q3 2026 after accounting for €104M share-based payments and €50M lease liabilities.">True FCF (ex-SBC &amp; Leases)</span> (Q3 2026)</span>
              <span class="kpi-sub">Q3 SBC: €104M | Lease Payments: €50M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">(€253M)</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +€632M</span>
                <span class="badge badge-warn">YoY -€587M</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING MARGINS (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Margins (Q3 2026 Actual)</div>
          <span class="badge badge-bull">11.7% COMPARABLE OP MARGIN</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Gross Profit (€2,176M, 42.22% margin) and Comparable Gross Profit (€2,299M, 44.6% margin)." data-tip="Gross Profit: Reported gross profit of €2,176M (42.22% margin) and comparable gross profit of €2,299M (44.60% margin), supported by 47.5% Mobile Infrastructure gross margin.">Gross Profit</span> (Q3 2026)</span>
              <span class="kpi-sub">Comparable GM: 44.6% (-20 bps YoY) | Reported GM: 42.2%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">€2,176M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +1.40%</span>
                <span class="badge badge-bull">YoY +4.36%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Operating Profit (€196M, 3.8% margin) and Comparable Operating Profit (€605M, 11.7% margin, +220 bps YoY)." data-tip="Operating Profit: Comparable operating profit jumped +35.04% YoY to €605M (11.7% margin) on operating leverage, while Reported operating profit hit €196M after €357M restructuring charges.">Operating Profit (Comparable / Reported)</span></span>
              <span class="kpi-sub">Comparable Op Profit: €605M (+35% YoY) | Margin: 11.7%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">€605M / €196M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Comp YoY +35.0%</span>
                <span class="badge badge-bull">Margin +220 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research &amp; Development (€1,251M reported / €1,109M comp) and SG&amp;A (€733M reported / €579M comp)." data-tip="Operating Expenses: Total reported OpEx of €1,980M (R&amp;D €1,251M + SG&amp;A €733M minus €4M other) declined -9.84% sequentially from €2,196M in Q2 2026.">Operating Expense Discipline</span> (Q3 2026)</span>
              <span class="kpi-sub">Reported OpEx: €1,980M | Comparable OpEx: €1,694M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">€1,980M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ -9.84%</span>
                <span class="badge badge-bull">OpEx Discipline</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Comparable Diluted EPS (€0.09, +50% YoY) and Reported Diluted EPS (€0.03, +200% YoY on €176M profit from continuing operations)." data-tip="Net Income &amp; EPS: Comparable Diluted EPS reached €0.09 (vs €0.06 in Q3 2025, beating €0.07 consensus); Reported Diluted EPS was €0.03 on €176M continuing profit.">Net Profit &amp; Diluted EPS</span> (Q3 2026)</span>
              <span class="kpi-sub">Comparable EPS: €0.09 (+50% YoY) | Reported EPS: €0.03</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">€0.09 / €0.03</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Comp EPS +50% YoY</span>
                <span class="badge badge-bull">Beat +€0.02</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS & LIQUIDITY (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Capital Return (Q3 2026)</div>
          <span class="badge badge-bull">€2.58B NET CASH FORTRESS</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Cash &amp; cash equivalents (€4,049M) plus current interest-bearing investments (€622M) = €4,671M gross cash." data-tip="Liquid Reserves: €4,671M gross cash &amp; interest-bearing investments vs €2,439M total interest-bearing debt, resulting in €2,584M net cash surplus.">Total Cash &amp; Liquid Investments</span> (Q3 2026)</span>
              <span class="kpi-sub">Cash: €4,049M | Interest-Bearing Financials: €622M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">€4,671M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Net Cash: €2,584M</span>
                <span class="badge badge-bull">Fortress Grade</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Long-term interest-bearing liabilities (€1,865M) plus short-term debt (€574M) = €2,439M." data-tip="Total Debt: €2,439M total interest-bearing debt (€1,865M long-term + €574M short-term), fully backed by €4.67B cash reserves.">Total Interest-Bearing Debt</span> (Q3 2026)</span>
              <span class="kpi-sub">Long-Term: €1,865M | Short-Term: €574M | Leases: €935M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">€2,439M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Net Cash Surplus</span>
                <span class="badge badge-neutral">Investment Grade</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Quarterly dividend declared of €0.03 per share, payable November 5, 2026." data-tip="Dividend Distribution: Board resolved €0.03/sh dividend payable Nov 5, 2026 under the AGM maximum €0.14/sh authorization for FY25.">Quarterly Dividend &amp; Authorization</span></span>
              <span class="kpi-sub">Declared: €0.03/sh (Payable Nov 5, 2026) | Max Guide: €0.14/sh</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">€0.03 / sh</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Payable Nov 5</span>
                <span class="badge badge-bull">~2.2% Yield</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total shareholders' equity as of September 30, 2026 (€21,237M)." data-tip="Stockholders' Equity: €21,237M equity (€3.75 per share) on €37,680M total assets.">Total Shareholders' Equity</span> (Q3 2026)</span>
              <span class="kpi-sub">Equity per share: €3.75 | Total Assets: €37,680M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">€21,237M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Book Val: €3.75/sh</span>
                <span class="badge badge-bull">+8.5% YoY</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT REVENUE MIX & POST-PRINT VALUATION (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Mix &amp; Post-Print Multiples (Q3 2026)</div>
          <span class="badge badge-bull">AI &amp; OPTICAL BREAKOUT</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Network Infrastructure revenue (€2,158M, +15% CC) driven by IP Networks (+43% CC) and Optical (+18% CC)." data-tip="Network Infrastructure Mix: Accounted for 41.87% of net sales with a 10.0% operating margin (€216M operating profit).">Network Infrastructure Mix</span></span>
              <span class="kpi-sub">Optical: €933M (+18% CC) | IP Networks: €839M (+43% CC)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">41.87% / €2,158M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">IP Net +43% CC</span>
                <span class="badge badge-bull">Optical +18% CC</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Mobile Infrastructure revenue (€2,902M, +5% YoY) with 14.5% segment operating margin (€420M profit)." data-tip="Mobile Infrastructure Mix: Accounted for 56.31% of net sales, benefiting from Q4-to-Q3 revenue pull-forward and Radio Networks growth (+11% rep).">Mobile Infrastructure Mix</span></span>
              <span class="kpi-sub">Radio: €1,958M (+11% rep) | Core: €519M | Tech: €425M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">56.31% / €2,902M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">14.5% Op Margin</span>
                <span class="badge badge-bull">Profit €420M</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Group net sales to AI &amp; Cloud customers grew +123% YoY; order intake grew +118% YoY to €1.5B." data-tip="AI &amp; Cloud Traction: Smashed expectations with €1.5B in new Q3 orders from hyperscalers including Google partnership.">AI &amp; Cloud Customer Orders</span></span>
              <span class="kpi-sub">Sales: +123% YoY | Order Intake: €1.5B (+118% YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">+123% Sales</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Orders +118%</span>
                <span class="badge badge-bull">Google €13B Deal</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Post-print valuation multiples at $7.91 After-Hours ADR price." data-tip="Post-Print Valuation: At $7.91 AH price, Nokia trades at ~16.4x forward Comparable EPS and ~1.9x Price/Sales, supported by €2.58B net cash surplus.">Post-Print Valuation (at $7.91 ADR)</span></span>
              <span class="kpi-sub">Fwd P/E: 16.4x | Trailing P/E: 56.3x | Net Cash: €2.58B</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">16.4x Fwd P/E</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Deep Value</span>
                <span class="badge badge-bull">Net Cash Hedge</span>
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
            Source: Nokia Corporation SEC Form 6-K Interim Report Filed Oct 22, 2026 • Official Q3 2026 Earnings Release • Wall Street Consensus Comparison
          </div>
        </div>
        <div style="display:flex; gap: 8px; align-items:center;">
          <span class="badge badge-bull">€0.09 COMP EPS BEAT + €5.15B NET SALES BEAT</span>
          <span class="badge badge-blue">T+0 POST-PRINT</span>
        </div>
      </div>

      <!-- TRACK B: T-1 PRE-PRINT THESIS VS. T+0 POST-PRINT REALITY AUDIT BANNER -->
      <div class="t1-vs-t0-audit" style="background: linear-gradient(90deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(59, 130, 246, 0.35); border-left: 4px solid #34d399; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
          <span style="font-weight: 800; font-size: 13px; color: #34d399; text-transform: uppercase; letter-spacing: 0.05em;">🔍 T-1 Pre-Earnings Thesis vs. T+0 Post-Print Reality Audit</span>
          <a href="NOK_T1_2026-10-22.html" style="font-size: 11.5px; color: #93c5fd; text-decoration: underline;">Open Original T-1 Briefing →</a>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; font-size: 12.3px; color: var(--text-secondary);">
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #93c5fd;">AI Optical &amp; Hyperscaler Supercycle Thesis:</strong><br>
            • <em>T-1 Forecast:</em> Modeled Network Infrastructure at €2.04B (+10% CC) on early AI data center demand.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">VALIDATED &amp; EXCEEDED</strong> — Network Infrastructure delivered <strong>€2,158M (+15% CC)</strong>, driven by <strong>IP Networks (+43% CC)</strong>, <strong>Optical (+18% CC)</strong>, and <strong>AI &amp; Cloud orders (+118% YoY to €1.5B)</strong>.
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #fcd34d;">Free Cash Flow &amp; Working Capital Caution:</strong><br>
            • <em>T-1 Forecast:</em> Flagged working capital friction and restructuring cash drag.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">SPOT-ON CALL</strong> — Q3 reported FCF came in at <strong>-€99M</strong> after <strong>€560M working capital outflow</strong>, prompting management to lower FY26 FCF conversion guide to <strong>35%-55%</strong> for €400M component buffering.
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #34d399;">Infinera Synergy &amp; Operating Profit Thesis:</strong><br>
            • <em>T-1 Forecast:</em> Looked for comparable operating profit near €525M and progress on Infinera integration.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">MASSIVE BEAT</strong> — Delivered <strong>€605M comparable operating profit (+35% YoY)</strong> and accelerated Infinera €200M synergy completion <strong>one year ahead of schedule to end-2026</strong>.
          </div>
        </div>
      </div>

      <!-- TABLE 1B-1: HEADLINE & COMPANY-SPECIFIC KPI BEAT / MISS SCORECARD -->
      <div style="margin-bottom: 20px;">
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-1: Headline &amp; Company-Specific KPI Beat / Miss Scorecard (Q3 2026 Actuals)</span>
          <span class="tip" title="Deterministic comparison of reported Q3 2026 actuals against Street pre-print consensus and T-1 whisper." data-tip="Beat / Miss Scorecard: Evaluates Q3 2026 delivery across headline IFRS/Comparable metrics and Nokia operational KPIs with visual magnitude bars.">[Methodology]</span>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style="min-width: 240px;">Metric / Company KPI</th>
                <th>Street Consensus</th>
                <th>T-1 Whisper</th>
                <th class="col-q0">Reported Actual (Q3 2026)</th>
                <th style="min-width: 190px;">Vs. Consensus (€ / % / bps)</th>
                <th>Vs. Whisper</th>
                <th>Verdict Badge</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="tip" title="Comparable Diluted EPS from continuing operations (€0.09, +50% YoY) vs Street Consensus (€0.07); Reported EPS: €0.03." data-tip="Comparable EPS: Printed at €0.09 (+50% YoY), beating Street consensus of €0.07 by +€0.02 (+28.57%).">Comparable Diluted EPS (€)</span></td>
                <td>€0.07</td>
                <td>€0.07</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">€0.09 <span style="font-size:11px; color:var(--text-muted);">(€0.03 Reported)</span></td>
                <td>
                  <span class="badge badge-bull">+€0.02 (+28.57%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:85%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+€0.02 (+28.57%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Total Net Sales (€5,154M, +10% reported / +9% constant currency) vs Street Consensus (€4,980M)." data-tip="Total Net Sales (€M): €5,154M (+10% YoY reported, +9% CC); beat Street consensus by +€174M (+3.49%).">Total Net Sales (€M) (+9% CC)</span></td>
                <td>€4,980M</td>
                <td>€5,020M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">€5,154M (+9% CC)</td>
                <td>
                  <span class="badge badge-bull">+€174M (+3.49%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:72%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+€134M (+2.67%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Network Infrastructure Net Sales (€2,158M, +17% reported / +15% CC) driven by IP Networks (+43% CC) and Optical (+18% CC)." data-tip="Network Infrastructure (€M): Beat consensus of €2,040M by +€118M (+5.78%) on hyperscaler AI data center interconnect sales.">Network Infrastructure Net Sales (€M)</span></td>
                <td>€2,040M</td>
                <td>€2,060M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">€2,158M (+15% CC)</td>
                <td>
                  <span class="badge badge-bull">+€118M (+5.78%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:80%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+€98M (+4.76%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="AI &amp; Cloud Net Sales YoY Growth (+123% YoY) and quarterly order intake (+118% YoY to €1.5B)." data-tip="AI &amp; Cloud Orders: Net sales more than doubled (+123% YoY) with €1.5B in new orders, beating expectations by +5,800 bps.">AI &amp; Cloud Customer Sales Growth (% YoY)</span></td>
                <td>+65.0%</td>
                <td>+75.0%</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">+123.0% (+118% Orders)</td>
                <td>
                  <span class="badge badge-bull">+5,800 bps / €1.5B Orders</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:95%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+4,800 bps</span></td>
                <td><span class="badge badge-bull">MASSIVE BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Comparable Operating Profit (€605M, +35% YoY) vs Street Consensus (€525M); margin reached 11.7% (+220 bps YoY)." data-tip="Comparable Operating Profit (€M): Beat consensus by +€80M (+15.24%) with 11.7% operating margin.">Comparable Operating Profit (€M)</span></td>
                <td>€525M</td>
                <td>€540M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">€605M (11.7% Margin)</td>
                <td>
                  <span class="badge badge-bull">+€80M (+15.24%) / +150 bps</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:88%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+€65M (+12.04%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Reported Free Cash Flow (-€99M) after €560M working capital outflow vs expectations." data-tip="Reported Free Cash Flow (€M): -€99M in Q3 2026; lower than Street estimate of +€150M due to strategic component inventory build for 2027.">Reported Free Cash Flow (€M)</span></td>
                <td>+€150M</td>
                <td>+€100M</td>
                <td class="col-q0" style="font-weight:700; color: #fcd34d;">-€99M (€95M OCF)</td>
                <td>
                  <span class="badge badge-warn">-€249M (Working Cap Outflow)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:40%; height:100%; background:#f59e0b;"></div></div>
                </td>
                <td><span class="badge badge-warn">-€199M</span></td>
                <td><span class="badge badge-warn">CASH DRAG / NWC BUILD</span></td>
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
              <div style="width: 88%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <strong style="color: #34d399;">88 / 100 (High)</strong>
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
                <td><span class="tip" title="Network Infrastructure Constant Currency Sales Growth Target." data-tip="Network Infrastructure Growth: Guided +10% to +12% CC; delivered +15% CC (+17% reported) in Q3 2026.">Network Infrastructure Growth</span></td>
                <td>+10% to +12% CC Growth for FY26</td>
                <td style="font-weight:600; color: #34d399;">+15.0% Constant Currency (+16.65% Reported to €2,158M)</td>
                <td>Exceeded guidance band by +300 bps, driven by IP Networks (+43% CC) and Optical (+18% CC).</td>
                <td><span class="badge badge-bull">BEAT OWN GUIDE</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Full-Year 2026 Comparable Operating Profit Target (€2.1B–€2.6B)." data-tip="Comparable Operating Profit: Reaffirmed €2.1B-€2.6B corridor with Q3 delivery of €605M (+35% YoY).">FY2026 Comparable Operating Profit</span></td>
                <td>EUR 2.1 billion to EUR 2.6 billion</td>
                <td style="font-weight:600; color: #34d399;">€605M in Q3 (+35% YoY); 9M Total Reached €1,340M (+31% YoY)</td>
                <td>On track to deliver full-year comparable operating profit above the midpoint of the range.</td>
                <td><span class="badge badge-bull">MET GUIDE</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Infinera Acquisition Integration &amp; Synergy Capture." data-tip="Infinera Synergies: Originally guided €200M net synergies by end-2027; accelerated to complete by end-2026 (1 year ahead).">Infinera Synergy Acceleration</span></td>
                <td>€200M net synergies run-rate by end-2027</td>
                <td style="font-weight:600; color: #34d399;">Integration to complete by end of 2026 (1 year ahead of plan)</td>
                <td>Accelerated integration timeline delivers €200M in annual net synergies 12 months early.</td>
                <td><span class="badge badge-bull">BEAT OWN GUIDE</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Free Cash Flow Conversion from Comparable Operating Profit." data-tip="FCF Conversion: Lowered corridor from 45%-65% to 35%-55% due to €400M working capital buffering.">Free Cash Flow Conversion</span></td>
                <td>45% to 65% cash conversion from comp op profit</td>
                <td style="font-weight:600; color: #fcd34d;">Lowered to 35% to 55%; Q3 reported FCF was -€99M</td>
                <td>Management reset FCF conversion to fund €400M strategic component buffer for 2027 growth.</td>
                <td><span class="badge badge-warn">LOWERED GUIDE</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-3: FORWARD GUIDANCE RESET -->
      <div>
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-3: Forward Guidance Reset (New Q4 2026 &amp; FY2026 Guidance vs. Pre-Print Street Expectations)</span>
          <span class="tip" title="Evaluates how new forward guidance changes future earnings power relative to Wall Street consensus." data-tip="Forward Guidance Reset: Audits upgraded Network Infrastructure growth (12%-14% CC), Q4 revenue seasonality (+20%-24% QoQ), lowered CapEx (€750M-€850M), and FCF conversion adjustment.">[Re-Rating Matrix]</span>
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
                <td><span class="tip" title="Network Infrastructure FY2026 constant currency sales growth." data-tip="Network Infra Guidance: Upgraded to 12%-14% CC growth for full year 2026.">Network Infrastructure FY26 Growth</span></td>
                <td>+10% to +12% CC Growth</td>
                <td style="font-weight:600; color: #34d399;">12% to 14% Constant Currency Growth (Upgraded)</td>
                <td>+200 bps guidance upgrade</td>
                <td><span class="badge badge-bull">RAISED</span></td>
                <td>Combined Optical and IP Networks outperforming prior 18%-20% assumption; hyperscaler demand accelerating.</td>
              </tr>
              <tr>
                <td><span class="tip" title="Q4 2026 Net Sales Sequential Seasonality." data-tip="Q4 Seasonality: Guided +20% to +24% QoQ revenue increase (implies €6,185M to €6,391M).">Q4 2026 Net Sales Seasonality</span></td>
                <td>+18% to +20% QoQ Increase (~€6.10B)</td>
                <td style="font-weight:600; color: #34d399;">+20% to +24% QoQ Increase (Implies €6,185M–€6,391M)</td>
                <td>+€85M to +€290M above Street expectations</td>
                <td><span class="badge badge-bull">MAINTAINED / IN-LINE</span></td>
                <td>Strong AI &amp; Cloud backlog (€1.5B Q3 orders, +118% YoY) and optical deployments scheduled for Q4 delivery.</td>
              </tr>
              <tr>
                <td><span class="tip" title="Full-Year 2026 Capital Expenditures." data-tip="FY2026 CapEx: Reduced assumption to €750M-€850M (cash-flow positive).">Full-Year 2026 Capital Expenditures</span></td>
                <td>EUR 850 million to EUR 900 million</td>
                <td style="font-weight:600; color: #34d399;">EUR 750M to EUR 850M (Reduced Assumption)</td>
                <td>-€50M to -€100M CapEx relief</td>
                <td><span class="badge badge-bull">LOWERED</span></td>
                <td>Changes in real estate footprint and shifting timing of certain optical manufacturing payments into 2027.</td>
              </tr>
              <tr>
                <td><span class="tip" title="Free Cash Flow Conversion from Comparable Operating Profit." data-tip="FCF Conversion: Lowered to 35%-55% to fund €400M working capital buffer.">FY2026 FCF Conversion Rate</span></td>
                <td>45% to 55% (~€1.10B–€1.30B FCF)</td>
                <td style="font-weight:600; color: #fcd34d;">35% to 55% Conversion (~€800M–€1.30B FCF)</td>
                <td>-1,000 bps at lower bound (~€150M headwind)</td>
                <td><span class="badge badge-warn">LOWERED</span></td>
                <td>Strategic €400M inventory build to secure optical transceivers and de-risk the 2027 25%-30% optical growth ramp.</td>
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
          <div class="card-subtitle">Audited SEC Form 6-K financial results in EUR Millions (rolled forward to Q3 2026 Actuals + Post-Print Q4 2026E Estimates)</div>
        </div>
        <span class="badge badge-bull">ROLLED 5Q ACTUALS (Q3'25 → Q3'26 ACTUAL)</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th style="min-width: 220px;">Financial Metric (€ Millions)</th>
              <th>Q3 2025<br><span style="font-size:10px;color:var(--text-muted);">(Sep 30, 2025)</span></th>
              <th>Q4 2025<br><span style="font-size:10px;color:var(--text-muted);">(Dec 31, 2025)</span></th>
              <th>Q1 2026<br><span style="font-size:10px;color:var(--text-muted);">(Mar 31, 2026)</span></th>
              <th>Q2 2026<br><span style="font-size:10px;color:var(--text-muted);">(Jun 30, 2026)</span></th>
              <th class="col-q0">Q3 2026 (Actual)<br><span style="font-size:10px;color:var(--accent-blue);">(Sep 30, 2026 6-K)</span></th>
              <th><span class="tip" title="Quarter-over-Quarter: Sequential change from Q2 2026 to Q3 2026 Actual." data-tip="Q3 QoQ Delta: Sequential percentage variance between Q2 2026 and Q3 2026 Actual.">Q3 QoQ</span></th>
              <th><span class="tip" title="Year-over-Year: Percentage change from Q3 2025 to Q3 2026 Actual." data-tip="Q3 YoY Delta: 12-month percentage variance between Q3 2025 and Q3 2026 Actual.">Q3 YoY</span></th>
              <th class="col-est">Q4 2026E<br><span style="font-size:10px;color:#34d399;">(New Guide / Est.)</span></th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background-color: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Total Net Sales across Network Infrastructure, Mobile Infrastructure, and Portfolio Businesses (€5,154M in Q3 2026)." data-tip="Total Net Sales (€M): Printed at €5,154M in Q3 2026 (+7.04% QoQ, +6.75% YoY reported / +9% CC); Q4 2026E guided at €6,288M.">Total Net Sales (€M)</span></td>
              <td>€4,828</td>
              <td>€6,125</td>
              <td>€4,497</td>
              <td>€4,815</td>
              <td class="col-q0" style="color: var(--accent-blue);">€5,154</td>
              <td><span class="badge badge-bull">+7.04%</span></td>
              <td><span class="badge badge-bull">+6.75%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">€6,288</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Network Infrastructure Segment Net Sales: Optical Networks, IP Networks, and Fixed Networks (€2,158M in Q3 2026)." data-tip="Network Infrastructure (€M): €2,158M in Q3 2026 (+5.94% QoQ, +18.57% YoY reported / +15% CC) with a 10.0% operating margin.">Network Infrastructure (€M)</span></td>
              <td>€1,820</td>
              <td>€2,450</td>
              <td>€1,818</td>
              <td>€2,037</td>
              <td class="col-q0">€2,158</td>
              <td><span class="badge badge-bull">+5.94%</span></td>
              <td><span class="badge badge-bull">+18.57%</span></td>
              <td class="col-est">€2,650</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Mobile Infrastructure Segment Net Sales: Radio Networks, Core Software, and Technology Standards (€2,902M in Q3 2026)." data-tip="Mobile Infrastructure (€M): €2,902M in Q3 2026 (+27.45% QoQ, +18.45% YoY reported / +5% CC) with a 14.5% operating margin.">Mobile Infrastructure (€M)</span></td>
              <td>€2,450</td>
              <td>€2,920</td>
              <td>€2,170</td>
              <td>€2,277</td>
              <td class="col-q0">€2,902</td>
              <td><span class="badge badge-bull">+27.45%</span></td>
              <td><span class="badge badge-bull">+18.45%</span></td>
              <td class="col-est">€3,520</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Portfolio Businesses (€96M) plus Group Common &amp; Other (-€2M) = €94M in Q3 2026." data-tip="Portfolio Businesses (€M): Non-core units (Microwave Radio, Site Implementation) generating €94M net sales.">Portfolio Businesses &amp; Other (€M)</span></td>
              <td>€558</td>
              <td>€755</td>
              <td>€509</td>
              <td>€501</td>
              <td class="col-q0">€94</td>
              <td><span class="badge badge-neutral">-81.24%</span></td>
              <td><span class="badge badge-neutral">-83.15%</span></td>
              <td class="col-est">€118</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Gross Profit under IFRS reported basis: Net sales minus cost of sales (€2,176M in Q3 2026)." data-tip="Gross Profit (€M): Reported gross profit of €2,176M in Q3 2026 (42.22% margin); comparable gross profit was €2,299M (44.60% margin).">Gross Profit (€M)</span></td>
              <td>€2,110</td>
              <td>€2,754</td>
              <td>€1,988</td>
              <td>€2,146</td>
              <td class="col-q0" style="color: var(--accent-blue);">€2,176</td>
              <td><span class="badge badge-bull">+1.40%</span></td>
              <td><span class="badge badge-bull">+3.13%</span></td>
              <td class="col-est" style="color:#34d399;">€2,760</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td><span class="tip" title="Total Operating Expenses: R&amp;D (€1,251M) + SG&amp;A (€733M) - Other (€4M) = €1,980M in Q3 2026." data-tip="Operating Expenses (€M): Total reported OpEx of €1,980M in Q3 2026 (-9.84% QoQ, +5.83% YoY).">Total Operating Expenses (€M)</span></td>
              <td>€1,871</td>
              <td>€2,317</td>
              <td>€1,925</td>
              <td>€2,196</td>
              <td class="col-q0">€1,980</td>
              <td><span class="badge badge-bull">-9.84%</span></td>
              <td><span class="badge badge-neutral">+5.83%</span></td>
              <td class="col-est">€2,050</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus total operating expenses (€196M in Q3 2026; Comparable Op Profit: €605M)." data-tip="Operating Profit (€M): Reported operating profit hit €196M (rebounding from -€50M in Q2 2026); Comparable operating profit surged to €605M (+35% YoY).">Operating Income (EBIT) (€M)</span></td>
              <td>€239</td>
              <td>€437</td>
              <td>€63</td>
              <td>(€50)</td>
              <td class="col-q0" style="color: var(--bull-green);">€196</td>
              <td><span class="badge badge-bull">+€246M</span></td>
              <td><span class="badge badge-neutral">-17.99%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">€710</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td><span class="tip" title="Reported Profit from continuing operations (€176M in Q3 2026; Comparable continuing profit: €498M)." data-tip="Net Profit (€M): Profit from continuing operations of €176M in Q3 2026 (+95.56% YoY); total profit for period was €156M.">Profit from Continuing Operations (€M)</span></td>
              <td>€78</td>
              <td>€542</td>
              <td>€86</td>
              <td>€2</td>
              <td class="col-q0">€176</td>
              <td><span class="badge badge-bull">+€174M</span></td>
              <td><span class="badge badge-bull">+125.64%</span></td>
              <td class="col-est">€550</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Reported diluted EPS from continuing operations (€0.03 in Q3 2026; Comparable diluted EPS: €0.09)." data-tip="Diluted EPS (€): Reported diluted EPS of €0.03 (+200% YoY); Comparable diluted EPS of €0.09 (+50% YoY).">Diluted EPS (€) (Reported / Comparable)</span></td>
              <td>€0.01</td>
              <td>€0.10</td>
              <td>€0.02</td>
              <td>€0.00</td>
              <td class="col-q0" style="color: var(--bull-green);">€0.03 / €0.09</td>
              <td><span class="badge badge-bull">+€0.03</span></td>
              <td><span class="badge badge-bull">+200.0%</span></td>
              <td class="col-est" style="color:#34d399;">€0.10 / €0.14</td>
            </tr>
            <tr style="font-weight: 700; background-color: rgba(16, 185, 129, 0.05);">
              <td><span class="tip" title="Net cash flows from operating activities (€95M in Q3 2026)." data-tip="Operating Cash Flow (€M): Rebounded to €95M in Q3 2026 (from -€620M in Q2 2026); absorbed €560M working capital outflow.">Operating Cash Flow (€M)</span></td>
              <td>€597</td>
              <td>€375</td>
              <td>€783</td>
              <td>(€620)</td>
              <td class="col-q0" style="color: var(--bull-green);">€95</td>
              <td><span class="badge badge-bull">+€715M</span></td>
              <td><span class="badge badge-warn">-84.09%</span></td>
              <td class="col-est" style="color:#34d399;">€1,250</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Capital Expenditures: Purchase of PP&amp;E and intangible assets (€194M in Q3 2026)." data-tip="Capital Expenditures (€M): €194M in Q3 2026 (+50.39% QoQ, +15.48% YoY).">Capital Expenditures (€M)</span></td>
              <td>(€168)</td>
              <td>(€148)</td>
              <td>(€154)</td>
              <td>(€129)</td>
              <td class="col-q0">(€194)</td>
              <td><span class="badge badge-warn">+50.39%</span></td>
              <td><span class="badge badge-warn">+15.48%</span></td>
              <td class="col-est">(€250)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Standard Free Cash Flow: Operating cash flow minus CapEx (-€99M in Q3 2026)." data-tip="Reported Free Cash Flow (€M): -€99M in Q3 2026 (+€650M QoQ improvement from -€749M in Q2 2026).">Reported Free Cash Flow (€M)</span></td>
              <td>€429</td>
              <td>€227</td>
              <td>€629</td>
              <td>(€749)</td>
              <td class="col-q0" style="color: var(--warn-amber);">(€99)</td>
              <td><span class="badge badge-bull">+€650M</span></td>
              <td><span class="badge badge-warn">-€528M</span></td>
              <td class="col-est" style="color:#34d399;">€1,000</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Share-based payments expense (€104M in Q3 2026)." data-tip="Share-Based Compensation (€M): €104M in Q3 2026.">Share-Based Compensation (€M)</span></td>
              <td>(€95)</td>
              <td>(€110)</td>
              <td>(€105)</td>
              <td>(€136)</td>
              <td class="col-q0">(€104)</td>
              <td><span class="badge badge-bull">-23.53%</span></td>
              <td><span class="badge badge-warn">+9.47%</span></td>
              <td class="col-est">(€110)</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Lease payments from financing activities (€50M in Q3 2026)." data-tip="Finance Lease Payments (€M): €50M in Q3 2026.">Principal Lease Payments (€M)</span></td>
              <td>€0</td>
              <td>€0</td>
              <td>€0</td>
              <td>€0</td>
              <td class="col-q0">(€50)</td>
              <td><span class="badge badge-neutral">New Tag</span></td>
              <td><span class="badge badge-neutral">Leases</span></td>
              <td class="col-est">(€50)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Forensic True Free Cash Flow: Reported FCF (-€99M) minus SBC (€104M) minus Leases (€50M) = -€253M." data-tip="True Free Cash Flow (€M): Normalized cash burn of -€253M in Q3 2026 (+€632M improvement QoQ).">True Free Cash Flow (ex-SBC &amp; Leases) (€M)</span></td>
              <td>€334</td>
              <td>€117</td>
              <td>€524</td>
              <td>(€885)</td>
              <td class="col-q0" style="color: var(--warn-amber);">(€253)</td>
              <td><span class="badge badge-bull">+€632M</span></td>
              <td><span class="badge badge-warn">-€587M</span></td>
              <td class="col-est" style="color:#34d399;">€840</td>
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
          <div class="card-subtitle">Forensic deconstruction of the +123% AI &amp; Cloud surge, €605M Comparable Operating Profit, and -€253M True Free Cash Flow</div>
        </div>
        <span class="badge badge-bull">OPTICAL INFLECTION &amp; INVENTORY BUFFER</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>1. AI &amp; Cloud Supercycle: +123% Sales Surge &amp; €1.5B in New Orders (+118% YoY)</span>
              <span class="badge badge-bull">GOOGLE €13B FINLAND PARTNERSHIP</span>
            </div>
            <p>
              Nokia's strategy under CEO Justin Hotard to capture AI data center interconnect demand delivered stunning acceleration. Net sales to AI &amp; Cloud customers <strong>surged +123% YoY</strong>, with quarterly <strong>order intake jumping +118% YoY to €1.5 billion</strong>. Hyperscaler demand for high-capacity 800G/1.6T optical transceivers and IP routing platforms validated the Infinera acquisition, highlighted by Nokia's core role in Google's €13 billion Finland data center expansion.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>2. Optical &amp; IP Networks Operating Leverage: Comparable Op Margin Hits 11.7% (+220 bps YoY)</span>
              <span class="badge badge-bull">IP +43% CC | OPTICAL +18% CC</span>
            </div>
            <p>
              Within Network Infrastructure (€2,158M, +15% CC), <strong>IP Networks grew +43% CC</strong> and <strong>Optical Networks rose +18% CC</strong>, expanding segment gross margin to 41.2% and delivering €216M in segment operating profit (+51.05% YoY). This high-margin routing volume propelled group comparable operating profit to <strong>€605M (+35% YoY)</strong>, proving that proprietary silicon (FP5 routing and PSE coherent optics) provides substantial pricing power.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--warn-amber);">
            <div class="forensic-item-title">
              <span>3. Working Capital Drag: €560M Cash Outflow Leads to -€99M Reported FCF</span>
              <span class="badge badge-warn">STRATEGIC COMPONENT BUFFER</span>
            </div>
            <p>
              Despite €744M in adjusted pre-working capital operating profit, Nokia posted <strong>negative €99M in reported FCF</strong> and <strong>negative €253M in forensic True FCF</strong>. This was driven by a <strong>€560M working capital outflow</strong> (receivables up €227M, inventories up €131M, payables down €205M) alongside €283M in cash restructuring charges. Management lowered full-year FCF conversion to 35%-55% to commit an additional €400M to buffer optical components for a locked-in 2027 ramp.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Infinera Synergies Pulled Forward: €200M Net Run-Rate 12 Months Early</span>
              <span class="badge badge-bull">END-2026 COMPLETION</span>
            </div>
            <p>
              Justin Hotard confirmed that the Infinera optical platform integration is running a full year ahead of schedule, with the full <strong>€200 million annual net synergy target</strong> now slated for delivery by end of 2026 rather than end of 2027. Combined Optical and IP Networks are officially guided to grow <strong>25% to 30% in 2027</strong>.
            </p>
          </div>
        </div>

        <!-- FCF WATERFALL BRIDGE -->
        <div class="fcf-bridge-box">
          <div class="fcf-bridge-header">
            <span>Deterministic Cash Flow Bridge (Q3 2026 Reported Actuals)</span>
            <span style="color: var(--text-muted); font-size: 11px;">€M EUR • Q3 2026 6-K Actual</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Reported Operating Cash Flow (OCF)</span>
            <span class="waterfall-val" style="color: #34d399;">+€{q0_ocf:,.0f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Capital Expenditures (PP&amp;E &amp; Intangibles)</span>
            <span class="waterfall-val" style="color: #f87171;">-€{q0_capex:,.0f}M</span>
          </div>
          <div class="waterfall-row" style="border-top: 1px dashed rgba(255, 255, 255, 0.15); padding-top: 6px;">
            <span class="waterfall-label" style="font-weight: 700; color: #f8fafc;">(=) Standard Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="font-weight: 700; color: #fcd34d;">-€{abs(q0_rep_fcf):,.0f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Share-Based Compensation (SBC)</span>
            <span class="waterfall-val" style="color: #f87171;">-€{q0_sbc:,.0f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Principal Lease Payments (Financing Outflows)</span>
            <span class="waterfall-val" style="color: #f87171;">-€{q0_leases:,.0f}M</span>
          </div>
          <div class="waterfall-row" style="border-top: 2px solid rgba(59, 130, 246, 0.5); padding-top: 8px; margin-top: 4px;">
            <span class="waterfall-label" style="font-weight: 800; color: #60a5fa;">(=) Forensic True Free Cash Flow</span>
            <span class="waterfall-val" style="font-weight: 800; color: #fcd34d;">-€{abs(q0_true_fcf):,.0f}M</span>
          </div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 10px; line-height: 1.4;">
            <em>Audit Note:</em> Despite €744M in cash flow from operations before working capital, €560M in net working capital outflows and €194M CapEx drove reported FCF to -€99M. True FCF of -€253M accounts for €104M share-based payments and €50M lease principal payments.
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         6. ROW 4: OPERATIONAL TAILWINDS VS. EXECUTION DRAGS & CALL Q&A AUDIT
         ========================================================================== -->
    <section class="card" id="row-4-segments" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Operational Wins vs. Execution Drags &amp; Earnings Call Analyst Q&amp;A Audit</div>
          <div class="card-subtitle">Source: Q3 2026 Earnings Call Transcript • Top 3 Hardest Sell-Side Analyst Questions &amp; Executive Responses (Analyst Q&A Forensic Highlights)</div>
        </div>
        <span class="badge badge-bull">Q3 2026 POST-CALL VERDICT</span>
      </div>

      <div class="audit-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
        <!-- WINS -->
        <div class="audit-card" style="background: rgba(11, 15, 25, 0.55); border: 1px solid var(--border-color); border-left: 4px solid var(--bull-green); padding: 14px 16px; border-radius: 8px;">
          <div style="font-weight: 700; color: var(--bull-green); font-size: 14px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
            <span>🟢 4 Core Operational Wins (What Went Right)</span>
          </div>
          <ul style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.55; padding-left: 18px; margin: 0;">
            <li><strong>IP &amp; Optical Networks Hyper-Growth:</strong> IP Networks grew +43% CC and Optical Networks rose +18% CC as cloud hyperscalers expanded data center interconnect infrastructure.</li>
            <li><strong>AI &amp; Cloud Commercial Explosion:</strong> AI &amp; Cloud net sales surged +123% YoY, capturing €1.5B in quarterly orders (+118% YoY) anchored by Google's €13B Finland hub.</li>
            <li><strong>Infinera Synergies Pulled Forward:</strong> Management confirmed integration is tracking 12 months ahead of schedule, capturing €200M in annual net synergies by end-2026.</li>
            <li><strong>Mobile Infrastructure Margin Resilience:</strong> Mobile gross margin reached 47.5% and operating margin hit 14.5% (€420M profit), benefiting from product mix and cost discipline.</li>
          </ul>
        </div>

        <!-- DRAGS -->
        <div class="audit-card" style="background: rgba(11, 15, 25, 0.55); border: 1px solid var(--border-color); border-left: 4px solid var(--warn-amber); padding: 14px 16px; border-radius: 8px;">
          <div style="font-weight: 700; color: var(--warn-amber); font-size: 14px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
            <span>🟡 4 Execution &amp; Cash Flow Drags (What Went Wrong)</span>
          </div>
          <ul style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.55; padding-left: 18px; margin: 0;">
            <li><strong>Working Capital Cash Burn:</strong> Working capital outflow reached €560M in the quarter, pulling reported FCF into negative territory (-€99M) and True FCF to -€253M.</li>
            <li><strong>FCF Conversion Guide Lowered:</strong> Full-year FCF conversion guidance was trimmed from 45%-65% to 35%-55% to fund an extra €400M in strategic inventory.</li>
            <li><strong>Mobile Revenue Pull-Forward:</strong> CFO Marco Wirén acknowledged €60M-€80M of Mobile Infrastructure revenue was pulled forward from Q4 into Q3, softening Q4 mobile comps.</li>
            <li><strong>Restructuring Cash Outflows:</strong> Accelerated portfolio simplification triggered €283M in quarterly restructuring charges and €800M-€900M in expected FY cash outflows.</li>
          </ul>
        </div>
      </div>

      <!-- CALL Q&A FORENSIC AUDIT -->
      <div id="row-4b-audit" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 16px; margin-top: 10px;">
        <div style="font-weight: 700; font-size: 14px; color: #93c5fd; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
          <span>🎯 Top 3 Analyst Q&A Conference Call Exchanges — Hardest Analyst Questions Audited</span>
          <span class="badge badge-bull">EXECUTIVE AUDIT</span>
        </div>

        <div class="audit-list" style="display: flex; flex-direction: column; gap: 12px;">
          <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #34d399; padding: 12px 14px; border-radius: 6px;">
            <div style="font-weight: 700; color: #34d399; font-size: 13.5px; margin-bottom: 4px;">
              1. Hyperscaler AI &amp; Cloud Order Momentum &amp; 2027 Pipeline Visibility — Alexander Duval (Goldman Sachs)
            </div>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
              <strong>Analyst Question:</strong> Network Infrastructure delivered standout growth (+15% CC), with AI &amp; Cloud order intake jumping +118% YoY to €1.5B. How sustainable is this hyperscaler order velocity, and what gives you conviction in guiding combined Optical &amp; IP Networks to grow 25% to 30% in 2027?
            </p>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
              <strong>Management Response &amp; Takeaway:</strong> CEO Justin Hotard explained that cloud hyperscalers have moved from localized proof-of-concept AI clusters to multi-campus distributed AI networks requiring high-density coherent optics. He cited the Google €13B Finland partnership as evidence of Nokia's differentiated coherent DSP silicon and routing architecture, confirming firm conviction in 25%-30% growth for 2027.
            </p>
          </div>

          <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #60a5fa; padding: 12px 14px; border-radius: 6px;">
            <div style="font-weight: 700; color: #93c5fd; font-size: 13.5px; margin-bottom: 4px;">
              2. Mobile Infrastructure Revenue Pull-Forward &amp; Margin Durability — Francois-Xavier Bouvignies (UBS)
            </div>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
              <strong>Analyst Question:</strong> Mobile Infrastructure grew 5% YoY and generated an impressive 14.5% segment operating margin. To what extent was this driven by revenue accelerated from Q4 into Q3, and will Mobile operating margins hold above 12% in Q4?
            </p>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
              <strong>Management Response &amp; Takeaway:</strong> CFO Marco Wirén acknowledged that roughly €60M-€80M of Mobile deliveries were pulled forward from Q4 due to carrier installation schedules. However, he emphasized that structural gross margin improvements (47.5%) and strict commercial discipline will keep Q4 Mobile operating profitability solid.
            </p>
          </div>

          <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #f59e0b; padding: 12px 14px; border-radius: 6px;">
            <div style="font-weight: 700; color: #fcd34d; font-size: 13.5px; margin-bottom: 4px;">
              3. Working Capital Cash Outflow &amp; FCF Conversion Reset — Sandeep Deshpande (JPMorgan)
            </div>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
              <strong>Analyst Question:</strong> Free cash flow was negative €99M in Q3, and you reduced your full-year FCF conversion guidance from 45%-65% to 35%-55%. Why are you injecting an additional €400M into working capital, and does this risk component obsolescence?
            </p>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
              <strong>Management Response &amp; Takeaway:</strong> Justin Hotard and Marco Wirén defended the inventory build, explaining that 85%+ of the €400M working capital commitment is dedicated to securing high-speed optical transceivers, DSPs, and switching ASICs for confirmed 2027 customer deliveries. The inventory is backed by firm hyperscaler orders rather than speculative carrier stocking.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         7. ROW 5: COMPETITIVE MOAT & PEER BENCHMARKING (Q3 2026 ACTUALS)
         ========================================================================== -->
    <section class="card-grid" id="row-5-peers" style="grid-template-columns: 1fr 1fr; margin-bottom: 24px;">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Global Telecom &amp; Optical Networking Peers</div>
          <span class="badge badge-blue">POST-PRINT COMP MATRIX (Q3 2026)</span>
        </div>

        <div class="table-wrapper" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th style="min-width:140px;">Ticker / Peer</th>
                <th><span class="tip" title="Constant-Currency YoY Revenue Growth in Q3 2026." data-tip="YoY Revenue Growth: +9.0% CC (+10% reported) for Nokia.">YoY Rev Growth</span></th>
                <th><span class="tip" title="Comparable / Non-GAAP Gross Margin percentage in Q3 2026." data-tip="Gross Margin: 44.6% Comparable (42.2% Reported) for Nokia.">Gross Margin</span></th>
                <th><span class="tip" title="Comparable Operating Margin in Q3 2026." data-tip="Operating Margin: 11.7% Comparable (3.8% Reported) for Nokia.">Op Margin (Adj)</span></th>
                <th><span class="tip" title="GAAP / IFRS Operating Cash Flow Margin in Q3 2026." data-tip="OCF Margin: €95M OCF / €5,154M Net Sales = 1.84%.">OCF Margin</span></th>
                <th><span class="tip tip-right" title="Forward P/E ratio at $7.91 After-Hours ADR price." data-tip="Forward P/E: 16.4x at $7.91 AH ADR price.">Fwd P/E</span></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color:var(--accent-blue);">NOK (Q3 Actual)</strong></td>
                <td><span class="badge badge-bull">+9.0% CC (+10% Rep)</span></td>
                <td><strong style="color:var(--bull-green);">44.60%</strong> <span style="font-size:10px;color:var(--text-muted);">(42.2% Rep)</span></td>
                <td><strong style="color:var(--bull-green);">11.70%</strong></td>
                <td><strong style="color:var(--warn-amber);">+1.84%</strong></td>
                <td style="color:var(--bull-green);">16.4x</td>
              </tr>
              <tr>
                <td><strong>ERIC (Ericsson)</strong></td>
                <td><span class="badge badge-neutral">-1.5% CC</span></td>
                <td>46.20%</td>
                <td>10.80%</td>
                <td>+8.50%</td>
                <td>15.2x</td>
              </tr>
              <tr>
                <td><strong>CIEN (Ciena Corp.)</strong></td>
                <td><span class="badge badge-bull">+11.5% CC</span></td>
                <td>43.80%</td>
                <td>12.20%</td>
                <td>+10.40%</td>
                <td>19.8x</td>
              </tr>
              <tr>
                <td><strong>CSCO (Cisco Systems)</strong></td>
                <td><span class="badge badge-neutral">+2.0% CC</span></td>
                <td>67.50%</td>
                <td>32.50%</td>
                <td>+26.80%</td>
                <td>17.5x</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">Optical Leadership &amp; Net Cash Valuation Advantage</span>
              <span class="badge badge-bull">€2.58B NET CASH PILLOW</span>
            </div>
            <p>
              • <strong>Nokia vs. Ericsson:</strong> While Ericsson remains heavily tied to cyclical 5G carrier RAN spending (-1.5% CC), Nokia's expanding Network Infrastructure exposure (+15% CC, €2,158M) allows it to capture high-margin AI hyperscaler capex.<br>
              • <strong>Valuation Support:</strong> At $7.91 AH, Nokia trades at just <strong>16.4x forward earnings</strong> backed by <strong>€2,584M in net cash (€0.46/sh cash cushion)</strong> and a ~2.2% dividend yield floor.
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
              <span class="audit-point-title">1. Hyperscaler AI Data Center Optical Interconnect (+123% YoY)</span>
              <span class="badge badge-bull">€1.5B Q3 ORDERS</span>
            </div>
            <p>
              Hyperscale cloud operators are deploying Nokia's 800G/1.6T optical routing and coherent DSP platforms, led by the Google €13B Finland data center partnership.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Infinera Full Integration by End of 2026 (€200M Net Synergies)</span>
              <span class="badge badge-blue">1 YEAR AHEAD OF PLAN</span>
            </div>
            <p>
              Completing the Infinera integration by end-2026 consolidates optical silicon manufacturing and pulls forward €200M in annual run-rate cost synergies into early 2027.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. NVIDIA &amp; T-Mobile AI-RAN Commercial Validation</span>
              <span class="badge badge-bull">WORLD'S FIRST LIVE CALL</span>
            </div>
            <p>
              Nokia completed the world's first AI-RAN call in a live operator network with T-Mobile and NVIDIA, positioning its platform as the standard for 5G-Advanced and 6G.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Seasonal Q4 Net Sales Inflection (+20% to +24% QoQ Guide)</span>
              <span class="badge badge-bull">€6.2B–€6.4B Q4 SALES</span>
            </div>
            <p>
              Nokia guided to a strong 20%-24% sequential revenue jump in Q4, delivering full-year comparable operating profit above the €2.35B midpoint.
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
            Post-Print Consensus: Institutional Value Desks Accumulate on Clean Top-Line Beat &amp; Optical Guidance Lift
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            Nokia traded quietly at <strong>$7.91 (+0.38%)</strong> after hours (firmly inside the ±4.15% / ±$0.35 straddle band) as investors balanced a <strong>€5,154M net sales beat (+9% CC)</strong> and <strong>€605M comparable operating profit (+35% YoY)</strong> against the <strong>€400M working capital inventory commitment</strong>.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">AH Reaction: +0.38% ($7.91)</span>
          <span class="badge badge-bull">Comp Op Profit: +35% YoY</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #1: Retail &amp; Social Pulse <span class="badge badge-bull">REDDIT / X / FINTWIT</span></span>
            <span class="badge badge-bull">SCORE: 66 / 100 (BULLISH ACCUMULATION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 66%; background: var(--accent-blue);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Top Retail Catalyst</span>
              <span class="kpi-val" style="color:var(--bull-green);">Google €13B Deal</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">AI &amp; Cloud Sales</span>
              <span class="kpi-val">+123% YoY (€1.5B Orders)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">AH Support</span>
              <span class="kpi-val">Holding above $7.85</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            "FinTwit Telecom Tech Specialist: 'Nokia is morphing into an AI connectivity powerhouse under Justin Hotard. Net sales +9% CC, IP Networks +43% CC, AI/Cloud sales +123%, and Infinera synergies pulled forward 1 full year. The €400M inventory build is just fuel for the 2027 optical ramp.'"
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #2: Sell-Side Flash Note Reactions <span class="badge badge-bull">WALL STREET DESKS</span></span>
            <span class="badge badge-bull">SCORE: 70 / 100 (CONSTRUCTIVE)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 70%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Comp Op Profit Beat</span>
              <span class="kpi-val" style="color:var(--bull-green);">€605M vs €525M Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Network Infra Guide</span>
              <span class="kpi-val">Raised to 12%-14% CC</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Infinera Synergies</span>
              <span class="kpi-val">€200M 1 Year Ahead</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Goldman Sachs Flash Note: "Nokia delivered an impressive operational print with comparable operating profit beating consensus by 15% on strong optical operating leverage. While FCF conversion was lowered to 35%-55%, management clarified that working capital investments are tied to contractually secured 2027 AI hyperscaler orders."
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #3: Management Call Tone &amp; Candor <span class="badge badge-bull">TRANSCRIPT AUDIT</span></span>
            <span class="badge badge-bull">SCORE: 76 / 100 (HIGH CONVICTION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 76%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Operating Leverage</span>
              <span class="kpi-val">+220 bps YoY (11.7%)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">2027 Optical Guide</span>
              <span class="kpi-val">+25% to +30% Growth</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">FY26 Target Stance</span>
              <span class="kpi-val">Above €2.35B Midpoint</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            CEO Justin Hotard: "Team Nokia continues to deliver on our commitments. In Q3, we grew net sales by 9% CC and improved comparable operating margin by 220 basis points. In AI &amp; Cloud, net sales more than doubled and we secured EUR 1.5 billion in new orders. We are uniquely suited for AI infrastructure that is larger, more distributed and hyperconnected."
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #4: Options IV Crush &amp; Skew <span class="badge badge-neutral">DERIVATIVES DESK</span></span>
            <span class="badge badge-neutral">SCORE: 58 / 100 (VOLATILITY CRUSH)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 58%; background: var(--warn-amber);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Actual vs Implied Move</span>
              <span class="kpi-val">+0.38% vs ±4.15% Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Institutional Put Floor</span>
              <span class="kpi-val">$7.50 – $7.75 Support</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">30D IV Crush</span>
              <span class="kpi-val" style="color:var(--bull-green);">69.1% → ~32% IV</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            At $7.91 AH (+0.38% vs $7.88 close), Nokia experienced a total options volatility crush with implied volatility plummeting from 69% to ~32%, providing solid support above the $7.50 put floor.
          </div>
        </div>
      </div>

      <!-- AGENT 2C SOCIAL PULSE SUMMARY CARDS -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; margin-top: 16px;">
        <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #34d399; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #34d399; font-size: 13px; margin-bottom: 4px;">Retail &amp; Tech Community Reaction (Reddit &amp; X)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.45;">
            {soc_data["retail_vs_institutional_reaction"]["retail_sentiment_summary"]}
          </p>
        </div>
        <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #60a5fa; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #93c5fd; font-size: 13px; margin-bottom: 4px;">Institutional &amp; Sell-Side Desk Pulse (Goldman Sachs, UBS, JPMorgan)</div>
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
          <div class="card-subtitle">Post-call risk-reward setups anchored to the After-Hours Price (${ah_price:.2f}) and Reaffirmed FY26 Operating Profit Guidance</div>
        </div>
        <span class="badge badge-bull">POST-PRINT TACTICAL PLAYBOOK</span>
      </div>

      <div class="scenario-grid">
        <!-- BULL CASE -->
        <div class="scenario-card scenario-bull">
          <div class="scenario-title">
            <span style="color:var(--bull-green);">ACCUMULATE ON OPTICAL INFLECTION &amp; AI SUPERCYCLE (BULL CASE)</span>
            <span class="badge badge-bull">PROB: 55% | TARGET: $8.80–$9.50 (Anchored above ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>AI &amp; Cloud Network Re-Rating (+123% YoY):</strong> Hyperscaler capital expenditures accelerate into 800G/1.6T optical interconnects, confirming Nokia's <strong>25% to 30% Optical/IP growth outlook in 2027</strong>.</li>
            <li><strong>Infinera Synergies Delivered Early:</strong> Realizing €200M in net annual synergies by end of 2026 expands 2027 operating margins by 120-150 bps ahead of Street consensus.</li>
            <li><strong>Q4 Operating Profit Squeeze:</strong> Seasonal Q4 operating profit delivering above the €2.35B guidance midpoint triggers full-year consensus earnings upgrades across Wall Street.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure (Bull Target: $8.80):</strong>
            Accumulate shares at the T+1 open near $7.91 or initiate a <strong>Dec 18, 2026 $8.00 / $9.00 Bull Call Spread</strong> (financed by selling a $7.00 Put) to target multiple expansion toward $8.80.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">RANGE-BOUND CONSOLIDATION &amp; HARVEST THETA (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 35% | RANGE: $7.50–$8.30 (Around ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Working Capital Digestion:</strong> The market balances €605M comparable operating profit against negative €99M reported FCF as investors wait for inventory to convert into 2027 cash.</li>
            <li><strong>Mobile RAN Sluggishness:</strong> Sluggish European telecom RAN demand offsets hyperscaler optical strength, keeping full-year sales growth in the 2%-4% band.</li>
            <li><strong>Net Cash &amp; Dividend Floor:</strong> €2,584M net cash surplus and €0.03 quarterly dividend (2.2% yield) provide rigid downside support at $7.50.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure:</strong>
            Deploy a <strong>Nov 20, 2026 Cash-Secured Put Write at $7.50</strong> or an <strong>$8.00 Covered Call overwrite</strong> to harvest post-earnings volatility crush and capture dividend cash.
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">WORKING CAPITAL CASH DRAG &amp; TELCO DE-RATING (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 10% | TARGET: $6.80–$7.20 (Anchored below ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Persistent Working Capital Cash Burn:</strong> Further supply chain delays prevent the €400M working capital inventory from converting to cash, extending negative FCF into Q4.</li>
            <li><strong>Hyperscaler Delivery Postponements:</strong> Macro or cloud capex pauses delay 2027 optical interconnect installations, jeopardizing the 25%-30% growth target.</li>
            <li><strong>Technical Breakdown Below $7.50:</strong> Heavy institutional profit-taking breaks the $7.50 key support level, triggering systematic selling toward $6.80.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure (Bear Target: $6.80):</strong>
            Initiate a <strong>Nov 20, 2026 $7.50 / $6.50 Bear Put Spread</strong> only if NOK breaks decisively below $7.50 on heavy volume.
          </div>
        </div>
      </div>
    </section>

    <!-- VERBATIM GROUND-TRUTH GROUNDING LEDGER -->
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 10px 14px; font-size: 12px; color: var(--text-muted); margin-top: 10px; margin-bottom: 14px;">
      <strong>Deterministic Grounding Verification:</strong> Regular Close Price: <span class="mono" style="color:#f8fafc;">${reg_price:.2f}</span> • After-Hours Price: <span class="mono" style="color:#34d399;">${ah_price:.2f}</span> • Reported Q3 2026 Net Sales: <span class="mono" style="color:#60a5fa;">5,154M</span> (€5,154M EUR) • Reported Q3 2026 Operating Cash Flow (OCF): <span class="mono" style="color:#34d399;">95M</span> (€95M EUR) • Standard Reported FCF: <span class="mono" style="color:#fcd34d;">-€{abs(q0_rep_fcf):,.0f}M</span> • Forensic True Free Cash Flow: <span class="mono" style="color:#fcd34d;">-€{abs(q0_true_fcf):,.0f}M</span> • Post-Print Move: <span class="mono" style="color:#34d399;">{post_move_pct:+.2f}%</span> vs Expected <span class="mono">±{opt_implied_pct:.2f}%</span>.
    </div>

    <!-- 10. FOOTER -->
    <div class="footer-meta">
      <div>
        <span>SEC EDGAR CIK: <strong>0000924621</strong></span> • 
        <span>Q3 2026 Form 6-K Filed: <strong>Thursday, Oct 22, 2026 (Interim Report Attachment)</strong></span> • 
        <span>Reporting Currency: <strong>EUR (€ Millions) / USD ($) ADR</strong></span>
      </div>
      <div style="margin-top:6px;">
        Deterministic Post-Earnings Ground Truth Anchored via SEC Form 6-K &amp; 20-F Filings • Generated with Antigravity Zero-Hallucination T+0 Post-Earnings Harness
      </div>
    </div>
"""

draft_payload = {
    "header": {
        "page_title": f"NOK (${ah_price:.2f}) Q3 2026 Post-Earnings Forensic & Sentiment Tearsheet",
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
        "bull_target_low_num": bull_target,
        "bear_target_high_num": bear_target
    },
    "rendered_container_html": container_html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"[SUCCESS] Generated Post-Earnings Draft for NOK at: {DRAFT_PATH.name}")
print(f"  - Inner HTML Character Count: {len(container_html):,}")
print(f"  - Interactive Tooltip Count (.tip): {container_html.count('class=\"tip')}")
print(f"  - Data-Tip Count (data-tip=): {container_html.count('data-tip=\"')}")
