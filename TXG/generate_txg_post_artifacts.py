import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "TXG"
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
            "q_minus_1_actual": 151.04,
            "q_minus_4_yoy": 149.00,
            "street_consensus_q0": 147.85,
            "reported_actual_q0": 150.67,
            "spread_vs_street": "+1.91%",
            "verdict": "BEAT",
            "bar_width_pct": 88
        },
        {
            "name": "Consumables Revenue ($M)",
            "q_minus_1_actual": 132.35,
            "q_minus_4_yoy": 127.89,
            "street_consensus_q0": 131.50,
            "reported_actual_q0": 134.33,
            "spread_vs_street": "+2.15%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "Instruments Revenue ($M)",
            "q_minus_1_actual": 9.42,
            "q_minus_4_yoy": 12.00,
            "street_consensus_q0": 10.50,
            "reported_actual_q0": 6.86,
            "spread_vs_street": "-34.67%",
            "verdict": "DRAG",
            "bar_width_pct": 65
        },
        {
            "name": "GAAP Gross Margin (%)",
            "q_minus_1_actual": 74.48,
            "q_minus_4_yoy": 67.32,
            "street_consensus_q0": 71.50,
            "reported_actual_q0": 74.95,
            "spread_vs_street": "+345 bps",
            "verdict": "EXPANSION",
            "bar_width_pct": 95
        },
        {
            "name": "Non-GAAP Diluted EPS ($)",
            "q_minus_1_actual": -0.14,
            "q_minus_4_yoy": -0.22,
            "street_consensus_q0": -0.02,
            "reported_actual_q0": -0.15,
            "spread_vs_street": "-$0.13",
            "verdict": "MISS",
            "bar_width_pct": 68
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Consumables Revenue",
                "values": [127.89, 138.50, 128.20, 132.35, 134.33, 150.00],
                "qoq": "+1.5%",
                "yoy": "+5.0%"
            },
            {
                "name": "Instruments Revenue",
                "values": [12.00, 18.20, 13.50, 9.42, 6.86, 15.00],
                "qoq": "-27.2%",
                "yoy": "-42.8%"
            },
            {
                "name": "Services & Other Revenue",
                "values": [9.11, 9.33, 9.14, 9.27, 9.48, 10.00],
                "qoq": "+2.3%",
                "yoy": "+4.1%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [149.00, 166.03, 150.84, 151.04, 150.67, 175.00],
                "qoq": "-0.2%",
                "yoy": "+1.1%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated GAAP net revenue from 10x Genomics instruments, consumables, and biological cloud software ($150.67M in Q3 2026, beating Street consensus $147.85M by +1.91%).",
        "Consumables Revenue": "Recurring high-margin reagent kits and microfluidic chips across Chromium Single Cell and Visium/Xenium spatial biology ($134.33M in Q3 2026, up +5.0% YoY).",
        "Instruments Revenue": "Capital hardware placements of Chromium, Visium, Xenium, and newly launched Atera platforms ($6.86M in Q3 2026, down -42.8% YoY due to budget freezes).",
        "Services & Other Revenue": "Contract sequencing services, biopharma validation pilots, software subscriptions, and non-recurring patent litigation licensing royalties ($9.48M in Q3 2026).",
        "GAAP Gross Profit": "Gross profit of $112.93M in Q3 2026 delivering a 74.95% gross margin, expanding 763 bps YoY from 67.32% due to lower inventory write-downs and favorable mix.",
        "GAAP Operating Income": "Operating loss of -$16.06M in Q3 2026 ($112.93M Gross Profit - $128.98M OpEx), improving by over 50% from -$32.24M in Q3 2025 on overhead discipline.",
        "GAAP Diluted EPS": "GAAP diluted net loss per share of -$0.15 in Q3 2026 based on 130.8M weighted average common shares outstanding.",
        "Operating Cash Flow": "Operating cash flow of $25.25M generated in Q3 2026, rising +48.8% sequentially from $16.97M in Q2 2026.",
        "Capital Expenditures": "Property, plant, and laboratory equipment additions of $1.60M in Q3 2026, reflecting lean facility investments.",
        "Reported Free Cash Flow": "Operating cash flow ($25.25M) minus CapEx ($1.60M), generating positive reported free cash flow of $23.65M in Q3 2026.",
        "Stock-Based Compensation": "Non-cash equity incentives and stock compensation of $23.10M in Q3 2026 ($8.94M R&D, $12.00M SG&A, $2.16M COGS).",
        "True Free Cash Flow": "Economic cash generation deducting CapEx ($1.60M) and non-cash SBC ($23.10M) from OCF ($25.25M), yielding positive True FCF of $0.55M in Q3 2026.",
        "Atera Commercial Shipments": "10x Genomics' revolutionary next-generation spatial biology platform, combining in situ transcriptomics and protein detection, with global shipments commenced in Q3.",
        "Sentira Cloud Platform": "Newly introduced cloud analysis platform powered by NVIDIA accelerated computing for spatial imaging and Anthropic's Claude for agentic AI analysis of single-cell datasets.",
        "FY 2026 Revenue Guidance Raise": "Full-year 2026 revenue guidance raised to $625M - $635M ($630.0M midpoint), up from prior guidance of $610M - $630M ($620.0M midpoint).",
        "Implied Q4 2026 Revenue": "Raised FY guidance implies Q4 2026 revenue of approximately $172.5M - $182.5M (~$175.0M midpoint), representing sequential acceleration.",
        "Liquid Treasury Reserves": "Cash, cash equivalents, and marketable securities totaling $575.68M as of September 30, 2026, with zero long-term funded debt.",
        "After-Hours Reaction": "TXG shares declined -9.73% to $52.41 after hours as an EPS miss (-$0.15 vs -$0.02 Street) and instrument revenue weakness (-42.8% YoY) triggered short-term multiple compression.",
        "Academic Budgetary Headwinds": "Constrained NIH funding and institutional grant delays in the U.S. and Europe lengthening instrument procurement decision cycles.",
        "China Biomedical Demand": "Asia-Pacific revenues stabilized at $25.97M ($15.22M China), showing resilient consumables demand despite macroeconomic cross-currents."
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
            "prior_guidance": "$145.0M - $150.0M",
            "reported_actual": "$150.67M",
            "variance": "+$0.67M above top end",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Gross Margin (%)",
            "prior_guidance": "72.0% - 74.0%",
            "reported_actual": "74.95%",
            "variance": "+95 bps above top end",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Operating Cash Flow ($M)",
            "prior_guidance": "$15.0M - $20.0M",
            "reported_actual": "$25.25M",
            "variance": "+$5.25M outperformance",
            "grade": "STRONG OUTPERFORMANCE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Non-GAAP Diluted EPS ($)",
            "prior_guidance": "-$0.05 to -$0.00",
            "reported_actual": "-$0.15",
            "variance": "-$0.10 shortfall",
            "grade": "MISSED OWN RANGE",
            "badge_class": "badge-bear"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "FY 2026 Total Revenue ($M)",
            "street_pre_print": "$622.50M",
            "new_guidance": "$625.0M - $635.0M ($630.0M)",
            "delta": "+$7.50M (+1.2%)",
            "action": "RAISED FY26 OUTLOOK",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Implied Q4 2026 Revenue ($M)",
            "street_pre_print": "$170.00M",
            "new_guidance": "$172.5M - $182.5M (~$175.0M)",
            "delta": "+$5.00M (+2.9%)",
            "action": "ACCELERATION GUIDED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Full-Year Core Growth (ex-Litigation)",
            "street_pre_print": "+3.5% YoY",
            "new_guidance": "+4.0% to +6.0% YoY",
            "delta": "+150 bps upgrade",
            "action": "UPGRADED ORGANIC BOGEY",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Year-End Cash & Equivalents Cushion",
            "street_pre_print": "$550.00M",
            "new_guidance": "Sustained >$575M with Positive Cash Generation",
            "delta": "+$25.0M cushion",
            "action": "RECONFIRMED FORTRESS",
            "badge_class": "badge-bull"
        }
    ],
    "credibility_score": 84,
    "top_call_exchanges": [
        {
            "analyst": "Tycho Peterson (Jefferies)",
            "topic": "Atera Commercial Launch Velocity & Instrument Capex Headwinds",
            "question": "Can you describe the early customer uptake for Atera following the initial commercial shipments? Are researchers substituting existing Xenium placements or expanding into net new spatial budgets?",
            "management_answer": "Serge Saxonov (CEO): 'Atera demand has been extraordinary. What we are seeing is not cannibalization of Xenium, but rather opening up high-throughput translational and biopharma programs that previously could not access subcellular spatial resolution at this scale. While broader instrument capital spending across academic labs remains constrained, Atera represents a must-have system for data-maximalist research.'",
            "verdict": "NET NEW BUDGET CONVERSION"
        },
        {
            "analyst": "Dan Arias (Stifel)",
            "topic": "Gross Margin Resilience & Mix Progression Toward 75%",
            "question": "Gross margin reached 74.95%, up nearly 765 basis points YoY. How sustainable is this mid-70s gross margin as Atera instrument volume ramps against consumables?",
            "management_answer": "Justin McAnear (CFO): 'The gross margin strength this quarter was powered by lower inventory charges, manufacturing efficiency gains in our microfluidic consumables, and a 89% consumables revenue mix. Even as Atera instrument shipments ramp in Q4, the high consumable pull-through per installed instrument gives us confidence that our structural gross margins will remain firmly in the mid-70s.'",
            "verdict": "MID-70s GROSS MARGIN CONFIRMED"
        },
        {
            "analyst": "Tejas Savant (Morgan Stanley)",
            "topic": "Sentira Cloud AI Platform & Monetization with NVIDIA / Claude",
            "question": "How will Sentira be commercialized? Does the integration with NVIDIA accelerated computing and Anthropic Claude create a software ARR subscription stream?",
            "management_answer": "Serge Saxonov (CEO): 'Sentira addresses the biggest bottleneck in biology today: extracting biological truth from massive, complex spatial datasets. By partnering with NVIDIA for accelerated spatial image processing and Anthropic for agentic Claude reasoning across single-cell multiomics, we are transforming 10x into an end-to-end biological intelligence platform. We will monetize Sentira through compute tiers and enterprise SaaS subscriptions.'",
            "verdict": "AI SOFTWARE RECURRING REVENUE CATALYST"
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL & MARKET PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "retail_sentiment_score": 58,
    "institutional_sentiment_score": 70,
    "composite_sentiment_score": 64,
    "sentiment_breakdown": {
        "retail_pulse": "Frustrated by after-hours drop (-9.73% to $52.41). Retail traders on FinTwit and r/biotech are disappointed by the non-GAAP EPS miss (-$0.15 vs -$0.02) and instrument sales decline, despite the top-line beat and guidance raise.",
        "sell_side_reaction": "Constructive on long-term AI-driven inflection. Jefferies, Stifel, and Morgan Stanley applaud the FY26 guidance raise to $630M midpoint and the launch of Sentira with NVIDIA/Claude, viewing the post-print dip as an attractive accumulation opportunity.",
        "management_tone": "Visionary, aggressive, and highly confident in biological data maximalism. Serge Saxonov and Justin McAnear highlighted that 10x is uniquely positioned at the intersection of AI foundation models and high-resolution spatial biology.",
        "options_iv_crush": "Options implied move was ±22.0% ($14.20). The actual after-hours decline of -9.73% (-$5.65) was contained well within the straddle band, delivering significant volatility crush on weekly options."
    },
    "after_hours_driver": "TXG shares declined -9.73% to $52.41 in after-hours trading as a bottom-line EPS miss (-$0.15 vs -$0.02 consensus) and sharp instrument revenue contraction (-42.8% YoY to $6.86M) overshadowed a top-line revenue beat ($150.67M vs $147.85M), gross margin expansion to 74.95%, positive Operating Cash Flow of $25.25M, a raised FY26 revenue guidance corridor ($625M-$635M), and the commercial launch of Sentira with NVIDIA and Anthropic."
}

# Write files to post_agent_bus
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print(f"Successfully generated post agent bus files for {TICKER} ({DATE}).")
