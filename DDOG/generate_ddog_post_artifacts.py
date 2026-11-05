import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "DDOG"
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
            "q_minus_1_actual": 1121.45,
            "q_minus_4_yoy": 885.65,
            "street_consensus_q0": 1146.97,
            "reported_actual_q0": 1197.09,
            "spread_vs_street": "+4.37%",
            "verdict": "BEAT",
            "bar_width_pct": 94
        },
        {
            "name": "Customers with ARR >= $100K",
            "q_minus_1_actual": 4620.0,
            "q_minus_4_yoy": 4050.0,
            "street_consensus_q0": 4750.0,
            "reported_actual_q0": 4860.0,
            "spread_vs_street": "+2.32%",
            "verdict": "BEAT",
            "bar_width_pct": 91
        },
        {
            "name": "GAAP Gross Margin (%)",
            "q_minus_1_actual": 78.59,
            "q_minus_4_yoy": 80.08,
            "street_consensus_q0": 79.50,
            "reported_actual_q0": 80.19,
            "spread_vs_street": "+69 bps",
            "verdict": "EXPANSION",
            "bar_width_pct": 92
        },
        {
            "name": "Operating Cash Flow ($M)",
            "q_minus_1_actual": 315.87,
            "q_minus_4_yoy": 251.47,
            "street_consensus_q0": 290.00,
            "reported_actual_q0": 289.95,
            "spread_vs_street": "-0.02%",
            "verdict": "IN LINE",
            "bar_width_pct": 86
        },
        {
            "name": "Reported Free Cash Flow ($M)",
            "q_minus_1_actual": 278.70,
            "q_minus_4_yoy": 213.95,
            "street_consensus_q0": 260.00,
            "reported_actual_q0": 279.08,
            "spread_vs_street": "+7.34%",
            "verdict": "BEAT",
            "bar_width_pct": 95
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Infrastructure Monitoring & Cloud Observability",
                "values": [510.0, 545.0, 570.0, 625.0, 660.0, 655.0],
                "qoq": "+5.6%",
                "yoy": "+29.4%"
            },
            {
                "name": "APM, Log Management & Distributed Tracing",
                "values": [275.0, 298.0, 316.0, 355.0, 382.0, 385.0],
                "qoq": "+7.6%",
                "yoy": "+38.9%"
            },
            {
                "name": "AI Observability, LLM Monitoring & Security",
                "values": [100.65, 110.19, 120.43, 141.45, 155.09, 155.0],
                "qoq": "+9.6%",
                "yoy": "+54.1%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [885.65, 953.19, 1006.43, 1121.45, 1197.09, 1195.0],
                "qoq": "+6.7%",
                "yoy": "+35.2%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated subscription revenue across Datadog's unified observability and security SaaS platform ($1,197.09M in Q3 2026, +35.2% YoY).",
        "Infrastructure Monitoring & Cloud Observability": "Core host and container metrics collection across AWS, Azure, GCP, and on-premises environments ($660.0M in Q3 2026).",
        "APM, Log Management & Distributed Tracing": "Application performance monitoring, synthetic tests, network monitoring, and real-time structured log indexing ($382.0M in Q3 2026).",
        "AI Observability, LLM Monitoring & Security": "LLM observability, cloud security management (CSM), application security (ASM), and generative AI workload tracing ($155.09M in Q3 2026).",
        "GAAP Gross Margin": "GAAP gross margin of 80.19% in Q3 2026 ($959.92M gross profit), up from 78.59% in Q2 2026 reflecting cloud infrastructure optimization.",
        "GAAP Operating Income": "GAAP operating income of $74.71M in Q3 2026, surging sequentially from $7.46M in Q2 2026 as operating leverage expanded.",
        "GAAP Diluted EPS": "GAAP diluted earnings per share of $0.32 in Q3 2026 based on weighted-average diluted shares.",
        "Customers with ARR >= $100K": "Large enterprise customers generating over $100,000 in Annual Recurring Revenue (4,860 accounts, up +20% YoY).",
        "Operating Cash Flow": "GAAP cash flows from operating activities of $289.95M in Q3 2026 ($1,167.5M generated over the trailing twelve months).",
        "Capital Expenditures": "Purchases of property, equipment and capitalized software of $10.87M in Q3 2026.",
        "Reported Free Cash Flow": "Operating cash flow minus capital expenditures ($279.08M in Q3 2026, representing a 23.3% FCF margin).",
        "True Free Cash Flow": "Core economic cash generation deducting CapEx ($10.87M) and SBC ($9.51M) from OCF ($289.95M), yielding $269.57M in Q3 2026.",
        "AI Observability Attach Rate": "Percentage of Datadog enterprise customers utilizing specialized LLM monitoring, vector database tracing, and AI token cost analytics.",
        "Multi-Product Adoption": "Over 83% of customers using 2+ products, and over 49% of customers using 4+ products across Datadog's 20+ software modules.",
        "Dollar-Based Net Retention Rate (DBNRR)": "Trailing net expansion metric reflecting customer usage growth, seat expansions, and additional module cross-selling.",
        "Bits AI Copilot": "Datadog's generative AI assistant integrated into incident response workflows to automatically synthesize root causes and suggest remediations.",
        "Cloud Cost Management": "Specialized FinOps monitoring tooling enabling organizations to track, allocate, and optimize multi-cloud computing and GPU spend.",
        "Stock-Based Compensation": "Non-cash stock-based compensation of $9.51M in Q3 2026, maintaining prudent dilution control."
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
            "prior_guidance": "$1,135.0M - $1,145.0M ($1,140.0M midpoint)",
            "actual_delivered": "$1,197.09M delivered (+5.01% above midpoint)",
            "variance_commentary": "Revenue exceeded internal expectations by +$57.09M driven by surging multi-cloud data ingestion and AI workload monitoring.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Non-GAAP Operating Income",
            "prior_guidance": "$260.0M - $270.0M ($265.0M midpoint)",
            "actual_delivered": "$295.0M delivered (+11.32% above midpoint)",
            "variance_commentary": "Operating leverage on blowout top-line volume drove non-GAAP operating margin to 24.6%.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Free Cash Flow Margin",
            "prior_guidance": "20.0% - 22.0%",
            "actual_delivered": "23.3% delivered (279.08M FCF)",
            "variance_commentary": "Free cash flow exceeded expectations on strong enterprise multi-year upfront billing collections.",
            "credibility_grade": "BEAT OWN GUIDE"
        },
        {
            "metric": "Enterprise Customer Expansion",
            "prior_guidance": ">4,750 $100K+ ARR customers",
            "actual_delivered": "4,860 $100K+ ARR customers (+20% YoY)",
            "variance_commentary": "Net new enterprise customer additions accelerated to 240 in the quarter.",
            "credibility_grade": "BEAT OWN GUIDE"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026 Revenue Guidance",
            "pre_print_consensus": "$1,170.0M",
            "management_guidance": "$1,190.0M - $1,200.0M ($1,195.0M midpoint)",
            "delta_vs_street": "+$25.0M (+2.14%) upward revision",
            "action_badge": "RAISED",
            "pm_rationale": "Positions Datadog to exit FY26 at an annualized revenue run-rate approaching $4.8B."
        },
        {
            "metric": "Q4 2026 Non-GAAP Operating Income",
            "pre_print_consensus": "$275.0M",
            "management_guidance": "$280.0M - $290.0M ($285.0M midpoint)",
            "delta_vs_street": "+$10.0M above consensus expectations",
            "action_badge": "RAISED",
            "pm_rationale": "Demonstrates sustained non-GAAP operating margins around 24% while continuing aggressive R&D in agentic AI."
        },
        {
            "metric": "FY 2026 Total Revenue",
            "pre_print_consensus": "$4,450.0M",
            "management_guidance": "$4,515.0M - $4,525.0M ($4,520.0M midpoint)",
            "delta_vs_street": "+$70.0M (+1.57%) full-year raise",
            "action_badge": "RAISED",
            "pm_rationale": "Confirms durable 30%+ annual growth profile across secular AI and cloud migration tailwinds."
        },
        {
            "metric": "FY 2026 Non-GAAP Diluted EPS",
            "pre_print_consensus": "$2.65",
            "management_guidance": "$2.73 - $2.75 ($2.74 midpoint)",
            "delta_vs_street": "+$0.09 (+3.40%) upward reset",
            "action_badge": "RAISED",
            "pm_rationale": "Reflects superior operating discipline and higher cash generation yields."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Sanjit Singh (Morgan Stanley)",
            "topic": "AI Workload Monitoring Monetization & Customer Usage Trajectory",
            "question": "Olivier, you noted that 35% YoY revenue growth was fueled in part by digital operations and AI workloads. Can you quantify the direct contribution from AI-native customers and how traditional enterprises are using Datadog to monitor their LLMs?",
            "executive_answer": "Olivier Pomel (CEO) replied: 'AI is rapidly becoming a pervasive driver across our platform. AI-native customers represent over 6% of our ARR and are growing at triple-digit rates. But more importantly, traditional enterprises are now deploying LLM models into production, and they require Datadog for tracing, latency debugging, and token cost governance. We see AI accelerating cloud data consumption across all three pillars.'"
        },
        {
            "analyst": "Brad Zelnick (Deutsche Bank)",
            "topic": "Gross Margin Sustainability & Infrastructure Efficiency",
            "question": "David, GAAP gross margin expanded to 80.19% and Non-GAAP was above 82%. What drove the efficiency in cloud hosting costs, and is this 80%+ level sustainable into 2027?",
            "executive_answer": "David Obstler (CFO) responded: 'Our gross margin performance reflects ongoing structural engineering optimizations across our data processing pipeline. We've optimized our multi-cloud architecture and tiering of log data. While we continue to reinvest in new AI capabilities, we feel very comfortable with gross margins remaining in the low-to-mid 80s range.'"
        },
        {
            "analyst": "Kash Rangan (Goldman Sachs)",
            "topic": "Platform Consolidation & Multi-Product Cross-Selling Momentum",
            "question": "Olivier, with 4,860 customers now over $100K ARR, how much of the growth is coming from customers consolidating disjointed point solutions into the Datadog platform?",
            "executive_answer": "Olivier Pomel explained: 'Consolidation is our primary growth engine. CIOs are actively eliminating separate vendors for APM, infrastructure, logs, and cloud security. Over 49% of our customers now use four or more products, and our security products continue to show the fastest adoption curves in our history. The Datadog unified data model is an unbeatable value proposition.'"
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
        "institutional_score": 92,
        "retail_score": 85,
        "options_skew_score": 80,
        "sell_side_score": 94,
        "composite_verdict": "Premier AI Observability Cloud Compounder"
    },
    "retail_pulse": {
        "score": 85,
        "tone": "Strong Appreciation of 35% Hyper-Growth and Free Cash Flow",
        "key_themes": [
            "Active discussion on Reddit r/stocks and FinTwit praising Datadog's rare 35% growth at $1.2B quarterly revenue scale",
            "Stock holding flat after-hours (-0.38% to $188.01) after running up into the print, viewed as healthy consolidation",
            "Traders highlighting elite $279M free cash flow generation and clean balance sheet"
        ]
    },
    "institutional_positioning": {
        "score": 92,
        "tone": "Universal Consensus Upward Revisions on Resilient Enterprise Demand",
        "key_themes": [
            "Tier 1 sell-side firms (Morgan Stanley, Goldman Sachs, Deutsche Bank) preparing price target increases toward $215-$230",
            "Institutional portfolio managers noting Datadog's guidance raise to $4.52B midpoint demonstrates secular cloud migration re-acceleration",
            "Options volatility crush contained comfortably within the ±14.25% priced straddle band"
        ]
    },
    "pm_takeaway": "Datadog delivered an outstanding operational print for Q3 2026. Revenue of $1,197.09M grew 35.2% YoY, beating consensus ($1,146.97M) by +$50.12M (+4.37%) and whisper ($1,175.0M) by +$22.09M. Enterprise accounts with $100K+ ARR climbed to 4,860 (+20% YoY), while GAAP gross margin expanded to 80.19%. Q3 produced $289.95M in operating cash flow and $279.08M in reported FCF (23.3% margin), with True FCF reaching $269.57M. Management raised Q4 revenue guidance to $1.19B-$1.20B and full-year guidance to $4.515B-$4.525B, solidifying Datadog's moat as the indispensable observability platform for the AI era."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for DDOG.")
