"""Validate scoped published ratings and create Tableau / candidate-target tables.
Never transfers a whole-work label to a movement, splits a combined selection,
or normalizes between providers. Candidate targets still need edition review.
"""
from pathlib import Path
import csv,json
from collections import Counter
def write_csv(path, rows):
 with path.open('w', newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
ROOT=Path(__file__).resolve().parents[1]
FEATURES=['Notes per Quarter','Chord Onsets Pct','High Notes Pct','Mean Leap Semitones','Lowest MIDI','Highest MIDI','Quarter Beats','Noteheads','Onsets']
def read(name):
 with (ROOT/'data'/name).open() as f:return list(csv.DictReader(f))
def movement_candidates(ratings,pieces):
 out=[];index={r['Piece ID']:r for r in pieces}
 for r in ratings:
  if r['Scope']!='movement' or not r['Numeric Rating'] or not r['Training Status'].startswith('candidate:'):continue
  p=index[r['Piece IDs']]
  out.append({'Rating ID':r['Rating ID'],'Piece ID':p['Piece ID'],'Work ID':p['Work ID'],'Composer':p['Composer'],'Scheme':r['Scheme'],'Target':int(r['Numeric Rating']),'Review Status':'edition comparison pending','Historical Syllabus':r['Historical Syllabus'],**{x:p[x] for x in FEATURES}})
 return out

def main():
 ratings=read('ratings.csv');pieces=read('pieces.csv');works=read('works.csv');sources={r['source_id']:r for r in json.loads((ROOT/'data/rating_sources.json').read_text())}
 pmap={r['Piece ID']:r for r in pieces};wmap={r['Work ID']:r for r in works}
 assert len({r['Rating ID'] for r in ratings})==len(ratings)
 for r in ratings:
  assert r['Work ID'] in wmap and r['Source ID'] in sources
  assert r['Source URL']==sources[r['Source ID']]['url'] and r['Source Verified']=='true'
  ids=r['Piece IDs'].split('|') if r['Piece IDs'] else []
  assert (r['Scope']=='work' and not ids) or (r['Scope']=='movement' and len(ids)==1) or (r['Scope']=='movement_group' and len(ids)>1)
  assert all(i in pmap and pmap[i]['Work ID']==r['Work ID'] for i in ids)
  if r['Numeric Rating']:
   n=int(r['Numeric Rating']);assert 1<=n<=(9 if r['Scheme'].startswith('Henle') else 10 if r['Scheme'].startswith('RCM') else 8)
  else:assert r['Rating Value'] in ['ATCL','FTCL','ARCT','LRCM']
 candidates=movement_candidates(ratings,pieces);write_csv(ROOT/'data/movement_rating_candidates.csv',candidates)
 tableau=[]
 for r in ratings:
  work=wmap[r['Work ID']]
  target=work['Work']+(' — whole work' if r['Scope']=='work' else ' — '+', '.join(r['Piece IDs'].split('|')))
  tableau.append({'Rating ID':r['Rating ID'],'Scheme':r['Scheme'],'Target':target,'Rating Label':str(r['Rating Value']),'Scope':r['Scope'],'Composer':work['Composer'],'Source URL':r['Source URL'],'Source Locator':r['Source Locator'],'Review Status':r['Training Status'],'Performance Conditions':r['Performance Conditions']})
 write_csv(ROOT/'data/ratings_tableau.csv',tableau)
 coverage=[]
 for p in pieces:
  direct=[r for r in ratings if r['Scope']=='movement' and r['Piece IDs']==p['Piece ID']]
  groups=[r for r in ratings if r['Scope']=='movement_group' and p['Piece ID'] in r['Piece IDs'].split('|')]
  whole=[r for r in ratings if r['Scope']=='work' and r['Work ID']==p['Work ID']]
  coverage.append({'Piece ID':p['Piece ID'],'Work ID':p['Work ID'],'Piece':p['Piece'],'Movement Placement IDs':'|'.join(r['Rating ID'] for r in direct),'Group Placement IDs':'|'.join(r['Rating ID'] for r in groups),'Work Context IDs':'|'.join(r['Rating ID'] for r in whole),'Status':'movement placement found' if direct else 'group context only' if groups else 'whole-work context only' if whole else 'no matched source found'})
 write_csv(ROOT/'data/rating_coverage.csv',coverage)
 summary={'source_verified_records':len(ratings),'provider_count':len({r['Provider'] for r in ratings}),'works_with_any_label':len({r['Work ID'] for r in ratings}),'work_scope_records':sum(r['Scope']=='work' for r in ratings),'movement_scope_records':sum(r['Scope']=='movement' for r in ratings),'group_scope_records':sum(r['Scope']=='movement_group' for r in ratings),'movements_with_specific_source_placements':sum(bool(c['Movement Placement IDs']) for c in coverage),'numeric_movement_candidate_rows':len(candidates),'schemes':{},'trained_model':False,'training_ready':False,'blockers':['Small number of independent concerto works per scheme','Source edition differences still need review','Arrangement and cadenza mismatches held out','No cross-provider conversion or label inheritance permitted']}
 for scheme in sorted({r['Scheme'] for r in candidates}):
  cs=[r for r in candidates if r['Scheme']==scheme];summary['schemes'][scheme]={'candidate_rows':len(cs),'independent_works':len({r['Work ID'] for r in cs}),'targets':sorted({r['Target'] for r in cs})}
 (ROOT/'data/ratings_validation.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
