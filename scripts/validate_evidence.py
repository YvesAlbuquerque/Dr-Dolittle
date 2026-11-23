#!/usr/bin/env python3
"""Validate the provisional R1 evidence pilot and its source/provenance relations.

This is a structural validator, not independent scientific or taxonomic review.
Run from the repository root: python scripts/validate_evidence.py
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

RELATIONS = {
    "assertion_sources.csv": ("reference_id", "bibliography"),
    "assertion_capabilities.csv": ("capability_id", "capabilities.csv"),
    "assertion_modalities.csv": ("modality_id", "modalities.csv"),
    "assertion_phenomena.csv": ("phenomenon_id", "phenomenon_families.csv"),
    "assertion_physiological_markers.csv": ("family_id", "physiological_marker_families.csv"),
}
EVIDENCE_STATES = {"documented_presence", "documented_absence_under_test", "insufficient"}
REVIEW_STATES = {"draft_unreviewed", "source_checked", "reviewed"}


def load_csv(path, errors):
    try:
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                errors.append(f"{path}: missing header")
                return []
            rows = list(reader)
            if any(None in row or any(value is None for value in row.values()) for row in rows):
                errors.append(f"{path}: malformed CSV fields")
            return rows
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append(f"{path}: {exc}")
        return []


def validate(root):
    root = Path(root)
    errors, warnings = [], []
    base = root / "data" / "evidence"
    ontology = root / "data" / "ontology"
    try:
        bib = json.loads((root / "bibliography/catalog/seed.csl.json").read_text(encoding="utf-8"))
        references = {r["id"] for r in bib}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        references = set()
        errors.append(f"cannot load bibliography: {exc}")

    assertions = load_csv(base / "assertions.csv", errors)
    ids = [r.get("assertion_id", "") for r in assertions]
    if not assertions:
        errors.append("R1 pilot contains no assertions")
    errors.extend(f"duplicate assertion ID: {key}" for key, count in Counter(ids).items() if count > 1)
    if any(not key for key in ids):
        errors.append("empty assertion ID")
    source_ids = set(ids)

    for r in assertions:
        key = r.get("assertion_id", "")
        for field in ("claim", "claim_kind", "context", "methodology", "limitations", "classification_version", "review_status"):
            if not (r.get(field) or "").strip():
                errors.append(f"{key}: missing {field}")
        if r.get("evidence_state") not in EVIDENCE_STATES:
            errors.append(f"{key}: invalid atomic evidence state {r.get('evidence_state')}; conflicting/not_assessed are synthesis/coverage states")
        if r.get("review_status") not in REVIEW_STATES:
            errors.append(f"{key}: invalid review status")
        if r.get("evidence_state") == "documented_absence_under_test" and not (r.get("context") and r.get("methodology")):
            errors.append(f"{key}: absence under test requires specified test and context")
        if r.get("review_status") == "reviewed":
            warnings.append(f"{key}: manually confirm that an independent human actually reviewed the primary source")

    vocabs = {}
    for name, path, code in [
        ("capabilities.csv", ontology / "capabilities.csv", "capability_id"),
        ("modalities.csv", ontology / "modalities.csv", "modality_id"),
        ("phenomenon_families.csv", ontology / "phenomenon_families.csv", "phenomenon_id"),
        ("physiological_marker_families.csv", ontology / "physiological_marker_families.csv", "family_id"),
    ]:
        records = load_csv(path, errors)
        values = [r.get(code, "") for r in records]
        if any(not item for item in values) or len(values) != len(set(values)):
            errors.append(f"{name}: blank or duplicate code")
        vocabs[name] = set(values)

    links = {}
    for filename, (target_field, vocabulary) in RELATIONS.items():
        rows = load_csv(base / filename, errors)
        links[filename] = rows
        for r in rows:
            key = r.get("assertion_id", "")
            if key not in source_ids:
                errors.append(f"{filename}: orphan assertion ID {key}")
            target = r.get(target_field, "")
            valid = references if vocabulary == "bibliography" else vocabs.get(vocabulary, set())
            if target not in valid:
                errors.append(f"{filename}: unknown {target_field} {target}")
            if filename == "assertion_sources.csv" and not (r.get("source_location") or "").strip():
                errors.append(f"{key}: source location missing")
            if filename == "assertion_physiological_markers.csv":
                if not r.get("marker_or_analyte") or not r.get("measurement_method") or not r.get("source_location"):
                    errors.append(f"{key}: incomplete biomarker measurement provenance")
    for key in ids:
        if not any(row.get("assertion_id") == key for row in links.get("assertion_sources.csv", [])):
            errors.append(f"{key}: no reference link")
        if not any(row.get("assertion_id") == key for row in links.get("assertion_phenomena.csv", [])):
            errors.append(f"{key}: no phenomenon link")

    for filename in ("assertion_sampling_scope.csv", "assertion_screening.csv", "assertion_interpretations.csv", "reviews.csv"):
        rows = load_csv(base / filename, errors)
        keys = [r.get("assertion_id", "") for r in rows]
        for key in keys:
            if key not in source_ids:
                errors.append(f"{filename}: orphan assertion ID {key}")
        if filename in ("assertion_sampling_scope.csv", "assertion_screening.csv", "assertion_interpretations.csv"):
            for key in ids:
                if key not in keys:
                    errors.append(f"{filename}: no record for {key}")
        if filename == "assertion_screening.csv":
            for r in rows:
                if r.get("source_access_level") not in ("full_html", "abstract_only"):
                    errors.append(f"{r.get('assertion_id')}: invalid source access")
                url = r.get("source_access_url", "")
                if urlparse(url).scheme != "https" or not urlparse(url).netloc:
                    errors.append(f"{r.get('assertion_id')}: missing or non-HTTPS source")
                if r.get("independent_review") != "none":
                    warnings.append(f"{r.get('assertion_id')}: independent-review metadata needs external verification")
        if filename == "assertion_sampling_scope.csv":
            for r in rows:
                if not r.get("sampling_group") or not r.get("unit_of_inference"):
                    errors.append(f"{r.get('assertion_id')}: missing sampling group/scope")
                if r.get("taxonomy_authority_status") != "not_yet_matched_to_pinned_COL":
                    warnings.append(f"{r.get('assertion_id')}: check taxonomy source/release before claiming pinned taxon ID")

    if any(r.get("review_status") != "draft_unreviewed" for r in assertions):
        warnings.append("pilot chart may only show draft records when the visualization labels are accurate")

    return {"assertions": len(assertions), "references_linked": len(links.get("assertion_sources.csv", [])),
            "physiological_links": len(links.get("assertion_physiological_markers.csv", [])),
            "errors": errors, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    report = validate(args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return bool(report["errors"])


if __name__ == "__main__":
    raise SystemExit(main())
