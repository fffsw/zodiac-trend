#!/usr/bin/env python3
"""Independent raw-ledger recount and inclusion-exclusion verification of the four-sign study."""
from pathlib import Path
from collections import Counter
from itertools import combinations
from math import comb
import csv,hashlib,json,datetime
R=Path('/home/user');B=R/'archive/task288_325_review/before';U=R/'archive/task288_325_review/input/user-325.json';O=R/'archive/task289_326_release/analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=J(O/'four_sign_study.json');a=J(O/'four_sign_conjoint_exploratory.json');u=J(U);checks=[]
def ok(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
with (B/'445-source-through-311.csv').open(encoding='utf8',newline='') as f:src=list(csv.DictReader(f))
with (B/'history-through-324.csv').open(encoding='utf8',newline='') as f:hist=list(csv.DictReader(f))
records=[(int(r['period']),r['date'],r['zodiacs'].split(),r['usable']=='1') for r in src]
for r in reversed(hist):
 p=int(r['period'])
 if 2026312<=p<=2026324:records.append((p,r['date'],[r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']],True))
records.append((2026325,'',u['normal_zodiacs']+[u['seventh_zodiac']],True));ok(len(records)==2506 and records[-1][0]==2026325 and all(p<=2026325 for p,_,_,_ in records) and e['current_period_pending_326']['follow_numbers_read'] is False,'raw source ends at user 325; 326 excluded from known followups')
def adj(x,y):
 p,q=x[0],y[0];yp,yq=p//1000,q//1000
 if yp==yq:return q%1000-p%1000==1
 if yq==yp+1 and q%1000==1:
  try:return (datetime.date.fromisoformat(y[1])-datetime.date.fromisoformat(x[1])).days==1
  except ValueError:return False
 return False
V=[];invalid=[]
for i in range(len(records)-1):
 p,q=records[i:i+2]
 if not p[3] or not q[3] or not adj(p,q):invalid.append([p[0],q[0]]);continue
 P6=set(p[2][:6]);P7=set(p[2]);N6=set(q[2][:6]);N7=set(q[2]);incoming=len(set(records[i-1][2])&P7) if i and records[i-1][3] and adj(records[i-1],p) else None
 V.append({'p':p[0],'q':q[0],'P6':P6,'P7':P7,'N6':N6,'N7':N7,'six':len(P6&N6),'seven_six':len(P7&N6),'seven':len(P7&N7),'m6':sorted(Counter(p[2][:6]).values(),reverse=True),'m7':sorted(Counter(p[2]).values(),reverse=True),'incoming':incoming,'counter6':Counter(p[2][:6])})
ok(len(V)==e['valid_pairs']==2501 and invalid==e['invalid_or_nonadjacent_pairs'] and len(invalid)==4 and V[-1]['q']==2026325 and V[-1]['seven']==1,'valid adjacency, cross-year boundaries and invalid records independently checked')
C=lambda arr,k,limit: [sum(x[k]==n for x in arr) for n in range(limit+1)]
def check_group(name,arr):
 x=e['cohorts'][name]
 for label,selected,key,limit in [('normal4_next_normal',[v for v in arr if len(v['P6'])==4],'six',4),('seven4_next_normal',[v for v in arr if len(v['P7'])==4],'seven_six',4),('seven4_next_seven',[v for v in arr if len(v['P7'])==4],'seven',4),('any6_next6_baseline',arr,'six',6),('any7_next7_baseline',arr,'seven',7)]:
  z=x[label];assert z['n']==len(selected) and [z['counts'][str(i)] for i in range(limit+1)]==C(selected,key,limit),(name,label)
for k,arr in [('2024plus',[v for v in V if v['p']>=2024001]),('all_2020plus',V)]+[(str(y),[v for v in V if v['p']//1000==y]) for y in (2024,2025,2026)]:check_group(k,arr)
for w in (35,40,45):
 key=f'last_{w}_prior_trigger_periods';threshold=records[-w][0];check_group(key,[v for v in V if v['p']>=threshold]);assert e['cohorts'][key]['window']['pending_current_period_excluded_from_followup_denominator']
ok(True,'all three outcome scopes, 2024+, full historical and overlapping rolling-window distributions independently recounted')
for k,arr in [('2024plus',[v for v in V if v['p']>=2024001]),('all_2020plus',V)]+[(str(y),[v for v in V if v['p']//1000==y]) for y in (2024,2025,2026)]+[(f'last_{w}',[v for v in V if v['p']>=records[-w][0]]) for w in (35,40,45)]:
 g=[v for v in arr if len(v['P6'])==len(v['P7'])==4];x=a['groups'][k];assert x['next_normal_repeat']=={'n':len(g),'counts':C(g,'six',4)} and x['next_seven_repeat']=={'n':len(g),'counts':C(g,'seven',4)}
g=[v for v in V if v['p']>=2024001 and len(v['P6'])==len(v['P7'])==4 and v['m6']==[2,2,1,1] and v['m7']==[2,2,2,1]];assert a['groups']['2024plus_exact_325_both_multiplicities']['next_normal_repeat']=={'n':len(g),'counts':C(g,'six',4)} and a['groups']['2024plus_exact_325_both_multiplicities']['next_seven_repeat']=={'n':len(g),'counts':C(g,'seven',4)}
assert not [v for v in V if v['P6']=={'虎','龍','馬','鷄'}] and a['matching_exact_325_six_identity_set_all_2020plus_known_followups']==0
assert a['groups']['2024plus']['next_normal_repeat']=={'n':48,'counts':[5,18,17,8,0]} and a['groups']['2024plus']['next_seven_repeat']=={'n':48,'counts':[5,13,19,9,2]} and a['groups']['2024plus_exact_325_both_multiplicities']['next_normal_repeat']=={'n':31,'counts':[3,10,12,6,0]}
ok(True,'conjoint exact four-scope and exact-multiplicity exploratory analyses reproduced; exact prior four identities have no known followup')
sub=[v for v in V if v['p']>=2024001 and len(v['P6'])==4 and v['m6']==[2,2,1,1]]
for m in (1,2):
 ex=[(z,z in v['N6']) for v in sub for z,c in v['counter6'].items() if c==m];got=e['previous_normal_multiplicity_exposure_2024plus'][f'prior_{m}_normal_balls'];assert got['identity_exposures']==len(ex) and got['identities_also_in_next_normal']==sum(v for _,v in ex)
ok(True,'repeated-versus-single prior identities counted per exposure, not treated as independent draws')
# Independent inclusion-exclusion: fix exactly k of 4 labelled sign groups active.
sizes=[4,5,4,4];outside=32
for n in (6,7):
 exact=[]
 for k in range(5):
  total=0
  for ids in combinations(range(4),k):
   cap=outside+sum(sizes[i] for i in ids)
   for j in range(k+1):
    for absent in combinations(ids,j):total+=(-1)**j*comb(cap-sum(sizes[i] for i in absent),n)
  exact.append(total)
 v=e['ideal_independent_49_model'][str(n)];assert exact==v['exact_counts'] and sum(exact)==v['denominator']==comb(49,n) and all(abs(100*x/comb(49,n)-y)<1e-10 for x,y in zip(exact,v['percent']))
ok(True,'six- and seven-ball ideal models verified by independent inclusion-exclusion, not empirical forecasting')
with (O/'four_sign_pairs.csv').open(encoding='utf8',newline='') as f:csvrows=list(csv.DictReader(f))
want=[v for v in V if len(v['P6'])==4 or len(v['P7'])==4];assert len(csvrows)==len(want)
for x,y in zip(csvrows,want):
 assert (int(x['prev']),int(x['next']))==(y['p'],y['q']) and set(x['prev6'].split())==y['P6'] and set(x['prev7'].split())==y['P7'] and set(x['next6'].split())==y['N6'] and set(x['next7'].split())==y['N7'] and [int(x[k]) for k in ('six_six_count','seven_six_count','seven_seven_count')]==[y['six'],y['seven_six'],y['seven']]
ok(True,'all historical four-sign pair ledger rows reconcile to frozen raw records')
assert e['spec_sha256']==H(O/'four_sign_study_spec.json') and e['source_sha256']==H(B/'445-source-through-311.csv') and a['source_csv_sha256']==H(O/'four_sign_pairs.csv');ok(True,'prespecified marginals and explicitly exploratory conjoint analysis hash-linked to frozen source')
out={'status':'PASS','scope':'325 user-only four-sign repeat count study through 325, 326 unknown; descriptive sources not authenticated, no promised future count','checks':checks,'study_sha256':H(O/'four_sign_study.json'),'conjoint_sha256':H(O/'four_sign_conjoint_exploratory.json'),'pair_csv_sha256':H(O/'four_sign_pairs.csv')};p=O/'four_sign_independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
