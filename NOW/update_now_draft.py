import re

path = 'NOW/build_now_post_draft.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Table 1B-1 rows
new_sub_and_tot = '''f"""              <tr>
                <td><span class="tip" title="Reported Total Net Revenues across subscriptions and professional services." data-tip="Total Revenues: $4,106.0M consolidated net revenue (+20.5% YoY), beating consensus.">Total Net Revenues ($M)</span></td>
                <td>$3,987.0M</td>
                <td>$3,407.0M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$4,070.0M</td>
                <td style="font-weight:700; color: #34d399;">${q0_rev:,.1f}M</td>
                <td>
                  <span class="badge badge-bull">+$36.0M (+0.88%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:76%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>""",
    f"""              <tr>
                <td><span class="tip" title="Subscription revenues across cloud enterprise solutions." data-tip="Subscription Revenues: Core SaaS contract revenues ($3,988M vs $3,950M consensus, +21% YoY).">Subscription Revenues ($M)</span></td>
                <td>$3,892.0M</td>
                <td>$3,313.0M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">$3,950.0M</td>
                <td style="font-weight:700; color: #34d399;">$3,988.0M</td>
                <td>
                  <span class="badge badge-bull">+$38.0M (+0.96%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:75%; height:100%; background:linear-gradient(90deg, #3b82f6, #10b981);"></div></div>
                </td>
                <td><span class="badge badge-bull">BEAT</span></td>
              </tr>"""'''

old_1b1_first = re.search(r'f\"\"\"\s*<tr>\s*<td><span class=\"tip\"[^>]*>Subscription Revenues.*?<\/tr>\"\"\"', text, re.DOTALL)
if old_1b1_first:
    text = text[:old_1b1_first.start()] + new_sub_and_tot + text[old_1b1_first.end():]
    print('Updated Table 1B-1 rows!')
else:
    print('Table 1B-1 first row not matched!')

# 2. Update Strip Item
old_strip = re.search(r'<div class=\"strip-item\">\s*<span class=\"strip-label\">Q3 2026 Actual <span class=\"tip\"[^>]*>Subscription Revenue vs\. Street.*?<\/div>', text, re.DOTALL)
if old_strip:
    new_strip = '''<div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 Total Net Revenues ($4,106M, +20.5% YoY) vs Street." data-tip="Q3 2026 Total Revenues: Reported $4,106M (+20.5% YoY), with Subscription revenue reaching $3,988M (+21% YoY, +20.5% c/c), beating guidance midpoint.">Total Revenue vs. Street</span></span>
          <span class="strip-val" style="color: var(--bull-green);">${q0_rev:,.0f}M <span style="font-size:12px;">(+20.5% YoY | +$36M Beat)</span></span>
          <span class="kpi-sub">Sub Revenue: $3,988M (+21%) | cRPO: $13.65B (+20.5%)</span>
        </div>'''
    text = text[:old_strip.start()] + new_strip + text[old_strip.end():]
    print('Updated strip item!')
else:
    print('Strip item not matched!')

# 3. Update 5Q Table Total Revenue row
old_5q = re.search(r'<tr style=\"font-weight: 700; background: rgba\(59, 130, 246, 0\.06\);\">\s*<td><span class=\"tip\"[^>]*>Total Subscription Revenue.*?<\/tr>', text, re.DOTALL)
if old_5q:
    new_5q = '''<tr style="font-weight: 700; background: rgba(59, 130, 246, 0.06);">
              <td><span class="tip" title="Total recognized net revenues across subscription and professional services." data-tip="Total Net Revenues: $4,106.0M reported in Q3 2026 (+20.5% YoY), driven by $3,988M in subscription revenue.">Total Net Revenue ($M)</span></td>
              <td>$3,407.0M</td>
              <td>$3,568.0M</td>
              <td>$3,770.0M</td>
              <td>$3,987.0M</td>
              <td class="col-q0" style="font-weight:800; color:#34d399;">${q0_rev:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color:#60a5fa;">$4,360.0M</td>
            </tr>'''
    text = text[:old_5q.start()] + new_5q + text[old_5q.end():]
    print('Updated 5Q table row!')
else:
    print('5Q row not matched!')

# 4. Update Ledger
old_ledger = re.search(r'<!-- VERBATIM GROUND-TRUTH GROUNDING LEDGER -->.*?</div>', text, re.DOTALL)
if old_ledger:
    new_ledger = '''<!-- VERBATIM GROUND-TRUTH GROUNDING LEDGER -->
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 10px 14px; font-size: 12px; color: var(--text-muted); margin-top: 10px; margin-bottom: 14px;">
      <strong>Deterministic Grounding Verification:</strong> Regular Close Price: <span class="mono" style="color:#f8fafc;">${reg_price:.2f}</span> • After-Hours Price: <span class="mono" style="color:#34d399;">${ah_price:.2f}</span> • Reported Q3 2026 Total Revenue: <span class="mono" style="color:#60a5fa;">${q0_rev:,.0f}M (${q0_rev:.1f}M)</span> • Subscription Revenue: <span class="mono" style="color:#60a5fa;">$3,988M</span> • Reported Q3 2026 Operating Cash Flow (OCF): <span class="mono" style="color:#34d399;">${q0_ocf:,.0f}M (${q0_ocf:.1f}M)</span> • Standard Reported FCF: <span class="mono" style="color:#fcd34d;">${q0_rep_fcf:,.0f}M</span> • Forensic True Free Cash Flow: <span class="mono" style="color:#34d399;">${q0_true_fcf:,.0f}M</span> • Post-Print Move: <span class="mono" style="color:#f87171;">{post_move_pct:+.2f}%</span> vs Expected <span class="mono">±{opt_implied_pct:.2f}%</span>.
    </div>'''
    text = text[:old_ledger.start()] + new_ledger + text[old_ledger.end():]
    print('Updated ledger!')
else:
    print('Ledger not matched!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Successfully wrote updated NOW builder!')
