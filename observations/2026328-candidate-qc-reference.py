#!/usr/bin/env python3
"""Independent group-polynomial audit of 12 328 candidates and repeat-conditioned outcomes."""
from pathlib import Path
from collections import defaultdict
from math import comb
from itertools import product
import csv,hashlib,json
R=Path('/home/user');O=R/'archive/task295_328_release/analysis';S=R/'archive/task295_328_release/stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();audit=J(O/'candidate_audit.json');design=J(O/'handcrafted_candidates.json');sel=J(O/'manual_decision.json');checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if n2z(n)==z] for z in Z};prev=set(sel['previous_327_six']);den=comb(49,6)
assert audit['status']=='PASS' and design['choice']==sel['choice']=='CC01' and not audit['target_328_result_queried_or_used'] and not sel['target_328_result_queried_or_used'] and len(audit['candidates'])==len(design['candidates'])==12 and 'spot checks' in audit['selection_source']
for a,b in zip(design['candidates'],audit['candidates']):
 rr=a['roles'];assert a['id']==b['id'] and rr==b['roles'] and a['reserves']==b['reserves'];show=set(rr.values());bits={z:1<<i for i,z in enumerate(sorted(show,key=Z.index))};dp={(0,0):1}
 for z in Z:
  nxt=defaultdict(int)
  for (balls,mask),ways in dp.items():
   for take in range(min(len(G[z]),6-balls)+1):nxt[(balls+take,mask|(bits.get(z,0) if take else 0))]+=ways*comb(len(G[z]),take)
  dp=nxt
 counts={k:0 for k in ('single','pair','triple','all_columns','no_complete_column','at_least_one_complete','pair_and_triple')}
 for (balls,mask),ways in dp.items():
  if balls!=6:continue
  got={z for z,v in bits.items() if mask&v};s={rr['top']}<=got;p={rr['A'],rr['B']}<=got;t={rr['A'],rr['C'],rr['D']}<=got
  counts['single']+=ways*s;counts['pair']+=ways*p;counts['triple']+=ways*t;counts['all_columns']+=ways*(s and p and t);counts['no_complete_column']+=ways*(not(s or p or t));counts['at_least_one_complete']+=ways*(s or p or t);counts['pair_and_triple']+=ways*(p and t)
 assert b['ideal_model']['counts']==counts and b['ideal_model']['denominator']==den and b['displayed_code_count']==sum(len(G[z]) for z in show) and b['universe_code_count']==sum(len(G[z]) for z in show|set(a['reserves']))
 for k,v in counts.items():assert abs(b['ideal_model']['percent'][k]-100*v/den)<1e-10
ck(True,'all 12 candidate exact event counts independently reproduced by zodiac-group generating polynomial')
r=audit['selected']['roles'];assert r=={'top':'馬','A':'狗','B':'鷄','C':'馬','D':'蛇'} and audit['selected']['reserves']==['虎','牛'] and audit['selected']['displayed_code_count']==17 and audit['selected']['universe_code_count']==25
p=audit['selected']['ideal_model']['percent'];old=J(R/'archive/task294_327_review/before/327-candidates.json')['selected']['ideal_model']['percent'];assert round(p['single'],4)==49.5198 and round(p['pair'],4)==15.6616 and round(p['triple'],4)==6.1500 and round(p['all_columns'],4)==1.6585 and round(p['no_complete_column'],4)==40.9686 and round(old['all_columns'],4)==0.3295 and round(old['no_complete_column'],4)==38.5598
ck(True,'selected four-sign concentration increases modeled all-column share while increasing modeled zero-column share; no forecast claim')
# A separate count over selected four identities + aggregated previous/nonprevious groups.
selected=set(r.values());names=sorted(selected,key=Z.index);other_prev=[z for z in Z if z in prev-selected];other_new=[z for z in Z if z not in (prev|selected)];groups=[(len(G[z]),z in prev,z) for z in names]+[(sum(map(lambda z:len(G[z]),other_prev)),True,None),(sum(map(lambda z:len(G[z]),other_new)),False,None)];assert sum(g[0] for g in groups)==49
# Aggregating multiple previous zodiac signs would lose distinct-repeat counts. For conditional recount, keep them separate.
groups=[(len(G[z]),z in prev,z if z in selected else None) for z in Z];bits={z:1<<i for i,z in enumerate(names)};dp={(0,0,0):1}
for size,was,z in groups:
 nxt=defaultdict(int)
 for (balls,mask,k),ways in dp.items():
  for take in range(min(size,6-balls)+1):nxt[(balls+take,mask|(bits.get(z,0) if take else 0),k+int(was and take>0))]+=ways*comb(size,take)
 dp=nxt
for k,v in enumerate(audit['selected_conditional_on_repeat_0_to_6']):
 counts={x:0 for x in ('denominator','single','pair','triple','all_columns','no_complete_column')}
 for (balls,mask,rep),ways in dp.items():
  if balls!=6 or rep!=k:continue
  got={z for z,b in bits.items() if mask&b};ss={r['top']}<=got;pp={r['A'],r['B']}<=got;tt={r['A'],r['C'],r['D']}<=got;counts['denominator']+=ways;counts['single']+=ways*ss;counts['pair']+=ways*pp;counts['triple']+=ways*tt;counts['all_columns']+=ways*(ss and pp and tt);counts['no_complete_column']+=ways*(not(ss or pp or tt))
 assert all(v[x]==counts[x] for x in counts)
 assert (v['all_columns']>0)==(k in (3,4,5))
assert audit['selected_conditional_on_repeat_0_to_6'][6]['single']==audit['selected_conditional_on_repeat_0_to_6'][6]['pair']==audit['selected_conditional_on_repeat_0_to_6'][6]['denominator'] and audit['selected_conditional_on_repeat_0_to_6'][6]['triple']==0
ck(True,'repeat-conditioned exact counts and full-column impossibility outside repeat 3–5 independently checked')
with (S/'data/macau_mark_six_full.csv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f))
for w in (35,40,45):
 sets=[{row[f'z{i}'] for i in range(1,7)} for row in rows[:w]];zero=sum(not ({r['top']}<=x or {r['A'],r['B']}<=x or {r['A'],r['C'],r['D']}<=x) for x in sets);byformula=sum('馬' not in x and ('狗' not in x or '鷄' not in x) for x in sets);v=audit['selected_window_zero_column_risk'][str(w)];assert v['zero_complete_columns']==zero==byformula and v['horse_and_dog_both_absent']==sum(not {'馬','狗'}&x for x in sets) and v['horse_and_chicken_both_absent']==sum(not {'馬','鷄'}&x for x in sets)
assert [audit['selected_window_zero_column_risk'][str(w)]['zero_complete_columns'] for w in (35,40,45)]==[10,14,16]
ck(True,'joint zero-column condition and overlapping W35/W40/W45 descriptive counts independently checked')
assert all(b in (c,d) for a,b,c,d in product(range(3),repeat=4) if a!=b and len({a,c,d})==3);ck(True,'cross-column duplicated-road limitation proven for every route assignment satisfying pair/triple spread')
with (O/'candidate_audit.csv').open(encoding='utf8',newline='') as f:cr=list(csv.DictReader(f))
assert len(cr)==12 and all(x['id']==y['id'] and abs(float(y['ideal_none_pct'])-x['ideal_model']['percent']['no_complete_column'])<0.000001 for x,y in zip(audit['candidates'],cr));ck(True,'candidate table agrees with exact audit; reserve-only comparison leaves event probabilities unchanged')
out={'status':'PASS','scope':'independent integer combinatorics, historical description and structure only; not official source, date, winning, timing or predictive verification','checks':checks,'selected_id':'CC01','candidate_audit_sha256':H(O/'candidate_audit.json'),'manual_decision_sha256':H(O/'manual_decision.json'),'target_328_result_queried_or_used':False};pout=O/'candidate_audit_qc.json';assert not pout.exists();pout.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
