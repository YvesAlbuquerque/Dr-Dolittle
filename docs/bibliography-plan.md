# Bibliographic discovery, screening, and provenance protocol

**Status:** Adopted initial collection protocol, **not executed as a systematic or scoping review**. The first broad mapping phase now targets [PRISMA-ScR reporting](review-protocol-r1.md); no registration or exhaustive searching is claimed. See [reading queue](references.md) and [instrumentation choice](research-instrumentation.md).

## Research question

What operational definitions, observed phenomena, measurable capacities and empirical tests allow comparison of animal communication **across modalities and taxonomic groups**? Distinguish communicative signals, cues, coercion/influence, functional effects, learning, and interpretive claims.

## Search sources

- [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) — DOI and publication metadata; deduplication.
- [OpenAlex](https://openalex.org/) — broader scholarly discovery and citation graph; API budget/terms must be respected.
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) — relevant biological and behavioral literature.
- [Semantic Scholar](https://www.semanticscholar.org/) — supplementary discovery; do not treat rankings as quality.
- Direct journal, publisher and scholarly archive records for verification.
- Snowballing from review bibliographies, including [Tanner & Pfennig 2026](https://doi.org/10.1146/annurev-ecolsys-102723-051605).

## Search strategy v0 (candidate strings, not yet executed as a reproducible batch)

Use explicit source-specific syntax and record query, date, endpoint, filters, page or cursor, total retrieved, exclusions, and source API version. Search English literature initially, then evaluate language bias and targeted translation/discovery strategies.

**Conceptual definitions**
```
"animal communication" AND ("signal" OR "cue" OR "influence") AND (definition OR evolution)
"animal communication" AND ("meaning" OR "context" OR "functional reference")
"animal communication" AND ("receiver" OR "audience" OR "multimodal")
```

**Deliberate modality balance**
```
("pheromone" OR "chemical signal" OR "semiochemical") AND ("communication" OR "receiver")
("substrate-borne vibration" OR "vibrational communication") AND animal*
("electric communication" OR "electric organ discharge") AND fish
("visual signal" OR "body pattern" OR gesture) AND animal* AND communication
("animal vocal" OR "bioacoustics") AND ("context" OR "playback")
```

**Capabilities and evolution**
```
("vocal learning" OR "cultural transmission") AND (bird* OR whale* OR mammal*)
("call combination" OR compositionality OR "signal sequence") AND animal*
("phylogenetic comparative" OR convergence) AND "communication"
```

Avoid one undifferentiated high-volume search. Predefine a **stratified discovery quota** per modality and record zero-result strata rather than filling them with irrelevant works.

## Inclusion and exclusions (pilot)

Include peer-reviewed primary studies and scholarly reviews about observable animal signal production/reception, function, context, learning, interaction, or evolutionary mechanism; include relevant analytical methods and comparative datasets as separate types. Book chapters and credible preprints may be included **with type labels**.

Exclude purely metaphorical "communication", human-only linguistics unless comparative controls are relevant, commercial promotional claims without methods, and untraceable AI-generated bibliographic records.

**Do not equate:** a recorded noise with a communicative signal; an open-access article with reusable audio; a taxonomy with behavior annotations; a benchmark classification score with validation of meaning.

## Metadata and screening states

`discovered` → `metadata_checked` → `title_abstract_screened` → `full_text_assessed` → `evidence_extracted` → `independently_reviewed`. An `excluded` state requires a reason.

Every record: stable local ID; title; year; authors (when verified); type; DOI or stable URL; publisher/venue when verified; metadata source/retrieval date; potential modality, taxa and capabilities as **unreviewed discovery tags**; deduplication decision; screening reviewer; accessible full text?; data/code links and separate license terms; methodological concerns.

The **bibliography is not evidence**. An assertion enters the separate evidence register only when its actual study passage, method, tested group/context and competing interpretation are traceable.

## Replicability and review

Use the [blank execution search log](../bibliography/search-log.csv) for **actual** runs only (currently none). Keep a search-log CSV with query version, date, endpoint, result count and retrieval artifacts/checksums when legal. Prefer an ordinary CSL JSON catalog with project-local stable IDs. Preserve import source for manual metadata corrections. On import, deduplicate by normalized DOI first; fallback to normalized title, first author and year with a manual check. Never silently combine distinct reports or preprint/final publication records.

Before claiming a systematic or scoping review, choose and document the review/reporting standard, preregistration decision, exhaustive queries, screening decisions and counts. The current manually curated list makes no such claim.

## Practical sequence

R1a: expand the [public landscape index](related-projects.md). R1b: maintain a 30+ multi-modal bibliographic seed. R1c: ingest CSL JSON + query logs. R1d: critically read the P0 definition debate. R1e: publish controlled vocabulary and reviewed, sourced exemplar claims. R2 begins only after these are traceable.
