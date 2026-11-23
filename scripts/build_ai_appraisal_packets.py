#!/usr/bin/env python3
"""Build source-grounded methodological appraisal input packets for human or AI critique.

No network, no AI calls, no scientific grading, and no mutation of canonical evidence.
Usage:
  python scripts/build_ai_appraisal_packets.py --ids r1-001 r1-006 r1-009 r1-013
  python scripts/build_ai_appraisal_packets.py --ids r1-013 --output _local/ai-packets/r1-013.json
"""
import argparse
import csv
import json
from pathlib import Path

DOMAINS = [
    "source_access_and_fidelity", "risk_of_bias", "measurement_validity",
    "controls_confounding", "precision", "reporting_completeness",
    "directness", "reproducibility",
]
DEFAULT_IDS = ["r1-001", "r1-006", "r1-009", "r1-013"]


def load(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def indexed(rows, key):
    result = {}
    for row in rows:
        value = row.get(key)
        if not value or value in result:
            raise ValueError(f"blank or duplicate {key}: {value!r}")
        result[value] = row
    return result


def generate(root, ids=None):
    root = Path(root)
    base = root / "data/evidence"
    catalog = indexed(json.loads((root / "bibliography/catalog/seed.csl.json").read_text(encoding="utf-8")), "id")
    assertions = indexed(load(base / "assertions.csv"), "assertion_id")
    screen = indexed(load(base / "assertion_screening.csv"), "assertion_id")
    sources = load(base / "assertion_sources.csv")
    appraisals = indexed(load(base / "study_appraisals.csv"), "assertion_id")
    selected = ids or DEFAULT_IDS
    if len(selected) != len(set(selected)):
        raise ValueError("duplicate requested assertion ID")
    packets = []
    for aid in selected:
        if aid not in assertions or aid not in screen or aid not in appraisals:
            raise ValueError(f"unknown or incompletely linked study assertion {aid!r}")
        relevant = [s for s in sources if s.get("assertion_id") == aid]
        if len(relevant) != 1:
            raise ValueError(f"pilot expects one primary source per assertion, got {len(relevant)} for {aid}")
        source = relevant[0]
        ref = catalog.get(source["reference_id"])
        if ref is None:
            raise ValueError(f"{aid}: source ID not in CSL bibliography")
        baseline = appraisals[aid]
        if baseline.get("status") != "not_assessed":
            raise ValueError(f"{aid}: packet cannot overwrite a completed study appraisal")
        access = screen[aid].get("source_access_level")
        if access not in ("abstract_only", "full_html"):
            raise ValueError(f"{aid}: unknown source access level")
        packets.append({
            "schema_version": "r1-ai-method-critic-packet-v0.1",
            "assertion_id": aid,
            "appraisal_id": baseline["appraisal_id"],
            "reference_id": ref["id"],
            "source": {
                "doi": ref.get("DOI"),
                "title": ref.get("title"),
                "url": screen[aid].get("source_access_url"),
                "access_level_at_seed_screening": access,
                "source_location_in_seed": source.get("source_location"),
                "actual_source_bytes_or_full_text_attached": False,
                "fetched_source_snapshot_sha256": None,
            },
            "draft_study_claim_not_yet_validated": assertions[aid]["claim"],
            "study_context_as_drafted": assertions[aid].get("context"),
            "methodology_as_drafted": assertions[aid].get("methodology"),
            "limitations_as_drafted": assertions[aid].get("limitations"),
            "assessment_domains": DOMAINS,
            "requirements": {
                "retrieve_source_before_assessment": True,
                "primary_methods_results_required_for_completed_appraisal": True,
                "if_only_abstract_accessible": "abstain_from_full_methods_appraisal",
                "show_independent_sample_size_and_controls_or_mark_unknown": True,
                "give_exact_section_figure_or_table_locator": True,
                "separate_observation_from_communication_meaning": True,
                "do_not_infer_truth_from_publisher_or_institution": True,
                "do_not_update_study_appraisals_or_certainty_assessments": True,
                "retain_disconfirming_and_null_studies": True,
                "output_kind": "draft_proposal_only",
            },
        })
    return {
        "protocol": "docs/ai-methodological-appraisal-prompt-v0.1.md",
        "source_text_attached": False,
        "ai_model_invoked": False,
        "scientific_confidence_assigned": False,
        "packets": packets,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--ids", nargs="+", default=None)
    parser.add_argument("--output", type=Path, default=None)
    opt = parser.parse_args()
    try:
        data = generate(opt.root, opt.ids)
        rendered = json.dumps(data, indent=2, ensure_ascii=False)+"\n"
        if opt.output is None:
            print(rendered)
        else:
            if opt.output.exists():
                raise FileExistsError(f"refusing to overwrite {opt.output}")
            opt.output.parent.mkdir(parents=True, exist_ok=True)
            opt.output.write_text(rendered, encoding="utf-8")
            print(json.dumps({"path": str(opt.output), "packets": len(data["packets"]),
                              "ai_model_invoked": False, "source_text_attached": False}))
        return 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
