#!/usr/bin/env python3
"""Audit 332 related structures by exact weighted sign masks and fixed post-hoc windows."""
from pathlib import Path
from collections import Counter
from math import comb
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task305_331_review_332';Q=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=J(Q/'candidate_design.json');br=J(Q/'brute_model.json');assert d['choice']=='HH01' and len(d['candidates'])==16 and not d['target_332_result_queried_or_used'] and br['denominator']==comb(49,6)==13983816 and not (Q/'candidate_audit.json').exists()
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
assert len(rows)==1062 and int(rows[-1]['period'])==2026331
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if sign(n)==z] for z in Z};prev={'龍','牛','猴','兔','蛇'};pb=sum(1<<Z.index(z) for z in prev);bit=lambda z:1<<Z.index(z);maskof=lambda ss:sum(bit(z) for z in set(ss));order=lambda ss:[z for z in Z if z in ss];ways={}
for mask in range(1<<12):
 if mask.bit_count()>6:continue
 poly=[1,0,0,0,0,0,0]
 for i,z in enumerate(Z):
  if not (mask>>i)&1:continue
  nxt=[0]*7
  for n in range(7):
   for k in range(1,min(len(G[z]),6-n)+1):nxt[n+k]+=poly[n]*comb(len(G[z]),k)
  poly=nxt
 if poly[6]:ways[mask]=poly[6]
assert sum(ways.values())==comb(49,6) and len(ways)>1000

def minima(zs):
 vals=[G[z][0] for z in set(zs)];return {'road_0_1_2':[sum(n%3==k for n in vals) for k in range(3)],'odd_even':[sum(n%2==k for n in vals) for k in (1,0)]}
def settle(x,row):
 got={row[f'z{i}'] for i in range(1,7)};slots=[]
 for label,need in (('single',[x['single']]),('pair',x['pair']),('triple',x['triple'])):
  have=[z for z in need if z in got];missing=[z for z in need if z not in got];slots.append({'name':label,'required':need,'present':have,'missing':missing,'present_count':len(have),'needed_count':len(need),'complete':not missing})
 return {'slots':slots,'complete_columns':sum(v['complete'] for v in slots)}
results=[]
for x in d['candidates']:
 shown={x['single']}|set(x['pair'])|set(x['triple']);assert order(shown&prev)==x['previous_six_overlap'];ss=bit(x['single']);pp=maskof(x['pair']);tt=maskof(x['triple']);total=[0]*4;cond=[[0]*4 for k in range(6)];cn=Counter();condn=[Counter() for k in range(6)]
 for mask,w in ways.items():
  s=mask&ss==ss;p=mask&pp==pp;t=mask&tt==tt;k=(mask&pb).bit_count();n=s+p+t;total[n]+=w;cond[k][n]+=w
  for label,v in (('single',s),('pair',p),('triple',t),('pair_and_triple',p and t)):
   cn[label]+=w*v;condn[k][label]+=w*v
 ideal={'distribution':total,**dict(cn),'both_combinations_incomplete':comb(49,6)-cn['pair']-cn['triple']+cn['pair_and_triple'],'denominator':comb(49,6),'distribution_percent':[100*v/comb(49,6) for v in total]};conditional=[]
 for k in range(6):
  den=sum(cond[k]);conditional.append({'repeat_count':k,'denominator':den,'distribution':cond[k],**dict(condn[k]),'zero_percent':100*cond[k][0]/den if den else None,'all_percent':100*cond[k][3]/den if den else None})
 hist={}
 for w in (35,40,45,60,100,250):
  vals=[settle(x,r)['complete_columns'] for r in rows[-w:]];hist[str(w)]={'first_period':int(rows[-w]['period']),'last_period':2026331,'complete_0_1_2_3':[vals.count(k) for k in range(4)]}
 common=set(x['pair'])&set(x['triple']);info={z:{'numbers':G[z],'road':G[z][0]%3,'odd_even':'odd' if G[z][0]%2 else 'even','from_previous_six':z in prev} for z in order(shown)}
 result={**x,'shared_pair_triple':order(common),'formal_distinct':order(shown),'formal_code_count':sum(len(G[z]) for z in shown),'universe_code_count':sum(len(G[z]) for z in shown|set(x['reserves'])),'single_minimum':minima([x['single']]),'pair_minimum':minima(x['pair']),'triple_minimum':minima(x['triple']),'all_minimum':minima(shown),'per_sign':info,'uniform_model':ideal,'conditional_repeat':conditional,'posthoc_331':settle(x,rows[-1]),'posthoc_fixed_windows':hist};results.append(result)
 if x['id'] in br['cases']:
  o=br['cases'][x['id']]['overall'];assert all(o[k]==ideal[k] for k in ('distribution','single','pair','triple','pair_and_triple'))
  for i,c in enumerate(br['cases'][x['id']]['conditional']):assert all(c[k]==conditional[i][k] for k in ('distribution','single','pair','triple','pair_and_triple'))
lookup={x['id']:x for x in results};old,new=lookup['HH00'],lookup['HH01'];assert old['uniform_model']['distribution']==new['uniform_model']['distribution']==[5392128,7401592,1144016,46080] and [c['distribution'][3]>0 for c in old['conditional_repeat']]==[False,False,False,True,True,False] and [c['distribution'][3]>0 for c in new['conditional_repeat']]==[False,True,True,False,False,False] and new['pair_minimum']=={'road_0_1_2':[1,0,1],'odd_even':[1,1]} and new['triple_minimum']=={'road_0_1_2':[1,1,1],'odd_even':[1,2]} and new['all_minimum']=={'road_0_1_2':[2,2,1],'odd_even':[2,3]} and new['posthoc_331']['complete_columns']==0
assert new['conditional_repeat'][0]['pair']==0 and new['conditional_repeat'][0]['single']>0 and new['conditional_repeat'][0]['triple']>0 and len(lookup['T14']['formal_distinct'])==6 and not lookup['T14']['shared_pair_triple'] and not lookup['T15']['shared_pair_triple'] and lookup['T15']['single'] in lookup['T15']['triple'] and lookup['T14']['uniform_model']['distribution'][3]==5120 and lookup['T15']['uniform_model']['distribution'][3]==46080
out={'status':'PASS_EXACT_MODEL_AND_POSTHOC_NOT_A_FORECAST','choice':'HH01','target_332_result_queried_or_used':False,'history_scope':'All fixed windows end at user-confirmed 331 and were available before selection; windows overlap and are retrospective, not a blind performance test.','model_scope':'49 equiprobable numbers without replacement, six normals, current mapping held fixed. Group-mask counts compared against direct enumeration of all 13,983,816 sets for HH00, HH01, HH08, T14, T15. This is conditional mathematics, not proof of actual odds or forecast advantage.','user_331_normal':order(prev),'candidates':results,'selected':new,'baseline':old,'input_sha256':{'design':H(Q/'candidate_design.json'),'history':H(S/'data/macau_mark_six_full.csv'),'brute':H(Q/'brute_model.json')}};(Q/'candidate_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
with (Q/'candidate_comparison.csv').open('x',encoding='utf8',newline='') as f:
 cols=['id','architecture','single','pair','triple','reserve','previous_six_overlap','formal_changes_vs_331','zero_ideal_pct','all_ideal_pct','both_combinations_incomplete_ideal_pct','possible_all_repeat_counts','posthoc_331_complete_columns','posthoc_last35_zero','posthoc_last40_zero','posthoc_last45_zero','scope'];w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
 for x in results:
  v=x['uniform_model'];w.writerow({'id':x['id'],'architecture':x['architecture'],'single':x['single'],'pair':' '.join(x['pair']),'triple':' '.join(x['triple']),'reserve':' '.join(x['reserves']),'previous_six_overlap':' '.join(x['previous_six_overlap']),'formal_changes_vs_331':' '.join(x['changed_formal_relative_to_331']),'zero_ideal_pct':f"{v['distribution_percent'][0]:.4f}",'all_ideal_pct':f"{v['distribution_percent'][3]:.4f}",'both_combinations_incomplete_ideal_pct':f"{100*v['both_combinations_incomplete']/v['denominator']:.4f}",'possible_all_repeat_counts':' '.join(str(y['repeat_count']) for y in x['conditional_repeat'] if y['distribution'][3]),'posthoc_331_complete_columns':x['posthoc_331']['complete_columns'],'posthoc_last35_zero':x['posthoc_fixed_windows']['35']['complete_0_1_2_3'][0],'posthoc_last40_zero':x['posthoc_fixed_windows']['40']['complete_0_1_2_3'][0],'posthoc_last45_zero':x['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0],'scope':'post-hoc/hypothetical, not prediction'})
print(json.dumps({'status':out['status'],'selected':'HH01','selected_model_percent':[round(v,4) for v in new['uniform_model']['distribution_percent']],'baseline_model_percent':[round(v,4) for v in old['uniform_model']['distribution_percent']],'selected_posthoc_331':new['posthoc_331'],'historical_zero_35_40_45':{k:[lookup[k]['posthoc_fixed_windows'][str(w)]['complete_0_1_2_3'][0] for w in (35,40,45)] for k in ('HH00','HH01','HH08','T14','T15')},'model_theoretical_T14_T15':{k:[round(v,4) for v in lookup[k]['uniform_model']['distribution_percent']] for k in ('T14','T15')},'target_332_result_queried_or_used':False},ensure_ascii=False,indent=2))
