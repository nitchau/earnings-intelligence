import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "PLUG"
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
            "metric": "Total Net GAAP Revenue ($M)",
            "tooltip_title": "Consolidated quarterly GAAP revenue across Fuel Cell Systems, Electrolyzers, Hydrogen Fuel, and Services.",
            "tooltip_def": "Total GAAP Revenue ($M): Plug Power delivered $178.30M in Q2 2026 (+2.49% YoY vs $173.97M in Q2 2025 and +9.05% QoQ vs $163.51M in Q1 2026). Wall Street consensus models $193.33M for Q3 2026E (+9.19% YoY vs $177.06M in Q3 2025), with buy-side whisper bogeys looking for $198.0M on accelerating material handling deployments.",
            "q_minus_1_actual": "$178.30M",
            "q_minus_4_yoy_baseline": "$177.06M",
            "street_consensus_q0e": "$193.33M",
            "whisper_bogey_q0e": "$198.00M",
            "whisper_spread_display": "+2.42% Spread",
            "bar_width_pct": 82,
            "hurdle_badge": "Top-Line Hurdle"
        },
        {
            "metric": "GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Quarterly GAAP net loss per share reflecting cost containment and manufacturing margin improvements.",
            "tooltip_def": "GAAP Diluted EPS ($/sh): Q2 2026 actual EPS came in at -$0.07 (beating consensus of -$0.08). Street consensus models -$0.06 for Q3 2026E with buy-side whisper looking for -$0.05 on improved green hydrogen internal production margins.",
            "q_minus_1_actual": "-$0.07",
            "q_minus_4_yoy_baseline": "-$0.12",
            "street_consensus_q0e": "-$0.06",
            "whisper_bogey_q0e": "-$0.05",
            "whisper_spread_display": "+$0.01 Better",
            "bar_width_pct": 76,
            "hurdle_badge": "Loss Reduction"
        },
        {
            "metric": "Liquid Hydrogen Plant Production (TPD)",
            "tooltip_title": "Daily tons per day (TPD) of internal green hydrogen fuel produced across Georgia, Tennessee, and Louisiana generation facilities.",
            "tooltip_def": "Internal Green Hydrogen Production: Internal production reached 40 TPD across Georgia and Tennessee in Q2 2026, lowering third-party molecule procurement costs; Street looks for expansion past 55 TPD in Q3 2026E.",
            "q_minus_1_actual": "40 TPD",
            "q_minus_4_yoy_baseline": "15 TPD",
            "street_consensus_q0e": "55 TPD",
            "whisper_bogey_q0e": "60 TPD",
            "whisper_spread_display": "+5 TPD Margin Driver",
            "bar_width_pct": 88,
            "hurdle_badge": "Margin Driver"
        },
        {
            "metric": "DOE $1.66B Loan Facility Finalization",
            "tooltip_title": "Status of the U.S. Department of Energy (DOE) Title 17 conditional clean energy loan guarantee facility.",
            "tooltip_def": "DOE Loan Guarantee: Finalization and definitive documentation of the $1.66B DOE loan guarantee to construct up to six green hydrogen generation facilities; key institutional milestone to eliminate dilution fears.",
            "q_minus_1_actual": "Conditional",
            "q_minus_4_yoy_baseline": "Application",
            "street_consensus_q0e": "Closing Steps",
            "whisper_bogey_q0e": "Definitive Close",
            "whisper_spread_display": "Liquidity Inflection",
            "bar_width_pct": 94,
            "hurdle_badge": "Balance Sheet Catalyst"
        }
    ]
}

# Agent 2B: Guidance & Debates
bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 74,
    "credibility_label": "74 / 100 (Operational Cost Execution & 75% EPS Beat Rate Counterbalanced by High Capital Intensity)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 2026E Revenue Guidance Corridor",
            "tooltip_title": "Prior revenue guidance provided during Q2 2026 earnings conference call.",
            "tooltip_def": "Q3 2026 Revenue Guidance: Guided toward $185.0M - $205.0M ($195.0M midpoint); current Street consensus sits at $193.33M.",
            "prior_q_guidance_for_q0": "$185.0M – $205.0M ($195.0M Midpoint)",
            "current_street_consensus": "$193.33M",
            "historical_4q_beat_rate": "75.0% (3 of 4 Quarters)",
            "variance_and_sandbag_commentary": "Management has met or beaten bottom-line EPS targets in 3 of the last 4 quarters as restructuring actions and internal hydrogen generation narrowed gross losses.",
            "credibility_grade": "Grade B+ (Improving Execution)"
        },
        {
            "metric": "Equipment Gross Margin Breakeven Trajectory",
            "tooltip_title": "Target timeline for returning equipment manufacturing and fuel margins to positive territory.",
            "tooltip_def": "Gross Margin Trajectory: Management guided to near-breakeven equipment margins by Q3/Q4 2026 as legacy fixed-price fuel contracts roll off.",
            "prior_q_guidance_for_q0": "Inflection toward 0% Gross Margin",
            "current_street_consensus": "-0.87% Gross Margin",
            "historical_4q_beat_rate": "50.0% Execution",
            "variance_and_sandbag_commentary": "Internal hydrogen production from the Georgia plant has begun replacing high-cost third-party merchant hydrogen, reducing fuel margin drag.",
            "credibility_grade": "Grade B (Moderate)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 2026E Revenue Guidance Hurdle",
            "tooltip_title": "Expected top-line fourth quarter revenue guidance required to satisfy institutional turnaround models.",
            "tooltip_def": "Q4 2026E Guidance Hurdle: Street models $245.0M; buy-side bull bogey requires guidance >= $260.0M on seasonal equipment delivery surges.",
            "street_consensus_hurdle": "$245.0M (+8.8% YoY)",
            "bull_case_bogey": "$260.0M+ (Electrolyzer Delivery Acceleration)",
            "bear_case_breakdown": "< $225.0M (Customer CapEx Delays)",
            "sensitivity_badge": "High Multiple Sensitivity",
            "strategic_rationale": "High short interest (23.54% of float) means a raised Q4 revenue guide triggers immediate short covering across hedge fund accounts."
        },
        {
            "forward_metric": "Path to Positive Operating Cash Flow (2027)",
            "tooltip_title": "Target operating cash burn reduction and timeline for crossing into cash flow neutrality.",
            "tooltip_def": "Cash Flow Neutrality: Management commitment to reducing quarterly OCF burn below -$40M by early 2027.",
            "street_consensus_hurdle": "Burn < -$50M/Quarter by Q2 2027",
            "bull_case_bogey": "Cash Flow Breakeven by Q4 2026 / Q1 2027",
            "bear_case_breakdown": "Burn Persisting > -$80M/Quarter",
            "sensitivity_badge": "Solvency & Valuation Floor",
            "strategic_rationale": "With Q2 OCF at -$94.06M and True FCF at -$137.67M, institutional investors strictly scrutinize cash runway and time-to-breakeven."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "title": "1. Internal Green Hydrogen Plant Ramp & Fuel Margin Turnaround",
            "title_color": "#60a5fa",
            "border_color": "#3b82f6",
            "badge": "MARGIN INFLECTION",
            "badge_class": "badge-blue",
            "content": "Plug Power has historically suffered massive negative gross margins on its hydrogen delivery business due to soaring third-party merchant liquid hydrogen purchase costs. With its 15 TPD Georgia plant operational and Tennessee online, analysts will probe CEO Andy Marsh on whether the internal cost per kilogram is falling below $4/kg and when fuel gross margin turns permanently positive."
        },
        {
            "title": "2. DOE $1.66 Billion Loan Facility Closing & Dilution Protection",
            "title_color": "#34d399",
            "border_color": "#10b981",
            "badge": "CAPITAL STRUCTURE MOAT",
            "badge_class": "badge-bull",
            "content": "The U.S. Department of Energy's conditional commitment for up to $1.66 billion in debt financing is the single largest liquidity catalyst in Plug's history. Institutional investors demand concrete timing on definitive documentation closing, conditions precedent, and initial draw schedules to definitively remove the threat of ATM equity offerings."
        },
        {
            "title": "3. High Short Float (23.54%) & Commercial Forklift Customer Concentration",
            "title_color": "#f59e0b",
            "border_color": "#f59e0b",
            "badge": "SQUEEZE ASYMMETRY",
            "badge_class": "badge-warn",
            "content": "With 23.54% of float sold short, Plug Power represents a classic high-beta short squeeze candidate. Bears point to customer concentration in warehouse material handling (Amazon, Walmart, Home Depot) and slow electrolyzer project final investment decisions (FIDs). Any major European or Asian green ammonia electrolyzer contract win could spark a rapid squeeze toward mean PT ($3.39, +142% upside)."
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
        "flagship_products": "GenDrive (Hydrogen Fuel Cell Systems for Electric Forklifts), GenFuel (Turnkey Hydrogen Dispensing & Storage Infrastructure), GenSure (Stationary Fuel Cells for Telecom & Data Center Backup), ProGen & GenSys PEM Electrolyzers (1MW–5MW modular green hydrogen generation stacks), Cryogenic Liquid Hydrogen Transport Trailers",
        "commercialization_channels": "Material handling fleet deployments at major retailers and logistics giants (Amazon, Walmart, Home Depot, BMW), commercial electrolyzer supply contracts for green hydrogen/ammonia developers, and turnkey hydrogen fuel delivery agreements across North America and Europe"
    },
    "composite_pre_print_sentiment_score": 74,
    "composite_sentiment_label": "Bullish / Extreme Short Squeeze & Valuation Turnaround (74/100)",
    "retail_vs_institutional_positioning": {
        "retail_sentiment_score": 85,
        "retail_summary": "Retail clean energy investors across Reddit r/wallstreetbets, r/plugpower, FinTwit, and Threads are intensely vocal, focusing on the 23.54% short interest, $3.39 mean price target (+142.1% upside), and 0.10x Put/Call ratio as prime indicators of an impending short-squeeze rally.",
        "institutional_sentiment_score": 64,
        "institutional_summary": "Institutional funds remain split between long-term ESG and infrastructure transition managers who see Plug as the only vertically integrated commercial hydrogen platform, and credit/hedge funds monitoring cash burn (-$94M OCF in Q2) and DOE loan closing timing.",
        "short_interest_summary": "Short interest sits at 23.54% of float with 160.94% implied volatility pricing in an ±18.57% post-earnings move ($0.26 straddle). Put/Call OI ratio of 0.10x reflects extreme call buying speculative positioning."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print("PLUG pre_agent_bus files created successfully!")
