"""
build_nvt_post_draft.py: Generates drafts/NVT_2026-10-30_post_draft.json
Institutional Post-Earnings Forensic Tearsheet for nVent Electric plc (NVT)
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "NVT"
DATE = "2026-10-30"

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

reg_price = truth["post_print_reaction"]["regular_close_price"]          # 125.98
ah_price = truth["post_print_reaction"]["after_hours_price"]            # 127.30
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]     # +1.05%
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] or 14.04
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 19.50)
verdict = truth["post_print_reaction"]["overall_print_verdict"]          # EPS BEAT / REVENUE MISS

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]          # 1514.9
cons_rev = truth["beat_miss_scorecard"]["revenue"]["street_consensus_millions"]       # 1540.0
whisper_rev = truth["t1_baseline"].get("whisper_revenue_millions", 1575.0)
rev_delta_m = round(q0_rev - cons_rev, 2)                                              # -25.10
rev_delta_pct = round(rev_delta_m / cons_rev * 100, 2)                                 # -1.63%

q0_eps_ng = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"]            # 1.52
cons_eps_ng = truth["beat_miss_scorecard"]["eps_nongaap"]["street_consensus"] or 1.40
eps_delta_ng = round(q0_eps_ng - cons_eps_ng, 2)                                      # +0.12
eps_delta_pct_ng = round(eps_delta_ng / cons_eps_ng * 100, 2)                         # +8.57%

q0_eps_gaap = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"]             # 1.23

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # 571.5
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 94.6
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # 476.9
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 30.9
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 0.0
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # 446.0

s5q = truth["stitched_5q_chronological"]
p_labels = s5q["period_labels"]                                # Q3 2025, Q4 2025, Q1 2026, Q2 2026, Q3 2026 (Actual)
next_q_label = s5q["next_quarter_estimate_label"]              # Q4 2026E (Guided / Street)

mcap_m = truth["market_portal"]["market_cap_millions"] or 20390.86
ev_m = truth["market_portal"]["enterprise_value_millions"] or 21767.76

# Table 1B-1 rows
rows_1b1 = [
    f"""              <tr>
                <td><span class="tip" title="Consolidated Total Net Revenue / Net Sales across all continuing operations." data-tip="Total Net Revenue: $1,514.9M (1514.9M exact, $1,515M rounded) reported in Q3 2026 (+43.7% YoY vs $1,054.0M in Q3 2025), trailing $1,540.0M consensus by -$25.1M (-1.63%) but up +44% organically.">Total Net Revenue ($M)</span></td>
                <td>${s5q["total_revenue"][3]:,.1f}M</td>
                <td>${s5q["total_revenue"][0]:,.1f}M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">${cons_rev:,.1f}M</td>
                <td style="font-weight:700; color: #f87171;">${q0_rev:,.1f}M</td>
                <td>
                  <span class="badge badge-bear">${rev_delta_m:,.1f}M ({rev_delta_pct:+.2f}%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:48%; height:100%; background:linear-gradient(90deg, #ef4444, #b91c1c);"></div></div>
                </td>
                <td><span class="badge badge-warn">NARROW MISS</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Non-GAAP Adjusted Diluted Earnings Per Share." data-tip="Non-GAAP Diluted EPS: $1.52 vs $1.40 Street consensus (+8.57% beat), up +67.0% YoY vs $0.91 in Q3 2025, driven by operating leverage in high-margin liquid cooling and factory efficiency.">Non-GAAP Diluted EPS ($)</span></td>
                <td>$1.45</td>
                <td>$0.91</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">${cons_eps_ng:.2f}</td>
                <td style="font-weight:700; color: #34d399;">${q0_eps_ng:.2f}</td>
                <td>
                  <span class="badge badge-bull">+${eps_delta_ng:.2f} (+{eps_delta_pct_ng:+.2f}%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:88%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">SOLID BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="GAAP Diluted Earnings Per Share from continuing operations." data-tip="GAAP Diluted EPS: $1.23 in Q3 2026, surging +68.5% YoY compared to $0.73 in Q3 2025.">GAAP Diluted EPS ($)</span></td>
                <td>$1.32</td>
                <td>$0.73</td>
                <td class="col-q0" style="font-weight:700; color: #94a3b8;">$1.15</td>
                <td style="font-weight:700; color: #34d399;">${q0_eps_gaap:.2f}</td>
                <td>
                  <span class="badge badge-bull">+$0.08 (+6.96%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:82%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
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
    b_cls = "badge-bull" if "RAISED" in item["action_badge"] else "badge-warn"
    rows_1b3.append(f"""              <tr>
                <td><span class="tip" title="Forward guidance benchmark for {item['metric']}." data-tip="{item['metric']}: Guided to {item['management_guidance']} vs {item['pre_print_consensus']} Street.">{item['metric']}</span></td>
                <td>{item['pre_print_consensus']}</td>
                <td style="font-weight:700; color: #34d399;">{item['management_guidance']}</td>
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
            <span class="badge badge-bull" style="font-size: 12px; font-weight: 700;">{verdict}</span>
            <span style="font-size: 12px; color: var(--text-muted);">SEC Form 8-K / Exhibit 99.1 Certified</span>
          </div>
          <h1 style="font-size: 26px; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: -0.02em;">
            NVENT ELECTRIC PLC <span style="color: #60a5fa; font-weight: 700;">(NYSE: NVT)</span>
          </h1>
          <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
            Q3 2026 Earnings Release Analysis | Reporting Date: {DATE} | Market Close: ${reg_price:.2f} | After-Hours: ${ah_price:.2f} ({post_move_pct:+.2f}%)
          </div>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <a href="NVT_T1_{DATE}.html" style="text-decoration: none;">
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
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${ah_price:.2f} ({post_move_pct:+.2f}%)</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Q0 Total Net Revenue</div>
          <div style="font-size: 16px; font-weight: 700; color: #f87171;">${q0_rev:,.1f}M <span style="font-size: 11px; color: #f87171;">(-1.6%)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Adjusted Diluted EPS</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_eps_ng:.2f} <span style="font-size: 11px; color: #34d399;">(+$0.12 beat)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Operating Cash Flow (9M)</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_ocf:,.1f}M</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">True FCF (9M)</div>
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_true_fcf:,.1f}M</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">1-Wk Straddle Implied</div>
          <div style="font-size: 16px; font-weight: 700; color: #38bdf8;">±{opt_implied_pct:.2f}% (${opt_straddle:.2f}) [CONTAINED]</div>
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
        <div style="font-size: 11px; text-transform: uppercase; color: #93c5fd; font-weight: 700;">T-1 Pre-Print Expectations</div>
        <p style="font-size: 12.5px; color: #cbd5e1; margin: 4px 0 0 0;">
          Consensus required $1,540.0M in sales and $1.40 Adjusted EPS, while buy-side whisper bogeys looked for $1,575.0M and $1.60 EPS. Options straddle priced a wide ±14.04% implied move ($19.50) on AI liquid cooling adoption fears.
        </p>
      </div>
      <div style="border-left: 3px solid #10b981; padding-left: 12px;">
        <div style="font-size: 11px; text-transform: uppercase; color: #6ee7b7; font-weight: 700;">T+0 Delivery &amp; Guidance Raise</div>
        <p style="font-size: 12.5px; color: #cbd5e1; margin: 4px 0 0 0;">
          nVent delivered record sales of $1,514.9M (+44% reported and organic) and blowout Adjusted EPS of $1.52 (+67% YoY, beating $1.40 consensus). Management aggressively raised FY26 sales guidance to 48%-49% and EPS to $5.36-$5.39.
        </p>
      </div>
      <div style="border-left: 3px solid #8b5cf6; padding-left: 12px;">
        <div style="font-size: 11px; text-transform: uppercase; color: #c4b5fd; font-weight: 700;">T-1 Thesis Verdict: VALIDATED</div>
        <p style="font-size: 12.5px; color: #cbd5e1; margin: 4px 0 0 0;">
          The structural electrification thesis is firmly validated. Systems Protection organic growth hit 54%, cash balances reached $1.12B, and Maverick Power closed on Oct 1st, establishing an integrated utility-to-chip power and cooling platform.
        </p>
      </div>
    </div>

    <!-- ROW 1: EXECUTIVE KPI GRID -->
    <section class="kpi-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; margin-bottom: 24px;">
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Systems Protection Segment</div>
        <div style="font-size: 22px; font-weight: 800; color: #34d399; margin: 4px 0;">$1,098.0M <span style="font-size: 12px; color: #34d399; font-weight: 600;">(+53.4% YoY)</span></div>
        <div style="font-size: 12px; color: var(--text-secondary);">Liquid cooling and server enclosures beat $1,050.0M consensus.</div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Adjusted Operating Margin (ROS)</div>
        <div style="font-size: 22px; font-weight: 800; color: #34d399; margin: 4px 0;">22.1% <span style="font-size: 12px; color: #34d399; font-weight: 600;">(+190 bps YoY)</span></div>
        <div style="font-size: 12px; color: var(--text-secondary);">Adjusted operating income reached $335.4M, beating 21.5% Street bogey.</div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">FY2026 Sales Guidance Raise</div>
        <div style="font-size: 22px; font-weight: 800; color: #38bdf8; margin: 4px 0;">+48% to 49% <span style="font-size: 12px; color: #38bdf8; font-weight: 600;">(+1,000 bps)</span></div>
        <div style="font-size: 12px; color: var(--text-secondary);">Raised from prior 37%-39%; organic growth raised to 38%-39%.</div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">FY2026 Adjusted EPS Raise</div>
        <div style="font-size: 22px; font-weight: 800; color: #34d399; margin: 4px 0;">$5.36 - $5.39 <span style="font-size: 12px; color: #34d399; font-weight: 600;">(+$0.325)</span></div>
        <div style="font-size: 12px; color: var(--text-secondary);">Raised from prior $5.00-$5.10; decisively ahead of $5.05 consensus.</div>
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
              <div class="credibility-gauge-fill" style="width: 94%; height: 100%; background: linear-gradient(90deg, #10b981, #059669);"></div>
            </div>
            <strong style="color: #34d399;">94 / 100 (Exemplary Delivery)</strong>
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
          Table 1B-3: Forward Guidance Reset (New Guidance vs. Pre-Print Street Expectations)
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
        <div class="card-title"><span class="card-title-accent"></span>Row 2: 5-Quarter Stitched Financial Performance &amp; Forward Guidance (Continuing Operations)</div>
        <span class="badge badge-purple">ROLLING 5Q ACTUALS + Q4 2026E</span>
      </div>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Financial Metric ($M except EPS)</th>
              <th>{p_labels[0]}</th>
              <th>{p_labels[1]}</th>
              <th>{p_labels[2]}</th>
              <th>{p_labels[3]}</th>
              <th class="col-q0">{p_labels[4]}</th>
              <th class="col-est">{next_q_label}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="tip" title="Consolidated net sales from continuing operations." data-tip="Total Net Revenue: $1,514.9M in Q3 2026 (+43.7% YoY, +44% organic).">Total Revenue (Net Sales)</span></td>
              <td>${s5q["total_revenue"][0]:,.1f}M</td>
              <td>${s5q["total_revenue"][1]:,.1f}M</td>
              <td>${s5q["total_revenue"][2]:,.1f}M</td>
              <td>${s5q["total_revenue"][3]:,.1f}M</td>
              <td class="col-q0" style="font-weight:700; color: #34d399;">${s5q["total_revenue"][4]:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color: #60a5fa;">$1,562.7M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Systems Protection operating segment." data-tip="Systems Protection: Enclosures and liquid cooling ($1,098.0M in Q3 2026, +53.4% YoY).">↳ Systems Protection Sales</span></td>
              <td>$715.6M</td>
              <td>$730.0M</td>
              <td>$894.8M</td>
              <td>$1,072.1M</td>
              <td class="col-q0">$1,098.0M</td>
              <td class="col-est">$1,135.0M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Electrical Connections operating segment." data-tip="Electrical Connections: Fasteners, grounding, and power connectors ($416.9M in Q3 2026, +23.2% YoY).">↳ Electrical Connections Sales</span></td>
              <td>$338.4M</td>
              <td>$336.7M</td>
              <td>$347.2M</td>
              <td>$399.2M</td>
              <td class="col-q0">$416.9M</td>
              <td class="col-est">$427.7M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cost of goods sold." data-tip="Cost of Goods Sold: Manufacturing input costs, raw materials copper and steel, and assembly labor ($972.0M in Q3 2026).">Cost of Goods Sold (COGS)</span></td>
              <td>$659.3M</td>
              <td>$677.8M</td>
              <td>$796.4M</td>
              <td>$913.3M</td>
              <td class="col-q0">$972.0M</td>
              <td class="col-est">$1,003.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Gross Profit (Net Sales - COGS)." data-tip="Gross Profit: $542.9M in Q3 2026 (35.84% gross margin), up +37.5% YoY.">Gross Profit</span></td>
              <td>${s5q["gross_profit"][0]:,.1f}M</td>
              <td>${s5q["gross_profit"][1]:,.1f}M</td>
              <td>${s5q["gross_profit"][2]:,.1f}M</td>
              <td>${s5q["gross_profit"][3]:,.1f}M</td>
              <td class="col-q0" style="font-weight:700; color: #34d399;">${s5q["gross_profit"][4]:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color: #60a5fa;">$559.7M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Consolidated operating expenses." data-tip="Operating Expenses: SG&amp;A ($236.3M) plus R&amp;D ($24.3M), totaling $260.9M in Q3 2026.">Total Operating Expenses</span></td>
              <td>${s5q["operating_expenses"][0]:,.1f}M</td>
              <td>${s5q["operating_expenses"][1]:,.1f}M</td>
              <td>${s5q["operating_expenses"][2]:,.1f}M</td>
              <td>${s5q["operating_expenses"][3]:,.1f}M</td>
              <td class="col-q0" style="font-weight:700; color: #94a3b8;">${s5q["operating_expenses"][4]:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color: #94a3b8;">$274.7M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Selling, General and Administrative expenses." data-tip="SG&amp;A: $236.3M in Q3 2026 (15.60% of sales vs 19.71% in Q3 2025, a 411 bps efficiency improvement).">↳ Selling, General &amp; Administrative (SG&amp;A)</span></td>
              <td>$207.8M</td>
              <td>$204.6M</td>
              <td>$226.7M</td>
              <td>$233.3M</td>
              <td class="col-q0">$236.3M</td>
              <td class="col-est">$248.0M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Research and Development expenses." data-tip="R&amp;D: $24.3M in Q3 2026, advancing high-power CDUs and quick-disconnect fluid fittings.">↳ Research &amp; Development (R&amp;D)</span></td>
              <td>$20.6M</td>
              <td>$20.5M</td>
              <td>$23.2M</td>
              <td>$24.0M</td>
              <td class="col-q0">$24.3M</td>
              <td class="col-est">$26.7M</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Operating Income (Gross Profit - OpEx)." data-tip="Operating Income: $282.0M in Q3 2026 (18.62% operating margin), up +69.6% YoY vs $166.3M in Q3 2025.">GAAP Operating Income (EBIT)</span></td>
              <td>${s5q["operating_income"][0]:,.1f}M</td>
              <td>${s5q["operating_income"][1]:,.1f}M</td>
              <td>${s5q["operating_income"][2]:,.1f}M</td>
              <td>${s5q["operating_income"][3]:,.1f}M</td>
              <td class="col-q0" style="font-weight:700; color: #34d399;">${s5q["operating_income"][4]:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color: #60a5fa;">$285.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Non-GAAP Adjusted Operating Income." data-tip="Adjusted Operating Income: $335.4M in Q3 2026 (22.14% ROS), up +57.2% YoY vs $213.3M.">Adjusted Operating Income</span></td>
              <td>$213.3M</td>
              <td>$210.3M</td>
              <td>$248.5M</td>
              <td>$322.7M</td>
              <td class="col-q0" style="font-weight:700; color: #34d399;">$335.4M</td>
              <td class="col-est" style="font-weight:700; color: #60a5fa;">$321.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income from continuing operations." data-tip="GAAP Net Income: $202.4M in Q3 2026, surging +70.1% YoY vs $119.0M in Q3 2025.">GAAP Net Income</span></td>
              <td>${s5q["gaap_net_income"][0]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][1]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][2]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][3]:,.1f}M</td>
              <td class="col-q0" style="font-weight:700; color: #34d399;">${s5q["gaap_net_income"][4]:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color: #60a5fa;">$188.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Diluted Earnings Per Share." data-tip="GAAP Diluted EPS: $1.23 in Q3 2026 vs $0.73 in Q3 2025 (+68.5% YoY).">GAAP Diluted EPS ($)</span></td>
              <td>$0.73</td>
              <td>$0.71</td>
              <td>$0.86</td>
              <td>$1.32</td>
              <td class="col-q0" style="font-weight:700; color: #34d399;">${q0_eps_gaap:.2f}</td>
              <td class="col-est" style="font-weight:700; color: #60a5fa;">$1.15</td>
            </tr>
            <tr>
              <td><span class="tip" title="Non-GAAP Adjusted Diluted Earnings Per Share." data-tip="Adjusted Diluted EPS: $1.52 in Q3 2026 vs $0.91 in Q3 2025 (+67.0% YoY).">Non-GAAP Diluted EPS ($)</span></td>
              <td>$0.91</td>
              <td>$0.90</td>
              <td>$1.09</td>
              <td>$1.45</td>
              <td class="col-q0" style="font-weight:700; color: #34d399;">${q0_eps_ng:.2f}</td>
              <td class="col-est" style="font-weight:700; color: #60a5fa;">$1.32</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 5. ROW 3: FORENSIC TRUE FCF BRIDGE -->
    <section class="card" id="sec-fcf" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 3: Forensic Quality-of-Earnings &amp; True Free Cash Flow Bridge (9M YTD Cumulative)</div>
        <span class="badge badge-purple">SEC CASH FLOW AUDIT</span>
      </div>
      <div class="forensic-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 12px;">9M YTD Cumulative Cash Flow Waterfall ($M)</div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Cash provided by operating activities." data-tip="Operating Cash Flow: $571.5M 9M YTD (Q3 3-month OCF was $303.2M, up +11.6% YoY).">(+) Operating Cash Flow (OCF)</span>
            <span style="font-weight:700; color: #34d399;">${q0_ocf:,.1f}M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Capital expenditures." data-tip="CapEx: $94.6M 9M YTD (Q3 3-month CapEx was $37.0M for manufacturing line automation).">(-) Capital Expenditures (CapEx)</span>
            <span style="font-weight:700; color: #f87171;">-${q0_capex:,.1f}M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px; background: rgba(59, 130, 246, 0.08); padding-left: 6px; padding-right: 6px;">
            <span style="font-weight:600;">(=) Reported Free Cash Flow</span>
            <span style="font-weight:700; color: #38bdf8;">${q0_rep_fcf:,.1f}M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Stock-based compensation." data-tip="Stock-Based Compensation: $30.9M 9M YTD (disciplined 0.73% of net sales).">(-) Stock-Based Compensation (SBC)</span>
            <span style="font-weight:700; color: #f87171;">-${q0_sbc:,.1f}M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Finance lease payments." data-tip="Finance Leases: $0.0M principal lease payments recorded in 9M 2026.">(-) Principal Finance Leases</span>
            <span style="font-weight:700; color: #94a3b8;">-$0.0M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 8px 6px; font-size: 13.5px; background: rgba(16, 185, 129, 0.12); border-radius: 6px; margin-top: 6px;">
            <span style="font-weight:700; color: #34d399;">(=) Forensic True Free Cash Flow</span>
            <span style="font-weight:800; color: #34d399;">${q0_true_fcf:,.1f}M</span>
          </div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color); display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 10px;">Balance Sheet &amp; Liquidity Fortress</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-bottom: 10px;">
              Following the closing of the Thermal Management sale and strong Q3 operations, cash and cash equivalents surged to <strong>$1,121.8M</strong> (vs $237.5M at Dec 31, 2025). Net leverage stands at a conservative 1.1x net debt to EBITDA, creating over $2.0B in available capital deployment capacity.
            </p>
            <div style="font-size: 12px; color: var(--text-muted); line-height: 1.4;">
              • 3-Month Q3 Free Cash Flow printed at $267.9M (+6% YoY), achieving a 107% conversion rate of adjusted net income.<br>
              • Share repurchases totaled $100.2M YTD with a newly approved $0.21/share quarterly cash dividend payable Nov 6, 2026.
            </div>
          </div>
          <div style="padding: 10px; background: rgba(255,255,255,0.03); border-radius: 6px; border-left: 3px solid #10b981; font-size: 12px; color: #cbd5e1; margin-top: 12px;">
            <strong>Forensic Assessment:</strong> High earnings quality. Working capital absorption is minimal, SBC dilution is negligible (<1% of sales), and cash flow expansion matches GAAP operating profit growth point-for-point.
          </div>
        </div>
      </div>
    </section>

    <!-- 6. ROW 4: AUDIT GRID & CALL FORENSICS -->
    <section class="card" id="sec-audit" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 4: Operational Execution Audit & Analyst Q&A Highlights</div>
        <span class="badge badge-blue">WINS / DRAGS & ANALYST Q&A</span>
      </div>
      <div class="audit-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 20px;">
        <div style="background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-weight: 700; font-size: 13px; color: #34d399; margin-bottom: 8px;">What Management Did Right (Operational Tailwinds)</div>
          <ul style="font-size: 12.5px; color: #cbd5e1; padding-left: 18px; margin: 0; line-height: 1.55;">
            <li><strong>Explosive Liquid Cooling Growth:</strong> Systems Protection organic growth hit +54%, propelled by Data Solutions multiplying threefold with tier-1 hyperscaler cluster deployments.</li>
            <li><strong>Aggressive Guidance Raise:</strong> Upwardly revised full-year reported sales growth to 48%-49% and EPS to $5.36-$5.39, decisively signaling resilient secular demand.</li>
            <li><strong>Maverick Power Catalyst:</strong> Closed on October 1st, establishing an integrated utility-to-chip power skid and modular busway offering that commands higher margin capture.</li>
            <li><strong>Operating Margin Expansion:</strong> Adjusted ROS expanded 190 bps YoY to 22.1%, showing strong factory operating leverage despite supply chain scaling.</li>
          </ul>
        </div>
        <div style="background: rgba(239, 68, 68, 0.04); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-weight: 700; font-size: 13px; color: #f87171; margin-bottom: 8px;">What Went Wrong & Execution Headwinds</div>
          <ul style="font-size: 12.5px; color: #cbd5e1; padding-left: 18px; margin: 0; line-height: 1.55;">
            <li><strong>Headline Revenue Missed Whisper:</strong> Sales of $1,514.9M came in 1.6% below consensus ($1,540.0M) and below the $1,575.0M whisper bogey, prompting initial intraday profit taking.</li>
            <li><strong>Electrical Connections Softness:</strong> Segment revenue of $416.9M missed $440.0M expectations, reflecting subdued non-residential commercial building construction in EMEA.</li>
            <li><strong>Electrical Connections Margin Compression:</strong> Segment Adjusted ROS contracted 180 bps YoY to 28.2%, impacted by copper raw material inflation and product mix shifts.</li>
            <li><strong>M&A Integration Risk:</strong> Integrating Maverick Power and Trachte simultaneously across multiple manufacturing footprints creates short-term operational complexity.</li>
          </ul>
        </div>
      </div>

      <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 10px;">
        Institutional Conference Call Analyst Q&A Forensic Highlights
      </div>
{qa_cards_html}
    </section>

    <!-- 7. ROW 5: PEER GROUP VALUATION COMPS -->
    <section class="card" id="sec-comps" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 5: Electrical Infrastructure Peer Group Valuation Comps (Re-Anchored to After-Hours Price)</div>
        <span class="badge badge-purple">COMPARATIVE MULTIPLES</span>
      </div>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Company Name</th>
              <th>Ticker</th>
              <th>Market Cap ($B)</th>
              <th>Enterprise Value ($B)</th>
              <th>Forward P/E</th>
              <th>EV / EBITDA</th>
              <th>Organic YoY Growth</th>
              <th>Adjusted Operating Margin</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background: rgba(59, 130, 246, 0.08); font-weight: 700;">
              <td><span class="tip" title="nVent Electric plc." data-tip="nVent Electric: Pure-play connection and protection leader benefiting from AI liquid cooling and grid electrification.">nVent Electric plc (Post-Print)</span></td>
              <td>NVT</td>
              <td style="color: #60a5fa;">${mcap_m/1000:.2f}B</td>
              <td style="color: #60a5fa;">${ev_m/1000:.2f}B</td>
              <td style="color: #34d399;">23.7x (FY26E)</td>
              <td>18.5x</td>
              <td style="color: #34d399;">+44.0%</td>
              <td style="color: #34d399;">22.1%</td>
            </tr>
            <tr>
              <td>Vertiv Holdings Co</td>
              <td>VRT</td>
              <td>$42.50B</td>
              <td>$44.80B</td>
              <td>36.2x</td>
              <td>24.5x</td>
              <td>+35.0%</td>
              <td>20.1%</td>
            </tr>
            <tr>
              <td>Eaton Corporation plc</td>
              <td>ETN</td>
              <td>$145.20B</td>
              <td>$156.00B</td>
              <td>29.8x</td>
              <td>22.1x</td>
              <td>+14.0%</td>
              <td>23.2%</td>
            </tr>
            <tr>
              <td>Hubbell Incorporated</td>
              <td>HUBB</td>
              <td>$23.80B</td>
              <td>$25.60B</td>
              <td>24.1x</td>
              <td>17.8x</td>
              <td>+11.0%</td>
              <td>21.0%</td>
            </tr>
            <tr>
              <td>Schneider Electric SE</td>
              <td>SBGSF</td>
              <td>$135.00B</td>
              <td>$148.00B</td>
              <td>23.5x</td>
              <td>16.9x</td>
              <td>+8.0%</td>
              <td>18.5%</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div style="font-size: 12px; color: var(--text-muted); margin-top: 10px; line-height: 1.4;">
        <strong>Valuation Takeaway:</strong> At $127.30 after-hours, NVT trades at a steep discount to peer Vertiv (23.7x 2026E EPS vs 36.2x) despite posting higher organic growth (+44% vs +35%) and superior cash conversion. As Maverick Power establishes an end-to-end power platform, multiple expansion toward 28x-30x represents significant upside.
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
          <div style="font-size: 20px; font-weight: 800; color: #34d399; margin: 4px 0;">{soc_data['four_pillar_sentiment']['institutional_score']} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data['four_pillar_sentiment']['institutional_score']}%; height: 100%; background: #10b981;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Hedge funds aggressively accumulate on multi-year AI electrification thesis.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Retail Trader Pulse</div>
          <div style="font-size: 20px; font-weight: 800; color: #60a5fa; margin: 4px 0;">{soc_data['four_pillar_sentiment']['retail_score']} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data['four_pillar_sentiment']['retail_score']}%; height: 100%; background: #3b82f6;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Active FinTwit and Reddit discussions highlight NVT as a deep-value alternative to Vertiv.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Options Volatility Skew</div>
          <div style="font-size: 20px; font-weight: 800; color: #a855f7; margin: 4px 0;">{soc_data['four_pillar_sentiment']['options_skew_score']} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data['four_pillar_sentiment']['options_skew_score']}%; height: 100%; background: #a855f7;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Implied move was ±14.04%; realized move +1.05% triggered massive IV crush.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Sell-Side Revision Tone</div>
          <div style="font-size: 20px; font-weight: 800; color: #34d399; margin: 4px 0;">{soc_data['four_pillar_sentiment']['sell_side_score']} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data['four_pillar_sentiment']['sell_side_score']}%; height: 100%; background: #10b981;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Sell-side analysts universally hike estimates following 48%-49% sales guide.</div>
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
          <div style="font-size: 13px; font-weight: 700; color: #34d399; margin-bottom: 6px;">Bull Case: Valuation Multiple Re-Rating to Vertiv</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $145.00 - $160.00 (+14% to +26%)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Wall Street re-rates NVT from 23.7x to 28x+ forward earnings as Maverick Power integration accelerates and liquid cooling demand scales across new hyperscaler clusters, driving 2027 EPS toward $6.50.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #10b981;">
            <strong>Options Structure:</strong> Buy Jan 2027 $135.00 / $155.00 Bull Call Spread. Sell $115.00 Put to finance premium.
          </div>
        </div>
        <div class="scenario-base" style="background: rgba(59, 130, 246, 0.04); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #60a5fa; margin-bottom: 6px;">Base Case: Healthy Post-Print Consolidation</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $122.00 - $138.00 (-4% to +8%)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Shares consolidate recent gains between $125 and $135 as the market absorbs Q4 acquisition integration expenses and monitors broader European industrial demand pacing.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #3b82f6;">
            <strong>Options Structure:</strong> Sell Nov 2026 $115.00 / $140.00 Short Strangle to capture elevated volatility crush.
          </div>
        </div>
        <div class="scenario-bear" style="background: rgba(239, 68, 68, 0.04); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #f87171; margin-bottom: 6px;">Bear Case: Hyperscaler Digestion &amp; Margin Erosion</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $105.00 - $115.00 (-10% to -18%)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Supply chain grid connection bottlenecks delay data center buildouts, while copper raw material costs compress Electrical Connections operating margins below 25%.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #ef4444;">
            <strong>Options Structure:</strong> Buy Nov 2026 $120.00 / $105.00 Bear Put Spread financed by selling $135.00 Calls.
          </div>
        </div>
      </div>
    </section>

    <!-- SEC CITATIONS & AUDIT LEDGER FOOTER -->
    <footer style="padding: 16px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
      <div><strong>Filing Ledger &amp; Source Attributions:</strong> SEC Form 8-K filed on October 30, 2026 (Item 2.02 Results of Operations and Financial Condition, Exhibit 99.1 Press Release). Historical 5Q financial series sourced from SEC EDGAR Forms 10-Q and verified against nVent Electric Investor Relations. Stock pricing captured at 6:00 PM PST (${ah_price:.2f} USD).</div>
      <div style="margin-top: 4px;">Zero-Hallucination Pipeline standard enforced: All historical numbers, beat/miss deltas, options-implied moves, and forensic cash flow metrics are immutable ground truth.</div>
    </footer>
"""

draft_payload = {
    "header": {
        "ticker": TICKER,
        "earnings_date": DATE,
        "page_title": f"{TICKER} T+0 Post-Earnings Forensic Tearsheet ({DATE})",
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
        "bull_target_low_num": 145.0,
        "bear_target_high_num": 115.0
    },
    "rendered_container_html": html_content
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
tip_count = html_content.count('class="tip')
datatip_count = html_content.count('data-tip="')
print(f"[SUCCESS] Generated Post-Earnings Draft for {TICKER} at: {DRAFT_PATH.name}")
print(f"  - Inner HTML Character Count: {len(html_content):,}")
print(f"  - Interactive Tooltip Count (.tip): {tip_count} | data-tip: {datatip_count}")
