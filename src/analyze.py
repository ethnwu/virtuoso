"""Rebuild Virtuoso's pilot dataset from the bundled, public-domain MIDI files.
Usage: python src/analyze.py (from the project directory). Requires mido.
The index measures encoded musical features, not validated performer difficulty.
"""
from pathlib import Path
from collections import defaultdict
import csv, json, math, statistics
import mido
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=180'
WEIGHTS={'Density':.35,'Chords':.30,'Register':.20,'Leaps':.15}

def percentile(values,p):
    a=sorted(values); k=(len(a)-1)*p; lo=math.floor(k); hi=math.ceil(k)
    return a[lo]+(a[hi]-a[lo])*(k-lo)

def analyze(path):
    midi=mido.MidiFile(path)
    tracks=[]
    for track in midi.tracks:
        tick=0; active=defaultdict(list); notes=[]; names=[]
        for msg in track:
            tick+=msg.time
            if msg.type=='track_name': names.append(msg.name)
            if getattr(msg,'channel',None)==9: continue
            if msg.type=='note_on' and msg.velocity>0:
                active[(msg.channel,msg.note)].append(tick)
            elif msg.type=='note_off' or (msg.type=='note_on' and msg.velocity==0):
                k=(msg.channel,msg.note)
                if active[k]:
                    start=active[k].pop(0)
                    if tick>start: notes.append((start/midi.ticks_per_beat,tick/midi.ticks_per_beat,msg.note))
        if notes: tracks.append((notes,' / '.join(names)))
    assert len(tracks)==1, f'Expected one violin track: {path.name}: {len(tracks)}'
    notes,track_name=tracks[0]
    notes.sort(); groups=defaultdict(list)
    for start,end,pitch in notes: groups[round(start,8)].append(pitch)
    first=min(n[0] for n in notes); last=max(n[1] for n in notes); span=last-first
    onsets=sorted(groups); tops=[max(groups[t]) for t in onsets]
    leaps=[abs(b-a) for a,b in zip(tops,tops[1:])]
    chord_rate=sum(len(p)>1 for p in groups.values())/len(groups)*100
    density=len(notes)/span
    high=sum(n[2]>=84 for n in notes)/len(notes)*100
    mean_leap=statistics.mean(leaps) if leaps else 0
    components={'Density':min(100,density/8*100),'Chords':min(100,chord_rate/60*100),
                'Register':min(100,high/50*100),'Leaps':min(100,mean_leap/12*100)}
    index=sum(components[k]*WEIGHTS[k] for k in WEIGHTS)
    return dict(file=path.name,track_name=track_name,notes=len(notes),onsets=len(onsets),
                quarter_beats=round(span,4),notes_per_quarter=round(density,4),
                chord_onsets_pct=round(chord_rate,4),high_notes_pct=round(high,4),
                mean_topline_leap=round(mean_leap,4),low_midi=min(n[2] for n in notes),
                high_midi=max(n[2] for n in notes),score=round(index,2),components=components),notes

def write_csv(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    metadata=json.loads((ROOT/'data/metadata.json').read_text())
    pieces=[]; features=[]; events=[]
    for item in metadata:
        a,notes=analyze(ROOT/'data/raw'/item['file'])
        base={'Piece ID':item['id'],'Piece':item['title'],'Composer':'J. S. Bach',
              'Work':'Partita No. 1 in B minor, BWV 1002','Movement Order':item['order']}
        pieces.append({**base,'Virtuoso Index':a['score'],'Noteheads':a['notes'],'Onsets':a['onsets'],
                       'Quarter Beats':a['quarter_beats'],'Notes per Quarter':a['notes_per_quarter'],
                       'Chord Onsets Pct':a['chord_onsets_pct'],'High Notes Pct':a['high_notes_pct'],
                       'Mean Leap Semitones':a['mean_topline_leap'],'Lowest MIDI':a['low_midi'],
                       'Highest MIDI':a['high_midi'],'Source URL':SOURCE,'License':'Public Domain',
                       'Model Version':'0.1 exploratory'})
        for k,v in a['components'].items():
            features.append({**base,'Feature':k,'Feature Score':round(v,4),
                             'Weight':WEIGHTS[k],'Weighted Contribution':round(v*WEIGHTS[k],4)})
        for i,(start,end,pitch) in enumerate(notes):
            events.append({'Piece ID':item['id'],'Piece':item['title'],'Event':i+1,
                           'Start Quarter Beat':round(start,6),'End Quarter Beat':round(end,6),'MIDI Pitch':pitch})
    pieces.sort(key=lambda r:-r['Virtuoso Index'])
    write_csv(ROOT/'data/pieces.csv',pieces); write_csv(ROOT/'data/features.csv',features)
    write_csv(ROOT/'data/note_events.csv',events)
    for row in pieces:
        fs=[r for r in features if r['Piece ID']==row['Piece ID']]
        assert abs(sum(r['Weighted Contribution'] for r in fs)-row['Virtuoso Index'])<.011
        assert 0<=row['Virtuoso Index']<=100
        assert row['Noteheads']>=row['Onsets']>0
        assert 0<=row['Chord Onsets Pct']<=100 and row['Lowest MIDI']<=row['Highest MIDI']
    assert len({r['Piece ID'] for r in pieces})==len(pieces)
    summary={'movements':len(pieces),'noteheads':len(events),'features':len(features),
             'checks':'Index recomputation, bounds, unique IDs, note/onset counts passed',
             'model_version':'0.1 exploratory','source':SOURCE}
    (ROOT/'data/validation.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
    for p in pieces: print(p['Piece'],p['Virtuoso Index'],p['Noteheads'])
if __name__=='__main__': main()
