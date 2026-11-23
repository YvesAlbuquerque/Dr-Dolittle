# Research instrumentation: records, classification and visualization

**Status: Proposed architecture (2026-11-23).** No software stack has been implemented or benchmarked by this document.

## Design requirements

1. Open formats, reproducible transformations, permissive access, and minimal infrastructure.
2. Keep bibliographic metadata separate from *claims* and *evidence*.
3. Preserve source and taxonomic version provenance.
4. Support multi-label, multi-modal, uncertain, and contradictory classifications.
5. Make manual scientific review possible without requiring programming skills.
6. Avoid premature custom web application or graph database deployment.

## Proposed initial toolchain

| Responsibility | Candidate | Reason | Decision |
| --- | --- | --- | --- |
| Literature discovery | OpenAlex, Crossref, PubMed | Search and DOI metadata | Evaluate coverage, API terms and reproducibility |
| Reference management | Zotero + Better BibTeX export (optional) | Human-friendly reading, tagging, annotation | Candidate; no mandatory hosted account |
| Canonical bibliography | CSL JSON / BibTeX plus stable IDs | Portable, diffable, interoperable | Proposed |
| Taxonomy | Pinned Catalogue of Life release | Traceable names and hierarchy | Adopted source policy; ingestion not implemented |
| Structured records | CSV for flat tables, JSON Schema and JSONL for evidence | Readable and machine-checkable | Proposed |
| Validation | Python, pytest, JSON Schema | Deterministic checks and export generation | Proposed, not installed |
| Local analytical query | DuckDB over Parquet snapshots | Lightweight joins and exploratory analysis | Candidate; no database server required |
| Exploratory notebooks | Jupyter + pandas / DuckDB | Reproducible plots and statistics | Candidate |
| Comparative graph | NetworkX for derived graph; Cytoscape for exploration | Flexible many-to-many links | Candidate |
| Phylogenetic views | Tree of Life sources + compatible phylogeny libraries | Overlay independently sourced trees | Research required |
| Public publication | GitHub Pages + static generated charts | Low-maintenance public exploration | Candidate, not deployed |

## Data model (conceptual)

**Reference**: bibliographic work, DOI/URL, source metadata, access and review status.

**Study**: design, sampling, population, context, controls and limitations; may be linked to multiple references.

**Taxon**: name, rank, parent, accepted/synonym status, source/release identifier.

**Phenomenon**: observable communication-related process, not presumed semantics.

**Communication system**: recurrent patterns of signal production, perception and response, potentially spanning modalities.

**Capability**: independently defined testable property, not a rank of intelligence.

**Evidence assertion**: explicit link between study, taxon or group, phenomenon/system, capability, observed result, evidence status, uncertainty and reviewer.

**Classification scheme**: versioned axes and terms; changing definitions requires migration or preserved historical codes.

All many-to-many relations should have stable IDs and documented provenance. Avoid a single spreadsheet where a paper, species, signal and claim are treated as one row.

## Suggested repository layout (not yet created)

```text
bibliography/
  sources/                 # provenance and search protocols
  catalog/                 # DOI-deduplicated CSL JSON or BibTeX
data/
  taxonomy/                # release manifest; large external data excluded from git
  ontology/                # controlled vocabularies and definitions
  evidence/                # curated assertions, reviews and uncertainty
schemas/                   # machine-readable validation
scripts/                   # import, normalize, validate, build
notebooks/                 # exploratory analysis with pinned dependencies
site/                      # generated static atlas (later)
docs/                      # scientific rationale and methods
```

## Visualization roadmap

**V0: evidence coverage matrix** — axes: capability × animal group; cell: evidence status and number of reviewed studies, never a simplistic present/absent Boolean.

**V1: modality-capability explorer** — filter systems by modalities, signal structure, context and confidence.

**V2: comparative similarity network** — weighted relationships with explicit distance metric, sensitivity analysis, and missing-data handling.

**V3: phylogenetic overlay** — compare similarity with externally sourced evolutionary trees; do not infer shared ancestry from layout.

**V4: study-to-claim provenance view** — click a cell to see papers, operational criteria, conflicting evidence and reviewer notes.

## Scientific safeguards

- Store contradictory claims; do not overwrite them with a consensus Boolean.
- Unknown and not-assessed are distinct from documented absence.
- Review counts measure research effort, not biological capacity.
- Do not silently propagate a group-level observation to every species.
- Record whether each datum is observation, interpretation, hypothesis, or model prediction.
- Dataset licensing and ethics metadata travel with derived exports.
- AI may propose tags, but acceptance of scientific claims remains human-reviewed.
- Cite and pin phylogeny sources separately from Catalogue of Life taxonomy.

## Evaluation before selecting a stack

Run a small vertical slice: 20–30 references, 3 contrasting modalities, 3–5 animal groups, and 10–20 reviewed assertions. Validate DOI normalization, taxonomy lookup, multi-label coding, disagreement capture, export/import, and generation of a coverage matrix.

Choose tools only after this test. Prefer the simplest stack that supports reliable contributions.

## Decisions needed

1. Is Zotero optional or a recommended collaborative interface?
2. Should the first evidence schema use JSONL + JSON Schema, or normalized CSV tables?
3. What are the review roles and criteria for promoting an assertion?
4. Which public interactive views matter most for the first milestone?
