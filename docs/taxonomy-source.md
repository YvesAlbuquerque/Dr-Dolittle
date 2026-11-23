# Taxonomic authority and species inventory policy

**Decision (2026-11-23):** use [Catalogue of Life (COL)](https://www.catalogueoflife.org/) as the default source of taxonomic names and hierarchy. This is a **taxonomy reference**, not a dataset of communication capabilities, not an exhaustive count of organisms alive, and not necessarily a complete list of all scientifically described species.

## Why Catalogue of Life?

COL provides curated taxonomic checklists, accepted names, synonyms, higher-level classification, downloadable release archives, and versioned records. Its **Base Release** prioritizes scrutinized global sources; the **Extended Release (XR)** increases coverage by integrating additional sources. These are different coverage/quality tradeoffs, not interchangeable editions.

- [COL download and releases](https://www.catalogueoflife.org/data/download)
- [COL access guide and search](https://www.catalogueoflife.org/howto/access)
- [COL metadata](https://www.catalogueoflife.org/data/metadata)
- [ChecklistBank](https://www.checklistbank.org/)
- [GBIF explanation of COL XR migration](https://data-blog.gbif.org/post/catalogue-of-life-taxonomic-backbone/)

## Reproducibility policy

1. Prefer the **COL Base Release** for an initial accepted-name baseline; record the exact release ID/date, dataset DOI, download format, and retrieval date.
2. Consult **COL XR** and specialist taxonomic authorities when the Base Release lacks a taxon; record disagreements and provenance.
3. Never silently update historical analyses to the newest taxonomy. Pin releases for comparisons and provide explicit migration/crosswalks.
4. Store accepted name, taxon identifier **scoped to source/release**, rank, parent, synonyms where needed, and source record.
5. Keep taxonomic entities separate from communicative capability claims. A group-level claim does not automatically apply to every descendant species.
6. Preserve extinct/extant and accepted/synonym distinctions. Document filters before reporting any species counts.
7. Review data licenses and attribution for the **specific release and constituent sources** before redistributing downloaded records. Repository MIT licensing does not relicense external taxonomy.

## Baseline snapshot to pin when data ingestion begins

**Verified release citation:** the [COL metadata page](https://www.catalogueoflife.org/data/metadata) recommends DOI [10.48580/dgzlf](https://doi.org/10.48580/dgzlf) for the 2026-10-16 **Extended** release. Do **not** use this XR DOI to cite the 2026-10-14 Base release without checking its own release-specific citation. The [local source manifest](../data/taxonomy/source-manifest.json) intentionally records both as **not downloaded**.

As observed on COL's release page in November 2026:
- Base: **2026-10-14**, prioritized accuracy, 2,276,639 listed species across all kingdoms.
- Extended: **2026-10-16 XR**, broader coverage, 2,504,814 listed species across all kingdoms.

These are **not animal-only totals**, include extinct species in the COL reporting convention, and are not a complete census of life. Do not present them as such. No taxonomy dump has yet been downloaded, filtered, or ingested.

## Scope and specialist checks

For the first atlas, extract **Animalia** and its descendants from a pinned COL release, then check specialist sources when necessary. We should not select particular species until the capability/group survey makes their inclusion useful.

## Future acceptance criteria

- A version-pinned Animalia inventory with reproducible extraction and source attribution.
- A documented protocol for synonyms, uncertain identifications, and taxonomic changes.
- A crosswalk for any additional biodiversity occurrence or phylogeny source.
- No inferred communicative capacity based only on taxonomic membership.
