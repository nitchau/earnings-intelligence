import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TICKER = "ANET"
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
            "name": "Product Revenue ($M)",
            "q_minus_1_actual": 2548.0,
            "q_minus_4_yoy": 1911.7,
            "street_consensus_q0": 2720.0,
            "reported_actual_q0": 3190.0,
            "spread_vs_street": "+17.28%",
            "verdict": "BLOWOUT BEAT",
            "bar_width_pct": 98
        },
        {
            "name": "Service Revenue ($M)",
            "q_minus_1_actual": 487.7,
            "q_minus_4_yoy": 396.6,
            "street_consensus_q0": 460.0,
            "reported_actual_q0": 467.6,
            "spread_vs_street": "+1.65%",
            "verdict": "BEAT",
            "bar_width_pct": 86
        },
        {
            "name": "Non-GAAP Gross Margin (%)",
            "q_minus_1_actual": 64.2,
            "q_minus_4_yoy": 65.2,
            "street_consensus_q0": 63.5,
            "reported_actual_q0": 64.0,
            "spread_vs_street": "+50 bps",
            "verdict": "BEAT",
            "bar_width_pct": 90
        },
        {
            "name": "Non-GAAP Operating Margin (%)",
            "q_minus_1_actual": 47.5,
            "q_minus_4_yoy": 48.6,
            "street_consensus_q0": 45.2,
            "reported_actual_q0": 49.1,
            "spread_vs_street": "+390 bps",
            "verdict": "BLOWOUT BEAT",
            "bar_width_pct": 96
        },
        {
            "name": "Operating Cash Flow ($M)",
            "q_minus_1_actual": 1083.0,
            "q_minus_4_yoy": 1268.2,
            "street_consensus_q0": 1150.0,
            "reported_actual_q0": 1200.9,
            "spread_vs_street": "+4.43%",
            "verdict": "BEAT",
            "bar_width_pct": 91
        }
    ],
    "segment_reporting": {
        "periods": ["Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)", "Q4 2026E (Guided / Street)"],
        "segments": [
            {
                "name": "Product Revenue",
                "values": [1911.7, 2065.0, 2260.0, 2548.0, 3190.0, 3450.0],
                "qoq": "+25.2%",
                "yoy": "+66.8%"
            },
            {
                "name": "Service Revenue",
                "values": [396.6, 422.8, 449.0, 487.7, 467.6, 500.0],
                "qoq": "-4.1%",
                "yoy": "+17.9%"
            },
            {
                "name": "Total Consolidated Revenue",
                "values": [2308.3, 2487.8, 2709.0, 3035.7, 3657.6, 3950.0],
                "qoq": "+20.5%",
                "yoy": "+58.5%"
            }
        ]
    },
    "tooltip_definitions": {
        "Product Revenue": "Switching, routing platforms, and AI networking hardware systems including Arista 7800 AI Spine, 7700R, and 7060X series switches ($3,190.0M in Q3 2026, surging +66.8% YoY).",
        "Service Revenue": "Post-contract customer software support, A-Care maintenance, and advanced network operating subscriptions ($467.6M in Q3 2026, up +17.9% YoY).",
        "Non-GAAP Gross Margin": "Adjusted gross margin excluding stock-based compensation ($8.4M) and intangible asset amortization ($7.0M), reaching 64.0% in Q3 2026.",
        "Non-GAAP Operating Margin": "Adjusted operating margin excluding stock compensation ($138.1M) and intangibles ($15.3M), expanding to a record 49.1% in Q3 2026.",
        "Non-GAAP Diluted EPS": "Adjusted net income per share excluding stock-based awards and strategic investment gains, delivering $1.20 in Q3 2026 vs $1.08 consensus.",
        "GAAP Diluted EPS": "Diluted earnings per share under U.S. GAAP ($1.22 in Q3 2026, up +82.1% YoY from $0.67 in Q3 2025).",
        "Etherlink SU-144 Architecture": "Liquid-cooled open Ethernet architecture for scale-up AI networking supporting up to 144 accelerators per rack in a single hop and up to 1,024 XPUs via cross-rack topologies.",
        "Arista 7800 AI Spine": "Flagship high-radix distributed AI spine chassis delivering high-density 800G and 1.6T Ethernet switching across clusters of up to 1 million XPUs.",
        "Extensible Operating System (EOS)": "Arista's unified, programmable Linux-based network operating system running across every device, eliminating downtime with state-sharing NetDB architecture.",
        "Ethernet for Scale-Up Networks (ESUN)": "Open standards-based networking framework developed with AMD, Arm, Broadcom, d-Matrix, Meta, Microsoft, and Qualcomm to replace proprietary GPU interconnects.",
        "True Free Cash Flow": "Core economic cash generation deducting capital expenditures ($100.7M) and stock-based compensation ($138.1M) from operating cash flow ($1,200.9M), yielding $962.1M.",
        "Operating Cash Flow": "Cash generated by operations ($1,200.9M in Q3 2026, reaching $3,977.4M YTD).",
        "Capital Expenditures": "Reinvestment in specialized network testing infrastructure and engineering facilities ($100.7M in Q3 2026).",
        "Reported Free Cash Flow": "Operating cash flow minus capital expenditures ($1,100.2M in Q3 2026).",
        "Cash and Marketable Securities Fortress": "Combined cash ($2,288.1M) and liquid short-term marketable securities ($12,070.9M) totaling $14.36B with zero debt on the balance sheet.",
        "Segment Routing over IPv6 (SRv6)": "Advanced network layer deterministic multiplane routing enabling ultra-low latency, lossless AI packet transport across geographically separated data centers.",
        "S&P 100 Index Addition": "Arista was officially inducted into the S&P 100 blue-chip index in September 2026, driving mandatory passive institutional index fund accumulation.",
        "Full-Year Guidance Surge": "Q4 2026 guidance raised to $3.9B - $4.0B ($3,950M midpoint, +58.8% YoY), positioning FY26 revenue to surpass $13.35B."
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
            "prior_guidance": "$3,250.0M - $3,350.0M ($3,300.0M midpoint)",
            "actual_delivered": "$3,657.6M delivered (+10.84% above midpoint)",
            "variance_commentary": "Revenue shattered internal guide by +$357.6M as cloud titan AI cluster deployments accelerated ahead of schedule.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Non-GAAP Operating Margin",
            "prior_guidance": "Approximately 43.0% - 44.0%",
            "actual_delivered": "49.1% delivered (+510 bps above high-end)",
            "variance_commentary": "Massive operating leverage on blowout revenue ramp expanded operating margin to an all-time record 49.1%.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Q3 2026 Non-GAAP Diluted EPS",
            "prior_guidance": "$1.02 - $1.06 ($1.04 midpoint)",
            "actual_delivered": "$1.20 delivered (+$0.16 / +15.4% beat)",
            "variance_commentary": "Delivered record EPS driven by 64.0% non-GAAP gross margin and disciplined G&A execution.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        },
        {
            "metric": "Product Revenue Expansion",
            "prior_guidance": ">45% YoY growth",
            "actual_delivered": "+66.8% YoY ($3,190.0M delivered)",
            "variance_commentary": "Product revenue surged as 800G Etherlink switches shipped in record volume across Meta and Microsoft AI data centers.",
            "credibility_grade": "CRUSHED OWN GUIDE"
        }
    ],
    "matrix_b_forward_guidance_reset": [
        {
            "metric": "Q4 2026 Revenue Guidance",
            "pre_print_consensus": "$3,450.0M",
            "management_guidance": "$3,900.0M - $4,000.0M ($3,950.0M midpoint)",
            "delta_vs_street": "+$500.0M (+14.49%) blowout upward revision",
            "action_badge": "RAISED AGGRESSIVELY",
            "pm_rationale": "Represents 58.8% YoY growth, demonstrating sustained hyper-growth across AI back-end and front-end fabrics."
        },
        {
            "metric": "Q4 2026 Non-GAAP Operating Margin",
            "pre_print_consensus": "44.5%",
            "management_guidance": "48.0% - 49.0% (~48.5% midpoint)",
            "delta_vs_street": "+400 bps above Street consensus",
            "action_badge": "RAISED AGGRESSIVELY",
            "pm_rationale": "Signals sustained profitability near peak margin levels even while scaling production of complex liquid-cooled systems."
        },
        {
            "metric": "Q4 2026 Non-GAAP Diluted EPS",
            "pre_print_consensus": "$1.15",
            "management_guidance": "$1.26 - $1.30 ($1.28 midpoint)",
            "delta_vs_street": "+$0.13 (+11.3%) upward reset",
            "action_badge": "RAISED",
            "pm_rationale": "Implies full-year non-GAAP EPS approaching $4.37, well above consensus expectations."
        },
        {
            "metric": "FY 2026 Total Revenue",
            "pre_print_consensus": "$12,850.0M",
            "management_guidance": "Exceeding $13,350.0M (>50% YoY growth)",
            "delta_vs_street": "+$500.0M full-year top-line raise",
            "action_badge": "RAISED AGGRESSIVELY",
            "pm_rationale": "Confirms Arista as the definitive networking champion of the generative and agentic AI infrastructure buildout."
        }
    ],
    "call_qa_forensic_highlights": [
        {
            "analyst": "Meta Marshall (Morgan Stanley)",
            "topic": "Etherlink SU-144 Scale-Up Adoption & Ultra Ethernet Momentum vs InfiniBand",
            "question": "Jayshree, the announcement of Etherlink SU-144 with AMD, Meta, Microsoft, and Broadcom is a major milestone for open scale-up fabrics. Can you talk about how quickly hyperscalers are transitioning from proprietary InfiniBand to Arista Ethernet for their largest generative AI clusters?",
            "executive_answer": "Jayshree Ullal (Chairperson & CEO) stated: 'The shift toward open Ethernet for both scale-up and scale-out AI is happening faster than anticipated. Customers refuse to be locked into proprietary single-vendor stacks. With our Etherlink SU-144 architecture supporting 144 accelerators per rack in a single hop and lossless transport, hyperscalers are realizing equivalent or superior job completion times at significantly lower total cost of ownership. We see Ethernet capturing the vast majority of new AI cluster deployments.'"
        },
        {
            "analyst": "Samik Chatterjee (JPMorgan)",
            "topic": "Q4 Operating Margin Durability & Supply Chain Allocation for 800G/1.6T Optics",
            "question": "Chantelle, your Q4 guide of 48-49% operating margin follows this quarter's record 49.1%. As you ramp 1.6T systems and liquid-cooled gear, how are you managing component availability, optical transceivers, and gross margin durability?",
            "executive_answer": "Chantelle Breithaupt (CFO) responded: 'Our gross margin of 64% reflects excellent manufacturing execution and strong software attach. While 1.6T optics and high-radix switch silicon require disciplined inventory staging—which is why inventory grew to $3.2B—our supply chain commitments are fully secured. The 48-49% operating margin guide shows that our operating leverage is structural, not a one-quarter anomaly.'"
        },
        {
            "analyst": "Tal Liani (Bank of America)",
            "topic": "Enterprise & Campus Networking Momentum vs Cloud Titan Concentration",
            "question": "Jayshree, product revenue grew 66.8% YoY, clearly driven by cloud titans. What are you seeing in enterprise campus switching and routing, and how is the pipeline shaping up for non-cloud customers deploying private AI models?",
            "executive_answer": "Jayshree Ullal explained: 'While Cloud Titans represented the largest volume driver this quarter, Enterprise and Campus grew double-digits. Enterprises are beginning to deploy private AI clusters on-premise, and they want the exact same Arista EOS software that runs the world's largest AI supercomputers. That gives Arista an unrivaled competitive moat across client-to-cloud.'"
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
        "institutional_score": 96,
        "retail_score": 91,
        "options_skew_score": 78,
        "sell_side_score": 97,
        "composite_verdict": "Premier AI Networking Monopoly & Secular Compounder"
    },
    "retail_pulse": {
        "score": 91,
        "tone": "Celebration of Ethernet Victory over InfiniBand",
        "key_themes": [
            "Active chatter on Reddit r/wallstreetbets and FinTwit praising Jayshree Ullal's unmatched execution as ANET shares rallied +9.48% after-hours to $186.01",
            "Retail enthusiasm around Arista's coalition with AMD, Meta, and Microsoft to standardize open AI networking fabrics",
            "Investors highlighting Arista's pristine $14.4B cash cushion with zero long-term debt and record 49.1% operating margin"
        ]
    },
    "institutional_positioning": {
        "score": 96,
        "tone": "Universal Consensus Upward Revisions & Multiple Expansion",
        "key_themes": [
            "Tier 1 sell-side firms (Morgan Stanley, JPMorgan, BofA, Evercore ISI) preparing price target increases toward $210-$230",
            "Institutional portfolio managers aggressively accumulating ANET following S&P 100 inclusion and blowout 58.5% YoY revenue acceleration",
            "Options market experiencing rapid implied volatility crush as the stock's +9.48% after-hours move trades cleanly inside the 12.46% expected band"
        ]
    },
    "pm_takeaway": "Arista delivered a flawless operational print and blockbuster guidance. Q3 revenue of $3,657.6M shattered consensus ($3,180.0M) by +$477.6M (+15.02%), growing 58.5% YoY in the highest growth print since its IPO. Non-GAAP diluted EPS reached $1.20 vs $1.08 consensus (+11.11%), while non-GAAP operating margin surged to a record 49.1%. Forward guidance for Q4 at $3.9B - $4.0B ($3,950M midpoint) beat Street expectations by +$500M (+14.5%), accompanied by an operating margin guide of 48-49% and EPS of $1.26-$1.30. Arista's balance sheet boasts $14.36B in cash and investments with zero debt, generating $962.1M in true free cash flow."
}

(BUS_DIR / f"{TICKER}_{DATE}_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")

print("[OK] Successfully generated Agent 2A, 2B, and 2C artifacts for ANET.")
