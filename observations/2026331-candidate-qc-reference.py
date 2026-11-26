#!/usr/bin/env python3
"""Independently audit 12 designs, full 49-choose-6 enumeration and feasible identity conditions."""
from pathlib import Path
from collections import Counter,defaultdict
from math import comb
import csv,hashlib,json
R=Path('/home/user');O=R/'archive/task303_331_release/analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();a=J(O/'candidate_audit.json');m=J(O/'manual_decision.json');b=J(O/'brute_model.json');st=J(O/'six_sign_repeat_study.json');design=J(O/'handcrafted_candidates.json');checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');nm=lambda n:z[(7-n)%12];grp={x:[n for n in range(1,50) if nm(n)==x] for x in z};den=b['denominator'];v=a['selected']['ideal_model'];ck(den==v['denominator']==13983816 and b['chosen']['distribution']==v['exact_complete_column_distribution'] and b['old']==b['chosen'],'direct enumeration of all sets: old and chosen distributions equal')
for k in ('single','pair','triple','pair_and_triple'):ck(b['chosen'][k]==v['counts'][k],f'exhaustive count {k}')
for k,c in enumerate(a['selected_conditional_on_repeat_0_to_5']):
 x=b['conditional'][k];ck(c['repeat_count']==k and c['denominator']==sum(x['distribution']) and c['all_columns']==x['distribution'][3] and c['no_complete_column']==x['distribution'][0] and all(c[y]==x[y] for y in ('single','pair','triple')),f'exhaustive conditional repeat {k}')
ck(m['choice']=='FF01' and m['top']=='馬' and m['pair']==['鷄','牛'] and m['triple']==['鷄','龍','蛇'] and m['reserves']==['虎'] and not m['target_331_result_queried_or_used'] and a['candidate_count']==len(a['candidates'])==12,'selected roles and no target used')
with (R/'archive/task303_331_release/stage/data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rr=list(csv.DictReader(f));rr.sort(key=lambda r:int(r['period']))
last=rr[-1];prev={last[f'z{i}'] for i in range(1,7)};prev7=prev|{last['special_zodiac']};ck(prev=={'馬','猴','豬','牛','鷄'} and prev7-prev=={'蛇'} and len(st['current_pending']['previous_six'])==5 and int(last['period'])==2026330,'previous normal identity set and separate seventh')
for source,x in zip(design['candidates'],a['candidates']):
 r=x['roles'];s={r['top']};p={r['A'],r['B']};t={r['A'],r['C'],r['D']};shown=s|p|t;u=shown|set(x['reserves']);nums=sorted(n for k in shown for n in grp[k]);unums=sorted(n for k in u for n in grp[k]);ck(source['id']==x['id'] and source['roles']==r and source['reserves']==x['reserves'] and len(u)==6 and nums==x['display_numbers'] and unums==x['universe_numbers'] and len(nums)==x['displayed_code_count'] and len(unums)==x['universe_code_count'],f"{x['id']} source, identities and number lists")
 # Independent probability generating function, not inclusion-exclusion.
 bits={k:1<<i for i,k in enumerate(z) if k in shown};dp={(0,0):1}
 for k in z:
  nxt=defaultdict(int)
  for (n,mask),ways in dp.items():
   for take in range(min(len(grp[k]),6-n)+1):nxt[(n+take,mask|(bits.get(k,0) if take else 0))]+=ways*comb(len(grp[k]),take)
  dp=nxt
 counts=Counter();dist=[0]*4
 for (n,mask),ways in dp.items():
  if n!=6:continue
  got={k for k,bit in bits.items() if mask&bit};cs=s<=got;cp=p<=got;ct=t<=got;vsum=cs+cp+ct;dist[vsum]+=ways;counts['single']+=ways*cs;counts['pair']+=ways*cp;counts['triple']+=ways*ct;counts['all_columns']+=ways*(vsum==3);counts['no_complete_column']+=ways*(vsum==0);counts['at_least_one_complete']+=ways*(vsum>0);counts['at_least_two_complete']+=ways*(vsum>=2);counts['pair_and_triple']+=ways*(cp and ct)
 ck(dict(counts)==x['ideal_model']['counts'] and dist==x['ideal_model']['exact_complete_column_distribution'] and sum(dist)==den,f"{x['id']} all ideal counts independently via group polynomial")
 for name,g in [('single',s),('pair',p),('triple',t),('all_columns',shown)]:
  mm=x['minimums'][name];ck(mm['distinct_zodiacs']==len(g) and mm['road_0_1_2']==[sum(grp[k][0]%3==j for k in g) for j in range(3)] and mm['odd_even']==[sum(grp[k][0]%2==j for k in g) for j in (1,0)] and set(mm['previous_330_normal_identities'])==g&prev and set(mm['new_relative_to_330_normal_identities'])==g-prev,f"{x['id']} {name} route/parity/overlap requirements")
 for w in (35,40,45):
  dist=[0]*4
  for q in rr[-w:]:
   got={q[f'z{i}'] for i in range(1,7)};dist[sum(g<=got for g in (s,p,t))]+=1
  ck(dist==x['fixed_history_windows'][str(w)]['complete_0_1_2_3'] and 'NOT historical prospective' in x['fixed_history_windows'][str(w)]['scope'],f"{x['id']} post-hoc W{w} replay")
sel=a['selected'];r=sel['roles'];S={r['top']};P={r['A'],r['B']};T={r['A'],r['C'],r['D']}
for mask in range(1<<12):
 got={x for i,x in enumerate(z) if mask>>i&1};s=S<=got;p=P<=got;t=T<=got;null=not(s or p or t);form=('馬' not in got and ('鷄' not in got or ('牛' not in got and ('龍' not in got or '蛇' not in got))));ck(null==form,f'identity Boolean full-space mask {mask:04x}')
 # Repeat conditions are restricted to at most six distinct identities, not arbitrary seven-sign masks.
 if len(got)<=6 and all((s,p,t)):ck(len(prev&got) in (3,4),f'feasible six-ball full-column repeat mask {mask:04x}')
 if len(got)<=6 and len(prev&got)==0:ck(null,f'feasible zero-repeat zero-column mask {mask:04x}')
 if len(got)<=6 and len(prev&got)==5:ck(s and p and not t,f'feasible five-repeat exactly-two-columns mask {mask:04x}')
ck(st['groups']['previous_six_5_seven_6']['n']==345 and st['groups']['previous_six_5_seven_5']['n']==227 and st['groups']['previous_six_6_seven_7']['n']==131,'5/6, 5/5 and 6/7 cohorts distinct')
ck(sel['minimums']['all_columns']['road_0_1_2']==[2,2,1] and sel['minimums']['all_columns']['odd_even']==[2,3] and sel['minimums']['pair']['odd_even']==[0,2] and sel['minimums']['triple']['road_0_1_2']==[1,1,1] and sel['minimums']['triple']['odd_even']==[1,2],'even, route and all-column necessary constraints')
ck(all(abs(v['counts'][k]/den*100-v['percent'][k])<1e-12 for k in v['counts']) and round(v['percent']['no_complete_column'],4)==38.5598 and round(v['percent']['all_columns'],4)==0.3295 and a['selected']['ideal_model']==a['previous_330_EE01_ideal_comparison'],'conditional uniform model percentages correct; same model as prior')
w=a['no_2road_synthetic_witness'];got={nm(n) for n in w['numbers']};ck(len(set(w['numbers']))==6 and all(n%3!=2 for n in w['numbers']) and [nm(n) for n in w['numbers']]==w['zodiacs'] and S<=got and P<=got and not T<=got and 'fabricated' in w['scope'],'synthetic no-two-road non-target witness')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'model_enumerated_sets':den,'candidate_audit_sha256':H(O/'candidate_audit.json'),'brute_model_sha256':H(O/'brute_model.json'),'manual_decision_sha256':H(O/'manual_decision.json'),'scope':'Identity, arithmetic and structural audit. No claim about source, official status, blind selection, event timing, future probability or return.','target_331_result_queried_or_used':False};p=O/'candidate_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','checks_count','model_enumerated_sets','target_331_result_queried_or_used')},indent=2))
