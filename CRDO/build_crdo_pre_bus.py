import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "pre_agent_bus"
BUS_DIR.mkdir(exist_ok=True)
TRUTH_PATH = BASE_DIR / "ground_truth" / "CRDO_2026-12-01_truth.json"
truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

TICKER = "CRDO"
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
    "upcoming_quarter_label": "Q2 FY27E (Ended Oct 31, 2026)",
    "latest_reported_quarter_label": "Q1 FY27 (Ended Aug 1, 2026)",
    "headline_and_company_kpis": [
        {
            "metric": "Consolidated GAAP Revenue ($M)",
            "tooltip_title": "Total consolidated GAAP revenue across Active Electrical Cables, Optical DSPs, SiPho PICs, and IP Licensing.",
            "tooltip_def": "Consolidated GAAP Revenue ($M): Credo generated $479.00M in Q1 FY27 (+114.7% YoY, +9.6% QoQ). Management guided Q2 FY27 revenue to $525M–$535M ($530M midpoint); Yahoo consensus sits at $531.95M (+98.5% YoY) while buy-side whispers target $542M–$550M+.",
            "q_minus_1_actual": "$479.00M",
            "q_minus_4_yoy_baseline": "$268.03M",
            "street_consensus_q0e": f"${cons_rev:,.2f}M",
            "whisper_bogey_q0e": "$542.0M–$550.0M+",
            "whisper_spread_display": "+2.3% vs Consensus",
            "bar_width_pct": 92,
            "hurdle_badge": "Top-Line Hurdle"
        },
        {
            "metric": "Non-GAAP Diluted EPS ($/sh)",
            "tooltip_title": "Non-GAAP diluted earnings per share excluding $87.98M stock-based compensation and acquisition intangibles.",
            "tooltip_def": "Non-GAAP Diluted EPS ($/sh): Consensus is $1.28/sh (+91% YoY vs $0.67 in Q2 FY26, and +6.7% QoQ vs $1.20 in Q1 FY27) on ~200M guided diluted shares. Credo has beaten consensus EPS 4 consecutive quarters (+15.96% avg surprise).",
            "q_minus_1_actual": "$1.20",
            "q_minus_4_yoy_baseline": "$0.67",
            "street_consensus_q0e": f"${cons_eps:.2f}",
            "whisper_bogey_q0e": "$1.34–$1.38",
            "whisper_spread_display": "+4.7% to +7.8% Whisper",
            "bar_width_pct": 88,
            "hurdle_badge": "Bottom-Line Hurdle"
        },
        {
            "metric": "Non-GAAP Gross Margin (%)",
            "tooltip_title": "Non-GAAP product and IP gross margin excluding SBC and acquired intangible amortization.",
            "tooltip_def": "Non-GAAP Gross Margin (%): Posted 68.0% in Q1 FY27 (64.5% GAAP). Management guided Q2 FY27 Non-GAAP GM to 67.0%–69.0% despite integrating DustPhotonics silicon photonics PICs and ramping new 1.6T optical/AEC SKUs.",
            "q_minus_1_actual": "68.0% (64.5% GAAP)",
            "q_minus_4_yoy_baseline": "67.6% (GAAP)",
            "street_consensus_q0e": "68.0% (Guide 67–69%)",
            "whisper_bogey_q0e": "68.5%–69.2%",
            "whisper_spread_display": "+50bps to +120bps",
            "bar_width_pct": 84,
            "hurdle_badge": "Margin Mix Audit"
        },
        {
            "metric": "Optical Portfolio Run-Rate (DSPs, ZeroFlap & SiPho PICs)",
            "tooltip_title": "Combined revenue trajectory across Optical DSPs (50G/100G/1.6T), ZeroFlap optics, and DustPhotonics SiPho PICs.",
            "tooltip_def": "Optical Portfolio Trajectory: Management targets >$600M in FY27 optical revenue (with ZeroFlap, SiPho PICs, and Optical DSPs each exceeding $100M) to diversify away from copper AEC concentration and drive fiscal H2 re-acceleration.",
            "q_minus_1_actual": "Record DSP + 1st SiPho",
            "q_minus_4_yoy_baseline": "Early 50G/100G Ramp",
            "street_consensus_q0e": ">$140M Q2E Implied",
            "whisper_bogey_q0e": ">$155M + FY27 Raise",
            "whisper_spread_display": "H2 Optical Inflection",
            "bar_width_pct": 86,
            "hurdle_badge": "Secondary TAM Driver"
        },
        {
            "metric": "Inventory Buffer & Hyperscaler Mix ($M)",
            "tooltip_title": "Balance sheet inventory staging ($313.05M) and US/APAC hyperscaler shipment concentration.",
            "tooltip_def": "Inventory & Hyperscaler Mix: Inventory climbed +24.8% QoQ to $313.05M (+168% YoY) to support unfulfilled AEC and 1.6T backlog, while US shipments hit $255.44M (53.3%) and Malaysia surged 11x YoY to $74.46M.",
            "q_minus_1_actual": "$313.05M Inv / 53.3% US",
            "q_minus_4_yoy_baseline": "$150.19M Inv / 38.7% US",
            "street_consensus_q0e": "Stable Days Inv. / 3+ Hyperscalers",
            "whisper_bogey_q0e": "New Neo-Cloud & 1.6T Wins",
            "whisper_spread_display": "Diversification Check",
            "bar_width_pct": 79,
            "hurdle_badge": "Concentration Risk"
        }
    ]
}

bus_2b = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Guidance_Debate_Agent (Agent 2B)",
    "model": "Gemini 3.8 Flash High Standard",
    "credibility_score": 84,
    "credibility_label": "84 / 100 (100% 4Q EPS Beat Rate, +15.96% Avg Surprise, Though Sequential Growth Deceleration Triggered -20% Q1 Sell-Off)",
    "matrix_a_prior_guidance_and_track_record": [
        {
            "metric": "Q2 FY27E Revenue vs. Prior Management Guide",
            "tooltip_title": "Comparison of management's Q1 FY27 outlook for Q2 FY27 against Street consensus.",
            "tooltip_def": "Revenue Guidance Calibration: On Sept 1, 2026, management guided Q2 FY27 revenue to $525M–$535M (+96% to +100% YoY, +10.6% QoQ at midpoint). Yahoo consensus sits at $531.95M, slightly above midpoint.",
            "prior_q_guidance_for_q0": "$525.0M – $535.0M (Q1 Call)",
            "current_street_consensus": f"${cons_rev:,.2f}M (Range ${truth['street_consensus_and_targets']['yahoo_revenue_low_q0e']:,.1f}M–${truth['street_consensus_and_targets']['yahoo_revenue_high_q0e']:,.1f}M)",
            "historical_4q_beat_rate": "4 / 4 Beats (+98.5% YoY Q2E)",
            "variance_and_sandbag_commentary": "Credo beat top-line consensus in 4 straight quarters, yet Q1's 9.6% QoQ pace cooled from Q3 FY26's +51.9% jump, prompting a -20.04% post-print pullback despite beating EPS.",
            "credibility_grade": "Grade A- (Consistent Beat, High Bar)"
        },
        {
            "metric": "Non-GAAP Gross Margin & OpEx Leverage",
            "tooltip_title": "Management's track record delivering 67%–69% Non-GAAP gross margin alongside elevated R&D.",
            "tooltip_def": "Margin Execution: Q1 Non-GAAP GM printed 68.0% even as GAAP R&D surged +118% YoY to $114.52M and SBC hit $87.98M. Q2 Non-GAAP OpEx is guided to $100M–$105M.",
            "prior_q_guidance_for_q0": "67.0%–69.0% GM / $100M–$105M OpEx",
            "current_street_consensus": "68.0% GM / ~50% FY27 Net Margin",
            "historical_4q_beat_rate": "4 / 4 Gross Margin Meets/Beats",
            "variance_and_sandbag_commentary": "Management has consistently outperformed initial gross margin bands by 50–100 bps due to favorable 100G/lane SerDes mix, offsetting DustPhotonics integration costs.",
            "credibility_grade": "Grade A (Strong Pricing Power)"
        },
        {
            "metric": "Non-GAAP Diluted EPS & SBC Dilution Control",
            "tooltip_title": "4Q Non-GAAP EPS surprise history versus GAAP SBC dilution ($87.98M in Q1 FY27).",
            "tooltip_def": "EPS & SBC Audit: Trailing 4Q EPS surprises were +35.26%, +13.74%, +12.17%, and +2.69% (avg +15.96%), though surprise magnitude compressed as Street caught up and Q1 SBC jumped +77% QoQ to $87.98M.",
            "prior_q_guidance_for_q0": "~200M Diluted Shares / ~50% Net Margin",
            "current_street_consensus": f"${cons_eps:.2f}/sh (Whisper $1.34–$1.38)",
            "historical_4q_beat_rate": "100% Beat Rate (+15.96% Avg Surp.)",
            "variance_and_sandbag_commentary": "Surprise compression from +35% to +2.7% over 4 quarters alongside Q1 True FCF dipping to -$5.03M makes Q3 FY27 guidance and SBC moderation critical.",
            "credibility_grade": "Grade B+ (Watch SBC Surge)"
        }
    ],
    "matrix_b_forward_guidance_bogeys": [
        {
            "forward_metric": "Q3 FY27E Revenue Guide & H2 Optical Re-Acceleration",
            "tooltip_title": "Forward Q3 FY27 (Jan 2027 quarter) revenue guidance confirming fiscal H2 re-acceleration.",
            "tooltip_def": "Q3 FY27E Guidance Bogey: With Q2 consensus at $531.95M and full-year FY27 growth guided >85% YoY (~$2.47B+ implied), Q3 FY27 needs to accelerate meaningfully above $585M–$600M.",
            "street_consensus_hurdle": "$585M–$600M Q3E (~10–13% QoQ)",
            "bull_case_bogey": ">= $615M Q3E + >$650M FY27 Optical Guide",
            "bear_case_breakdown": "< $565M Q3E (Signals Sequential Plateau)",
            "sensitivity_badge": "Primary Re-Rating Catalyst",
            "strategic_rationale": "After Q1's -20.04% sell-off on sequential deceleration fears, proving an H2 optical + 1.6T AEC inflection is essential to unlock the 152% implied Street PT upside."
        },
        {
            "forward_metric": "1.6T AEC / DSP Ramp & DustPhotonics SiPho Integration",
            "tooltip_title": "Commercial ramp timing for 1.6T Active Electrical Cables, 1.6T Optical DSPs, and Silicon Photonics PICs.",
            "tooltip_def": "1.6T & SiPho Execution: Investors need concrete milestone updates on 1.6T AEC customer qualifications, initial 1.6T DSP orders, and DustPhotonics SiPho PIC scaling beyond Q1's first revenue.",
            "street_consensus_hurdle": "On-Track H2 1.6T Sampling & Ramps",
            "bull_case_bogey": "Accelerated 1.6T Production + 4th/5th Hyperscaler",
            "bear_case_breakdown": "1.6T Qualification Delays or Customer Pushouts",
            "sensitivity_badge": "Architecture Moat",
            "strategic_rationale": "Hyperscaler transition from 800G to 1.6T clusters (200G/lane) pits Credo's n-1 legacy-node power/cost edge against Astera Labs (20.5x EV/S) and Broadcom."
        },
        {
            "forward_metric": "Gross Margin Durability & Cash Conversion post-M&A",
            "tooltip_title": "Sustaining 67%+ Non-GAAP gross margin while rebuilding $764.26M cash after DustPhotonics.",
            "tooltip_def": "Margin & FCF Quality: Cash fell from $1,443.29M to $764.26M on DustPhotonics cash outlay while Inventory climbed to $313.05M and SBC hit $87.98M (True FCF -$5.03M).",
            "street_consensus_hurdle": "67%–69% Q3E Non-GAAP GM & Positive OCF",
            "bull_case_bogey": ">= 68.5% GM + SBC < 14% Rev + Inv Turn Improvement",
            "bear_case_breakdown": "GM < 66.5% or Rising Working Capital Drag",
            "sensitivity_badge": "Quality of Earnings",
            "strategic_rationale": "Rebuilding FCF conversion above $120M/qtr and normalizing SBC below $65M/qtr will silence bears pointing to Q1's -$5.03M True FCF."
        }
    ],
    "section_4b_pre_print_debates": [
        {
            "debate_id": "DEBATE_1",
            "title": "Law of Large Numbers Deceleration vs. H2 Optical & 1.6T Re-Acceleration",
            "consensus_view": "Skeptics point out that despite beating Q1 FY27 EPS by +2.69%, CRDO plunged -20.04% on Sept 2 as sequential revenue growth moderated to +9.6% QoQ ($479M vs $437M), questioning whether copper AEC demand is maturing ahead of 1.6T transitions.",
            "variant_perception": "Bulls emphasize that Credo trades at just 10.97x Forward P/E and 12.15x EV/Sales despite +98.5% YoY Q2E revenue growth—less than half Astera Labs' 26.0x Forward P/E—while >$600M FY27 optical revenue (ZeroFlap, SiPho PICs, Optical DSPs) creates a second hyper-growth S-curve in H2.",
            "call_focus_question": "CEO Bill Brennan: With Q1 sequential growth moderating to +9.6% before the guided Q2 acceleration to $530M midpoint, how much visibility do you have into Q3/Q4 1.6T AEC and optical DSP ramps to sustain >85% full-year FY27 growth?"
        },
        {
            "debate_id": "DEBATE_2",
            "title": "Hyperscaler Concentration & Copper-to-Optics Transition (Scale-Up / Scale-Out)",
            "consensus_view": "Bears warn that Credo remains heavily concentrated across a few US hyperscalers (US shipments were 53.3% of Q1 revenue, down from 71.9% in Q4 FY26) and fear optical interconnects or Co-Packaged Optics (CPO) could encroach on copper AEC reach inside next-gen GPU racks.",
            "variant_perception": "Management's vertical integration—acquiring Hyperlume (microLED optical interconnects) and DustPhotonics (Silicon Photonics PICs), plus launching ZeroFlap optics—positions Credo as architecture-agnostic across both short-reach copper AECs and rack-to-rack optical links, while expanding Neo-Cloud and Malaysia ODM deployments ($74.5M in Q1).",
            "call_focus_question": "CEO Bill Brennan & CFO Dan Fleming: How many >10% hyperscaler customers did Credo serve in Q2, and how should investors model the gross margin mix between maturing 800G AECs, ramping 1.6T DSPs, and newly integrated DustPhotonics SiPho PICs?"
        },
        {
            "debate_id": "DEBATE_3",
            "title": "Forensic SBC Spike ($87.98M), Inventory Build ($313.05M) & Post-M&A Cash Drawdown",
            "consensus_view": "Forensic analysts flag that Q1 FY27 cash and short-term investments dropped by $679M QoQ (from $1,443.3M to $764.3M) to fund DustPhotonics, while SBC jumped +77% QoQ to $87.98M (pulling True FCF to -$5.03M) and inventory swelled +24.8% QoQ to $313.05M.",
            "variant_perception": "Bullish desks view the $313.05M inventory build as intentional wafer and substrate staging for confirmed H2 hyperscaler AEC/DSP backlog, while $764.26M cash vs $26.20M total debt still leaves a $738.06M net cash fortress with zero liquidity risk.",
            "call_focus_question": "CFO Dan Fleming: Following Q1's $87.98M GAAP SBC surge and $313.05M inventory build, was the SBC jump tied to DustPhotonics/Hyperlume acquisition retention awards, and when do you expect working capital and True FCF to normalize?"
        }
    ]
}

bus_2c = {
    "ticker": TICKER,
    "earnings_date": EARNINGS_DATE,
    "agent": "Pre_Whisper_Sentiment_Agent (Agent 2C)",
    "model": "Gemini 3.8 Flash High Standard",
    "verified_products": [
        "HiWire Active Electrical Cables (AECs): Copper-based SerDes-retimed interconnects dominating intra-rack and rack-to-rack AI cluster connectivity up to 800G and ramping 1.6T",
        "Optical DSPs & ZeroFlap Optics: 50G/100G/200G-per-lane optical digital signal processors and high-reliability ZeroFlap optical transceivers targeting >$600M FY27 optical revenue",
        "DustPhotonics Silicon Photonics (SiPho) PICs & Hyperlume microLED: Vertically integrated photonic integrated circuits and microLED chip-to-chip optical engines",
        "PCIe Gen6 Retimers & OmniConnect Chiplets: Low-power n-1 legacy-node SerDes retimers and IP licensing solutions for scale-up AI architectures"
    ],
    "four_pillar_sentiment": {
        "options_volatility_score": 52,
        "options_volatility_desc": f"52/100 (Dec 4 ATM Straddle implies ±{opt_move_pct:.2f}% / ${opt_move_usd:.2f} at 149.2% IV vs {avg_1d_move:.2f}% 4Q Avg Realized Move — Overpriced Event Vol by +{vol_delta:.2f}%, Neutral {put_call_ratio:.2f} P/C OI)",
        "institutional_positioning_score": 86,
        "institutional_positioning_desc": f"86/100 ({analyst_cnt} Analysts with Strong Buy 1.35 consensus & ${mean_pt:.2f} Mean PT implying +{upside_to_pt:.2f}% upside; High PT ${high_pt:.0f}, Low ${low_pt:.0f} after post-Q1 pullback to 10.97x Fwd P/E)",
        "retail_sentiment_score": 68,
        "retail_sentiment_desc": "68/100 (Constructive FinTwit & r/GrowthStockInvesting accumulation viewing 11x Fwd P/E as an AI picks-and-shovels dislocation, tempered by WSB caution after Sept's -20% drop)",
        "short_interest_score": 44,
        "short_interest_desc": f"44/100 (Moderate {short_float:.2f}% Short Interest of Float — meaningful tactical hedging into the print that could fuel upside covering if Q3 optical guidance beats)"
    },
    "retail_vs_institutional_audit": {
        "retail_narrative": f"On Reddit (r/wallstreetbets, r/GrowthStockInvesting) and FinTwit, traders are split after CRDO's steep drawdown from its 2026 highs to ${spot_price:.2f}. Bulls highlight a rare sub-11x forward P/E on nearly +100% YoY revenue growth and bet on H2 optical re-acceleration, while cautious options traders note the massive ±{opt_move_pct:.2f}% (${opt_move_usd:.2f}) straddle price makes naked long calls expensive against theta crush.",
        "institutional_narrative": f"Sell-side coverage remains overwhelmingly bullish ({analyst_cnt} analysts, Strong Buy, ${mean_pt:.2f} mean PT), viewing the pullback to 12.15x EV/Sales (vs ALAB at 20.52x) as an asymmetric entry ahead of the 1.6T AEC and >$600M optical ramp. However, hedge funds are closely policing Q3 guidance quality, hyperscaler concentration, and Q1's $87.98M SBC jump, keeping put/call OI balanced at {put_call_ratio:.2f} and pricing a +{vol_delta:.2f}% vol premium."
    }
}

(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2a_kpis.json").write_text(json.dumps(bus_2a, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2b_guidance.json").write_text(json.dumps(bus_2b, indent=2), encoding="utf-8")
(BUS_DIR / f"{TICKER}_{EARNINGS_DATE}_pre_agent2c_sentiment.json").write_text(json.dumps(bus_2c, indent=2), encoding="utf-8")
print(f"[SUCCESS] Wrote Layer 2 pre_agent_bus files for {TICKER} ({EARNINGS_DATE}).")
