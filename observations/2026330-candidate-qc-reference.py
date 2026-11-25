#!/usr/bin/env python3
"""Compare model to 13,983,816 direct enumerations, rebuild roles/windows and exhaust identities."""
from pathlib import Path
from itertools import product
import csv,hashlib,json
R=Path('/home/user');O=R/'archive/task301_330_release/analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();a=J(O/'candidate_audit.json');m=J(O/'manual_decision.json');b=J(O/'brute_model.json');e=J(O/'evidence.json');st=J(O/'six_sign_repeat_study.json');checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');nm=lambda n:z[(7-n)%12];grp={x:[n for n in range(1,50) if nm(n)==x] for x in z};den=b['denominator'];v=a['selected']['ideal_model'];ck(den==v['denominator']==13983816 and b['chosen']['distribution']==v['exact_complete_column_distribution'] and b['old']==b['chosen'],'exhaustive direct counts for old and new both match all column distributions')
for k in ('single','pair','triple','pair_and_triple'):ck(b['chosen'][k]==v['counts'][k],f'exhaustive count {k}')
for k,c in enumerate(a['selected_conditional_on_repeat_0_to_5']):
 x=b['conditional'][k];ck(c['repeat_count']==k and c['denominator']==sum(x['distribution']) and c['all_columns']==x['distribution'][3] and c['no_complete_column']==x['distribution'][0] and all(c[y]==x[y] for y in ('single','pair','triple')),f'exhaustive conditional repeat {k}')
ck(m['choice']=='EE01' and m['top']=='馬' and m['pair']==['鷄','牛'] and m['triple']==['鷄','龍','虎'] and m['reserves']==['蛇'] and not m['target_330_result_queried_or_used'] and a['candidate_count']==len(a['candidates'])==12,'selected roles and no target used')
with (R/'archive/task301_330_release/stage/data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rr=list(csv.DictReader(f));rr.sort(key=lambda r:int(r['period']))
last=rr[-1];prev={last[f'z{i}'] for i in range(1,7)};prev7=prev|{last['special_zodiac']};ck(prev=={'鼠','牛','兔','鷄','狗'} and prev7-prev=={'豬'} and len(st['current_pending']['previous_six'])==5,'normal identity set and seventh distinction')
for x in a['candidates']:
 r=x['roles'];s={r['top']};p={r['A'],r['B']};t={r['A'],r['C'],r['D']};shown=s|p|t;u=shown|set(x['reserves']);nums=sorted(n for k in shown for n in grp[k]);unums=sorted(n for k in u for n in grp[k]);ck(len(u)==6 and nums==x['display_numbers'] and unums==x['universe_numbers'] and len(nums)==x['displayed_code_count'] and len(unums)==x['universe_code_count'],f"{x['id']} identities and code lists")
 for name,g in [('single',s),('pair',p),('triple',t),('all_columns',shown)]:
  mm=x['minimums'][name];ck(mm['distinct_zodiacs']==len(g) and mm['road_0_1_2']==[sum(grp[k][0]%3==j for k in g) for j in range(3)] and mm['odd_even']==[sum(grp[k][0]%2==j for k in g) for j in (1,0)] and set(mm['previous_329_normal_identities'])==g&prev and set(mm['new_relative_to_329_normal_identities'])==g-prev,f"{x['id']} {name} road/parity/repeat requirements")
 for w in (35,40,45):
  dist=[0]*4
  for q in rr[-w:]:
   got={q[f'z{i}'] for i in range(1,7)};dist[sum(g<=got for g in (s,p,t))]+=1
  ck(dist==x['fixed_history_windows'][str(w)]['complete_0_1_2_3'],f"{x['id']} post-hoc W{w} replay")
sel=a['selected'];r=sel['roles'];S={r['top']};P={r['A'],r['B']};T={r['A'],r['C'],r['D']}
for mask in range(1<<12):
 got={x for i,x in enumerate(z) if mask>>i&1};s=S<=got;p=P<=got;t=T<=got;null=not(s or p or t);form=('馬' not in got and ('鷄' not in got or ('牛' not in got and ('龍' not in got or '虎' not in got))));ck(null==form,f'identity Boolean full-space mask {mask:04x}')
 # The repeat constraints depend on having at most six distinct identities in six balls.
 # Boolean column logic above holds for every mask, but a seven-identity mask cannot
 # represent a six-ball outcome and must not be used to challenge these constraints.
 if len(got)<=6 and all((s,p,t)):ck(len(prev&got) in (2,3),f'six-ball identity full-column repeat constraint mask {mask:04x}')
 if len(got)<=6 and len(prev&got) in (0,5):ck(not t,f'six-ball identity triple impossible at repeat 0/5 mask {mask:04x}')
if len(st['current_pending']['previous_six'])==5:ck(st['groups']['previous_six_5_seven_6']['n']==344 and st['groups']['previous_six_6_seven_7']['n']==131,'5/6 vs 6/7 groups not interchanged')
ck(sel['minimums']['all_columns']['road_0_1_2']==[2,2,1] and sel['minimums']['all_columns']['odd_even']==[3,2] and sel['minimums']['pair']['odd_even']==[0,2] and sel['minimums']['triple']['road_0_1_2']==[1,1,1],'even, route and all-column necessary constraints')
ck(all(abs(v['counts'][k]/den*100-v['percent'][k])<1e-12 for k in v['counts']) and round(v['percent']['no_complete_column'],4)==38.5598 and round(v['percent']['all_columns'],4)==0.3295,'displayed model percentages correct to floating-point tolerance, conditional on assumptions')
w=a['no_2road_synthetic_witness'];got={nm(n) for n in w['numbers']};ck(len(set(w['numbers']))==6 and all(n%3!=2 for n in w['numbers']) and [nm(n) for n in w['numbers']]==w['zodiacs'] and S<=got and P<=got and not T<=got and 'fabricated' in w['scope'],'synthetic no-two-road non-target witness')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'model_enumerated_sets':den,'candidate_audit_sha256':H(O/'candidate_audit.json'),'brute_model_sha256':H(O/'brute_model.json'),'manual_decision_sha256':H(O/'manual_decision.json'),'scope':'Identity, arithmetic and structural audit. No claim about source, official status, blind selection, event timing, future probability or return.','target_330_result_queried_or_used':False};(O/'candidate_qc.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','checks_count','model_enumerated_sets','target_330_result_queried_or_used')},indent=2))
