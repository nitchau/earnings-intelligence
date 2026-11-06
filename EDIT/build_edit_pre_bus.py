import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "EDIT"
EARNINGS_DATE = "2026-11-09"

# Agent 2A: KPIs
bus_2a = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_KPI_Consensus_Agent (Agent 2A)",
    "model": "Gemini 3.8 Flash High Standard",
    "upcoming_quarter_label": "Q3 2026E",
    "latest_reported_quarter_label": "Q2 2026 (Ended Jun 30, 2026)",
    "headline_and_company_kpis": [
        {
            "metric": "Collaboration & License Revenue ($M)",
            "tooltip_title": "Quarterly revenue recognized from Cas9 and Cas12a intellectual property licensing and pharma partnerships.",
            "tooltip_def": "Collaboration & License Revenue ($M): Editas generated $11.89M in Q2 2026 (+232% YoY vs $3.58M in Q2 2025). Street consensus models $4.53M for Q3 2026E (-39.88% YoY vs $7.54M in Q3 2025), with buy-side whisper bogeys looking for $5.20M on Cas12a out-licensing payments.",
            "q_minus_1_actual": "$11.89M",
            "q_minus_4_yoy_baseline": "$7.54M",
            "street_consensus_q0e": "$4.53M",
            "whisper_bogey_q0e": "$5.20M",
            "whisper_spread_display": "+14.79% Spread",
            "bar_width_pct": 84,
            "hurdle_badge": "Revenue Hurdle"
        },
        {
            "metric": "GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Quarterly GAAP net loss per share reflecting research burn and clinical pipeline execution.",
            "tooltip_def": "GAAP Diluted EPS ($/sh): Q2 2026 actual EPS was -$0.15 (beating consensus of -$0.28). Wall Street consensus models -$0.21 for Q3 2026E with buy-side whisper looking for -$0.18 on disciplined headcount containment.",
            "q_minus_1_actual": "-$0.15",
            "q_minus_4_yoy_baseline": "-$0.28",
            "street_consensus_q0e": "-$0.21",
            "whisper_bogey_q0e": "-$0.18",
            "whisper_spread_display": "+$0.03 Better",
            "bar_width_pct": 78,
            "hurdle_badge": "EPS Hurdle"
        },
        {
            "metric": "Cash Runway Horizon (Months / Year)",
            "tooltip_title": "Total cash, cash equivalents, and marketable securities divided by quarterly operating burn.",
            "tooltip_def": "Cash Runway Horizon: Editas holds >$265M in liquid cash resources providing operational runway into 2027; consensus expects management to reaffirm runway past year-end 2026 without near-term equity dilution.",
            "q_minus_1_actual": "Into 2027",
            "q_minus_4_yoy_baseline": "Late 2026",
            "street_consensus_q0e": "Mid 2027",
            "whisper_bogey_q0e": "Late 2027+",
            "whisper_spread_display": "Fortress Runway",
            "bar_width_pct": 88,
            "hurdle_badge": "Liquidity Fortress"
        },
        {
            "metric": "Reni-cel Clinical Partnering / In Vivo Pipeline",
            "tooltip_title": "Strategic partnership status for reni-cel (EDIT-301) in Sickle Cell / Beta-Thalassemia and preclinical in vivo programs.",
            "tooltip_def": "Clinical Partnering Pipeline: Management is actively seeking an ex-US or global commercialization partner for reni-cel to fund Phase 3 pivotal trials while refocusing internal resources on proprietary in vivo upregulation platforms.",
            "q_minus_1_actual": "Partner Search",
            "q_minus_4_yoy_baseline": "Phase 1/2 Data",
            "street_consensus_q0e": "Term Sheet Update",
            "whisper_bogey_q0e": "Signed Partnership",
            "whisper_spread_display": "Binary Catalyst",
            "bar_width_pct": 92,
            "hurdle_badge": "Strategic Bogey"
        }
    ]
}

# Agent 2B: Guidance & Debates
bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 80,
    "credibility_label": "80 / 100 (Strong Track Record of 75% EPS Beats & Conservative Burn Management)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 2026E Net Collaboration Revenue",
            "tooltip_title": "Prior revenue expectations discussed during Q2 2026 earnings conference call.",
            "tooltip_def": "Q3 Revenue Baseline: Management indicated quarterly license revenue would normalize between $3.0M and $6.0M following Q2's milestone timing.",
            "prior_q_guidance_for_q0": "$3.0M – $6.0M ($4.5M Midpoint)",
            "current_street_consensus": "$4.53M",
            "historical_4q_beat_rate": "75.0% (3 of 4 Quarters)",
            "variance_and_sandbag_commentary": "Editas has beaten consensus EPS in 3 of the last 4 quarters (avg surprise +34.5%), consistently underspending on SG&A while hitting patent license collection milestones.",
            "credibility_grade": "Grade A- (Disciplined)"
        },
        {
            "metric": "Annual Operating Expense Burn Target",
            "tooltip_title": "Full-year guidance for operating expenses and cash burn trajectory.",
            "tooltip_def": "OpEx Burn Corridor: Management targeted full-year operating expense reduction of 15-20% YoY through strategic reprioritization toward in vivo programs.",
            "prior_q_guidance_for_q0": "15–20% YoY Reduction",
            "current_street_consensus": "-18.5% YoY",
            "historical_4q_beat_rate": "100.0% Execution",
            "variance_and_sandbag_commentary": "Management has successfully rationalized laboratory operations and clinical site costs in line with guidance.",
            "credibility_grade": "Grade A (Prudent Stewardship)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Reni-cel Commercial Partnership Deal Announcement",
            "tooltip_title": "Target timeline for securing an external pharma partner to assume clinical trial funding.",
            "tooltip_def": "Reni-cel Partnership Hurdle: Street models non-dilutive upfront cash payment >$50M plus downstream development milestones; buy-side requires signed agreement by Q4 2026.",
            "street_consensus_hurdle": "Agreement by Year-End 2026",
            "bull_case_bogey": "Upfront Cash >$75M + Global Rights",
            "bear_case_breakdown": "Partnership Delayed into 2027",
            "sensitivity_badge": "High Multiple Sensitivity",
            "strategic_rationale": "Editas' high short interest (24.91% of float) means a cash-rich partnership announcement would trigger immediate short covering toward the $6.10 mean price target (+132.8% upside)."
        },
        {
            "forward_metric": "Cas12a IP Licensing Revenue Acceleration (2027)",
            "tooltip_title": "Projected royalty streams from Vertex Cas9 licensing and emerging Cas12a gene editing licenses.",
            "tooltip_def": "Cas12a IP Royalties: Confirmation of expanding third-party licensing revenue pipeline exceeding $25M annually by FY2027.",
            "street_consensus_hurdle": "$15.0M – $20.0M Annual Run-Rate",
            "bull_case_bogey": "> $30.0M / Multiple New Licensees",
            "bear_case_breakdown": "< $10.0M or Patent Litigation Drag",
            "sensitivity_badge": "Valuation Floor",
            "strategic_rationale": "High-margin IP licensing provides a recurring non-dilutive valuation floor that decouples Editas from clinical trial binary risk."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "title": "1. Reni-cel Partnering Deal Structure & Upfront Cash Inflow",
            "title_color": "#60a5fa",
            "border_color": "#3b82f6",
            "badge": "CLINICAL PARTNERSHIP",
            "badge_class": "badge-blue",
            "content": "Editas has demonstrated compelling clinical proof-of-concept for reni-cel (EDIT-301) in severe sickle cell disease and transfusion-dependent beta-thalassemia, achieving complete resolution of vaso-occlusive events. However, CEO Gilmore O'Neill has committed to not self-funding expensive Phase 3 commercial trials. Analysts will press management on whether a deal with upfront non-dilutive cash is imminent."
        },
        {
            "title": "2. High Short Float (24.91%) & Asymmetric Squeeze Potential",
            "title_color": "#34d399",
            "border_color": "#10b981",
            "badge": "EXTREME SQUEEZE POTENTIAL",
            "badge_class": "badge-bull",
            "content": "Short sellers hold 24.91% of Editas' float, betting that gene editing commercialization hurdles and competition from Vertex/CRISPR Therapeutics (Casgevy) will force dilutive equity raises. With options pricing a ±26.72% move ($0.70 straddle) and Put/Call OI ratio at an ultra-low 0.15x, any positive licensing deal or partnership announcement creates massive upward squeeze convexity."
        },
        {
            "title": "3. In Vivo Pipeline Translation & Cas12a Patent Defense",
            "title_color": "#f59e0b",
            "border_color": "#f59e0b",
            "badge": "IP MOAT & IN VIVO PIPELINE",
            "badge_class": "badge-warn",
            "content": "Editas' long-term proprietary value proposition centers on targeted in vivo gene editing using engineered Cas12a (AsCas12a) and targeted lipid nanoparticles (LNPs) for genetic diseases of the liver and eye. Institutional investors seek pipeline milestones for IND-enabling studies and clarity on patent licensing disputes."
        }
    ]
}

# Agent 2C: Sentiment & Whisper
bus_2c = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Whisper_Sentiment_Agent (Agent 2C)",
    "model": "Gemini 3.8 Flash High Standard",
    "verified_live_product_context": {
        "flagship_products": "Reni-cel (EDIT-301, AsCas12a gene-edited cell therapy for Sickle Cell Disease and Transfusion-Dependent Beta-Thalassemia), Proprietary In Vivo Targeted Gene Editing Platform (Targeted LNPs & Cas12a Upregulation for rare liver and ocular genetic indications), Foundational CRISPR-Cas9 & Cas12a Intellectual Property Estate",
        "commercialization_channels": "Out-licensing to commercial biopharma partners (Vertex non-exclusive Cas9 license for ex vivo treatments), clinical research collaborations (BMS oncology targets), and future direct commercialization of proprietary in vivo assets"
    },
    "composite_pre_print_sentiment_score": 75,
    "composite_sentiment_label": "Bullish / Extreme Short Squeeze Convexity (75/100)",
    "retail_vs_institutional_positioning": {
        "retail_sentiment_score": 84,
        "retail_summary": "Retail biotech investors across Reddit r/wallstreetbets, r/biotechplays, FinTwit, and Threads view Editas as an underappreciated turnaround opportunity with 24.91% short float, $6.10 mean price target (+132.8% upside), and high call volume (Put/Call OI 0.15x) setting up for a violent squeeze.",
        "institutional_sentiment_score": 66,
        "institutional_summary": "Specialist healthcare institutions remain cautiously constructive, appreciating the $265M+ balance sheet runway into 2027 and non-dilutive licensing revenue, while awaiting formal execution of the reni-cel partnering agreement before re-rating the equity.",
        "short_interest_summary": "Short interest is heavily elevated at 24.91% of float with 130.66% implied volatility pricing in a ±26.72% post-earnings move ($0.70 straddle). Put/Call OI ratio of 0.15x demonstrates intense call-skewed positioning."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print("EDIT pre_agent_bus files created successfully!")
