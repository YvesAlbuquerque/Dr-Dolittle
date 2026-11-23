# Crossref provenance-only DOI worker — R1 implementation

**2026-11-23 — Status: Prototyped.** A bounded Python worker and offline regression tests are implemented. **No live Crossref batch has been executed by this document or merged automatically into the canonical bibliography.** The worker **does not use an LLM** and **does not grade scientific claims**.

## Why Crossref first

The [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) provides public DOI metadata without a mandatory paid key. Its documentation specifies public single-DOI requests and an optional contact email for the polite pool. The [Retraction Watch metadata](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/) includes some update/retraction notices as `update-to` relationships. These are incomplete for a universal retraction clearance.

[OpenAlex](https://help.openalex.org/api/authentication/) remains a separate **candidate adapter** for citation/network expansion, preferably using a free API key when operating at scale; 2026 usage/credential rules differ from older advice. No OpenAlex dependency is required for this first step.

## How to run

From the repository root, with Python 3.12+:

```bash
# Offline and read-only; inspect the selected DOI records; no API calls.
python scripts/crossref_metadata_worker.py --limit 5

# Explicit real requests. Defaults to at most 5, hard limit 25.
python scripts/crossref_metadata_worker.py --live --limit 5

# Recommended: optional contact email to use Crossref's polite pool.
# Use your own address; do not commit it or snapshots to the repository.
python scripts/crossref_metadata_worker.py --live --limit 5 --email your-contact@example.org

# Hand-pick three pilot works for metadata validation.
python scripts/crossref_metadata_worker.py --live --limit 3 --ids \
  ref-monkey-responses-to-three-different-alarm-calls \
  ref-issa-porostocky-dog-sigh-1993 \
  ref-zebra-finch-neural-vocal-familiarity-2026
```

Each real execution creates a unique timestamped `_local/crossref/<run-id>/` folder, ignored by Git, containing numbered source snapshots and a manifest. Raw API bytes are hashed for provenance; only curated metadata fields are saved, not copyrighted article text. Dates, catalog digest, exact source URL, DOI, detected update relationships and response outcomes are recorded. Re-running produces a new folder rather than silently replacing a prior snapshot.

The worker does **not** write `data/bibliography/source_integrity.csv`, `bibliography/catalog/seed.csl.json`, `data/evidence/*`, or scientific confidence labels. Future promotion from a local API observation to canonical source integrity remains a separately tested decision.

## Interpretation of outcomes

| Outcome | What it means | What it does **not** mean |
| --- | --- | --- |
| `matched` | Crossref returned a DOI equal to the selected DOI and nonblank deposited title | Title/body/peer review/methods are independently verified |
| `mismatch_or_incomplete` | DOI or title differed/missing | A paper is fraudulent |
| `not_found` | Crossref returned HTTP 404 | DOI is invalid everywhere, unreviewed, or predatory |
| `http_error`, `transport_error` | Could not reliably retrieve data | The paper is false or withdrawn |
| `metadata_updates_present` | Crossref lists one or more update relations in selected fields | All listed notices or article conclusions have been independently assessed |
| `not_cleared` | No listed update was discovered in the retrieved record | Proof there are no retractions or corrections **anywhere** |

**Peer-review status always remains `unknown`** in this first worker. Editorial transparency and institutional reputation are not inferred from Crossref article type or publisher label.

## Reproducibility and reliability

- No external Python dependencies, no paid APIs, no secrets, no persistent server.
- Fixed HTTPS host (Crossref); no arbitrary-URL fetching and no article-body scraping.
- Timeouts, sequential lookups, short delays, bounded retries for 429/5xx and a 2 MB response cap.
- An explicit `--live` switch; local immutable runs; no mutation of canonical evidence.
- Injected mock responses for test coverage including DOI mismatch, Retraction Watch update, 404 and 429.
- Rate budgets may change; handle real-world 403/429 by stopping/retrying later rather than evading provider limits.
- The worker is **not yet calibrated** on a known retracted DOI corpus, journal verification dataset, real current API responses, or stable snapshots of this repo's entire bibliography.

## Next measurable milestone

Run a **small live DOI sample** and compare returned titles, publication types, changes and dates manually against official publisher/Crossref pages. Then build an *evidence-backed promotion step* to source-integrity records, with dual source-check and a fail-closed treatment of missing notice information. Benchmark deliberately selected known retracted/corrected articles, DOI typos, books, preprints and non-Crossref records before any larger batch.

**Scientific assurance status:** this proves a reproducible provenance transport mechanism only. It does not establish source credibility or AI scientific assessment reliability.
