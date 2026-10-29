import re

path = 'FTNT/build_ftnt_post_draft.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Table 1B-1 last row
old_1b1 = re.search(r'f\"\"\"\s*<tr>\s*<td><span class=\"tip\"[^>]*>Total Recognized Revenue.*?<\/tr>\"\"\"', text, re.DOTALL)
if old_1b1:
    new_1b1 = '''f"""              <tr>
                <td><span class="tip" title="Reported Total Net Revenues ($2,078.4M consolidated net revenue, +20.5% YoY)." data-tip="Total Revenues: $2,078.4M reported recognized revenue across products and services.">Total Net Revenue ($M)</span></td>
                <td>$2,047.9M</td>
                <td>$1,724.9M</td>
                <td class="col-q0" style="font-weight:700; color: #60a5fa;">${cons_rev:,.1f}M</td>
                <td style="font-weight:700; color: #f87171;">${q0_rev:,.1f}M</td>
                <td>
                  <span class="badge badge-bear">-${cons_rev - q0_rev:,.1f}M ({(q0_rev - cons_rev)/cons_rev * 100:.2f}%)</span>
                  <div class="beat-bar-track" style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; margin-top:4px; overflow:hidden;"><div class="beat-bar-fill" style="width:48%; height:100%; background:linear-gradient(90deg, #ef4444, #f59e0b);"></div></div>
                </td>
                <td><span class="badge badge-bear">SLIGHT MISS</span></td>
              </tr>"""'''
    text = text[:old_1b1.start()] + new_1b1 + text[old_1b1.end():]
    print('Updated 1B-1 row')
else:
    print('1B-1 row not matched!')

# 2. Update Strip Item
old_strip = re.search(r'<div class=\"strip-item\">\s*<span class=\"strip-label\">Q3 2026 Actual <span class=\"tip\"[^>]*>Recognized Revenue vs\. Street.*?<\/div>', text, re.DOTALL)
if old_strip:
    new_strip = '''<div class="strip-item">
          <span class="strip-label">Q3 2026 Actual <span class="tip" title="Reported Q3 2026 Total Net Revenue ($2,078.4M) vs Consensus ($2,120.0M)." data-tip="Q3 2026 Net Revenues: Reported $2,078.4M net quarterly revenue (+20.5% YoY), slightly trailing $2,120M consensus despite Billings beating ($2,340M vs $2,250M).">Net Revenue vs. Street</span></span>
          <span class="strip-val" style="color: var(--bear-red);">${q0_rev:,.1f}M <span style="font-size:12px;">(-1.96% Miss vs $2,120M)</span></span>
          <span class="kpi-sub">Street Est: $2,120.0M | Billings: $2,340M (+29% YoY)</span>
        </div>'''
    text = text[:old_strip.start()] + new_strip + text[old_strip.end():]
    print('Updated strip item')
else:
    print('Strip item not matched!')

# 3. Update 5Q Table Total Revenue row
old_5q = re.search(r'<tr style=\"font-weight: 700; background: rgba\(59, 130, 246, 0\.06\);\">\s*<td><span class=\"tip\"[^>]*>Total Revenue.*?<\/tr>', text, re.DOTALL)
if old_5q:
    new_5q = '''<tr style="font-weight: 700; background: rgba(59, 130, 246, 0.06);">
              <td><span class="tip" title="Total recognized net revenue." data-tip="Total Recognized Revenue: $2,078.4M net quarterly revenue (+20.5% YoY).">Total Revenue ($M)</span></td>
              <td>$1,724.9M</td>
              <td>$1,905.0M</td>
              <td>$1,849.6M</td>
              <td>$2,047.9M</td>
              <td class="col-q0" style="font-weight:800; color:#34d399;">${rev_5q[4]:,.1f}M</td>
              <td class="col-est" style="font-weight:700; color:#60a5fa;">$2,200.0M</td>
            </tr>'''
    text = text[:old_5q.start()] + new_5q + text[old_5q.end():]
    print('Updated 5Q table row')
else:
    print('5Q row not matched!')

# 4. Update Ledger and comments
text = text.replace('$3,961M (${q0_rev:.1f}M)', '${q0_rev:,.0f}M (${q0_rev:.1f}M)')
text = text.replace('# 3961.0', '# 2078.4')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Successfully wrote updated FTNT builder!')
