# CSL JSON bibliography catalog

The [seed catalog](seed.csl.json) contains **48 discovered records** compiled from the [initial reading queue](../../docs/references.md) on 2026-11-23. Records have project-local IDs, title, link, and year; some include a DOI. The [status table](status.csv) marks all entries as **discovered / partial metadata**, not as fully verified or read. Authors, venues and publication types still need authoritative metadata normalization.

CSL JSON is the **canonical interchange format** and can be imported into reference managers such as Zotero. Zotero is optional. The catalog is not a scientific evidence database and must not be cited as proof of behavioral claims.

Rules:
- Stable `id` for each reference; preserve it across DOI corrections.
- Prefer DOI resolved via Crossref or the publisher. Treat preprint and final publication links carefully.
- Do not add fake author lists, journals or abstracts to make a record appear complete.
- Record data licenses and audio rights independently from journal metadata.
- Future automated import must be repeatable and rate-limit aware.
