#!/usr/bin/env python3
"""Settle one already-frozen plan and all manual comparisons using user-supplied first six.
Inputs are explicit configs; no external draw access, next choice, rankings, or site writes.
320 was an actually published unverified display; this freeze occurs after receipt of user input and is not predraw certification.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from math import comb
import csv,hashlib,json,sys
R=Path('/home/user');period=int(sys.argv[1]);assert period==2026320;A=R/'archive/task278_320_review';O=A/'analysis';J=lambda p:json.loads(p.read_text(encoding='utf8'));cfg=J(O/'retrospective_config.json');assert cfg['period']==period
def path(k):return R/cfg['files'][k]
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def save(p,x):
 assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z={n:Z[(7-n)%12] for n in range(1,50)};groups={z:{n for n in range(1,50) if n2z[n]==z} for z in Z};order=lambda s:sorted(s,key=Z.index);numbers=lambda r:[int(r[f'n{i}']) for i in range(1,7)];zs=lambda r:[r[f'z{i}'] for i in range(1,7)];pairkey=lambda a,b:'|'.join(sorted([a,b],key=Z.index))
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠'
u=J(path('user'));ns=u['normal_numbers'];nz=u['normal_zodiacs'];sp=u['seventh_number'];sz=u['seventh_zodiac'];assert u['issue']==period and u['issue_user_specified'] and u['date'] is None and len(ns)==6 and len(set(ns+[sp]))==7 and [n2z[n] for n in ns]==nz and n2z[sp]==sz
assert ns==[14,17,32,34,24,46] and sp==20 and cfg['plan_status']=='PUBLISHED_320_UNVERIFIED_DISPLAY'
rows=sorted(C(path('history_prior')),key=lambda r:int(r['period']));assert len(rows)==1048+(period-2026318) and rows[-1]['period']==str(period-1) and rows[-1]['date']=='' and not any(int(r['period'])>=period for r in rows)
e=J(path('evidence_prior'));assert e['history_rows']==len(rows) and e['latest_period']==period-1 and e['history_sha256']==hashlib.sha256(path('history_prior').read_bytes()).hexdigest()
hand=J(path('candidates'));audit=J(path('audit'));manual=J(path('manual'));assert len(hand['candidates'])==len(audit['candidates'])==38 and hand['proposed_id']==manual['human_choice']==audit['selected']['id']==cfg['selection_id'];sel=next(c for c in hand['candidates'] if c['id']==cfg['selection_id']);roles=sel['roles'];display=list(dict.fromkeys(roles[k] for k in ('top','A','B','C','D')));univ=display+sel['reserves'];assert len(set(univ))==6 and set(univ)==set(manual['universe']) and roles['top']==manual['top'] and [roles['A'],roles['B']]==manual['pair'] and [roles['A'],roles['C'],roles['D']]==manual['triple'] and sel['reserves']==manual['reserves']
d=J(path('manual_site'))['decisions']['2026320'];assert d['universe_zodiac']==manual['universe'] and [d['top_zodiac'],d['a_zodiac'],d['b_zodiac'],d['c_zodiac'],d['d_zodiac']]==[roles[k] for k in ('top','A','B','C','D')]
actual=set(nz);seven=actual|{sz};prev=rows[-1];prev6=set(zs(prev));prev7=prev6|{prev['special_zodiac']}
def settle(r,reserve):
 disp={r[k] for k in ('top','A','B','C','D')};universe=disp|set(reserve);slots=[]
 for name,req in [('single',{r['top']}),('double',{r['A'],r['B']}),('triple',{r['A'],r['C'],r['D']})]:
  slots.append({'name':name,'required':order(req),'present':order(req&actual),'missing':order(req-actual),'present_count':len(req&actual),'needed_count':len(req),'complete':req<=actual,'balls':[{'number':n,'zodiac':z} for n,z in zip(ns,nz) if z in req]})
 return {'display':order(disp),'universe':order(universe),'reserve_only':order(set(reserve)),'slots':slots,'complete_count':sum(x['complete'] for x in slots),'normal_distinct_signs':order(actual),'displayed_signs_hit':order(actual&disp),'reserve_signs_hit':order(actual&set(reserve)),'universe_signs_hit':order(actual&universe),'outside_universe_signs':order(actual-universe),'display_ball_count':sum(z in disp for z in nz),'reserve_ball_count':sum(z in reserve for z in nz),'universe_ball_count':sum(z in universe for z in nz),'outside_universe_ball_count':sum(z not in universe for z in nz)}
s=settle(roles,sel['reserves'])
def metrics(v):
 z=[n2z[n] for n in v];zc=Counter(z);return {'numbers':v,'zodiacs':z,'distinct_zodiac_count':len(zc),'zodiac_ball_count':dict(zc),'multiplicity_pattern':sorted(zc.values(),reverse=True),'road_0_1_2':[sum(n%3==k for n in v) for k in range(3)],'odd_even':[sum(n%2 for n in v),sum(n%2==0 for n in v)],'red_blue_green':[sum(wave(n)==x for n in v) for x in ('紅','藍','綠')],'small_big_1_24_25_49':[sum(n<=24 for n in v),sum(n>=25 for n in v)],'heads_0_to_4':[sum(n//10==k for n in v) for k in range(5)],'tails_0_to_9':[sum(n%10==k for n in v) for k in range(10)],'sum':sum(v),'span':max(v)-min(v),'road_numbers':{str(k):[n for n in v if n%3==k] for k in range(3)},'road_parity_numbers':{f'{k}_{p}':[n for n in v if n%3==k and n%2==(p=='odd')] for k in range(3) for p in ('odd','even')},'wave_numbers':{c:[n for n in v if wave(n)==c] for c in ('紅','藍','綠')}}
m=metrics(ns)
assert m['road_0_1_2']==[1,2,3] and m['odd_even']==[1,5] and m['red_blue_green']==[3,1,2] and m['sum']==167 and m['span']==32 and m['distinct_zodiac_count']==5 and [v['present_count'] for v in s['slots']]==[1,0,1] and s['complete_count']==1
pre=[]
for n,z in zip(ns,nz):
 x=e['per_number'][str(n)];loc='top' if z==roles['top'] else 'A' if z==roles['A'] else 'B' if z==roles['B'] else 'C' if z==roles['C'] else 'D' if z==roles['D'] else 'reserve' if z in univ else 'outside_universe';pre.append({'number':n,'zodiac':z,'road':x['road'],'odd_even':x['odd_even'],'wave':x['wave'],'head':x['head'],'tail':x['tail'],'last_normal_age_before':x['last_normal_age'],'windows_before':x['window_counts'],'location':loc})
shape={}
for w in (10,20,35,40,45,60,100,250):
 rs=rows[-w:];mm=[metrics(numbers(r)) for r in rs];ct=lambda f:sum(f(x) for x in mm);v={'first_period':int(rs[0]['period']),'last_period':period-1,'periods':w,'exact_actual_road':ct(lambda x:x['road_0_1_2']==m['road_0_1_2']),'exact_actual_odd_even':ct(lambda x:x['odd_even']==m['odd_even']),'exact_actual_waves':ct(lambda x:x['red_blue_green']==m['red_blue_green']),'actual_or_fewer_distinct_signs':ct(lambda x:x['distinct_zodiac_count']<=m['distinct_zodiac_count']),'no_top':ct(lambda x:roles['top'] not in x['zodiacs']),'no_shared':ct(lambda x:roles['A'] not in x['zodiacs']),'no_top_and_shared':ct(lambda x:roles['top'] not in x['zodiacs'] and roles['A'] not in x['zodiacs']),'at_most_one_even':ct(lambda x:x['odd_even'][1]<=1),'at_most_two_even':ct(lambda x:x['odd_even'][1]<=2),'at_most_two_odd':ct(lambda x:x['odd_even'][0]<=2),'at_most_four_signs':ct(lambda x:x['distinct_zodiac_count']<=4),'three_roads_present':ct(lambda x:all(v>0 for v in x['road_0_1_2']))}
 for k in range(3):
  v[f'no_{k}road']=ct(lambda x:x['road_0_1_2'][k]==0);v[f'at_most_one_{k}road']=ct(lambda x:x['road_0_1_2'][k]<=1)
  for p in ('odd','even'):v[f'no_{p}_{k}road']=ct(lambda x:not x['road_parity_numbers'][f'{k}_{p}'])
 for z in Z:
  peer=e['same_route_parity_peer_present_target_absent_periods'][str(w)][z]['peer'];v[f'no_{z}']=ct(lambda x:z not in x['zodiacs']);v[f'peer_{peer}_present_no_{z}']=ct(lambda x:peer in x['zodiacs'] and z not in x['zodiacs']);assert v[f'peer_{peer}_present_no_{z}']==e['same_route_parity_peer_present_target_absent_periods'][str(w)][z]['target_absent_peer_present_periods']
 if roles['top']!=roles['A']:assert v['no_top_and_shared']==e['joint_zodiac_absence_periods'][str(w)][pairkey(roles['top'],roles['A'])]
 for k in range(3):
  assert v[f'no_{k}road']==e['structural_windows'][str(w)][f'no_{k}road_periods']
  for p in ('odd','even'):assert v[f'no_{p}_{k}road']==e['structural_windows'][str(w)][f'no_{p}_{k}road_periods']
 shape[str(w)]=v
cand=[];canonical=defaultdict(list)
for x,y in zip(hand['candidates'],audit['candidates']):
 assert x['id']==y['id'] and x['roles']==y['roles'] and x['reserves']==y['reserves'];r=x['roles'];st=settle(r,x['reserves']);key=(r['top'],frozenset([r['A'],r['B']]),frozenset([r['A'],r['C'],r['D']]));canonical[key].append(x['id']);cand.append({'id':x['id'],'roles':r,'reserves':x['reserves'],'slots':st['slots'],'complete_count':st['complete_count'],'display_signs_hit':st['displayed_signs_hit'],'reserve_signs_hit':st['reserve_signs_hit'],'outside_universe_signs':st['outside_universe_signs'],'display_ball_count':st['display_ball_count'],'universe_ball_count':st['universe_ball_count'],'original_comparison':x['comparison']})
Acounts=Counter(x['roles']['A'] for x in cand);dist=Counter(x['complete_count'] for x in cand);dupes=[v for v in canonical.values() if len(v)>1];overlap=[x['id'] for x in cand if x['roles']['top'] in {x['roles'][k] for k in 'ABCD'}];assert audit['unique_column_structures']==len(canonical) and audit['top_overlap_candidate_count']==len(overlap) and audit['shared_A_counts']==dict(Acounts)
lookup={x['id']:x for x in cand};assert lookup[cfg['selection_id']]['slots']==s['slots']
# Ideal illustrative model only; no certification about actual source, mechanism, or gain.
den=comb(49,6)
def count(gs):
 gs=list(set(gs));return sum((-1)**k*sum(comb(49-sum(len(groups[z]) for z in t),6) for t in combinations(gs,k)) for k in range(len(gs)+1))
cols=[{roles['top']},{roles['A'],roles['B']},{roles['A'],roles['C'],roles['D']}];a,b,c=[count(t) for t in cols];ab=count(cols[0]|cols[1]);ac=count(cols[0]|cols[2]);bc=count(cols[1]|cols[2]);abc=count(cols[0]|cols[1]|cols[2]);none=den-a-b-c+ab+ac+bc-abc;model={'assumption':'49 distinct numbers equally likely, sample six without replacement; illustrative and not verified for the actual mechanism','column_complete_percent':[100*x/den for x in (a,b,c)],'all_complete_percent':100*abc/den,'zero_complete_percent':100*none/den};old=audit['selected']['ideal_model_probabilities_percent'];assert abs(model['zero_complete_percent']-old['no_column_pct'])<1e-9 and abs(model['all_complete_percent']-old['all_columns_pct'])<1e-9
res={'scope':cfg['scope'],'plan_status':cfg['plan_status'],'input':u,'choice':{'id':cfg['selection_id'],'roles':roles,'reserves':sel['reserves'],'universe':univ},'actual_structure':m,'settlement':s,'previous_input_identity':{'previous_normal_distinct':order(prev6),'previous_seven_distinct':order(prev7),'current_normal_distinct':order(actual),'current_seven_distinct':order(seven),'seven_v_seven':order(seven&prev7),'six_v_six':order(actual&prev6),'current_six_v_previous_seven':order(actual&prev7),'same_numbers_seven_v_seven':sorted(set(ns+[sp])&set(numbers(prev)+[int(prev['special'])])),'same_numbers_six_v_six':sorted(set(ns)&set(numbers(prev)))},'each_actual_normal_ball_prior':pre,'pre_period_shape_windows':shape,'zodiac_prior':e['per_zodiac'],'number_prior':e['per_number'],'frozen_38_candidate_review':{'count':38,'A_counts':dict(Acounts),'unique_actual_column_structures':len(canonical),'duplicate_groups_excluding_reserve':dupes,'top_overlap_cases':overlap,'post_result_complete_count_distribution':dict(dist),'original_order_candidates':cand},'ideal_model_only':model}
save(O/'retrospective.json',res)
with (O/'prior_shape_windows.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['window']+list(shape['35']));w.writeheader();[w.writerow({'window':k,**v}) for k,v in shape.items()]
with (O/'candidate_outcomes_original_order.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['candidate_id','single','double','triple','reserves','single_progress','double_progress','triple_progress','complete_columns','normal_display_balls','normal_universe_balls','normal_reserve_signs','normal_outside_universe_signs','note'])
 for x in cand:
  r=x['roles'];w.writerow([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],' '.join(x['reserves'])]+[f"{t['present_count']}/{t['needed_count']}" for t in x['slots']]+[x['complete_count'],x['display_ball_count'],x['universe_ball_count'],' '.join(x['reserve_signs_hit']),' '.join(x['outside_universe_signs']),'after-result diagnostic only; not a rule ranking or predraw claim'])
with (O/'user_six_prior_ledger.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['number','zodiac','road','odd_even','wave','head','tail','prior_last_normal_age','W10','W20','W35','W40','W45','location'])
 for x in pre:w.writerow([f"{x['number']:02d}",x['zodiac'],x['road'],x['odd_even'],x['wave'],x['head'],x['tail'],x['last_normal_age_before']]+[x['windows_before'][str(k)] for k in (10,20,35,40,45)]+[x['location']])
print('PASS',period,cfg['plan_status'],'choice',cfg['selection_id'],'38 candidates settled; no external results or site writes')
print('structure',json.dumps(m,ensure_ascii=False));print('settlement',json.dumps(s,ensure_ascii=False));print('repeats',json.dumps(res['previous_input_identity'],ensure_ascii=False));print('pre-windows',json.dumps({w:shape[w] for w in ('35','40','45')},ensure_ascii=False));print('candidate distribution',dict(dist),'structures',len(canonical),'shared identities',dict(Acounts));print('ideal hypothetical model',json.dumps(model,ensure_ascii=False))
