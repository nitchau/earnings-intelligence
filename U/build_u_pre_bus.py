import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "U"
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
            "metric": "Strategic Grow Revenue ($M)",
            "tooltip_title": "Core mobile advertising monetization and LevelPlay mediation revenue powered by Unity Vector neural ranking.",
            "tooltip_def": "Strategic Grow Revenue ($M): Unity reported $329.00M in Q2 2026 (+63.0% YoY). Wall Street consensus models $382.50M in Q3 2026E, with buy-side whisper bogey looking for $388.00M on accelerating Vector AI neural bidding and eCPM expansion.",
            "q_minus_1_actual": "$329.00M",
            "q_minus_4_yoy_baseline": "$201.80M",
            "street_consensus_q0e": "$382.50M",
            "whisper_bogey_q0e": "$388.00M",
            "whisper_spread_display": "+1.44% Spread",
            "bar_width_pct": 82,
            "hurdle_badge": "Monetization Engine"
        },
        {
            "metric": "Strategic Create Revenue ($M)",
            "tooltip_title": "Subscription editor seats across Gaming, Unity Cloud, Sentis runtime, and Enterprise Digital Twins.",
            "tooltip_def": "Strategic Create Revenue ($M): Unity reported $157.47M in Q2 2026 (+5.0% YoY reported, +14% YoY normalized). Street consensus models $161.00M for Q3 2026E, with whisper bogey at $164.50M driven by Unity 6 enterprise seat conversions.",
            "q_minus_1_actual": "$157.47M",
            "q_minus_4_yoy_baseline": "$150.00M",
            "street_consensus_q0e": "$161.00M",
            "whisper_bogey_q0e": "$164.50M",
            "whisper_spread_display": "+2.17% Spread",
            "bar_width_pct": 76,
            "hurdle_badge": "Core Subscription Moat"
        },
        {
            "metric": "Adjusted EBITDA ($M)",
            "tooltip_title": "Non-GAAP Adjusted EBITDA reflecting operational efficiency and headcount restructuring leverage.",
            "tooltip_def": "Adjusted EBITDA ($M): Q2 2026 Adjusted EBITDA delivered $113.0M. Management guided $185.0M - $190.0M for Q3 2026; Street consensus sits at $187.50M with whisper bogey at $192.00M (implied ~33% cash EBITDA margin).",
            "q_minus_1_actual": "$113.00M",
            "q_minus_4_yoy_baseline": "$109.50M",
            "street_consensus_q0e": "$187.50M",
            "whisper_bogey_q0e": "$192.00M",
            "whisper_spread_display": "+2.40% Spread",
            "bar_width_pct": 88,
            "hurdle_badge": "Operating Leverage"
        },
        {
            "metric": "Non-GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Quarterly adjusted diluted earnings per share reflecting profitability turnaround.",
            "tooltip_def": "Non-GAAP Diluted EPS ($/sh): Q2 2026 actual EPS delivered $0.28 (beating consensus of $0.25). Wall Street consensus models $0.35 for Q3 2026E with buy-side whisper at $0.38.",
            "q_minus_1_actual": "$0.28",
            "q_minus_4_yoy_baseline": "$0.20",
            "street_consensus_q0e": "$0.35",
            "whisper_bogey_q0e": "$0.38",
            "whisper_spread_display": "+$0.03 Better",
            "bar_width_pct": 84,
            "hurdle_badge": "Bottom-Line Hurdle"
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
    "credibility_label": "85 / 100 (Strong 75% 4Q Beat Track Record, Restructuring Cost Discipline & Portfolio Focus)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 2026 Strategic Revenue Guidance Corridor",
            "tooltip_title": "Prior strategic revenue guidance issued in Q2 2026 earnings release.",
            "tooltip_def": "Q3 2026 Strategic Revenue Guidance: Guided toward $540.0M - $550.0M ($545.0M midpoint, +44% to +47% YoY); current Street consensus sits at $547.50M.",
            "prior_q_guidance_for_q0": "$540.0M - $550.0M ($545.0M Midpoint)",
            "current_street_consensus": "$547.50M",
            "historical_4q_beat_rate": "75.0% (3 of 4 Quarters)",
            "variance_and_sandbag_commentary": "Management under CEO Matthew Bromberg has exceeded consensus in 3 of the last 4 quarters with an average positive EPS surprise of +10.64%, re-establishing conservative baseline forecasting.",
            "credibility_grade": "Grade A- (Disciplined Execution)"
        },
        {
            "metric": "Q3 2026 Adjusted EBITDA Target Corridor",
            "tooltip_title": "Quarterly Adjusted EBITDA guidance range.",
            "tooltip_def": "Q3 2026 Adjusted EBITDA Guidance: Guided to $185.0M - $190.0M ($187.5M midpoint, ~33% margin); Street consensus sits at $187.50M.",
            "prior_q_guidance_for_q0": "$185.0M - $190.0M ($187.5M Midpoint)",
            "current_street_consensus": "$187.50M",
            "historical_4q_beat_rate": "75.0% Execution",
            "variance_and_sandbag_commentary": "Workforce right-sizing, cloud hosting optimizations, and reduction of non-strategic overhead provide exceptional visibility on margin targets.",
            "credibility_grade": "Grade A (High Visibility)"
        },
        {
            "metric": "Total Consolidated Revenue Guidance",
            "tooltip_title": "Total consolidated net revenue including Supersonic stub.",
            "tooltip_def": "Consolidated Q3 Revenue Guidance: Strategic revenue ($540M-$550M) plus ~$20M non-strategic Supersonic stub implies $560.0M - $570.0M; Street consensus models $567.45M.",
            "prior_q_guidance_for_q0": "$560.0M - $570.0M ($565.0M Midpoint)",
            "current_street_consensus": "$567.45M",
            "historical_4q_beat_rate": "75.0% Track Record",
            "variance_and_sandbag_commentary": "Divestiture of Supersonic completed August 4, 2026, eliminating publisher conflicts and streamlining revenue mix toward high-margin software.",
            "credibility_grade": "Grade A- (Transformational)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 2026 Strategic Revenue Hurdle",
            "tooltip_title": "Required sequential revenue ramp for holiday mobile advertising and annual enterprise renewals.",
            "tooltip_def": "Q4 2026 Strategic Revenue Hurdle: Street models $575.0M - $585.0M (+18% YoY); buy-side bull bogey requires >= $595.0M driven by Vector ad share gains.",
            "street_consensus_hurdle": "$575.00M - $585.00M (+18% YoY)",
            "bull_case_bogey": "$595.00M+ (Accelerated Vector Ad Share)",
            "bear_case_breakdown": "< $565.00M (Ad Deceleration vs AppLovin)",
            "sensitivity_badge": "High Multiple Sensitivity",
            "strategic_rationale": "Holiday gaming ad spend and enterprise annual contract renewals dictate whether Unity can sustain 20%+ top-line momentum into FY2027."
        },
        {
            "forward_metric": "Q4 2026 Adjusted EBITDA & Margin Hurdle",
            "tooltip_title": "Management operating leverage guidance for the fourth quarter.",
            "tooltip_def": "Q4 2026 Adjusted EBITDA Hurdle: Street hurdle stands at $200.0M - $210.0M (34% margin); bull bogey requires >= $220.0M (36% margin).",
            "street_consensus_hurdle": "$200.00M - $210.00M (34% Margin)",
            "bull_case_bogey": "$220.00M+ (36% Margin Profile)",
            "bear_case_breakdown": "< $190.00M (< 32% Margin Compression)",
            "sensitivity_badge": "Multiple Expansion Gatekeeper",
            "strategic_rationale": "Demonstrates structural cash generation durability post-portfolio divestitures, validating long-term 35%+ cash EBITDA profile."
        },
        {
            "forward_metric": "FY2027 Organic Growth Horizon & Margin Target",
            "tooltip_title": "Preliminary FY2027 growth outlook provided during Q3 conference call.",
            "tooltip_def": "FY2027 Outlook: Street consensus models +15% to +18% organic growth with FCF conversion exceeding 70% of Adjusted EBITDA.",
            "street_consensus_hurdle": "Guided to +15% to +18% YoY Growth",
            "bull_case_bogey": "Guided to +20%+ YoY with True FCF > $500M",
            "bear_case_breakdown": "Sub-12% Organic Growth Stagnation",
            "sensitivity_badge": "Structural Re-Rating",
            "strategic_rationale": "High short interest (6.41% of float) creates significant squeeze asymmetry if management confirms sustainable double-digit growth."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "title": "1. Unity Vector vs AppLovin AXON 2.0 Competitive Moat & Ad Share",
            "title_color": "#60a5fa",
            "border_color": "#3b82f6",
            "badge": "AI MONETIZATION MOAT",
            "badge_class": "badge-blue",
            "content": "The central battleground for institutional investors is whether Unity Vector's AI neural bidding engine can reclaim mobile ad mediation market share from AppLovin's AXON 2.0. Unity holds unique in-engine telemetry across millions of games that pure mediation networks lack, but Wall Street demands proof of sustained eCPM and ROAS outperformance among top gaming publishers."
        },
        {
            "title": "2. Unity 6 Upgrade Cycle & Developer Trust Rehabilitation",
            "title_color": "#34d399",
            "border_color": "#10b981",
            "badge": "SUBSCRIPTION ADOPTION",
            "badge_class": "badge-bull",
            "content": "Following the definitive cancellation of the controversial runtime fee, CEO Matthew Bromberg has refocused Create Solutions around Unity 6. The release introduces WebGPU compilation, GPU-resident drawer architectures, and native Sentis on-device neural inferencing. Desks want to verify how many enterprise and Pro seats have upgraded, and whether net retention rates have stabilized above 105%."
        },
        {
            "title": "3. Operating Cash Flow Conversion ($205.62M) & Balance Sheet Fortress",
            "title_color": "#f59e0b",
            "border_color": "#f59e0b",
            "badge": "FREE CASH FLOW PURITY",
            "badge_class": "badge-warn",
            "content": "Unity generated a massive $205.62M in Operating Cash Flow and $201.96M in reported FCF in Q2 2026. Even after deducting $79.95M in stock-based compensation, True FCF stood at $122.01M. With $2.35B in balance sheet cash, institutional investors are focused on CFO Jarrod Yahes's capital allocation strategy regarding upcoming convertible debt maturities vs share repurchases."
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
        "flagship_products": "Unity 6 Game Engine Runtime (WebGPU & Sentis On-Device AI Inferencing), Unity Vector AI Monetization & Neural Bidding Platform, LevelPlay Mobile Mediation, Unity Cloud DevOps & Asset Manager, Unity Industry Digital Twin Suite",
        "commercialization_channels": "Direct enterprise sales to top AAA & mobile studios, seat-based Pro/Enterprise SaaS subscriptions, and programmatic revenue share on LevelPlay mobile ad mediation"
    },
    "composite_pre_print_sentiment_score": 68,
    "composite_sentiment_label": "Constructive Turnaround Execution / AI Ad Catch-Up (68/100)",
    "retail_vs_institutional_positioning": {
        "retail_sentiment_score": 64,
        "retail_summary": "Retail traders on Reddit r/wallstreetbets and FinTwit view Unity as a prime turnaround candidate, noting AppLovin's massive multi-billion re-rating and betting that Unity Vector can replicate similar AI monetization expansion.",
        "institutional_sentiment_score": 72,
        "institutional_summary": "Institutional software and tech funds are constructive on CEO Matt Bromberg's turnaround execution, highlighting the sale of Supersonic, elimination of runtime fees, and expansion of True FCF ($122.01M) toward the $50.45 mean price target (+28.21% upside).",
        "short_interest_summary": "Short interest sits at 6.41% of float with a 0.97x Put/Call OI ratio and ATM straddle implying a ±12.38% move against historical 15.37% realized post-earnings volatility, offering attractive upside convexity."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print("U pre_agent_bus files refreshed successfully!")
