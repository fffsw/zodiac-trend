#!/usr/bin/env python3
"""Independently enumerate per-category ball counts and falsifiable witnesses for post-hoc revision."""
from pathlib import Path
from itertools import product
from math import comb
from collections import Counter
import csv,json,hashlib
R=Path('/home/user');A=R/'archive/task290_326_revision';O=A/'analysis';B=A/'before';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();doc=J(O/'revision_design.json');audit=J(O/'revision_model.json');decision=J(O/'revision_decision.json');Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if n2z(n)==z] for z in Z};prev=set(doc['previous_325']);den=comb(49,6);checks=[]
def check(v,msg):
 if not v:raise AssertionError(msg)
 checks.append(msg)
check({z:len(x) for z,x in G.items()}==audit['sign_number_sizes'] and den==audit['model_denominator'] and prev=={'虎','馬','鷄','龍'},'2026 identity map, group cardinalities and fair six-ball denominator checked independently')
for plan,x in zip(doc['plans'],audit['plans']):
 assert plan['id']==x['id'] and plan['roles']==x['roles'];q=plan['roles'];signs=prev|set(q.values());signs=sorted(signs,key=Z.index);outside=49-sum(len(G[z]) for z in signs);c=[0]*4;cols=[0]*3;cr=[[0]*4 for _ in range(5)];th=[0]*5
 sets=[{q['top']},{q['A'],q['B']},{q['A'],q['C'],q['D']}]
 for vec in product(*(range(len(G[z])+1) for z in signs)):
  rem=6-sum(vec)
  if not 0<=rem<=outside:continue
  ways=comb(outside,rem)
  for z,k in zip(signs,vec):ways*=comb(len(G[z]),k)
  active={z for z,k in zip(signs,vec) if k};r=len(prev&active);flags=[s<=active for s in sets];n=sum(flags);c[n]+=ways;cr[r][n]+=ways;th[r]+=ways*flags[2]
  for i,v in enumerate(flags):cols[i]+=ways*v
 assert sum(c)==den and c==x['complete_columns_numerator_0_to_3'] and cols==x['single_pair_triple_numerators']
 for r in range(5):
  b=x['by_repeat_count'][str(r)];assert cr[r]==b['complete_columns_numerator_0_to_3'] and th[r]==b['three_complete_numerator'] and sum(cr[r])==b['model_hands']==audit['repeat_0_to_4_numerators'][r]
check(True,'all 11 fixed plans recounted by a different category-count enumeration, including repeat-conditioned columns')
# Independently derive the previous-four intersection distribution with inclusion-exclusion.
repeat=[];P=[len(G[z]) for z in sorted(prev,key=Z.index)]
for k in range(5):
 from itertools import combinations
 v=0
 for selected in combinations(range(4),k):
  for sub in range(1<<k):
   total=49-sum(P)+sum(P[i] for j,i in enumerate(selected) if not sub>>j&1);v+=(-1)**sub.bit_count()*comb(total,6)
 repeat.append(v)
check(repeat==audit['repeat_0_to_4_numerators']==[906192,4543392,5936976,2365336,231920],'previous-four intersection distribution checked by direct inclusion-exclusion')
by={x['id']:x for x in audit['plans']};old,new=by['R00'],by['R01'];assert old['percent']==new['percent'] and new['by_repeat_count']['4']['three_complete_numerator']==repeat[4] and new['by_repeat_count']['4']['complete_columns_numerator_0_to_3'][3]==46080 and old['by_repeat_count']['4']['three_complete_numerator']==46080
assert all(new['by_repeat_count'][str(i)]['three_complete_numerator']==0 for i in range(3));delta=audit['old_new_triple_disagreement'];assert delta['v2_complete_v1_incomplete_by_repeat_0_to_4']==[0,0,0,442240,185840] and delta['v1_complete_v2_incomplete_by_repeat_0_to_4']==[0,0,442240,185840,0]
# Direct weights for disagreement: require tiger/horse and only one of chicken/rabbit.
for r in range(5):
 vals=[]
 for gain in (True,False):
  sig=['虎','馬','鷄','龍','兔'];extra=49-sum(len(G[z]) for z in sig);ans=0
  for vec in product(*(range(len(G[z])+1) for z in sig)):
   remain=6-sum(vec)
   if not 0<=remain<=extra:continue
   a={z for z,k in zip(sig,vec) if k};g={'虎','馬','鷄'}<=a and '兔' not in a;l={'虎','馬','兔'}<=a and '鷄' not in a
   if len(a&prev)!=r or not (g if gain else l):continue
   ways=comb(extra,remain)
   for z,k in zip(sig,vec):ways*=comb(len(G[z]),k)
   ans+=ways
  vals.append(ans)
 assert vals==[delta['v2_complete_v1_incomplete_by_repeat_0_to_4'][r],delta['v1_complete_v2_incomplete_by_repeat_0_to_4'][r]]
check(True,'AA01 versus AA16: equal unconditional baseline, but all conditional gained/lost situations recounted separately')
oldslots=[{'羊'},{'虎','羊'},{'虎','馬','兔'}];newslots=[{'羊'},{'虎','羊'},{'虎','馬','鷄'}]
def state(nums,slots):
 s={n2z(n) for n in nums};return [int(x<=s) for x in slots],len(s&prev)
witnesses=[([5,13,4,6,7,2],2,[0,0,1],[0,0,0]),([5,13,4,12,6,2],2,[1,1,1],[1,1,0]),([5,13,10,6,7,2],3,[0,0,0],[0,0,1]),([5,13,27,4,6,2],3,[0,0,1],[0,0,0]),([5,13,10,27,6,2],4,[0,0,0],[0,0,1]),([5,13,10,27,12,6],4,[1,1,0],[1,1,1])]
for nums,r,a,b in witnesses:assert len(set(nums))==6 and state(nums,oldslots)==(a,r) and state(nums,newslots)==(b,r)
nums=[5,13,27,6,2,7];special=10;assert len(set(nums+[special]))==7 and state(nums,newslots)==([0,0,0],3) and len(({n2z(n) for n in nums}|{n2z(special)})&prev)==4
check(True,'synthetic examples confirm advantages and disadvantages, and seven-ball repeat-four does not imply first-six triple completion')
with (B/'history-through-325.csv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f))
for i,w in enumerate((35,40,45)):
 ns=[[int(x[f'n{j}']) for j in range(1,7)] for x in rows[:w]]
 assert sum(not {'羊','虎'}&{n2z(n) for n in row} for row in ns)==[16,16,18][i] and sum(sum(n%3==1 for n in row)<=1 for row in ns)==[5,8,9][i]
check(True,'recent-window shared-absence and <=1 1-road risk counts checked from frozen raw first-six numbers')
a=J(B/'326-v1-candidate-audit.json');aa=next(x for x in a['candidates'] if x['id']=='AA16');assert aa['roles']==new['roles'] and aa['reserves']==new['reserve_only']==['龍','蛇'] and decision['selected_id']=='R01' and decision['source_in_earlier_38']=='AA16' and decision['triple']==['虎','馬','鷄'] and decision['selection_is_not_an_actual_repeat_count'] and not decision['target_result_read']
check(True,'revised selection exactly equals pre-existing alternative AA16; decision is explicitly not an actual repeat count')
out={'status':'PASS','scope':'independent identity/category mathematics and synthetic witnesses, not actual result or forecast','checks':checks,'model_sha256':H(O/'revision_model.json'),'design_sha256':H(O/'revision_design.json'),'decision_sha256':H(O/'revision_decision.json')};p=O/'revision_model_independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
