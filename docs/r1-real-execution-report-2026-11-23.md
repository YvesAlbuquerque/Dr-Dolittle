# R1 executable research pipeline — observed benchmark, 2026-11-23

**Status:** initial live source capture **demonstrated**; local LLM inference **executed**, but methodological output **uncalibrated** and no scientific assertion promoted. These results refer to specific GitHub Actions runs, not to an unattended scientific workforce.

## Recorded runs

| Run | Link | Actual result |
| --- | --- | --- |
| First source-only attempt | [45119729100](https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45119729100) | Two abstracts; one source timeout; one DOI search no hit; zero full texts |
| First local Ollama execution | [45119621618](https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45119621618) | A real `qwen2.5:0.5b` model ran; two draft critiques, both abstained on abstract-only material and failed strict quote-pointer format; **zero canonical appraisals** |
| Corrected four-source acquisition | [45120478807](https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45120478807) | **4/4 sources available:** two full JATS XML articles (ant pheromones and zebra finch neural response) plus two abstracts (vervet alarm calls and dog sigh physiology); zero unhandled source errors |
| Follow-up source-only run | [45120725630](https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45120725630) | **4/4 retrieved again:** 2 full JATS XML, 2 abstracts; Results/Methods parent headers preserved in subsequent source passages |
| First full-text local model run | [45120725572](https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45120725572) | Four sources, two full texts. The model produced **two parsed proposals:** one structurally accepted, one rejected for overlong quote; **two other model outputs had malformed/truncated JSON**. All scientific confidence unchanged |
| Nested section and BioC fallback tests | See latest PR #8 checks | Added official PMC OA BioC fallback, explicit PMID abstract fallback, source section hierarchy and exact passage-label support. Distinguish **tested** from **observed live usage** |

The raw snapshots, selected passages, hashes, model outputs and metric reports are attached as short-lived Actions artifacts. **Do not commit entire papers without checking their reuse terms.**

## Structural checks and findings

- Both full JATS records contain an article DOI matching the local bibliography and a parseable article license element. Their source bytes and extracted sections were hashed in the run artifact.
- `r1-006`: 30 source passages, with methods, chemical assay, behavioral bioassays, results, and discussion represented. Subsequent parser improvements preserve the parent `3. Results` heading for nested subsections.
- `r1-013`: 39 source passages, including neurophysiology, behavioral methods, results, statistics and controls; later parsing preserves `Results > [subsection]`.
- `r1-001`: bibliographically matched but abstract-only; cannot grade full Methods/Results.
- `r1-009`: PubMed ID 8210757 retrieved an abstract even when the DOI search did not return a record; the route is flagged separately from a directly successful DOI query, preserving this search discrepancy.

**The full texts were delivered by the Europe PMC JATS XML endpoint** on the successful run. The NCBI PMC BioC adapter is an *additional tested fallback*; claiming that it was used for these two successful acquisitions would be false.

## First local model errors

The first Qwen model wrote the source pointer as `p001 Abstract` instead of bare `p001`. Inspecting the artifacts showed both short source quotes were **verbatim present in their abstract passages**, so the original rejection was a rigid pointer-format failure, not proven quote fabrication. The validator now accepts a passage ID **only with its exact recorded section label**, not fuzzy citation identifiers. A source quote being present is only a structural check: the model can still misinterpret it.

The local model **did not perform a complete methodological appraisal** because that first execution only supplied abstracts. It indicated abstention on both candidate proposals; no confidence value was assigned. These facts demonstrate initial AI proposal generation, but not calibrated scientific competence.

## First full-text model failure analysis

On the follow-up real Ollama run (45120725572), the local `qwen2.5:0.5b` model was given two full JATS texts and two abstracts. The artifact records:

- `r1-001` (abstract): concise source-verbatim quote, exact normalized section pointer, correct **abstention** from completed methodological appraisal; **structurally valid draft only**.
- `r1-009` (abstract): model copied virtually the **entire abstract** as an evidence quote, exceeding the short-quote guard; **rejected** even though the quote text appeared in the article.
- `r1-006` and `r1-013` (full JATS): model generated **unterminated JSON strings**, rejected as `model_error`; no method assessment recorded.

Counts: **4 sources retrieved; 2 with full text; 2 draft JSON proposals parsed; 1 structurally accepted; 1 rejected; 2 malformed responses; 0 confidence assessments.** A successful workflow only says the pipeline caught and recorded the failures, not that model-generated scientific analysis passed.

The prompt was subsequently tightened to cap evidence quotes, minimize generated fields and balance Methods/Results excerpts; its real-world effect must be measured in a separate workflow run, not inferred from code.

## Scientific next gate

1. Repeat the local model test on the now-available full texts, after retaining Results and Methods parent headings.
2. Preserve source identity, article licensing, study unit, controls, section citations and exact short quotes.
3. Build a **held-out, source-anchored reference answer key** and report extraction correctness per field (including false assertions and missing evidence), rather than counting only syntactically valid JSON.
4. Test adversarial prompts in primary text, duplicate/reused samples and prestige-masked metadata.
5. Do not promote study_appraisals, certainty_assessments or capability claims before these empirical controls pass.

**Maturity:** source/transport tooling **Prototyped** with first real success; AI-generated draft critique **Prototyped** with correctness **not validated**; automated scientific assessment **Planned**.
