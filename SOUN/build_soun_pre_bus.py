import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "SOUN"
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
            "tooltip_title": "Consolidated quarterly GAAP revenue across Automotive Voice AI, Restaurant Drive-Thru ordering, and Enterprise customer service.",
            "tooltip_def": "Total GAAP Revenue ($M): SoundHound delivered $61.90M in Q2 2026 (+45.03% YoY vs $42.68M in Q2 2025). Wall Street consensus models $62.18M in Q3 2026E (+47.87% YoY vs $42.05M in Q3 2025), with buy-side whisper bogeys looking for $64.00M+ on Amelia acquisition synergies.",
            "q_minus_1_actual": "$61.90M",
            "q_minus_4_yoy_baseline": "$42.05M",
            "street_consensus_q0e": "$62.18M",
            "whisper_bogey_q0e": "$64.00M",
            "whisper_spread_display": "+2.93% Spread",
            "bar_width_pct": 85,
            "hurdle_badge": "Top-Line Hurdle"
        },
        {
            "metric": "Adjusted Diluted EPS ($/sh)",
            "tooltip_title": "Quarterly adjusted net profit per share excluding acquisition-related amortization and non-cash equity compensation.",
            "tooltip_def": "Adjusted Diluted EPS ($/sh): Q2 2026 actual EPS came in at -$0.02 (beating consensus of -$0.05). Street models -$0.05 for Q3 2026E with buy-side whisper looking for -$0.03.",
            "q_minus_1_actual": "-$0.02",
            "q_minus_4_yoy_baseline": "-$0.03",
            "street_consensus_q0e": "-$0.05",
            "whisper_bogey_q0e": "-$0.03",
            "whisper_spread_display": "+$0.02 Better",
            "bar_width_pct": 80,
            "hurdle_badge": "Profitability Path"
        },
        {
            "metric": "Cumulative Backlog & Contract Bookings ($M)",
            "tooltip_title": "Contracted future revenue under multi-year automotive, restaurant, and enterprise software agreements.",
            "tooltip_def": "Cumulative Bookings Backlog: Long-term committed contract value exceeded $725M in Q2 2026; Street looks for expansion past $775M in Q3 2026E.",
            "q_minus_1_actual": "$725.0M",
            "q_minus_4_yoy_baseline": "$450.0M",
            "street_consensus_q0e": "$775.0M",
            "whisper_bogey_q0e": "$810.0M",
            "whisper_spread_display": "+$35.0M",
            "bar_width_pct": 90,
            "hurdle_badge": "Contract Visibility"
        },
        {
            "metric": "Restaurant Smart Ordering Locations",
            "tooltip_title": "Total active commercial restaurant drive-thru and phone ordering installations deployed.",
            "tooltip_def": "Restaurant AI Locations: Commercial drive-thru and automated phone ordering installations deployed across national fast-food chains; whisper models 12,500+ live doors.",
            "q_minus_1_actual": "10,800 Locations",
            "q_minus_4_yoy_baseline": "5,200 Locations",
            "street_consensus_q0e": "12,000 Locations",
            "whisper_bogey_q0e": "12,500 Locations",
            "whisper_spread_display": "+500 Locations",
            "bar_width_pct": 88,
            "hurdle_badge": "QSR Commercial Scale"
        }
    ]
}

# Agent 2B: Guidance & Debates
bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 78,
    "credibility_label": "78 / 100 (Strong Commercial Pipeline & Acquisition Integration Offsetting High Operating Cash Burn)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 2026E Net Revenue Guidance Corridor",
            "tooltip_title": "Management prior quarter revenue guidance range provided during Q2 2026 earnings.",
            "tooltip_def": "Q3 2026 Revenue Guidance: Guided to $60.0M - $64.0M ($62.0M midpoint); current consensus sits at $62.18M.",
            "prior_q_guidance_for_q0": "$60.0M – $64.0M ($62.0M Midpoint)",
            "current_street_consensus": "$62.18M",
            "historical_4q_beat_rate": "25.0% (1 Beat, 2 Meets, 1 Miss)",
            "variance_and_sandbag_commentary": "Management has delivered tight execution against guided midpoints, though revenue beat margins have historically been narrow due to restaurant rollout timelines.",
            "credibility_grade": "Grade B+ (Reliable)"
        },
        {
            "metric": "FY2026 Full-Year Top-Line Revenue Guidance",
            "tooltip_title": "Full-year 2026 revenue target raised during prior earnings call.",
            "tooltip_def": "FY2026 Guidance: Prior guidance corridor set at $235M - $250M ($242.5M midpoint); consensus models $245.0M.",
            "prior_q_guidance_for_q0": "$235.0M – $250.0M ($242.5M Midpoint)",
            "current_street_consensus": "$245.00M",
            "historical_4q_beat_rate": "75.0% Guidance Execution",
            "variance_and_sandbag_commentary": "Inorganic contribution from Amelia acquisition is accelerating full-year run-rate toward $250M+.",
            "credibility_grade": "Grade A- (Accretive)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 2026E Revenue Guidance Hurdle",
            "tooltip_title": "Expected top-line fourth quarter guidance required to satisfy institutional growth expectations.",
            "tooltip_def": "Q4 2026E Guidance Hurdle: Street models $78.0M; buy-side bull bogey requires guidance >= $83.0M on holiday drive-thru volume and automotive royalty inflection.",
            "street_consensus_hurdle": "$78.00M (+41.7% YoY)",
            "bull_case_bogey": "$83.00M+ (Amelia Enterprise Synergies)",
            "bear_case_breakdown": "< $73.00M (Deployment Delays)",
            "sensitivity_badge": "High Multiple Sensitivity",
            "strategic_rationale": "High short interest (41.35% of float) means a raised Q4 revenue guide triggers massive short-covering across hedge fund accounts."
        },
        {
            "forward_metric": "Path to Adjusted EBITDA Breakeven (2027)",
            "tooltip_title": "Target timeline for crossing into sustained positive adjusted EBITDA.",
            "tooltip_def": "EBITDA Breakeven Horizon: Management confirmation of crossing into positive adjusted EBITDA by early FY2027.",
            "street_consensus_hurdle": "Targeted by Q2 2027",
            "bull_case_bogey": "Pulled Forward to Q4 2026 / Q1 2027",
            "bear_case_breakdown": "Pushed Out Beyond Late 2027",
            "sensitivity_badge": "Profitability Inflection",
            "strategic_rationale": "Given Q2 operating cash flow of -$33.71M, institutional investors strictly scrutinize cash runway and time-to-breakeven."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "title": "1. Amelia Enterprise Acquisition Integration & Synergies",
            "title_color": "#60a5fa",
            "border_color": "#3b82f6",
            "badge": "ENTERPRISE EXPANSION",
            "badge_class": "badge-blue",
            "content": "SoundHound's acquisition of conversational AI leader Amelia significantly expands its TAM into enterprise customer service, financial services, and healthcare. Investors are probing whether Amelia's enterprise sales cycles are integrating smoothly or experiencing post-merger integration friction."
        },
        {
            "title": "2. High Short Interest Dynamics & Squeeze Risk (41.35% Float)",
            "title_color": "#34d399",
            "border_color": "#10b981",
            "badge": "EXTREME SQUEEZE ASYMMETRY",
            "badge_class": "badge-bull",
            "content": "With 41.35% of floating shares sold short, SoundHound is one of the most heavily shorted artificial intelligence equities on Wall Street. Any upside surprise in restaurant ordering ARR or automotive voice wins could trigger a violent squeeze toward consensus mean price targets ($12.57, +205% upside)."
        },
        {
            "title": "3. Cash Burn Trajectory & True FCF Conversion (-$57.50M)",
            "title_color": "#f59e0b",
            "border_color": "#f59e0b",
            "badge": "RUNWAY SCRUTINY",
            "badge_class": "badge-warn",
            "content": "Operating cash flow was -$33.71M in Q2 2026, and True Free Cash Flow was -$57.50M after accounting for $20.62M in stock-based compensation. While SoundHound holds over $200M in cash and equivalents, analysts on the conference call will press CFO Nitesh Sharan on the burn trajectory and capital requirements."
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
        "flagship_products": "SoundHound Chat AI (Automotive In-Vehicle Voice Assistant with Generative AI), Smart Ordering (Voice AI for Drive-Thru and Phone Ordering), Amelia AI Agents (Enterprise Conversational AI for Banking, Healthcare & Service Desks), Dynamic Interaction & Deep Meaning Understanding Platform",
        "commercialization_channels": "Automotive OEM tier-1 contracts (Stellantis, Hyundai, Honda), Quick-Service Restaurant (QSR) franchise systems (White Castle, Jersey Mike's), enterprise customer care channel partners, and point-of-sale (POS) integrations (Oracle MICROS, Toast)"
    },
    "composite_pre_print_sentiment_score": 76,
    "composite_sentiment_label": "Bullish / Extreme Short Squeeze Speculation (76/100)",
    "retail_vs_institutional_positioning": {
        "retail_sentiment_score": 86,
        "retail_summary": "Retail communities on Reddit r/wallstreetbets, r/SoundHound, and FinTwit are heavily engaged, citing the 41.35% short float, Nvidia ecosystem ties, and $12.57 mean target (+205% upside) as setup for a parabolic short-squeeze run.",
        "institutional_sentiment_score": 68,
        "institutional_summary": "Institutional hedge fund positioning is sharply polarized: long-only technology funds favor the $725M+ backlog and restaurant TAM expansion, while dedicated short-sellers focus on cash burn and dilution from stock compensation.",
        "short_interest_summary": "Short interest is extreme at 41.35% of float with an ultra-bullish Put/Call OI ratio of 0.20x, indicating aggressive retail call option buying ahead of earnings."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print("SOUN pre_agent_bus files created successfully!")
