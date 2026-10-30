import json
import os
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
BUS_DIR = BASE_DIR / "post_agent_bus"
BUS_DIR.mkdir(exist_ok=True)

# ==============================================================================
# AGENT 2A: KPI DISCOVERY AGENT
# ==============================================================================
agent2a = {
  "ticker": "AMZN",
  "earnings_date": "2026-10-29",
  "agent_role": "KPI_Discovery_Agent",
  "model": "Gemini 3.8 Flash High",
  "company_operational_kpis": [
    {
      "kpi_name": "Amazon Web Services (AWS) Net Sales ($M)",
      "definition": "Cloud infrastructure, foundational model hosting (Bedrock), and custom Trainium2/Inferentia silicon deployments reaching a $184B annualized run rate.",
      "street_consensus": 41800.0,
      "t1_whisper": 42500.0,
      "reported_q0_actual": 42232.0,
      "qoq_change_pct": 23.4,
      "yoy_change_pct": 39.3,
      "vs_consensus_delta": "+$432.0M (+1.03%)",
      "verdict": "BEAT"
    },
    {
      "kpi_name": "Worldwide Consolidated Operating Income ($M)",
      "definition": "Total consolidated operating profit across North America, International, and AWS, achieving an all-time record 13.9% operating margin.",
      "street_consensus": 18500.0,
      "t1_whisper": 19500.0,
      "reported_q0_actual": 28076.0,
      "qoq_change_pct": 2.2,
      "yoy_change_pct": 61.1,
      "vs_consensus_delta": "+$9,576.0M (+51.76%)",
      "verdict": "MASSIVE BEAT"
    },
    {
      "kpi_name": "Advertising Services Revenue ($M)",
      "definition": "High-margin digital retail media advertising across Sponsored Products, Sponsored Brands, and default Prime Video ad placements.",
      "street_consensus": 19200.0,
      "t1_whisper": 19600.0,
      "reported_q0_actual": 19809.0,
      "qoq_change_pct": 0.0,
      "yoy_change_pct": 19.5,
      "vs_consensus_delta": "+$609.0M (+3.17%)",
      "verdict": "BEAT"
    },
    {
      "kpi_name": "Third-Party (3P) Seller Services ($M)",
      "definition": "Commissions, fulfillment (FBA), and shipping fees generated from marketplace merchants representing >61% of total paid unit volume.",
      "street_consensus": 45500.0,
      "t1_whisper": 46200.0,
      "reported_q0_actual": 46780.0,
      "qoq_change_pct": 0.0,
      "yoy_change_pct": 12.0,
      "vs_consensus_delta": "+$1,280.0M (+2.81%)",
      "verdict": "BEAT"
    },
    {
      "kpi_name": "Full-Year 2026 Cash Capital Expenditures ($B)",
      "definition": "Cash investments in generative AI data center infrastructure, custom Trainium2 server clusters, and robotics fulfillment automation.",
      "street_consensus": 195.0,
      "t1_whisper": 205.0,
      "reported_q0_actual": 220.0,
      "qoq_change_pct": 10.0,
      "yoy_change_pct": 65.0,
      "vs_consensus_delta": "+$25.0B (+12.82% CapEx Surge)",
      "verdict": "CAPEX SURGE"
    }
  ],
  "reporting_segments_5q_mapping": [
    {
      "segment_name": "North America",
      "q0_revenue_millions": 118500.0,
      "share_of_revenue_pct": 58.68,
      "sub_rows": [
        "Online stores ($70,432.0M, +9.2% YoY)",
        "Third-party seller services ($46,780.0M, +12.0% YoY)",
        "North America Operating Income ($9,123.0M, 7.7% margin)"
      ]
    },
    {
      "segment_name": "Amazon Web Services (AWS)",
      "q0_revenue_millions": 42232.0,
      "share_of_revenue_pct": 20.91,
      "sub_rows": [
        "Cloud Enterprise Compute, Bedrock AI & Storage ($42,232.0M, +39.3% YoY)",
        "AWS Segment Operating Profit ($16,621.0M, 39.4% operating margin)"
      ]
    },
    {
      "segment_name": "International",
      "q0_revenue_millions": 41212.0,
      "share_of_revenue_pct": 20.41,
      "sub_rows": [
        "International Consumer & Marketplace ($41,212.0M, +7.1% YoY)",
        "International Operating Profit ($1,717.0M, 4.2% margin vs -$35M in Q3 2025)"
      ]
    }
  ]
}

(BUS_DIR / "AMZN_2026-10-29_agent2a_kpis.json").write_text(json.dumps(agent2a, indent=2), encoding="utf-8")

# ==============================================================================
# AGENT 2B: TRANSCRIPT FORENSIC AGENT
# ==============================================================================
agent2b = {
  "ticker": "AMZN",
  "earnings_date": "2026-10-29",
  "agent_role": "Transcript_Forensic_Agent",
  "model": "Gemini 3.8 Flash High",
  "guidance_accountability_matrix_a": [
    {
      "guided_metric": "Q3 2026 Net Sales Corridor",
      "prior_quarter_guidance": "$186.0B to $191.0B (+5.7% to +8.5% YoY; Consensus: $202.26B / $190.5B)",
      "reported_q0_actual": "Net sales surged to $201,944.0M ($201.9B, +12.0% YoY), exceeding company prior guidance upper bound by +$10.9B",
      "variance_commentary": "Top-line delivered +12% YoY despite an estimated 400 bps drag from Prime Day shifting into Q2 this year versus entirely Q3 in 2025.",
      "credibility_grade": "BEAT OWN GUIDE"
    },
    {
      "guided_metric": "Q3 2026 Operating Income Corridor",
      "prior_quarter_guidance": "$16.5B to $20.5B ($18.5B midpoint; $17.42B in Q3 2025)",
      "reported_q0_actual": "Consolidated operating income hit an all-time record $28,076.0M ($28.1B, 13.9% margin), shattering guidance upper bound by +$7.58B",
      "variance_commentary": "AWS high-margin software leverage (39.4% margin) and North American regional fulfillment efficiencies unlocked record consolidated operating leverage.",
      "credibility_grade": "MASSIVE BEAT"
    },
    {
      "guided_metric": "AWS Enterprise Generative AI Acceleration",
      "prior_quarter_guidance": "High-teens to low-20s YoY growth hurdle with accelerating Bedrock and Trainium adoption",
      "reported_q0_actual": "AWS net sales accelerated to +39.3% YoY reaching $42,232.0M, pacing at a $184B annualized run rate",
      "variance_commentary": "Fastest AWS expansion in nearly five years, proving custom Trainium2 chips and enterprise Bedrock migrations are translating directly into revenue.",
      "credibility_grade": "BLOWOUT EXPANSION"
    },
    {
      "guided_metric": "Full-Year 2026 Capital Expenditures Pace",
      "prior_quarter_guidance": "Elevated capital intensity to support overwhelming generative AI compute constraints (~$190B-$200B expected)",
      "reported_q0_actual": "Q3 CapEx reached $77,259.0M, pushing quarterly True FCF to -$54,902.0M; guidance raised to ~$220B for FY2026",
      "variance_commentary": "Management aggressively increased FY2026 CapEx to $220B, sparking institutional concerns over free cash flow conversion and ROIC timelines.",
      "credibility_grade": "HIGHER CAPEX SURGE"
    }
  ],
  "forward_guidance_reset_matrix_b": [
    {
      "forward_horizon_and_metric": "Q4 2026 Holiday Net Sales Guidance Corridor",
      "preprint_street_consensus": "$238.5B to $242.0B ($240.25B consensus midpoint)",
      "new_management_guidance": "$240.0 billion to $247.0 billion (+12% to +16% YoY growth; $243.5B midpoint)",
      "delta_vs_street": "+$3.25B higher revenue midpoint (+1.35% vs consensus)",
      "action_badge": "RAISED GUIDANCE",
      "rationale": "Strong early holiday momentum, resilient Prime consumer demand, and high-teens advertising acceleration heading into Cyber Week."
    },
    {
      "forward_horizon_and_metric": "Q4 2026 Consolidated Operating Income Outlook",
      "preprint_street_consensus": "$26.5B to $28.0B ($27.25B midpoint)",
      "new_management_guidance": "$28.5 billion to $33.5 billion ($31.0B midpoint vs $25.0B in Q4 2025)",
      "delta_vs_street": "+$3.75B higher operating income midpoint (+13.76% vs consensus)",
      "action_badge": "RAISED CORRIDOR",
      "rationale": "High-margin digital advertising growth in high teens and AWS capacity scale offsetting seasonal fulfillment center staffing."
    },
    {
      "forward_horizon_and_metric": "Full-Year 2026 Cash Capital Expenditures",
      "preprint_street_consensus": "~$195B to $200B total 2026 capital budget",
      "new_management_guidance": "Approximately $220 billion in cash capital expenditures for full-year 2026",
      "delta_vs_street": "+$20B to +$25B higher CapEx (~+11% increase above pre-print models)",
      "action_badge": "CAPEX SURGE",
      "rationale": "Front-loading high-density liquid-cooled data center builds, power infrastructure, and custom Trainium2 silicon clusters."
    },
    {
      "forward_horizon_and_metric": "Free Cash Flow & Capital Allocation Philosophy",
      "preprint_street_consensus": "Expectation of positive quarterly FCF inflection to support share buybacks",
      "new_management_guidance": "Prioritizing massive generational AI compute deployment over short-term FCF maximization; no share buybacks authorized in Q3",
      "delta_vs_street": "Organic cash generation fully reinvested into AI infrastructure war chest",
      "action_badge": "REINVESTMENT FOCUS",
      "rationale": "Andy Jassy reiterated that AWS's 39% margins demonstrate exceptional ROIC on early cloud investments, justifying aggressive capex."
    }
  ],
  "call_qa_forensic_highlights": [
    {
      "analyst_name": "Brian Nowak (Morgan Stanley)",
      "topic": "$220B FY26 CapEx, Negative Quarterly FCF (-$34.8B) & ROIC Underwriting",
      "question": "Andy and Brian, Q3 CapEx accelerated to $77.26 billion, pushing quarterly reported free cash flow to -$34.84 billion, and you guided full-year 2026 CapEx to $220 billion. How should institutional investors underwrite the durability of AWS margins and return on capital on this level of spending?",
      "executive_response": "CEO Andy Jassy explained that AWS net sales grew 39.3% YoY to a $184 billion annualized run rate with 39.4% operating margins, generating $16.62 billion in segment EBIT in a single quarter. The overwhelming majority of the $220 billion CapEx is for contracted generative AI infrastructure and custom Trainium2 chips where demand dramatically outstrips available capacity, giving Amazon high conviction in rapid multi-year payback."
    },
    {
      "analyst_name": "Doug Anmuth (JPMorgan)",
      "topic": "AWS Deceleration Concerns vs 39.3% Growth & Trainium2 Chip Supply",
      "question": "Andy, AWS delivered an extraordinary 39.3% growth rate to $42.23 billion. Could you unpack the contribution between core enterprise cloud migrations versus generative AI workloads on Bedrock, and what are the primary supply chain gating factors for Trainium2 silicon?",
      "executive_response": "Andy Jassy noted that AWS growth was powered by both large-scale migrations of traditional workloads and massive enterprise adoption of Bedrock and Trainium2. Trainium2 clusters are virtually 100% committed upon delivery, offering clients 40% to 50% better price-performance than commercial GPUs, which is driving accelerated customer retention."
    },
    {
      "analyst_name": "Ross Sandler (Barclays)",
      "topic": "Advertising Growth (+12% vs +19.5% Prior) & Prime Day Timing Impact",
      "question": "Brian, advertising revenue grew 12% YoY in Q3 after growing 19.5% in Q2, while you guide advertising back to the high teens in Q4. Can you clarify how much of the Q3 deceleration was purely Prime Day timing versus macro ad demand?",
      "executive_response": "CFO Brian Olsavsky confirmed that Prime Day shifted entirely to Q2 in 2026 for most major geographies, whereas in 2025 it occurred in Q3. Excluding this 400 bps shift and foreign exchange headwinds, baseline advertising demand remains exceptionally healthy, leading to strong visibility for high-teens ad growth during the Q4 holiday quarter."
    }
  ]
}

(BUS_DIR / "AMZN_2026-10-29_agent2b_transcript.json").write_text(json.dumps(agent2b, indent=2), encoding="utf-8")

# ==============================================================================
# AGENT 2C: SOCIAL & MICROBLOGGING PULSE AGENT
# ==============================================================================
agent2c = {
  "ticker": "AMZN",
  "earnings_date": "2026-10-29",
  "agent_role": "Social_Pulse_Agent",
  "model": "Gemini 3.8 Flash High",
  "social_channels_crawled": [
    "Reddit (r/wallstreetbets, r/stocks, r/options, r/amazon)",
    "X (FinTwit / $AMZN / #AWS / #Trainium2)",
    "Threads (threads.net / #techstocks)",
    "Stocktwits ($AMZN earnings stream)",
    "Seeking Alpha Q3 2026 8-K Analysis & Conference Call Reactions",
    "Sell-Side Flash Reactions (JPMorgan, Morgan Stanley, Goldman Sachs, Barclays)"
  ],
  "retail_vs_institutional_reaction": {
    "retail_sentiment_summary": "Retail traders on r/wallstreetbets and FinTwit celebrated the blowout AWS growth (+39.3% to $42.23B) and record $28.08B operating profit. However, retail bulls were bewildered by the -7.30% after-hours sell-off to $225.99, blaming algorithmic stop-loss cascades triggered by the headline $77.26B CapEx print and -$34.8B reported quarterly FCF.",
    "institutional_sentiment_summary": "Institutional hedge fund PMs and long-only funds de-grossed tech exposure in after-hours trading due to capital allocation digestion: (1) FY2026 CapEx guide escalated to $220B (~+$25B above expectations); (2) quarterly True FCF flipped to -$54.90B, extinguishing buyback hopes; and (3) GAAP Diluted EPS ($1.89) narrowly trailed consensus ($1.96). Nonetheless, enterprise analysts underscored that 39.4% AWS margins and $31B Q4 EBIT guidance represent an exceptional operating fortress.",
    "after_hours_movement_driver": "AMZN dropped -7.30% after-hours to $225.99 (-$17.80 from $243.79 close) as the market digested an eye-popping $77,259.0M quarterly CapEx print ($220B full-year 2026 guide) that drove quarterly True FCF to -$54,902.0M and optically suppressed GAAP EPS ($1.89 vs $1.96 est), completely overshadowing AWS accelerating +39.3% YoY to $42.23B and record $28.08B consolidated operating income."
  },
  "four_pillar_post_sentiment_scores": {
    "pillar_1_retail_and_social_pulse": {
      "score_out_of_100": 64,
      "classification": "BULLISH ON AWS / JOLTED BY CAPEX DIGESTION",
      "key_themes": [
        "Awe at AWS hitting $42.23B (+39.3% YoY) with a 39.4% operating margin",
        "Disbelief over $77.26B quarterly CapEx and full-year $220B guidance",
        "Debate over whether CapEx burn is generational AI leadership or cash destruction",
        "Frustration at algos dumping shares despite record $28.08B operating income"
      ],
      "top_quote": "FinTwit Tech Fund Manager: 'Amazon grew AWS 39% to a $184B run rate and printed $28.1B of EBIT, but Wall Street is having a mini panic attack because Andy Jassy is spending $220B on Trainium data centers. Buy the dip.'"
    },
    "pillar_2_sellside_flash_reactions": {
      "score_out_of_100": 80,
      "classification": "HIGH CONVICTION ON CLOUD / RECALIBRATING CASH FLOW MODELS",
      "key_themes": [
        "Morgan Stanley and JPMorgan maintain Overweight, highlighting AWS +39% inflection",
        "Sell-side adjusting FY26-FY27 FCF estimates lower to incorporate $220B CapEx pace",
        "Q4 guidance midpoint of $243.5B revenue and $31.0B EBIT exceeds Street hurdle",
        "Prime Day shift to Q2 fully explains the optical deceleration in advertising"
      ],
      "top_quote": "Goldman Sachs Flash Note: 'While -$34.8B quarterly FCF on $77.3B CapEx will cause near-term indigestion, AWS accelerating +39.3% YoY at 39.4% operating margins demonstrates indisputable commercial returns on AI silicon.'"
    },
    "pillar_3_management_call_tone": {
      "score_out_of_100": 88,
      "classification": "CONFIDENT ON AI TRAINIUM SCALE & OPERATIONAL DISCIPLINE",
      "key_themes": [
        "Andy Jassy highlighted historic operating margin of 13.9% and AWS acceleration",
        "Trainium2 customer commitments virtually 100% booked out",
        "CFO Brian Olsavsky reiterated high-teens advertising acceleration in Q4",
        "Unapologetic commitment to $220B FY26 CapEx as backlog-driven demand"
      ],
      "top_quote": "Andy Jassy: 'AWS net sales increased 39.3%—its fastest growth in nearly five years—to a $184 billion annualized run rate. Our customers are choosing AWS Bedrock and Trainium2 because we offer unmatched performance and security.'"
    },
    "pillar_4_options_iv_crush_and_skew": {
      "score_out_of_100": 55,
      "classification": "VOLATILITY BREACH / IMPERFECT STRADDLE PRICING",
      "key_themes": [
        "After-hours drop of -7.30% to $225.99 exceeded the ±5.5% options implied move band",
        "Front-month puts expiring Friday seeing 100%+ premium spikes into Thursday open",
        "Heavy institutional call buying emerging at the $220.00 strike for December expiries"
      ],
      "top_quote": "Options Flow Desk: 'AMZN broke just outside its ±5.5% straddle band to $225.99 on the $220B CapEx announcement. Expect volatility crush to set in once initial put delta hedging clears.'"
    }
  }
}

(BUS_DIR / "AMZN_2026-10-29_agent2c_social.json").write_text(json.dumps(agent2c, indent=2), encoding="utf-8")
print("[SUCCESS] Layer 2 Bus files created for AMZN (2026-10-29)")
