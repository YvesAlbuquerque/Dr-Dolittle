# R1 Pilot 01 — Fifteen source-linked observations, not yet reviewed

**Date:** 2026-11-23  
**Status:** Prototyped data transformation + *draft* scientific extraction. **NOT a validated communication atlas.**  
**Sampling:** purposive test set, not a PRISMA-ScR search result or a representative animal census.

## What this pilot actually contains

- **15 atomic source-reported observations**, provisionally extracted from 15 distinct publications; each has a source locator, study context, methodological summary, limitations and an explicitly unreviewed status.
- **Nine sampling groups**, used only to stress-test the representation; they are **not** accepted phylogenetic or taxonomic categories.
- **Seven candidate capability/association tags** and **15 provisional observed-phenomenon labels**. Their definitions are not validated.
- **Five physiological measurement links** (respiration, neural recordings, cardiovascular variability).
- **15 placeholder study appraisals**, all `not_assessed`, and **zero hypothesis-level certainty ratings**. No taxon is matched to a pinned Catalogue of Life release.
- **A source-coverage matrix**, not a trait matrix. Cells show distinct linked *draft papers*, not counts of animals that possess a trait.

## Read the data and visualization

- [R1 draft source matrix (SVG)](figures/r1-draft-coverage.svg)
- [Source counts CSV](figures/r1-draft-coverage.csv)
- [Atomic source-reported observations](../data/evidence/assertions.csv)
- [Scientific paper links and source passages](../data/evidence/assertion_sources.csv)
- [Access level and review provenance](../data/evidence/assertion_screening.csv)
- [Observed phenomena (proposed terms)](../data/ontology/phenomenon_families.csv)
- [Study sampling group and unit of inference](../data/evidence/assertion_sampling_scope.csv)
- [Provisional interpretations kept separate](../data/evidence/assertion_interpretations.csv)
- [Physiological-measure links](../data/evidence/assertion_physiological_markers.csv)
- [Validation script](../scripts/validate_evidence.py) and [visualization generator](../scripts/build_r1_pilot_matrix.py)

## Selected stress tests

| R1 item | Source (DOI or indexed article) | Why we included it | Principal boundary |
| --- | --- | --- | --- |
| 001 | [Vervet alarm-call playback (1980)](https://doi.org/10.1126/science.7433999) | Source-specific receiver behavior | Response need not establish word meaning |
| 002 | [Honeybee recruit flight trajectories (2005)](https://doi.org/10.1038/nature03526) | Directional recruitment with externally recorded paths | This paper does not isolate every perceptual modality |
| 003 | [Sperm-whale coda structure (2024)](https://doi.org/10.1038/s41467-024-47221-8) | Combinatorial timing | Structure is not proven semantics |
| 004 | [Chimpanzee gestural timing (2024)](https://doi.org/10.1016/j.cub.2024.06.009) | Reciprocal non-vocal exchange | Similar latency is not language equivalence |
| 005 | [Cuttlefish lateral display (2012)](https://doi.org/10.1098/rsbl.2012.0435) | Audience-specific visual patterning | Tactical outcome is not proof of conscious deception |
| 006 | [Ant trail pheromone response (2019)](https://doi.org/10.3390/insects10110383) | Chemicals used by unintended recipients | Eavesdropping is not intended cross-species messaging |
| 007 | [Treehopper vibration recruitment (2005)](https://doi.org/10.1098/rspb.2004.3041) | Substrate-borne cooperative recruitment | One studied system is not an insect-wide trait |
| 008 | [Electric fish and robot interaction (2021)](https://doi.org/10.1007/s00422-021-00892-8) | Electric discharge and synchronized responses | Communication and electrolocation overlap |
| 009 | [Dog sighs during sleep (1993)](https://doi.org/10.1016/0034-5687(93)90004-t) | Physiological negative control | No receiver was tested |
| 010 | [Rat sighs and relief (2005)](https://doi.org/10.1016/j.physbeh.2005.06.008) | Context-correlated breath | Hypothesized safety signal not validated |
| 011 | [Horse snorts by context (2018)](https://doi.org/10.1371/journal.pone.0197898) | Audibly observable physiological cue | Context correlation not a proven communicative message |
| 012 | [Rat breath–ultrasound coupling (2020)](https://doi.org/10.1152/jn.00590.2019) | Respiratory mechanism shaping call | Motor component is not necessarily an independent signal |
| 013 | [Zebra-finch vocal and HVC response (2026)](https://doi.org/10.1371/journal.pcbi.1014024) | Neural receiver measurement and context | Neural and behavioral recording arrangements differ |
| 014 | [Dog cardiac/hormonal markers (2024)](https://doi.org/10.1038/s41598-024-56859-9) | Biomarkers associated with study states | Does not demonstrate a signal to another dog |
| 015 | [Macaque tactile grooming initiation (2026)](https://doi.org/10.1111/eth.70075) | Contact-based gesture | Single population and untested culture hypothesis |

**Access boundary:** some items were sourced from publicly accessible publisher/PMC HTML sections; others from a publisher/PubMed abstract only. The [screening CSV](../data/evidence/assertion_screening.csv) records this for each. Source *locations* are section names (not invented page numbers). Full Methods/Results appraisal, effect-size/uncertainty extraction, sample reconciliation and hypothesis-specific evidence synthesis remain pending. A reviewer signature alone is not a claim of validity.

## Stress-test results / ontology critiques

1. **Observation and communication are different types of assertion.** Dog sighs during sleep and dog cardiovascular markers need representation despite no established recipient. The 15 observations are not automatically 15 communicative signals.
2. **Phenomena and sensory channels cannot be collapsed.** Respiration is a motor/physiological event; visual or acoustic cues depend on what was actually perceived/measured. For honeybee recruit tracking, the sensory modality was deliberately left **uncoded**, as this particular paper did not isolate the channel.
3. **Tags are not all capacities.** The pilot includes `physiological_covariation` under an inherited `capabilities` table as a *temporary tagging compromise*. It should likely move to a broader **association/mechanism axis** before the ontology is stabilized.
4. **Inference scopes must be explicit.** Our nine sampling group names are workbench categories. Published species labels are not yet mapped to COL IDs, nor is a taxon-wide trait inferred from a study.
5. **Missing cells must be honest.** The matrix uses dashes for **not covered by these 15 papers**, never for demonstrated absence. It is a biased purposive sample and cannot estimate prevalence.
6. **Review status is orthogonal to source reports and confidence.** An observation tagged `documented_presence` is explicitly *reported in the cited study*, but the record's `draft_unreviewed` state prevents displaying it as scientific consensus.
7. **Conflicting/not-assessed belong to synthesis/coverage.** The validator now restricts *atomic observation states* to documented presence, documented absence under test, and insufficient evidence. Contradictions require separate source records and review, not an overwriting enum.

## Reproduce (stdlib only)

From a repository checkout:

```bash
python scripts/validate_bibliography.py
python scripts/validate_evidence.py
python -m unittest discover -s tests -v
python scripts/build_r1_pilot_matrix.py
```

The generator writes `docs/figures/r1-draft-coverage.csv` and `.svg`. GitHub Actions is configured to run these checks on relevant changes, but a workflow file is **not proof** that GitHub hosted checks passed; inspect the PR checks independently. Tooling validation is not scientific review.

The [first AI-assisted method critique](r1-ai-methodological-critique-01.md) examines four of these studies with explicit source access and abstention. It is an exploratory analysis, **not** a scientific confidence promotion or a stand-in for full independent replication.

## Next decisive gate

Apply the [criteria-based confidence protocol](evidence-certainty-methodology.md) to a **diverse four-source pilot**: (a) alarm playback, (b) chemical eavesdropping, (c) sighs without any recipient, (d) neural response/playback. Capture exact Methods/Results, controls, sampling independence, risks of bias, measurement validity, conflicting evidence and all uncertainty domains. Human/AI assessors can propose assessments with provenance; external replication and falsification matter more than a reviewer's signature. Do **not** assign hypothesis certainty until enough source evidence has actually been appraised.

The next software improvement should move physiological covariation out of the *communicative capability* vocabulary, while preserving existing pilot IDs and transparent versioning.
