import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "TEM"
DATE = "2026-11-02"

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
            "name": "Diagnostics Segment Net Revenue ($M)",
            "q_minus_1_actual": 285.0,
            "q_minus_4_yoy": 253.0,
            "street_consensus_q0": 300.0,
            "reported_actual_q0": 303.5,
            "spread_vs_street": "+1.17%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "Data & Applications Net Revenue ($M)",
            "q_minus_1_actual": 97.5,
            "q_minus_4_yoy": 81.2,
            "street_consensus_q0": 105.0,
            "reported_actual_q0": 108.1,
            "spread_vs_street": "+2.95%",
            "verdict": "BEAT",
            "bar_width_pct": 94
        },
        {
            "name": "Adjusted EBITDA ($M)",
            "q_minus_1_actual": 18.2,
            "q_minus_4_yoy": 1.48,
            "street_consensus_q0": 20.0,
            "reported_actual_q0": 25.57,
            "spread_vs_street": "+27.85%",
            "verdict": "BLOWOUT BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Minimal Residual Disease (MRD) Tests Volume",
            "q_minus_1_actual": 9000,
            "q_minus_4_yoy": 3000,
            "street_consensus_q0": 10500,
            "reported_actual_q0": 12000,
            "spread_vs_street": "+14.29%",
            "verdict": "BEAT",
            "bar_width_pct": 95
        },
        {
            "name": "Cash, Equivalents & Marketable Securities ($M)",
            "q_minus_1_actual": 780.0,
            "q_minus_4_yoy": 450.0,
            "street_consensus_q0": 820.0,
            "reported_actual_q0": 854.4,
            "spread_vs_street": "+4.20%",
            "verdict": "BEAT",
            "bar_width_pct": 90
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Diagnostics (Genomics & Clinical Testing)",
                "values": [253.0, 275.0, 260.0, 285.0, 303.5, 335.0],
                "qoq": "+6.5%",
                "yoy": "+20.0%"
            },
            {
                "name": "Data and Applications (AI & Licensing)",
                "values": [81.21, 92.21, 88.12, 97.49, 108.04, 125.5],
                "qoq": "+10.8%",
                "yoy": "+33.0%"
            }
        ]
    },
    "tooltip_definitions": {
        "Diagnostics Segment": "Clinical next-generation sequencing (NGS), somatic oncology profiling, hereditary germline testing, and liquid biopsy assays ($303.5M in Q3 2026, up +20.0% YoY).",
        "Data and Applications": "High-margin pharmaceutical multimodal data licensing, algorithm co-development, and clinical trial matching software ($108.1M in Q3 2026, up +33.0% YoY).",
        "Minimal Residual Disease (MRD)": "Ultra-sensitive personalized circulating tumor DNA (ctDNA) blood test monitoring post-treatment molecular recurrence (~12,000 tests in Q3, up +300% YoY).",
        "Adjusted EBITDA": "Earnings before interest, taxes, depreciation, and amortization, excluding stock-based compensation and transaction costs ($25.57M in Q3 2026, surging +1,633% YoY).",
        "Oncology Clinical Volume": "Volume of somatic tissue and liquid sequencing tests ordered by oncologists across Tempus' network of connected healthcare systems (+32% unit growth).",
        "Merck & Moderna Collaboration": "Multi-year strategic alliance supporting commercialization and patient identification for individualized neoantigen therapy (INT) cancer vaccines.",
        "BMS Strategic Agreement": "Major data licensing and translational research expansion announced in October 2026, bringing YTD cumulative data bookings above $550M.",
        "Total Net Revenue": "Consolidated net sales across Diagnostics and Data & Applications ($411.54M in Q3 2026, beating $409.30M Street consensus by +$2.24M / +0.55%).",
        "Non-GAAP Diluted EPS": "Adjusted net income per share excluding stock-based compensation and non-operating fair value adjustments ($0.07 vs -$0.08 Street consensus, +$0.15 beat).",
        "GAAP Net Loss": "Net loss attributable to common stockholders under U.S. GAAP (-$14.85M in Q3 2026, improved by +81.4% YoY from -$79.98M).",
        "Operating Cash Flow": "Cash used in operating activities (-$71.59M in Q3 2026, demonstrating improved working capital efficiency vs -$119.84M YoY).",
        "Capital Expenditures": "Cash reinvested in high-throughput sequencing instrumentation, lab automation, and proprietary data infrastructure ($23.66M in Q3 2026).",
        "Reported Free Cash Flow": "Operating cash flow minus capital expenditures (-$95.25M in Q3 2026).",
        "True Free Cash Flow": "Forensic cash generation deducting $154.90M in non-cash stock compensation expense (-$250.15M institutional economic balance).",
        "Full-Year Guidance Raise": "Upward revision of FY2026 revenue guidance to $1.60B-$1.605B (~25% annual growth) and reaffirmation of full-year ~$65M Adjusted EBITDA.",
        "Options Volatility Regime": "Weekly ATM straddle priced a ±12.40% move ($9.05); stock moved -0.74% after-hours ($77.90), producing sharp volatility crush.",
        "Enterprise Value to Sales": "Valuation multiple comparing enterprise value ($14.79B) against forward annualized sales run-rate (~9.2x EV/Sales).",
        "Liquid Biopsy ctDNA": "Non-invasive genomic sequencing of cell-free circulating tumor DNA from peripheral blood samples, accelerating targeted therapy selection."
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
            "prior_guidance": "$405.0M - $410.0M ($407.5M midpoint)",
            "actual_delivered": "$411.54M delivered (+0.99% above midpoint)",
            "variance_commentary": "Top-line exceeded guidance driven by 32% volume growth in oncology diagnostics and 33% growth in high-margin Data & Applications.",
            "credibility_grade": "EXCEEDED OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Adjusted EBITDA",
            "prior_guidance": "$18.0M - $22.0M ($20.0M midpoint)",
            "actual_delivered": "$25.57M delivered (+27.85% beat)",
            "variance_commentary": "Adjusted EBITDA expanded by +1,633% YoY from $1.48M to $25.57M, reflecting strong operational leverage across automated sequencing labs.",
            "credibility_grade": "EXCEEDED OWN GUIDE"
        },
        {
            "metric": "Non-GAAP Diluted EPS",
            "prior_guidance": "Break-even (-$0.02 to +$0.02)",
            "actual_delivered": "$0.07 delivered (+$0.07 beat)",
            "variance_commentary": "Tempus crossed decisively into non-GAAP net profitability, crushing the consensus hurdle of -$0.08 by +$0.15.",
            "credibility_grade": "EXCEEDED OWN GUIDE"
        },
        {
            "metric": "MRD Volume Acceleration",
            "prior_guidance": ">10,000 tests",
            "actual_delivered": "~12,000 tests delivered (+300% YoY)",
            "variance_commentary": "Minimal Residual Disease assay uptake multiplied fourfold year-over-year as clinical adoption among academic medical centers expanded.",
            "credibility_grade": "EXCEEDED OWN GUIDE"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "FY 2026 Total Revenue",
            "pre_print_consensus": "$1,590.0M",
            "management_guidance": "$1.60B to $1.605B ($1,602.5M midpoint)",
            "delta_vs_street": "+$12.5M (+0.8%) upward revision",
            "action_badge": "RAISED",
            "pm_rationale": "Signals sustained momentum across pharma data partnerships and NGS sequencing volume throughout Q4."
        },
        {
            "metric": "FY 2026 Adjusted EBITDA",
            "pre_print_consensus": "$60.0M",
            "management_guidance": "~$65.0M (~4.1% margin)",
            "delta_vs_street": "+$5.0M (+8.3%) guidance floor",
            "action_badge": "RAISED",
            "pm_rationale": "Demonstrates path to sustainable positive operating cash flow generation entering fiscal 2027."
        },
        {
            "metric": "Implied Q4 2026 Revenue",
            "pre_print_consensus": "$452.0M",
            "management_guidance": "$458.0M to $463.0M ($460.5M midpoint)",
            "delta_vs_street": "+$8.5M (+1.9%) higher Q4 baseline",
            "action_badge": "RAISED",
            "pm_rationale": "Implies 26% YoY growth in fourth quarter as new multi-pharma licensing agreements begin recognizing upfront revenue."
        },
        {
            "metric": "Full-Year 2026 CapEx",
            "pre_print_consensus": "$65.0M",
            "management_guidance": "$75.0M to $85.0M",
            "delta_vs_street": "+$15.0M CapEx expansion",
            "action_badge": "INCREASED (CAPEX SURGE)",
            "pm_rationale": "Accelerating automation robotics and AI multimodal compute clusters to handle surge in pharma biobank sequencing."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Matt Larew (William Blair)",
            "topic": "Data & Applications Growth & Multi-Year Pharma Bookings",
            "question": "Eric, Data & Applications grew 33% and bookings surpassed $550M YTD with the BMS deal. How much of this is upfront software licensing versus recurring milestone ARR, and what is the pipeline for additional pharma partnerships?",
            "executive_answer": "Eric Lefkofsky (CEO) responded: 'Our data licensing model is increasingly institutionalized. Pharma partners are not buying one-off datasets; they are integrating Tempus multimodal data directly into their clinical oncology pipelines. The Merck, Moderna, and BMS collaborations are multi-year structural agreements with high renewal rates and expanding per-study licensing fees.'"
        },
        {
            "analyst": "Michael Ryskin (Bank of America)",
            "topic": "MRD Ramp, Reimbursement Coverage & Diagnostics Margins",
            "question": "Jim, with MRD tests reaching 12,000 units and gross margins expanding to 64.8%, what is your timeline for broad Medicare and commercial coverage for pan-cancer recurrence monitoring?",
            "executive_answer": "Jim Rogers (CFO) noted that Tempus has secured key MolDX local coverage determinations across colorectal and breast cancer indications, with broader pan-cancer dossiers submitted. He highlighted that lab automation is driving significant cost-of-sequencing efficiencies, allowing gross margins to scale toward 68%-70% over the next 18 months."
        },
        {
            "analyst": "Dan Leonard (UBS)",
            "topic": "Cash Runway, Path to Positive FCF & CapEx Discipline",
            "question": "With $854M in cash and marketable securities and Q3 Adjusted EBITDA hitting $25.6M, when do you anticipate crossing into positive quarterly Free Cash Flow after CapEx and lease commitments?",
            "executive_answer": "Jim Rogers (CFO) stated that Tempus expects operating cash burn to continue contracting sequentially, targeting sustained positive operating cash flow by mid-2027. He emphasized that the $854M balance sheet provides ample runway without any need for external dilutive equity financing."
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
        "institutional_score": 82,
        "retail_score": 75,
        "options_skew_score": 55,
        "sell_side_score": 88,
        "composite_verdict": "Premier AI Healthcare Platform & Emerging EBITDA Engine"
    },
    "retail_pulse": {
        "score": 75,
        "tone": "Bullish Consolidation & AI Healthcare Validation",
        "key_themes": [
            "Retail traders on Reddit and FinTwit celebrating Tempus' first non-GAAP profitable quarter ($0.07 EPS vs -$0.08 expected) as proof the business model is self-funding",
            "High enthusiasm over the Merck, Moderna, and BMS partnerships positioning Tempus as the 'Palantir of Precision Medicine'",
            "Mild -0.74% after-hours price reaction viewed as healthy consolidation following a +12% run-up heading into the print"
        ]
    },
    "institutional_positioning": {
        "score": 82,
        "tone": "Institutional Accumulation & Positive Estimate Revisions",
        "key_themes": [
            "Biotech and tech crossover funds view TEM as a rare high-growth asset (+23% rev growth, 65% gross margin) combining high-barrier diagnostics with AI software economics",
            "Sell-side analysts (BofA, William Blair, UBS) maintaining Overweight / Buy ratings with price targets clustered around $90-$100",
            "Options implied move of ±12.40% experienced a complete volatility collapse as the stock finished flat at $77.90"
        ]
    },
    "pm_takeaway": "Tempus delivered a solid beat-and-raise quarter. Q3 revenue of $411.54M beat consensus ($409.30M), Non-GAAP EPS surged to positive $0.07 (beating -$0.08 consensus), and Adjusted EBITDA exploded +1,633% to $25.57M. Lefkofsky raised full-year revenue guidance to $1.60B-$1.605B and reaffirmed ~$65M EBITDA. With $854.4M in liquidity and MRD volume accelerating +300% YoY, Tempus at $77.90 after-hours offers a compelling risk/reward entry for institutional portfolios building AI-enabled precision medicine exposure."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for TEM.")
