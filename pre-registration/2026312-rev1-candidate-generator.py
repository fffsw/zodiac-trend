#!/usr/bin/env python3
"""Audit explicit manual alternatives after repeat-history QA; never choose by score."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone,timedelta
import csv,hashlib,json,math,sys
sys.path.insert(0,'/home/user/scripts');import structure_audit_gate as gate
R=Path('/home/user');D=R/'data';OUT=D/'task242_312_revision_candidate_audit_v2.json';TXT=D/'task242_312_revision_candidate_audit_v2.txt'
assert not OUT.exists() and not TXT.exists()
Z={'鼠':[7,19,31,43],'牛':[6,18,30,42],'虎':[5,17,29,41],'兔':[4,16,28,40],
 '龍':[3,15,27,39],'蛇':[2,14,26,38],'馬':[1,13,25,37,49],'羊':[12,24,36,48],
 '猴':[11,23,35,47],'鷄':[10,22,34,46],'狗':[9,21,33,45],'豬':[8,20,32,44]};DEN=math.comb(49,6)
source=D/'task242_312_manual_candidate_design.json';design=json.loads(source.read_text());cands=design['candidates'];assert len(cands)==23
met=D/'task242_1000_repeat_metrics_v2.json';assert 'METRICS_SHA256='+hashlib.sha256(met.read_bytes()).hexdigest() in (D/'task242_1000_repeat_independent_test_v2.txt').read_text()
assert 'TASK242_1000_REPEAT_INDEPENDENT_V2 PASS' in (D/'task242_1000_repeat_independent_test_v2.txt').read_text()
orig=R/'archive/superseded_2026312_20261108_v1_before_reselection/prereg_2026312_original.json'
assert hashlib.sha256((D/'prereg_2026312.json').read_bytes()).hexdigest()==hashlib.sha256(orig.read_bytes()).hexdigest()
rows=sorted(csv.DictReader((D/'task242_1042_reconciled_history.csv').open(encoding='utf-8-sig')),key=lambda x:int(x['period']));assert int(rows[-1]['period'])==2026311
PREV=set(rows[-1][f'z{i}'] for i in range(1,7))|{rows[-1]['special_zodiac']}
assert PREV=={'鼠','兔','蛇','馬','鷄','豬'}

def exact(role,reserves):
 groups=list(dict.fromkeys([role[k] for k in ('top','A','B','C','D')]+list(reserves)))
 sizes=[len(Z[z]) for z in groups]+[49-sum(len(Z[z]) for z in groups)];idx={z:i for i,z in enumerate(groups)}
 marginal=[0]*3;counts=Counter();reserve_zero=0;total=0
 def go(i,left,weight,ks):
  nonlocal total,reserve_zero
  if i==len(sizes):
   if left:return
   hit=lambda z:ks[idx[z]]>0
   flags=(hit(role['top']),hit(role['A']) and hit(role['B']),hit(role['A']) and hit(role['C']) and hit(role['D']))
   total+=weight;counts[sum(flags)]+=weight
   for j,v in enumerate(flags):marginal[j]+=weight*int(v)
   if not any(flags) and any(hit(z) for z in reserves):reserve_zero+=weight
   return
  for k in range(min(sizes[i],left)+1):go(i+1,left-k,weight*math.comb(sizes[i],k),ks+[k])
 go(0,6,1,[]);assert total==DEN
 return {'denominator':DEN,'column_counts':marginal,'column_probabilities':[v/DEN for v in marginal],
  'completed_count_counts':[counts[i] for i in range(4)],'completed_count_probabilities':[counts[i]/DEN for i in range(4)],
  'reserve_hit_and_zero_complete_count':reserve_zero,'reserve_hit_and_zero_complete_probability':reserve_zero/DEN}
def cat(zs):
 need=[[0,0] for _ in range(3)]
 for z in zs:
  n=Z[z][0];need[n%3][0 if n%2 else 1]+=1
 sizes=[[8,8],[9,8],[8,8]];hit=0
 def rec(i,left,weight):
  nonlocal hit
  if i==6:
   if left==0:hit+=weight
   return
  r,j=divmod(i,2)
  for k in range(need[r][j],min(sizes[r][j],left)+1):rec(i+1,left-k,weight*math.comb(sizes[r][j],k))
 rec(0,6,1)
 return {'road_parity_odd_even_minima':need,'necessary_category_condition_count':hit,'necessary_category_condition_probability':hit/DEN}
def risk(k,total):
 a=math.comb(49-total,6);b=math.comb(49-k,6)
 return {'class_absent_probability':a/DEN,'class_present_but_no_displayed_member_probability':(b-a)/DEN,'no_displayed_member_probability':b/DEN}
out={}
for name,c in cands.items():
 U=c['U'];r={k:c[k] for k in ('top','A','B','C','D')};assert len(U)==len(set(U))==6 and set(r.values())<=set(U) and len({r[k] for k in 'ABCD'})==4
 display=list(dict.fromkeys(r.values()));reserve=[z for z in U if z not in display];u=gate.describe_pool(U,Z);d=gate.describe_pool(display,Z);cc=d['category_counts']
 out[name]={'roles':r,'universe':u,'display':d,'reserves':reserve,
  'universe_previous_identities':[z for z in U if z in PREV],
  'display_previous_identities':[z for z in display if z in PREV],
  'road_parity_display':[[sum(n%3==road and n%2==odd for n in d['numbers']) for odd in (1,0)] for road in range(3)],
  'road_risk':{str(i):risk(cc[f'road{i}'],(16,17,16)[i]) for i in range(3)},
  'A_absent_probability':math.comb(49-len(Z[r['A']]),6)/DEN,
  'category_conditions':{'top':cat([r['top']]),'two':cat([r['A'],r['B']]),'three':cat([r['A'],r['C'],r['D']])},
  'exact':exact(r,reserve)}
assert out['original_frozen']['roles']=={'top':'蛇','A':'兔','B':'龍','C':'虎','D':'馬'}
# These checks assert scenario differences, not a winner or an identity quota.
assert out['mouse_reserve_horse_B_dragon_D']['display']['numbers']==out['original_frozen']['display']['numbers']
assert out['mouse_reserve_horse_B_dragon_D']['universe_previous_identities']==['蛇','兔','馬','鼠']
assert out['mouse_reserve_horse_B_dragon_D']['reserves']==['鼠']
for z in ('牛','虎','兔','龍','蛇','馬','羊','猴','鷄','狗','豬','鼠'):assert any(z in c['U'] for c in cands.values())
res={'created_cst':datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'),'target':2026312,'cutoff':2026311,
 'manual_design_path':str(source.relative_to(R)),'manual_design_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'repeat_metrics_path':str(met.relative_to(R)),'repeat_metrics_sha256':hashlib.sha256(met.read_bytes()).hexdigest(),
 'selection_policy':'23 explicit human-written alternatives; no ranking, no RNG, no post-hoc replay. Prior identities in a candidate do not determine actual next draw repeats.',
 'candidates':out}
with OUT.open('x',encoding='utf-8') as f:json.dump(res,f,ensure_ascii=False,indent=2);f.write('\n')
lines=['TASK242 312 REVISION CANDIDATE AUDIT: hand-written, not scored/ranked; hypothetical uniform six-of-49 is not a prediction',
 'Previous identities from 311 seven: 鼠兔蛇馬鷄豬; 鷄 was 311 special identity only. In-candidate previous count != 312 observed repeat count.']
for name,v in out.items():
 c=v['display']['category_counts'];u=v['universe']['category_counts'];e=v['exact'];fmt=lambda q:f"012={q['road0']}/{q['road1']}/{q['road2']} parity={q['odd']}/{q['even']} small24/big25={q['small_1_24']}/{q['big_25_49']} red/blue/green={q['red']}/{q['blue']}/{q['green']}"
 lines+=['',name+' roles='+str(v['roles'])+' reserve='+str(v['reserves'])+' prev_U='+str(v['universe_previous_identities']),
  ' U '+fmt(u)+' head='+str(v['universe']['head_counts'])+' tail='+str(v['universe']['tail_counts']),
  ' display '+fmt(c)+' road-parity='+str(v['road_parity_display'])+' head='+str(v['display']['head_counts'])+' tail='+str(v['display']['tail_counts']),
  ' necessary-category='+str(v['category_conditions']),
  ' exact uniform column%='+str([round(100*x,4) for x in e['column_probabilities']])+' 0/1/2/3%='+str([round(100*x,4) for x in e['completed_count_probabilities']]),
  ' A-absent%='+str(round(v['A_absent_probability']*100,4))+' 0-road risk='+str(v['road_risk']['0'])]
lines+=['','All descriptions are opportunity-cost comparisons, not evidence of future advantage; odds unknown. TASK242_REVISION_CANDIDATE_AUDIT_V2 PASS']
with TXT.open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
print('\n'.join(lines))
