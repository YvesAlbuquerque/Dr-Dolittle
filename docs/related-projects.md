# Research landscape: projects, labs, archives, and tools

**Survey date:** 2026-11-23. **Status:** curated, non-exhaustive research discovery index; websites were checked for relevance, but licenses, scientific claims, and dataset access have **not** been audited. Links do not imply affiliation, endorsement, or collaboration.

This directory is organized by **what each resource contributes**, rather than claiming all of them attempt to "translate" animals. The Dr. Dolittle research question is different: build a cross-modal, provenance-aware atlas of communication *phenomena and capabilities* before selecting species-specific experiments.

## Research programs and comparative collaborations

| Initiative / official resource | Primary subject | Relevance to the atlas | Role |
| --- | --- | --- | --- |
| [Earth Species Project](https://earthspecies.org/what-we-do/publications/) | AI research on animal communication | Methods and open publications; investigate claims independently | Computational research |
| [Project CETI](https://www.projectceti.org/research/index) | Sperm-whale vocalizations, behavior and AI | Deep study of structure, context, and validation limits | Field + computational research |
| [Wild Dolphin Project](https://www.wilddolphinproject.org/our-research/) | Long-running free-ranging dolphin behavioral research | Linking communication to observed social behavior | Field research |
| [Dolphin Communication Project](https://www.dolphincommunicationproject.org/current-research/) | Dolphin social behavior and acoustic communication | Multisite research and contextual observations | Field research |
| [ElephantVoices / Elephant Ethogram](https://www.elephantvoices.org/the-elephant-ethogram-user-guide) | Elephant behavior, acoustic, visual and seismic communication | Especially relevant: behavior taxonomy that links signal to context | Behavioral atlas |
| [ManyPrimates](https://manyprimates.github.io/) | Distributed comparative primate cognition | Template for multi-site research methods, sampling and open contribution | Collaborative methodology |
| [ManyDogs](https://manydogs.org/) | Distributed research on canine cognition and human–dog communication | Comparative replication and interspecies signals as supporting evidence | Collaborative methodology |
| [University of Minnesota Animal Communication Lab](https://cbs.umn.edu/animal-communication-lab/research) | Signal design, noise, receiver decisions, frog communication | Receiver-side and environmental dimensions | Research lab |
| [Patricelli Lab (UC Davis)](https://patricellilab.faculty.ucdavis.edu/research/) | Visual and acoustic courtship signaling, environmental effects | Mechanism, multimodality and behavioral experimentation | Research lab |
| [Derby Lab (Georgia State)](https://labs.ni.gsu.edu/derby/research/) | Crustacean chemical sensing and communication | Non-acoustic evidence, chemical signals and receptors | Research lab |
| [iMak AI Lab animal communication](https://imak.ai/projects/animals-communication) | ML approaches to animal vocalization | Adjacent exploratory effort; independently verify outputs | Related research lead |

## Existing cross-taxon databases and interaction tooling

| Resource | What it contributes | Boundary / reuse check |
| --- | --- | --- |
| [Animal Culture Database (ACDB)](https://datadiversitylab.github.io/ACDB/) / [source data release](https://github.com/datadiversitylab/ACDB_datarelease) | Comparative records of socially transmitted behaviors, including communicative behaviors, at species/population/group granularity | Not a comprehensive communication atlas; review the specific data-release terms and coding choices before reuse |
| [ACDB web application and methods paper](https://doi.org/10.1002/ece3.71913) | Public exploration of comparative behavioral data; possible reference for our visualizations | Assess use and maintenance cost before writing a bespoke atlas front end |
| [Multi-interaction (2026)](https://doi.org/10.1016/j.anbehav.2026.123526) / [institutional summary](https://www.ilcb.fr/multi-interaction-a-new-open-access-approach-for-studying-multimodal-communication-and-interactions-across-species/) | Open-access analysis approach addressing multimodal overlap, simultaneous exchange and silence | Tool capability, code availability and license need direct evaluation |

## Structured domain resources (important for modality balance)

| Resource | Primary content | Research-use caution |
| --- | --- | --- |
| [The Pherobase](https://www.pherobase.com/about/) | Pheromones, semiochemicals and associated scientific literature | Specialized chemical ecology; database material is **not** automatically MIT-licensed |
| [FishSounds](https://fishsounds.net/) | Fish sound records, references, terminology and some recordings | Sound production or detection alone does not establish social communication |
| [BirdNET](https://birdnet.cornell.edu/about/) | Bioacoustic species identification and monitoring | A species classifier is not a semantic translator |
| [Xeno-canto](https://xeno-canto.org/) | Community recordings of wildlife | Check the license and provenance of **each recording** |
| [Macaulay Library](https://www.macaulaylibrary.org/) | Animal audio, images and video | Access for research and redistribution can be different; request licensing as needed |
| [Animal Sound Archive (Berlin)](https://www.museumfuernaturkunde.berlin/en/research/collection/animal-sound-archive/) | Historical and contemporary animal sounds | Check archive-specific access and reuse rights |
| [Movebank](https://www.movebank.mpg.de/cms/movebank-content/about-movebank) | Animal movement and tracking data | Useful context, **not** automatically communication labels; study-specific access |
| [Ocean Voices (Zooniverse)](https://www.zooniverse.org/projects/annelistens/ocean-voices) | Citizen-science identification of cetaceans in audio | Detection and labeling, rather than validated signal interpretation |

## Reusable computational baselines and literature discovery

| Resource | What to inspect |
| --- | --- |
| [Earth Species Project — BEANS](https://github.com/earthspecies/beans) | Bioacoustic ML benchmark spanning multiple animal groups |
| [Earth Species Project — NatureLM-audio](https://github.com/earthspecies/NatureLM-audio) | Audio model research; model outputs must not be treated as evidence of meaning |
| [Earth Species Project — alp-data](https://github.com/earthspecies/alp-data) | Uniform access to many bioacoustic datasets; audit original dataset licenses |
| [Earth Species Project — AVES](https://github.com/earthspecies/aves) | Self-supervised animal vocalization representations |
| [Talk2Nature resources](https://metivity.github.io/talk2nature/research/resources/) | Secondary discovery directory; verify each citation and link at its source |

## Coverage assessment

The current ecosystem is **not evenly distributed across modalities**. Many public AI and archival efforts are sound-centered. Our atlas should deliberately seek chemical signaling, visual displays, tactile interaction, substrate-borne vibration, and electrocommunication, even where the strongest evidence exists only in conventional papers rather than named open-source projects.

An institutional lab, a research consortium, an online archive, a biodiversity database, and a software model are **different resource types**. They must not be presented as directly comparable accomplishments.

## How to submit a new resource

Record: official URL; organization; resource type; group(s); modality or methods; public outputs; date last checked; evidence/metadata quality; code license; dataset license; potential overlap with the atlas. Leave license/access fields **unknown** unless confirmed by official terms. Prefer a project page and at least one primary publication to validate scientific claims.

**Maintenance rule:** review this index periodically; a working URL does not prove an active project, an open-access article does not prove open data, and an open-source model does not prove validated communication decoding.
