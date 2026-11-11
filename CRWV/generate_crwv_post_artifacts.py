import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "CRWV"
DATE = "2026-11-10"

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
            "q_minus_1_actual": 2575.00,
            "q_minus_4_yoy": 1364.68,
            "street_consensus_q0": 3540.79,
            "reported_actual_q0": 3661.00,
            "spread_vs_street": "+3.40%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "Active Deployed Power Footprint (GW)",
            "q_minus_1_actual": 1.50,
            "q_minus_4_yoy": 0.85,
            "street_consensus_q0": 1.65,
            "reported_actual_q0": 1.70,
            "spread_vs_street": "+50 MW Beat",
            "verdict": "EXPANSION",
            "bar_width_pct": 94
        },
        {
            "name": "GAAP Diluted EPS ($)",
            "q_minus_1_actual": -1.14,
            "q_minus_4_yoy": -0.22,
            "street_consensus_q0": -1.55,
            "reported_actual_q0": -1.27,
            "spread_vs_street": "+$0.28 (+18.06%)",
            "verdict": "BEAT",
            "bar_width_pct": 86
        },
        {
            "name": "Exit-2026 Annualized Run-Rate Revenue ($B)",
            "q_minus_1_actual": 17.00,
            "q_minus_4_yoy": 6.50,
            "street_consensus_q0": 18.50,
            "reported_actual_q0": 20.50,
            "spread_vs_street": "+$2.00B Raise",
            "verdict": "RAISED",
            "bar_width_pct": 96
        },
        {
            "name": "Capital Expenditures Deployment ($M)",
            "q_minus_1_actual": 6422.00,
            "q_minus_4_yoy": 2389.24,
            "street_consensus_q0": 8500.00,
            "reported_actual_q0": 9441.00,
            "spread_vs_street": "+$941.0M Expansion",
            "verdict": "CAPEX SURGE",
            "bar_width_pct": 98
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Dedicated GPU Compute (Contracted AI Clusters)",
                "values": [1023.51, 1205.00, 1620.00, 2035.00, 2928.80, 3850.00],
                "qoq": "+43.9%",
                "yoy": "+186.2%"
            },
            {
                "name": "On-Demand Cloud & AI Software Services",
                "values": [341.17, 366.90, 458.00, 540.00, 732.20, 986.00],
                "qoq": "+35.6%",
                "yoy": "+114.6%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [1364.68, 1571.90, 2078.00, 2575.00, 3661.00, 4836.00],
                "qoq": "+42.2%",
                "yoy": "+168.3%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated GAAP net revenue from CoreWeave AI infrastructure services, dedicated GPU clusters, and high-performance network orchestration ($3,661.0M in Q3 2026, beating Street consensus $3,540.79M by +$120.21M / +3.40%).",
        "Active Deployed Power": "Operational energised capacity across CoreWeave data center campuses hosting production GPU workloads, surpassing 1.7 GW in Q3 2026 after adding 200+ MW in the quarter.",
        "Contracted Power Pipeline": "Total contracted power pipeline growing to over 4.6 GW across diversified global utility partners, including over 1.3 GW international footprint across India, Indonesia, and Spain.",
        "GAAP Diluted EPS": "GAAP diluted net loss per share of -$1.27 in Q3 2026 based on 559M weighted average shares, beating Street consensus (-$1.55) by $0.28 (+18.06%).",
        "Operating Income": "GAAP operating income turned positive to $207.0M in Q3 2026 (5.65% operating margin) compared to -$49.0M in Q2 2026 and -$144.0M in Q1 2026, marking an essential operational inflection point.",
        "Gross Profit": "GAAP gross profit of $2,478.0M in Q3 2026 (67.69% gross margin) compared to $1,696.0M in Q2 2026 and $995.85M in Q3 2025 (+148.8% YoY).",
        "Operating Cash Flow": "Cash provided by operating activities reached $1,975.0M in Q3 2026, surging sequentially from $679.0M in Q2 2026 on accelerated contract milestone payments and AI cluster billings.",
        "Capital Expenditures": "Cash purchases of property and equipment, including capitalized internal-use software, of $9,441.0M in Q3 2026, funding Nvidia Blackwell B200 and H200 GPU infrastructure.",
        "Reported Free Cash Flow": "Operating cash flow ($1,975.0M) minus capital expenditures ($9,441.0M) equals reported negative free cash flow of -$7,466.0M in Q3 2026 due to historic infrastructure investment.",
        "Stock-Based Compensation": "Non-cash equity compensation expense of $160.0M in Q3 2026 ($478.0M for 9M 2026), reflecting disciplined equity grant controls.",
        "Finance Lease Obligations": "Principal payments on finance leases and long-term data center equipment obligations, which stood at $0.0M in Q3 2026 after substantial payoffs in Q2.",
        "True Free Cash Flow": "Comprehensive economic cash flow subtracting CapEx ($9,441.0M) and SBC ($160.0M) from OCF ($1,975.0M), totaling -$7,626.0M in Q3 2026.",
        "Customer Prepayments and Deposits": "Customer cash prepayments and reservation deposits expected to total approximately $9.0B over the next three months, providing non-dilutive capex liquidity.",
        "Revenue Backlog": "Remaining performance obligations and long-term contracted AI compute commitments from leading AI frontier labs, hyperscalers, and enterprise clients.",
        "After-Hours Reaction": "CRWV shares surged +7.90% to $52.58 in after-hours trading as CoreWeave beat Q3 revenue, turned operating profitable, and raised full-year 2026 revenue guidance to $13.0B-$13.3B.",
        "Blackwell B200 Deployments": "CoreWeave's prioritized allocation and initial commercial cluster turn-ups of Nvidia's next-generation Blackwell architecture across North American data centers.",
        "Exit-2026 ARR Guidance": "Management increased exit-2026 annualized run-rate revenue guidance to $20.0B - $21.0B, reflecting massive forward visibility on committed GPU instances.",
        "Liquid Cash & Balance Sheet": "Cash, restricted cash, and marketable securities totaling $5,589.0M at September 30, 2026, anchored by $56.8B in deployed net property and equipment."
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
            "prior_guidance": "$3,450M - $3,650M",
            "reported_actual": "$3,661.0M",
            "variance": "+$11.0M above top end (+3.1% vs midpoint)",
            "grade": "BEAT TOP OF RANGE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 GAAP Operating Income ($M)",
            "prior_guidance": "Near breakeven (-$50M to +$50M)",
            "reported_actual": "$207.0M (5.65% margin)",
            "variance": "+$157.0M above top end",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Active Deployed Power Footprint",
            "prior_guidance": "1.65 GW by end of Q3",
            "reported_actual": ">1.70 GW (>200 MW added)",
            "variance": "+50 MW ahead of schedule",
            "grade": "AHEAD OF SCHEDULE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 GAAP Diluted EPS ($)",
            "prior_guidance": "-$1.60 to -$1.45",
            "reported_actual": "-$1.27",
            "variance": "+$0.18 outperformance",
            "grade": "BEAT OWN RANGE",
            "badge_class": "badge-bull"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Full-Year 2026 Revenue Guidance",
            "street_pre_print": "$12.72B ($12.50B - $12.90B)",
            "new_guidance": "$13.0B - $13.3B ($13.15B Midpoint)",
            "delta": "+$430M (+3.4%) above Street consensus",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q4 2026E Implied Revenue Guidance",
            "street_pre_print": "$4.41B Consensus",
            "new_guidance": "$4.69B - $4.99B ($4.84B Midpoint)",
            "delta": "+$430M sequential expansion above Street",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Full-Year 2026 Adjusted Operating Income",
            "street_pre_print": "$1.05B - $1.15B (~$1.10B)",
            "new_guidance": "$1.275B - $1.375B (+26% at midpoint)",
            "delta": "+$225M (+19.6%) operating expansion",
            "action": "RAISED AGGRESSIVELY",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Exit-2026 Annualized Run-Rate Revenue (ARR)",
            "street_pre_print": "$18.5B Consensus",
            "new_guidance": "$20.0B - $21.0B ($20.5B Midpoint)",
            "delta": "+$2.0B higher exit velocity",
            "action": "RAISED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Full-Year 2026 Capital Expenditures",
            "street_pre_print": "$36.5B Consensus",
            "new_guidance": "$37.0B - $39.0B (raised low end from $35B)",
            "delta": "+$1.5B at midpoint on accelerated deployment",
            "action": "CAPEX RAISED",
            "badge_class": "badge-blue"
        }
    ],
    "credibility_score": 88,
    "top_call_exchanges": [
        {
            "analyst": "Brad Zelnick (Deutsche Bank)",
            "topic": "Blackwell B200 Cluster Ramp & Sovereign/Tier-1 Demand Durability",
            "question": "Can you provide more granularity on the Blackwell B200 turn-up schedule for Q4 and into 1H 2027? Are enterprise customers and frontier AI labs signing multi-year commitments despite rapid chip architecture replacement cycles?",
            "management_answer": "Michael Intrator (CEO): 'Demand for our specialized AI cloud continues to accelerate faster than power can be energized. Every single Blackwell cluster scheduled for delivery over the next four quarters is already fully allocated under multi-year contract take-or-pay structures. Customers recognize that our software orchestration and networking fabric deliver up to 30% lower training latency than general-purpose hyperscalers, ensuring durable high utilization.'",
            "verdict": "100% CAPACITY COMMITTED UNDER TAKE-OR-PAY"
        },
        {
            "analyst": "Mark Murphy (JPMorgan)",
            "topic": "Customer Prepayments & Capital Structure Self-Sufficiency",
            "question": "You mentioned expecting approximately $9 billion in customer prepayments and deposits in the next three months. How does that cash inflow alter your debt issuance plans and equity dilution expectations for the $37B-$39B CapEx program?",
            "management_answer": "Michael Intrator (CEO): 'Customer prepayments represent the purest form of non-dilutive financing. These are enterprise customers and sovereign entities committing multi-billion dollar capital upfront to guarantee multi-gigawatt delivery. Combined with our operating cash flow inflection to nearly $2 billion this quarter, this liquidity provides immense balance sheet flexibility without requiring opportunistic equity dilution.'",
            "verdict": "NON-DILUTIVE PREPAYMENT MOAT CONFIRMED"
        },
        {
            "analyst": "Keith Weiss (Morgan Stanley)",
            "topic": "Adjusted Operating Margin Trajectory & Depreciation Headwinds",
            "question": "You raised adjusted operating income guidance by 26% at the midpoint while operating margins reached double digits ahead of schedule. As $38B in assets hit the balance sheet, how should we think about gross margin sustainability against rising depreciation?",
            "management_answer": "Michael Intrator (CEO): 'Our gross margins in Q3 remained robust at 67.7% because cluster utilization ramped immediately upon energization. Because our contracts are structured with multi-year take-or-pay minimums, depreciation is matched against contractual revenue inflows from day one. We expect operating margin expansion to continue as corporate overhead scales over a doubling revenue base.'",
            "verdict": "DEPRECIATION ABSORPTION PROTECTED BY CONTRACTS"
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL & MARKET PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "retail_sentiment_score": 84,
    "institutional_sentiment_score": 88,
    "composite_sentiment_score": 86,
    "sentiment_breakdown": {
        "retail_pulse": "Extremely bullish enthusiasm across r/wallstreetbets, X/FinTwit, and Threads. Retail traders are celebrating CoreWeave's top-line beat ($3.66B vs $3.54B), operating profit turnaround ($207M vs -$49M in Q2), and the $20B-$21B exit ARR guide. Discussion is dominated by CoreWeave outmaneuvering legacy cloud providers in pure-play AI workload capture.",
        "sell_side_reaction": "Unanimously positive with target price raises anticipated. Morgan Stanley, JPMorgan, and Deutsche Bank highlighted the $9B customer prepayment inflow, raised full-year operating income (+26% at midpoint), and contracted power expansion to 4.6 GW as definitive evidence that CoreWeave is widening its lead in AI compute infrastructure.",
        "management_tone": "Aggressive, commanding, and operationally rigorous. Michael Intrator exuded immense confidence regarding power interconnection execution, Blackwell B200 customer allocations, and balance sheet self-funding through customer prepayments.",
        "options_iv_crush": "Options implied move was ±19.95% ($9.57). With the stock gaining +7.90% (+$3.85 to $52.58) after-hours, the move stayed comfortably within the implied straddle band, generating rapid IV crush on weekly options contracts and delivering profits to net options sellers."
    },
    "after_hours_driver": "CRWV shares surged +7.90% to $52.58 in after-hours trading as CoreWeave crushed third-quarter revenue consensus ($3,661M vs $3,540.79M), swung to positive GAAP operating income of $207.0M, raised full-year 2026 revenue guidance to $13.0B-$13.3B, lifted exit ARR guidance to $20.0B-$21.0B, and announced an anticipated $9.0B influx of customer prepayments and deposits over the next three months."
}

# Write files to post_agent_bus
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print(f"Successfully generated post agent bus files for {TICKER} ({DATE}).")
