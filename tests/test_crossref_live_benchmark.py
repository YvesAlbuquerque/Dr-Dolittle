"""Offline synthetic control-case tests; live correctness is separately measured in CI."""
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path

from scripts.crossref_live_benchmark import CASES, benchmark


class _Response:
    def __init__(self, body): self.body = body
    def __enter__(self): return self
    def __exit__(self, *exc): return None
    def read(self, maxbytes): return self.body[:maxbytes]


class BenchmarkTests(unittest.TestCase):
    def test_dry_run_has_six_cases_no_output(self):
        result = benchmark()
        self.assertEqual("dry_run", result["mode"])
        self.assertEqual(6, result["case_count"])
        self.assertEqual(0, result["real_requests"])

    def test_synthetic_retraction_positive_control_detected(self):
        def opener(req, timeout):
            doi = req.full_url.split("/works/")[1].split("?")[0].lower()
            # The transport percent-escapes some DOI punctuation; original DOI
            # is extracted from the fixed benchmark case list.
            from urllib.parse import unquote
            doi = unquote(doi)
            if "dr-dolittle-nonexistent" in doi:
                raise urllib.error.HTTPError(req.full_url, 404, "Not found", {}, None)
            record = {"message": {
                "DOI": doi, "title": ["Synthetic "+doi],
                "type": "journal-article", "published":{"date-parts":[[2020]]}
            }}
            if doi == "10.1021/am300292v":
                record["message"]["updated-by"] = [
                    {"DOI":"10.1021/acsami.9b11759", "type":"retraction", "source":"retraction-watch"}]
            return _Response(json.dumps(record).encode())
        with tempfile.TemporaryDirectory() as t:
            target=Path(t)/"snapshot"
            result=benchmark(True, target, sleeper=lambda x:None, transport=opener)
            self.assertTrue(result["retraction_positive_control_pass"])
            self.assertFalse(result["scientific_certainty_assigned"])
            self.assertTrue((target/"benchmark-summary.json").exists())
            self.assertTrue(all(not row["metadata_clears_no_retraction"] for row in result["results"]))
            self.assertEqual("not_found", result["results"][-1]["status"])
            with self.assertRaises(FileExistsError):
                benchmark(True, target, sleeper=lambda x:None, transport=opener)

    def test_negative_control_does_not_erase_known_missing_link(self):
        cases = {c["case"]:c for c in CASES}
        self.assertIn("gap", cases["known_retraction_metadata_gap"]["kind"])
        self.assertIn("gap", cases["known_correction_metadata_gap"]["kind"])


if __name__ == "__main__":
    unittest.main()
