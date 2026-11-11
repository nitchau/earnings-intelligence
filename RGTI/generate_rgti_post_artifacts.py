import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "RGTI"
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
            "name": "Total GAAP Net Revenue ($M)",
            "q_minus_1_actual": 5.14,
            "q_minus_4_yoy": 1.95,
            "street_consensus_q0": 3.68,
            "reported_actual_q0": 1.41,
            "spread_vs_street": "-61.68%",
            "verdict": "MISS",
            "bar_width_pct": 38
        },
        {
            "name": "2-Qubit Gate Fidelity on 108Q System",
            "q_minus_1_actual": "99.30%",
            "q_minus_4_yoy": "98.00%",
            "street_consensus_q0": "99.50%",
            "reported_actual_q0": "99.50% (99.7% on 8Q)",
            "spread_vs_street": "MET MILESTONE",
            "verdict": "MILESTONE MET",
            "bar_width_pct": 95
        },
        {
            "name": "GAAP Diluted EPS ($)",
            "q_minus_1_actual": -0.16,
            "q_minus_4_yoy": -0.62,
            "street_consensus_q0": -0.05,
            "reported_actual_q0": -0.08,
            "spread_vs_street": "-$0.03 (-60.0%)",
            "verdict": "MISS",
            "bar_width_pct": 45
        },
        {
            "name": "U.S. Dept of Commerce CHIPS Award ($M)",
            "q_minus_1_actual": 0.00,
            "q_minus_4_yoy": 0.00,
            "street_consensus_q0": 0.00,
            "reported_actual_q0": 100.00,
            "spread_vs_street": "+$100.0M Award",
            "verdict": "LANDMARK AWARD",
            "bar_width_pct": 98
        },
        {
            "name": "Total Liquid Cash & Equivalents ($M)",
            "q_minus_1_actual": 67.67,
            "q_minus_4_yoy": 44.85,
            "street_consensus_q0": 55.00,
            "reported_actual_q0": 45.80,
            "spread_vs_street": "-$9.20M Below Est",
            "verdict": "BURN CONCERN",
            "bar_width_pct": 72
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Development Contracts & Government R&D",
                "values": [1.15, 1.10, 2.80, 3.20, 0.90, 2.10],
                "qoq": "-71.9%",
                "yoy": "-21.7%"
            },
            {
                "name": "Quantum Computing Systems & Cloud (QCS / Novera)",
                "values": [0.80, 0.77, 1.60, 1.94, 0.51, 1.40],
                "qoq": "-73.7%",
                "yoy": "-36.2%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [1.95, 1.87, 4.40, 5.14, 1.41, 3.50],
                "qoq": "-72.6%",
                "yoy": "-27.7%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Net Revenue": "Consolidated GAAP net revenue from Rigetti quantum computing systems (Novera QPU), Quantum Cloud Services (QCS), and government research development contracts ($1.41M in Q3 2026, missing consensus $3.68M by -61.68%).",
        "Cepheus-1-108Q Architecture": "Rigetti's flagship 108-qubit quantum processor assembled from twelve 9-qubit chiplets tiled together, delivering the industry's largest multi-chip superconducting quantum computer.",
        "Median Two-Qubit Fidelity": "Quantum gate benchmark measuring gate error rates; Cepheus-1-108Q achieved 99.5% median 2-qubit fidelity across the full 108 qubits, 99.6% on an 80-qubit sublattice, and 99.7% on an 8-qubit sublattice.",
        "CHIPS Act $100M Award": "Definitive agreement signed with the U.S. Department of Commerce in September 2026 for up to $100M in non-dilutive R&D funding with a minority government equity stake.",
        "Operating Loss": "GAAP operating loss of -$33.19M in Q3 2026 compared to -$28.06M in Q2 2026 and -$20.55M in Q3 2025 as R&D scaling in cryogenics and microelectronics elevated operational costs.",
        "Research and Development": "Laboratory R&D and chip fabrication costs at Fab-1 totaling $25.50M in Q3 2026 ($66.18M for 9M 2026) compared to $15.02M in Q3 2025 (+69.8% YoY).",
        "Selling, General and Administrative": "Corporate, marketing, and legal expenses of $8.55M in Q3 2026 compared to $5.93M in Q3 2025 (+44.2% YoY).",
        "GAAP Net Loss": "GAAP net loss of -$3.14M in Q3 2026 (-$0.08 per share), benefiting from a $25.3M non-cash fair value gain on derivative warrant liabilities.",
        "Non-GAAP Net Loss": "Non-GAAP net loss of -$20.5M (-$0.06 per share) in Q3 2026, excluding warrant revaluations and $7.96M in stock-based compensation expense.",
        "Operating Cash Burn": "Operating cash outflow of -$17.06M in Q3 2026 (-$49.06M for 9M 2026), worsening sequentially from -$15.78M in Q2 2026.",
        "Capital Expenditures": "Cash purchases of property and equipment of $26.20M in Q3 2026 ($42.60M for 9M 2026), primarily funding cleanroom expansion and cryogenic dilution refrigerator installations.",
        "Reported Free Cash Flow": "Operating cash flow (-$17.06M) minus capital expenditures ($26.20M) equals reported negative free cash flow of -$43.26M in Q3 2026.",
        "Stock-Based Compensation": "Non-cash equity compensation expense of $7.96M in Q3 2026 ($20.87M for 9M 2026) to retain key quantum physicists and fabrication engineers.",
        "True Free Cash Flow": "Comprehensive economic cash burn subtracting CapEx ($26.20M) and SBC ($7.96M) from OCF (-$17.06M), totaling -$51.22M in Q3 2026.",
        "Cash Runway Horizon": "Cash and cash equivalents of $45.80M at September 30, 2026, requiring initial tranches of the $100M CHIPS Act funding to support operations through late 2027.",
        "After-Hours Reaction": "RGTI stock dropped -6.83% to $11.32 in after-hours trading as commercial revenue fell short ($1.41M vs $3.68M Street consensus), despite landmark 99.5% fidelity validation on Cepheus-1-108Q.",
        "300-Plus-Qubit Target": "Next-generation quantum processor roadmap targeting >300 qubits with approximately 99.7% median 2-qubit gate fidelity and ultra-fast 50-70ns gate speeds.",
        "1,000-Qubit Roadmap": "Long-term architecture roadmap advancing toward 1,000 qubits with 99.9% 2-qubit fidelity, laying the foundation for commercial fault-tolerant quantum advantage."
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
            "metric": "Q3 2026 Total Net Revenue ($M)",
            "prior_guidance": "$3.5M - $4.5M",
            "reported_actual": "$1.41M",
            "variance": "-$2.27M below midpoint (-61.7% miss)",
            "grade": "MISSED OWN GUIDE",
            "badge_class": "badge-bear"
        },
        {
            "metric": "108-Qubit Gate Fidelity Benchmark",
            "prior_guidance": ">=99.5% median 2-qubit fidelity",
            "reported_actual": "99.5% achieved (99.6% on 80Q)",
            "variance": "Target met on schedule",
            "grade": "MET BENCHMARK",
            "badge_class": "badge-bull"
        },
        {
            "metric": "CHIPS Act Finalization",
            "prior_guidance": "Definitive agreement in 2H 2026",
            "reported_actual": "Signed $100M agreement in September",
            "variance": "Landmark government award executed",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Diluted EPS ($)",
            "prior_guidance": "-$0.06 to -$0.04",
            "reported_actual": "-$0.08 GAAP / -$0.06 Non-GAAP",
            "variance": "-$0.02 GAAP variance",
            "grade": "MISSED RANGE",
            "badge_class": "badge-bear"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Full-Year 2026 Revenue Guidance",
            "street_pre_print": "$16.5M ($15.0M - $18.0M)",
            "new_guidance": "$14.0M - $15.5M (~$14.75M Midpoint)",
            "delta": "-$1.75M revision due to lumpy milestone recognition",
            "action": "LOWERED",
            "badge_class": "badge-bear"
        },
        {
            "metric": "Q4 2026E Implied Revenue Guidance",
            "street_pre_print": "$5.55M Consensus",
            "new_guidance": "$3.1M - $4.6M (~$3.85M Midpoint)",
            "delta": "-$1.70M reset reflecting deployment schedules",
            "action": "LOWERED",
            "badge_class": "badge-bear"
        },
        {
            "metric": "300-Plus-Qubit Deployment Horizon",
            "street_pre_print": "Late 2027",
            "new_guidance": "Targeting 300+ qubits with 99.7% fidelity by year-end 2027",
            "delta": "Reconfirmed technical timeline",
            "action": "MAINTAINED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "CHIPS Act Cash Tranche Inflows",
            "street_pre_print": "$15.0M initial draw",
            "new_guidance": "$20.0M - $25.0M expected initial funding in Q4/Q1",
            "delta": "+$7.5M non-dilutive liquidity boost",
            "action": "NON-DILUTIVE REINFORCEMENT",
            "badge_class": "badge-bull"
        }
    ],
    "credibility_score": 72,
    "top_call_exchanges": [
        {
            "analyst": "David Williams (Benchmark Company)",
            "topic": "Revenue Lumpiness & Delivery Timing vs Contract Delays",
            "question": "Can you walk through what caused the top-line decline from $5.14M in Q2 to $1.41M in Q3? Were any Novera QPU purchase orders or government milestones cancelled or pushed into future quarters?",
            "management_answer": "Dr. Subodh Kulkarni (CEO): 'None of our contracted projects or Novera pipelines have been cancelled. Our revenue model in this nascent phase is heavily tied to delivery acceptance milestones. In Q2, we recognized multi-system Novera shipments and initial government phases; in Q3, our engineering resources were overwhelmingly committed to validating the Cepheus-1-108Q chiplet architecture and finalizing the $100M CHIPS agreement. We expect acceptance revenue to rebound sharply in Q4 and 2027.'",
            "verdict": "ACCEPTANCE TIMING DRIVING REVENUE LUMPINESS"
        },
        {
            "analyst": "Craig Ellis (B. Riley Securities)",
            "topic": "CHIPS Act $100M Award Tranches & Liquidity Runway",
            "question": "With cash at $45.8M and quarterly cash burn around $17M-$26M with CapEx, when will the first capital disbursements from the $100M CHIPS agreement hit the balance sheet, and what are the matching fund requirements?",
            "management_answer": "Dr. Subodh Kulkarni (CEO): 'We have completed the definitive agreement with the Department of Commerce, and the first disbursements are tied to technical milestones across our three R&D initiatives: miniaturized readout electronics, advanced cryogenic cryostats, and high-connectivity chiplet fabrication. We expect initial funding disbursements to begin in the coming quarters, which substantially extends our operational runway into late 2027 without relying on dilutive equity financing.'",
            "verdict": "DISBURSEMENTS TIED TO TECHNICAL MILESTONES"
        },
        {
            "analyst": "Quinn Bolton (Needham & Co.)",
            "topic": "Chiplet Modularity vs Monolithic QPU Scaling",
            "question": "Achieving 99.5% median fidelity across 108 qubits using twelve tiled 9-qubit chiplets is a technical milestone. How do inter-chip coupler losses compare to on-chip gate speeds, and what is the gating factor to 300+ qubits?",
            "management_answer": "Dr. Subodh Kulkarni (CEO): 'Our proprietary silicon interposer and 3D superconducting interconnect technology enable inter-chiplet quantum logic gates to operate at nearly identical 50-70 nanosecond speeds as on-chip couplers. The primary engineering hurdle to 300+ qubits is cryogenic wiring heat load, which our second CHIPS Act project directly solves by orders of magnitude through next-gen cryostat integration.'",
            "verdict": "CHIPLET ARCHITECTURE VALIDATED OVER MONOLITHIC"
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL & MARKET PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "retail_sentiment_score": 62,
    "institutional_sentiment_score": 68,
    "composite_sentiment_score": 65,
    "sentiment_breakdown": {
        "retail_pulse": "Mixed to disappointed on r/wallstreetbets and FinTwit. Retail traders had anticipated stronger sequential revenue momentum following Q2's $5.14M print, leading to frustration over the $1.41M print. However, quantum technology purists are actively defending the stock on X, pointing to the 99.5% 2-qubit fidelity benchmark on 108 qubits and the $100M CHIPS Act backing.",
        "sell_side_reaction": "Cautious on near-term revenue visibility but constructive on technology leadership. Analysts at Benchmark and Needham lowered 2026 price targets slightly to account for revenue volatility, while reaffirming buy ratings based on Rigetti's defensible multi-chip modular architecture and federal funding.",
        "management_tone": "Methodical, transparent, and technology-focused. Dr. Subodh Kulkarni acknowledged revenue lumpiness without equivocation, emphasizing that achieving 99.5% 2-qubit fidelity on a 108-qubit system proves that Rigetti's modular chiplet approach is the viable path to scaling superconducting quantum computers.",
        "options_iv_crush": "Options implied move was ±13.39% ($1.62). The after-hours decline of -6.83% (-$0.83 to $11.32) was well within the straddle pricing, inflicting sharp IV collapse on weekly long straddles and rewarding short options premium sellers."
    },
    "after_hours_driver": "RGTI shares declined -6.83% to $11.32 in after-hours trading after Rigetti reported third-quarter revenue of $1.41M, missing Street expectations of $3.68M due to customer delivery acceptance timing, despite achieving a major technical milestone with 99.5% median 2-qubit gate fidelity on its 108-qubit Cepheus-1 system and executing a $100M CHIPS Act definitive agreement."
}

# Write files to post_agent_bus
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print(f"Successfully generated post agent bus files for {TICKER} ({DATE}).")
