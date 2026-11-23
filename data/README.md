# Data model — initial scaffold

**Status: Prototyped R1 study pilot, NOT independently scientifically reviewed.** Some CSVs now contain **15 draft source-reported observations** from a purposive test set; there are **no independently accepted scientific claims**, and no taxonomic inventory has been downloaded. See [R1 pilot 01](../docs/r1-pilot-01.md).

The repository's canonical small structured datasets are UTF-8 CSV with stable IDs and normalized relationships. Bibliography metadata is separately stored in [CSL JSON](../bibliography/catalog/seed.csl.json). DuckDB/Parquet are optional *derived* analytical products, not the source of truth.

## Relation map

- `evidence/assertions.csv`: one atomic scientific assertion and its observation/inference type, context, limitations, evidence state, and editorial review status
- `evidence/assertion_sources.csv`: links assertions to CSL JSON references and accessible study sections; an assertion may have multiple sources
- `evidence/assertion_capabilities.csv`: many-to-many assertion/capability classification; empty until definitions exist
- `evidence/assertion_modalities.csv`: many-to-many classification; multimodality is **derived**, not a single modality label
- `evidence/assertion_taxa.csv`: remains empty until pinned Catalogue of Life IDs are verified; no inheritance to every group member
- `evidence/assertion_sampling_scope.csv`: study-as-described group/taxon labels with explicit missing COL match and actual unit of inference
- `evidence/assertion_phenomena.csv`: study-to-provisional observed phenomenon link
- `evidence/assertion_screening.csv`: source URL, access level, extraction provenance and zero independent review
- `evidence/assertion_interpretations.csv`: source-reported observation vs provisional explanation retained separately
- `evidence/reviews.csv`: independent reviewer decisions; disagreeing reviews retained
- `evidence/assertion_physiological_markers.csv`: five source-linked **draft** physiological measurement descriptors, not a measurement dataset or verified communication claim
- `ontology/physiological_marker_families.csv`: **proposed** physiological/mechanistic evidence families, not a table of validated species abilities
- `ontology/modalities.csv`: **provisional**, descriptive categories, not evidence for animal abilities
- `ontology/capabilities.csv`: **seven proposed pilot tags** for stress-testing only; includes `physiological_covariation`, which may later move to a non-capability axis
- `ontology/phenomenon_families.csv`: fifteen provisional event families, not evidence of any species trait
- `taxonomy/source-manifest.json`: proposed COL source release, with ingestion explicitly marked false

See [biomarker scope and recording limitations](../docs/physiological-biomarkers-and-communication.md). A measurement linking to an assertion must retain an exact source passage, time window and baseline/comparator. Hormone assay comparability and homologous molecule identities must be validated independently of behavior.

## Null and status rules

Blank CSV fields = missing/unknown information, never a documented biological absence. Use only documented evidence states: `documented_presence`, `documented_absence_under_test`, `conflicting`, `insufficient`, `not_assessed`, `hypothesis_only`. In the evidence record, a documented absence **requires** a specified test/context. Separate review states from evidence states.

Scientific claims are accepted only after source-specific human review; seed records and any auto-generated drafts are not reviewed evidence. The 15 pilot assertions use `documented_presence` solely for **phenomena reported by their own source** and also use `review_status=draft_unreviewed`; they are never positive, accepted trait assertions. `not_assessed` and `conflicting` belong to derived coverage/synthesis, not to a single study observation. Run `python scripts/validate_evidence.py` from root to check graph integrity and `python scripts/build_r1_pilot_matrix.py` to regenerate the explicitly provisional source-count chart.
