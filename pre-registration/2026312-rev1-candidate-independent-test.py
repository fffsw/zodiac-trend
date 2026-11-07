#!/usr/bin/env python3
"""Independently audit every revision candidate by inclusion-exclusion."""
from pathlib import Path
from collections import Counter
import itertools,hashlib,json,math,csv
R=Path('/home/user');D=R/'data';P=D/'task242_312_revision_candidate_audit_v2.json';o=json.loads(P.read_text());cands=o['candidates'];design=json.loads((D/'task242_312_manual_candidate_design.json').read_text())['candidates'];assert len(cands)==len(design)==23
assert o['manual_design_sha256']==hashlib.sha256((D/o['manual_design_path'].split('/')[-1]).read_bytes()).hexdigest()
Z={'鼠':(7,19,31,43),'牛':(6,18,30,42),'虎':(5,17,29,41),'兔':(4,16,28,40),
 '龍':(3,15,27,39),'蛇':(2,14,26,38),'馬':(1,13,25,37,49),'羊':(12,24,36,48),
 '猴':(11,23,35,47),'鷄':(10,22,34,46),'狗':(9,21,33,45),'豬':(8,20,32,44)}
assert set(itertools.chain.from_iterable(Z.values()))==set(range(1,50));den=math.comb(49,6)
def subsets(xs):
 for k in range(len(xs)+1):yield from itertools.combinations(xs,k)
def req(req,N=49):return sum((-1)**len(s)*math.comb(N-sum(len(Z[z]) for z in s),6) for s in subsets(sorted(req)))
categories=(8,8,9,8,8,8);bins=[]
for ks in itertools.product(range(7),repeat=6):
 if sum(ks)==6:bins.append((ks,math.prod(math.comb(n,k) for n,k in zip(categories,ks))))
assert sum(w for _,w in bins)==den
prev={'鼠','兔','蛇','馬','鷄','豬'}
for name,c in cands.items():
 r=c['roles'];U=design[name]['U'];assert r=={k:design[name][k] for k in ('top','A','B','C','D')}
 assert len(U)==len(set(U))==6 and all(v in U for v in r.values()) and len({r[k] for k in 'ABCD'})==4
 disp=set(r.values());reserve=set(U)-disp;assert reserve==set(c['reserves']);assert set(c['universe_previous_identities'])==set(U)&prev
 nums=sorted(n for z in U for n in Z[z]);dn=sorted(n for z in disp for n in Z[z]);assert nums==c['universe']['numbers'] and dn==c['display']['numbers']
 for section,ns in [('universe',nums),('display',dn)]:
  q=c[section]['category_counts'];assert [q[f'road{i}'] for i in range(3)]==[sum(n%3==i for n in ns) for i in range(3)]
  assert (q['odd'],q['even'])==(sum(n%2 for n in ns),sum(1-n%2 for n in ns))
  assert c[section]['head_counts']==[sum(n//10==h for n in ns) for h in range(5)]
  assert c[section]['tail_counts']==[sum(n%10==t for n in ns) for t in range(10)]
 assert c['road_parity_display']==[[sum(n%3==i and n%2==j for n in dn) for j in (1,0)] for i in range(3)]
 events=[{r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}];s=[req(a) for a in events]
 s1=sum(s);s2=sum(req(events[i]|events[j]) for i,j in itertools.combinations(range(3),2));s3=req(set.union(*events))
 counts=[den-s1+s2-s3,s1-2*s2+3*s3,s2-3*s3,s3];assert s==c['exact']['column_counts'] and counts==c['exact']['completed_count_counts']
 n0=0;N=49-sum(len(Z[z]) for z in reserve)
 for I in subsets(range(3)):n0+=(-1)**len(I)*req(set().union(*(events[i] for i in I)),N)
 assert counts[0]-n0==c['exact']['reserve_hit_and_zero_complete_count']
 for label,ev in zip(('top','two','three'),events):
  need=Counter((Z[z][0]%3,0 if Z[z][0]%2 else 1) for z in ev)
  expected=sum(w for ks,w in bins if all(ks[2*road+par]>=v for (road,par),v in need.items()))
  assert c['category_conditions'][label]['necessary_category_condition_count']==expected
 for i,n in enumerate((16,17,16)):
  k=sum(x%3==i for x in dn);risk=c['road_risk'][str(i)]
  assert abs(risk['class_absent_probability']-math.comb(49-n,6)/den)<1e-12
  assert abs(risk['no_displayed_member_probability']-math.comb(49-k,6)/den)<1e-12
  assert abs(risk['class_present_but_no_displayed_member_probability']-(math.comb(49-k,6)-math.comb(49-n,6))/den)<1e-12
 assert abs(c['A_absent_probability']-math.comb(49-len(Z[r['A']]),6)/den)<1e-12
rows=list(csv.DictReader((D/'task242_1042_reconciled_history.csv').open(encoding='utf-8-sig')));assert max(int(r['period']) for r in rows)==2026311
orig=R/'archive/superseded_2026312_20261108_v1_before_reselection/prereg_2026312_original.json';assert orig.read_bytes()==(D/'prereg_2026312.json').read_bytes()
print('23 human-entered candidates: six identities, all slots legal and earlier prereg unchanged PASS')
print('Independent inclusion-exclusion: each marginal, completed 0/1/2/3 and reserve/no-column integers PASS')
print('Independent 462 category compositions: necessary category, A absence, 0/1/2 road risk decomposition PASS')
print('Direct number expansion: U and display, parity, roads, heads, tails, prior identity set PASS')
print('No outcome replay, score or RNG; chosen prior identities are NOT actual future repeated identities.')
print('CANDIDATE_JSON_SHA256='+hashlib.sha256(P.read_bytes()).hexdigest())
print('TASK242_REVISION_CANDIDATE_INDEPENDENT_V2 PASS')
