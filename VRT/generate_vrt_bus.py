import json
import os

os.makedirs("post_agent_bus", exist_ok=True)

# -------------------------------------------------------------
# Agent 2A: KPI Discovery Agent
# -------------------------------------------------------------
agent2a = {
    "ticker": "VRT",
    "earnings_date": "2026-10-28",
    "agent_role": "KPI_Discovery_Agent",
    "model": "gemini-3.8-flash-high",
    "company_operational_kpis": [
        {
            "kpi_name": "Organic Orders Growth YoY (%)",
            "definition": "Growth in booked equipment and infrastructure orders excluding foreign currency and acquisition effects, reflecting forward AI data center buildout velocity.",
            "street_consensus": 45.0,
            "t1_whisper": 60.0,
            "reported_q0_actual": 100.0,
            "qoq_change_pct": 35.0,
            "yoy_change_pct": 100.0,
            "vs_consensus_delta": "+55.0% pts vs Consensus",
            "verdict": "BEAT"
        },
        {
            "kpi_name": "Net Sales ($M)",
            "definition": "Total consolidated revenue across critical power, thermal management, modular solutions, and lifecycle services.",
            "street_consensus": 3760.0,
            "t1_whisper": 3950.0,
            "reported_q0_actual": 4312.8,
            "qoq_change_pct": 31.7,
            "yoy_change_pct": 61.2,
            "vs_consensus_delta": "+$552.8M (+14.70%)",
            "verdict": "BEAT"
        },
        {
            "kpi_name": "Adjusted Operating Margin (%)",
            "definition": "Non-GAAP operating profit divided by net sales, excluding corporate transaction costs, amortization, and restructuring.",
            "street_consensus": 23.0,
            "t1_whisper": 24.0,
            "reported_q0_actual": 25.2,
            "qoq_change_pct": 1.9,
            "yoy_change_pct": 2.9,
            "vs_consensus_delta": "+220 bps vs Consensus",
            "verdict": "BEAT"
        },
        {
            "kpi_name": "Americas Net Sales ($M)",
            "definition": "Revenue delivered to hyperscale, colocation, and enterprise customers across North and South America, driven by high-density liquid cooling deployments.",
            "street_consensus": 2500.0,
            "t1_whisper": 2650.0,
            "reported_q0_actual": 2988.8,
            "qoq_change_pct": 35.5,
            "yoy_change_pct": 74.5,
            "vs_consensus_delta": "+$488.8M (+19.55%)",
            "verdict": "BEAT"
        },
        {
            "kpi_name": "Full-Year 2026 Adjusted FCF Guidance ($M)",
            "definition": "Management forecasted free cash flow generation for FY26 reflecting robust operational conversion minus elevated growth CapEx for liquid cooling capacity.",
            "street_consensus": 2500.0,
            "t1_whisper": 2600.0,
            "reported_q0_actual": 2700.0,
            "qoq_change_pct": 15.0,
            "yoy_change_pct": 48.0,
            "vs_consensus_delta": "+$200.0M raise at midpoint",
            "verdict": "BEAT"
        }
    ],
    "reporting_segments_5q_mapping": {
        "headers": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Americas (AMER)",
                "values": [1712.4, 1850.0, 1690.0, 2195.2, 2988.8, 3050.0],
                "yoy_growth_q0": "+74.5% (+66.2% organic)",
                "adj_op_margin_q0": "29.4%"
            },
            {
                "name": "Asia Pacific (APAC)",
                "values": [519.8, 560.0, 525.0, 708.6, 779.3, 800.0],
                "yoy_growth_q0": "+49.9% (+48.3% organic)",
                "adj_op_margin_q0": "17.0%"
            },
            {
                "name": "Europe, Middle East & Africa (EMEA)",
                "values": [443.6, 470.0, 434.5, 370.5, 544.7, 563.0],
                "yoy_growth_q0": "+22.8% (+19.3% organic)",
                "adj_op_margin_q0": "28.0%"
            },
            {
                "name": "Consolidated Net Sales",
                "values": [2675.8, 2880.0, 2649.5, 3274.3, 4312.8, 4413.0],
                "yoy_growth_q0": "+61.2% (+55.0% organic)",
                "adj_op_margin_q0": "25.2%"
            }
        ]
    }
}

with open("post_agent_bus/VRT_2026-10-28_agent2a_kpis.json", "w", encoding="utf-8") as f:
    json.dump(agent2a, f, indent=2)

# -------------------------------------------------------------
# Agent 2B: Transcript Forensic Agent
# -------------------------------------------------------------
agent2b = {
    "ticker": "VRT",
    "earnings_date": "2026-10-28",
    "agent_role": "Transcript_Forensic_Agent",
    "model": "gemini-3.8-flash-high",
    "guidance_accountability_matrix_a": [
        {
            "guided_metric": "Q3 2026 Net Sales ($M)",
            "prior_quarter_guidance": "$3,700M to $3,850M ($3,775M midpoint)",
            "reported_q0_actual": "Delivered $4,312.8M (+61.2% YoY, 55% organic growth)",
            "variance_commentary": "Crushed prior guided top-end by $462.8M (+12.0%) fueled by unprecedented hyperscale AI data center infrastructure acceleration.",
            "credibility_grade": "BEAT OWN GUIDE"
        },
        {
            "guided_metric": "Q3 2026 Adjusted Diluted EPS ($)",
            "prior_quarter_guidance": "$1.75 to $1.85 ($1.80 midpoint)",
            "reported_q0_actual": "Reported $2.21 adjusted diluted EPS ($1.95 GAAP EPS)",
            "variance_commentary": "Exceeded the high end of prior guidance by $0.36 (+19.5%) on powerful operating leverage and gross margin expansion.",
            "credibility_grade": "BEAT OWN GUIDE"
        },
        {
            "guided_metric": "Q3 2026 Adjusted Operating Margin (%)",
            "prior_quarter_guidance": "22.5% to 23.5% (23.0% midpoint)",
            "reported_q0_actual": "Expanded to 25.2% (+290 bps YoY)",
            "variance_commentary": "Exceeded upper guidance range by 170 bps via operational efficiency, fixed cost absorption, and higher mix of proprietary thermal systems.",
            "credibility_grade": "BEAT OWN GUIDE"
        }
    ],
    "forward_guidance_reset_matrix_b": [
        {
            "forward_horizon_and_metric": "Full-Year 2026 Net Sales Guidance ($M)",
            "preprint_street_consensus": "$13,800M to $14,100M ($13,950M midpoint)",
            "new_management_guidance": "Raised to $14,450M to $14,850M ($14,650M midpoint, +38% organic growth)",
            "delta_vs_street": "+$700M lift vs Street consensus (+5.0% raise)",
            "action_badge": "RAISED",
            "rationale": "Massive backlog expansion, record hyperscale orders, and rapid conversion of direct-to-chip liquid cooling deployments."
        },
        {
            "forward_horizon_and_metric": "Full-Year 2026 Adjusted Diluted EPS ($)",
            "preprint_street_consensus": "$6.60 to $6.80 ($6.70 midpoint)",
            "new_management_guidance": "Raised to $7.10 to $7.20 ($7.15 midpoint, +70% YoY growth)",
            "delta_vs_street": "+$0.45 per share lift at midpoint (+6.7% raise)",
            "action_badge": "RAISED",
            "rationale": "High operating conversion and factory efficiency gains across North America and APAC manufacturing lines."
        },
        {
            "forward_horizon_and_metric": "Q4 2026 Net Sales Guidance ($M)",
            "preprint_street_consensus": "$4,050M to $4,200M ($4,125M midpoint)",
            "new_management_guidance": "Guide set at $4,313M to $4,513M ($4,413M midpoint, 50% organic growth)",
            "delta_vs_street": "+$288M above consensus at midpoint",
            "action_badge": "ABOVE CONSENSUS",
            "rationale": "Uninterrupted shipment ramp for NVIDIA Blackwell GB200/NVL72 data center thermal architecture."
        },
        {
            "forward_horizon_and_metric": "Full-Year 2026 Adjusted Free Cash Flow ($M)",
            "preprint_street_consensus": "$2,450M to $2,550M ($2,500M midpoint)",
            "new_management_guidance": "Raised to $2,600M to $2,800M ($2,700M midpoint, +50% YoY)",
            "delta_vs_street": "+$200M increase at midpoint",
            "action_badge": "RAISED",
            "rationale": "Strong working capital discipline and cash conversion despite accelerated CapEx expansion."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst_name": "Amit Daryanani (Evercore ISI)",
            "topic": "Organic Order Growth >100% and Liquid Cooling Capacity",
            "question": "Giordano, congratulations on organic orders doubling year-over-year. Could you give us more granularity on how much of this order surge is driven by liquid cooling versus traditional power/thermal, and what is your current manufacturing lead time for complete converged modular infrastructure?",
            "executive_response": "CEO Giordano Albertazzi explained that while liquid cooling demand is growing exponentially with high-density AI clusters, traditional air and hybrid power systems also saw immense growth because customers are retrofitting existing facilities. Lead times for standardized modular power solutions have actually compressed by 30% due to capacity additions in North America and Europe, while Vertiv's proprietary CoolTera CDUs and manifold systems are scaling rapidly to meet hyperscaler deployment deadlines."
        },
        {
            "analyst_name": "Mark Delaney (Goldman Sachs)",
            "topic": "After-Hours Digestion (-2.8%) vs. Supply Chain & Margins into 2027",
            "question": "David, the print was exceptional across every single metric, yet the stock is taking a modest breather in the aftermarket (-2.8%). Is there any concern that gross margin at 29.97% or adjusted operating margin at 25.2% is nearing a cyclical peak as more hardware volume ramps, or do you see structural operating leverage continuing into 2027?",
            "executive_response": "CFO David Fallon addressed margin dynamics directly: 'We do not see 25% adjusted operating margin as a ceiling. As our product mix continues to tilt toward integrated high-value liquid-to-air heat exchangers, busways, and converged power pods, software monitoring, and lifecycle spares, our value capture expands. The aftermarket reaction simply reflects a stock that has appreciated tremendously year-to-date digesting a monster quarter.'"
        },
        {
            "analyst_name": "Andrew Obin (Bank of America)",
            "topic": "Hyperscaler CapEx Trajectory & Backlog Visibility",
            "question": "With Microsoft, Alphabet, and Meta all signaling sustained CapEx increases through 2027, how far out does Vertiv's current backlog extend, and are you seeing any signs of double-ordering or capacity hoarding among colocation providers?",
            "executive_response": "Albertazzi stated that Vertiv's order validation process requires firm customer site engineering approvals and financial commitments, preventing speculative phantom backlog. Visibility extends comfortably through the entirety of 2027, with multi-gigawatt pipeline discussions underway for modular installations scheduled for late 2027 and 2028."
        }
    ]
}

with open("post_agent_bus/VRT_2026-10-28_agent2b_transcript.json", "w", encoding="utf-8") as f:
    json.dump(agent2b, f, indent=2)

# -------------------------------------------------------------
# Agent 2C: Social Pulse Agent
# -------------------------------------------------------------
agent2c = {
    "ticker": "VRT",
    "earnings_date": "2026-10-28",
    "agent_role": "Social_Pulse_Agent",
    "model": "gemini-3.8-flash-high",
    "social_channels_crawled": [
        "Reddit r/wallstreetbets & r/options",
        "X/FinTwit #VRT & AI Infrastructure community",
        "Stocktwits Vertiv stream",
        "Institutional Sell-Side Flash Notes (Evercore, Goldman, BofA, Morgan Stanley)"
    ],
    "retail_vs_institutional_reaction": {
        "retail_sentiment_summary": "Retail traders are celebrating the blowout +100% order book and $4.31B revenue print, but expressing slight frustration that the stock dipped -2.8% to $236 after-hours. Common consensus is that the print was an undisputed home run and the modest drop is healthy consolidation after a massive pre-earnings run.",
        "institutional_sentiment_summary": "Institutional desks are uniformly bullish. Sell-side analysts raised price targets across the board, citing Vertiv as the premier pure-play beneficiary of the AI power and thermal bottleneck. The -2.8% AH reaction is viewed as normal straddle digestion (implied was 11.04%), with funds eager to accumulate on any pullback toward the $230-$235 support zone.",
        "after_hours_movement_driver": "Mild profit-taking and 'sell the news' reaction within the ATM options straddle band (-2.82% move vs 11.04% implied move), following a +15% run-up over the preceding two weeks."
    },
    "four_pillar_post_sentiment_scores": {
        "pillar_1_retail_and_social_pulse": {
            "score_out_of_100": 85,
            "classification": "BULLISH ACCUMULATION & DIP-BUYING CONSENSUS",
            "key_themes": [
                "Orders doubled YoY (+100%) confirming AI data center supercycle is real",
                "Vertiv called 'the picks-and-shovels king of AI'",
                "Calls for $300 price target as Blackwell servers deploy in Q4/Q1",
                "Mild frustration over -2.8% AH dip, but widespread intention to add calls"
            ],
            "top_quote": "FinTwit DataCenter Bull: 'VRT grew organic orders OVER 100%, net sales +61% to $4.31B, raised FY26 guide by $650M, and trades down $6 in after-hours? That is a textbook buy-the-dip gift. Blackwell thermal liquid cooling is just getting started.'"
        },
        "pillar_2_sellside_flash_reactions": {
            "score_out_of_100": 94,
            "classification": "UNANIMOUS OUTPERFORM / AGGRESSIVE PT HIKES",
            "key_themes": [
                "Evercore ISI, Goldman Sachs, and BofA reiterate Buy/Overweight",
                "Full-year revenue guidance raise of $650M exceeds Street bull estimates",
                "Americas organic growth of 66% proves Vertiv's dominant market share in liquid cooling",
                "Adjusted operating margins at 25.2% show extraordinary operational execution"
            ],
            "top_quote": "Goldman Sachs Equity Research: 'Vertiv delivered another masterclass in AI infrastructure execution. Organic orders +100% YoY demonstrates that hyperscaler power and cooling constraints are directly translating into Vertiv backlog. We reiterate Conviction Buy and raise our 12-month target to $285.'"
        },
        "pillar_3_management_call_tone": {
            "score_out_of_100": 92,
            "classification": "HIGHLY CONFIDENT, STRATEGIC & OPERATIONAL FOCUS",
            "key_themes": [
                "CEO Giordano Albertazzi emphasizes compressing product cycles from years to months",
                "Global manufacturing capacity additions executing ahead of schedule",
                "Liquidity of $6.2 billion provides fortress balance sheet for R&D and expansion",
                "Order visibility solid through late 2027 with zero double-ordering detected"
            ],
            "top_quote": "CEO Giordano Albertazzi on Call: 'The data center market continues to generate strong, broad-based global demand, validating the depth and duration of this AI buildout cycle. We are compressing development cycles, expanding factory output, and leading the transition to liquid cooling at scale.'"
        },
        "pillar_4_options_iv_crush_and_skew": {
            "score_out_of_100": 88,
            "classification": "VOL CRUSH WITHIN STRADDLE BAND / BULLISH REGIME",
            "key_themes": [
                "Stock moved -2.82% (-$6.84), comfortably contained within the 11.04% ($21.65) straddle band",
                "Massive IV crush rewarding short premium and weekly volatility sellers",
                "Call open interest remains heavily skewed toward $250 and $260 strikes for November"
            ],
            "top_quote": "Floor Derivatives Trader: 'VRT printed a textbook vol crush. The 11.04% straddle implied a \u00c2\u00b1$21.65 move, and the stock traded down just $6.84 to $236.10. Implied volatility will contract hard at open, giving call buyers a great entry on longer-dated contracts.'"
        }
    }
}

with open("post_agent_bus/VRT_2026-10-28_agent2c_social.json", "w", encoding="utf-8") as f:
    json.dump(agent2c, f, indent=2)

print("[SUCCESS] Created all 3 Layer 2 bus files for VRT in post_agent_bus/")
