"""
HOOD Dedicated Post-Earnings Draft Builder (Track A + Track B Standard)
Builds drafts/HOOD_2026-10-27_post_draft.json with 100% Q3 2026 (Actual) rolled 5-quarter tables,
Q4 2026E forward guidance columns, zero T-1 bleed-through, and Track B interactive enhancements.
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "HOOD_2026-10-27_post_truth.json"
BUS_2A_PATH = BASE_DIR / "post_agent_bus" / "HOOD_2026-10-27_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / "post_agent_bus" / "HOOD_2026-10-27_agent2b_transcript.json"
BUS_2C_PATH = BASE_DIR / "post_agent_bus" / "HOOD_2026-10-27_agent2c_social.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "HOOD_2026-10-27_post_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
kpis_data = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
trans_data = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
soc_data = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

reg_price = truth["post_print_reaction"]["regular_close_price"]      # 94.56
ah_price = truth["post_print_reaction"]["after_hours_price"]         # 87.34
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]  # -7.64
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] # 10.13
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 9.73)
verdict = truth["post_print_reaction"]["overall_print_verdict"]      # EPS BEAT & FCF RAISE

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]  # 1424.0
cons_rev = truth["t1_baseline"]["consensus_revenue_millions"]                 # 1425.0
whisper_rev = truth["t1_baseline"].get("whisper_revenue_millions", 1460.0)
q0_gaap_eps = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"]     # 0.51
q0_adj_eps = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"]   # 0.60
cons_eps = truth["t1_baseline"]["consensus_eps_nongaap"]                      # 0.55

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # 1225.0
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 21.0
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # 1204.0
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 80.0
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 0.0
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # 1124.0

s5q = truth["stitched_5q_chronological"]

bull_target = 98.00
bear_target = 76.00

# Table 1B-1 Beat/Miss rows
rows_1b1 = [
    f"""              <tr>
                <td><span class="tip" title="Total net revenues generated from brokerage transactions." data-tip="Transaction-Based Revenues: Customer trading fees and order routing across options, event contracts, equities, and crypto.">Transaction-Based Revenues</span></td>
                <td>$776.0M</td>
                <td>$730.0M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$845.0M</td>
                <td style="font-weight:700; color: #34d399;">$867.0M</td>
                <td>
                  <span class="badge badge-bull">+$22.0M (+2.60%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:72%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Net revenues generated from prediction markets and event contracts." data-tip="Event Contracts Revenue: Revenue from trading prediction market contracts on political elections, macro data, and sports.">Event Contracts Revenue</span></td>
                <td>$156.0M</td>
                <td>$25.0M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$145.0M</td>
                <td style="font-weight:700; color: #34d399;">$173.0M</td>
                <td>
                  <span class="badge badge-bull">+$28.0M (+19.31%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:95%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT (&gt;6x YoY)</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Total net revenues across all 14 business lines." data-tip="Total Net Revenues: Combined transaction fees, net interest income, and subscription services ($1,424M).">Total Net Revenues</span></td>
                <td>$1,308.0M</td>
                <td>$1,274.0M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$1,425.0M</td>
                <td style="font-weight:700; color: #34d399;">$1,424.0M</td>
                <td>
                  <span class="badge badge-neutral">-$1.0M (-0.07%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:50%; height:100%; background:linear-gradient(90deg, #3b82f6, #64748b);"></div></div>
                </td>
                <td><span class="badge badge-neutral">IN-LINE</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Non-GAAP diluted earnings per share." data-tip="Adjusted Diluted EPS: Net profit per diluted share adjusted for non-cash mark-to-market venture fund revaluations ($0.60 vs $0.55 est).">Adjusted Diluted EPS (Non-GAAP)</span></td>
                <td>$0.62</td>
                <td>$0.61</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$0.55</td>
                <td style="font-weight:700; color: #34d399;">$0.60</td>
                <td>
                  <span class="badge badge-bull">+$0.05 (+9.09%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:82%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Total paid subscribers to Robinhood Gold premium tiers." data-tip="Robinhood Gold Subscribers: Paying members receiving 5% APY cash sweep, lower margin rates, and 3% retirement match.">Robinhood Gold Subscribers</span></td>
                <td>4.84M</td>
                <td>3.20M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">5.00M</td>
                <td style="font-weight:700; color: #34d399;">5.20M</td>
                <td>
                  <span class="badge badge-bull">+0.20M (+4.00%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:78%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT (+62.5% YoY)</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Adjusted EBITDA and operational profitability margin." data-tip="Adjusted EBITDA: Operating profitability before D&amp;A, SBC, and venture fund valuation swings ($808M, 57% margin).">Adjusted EBITDA &amp; Margin</span></td>
                <td>$741.0M (57%)</td>
                <td>$742.0M (58%)</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$765.0M (54%)</td>
                <td style="font-weight:700; color: #34d399;">$808.0M (57%)</td>
                <td>
                  <span class="badge badge-bull">+$43.0M (+5.62%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:85%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Organic cash flow generated after CapEx, SBC, and leases." data-tip="True Free Cash Flow: Operating cash flow ($1,225M) minus CapEx ($21M) minus SBC ($80M) = $1,124M.">True Free Cash Flow (ex-SBC)</span></td>
                <td>$591.0M</td>
                <td>-$1,666.0M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$550.0M</td>
                <td style="font-weight:700; color: #34d399;">$1,124.0M</td>
                <td>
                  <span class="badge badge-bull">+$574.0M (+104.4%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:100%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-bull">MASSIVE BEAT</span></td>
              </tr>"""
]
table_1b1_html = "\n".join(rows_1b1)

# Table 1B-2 rows from Agent 2B
rows_1b2 = []
for row in trans_data["guidance_accountability_matrix_a"]:
    rows_1b2.append(f"""              <tr>
                <td style="font-weight:600;"><span class="tip" title="Accountability audit against prior management guidance." data-tip="{row['guided_metric']}: Comparison of management commitments made at Q2 earnings vs actual Q3 reported performance.">{row['guided_metric']}</span></td>
                <td>{row['prior_quarter_guidance']}</td>
                <td style="font-weight:600; color: #34d399;">{row['reported_q0_actual']}</td>
                <td>{row['variance_commentary']}</td>
                <td><span class="badge badge-bull">{row['credibility_grade']}</span></td>
              </tr>""")
table_1b2_html = "\n".join(rows_1b2)

# Table 1B-3 rows from Agent 2B
rows_1b3 = []
for row in trans_data["forward_guidance_reset_matrix_b"]:
    rows_1b3.append(f"""              <tr>
                <td style="font-weight:600;"><span class="tip" title="Forward-looking financial expectations and guidance revisions." data-tip="{row['forward_horizon_and_metric']}: Management's forward guidance updates vs Wall Street pre-print hurdle rates.">{row['forward_horizon_and_metric']}</span></td>
                <td>{row['preprint_street_consensus']}</td>
                <td style="font-weight:600; color: #60a5fa;">{row['new_management_guidance']}</td>
                <td style="font-weight:600; color: #34d399;">{row['delta_vs_street']}</td>
                <td><span class="badge badge-bull">{row['action_badge']}</span></td>
                <td>{row['rationale']}</td>
              </tr>""")
table_1b3_html = "\n".join(rows_1b3)

# Q&A Cards from Agent 2B
qa_cards = []
for q in trans_data["call_qa_forensic_highlights"]:
    qa_cards.append(f"""        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #3b82f6; padding: 14px 16px; border-radius: 6px; margin-bottom: 12px;">
          <div style="font-weight: 700; color: #60a5fa; font-size: 14px; margin-bottom: 4px;">
            {q['analyst_name']} • Topic: {q['topic']}
          </div>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 8px;">
            <strong>Analyst Question:</strong> "{q['question']}"
          </p>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5;">
            <strong>Executive Response:</strong> "{q['executive_response']}"
          </p>
        </div>""")
qa_cards_html = "\n".join(qa_cards)

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
            <span class="ticker-symbol">HOOD</span>
            <h1 class="company-name">Robinhood Markets, Inc.</h1>
            <span class="badge badge-bull">{verdict}</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="Immediate post-earnings release forensic tearsheet." data-tip="T+0 Post-Print: Forensic analysis synthesized immediately following the official Q3 2026 SEC Form 8-K release and management conference call.">T+0</span> POST-EARNINGS FORENSIC TEARSHEET</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select • Financial Services, Capital Markets, Retail Brokerage, Crypto &amp; Prediction Markets • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): 0001783879 assigned by the U.S. Securities and Exchange Commission to Robinhood Markets, Inc.">CIK</span>: 0001783879</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Regular Close / <span style="color:#f87171;">After-Hours Price</span></div>
            <div class="price-value">${reg_price:.2f} / <span style="color:#f87171;">${ah_price:.2f}</span> <span style="font-size:14px; color:#f87171;">({post_move_pct:+.2f}%)</span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total equity value at after-hours price across 911M diluted shares." data-tip="Market Capitalization: Post-print equity valuation ($85.0B at $87.34 AH) vs $84.1B Enterprise Value.">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash and liquid investments." data-tip="Enterprise Value (EV): Enterprise value reflects fortress liquidity with $14.75B in cash, segregated cash, and restricted cash.">EV</span></div>
            <div class="price-value">$85.0B / $84.1B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Q3 2026 SEC Form 8-K Filed</span>
          <span class="strip-val" style="color: var(--bull-green);">Tue, Oct 27, 2026 • <span class="tip" title="After Market Close: Official Q3 2026 earnings release filed under Form 8-K Item 2.02." data-tip="Form 8-K Item 2.02 filed October 27, 2026; Exhibit 99.1 Press Release verified and ingested deterministically.">8-K Verified</span></span>
          <span class="kpi-sub">Exhibit 99.1 Financial Statements &amp; Webcast Audited</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="Actual post-market stock reaction (-7.64%) compared against pre-print options straddle implied move (±10.13%)." data-tip="Actual vs. Implied Move: HOOD traded down -7.64% to $87.34 in after-hours trading, remaining strictly inside the ±10.13% (±$9.73/sh) weekly ATM straddle band.">Actual AH Move vs. Implied</span></span>
          <span class="strip-val" style="color: var(--warn-amber);">{post_move_pct:+.2f}% (vs ±{opt_implied_pct:.2f}% Est)</span>
          <span class="kpi-sub">${ah_price - reg_price:+.2f}/sh Actual vs ±${opt_straddle:.2f}/sh <span class="tip" title="At-The-Money weekly straddle price prior to earnings." data-tip="ATM Straddle: Pre-earnings weekly option straddle priced at ±$9.73/sh (10.13% implied move).">ATM Straddle</span></span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 Total Net Revenues ($1,424M, +12% YoY) vs Wall Street Consensus ($1,425M)." data-tip="Q3 2026 Net Revenues: Reported record $1,424M (+12% YoY, +9% QoQ), essentially in-line with $1,425M Street consensus, led by Event Contracts ($173M, up &gt;6x) and Options ($399M, +31%).">Net Revenues vs. Street</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$1,424M <span style="font-size:12px;">(+12% YoY | -$1M In-Line)</span></span>
          <span class="kpi-sub">Street Est: $1,425M | Whisper: $1,460M | Q2 Actual: $1,308M</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 Non-GAAP Adjusted EPS ($0.60) and GAAP Diluted EPS ($0.51) vs Consensus ($0.55)." data-tip="Q3 2026 EPS Beat: Reported $0.60 Adjusted Diluted EPS, beating $0.55 Street consensus by +$0.05 (+9.09%). GAAP Diluted EPS was $0.51 including -$0.07/sh mark-to-market loss on RVI venture fund.">EPS (Adjusted / GAAP)</span></span>
          <span class="strip-val" style="color: var(--bull-green);">$0.60 Adj / $0.51 <span class="tip" title="Reported GAAP diluted EPS ($0.51, included $0.07/sh unrealized loss on RVI fund)." data-tip="GAAP EPS: $0.51 Diluted EPS reflects $67M mark-to-market markdown on Robinhood Ventures Fund I.">GAAP</span></span>
          <span class="kpi-sub">Beat $0.55 Consensus (+9.1%) | Adj EBITDA Margin: 57%</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">FY2026 <span class="tip tip-right" title="Official Full-Year 2026 guidance assumptions updated in the Q3 2026 release." data-tip="FY2026 Guidance Lowered: Management lowered the upper bound of full-year Adjusted OpEx &amp; SBC guidance by $25M to $2.675B-$2.750B on operating efficiencies.">Guidance Stance</span></span>
          <span class="strip-val" style="color: var(--bull-green);">FY26 OpEx Guide Lowered</span>
          <span class="kpi-sub">Ceiling Cut by $25M ($2.675B–$2.750B) | Oct Deposits &gt;$13B MTD</span>
        </div>
      </div>
    </header>

    <!-- TRACK B: STICKY SECTION JUMP-NAV & PAIRED T-1 SWITCHER -->
    <nav class="post-jump-nav" style="position: sticky; top: 8px; z-index: 90; background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(10px); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 10px; padding: 8px 14px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
      <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
        <span style="font-size: 11px; font-weight: 800; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.06em; margin-right: 4px;">⚡ Jump To:</span>
        <a href="#row-1-kpis" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">1. Q3 KPIs</a>
        <a href="#sec-scorecard" style="font-size: 11.5px; color: #34d399; font-weight: 700; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.35);">1B. Beat/Miss &amp; Guidance Scorecard</a>
        <a href="#sec-5q" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">2. Rolling 5Q Table (Q3 Actual + Q4E)</a>
        <a href="#sec-fcf" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">3. Forensic FCF Bridge</a>
        <a href="#sec-audit" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">4. Wins/Drags &amp; Call Audit</a>
        <a href="#sec-comps" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">5. Comps &amp; Valuation</a>
        <a href="#sec-sentiment" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">6. 4-Pillar Sentiment</a>
        <a href="#sec-trade" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">7. PM Trade Matrix</a>
      </div>
      <a href="HOOD_T1_2026-10-27.html" style="font-size: 11.5px; font-weight: 700; color: #60a5fa; text-decoration: none; padding: 5px 12px; border-radius: 6px; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.45); display: flex; align-items: center; gap: 6px;">
        ⇄ Compare Paired T-1 Pre-Earnings Briefing
      </a>
    </nav>

    <!-- 2. ROW 1: TOP KPI CARDS (4 EXECUTIVE CARDS) -->
    <section class="kpi-grid" id="row-1-kpis">
      <!-- CARD A: CASH FLOW & CAPITAL LIGHT MODEL -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Light Scale (Q3 2026)</div>
          <span class="badge badge-bull">RECORD FCF SURGE</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Cash generated from brokerage operations and interest spreads." data-tip="Operating Cash Flow (OCF): Cash inflow generated from Robinhood's brokerage operations ($1,225M in Q3 2026 vs $720M in Q2).">Operating Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">Total OCF Generated: $1,225M (Massive Inflow)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,225M</span>
              <div class="delta-pair">
                <span class="badge badge-bull"><span class="tip" title="Quarter-over-Quarter change from Q2 2026 ($720M) to Q3 2026 ($1,225M)." data-tip="QoQ OCF Growth: +70.14% surge reflecting cash clearing settlements and client deposit growth.">QoQ</span> +70.14%</span>
                <span class="badge badge-bull">YoY +177.7%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Cash spent on IT equipment and software development." data-tip="Capital Expenditures (CapEx): Cash deployed into server capacity and internal software ($10M PPE + $11M software capitalization = $21M).">Capital Expenditures</span> (Q3 2026)</span>
              <span class="kpi-sub">Ultra-Capital-Light: Only 1.47% of Net Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">($21M)</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ -12.50%</span>
                <span class="badge badge-neutral">YoY +75.00%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow minus CapEx." data-tip="Reported FCF: Operating Cash Flow ($1,225M) minus CapEx ($21M) = $1,204M.">Reported Free Cash Flow</span> (Q3 2026)</span>
              <span class="kpi-sub">Exceptional 84.55% FCF Conversion from Net Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,204M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +72.99%</span>
                <span class="badge badge-bull">YoY +175.8%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="True Free Cash Flow: Organic cash flow after subtracting Stock-Based Compensation." data-tip="True Free Cash Flow (ex-SBC): Reported FCF ($1,204M) minus SBC ($80M) minus finance leases ($0M) = $1,124M.">True FCF (ex-SBC)</span> (Q3 2026)</span>
              <span class="kpi-sub">SBC Contained: $80M (5.62% of Net Revenue)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,124M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +90.19%</span>
                <span class="badge badge-bull">YoY +167.5%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING LEVERAGE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Leverage (Q3 2026)</div>
          <span class="badge badge-bull">57% ADJ EBITDA MARGIN</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Net Revenues: Record quarterly net revenues." data-tip="Total Net Revenues: All-time high of $1,424M (+12% YoY, +9% QoQ) driven by event contracts and options.">Total Net Revenues</span> (Q3 2026)</span>
              <span class="kpi-sub">Record Top-Line: $1,424M ($5,082M TTM run-rate)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,424M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +8.87%</span>
                <span class="badge badge-bull">YoY +11.77%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Adjusted EBITDA: Core operational cash earnings." data-tip="Adjusted EBITDA: Reached record $808M (+9% YoY) with industry-leading 56.74% adjusted EBITDA margin.">Adjusted EBITDA</span> (Q3 2026)</span>
              <span class="kpi-sub">56.74% Adjusted EBITDA Margin</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$808M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +9.04%</span>
                <span class="badge badge-bull">YoY +8.89%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Non-GAAP Adjusted EPS: Profitability per share before non-operating valuation marks." data-tip="Adjusted EPS: $0.60 Adjusted EPS (+9.09% beat vs $0.55 consensus), providing clear operational view.">Adjusted Diluted EPS</span> (Non-GAAP)</span>
              <span class="kpi-sub">Beat $0.55 Consensus by +$0.05 / +9.1%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$0.60</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ -3.23%</span>
                <span class="badge badge-neutral">YoY -3.23%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Diluted EPS: Net profit per common share under U.S. GAAP." data-tip="GAAP Diluted EPS: $0.51 includes $67M (-$0.07/sh) unrealized mark-to-market loss on RVI venture fund investments.">GAAP Diluted EPS</span> (Reported)</span>
              <span class="kpi-sub">Includes -$0.07/sh RVI Investment Valuation Loss</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$0.51</span>
              <div class="delta-pair">
                <span class="badge badge-bear">QoQ -17.74%</span>
                <span class="badge badge-bear">YoY -16.39%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS & LIQUIDITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Liquidity (Q3 2026)</div>
          <span class="badge badge-bull">$14.75B TOTAL LIQUID CASH</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Cash, Cash Equivalents &amp; Segregated Funds." data-tip="Liquid Cash &amp; Segregated Cash: $5,829M unrestricted cash + $8,883M segregated customer funds + $42M restricted = $14,754M.">Total Liquid Cash &amp; Segregated Funds</span></span>
              <span class="kpi-sub">$5,829M Unrestricted Cash + $8,883M Segregated</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$14,754M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +7.90%</span>
                <span class="badge badge-bull">YoY +30.93%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Stockholders' Equity: Net worth of the business." data-tip="Total Stockholders' Equity: Surpassed $10 billion for the first time ($10,078M as of Sep 30, 2026).">Total Stockholders' Equity</span></span>
              <span class="kpi-sub">Book Value Surpassed $10B Milestone</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$10,078M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +6.31%</span>
                <span class="badge badge-bull">YoY +27.73%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Net Deposits: Inflow of client assets onto the platform." data-tip="Net Deposits: $16.0B added in Q3; October MTD deposits already exceeded $13.0B ($6B from Dell family).">Q3 Net Deposits / October Momentum</span></span>
              <span class="kpi-sub">$16.0B Q3 Deposits • Oct MTD &gt;$13.0B Surging</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$16.0B</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +21.2%</span>
                <span class="badge badge-bull">YoY +45.5%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Paid subscribers to Robinhood Gold." data-tip="Gold Subscribers: Reached record 5.2 million paying members (+360K QoQ, +62.5% YoY).">Robinhood Gold Subscribers</span></span>
              <span class="kpi-sub">Record 5.20M Subscribers (+360K QoQ)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">5.20M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +7.44%</span>
                <span class="badge badge-bull">YoY +62.50%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT DIVERSIFICATION & MULTIPLES -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Mix &amp; Multiples (Q3 2026)</div>
          <span class="badge badge-blue">14 BUSINESS CYLINDERS &gt;$100M</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Transaction-based revenue share of net revenues." data-tip="Transaction Revenue Share: Options ($399M), Event Contracts ($173M), Equities ($121M), Crypto ($120M) = $867M (60.88%).">Transaction Revenue Mix</span></span>
              <span class="kpi-sub">$867M (Options $399M | Events $173M | Eq $121M)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">60.88%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +156 bps</span>
                <span class="badge badge-bull">YoY +358 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Net interest revenue share of net revenues." data-tip="Net Interest Revenue Mix: $415M (29.14% of total net revenues) generated on interest-earning client balances.">Net Interest Revenue Mix</span></span>
              <span class="kpi-sub">$415M Generated on Growing Asset Base</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">29.14%</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ -60 bps</span>
                <span class="badge badge-bear">YoY -665 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forward Price to Earnings multiple at after-hours price." data-tip="Forward P/E: 27.69x forward consensus EPS at $87.34 after-hours reference price.">Post-Print Forward P/E</span></span>
              <span class="kpi-sub">Compelling Valuation at $87.34 After-Hours Price</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">27.69x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Down from 30.1x</span>
                <span class="badge badge-bull">Attractive PEG</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Percentage of tradable float held by short sellers." data-tip="Short Float: 5.12% of float sold short (~46.6M shares) provides solid short-squeeze fuel on guidance execution.">Short Interest as % of Float</span></span>
              <span class="kpi-sub">5.12% of Float Shorted (~46.6M Shares)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">5.12%</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">Days to Cover: 1.8</span>
                <span class="badge badge-bull">Squeeze Fuel</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. ROW 1B: SCORECARD SECTION (#sec-scorecard) -->
    <section class="scorecard" id="sec-scorecard">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Post-Release Print vs. Expectations &amp; Guidance Scorecard</div>
          <span class="badge badge-bull">{verdict}</span>
        </div>

        <!-- TRACK B: T-1 VS T+0 THESIS AUDIT BANNER -->
        <div class="t1-vs-t0-audit" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 14px; margin-bottom: 18px;">
          <div style="border-right: 1px solid rgba(255,255,255,0.08); padding-right: 12px;">
            <div style="font-size: 11px; font-weight: 800; color: #93c5fd; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">1. Pre-Print T-1 Baseline</div>
            <div style="font-size: 13px; color: #f1f5f9; line-height: 1.5;">
              • Consensus Rev: <strong>$1,425.0M</strong> (Whisper: $1,460.0M)<br>
              • Consensus EPS: <strong>$0.55</strong> (Whisper: $0.60)<br>
              • Implied Move: <strong>±10.13%</strong> (±$9.73 straddle)<br>
              • Focus: Event contracts scale &amp; FY26 OpEx
            </div>
          </div>
          <div style="border-right: 1px solid rgba(255,255,255,0.08); padding-right: 12px;">
            <div style="font-size: 11px; font-weight: 800; color: #34d399; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">2. Actual Q3 2026 Print &amp; Guide</div>
            <div style="font-size: 13px; color: #f1f5f9; line-height: 1.5;">
              • Reported Rev: <strong>$1,424.0M</strong> (In-line / +12% YoY)<br>
              • Adjusted EPS: <strong>$0.60</strong> (+9.1% Beat vs $0.55)<br>
              • True FCF: <strong>$1,124.0M</strong> (Massive FCF conversion)<br>
              • FY26 OpEx Guide: <strong>Ceiling cut by $25M</strong> ($2.675B–$2.75B)
            </div>
          </div>
          <div>
            <div style="font-size: 11px; font-weight: 800; color: #fcd34d; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">3. T-1 Thesis Verdict</div>
            <div style="font-size: 13px; color: #f1f5f9; line-height: 1.5;">
              <span class="badge badge-bull" style="margin-bottom: 4px; display: inline-block;">THESIS VALIDATED</span><br>
              Core operating leverage and event contracts monetization confirmed. The -7.64% after-hours move to $87.34 stayed inside the ±10.13% straddle band, driven by paper venture markdowns, creating an attractive entry.
            </div>
          </div>
        </div>

        <!-- TABLE 1B-1: HEADLINE & COMPANY KPI SCORECARD -->
        <h3 style="font-size: 14px; font-weight: 700; color: #f1f5f9; margin: 14px 0 8px 0; display: flex; align-items: center; justify-content: space-between;">
          <span>Table 1B-1: Headline &amp; Company KPI Consensus vs. Actual Delivery</span>
          <span style="font-size: 11.5px; font-weight: normal; color: var(--text-muted);">All figures in $ Millions except EPS</span>
        </h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th><span class="tip" title="Key financial or operational metric reported by Robinhood." data-tip="Reported KPI: Essential operational performance indicators tracked by Wall Street analysts.">Operational Metric</span></th>
                <th>Q2 2026 (Q-1)</th>
                <th>Q3 2025 (Q-4 YoY)</th>
                <th class="col-q0">Street Consensus</th>
                <th style="color: #34d399;">Reported Q3 Actual</th>
                <th>vs. Consensus Delta</th>
                <th>Print Verdict</th>
              </tr>
            </thead>
            <tbody>
{table_1b1_html}
            </tbody>
          </table>
        </div>

        <!-- TABLE 1B-2: MANAGEMENT GUIDANCE ACCOUNTABILITY -->
        <div style="margin-top: 24px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h3 style="font-size: 14px; font-weight: 700; color: #f1f5f9; margin: 0;">
              Table 1B-2: Management Execution Accountability (Q3 Actual vs. Q2 Guidance)
            </h3>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 11.5px; color: var(--text-muted);">Guidance Credibility Score:</span>
              <span class="badge badge-bull" style="font-size: 12px; font-weight: 800;">94 / 100</span>
            </div>
          </div>
          <!-- TRACK B: CREDIBILITY GAUGE BAR -->
          <div class="credibility-gauge-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; margin-bottom: 12px;">
            <div class="credibility-gauge-fill" style="width: 94%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
          </div>
          <div class="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Guided Metric</th>
                  <th>Prior Q2 Guidance for Q3/FY26</th>
                  <th>Reported Q3 Actual Delivery</th>
                  <th>Variance &amp; Execution Commentary</th>
                  <th>Execution Grade</th>
                </tr>
              </thead>
              <tbody>
{table_1b2_html}
              </tbody>
            </table>
          </div>
        </div>

        <!-- TABLE 1B-3: FORWARD GUIDANCE RESET -->
        <div style="margin-top: 24px;">
          <h3 style="font-size: 14px; font-weight: 700; color: #f1f5f9; margin: 0 0 8px 0; display: flex; align-items: center; justify-content: space-between;">
            <span>Table 1B-3: Forward Guidance Reset (New Management Guidance vs. Street Expectations)</span>
            <span class="badge badge-bull">EXPENSE CUT &amp; SURGING OCTOBER MOMENTUM</span>
          </h3>
          <div class="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Forward Horizon &amp; Metric</th>
                  <th>Pre-Print Street Consensus</th>
                  <th>New Management Guidance</th>
                  <th>Delta vs. Street</th>
                  <th>Action Badge</th>
                  <th>Strategic Rationale</th>
                </tr>
              </thead>
              <tbody>
{table_1b3_html}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. ROW 2: 5-QUARTER STITCHED FINANCIAL PERFORMANCE TABLE (#sec-5q) -->
    <section id="sec-5q" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Rolling 5-Quarter Financial Performance &amp; Dynamic Segment Breakdown</div>
          <span class="badge badge-bull">Q3 2026 ACTUAL REPORTED</span>
        </div>
        <p style="font-size: 12.8px; color: var(--text-muted); margin-bottom: 12px;">
          Comprehensive 5-quarter chronological financial statement audit with strict segment reconciliation across Transaction-Based (Options, Event Contracts, Equities, Crypto), Net Interest, and Other Revenues. All historical figures reconcile to official SEC 10-Q &amp; 8-K exhibits.
        </p>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Financial Metric ($ Millions)</th>
                <th>Q3 2025</th>
                <th>Q4 2025</th>
                <th>Q1 2026</th>
                <th>Q2 2026</th>
                <th class="col-q0">Q3 2026 (Actual)</th>
                <th class="col-est">Q4 2026E (Guided / Street)</th>
                <th>QoQ %</th>
                <th>YoY %</th>
              </tr>
            </thead>
            <tbody>
              <!-- TOP-LINE REVENUE & SEGMENTS -->
              <tr style="font-weight:700; background: rgba(59, 130, 246, 0.08);">
                <td><span class="tip" title="Total net revenues across all revenue streams." data-tip="Total Net Revenues: Reconciles all trading transaction fees, net interest, and subscription revenues ($1,424M in Q3 2026).">Total Net Revenues</span></td>
                <td>$1,274.0</td>
                <td>$1,283.0</td>
                <td>$1,067.0</td>
                <td>$1,308.0</td>
                <td class="col-q0" style="font-weight:700; color:#34d399;">$1,424.0</td>
                <td class="col-est" style="font-weight:700; color:#60a5fa;">$1,500.0</td>
                <td><span class="badge badge-bull">+8.87%</span></td>
                <td><span class="badge badge-bull">+11.77%</span></td>
              </tr>
              <tr>
                <td style="padding-left: 20px;">↳ <span class="tip" title="Transaction-based revenue." data-tip="Transaction-Based Revenues: Total fee revenue from order routing across options, events, equities, and crypto ($867M).">Transaction-Based Revenues</span></td>
                <td>$730.0</td>
                <td>$765.0</td>
                <td>$580.0</td>
                <td>$776.0</td>
                <td class="col-q0" style="font-weight:600; color:#34d399;">$867.0</td>
                <td class="col-est">$920.0</td>
                <td><span class="badge badge-bull">+11.73%</span></td>
                <td><span class="badge badge-bull">+18.77%</span></td>
              </tr>
              <tr>
                <td style="padding-left: 36px; color: var(--text-muted);">• <span class="tip" title="Options transaction revenue." data-tip="Options Revenue: Total customer options contract transaction fees ($399M in Q3 2026, +31% YoY).">Options Contracts Revenue</span></td>
                <td>$305.0</td>
                <td>$325.0</td>
                <td>$280.0</td>
                <td>$342.0</td>
                <td class="col-q0" style="font-weight:600;">$399.0</td>
                <td class="col-est">$420.0</td>
                <td><span class="badge badge-bull">+16.67%</span></td>
                <td><span class="badge badge-bull">+30.82%</span></td>
              </tr>
              <tr>
                <td style="padding-left: 36px; color: var(--text-muted);">• <span class="tip" title="Prediction market event contracts revenue." data-tip="Event Contracts Revenue: Trading revenue from Robinhood Derivatives prediction markets ($173M in Q3 2026, up &gt;6x YoY).">Event Contracts Revenue</span></td>
                <td>$25.0</td>
                <td>$65.0</td>
                <td>$95.0</td>
                <td>$156.0</td>
                <td class="col-q0" style="font-weight:600; color:#34d399;">$173.0</td>
                <td class="col-est">$210.0</td>
                <td><span class="badge badge-bull">+10.90%</span></td>
                <td><span class="badge badge-bull">+592.0%</span></td>
              </tr>
              <tr>
                <td style="padding-left: 36px; color: var(--text-muted);">• <span class="tip" title="Equities transaction revenue." data-tip="Equities Revenue: Trading volume and order flow fees for cash stock trading ($121M in Q3 2026, +41% YoY).">Equities Trading Revenue</span></td>
                <td>$86.0</td>
                <td>$95.0</td>
                <td>$71.0</td>
                <td>$129.0</td>
                <td class="col-q0" style="font-weight:600;">$121.0</td>
                <td class="col-est">$130.0</td>
                <td><span class="badge badge-neutral">-6.20%</span></td>
                <td><span class="badge badge-bull">+40.70%</span></td>
              </tr>
              <tr>
                <td style="padding-left: 36px; color: var(--text-muted);">• <span class="tip" title="Cryptocurrency trading revenue." data-tip="Cryptocurrencies Revenue: Revenue generated from spot crypto trading ($120M in Q3 2026, down -55% YoY).">Cryptocurrencies Revenue</span></td>
                <td>$268.0</td>
                <td>$215.0</td>
                <td>$134.0</td>
                <td>$100.0</td>
                <td class="col-q0" style="font-weight:600;">$120.0</td>
                <td class="col-est">$160.0</td>
                <td><span class="badge badge-bull">+20.00%</span></td>
                <td><span class="badge badge-bear">-55.22%</span></td>
              </tr>
              <tr>
                <td style="padding-left: 20px;">↳ <span class="tip" title="Net interest revenue on assets and loans." data-tip="Net Interest Revenues: Interest on margin loans, securities lending, and cash deposits ($415M in Q3 2026).">Net Interest Revenues</span></td>
                <td>$456.0</td>
                <td>$415.0</td>
                <td>$375.0</td>
                <td>$389.0</td>
                <td class="col-q0" style="font-weight:600; color:#34d399;">$415.0</td>
                <td class="col-est">$425.0</td>
                <td><span class="badge badge-bull">+6.68%</span></td>
                <td><span class="badge badge-bear">-8.99%</span></td>
              </tr>
              <tr>
                <td style="padding-left: 20px;">↳ <span class="tip" title="Other revenues including subscriptions." data-tip="Other Revenues: Robinhood Gold subscription fees, Trump Accounts, and Rothera JV revenues ($142M in Q3 2026).">Other Revenues (Gold &amp; Subscriptions)</span></td>
                <td>$88.0</td>
                <td>$103.0</td>
                <td>$112.0</td>
                <td>$143.0</td>
                <td class="col-q0" style="font-weight:600; color:#34d399;">$142.0</td>
                <td class="col-est">$155.0</td>
                <td><span class="badge badge-neutral">-0.70%</span></td>
                <td><span class="badge badge-bull">+61.36%</span></td>
              </tr>

              <!-- OPERATING EXPENSES & MARGINS -->
              <tr style="border-top: 1px solid var(--border-color);">
                <td><span class="tip" title="Cost of revenues: Brokerage and transaction clearance." data-tip="Brokerage &amp; Transaction Costs: Clearing fees, exchange access fees, and regulatory fees ($68M in Q3 2026).">Brokerage &amp; Transaction Expense (Cost of Rev)</span></td>
                <td>$169.0</td>
                <td>$301.0</td>
                <td>$207.0</td>
                <td>$236.0</td>
                <td class="col-q0" style="font-weight:600;">$68.0</td>
                <td class="col-est">$75.0</td>
                <td><span class="badge badge-bull">-71.19%</span></td>
                <td><span class="badge badge-bull">-59.76%</span></td>
              </tr>
              <tr style="font-weight:700; background: rgba(59, 130, 246, 0.04);">
                <td><span class="tip" title="Gross Profit: Total Net Revenues minus Brokerage &amp; Transaction Costs." data-tip="Gross Profit: Net revenues minus brokerage clearing expenses ($1,424M - $68M = $1,356M, 95.22% gross margin).">Gross Profit</span></td>
                <td>$1,105.0</td>
                <td>$982.0</td>
                <td>$860.0</td>
                <td>$1,072.0</td>
                <td class="col-q0" style="font-weight:700; color:#34d399;">$1,356.0</td>
                <td class="col-est" style="font-weight:700; color:#60a5fa;">$1,425.0</td>
                <td><span class="badge badge-bull">+26.49%</span></td>
                <td><span class="badge badge-bull">+22.71%</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Operating expenses excluding brokerage &amp; transaction costs." data-tip="Operating Expenses: Technology, operations, marketing, credit loss provisions, and G&amp;A ($671M in Q3 2026).">Operating Expenses (ex-Brokerage Clearing)</span></td>
                <td>$470.0</td>
                <td>$332.0</td>
                <td>$449.0</td>
                <td>$498.0</td>
                <td class="col-q0" style="font-weight:600;">$671.0</td>
                <td class="col-est">$695.0</td>
                <td><span class="badge badge-neutral">+34.74%</span></td>
                <td><span class="badge badge-neutral">+42.77%</span></td>
              </tr>
              <tr style="font-weight:700; background: rgba(59, 130, 246, 0.08);">
                <td><span class="tip" title="Operating Income (EBIT): Gross Profit minus Operating Expenses." data-tip="Operating Income (EBIT): Gross Profit ($1,356M) minus OpEx ($671M) = $685M. Reconciles exactly to Net Revenues ($1,424M) minus Total OpEx ($739M).">Operating Income (EBIT)</span></td>
                <td>$635.0</td>
                <td>$650.0</td>
                <td>$411.0</td>
                <td>$574.0</td>
                <td class="col-q0" style="font-weight:700; color:#34d399;">$685.0</td>
                <td class="col-est" style="font-weight:700; color:#60a5fa;">$730.0</td>
                <td><span class="badge badge-bull">+19.34%</span></td>
                <td><span class="badge badge-bull">+7.87%</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Operating Margin percentage." data-tip="Operating Margin: Operating Income divided by Total Net Revenues ($685M / $1,424M = 48.10%).">Operating Margin (%)</span></td>
                <td>49.84%</td>
                <td>50.66%</td>
                <td>38.52%</td>
                <td>43.88%</td>
                <td class="col-q0" style="font-weight:600; color:#34d399;">48.10%</td>
                <td class="col-est">48.67%</td>
                <td><span class="badge badge-bull">+422 bps</span></td>
                <td><span class="badge badge-bear">-174 bps</span></td>
              </tr>

              <!-- NET INCOME & EPS -->
              <tr style="border-top: 1px solid var(--border-color);">
                <td><span class="tip" title="GAAP Net Income attributable to Robinhood." data-tip="GAAP Net Income: Net profit attributable to Robinhood common stockholders ($476M reported, $468M common).">GAAP Net Income</span></td>
                <td>$556.0</td>
                <td>$605.0</td>
                <td>$350.0</td>
                <td>$561.0</td>
                <td class="col-q0" style="font-weight:600;">$476.0</td>
                <td class="col-est">$525.0</td>
                <td><span class="badge badge-bear">-15.15%</span></td>
                <td><span class="badge badge-bear">-14.39%</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="GAAP Diluted Earnings Per Share." data-tip="GAAP Diluted EPS: Net profit divided by diluted shares ($0.51 in Q3 2026).">GAAP Diluted EPS</span></td>
                <td>$0.61</td>
                <td>$0.66</td>
                <td>$0.38</td>
                <td>$0.62</td>
                <td class="col-q0" style="font-weight:600;">$0.51</td>
                <td class="col-est">$0.57</td>
                <td><span class="badge badge-bear">-17.74%</span></td>
                <td><span class="badge badge-bear">-16.39%</span></td>
              </tr>
              <tr style="font-weight:700;">
                <td><span class="tip" title="Non-GAAP Adjusted Diluted EPS." data-tip="Non-GAAP Adjusted EPS: Profitability per share before non-cash venture fund valuation markdowns ($0.60 in Q3 2026).">Adjusted Diluted EPS (Non-GAAP)</span></td>
                <td>$0.61</td>
                <td>$0.66</td>
                <td>$0.38</td>
                <td>$0.62</td>
                <td class="col-q0" style="font-weight:700; color:#34d399;">$0.60</td>
                <td class="col-est" style="font-weight:700; color:#60a5fa;">$0.65</td>
                <td><span class="badge badge-neutral">-3.23%</span></td>
                <td><span class="badge badge-neutral">-3.23%</span></td>
              </tr>

              <!-- CASH FLOW & FCF -->
              <tr style="border-top: 1px solid var(--border-color);">
                <td><span class="tip" title="Net cash provided by operating activities." data-tip="Operating Cash Flow: Operating cash generation ($1,225M in Q3 2026).">Operating Cash Flow (OCF)</span></td>
                <td>-$1,576.0</td>
                <td>-$937.0</td>
                <td>$2,038.0</td>
                <td>$720.0</td>
                <td class="col-q0" style="font-weight:600; color:#34d399;">$1,225.0</td>
                <td class="col-est">$1,100.0</td>
                <td><span class="badge badge-bull">+70.14%</span></td>
                <td><span class="badge badge-bull">+177.7%</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Capital Expenditures: Purchases of property and capitalized software." data-tip="CapEx: Equipment purchases and software capitalization ($21M in Q3 2026).">Capital Expenditures (CapEx)</span></td>
                <td>($12.0)</td>
                <td>($13.0)</td>
                <td>($18.0)</td>
                <td>($24.0)</td>
                <td class="col-q0" style="font-weight:600; color:#34d399;">($21.0)</td>
                <td class="col-est">($25.0)</td>
                <td><span class="badge badge-bull">-12.50%</span></td>
                <td><span class="badge badge-neutral">+75.00%</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Standard Reported Free Cash Flow: OCF minus CapEx." data-tip="Reported FCF: Operating cash flow minus capital expenditures ($1,225M - $21M = $1,204M in Q3 2026).">Reported Free Cash Flow</span></td>
                <td>-$1,588.0</td>
                <td>-$950.0</td>
                <td>$2,020.0</td>
                <td>$696.0</td>
                <td class="col-q0" style="font-weight:600; color:#34d399;">$1,204.0</td>
                <td class="col-est">$1,075.0</td>
                <td><span class="badge badge-bull">+72.99%</span></td>
                <td><span class="badge badge-bull">+175.8%</span></td>
              </tr>
              <tr>
                <td><span class="tip" title="Stock-Based Compensation." data-tip="Stock-Based Compensation: Non-cash equity compensation grants ($80M in Q3 2026).">Stock-Based Compensation (SBC)</span></td>
                <td>$78.0</td>
                <td>$76.0</td>
                <td>$92.0</td>
                <td>$105.0</td>
                <td class="col-q0" style="font-weight:600;">$80.0</td>
                <td class="col-est">$85.0</td>
                <td><span class="badge badge-bull">-23.81%</span></td>
                <td><span class="badge badge-neutral">+2.56%</span></td>
              </tr>
              <tr style="font-weight:700; background: rgba(16, 185, 129, 0.08);">
                <td><span class="tip" title="Forensic True Free Cash Flow: Reported FCF minus SBC minus Finance Leases." data-tip="True Free Cash Flow: Pure organic cash generation ($1,204M - $80M - $0M = $1,124M in Q3 2026).">Forensic True Free Cash Flow (ex-SBC)</span></td>
                <td>-$1,666.0</td>
                <td>-$1,026.0</td>
                <td>$1,928.0</td>
                <td>$591.0</td>
                <td class="col-q0" style="font-weight:700; color:#34d399;">$1,124.0</td>
                <td class="col-est" style="font-weight:700; color:#60a5fa;">$990.0</td>
                <td><span class="badge badge-bull">+90.19%</span></td>
                <td><span class="badge badge-bull">+167.5%</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 5. ROW 3: FORENSIC QUALITY-OF-EARNINGS & TRUE FCF BRIDGE (#sec-fcf) -->
    <section class="forensic-grid" id="sec-fcf" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Forensic Quality-of-Earnings &amp; True Free Cash Flow Bridge (Q3 2026)</div>
          <span class="badge badge-bull">$1,124M ORGANIC TRUE FCF</span>
        </div>
        <p style="font-size: 12.8px; color: var(--text-muted); margin-bottom: 14px;">
          Wall Street reported FCF frequently masks dilution from equity grants and off-balance sheet lease obligations. Our forensic bridge isolates exact cash generated from brokerage operations after deducting CapEx, non-cash Stock-Based Compensation ($80M), and finance leases ($0M).
        </p>

        <div class="waterfall-bridge" style="display: flex; flex-direction: column; gap: 8px;">
          <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(59, 130, 246, 0.08); border-radius: 6px;">
            <div>
              <strong>1. Net Cash Provided by Operating Activities (OCF)</strong>
              <div style="font-size: 11.5px; color: var(--text-muted);">Official SEC Form 8-K Statement of Cash Flows (3 Months Ended Sep 30, 2026)</div>
            </div>
            <div class="mono" style="font-size: 15px; font-weight: 700; color: #34d399;">+$1,225.0M</div>
          </div>

          <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(239, 68, 68, 0.06); border-radius: 6px;">
            <div>
              <strong>2. Less: Capital Expenditures (PPE &amp; Internal Software Capitalization)</strong>
              <div style="font-size: 11.5px; color: var(--text-muted);">$10M Purchases of property/equipment + $11M software capitalization</div>
            </div>
            <div class="mono" style="font-size: 15px; font-weight: 700; color: #f87171;">-$21.0M</div>
          </div>

          <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(59, 130, 246, 0.12); border-radius: 6px; font-weight: 700;">
            <div>
              <strong>= Standard Reported Free Cash Flow (FCF)</strong>
              <div style="font-size: 11.5px; color: var(--text-muted);">OCF ($1,225M) minus Total CapEx ($21M) = 84.55% FCF conversion</div>
            </div>
            <div class="mono" style="font-size: 15px; color: #34d399;">+$1,204.0M</div>
          </div>

          <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(239, 68, 68, 0.06); border-radius: 6px;">
            <div>
              <strong>3. Less: Stock-Based Compensation (SBC) Dilution</strong>
              <div style="font-size: 11.5px; color: var(--text-muted);">Disciplined equity comp: $80M (down -23.8% QoQ from $105M, 5.62% of net revenue)</div>
            </div>
            <div class="mono" style="font-size: 15px; font-weight: 700; color: #f87171;">-$80.0M</div>
          </div>

          <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(255, 255, 255, 0.03); border-radius: 6px;">
            <div>
              <strong>4. Less: Principal Payments on Finance Leases &amp; Debt</strong>
              <div style="font-size: 11.5px; color: var(--text-muted);">Zero finance lease principal obligations reported in cash flow statements</div>
            </div>
            <div class="mono" style="font-size: 15px; font-weight: 700; color: #94a3b8;">-$0.0M</div>
          </div>

          <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 6px; font-weight: 800;">
            <div>
              <strong style="color: #34d399; font-size: 14px;">= Forensic True Free Cash Flow (ex-SBC)</strong>
              <div style="font-size: 11.5px; color: #cbd5e1;">True organic cash generated by the business ready for buybacks and capital return</div>
            </div>
            <div class="mono" style="font-size: 17px; color: #34d399;">+$1,124.0M</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. ROW 4: WHAT MANAGEMENT DID RIGHT VS WRONG & CALL Q&A AUDIT (#sec-audit) -->
    <section class="audit-grid" id="sec-audit" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Execution Audit: What Management Got Right vs. What Went Wrong</div>
          <span class="badge badge-bull">STRONG STRATEGIC DELIVERY</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 20px;">
          <!-- WINS -->
          <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 6px; padding: 14px;">
            <div style="font-weight: 800; color: #34d399; font-size: 13.5px; margin-bottom: 8px;">✅ What Management Did Right (Operational Wins)</div>
            <ul style="margin: 0; padding-left: 18px; font-size: 12.8px; color: var(--text-secondary); line-height: 1.6;">
              <li><strong>Prediction Market Leadership:</strong> Scaled Event Contracts over 6x YoY to $173M in Q3, turning prediction markets into Robinhood's fastest-growing trading cylinder.</li>
              <li><strong>Expense Guidance Discipline:</strong> Lowered the top end of full-year 2026 Adjusted OpEx &amp; SBC guidance by $25M ($2.675B–$2.750B), demonstrating clear operating leverage.</li>
              <li><strong>Massive Cash &amp; FCF Generation:</strong> Delivered record $1,225M OCF and $1,124M True FCF, expanding total cash and segregated assets to $14.75B.</li>
              <li><strong>High-Net-Worth Traction:</strong> Added $16B in Q3 Net Deposits and announced October MTD deposits already exceeded $13B, including $6B from the Dell family to Trump Accounts.</li>
            </ul>
          </div>

          <!-- DRAGS -->
          <div style="background: rgba(239, 68, 68, 0.06); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 6px; padding: 14px;">
            <div style="font-weight: 800; color: #f87171; font-size: 13.5px; margin-bottom: 8px;">⚠️ What Management Got Wrong (Execution Drags)</div>
            <ul style="margin: 0; padding-left: 18px; font-size: 12.8px; color: var(--text-secondary); line-height: 1.6;">
              <li><strong>Cryptocurrency Volume Contraction:</strong> Crypto transaction revenues fell -55% YoY to $120M (vs $268M in Q3 2025), reflecting market-wide spot retail trading fatigue.</li>
              <li><strong>Headline GAAP EPS Confusion:</strong> A $67M (-$0.07/sh) non-cash mark-to-market loss on Robinhood Ventures Fund I caused headline GAAP EPS ($0.51) to optically miss Street consensus ($0.55).</li>
              <li><strong>Net Interest Income Headwind:</strong> Net interest revenue fell -9% YoY to $415M due to lower securities lending activity and lower short-term benchmark rates.</li>
              <li><strong>Post-Earnings Price Softness:</strong> The stock dropped -7.64% after-hours to $87.34 on fast-money profit taking following a +158% year-to-date run-up.</li>
            </ul>
          </div>
        </div>

        <h3 style="font-size: 14px; font-weight: 700; color: #f1f5f9; margin: 16px 0 10px 0;">
          Earnings Conference Call Forensic Highlights: Top 3 Analyst Questions &amp; Answers (Analyst Q&A)
        </h3>
{qa_cards_html}
      </div>
    </section>

    <!-- 7. ROW 5: POST-PRINT PEER GROUP VALUATION & MULTIPLES COMPS (#sec-comps) -->
    <section id="sec-comps" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Post-Print Peer Group Valuation &amp; Capital Markets Comps</div>
          <span class="badge badge-blue">RE-ANCHORED TO $87.34 AFTER-HOURS</span>
        </div>
        <p style="font-size: 12.8px; color: var(--text-muted); margin-bottom: 12px;">
          Valuation benchmarks updated against direct fintech, online brokerage, and crypto custody peers following Robinhood's Q3 2026 earnings release. Multiples re-anchored to $87.34 after-hours closing price.
        </p>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Ticker &amp; Company</th>
                <th>Price ($)</th>
                <th>Market Cap</th>
                <th>Enterprise Value</th>
                <th>Forward P/E</th>
                <th>TTM P/S</th>
                <th>EV / EBITDA</th>
                <th>Q3 Rev Growth YoY</th>
                <th>True FCF (ex-SBC)</th>
              </tr>
            </thead>
            <tbody>
              <tr style="font-weight: 700; background: rgba(59, 130, 246, 0.1);">
                <td style="color: #60a5fa;">HOOD (Robinhood Markets)</td>
                <td style="color: #f87171;">$87.34 (AH)</td>
                <td>$85.0B</td>
                <td>$84.1B</td>
                <td>27.69x</td>
                <td>17.51x</td>
                <td>26.5x</td>
                <td><span class="badge badge-bull">+11.77%</span></td>
                <td style="color: #34d399;">$1,124M</td>
              </tr>
              <tr>
                <td>SCHW (Charles Schwab Corp.)</td>
                <td>$75.50</td>
                <td>$138.2B</td>
                <td>$145.0B</td>
                <td>19.80x</td>
                <td>7.20x</td>
                <td>16.5x</td>
                <td><span class="badge badge-bull">+5.20%</span></td>
                <td>$1,450M</td>
              </tr>
              <tr>
                <td>COIN (Coinbase Global)</td>
                <td>$215.00</td>
                <td>$53.4B</td>
                <td>$48.2B</td>
                <td>34.50x</td>
                <td>11.20x</td>
                <td>28.2x</td>
                <td><span class="badge badge-bull">+78.00%</span></td>
                <td>$620M</td>
              </tr>
              <tr>
                <td>IBKR (Interactive Brokers)</td>
                <td>$148.00</td>
                <td>$62.1B</td>
                <td>$58.4B</td>
                <td>21.40x</td>
                <td>13.80x</td>
                <td>18.9x</td>
                <td><span class="badge badge-bull">+18.50%</span></td>
                <td>$850M</td>
              </tr>
              <tr>
                <td>SOFI (SoFi Technologies)</td>
                <td>$10.50</td>
                <td>$11.5B</td>
                <td>$14.2B</td>
                <td>38.00x</td>
                <td>4.80x</td>
                <td>22.0x</td>
                <td><span class="badge badge-bull">+20.10%</span></td>
                <td>$180M</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 8. ROW 6: 4-PILLAR POST-EARNINGS SENTIMENT & SOCIAL PULSE (#sec-sentiment) -->
    <section class="sentiment-grid" id="sec-sentiment" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>4-Pillar Post-Earnings Sentiment &amp; Microblogging Pulse</div>
          <span class="badge badge-bull">OVERALL SCORE: 76 / 100</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-bottom: 18px;">
          <!-- PILLAR 1 -->
          <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 6px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-weight: 700; font-size: 13px; color: #f1f5f9;">1. Retail &amp; Social Pulse</span>
              <span class="badge badge-bull">74 / 100</span>
            </div>
            <div class="sentiment-meter-bar" style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 8px;">
              <div style="width: 74%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <p style="font-size: 12.2px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
              r/wallstreetbets &amp; FinTwit traders actively buying the after-hours dip, highlighting event contract leadership and October deposit momentum.
            </p>
            <div style="font-size: 11.5px; color: var(--text-muted); font-style: italic;">
              "{soc_data['four_pillar_post_sentiment_scores']['pillar_1_retail_and_social_pulse']['top_quote']}"
            </div>
          </div>

          <!-- PILLAR 2 -->
          <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 6px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-weight: 700; font-size: 13px; color: #f1f5f9;">2. Sell-Side Flash Reactions</span>
              <span class="badge badge-bull">78 / 100</span>
            </div>
            <div class="sentiment-meter-bar" style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 8px;">
              <div style="width: 78%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <p style="font-size: 12.2px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
              Piper Sandler, Citizens JMP, and Mizuho reiterate Overweight ratings, pointing to disciplined FY26 expense ceiling reduction and Rothera scaling.
            </p>
            <div style="font-size: 11.5px; color: var(--text-muted); font-style: italic;">
              "{soc_data['four_pillar_post_sentiment_scores']['pillar_2_sellside_flash_reactions']['top_quote']}"
            </div>
          </div>

          <!-- PILLAR 3 -->
          <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 6px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-weight: 700; font-size: 13px; color: #f1f5f9;">3. Management Call Tone</span>
              <span class="badge badge-bull">85 / 100</span>
            </div>
            <div class="sentiment-meter-bar" style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 8px;">
              <div style="width: 85%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <p style="font-size: 12.2px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
              CEO Vlad Tenev and CFO Shiv Verma projected supreme confidence around multi-cylinder diversification, high-net-worth onboarding, and global expansion.
            </p>
            <div style="font-size: 11.5px; color: var(--text-muted); font-style: italic;">
              "{soc_data['four_pillar_post_sentiment_scores']['pillar_3_management_call_tone']['top_quote']}"
            </div>
          </div>

          <!-- PILLAR 4 -->
          <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 6px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-weight: 700; font-size: 13px; color: #f1f5f9;">4. Options Vol Crush &amp; Skew</span>
              <span class="badge badge-bull">70 / 100</span>
            </div>
            <div class="sentiment-meter-bar" style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 8px;">
              <div style="width: 70%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
            <p style="font-size: 12.2px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 6px;">
              After-hours decline of -7.64% stayed well inside the ±10.13% options implied straddle band, triggering rapid IV collapse from 86.13% to ~45%.
            </p>
            <div style="font-size: 11.5px; color: var(--text-muted); font-style: italic;">
              "{soc_data['four_pillar_post_sentiment_scores']['pillar_4_options_iv_crush_and_skew']['top_quote']}"
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 9. ROW 7: HEDGE FUND PM TRADE EXECUTION MATRIX (#sec-trade) -->
    <section class="scenario-grid" id="sec-trade" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>T+1 Hedge Fund PM Trade Execution Matrix (Anchored to $87.34 AH)</div>
          <span class="badge badge-bull">DISCIPLINED DIP-BUYING BLUEPRINT</span>
        </div>
        <p style="font-size: 12.8px; color: var(--text-muted); margin-bottom: 14px;">
          Asymmetric options structures and equity accumulation targets anchored to the post-earnings reference price ($87.34). Calibrated for the upcoming post-earnings opening bell.
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 14px;">
          <!-- BULL CASE -->
          <div class="scenario-bull" style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-weight: 800; color: #34d399; font-size: 14px;">🟢 BULL CASE (Price Target: $98.00–$105.00)</span>
              <span class="badge badge-bull">PROBABILITY: 55%</span>
            </div>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
              <strong>Catalyst Validation:</strong> The market digests the $0.60 adjusted EPS beat, realizes the GAAP miss was caused by a paper venture markdown, and bids HOOD back toward $98+ on surging October net deposits (&gt;$13B MTD) and election event contract volume.
            </p>
            <div class="trade-structure" style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #34d399; padding: 8px 10px; font-size: 12.2px; color: #f1f5f9; border-radius: 4px;">
              <strong>Actionable Options Structure:</strong> Buy <strong>Nov 20, 2026 $90 / $100 Bull Call Spread</strong> at open for ~$2.80 debit. Max profit ~$7.20 (+257% ROC) if HOOD recovers above $100 by November expiry.
            </div>
          </div>

          <!-- BASE CASE -->
          <div class="scenario-base" style="background: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-weight: 800; color: #60a5fa; font-size: 14px;">🔵 BASE CASE (Consolidation: $85.00–$92.00)</span>
              <span class="badge badge-blue">PROBABILITY: 30%</span>
            </div>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
              <strong>Sideways Churn:</strong> HOOD consolidates between $85 and $92 as fast-money rotation is absorbed by long-term institutional accumulation ahead of the November U.S. election trading volume climax.
            </p>
            <div class="trade-structure" style="background: rgba(59, 130, 246, 0.1); border-left: 3px solid #60a5fa; padding: 8px 10px; font-size: 12.2px; color: #f1f5f9; border-radius: 4px;">
              <strong>Actionable Options Structure:</strong> Sell <strong>Nov 20, 2026 $80 Cash-Secured Puts</strong> for ~$2.10 credit, effectively acquiring shares at $77.90 cost basis or capturing 2.6% yield in 24 days.
            </div>
          </div>

          <!-- BEAR CASE -->
          <div class="scenario-bear" style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-weight: 800; color: #f87171; font-size: 14px;">🔴 BEAR CASE (Downside Support: $76.00)</span>
              <span class="badge badge-bear">PROBABILITY: 15%</span>
            </div>
            <p style="font-size: 12.8px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
              <strong>Downside Breakdown:</strong> Persistent weakness in crypto retail trading volume (-55% YoY) and further regulatory scrutiny on prediction markets cause a breakdown below the 50-day moving average toward $76 support.
            </p>
            <div class="trade-structure" style="background: rgba(239, 68, 68, 0.1); border-left: 3px solid #f87171; padding: 8px 10px; font-size: 12.2px; color: #f1f5f9; border-radius: 4px;">
              <strong>Actionable Options Structure:</strong> Buy <strong>Nov 20, 2026 $82.50 / $75.00 Bear Put Spread</strong> only if HOOD loses the $85.00 support level on heavy volume at the open.
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- VERBATIM GROUND-TRUTH GROUNDING LEDGER -->
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 10px 14px; font-size: 12px; color: var(--text-muted); margin-top: 10px; margin-bottom: 14px;">
      <strong>Deterministic Grounding Verification:</strong> Regular Close Price: <span class="mono" style="color:#f8fafc;">${reg_price:.2f}</span> • After-Hours Price: <span class="mono" style="color:#34d399;">${ah_price:.2f}</span> • Reported Q3 2026 Net Revenues: <span class="mono" style="color:#60a5fa;">$1,424M</span> • Reported Q3 2026 Operating Cash Flow (OCF): <span class="mono" style="color:#34d399;">$1,225M</span> • Standard Reported FCF: <span class="mono" style="color:#fcd34d;">${q0_rep_fcf:,.0f}M</span> • Forensic True Free Cash Flow: <span class="mono" style="color:#34d399;">${q0_true_fcf:,.0f}M</span> • Post-Print Move: <span class="mono" style="color:#f87171;">{post_move_pct:+.2f}%</span> vs Expected <span class="mono">±{opt_implied_pct:.2f}%</span>.
    </div>

    <!-- 10. FOOTER -->
    <div class="footer-meta">
      <div>
        <span>SEC EDGAR CIK: <strong>0001783879</strong></span> • 
        <span>Q3 2026 Form 8-K Filed: <strong>Tuesday, Oct 27, 2026 (Exhibit 99.1 Press Release)</strong></span> • 
        <span>Reporting Currency: <strong>USD ($ Millions)</strong></span>
      </div>
      <div style="margin-top:6px;">
        Deterministic Post-Earnings Ground Truth Anchored via SEC Form 8-K &amp; 10-Q Filings • Generated with Antigravity Zero-Hallucination T+0 Post-Earnings Harness
      </div>
    </div>
"""

draft_payload = {
    "header": {
        "page_title": f"HOOD (${ah_price:.2f}) Q3 2026 Post-Earnings Forensic & Sentiment Tearsheet",
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
print(f"[SUCCESS] Generated Post-Earnings Draft for HOOD at: {DRAFT_PATH.name}")
print(f"  - Inner HTML Character Count: {len(container_html):,}")
print(f"  - Interactive Tooltip Count (.tip): {container_html.count('class=\"tip')}")
print(f"  - Data-Tip Count (data-tip=): {container_html.count('data-tip=\"')}")
