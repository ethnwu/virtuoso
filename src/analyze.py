"""Extract features from a selected violin MIDI track.
Usage: python src/analyze.py (from the project directory). Requires mido.
The index measures encoded musical features, not validated performer difficulty.
"""
from pathlib import Path
from collections import defaultdict
import csv, json, math, statistics
import mido
ROOT=Path(__file__).resolve().parents[1]
WEIGHTS={'Density':.35,'Chords':.30,'Register':.20,'Leaps':.15}

def percentile(values,p):
    a=sorted(values); k=(len(a)-1)*p; lo=math.floor(k); hi=math.ceil(k)
    return a[lo]+(a[hi]-a[lo])*(k-lo)

def analyze(path, track_index=None):
    midi=mido.MidiFile(path)
    tracks=[]
    for original_index,track in enumerate(midi.tracks):
        if track_index is not None and original_index != track_index: continue
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
    if len(tracks)!=1:
        raise ValueError(f'Expected exactly one violin note-bearing track, found {len(tracks)} in {path.name}. Select the solo part with --track; never combine accompaniment.')
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

if __name__=='__main__':
    from build_corpus import main
    main()
