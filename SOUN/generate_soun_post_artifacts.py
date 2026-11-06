import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "SOUN"
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
            "q_minus_1_actual": 61.90,
            "q_minus_4_yoy": 42.05,
            "street_consensus_q0": 62.18,
            "reported_actual_q0": 62.42,
            "spread_vs_street": "+0.39%",
            "verdict": "SLIGHT BEAT",
            "bar_width_pct": 88
        },
        {
            "name": "GAAP Gross Margin (%)",
            "q_minus_1_actual": 45.12,
            "q_minus_4_yoy": 42.62,
            "street_consensus_q0": 44.00,
            "reported_actual_q0": 34.09,
            "spread_vs_street": "-991 bps",
            "verdict": "COMPRESSION",
            "bar_width_pct": 72
        },
        {
            "name": "GAAP Diluted EPS ($)",
            "q_minus_1_actual": -0.10,
            "q_minus_4_yoy": -0.27,
            "street_consensus_q0": -0.05,
            "reported_actual_q0": -0.10,
            "spread_vs_street": "-$0.05",
            "verdict": "IN LINE",
            "bar_width_pct": 80
        },
        {
            "name": "Operating Cash Burn ($M)",
            "q_minus_1_actual": -33.71,
            "q_minus_4_yoy": -32.65,
            "street_consensus_q0": -30.00,
            "reported_actual_q0": -95.99,
            "spread_vs_street": "-$65.99M",
            "verdict": "HIGH BURN",
            "bar_width_pct": 68
        },
        {
            "name": "Annualized Synergy Actions ($M)",
            "q_minus_1_actual": 0.0,
            "q_minus_4_yoy": 0.0,
            "street_consensus_q0": 50.0,
            "reported_actual_q0": 120.0,
            "spread_vs_street": "+$70.0M",
            "verdict": "BEAT",
            "bar_width_pct": 98
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Automotive & Connected IoT Voice AI",
                "values": [23.13, 29.18, 22.10, 27.85, 27.50, 35.00],
                "qoq": "-1.3%",
                "yoy": "+18.9%"
            },
            {
                "name": "Restaurant Smart Ordering & Drive-Thru AI",
                "values": [13.46, 17.62, 14.59, 21.67, 22.50, 30.00],
                "qoq": "+3.8%",
                "yoy": "+67.2%"
            },
            {
                "name": "Enterprise Conversational AI & Amelia Unit",
                "values": [3.36, 5.51, 5.30, 9.28, 9.82, 17.00],
                "qoq": "+5.8%",
                "yoy": "+192.3%"
            },
            {
                "name": "Consumer Apps & Other Emerging",
                "values": [2.10, 2.75, 2.21, 3.10, 2.60, 4.48],
                "qoq": "-16.1%",
                "yoy": "+23.8%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [42.05, 55.06, 44.20, 61.90, 62.42, 86.48],
                "qoq": "+0.8%",
                "yoy": "+48.4%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated GAAP net revenue from SoundHound's conversational and agentic voice AI platform ($62.42M in Q3 2026, up +48.4% YoY from $42.05M in Q3 2025 and +0.8% QoQ from $61.90M in Q2 2026).",
        "Automotive & Connected IoT Voice AI": "Embedded in-vehicle and smart device voice interfaces powered by Houndify and OASYS ($27.50M in Q3 2026, deployed across Stellantis, Hyundai, and Kia).",
        "Restaurant Smart Ordering & Drive-Thru AI": "Automated voice ordering and phone answering for global QSR chains including White Castle, Jersey Mike's, and Chipotle ($22.50M in Q3 2026).",
        "Enterprise Conversational AI & Amelia Unit": "Customer service agents, IT helpdesk automation, and healthcare patient triaging inherited from Amelia acquisition ($9.82M in Q3 2026).",
        "Consumer Apps & Other Emerging": "Legacy consumer mobile applications, music identification, and specialized developer licensing ($2.60M in Q3 2026).",
        "GAAP Gross Profit": "GAAP gross profit of $21.28M in Q3 2026 (34.09% gross margin), down from 45.12% in Q2 2026 due to negative gross margin contracts from legacy acquisitions.",
        "GAAP Operating Income": "GAAP operating loss of -$46.50M in Q3 2026 ($21.28M Gross Profit - $67.78M OpEx), reflecting R&D investments and integration restructuring.",
        "GAAP Diluted EPS": "GAAP diluted net loss per share of -$0.10 in Q3 2026 based on 460M weighted average common shares outstanding.",
        "Operating Cash Burn": "Operating cash flow burn of -$95.99M in Q3 2026, elevated by acquisition payments, Amelia severance, and working capital realignments.",
        "Capital Expenditures": "Capital expenditures of $1.12M in Q3 2026, reflecting the lightweight cloud-native nature of voice model training.",
        "Reported Free Cash Flow": "Operating cash flow (-$95.99M) minus CapEx ($1.12M), delivering -$97.11M in Q3 2026.",
        "Stock-Based Compensation": "Equity awards and stock incentives of $61.02M in Q3 2026, driven by acquisition retention grants and new engineering hires.",
        "True Free Cash Flow": "Economic cash generation deducting CapEx ($1.12M) and non-cash SBC ($61.02M) from OCF (-$95.99M), yielding -$158.13M in Q3 2026.",
        "Contract Pruning Strategy": "Management's deliberate decision to non-renew negative margin legacy contracts, temporarily muting revenue growth to accelerate EBITDA profitability in 2027.",
        "Synergy Cost Reductions": "Identified $120M in annualized run-rate cost synergies ($80M effective before Jan 1, 2027), targeting sustained positive adjusted EBITDA in 2H 2027.",
        "FY 2026 Guidance": "Full-year 2026 revenue guided to $250M - $260M ($255.0M midpoint), with 2027 revenue projected between $350M - $400M.",
        "Available Liquidity": "Cash and cash equivalents of $207.6M as of September 30, 2026, providing sufficient runway through 2027 profitability crossover.",
        "After-Hours Reaction": "SoundHound AI shares dipped -7.51% to $3.94 after hours as the market digested contract non-renewals and near-term margin compression."
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
            "prior_guidance": "$61.0M - $63.0M",
            "reported_actual": "$62.42M",
            "variance": "+$0.42M (+0.7%)",
            "grade": "MET GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Gross Margin (%)",
            "prior_guidance": "42.0% - 45.0%",
            "reported_actual": "34.09%",
            "variance": "-891 bps",
            "grade": "MISSED OWN GUIDE",
            "badge_class": "badge-bear"
        },
        {
            "metric": "Q3 2026 GAAP Operating Loss ($M)",
            "prior_guidance": "-$42.0M to -$48.0M",
            "reported_actual": "-$46.50M",
            "variance": "Within Range",
            "grade": "MET GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Cash & Equivalents ($M)",
            "prior_guidance": "$200.0M - $220.0M",
            "reported_actual": "$207.58M",
            "variance": "+$7.58M",
            "grade": "MET GUIDE",
            "badge_class": "badge-bull"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "FY 2026 Revenue ($M)",
            "street_pre_print": "$262.50M",
            "new_guidance": "$250.0M - $260.0M ($255.0M)",
            "delta": "-$7.5M (-2.9%)",
            "action": "LOWERED (CONTRACT PRUNING)",
            "badge_class": "badge-bear"
        },
        {
            "metric": "FY 2027 Revenue Outlook ($M)",
            "street_pre_print": "$365.00M",
            "new_guidance": "$350.0M - $400.0M ($375.0M)",
            "delta": "+$10.0M (+2.7%)",
            "action": "INITIATED POSITIVE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "EBITDA Profitability Timeline",
            "street_pre_print": "Q4 2026",
            "new_guidance": "Sustained Positive within 2H 2027",
            "delta": "Pushed 2 Quarters",
            "action": "RESET",
            "badge_class": "badge-warn"
        },
        {
            "metric": "Annualized Cost Synergies ($M)",
            "street_pre_print": "$60.00M",
            "new_guidance": "$120.00M ($80M pre-Jan 2027)",
            "delta": "+$60.0M (+100%)",
            "action": "DOUBLED",
            "badge_class": "badge-bull"
        }
    ],
    "credibility_score": 85,
    "top_call_exchanges": [
        {
            "analyst": "Dan Ives (Wedbush)",
            "topic": "Contract Pruning Strategy & Gross Margin Trough",
            "question": "Can you walk through the decision to exit certain negative gross margin contracts? Is 34% the trough for gross margin, and how quickly does it rebound toward 50%?",
            "management_answer": "Keyvan Mohajer (CEO): 'When we acquired Amelia and earlier assets, some legacy customer commitments carried negative economics. We made the disciplined decision not to renew those contracts. That creates a minor short-term revenue drag, but it immediately clears our path to sustained gross margins above 50% and positive EBITDA by second half 2027.'",
            "verdict": "DISCIPLINED OPERATIONAL RESET"
        },
        {
            "analyst": "Glenn Mattson (Ladenburg Thalmann)",
            "topic": "Cash Runway & Operating Burn Spikes",
            "question": "Operating cash burn rose to -$96M this quarter, leaving $207.6M in cash. Do you have sufficient liquidity to reach your 2H 2027 profitability milestone without dilutive capital raises?",
            "management_answer": "Nitesh Sharan (CFO): 'Yes, absolutely. The Q3 cash burn included one-time transaction fees, severance costs, and working capital timing from our acquisitions. With $80M in synergy actions hitting before year-end, our quarterly cash burn will drop precipitously in Q4 and through 2027. We do not need outside financing.'",
            "verdict": "LIQUIDITY RUNWAY CONFIRMED"
        },
        {
            "analyst": "Scott Buck (H.C. Wainwright)",
            "topic": "OASYS Agentic AI Platform & Enterprise Demand",
            "question": "How are customers responding to OASYS, and does the shift to a hosted recurring model change your sales cycle length?",
            "management_answer": "Keyvan Mohajer: 'OASYS shifts us from episodic upfront software licenses to predictable monthly recurring revenue. Our agentic voice models can now perform multi-step transactional tasks—like booking service appointments or processing complex food orders—fully autonomously. Enterprise pipeline is at an all-time high.'",
            "verdict": "ARR STABILITY FOCUS"
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL & MARKET PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "retail_sentiment_score": 68,
    "institutional_sentiment_score": 74,
    "composite_sentiment_score": 71,
    "sentiment_breakdown": {
        "retail_pulse": "Mixed to Cautious (-7.5% AH). Retail retail traders on r/wallstreetbets and FinTwit are disappointed by the margin compression and pushed-out EBITDA timeline, though pleased by 2027 guidance.",
        "sell_side_reaction": "Constructive on long-term strategy. Wedbush and Ladenburg view the contract pruning as necessary medicine that clears the decks for clean 2027 margin expansion.",
        "management_tone": "Pragmatic, resolute, and forward-looking. Keyvan Mohajer emphasized building a high-margin recurring business over chasing low-margin point-in-time revenue.",
        "options_iv_crush": "Options implied move was ±12.38%. The post-earnings dip of -7.51% remained inside the implied corridor, generating substantial IV crush on weekly call options."
    },
    "after_hours_driver": "Stock declined -7.51% to $3.94 as gross margin fell to 34.09% and management reset 2026 revenue guidance to $255M midpoint due to strategic non-renewal of negative margin contracts, despite initiating strong 2027 revenue targets ($350M-$400M) and doubling cost synergies to $120M."
}

# Write files to post_agent_bus
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print(f"Successfully generated post agent bus files for {TICKER} ({DATE}).")
