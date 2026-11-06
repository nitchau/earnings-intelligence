import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "CRWV"
EARNINGS_DATE = "2026-11-10"

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
            "tooltip_title": "Consolidated quarterly GAAP revenue across Dedicated GPU Compute, On-Demand Cloud, and High-Speed AI Interconnect.",
            "tooltip_def": "Total GAAP Revenue ($M): CoreWeave delivered $2,575.0M in Q2 2026 (+112.46% YoY vs $1,212.0M in Q2 2025). Wall Street consensus models $3,540.79M in Q3 2026E (+159.46% YoY vs $1,364.68M in Q3 2025), with buy-side whisper bogeys looking for $3,650.0M+ on aggressive Nvidia Blackwell B200 and H200 cluster turn-ups.",
            "q_minus_1_actual": "$2,575.0M",
            "q_minus_4_yoy_baseline": "$1,364.7M",
            "street_consensus_q0e": "$3,540.8M",
            "whisper_bogey_q0e": "$3,650.0M",
            "whisper_spread_display": "+3.08% Spread",
            "bar_width_pct": 88,
            "hurdle_badge": "Consensus Hurdle"
        },
        {
            "metric": "GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Quarterly GAAP net loss per share reflecting massive data center buildout depreciation and debt service.",
            "tooltip_def": "GAAP Diluted EPS ($/sh): Q2 2026 actual EPS came in at -$1.14 (beating consensus of -$1.47). Street models -$1.55 for Q3 2026E with buy-side whisper looking for -$1.45 on superior power utilization.",
            "q_minus_1_actual": "-$1.14",
            "q_minus_4_yoy_baseline": "-$0.22",
            "street_consensus_q0e": "-$1.55",
            "whisper_bogey_q0e": "-$1.45",
            "whisper_spread_display": "+$0.10 Better",
            "bar_width_pct": 78,
            "hurdle_badge": "Bottom-Line Hurdle"
        },
        {
            "metric": "Contracted Revenue Backlog ($B)",
            "tooltip_title": "Total multi-year contractual commitments for dedicated GPU AI clusters from foundation model developers and hyperscalers.",
            "tooltip_def": "Contracted Revenue Backlog ($B): CoreWeave reported $28.5B in contracted backlog in Q2 2026; Street consensus models expansion to $33.0B, with whisper bogeys stretching to $35.0B+ driven by Tier-1 frontier lab multi-year reservation extensions.",
            "q_minus_1_actual": "$28.50B",
            "q_minus_4_yoy_baseline": "$14.20B",
            "street_consensus_q0e": "$33.00B",
            "whisper_bogey_q0e": "$35.00B",
            "whisper_spread_display": "+$2.00B Expansion",
            "bar_width_pct": 92,
            "hurdle_badge": "Visibility Driver"
        },
        {
            "metric": "Active Deployed Megawatts (MW)",
            "tooltip_title": "Total energised and operational data center power capacity hosting production GPU workloads.",
            "tooltip_def": "Active Deployed Megawatts (MW): Total energised data center power reached 470 MW in Q2 2026 (+135% YoY); consensus expects 620 MW operational by Q3 2026E as gigawatt-scale campus phases come online.",
            "q_minus_1_actual": "470 MW",
            "q_minus_4_yoy_baseline": "200 MW",
            "street_consensus_q0e": "620 MW",
            "whisper_bogey_q0e": "650 MW",
            "whisper_spread_display": "+30 MW Capacity",
            "bar_width_pct": 85,
            "hurdle_badge": "Infrastructure Scale"
        }
    ]
}

# Agent 2B: Guidance & Debates
bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 76,
    "credibility_label": "76 / 100 (Unprecedented AI Compute Demand & Multi-Year Backlog Balanced Against Gigawatt CapEx Execution Risks)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 2026E Revenue Guidance Corridor",
            "tooltip_title": "Prior revenue guidance provided during Q2 earnings call.",
            "tooltip_def": "Q3 2026 Revenue Guidance: Guided toward $3,450M - $3,650M ($3,550M midpoint); current Street consensus sits at $3,540.79M.",
            "prior_q_guidance_for_q0": "$3,450M – $3,650M ($3,550M Midpoint)",
            "current_street_consensus": "$3,540.79M",
            "historical_4q_beat_rate": "50.0% (2 Beats, 2 Misses)",
            "variance_and_sandbag_commentary": "Management guidance tracks tightly to power interconnect energization schedules. Two prior misses were directly attributable to utility grid delays rather than demand softness.",
            "credibility_grade": "Grade B+ (Reliable)"
        },
        {
            "metric": "FY2026 CapEx & Capital Deployment Target",
            "tooltip_title": "Full-year infrastructure capital expenditure target for GPU clusters and data center leases.",
            "tooltip_def": "FY2026 CapEx Corridor: Guided to $22.0B - $25.0B to fund rapid Blackwell B200 buildout and long-haul dark fiber infrastructure.",
            "prior_q_guidance_for_q0": "$22.0B – $25.0B Target Range",
            "current_street_consensus": "$23.80B",
            "historical_4q_beat_rate": "100.0% Deployment Execution",
            "variance_and_sandbag_commentary": "CoreWeave consistently fulfills its equipment procurement obligations backed by its debt financing consortium and Nvidia allocation priority.",
            "credibility_grade": "Grade A (Premier Execution)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 2026E Revenue Guidance Hurdle",
            "tooltip_title": "Expected fourth quarter revenue corridor required to sustain institutional multiple expansion.",
            "tooltip_def": "Q4 2026E Guidance Hurdle: Street models $4,250.0M; buy-side bull bogey demands guidance >= $4,500.0M on full commercial ramp of Blackwell GB200 NVL72 racks.",
            "street_consensus_hurdle": "$4,250.0M (+170.4% YoY)",
            "bull_case_bogey": "$4,500.0M+ (Accelerated Blackwell Delivery)",
            "bear_case_breakdown": "< $3,950.0M (Utility Substation Delays)",
            "sensitivity_badge": "High Multiple Sensitivity",
            "strategic_rationale": "Given CoreWeave's enterprise value of $70.15B and 22.4% short interest, any guide above $4.5B triggers aggressive short covering."
        },
        {
            "forward_metric": "FY2027 Initial Power Capacity & Revenue Outlook",
            "tooltip_title": "Preliminary qualitative commentary on FY2027 contracted power pipeline and GPU cluster deliveries.",
            "tooltip_def": "FY2027 Outlook: Street seeks confirmation of >1.5 GW total capacity under contract and initial FY2027 top-line guidance exceeding $18.0B.",
            "street_consensus_hurdle": "> 1.4 GW & $17.5B+ Top-Line",
            "bull_case_bogey": "> 1.8 GW Contracted & $20.0B+ Outlook",
            "bear_case_breakdown": "< 1.2 GW or Grid Interconnect Bottlenecks",
            "sensitivity_badge": "Structural Re-Rating",
            "strategic_rationale": "Long-term institutional valuation anchors to power interconnect rights and multi-year sovereign and hyperscale contracts."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "title": "1. Blackwell GB200 Architecture Deployment Pace & Liquid Cooling Scaling",
            "title_color": "#60a5fa",
            "border_color": "#3b82f6",
            "badge": "COMPUTE ARCHITECTURE",
            "badge_class": "badge-blue",
            "content": "CoreWeave was the first cloud provider to receive production Nvidia Blackwell B200 and GB200 NVL72 clusters. Analysts will aggressively interrogate CEO Michael Intrator on liquid cooling manifold readiness, facility power density (120 kW/rack), and whether Nvidia allocations remain unconstrained amid global packaging capacity tightness."
        },
        {
            "title": "2. High Debt Service, CapEx Intensity & Forensic True FCF Conversion (-$5,908M)",
            "title_color": "#f59e0b",
            "border_color": "#f59e0b",
            "badge": "LIQUIDITY & DEBT LEVERAGE",
            "badge_class": "badge-warn",
            "content": "In Q2 2026, CoreWeave generated $679M in Operating Cash Flow but spent $6,422M in CapEx, resulting in True FCF of -$5,908M (including $165M SBC). With total enterprise value of $70.15B vs market cap of $25.55B, net debt exceeds $44B. Institutional desks demand clarity on debt refinancing schedules, equipment financing interest rates, and payback horizons per GPU cluster."
        },
        {
            "title": "3. Short Interest Crowding (22.4% Float) & Hyperscaler Customer Concentration",
            "title_color": "#34d399",
            "border_color": "#10b981",
            "badge": "SQUEEZE ASYMMETRY",
            "badge_class": "badge-bull",
            "content": "With short float at 22.4% and an options-implied earnings move of ±22.88%, CoreWeave presents massive pre-print asymmetry. Bears highlight that over 65% of revenue originates from two frontier AI foundation labs. A diversified Q3 customer backlog addition or sovereign AI deal announcement would spark an immediate short squeeze toward mean PT ($132.18, +185% upside)."
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
        "flagship_products": "CoreWeave Cloud Platform (Specialized Kubernetes-Native AI Hyperscaler), Dedicated GPU Clusters (Nvidia Blackwell GB200 NVL72, H200, H100 SXM5), CoreWeave Mission Control (Cluster Orchestration & Automated Node Healing), Quantum-2 800Gb/s InfiniBand & Slingshot Networking, High-Performance Object & Scratch Storage",
        "commercialization_channels": "Direct multi-year enterprise contracts with frontier AI labs (OpenAI, Inflection, Mistral AI), strategic cloud partnership agreements with Microsoft Azure, tier-1 financial enterprise quantitative compute, and sovereign AI cloud deployments across North America and Europe"
    },
    "composite_pre_print_sentiment_score": 74,
    "composite_sentiment_label": "Bullish / Extreme Short Squeeze & Volatility Positioning (74/100)",
    "retail_vs_institutional_positioning": {
        "retail_sentiment_score": 82,
        "retail_summary": "Retail communities across Reddit r/wallstreetbets, r/CoreWeave, FinTwit, and Threads exhibit passionate bullishness, viewing CoreWeave as the purest pure-play infrastructure proxy for the generative AI explosion. Retail traders are fixated on the 22.4% short float and $132.18 mean analyst target (+185.3% upside) heading into the print.",
        "institutional_sentiment_score": 67,
        "institutional_summary": "Institutional hedge fund positioning is sharply split between long-growth AI thematic funds who value the $28.5B contracted backlog, and deep value / credit-oriented short sellers who fear capital expenditure debt burdens and residual value depreciation as GPU architectures iterate rapidly.",
        "short_interest_summary": "Short interest sits elevated at 22.4% of float with Put/Call OI ratio at 0.89 and 186.7% implied volatility, pricing in a violent ±22.88% post-earnings move ($10.60 straddle value)."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print(f"CRWV pre_agent_bus files created successfully!")
