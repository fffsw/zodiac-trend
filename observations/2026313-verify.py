#!/usr/bin/env python3
"""Portable arithmetic/structure verifier for the nonofficial 313 display.

Run in any directory containing the 2026313-* package: python3 2026313-verify.py
Needs only Python's standard library. It verifies consistency, not the truth,
source independence, fairness, official status, or time of any observation.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
from math import comb
import csv,hashlib,json,re
P=Path(__file__).resolve().parent
J=lambda name:json.loads((P/name).read_text(encoding='utf-8'))
def C(name):
 with (P/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def check(x,msg):
 if not x:raise AssertionError(msg)
 print('PASS',msg)
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬')
S={'鼠':{7,19,31,43},'牛':{6,18,30,42},'虎':{5,17,29,41},'兔':{4,16,28,40},'龍':{3,15,27,39},'蛇':{2,14,26,38},'馬':{1,13,25,37,49},'羊':{12,24,36,48},'猴':{11,23,35,47},'鷄':{10,22,34,46},'狗':{9,21,33,45},'豬':{8,20,32,44}}
R={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};B={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};G=set(range(1,50))-R-B
hist=sorted(C('2026313-source-data.csv'),key=lambda r:int(r['period']));u=J('2026313-user-input.json')
ns=lambda r:[int(r[f'n{i}']) for i in range(1,7)];zs=lambda r:[r[f'z{i}'] for i in range(1,7)]
check(len(hist)==1043 and int(hist[-1]['period'])==2026312 and ns(hist[-1])+[int(hist[-1]['special'])]==[31,46,4,43,32,15,38] and u['normal_numbers']+[u['seventh_number']]==[31,46,4,43,32,15,38],'1043 records and user-confirmed 312')
check(all(len(set(ns(r)+[int(r['special'])]))==7 and all(1<=x<=49 for x in ns(r)+[int(r['special'])]) for r in hist),'all stored numbers in range and no duplicates within a record')
zled={r['zodiac']:r for r in C('2026313-zodiac-ledger.csv')};nled={int(r['number']):r for r in C('2026313-number-ledger.csv')}
check(set(zled)==set(Z) and set(nled)==set(range(1,50)),'12 zodiacs and 49 numbers')
for w in (10,20,35,40,45,60,100,250):
 sample=hist[-w:];zc=Counter(z for r in sample for z in zs(r));zp=Counter(z for r in sample for z in set(zs(r)));nc=Counter(n for r in sample for n in ns(r))
 for z in Z:assert (int(zled[z][f'W{w}_balls']),int(zled[z][f'W{w}_periods']))==(zc[z],zp[z])
 for n in nled:assert int(nled[n][f'W{w}'])==nc[n]
for a,b in ((0,9),(10,19),(20,34),(35,39),(40,44)):
 sample=list(reversed(hist))[a:b+1];zc=Counter(z for r in sample for z in zs(r));zp=Counter(z for r in sample for z in set(zs(r)))
 for z in Z:assert (int(zled[z][f'age{a}_{b}_balls']),int(zled[z][f'age{a}_{b}_periods']))==(zc[z],zp[z])
for n,r in nled.items():
 assert r['zodiac']==next(z for z in Z if n in S[z]) and int(r['road'])==n%3 and int(r['head'])==n//10 and int(r['tail'])==n%10
 assert r['wave']==('紅' if n in R else '藍' if n in B else '綠') and int(r['last_flat_age'])==next(i for i,x in enumerate(reversed(hist)) if n in ns(x))
check(True,'8 windows, 5 age blocks, 12/49 ledgers and number attributes')
fmt=lambda v:'/'.join(map(str,v))
for r in C('2026313-structure-windows.csv'):
 w=int(r['window']);sample=hist[-w:];v=[n for x in sample for n in ns(x)];roads=[{n%3 for n in ns(x)} for x in sample]
 assert r['road_0_1_2']==fmt([sum(n%3==k for n in v) for k in range(3)])
 assert r['odd_even']==fmt([sum(n%2==1 for n in v),sum(n%2==0 for n in v)])
 assert r['red_blue_green']==fmt([sum(n in col for n in v) for col in (R,B,G)])
 assert r['small_big']==fmt([sum(n<=24 for n in v),sum(n>=25 for n in v)])
 assert r['heads_0_to_4']==fmt([sum(n//10==k for n in v) for k in range(5)])
 assert r['tails_0_to_9']==fmt([sum(n%10==k for n in v) for k in range(10)])
 assert int(r['no_0road_periods'])==sum(0 not in x for x in roads)
 assert int(r['three_roads_present_periods'])==sum(len(x)==3 for x in roads)
 assert int(r['at_least_two_2road_periods'])==sum(sum(n%3==2 for n in ns(x))>=2 for x in sample)
check(True,'window road, parity, color, size, head, tail and period counts')
def event_count(req):
 total=0;ls=list(req)
 for k in range(len(ls)+1):
  for sub in combinations(ls,k):
   missing=set().union(*(S[z] for z in sub)) if sub else set();total+=(-1)**k*comb(49-len(missing),6)
 return total
D=comb(49,6);cs=J('2026313-manual-candidates.json')['candidates'];assert len(cs)==20
for c in cs:
 r=c['roles'];U=set(c['universe']);V=set(c['display']);assert U==set(r.values())|set(c['reserve']) and V==set(r.values()) and len(U)==6
 for name,zz in [('universe_structure',U),('display_structure',V)]:
  v=set().union(*(S[z] for z in zz));x=c[name];assert x['number_count']==len(v)
  assert x['road_0_1_2']==[sum(n%3==k for n in v) for k in range(3)]
  assert x['odd_even']==[sum(n%2==1 for n in v),sum(n%2==0 for n in v)] and x['red_blue_green']==[len(v&q) for q in (R,B,G)]
  assert x['heads_0_to_4']==[sum(n//10==k for n in v) for k in range(5)] and x['tails_0_to_9']==[sum(n%10==k for n in v) for k in range(10)]
 ev=[{r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}];counts=[event_count(x) for x in ev]
 intersections=[D]+[sum(event_count(set().union(*sub)) for sub in combinations(ev,k)) for k in range(1,4)]
 dist=[sum((-1)**(j-k)*comb(j,k)*intersections[j] for j in range(k,4)) for k in range(4)]
 assert c['ideal_fair_model']['column_combinations']==counts and c['ideal_fair_model']['complete_slots_combinations']==dist
check(True,'20 manually proposed candidates and ideal-model inclusion/exclusion counts (not real probabilities)')
doc=J('2026313-manual-display-decisions.json')['decisions']['2026313'];assert doc['scope']=='user_authorized_nonofficial_observation_not_predraw_preregistration'
assert [doc[x+'_zodiac'] for x in ('top','a','b','c','d')]==['馬','兔','龍','虎','蛇'] and doc['universe_zodiac']==['馬','兔','龍','虎','蛇','豬']
html=(P/'2026313-page.html').read_text(encoding='utf8');m=re.search(r'const DATA=(.*?), ZN=DATA\.order, ALL=DATA\.rows;',html);assert m;data=json.loads(m.group(1));assert len(data['rows'])==250
for got,r in zip(data['rows'],hist[-250:]):assert got==[int(r['period']),r['date'][5:10].replace('-','/'),ns(r),[Z.index(z) for z in zs(r)],int(r['special']),Z.index(r['special_zodiac'])]
assert all(data['n2z'][str(n)]==(7-n)%12 for n in range(1,50))
m=re.search(r'const MANUAL_SITE_DECISIONS_V50=(.*?);',html);assert m and json.loads(m.group(1))['2026312']=={'U':[6,3,4,2,5,11],'top':6,'A':3,'B':4,'C':2,'D':5,'top_overlap_mode':'coverage'}
assert all(x in html for x in ('313非官方人工展示','是否赛前未经独立证实','不提供赛前预注册或官方认证','司法警察局2024年'))
check(True,'page snapshot 250 rows, 49 mappings, exact display and nonofficial warnings')
print('PASS consistency only; NOT official status, fair randomness, pre-draw timing, or financial advice')
