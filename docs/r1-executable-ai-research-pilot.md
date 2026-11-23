# R1 executable open-science / local AI research pilot

**Date:** 2026-11-23.  
**Status:** **Prototyped implementation** pending real benchmark results and calibration. This pipeline is not an autonomous scientist, not equivalent to human scientific peer review, and not a source of validated biological conclusions.

## Goal and inputs

The [source-first runner](../scripts/r1_research_pipeline.py) takes four [R1 pilot](r1-pilot-01.md) studies: `r1-001` vervet alarm playback, `r1-006` ant chemical cues, `r1-009` dog sigh physiology and `r1-013` zebra finch neural response. They cover clear experiments, potentially misleading semantic interpretation, respiratory physiology, and a complex multi-level neural design.

A reproducible pilot runs on [GitHub Actions](../.github/workflows/r1-live-science.yml), first checking code offline, then launching a *local* Ollama container and the open `qwen2.5:0.5b` instruct model. Unlike the now-retired GitHub Models API, this uses **local model inference**; there is no OpenAI, GitHub Models, or paid model API call. Hosted runner and registry quotas, model licensing and CPU resources still have to be accounted for.

### Steps

1. Match each local reference to the **exact DOI** in Europe PMC's public `search` API (core result format).
2. If the record advertises open access and a plausible PMCID, request `fullTextXML`. Accept the XML **only if it matches the DOI and includes an inspectable license declaration and article body**. Otherwise use an available abstract or abstain.
3. Save a run-local source snapshot, metadata, text sections, selected source excerpts and SHA-256 values. **Do not commit potentially copyrighted full texts**, credentials, or transient snapshots; retain CI artifacts briefly.
4. Feed limited, labeled primary-source passages into a local model with explicit **untrusted source** handling. Require structured output separating observations and controls from alternative hypotheses; do not infer semantics or evolved communicative intent.
5. Validate that cited passage IDs and *exact short quotes* actually appear in the retrieved text, that abstract-only sources abstain from full-method evaluation, and that no scientific confidence value is supplied.
6. Report number of sources acquired, full texts obtained, proposals accepted/rejected **structurally**, errors and model absten­tions. Any proposal is **uncalibrated**, not a verified study appraisal.
7. Never modify `data/evidence/study_appraisals.csv`, `certainty_assessments.csv`, `source_integrity.csv`, or `conjectures.csv`.

The currently configured retrieval host is `https://www.ebi.ac.uk/europepmc/webservices/rest/`; the only model URL is loopback `http://127.0.0.1:11434/api/generate`. No arbitrary URL or credential-powered scraping is supported. For production, pin the container and model artifact digests and add provider rate-limit/HTTP 429 monitoring.

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
