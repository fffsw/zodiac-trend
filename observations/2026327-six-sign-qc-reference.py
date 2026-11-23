#!/usr/bin/env python3
"""Independently recount six-sign histories and cross-check exact ideal model with dynamic programming."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import date
from math import comb
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task292_327_release';O=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=J(O/'six_sign_repeat_study.json');checks=[]
def ck(v,msg):
 if not v:raise AssertionError(msg)
 checks.append(msg)
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
r=sorted(read(S/'data/macau_mark_six_full.csv'),key=lambda x:int(x['period']));raw=read(R/'data/task246_445_all_available_draws.csv');by={int(x['period']):x for x in raw};common=0
for x in r:
 p=int(x['period']);y=by.get(p)
 if y:
  assert [int(x[f'n{i}']) for i in range(1,7)]+[int(x['special'])]==list(map(int,y['numbers'].split())) and [x[f'z{i}'] for i in range(1,7)]+[x['special_zodiac']]==y['zodiacs'].split();common+=1
ck(common==1042 and len(r)==1057 and int(r[-1]['period'])==2026326 and H(S/'data/macau_mark_six_full.csv')==d['input_history_sha256'],'1042 earlier records agree with longer frozen source; remaining recent user history and 326 treated as unverified user source')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');normalize=lambda xs:' '.join(z for z in Z if z in xs);seen=[]
for a,b in zip(r,r[1:]):
 p,q=int(a['period']),int(b['period']);same=p//1000==q//1000 and p+1==q
 if p//1000!=q//1000:
  try:same=q//1000==p//1000+1 and q%1000==1 and (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days==1
  except ValueError:same=False
 if not same:continue
 if len({int(a[f'n{i}']) for i in range(1,7)}|{int(a['special'])})!=7 or len({int(b[f'n{i}']) for i in range(1,7)}|{int(b['special'])})!=7:continue
 a6={a[f'z{i}'] for i in range(1,7)};a7=a6|{a['special_zodiac']};b6={b[f'z{i}'] for i in range(1,7)};b7=b6|{b['special_zodiac']}
 if len(a6)==len(a7)==6:seen.append((p,q,normalize(a6),normalize(a7),normalize(b6),normalize(b7),normalize(a6&b6),len(a6&b6),normalize(a7&b7),len(a7&b7)))
record=read(O/'six_sign_repeat_pairs.csv');assert len(seen)==len(record)==131
for x,y in zip(seen,record):assert x==(int(y['previous']),int(y['next']),y['prev6'],y['prev7'],y['next6'],y['next7'],y['repeat6'],int(y['repeat6_count']),y['repeat7'],int(y['repeat7_count']))
for year in ('2024plus','2024','2025','2026'):
 xs=seen if year=='2024plus' else [x for x in seen if x[0]//1000==int(year)];v=d['groups'][year];assert v['n']==len(xs) and v['six_to_six_counts_0_to_6']==[sum(x[7]==i for x in xs) for i in range(7)] and v['seven_to_seven_counts_0_to_6']==[sum(x[9]==i for x in xs) for i in range(7)]
ck(True,'all 131 adjacent followups and each year distribution independently recomputed using archived zodiac labels, not 2026 mapping')
for draw in (6,7):
 dp={(0,0):1}
 for size,prior in [(4,True)]*6+[(25,False)]:
  nd=defaultdict(int)
  for (balls,k),ways in dp.items():
   for take in range(min(size,draw-balls)+1):nd[(balls+take,k+int(prior and take>0))]+=ways*comb(size,take)
  dp=nd
 counts=[dp.get((draw,i),0) for i in range(7)];v=d['uniform_49_independent_model'][str(draw)];assert counts==v['counts_0_to_6'] and sum(counts)==v['denominator']==comb(49,draw)
ck(True,'separate generating-function recurrence reproduces six- and seven-ball ideal counts and denominators')
current={r[-1][f'z{i}'] for i in range(1,7)};assert len(current)==6 and current|{r[-1]['special_zodiac']}==current and d['current_pending']['included_in_followup_denominators'] is False and d['current_pending']['target_result_read'] is False and all(x[1]<=2026326 for x in seen)
for key,n in [('witness_six_repeat_6_not_327',6),('witness_six_repeat_0_not_327',0)]:
 ws=d[key];assert len(ws)==len({x['number'] for x in ws})==6 and all(Z[(7-x['number'])%12]==x['zodiac'] for x in ws) and len(current&{x['zodiac'] for x in ws})==n
ck(True,'326 pending six-sign trigger and illustrative repeat-0/repeat-6 examples; neither is 327')
out={'status':'PASS','scope':'independent historical and mathematical recount only; no official, future outcome or predraw authentication','checks':checks,'study_sha256':H(O/'six_sign_repeat_study.json'),'pairs_sha256':H(O/'six_sign_repeat_pairs.csv')};p=O/'six_sign_repeat_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
