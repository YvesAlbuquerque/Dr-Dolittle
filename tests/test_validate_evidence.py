"""Synthetic regression cases for evidence relationships. These are not biological tests."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripts.validate_evidence import validate
from scripts.build_r1_pilot_matrix import build


class EvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "data/evidence").mkdir(parents=True)
        (self.root / "data/ontology").mkdir(parents=True)
        (self.root / "bibliography/catalog").mkdir(parents=True)
        (self.root / "bibliography/catalog/seed.csl.json").write_text(
            json.dumps([{"id": "ref-x", "title": "Test paper"}]), encoding="utf-8")
        self.write("data/evidence/assertions.csv",
                   ["assertion_id","claim","claim_kind","evidence_state","context","methodology","limitations","classification_version","review_status"],
                   [["r1-test","Source reports a measured response","source_reported_observation","documented_presence","laboratory playback","playback and coding","narrow sample","pilot_r1_v0.1","draft_unreviewed"]])
        self.write("data/evidence/assertion_sources.csv",
                   ["assertion_id","reference_id","source_location","relation"], [["r1-test","ref-x","Abstract","supports_reported_observation_draft"]])
        self.write("data/evidence/assertion_capabilities.csv", ["assertion_id","capability_id"],[["r1-test","response"]])
        self.write("data/evidence/assertion_modalities.csv", ["assertion_id","modality_id"],[["r1-test","acoustic"]])
        self.write("data/evidence/assertion_phenomena.csv", ["assertion_id","phenomenon_id"],[["r1-test","playback"]])
        self.write("data/evidence/assertion_physiological_markers.csv",["assertion_id","family_id","marker_or_analyte","measurement_method","sample_matrix_or_site","time_relative_to_event","baseline_or_comparator","controls_and_confounders","source_location","interpretation_limits"],[])
        self.write("data/evidence/assertion_sampling_scope.csv",
                   ["assertion_id","sampling_group","taxon_as_published","unit_of_inference","taxonomy_authority_status"],
                   [["r1-test","birds","bird","one population","not_yet_matched_to_pinned_COL"]])
        self.write("data/evidence/assertion_screening.csv",
                   ["assertion_id","source_access_level","source_access_url","extraction_date","extraction_provenance","independent_review"],
                   [["r1-test","abstract_only","https://example.org/test","2026-11-23","synthetic","none"]])
        self.write("data/evidence/assertion_interpretations.csv",
                   ["assertion_id","interpretation_level","interpretation_note"],[["r1-test","caution","Test case not semantic evidence"]])
        self.write("data/evidence/reviews.csv",["review_id","assertion_id","reviewer_id","decision","reason","review_date"],[])
        self.write("data/ontology/capabilities.csv",["capability_id","label","operational_definition","status"],
                   [["response","Response","Measured behavior","proposed_pilot_only"]])
        self.write("data/ontology/modalities.csv",["modality_id","label","definition","status"],
                   [["acoustic","Acoustic","Sound","proposed"]])
        self.write("data/ontology/phenomenon_families.csv",["phenomenon_id","label","operational_definition","status"],
                   [["playback","Playback","Measured event","proposed_pilot_only"]])
        self.write("data/ontology/physiological_marker_families.csv",["family_id","label","definition","status"],
                   [["neural_activity","Neural","Recorded activity","proposed"]])
    
    def tearDown(self):
        self.temp.cleanup()

    def write(self, path, headers, rows):
        target = self.root / path
        with target.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def replace(self, path, original, replacement):
        p = self.root / path
        p.write_text(p.read_text(encoding="utf-8").replace(original, replacement), encoding="utf-8")

    def test_valid_draft_and_matrix(self):
        report = validate(self.root)
        self.assertEqual([], report["errors"])
        result = build(self.root)
        self.assertEqual(1, result["studies"])
        output = (self.root / "docs/figures/r1-draft-coverage.csv").read_text()
        self.assertIn("draft_sources_only", output)

    def test_unknown_reference_is_rejected(self):
        self.replace("data/evidence/assertion_sources.csv","ref-x","ref-unknown")
        self.assertIn("unknown reference_id", " ".join(validate(self.root)["errors"]))

    def test_unassessed_is_not_an_atomic_observation(self):
        self.replace("data/evidence/assertions.csv","documented_presence","not_assessed")
        self.assertIn("invalid atomic evidence", " ".join(validate(self.root)["errors"]))

    def test_missing_precise_source_location_is_rejected(self):
        self.replace("data/evidence/assertion_sources.csv","Abstract,"," ,")
        self.assertIn("source location missing", " ".join(validate(self.root)["errors"]))


if __name__ == "__main__":
    unittest.main()
