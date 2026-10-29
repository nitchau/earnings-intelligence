import re

for ticker in ["GOOGL", "GOOG"]:
    path = f"{ticker}/build_{ticker.lower()}_post_draft.py"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Update KPI card 4
    old_kpi4 = re.search(r'<div class="kpi-card">\s*<div class="kpi-title"><span class="tip"[^>]*>Quarterly Cash Flow.*?</div>\s*</div>', text, re.DOTALL)
    if old_kpi4:
        new_kpi4 = '''<div class="kpi-card">
        <div class="kpi-title"><span class="tip" title="Operating Cash Flow: Total cash generated from operations." data-tip="Operating Cash Flow: $42,290M generated in Q3 2026.">Quarterly Cash Flow</span></div>
        <div class="kpi-value">$42.29B</div>
        <div class="kpi-sub">$42,290M Operating Cash Flow • -$17,695M True Free Cash Flow</div>
      </div>'''
        text = text[:old_kpi4.start()] + new_kpi4 + text[old_kpi4.end():]
        print(f"[{ticker}] Updated KPI card 4")

    # 2. Update CapEx mention in thesis audit banner
    text = re.sub(
        r'CapEx surged to \$24B',
        'CapEx surged to $51.4B on aggressive technical AI infrastructure',
        text
    )

    # 3. Update 5Q Table (from <div class="table-wrapper"> under #sec-5q to </table>)
    old_table = re.search(r'<section class="section" id="sec-5q".*?<div class="table-wrapper">\s*<table>.*?</table>\s*</div>', text, re.DOTALL)
    if old_table:
        new_table_content = '''<section class="section" id="sec-5q" style="margin-bottom: 26px;">
      <h2 style="font-size: 16px; font-weight: 800; color: #f1f5f9; margin-bottom: 12px; letter-spacing: 0.02em;">
        2. Rolling 5-Quarter Financials &amp; Segment Breakdown (Q3 2026 Actual Delivery)
      </h2>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Metric / Segment (USD Millions)</th>
              <th>Q3 2025</th>
              <th>Q4 2025</th>
              <th>Q1 2026</th>
              <th>Q2 2026</th>
              <th class="col-q0">Q3 2026 (Actual)</th>
              <th class="col-est">Q4 2026E (Guided / Street)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="font-weight: 700; background: rgba(59, 130, 246, 0.06);">
              <td><span class="tip" title="Recognized gross revenue across Alphabet." data-tip="Total Alphabet Revenue: $127,577.0M gross consolidated revenue (+25% YoY).">Total Consolidated Revenues ($M)</span></td>
              <td>${s5q["total_revenue"][0]:,.1f}M</td>
              <td>${s5q["total_revenue"][1]:,.1f}M</td>
              <td>${s5q["total_revenue"][2]:,.1f}M</td>
              <td>${s5q["total_revenue"][3]:,.1f}M</td>
              <td class="col-q0" style="font-weight:800; color:#34d399;">${s5q["total_revenue"][4]:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color:#60a5fa;">$130,000.0M</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">↳ Google Services (Search, YouTube, Ads)</td>
              <td>$87,052.0M</td>
              <td>$95,000.0M</td>
              <td>$91,000.0M</td>
              <td>$98,500.0M</td>
              <td class="col-q0">$96,302.0M</td>
              <td class="col-est">$102,000.0M</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">↳ Google Cloud (GCP + Workspace)</td>
              <td>$15,157.0M</td>
              <td>$18,500.0M</td>
              <td>$18,500.0M</td>
              <td>$21,000.0M</td>
              <td class="col-q0">$30,700.0M</td>
              <td class="col-est">$27,500.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Total cost of revenues including TAC and data center operational costs." data-tip="Cost of Revenues: $51,419.0M in Q3 2026.">Cost of Revenues</span></td>
              <td>${s5q["total_revenue"][0] - s5q["gross_profit"][0]:,.1f}M</td>
              <td>${s5q["total_revenue"][1] - s5q["gross_profit"][1]:,.1f}M</td>
              <td>${s5q["total_revenue"][2] - s5q["gross_profit"][2]:,.1f}M</td>
              <td>${s5q["total_revenue"][3] - s5q["gross_profit"][3]:,.1f}M</td>
              <td class="col-q0">${s5q["total_revenue"][4] - s5q["gross_profit"][4]:,.1f}M</td>
              <td class="col-est">$52,000.0M</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Gross Profit: Revenue minus cost of revenues." data-tip="Gross Profit: $76,158.0M in Q3 2026.">Total Gross Profit</span></td>
              <td>${s5q["gross_profit"][0]:,.1f}M</td>
              <td>${s5q["gross_profit"][1]:,.1f}M</td>
              <td>${s5q["gross_profit"][2]:,.1f}M</td>
              <td>${s5q["gross_profit"][3]:,.1f}M</td>
              <td class="col-q0" style="color: #34d399;">${s5q["gross_profit"][4]:,.1f}M</td>
              <td class="col-est">$78,000.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Operating expenses including R&amp;D, Sales &amp; Marketing, and General &amp; Administrative." data-tip="Operating Expenses: $35,582.0M in Q3 2026.">Total Operating Expenses ($M)</span></td>
              <td>${s5q["operating_expenses"][0]:,.1f}M</td>
              <td>${s5q["operating_expenses"][1]:,.1f}M</td>
              <td>${s5q["operating_expenses"][2]:,.1f}M</td>
              <td>${s5q["operating_expenses"][3]:,.1f}M</td>
              <td class="col-q0">${s5q["operating_expenses"][4]:,.1f}M</td>
              <td class="col-est">$35,000.0M</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">↳ Research &amp; Development (R&amp;D)</td>
              <td>$14,000.0M</td>
              <td>$15,500.0M</td>
              <td>$17,000.0M</td>
              <td>$15,500.0M</td>
              <td class="col-q0">$17,500.0M</td>
              <td class="col-est">$18,500.0M</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">↳ Sales &amp; Marketing</td>
              <td>$8,000.0M</td>
              <td>$9,500.0M</td>
              <td>$9,800.0M</td>
              <td>$8,800.0M</td>
              <td class="col-q0">$10,200.0M</td>
              <td class="col-est">$10,800.0M</td>
            </tr>
            <tr class="sub-row">
              <td style="padding-left: 20px;">↳ General &amp; Administrative</td>
              <td>$4,118.0M</td>
              <td>$4,749.0M</td>
              <td>$5,328.0M</td>
              <td>$4,629.0M</td>
              <td class="col-q0">$7,882.0M</td>
              <td class="col-est">$5,700.0M</td>
            </tr>
            <tr style="font-weight: 800; background: rgba(16, 185, 129, 0.05);">
              <td><span class="tip" title="Operating Income (EBIT): Gross Profit minus Operating Expenses." data-tip="Operating Income: $40,576.0M operating profit in Q3 2026.">Operating Income (EBIT)</span></td>
              <td>${s5q["operating_income"][0]:,.1f}M</td>
              <td>${s5q["operating_income"][1]:,.1f}M</td>
              <td>${s5q["operating_income"][2]:,.1f}M</td>
              <td>${s5q["operating_income"][3]:,.1f}M</td>
              <td class="col-q0" style="color:#34d399;">${s5q["operating_income"][4]:,.1f}M</td>
              <td class="col-est" style="color:#34d399;">$43,000.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="GAAP Net Income available to common stockholders." data-tip="GAAP Net Income: $26,468.0M in Q3 2026.">GAAP Net Income</span></td>
              <td>${s5q["gaap_net_income"][0]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][1]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][2]:,.1f}M</td>
              <td>${s5q["gaap_net_income"][3]:,.1f}M</td>
              <td class="col-q0">${s5q["gaap_net_income"][4]:,.1f}M</td>
              <td class="col-est">$35,000.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Diluted earnings per share." data-tip="Diluted EPS: $2.12 GAAP EPS in Q3 2026 across diluted shares.">Diluted Earnings Per Share ($)</span></td>
              <td>${s5q["gaap_diluted_eps"][0]:.2f}</td>
              <td>${s5q["gaap_diluted_eps"][1]:.2f}</td>
              <td>${s5q["gaap_diluted_eps"][2]:.2f}</td>
              <td>${s5q["gaap_diluted_eps"][3]:.2f}</td>
              <td class="col-q0">${s5q["gaap_diluted_eps"][4]:.2f}</td>
              <td class="col-est">$2.85</td>
            </tr>
            <tr style="font-weight: 700; background: rgba(59, 130, 246, 0.04);">
              <td><span class="tip" title="Cash flow generated from operating activities." data-tip="Operating Cash Flow: $42,290.0M generated in Q3 2026.">Operating Cash Flow (OCF)</span></td>
              <td>${s5q["operating_cash_flow"][0]:,.1f}M</td>
              <td>${s5q["operating_cash_flow"][1]:,.1f}M</td>
              <td>${s5q["operating_cash_flow"][2]:,.1f}M</td>
              <td>${s5q["operating_cash_flow"][3]:,.1f}M</td>
              <td class="col-q0">${s5q["operating_cash_flow"][4]:,.1f}M</td>
              <td class="col-est">$48,000.0M</td>
            </tr>
            <tr>
              <td><span class="tip" title="Capital Expenditures dedicated to technical infrastructure, servers, and data centers." data-tip="Capital Expenditures: $51,355.0M invested in Q3 2026 to expand TPU compute clusters and AI data centers.">Capital Expenditures (CapEx)</span></td>
              <td>${s5q["capital_expenditures"][0]:,.1f}M</td>
              <td>${s5q["capital_expenditures"][1]:,.1f}M</td>
              <td>${s5q["capital_expenditures"][2]:,.1f}M</td>
              <td>${s5q["capital_expenditures"][3]:,.1f}M</td>
              <td class="col-q0">${s5q["capital_expenditures"][4]:,.1f}M</td>
              <td class="col-est">$45,000.0M</td>
            </tr>
            <tr style="font-weight: 700;">
              <td><span class="tip" title="Standard Free Cash Flow: OCF minus CapEx." data-tip="Reported FCF: $42,290.0M OCF - $51,355.0M CapEx = -$9,065.0M.">Reported Free Cash Flow (FCF)</span></td>
              <td>${s5q["reported_fcf"][0]:,.1f}M</td>
              <td>${s5q["reported_fcf"][1]:,.1f}M</td>
              <td>${s5q["reported_fcf"][2]:,.1f}M</td>
              <td>${s5q["reported_fcf"][3]:,.1f}M</td>
              <td class="col-q0" style="color: #f87171;">${s5q["reported_fcf"][4]:,.1f}M</td>
              <td class="col-est">$3,000.0M</td>
            </tr>
            <tr style="font-weight: 800; background: rgba(16, 185, 129, 0.05);">
              <td><span class="tip" title="True Free Cash Flow: Reported FCF minus SBC and Finance Leases." data-tip="True FCF: -$9,065.0M Reported FCF - $8,630.0M SBC = -$17,695.0M organic free cash flow.">Forensic True FCF (ex-SBC &amp; Leases)</span></td>
              <td>${s5q["true_fcf"][0]:,.1f}M</td>
              <td>${s5q["true_fcf"][1]:,.1f}M</td>
              <td>${s5q["true_fcf"][2]:,.1f}M</td>
              <td>${s5q["true_fcf"][3]:,.1f}M</td>
              <td class="col-q0" style="color:#f87171;">${s5q["true_fcf"][4]:,.1f}M</td>
              <td class="col-est">-$5,000.0M</td>
            </tr>
          </tbody>
        </table>
      </div>'''
        text = text[:old_table.start()] + new_table_content + text[old_table.end():]
        print(f"[{ticker}] Updated 5Q Table")

    # 4. Update Section 3 Forensic Waterfall Grid
    old_fcf = re.search(r'<section class="section" id="sec-fcf".*?</section>', text, re.DOTALL)
    if old_fcf:
        new_fcf_content = '''<section class="section" id="sec-fcf" style="margin-bottom: 26px;">
      <h2 style="font-size: 16px; font-weight: 800; color: #f1f5f9; margin-bottom: 12px; letter-spacing: 0.02em;">
        3. Forensic Quality-of-Earnings &amp; True Free Cash Flow Waterfall Bridge
      </h2>
      <div class="forensic-grid" style="display: grid; grid-template-columns: 1fr; gap: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px;">
        <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 8px;">
          <strong>Forensic Bridge Reconciliation:</strong> Operating Cash Flow of <strong>${q0_ocf:,.0f}M</strong> minus CapEx of <strong>${q0_capex:,.0f}M</strong> yields Reported Free Cash Flow of <strong>${q0_rep_fcf:,.0f}M</strong>. Subtracting non-cash Stock-Based Compensation of <strong>${q0_sbc:,.0f}M</strong> and Finance Leases of <strong>${q0_leases:,.0f}M</strong> bridges directly to True Free Cash Flow of <strong>${q0_true_fcf:,.0f}M</strong>.
        </div>
        <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.03);">
          <span><span class="tip" title="Operating Cash Flow: Cash generated from global services and cloud." data-tip="Operating Cash Flow: $42,290M generated in Q3 alone.">Operating Cash Flow (OCF)</span></span>
          <span class="mono" style="font-weight: 700; color: #34d399;">${q0_ocf:,.0f}M (${q0_ocf:,.2f})</span>
        </div>
        <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.03);">
          <span><span class="tip" title="Capital Expenditures: Investment in AI servers, TPUs, and data center infrastructure." data-tip="CapEx: $51,355M invested into technical infrastructure and data centers.">Less: Capital Expenditures (CapEx)</span></span>
          <span class="mono" style="font-weight: 700; color: #f87171;">-${q0_capex:,.0f}M</span>
        </div>
        <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-radius: 6px; background: rgba(59, 130, 246, 0.08); font-weight: 700;">
          <span>Standard Reported Free Cash Flow</span>
          <span class="mono" style="color: #f87171;">${q0_rep_fcf:,.0f}M</span>
        </div>
        <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.03);">
          <span><span class="tip" title="Stock-Based Compensation: Non-cash equity incentives." data-tip="Stock-Based Compensation: $8,630M equity compensation.">Less: Non-Cash Stock-Based Compensation (SBC)</span></span>
          <span class="mono" style="font-weight: 700; color: #f87171;">-${q0_sbc:,.0f}M</span>
        </div>
        <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.03);">
          <span><span class="tip" title="Finance Leases: Capital lease obligations and repayments." data-tip="Finance Leases: $0M in Q3 2026.">Less: Capital &amp; Finance Lease Principal</span></span>
          <span class="mono" style="color: var(--text-muted);">$0M</span>
        </div>
        <div class="waterfall-row" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; border-radius: 6px; background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.35); font-weight: 800;">
          <span><span class="tip" title="Forensic True Free Cash Flow: True unencumbered cash flow." data-tip="True FCF: -$9,065M - $8,630M SBC = -$17,695M organic true FCF.">Forensic True Free Cash Flow</span></span>
          <span class="mono" style="color: #f87171; font-size: 15px;">${q0_true_fcf:,.0f}M</span>
        </div>
      </div>
    </section>'''
        text = text[:old_fcf.start()] + new_fcf_content + text[old_fcf.end():]
        print(f"[{ticker}] Updated Section 3 Forensic Waterfall Grid")

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[{ticker}] Wrote updated builder script!")
