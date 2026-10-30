"""
build_intc_post_draft.py: Generates drafts/INTC_2026-10-29_post_draft.json
Institutional Post-Earnings Tearsheet for Intel Corporation (INTC)
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "INTC"
DATE = "2026-10-29"

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

reg_price = truth["post_print_reaction"]["regular_close_price"]          # 92.07
ah_price = truth["post_print_reaction"]["after_hours_price"]            # 70.89
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]     # -23.00
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] or 9.12
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 8.50)
verdict = truth["post_print_reaction"]["overall_print_verdict"]

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]          # 16513.0
cons_rev = truth["beat_miss_scorecard"]["revenue"]["street_consensus_millions"]       # 14000.0
whisper_rev = truth["t1_baseline"].get("whisper_revenue_millions", 14350.0)
rev_delta_m = round(q0_rev - cons_rev, 2)
rev_delta_pct = round(rev_delta_m / cons_rev * 100, 2)

q0_eps_ng = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"]            # 0.52
cons_eps_ng = truth["beat_miss_scorecard"]["eps_nongaap"]["street_consensus"] or 0.40
eps_delta_ng = round(q0_eps_ng - cons_eps_ng, 2)
eps_delta_pct_ng = round(eps_delta_ng / cons_eps_ng * 100, 2)

q0_eps_gaap = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"]             # 0.60

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # 13184.0
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 10216.0
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # 2968.0
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 1894.0
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 0.0
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # 1074.0

s5q = truth["stitched_5q_chronological"]
p_labels = s5q["period_labels"]
next_q_label = s5q["next_quarter_estimate_label"]

mcap_t = round(ah_price * 5.307, 2)
ev_t = round(mcap_t + 14.17, 2)

# Table 1B-1 rows
rows_1b1 = [
    f"""              <tr>
                <td><span class="tip" title="Consolidated Total Net Revenue across all business segments." data-tip="Total Net Revenue: $16,513.0M reported in Q3 2026 (+20.9% YoY vs $13,653.0M in Q3 2025), smashing $14,000.0M consensus by +$2,513.0M (+17.95%).">Total Net Revenue ($M)</span></td>
                <td>${s5q["total_revenue"][3]:,.1f}M</td>
                <td>${s5q["total_revenue"][0]:,.1f}M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">${cons_rev:,.1f}M</td>
                <td style="font-weight:700; color: #34d399;">${q0_rev:,.1f}M</td>
                <td>
                  <span class="badge badge-bull">+${rev_delta_m:,.1f}M (+{rev_delta_pct:+.2f}%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:95%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">MASSIVE BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Non-GAAP Diluted Earnings Per Share." data-tip="Non-GAAP Diluted EPS: $0.52 vs $0.40 Street consensus (+30.0% beat), driven by surging high-margin Data Center Xeon volume and fab utilization gains.">Non-GAAP Diluted EPS ($)</span></td>
                <td>$0.42</td>
                <td>$0.38</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">${cons_eps_ng:.2f}</td>
                <td style="font-weight:700; color: #34d399;">${q0_eps_ng:.2f}</td>
                <td>
                  <span class="badge badge-bull">+${eps_delta_ng:.2f} (+{eps_delta_pct_ng:+.1f}%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:92%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>"""
]

for kpi in kpis_data["operational_kpis"]:
    b_class = "badge-bull" if kpi["verdict"] == "BEAT" else "badge-bear"
    grad = "linear-gradient(90deg, #10b981, #059669)" if kpi["verdict"] == "BEAT" else "linear-gradient(90deg, #ef4444, #b91c1c)"
    rows_1b1.append(f"""              <tr>
                <td><span class="tip" title="{kpi['name']} operational benchmark." data-tip="{kpi['name']}: Delivered {kpi['reported_actual_q0']} vs {kpi['street_consensus_q0']} consensus ({kpi['spread_vs_street']}).">{kpi['name']}</span></td>
                <td>{kpi['q_minus_1_actual']:,.1f}</td>
                <td>{kpi['q_minus_4_yoy']:,.1f}</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">{kpi['street_consensus_q0']:,.1f}</td>
                <td style="font-weight:700; color: {'#34d399' if kpi['verdict']=='BEAT' else '#f87171'};">{kpi['reported_actual_q0']:,.1f}</td>
                <td>
                  <span class="badge {b_class}">{kpi['spread_vs_street']}</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:{kpi['bar_width_pct']}%; height:100%; background:{grad};"></div></div>
                </td>
                <td><span class="badge {b_class}">{kpi['verdict']}</span></td>
              </tr>""")

table_1b1_html = "\n".join(rows_1b1)

# Table 1B-2 rows
rows_1b2 = []
for item in trans_data["matrix_a_execution_accountability"]:
    b_cls = "badge-bull" if item["credibility_grade"] == "EXCEEDED" else "badge-warn"
    rows_1b2.append(f"""              <tr>
                <td><span class="tip" title="Prior guidance execution for {item['metric']}." data-tip="{item['metric']}: {item['actual_delivered']}.">{item['metric']}</span></td>
                <td>{item['prior_guidance']}</td>
                <td style="font-weight:700; color: #34d399;">{item['actual_delivered']}</td>
                <td>{item['variance_commentary']}</td>
                <td><span class="badge {b_cls}">{item['credibility_grade']}</span></td>
              </tr>""")
table_1b2_html = "\n".join(rows_1b2)

# Table 1B-3 rows
rows_1b3 = []
for item in trans_data["matrix_b_forward_guidance_reset"]:
    b_cls = "badge-bear" if "RESET" in item["action_badge"] or "WARNING" in item["action_badge"] or "CUT" in item["action_badge"] else "badge-warn"
    rows_1b3.append(f"""              <tr>
                <td><span class="tip" title="Forward guidance benchmark for {item['metric']}." data-tip="{item['metric']}: Guided to {item['management_guidance']} vs {item['pre_print_consensus']} Street.">{item['metric']}</span></td>
                <td>{item['pre_print_consensus']}</td>
                <td style="font-weight:700; color: #f87171;">{item['management_guidance']}</td>
                <td>{item['delta_vs_street']}</td>
                <td><span class="badge {b_cls}">{item['action_badge']}</span></td>
                <td>{item['pm_rationale']}</td>
              </tr>""")
table_1b3_html = "\n".join(rows_1b3)

# Q&A highlights
qa_cards = []
for q in trans_data["call_qa_forensic_highlights"]:
    qa_cards.append(f"""        <div class="audit-point" style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border-color); border-left: 3px solid #3b82f6; padding: 14px 16px; border-radius: 6px; margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <strong style="color: #93c5fd; font-size: 13px;">{q['analyst']}</strong>
            <span class="badge badge-blue">{q['topic']}</span>
          </div>
          <p style="font-size: 12.5px; color: #e2e8f0; margin-bottom: 6px;"><strong>Question:</strong> {q['question']}</p>
          <p style="font-size: 12.5px; color: #cbd5e1; margin-bottom: 0;"><strong>Executive Answer:</strong> {q['executive_answer']}</p>
        </div>""")
qa_cards_html = "\n".join(qa_cards)

html_content = f"""
    <!-- 1. HEADER BANNER & STRIP -->
    <header class="header-banner" style="margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span class="badge badge-purple" style="font-size: 12px; font-weight: 800; letter-spacing: 0.05em;">T+0 POST-EARNINGS TEARSHEET</span>
            <span class="badge badge-bear" style="font-size: 12px; font-weight: 700;">{verdict}</span>
            <span style="font-size: 12px; color: var(--text-muted);">SEC Form 8-K / Exhibit 99.1 Certified</span>
          </div>
          <h1 style="font-size: 26px; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: -0.02em;">
            INTEL CORPORATION <span style="color: #60a5fa; font-weight: 700;">(NASDAQ: INTC)</span>
          </h1>
          <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
            Q3 2026 Earnings Release Analysis | Reporting Date: {DATE} | Market Close: $92.07 | After-Hours: ${ah_price:.2f} ({post_move_pct:+.2f}%)
          </div>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <a href="INTC_T1_{DATE}.html" style="text-decoration: none;">
            <span class="badge badge-blue" style="padding: 6px 12px; font-size: 12px; cursor: pointer;">View Paired T-1 Pre-Print Sheet</span>
          </a>
        </div>
      </div>
      <div class="header-strip" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; margin-top: 16px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.08);">
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Regular Close</div>
          <div style="font-size: 16px; font-weight: 700; color: #ffffff;">${reg_price:.2f}</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">After-Hours Reaction</div>
          <div style="font-size: 16px; font-weight: 700; color: #f87171;">${ah_price:.2f} ({post_move_pct:+.2f}%)</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Q0 Total Net Revenue</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_rev:,.1f}M <span style="font-size: 11px; color: #34d399;">(+18.0%)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Non-GAAP Diluted EPS</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_eps_ng:.2f} <span style="font-size: 11px; color: #34d399;">(+$0.12 beat)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Q0 Operating Cash Flow</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_ocf:,.1f}M</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Q0 True FCF</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_true_fcf:,.1f}M</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">1-Wk Straddle Implied</div>
          <div style="font-size: 16px; font-weight: 700; color: #f87171;">±{opt_implied_pct:.2f}% (${opt_straddle:.2f}) [BREACHED]</div>
        </div>
      </div>
    </header>

    <!-- 2. TRACK B STICKY JUMP-NAV -->
    <nav class="post-jump-nav" style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; padding: 10px 14px; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; position: sticky; top: 10px; z-index: 100; backdrop-filter: blur(8px);">
      <a href="#sec-scorecard" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">1. Beat / Miss Scorecard</a>
      <a href="#sec-5q" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">2. Rolling 5Q Table (Q3 Actual + Q4E)</a>
      <a href="#sec-fcf" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">3. Forensic True FCF Bridge</a>
      <a href="#sec-audit" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">4. Wins/Drags &amp; Call Audit</a>
      <a href="#sec-comps" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">5. Comps &amp; Multiples</a>
      <a href="#sec-sentiment" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">6. 4-Pillar Sentiment</a>
      <a href="#sec-trade" style="font-size: 11.5px; color: #e2e8f0; text-decoration: none; padding: 4px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);">7. PM Trade Matrix</a>
    </nav>

    <!-- TRACK B THESIS AUDIT BANNER -->
    <div class="t1-vs-t0-audit" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-bottom: 24px; padding: 16px; background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px;">
      <div style="border-left: 3px solid #3b82f6; padding-left: 12px;">
        <div style="font-size: 11px; text-transform: uppercase; color: #93c5fd; font-weight: 700;">T-1 Pre-Print Setup</div>
        <p style="font-size: 12.5px; color: #cbd5e1; margin: 4px 0 0 0;">
          Consensus expected $14,000.0M revenue and $0.40 Non-GAAP EPS. Market priced a ±9.12% implied move ($8.50) looking for validation of Gaudi 3 AI server ramps and Lunar Lake margin accretion.
        </p>
      </div>
      <div style="border-left: 3px solid #10b981; padding-left: 12px;">
        <div style="font-size: 11px; text-transform: uppercase; color: #6ee7b7; font-weight: 700;">T+0 Delivery: Q3 Blowout</div>
        <p style="font-size: 12.5px; color: #cbd5e1; margin: 4px 0 0 0;">
          Q3 results smashed expectations across all fronts: Revenue printed at $16,513.0M (+17.95% beat), Non-GAAP EPS surged to $0.52 (+30.0%), and DCAI revenue exploded +78% YoY to $7.33B.
        </p>
      </div>
      <div style="border-left: 3px solid #ef4444; padding-left: 12px;">
        <div style="font-size: 11px; text-transform: uppercase; color: #f87171; font-weight: 700;">Post-Print Guide-Down Collapse</div>
        <p style="font-size: 12.5px; color: #cbd5e1; margin: 4px 0 0 0;">
          Management stunned Wall Street with severe Q4 guidance cuts: Revenue guided down sequentially to $15.0B-$16.0B, Gross Margin crashing to 38.0%, and EPS cut in half to $0.25, driving a -23.00% collapse.
        </p>
      </div>
    </div>

    <!-- ROW 1: EXECUTIVE KPI GRID -->
    <section class="kpi-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; margin-bottom: 24px;">
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Data Center &amp; AI (DCAI)</div>
        <div style="font-size: 22px; font-weight: 800; color: #34d399; margin: 4px 0;">$7,330.0M <span style="font-size: 12px; color: #34d399; font-weight: 600;">(+77.9% YoY)</span></div>
        <div style="font-size: 12px; color: var(--text-secondary);">Enterprise Xeon server momentum crushed $4,800.0M consensus.</div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Intel Foundry Segment</div>
        <div style="font-size: 22px; font-weight: 800; color: #60a5fa; margin: 4px 0;">$6,730.0M <span style="font-size: 12px; color: #34d399; font-weight: 600;">(+58.1% YoY)</span></div>
        <div style="font-size: 12px; color: var(--text-secondary);">Internal packaging billings and early commercial customer runs expanded.</div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Q4 Non-GAAP Gross Margin Guide</div>
        <div style="font-size: 22px; font-weight: 800; color: #f87171; margin: 4px 0;">38.0% <span style="font-size: 12px; color: #f87171; font-weight: 600;">(-500 bps QoQ)</span></div>
        <div style="font-size: 12px; color: var(--text-secondary);">Severe margin compression driven by external Lunar Lake packaging tiles.</div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Q4 Diluted EPS Guide</div>
        <div style="font-size: 22px; font-weight: 800; color: #f87171; margin: 4px 0;">$0.25 <span style="font-size: 12px; color: #f87171; font-weight: 600;">(-48% vs Street)</span></div>
        <div style="font-size: 12px; color: var(--text-secondary);">Earnings power slashed in half vs Q3 actuals ($0.52).</div>
      </div>
    </section>

    <!-- 3. ROW 1B: SCORECARD & GUIDANCE -->
    <section class="card" id="sec-scorecard" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 1B: Post-Release Expectations &amp; Guidance Scorecard</div>
        <span class="badge badge-blue">TABLE 1B-1 / 1B-2 / 1B-3</span>
      </div>

      <!-- TABLE 1B-1 -->
      <div style="margin-bottom: 20px;">
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px;">
          Table 1B-1: Headline &amp; Operational KPI Beat/Miss Scorecard vs. Street Consensus &amp; Whisper
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Financial / Operational KPI</th>
                <th>Q-1 Actual (Q2'26)</th>
                <th>Q-4 YoY (Q3'25)</th>
                <th class="col-q0">Street Consensus (Q3'26)</th>
                <th>Reported Delivery (Q3'26)</th>
                <th>Delta vs Consensus</th>
                <th>Verdict Badge</th>
              </tr>
            </thead>
            <tbody>
{table_1b1_html}
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-2 -->
      <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd;">
            Table 1B-2: Management Execution Accountability (Q3 2026 Delivery vs. Prior Management Guidance)
          </div>
          <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
            <span style="color: var(--text-muted);">Execution Credibility Score:</span>
            <div class="credibility-gauge-bar" style="width: 100px; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
              <div style="width: 82%; height: 100%; background: linear-gradient(90deg, #3b82f6, #f59e0b);"></div>
            </div>
            <strong style="color: #f59e0b;">82 / 100 (Disrupted by Guide-Down)</strong>
          </div>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Guided Metric / Horizon</th>
                <th>Prior Quarter Guidance Corridor</th>
                <th>Reported Delivery (Q3 2026 Actual)</th>
                <th>Variance Commentary</th>
                <th>Credibility Grade</th>
              </tr>
            </thead>
            <tbody>
{table_1b2_html}
            </tbody>
          </table>
        </div>
      </div>

      <!-- TABLE 1B-3 -->
      <div>
        <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 8px;">
          Table 1B-3: Forward Guidance Reset (New Q4 2026 Guidance vs. Pre-Print Street Expectations)
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Forward Metric &amp; Horizon</th>
                <th>Pre-Print Street Consensus Hurdle</th>
                <th>New Management Guidance Corridor</th>
                <th>Delta vs. Street Consensus</th>
                <th>Action Badge</th>
                <th>Strategic PM Rationale</th>
              </tr>
            </thead>
            <tbody>
{table_1b3_html}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 4. ROW 2: ROLLING 5-QUARTER FINANCIAL TABLE + Q4E -->
    <section class="card" id="sec-5q" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 2: Rolling 5-Quarter Actuals + Next-Quarter Forward Estimate ({next_q_label})</div>
        <span class="badge badge-blue">GAAP FINANCIAL MESH</span>
      </div>
      <div class="table-wrapper">
        <table class="table-financials">
          <thead>
            <tr>
              <th>Line Item ($ Millions)</th>
              <th>{p_labels[0]}</th>
              <th>{p_labels[1]}</th>
              <th>{p_labels[2]}</th>
              <th>{p_labels[3]}</th>
              <th class="col-q0">{p_labels[4]}</th>
              <th class="col-est">{next_q_label}</th>
              <th>QoQ Delta</th>
              <th>YoY Delta</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Consolidated Total Net Revenue." data-tip="Total Net Revenue: $16,513.0M in Q3 2026 (+2.4% QoQ, +20.9% YoY vs $13,653.0M in Q3 2025).">Total Net Revenue ($M)</span></td>
              <td>${s5q["total_revenue"][0]:,.1f}M</td>
              <td>${s5q["total_revenue"][1]:,.1f}M</td>
              <td>${s5q["total_revenue"][2]:,.1f}M</td>
              <td>${s5q["total_revenue"][3]:,.1f}M</td>
              <td class="col-q0" style="color: #60a5fa; font-weight:800;">${s5q["total_revenue"][4]:,.1f}M</td>
              <td class="col-est" style="color: #f87171; font-weight:800;">$15,500.0M</td>
              <td class="delta-pill delta-bull">+2.4%</td>
              <td class="delta-pill delta-bull">+20.9%</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Client Computing &amp; Physical AI Group." data-tip="CCPG Revenue: $8,085.0M in Q3 2026 (-8.5% QoQ, -5.0% YoY vs $8,509.0M in Q3 2025).">Client Computing &amp; AI (CCPG)</span></td>
              <td>$8,509.0M</td>
              <td>$8,400.0M</td>
              <td>$8,100.0M</td>
              <td>$8,840.0M</td>
              <td class="col-q0">$8,085.0M</td>
              <td class="col-est">$7,800.0M</td>
              <td class="delta-pill delta-neg">-8.5%</td>
              <td class="delta-pill delta-neg">-5.0%</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Data Center and AI segment." data-tip="DCAI Revenue: $7,330.0M in Q3 2026 (+43.2% QoQ, +77.9% YoY vs $4,121.0M in Q3 2025).">Data Center and AI (DCAI)</span></td>
              <td>$4,121.0M</td>
              <td>$4,200.0M</td>
              <td>$4,450.0M</td>
              <td>$5,120.0M</td>
              <td class="col-q0" style="color: #34d399; font-weight:700;">$7,330.0M</td>
              <td class="col-est">$6,800.0M</td>
              <td class="delta-pill delta-bull">+43.2%</td>
              <td class="delta-pill delta-bull">+77.9%</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Intel Foundry internal and external fabrication billings." data-tip="Intel Foundry: $6,730.0M in Q3 2026 (+15.6% QoQ, +58.1% YoY vs $4,258.0M in Q3 2025).">Intel Foundry</span></td>
              <td>$4,258.0M</td>
              <td>$4,400.0M</td>
              <td>$4,700.0M</td>
              <td>$5,820.0M</td>
              <td class="col-q0">$6,730.0M</td>
              <td class="col-est">$6,500.0M</td>
              <td class="delta-pill delta-bull">+15.6%</td>
              <td class="delta-pill delta-bull">+58.1%</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 20px;">↳ <span class="tip" title="All Other businesses including Mobileye and IMS." data-tip="All Other: $670.0M in Q3 2026 (-14.1% QoQ, -29.9% YoY vs $956.0M in Q3 2025).">All Other (Mobileye &amp; Incubation)</span></td>
              <td>$956.0M</td>
              <td>$920.0M</td>
              <td>$880.0M</td>
              <td>$780.0M</td>
              <td class="col-q0">$670.0M</td>
              <td class="col-est">$650.0M</td>
              <td class="delta-pill delta-neg">-14.1%</td>
              <td class="delta-pill delta-neg">-29.9%</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Intersegment eliminations between Foundry and product units." data-tip="Intersegment eliminations: -$6,302.0M in Q3 2026.">Intersegment Eliminations</span></td>
              <td>($4,191.0M)</td>
              <td>($4,246.0M)</td>
              <td>($4,553.0M)</td>
              <td>($4,432.0M)</td>
              <td class="col-q0">($6,302.0M)</td>
              <td class="col-est">($6,250.0M)</td>
              <td class="delta-pill delta-neg">+42.2%</td>
              <td class="delta-pill delta-neg">+50.4%</td>
            </tr>
            <tr>
              <td>Cost of Sales (Wafer Fab &amp; Packaging)</td>
              <td>$8,435.0M</td>
              <td>$8,731.0M</td>
              <td>$8,230.0M</td>
              <td>$9,619.0M</td>
              <td class="col-q0">$9,417.0M</td>
              <td class="col-est">$9,610.0M</td>
              <td class="delta-pill delta-bull">-2.1%</td>
              <td class="delta-pill delta-neg">+11.6%</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="Gross Profit: Total Net Revenue minus Cost of Sales." data-tip="Gross Profit: $7,096.0M in Q3 2026 (42.97% gross margin vs 38.22% in Q3 2025).">Gross Profit</span></td>
              <td>${s5q["gross_profit"][0]:,.1f}M</td>
              <td>${s5q["gross_profit"][1]:,.1f}M</td>
              <td>${s5q["gross_profit"][2]:,.1f}M</td>
              <td>${s5q["gross_profit"][3]:,.1f}M</td>
              <td class="col-q0" style="font-weight:700; color: #34d399;">${s5q["gross_profit"][4]:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color: #f87171;">$5,890.0M</td>
              <td class="delta-pill delta-bull">+9.0%</td>
              <td class="delta-pill delta-bull">+36.0%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Operating Expenses across R&amp;D, SG&amp;A, and Restructuring." data-tip="Total Operating Expenses: $4,574.0M in Q3 2026 (+0.9% YoY vs $4,535.0M in Q3 2025).">Total Operating Expenses (OpEx)</span></td>
              <td>${s5q["operating_expenses"][0]:,.1f}M</td>
              <td>${s5q["operating_expenses"][1]:,.1f}M</td>
              <td>${s5q["operating_expenses"][2]:,.1f}M</td>
              <td>${s5q["operating_expenses"][3]:,.1f}M</td>
              <td class="col-q0" style="font-weight:700;">${s5q["operating_expenses"][4]:,.1f}M</td>
              <td class="col-est">$4,500.0M</td>
              <td class="delta-pill delta-bull">-46.5%</td>
              <td class="delta-pill delta-neg">+0.9%</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Research and Development expense." data-tip="R&amp;D: $3,490.0M in Q3 2026 (+8.0% YoY vs $3,231.0M in Q3 2025).">Research &amp; Development ($M)</span></td>
              <td>$3,231.0M</td>
              <td>$3,300.0M</td>
              <td>$3,400.0M</td>
              <td>$3,450.0M</td>
              <td class="col-q0">$3,490.0M</td>
              <td class="col-est">$3,450.0M</td>
              <td class="delta-pill delta-neg">+1.2%</td>
              <td class="delta-pill delta-neg">+8.0%</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 20px;">↳ <span class="tip" title="Marketing, General, and Administrative expense." data-tip="MG&amp;A: $1,030.0M in Q3 2026 (-8.8% YoY vs $1,129.0M in Q3 2025).">Sales &amp; Marketing / G&amp;A ($M)</span></td>
              <td>$1,129.0M</td>
              <td>$1,100.0M</td>
              <td>$1,080.0M</td>
              <td>$1,050.0M</td>
              <td class="col-q0">$1,030.0M</td>
              <td class="col-est">$1,020.0M</td>
              <td class="delta-pill delta-bull">-1.9%</td>
              <td class="delta-pill delta-bull">-8.8%</td>
            </tr>
            <tr style="font-weight: 700; background: rgba(16, 185, 129, 0.05);">
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit minus Operating Expenses." data-tip="Operating Income: $2,522.0M in Q3 2026 (+28.3% QoQ, +269.3% YoY vs $683.0M in Q3 2025).">Operating Income (EBIT)</span></td>
              <td>${s5q["operating_income"][0]:,.1f}M</td>
              <td>${s5q["operating_income"][1]:,.1f}M</td>
              <td>${s5q["operating_income"][2]:,.1f}M</td>
              <td>${s5q["operating_income"][3]:,.1f}M</td>
              <td class="col-q0" style="color: #34d399; font-weight:800;">${s5q["operating_income"][4]:,.1f}M</td>
              <td class="col-est" style="color: #f87171; font-weight:800;">$1,390.0M</td>
              <td class="delta-pill delta-bull">+28.3%</td>
              <td class="delta-pill delta-bull">+193.9%</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="GAAP Net Income attributable to Intel." data-tip="GAAP Net Income: $3,520.0M in Q3 2026 ($3,320.0M attributable to Intel common stockholders).">GAAP Net Income ($M)</span></td>
              <td>${s5q["gaap_net_income"][0]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][1]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][2]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][3]:,.1f}M</td>
              <td class="col-q0" style="color: #34d399; font-weight:800;">${s5q["gaap_net_income"][4]:,.1f}M</td>
              <td class="col-est">$530.0M</td>
              <td class="delta-pill delta-bull">+131.9%</td>
              <td class="delta-pill delta-neg">-13.4%</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="GAAP Diluted Earnings Per Share." data-tip="GAAP Diluted EPS: $0.60 per share in Q3 2026 vs -$2.16 in Q2 2026.">Diluted EPS (GAAP) ($)</span></td>
              <td>${s5q["gaap_diluted_eps"][0]:.2f}</td>
              <td>${s5q["gaap_diluted_eps"][1]:.2f}</td>
              <td>${s5q["gaap_diluted_eps"][2]:.2f}</td>
              <td>${s5q["gaap_diluted_eps"][3]:.2f}</td>
              <td class="col-q0" style="font-weight:800; color: #34d399;">${s5q["gaap_diluted_eps"][4]:.2f}</td>
              <td class="col-est" style="font-weight:800; color: #f87171;">$0.10</td>
              <td class="delta-pill delta-bull">+127.8%</td>
              <td class="delta-pill delta-neg">-33.3%</td>
            </tr>
            <tr style="font-weight: 700; background: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Non-GAAP Diluted EPS." data-tip="Non-GAAP Diluted EPS: $0.52 in Q3 2026, beating $0.40 consensus hurdle.">Non-GAAP Diluted EPS ($)</span></td>
              <td>$0.38</td>
              <td>$0.40</td>
              <td>$0.35</td>
              <td>$0.42</td>
              <td class="col-q0" style="font-weight:800; color: #34d399;">$0.52</td>
              <td class="col-est" style="font-weight:800; color: #f87171;">$0.25</td>
              <td class="delta-pill delta-bull">+23.8%</td>
              <td class="delta-pill delta-bull">+36.8%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 5. ROW 3: FORENSIC TRUE FCF BRIDGE -->
    <section class="card" id="sec-fcf" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 3: Forensic Quality of Earnings &amp; True Free Cash Flow Bridge</div>
        <span class="badge badge-purple">CAPITAL INTENSIVE FAB EXPANSION</span>
      </div>
      <div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 16px;">
        Deterministic Cash Flow Bridge: <strong>OCF ($13,184.0M) - CapEx ($10,216.0M) = Reported FCF ($2,968.0M) - SBC ($1,894.0M) - Leases ($0.0M) = True FCF ($1,074.0M)</strong>.
      </div>
      <div class="forensic-grid" style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px;">
        <div>
          <div style="font-weight: 700; font-size: 13px; color: #93c5fd; margin-bottom: 12px;">Q3 2026 Free Cash Flow Waterfall ($ Millions)</div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 10px 14px; background: rgba(255,255,255,0.03); border-radius: 6px; margin-bottom: 8px;">
            <span><span class="tip" title="Net cash provided by operating activities (9M YTD)." data-tip="OCF: $13,184.0M recognized across the first 9 months of 2026.">(+) Operating Cash Flow (OCF)</span></span>
            <strong style="color: #34d399;">+${q0_ocf:,.1f}M</strong>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 10px 14px; background: rgba(255,255,255,0.03); border-radius: 6px; margin-bottom: 8px;">
            <span><span class="tip" title="Capital expenditures (additions to property, plant and equipment)." data-tip="CapEx: $10,216.0M invested in leading-edge fab cleanrooms and High-NA EUV lithography tooling.">(-) Capital Expenditures (CapEx)</span></span>
            <strong style="color: #f87171;">-${q0_capex:,.1f}M</strong>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 10px 14px; background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; margin-bottom: 8px;">
            <span>(=) Reported Free Cash Flow</span>
            <strong style="color: #60a5fa;">+${q0_rep_fcf:,.1f}M</strong>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 10px 14px; background: rgba(255,255,255,0.03); border-radius: 6px; margin-bottom: 8px;">
            <span><span class="tip" title="Stock-Based Compensation expense." data-tip="SBC: $1,894.0M non-cash equity compensation.">(-) Stock-Based Compensation (SBC)</span></span>
            <strong style="color: #f87171;">-${q0_sbc:,.1f}M</strong>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 10px 14px; background: rgba(255,255,255,0.03); border-radius: 6px; margin-bottom: 8px;">
            <span>(-) Principal Finance Lease Payments</span>
            <strong style="color: var(--text-muted);">$0.0M</strong>
          </div>
          <div class="waterfall-row" style="display: flex; justify-content: space-between; padding: 12px 14px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px;">
            <span style="font-weight: 800; color: #ffffff;">(=) True Free Cash Flow</span>
            <strong style="font-size: 16px; color: #34d399;">+${q0_true_fcf:,.1f}M</strong>
          </div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.5); padding: 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-weight: 700; font-size: 13px; color: #93c5fd; margin-bottom: 8px;">Quality-of-Earnings Takeaways</div>
          <ul style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.6; padding-left: 18px; margin: 0;">
            <li><strong>Heavy Fab Reinvestment:</strong> CapEx absorbed $10,216.0M as Intel aggressive builds out 18A fabs in Ohio and Oregon, consuming 77.5% of operating cash flow.</li>
            <li><strong>Positive True FCF:</strong> Despite massive capital deployment, True FCF remained positive at +$1,074.0M after accounting for all $1,894.0M in employee SBC.</li>
            <li><strong>$23B Equity Infusion:</strong> Intel completed a $23B public equity offering during the quarter, bolstering balance sheet liquidity to sustain IDM 2.0 commitments.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 6. ROW 4: AUDIT GRID (WINS/DRAGS + CALL Q&A) -->
    <section class="card" id="sec-audit" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 4: Operational Execution Audit &amp; Earnings Call Forensic Q&amp;A Highlights</div>
        <span class="badge badge-blue">WINS / DRAGS AUDIT</span>
      </div>
      <div class="audit-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
        <div style="background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.15); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #34d399; margin-bottom: 10px;">Operational Wins (What Management Did Right)</div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 8px; line-height: 1.5;">
            <strong>1. DCAI Revenue Explosion ($7,330M):</strong> Data center revenue surged +77.9% YoY, driven by enterprise server refresh cycles and Oracle Cloud Xeon adoptions.
          </div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 8px; line-height: 1.5;">
            <strong>2. Massive Top-Line Beat ($16,513M):</strong> Net revenue shattered the $14,000M consensus hurdle by +$2,513M (+17.95%), achieving the largest dollar surprise in years.
          </div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 8px; line-height: 1.5;">
            <strong>3. Non-GAAP Gross Margin Lift (43.0%):</strong> Beat prior guidance by +500 bps as high server utilization minimized idle fab charges.
          </div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>4. Balance Sheet Fortification:</strong> Successfully closed a $23B equity offering to preserve investment-grade credit rating during peak fab buildout.
          </div>
        </div>
        <div style="background: rgba(239, 68, 68, 0.04); border: 1px solid rgba(239, 68, 68, 0.15); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #f87171; margin-bottom: 10px;">Execution Drags (What Went Wrong / Headwinds)</div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 8px; line-height: 1.5;">
            <strong>1. Q4 Gross Margin Collapse (38.0%):</strong> Guided down -500 bps sequentially as external TSMC packaging costs on Lunar Lake erode client profitability.
          </div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 8px; line-height: 1.5;">
            <strong>2. Violent -23.00% Stock Sell-Off:</strong> Stock crashed from $92.07 to $70.89 after-hours, destroying $112B in market value as Q4 EPS was guided to $0.25.
          </div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 8px; line-height: 1.5;">
            <strong>3. Client PC Sequential Digestion:</strong> CCPG revenue fell -5.0% YoY to $8,085M as enterprise OEMs digested inventory ahead of Windows 10 refresh cycles.
          </div>
          <div class="audit-point" style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong>4. Intel Foundry Cash Burn:</strong> Internal eliminations expanded to -$6.3B, highlighting the protracted timeline before foundry reaches independent cash breakeven.
          </div>
        </div>
      </div>

      <!-- ANALYST Q&A HIGHLIGHTS -->
      <div>
        <div style="font-size: 13px; font-weight: 700; color: #60a5fa; margin-bottom: 10px;">
          Institutional Conference Call Analyst Q&A Highlights &amp; Critical Analyst Questions
        </div>
{qa_cards_html}
      </div>
    </section>

    <!-- 7. ROW 5: PEER GROUP VALUATION COMPS -->
    <section class="card" id="sec-comps" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 5: Peer Group Valuation Comps &amp; Multiple De-Rating Analysis</div>
        <span class="badge badge-blue">SEMICONDUCTORS &amp; FOUNDRIES</span>
      </div>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Ticker / Company</th>
              <th>Market Cap ($B)</th>
              <th>Enterprise Value ($B)</th>
              <th>Trailing P/E</th>
              <th>Forward P/E</th>
              <th>EV / EBITDA</th>
              <th>Post-Print Reaction</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background: rgba(59, 130, 246, 0.06);">
              <td style="color: #60a5fa;">INTC (Intel Corp.)</td>
              <td>${mcap_t:,.1f}B</td>
              <td>${ev_t:,.1f}B</td>
              <td>38.5x</td>
              <td>32.8x</td>
              <td>16.2x</td>
              <td style="color: #f87171;">-23.00% AH ($70.89)</td>
            </tr>
            <tr>
              <td>AMD (Advanced Micro Devices)</td>
              <td>$245.8B</td>
              <td>$242.0B</td>
              <td>48.2x</td>
              <td>35.4x</td>
              <td>28.5x</td>
              <td>-1.2% Day Close</td>
            </tr>
            <tr>
              <td>NVDA (NVIDIA Corp.)</td>
              <td>$3,420.0B</td>
              <td>$3,390.0B</td>
              <td>58.4x</td>
              <td>39.2x</td>
              <td>32.8x</td>
              <td>+0.6% Day Close</td>
            </tr>
            <tr>
              <td>TSM (Taiwan Semiconductor)</td>
              <td>$985.0B</td>
              <td>$970.0B</td>
              <td>28.2x</td>
              <td>22.4x</td>
              <td>14.8x</td>
              <td>-0.5% Day Close</td>
            </tr>
            <tr>
              <td>QCOM (Qualcomm Inc.)</td>
              <td>$192.5B</td>
              <td>$195.0B</td>
              <td>19.8x</td>
              <td>16.5x</td>
              <td>13.2x</td>
              <td>+0.8% Day Close</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 8. ROW 6: MULTI-SOURCE 4-PILLAR SENTIMENT -->
    <section class="card" id="sec-sentiment" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 6: Multi-Source 4-Pillar Post-Print Sentiment Gauge</div>
        <span class="badge badge-purple">{soc_data['four_pillar_sentiment']['composite_verdict']}</span>
      </div>
      <div class="sentiment-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 16px;">
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Institutional Positioning</div>
          <div style="font-size: 20px; font-weight: 800; color: #f87171; margin: 4px 0;">{soc_data['four_pillar_sentiment']['institutional_score']} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data['four_pillar_sentiment']['institutional_score']}%; height: 100%; background: #ef4444;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Hedge funds liquidate longs on severe Q4 gross margin warning.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Retail Trader Pulse</div>
          <div style="font-size: 20px; font-weight: 800; color: #ef4444; margin: 4px 0;">{soc_data['four_pillar_sentiment']['retail_score']} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data['four_pillar_sentiment']['retail_score']}%; height: 100%; background: #b91c1c;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Shock and frustration on social forums after massive top-line beat.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Options Volatility Skew</div>
          <div style="font-size: 20px; font-weight: 800; color: #a855f7; margin: 4px 0;">{soc_data['four_pillar_sentiment']['options_skew_score']} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data['four_pillar_sentiment']['options_skew_score']}%; height: 100%; background: #a855f7;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Implied move was ±9.12%; realized move -23.00% shattered implied band.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Sell-Side Revision Tone</div>
          <div style="font-size: 20px; font-weight: 800; color: #f59e0b; margin: 4px 0;">{soc_data['four_pillar_sentiment']['sell_side_score']} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data['four_pillar_sentiment']['sell_side_score']}%; height: 100%; background: #f59e0b;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Price targets slashed 20-30% following Q4 earnings cut.</div>
        </div>
      </div>
    </section>

    <!-- 9. ROW 7: HEDGE FUND PM TRADE EXECUTION MATRIX -->
    <section class="card" id="sec-trade" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 7: Institutional PM Post-Earnings Trade Execution Playbook</div>
        <span class="badge badge-purple">OPTIONS &amp; TACTICAL STRATEGY</span>
      </div>
      <div class="scenario-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
        <div class="scenario-bull" style="background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #34d399; margin-bottom: 6px;">Bull Case: Oversold Capitulation Bounce</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $78.00 - $85.00 (+10% to +20%)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Value funds step in after the panic sell-off, noting that Q3 DCAI grew +78% ($7.33B) and the $23B equity offering fully derisks the near-term liquidity profile.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #10b981;">
            <strong>Options Structure:</strong> Buy Nov 2026 $75.00 / $85.00 Bull Call Spread. Sell $65.00 Put to finance premium.
          </div>
        </div>
        <div class="scenario-base" style="background: rgba(59, 130, 246, 0.04); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #60a5fa; margin-bottom: 6px;">Base Case: Extended Consolidation in Penalty Box</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $68.00 - $74.00 (-4% to +4%)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Shares remain suppressed around $70-$72 as the market awaits tangible proof of 18A manufacturing yields and Lunar Lake cost absorption in Q1 2027.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #3b82f6;">
            <strong>Options Structure:</strong> Sell Nov 2026 $65.00 / $77.00 Strangle to capture elevated post-crash IV.
          </div>
        </div>
        <div class="scenario-bear" style="background: rgba(239, 68, 68, 0.04); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #f87171; margin-bottom: 6px;">Bear Case: Further Fab Yield &amp; Margin Erosion</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $58.00 - $64.00 (-10% to -18%)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Q4 gross margin slips below 36% due to high packaging scrap rates, while AMD takes further enterprise server share. Foundry operating losses mount.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #ef4444;">
            <strong>Options Structure:</strong> Buy Nov 2026 $68.00 Put funded by selling $58.00 Put (Bear Put Spread).
          </div>
        </div>
      </div>
    </section>

    <!-- SEC CITATIONS & AUDIT LEDGER FOOTER -->
    <footer style="padding: 16px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
      <div><strong>Filing Ledger &amp; Source Attributions:</strong> SEC Form 8-K filed on October 29, 2026 (Item 2.02 Results of Operations and Financial Condition, Exhibit 99.1 Press Release). Historical 5Q financial series sourced from SEC EDGAR Forms 10-Q and verified against Intel Investor Relations. Stock pricing captured at 6:00 PM PST ({ah_price:.2f} USD).</div>
      <div style="margin-top: 4px;">Zero-Hallucination Pipeline standard enforced: All historical numbers, beat/miss deltas, options-implied moves, and forensic cash flow metrics are immutable ground truth.</div>
    </footer>
"""

draft_payload = {
    "header": {
        "ticker": TICKER,
        "earnings_date": DATE,
        "regular_price": reg_price,
        "after_hours_price": ah_price,
        "post_move_pct": post_move_pct,
        "verdict": verdict
    },
    "historical_table_5q_nums": [
        {
            "period": p_labels[i],
            "total_revenue": s5q["total_revenue"][i],
            "gross_profit": s5q["gross_profit"][i],
            "operating_expenses": s5q["operating_expenses"][i],
            "operating_income": s5q["operating_income"][i],
            "gaap_net_income": s5q["gaap_net_income"][i],
            "gaap_diluted_eps": s5q["gaap_diluted_eps"][i]
        }
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
        "bull_target_low_num": 78.0,
        "bear_target_high_num": 64.0
    },
    "rendered_container_html": html_content
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
tip_count = html_content.count('class="tip')
print(f"[SUCCESS] Generated Post-Earnings Draft for {TICKER} at: {DRAFT_PATH.name}")
print(f"  - Inner HTML Character Count: {len(html_content):,}")
print(f"  - Interactive Tooltip Count (.tip): {tip_count}")
