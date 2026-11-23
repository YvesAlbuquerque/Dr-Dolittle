# CSL JSON bibliography catalog

The [seed catalog](seed.csl.json) now contains **80 candidate references**. The [status table](status.csv) has a matching row for each record. **Eight** reference records have structured authors and venue metadata checked against publisher or institutional records; the remainder have only partial bibliographic metadata. **14** records lack a DOI field (which can be appropriate for books or web resources); **66** have a DOI value. No paper has been promoted to an independently reviewed evidence assertion.

An in-session check of the **65 entries at the earlier check** found unique IDs, unique populated DOI strings and a matching status for each ID. The [Python validator](../../scripts/validate_bibliography.py) and [synthetic unit tests](../../tests/test_validate_bibliography.py) now exist; see the [workflow](../../.github/workflows/validate-bibliography.yml). Five unit tests ran successfully **locally against synthetic fixtures**. The GitHub-hosted workflow and clean checkout were not confirmed as run at the time of this update. The **9 physiological research references** were added as *discovery candidates*, not human-verified evidence; their addition does not change the original test claims. **Checking bibliographic structure is not checking the correctness of scientific conclusions.**

CSL JSON is the **canonical interchange format** and can be imported into reference managers such as Zotero. Zotero is optional. The catalog is not a scientific evidence database and must not be cited as proof of behavioral claims.

Rules:
- Stable `id` for each reference; preserve it across DOI corrections.
- Prefer DOI resolved via Crossref or the publisher. Treat preprint and final publication links carefully.
- Do not add fake author lists, journals or abstracts to make a record appear complete.
- Record data licenses and audio rights independently from journal metadata.
- Future automated import must be repeatable and rate-limit aware.

The [R1 pilot](../../docs/r1-pilot-01.md) added two primary research references and one missing DOI to this catalog. All 15 source-linked pilot observations remain draft, and none has independent scientific review.
