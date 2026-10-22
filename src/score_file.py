"""Inspect and score a new MIDI or MusicXML violin part.
Examples:
  python src/score_file.py concerto.mid --list-parts
  python src/score_file.py concerto.mid --track 8 --output result.json
  python src/score_file.py concerto.musicxml --part 0 --output result.json
The output is an exploratory formula, not a trained difficulty prediction.
"""
import argparse,json,tempfile
from pathlib import Path
from analyze import analyze,WEIGHTS
import mido

def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('file',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--track',type=int,help='Zero-based MIDI track index')
    p.add_argument('--part',type=int,help='Zero-based MusicXML part index')
    p.add_argument('--list-parts',action='store_true',help='List MIDI tracks or MusicXML parts without scoring')
    a=p.parse_args()
    try:
        if a.file.suffix.lower() in {'.mid','.midi'}:
            if a.part is not None:p.error('Use --track for MIDI')
            if a.list_parts:
                m=mido.MidiFile(a.file)
                print(json.dumps([{'track':i,'name':' / '.join(x.name for x in t if x.type=='track_name'),'note_events':sum(x.type=='note_on' and x.velocity>0 for x in t)} for i,t in enumerate(m.tracks)],indent=2));return
            r,_=analyze(a.file,track_index=a.track)
        elif a.file.suffix.lower() in {'.musicxml','.xml','.mxl'}:
            if a.track is not None:p.error('Use --part for MusicXML')
            from music21 import converter,stream
            score=converter.parse(a.file);parts=list(score.parts) if hasattr(score,'parts') else [score]
            if a.list_parts:
                print(json.dumps([{'part':i,'name':s.partName or str(s.id),'notated_events':len(s.recurse().notes)} for i,s in enumerate(parts)],indent=2));return
            if a.part is None and len(parts)!=1:p.error(f'This score has {len(parts)} parts. Run --list-parts and select the solo violin using --part.')
            idx=0 if a.part is None else a.part
            if not 0<=idx<len(parts):p.error('Part index is outside the available parts')
            selected=stream.Score();selected.insert(0,parts[idx])
            # Export the selected symbolic part through the same MIDI feature engine.
            # This first implementation deliberately excludes score-specific bowing/fingering.
            with tempfile.TemporaryDirectory() as td:
                mid=Path(td)/'selected.mid';selected.write('midi',fp=mid);r,_=analyze(mid)
            r['file']=a.file.name;r['selected_part']=idx;r['part_name']=parts[idx].partName
            r['conversion_note']='MusicXML converted to MIDI for shared feature extraction; bowing, fingering and notation-only detail are not modeled.'
        else:p.error('Supported inputs: .mid, .midi, .musicxml, .xml, .mxl. PDF/image recognition is not implemented.')
        r['index_type']='Exploratory rules-based technical-demand index; not a trained predictor'
        r['model_version']='0.1';r['weights']=WEIGHTS
        out=json.dumps(r,indent=2)
        if a.output:a.output.write_text(out+'\n')
        print(out)
    except (ValueError,AssertionError,FileNotFoundError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
