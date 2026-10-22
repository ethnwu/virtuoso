# Measurement and model card — version 0.1

## Unit and scope
One movement from one source edition, solo violin only. This pilot includes all eight movements of one Bach partita. It is not a representative sample of violin repertoire. Timings and repeats reflect what is encoded in the MIDI. MIDI note events need not match notated noteheads one-for-one because ties and ornaments can be represented differently; the CSV field `Noteheads` counts encoded MIDI notes.

## Feature extraction
The analyzer merges notes on a single nonpercussion note-bearing track. It pairs each note-on to its note-off by channel and pitch. Quarter beats = (last note ending minus first note onset) in quarter-note units. Simultaneous note-on events form an onset group; onset groups are not the same as sustained polyphony. Consecutive top pitches at onset groups approximate the upper melodic line.

| Component | Raw measure | 0–100 component score | Weight |
|---|---|---|---|
| Density | Encoded note events / quarter beats | min(100, density / 8 × 100) | 35% |
| Chords | Percentage of onset groups starting 2+ notes simultaneously | min(100, chord percentage / 60 × 100) | 30% |
| Register | Percentage of encoded notes at C6 (MIDI 84) or above | min(100, high-note percentage / 50 × 100) | 20% |
| Leaps | Mean absolute interval in semitones between consecutive highest pitches at onset groups | min(100, mean leap / 12 × 100) | 15% |

Virtuoso Index = weighted sum of these component scores. It is a 0–100 theoretical scale, not a percentile and not an exam grade. Weights and anchors are explicit design assumptions, not fitted coefficients, published standards, or expert-certified ratings. A low index does not imply a piece is easy. Do not train an ML model on this formula's own labels and claim to have validated difficulty prediction.

## Important omissions
Tempo is deliberately absent: the source's MIDI tempi are editorial playback settings, not measured performer speeds or a consistent pedagogical standard. Notes-per-quarter is rhythmic density, not notes per second. Chords might be rolled in real performance. Ties, bowing, articulation, string crossings, position shifts, fingerings, endurance, phrasing, expressive control, and player experience are not measured. Pitch does not determine hand position without fingering context. Average features conceal short extreme passages. Register and leaps are only proxies.

Consequently the Sarabande can receive a higher index than a fast Double because chord frequency has a substantial weight and actual playing speed is excluded. This is a useful limitation to investigate, not proof of a real difficulty ranking.

## Toward genuine prediction
1. Assemble a broader licensed corpus with diverse composers, periods, and difficulty levels.
2. Obtain independently sourced expert ratings or comparable syllabus grades. Preserve rating scheme, edition, movement versus full-work scope, and disagreements; different grading systems are not automatically interchangeable.
3. Prefer MusicXML to retain notation details. Select the violin part; use a supported tempo assumption or ask the user for intended tempo.
4. Add local passage features and peak demands rather than whole-piece means alone.
5. Establish a simple baseline before fitting a supervised model. Group train/test splits by complete work and composer to reduce leakage between related movements and arrangements.
6. Evaluate on held-out works with ordinal error, grade-distance accuracy, and honest uncertainty. Have violinists review failure cases.
7. Only then describe outputs as learned difficulty predictions. Restrict claims to supported violin scores and identify unfamiliar inputs.

## Planned product architecture
A small upload application parses a supported violin score, runs the Python feature pipeline/model, and displays a result with reasons. Tableau Public is a complementary, published explorer for the reference corpus and evaluation. Uploading a new score does not automatically refresh a published Tableau Public workbook or create a private user-specific session. A live Python integration needs a separate supported deployment; it is not supplied by this starter.
