"""Synthetic tests for source provenance, AI proposals, and conjecture preservation.

The test fixtures are hypothetical; no biological or editorial claims are made.
"""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripts.validate_ai_readiness import validate


class AIReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for p in ("bibliography/catalog", "data/evidence", "data/bibliography",
                  "data/ai", "data/research"):
            (self.root / p).mkdir(parents=True)
        (self.root / "bibliography/catalog/seed.csl.json").write_text(
            json.dumps([{"id":"r1", "title":"Synthetic"}]), encoding="utf-8")
        self.columns = {
            "data/evidence/assertions.csv": ["assertion_id"],
            "data/evidence/hypotheses.csv": ["hypothesis_id"],
            "data/evidence/study_appraisals.csv": ["appraisal_id","assertion_id","reference_id"],
            "data/bibliography/source_integrity.csv": [
                "reference_id", "verification_status", "checked_at_utc", "publication_type",
                "peer_review_status", "peer_review_evidence_uri", "venue_transparency",
                "venue_evidence_uri", "integrity_notice", "integrity_notice_uri",
                "integrity_check_source", "rationale"
            ],
            "data/ai/assessment_runs.csv": [
                "run_id", "task_type", "status", "model_provider", "model_id", "model_version",
                "prompt_version", "started_at_utc", "finished_at_utc",
                "source_snapshot_hash", "code_commit", "calibration_reference", "notes"
            ],
            "data/ai/appraisal_proposals.csv": [
                "proposal_id", "run_id", "assertion_id", "appraisal_id", "domain",
                "judgement", "source_reference_id", "evidence_location",
                "source_snapshot_hash", "reasoning_summary", "alternative_explanation", "status"
            ],
            "data/research/conjectures.csv": [
                "conjecture_id", "created_at_utc", "origin_kind", "origin_reference_id",
                "statement", "scope", "testable_prediction", "disconfirming_test", "state",
                "linked_hypothesis_id", "supersedes_id", "revision_reason"
            ],
        }
        self.rows = {key: [] for key in self.columns}
        self.rows["data/evidence/assertions.csv"] = [{"assertion_id":"a1"}]
        self.rows["data/evidence/study_appraisals.csv"] = [{
            "appraisal_id":"app-a1", "assertion_id":"a1","reference_id":"r1"}]
        self.rows["data/bibliography/source_integrity.csv"] = [{
            "reference_id":"r1","verification_status":"not_checked",
            "peer_review_status":"unknown", "venue_transparency":"unknown",
            "integrity_notice":"not_checked"}]
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        for path, headers in self.columns.items():
            with (self.root / path).open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.rows[path])

    def test_unknown_integrity_and_unassessed_conjectures_are_valid(self):
        self.rows["data/research/conjectures.csv"] = [{
            "conjecture_id":"c1", "created_at_utc":"2026-11-23T00:00:00Z",
            "origin_kind":"observer_hypothesis", "statement":"Hypothetical breath cue",
            "scope":"only example","state":"idea"}]
        self.save()
        x = validate(self.root)
        self.assertEqual([], x["errors"])
        self.assertEqual(1, x["unchecked_sources"])
        self.assertEqual(1, x["conjectures"])

    def test_source_cannot_fake_checked_status(self):
        r = self.rows["data/bibliography/source_integrity.csv"][0]
        r["verification_status"] = "checked"
        r["peer_review_status"] = "peer_review_documented"
        self.save()
        self.assertIn("checked integrity needs", " ".join(validate(self.root)["errors"]))

    def test_coverage_must_match_bibliography(self):
        self.rows["data/bibliography/source_integrity.csv"] = []
        self.save()
        self.assertIn("index mismatch", " ".join(validate(self.root)["errors"]))

    def test_ai_run_cannot_claim_completed_without_manifest(self):
        self.rows["data/ai/assessment_runs.csv"] = [{
            "run_id":"run1", "status":"completed","task_type":"appraisal",
            "model_provider":"hypothetical", "model_id":"example"}]
        self.save()
        self.assertIn("completed AI run missing", " ".join(validate(self.root)["errors"]))

    def test_ai_proposal_cannot_point_to_unknown_assessment(self):
        self.rows["data/ai/appraisal_proposals.csv"] = [{
            "proposal_id":"p1","run_id":"unknown","assertion_id":"a1",
            "appraisal_id":"false", "source_reference_id":"r1",
            "domain":"risk_of_bias", "judgement":"low_concern",
            "status":"draft","evidence_location":"Abstract","reasoning_summary":"test",
            "source_snapshot_hash":"f"*64}]
        self.save()
        result = " ".join(validate(self.root)["errors"])
        self.assertIn("no known provenance run", result)
        self.assertIn("unknown appraisal", result)

    def test_disconfirmed_conjecture_needs_test_and_reason(self):
        self.rows["data/research/conjectures.csv"] = [{
            "conjecture_id":"c1","created_at_utc":"2026-11-23T00:00:00Z",
            "origin_kind":"observer_hypothesis","statement":"Hypothesis",
            "scope":"only example","state":"disconfirmed_in_tested_scope"}]
        self.save()
        result = " ".join(validate(self.root)["errors"])
        self.assertIn("disconfirmation test", result)
        self.assertIn("requires reason", result)


if __name__ == "__main__":
    unittest.main()
