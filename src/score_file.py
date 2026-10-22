"""Analyze a new single-track violin MIDI using the exploratory index.
python src/score_file.py path/to/violin.mid --output new_piece.json
This is a rules-based estimate, NOT a trained prediction or exam grade.
"""
import argparse,json
from pathlib import Path
from analyze import analyze,WEIGHTS
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('file',type=Path);p.add_argument('--output',type=Path)
a=p.parse_args()
if a.file.suffix.lower() not in {'.mid','.midi'}: p.error('This pilot accepts MIDI only. Export a single violin part as MIDI; PDF and MusicXML import are future work.')
r,_=analyze(a.file)
r['index_type']='Exploratory rules-based technical-demand index; not a trained predictor'
r['model_version']='0.1';r['weights']=WEIGHTS
out=json.dumps(r,indent=2)
if a.output: a.output.write_text(out+'\n')
print(out)
