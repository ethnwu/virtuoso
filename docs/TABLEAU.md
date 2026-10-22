# Tableau build and portfolio guide

## Generated starter
Open `tableau/Virtuoso.twbx` in Tableau Public on Mac. This starter contains a landscape dashboard and four editable worksheets. Application-level opening and rendering have not been verified here. The standalone `.twb` uses the two adjacent CSV sources in `tableau/Data`.

## Reliable manual fallback or rebuild
Connect to `data/pieces.csv` as a text file. Treat Piece ID, Piece, Composer, Work, Source URL, License, and Model Version as dimensions. Keep Movement Order as a dimension when sorting.

1. **Technical demand index:** Piece on Rows; AVG(Virtuoso Index) on Columns; Bar marks; show labels; sort descending. Fix the axis at 0–100 if using it as an absolute scale. Subtitle: Experimental index, not a validated difficulty grade.
2. **Density versus chords:** AVG(Notes per Quarter) on Columns; AVG(Chord Onsets Pct) on Rows; Piece on Detail and Label; Circle marks. Each point is one concerto movement, not one note. Add Composer and Work as filters.
3. Add `data/features.csv` as a **separate data source**, without joining it to pieces. **Technical profiles:** Piece on Rows; Feature on Columns; Square marks; AVG(Feature Score) on Color and Label; fix the color scale to 0–100. These are unweighted component scores; Weighted Contribution is available separately.
4. **Pitch range:** use pieces.csv; Piece on Rows, AVG(Highest MIDI) on Columns. Lowest MIDI is also available. MIDI 60 is middle C; MIDI 84 is C6. This is pitch range, not a measured shift/position requirement.
5. Add the first three worksheets to a 1600 × 1500 dashboard. Use cream backgrounds, deep green text, and copper chart marks. Include the index definition and limitation note from the method card.
6. Add a Piece filter on the pieces data source and apply to all worksheets using that source. The technical-profiles worksheet uses a separate source; filter it separately or configure a cross-source relationship/filter deliberately. Do not imply filtering one automatically filters the other.

Keep exploratory index scores distinct from expert ratings. Don't rename the index to an exam grade or claim predictive accuracy.

## Portfolio
Once you have reviewed the workbook in Tableau:
1. Publish it to your Tableau Public profile. Published data is public.
2. Copy the Share / Embed Code from the published visualization.
3. Insert it in your existing portfolio's Virtuoso page. Include a screenshot fallback, a link to open the dashboard, a short method explanation, and a GitHub link to your code.
4. Replace any screenshot or iframe placeholder with the actual published visualization; this starter has not published a dashboard or changed your portfolio.

## Suggested project introduction
Virtuoso analyzes the technical demands of violin concertos. Its first concerto corpus extracts rhythmic density, simultaneous-note frequency, register, and melodic intervals from 25 movements across nine works. An explainable experimental index makes its assumptions visible, while Tableau lets visitors compare technical profiles. A Python tool also analyzes selected violin parts from new MIDI or MusicXML scores. Difficulty prediction against independent expert ratings is future work.
