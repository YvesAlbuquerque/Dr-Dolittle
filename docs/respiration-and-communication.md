# Respiratory behavior as a comparative research phenomenon

**Status: Candidate phenomenon / targeted literature survey, 2026-11-23.** This was prompted by an observation that some animals visibly take deep breaths in particular situations. The species, environment, recording, and repeated context of that original observation were not supplied; **it is a hypothesis-generating observation, not a documented behavioral finding**.

## Why it belongs

Our research must include **physiological and bodily events that become perceptible to others**, even if they never prove communicative. Breathing is not, by itself, a sensory *modality*; a respiratory act can generate **visual** chest/body movement, **acoustic** exhalations or vocalizations, tactile airflow, and chemical changes. It may also occur without any receiver.

**Do not classify every deep breath as a sigh.** `sigh`, `snort`, `blow`, `sniff`, `pant`, `yawn`, labored breathing, and respiratory movement can differ in mechanism and circumstance. A visible inhale must be distinguished from an audible exhale, a voiced call, and an inference about emotion.

## Preliminary evidence map

| Source | Observed system and finding reported | What it cannot establish from this study alone | Access |
| --- | --- | --- | --- |
| [Issa & Porostocky, 1993](https://doi.org/10.1016/0034-5687(93)90004-t) | Four unrestrained dogs showed spontaneous sigh breaths during wake, REM and NREM sleep, with post-sigh respiratory changes | That the sigh is necessarily a signal to another animal | PubMed abstract inspected |
| [Soltysik & Jelen, 2005](https://doi.org/10.1016/j.physbeh.2005.06.008) | Rat sigh frequency associated with experimental safety/relief following threat; authors propose possible safety signaling | That another rat detects, uses or benefits from the sigh | PubMed/publisher abstract inspected |
| [Stomp et al., 2018](https://doi.org/10.1371/journal.pone.0197898) | Horse snort rate associated with grazing/pasture and other conditions interpreted as positive; observational welfare correlations | That a snort and a mammalian deep inspiratory sigh are the same act, or that horses intentionally communicate wellbeing | PLOS full paper landing / abstract inspected |
| [Stomp et al., 2018, acoustic variation](https://doi.org/10.1007/s00114-018-1582-9) | Horse snort acoustic structure varied with recorded contexts | That snort types constitute distinct meaningful messages | PubMed abstract inspected |
| [Study (2020), *Role of deep breaths in ultrasonic vocal production*](https://doi.org/10.1152/jn.00590.2019) | Deep inhalations in rats sometimes coordinated with ultrasonic vocalizations, affecting acoustic properties; some social-context variation reported | That the deep breath itself is a stand-alone communicative signal | Publisher/PubMed abstracts inspected; author metadata still needs confirmation |
| [Severs et al., 2022, *The psychophysiology of the sigh: I*](https://doi.org/10.1016/j.biopsycho.2022.108313) | Review of homeostatic/neurological sigh generation and links to arousal | That the same physiological roles or emotional interpretations hold equally across all animal taxa | PubMed/PMC abstract inspected |
| [Purinergic signaling mediates neuroglial interactions to modulate sighs (2023)](https://doi.org/10.1038/s41467-023-40812-x) | Neurophysiological study of sigh regulation; highlights strong endogenous non-communicative mechanisms | That sighs lack all possible social roles | Publisher/PMC abstract inspected |
| [Horse snorts in outdoor conditions (2026)](https://doi.org/10.1007/s00114-026-02113-3) | Temperature and conditions correlated with snort rate; authors also recorded few sighs distinctly | That snorting necessarily reflects social intent or positive emotion independently of temperature and activity | Springer HTML/abstract inspected |

**Metadata caveat:** items above are *research leads* from a targeted survey. The actual methods, full participant counts, coding schemes and competing evidence have **not been comprehensively extracted or independently reviewed**. No row is an accepted atlas assertion.

## Distinguish hypotheses, not merely words

| Candidate explanation | Prediction | Evidence that would distinguish it |
| --- | --- | --- |
| Lung maintenance / respiratory homeostasis | Deep breaths occur without social partners, including during sleep, related to physiology | Physiological recordings, respiratory phase, O₂/CO₂, sleep/arousal controls |
| Arousal or state-related **cue** | Rate/form changes with threat, relief, activity or context, whether or not others are present | Within-individual repeated measures controlling ambient conditions, movement and health |
| Preparation or motor component of vocalization | Inhalation timing predicts vocal production or acoustic contour | Synchronized respiratory, acoustic and body-movement recordings |
| Socially consequential cue | Another animal reliably detects the breath and changes behavior, even if the producer did not evolve to signal it | Receiver response comparison to matched control airflow/acoustic/visual stimuli |
| Communicative signal | Production changes with audience/receiver state and receiver responds adaptively; signal function supported beyond coincident detection | Audience manipulation, playback/replay with controls, developmental or evolutionary evidence |
| Deliberate social messaging | Signaler demonstrates flexible, recipient-directed production, adjusting after failed response | Stronger goal-directed and receiver-sensitive experiments; not inferable from a single sigh |

**Crucial caveat:** these are not a rigid hierarchy. A respiratory act can have a physiological function and simultaneously acquire a social role; functions need not be exclusive.

## Draft recording fields (for a future codebook, not yet accepted ontology)

- `behavior_family = respiratory`; `behavior_label` (sigh/deep_inspiration/snort/blow/sniff/pant/yawn/unknown), with operational measurement criteria;
- source of observation (visual/acoustic/physiological sensor), inspiration/expiration, duration, amplitude/volume where measured, audible characteristics and distance;
- individual identity, sex/age where recorded, social audience, interaction role, other individuals within hearing/visibility;
- contextual states: sleep/wake, exertion, feeding, threat, social contact, temperature, handling, illness/respiratory pathology;
- preceding and following events, repetition, time sync, camera and audio quality, observer confidence;
- receiver change (if any) and controlled comparison;
- interpretation class (`physiological`, `cue`, `candidate_signal`, `unresolved`) and source-specific theoretical justification.

The physical modality axis stays separate from the behavior family. A sigh observed as chest movement is visual; an audible snort is acoustic; one event can have both channels.

## Minimum empirical experiment before interpreting the user's observation

Collect **only voluntary, non-invasive** natural observations if warranted. For each event, annotate a short time window, actor, baseline respiration, context, partners, and changes before/after; include comparable periods with **no** deep breath. Code visible inhale separately from expiration noise. Compare within subject and by context, controlling movement, temperature and health.

**Do not** infer emotional state from a breathing event, disturb animals, induce fear/stress, or treat labored breathing as social signaling instead of a potential health concern.

## Open questions

- Under which ecological/social conditions are respiratory patterns not just diagnostic cues but evolved/learned signals?
- Can receiver responses be demonstrated independently of other simultaneous gestures, sounds or odors?
- How should we compare involuntary physiological emissions with voluntarily produced respiratory acts?
- Do signal/cue definitions from the theoretical literature accommodate learned social interpretation without assuming intention?
- Can respiratory behaviors make the atlas a better *cross-modal physiology-to-communication* reference without expanding into general animal physiology?

**Proposed classification:** `respiration_related_behavior` as a **candidate phenomenon family**, not a new seventh modality and not a confirmed communication capability.
