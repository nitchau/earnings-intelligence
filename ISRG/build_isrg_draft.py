import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "ISRG_2026-10-20_truth.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "ISRG_2026-10-20_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 427.86
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1000.0, 1) # 151.2
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1000.0, 1) # 143.4
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 49.07
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 35.34
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 13.70
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 34.29
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 2.11

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 7.88
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"]) # 33.70
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 0.76
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"]) # 63.45

# 5-Quarter Data Points
quarters = ["Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026 (Actual)", "Q3 2026E (Est)"]
total_rev = [2440.0, 2505.1, 2866.2, 2770.8, 2892.3, 2910.0]
instruments_rev = [1474.1, 1518.8, 1658.3, 1686.4, 1734.9, 1780.0]
systems_rev = [574.7, 590.4, 785.9, 650.7, 685.0, 655.0]
services_rev = [391.2, 395.9, 422.0, 433.7, 472.4, 475.0]

gross_profit = [1617.9, 1662.4, 1904.3, 1830.5, 1960.4, 1980.0]
gross_margin = [66.31, 66.36, 66.44, 66.06, 67.78, 68.04]
opex = [874.5, 902.7, 1040.0, 975.2, 988.5, 1010.0]
ebit = [743.4, 759.7, 864.3, 855.3, 971.9, 970.0]
operating_margin = [30.47, 30.33, 30.15, 30.87, 33.60, 33.33]
net_income = [658.4, 704.4, 794.8, 821.5, 818.1, 825.0]
eps_non_gaap = [2.05, 2.22, 2.50, 2.58, 2.60, 2.64]

ocf = [715.4, 841.0, 892.5, 911.9, 1061.0, 1020.0]
capex = [155.3, 105.4, 162.5, 103.3, 112.6, 125.0]
rep_fcf = [560.1, 735.6, 730.0, 808.6, 948.4, 895.0]
sbc = [196.2, 203.5, 203.3, 209.5, 209.9, 215.0]
true_fcf = [363.9, 532.1, 526.7, 599.1, 738.5, 680.0]

cash_st = [5326.5, 4908.8, 5934.9, 4517.3, 5216.2, 5400.0]
total_debt = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
net_debt = [-5326.5, -4908.8, -5934.9, -4517.3, -5216.2, -5400.0]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": ebit[i]}
    for i in range(5)
]

# Build rendered_container_html
html = f"""
    <!-- 1. HEADER BANNER -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#93c5fd;">Last Reported Quarter: <strong>Q2 2026 (Ended June 30, 2026)</strong> • Upcoming Release: <strong>Q3 2026 (Ended Sept 30, 2026)</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">ISRG</span>
            <h1 class="company-name">Intuitive Surgical, Inc.</h1>
            <span class="badge badge-bull">QUALITY COMPOUNDER / PREMIUM MULTIPLE SETUP</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day before the official quarterly earnings release." data-tip="T-1 (Time Minus 1 Day): Indicates this analysis is prepared one day prior to the upcoming Q3 2026 earnings release.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select • Healthcare, Robotic Surgical Systems, Medical Technology &amp; Minimally Invasive Automation • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC to all public company filings." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the U.S. Securities and Exchange Commission (SEC) to track Intuitive Surgical's official regulatory filings.">CIK</span>: 0001035267</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price (Oct 2026)</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+18.4% <span class="tip tip-right tip-bottom" title="Year-To-Date: Percentage price change since January 1, 2026." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of the current calendar year (2026) to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares (Share Price × Diluted Shares)." data-tip="Market Capitalization: Total equity value of the company calculated by multiplying current share price (${spot_price:.2f}) by total diluted shares (~353.3M).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash. Shows the true takeover cost of the business." data-tip="Enterprise Value (EV): Market Cap ($151.2B) + Total Debt ($0.0M) - Cash &amp; Short-Term Investments ($5.22B). Reflects zero debt and negative net debt fortress.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.1f}B / ${ev_b:.1f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Upcoming Q3 2026 Release Date</span>
          <span class="strip-val">Tue, Oct 20, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market hours (~4:05 PM Eastern Time).">AMC</span> (4:05 PM ET)</span>
          <span class="kpi-sub">Live Earnings Webcast: 4:30 PM ET (1:30 PM PT)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in for the day after earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) weekly option straddle prices. It reflects the expected 1-week percentage move post-earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market's forecast of annualized stock price volatility derived from option prices." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Call Heavy)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E <span class="tip" title="Wall Street Consensus: The average forecast of equity research analysts covering Intuitive Surgical." data-tip="Consensus Revenue: The average top-line sales forecast published by Wall Street sell-side analysts for Q3 2026.">Consensus Revenue</span> / <span class="tip" title="Whisper Number: The unofficial expectation among hedge funds and institutional traders." data-tip="Whisper Number: Unofficial top-line expectations among buy-side institutional investors.">Whisper</span></span>
          <span class="strip-val">$2,910M / $2,945M</span>
          <span class="kpi-sub">Street Estimate: $2.91B | +16.2% <span class="tip" title="Year-over-Year: Comparison against the exact same quarter last year (Q3 2025)." data-tip="Year-over-Year (YoY): Compares performance against the same quarter one year prior (Q3 2026E vs Q3 2025).">YoY</span> vs Q3 2025</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E Consensus <span class="tip" title="Earnings Per Share: Net profit divided by total diluted shares outstanding." data-tip="Earnings Per Share (EPS): Net profit allocated to each share of common stock.">EPS</span> / Whisper</span>
          <span class="strip-val">$2.64 <span class="tip" title="Non-GAAP: Adjusted earnings that exclude stock-based compensation and amortization." data-tip="Non-GAAP EPS: Adjusted EPS excluding non-cash Stock-Based Compensation and intangible amortization.">Non-GAAP</span> / $2.72 Whisper</span>
          <span class="kpi-sub"><span class="tip" title="Generally Accepted Accounting Principles: Official U.S. SEC accounting standards." data-tip="GAAP: Official U.S. accounting rules including all equity compensation expenses.">GAAP</span> EPS Est: $2.32 | Range: $2.55 – $2.75</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">30-Day <span class="tip tip-right" title="How much Wall Street analysts have adjusted their Q3 forecasts over the past 30 days." data-tip="30-Day Sell-Side Revisions: Measures recent upward or downward adjustments in profit projections.">Sell-Side Revisions</span></span>
          <span class="strip-val" style="color: var(--bull-green);"><span class="tip tip-right" title="Operating Income (EBIT): Profit before interest and taxes." data-tip="EBIT (Operating Income): Sales minus Cost of Goods Sold and Operating Expenses (R&amp;D, SG&amp;A).">EBIT</span> +2.8% | EPS +2.1%</span>
          <span class="kpi-sub">da Vinci 5 (DV5) Placements &amp; Procedure Acceleration Lift Revisions</span>
        </div>
      </div>
    </header>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS — ALL LABELED WITH EXACT Q2 2026 REPORTED DATA) -->
    <section class="kpi-grid">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Intensity (Q2 2026)</div>
          <span class="badge badge-bull">CASH GENERATION SURGE</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual cash generated from day-to-day healthcare operations." data-tip="Operating Cash Flow (OCF): Cash inflow generated from procedures, instrument sales, and service contracts before CapEx.">Operating Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">First Half 2026 OCF: $1,972.9M (+21.2% YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$1,061.0M</span>
              <div class="delta-pair">
                <span class="badge badge-bull"><span class="tip" title="Quarter-over-Quarter: Sequential change from Q1 2026 to Q2 2026." data-tip="Quarter-over-Quarter (QoQ): Change from preceding quarter ($911.9M to $1,061.0M).">QoQ</span> +16.3%</span>
                <span class="badge badge-bull"><span class="tip" title="Year-over-Year: Change from Q2 2025 ($715.4M) to Q2 2026 ($1,061.0M)." data-tip="Year-over-Year (YoY): Percentage change from same quarter last year.">YoY</span> +48.3%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Cash spent on manufacturing automation and facilities." data-tip="Capital Expenditures (CapEx): Investment in manufacturing infrastructure and customer training centers.">Capital Expenditures</span> (Q2 2026)</span>
              <span class="kpi-sub">DV5 Manufacturing Lines &amp; Facility Expansions</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$112.6M</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +9.0%</span>
                <span class="badge badge-bull">YoY -27.5%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow ($1,061.0M) minus CapEx ($112.6M)." data-tip="Reported Free Cash Flow (FCF): Operating Cash Flow less CapEx ($1,061.0M - $112.6M = $948.4M).">Reported Free Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">True Economic <span class="tip" title="Free Cash Flow minus Stock-Based Compensation." data-tip="True/Effective FCF: FCF after deducting Stock-Based Compensation ($209.9M) to account for economic equity dilution.">FCF (ex-SBC)</span>: $738.5M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$948.4M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +17.3%</span>
                <span class="badge badge-bull">YoY +69.3%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="CapEx as a percentage of Q2 2026 revenue ($112.6M / $2,892.3M = 3.89%)." data-tip="CapEx-to-Revenue Ratio: Capital intensity ratio. 3.89% highlights Intuitive's capital-light, razor-and-blade business model.">CapEx-to-Rev</span> / <span class="tip" title="Stock-Based Compensation as a percentage of revenue ($209.9M / $2,892.3M = 7.26%)." data-tip="SBC-to-Revenue: Proportion of top-line revenue dedicated to equity compensation.">SBC-to-Rev</span></span>
              <span class="kpi-sub"><span class="tip" title="Stock-Based Compensation: Non-cash employee and executive equity awards ($209.9M in Q2 2026)." data-tip="Stock-Based Compensation (SBC): Non-cash equity compensation grants.">SBC</span> Q2 2026: $209.9M (R&amp;D Engineering &amp; Clinical Talent)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">3.89% / 7.26%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">CapEx +16 bps QoQ</span>
                <span class="badge badge-neutral">SBC -30 bps QoQ</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: BALANCE SHEET & ZERO-DEBT LIQUIDITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Balance Sheet &amp; Liquidity (Q2 2026)</div>
          <span class="badge badge-bull">FORTRESS ZERO-DEBT</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total cash, cash equivalents, and short-term investments as of June 30, 2026." data-tip="Cash &amp; ST Investments: Total liquid reserves held in U.S. Treasuries, money markets, and cash.">Cash &amp; ST Investments</span> (Q2 2026)</span>
              <span class="kpi-sub">$2,760.4M Cash + $2,455.8M Marketable Securities</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$5,216.2M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +15.5%</span>
                <span class="badge badge-neutral">YoY -2.1%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total debt on the balance sheet: Intuitive Surgical operates with ZERO short-term or long-term debt." data-tip="Total Debt: Sum of short-term borrowings and long-term notes. Intuitive maintains zero balance-sheet debt.">Total Debt &amp; Leases</span> (Q2 2026)</span>
              <span class="kpi-sub">$0 ST Debt + $0 LT Debt (100% Equity Funded)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$0.0M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Zero Debt</span>
                <span class="badge badge-bull">Pristine</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Net Debt = Total Debt ($0.0M) minus Cash ($5,216.2M). A negative value denotes a net cash position." data-tip="Net Debt / Net Cash: Total debt less cash and short-term investments. Negative $5.22B net cash balance.">Net Debt &amp; Net Debt/EBITDA</span></span>
              <span class="kpi-sub">Net Cash Fortress / <span class="tip" title="Trailing Twelve Months EBITDA (~$4.25B)." data-tip="EBITDA: Cash operating profit before depreciation.">TTM EBITDA</span>: -1.23x</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">-$5,216.2M (-1.23x)</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Net Cash +15.5% QoQ</span>
                <span class="badge badge-neutral">Net Cash -2.1% YoY</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Proportion of revenue derived from high-margin recurring instruments, accessories, and annual service agreements." data-tip="Recurring Revenue (%): Over 83% of ISRG total revenue is recurring (Instruments &amp; Accessories + Services), insulating against capital spending cycles.">Recurring Revenue Model</span> (Q2 2026)</span>
              <span class="kpi-sub">Razor-and-Blade: Instruments ($1.73B) + Service ($472M)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">83.2% of Total Rev</span>
              <div class="delta-pair">
                <span class="badge badge-bull">+18.8% YoY Recurring</span>
                <span class="badge badge-bull">9,500+ Installed Base</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: MARGINS & CAPITAL EFFICIENCY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Margins &amp; Efficiency (Q2 2026)</div>
          <span class="badge badge-bull">OPERATING LEVERAGE EXPANSION</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Gross Margin: Gross Profit divided by Revenue ($1,960.4M / $2,892.3M = 67.78%)." data-tip="GAAP Gross Margin: Revenue remaining after manufacturing, direct materials, and customer support costs.">GAAP Gross Margin</span> (Q2 2026)</span>
              <span class="kpi-sub">Instruments GM: ~72% | Systems GM: ~64%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">67.78%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +172 bps</span>
                <span class="badge badge-bull">YoY +147 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Operating Margin: EBIT divided by Revenue ($971.9M / $2,892.3M = 33.60%)." data-tip="GAAP Operating Margin (EBIT Margin): Core operating profit margin after R&amp;D ($370.6M) and SG&amp;A ($617.9M).">GAAP Operating Margin</span> (Q2 2026)</span>
              <span class="kpi-sub">Non-GAAP Operating Margin (ex-SBC): 40.86%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">33.60%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +273 bps</span>
                <span class="badge badge-bull">YoY +313 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Return on Invested Capital: After-tax operating profit divided by total invested capital." data-tip="Return on Invested Capital (ROIC): Measures profitability efficiency relative to capital employed. Exceeds WACC by +939 bps.">Return on Invested Capital (ROIC)</span></span>
              <span class="kpi-sub">vs. <span class="tip" title="Weighted Average Cost of Capital: Cost of equity/debt capital (~8.85%)." data-tip="Weighted Average Cost of Capital (WACC): Blended cost of capital for ISRG (8.85%).">WACC</span> of 8.85% (+939 bps economic spread)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">18.24%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +118 bps</span>
                <span class="badge badge-bull">YoY +240 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Return on Equity: TTM Net Income divided by Stockholders' Equity ($18.17B)." data-tip="Return on Equity (ROE): Net profit generated per dollar of book equity.">Return on Equity (ROE - TTM)</span></span>
              <span class="kpi-sub">Book Value Equity: $18.17B ($51.42/sh)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">18.21%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +45 bps</span>
                <span class="badge badge-bull">YoY +182 bps</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: VALUATION MULTIPLES -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Valuation Multiples (Current)</div>
          <span class="badge badge-warn">PREMIUM QUALITY VALUATION</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Trailing Price-to-Earnings: Current Share Price (${spot_price:.2f}) divided by trailing 12 months GAAP EPS ($8.72)." data-tip="Trailing P/E (GAAP TTM): Share price divided by last 12 months reported GAAP EPS.">Trailing P/E</span> (GAAP TTM)</span>
              <span class="kpi-sub">TTM GAAP Diluted EPS: ~$8.72</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{trailing_pe:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">Historical Med: ~52x</span>
                <span class="badge badge-warn">Premium vs Medtech (26x)</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forward Price-to-Earnings: Share Price divided by projected next 12 months consensus EPS." data-tip="Forward P/E: Stock price divided by consensus analyst forward earnings projections.">Forward P/E</span> (Next 12M Non-GAAP)</span>
              <span class="kpi-sub">FY26E Consensus Non-GAAP EPS: ~$12.10</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">{fwd_pe:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">PEG Ratio: 1.95x</span>
                <span class="badge badge-neutral">DV5 Ramp Discount</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Price-to-Sales: Market Cap ($151.2B) divided by Trailing 12-Month Revenue ($11.03B)." data-tip="Price-to-Sales (P/S TTM): Market value divided by trailing 12 months top-line sales.">Price-to-Sales (P/S TTM)</span></span>
              <span class="kpi-sub">TTM Revenue: $11.03B (Q3'25–Q2'26)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{ps_ttm:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ -1.2%</span>
                <span class="badge badge-neutral">YoY +4.1%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Enterprise Value ($143.4B) divided by Trailing 12-Month EBITDA (~$4.25B)." data-tip="EV / EBITDA: Enterprise Value divided by operating cash profit before depreciation.">EV / EBITDA</span> (TTM)</span>
              <span class="kpi-sub">TTM Normalized EBITDA: $4.25B</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{ev_ebitda:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">Short Float: {short_float:.2f}%</span>
                <span class="badge badge-bull">Low Short Exposure</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. ROW 2: FULL-WIDTH 5-QUARTER HISTORICAL TABLE (ISRG REPORTING SEGMENTS) -->
    <section class="card">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>5-Quarter Historical Performance (Q2 2025 – Q2 2026 Actual) &amp; Upcoming Q3 2026E Consensus</div>
          <div class="card-subtitle">Source: Intuitive Surgical SEC Form 10-Q / 10-K Filings &amp; Earnings Releases ($ in Millions, except per-share and %). Hover over any metric for plain-English definitions.</div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">Green = Operating Leverage Expansion</span>
          <span class="badge badge-warn">Amber = R&amp;D / Clinical Ramp Investment</span>
        </div>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Metric ($ Millions / % / Per Share)</th>
              <th>Q2 2025<br><span style="font-size:10px;font-weight:400;color:var(--text-muted);">Ended Jun 30, 2025</span></th>
              <th>Q3 2025<br><span style="font-size:10px;font-weight:400;color:var(--text-muted);">Ended Sep 30, 2025</span></th>
              <th>Q4 2025<br><span style="font-size:10px;font-weight:400;color:var(--text-muted);">Ended Dec 31, 2025</span></th>
              <th>Q1 2026<br><span style="font-size:10px;font-weight:400;color:var(--text-muted);">Ended Mar 31, 2026</span></th>
              <th class="col-q0">Q2 2026 (Actual)<br><span style="font-size:10px;font-weight:700;color:#93c5fd;">Last Reported Qtr</span></th>
              <th>Q2 2026 QoQ Δ<br><span style="font-size:10px;font-weight:400;color:var(--text-muted);">vs. Q1 2026</span></th>
              <th>Q2 2026 YoY Δ<br><span style="font-size:10px;font-weight:400;color:var(--text-muted);">vs. Q2 2025</span></th>
              <th class="col-est">Q3 2026E (Est)<br><span style="font-size:10px;font-weight:700;color:#fde68a;">Oct 20, 2026 Print</span></th>
            </tr>
          </thead>
          <tbody>
            <!-- REVENUE & SEGMENT BREAKDOWN -->
            <tr class="section-divider">
              <td colspan="9">Top-Line Product &amp; Service Segment Breakdown</td>
            </tr>
            <tr>
              <td><strong>Total Revenue ($M)</strong></td>
              <td>$2,440.0</td>
              <td>$2,505.1</td>
              <td>$2,866.2</td>
              <td>$2,770.8</td>
              <td class="col-q0">$2,892.3</td>
              <td><span class="badge badge-bull">+4.39%</span></td>
              <td><span class="badge badge-bull">+18.54%</span></td>
              <td class="col-est">$2,910.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Consumable instruments, EndoWrist tools, staples, and accessories used per surgical procedure." data-tip="Instruments &amp; Accessories Revenue: High-margin recurring consumables sold per procedure. Grows in direct tandem with total robotic surgical procedure volumes (~15% YoY)."> —Instruments &amp; Accessories Revenue ($M)</span></td>
              <td>$1,474.1</td>
              <td>$1,518.8</td>
              <td>$1,658.3</td>
              <td>$1,686.4</td>
              <td class="col-q0">$1,734.9</td>
              <td><span class="badge badge-bull">+2.88%</span></td>
              <td><span class="badge badge-bull">+17.69%</span></td>
              <td class="col-est">$1,780.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital sales and operating leases of multi-port da Vinci 5, da Vinci Xi, single-port SP, and Ion endoluminal robotic systems." data-tip="Systems Revenue: Capital system sales and operating lease placements of da Vinci 5, Xi, SP, and Ion platforms."> —Systems Revenue (da Vinci &amp; Ion Placements) ($M)</span></td>
              <td>$574.7</td>
              <td>$590.4</td>
              <td>$785.9</td>
              <td>$650.7</td>
              <td class="col-q0">$685.0</td>
              <td><span class="badge badge-bull">+5.27%</span></td>
              <td><span class="badge badge-bull">+19.19%</span></td>
              <td class="col-est">$655.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Service contracts, routine preventive maintenance, and hospital system uptime guarantees." data-tip="Services Revenue: High-margin contractual maintenance and technical service agreements for installed systems."> —Services Revenue ($M)</span></td>
              <td>$391.2</td>
              <td>$395.9</td>
              <td>$422.0</td>
              <td>$433.7</td>
              <td class="col-q0">$472.4</td>
              <td><span class="badge badge-bull">+8.92%</span></td>
              <td><span class="badge badge-bull">+20.76%</span></td>
              <td class="col-est">$475.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Revenue remaining after direct manufacturing, component assembly, and service support costs." data-tip="GAAP Gross Profit ($M): Total Revenue minus Cost of Revenue. Reached $1,960.4M in Q2 2026.">GAAP Gross Profit ($M)</span></td>
              <td>$1,617.9</td>
              <td>$1,662.4</td>
              <td>$1,904.3</td>
              <td>$1,830.5</td>
              <td class="col-q0">$1,960.4</td>
              <td><span class="badge badge-bull">+7.10%</span></td>
              <td><span class="badge badge-bull">+21.17%</span></td>
              <td class="col-est">$1,980.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Gross Profit as a percentage of Total Revenue." data-tip="GAAP Gross Margin (%): Percentage of sales retained after direct production costs. Expanded to 67.78% in Q2 2026.">GAAP Gross Margin (%)</span></td>
              <td>66.31%</td>
              <td>66.36%</td>
              <td>66.44%</td>
              <td>66.06%</td>
              <td class="col-q0">67.78%</td>
              <td><span class="badge badge-bull">+172 bps</span></td>
              <td><span class="badge badge-bull">+147 bps</span></td>
              <td class="col-est">68.04%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating expenses including Research &amp; Development ($370.6M) and SG&amp;A ($617.9M)." data-tip="Total Operating Expenses ($M): Overhead costs to support commercial rollout, clinical trials, and engineering.">Total Operating Expenses ($M)</span></td>
              <td>$874.5</td>
              <td>$902.7</td>
              <td>$1,040.0</td>
              <td>$975.2</td>
              <td class="col-q0">$988.5</td>
              <td><span class="badge badge-neutral">+1.36%</span></td>
              <td><span class="badge badge-neutral">+13.04%</span></td>
              <td class="col-est">$1,010.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit minus Operating Expenses ($1,960.4M - $988.5M = $971.9M)." data-tip="GAAP Operating Income / EBIT ($M): Core healthcare operating profit before interest and taxes.">GAAP Operating Income / EBIT ($M)</span></td>
              <td>$743.4</td>
              <td>$759.7</td>
              <td>$864.3</td>
              <td>$855.3</td>
              <td class="col-q0">$971.9</td>
              <td><span class="badge badge-bull">+13.63%</span></td>
              <td><span class="badge badge-bull">+30.74%</span></td>
              <td class="col-est">$970.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Income as a percentage of Total Revenue." data-tip="GAAP Operating Margin (%): Expanded to 33.60% in Q2 2026 demonstrating robust operating leverage.">GAAP Operating Margin (%)</span></td>
              <td>30.47%</td>
              <td>30.33%</td>
              <td>30.15%</td>
              <td>30.87%</td>
              <td class="col-q0">33.60%</td>
              <td><span class="badge badge-bull">+273 bps</span></td>
              <td><span class="badge badge-bull">+313 bps</span></td>
              <td class="col-est">33.33%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Reported net profit attributable to Intuitive Surgical common stockholders." data-tip="GAAP Net Income ($M): Bottom-line net profit after tax and net interest income from cash reserves.">GAAP Net Income ($M)</span></td>
              <td>$658.4</td>
              <td>$704.4</td>
              <td>$794.8</td>
              <td>$821.5</td>
              <td class="col-q0">$818.1</td>
              <td><span class="badge badge-neutral">-0.41%</span></td>
              <td><span class="badge badge-bull">+24.26%</span></td>
              <td class="col-est">$825.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Adjusted Diluted Earnings Per Share excluding Stock-Based Compensation and intangible amortization." data-tip="Diluted EPS — Non-GAAP ($/sh): Headline benchmark metric tracked by Wall Street analysts.">Diluted EPS — Non-GAAP ($/sh)</span></td>
              <td>$2.05</td>
              <td>$2.22</td>
              <td>$2.50</td>
              <td>$2.58</td>
              <td class="col-q0">$2.60</td>
              <td><span class="badge badge-bull">+0.78%</span></td>
              <td><span class="badge badge-bull">+26.83%</span></td>
              <td class="col-est">$2.64</td>
            </tr>

            <!-- CASH FLOW & FCF METRICS -->
            <tr class="section-divider">
              <td colspan="9">Cash Flow, CapEx &amp; Free Cash Flow Bridge</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cash generated from surgical customer collections and service agreements." data-tip="Operating Cash Flow (OCF) ($M): Pure operational cash flow generated prior to physical infrastructure investments.">Operating Cash Flow (OCF) ($M)</span></td>
              <td>$715.4</td>
              <td>$841.0</td>
              <td>$892.5</td>
              <td>$911.9</td>
              <td class="col-q0">$1,061.0</td>
              <td><span class="badge badge-bull">+16.35%</span></td>
              <td><span class="badge badge-bull">+48.31%</span></td>
              <td class="col-est">$1,020.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital Expenditures on facilities, factory tooling, and IT infrastructure." data-tip="Capital Expenditures (CapEx) ($M): Cash spent on property, plant, and equipment additions.">Capital Expenditures (CapEx) ($M)</span></td>
              <td>($155.3)</td>
              <td>($105.4)</td>
              <td>($162.5)</td>
              <td>($103.3)</td>
              <td class="col-q0">($112.6)</td>
              <td><span class="badge badge-neutral">+9.00%</span></td>
              <td><span class="badge badge-bull">-27.50%</span></td>
              <td class="col-est">($125.0)</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Cash Flow minus Capital Expenditures ($1,061.0M - $112.6M = $948.4M)." data-tip="Reported Free Cash Flow (FCF) ($M): Unlevered cash generated after all capital expenditures.">Reported Free Cash Flow (FCF) ($M)</span></td>
              <td>$560.1</td>
              <td>$735.6</td>
              <td>$730.0</td>
              <td>$808.6</td>
              <td class="col-q0" style="color:var(--bull-green);">$948.4</td>
              <td><span class="badge badge-bull">+17.29%</span></td>
              <td><span class="badge badge-bull">+69.33%</span></td>
              <td class="col-est">$895.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Non-cash equity compensation grants awarded to clinical and engineering employees." data-tip="Stock-Based Compensation (SBC) ($M): Non-cash equity compensation.">Stock-Based Compensation (SBC) ($M)</span></td>
              <td>$196.2</td>
              <td>$203.5</td>
              <td>$203.3</td>
              <td>$209.5</td>
              <td class="col-q0">$209.9</td>
              <td><span class="badge badge-neutral">+0.19%</span></td>
              <td><span class="badge badge-neutral">+6.98%</span></td>
              <td class="col-est">$215.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="True Economic Free Cash Flow: Reported FCF minus Stock-Based Compensation ($948.4M - $209.9M = $738.5M)." data-tip="True / Effective FCF ($M): FCF after deducting SBC to treat equity compensation as an economic cash expense.">True / Effective FCF (FCF less SBC) ($M)</span></td>
              <td>$363.9</td>
              <td>$532.1</td>
              <td>$526.7</td>
              <td>$599.1</td>
              <td class="col-q0" style="color:var(--bull-green);">$738.5</td>
              <td><span class="badge badge-bull">+23.27%</span></td>
              <td><span class="badge badge-bull">+102.94%</span></td>
              <td class="col-est">$680.0</td>
            </tr>

            <!-- BALANCE SHEET & DEBT PROFILE -->
            <tr class="section-divider">
              <td colspan="9">Balance Sheet &amp; Zero-Debt Fortress Profile</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total cash, cash equivalents, and short-term investments at quarter end." data-tip="Cash, Equivalents &amp; ST Investments ($M): Total liquid reserves. Reached $5,216.2M as of June 30, 2026.">Cash, Equivalents &amp; ST Investments ($M)</span></td>
              <td>$5,326.5</td>
              <td>$4,908.8</td>
              <td>$5,934.9</td>
              <td>$4,517.3</td>
              <td class="col-q0">$5,216.2</td>
              <td><span class="badge badge-bull">+15.47%</span></td>
              <td><span class="badge badge-neutral">-2.07%</span></td>
              <td class="col-est">$5,400.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Intuitive Surgical holds zero short-term or long-term debt obligations." data-tip="Total Debt ($M): Total debt obligations on the balance sheet. Intuitive has $0 debt.">Total Debt ($M)</span></td>
              <td>$0.0</td>
              <td>$0.0</td>
              <td>$0.0</td>
              <td>$0.0</td>
              <td class="col-q0">$0.0</td>
              <td><span class="badge badge-bull">0.0%</span></td>
              <td><span class="badge badge-bull">0.0%</span></td>
              <td class="col-est">$0.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Net Debt = Total Debt ($0.0M) minus Cash ($5,216.2M)." data-tip="Net Debt / (Net Cash) ($M): Reflects the company's net liquid capital surplus.">Net Debt / (Net Cash) ($M)</span></td>
              <td>($5,326.5)</td>
              <td>($4,908.8)</td>
              <td>($5,934.9)</td>
              <td>($4,517.3)</td>
              <td class="col-q0" style="color:var(--bull-green);">($5,216.2)</td>
              <td><span class="badge badge-bull">+15.47%</span></td>
              <td><span class="badge badge-neutral">-2.07%</span></td>
              <td class="col-est">($5,400.0)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 4. ROW 3: FORENSIC CALLOUT CARD -->
    <section class="card">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Outlier &amp; Accounting Quality Audit (Q2 2026 Forensic Review)</div>
          <div class="card-subtitle">Forensic deconstruction of GAAP Operating vs. Net Income, da Vinci 5 adoption cadence, and razor-and-blade recurring cash generation</div>
        </div>
        <span class="badge badge-bull">PRISTINE QUALITY OF EARNINGS</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>1. GAAP Operating Income ($971.9M) vs. Net Income ($818.1M): Pristine Organic Conversion</span>
              <span class="badge badge-bull">+$82.7M INTEREST INCOME</span>
            </div>
            <p>
              Unlike peers relying on mark-to-market revaluations or tax credit windfalls, Intuitive's divergence between Operating Income ($971.9M) and GAAP Net Income ($818.1M) is driven strictly by routine corporate operations: a standard <strong>22.4% tax provision ($236.5M)</strong> offset by <strong>$82.7M in net Treasury interest income</strong> generated on its $5.22B cash and short-term investment hoard. There are zero non-operating write-downs, zero restructuring charges, and zero asset impairments.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--accent-blue);">
            <div class="forensic-item-title">
              <span>2. da Vinci 5 (DV5) Capital Placement Cycle &amp; Gross Margin Expansion (+172 bps QoQ)</span>
              <span class="badge badge-blue">67.78% GAAP GM</span>
            </div>
            <p>
              Systems revenue rose +19.2% YoY to $685.0M in Q2 2026, driven by higher average selling prices (ASPs) for the next-generation <strong>da Vinci 5 (DV5) multi-port robotic system</strong> and an expanding leased installed base. Consolidated GAAP Gross Margin expanded to <strong>67.78%</strong> (+172 bps QoQ, +147 bps YoY) as manufacturing tooling efficiencies and higher DV5 software feature adoption overcame early launch overhead costs.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>3. Razor-and-Blade Recurring Revenue Dominance (&gt;83% Recurring Revenue Base)</span>
              <span class="badge badge-bull">83.2% RECURRING REVENUE</span>
            </div>
            <p>
              Intuitive's structural moat lies in its recurring revenue engine. In Q2 2026, <strong>$2,207.3M (83.2% of total revenue)</strong> was generated from Instruments &amp; Accessories ($1,734.9M, +17.7% YoY) and Services ($472.4M, +20.8% YoY). With global installed da Vinci systems exceeding <strong>9,500 active units</strong> and worldwide surgical procedure volume growing at <strong>~15% YoY</strong>, consumable pull-through guarantees high-visibility cash conversion regardless of hospital capital budget cycles.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Capital-Light Super-Compounder Profile ($948.4M Reported FCF / $738.5M True FCF)</span>
              <span class="badge badge-bull">CAPEX / REV: 3.89%</span>
            </div>
            <p>
              Operating Cash Flow expanded +48.3% YoY to $1,061.0M while CapEx consumed only <strong>3.89% of revenue ($112.6M)</strong>, delivering a staggering <strong>$948.4M in Reported Free Cash Flow (32.8% FCF margin)</strong>. Even after deducting $209.9M in non-cash Stock-Based Compensation, True Economic FCF reached <strong>$738.5M (+102.9% YoY)</strong>, proving that Intuitive compounds capital at elite efficiency with zero balance-sheet leverage.
            </p>
          </div>
        </div>

        <!-- RIGHT SIDE: REPORTED FCF VS TRUE FCF RECONCILIATION -->
        <div class="fcf-bridge-box">
          <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border-color);padding-bottom:10px;">
            <span style="font-weight:700;font-size:13.5px;text-transform:uppercase;letter-spacing:0.04em;">Forensic Cash Flow Bridge: Reported vs. Effective FCF</span>
            <span class="badge badge-bull">Q2 2026 ACTUAL</span>
          </div>

          <table>
            <thead>
              <tr>
                <th>Cash Flow Component</th>
                <th>Q2 2025</th>
                <th>Q1 2026</th>
                <th>Q2 2026</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>GAAP Operating Cash Flow (OCF)</td>
                <td>$715.4M</td>
                <td>$911.9M</td>
                <td class="col-q0" style="color:var(--bull-green);">$1,061.0M</td>
              </tr>
              <tr>
                <td>Less: Capital Expenditures (CapEx)</td>
                <td>($155.3M)</td>
                <td>($103.3M)</td>
                <td class="col-q0">($112.6M)</td>
              </tr>
              <tr>
                <td><strong>Reported Free Cash Flow (Non-GAAP)</strong></td>
                <td><strong>$560.1M</strong></td>
                <td><strong>$808.6M</strong></td>
                <td class="col-q0" style="color:var(--bull-green);"><strong>$948.4M</strong></td>
              </tr>
              <tr>
                <td>Less: Stock-Based Compensation (SBC)</td>
                <td>($196.2M)</td>
                <td>($209.5M)</td>
                <td class="col-q0">($209.9M)</td>
              </tr>
              <tr>
                <td>Less: Finance Lease Principal Payments</td>
                <td>($0.0M)</td>
                <td>($0.0M)</td>
                <td class="col-q0">($0.0M)</td>
              </tr>
              <tr>
                <td><strong>True / Effective Economic FCF</strong></td>
                <td style="color:var(--bull-green);"><strong>$363.9M</strong></td>
                <td style="color:var(--bull-green);"><strong>$599.1M</strong></td>
                <td class="col-q0" style="color:var(--bull-green);"><strong>$738.5M</strong></td>
              </tr>
              <tr>
                <td>Effective FCF Margin (% of Revenue)</td>
                <td>+14.91%</td>
                <td>+21.62%</td>
                <td class="col-q0" style="color:var(--bull-green);">+25.53%</td>
              </tr>
            </tbody>
          </table>

          <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);border-radius:6px;padding:12px;font-size:12.3px;color:var(--text-secondary);">
            <strong style="color:#86efac;display:block;margin-bottom:4px;">PM Forensic Takeaway — Zero Debt Fortress Compounding:</strong>
            Intuitive Surgical is one of the highest-quality compounders in medical technology. With <strong>$5.22B in cash/investments</strong>, zero long-term debt, 33.6% operating margins, and 83.2% recurring revenues, downside risk is heavily insulated against macro contraction. The primary earnings sensitivity on Oct 20 is not balance-sheet stress, but whether da Vinci 5 adoption and international procedure volumes (China / Europe) justify a 35.3x Forward P/E multiple.
          </div>
        </div>
      </div>
    </section>

    <!-- 5. ROW 4: 2-COLUMN SPLIT (EXECUTION AUDIT: RIGHT VS WRONG) -->
    <section class="split-2col">
      <!-- LEFT CARD: WHAT MANAGEMENT DID RIGHT -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent" style="background-color:var(--bull-green);"></span>What Management Did Right (Operational Wins)</div>
          <span class="badge badge-bull">EXECUTION POSITIVES</span>
        </div>
        <div class="audit-list">
          <div class="audit-point audit-point-bull">
            <div class="audit-point-header">
              <span class="audit-point-title">1. Accelerating da Vinci 5 (DV5) Clinical Adoption &amp; Force Feedback Validation</span>
              <span class="badge badge-bull">SURGICAL ADVANCEMENT</span>
            </div>
            <p>
              Successfully expanded da Vinci 5 commercial placements following initial FDA 510(k) clearance. Clinical feedback confirms the platform's proprietary Force Feedback technology reduces tissue trauma, while 10,000x processing power supports real-time imaging integration and streamlined operating room workflow.
            </p>
          </div>
          <div class="audit-point audit-point-bull">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Resilient Global Surgical Procedure Volume Growth (~15% YoY)</span>
              <span class="badge badge-bull">VOLUME EXPANSION</span>
            </div>
            <p>
              Drove worldwide surgical procedure growth of ~15% YoY led by general surgery (cholecystectomy, bariatric, and hernia repair) and thoracic procedures, defying macro hospital staffing constraints and reinforcing high-margin consumable instrument sales.
            </p>
          </div>
          <div class="audit-point audit-point-bull">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Rapid Ion Endoluminal System Ramp (+36% Procedure Growth)</span>
              <span class="badge badge-bull">EXPANDING TAM</span>
            </div>
            <p>
              The Ion endoluminal robotic bronchoscopy system for minimally invasive lung biopsy achieved +36% procedure growth in Q2 2026, deepening Intuitive's penetration across diagnostic pulmonology and expanding its non-soft-tissue surgical footprint.
            </p>
          </div>
          <div class="audit-point audit-point-bull">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Superior Capital Allocation &amp; Operating Leverage (+313 bps Op Margin YoY)</span>
              <span class="badge badge-bull">DISCIPLINE</span>
            </div>
            <p>
              Expanded GAAP Operating Margin to 33.60% (+313 bps YoY) while self-funding all next-generation R&amp;D ($370.6M) and capital additions ($112.6M) from cash flow, accumulating over $5.2B in liquid reserves.
            </p>
          </div>
        </div>
      </div>

      <!-- RIGHT CARD: WHAT MANAGEMENT FACES / EXECUTION DRAGS -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent" style="background-color:var(--bear-red);"></span>Key Headwinds &amp; Valuation Sensitivities</div>
          <span class="badge badge-warn">POTENTIAL HEADWINDS</span>
        </div>
        <div class="audit-list">
          <div class="audit-point audit-point-bear">
            <div class="audit-point-header">
              <span class="audit-point-title">1. China Anti-Corruption Campaign &amp; Domestic Robotic Competition</span>
              <span class="badge badge-bear">CHINA TENDER FRICTION</span>
            </div>
            <p>
              Ongoing healthcare sector anti-corruption scrutiny in China continues to delay hospital system tender approvals and capital equipment procurement. Concurrently, local Chinese robotic competitors (MicroPort, Edge Medical) are pressuring pricing in provincial tenders.
            </p>
          </div>
          <div class="audit-point audit-point-bear">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Extended Hospital Capital Budget Review Cycles for System Placements</span>
              <span class="badge badge-bear">CAPITAL TIMING</span>
            </div>
            <p>
              Health systems globally remain sensitive to upfront capital outlays, prompting greater demand for operating leases and usage-based placements rather than direct capital purchases, moderately muting upfront Systems revenue realization.
            </p>
          </div>
          <div class="audit-point audit-point-bear">
            <div class="audit-point-header">
              <span class="audit-point-title">3. European Regulatory Clearance Timing for da Vinci 5 (CE Mark)</span>
              <span class="badge badge-warn">REGULATORY HORIZON</span>
            </div>
            <p>
              While DV5 placements are expanding rapidly in the United States, commercial rollout across Europe awaits broad CE Mark clearance, limiting near-term multi-port replacement cycles in non-U.S. developed markets.
            </p>
          </div>
          <div class="audit-point audit-point-bear">
            <div class="audit-point-header">
              <span class="audit-point-title">4. High Valuation Multiple Vulnerability (35.3x Forward P/E / 49.1x TTM)</span>
              <span class="badge badge-warn">MULTIPLE RISK</span>
            </div>
            <p>
              Trading at 35.3x forward earnings and 13.7x sales leaves zero room for execution missteps. Any procedural deceleration or quarterly shipment pause could trigger multi-point multiple compression.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. ROW 5: 2-COLUMN SPLIT (COMPETITIVE PEER MATRIX & PRODUCT CATALYSTS) -->
    <section class="split-2col">
      <!-- LEFT CARD: COMPETITOR BENCHMARKING TABLE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>MedTech Peer Benchmarking &amp; Margins</div>
          <span class="badge badge-blue">PEER COMP MATRIX (Q2 2026)</span>
        </div>

        <div class="table-wrapper" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th style="min-width:140px;">Ticker / Peer</th>
                <th><span class="tip" title="Year-over-Year Revenue Growth in Q2 2026." data-tip="YoY Revenue Growth: Top-line growth compared to same quarter last year.">YoY Rev Growth</span></th>
                <th><span class="tip" title="GAAP Gross Margin percentage." data-tip="Gross Margin: Gross profit divided by revenue.">Gross Margin</span></th>
                <th><span class="tip" title="Operating Margin percentage." data-tip="Operating Margin: EBIT divided by revenue.">Op Margin</span></th>
                <th><span class="tip" title="Free Cash Flow divided by revenue." data-tip="FCF Margin: Percentage of sales converted to unlevered free cash flow.">FCF Margin</span></th>
                <th><span class="tip tip-right" title="Forward P/E ratio based on consensus earnings." data-tip="Forward P/E: Stock price divided by next 12 months estimated EPS.">Fwd P/E</span></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color:var(--accent-blue);">ISRG (Intuitive)</strong></td>
                <td><span class="badge badge-bull">+18.5%</span></td>
                <td><strong style="color:var(--bull-green);">67.78%</strong></td>
                <td><strong style="color:var(--bull-green);">33.60%</strong></td>
                <td><strong style="color:var(--bull-green);">+32.79%</strong></td>
                <td style="color:var(--warn-amber);">{fwd_pe:.1f}x</td>
              </tr>
              <tr>
                <td><strong>SYK (Stryker)</strong></td>
                <td><span class="badge badge-bull">+10.2%</span></td>
                <td>64.10%</td>
                <td>21.40%</td>
                <td>+16.80%</td>
                <td>25.8x</td>
              </tr>
              <tr>
                <td><strong>MDT (Medtronic)</strong></td>
                <td><span class="badge badge-neutral">+4.6%</span></td>
                <td>65.20%</td>
                <td>19.80%</td>
                <td>+15.20%</td>
                <td>16.2x</td>
              </tr>
              <tr>
                <td><strong>BSX (Boston Scientific)</strong></td>
                <td><span class="badge badge-bull">+13.8%</span></td>
                <td>69.30%</td>
                <td>22.10%</td>
                <td>+18.40%</td>
                <td>28.4x</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">Robotic Surgery Monopoly &amp; Superior Margins</span>
              <span class="badge badge-bull">PRICING POWER</span>
            </div>
            <p>
              • <strong>Intuitive vs. Legacy MedTech:</strong> ISRG generates nearly double the operating margin (33.6% vs. 19%–22%) and superior cash conversion (+32.8% FCF margin) relative to diversified medtech giants Stryker and Medtronic.<br>
              • <strong>Barriers to Entry:</strong> Over 15 million lifetime surgeries performed across 9,500+ installed systems, supported by deep clinical surgeon training curricula and 4,500+ worldwide patents, creating virtually insurmountable customer switching costs.
            </p>
          </div>
        </div>
      </div>

      <!-- RIGHT CARD: PRODUCT PIPELINE & MARKET SHARE CATALYSTS -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Product Pipeline &amp; Growth Catalysts (Next 2–4 Qtrs)</div>
          <span class="badge badge-bull">PIPELINE CATALYSTS</span>
        </div>

        <div class="catalyst-grid">
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">1. da Vinci 5 Full-Scale Production &amp; International Expansion</span>
              <span class="badge badge-bull">MAJOR CYCLE</span>
            </div>
            <p>
              Transitioning from initial controlled launch to full-scale volume manufacturing at Sunnyvale. Expected regulatory clearances in Europe (CE Mark) and Japan (PMDA) over the next 6–12 months will unlock massive replacement demand across >3,000 legacy Xi systems.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Single-Port (SP) Indications Expansion</span>
              <span class="badge badge-blue">CLINICAL TRIALS</span>
            </div>
            <p>
              Expanding clinical indications for the da Vinci SP platform across urology, transoral robotic surgery (TORS), and colorectal applications, allowing surgeons to operate through a single 2.5 cm incision.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Digital Ecosystem &amp; AI Surgical Analytics (Intuitive Hub / Iris)</span>
              <span class="badge badge-bull">SOFTWARE MOAT</span>
            </div>
            <p>
              Deploying machine learning models to capture telemetric and video surgical data through Intuitive Hub, providing surgeons with AI-assisted procedure insights, operative milestone tracking, and tele-mentoring.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. General Surgery Procedural Penetration in International Markets</span>
              <span class="badge badge-bull">LONG RUNWAY</span>
            </div>
            <p>
              While U.S. urology is ~90% robotically penetrated, international adoption in hernia, colorectal, and bariatric surgery remains below 20%, representing a multi-decade procedural runway.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ROW 6: MULTI-SOURCE SENTIMENT ANALYSIS CARD -->
    <section class="card">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Multi-Source Pre-Earnings Sentiment Analysis (The 4 Institutional &amp; Retail Pillars)</div>
          <div class="card-subtitle">Triangulating Options Flow, Sell-Side Revisions, Institutional Holding Breadth, and Clinical Sentiment heading into the Oct 20, 2026 AMC Release.</div>
        </div>
        <span class="badge badge-bull">COMPOSITE SCORE: 68 / 100 (BULLISH / ACCUMULATION)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Institutional Consensus: High Conviction on DV5 Replacement Supercycle
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            Options positioning exhibits a strong call bias with a <strong>Put/Call Open Interest Ratio of 0.76</strong> and sell-side revision breadth skewing positively (+2.8% on EBIT). Institutional quality-of-earnings scores remain in the 95th percentile, reflecting zero debt and 83% recurring revenue stability.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">Institutions: Overweight / Quality Safe Haven</span>
          <span class="badge badge-bull">Options: Call Accumulation (PCR 0.76)</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <!-- SOURCE 1: OPTIONS MARKET -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #1: Options Market &amp; Dealer Positioning <span class="badge badge-blue">REAL CAPITAL</span></span>
            <span class="badge badge-bull">SCORE: 72 / 100 (CALL BIAS)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-bar-bg">
              <div class="sentiment-bar-fill" style="width: 72%; background-color: var(--bull-green);"></div>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);">
            • <strong>Put/Call OI Ratio:</strong> <span class="mono">0.76x</span> (Significant call open interest clustering at $440 and $450 strikes)<br>
            • <strong>ATM Implied Move:</strong> <span class="mono">±7.88% (±$33.70 / sh)</span> pricing in a ±$34 post-earnings swing<br>
            • <strong>30-Day Implied Volatility:</strong> <span class="mono">{iv_pct:.1f}%</span> (65th percentile elevation ahead of earnings print)
          </p>
        </div>

        <!-- SOURCE 2: SELL-SIDE REVISIONS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #2: Sell-Side Revision Breadth &amp; Consensus <span class="badge badge-blue">ESTIMATE TREND</span></span>
            <span class="badge badge-bull">SCORE: 68 / 100 (UPWARD REVISIONS)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-bar-bg">
              <div class="sentiment-bar-fill" style="width: 68%; background-color: var(--bull-green);"></div>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);">
            • <strong>30-Day Revision Skew:</strong> 18 Upward vs. 4 Downward EPS revisions (+2.1% net revision)<br>
            • <strong>Consensus EPS:</strong> <span class="mono">$2.64 Non-GAAP</span> (Whisper: $2.72)<br>
            • <strong>Wall Street Rating Breakdown (32 Analysts):</strong> 72% Buy | 25% Hold | 3% Sell • Mean Target: <span class="mono">$460.00</span>
          </p>
        </div>

        <!-- SOURCE 3: CLINICAL & RETAIL SENTIMENT -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #3: Hospital Procurement &amp; Clinical Surveys <span class="badge badge-blue">HEALTHCARE CHANNEL</span></span>
            <span class="badge badge-bull">SCORE: 65 / 100 (HIGH DEMAND)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-bar-bg">
              <div class="sentiment-bar-fill" style="width: 65%; background-color: var(--bull-green);"></div>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);">
            • <strong>Surgeon Survey Channel Checks:</strong> Over 80% of surgical departments expressing intent to upgrade to DV5 within 24 months<br>
            • <strong>Retail / FinTwit NLP:</strong> Positive sentiment on robotic surgery resilience and aging demographic macro tailwinds
          </p>
        </div>

        <!-- SOURCE 4: CORPORATE INSIDERS & 13F FLOW -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #4: Institutional Ownership &amp; 13F Whales <span class="badge badge-blue">SMART MONEY</span></span>
            <span class="badge badge-bull">SCORE: 66 / 100 (STEADY ACCUMULATION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-bar-bg">
              <div class="sentiment-bar-fill" style="width: 66%; background-color: var(--bull-green);"></div>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);">
            • <strong>Institutional Holding:</strong> 85.4% of float held by high-quality long-only institutional funds<br>
            • <strong>Insider Activity:</strong> Modest programmatic 10b5-1 sales, zero distressed open-market liquidations
          </p>
        </div>
      </div>
    </section>

    <!-- 8. ROW 7: HEDGE FUND PM TRADE EXECUTION MATRIX -->
    <section class="card">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Hedge Fund PM Post-Earnings Trade Execution Matrix (Q3 2026 Print Playbook)</div>
          <div class="card-subtitle">Exact quantitative post-print triggers for BUY (Bull Case), HOLD/FADE (Base Case), and SELL/SHORT (Bear Case) following the Oct 20, 2026 AMC release</div>
        </div>
        <span class="badge badge-blue">PM PLAYBOOK • Q3 2026 RELEASE</span>
      </div>

      <div class="playbook-setup-bar">
        <div>
          <span class="strip-label">Institutional Positioning</span>
          <div class="strip-val" style="margin-top:3px;">High Quality Long-Only Overweight</div>
          <span class="kpi-sub">Defensive safe haven with secular growth and zero leverage.</span>
        </div>
        <div>
          <span class="strip-label">Valuation Multiple Context</span>
          <div class="strip-val" style="margin-top:3px;color:var(--warn-amber);">35.3x Forward P/E / 49.1x TTM P/E</div>
          <span class="kpi-sub">Commands premium multiple supported by 33.6% EBIT margins and 83% recurring revenue.</span>
        </div>
        <div>
          <span class="strip-label">Primary Earnings Debate</span>
          <div class="strip-val" style="margin-top:3px;">DV5 Shipment Rate vs. China Scrutiny</div>
          <span class="kpi-sub">Can domestic DV5 acceleration overcome ongoing China tender delays?</span>
        </div>
        <div>
          <span class="strip-label">Historical Post-Earnings Skew</span>
          <div class="strip-val" style="margin-top:3px;color:var(--bull-green);">Gained +4.2% Avg on Last 3 Prints</div>
          <span class="kpi-sub">Strong history of beat-and-raise prints driven by procedure volume beats.</span>
        </div>
      </div>

      <div class="scenario-grid">
        <!-- BULL CASE -->
        <div class="scenario-card scenario-bull">
          <div class="scenario-title">
            <span style="color:var(--bull-green);">BUY / ADD EXPOSURE (BULL CASE)</span>
            <span class="badge badge-bull">PROB: 40% | TARGET: $465–$490 (+9% to +15%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Top-Line &amp; Procedure Beat:</strong> Q3 2026 Revenue &gt; <strong>$2.95B</strong> with global procedure growth accelerating ≥ <strong>16.5% YoY</strong>.</li>
            <li><strong>da Vinci 5 Placement Surge:</strong> Total system placements exceeding <strong>380 units</strong> with DV5 placements topping <strong>120 units</strong>.</li>
            <li><strong>Earnings Outperformance:</strong> Non-GAAP Diluted EPS ≥ <strong>$2.75</strong> (vs. $2.64 consensus) and GAAP Gross Margin expanding ≥ <strong>68.2%</strong>.</li>
            <li><strong>FY 2026 Procedure Guidance Raised:</strong> Full-year procedure growth guidance lifted to <strong>16.0%–17.0%</strong>.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Buy post-print momentum above $445 on heavy volume or initiate a <strong>Nov 20, 2026 $430 / $470 Bull Call Spread</strong> to capture upside momentum while mitigating IV crush.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">HOLD / RANGE-BOUND (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 45% | RANGE: $415–$445 (±3.5%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>In-Line Delivery:</strong> Q3 2026 Revenue prints between <strong>$2.89B – $2.93B</strong> (+15% to +17% YoY).</li>
            <li><strong>Steady Procedure Growth:</strong> Worldwide procedure growth lands at <strong>14.5% – 15.5%</strong> in line with management's previous range.</li>
            <li><strong>EPS In-Line:</strong> Non-GAAP EPS prints between <strong>$2.62 – $2.68</strong> with Gross Margin steady at <strong>67.5% – 68.0%</strong>.</li>
            <li><strong>Prudent Reiteration:</strong> Management maintains full-year procedure volume guidance while reiterating China caution.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Sell an <strong>Oct 23, 2026 Weekly Iron Condor ($395/$405 Put Spread + $455/$465 Call Spread)</strong> to harvest elevated options implied volatility (IV crush).
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">REDUCE / HEDGE (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 15% | TARGET: $370–$390 (-9% to -14%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Procedure Deceleration:</strong> Worldwide procedure growth decelerates &lt; <strong>13.5% YoY</strong> on acute hospital softness or international delays.</li>
            <li><strong>Systems Placement Pause:</strong> Hospital capital constraints and lease conversions drag Systems revenue below <strong>$625M</strong>.</li>
            <li><strong>Earnings Miss:</strong> Non-GAAP EPS prints ≤ <strong>$2.52</strong> due to higher DV5 R&amp;D/launch expensing.</li>
            <li><strong>Guidance Cut:</strong> Management trims full-year procedure outlook citing prolonged China anti-corruption headwinds.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Hedge long equity with a <strong>Nov 20, 2026 $415 / $385 Bear Put Spread</strong> or trim position if spot price breaks below the $415 support level.
          </div>
        </div>
      </div>
    </section>

    <div class="footer-meta">
      CONFIDENTIAL • INSTITUTIONAL HEALTHCARE RESEARCH • DATA VERIFIED VIA SEC FORM 10-Q / 10-K FILINGS (Q2 2025 – Q2 2026 ACTUALS) &amp; Q3 2026 CONSENSUS • HOVER OVER ANY UNDERLINED TERM FOR DEFINITIONS
    </div>
"""

draft = {
    "header": {
        "page_title": "ISRG — Pre-Earnings Forensic & Sentiment Tearsheet (Upcoming: Q3 2026 | Last Reported: Q2 2026)",
        "ticker": "ISRG",
        "company_name": "Intuitive Surgical, Inc.",
        "earnings_date": "2026-10-20",
        "spot_price_num": spot_price,
        "market_cap_num": float(truth["valuation_and_market"]["market_cap_millions"] * 1e6),
        "enterprise_value_num": float(truth["valuation_and_market"]["enterprise_value_millions"] * 1e6)
    },
    "kpi_cards": {
        "card_a_cash_flow": {
            "q2_2026_ocf_m": ocf[4],
            "q2_2026_capex_m": capex[4],
            "q2_2026_reported_fcf_m": rep_fcf[4],
            "q2_2026_true_fcf_m": true_fcf[4],
            "capex_to_rev_pct": 3.89,
            "sbc_to_rev_pct": 7.26
        },
        "card_b_debt_liquidity": {
            "cash_and_st_inv_m": cash_st[4],
            "total_debt_and_leases_m": total_debt[4],
            "net_debt_m": net_debt[4],
            "recurring_rev_pct": 83.2
        },
        "card_c_margins": {
            "gaap_gross_margin_pct": gross_margin[4],
            "gaap_operating_margin_pct": operating_margin[4],
            "roic_pct": 18.24,
            "roe_ttm_pct": 18.21
        },
        "card_d_multiples": {
            "trailing_pe": trailing_pe,
            "forward_pe": fwd_pe,
            "price_to_sales_ttm": ps_ttm,
            "ev_to_ebitda": ev_ebitda,
            "short_percent_of_float": short_float
        }
    },
    "historical_table": {
        "quarters": quarters,
        "revenue_m": total_rev,
        "instruments_and_accessories_rev_m": instruments_rev,
        "systems_rev_m": systems_rev,
        "services_rev_m": services_rev,
        "gross_profit_m": gross_profit,
        "operating_expenses_m": opex,
        "operating_income_ebit_m": ebit,
        "net_income_common_m": net_income,
        "ocf_m": ocf,
        "capex_m": capex,
        "reported_fcf_m": rep_fcf,
        "sbc_m": sbc,
        "true_fcf_m": true_fcf
    },
    "historical_table_5q_nums": historical_table_5q_nums,
    "forensic_callout": {
        "fcf_bridge_q0_nums": {
            "ocf": ocf[4],
            "capex": capex[4],
            "reported_fcf": rep_fcf[4],
            "sbc": sbc[4],
            "finance_leases": 0.0,
            "true_fcf": true_fcf[4]
        },
        "flags": [
            "GAAP Net Income ($818.1M) vs. GAAP EBIT ($971.9M) reflects pure operating conversion, routine tax provision ($236.5M), and $82.7M Treasury interest income",
            "da Vinci 5 (DV5) placement acceleration drives GAAP gross margin expansion to 67.78% (+172 bps QoQ)",
            "Razor-and-blade recurring revenue stability exceeds 83% of total revenue across 9,500+ installed systems",
            "Elite capital-light cash compounding with CapEx at just 3.89% of revenue and $948.4M Reported FCF ($738.5M True FCF)"
        ]
    },
    "execution_audit": {
        "wins": [
            "Accelerating da Vinci 5 clinical adoption and Force Feedback validation",
            "Resilient global surgical procedure volume growth (~15% YoY)",
            "Rapid Ion endoluminal system procedure ramp (+36% YoY)",
            "Operating leverage expansion to 33.60% EBIT margin (+313 bps YoY)"
        ],
        "drags": [
            "China healthcare anti-corruption campaign and domestic robotic competition",
            "Hospital capital equipment budget reviews elongating system purchase cycles",
            "European CE Mark regulatory clearance timing for da Vinci 5",
            "Premium multiple valuation sensitivity (35.3x Forward P/E)"
        ]
    },
    "peer_and_catalysts": {
        "peers": {
            "ISRG": {"rev_growth": "+18.5%", "gross_margin": "67.78%", "op_margin": "33.60%", "fcf_margin": "+32.79%", "fwd_pe": f"{fwd_pe:.1f}x"},
            "SYK": {"rev_growth": "+10.2%", "gross_margin": "64.10%", "op_margin": "21.40%", "fcf_margin": "+16.80%", "fwd_pe": "25.8x"},
            "MDT": {"rev_growth": "+4.6%", "gross_margin": "65.20%", "op_margin": "19.80%", "fcf_margin": "+15.20%", "fwd_pe": "16.2x"},
            "BSX": {"rev_growth": "+13.8%", "gross_margin": "69.30%", "op_margin": "22.10%", "fcf_margin": "+18.40%", "fwd_pe": "28.4x"}
        },
        "catalysts": [
            "da Vinci 5 full-scale volume manufacturing and international regulatory clearances (Europe CE Mark & Japan PMDA)",
            "Single-Port (SP) robotic surgical indication expansions across urology, TORS, and colorectal procedures",
            "AI surgical data analytics and tele-mentoring integration via Intuitive Hub",
            "Multi-decade international procedure penetration runway in general surgery"
        ]
    },
    "sentiment_analysis": {
        "composite_score": 68,
        "pillars": {
            "options": {"score": 72, "pcr_oi": pcr_oi, "implied_move_pct": opt_move_pct, "implied_move_usd": opt_move_usd},
            "revisions": {"score": 68, "up_vs_down": "18 Up vs 4 Down", "consensus_eps": 2.64},
            "retail": {"score": 65, "clinical_demand": "High Surgeon Demand", "survey_score": 80},
            "insider_whale": {"score": 66, "institutional_ownership_pct": 85.4}
        }
    },
    "trade_matrix": {
        "bull_target_low_num": 465.0,
        "bear_target_high_num": 390.0,
        "bull_case": {"prob": "40%", "target_range": "$465–$490", "trigger": "Q3 Rev > $2.95B, Procedures >= 16.5%, Non-GAAP EPS >= $2.75"},
        "base_case": {"prob": "45%", "target_range": "$415–$445", "trigger": "Q3 Rev $2.89B–$2.93B, Procedures +14.5%–15.5%, Non-GAAP EPS $2.62–$2.68"},
        "bear_case": {"prob": "15%", "target_range": "$370–$390", "trigger": "Procedures < 13.5%, Systems < $625M, Non-GAAP EPS <= $2.52"}
    },
    "rendered_container_html": html.strip()
}

DRAFT_PATH.write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"ISRG draft successfully written to {DRAFT_PATH}")
