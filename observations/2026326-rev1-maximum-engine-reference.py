#!/usr/bin/env python3
"""Post-clarification exploratory maxima/count distributions from frozen historical raw rows; no target data."""
from pathlib import Path
from collections import Counter
from datetime import date
from itertools import combinations
from math import comb
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task290_326_revision';B=A/'before';O=A/'analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert J(O/'freeze_receipt.json')['status']=='PASS' and not (O/'maximum_study.json').exists()
def C(p):
 with p.open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
raw=C(B/'445-source-through-311.csv');hist=C(B/'history-through-325.csv');u=J(B/'325-user-result.json');assert len(raw)==2492 and len(hist)==1056 and hist[0]['period']=='2026325' and not any(int(x['period'])>=2026326 for x in hist)
old={int(x['period']):x for x in raw};matches=0
for x in hist:
 y=old.get(int(x['period']))
 if y:
  assert [int(x[f'n{i}']) for i in range(1,7)]+[int(x['special'])]==list(map(int,y['numbers'].split())) and [x[f'z{i}'] for i in range(1,7)]+[x['special_zodiac']]==y['zodiacs'].split();matches+=1
assert matches==1042
records=[{'period':int(x['period']),'date':x['date'],'numbers':list(map(int,x['numbers'].split())),'z':x['zodiacs'].split(),'valid':x['usable']=='1','source':x['source']} for x in raw]
for x in reversed(hist):
 p=int(x['period'])
 if 2026312<=p<=2026325:records.append({'period':p,'date':x['date'],'numbers':[int(x[f'n{i}']) for i in range(1,7)]+[int(x['special'])],'z':[x[f'z{i}'] for i in range(1,7)]+[x['special_zodiac']],'valid':True,'source':'user-supplied history'})
assert len(records)==2506 and records[-1]['period']==2026325 and records[-1]['numbers']==u['normal_numbers']+[u['seventh_number']]
def adj(a,b):
 p,q=a['period'],b['period']
 if p//1000==q//1000:return q%1000==p%1000+1
 if q//1000==p//1000+1 and q%1000==1:
  try:return (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days==1
  except ValueError:return False
 return False
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');order=lambda xs:sorted(set(xs),key=Z.index);pairs=[];excluded=[]
for a,b in zip(records,records[1:]):
 if not a['valid'] or not b['valid'] or not adj(a,b):excluded.append([a['period'],b['period']]);continue
 p6,p7,n6,n7=set(a['z'][:6]),set(a['z']),set(b['z'][:6]),set(b['z']);pairs.append({'previous':a['period'],'next':b['period'],'p6':order(p6),'p7':order(p7),'n6':order(n6),'n7':order(n7),'repeat6':order(p6&n6),'repeat7':order(p7&n7),'p6_shape':sorted(Counter(a['z'][:6]).values(),reverse=True),'p7_shape':sorted(Counter(a['z']).values(),reverse=True),'previous_numbers':a['numbers'],'next_numbers':b['numbers']})
assert len(pairs)==2501 and len(excluded)==4 and max(x['next'] for x in pairs)==2026325

def dist(arr,key):
 c=Counter(len(x[key]) for x in arr);n=len(arr);m=max(c) if n else None;return {'n':n,'counts_0_to_4':[c[i] for i in range(5)],'maximum_observed':m,'maximum_observed_count':c[m] if n else 0,'max_example_pairs':[{'previous':x['previous'],'next':x['next'],'previous_six':x['p6'],'previous_seven':x['p7'],'next_six':x['n6'],'next_seven':x['n7'],'repeated':x[key],'previous_numbers':x['previous_numbers'],'next_numbers':x['next_numbers']} for x in arr if len(x[key])==m]}
def pack(arr):return {'next_six_repeat':dist(arr,'repeat6'),'next_seven_repeat':dist(arr,'repeat7')}
sel2024=[x for x in pairs if x['previous']>=2024001];both=lambda xs:[x for x in xs if len(x['p6'])==len(x['p7'])==4]
G={'both_four_2024plus':pack(both(sel2024)),'both_four_2020plus':pack(both(pairs)),'both_four_2026':pack(both([x for x in pairs if x['previous']//1000==2026])),'both_four_shape_325_2024plus':pack([x for x in both(sel2024) if x['p6_shape']==[2,2,1,1] and x['p7_shape']==[2,2,2,1]])}
# Broader previous-six-four condition: seven-ball set may contain a fifth sign.
normal=[x for x in sel2024 if len(x['p6'])==4];G['only_six_four_2024plus']={'next_six_repeat':dist(normal,'repeat6')}
seven=[x for x in sel2024 if len(x['p7'])==4]
# Trigger p7=4 may have p6=3; current 325 has same four in both sets.
G['only_seven_four_2024plus']={'n':len(seven),'next_six_repeat_from_previous_seven':{'counts_0_to_4':[sum(len(set(x['p7'])&set(x['n6']))==i for x in seven) for i in range(5)]},'next_seven_repeat':dist(seven,'repeat7')}
for k,expected in [('both_four_2024plus',([5,18,17,8,0],[5,13,19,9,2])),('both_four_2020plus',([8,47,46,12,0],[7,35,51,18,2])),('both_four_2026',([3,5,3,2,0],[3,4,3,2,1])),('both_four_shape_325_2024plus',([3,10,12,6,0],[3,7,13,6,2]))]:assert (G[k]['next_six_repeat']['counts_0_to_4'],G[k]['next_seven_repeat']['counts_0_to_4'])==expected
assert G['only_six_four_2024plus']['next_six_repeat']['counts_0_to_4']==[18,65,80,33,5] and G['only_seven_four_2024plus']['next_six_repeat_from_previous_seven']['counts_0_to_4']==[6,25,24,12,0]
post2024=[x for x in records if x['valid'] and x['period']>=2024001];distinct={}
for n in (6,7):
 c=Counter(len(set(x['z'][:n])) for x in post2024);minn=min(c);distinct[str(n)]={'n':len(post2024),'counts':dict(sorted(c.items())),'observed_minimum':minn,'example':next({'period':x['period'],'numbers':x['numbers'],'zodiacs':x['z']} for x in post2024 if len(set(x['z'][:n]))==minn)}
assert distinct['6']['observed_minimum']==distinct['7']['observed_minimum']==3
prev=set(records[-1]['z'][:6]);assert prev==set(records[-1]['z'])=={'虎','馬','鷄','龍'};witness=[5,13,10,27,6,2];n2z=lambda n:Z[(7-n)%12];assert len(set(witness))==6 and len(prev&{n2z(n) for n in witness})==4
result={'status':'PASS_DESCRIPTIVE_EXPLORATORY_NOT_FORECAST','clarified_target':'325前六与七球去重都只有虎馬鷄龍四个不同生肖，不是324至325重四','records':len(records),'valid_adjacent_pairs':len(pairs),'excluded_pairs':excluded,'target_326_outcome_read':False,'pending_current_excluded_from_denominators':True,'previous_set':order(prev),'theoretical_maximum_repeat_six':4,'theoretical_maximum_repeat_seven':4,'constructive_six_number_counterexample_not_real_326':witness,'historical_groups':G,'distinct_counts_2024plus':distinct,'limitations':'All grouped analyses after clarification are exploratory. Historical records are not officially authenticated; 2020 early data is partly single-source. Year-specific historical zodiac identities used, invalid/nonadjacent rows excluded; rolling cohorts overlap. Zero observed maximum does not prove impossible; finite descriptive maximum does not bound the next draw.'}
(O/'maximum_study.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');
with (O/'maximum_pairs.csv').open('x',encoding='utf8',newline='') as f:
 field=['previous','next','prev6','prev7','next6','next7','repeat6','repeat6_count','repeat7','repeat7_count','prior6_shape','prior7_shape','both_four','year_2024plus'];w=csv.DictWriter(f,fieldnames=field);w.writeheader()
 for x in pairs:
  if len(x['p6'])==4 or len(x['p7'])==4:w.writerow({'previous':x['previous'],'next':x['next'],'prev6':' '.join(x['p6']),'prev7':' '.join(x['p7']),'next6':' '.join(x['n6']),'next7':' '.join(x['n7']),'repeat6':' '.join(x['repeat6']),'repeat6_count':len(x['repeat6']),'repeat7':' '.join(x['repeat7']),'repeat7_count':len(x['repeat7']),'prior6_shape':' '.join(map(str,x['p6_shape'])),'prior7_shape':' '.join(map(str,x['p7_shape'])),'both_four':int(len(x['p6'])==len(x['p7'])==4),'year_2024plus':int(x['previous']>=2024001)})
print(json.dumps({'status':result['status'],'records':len(records),'valid_pairs':len(pairs),'groups':{k:{s:{x:y for x,y in v.items() if x!='max_example_pairs'} if isinstance(v,dict) else v for s,v in g.items()} for k,g in G.items()},'minimum_2024plus':distinct,'theoretical_max':4,'max_six_repeat_counterexample_not_real_326':witness},ensure_ascii=False,indent=2))
