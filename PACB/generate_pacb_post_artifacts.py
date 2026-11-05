import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "PACB"
DATE = "2026-11-04"

BUS_DIR = BASE_DIR / "post_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

# ==============================================================================
# AGENT 2A: OPERATIONAL KPIS & SEGMENTS (KPI_Discovery_Agent)
# ==============================================================================
agent2a = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "operational_kpis": [
        {
            "name": "Total GAAP Revenue ($M)",
            "q_minus_1_actual": 39.01,
            "q_minus_4_yoy": 38.44,
            "street_consensus_q0": 39.46,
            "reported_actual_q0": 40.56,
            "spread_vs_street": "+2.79%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "Consumables Revenue ($M)",
            "q_minus_1_actual": 17.55,
            "q_minus_4_yoy": 16.84,
            "street_consensus_q0": 18.20,
            "reported_actual_q0": 20.80,
            "spread_vs_street": "+14.29%",
            "verdict": "BLOWOUT BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Instrument Revenue ($M)",
            "q_minus_1_actual": 14.90,
            "q_minus_4_yoy": 15.76,
            "street_consensus_q0": 14.50,
            "reported_actual_q0": 13.20,
            "spread_vs_street": "-8.97%",
            "verdict": "SLIGHT MISS",
            "bar_width_pct": 78
        },
        {
            "name": "Non-GAAP Diluted EPS ($)",
            "q_minus_1_actual": -0.14,
            "q_minus_4_yoy": -0.12,
            "street_consensus_q0": -0.13,
            "reported_actual_q0": -0.11,
            "spread_vs_street": "+15.38%",
            "verdict": "BEAT",
            "bar_width_pct": 94
        },
        {
            "name": "Operating Cash Burn ($M)",
            "q_minus_1_actual": -35.58,
            "q_minus_4_yoy": -18.71,
            "street_consensus_q0": -32.00,
            "reported_actual_q0": -34.87,
            "spread_vs_street": "-8.97%",
            "verdict": "RUNWAY DISCIPLINE",
            "bar_width_pct": 82
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Consumables Revenue (SMRT Cells & Reagents)",
                "values": [16.84, 18.50, 16.90, 17.55, 20.80, 21.50],
                "qoq": "+18.5%",
                "yoy": "+23.5%"
            },
            {
                "name": "Instrument Revenue (Revio & Vega Placements)",
                "values": [15.76, 19.80, 14.10, 14.90, 13.20, 14.50],
                "qoq": "-11.4%",
                "yoy": "-16.2%"
            },
            {
                "name": "Service & Other Revenue",
                "values": [5.84, 6.35, 6.18, 6.56, 6.56, 6.80],
                "qoq": "+0.0%",
                "yoy": "+12.3%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [38.44, 44.65, 37.18, 39.01, 40.56, 42.80],
                "qoq": "+4.0%",
                "yoy": "+5.5%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated GAAP net revenue from long-read sequencing instruments, proprietary consumables, and service contracts ($40.56M in Q3 2026, up +5.5% YoY).",
        "Consumables Revenue": "Recurring SMRT Cells and sequencing reagent packs used on installed Revio and Vega sequencers ($20.80M in Q3 2026, surging +23.5% YoY).",
        "Instrument Revenue": "Capital equipment sales of Revio high-throughput long-read sequencers and benchtop Vega systems ($13.20M in Q3 2026).",
        "Service & Other Revenue": "Extended maintenance contracts, field support, and bioinformatics software subscriptions ($6.56M in Q3 2026, +12.3% YoY).",
        "Revio System Placements": "Shipments of PacBio's flagship high-throughput HiFi long-read sequencing platform (15 Revio units placed in Q3 2026).",
        "Vega Benchtop Sequencer": "PacBio's newly launched benchtop long-read sequencer democratizing HiFi sequencing for regional laboratories (35 Vega units placed in Q3 2026).",
        "Annualized Revio Pull-Through": "Annualized consumable pull-through per installed Revio sequencer (~$204,000 per system in Q3 2026).",
        "GAAP Gross Margin": "GAAP gross margin of 33.21% ($13.47M gross profit) and Non-GAAP gross margin of 36.11% ($14.65M gross profit) in Q3 2026.",
        "Non-GAAP Diluted EPS": "Adjusted diluted loss per share excluding restructuring and intangible amortization (-$0.11 in Q3 2026 vs -$0.13 consensus).",
        "GAAP Diluted EPS": "GAAP diluted net loss per share of -$0.12 in Q3 2026 based on 315M weighted-average common shares.",
        "Operating Cash Burn": "Cash used in operating activities of -$34.87M in Q3 2026, reflecting continued operational restructuring and cost discipline.",
        "Reported Free Cash Flow": "Operating cash flow minus capital expenditures (-$37.47M in Q3 2026, after $2.60M CapEx).",
        "True Free Cash Flow": "Economic cash generation deducting CapEx ($2.60M) and SBC ($8.00M) from OCF (-$34.87M), yielding -$45.47M in Q3 2026.",
        "Ending Cash & Investments": "Total cash, cash equivalents, and liquid short-term investments of $199.4M as of September 30, 2026.",
        "Cash Flow Breakeven by 2028": "Management's reiterated strategic financial commitment to reach operating cash flow breakeven by 2028 through restructuring savings.",
        "CFO Transition": "Transition of CFO Jim Gibson into an advisory role effective November 3, 2026, while the company initiates an executive search.",
        "Stock-Based Compensation": "Non-cash equity incentives of $8.00M in Q3 2026, down from $9.26M in Q2 2026 and $10.98M in Q3 2025.",
        "HiFi Sequencing Technology": "PacBio's circular consensus sequencing technology delivering >99.9% read accuracy with long-read structural variant detection."
    }
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")

# ==============================================================================
# AGENT 2B: TRANSCRIPT FORENSICS & GUIDANCE (Transcript_Forensic_Agent)
# ==============================================================================
agent2b = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "matrix_a_execution_accountability": [
        {
            "metric": "Q3 2026 Total Revenue",
            "prior_guidance": "$38.0M - $41.0M ($39.5M midpoint)",
            "actual_delivered": "$40.56M delivered (+2.68% above midpoint)",
            "variance_commentary": "Revenue exceeded guided midpoint as strong consumables pull-through ($20.80M) offset modest instrument delays.",
            "credibility_grade": "BEAT OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Non-GAAP Gross Margin",
            "prior_guidance": "34.0% - 37.0%",
            "actual_delivered": "36.11% delivered (+61 bps above midpoint)",
            "variance_commentary": "Gross margin expanded sequentially driven by higher consumable manufacturing efficiency and SPRQ-Nx chemistry attach.",
            "credibility_grade": "MET GUIDE"
        },
        {
            "metric": "Q3 2026 Operating Expense Reductions",
            "prior_guidance": "GAAP OpEx below $52.0M",
            "actual_delivered": "$50.47M delivered (Non-GAAP OpEx $46.95M)",
            "variance_commentary": "Exceeded cost reduction targets as headcount restructuring and rationalization of short-read assets generated structural savings.",
            "credibility_grade": "BEAT OWN GUIDE"
        },
        {
            "metric": "Consumables Pull-Through Velocity",
            "prior_guidance": "High-teens YoY revenue expansion",
            "actual_delivered": "+23.5% YoY ($20.80M delivered)",
            "variance_commentary": "Revio fleet utilization accelerated with customer sample sequencing runs climbing across population genomics projects.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "FY 2026 Total Revenue",
            "pre_print_consensus": "$156.5M",
            "management_guidance": "Narrowed to $155.0M - $160.0M ($157.5M midpoint)",
            "delta_vs_street": "+$1.0M (+0.64%) upward refinement at midpoint",
            "action_badge": "MAINTAINED & NARROWED",
            "pm_rationale": "Signals revenue stabilization with accelerating high-margin consumable recurring revenue counterbalancing capital equipment budget scrutiny."
        },
        {
            "metric": "Q4 2026 Revenue Guidance",
            "pre_print_consensus": "$41.5M",
            "management_guidance": "$41.0M - $44.0M ($42.5M midpoint)",
            "delta_vs_street": "+$1.0M (+2.41%) beat at midpoint",
            "action_badge": "RAISED",
            "pm_rationale": "Implies strongest sequential quarter of the year driven by year-end budget flushes and Vega customer deliveries."
        },
        {
            "metric": "Cash Flow Breakeven Runway",
            "pre_print_consensus": "High skepticism regarding cash runway beyond 2026",
            "management_guidance": "Reiterated positive operating cash flow by 2028 with $199.4M cash buffer",
            "delta_vs_street": "Runway extended via disciplined burn reduction",
            "action_badge": "REITERATED",
            "pm_rationale": "Reduces fears of imminent highly dilutive secondary equity offerings as quarterly burn stabilizes near -$30M."
        },
        {
            "metric": "Vega Benchtop Commercial Rollout",
            "pre_print_consensus": "20 units in Q4 2026",
            "management_guidance": "35 units already placed in Q3, scaling in Q4",
            "delta_vs_street": "+75% shipment upside",
            "action_badge": "EXCEEDED",
            "pm_rationale": "Broadens addressable customer base to smaller academic and core laboratories that could not afford a $750K Revio system."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Dan Arias (Stifel)",
            "topic": "Consumables Surging to $20.8M & Revio Installed Base Utilization",
            "question": "Christian, consumables came in very strong at $20.8M, up 23.5% YoY. Are you seeing an inflection in utilization across your population genomics customers, and how should we project Revio pull-through heading into 2027?",
            "executive_answer": "Christian Henry (CEO) answered: 'Our consumable revenue of $20.8M was driven by record HiFi sequencing volume. As customers scaled their projects with our new SPRQ chemistry and larger genome initiatives like Verily and TychoBio gained momentum, sample throughput reached all-time highs. We expect consumable pull-through to remain durable as customers transition from validation to full production.'"
        },
        {
            "analyst": "Subbu Nambi (Guggenheim)",
            "topic": "Cash Burn Trajectory & Path to 2028 Breakeven",
            "question": "With cash and investments at $199.4M and quarterly operating burn at $34.9M, can you walk us through the cadence of expense reductions that get PacBio to cash flow breakeven without external financing?",
            "executive_answer": "Christian Henry responded: 'We have executed structural restructuring that eliminated over $75M in annualized operating costs, reflected in our OpEx coming down to $50.5M this quarter. As Vega shipments scale and gross margins expand toward 40% with higher consumable attach, our quarterly cash burn will decline sequentially toward -$20M in 2027 and reach breakeven by 2028. We are fully focused on managing our $199.4M liquidity fortress.'"
        },
        {
            "analyst": "Kyle Mikson (Canaccord Genuity)",
            "topic": "CFO Transition & Executive Stability",
            "question": "Christian, regarding the announcement that Jim Gibson is stepping down as CFO to take an advisory role, can you give context on the transition timing and what qualifications you are prioritizing in the next finance chief?",
            "executive_answer": "Christian Henry stated: 'Jim has been a terrific partner through our restructuring and asset rationalization. With our major cost-cutting programs implemented and the company on a stabilized operational footing, Jim and the board felt this was the natural time to transition. Jim will remain actively advising through March 2027, ensuring a seamless handover while we conduct a comprehensive search for our next commercial-phase CFO.'"
        }
    ]
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")

# ==============================================================================
# AGENT 2C: SENTIMENT & SOCIAL PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "four_pillar_sentiment": {
        "institutional_score": 75,
        "retail_score": 78,
        "options_skew_score": 72,
        "sell_side_score": 76,
        "composite_verdict": "Stabilized Operational Turnaround & Long-Read Consumables Surge"
    },
    "retail_pulse": {
        "score": 78,
        "tone": "Relief on Revenue Beat and Strong Vega Placements",
        "key_themes": [
            "Retail genomic sequencing investors on Reddit and FinTwit celebrating top-line beat ($40.56M vs $39.46M consensus)",
            "Stock holding steady after-hours (-0.39% to $2.54) following sharp intraday positioning",
            "Enthusiasm around 35 Vega benchtop placements expanding market access beyond institutional core labs"
        ]
    },
    "institutional_positioning": {
        "score": 75,
        "tone": "Constructive on Restructuring Progress, Monitoring CFO Search",
        "key_themes": [
            "Sell-side analysts (Stifel, Canaccord, Guggenheim) pointing to +23.5% YoY consumable surge as evidence of authentic end-market demand",
            "Full-year revenue guidance narrowed to $155M-$160M ($157.5M midpoint), providing needed clarity",
            "Options volatility crush contained well inside the ±26.77% expected straddle move"
        ]
    },
    "pm_takeaway": "Pacific Biosciences reported a stabilizing Q3 2026 print. Total revenue of $40.56M beat consensus ($39.46M) by +$1.10M (+2.79%), underpinned by an exceptional blowout in high-margin Consumables revenue ($20.80M, +23.5% YoY). Non-GAAP diluted EPS of -$0.11 beat Street consensus (-$0.13) by $0.02 (+15.38%), benefiting from aggressive OpEx reductions ($50.47M GAAP OpEx vs $54.78M in Q3 2025). Operating cash burn of -$34.87M was maintained with $199.4M in total cash and investments. Management narrowed full-year revenue guidance to $155M-$160M ($157.5M midpoint) and reiterated its target to achieve operating cash flow breakeven by 2028."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for PACB.")
