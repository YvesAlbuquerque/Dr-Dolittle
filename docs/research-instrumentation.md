# Research instrumentation — adopted choices and evidence boundary

**Decision date:** 2026-11-23. **Decision: adopted for the first research data pilot.** This is a tooling decision. A basic [offline bibliography validator](../scripts/validate_bibliography.py), [synthetic tests](../tests/test_validate_bibliography.py) and [GitHub Actions workflow definition](../.github/workflows/validate-bibliography.yml) now exist. **Five tests were executed locally using synthetic fixtures**, and the live CSL/status files passed an in-session structural check through the GitHub connector; **a clean-checkout Python run and hosted CI run are not verified**. A 15-study **draft scientific extraction and source-count matrix** now exists in [R1 pilot 01](r1-pilot-01.md). It is not an accepted biological atlas, independent scientific validation or phylogeny. Additional graph-integrity checks and deterministic visualization generation are implemented but their hosted CI status must be checked separately.

## Architectural principle

**GitHub is the canonical, reviewable publication surface. Open text files are the archival source of truth.** Researcher-friendly tools and generated databases are optional adapters. No proprietary service, paid API, always-on server, relational database server, vector database, or AI model is required for R1.

## Selected choices

| Need | Selected tool / representation | Status |
| --- | --- | --- |
| Discovery and DOI metadata | [Crossref REST](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) first; [OpenAlex](https://help.openalex.org/api/) to expand citation and related-work graphs; PubMed for biomedical records | Selected; no harvest run |
| Human reference management | [Zotero](https://www.zotero.org/support/kb/exporting), recommended but **optional**, including CSL JSON import/export | Selected as optional interface |
| Canonical bibliography | **CSL JSON** with stable local `id`, DOI where available, and provenance in a separate review log | Selected; catalog seed may be partial |
| Scientific evidence and review | **Normalized UTF-8 CSV tables** (one claim, one source link, one review per row); foreign keys checked across files | Selected; no scientific assertions accepted |
| Controlled terms | Versioned CSV vocabularies; explicit IDs, definitions and migration notes | Selected |
| Validation | Python stdlib for bibliography, evidence graph, and confidence-record consistency; unittest regression checks | Implemented structure checks; **no scientific inference validation** |
| Analysis | [DuckDB](https://duckdb.org/docs/data/csv/overview) querying CSV directly, materialized Parquet optionally generated and ignored by Git | Selected; not yet benchmarked |
| First public visualization | [Vega-Lite](https://vega.github.io/vega-lite/docs/) matrix, sourced from **reviewed** evidence exports; optional GitHub Pages | Selected; not implemented |
| Derived graph | NetworkX, exportable as GraphML for optional Cytoscape exploration | Later; not implemented |
| Taxonomic names | Version-pinned Catalogue of Life Base; XR/specialists for gap resolution | Policy adopted; no taxonomy ingested |
| Phylogeny | Separate independently sourced and pinned reference tree(s) | Not selected; no evolutionary claims inferred |

### Why normalized CSV over JSONL as the *canonical* evidence representation?

The data must support independent sources, evidence assertions, multiple classification labels, and contradictory reviewers without merging them into one nested object. Small linked tables with stable IDs are easier for collaborators to diff, open in spreadsheet software, and query with SQL. JSONL is still a **possible derived interchange format**, not the initial canonical format.

The price is more tables and explicit referential-integrity validation. This cost is preferable to a flexible JSONL blob with hard-to-review nested changes. **CSV is not itself a semantic schema**: the accompanying field definitions and checks are mandatory.

### Why not a web application now?

We lack reviewed content. A beautiful atlas of unvalidated assertions could falsely imply scientific certainty. The initial public visualization must prominently differentiate **not assessed**, **insufficient**, **conflicting**, **presence in a particular test**, and **absence under a specified test**. Only **methodologically appraised and transparently synthesized** claims may be displayed as evidence with a certainty level; individual human review is not sufficient. The pilot can be displayed as **explicitly provisional source coverage**.

### Physiological evidence extension (2026-11-23)

A new [biomarker research note](physiological-biomarkers-and-communication.md) defines physiology as **source-specific mechanistic/context evidence**, distinct from perceptible communication modalities. The schema is **scaffolded only**: [marker families](../data/ontology/physiological_marker_families.csv) and the header-only [assertion–physiology join](../data/evidence/assertion_physiological_markers.csv). No biomarker values have been ingested or validated.

Add to a later pilot only with units, tissue/matrix, assay, temporal scale, physiological controls and correct evolution terminology. Do **not** infer external animal-to-animal signaling from an internal measurement.

### AI-operated research and source vetting extension

The [AI-first scientific operations design](ai-first-scientific-operations.md) adds independent metadata checks for journal/editorial authenticity, reproducible AI-run manifests, draft method appraisals with precise source locators, and a conjecture ledger. A [deterministic validator](../scripts/validate_ai_readiness.py) enforces schema consistency, but does not judge scientific quality. A bounded [Crossref DOI lookup worker](crossref-metadata-worker.md) is implemented for **explicit opt-in metadata retrieval only**, with local snapshots and offline tests. **A source-grounded [appraisal packet generator](../scripts/build_ai_appraisal_packets.py) and [first draft AI-assisted critique](r1-ai-methodological-critique-01.md) now exist; no autonomous LLM research worker or calibrated evaluator is implemented yet.** Journal prestige and institution name are metadata, not evidence multipliers.

## Conceptual relational entities

```text
references [CSL JSON] 1──N assertion_sources N──1 assertions
                                              │
                                              ├──N assertion_capabilities N──1 capabilities
                                              │
                                              ├──N assertion_modalities N──1 modalities
                                              │
                                              ├──N assertion_taxa N──1 taxa (from pinned COL)
                                              │
                                              └──N reviews
```

Avoid mandatory taxon or capability IDs on raw observations that cannot yet be classified. Group-level claims are **study-scope claims**, never inherited automatically by all descendant species. Contradictory assertions and reviews stay distinct; derived aggregations must show disagreement.

Minimum assertion fields: local ID; literal claim; evidence status; observation-vs-interpretation label; context; methodology/limitations; classification version; review status. Additional linked tables carry citation locations, groups, capabilities and modalities. A source must be traceable to a paper and preferably figure/table/page or experiment section. Do not use machine-generated claims as verified evidence.

## Contribution and review workflow

1. **Discovered** bibliographic reference: DOI/title/URL metadata available. May enter catalog; says nothing about a scientific conclusion.
2. **Screened** reference: scope and inclusion/exclusion reason documented.
3. **Extracted draft**: one atomic assertion supported by a specified source location and defined observational method. AI may draft tags only with an explicit draft flag.
4. **Appraised**: inspect the study's methods, observation, controls, measurement validity, bias, precision and applicability, documenting domain-level reasons and assessor provenance; no automatic promotion after a PR merge.
5. **Disputed**: preserve conflicting studies or assessments; neither a vote nor a single AI output resolves them.
6. **Synthesized with explicit confidence**: evaluate all relevant supporting/opposing/null studies, their independence, heterogeneity and alternative explanations, and issue a **versioned, revisable qualitative certainty assessment**. Independent replication/convergence is more informative than agreement between assessors.

Governance: the founder may curate metadata and propose interpretations but has no authority to make an unsupported claim scientifically true. Human/AI appraisers record method, source and rationale; independent scrutiny is welcome, not a substitute for empirical evidence. See [scientific certainty protocol](evidence-certainty-methodology.md).

## First useful visual

**V0: capability × sampled animal group evidence coverage**. A cell shows counts by *review state* and *evidence state*, with a drill-through to source assertions. In the pilot, assess whether `not_assessed` belongs to a **coverage cell without assertions**, and `conflicting` belongs to a **derived synthesis over separately recorded claims**, rather than both being intrinsic assertion types. Zero-reviewed-studies ≠ biological absence. Display counts per unique study separately from assertions to reduce double counting. Default to "not assessed" for an unexamined cell, not a negative.

**V1:** filter by modality, context and quality; **V2:** network of explicitly supported comparisons; **V3:** overlay an independently sourced phylogenetic tree. More elaborate visualizations are conditional on real reviewed data.

## Data hygiene

- Use UTF-8 CSV (RFC 4180 quoting), lowercase snake_case IDs, stable row order, dates as ISO 8601 and explicit null conventions.
- Git stores only original metadata, curated definitions and compact evidence records; no unauthorized article PDFs, recordings, major taxonomy dumps, caches or generated databases.
- Reference record `id` is a project-local key, never an implicit DOI; track duplicate/alternate DOI identifiers separately.
- Pinned taxonomy releases and retrieval dates belong in a provenance manifest, not in the license header of each assertion.
- Never infer data accessibility or redistribution permission from a public link or from the repository MIT license.
- Prefer small reviewable pull requests and deterministic transformations. Scientific claims must carry provenance and uncertainty.

## Free-tier caveat

OpenAlex documentation in November 2026 describes **$1 of free API usage per day** for a registered free account, with usage-metered calls. It is not accurate to promise unlimited free OpenAlex harvesting. Crossref's public API has dynamic rate limits. Caching, backoff, request budgets and provenance are required before implementing bulk collection.

## First verification slice (partially started; evidence pilot not run)

- 20–30 DOI-checked references spanning **acoustic, visual, chemical, vibrational and electric** signaling.
- 3–5 broad animal sampling groups, without choosing a canonical species list first.
- 10–20 draft evidence assertions, with at least one ambiguous and one conflicting case.
- Tests for missing DOI, duplicate references, broken foreign keys, unknown controlled terms, blank provenance and conflicting reviews.
- Generate V0 from approved evidence only and show all unknown/absence distinctions.
- Confirm that all outputs can be rebuilt offline from a clean checkout and documented tool versions.

**Exit criterion:** validated, repeatable data import + classification + matrix; no research finding is inferred from a successful software build.
