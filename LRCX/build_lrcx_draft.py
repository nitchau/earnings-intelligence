import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "LRCX_2026-10-21_truth.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "LRCX_2026-10-21_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 272.20
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1000.0, 1) # 340.6
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1000.0, 1) # 328.8
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 47.26
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 23.14
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 14.66
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 38.05
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 2.07

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 7.86
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"]) # 21.40
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 0.67
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"]) # 83.85

# 5-Quarter Data Points
# Q2 2025, Q3 2025, Q4 2025, Q1 2026, Q2 2026 (ended Jun 30, 2026)
quarters = ["Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026 (Actual)", "Q3 2026E (Est)"]
total_rev = [5171.39, 5324.17, 5344.79, 5841.49, 6722.24, 6950.0]
systems_rev = [3437.62, 3450.17, 3460.00, 3730.58, 4249.85, 4420.0]
csbg_rev = [1733.77, 1874.00, 1884.79, 2110.91, 2472.39, 2530.0]

gross_profit = [2589.71, 2684.88, 2651.16, 2910.53, 3478.74, 3614.0]
opex = [848.58, 855.79, 840.96, 863.51, 965.25, 985.0]
operating_income = [1741.13, 1829.09, 1810.20, 2047.02, 2513.49, 2629.0]
net_income = [1720.09, 1568.66, 1593.99, 1825.46, 2277.28, 2380.0]

ocf_5q = [2554.19, 1778.96, 1480.05, 1141.42, 1457.23, 1650.0]
capex_5q = [172.19, 185.12, 260.88, 331.60, 188.80, 210.0]
rep_fcf_5q = [2382.00, 1593.84, 1219.17, 809.82, 1268.43, 1440.0]
sbc_5q = [94.29, 97.24, 88.54, 96.62, 103.98, 110.0]
true_fcf_5q = [2287.71, 1496.60, 1130.63, 713.20, 1164.45, 1330.0]

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

bull_target = round(spot_price * (1 + opt_move_pct / 100), 2)  # 293.60
bear_target = round(spot_price * (1 - opt_move_pct / 100), 2)  # 250.80

html = f"""
    <!-- 1. HEADER BANNER -->
    <header class="header-banner">
      <div class="helper-bar">
        <span>💡 <strong>Interactive Definitions Enabled:</strong> Hover your mouse over any <span class="tip tip-bottom" title="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined term." data-tip="Plain-English definitions pop up automatically whenever you hover over any dotted-underlined financial metric or abbreviation.">dotted-underlined metric or abbreviation</span> for an instant plain-English explanation.</span>
        <span class="mono" style="font-size:11.5px;color:#93c5fd;">Last Reported Quarter: <strong>Q4 FY2026 / Q2 C2026 (Ended Jun 30, 2026)</strong> • Upcoming Release: <strong>Q1 FY2027 (Ended Sept 30, 2026)</strong></span>
      </div>

      <div class="header-top">
        <div class="ticker-identity">
          <div class="ticker-line">
            <span class="ticker-symbol">LRCX</span>
            <h1 class="company-name">Lam Research Corporation</h1>
            <span class="badge badge-bull">SEMICONDUCTOR ETCH &amp; DEPOSITION / AI MEMORY EXPANSION</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day before the official quarterly earnings release." data-tip="T-1 (Time Minus 1 Day): Indicates this analysis is prepared prior to the upcoming earnings release.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select • Technology &amp; Semiconductors • Wafer Fab Equipment (WFE), Atomic Layer Etch, High-Bandwidth Memory (HBM) &amp; Advanced 3D Packaging • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the SEC (0000707549) to track Lam Research regulatory filings.">CIK</span>: 0000707549</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+31.2% <span class="tip tip-right tip-bottom" title="Year-To-Date: Percentage price change since January 1, 2026." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of current year to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares." data-tip="Market Capitalization: Total equity value of the company calculated by share price (${spot_price:.2f}) × total diluted shares (~1,251M post stock split).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash." data-tip="Enterprise Value (EV): Market Cap ($340.6B) + Total Debt ($4.9B) - Cash &amp; Short-Term Investments ($6.7B). Reflects strong net cash balance sheet.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.1f}B / ${ev_b:.1f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Upcoming Q1 FY2027 Release Date</span>
          <span class="strip-val">Wed, Oct 21, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market hours (~4:05 PM Eastern Time).">AMC</span></span>
          <span class="kpi-sub">Official Webcast: 5:00 PM ET (2:00 PM PT)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in for the day after earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) option straddle prices. It reflects the expected 1-week percentage move post-earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market forecast of annualized stock price volatility." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Call Heavy)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q1 FY27E <span class="tip" title="Wall Street Consensus: The average forecast of equity research analysts." data-tip="Consensus Revenue: The average top-line sales forecast published by Wall Street sell-side analysts.">Consensus Revenue</span> / <span class="tip" title="Whisper Number: The unofficial expectation among institutional traders." data-tip="Whisper Number: Unofficial top-line expectations among buy-side institutional investors.">Whisper</span></span>
          <span class="strip-val">$6,950M / $7,050M</span>
          <span class="kpi-sub">Consensus Non-GAAP EPS: <strong>$2.18</strong> (vs $1.81 prior year)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="Valuation multiples based on earnings and cash flow generation." data-tip="Trailing P/E: Current share price divided by past 12 months EPS. Forward P/E: Price divided by consensus next 12 months estimated EPS.">Valuation Multiple</span> (P/E / EV)</span>
          <span class="strip-val">{trailing_pe:.1f}x Trailing / {fwd_pe:.1f}x Fwd</span>
          <span class="kpi-sub"><span class="tip" title="EV/EBITDA: Enterprise value divided by EBITDA." data-tip="EV/EBITDA: Enterprise Value divided by EBITDA. High-margin asset-light equipment business multiple.">EV/EBITDA</span>: {ev_ebitda:.1f}x | Short Float: {short_float:.2f}%</span>
        </div>
      </div>
    </header>

    <!-- 2. EXECUTIVE RADAR -->
    <section class="section">
      <div class="section-title">
        <span>1. Executive Pre-Earnings Radar — 4 Critical Focus Areas</span>
      </div>
      <div class="grid-4">
        <div class="card">
          <div class="card-title">HBM3e / HBM4 Packaging &amp; Cryo-Etch Dominance</div>
          <div class="card-body">
            Lam Research holds monopoly-like market share in cryogenic dielectric etch for Through-Silicon Via (TSV) manufacturing, essential for High-Bandwidth Memory (HBM) stacking. Memory Capex recovery across SK Hynix, Samsung, and Micron serves as a massive multi-year tailwind.
          </div>
        </div>
        <div class="card">
          <div class="card-title">Gate-All-Around (GAA) Nanosheet Node Transitions</div>
          <div class="card-body">
            Foundry and Logic leading-edge transition from FinFET to Gate-All-Around nanosheets (2nm/A16 nodes at TSMC and Intel) requires 20% to 30% more selective atomic-layer etch steps per wafer, directly increasing Lam's equipment intensity and dollar content.
          </div>
        </div>
        <div class="card">
          <div class="card-title">Installed Base Expansion (CSBG $2.47B Run-Rate)</div>
          <div class="card-body">
            Customer Support Business Group (CSBG) revenue hit record levels ($2,472M in Q2 2026), growing to 37% of total sales. High-margin spares, chamber maintenance, and upgrade kits provide sticky recurring cash flow resilient to broad macro cyclicality.
          </div>
        </div>
        <div class="card">
          <div class="card-title">Cash Flow Execution &amp; Aggressive Capital Return</div>
          <div class="card-body">
            Delivered $1,457M in Operating Cash Flow in Q2 2026 ($1,268M reported FCF, $1,164M True FCF). Lam's balance sheet boasts $6.7B in liquid assets with net cash position, financing consistent share repurchases and progressive dividend payouts.
          </div>
        </div>
      </div>
    </section>

    <!-- 3. HISTORICAL 5-QUARTER FINANCIAL TABLE -->
    <section class="section">
      <div class="section-title">
        <span>2. Historical 5-Quarter Financial Performance &amp; Segment Disclosures ($M)</span>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th style="min-width: 220px;">Financial Metric ($M)</th>
              <th>Q2 2025</th>
              <th>Q3 2025</th>
              <th>Q4 2025</th>
              <th>Q1 2026</th>
              <th>Q2 2026 (Actual)</th>
              <th style="background: rgba(59, 130, 246, 0.15); color: #93c5fd;">Q3 2026E (Consensus)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background: rgba(255, 255, 255, 0.03);">
              <td>Total Revenue ($M)</td>
              <td>$5,171</td>
              <td>$5,324</td>
              <td>$5,345</td>
              <td>$5,841</td>
              <td>$6,722</td>
              <td style="color: #60a5fa;">$6,950</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Systems Revenue (Etch &amp; Deposition Tools)</td>
              <td>$3,438</td>
              <td>$3,450</td>
              <td>$3,460</td>
              <td>$3,731</td>
              <td>$4,250</td>
              <td>$4,420</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Customer Support (CSBG Spares &amp; Services)</td>
              <td>$1,734</td>
              <td>$1,874</td>
              <td>$1,885</td>
              <td>$2,111</td>
              <td>$2,472</td>
              <td>$2,530</td>
            </tr>
            <tr>
              <td><span class="tip" title="Gross Profit: Total Revenue minus Cost of Revenue." data-tip="Gross Profit: Revenue remaining after subtracting manufacturing costs, precision components, and direct assembly labor.">Gross Profit</span> ($M)</td>
              <td>$2,590</td>
              <td>$2,685</td>
              <td>$2,651</td>
              <td>$2,911</td>
              <td>$3,479</td>
              <td>$3,614</td>
            </tr>
            <tr>
              <td>Operating Expenses ($M)</td>
              <td>$849</td>
              <td>$856</td>
              <td>$841</td>
              <td>$864</td>
              <td>$965</td>
              <td>$985</td>
            </tr>
            <tr style="font-weight: 700; color: #38bdf8;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income (EBIT): Core profitability of manufacturing wafer fabrication equipment before interest and taxes.">Operating Income</span> ($M)</td>
              <td>$1,741</td>
              <td>$1,829</td>
              <td>$1,810</td>
              <td>$2,047</td>
              <td>$2,513</td>
              <td style="color: #60a5fa;">$2,629</td>
            </tr>
            <tr>
              <td>Net Income ($M)</td>
              <td>$1,720</td>
              <td>$1,569</td>
              <td>$1,594</td>
              <td>$1,825</td>
              <td>$2,277</td>
              <td>$2,380</td>
            </tr>
            <tr>
              <td>Operating Cash Flow (<span class="tip" title="Cash flow generated from core operations." data-tip="Operating Cash Flow (OCF): Pure cash generated from equipment customer prepayments and deliveries before CapEx.">OCF</span>)</td>
              <td>$2,554</td>
              <td>$1,779</td>
              <td>$1,480</td>
              <td>$1,141</td>
              <td>$1,457</td>
              <td>$1,650</td>
            </tr>
            <tr>
              <td>Capital Expenditures (<span class="tip" title="Cash invested into cleanroom facilities and R&amp;D labs." data-tip="CapEx: Capital expenditures on cleanroom expansions, advanced prototyping labs, and manufacturing robotics.">CapEx</span>)</td>
              <td>$172</td>
              <td>$185</td>
              <td>$261</td>
              <td>$332</td>
              <td>$189</td>
              <td>$210</td>
            </tr>
            <tr style="font-weight: 700; color: #4ade80;">
              <td>Reported Free Cash Flow (<span class="tip" title="Operating cash flow minus capital expenditures." data-tip="Reported FCF: OCF minus CapEx. Key metric monitored for share buyback capacity.">FCF</span>)</td>
              <td>$2,382</td>
              <td>$1,594</td>
              <td>$1,219</td>
              <td>$810</td>
              <td>$1,268</td>
              <td>$1,440</td>
            </tr>
            <tr>
              <td>Stock-Based Compensation (<span class="tip" title="Non-cash expense compensating key engineering talent." data-tip="Stock-Based Compensation (SBC): Non-cash equity compensation to semiconductor engineers and management.">SBC</span>)</td>
              <td>$94</td>
              <td>$97</td>
              <td>$89</td>
              <td>$97</td>
              <td>$104</td>
              <td>$110</td>
            </tr>
            <tr style="font-weight: 700; color: #22c55e;">
              <td>True FCF (Reported FCF - SBC)</td>
              <td>$2,288</td>
              <td>$1,497</td>
              <td>$1,131</td>
              <td>$713</td>
              <td>$1,164</td>
              <td>$1,330</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 4. FORENSIC CASH FLOW BRIDGE -->
    <section class="section">
      <div class="section-title">
        <span>3. Forensic Cash Flow Quality &amp; Capital Allocation Bridge (Q2 2026 Actual)</span>
      </div>
      <div class="grid-2">
        <div class="card">
          <div class="card-title">Q2 2026 Free Cash Flow Bridge ($M)</div>
          <div class="card-body">
            <p style="margin-top:0;">Reconciling headline Operating Cash Flow to True Economic Cash Flow available to equity owners:</p>
            <table style="width:100%; border-collapse: collapse; margin-top: 10px;">
              <tr style="border-bottom: 1px solid var(--border-color);">
                <td style="padding: 6px 0;">Operating Cash Flow (OCF)</td>
                <td style="text-align: right; font-weight:700;">$1,457</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #f87171;">
                <td style="padding: 6px 0;">Less: Capital Expenditures (CapEx)</td>
                <td style="text-align: right; font-weight:700;">-$189</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); font-weight:700; color: #4ade80;">
                <td style="padding: 6px 0;">Reported Free Cash Flow (FCF)</td>
                <td style="text-align: right;">$1,268</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #fbbf24;">
                <td style="padding: 6px 0;">Less: Stock-Based Compensation (SBC)</td>
                <td style="text-align: right; font-weight:700;">-$104</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #94a3b8;">
                <td style="padding: 6px 0;">Less: Finance Lease Principal Repayments</td>
                <td style="text-align: right; font-weight:700;">-$0</td>
              </tr>
              <tr style="font-weight: 800; color: #22c55e;">
                <td style="padding: 8px 0;">True Economic Free Cash Flow</td>
                <td style="text-align: right; font-size: 15px;">$1,164</td>
              </tr>
            </table>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Balance Sheet Health &amp; Capital Allocation</div>
          <div class="card-body">
            <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
              <li><strong>Liquidity Fortress:</strong> Lam holds $6,715M in total cash, equivalents, and short-term investments against $4,980M in total debt, giving a net cash balance of $1.73B.</li>
              <li><strong>Working Capital Rebound:</strong> Inventory normalization across Chinese and global customer fabs drove working capital stabilization following previous export rule adjustments.</li>
              <li><strong>Share Repurchase Power:</strong> Board authorization supports continued aggressive buybacks, having retired over $950M in stock during the recent quarter.</li>
              <li><strong>Dividend Expansion:</strong> Annual dividend grew by double digits, requiring less than 25% of annual True FCF generation.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. 4-PILLAR INSTITUTIONAL SENTIMENT -->
    <section class="section">
      <div class="section-title">
        <span>4. Four-Pillar Institutional Sentiment Scorecard</span>
      </div>
      <div class="grid-4">
        <div class="card">
          <div class="card-title">1. Wall Street Sell-Side (Bullish Bias)</div>
          <div class="card-body">
            Consensus price target of $295.00 reflects high conviction that memory WFE spend is inflecting upwards in FY2027 led by HBM3e/HBM4 packaging buildouts at SK Hynix, Micron, and Samsung.
          </div>
        </div>
        <div class="card">
          <div class="card-title">2. Buy-Side Hedge Funds (High Conviction)</div>
          <div class="card-body">
            Long-only funds consider Lam Research the premier pure-play beneficiary of 3D memory scaling and GAA etch complexity. Very low short interest (2.07%) highlights institutional backing.
          </div>
        </div>
        <div class="card">
          <div class="card-title">3. Options Market Positioning (±7.86%)</div>
          <div class="card-body">
            ATM straddles price in an expected 1-week move of ±$21.40 (±7.86%). 30-day IV is elevated at 83.85%, reflecting traders positioning for a volatile guidance update on China export controls.
          </div>
        </div>
        <div class="card">
          <div class="card-title">4. Retail &amp; Social Sentiment (Enthusiastic)</div>
          <div class="card-body">
            Retail interest has climbed rapidly post stock-split. Discussion on financial forums is heavily focused on AI server memory shortages and Lam's critical etch monopoly.
          </div>
        </div>
      </div>
    </section>

    <!-- 6. PORTFOLIO MANAGER TRADE MATRIX -->
    <section class="section">
      <div class="section-title">
        <span>5. Portfolio Manager Pre-Earnings Action Matrix</span>
      </div>
      <div class="grid-2">
        <div class="card" style="border-left: 4px solid #22c55e;">
          <div class="card-title" style="color: #4ade80;">Bull Case Scenario (Price Target: &gt; ${bull_target})</div>
          <div class="card-body">
            <strong>Triggers:</strong> Q1 FY27 revenue guidance exceeds $7.1B, gross margin expands above 49.5%, HBM etch equipment demand accelerates, and management confirms robust China domestic demand resilience.<br><br>
            <strong>Tactical Play:</strong> Long Oct 23 $275 / $295 bull call vertical spread or pre-earnings long stock with stop-loss at 20-day moving average ($262).
          </div>
        </div>
        <div class="card" style="border-left: 4px solid #ef4444;">
          <div class="card-title" style="color: #f87171;">Bear Case Scenario (Price Target: &lt; ${bear_target})</div>
          <div class="card-body">
            <strong>Triggers:</strong> Stricter U.S. export licensing restrictions on mature node China sales, delayed customer fab tool installations in Europe/US, or gross margins compressing below 47%.<br><br>
            <strong>Tactical Play:</strong> Oct 23 $265 / $245 bear put vertical spread or harvest high implied volatility (83.85% IV) via out-of-the-money call credit spreads above $300.
          </div>
        </div>
      </div>
    </section>
"""

draft_payload = {
    "header": {
        "page_title": "LRCX — Institutional Pre-Earnings Tearsheet (Q1 FY27)",
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
    "rendered_container_html": html
}

DRAFT_PATH.write_text(json.dumps(draft_payload, indent=2), encoding="utf-8")
print(f"Successfully generated LRCX draft at {DRAFT_PATH}")
