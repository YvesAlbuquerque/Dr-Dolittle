# CSL JSON bibliography catalog

The [seed catalog](seed.csl.json) now contains **65 candidate references**. The [status table](status.csv) has a matching row for each record. **Eight** reference records have structured authors and venue metadata checked against publisher or institutional records; the remainder have only partial bibliographic metadata. **15** records lack a DOI field (which can be appropriate for books or web resources); **50** have a DOI value. No paper has been promoted to an independently reviewed evidence assertion.

An in-session check of the **actual 65 catalog entries** found unique IDs, unique populated DOI strings and a matching status for each ID. The [Python validator](../../scripts/validate_bibliography.py) and [synthetic unit tests](../../tests/test_validate_bibliography.py) now exist; see the [workflow](../../.github/workflows/validate-bibliography.yml). Five unit tests ran successfully **locally against synthetic fixtures**. The GitHub-hosted workflow and clean checkout were not confirmed as run at the time of this update. **Checking bibliographic structure is not checking the correctness of scientific conclusions.**

CSL JSON is the **canonical interchange format** and can be imported into reference managers such as Zotero. Zotero is optional. The catalog is not a scientific evidence database and must not be cited as proof of behavioral claims.

Rules:
- Stable `id` for each reference; preserve it across DOI corrections.
- Prefer DOI resolved via Crossref or the publisher. Treat preprint and final publication links carefully.
- Do not add fake author lists, journals or abstracts to make a record appear complete.
- Record data licenses and audio rights independently from journal metadata.
- Future automated import must be repeatable and rate-limit aware.
