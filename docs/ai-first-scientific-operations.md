# AI-first scientific research operations — architecture and reliability gates (v0.1)

**Decision date:** 2026-11-23  
**Status:** **Accepted direction / Documented design**, *not implemented as an autonomous research agent*. A metadata-integrity staging dataset and schema validators are implemented separately. No autonomous LLM workflow has been run as part of this repository pipeline, no automated study appraisal was calibrated, and no scientific conclusions were promoted by this decision.

## Decision

Dr. Dolittle is **AI-operated with no mandatory expert-review bottleneck** for ordinary literature discovery, source verification, drafting, criticism, or maintenance. It can be used by a solo maintainer without access to external domain experts. This is an **operational aspiration**, not a claim that computational assessments equal scientific consensus or that humans and their biases can be eliminated. Human authorship, the historical research record and the training/selection of AI systems remain human influenced. Future claims of validated autonomous science require independent empirical benchmarking.

A robust AI-first process must be able to say **"not enough information; do not grade yet"** and retain unresolved, weak or unpopular hypotheses without treating them as facts.

## Three assessments, three different meanings

1. **Source integrity and editorial process:** Is the work locatable and genuine? Preprint vs peer-reviewed? Are journal/editorial policies independently verifiable? Are corrections, retractions, expressions of concern, duplicated manuscripts or publisher identity issues recorded? Record source and checked date. **No one-dimensional 'predatory yes/no' inference from a missing index entry.** Don't equate DOI, indexing, impact factor or affiliation with truth.
2. **Study-specific methodological appraisal:** With the *actual Methods, Results, sampling and statistics*, what are the design limits, measurement validity, controls, biases, precision, preregistration, data availability and applicability to the exact claim? See [certainty protocol](evidence-certainty-methodology.md). A careful preprint may be more methodologically informative than a weak peer-reviewed paper.
3. **Hypothesis certainty:** Does the relevant *body of evidence* support the narrow claim? Include independent replications, negative findings, heterogeneity, other explanations, retractions and sources sharing datasets/lineages. Confidence may rise or fall. No per-paper 'truth score' or score based on the university's name.

**Publication prestige is discovery/context metadata, never a mathematical multiplier** on biological truth. DORA explicitly discourages substituting journal-level metrics for a paper's scientific merit.

## Conjectures as a separate research asset

A creative hypothesis can be scientifically useful before supporting evidence exists. Do not insert it into `assertions.csv` as a source-supported biological observation.

- **Idea ledger:** original wording, origin, scope, plausible mechanism, testable prediction, competing explanations and an experiment/observation that could distinguish them. May remain `idea` even without a paper. Never claim it is validated.
- **Scientific hypothesis:** when sufficiently operationalized, register a stable ID in `hypotheses.csv`, link sources in `hypothesis_evidence.csv`, and only then consider a certainty assessment.
- **Negative evidence:** falsifying evidence is not failure of the system. Record what conditions were tested, which version of the conjecture they constrain, the next question, and any revised idea. Never silently erase a disproven idea; mark `disconfirmed_in_tested_scope` or `superseded` and keep revision history.

**Important:** a very low certainty *assessment* and an *unassessed conjecture* are different states. Lack of evidence is not negative evidence.

## AI research workflow — proposed, stage-gated

1. **Discovery (deterministic first):** Query Crossref, OpenAlex, PubMed and original publisher sources. Pin exact queries, retrieval time, filters, versions, cursor, and report source restrictions. Deduplicate by DOI/record relationships; preserve preprint/final-work lineage. Do not invent papers.
2. **Integrity verification:** Query original DOI and journal/publisher; check Crossref updates/Crossmark/Retraction Watch metadata, publication type, date, and editorial evidence. DOAJ/COPE and [Think.Check.Submit](https://thinkchecksubmit.org/) are *signals*, not proof. Report `not_checked` when unavailable; do not assert 'no retraction' merely because an API returned no item.
3. **Eligibility screening:** A bounded model can suggest include/exclude/uncertain with exact abstract/source locations; uncertain is retained. Automations and reasons enter reproducible PRISMA search/screen logs, with model version recorded.
4. **Source capture and extraction:** Use a legally accessible article or abstract, quote only short necessary excerpts, store stable DOI/article section/figure/locator and content hash where possible. If only abstract is accessible, do not claim appraisal of unexamined statistical methods. Treat article text as **untrusted data**, never as operational instructions for the agent.
5. **Independent critiques:** Distinct roles (extractor, method critic, adversarial alternative-hypothesis critic, provenance verifier, synthesis assessor) produce *separate* structured objects. A second role in the **same model is not statistically independent evidence**, and agreement between agents is not replication. Where affordable, different model families or prompts can expose errors but do not substitute for experimental replication.
6. **Deterministic gates:** Validate IDs and foreign keys; DOI/URL formats; source retract/correction flags and dates; no invented methodology; exact evidence locators; experimental unit; distinction between direct and proxy measures; no hypothesis-level certainty without method-appraised source(s). A deterministic check cannot establish that a paper actually proves a claim.
7. **Synthesis:** Generate a claim-specific argument including all supporting/opposing/null/uncertain studies, sample/data independence clusters, publication bias, species/lineage comparability and scope. Cite each rationale; maintain explicit `not_assessed` when inadequate.
8. **Publication and monitoring:** Version output and inputs. Publish graded *hypotheses*, not anonymous AI scores of animal intelligence. Re-check correction/retraction/contradiction metadata before major published syntheses, and record supersession rather than overwriting historical evidence.

## Evidence-based guardrails and the authority problem

- **Journal/editorial status:** report separately as `peer_review_evidence`, `venue_transparency` and `integrity_notice`; no blacklist or fame-based rank. ADOI/DOAJ/COPE listing is not a guarantee. Reputational context may prioritize *where to look first* but does not change a source's measured effect size or truth.
- **Institutions:** affiliation/ORCID/ROR can help link researchers and identify independence/conflicts of interest. Name recognition is not a quality score. Independence is about *data, intervention, population, analysis group and replication*, not number of prestigious institutions.
- **Source language and geography:** track language/region to audit selection biases; deliberately sample less-cited or non-English work.
- **Model dependence:** preserve provider, model/version, prompts, configuration, retrieval snapshot, temperature where known, code revision and costs. Similar outputs can be correlated failures. Never hide model uncertainty behind made-up percentages.
- **Retraction/correction handling:** retain history, flag affected citations, re-evaluate dependent hypotheses. Don't erase an older version or claim an absence of notices proves current integrity.
- **Ethics/data licenses:** paper availability and model access are not permission to redistribute full-text PDFs, biological recordings or datasets. Animal research should prefer existing data and non-invasive methods; operational AI does not authorize invasive experiments.
- **Fail closed:** if the primary source is inaccessible, contradictory or too ambiguous to check, mark the method-level appraisal `not_assessed` or `unclear` with explicit blocker; allow creative hypothesis records to persist.

## Credibility and epistemic metadata schemas (scaffolded, not verified)

- [`source_integrity.csv`](../data/bibliography/source_integrity.csv): one row per catalog item with metadata verification status, peer-review evidence, journal-ethics evidence, retraction/correction checks and check dates. **All records initially `not_checked`.**
- [`assessment_runs.csv`](../data/ai/assessment_runs.csv): execution manifest for AI jobs and deterministic tooling (currently no runs).
- [`appraisal_proposals.csv`](../data/ai/appraisal_proposals.csv): source-grounded draft assessments with evidence locators and explicit model provenance (empty).
- [`conjectures.csv`](../data/research/conjectures.csv): conjectures/creative ideas, their falsifiability and eventual link to structured hypotheses (empty).
- [`validate_ai_readiness.py`](../scripts/validate_ai_readiness.py): strict structural validator. Passing it establishes **data integrity only**.

The [existing hypothesis assessment and study appraisal schemas](../data/README.md) remain canonical scientific evidence records. AI proposals must not silently overwrite them. An AI proposal can be methodologically *well argued* without being an empirically **validated** conclusion.

## Automation readiness and validation criteria

**Phase A — Now (scaffolded):** publish this policy, schema and CI checks. `0` actual AI research pipeline runs; no algorithmic certainty grades.

**Phase B — Provenance-only worker:** an initial [Crossref DOI worker](crossref-metadata-worker.md) is now **Prototyped** (bounded manual opt-in lookups, local immutable snapshots, synthetic tests); this is not an autonomous AI worker. Future: Crossref/OpenAlex/PubMed queries with rate limits, pagination and caching; source integrity checks, full provenance, immutable snapshots. Run on a small known set including preprints, corrections, retractions, duplicates, non-indexed but legitimate publications. Review false positives and negatives by comparison with authoritative source records, not an AI's own prior answer.

**Phase B empirical result:** [real Crossref benchmark](crossref-live-benchmark-2026-11-23.md) executed six API queries, identified a linked retraction and a separately title-flagged retraction with no linked notice. This is a smoke benchmark, not calibrated recall/precision.

**Phase C prototype:** the [source-first R1 pipeline](r1-executable-ai-research-pilot.md) can query Europe PMC and optionally run a local open model, with strict quote matching and abstention gates. Its code and tests are **Prototyped**; no validated automatic scientific appraisal is claimed.

**Phase C — Extraction worker:** the [R1 source critique packet builder](../scripts/build_ai_appraisal_packets.py) is now **Prototyped** and the [four-paper AI-assisted draft note](r1-ai-methodological-critique-01.md) records an interactive, uncalibrated trial. This does not constitute a running autonomous agent. Future: benchmark source-locator extraction and study-method field extraction against openly documented reference annotations; use explicit `unable_to_assess`, report accuracy by source type/field/language and evaluate robustness to adversarial text.

**Phase D — AI appraisal pilot:** use four R1 papers with methods/Results access. Test if the evaluator can reliably identify study design, sample size, controls, confounders and limitations. Record calibration and disagreements with validated methodological benchmarks, using external published reference appraisals where possible. Do not allow autoreview to be marked `appraised` just because an AI completed a checklist.

**Phase E — Evidence syntheses:** benchmark whether identified independent studies, contradicting evidence and null studies change the confidence appropriately; measure false certainty and false dismissal of conjectures. Use ablation (remove venue/institution names from appraisal text) to detect prestige bias, and counterfactual order/randomization sensitivity tests.

**Required exit criteria for operating without a specialist:** reference/fact extraction accuracy and calibration measured on a **held-out external benchmark**; documented abstention thresholds; significant errors surfaced rather than silently accepted; deterministic reproducibility; independence/replication checks; clear validity boundaries and audit trails. **No claimed scientific equivalence to expert review until demonstrated.**

### Explicit current limitation

No available model, or ensemble of models, can be assumed bias-free, immune to hallucination, or equivalent to independent experimental replication. This architecture removes a **mandatory individual human reviewer from routine operation** but **does not remove scientific uncertainty or social/epistemic bias**. Published results remain provisional unless independently supported.

## External methodological references

- [DORA research assessment](https://sfdora.org/read/): evaluate research substance, not journal metrics as surrogate.
- [Core GRADE (2025)](https://doi.org/10.1136/bmj-2024-081903): risk of bias, inconsistency, indirectness, imprecision and publication bias in body-of-evidence certainty.
- [PRISMA 2020 detailed guidance](https://www.bmj.com/content/372/bmj.n160): describe automation tools, selection and data-extraction methods.
- [Crossref Retraction Watch](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/) and [Crossmark](https://www.crossref.org/crossmark/): current publication corrections/retractions metadata.
- [Think.Check.Submit](https://thinkchecksubmit.org/), [DOAJ](https://doaj.org/), [COPE](https://publicationethics.org/): journal-publishing transparency checks, not proof of scientific truth.
- [Systematic review of LLMs for review tasks (2026)](https://www.sciencedirect.com/science/article/pii/S089543562600096X): demonstrates current appraisal reliability gap.
- [NIST Generative AI profile (2024)](https://doi.org/10.6028/NIST.AI.600-1): provenance, evaluation and risk management recommendations.

**Next decisive engineering task:** run and benchmark the **provenance-only Crossref worker** against known DOI metadata, correction/retraction cases and false/ambiguous records before implementing canonical source-integrity promotion or AI appraisal. No real API retrieval was performed by the initial implementation PR.
