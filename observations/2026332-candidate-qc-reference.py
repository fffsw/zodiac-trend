#!/usr/bin/env python3
"""Independent 49-number DP audit of all 16 candidates and their historical settlements."""
from pathlib import Path
from collections import Counter,defaultdict
from math import comb
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task305_331_review_332';Q=A/'analysis';S=A/'stage';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads(p.read_text());d=J(Q/'candidate_design.json');a=J(Q/'candidate_audit.json');br=J(Q/'brute_model.json');checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];bit=lambda z:1<<Z.index(z);maskof=lambda ss:sum(bit(z) for z in set(ss));prev={rows[-1][f'z{i}'] for i in range(1,7)};pm=maskof(prev)
ck(len(rows)==1062 and max(int(r['period']) for r in rows)==2026331 and prev=={'龍','牛','猴','兔','蛇'} and not d['target_332_result_queried_or_used'],'no 332 outcome in confirmed 331 source')
# Independent DP acts on 49 individual numbers rather than the audit's grouped polynomial.
dp={(0,0):1}
for number in range(1,50):
 b=bit(sign(number));nxt=defaultdict(int,dp)
 for (k,m),v in dp.items():
  if k<6:nxt[(k+1,m|b)]+=v
 dp=nxt
ways={m:v for (k,m),v in dp.items() if k==6};ck(sum(ways.values())==comb(49,6)==13983816==br['denominator'],'49-individual-number dynamic program sums to full 49 choose 6')
ck(len(d['candidates'])==len(a['candidates'])==16 and d['choice']==a['choice']=='HH01' and a['input_sha256']['design']==H(Q/'candidate_design.json') and a['input_sha256']['history']==H(S/'data/macau_mark_six_full.csv'),'16 recorded related designs, selected before formal audit')
with (Q/'candidate_comparison.csv').open(encoding='utf8',newline='') as f:tab=list(csv.DictReader(f))
ck(len(tab)==16,'16-row candidate comparison CSV')
for src,x,t in zip(d['candidates'],a['candidates'],tab):
 ck(all(src[k]==x[k] for k in src) and src['id']==t['id'] and src['architecture']==t['architecture'],'candidate '+src['id']+' identities unchanged')
 single=maskof([src['single']]);pair=maskof(src['pair']);triple=maskof(src['triple']);c0=[0]*4;cc=[[0]*4 for _ in range(6)];cnt=Counter();sub=[Counter() for _ in range(6)]
 for m,v in ways.items():
  s=m&single==single;p=m&pair==pair;tr=m&triple==triple;k=(m&pm).bit_count();n=s+p+tr;c0[n]+=v;cc[k][n]+=v
  for k1,v1 in (('single',s),('pair',p),('triple',tr),('pair_and_triple',p and tr)):cnt[k1]+=v*v1;sub[k][k1]+=v*v1
 ideal=x['uniform_model'];ck(c0==ideal['distribution'] and sum(c0)==13983816 and all(cnt[k]==ideal[k] for k in cnt) and ideal['both_combinations_incomplete']==13983816-cnt['pair']-cnt['triple']+cnt['pair_and_triple'],src['id']+' unconditional model distribution')
 for k in range(6):
  cond=x['conditional_repeat'][k];ck(cond['repeat_count']==k and cond['denominator']==sum(cc[k]) and cond['distribution']==cc[k] and all(cond[n]==sub[k][n] for n in ('single','pair','triple','pair_and_triple')),f'{src["id"]} conditional repeat {k}')
 for w in (35,40,45,60,100,250):
  dist=[0]*4
  for r in rows[-w:]:
   present={r[f'z{k}'] for k in range(1,7)};n=(src['single'] in present)+int(set(src['pair'])<=present)+int(set(src['triple'])<=present);dist[n]+=1
  ck(dist==x['posthoc_fixed_windows'][str(w)]['complete_0_1_2_3'] and sum(dist)==w,src['id']+' fixed hindsight '+str(w))
 got={rows[-1][f'z{k}'] for k in range(1,7)};need=[[src['single']],src['pair'],src['triple']];sl=x['posthoc_331']['slots'];ck(x['posthoc_331']['complete_columns']==sum(set(v)<=got for v in need) and all(s['required']==v and s['present']==[z for z in v if z in got] and s['missing']==[z for z in v if z not in got] for s,v in zip(sl,need)),src['id']+' 331 post-result settlement')
 show={src['single']}|set(src['pair'])|set(src['triple']);univ=show|set(src['reserves']);common=set(src['pair'])&set(src['triple']);ck(len(univ)==6 and not show&set(src['reserves']) and set(x['previous_six_overlap'])==show&prev and set(x['shared_pair_triple'])==common,src['id']+' universe, previous overlap and exact common identities')
 if src['architecture']=='shared':ck(len(common)==1 and src['pair'][0]==src['triple'][0] and src['single'] not in set(src['pair'])|set(src['triple']) and len(show)==5 and len(src['reserves'])==1,src['id']+' shared-slot site format')
 else:ck(not common and src['id'] in ('T14','T15'),src['id']+' theoretical no pair/triple overlap, not deployed')
 for label,sg in [('pair',src['pair']),('triple',src['triple']),('all',list(show))]:
  nums=[next(n for n in range(1,50) if sign(n)==z) for z in set(sg)];expected={'road_0_1_2':[sum(n%3==i for n in nums) for i in range(3)],'odd_even':[sum(n%2==i for n in nums) for i in (1,0)]};ck(x[label+'_minimum']==expected,src['id']+' '+label+' road/parity necessary minima')
 ck(t['posthoc_331_complete_columns']==str(x['posthoc_331']['complete_columns']) and t['posthoc_last35_zero']==str(x['posthoc_fixed_windows']['35']['complete_0_1_2_3'][0]) and t['posthoc_last40_zero']==str(x['posthoc_fixed_windows']['40']['complete_0_1_2_3'][0]) and t['posthoc_last45_zero']==str(x['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0]) and t['zero_ideal_pct']==f"{100*c0[0]/13983816:.4f}" and t['all_ideal_pct']==f"{100*c0[3]/13983816:.4f}",src['id']+' CSV agrees')
 if src['id'] in br['cases']:
  v=br['cases'][src['id']];ck(v['overall']['distribution']==c0 and all(v['overall'][n]==cnt[n] for n in cnt) and all(v['conditional'][i]['distribution']==cc[i] for i in range(6)),src['id']+' separate direct enumerator')
sel=a['selected'];old=a['baseline'];ck(sel['id']=='HH01' and sel['single']=='馬' and sel['pair']==['虎','牛'] and sel['triple']==['虎','鷄','羊'] and sel['reserves']==['龍'] and sel['previous_six_overlap']==['牛'] and set(sel['previous_universe_overlap'])=={'牛','龍'} and set(sel['changed_formal_relative_to_331'])=={'虎','鷄','羊'} and set(sel['removed_formal_relative_to_331'])=={'狗','兔','蛇'},'actual chosen 332 format, one previous-six formal identity, three formal replacements')
ck(old['uniform_model']['distribution']==sel['uniform_model']['distribution']==[5392128,7401592,1144016,46080] and old['uniform_model']['both_combinations_incomplete']==sel['uniform_model']['both_combinations_incomplete'] and [x['repeat_count'] for x in sel['conditional_repeat'] if x['distribution'][3]]==[1,2] and [x['repeat_count'] for x in old['conditional_repeat'] if x['distribution'][3]]==[3,4],'selected and prior full unconditional distribution equal; different repeat-conditioned exposure')
ck(sel['posthoc_331']['complete_columns']==0 and [x['present_count'] for x in sel['posthoc_331']['slots']]==[0,1,0] and [sel['posthoc_fixed_windows'][str(w)]['complete_0_1_2_3'][0] for w in (35,40,45)]==[9,12,14] and [old['posthoc_fixed_windows'][str(w)]['complete_0_1_2_3'][0] for w in (35,40,45)]==[11,14,19],'actual 331 outcome would also fail new design; known overlapping historical windows compared without forward claims')
ck(next(x for x in a['candidates'] if x['id']=='HH11')['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0]==13 and sel['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0]==14,'HH11 has fewer historical zeroes than selected; audit retains unfavorable comparison')
ck(sel['pair_minimum']=={'road_0_1_2':[1,0,1],'odd_even':[1,1]} and sel['triple_minimum']=={'road_0_1_2':[1,1,1],'odd_even':[1,2]} and sel['all_minimum']=={'road_0_1_2':[2,2,1],'odd_even':[2,3]} and sel['conditional_repeat'][0]['pair']==0 and sel['conditional_repeat'][0]['single']>0 and sel['conditional_repeat'][0]['triple']>0,'road/parity necessary conditions and zero-repeat still allow single/triple')
t14=next(x for x in a['candidates'] if x['id']=='T14');t15=next(x for x in a['candidates'] if x['id']=='T15');ck(t14['uniform_model']['distribution']==[5280128,7584632,1113936,5120] and t15['uniform_model']['distribution']==[5728968,6580928,1627840,46080] and t15['single'] in t15['triple'] and not (set(t14['pair'])&set(t14['triple'])) and not (set(t15['pair'])&set(t15['triple'])),'non-shared hypothetical alternatives do not imply all objectives improve')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'audit_sha256':H(Q/'candidate_audit.json'),'design_sha256':H(Q/'candidate_design.json'),'brute_sha256':H(Q/'brute_model.json'),'target_332_result_queried_or_used':False,'scope':'Individual-number dynamic programming, direct enumeration and historical recount; no official source, timing or future accuracy guarantee.'};p=Q/'candidate_independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks_count':len(checks),'target_332_result_queried_or_used':False},ensure_ascii=False,indent=2))
