# CSL JSON bibliography catalog

The [seed catalog](seed.csl.json) contains **54 discovered records** compiled from the [reading queue](../../docs/references.md) and targeted follow-up on 2026-11-23. Records have project-local IDs, title, link, and year; some include a DOI. The [status table](status.csv) marks all entries as **discovered / partial metadata**, not as fully verified or read. All 54 records still lack structured authors; 15 of the original 48 have no DOI field (some may not have a DOI by nature). Authors, venues and publication types still need authoritative metadata normalization. A check of the **original 48** found unique IDs matching their 48 status rows and no duplicate populated DOI strings; this is not a semantic duplicate audit. See [second review](../../docs/foundation-review-round-2-2026-11-23.md).

CSL JSON is the **canonical interchange format** and can be imported into reference managers such as Zotero. Zotero is optional. The catalog is not a scientific evidence database and must not be cited as proof of behavioral claims.

Rules:
- Stable `id` for each reference; preserve it across DOI corrections.
- Prefer DOI resolved via Crossref or the publisher. Treat preprint and final publication links carefully.
- Do not add fake author lists, journals or abstracts to make a record appear complete.
- Record data licenses and audio rights independently from journal metadata.
- Future automated import must be repeatable and rate-limit aware.
