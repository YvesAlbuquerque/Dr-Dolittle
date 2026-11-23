"""Synthetic fixtures only; actual repository validation requires a checkout."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripts.validate_bibliography import validate


class ValidatorTests(unittest.TestCase):
    def check(self, entries, rows):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            catalog, status = base / "seed.csl.json", base / "status.csv"
            catalog.write_text(json.dumps(entries), encoding="utf-8")
            with status.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "reference_id", "screening_status", "metadata_status", "source_provenance", "checked_on"])
                writer.writeheader()
                writer.writerows(rows)
            return validate(catalog, status)

    def fixtures(self):
        paper = {
            "id": "ref-a", "title": "A title", "type": "article-journal",
            "DOI": "10.1234/foo", "URL": "https://doi.org/10.1234/foo",
            "issued": {"date-parts": [[2020]]}}
        row = {
            "reference_id": "ref-a", "screening_status": "discovered",
            "metadata_status": "partial_metadata",
            "source_provenance": "manual_survey", "checked_on": "2026-11-23"}
        return paper, row

    def test_valid_metadata_with_author_warning(self):
        p, r = self.fixtures()
        result = self.check([p], [r])
        self.assertFalse(result["errors"])
        self.assertTrue(result["warnings"])

    def test_duplicate_doi_is_error(self):
        p, r = self.fixtures()
        p2, r2 = {**p, "id": "ref-b"}, {**r, "reference_id": "ref-b"}
        self.assertIn("duplicate DOI", "\n".join(self.check([p, p2], [r, r2])["errors"]))

    def test_missing_status_is_error(self):
        p, _ = self.fixtures()
        self.assertIn("missing status", "\n".join(self.check([p], [])["errors"]))

    def test_missing_doi_is_warning_only(self):
        p, r = self.fixtures()
        del p["DOI"]
        result = self.check([p], [r])
        self.assertFalse(result["errors"])
        self.assertIn("DOI missing", "\n".join(result["warnings"]))

    def test_invalid_source_date_is_error(self):
        p, r = self.fixtures()
        r["checked_on"] = "yesterday"
        self.assertIn("checked_on", "\n".join(self.check([p], [r])["errors"]))


if __name__ == "__main__":
    unittest.main()
