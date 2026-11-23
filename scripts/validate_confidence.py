#!/usr/bin/env python3
"""Validate *structure* of R1 evidence appraisals and hypothesis certainty.

No automatic biological truth score. Not-assessed must never silently become low.
Run from repository root: python scripts/validate_confidence.py
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from datetime import date

DOMAINS = ("risk_of_bias", "measurement_validity", "controls_confounding", "precision",
           "reporting_completeness", "directness", "reproducibility")
DOMAIN_VALUES = {"low_concern", "some_concern", "high_concern", "unclear", "not_applicable"}
CONFIDENCE = {"not_assessed", "very_low", "low", "moderate", "high"}
RELATIONS = {"supports", "opposes", "null", "context_only", "methodological_limit"}
ASSESSORS = {"human", "ai_assisted", "automated", "mixed"}
ASSESSMENT_DOMAINS = ("risk_of_bias", "measurement_validity", "independence",
                      "consistency", "precision", "directness", "publication_bias",
                      "phylogenetic_dependence", "alternative_explanations")


def read_csv(path, errors):
    try:
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                errors.append(f"{path}: missing header")
                return []
            rows = list(reader)
            for n, row in enumerate(rows, 2):
                if None in row or any(x is None for x in row.values()):
                    errors.append(f"{path}:{n}: malformed CSV row")
            return rows
    except (OSError, csv.Error, UnicodeError) as e:
        errors.append(f"{path}: cannot read CSV: {e}")
        return []


def unique(rows, field, errors, label):
    vals = [r.get(field, "") for r in rows]
    for key, n in Counter(vals).items():
        if n > 1 or not key:
            errors.append(f"{label}: duplicate or empty {field}: {key!r}")
    return set(vals)


def check_date(value):
    try:
        return date.fromisoformat(value).isoformat() == value
    except (TypeError, ValueError):
        return False


def validate(root):
    root = Path(root)
    errs, warnings = [], []
    base = root / "data/evidence"
    original = read_csv(base / "assertions.csv", errs)
    sources = read_csv(base / "assertion_sources.csv", errs)
    screening = read_csv(base / "assertion_screening.csv", errs)
    appraisals = read_csv(base / "study_appraisals.csv", errs)
    hypotheses = read_csv(base / "hypotheses.csv", errs)
    links = read_csv(base / "hypothesis_evidence.csv", errs)
    assessments = read_csv(base / "certainty_assessments.csv", errs)
    try:
        bibliography = json.loads((root / "bibliography/catalog/seed.csl.json").read_text(encoding="utf-8"))
        references = {r["id"] for r in bibliography}
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errs.append(f"bibliography: {exc}")
        references = set()

    aid = unique(original, "assertion_id", errs, "assertions")
    unique(appraisals, "appraisal_id", errs, "appraisals")
    hid = unique(hypotheses, "hypothesis_id", errs, "hypotheses")
    unique(assessments, "assessment_id", errs, "certainty assessments")
    # Empty hypothesis/assessment collections are valid and expected in the pilot.
    if not hypotheses:
        hid = set()
    if not assessments:
        pass
    screening_by_id = {r.get("assertion_id"): r for r in screening}
    source_links = {(r.get("assertion_id"), r.get("reference_id")) for r in sources}
    appraisal_by_key = {}
    for r in appraisals:
        key = r.get("assertion_id", "")
        ref = r.get("reference_id", "")
        if key not in aid or ref not in references or (key, ref) not in source_links:
            errs.append(f"appraisal {r.get('appraisal_id')}: invalid assertion/reference link")
        if (key, ref) in appraisal_by_key:
            errs.append(f"appraisal: duplicate assertion/reference pair {key}/{ref}")
        appraisal_by_key[(key, ref)] = r
        status = r.get("status")
        if status not in {"not_assessed", "appraised"}:
            errs.append(f"appraisal {key}: unknown status")
        if status == "not_assessed":
            if any(r.get(field, "").strip() for field in DOMAINS):
                errs.append(f"appraisal {key}: not_assessed may not contain domain judgments")
            if r.get("assessor_kind", "").strip() or r.get("assessed_on", "").strip():
                errs.append(f"appraisal {key}: not_assessed cannot claim an assessor/date")
        elif status == "appraised":
            for field in DOMAINS:
                if r.get(field) not in DOMAIN_VALUES:
                    errs.append(f"appraisal {key}: missing or invalid {field}")
            for field in ("assessment_method", "assessor_id", "evidence_location", "rationale"):
                if not (r.get(field) or "").strip():
                    errs.append(f"appraisal {key}: missing {field}")
            if r.get("assessor_kind") not in ASSESSORS or not check_date(r.get("assessed_on")):
                errs.append(f"appraisal {key}: invalid assessor provenance or date")
            if screening_by_id.get(key, {}).get("source_access_level") == "abstract_only":
                errs.append(f"appraisal {key}: abstract-only pilot access insufficient for method-level appraisal; update screening after examining full methods")
    if {k for k, _ in appraisal_by_key} != aid:
        errs.append("Every source-reported pilot assertion must have a study appraisal record (not_assessed placeholder is valid)")

    for r in hypotheses:
        key = r.get("hypothesis_id", "")
        for field in ("statement", "testable_outcome", "unit_of_inference", "falsification_criteria"):
            if not (r.get(field) or "").strip():
                errs.append(f"hypothesis {key}: missing {field}")
        if r.get("status") not in {"proposed", "active", "superseded", "withdrawn"}:
            errs.append(f"hypothesis {key}: invalid status")
    evidence = {}
    for r in links:
        key, ref = r.get("hypothesis_id"), r.get("assertion_id")
        if key not in hid or ref not in aid:
            errs.append(f"hypothesis evidence: broken link {key}/{ref}")
        if r.get("relation") not in RELATIONS:
            errs.append(f"hypothesis evidence: invalid relation for {key}/{ref}")
        if not (r.get("linkage_rationale") or "").strip():
            errs.append(f"hypothesis evidence: missing rationale for {key}/{ref}")
        evidence.setdefault(key, []).append(r)

    assessments_by_id = {r.get("assessment_id"): r for r in assessments}
    for r in assessments:
        key, level, ident = r.get("hypothesis_id"), r.get("level"), r.get("assessment_id")
        if key not in hid:
            errs.append(f"certainty {ident}: unknown hypothesis")
        if level not in CONFIDENCE:
            errs.append(f"certainty {ident}: invalid level")
        try:
            if int(r.get("assessment_version", "")) < 1:
                raise ValueError()
        except (ValueError, TypeError):
            errs.append(f"certainty {ident}: version must be positive integer")
        prev = r.get("supersedes_id", "")
        if prev:
            earlier = assessments_by_id.get(prev)
            if not earlier or earlier.get("hypothesis_id") != key or prev == ident:
                errs.append(f"certainty {ident}: invalid supersedes_id")
        if level == "not_assessed":
            if any((r.get(field) or "").strip() for field in ASSESSMENT_DOMAINS):
                errs.append(f"certainty {ident}: not_assessed must not contain a synthesis evaluation")
            continue
        # Ratings require an inspectable argument grounded in source-specific appraisals.
        for field in ("assessment_method", "assessor_id", "assessor_kind", "assessed_on", "reason", "source_set"):
            if not (r.get(field) or "").strip():
                errs.append(f"certainty {ident}: assessed certainty missing {field}")
        if r.get("assessor_kind") not in ASSESSORS or not check_date(r.get("assessed_on")):
            errs.append(f"certainty {ident}: invalid assessor provenance/date")
        if any(not (r.get(field) or "").strip() for field in ASSESSMENT_DOMAINS):
            errs.append(f"certainty {ident}: all synthesis considerations must be explicitly addressed or marked not_applicable with reason")
        supported = evidence.get(key, [])
        if not supported:
            errs.append(f"certainty {ident}: no linked evidence")
            continue
        for ref in (r.get("source_set") or "").split(";"):
            if ref not in references:
                errs.append(f"certainty {ident}: unknown source reference {ref!r}")
        appraised = []
        for link in supported:
            a = link.get("assertion_id")
            appraised.extend(v for (key2, _), v in appraisal_by_key.items()
                             if key2 == a and v.get("status") == "appraised")
        if not appraised:
            errs.append(f"certainty {ident}: no method-appraised supporting or opposing evidence")
        if level == "high":
            clusters = {x.get("independence_cluster") for x in supported
                        if x.get("independence_cluster")}
            if len(clusters) < 2:
                errs.append(f"certainty {ident}: high certainty needs at least two explicitly distinct independently justified study clusters")
        if level in {"moderate", "high"} and any(not l.get("independence_cluster")
                                                for l in supported if l.get("relation") in {"supports", "opposes", "null"}):
            errs.append(f"certainty {ident}: independence not characterized for material evidence")
    return {"assertions": len(original), "study_appraisals": len(appraisals),
            "completed_study_appraisals": sum(a.get("status") == "appraised" for a in appraisals),
            "hypotheses": len(hypotheses), "certainty_assessments": len(assessments),
            "errors": errs, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    result = validate(args.root)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
