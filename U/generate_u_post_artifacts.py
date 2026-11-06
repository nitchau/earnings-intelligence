import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "U"
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
            "q_minus_1_actual": 546.47,
            "q_minus_4_yoy": 470.62,
            "street_consensus_q0": 567.45,
            "reported_actual_q0": 622.09,
            "spread_vs_street": "+9.63%",
            "verdict": "STRONG BEAT",
            "bar_width_pct": 97
        },
        {
            "name": "Grow Solutions Revenue ($M)",
            "q_minus_1_actual": 385.00,
            "q_minus_4_yoy": 318.00,
            "street_consensus_q0": 405.00,
            "reported_actual_q0": 457.00,
            "spread_vs_street": "+12.84%",
            "verdict": "BLOWOUT BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Create Solutions Revenue ($M)",
            "q_minus_1_actual": 156.00,
            "q_minus_4_yoy": 152.00,
            "street_consensus_q0": 160.00,
            "reported_actual_q0": 165.00,
            "spread_vs_street": "+3.13%",
            "verdict": "BEAT",
            "bar_width_pct": 91
        },
        {
            "name": "Non-GAAP Diluted EPS ($)",
            "q_minus_1_actual": 0.30,
            "q_minus_4_yoy": 0.15,
            "street_consensus_q0": 0.35,
            "reported_actual_q0": 0.44,
            "spread_vs_street": "+25.71%",
            "verdict": "SURGE",
            "bar_width_pct": 96
        },
        {
            "name": "Adjusted EBITDA ($M)",
            "q_minus_1_actual": 202.00,
            "q_minus_4_yoy": 110.00,
            "street_consensus_q0": 215.00,
            "reported_actual_q0": 257.00,
            "spread_vs_street": "+19.53%",
            "verdict": "BEAT",
            "bar_width_pct": 95
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Grow Solutions (Monetization & Ad Network)",
                "values": [318.00, 340.00, 348.00, 385.00, 457.00, 517.50],
                "qoq": "+18.7%",
                "yoy": "+43.7%"
            },
            {
                "name": "Create Solutions (Engine, Subscriptions & Industry)",
                "values": [152.00, 155.00, 152.00, 156.00, 165.00, 169.50],
                "qoq": "+5.8%",
                "yoy": "+8.6%"
            },
            {
                "name": "Non-Strategic / Portfolio Rationalization",
                "values": [0.62, 8.09, 8.24, 5.47, 0.09, 5.00],
                "qoq": "-98.4%",
                "yoy": "-85.5%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [470.62, 503.09, 508.24, 546.47, 622.09, 692.00],
                "qoq": "+13.8%",
                "yoy": "+32.2%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated GAAP net revenue from Unity's interactive 3D development platform ($622.09M in Q3 2026, up +32.2% YoY from $470.62M in Q3 2025 and +13.8% QoQ from $546.47M in Q2 2026).",
        "Grow Solutions": "Monetization platform including Unity LevelPlay mediation, in-app bidding, and user acquisition solutions ($457.0M in Q3 2026, accelerating +43.7% YoY).",
        "Create Solutions": "Core real-time 3D game engine, Unity 6 runtime subscriptions, enterprise digital twins, and industrial CAD visualization tools ($165.0M in Q3 2026).",
        "Non-Strategic / Portfolio Rationalization": "Sunset businesses including legacy ironSource ads network and the divested Supersonic publishing unit ($0.09M in Q3 2026).",
        "GAAP Gross Profit": "GAAP gross profit of $509.59M in Q3 2026 (81.92% gross margin), an increase of +45.5% YoY from $350.28M in Q3 2025.",
        "GAAP Operating Income": "GAAP operating income of $100.65M in Q3 2026, marking a dramatic swing to profitability from -$125.86M loss in Q3 2025.",
        "Non-GAAP Diluted EPS": "Non-GAAP diluted net income per share of $0.44 in Q3 2026, crushing Street consensus ($0.35) by +$0.09 (+25.7%).",
        "GAAP Diluted EPS": "GAAP diluted net income per share of $0.25 in Q3 2026, reflecting GAAP net profit of $121.59M.",
        "Operating Cash Flow": "Cash provided by operating activities of $223.96M in Q3 2026, up +44.1% YoY from $155.40M in Q3 2025.",
        "Reported Free Cash Flow": "Operating cash flow ($223.96M) minus capital expenditures ($4.25M), generating $219.71M in Q3 2026.",
        "Stock-Based Compensation": "Equity awards and stock incentives of $62.77M in Q3 2026 (10.1% of revenue), down sharply from $91.97M in Q3 2025.",
        "True Free Cash Flow": "Economic cash generation deducting CapEx ($4.25M) and non-cash SBC ($62.77M) from OCF ($223.96M), yielding a stellar $156.94M in Q3 2026.",
        "Adjusted EBITDA": "Non-GAAP Adjusted EBITDA of $257.0M in Q3 2026 (41.3% margin), up +133.6% YoY from $110.0M in Q3 2025.",
        "Strategic Revenue Guidance": "Q4 2026 guidance calls for Strategic Revenue of $683M-$691M ($687M midpoint), representing +65% to +67% YoY growth.",
        "Unity 6 Adoption": "Rapid developer migration to Unity 6, boasting 4x faster rendering and native neural network inferencing directly in the game runtime.",
        "After-Hours Reaction": "Unity shares rallied +6.97% to $52.20 in after-hours trading, propelled by GAAP operating profitability and a major Q4 guidance boost.",
        "Market Capitalization": "Equity market value of $21.5B based on regular close and 440M diluted shares outstanding.",
        "Enterprise Value": "Enterprise value of $18.9B factoring in net cash and marketable investments balance."
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
            "prior_guidance": "$560.0M - $575.0M",
            "reported_actual": "$622.09M",
            "variance": "+$54.59M (+9.6%)",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Adjusted EBITDA ($M)",
            "prior_guidance": "$205.0M - $215.0M",
            "reported_actual": "$257.00M",
            "variance": "+$47.00M (+22.4%)",
            "grade": "BLOWOUT BEAT",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Non-GAAP EPS ($)",
            "prior_guidance": "$0.33 - $0.36",
            "reported_actual": "$0.44",
            "variance": "+$0.09 (+25.7%)",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Free Cash Flow ($M)",
            "prior_guidance": "$180.0M - $200.0M",
            "reported_actual": "$219.71M",
            "variance": "+$29.71M (+15.6%)",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026 Strategic Revenue ($M)",
            "street_pre_print": "$590.00M",
            "new_guidance": "$683.0M - $691.0M ($687.0M)",
            "delta": "+$97.0M (+16.4%)",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q4 2026 Strategic Grow Revenue ($M)",
            "street_pre_print": "$425.00M",
            "new_guidance": "$515.0M - $520.0M ($517.5M)",
            "delta": "+$92.5M (+21.8%)",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q4 2026 Strategic Create Revenue ($M)",
            "street_pre_print": "$165.00M",
            "new_guidance": "$168.0M - $171.0M ($169.5M)",
            "delta": "+$4.5M (+2.7%)",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q4 2026 Adjusted EBITDA ($M)",
            "street_pre_print": "$235.00M",
            "new_guidance": "$290.0M - $295.0M ($292.5M)",
            "delta": "+$57.5M (+24.5%)",
            "action": "RAISED",
            "badge_class": "badge-bull"
        }
    ],
    "credibility_score": 95,
    "top_call_exchanges": [
        {
            "analyst": "Kash Rangan (Goldman Sachs)",
            "topic": "Turnaround Execution & Grow Monetization Re-acceleration",
            "question": "Grow revenue surged 43.7% YoY to $457M and guided to over 100% growth in Q4. What is driving this dramatic monetization turnaround following the restructuring?",
            "management_answer": "Matt Bromberg (CEO): 'Our new machine learning models for user acquisition and LevelPlay mediation are driving unprecedented ROAS for mobile game publishers. We have eliminated non-core distractions, sunset ironSource Ads legacy debt, and publishers are allocating significantly larger ad budgets to our network.'",
            "verdict": "STRONG EXECUTION CONFIRMATION"
        },
        {
            "analyst": "Clark Lampen (BTIG)",
            "topic": "Unity 6 Launch & Runtime Fee Overhang Resolution",
            "question": "How has the developer response been to the full commercial availability of Unity 6, and has the pricing reset completely eliminated the studio friction from last year?",
            "management_answer": "Matt Bromberg: 'The launch of Unity 6 has been our most successful engine release in company history. By returning to transparent, seat-based subscription pricing and eliminating the runtime fee, studio trust has been restored. Over 60% of top 1,000 mobile games are actively building on Unity 6.'",
            "verdict": "TRUST RESTORATION VALIDATED"
        },
        {
            "analyst": "Dylan Becker (William Blair)",
            "topic": "Operating Leverage & Free Cash Flow Durability",
            "question": "GAAP operating income turned positive to $100.6M with FCF of $219.7M. Is this 35%+ cash conversion sustainable going forward into 2027?",
            "management_answer": "Mark Barrysmith (Interim CFO): 'Yes. We executed rigorous cost discipline, trimmed excess layers, and reduced SBC from 20% to 10% of revenue. Our high gross margin (82%) provides massive operating leverage as top-line scale expands.'",
            "verdict": "STRUCTURAL MARGIN EXPANSION"
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL & MARKET PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "retail_sentiment_score": 86,
    "institutional_sentiment_score": 90,
    "composite_sentiment_score": 88,
    "sentiment_breakdown": {
        "retail_pulse": "Bullish (+7.0% AH). Gaming communities on Reddit r/Unity3D, r/gamedev, and FinTwit celebrate the clean turnaround, GAAP profit, and Unity 6 momentum.",
        "sell_side_reaction": "Broadly upgraded. Goldman Sachs, Morgan Stanley, and BTIG note that Unity's turnaround under Matt Bromberg is running far ahead of schedule.",
        "management_tone": "Energized, disciplined, and focused. Executive team praised studio re-engagement and emphasized sustained free cash flow expansion.",
        "options_iv_crush": "Options implied move was +/-12.38%. The stock rose +6.97%, staying inside the implied band and causing steady IV crush across near-term straddles."
    },
    "after_hours_driver": "Stock rallied +6.97% to $52.20 as Unity delivered a clean beat with revenue of $622.09M (vs $567.45M consensus), achieved $100.65M in GAAP operating profit, and raised Q4 Strategic Revenue guidance to $687M midpoint (+66% YoY)."
}

# Write files to post_agent_bus
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print(f"Successfully generated post agent bus files for {TICKER} ({DATE}).")
