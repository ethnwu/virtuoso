# Virtuoso
**The data behind violin difficulty.**

Virtuoso is a browser-based violin score lab with a reproducible Python corpus and an editable Tableau workbook. Explore repertoire, compare technical fingerprints, or analyze your own MIDI/MusicXML solo part locally.

**App:** https://virtuoso-score-lab-ethan.ewuf4n.chatgpt.site (owner-private deployment).

## Open the app locally

No npm install or server backend is needed. On Mac:

```bash
python3 -m http.server 8000 --directory web
```

Open http://localhost:8000. Use **Analyze a score → Try Beethoven’s second movement** for a real public-domain example, or upload a `.mid`, `.midi`, `.musicxml`, `.xml`, or `.mxl` file. Select the solo part when multiple parts are present. Processing stays in your browser; there are no analytics or score-upload requests. Internet is needed only to follow external sources.

The app includes a searchable catalogue, movement comparison, component profiles, passage-density charts, custom index weights, nearest feature matches, and JSON/CSV export. Files are limited to 8 MB. PDFs and images are not supported.

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

These are source-available scores, not a representative sample of every violin concerto. Bach's partitas are no longer the project dataset. The expanded catalogue also contains Sibelius Op. 47, Lalo’s *Symphonie espagnole*, Mendelssohn Op. 64, Bruch Op. 26, Brahms Op. 77, Saint-Saëns No. 3, and Mozart Nos. 3–5. These nine additions have official Trinity diploma placements with scope/edition conditions, but their symbolic solo parts have not been verified here. They have **no assigned numerical features or index**. The app therefore has 18 catalogue works, of which 9 are measured. BWV 1056R is a reconstruction and only its second movement is available from the selected edition. Solo violin tracks were explicitly checked against the source parts; orchestral/piano accompaniment is excluded. The selected solo lines may contain their own tutti passages.

## What works now
- Reproducible downloads with SHA-256 verification and exact archive-member/solo-track selection.
- Four interpretable features: rhythmic density, simultaneous-note frequency, high-register frequency, and melodic leaps.
- Exploratory index with visible component weights; movement and passage datasets for Tableau.
- New-file analysis for MIDI, MusicXML, and compressed MusicXML; explicit violin-part selection for multi-part files.
- Packaged Tableau starter with rankings, feature profiles, and comparison views.

**The index is a transparent formula, not a trained difficulty predictor or exam grade.** There are now 22 published rating/placement records across eight works, kept separate by provider and scope. Nine numeric movement candidates remain after scope/arrangement exclusions, all pending edition review. Predictive training and evaluation are not complete. The web app provides rule-based estimates and feature similarity; it does not claim trained prediction accuracy.

## Run on Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/build_corpus.py
python src/build_ratings.py
python src/build_workbook.py
python src/export_web.py
python -m unittest discover -s tests -v
```

Source archives download into ignored `data/downloads/`; the manifest pins their hashes. The note-level audit CSV is generated locally rather than committed. Tableau-ready summaries are committed.

Run the browser engine checks with Node 18+:

```bash
node --test web/tests/engine.test.mjs
```

## Analyze a new score from the command line

```bash
python src/score_file.py concerto.mid --list-parts
python src/score_file.py concerto.mid --track 8 --output result.json
python src/score_file.py concerto.musicxml --list-parts
python src/score_file.py concerto.musicxml --part 0 --output result.json
```

MIDI tracks and MusicXML parts use **zero-based indices**. Inspect the listing and select the violin solo; do not assume the first violin is the soloist. A multi-part file is rejected until a part is selected. The Python CLI converts MusicXML to MIDI; the browser reads written MusicXML durations directly, merges ties, and does not unfold repeats. Grace notes without duration are omitted and reported. In either route, so score-only bowing/fingering details are not modeled. PDF/image recognition is not implemented. Supported input does not guarantee accurate pedagogical difficulty prediction.

## Tableau
Open `tableau/Virtuoso.twbx` in Tableau Desktop Public Edition. If a source needs locating, use the adjacent `tableau/Data` CSV files. The generated workbook's XML, paths, and ZIP integrity were checked, but **it has not been opened or visually verified in Tableau**. See `docs/TABLEAU.md` for a manual rebuild if your Tableau version rejects it.

Publish a reviewed dashboard to Tableau Public and embed it in your existing portfolio. Tableau Public is the reference-corpus explorer; browser uploads are handled by the included static app. The expanded catalogue appears in worksheet 06 as a separate source, preserving the absence of measured features.

## Put it on your portfolio

Deploy the contents of `web/` to any static host (GitHub Pages, Netlify, or your existing site). Keep `engine.mjs`, `data.json`, `vendor/`, and `downloads/` beside `index.html`. There are no API keys, build steps, or paid services. For an iframe, point `src` at **your publicly deployed URL** and include a descriptive title and sufficient height. The current Sites deployment and GitHub repository are private; they are not public portfolio links yet. This project does not change their audience automatically.

## Project files
- `web/`: complete static app; vendored fflate 0.8.2 includes its MIT license.
- `data/known_repertoire.json` / `.csv`: nine additional works with official placements and explicit pending-analysis status.
- `data/pieces.csv`: 25 movement-level feature rows and source attribution.
- `data/works.csv`: nine works with explicit movement coverage.
- `data/features.csv`: 100 component rows.
- `data/passages.csv`: 660 occupied 16-quarter-note onset windows.
- `data/sources.json`: download URLs, archive hashes, licenses, and credits.
- `data/concerto_manifest.json`: exact source members and verified solo tracks.
- `data/ratings.csv`: curated source-verified ratings, with scope and edition conditions.
- `data/ratings_tableau.csv`: a separate published-ratings source for Tableau.
- `data/movement_rating_candidates.csv`: nine numeric candidates, not approved training examples.
- `data/ratings_template.csv`: optional manual collection sheet.
- `docs/RATINGS.md`: findings, sources, and next collection priorities.
- `data/validation.json`: checks, counts, and solo-track audit.
- `docs/METHOD.md`: index definitions, limitations, and the prediction roadmap.

## Attribution and licenses
Scores originate from the [Mutopia Project](https://www.mutopiaproject.org/). Full per-source attribution and license links are in `data/sources.json` and `docs/SOURCES.md`. Code is MIT licensed. Derived dataset tables are shared under CC BY-SA 4.0; source editions retain their stated public-domain, CC BY, or CC BY-SA status. Files were transformed by selecting the solo part and calculating features. No original source archive is redistributed in the repository.
