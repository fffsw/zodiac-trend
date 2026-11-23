#!/usr/bin/env python3
"""Independent integer-composition validation of chosen and comparison structures."""
from pathlib import Path
from itertools import product
from math import comb
import csv,hashlib,json
R=Path('/home/user');O=R/'archive/task292_327_release/analysis';S=R/'archive/task292_327_release/stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();audit=J(O/'candidate_audit.json');src=J(O/'handcrafted_candidates.json');m=J(O/'manual_decision.json');study=J(O/'six_sign_repeat_study.json');Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');G={z:[n for n in range(1,50) if Z[(7-n)%12]==z] for z in Z};D=comb(49,6);previous=set(m['previous_326_six']);checks=[]
def ck(x,s):
 if not x:raise AssertionError(s)
 checks.append(s)
ck(audit['selection_source'].startswith('manual_decision') and audit['target_327_result_read'] is False and len(audit['candidates'])==len(src['candidates'])==12 and audit['selected']['id']==m['choice']=='BB01','all structures frozen before audit; target values not read')
# Direct composition over displayed zodiac groups and remaining undivided numbers; no inclusion-exclusion.
def enumerate_events(roles):
 seen=list(dict.fromkeys(roles.values()));S={roles['top']};P={roles['A'],roles['B']};T={roles['A'],roles['C'],roles['D']};sizes=[len(G[z]) for z in seen];other=49-sum(sizes);counts=dict.fromkeys(['single','pair','triple','all_columns','no_complete_column','at_least_one_complete','pair_and_triple'],0)
 for ks in product(*(range(s+1) for s in sizes)):
  rem=6-sum(ks)
  if not 0<=rem<=other:continue
  n=comb(other,rem)
  for s,k in zip(sizes,ks):n*=comb(s,k)
  present={z for z,k in zip(seen,ks) if k};a,b,c=S<=present,P<=present,T<=present
  for key,on in [('single',a),('pair',b),('triple',c),('all_columns',a and b and c),('no_complete_column',not(a or b or c)),('at_least_one_complete',a or b or c),('pair_and_triple',b and c)]:counts[key]+=n*on
 return counts
for x,y in zip(src['candidates'],audit['candidates']):
 assert x['id']==y['id'] and x['roles']==y['roles'] and x['reserves']==y['reserves'] and y['ideal_model']['denominator']==D and enumerate_events(x['roles'])==y['ideal_model']['counts']
 assert set(y['displayed'])==set(x['roles'].values()) and len(set(y['universe']))==6 and set(y['universe'])==set(x['roles'].values())|set(x['reserves']) and len(y['display_numbers'])==len(set(y['display_numbers']))
 assert [sum(G[z][0]%3==i for z in {x['roles'][k] for k in ('A','C','D')}) for i in range(3)]==y['minimums']['triple']['road_0_1_2']
ck(True,'all 12 exact model event counts independently reproduced using direct integer compositions, with identity-union and road checks')
chosen=audit['selected'];base=audit['candidates'][1];assert chosen['roles']=={'top':'馬','A':'鷄','B':'龍','C':'虎','D':'牛'} and m['top']=='馬' and m['pair']==['鷄','龍'] and m['triple']==['鷄','虎','牛'] and chosen['reserves']==['蛇'] and chosen['displayed_code_count']==21 and chosen['universe_code_count']==25
p=chosen['ideal_model']['percent'];b=base['ideal_model']['percent'];assert round(p['no_complete_column'],4)==38.5598 and round(b['no_complete_column'],4)==54.5086 and round(p['all_columns'],4)==0.3295 and round(b['all_columns'],4)==1.3611 and round(p['triple'],4)==5.0989
ck(True,'BB01 vs same-combination BB02 tradeoff confirmed, not forecast or return')
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rr=sorted(csv.DictReader(f),key=lambda x:int(x['period']),reverse=True)
for w in (35,40,45):
 both=sum(not {'馬','鷄'}&{r[f'z{i}'] for i in range(1,7)} for r in rr[:w]);assert both==chosen['standalone_and_shared_both_absent_in_historical_windows'][str(w)]
ck([chosen['standalone_and_shared_both_absent_in_historical_windows'][str(w)] for w in (35,40,45)]==[6,8,8],'historical 35/40/45 horse and chicken jointly absent directly recounted; windows overlap')
# An independent recursive group enumerator: the 6 previous groups, 3 additional displayed
# groups, and an aggregated 12-number rest. No historical future or draw results are consumed.
others=set(chosen['displayed'])-previous;assert others=={'馬','龍','牛'} and len(previous)==6
keys=sorted(previous,key=Z.index)+sorted(others,key=Z.index);sizes=[len(G[z]) for z in keys];rest=49-sum(sizes);assert rest==12
counts=[{k:0 for k in ('denominator','single','pair','triple','all_columns','no_complete_column')} for _ in range(7)];S1={m['top']};P=set(m['pair']);T=set(m['triple'])
def rec(i,balls,ways,present,k):
 if i==len(keys):
  left=6-balls
  if left<0 or left>rest:return
  n=ways*comb(rest,left);a,b,c=S1<=present,P<=present,T<=present
  for key,on in [('denominator',True),('single',a),('pair',b),('triple',c),('all_columns',a and b and c),('no_complete_column',not(a or b or c))]:counts[k][key]+=n*on
  return
 z=keys[i]
 for take in range(min(sizes[i],6-balls)+1):rec(i+1,balls+take,ways*comb(sizes[i],take),present|({z} if take else set()),k+int(take>0 and z in previous))
rec(0,0,1,set(),0)
cond=audit['selected_conditional_on_repeat_0_to_6'];assert [x['denominator'] for x in counts]==study['uniform_49_independent_model']['6']['counts_0_to_6']
for a,b in zip(counts,cond):assert all(a[k]==b[k] for k in a)
assert all(counts[k]['all_columns']==0 for k in [0,1,4,5,6]) and counts[6]['no_complete_column']==counts[6]['denominator'] and counts[0]['pair']==counts[0]['triple']==counts[1]['triple']==0
ck(True,'repeat-conditioned events independently enumerated: full columns only possible for repeat 2 or 3, six repeats forces zero for this layout')
max_example=[x['number'] for x in study['witness_six_repeat_6_not_327']];zs={Z[(7-n)%12] for n in max_example};assert len(zs&previous)==6 and not S1<=zs and not P<=zs and not T<=zs
ck(True,'six-repeat counterexample valid and explicitly synthetic, not target result')
out={'status':'PASS','scope':'independent combinatorial and descriptive audit, not real mechanism, timing, official results, forecast or winnings','checks':checks,'selected_id':'BB01','candidate_audit_sha256':H(O/'candidate_audit.json'),'manual_decision_sha256':H(O/'manual_decision.json')};p=O/'candidate_audit_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
