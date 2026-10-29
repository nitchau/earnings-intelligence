"""
Ground-Truth Fact Ledger for the AI Discover News Portal
- Every figure the portal renders is resolved from a repo file (ground_truth/, post_agent_bus/,
  pre_agent_bus/, drafts/, {TICKER}/exhibit_99_1.txt) through a Ledger.
- The Ledger records file + JSON path + raw value + rendered display for each figure, so
  validate_news_portal.py can independently re-resolve and re-format every number (AGENTS.md Rule 2).
- Derived figures (QoQ %, beat counts, averages) record their operation and inputs so they can be recomputed.
"""

import json
import math
import re
from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_DIR = Path(__file__).parent.resolve()

_JSON_CACHE: dict[str, dict] = {}
_PATH_TOKEN = re.compile(r"[^.\[\]]+|\[-?\d+\]")


def load_json(rel: str, use_cache: bool = True) -> dict:
    """Loads a repo-relative JSON file ({} when missing or malformed)."""
    if use_cache and rel in _JSON_CACHE:
        return _JSON_CACHE[rel]
    path = BASE_DIR / rel
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            data = {}
    if not isinstance(data, dict):
        data = {}
    if use_cache:
        _JSON_CACHE[rel] = data
    return data


def clear_cache():
    _JSON_CACHE.clear()


def resolve(data, path: str):
    """Resolves a dotted path with optional [index] parts, e.g. 'stitched_5q_chronological.capital_expenditures[-1]'."""
    cur = data
    for tok in _PATH_TOKEN.findall(path):
        if cur is None:
            return None
        if tok.startswith("["):
            if not isinstance(cur, list):
                return None
            idx = int(tok[1:-1])
            if idx >= len(cur) or idx < -len(cur):
                return None
            cur = cur[idx]
        else:
            if not isinstance(cur, dict):
                return None
            cur = cur.get(tok)
    return cur


def is_number(val) -> bool:
    return isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(val)


def _q(val, places: int) -> Decimal:
    """Half-up rounding of the decimal value as written in the source (174.5 -> 175, 2.675 -> 2.68)."""
    return Decimal(repr(float(val))).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------------------
# Formatters (pure functions of the raw value, so the validator can re-run them)
# ---------------------------------------------------------------------------

def fmt_money_m(val, ccy="$"):
    """Millions -> '$64,601M' / '$174.5M' / '-€253M'; >= 10,000M renders in billions ('$64.60B')."""
    v = float(val)
    sign = "-" if v < 0 else ""
    av = abs(v)
    if av >= 10000:
        return f"{sign}{ccy}{_q(av / 1000, 2):,.2f}B"
    if av != int(av) and av < 1000:
        return f"{sign}{ccy}{_q(av, 1):,.1f}M"
    return f"{sign}{ccy}{_q(av, 0):,.0f}M"


def fmt_price(val, ccy="$"):
    v = float(val)
    sign = "-" if v < 0 else ""
    return f"{sign}{ccy}{_q(abs(v), 2):,.2f}"


def fmt_pct(val):
    q = _q(val, 2)
    if q == 0:
        return "0.00%"
    return f"{'+' if q > 0 else ''}{q:.2f}%"


def fmt_pct_plain(val):
    q = _q(val, 2)
    return f"{abs(q) if q == 0 else q:.2f}%"


def fmt_band(val):
    return f"±{_q(abs(float(val)), 2):.2f}%"


def fmt_mult(val):
    """Valuation multiple; a negative (loss-making) multiple is not meaningful."""
    return "NM" if float(val) < 0 else f"{_q(val, 2):.2f}x"


def fmt_int(val):
    return f"{_q(val, 0):,.0f}"


def fmt_signed_money_m(val, ccy="$"):
    v = float(val)
    out = fmt_money_m(v, ccy)
    return f"+{out}" if v > 0 else out


def fmt_signed_price(val, ccy="$"):
    v = float(val)
    out = fmt_price(v, ccy)
    return f"+{out}" if v > 0 else out


FORMATTERS = {
    "money_m": fmt_money_m,
    "signed_money_m": fmt_signed_money_m,
    "price": fmt_price,
    "eps": fmt_price,
    "signed_eps": fmt_signed_price,
    "pct": fmt_pct,
    "pct_plain": fmt_pct_plain,
    "band": fmt_band,
    "mult": fmt_mult,
    "int": fmt_int,
}

_CCY_FORMATS = {"money_m", "signed_money_m", "price", "eps", "signed_eps"}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fmt_date_short(iso: str) -> str:
    """'2026-10-28' -> 'Oct 28'."""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", iso or "")
    if not m:
        return iso or ""
    return f"{MONTHS[int(m.group(2)) - 1]} {int(m.group(3))}"


def format_value(raw, fmt: str, ccy: str = "$") -> str:
    fn = FORMATTERS[fmt]
    if fmt in _CCY_FORMATS:
        return fn(raw, ccy)
    return fn(raw)


DERIVE_OPS = {
    "pct_change": lambda new, old: (new - old) / abs(old) * 100.0,
    "diff": lambda a, b: a - b,
    "sum": lambda *xs: sum(xs),
    "mean": lambda *xs: sum(xs) / len(xs),
    "count": lambda *xs: float(sum(1 for x in xs if x)),
    "abs_max": lambda *xs: max(abs(x) for x in xs),
}


def compute_derived(op: str, inputs: list[float]) -> float:
    return DERIVE_OPS[op](*inputs)


def band_side(status) -> str:
    """Stage 1 move_vs_implied_status -> 'inside' / 'outside' / ''."""
    s = str(status or "").upper()
    if "EXCEED" in s or "OUTSIDE" in s:
        return "outside"
    if "WITHIN" in s or "INSIDE" in s:
        return "inside"
    return ""


def flag_from_basis(basis: dict) -> bool:
    """Recomputes one count flag from its recorded basis (shared by the builder and the validator)."""
    kind = basis["kind"]
    if kind == "text_in":
        val = resolve(load_json(basis["file"], use_cache=False), basis["path"])
        return isinstance(val, str) and val.strip() in basis["accept"]
    if kind == "side_text":
        data = load_json(basis["file"], use_cache=False)
        return is_number(resolve(data, basis["band_path"])) and band_side(resolve(data, basis["path"])) == basis["side"]
    if kind == "abs_vs_band":
        outside = abs(basis["move"]) > abs(basis["band"])
        return outside if basis["side"] == "outside" else not outside
    raise ValueError(f"unknown count basis {kind}")


# ---------------------------------------------------------------------------
# Repo-specific deterministic helpers
# ---------------------------------------------------------------------------

def exhibit_rel(ticker: str) -> str:
    return f"{ticker}/exhibit_99_1.txt"


def _exhibit_text(ticker: str) -> str:
    path = BASE_DIR / exhibit_rel(ticker)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def reporting_currency(ticker: str) -> str:
    """Currency symbol of the reported financial statements, read from the SEC Exhibit 99.1 text."""
    text = _exhibit_text(ticker)
    if len(re.findall(r"\bEUR million", text)) >= 3:
        return "€"
    return "$"


_TZ_OFFSETS = {"EEST": 3, "EET": 2, "CEST": 2, "CET": 1, "BST": 1, "GMT": 0, "UTC": 0, "JST": 9, "KST": 9, "HKT": 8, "SGT": 8}
_MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December"]
_RELEASE_STAMP = re.compile(r"\b(\d{1,2}) (" + "|".join(_MONTH_NAMES) + r") (\d{4}) at (\d{1,2}):(\d{2}) ("
                            + "|".join(_TZ_OFFSETS) + r")\b")


def exhibit_release_time_et(ticker: str) -> datetime | None:
    """Release time printed on foreign-issuer exhibits ('22 October 2026 at 08:00 EEST'), converted to ET."""
    m = _RELEASE_STAMP.search(_exhibit_text(ticker)[:6000])
    if not m:
        return None
    local = datetime(int(m.group(3)), _MONTH_NAMES.index(m.group(2)) + 1, int(m.group(1)), int(m.group(4)),
                     int(m.group(5)), tzinfo=timezone(timedelta(hours=_TZ_OFFSETS[m.group(6)])))
    return local.astimezone(ZoneInfo("America/New_York"))


def filing_form(ticker: str, metadata_form: str = "") -> str:
    """Filing form from the exhibit cover page (6-K for foreign private issuers), falling back to metadata."""
    head = _exhibit_text(ticker)[:4000]
    m = re.search(r"\bFORM\s+(6-K|8-K)\b", head, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    return metadata_form or "8-K"


# ---------------------------------------------------------------------------
# Ledger
# ---------------------------------------------------------------------------

class Ledger:
    """Collects every figure rendered for one article, with its provenance."""

    def __init__(self):
        self.facts: list[dict] = []

    def _record(self, entry: dict):
        self.facts.append(entry)

    def raw(self, rel: str, path: str):
        """Resolves and records a raw value (used as an input to derived figures or logic)."""
        val = resolve(load_json(rel), path)
        if val is not None:
            self._record({"kind": "raw", "file": rel, "path": path, "raw": val, "display": None})
        return val

    def num(self, rel: str, path: str, fmt: str, ccy: str = "$", label: str = "") -> str | None:
        val = resolve(load_json(rel), path)
        if not is_number(val):
            return None
        display = format_value(val, fmt, ccy)
        self._record({"kind": "num", "file": rel, "path": path, "raw": val, "fmt": fmt, "ccy": ccy,
                      "display": display, "label": label})
        return display

    def text(self, rel: str, path: str, label: str = "") -> str | None:
        val = resolve(load_json(rel), path)
        if not isinstance(val, str) or not val.strip():
            return None
        val = val.strip()
        self._record({"kind": "text", "file": rel, "path": path, "raw": val, "display": val, "label": label})
        return val

    def date(self, rel: str, path: str, label: str = "") -> str | None:
        val = resolve(load_json(rel), path)
        if not isinstance(val, str) or not re.match(r"^\d{4}-\d{2}-\d{2}", val):
            return None
        display = fmt_date_short(val)
        self._record({"kind": "date", "file": rel, "path": path, "raw": val, "display": display,
                      "display_iso": val[:10], "label": label})
        return display

    def file_date(self, rel: str, iso: str, label: str = "") -> str:
        """A date carried by a repo filename (e.g. published_reports/GOOGL_T1_2026-10-28.html)."""
        display = fmt_date_short(iso)
        self._record({"kind": "file", "file": rel, "path": "", "raw": iso, "display": display,
                      "display_iso": iso, "label": label})
        return display

    def derived(self, op: str, inputs: list[float], fmt: str, ccy: str = "$", label: str = "") -> str | None:
        if not inputs or any(not is_number(x) for x in inputs):
            return None
        try:
            val = compute_derived(op, [float(x) for x in inputs])
        except ZeroDivisionError:
            return None
        display = format_value(val, fmt, ccy)
        self._record({"kind": "derived", "op": op, "inputs": [float(x) for x in inputs], "fmt": fmt,
                      "ccy": ccy, "raw": val, "display": display, "label": label})
        return display

    def count(self, basis: list[dict], label: str = "") -> str:
        """Counts items whose flag (recomputed from each recorded basis) is true; the validator recomputes it."""
        flags = [flag_from_basis(b) for b in basis]
        display = str(sum(1 for f in flags if f))
        self._record({"kind": "count", "basis": basis, "inputs": [1.0 if f else 0.0 for f in flags],
                      "raw": float(display), "display": display, "label": label})
        return display

    def tally(self, members: list[str], label: str = "") -> str:
        """Number of distinct items listed in the same article (e.g. upcoming prints shown)."""
        display = str(len(members))
        self._record({"kind": "tally", "members": list(members), "raw": len(members), "display": display, "label": label})
        return display

    def exhibit_currency(self, ticker: str) -> str:
        ccy = reporting_currency(ticker)
        self._record({"kind": "exhibit", "file": exhibit_rel(ticker), "path": "currency", "raw": ccy,
                      "display": None, "label": f"{ticker} reporting currency"})
        return ccy

    def displays(self) -> list[str]:
        out = []
        for f in self.facts:
            if f.get("display"):
                out.append(str(f["display"]))
            if f.get("display_iso"):
                out.append(f["display_iso"])
        return out

    def to_json(self) -> list[dict]:
        return list(self.facts)
