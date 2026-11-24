#!/usr/bin/env python3
"""Independent inclusion-exclusion and set-level replay of the frozen deep review."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from math import comb
import csv,hashlib,json,subprocess
R=Path('/home/user');A=R/'archive/task297_328_deep_review';B=A/'before';O=A/'analysis';J=lambda p:json.loads(p.read_text(encoding='utf8'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();data=J(O/'deep_metrics.json');checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True);ck(data['status']=='PASS_DEEP_REVIEW_NOT_A_FORECAST' and not data['target_328_outcome_queried_or_used'] and H(A/'before.sha256')==data['input_freeze_sha256'],'23 frozen input files and no target result in analysis')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');den=comb(49,6);g=lambda off:{z:{n for n in range(1,50) if Z[(off-n)%12]==z} for z in Z};G=g(7);HYP=g(8);assert len(G['馬'])==5 and all(len(G[z])==4 for z in Z if z!='馬')
def ie(groups,plan):
 names=sorted(set().union(*plan));out=Counter()
 for mask in range(1<<len(names)):
  pres={z for i,z in enumerate(names) if mask&(1<<i)};available=49-sum(len(groups[z]) for z in names if z not in pres);ways=0
  pp=list(pres)
  for k in range(len(pp)+1):
   for excluded in combinations(pp,k):
    size=available-sum(len(groups[z]) for z in excluded)
    if size>=6:ways+=(-1)**k*comb(size,6)
  assert ways>=0
  out[''.join('1' if group<=pres else '0' for group in plan)]+=ways
 for i in range(8):out.setdefault(f'{i:03b}',0)
 assert sum(out.values())==den
 return dict(sorted(out.items()))
cc=[{'馬'},{'狗','鷄'},{'狗','馬','蛇'}];bb=[{'馬'},{'鷄','龍'},{'鷄','虎','牛'}];models=data['ideal_model'];assert ie(G,cc)==models['CC01']['patterns_single_pair_triple'] and ie(G,bb)==models['BB01']['patterns_single_pair_triple'] and ie(HYP,cc)==models['hypothetical_offset8_not_a_328_mapping_claim']['patterns_single_pair_triple']
for name in ('CC01','BB01','hypothetical_offset8_not_a_328_mapping_claim'):
 v=models[name];ct=[sum(w for pattern,w in v['patterns_single_pair_triple'].items() if pattern.count('1')==k) for k in range(4)];assert ct==v['complete_columns_0_to_3_counts'] and all(abs(100*c/den-p)<1e-11 for c,p in zip(ct,v['complete_columns_0_to_3_pct']))
ck(True,'all BB01/CC01 exact joint event counts and hypothetical 4-code variant independently reproduced with inclusion-exclusion')
x=models['CC01']['patterns_single_pair_triple'];assert x['001']==x['011']==0 and x['111']==231920 and x['000']==5728968 and all(x[k]>=0 for k in x);part=models['CC01_zero_column_disjoint_partition'];assert part['no_horse_and_no_dog_count']==comb(40,6) and part['no_horse_dog_present_no_chicken_count']==comb(40,6)-comb(36,6) and part['no_displayed_identity_count']==comb(32,6) and sum([part['no_horse_and_no_dog_count'],part['no_horse_dog_present_no_chicken_count']])==x['000'];ck(True,'triple implies single; zero-column disjoint partition and partial-hit risk verified')
# Completely independent per-identity presence enumeration, including repeat-conditioned counts.
prev={'鼠','虎','馬','羊','鷄','狗'};pos=defaultdict(set);conditional=[Counter() for _ in range(7)];feasible=0
for n in range(1,7):
 for chosen in combinations(Z,n):
  s=set(chosen);size=sum(len(G[z]) for z in s)
  if size<6:continue
  ways=0
  for j in range(n+1):
   for excluded in combinations(chosen,j):
    left=size-sum(len(G[z]) for z in excluded)
    if left>=6:ways+=(-1)**j*comb(left,6)
  assert ways>0;feasible+=1;k=len(s&prev);hit=[v<=s for v in cc];pos[k].add(sum(hit));r=conditional[k];r['denominator']+=ways;r['single']+=ways*hit[0];r['pair']+=ways*hit[1];r['triple']+=ways*hit[2];r['all_columns']+=ways*all(hit);r['no_complete_column']+=ways*(not any(hit))
assert feasible==data['feasible_identity_sets_enumerated'] and {str(k):sorted(v) for k,v in pos.items()}==data['logical_repeat_possibilities'] and sum(x['denominator'] for x in conditional)==den
for k,v in enumerate(data['conditional_model_by_repeat']):assert v['repeat']==k and all(v[a]==conditional[k][a] for a in ('denominator','single','pair','triple','all_columns','no_complete_column'))
assert pos[0]=={0} and pos[1]=={0,1} and pos[5]=={1,2,3} and pos[6]=={2};ck(True,'all feasible zodiac sets independently enumerate repeat 0→zero, repeat 5→at least one, repeat 6→exactly two')
for w in data['synthetic_witnesses_not_328']:
 ns=w['synthetic_not_328_numbers'];s={Z[(7-n)%12] for n in ns};assert len(ns)==len(set(ns))==6 and len(s&prev)==w['repeat_identities'] and [v<=s for v in cc]==w['completed_single_pair_triple'] and sum(w['completed_single_pair_triple'])==w['complete_columns']
ck(True,'every disclosed repeat-condition witness is a labeled synthetic six-number set, not a claimed outcome')
assert models['identical_ideal_distribution_role_permutations']==11*10*9==990 and next(x for x in models['equivalence_within_12'] if 'CC01' in x)==['CC01','CC05','CC06','CC07','CC08','CC09','CC10','CC12'] and len({len(G[z]) for z in Z if z!='馬'})==1
ck(True,'990 identical-role distributions follow from exchangeable 4-code groups; not evidence of predictive equivalence in real draws')
with (B/'history-through-user-327.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
zs=lambda r:[r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']];ns=lambda r:[int(r[f'n{i}']) for i in range(1,7)]+[int(r['special'])];offsets=[]
for r in rows:
 vals={(Z.index(z)+n)%12 for z,n in zip(zs(r),ns(r))};assert len(vals)==1 and len(set(ns(r)))==7;offsets.append(vals.pop())
trans=[(int(rows[i-1]['period']),int(rows[i]['period'])) for i in range(1,len(rows)) if offsets[i-1]!=offsets[i]];cohort=[i for i in range(1,len(rows)) if len(set(zs(rows[i-1])[:6]))==len(set(zs(rows[i-1])))==6];assert len(rows)==1058 and trans==[(2024040,2024041),(2025028,2025029),(2026047,2026048)] and len(cohort)==132 and all(offsets[i-1]==offsets[i] for i in cohort) and [int(r['period']) for r in rows if not r['date']]==list(range(2026313,2026328))
ck(True,'all stored records have internally consistent zodiac offsets; three transitions and no transition among 132 selected pairs; 15 dates absent')
recent=list(reversed(rows[-45:]));blocks=data['recent_45_retrospective']['blocks']
for lo,hi,b in zip((0,10,20,35,40),(9,19,34,39,44),blocks):
 sub=recent[lo:hi+1];s=lambda r:set(zs(r)[:6]);dist=lambda plan:[sum(sum(group<=s(r) for group in plan)==i for r in sub) for i in range(4)];assert b['n']==len(sub) and b['CC01_complete_columns_0_to_3']==dist(cc) and b['BB01_complete_columns_0_to_3']==dist(bb)
assert data['recent_45_retrospective']['CC01_distribution_0_to_3']==[16,19,6,4] and data['recent_45_retrospective']['BB01_distribution_0_to_3']==[14,29,2,0]
ck(True,'five nonoverlapping retrospective blocks and old/new 45-row distributions directly re-settled')
with (O/'repeat_structural.csv').open(encoding='utf8',newline='') as f:r=list(csv.DictReader(f))
with (O/'recent_45_comparison.csv').open(encoding='utf8',newline='') as f:b=list(csv.DictReader(f))
assert len(r)==7 and len(b)==5 and [x['possible_complete_columns'] for x in r]==['0','0/1','0/1/2','0/1/2/3','0/1/2/3','1/2/3','2'] and sum(int(x['n']) for x in b)==45
assert data['decision'].startswith('No new authenticated information') and models['hypothetical_offset8_not_a_328_mapping_claim']['group_sizes']=={'馬':4,'狗':4,'鷄':4,'蛇':4}
ck(True,'downloadable tables, mapping sensitivity and decision-to-hold are consistent; hypothesis is not asserted as the 328 mapping')
out={'status':'PASS_INDEPENDENT_DEEP_REVIEW','scope':'Internal source consistency, deterministic logic and exact assumed-fair combinatorics. Not official data, chronology, 328 results, prediction, profitability or real WeChat certification.','checks':checks,'deep_metrics_sha256':H(O/'deep_metrics.json'),'history_sha256':H(B/'history-through-user-327.csv'),'target_328_outcome_queried_or_used':False};p=O/'independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
