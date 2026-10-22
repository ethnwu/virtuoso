# Published difficulty labels — first research pass

Checked 2026-10-22. The source records cover eight existing works; no verified rating was matched to the **second** movement of reconstructed BWV 1056R. Its first movement appears in the RCM syllabus, which does not label the movement in our corpus.

## What was added

- 22 source-verified records from Henle, ABRSM, RCM, and Trinity.
- 8 records refer to whole works, 13 to specific movements, and 1 to a combined selection.
- 12 different corpus movements have a specific source placement; multiple sources for one movement are not extra independent examples.
- 9 numeric movement candidate rows remain after holding out arrangements, grouped selections, and diplomas. They are separated by scheme and still need source-edition comparison.
- The strongest single-scheme start is RCM 2021: six numeric movement candidates across four independent concertos. This is insufficient for a convincing generalization claim.

## Selected matches

| Scope | Work / movement | Scheme | Published value | Record |
|---|---|---|---|---|
| Whole work | Bach BWV 1041 | Henle violin | 5 | R001 |
| Whole work | Bach BWV 1042 | Henle violin | 6 | R002 |
| Whole work | Beethoven Op. 61 | Henle violin | 8 | R003 |
| Whole work | Tchaikovsky Op. 35 | Henle violin | 9 | R004 |
| Movement | Rieding Op. 35, I and III separately | RCM 2021 | Level 4 | R008, R009 |
| Movement | Vivaldi RV 356, I and III separately | RCM 2021 | Level 6 | R010, R011 |
| Movement | Bach BWV 1041, I | RCM 2021 | Level 8 | R014 |
| Movement | Bach BWV 1042, I | RCM 2021 | Level 9 | R015 |
| Movement | Tchaikovsky Op. 35, II | ABRSM from 2024 | Grade 8 | R006 |
| Movement | Rieding Op. 35, II | ABRSM 2020–2023 | Grade 3, historical | R007 |

All URLs, source locators, editions, and conditions are in `data/ratings.csv`; provider metadata is in `data/rating_sources.json`. A syllabus listing is a curriculum placement, not an objective universal measure of difficulty or a statement that the piece can only be played at that level.

## Matching rules and exclusions

- **Keep scopes:** a whole-concerto rating does not label each movement. RCM's combined BWV 1042 II+III selection remains a group record; it is not split into two Level 9 examples.
- **Keep schemes:** Henle 8, ABRSM Grade 8, and RCM Level 8 are not interchangeable. Diploma codes stay categorical; they are not converted to numbers above Grade 8.
- **Keep editions:** Telemann I uses a Schroeder arrangement and RV 310 I a Wood arrangement in RCM. Both are held out until compared with our editions. Other work/movement matches still need edition review.
- **Keep conditions:** diploma records requiring a cadenza are held pending coverage checks. Henle's ABRSM cross-reference on the Tchaikovsky product page is not copied as a whole-work Grade 8 rating; the official ABRSM source specifies movement II.
- **Keep history:** Rieding II's ABRSM Grade 3 is explicitly a 2020–2023 placement, not a claim of current exam eligibility.
- **Avoid false instrument matches:** ABRSM also lists Rieding Op. 35 transposed for viola. Those entries do not label our violin score.

`Source Verified` means the provider's published rating/placement was checked. It does not mean our edition was compared note-for-note or the source label was validated experimentally. All training approvals remain pending.

## Files and repeatable checks

Run `python src/build_ratings.py` to validate source identities, scopes, keys, grade ranges, and foreign keys, then recreate:

- `data/ratings_tableau.csv`: one published record per row, for a separate Tableau data source.
- `data/movement_rating_candidates.csv`: numeric single-movement candidates with the existing feature columns; no Virtuoso Index as a training label or predictor.
- `data/rating_coverage.csv`: one row per corpus movement, distinguishing direct, group, and whole-work context.
- `data/ratings_validation.json`: scheme-specific row counts, work counts, and readiness blockers.

Do not join `ratings.csv` directly to `pieces.csv` and sum features: the many-to-one labels can duplicate musical observations. Use separate Tableau sources or intentional relationships. A published-ratings worksheet is included in the generated workbook, which still requires opening and visual QA in Tableau.

## Next data collection

Expand **within one scale** before modeling: prioritize RCM-listed concerto movements at missing levels and add legally usable symbolic scores matching those exact selections. Review the source editions of the six current RCM candidates first. Keep one held-out group per complete concerto; use composer-level holdouts only once there are enough composers. Add labels by editing the curated ratings ledger with a source and scope, not by manually overwriting a generic Expert Grade column.
