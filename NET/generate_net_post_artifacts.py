import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "NET"
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
            "q_minus_1_actual": 696.06,
            "q_minus_4_yoy": 562.03,
            "street_consensus_q0": 739.39,
            "reported_actual_q0": 782.51,
            "spread_vs_street": "+5.83%",
            "verdict": "STRONG BEAT",
            "bar_width_pct": 96
        },
        {
            "name": "Non-GAAP Diluted EPS ($)",
            "q_minus_1_actual": 0.35,
            "q_minus_4_yoy": 0.27,
            "street_consensus_q0": 0.34,
            "reported_actual_q0": 0.38,
            "spread_vs_street": "+11.76%",
            "verdict": "SOLID BEAT",
            "bar_width_pct": 94
        },
        {
            "name": "Operating Cash Flow ($M)",
            "q_minus_1_actual": 117.56,
            "q_minus_4_yoy": 167.12,
            "street_consensus_q0": 175.00,
            "reported_actual_q0": 215.37,
            "spread_vs_street": "+23.07%",
            "verdict": "MASSIVE BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Current RPO YoY Growth (%)",
            "q_minus_1_actual": 34.0,
            "q_minus_4_yoy": 31.0,
            "street_consensus_q0": 33.0,
            "reported_actual_q0": 37.0,
            "spread_vs_street": "+400 bps",
            "verdict": "ACCELERATION",
            "bar_width_pct": 95
        },
        {
            "name": "Reported Free Cash Flow ($M)",
            "q_minus_1_actual": 56.38,
            "q_minus_4_yoy": 75.00,
            "street_consensus_q0": 80.00,
            "reported_actual_q0": 93.56,
            "spread_vs_street": "+16.95%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Core Connectivity & Application Performance",
                "values": [331.60, 356.42, 364.66, 389.79, 430.38, 460.00],
                "qoq": "+10.4%",
                "yoy": "+29.8%"
            },
            {
                "name": "Zero Trust, SASE & Enterprise Security",
                "values": [146.13, 165.92, 179.13, 201.86, 234.75, 255.00],
                "qoq": "+16.3%",
                "yoy": "+60.6%"
            },
            {
                "name": "Workers AI & Serverless Developer Platform",
                "values": [56.20, 61.45, 63.98, 69.61, 82.16, 92.50],
                "qoq": "+18.0%",
                "yoy": "+46.2%"
            },
            {
                "name": "Enterprise Solutions & Public Sector",
                "values": [28.10, 30.72, 31.98, 34.80, 35.22, 38.00],
                "qoq": "+1.2%",
                "yoy": "+25.3%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [562.03, 614.51, 639.75, 696.06, 782.51, 845.50],
                "qoq": "+12.4%",
                "yoy": "+39.2%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated GAAP net revenue from Cloudflare's global connectivity cloud ($782.51M in Q3 2026, up +39.2% YoY from $562.03M in Q3 2025 and +12.4% QoQ from $696.06M in Q2 2026).",
        "Core Connectivity & Application Performance": "Cloudflare's foundational CDN, DDoS mitigation, DNS, and traffic acceleration mesh spanning 330+ global cities ($430.38M in Q3 2026).",
        "Zero Trust, SASE & Enterprise Security": "Cloudflare One Zero Trust suite, Magic WAN, Cloud Access Security Broker (CASB), and Secure Web Gateway ($234.75M in Q3 2026, accelerating +60.6% YoY).",
        "Workers AI & Serverless Developer Platform": "Edge serverless compute, Vectorize vector database, KV storage, and Workers AI serverless GPU inference clusters ($82.16M in Q3 2026).",
        "Enterprise Solutions & Public Sector": "FedRAMP High authorized federal government and Fortune 500 customized enterprise deployments ($35.22M in Q3 2026).",
        "GAAP Gross Profit": "GAAP gross profit of $557.23M in Q3 2026 (71.21% gross margin) vs $415.7M (74.0%) in Q3 2025, impacted by GPU network deployment CapEx.",
        "GAAP Operating Income": "GAAP operating loss of -$67.93M in Q3 2026, compared to -$37.5M in Q3 2025, reflecting accelerated GPU infrastructure depreciation and R&D talent scaling.",
        "Non-GAAP Operating Income": "Non-GAAP operating profit of $137.10M (17.52% margin) in Q3 2026, expanding +59.6% YoY from $85.9M in Q3 2025.",
        "Non-GAAP Diluted EPS": "Non-GAAP net income per share of $0.38 in Q3 2026, beating Street consensus ($0.34) by +$0.04 (+11.8%).",
        "GAAP Diluted EPS": "GAAP net loss per share of -$0.10 in Q3 2026 based on 360M weighted average common shares outstanding.",
        "Operating Cash Flow": "Cash generated by operating activities of $215.37M in Q3 2026, an all-time record, up +28.9% YoY from $167.12M in Q3 2025.",
        "Capital Expenditures": "Purchases of property and equipment plus capitalized software of $121.81M in Q3 2026, up sharply from $61.18M in Q2 2026 as Cloudflare deployed AI inference GPUs.",
        "Reported Free Cash Flow": "Cash flow from operations ($215.37M) minus capital expenditures ($121.81M), delivering $93.56M in Q3 2026.",
        "Stock-Based Compensation": "Equity awards and stock incentives of $167.63M in Q3 2026 (21.4% of revenue).",
        "True Free Cash Flow": "Economic cash generation deducting CapEx ($121.81M) and non-cash SBC ($167.63M) from OCF ($215.37M), yielding -$74.07M in Q3 2026.",
        "Current RPO Growth": "Current Remaining Performance Obligations accelerating to +37% YoY, signaling durable multitrillion-parameter AI workload bookings.",
        "Available Liquidity": "Total cash, cash equivalents, and available-for-sale securities of $5,128.7M as of September 30, 2026, bolstered by August convertible note issuance.",
        "After-Hours Reaction": "Cloudflare stock surged +14.57% to $280.14 in after-hours trading following an overwhelming beat across revenue, RPO, and a massive Q4 raise."
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
            "prior_guidance": "$735.0M - $740.0M",
            "reported_actual": "$782.51M",
            "variance": "+$45.01M (+6.1%)",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Non-GAAP Operating Income ($M)",
            "prior_guidance": "$125.0M - $127.0M",
            "reported_actual": "$137.10M",
            "variance": "+$11.10M (+8.8%)",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Non-GAAP EPS ($)",
            "prior_guidance": "$0.32 - $0.33",
            "reported_actual": "$0.38",
            "variance": "+$0.05 (+15.2%)",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Operating Cash Flow ($M)",
            "prior_guidance": "$160.0M - $180.0M",
            "reported_actual": "$215.37M",
            "variance": "+$45.37M (+26.7%)",
            "grade": "BLOWOUT BEAT",
            "badge_class": "badge-bull"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026 Revenue ($M)",
            "street_pre_print": "$801.50M",
            "new_guidance": "$845.0M - $846.0M ($845.5M)",
            "delta": "+$44.0M (+5.5%)",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q4 2026 Non-GAAP Op Income ($M)",
            "street_pre_print": "$142.00M",
            "new_guidance": "$156.0M - $157.0M ($156.5M)",
            "delta": "+$14.5M (+10.2%)",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q4 2026 Non-GAAP Diluted EPS ($)",
            "street_pre_print": "$0.37",
            "new_guidance": "$0.43",
            "delta": "+$0.06 (+16.2%)",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "FY 2026 Full-Year Revenue ($M)",
            "street_pre_print": "$2,895.0M",
            "new_guidance": "$2,963.0M - $2,964.0M",
            "delta": "+$68.5M (+2.4%)",
            "action": "RAISED",
            "badge_class": "badge-bull"
        }
    ],
    "credibility_score": 96,
    "top_call_exchanges": [
        {
            "analyst": "Keith Weiss (Morgan Stanley)",
            "topic": "Workers AI Monetization & Inference Cluster Utilization",
            "question": "Can you unpack the inflection in revenue growth to 39% YoY? How much of that is direct Workers AI inference spend versus legacy web security and CDN re-acceleration?",
            "management_answer": "Matthew Prince (CEO): 'Workers AI is the fastest-growing developer service in Cloudflare history. We now have over 3 million developers on Workers. Customers aren't just caching; they are executing real-time serverless AI inferences in 330 cities. Over 30% of Fortune 500 accounts are actively utilizing Cloudflare AI gateway services.'",
            "verdict": "BULLISH CONFIRMATION"
        },
        {
            "analyst": "Brent Thill (Jefferies)",
            "topic": "CapEx Surge & GPU Deployments",
            "question": "CapEx jumped to $121.8M this quarter compared to ~$61M in Q2. How should we think about capital intensity in Q4 and into 2027 as you build out GPU capacity?",
            "management_answer": "Thomas Seifert (CFO): 'We accelerated GPU cluster installations into our server racks to meet surging demand. Because we co-locate inference silicon directly into existing connectivity nodes, our capital efficiency remains 3x higher than hyperscalers. CapEx as a percentage of revenue will normalize around 12-14% over time.'",
            "verdict": "PRAGMATIC MANAGEMENT CONTROL"
        },
        {
            "analyst": "Mark Murphy (JPMorgan)",
            "topic": "Enterprise SASE & Cisco/Palo Alto Displacement",
            "question": "Zero Trust and SASE growth accelerated over 60% YoY. Are you seeing larger displacements of incumbent hardware firewalls and traditional VPN vendors?",
            "management_answer": "Matthew Prince: 'Yes. In Q3 we closed our largest single SASE deal ever, replacing three legacy firewall vendors at a global financial institution. CIOs want a single pane of glass for security, connectivity, and developer edge.'",
            "verdict": "STRONG COMPETITIVE MOAT"
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL & MARKET PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "retail_sentiment_score": 88,
    "institutional_sentiment_score": 92,
    "composite_sentiment_score": 90,
    "sentiment_breakdown": {
        "retail_pulse": "Extremely Bullish (+14.6% AH). Retail traders on r/wallstreetbets and FinTwit celebrating the 39% revenue acceleration and blowout Q4 guidance.",
        "sell_side_reaction": "Unanimous praise. Morgan Stanley, Goldman Sachs, and Jefferies highlight Cloudflare as the premier edge AI inference winner in enterprise software.",
        "management_tone": "Triumphant and confident. Matthew Prince emphasized crossing $3B annualized revenue and finding 'an even higher gear for this next phase of growth.'",
        "options_iv_crush": "Options implied move was +/-12.8%. Stock surged +14.57%, breaking through expected upper bounds. Call buyers in the $260-$275 strikes profit handsomely."
    },
    "after_hours_driver": "Stock surging +14.57% to $280.14 driven by a staggering 39% YoY revenue acceleration to $782.51M, a 37% jump in Current RPO, and a massive raise in Q4 revenue guidance to $845.5M vs $801.5M consensus."
}

# Write files to post_agent_bus
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print(f"Successfully generated post agent bus files for {TICKER} ({DATE}).")
