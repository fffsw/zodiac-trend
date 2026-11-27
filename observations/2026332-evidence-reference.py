#!/usr/bin/env python3
"""Descriptive evidence through user-confirmed 331, never querying target 332."""
from pathlib import Path
from datetime import date
from itertools import combinations,product
from math import comb
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task305_331_review_332';S=A/'stage';Q=A/'analysis';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads(p.read_text());assert J(Q/'retrospective.json')['status']=='PASS_USER_CONFIRMED_REVIEW_NOT_OFFICIAL_OR_PREDRAW_AUTHENTICATION' and J(Q/'user_331_stage.json')['six_plus_one_explicitly_confirmed_by_user'] and not (Q/'evidence.json').exists()
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda x:int(x['period']))
assert len(rows)==1062 and int(rows[0]['period'])==2024001 and int(rows[-1]['period'])==2026331 and rows[-1]['date']=='' and not any(int(x['period'])>2026331 for x in rows)
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if n2z(n)==z] for z in Z};order=lambda v:[z for z in Z if z in v];nums=lambda r:[int(r[f'n{i}']) for i in range(1,7)];zs=lambda r:[r[f'z{i}'] for i in range(1,7)];sevenz=lambda r:set(zs(r))|{r['special_zodiac']};sevenn=lambda r:nums(r)+[int(r['special'])]
for r in rows[-250:]:assert [n2z(n) for n in nums(r)]==zs(r) and n2z(int(r['special']))==r['special_zodiac'] and len(set(sevenn(r)))==7
windows=(10,20,35,40,45,60,100,250);perz={};pern={};joint={};structure={}
for z in Z:
 perz[z]={'numbers':G[z],'windows':{str(w):{'balls':sum(zs(r).count(z) for r in rows[-w:]),'periods':sum(z in zs(r) for r in rows[-w:])} for w in windows},'last_normal_age':next(i for i,r in enumerate(reversed(rows)) if z in zs(r)),'in_331_six':z in zs(rows[-1]),'in_331_seven':z in sevenz(rows[-1])}
for n in range(1,50):pern[str(n)]={'zodiac':n2z(n),'road':n%3,'odd_even':'odd' if n%2 else 'even','last_normal_age':next(i for i,r in enumerate(reversed(rows)) if n in nums(r)),'windows':{str(w):sum(n in nums(r) for r in rows[-w:]) for w in windows}}
for w in windows:
 rr=rows[-w:];ss=[set(zs(r)) for r in rr];joint[str(w)]={'|'.join(order({a,b})):sum(not ({a,b}&x) for x in ss) for a,b in combinations(Z,2)};structure[str(w)]={'first_period':int(rr[0]['period']),'last_period':2026331,'road_ball_counts':[sum(n%3==k for r in rr for n in nums(r)) for k in range(3)],'odd_even_ball_counts':[sum(n%2==k for r in rr for n in nums(r)) for k in (1,0)],'five_distinct_or_fewer_periods':sum(len(x)<=5 for x in ss),'three_roads_present':sum(all(any(n%3==k for n in nums(r)) for k in range(3)) for r in rr),'no_2road_periods':sum(not any(n%3==2 for n in nums(r)) for r in rr),'at_most_two_odd_periods':sum(sum(n%2==1 for n in nums(r))<=2 for r in rr),'at_most_one_even_periods':sum(sum(n%2==0 for n in nums(r))<=1 for r in rr),'at_most_one_road_periods':[sum(sum(n%3==k for n in nums(r))<=1 for r in rr) for k in range(3)]}
e={'status':'DESCRIPTIVE_INPUT_ONLY_NOT_A_FORECAST','scope':'Through user-confirmed 331 only; 331 first six/seventh user confirmed, 330 and 329 partitions inferred. Overlapping windows not independent tests. Official source, dates, mechanism, mapping and pre-draw timing unverified.','history_sha256':H(S/'data/macau_mark_six_full.csv'),'history_rows':len(rows),'latest_period':2026331,'latest_date':None,'target_332_result_queried_or_used':False,'windows':list(windows),'per_zodiac':perz,'per_number':pern,'structural_windows':structure,'joint_zodiac_absence_periods':joint,'recent_45_normal_records':[{'period':int(r['period']),'numbers':nums(r),'zodiacs':zs(r)} for r in rows[-45:]]};(Q/'evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
with (Q/'zodiac_ledger.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['zodiac','numbers']+[f'W{k}_balls_periods' for k in windows]+['last_normal_age','in_331_six','in_331_seven'])
 for z in Z:
  x=perz[z];w.writerow([z,' '.join(f'{n:02d}' for n in G[z])]+[f"{x['windows'][str(k)]['balls']}/{x['windows'][str(k)]['periods']}" for k in windows]+[x['last_normal_age'],x['in_331_six'],x['in_331_seven']])
with (Q/'number_ledger.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['number','zodiac','road','odd_even','last_normal_age']+[f'W{k}' for k in windows])
 for n in range(1,50):
  x=pern[str(n)];w.writerow([f'{n:02d}',x['zodiac'],x['road'],x['odd_even'],x['last_normal_age']]+[x['windows'][str(k)] for k in windows])
era=lambda p:3 if p<=2024040 else 4 if p<=2025028 else 5 if p<=2026047 else 6
def adjacent(a,b):
 p,q=int(a['period']),int(b['period'])
 if p//1000==q//1000:return q==p+1
 if q//1000==p//1000+1 and q%1000==1:
  try:return (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days==1
  except ValueError:return False
 return False
pairs=[];excluded=[]
for a,b in zip(rows,rows[1:]):
 pa,pb=int(a['period']),int(b['period']);reason=[]
 if not adjacent(a,b):reason.append('nonadjacent_or_unknown_date_across_year')
 if len(set(sevenn(a)))!=7 or len(set(sevenn(b)))!=7:reason.append('invalid_duplicate_numbers')
 if era(pa)!=era(pb):reason.append('cross_zodiac_mapping_era')
 if reason:excluded.append({'previous':pa,'next':pb,'reasons':reason});continue
 a6=set(zs(a));a7=sevenz(a);b6=set(zs(b));b7=sevenz(b)
 if len(a6) in (5,6):pairs.append({'previous':pa,'next':pb,'prev6_distinct':len(a6),'prev7_distinct':len(a7),'prev6':order(a6),'prev7':order(a7),'next6':order(b6),'next7':order(b7),'repeat6':order(a6&b6),'repeat7':order(a7&b7),'repeat6_count':len(a6&b6),'repeat7_count':len(a7&b7),'source':'stored historical labels; not externally authenticated'})
assert [(x['previous'],x['next']) for x in excluded]==[(2024040,2024041),(2025028,2025029),(2026047,2026048)] and len(pairs)==837
groups={}
for n,k in ((5,5),(5,6),(6,6),(6,7)):
 xs=[x for x in pairs if x['prev6_distinct']==n and x['prev7_distinct']==k];groups[f'previous_six_{n}_seven_{k}']={'n':len(xs),'six_to_six_counts_0_to_'+str(n):[sum(x['repeat6_count']==i for x in xs) for i in range(n+1)],'seven_to_seven_counts_0_to_'+str(k):[sum(x['repeat7_count']==i for x in xs) for i in range(k+1)]}
assert groups['previous_six_5_seven_6']=={'n':346,'six_to_six_counts_0_to_5':[8,70,141,107,20,0],'seven_to_seven_counts_0_to_6':[0,23,84,154,73,12,0]} and groups['previous_six_5_seven_5']['n']==227 and groups['previous_six_6_seven_6']['n']==133 and groups['previous_six_6_seven_7']['n']==131
assert pairs[-1]['previous']==2026330 and pairs[-1]['next']==2026331 and pairs[-1]['repeat6_count']==2 and pairs[-1]['repeat7_count']==4
a6=set(zs(rows[-1]));a7=sevenz(rows[-1]);assert a6=={'龍','牛','猴','兔','蛇'} and a7==a6|{'馬'} and len(a6)==5 and len(a7)==6
model={}
for typ,ids,draw in [('six_to_six',order(a6),6),('seven_to_seven',order(a7),7)]:
 sizes=[len(G[z]) for z in ids];assert all(x in (4,5) for x in sizes) and (sizes.count(5)==0 if typ=='six_to_six' else sizes.count(5)==1);other=49-sum(sizes);cnt=[0]*(len(ids)+1)
 for ks in product(*(range(s+1) for s in sizes)):
  rest=draw-sum(ks)
  if 0<=rest<=other:
   ways=comb(other,rest)
   for size,k in zip(sizes,ks):ways*=comb(size,k)
   cnt[sum(k>0 for k in ks)]+=ways
 den=comb(49,draw);assert sum(cnt)==den;model[typ]={'previous_identities':ids,'sizes':sizes,'draw_count':draw,'denominator':den,'counts':cnt,'percent':[100*x/den for x in cnt]}
study={'status':'PASS_DESCRIPTIVE_EXPLORATORY_NOT_FORECAST','scope':'331 has five distinct confirmed normal identities (dragon repeated) and six distinct seven-ball identities. Historical 5/6 cohort matches this structure; other cohorts separate. 330/329 partition inferred; official source, date and target timing unverified. Era boundaries excluded.','input_history_sha256':H(S/'data/macau_mark_six_full.csv'),'historical_records':len(rows),'excluded_pairs':excluded,'groups':groups,'current_pending':{'previous_issue':2026331,'previous_six':order(a6),'previous_seven':order(a7),'target_issue':2026332,'target_result_queried_or_used':False,'included_in_followup_denominators':False},'uniform_49_independent_model':model,'limitations':'The cohort was selected after observing 331; consecutive observations overlap and data provenance is unauthenticated, so no next-period probability can be inferred from empirical shares. Seven-to-seven includes the seventh ball, never normal-column settlement. The 331 normal five are all four-code; horse with five codes is present only in the seven-ball set. Equal-probability model is an assumption, not real-world proof.'};(Q/'six_sign_repeat_study.json').write_text(json.dumps(study,ensure_ascii=False,indent=2)+'\n')
with (Q/'six_sign_repeat_pairs.csv').open('x',encoding='utf8',newline='') as f:
 cols=['previous','next','prev6_distinct','prev7_distinct','prev6','prev7','next6','next7','repeat6','repeat6_count','repeat7','repeat7_count','source'];w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
 for x in pairs:w.writerow({k:' '.join(v) if isinstance(v,list) else v for k,v in x.items()})
print(json.dumps({'status':study['status'],'groups':groups,'current_pending':study['current_pending'],'model_six_sizes':model['six_to_six']['sizes'],'model_six_repeat_percent':[round(x,4) for x in model['six_to_six']['percent']]},ensure_ascii=False,indent=2))
