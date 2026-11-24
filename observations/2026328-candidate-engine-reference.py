#!/usr/bin/env python3
"""Audit frozen 328 structures under explicit combinatorial assumptions; no 328 outcomes."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
from math import comb
import csv,hashlib,json
R=Path('/home/user');O=R/'archive/task295_328_release/analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=J(O/'evidence.json');d=J(O/'manual_decision.json');src=J(O/'handcrafted_candidates.json');study=J(O/'six_sign_repeat_study.json');assert d['choice']==src['choice']=='CC01' and not d['target_328_result_queried_or_used'] and len(src['candidates'])==12 and not (O/'candidate_audit.json').exists()
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');G={z:e['per_zodiac'][z]['numbers'] for z in Z};prev=set(d['previous_327_six']);den=comb(49,6);order=lambda s:[z for z in Z if z in s];key=lambda a,b:'|'.join(order({a,b}));assert prev=={'狗','馬','鼠','虎','鷄','羊'} and len(G['馬'])==5 and all(len(G[z])==4 for z in Z if z!='馬')
def req(gs):
 gs=list(gs);return sum((-1)**k*sum(comb(49-sum(len(G[z]) for z in t),6) for t in combinations(gs,k)) for k in range(len(gs)+1))
def metrics(s,p,t):
 s0,p0,t0=map(req,(s,p,t));sp,st,pt=(req(x) for x in (s|p,s|t,p|t));a=req(s|p|t);none=den-s0-p0-t0+sp+st+pt-a;counts={'single':s0,'pair':p0,'triple':t0,'all_columns':a,'no_complete_column':none,'at_least_one_complete':den-none,'pair_and_triple':pt};return {'denominator':den,'counts':counts,'percent':{k:100*v/den for k,v in counts.items()}}
def minreq(gs):return {'distinct_zodiacs':len(gs),'road_0_1_2':[sum(G[z][0]%3==k for z in gs) for k in range(3)],'odd_even':[sum(G[z][0]%2==1 for z in gs),sum(G[z][0]%2==0 for z in gs)],'previous_327_identities':order(gs&prev),'nonprevious_identities':order(gs-prev)}
out=[]
for c in src['candidates']:
 r=c['roles'];display=set(r.values());univ=display|set(c['reserves']);assert len({r[k] for k in ('A','B','C','D')})==4 and len(univ)==6 and display.isdisjoint(c['reserves']);s={r['top']};p={r['A'],r['B']};t={r['A'],r['C'],r['D']};slots={'single':s,'pair':p,'triple':t,'all_columns':display};nums=sorted(n for z in display for n in G[z]);allnums=sorted(n for z in univ for n in G[z]);forced={f'{road}_{par}':[name for name in ('single','pair','triple') if any(G[z][0]%3==road and G[z][0]%2==(par=='odd') for z in slots[name])] for road in range(3) for par in ('odd','even')};joint={str(w):e['joint_zodiac_absence_periods'][str(w)][key(r['top'],r['A'])] if r['top']!=r['A'] else e['structural_windows'][str(w)]['no_'+r['top']+'_periods'] for w in (35,40,45)}
 out.append({'id':c['id'],'roles':r,'reserves':c['reserves'],'displayed':order(display),'universe':order(univ),'displayed_code_count':len(nums),'universe_code_count':len(allnums),'display_numbers':nums,'universe_numbers':allnums,'display_code_road_0_1_2':[sum(n%3==i for n in nums) for i in range(3)],'display_code_odd_even':[sum(n%2==1 for n in nums),sum(n%2==0 for n in nums)],'ideal_model':metrics(s,p,t),'minimums':{k:minreq(v) for k,v in slots.items()},'no_route_parity_forced_incomplete_columns':forced,'standalone_and_shared_both_absent_in_historical_windows':joint,'comparison':c['comparison']})
sel=out[0];assert sel['roles']=={'top':'馬','A':'狗','B':'鷄','C':'馬','D':'蛇'} and sel['reserves']==['虎','牛'] and sel['displayed_code_count']==17 and sel['universe_code_count']==25 and sel['minimums']['all_columns']['previous_327_identities']==['馬','鷄','狗'] and sel['minimums']['all_columns']['nonprevious_identities']==['蛇'] and sel['minimums']['triple']['road_0_1_2']==[1,1,1]
assert out[11]['ideal_model']==sel['ideal_model'] and out[11]['roles']==sel['roles']
# Count selected events by exactly how many of the six previous identities appear.
bits={z:1<<i for i,z in enumerate(sel['displayed'])};dp={(0,0,0):1}
for z in Z:
 nxt=defaultdict(int)
 for (balls,mask,repeats),ways in dp.items():
  for take in range(min(len(G[z]),6-balls)+1):nxt[(balls+take,mask|(bits.get(z,0) if take else 0),repeats+int(take>0 and z in prev))]+=ways*comb(len(G[z]),take)
 dp=nxt
r=sel['roles'];S={r['top']};P={r['A'],r['B']};T={r['A'],r['C'],r['D']};conditional=[]
for k in range(7):
 cnt=Counter()
 for (balls,mask,rep),ways in dp.items():
  if balls!=6 or rep!=k:continue
  got={z for z,b in bits.items() if mask&b};v=[S<=got,P<=got,T<=got];cnt['denominator']+=ways;cnt['single']+=ways*v[0];cnt['pair']+=ways*v[1];cnt['triple']+=ways*v[2];cnt['all_columns']+=ways*all(v);cnt['no_complete_column']+=ways*(not any(v))
 conditional.append({'repeat_count':k,**{n:cnt[n] for n in ('denominator','single','pair','triple','all_columns','no_complete_column')},'percent_if_given_repeat_count':{n:(100*cnt[n]/cnt['denominator'] if cnt['denominator'] else None) for n in ('single','pair','triple','all_columns','no_complete_column')}})
assert [x['denominator'] for x in conditional]==study['uniform_49_independent_model']['6']['counts_0_to_6'] and sum(x['denominator'] for x in conditional)==den and all(sum(x[k] for x in conditional)==sel['ideal_model']['counts'][k] for k in ('single','pair','triple','all_columns','no_complete_column'))
assert all(conditional[i]['all_columns']==0 for i in (0,1,2,6)) and all(conditional[i]['all_columns']>0 for i in (3,4,5)) and conditional[6]['single']==conditional[6]['pair']==conditional[6]['denominator'] and conditional[6]['triple']==conditional[6]['no_complete_column']==0
assert all(B in (C,D) for A,B,C,D in product(range(3),repeat=4) if A!=B and len({A,C,D})==3)
recent=e['recent_45_normal_records'];windowrisk={}
for w in (35,40,45):
 rows=recent[-w:];n=sum('馬' not in set(x['zodiacs']) and ('狗' not in set(x['zodiacs']) or '鷄' not in set(x['zodiacs'])) for x in rows);windowrisk[str(w)]={'zero_complete_columns':n,'horse_and_dog_both_absent':e['joint_zodiac_absence_periods'][str(w)][key('馬','狗')],'horse_and_chicken_both_absent':e['joint_zodiac_absence_periods'][str(w)][key('馬','鷄')]}
prior=J(R/'archive/task294_327_review/before/327-candidates.json')['selected']['ideal_model'];assert prior['percent']['all_columns']<sel['ideal_model']['percent']['all_columns'] and prior['percent']['no_complete_column']<sel['ideal_model']['percent']['no_complete_column']
result={'status':'PASS','selection_source':'manual_decision.json frozen after disclosed spot checks, before this formal audit; not blind or preregistered','target_328_result_queried_or_used':False,'candidate_count':len(out),'ideal_model_scope':'Six different numbers sampled uniformly without replacement from 49; independent of previous draw. This is a mathematical baseline, not verified actual mechanism, real-world success, gain or forecast.','display_definition':'Each named identity must appear among the six normal numbers to complete its column; reserves never substitute.','selected':sel,'selected_conditional_on_repeat_0_to_6':conditional,'previous_327_BB01_ideal_comparison':prior,'structural_impossibility':'If pair A/B covers different roads and triple A/C/D covers all three roads, B necessarily shares a road with C or D; exact identity matching remains necessary.','selected_window_zero_column_risk':windowrisk,'candidates':out,'input_sha256':{n:H(O/n) for n in ('evidence.json','handcrafted_candidates.json','manual_decision.json','six_sign_repeat_study.json')}};(O/'candidate_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
with (O/'candidate_audit.csv').open('x',encoding='utf8',newline='') as f:
 cols=['id','single','pair','triple','reserve','displayed_codes','universe_codes','previous_identities_shown','all_min_0_1_2','triple_min_0_1_2','historical_top_shared_both_absent_W35_W40_W45','ideal_single_pct','ideal_pair_pct','ideal_triple_pct','ideal_all_pct','ideal_none_pct','comparison'];w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
 for x in out:
  r=x['roles'];p=x['ideal_model']['percent'];w.writerow({'id':x['id'],'single':r['top'],'pair':r['A']+r['B'],'triple':r['A']+r['C']+r['D'],'reserve':' '.join(x['reserves']),'displayed_codes':x['displayed_code_count'],'universe_codes':x['universe_code_count'],'previous_identities_shown':' '.join(x['minimums']['all_columns']['previous_327_identities']),'all_min_0_1_2':'/'.join(map(str,x['minimums']['all_columns']['road_0_1_2'])),'triple_min_0_1_2':'/'.join(map(str,x['minimums']['triple']['road_0_1_2'])),'historical_top_shared_both_absent_W35_W40_W45':'/'.join(str(x['standalone_and_shared_both_absent_in_historical_windows'][str(i)]) for i in (35,40,45)),'ideal_single_pct':f"{p['single']:.6f}",'ideal_pair_pct':f"{p['pair']:.6f}",'ideal_triple_pct':f"{p['triple']:.6f}",'ideal_all_pct':f"{p['all_columns']:.6f}",'ideal_none_pct':f"{p['no_complete_column']:.6f}",'comparison':x['comparison']})
print(json.dumps({'status':'PASS','selected':sel,'previous_327_ideal':prior,'conditional_repeat_counts':conditional,'recent_window_zero_risk':windowrisk,'target_328_result_queried_or_used':False},ensure_ascii=False,indent=2))
