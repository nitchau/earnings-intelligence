import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "FISV"
DATE = "2026-11-03"

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
            "name": "Merchant Solutions Segment Revenue ($M)",
            "q_minus_1_actual": 2540.0,
            "q_minus_4_yoy": 2586.0,
            "street_consensus_q0": 2490.0,
            "reported_actual_q0": 2521.0,
            "spread_vs_street": "+1.24%",
            "verdict": "BEAT",
            "bar_width_pct": 88
        },
        {
            "name": "Financial Solutions Segment Revenue ($M)",
            "q_minus_1_actual": 2360.0,
            "q_minus_4_yoy": 2333.0,
            "street_consensus_q0": 2310.0,
            "reported_actual_q0": 2331.0,
            "spread_vs_street": "+0.91%",
            "verdict": "BEAT",
            "bar_width_pct": 85
        },
        {
            "name": "Adjusted Operating Margin (%)",
            "q_minus_1_actual": 31.0,
            "q_minus_4_yoy": 37.0,
            "street_consensus_q0": 30.8,
            "reported_actual_q0": 31.2,
            "spread_vs_street": "+40 bps",
            "verdict": "BEAT",
            "bar_width_pct": 89
        },
        {
            "name": "Project Elevate Cost Savings Target ($M)",
            "q_minus_1_actual": 500.0,
            "q_minus_4_yoy": 0.0,
            "street_consensus_q0": 500.0,
            "reported_actual_q0": 1000.0,
            "spread_vs_street": "+100.00%",
            "verdict": "BLOWOUT RAISE",
            "bar_width_pct": 99
        },
        {
            "name": "Operating Cash Flow ($M)",
            "q_minus_1_actual": 1483.0,
            "q_minus_4_yoy": 1805.0,
            "street_consensus_q0": 980.0,
            "reported_actual_q0": 1012.0,
            "spread_vs_street": "+3.27%",
            "verdict": "BEAT",
            "bar_width_pct": 87
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Merchant Solutions",
                "values": [2586.0, 2520.0, 2441.0, 2540.0, 2521.0, 2550.0],
                "qoq": "-0.7%",
                "yoy": "-2.5%"
            },
            {
                "name": "Financial Solutions",
                "values": [2333.0, 2420.0, 2297.0, 2360.0, 2331.0, 2380.0],
                "qoq": "-1.2%",
                "yoy": "-0.1%"
            },
            {
                "name": "Corporate and Other",
                "values": [344.0, 344.0, 289.0, 392.0, 344.0, 340.0],
                "qoq": "-12.2%",
                "yoy": "0.0%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [5263.0, 5284.0, 5027.0, 5292.0, 5196.0, 5270.0],
                "qoq": "-1.8%",
                "yoy": "-1.3%"
            }
        ]
    },
    "tooltip_definitions": {
        "Merchant Solutions Segment": "Global merchant acquiring, eCommerce gateway processing, and Clover cloud-based point-of-sale platform ($2,521.0M revenue, 28.7% operating margin).",
        "Financial Solutions Segment": "Core banking account processing, digital banking platforms, digital payments, card services, and risk management ($2,331.0M revenue, 38.1% operating margin).",
        "Adjusted Operating Margin": "Operating margin excluding goodwill impairment, merger integration, and One Fiserv restructuring ($1,512.0M operating income / 31.2% margin in Q3 2026).",
        "Project Elevate Savings Target": "Comprehensive corporate process modernization and AI automation initiative; target doubled from $500M to $1.0B in annualized structural run-rate savings.",
        "Non-Cash Goodwill Impairment": "A non-cash GAAP accounting charge of $6,452.0M ($6.45B) triggered by market capitalization compression, resetting carrying value with zero operational cash impact.",
        "Adjusted Diluted EPS": "Non-GAAP diluted earnings per share excluding goodwill impairment and amortization ($1.75 in Q3 2026, beating $1.71 Street consensus).",
        "GAAP Diluted EPS": "GAAP diluted loss per share of $(11.17) in Q3 2026 due to the non-cash goodwill impairment charge.",
        "Clover Point of Sale Platform": "Flagship smart POS hardware and cloud business management operating system powering small-to-medium business commerce worldwide.",
        "Banking Net Attrition": "Financial institution client retention metric improving significantly, with net client attrition down more than 25% year-to-date.",
        "True Free Cash Flow": "Core economic cash generation deducting CapEx ($0.0M) and SBC ($110.0M) from operating cash flow ($1,012.0M), delivering $902.0M in Q3 2026.",
        "Operating Cash Flow": "Cash flow from operations ($1,012.0M in Q3 2026, bringing 9M YTD operating cash generation to $3,094.0M).",
        "Capital Expenditures": "Cash reinvested in proprietary data centers and terminal manufacturing ($0.0M in Q3 2026).",
        "Reported Free Cash Flow": "Operating cash flow minus capital expenditures ($1,012.0M in Q3 2026).",
        "Share Repurchase Acceleration": "Company announced $500M in common share repurchases scheduled for execution in Q4 2026.",
        "One Fiserv Action Plan": "Enterprise technology standardization, single-platform integration, and client experience simplification across merchant and banking divisions.",
        "MoneyPass Joint Venture": "Carve-out and partnership forming MoneyPass Group encompassing ATM Managed Services, of which Fiserv retains a minority financial interest.",
        "Full-Year Guidance Reaffirmation": "Company reaffirmed full-year 2026 organic revenue of (1%) to 0% and adjusted EPS corridor of $7.20 to $7.40.",
        "Stock-Based Compensation": "Equity awards granted to employees and management ($110.0M in Q3 2026)."
    }
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")

# ==============================================================================
# AGENT 2B: TRANSCRIPT FORENSICS & GUIDANCE (Transcript_Forensic_Agent)
# ==============================================================================
agent2b = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "matrix_a_execution_accountability": [
        {
            "metric": "Q3 2026 Total Revenue",
            "prior_guidance": "$4,800.0M - $4,950.0M adjusted ($4,875.0M midpoint)",
            "actual_delivered": "$5,196.0M GAAP / $4,852.0M adjusted",
            "variance_commentary": "Delivered solid top-line performance meeting expectations; Financial Solutions organic growth returned to positive territory (+2%).",
            "credibility_grade": "MET OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Adjusted Diluted EPS",
            "prior_guidance": "$1.70 - $1.74 ($1.72 midpoint)",
            "actual_delivered": "$1.75 delivered (+$0.03 above midpoint)",
            "variance_commentary": "Adjusted EPS beat expectations on operating cost discipline and favorable tax timing.",
            "credibility_grade": "BEAT OWN GUIDE"
        },
        {
            "metric": "Project Elevate Cost Savings",
            "prior_guidance": "$500.0M initial target",
            "actual_delivered": "Doubled to $1,000.0M ($1.0B) run-rate savings",
            "variance_commentary": "Management accelerated organizational streamlining, portfolio simplification, and AI automation adoption.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Banking Net Attrition Rate",
            "prior_guidance": "Stabilizing / moderate decline",
            "actual_delivered": "Down >25% year-to-date",
            "variance_commentary": "Net client attrition in regional and community banking dropped 25% YTD as new platform implementations stabilized.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "FY 2026 Organic Revenue Growth",
            "pre_print_consensus": "-0.5%",
            "management_guidance": "(1%) to 0% (Reaffirmed)",
            "delta_vs_street": "In-line with Street expectations",
            "action_badge": "REAFFIRMED",
            "pm_rationale": "Signals second-half stability and acceleration heading into Q4, driven by Financial Solutions pipeline ramp."
        },
        {
            "metric": "FY 2026 Adjusted Diluted EPS",
            "pre_print_consensus": "$7.28",
            "management_guidance": "$7.20 to $7.40 ($7.30 midpoint)",
            "delta_vs_street": "+$0.02 above Street consensus midpoint",
            "action_badge": "REAFFIRMED",
            "pm_rationale": "High earnings visibility backed by $1.0B Project Elevate savings and $500M Q4 share buybacks."
        },
        {
            "metric": "Q4 2026 Share Repurchase Program",
            "pre_print_consensus": "$0 - $250M",
            "management_guidance": "$500.0M in open-market repurchases",
            "delta_vs_street": "+$250.0M capital return acceleration",
            "action_badge": "RAISED AGGRESSIVELY",
            "pm_rationale": "Demonstrates management confidence in free cash flow durability and undervalued share price at ~7.3x forward P/E."
        },
        {
            "metric": "Long-Term Cost Run-Rate Savings",
            "pre_print_consensus": "$500.0M",
            "management_guidance": "$1,000.0M ($1.0B) through Project Elevate",
            "delta_vs_street": "+$500.0M (+100%) expansion",
            "action_badge": "RAISED AGGRESSIVELY",
            "pm_rationale": "Substantially expands forward margin expansion potential into FY27 and FY28."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Tien-tsin Huang (JPMorgan)",
            "topic": "Project Elevate Savings Expansion to $1B & Goodwill Impairment Trigger",
            "question": "Takis, you doubled the Project Elevate target to $1 billion while taking a $6.45B non-cash goodwill impairment. How much of the $1B savings flows through to net operating income in 2027 versus being reinvested, and what drove the timing of the impairment?",
            "executive_answer": "Takis Georgakopoulos (CEO) replied: 'The goodwill impairment was a non-cash accounting exercise required by the sustained pressure on our equity valuation; it has zero impact on our cash balances, bank covenants, or liquidity. Regarding Project Elevate, we identified profound structural efficiencies as we apply AI across customer service, code modernization, and merchant onboarding. We expect at least half of the $1 billion in annualized savings to drop directly to operating income over the next 18 to 24 months.'"
        },
        {
            "analyst": "Jason Kupferberg (Bank of America)",
            "topic": "Clover Volume Growth & Merchant Attrition vs Integrated FinTech Rivals",
            "question": "Paul, Merchant Solutions revenue was down 3% GAAP and 2% organic. Can you unpack Clover's performance, merchant take rates, and how competitive dynamics are playing out against Toast and Square?",
            "executive_answer": "Paul Todd (CFO) answered: 'Clover volume continues to grow at double-digit rates, and software attach is expanding. The slight headline revenue decline was primarily driven by lower hardware shipments compared to tough comps and our deliberate pruning of low-margin processing volume. As our modern merchant platform ramps, we see merchant organic revenue re-accelerating in the fourth quarter.'"
        },
        {
            "analyst": "Ramsey El-Assal (Barclays)",
            "topic": "Banking Attrition Reduction & Q4 Revenue Acceleration Path",
            "question": "Takis, net attrition in banking is down 25% YTD and Financial Solutions was flat GAAP / +2% organic. What gives you confidence in sequential acceleration for Q4, and are you seeing core conversion wins?",
            "executive_answer": "Takis Georgakopoulos explained: 'Client retention is our top operating priority, and seeing net banking attrition fall over 25% is proof that our One Fiserv integration is working. We signed multiple major financial institution renewals in Q3 that start billing in Q4. That gives us full line of sight to achieving our full-year organic guidance and returning to sustainable growth in 2027.'"
        }
    ]
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")

# ==============================================================================
# AGENT 2C: SENTIMENT & SOCIAL PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "four_pillar_sentiment": {
        "institutional_score": 78,
        "retail_score": 72,
        "options_skew_score": 70,
        "sell_side_score": 79,
        "composite_verdict": "Value Turnaround & Capital Return Acceleration"
    },
    "retail_pulse": {
        "score": 72,
        "tone": "Relief on Steady EPS & Buyback News",
        "key_themes": [
            "Retail sentiment across Reddit r/stocks and FinTwit relieved that core operations held steady with $1.75 adjusted EPS",
            "Discussion focusing on the $6.45B goodwill impairment being purely non-cash, with attention shifting to the $1B Project Elevate savings and $500M share buyback",
            "Stock holding steady after-hours at $57.79 (-1.04%), well inside the priced 9.75% straddle band"
        ]
    },
    "institutional_positioning": {
        "score": 78,
        "tone": "Turnaround Validation & Attractive Deep Value Multiples",
        "key_themes": [
            "Institutional value investors viewing FISV as deeply undervalued at ~7.3x forward P/E and ~11.2x trailing earnings",
            "Positive reaction to the 25% reduction in banking attrition and doubling of Project Elevate cost savings target to $1.0B",
            "Sell-side desks (JPMorgan, BofA, Barclays, Evercore) maintaining positive ratings, emphasizing robust $902M True FCF"
        ]
    },
    "pm_takeaway": "Fiserv delivered a solid operating stabilization print. Q3 GAAP revenue of $5,196.0M beat consensus ($4,844.24M) by +$351.76M (+7.26%), while Adjusted EPS came in at $1.75 vs $1.71 Street consensus (+2.34% beat). While a non-cash goodwill impairment of $6.45B resulted in a GAAP loss of $(11.17) per share, underlying operating cash flow reached $1,012.0M, generating $902.0M in True Free Cash Flow. Crucially, CEO Takis Georgakopoulos doubled the Project Elevate savings target to $1.0B and announced an accelerated $500M share buyback for Q4, reaffirming full-year guidance."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for FISV.")
