import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "LIDR"
DATE = "2026-11-05"

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
            "q_minus_1_actual": 0.20,
            "q_minus_4_yoy": 0.05,
            "street_consensus_q0": 0.57,
            "reported_actual_q0": 0.51,
            "spread_vs_street": "-10.53%",
            "verdict": "MISS",
            "bar_width_pct": 75
        },
        {
            "name": "GAAP Gross Margin (%)",
            "q_minus_1_actual": -80.00,
            "q_minus_4_yoy": -100.00,
            "street_consensus_q0": -50.00,
            "reported_actual_q0": -33.33,
            "spread_vs_street": "+1667 bps",
            "verdict": "REBOUND",
            "bar_width_pct": 85
        },
        {
            "name": "Commercial Revenue Customers",
            "q_minus_1_actual": 25,
            "q_minus_4_yoy": 12,
            "street_consensus_q0": 28,
            "reported_actual_q0": 32,
            "spread_vs_street": "+4 accounts (+14.3%)",
            "verdict": "BEAT",
            "bar_width_pct": 95
        },
        {
            "name": "GAAP Diluted EPS ($)",
            "q_minus_1_actual": -0.22,
            "q_minus_4_yoy": -0.30,
            "street_consensus_q0": -0.17,
            "reported_actual_q0": -0.24,
            "spread_vs_street": "-$0.07",
            "verdict": "MISS",
            "bar_width_pct": 70
        },
        {
            "name": "Cash & Marketable Securities ($M)",
            "q_minus_1_actual": 32.50,
            "q_minus_4_yoy": 28.00,
            "street_consensus_q0": 22.00,
            "reported_actual_q0": 63.10,
            "spread_vs_street": "+$41.10M (ATM Infusion)",
            "verdict": "FORTRESS",
            "bar_width_pct": 98
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Apollo™ Commercial & Sensor Shipments",
                "values": [0.03, 0.06, 0.06, 0.12, 0.32, 0.65],
                "qoq": "+166.7%",
                "yoy": "+966.7%"
            },
            {
                "name": "Strategic Development Programs (Lunar Outpost / STRATOS™)",
                "values": [0.01, 0.03, 0.03, 0.05, 0.14, 0.25],
                "qoq": "+180.0%",
                "yoy": "+1300.0%"
            },
            {
                "name": "Software-Defined Sensing & Sports Analytics",
                "values": [0.01, 0.01, 0.01, 0.03, 0.05, 0.10],
                "qoq": "+66.7%",
                "yoy": "+400.0%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [0.05, 0.10, 0.10, 0.20, 0.51, 1.00],
                "qoq": "+155.0%",
                "yoy": "+920.0%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated GAAP net revenue from AEye's software-defined adaptive lidar sensing platform ($0.51M in Q3 2026, up ~10x YoY from $0.05M in Q3 2025 and 2.5x QoQ from $0.20M in Q2 2026).",
        "Apollo™ Commercial & Sensor Shipments": "Hardware shipments and core modular sensor packages incorporating AEye's software-configurable perception architecture ($0.32M in Q3 2026).",
        "Strategic Development Programs": "Milestone-based engineering, qualification, and hardware development revenue including the multi-million-dollar Lunar Outpost Pegasus rover contract and Swiftstrike AI counter-UAS ($0.14M in Q3 2026).",
        "Software-Defined Sensing & Sports Analytics": "Pure software licensing, perception algorithms, and sports analytics tracking deployments including Alive3D and a second newly signed customer ($0.05M in Q3 2026).",
        "GAAP Gross Profit": "GAAP gross loss of -$0.17M in Q3 2026 (gross margin -33.33%), representing a 4700 bps sequential improvement from -80.0% in Q2 2026 due to BOM cost reductions and richer mix.",
        "GAAP Operating Income": "GAAP operating loss of -$11.29M in Q3 2026 (-$0.17M Gross Profit - $11.12M OpEx), reflecting disciplined R&D execution across Apollo and STRATOS programs.",
        "GAAP Diluted EPS": "GAAP diluted net loss per share of -$0.24 in Q3 2026 based on 46.8M weighted average common shares outstanding.",
        "Operating Cash Burn": "Operating cash flow utilization of -$8.05M in Q3 2026, consistent with quarterly burn rates of -$7.29M in Q2 2026 and -$8.55M in Q1 2026.",
        "Capital Expenditures": "Capital expenditures of $0.01M in Q3 2026, reflecting AEye's capital-light, fabless manufacturing and software-centric delivery model.",
        "Reported Free Cash Flow": "Operating cash flow (-$8.05M) minus CapEx ($0.01M), delivering -$8.06M in Q3 2026.",
        "Stock-Based Compensation": "Equity compensation and share-based awards of $3.25M in Q3 2026, providing key engineering and executive retention.",
        "True Free Cash Flow": "Economic free cash flow deducting CapEx ($0.01M) and non-cash SBC ($3.25M) from OCF (-$8.05M), yielding -$11.31M in Q3 2026.",
        "Lunar Outpost Program": "Binding multi-million-dollar contract with Lunar Outpost to supply Apollo™ lidar for the Pegasus Lunar Terrain Vehicle from qualification through flight hardware delivery.",
        "STRATOS Defense Integration": "AEye's high-performance long-range sensor selected by Swiftstrike AI for integration into counter-unmanned aerial systems (counter-UAS).",
        "Commercial Customer Base": "Total active revenue-generating customer accounts expanded to 32 in Q3 2026, up 28% sequentially from 25 in Q2 2026, with over 200 active technical engagements.",
        "Cash Runway into 2028": "Total cash, cash equivalents, and marketable securities reached $63.1M as of Sept 30, 2026, bolstering liquidity to fund operations into 2028.",
        "FY 2026 Cash Consumption Target": "Management guided full-year 2026 cash consumption of $35.0M (inclusive of ~$5.0M working capital) and targeted a ~15% reduction in 2027 cash burn.",
        "Q4 2026 Guidance Baseline": "Q4 2026 revenue guided to approximately double QoQ to ~$1.00M, marking AEye's first million-dollar quarter and establishing a new quarterly revenue baseline.",
        "After-Hours Reaction": "LIDR shares traded down -2.25% to $0.87 after hours as revenue ($0.51M) slightly missed Street consensus ($0.57M), despite robust guidance and cash balances.",
        "Negative Enterprise Value": "Enterprise Value of -$28.85M with cash and marketable securities ($63.1M) significantly exceeding market capitalization ($41.34M)."
    }
}

# ==============================================================================
# AGENT 2B: TRANSCRIPT & GUIDANCE FORENSIC (Transcript_Forensic_Agent)
# ==============================================================================
agent2b = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "matrix_a_guidance_accountability": [
        {
            "metric": "Q3 2026 Total Revenue ($M)",
            "prior_guidance": "$0.45M - $0.60M",
            "reported_actual": "$0.51M",
            "variance": "-$0.06M vs midpoint",
            "grade": "MET GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Gross Margin (%)",
            "prior_guidance": "-60.0% to -40.0%",
            "reported_actual": "-33.33%",
            "variance": "+1667 bps beat",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Operating Cash Burn ($M)",
            "prior_guidance": "-$7.0M to -$9.0M",
            "reported_actual": "-$8.05M",
            "variance": "Within Range",
            "grade": "MET GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Ending Cash & Investments ($M)",
            "prior_guidance": "$25.0M - $30.0M",
            "reported_actual": "$63.10M",
            "variance": "+$33.10M",
            "grade": "SIGNIFICANT OUTPERFORMANCE",
            "badge_class": "badge-bull"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026 Revenue ($M)",
            "street_pre_print": "$0.80M",
            "new_guidance": "Double QoQ to ~$1.00M (First $1M Quarter)",
            "delta": "+$0.20M (+25.0%)",
            "action": "RAISED / NEW BASELINE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "FY 2026 Cash Consumption ($M)",
            "street_pre_print": "$38.00M",
            "new_guidance": "$35.00M (incl. $5M working capital)",
            "delta": "-$3.00M favorable",
            "action": "REAFFIRMED WITH CAPITAL DISCIPLINE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "FY 2027 Cash Consumption Outlook",
            "street_pre_print": "$32.00M",
            "new_guidance": "~15% reduction vs 2026 (~$29.75M)",
            "delta": "-$2.25M burn reduction",
            "action": "INITIATED POSITIVE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Cash Runway Horizon",
            "street_pre_print": "Late 2026",
            "new_guidance": "Funded into 2028 with $63.1M Cash",
            "delta": "+1.5 Years Extension",
            "action": "EXTENDED THROUGH ATM FACILITY",
            "badge_class": "badge-bull"
        }
    ],
    "credibility_score": 78,
    "top_call_exchanges": [
        {
            "analyst": "Kevin Garrigan (WestPark Capital)",
            "topic": "Q4 2026 $1M Revenue Target & Lunar Outpost Commercial Ramp",
            "question": "Can you discuss what provides the confidence to guide Q4 revenue doubling to ~$1.0 million, and how much of that is driven by recurring hardware shipments versus Lunar Outpost development milestones?",
            "management_answer": "Matt Fisch (CEO): 'Our visibility into Q4 comes from binding purchase orders and committed program schedules. Lunar Outpost is now contributing under our multi-million-dollar contract as Apollo moves from qualification into flight hardware fabrication. Simultaneously, our lead defense customer placed its fifth order, and repeat commercial orders across our 32 active accounts provide the foundation for this $1M quarterly baseline.'",
            "verdict": "CLEAR VISIBILITY TO $1M BASELINE"
        },
        {
            "analyst": "Casey Ryan (WestPark Capital)",
            "topic": "Gross Margin Progression & STRATOS Counter-UAS Unit Economics",
            "question": "Gross margin improved substantially from -80% in Q2 to -33% in Q3. How does the STRATOS revenue mix with Swiftstrike AI impact margin progression into positive territory in 2027?",
            "management_answer": "Conor Tierney (CFO): 'The 47-percentage-point sequential gross margin improvement reflects three factors: lower bill-of-materials costs as Apollo reaches volume, lower warranty accruals, and an initial contribution from STRATOS. Because STRATOS incorporates our software-defined architecture, it commands higher software attachment rates and better ASPs. As commercial volumes ramp through 2027, we expect to cross into positive gross margins.'",
            "verdict": "GROSS MARGIN INFLECTION CONFIRMED"
        },
        {
            "analyst": "Institutional Tech Specialist",
            "topic": "ATM Utilization, Balance Sheet Cash, and Runway into 2028",
            "question": "Ending cash rose to $63.1 million this quarter. Can you detail the capital raised under your ATM facility, your planned cash burn for 2027, and whether additional equity financing is needed?",
            "management_answer": "Conor Tierney (CFO): 'We strategically tapped our ATM facility during periods of liquidity to build a fortress balance sheet with $63.1M in cash and marketable securities and virtually zero debt. With full-year 2026 cash consumption guided at $35M and our commitment to reduce burn by ~15% in 2027, our cash runway now comfortably extends into 2028 without requiring near-term capital raises.'",
            "verdict": "RUNWAY EXTENDED TO 2028"
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL & MARKET PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "retail_sentiment_score": 62,
    "institutional_sentiment_score": 72,
    "composite_sentiment_score": 67,
    "sentiment_breakdown": {
        "retail_pulse": "Cautious but intrigued by sub-$1.00 valuation and $1M Q4 target. Retail discussions on Stocktwits and FinTwit note the top-line miss ($0.51M vs $0.57M), but celebrate the Lunar Outpost contract and 10x YoY revenue surge.",
        "sell_side_reaction": "Constructive on commercial pipeline conversion. WestPark Capital highlights customer expansion to 32 accounts, repeat defense purchasing, and the $63.1M balance sheet as material de-risking achievements.",
        "management_tone": "Resolute, confident, and highly execution-oriented. Matt Fisch and Conor Tierney stressed that software-defined sensing allows AEye to scale across defense, lunar rovers, and sports analytics with minimal incremental CapEx.",
        "options_iv_crush": "Microcap options volume was minimal with negligible open interest. After-hours equity shares slipped -2.25% to $0.87 on modest volume, remaining well within historic trading ranges."
    },
    "after_hours_driver": "AEye shares dipped -2.25% to $0.87 in after-hours trading as Q3 revenue ($0.51M) came in below Street consensus ($0.57M). However, the downside was cushioned by management's strong forward guidance of approximately doubling Q4 revenue to ~$1.00M, gross margin improvement from -80% to -33%, customer accounts growing to 32, and cash surging to $63.1M extending operating runway into 2028."
}

# Write files to post_agent_bus
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print(f"Successfully generated post agent bus files for {TICKER} ({DATE}).")
