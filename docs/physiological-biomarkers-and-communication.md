# Physiological markers, neurobiology and animal communication

**Status: Proposed comparative research axis / targeted literature survey.** Drafted 2026-11-23. This is **not** a validated list of biological indicators, a medical diagnostic guide, an accepted evidence database or permission to conduct invasive experiments.

## Why this belongs in Dr. Dolittle

Communication is produced and received by organisms with nervous, endocrine, cardiovascular, respiratory, metabolic and sensory systems. Measurements of these systems can help evaluate **mechanisms**, **physiological correlates** and **consequences** of specific communicative events. Some bodily changes may themselves be **perceptible cues** to other animals, but an internal measurement is **not automatically a communicative signal**.

**Scope boundary:** hormone release within one organism, neural spikes, cell-to-cell signaling and blood-pressure changes are *physiological mechanisms/measurements*, not automatically animal-to-animal communication. This project remains about the latter.

## Four separate relations (not one causal chain)

1. **Context → internal state:** physiological response to environment, disease, exercise, threat, social contact or reproduction.
2. **Internal mechanism ↔ behavior:** neural and endocrine activity may regulate signal production, perception or social behavior; behavior may also alter physiology.
3. **Externally available cue:** visible breathing, temperature-related color/position changes, an odor or involuntary vocalization may be available to a receiver.
4. **Demonstrated signaling/response:** producer and receiver contingencies plus behavioral or evolutionary evidence support a communicative interpretation.

An increase in a biomarker can be consistent with multiple states; do **not** translate a cortisol, oxytocin or heart-rate number into a word, emotion, intent or universal species label. An internally measured hormone is only a signal **between animals** if a separately defined external interaction is demonstrated.

## Candidate measurement families

| Family | Variables to investigate | Questions and confounders |
| --- | --- | --- |
| Endocrine / neurochemical | Glucocorticoids (cortisol/corticosterone), catecholamines, oxytocin-family and vasopressin/vasotocin-family peptides, sex steroids, neuropeptide receptors | Endogenous state vs context; hormone vs receptor distribution; assay sensitivity; biological matrix; circadian/seasonal and reproductive effects |
| Autonomic / cardiovascular | Heart rate, heart-rate variability (HRV), blood pressure, electrodermal responses where species-appropriate | Arousal, temperature, movement, respiration, cardiac anatomy, baseline, sensor placement; HRV must not become a one-number emotion scale |
| Neural / neurophysiological | Neural spiking, field potentials/EEG, fMRI where justified, immediate-early gene expression, receptor expression | Is the measure a response to a signal, preparation of an act, or an unrelated change? Brain area, method, anesthesia, handling and stimulus controls |
| Respiratory / somatic | Inspiration/expiration timing, sighs, breathing rate, panting, breath-linked vocalizations | Lung maintenance, exercise, temperature, pathology, voluntary and involuntary actions; see [respiratory phenomenon note](respiration-and-communication.md) |
| Thermal / metabolic | Body/skin temperature, oxygen use, metabolism where pertinent | Environment, energetic load, illness and individual variation |
| Immune / biochemical | Inflammatory markers and other verified biomarkers potentially coupled to social challenges | Time lags, low specificity, illness and chronic vs acute physiology |
| Molecular / evolutionary | Genes, peptide-family orthology/paralogy, receptor sequences and expression | Conservation of a molecule does **not** prove conservation of behavior or meaning |

These are **possible measurement families**, not six new sensory modalities, standardized thresholds or lists of proven communication markers. Different taxa have different physiology and suitable methods.

## Evidence anchors (literature leads, not accepted atlas assertions)

| Source | What it contributes | Interpretation boundary |
| --- | --- | --- |
| [Neuroendocrine mechanisms contributing to the coevolution of sociality and communication (2023)](https://doi.org/10.1016/j.yfrne.2023.101077) | Direct theoretical link between social systems, signal production/reception and neuroendocrine mechanisms | Synthesizes hypotheses; cannot assign a hormone a universal communication meaning |
| [Universal nomenclature for oxytocin–vasotocin ligand and receptor families (2021)](https://doi.org/10.1038/s41586-020-03040-7) | Genomic/phylogenetic nomenclature and complex homolog/duplicate peptide families | Similar chemistry does not make two species' social functions identical |
| [Heart rate as a measure of emotional arousal in evolutionary biology (2021)](https://doi.org/10.1098/rstb.2020.0479) | Strengths and limitations of measuring cardiac arousal | Heart rate is neither direct valence nor intentional communication |
| [Selection of appropriate biomatrices for studies of chronic stress in animals (2022)](https://doi.org/10.5187/jast.2022.e38) | Blood, saliva, feces, hair, feathers and different observation windows | Sample matrix and collection method alter what a biomarker can tell us |
| [Finding biomarkers of experience in animals (2024)](https://doi.org/10.1186/s40104-023-00989-z) | Validation difficulties, measurement disturbance and the need for multiple measures | Welfare/experience models are not necessarily animal communication models |
| [Evaluation of indicators of acute emotional states in dogs (2024)](https://doi.org/10.1038/s41598-024-56859-9) | Comparison of candidate behavioral/physiological indicators and confounds | Single markers do not identify a unique emotional state |
| [Central versus peripheral oxytocin concentrations (2017)](https://doi.org/10.1016/j.neubiorev.2017.04.017) | Important warning against assuming peripheral oxytocin tracks brain release, especially at baseline | Do not infer neural events from an unvalidated saliva/plasma proxy |
| [Social familiarity strengthens neural and vocal responses to conspecific calls in zebra finches (2026)](https://doi.org/10.1371/journal.pcbi.1014024) | Example of joint behavioral, neural, auditory and social-context measurements | Neural response to sound does not establish a universal meaning for that sound |
| [Functional and evolutionary implications of gene orthology (2013)](https://doi.org/10.1038/nrg3456) | Why related genes tend to support comparative hypotheses but need functional verification | Orthology and molecular similarity cannot substitute for species-specific physiology |

The linked articles were located and selected in a **targeted discovery pass**, not exhaustively screened. Read methods, participant/sampling details and limitations before extracting accepted assertions.

## Evolutionary comparison: be precise about 'similar hormones'

**Homology** is common evolutionary origin. **Orthology** refers to genes diverged through speciation, and **paralogy** to genes diverged through duplication. **Analogy** is functional resemblance without establishing common ancestry. A hormone's homologous peptide, its receptor ortholog and its physiological role must be recorded separately.

A concrete case is the oxytocin–vasopressin/vasotocin family. Oxytocin, mesotocin, isotocin and related peptides, and vasopressin/vasotocin variants, provide a comparative test case across vertebrate groups. However:
- nomenclature and gene duplication are nontrivial;
- receptors, target tissues and brain-region expression can differ;
- reproductive stage, sex, social organization and context change results;
- functions like bond formation, aggression, care or vocalizing are not one-to-one hormone readouts.

**Comparative hypothesis to test:** some mechanisms regulating *production or reception of social signals* are evolutionarily conserved despite divergent external signal modalities. Need independent phylogeny, receptor/ligand evidence and behavioral tests before calling this demonstrated conservation.

## Proposed data relationship (normalized, provisional)

Add a **physiological measurement** associated with a source-specific scientific assertion, **separate** from sensory modality and observable external behavior. The proposal is reflected in header-only [assertion physiological markers table](../data/evidence/assertion_physiological_markers.csv) and a [proposed controlled family vocabulary](../data/ontology/physiological_marker_families.csv).

Minimum **study-based** fields to preserve:
- marker family and exact analyte or physiological variable; gene, receptor and ligand identities are distinct;
- species/population/individual, tissue or sample matrix, sensor or assay, units and analytical validation;
- endogenous location (central/peripheral), baseline/reference comparator, sample size and controls;
- sampling time relative to **signal produced**, **signal perceived** and behavioral outcome; temporal resolution and lag;
- context: time of day, temperature, exertion, feeding, sex/age, reproductive status, social audience, handling, health;
- observed association and effect/uncertainty, source passage, alternative explanations;
- hypothesized role: producer mechanism, receiver mechanism, state correlate, externally perceptible cue, candidate signal, or unresolved;
- whether the procedure was non-invasive, minimally invasive or invasive; approvals and data permissions when applicable;
- evidence/review state separate from confidence and semantic interpretation.

**No numeric cross-species comparison** without validating assay comparability, different biological matrices, baseline distributions and phylogenetic independence.

## Pilot research questions

1. During conspecific signaling, which endocrine or neural changes correlate with **producing** a signal versus **hearing/perceiving** it?
2. Can jointly measured heart rate/HRV, respiration and observed behavior distinguish a broad arousal response from context-specific communication? What negative controls disprove an association?
3. Do hormone/receptor family homologies predict **comparable mechanisms**, after controlling for divergent ecology, social structure and receptor distributions?
4. How do the signal's timescale (milliseconds to seconds) and hormone sample's timescale (minutes to weeks) limit causal interpretation?
5. Can a non-invasive external physiological cue affect another animal without having evolved or been learned as a deliberate signal?

## Validation and animal welfare

Prefer re-analysis of already published, permission-cleared datasets; use non-invasive recording if later field observations are appropriate. An invasive measurement (blood draw, implant, brain recording) must never be treated as routine or authorized solely because a paper used it. No independent experiments, handling, stress induction or neural interventions are authorized by this proposal.

### Suggested first bounded test

Add **three to five** study-based *draft* biomarker-linked assertions to the R1 evidence pilot, representing a neuroendocrine review, a cardiovascular measure, a validated assay/matrix limitation, and a direct neural-response experiment. Link each to its actual experiment/section and a competing explanation. Preserve `draft` until human review. The key deliverable is correct *classification*, not an emotion recognizer.
