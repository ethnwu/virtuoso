# Virtuoso model card — exploratory index 0.1

## Scope and grain
25 movements from nine source-available violin concerto works, six composers. One row is one movement's designated solo violin line. Full orchestral and piano parts are excluded. The solo line can include its own tutti passages. BWV 1056R is a reconstruction represented by its second movement only. Other works contain three source movements; this describes edition coverage, not proof of editorial correctness or completeness of every cadenza.

The corpus is biased toward machine-readable editions available in Mutopia. It cannot establish a universal difficulty standard. There are **22 source-verified rating/placement records** (mixed work, movement, and group scopes), with nine numeric movement candidates after exclusions. Edition comparisons remain pending; no fitted predictive model exists. See `docs/RATINGS.md`.

## Feature definitions
`Noteheads` in the CSV is a legacy name for encoded MIDI note events, not a guarantee of one-to-one correspondence with printed notes. Each note is paired with its note-off on the same channel and pitch. Quarter beats measure last note ending minus first onset; internal rests are included. Onsets group notes beginning at the exact same encoded time. Chord rate counts onset groups starting multiple notes, not every sustained overlap. Leaps follow the highest new pitch at each onset; this is only a proxy for melody or fingering.

| Component | Raw measure | 0–100 component | Weight |
|---|---|---|---:|
| Density | Note events / quarter-note span | min(100, density / 8 × 100) | 35% |
| Chords | Percentage of simultaneous multi-note onsets | min(100, percentage / 60 × 100) | 30% |
| Register | Percentage of note events at C6 / MIDI 84 or higher | min(100, percentage / 50 × 100) | 20% |
| Leaps | Mean absolute upper-onset-pitch interval, semitones | min(100, mean / 12 × 100) | 15% |

Virtuoso Index = weighted sum of the four components. Scale anchors and weights are **unvalidated design choices**, not learned coefficients or expert standards. Zero to 100 is a theoretical scale, not a percentile or grade. A low index does not establish that a piece is easy. Training a model to reproduce these formula-generated labels would not validate actual difficulty.

## Passage windows
`passages.csv` groups note **starts** into fixed 16-quarter-note windows from the MIDI time origin, omits windows with no new notes, and records event counts and starting-note pitch bounds. These windows are not necessarily four bars and do not represent difficulty ratings or complete sustained-note occupancy. The final window can be partial. Window counts reconcile to the movement note-event totals.

## Important limitations
- Editorial MIDI tempo is excluded, so density is not playing speed. A fast movement's real demand can be underestimated.
- Long internal solo rests reduce whole-movement density; final orchestral-only time is outside the solo span.
- Whole-movement means conceal short hard passages. Passage-level features help inspection but are not incorporated into the index yet.
- Notation, ties, ornament realization, repeats, and source MIDI encoding affect event counts.
- MIDI has no reliable bowing, fingering, shifting, string crossings, expressive difficulty, or player-specific experience information.
- High pitch alone does not identify hand position. Simultaneous notes may be rolled. Upper-onset leaps do not equal required finger shifts.
- MusicXML input currently exports only the selected part through MIDI. It does not yet use notation-specific technical features.
- Source editions have not been compared note-for-note with printed critical editions. Source hashes and solo-part mappings establish reproducibility, not musicological infallibility.

## Toward prediction
1. Expand the licensed concerto corpus and include a wider spread of composers and difficulty levels.
2. Extend the curated ratings in `data/ratings.csv`, preserving source, rating scheme, movement/full-work scope, edition, and uncertainty. Blank values are missing, not zero.
3. Add local peak demands, sustained polyphony, intended tempo, and notation-aware features.
4. Fit a simple supervised baseline once independent labels are sufficient. Use grouped train/test splits by **complete concerto**, not random movement/passage rows. Related arrangements and composer overlap require explicit evaluation.
5. Report held-out ordinal error and grade-distance accuracy; review mistakes with violinists. Do not claim performance on unseen composers or unsupported repertoire without testing it.
6. Deploy a separate score-upload application for live results. Tableau Public visualizes the reference corpus and evaluation; it is not an arbitrary-file upload server.
