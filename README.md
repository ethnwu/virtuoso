# Virtuoso
**The data behind violin difficulty.**

Virtuoso extracts technical features from violin concerto scores and compares them in Tableau. Its Python analyzer also accepts a new MIDI or MusicXML violin part.

## Current concerto corpus

| Composer | Works | Available movements |
|---|---|---:|
| J. S. Bach | BWV 1041; BWV 1042; reconstructed BWV 1056R (II only) | 7 |
| Beethoven | Violin Concerto, Op. 61 | 3 |
| Tchaikovsky | Violin Concerto, Op. 35 | 3 |
| Rieding | Violin Concerto, Op. 35 | 3 |
| Telemann | Violin Concerto, TWV 51:G8 | 3 |
| Vivaldi | Op. 3 No. 3, RV 310; Op. 3 No. 6, RV 356 | 6 |

**9 works · 25 movements · 6 composers · 28,108 encoded solo-part notes.**

These are source-available scores, not a representative sample of every violin concerto. Bach's partitas are no longer the project dataset. Mozart, Mendelssohn, Bruch, and Sibelius are not included yet. BWV 1056R is a reconstruction and only its second movement is available from the selected edition. Solo violin tracks were explicitly checked against the source parts; orchestral/piano accompaniment is excluded. The selected solo lines may contain their own tutti passages.

## What works now
- Reproducible downloads with SHA-256 verification and exact archive-member/solo-track selection.
- Four interpretable features: rhythmic density, simultaneous-note frequency, high-register frequency, and melodic leaps.
- Exploratory index with visible component weights; movement and passage datasets for Tableau.
- New-file analysis for MIDI, MusicXML, and compressed MusicXML; explicit violin-part selection for multi-part files.
- Packaged Tableau starter with rankings, feature profiles, and comparison views.

**The index is a transparent formula, not a trained difficulty predictor or exam grade.** There are currently zero independent difficulty labels. Predictive training and evaluation are not complete. No upload website is deployed.

## Run on Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/build_corpus.py
python src/build_workbook.py
python -m unittest discover -s tests -v
```

Source archives download into ignored `data/downloads/`; the manifest pins their hashes. The note-level audit CSV is generated locally rather than committed. Tableau-ready summaries are committed.

## Analyze a new score

```bash
python src/score_file.py concerto.mid --list-parts
python src/score_file.py concerto.mid --track 8 --output result.json
python src/score_file.py concerto.musicxml --list-parts
python src/score_file.py concerto.musicxml --part 0 --output result.json
```

MIDI tracks and MusicXML parts use **zero-based indices**. Inspect the listing and select the violin solo; do not assume the first violin is the soloist. A multi-part file is rejected until a part is selected. MusicXML is converted to MIDI for this first feature engine, so score-only bowing/fingering details are not modeled. PDF/image recognition is not implemented. Supported input does not guarantee accurate pedagogical difficulty prediction.

## Tableau
Open `tableau/Virtuoso.twbx` in Tableau Desktop Public Edition. If a source needs locating, use the adjacent `tableau/Data` CSV files. The generated workbook's XML, paths, and ZIP integrity were checked, but **it has not been opened or visually verified in Tableau**. See `docs/TABLEAU.md` for a manual rebuild if your Tableau version rejects it.

Publish a reviewed dashboard to Tableau Public and embed it in your existing portfolio. Tableau Public is the reference-corpus explorer; live uploads and individual predictions require a separate application.

## Project files
- `data/pieces.csv`: 25 movement-level feature rows and source attribution.
- `data/works.csv`: nine works with explicit movement coverage.
- `data/features.csv`: 100 component rows.
- `data/passages.csv`: 660 occupied 16-quarter-note onset windows.
- `data/sources.json`: download URLs, archive hashes, licenses, and credits.
- `data/concerto_manifest.json`: exact source members and verified solo tracks.
- `data/ratings_template.csv`: blank expert-label collection sheet; not training labels.
- `data/validation.json`: checks, counts, and solo-track audit.
- `docs/METHOD.md`: index definitions, limitations, and the prediction roadmap.

## Attribution and licenses
Scores originate from the [Mutopia Project](https://www.mutopiaproject.org/). Full per-source attribution and license links are in `data/sources.json` and `docs/SOURCES.md`. Code is MIT licensed. Derived dataset tables are shared under CC BY-SA 4.0; source editions retain their stated public-domain, CC BY, or CC BY-SA status. Files were transformed by selecting the solo part and calculating features. No original source archive is redistributed in the repository.
