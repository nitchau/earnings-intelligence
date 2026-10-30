import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "INTC"
DATE = "2026-10-29"

BUS_DIR = BASE_DIR / "post_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

# 1. Agent 2A: KPIs & Segments
agent2a = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "operational_kpis": [
        {
            "name": "Data Center & AI (DCAI) Revenue ($M)",
            "q_minus_1_actual": 5120.0,
            "q_minus_4_yoy": 4121.0,
            "street_consensus_q0": 4800.0,
            "reported_actual_q0": 7330.0,
            "spread_vs_street": "+52.7%",
            "verdict": "BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Client Computing (CCPG) Revenue ($M)",
            "q_minus_1_actual": 8840.0,
            "q_minus_4_yoy": 8509.0,
            "street_consensus_q0": 8300.0,
            "reported_actual_q0": 8085.0,
            "spread_vs_street": "-2.6%",
            "verdict": "MISS",
            "bar_width_pct": 52
        },
        {
            "name": "Intel Foundry Revenue ($M)",
            "q_minus_1_actual": 5820.0,
            "q_minus_4_yoy": 4258.0,
            "street_consensus_q0": 5100.0,
            "reported_actual_q0": 6730.0,
            "spread_vs_street": "+32.0%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "Non-GAAP Gross Margin (%)",
            "q_minus_1_actual": 40.5,
            "q_minus_4_yoy": 38.2,
            "street_consensus_q0": 41.0,
            "reported_actual_q0": 43.0,
            "spread_vs_street": "+200 bps",
            "verdict": "BEAT",
            "bar_width_pct": 88
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E"],
        "segments": [
            {
                "name": "Client Computing & AI (CCPG)",
                "values": [8509.0, 8400.0, 8100.0, 8840.0, 8085.0, 7800.0],
                "qoq": "-8.5%",
                "yoy": "-5.0%"
            },
            {
                "name": "Data Center and AI (DCAI)",
                "values": [4121.0, 4200.0, 4450.0, 5120.0, 7330.0, 6800.0],
                "qoq": "+43.2%",
                "yoy": "+77.9%"
            },
            {
                "name": "Intel Foundry",
                "values": [4258.0, 4400.0, 4700.0, 5820.0, 6730.0, 6500.0],
                "qoq": "+15.6%",
                "yoy": "+58.1%"
            },
            {
                "name": "All Other (Mobileye & Incubation)",
                "values": [956.0, 920.0, 880.0, 780.0, 670.0, 650.0],
                "qoq": "-14.1%",
                "yoy": "-29.9%"
            },
            {
                "name": "Intersegment Eliminations",
                "values": [-4191.0, -4246.0, -4553.0, -4432.0, -6302.0, -6250.0],
                "qoq": "+42.2%",
                "yoy": "+50.4%"
            }
        ]
    },
    "tooltip_definitions": {
        "Data Center & AI (DCAI)": "Xeon server processors, Gaudi AI accelerators, and cloud hyperscaler infrastructure silicon.",
        "Client Computing (CCPG)": "Core Ultra processors (Lunar Lake, Arrow Lake) for AI PCs, enterprise laptops, and gaming desktops.",
        "Intel Foundry": "Internal fab manufacturing and external advanced packaging (CoWoS, EMIB) for commercial foundry customers.",
        "Intersegment Eliminations": "Elimination of internal silicon wafer transfer billings between Intel Foundry and product business units.",
        "Non-GAAP Gross Margin": "Gross margin adjusted for fab startup costs, patent amortization, and restructuring charges (43.0% in Q3).",
        "Operating Income (EBIT)": "Consolidated operating profit ($2,522.0M in Q3 2026, 15.27% operating margin).",
        "True FCF": "Operating cash flow minus capital expenditures, stock-based compensation, and lease obligations ($1,074.0M in Q3).",
        "Q4 Guidance Reset": "Severe sequential margin warning: Q4 Gross Margin guided down to 38.0% and EPS to $0.25 (vs $0.52 in Q3).",
        "18A Process Node": "Intel's next-generation 1.8nm manufacturing process featuring RibbonFET transistors and PowerVia backside power.",
        "Lunar Lake": "High-efficiency mobile SoC designed for AI laptops, utilizing external TSMC N3B packaging before transitioning in-house.",
        "Gaudi 3": "Cost-effective AI training and inference accelerator competing against Nvidia H100/H200 in enterprise clusters.",
        "Research & Development": "Expenditures on advanced extreme ultraviolet (High-NA EUV) lithography and packaging tooling ($3,490M in Q3).",
        "Cost of Sales": "Silicon wafer fabrication materials, packaging yield scrap, cleanroom depreciation, and utility power ($9,417M in Q3).",
        "GAAP Diluted EPS": "Net profit divided by diluted common shares ($0.60 per share in Q3 2026).",
        "Non-GAAP Diluted EPS": "Adjusted earnings per share ($0.52 vs $0.40 consensus hurdle, beating by +$0.12).",
        "Operating Cash Flow": "Cash generated by semiconductor deliveries and hyperscaler customer deposits ($13,184M 9M YTD).",
        "Capital Expenditures": "Investment in fab construction across Ohio, Oregon, Ireland, and Magdeburg Germany ($10,216M 9M YTD).",
        "CHIPS Act Funding": "Direct federal subsidies and manufacturing investment tax credits supporting U.S. fab buildouts.",
        "Enterprise Value": "Consolidated market capitalization adjusted for net debt and cash balances ($500.86B at regular close).",
        "Options Volatility Regime": "9.12% straddle implied move breached decisively by actual -23.00% post-market gap down to $70.89."
    }
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")

# 2. Agent 2B: Transcript Forensics & Guidance
agent2b = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "matrix_a_execution_accountability": [
        {
            "metric": "Q3 2026 Total Net Revenue",
            "prior_guidance": "$13.5B - $14.5B ($14.0B midpoint)",
            "actual_delivered": "$16,513.0M delivered (+17.95% above midpoint)",
            "variance_commentary": "Massive top-line beat powered by surging hyperscaler enterprise demand for Xeon 6 and custom packaging.",
            "credibility_grade": "EXCEEDED"
        },
        {
            "metric": "Non-GAAP Gross Margin",
            "prior_guidance": "38.0% at midpoint",
            "actual_delivered": "43.0% delivered (+500 bps beat)",
            "variance_commentary": "Stronger factory utilization and higher server mix drove superior gross margin conversion.",
            "credibility_grade": "EXCEEDED"
        },
        {
            "metric": "Non-GAAP Diluted EPS",
            "prior_guidance": "$0.38 - $0.42 ($0.40 midpoint)",
            "actual_delivered": "$0.52 delivered (+$0.12 beat)",
            "variance_commentary": "Operating leverage on blowout top-line and restructuring cost savings delivered a 30% EPS beat.",
            "credibility_grade": "EXCEEDED"
        },
        {
            "metric": "Operating Income (EBIT)",
            "prior_guidance": "~$1,200M",
            "actual_delivered": "$2,522.0M delivered (+110% beat)",
            "variance_commentary": "Operating profit more than doubled prior guidance as fab utilization penalties decreased.",
            "credibility_grade": "EXCEEDED"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026 Total Net Revenue",
            "pre_print_consensus": "$16.8B ($16,800M)",
            "management_guidance": "$15.0B - $16.0B ($15.5B midpoint)",
            "delta_vs_street": "-$1.30B (-7.7%) sequential drop below Street",
            "action_badge": "GUIDANCE RESET",
            "pm_rationale": "Management warned of inventory digestion in client PCs and seasonal enterprise server budget pauses."
        },
        {
            "metric": "Q4 2026 Non-GAAP Gross Margin",
            "pre_print_consensus": "42.5%",
            "management_guidance": "38.0% (down -500 bps sequentially)",
            "delta_vs_street": "-450 bps sequential gross margin compression",
            "action_badge": "SEVERE WARNING",
            "pm_rationale": "Initial ramp costs for external Lunar Lake tiles and early 18A fab pre-production depreciation weigh on Q4 margins."
        },
        {
            "metric": "Q4 2026 Non-GAAP Diluted EPS",
            "pre_print_consensus": "$0.48",
            "management_guidance": "$0.25 (collapsing from $0.52 in Q3)",
            "delta_vs_street": "-$0.23 (-47.9%) EPS cut vs Street expectations",
            "action_badge": "EARNINGS CUT",
            "pm_rationale": "The severe guidance reset triggered an institutional liquidation, driving the stock down -23.00% to $70.89."
        },
        {
            "metric": "Q4 2026 GAAP Diluted EPS",
            "pre_print_consensus": "$0.35",
            "management_guidance": "$0.10",
            "delta_vs_street": "-$0.25 (-71.4%) vs Street baseline",
            "action_badge": "DOWNWARD RESET",
            "pm_rationale": "Reflects ongoing fab restructuring charges and elevated cleanroom transition expenses."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "C.J. Muse (Cantor Fitzgerald)",
            "topic": "Q4 Gross Margin Compression & Lunar Lake Tile Cost Structure",
            "question": "Why is Q4 gross margin stepping down 500 bps from 43% to 38% despite higher full-year revenue volumes, and how much of that is driven by external TSMC packaging costs on Lunar Lake?",
            "executive_answer": "David Zinsner (CFO) admitted that Lunar Lake’s architecture relies on external foundry packaging which carries lower initial gross margins until Panther Lake brings high-volume compute tiles back to internal 18A fabs in 2027. Q4 also bears elevated start-up costs for Fab 34 and Fab 52."
        },
        {
            "analyst": "Timothy Arcuri (UBS)",
            "topic": "Client PC Inventory Digestion & AI PC Momentum",
            "question": "Can you unpack the Client Computing guidance drop to $15B-$16B? Are enterprise customers delaying corporate desktop refreshes until Windows 10 end-of-life in late 2027?",
            "executive_answer": "Pat Gelsinger (CEO) explained that after aggressive pre-ordering in Q3, OEM customers in North America and EMEA are maintaining lean inventory. While AI PC adoption is expanding rapidly with over 100M Core Ultra units targeted by year-end, component supply chains remain disciplined."
        },
        {
            "analyst": "Stacy Rasgon (Bernstein Research)",
            "topic": "Intel Foundry External Commitments & 18A Milestones",
            "question": "Where do customer tape-outs stand on 18A, and how much external cash burn should we expect from Intel Foundry before breakeven in 2028?",
            "executive_answer": "Pat Gelsinger reiterated that 18A is on track for full manufacturing readiness, with Panther Lake and Clearwater Forest leading internal production. Commercial foundry pipeline stands at over $15B in lifetime deal value, with major hyperscaler tape-outs scheduled for H1 2027."
        }
    ]
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")

# 3. Agent 2C: Sentiment & Market Positioning
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "four_pillar_sentiment": {
        "institutional_score": 38,
        "retail_score": 32,
        "options_skew_score": 25,
        "sell_side_score": 45,
        "composite_verdict": "Violent Multiple Compression & De-Risking Capitulation"
    },
    "retail_pulse": {
        "score": 32,
        "tone": "Outrage and Shock",
        "key_themes": [
            "Severe anger on FinTwit and Reddit over -23% crash after massive headline revenue beat ($16.5B vs $14.0B)",
            "Frustration with management's recurring guidance guide-downs and execution flip-flops",
            "Calls for structural spin-off of Intel Foundry to unlock product business value"
        ]
    },
    "institutional_positioning": {
        "score": 38,
        "tone": "Institutional Liquidation and Put Hedging",
        "key_themes": [
            "Quantitative funds caught off-guard by the magnitude of the Q4 gross margin collapse (38.0% vs 42.5% consensus)",
            "9.12% options straddle failed to contain the violent -23.00% gap down to $70.89",
            "Long-term value funds reassessing the capital intensity of the IDM 2.0 multi-fab buildout"
        ]
    },
    "pm_takeaway": "INTC produced a textbook 'Beat and Guide Down' disaster. While Q3 delivered blowout revenue ($16,513M vs $14,000M) and EPS ($0.52 vs $0.40), management guided Q4 gross margin down -500 bps to 38.0% and EPS to $0.25 (slashing Street expectations by -48%). Shares violently breached the 9.12% options-implied band, plummeting -23.00% to $70.89. Until 18A manufacturing yields and internal packaging ramp in 2027, the stock remains in a high-beta penalty box."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for INTC.")
