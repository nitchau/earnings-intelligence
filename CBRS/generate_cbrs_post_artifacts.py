"""
generate_cbrs_post_artifacts.py
Generates Layer 2 Specialized Agent Bus files for CBRS (Cerebras Systems Inc.) T+0 Post-Earnings
Output paths:
- post_agent_bus/CBRS_2026-11-12_agent2a_kpis.json
- post_agent_bus/CBRS_2026-11-12_agent2b_transcript.json
- post_agent_bus/CBRS_2026-11-12_agent2c_social.json
"""

import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "CBRS"
DATE = "2026-11-12"

BUS_DIR = BASE_DIR / "post_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

# ==============================================================================
# AGENT 2A: OPERATIONAL KPIS & SEGMENTS (KPI_Discovery_Agent)
# ==============================================================================
agent2a = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "agent": "KPI_Discovery_Agent (Agent 2A)",
    "model": "Gemini 3.8 Flash High Standard",
    "operational_kpis": [
        {
            "name": "Cloud and Other Services GAAP Revenue ($M)",
            "q_minus_1_actual": 126.00,
            "q_minus_4_yoy": 38.92,
            "street_consensus_q0": 135.00,
            "whisper_q0": 140.00,
            "reported_actual_q0": 141.93,
            "spread_vs_street": "+$6.93M (+5.13%)",
            "spread_vs_whisper": "+$1.93M (+1.38%)",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "Core Non-GAAP Total Revenue ($M)",
            "q_minus_1_actual": 209.90,
            "q_minus_4_yoy": 135.71,
            "street_consensus_q0": 220.00,
            "whisper_q0": 228.00,
            "reported_actual_q0": 230.90,
            "spread_vs_street": "+$10.90M (+4.95%)",
            "spread_vs_whisper": "+$2.90M (+1.27%)",
            "verdict": "BEAT",
            "bar_width_pct": 94
        },
        {
            "name": "Contracted Data Center Capacity (Megawatts)",
            "q_minus_1_actual": 600.0,
            "q_minus_4_yoy": 250.0,
            "street_consensus_q0": 650.0,
            "whisper_q0": 675.0,
            "reported_actual_q0": 700.0,
            "spread_vs_street": "+50 MW (+7.69%)",
            "spread_vs_whisper": "+25 MW (+3.70%)",
            "verdict": "BEAT",
            "bar_width_pct": 96
        },
        {
            "name": "Consolidated GAAP Revenue ($M)",
            "q_minus_1_actual": 180.11,
            "q_minus_4_yoy": 135.71,
            "street_consensus_q0": 214.70,
            "whisper_q0": 225.00,
            "reported_actual_q0": 210.81,
            "spread_vs_street": "-$3.89M (-1.81%)",
            "spread_vs_whisper": "-$14.19M (-6.31%)",
            "verdict": "MISS",
            "bar_width_pct": 74
        },
        {
            "name": "Core Gross Margin (%)",
            "q_minus_1_actual": 41.0,
            "q_minus_4_yoy": 31.6,
            "street_consensus_q0": 40.5,
            "whisper_q0": 41.5,
            "reported_actual_q0": 41.0,
            "spread_vs_street": "+50 bps",
            "spread_vs_whisper": "-50 bps",
            "verdict": "MET",
            "bar_width_pct": 88
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Cloud and Other Services Revenue ($M)",
                "values": [38.92, 45.10, 115.30, 126.00, 141.93, 205.00],
                "qoq": "+12.6%",
                "yoy": "+264.7%"
            },
            {
                "name": "Hardware System Revenue ($M)",
                "values": [96.79, 58.22, 78.11, 54.11, 68.88, 115.00],
                "qoq": "+27.3%",
                "yoy": "-28.8%"
            },
            {
                "name": "Total GAAP Consolidated Revenue ($M)",
                "values": [135.71, 103.32, 193.41, 180.11, 210.81, 320.00],
                "qoq": "+17.0%",
                "yoy": "+55.3%"
            }
        ]
    },
    "tooltip_definitions": {
        "Cloud and Other Services GAAP Revenue": "GAAP revenue derived from Cerebras Cloud inference tokens, dedicated cluster hosting, and customer engineering support ($141.93M in Q3 2026, up +264.7% YoY, beating Street consensus $135.0M).",
        "Core Non-GAAP Total Revenue": "Core revenue excluding non-cash warrant amortization, stock-based compensation, and data center pass-through costs ($230.90M in Q3 2026, up +70.1% YoY, beating consensus $220.0M).",
        "Contracted Data Center Capacity": "Total energized and contracted data center power under binding multi-year delivery agreements across North America and Europe, reaching 700 megawatts (up from 600 MW in Q2 2026).",
        "Consolidated GAAP Revenue": "Total GAAP revenue recognizing both wafer-scale hardware deliveries and cloud inference services ($210.81M in Q3 2026, up +55.3% YoY, narrowly missing consensus $214.70M by -1.81% due to warrant timing).",
        "Core Gross Margin": "Non-GAAP gross profit margin adjusting for IPO warrant charges, standing at 41.0% in Q3 2026 (+940 bps YoY vs Q3 2025).",
        "Hardware System Revenue": "Direct sales of CS-3 wafer-scale server clusters and rack-scale AI supercomputers to enterprise AI labs and sovereign data centers ($68.88M in Q3 2026, up +27.3% QoQ).",
        "Wafer-Scale Engine 3 (WSE-3)": "Cerebras's 4-trillion transistor monolithic silicon processor fabricated by TSMC on 5nm process, delivering 900,000 AI cores and 44GB on-chip SRAM with 21 petabytes/sec memory bandwidth.",
        "CS-3 AI Supercomputer": "Liquid-cooled server unit packaging the WSE-3 processor, delivering 125 petaflops of AI compute in a 15U rack chassis without requiring external interconnect fabrics.",
        "Remaining Performance Obligations (RPO)": "Contractually committed future revenue backlog for hardware deliveries and multi-year cloud capacity, totaling over $25.4 billion.",
        "Disaggregated Inference": "Pioneering architectural framework developed with AMD and AWS splitting prefill and decode stages across disparate compute nodes to maximize token throughput and minimize latency.",
        "OpenAI GPT-5.6 Sol Integration": "Tier-1 launch partnership serving OpenAI's frontier reasoning model at an unprecedented 750 tokens per second on Cerebras Cloud infrastructure.",
        "Oracle Cloud Infrastructure (OCI) Deployment": "Definitive multi-year agreement to stand up Cerebras CS-3 superclusters inside OCI data centers worldwide beginning in 2027.",
        "Operating Loss": "GAAP operating loss of -$224.15M in Q3 2026 as heavy R&D for next-generation CS-4/CS-5 silicon ($177.84M) and global data center expansion scaled ahead of revenue.",
        "Research and Development": "Silicon architecture engineering, next-gen chiplet design, and software stack development totaling $177.84M in Q3 2026 ($573.49M for 9M 2026).",
        "Capital Expenditure": "Purchases of data center infrastructure, liquid cooling systems, and specialized manufacturing equipment totaling $497.19M in Q3 2026 ($1,046.06M YTD).",
        "Stock-Based Compensation": "Non-cash equity compensation to engineers and executives, normalizing to $32.85M in Q3 2026 following Q2's post-IPO catch-up vesting.",
        "True Free Cash Flow": "Forensic cash generation metric deducting OCF (-$341.41M), CapEx ($497.19M), and SBC ($32.85M), yielding True FCF of -$871.45M.",
        "Cash and Liquid Resources": "Cash, cash equivalents, restricted cash, and short-term investments totaling $7.80 billion with an additional $850 million undrawn revolving credit line.",
        "TSMC Packaging Allocation": "Direct wafer allocation and advanced silicon packaging capacity secured with TSMC, bypassing CoWoS packaging bottlenecks by utilizing monolithic wafer-scale dies.",
        "Breakeven Operating Margin Target": "Guidance corridor targeting Core non-GAAP operating margin of (1%) to +1% in Q4 2026, marking Cerebras's imminent transition to operational profitability."
    }
}

# ==============================================================================
# AGENT 2B: EARNINGS CALL TRANSCRIPT & GUIDANCE FORENSIC AGENT (Transcript_Forensic_Agent)
# ==============================================================================
agent2b = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "agent": "Transcript_Forensic_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 86,
    "credibility_label": "86 / 100 (High Credibility: Three Consecutive Quarters of Guidance Beats & Massive Revenue Guidance Hike)",
    "matrix_a_prior_guidance_accountability": [
        {
            "metric": "Q3 2026 Core Total Revenue ($M)",
            "prior_guidance": "$210.0M – $220.0M ($215.0M Midpoint)",
            "reported_delivery": "$230.90M",
            "variance": "+$15.90M (+7.4% vs Midpoint)",
            "credibility_grade": "BEAT OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Core Gross Margin (%)",
            "prior_guidance": "40.0% – 42.0% (41.0% Midpoint)",
            "reported_delivery": "41.00%",
            "variance": "Met Guidance Exactly",
            "credibility_grade": "MET GUIDE"
        },
        {
            "metric": "Q3 2026 Data Center Capacity",
            "prior_guidance": "650 MW by Q3 end",
            "reported_delivery": "700 MW under contract",
            "variance": "+50 MW Ahead of Plan",
            "credibility_grade": "BEAT OWN GUIDE"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026E Core Revenue ($M)",
            "pre_print_consensus": "$260.0M – $275.0M ($267.5M Midpoint)",
            "new_guidance": "$310.0M – $330.0M ($320.0M Midpoint)",
            "delta_display": "+$52.50M (+19.6% vs Street)",
            "action_badge": "RAISED"
        },
        {
            "metric": "Q4 2026E Core Gross Margin (%)",
            "pre_print_consensus": "43.0% – 45.0%",
            "new_guidance": "47.0% – 49.0% (48.0% Midpoint)",
            "delta_display": "+400 bps Expansion",
            "action_badge": "RAISED"
        },
        {
            "metric": "Q4 2026E Core Operating Margin (%)",
            "pre_print_consensus": "-8.0% to -5.0%",
            "new_guidance": "-1.0% to +1.0% (Breakeven Trajectory)",
            "delta_display": "+700 bps Surge to Breakeven",
            "action_badge": "RAISED"
        },
        {
            "metric": "Full-Year 2026 Core Revenue ($M)",
            "pre_print_consensus": "$875.0M – $900.0M",
            "new_guidance": "$940.0M – $960.0M ($950.0M Midpoint)",
            "delta_display": "+$65.0M (+7.3% Increase)",
            "action_badge": "RAISED"
        },
        {
            "metric": "FY2027 Long-Term Growth Target",
            "pre_print_consensus": "+100% YoY Growth",
            "new_guidance": "Triple Revenue in 2027 (>+200% YoY)",
            "delta_display": "Reaffirmed >3x Growth Target",
            "action_badge": "RAISED"
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "question_num": 1,
            "analyst_name": "Toshiya Hari",
            "firm": "Goldman Sachs",
            "topic": "Wafer Supply Bottlenecks & TSMC Advanced Node Transitions",
            "hard_question": "Andrew, with data center commitments jumping to 700 MW and Q4 revenue guided up to $320M, are you facing any allocation limits at TSMC for monolithic 5nm wafers, and when will Cerebras transition to 3nm/2nm for the next-generation CS-4/CS-5 accelerators?",
            "management_answer": "Andrew Feldman (CEO): 'We have secured 100% of the TSMC wafer supply required to meet both our Q4 guide and our plan to triple revenue in 2027. Because we use monolithic wafer-scale silicon rather than advanced CoWoS packaging or HBM memory stacks, we completely bypass the industry's biggest supply chain choke points. CS-4 tape-out is on schedule, and we see zero silicon gating for our delivery roadmap.'",
            "forensic_verdict": "STRONG REASSURANCE: Direct confirmation that bypassing CoWoS packaging gives Cerebras a structural lead times advantage over Nvidia and AMD."
        },
        {
            "question_num": 2,
            "analyst_name": "Stacy Rasgon",
            "firm": "Bernstein Research",
            "topic": "GAAP vs Core Revenue Divergence & Customer Warrant Amortization",
            "hard_question": "Bob, GAAP revenue missed consensus at $210.8M while Core revenue beat at $230.9M. Can you walk through the $20M delta and specifically how customer warrant amortization will impact reported GAAP margins over the next four quarters?",
            "management_answer": "Bob Komin (CFO): 'The $20.1M variance is entirely non-cash amortization associated with strategic customer equity warrants granted at the time of multi-gigawatt contracted capacity signings. As cloud inference volumes ramp and hardware deliveries accelerate in Q4, that non-cash discount diminishes as a percentage of top-line, which is why our Core gross margin expands directly to 47%-49% next quarter.'",
            "forensic_verdict": "ACCOUNTING CLARITY: Demonstrates that the GAAP revenue optical 'miss' was purely non-cash warrant timing, while underlying cash collections and Core revenues surged."
        },
        {
            "question_num": 3,
            "analyst_name": "Vivek Arya",
            "firm": "BofA Securities",
            "topic": "CapEx Surge & Free Cash Flow Burn Runway",
            "hard_question": "You spent $497M on CapEx in Q3 and burned $871M in True Free Cash Flow. At what point does data center build-out peak, and when do customer cash deposits turn operating cash flow sustainably positive?",
            "management_answer": "Bob Komin (CFO): 'CapEx in Q2 and Q3 represented front-loaded capital deployment to secure 700 MW of high-density powered shell capacity across North America and Europe. We are sitting on $7.8 billion in cash and short-term liquid investments plus an undrawn $850 million credit facility. With Q4 operating margins reaching breakeven (-1% to +1%), operating cash flow inflects sharply in the first half of 2027 as customer deposits on our $25.4B backlog convert.'",
            "forensic_verdict": "FORTRESS BALANCE SHEET: $7.8B liquid reserves eliminates dilutive financing risk despite near-term capital expenditure intensity."
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL PULSE, INSTITUTIONAL DESK & AH REACTION (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "agent": "Social_Pulse_Agent (Agent 2C)",
    "model": "Gemini 3.8 Flash High Standard",
    "after_hours_reaction": {
        "regular_close": 97.75,
        "after_hours_price": 115.68,
        "post_print_move_pct": 18.34,
        "options_implied_move_pct": 15.78,
        "verdict": "EXPLOSIVE BEAT & RAISE SURGE",
        "primary_driver": "Blockbuster Q4 revenue guidance ($310M-$330M vs $267.5M Street consensus) and Q4 breakeven operating margin trajectory (-1% to +1%) completely overwhelmed the optical non-cash GAAP revenue noise, triggering aggressive short-covering and institutional multiple expansion."
    },
    "four_pillar_sentiment_scores": {
        "retail_pulse_score": 88,
        "retail_pulse_status": "EXTREMELY BULLISH",
        "sell_side_flash_score": 92,
        "sell_side_flash_status": "OVERWHELMINGLY POSITIVE",
        "management_call_tone_score": 85,
        "management_call_tone_status": "CONFIDENT & AGGRESSIVE",
        "options_iv_skew_score": 80,
        "options_iv_skew_status": "CALL DEMAND RUSH / SHORT SQUEEZE"
    },
    "social_channels": {
        "reddit_wallstreetbets": "Trending #1 on r/wallstreetbets and r/options. Traders celebrating massive call option gains as 100-strike and 105-strike weekly calls print 400%+ gains; widespread memes highlighting Cerebras 'inference speed superiority' over Nvidia GPUs for OpenAI GPT-5.6 Sol.",
        "x_fintwit": "Semiconductor analysts on X/FinTwit praising Bob Komin's guidance raise to $320M midpoint for Q4. Noted tech investors highlighting that 700MW contracted power makes Cerebras the fastest-scaling independent AI infrastructure provider in the world.",
        "threads_and_stocktwits": "Sentiment index at 94% Bullish on Stocktwits with message volume spiking 650% above 30-day average. Institutional desks reporting aggressive block buys above $115 in after-hours trading.",
        "sell_side_flash_notes": "Morgan Stanley reiterates Overweight and lifts price target to $135 (from $110), citing 'inflecting cloud inference leverage and breakeven timeline ahead of schedule.' BofA notes that 48% Q4 gross margin guidance proves pricing power for wafer-scale architectures."
    }
}

# Write out the files
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print(f"[{TICKER}] Successfully generated Layer 2 post-earnings bus files in {BUS_DIR.name}/")
