# R1 — Evidence appraisal, uncertainty and scientific certainty (v0.1)

**Decision dated 2026-11-23. Status:** **Adopted as a provisional assessment protocol**, not yet calibrated, externally tested or applied to the 15 pilot observations. This is the project's own methodology, **informed by**, but **not accredited by**, GRADE, ARRIVE, SYRCLE or PRISMA.

## Principle: evaluation is an argument, not a vote

A paper being published, a person approving it, an AI agreeing with it, a successful CI run or a famous research group are **not** the scientific basis for a biological conclusion. We seek **transparent reasons grounded in methods, measurements, controls, falsifiable predictions and independent evidence**. Human and computational assessors can err. We preserve who/what performed an appraisal, its inputs, limitations, disagreement and revisions.

We distinguish **four different objects**:
1. **Source record:** a bibliographic work and its access/provenance.
2. **Atomic study assertion:** what a particular study reports observing (e.g., a measured sigh, a playback response). Its `documented_presence` is *source-reported*, not a validated communication trait.
3. **Study appraisal:** source-specific assessment of methodological strengths, measurement, bias and applicability for that exact assertion. No global “good paper/bad paper” number.
4. **Hypothesis-level certainty assessment:** a separate, versioned judgment about a **precise testable claim**, considering the **whole relevant body of evidence**, including contradicting and null findings. This is where confidence levels belong.

A “confidence that the paper says X” is not “confidence that X is biologically true.” Verification of transcription, source fidelity, causal inference and external generalization are separate questions.

## Scientific certainty scale

| Level | Interpretation | Expected evidentiary basis |
| --- | --- | --- |
| `not_assessed` | Evidence has not been adequately appraised | The default for **all 15 current draft assertions**; absence of appraisal must not be called low biological confidence |
| `very_low` | Very substantial uncertainty; inference may change fundamentally | Major unresolved bias, indirectness, inadequate controls or only fragile observations |
| `low` | A working interpretation with important unresolved limitations | Some direct evidence, but replication/precision/methodological limits remain |
| `moderate` | Evidence supports a scoped claim with bounded uncertainty | Appropriate controls, reliable measures and reasonably consistent independent evidence, with residual caveats |
| `high` | Robust convergence on a narrowly defined claim | Strong direct evidence, independent replication or converging methods, competing explanations tested, no material unresolved bias |

**These are qualitative assessments, not probabilities.** A mapping such as `high=95%` would be unjustified without a separately specified, calibrated statistical model. A confidence rating is not an evolutionary rank or a fixed trait of a species. **Contradiction** is tracked as a property of the body of evidence, not an additional order on this scale; a hypothesis can remain contested with low or unresolved certainty.

**No algorithm automatically upgrades certainty because more papers exist or because a p-value crosses 0.05.** Even consistent papers can be non-independent, biased or reusing the same dataset.

## Study-level domain appraisal (do not merge into one score)

For a defined assertion, assess:
- **Source access and fidelity:** full study, exact Results/Methods/figure, or abstract only; exact operational words and limitations.
- **Risk of bias/design:** selection, confounding, allocation, blinding where applicable, pseudoreplication, analysis flexibility, and selective reporting.
- **Measurement validity:** how signals, receptor behavior, hormones, neural activity or other outcomes were operationalized, calibrated and sampled.
- **Controls and causal identification:** intervention/playback, comparisons, environmental context, competing sensory cues, physiological and population confounders.
- **Precision and sampling:** experimental unit vs repeated events, uncertainty intervals, missingness, and effective independent sample size.
- **Reporting and reproducibility:** sufficient methods, data/code/protocol access (respecting copyright and animal welfare), transparent exclusion decisions.
- **Directness:** is the test actually about the claimed animal, population, behavior and meaning? Is it only correlational, peripheral biomarker or indirect surrogate?

Record each domain as `low_concern`, `some_concern`, `high_concern` or `unclear` **only after a documented examination**; `not_assessed` is allowed during staging. Some domains are genuinely `not_applicable` and require a justification. **Unreported ≠ absent ≠ low risk.**

ARRIVE 2.0 informs **reporting completeness** for in-vivo animal experiments. SYRCLE informs risk-of-bias assessment of **animal intervention studies** where applicable; neither is a universal quality rating of observational ethology, evolutionary theory or neural analysis. Specify the domain tool and why it fits the design.

## Hypothesis-level synthesis (only when studies are appraised)

For a clear hypothesis with defined population/context/outcome, compare:
1. **Directness of evidence**, including tested emitter/receiver and function versus mere co-occurrence.
2. **Consistency and heterogeneity** across relevant outcomes, contexts and species.
3. **Independence:** overlapping datasets, lab groups, individuals, colonies, lineages and phylogenetic relatedness.
4. **Risk of bias**, measurement validity, controls and attrition across studies.
5. **Precision**, effect size and uncertainty interval when estimable; never confuse null result with equivalence.
6. **Publication and availability biases**, including language, charisma, modality and negative-results gaps.
7. **Competing explanations, falsification attempts and replications**; record supportive, opposing, null and context-only findings.
8. **Generalization:** a well-demonstrated effect in one population does not imply it is universal across a species or related taxa.

For a quantitative meta-analysis use an appropriate model with correlated observations/phylogenetic effects and sensitivity analyses; do not invent a universal weighted point score. Adopt relevant PRISMA-EcoEvo guidance when the review becomes an ecology/evolution systematic synthesis.

## AI-first operational interpretation

The project does not require access to a domain expert to **run** discovery, screening, source-level extraction, method critiques or hypothesis synthesis. Such steps may be proposed by AI if model identity, prompt version, source snapshot, exact evidence locations, calibrated capabilities and any abstention are recorded. **An AI-produced critique is still a critique, not evidence from a new experiment.**

The [AI-first operations design](ai-first-scientific-operations.md) separates journal/editorial authenticity, study-specific methods and body-of-evidence certainty. An apparently prestigious institute, high journal impact or a committee endorsement must not automatically improve biological certainty. The operational workflow is only *Documented*; an AI scientific assessor has not been run, benchmarked or approved for graded conclusions.

## Governance and updating

**Propose → verify provenance → appraise domains → synthesize competing studies → issue a versioned certainty assessment → challenge → update.**

- Any contributor or AI can submit **draft** extractions or domain appraisals with an `assessor_kind`, method, evidence-location and rationale. Automated tools can check syntax/provenance and flag inconsistent claims; they **cannot** certify biological truth.
- Multiple assessors are useful to **measure disagreement and reveal failure modes**, not as a majority-vote mechanism. The human maintainer can curate records but cannot elevate certainty solely by approval.
- An assessment may be revised **up or down** after replication, contradictory data, corrections, retractions, newly found bias or revised operational definitions. Keep prior versions immutable with `supersedes_id`, dated justification and the source set used.
- A `not_assessed` record must never be presented as `very_low`; this would confuse **lack of appraisal** with **weak evidence**.
- High certainty remains **claim- and context-specific**. No system-generated star ratings for species intelligence, emotion, or communication sophistication.

## Data contract and current status

- [`study_appraisals.csv`](../data/evidence/study_appraisals.csv): one appraisal placeholder per existing pilot assertion, **15 records all `not_assessed`**. Domain assessments remain blank until the studies are actually assessed.
- [`hypotheses.csv`](../data/evidence/hypotheses.csv): versioned falsifiable claims. **Header only.**
- [`hypothesis_evidence.csv`](../data/evidence/hypothesis_evidence.csv): positive/negative/null/context-only links, with independence clusters. **Header only.**
- [`certainty_assessments.csv`](../data/evidence/certainty_assessments.csv): versioned hypothesis-level synthesis, supporting rationale, assessor provenance and domain judgments. **Header only.**
- [`validate_confidence.py`](../scripts/validate_confidence.py) checks structural integrity and prohibits unsupported certainty promotion, **not scientific validity**.

**Current scientific state:** 15 candidate observational extractions; **zero completed domain appraisals, zero hypothesis syntheses, zero graded hypotheses**.

## Four adversarial test hypotheses to consider later

Not yet entered as proven claims; define precise operational outcomes and null controls before registration:
1. *Rat sigh as a conspecific safety signal* versus physiological release without any receiver: test recipient reaction independently of threat and sound.
2. *Dog sigh changes reliably with social audience* versus homeostatic sighs during sleep: control rest/sleep, activity and pathology.
3. *Ants use heterospecific trail pheromone cues* versus sender-intended interspecies communication: independently assess sender and receiver selection.
4. *Zebra finch call familiarity predicts differential neural and vocal responses*: require source-level method assessment, independence of samples and carefully bounded neural interpretations.

## Foundational methodology references

- [GRADE/Core GRADE (2025)](https://doi.org/10.1136/bmj-2024-081903): certainty of evidence addresses a **body of evidence**, not mere per-paper voting; **adapt concepts cautiously**, as this is originally healthcare decision research.
- [ARRIVE 2.0 (2020)](https://doi.org/10.1371/journal.pbio.3000410): reporting items for animal experiments, not scientific guarantees.
- [SYRCLE risk-of-bias tool (2014)](https://doi.org/10.1186/1471-2288-14-43): designed for animal intervention studies.
- [PRISMA-EcoEvo (2021)](https://doi.org/10.1111/brv.12721): reporting standards and treatment of dependence/bias in ecology and evolution synthesis.
- [PRISMA-ScR (2018)](https://doi.org/10.7326/M18-0850): descriptive mapping; does not by itself require quality grading. Our certainty protocol supplements rather than replaces scoping-review reporting.

## Next empirical step

Run a **blinded, criteria-driven pilot appraisal of four diverse R1 sources**, checking full methods and results and recording all uncertainty domains. Only then link appropriately scoped falsifiable hypotheses to supporting/opposing/null studies and issue any level above `not_assessed`. Tests may discover that some of these sources are insufficient for an assessed hypothesis; that is a valid research result.

**Do not represent this document as a validated confidence algorithm.** Calibration against independent assessors, repeated assessment, sensitivity to domain changes, and evidence-driven reversals are future requirements.
