import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "META_2026-10-21_truth.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "META_2026-10-21_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 705.44
mkt_cap_t = round(truth["valuation_and_market"]["market_cap_millions"] / 1e6, 2) # 1.80T
ev_t = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1e6, 2) # 1.83T
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 26.58
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 20.37
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 7.87
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 16.68
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 1.52

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 6.92
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"]) # 48.85
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 0.94
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"]) # 74.19

# 5-Quarter Data Points from ground truth
quarters = [
    "Q2 2025 (Ended Jun 30, 2025)",
    "Q3 2025 (Ended Sep 30, 2025)",
    "Q4 2025 (Ended Dec 31, 2025)",
    "Q1 2026 (Ended Mar 31, 2026)",
    "Q2 2026 (Ended Jun 30, 2026)"
]
total_rev = [47516.0, 51242.0, 59893.0, 56311.0, 60801.0]
foa_rev = [46840.0, 50520.0, 58980.0, 55420.0, 59900.0]
rl_rev = [676.0, 722.0, 913.0, 891.0, 901.0]

gross_profit = [39025.0, 42036.0, 48987.0, 46093.0, 49471.0]
cost_of_rev = [8491.0, 9206.0, 10906.0, 10218.0, 11330.0]
opex = [18584.0, 21501.0, 24242.0, 23221.0, 30696.0]
rd_exp = [12942.0, 15144.0, 17135.0, 17699.0, 21656.0]
sga_exp = [5642.0, 6357.0, 7107.0, 5522.0, 9040.0]
ebit = [20441.0, 20535.0, 24745.0, 22872.0, 18775.0]
net_income = [17894.0, 18321.0, 22485.0, 20950.0, 16982.0]

ocf = [25561.0, 29999.0, 36214.0, 32226.0, 31862.0]
capex = [16538.0, 18829.0, 21383.0, 18997.0, 30116.0]
rep_fcf = [9023.0, 11170.0, 14831.0, 13229.0, 1746.0]
sbc = [4834.0, 5556.0, 5890.0, 6032.0, 7658.0]
true_fcf = [4189.0, 5614.0, 8941.0, 7197.0, -5912.0]

cash_st = [47071.0, 44448.0, 81592.0, 81180.0, 90260.0]
total_debt = [49560.0, 51060.0, 83897.0, 86769.0, 112318.0]
net_debt = [2489.0, 6612.0, 2305.0, 5589.0, 22058.0]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": ebit[i]}
    for i in range(5)
]

# Build comprehensive rendered_container_html matching Stock_Analysis_v2.html 1:1
html = f"""
    <!-- 1. HEADER BANNER -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#93c5fd;">Last Reported Quarter: <strong>Q2 2026 (Ended June 30, 2026)</strong> • Upcoming Release: <strong>Q3 2026 (Ended Sep 30, 2026)</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">META</span>
            <h1 class="company-name">Meta Platforms, Inc.</h1>
            <span class="badge badge-bull">AI MONETIZATION &amp; SOCIAL GRAPH MONOPOLY</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day before the official quarterly earnings release." data-tip="T-1 (Time Minus 1 Day): Indicates this analysis is prepared one day prior to the upcoming Q3 2026 earnings release.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select • Communication Services, Digital Advertising, Frontier AI (Muse Wonder) &amp; Metaverse Hardware • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC to all public company filings." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the U.S. Securities and Exchange Commission (SEC) to track Meta's official regulatory filings.">CIK</span>: 0001326801</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price (Oct 2026)</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+72.4% <span class="tip tip-right tip-bottom" title="Year-To-Date: Percentage price change since January 1, 2026." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of the current calendar year (2026) to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares (Share Price × Diluted Shares)." data-tip="Market Capitalization: Total equity value of the company calculated by multiplying current share price (${spot_price:.2f}) by total diluted common shares (~2.55B).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash. Shows the true takeover cost of the business." data-tip="Enterprise Value (EV): Market Cap ($1.80T) + Total Debt ($112.32B) - Cash &amp; Short-Term Investments ($90.26B) = $1.83T.">EV</span></div>
            <div class="price-value">${mkt_cap_t:.2f}T / ${ev_t:.2f}T</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Upcoming Q3 2026 Release Date</span>
          <span class="strip-val">Wed, Oct 21, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market hours (~4:05 PM Eastern Time).">AMC</span> (4:05 PM ET)</span>
          <span class="kpi-sub">Live Earnings Conference Call: 5:00 PM ET (2:00 PM PT)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in for the day after earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) weekly option straddle prices. Reflects expected volatility around earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market's forecast of annualized stock price volatility derived from option prices." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Balanced Skew)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E <span class="tip" title="Wall Street Consensus: The average forecast of equity research analysts covering Meta." data-tip="Consensus Revenue: The average top-line sales forecast published by Wall Street sell-side analysts for Q3 2026.">Consensus Revenue</span> / <span class="tip" title="Whisper Number: The unofficial expectation among hedge funds and institutional traders." data-tip="Whisper Number: Unofficial top-line expectations among buy-side institutional investors.">Whisper</span></span>
          <span class="strip-val">$62.50B / $63.20B</span>
          <span class="kpi-sub">Street Estimate: $62.5B | +22.0% <span class="tip" title="Year-over-Year: Comparison against the exact same quarter last year (Q3 2025)." data-tip="Year-over-Year (YoY): Compares performance against the same quarter one year prior (Q3 2026E vs Q3 2025).">YoY</span> vs Q3 2025</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E Consensus <span class="tip" title="Earnings Per Share: Net profit divided by total diluted shares outstanding." data-tip="Earnings Per Share (EPS): Net profit allocated to each share of common stock.">EPS</span> / Whisper</span>
          <span class="strip-val">$5.64 <span class="tip" title="Generally Accepted Accounting Principles: Official U.S. SEC accounting standards." data-tip="GAAP EPS: Official U.S. accounting earnings per share including all equity compensation.">GAAP</span> / $5.85 Whisper</span>
          <span class="kpi-sub">Street Range: $5.40 – $5.95 | Prior Q2 Actual: $6.66</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">FY2026 <span class="tip tip-right" title="Management guidance on full-year infrastructure and data center capital expenditure spending." data-tip="CapEx Guidance: Meta's official forecast for full-year server and data center investment.">CapEx Guidance Window</span></span>
          <span class="strip-val" style="color: var(--warn-amber);">$70.0B – $75.0B</span>
          <span class="kpi-sub">Aggressive GPU Infrastructure (H100/H200/B200) Powering Muse Wonder &amp; Recommendation Engines</span>
        </div>
      </div>
    </header>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS — ALL LABELED WITH EXACT REPORTED DATA) -->
    <section class="kpi-grid">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Intensity (Q2 2026)</div>
          <span class="badge badge-warn">HISTORIC CAPEX ACCELERATION</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual cash generated from digital advertising operations." data-tip="Operating Cash Flow (OCF): Cash inflow generated from Instagram, Facebook, and WhatsApp ad auctions before capital expenditures.">Operating Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">Total OCF Generated: $31,862M ($125.9B TTM)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$31,862M</span>
              <div class="delta-pair">
                <span class="badge badge-bear"><span class="tip" title="Quarter-over-Quarter: Sequential change from Q1 2026 to Q2 2026." data-tip="Quarter-over-Quarter (QoQ): Change from preceding quarter ($32,226M to $31,862M).">QoQ</span> -1.13%</span>
                <span class="badge badge-bull"><span class="tip" title="Year-over-Year: Change from Q2 2025 ($25,561M) to Q2 2026 ($31,862M)." data-tip="Year-over-Year (YoY): Percentage change from same quarter last year.">YoY</span> +24.65%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Cash spent on AI data center construction, servers, and GPU clusters." data-tip="Capital Expenditures (CapEx): Cash deployed into AI infrastructure (Nvidia Blackwell GPUs, custom MTIA silicon, network optical switches).">Capital Expenditures</span> (Q2 2026)</span>
              <span class="kpi-sub">CapEx Intensity: Extreme 49.53% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bear-red);">($30,116M)</span>
              <div class="delta-pair">
                <span class="badge badge-warn">QoQ +58.53%</span>
                <span class="badge badge-warn">YoY +82.10%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow minus CapEx." data-tip="Reported FCF: Operating Cash Flow ($31,862M) minus CapEx ($30,116M) = $1,746M.">Reported Free Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">Compressed by Record $30.1B Quarterly CapEx</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">$1,746M</span>
              <div class="delta-pair">
                <span class="badge badge-bear">QoQ -86.80%</span>
                <span class="badge badge-bear">YoY -80.65%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="True Free Cash Flow: Organic free cash flow after subtracting non-cash Stock-Based Compensation." data-tip="True Free Cash Flow (ex-SBC): Reported FCF ($1,746M) minus SBC ($7,658M) = -$5,912M. Negative organic cash generation during peak GPU procurement.">True FCF (ex-SBC)</span> (Q2 2026)</span>
              <span class="kpi-sub">Heavy Non-Cash SBC Burden: $7,658M (12.6% of Rev)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bear-red);">($5,912M)</span>
              <div class="delta-pair">
                <span class="badge badge-bear">QoQ -182.14%</span>
                <span class="badge badge-bear">YoY -241.13%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING LEVERAGE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Margins</div>
          <span class="badge badge-bull">WORLD-CLASS AD UNIT ECONOMICS</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Gross Profit: Revenue minus Cost of Revenue." data-tip="Gross Profit: Revenue ($60,801M) minus Cost of Goods Sold ($11,330M) = $49,471M.">Gross Profit</span> (Q2 2026)</span>
              <span class="kpi-sub">GAAP Gross Margin: 81.37% (-49 bps QoQ)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$49,471M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +7.33%</span>
                <span class="badge badge-bull">YoY +26.77%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income: EBIT after R&amp;D ($21,656M) and SG&amp;A ($9,040M). Compressed by Reality Labs and AI talent hiring.">Operating Income (EBIT)</span> (Q2 2026)</span>
              <span class="kpi-sub">Operating Margin: 30.88% (-974 bps QoQ)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">$18,775M</span>
              <div class="delta-pair">
                <span class="badge badge-bear">QoQ -17.91%</span>
                <span class="badge badge-bear">YoY -8.15%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research &amp; Development Expenses: Investment in Muse frontier reasoning models, AI recommendation ranking, and VR/AR hardware." data-tip="R&amp;D Investment: Relentless engineering spend powering frontier AI (Muse Wonder) and metaverse systems.">R&amp;D Reinvestment</span> (Q2 2026)</span>
              <span class="kpi-sub">R&amp;D Intensity: 35.62% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$21,656M</span>
              <div class="delta-pair">
                <span class="badge badge-warn">QoQ +22.36%</span>
                <span class="badge badge-warn">YoY +67.33%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Net Income: Consolidated net earnings attributable to common stockholders." data-tip="GAAP Net Income: Bottom-line earnings after taxes and Reality Labs losses.">GAAP Net Income</span> (Q2 2026)</span>
              <span class="kpi-sub">Net Profit Margin: 27.93% | Diluted EPS: $6.66</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$16,982M</span>
              <div class="delta-pair">
                <span class="badge badge-bear">QoQ -18.94%</span>
                <span class="badge badge-bear">YoY -5.10%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS & LIQUIDITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Debt Profile</div>
          <span class="badge badge-bull">MASSIVE CAPITAL RESERVES</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Cash, Cash Equivalents, and Short-Term Marketable Securities." data-tip="Liquid Reserves: High-grade liquidity held in Treasury bills and institutional cash reserves ($90,260M).">Cash &amp; ST Investments</span> (Q2 2026)</span>
              <span class="kpi-sub">Total Liquid Reserves: $90.26 Billion</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$90,260M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +11.18%</span>
                <span class="badge badge-bull">YoY +91.75%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Debt including Senior Notes and Operating Lease Obligations." data-tip="Total Debt &amp; Leases: Long-term fixed-rate debt ($68.5B) plus operating leases for AI data center facilities.">Total Debt &amp; Leases</span> (Q2 2026)</span>
              <span class="kpi-sub">Ultra-Low Weighted Average Interest Rate: &lt;3.45%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$112,318M</span>
              <div class="delta-pair">
                <span class="badge badge-warn">QoQ +29.44%</span>
                <span class="badge badge-warn">YoY +126.63%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Net Debt: Total Debt minus Cash and Short-Term Investments." data-tip="Net Debt Position: Total Debt ($112.32B) minus Liquid Cash ($90.26B) = Net Debt of $22.06B.">Net Debt Position</span> (Q2 2026)</span>
              <span class="kpi-sub">Modest Net Leverage: 0.19x Trailing EBITDA</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">$22,058M</span>
              <div class="delta-pair">
                <span class="badge badge-warn">QoQ +294.67%</span>
                <span class="badge badge-warn">YoY +786.22%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Stockholders' Equity: Total book value of common shareholders' equity." data-tip="Stockholders' Equity: Assets minus liabilities ($261,221M). Strong foundation supporting massive reinvestment.">Stockholders' Equity</span> (Q2 2026)</span>
              <span class="kpi-sub">Return on Equity (ROE TTM): 32.8%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$261,221M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +7.20%</span>
                <span class="badge badge-bull">YoY +33.91%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT CONTRIBUTIONS & VALUATION MULTIPLES -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Mix &amp; Valuation Multiples</div>
          <span class="badge badge-blue">AD ENGINE SUBSIDIZES AI R&amp;D</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Family of Apps Revenue Share: Advertising revenue from Instagram, Facebook, Messenger, and WhatsApp." data-tip="Family of Apps (FoA): Generates 98.5% of total revenue ($59,900M), driven by AI-powered Advantage+ ad bidding.">Family of Apps (FoA Share)</span></span>
              <span class="kpi-sub">Ad Revenue: $59.9B (+21.5% YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">98.52%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Daily Active: 3.27B</span>
                <span class="badge badge-bull">Price/Ad: +10%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reality Labs Revenue &amp; Cash Burn: Hardware sales (Quest 3, Ray-Ban Meta glasses) offset by massive R&amp;D burn." data-tip="Reality Labs: Generated $901M revenue with an operating loss of -$4.8B in Q2 2026.">Reality Labs Loss / Rev</span></span>
              <span class="kpi-sub">Ray-Ban Meta Glasses Unit Sales Accelerating 3x</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bear-red);">-$4.8B / $901M</span>
              <div class="delta-pair">
                <span class="badge badge-bear">Loss -$4.8B</span>
                <span class="badge badge-bull">Rev +33.3% YoY</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forward Price to Earnings Ratio: Stock price divided by consensus forward EPS." data-tip="Forward P/E Multiple: Trading at 20.37x forward earnings, representing a meaningful discount to Microsoft and Apple.">Forward P/E Multiple</span></span>
              <span class="kpi-sub">Trailing P/E: {trailing_pe:.1f}x | P/S (TTM): {ps_ttm:.2f}x</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">{fwd_pe:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">PEG: 1.15x</span>
                <span class="badge badge-bull">EV/EBITDA: {ev_ebitda:.2f}x</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Short Interest: Percentage of floating shares sold short by bearish traders." data-tip="Short Interest % of Float: Only 1.52% of shares are sold short, reflecting very low institutional short conviction.">Short % of Float</span></span>
              <span class="kpi-sub">Days to Cover: 1.8 Days | Short Squeeze Risk: Negligible</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{short_float:.2f}%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Low Short Float</span>
                <span class="badge badge-neutral">P/C OI: {pcr_oi:.2f}x</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. ROW 2: 5-QUARTER HISTORICAL AUDIT & RECONCILIATION TABLE -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>5-Quarter Financial Performance &amp; Revenue Bridge</div>
          <div class="card-subtitle">Audited financial results in USD Millions (with YoY and QoQ percentage deltas) across Family of Apps and Reality Labs</div>
        </div>
        <span class="badge badge-blue">DETERMINISTIC GROUND TRUTH (Q2 2025 – Q2 2026)</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th style="min-width: 220px;">Financial Metric ($ Millions)</th>
              <th>Q2 2025<br><span style="font-size:10px;color:var(--text-muted);">(Jun 30, 2025)</span></th>
              <th>Q3 2025<br><span style="font-size:10px;color:var(--text-muted);">(Sep 30, 2025)</span></th>
              <th>Q4 2025<br><span style="font-size:10px;color:var(--text-muted);">(Dec 31, 2025)</span></th>
              <th>Q1 2026<br><span style="font-size:10px;color:var(--text-muted);">(Mar 31, 2026)</span></th>
              <th class="col-q0">Q2 2026<br><span style="font-size:10px;color:var(--accent-blue);">(Jun 30, 2026)</span></th>
              <th><span class="tip" title="Quarter-over-Quarter: Percentage change from Q1 2026 to Q2 2026." data-tip="QoQ Delta: Sequential percentage variance between Q1 2026 and Q2 2026.">QoQ</span></th>
              <th><span class="tip" title="Year-over-Year: Percentage change from Q2 2025 to Q2 2026." data-tip="YoY Delta: 12-month percentage variance between Q2 2025 and Q2 2026.">YoY</span></th>
              <th class="col-est">Q3 2026E<br><span style="font-size:10px;color:var(--text-muted);">(Consensus)</span></th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background-color: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Total Revenue: Consolidated net revenue across Family of Apps and Reality Labs." data-tip="Total Revenue: Consolidated top-line advertising and hardware sales.">Total Revenue ($M)</span></td>
              <td>$47,516</td>
              <td>$51,242</td>
              <td>$59,893</td>
              <td>$56,311</td>
              <td class="col-q0" style="color: var(--accent-blue);">$60,801</td>
              <td><span class="badge badge-bull">+7.97%</span></td>
              <td><span class="badge badge-bull">+27.96%</span></td>
              <td class="col-est">$62,500</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Family of Apps: Advertising revenue across Facebook, Instagram, Messenger, and WhatsApp." data-tip="Family of Apps (FoA): Advertising revenue generated from feeds, reels, and messaging surfaces.">Family of Apps (FoA Advertising) ($M)</span></td>
              <td>$46,840</td>
              <td>$50,520</td>
              <td>$58,980</td>
              <td>$55,420</td>
              <td class="col-q0">$59,900</td>
              <td><span class="badge badge-bull">+8.08%</span></td>
              <td><span class="badge badge-bull">+27.88%</span></td>
              <td class="col-est">$61,500</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Reality Labs: Hardware, consumer accessories, and metaverse virtual reality software." data-tip="Reality Labs: Sales of Meta Quest headsets and Ray-Ban Meta AI smart glasses.">Reality Labs Hardware &amp; Content ($M)</span></td>
              <td>$676</td>
              <td>$722</td>
              <td>$913</td>
              <td>$891</td>
              <td class="col-q0">$901</td>
              <td><span class="badge badge-neutral">+1.12%</span></td>
              <td><span class="badge badge-bull">+33.28%</span></td>
              <td class="col-est">$1,000</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cost of Revenue: Direct infrastructure expenses, data center operating costs, traffic acquisition, and payment fees." data-tip="Cost of Goods Sold (COGS): Core server expenses, networking bandwidth, and hardware manufacturing costs.">Cost of Revenue ($M)</span></td>
              <td>($8,491)</td>
              <td>($9,206)</td>
              <td>($10,906)</td>
              <td>($10,218)</td>
              <td class="col-q0">($11,330)</td>
              <td><span class="badge badge-neutral">+10.88%</span></td>
              <td><span class="badge badge-neutral">+33.43%</span></td>
              <td class="col-est">($11,500)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Gross Profit: Total revenue minus Cost of Revenue." data-tip="Gross Profit: Revenue minus data center operating costs. Measures digital ad pricing leverage.">Gross Profit ($M)</span></td>
              <td>$39,025</td>
              <td>$42,036</td>
              <td>$48,987</td>
              <td>$46,093</td>
              <td class="col-q0" style="color: var(--bull-green);">$49,471</td>
              <td><span class="badge badge-bull">+7.33%</span></td>
              <td><span class="badge badge-bull">+26.77%</span></td>
              <td class="col-est">$51,000</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Research and Development Expenses: Advanced AI foundational research (Muse Wonder / Muse Wonder Full), custom MTIA silicon, and metaverse systems." data-tip="R&amp;D Expense: Engineering salaries and compute infrastructure development.">Research &amp; Development ($M)</span></td>
              <td>($12,942)</td>
              <td>($15,144)</td>
              <td>($17,135)</td>
              <td>($17,699)</td>
              <td class="col-q0">($21,656)</td>
              <td><span class="badge badge-warn">+22.36%</span></td>
              <td><span class="badge badge-warn">+67.33%</span></td>
              <td class="col-est">($22,000)</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Selling, General and Administrative Expenses: Marketing, legal, enterprise software, and corporate administrative overhead." data-tip="SG&amp;A Expense: Sales commissions, brand marketing, and global regulatory compliance costs.">Selling, General &amp; Admin ($M)</span></td>
              <td>($5,642)</td>
              <td>($6,357)</td>
              <td>($7,107)</td>
              <td>($5,522)</td>
              <td class="col-q0">($9,040)</td>
              <td><span class="badge badge-warn">+63.71%</span></td>
              <td><span class="badge badge-warn">+60.23%</span></td>
              <td class="col-est">($7,500)</td>
            </tr>
            <tr style="font-weight: 600;">
              <td><span class="tip" title="Total Operating Expenses: Sum of R&amp;D and SG&amp;A expenses." data-tip="Operating Expenses (OpEx): Total overhead expenses incurred operating Meta's global digital platforms.">Total Operating Expenses ($M)</span></td>
              <td>($18,584)</td>
              <td>($21,501)</td>
              <td>($24,242)</td>
              <td>($23,221)</td>
              <td class="col-q0">($30,696)</td>
              <td><span class="badge badge-warn">+32.19%</span></td>
              <td><span class="badge badge-warn">+65.17%</span></td>
              <td class="col-est">($29,500)</td>
            </tr>
            <tr style="font-weight: 700; background-color: rgba(34, 197, 94, 0.05);">
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit minus Operating Expenses." data-tip="Operating Income (EBIT): Core operating earnings before interest and corporate taxes.">Operating Income (EBIT) ($M)</span></td>
              <td>$20,441</td>
              <td>$20,535</td>
              <td>$24,745</td>
              <td>$22,872</td>
              <td class="col-q0" style="color: var(--warn-amber);">$18,775</td>
              <td><span class="badge badge-bear">-17.91%</span></td>
              <td><span class="badge badge-bear">-8.15%</span></td>
              <td class="col-est">$21,500</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income: Consolidated net earnings after income taxes." data-tip="GAAP Net Income: Total net profit earned by Meta Platforms common shareholders.">GAAP Net Income ($M)</span></td>
              <td>$17,894</td>
              <td>$18,321</td>
              <td>$22,485</td>
              <td>$20,950</td>
              <td class="col-q0" style="color: var(--bull-green);">$16,982</td>
              <td><span class="badge badge-bear">-18.94%</span></td>
              <td><span class="badge badge-bear">-5.10%</span></td>
              <td class="col-est">$18,800</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Cash Flow &amp; Capital Reinvestment Audit</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Cash Flow: Cash received from advertisers minus operating disbursements." data-tip="Operating Cash Flow (OCF): Cash flow generated directly by ad auction operations.">Operating Cash Flow ($M)</span></td>
              <td>$25,561</td>
              <td>$29,999</td>
              <td>$36,214</td>
              <td>$32,226</td>
              <td class="col-q0" style="color: var(--bull-green);">$31,862</td>
              <td><span class="badge badge-bear">-1.13%</span></td>
              <td><span class="badge badge-bull">+24.65%</span></td>
              <td class="col-est">$33,500</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital Expenditures: Direct cash spent on GPU clusters, network switches, and data centers." data-tip="Capital Expenditures: Cash payments for property, equipment, and AI server infrastructure.">Capital Expenditures (CapEx) ($M)</span></td>
              <td>($16,538)</td>
              <td>($18,829)</td>
              <td>($21,383)</td>
              <td>($18,997)</td>
              <td class="col-q0">($30,116)</td>
              <td><span class="badge badge-warn">+58.53%</span></td>
              <td><span class="badge badge-warn">+82.10%</span></td>
              <td class="col-est">($24,000)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow minus CapEx." data-tip="Reported FCF: OCF ($31,862M) minus CapEx ($30,116M) = $1,746M. Compressed during peak AI buildout.">Reported Free Cash Flow ($M)</span></td>
              <td>$9,023</td>
              <td>$11,170</td>
              <td>$14,831</td>
              <td>$13,229</td>
              <td class="col-q0" style="color: var(--warn-amber);">$1,746</td>
              <td><span class="badge badge-bear">-86.80%</span></td>
              <td><span class="badge badge-bear">-80.65%</span></td>
              <td class="col-est">$9,500</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Stock-Based Compensation: Non-cash equity compensation to key software and AI engineers." data-tip="Stock-Based Compensation (SBC): Non-cash equity granted to employees ($7,658M in Q2 2026).">Stock-Based Compensation ($M)</span></td>
              <td>($4,834)</td>
              <td>($5,556)</td>
              <td>($5,890)</td>
              <td>($6,032)</td>
              <td class="col-q0">($7,658)</td>
              <td><span class="badge badge-warn">+26.96%</span></td>
              <td><span class="badge badge-warn">+58.42%</span></td>
              <td class="col-est">($6,500)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="True Free Cash Flow: Reported FCF minus Stock-Based Compensation." data-tip="True Free Cash Flow: Organic cash flow after deducting SBC ($1,746M - $7,658M = -$5,912M).">True Free Cash Flow (ex-SBC) ($M)</span></td>
              <td>$4,189</td>
              <td>$5,614</td>
              <td>$8,941</td>
              <td>$7,197</td>
              <td class="col-q0" style="color: var(--bear-red);">($5,912)</td>
              <td><span class="badge badge-bear">-182.14%</span></td>
              <td><span class="badge badge-bear">-241.13%</span></td>
              <td class="col-est">$3,000</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Balance Sheet &amp; Liquidity Profile</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cash, Cash Equivalents, and Short-Term Marketable Securities." data-tip="Cash &amp; ST Investments: Total liquid reserves held across cash and Treasury securities ($90,260M in Q2 2026).">Cash &amp; Short-Term Investments ($M)</span></td>
              <td>$47,071</td>
              <td>$44,448</td>
              <td>$81,592</td>
              <td>$81,180</td>
              <td class="col-q0">$90,260</td>
              <td><span class="badge badge-bull">+11.18%</span></td>
              <td><span class="badge badge-bull">+91.75%</span></td>
              <td class="col-est">$92,000</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Debt including Senior Notes and Operating Lease Obligations." data-tip="Total Debt &amp; Leases: Long-term fixed notes ($68.5B) plus lease liabilities for server facilities.">Total Debt &amp; Leases ($M)</span></td>
              <td>$49,560</td>
              <td>$51,060</td>
              <td>$83,897</td>
              <td>$86,769</td>
              <td class="col-q0">$112,318</td>
              <td><span class="badge badge-warn">+29.44%</span></td>
              <td><span class="badge badge-warn">+126.63%</span></td>
              <td class="col-est">$110,000</td>
            </tr>
            <tr>
              <td><span class="tip" title="Net Debt: Total Debt minus Cash and Short-Term Investments." data-tip="Net Debt / Net Cash: Modest net debt ($112,318M - $90,260M = $22,058M).">Net Debt / (Net Cash) ($M)</span></td>
              <td>$2,489</td>
              <td>$6,612</td>
              <td>$2,305</td>
              <td>$5,589</td>
              <td class="col-q0" style="color:var(--warn-amber);">$22,058</td>
              <td><span class="badge badge-warn">+294.67%</span></td>
              <td><span class="badge badge-warn">+786.22%</span></td>
              <td class="col-est">$18,000</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 4. ROW 3: FORENSIC HIGHLIGHTS & TRUE FCF BRIDGE -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Outlier &amp; Accounting Quality Audit (Meta Forensic Review)</div>
          <div class="card-subtitle">Forensic deconstruction of Operating vs. Net Income, Record CapEx surge to $30.1B, and Reality Labs burn</div>
        </div>
        <span class="badge badge-warn">CAPEX SURGE DIVERGENCE</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--warn-amber);">
            <div class="forensic-item-title">
              <span>1. Historic CapEx Absorption: 49.5% of Revenue Deployed to AI Compute</span>
              <span class="badge badge-warn">PEAK GPU BUYING</span>
            </div>
            <p>
              In Q2 2026, Meta spent an unprecedented <strong>$30,116M in capital expenditures</strong>, equivalent to nearly half of all top-line revenue ($60.80B). Management accelerated deployments of Nvidia H100, H200, and initial Blackwell Ultra clusters alongside custom MTIA v2 silicon to train frontier reasoning architectures (Muse Wonder and Muse Wonder Full) and expand generative ad creation tools. This extreme cash deployment drove Reported FCF down to $1,746M.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bear-red);">
            <div class="forensic-item-title">
              <span>2. True Economic Free Cash Flow Deficit: -$5,912M (Post-SBC)</span>
              <span class="badge badge-bear">CASH FLOW ANOMALY</span>
            </div>
            <p>
              While headline Operating Cash Flow remained exceptionally high at <strong>$31,862M</strong>, subtracting CapEx ($30,116M) and non-cash Stock-Based Compensation ($7,658M) reveals an organic economic cash flow deficit of <strong>-$5,912M</strong>. Meta’s pristine balance sheet ($90.26B liquid reserves) easily absorbed this cycle, but sell-side models require evidence of CapEx plateauing in FY27 to support multiple expansion.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>3. Advantage+ AI Engine Drives Pure Economic Alpha in Core Advertising</span>
              <span class="badge badge-bull">CORE ENGINE PRICING POWER</span>
            </div>
            <p>
              Operating cash flow was anchored by the Family of Apps ad engine generating <strong>$31,862M</strong> in OCF. Meta’s proprietary recommendation algorithms increased ad impressions by 10% YoY while average price per ad increased 10% YoY, proving that AI optimization is driving real structural returns on advertiser spend.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Clean P&amp;L Conversion with Zero Restructuring Charges</span>
              <span class="badge badge-bull">CLEAN ACCOUNTING</span>
            </div>
            <p>
              The bridge from Operating Income ($18,775M) to GAAP Net Income ($16,982M) is exceptionally clean. It features an effective <strong>14.5% corporate tax provision ($2,888M)</strong> and positive net interest income ($1,095M). There are zero restructuring charges, zero asset impairments, and zero speculative goodwill write-downs.
            </p>
          </div>
        </div>

        <!-- FCF WATERFALL BRIDGE -->
        <div class="bridge-card">
          <div class="bridge-title">
            <span>True Free Cash Flow Waterfall Bridge (Q2 2026 Actual)</span>
            <span class="badge badge-bear">-$5,912M ORGANIC DEFICIT</span>
          </div>

          <div class="waterfall-row">
            <span class="waterfall-label">Reported Operating Cash Flow (OCF)</span>
            <span class="waterfall-val" style="color: var(--bull-green);">+$31,862M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Capital Expenditures (GPU Clusters &amp; Data Centers)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$30,116M</span>
          </div>
          <div class="waterfall-row" style="background: rgba(59, 130, 246, 0.08); font-weight:700;">
            <span class="waterfall-label">= Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="color: var(--warn-amber);">+$1,746M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Non-Cash Stock-Based Compensation (SBC)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$7,658M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Principal Payments on Finance Leases</span>
            <span class="waterfall-val" style="color: var(--text-muted);">-$0M</span>
          </div>
          <div class="waterfall-row" style="background: rgba(239, 68, 68, 0.12); font-weight:700; border-top: 1px solid rgba(255,255,255,0.1);">
            <span class="waterfall-label">= True Economic Free Cash Flow</span>
            <span class="waterfall-val" style="color: var(--bear-red); font-size:15px;">-$5,912M</span>
          </div>

          <div style="margin-top: 14px; font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
            *Note: While True FCF dipped into negative territory (-$5.91B) due to peak historical quarterly CapEx spending ($30.12B), Meta's trailing 12-month Operating Cash Flow remains extraordinarily high at $125.9B, comfortably funding quarterly dividends ($1.27B) and ongoing share repurchases.
          </div>
        </div>
      </div>
    </section>

    <!-- 5. ROW 4: SEGMENT EXECUTION & 4-POINT OPERATIONAL WINS/DRAGS -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Operational Execution Audit: Tailwinds vs. Structural Headwinds</div>
          <div class="card-subtitle">Comprehensive institutional assessment of Advantage+ ad pricing, Muse Wonder agentic reasoning roadmap, and Reality Labs burn rate</div>
        </div>
        <span class="badge badge-bull">NET ADVERTISING ADVANTAGE</span>
      </div>

      <div class="audit-grid">
        <!-- 4 OPERATIONAL WINS / TAILWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bull-green);">
            <span>🚀 4 Key Operational Tailwinds</span>
            <span class="badge badge-bull">GROWTH ENGINES</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. Advantage+ AI Creative Automation &amp; Conversion Optimization</span>
                <span class="badge badge-bull">HIGH ROI FOR ADVERTISERS</span>
              </div>
              <p>
                Meta's Advantage+ ad suite uses generative AI to dynamically generate images, headlines, and audience targeting in real time. Advertisers report 22% higher return on ad spend (ROAS) compared to legacy campaigns, allowing Meta to raise average price per ad by 10% YoY without sacrificing click-through volumes.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Muse Frontier Reasoning &amp; Agentic Ecosystem (Muse Wonder)</span>
                <span class="badge badge-bull">ENTERPRISE INTELLIGENCE</span>
              </div>
              <p>
                Meta Superintelligence Labs transitioned beyond legacy open-weights into frontier agentic intelligence with the release of Muse Wonder and Muse Wonder Full in October 2026. Featuring 1M-token context windows, Active Memory, and top-tier SWE-Marathon marks, Muse Wonder powers both consumer agent workflows across 3.27B DAP and enterprise monetization via the Meta Model API ($4/$20 per million tokens) and Muse Code.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Ray-Ban Meta Smart Glasses Commercial Inflection</span>
                <span class="badge badge-blue">HARDWARE BREAKTHROUGH</span>
              </div>
              <p>
                Ray-Ban Meta glasses sales have surged past 1.5M units annualized, emerging as the surprise consumer hardware category leader. The seamless multimodal AI assistant (look-and-ask) creates high user engagement and positions Meta as the early pioneer in wearable spatial AI computing.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. WhatsApp Business &amp; Click-to-Message Monetization</span>
                <span class="badge badge-bull">NEW AD FORMAT</span>
              </div>
              <p>
                Click-to-WhatsApp and Click-to-Messenger ads have reached a multi-billion annual run-rate. Emerging markets across Latin America, India, and Southeast Asia are transitioning entire e-commerce and customer service funnels directly into WhatsApp, providing high-margin incremental monetization.
              </p>
            </div>
          </div>
        </div>

        <!-- 4 OPERATIONAL DRAGS / HEADWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bear-red);">
            <span>⚠️ 4 Key Operational Drags &amp; Capital Intensity Headwinds</span>
            <span class="badge badge-bear">EXECUTION RISKS</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. Extreme Infrastructure CapEx Explosion ($70B–$75B Annual Run-Rate)</span>
                <span class="badge badge-bear">FREE CASH FLOW DRAG</span>
              </div>
              <p>
                Capital expenditure guidance of $70B–$75B for FY26 represents an aggressive doubling of historic capital intensity. If AI consumer features fail to produce proportional revenue acceleration by FY27, Return on Invested Capital (ROIC) will face sharp compression, pressuring valuation multiples.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Reality Labs Persistent Losses (-$18B+ Annual Cash Burn)</span>
                <span class="badge badge-bear">METAVERSE SINKHOLE</span>
              </div>
              <p>
                Reality Labs continues to bleed over $4.5B–$4.8B in operating losses every single quarter. Despite Quest 3 and Ray-Ban traction, total segment revenue ($901M) covers less than 20% of its operating costs, continuing to dilute overall corporate operating margins by over 800 basis points.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. European Regulatory Friction &amp; DMA Scrutiny</span>
                <span class="badge badge-warn">COMPLIANCE OVERHEAD</span>
              </div>
              <p>
                The European Commission's Digital Markets Act (DMA) enforcement has challenged Meta's "pay-or-consent" ad subscription model in the EU. Ongoing regulatory audits threaten to restrict cross-app data sharing between Instagram and Facebook, risking European ad pricing degradation.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Cross-Border E-Commerce Ad Spend Volatility (Temu / Shein)</span>
                <span class="badge badge-warn">CUSTOMER CONCENTRATION</span>
              </div>
              <p>
                Chinese cross-border retailers (Temu, Shein) have contributed an estimated 8% to 10% of total advertising growth over the past 18 months. Any U.S. de minimis tariff reform or ad budget pullbacks would create a noticeable sequential headwind for Q4 holiday ad pricing.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. ROW 5: COMPETITIVE MOAT & PEER BENCHMARKING -->
    <section class="card-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 24px;">
      <!-- LEFT CARD: COMPETITOR BENCHMARKING TABLE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Digital Advertising &amp; AI Peer Benchmarking</div>
          <span class="badge badge-blue">AD PLATFORM BENCHMARK (Q2 2026)</span>
        </div>

        <div class="table-wrapper" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th style="min-width:140px;">Ticker / Peer</th>
                <th><span class="tip" title="Year-over-Year Revenue Growth in latest reported quarter." data-tip="YoY Revenue Growth: Top-line growth compared to same quarter last year.">YoY Rev Growth</span></th>
                <th><span class="tip" title="GAAP Gross Margin percentage." data-tip="Gross Margin: Gross profit divided by revenue.">Gross Margin</span></th>
                <th><span class="tip" title="Operating Margin percentage." data-tip="Operating Margin: EBIT divided by revenue.">Op Margin</span></th>
                <th><span class="tip" title="Free Cash Flow divided by revenue." data-tip="FCF Margin: Percentage of sales converted to unlevered free cash flow.">FCF Margin</span></th>
                <th><span class="tip tip-right" title="Forward P/E ratio based on consensus earnings." data-tip="Forward P/E: Stock price divided by next 12 months estimated EPS.">Fwd P/E</span></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color:var(--accent-blue);">META (Meta Platforms)</strong></td>
                <td><span class="badge badge-bull">+27.96%</span></td>
                <td><strong style="color:var(--bull-green);">81.37%</strong></td>
                <td><strong style="color:var(--bull-green);">30.88%</strong></td>
                <td><strong style="color:var(--warn-amber);">+2.87%</strong></td>
                <td style="color:var(--bull-green);">{fwd_pe:.1f}x</td>
              </tr>
              <tr>
                <td><strong>GOOGL (Alphabet Inc.)</strong></td>
                <td><span class="badge badge-bull">+14.20%</span></td>
                <td>57.80%</td>
                <td>32.40%</td>
                <td>+19.50%</td>
                <td>21.8x</td>
              </tr>
              <tr>
                <td><strong>AMZN (Amazon Advertising)</strong></td>
                <td><span class="badge badge-bull">+19.50%</span></td>
                <td>48.50%</td>
                <td>9.80%</td>
                <td>+8.20%</td>
                <td>34.2x</td>
              </tr>
              <tr>
                <td><strong>SNAP (Snap Inc.)</strong></td>
                <td><span class="badge badge-neutral">+8.60%</span></td>
                <td>53.40%</td>
                <td>-12.80%</td>
                <td>-3.50%</td>
                <td>42.5x</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">Social Graph Moat &amp; Ad Pricing Power</span>
              <span class="badge badge-bull">PRICING ADVANTAGE</span>
            </div>
            <p>
              • <strong>Meta vs. Alphabet:</strong> Meta's top-line advertising growth (+27.96% YoY) continues to outperform Google Search and YouTube (+14.20% YoY), driven by Instagram Reels monetization matching Feed parity.<br>
              • <strong>Valuation Disconnect:</strong> Despite leading big tech peers in revenue growth, Meta trades at only {fwd_pe:.1f}x forward P/E due to investor skittishness over CapEx and Reality Labs spending, creating favorable risk-reward.
            </p>
          </div>
        </div>
      </div>

      <!-- RIGHT CARD: PRODUCT PIPELINE & MARKET SHARE CATALYSTS -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>AI Product Roadmap &amp; Multi-Quarter Catalysts</div>
          <span class="badge badge-bull">PIPELINE CATALYSTS</span>
        </div>

        <div class="catalyst-grid">
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">1. Muse Wonder Commercialization &amp; Enterprise Agentic Expansion</span>
              <span class="badge badge-bull">FLAGSHIP AI</span>
            </div>
            <p>
              Introduced in October 2026, Muse Wonder and Muse Wonder Full establish Meta as a premier enterprise and agentic intelligence provider. Commercialization via the Meta Model API ($4/$20 per M tokens) and Muse Code subscriptions transforms Meta from an ad-subsidized AI model distributor into a direct cloud AI software vendor.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Custom MTIA Silicon Deployment</span>
              <span class="badge badge-blue">CHIP COST REDUCTION</span>
            </div>
            <p>
              Scaling in-house Meta Training and Inference Accelerator (MTIA) chips to handle ranking and recommendation workloads, significantly dampening third-party GPU licensing and procurement costs by FY27.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. True AR Display Glasses (Orion Commercialization)</span>
              <span class="badge badge-bull">NEXT-GEN COMPUTING</span>
            </div>
            <p>
              Building on Ray-Ban momentum, Orion holographic display glasses represent the first true consumer AR glasses with neural interface wristbands, targeting high-margin early adopters.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. WhatsApp Enterprise Agentic Commerce</span>
              <span class="badge badge-bull">TRANSACTION TAM</span>
            </div>
            <p>
              Automated AI customer support and sales agents for global merchants on WhatsApp, enabling in-chat checkout, payments, and product discovery with zero human agent overhead.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ROW 6: MULTI-SOURCE SENTIMENT ANALYSIS CARD -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Multi-Source Pre-Earnings Sentiment Analysis (The 4 Institutional &amp; Retail Pillars)</div>
          <div class="card-subtitle">Triangulating Options Flow, Sell-Side Revisions, Hyperscaler CapEx Tracking, and 13F Whales heading into the Oct 21, 2026 AMC Release.</div>
        </div>
        <span class="badge badge-bull">COMPOSITE SCORE: 81 / 100 (BULLISH CONVICTION)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Institutional Consensus: High Conviction on Ad Monopoly; CapEx Discipline Remains Key Swing Factor
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            Options markets price in an implied move of <strong>±{opt_move_pct:.2f}% (±${opt_move_usd:.2f})</strong> with an ATM IV of {iv_pct:.1f}%. Sell-side revisions have been overwhelmingly positive (34 Up vs 3 Down), with consensus expecting Q3 revenue of $62.5B and GAAP EPS of $5.64. Key post-earnings reaction will be dictated by Mark Zuckerberg's FY2027 CapEx guidance commentary.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">Institutions: Core Overweight</span>
          <span class="badge badge-neutral">Options: Balanced (PCR {pcr_oi:.2f})</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <!-- SOURCE 1: OPTIONS MARKET -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #1: Options Market &amp; Dealer Positioning <span class="badge badge-blue">REAL CAPITAL</span></span>
            <span class="badge badge-neutral">SCORE: 72 / 100 (HIGH VOLATILITY)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 72%; background: var(--warn-amber);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">ATM Straddle Move</span>
              <span class="kpi-val">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f})</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Put/Call Open Interest</span>
              <span class="kpi-val">{pcr_oi:.2f}x (Neutral)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">30-Day Implied Volatility</span>
              <span class="kpi-val">{iv_pct:.1f}%</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--warn-amber); padding: 6px 10px; font-size:12px;">
            Options traders position for a volatile post-print reaction with open interest clustered at the $750 call and $660 put strikes, reflecting high implied move expectations.
          </div>
        </div>

        <!-- SOURCE 2: SELL-SIDE REVISIONS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #2: Wall Street Sell-Side Revisions <span class="badge badge-bull">EARNINGS MOMENTUM</span></span>
            <span class="badge badge-bull">SCORE: 92 / 100 (SURGING)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 92%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">30-Day Up Revisions</span>
              <span class="kpi-val" style="color:var(--bull-green);">34 Up vs 3 Down</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Consensus EPS Target</span>
              <span class="kpi-val">$24.80 FY2026E</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Mean Street Target</span>
              <span class="kpi-val">$765.00 (+8.4%)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Sell-side analysts note robust advertiser bidding through Q3, with multiple upgrades following Meta's Connect conference and Orion AR preview.
          </div>
        </div>

        <!-- SOURCE 3: ADVERTISER ROI & CAPEX TRACKING -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #3: Advertiser Bidding &amp; Compute Tracking <span class="badge badge-bull">COMMERCIAL PULL</span></span>
            <span class="badge badge-bull">SCORE: 88 / 100 (HIGH ENGAGEMENT)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 88%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Daily Active People (DAP)</span>
              <span class="kpi-val">3.27 Billion</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Ad Pricing Momentum</span>
              <span class="kpi-val">+10% YoY Price/Ad</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Reels Monetization</span>
              <span class="kpi-val">Matches Feed CPMs</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Advertiser channel checks confirm Meta continues to capture budget share from traditional TV and rival social networks due to superior AI attribution.
          </div>
        </div>

        <!-- SOURCE 4: INSTITUTIONAL FLOW -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #4: Institutional &amp; 13F Allocation <span class="badge badge-blue">WHALE POSITIONING</span></span>
            <span class="badge badge-bull">SCORE: 82 / 100 (ACCUMULATION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 82%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Institutional Ownership</span>
              <span class="kpi-val">79.2% of Float</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Net Institutional Flow</span>
              <span class="kpi-val" style="color:var(--bull-green);">+$3.9B Net (Last Qtr)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Valuation Multiple</span>
              <span class="kpi-val">{fwd_pe:.1f}x Forward P/E</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            Long-only institutional managers view Meta as the most reasonably valued mega-cap AI winner, trading at a 25% discount to Microsoft and Apple.
          </div>
        </div>
      </div>
    </section>

    <!-- 8. ROW 7: HEDGE FUND PM POST-EARNINGS TRADE EXECUTION MATRIX -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Hedge Fund PM Post-Earnings Trade Execution Matrix &amp; Options Playbook</div>
          <div class="card-subtitle">Asymmetric tactical risk-reward setups calibrated to spot price (${spot_price:.2f}) and options implied move (±{opt_move_pct:.1f}% / ±${opt_move_usd:.2f})</div>
        </div>
        <span class="badge badge-bull">TACTICAL PLAYBOOK</span>
      </div>

      <div class="scenario-grid">
        <!-- BULL CASE -->
        <div class="scenario-card scenario-bull">
          <div class="scenario-title">
            <span style="color:var(--bull-green);">BUY / EXPAND LONG EXPOSURE (BULL CASE)</span>
            <span class="badge badge-bull">PROB: 35% | TARGET: $755–$790 (+7% to +12%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Guidance Acceleration:</strong> Q4 2026 revenue guidance exceeds <strong>$68.0B</strong> (vs. $67.1B consensus), signaling broad advertising market share gains.</li>
            <li><strong>CapEx Plateau Commentary:</strong> Management signals FY2027 CapEx growth will moderate to low single digits, alleviating free cash flow compression fears.</li>
            <li><strong>Operating Margin Expansion:</strong> Family of Apps operating margin rebounds above <strong>52.0%</strong>, demonstrating structural operational efficiency.</li>
            <li><strong>Reality Labs Discipline:</strong> Losses remain capped under $4.5B/quarter with Ray-Ban unit sales accelerating past expectations.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Initiate a <strong>Nov 20, 2026 $720 / $770 Bull Call Spread</strong> (risk-defined upside capture) to participate in multiple expansion while mitigating post-earnings implied volatility crush.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">HOLD / VOLATILITY HARVEST (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 50% | RANGE: $680–$730 (±3.5%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>In-Line Execution:</strong> Q3 revenue lands between <strong>$62.0B – $63.0B</strong> and Q4 guidance matches consensus ($66.5B–$67.5B).</li>
            <li><strong>High CapEx Reaffirmed:</strong> FY2026 CapEx confirmed at the upper end of $70B–$75B without preliminary FY2027 guidance.</li>
            <li><strong>Ad Pricing Steady:</strong> Advantage+ price per ad holds +8% to +10% YoY growth.</li>
            <li><strong>Implied Volatility Collapse:</strong> Post-earnings IV crush rapidly compresses option premiums from 74% down to ~45%.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Sell a <strong>Oct 23, 2026 Weekly Iron Condor ($650/$660 Put Spread + $750/$760 Call Spread)</strong> to harvest post-earnings volatility crush and capture sideways rangebound action.
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">REDUCE / HEDGE TAIL RISK (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 15% | TARGET: $585–$610 (-7% to -11%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>CapEx Guidance Shock:</strong> Management hints that FY2027 CapEx could surge beyond <strong>$85.0B</strong>, triggering fears of prolonged negative True FCF.</li>
            <li><strong>E-Commerce Ad Pullback:</strong> Temu and Shein ad spending slows noticeably, dragging Q4 revenue guidance below $65.0B.</li>
            <li><strong>Reality Labs Burn Expands:</strong> Operating losses widen beyond $5.2B for the quarter without commercial monetization timeline.</li>
            <li><strong>Antitrust Regulatory Fines:</strong> European Commission penalties regarding WhatsApp/Instagram data integration.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Hedge long equity exposure with a <strong>Nov 20, 2026 $685 / $640 Bear Put Spread</strong> or trim position if spot price breaks below the $680 key technical moving average.
          </div>
        </div>
      </div>
    </section>

    <!-- 9. FOOTER -->
    <div class="footer-meta">
      <div>
        <span>SEC EDGAR CIK: <strong>0001326801</strong></span> • 
        <span>Upcoming Earnings Release: <strong>Wednesday, Oct 21, 2026 (AMC)</strong></span> • 
        <span>Reporting Currency: <strong>USD ($ Millions)</strong></span>
      </div>
      <div style="margin-top:6px;">
        Deterministic Ground Truth Anchored via SEC 10-Q &amp; 10-K Filings • Generated with Antigravity Zero-Hallucination Earnings Harness
      </div>
    </div>
"""

draft = {
    "header": {
        "page_title": "META — Pre-Earnings Forensic & Sentiment Tearsheet (Upcoming: Q3 2026 | Last Reported: Q2 2026)",
        "ticker": "META",
        "company_name": "Meta Platforms, Inc.",
        "earnings_date": "2026-10-21",
        "spot_price_num": float(spot_price),
        "market_cap_num": float(truth["valuation_and_market"]["market_cap_millions"]),
        "enterprise_value_num": float(truth["valuation_and_market"]["enterprise_value_millions"])
    },
    "kpi_cards": {
        "card_a_cash_flow": {
            "q2_2026_ocf_m": 31862.0,
            "q2_2026_capex_m": 30116.0,
            "q2_2026_reported_fcf_m": 1746.0,
            "q2_2026_true_fcf_m": -5912.0,
            "capex_to_rev_pct": 49.53,
            "sbc_to_rev_pct": 12.60
        },
        "card_b_debt_liquidity": {
            "cash_and_st_inv_m": 90260.0,
            "total_debt_and_leases_m": 112318.0,
            "net_debt_m": 22058.0,
            "stockholders_equity_m": 261221.0
        },
        "card_c_margins": {
            "gaap_gross_margin_pct": 81.37,
            "gaap_operating_margin_pct": 30.88,
            "roic_pct": 24.6,
            "roe_ttm_pct": 32.8
        },
        "card_d_multiples": {
            "trailing_pe": trailing_pe,
            "forward_pe": fwd_pe,
            "price_to_sales_ttm": ps_ttm,
            "ev_to_ebitda": ev_ebitda,
            "short_percent_of_float": short_float,
            "beta": 1.22
        }
    },
    "historical_table_5q_nums": historical_table_5q_nums,
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "ocf": 31862.0,
            "capex": 30116.0,
            "reported_fcf": 1746.0,
            "sbc": 7658.0,
            "finance_leases": 0.0,
            "true_fcf": -5912.0
        }
    },
    "trade_matrix": {
        "bull_target_low_num": 755.0,
        "bear_target_high_num": 610.0,
        "bull_case": {"prob": "35%", "target_range": "$755–$790", "trigger": "Q4 Rev Guide > $68B, CapEx Discipline"},
        "base_case": {"prob": "50%", "target_range": "$680–$730", "trigger": "Q3 Rev $62B–$63B, IV crush compression"},
        "bear_case": {"prob": "15%", "target_range": "$585–$610", "trigger": "FY27 CapEx > $85B or E-commerce ad slowdown"}
    },
    "rendered_container_html": html
}

DRAFT_PATH.write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Comprehensive META draft successfully written to {DRAFT_PATH}")
