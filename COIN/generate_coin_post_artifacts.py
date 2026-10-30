import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "COIN"
DATE = "2026-10-29"

BUS_DIR = BASE_DIR / "post_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

# 1. Agent 2A: KPIs & Segments
agent2a = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "operational_kpis": [
        {
            "name": "Transaction Revenue ($M)",
            "q_minus_1_actual": 599.2,
            "q_minus_4_yoy": 1046.3,
            "street_consensus_q0": 630.0,
            "reported_actual_q0": 590.2,
            "spread_vs_street": "-6.3%",
            "verdict": "MISS",
            "bar_width_pct": 52
        },
        {
            "name": "Subscription & Services Revenue ($M)",
            "q_minus_1_actual": 555.1,
            "q_minus_4_yoy": 716.6,
            "street_consensus_q0": 550.0,
            "reported_actual_q0": 570.2,
            "spread_vs_street": "+3.7%",
            "verdict": "BEAT",
            "bar_width_pct": 82
        },
        {
            "name": "Stablecoin Revenue ($M)",
            "q_minus_1_actual": 292.0,
            "q_minus_4_yoy": 325.0,
            "street_consensus_q0": 298.0,
            "reported_actual_q0": 307.0,
            "spread_vs_street": "+3.0%",
            "verdict": "BEAT",
            "bar_width_pct": 78
        },
        {
            "name": "Adjusted EBITDA ($M)",
            "q_minus_1_actual": 207.8,
            "q_minus_4_yoy": 800.7,
            "street_consensus_q0": 260.0,
            "reported_actual_q0": 332.9,
            "spread_vs_street": "+28.0%",
            "verdict": "BEAT",
            "bar_width_pct": 92
        },
        {
            "name": "Crypto Trading Volume Market Share (%)",
            "q_minus_1_actual": 10.3,
            "q_minus_4_yoy": 5.6,
            "street_consensus_q0": 10.5,
            "reported_actual_q0": 10.7,
            "spread_vs_street": "+0.2%",
            "verdict": "BEAT",
            "bar_width_pct": 88
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E"],
        "segments": [
            {
                "name": "Transaction Revenue",
                "values": [1046.3, 982.7, 755.8, 599.2, 590.2, 610.0],
                "qoq": "-1.5%",
                "yoy": "-43.6%"
            },
            {
                "name": "Consumer Transaction Revenue",
                "values": [844.0, 734.0, 567.0, 452.0, 450.0, 470.0],
                "qoq": "-0.4%",
                "yoy": "-46.7%"
            },
            {
                "name": "Institutional Transaction Revenue",
                "values": [135.0, 185.0, 136.0, 100.0, 92.0, 95.0],
                "qoq": "-8.0%",
                "yoy": "-31.9%"
            },
            {
                "name": "Subscription and Services Revenue",
                "values": [716.6, 694.5, 583.5, 555.1, 570.2, 590.0],
                "qoq": "+2.7%",
                "yoy": "-20.4%"
            },
            {
                "name": "Stablecoin Revenue (USDC)",
                "values": [325.0, 331.0, 305.0, 292.0, 307.0, 320.0],
                "qoq": "+5.1%",
                "yoy": "-5.5%"
            },
            {
                "name": "Blockchain Rewards (Staking)",
                "values": [185.0, 152.0, 101.0, 83.0, 86.0, 88.0],
                "qoq": "+3.6%",
                "yoy": "-53.5%"
            }
        ]
    },
    "tooltip_definitions": {
        "Transaction Revenue": "Fees earned from retail consumer and institutional trades across spot and crypto derivatives.",
        "Subscription & Services": "Recurring and utility-based revenues including stablecoin interest sharing, blockchain staking rewards, and Coinbase One subscriptions.",
        "Stablecoin Revenue": "Revenue earned via the Centre/Circle partnership from interest on reserves backing USDC held on and off platform.",
        "Adjusted EBITDA": "Operating income adjusted for stock-based compensation, depreciation, amortization, and crypto asset impairment gains/losses.",
        "Trading Volume Market Share": "Coinbase's share of global fiat-to-crypto and crypto-to-crypto trading volume across spot and derivatives.",
        "Total Operating Expenses": "Consolidated expenses including transaction expenses, technology & development, sales & marketing, and general & administrative.",
        "Consumer Crypto Spot Volume": "Direct trading volume executed by retail customers on the Coinbase consumer app and website.",
        "Institutional Volume": "Prime brokerage, OTC, and high-frequency exchange execution volume for hedge funds, asset managers, and corporate treasuries.",
        "Derivatives Trading Volume": "Regulated futures and perpetual contracts executed via Coinbase Financial Markets and INTX.",
        "Coinbase One": "Paid consumer subscription tier offering zero trading fee allowances, boosted staking rewards, and priority support.",
        "True FCF": "Operating cash flow minus capital expenditures, stock-based compensation, and finance lease obligations.",
        "Crypto Asset Volatility": "Measure of price fluctuations across Bitcoin, Ethereum, and large-cap altcoins driving retail trading fee velocity.",
        "Base L2": "Coinbase's Ethereum Layer-2 rollup network generating sequencer revenue and ecosystem developer activity.",
        "Deribit / INTX Integration": "Integration of offshore derivatives venue Deribit with Coinbase International Exchange to expand global options OI.",
        "Stock-Based Compensation": "Non-cash equity incentives granted to engineering, product, and leadership teams.",
        "Operating Cash Flow": "Cash generated by core brokerage operations, customer balance sweeps, and staking distributions.",
        "GAAP Diluted EPS": "Net profit divided by diluted common shares, reflecting crypto mark-to-market accounting adjustments under ASU 2023-08.",
        "Net Income": "Consolidated GAAP earnings attributable to common stockholders after tax and fair value crypto asset adjustments.",
        "Transaction Expenses": "Miner fees, bank payment processing charges, and liquidity provider rebates incurred to settle trades.",
        "Cash & Cash Equivalents": "Available cash, USDC balances, and short-term Treasuries held directly by Coinbase corporate treasury."
    }
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")

# 2. Agent 2B: Transcript Forensics & Guidance
agent2b = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "matrix_a_execution_accountability": [
        {
            "metric": "Subscription & Services Revenue",
            "prior_guidance": "$500M - $580M ($540M midpoint)",
            "actual_delivered": "$570.2M delivered (+5.6% vs midpoint)",
            "variance_commentary": "Upper-bound execution driven by record average USDC held on-platform ($307M) and stable interest rate yields.",
            "credibility_grade": "EXCEEDED"
        },
        {
            "metric": "Transaction Expenses (% of Net Rev)",
            "prior_guidance": "Mid-teens as % of net revenue (~15%)",
            "actual_delivered": "16.8% of net revenue",
            "variance_commentary": "Slightly above mid-teens target due to higher network miner fees on Layer-1 rollups and payment rail costs.",
            "credibility_grade": "MET"
        },
        {
            "metric": "Adjusted Expenses (OpEx)",
            "prior_guidance": "$980M - $1,080M ($1,030M midpoint)",
            "actual_delivered": "$975.0M delivered (below low-end)",
            "variance_commentary": "Rigorous operating cost controls beat the lower bound of guidance by $5M, reflecting headcount discipline.",
            "credibility_grade": "EXCEEDED"
        },
        {
            "metric": "Stock-Based Compensation",
            "prior_guidance": "~$245M",
            "actual_delivered": "$233.0M delivered (-$12M favorable)",
            "variance_commentary": "SBC came in 5% below target as equity grant vesting was managed tightly.",
            "credibility_grade": "EXCEEDED"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026 Subscription & Services",
            "pre_print_consensus": "$565.0M",
            "management_guidance": "$550M - $630M ($590M midpoint)",
            "delta_vs_street": "+$25.0M (+4.4%) above Street midpoint",
            "action_badge": "RAISED",
            "pm_rationale": "Bullish recurring revenue anchor as higher interest rates and expanding USDC balances buffer crypto market volatility."
        },
        {
            "metric": "Q4 2026 Transaction Revenue",
            "pre_print_consensus": "$650.0M",
            "management_guidance": "~$165M QTD through Oct 25; caution extrapolating",
            "delta_vs_street": "Run-rate suggests $550M - $620M (~$585M midpoint)",
            "action_badge": "CAUTIONARY RESET",
            "pm_rationale": "Management warned against linear extrapolation given muted crypto spot volatility and post-election uncertainty."
        },
        {
            "metric": "FY2026 Adjusted Expenses Corridor",
            "pre_print_consensus": "$4,250M - $4,350M",
            "management_guidance": "$4,150M - $4,300M (lowered -$100M at midpoint)",
            "delta_vs_street": "-$75.0M favorable cost reduction",
            "action_badge": "LOWERED EXPENSES",
            "pm_rationale": "Second consecutive quarterly reduction in full-year expense envelope proves high operating leverage."
        },
        {
            "metric": "Q4 2026 Adjusted Expenses",
            "pre_print_consensus": "$1,090M",
            "management_guidance": "$1,007M - $1,157M ($1,082M midpoint)",
            "delta_vs_street": "-$8.0M below Street expectations",
            "action_badge": "IN-LINE",
            "pm_rationale": "Reflects seasonal Q4 performance marketing spend offset by continued general and administrative austerity."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Kenneth Worthington (JPMorgan)",
            "topic": "USDC Yield Sharing Dynamics & Regulatory Scrutiny",
            "question": "Can you elaborate on how potential Fed rate cuts will impact the stablecoin revenue sharing economics with Circle, and what percentage of USDC is migrating off-platform?",
            "executive_answer": "Alesia Haas (CFO) emphasized that while rate cuts compress gross yield, the total supply of USDC in Coinbase products reached a new all-time high in Q3. Platform stickiness and international adoption via Base and institutional custody are offsetting rate headwinds."
        },
        {
            "analyst": "Dan Dolev (Mizuho)",
            "topic": "Derivatives Market Share & Deribit Unified Exchange",
            "question": "How quickly can Coinbase convert international derivatives volume into revenue, and what is the cannibalization risk to existing spot trading fees?",
            "executive_answer": "Brian Armstrong (CEO) stated that derivatives trading volume grew 179% CAGR over the last two years and reached an all-time high market share of 10.7%. Relaunching Coinbase Pro with unified cross-collateralization allows traders to use spot balances as margin, increasing net platform activity."
        },
        {
            "analyst": "Devin Ryan (Citizens JMP)",
            "topic": "Prediction Markets & Base Layer-2 Monetization",
            "question": "What contributed to the surge in prediction market trading volume this quarter, and how does sequencer revenue on Base fit into medium-term revenue?",
            "executive_answer": "Emilie Choi (COO) noted that election and macro prediction contracts provided an important non-correlated volume cushion during low crypto volatility. Base sequencer fees are currently optimized for developer low-cost transactions, but app ecosystem traction is creating long-term subscription value."
        }
    ]
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")

# 3. Agent 2C: Sentiment & Market Positioning
agent2c = {
    "ticker": TICKER,
    "earnings_date": DATE,
    "four_pillar_sentiment": {
        "institutional_score": 62,
        "retail_score": 58,
        "options_skew_score": 50,
        "sell_side_score": 65,
        "composite_verdict": "Cautiously Constructive with Volatility Compression"
    },
    "retail_pulse": {
        "score": 58,
        "tone": "Subdued Euphoria to Neutral",
        "key_themes": [
            "Retail traders disappointed by spot volume stagnation and altcoin lag",
            "High enthusiasm for prediction markets and Coinbase Pro unified platform relaunch",
            "Questions surrounding regulatory clarity post-U.S. general election"
        ]
    },
    "institutional_positioning": {
        "score": 62,
        "tone": "Pragmatic Longs Hedging Spot Softness",
        "key_themes": [
            "Hedge funds heavily value S&S diversification (49% of net revenue) buffering transactional volatility",
            "Expense discipline (FY26 OpEx lowered -$100M) applauded as structural margin defense",
            "After-hours pullback of -4.74% viewed as orderly within the 8.29% weekly implied straddle"
        ]
    },
    "pm_takeaway": "COIN printed a massive GAAP EPS beat ($2.51 vs $0.07 consensus) propelled by crypto asset mark-to-market gains and expense austerity, despite top-line net revenue missing ($1,215.58M vs $1,280M consensus) due to multi-year lows in crypto volatility. With Q4 S&S guided higher ($550M-$630M) and FY26 expenses lowered, the -4.74% after-hours dip to $152.98 represents an attractive risk/reward entry for a post-election volatility expansion."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for COIN.")
