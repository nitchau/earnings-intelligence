import yfinance as yf
import requests
from bs4 import BeautifulSoup

t = yf.Ticker("HOOD")
info = t.info or {}
fast = t.fast_info
print("Regular price:", fast.get("last_price"), info.get("regularMarketPrice"))
print("Post market price:", info.get("postMarketPrice"))
print("Previous close:", fast.get("previousClose"), info.get("regularMarketPreviousClose"))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
}
url = "https://www.google.com/finance/quote/HOOD:NASDAQ"
resp = requests.get(url, headers=headers, timeout=8)
if resp.status_code == 200:
    soup = BeautifulSoup(resp.text, "html.parser")
    reg = soup.find("div", {"class": "YMlKec fxKbKc"})
    print("Google Finance Regular:", reg.text if reg else "None")
    ext = soup.find("div", {"class": "yg1AZe"}) or soup.find("div", {"class": "NydbP"})
    if ext:
        p_text = ext.find("div", {"class": "YMlKec"})
        print("Google Finance After-Hours:", p_text.text if p_text else "None")
