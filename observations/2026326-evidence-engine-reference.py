#!/usr/bin/env python3
"""First-six descriptive windows, joint absences and age blocks through the immediately prior user issue.
For 326, inputs end with user 325; no 326 result is queried or added.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import csv,json,hashlib,sys
R=Path('/home/user');target=int(sys.argv[1]);assert target==2026326;A=R/'archive/task289_326_release';S=A/'stage';O=A/'analysis'
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
rows=sorted(C(S/'data/macau_mark_six_full.csv'),key=lambda r:int(r['period']));assert len(rows)==1049+(target-2026319) and int(rows[-1]['period'])==target-1 and rows[-1]['date']==''
u=json.loads((R/'archive/task288_325_review/input/user-325.json').read_text());Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z={n:Z[(7-n)%12] for n in range(1,50)};red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠';nums=lambda r:[int(r[f'n{i}']) for i in range(1,7)];zs=lambda r:[r[f'z{i}'] for i in range(1,7)]
assert nums(rows[-1])+[int(rows[-1]['special'])]==u['normal_numbers']+[u['seventh_number']] and zs(rows[-1])==u['normal_zodiacs'] and rows[-1]['special_zodiac']==u['seventh_zodiac']
for r in rows[-250:]:assert [n2z[n] for n in nums(r)]==zs(r) and n2z[int(r['special'])]==r['special_zodiac'] and len(set(nums(r)+[int(r['special'])]))==7
W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));rev=rows[::-1];seven=lambda r:set(zs(r))|{r['special_zodiac']};pairkey=lambda a,b:'|'.join(sorted([a,b],key=Z.index));perz={};pernum={}
for z in Z:
 windows={};age={}
 for w in W:
  x=rows[-w:];windows[str(w)]={'balls':sum(zs(r).count(z) for r in x),'periods':sum(z in zs(r) for r in x)}
 for a,b in blocks:
  x=rev[a:b+1];age[f'{a}-{b}']={'balls':sum(zs(r).count(z) for r in x),'periods':sum(z in zs(r) for r in x)}
 perz[z]={'numbers':[n for n in range(1,50) if n2z[n]==z],'windows':windows,'disjoint_age_blocks':age,'last_normal_age':next(i for i,r in enumerate(rev) if z in zs(r)),'previous_six_identity':z in zs(rows[-1])}
for n in range(1,50):
 pernum[str(n)]={'zodiac':n2z[n],'road':n%3,'odd_even':'奇' if n%2 else '偶','wave':wave(n),'head':n//10,'tail':n%10,'last_normal_age':next(i for i,r in enumerate(rev) if n in nums(r)),'window_counts':{str(w):sum(n in nums(r) for r in rows[-w:]) for w in W}}
struct={};joint={};peer={}
for w in W:
 rs=rows[-w:];ball=[v for r in rs for v in nums(r)];roads=[Counter(v%3 for v in nums(r)) for r in rs];mult=[Counter(zs(r)) for r in rs];sets=[set(zs(r)) for r in rs]
 s={'first_period':int(rs[0]['period']),'last_period':target-1,'road_ball_counts':[sum(x%3==k for x in ball) for k in range(3)],'odd_even_ball_counts':[sum(x%2 for x in ball),sum(x%2==0 for x in ball)],'red_blue_green_ball_counts':[sum(wave(x)==c for x in ball) for c in ('紅','藍','綠')],'small_big_1_24_25_49':[sum(x<=24 for x in ball),sum(x>=25 for x in ball)],'head_ball_counts':[sum(x//10==k for x in ball) for k in range(5)],'tail_ball_counts':[sum(x%10==k for x in ball) for k in range(10)],'at_most_one_odd_periods':sum(sum(v%2==1 for v in nums(r))<=1 for r in rs),'at_most_two_odd_periods':sum(sum(v%2==1 for v in nums(r))<=2 for r in rs),'at_most_one_even_periods':sum(sum(v%2==0 for v in nums(r))<=1 for r in rs),'at_most_two_even_periods':sum(sum(v%2==0 for v in nums(r))<=2 for r in rs),'no_red_periods':sum(not any(wave(v)=='紅' for v in nums(r)) for r in rs),'at_least_four_green_periods':sum(sum(wave(v)=='綠' for v in nums(r))>=4 for r in rs),'distinct4_or_fewer_periods':sum(len(c)<=4 for c in mult),'three_roads_present_periods':sum(all(c[k]>0 for k in range(3)) for c in roads),'exact_road_2_4_0_periods':sum([c[k] for k in range(3)]==[2,4,0] for c in roads)}
 for k in range(3):
  s[f'no_{k}road_periods']=sum(c[k]==0 for c in roads);s[f'at_most_one_{k}road_periods']=sum(c[k]<=1 for c in roads);s[f'at_least_four_{k}road_periods']=sum(c[k]>=4 for c in roads)
  for parity in ('odd','even'):s[f'no_{parity}_{k}road_periods']=sum(not any(n%3==k and n%2==(parity=='odd') for n in nums(r)) for r in rs)
 for z in Z:s['no_'+z+'_periods']=sum(z not in x for x in sets)
 struct[str(w)]=s;joint[str(w)]={pairkey(a,b):sum(a not in x and b not in x for x in sets) for a,b in combinations(Z,2)};peer[str(w)]={}
 for z in Z:
  group=[n for n in range(1,50) if n2z[n]==z];other=[q for q in Z if q!=z and next(n for n in range(1,50) if n2z[n]==q)%6==group[0]%6];assert len(other)==1
  peer[str(w)][z]={'peer':other[0],'target_absent_peer_present_periods':sum(z not in x and other[0] in x for x in sets)}
base={int(r['period']):r for r in rows};rep={str(p):{'seven_v_seven_count':len(seven(base[p])&seven(base[p-1])),'seven_v_seven_signs':sorted(seven(base[p])&seven(base[p-1]),key=Z.index),'current_six_vs_previous_seven_count':len(set(zs(base[p]))&seven(base[p-1])),'current_six_vs_previous_six_count':len(set(zs(base[p]))&set(zs(base[p-1])))} for p in range(2026309,target)}
full={'status':'DESCRIPTIVE_INPUT_ONLY_NOT_A_FORECAST','scope':f'only user numbers through {target-1}; selection ledgers use first six; seventh only raw history and seven-ball identity. 326 result was not looked up, but source timing and pre-draw status are not authenticated.','history_sha256':hashlib.sha256((S/'data/macau_mark_six_full.csv').read_bytes()).hexdigest(),'history_rows':len(rows),'latest_period':target-1,'latest_date':None,'target_result_was_already_provided':False,'primary_windows':[35,40,45],'windows_overlap_not_independent_votes':True,'blocks':[list(x) for x in blocks],'per_zodiac':perz,'per_number':pernum,'structural_windows':struct,'joint_zodiac_absence_periods':joint,'same_route_parity_peer_present_target_absent_periods':peer,'adjacent_identity_repeats':rep,'recent_45_normal_records':[{'period':int(r['period']),'numbers':nums(r),'zodiacs':zs(r)} for r in rows[-45:]]}
p=O/'evidence.json';assert not p.exists();p.write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n')
with (O/'zodiac_ledger.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['zodiac','numbers']+[f'W{k}_balls_periods' for k in (10,20,35,40,45)]+['age0_9','age10_19','age20_34','age35_39','age40_44','last_age','last_six_identity'])
 for z in Z:
  x=perz[z];fm=lambda v:f"{v['balls']}/{v['periods']}";w.writerow([z,' '.join(f'{n:02d}' for n in x['numbers'])]+[fm(x['windows'][str(i)]) for i in (10,20,35,40,45)]+[fm(x['disjoint_age_blocks'][f'{a}-{b}']) for a,b in blocks]+[x['last_normal_age'],x['previous_six_identity']])
with (O/'number_ledger.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['number','zodiac','road','odd_even','wave','head','tail','last_age']+[f'W{k}' for k in W])
 for n in range(1,50):
  x=pernum[str(n)];w.writerow([f'{n:02d}',x['zodiac'],x['road'],x['odd_even'],x['wave'],x['head'],x['tail'],x['last_normal_age']]+[x['window_counts'][str(k)] for k in W])
with (O/'joint_absence_ledger.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['sign_one','sign_two','W35_both_absent','W40_both_absent','W45_both_absent','note'])
 for a,b in combinations(Z,2):w.writerow([a,b]+[joint[str(k)][pairkey(a,b)] for k in (35,40,45)]+['first six only; overlapping windows; descriptive, not forecast or rank'])
print(f'PASS target {target}: {len(rows)} prior rows; 12/49 ledgers, 66 joint absences, eight windows, five disjoint age blocks; not a prediction')
for z in Z:
 x=perz[z];print(z,'nums',','.join(f'{n:02d}' for n in x['numbers']),'age',x['last_normal_age'],'W35/40/45',[(x['windows'][str(k)]['periods'],x['windows'][str(k)]['balls']) for k in (35,40,45)],'disjoint',[(x['disjoint_age_blocks'][f'{a}-{b}']['periods'],x['disjoint_age_blocks'][f'{a}-{b}']['balls']) for a,b in blocks],'peer',peer['35'][z])
for w in (35,40,45):print('struct',w,{k:v for k,v in struct[str(w)].items() if k in ('no_0road_periods','no_1road_periods','no_2road_periods','no_odd_0road_periods','no_even_0road_periods','no_odd_1road_periods','no_even_1road_periods','no_odd_2road_periods','no_even_2road_periods','exact_road_2_4_0_periods','three_roads_present_periods')})
