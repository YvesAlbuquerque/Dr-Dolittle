#!/usr/bin/env python3
"""Audit source and AI proposal runs. Counts structural validity, NOT scientific correctness."""
import argparse
import json
from pathlib import Path

EXPECTED = {"r1-001", "r1-006", "r1-009", "r1-013"}

def summarize(root):
    root = Path(root)
    manifest = json.loads((root/"manifest.json").read_text(encoding="utf-8"))
    rows = manifest["results"]
    ids = {r["id"] for r in rows}
    if len(rows) != len(ids) or not ids or ids - EXPECTED:
        raise ValueError("invalid study coverage or duplicate IDs")
    total = len(rows)
    available = sum(r.get("source_access") in ("full_text", "abstract") for r in rows)
    full = sum(r.get("source_access") == "full_text" for r in rows)
    attempts = sum((root/r["id"]/"model-proposal.json").exists() for r in rows)
    source_errors = [r["id"] for r in rows if r.get("source_status") == "error"]
    validated = sum(r.get("methodology_proposal_status") == "draft_validated_structurally" for r in rows)
    rejected = sum(r.get("methodology_proposal_status") == "draft_rejected" for r in rows)
    model_errors = sum(r.get("methodology_proposal_status") == "model_error" for r in rows)
    abstentions = 0
    quote_errors = 0
    for r in rows:
        f = root / r["id"] / "model-proposal.json"
        if not f.exists(): continue
        proposal = json.loads(f.read_text(encoding="utf-8"))
        draft = proposal.get("draft", {})
        abstentions += bool(draft.get("abstain_from_method_appraisal")) if isinstance(draft, dict) else 0
        quote_errors += sum("quote" in s for s in proposal.get("validation_errors", []))
    return {
        "studies":total, "sources_available":available, "full_text_sources":full,
        "abstract_only_sources":available-full, "source_errors":source_errors,
        "ai_proposals_attempted": attempts, "structurally_valid_proposals":validated,
        "rejected_proposals":rejected,"model_errors":model_errors,
        "model_declared_abstentions":abstentions,
        "quote_validation_failures":quote_errors,
        "scientific_extraction_accuracy":"not_measured_without_independent_gold_standard",
        "scientific_confidence_certified":False,
        "model_equivalent_to_expert_review":False,
        "technical_gate": "pass" if available >= 2 else "insufficient_sources",
        "conclusion": "No hypothesis claims may be promoted from this first uncalibrated execution",
    }

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("run_dir",type=Path)
    args=p.parse_args()
    m=summarize(args.run_dir)
    (args.run_dir/"evaluation.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(m,ensure_ascii=False,indent=2))
    raise SystemExit(m["technical_gate"] != "pass")
