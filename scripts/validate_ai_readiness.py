#!/usr/bin/env python3
"""Validate staged AI-science provenance without pretending to verify scientific truth.

R1: deterministic integrity checks only. No LLM scoring or network access.
Run: python scripts/validate_ai_readiness.py
"""
import argparse
import csv
import datetime as dt
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

INTEGRITY_STATES = {"not_checked", "checked", "indeterminate", "flagged"}
PEER_STATES = {"unknown", "peer_review_documented", "not_peer_reviewed", "not_applicable"}
VENUE_STATES = {"unknown", "transparent_process_documented", "concerns_documented", "not_applicable"}
NOTICE_STATES = {"not_checked", "no_notice_found_at_check", "correction", "retraction", "expression_of_concern", "multiple_or_conflicting_notices"}
RUN_STATES = {"pending", "completed", "failed", "abstained"}
RUN_TYPES = {"metadata_verification", "source_extraction", "appraisal", "synthesis", "calibration"}
PROPOSAL_STATES = {"draft", "flagged", "withdrawn", "superseded"}
DOMAIN_STATES = {"low_concern", "some_concern", "high_concern", "unclear", "not_applicable"}
CONJECTURE_STATES = {"idea", "testable", "under_investigation", "not_supported_yet", "disconfirmed_in_tested_scope", "superseded", "withdrawn"}
SHA256 = re.compile(r"^[0-9a-f]{64}$", re.I)


def read(path, errors):
    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                errors.append(f"{path}: missing header")
                return []
            data = list(reader)
            for i, r in enumerate(data, 2):
                if None in r or any(value is None for value in r.values()):
                    errors.append(f"{path}:{i}: malformed columns")
            return data
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append(f"{path}: {exc}")
        return []


def unique(rows, field, errors):
    values = [r.get(field, "") for r in rows]
    for key, n in Counter(values).items():
        if not key or n > 1:
            errors.append(f"{field}: missing or repeated value {key!r}")
    return set(values)


def valid_date(value):
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return bool(re.search(r"(Z|[+-][0-9]{2}:[0-9]{2})$", value))
    except (ValueError, AttributeError):
        return False


def valid_url(value):
    try:
        result = urlparse(value)
        return result.scheme == "https" and bool(result.netloc)
    except (ValueError, TypeError):
        return False


def validate(root):
    root = Path(root)
    errors, warnings = [], []
    try:
        catalog = json.loads((root / "bibliography/catalog/seed.csl.json").read_text(encoding="utf-8"))
        bib_ids = {item["id"] for item in catalog}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        catalog, bib_ids = [], set()
        errors.append(f"cannot read CSL bibliography: {exc}")
    assertions = read(root / "data/evidence/assertions.csv", errors)
    hypothesis_records = read(root / "data/evidence/hypotheses.csv", errors)
    existing_appraisals = read(root / "data/evidence/study_appraisals.csv", errors)
    integrity = read(root / "data/bibliography/source_integrity.csv", errors)
    runs = read(root / "data/ai/assessment_runs.csv", errors)
    proposals = read(root / "data/ai/appraisal_proposals.csv", errors)
    conjectures = read(root / "data/research/conjectures.csv", errors)
    assertion_ids = {r.get("assertion_id") for r in assertions}
    hypothesis_ids = {r.get("hypothesis_id") for r in hypothesis_records}
    appraisal_pairs = {(r.get("appraisal_id"), r.get("assertion_id"), r.get("reference_id")) for r in existing_appraisals}

    integrity_ids = unique(integrity, "reference_id", errors)
    if bib_ids != integrity_ids:
        errors.append(f"source integrity index mismatch: missing={sorted(bib_ids-integrity_ids)} extra={sorted(integrity_ids-bib_ids)}")
    for row in integrity:
        ref = row.get("reference_id", "")
        state = row.get("verification_status", "")
        if state not in INTEGRITY_STATES:
            errors.append(f"{ref}: invalid verification_status")
        if row.get("peer_review_status") not in PEER_STATES:
            errors.append(f"{ref}: invalid peer review metadata")
        if row.get("venue_transparency") not in VENUE_STATES:
            errors.append(f"{ref}: invalid venue metadata")
        if row.get("integrity_notice") not in NOTICE_STATES:
            errors.append(f"{ref}: invalid integrity notice")
        if state == "not_checked":
            for field in ("checked_at_utc", "peer_review_evidence_uri", "venue_evidence_uri",
                          "integrity_notice_uri", "integrity_check_source", "rationale"):
                if (row.get(field) or "").strip():
                    errors.append(f"{ref}: not_checked may not claim verification details")
            if row.get("peer_review_status") != "unknown" or row.get("venue_transparency") != "unknown" or row.get("integrity_notice") != "not_checked":
                errors.append(f"{ref}: not_checked cannot assert source/editorial integrity")
        else:
            if not valid_date(row.get("checked_at_utc")) or not (row.get("rationale") or "").strip():
                errors.append(f"{ref}: checked integrity needs UTC timestamp and rationale")
            if not (row.get("integrity_check_source") or "").strip():
                errors.append(f"{ref}: checked integrity missing verification service")
            for value_field, evidence_field, empty_state in (
                ("peer_review_status", "peer_review_evidence_uri", "unknown"),
                ("venue_transparency", "venue_evidence_uri", "unknown"),
                ("integrity_notice", "integrity_notice_uri", "not_checked")
            ):
                if row.get(value_field) not in (empty_state, "no_notice_found_at_check", "not_applicable") and not valid_url(row.get(evidence_field)):
                    errors.append(f"{ref}: {value_field} requires directly linkable provenance")
            if row.get("integrity_notice") == "no_notice_found_at_check" and not row.get("integrity_check_source"):
                errors.append(f"{ref}: no notice found needs exact checking service")
    run_ids = unique(runs, "run_id", errors)
    for row in runs:
        key = row.get("run_id", "")
        if row.get("task_type") not in RUN_TYPES or row.get("status") not in RUN_STATES:
            errors.append(f"{key}: unsupported run type/status")
        if row.get("status") == "completed":
            for field in ("model_provider", "model_id", "model_version", "prompt_version",
                          "started_at_utc", "finished_at_utc", "source_snapshot_hash", "code_commit"):
                if not (row.get(field) or "").strip():
                    errors.append(f"{key}: completed AI run missing {field}")
            for field in ("started_at_utc", "finished_at_utc"):
                if not valid_date(row.get(field)):
                    errors.append(f"{key}: invalid {field}")
            if not SHA256.fullmatch(row.get("source_snapshot_hash") or ""):
                errors.append(f"{key}: source snapshot hash must be SHA-256")
    unique(proposals, "proposal_id", errors)
    for row in proposals:
        key = row.get("proposal_id", "")
        if row.get("run_id") not in run_ids:
            errors.append(f"{key}: proposal has no known provenance run")
        pair = (row.get("appraisal_id"), row.get("assertion_id"), row.get("source_reference_id"))
        if pair not in appraisal_pairs:
            errors.append(f"{key}: proposal refers to unknown appraisal/observation/source")
        if row.get("judgement") not in DOMAIN_STATES:
            errors.append(f"{key}: invalid proposed methodological judgement")
        if row.get("domain") not in {"risk_of_bias", "measurement_validity", "controls_confounding",
                "precision", "reporting_completeness", "directness", "reproducibility"}:
            errors.append(f"{key}: unknown appraisal domain")
        if row.get("status") not in PROPOSAL_STATES:
            errors.append(f"{key}: invalid proposal status")
        for field in ("evidence_location", "source_snapshot_hash", "reasoning_summary"):
            if not (row.get(field) or "").strip():
                errors.append(f"{key}: missing source-grounded detail {field}")
        if not SHA256.fullmatch(row.get("source_snapshot_hash") or ""):
            errors.append(f"{key}: invalid evidence source snapshot SHA-256")
        # This table is strictly proposals; it cannot directly certify a scientific claim.
    conjecture_ids = unique(conjectures, "conjecture_id", errors)
    for row in conjectures:
        key, state = row.get("conjecture_id", ""), row.get("state", "")
        if state not in CONJECTURE_STATES:
            errors.append(f"{key}: invalid conjecture state")
        for field in ("created_at_utc", "statement", "scope", "origin_kind"):
            if not (row.get(field) or "").strip():
                errors.append(f"{key}: missing {field}")
        if row.get("created_at_utc") and not valid_date(row.get("created_at_utc")):
            errors.append(f"{key}: invalid conjecture date")
        if row.get("linked_hypothesis_id") and row.get("linked_hypothesis_id") not in hypothesis_ids:
            errors.append(f"{key}: linked hypothesis does not exist")
        if state in {"testable", "under_investigation", "disconfirmed_in_tested_scope"}:
            if not (row.get("testable_prediction") or "").strip() or not (row.get("disconfirming_test") or "").strip():
                errors.append(f"{key}: testable conjecture requires prediction and a disconfirmation test")
        if state in {"disconfirmed_in_tested_scope", "superseded", "withdrawn"} and not (row.get("revision_reason") or "").strip():
            errors.append(f"{key}: terminal/revised conjecture requires reason")
        if row.get("supersedes_id") and row.get("supersedes_id") not in conjecture_ids:
            errors.append(f"{key}: supersedes nonexistent conjecture")
    return {
        "source_integrity_rows": len(integrity),
        "unchecked_sources": sum(r.get("verification_status") == "not_checked" for r in integrity),
        "ai_runs": len(runs),
        "ai_appraisal_proposals": len(proposals),
        "conjectures": len(conjectures),
        "errors": errors,
        "warnings": warnings,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("."))
    args = p.parse_args()
    result = validate(args.root)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return bool(result["errors"])


if __name__ == "__main__":
    raise SystemExit(main())
