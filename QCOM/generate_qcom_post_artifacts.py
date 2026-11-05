import json
import os

os.makedirs("post_agent_bus", exist_ok=True)
ticker = "QCOM"
date = "2026-11-04"

agent2a_data = {
    "ticker": ticker,
    "earnings_date": date,
    "operational_kpis": [
        {
            "name": "Total GAAP Revenue ($M)",
            "q_minus_1_actual": 9947.0,
            "q_minus_4_yoy": 11270.0,
            "street_consensus_q0": 10145.91,
            "reported_actual_q0": 10322.0,
            "spread_vs_street": "+1.74%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "QCT Automotive Revenue ($M)",
            "q_minus_1_actual": 1700.0,
            "q_minus_4_yoy": 1053.0,
            "street_consensus_q0": 1780.0,
            "reported_actual_q0": 1990.0,
            "spread_vs_street": "+11.80%",
            "verdict": "BEAT",
            "bar_width_pct": 96
        },
        {
            "name": "QCT Handsets Revenue ($M)",
            "q_minus_1_actual": 5800.0,
            "q_minus_4_yoy": 6961.0,
            "street_consensus_q0": 5350.0,
            "reported_actual_q0": 5137.0,
            "spread_vs_street": "-3.98%",
            "verdict": "MISS",
            "bar_width_pct": 74
        },
        {
            "name": "QTL Licensing Revenue ($M)",
            "q_minus_1_actual": 1397.0,
            "q_minus_4_yoy": 1409.0,
            "street_consensus_q0": 1320.0,
            "reported_actual_q0": 1304.0,
            "spread_vs_street": "-1.21%",
            "verdict": "IN LINE",
            "bar_width_pct": 82
        },
        {
            "name": "Operating Cash Flow ($M)",
            "q_minus_1_actual": 991.0,
            "q_minus_4_yoy": 3996.0,
            "street_consensus_q0": 2400.0,
            "reported_actual_q0": 2740.0,
            "spread_vs_street": "+14.17%",
            "verdict": "BEAT",
            "bar_width_pct": 93
        }
    ],
    "segment_reporting": {
        "periods": [
            "Q3 2025",
            "Q4 2025",
            "Q1 2026",
            "Q2 2026",
            "Q3 2026 (Actual)",
            "Q4 2026E (Guided / Street)"
        ],
        "segments": [
            {
                "name": "QCT Handsets (Snapdragon Mobile SoC)",
                "values": [6961.0, 7520.0, 6680.0, 5800.0, 5137.0, 5400.0]
            },
            {
                "name": "QCT Automotive (Snapdragon Digital Chassis)",
                "values": [1053.0, 1220.0, 1350.0, 1700.0, 1990.0, 2050.0]
            },
            {
                "name": "QCT IoT & Compute (Snapdragon X Elite / Edge)",
                "values": [1807.0, 1850.0, 1720.0, 1650.0, 1888.0, 1850.0]
            },
            {
                "name": "QTL Licensing (Wireless Patent Royalties)",
                "values": [1409.0, 1600.0, 1449.0, 1397.0, 1304.0, 1400.0]
            }
        ]
    },
    "tooltips": {
        "QCT": "Qualcomm CDMA Technologies: semiconductor chip division comprising Handsets, Automotive, IoT, and AI compute.",
        "QTL": "Qualcomm Technology Licensing: patent licensing division collecting wireless royalty revenues on 3G, 4G, 5G, and Wi-Fi devices.",
        "Snapdragon 8 Elite": "Qualcomm's 3nm flagship mobile application processor and modem platform featuring custom Oryon CPU cores.",
        "Digital Chassis": "Qualcomm's comprehensive automotive tech stack covering infotainment, digital cockpit, and ADAS automated driving.",
        "Snapdragon X Elite": "ARM-based PC processor series delivering 45 TOPS NPU performance for Copilot+ AI personal computers.",
        "Input Cost Inflation": "Industry-wide price increases across leading-edge wafer fabrication, advanced packaging, memory, and substrate materials.",
        "True FCF": "Forensic Free Cash Flow: Operating Cash Flow minus CapEx, Share-Based Compensation, and Capital Leases.",
        "Oryon CPU": "Qualcomm's proprietary custom CPU microarchitecture engineered by Nuvia acquisition, deployed in PC and flagship mobile.",
        "QTL License Renewal": "Multi-year patent licensing agreements extended with tier-1 OEMs including Apple, Huawei, and Transsion.",
        "Data Center AI Ramp": "Multi-generational AI cloud acceleration partnership with Amazon targeting $5B in fiscal 2027 revenue.",
        "Handset Replacement Cycle": "Global smartphone refresh cycles in China and North America influencing volume demand for RF and baseband silicon.",
        "EBT Margin": "Earnings Before Taxes expressed as a percentage of total segment revenue reflecting underlying operational profitability.",
        "Advanced Packaging": "2.5D/3D wafer-level multi-die packaging essential for high-performance AI inference and server chips.",
        "SBC Dilution": "Stock-based compensation awarded to engineering talent, requiring deduction from cash flow to gauge real economic yield.",
        "RF Front-End (RFFE)": "Radio frequency components including power amplifiers, filters, and antenna tuners paired with Snapdragon modems.",
        "China OEM Mix": "Qualcomm's exposure to Chinese smartphone manufacturers including Xiaomi, Oppo, Vivo, and Honor.",
        "ATM Straddle": "At-the-Money options straddle pricing 1-week expected volatility post-earnings print.",
        "Implied Move Band": "The statistically priced expected percentage price excursion derived from options market open interest.",
        "Copilot+ PC": "Microsoft standard for AI PCs requiring dedicated NPUs delivering over 40 TOPS of compute.",
        "Wafer Foundry Allocation": "Contract manufacturing agreements with TSMC and Samsung Foundry for 3nm and 4nm node production."
    }
}

agent2b_data = {
    "ticker": ticker,
    "earnings_date": date,
    "matrix_a_execution_accountability": [
        {
            "metric": "Q4 FY26 Total Revenues",
            "prior_guidance": "$9.9B - $10.7B ($10.30B midpoint)",
            "actual_delivered": "$10,322M delivered (+0.21% above midpoint)",
            "variance_commentary": "Top-line delivered near the upper half of guidance driven by automotive outperformance offsetting mobile handset weakness.",
            "credibility_grade": "MET OWN GUIDE"
        },
        {
            "metric": "Q4 FY26 Non-GAAP Diluted EPS",
            "prior_guidance": "$2.10 - $2.30 ($2.20 midpoint)",
            "actual_delivered": "$2.17 delivered (in-line with guidance range)",
            "variance_commentary": "Non-GAAP EPS arrived in line with the midpoint as automotive mix offset wafer fab cost inflation.",
            "credibility_grade": "MET OWN GUIDE"
        },
        {
            "metric": "QCT Automotive Revenue Run-Rate",
            "prior_guidance": "~$1.7B - $1.8B",
            "actual_delivered": "$1,990M delivered (+89% YoY growth)",
            "variance_commentary": "First ever $2B quarterly revenue print for automotive, accelerating on Digital Chassis cockpit and ADAS rollouts.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Operating Cash Flow Generation",
            "prior_guidance": "$2.2B - $2.5B",
            "actual_delivered": "$2,740M delivered (+14% above expectations)",
            "variance_commentary": "Strong cash collections and working capital discipline lifted operating cash flow to $2.74B.",
            "credibility_grade": "BEAT OWN GUIDE"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q1 FY27 Total Revenues (Q+1E)",
            "pre_print_consensus": "$10,650.0M",
            "management_guidance": "$10.4B - $11.2B ($10.80B midpoint)",
            "delta_vs_street": "+$150.0M (+1.41%) above consensus midpoint",
            "action_badge": "RAISED",
            "pm_rationale": "Guides Q1 FY27 above Wall Street expectations, supported by Snapdragon 8 Elite flagship ramp and automotive momentum."
        },
        {
            "metric": "Q1 FY27 Non-GAAP EPS (Q+1E)",
            "pre_print_consensus": "$2.20",
            "management_guidance": "$2.15 - $2.35 ($2.25 midpoint)",
            "delta_vs_street": "+$0.05 (+2.27%) above consensus midpoint",
            "action_badge": "RAISED",
            "pm_rationale": "Forecasts sequential earnings expansion despite semiconductor supply chain wafer input cost friction."
        },
        {
            "metric": "Q1 FY27 QCT Segment Revenue",
            "pre_print_consensus": "$9,150.0M",
            "management_guidance": "$9.0B - $9.6B ($9.30B midpoint)",
            "delta_vs_street": "+$150.0M above prior baseline",
            "action_badge": "RAISED",
            "pm_rationale": "Reflects first-quarter contribution from data center collaboration and premium mobile tier gains."
        },
        {
            "metric": "Fiscal 2027 Data Center Target",
            "pre_print_consensus": "$3.5B - $4.0B",
            "management_guidance": "$5.0B reiterated target",
            "delta_vs_street": "+$1.0B premium over conservative sell-side models",
            "action_badge": "REITERATED",
            "pm_rationale": "Reiterates aggressive $5B Data Center target for FY27 anchored by multi-generational Amazon partnership."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Stacy Rasgon (Bernstein)",
            "topic": "Handset Revenue Slump (-26% YoY) & Premium ASP Offsets",
            "question": "Can you unpack the 26% year-over-year decline in QCT Handset revenues to $5.14B, and how much traction the new Snapdragon 8 Elite is seeing in offsetting mature smartphone volume drag?",
            "management_answer": "Cristiano Amon explained that the prior year comparison included anomalous channel replenishment. In Q4, premium and high-tier content expanded significantly with Chinese OEMs adopting the Snapdragon 8 Elite, which commands substantially higher ASPs. Smartphone volume may be mature, but silicon dollar content per device is rising 15-20%."
        },
        {
            "analyst": "Ross Seymore (Deutsche Bank)",
            "topic": "Wafer Input Cost Inflation & Gross Margin Inflection Timeline",
            "question": "Management explicitly cited broad-based semiconductor input cost increases across wafers, packaging, and materials. When will pricing adjustments fully offset these cost pressures in gross margins?",
            "management_answer": "CFO Akash Palkhiwala stated that cost inflation at leading-edge foundry nodes is being actively addressed via renegotiated contract pricing with OEM partners. However, because product shipments lag price adjustments, the full benefit to QCT gross margins will materialize in the second half of fiscal 2027."
        },
        {
            "analyst": "Blayne Curtis (Barclays)",
            "topic": "Automotive $2B Milestone & Amazon AI Data Center Architecture",
            "question": "Automotive reached a historic $1.99B run-rate growing 89% YoY. Concurrently, you announced an Amazon data center collaboration. How should investors model the FY27 $5B data center ramp vs automotive?",
            "management_answer": "Cristiano Amon highlighted that the automotive design win backlog now exceeds $45B, with ADAS and digital cockpit deployments scaling globally. The Amazon partnership represents a multi-generational inference architecture that will ramp in late FY27, underpinning the reiterated $5B data center revenue target."
        }
    ]
}

agent2c_data = {
    "ticker": ticker,
    "earnings_date": date,
    "four_pillar_sentiment": {
        "institutional_score": 68,
        "retail_score": 52,
        "options_skew_score": 60,
        "sell_side_score": 75,
        "composite_verdict": "Transitional AI & Auto Growth vs Near-Term Handset & Cost Friction"
    },
    "retail_pulse": {
        "score": 52,
        "tone": "Disappointment on Handset Contraction Offset by Auto Hype",
        "key_themes": [
            "Reddit r/stocks and FinTwit reacting sharply to the -7.4% after-hours drop to $160.37, noting smartphone revenues plummeted 26% YoY to $5.14B",
            "Retail bulls circulating the 89% YoY surge in Automotive to $1.99B and the Amazon AI data center partnership announcement",
            "Traders expressing frustration that despite beating revenue estimates ($10.32B vs $10.15B), gross margin cost commentary triggered algorithmic selling"
        ]
    },
    "institutional_positioning": {
        "score": 68,
        "tone": "Cautious Multi-Expansion Pending 2H FY27 Margin Recovery",
        "key_themes": [
            "Tier 1 sell-side desks noting that while Non-GAAP EPS met bogeys and Q1 FY27 revenue guidance ($10.8B midpoint) beat consensus, wafer cost inflation limits near-term multiple expansion",
            "Institutions modeling 2H FY27 as the key margin inflection point once price increases take effect",
            "Options volatility crush contained comfortably within the \u00b19.0% ($15.10) priced weekly straddle band, with the -7.4% move trading inside expected bounds"
        ]
    },
    "pm_takeaway": "Qualcomm reported a mixed but strategically compelling Q4 FY26 print. Total revenue of $10,322M (+1.74% vs consensus $10,145.91M) beat expectations, driven by record Automotive revenues of $1,990M (+89% YoY) and steady IoT at $1,888M. However, Handsets contracted 26% YoY to $5,137M, and management highlighted industry-wide wafer and packaging input cost inflation that will suppress gross margins until price increases take full effect in 2H FY27. Operating cash flow stood strong at $2,740M ($1,824M reported FCF and $951M True FCF). With Q1 FY27 revenue guidance raised to $10.4B-$11.2B and long-term QTL licensing agreements renewed with Apple, Huawei, and Transsion, alongside an Amazon AI data center alliance, the -7.4% after-hours pullback to $160.37 presents a high-risk/high-reward entry for patient capital."
}

with open(f"post_agent_bus/{ticker}_{date}_agent2a_kpis.json", "w") as f:
    json.dump(agent2a_data, f, indent=2)

with open(f"post_agent_bus/{ticker}_{date}_agent2b_transcript.json", "w") as f:
    json.dump(agent2b_data, f, indent=2)

with open(f"post_agent_bus/{ticker}_{date}_agent2c_social.json", "w") as f:
    json.dump(agent2c_data, f, indent=2)

print(f"[OK] Generated post_agent_bus files for {ticker} {date}")
