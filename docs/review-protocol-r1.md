# R1 scoping-review protocol — version 0.1

**Date drafted:** 2026-11-23
**Status:** Proposed protocol, not preregistered, not executed as a reproducible search, not peer reviewed.
**Reporting target:** [PRISMA-ScR](https://doi.org/10.7326/M18-0850) for scoping reviews; see [PRISMA scoping guidance](https://www.prisma-statement.org/scoping). A future narrowly framed effectiveness or causal question may require a full systematic-review protocol instead.

## Purpose and review question

**What operational definitions, physical modalities, observable phenomena, interaction structures, learning properties and evidence methods have been used to describe animal communication across animal groups?** This is a mapping question, *not* an estimate of the prevalence of communication capabilities.

Use the Population–Concept–Context (PCC) frame:
- **Population:** non-human animals, with humans included only where the comparison explicitly illuminates a biological capacity or method.
- **Concept:** communicative signals, informational cues, reception and influence, multimodal exchanges, social learning, structure, and competing definitions.
- **Context:** free-ranging, laboratory and captive observations, comparative theoretical studies, and validated methodological publications. Record context rather than treating them as equivalent.

## Search plan and audit trail

Sources: Crossref (metadata), OpenAlex (discovery), PubMed, specialist journals and backward/forward citation tracing. Use repository [search strategy](bibliography-plan.md) as draft vocabulary; record *exact executed* endpoint syntax separately, because text search differs across sources.

Use a stratified pilot rather than pretending an exhaustive run:
1. Definition / influence / information / receiver / cue debate.
2. Visual, chemical, contact/tactile, substrate vibration and electrical signaling.
3. Acoustic signaling and multimodal integration.
4. Structural organization, contextual modulation, learning/cultural transmission and phylogenetic comparisons.
5. **Physiological mechanisms and biomarkers:** endocrine, neural, cardiovascular/autonomic, respiration, physiological correlates of signal production and perception, ligand/receptor homology, and measurement validity (control for purely clinical biomarkers unrelated to communication).

Before each batch, document source-specific query and syntax, UTC date, filters, language, result total, paging/cursors, request budgets and deduplication. Put actual runs in [search-log.csv](../bibliography/search-log.csv). A heading or example query is *not* evidence a search occurred.

Do not pre-select an article count as evidence of comprehensiveness. Track the number of discovered, deduplicated, screened, excluded (with reason), sought, unavailable and included records. Document citation chasing separately.

## Eligibility and screening

**Include:** peer-reviewed primary studies, critical reviews and theory that clearly define relevant animal communication concepts; open methodological papers; comparative trait databases with identifiable study-level provenance. Mark books and preprints as separate publication types.

**Exclude or flag separately:** detection-only works with no communicative question (unless used as a method reference); human-only work without explicit comparative use; assertions based solely on marketing; unverifiable records; redundant preprint/final-publication pairs (retain both links when useful).

Screen titles/abstracts first, then retrieve authorized full text. Record each inclusion/exclusion decision, responsible reviewer and reason. There is currently no independent second reviewer. Do **not** claim independent screening or scientific validation.

## Charting / extraction template

For each eligible record:
- project-local reference ID, DOI/URL, verified authors/venue/year, source check date;
- evidence type: primary study / theory / systematic/scoping review / methods / dataset;
- taxon and **unit of observation** (individual, dyad, group, population, species, or other); sample characteristics and captive/wild context;
- signal production and perception channels separately, and whether cues or communicative signals were actually tested;
- phenomenon, operational definitions, study design, measured receiver response, sampling/controls;
- any physiological or molecular markers as **separate measures**: analyte or electrophysiological variable, anatomical site, biological sample matrix, sensor/assay, units, timing and latency relative to interaction, central/peripheral origin, within-individual baseline and calibration, physiological confounders and welfare implications;
- explicit role of the marker in the study: source-production mechanism, reception mechanism, state correlate, externally perceivable cue, candidate signal, or unresolved; evolutionary homolog/ortholog/paralog/analog claims require separate sources;
- inferred function, reference, meaning or intention as **separate interpretations**;
- article location (section, page, figure, table, experiment) supporting each assertion;
- uncertainty, alternative explanations, contradictory sources and human review state;
- external data or code license and ethics limitations when applicable.

Record multiple interacting receivers, simultaneous modalities, temporal overlaps, silence, and background/eavesdropper effects when relevant; do not require a single emitter–receiver pair.

## Preventing false inference

- A title/abstract is metadata, not a validated claim.
- A missing study is not a negative finding.
- Evidence for a population does not automatically characterize a species, clade or all instances of a signal.
- A phylogenetic tree comes from an independently cited source, not Catalogue of Life names alone.
- A signal classification and a cognitive/semantic interpretation must be independently supported.
- Review *disagreements* are preserved, not resolved by majority vote.

### Known model ambiguity to test

The current scaffold allows `conflicting` and `not_assessed` as assertion-level `evidence_state` values. In the pilot, test whether these should instead be **derived coverage/synthesis states**: contradictory source-specific assertions remain independently stored, while an unexamined matrix cell may have no assertion row at all. Do not silently migrate an unvalidated schema.

## First review gate

R1 cannot be called a completed scoping review until exact searches, deduplication/screening trail, source-level extraction, full reporting, and PRISMA-ScR coverage exist. Proposed next slice: verify structured metadata of P0 sources, then critically read six cornerstone definitions papers, compare their conflicting terms in a versioned matrix, and draft a handful of sourced examples **marked unreviewed**. No public biological capability map from this alone.

## Methodological precedents

- [Tricco et al. 2018, PRISMA-ScR](https://doi.org/10.7326/M18-0850).
- [Animal Culture Database (2025)](https://doi.org/10.1038/s41597-025-05315-y) — study-linked coding and group/population granularity as an example to evaluate, not copy blindly.
- [Multi-interaction (2026)](https://doi.org/10.1016/j.anbehav.2026.123526) — temporally rich cross-species multimodal analysis; evaluate before custom annotation tooling.
