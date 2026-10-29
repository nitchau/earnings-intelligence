"""
News Portal Ground-Truth Validator (AGENTS.md Rule 2 guardrail for the Discover portal in news.html / index.html)
Rebuilds every Section 1 / Section 2 article and every hovercard in memory and enforces:
  1. Provenance: every ledger fact is re-resolved from its source file with a fresh (uncached) read and re-formatted;
     raw value and rendered display must match exactly. Derived values, counts and tallies are recomputed, and money
     figures must carry the reporting currency of the SEC exhibit (prices / options / targets stay in USD).
  2. Coverage: every number token in visible text (sign, currency and unit included) must equal a token of a figure
     in that article's own ledger. Agent-bus prose is attributed quotation and is removed before the check, so numbers
     inside it can never vouch for template numbers.
  3. Hygiene: no placeholder garbage ("N/A", "None", "undefined", "NaN", "inf", "null", "$-").
  4. Structure: unique article ids, cited source files exist, sources_count == len(sources), citations in range.
  5. (CLI only) Published pages: news.html / index.html (root and published_reports/) carry the same articles as a rebuild.
Usage: python validate_news_portal.py   (exit code 1 on any violation)
"""

import html
import json
import re
import sys

from news_facts import (BASE_DIR, clear_cache, compute_derived, flag_from_basis, fmt_date_short, format_value, is_number,
                        load_json, reporting_currency, resolve)

NUM_TOKEN = re.compile(r"[+\-]?[$€±]?\d[\d,]*(?:\.\d+)?(?:%|[MBx](?![A-Za-z]))?")
FILE_PATH = re.compile(r"[\w./\\-]+\.(?:json|txt|html)\b")
# Labels that carry digits but are not numeric claims (period / filing / pipeline identifiers)
NON_CLAIM = re.compile(
    r"\bT[-+][01]\b|\bQ[-+]?[0-4]E?\b|\b\d+Q\b|\bExhibit 99\.1\b|\bItem 2\.02\b|\b[68]-K\b|\b10-[QK]\b"
    r"|\bAgent [0-9][A-C]?\b|\b(?:Stage|Layer) [0-9]\b|\b1-day\b"
)
CITATION = re.compile(r"\[(\d+(?:,\s*\d+)*)\]")
GARBAGE = re.compile(r"\bN/A\b|\bNone\b|\bundefined\b|\b[Nn]a[Nn]\b|\b(?:inf|Infinity)\b|\bnull\b|\$-|€-|±N/A")
MONEY_FORMATS = {"money_m", "signed_money_m", "eps", "signed_eps"}
LONG_TEXT = 60  # agent-bus prose (quoted, attributed); shorter text facts are labels such as 'Q3 2026 (Actual)'


def _norm(token: str) -> str:
    return token.replace(",", "")


def _tokens(text: str) -> set[str]:
    return {_norm(t) for t in NUM_TOKEN.findall(str(text))}


def _strip_html(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", text or ""))


def _ticker_of(rel: str) -> str:
    name = rel.replace("\\", "/").split("/")[-1]
    return name.split("_")[0] if "_" in name else rel.split("/")[0]


def _article_text(item: dict) -> list[tuple[str, str]]:
    parts = [("headline", item.get("headline", "")), ("summary", item.get("summary", "")),
             ("published", item.get("published", "")), ("chart", item.get("chart_alt", ""))]
    for key in ("status_badge", "verdict_badge", "earnings_date"):
        if item.get(key):
            parts.append((key, item[key]))
    for m in item.get("metrics_strip", []):
        parts.append(("metric", f"{m.get('label', '')} {m.get('val', '')}"))
    for t in item.get("key_takeaways", []):
        parts.append(("takeaway", _strip_html(t)))
    for s in item.get("sections", []):
        parts.append(("section", f"{s.get('heading', '')} {_strip_html(s.get('body', ''))}"))
    for s in item.get("sources", []):
        parts.append(("source", f"{s.get('name', '')} {s.get('detail', '')}"))
    return parts


def _hover_text(hs: dict) -> list[tuple[str, str]]:
    parts = [("hover-verdict", hs.get("verdict", "")), ("hover-date", hs.get("date", "")),
             ("hover-driver", hs.get("driver", "").rstrip("…")), ("hover-guide", hs.get("guide", ""))]
    for lbl, val, _ in hs.get("cells", []):
        parts.append(("hover-cell", f"{lbl} {val}"))
    for b in hs.get("boxes", []):
        parts.append(("hover-box", " ".join(str(b.get(k) or "") for k in ("label", "value", "small", "sub"))))
    if hs.get("footer"):
        parts.append(("hover-footer", " ".join(hs["footer"])))
    return parts


def _currency_error(fact: dict) -> str | None:
    if fact.get("fmt") not in MONEY_FORMATS:
        return None
    rel, path = fact["file"], fact["path"]
    reported = (rel.endswith("_post_truth.json") and path.startswith(("beat_miss_scorecard", "forensic_fcf_bridge_q0", "stitched_5q")))
    reported = reported or (rel.endswith("_truth.json") and path.startswith("forensic_fcf_bridge_latest"))
    expected = reporting_currency(_ticker_of(rel)) if reported else "$"
    if fact.get("ccy") != expected:
        return f"{rel} -> {path}: rendered in {fact.get('ccy')!r} but the source reports in {expected!r}"
    return None


def _verify_fact(fact: dict, number_pool: list[float]) -> str | None:
    kind = fact["kind"]
    if kind in ("num", "text", "date", "raw"):
        fresh = resolve(load_json(fact["file"], use_cache=False), fact["path"])
        if kind == "text" and isinstance(fresh, str):
            fresh = fresh.strip()
        if fresh != fact["raw"]:
            return f"{fact['file']} -> {fact['path']}: ledger raw {fact['raw']!r} != source {fresh!r}"
        if kind == "num":
            if format_value(fresh, fact["fmt"], fact["ccy"]) != fact["display"]:
                return f"{fact['file']} -> {fact['path']}: display {fact['display']!r} is not the {fact['fmt']} format of {fresh!r}"
            return _currency_error(fact)
        if kind == "date" and fmt_date_short(fresh) != fact["display"]:
            return f"{fact['file']} -> {fact['path']}: date display {fact['display']!r} != {fmt_date_short(fresh)!r}"
    elif kind == "file":
        if not (BASE_DIR / fact["file"]).exists() or fact["raw"] not in fact["file"]:
            return f"file fact {fact['file']} missing or does not carry date {fact['raw']}"
        if fmt_date_short(fact["raw"]) != fact["display"]:
            return f"file date display {fact['display']!r} != {fmt_date_short(fact['raw'])!r}"
    elif kind == "derived":
        value = compute_derived(fact["op"], fact["inputs"])
        if format_value(value, fact["fmt"], fact["ccy"]) != fact["display"]:
            return f"derived {fact['op']} display {fact['display']!r} != recomputed {value!r}"
        orphans = [x for x in fact["inputs"] if not any(abs(r - x) < 1e-9 for r in number_pool)]
        if orphans:
            return f"derived {fact['op']} uses inputs not present in the ledger: {orphans}"
    elif kind == "count":
        flags = [flag_from_basis(b) for b in fact["basis"]]
        if [1.0 if f else 0.0 for f in flags] != fact["inputs"] or str(sum(flags)) != fact["display"]:
            return f"count {fact.get('label')!r}: recomputed {sum(flags)} from its basis, rendered {fact['display']!r}"
        for b in fact["basis"]:
            if b["kind"] == "abs_vs_band" and not all(any(abs(r - v) < 1e-9 for r in number_pool) for v in (b["move"], abs(b["band"]))):
                return f"count {fact.get('label')!r}: band comparison uses values not present in the ledger"
    elif kind == "tally":
        members = fact.get("members", [])
        if len(members) != fact["raw"] or len(set(members)) != len(members) or str(len(members)) != fact["display"]:
            return f"tally {fact.get('label')!r}: {fact['display']!r} does not match its {len(set(members))} distinct members"
    elif kind == "exhibit":
        if reporting_currency(_ticker_of(fact["file"])) != fact["raw"]:
            return f"{fact['file']}: currency {fact['raw']!r} no longer matches the exhibit"
    return None


def _check_facts(facts: list[dict]) -> list[str]:
    pool = [float(f["raw"]) for f in facts if f["kind"] in ("num", "raw", "derived") and is_number(f.get("raw"))]
    pool += [abs(x) for x in pool]
    errors = [f"[provenance] {err}" for err in (_verify_fact(f, pool) for f in facts) if err]
    # Every tallied item must be a ticker whose own source files feed this same ledger
    cited = {_ticker_of(f["file"]) for f in facts if f.get("file")}
    for f in facts:
        if f["kind"] == "tally":
            strays = [m for m in f.get("members", []) if m not in cited]
            if strays:
                errors.append(f"[provenance] tally {f.get('label')!r} counts items with no source in this brief: {strays[:5]}")
    return errors


def _check_coverage(parts: list[tuple[str, str]], facts: list[dict], names: list[str]) -> list[str]:
    errors = []
    allowed = set()
    long_texts = []
    for f in facts:
        disp = f.get("display")
        if not disp:
            continue
        if f["kind"] == "text" and len(disp) > LONG_TEXT:
            long_texts.append(disp)
            continue
        allowed |= _tokens(disp)
        if f.get("display_iso"):
            allowed |= _tokens(f["display_iso"])
    long_texts.sort(key=len, reverse=True)
    for where, text in parts:
        clean = text
        # A trimmed quote (hovercards cut bus prose at ~320 chars) is a prefix of its recorded text fact
        if text.strip() and any(q.startswith(text.strip()) for q in long_texts):
            clean = ""
        for quote in long_texts:
            clean = clean.replace(quote, " ")
        for name in names:
            clean = clean.replace(name, " ")
        clean = NON_CLAIM.sub(" ", FILE_PATH.sub(" ", clean))
        if where in ("takeaway", "section"):
            clean = CITATION.sub(" ", clean)
        for tok in NUM_TOKEN.findall(clean):
            if _norm(tok) not in allowed:
                errors.append(f"[coverage] {where}: number {tok!r} is not backed by this brief's ledger -> {text[:140]!r}")
        bad = GARBAGE.search(text)
        if bad:
            errors.append(f"[hygiene] {where}: placeholder text {bad.group(0)!r} -> {text[:140]!r}")
    return errors


def validate_item(item: dict, names: list[str] | None = None) -> tuple[list[str], int]:
    facts = item["ledger"].facts
    errors = _check_facts(facts) + _check_coverage(_article_text(item), facts, names or [])
    n_sources = len(item.get("sources", []))
    if item.get("sources_count") != n_sources:
        errors.append(f"[structure] sources_count {item.get('sources_count')} != {n_sources} listed sources")
    for s in item.get("sources", []):
        if not (BASE_DIR / s["path"]).exists():
            errors.append(f"[structure] cited source file missing: {s['path']}")
    for blob in item.get("key_takeaways", []) + [s.get("body", "") for s in item.get("sections", [])]:
        for group in CITATION.findall(_strip_html(blob)):
            for n in (int(x) for x in group.split(",")):
                if not 1 <= n <= n_sources:
                    errors.append(f"[structure] citation [{n}] outside 1..{n_sources}")
    return errors, len(facts)


def _names(intel: dict, short_name) -> list[str]:
    names = set()
    for entry in intel.values():
        name = entry.get("company_name") or ""
        if name and any(ch.isdigit() for ch in name):
            names.update({name, short_name(name)})
    return sorted((n for n in names if n), key=len, reverse=True)


def _published_articles(path) -> dict | None:
    if not path.exists():
        return None
    m = re.search(r"const DISCOVER_ARTICLES = (.*?);\n", path.read_text(encoding="utf-8", errors="ignore"), re.S)
    return json.loads(m.group(1)) if m else None


def check_published(items: list[dict]) -> list[str]:
    """Published pages must carry exactly the articles a rebuild produces (otherwise they are stale)."""
    expected = {i["id"]: i["headline"] for i in items}
    errors = []
    for rel in ("news.html", "index.html", "published_reports/news.html", "published_reports/index.html"):
        arts = _published_articles(BASE_DIR / rel)
        if arts is None:
            errors.append(f"{rel}: [published] no Discover article payload found (run python update_index.py)")
            continue
        got = {k: v.get("headline") for k, v in arts.items()}
        if got != expected:
            missing, extra = sorted(set(expected) - set(got)), sorted(set(got) - set(expected))
            changed = sorted(k for k in set(expected) & set(got) if expected[k] != got[k])
            errors.append(f"{rel}: [published] out of date vs rebuild (missing {missing}, extra {extra}, changed {changed}); "
                          f"run python update_index.py")
    return errors


def validate_portal(intel: dict | None = None, published: bool = False) -> dict:
    import build_news_portal as portal

    clear_cache()
    if intel is None:
        intel = portal.discover_ticker_intelligence()
    names = _names(intel, portal._short_name)
    items = portal.build_market_news_items(intel) + portal.build_portfolio_news_items(intel)
    report = {"passed": True, "articles": len(items), "hovercards": 0, "facts_verified": 0, "errors": []}
    ids = [i["id"] for i in items]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        report["errors"].append(f"{dup}: [structure] duplicate article id")
    for item in items:
        errs, n = validate_item(item, names)
        report["facts_verified"] += n
        report["errors"].extend(f"{item['id']}: {e}" for e in errs)
    for tk, entry in sorted(intel.items()):
        L, hs = entry.get("hover_ledger"), entry.get("hover_summary") or {}
        facts = L.facts if L else []
        errs = _check_facts(facts) + _check_coverage(_hover_text(hs), facts, names)
        report["hovercards"] += 1
        report["facts_verified"] += len(facts)
        report["errors"].extend(f"hovercard-{tk}: {e}" for e in errs)
    if published:
        report["errors"].extend(check_published(items))
    report["passed"] = not report["errors"]
    return report


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    rep = validate_portal(published="--no-published" not in sys.argv)
    print(f"News portal ledger validation: {rep['articles']} articles, {rep['hovercards']} hovercards, "
          f"{rep['facts_verified']} ledger facts re-verified")
    for e in rep["errors"]:
        print(f"  FAIL {e}")
    print("PASSED" if rep["passed"] else f"FAILED ({len(rep['errors'])} violations)")
    sys.exit(0 if rep["passed"] else 1)
