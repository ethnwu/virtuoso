"""Export the reviewed corpus to the static score-analysis app; no user data."""
from pathlib import Path
import csv,json,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
def read(n):
 with (ROOT/'data'/n).open() as f:return list(csv.DictReader(f))
def main():
 web=ROOT/'web';web.mkdir(exist_ok=True);out=web/'downloads';out.mkdir(exist_ok=True)
 features=read('features.csv');pieces=[]
 for r in read('pieces.csv'):
  comps={f['Feature']:float(f['Feature Score']) for f in features if f['Piece ID']==r['Piece ID']}
  pieces.append({'id':r['Piece ID'],'workId':r['Work ID'],'title':r['Piece'],'composer':r['Composer'],'work':r['Work'],'movement':int(r['Movement Order']),'index':float(r['Virtuoso Index']),'components':[comps[k] for k in ['Density','Chords','Register','Leaps']],'raw':{'noteEvents':int(r['Noteheads']),'onsets':int(r['Onsets']),'quarterBeats':float(r['Quarter Beats']),'density':float(r['Notes per Quarter']),'chords':float(r['Chord Onsets Pct']),'register':float(r['High Notes Pct']),'leaps':float(r['Mean Leap Semitones']),'low':int(r['Lowest MIDI']),'high':int(r['Highest MIDI'])},'source':r['Source URL'],'scopeNote':r['Scope Note']})
 works=[{'id':w['Work ID'],'title':w['Work'],'composer':w['Composer'],'coverage':w['Coverage'],'status':'analyzed'} for w in read('works.csv')]
 for k in json.loads((ROOT/'data/known_repertoire.json').read_text()):works.append({'id':k['Work ID'],'title':k['Work'],'composer':k['Composer'],'coverage':'Verified published placement; score analysis pending','status':'catalogue','source':k['Source URL'],'placement':{'scheme':k['Scheme'],'rating':k['Rating'],'scope':k['Scope'],'locator':k['Source Locator'],'conditions':k['Conditions']}})
 ratings=[{'id':r['Rating ID'],'workId':r['Work ID'],'pieceIds':r['Piece IDs'].split('|') if r['Piece IDs'] else [],'scope':r['Scope'],'scheme':r['Scheme'],'value':r['Rating Value'],'source':r['Source URL'],'locator':r['Source Locator'],'conditions':r['Performance Conditions'],'review':r['Training Status']} for r in read('ratings.csv')]
 passages=[{'pieceId':p['Piece ID'],'window':int(p['Window']),'start':float(p['Start Quarter Beat']),'end':float(p['End Quarter Beat']),'count':int(p['Note Events']),'low':int(p['Lowest MIDI']),'high':int(p['Highest MIDI'])} for p in read('passages.csv')]
 data={'version':'1.0','updated':'2026-10-22','pieces':pieces,'works':works,'ratings':ratings,'passages':passages,'validation':json.loads((ROOT/'data/validation.json').read_text()),'ratingValidation':json.loads((ROOT/'data/ratings_validation.json').read_text())}
 (web/'data.json').write_text(json.dumps(data,separators=(',',':'),ensure_ascii=False))
 for f in ['pieces.csv','features.csv','works.csv','ratings.csv','passages.csv','concerto_manifest.json','sources.json','known_repertoire.json','known_repertoire.csv']:shutil.copy(ROOT/'data'/f,out/f)
 shutil.copy(ROOT/'tableau/Virtuoso.twbx',out/'Virtuoso.twbx')
 for f in ['METHOD.md','RATINGS.md','SOURCES.md']:shutil.copy(ROOT/'docs'/f,out/f)
 # A public-domain real concerto part for the browser's Try a score interaction.
 source=ROOT/'data/downloads/beethoven2/beethoven2.mid'
 if source.exists():
  import mido
  original=mido.MidiFile(source);mid=mido.MidiFile(ticks_per_beat=original.ticks_per_beat)
  mid.tracks.extend([original.tracks[0].copy(),original.tracks[4].copy()]);mid.save(web/'sample-beethoven.mid')
 assert len(pieces)==25 and len(works)==18
 print('Web export:',len(works),'works;',len(pieces),'analyzed movements;',len(ratings),'published corpus records.')
if __name__=='__main__':main()
