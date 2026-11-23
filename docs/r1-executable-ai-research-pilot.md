# R1 executable open-science / local AI research pilot

**Date:** 2026-11-23.  
**Status:** **Prototyped implementation** pending real benchmark results and calibration. This pipeline is not an autonomous scientist, not equivalent to human scientific peer review, and not a source of validated biological conclusions.

## Goal and inputs

The [source-first runner](../scripts/r1_research_pipeline.py) takes four [R1 pilot](r1-pilot-01.md) studies: `r1-001` vervet alarm playback, `r1-006` ant chemical cues, `r1-009` dog sigh physiology and `r1-013` zebra finch neural response. They cover clear experiments, potentially misleading semantic interpretation, respiratory physiology, and a complex multi-level neural design.

A reproducible pilot runs on [GitHub Actions](../.github/workflows/r1-live-science.yml), first checking code offline, then launching a *local* Ollama container and the open `qwen2.5:0.5b` instruct model. Unlike the now-retired GitHub Models API, this uses **local model inference**; there is no OpenAI, GitHub Models, or paid model API call. Hosted runner and registry quotas, model licensing and CPU resources still have to be accounted for.

### Steps

1. Match each local reference to the **exact DOI** in Europe PMC's public `search` API (core result format).
2. If the record advertises open access and a plausible PMCID, request `fullTextXML`. Accept JATS **only if the XML matches the DOI and includes an inspectable license and article body**. If Europe PMC returns HTTP 500 or malformed XML, try the **official NCBI PMC Open Access BioC API**, requiring confirmed DOI/PMCID/OA metadata and matching document identity; record that the per-article reuse license still needs inspection. Otherwise use an abstract or abstain.
3. Save a run-local source snapshot, metadata, text sections, selected source excerpts and SHA-256 values. **Do not commit potentially copyrighted full texts**, credentials, or transient snapshots; retain CI artifacts briefly.
4. Feed limited, labeled primary-source passages into a local model with explicit **untrusted source** handling. Require structured output separating observations and controls from alternative hypotheses; do not infer semantics or evolved communicative intent.
5. Validate that cited passage IDs and *exact short quotes* actually appear in the retrieved text, that abstract-only sources abstain from full-method evaluation, and that no scientific confidence value is supplied.
6. Report number of sources acquired, full texts obtained, proposals accepted/rejected **structurally**, errors and model absten­tions. Any proposal is **uncalibrated**, not a verified study appraisal.
7. Never modify `data/evidence/study_appraisals.csv`, `certainty_assessments.csv`, `source_integrity.csv`, or `conjectures.csv`.

The allowlisted retrieval hosts are `https://www.ebi.ac.uk/europepmc/webservices/rest/` and NCBI's [PMC OA BioC API](https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PMC/); the only model URL is loopback `http://127.0.0.1:11434/api/generate`. No arbitrary URL or credential-powered scraping is supported. For production, pin the container and model artifact digests and add provider rate-limit/HTTP 429 monitoring.

### Commands

```bash
# No network, no model, no output files:
python scripts/r1_research_pipeline.py

# Four real source lookups without calling AI:
python scripts/r1_research_pipeline.py --live --model none \
  --output _local/r1/metadata-run

# With your own running local Ollama server, after pulling qwen2.5:0.5b:
python scripts/r1_research_pipeline.py --live --model qwen2.5:0.5b \
  --output _local/r1/with-ollama

python scripts/report_r1_run.py _local/r1/with-ollama
python -m unittest tests.test_r1_research_pipeline -v
```

The output directory must not exist to avoid overwriting provenance. The CI job has a 25-minute limit, and emits an artifact retained for seven days.

## Initial empirical failure modes and corrections

The first four-study source acquisition returned **two abstracts, zero full texts, one HTTP timeout and one record without a DOI search hit**. The latter was recovered through a cited PubMed ID without asserting an unverified DOI; a subsequent run returned **all four abstracts**, but the OA JATS endpoint returned **HTTP 500** for both eligible open-access papers. A fallback to the official NCBI PMC OA BioC JSON endpoint was therefore added, with separate tests.

The first local Qwen run produced **two draft proposals**, each of which cited a real source quote but formatted the passage ID as `p001 Abstract` instead of the strict `p001`; both were initially rejected. The validator now accepts only **exact known passage ID + known section label**, not fuzzy IDs, so that a formatting difference does not masquerade as fabricated evidence. This does not mean the inference itself has been verified.

These observations are source/format and model-fidelity **engineering benchmark results**, not scientific accuracy measurements. See [initial GitHub Actions model run](https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45119621618) and [source-only run](https://github.com/YvesAlbuquerque/Dr-Dolittle/actions/runs/45120235254).

## What the current tests do *not* prove

- Quote matching checks whether a short string occurs in the source, **not** whether the surrounding interpretation is correct.
- A model can misread study design or confidently repeat a passage about something unrelated.
- The source may not include full methods even when tagged `full_text`; license and DOI checks are necessary but not sufficient for completeness.
- The model's independent factual extraction accuracy is **not measured** without a verified, held-out gold reference set and a prespecified scoring method.
- An abstract-only report can still be scientifically useful, but cannot be used to grade methodological details unavailable in the abstract.
- GitHub Actions tests establish code behavior and execution trace; **no confidence level is assigned to any animal communication hypothesis**.

## Scientific validation gate

Before automatic promotion to an appraised record, construct an independent answer key for at least a few full-text papers covering animal count, experimental unit, controls and reported outcomes, evaluate field-wise precision/recall and abstention, run adversarial off-topic passages, test masking of publication/institution names, and measure instability across model versions or prompt changes.

The next step is not a bigger model or more papers by default: **analyse the first real run's failure modes and tune acquisition, citations and refusal behavior.**
