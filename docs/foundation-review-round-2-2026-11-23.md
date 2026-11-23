# Second foundation review — 2026-11-23

**Scope:** checked current repository texts and the bibliographic catalog, then performed a *targeted* external source check. This is a documentation and metadata consistency review, **not** critical full-text evaluation, systematic search, or validation of any biological assertions.

## Structural checks performed

- CSL JSON seed contained **48 records** before this update.
- 48 unique project IDs; 48 corresponding status entries; no unmatched status IDs.
- **0 duplicate DOI strings among populated DOI fields** (not a title-/author-level near-duplicate audit).
- **15 records with no DOI field** (some may legitimately be books, web pages or non-DOI records; do not automatically call them erroneous).
- **48 records without a structured author field**. Important normalization gap.
- Evidence assertion CSV has headers but **no scientific claims**.
- A Catalogue of Life source manifest exists; no Animalia extract ingested.

These checks inspect repository *content*, not an actual Crossref batch query, an executed Python validator, or a clean-checkout build.

## Corrections and recommendations

1. **Adopt scoping-review framing for R1**, with PRISMA-ScR as a *future reporting target*, rather than incorrectly promising that an early broad bibliography is systematic.
2. **Record units of inference:** observation, individual, interaction, group/population, species and clade are different scopes. Never infer species-wide capacities from one group/population result.
3. **Treat conflict and not-assessed carefully:** source-specific observations should stay separate; a synthesis cell can be conflicting while each source makes its own claim. Empty cells are *not assessed*, not biological negatives.
4. **Add adjacent open comparative work:** Animal Culture Database, its public exploratory app, Multi-interaction and a focused electric-fish computational study. References are discovery records until read.
5. **Avoid unnecessary bespoke tooling:** published multimodal and comparative trait tools must be assessed against actual use-cases before creating new software.
6. **Retain independent taxonomic and evolutionary sources:** a name checklist is not a phylogeny or behavioral registry.
7. **Do not inflate bibliography maturity:** metadata-only additions and verified article landing pages are not source extraction or independent review.

## Decision and next gate

Keep CSL JSON / status CSV and normalized scientific-evidence CSV as the working archival layout. The next **highest-value deliverable** is **R1 definition-comparison and metadata integrity**, not a new visualization:

- normalize and check the first 6–10 P0 records against authoritative publication records;
- document six core theoretical sources (signal, cue, information, influence, coercion, function);
- compare operational definitions, disagreements and falsifiable tests in one tabular report;
- write/execute a small catalog validator so bad IDs/DOIs/links cannot silently enter;
- preserve all claims as draft until passage-level human review.

**Exit:** a traceable, reproducible first source batch and an explicit unresolved-debate matrix. Further collection should proceed by systematic modality and evidence gaps, not just citation volume.
