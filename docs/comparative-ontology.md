# Comparative communication ontology (v0.1 proposal)

**Status: Proposed.** This is a set of orthogonal *axes*, not a single hierarchy or an evolutionary ladder. A species may participate in multiple systems; a signal may occupy multiple categories.

## Level 1 — broad classification axes

| Axis | Candidate values | Key caveat |
| --- | --- | --- |
| Physical modality | Acoustic, visual, chemical, tactile, substrate-borne vibration, electrical, multimodal | Production and reception may differ; avoid forcing one label |
| Signal structure | Discrete, continuous, graded, rhythmic, sequential, combined | Distinguish physical form from linguistic composition |
| Observed function | Alarm, attraction, affiliation, coordination, solicitation, recognition, competition | Requires behavioral evidence; not automatically meaning |
| Flexibility | Stereotyped, modulated, context-sensitive, learned, socially transmitted | These properties are not a single ordinal scale |
| Interaction organization | Dyadic, group, broadcast, networked, colony-level | Receiver identity and audience effects matter |
| Informational/cognitive capacities | Discrimination, reference-like behavior, combinatoriality, turn-taking, repair, cultural transmission | Strong claims need operational definitions and controls |

## Level 2 — capabilities

For each candidate capability, document:
- **Operational definition:** measurable observable criteria.
- **Alternative explanations:** arousal, context, identity, environment, conditioning, and sampling bias.
- **Evidence type:** observation, controlled experiment, comparative synthesis, or model prediction.
- **Confidence and limitations:** what is supported, what remains uncertain.
- **Applicable systems:** a capability may occur in multiple modalities and groups.

Example: *context-sensitive modulation* means demonstrably different signal production or reception conditional on context, after controlling for individual and recording conditions. It does not automatically imply intentional communication.

## Level 3 — candidate animal groups

Candidate comparative groups include social insects, fishes, birds, social mammals, and cephalopods, with humans as a well-studied reference. These are **sampling strata**, not ranked stages or confirmed capability profiles. Actual group selection requires literature review.

## Level 4 — species and empirical evidence

Only after a group-level evidence survey should the project prioritize species by:
1. relevance to a comparative gap;
2. quality and accessibility of synchronized behavioral and signal data;
3. experimental interpretability;
4. legal, licensing, ethical, and computational feasibility.

## Evidence states

Use **documented presence**, **documented absence under a defined test**, **conflicting evidence**, **insufficient evidence**, **not assessed**, and **hypothesis only**. Record study, method, population, context, and date. Never turn an untested cell into zero.

## Suggested future evidence record

```yaml
capability_id: context_sensitive_modulation
group: null
species: null
modality: null
evidence_state: not_assessed
operational_definition: null
source_doi_or_url: null
study_design: null
observed_context: null
limitations: []
review_status: proposed
```

This schema is illustrative and not yet an implemented database format.
