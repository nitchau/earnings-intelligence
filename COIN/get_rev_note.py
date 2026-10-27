from edgar import Company, set_identity
import sys

set_identity('PortfolioResearch research@local.dev')
c = Company('COIN')
x = c.get_filings(form='10-Q')[0].xbrl()
s = x.statements[11]
df = s.to_dataframe()
with open("COIN/revenue_statement.txt", "w", encoding="utf-8") as f:
    f.write(df.to_string())
print("Wrote COIN/revenue_statement.txt successfully!")
