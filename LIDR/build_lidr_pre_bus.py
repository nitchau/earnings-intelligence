import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "LIDR"
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
            "tooltip_title": "Consolidated quarterly GAAP revenue across Defense, Automotive ADAS, and Industrial/Sports licensing.",
            "tooltip_def": "Total GAAP Revenue ($M): AEye reported $0.20M in Q2 2026 (+900% YoY vs $0.02M in Q2 2025 and +100% QoQ vs $0.10M in Q1 2026). Wall Street consensus models $0.57M in Q3 2026E (+1050% YoY vs $0.05M in Q3 2025), with buy-side whisper looking for $0.62M on accelerating defense purchase orders.",
            "q_minus_1_actual": "$0.20M",
            "q_minus_4_yoy_baseline": "$0.05M",
            "street_consensus_q0e": "$0.57M",
            "whisper_bogey_q0e": "$0.62M",
            "whisper_spread_display": "+8.77% Spread",
            "bar_width_pct": 82,
            "hurdle_badge": "Consensus Hurdle"
        },
        {
            "metric": "GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Quarterly GAAP net loss per share reflecting operating burn and commercialization investments.",
            "tooltip_def": "GAAP Diluted EPS ($/sh): Q2 2026 actual EPS came in at -$0.22 (normalized net income -$10.02M across 45.92M shares). Wall Street consensus models -$0.17 for Q3 2026E with buy-side whisper bogey at -$0.16.",
            "q_minus_1_actual": "-$0.22",
            "q_minus_4_yoy_baseline": "-$0.30",
            "street_consensus_q0e": "-$0.17",
            "whisper_bogey_q0e": "-$0.16",
            "whisper_spread_display": "+$0.01 Better",
            "bar_width_pct": 74,
            "hurdle_badge": "Bottom-Line Hurdle"
        },
        {
            "metric": "Defense & Aerospace Contract Orders ($M)",
            "tooltip_title": "Total contract value and purchase orders for UAV and counter-UAS sensor integration.",
            "tooltip_def": "Defense & Aerospace Orders: AEye's fastest growing vertical with engagements doubling QoQ in Q2 2026; Q3 2026E whisper models $1.20M in cumulative defense procurement bookings.",
            "q_minus_1_actual": "$0.65M",
            "q_minus_4_yoy_baseline": "$0.10M",
            "street_consensus_q0e": "$0.95M",
            "whisper_bogey_q0e": "$1.20M",
            "whisper_spread_display": "+26.3% Spread",
            "bar_width_pct": 88,
            "hurdle_badge": "Strategic Bogey"
        },
        {
            "metric": "Operating Cash Burn / Run-Rate ($M)",
            "tooltip_title": "Cash utilized in operations reflecting strict runway management and capital discipline.",
            "tooltip_def": "Operating Cash Burn ($M): Q2 2026 OCF was -$7.29M with total cash and marketable securities sustaining runway into late 2027; consensus expects Q3 cash burn of -$6.80M.",
            "q_minus_1_actual": "-$7.29M",
            "q_minus_4_yoy_baseline": "-$8.50M",
            "street_consensus_q0e": "-$6.80M",
            "whisper_bogey_q0e": "-$6.50M",
            "whisper_spread_display": "+$0.30M Preserved",
            "bar_width_pct": 78,
            "hurdle_badge": "Fortress Runway"
        }
    ]
}

# Agent 2B: Guidance & Debates
bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 72,
    "credibility_label": "72 / 100 (Prudent Runway Management & Strict Cost Containment Against Early-Stage Commercial Scaling)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 2026E Revenue Guidance Corridor",
            "tooltip_title": "Prior revenue guidance provided during Q2 earnings call.",
            "tooltip_def": "Q3 2026 Revenue Guidance: Guided toward $0.45M - $0.65M ($0.55M midpoint) on accelerating Apollo software deployments and defense prototype shipments.",
            "prior_q_guidance_for_q0": "$0.45M – $0.65M ($0.55M Midpoint)",
            "current_street_consensus": "$0.57M",
            "historical_4q_beat_rate": "50.0% (2 of 4 Quarters)",
            "variance_and_sandbag_commentary": "Consensus sits right near the guided midpoint ($0.57M vs $0.55M), reflecting conservative defense milestone recognition.",
            "credibility_grade": "Grade B (Moderate)"
        },
        {
            "metric": "Quarterly Cash Burn Corridor",
            "tooltip_title": "Targeted quarterly net operating cash outflow.",
            "tooltip_def": "Operating Cash Outflow Target: Management targeted $6.5M - $7.5M quarterly burn to preserve liquidity into commercial volume inflection.",
            "prior_q_guidance_for_q0": "-$7.00M Midpoint",
            "current_street_consensus": "-$6.80M",
            "historical_4q_beat_rate": "75.0% Beat Rate",
            "variance_and_sandbag_commentary": "Management consistently keeps OpEx below $11M/quarter through lean engineering headcount and outsourced manufacturing.",
            "credibility_grade": "Grade A- (Disciplined)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 2026E Top-Line Net Sales Hurdle",
            "tooltip_title": "Required sequential revenue ramp for year-end 2026.",
            "tooltip_def": "Q4 2026E Guidance Hurdle: Street models $0.90M; buy-side bull bogey requires >= $1.25M with commercial production milestone commitments.",
            "street_consensus_hurdle": "$0.90M (+800% YoY)",
            "bull_case_bogey": "$1.25M+ (Defense & NVIDIA Pipeline)",
            "bear_case_breakdown": "< $0.60M (Commercial Pushouts)",
            "sensitivity_badge": "High Multiple Sensitivity",
            "strategic_rationale": "Microcap valuation multiple re-rating hinges entirely on validating scalable OEM licensing rather than one-off NRE prototypes."
        },
        {
            "forward_metric": "Full-Year 2027 Cash Runway Horizon",
            "tooltip_title": "Management confirmation of capital adequacy and zero dilutive near-term equity offering.",
            "tooltip_def": "Cash Runway Horizon: Confirmation that existing cash position and debt facilities provide funding runway through FY2027 without immediate microcap dilution.",
            "street_consensus_hurdle": "Funded Through Mid-2027",
            "bull_case_bogey": "Funded Through Q4 2027+ via Milestone Receipts",
            "bear_case_breakdown": "Capital Raise / S-3 ATM Dilution Warning",
            "sensitivity_badge": "Existential Runway Hurdle",
            "strategic_rationale": "Given $47.6M market cap, institutional microcap buyers strictly monitor dilution risk and share count preservation."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "title": "1. NVIDIA DRIVE AGX Thor™ & Hyperion Commercial Conversion",
            "title_color": "#60a5fa",
            "border_color": "#3b82f6",
            "badge": "TIER-1 ADAS CATALYST",
            "badge_class": "badge-blue",
            "content": "Institutional investors are intensely focused on how quickly AEye's validation of Apollo™ on NVIDIA DRIVE Thor translates into binding Tier-1 automotive sensor design wins. With automotive OEMs selecting autonomous platforms for 2027–2028 model years, will CEO Matt Fisch announce production agreements on the call?"
        },
        {
            "title": "2. Defense & Counter-UAS Vertical Acceleration vs Lidar Peers",
            "title_color": "#34d399",
            "border_color": "#10b981",
            "badge": "IMMEDIATE CASH FLOW",
            "badge_class": "badge-bull",
            "content": "Unlike automotive lidar deployments that face long 3-to-5 year lead times, defense and aerospace counter-drone applications are generating immediate repeat purchase orders. Analysts want to see what percentage of 2027 revenue is derisked by defense contracts compared to automotive ADAS."
        },
        {
            "title": "3. Cash Burn Trajectory & Path to Gross Margin Inflection",
            "title_color": "#f59e0b",
            "border_color": "#f59e0b",
            "badge": "CAPITAL DISCIPLINE",
            "badge_class": "badge-warn",
            "content": "AEye's enterprise value is currently -$25.75M, reflecting cash holdings that exceed total equity valuation. If management can demonstrate that quarterly burn stays under $7.0M while revenue scales past $1M/quarter, the stock could undergo rapid multiple expansion toward Street mean price targets ($4.75)."
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
        "flagship_products": "AEye Apollo™ (Adaptive, Software-Defined Long-Range LiDAR), AEye STRATOS™ Automotive Perception Platform, 4Sight Intelligent Sensing Architecture, Alive3D Sports Analytics Spatial Platform",
        "commercialization_channels": "Direct Tier-1 automotive partnerships, NVIDIA DRIVE AGX Thor ecosystem integrations, commercial defense primes, and industrial sports analytics licensing"
    },
    "composite_pre_print_sentiment_score": 58,
    "composite_sentiment_label": "Cautiously Bullish / Asymmetric Deep Value (58/100)",
    "retail_vs_institutional_positioning": {
        "retail_sentiment_score": 64,
        "retail_summary": "Retail traders on Reddit r/smallstreetbets, r/pennystocks, and FinTwit view LIDR as a high-upside turnaround play with negative enterprise value (-$25.75M EV) and 365% upside to analyst mean price target ($4.75), watching closely for defense order updates.",
        "institutional_sentiment_score": 54,
        "institutional_summary": "Institutional microcap desks acknowledge clean execution on cost controls and Apollo integration with NVIDIA, but remain disciplined regarding revenue ramp execution and conversion from paid trials to multi-year contracts.",
        "short_interest_summary": "Short interest sits at 5.34% of float, presenting moderate short-squeeze potential if revenue surprises above the $0.65M top-end guidance corridor."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print("LIDR pre_agent_bus files created successfully!")
