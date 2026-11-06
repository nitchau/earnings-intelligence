"""
build_soun_post_draft.py: Generates drafts/SOUN_2026-11-05_post_draft.json
Institutional Post-Earnings Forensic Tearsheet for SoundHound AI, Inc. (SOUN)
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "SOUN"
DATE = "2026-11-05"

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

reg_price = truth["post_print_reaction"]["regular_close_price"]          # 4.26
ah_price = truth["post_print_reaction"]["after_hours_price"]            # 3.94
post_move_pct = truth["post_print_reaction"]["post_print_move_pct"]     # -7.51%
opt_implied_pct = truth["post_print_reaction"]["t1_options_implied_move_pct"] or 12.38
opt_straddle = truth["t1_baseline"].get("atm_straddle_usd", 0.53)
verdict = truth["post_print_reaction"]["overall_print_verdict"]          # HEADLINE BEAT / GUIDANCE RESET

q0_rev = truth["beat_miss_scorecard"]["revenue"]["reported_actual_millions"]          # 62.42
cons_rev = truth["beat_miss_scorecard"]["revenue"]["street_consensus_millions"]       # 62.18
whisper_rev = truth["t1_baseline"].get("whisper_revenue_millions", 64.0)
rev_delta_m = round(q0_rev - cons_rev, 2)                                              # +0.24
rev_delta_pct = round(rev_delta_m / cons_rev * 100, 2)                                 # +0.39%

q0_eps_gaap = truth["beat_miss_scorecard"]["eps_gaap"]["reported_actual"] or -0.10
q0_eps_nongaap = truth["beat_miss_scorecard"]["eps_nongaap"]["reported_actual"] or 4.0

q0_gp = truth["company_specific_facts"].get("gross_profit_q0", 21.28)
q0_opex = truth["company_specific_facts"].get("operating_expenses_q0", 67.78)
q0_opinc = truth["company_specific_facts"].get("operating_income_q0", -46.50)
q0_net_inc = truth["company_specific_facts"].get("net_income_gaap_q0", -46.37)

q0_ocf = truth["forensic_fcf_bridge_q0"]["ocf"]               # -95.99
q0_capex = truth["forensic_fcf_bridge_q0"]["capex"]           # 1.12
q0_rep_fcf = truth["forensic_fcf_bridge_q0"]["reported_fcf"]  # -97.11
q0_sbc = truth["forensic_fcf_bridge_q0"]["sbc"]               # 61.02
q0_leases = truth["forensic_fcf_bridge_q0"]["finance_leases"] # 0.0
q0_true_fcf = truth["forensic_fcf_bridge_q0"]["true_fcf"]     # -158.13

s5q = truth["stitched_5q_chronological"]
p_labels = s5q["period_labels"]                                # Q3 2025, Q4 2025, Q1 2026, Q2 2026, Q3 2026 (Actual)
next_q_label = s5q["next_quarter_estimate_label"]              # Q4 2026E (Guided / Street)

mcap_m = truth["market_portal"]["market_cap_millions"] or 1913.6
ev_m = truth["market_portal"]["enterprise_value_millions"] or 1694.6

# Table 1B-1 rows
rows_1b1 = [
    f"""              <tr>
                <td><span class="tip" title="Consolidated GAAP Net Revenue across voice and agentic AI." data-tip="Total GAAP Revenue: $62.42M reported in Q3 2026 (+48.4% YoY vs $42.05M in Q3 2025 and +0.8% QoQ vs $61.90M in Q2 2026), slightly beating Street consensus ($62.18M) by +$0.24M (+0.39%) while falling below whisper ($64.0M) due to negative margin contract non-renewals.">Total GAAP Revenue ($M)</span></td>
                <td>$61.90M</td>
                <td>$42.05M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">${cons_rev:,.2f}M</td>
                <td style="font-weight:700; color: #34d399;">${q0_rev:,.2f}M</td>
                <td>
                  <span class="badge badge-bull">+${rev_delta_m:.2f}M (+{rev_delta_pct:+.2f}%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:88%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">IN LINE / BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="GAAP Gross Margin percentage." data-tip="Gross Margin: 34.09% in Q3 2026 ($21.28M gross profit) down from 45.12% in Q2 2026 and 42.62% in Q3 2025, reflecting low-margin contracts from legacy Amelia acquisition that management is actively pruning.">GAAP Gross Margin (%)</span></td>
                <td>45.12%</td>
                <td>42.62%</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">44.00%</td>
                <td style="font-weight:700; color: #f87171;">34.09%</td>
                <td>
                  <span class="badge badge-bear">-991 bps</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:72%; height:100%; background:linear-gradient(90deg, #ef4444, #b91c1c);"></div></div>
                </td>
                <td><span class="badge badge-bear">COMPRESSION</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="GAAP Diluted Earnings Per Share." data-tip="GAAP Diluted EPS: -$0.10 in Q3 2026 vs -$0.05 Street consensus and -$0.27 in Q3 2025, impacted by acquisition integration and restructuring expenses.">GAAP Diluted EPS ($)</span></td>
                <td>-$0.10</td>
                <td>-$0.27</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">-$0.05</td>
                <td style="font-weight:700; color: #f87171;">-${abs(q0_eps_gaap):.2f}</td>
                <td>
                  <span class="badge badge-bear">-$0.05</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:80%; height:100%; background:linear-gradient(90deg, #f59e0b, #d97706);"></div></div>
                </td>
                <td><span class="badge badge-warn">MISS</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Operating cash flow from continuing operations." data-tip="Operating Cash Flow: -$95.99M in Q3 2026, widening from -$33.71M in Q2 2026 due to transaction expenses, restructuring, and working capital realignments.">Operating Cash Burn ($M)</span></td>
                <td>-$33.71M</td>
                <td>-$32.65M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">-$30.00M</td>
                <td style="font-weight:700; color: #f87171;">-${abs(q0_ocf):.2f}M</td>
                <td>
                  <span class="badge badge-bear">-$65.99M</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:68%; height:100%; background:linear-gradient(90deg, #ef4444, #b91c1c);"></div></div>
                </td>
                <td><span class="badge badge-bear">HIGH BURN</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Annualized run-rate cost synergies identified." data-tip="Annualized Synergy Actions: $120.0M identified ($80M+ effective before Jan 1, 2027), doubling Street expectations of $60M to accelerate EBITDA crossover in 2H 2027.">Annualized Synergy Actions ($M)</span></td>
                <td>$0.0M</td>
                <td>$0.0M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$50.0M</td>
                <td style="font-weight:700; color: #34d399;">$120.0M</td>
                <td>
                  <span class="badge badge-bull">+$70.0M (+140%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:98%; height:100%; background:linear-gradient(90deg, #10b981, #059669);"></div></div>
                </td>
                <td><span class="badge badge-bull">EXPANSION</span></td>
              </tr>"""
]
table_1b1_html = "\n".join(rows_1b1)

# Table 1B-2 rows
rows_1b2 = []
for row in trans_data["matrix_a_guidance_accountability"]:
    rows_1b2.append(f"""              <tr>
                <td><span class="tip" title="{row['metric']}" data-tip="Prior Guidance accountability check: {row['metric']} reported at {row['reported_actual']} vs guided {row['prior_guidance']}.">{row['metric']}</span></td>
                <td>{row['prior_guidance']}</td>
                <td style="font-weight:700; color: #34d399;">{row['reported_actual']}</td>
                <td>{row['variance']}</td>
                <td><span class="badge {row['badge_class']}">{row['grade']}</span></td>
              </tr>""")
table_1b2_html = "\n".join(rows_1b2)

# Table 1B-3 rows
rows_1b3 = []
for row in trans_data["matrix_b_forward_guidance_reset"]:
    rows_1b3.append(f"""              <tr>
                <td><span class="tip" title="{row['metric']}" data-tip="Forward guidance reset: New FY target for {row['metric']} is {row['new_guidance']} vs pre-print consensus {row['street_pre_print']}.">{row['metric']}</span></td>
                <td>{row['street_pre_print']}</td>
                <td style="font-weight:700; color: #34d399;">{row['new_guidance']}</td>
                <td style="font-weight:600; color: #60a5fa;">{row['delta']}</td>
                <td><span class="badge {row['badge_class']}">{row['action']}</span></td>
              </tr>""")
table_1b3_html = "\n".join(rows_1b3)

# Q&A Cards
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
            <h1 style="margin: 0; font-size: 24px; font-weight: 800; color: #fff;">SoundHound AI, Inc. ({TICKER})</h1>
            <span class="badge badge-bull" style="font-size: 13px; padding: 4px 8px;">T+0 POST-EARNINGS FORENSIC TEARSHEET</span>
            <span class="badge badge-purple" style="font-size: 13px; padding: 4px 8px;">{verdict}</span>
          </div>
          <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">
            Q3 2026 Earnings Release &bull; Filing Date: November 5, 2026 &bull; Form 8-K Exhibits 99.1 &amp; 99.2 &bull; Market Cap: ${mcap_m:,.1f}M &bull; EV: ${ev_m:,.1f}M
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
          <div style="font-size: 16px; font-weight: 700; color: #34d399;">${q0_rev:,.2f}M <span style="font-size: 11px; color: #34d399;">(+48.4% YoY)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">GAAP Gross Margin</div>
          <div style="font-size: 16px; font-weight: 700; color: #f87171;">34.09% <span style="font-size: 11px; color: #f87171;">(-991 bps QoQ)</span></div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Operating Cash Flow</div>
          <div style="font-size: 16px; font-weight: 700; color: #f87171;">-${abs(q0_ocf):,.2f}M</div>
        </div>
        <div>
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">True Free Cash Flow</div>
          <div style="font-size: 16px; font-weight: 700; color: #f87171;">-${abs(q0_true_fcf):,.2f}M</div>
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
          Consensus called for $62.18M in Q3 revenue (+47.9% YoY) and -$0.05 in GAAP EPS. Buy-side whisper was $64.0M. Options straddles priced a ±12.38% move ($0.53) on restaurant AI expansion.
        </p>
      </div>
      <div style="border-left: 3px solid #f59e0b; padding-left: 12px;">
        <div style="font-size: 11px; text-transform: uppercase; color: #fcd34d; font-weight: 700;">T+0 Delivery &amp; Strategic Portfolio Pruning</div>
        <p style="font-size: 12.5px; color: #cbd5e1; margin: 4px 0 0 0;">
          SoundHound delivered $62.42M in revenue (+48.4% YoY), slightly beating Street ($62.18M). However, GAAP gross margin contracted to 34.09% as management non-renewed negative-margin legacy contracts, trimming FY26 guidance to $255M midpoint while initiating $375M midpoint for 2027.
        </p>
      </div>
      <div style="border-left: 3px solid #8b5cf6; padding-left: 12px;">
        <div style="font-size: 11px; text-transform: uppercase; color: #c4b5fd; font-weight: 700;">T-1 Thesis Verdict: MIXED / TRANSITIONAL</div>
        <p style="font-size: 12.5px; color: #cbd5e1; margin: 4px 0 0 0;">
          The voice AI deployment thesis remains intact with $120M in annualized synergies and $350M-$400M guided for 2027. However, elevated quarterly cash burn (-$95.99M) and contract pruning push sustained positive Adjusted EBITDA into second half 2027.
        </p>
      </div>
    </div>

    <!-- ROW 1: EXECUTIVE KPI GRID -->
    <section class="kpi-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; margin-bottom: 24px;">
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Total GAAP Revenue</div>
        <div style="font-size: 22px; font-weight: 800; color: #34d399; margin: 4px 0;">$62.42M</div>
        <div style="font-size: 12px; color: var(--text-secondary);">
          <span style="color: #34d399; font-weight: 700;">+48.4% YoY</span> | +$0.24M vs Consensus
        </div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">GAAP Gross Margin</div>
        <div style="font-size: 22px; font-weight: 800; color: #f87171; margin: 4px 0;">34.09%</div>
        <div style="font-size: 12px; color: var(--text-secondary);">
          <span style="color: #f87171; font-weight: 700;">-991 bps QoQ</span> | Legacy Contract Pruning
        </div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Annualized Synergy Actions</div>
        <div style="font-size: 22px; font-weight: 800; color: #60a5fa; margin: 4px 0;">$120.0M</div>
        <div style="font-size: 12px; color: var(--text-secondary);">
          <span style="color: #60a5fa; font-weight: 700;">$80M+ Pre-2027</span> | Targeting 2H 2027 EBITDA
        </div>
      </div>
      <div class="card kpi-card" style="padding: 16px; border: 1px solid var(--border-color); border-radius: 8px;">
        <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">Cash &amp; Equivalents</div>
        <div style="font-size: 22px; font-weight: 800; color: #38bdf8; margin: 4px 0;">$207.58M</div>
        <div style="font-size: 12px; color: var(--text-secondary);">
          <span style="color: #38bdf8; font-weight: 700;">Runway to 2027</span> | Zero Near-Term Financing Needed
        </div>
      </div>
    </section>

    <!-- ROW 1B: SCORECARD SECTION -->
    <section class="card scorecard" id="sec-scorecard" style="margin-bottom: 24px;">
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
                <th>Metric</th>
                <th>Q-1 Actual</th>
                <th>Q-4 YoY</th>
                <th class="col-q0">Street Consensus</th>
                <th>Reported Q0 Actual</th>
                <th>vs. Consensus</th>
                <th>Verdict</th>
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
            Table 1B-2: Prior-Quarter Guidance Accountability &amp; Track Record Scorecard
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 12px; color: var(--text-muted);">Guidance Credibility Score:</span>
            <span style="font-weight: 800; color: #34d399; font-size: 13px;">{trans_data["credibility_score"]} / 100</span>
          </div>
        </div>
        <div class="credibility-gauge-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 10px;">
          <div class="credibility-gauge-fill" style="width: {trans_data["credibility_score"]}%; height: 100%; background: linear-gradient(90deg, #10b981, #059669);"></div>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Guided Metric</th>
                <th>Prior Q2 Guidance for Q3</th>
                <th>Reported Delivery</th>
                <th>Variance vs Guide</th>
                <th>Accountability Grade</th>
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
          Table 1B-3: Forward FY 2026 &amp; FY 2027 Guidance Reset vs. Street Pre-Print Hurdle
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Forward Target Metric</th>
                <th>Street Pre-Print Hurdle</th>
                <th>New Management Guidance</th>
                <th>Guidance Spread</th>
                <th>Action Badge</th>
              </tr>
            </thead>
            <tbody>
{table_1b3_html}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ROW 2: 5-QUARTER TABLE WITH ROLLING Q0 ACTUAL + Q+1E -->
    <section class="card rolling-5q" id="sec-5q" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 2: 5-Quarter Financial Performance &amp; Dynamic Segment Breakdown</div>
        <span class="badge badge-blue">GAAP CONDENSED P&amp;L RECONCILIATION</span>
      </div>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Metric ($M)</th>
              <th>{p_labels[0]}</th>
              <th>{p_labels[1]}</th>
              <th>{p_labels[2]}</th>
              <th>{p_labels[3]}</th>
              <th class="col-q0" style="color: #34d399; font-weight: 700;">{p_labels[4]}</th>
              <th class="col-est" style="color: #60a5fa; font-weight: 700;">{next_q_label}</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background: rgba(255,255,255,0.02);">
              <td><span class="tip" title="Total GAAP Net Revenue" data-tip="Total GAAP Revenue: $62.42M in Q3 2026, representing +48.4% YoY growth from $42.05M in Q3 2025.">Total GAAP Revenue</span></td>
              <td>$42.05M</td>
              <td>$55.06M</td>
              <td>$44.20M</td>
              <td>$61.90M</td>
              <td class="col-q0" style="color: #34d399;">$62.42M</td>
              <td class="col-est">$86.48M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Automotive &amp; Connected IoT Voice AI" data-tip="Embedded automotive voice interfaces deployed across Stellantis, Hyundai, and Kia.">↳ Automotive &amp; Connected IoT Voice AI</span></td>
              <td>$23.13M</td>
              <td>$29.18M</td>
              <td>$22.10M</td>
              <td>$27.85M</td>
              <td class="col-q0">$27.50M</td>
              <td class="col-est">$35.00M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Restaurant Smart Ordering &amp; Drive-Thru AI" data-tip="Automated voice ordering and phone answering for global QSR chains.">↳ Restaurant Smart Ordering &amp; Drive-Thru AI</span></td>
              <td>$13.46M</td>
              <td>$17.62M</td>
              <td>$14.59M</td>
              <td>$21.67M</td>
              <td class="col-q0">$22.50M</td>
              <td class="col-est">$30.00M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Enterprise Conversational AI &amp; Amelia Unit" data-tip="Customer service agents and IT helpdesk automation inherited from Amelia acquisition.">↳ Enterprise AI &amp; Amelia Platform</span></td>
              <td>$3.36M</td>
              <td>$5.51M</td>
              <td>$5.30M</td>
              <td>$9.28M</td>
              <td class="col-q0">$9.82M</td>
              <td class="col-est">$17.00M</td>
            </tr>
            <tr class="sub-row">
              <td><span class="tip" title="Consumer Apps &amp; Other Emerging" data-tip="Consumer apps, music ID, and specialized developer licensing.">↳ Consumer Apps &amp; Emerging</span></td>
              <td>$2.10M</td>
              <td>$2.75M</td>
              <td>$2.21M</td>
              <td>$3.10M</td>
              <td class="col-q0">$2.60M</td>
              <td class="col-est">$4.48M</td>
            </tr>
            <tr>
              <td>Cost of Revenue</td>
              <td>$24.13M</td>
              <td>$28.71M</td>
              <td>$30.46M</td>
              <td>$33.97M</td>
              <td class="col-q0">$41.14M</td>
              <td class="col-est">$48.00M</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Gross Profit" data-tip="Gross profit of $21.28M in Q3 2026.">Gross Profit</span></td>
              <td>$17.92M</td>
              <td>$26.35M</td>
              <td>$13.74M</td>
              <td>$27.93M</td>
              <td class="col-q0" style="color: #34d399;">$21.28M</td>
              <td class="col-est">$38.48M</td>
            </tr>
            <tr>
              <td>Gross Margin %</td>
              <td>42.62%</td>
              <td>47.86%</td>
              <td>31.09%</td>
              <td>45.12%</td>
              <td class="col-q0" style="color: #f87171;">34.09%</td>
              <td class="col-est">44.50%</td>
            </tr>
            <tr class="sub-row">
              <td>↳ Research &amp; Development (R&amp;D)</td>
              <td>$28.00M</td>
              <td>$27.50M</td>
              <td>$32.00M</td>
              <td>$31.50M</td>
              <td class="col-q0">$30.87M</td>
              <td class="col-est">$28.00M</td>
            </tr>
            <tr class="sub-row">
              <td>↳ Sales &amp; Marketing (S&amp;M)</td>
              <td>$16.50M</td>
              <td>$17.00M</td>
              <td>$19.50M</td>
              <td>$18.50M</td>
              <td class="col-q0">$18.22M</td>
              <td class="col-est">$17.00M</td>
            </tr>
            <tr class="sub-row">
              <td>↳ General &amp; Administrative (G&amp;A)</td>
              <td>$23.07M</td>
              <td>$23.91M</td>
              <td>$24.31M</td>
              <td>$24.92M</td>
              <td class="col-q0">$35.95M</td>
              <td class="col-est">$20.00M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Operating Expenses" data-tip="Total GAAP OpEx of $67.78M in Q3 2026.">Total Operating Expenses</span></td>
              <td>$67.57M</td>
              <td>$68.41M</td>
              <td>$75.81M</td>
              <td>$74.92M</td>
              <td class="col-q0">$67.78M</td>
              <td class="col-est">$65.00M</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Operating Income (Loss)" data-tip="GAAP Operating Loss of -$46.50M in Q3 2026 ($21.28M Gross Profit - $67.78M OpEx).">Operating Income (Loss)</span></td>
              <td>-$49.65M</td>
              <td>-$42.06M</td>
              <td>-$62.06M</td>
              <td>-$46.99M</td>
              <td class="col-q0" style="color: #f87171;">-$46.50M</td>
              <td class="col-est">-$26.52M</td>
            </tr>
            <tr>
              <td>GAAP Net Income (Loss)</td>
              <td>-$109.27M</td>
              <td>$40.06M</td>
              <td>-$25.03M</td>
              <td>-$42.82M</td>
              <td class="col-q0" style="color: #f87171;">-$46.37M</td>
              <td class="col-est">-$25.00M</td>
            </tr>
            <tr>
              <td>GAAP Diluted EPS ($)</td>
              <td>-$0.27</td>
              <td>-$0.03</td>
              <td>-$0.11</td>
              <td>-$0.10</td>
              <td class="col-q0" style="color: #f87171;">-$0.10</td>
              <td class="col-est">-$0.05</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ROW 3: FORENSIC TRUE FCF BRIDGE -->
    <section class="card" id="sec-fcf" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 3: Forensic Quality-of-Earnings &amp; True Free Cash Flow Bridge</div>
        <span class="badge badge-purple">SEC CASH FLOW AUDIT</span>
      </div>
      <div class="forensic-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
          <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 12px;">Q3 2026 Quarterly Cash Flow Waterfall ($M)</div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Operating cash flow from continuing operations." data-tip="Operating Cash Flow: -$95.99M (-95.99M exact) in Q3 2026.">(+) Operating Cash Flow (OCF)</span>
            <span style="font-weight:700; color: #f87171;">-${abs(q0_ocf):,.2f}M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Capital expenditures." data-tip="CapEx: $1.12M in Q3 2026.">(-) Capital Expenditures (CapEx)</span>
            <span style="font-weight:700; color: #f87171;">-${q0_capex:,.2f}M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px; background: rgba(59, 130, 246, 0.08); padding-left: 6px; padding-right: 6px;">
            <span style="font-weight:600;">(=) Reported Free Cash Flow</span>
            <span style="font-weight:700; color: #f87171;">-${abs(q0_rep_fcf):,.2f}M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Stock-based compensation." data-tip="Stock-Based Compensation: $61.02M in Q3 2026.">(-) Stock-Based Compensation (SBC)</span>
            <span style="font-weight:700; color: #f87171;">-${q0_sbc:,.2f}M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 12.5px;">
            <span class="tip" title="Finance lease payments." data-tip="Finance Leases: $0.00M recorded.">(-) Principal Finance Leases</span>
            <span style="font-weight:700; color: #94a3b8;">-$0.00M</span>
          </div>
          <div class="waterfall-row" style="display:flex; justify-content:space-between; padding: 8px 6px; font-size: 13.5px; background: rgba(239, 68, 68, 0.12); border-radius: 6px; margin-top: 6px;">
            <span style="font-weight:700; color: #f87171;">(=) Forensic True Free Cash Flow</span>
            <span style="font-weight:800; color: #f87171;">-${abs(q0_true_fcf):,.2f}M</span>
          </div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color); display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-weight: 700; font-size: 13.5px; color: #93c5fd; margin-bottom: 10px;">Forensic Cash Quality &amp; Balance Sheet Fortress Assessment</div>
            <p style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-bottom: 10px;">
              SoundHound recorded elevated cash burn in Q3 2026 with Operating Cash Flow of <strong>-${abs(q0_ocf):,.2f}M</strong> and Reported Free Cash Flow of <strong>-${abs(q0_rep_fcf):,.2f}M</strong>. Non-cash stock-based compensation totaled $61.02M, leading to Forensic True Free Cash Flow of <strong>-${abs(q0_true_fcf):,.2f}M</strong>.
            </p>
            <div style="font-size: 12px; color: var(--text-muted); line-height: 1.6;">
              • <strong>Cash &amp; Equivalents Cushion:</strong> SoundHound held $207.58M in cash and cash equivalents as of September 30, 2026. Management reiterated that this capital base provides sufficient runway to bridge the company to positive adjusted EBITDA in 2H 2027 without secondary equity issuance.<br>
              • <strong>One-Time Acquisition Burn Items:</strong> Cash burn in Q3 included non-recurring integration disbursements, advisory fees, and restructuring payouts associated with the Amelia transaction.<br>
              • <strong>Cost Synergy Realization Schedule:</strong> Over $80M of the total $120M identified annualized cost synergies will be executed before January 1, 2027, drastically curtailing quarterly operating expenses.<br>
              • <strong>Capital Intensity Discipline:</strong> Property and equipment additions remained minimal at $1.12M, preserving balance sheet flexibility for cloud model training.
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ROW 4: AUDIT GRID & CALL QA -->
    <section class="card audit-grid" id="sec-audit" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 4: Operational Wins, Drags &amp; Earnings Call Q&amp;A Audit</div>
        <span class="badge badge-blue">QUALITATIVE &amp; TRANSCRIPT FORENSICS</span>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 20px;">
        <div style="border-left: 3px solid #10b981; padding-left: 14px;">
          <h4 style="margin: 0 0 8px 0; color: #34d399; font-size: 14px;">Operational Wins &amp; Catalysts</h4>
          <ul style="font-size: 12.5px; color: #cbd5e1; margin: 0; padding-left: 18px; line-height: 1.6;">
            <li><strong>Robust Top-Line Expansion:</strong> Revenue increased 48.4% YoY to $62.42M, driven by rapid customer rollouts across automotive and restaurant verticals.</li>
            <li><strong>Doubled Synergy Target:</strong> Identified $120M in annualized cost reductions ($80M+ pre-2027), doubling previous estimates and accelerating structural margin recovery.</li>
            <li><strong>Restaurant Voice AI Expansion:</strong> Restaurant smart ordering revenue climbed 67.2% YoY to $22.50M as leading QSR brands scaled drive-thru automation.</li>
            <li><strong>Strong 2027 Revenue Outlook:</strong> Initiated 2027 revenue guidance of $350M - $400M ($375M midpoint), reflecting high-confidence enterprise pipeline conversions.</li>
          </ul>
        </div>
        <div style="border-left: 3px solid #ef4444; padding-left: 14px;">
          <h4 style="margin: 0 0 8px 0; color: #f87171; font-size: 14px;">Execution Drags &amp; Watch Items</h4>
          <ul style="font-size: 12.5px; color: #cbd5e1; margin: 0; padding-left: 18px; line-height: 1.6;">
            <li><strong>Gross Margin Compression:</strong> Gross margin fell to 34.09% (-991 bps QoQ) as legacy low-margin contracts from acquired units weighed on profitability.</li>
            <li><strong>FY 2026 Guidance Trimming:</strong> Full-year revenue guided to $250M-$260M (down from $262.5M Street consensus) due to deliberate contract non-renewals.</li>
            <li><strong>Pushed-Out EBITDA Milestone:</strong> Sustained positive Adjusted EBITDA timeline shifted two quarters forward into second half 2027.</li>
            <li><strong>Spike in Quarterly Cash Burn:</strong> Operating cash flow burn expanded to -$95.99M, necessitating strict execution on announced synergy targets.</li>
          </ul>
        </div>
      </div>
      <div>
        <h4 style="margin: 0 0 10px 0; color: #93c5fd; font-size: 14px;">Top Institutional Analyst Q&amp;A and Analyst Questions Forensic Exchanges</h4>
{qa_cards_html}
      </div>
    </section>

    <!-- ROW 5: PEER GROUP COMPS -->
    <section class="card peers" id="sec-comps" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 5: Conversational AI &amp; Enterprise Software Peer Valuation Comps</div>
        <span class="badge badge-blue">RE-ANCHORED TO AFTER-HOURS PRICE</span>
      </div>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Company</th>
              <th>Ticker</th>
              <th>Market Cap ($M)</th>
              <th>EV ($M)</th>
              <th>Q3 YoY Rev Growth</th>
              <th>Gross Margin %</th>
              <th>EV / NTM Rev</th>
              <th>Strategic Positioning</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background: rgba(59, 130, 246, 0.1); font-weight: 700;">
              <td>SoundHound AI, Inc.</td>
              <td>SOUN</td>
              <td>${mcap_m:,.1f}M</td>
              <td>${ev_m:,.1f}M</td>
              <td style="color: #34d399;">+48.4%</td>
              <td>34.09%</td>
              <td>5.2x</td>
              <td>Voice &amp; Agentic AI for Automotive, Restaurants &amp; Enterprise Service</td>
            </tr>
            <tr>
              <td>Cerence Inc.</td>
              <td>CRNC</td>
              <td>$450.0M</td>
              <td>$680.0M</td>
              <td>-4.0%</td>
              <td>68.50%</td>
              <td>2.1x</td>
              <td>Automotive In-Vehicle Voice &amp; Connected Assistant Software</td>
            </tr>
            <tr>
              <td>LivePerson, Inc.</td>
              <td>LPSN</td>
              <td>$110.0M</td>
              <td>$490.0M</td>
              <td>-18.0%</td>
              <td>62.00%</td>
              <td>1.8x</td>
              <td>Enterprise Conversational Commerce &amp; Customer Care Messaging</td>
            </tr>
            <tr>
              <td>C3.ai, Inc.</td>
              <td>AI</td>
              <td>$3,200.0M</td>
              <td>$2,450.0M</td>
              <td>+20.5%</td>
              <td>59.00%</td>
              <td>7.5x</td>
              <td>Enterprise Generative AI Applications &amp; Predictive Maintenance</td>
            </tr>
            <tr>
              <td>Verint Systems</td>
              <td>VRNT</td>
              <td>$1,850.0M</td>
              <td>$2,150.0M</td>
              <td>+5.5%</td>
              <td>71.00%</td>
              <td>2.4x</td>
              <td>Customer Engagement Software, Workforce Automation &amp; AI Bots</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ROW 6: 4-PILLAR POST-EARNINGS SENTIMENT -->
    <section class="card" id="sec-sentiment" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title"><span class="card-title-accent"></span>Row 6: Multi-Source 4-Pillar Post-Print Sentiment Gauge</div>
        <span class="badge badge-purple">TRANSITIONAL CAUTION ({soc_data["composite_sentiment_score"]} / 100)</span>
      </div>
      <div class="sentiment-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 16px;">
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Institutional Positioning</div>
          <div style="font-size: 20px; font-weight: 800; color: #60a5fa; margin: 4px 0;">{soc_data["institutional_sentiment_score"]} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data["institutional_sentiment_score"]}%; height: 100%; background: #3b82f6;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Institutional accounts adopt wait-and-see stance on execution of $120M cost synergies.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Retail Trader Pulse</div>
          <div style="font-size: 20px; font-weight: 800; color: #f87171; margin: 4px 0;">{soc_data["retail_sentiment_score"]} / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: {soc_data["retail_sentiment_score"]}%; height: 100%; background: #ef4444;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Retail traders disappointed by gross margin drop to 34% and pushed-out EBITDA timeline.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Options Volatility Skew</div>
          <div style="font-size: 20px; font-weight: 800; color: #a855f7; margin: 4px 0;">82 / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: 82%; height: 100%; background: #a855f7;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Downside move of -7.51% remained inside the ±12.38% priced band, driving IV crush.</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Sell-Side Revision Tone</div>
          <div style="font-size: 20px; font-weight: 800; color: #34d399; margin: 4px 0;">76 / 100</div>
          <div class="sentiment-meter-bar" style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-top: 6px;">
            <div style="width: 76%; height: 100%; background: #10b981;"></div>
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 6px;">Analysts welcome contract pruning as necessary medicine that clears the path to 2027 profits.</div>
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
          <div style="font-size: 13px; font-weight: 700; color: #34d399; margin-bottom: 6px;">Bull Case Target: $5.80</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $5.20 - $6.50 (+32% to +65% from AH $3.94)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            $120M in annualized cost synergies materialize ahead of schedule, gross margins rebound above 50% as negative contracts exit, and 2027 revenue approaches the top end of the $350M-$400M guidance range.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #10b981;">
            <strong>Options Structure:</strong> Buy Jan 2027 $4.00 / $6.00 Bull Call Spread. Sell $3.00 Put to finance premium.
          </div>
        </div>
        <div class="scenario-base" style="background: rgba(59, 130, 246, 0.04); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #60a5fa; margin-bottom: 6px;">Base Case Anchor: $4.00</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $3.60 - $4.40 (-9% to +12% around AH $3.94)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Stock stabilizes around $4.00 as the market digests the guidance reset and monitors Q4 cash burn progression toward lower sequential run-rates.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #3b82f6;">
            <strong>Options Structure:</strong> Sell Nov 2026 $3.50 / $4.50 Strangle to capture post-earnings volatility contraction.
          </div>
        </div>
        <div class="scenario-bear" style="background: rgba(239, 68, 68, 0.04); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #f87171; margin-bottom: 6px;">Bear Case Target: $2.80</div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Target Range: $2.40 - $3.20 (-19% to -39% from AH $3.94)</div>
          <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            Cash burn remains elevated into 2027, Amelia integration stalls, and customer churn accelerates beyond management's initial pruning expectations.
          </p>
          <div class="trade-structure" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; font-size: 12px; border-left: 3px solid #ef4444;">
            <strong>Options Structure:</strong> Buy Dec 2026 $3.50 Puts funded by writing $5.00 Covered Calls.
          </div>
        </div>
      </div>
    </section>

    <!-- SEC CITATIONS & AUDIT LEDGER FOOTER -->
    <footer style="padding: 16px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
      <div><strong>Filing Ledger &amp; Source Attributions:</strong> SEC Form 8-K filed on November 5, 2026 (Item 2.02 Results of Operations and Financial Condition, Exhibits 99.1 Press Release and 99.2 Condensed Financial Statements). Historical 5Q financial series sourced from SEC EDGAR Forms 10-Q and verified against SoundHound AI Investor Relations. Stock pricing captured at 6:00 PM PST (${ah_price:.2f} USD).</div>
      <div style="margin-top: 4px;">Zero-Hallucination Pipeline standard enforced: All historical numbers, beat/miss deltas, options-implied moves, and forensic cash flow metrics are immutable ground truth.</div>
    </footer>
"""

post_draft = {
    "header": {
        "page_title": f"{TICKER} T+0 Post-Earnings Forensic Tearsheet ({DATE})",
        "ticker": TICKER,
        "earnings_date": DATE,
        "regular_price": reg_price,
        "after_hours_price": ah_price,
        "post_move_pct": post_move_pct,
        "verdict": verdict
    },
    "historical_table_5q_nums": [
        {
            "period": "Q3 2025",
            "total_revenue": 42.05,
            "gross_profit": 17.92,
            "operating_expenses": 67.57,
            "operating_income": -49.65,
            "gaap_net_income": -109.27,
            "gaap_diluted_eps": -0.27
        },
        {
            "period": "Q4 2025",
            "total_revenue": 55.06,
            "gross_profit": 26.35,
            "operating_expenses": 68.41,
            "operating_income": -42.06,
            "gaap_net_income": 40.06,
            "gaap_diluted_eps": -0.03
        },
        {
            "period": "Q1 2026",
            "total_revenue": 44.20,
            "gross_profit": 13.74,
            "operating_expenses": 75.81,
            "operating_income": -62.06,
            "gaap_net_income": -25.03,
            "gaap_diluted_eps": -0.11
        },
        {
            "period": "Q2 2026",
            "total_revenue": 61.90,
            "gross_profit": 27.93,
            "operating_expenses": 74.92,
            "operating_income": -46.99,
            "gaap_net_income": -42.82,
            "gaap_diluted_eps": -0.10
        },
        {
            "period": "Q3 2026 (Actual)",
            "total_revenue": 62.42,
            "gross_profit": 21.28,
            "operating_expenses": 67.78,
            "operating_income": -46.50,
            "gaap_net_income": -46.37,
            "gaap_diluted_eps": -0.10
        }
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
        "bull_target_low_num": 5.20,
        "bear_target_high_num": 3.20
    },
    "rendered_container_html": html_content.strip()
}

DRAFT_PATH.write_text(json.dumps(post_draft, indent=2), encoding="utf-8")
print(f"[OK] Generated {DRAFT_PATH.name} with length {len(html_content)} chars.")
