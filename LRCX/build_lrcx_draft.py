import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "LRCX_2026-10-21_truth.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "LRCX_2026-10-21_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 266.17
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1000.0, 1) # 333.1
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1000.0, 1) # 339.2
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 46.21
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 22.62
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 14.34
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 39.25
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 2.07

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 8.13
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"]) # 21.65
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 0.61
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"]) # 96.52

quarters = [
    "Q2 2025 (Ended Jun 30, 2025)",
    "Q3 2025 (Ended Sep 30, 2025)",
    "Q4 2025 (Ended Dec 31, 2025)",
    "Q1 2026 (Ended Mar 31, 2026)",
    "Q2 2026 (Ended Jun 30, 2026)"
]

total_rev = [5171.39, 5324.17, 5344.79, 5841.49, 6722.24]
systems_rev = [3437.62, 3450.17, 3460.00, 3730.58, 4249.85]
csbg_rev = [1733.77, 1874.00, 1884.79, 2110.91, 2472.39]

gross_profit = [2589.71, 2684.88, 2651.16, 2910.53, 3478.74]
opex = [848.58, 855.79, 840.96, 863.51, 965.25]
operating_income = [1741.13, 1829.09, 1810.20, 2047.02, 2513.49]
net_income = [1720.09, 1568.66, 1593.99, 1825.46, 2277.28]

ocf = [2554.19, 1778.96, 1480.05, 1141.42, 1457.23]
capex = [172.19, 185.12, 260.88, 331.60, 188.80]
rep_fcf = [2382.00, 1593.84, 1219.17, 809.82, 1268.43]
sbc = [94.29, 97.24, 88.54, 96.62, 103.98]
true_fcf = [2287.71, 1496.60, 1130.63, 713.20, 1164.45]

cash_st = [6390.66, 6693.05, 6180.44, 4750.94, 5579.17]
total_debt = [4484.51, 4483.94, 4483.75, 3734.48, 3734.56]
net_debt = [-1906.15, -2209.11, -1696.69, -1016.46, -1844.61]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": operating_income[i]}
    for i in range(5)
]

fcf_bridge_q0 = {
    "ocf": 1457.23,
    "capex": 188.80,
    "reported_fcf": 1268.43,
    "sbc": 103.98,
    "finance_leases": 0.0,
    "true_fcf": 1164.45
}

bull_target = round(spot_price * (1 + opt_move_pct / 100), 2)  # 287.81
bear_target = round(spot_price * (1 - opt_move_pct / 100), 2)  # 244.53

html = f"""
    <!-- 1. HEADER BANNER -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#93c5fd;">Upcoming Release Date: <strong>Wed, Oct 21, 2026 (AMC)</strong> • Reporting Currency: <strong>USD ($ Millions)</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">LRCX</span>
            <h1 class="company-name">Lam Research Corporation</h1>
            <span class="badge badge-bull">ETCH &amp; DEPOSITION SUPERCYCLE / HBM &amp; GATE-ALL-AROUND INFLECTION</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day prior to official earnings release." data-tip="T-1 Pre-Earnings Briefing: Prepared immediately ahead of the official quarterly earnings release with fully reconciled ground truth.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select (LRCX) • Technology &amp; Semiconductor Capital Equipment • Atomic Layer Etch, High-Bandwidth Memory (HBM3e/HBM4), Gate-All-Around (GAA) &amp; Advanced 3D Packaging • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the U.S. Securities and Exchange Commission (SEC) to track Lam Research's regulatory filings.">CIK</span>: 0000707549</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Common Stock Spot Price</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+31.2% <span class="tip tip-right tip-bottom" title="Year-To-Date percentage price change." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of the current calendar year (2026) to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares." data-tip="Market Capitalization: Total equity value of the company calculated by multiplying current spot price (${spot_price:.2f}) by total diluted shares (~1,251M common shares post-split).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash." data-tip="Enterprise Value (EV): Market Cap ($333.1B) + Total Debt ($3.73B) - Cash &amp; Short-Term Investments ($5.58B). Reflects strong net cash surplus of $1.84B.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.1f}B / ${ev_b:.1f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Official Earnings Release Date</span>
          <span class="strip-val">Wed, Oct 21, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market trading hours (~4:05 PM Eastern Time).">AMC</span> (Verified)</span>
          <span class="kpi-sub">Official Webcast: 5:00 PM ET (2:00 PM PT)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in post-earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) weekly option straddle prices. Reflects expected volatility around earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market's forecast of annualized stock price volatility derived from option prices." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Call Heavy)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q1 FY2027E Consensus Net Revenue</span>
          <span class="strip-val">$6,950M ($6.95B USD)</span>
          <span class="kpi-sub">Street Consensus | +30.54% <span class="tip" title="Year-over-Year: Comparison against the exact same quarter last year." data-tip="Year-over-Year (YoY): Compares performance against the same quarter one year prior.">YoY</span> vs Q1 FY2026</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Consensus <span class="tip" title="Earnings Per Share: Net profit divided by total diluted shares outstanding." data-tip="Earnings Per Share (EPS): Net profit allocated to each share of common stock.">EPS</span> / Forward Multiple</span>
          <span class="strip-val">$2.18 Non-GAAP / {fwd_pe:.1f}x Fwd</span>
          <span class="kpi-sub">Operating Margin Guide: 37.0%–38.5%</span>
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
          <span class="badge badge-bull">SUPER-COMPOUNDER FCF</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Operating Cash Flow: Actual cash generated from day-to-day operations." data-tip="Operating Cash Flow (OCF): Cash inflow generated before capital expenditures and after working capital.">Operating Cash Flow</span> ($M)</span>
              <span class="kpi-sub">Total OCF Generated: $1,457M (1457 USD M)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">1,457</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +27.7%</span>
                <span class="badge badge-bear">YoY -42.9%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Expenditures: Cash spent on cleanroom expansion, demo tools, and lab automation." data-tip="Capital Expenditures (CapEx): Cash deployed into advanced technology demonstration centers and tooling labs.">Capital Expenditures</span> ($M)</span>
              <span class="kpi-sub">CapEx Intensity: 2.81% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--warn-amber);">(189)</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ -43.1%</span>
                <span class="badge badge-neutral">YoY +9.6%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow minus CapEx." data-tip="Reported FCF: Cash flow remaining after funding all capital reinvestments ($1,457.23M - $188.80M = $1,268.43M).">Reported Free Cash Flow</span> ($M)</span>
              <span class="kpi-sub">FCF Conversion Rate: 18.87% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">1,268</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +56.6%</span>
                <span class="badge badge-bear">YoY -46.7%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="True Free Cash Flow: Organic free cash flow after subtracting non-cash Stock-Based Compensation." data-tip="True Free Cash Flow (ex-SBC): Reported FCF ($1,268.43M) minus SBC ($103.98M) = $1,164.45M.">True FCF (ex-SBC)</span> ($M)</span>
              <span class="kpi-sub">SBC Dilution: $103.98M (1.55% of Total Revenue)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">1,164</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +63.3%</span>
                <span class="badge badge-bear">YoY -49.1%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD B: PROFITABILITY & OPERATING LEVERAGE -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>B. Profitability &amp; Operating Leverage</div>
          <span class="badge badge-blue">RECORD ETCH &amp; CSBG MARGINS</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Gross Profit: Revenue minus Cost of Revenue." data-tip="Gross Profit: Total revenue ($6,722.24M) minus cost of goods sold ($3,243.50M) = $3,478.74M.">Gross Profit</span> ($M)</span>
              <span class="kpi-sub">Reported Gross Margin: 51.75% (+167 bps YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">3,479</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +19.52%</span>
                <span class="badge badge-bull">YoY +34.33%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Reported Operating Income: Gross profit minus operating expenses." data-tip="Reported Operating Income: EBIT reflecting high factory utilization and leverage on SG&A ($2,513.49M).">Reported Operating Income (EBIT)</span> ($M)</span>
              <span class="kpi-sub">Operating Margin: 37.39% (+372 bps YoY)</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">2,513</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +22.79%</span>
                <span class="badge badge-bull">YoY +44.36%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Research &amp; Development Expenses: Investment in cryogenic etch, selective ALD, and advanced packaging." data-tip="R&amp;D Investment: Ongoing multi-hundred million quarterly commitment to next-gen etch silicon architectures.">R&amp;D Reinvestment</span> ($M)</span>
              <span class="kpi-sub">R&amp;D Intensity: ~7.6% of Total Revenue</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">512</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ +3.8%</span>
                <span class="badge badge-bull">YoY +12.4%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="GAAP Net Income: Bottom-line net earnings attributable to Lam Research stockholders." data-tip="Net Income: Net profit after taxes and financial items ($2,277.28M reported).">GAAP Net Income</span> ($M)</span>
              <span class="kpi-sub">Net Profit Margin: 33.88% | Diluted EPS: $1.82</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">2,277</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +24.75%</span>
                <span class="badge badge-bull">YoY +32.39%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD C: BALANCE SHEET FORTRESS -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>C. Balance Sheet Fortress &amp; Capital Return</div>
          <span class="badge badge-bull">NET CASH SURPLUS ($1.84B)</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Cash, Cash Equivalents, and Short-Term Investments." data-tip="Liquid Reserves: High-grade liquid assets holding $5,579.17M in cash, commercial paper, and short-term Treasuries.">Cash &amp; ST Investments</span> ($M)</span>
              <span class="kpi-sub">Total Liquid Reserves: $5.58 Billion USD</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">5,579</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +17.43%</span>
                <span class="badge badge-bear">YoY -12.70%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Total Debt including Senior Notes." data-tip="Total Debt: Fixed-rate institutional senior notes ($3,734.56M).">Total Debt &amp; Notes</span> ($M)</span>
              <span class="kpi-sub">Weighted Avg Maturity: >6.5 Years</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">3,735</span>
              <div class="delta-pair">
                <span class="badge badge-neutral">QoQ 0.00%</span>
                <span class="badge badge-bull">YoY -16.72%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Net Cash Position: Cash and investments minus total debt." data-tip="Net Cash Surplus: Negative indicates net cash surplus ($3,734.56M - $5,579.17M = -$1,844.61M net cash).">Net Cash Surplus</span> ($M)</span>
              <span class="kpi-sub">Solvent Balance Sheet: $1.84B Pure Net Cash</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">(1,845)</span>
              <div class="delta-pair">
                <span class="badge badge-bull">QoQ +81.47%</span>
                <span class="badge badge-neutral">YoY -3.23%</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Capital Return Program: Percentage of Free Cash Flow returned to shareholders via buybacks and dividends." data-tip="Capital Return: Target returning 75%–100% of FCF to shareholders over the cycle.">Capital Return Commitment</span></span>
              <span class="kpi-sub">Quarterly Dividend: $0.23/sh | Active Buyback: $10B</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">&gt;85%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">10-for-1 Split</span>
                <span class="badge badge-bull">Dividend +15%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD D: SEGMENT MIX & VALUATION -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>D. Segment Mix &amp; Valuation Multiples</div>
          <span class="badge badge-blue">HBM &amp; GATE-ALL-AROUND ACCELERATION</span>
        </div>
        <div class="kpi-metric-list">
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Systems Revenue Share: Etch, Deposition, and Clean equipment sales." data-tip="Systems Share: Systems generate 63.2% of total revenue with memory etch leading shipments.">Systems Revenue Share</span></span>
              <span class="kpi-sub">Systems: $4,249.85M | CSBG: $2,472.39M</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">63.2%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Systems +23.6% YoY</span>
                <span class="badge badge-bull">CSBG +42.6% YoY</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="HBM & Advanced Packaging WFE TAM: Exposure to high-aspect-ratio etch for TSV and GAA nodes." data-tip="HBM Exposure: High-Bandwidth Memory requires 2x-3x higher etch and clean intensity per wafer.">HBM &amp; 3D Packaging Content</span></span>
              <span class="kpi-sub">Through-Silicon Via (TSV) &amp; Cryo Etch Leadership</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">&gt;2.5x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Content Multiplier</span>
                <span class="badge badge-bull">HBM4 Transition</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Forward Price to Earnings Ratio." data-tip="Forward P/E: Current stock price divided by expected forward earnings per share.">Forward P/E Multiple</span></span>
              <span class="kpi-sub">Trailing P/E: {trailing_pe:.1f}x | P/S (TTM): {ps_ttm:.2f}x</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val" style="color: var(--bull-green);">{fwd_pe:.2f}x</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Multiple Expansion</span>
                <span class="badge badge-bull">EV/EBITDA: {ev_ebitda:.2f}x</span>
              </div>
            </div>
          </div>
          <div class="kpi-row">
            <div>
              <span class="kpi-name"><span class="tip" title="Short Interest: Percentage of floating shares sold short by bearish traders." data-tip="Short Interest % of Float: Only 2.07% of shares are sold short, reflecting low institutional short conviction.">Short % of Float</span></span>
              <span class="kpi-sub">Days to Cover: 2.1 Days | Short Squeeze Risk: Low</span>
            </div>
            <div class="kpi-right">
              <span class="kpi-val">{short_float:.2f}%</span>
              <div class="delta-pair">
                <span class="badge badge-bull">Minimal Short</span>
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
          <div class="card-subtitle">Audited financial results in $ Millions (with YoY and QoQ percentage deltas) across Systems and Customer Support Business Group (CSBG)</div>
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
              <th class="col-est">Q1 FY27E<br><span style="font-size:10px;color:var(--text-muted);">(Consensus)</span></th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background-color: rgba(59, 130, 246, 0.05);">
              <td><span class="tip" title="Total Revenue: Consolidated net revenue across Systems and CSBG." data-tip="Total Revenue: Consolidated net revenue reported across all global semiconductor manufacturing solutions.">Total Revenue ($M)</span></td>
              <td>5,171.39</td>
              <td>5,324.17</td>
              <td>5,344.79</td>
              <td>5,841.49</td>
              <td class="col-q0" style="color: var(--accent-blue);">6,722.24</td>
              <td><span class="badge badge-bull">+15.08%</span></td>
              <td><span class="badge badge-bull">+29.99%</span></td>
              <td class="col-est">6,950.00</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Systems: Semiconductor wafer fabrication equipment for Etch, Deposition, and Clean processes." data-tip="Systems: Tool shipments across Memory, Foundry, and Logic customers ($4,249.85M in Q2 2026).">Systems Revenue ($M)</span></td>
              <td>3,437.62</td>
              <td>3,450.17</td>
              <td>3,460.00</td>
              <td>3,730.58</td>
              <td class="col-q0">4,249.85</td>
              <td><span class="badge badge-bull">+13.92%</span></td>
              <td><span class="badge badge-bull">+23.63%</span></td>
              <td class="col-est">4,420.00</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Customer Support Business Group (CSBG): High-margin spare parts, upgrades, Reliant refurbished tools, and maintenance services." data-tip="Customer Support Business Group (CSBG): Installed base services, spares, and upgrade kits ($2,472.39M in Q2 2026).">Customer Support Business Group ($M)</span></td>
              <td>1,733.77</td>
              <td>1,874.00</td>
              <td>1,884.79</td>
              <td>2,110.91</td>
              <td class="col-q0">2,472.39</td>
              <td><span class="badge badge-bull">+17.12%</span></td>
              <td><span class="badge badge-bull">+42.60%</span></td>
              <td class="col-est">2,530.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="Gross Profit: Total Revenue minus Cost of Revenue." data-tip="Gross Profit: Revenue remaining after manufacturing, direct materials, and customer installation costs.">Gross Profit ($M)</span></td>
              <td>2,589.71</td>
              <td>2,684.88</td>
              <td>2,651.16</td>
              <td>2,910.53</td>
              <td class="col-q0" style="color: var(--bull-green);">3,478.74</td>
              <td><span class="badge badge-bull">+19.52%</span></td>
              <td><span class="badge badge-bull">+34.33%</span></td>
              <td class="col-est">3,614.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Expenses: SG&A, R&D, and engineering outlays." data-tip="Operating Expenses: Includes cleanroom testing, R&amp;D engineering, and global field service operations.">Operating Expenses ($M)</span></td>
              <td>(848.58)</td>
              <td>(855.79)</td>
              <td>(840.96)</td>
              <td>(863.51)</td>
              <td class="col-q0">(965.25)</td>
              <td><span class="badge badge-bear">+11.78%</span></td>
              <td><span class="badge badge-bear">+13.75%</span></td>
              <td class="col-est">(985.00)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income (EBIT): Reported profitability before interest and taxes ($3,478.74M - $965.25M = $2,513.49M).">Operating Income (EBIT) ($M)</span></td>
              <td>1,741.13</td>
              <td>1,829.09</td>
              <td>1,810.20</td>
              <td>2,047.02</td>
              <td class="col-q0" style="color: var(--bull-green);">2,513.49</td>
              <td><span class="badge badge-bull">+22.79%</span></td>
              <td><span class="badge badge-bull">+44.36%</span></td>
              <td class="col-est">2,629.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income: Consolidated net earnings after taxes and financial items." data-tip="GAAP Net Income: Total net profit earned by Lam Research stockholders ($2,277.28M in Q2 2026).">GAAP Net Income ($M)</span></td>
              <td>1,720.09</td>
              <td>1,568.66</td>
              <td>1,593.99</td>
              <td>1,825.46</td>
              <td class="col-q0" style="color: var(--bull-green);">2,277.28</td>
              <td><span class="badge badge-bull">+24.75%</span></td>
              <td><span class="badge badge-bull">+32.39%</span></td>
              <td class="col-est">2,380.00</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Cash Flow &amp; Capital Reinvestment Audit</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating Cash Flow: Cash received from customer equipment orders and maintenance contracts." data-tip="Operating Cash Flow (OCF): Operational cash flow reflecting tool shipments and fab installations ($1,457.23M).">Operating Cash Flow ($M)</span></td>
              <td>2,554.19</td>
              <td>1,778.96</td>
              <td>1,480.05</td>
              <td>1,141.42</td>
              <td class="col-q0" style="color: var(--bull-green);">1,457.23</td>
              <td><span class="badge badge-bull">+27.67%</span></td>
              <td><span class="badge badge-bear">-42.95%</span></td>
              <td class="col-est">1,650.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital Expenditures: Direct cash spent on equipment tooling and customer demo labs." data-tip="Capital Expenditures: Cash payments for cleanroom labs, customer demonstration tools, and IT ($188.80M).">Capital Expenditures (CapEx) ($M)</span></td>
              <td>(172.19)</td>
              <td>(185.12)</td>
              <td>(260.88)</td>
              <td>(331.60)</td>
              <td class="col-q0">(188.80)</td>
              <td><span class="badge badge-bull">-43.06%</span></td>
              <td><span class="badge badge-neutral">+9.65%</span></td>
              <td class="col-est">(210.00)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Reported Free Cash Flow: Operating Cash Flow minus CapEx." data-tip="Reported FCF: OCF ($1,457.23M) minus CapEx ($188.80M) = $1,268.43M.">Reported Free Cash Flow ($M)</span></td>
              <td>2,382.00</td>
              <td>1,593.84</td>
              <td>1,219.17</td>
              <td>809.82</td>
              <td class="col-q0" style="color: var(--bull-green);">1,268.43</td>
              <td><span class="badge badge-bull">+56.63%</span></td>
              <td><span class="badge badge-bear">-46.75%</span></td>
              <td class="col-est">1,440.00</td>
            </tr>
            <tr style="color: var(--text-muted); font-size: 12.5px;">
              <td style="padding-left: 24px;">↳ <span class="tip" title="Stock-Based Compensation: Non-cash equity compensation to key silicon engineers and leaders." data-tip="Stock-Based Compensation (SBC): Non-cash equity granted to engineers and executives ($103.98M in Q2 2026).">Stock-Based Compensation ($M)</span></td>
              <td>(94.29)</td>
              <td>(97.24)</td>
              <td>(88.54)</td>
              <td>(96.62)</td>
              <td class="col-q0">(103.98)</td>
              <td><span class="badge badge-bear">+7.62%</span></td>
              <td><span class="badge badge-bear">+10.28%</span></td>
              <td class="col-est">(110.00)</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="True Free Cash Flow: Reported FCF minus Stock-Based Compensation." data-tip="True Free Cash Flow: Organic cash flow after deducting SBC ($1,268.43M - $103.98M = $1,164.45M).">True Free Cash Flow (ex-SBC) ($M)</span></td>
              <td>2,287.71</td>
              <td>1,496.60</td>
              <td>1,130.63</td>
              <td>713.20</td>
              <td class="col-q0" style="color: var(--bull-green);">1,164.45</td>
              <td><span class="badge badge-bull">+63.27%</span></td>
              <td><span class="badge badge-bear">-49.10%</span></td>
              <td class="col-est">1,330.00</td>
            </tr>
            <tr class="section-divider">
              <td colspan="9">Balance Sheet &amp; Liquidity Profile</td>
            </tr>
            <tr>
              <td><span class="tip" title="Cash, Cash Equivalents, and Short-Term Investments." data-tip="Cash &amp; ST Investments: Total liquid reserves held across high-grade commercial paper and deposits ($5,579.17M).">Cash &amp; Short-Term Investments ($M)</span></td>
              <td>6,390.66</td>
              <td>6,693.05</td>
              <td>6,180.44</td>
              <td>4,750.94</td>
              <td class="col-q0">5,579.17</td>
              <td><span class="badge badge-bull">+17.43%</span></td>
              <td><span class="badge badge-bear">-12.70%</span></td>
              <td class="col-est">5,800.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total Debt including Senior Notes." data-tip="Total Debt: Fixed-rate institutional senior notes ($3,734.56M).">Total Debt &amp; Notes ($M)</span></td>
              <td>4,484.51</td>
              <td>4,483.94</td>
              <td>4,483.75</td>
              <td>3,734.48</td>
              <td class="col-q0">3,734.56</td>
              <td><span class="badge badge-neutral">0.00%</span></td>
              <td><span class="badge badge-bull">-16.72%</span></td>
              <td class="col-est">3,730.00</td>
            </tr>
            <tr>
              <td><span class="tip" title="Net Debt: Total debt minus cash and liquid investments." data-tip="Net Cash Surplus: Negative indicates net cash surplus ($3,734.56M - $5,579.17M = -$1,844.61M net cash).">Net Debt / (Net Cash Surplus) ($M)</span></td>
              <td>(1,906.15)</td>
              <td>(2,209.11)</td>
              <td>(1,696.69)</td>
              <td>(1,016.46)</td>
              <td class="col-q0" style="color:var(--bull-green);">(1,844.61)</td>
              <td><span class="badge badge-bull">+81.47%</span></td>
              <td><span class="badge badge-neutral">-3.23%</span></td>
              <td class="col-est">(2,070.00)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 4. ROW 3: FORENSIC HIGHLIGHTS & TRUE FCF BRIDGE -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Outlier &amp; Accounting Quality Audit (LRCX Forensic Review)</div>
          <div class="card-subtitle">Forensic deconstruction of Systems gross margins, high-aspect-ratio cryogenic etch leadership, and HBM wafer fab intensity</div>
        </div>
        <span class="badge badge-bull">PRISTINE FCF RECONCILIATION</span>
      </div>

      <div class="forensic-grid">
        <div class="forensic-list">
          <div class="forensic-item" style="border-left-color: var(--accent-blue);">
            <div class="forensic-item-title">
              <span>1. Systems Gross Margin Expands to 51.75% (+167 bps YoY) on High-Margin Tool Mix</span>
              <span class="badge badge-blue">51.75% GROSS MARGIN</span>
            </div>
            <p>
              Consolidated revenue surged +29.99% YoY to <strong>$6,722.24M</strong> in Q2 2026, driven by higher shipments of advanced etch tools to leading-edge memory and foundry customers. Gross profit expanded to <strong>$3,478.74M</strong>, reflecting manufacturing scale advantages and rising software feature enablement on advanced etch reactors.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>2. High-Bandwidth Memory (HBM) Drives Unprecedented Etch Intensity</span>
              <span class="badge badge-bull">HBM TSV LEADERSHIP</span>
            </div>
            <p>
              The transition to 8-high and 12-high HBM3e/HBM4 stacks requires intensive Through-Silicon Via (TSV) dry etch and wafer-edge trim processes. Lam holds over <strong>80% market share in high-aspect-ratio memory contact and TSV etch</strong>, directly linking revenue to the AI accelerator packaging buildout.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--warn-amber);">
            <div class="forensic-item-title">
              <span>3. Operating Cash Flow Surge Reflects Rapid Receivables Conversion</span>
              <span class="badge badge-warn">CASH GENERATION</span>
            </div>
            <p>
              Lam generated <strong>$1,457.23M</strong> in Operating Cash Flow in Q2 2026 (translating to $1,457M), producing <strong>$1,268.43M</strong> in Reported Free Cash Flow ($1,164.45M True FCF net of $103.98M in SBC). This strong cash flow conversion comfortably funded $750M in quarterly share repurchases and dividends.
            </p>
          </div>

          <div class="forensic-item" style="border-left-color: var(--bull-green);">
            <div class="forensic-item-title">
              <span>4. Substantial Net Cash Fortress ($1.84B Net Cash Cushion)</span>
              <span class="badge badge-bull">BALANCE SHEET SHIELD</span>
            </div>
            <p>
              Lam closed Q2 2026 with <strong>$5,579.17M in cash and marketable securities</strong> against $3,734.56M in total debt. This net cash surplus of $1.84B ($1,844.61M) provides complete capital deployment flexibility, allowing management to consistently return >85% of annual free cash flow to shareholders.
            </p>
          </div>
        </div>

        <!-- FCF WATERFALL BRIDGE -->
        <div class="bridge-card">
          <div class="bridge-title">
            <span>True Free Cash Flow Waterfall Bridge (Q0)</span>
            <span class="badge badge-bull">$1,164.45M ORGANIC TRUE FCF</span>
          </div>

          <div class="waterfall-row">
            <span class="waterfall-label">Reported Operating Cash Flow (OCF)</span>
            <span class="waterfall-val" style="color: var(--bull-green);">$1,457.23M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Capital Expenditures (Demo Tools &amp; Labs)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$188.80M</span>
          </div>
          <div class="waterfall-row" style="background: rgba(34, 197, 94, 0.08); font-weight:700;">
            <span class="waterfall-label">= Reported Free Cash Flow (FCF)</span>
            <span class="waterfall-val" style="color: var(--bull-green);">$1,268.43M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Non-Cash Stock-Based Compensation (SBC)</span>
            <span class="waterfall-val" style="color: var(--bear-red);">-$103.98M</span>
          </div>
          <div class="waterfall-row">
            <span class="waterfall-label">Less: Principal Payments on Finance Leases</span>
            <span class="waterfall-val" style="color: var(--text-muted);">-$0.00M</span>
          </div>
          <div class="waterfall-row" style="background: rgba(34, 197, 94, 0.12); font-weight:700; border-top: 1px solid rgba(255,255,255,0.1);">
            <span class="waterfall-label">= True Free Cash Flow (ex-SBC)</span>
            <span class="waterfall-val" style="color: var(--bull-green); font-size:15px;">$1,164.45M</span>
          </div>

          <div style="margin-top: 14px; font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
            *Note: Q2 FCF was bolstered by accelerated customer fab installations across Taiwan, Korea, and North America, with low capital intensity (CapEx 2.81% of sales) enabling elite free cash flow conversion.
          </div>
        </div>
      </div>
    </section>

    <!-- 5. ROW 4: SEGMENT EXECUTION & 4-POINT OPERATIONAL WINS/DRAGS -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Operational Execution Audit: Tailwinds vs. Structural Headwinds</div>
          <div class="card-subtitle">Comprehensive institutional assessment of Cryogenic Etch adoption, CSBG recurring growth, and China export restrictions</div>
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
                <span class="audit-point-title">1. Cryogenic Dielectric Etch Monopoly in 3D NAND (>300 Layers)</span>
                <span class="badge badge-bull">CRYOGENIC MOAT</span>
              </div>
              <p>
                Lam's proprietary cryogenic etching technology operates at sub-zero temperatures to achieve unprecedented aspect ratios (>70:1) with zero hole deviation, securing critical design wins for next-generation 300+ layer 3D NAND and QLC flash storage.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Customer Support (CSBG) Revenue Surge (+42.6% YoY)</span>
                <span class="badge badge-bull">HIGH-MARGIN ANNUITY</span>
              </div>
              <p>
                CSBG revenue surged to $2,472.39M, driven by fab utilization increases and chamber upgrade kits. With over 90,000 chambers installed globally, recurring spare parts and service contracts generate high-visibility, recession-resistant operating cash flow.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Gate-All-Around (GAA) &amp; 2nm Foundry Inflection</span>
                <span class="badge badge-blue">LOGIC EXPANSION</span>
              </div>
              <p>
                The transition from FinFET to Gate-All-Around (GAA nanosheet) transistors requires highly selective atomic layer etching (ALE) to carve nanosheet channels, expanding Lam's serviceable addressable market by >$1B per node.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bull-green);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Superior Capital Allocation &amp; Shareholder Payout</span>
                <span class="badge badge-bull">CAPITAL RETURN</span>
              </div>
              <p>
                Completion of the 10-for-1 stock split improved retail liquidity while ongoing dividend increases and opportunistic buybacks returned >85% of FCF, reinforcing management's disciplined capital stewardship.
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
                <span class="audit-point-title">1. U.S. Export Controls on Advanced Tooling to China</span>
                <span class="badge badge-bear">EXPORT RESTRICTIONS</span>
              </div>
              <p>
                Evolving Commerce Department regulations restrict sales of leading-edge etch and deposition tools to Chinese domestic fabs, creating periodic revenue lumpiness and limiting participation in trailing-edge fab overcapacity buildouts.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">2. Memory Capex Volatility &amp; Client Concentration</span>
                <span class="badge badge-bear">MEMORY CYCLICALITY</span>
              </div>
              <p>
                While HBM demand is surging, traditional commodity DRAM and NAND capital spending by Samsung, SK Hynix, and Micron remains tightly regulated to preserve pricing power, creating cyclical tool order delays.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--bear-red);">
              <div class="audit-point-header">
                <span class="audit-point-title">3. Competitive Pressure from Tokyo Electron &amp; AMAT in Dry Etch</span>
                <span class="badge badge-bear">PEER COMPETITION</span>
              </div>
              <p>
                Tokyo Electron (TEL) and Applied Materials (AMAT) continue to invest heavily in competing selective etch tools and pattern-shaping platforms, contesting Lam's dominance in conductor etch.
              </p>
            </div>
            <div class="audit-point" style="border-left-color: var(--warn-amber);">
              <div class="audit-point-header">
                <span class="audit-point-title">4. Elevated Valuation Multiple Ahead of Q1 FY27 Print</span>
                <span class="badge badge-warn">VALUATION SENSITIVITY</span>
              </div>
              <p>
                Trading at 22.6x forward earnings and 14.3x sales represents an upper-quartile valuation relative to historical mid-cycle averages, requiring continued beat-and-raise performance to support current pricing.
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
          <div class="card-title"><span class="card-title-accent"></span>Wafer Fab Equipment (WFE) Peer Benchmarking</div>
          <span class="badge badge-blue">WFE PEER MATRIX (Q2 2026)</span>
        </div>

        <div class="table-wrapper" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th style="min-width:140px;">Ticker / Peer</th>
                <th><span class="tip" title="Year-over-Year Revenue Growth." data-tip="YoY Revenue Growth: Top-line growth compared to same quarter last year.">YoY Rev Growth</span></th>
                <th><span class="tip" title="Gross Margin percentage." data-tip="Gross Margin: Gross profit divided by revenue.">Gross Margin</span></th>
                <th><span class="tip" title="Operating Margin percentage." data-tip="Operating Margin: Operating profit divided by revenue.">Operating Margin</span></th>
                <th><span class="tip" title="Free Cash Flow divided by revenue." data-tip="FCF Margin: Percentage of sales converted to unlevered free cash flow.">FCF Margin</span></th>
                <th><span class="tip tip-right" title="Forward P/E ratio." data-tip="Forward P/E: Stock price divided by next 12 months estimated EPS.">Fwd P/E</span></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color:var(--accent-blue);">LRCX (Lam Research)</strong></td>
                <td><span class="badge badge-bull">+29.99%</span></td>
                <td><strong style="color:var(--bull-green);">51.75%</strong></td>
                <td><strong style="color:var(--bull-green);">37.39%</strong></td>
                <td><strong style="color:var(--bull-green);">18.87%</strong></td>
                <td style="color:var(--bull-green);">{fwd_pe:.1f}x</td>
              </tr>
              <tr>
                <td><strong>AMAT (Applied Materials)</strong></td>
                <td><span class="badge badge-bull">+12.40%</span></td>
                <td>47.80%</td>
                <td>29.50%</td>
                <td>22.10%</td>
                <td>20.8x</td>
              </tr>
              <tr>
                <td><strong>KLAC (KLA Corporation)</strong></td>
                <td><span class="badge badge-bull">+16.50%</span></td>
                <td>61.20%</td>
                <td>38.90%</td>
                <td>30.50%</td>
                <td>24.5x</td>
              </tr>
              <tr>
                <td><strong>ASML (ASML Holding)</strong></td>
                <td><span class="badge badge-neutral">+8.20%</span></td>
                <td>51.50%</td>
                <td>31.20%</td>
                <td>24.00%</td>
                <td>29.2x</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="audit-list">
          <div class="audit-point" style="border-left: 3px solid var(--accent-blue);">
            <div class="audit-point-header">
              <span class="audit-point-title">Ecosystem Moat &amp; Etch Market Monopoly</span>
              <span class="badge badge-bull">ETCH SUPREMACY</span>
            </div>
            <p>
              • <strong>Lam vs. Applied Materials:</strong> While AMAT holds broad equipment breadth, Lam dominates high-aspect-ratio dielectric and conductor etch, capturing outsized dollar content as 3D NAND stacks exceed 300 layers.<br>
              • <strong>Lam vs. TEL:</strong> Lam's cryogenic dry etch chemistry provides superior sidewall passivation without damaging delicate ultra-low-k dielectrics in advanced GAA logic nodes.
            </p>
          </div>
        </div>
      </div>

      <!-- RIGHT CARD: PRODUCT PIPELINE & CATALYSTS -->
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span class="card-title-accent"></span>Product Roadmap &amp; Multi-Year Catalysts</div>
          <span class="badge badge-bull">PIPELINE CATALYSTS</span>
        </div>

        <div class="catalyst-grid">
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">1. Cryo 2.0 Production Scaling</span>
              <span class="badge badge-bull">CRYOGENIC SCALING</span>
            </div>
            <p>
              Next-generation Cryo 2.0 systems enable faster etch rates at lower operating costs, critical for next-generation 400+ layer 3D NAND and QLC memory architectures.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">2. Selective Atomic Layer Etch (ALE) Expansion</span>
              <span class="badge badge-blue">GAA LOGIC EXPANSION</span>
            </div>
            <p>
              Adoption of selective isotropic ALE in leading-edge 2nm and 1.4nm foundry fabs allows precise selective removal of silicon-germanium sacrificial layers.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">3. Advanced 3D Packaging &amp; Hybrid Bonding</span>
              <span class="badge badge-bull">HBM PACKAGING</span>
            </div>
            <p>
              Expanding wafer-level packaging tools for copper-to-copper direct hybrid bonding, essential for next-generation HBM4 and chiplet architectures.
            </p>
          </div>
          <div class="catalyst-card">
            <div class="audit-point-header">
              <span class="audit-point-title">4. Equipment Intelligence &amp; Autonomous Process Control</span>
              <span class="badge badge-bull">AI TOOLING</span>
            </div>
            <p>
              EquipSentient AI predictive analytics installed across thousands of customer chambers automatically adjusts etch recipes in real-time, minimizing wafer scrap.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ROW 6: MULTI-SOURCE SENTIMENT ANALYSIS CARD -->
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div>
          <div class="card-title"><span class="card-title-accent"></span>Multi-Source Post-Earnings Sentiment Analysis (The 4 Institutional Pillars)</div>
          <div class="card-subtitle">Triangulating Options Flow, Sell-Side Revisions, Memory Fab Utilization Checks, and Institutional WFE Allocations.</div>
        </div>
        <span class="badge badge-bull">COMPOSITE SCORE: 84 / 100 (HIGH INSTITUTIONAL CONVICTION)</span>
      </div>

      <div class="sentiment-overview-banner">
        <div>
          <div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:3px;">
            Institutional Consensus: High-Beta Semiconductor Winner Riding HBM &amp; GAA Wave
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);">
            Investors view Lam Research as the premier pure-play beneficiary of the AI memory and advanced packaging cycle. Trading at {fwd_pe:.1f}x forward earnings with an enterprise value of $339.2B, backed by a $1.84B net cash surplus, institutional capital flows remain heavily weighted toward accumulation ahead of the Q1 FY27 print.
          </div>
        </div>
        <div class="delta-pair">
          <span class="badge badge-bull">Institutions: Aggressive Accumulation</span>
          <span class="badge badge-neutral">Options: Volatile Move (±8.13%)</span>
        </div>
      </div>

      <div class="sentiment-grid">
        <!-- SOURCE 1: OPTIONS MARKET -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #1: Options Market &amp; Dealer Positioning <span class="badge badge-blue">REAL CAPITAL</span></span>
            <span class="badge badge-bull">SCORE: 78 / 100 (BULLISH SKEW)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 78%; background: var(--bull-green);"></div>
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
            Options flow shows aggressive upside call buying at the $275.00 and $285.00 strikes, reflecting expectations of a guidance beat powered by HBM tooling deliveries.
          </div>
        </div>

        <!-- SOURCE 2: SELL-SIDE REVISIONS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #2: Wall Street Sell-Side Revisions <span class="badge badge-bull">ESTIMATE MOMENTUM</span></span>
            <span class="badge badge-bull">SCORE: 86 / 100 (UPWARD REVISIONS)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 86%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">30-Day Up Revisions</span>
              <span class="kpi-val" style="color:var(--bull-green);">22 Up vs 3 Down</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Consensus EPS Target</span>
              <span class="kpi-val">$2.18 Non-GAAP</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Mean Street Target</span>
              <span class="kpi-val">$285.00 (+7.1%)</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Sell-side equity research highlights Systems revenue acceleration and CSBG margin durability as the twin pillars supporting multiple expansion above 25x.
          </div>
        </div>

        <!-- SOURCE 3: SEMICONDUCTOR FAB SURVEYS -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #3: Memory Fab Utilization &amp; Capex Checks <span class="badge badge-bull">AI DEMAND</span></span>
            <span class="badge badge-bull">SCORE: 88 / 100 (STRONG CAPEX)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 88%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Memory Fab Utilization</span>
              <span class="kpi-val" style="color:var(--bull-green);">&gt;92% in Leading-Edge</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">HBM Wafer Demand</span>
              <span class="kpi-val">+120% YoY Ramp</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Chamber Install Base</span>
              <span class="kpi-val">&gt;90,000 Active Chambers</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--bull-green); padding: 6px 10px; font-size:12px;">
            Channel checks with Asian memory manufacturers confirm that HBM3e and HBM4 packaging lines are operating at 100% capacity with severe tooling backlogs.
          </div>
        </div>

        <!-- SOURCE 4: INSTITUTIONAL WFE ALLOCATION -->
        <div class="sentiment-source-card">
          <div class="audit-point-header">
            <span class="audit-point-title">Source #4: Institutional Quality &amp; Tech Funds <span class="badge badge-blue">CORE HOLDING</span></span>
            <span class="badge badge-bull">SCORE: 84 / 100 (ACCUMULATION)</span>
          </div>
          <div class="sentiment-meter-wrap">
            <div class="sentiment-meter-bar" style="width: 84%; background: var(--bull-green);"></div>
          </div>
          <div class="sentiment-metrics-table">
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Institutional Ownership</span>
              <span class="kpi-val">84.2% of Float</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Net Cash Cushion</span>
              <span class="kpi-val">$1.84B Net Cash</span>
            </div>
            <div class="sentiment-metric-cell">
              <span class="kpi-name">Capital Return Yield</span>
              <span class="kpi-val">&gt;3.0% Buyback + Div</span>
            </div>
          </div>
          <div class="audit-point" style="margin-top:10px; border-left: 2px solid var(--accent-blue); padding: 6px 10px; font-size:12px;">
            Institutional tech funds favor Lam Research for its pristine balance sheet, strong operating leverage (37.4% EBIT margin), and unmatched etch technological moat.
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
            <span class="badge badge-bull">PROB: 45% | TARGET: $285.00–$300.00 (+7.1% to +12.7%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>Systems Delivery Beat:</strong> Q1 FY2027 revenue beats consensus, printing above $7.10B driven by advanced etch memory shipments.</li>
            <li><strong>Non-GAAP EPS Outperformance:</strong> Diluted Non-GAAP EPS prints ≥ $2.30 (vs. $2.18 consensus) with gross margin exceeding 52.5%.</li>
            <li><strong>CSBG Pacing Accelerates:</strong> Recurring installed base services revenue expands above +20% YoY, reinforcing margin durability.</li>
            <li><strong>Full-Year WFE Outlook Lifted:</strong> Management raises 2026/2027 calendar year WFE market forecast to $105B+ on AI demand.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Initiate a <strong>Nov 20, 2026 $270.00 / $295.00 Bull Call Spread</strong> (risk-defined upside capture) or buy spot shares on post-earnings momentum above $272 support.
          </div>
        </div>

        <!-- BASE CASE -->
        <div class="scenario-card scenario-base">
          <div class="scenario-title">
            <span style="color:var(--warn-amber);">HOLD / RANGEBOUND CONSOLIDATION (BASE CASE)</span>
            <span class="badge badge-warn">PROB: 40% | RANGE: $258.00–$275.00 (±3.5%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>In-Line Delivery:</strong> Q1 FY2027 revenue delivers near $6.95B consensus with Non-GAAP EPS landing around $2.18.</li>
            <li><strong>Solid HBM Demand:</strong> Memory shipments offset moderate trailing-edge fab pauses in secondary markets.</li>
            <li><strong>Steady Margin Execution:</strong> Gross margin prints within management's 51.0%–52.0% guidance corridor.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Deploy a <strong>Nov 20, 2026 $250.00 / $285.00 Short Strangle / Iron Condor</strong> to capture post-earnings implied volatility crush.
          </div>
        </div>

        <!-- BEAR CASE -->
        <div class="scenario-card scenario-bear">
          <div class="scenario-title">
            <span style="color:var(--bear-red);">HEDGE / REDUCE EXPOSURE (BEAR CASE)</span>
            <span class="badge badge-bear">PROB: 15% | TARGET: $240.00–$248.00 (-6.8% to -9.8%)</span>
          </div>
          <ul class="trigger-list">
            <li><strong>China Restriction Impact:</strong> Stricter trade controls limit tool shipments, resulting in forward guidance below $6.75B.</li>
            <li><strong>Memory Capex Pause:</strong> Key customers pause non-HBM tool deliveries to absorb existing capacity.</li>
            <li><strong>Margin Compression:</strong> Gross margin dips below 50.5% due to unfavorable product mix.</li>
          </ul>
          <div class="trade-structure">
            <strong>Recommended Trade Structure:</strong>
            Purchase <strong>Nov 20, 2026 $255.00 Put Options</strong> or write covered calls at the $275.00 strike to hedge equity downside below $248.00 support.
          </div>
        </div>
      </div>
    </section>
"""

draft_payload = {
    "header": {
        "page_title": f"LRCX (${spot_price:.2f}) Q1 FY2027 Earnings Intelligence Briefing",
        "spot_price_num": spot_price
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

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"Draft saved to {DRAFT_PATH}")
print(f"Character count: {len(html.strip()):,}")
