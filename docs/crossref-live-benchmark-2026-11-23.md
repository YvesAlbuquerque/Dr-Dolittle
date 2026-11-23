# R1 live Crossref DOI benchmark — first observed run

**Executed:** 2026-11-23 (GitHub Actions, Ubuntu runner; real HTTPS requests).  
**Runs:** initial https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45108997603 and corrected-regression rerun https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45109156893  
**Artifact:** https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45108997603/artifacts/14787734664  
**Repository PR:** https://github.com/YvesAlbuquerque/Dr-Dolittle/pull/6  
**Status:** first small empirical transport/metadata check, **not an estimate of general sensitivity or specificity**, not a bibliographic review, not a peer-review check, not an AI-methods assessment.

## Why this run matters

Six requests reached the real public Crossref API after offline regressions passed. The uploaded artifact contains six individual normalized API-response records (including SHA-256 hashes of raw API responses) and a benchmark summary. Nothing was promoted to the canonical bibliography or `source_integrity.csv`.

| Case | DOI | Actual response | Scientific interpretation boundary |
| --- | --- | --- | --- |
| Vervet alarm-call paper | `10.1126/science.7433999` | `matched`; article title/types returned | DOI/title lookup succeeded; not a Methods/Results assessment |
| Horse snort paper | `10.1371/journal.pone.0197898` | `matched` | DOI/title lookup succeeded; not a biological claim |
| **Known retraction control** | `10.1021/am300292v` | `matched`, **`updated-by` lists a `retraction`** | **Positive control passed**; this checks metadata plumbing, not generalized recall |
| **Known retraction with absent update link** | `10.33263/BRIAC94.979986` | `matched`, **no linked updates; title includes “RETRACTED:”** | Real counterexample to clearing a work just because `updated-by` is absent |
| **Known publisher correction with absent link** | `10.1029/2001RG000106` | `matched`, no linked updates | Requires publisher follow-up; source documents that some corrections are separately registered and not linked |
| Made-up DOI | `10.9999/dr-dolittle-nonexistent-2026-11-23` | Crossref HTTP **404 / not_found** | Error handling succeeded for one synthetic negative |

**Observed outcomes:** **5/6** DOI lookups matched deposited DOI and a title; the sixth returned HTTP 404 as intended. The single linked-retraction positive control was caught (**1/1**), and the missing-link examples demonstrated why “no update in API” is **not** a clean certificate. These selected cases cannot be used to estimate accuracy on the wider 80-reference bibliography.

## Discovered implementation defects and repairs

1. The original code inspected `update-by` (incorrect for the original work), whereas actual Crossref JSON uses `updated-by`. This could miss known retraced works. Fixed, tested on synthetic cases and **confirmed by the live positive control**.
2. The API returned **“RETRACTED:” in the title** for `10.33263/BRIAC94.979986`, but no structured update relationship. The original benchmark recorded an empty update list. A subsequent code change added the independent `title_retraction_flag_present` and `title_suggests_retraction_needs_verification` warning. The updated code was **executed in a second live GitHub Actions run** (45109156893). The six calls again returned **5 matched / 1 not-found**, the linked-retraction positive control passed, and the gap article correctly produced `title_retraction_flag_present=true`. This is a metadata flag, not an independently verified publisher notice.

An absent linked notice is intentionally **not** a negative control proving a publication is sound. This pipeline therefore has **no “verified no retraction” result**.

## Limitations and follow-up

- These six examples were **selected because their expected behavior is known**; this is a smoke benchmark, not a random sample or calibration corpus.
- Crossref deposits depend on member metadata and trusted external feeds; missed notices happen.
- The correction DOI example was located via a Crossref community discussion; the publisher's actual correction DOI needs independent confirmation before declaring a fully verified positive control.
- A DOI registered by Crossref does not prove the text's accuracy, peer-review rigor, journal quality, reproducibility, or absence of fraud.
- We have no live benchmark against DataCite-only works, preprint pairs, non-Crossref registrations, deliberate misleading titles, or large-scale simultaneous queries.
- The exact response snapshots and request timestamps are in the GitHub Actions artifact, retained by that run for **30 days**; the summary here is a durable record of findings.

## Next research gate

1. Apply **both linked-update and suspicious-title checks** on a few selected original DOI records and recheck with publisher/Retraction Watch information.
2. Construct source-grounded model-appraisal packets from four R1 studies, with fields for Methods/Results evidence, study sample, controls and directness; require `abstain` when only an abstract is accessible.
3. Benchmark an AI's methodological *extraction accuracy*, before interpreting its judgments as calibrated assessments. Do not auto-upgrade `not_assessed` and do not elevate conjectures to facts.
