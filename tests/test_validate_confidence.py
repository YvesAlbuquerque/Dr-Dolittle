"""Synthetic tests of confidence assessment data integrity; no scientific ratings implied."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripts.validate_confidence import validate, DOMAINS, ASSESSMENT_DOMAINS


class ConfidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "data/evidence").mkdir(parents=True)
        (self.root / "bibliography/catalog").mkdir(parents=True)
        (self.root / "bibliography/catalog/seed.csl.json").write_text(
            json.dumps([{"id": "ref-test", "title": "Synthetic primary source"}]), encoding="utf-8")
        base = "data/evidence/"
        self.write(base+"assertions.csv", ["assertion_id"], [["a1"]])
        self.write(base+"assertion_sources.csv", ["assertion_id", "reference_id"], [["a1", "ref-test"]])
        self.write(base+"assertion_screening.csv", ["assertion_id", "source_access_level"], [["a1", "abstract_only"]])
        self.appraisal_fields = ["appraisal_id", "assertion_id", "reference_id", "status",
                                 *DOMAINS, "assessment_method", "assessor_kind", "assessor_id",
                                 "assessed_on", "evidence_location", "rationale"]
        self.placeholder = {"appraisal_id":"app-a1", "assertion_id":"a1", "reference_id":"ref-test",
                            "status":"not_assessed", "rationale":"Awaiting method assessment"}
        self.write_dict(base+"study_appraisals.csv", self.appraisal_fields, [self.placeholder])
        self.write(base+"hypotheses.csv",
                   ["hypothesis_id","statement","testable_outcome","unit_of_inference","falsification_criteria","status"], [])
        self.write(base+"hypothesis_evidence.csv",
                   ["hypothesis_id","assertion_id","relation","independence_cluster","linkage_rationale"], [])
        self.certainty_fields = ["assessment_id","hypothesis_id","assessment_version","level",
                                 *ASSESSMENT_DOMAINS, "assessment_method","assessor_kind",
                                 "assessor_id","assessed_on","source_set","reason","supersedes_id"]
        self.write(base+"certainty_assessments.csv", self.certainty_fields, [])

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, headers, rows):
        with (self.root / path).open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerows(rows)

    def write_dict(self, path, headers, rows):
        with (self.root / path).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            w.writerows(rows)

    def add_hypothesis(self):
        self.write("data/evidence/hypotheses.csv",
                   ["hypothesis_id","statement","testable_outcome","unit_of_inference","falsification_criteria","status"],
                   [["h1","A receiver reacts to A","Difference in response rate","one population",
                     "No response difference under blinded playback", "proposed"]])

    def test_placeholder_does_not_assign_low_certainty(self):
        r = validate(self.root)
        self.assertEqual([], r["errors"])
        self.assertEqual(0, r["completed_study_appraisals"])
        self.assertEqual(0, r["certainty_assessments"])

    def test_domain_assessment_in_unassessed_record_fails(self):
        modified = {**self.placeholder, "risk_of_bias": "low_concern"}
        self.write_dict("data/evidence/study_appraisals.csv", self.appraisal_fields, [modified])
        self.assertIn("not_assessed may not contain", " ".join(validate(self.root)["errors"]))

    def test_nonexistent_reference_rejected(self):
        modified = {**self.placeholder, "reference_id": "ref-fabricated"}
        self.write_dict("data/evidence/study_appraisals.csv", self.appraisal_fields, [modified])
        self.assertIn("invalid assertion/reference link", " ".join(validate(self.root)["errors"]))

    def test_promoted_certainty_without_evidence_rejected(self):
        self.add_hypothesis()
        assessment = {"assessment_id":"cert1","hypothesis_id":"h1","assessment_version":"1",
                      "level":"low","assessment_method":"hypothetical appraisal",
                      "assessor_kind":"human","assessor_id":"test","assessed_on":"2026-11-23",
                      "source_set":"ref-test","reason":"synthetic only"}
        assessment.update({k:"unclear" for k in ASSESSMENT_DOMAINS})
        self.write_dict("data/evidence/certainty_assessments.csv", self.certainty_fields, [assessment])
        errs = " ".join(validate(self.root)["errors"])
        self.assertIn("no linked evidence", errs)

    def test_high_certainty_needs_independent_study_clusters(self):
        self.add_hypothesis()
        self.write("data/evidence/assertion_screening.csv",["assertion_id","source_access_level"],[["a1","full_html"]])
        app = {**self.placeholder, "status":"appraised","assessment_method":"source-check",
               "assessor_kind":"human","assessor_id":"example","assessed_on":"2026-11-23",
               "evidence_location":"Methods","rationale":"synthetic"}
        app.update({k:"unclear" for k in DOMAINS})
        self.write_dict("data/evidence/study_appraisals.csv", self.appraisal_fields, [app])
        self.write("data/evidence/hypothesis_evidence.csv",
                   ["hypothesis_id","assertion_id","relation","independence_cluster","linkage_rationale"],
                   [["h1","a1","supports","cluster1","synthetic"]])
        assessment = {"assessment_id":"cert1","hypothesis_id":"h1","assessment_version":"1",
                      "level":"high","assessment_method":"test","assessor_kind":"human","assessor_id":"test",
                      "assessed_on":"2026-11-23","source_set":"ref-test","reason":"synthetic"}
        assessment.update({k:"unclear" for k in ASSESSMENT_DOMAINS})
        self.write_dict("data/evidence/certainty_assessments.csv", self.certainty_fields, [assessment])
        self.assertIn("two explicitly distinct", " ".join(validate(self.root)["errors"]))


if __name__ == "__main__":
    unittest.main()
