# Data model — initial scaffold

**Status: Scaffolded, not populated or validated.** The CSV files contain headers only (except proposed modality vocabulary). There are **no accepted scientific claims**, and no taxonomic inventory has been downloaded.

The repository's canonical small structured datasets are UTF-8 CSV with stable IDs and normalized relationships. Bibliography metadata is separately stored in [CSL JSON](../bibliography/catalog/seed.csl.json). DuckDB/Parquet are optional *derived* analytical products, not the source of truth.

## Relation map

- `evidence/assertions.csv`: one atomic scientific assertion and its observation/inference type, context, limitations, evidence state, and editorial review status
- `evidence/assertion_sources.csv`: links assertions to CSL JSON references and precise study locations; an assertion may have multiple sources
- `evidence/assertion_capabilities.csv`: many-to-many assertion/capability classification; empty until definitions exist
- `evidence/assertion_modalities.csv`: many-to-many classification; multimodality is **derived**, not a single modality label
- `evidence/assertion_taxa.csv`: scoped taxon links to pinned taxonomy references; no inheritance to every group member
- `evidence/reviews.csv`: independent reviewer decisions; disagreeing reviews retained
- `evidence/assertion_physiological_markers.csv`: **header-only provisional** study-linked physiological measurement metadata; a biomarker is not a communication channel or a verified claim
- `ontology/physiological_marker_families.csv`: **proposed** physiological/mechanistic evidence families, not a table of validated species abilities
- `ontology/modalities.csv`: **provisional**, descriptive categories, not evidence for animal abilities
- `ontology/capabilities.csv`: empty until operational definitions are reviewed
- `taxonomy/source-manifest.json`: proposed COL source release, with ingestion explicitly marked false

See [biomarker scope and recording limitations](../docs/physiological-biomarkers-and-communication.md). A measurement linking to an assertion must retain an exact source passage, time window and baseline/comparator. Hormone assay comparability and homologous molecule identities must be validated independently of behavior.

## Null and status rules

Blank CSV fields = missing/unknown information, never a documented biological absence. Use only documented evidence states: `documented_presence`, `documented_absence_under_test`, `conflicting`, `insufficient`, `not_assessed`, `hypothesis_only`. In the evidence record, a documented absence **requires** a specified test/context. Separate review states from evidence states.

Scientific claims are accepted only after source-specific human review; seed records and any auto-generated drafts are not reviewed evidence.
