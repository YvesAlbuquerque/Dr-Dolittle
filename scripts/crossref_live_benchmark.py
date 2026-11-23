#!/usr/bin/env python3
"""Small opt-in live Crossref benchmark: provenance and editorial-update detection.

No AI model, no biological grading, no changes to canonical bibliography.
Dry run by default; --live triggers at most six sequential Crossref DOI requests.
"""
import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

try:
    from .crossref_metadata_worker import lookup
except ImportError:
    from crossref_metadata_worker import lookup

# Source-backed challenge cases, including known Crossref metadata *gaps*.
# A retraction without an update link is NOT a negative ground truth.
CASES = [
    {
        "case": "vervet_alarm_study",
        "doi": "10.1126/science.7433999",
        "kind": "ordinary_catalog_doi",
        "context": "R1 catalog paper; test DOI response and metadata only",
        "expected": "match_or_explicit_error",
    },
    {
        "case": "horse_snort_study",
        "doi": "10.1371/journal.pone.0197898",
        "kind": "ordinary_catalog_doi",
        "context": "R1 catalog paper; test DOI response and metadata only",
        "expected": "match_or_explicit_error",
    },
    {
        "case": "known_retraction_recorded",
        "doi": "10.1021/am300292v",
        "kind": "known_retracted_article_crossref_positive_control",
        "context": "Crossref itself documents updated-by retraction-watch for this article",
        "expected": "updated-by retraction present",
        "ground_truth_url": "https://community.crossref.org/t/deprecating-retraction-watch-annotations-in-the-labs-api/15884",
    },
    {
        "case": "known_retraction_metadata_gap",
        "doi": "10.33263/BRIAC94.979986",
        "kind": "known_retraction_metadata_gap",
        "context": "Crossref community discussion 2026 describes a Retraction Watch record without a linked Crossref update",
        "expected": "do not issue no-retraction verdict from missing updates",
        "ground_truth_url": "https://community.crossref.org/t/rwdb-record-62686-10-33263-briac94-979986-retraction-recorded-in-retraction-watch-but-absent-from-crossref-metadata/16586",
    },
    {
        "case": "known_correction_metadata_gap",
        "doi": "10.1029/2001RG000106",
        "kind": "publisher_correction_metadata_gap",
        "context": "Crossref community discussion says correction notices may have separate unlinked DOI",
        "expected": "do not issue no-correction verdict from missing updates",
        "ground_truth_url": "https://community.crossref.org/t/rwdb-record-62686-10-33263-briac94-979986-retraction-recorded-in-retraction-watch-but-absent-from-crossref-metadata/16586",
    },
    {
        "case": "nonexistent_doi_negative_control",
        "doi": "10.9999/dr-dolittle-nonexistent-2026-11-23",
        "kind": "invalid_or_unregistered_control",
        "context": "Constructed test input; if registered unexpectedly, report mismatch rather than overwrite",
        "expected": "not_found_or_explicit_error",
    },
]


def summarize(record):
    status = record.get("status")
    types = [str(x.get("type", "")).lower() for x in record.get("listed_updates", [])]
    positive_control = record.get("case") == "known_retraction_recorded"
    detected = "retraction" in types
    return {
        "case": record["case"],
        "doi": record["doi"],
        "kind": record["kind"],
        "status": status,
        "crossref_doi": record.get("crossref_doi"),
        "crossref_title": record.get("crossref_title"),
        "crossref_type": record.get("crossref_type"),
        "update_types": types,
        "retraction_detected": detected,
        "title_retraction_flag_present": bool(record.get("title_retraction_flag_present")),
        "integrity_notice_result": record.get("integrity_notice_result"),
        "expected": record["expected"],
        "positive_control_pass": detected and status == "matched" if positive_control else None,
        "metadata_clears_no_retraction": False,
        "ground_truth_url": record.get("ground_truth_url"),
        "error": record.get("error"),
        "http_status": record.get("http_status"),
    }


def benchmark(live=False, destination=None, sleeper=None, transport=None):
    if not live:
        return {
            "mode": "dry_run",
            "case_count": len(CASES),
            "cases": [{k:v for k,v in c.items() if k in ("case", "doi", "kind", "expected")} for c in CASES],
            "real_requests": 0,
        }
    if destination is None:
        raise ValueError("--output is required for live runs")
    target = Path(destination)
    if target.exists():
        raise FileExistsError("Output directory already exists; refusing to overwrite benchmark snapshot")
    target.mkdir(parents=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    full = []
    for i, c in enumerate(CASES):
        kwargs = {"sleeper": sleeper}
        if transport:
            kwargs["opener"] = transport
        result = lookup(c["doi"], **kwargs)
        record = {**c, **result, "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")}
        full.append(record)
        # One record per file supports exact audit and source-provenance inspection.
        (target / f"{i:02d}-{c['case']}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if i+1 < len(CASES):
            (sleeper or time.sleep)(0.6)
    rows = [summarize(r) for r in full]
    pass_control = next(x["positive_control_pass"] for x in rows if x["case"] == "known_retraction_recorded")
    matched_count = sum(r["status"] == "matched" for r in rows)
    summary = {
        "mode": "live",
        "started_at_utc": started,
        "completed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_api": "https://api.crossref.org/works/{doi}",
        "case_count": len(rows),
        "matched_count": matched_count,
        "retraction_positive_control_pass": pass_control,
        "note": "Missing Crossref updates cannot clear a paper; correction and retraction gaps are tracked separately.",
        "scientific_certainty_assigned": False,
        "canonical_data_mutated": False,
        "results": rows,
    }
    (target / "benchmark-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Opt in to six real HTTPS API queries")
    parser.add_argument("--output", type=Path, help="Unique artifact directory, must not already exist")
    args = parser.parse_args()
    try:
        result = benchmark(args.live, args.output)
    except (OSError, ValueError) as e:
        print(json.dumps({"error":str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    # Sentinel detects regression in update-field parsing; other network failures are reported,
    # not misclassified as biologically clean metadata.
    if args.live and not result["retraction_positive_control_pass"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
