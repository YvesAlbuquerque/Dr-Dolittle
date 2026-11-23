"""Offline tests for source-grounded AI appraisal input packets.

These check *data preparation*, not whether an LLM's scientific critique is valid.
"""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripts.build_ai_appraisal_packets import generate


class AppraisalPacketTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for p in ("data/evidence", "bibliography/catalog"):
            (self.root / p).mkdir(parents=True)
        (self.root / "bibliography/catalog/seed.csl.json").write_text(
            json.dumps([{"id":"ref1","title":"An illustrative paper","DOI":"10.1234/test"}]),
            encoding="utf-8")
        self.write("data/evidence/assertions.csv",
                   ["assertion_id", "claim", "context", "methodology", "limitations"],
                   [["a1","Recorded behavior changes","one group","observational","small sample"]])
        self.write("data/evidence/assertion_screening.csv",
                   ["assertion_id","source_access_level","source_access_url"],
                   [["a1","abstract_only","https://example.org/abstract"]])
        self.write("data/evidence/assertion_sources.csv",
                   ["assertion_id","reference_id","source_location"],
                   [["a1","ref1","Abstract"]])
        self.write("data/evidence/study_appraisals.csv",
                   ["appraisal_id","assertion_id","reference_id","status"],
                   [["app-a1","a1","ref1","not_assessed"]])

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, headers, rows):
        with (self.root / path).open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerows(rows)

    def test_prep_packet_does_not_invent_source_text_or_confidence(self):
        x = generate(self.root, ["a1"])
        self.assertFalse(x["ai_model_invoked"])
        self.assertFalse(x["scientific_confidence_assigned"])
        self.assertFalse(x["source_text_attached"])
        p = x["packets"][0]
        self.assertEqual("abstract_only", p["source"]["access_level_at_seed_screening"])
        self.assertFalse(p["source"]["actual_source_bytes_or_full_text_attached"])
        self.assertIsNone(p["source"]["fetched_source_snapshot_sha256"])
        self.assertEqual("abstain_from_full_methods_appraisal", p["requirements"]["if_only_abstract_accessible"])
        self.assertEqual("draft_proposal_only", p["requirements"]["output_kind"])

    def test_missing_source_fails(self):
        self.write("data/evidence/assertion_sources.csv",["assertion_id","reference_id","source_location"],[])
        with self.assertRaisesRegex(ValueError, "expects one primary source"):
            generate(self.root, ["a1"])

    def test_already_appraised_cannot_be_overwritten(self):
        self.write("data/evidence/study_appraisals.csv",
                   ["appraisal_id","assertion_id","reference_id","status"],
                   [["app-a1","a1","ref1","appraised"]])
        with self.assertRaisesRegex(ValueError, "cannot overwrite"):
            generate(self.root, ["a1"])

    def test_unknown_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            generate(self.root, ["nonexistent"])

    def test_duplicate_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            generate(self.root, ["a1","a1"])


if __name__ == "__main__":
    unittest.main()
