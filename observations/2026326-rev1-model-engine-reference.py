#!/usr/bin/env python3
"""Fixed post-hoc plan comparison: exact fair 49-ball model via zodiac-set Mobius inversion.
This is a conditional mathematical baseline, NOT an authenticated draw mechanism or ranking.
"""
from pathlib import Path
from itertools import combinations
from math import comb
import json,hashlib
R=Path('/home/user');A=R/'archive/task290_326_revision';O=A/'analysis';B=A/'before';J=lambda p:json.loads(p.read_text(encoding='utf8'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();plans=J(O/'revision_design.json');old=J(B/'326-v1-candidate-audit.json');assert J(O/'maximum_independent_qc.json')['status']=='PASS' and len(plans['plans'])==11
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z=lambda n:Z[(7-n)%12];size=[sum(n2z(n)==z for n in range(1,50)) for z in Z];assert size==[4,4,4,4,4,4,5,4,4,4,4,4];den=comb(49,6);subset_sizes=[0]*4096
for m in range(1,4096):
 bit=m&-m;subset_sizes[m]=subset_sizes[m^bit]+size[bit.bit_length()-1]
# C(size of all allowed signs,6) = sum of exact-active-set counts over all submasks.
exact=[comb(n,6) if n>=6 else 0 for n in subset_sizes]
for i in range(12):
 for mask in range(4096):
  if mask>>i&1:exact[mask]-=exact[mask^(1<<i)]
assert min(exact)>=0 and sum(exact)==den
bitset=lambda zs:sum(1<<Z.index(z) for z in set(zs));prev=bitset(plans['previous_325']);repeat=[sum(v for m,v in enumerate(exact) if (m&prev).bit_count()==r) for r in range(5)];assert sum(repeat)==den
out=[];per={}
for p in plans['plans']:
 q=p['roles'];abcd=[q[k] for k in 'ABCD'];shown=set([q['top']]+abcd);universe=shown|set(p['reserves']);assert len(set(abcd))==4 and len(universe)==6 and shown.isdisjoint(p['reserves']) and len(set(p['reserves']))==len(p['reserves'])
 slot=[bitset([q['top']]),bitset([q['A'],q['B']]),bitset([q['A'],q['C'],q['D']])];counts=[0]*4;col=[0]*3;rc=[[0]*4 for _ in range(5)];event=[]
 for m,v in enumerate(exact):
  flags=tuple(int(m&s==s) for s in slot);c=sum(flags);r=(m&prev).bit_count();counts[c]+=v;rc[r][c]+=v
  for i,x in enumerate(flags):col[i]+=v*x
  event.append(flags)
 assert sum(counts)==den and all(sum(rc[i])==repeat[i] for i in range(5));per[p['id']]=event
 out.append({'id':p['id'],'roles':q,'reserve_only':p['reserves'],'displayed_in_order':list(dict.fromkeys([q['top']]+abcd)),'previous_signs_in_three':sorted(set([q['A'],q['C'],q['D']])&set(plans['previous_325']),key=Z.index),'number_of_previous_signs_in_three':len(set([q['A'],q['C'],q['D']])&set(plans['previous_325'])),'complete_columns_numerator_0_to_3':counts,'single_pair_triple_numerators':col,'percent':{'single':100*col[0]/den,'pair':100*col[1]/den,'triple':100*col[2]/den,'all':100*counts[3]/den,'zero':100*counts[0]/den},'by_repeat_count':{str(r):{'model_hands':repeat[r],'complete_columns_numerator_0_to_3':rc[r],'three_complete_numerator':sum(v for m,v in enumerate(exact) if (m&prev).bit_count()==r and event[m][2]),'zero_pct_conditional':100*rc[r][0]/repeat[r] if repeat[r] else None,'all_pct_conditional':100*rc[r][3]/repeat[r] if repeat[r] else None} for r in range(5)},'comparison_note':p['comparison']})
by={x['id']:x for x in out};v1,v2=by['R00'],by['R01'];assert v1['roles']=={'top':'羊','A':'虎','B':'羊','C':'馬','D':'兔'} and v2['roles']=={'top':'羊','A':'虎','B':'羊','C':'馬','D':'鷄'};aa=next(x for x in old['candidates'] if x['id']=='AA16');assert v2['roles']==aa['roles'] and v2['reserve_only']==aa['reserves'];keys={'single':'single_pct','pair':'pair_pct','triple':'triple_pct','all':'all_columns_pct','zero':'no_column_pct'};assert all(abs(v2['percent'][k]-aa['ideal_model_probabilities_percent'][v])<1e-10 for k,v in keys.items())
assert v1['complete_columns_numerator_0_to_3']==v2['complete_columns_numerator_0_to_3'] and v1['single_pair_triple_numerators']==v2['single_pair_triple_numerators']
gain=[0]*5;lose=[0]*5
for m,v in enumerate(exact):
 r=(m&prev).bit_count();a=per['R00'][m][2];b=per['R01'][m][2];gain[r]+=v*(b and not a);lose[r]+=v*(a and not b)
assert gain==[0,0,0,442240,185840] and lose==[0,0,442240,185840,0] and sum(gain)==sum(lose)==628080
assert v2['by_repeat_count']['4']['three_complete_numerator']==repeat[4] and all(v2['by_repeat_count'][str(r)]['three_complete_numerator']==0 for r in (0,1,2))
result={'status':'PASS_EXACT_MATHEMATICAL_MODEL_NOT_FORECAST','scope':'Fixed manual comparisons chosen after examining data. Assumes six numbers uniformly drawn without replacement from 1–49, the 2026 mapping, and identity-only first-six settlement. Neither actual fairness, source, timing, outcome, prediction nor returns authenticated.','identity_method':'2^12 allowed-zodiac subsets and Mobius inversion; exact present-set weights','sign_number_sizes':dict(zip(Z,size)),'model_denominator':den,'prior_distinct':['虎','馬','鷄','龍'],'repeat_0_to_4_numerators':repeat,'repeat_0_to_4_percent':[100*x/den for x in repeat],'plans':out,'selected_id':'R01','old_v1_id':'R00','old_new_triple_disagreement':{'v2_complete_v1_incomplete_by_repeat_0_to_4':gain,'v1_complete_v2_incomplete_by_repeat_0_to_4':lose,'v2_gain_total':sum(gain),'v2_loss_total':sum(lose),'interpretation':'The equal four-number groups for rabbit/chicken balance marginal ideal-model probabilities; conditional scenarios exchange, so no predicted improvement.'},'target_result_read':False,'input_design_sha256':H(O/'revision_design.json')}
p=O/'revision_model.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'status':result['status'],'denominator':den,'repeat':repeat,'old':v1['percent'],'revised':v2['percent'],'gain_by_repeat':gain,'lose_by_repeat':lose,'selected_r4_three_complete':v2['by_repeat_count']['4']['three_complete_numerator'],'old_r4_three_complete':v1['by_repeat_count']['4']['three_complete_numerator'],'sha256':H(p)},ensure_ascii=False,indent=2))
