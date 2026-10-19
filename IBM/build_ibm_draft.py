import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "IBM_2026-10-21_truth.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "IBM_2026-10-21_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 236.39
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1000.0, 1) # 222.7
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1000.0, 1) # 275.9
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 21.01
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 17.98
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 3.22
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 16.75
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 2.85

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 6.90
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"]) # 16.30
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 0.60
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"]) # 75.03

# 5-Quarter Data Points
# Q2 2025, Q3 2025, Q4 2025, Q1 2026, Q2 2026
quarters = ["Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026 (Actual)", "Q3 2026E (Est)"]
total_rev = [16977.0, 16331.0, 19687.0, 15917.0, 17162.0, 17550.0]
software_rev = [7387.0, 7209.0, 9036.0, 7052.0, 7761.0, 7920.0]
consulting_rev = [5314.0, 5324.0, 5310.0, 5272.0, 5327.0, 5380.0]
infrastructure_rev = [4142.0, 3559.0, 5116.0, 3326.0, 3835.0, 3980.0]
financing_rev = [134.0, 239.0, 225.0, 267.0, 239.0, 270.0]

gross_profit = [9977.0, 9360.0, 11928.0, 8950.0, 9907.0, 10180.0]
opex = [6891.0, 6568.0, 7079.0, 6731.0, 7062.0, 7150.0]
operating_income = [3086.0, 2792.0, 4849.0, 2219.0, 2845.0, 3030.0]
net_income = [2194.0, 1744.0, 5600.0, 1216.0, 2165.0, 2480.0]

ocf_5q = [1701.0, 3082.0, 4040.0, 5169.0, 2597.0, 2850.0]
capex_5q = [373.0, 417.0, 553.0, 391.0, 383.0, 400.0]
rep_fcf_5q = [1328.0, 2665.0, 3487.0, 4778.0, 2214.0, 2450.0]
sbc_5q = [441.0, 443.0, 430.0, 506.0, 498.0, 510.0]
true_fcf_5q = [887.0, 2222.0, 3057.0, 4272.0, 1716.0, 1940.0]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": operating_income[i]}
    for i in range(5)
]

fcf_bridge_q0 = {
    "ocf": 2597.0,
    "capex": 383.0,
    "reported_fcf": 2214.0,
    "sbc": 498.0,
    "finance_leases": 0.0,
    "true_fcf": 1716.0
}

bull_target = round(spot_price * (1 + opt_move_pct / 100), 2)  # 252.70
bear_target = round(spot_price * (1 - opt_move_pct / 100), 2)  # 220.08

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
            <span class="ticker-symbol">IBM</span>
            <h1 class="company-name">International Business Machines Corporation</h1>
            <span class="badge badge-bull">HYBRID CLOUD &amp; WATSONX ENTERPRISE AI ACCELERATION</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day before the official quarterly earnings release." data-tip="T-1 (Time Minus 1 Day): Indicates this analysis is prepared prior to the upcoming Q3 2026 earnings release.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NYSE • Technology &amp; Enterprise Software • Hybrid Cloud, Red Hat, Watsonx GenAI &amp; Mission-Critical Infrastructure • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the SEC (0000051143) to track IBM's official regulatory filings.">CIK</span>: 0000051143</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+22.8% <span class="tip tip-right tip-bottom" title="Year-To-Date: Percentage price change since January 1, 2026." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of current year to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares." data-tip="Market Capitalization: Total equity value of the company calculated by share price (${spot_price:.2f}) × total diluted shares (~942M).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash." data-tip="Enterprise Value (EV): Market Cap ($222.7B) + Total Debt ($65.3B) - Cash &amp; Short-Term Investments ($11.8B). Shows total takeover cost.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.1f}B / ${ev_b:.1f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Upcoming Q3 2026 Release Date</span>
          <span class="strip-val">Wed, Oct 21, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market hours (~4:10 PM Eastern Time).">AMC</span></span>
          <span class="kpi-sub">Official Webcast: 5:00 PM ET (2:00 PM PT)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in for the day after earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) option straddle prices. It reflects the expected 1-week percentage move post-earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market forecast of annualized stock price volatility." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Call Heavy)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E <span class="tip" title="Wall Street Consensus: The average forecast of equity research analysts." data-tip="Consensus Revenue: The average top-line sales forecast published by Wall Street sell-side analysts for Q3 2026.">Consensus Revenue</span> / <span class="tip" title="Whisper Number: The unofficial expectation among institutional traders." data-tip="Whisper Number: Unofficial top-line expectations among buy-side institutional investors.">Whisper</span></span>
          <span class="strip-val">$17,550M / $17,680M</span>
          <span class="kpi-sub">Consensus Non-GAAP EPS: <strong>$2.87</strong> (vs $2.30 prior year)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="Valuation multiples based on earnings and cash flow generation." data-tip="Trailing P/E: Current share price divided by past 12 months EPS. Forward P/E: Price divided by consensus next 12 months estimated EPS.">Valuation Multiple</span> (P/E / EV)</span>
          <span class="strip-val">{trailing_pe:.1f}x Trailing / {fwd_pe:.1f}x Fwd</span>
          <span class="kpi-sub"><span class="tip" title="EV/EBITDA: Enterprise value divided by earnings before interest, tax, depreciation, and amortization." data-tip="EV/EBITDA: Enterprise Value divided by EBITDA. Useful for comparing asset-heavy and leveraged balance sheets.">EV/EBITDA</span>: {ev_ebitda:.1f}x | Short Float: {short_float:.2f}%</span>
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
          <div class="card-title">watsonx &amp; GenAI Book of Business ($12.5B+ Inception)</div>
          <div class="card-body">
            Enterprise Generative AI book of business doubled year-over-year to surpass $12.5B across software and consulting. Investors are scrutinizing conversion velocity from initial enterprise pilots to long-term recurring Red Hat OpenShift and watsonx runtime contracts.
          </div>
        </div>
        <div class="card">
          <div class="card-title">Software Margin Expansion &amp; Red Hat Acceleration</div>
          <div class="card-body">
            Software represents IBM's highest-margin profit engine (gross margins above 75%). Red Hat annual recurring revenue expansion and Automation (Apptio &amp; HashiCorp integration) are the central pillars offsetting traditional cyclical client tech budgets.
          </div>
        </div>
        <div class="card">
          <div class="card-title">Consulting Reprioritization vs Discretionary Pause</div>
          <div class="card-body">
            Consulting revenue growth stabilized around +3% YoY. Clients continue to pause long-tail discretionary advisory projects to aggressively reallocate budget toward generative AI architecture and cloud modernization implementations.
          </div>
        </div>
        <div class="card">
          <div class="card-title">Free Cash Flow Durability &amp; Dividend Fortress</div>
          <div class="card-body">
            IBM delivered $2,597M in Operating Cash Flow in Q2 2026, generating $2,214M in reported FCF ($1,716M True FCF net of SBC). Management's FY2026 FCF guidance target of $12.5B+ supports both aggressive M&amp;A integration and reliable dividend payments ($1.59B/quarter).
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
              <td>$16,977</td>
              <td>$16,331</td>
              <td>$19,687</td>
              <td>$15,917</td>
              <td>$17,162</td>
              <td style="color: #60a5fa;">$17,550</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Software (Red Hat, Data, Automation)</td>
              <td>$7,387</td>
              <td>$7,209</td>
              <td>$9,036</td>
              <td>$7,052</td>
              <td>$7,761</td>
              <td>$7,920</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Consulting (Strategy, Tech, Operations)</td>
              <td>$5,314</td>
              <td>$5,324</td>
              <td>$5,310</td>
              <td>$5,272</td>
              <td>$5,327</td>
              <td>$5,380</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Infrastructure (IBM Z, Hybrid Infra)</td>
              <td>$4,142</td>
              <td>$3,559</td>
              <td>$5,116</td>
              <td>$3,326</td>
              <td>$3,835</td>
              <td>$3,980</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Financing &amp; Other Items</td>
              <td>$134</td>
              <td>$239</td>
              <td>$225</td>
              <td>$267</td>
              <td>$239</td>
              <td>$270</td>
            </tr>
            <tr>
              <td><span class="tip" title="Gross Profit: Total Revenue minus Cost of Revenue." data-tip="Gross Profit: Revenue remaining after subtracting direct cost of delivering software licenses, infrastructure hardware, and consulting labor.">Gross Profit</span> ($M)</td>
              <td>$9,977</td>
              <td>$9,360</td>
              <td>$11,928</td>
              <td>$8,950</td>
              <td>$9,907</td>
              <td>$10,180</td>
            </tr>
            <tr>
              <td>Operating Expenses ($M)</td>
              <td>$6,891</td>
              <td>$6,568</td>
              <td>$7,079</td>
              <td>$6,731</td>
              <td>$7,062</td>
              <td>$7,150</td>
            </tr>
            <tr style="font-weight: 700; color: #38bdf8;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income (EBIT): Profit realized from core business operations before deducting interest charges and tax expenses.">Operating Income</span> ($M)</td>
              <td>$3,086</td>
              <td>$2,792</td>
              <td>$4,849</td>
              <td>$2,219</td>
              <td>$2,845</td>
              <td style="color: #60a5fa;">$3,030</td>
            </tr>
            <tr>
              <td>Net Income ($M)</td>
              <td>$2,194</td>
              <td>$1,744</td>
              <td>$5,600</td>
              <td>$1,216</td>
              <td>$2,165</td>
              <td>$2,480</td>
            </tr>
            <tr>
              <td>Operating Cash Flow (<span class="tip" title="Cash flow generated from day-to-day operational activities." data-tip="Operating Cash Flow (OCF): Pure cash generated from delivering products and services before capital reinvestment.">OCF</span>)</td>
              <td>$1,701</td>
              <td>$3,082</td>
              <td>$4,040</td>
              <td>$5,169</td>
              <td>$2,597</td>
              <td>$2,850</td>
            </tr>
            <tr>
              <td>Capital Expenditures (<span class="tip" title="Cash invested in purchasing physical equipment and software assets." data-tip="CapEx: Capital expenditures on software, tooling, and property, plant &amp; equipment.">CapEx</span>)</td>
              <td>$373</td>
              <td>$417</td>
              <td>$553</td>
              <td>$391</td>
              <td>$383</td>
              <td>$400</td>
            </tr>
            <tr style="font-weight: 700; color: #4ade80;">
              <td>Reported Free Cash Flow (<span class="tip" title="Operating cash flow minus capital expenditures." data-tip="Reported FCF: OCF minus CapEx. Key metric monitored by management for dividend coverage.">FCF</span>)</td>
              <td>$1,328</td>
              <td>$2,665</td>
              <td>$3,487</td>
              <td>$4,778</td>
              <td>$2,214</td>
              <td>$2,450</td>
            </tr>
            <tr>
              <td>Stock-Based Compensation (<span class="tip" title="Non-cash expense compensating employees with stock grants." data-tip="Stock-Based Compensation (SBC): Non-cash compensation expense adding back to OCF but diluting equity holders.">SBC</span>)</td>
              <td>$441</td>
              <td>$443</td>
              <td>$430</td>
              <td>$506</td>
              <td>$498</td>
              <td>$510</td>
            </tr>
            <tr style="font-weight: 700; color: #22c55e;">
              <td>True FCF (Reported FCF - SBC)</td>
              <td>$887</td>
              <td>$2,222</td>
              <td>$3,057</td>
              <td>$4,272</td>
              <td>$1,716</td>
              <td>$1,940</td>
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
                <td style="text-align: right; font-weight:700;">$2,597</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #f87171;">
                <td style="padding: 6px 0;">Less: Capital Expenditures (CapEx)</td>
                <td style="text-align: right; font-weight:700;">-$383</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); font-weight:700; color: #4ade80;">
                <td style="padding: 6px 0;">Reported Free Cash Flow (FCF)</td>
                <td style="text-align: right;">$2,214</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #fbbf24;">
                <td style="padding: 6px 0;">Less: Stock-Based Compensation (SBC)</td>
                <td style="text-align: right; font-weight:700;">-$498</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #94a3b8;">
                <td style="padding: 6px 0;">Less: Finance Lease Principal Repayments</td>
                <td style="text-align: right; font-weight:700;">-$0</td>
              </tr>
              <tr style="font-weight: 800; color: #22c55e;">
                <td style="padding: 8px 0;">True Economic Free Cash Flow</td>
                <td style="text-align: right; font-size: 15px;">$1,716</td>
              </tr>
            </table>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Balance Sheet Health &amp; Capital Allocation</div>
          <div class="card-body">
            <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
              <li><strong>Cash &amp; Liquidity:</strong> IBM closed Q2 2026 with $11,783M in total cash, cash equivalents, and marketable securities ($7,217M in pure cash and cash equivalents).</li>
              <li><strong>Total Debt Position:</strong> Total debt stands at $65,272M ($58,727M long-term, $6,545M short-term), generating Net Debt of $53,489M.</li>
              <li><strong>Deleveraging Track Record:</strong> Core IBM operations consistently prioritize debt reduction following major acquisitions, retiring over $4,213M of debt in Q2 2026 alone.</li>
              <li><strong>Shareholder Returns:</strong> Paid $1,590M in quarterly cash dividends in Q2 2026. The 5-quarter True FCF generation of $12.16B provides 1.5x coverage over regular dividend disbursements.</li>
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
          <div class="card-title">1. Wall Street Sell-Side (Moderate Bull)</div>
          <div class="card-body">
            Consensus price target of $248.00 reflects multiple expansion following Red Hat strength and enterprise AI adoption. Analysts focus heavily on whether Consulting bookings reaccelerate in H2.
          </div>
        </div>
        <div class="card">
          <div class="card-title">2. Buy-Side Hedge Funds (Accumulation)</div>
          <div class="card-body">
            Institutions favor IBM as a high-free-cash-flow enterprise AI defensive compounder. Low short interest (2.85%) and 0.60x Put/Call ratio signal minimal aggressive downside speculation.
          </div>
        </div>
        <div class="card">
          <div class="card-title">3. Options Market Positioning (±6.90%)</div>
          <div class="card-body">
            ATM straddles price in an implied move of ±$16.30 (±6.90%). 30-day IV sits at 75.03% heading into Wednesday's close. Heavy open interest at the $250 call and $220 put strikes.
          </div>
        </div>
        <div class="card">
          <div class="card-title">4. Retail &amp; Social Sentiment (Constructive)</div>
          <div class="card-body">
            Retail interest has climbed steadily alongside IBM's multi-year share price breakout. Positive discussion centers around watsonx commercial partnerships with AWS, Microsoft Azure, and SAP.
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
            <strong>Triggers:</strong> watsonx GenAI book of business beats expectations (&gt;$13.5B), Red Hat growth accelerates back to double digits (&gt;12%), Consulting bookings inflect positively, and FY2026 FCF guidance is reaffirmed at &gt;$13B.<br><br>
            <strong>Tactical Play:</strong> Long Oct 23 $240 / $255 bull call vertical spread or pre-earnings long equity accumulation with trailing stop at 50-day moving average ($225).
          </div>
        </div>
        <div class="card" style="border-left: 4px solid #ef4444;">
          <div class="card-title" style="color: #f87171;">Bear Case Scenario (Price Target: &lt; ${bear_target})</div>
          <div class="card-body">
            <strong>Triggers:</strong> Consulting revenue turns negative YoY due to client budget freezes, Software growth slows below 5%, or integration costs from recent software acquisitions compress operating margins below 16%.<br><br>
            <strong>Tactical Play:</strong> Defined-risk Oct 23 $230 / $215 put spread or sell out-of-the-money call credit spreads above the 1-standard-deviation implied move ($255 strike).
          </div>
        </div>
      </div>
    </section>
"""

draft_payload = {
    "header": {
        "page_title": "IBM — Institutional Pre-Earnings Tearsheet (Q3 2026)",
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
print(f"Successfully generated IBM draft at {DRAFT_PATH}")
