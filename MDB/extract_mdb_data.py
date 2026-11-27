import json
from pathlib import Path
import yfinance as yf
from edgar import Company, set_identity

set_identity("PortfolioResearch research@local.dev")
OUT_DIR = Path("c:/Users/nitin/.earningreport/MDB")
OUT_DIR.mkdir(exist_ok=True)

peers = ["MDB", "SNOW", "DDOG", "ESTC", "DT", "ORCL"]
peer_data = {}
for sym in peers:
    try:
        t = yf.Ticker(sym)
        info = t.info or {}
        q_cf = t.quarterly_cashflow
        ttm_fcf = None
        if q_cf is not None and not q_cf.empty and "Free Cash Flow" in q_cf.index:
            vals = q_cf.loc["Free Cash Flow"].iloc[:4].dropna()
            if len(vals) > 0:
                ttm_fcf = round(float(vals.sum()) / 1e9, 2)
        peer_data[sym] = {
            "name": info.get("longName", sym),
            "price": info.get("currentPrice") or t.fast_info.get("last_price"),
            "mkt_cap_b": round((info.get("marketCap") or 0) / 1e9, 2),
            "ev_b": round((info.get("enterpriseValue") or 0) / 1e9, 2),
            "forward_pe": round(float(info.get("forwardPE")), 1) if info.get("forwardPE") else None,
            "ev_to_rev": round(float(info.get("enterpriseToRevenue")), 2) if info.get("enterpriseToRevenue") else None,
            "ps_ttm": round(float(info.get("priceToSalesTrailing12Months")), 2) if info.get("priceToSalesTrailing12Months") else None,
            "rev_growth_pct": round(float(info.get("revenueGrowth")) * 100, 1) if info.get("revenueGrowth") is not None else None,
            "gross_margin_pct": round(float(info.get("grossMargins")) * 100, 1) if info.get("grossMargins") is not None else None,
            "ttm_fcf_b": ttm_fcf,
        }
    except Exception as e:
        peer_data[sym] = {"error": str(e)}

sec_info = {}
try:
    comp = Company("MDB")
    facts = comp.get_facts()
    if facts:
        df_facts = facts.to_pandas() if hasattr(facts, "to_pandas") else None
        if df_facts is not None:
            sub_rows = df_facts[df_facts["concept"].str.contains("Revenue|Subscription|Services", case=False, na=False)]
            recent = sub_rows[sub_rows["end"] >= "2025-07-01"].copy()
            sec_info["revenue_concepts_sample"] = recent[["concept", "label", "start", "end", "val", "form"]].drop_duplicates().head(80).to_dict(orient="records")
except Exception as e:
    sec_info["error"] = str(e)

(OUT_DIR / "mdb_research_cache.json").write_text(
    json.dumps({"peers": peer_data, "sec": sec_info}, indent=2, default=str),
    encoding="utf-8"
)
print("Saved MDB/mdb_research_cache.json")
