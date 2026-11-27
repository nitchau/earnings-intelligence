import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)
TRUTH_PATH = BASE_DIR / "ground_truth" / "MDB_2026-12-01_truth.json"
truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

TICKER = "MDB"
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
            "tooltip_title": "Total consolidated GAAP revenue across MongoDB Atlas, Enterprise Advanced, and Services.",
            "tooltip_def": "Consolidated GAAP Revenue ($M): MongoDB posted $771.77M in Q2 FY27 (+30.5% YoY). Management guided Q3 FY27 revenue to $756M–$761M (~20%–21% YoY); Yahoo consensus sits at $761.75M (+21.24% YoY) while buy-side whispers look for $780M–$790M+.",
            "q_minus_1_actual": "$771.77M",
            "q_minus_4_yoy_baseline": "$628.31M",
            "street_consensus_q0e": f"${cons_rev:,.2f}M",
            "whisper_bogey_q0e": "$780.0M–$792.0M+",
            "whisper_spread_display": "+3.2% vs Consensus",
            "bar_width_pct": 90,
            "hurdle_badge": "Top-Line Hurdle"
        },
        {
            "metric": "Non-GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Non-GAAP diluted earnings per share excluding $148.94M stock-based compensation.",
            "tooltip_def": "Non-GAAP Diluted EPS ($/sh): Consensus is $1.61/sh (top of Q3 guidance $1.57–$1.61 vs $1.90 in Q2 FY27 and $1.32 in Q3 FY26). MongoDB has beaten consensus EPS 4 consecutive quarters (+26.99% avg surprise).",
            "q_minus_1_actual": "$1.90",
            "q_minus_4_yoy_baseline": "$1.32",
            "street_consensus_q0e": f"${cons_eps:.2f}",
            "whisper_bogey_q0e": "$1.78–$1.88",
            "whisper_spread_display": "+10.6% to +16.8% Whisper",
            "bar_width_pct": 89,
            "hurdle_badge": "Bottom-Line Hurdle"
        },
        {
            "metric": "MongoDB Atlas Cloud Revenue ($M & YoY %)",
            "tooltip_title": "Usage-based multi-cloud DBaaS revenue including Atlas Search, Vector Search, and Stream Processing.",
            "tooltip_def": "MongoDB Atlas ($M): Reached $565.92M in Q2 FY27 (+28.9% YoY, 73.3% of revenue), adding a record $127M net-new annualized run rate. Management guided Q3 Atlas growth to ~26% YoY (~$592.7M); bulls demand >= 28% YoY (~$602M+).",
            "q_minus_1_actual": "$565.92M (+28.9% YoY)",
            "q_minus_4_yoy_baseline": "$470.40M (74.9% Mix)",
            "street_consensus_q0e": "~$592.7M (~26% YoY)",
            "whisper_bogey_q0e": "$602M+ (>= 28% YoY)",
            "whisper_spread_display": "+200bps Growth Bogey",
            "bar_width_pct": 93,
            "hurdle_badge": "Primary Valuation Anchor"
        },
        {
            "metric": "Enterprise Advanced (EA) & Search/Vector Adoption",
            "tooltip_title": "Self-managed Enterprise Advanced and other subscription revenue ($181.23M in Q2 FY27).",
            "tooltip_def": "Enterprise Advanced & Other ($M): Surged +35.9% YoY to $181.23M in Q2 FY27 (3-year high) on GA rollout of embedded Search & Vector Search for private/multi-cloud deployments.",
            "q_minus_1_actual": "$181.23M (+35.9% YoY)",
            "q_minus_4_yoy_baseline": "$138.67M",
            "street_consensus_q0e": "$145M–$150M",
            "whisper_bogey_q0e": "$155M–$162M+",
            "whisper_spread_display": "Vector Search Upside",
            "bar_width_pct": 83,
            "hurdle_badge": "Hybrid Cloud Catalyst"
        },
        {
            "metric": "Non-GAAP Operating Margin & Net New Customers",
            "tooltip_title": "Non-GAAP operating margin (24.1% in Q2 FY27) and net customer additions (2,900 added in Q2).",
            "tooltip_def": "Operating Margin & Customer Scale: Q2 Non-GAAP operating income reached $185.9M (24% margin vs 15% YoY) while total customers topped 70,600 (2,999 >=$100K ARR). Q3 guide implies ~20.5% margin ($152M–$156M).",
            "q_minus_1_actual": "24.1% OM / 70,600+ Cust",
            "q_minus_4_yoy_baseline": "19.5% OM / 62,500+ Cust",
            "street_consensus_q0e": "20.5% OM ($154M Mid)",
            "whisper_bogey_q0e": "22.5%+ OM / 2,600+ Adds",
            "whisper_spread_display": "+200bps Margin Cushion",
            "bar_width_pct": 85,
            "hurdle_badge": "Profitability & AI Logos"
        }
    ]
}

bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 82,
    "credibility_label": "82 / 100 (100% 4Q EPS Beat Rate, +26.99% Avg Surprise, Yet Cautious Q3 Atlas Guide & CEO Transition Drove -13.5% Q2 Reaction)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 FY27E Total Revenue vs. Prior Management Guide",
            "tooltip_title": "Comparison of management's Q2 FY27 outlook for Q3 FY27 against Street consensus.",
            "tooltip_def": "Revenue Guidance Calibration: Management guided Q3 FY27 revenue to $756M–$761M (sequentially below Q2's $771.77M due to Q2's multi-year EA upfront license strength). Yahoo consensus sits at $761.75M.",
            "prior_q_guidance_for_q0": "$756.0M – $761.0M (Q2 Call)",
            "current_street_consensus": f"${cons_rev:,.2f}M (Range ${truth['street_consensus_and_targets']['yahoo_revenue_low_q0e']:,.1f}M–${truth['street_consensus_and_targets']['yahoo_revenue_high_q0e']:,.1f}M)",
            "historical_4q_beat_rate": "4 / 4 Top-Line Beats",
            "variance_and_sandbag_commentary": "MongoDB consistently beats conservative quarterly guidance by 2.5%–4.5%, yet two of the last three beats (Q4 FY26 -22.2%, Q2 FY27 -13.5%) sold off on softer sequential/Atlas outlook commentary.",
            "credibility_grade": "Grade A- (Consistent Beat, Tough Bar)"
        },
        {
            "metric": "Atlas Cloud Growth (~26% Guide vs 29% Q2 Actual)",
            "tooltip_title": "Management's Atlas cloud consumption deceleration guide vs historical consumption upside.",
            "tooltip_def": "Atlas Consumption Audit: Atlas delivered ~29% YoY growth for 5 consecutive quarters through Q2 FY27 ($565.92M). Guiding Q3 to ~26% YoY (while raising FY27 Atlas to ~27%) reflects typical usage-model prudence.",
            "prior_q_guidance_for_q0": "~26% YoY Atlas Growth (Q3) / ~27% FY27",
            "current_street_consensus": "~$592.7M Atlas (~26% YoY)",
            "historical_4q_beat_rate": "5 Straight Qtrs ~29% Atlas Growth",
            "variance_and_sandbag_commentary": "Buy-side desks treat 26% as an artificial floor; anything below 27.5% actual Atlas growth in Q3 will be viewed as real consumption deceleration.",
            "credibility_grade": "Grade A (Proven Atlas Conservatism)"
        },
        {
            "metric": "Non-GAAP Operating Margin & GAAP SBC Discipline",
            "tooltip_title": "4Q Non-GAAP EPS surprise rate vs $148.94M GAAP SBC dilution.",
            "tooltip_def": "Profitability & SBC Audit: Trailing 4Q EPS beats averaged +26.99% (+66.24%, +12.08%, +11.54%, +18.09%). Q2 GAAP EBIT turned positive (+$28.40M), though $148.94M SBC pushed True FCF to -$9.53M.",
            "prior_q_guidance_for_q0": "$152M–$156M OpInc / $1.57–$1.61 EPS",
            "current_street_consensus": f"${cons_eps:.2f}/sh (FY27 $6.39–$6.58)",
            "historical_4q_beat_rate": "100% Beat Rate (+26.99% Avg Surp.)",
            "variance_and_sandbag_commentary": "MongoDB achieved GAAP operating profitability (+3.7% GAAP EBIT margin) in Q2 while expanding Non-GAAP operating margin +900 bps YoY to 24.1%.",
            "credibility_grade": "Grade A (Strong Operating Leverage)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 FY27E Revenue & Full-Year FY27 Raise (Above $3.03B)",
            "tooltip_title": "Forward Q4 FY27 revenue guide and FY27 raise needed to reverse Q4's double-digit stock pullback.",
            "tooltip_def": "Forward Revenue Bogey: Current FY27 guidance is $2.99B–$3.03B (+21%–23% YoY). Clearing $3.05B+ FY27 and guiding Q4 Atlas >= 26%–27% YoY is essential to re-rate MDB from 8.23x EV/Sales.",
            "street_consensus_hurdle": "$795M–$805M Q4E / $3.03B FY27",
            "bull_case_bogey": ">= $818M Q4E + FY27 Raised >= $3.06B",
            "bear_case_breakdown": "< $785M Q4E or Atlas FY27 Cut < 27%",
            "sensitivity_badge": "Primary Re-Rating Anchor",
            "strategic_rationale": "With CJ Desai's departure to Meta weighing on sentiment, an explicit FY27 raise above $3.05B proves enterprise Atlas demand is unaffected by executive turnover."
        },
        {
            "forward_metric": "Atlas AI-Native Workload Consumption & EA Vector Search",
            "tooltip_title": "Evidence that AI-native production apps are driving durable Atlas consumption and EA upgrades.",
            "tooltip_def": "AI Database Moat: Investors demand concrete proof that MongoDB's operational JSON + native Vector Search architecture is winning production AI agents rather than losing workloads to Postgres (pgvector) or Snowflake.",
            "street_consensus_hurdle": "Atlas >= 27.5% YoY + EA Search Traction",
            "bull_case_bogey": "Atlas >= 28.5% YoY + Record AI Net Adds",
            "bear_case_breakdown": "Atlas < 26.5% YoY (Signals Consumption Slowdown)",
            "sensitivity_badge": "Multiple Catalyst",
            "strategic_rationale": "Directly refutes the FinTwit bear narrative that AI code-generation tools lower switching costs toward commoditized relational Postgres databases."
        },
        {
            "forward_metric": "CEO Transition Clarity & True FCF Inflection",
            "tooltip_title": "Permanent CEO succession update from Dev Ittycheria and narrowing the $148.94M SBC gap.",
            "tooltip_def": "Governance & Cash Quality: Following CJ Desai's exit to Meta and Q2's -$9.53M True FCF ($139.41M Rep FCF minus $148.94M SBC), investors look for leadership stability and SBC moderating below 18% of sales.",
            "street_consensus_hurdle": "Stable Exec Bench & 22%+ FY27 Non-GAAP OM",
            "bull_case_bogey": "CEO Clarity + SBC < 18% Rev + Positive True FCF",
            "bear_case_breakdown": "Prolonged Leadership Vacuum or Rising SBC",
            "sensitivity_badge": "Governance & Quality",
            "strategic_rationale": "Clearing executive uncertainty while holding $2.41B cash ($28.6M debt) removes the overhang keeping MDB 30% below its $449.13 Street mean target."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "debate_id": "DEBATE_1",
            "title": "Atlas ~28%–29% Durability vs. Postgres/AI Code-Gen Moat Disruption Fears",
            "consensus_view": "Bears point to MongoDB's recent pullback and question whether AI code-generation tools make relational Postgres + pgvector 'good enough' for new applications, while noting Q3 Atlas guidance (~26% YoY) implies deceleration from Q2's 28.9%.",
            "variant_perception": "Bulls emphasize that Atlas sustained ~29% YoY growth for 5 straight quarters, added a record $127M net-new ARR in Q2 and 2,900 net new customers (70,600+ total), while embedded Search & Vector Search propelled Enterprise Advanced +35.9% YoY.",
            "call_focus_question": "Interim CEO Dev Ittycheria: After five consecutive quarters near 29% Atlas growth, what consumption trends did you see in Q3 across AI-native workloads, and how conservative was your 26% Q3 Atlas baseline?"
        },
        {
            "debate_id": "DEBATE_2",
            "title": "CEO Succession Overhang (Post-CJ Desai Exit to Meta) vs. 8.2x EV/Sales Valuation Floor",
            "consensus_view": "Institutional desks remain cautious following former CEO CJ Desai's departure to Meta earlier in 2026, adding execution uncertainty ahead of Q4/FY28 planning and contributing to negative post-earnings stock drift in prior prints.",
            "variant_perception": "Returning chief executive Dev Ittycheria brings deep operational credibility, and sell-side defenders (Rosenblatt, RBC) highlight that 8.23x EV/Sales (less than half Snowflake's 17.44x) with 24% Non-GAAP operating margins prices in an overly punitive transition discount vs the $449.13 Street mean PT (+43.3% upside).",
            "call_focus_question": "Board / Dev Ittycheria: Can you update shareholders on the permanent CEO search timeline and how go-to-market leadership is retaining enterprise field productivity during the transition?"
        },
        {
            "debate_id": "DEBATE_3",
            "title": "GAAP EBIT Inflection (+$28.40M) vs. $148.94M SBC Dilution (-$9.53M True FCF)",
            "consensus_view": "Quality-of-earnings analysts note that despite $139.41M in Q2 Reported FCF (18.1% margin), GAAP Stock-Based Compensation of $148.94M (19.3% of revenue) kept True Forensic FCF negative at -$9.53M.",
            "variant_perception": "MongoDB crossed into positive GAAP Operating Income (+$28.40M) and GAAP Net Income (+$40.94M) in Q2 FY27 while holding $2,411.25M in cash against just $28.59M total debt ($2.38B net cash) and growing Total Deferred Revenue +44.8% YoY to $447.69M.",
            "call_focus_question": "CFO Michael Gordon: With GAAP operating income turning positive at +$28.4M and TTM Reported FCF reaching $660M, when will SBC decelerate below 17% of revenue to turn True Forensic FCF sustainably positive?"
        }
    ]
}

bus_2c = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Whisper_Sentiment_Agent (Agent 2C)",
    "model": "Gemini 3.8 Flash High Standard",
    "verified_products": [
        "MongoDB Atlas Multi-Cloud DBaaS: Fully managed cloud database ($565.92M in Q2, 73.3% of revenue) spanning AWS, Azure, and GCP with native Vector Search and Stream Processing",
        "MongoDB Enterprise Advanced (EA) with Embedded Search & Vector Search: Self-managed and hybrid-cloud enterprise suite surging +35.9% YoY to $181.23M in Q2 FY27",
        "Voyage AI & Native Vector Search Stack: Integrated semantic retrieval, embeddings, and operational data layer powering enterprise RAG and agentic AI applications",
        "MongoDB Relational Migrator & AI Application Modernization: Automated schema conversion accelerating legacy SQL-to-document enterprise migrations"
    ],
    "four_pillar_sentiment": {
        "options_volatility_score": 56,
        "options_volatility_desc": f"56/100 (Dec 4 ATM Straddle implies ±{opt_move_pct:.2f}% / ${opt_move_usd:.2f} vs {avg_1d_move:.2f}% 4Q Avg Realized Move — Fairly Priced Event Vol +{vol_delta:.2f}%, Moderate {put_call_ratio:.2f} P/C OI)",
        "institutional_positioning_score": 78,
        "institutional_positioning_desc": f"78/100 ({analyst_cnt} Analysts with Buy consensus 1.54 & ${mean_pt:.2f} Mean PT implying +{upside_to_pt:.2f}% upside; High PT ${high_pt:.0f}, Low ${low_pt:.0f} at 8.23x EV/Sales)",
        "retail_sentiment_score": 48,
        "retail_sentiment_desc": "48/100 (Tactical bottom-fishing vs lingering PEAD skepticism on Reddit/WSB after prior -13.5% and -22.2% post-earnings drops)",
        "short_interest_score": 34,
        "short_interest_desc": f"34/100 (Moderate {short_float:.2f}% Short Interest of Float — stock reaction driven primarily by institutional long re-accumulation rather than short squeezes)"
    },
    "retail_vs_institutional_audit": {
        "retail_narrative": f"On WallStreetBets and FinTwit, sentiment on MDB at ${spot_price:.2f} is cautious-to-contrarian after double-digit pullbacks following Q4 FY26 (-22.24%) and Q2 FY27 (-13.54%). Retail traders debate whether MDB is a coiled spring on AI-native Atlas growth or a volatility trap under a ±{opt_move_pct:.2f}% (${opt_move_usd:.2f}) straddle.",
        "institutional_narrative": f"Wall Street growth desks ({analyst_cnt} analysts, ${mean_pt:.2f} mean PT) argue MDB's pullback to 8.23x EV/Sales and 39.5x Forward P/E offers compelling value for a 24% operating-margin cloud leader. Still, institutional positioning remains tactical ahead of Dec 1 due to CJ Desai's CEO transition and the need to see Q3 Atlas growth clear 27.5%–28%+ YoY."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print(f"[SUCCESS] Wrote Layer 2 pre_agent_bus files for {TICKER} ({EARNINGS_DATE}).")
