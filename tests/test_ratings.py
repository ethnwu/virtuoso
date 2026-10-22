import unittest,sys,csv,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from build_ratings import movement_candidates

def read(name):
 with (ROOT/'data'/name).open() as f:return list(csv.DictReader(f))
class RatingScopeTests(unittest.TestCase):
 def test_scope_and_arrangement_exclusions(self):
  ratings=read('ratings.csv');pieces=read('pieces.csv');c=movement_candidates(ratings,pieces)
  self.assertEqual(len(c),9)
  self.assertFalse(any(r['Scheme'].startswith('Henle') for r in c))
  self.assertFalse(any(r['Piece ID'] in ['BWV1042-2','BWV1042-3','TWV51G8-1','RV310-1'] for r in c))
  rcm=[r for r in c if r['Scheme']=='RCM violin levels 2021']
  self.assertEqual(len(rcm),6);self.assertEqual(len({r['Work ID'] for r in rcm}),4)
 def test_no_cross_provider_grade_column(self):
  cs=movement_candidates(read('ratings.csv'),read('pieces.csv'))
  self.assertTrue(all('Scheme' in c and c['Review Status']=='edition comparison pending' for c in cs))
  self.assertTrue(all('Virtuoso Index' not in c for c in cs))
 def test_whole_work_cannot_create_movement_target(self):
  row=read('ratings.csv')[0]
  self.assertEqual(row['Scope'],'work')
  self.assertEqual(movement_candidates([row],read('pieces.csv')),[])
 def test_coverage_grain_is_preserved(self):
  rows=read('rating_coverage.csv')
  self.assertEqual(len(rows),25);self.assertEqual(len({r['Piece ID'] for r in rows}),25)
if __name__=='__main__':unittest.main()
