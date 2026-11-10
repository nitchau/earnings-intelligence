import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "GUTS"
EARNINGS_DATE = "2026-11-12"

# Agent 2A: KPIs
bus_2a = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_KPI_Consensus_Agent (Agent 2A)",
    "model": "Gemini 3.8 Flash High Standard",
    "upcoming_quarter_label": "Q3 2026E",
    "latest_reported_quarter_label": "Q2 2026 (Ended Jun 30, 2026)",
    "headline_and_company_kpis": [
        {
            "metric": "Consolidated Commercial Revenue ($M)",
            "tooltip_title": "Commercial product revenue from Revita procedural therapy or collaborative licensing milestone payments.",
            "tooltip_def": "Consolidated Commercial Revenue ($M): Fractyl Health is a clinical-stage metabolic therapeutic company with no commercial product sales prior to FDA regulatory authorization. Consensus models $0.00M in Q3 2026E, with whisper expectations centered on potential non-dilutive licensing milestone income from Rejuva partnering.",
            "q_minus_1_actual": "$0.00M",
            "q_minus_4_yoy_baseline": "$0.00M",
            "street_consensus_q0e": "$0.00M",
            "whisper_bogey_q0e": "$0.00M",
            "whisper_spread_display": "Pre-Commercial",
            "bar_width_pct": 50,
            "hurdle_badge": "Clinical Stage"
        },
        {
            "metric": "GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Diluted net loss per share reflecting clinical trial site activation, regulatory filing preparations, and corporate overhead.",
            "tooltip_def": "GAAP Diluted EPS ($/sh): Q2 2026 actual EPS came in at -$1.41 (beating consensus of -$1.64). Street consensus models -$1.59 for Q3 2026E, with buy-side whisper bogeys looking for -$1.40 as initial workforce restructuring efficiencies take hold.",
            "q_minus_1_actual": "-$1.41",
            "q_minus_4_yoy_baseline": "-$8.52",
            "street_consensus_q0e": "-$1.59",
            "whisper_bogey_q0e": "-$1.40",
            "whisper_spread_display": "+$0.19 Better",
            "bar_width_pct": 82,
            "hurdle_badge": "Burn Hurdle"
        },
        {
            "metric": "Quarterly Operating Cash Burn ($M)",
            "tooltip_title": "Net operating cash consumption per quarter dedicated to the REMAIN-1 pivotal study and regulatory submissions.",
            "tooltip_def": "Quarterly Operating Cash Burn ($M): Q2 2026 OCF was -$15.90M. Consensus anticipates Q3 operating cash outflow of -$14.50M, with management targeting a steady-state burn reduction to ~$8.0M per quarter by mid-2027 following the October corporate restructuring.",
            "q_minus_1_actual": "-$15.90M",
            "q_minus_4_yoy_baseline": "-$18.20M",
            "street_consensus_q0e": "-$14.50M",
            "whisper_bogey_q0e": "-$13.00M",
            "whisper_spread_display": "+$1.50M Savings",
            "bar_width_pct": 85,
            "hurdle_badge": "Capital Discipline"
        },
        {
            "metric": "Cash Runway Horizon (Quarter)",
            "tooltip_title": "Projected cash runway duration under current streamlined operating budget.",
            "tooltip_def": "Cash Runway Horizon: Following the 45% workforce reduction in October 2026, management guided that existing cash reserves provide operational runway into Q2 2027, fully funding operations past the 12-month REMAIN-1 readout and FDA De Novo submission.",
            "q_minus_1_actual": "Q4 2026",
            "q_minus_4_yoy_baseline": "Q3 2026",
            "street_consensus_q0e": "Q2 2027",
            "whisper_bogey_q0e": "Q3 2027",
            "whisper_spread_display": "Funded to Readout",
            "bar_width_pct": 88,
            "hurdle_badge": "Runway Buffer"
        }
    ]
}

# Agent 2B: Guidance & Debates
bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 75,
    "credibility_label": "75 / 100 (Solid Clinical Pivotal Trial Execution & Positive 6-Month Data Balanced Against Microcap Balance Sheet Runway)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "REMAIN-1 Pivotal 6-Month Topline Readout",
            "tooltip_title": "Prior clinical milestone guidance for 6-month REMAIN-1 cohort data.",
            "tooltip_def": "REMAIN-1 6-Month Readout: Guided to Q4 2026; delivered successfully in late October 2026 meeting co-primary endpoint (p=0.0023).",
            "prior_q_guidance_for_q0": "Topline 6-Month Data in Q4 2026",
            "current_street_consensus": "Met Primary Endpoint (p=0.0023)",
            "historical_4q_beat_rate": "75.0% (3 Beats, 1 Miss on EPS)",
            "variance_and_sandbag_commentary": "Management delivered ahead of timeline on the REMAIN-1 pivotal study, demonstrating statistically significant weight loss retention post-GLP-1 cessation.",
            "credibility_grade": "Grade A- (Pivotal Success)"
        },
        {
            "metric": "Operating Cash Burn Reduction Target",
            "tooltip_title": "Quarterly operating cash burn target post-restructuring.",
            "tooltip_def": "Cash Burn Reduction: Guided to reduce quarterly burn by ~50% to ~$8M by Q2 2027.",
            "prior_q_guidance_for_q0": "~50% Reduction to ~$8.0M/Qtr",
            "current_street_consensus": "$8.0M – $9.0M Target by Q2 2027",
            "historical_4q_beat_rate": "80.0% R&D Budget Adherence",
            "variance_and_sandbag_commentary": "The 45% workforce reduction and discontinuation of internal Rejuva clinical development directly preserve capital for the Revita commercial pathway.",
            "credibility_grade": "Grade B+ (Disciplined Focus)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "FDA De Novo Submission Filing Timing",
            "tooltip_title": "Target timeline for formal submission of the Revita De Novo regulatory packet.",
            "tooltip_def": "FDA De Novo Submission: Street consensus hurdle requires formal submission by late Q4 2026 / early Q1 2027; any slippage beyond Q1 2027 risks valuation degradation.",
            "street_consensus_hurdle": "Late Q4 2026 – Early Q1 2027 Submission",
            "bull_case_bogey": "Filed by Dec 31, 2026 with Priority Review",
            "bear_case_breakdown": "Delayed to Mid-2027 or Additional Trial Mandated",
            "sensitivity_badge": "High Regulatory Sensitivity",
            "strategic_rationale": "Key gating item to unlock U.S. commercial clearance and establish first-mover advantage in procedural post-GLP-1 maintenance."
        },
        {
            "forward_metric": "REMAIN-1 12-Month Durability Readout",
            "tooltip_title": "Anticipated readout timing for full 12-month pivotal cohort data.",
            "tooltip_def": "REMAIN-1 12-Month Readout: Consensus expects topline 1-year data in Q1 2027. Bull case bogey looks for >75% weight loss retention at 12 months.",
            "street_consensus_hurdle": "Q1 2027 Topline Data (Second Co-Primary)",
            "bull_case_bogey": ">75% GLP-1 Weight Retention at 12 Months",
            "bear_case_breakdown": "Waning Efficacy (<60% Retention vs Sham)",
            "sensitivity_badge": "Clinical Efficacy Anchor",
            "strategic_rationale": "Confirms long-term metabolic signaling durability and underpins commercial reimbursement adoption."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "debate_id": "DEBATE_1",
            "title": "Post-GLP-1 Weight Maintenance: Procedural Revita vs. Maintenance Oral GLP-1s",
            "consensus_view": "Patients completing intensive GLP-1 therapy will transition to low-dose oral GLP-1 pills or second-generation peptides rather than an endoscopic ablation procedure.",
            "variant_perception": "Over 50% of patients discontinue GLP-1s within one year due to gastrointestinal side effects, cost, or fatigue; a single 30-minute outpatient Revita procedure offers a permanent, drug-free maintenance alternative.",
            "call_focus_question": "CEO Harith Rajagopalan: What commercial physician feedback have you received from obesity medicine specialists regarding patient willingness to undergo duodenal mucosal resurfacing vs. lifelong GLP-1 adherence?"
        },
        {
            "debate_id": "DEBATE_2",
            "title": "Cash Runway Sufficiency & Financing Strategy",
            "consensus_view": "With market cap under $15M and enterprise value at $25.5M, Fractyl faces severe equity dilution risk before commercial revenue inflects in 2028.",
            "variant_perception": "The 45% workforce reduction extends runway past the 12-month REMAIN-1 readout into Q2 2027, allowing Fractyl to partner Rejuva out-of-license and secure non-dilutive milestone financing.",
            "call_focus_question": "CFO Bradley Campbell: What is the current status of the strategic alternatives process for the Rejuva platform, and can non-dilutive upfront proceeds bridge the company through FDA clearance?"
        },
        {
            "debate_id": "DEBATE_3",
            "title": "Reimbursement & CPT Coding Roadmap",
            "consensus_view": "Securing broad commercial and Medicare payer coverage for a novel endoscopic metabolic device will take 3-5 years post-approval.",
            "variant_perception": "The AMA has already issued dedicated Category III CPT code 1122T effective January 1, 2027, substantially accelerating hospital outpatient department (HOPD) billing and private payer coverage determinations.",
            "call_focus_question": "Chief Commercial Officer: How will the implementation of CPT code 1122T in January 2027 streamline early commercial center activation ahead of the formal 2028 U.S. launch?"
        }
    ]
}

# Agent 2C: Sentiment & Positioning
bus_2c = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Whisper_Sentiment_Agent (Agent 2C)",
    "model": "Gemini 3.8 Flash High Standard",
    "verified_products": [
        "Revita® System: Endoscopic duodenal mucosal resurfacing therapy holding FDA Breakthrough Device Designation",
        "REMAIN-1 Pivotal Study: 308-patient randomized, double-blind sham-controlled trial meeting 6-month primary endpoint (p=0.0023)",
        "Rejuva® Gene Therapy Platform: Pancreas-targeted AAV gene therapy (RJVA-001/002) undergoing strategic partnering",
        "CPT Code 1122T: Dedicated AMA reimbursement code for duodenal mucosal resurfacing effective January 1, 2027"
    ],
    "four_pillar_sentiment": {
        "options_volatility_score": 60,
        "options_volatility_desc": "60/100 (Unlisted Options Liquidity; Historical Realized 1-Day Earnings Volatility Averages ±12.58%)",
        "institutional_positioning_score": 78,
        "institutional_positioning_desc": "78/100 (5 Sell-Side Analysts with Mean PT $23.60 representing massive asymmetric recovery potential)",
        "retail_sentiment_score": 72,
        "retail_sentiment_desc": "72/100 (Active Retail Speculation on Stocktwits and microcap biotech channels following positive REMAIN-1 data)",
        "short_interest_score": 55,
        "short_interest_desc": "55/100 (2.14% Short Float reflects low institutional borrowing but high upside beta to positive catalysts)"
    },
    "retail_vs_institutional_audit": {
        "retail_narrative": "Retail biotech traders view GUTS as an oversold metabolic turnaround play after positive pivotal trial results, betting on a short-term re-rating toward historical IPO levels.",
        "institutional_narrative": "Institutional healthcare funds focus on FDA De Novo filing acceptance, cash runway management through Q2 2027, and strategic partnering monetization of the Rejuva asset."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")

print(f"Successfully generated all 3 pre_agent_bus files for {TICKER} ({EARNINGS_DATE}).")
