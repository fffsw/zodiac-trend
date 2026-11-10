#!/usr/bin/env python3
"""Review user-provided 314 only against frozen 314 display and its hand candidates.
No third-party draw fetch, no main-history update, no 315 choice, no rankings.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import product
from math import comb
import csv,json,re,hashlib
R=Path('/home/user');A=R/'archive/task261_314_failure_review';B=A/'before';O=A/'analysis';J=lambda p:json.loads(p.read_text(encoding='utf8'))
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zmap={n:Z[(7-n)%12] for n in range(1,50)};group={z:{n for n in range(1,50) if zmap[n]==z} for z in Z};order=lambda s:sorted(s,key=Z.index)
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠';nums=lambda r:[int(r[f'n{i}']) for i in range(1,7)];zods=lambda r:[r[f'z{i}'] for i in range(1,7)]
rows=sorted(C(B/'history-through-313.csv'),key=lambda r:int(r['period']));u=J(A/'input/user_314.json');e=J(B/'314-evidence-before-draw.json');assert len(rows)==1044 and rows[-1]['period']=='2026313' and rows[-1]['date']=='' and not any(int(r['period'])>=2026314 for r in rows)
ns=u['normal_numbers'];nz=u['normal_zodiacs'];sp=u['seventh_number'];sz=u['seventh_zodiac'];assert ns==[13,26,9,37,34,44] and sp==31 and len(set(ns+[sp]))==7 and [zmap[n] for n in ns]==nz==['馬','蛇','狗','馬','鷄','豬'] and zmap[sp]==sz=='鼠' and set(nz+[sz])==set(u['seven_ball_distinct_zodiacs']) and u['date'] is None
actual=set(nz);seven=actual|{sz};prev6=set(zods(rows[-1]));prev7=prev6|{rows[-1]['special_zodiac']};chosen=J(B/'314-handwritten-decision.json');doc=J(B/'manual-site-decisions.json')['decisions']['2026314']
d={'universe':doc['universe_zodiac'],'top':doc['top_zodiac'],'A':doc['a_zodiac'],'B':doc['b_zodiac'],'C':doc['c_zodiac'],'D':doc['d_zodiac']};assert d=={'universe':['牛','虎','馬','狗','鷄','豬'],'top':'牛','A':'虎','B':'馬','C':'狗','D':'鷄'}
html=(B/'314-published-page.html').read_text(encoding='utf8');raw=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',html).group(1))['2026313'];assert raw=={'U':[Z.index(z) for z in d['universe']],'top':Z.index(d['top']),'A':Z.index(d['A']),'B':Z.index(d['B']),'C':Z.index(d['C']),'D':Z.index(d['D']),'top_overlap_mode':'coverage'}
def settle(x):
 slots=[];display={x[k] for k in ('top','A','B','C','D')};univ=set(x['universe']);reserve=univ-display
 for name,s in [('single',{x['top']}),('double',{x['A'],x['B']}),('triple',{x['A'],x['C'],x['D']})]:
  slots.append({'name':name,'required':order(s),'present':order(s&actual),'missing':order(s-actual),'present_count':len(s&actual),'needed_count':len(s),'complete':s<=actual,'balls':[{ 'number':n,'zodiac':z} for n,z in zip(ns,nz) if z in s]})
 return {'display':order(display),'universe':order(univ),'reserve_only':order(reserve),'slots':slots,'complete_count':sum(x['complete'] for x in slots),'normal_distinct_signs':order(actual),'displayed_signs_hit':order(actual&display),'reserve_signs_hit':order(actual&reserve),'universe_signs_hit':order(actual&univ),'outside_universe_signs':order(actual-univ),'display_ball_count':sum(z in display for z in nz),'reserve_ball_count':sum(z in reserve for z in nz),'universe_ball_count':sum(z in univ for z in nz),'outside_universe_ball_count':sum(z not in univ for z in nz)}
settled=settle(d);assert [s['present_count'] for s in settled['slots']]==[0,1,2] and settled['complete_count']==0 and settled['display_ball_count']==4 and settled['reserve_ball_count']==1 and settled['universe_ball_count']==5 and settled['outside_universe_ball_count']==1

def metrics(v):
 z=[zmap[n] for n in v];zc=Counter(z);road=[sum(n%3==k for n in v) for k in range(3)];return {'numbers':v,'zodiacs':z,'distinct_zodiac_count':len(zc),'zodiac_ball_count':dict(zc),'multiplicity_pattern':sorted(zc.values(),reverse=True),'road_0_1_2':road,'odd_even':[sum(n%2 for n in v),sum(n%2==0 for n in v)],'red_blue_green':[sum(wave(n)==x for n in v) for x in ('紅','藍','綠')],'small_big_1_24_25_49':[sum(n<=24 for n in v),sum(n>=25 for n in v)],'heads_0_to_4':[sum(n//10==k for n in v) for k in range(5)],'tails_0_to_9':[sum(n%10==k for n in v) for k in range(10)],'sum':sum(v),'span':max(v)-min(v),'odd_2road_numbers':[n for n in v if n%3==2 and n%2==1],'even_2road_numbers':[n for n in v if n%3==2 and n%2==0],'zero_road_numbers':[n for n in v if n%3==0]}
m=metrics(ns);assert m['road_0_1_2']==[1,3,2] and m['odd_even']==[3,3] and m['red_blue_green']==[2,3,1] and m['small_big_1_24_25_49']==[2,4] and m['heads_0_to_4']==[1,1,1,2,1] and m['sum']==163 and m['span']==35 and m['odd_2road_numbers']==[] and m['even_2road_numbers']==[26,44] and m['zero_road_numbers']==[9] and m['multiplicity_pattern']==[2,1,1,1,1]
shape={}
for w in (10,20,35,40,45,60,100,250):
 recs=rows[-w:];ms=[metrics(nums(r)) for r in recs];ct=lambda f:sum(f(x) for x in ms)
 shape[str(w)]={'first_period':int(recs[0]['period']),'last_period':2026313,'n':w,'exact_road_1_3_2':ct(lambda x:x['road_0_1_2']==[1,3,2]),'road0_exact_1':ct(lambda x:x['road_0_1_2'][0]==1),'road0_at_most_1':ct(lambda x:x['road_0_1_2'][0]<=1),'only_0road_and_it_is_dog':ct(lambda x:x['road_0_1_2'][0]==1 and zmap[x['zero_road_numbers'][0]]=='狗'),'three_roads_all_present':ct(lambda x:all(x['road_0_1_2'])),'no_odd_2road':ct(lambda x:len(x['odd_2road_numbers'])==0),'two_even_2road_no_odd_2road':ct(lambda x:len(x['even_2road_numbers'])==2 and len(x['odd_2road_numbers'])==0),'odd3_even3':ct(lambda x:x['odd_even']==[3,3]),'distinct_exactly_5':ct(lambda x:x['distinct_zodiac_count']==5),'pattern_2_1_1_1_1':ct(lambda x:x['multiplicity_pattern']==[2,1,1,1,1]),'horse_at_least_two_balls':ct(lambda x:x['zodiac_ball_count'].get('馬',0)>=2),'both_snake_and_pig':ct(lambda x:{'蛇','豬'}<=set(x['zodiacs']))}
pre=[]
for n,z in zip(ns,nz):
 x=e['per_number'][str(n)];location='top' if z==d['top'] else 'A' if z==d['A'] else 'B' if z==d['B'] else 'C' if z==d['C'] else 'D' if z==d['D'] else 'reserve' if z in d['universe'] else 'outside_universe';pre.append({'number':n,'zodiac':z,'road':x['road'],'odd_even':x['odd_even'],'wave':x['wave'],'head':x['head'],'tail':x['tail'],'last_normal_age_before_314':x['last_normal_age'],'windows_before_314':x['window_counts'],'location':location})
# Frozen, pre-result alternatives are reviewed in their original order.
design=J(B/'314-31-handwritten-designs.json');audit=J(B/'314-candidates-audit.json');assert len(design['candidates'])==len(audit['candidates'])==31 and design['proposed_id']==chosen['human_choice']
cand=[];canonical=defaultdict(list)
for x,y in zip(design['candidates'],audit['candidates']):
 assert x['id']==y['id'] and x['roles']==y['roles'] and x['reserves']==y['reserves'];r=x['roles'];display=list(dict.fromkeys(r[k] for k in ('top','A','B','C','D')));dd={'universe':display+x['reserves'],**r};s=settle(dd);key=(r['top'],tuple(sorted([r['A'],r['B']],key=Z.index)),tuple(sorted([r['A'],r['C'],r['D']],key=Z.index)));canonical[key].append(x['id']);cand.append({'id':x['id'],'roles':r,'reserves':x['reserves'],'slots':s['slots'],'complete_count':s['complete_count'],'display_signs_hit':s['displayed_signs_hit'],'reserve_signs_hit':s['reserve_signs_hit'],'outside_universe_signs':s['outside_universe_signs'],'display_ball_count':s['display_ball_count'],'universe_ball_count':s['universe_ball_count'],'original_comparison':x['comparison']})
Acounts=Counter(x['roles']['A'] for x in cand);dist=Counter(x['complete_count'] for x in cand);dupes=[v for v in canonical.values() if len(v)>1];overlap=[x['id'] for x in cand if x['roles']['top'] in {x['roles'][k] for k in 'ABCD'}];assert Acounts['虎']==16 and len(Acounts)==12 and len(canonical)==30 and len(dupes)==1 and [s[:3] for s in dupes[0]]==['E01','E09'] and dist=={0:22,1:7,2:2} and [x[:3] for x in overlap]==['E22']
assert [x['id'][:3] for x in cand if x['complete_count']==2]==['E10','E11'];assert all(x['complete_count']==0 for x in cand if x['roles']['A']=='虎' and x['roles']['top']=='牛')
# Earlier frozen site versions, not a backtest or a rule ranking.
old=J(B/'313-retrospective-evidence.json');periods=[]
for x in old['prior_periods']:
 periods.append({'period':x['period'],'normal_zodiacs':x['normal_zodiacs'],'progress':[f"{len(s['present'])}/{len(s['required'])}" for s in x['slots']],'complete_count':x['complete_count'],'mode':x['mode']})
for p,source,settlekey in [(2026313,old['D2'],old['settlement_D2']),(2026314,d,settled)]:
 ss=settlekey['slots'];periods.append({'period':p,'normal_zodiacs':['狗','龍','狗','龍','鼠','豬'] if p==2026313 else nz,'progress':[f"{s['present_count']}/{s['needed_count']}" for s in ss],'complete_count':settlekey['complete_count'],'mode':'v5.0 nonofficial D2' if p==2026313 else 'v5.0 nonofficial 314'})
assert [x['complete_count'] for x in periods]==[0,1,1,2,0,1,0]
# Idealized model only: count complete columns via direct group-size enumeration.
shown=[d[k] for k in ('top','A','B','C','D')];sizes=[len(group[z]) for z in shown];other=49-sum(sizes);den=comb(49,6);distideal=[0,0,0,0];cols=[0,0,0];both=0
for counts in product(*(range(k+1) for k in sizes)):
 rem=6-sum(counts)
 if not 0<=rem<=other:continue
 ways=comb(other,rem)
 for size,count in zip(sizes,counts):ways*=comb(size,count)
 yes=[n>0 for n in counts];done=[yes[0],yes[1] and yes[2],yes[1] and yes[3] and yes[4]];distideal[sum(done)]+=ways
 for i,flag in enumerate(done):cols[i]+=ways*flag
 if done[1] and done[2]:both+=ways
assert sum(distideal)==den
ideal={'assumption':'49 equally likely distinct numbers, 6 sampled without replacement; an illustrative mathematical model only, not the actual unauthenticated draw mechanism','denominator':den,'display_group_sizes':sizes,'complete_column_count_combinations':distideal,'complete_column_count_percent':[100*x/den for x in distideal],'single_double_triple_percent':[100*x/den for x in cols],'double_and_triple_joint_percent':100*both/den,'common_tiger_absent_percent':100*comb(45,6)/den,'both_tiger_and_cow_absent_percent':100*comb(41,6)/den}
result={'scope':'User-supplied 314 retrospective only; period and 6+1 inferred, date unknown; no official authentication, no 315 choice or public website update','input':u,'published_choice':d,'actual_structure':m,'settlement':settled,'previous_input_identity':{'313_normal_distinct':order(prev6),'313_seven_distinct':order(prev7),'314_normal_distinct':order(actual),'314_seven_distinct':order(seven),'314seven_intersect_313seven':order(seven&prev7),'314normal_intersect_313seven':order(actual&prev7),'314normal_intersect_313normal':order(actual&prev6),'314seven_intersect_313seven_same_numbers':sorted(set(ns+[sp])&set(nums(rows[-1])+[int(rows[-1]['special'])]))},'each_actual_normal_ball_prior':pre,'pre_period_shape_windows':shape,'zodiac_prior':e['per_zodiac'],'number_prior':e['per_number'],'earlier_versions':periods,'frozen_31_candidate_review':{'count':31,'A_counts':dict(Acounts),'A_hit_candidates':sum(x['roles']['A'] in actual for x in cand),'A_absent_candidates':sum(x['roles']['A'] not in actual for x in cand),'unique_actual_column_structures':len(canonical),'duplicate_groups_excluding_reserve':dupes,'top_overlap_cases':overlap,'post_result_complete_count_distribution':dict(dist),'original_order_candidates':cand},'ideal_model_only':ideal}
write(O/'retrospective.json',result)
with (O/'prior_shape_windows.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['window']+list(shape['35']));w.writeheader()
 for k,v in shape.items():w.writerow({'window':k,**v})
with (O/'candidate_outcomes_original_order.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['candidate_id','single','double','triple','reserves','single_progress','double_progress','triple_progress','complete_columns','normal_display_balls','normal_universe_balls','normal_reserve_signs','normal_outside_universe_signs','note'])
 for x in cand:
  r=x['roles'];ss=x['slots'];w.writerow([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],' '.join(x['reserves'])]+[f"{s['present_count']}/{s['needed_count']}" for s in ss]+[x['complete_count'],x['display_ball_count'],x['universe_ball_count'],' '.join(x['reserve_signs_hit']),' '.join(x['outside_universe_signs']),'Post-result description only, not ranking or rule selection'])
with (O/'user_six_prior_ledger.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['number','zodiac','road','odd_even','wave','head','tail','prior_last_normal_age','W10','W20','W35','W40','W45','location'])
 for x in pre:w.writerow([f"{x['number']:02d}",x['zodiac'],x['road'],x['odd_even'],x['wave'],x['head'],x['tail'],x['last_normal_age_before_314']]+[x['windows_before_314'][str(k)] for k in (10,20,35,40,45)]+[x['location']])
print('USER INPUT 314, FROZEN PAGE SETTLEMENT AND 31 ORIGINAL CANDIDATES PASS; no main-history/site mutation')
print('Actual structure',json.dumps(m,ensure_ascii=False));print('Settled',json.dumps(settled,ensure_ascii=False));print('Candidate shared A',dict(Acounts),'canonical',len(canonical),'completed counts',dict(dist),'overlap',overlap);print('Prior shape windows',json.dumps({w:shape[w] for w in ('35','40','45')},ensure_ascii=False));print('Ideal model',json.dumps(ideal,ensure_ascii=False))
