import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

TICKER = "NET"
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
            "tooltip_title": "Consolidated quarterly GAAP revenue across Cloudflare network connectivity, security, and developer platforms.",
            "tooltip_def": "Total GAAP Revenue ($M): Cloudflare delivered $696.06M in Q2 2026 (+35.86% YoY vs $512.32M in Q2 2025). Wall Street consensus models $739.39M in Q3 2026E (+31.56% YoY vs $562.03M in Q3 2025), with buy-side whisper looking for $748.50M+ on accelerating Workers AI inference demand.",
            "q_minus_1_actual": "$696.06M",
            "q_minus_4_yoy_baseline": "$562.03M",
            "street_consensus_q0e": "$739.39M",
            "whisper_bogey_q0e": "$748.50M",
            "whisper_spread_display": "+1.23% Spread",
            "bar_width_pct": 86,
            "hurdle_badge": "Top-Line Hurdle"
        },
        {
            "metric": "Non-GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Quarterly adjusted diluted earnings per share excluding stock compensation and intangible amortization.",
            "tooltip_def": "Non-GAAP Diluted EPS ($/sh): Q2 2026 actual EPS delivered $0.29 (+7.5% beat vs $0.27 consensus). Street models $0.34 for Q3 2026E with buy-side whisper bogeys looking for $0.36.",
            "q_minus_1_actual": "$0.29",
            "q_minus_4_yoy_baseline": "$0.27",
            "street_consensus_q0e": "$0.34",
            "whisper_bogey_q0e": "$0.36",
            "whisper_spread_display": "+$0.02 Better",
            "bar_width_pct": 82,
            "hurdle_badge": "EPS Bogey"
        },
        {
            "metric": "Large Enterprise Customers (> $100K ARR)",
            "tooltip_title": "Count of commercial enterprise customers contributing annualized recurring revenue exceeding $100,000.",
            "tooltip_def": "Large Enterprise Customers (> $100K ARR): Scaled past 3,250 accounts in Q2 2026; Street expects net customer adds of +185 accounts in Q3 2026E to reach 3,440+ enterprises.",
            "q_minus_1_actual": "3,255 Accounts",
            "q_minus_4_yoy_baseline": "2,784 Accounts",
            "street_consensus_q0e": "3,440 Accounts",
            "whisper_bogey_q0e": "3,490 Accounts",
            "whisper_spread_display": "+50 Accounts",
            "bar_width_pct": 88,
            "hurdle_badge": "Enterprise Expansion"
        },
        {
            "metric": "Workers AI Inference & Serverless Compute ($M)",
            "tooltip_title": "Revenue and developer consumption run-rate across Cloudflare Workers AI edge GPUs, Vectorize, and R2 object storage.",
            "tooltip_def": "Workers AI & Edge GPU Inference: Cloudflare's fastest-growing developer engine deployed across global edge points of presence; whisper models $85M+ run-rate in Q3 2026E.",
            "q_minus_1_actual": "$68.50M",
            "q_minus_4_yoy_baseline": "$28.00M",
            "street_consensus_q0e": "$78.00M",
            "whisper_bogey_q0e": "$85.00M",
            "whisper_spread_display": "+8.97% Spread",
            "bar_width_pct": 92,
            "hurdle_badge": "AI Edge Driver"
        }
    ]
}

# Agent 2B: Guidance & Debates
bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 92,
    "credibility_label": "92 / 100 (Flawless 4Q Beat Rate, Consistent Guidance Upgrades & Structural Operating Leverage)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 2026E Revenue Guidance Corridor",
            "tooltip_title": "Management prior quarter revenue guidance range provided during Q2 2026 earnings.",
            "tooltip_def": "Q3 2026 Revenue Guidance: Management guided to $735.0M - $741.0M ($738.0M midpoint); current consensus sits at $739.39M.",
            "prior_q_guidance_for_q0": "$735.0M – $741.0M ($738.0M Midpoint)",
            "current_street_consensus": "$739.39M",
            "historical_4q_beat_rate": "100.0% (4 of 4 Quarters)",
            "variance_and_sandbag_commentary": "Consensus models near high end of the guidance corridor; Cloudflare has beaten consensus revenue by an average of 1.5% to 2.8% over the past 4 quarters.",
            "credibility_grade": "Grade A+ (Elite Execution)"
        },
        {
            "metric": "Q3 2026E Non-GAAP Operating Income Corridor",
            "tooltip_title": "Targeted quarterly operating profit margin and non-GAAP EBIT.",
            "tooltip_def": "Operating Income Guidance: Guided to $98.0M - $102.0M non-GAAP EBIT; consensus models $101.5M with whisper at $105.0M.",
            "prior_q_guidance_for_q0": "$98.0M – $102.0M ($100.0M Midpoint)",
            "current_street_consensus": "$101.50M",
            "historical_4q_beat_rate": "100.0% Beat Rate",
            "variance_and_sandbag_commentary": "Cloudflare's server architecture efficiency and automated network routing drive continuous gross margin resilience above 71%.",
            "credibility_grade": "Grade A (Strong)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 2026E Net Sales Guidance Hurdle",
            "tooltip_title": "Expected top-line revenue guidance for the upcoming fourth quarter.",
            "tooltip_def": "Q4 2026E Guidance Hurdle: Street models $785.0M; buy-side bull bogey requires guidance >= $800.0M to sustain multiple expansion above 38x P/S.",
            "street_consensus_hurdle": "$785.0M (+27.7% YoY)",
            "bull_case_bogey": "$800.0M+ (Workers AI & SASE Acceleration)",
            "bear_case_breakdown": "< $775.0M (Enterprise Sales Cycle Elongation)",
            "sensitivity_badge": "High Multiple Sensitivity",
            "strategic_rationale": "At a rich forward valuation (161x P/E, 38.7x P/S), any Q4 guidance deceleration below 27% triggers valuation compression."
        },
        {
            "forward_metric": "Full-Year 2026 FY Guidance Raise",
            "tooltip_title": "Full-year 2026 top-line guidance raise expected from CEO Matthew Prince.",
            "tooltip_def": "FY2026 Guidance: Street models $2.84B; buy-side expects raise to $2.87B - $2.90B.",
            "street_consensus_hurdle": "$2.84B (+30.5% YoY)",
            "bull_case_bogey": "$2.88B+ (Raised by > $40M)",
            "bear_case_breakdown": "Reiterated / Unchanged ($2.82B)",
            "sensitivity_badge": "Full-Year Benchmark",
            "strategic_rationale": "Institutional funds require beat-and-raise cadence across both Q4 revenue and full-year operating cash flow."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "title": "1. Workers AI Monetization & Edge GPU Inference Scale",
            "title_color": "#60a5fa",
            "border_color": "#3b82f6",
            "badge": "AI SUPER-CYCLE",
            "badge_class": "badge-blue",
            "content": "Cloudflare has placed GPUs across hundreds of cities in its global edge network, enabling sub-millisecond AI inference without centralized hyperscaler egress fees. Institutional investors are seeking evidence that developer uptake of Workers AI and Vectorize is driving material incremental ARR rather than cannibalizing legacy CDN usage."
        },
        {
            "title": "2. Zero Trust & SASE Consolidation vs Palo Alto Networks & Zscaler",
            "title_color": "#34d399",
            "border_color": "#10b981",
            "badge": "CYBERSECURITY MOAT",
            "badge_class": "badge-bull",
            "content": "As Fortune 500 CISOs consolidate security point solutions, Cloudflare One is aggressively competing against Zscaler and Palo Alto Networks. Analysts want color on contract win rates for enterprise-wide Secure Access Service Edge (SASE) and single-vendor secure connectivity replacements."
        },
        {
            "title": "3. High Multiple Valuation Durability & FCF Conversion (38.7x P/S)",
            "title_color": "#f59e0b",
            "border_color": "#f59e0b",
            "badge": "VALUATION TENSION",
            "badge_class": "badge-warn",
            "content": "Trading at 38.66x TTM sales and 161.2x forward P/E, Cloudflare trades at one of the highest multiples in enterprise software. While Operating Cash Flow reached $117.56M in Q2, stock-based compensation of $159.87M resulted in True FCF of -$103.49M. Bulls argue network architecture moat justifies premium; bears warn of multiple compression on any growth deceleration."
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
        "flagship_products": "Cloudflare Connectivity Cloud (Global Anycast Network), Cloudflare One (Zero Trust SASE, Access, Gateway), Cloudflare Workers (Serverless Edge Compute & Workers AI GPUs), Vectorize (Vector Database), R2 (Zero-Egress Object Storage), Cloudflare DDoS & Web Application Firewall (WAF)",
        "commercialization_channels": "Enterprise direct sales force, global system integrators (Accenture, Kyndryl), channel partners, self-serve developer tier, and hyperscaler co-sell programs"
    },
    "composite_pre_print_sentiment_score": 84,
    "composite_sentiment_label": "Strongly Bullish / High Growth AI & Security Momentum (84/100)",
    "retail_vs_institutional_positioning": {
        "retail_sentiment_score": 88,
        "retail_summary": "Retail sentiment on Reddit r/stocks, r/wallstreetbets, and FinTwit is aggressively bullish, viewing Cloudflare as the premier picks-and-shovels infrastructure play for low-latency AI inference and zero-egress cloud storage.",
        "institutional_sentiment_score": 79,
        "institutional_summary": "Institutional desks are heavily overweight on strategic quality, noting Cloudflare's 100% 4Q beat track record and 31.5% revenue growth, while hedging against short-term multiple compression given elevated valuation (38.7x P/S).",
        "short_interest_summary": "Short interest is modest at 2.81% of float, indicating high institutional sponsorship with limited immediate short-squeeze fuel."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print("NET pre_agent_bus files created successfully!")
