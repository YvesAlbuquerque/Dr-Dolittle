"""Offline synthetic Crossref worker tests: no external network or editorial verdicts."""
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from scripts.crossref_metadata_worker import (
    crossref_url, lookup, normalize_doi, parse_payload, run, select_records
)


def response(data):
    class Reply:
        def __enter__(self): return self
        def __exit__(self, *args): return None
        def read(self, n): return data[:n]
    return Reply()


def payload(doi="10.1234/test", title="Test", update=None):
    work = {"DOI": doi, "title": [title], "type": "journal-article",
            "container-title": ["Journal"], "published": {"date-parts": [[2025]]}}
    if update is not None:
        work["update-to"] = update
    return json.dumps({"message": work}).encode("utf-8")


class CrossrefWorkerTests(unittest.TestCase):
    def test_doi_normalization_and_safe_url(self):
        self.assertEqual("10.1234/test", normalize_doi("HTTPS://DOI.ORG/10.1234/TEST"))
        self.assertEqual("https://api.crossref.org/works/10.1234/test", crossref_url("10.1234/TEST"))
        self.assertIsNone(normalize_doi("not-a-doi"))

    def test_matching_record_is_not_peer_review_proof(self):
        result = lookup("10.1234/test", opener=lambda request, timeout: response(payload()), sleeper=lambda sec: None)
        self.assertEqual("matched", result["status"])
        self.assertEqual("unknown", result["peer_review_status"])
        self.assertEqual("not_cleared", result["integrity_notice_result"])
        self.assertEqual("2025", str(result["crossref_year"]))
        self.assertEqual(64, len(result["raw_sha256"]))

    def test_retraction_metadata_is_flagged_but_not_a_truth_grade(self):
        notice = [{"type": "retraction", "DOI": "10.1234/notice", "source": "retraction-watch"}]
        r = parse_payload("10.1234/test", payload(update=notice))
        self.assertEqual("metadata_updates_present", r["integrity_notice_result"])
        self.assertEqual("retraction", r["listed_updates"][0]["type"])
        self.assertEqual("unknown", r["peer_review_status"])

    def test_original_updated_by_retraction_and_correction_are_recognized(self):
        retracted = json.loads(payload())
        retracted["message"]["updated-by"] = [
            {"type":"retraction","DOI":"10.1234/retraction-notice","source":"retraction-watch"}]
        result = parse_payload("10.1234/test", json.dumps(retracted).encode())
        self.assertEqual("metadata_updates_present", result["integrity_notice_result"])
        self.assertEqual("updated-by", result["listed_updates"][0]["relation_field"])
        corrected = json.loads(payload())
        corrected["message"]["updated-by"] = [
            {"type":"correction","DOI":"10.1234/correction-notice","source":"publisher"}]
        r = parse_payload("10.1234/test", json.dumps(corrected).encode())
        self.assertEqual("correction", r["listed_updates"][0]["type"])
        self.assertEqual("unknown", r["peer_review_status"])

    def test_title_retraction_warning_even_without_update_links(self):
        flagged = parse_payload("10.1234/test", payload(title="RETRACTED: Synthetic experiment"))
        self.assertTrue(flagged["title_retraction_flag_present"])
        self.assertEqual("title_suggests_retraction_needs_verification", flagged["integrity_notice_result"])
        self.assertEqual([], flagged["listed_updates"])
        normal = parse_payload("10.1234/test", payload(title="Normal article"))
        self.assertFalse(normal["title_retraction_flag_present"])
        self.assertEqual("not_cleared", normal["integrity_notice_result"])

    def test_mismatched_or_invalid_payload_not_promoted(self):
        self.assertEqual("mismatch_or_incomplete",
                         parse_payload("10.1234/test", payload("10.1234/other"))["status"])
        self.assertEqual("malformed_response", parse_payload("10.1234/test", b"{}")["status"])

    def test_not_found_and_rate_limit_retry(self):
        attempts = []
        def limited(req, timeout):
            attempts.append(1)
            if len(attempts) == 1:
                raise urllib.error.HTTPError(req.full_url, 429, "too many", {"Retry-After": "0.1"}, None)
            return response(payload())
        r = lookup("10.1234/test", opener=limited, sleeper=lambda sec: None)
        self.assertEqual("matched", r["status"])
        self.assertEqual(2, len(attempts))
        def missing(req, timeout):
            raise urllib.error.HTTPError(req.full_url, 404, "missing", {}, None)
        self.assertEqual("not_found", lookup("10.1234/test", opener=missing)["status"])

    def test_bounded_selection_and_dry_run_no_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/"bibliography/catalog").mkdir(parents=True)
            (root/"bibliography/catalog/seed.csl.json").write_text(
                json.dumps([{"id":"book","title":"Book"},
                            {"id":"ref1","title":"Paper","DOI":"10.1234/test"},
                            {"id":"ref2","title":"Duplicate DOI","DOI":"10.1234/TEST"}]), encoding="utf-8")
            plan = run(root, limit=5)
            self.assertEqual("dry_run", plan["mode"])
            self.assertEqual(1, plan["selected_count"])
            self.assertFalse((root/"_local").exists())
            with self.assertRaises(ValueError):
                select_records([], 26)
            with self.assertRaises(ValueError):
                run(root, ids=["missing"])

    def test_live_fixture_writes_local_provenance_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/"bibliography/catalog").mkdir(parents=True)
            catalog = root/"bibliography/catalog/seed.csl.json"
            original = json.dumps([{"id":"ref1","title":"Test","DOI":"10.1234/test"}])
            catalog.write_text(original, encoding="utf-8")
            report = run(root, live=True, limit=1, opener=lambda req, timeout: response(payload()),
                         sleeper=lambda _: None)
            directory = Path(report["local_run_dir"])
            manifest = json.loads((directory/"manifest.json").read_text())
            self.assertEqual({"matched":1}, manifest["results"])
            self.assertEqual("unknown", json.loads((directory/"000.json").read_text())["peer_review_status"])
            self.assertEqual(original, catalog.read_text())
            self.assertFalse((root/"data/bibliography/source_integrity.csv").exists())


if __name__ == "__main__":
    unittest.main()
