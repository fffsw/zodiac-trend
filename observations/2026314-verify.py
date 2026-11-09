#!/usr/bin/env python3
"""Offline, independent 314 release verification (no target lookup or selection).
Run from any cwd; all required evidence is beside this script except 312 frozen
files in ../pre-registration. This does not establish authenticity or timing.
"""
from pathlib import Path
from collections import Counter
from math import comb
from tempfile import TemporaryDirectory
import csv,hashlib,json,os,re,shutil,subprocess,sys
O=Path(__file__).resolve().parent;D=O.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def J(n):return json.loads((O/n).read_text(encoding='utf8'))
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ck(x,msg):
 if not x:raise AssertionError(msg)
 print('PASS',msg)
prior=O/'2026313-source-data.csv';source=O/'2026314-source-data.csv';old=prior.read_bytes().splitlines(keepends=True);new=source.read_bytes().splitlines(keepends=True)
ck(sha(prior)=='7368457fed12328fb796eefaa8c97d0f6689cd926b10a624644a333311a52409' and sha(source)=='662032bf9829c1451ea4dcc221b2b4c8386d5efe953a73e1ac14789b0869e629','source SHA-256 matches frozen 312 and staged 313')
ck(len(old)==1044 and len(new)==1045 and old[0]==new[0] and old[1:]==new[2:],'all 1043 original record lines retained byte-for-byte')
rows=C(source);ck(len(rows)==1044 and len({r['period'] for r in rows})==1044 and rows[0]['period']=='2026313' and rows[1]['period']=='2026312','1044 unique records and correct descending endpoint')
N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zn=lambda n:Z[(7-n)%12];groups={z:[n for n in range(1,50) if zn(n)==z] for z in Z}
u=J('2026313-user-result.json');ck(u['date'] is None and rows[0]['date']=='' and N(rows[0])==u['normal_numbers']==[33,39,45,15,7,20] and int(rows[0]['special'])==u['seventh_number']==43,'313 is user input only, date blank, exact six-plus-one; period/order inferred')
ck(N(rows[1])+[int(rows[1]['special'])]==[31,46,4,43,32,15,38],'confirmed 312 first ball and all seven unchanged')
ck(all(len(set(N(r)+[int(r['special'])]))==7 for r in rows),'seven numbers distinct in all source records')
ck(all([zn(n) for n in N(r)]==[r[f'z{i}'] for i in range(1,7)] and zn(int(r['special']))==r['special_zodiac'] for r in rows[:250]),'250 displayed historical rows agree with current zodiac mapping')
e=J('2026314-evidence.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44))
for z in Z:
 v=e['per_zodiac'][z];assert v['numbers']==groups[z];g=set(groups[z]);assert v['last_normal_age']==next(i for i,r in enumerate(rows) if any(n in g for n in N(r)))
 for w in W:
  b=[N(r) for r in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(sum(n in g for n in a) for a in b),'periods':sum(any(n in g for n in a) for a in b)}
 for first,last in blocks:
  b=[N(r) for r in rows[first:last+1]];assert v['disjoint_age_blocks'][f'{first}-{last}']=={'balls':sum(sum(n in g for n in a) for a in b),'periods':sum(any(n in g for n in a) for a in b)}
ck(len(C(O/'2026314-zodiac-ledger.csv'))==12,'12 zodiac windows and non-overlapping blocks independently recounted')
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠'
ledger=C(O/'2026314-number-ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for row in ledger:
 n=int(row['number']);x=e['per_number'][str(n)];assert (x['zodiac'],x['road'],x['odd_even'],x['wave'],x['head'],x['tail'])==(zn(n),n%3,'奇' if n%2 else '偶',wave(n),n//10,n%10);assert x['last_normal_age']==next(i for i,r in enumerate(rows) if n in N(r))
 for w in W:assert int(row[f'W{w}'])==x['window_counts'][str(w)]==sum(n in N(r) for r in rows[:w])
ck(True,'49 normal numbers, mapping, attributes, ages, and eight windows independently checked')
for w in W:
 rs=rows[:w];n=[a for r in rs for a in N(r)];x=e['structural_windows'][str(w)];assert x['road_ball_counts']==[sum(a%3==k for a in n) for k in range(3)] and x['odd_even_ball_counts']==[sum(a%2 for a in n),sum(a%2==0 for a in n)] and x['red_blue_green_ball_counts']==[sum(wave(a)==c for a in n) for c in ('紅','藍','綠')] and x['head_ball_counts']==[sum(a//10==k for a in n) for k in range(5)] and x['tail_ball_counts']==[sum(a%10==k for a in n) for k in range(10)]
ck(True,'012 roads, parity, waves, heads and tails independently counted from six normals')
# Separate historical seven-ball zodiac identity intersections, including current seventh only here.
seven=lambda r:set([r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']]);by={int(r['period']):r for r in rows}
counts=[len(seven(by[p])&seven(by[p-1])) for p in range(2026309,2026314)];ck(counts==[4,4,5,5,3] and e['adjacent_identity_repeats']['2026313']['seven_v_seven_count']==3,'309–313 exact seven-v-seven distinct zodiac overlaps 4/4/5/5/3')
frozen=O/'2026314-445-source-through-311.csv';ck(sha(frozen)=='50a169bba6e0c07c57c7f105c19c92505b96d149d7c16e992bf8a4be2adfe156','full-history 445 input snapshot hash')
x=C(frozen);sets=[set(r['zodiacs'].split()) if r['usable']=='1' else None for r in x]+[seven(rows[1]),seven(rows[0])];tr=[None]+[len(a&b) if a is not None and b is not None else None for a,b in zip(sets,sets[1:])];ends=[i for i in range(3,len(sets)) if tr[i-2:i+1]==[4,4,5]];follows=Counter(tr[i+1] for i in ends if i+1<len(tr));inv=sum(None in tr[i-2:i+1] for i in range(3,len(sets)));r=J('2026314-repeat-445.json');ck(len(sets)==2494 and len(ends)==9 and follows=={2:2,3:3,4:3,5:1} and inv==8 and r['valid_candidate_windows']==2483,'445 exact seven-ball, 9 followups; bad-draw windows excluded')
# Independent direct polynomial multiplication; candidate source fixed before metric audit.
def probability(gs):
 poly=[1]+[0]*6
 for z in gs:
  q=[0]+[comb(len(groups[z]),i) if i<=len(groups[z]) else 0 for i in range(1,7)];poly=[sum(poly[i]*q[j-i] for i in range(j+1)) for j in range(7)]
 rest=49-sum(len(groups[z]) for z in gs);return 100*sum(poly[i]*comb(rest,6-i) for i in range(7))/comb(49,6)
hand=J('2026314-handwritten-design.json');audit=J('2026314-candidates.json');m=J('2026314-manual-decision.json');assert len(hand['candidates'])==len(audit['candidates'])==31
for key,name in [('handcrafted_candidates.json','2026314-handwritten-design.json'),('manual_decision.json','2026314-manual-decision.json'),('evidence.json','2026314-evidence.json')]:assert audit['input_sha256'][key]==sha(O/name)
seen=[]
for a,b in zip(hand['candidates'],audit['candidates']):
 r=a['roles'];assert a['id']==b['id'] and r==b['roles'] and a['reserves']==b['reserves'];assert len({r[k] for k in 'ABCD'})==4 and len(set(r.values())|set(a['reserves']))==6 and not set(r.values())&set(a['reserves']);seen.append(tuple(r[k] for k in ('top','A','B','C','D')))
 for k,gs in {'single':{r['top']},'pair':{r['A'],r['B']},'triple':{r['A'],r['C'],r['D']},'all_columns':set(r.values())}.items():
  assert abs(probability(gs)-b['ideal_model_probabilities_percent'][k])<1e-9;road=[sum(groups[z][0]%3==n for z in gs) for n in range(3)];odd=sum(groups[z][0]%2 for z in gs);assert b['minimums'][k]=={'distinct_zodiacs':len(gs),'road_min':road,'odd_min':odd,'even_min':len(gs)-odd}
ck(len(set(seen))==30 and {a['roles']['A'] for a in hand['candidates']}==set(Z) and hand['proposed_id']==m['human_choice']==audit['selected']['id'],'31 prewritten designs, 30 distinct column structures, 12 A identities; no selection by audit')
ck(m['top']=='牛' and m['pair']==['虎','馬'] and m['triple']==['虎','狗','鷄'] and m['reserves']==['豬'],'human chosen roles and reserve')
ck(audit['selected']['minimums']['triple']['road_min']==[1,1,1] and audit['selected']['minimums']['all_columns']['road_min']==[2,2,1] and audit['selected']['minimums']['all_columns']['odd_min']==3,'joint minimums and shared A independently reconstructed')
d=J('2026314-manual-decisions.json');pre=J('2026313-reanalysis-v2-manual-decisions.json');ck(all(d['decisions'][k]==v for k,v in pre['decisions'].items()) and d['decisions']['2026314']['human_comparison_id']==m['human_choice'],'all prior manual records preserved and 314 choice appended')
for n,h in [('2026312.json','e8b6fa62a1a5255215fcb1eee625aa8a462271a2ec768f020668afc83c54a5e5'),('2026312-rev1.json','077a1dec6e1f5a576c20146e748b3f0bad5550dc820427850b691079a1a437c3')]:assert sha(D/'pre-registration'/n)==h
ck(not (D/'pre-registration/2026313.json').exists() and not (D/'pre-registration/2026314.json').exists(),'312 original/rev1 frozen; no false 313 or 314 prereg')
page=(O/'2026314-page.html').read_text(encoding='utf8');assert sha(O/'2026314-page.html')=='54c9d5da57cca4fa2b8f4d2c151f31b228cd3a4de3b4fed6ef2c5cd0b6f23b0b';p=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));assert len(p['rows'])==250 and p['order']==Z
for a,r in zip(p['rows'],reversed(rows[:250])):assert a==[int(r['period']),r['date'][5:10].replace('-','/') if r['date'] else '--/--',N(r),[Z.index(r[f'z{i}']) for i in range(1,7)],int(r['special']),Z.index(r['special_zodiac'])]
assert p['n2z']=={str(n):Z.index(zn(n)) for n in range(1,50)};md=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));assert md['2026313']=={'U':[1,2,6,10,9,11],'top':1,'A':2,'B':6,'C':10,'D':9,'top_overlap_mode':'coverage'}
ck(all(x in page for x in ('314赛前未核实、无预注册','来源与机制未认证','谨防博彩诈骗','2026314-analysis.md','313日期未知')),'browser payload, exact slots, unknown date and compact risk notice')
with TemporaryDirectory(prefix='314-reproduce-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(source,t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026314-manual-decisions.json',t/'data/manual_site_decisions.json');env=dict(os.environ);env['POOL_VERSION']='v5.0';subprocess.run([sys.executable,str(O/'2026314-generator.py')],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026314-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
ck(True,'self-contained byte-for-byte page reproduction from packaged source and decision')
print('314 OFFLINE INDEPENDENT VERIFICATION PASS — no official-source, predraw-time, mechanism, odds or predictive claim')
