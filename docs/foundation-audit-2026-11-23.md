# Foundation audit and research expansion — 2026-11-23

**Status: completed documentation audit and initial source discovery; NOT a completed scientific literature review.**

This audit re-reads the existing Dr. Dolittle repository documents as claims about **scope and method**, distinguishes these from actual empirical evidence, and records what changed.

## What remains coherent

- Project is independent, publicly MIT-licensed for **its own** original work; author-origin history is factual credit, not an extra credit condition.
- Phenomena → operational capacities → broad animal groups → justified species selection is a defensible research **workflow**, not a biological evolutionary sequence.
- Signal/cue, form/function/meaning, observation/inference, missing/absent and similarity/ancestry distinctions are scientifically important.
- Cross-species comprehension remains supporting evidence, rather than a second exhaustive atlas.
- No trained decoding model, validated ontology, benchmark or taxonomy ingestion is claimed.

## Corrective findings

| Topic | Problem in early notes | Adjustment |
| --- | --- | --- |
| Definition of communication | Our signal/cue distinction risked reading as the single agreed definition | Examine adaptive-effect, influence and information theories side by side; retain competing definitions in R1 |
| Modality taxonomy | Earlier tables treated **multimodal** as if it were one physical channel | Treat multimodal as a **relation among two or more modalities**, not an additional sensory channel |
| Emitter/receiver model | Pairwise event language too restrictive | Permit multiple receivers, audiences, background cues, eavesdroppers, propagating media and feedback |
| Animals / sampling | Candidate groups were plausible but not a taxon inventory | Use pinned COL taxonomy, **without** assuming its taxonomy encodes communication |
| Group-level capability | Risk of extrapolating from a single study/species | Report tested group/population, sample structure and phylogenetic dependence; no automatic descendant propagation |
| Evidence strength | "Documented presence" could sound universal | Tie status to a specific test, population, context and observation; preserve contradictions |
| Missing modality coverage | Initial citations skewed vocal and mammalian | Add chemical, vibrational, electrical, visual, and receiver-centered projects and papers |
| Instruments | Proposed JSONL evidence could mix nested claims, reviewers and sources | Adopt CSL JSON + normalized CSV + simple validation; analysis and site generated later |
| Platform claims | APIs, tools, and licensing change | Record checked date, rate limits, third-party license scope and status |
| Navigation | Root README's `../../issues` links point above the repository | Replace with explicit repository issue URLs |

## Core source checks informing the corrections

1. [Scott-Phillips (2008)](https://doi.org/10.1111/j.1420-9101.2007.01497.x), [2010 response](https://doi.org/10.1111/j.1420-9101.2010.01944.x), and [2011 terminology synthesis](https://doi.org/10.1111/j.1420-9101.2011.02386.x): definitions are contested.
2. [Partan & Marler (2005)](https://doi.org/10.1086/431246): multimodal classification is multidimensional.
3. [Tanner & Pfennig (2026)](https://doi.org/10.1146/annurev-ecolsys-102723-051605): communicator–receiver interactions operate in complex environmental and social settings.
4. [Froehlich et al. (2025)](https://doi.org/10.1111/brv.70054): context, function and meaning need operational separation.
5. [Catalogue of Life October 2026 downloads](https://www.catalogueoflife.org/data/download) and [metadata](https://www.catalogueoflife.org/data/metadata): versioned source for names, not behavior.
6. [OpenAlex pricing](https://help.openalex.org/access/pricing/): free API use is budgeted, not an unlimited guaranteed quota.
7. [FishSounds](https://fishsounds.net/), [Pherobase](https://www.pherobase.com/about/), and [Elephant Ethogram](https://www.elephantvoices.org/the-elephant-ethogram-user-guide): distinct types of domain reference.

## Current inventory and confidence

| Deliverable | What exists after audit | Confidence / state |
| --- | --- | --- |
| Project scope, mission, open contribution rules | Existing foundational texts; coherent | Documented |
| Comparative ontology | Six axes, **provisional** definitions; modality correction needed | Proposed |
| Literature landscape | Expanded curated index, 20+ resources | Discovered/linked; licensing and publication audits pending |
| Literature bibliography | 30+ manually located sources; 33 partial CSL JSON seed records | Seed metadata, **not** full text screened |
| Taxonomy reference | COL Base policy and release manifest candidate | Source chosen; **no** Animalia inventory ingested |
| Evidence data | CSV headers and provisional modalities | Scaffolded, **0 reviewed assertions** |
| Validator and tests | JSON schema exists; no runnable automated validation | Not implemented |
| Public atlas | Design only | Not implemented |
| Phylogenetic study | No independently sourced tree | Not started |

## Research priority after audit

**P0:** Critically compare definitions and operational criteria for communication, signal, cue, influence, context, learning and meaning. Work from primary publications and theoretical counterarguments.

**P1:** Automate verifiable, source-provenanced bibliographic metadata ingestion (within free API budgets), screen selected papers, and record limited claim examples from contrasting modalities. Add actual human review and uncertainty.

**P2:** Choose broad comparative strata only after reviewing evidence distribution, then compile a pinned Animalia inventory from COL and resolve specialist sources as needed.

**P3:** Build the first honest coverage matrix after records are validated and reviewed. No scores, rankings of animals, or semantic AI predictions in the public atlas before independent evidence.

## External review requests

Invite researchers to challenge the signal/cue operationalization, multi-recipient model, modality taxonomy, evidence status definitions and sampling bias. GitHub issue discussion is useful for critique but is not, by itself, peer review or empirical confirmation.
