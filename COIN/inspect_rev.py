from edgar import Company, set_identity
import pandas as pd

set_identity('PortfolioResearch research@local.dev')
c = Company('COIN')
f = c.get_filings(form='10-Q')[0]
x = f.xbrl()
s = x.statements[51]
df = s.to_dataframe()
for idx, r in df.iterrows():
    lbl = r.get('label')
    m_lbl = r.get('dimension_member_label')
    val_q2_26 = r.get('2026-06-30 (Q2)')
    val_q2_25 = r.get('2025-06-30 (Q2)')
    v26 = f"{val_q2_26/1e6:.1f}M" if pd.notnull(val_q2_26) and isinstance(val_q2_26, (int, float)) else str(val_q2_26)
    v25 = f"{val_q2_25/1e6:.1f}M" if pd.notnull(val_q2_25) and isinstance(val_q2_25, (int, float)) else str(val_q2_25)
    print(f"{str(lbl):35s} | {str(m_lbl):30s} | Q2 26: {v26:10s} | Q2 25: {v25}")
