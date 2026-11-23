# Schema and validation plan

This folder contains a **proposed row-level** [JSON Schema](assertion-row.schema.json) for `data/evidence/assertions.csv` after CSV is parsed into dictionaries. It is not a claim that a validator or CI has already run.

Additional required validation still to implement: header consistency, unique primary keys, reference IDs found in CSL JSON, all assertion/source links resolved, modalities/capabilities in vocabulary, date values, linked COL release, absence requiring tested context, and no claim promoted without documented review.

Scientific validity is **not** guaranteed by structural validation. The full pilot must test this schema with both valid and deliberately malformed records and document the results before claiming validation.
