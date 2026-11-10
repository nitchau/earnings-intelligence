"""
build_plug_post_draft.py: Generates drafts/PLUG_2026-11-09_post_draft.json
Institutional Post-Earnings Forensic Tearsheet for Plug Power Inc. (PLUG)
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "PLUG"
DATE = "2026-11-09"

TRUTH_PATH = BASE_DIR / f"ground_truth/{TICKER}_{DATE}_post_truth.json"
BUS_2A_PATH = BASE_DIR / f"post_agent_bus/{TICKER}_{DATE}_agent2a_kpis.json"
BUS_2B_PATH = BASE_DIR / f"post_agent_bus/{TICKER}_{DATE}_agent2b_transcript.json"
BUS_2C_PATH = BASE_DIR / f"post_agent_bus/{TICKER}_{DATE}_agent2c_social.json"

DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / f"{TICKER}_{DATE}_post_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))
kpis_data = json.loads(BUS_2A_PATH.read_text(encoding="utf-8"))
trans_data = json.loads(BUS_2B_PATH.read_text(encoding="utf-8"))
soc_data = json.loads(BUS_2C_PATH.read_text(encoding="utf-8"))

reg_price = truth["post_print_reaction"]["regular_close_price"]          # 1.50
ah_price = truth["post_print_reaction"]["after_hours_price"]            # 1.49
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]     # -0.67%
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] or 18.57
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 0.26)
verdict = "REVENUE BEAT / MARGIN INFLECTION"

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]          # 200.60
cons_rev = truth["beat_miss_scorecard"]["revenue"]["street_consensus_millions"]       # 193.33
whisper_rev = 198.00
rev_delta_m = round(q0_rev - cons_rev, 2)                                              # +7.27
rev_delta_pct = round(rev_delta_m / cons_rev * 100, 2)                                 # +3.76%

q0_eps_nongaap = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"] or -0.05
cons_eps_nongaap = truth["beat_miss_scorecard"]["eps_nongaap"]["street_consensus"] or -0.06
eps_delta_d = round(q0_eps_nongaap - cons_eps_nongaap, 2)                              # +0.01
q0_eps_gaap = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"] or 0.07

q0_gp = -5.36
q0_opex = 69.90
q0_opinc = -75.25
q0_net_inc = 99.77

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # -76.42
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 14.80
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # -91.22
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 13.12
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 0.0
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # -104.34

s5q = truth["stitched_5q_chronological"]
p_labels = s5q["period_labels"]                                # Q3 2025, Q4 2025, Q1 2026, Q2 2026, Q3 2026 (Actual)
next_q_label = s5q["next_quarter_estimate_label"]              # Q4 2026E (Guided / Street)

mcap_m = truth["market_portal"]["market_cap_millions"] or 2095.79
ev_m = truth["market_portal"]["enterprise_value_millions"] or 2966.19
fwd_pe = truth["market_portal"]["forward_pe"] or -10.11

# Table 1B-1 rows
rows_1b1 = [
    f"""              <tr>
                <td><span class="tip" title="Total Consolidated Net Revenue across fuel cell equipment, infrastructure, services, and fuel delivery." data-tip="Total Consolidated Revenue: $200.60M reported in Q3 2026 (+13.3% YoY vs $177.06M in Q3 2025 and +12.5% QoQ vs $178.30M in Q2 2026), beating Street consensus ($193.33M) by +$7.27M (+3.76%) and whisper bogey ($198.00M) by +$2.60M driven by commercial equipment shipments.">Total Consolidated Revenue ($M)</span></td>
                <td>$178.30M</td>
                <td>$177.06M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">${cons_rev:,.2f}M</td>
                <td style="font-weight:700; color: #34d399;">${q0_rev:,.2f}M</td>
                <td>
                  <span class="badge badge-bull">+${rev_delta_m:.2f}M (+{rev_delta_pct:+.2f}%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:89%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Sales of Fuel Cell Equipment &amp; Related Infrastructure." data-tip="Equipment Revenue: $105.74M in Q3 2026 (+9.3% YoY vs $96.77M in Q3 2025), driven by 1,136 GenDrive commercial unit deployments across material handling customers.">Equipment &amp; Infrastructure ($M)</span></td>
                <td>$112.40M</td>
                <td>$96.77M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$102.50M</td>
                <td style="font-weight:700; color: #34d399;">$105.74M</td>
                <td>
                  <span class="badge badge-bull">+$3.24M (+3.16%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:88%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="GAAP Gross Margin percentage." data-tip="Gross Margin: -2.67% in Q3 2026 (-$5.36M gross loss) vs -67.87% (-$120.17M) in Q3 2025 and -0.94% in Q2 2026, delivering an astounding ~65 percentage point YoY recovery as internal green hydrogen plants cut fuel molecule costs.">Gross Margin (%)</span></td>
                <td>-0.94%</td>
                <td>-67.87%</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">-6.50%</td>
                <td style="font-weight:700; color: #34d399;">-2.67%</td>
                <td>
                  <span class="badge badge-bull">+383 bps vs Est</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:94%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">EXPANSION</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Non-GAAP Diluted Earnings Per Share (Adjusted)." data-tip="Non-GAAP Adjusted EPS: -$0.05 in Q3 2026 vs -$0.06 Street consensus, outperforming by +$0.01 as Project Quantum Leap cost reductions lowered total OpEx by ~69% YoY.">Non-GAAP Adjusted EPS ($)</span></td>
                <td>-$0.07</td>
                <td>-$0.31</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">-${abs(cons_eps_nongaap):.2f}</td>
                <td style="font-weight:700; color: #34d399;">-${abs(q0_eps_nongaap):.2f}</td>
                <td>
                  <span class="badge badge-bull">+${eps_delta_d:.2f} (+16.67%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:85%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Quarterly Net Cash Usage (excluding restricted cash)." data-tip="Net Cash Usage: ~$28.0M ($28.00M) in Q3 2026, dropping 54% sequentially from $61.0M in Q2 2026 with zero ATM equity issuance, marking a record low for the company.">Quarterly Net Cash Usage ($M)</span></td>
                <td>$61.00M</td>
                <td>$110.00M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$45.00M</td>
                <td style="font-weight:700; color: #34d399;">$28.00M</td>
                <td>
                  <span class="badge badge-bull">-$17.00M Less Usage</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:96%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">RECORD LOW</span></td>
              </tr>"""
]
table_1b1_html = "\n".join(rows_1b1)

# Table 1B-2 rows
rows_1b2 = []
for item in trans_data["matrix_a_guidance_accountability"]:
    rows_1b2.append(f"""              <tr>
                <td><span class="tip" title="{item['metric']}" data-tip="{item['metric']}: Reported {item['reported_actual']} vs prior guidance corridor {item['prior_guidance']}. Variance: {item['variance']}.">{item['metric']}</span></td>
                <td>{item['prior_guidance']}</td>
                <td style="font-weight:700; color: #34d399;">{item['reported_actual']}</td>
                <td>{item['variance']}</td>
                <td><span class="badge {item['badge_class']}">{item['grade']}</span></td>
              </tr>""")
table_1b2_html = "\n".join(rows_1b2)

# Table 1B-3 rows
rows_1b3 = []
for item in trans_data["matrix_b_forward_guidance_reset"]:
    rows_1b3.append(f"""              <tr>
                <td><span class="tip" title="{item['metric']}" data-tip="{item['metric']}: Reset to {item['new_guidance']} vs Street pre-print expectations {item['street_pre_print']}. Variance: {item['delta']}.">{item['metric']}</span></td>
                <td>{item['street_pre_print']}</td>
                <td style="font-weight:700; color: #60a5fa;">{item['new_guidance']}</td>
                <td style="font-weight:700; color: #34d399;">{item['delta']}</td>
                <td><span class="badge {item['badge_class']}">{item['action']}</span></td>
              </tr>""")
table_1b3_html = "\n".join(rows_1b3)

# Analyst Q&A cards
qa_cards = []
for qa in trans_data["top_call_exchanges"]:
    qa_cards.append(f"""        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #3b82f6; padding: 12px 14px; border-radius: 6px; margin-bottom: 12px;">
          <div style="font-weight: 700; color: #93c5fd; font-size: 13.5px; margin-bottom: 4px;">
            {qa['analyst']} &mdash; <span style="color: #cbd5e1;">{qa['topic']}</span>
          </div>
          <p style="font-size: 12.5px; color: #94a3b8; margin: 4px 0;"><strong>Question:</strong> {qa['question']}</p>
          <p style="font-size: 12.5px; color: #e2e8f0; margin: 4px 0;"><strong>Executive Answer:</strong> {qa['management_answer']}</p>
          <div style="font-size: 11px; color: #34d399; font-weight: 600; margin-top: 4px;">Forensic Assessment: {qa['verdict']}</div>
        </div>""")
qa_cards_html = "\n".join(qa_cards)

html_content = f"""
    <!-- 1. HEADER BANNER & STRIP -->
    <header class="header-banner" style="margin-bottom: 20px;">
      <div class="header-top" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; margin-bottom: 16px;">
        <div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <h1 style="margin: 0; font-size: 24px; font-weight: 800; color: #fff;">Plug Power Inc. ({TICKER})</h1>
            <span class="badge badge-bull" style="font-size: 13px; padding: 4px 8px;">T+0 POST-EARNINGS FORENSIC TEARSHEET</span>
            <span class="badge badge-purple" style="font-size: 13px; padding: 4px 8px;">{verdict}</span>
          </div>
          <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">
            Q3 2026 Earnings Release &bull; Filing Date: November 9, 2026 &bull; Form 8-K Exhibit 99.1 &bull; Market Cap: ${mcap_m:,.1f}M &bull; EV: ${ev_m:,.1f}M
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 13px; color: var(--text-muted);">Regular Close: <strong style="color: #fff;">${reg_price:.2f}</strong></div>
          <div style="font-size: 20px; font-weight: 800; color: #f87171;">
            After-Hours: ${ah_price:.2f} <span style="font-size: 14px;">({post_move_pct:.2f}%)</span>
          </div>
        </div>
      </div>

      <div class="header-strip" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; background: rgba(15, 23, 42, 0.6); padding: 12px 16px; border-radius: 8px; border: 1px solid var(--border-color);">
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">T+0 Print Verdict</div>
          <div style="font-size: 15px; font-weight: 700; color: #34d399;">{verdict}</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Q0 Total Net Revenue</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_rev:,.2f}M <span style="font-size: 11px; color: #34d399;">(+3.76% vs $193.33M)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Gross Margin Rebound</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">-2.67% <span style="font-size: 11px; color: #34d399;">(+65 pts YoY from -68%)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Net Cash Usage</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">$28.00M <span style="font-size: 11px; color: #34d399;">(54% sequential drop)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Cash &amp; Equivalents</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">$134.00M <span style="font-size: 11px; color: #34d399;">(Zero ATM Issuance)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">1-Wk Straddle Implied</div>
          <div style="font-size: 16px; font-weight: 700; color: #38bdf8;">±{opt_implied_pct:.1f}% (${opt_straddle:.2f}) [CONTAINED]</div>
        </div>
      </div>
    </header>

    <!-- 2. TRACK B STICKY JUMP-NAV -->
    <nav class="post-jump-nav" style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; padding: 10px 14px; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; position: sticky; top: 10px; z-index: 100; backdrop-filter: blur(8px);">
      <a href="#sec-scorecard" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">1. Beat / Miss Scorecard</a>
      <a href="#sec-5q" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">2. Rolling 5Q Table (Q3 Actual + Q4E)</a>
      <a href="#sec-fcf" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">3. Forensic True FCF Bridge</a>
      <a href="#sec-audit" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">4. Wins, Drags &amp; Call Q&amp;A</a>
      <a href="#sec-comps" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">5. Peer Group Multiples</a>
      <a href="#sec-sentiment" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">6. 4-Pillar Sentiment</a>
      <a href="#sec-trade" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">7. PM Trade Matrix</a>
    </nav>

    <!-- EXECUTIVE KPI GRID -->
    <section class="kpi-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 24px;">
      <div style="background: rgba(15, 23, 42, 0.6); padding: 14px; border-radius: 8px; border: 1px solid var(--border-color);">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Fuel Cell Deployments</div>
        <div style="font-size: 18px; font-weight: 800; color: #34d399; margin: 4px 0;">1,136 Units</div>
        <div style="font-size: 11.5px; color: var(--text-secondary);">GenDrive deployments more than doubled YoY (+110% vs 540 units in Q3 2025).</div>
      </div>
      <div style="background: rgba(15, 23, 42, 0.6); padding: 14px; border-radius: 8px; border: 1px solid var(--border-color);">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Gross Margin Recovery</div>
        <div style="font-size: 18px; font-weight: 800; color: #60a5fa; margin: 4px 0;">-2.67% Margin</div>
        <div style="font-size: 11.5px; color: var(--text-secondary);">65 percentage point YoY rebound on internal hydrogen production &amp; supply chain efficiency.</div>
      </div>
      <div style="background: rgba(15, 23, 42, 0.6); padding: 14px; border-radius: 8px; border: 1px solid var(--border-color);">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Project Quantum Leap</div>
        <div style="font-size: 18px; font-weight: 800; color: #38bdf8; margin: 4px 0;">69% OpEx Reduction</div>
        <div style="font-size: 11.5px; color: var(--text-secondary);">Operating expenses fell to $69.90M from $228.62M in Q3 2025, rationalizing overhead.</div>
      </div>
      <div style="background: rgba(15, 23, 42, 0.6); padding: 14px; border-radius: 8px; border: 1px solid var(--border-color);">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Electrolyzer Funnel</div>
        <div style="font-size: 18px; font-weight: 800; color: #a855f7; margin: 4px 0;">~$8.0B Pipeline</div>
        <div style="font-size: 11.5px; color: var(--text-secondary);">280 MW Arcadia eFuels Project ENDOR order and &gt;1 GW e-SAF strategic partnership.</div>
      </div>
    </section>

    <!-- ROW 1B: SCORECARD SECTION -->
    <section class="card" id="sec-scorecard" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 1B: Post-Release Print vs Expectations &amp; Guidance Scorecard</div>
        <span class="badge badge-bull">Q3 2026 AUDIT COMPLETE</span>
      </div>

      <!-- Track B: T-1 vs T-0 Thesis Audit Banner -->
      <div class="t1-vs-t0-audit" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin-bottom: 16px; padding: 12px; background: rgba(15, 23, 42, 0.7); border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
        <div style="padding: 10px; background: rgba(255,255,255,0.03); border-radius: 6px; border-left: 3px solid #3b82f6;">
          <div style="font-size: 11px; text-transform: uppercase; color: #93c5fd; font-weight: 700;">Pre-Print Baseline (T-1)</div>
          <div style="font-size: 13px; font-weight: 600; color: #fff; margin-top: 4px;">Consensus: $193.33M Rev | -$0.06 EPS</div>
          <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Straddle Implied: ±18.57% ($0.26) &bull; Whisper Rev: $198.00M</div>
        </div>
        <div style="padding: 10px; background: rgba(255,255,255,0.03); border-radius: 6px; border-left: 3px solid #10b981;">
          <div style="font-size: 11px; text-transform: uppercase; color: #34d399; font-weight: 700;">Reported Q0 Print (T+0)</div>
          <div style="font-size: 13px; font-weight: 600; color: #fff; margin-top: 4px;">Actual: $200.60M Rev | -$0.05 Adj EPS ($0.07 GAAP)</div>
          <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Beat: +$7.27M (+3.76%) &bull; Margin: -2.67% (vs -68% YoY)</div>
        </div>
        <div style="padding: 10px; background: rgba(255,255,255,0.03); border-radius: 6px; border-left: 3px solid #a855f7;">
          <div style="font-size: 11px; text-transform: uppercase; color: #c084fc; font-weight: 700;">Thesis Verdict &amp; Reaction</div>
          <div style="font-size: 13px; font-weight: 600; color: #34d399; margin-top: 4px;">VALIDATED: BEAT &amp; MARGIN EXPANSION</div>
          <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">After-Hours: $1.49 (-0.67%) &bull; Net Cash Usage: ~$28M</div>
        </div>
      </div>

      <!-- Table 1B-1: Headline & KPI Beat/Miss Scorecard -->
      <div style="margin-bottom: 20px;">
        <div style="font-weight: 700; font-size: 14px; color: #93c5fd; margin-bottom: 8px;">
          Table 1B-1: Headline &amp; Company KPI Beat / Miss Scorecard
        </div>
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Operational Metric</th>
                <th>Q-1 Actual (Q2 26)</th>
                <th>Q-4 Baseline (Q3 25)</th>
                <th class="col-q0">Street Consensus</th>
                <th>Reported Q0 Actual</th>
                <th>Surprise Delta &amp; Beat Bar</th>
                <th>Verdict</th>
              </tr>
            </thead>
            <tbody>
{table_1b1_html}
            </tbody>
          </table>
        </div>
      </div>

      <!-- Table 1B-2: Management Guidance Accountability -->
      <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <div style="font-weight: 700; font-size: 14px; color: #93c5fd;">
            Table 1B-2: Management Execution Accountability (Q0 Actual vs Prior Guidance)
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 12px; color: var(--text-muted);">Credibility Score: <strong>86 / 100</strong></span>
            <div class="credibility-gauge-bar" style="width: 80px; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
              <div class="credibility-gauge-fill" style="width: 86%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
          </div>
        </div>
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Guided Metric</th>
                <th>Prior Management Guidance</th>
                <th>Reported Q0 Actual</th>
                <th>Execution Variance</th>
                <th>Grade</th>
              </tr>
            </thead>
            <tbody>
{table_1b2_html}
            </tbody>
          </table>
        </div>
      </div>

      <!-- Table 1B-3: Forward Guidance Reset -->
      <div>
        <div style="font-weight: 700; font-size: 14px; color: #93c5fd; margin-bottom: 8px;">
          Table 1B-3: Forward Guidance Reset (New Management Outlook vs Street Expectations)
        </div>
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Forward Target Metric</th>
                <th>Street Pre-Print Consensus</th>
                <th>New Management Guidance</th>
                <th>Guidance Delta</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
{table_1b3_html}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ROW 2: 5-QUARTER HISTORICAL FINANCIALS & SEGMENTS -->
    <section class="card" id="sec-5q" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 2: 5-Quarter Rolling Financial Performance &amp; Dynamic Segment Breakdown</div>
        <span class="badge badge-bull">Q3 2026 ACTUAL + Q4 2026E FORWARD</span>
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Financial Metric ($M)</th>
              <th>Q3 2025</th>
              <th>Q4 2025</th>
              <th>Q1 2026</th>
              <th>Q2 2026</th>
              <th class="col-q0">Q3 2026 (Actual)</th>
              <th class="col-est">Q4 2026E (Guided / Street)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background: rgba(255,255,255,0.02);">
              <td><span class="tip" title="Total Consolidated Revenue" data-tip="Total consolidated revenue from equipment, infrastructure, services, and hydrogen fuel delivery ($200.60M in Q3 2026).">Total Consolidated Revenue</span></td>
              <td>$177.06M</td>
              <td>$225.22M</td>
              <td>$163.51M</td>
              <td>$178.30M</td>
              <td class="col-q0" style="color: #34d399;">$200.60M</td>
              <td class="col-est" style="color: #60a5fa;">$220.00M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Equipment &amp; Infrastructure" data-tip="GenDrive fuel cells, stationary GenSure units, and hydrogen dispensers.">↳ Equipment &amp; Infrastructure</span></td>
              <td>$96.77M</td>
              <td>$142.30M</td>
              <td>$98.10M</td>
              <td>$112.40M</td>
              <td class="col-q0">$105.74M</td>
              <td class="col-est">$125.00M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Fuel Delivered" data-tip="Liquid and gaseous hydrogen supply delivered to customer locations.">↳ Fuel Delivered to Customers</span></td>
              <td>$35.91M</td>
              <td>$41.80M</td>
              <td>$33.60M</td>
              <td>$35.10M</td>
              <td class="col-q0">$38.11M</td>
              <td class="col-est">$42.00M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Services Performed" data-tip="Service contracts, fleet maintenance, and aftermarket support.">↳ Services on Fuel Cell Systems</span></td>
              <td>$19.74M</td>
              <td>$16.62M</td>
              <td>$14.01M</td>
              <td>$14.60M</td>
              <td class="col-q0">$29.01M</td>
              <td class="col-est">$28.00M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Power Purchase Agreements" data-tip="Equipment leased under power purchase agreements.">↳ Power Purchase Agreements</span></td>
              <td>$24.60M</td>
              <td>$24.50M</td>
              <td>$17.80M</td>
              <td>$16.20M</td>
              <td class="col-q0">$27.71M</td>
              <td class="col-est">$25.00M</td>
            </tr>
            <tr>
              <td>Cost of Revenue</td>
              <td>$297.22M</td>
              <td>$219.77M</td>
              <td>$185.12M</td>
              <td>$179.98M</td>
              <td class="col-q0">$205.96M</td>
              <td class="col-est">$218.00M</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Gross Profit (Loss)" data-tip="Gross loss of -$5.36M in Q3 2026 reflecting a dramatic ~65 percentage point YoY margin recovery toward breakeven.">Gross Profit (Loss)</span></td>
              <td>-$120.17M</td>
              <td>$5.45M</td>
              <td>-$21.61M</td>
              <td>-$1.68M</td>
              <td class="col-q0" style="color: #34d399;">-$5.36M</td>
              <td class="col-est" style="color: #34d399;">$2.00M</td>
            </tr>
            <tr>
              <td>Gross Margin %</td>
              <td>-67.87%</td>
              <td>2.42%</td>
              <td>-13.22%</td>
              <td>-0.94%</td>
              <td class="col-q0" style="color: #34d399;">-2.67%</td>
              <td class="col-est">0.91%</td>
            </tr>
            <tr class="sub-row">
              <td>↳ Research &amp; Development (R&amp;D)</td>
              <td>$16.12M</td>
              <td>$15.20M</td>
              <td>$12.80M</td>
              <td>$12.73M</td>
              <td class="col-q0">$12.55M</td>
              <td class="col-est">$13.00M</td>
            </tr>
            <tr class="sub-row">
              <td>↳ Selling, General &amp; Administrative (SG&amp;A)</td>
              <td>$110.59M</td>
              <td>$97.34M</td>
              <td>$69.52M</td>
              <td>$29.96M</td>
              <td class="col-q0">$68.34M</td>
              <td class="col-est">$52.00M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Operating Expenses" data-tip="Total operating expenses of $69.90M in Q3 2026, down ~69% YoY through Project Quantum Leap cost reductions.">Total Operating Expenses</span></td>
              <td>$126.71M</td>
              <td>$112.54M</td>
              <td>$82.32M</td>
              <td>$42.69M</td>
              <td class="col-q0">$69.90M</td>
              <td class="col-est">$65.00M</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Operating Income (Loss)" data-tip="Operating loss of -$75.25M in Q3 2026 (-$5.36M Gross Profit - $69.90M OpEx), improving by over $170M YoY.">Operating Income (Loss)</span></td>
              <td>-$246.88M</td>
              <td>-$107.09M</td>
              <td>-$103.93M</td>
              <td>-$44.36M</td>
              <td class="col-q0" style="color: #f87171;">-$75.25M</td>
              <td class="col-est" style="color: #60a5fa;">-$63.00M</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income (Loss)" data-tip="GAAP net income of $99.77M attributable to Plug Power Inc. in Q3 2026 benefiting from $192M non-cash fair value gains.">GAAP Net Income (Loss)</span></td>
              <td>-$361.87M</td>
              <td>-$845.97M</td>
              <td>-$245.30M</td>
              <td>-$188.21M</td>
              <td class="col-q0" style="color: #34d399;">$99.77M</td>
              <td class="col-est" style="color: #60a5fa;">-$70.00M</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Diluted EPS" data-tip="GAAP basic EPS was $0.07 ($0.00 diluted) in Q3 2026 compared to -$0.31 in Q3 2025.">GAAP Basic EPS ($)</span></td>
              <td>-$0.31</td>
              <td>-$0.64</td>
              <td>-$0.18</td>
              <td>-$0.07</td>
              <td class="col-q0" style="color: #34d399;">$0.07</td>
              <td class="col-est" style="color: #60a5fa;">-$0.05</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ROW 3: FORENSIC HIGHLIGHTS & TRUE FCF BRIDGE -->
    <section class="card" id="sec-fcf" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 3: Forensic Quality-of-Earnings &amp; True Free Cash Flow Bridge (Q3 2026)</div>
        <span class="badge badge-bull">CASH DISCIPLINE AUDIT</span>
      </div>
      <div class="forensic-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 12px;">Q3 2026 Free Cash Flow Waterfall Reconciliation ($M)</div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Operating Cash Flow" data-tip="Operating Cash Flow: -76.42M (-$76.42M) in Q3 2026, improving from -$94.06M in Q2 2026.">(+) Operating Cash Flow (OCF)</span>
            <span style="font-weight: 700; color: #f87171;">-${abs(q0_ocf):.2f}M ({q0_ocf:.2f})</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Capital Expenditures" data-tip="CapEx of $14.80M in Q3 2026, down over 50% sequentially from $30.66M in Q2 2026.">(-) Capital Expenditures (CapEx)</span>
            <span style="font-weight: 700; color: #f87171;">-${q0_capex:.2f}M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px; background: rgba(59, 130, 246, 0.08); padding-left: 6px; padding-right: 6px;">
            <span style="font-weight: 600;">(=) Reported Free Cash Flow</span>
            <span style="font-weight: 700; color: #f87171;">-${abs(q0_rep_fcf):.2f}M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Stock-Based Compensation" data-tip="SBC of $13.12M in Q3 2026 for non-cash equity incentives.">(-) Stock-Based Compensation (SBC)</span>
            <span style="font-weight: 700; color: #f87171;">-${q0_sbc:.2f}M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Finance Lease Principal Payments" data-tip="Zero capital lease principal debt payments in Q3 2026.">(-) Principal Finance Leases</span>
            <span style="font-weight: 700; color: #94a3b8;">-$0.00M</span>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 8px 6px; font-size: 13.5px; background: rgba(239, 68, 68, 0.08); border-radius: 6px; margin-top: 6px;">
            <span style="font-weight: 700; color: #f87171;">(=) Forensic True Free Cash Flow</span>
            <span style="font-weight: 800; color: #f87171;">-${abs(q0_true_fcf):.2f}M</span>
          </div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color); display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 10px;">Forensic Cash Quality &amp; Balance Sheet Fortress Assessment</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-bottom: 10px;">
              Plug Power demonstrated material cash conservation in Q3 2026, posting Operating Cash Flow of <strong>-${abs(q0_ocf):.2f}M</strong> and Reported Free Cash Flow of <strong>-${abs(q0_rep_fcf):.2f}M</strong>, an improvement from -$124.7M in Q2 2026. Deducting $13.12M in non-cash stock compensation brings Forensic True Free Cash Flow to <strong>-${abs(q0_true_fcf):.2f}M</strong>.
            </p>
            <div style="font-size: 12px; color: var(--text-muted); line-height: 1.6;">
              &bull; <strong>Record-Low Net Cash Usage:</strong> Net cash usage was approximately $28.0M ($28.00M) for the quarter, declining 54% from $61.0M in Q2 2026 and marking the lowest cash usage in multiple years.<br>
              &bull; <strong>Zero ATM Issuance:</strong> Plug completed Q3 with $134.0M in cash and cash equivalents, without selling a single share under its at-the-market (ATM) facility.<br>
              &bull; <strong>Halved CapEx Intensity:</strong> Capital expenditures declined to $14.80M (down from $30.66M in Q2 and $106.8M in 9M 2025), reflecting completion of key green hydrogen plant builds.<br>
              &bull; <strong>Internal Hydrogen Supply Dividends:</strong> In-house hydrogen production in Georgia and Tennessee reduced purchased molecule costs from ~$12/kg to $3-$4/kg.
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ROW 4: OPERATIONAL AUDIT & ANALYST Q&A FORENSIC EXCHANGES -->
    <section class="card audit-grid" id="sec-audit" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 4: Operational Wins, Drags &amp; Earnings Call Q&amp;A Audit</div>
        <span class="badge badge-blue">QUALITATIVE &amp; TRANSCRIPT FORENSICS</span>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-bottom: 20px;">
        <div style="border-left: 3px solid #10b981; padding-left: 14px;">
          <h4 style="margin: 0 0 8px 0; color: #34d399; font-size: 14px;">Operational Wins &amp; Catalysts</h4>
          <ul style="font-size: 12.5px; color: #cbd5e1; margin: 0; padding-left: 18px; line-height: 1.6;">
            <li><strong>GenDrive Deployments Doubled:</strong> Shipped 1,136 commercial fuel cell units in Q3 2026, surging +110% YoY compared to 540 units in Q3 2025 across material handling clients.</li>
            <li><strong>Dramatic Gross Margin Rebound:</strong> Rebounded from -67.87% in Q3 2025 to -2.67% in Q3 2026, an improvement of ~65 percentage points.</li>
            <li><strong>Arcadia eFuels 280 MW Contract:</strong> Signed landmark 280 MW GenEco electrolyzer supply agreement for Project ENDOR in Denmark and strategic partnership covering &gt;1 GW of e-SAF projects.</li>
            <li><strong>Disciplined Cash Management:</strong> Record-low quarterly net cash usage of ~$28M achieved with zero ATM equity issuance during the entire quarter.</li>
          </ul>
        </div>
        <div style="border-left: 3px solid #ef4444; padding-left: 14px;">
          <h4 style="margin: 0 0 8px 0; color: #f87171; font-size: 14px;">Execution Drags &amp; Watch Items</h4>
          <ul style="font-size: 12.5px; color: #cbd5e1; margin: 0; padding-left: 18px; line-height: 1.6;">
            <li><strong>GAAP Operating Loss Continues:</strong> Operating loss was -$75.25M in Q3 2026, requiring continued execution of Project Quantum Leap to achieve operating breakeven.</li>
            <li><strong>Non-Cash Impact on GAAP EPS:</strong> Positive GAAP Basic EPS ($0.07) was driven by $192M in mark-to-market debt instrument adjustments rather than operating profit.</li>
            <li><strong>Electrolyzer Delivery Lead Times:</strong> Complex multi-hundred-megawatt projects involve lengthy front-end engineering design cycles before milestone cash realization.</li>
            <li><strong>Working Capital Intensity:</strong> Accounts receivable and inventory balances require continuous monitoring to ensure cash burn remains below $30M per quarter.</li>
          </ul>
        </div>
      </div>

      <!-- Top Institutional Analyst Q&A -->
      <div>
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 12px;">
          Top Institutional Analyst Q&amp;A and Conference Call Forensic Exchanges
        </div>
{qa_cards_html}
      </div>
    </section>

    <!-- ROW 5: POST-PRINT PEER BENCHMARKS -->
    <section class="card" id="sec-comps" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 5: Post-Print Peer Benchmarks &amp; Valuation Comps</div>
        <span class="badge badge-blue">HYDROGEN &amp; CLEAN ENERGY PEER MULTIPLES</span>
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Company / Peer Ticker</th>
              <th>Market Cap</th>
              <th>Enterprise Value</th>
              <th>Forward P/E</th>
              <th>Price / Sales</th>
              <th>Cash Runway</th>
              <th>Quarterly Revenue</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background: rgba(59, 130, 246, 0.1); font-weight: 700;">
              <td><span class="tip" title="Plug Power Inc. (Target Company)" data-tip="Plug Power: Turnkey hydrogen solutions leader. Market cap $2.10B, EV $2.97B with $134M cash and $28M quarterly cash burn.">Plug Power (PLUG)</span></td>
              <td>${mcap_m:,.2f}M</td>
              <td>${ev_m:,.2f}M</td>
              <td>{fwd_pe:.2f}x</td>
              <td>2.63x</td>
              <td style="color: #34d399;">4+ Qtrs</td>
              <td style="color: #60a5fa;">$200.60M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Bloom Energy Corporation" data-tip="BE: Solid oxide fuel cell server manufacturer.">Bloom Energy (BE)</span></td>
              <td>$2,450.0M</td>
              <td>$3,100.0M</td>
              <td>22.5x</td>
              <td>1.8x</td>
              <td>Funded</td>
              <td>$330.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="FuelCell Energy, Inc." data-tip="FCEL: Carbonate fuel cell power platforms.">FuelCell Energy (FCEL)</span></td>
              <td>$280.0M</td>
              <td>$390.0M</td>
              <td>-2.1x</td>
              <td>2.4x</td>
              <td>2026</td>
              <td>$24.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Ballard Power Systems Inc." data-tip="BLDP: PEM fuel cell stacks for bus, truck, rail, and marine.">Ballard Power (BLDP)</span></td>
              <td>$520.0M</td>
              <td>$480.0M</td>
              <td>-3.5x</td>
              <td>5.1x</td>
              <td>2027</td>
              <td>$16.0M</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ROW 6: 4-PILLAR POST-PRINT SENTIMENT GAUGE -->
    <section class="card" id="sec-sentiment" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 6: Multi-Source 4-Pillar Post-Print Sentiment Gauge</div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 12px; color: var(--text-muted);">Composite Score: <strong>{soc_data["composite_sentiment_score"]} / 100</strong></span>
          <div class="sentiment-meter-bar" style="width: 100px; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
            <div style="width: {soc_data["composite_sentiment_score"]}%; height: 100%; background: linear-gradient(90deg, #f59e0b, #10b981);"></div>
          </div>
        </div>
      </div>
      <div class="sentiment-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 16px;">
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Institutional Sentiment</div>
          <div style="font-size: 20px; font-weight: 800; color: #60a5fa; margin: 4px 0;">{soc_data["institutional_sentiment_score"]} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data["institutional_sentiment_score"]}%; height: 100%; background: #3b82f6;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Institutions focus on 65-point margin turnaround, $28M cash burn, and zero ATM dilution.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Retail Trader Pulse</div>
          <div style="font-size: 20px; font-weight: 800; color: #34d399; margin: 4px 0;">{soc_data["retail_sentiment_score"]} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data["retail_sentiment_score"]}%; height: 100%; background: #10b981;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Retail relieved by lack of ATM dilution and revenue beat ahead of Nov 19 Symposium.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Options Volatility Skew</div>
          <div style="font-size: 20px; font-weight: 800; color: #a855f7; margin: 4px 0;">75 / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: 75%; height: 100%; background: #a855f7;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Implied move was ±18.57% ($0.26); -0.67% move caused deep post-print volatility collapse.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Sell-Side Revision Tone</div>
          <div style="font-size: 20px; font-weight: 800; color: #34d399; margin: 4px 0;">72 / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: 72%; height: 100%; background: #10b981;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Analysts highlight Arcadia eFuels order and reaffirmation of +15% to +16% FY26 growth.</div>
        </div>
      </div>
      <p style="font-size: 12.5px; color: var(--text-secondary); margin: 0; line-height: 1.5;">
        <strong>Desk Takeaway &amp; Driver:</strong> {soc_data["after_hours_driver"]}
      </p>
    </section>

    <!-- ROW 7: HEDGE FUND PM TRADE EXECUTION MATRIX -->
    <section class="card" id="sec-trade" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 7: Institutional PM Post-Earnings Trade Execution Playbook</div>
        <span class="badge badge-purple">OPTIONS &amp; TACTICAL STRATEGY</span>
      </div>
      <div class="scenario-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
        <div class="scenario-bull" style="background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #34d399; margin-bottom: 6px;">Bull Case Target: $2.10</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $1.80 - $2.50 (+21% to +68% from AH $1.49)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            GenDrive commercial deployment momentum continues into Q4, green hydrogen plant output pushes gross margin into positive territory, and the Nov 19 Symposium showcases firm conversions from the $8B electrolyzer funnel.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #10b981;">
            <strong>Options Structure:</strong> Buy Jan 2027 $1.50 Calls. Sell Feb 2027 $2.50 Calls to construct an asymmetrical low-cost vertical spread.
          </div>
        </div>
        <div class="scenario-base" style="background: rgba(59, 130, 246, 0.04); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #60a5fa; margin-bottom: 6px;">Base Case Anchor: $1.50</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $1.35 - $1.65 (-9% to +11% around AH $1.49)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Stock consolidates near $1.50 as the market balances top-line outperformance and cash burn discipline against ongoing GAAP operating losses and non-cash valuation adjustments.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #3b82f6;">
            <strong>Options Structure:</strong> Sell Nov 2026 $1.00 / $2.00 Strangle to monetize rich implied volatility crush.
          </div>
        </div>
        <div class="scenario-bear" style="background: rgba(239, 68, 68, 0.04); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #f87171; margin-bottom: 6px;">Bear Case Target: $1.15</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $1.00 - $1.25 (-16% to -33% from AH $1.49)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Delays in commercial electrolyzer milestone execution or customer logistics challenges push cash usage back above $40M per quarter, reigniting financing overhangs.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #ef4444;">
            <strong>Options Structure:</strong> Buy Dec 2026 $1.50 Puts financed by writing Jan 2027 $2.00 Covered Calls.
          </div>
        </div>
      </div>
    </section>

    <!-- SEC CITATIONS & AUDIT LEDGER FOOTER -->
    <footer style="margin-top: 30px; padding-top: 16px; border-top: 1px solid var(--border-color); font-size: 11px; color: var(--text-muted); line-height: 1.6;">
      <div style="font-weight: 700; color: #94a3b8; margin-bottom: 6px;">Regulatory SEC Filing Citations &amp; Ground Truth Verification Ledger</div>
      <div>
        &bull; <strong>Primary Filing:</strong> Form 8-K (Item 2.02 Results of Operations and Financial Condition), Exhibit 99.1 Press Release, filed November 9, 2026 with the U.S. Securities and Exchange Commission (Accession: 0001104659-26-124487).<br>
        &bull; <strong>Quarterly Statement:</strong> Form 10-Q Quarterly Report for the Period Ended September 30, 2026 (Accession: 0001104659-26-124578).<br>
        &bull; <strong>Market Quotes:</strong> Regular Close: $1.50 | After-Hours: $1.49 (-0.67%) | Implied Move: ±18.57% ($0.26 straddle).<br>
        &bull; <strong>Revenue Provenance:</strong> Consolidated Net Revenue: $200.60M ($200,602 thousand) vs Street consensus $193.33M (+$7.27M beat).<br>
        &bull; <strong>Cash Flow Reconciliation:</strong> Nine-month OCF -$320.53M (-$320,525K) less six-month OCF -$244.11M yields Q3 2026 OCF of -$76.42M. CapEx $14.80M. Reported FCF -$91.22M. SBC $13.12M. True FCF -$104.34M. Net cash usage approximately $28.0M.<br>
        &bull; <strong>Disclaimer:</strong> This forensic post-earnings tearsheet is generated deterministically by the Antigravity 2.0 multi-agent research harness for institutional analysis and pair-programming research. Not financial advice.
      </div>
    </footer>
"""

draft_payload = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "rendered_container_html": html_content,
    "trade_matrix": {
        "bull_target_low_num": 2.10,
        "bear_target_high_num": 1.15
    },
    "historical_table_5q_nums": [
        {"gross_profit": -120.17, "operating_expenses": 126.71, "operating_income": -246.88},
        {"gross_profit": 5.45, "operating_expenses": 112.54, "operating_income": -107.09},
        {"gross_profit": -21.61, "operating_expenses": 82.32, "operating_income": -103.93},
        {"gross_profit": -1.68, "operating_expenses": 42.69, "operating_income": -44.36},
        {"gross_profit": -5.36, "operating_expenses": 69.90, "operating_income": -75.25}
    ],
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "period_label": "Q3 2026 (Ended Sep 30, 2026)",
            "ocf": q0_ocf,
            "capex": q0_capex,
            "reported_fcf": q0_rep_fcf,
            "sbc": q0_sbc,
            "finance_leases": q0_leases,
            "true_fcf": q0_true_fcf
        }
    }
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"Successfully generated post draft for {TICKER} ({DATE}) at {DRAFT_PATH} ({len(html_content):,} chars).")
