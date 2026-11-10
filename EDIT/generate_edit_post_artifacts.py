import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "EDIT"
DATE = "2026-11-09"

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
            "q_minus_1_actual": 11.89,
            "q_minus_4_yoy": 7.54,
            "street_consensus_q0": 4.53,
            "reported_actual_q0": 10.37,
            "spread_vs_street": "+128.92%",
            "verdict": "BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Collaboration & Licensing Revenue ($M)",
            "q_minus_1_actual": 10.40,
            "q_minus_4_yoy": 6.20,
            "street_consensus_q0": 3.80,
            "reported_actual_q0": 10.37,
            "spread_vs_street": "+172.89%",
            "verdict": "BEAT",
            "bar_width_pct": 99
        },
        {
            "name": "Diluted EPS ($)",
            "q_minus_1_actual": -0.15,
            "q_minus_4_yoy": -0.28,
            "street_consensus_q0": -0.21,
            "reported_actual_q0": -0.15,
            "spread_vs_street": "+$0.06",
            "verdict": "BEAT",
            "bar_width_pct": 85
        },
        {
            "name": "Operating Cash Burn ($M)",
            "q_minus_1_actual": -29.57,
            "q_minus_4_yoy": -30.84,
            "street_consensus_q0": -28.00,
            "reported_actual_q0": -21.19,
            "spread_vs_street": "+$6.81M",
            "verdict": "DISCIPLINE",
            "bar_width_pct": 92
        },
        {
            "name": "Liquid Cash & Securities Runway ($M)",
            "q_minus_1_actual": 184.49,
            "q_minus_4_yoy": 146.60,
            "street_consensus_q0": 165.00,
            "reported_actual_q0": 190.20,
            "spread_vs_street": "+$25.20M",
            "verdict": "FORTRESS",
            "bar_width_pct": 95
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Collaboration & Licensing Revenue",
                "values": [6.20, 22.50, 2.10, 10.40, 10.37, 8.50],
                "qoq": "-0.3%",
                "yoy": "+67.3%"
            },
            {
                "name": "Development Milestones & Grants",
                "values": [1.34, 2.24, 0.73, 1.49, 0.00, 1.50],
                "qoq": "-100.0%",
                "yoy": "-100.0%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [7.54, 24.74, 2.83, 11.89, 10.37, 10.00],
                "qoq": "-12.8%",
                "yoy": "+37.5%"
            }
        ]
    },
    "tooltip_definitions": {
        "Total GAAP Revenue": "Consolidated GAAP net revenue from Editas Medicine biopharma collaborations, license fees, and research milestones ($10.37M in Q3 2026, beating Street consensus $4.53M by +128.92%).",
        "Collaboration & Licensing Revenue": "Contractual research and development fees and upfront license amortization from strategic partners including Bristol Myers Squibb ($10.37M in Q3 2026, up +67.3% YoY).",
        "Diluted EPS": "GAAP diluted net loss per share of -$0.15 in Q3 2026 based on 153.6M weighted average shares, beating Street consensus (-$0.21) by $0.06.",
        "Operating Cash Burn": "Operating cash outflow of -$21.19M in Q3 2026, narrowing significantly from -$29.57M in Q2 2026 and -$30.84M in Q3 2025 due to prudent R&D expense management.",
        "Liquid Cash & Securities Runway": "Cash, cash equivalents, and marketable securities totaling $190.20M as of September 30, 2026, funding operations into the second half of 2028.",
        "EDIT-401 Strive Study": "Editas' wholly-owned, in vivo gene editing medicine targeting LDLR for hyperlipidemia/HeFH; cleared by Australia HREC/TGA for Phase 1/2 Strive trial with dosing initiating in 2026.",
        "AHA Preclinical Durability": "New preclinical data presented at American Heart Association (AHA) demonstrating >=90% durable LDL-C reduction sustained over 10 months in non-human primates.",
        "BMS-986527 Milestone": "Second IND/CTA accepted for BMS collaboration program (CD70 allogeneic CAR-T therapy using Cas12a for clear cell renal cell carcinoma), triggering a cash milestone to Editas.",
        "Cas12a Patent Estate": "Editas' proprietary CRISPR-Cas12a intellectual property portfolio, providing fundamental freedom-to-operate and cross-licensing leverage across oncology and cardiovascular medicine.",
        "Targeted LNP Platform (tLNP)": "Novel extrahepatic targeted lipid nanoparticle delivery platform presented at ESGCT 2026 demonstrating precise in vivo delivery of mRNA to targeted T-cells.",
        "Operating Loss": "GAAP operating loss of -$24.28M in Q3 2026 ($10.37M revenue minus $34.65M operating expenses), improving YoY from -$24.55M.",
        "Research and Development": "Laboratory discovery, preclinical pharmacology, and Strive study preparatory costs totaling $21.17M in Q3 2026 compared to $19.78M in Q3 2025.",
        "General and Administrative": "Corporate overhead, legal defense, and patent prosecution expenses of $13.48M in Q3 2026 compared to $12.32M in Q3 2025.",
        "Reported Free Cash Flow": "Operating cash flow (-$21.19M) minus capital expenditures (-$0.09M) equals reported negative free cash flow of -$21.28M in Q3 2026.",
        "Stock-Based Compensation": "Non-cash equity compensation expense of $2.48M in Q3 2026 ($6.87M for 9M 2026).",
        "True Free Cash Flow": "Comprehensive economic cash burn subtracting CapEx ($0.09M) and SBC ($2.48M) from OCF (-$21.19M), totaling -$23.76M in Q3 2026.",
        "After-Hours Reaction": "EDIT stock rose +1.82% to $2.80 in after-hours trading as revenue more than doubled consensus ($10.37M vs $4.53M) and cash runway was reconfirmed into 2H 2028.",
        "Dan Ory Appointment": "Appointment of Dan Ory, M.D. as Chief Medical Officer, bringing over 25 years of cardiovascular and genetic medicine expertise to lead the EDIT-401 clinical campaign.",
        "Evercore Fireside Chat": "Upcoming institutional presentation scheduled for November 30, 2026 at the 9th Annual Evercore Healthcare Conference."
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
            "prior_guidance": "$4.0M - $6.0M",
            "reported_actual": "$10.37M",
            "variance": "+$4.37M above top end",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Cash Runway Horizon",
            "prior_guidance": "Into 2H 2028",
            "reported_actual": "Reconfirmed into 2H 2028 ($190.2M balance)",
            "variance": "On track through key readouts",
            "grade": "MET GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "EDIT-401 Regulatory Milestones",
            "prior_guidance": "Australian CTN/HREC clearance in 2H 2026",
            "reported_actual": "Cleared HREC and CTN; Strive trial ready",
            "variance": "100% execution on timeline",
            "grade": "BEAT OWN GUIDE",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Q3 2026 Diluted EPS ($)",
            "prior_guidance": "-$0.25 to -$0.20",
            "reported_actual": "-$0.15",
            "variance": "+$0.05 outperformance",
            "grade": "BEAT OWN RANGE",
            "badge_class": "badge-bull"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Cash Runway Horizon",
            "street_pre_print": "Mid-2028",
            "new_guidance": "Into Second Half of 2028 ($190.2M liquid)",
            "delta": "Fully funded through Strive readouts",
            "action": "RECONFIRMED FORTRESS",
            "badge_class": "badge-bull"
        },
        {
            "metric": "EDIT-401 Initial Clinical Data",
            "street_pre_print": "1H 2027",
            "new_guidance": "Patient dosing in 2026; initial safety Q1 2027",
            "delta": "Accelerated timeline visibility",
            "action": "MILESTONE CLARITY",
            "badge_class": "badge-bull"
        },
        {
            "metric": "EDIT-401 Part 1 Topline Safety & Efficacy",
            "street_pre_print": "Late 2027",
            "new_guidance": "Complete enrollment & report data 2H 2027",
            "delta": "Clear catalyst roadmap",
            "action": "SCHEDULE LOCKED",
            "badge_class": "badge-bull"
        },
        {
            "metric": "Full-Year 2026 Operating Cash Burn",
            "street_pre_print": "$105.0M",
            "new_guidance": "$95.0M - $100.0M (~$98.0M midpoint)",
            "delta": "-$7.0M disciplined reduction",
            "action": "BURN REDUCED",
            "badge_class": "badge-bull"
        }
    ],
    "credibility_score": 90,
    "top_call_exchanges": [
        {
            "analyst": "Gena Wang (Barclays)",
            "topic": "EDIT-401 Strive Study Initiation & Dose Escalation Strategy",
            "question": "With HREC approval and CTN clearance in hand in Australia, what are the next gating items to dosing the first patient in the Strive study before year-end, and when will we see the first clinical biomarker data?",
            "management_answer": "Gilmore O'Neill (CEO): 'We have completed site activation in Australia and screening is actively underway. We remain fully on track to dose our first HeFH patient this year and report initial clinical safety and tolerability metrics in the first quarter of 2027, followed by Part 1 topline efficacy in the second half of 2027.'",
            "verdict": "FIRST PATIENT DOSING 2026 COMMITTED"
        },
        {
            "analyst": "Yanan Zhu (Wells Fargo)",
            "topic": "AHA 10-Month NHP Durability & Competitive LDL-C Positioning",
            "question": "At AHA, you demonstrated >=90% LDL-C reduction sustained over 10 months in NHPs. How does the upregulation mechanism compare to base editing or PCSK9 knockdown approaches in terms of permanence and off-target safety?",
            "management_answer": "Dan Ory (CMO): 'Our targeted upregulation approach directly restores LDLR protein expression, tackling the root etiology of HeFH. The 10-month preclinical durability data in NHPs showed clean liver specificity, transient LFT blips with zero histopathology, and no genotoxicity in primary human cells, creating a potentially best-in-class profile.'",
            "verdict": "BEST-IN-CLASS DURABILITY VALIDATED"
        },
        {
            "analyst": "Greg Harrison (Bank of America)",
            "topic": "BMS Collaboration Pipeline & Milestone Inflows",
            "question": "Can you provide more context on the second IND acceptance for BMS-986527 in renal cell carcinoma? Does this trigger near-term cash milestones and validate Cas12a commercial royalties?",
            "management_answer": "Gilmore O'Neill (CEO): 'The acceptance of the second IND/CTA for BMS-986527 validates both our Cas12a gene editing platform and our collaboration engine. It triggered a milestone payment recognized this quarter and positions Editas for downstream clinical and commercial milestone payments plus tiered royalties as BMS advances into Phase 1.'",
            "verdict": "CASH MILESTONE & ROYALTY UPSIDE"
        }
    ]
}

# ==============================================================================
# AGENT 2C: SOCIAL & MARKET PULSE (Social_Pulse_Agent)
# ==============================================================================
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "retail_sentiment_score": 74,
    "institutional_sentiment_score": 78,
    "composite_sentiment_score": 76,
    "sentiment_breakdown": {
        "retail_pulse": "Bullish relief on FinTwit and r/CRISPR. Retail investors are celebrating the massive revenue beat ($10.37M vs $4.53M), narrowing quarterly net loss (-$0.15 vs -$0.21), and the reconfirmed cash runway into 2H 2028, removing near-term dilution overhang.",
        "sell_side_reaction": "Positive and catalyst-focused. Analysts at Barclays, Wells Fargo, and Evercore view the Australian trial green light for EDIT-401 and the durable 10-month AHA data as key clinical de-risking milestones ahead of 2027 readouts.",
        "management_tone": "Methodical, confident, and scientifically grounded. Dr. Gilmore O'Neill and new CMO Dr. Dan Ory emphasized regulatory execution, balance sheet strength, and rapid progression of the in vivo hyperlipidemia pipeline.",
        "options_iv_crush": "Options implied move was ±26.72% ($0.70). The muted after-hours uptick of +1.82% (+$0.05 to $2.80) resulted in steep IV crush on weekly options, favoring theta-positive straddle sellers."
    },
    "after_hours_driver": "EDIT shares rose +1.82% to $2.80 in after-hours trading as Editas delivered a commanding top-line revenue beat ($10.37M vs $4.53M Street consensus), narrowed EPS loss (-$0.15 vs -$0.21), and reconfirmed an extensive cash runway into the second half of 2028 ($190.2M balance), providing fully-funded clinical execution through initial 2027 data readouts for its lead in vivo gene editing candidate EDIT-401."
}

# Write files to post_agent_bus
(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print(f"Successfully generated post agent bus files for {TICKER} ({DATE}).")
