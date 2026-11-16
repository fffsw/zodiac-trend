#!/usr/bin/env python3
"""Portable offline verification of 317 retrospective and 318 manual display.
Run python3 observations/2026318-verify.py. No result lookup, random choice,
source/timing authentication, predictive claim, or network is used.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
from tempfile import TemporaryDirectory
from math import comb
import csv,hashlib,json,os,re,shutil,subprocess,sys
O=Path(__file__).resolve().parent;D=O.parent;F=O/'2026317-retrospective-frozen';J=lambda n:json.loads((O/n).read_text(encoding='utf8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ck(x,m):
 if not x:raise AssertionError(m)
 checks.append(m);print('PASS',m)
r=subprocess.run([sys.executable,str(O/'2026317-verify.py')],cwd=D,capture_output=True,text=True,timeout=90);ck(r.returncode==0 and 'OFFLINE 316/317 VERIFICATION PASS' in r.stdout,'unchanged prior portable verifier and eleven canonical manifests pass')
old=(F/'history-through-316.csv').read_bytes().splitlines(keepends=True);new=(O/'2026318-source-data.csv').read_bytes().splitlines(keepends=True);ck(len(old)==1048 and len(new)==1049 and old[0]==new[0] and old[1:]==new[2:] and all(x.endswith(b'\r\n') for x in new),'1047 earlier source rows and CRLF byte-identical; only user 317 added')
ck(sha(F/'history-through-316.csv')==sha(O/'2026317-source-data.csv')=='c512317d3da1c9cb80af3d335e884733d7783444e0d454cfe75cb572b7178e88' and sha(O/'2026318-source-data.csv')=='107f5139da77110592bfef5985de3563489d1e3e2950ae69acb6009c4e3fce9e','source-data hashes and preceding public snapshot match')
rows=C(O/'2026318-source-data.csv');N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zn=lambda n:Z[(7-n)%12];groups={z:[n for n in range(1,50) if zn(n)==z] for z in Z};u=J('2026317-user-result.json');ck(len(rows)==1048 and len({r['period'] for r in rows})==1048 and [r['period'] for r in rows[:5]]==['2026317','2026316','2026315','2026314','2026313'],'1048 distinct source periods through user 317')
ck(u['date'] is None and u['issue_and_six_plus_one_are_inferred_from_conversation'] and all(rows[i]['date']=='' for i in range(5)) and N(rows[0])==u['normal_numbers']==[31,49,30,22,43,24] and int(rows[0]['special'])==u['seventh_number']==26,'317 exact user six-plus-one inferred, 313–317 dates unknown')
ck([zn(n) for n in N(rows[0])]==u['normal_zodiacs']==['鼠','馬','牛','鷄','鼠','羊'] and zn(26)==u['seventh_zodiac']=='蛇' and all(len(set(N(r)+[int(r['special'])]))==7 for r in rows) and all([zn(n) for n in N(r)]==[r[f'z{i}'] for i in range(1,7)] and zn(int(r['special']))==r['special_zodiac'] for r in rows[:250]),'distinct seven values and 250 mapped rows; seventh separate from normal settlement')
oldplan=json.loads((F/'317-38-handwritten.json').read_text())['candidates'];retro=J('2026317-retrospective-evidence.json');ballset={zn(n) for n in N(rows[0])};assert len(oldplan)==38 and ballset=={'鼠','馬','牛','鷄','羊'};settled=[]
for x,y in zip(oldplan,retro['frozen_38_candidate_review']['original_order_candidates']):
 role=x['roles'];sets=[{role['top']},{role['A'],role['B']},{role['A'],role['C'],role['D']}];done=[s<=ballset for s in sets];counts=[len(s&ballset) for s in sets];assert x['id']==y['id'] and x['roles']==y['roles'] and x['reserves']==y['reserves'] and [v['present_count'] for v in y['slots']]==counts and y['complete_count']==sum(done);settled.append(sum(done))
ck(Counter(settled)=={0:29,1:9} and settled[0]==0 and [v['present_count'] for v in retro['settlement']['slots']]==[0,0,2] and retro['settlement']['complete_count']==0 and retro['settlement']['display_ball_count']==2 and retro['settlement']['outside_universe_ball_count']==4,'317 R01 0/1, 0/2, 2/3: independently settle all 38 frozen candidates')
ck([sum(n%3==k for n in N(rows[0])) for k in range(3)]==[2,4,0] and sum(n%2 for n in N(rows[0]))==3 and sum(N(rows[0]))==199 and not any(n%3==0 and n%2 for n in N(rows[0])) and any(n%3==1 and n%2==0 for n in N(rows[0])) and '兔' not in ballset,'317 normal 2/4/0, parity 3/3, sum 199: no odd0, chicken even1 is not rabbit')
seven=lambda row:set([row[f'z{i}'] for i in range(1,7)]+[row['special_zodiac']]);by={int(row['period']):row for row in rows};counts=[len(seven(by[p])&seven(by[p-1])) for p in range(2026309,2026318)];ck(counts==[4,4,5,5,3,3,3,4,3] and {zn(n) for n in N(rows[0])}&{zn(n) for n in N(rows[1])}=={'馬','鷄'} and seven(rows[0])&seven(rows[1])=={'蛇','馬','鷄'},'six-versus-six and seven-versus-seven zodiac identity intersections separated')
x=C(F/'445-source-through-311.csv');sets=[set(row['zodiacs'].split()) if row['usable']=='1' else None for row in x]+[seven(rows[i]) for i in (5,4,3,2,1,0)];tr=[None]+[len(a&b) if a is not None and b is not None else None for a,b in zip(sets,sets[1:])];ends=[i for i in range(3,len(sets)) if tr[i-2:i+1]==[4,4,5]];follows=Counter(tr[i+1] for i in ends if i+1<len(tr));invalid=sum(None in tr[i-2:i+1] for i in range(3,len(sets)));repeat=J('2026317-retrospective-repeat445.json');ck(len(sets)==2498 and len(ends)==9 and follows=={2:2,3:3,4:3,5:1} and invalid==8 and repeat['valid_candidate_windows']==2487,'exact 4/4/5 deduplicated seven-ball intersections; 8 invalid windows excluded')
e=J('2026318-evidence.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));assert e['history_rows']==1048 and e['latest_period']==2026317 and e['latest_date'] is None and e['history_sha256']==sha(O/'2026318-source-data.csv') and e['windows_overlap_not_independent_votes']
for z in Z:
 v=e['per_zodiac'][z];g=set(groups[z]);assert v['numbers']==groups[z] and v['last_normal_age']==next(i for i,row in enumerate(rows) if any(n in g for n in N(row))) and 'previous_seven_identity' not in v
 for w in W:
  b=[N(row) for row in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(sum(n in g for n in a) for a in b),'periods':sum(any(n in g for n in a) for a in b)}
 for lo,hi in blocks:
  b=[N(row) for row in rows[lo:hi+1]];assert v['disjoint_age_blocks'][f'{lo}-{hi}']=={'balls':sum(sum(n in g for n in a) for a in b),'periods':sum(any(n in g for n in a) for a in b)}
ck(len(C(O/'2026318-zodiac-ledger.csv'))==12,'12 signs, eight normal-ball windows and five nonoverlapping age blocks independently recounted')
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠';ledger=C(O/'2026318-number-ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for item in ledger:
 n=int(item['number']);v=e['per_number'][str(n)];assert (v['zodiac'],v['road'],v['odd_even'],v['wave'],v['head'],v['tail'])==(zn(n),n%3,'奇' if n%2 else '偶',wave(n),n//10,n%10) and v['last_normal_age']==next(i for i,row in enumerate(rows) if n in N(row))
 for w in W:assert int(item[f'W{w}'])==v['window_counts'][str(w)]==sum(n in N(row) for row in rows[:w])
ck(True,'49 numbers: attributes, age and eight normal-ball windows independently recounted')
pairkey=lambda a,b:'|'.join(sorted((a,b),key=Z.index));zset=lambda row:{zn(n) for n in N(row)}
for w in W:
 rs=rows[:w];balls=[n for row in rs for n in N(row)];v=e['structural_windows'][str(w)];assert v['road_ball_counts']==[sum(n%3==k for n in balls) for k in range(3)] and v['odd_even_ball_counts']==[sum(n%2 for n in balls),sum(n%2==0 for n in balls)] and v['red_blue_green_ball_counts']==[sum(wave(n)==c for n in balls) for c in ('紅','藍','綠')] and v['head_ball_counts']==[sum(n//10==k for n in balls) for k in range(5)] and v['tail_ball_counts']==[sum(n%10==k for n in balls) for k in range(10)]
 for k in range(3):
  assert v[f'no_{k}road_periods']==sum(not any(n%3==k for n in N(row)) for row in rs)
  for par in ('odd','even'):assert v[f'no_{par}_{k}road_periods']==sum(not any(n%3==k and n%2==(par=='odd') for n in N(row)) for row in rs)
 for a,b in combinations(Z,2):assert e['joint_zodiac_absence_periods'][str(w)][pairkey(a,b)]==sum(not {a,b}&zset(row) for row in rs)
 for z in Z:
  p=e['same_route_parity_peer_present_target_absent_periods'][str(w)][z];other=p['peer'];assert other!=z and groups[other][0]%6==groups[z][0]%6 and p['target_absent_peer_present_periods']==sum(z not in zset(row) and other in zset(row) for row in rs)
ledger=C(O/'2026318-joint-absence-ledger.csv');assert len(ledger)==66 and all(int(x[f'W{w}_both_absent'])==e['joint_zodiac_absence_periods'][str(w)][pairkey(x['sign_one'],x['sign_two'])] for x in ledger for w in (35,40,45));ck(True,'all 66 joint absences, same-class replacement, route, parity, wave, head and tail rechecked')
ck([e['joint_zodiac_absence_periods'][str(w)]['牛|馬'] for w in (35,40,45)]==[10,11,13] and [e['joint_zodiac_absence_periods'][str(w)]['兔|狗'] for w in (35,40,45)]==[8,10,11],'S01 cow+horse and R01 rabbit+dog jointly absent counts exposed; overlapping, non-predictive')
hand=J('2026318-handwritten-design.json');audit=J('2026318-candidates.json');m=J('2026318-manual-decision.json');assert len(hand['candidates'])==len(audit['candidates'])==38
for key,name in [('handcrafted_candidates.json','2026318-handwritten-design.json'),('manual_decision.json','2026318-manual-decision.json'),('evidence.json','2026318-evidence.json')]:assert audit['input_sha256'][key]==sha(O/name)
den=comb(49,6);sigs=defaultdict(list);aa=Counter();overlap=[]
for a,b in zip(hand['candidates'],audit['candidates']):
 r=a['roles'];shown=list(dict.fromkeys(r[k] for k in ('top','A','B','C','D')));assert a['id']==b['id'] and r==b['roles'] and a['reserves']==b['reserves'] and len({r[k] for k in 'ABCD'})==4 and len(set(shown)|set(a['reserves']))==6 and not set(shown)&set(a['reserves']);ss={'single':{r['top']},'pair':{r['A'],r['B']},'triple':{r['A'],r['C'],r['D']},'all_columns':set(shown)};sigs[(r['top'],frozenset(ss['pair']),frozenset(ss['triple']))].append(a['id']);aa[r['A']]+=1
 if r['top'] in {r[k] for k in 'ABCD'}:overlap.append(a['id'])
 for key,gs in ss.items():
  road=[sum(groups[z][0]%3==n for z in gs) for n in range(3)];odd=sum(groups[z][0]%2 for z in gs);cross={f'{k}_{par}':sum(groups[z][0]%3==k and groups[z][0]%2==(par=='odd') for z in gs) for k in range(3) for par in ('odd','even')};assert b['minimums'][key]=={'distinct_zodiacs':len(gs),'road_min':road,'odd_min':odd,'even_min':len(gs)-odd,'cross_road_parity_min':cross}
 for road in range(3):
  assert b['no_route_forced_incomplete_columns'][str(road)]==[name for name in ('single','pair','triple') if any(groups[z][0]%3==road for z in ss[name])]
  for par in ('odd','even'):assert b['no_road_parity_forced_incomplete_columns'][f'{road}_{par}']==[name for name in ('single','pair','triple') if any(groups[z][0]%3==road and groups[z][0]%2==(par=='odd') for z in ss[name])]
 for w in (35,40,45):
  pair={r['top'],r['A']};assert b['top_and_shared_both_absent_history'][str(w)]==sum(not pair&zset(row) for row in rows[:w]);peer=next(z for z in Z if z!=r['A'] and groups[z][0]%6==groups[r['A']][0]%6);pv=b['shared_missing_peer_present_history'][str(w)];assert pv['peer']==peer and pv['target_absent_peer_present_periods']==sum(r['A'] not in zset(row) and peer in zset(row) for row in rows[:w])
 count=[0,0,0,0];col=[0,0,0];both=0;rest=49-sum(len(groups[z]) for z in shown)
 for vec in product(*(range(len(groups[z])+1) for z in shown)):
  rem=6-sum(vec)
  if not 0<=rem<=rest:continue
  ways=comb(rest,rem)
  for z,k in zip(shown,vec):ways*=comb(len(groups[z]),k)
  active={z for z,k in zip(shown,vec) if k};done=[ss[k]<=active for k in ('single','pair','triple')];count[sum(done)]+=ways
  for i,k in enumerate(done):col[i]+=ways*k
  if done[1] and done[2]:both+=ways
 assert sum(count)==den;actual={'single_pct':col[0],'pair_pct':col[1],'triple_pct':col[2],'all_columns_pct':count[3],'no_column_pct':count[0],'pair_and_triple_pct':both};assert all(abs(100*v/den-b['ideal_model_probabilities_percent'][k])<1e-9 for k,v in actual.items())
ck(len(sigs)==36 and [x for x in sigs.values() if len(x)>1]==[['S01','S17','S18']] and len(overlap)==6 and set(aa)==set(Z) and aa['馬']==13 and dict(aa)==audit['shared_A_counts'] and hand['proposed_id']==m['human_choice']==audit['selected']['id']=='S01','38 human designs, 36 distinct slot structures, six overlaps, A concentration and ideal models independently enumerated')
sel=audit['selected'];ck(m['universe']==['牛','馬','豬','狗','鷄','虎'] and m['top']=='牛' and m['pair']==['馬','豬'] and m['triple']==['馬','狗','鷄'] and m['reserves']==['虎'] and sel['minimums']['triple']['road_min']==[1,2,0] and sel['minimums']['triple']['odd_min']==2 and sel['minimums']['all_columns']['road_min']==[2,2,1] and sel['minimums']['all_columns']['odd_min']==2 and sel['minimums']['all_columns']['even_min']==3,'manually fixed S01, tiger reserve outside slots, precise route/parity constraints')
ck(sel['no_route_forced_incomplete_columns']=={'0':['single','triple'],'1':['pair','triple'],'2':['pair']} and sel['no_road_parity_forced_incomplete_columns']=={'0_odd':['triple'],'0_even':['single'],'1_odd':['pair','triple'],'1_even':['triple'],'2_odd':[],'2_even':['pair']},'no-route and six crossed parity absence impacts independently reproduced')
other={x['id']:x for x in audit['candidates']};p=sel['ideal_model_probabilities_percent'];ck(other['S03']['ideal_model_probabilities_percent']==p and other['S20']['ideal_model_probabilities_percent']['all_columns_pct']>p['all_columns_pct'] and other['S20']['ideal_model_probabilities_percent']['no_column_pct']>p['no_column_pct'] and '馬' not in other['S07']['universe'] and other['S17']['roles']==sel['roles']==other['S18']['roles'],'S03/S07/S20 and reserve-only counterarguments retained, model does not prove prediction')
d=J('2026318-manual-decisions.json');previous=json.loads((F/'manual-site-decisions-through-317.json').read_text());ck(all(d['decisions'][k]==v for k,v in previous['decisions'].items()) and len(d['decisions'])==len(previous['decisions'])+1 and d['decisions']['2026318']['target']==2026318,'all prior manual decisions preserved, only 318 appended')
ck(all(not (D/'pre-registration'/f'2026{n}.json').exists() for n in (313,314,315,316,317,318)),'no retroactive 313–318 preregistrations')
page=(O/'2026318-page.html').read_text(encoding='utf8');pd=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));assert len(pd['rows'])==250 and pd['order']==Z
for a,row in zip(pd['rows'],reversed(rows[:250])):assert a==[int(row['period']),row['date'][5:10].replace('-','/') if row['date'] else '--/--',N(row),[Z.index(row[f'z{i}']) for i in range(1,7)],int(row['special']),Z.index(row['special_zodiac'])]
assert pd['n2z']=={str(n):Z.index(zn(n)) for n in range(1,50)};md=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));assert md['2026317']=={'U':[1,6,11,10,9,2],'top':1,'A':6,'B':11,'C':10,'D':9,'top_overlap_mode':'coverage'} and '<footer' not in page and 'footSrc' not in page
ck(True,'all 250 page rows, unknown dates, exact S01 roles, no footer and 49 mappings verified')
with TemporaryDirectory(prefix='318-reproduce-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026318-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026318-manual-decisions.json',t/'data/manual_site_decisions.json');env=dict(os.environ);env['POOL_VERSION']='v5.0';subprocess.run([sys.executable,str(O/'2026318-generator.py')],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026318-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
ck(True,'optimized generator reproducibly rebuilds page snapshot byte-for-byte')
ck(sha(O/'2026317-retrospective-original.md')==J('2026317-retrospective-report-qc.json')['report_sha256'] and sha(O/'2026318-analysis-local-original.md')==J('2026318-report-qc.json')['report_sha256'],'original report hashes match independent report QCs and remain byte-identical')
subprocess.run(['sha256sum','--quiet','--check','../2026317-retrospective-before.sha256'],cwd=F,check=True);ck(True,'all 38 frozen 317 files match original SHA-256 manifest')
for manifest in ('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256'):subprocess.run(['sha256sum','--quiet','--check',manifest],cwd=O,check=True)
ck(True,'eleven previous plus new immutable canonical evidence manifests verified')
print('OFFLINE 317/318 VERIFICATION PASS — no proof of source, predraw status, mechanism, prediction or returns')
