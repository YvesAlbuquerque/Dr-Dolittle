#!/usr/bin/env python3
"""Bounded, provenance-only Crossref DOI lookup worker.

Does NOT score scientific truth, infer peer review, clear retraction status, run AI,
or alter canonical bibliography or source_integrity.csv.

Default: dry-run plan without network. Live: --live explicitly; writes immutable
local snapshots under _local/crossref, which is gitignored.

Usage:
    python scripts/crossref_metadata_worker.py --limit 5
    python scripts/crossref_metadata_worker.py --live --limit 5 --email your@address.org
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CROSSREF = "https://api.crossref.org/works/"
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)
MAX_RECORDS = 25
MAX_BYTES = 2_000_000
RETRY_CODES = {429, 500, 502, 503, 504}
USER_AGENT = "DrDolittleMetadataResearch/0.1 (+https://github.com/YvesAlbuquerque/Dr-Dolittle)"
TIMEOUT_SECONDS = 15


def normalize_doi(value):
    if not isinstance(value, str):
        return None
    value = value.strip()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:)", "", value, flags=re.I).strip()
    if not DOI_RE.fullmatch(value):
        return None
    return value.lower()


def crossref_url(doi, email=None):
    normalized = normalize_doi(doi)
    if not normalized:
        raise ValueError("invalid DOI")
    path = urllib.parse.quote(normalized, safe="/")
    query = urllib.parse.urlencode({"mailto": email}) if email else ""
    return CROSSREF + path + ("?" + query if query else "")


def title_text(work):
    title = work.get("title", [])
    if isinstance(title, list) and title and isinstance(title[0], str):
        return title[0].strip()
    return None


def year_value(work):
    for key in ("published", "issued", "created"):
        node = work.get(key)
        try:
            year = node["date-parts"][0][0]
            if isinstance(year, int):
                return year
        except (TypeError, KeyError, IndexError):
            continue
    return None


def update_notices(work):
    """Record listed Crossref update metadata; absence never means 'no retraction'."""
    result = []
    for key in ("update-to", "updated-by"):
        entries = work.get(key, [])
        if not isinstance(entries, list):
            continue
        for item in entries:
            if not isinstance(item, dict):
                continue
            result.append({
                "relation_field": key,
                "type": item.get("type"),
                "doi": normalize_doi(item.get("DOI")),
                "source": item.get("source"),
                "label": item.get("label"),
                "updated": item.get("updated", {}).get("date-time") if isinstance(item.get("updated"), dict) else None,
            })
    # Crossref also exposes 'relation'; preserve keys for later source inspection.
    relation = work.get("relation", {})
    return result, sorted(relation) if isinstance(relation, dict) else []


def parse_payload(expected_doi, raw):
    try:
        payload = json.loads(raw)
        work = payload["message"]
        if not isinstance(work, dict):
            raise ValueError("message not an object")
    except (ValueError, TypeError, KeyError) as exc:
        return {"status": "malformed_response", "error": type(exc).__name__}
    recorded = normalize_doi(work.get("DOI"))
    notices, relations = update_notices(work)
    title = title_text(work)
    return {
        "status": "matched" if expected_doi == recorded and title else "mismatch_or_incomplete",
        "crossref_doi": recorded,
        "crossref_title": title,
        "crossref_year": year_value(work),
        "crossref_type": work.get("type"),
        "crossref_container_title": (work.get("container-title") or [None])[0]
            if isinstance(work.get("container-title"), list) else None,
        "crossref_publisher": work.get("publisher"),
        "crossref_issued": work.get("issued"),
        "listed_updates": notices,
        "relation_keys": relations,
        "integrity_notice_result": "metadata_updates_present" if notices else "not_cleared",
        "peer_review_status": "unknown",
        "venue_transparency": "unknown",
    }


def lookup(doi, email=None, opener=None, sleeper=None, retries=2):
    """Pure-ish transport boundary: injectable opener/sleeper for offline tests."""
    opener = opener or urllib.request.urlopen
    sleeper = sleeper or time.sleep
    url = crossref_url(doi, email)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(retries + 1):
        try:
            with opener(req, timeout=TIMEOUT_SECONDS) as response:
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    return {"status": "oversized_response", "request_url": url}
                result = parse_payload(normalize_doi(doi), raw)
                result["raw_sha256"] = hashlib.sha256(raw).hexdigest()
                result["request_url"] = url
                return result
        except urllib.error.HTTPError as exc:
            if exc.code in RETRY_CODES and attempt < retries:
                retry_after = exc.headers.get("Retry-After", "") if exc.headers else ""
                try:
                    delay = min(4.0, max(0.5, float(retry_after)))
                except ValueError:
                    delay = min(4.0, (attempt + 1) * 1.0)
                sleeper(delay)
                continue
            return {"status": "not_found" if exc.code == 404 else "http_error",
                    "http_status": exc.code, "request_url": url}
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt < retries:
                sleeper(min(4.0, (attempt + 1) * 1.0))
                continue
            return {"status": "transport_error", "error": type(exc).__name__,
                    "request_url": url}
    return {"status": "transport_error", "request_url": url}


def select_records(catalog, limit=5, only_ids=None):
    if not 1 <= limit <= MAX_RECORDS:
        raise ValueError(f"--limit must be between 1 and {MAX_RECORDS}")
    if not isinstance(catalog, list):
        raise ValueError("catalog must be a JSON list")
    chosen = []
    seen = set()
    for row in catalog:
        if not isinstance(row, dict):
            continue
        local_id = row.get("id")
        if only_ids and local_id not in only_ids:
            continue
        doi = normalize_doi(row.get("DOI"))
        if local_id and doi and doi not in seen:
            chosen.append({"reference_id": local_id, "doi": doi,
                           "catalog_title": row.get("title", "")})
            seen.add(doi)
        if len(chosen) == limit:
            break
    if only_ids and set(only_ids) - {c["reference_id"] for c in chosen}:
        raise ValueError("one or more --ids are missing, have no DOI, or exceed --limit")
    return chosen


def run(root, live=False, limit=5, ids=None, email=None, output=None, opener=None, sleeper=None):
    root = Path(root)
    catalog_path = root / "bibliography/catalog/seed.csl.json"
    original = catalog_path.read_bytes()
    selected = select_records(json.loads(original), limit=limit, only_ids=set(ids or []))
    plan = {
        "mode": "live" if live else "dry_run",
        "catalog_sha256": hashlib.sha256(original).hexdigest(),
        "selected": selected,
        "selected_count": len(selected),
        "max_requests": len(selected) * 3 if live else 0,
        "editorial_assessment": "not_performed",
        "scientific_assessment": "not_performed",
    }
    if not live:
        return plan
    if not selected:
        raise ValueError("no DOI-bearing catalog records selected")
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
    # A timestamped run directory means prior results are never overwritten.
    run_id = now.replace(":", "").replace("-", "").replace(".", "")
    target = Path(output) if output else root / "_local/crossref"
    run_dir = target / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    records = []
    for idx, work in enumerate(selected):
        result = lookup(work["doi"], email=email, opener=opener, sleeper=sleeper)
        record = {**work, **result, "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")}
        records.append(record)
        (run_dir / f"{idx:03d}.json").write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        if idx + 1 < len(selected):
            (sleeper or time.sleep)(0.5)  # one sequential lookup at a time
    manifest = {**plan, "run_id": run_id, "retrieved_at_utc": now,
                "results": {k: sum(x["status"] == k for x in records)
                            for k in sorted({r["status"] for r in records})},
                "snapshots": [f"{i:03d}.json" for i in range(len(records))],
                "important": "No data was promoted to canonical source_integrity.csv; inspect primary records and journal notices separately."}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return {**manifest, "local_run_dir": str(run_dir)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--live", action="store_true", help="Allow bounded HTTPS requests; default is offline dry run")
    parser.add_argument("--limit", type=int, default=5, help=f"Maximum DOI records, 1..{MAX_RECORDS}")
    parser.add_argument("--ids", nargs="+", default=None, help="Specific local reference IDs")
    parser.add_argument("--email", default=None, help="Optional contact email for Crossref polite pool; not saved in canonical metadata")
    parser.add_argument("--output", type=Path, default=None, help="Local snapshot parent directory; default _local/crossref")
    options = parser.parse_args()
    try:
        result = run(options.root, live=options.live, limit=options.limit, ids=options.ids,
                     email=options.email, output=options.output)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
