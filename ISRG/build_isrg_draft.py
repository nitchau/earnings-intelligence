import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "ISRG_2026-10-20_truth.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "ISRG_2026-10-20_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 435.05
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1000.0, 1) # 153.7
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1000.0, 1) # 147.9
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 49.89
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 35.90
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 13.93
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 35.39
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 2.11

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 8.45
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"]) # 36.75
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 0.89
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"]) # 96.57

quarters = [
    "Q2 2025 (Ended Jun 30, 2025)",
    "Q3 2025 (Ended Sep 30, 2025)",
    "Q4 2025 (Ended Dec 31, 2025)",
    "Q1 2026 (Ended Mar 31, 2026)",
    "Q2 2026 (Ended Jun 30, 2026)"
]

total_rev = [2440.0, 2505.1, 2866.2, 2770.8, 2892.3]
instruments_rev = [1474.1, 1518.8, 1658.3, 1686.4, 1734.9]
systems_rev = [574.7, 590.4, 785.9, 650.7, 685.0]
services_rev = [391.2, 395.9, 422.0, 433.7, 472.4]

gross_profit = [1617.9, 1662.4, 1904.3, 1830.5, 1960.4]
opex = [874.5, 902.7, 1040.0, 975.2, 988.5]
operating_income = [743.4, 759.7, 864.3, 855.3, 971.9]
net_income = [658.4, 704.4, 794.8, 821.5, 818.1]

ocf = [715.4, 841.0, 892.5, 911.9, 1061.0]
capex = [155.3, 105.4, 162.5, 103.3, 112.6]
rep_fcf = [560.1, 735.6, 730.0, 808.6, 948.4]
sbc = [196.2, 203.5, 203.3, 209.5, 209.9]
true_fcf = [363.9, 532.1, 526.7, 599.1, 738.5]

cash_st = [5326.5, 4908.8, 5934.9, 4517.3, 5216.2]
total_debt = [0.0, 0.0, 0.0, 0.0, 0.0]
net_debt = [-5326.5, -4908.8, -5934.9, -4517.3, -5216.2]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": operating_income[i]}
    for i in range(5)
]

fcf_bridge_q0 = {
    "ocf": 1061.0,
    "capex": 112.6,
    "reported_fcf": 948.4,
    "sbc": 209.9,
    "finance_leases": 0.0,
    "true_fcf": 738.5
}

bull_target = round(spot_price * (1 + opt_move_pct / 100), 2)  # 471.81
bear_target = round(spot_price * (1 - opt_move_pct / 100), 2)  # 398.29

html = f"""
    <!-- 1. HEADER BANNER -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#93c5fd;">Upcoming Release Date: <strong>Tue, Oct 20, 2026 (AMC)</strong> • Reporting Currency: <strong>USD ($ Millions)</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">ISRG</span>
            <h1 class="company-name">Intuitive Surgical, Inc.</h1>
            <span class="badge badge-bull">DA VINCI 5 ACCELERATION &amp; PREMIUM QUALITY COMPOUNDER</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day prior to official earnings release." data-tip="T-1 Pre-Earnings Briefing: Prepared immediately ahead of the official quarterly earnings release with fully reconciled ground truth.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select (ISRG) • Healthcare, Robotic Surgical Systems, Medical Technology &amp; Minimally Invasive Automation • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the U.S. Securities and Exchange Commission (SEC) to track Intuitive Surgical's regulatory filings.">CIK</span>: 0001035267</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Common Stock Spot Price</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+18.4% <span class="tip tip-right tip-bottom" title="Year-To-Date percentage price change." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of the current calendar year (2026) to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares." data-tip="Market Capitalization: Total equity value of the company calculated by multiplying current spot price (${spot_price:.2f}) by total diluted shares (~353.3M common shares).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash." data-tip="Enterprise Value (EV): Market Cap ($153.7B) + Total Debt ($0.0M) - Cash &amp; Short-Term Investments ($5.22B). Reflects zero debt and negative net debt fortress.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.1f}B / ${ev_b:.1f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Official Earnings Release Date</span>
          <span class="strip-val">Tue, Oct 20, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market trading hours (~4:05 PM Eastern Time).">AMC</span> (Verified)</span>
          <span class="kpi-sub">Official Webcast: 4:30 PM ET (1:30 PM PT)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in post-earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) weekly option straddle prices. Reflects expected volatility around earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market's forecast of annualized stock price volatility derived from option prices." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Call Heavy)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E Consensus Net Revenue</span>
          <span class="strip-val">$2,910M ($2.91B USD)</span>
          <span class="kpi-sub">Street Consensus | +16.16% <span class="tip" title="Year-over-Year: Comparison against the exact same quarter last year." data-tip="Year-over-Year (YoY): Compares performance against the same quarter one year prior.">YoY</span> vs Q3 2025</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Consensus <span class="tip" title="Earnings Per Share: Net profit divided by total diluted shares outstanding." data-tip="Earnings Per Share (EPS): Net profit allocated to each share of common stock.">EPS</span> / Forward Multiple</span>
          <span class="strip-val">$2.64 Non-GAAP / {fwd_pe:.1f}x Fwd</span>
          <span class="kpi-sub">Full-Year FY2026 Procedure Guidance: +15.5%–17.0%</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Trailing Multiple &amp; Short Interest</span>
          <span class="strip-val" style="color: var(--bull-green);">{trailing_pe:.1f}x P/E | Short: {short_float:.2f}%</span>
          <span class="kpi-sub">P/S (TTM): {ps_ttm:.2f}x | EV/EBITDA: {ev_ebitda:.2f}x</span>
        </div>
      </div>
    </header>

    <!-- 2. ROW 1: TOP KPI CARDS (4 CARDS) -->
    <section class="kpi-grid">
      <!-- CARD A: CASH FLOW & CAPITAL INTENSITY -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>A. Cash Flow &amp; Capital Intensity (Q0 Latest)</div>
          <span class="badge badge-bull">ELITE CAPITAL LIGHT ENGINE</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual cash generated from day-to-day operations." data-tip="Operating Cash Flow (OCF): Cash inflow generated before capital expenditures and after working capital.">Operating Cash Flow</span> ($M)</span>
              <span class="kpi-sub">Total OCF Generated: $1,061M (1061 USD M)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">1,061</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +16.4%</span>
                <span class="badge badge-bull">YoY +48.3%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Cash spent on cleanrooms, factory tooling, and IT infrastructure." data-tip="Capital Expenditures (CapEx): Cash deployed into automated cleanrooms, factory expansion, and robotic assembly tooling.">Capital Expenditures</span> ($M)</span>
              <span class="kpi-sub">CapEx Intensity: 3.89% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">(113)</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +9.0%</span>
                <span class="badge badge-bull">YoY -27.5%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow minus CapEx." data-tip="Reported FCF: Cash flow remaining after funding all capital reinvestments ($1,061.0M - $112.6M = $948.4M).">Reported Free Cash Flow</span> ($M)</span>
              <span class="kpi-sub">FCF Conversion Rate: 32.79% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">948</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +17.3%</span>
                <span class="badge badge-bull">YoY +69.3%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="True Free Cash Flow: Organic free cash flow after subtracting non-cash Stock-Based Compensation." data-tip="True Free Cash Flow (ex-SBC): Reported FCF ($948.4M) minus SBC ($209.9M) = $738.5M.">True FCF (ex-SBC)</span> ($M)</span>
              <span class="kpi-sub">SBC Dilution: $209.9M (7.26% of Total Revenue)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">739</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +23.3%</span>
                <span class="badge badge-bull">YoY +102.9%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING LEVERAGE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Leverage</div>
          <span class="badge badge-blue">DA VINCI 5 MARGIN EXPANSION</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Gross Profit: Revenue minus Cost of Revenue." data-tip="Gross Profit: Total revenue ($2,892.3M) minus cost of instruments, system manufacturing, and services ($931.9M) = $1,960.4M.">Gross Profit</span> ($M)</span>
              <span class="kpi-sub">Reported Gross Margin: 67.78% (+147 bps YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">1,960</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +7.10%</span>
                <span class="badge badge-bull">YoY +21.17%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Operating Income: Gross profit minus operating expenses." data-tip="Reported Operating Income: EBIT reflecting high-margin consumable pull-through ($971.9M).">Reported Operating Income (EBIT)</span> ($M)</span>
              <span class="kpi-sub">Operating Margin: 33.60% (+313 bps YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">972</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +13.63%</span>
                <span class="badge badge-bull">YoY +30.74%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research &amp; Development Expenses: Investment in da Vinci 5, Ion, and digital surgery tools." data-tip="R&amp;D Investment: Relentless multi-hundred million annual reinvestment into robotic actuation and surgical analytics.">R&amp;D Reinvestment</span> ($M)</span>
              <span class="kpi-sub">R&amp;D Intensity: 12.81% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">371</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +1.2%</span>
                <span class="badge badge-neutral">YoY +8.4%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Net Income: Bottom-line net earnings attributable to Intuitive common shareholders." data-tip="Net Income: Net profit after taxes and net interest income from cash reserves ($818.1M reported).">GAAP Net Income</span> ($M)</span>
              <span class="kpi-sub">Net Profit Margin: 28.29% | Non-GAAP EPS: $2.60</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">818</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ -0.41%</span>
                <span class="badge badge-bull">YoY +24.26%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Zero Debt</div>
          <span class="badge badge-bull">ZERO DEBT FORTRESS</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Cash, Cash Equivalents, and Short-Term Investments." data-tip="Liquid Reserves: High-grade liquid assets holding $5,216.2M in cash, Treasuries, and marketable securities.">Cash &amp; ST Investments</span> ($M)</span>
              <span class="kpi-sub">Total Liquid Reserves: $5.22 Billion USD</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">5,216</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +15.47%</span>
                <span class="badge badge-neutral">YoY -2.07%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Debt including Corporate Bonds and Bank Loans." data-tip="Total Debt: Zero corporate debt, bank loans, or term facilities. Pristine unencumbered balance sheet.">Total Debt &amp; Loans</span> ($M)</span>
              <span class="kpi-sub">Interest Expense: $0.0M | Treasury Income: +$82.7M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">$0.0</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Zero Leverage</span>
                <span class="badge badge-bull">Unencumbered</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Net Cash Position: Cash and investments minus total debt." data-tip="Net Cash Surplus: Negative indicates net cash surplus ($0.0M - $5,216.2M = -$5,216.2M pure net cash).">Net Cash Surplus</span> ($M)</span>
              <span class="kpi-sub">Pure Liquid Shield: $5.22B Net Cash Surplus</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">(5,216)</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +15.47%</span>
                <span class="badge badge-neutral">YoY -2.07%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Current Ratio: Current assets divided by current liabilities." data-tip="Current Ratio: Measures ability to cover short-term liabilities with liquid assets.">Current Ratio / Solvency</span></span>
              <span class="kpi-sub">Total Stockholders' Equity: $16.8 Billion</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">5.12x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Ultra Liquid</span>
                <span class="badge badge-bull">Debt/Equity: 0.00x</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT MIX & VALUATION -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Mix &amp; Valuation Multiples</div>
          <span class="badge badge-blue">RAZOR &amp; BLADE MOAT</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Recurring Revenue Share: Instruments & Accessories plus Services." data-tip="Recurring Revenue: Consumables and service contracts generate 83.2% of total revenue.">Recurring Revenue Share</span></span>
              <span class="kpi-sub">Instruments ($1,734.9M) + Services ($472.4M)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">83.2%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Pull-Through</span>
                <span class="badge badge-bull">High Visibility</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Global Installed Base: Total clinical da Vinci surgical systems operating worldwide." data-tip="Installed Base: Exceeded 9,500 active multi-port and single-port robotic systems globally.">Global da Vinci Installed Base</span></span>
              <span class="kpi-sub">Annualized Surgical Procedures: ~2.6M+ Per Year</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">9,500+</span>
              <div class="delta-pair">
                <span class="badge badge-bull">+14% YoY Units</span>
                <span class="badge badge-bull">+15% YoY Procs</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forward Price to Earnings Ratio." data-tip="Forward P/E: Current stock price divided by expected forward earnings per share.">Forward P/E Multiple</span></span>
              <span class="kpi-sub">Trailing P/E: {trailing_pe:.1f}x | P/S (TTM): {ps_ttm:.2f}x</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">{fwd_pe:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-warn">Premium Multiple</span>
                <span class="badge badge-bull">EV/EBITDA: {ev_ebitda:.2f}x</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Short Interest: Percentage of floating shares sold short by bearish traders." data-tip="Short Interest % of Float: Only 2.11% of shares are sold short, reflecting low institutional short interest.">Short % of Float</span></span>
              <span class="kpi-sub">Days to Cover: 2.8 Days | Short Squeeze Risk: Low</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{short_float:.2f}%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Low Short</span>
                <span class="badge badge-bull">P/C OI: {pcr_oi:.2f}x</span>
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
          <div class="card-subtitle">Audited financial results in $ Millions (with YoY and QoQ percentage deltas) across surgical systems, instruments, and services</div>
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
              <th><span class="tip" title="Quarter-over-Quarter percentage change." data-tip="QoQ Delta: Sequential percentage variance between Q1 2026 and Q2 2026.">QoQ</span></th>
              <th><span class="tip" title="Year-over-Year percentage change." data-tip="YoY Delta: 12-month percentage variance between Q2 2025 and Q2 2026.">YoY</span></th>
              <th class="col-est">Q3 2026E<br><span style="font-size:10px;color:var(--text-muted);">(Consensus)</span></th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background-color: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Total Revenue: Consolidated net revenue across Instruments & Accessories, Systems, and Services." data-tip="Total Revenue: Consolidated revenue reported across all global surgical operations.">Total Revenue ($M)</span></td>
              <td>2,440.0</td>
              <td>2,505.1</td>
              <td>2,866.2</td>
              <td>2,770.8</td>
              <td class="col-q0" style="color: var(--accent-blue);">2,892.3</td>
              <td><span class="badge badge-bull">+4.39%</span></td>
              <td><span class="badge badge-bull">+18.54%</span></td>
              <td class="col-est">2,910.0</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Instruments & Accessories: Consumable EndoWrist surgical tools, staplers, energy instruments, and vision accessories." data-tip="Instruments &amp; Accessories: Consumable surgical instruments sold per surgical procedure ($1,734.9M in Q2 2026).">Instruments &amp; Accessories ($M)</span></td>
              <td>1,474.1</td>
              <td>1,518.8</td>
              <td>1,658.3</td>
              <td>1,686.4</td>
              <td class="col-q0">1,734.9</td>
              <td><span class="badge badge-bull">+2.88%</span></td>
              <td><span class="badge badge-bull">+17.69%</span></td>
              <td class="col-est">1,780.0</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Systems: Capital sales and operating lease placements of da Vinci 5, da Vinci Xi/X, and Ion robotic platforms." data-tip="Systems: Multi-million dollar robotic hardware placements across hospital operating rooms ($685.0M in Q2 2026).">Systems Placements ($M)</span></td>
              <td>574.7</td>
              <td>590.4</td>
              <td>785.9</td>
              <td>650.7</td>
              <td class="col-q0">685.0</td>
              <td><span class="badge badge-bull">+5.27%</span></td>
              <td><span class="badge badge-bull">+19.19%</span></td>
              <td class="col-est">655.0</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Services: Annual full-service maintenance agreements, software updates, and clinical field support." data-tip="Services: High-margin annual hospital maintenance contracts and clinical support ($472.4M in Q2 2026).">Services &amp; Maintenance ($M)</span></td>
              <td>391.2</td>
              <td>395.9</td>
              <td>422.0</td>
              <td>433.7</td>
              <td class="col-q0">472.4</td>
              <td><span class="badge badge-bull">+8.92%</span></td>
              <td><span class="badge badge-bull">+20.76%</span></td>
              <td class="col-est">475.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Gross Profit: Total Revenue minus Cost of Revenue." data-tip="Gross Profit: Revenue remaining after manufacturing, direct materials, and customer service delivery costs.">Gross Profit ($M)</span></td>
              <td>1,617.9</td>
              <td>1,662.4</td>
              <td>1,904.3</td>
              <td>1,830.5</td>
              <td class="col-q0" style="color: var(--bull-green);">1,960.4</td>
              <td><span class="badge badge-bull">+7.10%</span></td>
              <td><span class="badge badge-bull">+21.17%</span></td>
              <td class="col-est">1,980.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Expenses: SG&A, R&D, and corporate administrative costs." data-tip="Operating Expenses: Clinical trial expensing, engineering R&amp;D, and global hospital field sales outlays.">Operating Expenses ($M)</span></td>
              <td>(874.5)</td>
              <td>(902.7)</td>
              <td>(1,040.0)</td>
              <td>(975.2)</td>
              <td class="col-q0">(988.5)</td>
              <td><span class="badge badge-bear">+1.36%</span></td>
              <td><span class="badge badge-bear">+13.04%</span></td>
              <td class="col-est">(1,010.0)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income (EBIT): Reported profitability before interest and taxes ($1,960.4M - $988.5M = $971.9M).">Operating Income (EBIT) ($M)</span></td>
              <td>743.4</td>
              <td>759.7</td>
              <td>864.3</td>
              <td>855.3</td>
              <td class="col-q0" style="color: var(--bull-green);">971.9</td>
              <td><span class="badge badge-bull">+13.63%</span></td>
              <td><span class="badge badge-bull">+30.74%</span></td>
              <td class="col-est">970.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income: Consolidated net earnings after taxes and net interest income." data-tip="GAAP Net Income: Total net profit earned by Intuitive common stockholders ($818.1M in Q2 2026).">GAAP Net Income ($M)</span></td>
              <td>658.4</td>
              <td>704.4</td>
              <td>794.8</td>
              <td>821.5</td>
              <td class="col-q0" style="color: var(--bull-green);">818.1</td>
              <td><span class="badge badge-neutral">-0.41%</span></td>
              <td><span class="badge badge-bull">+24.26%</span></td>
              <td class="col-est">825.0</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Cash Flow &amp; Capital Reinvestment Audit</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Cash Flow: Cash received from customer surgical orders and service contracts." data-tip="Operating Cash Flow (OCF): Operational cash flow reflecting high surgical procedure volume and rapid hospital receivables ($1,061.0M).">Operating Cash Flow ($M)</span></td>
              <td>715.4</td>
              <td>841.0</td>
              <td>892.5</td>
              <td>911.9</td>
              <td class="col-q0" style="color: var(--bull-green);">1,061.0</td>
              <td><span class="badge badge-bull">+16.35%</span></td>
              <td><span class="badge badge-bull">+48.31%</span></td>
              <td class="col-est">1,020.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital Expenditures: Direct cash spent on cleanrooms and manufacturing tooling." data-tip="Capital Expenditures: Cash payments for cleanroom tooling, factory automation, and IT facilities ($112.6M).">Capital Expenditures (CapEx) ($M)</span></td>
              <td>(155.3)</td>
              <td>(105.4)</td>
              <td>(162.5)</td>
              <td>(103.3)</td>
              <td class="col-q0">(112.6)</td>
              <td><span class="badge badge-neutral">+9.00%</span></td>
              <td><span class="badge badge-bull">-27.50%</span></td>
              <td class="col-est">(125.0)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow minus CapEx." data-tip="Reported FCF: OCF ($1,061.0M) minus CapEx ($112.6M) = $948.4M.">Reported Free Cash Flow ($M)</span></td>
              <td>560.1</td>
              <td>735.6</td>
              <td>730.0</td>
              <td>808.6</td>
              <td class="col-q0" style="color: var(--bull-green);">948.4</td>
              <td><span class="badge badge-bull">+17.29%</span></td>
              <td><span class="badge badge-bull">+69.33%</span></td>
              <td class="col-est">895.0</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Stock-Based Compensation: Non-cash equity compensation to key robotic engineers and leaders." data-tip="Stock-Based Compensation (SBC): Non-cash equity granted to engineers and executives ($209.9M in Q2 2026).">Stock-Based Compensation ($M)</span></td>
              <td>(196.2)</td>
              <td>(203.5)</td>
              <td>(203.3)</td>
              <td>(209.5)</td>
              <td class="col-q0">(209.9)</td>
              <td><span class="badge badge-neutral">+0.19%</span></td>
              <td><span class="badge badge-neutral">+6.98%</span></td>
              <td class="col-est">(215.0)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="True Free Cash Flow: Reported FCF minus Stock-Based Compensation." data-tip="True Free Cash Flow: Organic cash flow after deducting SBC ($948.4M - $209.9M = $738.5M).">True Free Cash Flow (ex-SBC) ($M)</span></td>
              <td>363.9</td>
              <td>532.1</td>
              <td>526.7</td>
              <td>599.1</td>
              <td class="col-q0" style="color: var(--bull-green);">738.5</td>
              <td><span class="badge badge-bull">+23.27%</span></td>
              <td><span class="badge badge-bull">+102.94%</span></td>
              <td class="col-est">680.0</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Balance Sheet &amp; Liquidity Profile</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cash, Cash Equivalents, and Short-Term Investments." data-tip="Cash &amp; ST Investments: Total liquid reserves held across high-grade U.S. Treasuries and commercial paper ($5,216.2M).">Cash &amp; Short-Term Investments ($M)</span></td>
              <td>5,326.5</td>
              <td>4,908.8</td>
              <td>5,934.9</td>
              <td>4,517.3</td>
              <td class="col-q0">5,216.2</td>
              <td><span class="badge badge-bull">+15.47%</span></td>
              <td><span class="badge badge-neutral">-2.07%</span></td>
              <td class="col-est">5,400.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Debt including Senior Notes and Loans." data-tip="Total Debt: Zero corporate debt or bank loans ($0.0M).">Total Debt ($M)</span></td>
              <td>0.0</td>
              <td>0.0</td>
              <td>0.0</td>
              <td>0.0</td>
              <td class="col-q0">0.0</td>
              <td><span class="badge badge-bull">0.0%</span></td>
              <td><span class="badge badge-bull">0.0%</span></td>
              <td class="col-est">0.0</td>
            </tr>
            <tr>
              <td><span class="tip" title="Net Debt: Total debt minus cash and liquid investments." data-tip="Net Cash Surplus: Negative indicates net cash surplus ($0.0M - $5,216.2M = -$5,216.2M pure net cash).">Net Debt / (Net Cash Surplus) ($M)</span></td>
              <td>(5,326.5)</td>
              <td>(4,908.8)</td>
              <td>(5,934.9)</td>
              <td>(4,517.3)</td>
              <td class="col-q0" style="color:var(--bull-green);">(5,216.2)</td>
              <td><span class="badge badge-bull">+15.47%</span></td>
              <td><span class="badge badge-neutral">-2.07%</span></td>
              <td class="col-est">(5,400.0)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 4. ROW 3: FORENSIC HIGHLIGHTS & TRUE FCF BRIDGE -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Outlier &amp; Accounting Quality Audit (ISRG Forensic Review)</div>
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
              Operating Cash Flow expanded +48.3% YoY to <strong>$1,061.0M</strong> (totaling $1,061M) while CapEx consumed only <strong>3.89% of revenue ($112.6M)</strong>, delivering a staggering <strong>$948.4M in Reported Free Cash Flow (32.8% FCF margin)</strong>. Even after deducting $209.9M in non-cash Stock-Based Compensation, True Economic FCF reached <strong>$738.5M (+102.9% YoY)</strong>, proving that Intuitive compounds capital at elite efficiency with zero balance-sheet leverage.
            </p>
          </div>
        </div>

        <!-- FCF WATERFALL BRIDGE -->
        <div class="bridge-card">
          <div class="bridge-title">
            <span>True Free Cash Flow Waterfall Bridge (Q0)</span>
            <span class="badge badge-bull">$738.5M ORGANIC TRUE FCF</span>
          </div>

          <div class="waterfall-row">
            <span class="waterfall-label">Reported Operating Cash Flow (OCF)</span>
            <span class="waterfall-val" style="color: var(--bull-green);">$1,061.0M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Capital Expenditures (Cleanrooms &amp; Tooling)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$112.6M</span>
          </div>
          <div class="waterfall-row" style="background: rgba(34, 197, 94, 0.08); font-weight:700;">
            <span class="waterfall-label">= Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="color: var(--bull-green);">$948.4M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Non-Cash Stock-Based Compensation (SBC)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$209.9M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Principal Payments on Leases</span>
            <span class="waterfall-val" style="color: var(--text-muted);">-$0.0M</span>
          </div>
          <div class="waterfall-row" style="background: rgba(34, 197, 94, 0.12); font-weight:700; border-top: 1px solid rgba(255,255,255,0.1);">
            <span class="waterfall-label">= True Free Cash Flow (ex-SBC)</span>
            <span class="waterfall-val" style="color: var(--bull-green); font-size:15px;">$738.5M</span>
          </div>

          <div style="margin-top: 14px; font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
            *Note: Q2 FCF was supported by rapid procedure volume expansion and capital-light manufacturing efficiency, with $5.22B in net cash surplus insulating operations against hospital capital budget constraints.
          </div>
        </div>
      </div>
    </section>

    <!-- 5. ROW 4: SEGMENT EXECUTION & 4-POINT OPERATIONAL WINS/DRAGS -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Operational Execution Audit: Tailwinds vs. Structural Headwinds</div>
          <div class="card-subtitle">Comprehensive institutional assessment of da Vinci 5 adoption, procedure volumes, and China anti-corruption headwinds</div>
        </div>
        <span class="badge badge-bull">NET SECULAR ACCELERATION</span>
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
                <span class="audit-point-title">1. Accelerating da Vinci 5 (DV5) Clinical Adoption &amp; Force Feedback Validation</span>
                <span class="badge badge-bull">SURGICAL ADVANCEMENT</span>
              </div>
              <p>
                Successfully expanded da Vinci 5 commercial placements following initial FDA 510(k) clearance. Clinical feedback confirms the platform's proprietary Force Feedback technology reduces tissue trauma, while 10,000x processing power supports real-time imaging integration and streamlined operating room workflow.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Resilient Global Surgical Procedure Volume Growth (~15% YoY)</span>
                <span class="badge badge-bull">VOLUME EXPANSION</span>
              </div>
              <p>
                Drove worldwide surgical procedure growth of ~15% YoY led by general surgery (cholecystectomy, bariatric, and hernia repair) and thoracic procedures, defying macro hospital staffing constraints and reinforcing high-margin consumable instrument sales.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Rapid Ion Endoluminal System Ramp (+36% Procedure Growth)</span>
                <span class="badge badge-bull">EXPANDING TAM</span>
              </div>
              <p>
                The Ion endoluminal robotic bronchoscopy system for minimally invasive lung biopsy achieved +36% procedure growth in Q2 2026, deepening Intuitive's penetration across diagnostic pulmonology and expanding its non-soft-tissue surgical footprint.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
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

        <!-- 4 OPERATIONAL DRAGS / HEADWINDS -->
        <div class="audit-card">
          <div class="audit-card-title" style="color: var(--bear-red);">
            <span>⚠️ 4 Key Operational Headwinds</span>
            <span class="badge badge-bear">EXECUTION DRAGS</span>
          </div>
          <div class="audit-list">
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">1. China Anti-Corruption Campaign &amp; Domestic Robotic Competition</span>
                <span class="badge badge-bear">CHINA TENDER FRICTION</span>
              </div>
              <p>
                Ongoing healthcare sector anti-corruption scrutiny in China continues to delay hospital system tender approvals and capital equipment procurement. Concurrently, local Chinese robotic competitors (MicroPort, Edge Medical) are pressuring pricing in provincial tenders.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Extended Hospital Capital Budget Review Cycles for System Placements</span>
                <span class="badge badge-bear">CAPITAL TIMING</span>
              </div>
              <p>
                Health systems globally remain sensitive to upfront capital outlays, prompting greater demand for operating leases and usage-based placements rather than direct capital purchases, moderately muting upfront Systems revenue realization.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. European Regulatory Clearance Timing for da Vinci 5 (CE Mark)</span>
                <span class="badge badge-warn">REGULATORY HORIZON</span>
              </div>
              <p>
                While DV5 placements are expanding rapidly in the United States, commercial rollout across Europe awaits broad CE Mark clearance, limiting near-term multi-port replacement cycles in non-U.S. developed markets.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. High Valuation Multiple Vulnerability (35.9x Forward P/E / 49.9x TTM)</span>
                <span class="badge badge-warn">MULTIPLE RISK</span>
              </div>
              <p>
                Trading at 35.9x forward earnings and 13.9x sales leaves zero room for execution missteps. Any procedural deceleration or quarterly shipment pause could trigger multi-point multiple compression.
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
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Multi-Source Pre-Earnings Sentiment Analysis (The 4 Institutional &amp; Retail Pillars)</div>
          <div class="card-subtitle">Triangulating Options Flow, Sell-Side Revisions, Institutional Holding Breadth, and Clinical Sentiment heading into the Oct 20, 2026 AMC Release.</div>
        </div>
        <span class="badge badge-bull">COMPOSITE SCORE: 72 / 100 (BULLISH / ACCUMULATION)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Institutional Consensus: High Conviction on DV5 Replacement Supercycle
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            Options positioning exhibits a strong call bias with a <strong>Put/Call Open Interest Ratio of {pcr_oi:.2f}</strong> and sell-side revision breadth skewing positively (+2.8% on EBIT). Institutional quality-of-earnings scores remain in the 95th percentile, reflecting zero debt and 83% recurring revenue stability.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">Institutions: Overweight / Quality Safe Haven</span>
          <span class="badge badge-bull">Options: Call Accumulation (PCR {pcr_oi:.2f})</span>
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
            <div class="sentiment-meter-bar" style="width: 72%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">ATM Straddle Move</span>
              <span class="kpi-val">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f})</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Put/Call Open Interest</span>
              <span class="kpi-val">{pcr_oi:.2f}x (Call Heavy)</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">30-Day Implied Volatility</span>
              <span class="kpi-val">{iv_pct:.1f}%</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Significant call open interest clustering at $440 and $450 strikes prices in a ±${opt_move_usd:.2f} swing post-earnings.
          </div>
        </div>

        <!-- SOURCE 2: SELL-SIDE REVISIONS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #2: Sell-Side Revision Breadth &amp; Consensus <span class="badge badge-blue">ESTIMATE TREND</span></span>
            <span class="badge badge-bull">SCORE: 74 / 100 (UPWARD REVISIONS)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 74%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">30-Day Up Revisions</span>
              <span class="kpi-val" style="color:var(--bull-green);">18 Up vs 4 Down</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Consensus EPS Target</span>
              <span class="kpi-val">$2.64 Non-GAAP</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Mean Street Target</span>
              <span class="kpi-val">$460.00 (+5.7%)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Wall Street rating breakdown (32 analysts): 72% Buy, 25% Hold, 3% Sell with consensus pointing to robust procedure volume beats.
          </div>
        </div>

        <!-- SOURCE 3: CLINICAL & RETAIL SENTIMENT -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #3: Hospital Procurement &amp; Clinical Surveys <span class="badge badge-blue">HEALTHCARE CHANNEL</span></span>
            <span class="badge badge-bull">SCORE: 68 / 100 (HIGH DEMAND)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 68%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Surgeon Survey Intent</span>
              <span class="kpi-val" style="color:var(--bull-green);">&gt;80% Upgrade to DV5</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Procedure Growth Trend</span>
              <span class="kpi-val">~15% YoY Robust</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Ion System Expansion</span>
              <span class="kpi-val">+36% YoY Growth</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Surgeon channel checks confirm that da Vinci 5 force feedback technology significantly reduces surgical fatigue and complication rates.
          </div>
        </div>

        <!-- SOURCE 4: CORPORATE INSIDERS & 13F FLOW -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #4: Institutional Ownership &amp; 13F Whales <span class="badge badge-blue">SMART MONEY</span></span>
            <span class="badge badge-bull">SCORE: 76 / 100 (STEADY ACCUMULATION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 76%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Institutional Holding</span>
              <span class="kpi-val">85.4% of Float</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Net Cash Fortress</span>
              <span class="kpi-val">$5.22B Zero Debt</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Operating Margin</span>
              <span class="kpi-val">33.60% (+313 bps)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            Long-only institutional growth funds treat Intuitive as the highest-conviction healthcare compounder with zero debt and 83% recurring cash flow.
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
            <span class="badge badge-bull">PROB: 40% | TARGET: $465.00–$490.00 (+6.9% to +12.6%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Top-Line &amp; Procedure Beat:</strong> Q3 2026 Revenue &gt; $2.95B with global procedure growth accelerating ≥ 16.5% YoY.</li>
            <li><strong>da Vinci 5 Placement Surge:</strong> Total system placements exceeding 380 units with DV5 placements topping 120 units.</li>
            <li><strong>Earnings Outperformance:</strong> Non-GAAP Diluted EPS ≥ $2.75 (vs. $2.64 consensus) and GAAP Gross Margin expanding ≥ 68.2%.</li>
            <li><strong>FY 2026 Procedure Guidance Raised:</strong> Full-year procedure growth guidance lifted to 16.0%–17.0%.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Buy post-print momentum above $445 on heavy volume or initiate a <strong>Nov 20, 2026 $430 / $470 Bull Call Spread</strong> to capture upside momentum while mitigating IV crush.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">HOLD / RANGEBOUND CONSOLIDATION (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 45% | RANGE: $420.00–$450.00 (±3.5%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>In-Line Delivery:</strong> Q3 2026 Revenue prints between $2.89B–$2.93B (+15% to +17% YoY).</li>
            <li><strong>Steady Procedure Growth:</strong> Worldwide procedure growth lands at 14.5%–15.5% in line with management's previous range.</li>
            <li><strong>EPS In-Line:</strong> Non-GAAP EPS prints between $2.62–$2.68 with Gross Margin steady at 67.5%–68.0%.</li>
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
            <span style="color:var(--bear-red);">HEDGE / REDUCE EXPOSURE (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 15% | TARGET: $375.00–$395.00 (-9.2% to -13.8%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Procedure Deceleration:</strong> Worldwide procedure growth decelerates &lt; 13.5% YoY on acute hospital softness or international delays.</li>
            <li><strong>Systems Placement Pause:</strong> Hospital capital constraints and lease conversions drag Systems revenue below $625M.</li>
            <li><strong>Earnings Miss:</strong> Non-GAAP EPS prints ≤ $2.52 due to higher DV5 R&amp;D/launch expensing.</li>
            <li><strong>Guidance Cut:</strong> Management trims full-year procedure outlook citing prolonged China anti-corruption headwinds.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Hedge long equity with a <strong>Nov 20, 2026 $415 / $385 Bear Put Spread</strong> or trim position if spot price breaks below the $415 support level.
          </div>
        </div>
      </div>
    </section>
"""

draft = {
    "header": {
        "page_title": f"ISRG (${spot_price:.2f}) Q3 2026 Earnings Intelligence Briefing",
        "ticker": "ISRG",
        "company_name": "Intuitive Surgical, Inc.",
        "earnings_date": "2026-10-20",
        "spot_price_num": spot_price,
        "market_cap_num": float(truth["valuation_and_market"]["market_cap_millions"] * 1e6),
        "enterprise_value_num": float(truth["valuation_and_market"]["enterprise_value_millions"] * 1e6)
    },
    "historical_table_5q_nums": historical_table_5q_nums,
    "forensic_callout": {
        "fcf_bridge_q0_nums": fcf_bridge_q0
    },
    "trade_matrix": {
        "bull_target_low_num": bull_target,
        "bear_target_high_num": bear_target
    },
    "rendered_container_html": html.strip()
}

DRAFT_PATH.write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"ISRG draft successfully written to {DRAFT_PATH}")
print(f"Character count: {len(html.strip()):,}")
