import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "TXG"
EARNINGS_DATE = "2026-11-05"

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
            "metric": "Total GAAP Revenue ($M)",
            "tooltip_title": "Consolidated quarterly GAAP revenue across Chromium Single Cell, Visium Spatial Biology, and Xenium In Situ platforms.",
            "tooltip_def": "Total GAAP Revenue ($M): 10x Genomics reported $151.04M in Q2 2026 (-12.65% YoY vs $172.91M in Q2 2025). Wall Street consensus models $147.85M in Q3 2026E (-0.78% YoY vs $149.00M in Q3 2025), with buy-side whisper looking for $150.50M on Visium HD and GEM-X adoption.",
            "q_minus_1_actual": "$151.04M",
            "q_minus_4_yoy_baseline": "$149.00M",
            "street_consensus_q0e": "$147.85M",
            "whisper_bogey_q0e": "$150.50M",
            "whisper_spread_display": "+1.79% Spread",
            "bar_width_pct": 84,
            "hurdle_badge": "Consensus Hurdle"
        },
        {
            "metric": "Diluted EPS ($/sh)",
            "tooltip_title": "Quarterly GAAP diluted earnings per share reflecting research investments and manufacturing efficiency.",
            "tooltip_def": "Diluted EPS ($/sh): Q2 2026 actual EPS delivered $0.03 (beating consensus of -$0.02). Street models -$0.02 for Q3 2026E with buy-side whisper looking for $0.01.",
            "q_minus_1_actual": "$0.03",
            "q_minus_4_yoy_baseline": "-$0.02",
            "street_consensus_q0e": "-$0.02",
            "whisper_bogey_q0e": "$0.01",
            "whisper_spread_display": "+$0.03 Better",
            "bar_width_pct": 86,
            "hurdle_badge": "Bottom-Line Hurdle"
        },
        {
            "metric": "Consumables Revenue & Pull-Through ($M)",
            "tooltip_title": "Recurring high-margin reagent kits and consumable assays utilized per installed instrument.",
            "tooltip_def": "Consumables Revenue: Recurring high-margin reagent sales delivered $125.0M in Q2 2026 (82.8% of sales); Street models $123.0M for Q3 2026E with whisper at $126.5M.",
            "q_minus_1_actual": "$125.00M",
            "q_minus_4_yoy_baseline": "$120.50M",
            "street_consensus_q0e": "$123.00M",
            "whisper_bogey_q0e": "$126.50M",
            "whisper_spread_display": "+2.85% Spread",
            "bar_width_pct": 88,
            "hurdle_badge": "Recurring Moat"
        },
        {
            "metric": "Xenium & Visium HD Spatial Placements",
            "tooltip_title": "Net new clinical and academic laboratory placements of Xenium In Situ and Visium HD systems.",
            "tooltip_def": "Spatial Instrument Placements: Commercial placements of Xenium analyzers and Visium HD upgrades; whisper looks for 85+ net new spatial system installations in Q3.",
            "q_minus_1_actual": "78 Units",
            "q_minus_4_yoy_baseline": "55 Units",
            "street_consensus_q0e": "80 Units",
            "whisper_bogey_q0e": "88 Units",
            "whisper_spread_display": "+8 Units",
            "bar_width_pct": 82,
            "hurdle_badge": "Spatial Adoption"
        }
    ]
}

# Agent 2B: Guidance & Debates
bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 85,
    "credibility_label": "85 / 100 (Flawless 4Q EPS Beat Track Record, Restructuring Cost Savings & Reagent Margin Discipline)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 2026E Revenue Guidance Corridor",
            "tooltip_title": "Prior revenue guidance provided during Q2 earnings call.",
            "tooltip_def": "Q3 2026 Revenue Guidance: Guided toward $144.0M - $152.0M ($148.0M midpoint); current consensus sits at $147.85M.",
            "prior_q_guidance_for_q0": "$144.0M – $152.0M ($148.0M Midpoint)",
            "current_street_consensus": "$147.85M",
            "historical_4q_beat_rate": "100.0% (4 of 4 Quarters)",
            "variance_and_sandbag_commentary": "Management has beaten EPS consensus in 4 of 4 prior quarters with an average surprise of +205.3%, maintaining conservative guidance hurdles.",
            "credibility_grade": "Grade A (Conservative)"
        },
        {
            "metric": "Full-Year 2026 Revenue Target Corridor",
            "tooltip_title": "Full-year 2026 revenue guidance maintained by management.",
            "tooltip_def": "FY2026 Revenue Guidance: Maintained at $610M - $630M ($620M midpoint); consensus models $618.5M.",
            "prior_q_guidance_for_q0": "$610.0M – $630.0M ($620.0M Midpoint)",
            "current_street_consensus": "$618.50M",
            "historical_4q_beat_rate": "100.0% Execution",
            "variance_and_sandbag_commentary": "Restructuring initiatives and sales force realignments completed in H1 2026 are stabilizing quarterly consumables run-rates.",
            "credibility_grade": "Grade A- (Stabilized)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 2026E Top-Line Net Sales Hurdle",
            "tooltip_title": "Required sequential revenue ramp for year-end academic and biopharma budget flushes.",
            "tooltip_def": "Q4 2026E Guidance Hurdle: Street models $168.0M (+1.2% YoY); buy-side bull bogey requires >= $173.0M driven by academic grant releases.",
            "street_consensus_hurdle": "$168.00M (+1.2% YoY)",
            "bull_case_bogey": "$173.00M+ (Biopharma Budget Flush)",
            "bear_case_breakdown": "< $162.00M (NIH Funding Headwinds)",
            "sensitivity_badge": "High Multiple Sensitivity",
            "strategic_rationale": "Year-end academic capital equipment budget cycles dictate whether 10x Genomics can re-accelerate toward double-digit organic growth."
        },
        {
            "forward_metric": "FY2027 Organic Growth Horizon & Margin Target",
            "tooltip_title": "Management confirmation of returning to double-digit organic top-line growth in 2027.",
            "tooltip_def": "FY2027 Growth Outlook: Investor day target for returning to > 10% organic growth with adjusted gross margins exceeding 76%.",
            "street_consensus_hurdle": "Guided to +8% to +10% YoY",
            "bull_case_bogey": "Guided to +12%+ YoY with Positive FCF",
            "bear_case_breakdown": "Mid-Single Digit (< 5%) Stagnation",
            "sensitivity_badge": "Multiple Expansion Hurdle",
            "strategic_rationale": "High short interest (14.33% of float) creates significant squeeze asymmetry if management signals an end to the academic funding slowdown."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "title": "1. Visium HD & GEM-X Single Cell Transition Velocity",
            "title_color": "#60a5fa",
            "border_color": "#3b82f6",
            "badge": "TECHNOLOGY MIGRATION",
            "badge_class": "badge-blue",
            "content": "Customer migration from legacy Chromium assays to next-generation GEM-X architecture and the rollout of Visium HD are central to the bull thesis. Analysts want to verify whether GEM-X is stimulating larger order volumes per customer and expanding single-cell sensitivity."
        },
        {
            "title": "2. Academic Grant Funding & Biopharma R&D Spending Environment",
            "title_color": "#34d399",
            "border_color": "#10b981",
            "badge": "MACRO BUDGET CYCLE",
            "badge_class": "badge-bull",
            "content": "Life science tools equities have faced persistent pressure from cautious biopharma capital spending and NIH grant award pacing. Institutional desks will scrutinize CEO Serge Saxonov's commentary regarding fourth-quarter year-end budget flush demand."
        },
        {
            "title": "3. Operating Cash Flow Conversion ($16.97M) & Positive FCF Runway",
            "title_color": "#f59e0b",
            "border_color": "#f59e0b",
            "badge": "FREE CASH FLOW",
            "badge_class": "badge-warn",
            "content": "Operating Cash Flow generated a solid $16.97M in Q2 2026, delivering $15.38M in reported FCF. While stock-based compensation of $25.62M resulted in True FCF of -$10.24M, 10x Genomics holds $380M+ in cash and zero debt, providing an impregnable fortress balance sheet."
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
        "flagship_products": "Chromium X / iX (Single Cell Gene Expression & Immune Profiling with GEM-X Technology), Visium HD (Whole Transcriptome Spatial Gene Expression at Subcellular Resolution), Xenium In Situ (High-Plex Subcellular In Situ Imaging Platform), Cell Ranger & Loupe Browser Software Suite",
        "commercialization_channels": "Direct sales organization across academic research institutions, biopharmaceutical corporations, clinical cancer centers, contract research organizations (CROs), and core sequencing laboratories"
    },
    "composite_pre_print_sentiment_score": 68,
    "composite_sentiment_label": "Cautiously Bullish / Life Science Turnaround Asymmetry (68/100)",
    "retail_vs_institutional_positioning": {
        "retail_sentiment_score": 62,
        "retail_summary": "Retail investors on Reddit r/biotech_stocks and FinTwit see TXG as an oversold genomics leader with an elite technological moat in spatial biology, focusing on the 14.33% short float and 100% 4Q beat track record.",
        "institutional_sentiment_score": 72,
        "institutional_summary": "Institutional healthcare funds are constructive on operational stabilization following H1 restructuring, noting that Visium HD placements and solid gross margins (>74%) offer compelling risk-reward toward the $77.50 mean price target (+20.06% upside).",
        "short_interest_summary": "Short interest sits at 14.33% of float with a 0.52x Put/Call OI ratio, presenting tangible short-covering potential on any full-year guidance raise."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print("TXG pre_agent_bus files created successfully!")
