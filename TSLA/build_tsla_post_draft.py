"""
TSLA Dedicated Post-Earnings Draft Builder (Track A + Track B Complete Re-Synthesis)
Builds drafts/TSLA_2026-10-21_post_draft.json with 100% Q3 2026 (Actual) rolled 5-quarter tables,
Q4 2026E forward guidance columns, zero T-1 bleed-through, and Track B interactive enhancements.
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "TSLA_2026-10-21_post_truth.json"
BUS_2A_PATH = BASE_DIR / "post_agent_bus" / "TSLA_2026-10-21_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "post_agent_bus" / "TSLA_2026-10-21_agent2b_transcript.json"
BUS_2C_PATH = BASE_DIR / "post_agent_bus" / "TSLA_2026-10-21_agent2c_social.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "TSLA_2026-10-21_post_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
kpis_data = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
trans_data = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
soc_data = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

reg_price = truth["post_print_reaction"]["regular_close_price"]      # 386.47
ah_price = truth["post_print_reaction"]["after_hours_price"]         # 373.63
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]  # -3.32
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] # 2.99
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 11.53)
verdict = truth["post_print_reaction"]["overall_print_verdict"]      # CLEAN BEAT & RAISE

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]  # 28046.0
cons_rev = truth["t1_baseline"]["consensus_revenue_millions"]                 # 27850.0
whisper_rev = truth["t1_baseline"]["whisper_revenue_millions"]                # 28400.0
q0_gaap_eps = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"]     # 0.22
q0_adj_eps = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"]   # 0.48
cons_eps = truth["t1_baseline"]["consensus_eps_nongaap"]                      # 0.45

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # 6263.0
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 4732.0
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # 1531.0
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 1165.0
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 26.0
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # 340.0

s5q = truth["stitched_5q_chronological"]

container_html = f"""
    <!-- 1. HEADER BANNER (T+0 POST-EARNINGS FORENSIC TEARSHEET) -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#34d399;">Newly Reported Quarter: <strong>Q3 2026 (Ended Sep 30, 2026)</strong> • Forward Guidance Horizon: <strong>Q4 2026 &amp; FY2027</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">TSLA</span>
            <h1 class="company-name">Tesla, Inc.</h1>
            <span class="badge badge-bull">{verdict}</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="Immediate post-earnings release forensic analysis." data-tip="T+0 Post-Print: Forensic analysis synthesized immediately following the official Q3 2026 SEC Form 8-K Shareholder Update and earnings conference call.">T+0</span> POST-EARNINGS FORENSIC TEARSHEET</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select • Electric Vehicles, Super Intelligence (SI), Cybercab Robotaxi, Optimus Robotics &amp; Megapack Energy Storage • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): 0001318605 assigned by the U.S. Securities and Exchange Commission (SEC) to Tesla, Inc.">CIK</span>: 0001318605</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Regular Close / <span style="color:#f87171;">After-Hours Price</span></div>
            <div class="price-value">${reg_price:.2f} / <span style="color:#f87171;">${ah_price:.2f}</span> <span style="font-size:14px; color:#f87171;">({post_move_pct:+.2f}%)</span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total equity value at $373.63 after-hours price across 3,541M diluted shares." data-tip="Market Capitalization: Post-print equity value (~$1.32T diluted / $1.53T portal valuation) vs $1.50T Enterprise Value reflecting $45.45B cash minus $9.52B debt.">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Debt ($9.52B) minus Cash &amp; Investments ($45.45B)." data-tip="Enterprise Value (EV): Reflects Tesla's -$35.92B net cash fortress ($45,447M cash &amp; short-term investments vs $9,523M total debt &amp; finance leases).">EV</span></div>
            <div class="price-value">$1.53T / $1.50T</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Q3 2026 SEC Form 8-K Filed</span>
          <span class="strip-val" style="color: var(--bull-green);">Wed, Oct 21, 2026 • <span class="tip" title="After Market Close: Official Q3 2026 Shareholder Deck filed via SEC Form 8-K Item 2.02." data-tip="Form 8-K Item 2.02 &amp; Exhibit 99.1 filed October 21, 2026 after market close; Webcast hosted at 4:30 PM CT / 5:30 PM ET.">8-K Verified</span></span>
          <span class="kpi-sub">Exhibit 99.1 &amp; Earnings Call Transcript Audited</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="Actual post-market stock reaction (-3.32%) compared against pre-print options straddle implied move (±2.99%)." data-tip="Actual vs. Implied Move: TSLA traded down -3.32% (-$12.84/sh to $373.63) in after-hours action, slightly exceeding the ±2.99% (±$11.53/sh) ATM weekly straddle band on whisper revenue digestion and $4.73B AI CapEx.">Actual AH Move vs. Implied</span></span>
          <span class="strip-val" style="color: var(--warn-amber);">{post_move_pct:+.2f}% (vs ±{opt_implied_pct:.2f}% Est)</span>
          <span class="kpi-sub">-${reg_price - ah_price:.2f}/sh Actual vs ±${opt_straddle:.2f}/sh <span class="tip" title="At-The-Money weekly straddle price prior to earnings." data-tip="ATM Straddle: Pre-earnings weekly option straddle priced at ±$11.53/sh (2.99% implied move).">ATM Straddle</span></span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 GAAP Revenue ($28,046M) vs Wall Street Consensus ($27,850M) and Whisper ($28,400M)." data-tip="Q3 2026 Revenue Beat: Reported $28,046M, beating Street consensus of $27,850M by +$196M (+0.70%) while modestly below elevated $28,400M buy-side whisper.">Revenue vs. Street</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$28.05B <span style="font-size:12px;">(+$196M Beat)</span></span>
          <span class="kpi-sub">Street Est: $27.85B | Whisper: $28.40B | 486,532 Deliveries</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 Non-GAAP Diluted EPS ($0.48) and GAAP Diluted EPS ($0.22) vs Consensus ($0.45)." data-tip="Q3 2026 EPS Beat: Reported $0.48 Non-GAAP Diluted EPS (+45.5% QoQ), beating $0.45 Street consensus by +$0.03 (+6.67%), alongside $0.22 GAAP Diluted EPS.">EPS (Non-GAAP / GAAP)</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$0.48 Adj / $0.22 <span class="tip" title="Generally Accepted Accounting Principles Diluted EPS ($0.22 on $787M GAAP Net Income)." data-tip="GAAP Diluted EPS ($0.22) reflects $1,165M in Stock-Based Compensation ($0.28/sh net of tax) including the 2025 CEO Performance Award.">GAAP</span></span>
          <span class="kpi-sub">Beat $0.45 Consensus (+6.7%) | Auto GM ex-Credits: 18.1%</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 Operational <span class="tip tip-right" title="Major operational milestones verified in the Q3 2026 Shareholder Deck." data-tip="Q3 Milestones: Cybercab launched in Austin Robotaxi fleet (8x QoQ unsupervised miles to ~2M), Semi volume production started in Nevada, Optimus production started in Fremont, and Megafactory Texas (50 GWh) began production.">Milestones &amp; Outlook</span></span>
          <span class="strip-val" style="color: var(--bull-green);">Cybercab + Semi + Optimus Live</span>
          <span class="kpi-sub">1.74M FSD Subs (+67% YoY) | 400 MW SI Compute Target</span>
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
      <a href="TSLA_T1_2026-10-21.html" style="font-size: 11.5px; font-weight: 700; color: #93c5fd; text-decoration: none; padding: 5px 12px; border-radius: 6px; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.45); display: flex; align-items: center; gap: 6px;">
        ⇄ Compare Paired T-1 Pre-Earnings Briefing
      </a>
    </nav>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS — ALL ROLLED FORWARD TO Q3 2026 ACTUALS) -->
    <section class="kpi-grid" id="row-1-kpis">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Intensity (Q3 2026 Actual)</div>
          <span class="badge badge-bull">+$1.53B FCF SNAPBACK</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual cash generated from operations in Q3 2026 ($6,263M)." data-tip="Operating Cash Flow (OCF): Surged +33.34% QoQ to $6,263M in Q3 2026 (from $4,697M in Q2 2026), aided by +$1,255M FSD deferred revenue inflows and working capital discipline.">Operating Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">TTM Operating Cash Flow: $18,710M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$6,263M</span>
              <div class="delta-pair">
                <span class="badge badge-bull"><span class="tip" title="Sequential change from Q2 2026 ($4,697M) to Q3 2026 ($6,263M)." data-tip="QoQ OCF Delta: Surged +33.34% sequentially from $4,697M in Q2 2026.">QoQ</span> +33.34%</span>
                <span class="badge badge-bull"><span class="tip" title="Year-over-Year change from Q3 2025 ($6,238M) to Q3 2026 ($6,263M)." data-tip="YoY OCF Delta: Up +0.40% vs Q3 2025 ($6,238M).">YoY</span> +0.40%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures in Q3 2026 ($4,732M) for Cortex 1/2 SI compute, Megafactory Texas, Semi, and Austin Fab." data-tip="Capital Expenditures (CapEx): $4,732M in Q3 2026 (-18.26% QoQ vs Q2's peak $5,789M, +110.50% YoY) as Tesla scales SI training compute toward 400 MW.">Capital Expenditures</span> (Q3 2026)</span>
              <span class="kpi-sub">CapEx Intensity: 16.87% of Revenue ($15,407M TTM)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">($4,732M)</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ -18.26%</span>
                <span class="badge badge-warn">YoY +110.50%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: OCF ($6,263M) minus CapEx ($4,732M) = +$1,531M." data-tip="Reported Free Cash Flow: Snapped back by +$2,623M sequentially from -$1,092M in Q2 2026 to +$1,531M in Q3 2026.">Reported Free Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">Rebounded +$2,623M Sequentially from -$1,092M in Q2</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,531M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +$2.62B</span>
                <span class="badge badge-warn">YoY -61.63%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forensic True Free Cash Flow: OCF ($6,263M) - CapEx ($4,732M) - SBC ($1,165M) - Finance Leases ($26M) = +$340M." data-tip="True Free Cash Flow: Turned positive at +$340M in Q3 2026 (vs -$2,262M in Q2 2026) even after deducting $1,165M in non-cash SBC and $26M in finance leases.">True FCF (ex-SBC &amp; Leases)</span> (Q3 2026)</span>
              <span class="kpi-sub">Q3 SBC: $1,165M (incl. CEO Award) | Leases: $26M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$340M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +$2.60B</span>
                <span class="badge badge-warn">YoY -89.72%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING MARGINS (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Margins (Q3 2026 Actual)</div>
          <span class="badge badge-bull">19.59% GROSS MARGIN (+276 BPS QOQ)</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Gross Profit: Q3 2026 Revenue ($28,046M) minus Cost of Revenues ($22,552M) = $5,494M." data-tip="Gross Profit: Jumped +15.64% QoQ and +8.71% YoY to $5,494M (19.59% GAAP Gross Margin; Auto GM ex-credits expanded to 18.1%).">Gross Profit</span> (Q3 2026)</span>
              <span class="kpi-sub">GAAP Gross Margin: 19.59% | Auto GM ex-Credits: 18.1%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$5,494M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +15.64%</span>
                <span class="badge badge-bull">YoY +8.71%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Income from Operations ($718M) in Q3 2026, up +80.40% sequentially from $398M in Q2 2026." data-tip="Operating Income (EBIT): Surged +80.40% QoQ from $398M in Q2 2026 to $718M in Q3 2026 (2.56% GAAP operating margin; Adjusted EBITDA $3,900M / 13.9% margin).">Operating Income (EBIT)</span> (Q3 2026)</span>
              <span class="kpi-sub">GAAP Op Margin: 2.56% | Adjusted EBITDA: $3,900M (13.9%)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$718M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +80.40%</span>
                <span class="badge badge-warn">YoY -55.79%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research &amp; Development Expenses in Q3 2026 ($2,761M)." data-tip="R&amp;D Investment: Reached a record $2,761M in Q3 2026 (+16.45% QoQ, +69.39% YoY) to fund Super Intelligence (SI), Cybercab, Optimus, and Next Gen Roadster.">R&amp;D Reinvestment</span> (Q3 2026)</span>
              <span class="kpi-sub">R&amp;D Intensity: 9.84% of Rev | SI Compute: &gt;225 MW Live</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$2,761M</span>
              <div class="delta-pair">
                <span class="badge badge-warn">QoQ +16.45%</span>
                <span class="badge badge-warn">YoY +69.39%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Non-GAAP Net Income ($1,697M, or $0.48/sh diluted) and GAAP Net Income ($787M, or $0.22/sh diluted)." data-tip="Net Income &amp; EPS: Non-GAAP Net Income rose +47.18% QoQ to $1,697M ($0.48 Diluted EPS vs $0.45 consensus); GAAP Net Income was $787M ($0.22 Diluted EPS).">Net Income &amp; EPS</span> (Q3 2026)</span>
              <span class="kpi-sub">Non-GAAP EPS: $0.48 (+45.5% QoQ) | GAAP EPS: $0.22</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,697M Adj</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Adj EPS: $0.48</span>
                <span class="badge badge-neutral">GAAP: $787M</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS & LIQUIDITY (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Debt Profile (Q3 2026)</div>
          <span class="badge badge-bull">$45.45B CASH FORTRESS</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Cash, cash equivalents and short-term investments as of September 30, 2026 ($45,447M)." data-tip="Liquid Reserves: Expanded by +$1,923M sequentially to an all-time record $45,447M (+4.42% QoQ, +9.12% YoY).">Cash &amp; Short-Term Investments</span> (Q3 2026)</span>
              <span class="kpi-sub">Increased +$1.92B Sequentially on Positive Q3 FCF</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$45,447M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +4.42%</span>
                <span class="badge badge-bull">YoY +9.12%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Current debt &amp; finance leases ($1,387M) plus non-current debt &amp; finance leases ($8,136M) = $9,523M." data-tip="Total Debt &amp; Finance Leases: $9,523M ($9,265M non-recourse project/auto debt and just $2M recourse debt).">Total Debt &amp; Finance Leases</span> (Q3 2026)</span>
              <span class="kpi-sub">Recourse Corporate Debt: Only $2M | Non-Recourse: $9,265M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$9,523M</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +1.94%</span>
                <span class="badge badge-warn">YoY +23.64%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Debt ($9,523M) minus Cash &amp; Short-Term Investments ($45,447M) = -$35,924M Net Cash." data-tip="Net Cash Position: Massive -$35,924M net debt (i.e. +$35.92B net cash surplus), self-funding the 2026-2027 SI compute and Austin Fab buildout.">Net Cash Position</span> (Q3 2026)</span>
              <span class="kpi-sub">+$35.92B Net Cash Surplus Over All Debt</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">-$35,924M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">+$1.74B QoQ</span>
                <span class="badge badge-bull">Zero Net Leverage</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Stockholders' Equity ($89,289M) and Total Deferred Revenue ($8,787M across current &amp; non-current)." data-tip="Stockholders' Equity &amp; Deferred FSD Pool: Equity reached $89,289M (+11.65% YoY), while total deferred revenue jumped +$1.29B QoQ to $8,787M on FSD subscriptions.">Stockholders' Equity &amp; Deferred Rev</span></span>
              <span class="kpi-sub">Total Deferred Revenue Pool: $8,787M (+$1,255M Q3 CF Inflow)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$89,289M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +2.80%</span>
                <span class="badge badge-bull">YoY +11.65%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT MIX & AUTONOMY KPIs (Q3 2026 ACTUAL) -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Mix &amp; Autonomy KPIs (Q3 2026)</div>
          <span class="badge badge-blue">CYBERCAB LIVE IN AUSTIN</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Automotive Revenue ($20,560M) and Vehicle Deliveries (486,532 units) in Q3 2026." data-tip="Automotive Segment: $20,560M (73.31% of revenue), with 486,532 deliveries (beat 482k consensus), 10Mth cumulative vehicle delivered, and 4-year high order backlog.">Automotive Share &amp; Deliveries</span> (Q3 2026)</span>
              <span class="kpi-sub">Rev: $20,560M | Deliveries: 486,532 | Inventory: 11 Days</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">73.31%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Auto GM: 18.5%</span>
                <span class="badge badge-bull">Ex-Credits: 18.1%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Energy Generation &amp; Storage Q3 2026 Revenue ($2,881M) and Deployment (13.7 GWh)." data-tip="Energy Generation &amp; Storage: Deployed a record 13.7 GWh (+9.6% YoY), generating $2,881M revenue and $954M gross profit (33.11% segment GM) as Megafactory Texas started production.">Energy Storage &amp; Margin</span> (Q3 2026)</span>
              <span class="kpi-sub">Rev: $2,881M | Deployed: 13.7 GWh | Segment GM: 33.11%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">10.27% / 13.7 GWh</span>
              <div class="delta-pair">
                <span class="badge badge-bull">GM: 33.11%</span>
                <span class="badge badge-bull">TX Megafactory Live</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Services &amp; Other Q3 2026 Revenue ($4,605M, +32.52% YoY) and Record Gross Profit ($734M)." data-tip="Services &amp; Other: Surged +32.52% YoY to $4,605M (16.42% of total revenue) with a record $734M gross profit (15.94% GM) across 84,465 Supercharger connectors.">Services &amp; Other Flywheel</span> (Q3 2026)</span>
              <span class="kpi-sub">Rev: $4,605M (+32.5% YoY) | Record Gross Profit: $734M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">16.42% / $4.61B</span>
              <div class="delta-pair">
                <span class="badge badge-bull">YoY +32.52%</span>
                <span class="badge badge-bull">GM: 15.94%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Active FSD Subscriptions (1.74M) and Cumulative Unsupervised Robotaxi Miles (~2M)." data-tip="FSD &amp; Robotaxi Scale: 1.74M active FSD paying subscribers (+67.3% YoY), 9 EU countries approved, and Cybercab launched in Austin Robotaxi fleet on Sep 3 (8x QoQ unsupervised miles).">Active FSD Subs &amp; Robotaxi</span> (Q3 2026)</span>
              <span class="kpi-sub">FSD Subs: 1.74M (+67% YoY) | Unsupervised Miles: 8x QoQ</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">1.74M Subs</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +17.57%</span>
                <span class="badge badge-bull">9 EU Markets</span>
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
            Source: Tesla SEC Form 8-K (Item 2.02, Exhibit 99.1) Filed Oct 21, 2026 • Q3 2026 Shareholder Update • Wall Street Consensus Comparison
          </div>
        </div>
        <div style="display:flex; gap: 8px; align-items:center;">
          <span class="badge badge-bull">AUTO GM EX-CREDITS 18.1% BEAT + $1.53B FCF SNAPBACK</span>
          <span class="badge badge-blue">T+0 POST-PRINT</span>
        </div>
      </div>

      <!-- TRACK B: T-1 PRE-PRINT THESIS VS. T+0 POST-PRINT REALITY AUDIT BANNER -->
      <div class="t1-vs-t0-audit" style="background: linear-gradient(90deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(59, 130, 246, 0.35); border-left: 4px solid #34d399; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
          <span style="font-weight: 800; font-size: 13px; color: #34d399; text-transform: uppercase; letter-spacing: 0.05em;">🔍 T-1 Pre-Earnings Thesis vs. T+0 Post-Print Reality Audit</span>
          <a href="TSLA_T1_2026-10-21.html" style="font-size: 11.5px; color: #93c5fd; text-decoration: underline;">Open Original T-1 Briefing →</a>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; font-size: 12.3px; color: var(--text-secondary);">
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #93c5fd;">Auto Margin Inflection Thesis:</strong><br>
            • <em>T-1 Forecast:</em> Street modeled 16.5% Auto GM ex-credits; Whisper was 17.2%.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">SHATTERED EXPECTATIONS</strong> — Auto GM ex-credits jumped +180 bps QoQ to <strong>18.1%</strong> (19.59% consolidated GM) despite credits dropping to $113M.
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #fcd34d;">FCF &amp; CapEx Intensity Thesis:</strong><br>
            • <em>T-1 Forecast:</em> Flagged Q2's -$1,092M FCF deficit from $5.79B AI CapEx.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">+$2.62B FCF REVERSAL</strong> — OCF surged to <strong>$6,263M</strong> against $4,732M CapEx, flipping Reported FCF to <strong>+$1,531M</strong> and True FCF to <strong>+$340M</strong>.
          </div>
          <div style="background: rgba(11, 15, 25, 0.55); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
            <strong style="color: #34d399;">Autonomy &amp; Physical AI Catalysts:</strong><br>
            • <em>T-1 Forecast:</em> Focused on Austin Cybercab launch, Semi, and Optimus timelines.<br>
            • <em>T+0 Reality:</em> <strong style="color:#34d399;">CONFIRMED LIVE</strong> — Cybercab deployed Sep 3 in Austin (8x QoQ miles), Semi &amp; Optimus lines started production, and FSD hit <strong>1.74M subs</strong>.
          </div>
        </div>
      </div>

      <!-- TABLE 1B-1: HEADLINE & COMPANY-SPECIFIC KPI BEAT / MISS SCORECARD -->
      <div style="margin-bottom: 20px;">
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-1: Headline &amp; Company-Specific KPI Beat / Miss Scorecard (Q3 2026 Actuals)</span>
          <span class="tip" title="Deterministic comparison of reported Q3 2026 actuals against Street pre-print consensus and T-1 whisper." data-tip="Beat / Miss Scorecard: Evaluates Q3 2026 delivery across headline GAAP/Non-GAAP metrics and Tesla-specific operational KPIs with visual magnitude bars.">[Methodology]</span>
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
                <td><span class="tip" title="Total top-line revenue recognized across Automotive ($20,560M), Energy ($2,881M), and Services ($4,605M)." data-tip="Total Revenue ($M): Q3 2026 printed at $28,046M, beating Street consensus of $27,850M by +$196M (+0.70%).">Total Revenue ($M)</span></td>
                <td>$27,850M</td>
                <td>$28,400M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$28,046M</td>
                <td>
                  <span class="badge badge-bull">+$196M (+0.70%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:65%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-warn">-$354M (-1.25%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Non-GAAP Diluted EPS ($0.48) vs Street Consensus ($0.45); GAAP Diluted EPS printed at $0.22." data-tip="Non-GAAP Diluted EPS: Jumped +45.45% QoQ from $0.33 to $0.48, beating Street consensus ($0.45) by +$0.03 (+6.67%).">Non-GAAP Diluted EPS (GAAP: $0.22)</span></td>
                <td>$0.45</td>
                <td>$0.47</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">$0.48 <span style="font-size:11px; color:var(--text-muted);">($0.22 GAAP)</span></td>
                <td>
                  <span class="badge badge-bull">+$0.03 (+6.67%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:82%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+$0.01 (+2.13%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Non-GAAP Automotive Gross Margin excluding regulatory credit sales (18.1% in Q3 2026 vs 16.3% in Q2 2026)." data-tip="Automotive Gross Margin (ex-Regulatory Credits): Expanded +180 bps QoQ and +270 bps YoY to 18.1% (GAAP Auto GM: 18.5%).">Automotive Gross Margin (ex-Credits)</span></td>
                <td>16.50%</td>
                <td>17.20%</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">18.10% <span style="font-size:11px; color:var(--text-muted);">(18.5% GAAP)</span></td>
                <td>
                  <span class="badge badge-bull">+160 bps</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:90%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+90 bps</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Consolidated GAAP Gross Margin ($5,494M Gross Profit / $28,046M Revenue = 19.59%)." data-tip="Consolidated GAAP Gross Margin: Expanded +276 bps QoQ from 16.83% in Q2 2026 to 19.59% in Q3 2026 (+160 bps YoY).">Consolidated GAAP Gross Margin (%)</span></td>
                <td>18.10%</td>
                <td>18.60%</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">19.59% ($5,494M)</td>
                <td>
                  <span class="badge badge-bull">+149 bps</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:88%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+99 bps</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Total Passenger Vehicle Deliveries in Q3 2026 (478,237 Model 3/Y + 8,295 Other Models)." data-tip="Total Vehicle Deliveries: 486,532 units delivered in Q3 2026 (+1.33% QoQ), with global inventory tightening to just 11 days of supply.">Total Vehicle Deliveries (Units)</span></td>
                <td>482,000</td>
                <td>485,000</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">486,532</td>
                <td>
                  <span class="badge badge-bull">+4,532 (+0.94%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:72%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+1,532 (+0.32%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Utility-scale Megapack and residential Powerwall storage deployed in Q3 2026 (13.7 GWh)." data-tip="Energy Storage Deployed: Reached 13.7 GWh (+9.6% YoY) as Megafactory Texas (50 GWh capacity) began production.">Energy Storage Deployment (GWh)</span></td>
                <td>12.8 GWh</td>
                <td>13.5 GWh</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">13.7 GWh</td>
                <td>
                  <span class="badge badge-bull">+0.90 GWh (+7.03%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:84%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+0.20 GWh (+1.48%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Active Full Self-Driving paying subscribers &amp; upfront buyers (excluding free trials)." data-tip="Active FSD Subscriptions: Surged +17.57% QoQ and +67.31% YoY to 1.74 million subscribers.">Active FSD Subscriptions (Millions)</span></td>
                <td>1.55M</td>
                <td>1.65M</td>
                <td class="col-q0" style="font-weight:700; color: #34d399;">1.74M</td>
                <td>
                  <span class="badge badge-bull">+0.19M (+12.26%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:92%; height:100%; background:#10b981;"></div></div>
                </td>
                <td><span class="badge badge-bull">+0.09M (+5.45%)</span></td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Zero-emission regulatory credit revenue in Q3 2026 ($113M)." data-tip="Regulatory Credit Revenue: Dropped to $113M (vs $146M in Q2 2026 and $417M in Q3 2025), proving the Q3 gross margin beat was 100% organic.">Automotive Regulatory Credits ($M)</span></td>
                <td>$250M</td>
                <td>$200M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$113M</td>
                <td>
                  <span class="badge badge-blue">-$137M (High-Quality GM Beat)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div style="width:45%; height:100%; background:#3b82f6;"></div></div>
                </td>
                <td><span class="badge badge-blue">-$87M</span></td>
                <td><span class="badge badge-blue">HIGH-QUALITY MISS</span></td>
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
              <div style="width: 89%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <strong style="color: #34d399;">89 / 100 (Strong)</strong>
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
                <td><span class="tip" title="Austin Unsupervised Robotaxi &amp; Cybercab Fleet Launch." data-tip="Cybercab Launch: Guided for Q3 commercial fleet entry; launched September 3 in Austin with 8x QoQ unsupervised miles.">Cybercab Austin Robotaxi Deployment</span></td>
                <td>Deploy Cybercab into Austin commercial Robotaxi fleet in Q3</td>
                <td style="font-weight:600; color: #34d399;">Launched Sep 3 in Austin; ~2M unsupervised miles (8x QoQ)</td>
                <td>Delivered commercial Cybercab rides on schedule with 6am–midnight operating hours and Grok voice integration.</td>
                <td><span class="badge badge-bull">DELIVERED ON TIME</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Tesla Semi &amp; Optimus High-Volume Line Start of Production." data-tip="Semi &amp; Optimus Production: Both Nevada Semi high-volume line and Fremont Optimus production lines started in Q3 2026.">Tesla Semi &amp; Optimus Production Start</span></td>
                <td>Begin volume production preparation in 2H 2026</td>
                <td style="font-weight:600; color: #34d399;">Volume production started for Semi (NV) &amp; Optimus (Fremont)</td>
                <td>Semi achieved 500-mile range at 82,000 lbs GCW (1.7 kWh/mile); Fremont line produced first commercial-process Optimus bots.</td>
                <td><span class="badge badge-bull">BEAT OWN GUIDE</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Megafactory Texas (50 GWh) &amp; Domestic LFP Cell Localization." data-tip="Megafactory Texas: Began production in Q3 2026 alongside first Megapacks built with Nevada LFP cells.">Megafactory Texas &amp; Nevada LFP Cells</span></td>
                <td>Ramp Megafactory Texas &amp; localize U.S. LFP supply</td>
                <td style="font-weight:600; color: #34d399;">Megafactory Texas live; 1st Nevada LFP Megapacks shipped</td>
                <td>13.7 GWh deployed in Q3 alongside record order rate and backlog driven by AI data center grid demand.</td>
                <td><span class="badge badge-bull">DELIVERED ON TIME</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Balance Sheet Liquidity &amp; Free Cash Flow Self-Funding." data-tip="Cash &amp; FCF: Rebounded from -$1.09B FCF in Q2 to +$1.53B FCF in Q3, lifting cash by +$1.92B to $45.45B.">Free Cash Flow &amp; Liquidity Preservation</span></td>
                <td>Maintain strong balance sheet liquidity during AI CapEx ramp</td>
                <td style="font-weight:600; color: #34d399;">+$1,531M FCF; Cash rose +$1.92B to $45,447M</td>
                <td>Generated $6,263M OCF, self-funding $4,732M of CapEx while expanding cash &amp; investments to a record $45.45B.</td>
                <td><span class="badge badge-bull">BEAT OWN GUIDE</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-3: FORWARD GUIDANCE RESET -->
      <div>
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          <span>Table 1B-3: Forward Guidance Reset (New Q4 2026 &amp; FY2027 Outlook vs. Pre-Print Street Expectations)</span>
          <span class="tip" title="Evaluates how new forward guidance changes future earnings power relative to Wall Street consensus." data-tip="Forward Guidance Reset: Audits Q4 2026 capacity utilization, 400 MW SI compute target, Austin semiconductor fab commissioning (2027), and software/fleet profit acceleration.">[Re-Rating Matrix]</span>
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
                <td><span class="tip" title="Q4 2026 Passenger Vehicle Volume &amp; Backlog." data-tip="Vehicle Backlog &amp; Utilization: Entered Q4 with the largest passenger vehicle backlog in 4 years and 11 days inventory.">Q4 2026 Vehicle Deliveries &amp; Backlog</span></td>
                <td>~495,000 Q4 Deliveries</td>
                <td style="font-weight:600; color: #34d399;">4-Year High Vehicle Backlog; Max Factory Utilization (~510k Est)</td>
                <td>+15,000 units upside vs Street; North America FSD take-rate +20 pts QoQ</td>
                <td><span class="badge badge-bull">RAISED</span></td>
                <td>FSD (Supervised) adoption in North America and 9 EU markets is driving record order intake while battery supply constraints ease.</td>
              </tr>
              <tr>
                <td><span class="tip" title="Super Intelligence (SI) Training Compute Capacity by Year-End 2026." data-tip="SI Compute Target: Reaching 400 MW of SI training compute by end of 2026 (Cortex 1 >105 MW + Cortex 2 >120 MW live).">Year-End 2026 SI Training Compute</span></td>
                <td>~300 MW SI Training Compute</td>
                <td style="font-weight:600; color: #34d399;">400 MW of SI Training Compute by Year-End 2026</td>
                <td>+100 MW (+33%) above Street infrastructure models</td>
                <td><span class="badge badge-bull">ACCELERATED</span></td>
                <td>Powers dual autonomy foundation models for unsupervised Robotaxi fleet orchestration and commercial Optimus humanoid bots.</td>
              </tr>
              <tr>
                <td><span class="tip" title="Austin Semiconductor Fab Equipment Commissioning." data-tip="Austin Fab: Construction underway with equipment commissioning slated for 2027.">Austin Semiconductor Fab &amp; Vertical Integration</span></td>
                <td>External foundry reliance</td>
                <td style="font-weight:600; color: #60a5fa;">Austin Fab Equipment Commissioning in 2027</td>
                <td>New multi-year silicon sovereignty milestone</td>
                <td><span class="badge badge-blue">NEW CATALYST</span></td>
                <td>Secures custom AI inference silicon supply alongside Texas 4680 (&gt;40 GWh), lithium refining (30 GWh), and cathode production (10 GWh).</td>
              </tr>
              <tr>
                <td><span class="tip" title="Hardware + SI, Software &amp; Fleet Profit Trajectory." data-tip="Profit Mix Shift: Hardware profits increasingly accompanied by SI, FSD software, and Robotaxi fleet profits.">SI, Software &amp; Fleet Profit Contribution</span></td>
                <td>Auto hardware margin compression fears</td>
                <td style="font-weight:600; color: #34d399;">Hardware Profits + Accelerating SI, Software &amp; Fleet Profits</td>
                <td>1.74M FSD subs + $8.79B deferred revenue pool</td>
                <td><span class="badge badge-bull">REITERATED &amp; VALIDATED</span></td>
                <td>High-margin FSD software, Services ($734M Q3 GP), and Megapack (33.1% GM) structurally lift consolidated gross margins toward 20%+.</td>
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
              <td><span class="tip" title="Total Revenue: Consolidated GAAP revenue across Automotive, Energy, and Services ($28,046M in Q3 2026)." data-tip="Total Revenue ($M): Printed at $28,046M in Q3 2026 (-0.67% QoQ, -0.17% YoY), achieving second consecutive quarter of TTM revenue >$100B; Q4 2026E modeled at $30,200M.">Total Revenue ($M)</span></td>
              <td>$28,095</td>
              <td>$24,901</td>
              <td>$22,387</td>
              <td>$28,236</td>
              <td class="col-q0" style="color: var(--accent-blue);">$28,046</td>
              <td><span class="badge badge-neutral">-0.67%</span></td>
              <td><span class="badge badge-neutral">-0.17%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$30,200</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Total Automotive Revenue: Automotive sales ($20,094M) + regulatory credits ($113M) + leasing ($353M) = $20,560M." data-tip="Total Automotive Revenue ($M): $20,560M in Q3 2026 (+0.21% QoQ, -3.04% YoY).">Automotive Revenues ($M)</span></td>
              <td>$21,205</td>
              <td>$17,693</td>
              <td>$16,234</td>
              <td>$20,516</td>
              <td class="col-q0">$20,560</td>
              <td><span class="badge badge-bull">+0.21%</span></td>
              <td><span class="badge badge-neutral">-3.04%</span></td>
              <td class="col-est">$21,600</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Energy Generation and Storage Revenue ($2,881M in Q3 2026 on 13.7 GWh deployed)." data-tip="Energy Generation &amp; Storage ($M): $2,881M in Q3 2026 (-8.22% QoQ, -15.64% YoY due to tariff-related customer refunds and lower LFP cell pricing pass-through, while gross profit rose to $954M / 33.1% GM).">Energy Generation &amp; Storage ($M)</span></td>
              <td>$3,415</td>
              <td>$3,837</td>
              <td>$2,408</td>
              <td>$3,139</td>
              <td class="col-q0">$2,881</td>
              <td><span class="badge badge-warn">-8.22%</span></td>
              <td><span class="badge badge-warn">-15.64%</span></td>
              <td class="col-est">$3,750</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Services and Other Revenue: Supercharging, insurance, collision repair, and paid services ($4,605M in Q3 2026)." data-tip="Services &amp; Other ($M): Reached a record $4,605M in Q3 2026 (+0.52% QoQ, +32.52% YoY) with record $734M segment gross profit.">Services &amp; Other ($M)</span></td>
              <td>$3,475</td>
              <td>$3,371</td>
              <td>$3,745</td>
              <td>$4,581</td>
              <td class="col-q0">$4,605</td>
              <td><span class="badge badge-bull">+0.52%</span></td>
              <td><span class="badge badge-bull">+32.52%</span></td>
              <td class="col-est">$4,850</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Cost of Revenues ($22,552M in Q3 2026, down -3.97% QoQ despite higher deliveries and storage volume)." data-tip="Cost of Revenues ($M): Declined -3.97% QoQ to $22,552M in Q3 2026 due to lower raw material costs and manufacturing efficiency.">Cost of Revenue ($M)</span></td>
              <td>($23,041)</td>
              <td>($19,892)</td>
              <td>($17,667)</td>
              <td>($23,485)</td>
              <td class="col-q0">($22,552)</td>
              <td><span class="badge badge-bull">-3.97%</span></td>
              <td><span class="badge badge-bull">-2.12%</span></td>
              <td class="col-est">($24,100)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Gross Profit: Total Revenue ($28,046M) minus Cost of Revenues ($22,552M) = $5,494M." data-tip="Gross Profit ($M): Jumped +15.64% QoQ and +8.71% YoY to $5,494M (19.59% GAAP Gross Margin).">Gross Profit ($M)</span></td>
              <td>$5,054</td>
              <td>$5,009</td>
              <td>$4,720</td>
              <td>$4,751</td>
              <td class="col-q0" style="color: var(--bull-green);">$5,494</td>
              <td><span class="badge badge-bull">+15.64%</span></td>
              <td><span class="badge badge-bull">+8.71%</span></td>
              <td class="col-est">$6,100</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Research and Development Expenses ($2,761M in Q3 2026)." data-tip="R&amp;D Expense ($M): $2,761M in Q3 2026 (+16.45% QoQ, +69.39% YoY) driven by SI compute, Optimus, and Cybercab engineering.">Research &amp; Development ($M)</span></td>
              <td>($1,630)</td>
              <td>($1,783)</td>
              <td>($1,946)</td>
              <td>($2,371)</td>
              <td class="col-q0">($2,761)</td>
              <td><span class="badge badge-warn">+16.45%</span></td>
              <td><span class="badge badge-warn">+69.39%</span></td>
              <td class="col-est">($2,850)</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Selling, General and Administrative Expenses ($2,015M in Q3 2026; $0M restructuring)." data-tip="SG&amp;A &amp; Other ($M): $2,015M in Q3 2026 (+1.66% QoQ, +12.01% YoY incl. prior restructuring).">Selling, General &amp; Admin ($M)</span></td>
              <td>($1,800)</td>
              <td>($1,817)</td>
              <td>($1,833)</td>
              <td>($1,982)</td>
              <td class="col-q0">($2,015)</td>
              <td><span class="badge badge-neutral">+1.66%</span></td>
              <td><span class="badge badge-warn">+11.94%</span></td>
              <td class="col-est">($2,050)</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="Total Operating Expenses: R&amp;D ($2,761M) + SG&amp;A ($2,015M) = $4,776M." data-tip="Total Operating Expenses ($M): $4,776M in Q3 2026 (+9.72% QoQ, +39.24% YoY).">Total Operating Expenses ($M)</span></td>
              <td>($3,430)</td>
              <td>($3,600)</td>
              <td>($3,779)</td>
              <td>($4,353)</td>
              <td class="col-q0">($4,776)</td>
              <td><span class="badge badge-warn">+9.72%</span></td>
              <td><span class="badge badge-warn">+39.24%</span></td>
              <td class="col-est">($4,900)</td>
            </tr>
            <tr style="font-weight: 700; background-color: rgba(34, 197, 94, 0.05);">
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit ($5,494M) minus Total OpEx ($4,776M) = $718M." data-tip="Operating Income (EBIT): Surged +80.40% QoQ from $398M in Q2 2026 to $718M in Q3 2026.">Operating Income (EBIT) ($M)</span></td>
              <td>$1,624</td>
              <td>$1,409</td>
              <td>$941</td>
              <td>$398</td>
              <td class="col-q0" style="color: var(--bull-green);">$718</td>
              <td><span class="badge badge-bull">+80.40%</span></td>
              <td><span class="badge badge-warn">-55.79%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$1,200</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income attributable to common stockholders ($787M in Q3 2026; Non-GAAP Net Income: $1,697M)." data-tip="GAAP Net Income ($M): $787M in Q3 2026 (vs $1,114M in Q2 2026 which included a $1,005M unrealized SpaceX mark-to-market gain); Non-GAAP Net Income jumped +47.18% QoQ to $1,697M.">GAAP Net Income ($M) (Non-GAAP: $1,697M)</span></td>
              <td>$1,373</td>
              <td>$840</td>
              <td>$477</td>
              <td>$1,114</td>
              <td class="col-q0">$787</td>
              <td><span class="badge badge-warn">-29.35%</span></td>
              <td><span class="badge badge-warn">-42.68%</span></td>
              <td class="col-est">$1,150</td>
            </tr>
            <tr>
              <td><span class="tip" title="Non-GAAP Diluted EPS ($0.48) and GAAP Diluted EPS ($0.22) across 3,541M diluted shares." data-tip="Diluted EPS: Non-GAAP EPS jumped +45.45% QoQ to $0.48 ($0.22 GAAP).">Diluted EPS (Non-GAAP / GAAP) ($)</span></td>
              <td>$0.50 <span style="font-size:10px;color:var(--text-muted);">($0.39)</span></td>
              <td>$0.50 <span style="font-size:10px;color:var(--text-muted);">($0.24)</span></td>
              <td>$0.41 <span style="font-size:10px;color:var(--text-muted);">($0.13)</span></td>
              <td>$0.33 <span style="font-size:10px;color:var(--text-muted);">($0.32)</span></td>
              <td class="col-q0" style="font-weight:700; color: var(--bull-green);">$0.48 <span style="font-size:11px;color:var(--text-muted);">($0.22 GAAP)</span></td>
              <td><span class="badge badge-bull">+45.45%</span></td>
              <td><span class="badge badge-neutral">-4.00%</span></td>
              <td class="col-est" style="font-weight:700; color:#34d399;">$0.56</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Cash Flow &amp; Capital Reinvestment Audit (Rolled to Q3 2026 Actual)</td>
            </tr>
            <tr>
              <td><span class="tip" title="Net cash provided by operating activities ($6,263M in Q3 2026)." data-tip="Operating Cash Flow (OCF): Surged +33.34% QoQ to $6,263M in Q3 2026.">Operating Cash Flow ($M)</span></td>
              <td>$6,238</td>
              <td>$3,813</td>
              <td>$3,937</td>
              <td>$4,697</td>
              <td class="col-q0" style="color: var(--bull-green);">$6,263</td>
              <td><span class="badge badge-bull">+33.34%</span></td>
              <td><span class="badge badge-bull">+0.40%</span></td>
              <td class="col-est">$6,600</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital expenditures ($4,732M in Q3 2026)." data-tip="Capital Expenditures ($M): $4,732M in Q3 2026 (-18.26% QoQ, +110.50% YoY).">Capital Expenditures ($M)</span></td>
              <td>($2,248)</td>
              <td>($2,393)</td>
              <td>($2,493)</td>
              <td>($5,789)</td>
              <td class="col-q0">($4,732)</td>
              <td><span class="badge badge-bull">-18.26%</span></td>
              <td><span class="badge badge-warn">+110.50%</span></td>
              <td class="col-est">($4,800)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Reported Free Cash Flow: OCF ($6,263M) minus CapEx ($4,732M) = +$1,531M." data-tip="Reported Free Cash Flow ($M): Snapped back to +$1,531M in Q3 2026 from -$1,092M in Q2 2026.">Reported Free Cash Flow ($M)</span></td>
              <td>$3,990</td>
              <td>$1,420</td>
              <td>$1,444</td>
              <td>($1,092)</td>
              <td class="col-q0" style="color: var(--bull-green);">$1,531</td>
              <td><span class="badge badge-bull">+$2,623M</span></td>
              <td><span class="badge badge-warn">-61.63%</span></td>
              <td class="col-est">$1,800</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Stock-based compensation expense ($1,165M in Q3 2026)." data-tip="Stock-Based Compensation ($M): $1,165M in Q3 2026 (+1.22% QoQ, +75.72% YoY) including 2025 CEO Performance Award tranches.">Stock-Based Compensation ($M)</span></td>
              <td>($663)</td>
              <td>($954)</td>
              <td>($1,030)</td>
              <td>($1,151)</td>
              <td class="col-q0">($1,165)</td>
              <td><span class="badge badge-neutral">+1.22%</span></td>
              <td><span class="badge badge-warn">+75.72%</span></td>
              <td class="col-est">($1,180)</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Principal payments on finance leases ($26M in Q3 2026)." data-tip="Principal Finance Lease Payments ($M): $26M in Q3 2026.">Principal Finance Lease Payments ($M)</span></td>
              <td>($18)</td>
              <td>($19)</td>
              <td>($18)</td>
              <td>($19)</td>
              <td class="col-q0">($26)</td>
              <td><span class="badge badge-warn">+36.84%</span></td>
              <td><span class="badge badge-warn">+44.44%</span></td>
              <td class="col-est">($25)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Forensic True Free Cash Flow: Reported FCF ($1,531M) minus SBC ($1,165M) minus Finance Leases ($26M) = +$340M." data-tip="True Free Cash Flow ($M): Positive +$340M in Q3 2026 (rebounding +$2,602M from -$2,262M in Q2 2026).">True Free Cash Flow (ex-SBC &amp; Leases) ($M)</span></td>
              <td>$3,309</td>
              <td>$447</td>
              <td>$396</td>
              <td>($2,262)</td>
              <td class="col-q0" style="color: var(--bull-green);">$340</td>
              <td><span class="badge badge-bull">+$2,602M</span></td>
              <td><span class="badge badge-warn">-89.72%</span></td>
              <td class="col-est">$595</td>
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
          <div class="card-subtitle">Forensic deconstruction of the 18.1% Auto Gross Margin ex-Credits, +$1,255M FSD Deferred Revenue Inflow, and +$340M True FCF</div>
        </div>
        <span class="badge badge-bull">HIGH-QUALITY MARGIN &amp; OCF EXPANSION</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>1. Organic Auto Margin Snapback: 18.1% Ex-Credits Despite Regulatory Credits Falling to $113M</span>
              <span class="badge badge-bull">+180 BPS QOQ AUTO GM</span>
            </div>
            <p>
              Zero-emission regulatory credit revenue fell from $417M in Q3 2025 and $146M in Q2 2026 to just <strong>$113M in Q3 2026</strong>. Despite this headwind, GAAP Automotive Gross Margin rose from 16.9% to <strong>18.5%</strong>, and Non-GAAP Automotive Gross Margin ex-credits expanded +180 bps QoQ (and +270 bps YoY) to <strong>18.1%</strong>—proving genuine manufacturing cost reductions and software attach lift.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>2. FSD Deferred Revenue Flywheel: +$1,255M Q3 Cash Flow Inflow ($8,787M Balance)</span>
              <span class="badge badge-bull">1.74M ACTIVE FSD SUBS</span>
            </div>
            <p>
              On the Statement of Cash Flows, changes in Deferred Revenue generated a massive <strong>+$1,255M operating cash inflow</strong> in Q3 2026 (up 5.5x from +$228M in Q2), lifting total balance sheet deferred revenue ($4,661M current + $4,126M long-term) to <strong>$8,787M</strong> as active FSD subscriptions surged to <strong>1.74 million</strong>.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--warn-amber);">
            <div class="forensic-item-title">
              <span>3. Non-Operating Mark-to-Market Noise: SpaceX (-$142M) vs. Digital Assets (+$288M)</span>
              <span class="badge badge-warn">BELOW-THE-LINE AUDIT</span>
            </div>
            <p>
              In Q2 2026, GAAP Net Income ($1,114M) was artificially boosted by a +$1,005M unrealized gain on Tesla's $2.0B SpaceX equity investment. In Q3 2026, Tesla recorded a <strong>-$142M unrealized SpaceX loss</strong> offset by a <strong>+$288M unrealized Bitcoin/digital asset gain</strong> (lifting digital assets to $962M). Stripping out both items and $982M after-tax SBC, Non-GAAP Net Income surged +47.2% QoQ to <strong>$1,697M ($0.48 EPS)</strong>.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Forensic True Free Cash Flow Inflection: Rebounded +$2.60B Sequentially to +$340M</span>
              <span class="badge badge-bull">+$1,531M REPORTED FCF</span>
            </div>
            <p>
              With Operating Cash Flow surging to <strong>$6,263M</strong> (+33.3% QoQ, aided by +$3,991M AP/accrued liability expansion as DPO rose to 66 days) and CapEx moderating to <strong>$4,732M</strong>, Reported FCF flipped from -$1,092M in Q2 to <strong>+$1,531M</strong>, and Forensic True FCF (after $1,165M SBC and $26M finance leases) turned positive at <strong>+$340M</strong>.
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
            <span class="waterfall-label">(-) Capital Expenditures (AI Compute &amp; Factories)</span>
            <span class="waterfall-val" style="color: #f87171;">-${q0_capex:,.0f}M</span>
          </div>
          <div class="waterfall-row" style="border-top: 1px dashed rgba(255, 255, 255, 0.15); padding-top: 6px;">
            <span class="waterfall-label" style="font-weight: 700; color: #f8fafc;">(=) Standard Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="font-weight: 700; color: #34d399;">+${q0_rep_fcf:,.0f}M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">(-) Stock-Based Compensation (incl. 2025 CEO Award)</span>
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
            *Note: Even after deducting $1,165M in non-cash SBC and $26M in finance lease principal repayments, Tesla generated positive <strong>+$340M</strong> True Free Cash Flow in Q3 2026 while adding +$1,923M to its $45,447M cash fortress.
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
          <div class="card-subtitle">Post-print institutional assessment of Austin Cybercab Robotaxi, 18.1% Auto Margin, Megafactory Texas, and $4.73B AI CapEx</div>
        </div>
        <span class="badge badge-bull">PHYSICAL AI &amp; AUTO MARGIN INFLECTION</span>
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
                <span class="audit-point-title">1. Cybercab Commercial Robotaxi Launch in Austin (8x QoQ Unsupervised Miles)</span>
                <span class="badge badge-bull">~2M UNSUPERVISED MILES</span>
              </div>
              <p>
                Tesla began providing commercial Robotaxi rides using <strong>Cybercabs in Austin on September 3, 2026</strong> (operating 6am–midnight with hands-free Grok voice integration), driving an <strong>8-fold sequential surge</strong> in cumulative unsupervised Robotaxi miles to nearly 2 million miles.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Auto Gross Margin Ex-Credits Expansion (+180 bps QoQ to 18.1%)</span>
                <span class="badge badge-bull">4-YEAR HIGH BACKLOG</span>
              </div>
              <p>
                Non-GAAP Automotive gross margin ex-credits jumped to <strong>18.1%</strong> (from 16.3% in Q2) alongside record Gigafactory Berlin production, 11 days of global inventory, and the largest passenger vehicle backlog in four years.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Start of Volume Production: Tesla Semi (Nevada) &amp; Optimus (Fremont)</span>
                <span class="badge badge-blue">COMMERCIAL PRODUCTION</span>
              </div>
              <p>
                Tesla commenced volume production of the Class 8 <strong>Tesla Semi in Nevada</strong> (500-mile range at 82,000 lbs GCW, 1.7 kWh/mile) and began manufacturing the first production-quality <strong>Optimus humanoid robots on high-volume lines in Fremont</strong>.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Megafactory Texas (50 GWh) Start of Production &amp; 33.1% Energy Margin</span>
                <span class="badge badge-bull">13.7 GWH DEPLOYED</span>
              </div>
              <p>
                Energy Storage deployed <strong>13.7 GWh</strong> in Q3 with a <strong>33.11% segment gross margin ($954M gross profit)</strong>, commenced production at <strong>Megafactory Texas (50 GWh capacity)</strong>, and shipped the first Megapacks using domestic Nevada LFP cells.
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
                <span class="audit-point-title">1. Battery Cell Availability Limiting Global Vehicle Volume Ramp</span>
                <span class="badge badge-bear">CELL BOTTLENECK</span>
              </div>
              <p>
                Management explicitly disclosed that <strong>battery cell availability remained the primary limiting factor</strong> on global vehicle production growth in Q3 (464,391 produced / 486,532 delivered, -2% YoY) as cells are shared across Model Y, Cybercab, Semi, and Megapack.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Surging OpEx (+39.2% YoY to $4,776M) Compressing GAAP Operating Margin (2.56%)</span>
                <span class="badge badge-bear">R&amp;D +69% YOY</span>
              </div>
              <p>
                Aggressive investments in Super Intelligence (SI), robotics, and the 2025 CEO Performance Award lifted R&amp;D by +69.4% YoY to <strong>$2,761M</strong> and total OpEx to <strong>$4,776M</strong>, keeping GAAP operating margin at <strong>2.56% ($718M EBIT)</strong>.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Energy Revenue Compression (-15.6% YoY to $2,881M) on Tariff Refunds</span>
                <span class="badge badge-warn">TARIFF REFUNDS</span>
              </div>
              <p>
                Despite record 13.7 GWh deployments, Energy Generation &amp; Storage revenue declined -15.6% YoY to <strong>$2,881M</strong> partially due to tariff-related customer refunds and lower LFP battery price pass-throughs.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Elevated Multi-Year Capital Intensity ($15.41B TTM CapEx)</span>
                <span class="badge badge-warn">$4.73B Q3 CAPEX</span>
              </div>
              <p>
                Scaling SI training compute to 400 MW by year-end, building out the Austin Semiconductor Fab for 2027 commissioning, and ramping Texas 4680/lithium/cathode lines require sustained multi-billion quarterly CapEx.
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
            1. Cybercab Austin Unit Economics &amp; Multi-City Expansion — Dan Levy (Barclays)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> You launched Cybercab in the Austin Robotaxi fleet on September 3 and grew unsupervised miles 8x QoQ to nearly 2 million miles. What are the gating regulatory and fleet supply milestones before expanding unsupervised Cybercab service to additional Texas and California metros?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> Management confirmed that Austin operating hours are now 6am to midnight with Grok voice assistant integration, and that weekly unsupervised miles are compounding at double-digit rates. Allocation decisions in Q4 and 2027 will explicitly balance selling vehicles to customers against retaining Cybercabs and Model Ys for Tesla's high-margin owned-and-operated Robotaxi fleet.
          </p>
        </div>
        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #34d399; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #34d399; font-size: 13.5px; margin-bottom: 4px;">
            2. Sustainability of 18.1% Auto Gross Margin Ex-Credits &amp; FSD Take-Rate Surge — Adam Jonas (Morgan Stanley)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> Non-GAAP Automotive gross margin ex-credits expanded 180 bps sequentially to 18.1% even as regulatory credits fell to $113M. How much of that expansion came from North American FSD attach rates rising nearly 20 percentage points sequentially versus manufacturing cost reductions?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> CFO Vaibhav Taneja highlighted that both levers contributed: active FSD subscriptions jumped +260k QoQ to 1.74M (with North American new-delivery FSD attach surging nearly 20 percentage points QoQ and 4 new EU countries approved), while record production at Gigafactory Berlin and lower material costs drove down per-unit COGS.
          </p>
        </div>
        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #f59e0b; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #fcd34d; font-size: 13.5px; margin-bottom: 4px;">
            3. Battery Cell Supply Bottlenecks vs. 4-Year High Vehicle Backlog — Colin Langan (Wells Fargo)
          </div>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
            <strong>Analyst Question:</strong> You noted that passenger vehicle backlog ended Q3 at a 4-year high and global inventory dropped to 11 days, yet battery availability limited auto volume growth. When will in-house 4680 and Nevada LFP capacity relieve this bottleneck?
          </p>
          <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Management Response &amp; Takeaway:</strong> Management explained that shipping the first Megapacks with Nevada-built LFP cells and expanding Texas 4680 capacity (&gt;40 GWh) alongside Texas lithium refining (30 GWh) and cathode production (10 GWh) are steadily relieving cell constraints for Semi, Cybercab, and Model Y heading into 2027.
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
          <div class="card-title"><span class="card-title-accent"></span>EV, Autonomy &amp; Physical AI Peer Benchmarking</div>
          <span class="badge badge-blue">POST-PRINT COMP MATRIX (Q3 2026)</span>
        </div>

        <div class="table-wrapper" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th style="min-width:140px;">Ticker / Peer</th>
                <th><span class="tip" title="Quarterly Vehicle Deliveries or Scale in Q3 2026." data-tip="Q3 Volume: 486,532 vehicles + 13.7 GWh storage for TSLA.">Q3 Volume</span></th>
                <th><span class="tip" title="GAAP Gross Margin percentage in Q3 2026." data-tip="Gross Margin: 19.59% Consolidated (18.1% Auto ex-credits, 33.1% Energy) for TSLA.">Gross Margin</span></th>
                <th><span class="tip" title="Adjusted EBITDA Margin in Q3 2026." data-tip="Adjusted EBITDA Margin: 13.91% ($3,900M) for TSLA in Q3 2026.">EBITDA Margin</span></th>
                <th><span class="tip" title="Operating Cash Flow in Q3 2026." data-tip="Operating Cash Flow: $6,263M (22.33% OCF margin) for TSLA.">OCF Margin</span></th>
                <th><span class="tip tip-right" title="Net Cash / (Debt) Balance Sheet Position." data-tip="Net Cash Fortress: +$35.92B net cash for TSLA.">Net Cash</span></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color:var(--accent-blue);">TSLA (Q3 Actual)</strong></td>
                <td><span class="badge badge-bull">486.5k + 13.7 GWh</span></td>
                <td><strong style="color:var(--bull-green);">19.59%</strong></td>
                <td><strong style="color:var(--bull-green);">13.91%</strong></td>
                <td><strong style="color:var(--bull-green);">+22.33%</strong></td>
                <td style="color:var(--bull-green);">+$35.9B</td>
              </tr>
              <tr>
                <td><strong>BYDDY (BYD Co.)</strong></td>
                <td><span class="badge badge-bull">1,120k (BEV+PHEV)</span></td>
                <td>19.80%</td>
                <td>12.40%</td>
                <td>+14.10%</td>
                <td>+$6.4B</td>
              </tr>
              <tr>
                <td><strong>RIVN (Rivian Automotive)</strong></td>
                <td><span class="badge badge-neutral">14.2k BEVs</span></td>
                <td>-8.50%</td>
                <td>-42.00%</td>
                <td>-38.00%</td>
                <td>+$1.8B</td>
              </tr>
              <tr>
                <td><strong>GM (General Motors)</strong></td>
                <td><span class="badge badge-neutral">660k ICE/EV</span></td>
                <td>12.10%</td>
                <td>9.80%</td>
                <td>+10.50%</td>
                <td>-$84.0B (Fin)</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">Full-Stack Physical AI &amp; Energy Storage Moat</span>
              <span class="badge badge-bull">400 MW SI COMPUTE</span>
            </div>
            <p>
              • <strong>Unmatched Cash Generation:</strong> Tesla's $6.26B quarterly OCF and $45.45B cash fortress allow it to self-fund Cortex 1/2 superclusters, Austin Semiconductor Fab, and Megafactory Texas.<br>
              • <strong>Software + Energy Margin Buffer:</strong> 33.1% Energy gross margins ($954M GP) and 1.74M FSD subscribers decouple Tesla from legacy auto cyclicality.
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
              <span class="audit-point-title">1. Cybercab Austin Fleet Scaling &amp; Unsupervised Expansion</span>
              <span class="badge badge-bull">LIVE IN AUSTIN</span>
            </div>
            <p>
              Following the Sep 3 Austin launch and 8x QoQ growth in unsupervised miles (~2M miles), fleet supply and orchestration upgrades will cut wait times and unlock new metros.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Tesla Semi Volume Ramp in Nevada &amp; Megacharger Rollout</span>
              <span class="badge badge-blue">25,000/YR CAPACITY</span>
            </div>
            <p>
              High-volume Semi line in Nevada is now in production alongside the first pre-assembled Megachargers, targeting commercial freight operators with 1.7 kWh/mile efficiency.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Optimus Humanoid Robot Commercial Line in Fremont</span>
              <span class="badge badge-bull">PRODUCTION STARTED</span>
            </div>
            <p>
              First production-quality Optimus bots are coming off Fremont high-volume lines while Texas Optimus construction advances toward mass commercialization.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Megafactory Texas (50 GWh) &amp; AI Data Center Grid Demand</span>
              <span class="badge badge-bull">116 GWH GLOBAL CAP</span>
            </div>
            <p>
              With Megafactory Texas (50 GWh) joining Lathrop (40 GWh) and Shanghai (20 GWh), Tesla's energy storage capacity reaches 116+ GWh to serve hyperscale AI data centers.
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
        <span class="badge badge-bull">POST-PRINT COMPOSITE SCORE: 74 / 100 (CONSTRUCTIVE)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Post-Print Consensus: 18.1% Auto GM Ex-Credits &amp; +$1.53B FCF Beat Offset -3.32% AH Dip on $4.73B AI CapEx
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            TSLA dipped <strong>-3.32% (-$12.84/sh to $373.63)</strong> in volatile after-hours action (just outside the ±2.99% / ±$11.53 weekly straddle band) as quant algorithms reacted to headline GAAP EPS ($0.22) and $4.73B CapEx, before institutional desks highlighted the <strong>$0.48 Non-GAAP EPS beat, 18.1% Auto GM ex-credits (+180 bps QoQ), +$1.53B FCF snapback, and 4-year high vehicle backlog</strong>.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-warn">AH Reaction: -3.32% ($373.63)</span>
          <span class="badge badge-bull">Auto GM Ex-Cred: 18.1%</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #1: Retail &amp; Microblogging Pulse <span class="badge badge-bull">REDDIT / X / FINTWIT</span></span>
            <span class="badge badge-bull">SCORE: 82 / 100 (BULLISH)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 82%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Top Retail Catalyst</span>
              <span class="kpi-val" style="color:var(--bull-green);">Cybercab + Semi + Optimus</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">FSD Milestone</span>
              <span class="kpi-val">1.74M Paying Subs</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Dip-Buyer Sentiment</span>
              <span class="kpi-val">79% Buying $370–$375</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            "X / FinTwit Autonomy Thread: 'Auto gross margin ex-credits jumped to 18.1% with only $113M in credits, FCF flipped +$2.6B to +$1.53B, FSD subs hit 1.74M, and Cybercab/Semi/Optimus are all in production. Algos selling $373 are missing the forest.'"
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #2: Sell-Side Flash Note Reactions <span class="badge badge-bull">WALL STREET DESKS</span></span>
            <span class="badge badge-bull">SCORE: 75 / 100 (MARGIN UPGRADES)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 75%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Core Margin Surprise</span>
              <span class="kpi-val" style="color:var(--bull-green);">18.1% vs 16.5% Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Non-GAAP EPS Beat</span>
              <span class="kpi-val">$0.48 vs $0.45 Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Energy Gross Margin</span>
              <span class="kpi-val">33.11% ($954M GP)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Sell-Side Auto Desk: "The standout metric in Q3 is 18.1% non-GAAP auto gross margin ex-credits (+180 bps QoQ) paired with +$1,531M FCF and a 4-year high passenger vehicle backlog."
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #3: Management Call Tone &amp; Candor <span class="badge badge-bull">TRANSCRIPT AUDIT</span></span>
            <span class="badge badge-bull">SCORE: 84 / 100 (CONFIDENT)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 84%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Robotaxi Pace</span>
              <span class="kpi-val">8x QoQ Miles (~2M)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">NA FSD Attach Lift</span>
              <span class="kpi-val">+20 Pct Pts QoQ</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">SI Compute Target</span>
              <span class="kpi-val">400 MW by YE26</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Shareholder Update: "We started providing Robotaxi rides using Cybercabs on September 3 in Austin. Cumulative unsupervised Robotaxi miles grew eightfold quarter over quarter... We ended the quarter with the largest backlog for our passenger vehicles in four years."
          </div>
        </div>

        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Pillar #4: Post-Print Options &amp; Gamma Flow <span class="badge badge-blue">DERIVATIVES DESK</span></span>
            <span class="badge badge-neutral">SCORE: 56 / 100 (VOL DIGESTION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 56%; background: var(--accent-blue);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Actual vs Implied Move</span>
              <span class="kpi-val">-3.32% vs ±2.99% Est</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Key Gamma Support</span>
              <span class="kpi-val">$370.00 Put Wall</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">T+1 Reversal Trigger</span>
              <span class="kpi-val">Reclaim $380.00</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            With the -$12.84 AH move roughly matching the $11.53 straddle premium, front-week options face rapid theta/vega decay at the open if TSLA stabilizes between $370 and $380.
          </div>
        </div>
      </div>

      <!-- AGENT 2C SOCIAL PULSE SUMMARY CARDS -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; margin-top: 16px;">
        <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #34d399; padding: 12px 14px; border-radius: 6px;">
          <div style="font-weight: 700; color: #34d399; font-size: 13px; margin-bottom: 4px;">Retail Trader Reaction (Reddit r/teslainvestorsclub, r/wallstreetbets &amp; X)</div>
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
          <div class="card-subtitle">Post-call risk-reward setups anchored to the After-Hours Price (${ah_price:.2f}) and Core Auto Margin / FCF Inflection</div>
        </div>
        <span class="badge badge-bull">POST-PRINT TACTICAL PLAYBOOK</span>
      </div>

      <div class="scenario-grid">
        <!-- BULL CASE -->
        <div class="scenario-card scenario-bull">
          <div class="scenario-title">
            <span style="color:var(--bull-green);">BUY THE AH DIP / MARGIN RE-RATING (BULL CASE)</span>
            <span class="badge badge-bull">PROB: 50% | TARGET: $415.00–$440.00 (Anchored above ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>18.1% Core Auto Margin Validation:</strong> Institutional buyers step in at the T+1 open once models adjust for <strong>18.1% Auto GM ex-credits (+180 bps QoQ)</strong> and the <strong>4-year high vehicle backlog</strong>.</li>
            <li><strong>+$1.53B FCF &amp; +$1.26B FSD Cash Inflow:</strong> Recognition that Tesla generated <strong>$6,263M OCF</strong> and <strong>+$1,531M Reported FCF</strong> (+$340M True FCF) while growing active FSD subs to 1.74M.</li>
            <li><strong>Physical AI Production Inflection:</strong> Commercial Cybercab rides in Austin (8x QoQ miles), Nevada Semi volume production, and Fremont Optimus line ramp drive multi-quarter multiple expansion.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure (Bull Target: $415.00):</strong>
            Accumulate shares in the $370–$375 zone or initiate a <strong>Dec 18, 2026 $380 / $420 Bull Call Spread</strong> after morning IV crush to capture a reclaim of $386.47 regular close and breakout toward $415+.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">RANGE CONSOLIDATION &amp; THETA HARVEST (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 30% | RANGE: $360.00–$390.00 (Around ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>CapEx &amp; OpEx Digestion:</strong> Market balances the strong 19.59% gross margin and $0.48 Non-GAAP EPS beat against <strong>$4,776M quarterly OpEx (+39% YoY)</strong> and <strong>$4,732M CapEx</strong>.</li>
            <li><strong>Battery Cell Supply Constraint:</strong> Near-term auto volume growth stays capped by battery cell allocation across Model Y, Cybercab, Semi, and Megapack.</li>
            <li><strong>Options Pinning:</strong> Post-print IV crush pins TSLA between the $365 institutional put support and $390 call resistance.</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure:</strong>
            Deploy a <strong>Nov 20, 2026 $355 / $395 Iron Condor</strong> or sell <strong>$360 Cash-Secured Puts</strong> to harvest post-earnings volatility compression.
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">BREAKDOWN ON OPEX &amp; VALUATION MULTIPLE (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 20% | TARGET: $345.00–$330.00 (Anchored below ${ah_price:.2f} AH)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>GAAP Operating Margin Compression:</strong> Bears focus on GAAP operating margin of <strong>2.56% ($718M EBIT)</strong> and GAAP EPS of <strong>$0.22</strong> due to $1,165M quarterly SBC and +69% YoY R&amp;D growth.</li>
            <li><strong>Energy Revenue &amp; Tariff Headwinds:</strong> Concerns over Energy revenue declining -15.6% YoY to $2,881M on tariff-related customer refunds.</li>
            <li><strong>Technical Breakdown Below $370:</strong> Loss of the $370 gamma support triggers momentum selling toward the 50-day moving average ($345).</li>
          </ul>
          <div class="trade-structure">
            <strong>Post-Print Trade Structure (Bear Target: $345.00):</strong>
            Initiate a <strong>Nov 20, 2026 $370 / $345 Bear Put Spread</strong> if TSLA breaks below $368 on heavy T+1 opening volume.
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
        <span>SEC EDGAR CIK: <strong>0001318605</strong></span> • 
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
        "page_title": f"TSLA (${ah_price:.2f}) Q3 2026 Post-Earnings Forensic & Sentiment Tearsheet",
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
        "bull_target_low_num": 415.0,
        "bear_target_high_num": 345.0
    },
    "rendered_container_html": container_html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"[SUCCESS] Generated Post-Earnings Draft for TSLA at: {DRAFT_PATH.name}")
print(f"  - Inner HTML Character Count: {len(container_html):,}")
print(f"  - Interactive Tooltip Count (.tip): {container_html.count('class=\"tip')}")
print(f"  - Data-Tip Count (data-tip=): {container_html.count('data-tip=\"')}")
