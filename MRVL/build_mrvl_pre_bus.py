import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)
TRUTH_PATH = BASE_DIR / "ground_truth" / "MRVL_2026-12-01_truth.json"
truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

TICKER = "MRVL"
EARNINGS_DATE = "2026-12-01"

spot_price = float(truth["price_validation"]["yahoo_spot_price"])
short_float = float(truth["valuation_and_market"]["short_percent_of_float"])
opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"])
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"])
put_call_ratio = float(truth["options_positioning"]["put_call_oi_ratio"])
avg_1d_move = float(truth["historical_earnings_track_record"]["avg_historical_1d_move_abs_pct"])
vol_delta = float(truth["historical_earnings_track_record"]["implied_vs_historical_move_delta_pct"])
mean_pt = float(truth["street_consensus_and_targets"]["target_mean_price"])
high_pt = float(truth["street_consensus_and_targets"]["target_high_price"])
low_pt = float(truth["street_consensus_and_targets"]["target_low_price"])
upside_to_pt = float(truth["street_consensus_and_targets"]["implied_upside_to_mean_pct"])
analyst_cnt = int(truth["street_consensus_and_targets"]["analyst_count"])
cons_rev = float(truth["schedule_verification"]["yahoo_consensus_revenue"])
cons_eps = float(truth["schedule_verification"]["yahoo_consensus_eps"])

bus_2a = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_KPI_Consensus_Agent (Agent 2A)",
    "model": "Gemini 3.8 Flash High Standard",
    "upcoming_quarter_label": "Q3 FY27E (Ended Oct 31, 2026)",
    "latest_reported_quarter_label": "Q2 FY27 (Ended Aug 1, 2026)",
    "headline_and_company_kpis": [
        {
            "metric": "Consolidated Net Revenue ($M)",
            "tooltip_title": "Total consolidated GAAP net revenue across Data Center and Communications & Other end markets.",
            "tooltip_def": "Consolidated Net Revenue ($M): Marvell posted $2,739.30M in Q2 FY27 (+36.5% YoY). Management guided Q3 FY27 revenue to $3,150M (±5%, +51.8% YoY); Yahoo consensus sits at $3,152.21M (+51.95% YoY) while buy-side whispers look for $3,210M–$3,260M+.",
            "q_minus_1_actual": "$2,739.30M",
            "q_minus_4_yoy_baseline": "$2,074.50M",
            "street_consensus_q0e": f"${cons_rev:,.2f}M",
            "whisper_bogey_q0e": "$3,210M–$3,260M+",
            "whisper_spread_display": "+2.5% vs Consensus",
            "bar_width_pct": 91,
            "hurdle_badge": "Top-Line Hurdle"
        },
        {
            "metric": "Non-GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Non-GAAP diluted earnings per share excluding $326.2M SBC and acquisition intangible amortization.",
            "tooltip_def": "Non-GAAP Diluted EPS ($/sh): Consensus is $1.10/sh (matching Q3 guide $1.10 ±$0.05 vs $0.94 in Q2 FY27 and $0.76 in Q3 FY26). Marvell has beaten consensus EPS 4 consecutive quarters (+1.42% avg surprise).",
            "q_minus_1_actual": "$0.94",
            "q_minus_4_yoy_baseline": "$0.76",
            "street_consensus_q0e": f"${cons_eps:.2f}",
            "whisper_bogey_q0e": "$1.14–$1.18",
            "whisper_spread_display": "+3.6% to +7.3% Whisper",
            "bar_width_pct": 87,
            "hurdle_badge": "Bottom-Line Hurdle"
        },
        {
            "metric": "Data Center Segment Revenue ($M & % Mix)",
            "tooltip_title": "Hyperscaler custom AI ASICs/XPUs, electro-optics DSPs, Teralynx switches, and Celestial AI interconnects.",
            "tooltip_def": "Data Center Revenue ($M): Surged +45.7% YoY to $2,171.50M in Q2 FY27 (79.3% of total revenue). Custom AI XPU ramps and 800G/1.6T optical interconnects are expected to push Q3 Data Center above $2.56B (>81% mix).",
            "q_minus_1_actual": "$2,171.50M (79.3%)",
            "q_minus_4_yoy_baseline": "$1,517.90M (73.2%)",
            "street_consensus_q0e": "~$2,568M (+69% YoY)",
            "whisper_bogey_q0e": "$2,620M+ (>81% Mix)",
            "whisper_spread_display": "Custom ASIC Inflection",
            "bar_width_pct": 94,
            "hurdle_badge": "Core Valuation Engine"
        },
        {
            "metric": "Non-GAAP Gross Margin (%)",
            "tooltip_title": "Non-GAAP gross margin balancing high-margin optical DSPs against lower-margin custom AI ASIC ramps.",
            "tooltip_def": "Non-GAAP Gross Margin (%): Printed 58.9% in Q2 FY27 (53.1% GAAP). Management guided Q3 Non-GAAP GM slightly lower to 57.5%–58.5% due to rapid H2 mix shift toward custom AI silicon.",
            "q_minus_1_actual": "58.9% (53.1% GAAP)",
            "q_minus_4_yoy_baseline": "51.6% (GAAP)",
            "street_consensus_q0e": "58.0% (Guide 57.5–58.5%)",
            "whisper_bogey_q0e": "58.2%–58.6%",
            "whisper_spread_display": "Mix-Shift Discipline",
            "bar_width_pct": 80,
            "hurdle_badge": "Margin Mix Check"
        },
        {
            "metric": "Multi-Year AI Revenue & Lumentum Deal Framing ($B)",
            "tooltip_title": "Progress toward ~$12B FY27 / ~$18B FY28 revenue targets and Lumentum Holdings all-stock deal dilution clarity.",
            "tooltip_def": "FY27/FY28 AI Trajectory & M&A: Management previously raised FY27 revenue outlook to ~$12B and FY28 to ~$18B on hyperscaler ASIC bookings, while the announced all-stock Lumentum acquisition faces investor scrutiny over ~1/3 share dilution.",
            "q_minus_1_actual": "~$12B FY27 / ~$18B FY28",
            "q_minus_4_yoy_baseline": "$8.19B FY26 Actual",
            "street_consensus_q0e": "Reaffirm ~$12B / ~$18B",
            "whisper_bogey_q0e": "Raise FY27 >$12.3B + Synergies",
            "whisper_spread_display": "M&A Overhang Audit",
            "bar_width_pct": 84,
            "hurdle_badge": "Multiple Re-Rating Key"
        }
    ]
}

bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 83,
    "credibility_label": "83 / 100 (100% 4Q EPS Beat Rate, Massive H2 Custom ASIC Inflection, Yet Q2 -10.3% Pullback & Lumentum Dilution Overhang)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q3 FY27E Net Revenue vs. Prior Management Guide",
            "tooltip_title": "Comparison of management's Q2 FY27 outlook for Q3 FY27 against Street consensus.",
            "tooltip_def": "Revenue Guidance Calibration: Management guided Q3 FY27 net revenue to $3,150M (±5%), implying +15.0% QoQ and +51.8% YoY acceleration. Yahoo consensus sits right at $3,152.21M.",
            "prior_q_guidance_for_q0": "$3,150.0M ± 5% (Q2 Call)",
            "current_street_consensus": f"${cons_rev:,.2f}M (Range ${truth['street_consensus_and_targets']['yahoo_revenue_low_q0e']:,.1f}M–${truth['street_consensus_and_targets']['yahoo_revenue_high_q0e']:,.1f}M)",
            "historical_4q_beat_rate": "4 / 4 Revenue Beats",
            "variance_and_sandbag_commentary": "Q2 revenue ($2,739.3M) beat midpoint by ~$39M, yet MRVL fell -10.28% after Q2 on steepening expectations and sector multiple compression despite guiding Q3 up +15% QoQ.",
            "credibility_grade": "Grade A (Strong H2 Visibility)"
        },
        {
            "metric": "Non-GAAP Diluted EPS & Gross Margin Mix",
            "tooltip_title": "4Q Non-GAAP EPS surprise track record alongside custom ASIC gross margin dilution.",
            "tooltip_def": "EPS & Margin Audit: Trailing 4Q EPS beats were modest (+3.01%, +1.05%, +0.64%, +0.99%; avg +1.42%) as Marvell passes through high-volume custom XPU wafers at lower gross margin (57.5%–58.5% Q3 guide vs 58.9% in Q2).",
            "prior_q_guidance_for_q0": "$1.10 ± $0.05 EPS / 57.5%–58.5% GM",
            "current_street_consensus": f"${cons_eps:.2f}/sh (Whisper $1.14–$1.18)",
            "historical_4q_beat_rate": "100% Beat Rate (+1.42% Avg Surp.)",
            "variance_and_sandbag_commentary": "Because custom AI silicon carries lower gross margin percentage than merchant DSPs, maintaining Non-GAAP GM >= 58.0% while scaling EPS > $1.12 is critical for bull conviction.",
            "credibility_grade": "Grade B+ (Tight EPS Beats)"
        },
        {
            "metric": "Free Cash Flow Conversion & SBC Discipline",
            "tooltip_title": "Q2 FY27 OCF ($605.5M) and True FCF ($148.1M) after $131.2M CapEx and $326.2M SBC.",
            "tooltip_def": "FCF & Capital Audit: Unlike many AI peers, Marvell generated positive True Forensic FCF of +$148.10M in Q2 ($474.3M Rep FCF minus $326.2M SBC), though SBC jumped +57.1% QoQ post-Celestial AI & XConn deals.",
            "prior_q_guidance_for_q0": "Strong Cash Flow Generation",
            "current_street_consensus": ">$500M Q3 Reported FCF",
            "historical_4q_beat_rate": "$1.72B TTM Reported FCF",
            "variance_and_sandbag_commentary": "Debt rose to $5,286.1M vs $3,932.8M cash ($1.35B net debt) and SBC climbed to $326.2M (11.9% of sales) following M&A integrations, making post-Lumentum capital discipline a focal point.",
            "credibility_grade": "Grade B+ (Positive True FCF, Watch SBC)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q4 FY27E Revenue Guide & ~$12B FY27 / ~$18B FY28 Reaffirmation",
            "tooltip_title": "Forward Q4 FY27 revenue guidance confirming sequential custom XPU acceleration toward ~$12B FY27.",
            "tooltip_def": "Q4 FY27E Revenue Bogey: After Q3's $3.15B consensus, hitting ~$12B FY27 requires Q4 FY27 guidance >= $3.65B–$3.75B (+65% YoY). Any slippage below $3.55B threatens the ~$18B FY28 narrative.",
            "street_consensus_hurdle": "$3.60B–$3.68B Q4E / ~$12B FY27",
            "bull_case_bogey": ">= $3.75B Q4E + Raise FY27 > $12.2B",
            "bear_case_breakdown": "< $3.50B Q4E (Signals XPU Ramp Delay)",
            "sensitivity_badge": "Primary Re-Rating Catalyst",
            "strategic_rationale": "At just 17.76x Forward P/E (down sharply from mid-year highs), delivering >= $3.75B Q4 guidance proves the AWS/hyperscaler custom silicon ramp is accelerating on schedule."
        },
        {
            "forward_metric": "Lumentum All-Stock Deal Economics & Optical Vertical Integration",
            "tooltip_title": "Strategic defense, EPS accretion timeline, and dilution mitigation for the Lumentum Holdings acquisition.",
            "tooltip_def": "Lumentum Deal Audit: With current MRVL holders slated to own ~2/3 of the combined entity, investors require clear gross-margin synergy math and assurance that M&A isn't masking organic optical DSP share shifts.",
            "street_consensus_hurdle": "Clear Accretion Timeline & Laser Supply Edge",
            "bull_case_bogey": "Quantified Synergies + Buyback Offset",
            "bear_case_breakdown": "Margin Dilution or Delayed Regulatory Close",
            "sensitivity_badge": "Sentiment Overhang",
            "strategic_rationale": "Resolving retail and institutional backlash over Lumentum share dilution is mandatory to close the 128% gap to the $298.99 Street mean target."
        },
        {
            "forward_metric": "Custom AI XPU Customer Breadth & Non-GAAP Gross Margin Floor",
            "tooltip_title": "Defending >= 57.5% Non-GAAP GM while ramping multiple Tier-1 hyperscaler custom ASIC sockets.",
            "tooltip_def": "ASIC Mix & Margin Floor: Investors track next-gen AWS Trainium/custom silicon continuity, Google/Microsoft optical/XPU programs, and Celestial AI photonic fabric traction.",
            "street_consensus_hurdle": "Q4 Non-GAAP GM >= 57.0%–57.5%",
            "bull_case_bogey": "GM >= 58.0% + New Tier-1 XPU Ramp",
            "bear_case_breakdown": "GM < 56.5% or Hyperscaler Socket Loss",
            "sensitivity_badge": "Gross Margin & Share",
            "strategic_rationale": "Proves custom AI ASICs generate high operating-dollar leverage despite lower gross margin % vs merchant optical DSPs."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "debate_id": "DEBATE_1",
            "title": "Lumentum All-Stock Acquisition Dilution vs. End-to-End AI Optical Scale",
            "consensus_view": "Retail traders and skeptical funds blasted Marvell's all-stock deal for Lumentum Holdings—leaving existing MRVL shareholders with roughly two-thirds of the combined company—contributing to a brutal pullback from mid-year highs and price-target trims (e.g., Susquehanna to $225).",
            "variant_perception": "Bulls argue that owning Lumentum's high-power datacom lasers alongside Inphi's electro-optics DSPs and Celestial AI's photonic fabric creates an unmatched vertically integrated optical interconnect powerhouse for 1.6T/3.2T AI clusters, while 17.76x Forward P/E prices in peak pessimism.",
            "call_focus_question": "CEO Matt Murphy: Can you walk through the exact pro-forma EPS accretion, gross margin profile, and capital return plans following the Lumentum transaction to address shareholder dilution concerns?"
        },
        {
            "debate_id": "DEBATE_2",
            "title": "Hyperscaler Custom AI ASIC Ramp ($12B FY27 / $18B FY28) vs. Gross Margin Compression",
            "consensus_view": "Bears note that Marvell's Non-GAAP gross margin is guiding down from 58.9% (Q2) to 57.5%–58.5% (Q3) as lower-margin custom ASICs scale, while persistent rumors around AWS/hyperscaler next-gen socket sharing fuel volatility.",
            "variant_perception": "Data Center revenue surged +45.7% YoY to $2,171.5M in Q2 (79.3% mix) and Q3 overall revenue is guided up +51.8% YoY to $3.15B, putting Marvell squarely on track for ~$12B in FY27 and ~$18B in FY28 with expanding operating-dollar leverage.",
            "call_focus_question": "CEO Matt Murphy & CFO Willem Meintjes: What is the expected Q4 revenue split between custom AI silicon and merchant electro-optics, and where does Non-GAAP gross margin trough as custom XPU volumes peak?"
        },
        {
            "debate_id": "DEBATE_3",
            "title": "Post-M&A Balance Sheet Leverage ($5.29B Debt) & SBC Jump ($326.2M) vs. True FCF",
            "consensus_view": "Forensic analysts highlight that total debt rose to $5,286.1M (net debt $1,353.3M vs $3,932.8M cash) and GAAP SBC jumped +57.1% QoQ to $326.2M (up from $207.6M in Q1) following the Celestial AI and XConn acquisitions.",
            "variant_perception": "Even after deducting $131.2M CapEx and $326.2M SBC, Marvell generated +$148.1M in True Forensic FCF in Q2 ($474.3M Reported FCF, $1.72B TTM FCF) and grew GAAP Operating Income +52.9% YoY to $456.9M.",
            "call_focus_question": "CFO Willem Meintjes: How much of Q2's $326.2M SBC was tied to Celestial AI and XConn retention awards, and what is your leverage and free cash flow conversion target exiting FY27?"
        }
    ]
}

bus_2c = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Whisper_Sentiment_Agent (Agent 2C)",
    "model": "Gemini 3.8 Flash High Standard",
    "verified_products": [
        "Custom AI Accelerators / XPUs (5nm/3nm/2nm ASICs): Hyperscaler custom compute programs ramping sharply in H2 FY27 toward ~$12B FY27 and ~$18B FY28 revenue targets",
        "Inphi Electro-Optics DSPs & Lumentum Optical Portfolio: 800G/1.6T PAM4 DSPs, coherent optics, and proposed all-stock Lumentum laser integration",
        "Celestial AI Photonic Fabric & XConn PCIe/CXL Switching: Acquired scale-up optical and CXL interconnect silicon for multi-rack AI clusters",
        "Teralynx Ethernet Switches & Bravera Controllers: High-radix cloud data center switching and enterprise storage/carrier silicon"
    ],
    "four_pillar_sentiment": {
        "options_volatility_score": 50,
        "options_volatility_desc": f"50/100 (Dec 4 ATM Straddle implies ±{opt_move_pct:.2f}% / ${opt_move_usd:.2f} vs {avg_1d_move:.2f}% 4Q Avg Realized Move — Overpriced Event Vol by +{vol_delta:.2f}%, Bullish {put_call_ratio:.2f} P/C OI)",
        "institutional_positioning_score": 84,
        "institutional_positioning_desc": f"84/100 ({analyst_cnt} Analysts with Strong Buy 1.40 consensus & ${mean_pt:.2f} Mean PT implying +{upside_to_pt:.2f}% upside; High PT ${high_pt:.0f}, Low ${low_pt:.0f} at 17.76x Fwd P/E)",
        "retail_sentiment_score": 44,
        "retail_sentiment_desc": "44/100 (Cooled Reddit/WSB & FinTwit sentiment following drawdown from mid-year highs and Lumentum all-stock dilution backlash)",
        "short_interest_score": 38,
        "short_interest_desc": f"38/100 (Moderate {short_float:.2f}% Short Interest of Float — reflects M&A arbitrage / hedging rather than heavy directional short crowding)"
    },
    "retail_vs_institutional_audit": {
        "retail_narrative": f"Across Reddit (r/wallstreetbets) and FinTwit, sentiment on MRVL at ${spot_price:.2f} has turned wary after its sharp slide from mid-year peaks near $316 and backlash over the all-stock Lumentum acquisition. Traders debate whether 17.76x Forward P/E makes MRVL an oversold AI bounce play or if the ±{opt_move_pct:.2f}% (${opt_move_usd:.2f}) straddle favors selling premium.",
        "institutional_narrative": f"Institutional semis desks ({analyst_cnt} analysts, Strong Buy, ${mean_pt:.2f} mean PT) acknowledge sector-wide multiple compression and Lumentum integration scrutiny, yet maintain strong conviction in AWS/hyperscaler custom ASIC scaling and Q3's +51.95% YoY revenue acceleration. With P/C OI skewed bullish at {put_call_ratio:.2f}, funds want airtight Q4 guidance >= $3.75B to confirm the ~$18B FY28 trajectory."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print(f"[SUCCESS] Wrote Layer 2 pre_agent_bus files for {TICKER} ({EARNINGS_DATE}).")
