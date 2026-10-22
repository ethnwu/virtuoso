# Score sources and attribution

All archive hashes and exact URLs are recorded in `data/sources.json`. Derived feature tables: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). Changes: source-part selection, numerical feature extraction, and normalization; no original archives redistributed.

| Source | Contributor | License | Source page |
|---|---|---|---|
| bach1041 | Federico Bruni and Javier Ruiz-Alma | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [Mutopia 2051](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=2051) |
| bach1042 | David Chan | [Public Domain](https://www.mutopiaproject.org/legal.html#publicdomain) | [Mutopia 29](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=29) |
| bach1056 | Júda Ronén | [Public Domain](https://www.mutopiaproject.org/legal.html#publicdomain) | [Mutopia 2116](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=2116) |
| beethoven1 | Stelios Samelis | [Public Domain](https://www.mutopiaproject.org/legal.html#publicdomain) | [Mutopia 990](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=990) |
| beethoven2 | Stelios Samelis | [Public Domain](https://www.mutopiaproject.org/legal.html#publicdomain) | [Mutopia 1021](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=1021) |
| beethoven3 | Stelios Samelis | [Public Domain](https://www.mutopiaproject.org/legal.html#publicdomain) | [Mutopia 1165](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=1165) |
| tchaikovsky | Will Oram | [Public Domain](https://www.mutopiaproject.org/legal.html#publicdomain) | [Mutopia 466](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=466) |
| rieding | Michael Fischer v. Mollard | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | [Mutopia 1781](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=1781) |
| telemann | Elias Hernandis | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [Mutopia 2231](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=2231) |
| vivaldi | Felix Janda | [Public Domain](https://www.mutopiaproject.org/legal.html#publicdomain) | [Mutopia 2048](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=2048) |

## Editorial checks

Beethoven track names are generic (`eight`, `four`, `eight` for movements I–III); the LilyPond staff definitions map those names explicitly to `violinoprincipale`. Tchaikovsky uses `solo:`, Telemann `violinoP:`, and the other selected sources provide violin-only files. The manifest retains expected track names and source note counts.

Vivaldi archive folders must remain intact because each concerto reuses filenames. Only solo concertos III and VI are included; four- and two-violin works are excluded. The folder 6 header repeats RV 519, while its subtitle and A-minor notes identify Op. 3 No. 6. The catalogue number is corrected to RV 356 using the source collection listing and the publisher catalogue: https://www.halleonard.com/product/49019365/antonio-vivaldi-concerto-no-6-in-a-minor-op-36-rv-356 . This correction is recorded in the row-level scope note.

BWV 1056R contains movement II only in this edition and is explicitly marked partial. No absent movements were fabricated. Rieding is placed in the broad Romantic-era grouping for this project; the source website labels its style Classical. Period is descriptive metadata, not a trained feature.
