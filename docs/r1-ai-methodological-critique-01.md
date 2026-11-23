# R1 — First AI-assisted methodological critique (four studies)

**Date:** 2026-11-23.  
**Research operation:** An **interactive ChatGPT/GPT-6 critique** prepared from primary publisher/PubMed pages accessible in this session. This is **not** an unattended repository agent, independently replicated appraisal, calibrated expert-equivalent model, complete systematic review, or a scientific certainty rating. No fixed source-content snapshot is stored, and this document **does not** count as a validated `assessment_runs.csv` execution. The canonical 15 `study_appraisals.csv` remain `not_assessed`.

**Prompt contract:** [R1 methods critic v0.1](ai-methodological-appraisal-prompt-v0.1.md); [input packet generator](../scripts/build_ai_appraisal_packets.py). **Access control:** only the [finch source](https://doi.org/10.1371/journal.pcbi.1014024) had directly inspected full online Methods/Results. Three other records were checked at PubMed abstracts or publisher abstract (full text unavailable or uninspected in this pass). Source access statuses in the original R1 screening may reflect *earlier* lookups; the access table below applies to **this specific critique**.

## Quick methodological record

| Pilot record | Source and access in this critique | Observable source-supported details | Remaining scientific limitations / next discriminating test |
| --- | --- | --- | --- |
| **r1-001: alarm calls** | [Seyfarth et al. 1980](https://pubmed.ncbi.nlm.nih.gov/7433999/), **PubMed abstract and bibliographic record**, no complete Methods read | Three alarm-call classes associated with different predators and distinct conspecific responses, tested using playback; the paper uses the term semantic communication | Full primary Methods/Results and exact playback/randomization/sampling detail not inspected. Testing a stimulus-linked escape response does **not** by itself demonstrate word-like mental representations. Evaluate acoustic control, age and prior experience. **Abstain from methodological certainty.** |
| **r1-006: ant pheromones** | [Chalissery et al. 2019](https://www.mdpi.com/2075-4450/10/11/383), **publisher abstract inspected**; full methods not inspected in this pass | Three sympatric ant species; GC-EAD sensory detection and trail bioassays were reported; *Lasius niger* followed a six-pheromone blend over longer distances than its own trail pheromone | Assay design is appropriate in principle to separate sensing and behavior, but independent sample sizes, allocation, masking, possible deposition/chemical confounds and reproducibility cannot be assessed from this abstract alone. Heterospecific receivers can **eavesdrop**, not necessarily be intended recipients. **Abstain from full methods risk grade.** |
| **r1-009: dog sighs** | [Issa & Porostocky 1993](https://pubmed.ncbi.nlm.nih.gov/8210757/), **PubMed abstract** | Four unrestrained dogs, spontaneous sighs during wake/NREM/REM; respiratory volume and phase timing compared to control breathing | Good boundary case because the study did not test a conspecific receiver. `4 dogs` is an experimental animal count, not a universal species sample; repeated breaths are not independent animals. Full respiratory instrumentation/measurement details absent in this appraisal. **Do not use for social signaling hypotheses.** |
| **r1-013: zebra finch neural response** | [Gomez-Guzman et al. 2026](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014024), **publisher full HTML Methods/Results inspected** | Behavioral design: **seven male** birds and six female companions, familiarity-based playbacks pseudorandomized with silent controls; electrophysiology: **eight male birds** (nine recording sessions), **three also used behaviorally**. Head-fixed recordings use Neuropixels and no ordinary vocal turn-taking; `Fig. 4` neural/behavior correlations are from **three birds across four sessions**. | Study offers strong *design detail* and controls, but behavior and neural data arise from **different experimental arrangements**. Neurons, trials and sessions must not be treated as independent animals. Check bird-level generalization in classification splits, and whether acoustic and familiarity differences are sufficiently controlled. These are investigation questions, not an assertion of data leakage or invalidity. **No hypothesis certainty assigned.** |

## Operational distinctions uncovered by the critique

1. **A source claim, a measurement and a semantic interpretation are different:** behavioral discrimination is not a proof of word meaning; a respiration event during sleep is not evidence of deliberate social signaling.
2. **Experimental unit must be explicit:** neurons, acoustic tokens, repeated trials, individuals, groups and phylogenetic lineages have different dependence structures. Summaries such as `n=9 sessions` cannot substitute for `n=8 birds`.
3. **Methods accessibility drives abstention:** an abstract can verify what its authors reported, but cannot authorize scoring unexamined masking, precise replicates, or design-specific bias domains.
4. **Different simultaneous experiments are not direct mechanism demonstrations:** zebra finch vocal and head-fixed HVC findings support a **correlation across matched conditions**, not direct causal control of calling by those recorded neurons in freely interacting birds.
5. **Source prestige and publication peer review are deliberately masked from inference:** the above critique uses design and observable measurements, not university names or journal metrics.

## Why the current rubric stops here

The project currently has one source-reported observation per record. **Hypothesis-level certainty requires a relevant body of evidence** and conflicting/null studies, not four unrelated papers collectively assigned a single grade. This critique is **preliminary model-generated analysis**, not a completion of the formal appraisals. No changes were made to `study_appraisals.csv` or `certainty_assessments.csv`.

## Concrete calibration tasks

A future model-runner must:
- retrieve and pin exact source-content snapshots and hash, or abstain;
- correctly identify all bird-level and trial-level counts in the finch paper;
- identify that ant abstract access is insufficient to infer full method bias;
- reject the claim that four dogs sighing during sleep demonstrates an animal-to-animal communicative signal;
- distinguish cross-species eavesdropping from intended signaling;
- compare its conclusions under journal/university anonymization;
- output proposal objects only, with precise source section/figure citations, all uncertainties and a record of the actual model execution.

**No probability, confidence tier, editorial truth grade or peer-review substitute is produced here.** The usefulness of this first pass is demonstrating a falsifiable **assessment procedure and its limits**, with material that can later be independently checked or contradicted.
