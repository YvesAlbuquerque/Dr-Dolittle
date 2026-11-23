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
- `evidence/reviews.csv`: optional reviewer/disagreement provenance, **not** a scientific truth or promotion authority
- `evidence/study_appraisals.csv`: one per pilot source assertion; **all 15 not_assessed** pending methods/results examination and explicit domain-based reasons
- `evidence/hypotheses.csv`: registered falsifiable claims (currently empty)
- `evidence/hypothesis_evidence.csv`: supports/opposes/null/context-only source-assertion links and independence clusters (currently empty)
- `evidence/certainty_assessments.csv`: versioned hypothesis-level certainty synthesis (currently empty); **the certainty level is not a per-paper reputation score**
- `evidence/assertion_physiological_markers.csv`: five source-linked **draft** physiological measurement descriptors, not a measurement dataset or verified communication claim
- `ontology/physiological_marker_families.csv`: **proposed** physiological/mechanistic evidence families, not a table of validated species abilities
- `ontology/modalities.csv`: **provisional**, descriptive categories, not evidence for animal abilities
- `ontology/capabilities.csv`: **seven proposed pilot tags** for stress-testing only; includes `physiological_covariation`, which may later move to a non-capability axis
- `ontology/phenomenon_families.csv`: fifteen provisional event families, not evidence of any species trait
- `taxonomy/source-manifest.json`: proposed COL source release, with ingestion explicitly marked false

See [biomarker scope and recording limitations](../docs/physiological-biomarkers-and-communication.md). A measurement linking to an assertion must retain an exact source passage, time window and baseline/comparator. Hormone assay comparability and homologous molecule identities must be validated independently of behavior.

## Null and status rules

Blank CSV fields = missing/unknown, never documented biological absence. Atomic source-reported evidence states in the current validator: `documented_presence`, `documented_absence_under_test`, `insufficient`. `conflicting` is a synthesis state, while `not_assessed` means a *coverage or appraisal* has not been assessed. A documented absence requires a specified test and context. **Confidence** is a separate, justified hypothesis-level assessment, never inferred from a mere observation row.

Scientific claims require inspectable, calibrated **methodological appraisal and body-of-evidence synthesis**, not individual human approval or majority vote. Human, AI-assisted and automated assessments must record provenance, methods and contradictions; a code check cannot certify biology. See [certainty methodology](../docs/evidence-certainty-methodology.md) and run `python scripts/validate_confidence.py` for structural checks. All 15 study appraisals are **not_assessed** and there are **zero graded hypotheses**. The 15 pilot assertions use `documented_presence` solely for **phenomena reported by their own source** and also use `review_status=draft_unreviewed`; they are never positive, accepted trait assertions. `not_assessed` and `conflicting` belong to derived coverage/synthesis, not to a single study observation. Run `python scripts/validate_evidence.py` from root to check graph integrity and `python scripts/build_r1_pilot_matrix.py` to regenerate the explicitly provisional source-count chart.
