import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "RIVN"
DATE = "2026-10-29"

BUS_DIR = BASE_DIR / "post_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

# 1. Agent 2A: KPIs & Segments
agent2a = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "operational_kpis": [
        {
            "name": "Vehicle Deliveries (Units)",
            "q_minus_1_actual": 12194,
            "q_minus_4_yoy": 13201,
            "street_consensus_q0": 13500,
            "reported_actual_q0": 19248,
            "spread_vs_street": "+42.6%",
            "verdict": "BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Automotive Revenue ($M)",
            "q_minus_1_actual": 1143.0,
            "q_minus_4_yoy": 1142.0,
            "street_consensus_q0": 1050.0,
            "reported_actual_q0": 1550.0,
            "spread_vs_street": "+47.6%",
            "verdict": "BEAT",
            "bar_width_pct": 96
        },
        {
            "name": "Software and Services Revenue ($M)",
            "q_minus_1_actual": 515.0,
            "q_minus_4_yoy": 416.0,
            "street_consensus_q0": 400.0,
            "reported_actual_q0": 605.0,
            "spread_vs_street": "+51.3%",
            "verdict": "BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "GAAP Gross Margin (%)",
            "q_minus_1_actual": 10.8,
            "q_minus_4_yoy": 1.5,
            "street_consensus_q0": 4.5,
            "reported_actual_q0": 8.2,
            "spread_vs_street": "+370 bps",
            "verdict": "BEAT",
            "bar_width_pct": 86
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E"],
        "segments": [
            {
                "name": "Automotive",
                "values": [1142.0, 839.0, 908.0, 1143.0, 1550.0, 1680.0],
                "qoq": "+35.6%",
                "yoy": "+35.7%"
            },
            {
                "name": "Software and services",
                "values": [416.0, 447.0, 473.0, 515.0, 605.0, 640.0],
                "qoq": "+17.5%",
                "yoy": "+45.4%"
            }
        ]
    },
    "tooltip_definitions": {
        "Automotive Revenue": "Revenues from R1T, R1S, R2 midsize SUV, and Electric Delivery Van (EDV) retail and commercial deliveries.",
        "Software & Services": "Fleet telematics, charging network revenue, vehicle financing, insurance, and maintenance subscriptions.",
        "R2 Midsize Platform": "Rivian's high-volume midsize SUV platform manufactured in Normal, Illinois; outsold R1 and EDV in Q3.",
        "Vehicle Deliveries": "Customer handoffs of completed production vehicles (19,248 delivered in Q3 2026, +46% YoY).",
        "GAAP Gross Margin": "Gross profit divided by total revenue (8.17% in Q3 2026, positive for the fifth straight quarter).",
        "Operating Loss": "Consolidated GAAP loss from operations (-$881.0M in Q3 2026, stable vs -$881.0M in Q1 2026).",
        "True FCF": "Operating cash flow minus capital expenditures, stock-based compensation, and finance lease additions (-$1,276.0M in Q3).",
        "Volkswagen Joint Venture": "Strategic technology partnership with VW Group providing capital infusions and shared zonal architecture.",
        "Clean Regulatory Credits": "Environmental credit sales to legacy automakers lacking zero-emission vehicle compliance ($80M recognized in Q3).",
        "Research & Development": "Investment in next-gen electrical architecture, autonomy software, and battery cell manufacturing ($485M in Q3).",
        "Selling, General & Administrative": "Expenditures on retail spaces, service centers, delivery logistics, and executive operations ($572M in Q3).",
        "GAAP Diluted EPS": "Net loss per share attributable to common stockholders (-$0.63 in Q3 2026 vs -$0.72 consensus).",
        "Operating Cash Flow": "Cash flow from operations (-$703.0M in Q3 2026).",
        "Capital Expenditures": "Investment in Normal plant retooling and Georgia manufacturing facility ($366.0M in Q3).",
        "Normal Illinois Plant": "Primary manufacturing facility producing R1T, R1S, EDV, and the newly ramped R2 SUV.",
        "Georgia Manufacturing Facility": "Second manufacturing plant planned to scale global R2 and R3 platform production.",
        "EDV Fleet Deliveries": "Custom electric delivery vans delivered to Amazon and commercial logistics operators.",
        "Enterprise Value": "Total market capitalization plus debt minus cash ($16.67B at market close).",
        "Options Implied Move": "Weekly straddle implied move was ±11.18%; actual move was +5.59% to $12.09.",
        "Cash Fortress": "Available cash, cash equivalents, and short-term liquid investments supporting R2 production ramp."
    }
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")

# 2. Agent 2B: Transcript Forensics & Guidance
agent2b = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "matrix_a_execution_accountability": [
        {
            "metric": "Q3 2026 Total Revenue",
            "prior_guidance": "$1,400M - $1,500M ($1,450M midpoint)",
            "actual_delivered": "$2,155.0M delivered (+48.6% above midpoint)",
            "variance_commentary": "Massive top-line beat powered by rapid consumer uptake of R2 deliveries and $80M in clean regulatory credit monetization.",
            "credibility_grade": "EXCEEDED"
        },
        {
            "metric": "Q3 2026 Vehicle Deliveries",
            "prior_guidance": "13,000 - 14,000 units (~13,500 midpoint)",
            "actual_delivered": "19,248 units delivered (+42.6% beat)",
            "variance_commentary": "Normal plant achieved record throughput with R2 outselling R1 and commercial vans in its introductory quarter.",
            "credibility_grade": "EXCEEDED"
        },
        {
            "metric": "GAAP Gross Margin",
            "prior_guidance": "Low single digits (3% - 5%)",
            "actual_delivered": "8.17% delivered (+370 bps beat)",
            "variance_commentary": "Per-unit cost reductions and supplier bill-of-materials savings offset $120M in initial R2 ramp launch costs.",
            "credibility_grade": "EXCEEDED"
        },
        {
            "metric": "GAAP Diluted Net Loss Per Share",
            "prior_guidance": "-$0.70 to -$0.75 (-$0.72 midpoint)",
            "actual_delivered": "-$0.63 delivered (+$0.09 favorable)",
            "variance_commentary": "Strong revenue leverage and commercial software growth narrowed operating losses per share.",
            "credibility_grade": "EXCEEDED"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Full-Year 2026 Vehicle Deliveries",
            "pre_print_consensus": "66,500 units",
            "management_guidance": "67,000 - 70,000 units (raised lower bound by +2,000)",
            "delta_vs_street": "+2,000 units above Street midpoint",
            "action_badge": "RAISED",
            "pm_rationale": "Upward revision proves robust production line stability in Normal and accelerating consumer R2 order backlog."
        },
        {
            "metric": "Full-Year 2026 Adjusted EBITDA",
            "pre_print_consensus": "-$1.90B",
            "management_guidance": "-$1.85B to -$1.75B (improved +$100M at midpoint)",
            "delta_vs_street": "+$100M loss reduction vs Street",
            "action_badge": "IMPROVED",
            "pm_rationale": "Reflects higher regulatory credit sales, tariff recoveries, and superior vehicle delivery margins."
        },
        {
            "metric": "Full-Year 2026 Capital Expenditures",
            "pre_print_consensus": "$1.75B",
            "management_guidance": "$1.40B - $1.50B (reduced by -$300M at midpoint)",
            "delta_vs_street": "-$300M CapEx reduction due to spend timing",
            "action_badge": "DISCIPLINED CAPEX",
            "pm_rationale": "Capital efficiency preserves cash runway without delaying R2 factory tooling or software development."
        },
        {
            "metric": "Q4 2026 Implied Deliveries",
            "pre_print_consensus": "14,500 - 15,500 units",
            "management_guidance": "15,200 - 18,200 units implied",
            "delta_vs_street": "+1,200 units above Street expectations",
            "action_badge": "SOLID OUTLOOK",
            "pm_rationale": "Sets up Rivian for a strong holiday delivery finish and positive gross margins heading into 2027."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Adam Jonas (Morgan Stanley)",
            "topic": "R2 Ramp Velocity, Unit Economics & Cannibalization",
            "question": "Can you provide more color on the customer profile for the R2? Are you seeing any cannibalization of R1S demand, and what are the gross margins on R2 relative to the corporate average?",
            "executive_answer": "RJ Scaringe (CEO) emphasized that R2 is bringing overwhelmingly new buyers into the Rivian brand, with over 70% of purchasers trading in internal combustion vehicles. While Q3 absorbed $120M in launch costs, R2's simplified zonal architecture and structural battery pack position it for double-digit positive gross margins as line rates mature."
        },
        {
            "analyst": "Colin Langan (Wells Fargo)",
            "topic": "Volkswagen Joint Venture Capital Timing & Tech Milestones",
            "question": "How quickly will the cash infusions from the Volkswagen joint venture hit the balance sheet, and when will the shared software stack deploy in production vehicles?",
            "executive_answer": "Claire McDonough (CFO) confirmed that regulatory milestones remain on track, with the first $1B convertible note already closed and subsequent equity tranches scheduled upon joint venture formation. Engineering teams are already co-developing the next-generation zonal compute platform."
        },
        {
            "analyst": "George Gianarikas (Canaccord Genuity)",
            "topic": "Georgia Fab Construction Timeline & Department of Energy Loan",
            "question": "What is the update on resuming construction at the Georgia manufacturing facility, and what is the status of the DOE ATVM loan application?",
            "executive_answer": "RJ Scaringe explained that pausing Georgia to launch R2 in Normal saved over $2.25B in near-term capital. The DOE loan due diligence is progressing positively, and resumption of Georgia construction will be timed to align with R2 volume expansion and R3 international launch in late 2027."
        }
    ]
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")

# 3. Agent 2C: Sentiment & Market Positioning
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "four_pillar_sentiment": {
        "institutional_score": 68,
        "retail_score": 75,
        "options_skew_score": 65,
        "sell_side_score": 72,
        "composite_verdict": "Emphatic Operational Re-Rating Led by R2 Execution"
    },
    "retail_pulse": {
        "score": 75,
        "tone": "Euphoric Validation",
        "key_themes": [
            "Tremendous excitement over R2 outselling R1 and winning Top Gear SUV of the Year",
            "Relief that gross margin remained solidly positive at 8.17%",
            "After-hours rally (+5.59% to $12.09) seen as confirmation of long-term EV survival"
        ]
    },
    "institutional_positioning": {
        "score": 68,
        "tone": "Constructive Accumulation on Loss Reduction",
        "key_themes": [
            "Hedge funds applaud the +$100M EBITDA guidance improvement and -$300M CapEx reduction",
            "Blowout revenue of $2,155M proves strong operational execution in an otherwise tough EV macro environment",
            "Volkswagen partnership capital provides multi-year runway, reducing dilutive equity risk"
        ]
    },
    "pm_takeaway": "RIVN delivered the cleanest beat and raise in the EV sector this quarter. Smashed top-line consensus by +48.6% ($2,155M vs $1,450M) as R2 ramped aggressively to become the company's best-selling vehicle. Gross margin printed at +8.17% (absorbing $120M in launch costs), full-year deliveries were raised to 67k-70k, EBITDA losses improved by $100M, and CapEx was reduced by $300M. The +5.59% after-hours rally to $12.09 marks a durable operational turning point."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for RIVN.")
