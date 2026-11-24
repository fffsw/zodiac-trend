#!/usr/bin/env python3
"""Independent polynomial and 13,983,816-combination enumeration QC of 329 design."""
from pathlib import Path
from collections import defaultdict,Counter
from math import comb
from itertools import product
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task299_329_release';O=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();aud=J(O/'candidate_audit.json');design=J(O/'handcrafted_candidates.json');m=J(O/'manual_decision.json');br=J(O/'brute_model.json');checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if n2z(n)==z] for z in Z};den=comb(49,6);prev=set(m['previous_328_six']);ck(aud['status']=='PASS' and design['choice']==m['choice']=='DD01' and len(aud['candidates'])==len(design['candidates'])==12 and not aud['target_329_result_queried_or_used'] and not m['target_329_result_queried_or_used'],'audit and 12 frozen choices; no target result used')
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda x:int(x['period']))
for a,b in zip(design['candidates'],aud['candidates']):
 r=a['roles'];ck(a['id']==b['id'] and r==b['roles'] and a['reserves']==b['reserves'],f"{a['id']} design unchanged");show=set(r.values());bits={z:1<<i for i,z in enumerate(sorted(show,key=Z.index))};dp={(0,0):1}
 for z in Z:
  nxt=defaultdict(int)
  for (balls,mask),ways in dp.items():
   for take in range(min(len(G[z]),6-balls)+1):nxt[(balls+take,mask|(bits.get(z,0) if take else 0))]+=ways*comb(len(G[z]),take)
  dp=nxt
 counts={k:0 for k in ('single','pair','triple','all_columns','no_complete_column','at_least_one_complete','at_least_two_complete','pair_and_triple')};dist=[0]*4
 for (balls,mask),ways in dp.items():
  if balls!=6:continue
  got={z for z,v in bits.items() if mask&v};s={r['top']}<=got;p={r['A'],r['B']}<=got;t={r['A'],r['C'],r['D']}<=got;v=sum((s,p,t));dist[v]+=ways;counts['single']+=ways*s;counts['pair']+=ways*p;counts['triple']+=ways*t;counts['all_columns']+=ways*(v==3);counts['no_complete_column']+=ways*(v==0);counts['at_least_one_complete']+=ways*(v>=1);counts['at_least_two_complete']+=ways*(v>=2);counts['pair_and_triple']+=ways*(p and t)
 ck(b['ideal_model']['counts']==counts and b['ideal_model']['exact_complete_column_distribution']==dist and sum(dist)==den and b['displayed_code_count']==sum(len(G[z]) for z in show) and b['universe_code_count']==sum(len(G[z]) for z in show|set(a['reserves'])) and all(abs(b['ideal_model']['percent'][k]-100*v/den)<1e-10 for k,v in counts.items()),f"{a['id']} exact model via group polynomial")
 for w in (35,40,45):
  obs=Counter()
  for row in rows[-w:]:
   got={row[f'z{i}'] for i in range(1,7)};obs[sum(x<=got for x in ({r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}))]+=1
  ck(b['fixed_history_windows'][str(w)]['complete_0_1_2_3']==[obs[i] for i in range(4)],f"{a['id']} retrospective fixed W{w}, not rolling forecast")
r=aud['selected']['roles'];ck(r=={'top':'馬','A':'虎','B':'鷄','C':'鼠','D':'羊'} and aud['selected']['reserves']==['蛇'] and aud['selected']['displayed_code_count']==21 and aud['selected']['universe_code_count']==25 and prev=={'鼠','虎','龍','羊','猴','狗'},'chosen DD01 five distinct display identities and one reserve')
ck(aud['candidates'][0]['ideal_model']==aud['candidates'][9]['ideal_model'] and aud['candidates'][0]['roles']==aud['candidates'][9]['roles'],'changing reserve only does not change columns')
ck(br['denominator']==den,'brute enumeration contains all C(49,6) outcomes')
for label,key in [('chosen','selected'),('old','previous_328_CC01_ideal_comparison')]:
 v=aud[key]['ideal_model'] if label=='chosen' else aud[key];b=br[label];ck(v['exact_complete_column_distribution']==b['distribution'] and all(v['counts'][k]==b[k] for k in ('single','pair','triple','pair_and_triple')),f'{label}: direct 13,983,816-set brute enumeration agrees')
for k,(x,b) in enumerate(zip(aud['selected_conditional_on_repeat_0_to_6'],br['conditional'])):
 ck(sum(b['distribution'])==x['denominator'] and b['distribution'][0]==x['no_complete_column'] and b['distribution'][3]==x['all_columns'] and all(b[n]==x[n] for n in ('single','pair','triple')) and (x['all_columns']>0)==(k in (3,4)) and (k>=3 or x['triple']==0),f'full-set enumeration repeat {k}: exact counts and impossibility')
ck(br['conditional'][6]['triple']==sum(br['conditional'][6]['distribution']) and br['conditional'][6]['distribution'][0]==0,'if all six previous normal identities reappear, triple necessarily complete; no claim this will happen')
new=aud['selected']['ideal_model']['percent'];old=aud['previous_328_CC01_ideal_comparison']['percent'];ck(round(new['no_complete_column'],4)==38.5598 and round(old['no_complete_column'],4)==40.9686 and round(new['all_columns'],4)==0.3295 and round(old['all_columns'],4)==1.6585 and new['no_complete_column']<old['no_complete_column'] and new['all_columns']<old['all_columns'],'modeled zero risk decreases while modeled all-complete share also decreases; no real-world prediction')
for h,t,j,mouse,sheep in product((False,True),repeat=5):ck((not(h or (t and j) or (t and mouse and sheep)))==((not h) and ((not t) or ((not j) and ((not mouse) or (not sheep))))),'zero-column Boolean identity')
ck(all(B in (C,D) for A,B,C,D in product(range(3),repeat=4) if A!=B and len({A,C,D})==3),'route-sharing impossibility across pair and triple')
with (O/'candidate_audit.csv').open(encoding='utf8',newline='') as f:cr=list(csv.DictReader(f))
ck(len(cr)==12 and all(x['id']==y['id'] and abs(float(y['ideal_none_pct'])-x['ideal_model']['percent']['no_complete_column'])<0.000001 for x,y in zip(aud['candidates'],cr)),'CSV agrees with all candidate model values')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'candidate_audit_sha256':H(O/'candidate_audit.json'),'manual_decision_sha256':H(O/'manual_decision.json'),'brute_result_sha256':H(O/'brute_model.json'),'scope':'Independent number enumeration and structural arithmetic only; uniform model is assumed, not authenticated and not a forecast, gain, official source or timing claim.','target_329_result_queried_or_used':False};(O/'candidate_audit_qc.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','checks_count':len(checks),'brute_combinations':br['denominator'],'candidate_count':12,'conditional':{'all_full_possible_repeat':[3,4],'all_full_not_possible_repeat':[0,1,2,5,6]}},ensure_ascii=False,indent=2))
