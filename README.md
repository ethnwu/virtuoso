# Virtuoso
The data behind violin difficulty.

## What is ready
- A real pilot corpus: eight movements from Bach's Partita No. 1, BWV 1002.
- Features calculated from 4,001 MIDI note events; no invented observations.
- An experimental, explainable technical-demand index.
- CSV sources, a generated Tableau workbook, and reproducible Python code.
- A command-line analyzer for a new single-track violin MIDI file.

**This is a starter, not a trained predictor.** The eight movements have no independently validated difficulty labels. The model cannot currently assign a defensible exam grade or estimate all aspects of playing difficulty. No upload website has been deployed.

## Open on your Mac
1. Install Tableau Desktop Public Edition from https://www.tableau.com/products/public/download.
2. Open `tableau/Virtuoso.twbx`. It packages the two CSV sources with four worksheets and a dashboard.
3. If Tableau asks for a missing source, locate `tableau/Data/pieces.csv` or `tableau/Data/features.csv`.
4. Review the dashboard and save it from Tableau before publishing.

The workbook was generated as Tableau XML. XML structure, source paths, and package integrity were checked, but it has **not been opened or visually verified in Tableau**. If Tableau does not accept the generated workbook, use the manual build guide in `docs/TABLEAU.md` with the verified CSV data.

## Reproduce
From this directory, with Python 3.10 or later:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/analyze.py
python src/build_workbook.py
python src/score_file.py data/raw/violin.mid --output example_result.json
```

`score_file.py` supports a single nonpercussion MIDI note-bearing track. It rejects multi-track scores to avoid silently mixing violin and accompaniment. PDF, image, audio, and MusicXML input are not yet implemented. A PDF recognition stage and a violin-part selector are future work.

## Files
- `data/pieces.csv`: one row per movement, source links, raw features, and index.
- `data/features.csv`: one row per movement and index component.
- `data/note_events.csv`: note-level audit trail, quarter-note time and MIDI pitch.
- `data/metadata.json`: mapping from source MIDI filename to movement title.
- `data/validation.json`: actual validation checks and corpus counts.
- `data/raw/`: original violin MIDI files.
- `src/analyze.py`: feature extraction and explicit scoring formula.
- `src/build_workbook.py`: rebuilds the Tableau workbook and packaged workbook.
- `src/score_file.py`: analyzes a new violin MIDI.
- `docs/METHOD.md`: definitions, limitations, and next steps for ML.
- `docs/TABLEAU.md`: manual build and portfolio publishing instructions.

## Source and attribution
J. S. Bach, Partita I for Solo Violin, BWV 1002. Mutopia Project, ID 180, typeset/maintained by Erik Sandberg. Source page identifies the edition as Public Domain, based on a reproduction of the autograph; updated 2013-01-12.
https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=180
Original MIDI archive:
https://www.mutopiaproject.org/ftp/BachJS/BWV1002/partita-1/partita-1-mids.zip
Movement names/order checked against the corresponding LilyPond archive. The unnumbered `violin.mid` is movement 1; `violin-1.mid` through `violin-7.mid` are movements 2–8. Viola and cello transpositions were excluded.

The source data is public domain. Original project code and documentation in this starter are provided under the MIT License; see LICENSE.
