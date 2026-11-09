#!/usr/bin/env python3
"""Portable, offline, independent audit of the D2 nonofficial display.
No draw fetch, target result, selection, randomization, scoring or backtest ranking.
"""
from pathlib import Path
from collections import Counter
from itertools import product
from math import comb
from tempfile import TemporaryDirectory
import csv, hashlib, json, re, shutil, subprocess, sys
O=Path(__file__).resolve().parent;D=O.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def J(p):return json.loads(p.read_text(encoding='utf8'))
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def check(v,msg):
 if not v:raise AssertionError(msg)
 print('PASS',msg)
P='2026313-reanalysis-v2-';data=O/'2026313-source-data.csv';user=J(O/'2026313-user-input.json');olddata=D/'pre-registration/2026312-rev1-source-data.csv'
check(sha(data)=='7368457fed12328fb796eefaa8c97d0f6689cd926b10a624644a333311a52409','input historical data SHA-256')
a=olddata.read_bytes().splitlines(keepends=True);b=data.read_bytes().splitlines(keepends=True)
check(len(a)==1043 and len(b)==1044 and a[0]==b[0] and a[1:]==b[2:],'1,042 prior rows byte-identical, new 312 row inserted only')
rows=C(data);rows.sort(key=lambda x:int(x['period']));periods=[int(r['period']) for r in rows]
check(len(rows)==1043 and len(set(periods))==1043 and periods[-1]==2026312,'1,043 unique records through 312; no target row')
def nums(r):return [int(r[f'n{i}']) for i in range(1,7)]
def signs(r):return [r[f'z{i}'] for i in range(1,7)]
def seven(r):return set(signs(r))|{r['special_zodiac']}
check(all(len(set(nums(r)+[int(r['special'])]))==7 and all(1<=x<=49 for x in nums(r)+[int(r['special'])]) for r in rows),'all historical rows contain seven distinct in-range numbers')
check(nums(rows[-1])+[int(rows[-1]['special'])]==user['normal_numbers']+[user['seventh_number']]==[31,46,4,43,32,15,38] and signs(rows[-1])==user['normal_zodiacs'] and rows[-1]['special_zodiac']==user['seventh_zodiac'],'312 exact user-confirmed six-plus-one input and signs')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z={n:Z[(7-n)%12] for n in range(1,50)};groups={z:{n for n in range(1,50) if n2z[n]==z} for z in Z}
check(all([n2z[n] for n in nums(r)]==signs(r) and n2z[int(r['special'])]==r['special_zodiac'] for r in rows[-250:]),'all 250 on-page rows match current zodiac mapping')
e=J(O/(P+'evidence.json'));W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));rev=rows[::-1]
for z in Z:
 a=e['per_zodiac'][z];check(a['numbers']==sorted(groups[z]),'zodiac '+z+' group mapping')
 for w in W:
  b=rows[-w:];target={'balls':sum(signs(r).count(z) for r in b),'periods':sum(z in signs(r) for r in b)};assert target==a['windows'][str(w)]
 for first,last in blocks:
  b=rev[first:last+1];target={'balls':sum(signs(r).count(z) for r in b),'periods':sum(z in signs(r) for r in b)};assert target==a['disjoint_age_blocks'][f'{first}-{last}']
 assert a['last_normal_age']==next(k for k,r in enumerate(rev) if z in signs(r))
check(True,'12 zodiac ledgers across all windows and five disjoint age blocks')
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠'
for n in range(1,50):
 a=e['per_number'][str(n)];assert (a['zodiac'],a['road'],a['odd_even'],a['wave'],a['head'],a['tail'])==(n2z[n],n%3,'奇' if n%2 else '偶',wave(n),n//10,n%10)
 assert a['last_normal_age']==next(k for k,r in enumerate(rev) if n in nums(r))
 assert all(a['window_counts'][str(w)]==sum(n in nums(r) for r in rows[-w:]) for w in W)
ledger=C(O/(P+'number-ledger.csv'));check(len(ledger)==49 and {int(r['number']) for r in ledger}==set(range(1,50)),'49 individual numbers, routes, color, heads, tails, omission and windows')
for r in ledger:
 n=int(r['number']);a=e['per_number'][str(n)];assert all(int(r[f'W{w}'])==a['window_counts'][str(w)] for w in W) and r['zodiac']==a['zodiac']
assert len(C(O/(P+'zodiac-ledger.csv')))==12
for w in W:
 x=rows[-w:];ns=[n for r in x for n in nums(r)];a=e['structural_windows'][str(w)];roads=[Counter(n%3 for n in nums(r)) for r in x]
 assert a['road_ball_counts']==[sum(n%3==k for n in ns) for k in range(3)]
 assert a['odd_even_ball_counts']==[sum(n%2==1 for n in ns),sum(n%2==0 for n in ns)]
 assert a['red_blue_green_ball_counts']==[sum(wave(n)==k for n in ns) for k in ('紅','藍','綠')]
 assert a['head_ball_counts']==[sum(n//10==k for n in ns) for k in range(5)] and a['tail_ball_counts']==[sum(n%10==k for n in ns) for k in range(10)]
 assert a['no_0road_periods']==sum(c[0]==0 for c in roads) and a['three_roads_present_periods']==sum(all(c[k] for k in range(3)) for c in roads) and a['at_least_two_2road_periods']==sum(c[2]>=2 for c in roads)
check(True,'structural windows: route, parity, wave, head/tail and event counts')
byp={int(r['period']):r for r in rows}
for p in (2026309,2026310,2026311,2026312):
 a=e['adjacent_identity_repeats'][str(p)];cur,prev=byp[p],byp[p-1];assert a['seven_intersection_exact']==len(seven(cur)&seven(prev)) and a['normal6_with_previous_seven']==len(set(signs(cur))&seven(prev)) and a['normal6_with_previous_six']==len(set(signs(cur))&set(signs(prev)))
check([e['adjacent_identity_repeats'][str(p)]['seven_intersection_exact'] for p in (2026309,2026310,2026311,2026312)]==[4,4,5,5],'separate seven-v-seven / six-v-seven / six-v-six; exact 4/4/5/5')
for p,ref in ((2026308,O/(P+'308-reference.json')),(2026310,D/'pre-registration/2026310.json'),(2026311,D/'pre-registration/2026311.json'),(2026312,D/'pre-registration/2026312-rev1.json')):
 a=e['retrospectives'][str(p)];d=J(ref)['site_display'];actual=set(signs(byp[p]));req=[{Z[d['top']]},{Z[k] for k in d['t2']},{Z[k] for k in d['t3']}]
 assert [s['complete'] for s in a['slots']]==[v<=actual for v in req] and a['complete_count']==sum(v<=actual for v in req)
 assert set(a['actual_outside_universe'])==actual-set(d['universe_zodiac'])
check([e['retrospectives'][str(p)]['complete_count'] for p in (2026308,2026310,2026311,2026312)]==[0,1,2,0],'308/310/311/312 retrospectives versus prior decision snapshots')
old=J(O/'2026313-manual-display-decisions.json');new=J(O/(P+'manual-decisions.json'))
check(all(old['decisions'][k]==v for k,v in new['decisions'].items() if k!='2026313') and old['decisions']['2026313']['release_scope_version']=='nonofficial_display_D1','older period decisions and old D1 preserved')
d=new['decisions']['2026313'];roles={'top':d['top_zodiac'],'A':d['a_zodiac'],'B':d['b_zodiac'],'C':d['c_zodiac'],'D':d['d_zodiac']}
check(roles=={'top':'鼠','A':'兔','B':'龍','C':'虎','D':'豬'} and d['universe_zodiac']==['鼠','兔','龍','虎','豬','馬'] and d['release_scope_version']=='nonofficial_display_D2_reanalysis','manually specified D2 roles and reserve')
hand=J(O/(P+'handwritten-design.json'));cands=J(O/(P+'candidates.json'))
check(len(hand['candidates'])==len(cands['candidates'])==24 and hand['proposed_id']==cands['proposed_id_already_manually_declared']==d['human_comparison_id'],'24 handwritten alternatives and fixed proposed ID; no ranking')
DEN=comb(49,6)
for raw,c in zip(hand['candidates'],cands['candidates']):
 assert raw['id']==c['id'] and raw['roles']==c['roles'] and raw['reserves']==c['reserves']
 r=raw['roles'];shown=list(dict.fromkeys(r[k] for k in ('top','A','B','C','D')));U=shown+raw['reserves'];assert len(set(U))==len(U)==6 and len({r[k] for k in 'ABCD'})==4
 for names,entry in ((shown,c['display']),(U,c['universe'])):
  ns=sorted(set().union(*(groups[z] for z in names)));assert entry['zodiacs']==names and entry['numbers']==ns and entry['number_count']==len(ns)
  assert entry['road_0_1_2']==[sum(n%3==k for n in ns) for k in range(3)] and entry['odd_even']==[sum(n%2==1 for n in ns),sum(n%2==0 for n in ns)]
  assert entry['red_blue_green']==[sum(wave(n)==k for n in ns) for k in ('紅','藍','綠')] and entry['heads_0_to_4']==[sum(n//10==k for n in ns) for k in range(5)]
 # Independent direct product over how many balls come from each displayed zodiac;
 # it audits ideal-model combinatorics without using the author's inclusion-exclusion.
 col=[0,0,0];dist=[0,0,0,0];other=49-sum(len(groups[z]) for z in shown)
 for counts in product(*(range(len(groups[z])+1) for z in shown)):
  rest=6-sum(counts)
  if not 0<=rest<=other:continue
  mult=comb(other,rest)
  for z,n in zip(shown,counts):mult*=comb(len(groups[z]),n)
  active={z for z,n in zip(shown,counts) if n};done=[r['top'] in active,{r['A'],r['B']}<=active,{r['A'],r['C'],r['D']}<=active]
  for i,v in enumerate(done):col[i]+=mult*int(v)
  dist[sum(done)]+=mult
 assert col==c['ideal_model_only']['column_combinations'] and dist==c['ideal_model_only']['complete_slot_count_combinations'] and sum(dist)==DEN
check(True,'24 complete candidate structures and exact ideal-model combinatorics independently checked')
for path,digest in [('2026312.json','e8b6fa62a1a5255215fcb1eee625aa8a462271a2ec768f020668afc83c54a5e5'),('2026312-rev1.json','077a1dec6e1f5a576c20146e748b3f0bad5550dc820427850b691079a1a437c3')]:assert sha(D/'pre-registration'/path)==digest
check(not (D/'pre-registration/2026313.json').exists(),'312 frozen original/rev1 hashes intact; no 313 preregistration')
page=(O/(P+'page.html')).read_text(encoding='utf8');m=re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page);assert m;payload=json.loads(m.group(1));assert payload['order']==Z and len(payload['rows'])==250
for a,r in zip(payload['rows'],rows[-250:]):assert a==[int(r['period']),r['date'][5:10].replace('-','/'),nums(r),[Z.index(z) for z in signs(r)],int(r['special']),Z.index(r['special_zodiac'])]
check(payload['n2z']=={str(k):Z.index(v) for k,v in n2z.items()},'all 250 embedded browser rows and complete 49 mapping agree with source')
m=re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page);assert m;md=json.loads(m.group(1));q=md['2026312'];assert q=={'U':[0,3,4,2,11,6],'top':0,'A':3,'B':4,'C':2,'D':11,'top_overlap_mode':'coverage'}
assert '313赛前未核实、无预注册' in page and '来源与机制未认证' in page and '谨防博彩诈骗' in page and P+'analysis.md' in page
check(True,'page manual fields, D2 audit link and compact risk notice')
with TemporaryDirectory(prefix='d2-rebuild-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(data,t/'data/macau_mark_six_full.csv');shutil.copyfile(O/(P+'manual-decisions.json'),t/'data/manual_site_decisions.json')
 result=subprocess.run([sys.executable,str(O/(P+'generator.py'))],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 assert (t/'zodiac_trend.html').read_bytes()==(O/(P+'page.html')).read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
check(True,'empty-directory byte-for-byte page reproduction in both output locations')
print('D2 OFFLINE INDEPENDENT VERIFICATION PASS — descriptive evidence only, not an official result or proof of predraw timing')
