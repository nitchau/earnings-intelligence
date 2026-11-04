import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "XMTR"
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
            "name": "Marketplace Segment Revenue ($M)",
            "q_minus_1_actual": 215.0,
            "q_minus_4_yoy": 166.59,
            "street_consensus_q0": 221.0,
            "reported_actual_q0": 238.0,
            "spread_vs_street": "+7.69%",
            "verdict": "BLOWOUT BEAT",
            "bar_width_pct": 96
        },
        {
            "name": "Services Segment Revenue ($M)",
            "q_minus_1_actual": 14.28,
            "q_minus_4_yoy": 14.12,
            "street_consensus_q0": 14.58,
            "reported_actual_q0": 14.44,
            "spread_vs_street": "-0.96%",
            "verdict": "SLIGHT MISS",
            "bar_width_pct": 82
        },
        {
            "name": "Marketplace Active Buyers",
            "q_minus_1_actual": 89557.0,
            "q_minus_4_yoy": 78282.0,
            "street_consensus_q0": 91500.0,
            "reported_actual_q0": 93812.0,
            "spread_vs_street": "+2.53%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "Adjusted EBITDA ($M)",
            "q_minus_1_actual": 15.2,
            "q_minus_4_yoy": 6.14,
            "street_consensus_q0": 16.5,
            "reported_actual_q0": 21.42,
            "spread_vs_street": "+29.82%",
            "verdict": "BLOWOUT BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Operating Cash Flow ($M)",
            "q_minus_1_actual": 2.92,
            "q_minus_4_yoy": 5.79,
            "street_consensus_q0": 5.5,
            "reported_actual_q0": 7.87,
            "spread_vs_street": "+43.09%",
            "verdict": "BEAT",
            "bar_width_pct": 94
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Marketplace Revenue",
                "values": [166.59, 178.0, 190.5, 215.0, 238.0, 241.0],
                "qoq": "+10.7%",
                "yoy": "+42.9%"
            },
            {
                "name": "Services Revenue",
                "values": [14.12, 14.4, 14.64, 14.28, 14.44, 14.0],
                "qoq": "+1.1%",
                "yoy": "+2.3%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [180.72, 192.4, 205.14, 229.28, 252.44, 255.0],
                "qoq": "+10.1%",
                "yoy": "+39.7%"
            }
        ]
    },
    "tooltip_definitions": {
        "Marketplace Segment Revenue": "AI-powered on-demand manufacturing platform connecting enterprise buyers with certified suppliers ($238.0M in Q3 2026, up +42.9% YoY).",
        "Services Segment Revenue": "Supplier advertising, marketing services, and SaaS workflow tool subscriptions ($14.44M in Q3 2026, up +2.3% YoY).",
        "Marketplace Active Buyers": "Total unique customer accounts placing at least one on-demand manufacturing order in the last 12 months (surpassed 93,812 buyers, up +19.8% YoY).",
        "Adjusted EBITDA": "Core operating profitability excluding stock-based compensation, depreciation, and acquisition costs ($21.42M in Q3 2026, up 249% YoY with an 8.5% margin).",
        "Accounts Spend Over $50K": "Large enterprise accounts spending at least $50,000 annualized on custom parts (expanded +26.0% YoY to 2,172 accounts).",
        "Workcenter Experience": "Redesigned partner portal featuring AI sourcing models, interactive 3D drawing viewers, and automated job dispatching.",
        "TradeCentric eProcurement Integration": "Automated PunchOut, purchase order, and invoicing integration connected directly to Coupa, SAP Ariba, and Microsoft Dynamics across 220+ enterprise systems.",
        "GAAP Operating Income": "Operating profitability reached positive territory at $0.06M in Q3 2026, inflecting from a $(11.01)M operating loss in Q3 2025.",
        "GAAP Diluted EPS": "Net earnings per share of $0.03 in Q3 2026, turning profitable from $(0.23) diluted loss in Q3 2025.",
        "Non-GAAP Diluted EPS": "Adjusted earnings per share excluding stock compensation, reaching $0.28 in Q3 2026 vs $0.19 Street consensus (+47.4% beat).",
        "True Free Cash Flow": "Forensic cash generation deducting CapEx ($0.0M) and SBC ($11.29M) from operating cash flow ($7.87M), resulting in -$3.42M economic cash flow.",
        "Operating Cash Flow": "Positive operating cash generation of $7.87M in Q3 2026 ($25.41M 9M YTD).",
        "Capital Expenditures": "Reinvestment in platform infrastructure ($0.0M capitalized in Q3 2026).",
        "Reported Free Cash Flow": "Operating cash flow minus capital expenditures ($7.87M delivered in Q3 2026).",
        "Cash and Marketable Securities Fortress": "Combined cash, cash equivalents, and marketable securities totaling $505.0M with minimal debt.",
        "Annualized Revenue Run-Rate": "Xometry officially surpassed the landmark $1.0B annualized revenue run-rate during Q3 2026.",
        "Full-Year Guidance Surge": "Full-year 2026 revenue growth outlook raised to at least 37% (up from 33-34%), with Adjusted EBITDA guided to $68.0M - $68.5M.",
        "Stock-Based Compensation": "Equity-based compensation of $11.29M in Q3 2026."
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
            "prior_guidance": "$233.0M - $238.0M ($235.5M midpoint)",
            "actual_delivered": "$252.44M delivered (+7.19% above midpoint)",
            "variance_commentary": "Top-line crushed internal guidance as marketplace transaction volume surged +42.9% YoY on rapid enterprise adoption.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Adjusted EBITDA",
            "prior_guidance": "$15.0M - $17.0M ($16.0M midpoint)",
            "actual_delivered": "$21.42M delivered (+33.88% above midpoint)",
            "variance_commentary": "Adjusted EBITDA margin expanded 510 bps YoY to 8.5% driven by marketplace gross margin gains and operating leverage.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Marketplace Gross Margin",
            "prior_guidance": "~35.5% - 35.8%",
            "actual_delivered": "36.0% delivered (+30 bps YoY expansion)",
            "variance_commentary": "AI pricing and matching algorithms improved supplier routing efficiency, lifting marketplace gross margin to record 36.0%.",
            "credibility_grade": "BEAT OWN GUIDE"
        },
        {
            "metric": "Active Buyer Additions",
            "prior_guidance": "Sustained net buyer growth (~3,000 adds)",
            "actual_delivered": "Record 4,255 net additions (93,812 total)",
            "variance_commentary": "Record new buyer intake driven by enterprise marketing and expanding defense/aerospace supply chain adoption.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026 Revenue Guidance",
            "pre_print_consensus": "$248.0M",
            "management_guidance": "$254.0M - $256.0M ($255.0M midpoint)",
            "delta_vs_street": "+$7.0M (+2.82%) upward revision",
            "action_badge": "RAISED",
            "pm_rationale": "Represents 32-33% YoY growth, driven by sustained 35-36% marketplace volume expansion."
        },
        {
            "metric": "Q4 2026 Adjusted EBITDA",
            "pre_print_consensus": "$18.5M",
            "management_guidance": "$22.0M - $22.5M ($22.25M midpoint)",
            "delta_vs_street": "+$3.75M (+20.3%) margin expansion raise",
            "action_badge": "RAISED AGGRESSIVELY",
            "pm_rationale": "Demonstrates structural operating leverage with Adjusted EBITDA scaling nearly 3x from Q4 2025 ($8.4M)."
        },
        {
            "metric": "FY 2026 Revenue Growth Outlook",
            "pre_print_consensus": "+33.5% YoY",
            "management_guidance": "Raised to at least 37% YoY (> $940M)",
            "delta_vs_street": "+350 bps full-year growth acceleration",
            "action_badge": "RAISED",
            "pm_rationale": "Reinforces Xometry's expanding dominance as the default digital infrastructure for on-demand manufacturing."
        },
        {
            "metric": "FY 2026 Adjusted EBITDA",
            "pre_print_consensus": "$61.0M",
            "management_guidance": "$68.0M - $68.5M ($68.25M midpoint)",
            "delta_vs_street": "+$7.25M (+11.9%) full-year EBITDA raise",
            "action_badge": "RAISED AGGRESSIVELY",
            "pm_rationale": "Confirms compounding profitability with full-year Adjusted EBITDA surging nearly 4x from FY25 ($18.5M)."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Brian Peterson (Raymond James)",
            "topic": "Crossing the $1B Run-Rate & Enterprise Accounts Spending >$50K",
            "question": "Sanjeev, crossing the $1B run rate is a huge milestone. Can you talk about the 26% growth in $50K+ accounts, and how enterprise procurement integrations like TradeCentric are driving larger share of wallet?",
            "executive_answer": "Sanjeev Singh Sahni (CEO) stated: 'Crossing the $1 billion revenue run rate reflects our transformation from a spot quoting tool into essential enterprise supply chain infrastructure. Accounts spending over $50K grew 26% to 2,172, and 98% of our revenue came from existing accounts. With our TradeCentric integration now live across SAP Ariba, Coupa, and Microsoft Dynamics, corporate buyers can route purchase orders seamlessly through Xometry without leaving their native ERP systems.'"
        },
        {
            "analyst": "Eric Sheridan (Goldman Sachs)",
            "topic": "AI Sourcing Models, Workcenter Launch & Marketplace Gross Margin",
            "question": "James, marketplace gross margin hit a record 36.0%. How much of that expansion is driven by your new AI pricing algorithms versus supplier network scale, and what is the sustainable margin ceiling?",
            "executive_answer": "James Miln (CFO) responded: 'Our machine learning models continuously ingest supplier capacity, material spot costs, and regional delivery metrics. The 30 bps expansion to 36.0% was directly driven by improved pricing accuracy and automated routing in our new Workcenter portal. While we maintain a long-term target of 35-36%, our growing scale gives us exceptional pricing power and supplier engagement.'"
        },
        {
            "analyst": "Shawn Harrison (Loop Capital)",
            "topic": "Aerospace, Defense & Texas Manufacturing Hub Velocity",
            "question": "Sanjeev, you announced a partnership with MxD for CMMC cybersecurity certification and noted Texas partner jobs grew twice the national rate. How is defense and aerospace demand trending given reshoring mandates?",
            "executive_answer": "Sanjeev Singh Sahni explained: 'Defense and aerospace are among our fastest-growing sectors. Prime contractors require ITAR-compliant, CMMC-certified domestic suppliers, and our AI marketplace instantly identifies qualified American machine shops. Our Texas supplier network is expanding rapidly to meet aerospace demand, proving that digital manufacturing is central to the reshoring of the American industrial base.'"
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
        "institutional_score": 88,
        "retail_score": 82,
        "options_skew_score": 74,
        "sell_side_score": 89,
        "composite_verdict": "Digital Manufacturing Infrastructure Monopolist"
    },
    "retail_pulse": {
        "score": 82,
        "tone": "Strong Enthusiasm for $1B Run-Rate & GAAP Profitability",
        "key_themes": [
            "Retail investors on Reddit r/smallstreetbets and FinTwit celebrating Xometry inflecting to positive GAAP net income ($1.9M) and GAAP operating profit",
            "Enthusiasm surrounding the milestone of crossing $1.0B in annualized revenue run-rate and 40% top-line growth",
            "Stock holding steady after-hours at $109.80 (-1.34%), digesting a huge year-to-date run-up while staying well within the ±21.31% straddle band"
        ]
    },
    "institutional_positioning": {
        "score": 88,
        "tone": "Growth Compounding & Operating Leverage Inflection",
        "key_themes": [
            "Institutional small-to-mid-cap growth managers accumulating XMTR as the premier AI platform play in custom industrial manufacturing",
            "Appreciation for Adjusted EBITDA expanding 249% YoY to $21.4M with full-year guidance raised to $68M+",
            "Sell-side analysts (Raymond James, Goldman Sachs, Loop Capital, Needham) maintaining buy ratings with price targets moving toward $125-$140"
        ]
    },
    "pm_takeaway": "Xometry delivered an outstanding operational beat and guidance raise. Q3 revenue of $252.44M (+39.7% YoY) exceeded consensus ($235.58M) by +$16.86M (+7.16%), while Marketplace revenue surged 42.9% YoY to $238.0M as the company crossed the $1.0B annualized run-rate milestone. GAAP operations turned profitable at $1.94M net income ($0.03 EPS), and Adjusted EBITDA jumped 249% YoY to $21.42M (8.5% margin). Active Buyers reached a record 93,812 (+19.8% YoY). Management raised full-year revenue growth guidance to at least 37% and guided Q4 Adjusted EBITDA to $22.0M-$22.5M. With $505M in liquidity and positive operating cash flow ($7.87M), XMTR is compounding into an industrial tech powerhouse."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for XMTR.")
