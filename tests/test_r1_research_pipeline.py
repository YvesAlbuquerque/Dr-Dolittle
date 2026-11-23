"""Deterministic, network-free tests for the R1 source-first AI pipeline."""
import csv
import json
import urllib.error
import tempfile
import unittest
from pathlib import Path

from scripts.r1_research_pipeline import (
    extract_xml, extract_bioc, fetch_source, lookup_metadata, model_call_ollama,
    prompt, selected_passages, validate_model_draft, execute, request
)

DOI = "10.1371/journal.pcbi.1014024"

OA = b"""<?xml version="1.0"?>
<article>
<front><article-meta><article-id pub-id-type="doi">10.1371/journal.pcbi.1014024</article-id>
<permissions><license license-type="open-access"><license-p>Creative Commons Attribution</license-p></license></permissions>
<abstract><p>Familiar birds responded more frequently to the recorded sounds.</p></abstract>
</article-meta></front>
<body>
<sec><title>Materials and methods</title>
<p>Seven birds were enrolled in the behavioral experiment with independent subject identifiers.</p>
<p>Vocalizations were presented in pseudorandomized order, with a silent control condition.</p>
</sec>
<sec><title>Results</title><p>The reported response differed across familiarity conditions.</p></sec>
</body></article>
"""


class FakeResponse:
    def __init__(self, data): self.data = data
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, n): return self.data[:n]


def fake_source(req, timeout=18):
    url = req.full_url
    if "fullTextXML" in url:
        return FakeResponse(OA)
    if "search?" in url:
        obj = {"resultList":{"result":[{
            "doi":DOI,"title":"Zebra finch playback study","isOpenAccess":"Y",
            "pmcid":"PMC12345678","id":"98765","abstractText":"Familiar birds responded more frequently."
        }]}}
        return FakeResponse(json.dumps(obj).encode("utf-8"))
    raise ValueError("Unexpected endpoint")


class ResearchPipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        (self.root/"data/evidence").mkdir(parents=True)
        (self.root/"bibliography/catalog").mkdir(parents=True)
        (self.root/"bibliography/catalog/seed.csl.json").write_text(
            json.dumps([{"id":"ref13","DOI":DOI,"title":"Zebra finch playback study"}]))
        def write(path, heads, rows):
            with (self.root/path).open("w",encoding="utf-8",newline="") as f:
                w=csv.writer(f);w.writerow(heads);w.writerows(rows)
        write("data/evidence/assertions.csv", ["assertion_id","claim","limitations"],
              [["r1-013","A response was reported.","Single group"]])
        write("data/evidence/assertion_sources.csv",["assertion_id","reference_id"],
              [["r1-013","ref13"]])
        write("data/evidence/assertion_screening.csv",["assertion_id","source_access_url"],
              [["r1-013","https://journals.plos.org/ploscompbiol/article?id="+DOI]])

    def tearDown(self): self.tmp.cleanup()

    def test_core_metadata_exact_doi(self):
        r=lookup_metadata(DOI,opener=fake_source,sleeper=lambda t: None)
        self.assertEqual("matched",r["status"])
        self.assertTrue(r["is_open_access"])
        self.assertEqual("PMC12345678",r["pmcid"])

    def test_license_and_doi_gate(self):
        x=extract_xml(OA,DOI)
        self.assertTrue(x["full_text"])
        self.assertGreaterEqual(len(x["sections"]),3)
        with self.assertRaisesRegex(ValueError,"DOI"):
            extract_xml(OA,"10.1234/false")
        with self.assertRaisesRegex(ValueError,"license"):
            extract_xml(OA.replace(b"<license ",b"<licensing ").replace(b"</license>",b"</licensing>"),DOI)
        with self.assertRaisesRegex(ValueError,"DTD"):
            extract_xml(b"<!DOCTYPE bomb>"+OA,DOI)

    def test_valid_external_jats_doctype_sanitized(self):
        safe = OA.replace(b"<article>", b'<!DOCTYPE article PUBLIC "-//NLM//DTD JATS" "archive.dtd"><article>',1)
        data = extract_xml(safe, DOI)
        self.assertTrue(data["full_text"])

    def test_exact_pmid_fallback_does_not_claim_doi_verified(self):
        def source(req, timeout=18):
            if "EXT_ID" in req.full_url:
                return FakeResponse(json.dumps({"resultList":{"result":[{
                    "id":"8210757","source":"MED","doi":"10.1234/incorrect",
                    "abstractText":"Four dogs were recorded while sleeping.","isOpenAccess":"N"
                }]}}).encode())
            return FakeResponse(json.dumps({"resultList":{"result":[]}}).encode())
        result=lookup_metadata("10.1016/0034-5687(93)90004-t",opener=source,
                               sleeper=lambda _:None,pmid="8210757")
        self.assertEqual("pmid_match_doi_unconfirmed",result["status"])
        self.assertFalse(result["doi_confirmed"])

    def test_official_pmc_oa_bioc_fallback_with_confirmed_identity(self):
        sample={"documents":[{"id":"PMC12345678","passages":[
           {"infons":{"section_type":"METHODS"},"text":"Seven birds were tested using a playback design with controls."},
           {"infons":{"section_type":"RESULTS"},"text":"Familiar playback responses differed from control conditions."},
           {"infons":{"section_type":"DISCUSSION"},"text":"The interpretation remains constrained by design and sampling."}]}]}
        raw=json.dumps(sample).encode()
        output=extract_bioc(raw,"PMC12345678",known_pmid="98765",metadata_oa=True)
        self.assertEqual(3,len(output["sections"]))
        self.assertIn("PMC Open Access",output["rights_basis"])
        with self.assertRaisesRegex(ValueError,"OA metadata"):
            extract_bioc(raw,"PMC12345678",metadata_oa=False)
        with self.assertRaisesRegex(ValueError,"document id"):
            extract_bioc(raw,"PMC00000000",metadata_oa=True)

    def test_fallback_when_jats_service_returns_500(self):
        sample={"documents":[{"id":"PMC12345678","passages":[
           {"infons":{"section_type":"METHODS"},"text":"Seven birds were enrolled in the playback study with controls."},
           {"infons":{"section_type":"RESULTS"},"text":"Familiar calls produced different responses in this sample."},
           {"infons":{"section_type":"ABSTRACT"},"text":"This study examined social calling in zebra finches."}]}]}
        def fail_jats(req,timeout=18):
            if "fullTextXML" in req.full_url:
                raise urllib.error.HTTPError(req.full_url,500,"error",{},None)
            if "BioC_json" in req.full_url:
                return FakeResponse(json.dumps(sample).encode())
            return fake_source(req,timeout)
        r=fetch_source({"assertion_id":"r1-013","reference_id":"ref13","doi":DOI},
                       opener=fail_jats,sleeper=lambda _:None)
        self.assertEqual("full_text",r["status"])
        self.assertEqual("bioc_json",r["source_format"])

    def test_restricted_url_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"disallowed"):
            request("https://arbitrary.example.com/unsafe")

    def test_source_retrieval_and_passages_grounded(self):
        item={"assertion_id":"r1-013","reference_id":"ref13","doi":DOI}
        x=fetch_source(item,opener=fake_source,sleeper=lambda t: None)
        self.assertEqual("full_text",x["status"])
        p=selected_passages(x)
        self.assertTrue(any("Seven birds" in v["text"] for v in p))
        self.assertEqual(64,len(x["source_sha256"]))

    def test_quote_grounding_and_no_confidence(self):
        x=fetch_source({"assertion_id":"r1-013","reference_id":"ref13","doi":DOI},
                       opener=fake_source,sleeper=lambda t:None)
        passages=selected_passages(x)
        exact=next(p for p in passages if "Seven birds" in p["text"])
        draft={"study_id":"r1-013","abstain_from_method_appraisal":False,
               "observations":[{"claim":"Bird count","quote":"Seven birds were enrolled",
                                "passage_id":exact["id"]}],
               "controls":[],"uncertainties":["One sample"],"alternative_explanations":["training"],"scientific_confidence":None}
        self.assertEqual([],validate_model_draft(draft,"r1-013",x,passages))
        draft["observations"][0]["passage_id"]=exact["id"]+" "+exact["section"]
        self.assertEqual([],validate_model_draft(draft,"r1-013",x,passages))
        draft["observations"][0]["quote"]="Seven thousand birds"
        self.assertIn("unverifiable quote", " ".join(validate_model_draft(draft,"r1-013",x,passages)))
        draft["scientific_confidence"]="high"
        self.assertIn("tried to assign", " ".join(validate_model_draft(draft,"r1-013",x,passages)))

    def test_abstract_must_abstain(self):
        source={"source_access_level":"abstract"}
        draft={"study_id":"r1-001","abstain_from_method_appraisal":False,
               "observations":[{"claim":"x","passage_id":"p001","quote":"We saw an event."}],
               "controls":[],"uncertainties":[],"alternative_explanations":[],"scientific_confidence":None}
        err=validate_model_draft(draft,"r1-001",source,[{"id":"p001","text":"We saw an event."}])
        self.assertTrue(any("abstract-only" in x for x in err))

    def test_model_response_fixture_no_real_ai(self):
        reply={"response":json.dumps({"study_id":"r1-013","abstain_from_method_appraisal":True,
                "observations":[],"controls":[],"uncertainties":[],"alternative_explanations":[],
                "scientific_confidence":None})}
        def stub(req, timeout):
            self.assertEqual("http://127.0.0.1:11434/api/generate",req.full_url)
            return FakeResponse(json.dumps(reply).encode())
        obj,hash_value=model_call_ollama("hello","qwen2.5:0.5b",opener=stub)
        self.assertTrue(obj["abstain_from_method_appraisal"])
        self.assertEqual(64,len(hash_value))

    def test_end_to_end_mock_with_valid_model_proposal(self):
        def stub_model(req, timeout):
            body=json.loads(req.data)
            self.assertIn("source_passages",body["prompt"])
            quoted="Seven birds were enrolled in the behavioral experiment"
            # the quote text is present in the actual selected source passage.
            raw={"response":json.dumps({
                "study_id":"r1-013","abstain_from_method_appraisal":False,
                "observations":[{"claim":"The study enrolled seven birds",
                                 "passage_id":"p002","quote":quoted}],
                "controls":[],"uncertainties":["Other sample properties unknown"],
                "alternative_explanations":["Habituation"],"scientific_confidence":None})}
            return FakeResponse(json.dumps(raw).encode())
        folder=self.root/"output"
        result=execute(self.root,folder,["r1-013"],live=True,model="qwen2.5:0.5b",
                       source_opener=fake_source,model_opener=stub_model)
        self.assertEqual("draft_validated_structurally",
                         result["results"][0]["methodology_proposal_status"])
        self.assertFalse(result["scientific_certainty_updated"])
        self.assertTrue((folder/"r1-013"/"source.jats.xml").exists())
        self.assertFalse((self.root/"data/evidence/certainty_assessments.csv").exists())

    def test_default_is_zero_requests(self):
        result=execute(self.root, None, ["r1-013"])
        self.assertEqual("dry_run",result["mode"])
        self.assertEqual("none",result["model"])


if __name__=="__main__":
    unittest.main()
