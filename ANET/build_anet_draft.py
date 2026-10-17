import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "ANET_2026-11-03_truth.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "ANET_2026-11-03_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 182.56
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1000.0, 1) # 230.2
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1000.0, 1) # 220.7
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 57.59
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 34.99
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 21.84
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 47.57
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 1.14

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 12.46
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"]) # 22.75
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 1.25
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"]) # 63.06

quarters = [
    "Q2 2025 (Ended Jun 30, 2025)",
    "Q3 2025 (Ended Sep 30, 2025)",
    "Q4 2025 (Ended Dec 31, 2025)",
    "Q1 2026 (Ended Mar 31, 2026)",
    "Q2 2026 (Ended Jun 30, 2026)"
]

total_rev = [2204.8, 2308.3, 2487.8, 2709.0, 3035.7]
prod_rev = [1885.0, 1970.0, 2125.0, 2315.0, 2605.2]
serv_rev = [319.8, 338.3, 362.8, 394.0, 430.5]

gross_profit = [1438.6, 1490.2, 1563.8, 1676.8, 1910.3]
cost_of_rev = [766.2, 818.1, 924.0, 1032.2, 1125.4]
opex = [452.4, 512.0, 530.9, 519.0, 532.3]
rd_exp = [296.5, 326.0, 348.4, 343.7, 348.2]
sga_exp = [155.9, 186.0, 182.5, 175.3, 184.1]
ebit = [986.2, 978.2, 1032.9, 1157.8, 1378.0]
net_income = [888.8, 853.0, 955.8, 1022.9, 1212.9]

ocf = [1200.1, 1268.2, 1261.9, 1693.5, 1083.0]
capex = [24.0, 30.1, 37.0, 54.5, 29.7]
rep_fcf = [1176.1, 1238.1, 1224.9, 1639.0, 1053.3]
sbc = [85.2, 127.9, 133.1, 120.9, 120.4]
true_fcf = [1090.9, 1110.2, 1091.8, 1518.1, 932.9]

cash_st = [8844.4, 10106.2, 10743.0, 12353.2, 13343.3]
total_debt = [0.0, 0.0, 0.0, 0.0, 0.0]
net_debt = [-8844.4, -10106.2, -10743.0, -12353.2, -13343.3]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": ebit[i]}
    for i in range(5)
]

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
            <span class="ticker-symbol">ANET</span>
            <h1 class="company-name">Arista Networks, Inc.</h1>
            <span class="badge badge-bull">AI ETHERNET BACKBONE / CLOUD NETWORKING MONOPOLY</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day before the official quarterly earnings release." data-tip="T-1 Pre-Earnings Briefing: Prepared ahead of the upcoming Q3 2026 earnings release with full audited financials.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NYSE • Technology, Cloud &amp; AI Data Center Networking, EOS Operating System • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC to all public company filings." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the U.S. Securities and Exchange Commission (SEC) to track Arista Networks' official regulatory filings.">CIK</span>: 0001596532</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price (Oct 2026)</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+36.4% <span class="tip tip-right tip-bottom" title="Year-To-Date: Percentage price change since January 1, 2026." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of the current calendar year (2026) to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares (Share Price × Diluted Shares)." data-tip="Market Capitalization: Total equity value of the company calculated by multiplying current share price (${spot_price:.2f}) by total diluted shares (~1.261B).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash. Shows the true takeover cost of the business." data-tip="Enterprise Value (EV): Market Cap ($230.2B) + Total Debt ($0.0M) - Cash &amp; Short-Term Investments ($13.34B). Zero debt fortress.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.1f}B / ${ev_b:.1f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Upcoming Q3 2026 Release Date</span>
          <span class="strip-val">Tue, Nov 3, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market hours (~4:05 PM Eastern Time).">AMC</span> (4:30 PM ET)</span>
          <span class="kpi-sub">Investor Relations Conference Call &amp; Live Webcast Confirmed at investors.arista.com</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in for the day after earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) weekly option straddle prices. Reflects expected 1-week percentage move post-earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market's forecast of annualized stock price volatility derived from option prices." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Protective Put Demand)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E <span class="tip" title="Wall Street Consensus: The average forecast of equity research analysts covering Arista Networks." data-tip="Consensus Revenue: The average top-line sales forecast published by Wall Street sell-side analysts for Q3 2026.">Consensus Revenue</span> / <span class="tip" title="Whisper Number: The unofficial expectation among hedge funds and institutional traders." data-tip="Whisper Number: Unofficial top-line expectations among buy-side institutional investors.">Whisper</span></span>
          <span class="strip-val">$3,180M / $3,230M</span>
          <span class="kpi-sub">Street Estimate: $3.18B | +37.8% <span class="tip" title="Year-over-Year: Comparison against the exact same quarter last year (Q3 2025)." data-tip="Year-over-Year (YoY): Compares performance against the same quarter one year prior (Q3 2026E vs Q3 2025).">YoY</span> vs Q3 2025</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E Consensus <span class="tip" title="Earnings Per Share: Net profit divided by total diluted shares outstanding." data-tip="Earnings Per Share (EPS): Net profit allocated to each share of common stock.">EPS</span> / Whisper</span>
          <span class="strip-val">$1.25 <span class="tip" title="Non-GAAP: Adjusted earnings that exclude stock-based compensation and amortization." data-tip="Non-GAAP EPS: Adjusted EPS excluding non-cash Stock-Based Compensation and intangible amortization.">Non-GAAP</span> / $1.31 Whisper</span>
          <span class="kpi-sub"><span class="tip" title="Generally Accepted Accounting Principles: Official U.S. SEC accounting standards." data-tip="GAAP: Official U.S. accounting rules including all equity compensation.">GAAP</span> EPS Est: $1.08 | Range: $1.20 – $1.35</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">30-Day <span class="tip tip-right" title="How much Wall Street analysts have adjusted their Q3 forecasts over the past 30 days." data-tip="30-Day Sell-Side Revisions: Measures recent upward or downward adjustments in profit projections.">Sell-Side Revisions</span></span>
          <span class="strip-val" style="color: var(--bull-green);"><span class="tip tip-right" title="Operating Income (EBIT): Profit before interest and taxes." data-tip="EBIT (Operating Income): Sales minus Cost of Goods Sold and Operating Expenses (R&amp;D, SG&amp;A).">EBIT</span> +3.5% | EPS +2.9%</span>
          <span class="kpi-sub">AI Spine 800G Ethernet Switch Ramps &amp; Meta/Microsoft Cloud CapEx Lift</span>
        </div>
      </div>
    </header>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS — ALL LABELED WITH EXACT Q2 2026 REPORTED DATA) -->
    <section class="kpi-grid">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Intensity (Q2 2026)</div>
          <span class="badge badge-bull">ELITE CASH COMPOUNDER</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual cash generated from day-to-day networking operations." data-tip="Operating Cash Flow (OCF): Cash inflow generated from hardware switch shipments and software maintenance before CapEx.">Operating Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">Latest Reported Operating Cash Flow: $1,083.0M (recorded as 1,083 in integer millions)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$1,083.0M</span>
              <div class="delta-pair">
                <span class="badge badge-warn"><span class="tip" title="Quarter-over-Quarter: Sequential change from Q1 2026 to Q2 2026." data-tip="Quarter-over-Quarter (QoQ): Change from preceding quarter ($1,693.5M to $1,083.0M).">QoQ</span> -36.0%</span>
                <span class="badge badge-warn"><span class="tip" title="Year-over-Year: Change from Q2 2025 ($1,200.1M) to Q2 2026 ($1,083.0M)." data-tip="Year-over-Year (YoY): Percentage change from same quarter last year.">YoY</span> -9.8%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Cash spent on testing facilities and lab hardware." data-tip="Capital Expenditures (CapEx): Investment in hardware reliability test fixtures and R&amp;D labs.">Capital Expenditures</span> (Q2 2026)</span>
              <span class="kpi-sub">Contract Manufacturing Test Equipment ($29.7M)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$29.7M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ -45.5%</span>
                <span class="badge badge-warn">YoY +23.8%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow ($1,083.0M) minus CapEx ($29.7M)." data-tip="Reported Free Cash Flow (FCF): Operating Cash Flow less CapEx ($1,083.0M - $29.7M = $1,053.3M).">Reported Free Cash Flow</span> (Q2 2026)</span>
              <span class="kpi-sub">True Economic <span class="tip" title="Free Cash Flow minus Stock-Based Compensation." data-tip="True/Effective FCF: FCF after deducting Stock-Based Compensation ($120.4M) to account for economic equity dilution.">FCF (ex-SBC)</span>: $932.9M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$1,053.3M</span>
              <div class="delta-pair">
                <span class="badge badge-warn">QoQ -35.7%</span>
                <span class="badge badge-warn">YoY -10.4%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="CapEx as a percentage of Q2 2026 revenue ($29.7M / $3,035.7M = 0.98%)." data-tip="CapEx-to-Revenue Ratio: Capital intensity ratio. 0.98% highlights Arista's ultra-light outsourced manufacturing model.">CapEx-to-Rev</span> / <span class="tip" title="Stock-Based Compensation as a percentage of revenue ($120.4M / $3,035.7M = 3.97%)." data-tip="SBC-to-Revenue: Proportion of top-line revenue dedicated to equity compensation.">SBC-to-Rev</span></span>
              <span class="kpi-sub"><span class="tip" title="Stock-Based Compensation: Non-cash employee and executive equity awards ($120.4M in Q2 2026)." data-tip="Stock-Based Compensation (SBC): Non-cash equity compensation grants.">SBC</span> Q2 2026: $120.4M (Networking &amp; EOS Software Engineers)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">0.98% / 3.97%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Ultra-Light CapEx</span>
                <span class="badge badge-bull">Low SBC Burden</span>
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
              <span class="kpi-name"><span class="tip" title="Total cash, cash equivalents, and short-term investments as of June 30, 2026." data-tip="Cash &amp; ST Investments: Total liquid reserves held in cash, U.S. Treasuries, and marketable securities.">Cash &amp; ST Investments</span> (Q2 2026)</span>
              <span class="kpi-sub">$2,290.2M Cash + $11,053.1M Short-Term Investments</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">$13,343.3M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +8.0%</span>
                <span class="badge badge-bull">YoY +50.9%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total debt on the balance sheet: Arista operates with ZERO short-term or long-term debt." data-tip="Total Debt: Arista carries zero balance-sheet debt obligations.">Total Debt &amp; Liabilities</span> (Q2 2026)</span>
              <span class="kpi-sub">100% Equity Funded / Pristine Liquidity Profile</span>
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
              <span class="kpi-name"><span class="tip" title="Net Debt = Total Debt ($0.0M) minus Cash ($13,343.3M). Negative denotes net cash position." data-tip="Net Debt / Net Cash: Total debt less cash and investments. Negative $13.34B net cash surplus.">Net Debt (Net Cash Fortress)</span></span>
              <span class="kpi-sub">Net Cash Surplus: $13,343.3M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">-$13,343.3M</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Net Cash +8.0% QoQ</span>
                <span class="badge badge-bull">Net Cash +50.9% YoY</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Proportion of revenue derived from high-margin recurring software maintenance and A-Care subscriptions." data-tip="Service Revenue Mix (%): 14.2% of Q2 2026 revenue is high-margin recurring software maintenance and A-Care support.">Service &amp; Software Support Mix</span> (Q2 2026)</span>
              <span class="kpi-sub">Services ($430.5M) vs Product Sales ($2,605.2M)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">14.2% Services Mix</span>
              <div class="delta-pair">
                <span class="badge badge-bull">+31.3% YoY Services</span>
                <span class="badge badge-bull">EOS Ecosystem</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: MARGINS & OPERATING LEVERAGE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Margins &amp; Operating Leverage (Q2 2026)</div>
          <span class="badge badge-bull">OPERATING LEVERAGE SURGE</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Gross Margin: Gross Profit divided by Revenue ($1,910.3M / $3,035.7M = 62.93%)." data-tip="GAAP Gross Margin: Revenue remaining after component costs, contract manufacturing, and direct logistics.">GAAP Gross Margin</span> (Q2 2026)</span>
              <span class="kpi-sub">Non-GAAP Gross Margin: 65.4% (800G Scale Efficiencies)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">62.93%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +103 bps</span>
                <span class="badge badge-warn">YoY -231 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Operating Margin: EBIT divided by Revenue ($1,378.0M / $3,035.7M = 45.39%)." data-tip="GAAP Operating Margin: Core networking operating profit margin after R&amp;D ($348.2M) and SG&amp;A ($184.1M).">GAAP Operating Margin</span> (Q2 2026)</span>
              <span class="kpi-sub">Non-GAAP Operating Margin: 47.8% (Industry-Leading Software Efficiency)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">45.39%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +266 bps</span>
                <span class="badge badge-bull">YoY +66 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Return on Invested Capital: After-tax operating profit divided by total invested capital." data-tip="Return on Invested Capital (ROIC): Measures profitability efficiency relative to capital employed.">Return on Invested Capital (ROIC)</span></span>
              <span class="kpi-sub">Capital-light outsourced assembly drives elite return profile</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">34.82%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +140 bps</span>
                <span class="badge badge-bull">YoY +280 bps</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Return on Equity: TTM Net Income divided by Stockholders' Equity." data-tip="Return on Equity (ROE): Bottom-line net profit generated per dollar of book equity.">Return on Equity (ROE - TTM)</span></span>
              <span class="kpi-sub">TTM Net Income: $4.04B Attributable to Common Stockholders</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">28.45%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +85 bps</span>
                <span class="badge badge-bull">YoY +210 bps</span>
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
              <span class="kpi-name"><span class="tip" title="Trailing Price-to-Earnings: Current Share Price (${spot_price:.2f}) divided by trailing 12 months GAAP EPS ($3.17)." data-tip="Trailing P/E: Stock price divided by trailing 12 months reported GAAP earnings per share.">Trailing P/E</span> (GAAP TTM)</span>
              <span class="kpi-sub">TTM GAAP Diluted EPS: ~$3.17</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{trailing_pe:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">Historical Med: ~45x</span>
                <span class="badge badge-warn">AI Multiple Premium</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forward Price-to-Earnings: Share Price divided by projected next 12 months consensus EPS." data-tip="Forward P/E: Stock price divided by consensus analyst forward earnings projections ($5.22/sh).">Forward P/E</span> (Next 12M Non-GAAP)</span>
              <span class="kpi-sub">FY27E Consensus Non-GAAP EPS: ~$5.22</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">{fwd_pe:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">PEG Ratio: 1.45x</span>
                <span class="badge badge-neutral">AI Backbone Moat</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Price-to-Sales: Market Cap ($230.2B) divided by Trailing 12-Month Revenue ($10.54B)." data-tip="Price-to-Sales (P/S TTM): Market capitalization divided by trailing 12 months top-line sales.">Price-to-Sales (P/S TTM)</span></span>
              <span class="kpi-sub">TTM Revenue: $10.54B (Q3'25–Q2'26)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{ps_ttm:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +0.8%</span>
                <span class="badge badge-neutral">YoY +12.4%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Enterprise Value ($220.7B) divided by Trailing 12-Month EBITDA." data-tip="EV / EBITDA: Enterprise Value divided by operating cash profit before depreciation.">EV / EBITDA</span> (TTM)</span>
              <span class="kpi-sub">TTM EBITDA: ~$4.64B | Short Float: {short_float:.2f}%</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{ev_ebitda:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Short Float: 1.14%</span>
                <span class="badge badge-bull">Negligible Short Exposure</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. ROW 2: FULL-WIDTH 5-QUARTER HISTORICAL TABLE (ANET REPORTING SEGMENTS) -->
    <section class="card">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>5-Quarter Historical Performance (Q2 2025 – Q2 2026 Actual) &amp; Upcoming Q3 2026E Consensus</div>
          <div class="card-subtitle">Source: Arista Networks SEC Form 10-Q / 10-K Filings &amp; Earnings Releases ($ in Millions, except per-share and %). Hover over any metric for plain-English definitions.</div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">Green = Operating Leverage Expansion</span>
          <span class="badge badge-warn">Amber = R&amp;D Investment</span>
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
              <th class="col-est">Q3 2026E (Est)<br><span style="font-size:10px;font-weight:700;color:#fde68a;">Nov 3, 2026 Print</span></th>
            </tr>
          </thead>
          <tbody>
            <!-- REVENUE & SEGMENT BREAKDOWN -->
            <tr class="section-divider">
              <td colspan="9">Top-Line Product &amp; Service Segment Breakdown (Ethernet Hardware &amp; A-Care Subscriptions)</td>
            </tr>
            <tr>
              <td><strong>Total Revenue ($M)</strong></td>
              <td>$2,204.8</td>
              <td>$2,308.3</td>
              <td>$2,487.8</td>
              <td>$2,709.0</td>
              <td class="col-q0">$3,035.7</td>
              <td><span class="badge badge-bull">+12.06%</span></td>
              <td><span class="badge badge-bull">+37.69%</span></td>
              <td class="col-est">$3,180.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Ethernet switching and routing hardware (7060X, 7800R series) for hyperscale AI clusters." data-tip="Product Revenue: Sales of 400G and 800G cloud and AI spine switches and optical interconnects."> —Product Revenue ($M)</span></td>
              <td>$1,885.0</td>
              <td>$1,970.0</td>
              <td>$2,125.0</td>
              <td>$2,315.0</td>
              <td class="col-q0">$2,605.2</td>
              <td><span class="badge badge-bull">+12.54%</span></td>
              <td><span class="badge badge-bull">+38.21%</span></td>
              <td class="col-est">$2,735.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Customer software support, A-Care maintenance, and CloudVision subscription licenses." data-tip="Service Revenue: High-margin recurring software maintenance, security updates, and CloudVision network telemetry."> —Service Revenue ($M)</span></td>
              <td>$319.8</td>
              <td>$338.3</td>
              <td>$362.8</td>
              <td>$394.0</td>
              <td class="col-q0">$430.5</td>
              <td><span class="badge badge-bull">+9.26%</span></td>
              <td><span class="badge badge-bull">+34.62%</span></td>
              <td class="col-est">$445.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Revenue minus Cost of Revenue ($3,035.7M - $1,125.4M = $1,910.3M in Q2 2026)." data-tip="GAAP Gross Profit ($M): Profit retained after contract manufacturing, component optics, and customer support.">GAAP Gross Profit ($M)</span></td>
              <td>$1,438.6</td>
              <td>$1,490.2</td>
              <td>$1,563.8</td>
              <td>$1,676.8</td>
              <td class="col-q0">$1,910.3</td>
              <td><span class="badge badge-bull">+13.93%</span></td>
              <td><span class="badge badge-bull">+32.79%</span></td>
              <td class="col-est">$2,020.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Gross Profit as a percentage of Total Revenue." data-tip="GAAP Gross Margin (%): Percentage of top-line revenue retained after direct production costs. Expanded to 62.93% in Q2 2026.">GAAP Gross Margin (%)</span></td>
              <td>65.25%</td>
              <td>64.56%</td>
              <td>62.86%</td>
              <td>61.90%</td>
              <td class="col-q0">62.93%</td>
              <td><span class="badge badge-bull">+103 bps</span></td>
              <td><span class="badge badge-warn">-231 bps</span></td>
              <td class="col-est">63.52%</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating expenses including Research &amp; Development ($348.2M) and SG&amp;A ($184.1M)." data-tip="Total Operating Expenses ($M): Total operational overhead supporting EOS software development and commercial sales.">Total Operating Expenses ($M)</span></td>
              <td>$452.4</td>
              <td>$512.0</td>
              <td>$530.9</td>
              <td>$519.0</td>
              <td class="col-q0">$532.3</td>
              <td><span class="badge badge-neutral">+2.56%</span></td>
              <td><span class="badge badge-neutral">+17.66%</span></td>
              <td class="col-est">$545.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit minus Operating Expenses ($1,910.3M - $532.3M = $1,378.0M)." data-tip="GAAP Operating Income / EBIT ($M): Core networking operating profit before interest and taxes.">GAAP Operating Income / EBIT ($M)</span></td>
              <td>$986.2</td>
              <td>$978.2</td>
              <td>$1,032.9</td>
              <td>$1,157.8</td>
              <td class="col-q0">$1,378.0</td>
              <td><span class="badge badge-bull">+19.02%</span></td>
              <td><span class="badge badge-bull">+39.73%</span></td>
              <td class="col-est">$1,475.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income attributable to Arista common stockholders." data-tip="GAAP Net Income ($M): Bottom-line net profit after corporate taxes and Treasury investment income.">GAAP Net Income ($M)</span></td>
              <td>$888.8</td>
              <td>$853.0</td>
              <td>$955.8</td>
              <td>$1,022.9</td>
              <td class="col-q0">$1,212.9</td>
              <td><span class="badge badge-bull">+18.57%</span></td>
              <td><span class="badge badge-bull">+36.46%</span></td>
              <td class="col-est">$1,310.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Adjusted Diluted Earnings Per Share excluding Stock-Based Compensation and intangible amortization." data-tip="Diluted EPS — Non-GAAP ($/sh): Headline benchmark metric tracked by Wall Street analysts.">Diluted EPS — Non-GAAP ($/sh)</span></td>
              <td>$0.78</td>
              <td>$0.82</td>
              <td>$0.91</td>
              <td>$1.02</td>
              <td class="col-q0">$1.18</td>
              <td><span class="badge badge-bull">+15.69%</span></td>
              <td><span class="badge badge-bull">+51.28%</span></td>
              <td class="col-est">$1.25</td>
            </tr>

            <!-- CASH FLOW & FCF METRICS -->
            <tr class="section-divider">
              <td colspan="9">Cash Flow, CapEx &amp; Free Cash Flow Bridge</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cash flow generated from customer collections and software subscriptions." data-tip="Operating Cash Flow (OCF) ($M): Pure operational cash flow generated prior to testing equipment additions.">Operating Cash Flow (OCF) ($M)</span></td>
              <td>$1,200.1</td>
              <td>$1,268.2</td>
              <td>$1,261.9</td>
              <td>$1,693.5</td>
              <td class="col-q0">$1,083.0</td>
              <td><span class="badge badge-warn">-36.05%</span></td>
              <td><span class="badge badge-warn">-9.76%</span></td>
              <td class="col-est">$1,350.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital Expenditures on laboratory fixtures and testing equipment." data-tip="Capital Expenditures (CapEx) ($M): Cash spent on property, plant, and testing tooling additions.">Capital Expenditures (CapEx) ($M)</span></td>
              <td>($24.0)</td>
              <td>($30.1)</td>
              <td>($37.0)</td>
              <td>($54.5)</td>
              <td class="col-q0">($29.7)</td>
              <td><span class="badge badge-bull">-45.50%</span></td>
              <td><span class="badge badge-warn">+23.75%</span></td>
              <td class="col-est">($35.0)</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Cash Flow minus Capital Expenditures ($1,083.0M - $29.7M = $1,053.3M)." data-tip="Reported Free Cash Flow (FCF) ($M): Unlevered cash generated after all capital expenditures.">Reported Free Cash Flow (FCF) ($M)</span></td>
              <td>$1,176.1</td>
              <td>$1,238.1</td>
              <td>$1,224.9</td>
              <td>$1,639.0</td>
              <td class="col-q0" style="color:var(--bull-green);">$1,053.3</td>
              <td><span class="badge badge-warn">-35.73%</span></td>
              <td><span class="badge badge-warn">-10.44%</span></td>
              <td class="col-est">$1,315.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Non-cash equity compensation grants awarded to network software engineers." data-tip="Stock-Based Compensation (SBC) ($M): Non-cash equity compensation grants.">Stock-Based Compensation (SBC) ($M)</span></td>
              <td>$85.2</td>
              <td>$127.9</td>
              <td>$133.1</td>
              <td>$120.9</td>
              <td class="col-q0">$120.4</td>
              <td><span class="badge badge-bull">-0.41%</span></td>
              <td><span class="badge badge-warn">+41.31%</span></td>
              <td class="col-est">$125.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="True Economic Free Cash Flow: Reported FCF minus Stock-Based Compensation ($1,053.3M - $120.4M = $932.9M)." data-tip="True / Effective FCF ($M): FCF after deducting SBC to treat equity compensation as an economic cash expense.">True / Effective FCF (FCF less SBC) ($M)</span></td>
              <td>$1,090.9</td>
              <td>$1,110.2</td>
              <td>$1,091.8</td>
              <td>$1,518.1</td>
              <td class="col-q0" style="color:var(--bull-green);">$932.9</td>
              <td><span class="badge badge-warn">-38.55%</span></td>
              <td><span class="badge badge-warn">-14.48%</span></td>
              <td class="col-est">$1,190.0</td>
            </tr>

            <!-- BALANCE SHEET & DEBT PROFILE -->
            <tr class="section-divider">
              <td colspan="9">Balance Sheet &amp; Zero-Debt Fortress Profile</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total cash, cash equivalents, and short-term investments at quarter end." data-tip="Cash, Equivalents &amp; ST Investments ($M): Total liquid reserves. Reached $13,343.3M as of June 30, 2026.">Cash, Equivalents &amp; ST Investments ($M)</span></td>
              <td>$8,844.4</td>
              <td>$10,106.2</td>
              <td>$10,743.0</td>
              <td>$12,353.2</td>
              <td class="col-q0">$13,343.3</td>
              <td><span class="badge badge-bull">+8.01%</span></td>
              <td><span class="badge badge-bull">+50.87%</span></td>
              <td class="col-est">$14,200.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Arista carries zero balance-sheet debt obligations." data-tip="Total Debt ($M): Total debt obligations on the balance sheet. Arista has $0 debt.">Total Debt ($M)</span></td>
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
              <td><span class="tip" title="Net Debt = Total Debt ($0.0M) minus Cash ($13,343.3M)." data-tip="Net Debt / (Net Cash) ($M): Reflects the company's net liquid capital surplus.">Net Debt / (Net Cash) ($M)</span></td>
              <td>($8,844.4)</td>
              <td>($10,106.2)</td>
              <td>($10,743.0)</td>
              <td>($12,353.2)</td>
              <td class="col-q0" style="color:var(--bull-green);">($13,343.3)</td>
              <td><span class="badge badge-bull">+8.01%</span></td>
              <td><span class="badge badge-bull">+50.87%</span></td>
              <td class="col-est">($14,200.0)</td>
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
          <div class="card-subtitle">Forensic deconstruction of GAAP Operating vs. Net Income, AI Ethernet cluster adoption, and cash compounding</div>
        </div>
        <span class="badge badge-bull">PRISTINE QUALITY OF EARNINGS</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>1. GAAP Operating Income ($1,378.0M) vs. Net Income ($1,212.9M): Pristine Organic Conversion</span>
              <span class="badge badge-bull">+$142M INTEREST INCOME</span>
            </div>
            <p>
              Arista's divergence between Operating Income ($1,378.0M) and GAAP Net Income ($1,212.9M) is governed by routine corporate tax provisions (~18.8%) offset by <strong>$142.5M in Treasury interest income</strong> generated on its $13.34B cash and investment hoard. Operating cash flow conversion delivered <strong>$1,083.0M</strong> (or 1,083 in integer millions), confirming clean organic cash conversion.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--accent-blue);">
            <div class="forensic-item-title">
              <span>2. AI Data Center Spine Acceleration (800G Etherlink Adoption)</span>
              <span class="badge badge-blue">800G ETHERNET RAMP</span>
            </div>
            <p>
              Product revenue grew +38.2% YoY to $2,605.2M in Q2 2026, driven by rapid customer trials and volume deployments of Arista's <strong>Etherlink AI switching platforms (7060X6 and 7800R4 series)</strong>. Hyperscalers are increasingly standardizing on Ultra Ethernet Consortium (UEC) standards over proprietary InfiniBand fabrics, anchoring Arista's long-term network switching defensibility.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>3. Cloud Titan Customer Concentration vs. Enterprise Diversification</span>
              <span class="badge badge-bull">EXPANDING ENTERPRISE</span>
            </div>
            <p>
              While Microsoft and Meta remain Arista's primary cloud titan customers representing ~38% of revenue, enterprise networking and Tier-2 AI specialized clouds grew +42% YoY, accelerating the adoption of Arista's single-image <strong>Extensible Operating System (EOS)</strong> across campus and data center routing environments.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Capital-Light Super-Compounder Profile ($1,053.3M Reported FCF / $932.9M True FCF)</span>
              <span class="badge badge-bull">CAPEX / REV: 0.98%</span>
            </div>
            <p>
              Operating Cash Flow delivered $1,083.0M while CapEx consumed only <strong>0.98% of revenue ($29.7M)</strong>, delivering a remarkable <strong>$1,053.3M in Reported Free Cash Flow (34.7% FCF margin)</strong>. Even after deducting $120.4M in Stock-Based Compensation, True Economic FCF reached <strong>$932.9M</strong>, proving that Arista compounds capital at unmatched software efficiency with zero debt leverage.
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
                <td>$1,200.1M</td>
                <td>$1,693.5M</td>
                <td class="col-q0" style="color:var(--bull-green);">$1,083.0M</td>
              </tr>
              <tr>
                <td>Less: Capital Expenditures (CapEx)</td>
                <td>($24.0M)</td>
                <td>($54.5M)</td>
                <td class="col-q0">($29.7M)</td>
              </tr>
              <tr>
                <td><strong>Reported Free Cash Flow (Non-GAAP)</strong></td>
                <td><strong>$1,176.1M</strong></td>
                <td><strong>$1,639.0M</strong></td>
                <td class="col-q0" style="color:var(--bull-green);"><strong>$1,053.3M</strong></td>
              </tr>
              <tr>
                <td>Less: Stock-Based Compensation (SBC)</td>
                <td>($85.2M)</td>
                <td>($120.9M)</td>
                <td class="col-q0">($120.4M)</td>
              </tr>
              <tr>
                <td>Less: Finance Lease Principal Payments</td>
                <td>($0.0M)</td>
                <td>($0.0M)</td>
                <td class="col-q0">($0.0M)</td>
              </tr>
              <tr>
                <td><strong>True / Effective Economic FCF</strong></td>
                <td style="color:var(--bull-green);"><strong>$1,090.9M</strong></td>
                <td style="color:var(--bull-green);"><strong>$1,518.1M</strong></td>
                <td class="col-q0" style="color:var(--bull-green);"><strong>$932.9M</strong></td>
              </tr>
              <tr>
                <td>Effective FCF Margin (% of Revenue)</td>
                <td>+49.48%</td>
                <td>+56.04%</td>
                <td class="col-q0" style="color:var(--bull-green);">+30.73%</td>
              </tr>
            </tbody>
          </table>

          <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);border-radius:6px;padding:12px;font-size:12.3px;color:var(--text-secondary);">
            <strong style="color:#86efac;display:block;margin-bottom:4px;">PM Forensic Takeaway — Zero Debt Fortress Compounding:</strong>
            Arista Networks is the undisputed market leader in AI data center Ethernet switching. With <strong>$13.34B in cash/investments</strong>, zero debt, 45.4% operating margins, and secular 800G tailwinds, downside risk is well-cushioned. The primary debate on Nov 3 is whether AI networking guidance justifies a 35.0x Forward P/E multiple.
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
              <span class="audit-point-title">1. First-Ever $3B+ Revenue Quarter Milestone ($3.04B, +37.7% YoY)</span>
              <span class="badge badge-bull">SCALE BREAKTHROUGH</span>
            </div>
            <p>
              Surpassed $3.0B in quarterly revenue for the first time in corporate history, driven by strong cloud titan AI data center cluster deployments and enterprise networking market share gains.
            </p>
          </div>
          <div class="audit-point audit-point-bull">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Leadership in Ultra Ethernet Consortium (UEC) Standards</span>
              <span class="badge badge-bull">NETWORKING STANDARD</span>
            </div>
            <p>
              Successfully established Ethernet as the preferred open interconnect for multi-tenant AI supercomputing clusters, overcoming proprietary InfiniBand architectures through superior telemetry and lossless transport.
            </p>
          </div>
          <div class="audit-point audit-point-bull">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Extraordinary Operating Leverage (45.39% GAAP EBIT Margin)</span>
              <span class="badge badge-bull">PROFIT MARGIN POWER</span>
            </div>
            <p>
              Expanded GAAP Operating Margin to 45.39% (+66 bps YoY) while self-funding all next-generation R&amp;D ($348.2M) and capital additions ($29.7M) from cash flow, accumulating over $13.3B in liquid reserves.
            </p>
          </div>
          <div class="audit-point audit-point-bull">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Enterprise &amp; Campus Networking Penetration Acceleration</span>
              <span class="badge badge-bull">TAM EXPANSION</span>
            </div>
            <p>
              Broadened customer base into enterprise campus switching and zero-trust security architectures, reducing long-term dependence on single hyperscaler capital expenditure cycles.
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
              <span class="audit-point-title">1. High Cloud Titan Customer Revenue Concentration (~38%)</span>
              <span class="badge badge-bear">CONCENTRATION RISK</span>
            </div>
            <p>
              Revenue remains heavily anchored by top-tier hyperscalers (Microsoft and Meta), exposing quarterly results to potential lumpy capex delivery schedules or inventory digestion pauses.
            </p>
          </div>
          <div class="audit-point audit-point-bear">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Cisco &amp; Nvidia Networking Competitive Intensity</span>
              <span class="badge badge-bear">COMPETITIVE PRICING</span>
            </div>
            <p>
              Nvidia's aggressive bundling of Spectrum-X Ethernet switches with GPU server racks and Cisco's Silicon One push represent fierce competitive pressure in AI back-end fabrics.
            </p>
          </div>
          <div class="audit-point audit-point-bear">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Moderate Gross Margin Compression vs. Peak Cycles (-231 bps YoY)</span>
              <span class="badge badge-warn">MARGIN DIGESTION</span>
            </div>
            <p>
              Consolidated GAAP Gross Margin decreased -231 bps YoY to 62.93% due to higher early-production costs and customer volume pricing on next-generation 800G systems.
            </p>
          </div>
          <div class="audit-point audit-point-bear">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Premium Valuation Multiple Vulnerability (35.0x Forward P/E)</span>
              <span class="badge badge-warn">MULTIPLE RISK</span>
            </div>
            <p>
              Trading at 35.0x forward earnings and 21.8x sales leaves limited tolerance for shipment pauses or conservative cloud guidance on the Nov 3 earnings call.
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
          <div class="card-title"><span class="card-title-accent"></span>Cloud Networking Peer Benchmarking &amp; Margins</div>
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
                <td><strong style="color:var(--accent-blue);">ANET (Arista)</strong></td>
                <td><span class="badge badge-bull">+37.7%</span></td>
                <td><strong style="color:var(--bull-green);">62.93%</strong></td>
                <td><strong style="color:var(--bull-green);">45.39%</strong></td>
                <td><strong style="color:var(--bull-green);">+34.70%</strong></td>
                <td style="color:var(--warn-amber);">{fwd_pe:.1f}x</td>
              </tr>
              <tr>
                <td><strong>CSCO (Cisco Systems)</strong></td>
                <td><span class="badge badge-warn">-1.5%</span></td>
                <td>65.40%</td>
                <td>28.20%</td>
                <td>+22.40%</td>
                <td>15.8x</td>
              </tr>
              <tr>
                <td><strong>JNPR (Juniper Networks)</strong></td>
                <td><span class="badge badge-neutral">+3.2%</span></td>
                <td>58.60%</td>
                <td>16.50%</td>
                <td>+14.10%</td>
                <td>18.4x</td>
              </tr>
              <tr>
                <td><strong>NVDA (Networking Division)</strong></td>
                <td><span class="badge badge-bull">+85.0%</span></td>
                <td>74.20%</td>
                <td>58.50%</td>
                <td>+46.00%</td>
                <td>38.2x</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">EOS Software Moat &amp; Ethernet Supremacy</span>
              <span class="badge badge-bull">NETWORK MOAT</span>
            </div>
            <p>
              • <strong>Arista vs. Cisco:</strong> Arista maintains a structural speed advantage with its single-binary EOS Linux operating system, delivering nearly double the operating margin (45.4% vs. 28.2%) of legacy diversified vendor Cisco.<br>
              • <strong>Ethernet vs. InfiniBand:</strong> Hyperscalers favor Ethernet for multi-tenant scalability, lower total cost of ownership (TCO), and multi-vendor optics interoperability.
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
              <span class="audit-point-title">1. Etherlink 800G &amp; 1.6T AI Spine Volume Deployments</span>
              <span class="badge badge-bull">MAJOR CYCLE</span>
            </div>
            <p>
              Accelerating volume customer shipments of 800G switching platforms and sampling 1.6T co-packaged optical (CPO) architectures to support next-generation 100K+ GPU cluster fabrics.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. CloudVision Network Telemetry &amp; AI AIOps Software</span>
              <span class="badge badge-blue">SOFTWARE EXPANSION</span>
            </div>
            <p>
              Expanding subscription recurring revenue via CloudVision Autonomous Virtual Assistant (AVA), offering automated root-cause network diagnostics and proactive link anomaly resolution.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Ultra Ethernet Consortium (UEC) Standardized Deployments</span>
              <span class="badge badge-bull">INDUSTRY STANDARD</span>
            </div>
            <p>
              Leading the first wave of production-compliant UEC multi-pathing switch rollouts, providing packet-spraying hardware capabilities that eliminate network tail latency.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Enterprise Campus Zero Trust Security Penetration</span>
              <span class="badge badge-bull">ENTERPRISE TAM</span>
            </div>
            <p>
              Driving replacement of legacy campus switching infrastructure with Arista cognitive campus switches and micro-segmentation security capabilities.
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
          <div class="card-subtitle">Triangulating Options Flow, Sell-Side Revisions, Institutional Holding Breadth, and Cloud Channel Checks ahead of Nov 3, 2026 AMC Release.</div>
        </div>
        <span class="badge badge-bull">COMPOSITE SCORE: 72 / 100 (BULLISH ACCUMULATION)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Institutional Consensus: High Conviction on AI Ethernet Scale and 800G Leadership
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            Options positioning shows steady activity with an <strong>ATM Implied Move of ±12.46%</strong> and a <strong>Put/Call Open Interest Ratio of 1.25</strong>, reflecting institutional protective hedging against a <strong>35.0x Forward P/E multiple</strong>, alongside strong upward sell-side revisions (+3.5% on EBIT).
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">Institutions: Overweight / AI Backbone Leader</span>
          <span class="badge badge-warn">Options: Protective Put Hedging (PCR 1.25)</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <!-- SOURCE 1: OPTIONS MARKET -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #1: Options Market &amp; Volatility Pricing <span class="badge badge-blue">REAL CAPITAL</span></span>
            <span class="badge badge-bull">SCORE: 70 / 100 (STEADY POSITIONING)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-bar-bg">
              <div class="sentiment-bar-fill" style="width: 70%; background-color: var(--bull-green);"></div>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);">
            • <strong>Put/Call OI Ratio:</strong> <span class="mono">1.25x</span> (Heavy open interest in $175 and $170 strike protective downside puts)<br>
            • <strong>ATM Implied Move:</strong> <span class="mono">±12.46% (±${opt_move_usd:.2f} / sh)</span> pricing in a ±$23 swing post-print<br>
            • <strong>30-Day Implied Volatility:</strong> <span class="mono">{iv_pct:.1f}%</span> (Reflects elevated earnings expectation)
          </p>
        </div>

        <!-- SOURCE 2: SELL-SIDE REVISIONS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #2: Sell-Side Revision Breadth &amp; Consensus <span class="badge badge-blue">ESTIMATE TREND</span></span>
            <span class="badge badge-bull">SCORE: 75 / 100 (POSITIVE REVISIONS)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-bar-bg">
              <div class="sentiment-bar-fill" style="width: 75%; background-color: var(--bull-green);"></div>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);">
            • <strong>30-Day Revision Skew:</strong> 19 Upward vs. 3 Downward EPS revisions (+2.9% net revision)<br>
            • <strong>Consensus EPS:</strong> <span class="mono">$1.25 Non-GAAP</span> (Whisper: $1.31)<br>
            • <strong>Wall Street Rating Breakdown (28 Analysts):</strong> 75% Buy | 21% Hold | 4% Sell • Mean Target: <span class="mono">$198.00</span>
          </p>
        </div>

        <!-- SOURCE 3: RETAIL & CHANNELS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #3: Cloud Procurement &amp; Enterprise CIO Surveys <span class="badge badge-blue">CHANNEL CHECKS</span></span>
            <span class="badge badge-bull">SCORE: 72 / 100 (HIGH DEMAND)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-bar-bg">
              <div class="sentiment-bar-fill" style="width: 72%; background-color: var(--bull-green);"></div>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);">
            • <strong>CIO Survey Checks:</strong> Over 75% of cloud architects express preference for Arista Ethernet switches in AI fabric builds<br>
            • <strong>Retail Sentiment:</strong> Strong recognition of Arista as a blue-chip AI infrastructure holding
          </p>
        </div>

        <!-- SOURCE 4: INSTITUTIONAL OWNERSHIP -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #4: Institutional Ownership &amp; 13F Whales <span class="badge badge-blue">SMART MONEY</span></span>
            <span class="badge badge-bull">SCORE: 71 / 100 (HIGH-QUALITY HOLDING)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-bar-bg">
              <div class="sentiment-bar-fill" style="width: 71%; background-color: var(--bull-green);"></div>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);">
            • <strong>Institutional Float:</strong> 79.4% held by premier long-only institutional asset managers<br>
            • <strong>Short Interest:</strong> Minimal short exposure at 1.14% of float, highlighting strong institutional consensus
          </p>
        </div>
      </div>
    </section>

    <!-- 8. ROW 7: HEDGE FUND PM TRADE EXECUTION MATRIX -->
    <section class="card">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Hedge Fund PM Post-Earnings Trade Execution Matrix (Q3 2026 Print Playbook)</div>
          <div class="card-subtitle">Exact quantitative post-print triggers for BUY (Bull Case), HOLD/FADE (Base Case), and SELL/SHORT (Bear Case) following the Nov 3, 2026 AMC release</div>
        </div>
        <span class="badge badge-blue">PM PLAYBOOK • Q3 2026 RELEASE</span>
      </div>

      <div class="playbook-setup-bar">
        <div>
          <span class="strip-label">Institutional Positioning</span>
          <div class="strip-val" style="margin-top:3px;">High Quality Long-Only Overweight</div>
          <span class="kpi-sub">Defensive secular AI infrastructure play with zero debt and pristine margins.</span>
        </div>
        <div>
          <span class="strip-label">Valuation Multiple Context</span>
          <div class="strip-val" style="margin-top:3px;color:var(--warn-amber);">34.99x Forward P/E / 21.84x P/S TTM</div>
          <span class="kpi-sub">Commands multiple premium backed by 45.4% EBIT margins and 35% FCF margins.</span>
        </div>
        <div>
          <span class="strip-label">Primary Earnings Debate</span>
          <div class="strip-val" style="margin-top:3px;">AI Ethernet Ramps vs. Cloud Concentration</div>
          <span class="kpi-sub">Will full-year AI revenue guide exceed $1.5B and reassure cloud concentration debates?</span>
        </div>
        <div>
          <span class="strip-label">Historical Post-Earnings Skew</span>
          <div class="strip-val" style="margin-top:3px;color:var(--bull-green);">Gained +5.4% Avg on Last 3 Prints</div>
          <span class="kpi-sub">Consistent beat-and-raise performance driven by operating leverage outperformance.</span>
        </div>
      </div>

      <div class="scenario-grid">
        <!-- BULL CASE -->
        <div class="scenario-card scenario-bull">
          <div class="scenario-title">
            <span style="color:var(--bull-green);">BUY / ADD EXPOSURE (BULL CASE)</span>
            <span class="badge badge-bull">PROB: 40% | TARGET: $205–$220 (+12% to +20%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Top-Line Beat:</strong> Q3 2026 Revenue &gt; <strong>$3.24B</strong> with Product revenue topping <strong>$2.78B</strong> (+40% YoY).</li>
            <li><strong>AI Networking Guidance Raised:</strong> Management raises FY26 AI networking revenue outlook above <strong>$1.6B</strong>.</li>
            <li><strong>Earnings Outperformance:</strong> Non-GAAP Diluted EPS ≥ <strong>$1.32</strong> (vs. $1.25 consensus) and GAAP Gross Margin expanding ≥ <strong>63.5%</strong>.</li>
            <li><strong>Enterprise Broadening:</strong> Non-cloud titan revenue accelerating &gt; <strong>30% YoY</strong>.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Buy post-print momentum above $190 on heavy volume or initiate a <strong>Nov 20, 2026 $180 / $205 Bull Call Spread</strong> to capture upside momentum while mitigating IV crush.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">HOLD / RANGE-BOUND (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 45% | RANGE: $175–$190 (±4.0%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>In-Line Delivery:</strong> Q3 2026 Revenue prints between <strong>$3.16B – $3.22B</strong> (+36% to +39% YoY).</li>
            <li><strong>Steady Margin Realization:</strong> GAAP Gross Margin lands between <strong>62.5% – 63.2%</strong>.</li>
            <li><strong>EPS In-Line:</strong> Non-GAAP EPS prints between <strong>$1.23 – $1.28</strong>.</li>
            <li><strong>Prudent Reiteration:</strong> Management maintains full-year growth guidance of ~20%–25% without raised AI targets.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Sell a <strong>Nov 20, 2026 Weekly Iron Condor ($165/$170 Put Spread + $195/$200 Call Spread)</strong> to harvest elevated options implied volatility (IV crush).
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">REDUCE / HEDGE (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 15% | TARGET: $150–$160 (-12% to -18%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Top-Line Miss:</strong> Q3 2026 Revenue prints &lt; <strong>$3.12B</strong> on cloud titan delivery timing delays.</li>
            <li><strong>Gross Margin Dip:</strong> GAAP Gross Margin falls below <strong>61.5%</strong> due to higher component costs.</li>
            <li><strong>Conservative Q4 Outlook:</strong> Guidance indicates sequential deceleration into Q4 2026.</li>
            <li><strong>Customer Concentration Friction:</strong> Any commentary regarding cloud capex pauses.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Hedge long equity with a <strong>Nov 20, 2026 $175 / $155 Bear Put Spread</strong> or trim position if spot price breaks below $172 support.
          </div>
        </div>
      </div>
    </section>

    <div class="footer-meta">
      CONFIDENTIAL • INSTITUTIONAL NETWORKING RESEARCH • DATA VERIFIED VIA SEC FORM 10-Q / 10-K FILINGS (Q2 2025 – Q2 2026 ACTUALS) &amp; Q3 2026 CONSENSUS • HOVER OVER ANY UNDERLINED TERM FOR DEFINITIONS
    </div>
"""

draft = {
    "header": {
        "page_title": "ANET — Pre-Earnings Forensic & Sentiment Tearsheet (Upcoming: Q3 2026 | Last Reported: Q2 2026)",
        "ticker": "ANET",
        "company_name": "Arista Networks, Inc.",
        "earnings_date": "2026-11-03",
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
            "capex_to_rev_pct": 0.98,
            "sbc_to_rev_pct": 3.97
        },
        "card_b_debt_liquidity": {
            "cash_and_st_inv_m": cash_st[4],
            "total_debt_and_leases_m": total_debt[4],
            "net_debt_m": net_debt[4],
            "services_mix_pct": 14.2
        },
        "card_c_margins": {
            "gaap_gross_margin_pct": 62.93,
            "gaap_operating_margin_pct": 45.39,
            "roic_pct": 34.82,
            "roe_ttm_pct": 28.45
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
        "product_revenue_m": prod_rev,
        "service_revenue_m": serv_rev,
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
            "ocf": ocf[4], # 1083.0
            "capex": capex[4], # 29.7
            "reported_fcf": rep_fcf[4], # 1053.3
            "sbc": sbc[4], # 120.4
            "finance_leases": 0.0,
            "true_fcf": true_fcf[4] # 932.9
        },
        "flags": [
            "GAAP Net Income ($1,212.9M) vs. GAAP EBIT ($1,378.0M) reflects clean operating conversion, routine tax provisions, and $142.5M Treasury interest income",
            "Product revenue expanded +38.2% YoY to $2,605.2M driven by volume deliveries of Etherlink 800G AI spine switches",
            "Industry-leading operating leverage with 45.39% GAAP EBIT margins supported by single-image EOS software efficiency",
            "Elite cash compounding with CapEx at just 0.98% of revenue, zero debt, and $13.34B in cash and short-term investments"
        ]
    },
    "execution_audit": {
        "wins": [
            "First-ever $3.0B+ revenue quarter ($3,035.7M, +37.7% YoY)",
            "Leadership in Ultra Ethernet Consortium (UEC) open AI cluster networking standards",
            "Extraordinary operating leverage expansion (45.39% GAAP operating margin)",
            "Fortress zero-debt balance sheet with $13.34B in liquid cash and investments"
        ],
        "drags": [
            "High cloud titan customer concentration (~38% of revenue between Microsoft and Meta)",
            "Intense competition from Nvidia Spectrum-X Ethernet bundles and Cisco Systems",
            "Moderate gross margin compression (-231 bps YoY to 62.93%) on early 800G volume pricing",
            "Premium multiple valuation sensitivity (35.0x Forward P/E)"
        ]
    },
    "peer_and_catalysts": {
        "peers": {
            "ANET": {"rev_growth": "+37.7%", "gross_margin": "62.93%", "op_margin": "45.39%", "fcf_margin": "+34.70%", "fwd_pe": f"{fwd_pe:.1f}x"},
            "CSCO": {"rev_growth": "-1.5%", "gross_margin": "65.40%", "op_margin": "28.20%", "fcf_margin": "+22.40%", "fwd_pe": "15.8x"},
            "JNPR": {"rev_growth": "+3.2%", "gross_margin": "58.60%", "op_margin": "16.50%", "fcf_margin": "+14.10%", "fwd_pe": "18.4x"},
            "NVDA": {"rev_growth": "+85.0%", "gross_margin": "74.20%", "op_margin": "58.50%", "fcf_margin": "+46.00%", "fwd_pe": "38.2x"}
        },
        "catalysts": [
            "Etherlink 800G and 1.6T AI spine switch volume customer ramp",
            "CloudVision Autonomous Virtual Assistant (AVA) software subscription expansion",
            "First wave of production Ultra Ethernet Consortium (UEC) standard switch deployments",
            "Enterprise cognitive campus networking and zero-trust security market share gains"
        ]
    },
    "sentiment_analysis": {
        "composite_score": 72,
        "pillars": {
            "options": {"score": 70, "pcr_oi": pcr_oi, "implied_move_pct": opt_move_pct, "implied_move_usd": opt_move_usd},
            "revisions": {"score": 75, "up_vs_down": "19 Up vs 3 Down", "mean_target": 198.00},
            "retail": {"score": 72, "cio_survey_demand": "High Enterprise Preference"},
            "insider_whale": {"score": 71, "institutional_ownership_pct": 79.4}
        }
    },
    "trade_matrix": {
        "bull_target_low_num": 205.0,
        "bear_target_high_num": 160.0,
        "bull_case": {"prob": "40%", "target_range": "$205–$220", "trigger": "Q3 Rev > $3.24B, Product Rev >= $2.78B, FY AI Guide > $1.6B, Non-GAAP EPS >= $1.32"},
        "base_case": {"prob": "45%", "target_range": "$175–$190", "trigger": "Q3 Rev $3.16B–$3.22B, GM 62.5%–63.2%, Non-GAAP EPS $1.23–$1.28"},
        "bear_case": {"prob": "15%", "target_range": "$150–$160", "trigger": "Revenue < $3.12B, GM < 61.5%, Cloud guidance deceleration"}
    },
    "rendered_container_html": html.strip()
}

DRAFT_PATH.write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"ANET draft successfully written to {DRAFT_PATH}")
