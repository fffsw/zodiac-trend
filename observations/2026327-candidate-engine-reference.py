#!/usr/bin/env python3
"""Audit twelve already-frozen structures; ideal-model analysis only, not a selection algorithm."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from math import comb
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task292_327_release';O=A/'analysis';J=lambda p:json.loads(p.read_text(encoding='utf8'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=J(O/'evidence.json');d=J(O/'manual_decision.json');source=J(O/'handcrafted_candidates.json');study=J(O/'six_sign_repeat_study.json');assert source['choice']==d['choice']=='BB01' and not d['target_result_read_or_used'] and len(source['candidates'])==12 and not (O/'candidate_audit.json').exists()
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');G={z:e['per_zodiac'][z]['numbers'] for z in Z};previous=set(d['previous_326_six']);den=comb(49,6);sort=lambda x:[z for z in Z if z in x];pairkey=lambda a,b:'|'.join(sorted((a,b),key=Z.index))
assert set(previous)=={'狗','兔','鷄','羊','虎','猴'} and all(len({n%3 for n in v})==len({n%2 for n in v})==1 for v in G.values())
def count_required(gs):
 gs=list(gs);return sum((-1)**k*sum(comb(49-sum(len(G[z]) for z in t),6) for t in combinations(gs,k)) for k in range(len(gs)+1))
def metric(slots):
 S,P,T=[slots[k] for k in ('single','pair','triple')];s,p,t=(count_required(x) for x in (S,P,T));sp,st,pt=(count_required(x) for x in (S|P,S|T,P|T));all3=count_required(S|P|T);none=den-s-p-t+sp+st+pt-all3;counts={'single':s,'pair':p,'triple':t,'all_columns':all3,'no_complete_column':none,'at_least_one_complete':den-none,'pair_and_triple':pt};return {'denominator':den,'counts':counts,'percent':{k:100*v/den for k,v in counts.items()}}
def minimum(gs):return {'distinct_zodiacs':len(gs),'road_0_1_2':[sum(G[z][0]%3==k for z in gs) for k in range(3)],'odd_even':[sum(G[z][0]%2==1 for z in gs),sum(G[z][0]%2==0 for z in gs)],'previous_326_identities':sort(gs&previous),'nonprevious_identities':sort(gs-previous)}
out=[]
for c in source['candidates']:
 r=c['roles'];display=set(r.values());universe=display|set(c['reserves']);assert len(universe)==6 and len({r[x] for x in 'ABCD'})==4 and display.isdisjoint(c['reserves']);S={r['top']};P={r['A'],r['B']};T={r['A'],r['C'],r['D']};slots={'single':S,'pair':P,'triple':T,'all_columns':display};ns=sorted(n for z in display for n in G[z]);whole=sorted(n for z in universe for n in G[z]);forced={f'{road}_{par}':[label for label in ('single','pair','triple') if any(G[z][0]%3==road and G[z][0]%2==(par=='odd') for z in slots[label])] for road in range(3) for par in ('odd','even')}
 both={str(w):e['joint_zodiac_absence_periods'][str(w)][pairkey(r['top'],r['A'])] if r['top']!=r['A'] else e['structural_windows'][str(w)]['no_'+r['top']+'_periods'] for w in (35,40,45)}
 out.append({'id':c['id'],'roles':r,'reserves':c['reserves'],'displayed':sort(display),'universe':sort(universe),'displayed_code_count':len(ns),'universe_code_count':len(whole),'display_numbers':ns,'universe_numbers':whole,'display_code_road_0_1_2':[sum(n%3==i for n in ns) for i in range(3)],'display_code_odd_even':[sum(n%2==1 for n in ns),sum(n%2==0 for n in ns)],'display_code_waves':[sum(e['per_number'][str(n)]['wave']==q for n in ns) for q in ('紅','藍','綠')],'ideal_model':metric(slots),'minimums':{k:minimum(v) for k,v in slots.items()},'no_route_parity_forced_incomplete_columns':forced,'standalone_and_shared_both_absent_in_historical_windows':both,'comparison':c['comparison']})
selected=out[0];assert selected['roles']=={'top':'馬','A':'鷄','B':'龍','C':'虎','D':'牛'} and selected['reserves']==['蛇'] and selected['displayed_code_count']==21 and selected['universe_code_count']==25 and selected['standalone_and_shared_both_absent_in_historical_windows']=={'35':6,'40':8,'45':8}
assert selected['minimums']['all_columns']=={'distinct_zodiacs':5,'road_0_1_2':[2,2,1],'odd_even':[3,2],'previous_326_identities':['虎','鷄'],'nonprevious_identities':['牛','龍','馬']} and selected['minimums']['triple']['road_0_1_2']==[1,1,1]
# Dynamic programming over all 12 zodiac-number groups. Count six-ball subsets by previous-sign
# distinct repeat count and five selected identity presence. This is not historic estimation.
sel_signs=selected['displayed'];bits={z:1<<i for i,z in enumerate(sel_signs)};dp={(0,0,0):1}
for z in Z:
 nxt=defaultdict(int);size=len(G[z])
 for (balls,mask,rep),ways in dp.items():
  for take in range(min(size,6-balls)+1):nxt[(balls+take,mask|(bits.get(z,0) if take else 0),rep+int(take>0 and z in previous))]+=ways*comb(size,take)
 dp=nxt
r=selected['roles'];S={r['top']};P={r['A'],r['B']};T={r['A'],r['C'],r['D']};conditional=[]
for k in range(7):
 cnt=Counter()
 for (balls,mask,rep),ways in dp.items():
  if balls!=6 or rep!=k:continue
  got={z for z,b in bits.items() if mask&b};v=[S<=got,P<=got,T<=got];cnt['denominator']+=ways;cnt['single']+=ways*v[0];cnt['pair']+=ways*v[1];cnt['triple']+=ways*v[2];cnt['all_columns']+=ways*all(v);cnt['no_complete_column']+=ways*(not any(v))
 conditional.append({'repeat_count':k,**{n:cnt[n] for n in ('denominator','single','pair','triple','all_columns','no_complete_column')},'percent_if_given_repeat_count':{n:(100*cnt[n]/cnt['denominator'] if cnt['denominator'] else None) for n in ('single','pair','triple','all_columns','no_complete_column')}})
assert [x['denominator'] for x in conditional]==study['uniform_49_independent_model']['6']['counts_0_to_6'] and sum(x['denominator'] for x in conditional)==den and all(sum(x[k] for x in conditional)==selected['ideal_model']['counts'][k] for k in ('single','pair','triple','all_columns','no_complete_column'))
assert all(conditional[i]['triple']==0 for i in (0,1,6)) and all(conditional[i]['pair']==0 for i in (0,6)) and conditional[6]['no_complete_column']==conditional[6]['denominator'] and all(conditional[i]['all_columns']==0 for i in (0,1,4,5,6))
result={'status':'PASS','selection_source':'manual_decision.json frozen before this audit; candidate metrics do not choose or rank','target_327_result_read':False,'candidate_count':len(out),'ideal_model_scope':'Each of the 49 numbers equally likely, six drawn without replacement, and independent of previous draw. This is a mathematical baseline, not verified actual mechanism, performance or return.','display_definition':'A column is complete only if every explicitly named zodiac appears among the six normal numbers; reserve does not replace any member. No winnings/odds assumptions.','selected':selected,'selected_conditional_on_repeat_0_to_6':conditional,'candidates':out,'input_sha256':{n:H(O/n) for n in ('evidence.json','handcrafted_candidates.json','manual_decision.json','six_sign_repeat_study.json')}}
(O/'candidate_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
with (O/'candidate_audit.csv').open('x',encoding='utf8',newline='') as f:
 cols=['id','single','pair','triple','reserve','displayed_codes','universe_codes','repeat_previous_displayed','full_min_0_1_2','triple_min_0_1_2','historical_standalone_and_shared_absent_W35_W40_W45','ideal_single_pct','ideal_pair_pct','ideal_triple_pct','ideal_all_pct','ideal_none_pct','comparison'];w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
 for x in out:
  r=x['roles'];p=x['ideal_model']['percent'];w.writerow({'id':x['id'],'single':r['top'],'pair':r['A']+r['B'],'triple':r['A']+r['C']+r['D'],'reserve':' '.join(x['reserves']),'displayed_codes':x['displayed_code_count'],'universe_codes':x['universe_code_count'],'repeat_previous_displayed':' '.join(x['minimums']['all_columns']['previous_326_identities']),'full_min_0_1_2':'/'.join(map(str,x['minimums']['all_columns']['road_0_1_2'])),'triple_min_0_1_2':'/'.join(map(str,x['minimums']['triple']['road_0_1_2'])),'historical_standalone_and_shared_absent_W35_W40_W45':'/'.join(str(x['standalone_and_shared_both_absent_in_historical_windows'][str(i)]) for i in (35,40,45)),'ideal_single_pct':f"{p['single']:.6f}",'ideal_pair_pct':f"{p['pair']:.6f}",'ideal_triple_pct':f"{p['triple']:.6f}",'ideal_all_pct':f"{p['all_columns']:.6f}",'ideal_none_pct':f"{p['no_complete_column']:.6f}",'comparison':x['comparison']})
print(json.dumps({'status':result['status'],'selected':selected,'counterfactual_BB02_ideal':out[1]['ideal_model'],'conditional_repeat_counts':conditional,'target_result_read':False},ensure_ascii=False,indent=2))
