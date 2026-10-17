from bs4 import BeautifulSoup

def analyze(filename):
    print(f"\n=================== {filename} ===================")
    soup = BeautifulSoup(open(filename, encoding="utf-8").read(), "html.parser")
    cards = soup.find_all("div", class_="card")
    print(f"Total cards: {len(cards)}")
    for i, c in enumerate(cards):
        header = c.find(class_="card-title")
        title = header.text.strip() if header else "NO TITLE"
        print(f"  Card {i+1}: {title[:80]}")

analyze("Stock_Analysis_v2.html")
analyze("published_reports/ISRG_T1_2026-10-20.html")
analyze("published_reports/NVDA_T1_2026-11-17.html")
