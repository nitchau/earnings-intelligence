import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)
TRUTH_PATH = BASE_DIR / "ground_truth" / "GTLB_2026-12-01_truth.json"
truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

TICKER = "GTLB"
EARNINGS_DATE = "2026-12-01"

spot_price = float(truth["price_validation"]["yahoo_spot_price"])
short_float = float(truth["valuation_and_market"]["short_percent_of_float"])
opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"])
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"])
put_call_ratio = float(truth["options_positioning"]["put_call_oi_ratio"])
avg_1d_move = float(truth["historical_earnings_track_record"]["avg_historical_1d_move_abs_pct"])
vol_delta = float(truth["historical_earnings_track_record"]["implied_vs_historical_move_delta_pct"])
mean_pt = float(truth["street_consensus_and_targets"]["target_mean_price"])
high_pt = float(truth["street_consensus_and_targets"]["target_high_price"])
low_pt = float(truth["street_consensus_and_targets"]["target_low_price"])
upside_to_pt = float(truth["street_consensus_and_targets"]["implied_upside_to_mean_pct"])
analyst_cnt = int(truth["street_consensus_and_targets"]["analyst_count"])
cons_rev = float(truth["schedule_verification"]["yahoo_consensus_revenue"])
cons_eps = float(truth["schedule_verification"]["yahoo_consensus_eps"])

bus_2a = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_KPI_Consensus_Agent (Agent 2A)",
    "model": "Gemini 3.8 Flash High Standard",
    "upcoming_quarter_label": "Q3 FY27E (Ended Oct 31, 2026)",
    "latest_reported_quarter_label": "Q2 FY27 (Ended Jul 31, 2026)",
    "headline_and_company_kpis": [
        {
            "metric": "Consolidated GAAP Revenue ($M)",
            "tooltip_title": "Total consolidated GAAP revenue across Subscription (Self-Managed + SaaS) and License & Other.",
            "tooltip_def": "Consolidated GAAP Revenue ($M): GitLab delivered $286.25M in Q2 FY27 (+21.3% YoY). Management guided Q3 FY27 revenue to $281M–$283M (~15%–16% YoY), while Street Yahoo 0q consensus sits at $282.81M and buy-side whispers look for $290M–$295M+.",
            "q_minus_1_actual": "$286.25M",
            "q_minus_4_yoy_baseline": "$244.35M",
            "street_consensus_q0e": f"${cons_rev:,.2f}M",
            "whisper_bogey_q0e": "$290.0M–$295.0M+",
            "whisper_spread_display": "+3.4% vs Consensus",
            "bar_width_pct": 89,
            "hurdle_badge": "Top-Line Hurdle"
        },
        {
            "metric": "Non-GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Non-GAAP diluted earnings per share excluding $75.01M stock-based compensation.",
            "tooltip_def": "Non-GAAP Diluted EPS ($/sh): Consensus is $0.20/sh (matching Q3 guidance high end of $0.19–$0.20 vs $0.24 in Q2 FY27 and $0.25 in Q3 FY26). GitLab has beaten consensus EPS 4 straight quarters by an average of +24.98%.",
            "q_minus_1_actual": "$0.24",
            "q_minus_4_yoy_baseline": "$0.25",
            "street_consensus_q0e": f"${cons_eps:.2f}",
            "whisper_bogey_q0e": "$0.25–$0.27",
            "whisper_spread_display": "+25% to +35% Whisper",
            "bar_width_pct": 91,
            "hurdle_badge": "Bottom-Line Hurdle"
        },
        {
            "metric": "Paid Consumption Run Rate (Duo AI & Flex)",
            "tooltip_title": "Annualized Paid Consumption Run Rate (CRR) across GitLab Duo Agent Platform and hybrid Flex usage.",
            "tooltip_def": "Paid CRR ($M): Surged >$40M exiting Q2 FY27 (up sharply from $15M in Q1 FY27), propelled by ~50% QoQ Duo Agent Platform expansion and 130+ Flex customers committing >$20M in six weeks.",
            "q_minus_1_actual": ">$40.0M CRR",
            "q_minus_4_yoy_baseline": "Early Duo GA",
            "street_consensus_q0e": ">$52M–$55M Q3E",
            "whisper_bogey_q0e": ">$60M+ CRR & Flex Uptake",
            "whisper_spread_display": "Act 2 AI Monetization",
            "bar_width_pct": 87,
            "hurdle_badge": "Primary AI Catalyst"
        },
        {
            "metric": "Dollar-Based Net Retention Rate (DBNRR) & Ultimate Mix",
            "tooltip_title": "Trailing 12-month net expansion rate across existing cohorts and Ultimate tier share of ARR.",
            "tooltip_def": "DBNRR & Ultimate Tier: DBNRR accelerated sequentially to 117% in Q2 FY27 while Ultimate grew ~35% YoY to reach 59% of total ARR. Sustaining DBNRR >= 117% proves seat expansion + AI upsells offset macro headwinds.",
            "q_minus_1_actual": "117% / 59% Ultimate",
            "q_minus_4_yoy_baseline": "120%+ / 50%+ Ultimate",
            "street_consensus_q0e": "116%–117% DBNRR",
            "whisper_bogey_q0e": ">= 118% DBNRR / 60%+ Ult.",
            "whisper_spread_display": "+100bps Expansion",
            "bar_width_pct": 82,
            "hurdle_badge": "Net Expansion Check"
        },
        {
            "metric": "SaaS Revenue Mix & Net ARR Growth (%)",
            "tooltip_title": "Cloud-hosted GitLab SaaS share of total revenue and Net New ARR growth rate.",
            "tooltip_def": "SaaS & Net ARR: SaaS climbed +36% YoY to reach 34% of total revenue in Q2 FY27 while Net ARR grew >40% YoY (~42%). Investors track SaaS durability alongside Flex accounting timing ($13M potential FY27 rev-rec shift).",
            "q_minus_1_actual": "34% SaaS (+36% YoY)",
            "q_minus_4_yoy_baseline": "~30% SaaS",
            "street_consensus_q0e": "35% SaaS / +20% Tot Rev",
            "whisper_bogey_q0e": "36%+ SaaS / >35% NNARR",
            "whisper_spread_display": "Cloud Mix Shift",
            "bar_width_pct": 85,
            "hurdle_badge": "Cloud Transition"
        }
    ]
}

bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 86,
    "credibility_label": "86 / 100 (100% 4Q EPS Beat Rate, +24.98% Avg Surprise, Consistent Beat-and-Raise Execution on Non-GAAP Operating Margin)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 FY27E Total Revenue vs. Prior Management Guide",
            "tooltip_title": "Comparison of management's Q2 FY27 outlook for Q3 FY27 against Street consensus.",
            "tooltip_def": "Revenue Guidance Calibration: Management guided Q3 FY27 revenue to $281M–$283M (down sequentially from $286.25M due to Flex revenue-recognition timing conservatism). Yahoo consensus sits at $282.81M.",
            "prior_q_guidance_for_q0": "$281.0M – $283.0M (Q2 Call)",
            "current_street_consensus": f"${cons_rev:,.2f}M (Range ${truth['street_consensus_and_targets']['yahoo_revenue_low_q0e']:,.1f}M–${truth['street_consensus_and_targets']['yahoo_revenue_high_q0e']:,.1f}M)",
            "historical_4q_beat_rate": "4 / 4 Top-Line Beats (~3–5% Avg)",
            "variance_and_sandbag_commentary": "GitLab beat Q2 consensus by ~5 percentage points ($286.25M) and explicitly carved out up to $13M of Flex rev-rec timing from FY27 guidance, creating classic beat-and-raise cushion.",
            "credibility_grade": "Grade A (Systematic Sandbagger)"
        },
        {
            "metric": "Non-GAAP Operating Income & EPS Leverage",
            "tooltip_title": "4Q Non-GAAP EPS and operating income beat consistency.",
            "tooltip_def": "Operating Leverage: Q2 Non-GAAP operating income hit $42.6M (~14.9% margin) and EPS hit $0.24 (+33.6% beat). Management guided Q3 Non-GAAP OpInc to $35M–$37M and EPS to $0.19–$0.20.",
            "prior_q_guidance_for_q0": "$35M–$37M OpInc / $0.19–$0.20 EPS",
            "current_street_consensus": f"${cons_eps:.2f}/sh (Whisper $0.25+)",
            "historical_4q_beat_rate": "100% Beat Rate (+24.98% Avg Surp.)",
            "variance_and_sandbag_commentary": "Trailing 4Q EPS beats of +24.02%, +29.98%, +12.32%, and +33.60% confirm management builds 200–300 bps of OpEx buffer into quarterly margin guides.",
            "credibility_grade": "Grade A+ (Best-in-Class EPS Cushion)"
        },
        {
            "metric": "Cash Flow Timing vs. GAAP SBC Intensity",
            "tooltip_title": "Quarterly OCF seasonality and GAAP Stock-Based Compensation ($75.01M in Q2 FY27).",
            "tooltip_def": "FCF & SBC Audit: Q2 FY27 OCF dipped to -$3.09M (after +$149.20M in Q1) alongside a jump in SBC to $75.01M (26.2% of revenue), dragging Q2 True FCF to -$78.31M even as TTM Reported FCF stands at +$210M.",
            "prior_q_guidance_for_q0": "FY27 OCF / FCF Conversion Focus",
            "current_street_consensus": "Rebound to Positive Q3 OCF",
            "historical_4q_beat_rate": "Positive TTM FCF ($210M)",
            "variance_and_sandbag_commentary": "While Q1/Q4 carry seasonal collections strength, Q2's +50% QoQ SBC jump ($75.01M vs $50.06M) widened GAAP EBIT loss to -$56.94M and demands management clarification.",
            "credibility_grade": "Grade B (Monitor SBC & Q2 OCF Dip)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 FY27E Revenue & Full-Year FY27 Raise (Above $1.133B)",
            "tooltip_title": "Forward Q4 FY27 revenue guide and FY27 full-year raise needed to sustain GTLB's recovery rally.",
            "tooltip_def": "Forward Revenue Bogey: Current FY27 revenue guidance is $1.129B–$1.133B (+18%–19% YoY). Investors expect Q4 FY27 guidance >= $300M and a full-year raise toward $1.15B+.",
            "street_consensus_hurdle": "$298M–$302M Q4E / $1.135B FY27",
            "bull_case_bogey": ">= $308M Q4E + FY27 Raised >= $1.155B",
            "bear_case_breakdown": "< $292M Q4E or Flex Rev-Rec Deferral > $15M",
            "sensitivity_badge": "Primary Re-Rating Anchor",
            "strategic_rationale": "At 5.98x EV/Sales (half Datadog's 12.44x), proving ~20% durable growth without Flex accounting drag unlocks multiple expansion back toward $56+."
        },
        {
            "forward_metric": "GitLab Duo Agent Platform CRR & Flex Hybrid Commitments",
            "tooltip_title": "Scaling Paid Consumption Run Rate beyond $40M and expanding Flex customer commitments beyond 130 accounts.",
            "tooltip_def": "AI & Flex Monetization: Investors want concrete evidence that Duo Agent Platform and GitLab Orbit drive net-new budget expansion rather than cannibalizing fixed DevSecOps seats.",
            "street_consensus_hurdle": "Paid CRR > $52M / 200+ Flex Customers",
            "bull_case_bogey": "Paid CRR > $65M + 250+ Flex Logos",
            "bear_case_breakdown": "Seat Compression Outpaces Flex Consumption",
            "sensitivity_badge": "AI Thesis Validation",
            "strategic_rationale": "Directly counters the Street's existential bear thesis that AI coding agents (GitHub Copilot, Cursor, Claude Code) reduce total developer seat counts."
        },
        {
            "forward_metric": "Non-GAAP Operating Margin (>15%) & Q3 OCF Rebound",
            "tooltip_title": "Rebounding Operating Cash Flow from Q2's -$3.09M and containing SBC below 23% of revenue.",
            "tooltip_def": "Margin & Cash Quality: With $1,256.99M cash and zero debt, GitLab must rebound from Q2's -$3.09M OCF and $75.01M SBC spike to validate 20%+ FCF margin durability.",
            "street_consensus_hurdle": "Q3 Non-GAAP OpInc > $42M / Positive OCF",
            "bull_case_bogey": "Q4 OpMargin >= 17% + OCF > $45M",
            "bear_case_breakdown": "SBC > $75M Again or Second Negative OCF Qtr",
            "sensitivity_badge": "Quality of Earnings",
            "strategic_rationale": "With 8.64% short interest, disciplined SBC and strong Q3 collections remove the primary bear argument around GAAP operating losses (-$56.94M in Q2)."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "debate_id": "DEBATE_1",
            "title": "Seat Compression vs. GitLab Flex & Duo Agent Platform Monetization",
            "consensus_view": "Bears argue AI coding assistants reduce enterprise developer headcount growth, capping seat-based DevSecOps expansion and forcing GitLab to transition to hybrid Flex pricing that could shift up to $13M of FY27 revenue out of near-term recognition.",
            "variant_perception": "Bulls counter that Paid CRR more than doubled sequentially from $15M to >$40M in Q2, Flex captured 130+ customers (> $20M commitments) in just 6 weeks, and Net ARR surged >40% YoY with DBNRR accelerating to 117%.",
            "call_focus_question": "CEO Bill Staples: With Paid CRR crossing $40M and 130+ enterprises adopting GitLab Flex in six weeks, are Flex conversions expanding net ACV upon renewal, and how much of the potential $13M rev-rec shift materialized in Q3?"
        },
        {
            "debate_id": "DEBATE_2",
            "title": "Microsoft GitHub Competition vs. Enterprise Ultimate Tier Consolidation (59% ARR)",
            "consensus_view": "Skeptics cite bundled Microsoft GitHub Enterprise + Copilot pricing as an ongoing hurdle for mid-market net-new logo wins and pricing power.",
            "variant_perception": "GitLab's unified single-application DevSecOps + security compliance platform (Ultimate tier growing ~35% YoY to 59% of ARR) plus cloud-agnostic AWS Bedrock & Google Vertex AI integrations win regulated enterprises avoiding single-vendor lock-in.",
            "call_focus_question": "Management: What drove Ultimate's acceleration to 59% of ARR, and how are competitive win rates holding up against GitHub in regulated financial and public-sector deals?"
        },
        {
            "debate_id": "DEBATE_3",
            "title": "Q2 OCF Dip (-$3.09M) & +50% QoQ SBC Jump ($75.01M) vs. Zero-Debt Balance Sheet",
            "consensus_view": "Forensic bears highlight that Q2 GAAP Operating Cash Flow turned negative (-$3.09M vs +$49.37M YoY) while SBC surged from $50.06M to $75.01M (26.2% of sales), pushing Q2 GAAP EBIT loss to -$56.94M and True FCF to -$78.31M.",
            "variant_perception": "Long-only investors note Q2 reflects normal post-Q1 working capital timing (Q1 OCF was +$149.20M; TTM FCF remains +$210M) alongside $1,256.99M in cash/ST investments, zero debt, and $574.67M in total deferred revenue (+18.4% YoY).",
            "call_focus_question": "CFO Brian Robins: What specific payroll/bonus or equity vesting timing drove Q2's jump in SBC to $75.01M and negative -$3.09M OCF, and what is your Q3/Q4 free cash flow conversion outlook?"
        }
    ]
}

bus_2c = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Whisper_Sentiment_Agent (Agent 2C)",
    "model": "Gemini 3.8 Flash High Standard",
    "verified_products": [
        "GitLab DevSecOps Platform & Ultimate Tier: Unified single-application SDLC, CI/CD, and application security platform accounting for 59% of total ARR",
        "GitLab Flex Hybrid Model: Hybrid seat- and consumption-based licensing unlocking elastic AI agent usage ($20M+ from 130+ customers in first 6 weeks)",
        "GitLab Duo Agent Platform & GitLab Orbit: Agentic AI software development and developer knowledge workflows (> $40M Paid CRR exiting Q2, +50% QoQ)",
        "AWS Bedrock & Google Cloud Vertex AI Ecosystem Integrations: Cloud-agnostic enterprise AI orchestration across SaaS (34% of revenue) and Self-Managed deployments"
    ],
    "four_pillar_sentiment": {
        "options_volatility_score": 55,
        "options_volatility_desc": f"55/100 (Dec 4 ATM Straddle implies ±{opt_move_pct:.2f}% / ${opt_move_usd:.2f} vs {avg_1d_move:.2f}% 4Q Avg Realized Move — Overpriced Event Vol by +{vol_delta:.2f}%, Strong Call Skew {put_call_ratio:.2f} P/C OI)",
        "institutional_positioning_score": 74,
        "institutional_positioning_desc": f"74/100 ({analyst_cnt} Analysts with Buy consensus & ${mean_pt:.2f} Mean PT implying +{upside_to_pt:.2f}% upside; High PT ${high_pt:.0f}, Low ${low_pt:.0f} at 5.98x EV/Sales)",
        "retail_sentiment_score": 56,
        "retail_sentiment_desc": "56/100 (Neutral-to-moderately bullish Reddit/FinTwit sentiment (~53-56/100) focused on AI Act 2 monetization and 117% DBNRR recovery)",
        "short_interest_score": 68,
        "short_interest_desc": f"68/100 (Elevated {short_float:.2f}% Short Interest of Float — meaningful short-squeeze fuel if Q3 Duo CRR & Q4 guidance top whisper hurdles)"
    },
    "retail_vs_institutional_audit": {
        "retail_narrative": f"Across Reddit (r/stocks, r/investing) and FinTwit, GTLB at ${spot_price:.2f} has modest but constructive event-driven interest (~53-56 sentiment). Retail bulls point to the 0.05 Put/Call OI call skew and Q2's +9.98% breakout as signs of an Act 2 AI turnaround, while options traders hesitate to buy naked calls into a ±{opt_move_pct:.2f}% (${opt_move_usd:.2f}) straddle.",
        "institutional_narrative": f"Software specialists note GitLab trades at just 5.98x EV/Sales (less than half Datadog's 12.44x and one-third JFrog's 19.15x) with 85.9% gross margins and $1.26B net cash. Institutional focus centers squarely on Q4 FY27 guidance, Flex rev-rec timing, and whether Duo Agent Platform CRR accelerates past $55M+, with {short_float:.2f}% short interest creating asymmetric upside squeeze risk."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print(f"[SUCCESS] Wrote Layer 2 pre_agent_bus files for {TICKER} ({EARNINGS_DATE}).")
