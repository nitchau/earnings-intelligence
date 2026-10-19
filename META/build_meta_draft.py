import json
from pathlib import Path

BASE_DIR = Path("c:/Users/nitin/.earningreport")
TRUTH_PATH = BASE_DIR / "ground_truth" / "META_2026-10-21_truth.json"
DRAFT_DIR = BASE_DIR / "drafts"
DRAFT_DIR.mkdir(exist_ok=True)
DRAFT_PATH = DRAFT_DIR / "META_2026-10-21_draft.json"

truth = json.loads(TRUTH_PATH.read_text(encoding="utf-8"))

spot_price = float(truth["price_validation"]["yahoo_spot_price"]) # 705.44
mkt_cap_b = round(truth["valuation_and_market"]["market_cap_millions"] / 1000.0, 1) # 1797.1
ev_b = round(truth["valuation_and_market"]["enterprise_value_millions"] / 1000.0, 1) # 1829.1
trailing_pe = float(truth["valuation_and_market"]["trailing_pe"]) # 26.58
fwd_pe = float(truth["valuation_and_market"]["forward_pe"]) # 20.37
ps_ttm = float(truth["valuation_and_market"]["price_to_sales_ttm"]) # 7.87
ev_ebitda = float(truth["valuation_and_market"]["ev_to_ebitda"]) # 16.68
short_float = float(truth["valuation_and_market"]["short_percent_of_float"]) # 1.52

opt_move_pct = float(truth["options_positioning"]["atm_implied_move_pct"]) # 6.92
opt_move_usd = float(truth["options_positioning"]["atm_straddle_usd"]) # 48.85
pcr_oi = float(truth["options_positioning"]["put_call_oi_ratio"]) # 0.94
iv_pct = float(truth["options_positioning"]["atm_implied_volatility_pct"]) # 74.19

# 5-Quarter Data Points
# Q2 2025, Q3 2025, Q4 2025, Q1 2026, Q2 2026
quarters = ["Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026 (Actual)", "Q3 2026E (Est)"]
total_rev = [47516.0, 51242.0, 59893.0, 56311.0, 60801.0, 62450.0]
foa_adv_rev = [46563.0, 50350.0, 58400.0, 55024.0, 59363.0, 60800.0]
foa_other_rev = [583.0, 620.0, 800.0, 884.0, 1007.0, 1150.0]
reality_labs_rev = [370.0, 272.0, 693.0, 403.0, 431.0, 500.0]

gross_profit = [39025.0, 42036.0, 48987.0, 46093.0, 49471.0, 50900.0]
opex = [18584.0, 21501.0, 24242.0, 23221.0, 30696.0, 27500.0]
operating_income = [20441.0, 20535.0, 24745.0, 22872.0, 18775.0, 23400.0]
net_income = [18337.0, 2709.0, 22768.0, 26773.0, 15848.0, 20100.0]

ocf_5q = [25561.0, 29999.0, 36214.0, 32226.0, 31862.0, 33500.0]
capex_5q = [16538.0, 18829.0, 21383.0, 18997.0, 30116.0, 22500.0]
rep_fcf_5q = [9023.0, 11170.0, 14831.0, 13229.0, 1746.0, 11000.0]
sbc_5q = [4834.0, 5556.0, 5890.0, 6032.0, 7658.0, 6500.0]
true_fcf_5q = [4189.0, 5614.0, 8941.0, 7197.0, -5912.0, 4500.0]

historical_table_5q_nums = [
    {"gross_profit": gross_profit[i], "operating_expenses": opex[i], "operating_income": operating_income[i]}
    for i in range(5)
]

fcf_bridge_q0 = {
    "ocf": 31862.0,
    "capex": 30116.0,
    "reported_fcf": 1746.0,
    "sbc": 7658.0,
    "finance_leases": 0.0,
    "true_fcf": -5912.0
}

bull_target = round(spot_price * (1 + opt_move_pct / 100), 2)  # 754.26
bear_target = round(spot_price * (1 - opt_move_pct / 100), 2)  # 656.62

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
            <span class="ticker-symbol">META</span>
            <h1 class="company-name">Meta Platforms, Inc.</h1>
            <span class="badge badge-bull">LLAMA 4 &amp; GENAI AD MONETIZATION / HYPERSCALE CAPEX EXPANSION</span>
            <span class="badge badge-blue"><span class="tip tip-bottom" title="One trading day before the official quarterly earnings release." data-tip="T-1 (Time Minus 1 Day): Indicates this analysis is prepared prior to the upcoming Q3 2026 earnings release.">T-1</span> PRE-EARNINGS BRIEFING</span>
          </div>
          <div class="sector-tag">NASDAQ Global Select • Communication Services &amp; Digital Advertising • Social Media Ecosystem, Meta AI Assistant, Ray-Ban Smart Glasses &amp; Llama Open-Source Foundation Models • <span class="tip tip-bottom" title="Central Index Key: Unique 10-digit identifier assigned by the U.S. SEC." data-tip="Central Index Key (CIK): The unique 10-digit identifier assigned by the SEC (0001326801) to track Meta's regulatory filings.">CIK</span>: 0001326801</div>
        </div>
        <div class="header-price-block">
          <div class="price-box">
            <div class="price-label">Spot Price</div>
            <div class="price-value">${spot_price:.2f} <span class="badge badge-bull">+42.6% <span class="tip tip-right tip-bottom" title="Year-To-Date: Percentage price change since January 1, 2026." data-tip="Year-To-Date (YTD): Total percentage return of the stock from January 1 of current year to today.">YTD</span></span></div>
          </div>
          <div class="price-box">
            <div class="price-label"><span class="tip tip-right tip-bottom" title="Market Capitalization: Total value of all outstanding shares." data-tip="Market Capitalization: Total equity value of the company calculated by share price (${spot_price:.2f}) × total diluted shares (~2,548M).">Market Cap</span> / <span class="tip tip-right tip-bottom" title="Enterprise Value: Market Cap plus Total Debt minus Cash." data-tip="Enterprise Value (EV): Market Cap ($1,797B) + Total Debt ($79.3B) - Cash &amp; Marketable Securities ($58.1B). Shows full takeover valuation.">EV</span></div>
            <div class="price-value">${mkt_cap_b:.1f}B / ${ev_b:.1f}B</div>
          </div>
        </div>
      </div>

      <div class="header-strip">
        <div class="strip-item">
          <span class="strip-label">Upcoming Q3 2026 Release Date</span>
          <span class="strip-val">Wed, Oct 21, 2026 • <span class="tip" title="After Market Close: Earnings are released right after the 4:00 PM ET stock market close." data-tip="After Market Close (AMC): The company releases its earnings report after regular market hours (~4:05 PM Eastern Time).">AMC</span></span>
          <span class="kpi-sub">Official Webcast: 5:00 PM ET (2:00 PM PT)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="The percentage stock move (up or down) that the options market is pricing in for the day after earnings." data-tip="Options-Implied Move: Derived from At-The-Money (ATM) option straddle prices. It reflects the expected 1-week percentage move post-earnings.">Options-Implied Move</span> (1-Wk <span class="tip" title="At-The-Money: Options with a strike price equal to the current stock price." data-tip="At-The-Money (ATM): Options contracts whose strike price is closest to current trading price (${spot_price:.2f}).">ATM</span>)</span>
          <span class="strip-val" style="color: var(--warn-amber);">±{opt_move_pct:.2f}% (±${opt_move_usd:.2f} / sh)</span>
          <span class="kpi-sub">30D <span class="tip" title="Implied Volatility: Market forecast of annualized stock price volatility." data-tip="Implied Volatility (IV): The options market's annualized volatility expectation.">IV</span>: {iv_pct:.1f}% | Put/Call OI Ratio: {pcr_oi:.2f}x (Balanced Institutional)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label">Q3 2026E <span class="tip" title="Wall Street Consensus: The average forecast of equity research analysts." data-tip="Consensus Revenue: The average top-line sales forecast published by Wall Street sell-side analysts for Q3 2026.">Consensus Revenue</span> / <span class="tip" title="Whisper Number: The unofficial expectation among institutional traders." data-tip="Whisper Number: Unofficial top-line expectations among buy-side institutional investors.">Whisper</span></span>
          <span class="strip-val">$62,450M / $63,200M</span>
          <span class="kpi-sub">Consensus Non-GAAP EPS: <strong>$5.64</strong> (vs $4.39 prior year)</span>
        </div>
        <div class="strip-item">
          <span class="strip-label"><span class="tip" title="Valuation multiples based on earnings and cash flow generation." data-tip="Trailing P/E: Current share price divided by past 12 months EPS. Forward P/E: Price divided by consensus next 12 months estimated EPS.">Valuation Multiple</span> (P/E / EV)</span>
          <span class="strip-val">{trailing_pe:.1f}x Trailing / {fwd_pe:.1f}x Fwd</span>
          <span class="kpi-sub"><span class="tip" title="EV/EBITDA: Enterprise value divided by EBITDA." data-tip="EV/EBITDA: Enterprise Value divided by EBITDA. Compares cash earnings across tech hyperscalers.">EV/EBITDA</span>: {ev_ebitda:.1f}x | Short Float: {short_float:.2f}%</span>
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
          <div class="card-title">Advantage+ AI Ad Automation &amp; Conversion Lift</div>
          <div class="card-body">
            Advantage+ creative and audience tools continue to deliver superior ROAS (Return On Ad Spend) for direct-response advertisers. Meta AI assistant integration across Instagram and WhatsApp is generating incremental high-intent ad impressions, driving +22% YoY ad revenue growth ($59.36B in Q2).
          </div>
        </div>
        <div class="card">
          <div class="card-title">Hyperscale AI CapEx Guide ($65B-$75B FY26)</div>
          <div class="card-body">
            CapEx surged to $30,116M in Q2 2026 alone as Meta expanded its custom MTIA silicon and Blackwell GPU data centers for training Llama 4. Street debate centers on whether management increases FY2026 CapEx midpoint guidance above $72B.
          </div>
        </div>
        <div class="card">
          <div class="card-title">Reality Labs Losses ($4B-$4.5B/Qtr Drag)</div>
          <div class="card-body">
            Reality Labs posted revenue of $431M in Q2 with continued operating losses of ~$4.2B. While Ray-Ban Meta smart glasses exceeded sales forecasts with strong viral adoption, Quest VR software sales remain modest against heavy AR waveguide R&amp;D investments.
          </div>
        </div>
        <div class="card">
          <div class="card-title">Forensic Cash Flow Quality &amp; True FCF Bridge</div>
          <div class="card-body">
            Meta generated $31,862M in Operating Cash Flow in Q2 2026. However, after subtracting $30,116M in CapEx and $7,658M in Stock-Based Compensation, True Economic FCF fell to -$5,912M. Capital return pacing (buybacks &amp; dividend) hinges on CapEx moderation in FY27.
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
              <td>$47,516</td>
              <td>$51,242</td>
              <td>$59,893</td>
              <td>$56,311</td>
              <td>$60,801</td>
              <td style="color: #60a5fa;">$62,450</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Family of Apps: Advertising (IG, FB)</td>
              <td>$46,563</td>
              <td>$50,350</td>
              <td>$58,400</td>
              <td>$55,024</td>
              <td>$59,363</td>
              <td>$60,800</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Family of Apps: Other (WhatsApp Enterprise)</td>
              <td>$583</td>
              <td>$620</td>
              <td>$800</td>
              <td>$884</td>
              <td>$1,007</td>
              <td>$1,150</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">• Reality Labs (Hardware, Quest &amp; Smart Glasses)</td>
              <td>$370</td>
              <td>$272</td>
              <td>$693</td>
              <td>$403</td>
              <td>$431</td>
              <td>$500</td>
            </tr>
            <tr>
              <td><span class="tip" title="Gross Profit: Total Revenue minus Cost of Revenue." data-tip="Gross Profit: Revenue remaining after subtracting data center depreciation, traffic acquisition costs, and bandwidth expenses.">Gross Profit</span> ($M)</td>
              <td>$39,025</td>
              <td>$42,036</td>
              <td>$48,987</td>
              <td>$46,093</td>
              <td>$49,471</td>
              <td>$50,900</td>
            </tr>
            <tr>
              <td>Operating Expenses ($M)</td>
              <td>$18,584</td>
              <td>$21,501</td>
              <td>$24,242</td>
              <td>$23,221</td>
              <td>$30,696</td>
              <td>$27,500</td>
            </tr>
            <tr style="font-weight: 700; color: #38bdf8;">
              <td><span class="tip" title="Operating Income (EBIT): Gross profit minus operating expenses." data-tip="Operating Income (EBIT): Profit earned from core digital advertising and app operations before interest and taxes.">Operating Income</span> ($M)</td>
              <td>$20,441</td>
              <td>$20,535</td>
              <td>$24,745</td>
              <td>$22,872</td>
              <td>$18,775</td>
              <td style="color: #60a5fa;">$23,400</td>
            </tr>
            <tr>
              <td>Net Income ($M)</td>
              <td>$18,337</td>
              <td>$2,709</td>
              <td>$22,768</td>
              <td>$26,773</td>
              <td>$15,848</td>
              <td>$20,100</td>
            </tr>
            <tr>
              <td>Operating Cash Flow (<span class="tip" title="Cash flow generated from day-to-day app monetization." data-tip="Operating Cash Flow (OCF): Pure cash generated from advertiser billing before infrastructure reinvestment.">OCF</span>)</td>
              <td>$25,561</td>
              <td>$29,999</td>
              <td>$36,214</td>
              <td>$32,226</td>
              <td>$31,862</td>
              <td>$33,500</td>
            </tr>
            <tr>
              <td>Capital Expenditures (<span class="tip" title="Cash spent on hyperscale servers, GPUs, and network infrastructure." data-tip="CapEx: Capital expenditures on custom AI silicon (MTIA), NVIDIA GPUs, and custom AI data center clusters.">CapEx</span>)</td>
              <td>$16,538</td>
              <td>$18,829</td>
              <td>$21,383</td>
              <td>$18,997</td>
              <td>$30,116</td>
              <td>$22,500</td>
            </tr>
            <tr style="font-weight: 700; color: #4ade80;">
              <td>Reported Free Cash Flow (<span class="tip" title="Operating cash flow minus capital expenditures." data-tip="Reported FCF: OCF minus CapEx. Traditional cash flow benchmark.">FCF</span>)</td>
              <td>$9,023</td>
              <td>$11,170</td>
              <td>$14,831</td>
              <td>$13,229</td>
              <td>$1,746</td>
              <td>$11,000</td>
            </tr>
            <tr>
              <td>Stock-Based Compensation (<span class="tip" title="Non-cash compensation expense to retain top AI research talent." data-tip="Stock-Based Compensation (SBC): Equity grants to AI researchers and developers adding back to OCF but diluting shareholders.">SBC</span>)</td>
              <td>$4,834</td>
              <td>$5,556</td>
              <td>$5,890</td>
              <td>$6,032</td>
              <td>$7,658</td>
              <td>$6,500</td>
            </tr>
            <tr style="font-weight: 700; color: #22c55e;">
              <td>True FCF (Reported FCF - SBC)</td>
              <td>$4,189</td>
              <td>$5,614</td>
              <td>$8,941</td>
              <td>$7,197</td>
              <td>-$5,912</td>
              <td>$4,500</td>
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
                <td style="text-align: right; font-weight:700;">$31,862</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #f87171;">
                <td style="padding: 6px 0;">Less: Capital Expenditures (CapEx)</td>
                <td style="text-align: right; font-weight:700;">-$30,116</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); font-weight:700; color: #4ade80;">
                <td style="padding: 6px 0;">Reported Free Cash Flow (FCF)</td>
                <td style="text-align: right;">$1,746</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #fbbf24;">
                <td style="padding: 6px 0;">Less: Stock-Based Compensation (SBC)</td>
                <td style="text-align: right; font-weight:700;">-$7,658</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-color); color: #94a3b8;">
                <td style="padding: 6px 0;">Less: Finance Lease Principal Repayments</td>
                <td style="text-align: right; font-weight:700;">-$0</td>
              </tr>
              <tr style="font-weight: 800; color: #ef4444;">
                <td style="padding: 8px 0;">True Economic Free Cash Flow</td>
                <td style="text-align: right; font-size: 15px;">-$5,912</td>
              </tr>
            </table>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Balance Sheet Health &amp; Capital Allocation</div>
          <div class="card-body">
            <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
              <li><strong>Liquidity Fortress:</strong> Meta holds $58,137M in cash, cash equivalents, and marketable securities, providing abundant cushion during peak AI GPU cluster procurement.</li>
              <li><strong>Debt Profile:</strong> Long-term debt stands at $68,495M against minimal short-term obligations, with average bond maturities extending past 2035 at low fixed interest coupons.</li>
              <li><strong>Share Buybacks &amp; Dividends:</strong> Quarterly cash dividend of $0.50 per share ($1.27B/quarter) remains safely funded from trailing 12-month OCF ($130B+).</li>
              <li><strong>CapEx Intensity Inflection:</strong> Q2 CapEx absorption was extraordinary at 49.5% of total revenue. Any commentary indicating CapEx plateauing in FY27 will trigger severe multiple expansion.</li>
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
          <div class="card-title">1. Wall Street Sell-Side (Strong Bull)</div>
          <div class="card-body">
            Consensus price target of $760.00 reflects overwhelming optimism regarding Meta's open-source Llama 4 dominance, Advantage+ ad pricing power, and rising monetization per daily active user.
          </div>
        </div>
        <div class="card">
          <div class="card-title">2. Buy-Side Hedge Funds (Growth Accumulation)</div>
          <div class="card-body">
            Hedge funds maintain core overweight positioning. Low short interest of 1.52% indicates institutional investors view Meta as the premier consumer AI monetization engine.
          </div>
        </div>
        <div class="card">
          <div class="card-title">3. Options Market Positioning (±6.92%)</div>
          <div class="card-body">
            ATM straddles price in an implied move of ±$48.85 (±6.92%). 30-day IV is 74.19% with open interest heavily clustered at the $750 call and $660 put strikes.
          </div>
        </div>
        <div class="card">
          <div class="card-title">4. Retail &amp; Social Sentiment (Euphoric)</div>
          <div class="card-body">
            Retail sentiment is highly bullish, driven by the viral success of Ray-Ban Meta smart glasses and Meta AI chatbot integration across Instagram and WhatsApp.
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
            <strong>Triggers:</strong> Q3 revenue exceeds $63.2B, Q4 top-line guidance accelerates above 22% YoY, Family of Apps ad impressions grow double digits, and management signals FY27 CapEx discipline.<br><br>
            <strong>Tactical Play:</strong> Long Oct 23 $710 / $755 bull call vertical spread or pre-earnings equity position with trailing stop set at $685.
          </div>
        </div>
        <div class="card" style="border-left: 4px solid #ef4444;">
          <div class="card-title" style="color: #f87171;">Bear Case Scenario (Price Target: &lt; ${bear_target})</div>
          <div class="card-body">
            <strong>Triggers:</strong> FY2026 CapEx guide raised to &gt;$75B without proportional ad conversion gains, Reality Labs losses widen beyond $5B/quarter, or regulatory antitrust remedies force European ad subscription modifications.<br><br>
            <strong>Tactical Play:</strong> Oct 23 $690 / $650 bear put vertical spread or harvest high 74% IV via selling out-of-the-money call credit spreads above $765.
          </div>
        </div>
      </div>
    </section>
"""

draft_payload = {
    "header": {
        "page_title": "META — Institutional Pre-Earnings Tearsheet (Q3 2026)",
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
print(f"Successfully generated META draft at {DRAFT_PATH}")
