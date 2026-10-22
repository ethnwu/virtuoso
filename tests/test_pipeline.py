import unittest,tempfile,subprocess,sys,json
from pathlib import Path
import mido
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analyze import analyze
ROOT=Path(__file__).resolve().parents[1]
class ExtractionTests(unittest.TestCase):
 def test_explicit_solo_track_excludes_accompaniment(self):
  with tempfile.TemporaryDirectory() as td:
   m=mido.MidiFile(ticks_per_beat=480)
   for name,pitches in [('Solo',[72]),('Accompaniment',[48,52,55])]:
    t=mido.MidiTrack();m.tracks.append(t);t.append(mido.MetaMessage('track_name',name=name))
    for pitch in pitches:t.append(mido.Message('note_on',note=pitch,velocity=64,time=0))
    for i,pitch in enumerate(pitches):t.append(mido.Message('note_off',note=pitch,velocity=0,time=480 if i==0 else 0))
   p=Path(td)/'two.mid';m.save(p)
   with self.assertRaises(ValueError):analyze(p)
   a,_=analyze(p,track_index=0);self.assertEqual(a['notes'],1);self.assertEqual(a['chord_onsets_pct'],0)
   b,_=analyze(p,track_index=1);self.assertEqual(b['notes'],3);self.assertEqual(b['chord_onsets_pct'],100)
 def test_musicxml_requires_part_and_analyzes_selected_violin(self):
  from music21 import stream,note,instrument
  with tempfile.TemporaryDirectory() as td:
   score=stream.Score()
   for name,pitches in [('Violin',[72,76]),('Piano',[48,52,55])]:
    part=stream.Part();part.partName=name;part.append(instrument.Violin() if name=='Violin' else instrument.Piano())
    for pitch in pitches:part.append(note.Note(pitch,quarterLength=1))
    score.insert(0,part)
   p=Path(td)/'two.musicxml';score.write('musicxml',fp=p)
   cmd=[sys.executable,str(ROOT/'src/score_file.py'),str(p)]
   bad=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(bad.returncode,2);self.assertIn('--part',bad.stderr)
   good=subprocess.run(cmd+['--part','0'],capture_output=True,text=True);self.assertEqual(good.returncode,0,good.stderr)
   result=json.loads(good.stdout);self.assertEqual(result['notes'],2);self.assertEqual(result['low_midi'],72);self.assertEqual(result['high_midi'],76)
 def test_corpus_integrity(self):
  import csv
  with (ROOT/'data/pieces.csv').open() as f:rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),25);self.assertEqual(len({r['Work ID'] for r in rows}),9)
  self.assertEqual(len({r['Composer'] for r in rows}),6)
  self.assertTrue(all('BWV1002' not in r['Work ID'] for r in rows))
  self.assertEqual(sum(int(r['Noteheads']) for r in rows),28108)
  for r in rows:self.assertEqual(r['Expert Grade'],'')
if __name__=='__main__':unittest.main()
