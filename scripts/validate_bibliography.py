#!/usr/bin/env python3
"""Offline, dependency-free integrity checks for the Dr. Dolittle CSL seed catalog."""
import argparse
import csv
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

DOI = re.compile(r"^10\.\d{4,9}/\S+$", re.I)
STAGES = {
    "discovered", "metadata_checked", "title_abstract_screened",
    "full_text_assessed", "evidence_extracted", "independently_reviewed", "excluded",
}
META_STATES = {"partial_metadata", "checked", "verified", "needs_correction"}
REQUIRED_STATUS = {"reference_id", "screening_status", "metadata_status", "source_provenance", "checked_on"}


def validate(catalog_path: Path, status_path: Path):
    errors, warnings = [], []
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as ex:
        return {"errors": [f"catalog unreadable: {ex}"], "warnings": [], "references": 0, "statuses": 0}
    if not isinstance(catalog, list):
        return {"errors": ["catalog must be a CSL JSON array"], "warnings": [], "references": 0, "statuses": 0}
    ids, dois = [], []
    for n, entry in enumerate(catalog, 1):
        if not isinstance(entry, dict):
            errors.append(f"entry {n} is not an object")
            continue
        key = entry.get("id")
        if not isinstance(key, str) or not key.strip():
            errors.append(f"entry {n} lacks nonempty id")
            continue
        ids.append(key)
        if not isinstance(entry.get("title"), str) or not entry["title"].strip():
            errors.append(f"{key}: missing title")
        if not isinstance(entry.get("type"), str) or not entry["type"].strip():
            errors.append(f"{key}: missing CSL type")
        issued = entry.get("issued")
        year = issued.get("date-parts", [[None]]) if isinstance(issued, dict) else [[None]]
        try:
            y = year[0][0]
            if not isinstance(y, int) or y < 1500 or y > 2200:
                raise ValueError()
        except (IndexError, KeyError, TypeError, ValueError):
            errors.append(f"{key}: invalid issued date-parts year")
        rawdoi = entry.get("DOI")
        if rawdoi:
            if not isinstance(rawdoi, str) or not DOI.fullmatch(rawdoi):
                errors.append(f"{key}: malformed DOI")
            else:
                dois.append(rawdoi.lower())
        else:
            warnings.append(f"{key}: DOI missing or inapplicable; review manually")
        url = entry.get("URL")
        if not isinstance(url, str) or urlparse(url).scheme not in ("http", "https") or not urlparse(url).netloc:
            errors.append(f"{key}: missing/invalid URL")
        if not entry.get("author"):
            warnings.append(f"{key}: no structured author metadata")
    for kind, values in (("reference id", ids), ("DOI", dois)):
        for value, count in Counter(values).items():
            if count > 1:
                errors.append(f"duplicate {kind}: {value} ({count})")
    try:
        with status_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            missing = REQUIRED_STATUS - set(reader.fieldnames or ())
            if missing:
                errors.append("status missing columns: " + ", ".join(sorted(missing)))
            status = list(reader)
    except (OSError, UnicodeError, csv.Error) as ex:
        errors.append(f"status unreadable: {ex}")
        status = []
    sid = []
    for n, row in enumerate(status, 2):
        key = row.get("reference_id", "")
        if not key:
            errors.append(f"status line {n}: missing reference_id")
            continue
        sid.append(key)
        if row.get("screening_status") not in STAGES:
            errors.append(f"{key}: invalid screening_status")
        if row.get("metadata_status") not in META_STATES:
            errors.append(f"{key}: invalid metadata_status")
        if not isinstance(row.get("source_provenance"), str) or not row["source_provenance"].strip():
            errors.append(f"{key}: missing source provenance")
        try:
            dt.date.fromisoformat(row.get("checked_on", ""))
        except (TypeError, ValueError):
            errors.append(f"{key}: checked_on must be YYYY-MM-DD")
    for key, count in Counter(sid).items():
        if count > 1:
            errors.append(f"duplicate status reference_id: {key}")
    errors.extend(f"catalog record missing status: {key}" for key in sorted(set(ids) - set(sid)))
    errors.extend(f"status references unknown catalog id: {key}" for key in sorted(set(sid) - set(ids)))
    return {"references": len(catalog), "statuses": len(status),
            "doi_present": len(dois), "errors": errors, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("bibliography/catalog/seed.csl.json"))
    parser.add_argument("--status", type=Path, default=Path("bibliography/catalog/status.csv"))
    args = parser.parse_args()
    result = validate(args.catalog, args.status)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
