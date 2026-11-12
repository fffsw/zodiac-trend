#!/usr/bin/env python3
"""Portable offline verification of 315 retrospective and 316 display package.
No target result lookup, selection, timing, official status or draw mechanism authentication.
Run as: python3 observations/2026316-verify.py (from any directory).
"""
from pathlib import Path
from collections import Counter
from itertools import product
from tempfile import TemporaryDirectory
from math import comb
import csv,hashlib,json,os,re,shutil,subprocess,sys
O=Path(__file__).resolve().parent;D=O.parent;F=O/'2026315-retrospective-frozen';J=lambda n:json.loads((O/n).read_text(encoding='utf8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ck(x,m):
 if not x:raise AssertionError(m)
 checks.append(m);print('PASS',m)
old=(F/'history-through-314.csv').read_bytes().splitlines(keepends=True);new=(O/'2026316-source-data.csv').read_bytes().splitlines(keepends=True);ck(len(old)==1046 and len(new)==1047 and old[0]==new[0] and old[1:]==new[2:],'1045 earlier source rows byte-identical; only user 315 added')
assert sha(F/'history-through-314.csv')=='687efa128921ef7ace365131c023592a162a8dca4c367c88949ea0c16656ffb5';assert sha(O/'2026316-source-data.csv')=='d84c05b808a03c2c84b6a8191fb28e292da090df8a8708b2150f899dd3eea314'
rows=C(O/'2026316-source-data.csv');N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zn=lambda n:Z[(7-n)%12];groups={z:[n for n in range(1,50) if zn(n)==z] for z in Z};u=J('2026315-user-result.json');ck(len(rows)==1046 and len({r['period'] for r in rows})==1046 and [r['period'] for r in rows[:4]]==['2026315','2026314','2026313','2026312'],'1046 distinct source periods through 315')
ck(u['date'] is None and u['issue_and_six_plus_one_are_inferred_from_conversation'] and rows[0]['date']==rows[1]['date']==rows[2]['date']=='' and N(rows[0])==u['normal_numbers']==[6,9,25,27,33,22] and int(rows[0]['special'])==u['seventh_number']==48,'user 315 exact six-plus-one inferred, 313–315 dates unknown')
ck(N(rows[1])+[int(rows[1]['special'])]==[13,26,9,37,34,44,31] and N(rows[2])+[int(rows[2]['special'])]==[33,39,45,15,7,20,43] and N(rows[3])+[int(rows[3]['special'])]==[31,46,4,43,32,15,38],'user 314, 313 and corrected 312 unchanged')
ck(all(len(set(N(r)+[int(r['special'])]))==7 for r in rows) and all([zn(n) for n in N(r)]==[r[f'z{i}'] for i in range(1,7)] and zn(int(r['special']))==r['special_zodiac'] for r in rows[:250]),'distinct seven numbers and zodiac mapping of displayed rows')
# 315 original decision settled against the six user numbers, not the seventh.
oldplan=json.loads((F/'315-38-handwritten.json').read_text())['candidates'];out=J('2026315-retrospective-evidence.json');ballset={zn(n) for n in N(rows[0])};assert len(oldplan)==38 and ballset=={'牛','狗','馬','龍','鷄'}
settled=[]
for x,y in zip(oldplan,out['frozen_38_candidate_review']['original_order_candidates']):
 r=x['roles'];sets=[{r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}];done=[s<=ballset for s in sets];counts=[len(s&ballset) for s in sets];assert x['id']==y['id'] and x['roles']==y['roles'] and x['reserves']==y['reserves'] and [v['present_count'] for v in y['slots']]==counts and y['complete_count']==sum(done);settled.append(sum(done))
ck(Counter(settled)=={0:21,1:12,2:5} and settled[0]==0 and [v['present_count'] for v in out['settlement']['slots']]==[0,1,1] and out['settlement']['complete_count']==0,'315 P01 0/1, 1/2, 1/3; all 38 frozen candidate outcomes independently settled')
ck(Counter(n%3 for n in N(rows[0]))=={0:4,1:2} and sum(n%2 for n in N(rows[0]))==4 and sum(N(rows[0]))==122,'315 normal balls route 4/2/0, parity 4/2 and sum 122')
e=J('2026316-evidence.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));assert e['history_rows']==1046 and e['latest_period']==2026315 and e['history_sha256']==sha(O/'2026316-source-data.csv')
for z in Z:
 v=e['per_zodiac'][z];g=set(groups[z]);assert v['numbers']==groups[z] and v['last_normal_age']==next(i for i,r in enumerate(rows) if any(n in g for n in N(r)))
 for w in W:
  b=[N(r) for r in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(sum(n in g for n in a) for a in b),'periods':sum(any(n in g for n in a) for a in b)}
 for lo,hi in blocks:
  b=[N(r) for r in rows[lo:hi+1]];assert v['disjoint_age_blocks'][f'{lo}-{hi}']=={'balls':sum(sum(n in g for n in a) for a in b),'periods':sum(any(n in g for n in a) for a in b)}
ck(len(C(O/'2026316-zodiac-ledger.csv'))==12,'12 signs, eight normal-ball windows and five nonoverlapping age blocks')
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠';ledger=C(O/'2026316-number-ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for item in ledger:
 n=int(item['number']);v=e['per_number'][str(n)];assert (v['zodiac'],v['road'],v['odd_even'],v['wave'],v['head'],v['tail'])==(zn(n),n%3,'奇' if n%2 else '偶',wave(n),n//10,n%10) and v['last_normal_age']==next(i for i,r in enumerate(rows) if n in N(r))
 for w in W:assert int(item[f'W{w}'])==v['window_counts'][str(w)]==sum(n in N(r) for r in rows[:w])
ck(True,'all 49 numbers, mappings, attributes, ages and eight normal-ball windows')
q=J('2026316-independent-qc.json')
for w in W:
 rs=rows[:w];nums=[n for r in rs for n in N(r)];v=e['structural_windows'][str(w)];assert v['road_ball_counts']==[sum(n%3==k for n in nums) for k in range(3)] and v['odd_even_ball_counts']==[sum(n%2 for n in nums),sum(n%2==0 for n in nums)] and v['red_blue_green_ball_counts']==[sum(wave(n)==c for n in nums) for c in ('紅','藍','綠')]
 v=q['selected_shape_condition_counts'][str(w)];assert v['no_0road']==sum(not any(n%3==0 for n in N(r)) for r in rs) and v['no_2road']==sum(not any(n%3==2 for n in N(r)) for r in rs) and v['no_odd_0road']==sum(not any(n%3==0 and n%2 for n in N(r)) for r in rs) and v['at_most_two_odd']==sum(sum(n%2 for n in N(r))<=2 for r in rs) and v['no_dog']==sum('狗' not in {zn(n) for n in N(r)} for r in rs)
ck(True,'selected normal-ball route, parity, color and pressure scenarios independently recounted')
seven=lambda r:set([r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']]);by={int(r['period']):r for r in rows};counts=[len(seven(by[p])&seven(by[p-1])) for p in range(2026309,2026316)];ck(counts==[4,4,5,5,3,3,3],'309–315 seven-versus-seven identity intersections, not normal or special-number picks')
x=C(F/'445-source-through-311.csv');sets=[set(r['zodiacs'].split()) if r['usable']=='1' else None for r in x]+[seven(rows[i]) for i in (3,2,1,0)];tr=[None]+[len(a&b) if a is not None and b is not None else None for a,b in zip(sets,sets[1:])];ends=[i for i in range(3,len(sets)) if tr[i-2:i+1]==[4,4,5]];follows=Counter(tr[i+1] for i in ends if i+1<len(tr));invalid=sum(None in tr[i-2:i+1] for i in range(3,len(sets)));repeat=J('2026315-retrospective-repeat445.json');ck(len(sets)==2496 and len(ends)==9 and follows=={2:2,3:3,4:3,5:1} and invalid==8 and repeat['valid_candidate_windows']==2485,'445 exact 4/4/5 seven-ball intersections; 8 invalid windows excluded')
hand=J('2026316-handwritten-design.json');audit=J('2026316-candidates.json');m=J('2026316-manual-decision.json');assert len(hand['candidates'])==len(audit['candidates'])==38
for key,name in [('handcrafted_candidates.json','2026316-handwritten-design.json'),('manual_decision.json','2026316-manual-decision.json'),('evidence.json','2026316-evidence.json')]:assert audit['input_sha256'][key]==sha(O/name)
den=comb(49,6);sigs=[];overlap=0
for a,b in zip(hand['candidates'],audit['candidates']):
 r=a['roles'];shown=list(dict.fromkeys(r[k] for k in ('top','A','B','C','D')));assert a['id']==b['id'] and r==b['roles'] and a['reserves']==b['reserves'] and len({r[k] for k in 'ABCD'})==4 and len(set(shown)|set(a['reserves']))==6 and not set(shown)&set(a['reserves']);ss={'single':{r['top']},'pair':{r['A'],r['B']},'triple':{r['A'],r['C'],r['D']},'all_columns':set(shown)};sigs.append((r['top'],frozenset(ss['pair']),frozenset(ss['triple'])));overlap+=r['top'] in {r[k] for k in 'ABCD'}
 for key,gs in ss.items():
  road=[sum(groups[z][0]%3==n for z in gs) for n in range(3)];odd=sum(groups[z][0]%2 for z in gs);assert b['minimums'][key]=={'distinct_zodiacs':len(gs),'road_min':road,'odd_min':odd,'even_min':len(gs)-odd}
 for road in range(3):assert b['no_route_forced_incomplete_columns'][str(road)]==[name for name in ('single','pair','triple') if any(groups[z][0]%3==road for z in ss[name])]
 count=[0,0,0,0];col=[0,0,0];both=0;rest=49-sum(len(groups[z]) for z in shown)
 for v in product(*(range(len(groups[z])+1) for z in shown)):
  rem=6-sum(v)
  if not 0<=rem<=rest:continue
  ways=comb(rest,rem)
  for z,k in zip(shown,v):ways*=comb(len(groups[z]),k)
  active={z for z,k in zip(shown,v) if k};done=[ss[k]<=active for k in ('single','pair','triple')];count[sum(done)]+=ways
  for i,k in enumerate(done):col[i]+=ways*k
  if done[1] and done[2]:both+=ways
 assert sum(count)==den;actual={'single_pct':col[0],'pair_pct':col[1],'triple_pct':col[2],'all_columns_pct':count[3],'no_column_pct':count[0],'pair_and_triple_pct':both};assert all(abs(100*v/den-b['ideal_model_probabilities_percent'][k])<1e-9 for k,v in actual.items())
ck(len(set(sigs))==36 and overlap==10 and {x['roles']['A'] for x in hand['candidates']}==set(Z) and hand['proposed_id']==m['human_choice']==audit['selected']['id']=='Q01','38 handwritten designs, 36 distinct columns, 10 overlaps, exact ideal-model enumeration')
ck(m['universe']==['鷄','狗','蛇','馬','虎','牛'] and m['top']=='鷄' and m['pair']==['狗','蛇'] and m['triple']==['狗','馬','虎'] and m['reserves']==['牛'],'manually fixed Q01; reserve outside all columns')
sel=audit['selected'];ck(sel['minimums']['triple']['odd_min']==3 and sel['minimums']['all_columns']['road_min']==[1,2,2] and sel['minimums']['all_columns']['odd_min']==3 and sel['minimums']['all_columns']['even_min']==2 and sel['no_route_forced_incomplete_columns']=={'0':['pair','triple'],'1':['single','triple'],'2':['pair','triple']},'explicit joint route/parity risk, absent road effects and shared dog')
other={x['id']:x for x in audit['candidates']};p=sel['ideal_model_probabilities_percent'];ck(other['Q20']['ideal_model_probabilities_percent']==p and other['Q21']['ideal_model_probabilities_percent']['no_column_pct']<p['no_column_pct'] and other['Q35']['ideal_model_probabilities_percent']['all_columns_pct']>p['all_columns_pct'] and other['Q35']['ideal_model_probabilities_percent']['no_column_pct']>p['no_column_pct'],'same-universe counterexamples retained; model is not evidence of prediction')
d=J('2026316-manual-decisions.json');previous=json.loads((F/'manual-site-decisions-through-315.json').read_text());ck(all(d['decisions'][k]==v for k,v in previous['decisions'].items()) and len(d['decisions'])==len(previous['decisions'])+1 and d['decisions']['2026316']['target']==2026316,'all prior manual decisions preserved, 316 appended')
for n,h in [('2026312.json','e8b6fa62a1a5255215fcb1eee625aa8a462271a2ec768f020668afc83c54a5e5'),('2026312-rev1.json','077a1dec6e1f5a576c20146e748b3f0bad5550dc820427850b691079a1a437c3')]:assert sha(D/'pre-registration'/n)==h
ck(all(not (D/'pre-registration'/f'2026{n}.json').exists() for n in (313,314,315,316)),'312 originals unchanged; no 313–316 retroactive preregistration')
page=(O/'2026316-page.html').read_text(encoding='utf8');pd=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));assert len(pd['rows'])==250 and pd['order']==Z
for a,r in zip(pd['rows'],reversed(rows[:250])):assert a==[int(r['period']),r['date'][5:10].replace('-','/') if r['date'] else '--/--',N(r),[Z.index(r[f'z{i}']) for i in range(1,7)],int(r['special']),Z.index(r['special_zodiac'])]
assert pd['n2z']=={str(n):Z.index(zn(n)) for n in range(1,50)};md=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));assert md['2026315']=={'U':[9,10,5,6,2,1],'top':9,'A':10,'B':5,'C':6,'D':2,'top_overlap_mode':'coverage'} and '<footer' not in page and 'footSrc' not in page
ck(True,'complete page payload, unknown dates, exact Q01 slots, deleted footer and 49 zodiac mappings')
with TemporaryDirectory(prefix='316-reproduce-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026316-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026316-manual-decisions.json',t/'data/manual_site_decisions.json');env=dict(os.environ);env['POOL_VERSION']='v5.0';subprocess.run([sys.executable,str(O/'2026316-generator.py')],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026316-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
ck(True,'standalone generator reproduces packaged page byte-for-byte')
subprocess.run(['sha256sum','--quiet','--check','../2026315-retrospective-before.sha256'],cwd=F,check=True);ck(True,'all 24 frozen 315 before-files match original SHA-256 manifest')
for manifest in ('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256'):subprocess.run(['sha256sum','--quiet','--check',manifest],cwd=O,check=True)
ck(True,'nine existing plus one new immutable evidence manifests verified')
print('OFFLINE 315/316 VERIFICATION PASS — no proof of source, predraw status, mechanism, prediction or returns')
