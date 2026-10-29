"""
US Markets Quick-View Snapshot (top-of-page market strip)
- Fetches live quotes + intraday sparklines via yfinance for:
  S&P 500, Dow 30, Nasdaq, Russell 2000, 10-Yr Bond (yield), VIX, Gold, Crude Oil (WTI),
  Bitcoin USD, and a US Private Equity equal-weight basket (BX, KKR, APO, ARES, CG, TPG).
- Change / % change are computed against the prior session close; the 10-Yr yield shows change in bp.
- After the US session closes, "last" is the official daily close (intraday bars still drive the sparkline).
- Bitcoin trades 24/7: its change is a rolling 24h change (15-min bars over the last 24h; first bar = baseline).
- Caches the last good snapshot to market_snapshot.json so pages still render offline; cached
  instruments that keep failing are flagged stale and dropped after 24h.
- Used at build time by build_news_portal.py and live by serve_reports.py (/api/market-snapshot).
"""

import json
import os
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, time as dtime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_DIR = Path(__file__).parent.resolve()
CACHE_FILE = BASE_DIR / "market_snapshot.json"

ET = ZoneInfo("America/New_York")
PE_BASKET = ["BX", "KKR", "APO", "ARES", "CG", "TPG"]
PE_MIN_CONSTITUENTS = 5
STALE_MAX_AGE_SECONDS = 24 * 3600

INSTRUMENTS = [
    {"key": "spx", "label": "S&P 500", "symbol": "^GSPC", "decimals": 2},
    {"key": "dji", "label": "Dow 30", "symbol": "^DJI", "decimals": 2},
    {"key": "ixic", "label": "Nasdaq", "symbol": "^IXIC", "decimals": 2},
    {"key": "rut", "label": "Russell 2000", "symbol": "^RUT", "decimals": 2},
    {"key": "tnx", "label": "10-Yr Bond", "symbol": "^TNX", "decimals": 3, "unit": "yield"},
    {"key": "vix", "label": "VIX", "symbol": "^VIX", "decimals": 2},
    {"key": "gold", "label": "Gold", "symbol": "GC=F", "decimals": 2},
    {"key": "crude", "label": "Crude Oil (WTI)", "symbol": "CL=F", "decimals": 2},
    {"key": "btc", "label": "Bitcoin USD", "symbol": "BTC-USD", "decimals": 2, "session": "24h"},
    {"key": "pe", "label": "US Private Equity", "symbol": "PE-EW6", "decimals": 2, "basket": PE_BASKET},
]

SPARK_W, SPARK_H, SPARK_PAD = 64, 26, 2
_FETCH_LOCK = threading.Lock()


def _fetch_symbol(symbol: str) -> dict | None:
    """Returns intraday close series (latest session), the prior session close and that session's daily close."""
    import yfinance as yf

    t = yf.Ticker(symbol)
    intra = t.history(period="1d", interval="5m")["Close"].dropna()
    daily = t.history(period="7d", interval="1d")["Close"].dropna()
    if intra.empty:
        return None
    last_ts = intra.index[-1]
    session_date = last_ts.date()
    prior = daily[[d.date() < session_date for d in daily.index]] if not daily.empty else daily
    prev_close = float(prior.iloc[-1]) if len(prior) else float(intra.iloc[0])
    session = daily[[d.date() == session_date for d in daily.index]] if not daily.empty else daily
    official_close = float(session.iloc[-1]) if len(session) else None
    return {"series": intra, "prev_close": prev_close, "last": float(intra.iloc[-1]), "last_ts": last_ts,
            "official_close": official_close}


def _fetch_rolling_24h(symbol: str) -> dict | None:
    """24/7 instruments: 15-min bars from the last 24h; the first bar of that window is the change baseline."""
    import pandas as pd
    import yfinance as yf

    bars = yf.Ticker(symbol).history(period="5d", interval="15m")["Close"].dropna()
    if bars.empty:
        return None
    last_ts = bars.index[-1]
    window = bars[bars.index >= last_ts - pd.Timedelta(hours=24)]
    return {"series": window, "prev_close": float(window.iloc[0]), "last": float(window.iloc[-1]),
            "last_ts": last_ts, "official_close": None}


def _fetch_basket(symbols: list[str]) -> dict | None:
    """Equal-weight basket rebased to 100 at the prior close (daily-rebalanced EW index)."""
    import pandas as pd

    with ThreadPoolExecutor(max_workers=len(symbols)) as ex:
        results = list(ex.map(_safe_fetch, symbols))
    used = [(sym, res) for sym, res in zip(symbols, results) if res]
    if len(used) < min(PE_MIN_CONSTITUENTS, len(symbols)):
        print(f"[market_snapshot] basket: only {len(used)}/{len(symbols)} constituents fetched", file=sys.stderr)
        return None
    frame = pd.concat([res["series"] / res["prev_close"] for _, res in used], axis=1).sort_index().ffill().dropna()
    if frame.empty:
        return None
    ew = frame.mean(axis=1) * 100.0
    closes = [(res["last"] if res.get("official_close") is None else res["official_close"]) / res["prev_close"]
              for _, res in used]
    return {"series": ew, "prev_close": 100.0, "last": float(ew.iloc[-1]),
            "last_ts": max(res["last_ts"] for _, res in used),
            "official_close": sum(closes) / len(closes) * 100.0,
            "constituents_ok": len(used), "constituents_used": [sym for sym, _ in used]}


def _safe_fetch(symbol: str, rolling_24h: bool = False) -> dict | None:
    try:
        return _fetch_rolling_24h(symbol) if rolling_24h else _fetch_symbol(symbol)
    except Exception as exc:  # network / parsing failure for one symbol must not break the strip
        print(f"[market_snapshot] {symbol} fetch failed: {exc}", file=sys.stderr)
        return None


def _spark_paths(values: list[float], prev_close: float, max_points: int = 72) -> dict:
    if not values:
        values = [prev_close]
    step = max(1, len(values) // max_points)
    pts = values[::step]
    if pts[-1] != values[-1]:
        pts.append(values[-1])
    if len(pts) == 1:
        pts = pts * 2
    lo = min(min(pts), prev_close)
    hi = max(max(pts), prev_close)
    rng = (hi - lo) or 1.0
    inner_w = SPARK_W - 2 * SPARK_PAD
    inner_h = SPARK_H - 2 * SPARK_PAD
    n = len(pts)
    coords = [
        (SPARK_PAD + i * inner_w / (n - 1), SPARK_PAD + (hi - v) / rng * inner_h)
        for i, v in enumerate(pts)
    ]
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in coords)
    area = f"{line} L{coords[-1][0]:.1f} {SPARK_H} L{coords[0][0]:.1f} {SPARK_H} Z"
    base_y = SPARK_PAD + (hi - prev_close) / rng * inner_h
    return {"spark_line": line, "spark_area": area, "spark_base_y": round(base_y, 1)}


def _build_item(cfg: dict, data: dict | None, closed: bool = False) -> dict | None:
    if not data:
        return None
    d = cfg["decimals"]
    rolling_24h = cfg.get("session") == "24h"  # 24/7 market: never substitute an "official" daily close
    use_official = closed and not rolling_24h and data.get("official_close") is not None
    last = data["official_close"] if use_official else data["last"]
    prev = data["prev_close"]
    change = last - prev
    pct = (change / prev * 100.0) if prev else 0.0
    direction = "up" if change > 0 else ("down" if change < 0 else "flat")
    ts = data["last_ts"]
    if cfg.get("unit") == "yield":
        last_fmt, change_fmt, pct_fmt = f"{last:,.{d}f}%", f"{change * 100:+.1f} bp", ""
    else:
        last_fmt, change_fmt, pct_fmt = f"{last:,.{d}f}", f"{change:+,.{d}f}", f"{pct:+.2f}%"
    item = {
        "key": cfg["key"],
        "label": cfg["label"],
        "symbol": cfg["symbol"],
        "decimals": d,
        "last": round(last, d),
        "prev_close": round(prev, d),
        "change": round(change, d),
        "change_pct": round(pct, 2),
        "direction": direction,
        "last_fmt": last_fmt,
        "change_fmt": change_fmt,
        "pct_fmt": pct_fmt,
        "last_ts": ts.isoformat(),
        "price_basis": "official_close" if use_official else "intraday",
        "stale": False,
    }
    if cfg.get("unit"):
        item["unit"] = cfg["unit"]
    if cfg.get("unit") == "yield":
        item["change_bp"] = round(change * 100, 1)
    if rolling_24h:
        item["session"] = "24h"
        item["note"] = "24h change"
    if cfg.get("basket"):
        used = data.get("constituents_used") or cfg["basket"]
        missing = [s for s in cfg["basket"] if s not in used]
        item["basket"] = cfg["basket"]
        item["basket_used"] = used
        item["note"] = (f"Equal-weight index of {', '.join(used)} ({len(used)}/{len(cfg['basket'])} constituents"
                        + (f"; {', '.join(missing)} unavailable" if missing else "") + "; prior close = 100)")
    item.update(_spark_paths([float(v) for v in data["series"].values], prev))
    return item


def _load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _write_cache(snapshot: dict) -> None:
    """Atomic write: temp file in the cache directory, then os.replace()."""
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(prefix=f".{CACHE_FILE.name}.", suffix=".tmp", dir=CACHE_FILE.parent)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(snapshot, fh, indent=2)
        for attempt in range(5):
            try:
                os.replace(tmp, CACHE_FILE)
                tmp = None
                break
            except PermissionError:  # Windows: a concurrent reader can briefly hold the target open
                if attempt == 4:
                    raise
                time.sleep(0.05)
    except Exception as exc:
        print(f"[market_snapshot] cache write failed: {exc}", file=sys.stderr)
    finally:
        if tmp:
            try:
                os.remove(tmp)
            except OSError:
                pass


def _iso_epoch(value) -> float | None:
    try:
        return datetime.fromisoformat(value).timestamp()
    except Exception:
        return None


def _reuse_stale(cached: dict, cache: dict, now_epoch: float) -> dict | None:
    """Cached copy of an instrument that failed to fetch; None once its last good fetch is older than 24h."""
    fetched = cached.get("fetched_epoch") or cache.get("fetched_epoch") or _iso_epoch(cached.get("last_ts"))
    if not fetched or now_epoch - fetched > STALE_MAX_AGE_SECONDS:
        return None
    stale_since = cached.get("stale_since") or datetime.fromtimestamp(fetched, timezone.utc).isoformat()
    return dict(cached, stale=True, stale_since=stale_since, fetched_epoch=fetched)


def _fmt_et(dt: datetime) -> str:
    return f"{dt:%b} {dt.day}, {dt.hour % 12 or 12}:{dt:%M} {'AM' if dt.hour < 12 else 'PM'} ET"


def _cached_as_of(cache: dict, items: list[dict]) -> str | None:
    """'As of' for a snapshot whose S&P 500 bar is cached: the cached stamp, else the newest stale bar, + ' (cached)'."""
    suffix = " (cached)"
    cached = str(cache.get("as_of_display") or "").strip()
    if cached and cached != "Market data unavailable":
        return cached if cached.endswith(suffix) else cached + suffix
    stale_ts = [ts for ts in (_iso_epoch(it.get("last_ts")) for it in items if it.get("stale")) if ts]
    if stale_ts:
        return _fmt_et(datetime.fromtimestamp(max(stale_ts), ET)) + suffix
    return None


def _session_status(spx: dict | None, now_et: datetime) -> tuple[str, str]:
    """(market_state, as_of_display) from the last S&P 500 5-min bar, in America/New_York."""
    if not spx:
        is_open = now_et.weekday() < 5 and dtime(9, 30) <= now_et.time() < dtime(16, 0)
        return ("open" if is_open else "closed"), _fmt_et(now_et)
    bar_start = datetime.fromisoformat(spx["last_ts"].isoformat()).astimezone(ET)
    bar_end = bar_start + timedelta(minutes=5)
    session_close = bar_start.replace(hour=16, minute=0, second=0, microsecond=0)
    full_session = bar_start.time() >= dtime(15, 55)
    early_close = now_et >= session_close + timedelta(minutes=15)  # e.g. 1 PM half-days
    if full_session or bar_start.date() < now_et.date() or early_close:
        return "closed", f"{_fmt_et(session_close if full_session else bar_end)} close"
    return "open", _fmt_et(bar_end)


def fetch_market_snapshot(max_age_seconds: int = 0) -> dict:
    """
    Returns the snapshot dict. If the cache is younger than max_age_seconds it is reused.
    Any instrument that fails to fetch falls back to its cached value (flagged stale=True).
    """
    with _FETCH_LOCK:
        cache = _load_cache()
        if cache and max_age_seconds > 0 and time.time() - cache.get("fetched_epoch", 0) < max_age_seconds:
            return cache

        def fetch_cfg(cfg):
            if cfg.get("basket"):
                try:
                    return _fetch_basket(cfg["basket"])
                except Exception as exc:
                    print(f"[market_snapshot] basket fetch failed: {exc}", file=sys.stderr)
                    return None
            return _safe_fetch(cfg["symbol"], rolling_24h=cfg.get("session") == "24h")

        try:
            with ThreadPoolExecutor(max_workers=6) as ex:
                raw = list(ex.map(fetch_cfg, INSTRUMENTS))
        except Exception as exc:
            print(f"[market_snapshot] snapshot fetch failed: {exc}", file=sys.stderr)
            raw = [None] * len(INSTRUMENTS)

        now_epoch = time.time()
        # "As of" / market state come from the S&P 500 bars (ET); wall clock in ET if SPX failed.
        # The wall-clock state only decides official-close vs intraday for instruments fetched fresh now.
        spx_idx = next((i for i, c in enumerate(INSTRUMENTS) if c["key"] == "spx"), None)
        spx_raw = raw[spx_idx] if spx_idx is not None else None
        market_state, as_of_display = _session_status(spx_raw, datetime.now(ET))

        cached_items = {it["key"]: it for it in cache.get("items", [])}
        items = []
        fresh_keys = set()
        for cfg, data in zip(INSTRUMENTS, raw):
            item = _build_item(cfg, data, closed=market_state == "closed")
            if item is not None:
                item["fetched_epoch"] = now_epoch
                fresh_keys.add(cfg["key"])
            elif cfg["key"] in cached_items:
                item = _reuse_stale(cached_items[cfg["key"]], cache, now_epoch)
            if item is not None:
                items.append(item)

        if not items:
            return {"items": [], "as_of_display": "Market data unavailable", "market_state": market_state,
                    "fetched_epoch": 0, "pe_basket": PE_BASKET}

        if "spx" not in fresh_keys and any(it.get("stale") for it in items):
            # Never stamp cached prices with the wall clock: keep the cached session's "as of" and state.
            as_of_display = _cached_as_of(cache, items) or as_of_display
            market_state = cache.get("market_state") or market_state

        if not fresh_keys:
            # Nothing fetched fresh: keep the cached fetch time (so max_age reuse and the UI never treat
            # stale data as new) and leave the last good cache file untouched.
            snapshot = {
                "items": items,
                "as_of_display": as_of_display,
                "market_state": market_state,
                "fetched_epoch": cache.get("fetched_epoch", 0),
                "source": "Yahoo Finance (yfinance)",
                "pe_basket": PE_BASKET,
            }
            if cache.get("fetched_utc"):
                snapshot["fetched_utc"] = cache["fetched_utc"]
            return snapshot

        snapshot = {
            "items": items,
            "as_of_display": as_of_display,
            "market_state": market_state,
            "fetched_utc": datetime.now(timezone.utc).isoformat(),
            "fetched_epoch": now_epoch,
            "source": "Yahoo Finance (yfinance)",
            "pe_basket": PE_BASKET,
        }
        _write_cache(snapshot)
        return snapshot


if __name__ == "__main__":
    snap = fetch_market_snapshot()
    for it in snap.get("items", []):
        print(f"{it['label']:<18} {it['last_fmt']:>12} {it['change_fmt']:>10} {it['pct_fmt']:>8}{'  (stale)' if it.get('stale') else ''}")
    print("As of:", snap.get("as_of_display"), f"[{snap.get('market_state', '?')}]")
