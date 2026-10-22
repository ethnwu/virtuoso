"""Fetch checked source archives and rebuild the concerto-only Tableau datasets.
Run: python src/build_corpus.py. Raw downloads stay outside version control.
"""
from pathlib import Path
from collections import Counter
import json,csv,hashlib,io,zipfile,urllib.request,statistics
from analyze import analyze,write_csv,WEIGHTS
ROOT=Path(__file__).resolve().parents[1]
def source_bytes(source):
    p=ROOT/'data/downloads'/source['source_id']/'original.bin';p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists():p.write_bytes(urllib.request.urlopen(source['download_url'],timeout=60).read())
    b=p.read_bytes()
    if hashlib.sha256(b).hexdigest()!=source['sha256']: raise ValueError('Source hash changed: '+source['source_id']+'. Review the edition before updating the manifest.')
    return b

def main():
    sources={s['source_id']:s for s in json.loads((ROOT/'data/sources.json').read_text())}
    manifest=json.loads((ROOT/'data/concerto_manifest.json').read_text());blobs={}
    rows=[];features=[];events=[];audit=[]
    for entry in manifest:
        source=sources[entry['source_id']]
        if entry['source_id'] not in blobs:blobs[entry['source_id']]=source_bytes(source)
        b=blobs[entry['source_id']]
        if source['download_url'].endswith('.zip'): b=zipfile.ZipFile(io.BytesIO(b)).read(entry['archive_member'])
        path=ROOT/'data/downloads'/entry['source_id']/('selected-'+entry['id']+'.mid');path.write_bytes(b)
        a,notes=analyze(path,track_index=entry['track_index'])
        assert a['track_name']==entry['expected_track_name'],entry['id']
        assert a['notes']==entry['expected_note_ons'],(entry['id'],a['notes'],entry['expected_note_ons'])
        label=f"{entry['composer']} · {entry['work_id']} · {entry['movement']}. {entry['title']}"
        base={'Piece ID':entry['id'],'Piece':label,'Composer':entry['composer'],'Work ID':entry['work_id'],'Work':entry['work'],'Period':entry['period'],'Movement Order':entry['movement']}
        rows.append({**base,'Virtuoso Index':a['score'],'Noteheads':a['notes'],'Onsets':a['onsets'],'Quarter Beats':a['quarter_beats'],'Notes per Quarter':a['notes_per_quarter'],'Chord Onsets Pct':a['chord_onsets_pct'],'High Notes Pct':a['high_notes_pct'],'Mean Leap Semitones':a['mean_topline_leap'],'Lowest MIDI':a['low_midi'],'Highest MIDI':a['high_midi'],'Source URL':source['source_page'],'License':source['license'],'Attribution':source['attribution'],'Model Version':'0.1 exploratory','Scope Note':entry['scope_note'],'Expert Grade':''})
        for k,v in a['components'].items():features.append({**base,'Feature':k,'Feature Score':round(v,4),'Weight':WEIGHTS[k],'Weighted Contribution':round(v*WEIGHTS[k],4)})
        for i,(start,end,pitch) in enumerate(notes):events.append({'Piece ID':entry['id'],'Piece':label,'Event':i+1,'Start Quarter Beat':round(start,6),'End Quarter Beat':round(end,6),'MIDI Pitch':pitch})
        audit.append({'piece_id':entry['id'],'track_index':entry['track_index'],'track_name':a['track_name'],'note_events':a['notes'],'min_pitch':a['low_midi'],'max_pitch':a['high_midi'],'source_id':entry['source_id']})
    rows.sort(key=lambda x:(x['Composer'],x['Work ID'],x['Movement Order']))
    write_csv(ROOT/'data/pieces.csv',rows);write_csv(ROOT/'data/features.csv',features);write_csv(ROOT/'data/note_events.csv',events)
    # Passage-level features in 16-quarter-note windows; zero-note windows omitted.
    windows=[]
    for row in rows:
        ns=[e for e in events if e['Piece ID']==row['Piece ID']];groups={}
        for e in ns:groups.setdefault(int(e['Start Quarter Beat']//16),[]).append(e)
        for i,es in sorted(groups.items()):
            windows.append({'Piece ID':row['Piece ID'],'Piece':row['Piece'],'Composer':row['Composer'],'Work ID':row['Work ID'],'Window':i+1,'Start Quarter Beat':i*16,'End Quarter Beat':(i+1)*16,'Note Events':len(es),'Lowest MIDI':min(e['MIDI Pitch'] for e in es),'Highest MIDI':max(e['MIDI Pitch'] for e in es)})
    write_csv(ROOT/'data/passages.csv',windows)
    works=[]
    for wid in sorted({r['Work ID'] for r in rows}):
        rs=[r for r in rows if r['Work ID']==wid]
        works.append({'Work ID':wid,'Work':rs[0]['Work'],'Composer':rs[0]['Composer'],'Available Movements':len(rs),'Coverage':'Movement II only' if wid=='BWV1056R' else 'Three source movements','Note Events':sum(r['Noteheads'] for r in rs),'Maximum Movement Index':max(r['Virtuoso Index'] for r in rs)})
    write_csv(ROOT/'data/works.csv',works)
    for r in rows:
        assert r['Noteheads']>=r['Onsets']>0 and 0<=r['Virtuoso Index']<=100
        fs=[f for f in features if f['Piece ID']==r['Piece ID']]
        assert abs(sum(f['Weighted Contribution'] for f in fs)-r['Virtuoso Index'])<.011
    assert len({r['Piece ID'] for r in rows})==len(rows)
    assert sum(w['Note Events'] for w in windows)==len(events)
    assert all(r['Lowest MIDI']>=55 and r['Highest MIDI']<=108 for r in rows),'Unexpected violin register; inspect selected part'
    summary={'works':len(works),'movements':len(rows),'composers':len({r['Composer'] for r in rows}),'note_events':len(events),'passage_windows':len(windows),'expert_ratings_available':0,'model_status':'Rules-based index; no trained difficulty predictor','checks':['Unique movement IDs','Archive SHA-256 matches','Explicit solo-track names and note counts match source manifest','Violin pitch bounds','Score recomputation and range','Passage counts reconcile'],'solo_track_audit':audit,'coverage_by_composer':dict(Counter(r['Composer'] for r in rows))}
    (ROOT/'data/validation.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print(json.dumps({k:v for k,v in summary.items() if k!='solo_track_audit'},indent=2))
if __name__=='__main__':main()
