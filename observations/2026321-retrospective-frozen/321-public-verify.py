#!/usr/bin/env python3
"""Portable offline 320 published-display review and 321 manual evidence, from observations/.
No target draw values, scoring, prediction, official/clock/WeChat certification, or 319 blind claim.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
from tempfile import TemporaryDirectory
from math import comb
import csv,hashlib,json,os,re,shutil,subprocess,sys
O=Path(__file__).resolve().parent;D=O.parent;F=O/'2026320-retrospective-frozen';J=lambda n:json.loads((O/n).read_text(encoding='utf8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ck(x,m):
 if not x:raise AssertionError(m)
 checks.append(m);print('PASS',m)
def manifest(path,root):
 lines=path.read_text().splitlines();seen=set()
 for l in lines:
  h,n=l.split('  ',1);assert len(h)==64 and n not in seen;seen.add(n);p=(root/n).resolve();assert p.is_relative_to(root.resolve()) and p.is_file() and sha(p)==h,(path,n)
 return len(lines)
r=subprocess.run([sys.executable,str(O/'2026320-verify.py')],cwd=D,capture_output=True,text=True,timeout=120);ck(r.returncode==0 and 'OFFLINE 318/319/320 VERIFICATION PASS' in r.stdout,'prior portable verifier and 320 historical manifests pass; 319 remains unblinded and old clock caveat applies')
ck(manifest(O/'2026320-retrospective-before.sha256',F)==37 and sha(F/'actual-public-homepage-before.html')==sha(O/'2026320-page.html') and J('2026320-retrospective-freeze-receipt.json')['status']=='PASS_FROZEN_AFTER_USER_INPUT_NOT_PREDRAW_CERTIFICATION','37 320 public inputs and actual page frozen after receiving user outcome, not proof of pre-draw')
old=(O/'2026320-source-data.csv').read_bytes().splitlines(keepends=True);new=(O/'2026321-source-data.csv').read_bytes().splitlines(keepends=True);ck(len(old)==1051 and len(new)==1052 and old[0]==new[0] and old[1:]==new[2:] and all(x.endswith(b'\r\n') for x in new),'all 1050 older source rows byte-identical; exactly one user 320 row appended with CRLF')
rows=C(O/'2026321-source-data.csv');N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zn=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if zn(n)==z] for z in Z};u=J('2026320-user-result.json');assert len(rows)==1051 and len({r['period'] for r in rows})==1051 and [r['period'] for r in rows[:8]]==[str(x) for x in range(2026320,2026312,-1)] and all(r['date']=='' for r in rows[:8]);assert u['issue_user_specified'] and u['issue']==2026320 and u['date'] is None and u['six_plus_one_inferred_from_conversation_order'] and N(rows[0])==u['normal_numbers']==[14,17,32,34,24,46] and int(rows[0]['special'])==u['seventh_number']==20 and [zn(n) for n in N(rows[0])]==u['normal_zodiacs'] and zn(20)==u['seventh_zodiac']=='豬' and len(set(N(rows[0])+[20]))==7 and not u['official_authentication']
for row in rows[:250]:assert [row[f'z{i}'] for i in range(1,7)]==[zn(n) for n in N(row)] and row['special_zodiac']==zn(int(row['special']))
ck(True,'exact user-only 320 first six and separate seventh, issue supplied, date unknown, no 321 input row; current 49-code mapping checked')
six=lambda row:{row[f'z{i}'] for i in range(1,7)};seven=lambda row:six(row)|{row['special_zodiac']};actual=six(rows[0]);retro=J('2026320-retrospective-evidence.json');handold=json.loads((F/'320-38-handwritten.json').read_text());outcomes=retro['frozen_38_candidate_review']['original_order_candidates'];table=C(O/'2026320-retrospective-candidates.csv');assert len(handold['candidates'])==len(outcomes)==len(table)==38;distribution=Counter()
for x,y,c in zip(handold['candidates'],outcomes,table):
 role=x['roles'];slots=[{role['top']},{role['A'],role['B']},{role['A'],role['C'],role['D']}];counts=[len(k&actual) for k in slots];complete=sum(k<=actual for k in slots);distribution[complete]+=1;assert x['id']==y['id']==c['candidate_id'] and role==y['roles'] and x['reserves']==y['reserves'] and [k['present_count'] for k in y['slots']]==counts and y['complete_count']==complete==int(c['complete_columns']) and [c['single_progress'],c['double_progress'],c['triple_progress']]==[f'{n}/{d}' for n,d in zip(counts,(1,2,3))]
assert distribution=={0:8,1:28,2:2} and retro['plan_status']=='PUBLISHED_320_UNVERIFIED_DISPLAY' and [k['present_count'] for k in retro['settlement']['slots']]==[1,0,1] and retro['settlement']['complete_count']==1 and [table[6][k] for k in ('candidate_id','single_progress','double_progress','triple_progress','complete_columns')]==['U07','1/1','1/2','2/3','1']
ck(True,'all 38 frozen U candidates settled against user first six only: U01 1/1,0/2,1/3; U07 still single complete')
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠';ns=N(rows[0]);structure=retro['actual_structure'];assert structure['numbers']==ns and structure['road_0_1_2']==[sum(n%3==k for n in ns) for k in range(3)]==[1,2,3] and structure['odd_even']==[sum(n%2==1 for n in ns),sum(n%2==0 for n in ns)]==[1,5] and structure['red_blue_green']==[sum(wave(n)==x for n in ns) for x in ('紅','藍','綠')]==[3,1,2] and structure['sum']==sum(ns)==167 and structure['span']==max(ns)-min(ns)==32 and not (six(rows[0])&six(rows[1])) and seven(rows[0])&seven(rows[1])=={'虎'}
ck(True,'320 actual road, parity, colors, sum and span; 319/320 six-only versus seven-ball intersections kept distinct')
x=C(F/'445-source-through-311.csv');sets=[set(row['zodiacs'].split()) if row['usable']=='1' else None for row in x]+[seven(row) for row in reversed([r for r in rows if 2026312<=int(r['period'])<=2026320])];tr=[None]+[len(a&b) if a is not None and b is not None else None for a,b in zip(sets,sets[1:])];ends=[i for i in range(3,len(sets)) if tr[i-2:i+1]==[4,4,5]];follows=Counter(tr[i+1] for i in ends if i+1<len(tr));invalid=sum(None in tr[i-2:i+1] for i in range(3,len(sets)));repeat=J('2026320-retrospective-repeat445.json');ck(len(sets)==2501 and len(ends)==9 and follows=={2:2,3:3,4:3,5:1} and invalid==8 and repeat['valid_candidate_windows']==2490,'exact 4/4/5 deduplicated seven-ball identities independently scanned; eight invalid windows excluded')
e=J('2026321-evidence.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));assert e['history_rows']==1051 and e['latest_period']==2026320 and e['latest_date'] is None and e['history_sha256']==sha(O/'2026321-source-data.csv') and e['windows_overlap_not_independent_votes'] and not e['target_result_was_already_provided']
for z in Z:
 v=e['per_zodiac'][z];assert v['numbers']==G[z] and v['last_normal_age']==next(i for i,row in enumerate(rows) if z in six(row))
 for w in W:
  b=[[row[f'z{i}'] for i in range(1,7)] for row in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(a.count(z) for a in b),'periods':sum(z in a for a in b)}
 for lo,hi in blocks:
  b=[[row[f'z{i}'] for i in range(1,7)] for row in rows[lo:hi+1]];assert v['disjoint_age_blocks'][f'{lo}-{hi}']=={'balls':sum(a.count(z) for a in b),'periods':sum(z in a for a in b)}
ck(len(C(O/'2026321-zodiac-ledger.csv'))==12,'12 signs, eight first-six windows and five non-overlapping age blocks independently recounted')
ledger=C(O/'2026321-number-ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for item in ledger:
 n=int(item['number']);v=e['per_number'][str(n)];assert (v['zodiac'],v['road'],v['odd_even'],v['wave'],v['head'],v['tail'])==(zn(n),n%3,'奇' if n%2 else '偶',wave(n),n//10,n%10) and v['last_normal_age']==next(i for i,row in enumerate(rows) if n in N(row))
 for w in W:assert int(item[f'W{w}'])==v['window_counts'][str(w)]==sum(n in N(row) for row in rows[:w])
ck(True,'all 49 number attributes, age and eight normal windows independently recalculated; seventh excluded')
pairkey=lambda a,b:'|'.join(sorted((a,b),key=Z.index))
for w in W:
 rs=rows[:w];balls=[n for row in rs for n in N(row)];v=e['structural_windows'][str(w)];assert v['road_ball_counts']==[sum(n%3==k for n in balls) for k in range(3)] and v['odd_even_ball_counts']==[sum(n%2 for n in balls),sum(n%2==0 for n in balls)] and v['red_blue_green_ball_counts']==[sum(wave(n)==c for n in balls) for c in ('紅','藍','綠')] and v['head_ball_counts']==[sum(n//10==k for n in balls) for k in range(5)] and v['tail_ball_counts']==[sum(n%10==k for n in balls) for k in range(10)]
 for k in range(3):
  assert v[f'no_{k}road_periods']==sum(not any(n%3==k for n in N(row)) for row in rs) and v[f'at_most_one_{k}road_periods']==sum(sum(n%3==k for n in N(row))<=1 for row in rs)
  for par in ('odd','even'):assert v[f'no_{par}_{k}road_periods']==sum(not any(n%3==k and n%2==(par=='odd') for n in N(row)) for row in rs)
 for par in ('odd','even'):
  for limit in (1,2):assert v[f'at_most_{"one" if limit==1 else "two"}_{par}_periods']==sum(sum(n%2==(par=='odd') for n in N(row))<=limit for row in rs)
 for a,b in combinations(Z,2):assert e['joint_zodiac_absence_periods'][str(w)][pairkey(a,b)]==sum(not {a,b}&six(row) for row in rs)
 for z in Z:
  p=e['same_route_parity_peer_present_target_absent_periods'][str(w)][z];other=p['peer'];assert other!=z and G[other][0]%6==G[z][0]%6 and p['target_absent_peer_present_periods']==sum(z not in six(row) and other in six(row) for row in rs)
ledger=C(O/'2026321-joint-absence-ledger.csv');assert len(ledger)==66 and all(int(x[f'W{w}_both_absent'])==e['joint_zodiac_absence_periods'][str(w)][pairkey(x['sign_one'],x['sign_two'])] for x in ledger for w in (35,40,45));ck(True,'all 66 joint absences, same-class replacements and structural route/parity/wave/head/tail statistics recounted')
ck([e['joint_zodiac_absence_periods'][str(w)][pairkey('狗','蛇')] for w in (35,40,45)]==[11,13,14] and [e['joint_zodiac_absence_periods'][str(w)][pairkey('狗','豬')] for w in (35,40,45)]==[11,12,13] and [e['structural_windows'][str(w)]['at_most_one_1road_periods'] for w in (35,40,45)]==[6,7,9] and [e['structural_windows'][str(w)]['at_most_one_even_periods'] for w in (35,40,45)]==[3,3,3],'adverse V01 snake/pig alternatives and one-route versus odd-even tradeoffs explicitly checked')
hand=J('2026321-handwritten-design.json');audit=J('2026321-candidates.json');m=J('2026321-manual-decision.json');assert len(hand['candidates'])==len(audit['candidates'])==38
for key,name in [('handcrafted_candidates.json','2026321-handwritten-design.json'),('manual_decision.json','2026321-manual-decision.json'),('evidence.json','2026321-evidence.json')]:assert audit['input_sha256'][key]==sha(O/name)
den=comb(49,6);sigs=defaultdict(list);aa=Counter();overlap=[]
for x,y in zip(hand['candidates'],audit['candidates']):
 r=x['roles'];shown=list(dict.fromkeys(r[k] for k in ('top','A','B','C','D')));assert x['id']==y['id'] and r==y['roles'] and x['reserves']==y['reserves'] and len({r[k] for k in 'ABCD'})==4 and len(set(shown)|set(x['reserves']))==6 and not set(shown)&set(x['reserves']);ss={'single':{r['top']},'pair':{r['A'],r['B']},'triple':{r['A'],r['C'],r['D']},'all_columns':set(shown)};sigs[(r['top'],frozenset(ss['pair']),frozenset(ss['triple']))].append(x['id']);aa[r['A']]+=1
 if r['top'] in {r[k] for k in 'ABCD'}:overlap.append(x['id'])
 for key,gs in ss.items():
  road=[sum(G[z][0]%3==n for z in gs) for n in range(3)];odd=sum(G[z][0]%2 for z in gs);cross={f'{k}_{par}':sum(G[z][0]%3==k and G[z][0]%2==(par=='odd') for z in gs) for k in range(3) for par in ('odd','even')};assert y['minimums'][key]=={'distinct_zodiacs':len(gs),'road_min':road,'odd_min':odd,'even_min':len(gs)-odd,'cross_road_parity_min':cross}
 for road in range(3):
  assert y['no_route_forced_incomplete_columns'][str(road)]==[name for name in ('single','pair','triple') if any(G[z][0]%3==road for z in ss[name])]
  for par in ('odd','even'):assert y['no_road_parity_forced_incomplete_columns'][f'{road}_{par}']==[name for name in ('single','pair','triple') if any(G[z][0]%3==road and G[z][0]%2==(par=='odd') for z in ss[name])]
 for w in (35,40,45):assert y['top_and_shared_both_absent_history'][str(w)]==sum(not {r['top'],r['A']}&six(row) for row in rows[:w])
 count=[0,0,0,0];col=[0,0,0];both=0;rest=49-sum(len(G[z]) for z in shown)
 for vec in product(*(range(len(G[z])+1) for z in shown)):
  rem=6-sum(vec)
  if not 0<=rem<=rest:continue
  ways=comb(rest,rem)
  for z,k in zip(shown,vec):ways*=comb(len(G[z]),k)
  active={z for z,k in zip(shown,vec) if k};done=[ss[k]<=active for k in ('single','pair','triple')];count[sum(done)]+=ways
  for i,k in enumerate(done):col[i]+=ways*k
  if done[1] and done[2]:both+=ways
 assert sum(count)==den;model={'single_pct':col[0],'pair_pct':col[1],'triple_pct':col[2],'all_columns_pct':count[3],'no_column_pct':count[0],'pair_and_triple_pct':both};assert all(abs(100*v/den-y['ideal_model_probabilities_percent'][k])<1e-9 for k,v in model.items())
ck(len(sigs)==36 and [x for x in sigs.values() if len(x)>1]==[['V01','V17','V18']] and len(overlap)==6 and set(aa)==set(Z) and aa['蛇']==16 and dict(aa)==audit['shared_A_counts'] and hand['proposed_id']==m['human_choice']==audit['selected']['id']=='V01','38 manual designs, 36 structures, six overlaps and ideal-only models independently enumerated; not independent predictions')
sel=audit['selected'];ck(m['universe']==['狗','蛇','鷄','羊','馬','豬'] and m['top']=='狗' and m['pair']==['蛇','鷄'] and m['triple']==['蛇','羊','馬'] and m['reserves']==['豬'] and sel['minimums']['pair']['road_min']==[0,1,1] and sel['minimums']['pair']['even_min']==2 and sel['minimums']['triple']['road_min']==[1,1,1] and sel['minimums']['all_columns']['road_min']==[2,2,1] and (sel['minimums']['all_columns']['odd_min'],sel['minimums']['all_columns']['even_min'])==(2,3),'V01 roles, reserve-only pig, double-even pair, three-route triple and full-column minimums')
ck(sel['no_route_forced_incomplete_columns']=={'0':['single','triple'],'1':['pair','triple'],'2':['pair','triple']} and sel['no_road_parity_forced_incomplete_columns']=={'0_odd':['single'],'0_even':['triple'],'1_odd':['triple'],'1_even':['pair'],'2_odd':[],'2_even':['pair','triple']},'3 route and 6 crossed-parity absence matrices independently reproduced')
L={x['id']:x for x in audit['candidates']};p=sel['ideal_model_probabilities_percent'];oldmodel=retro['ideal_model_only'];ck(L['V06']['roles']['A']=='豬' and L['V06']['ideal_model_probabilities_percent']==p and L['V10']['roles']['A']=='馬' and L['V10']['minimums']['pair']['road_min']==[0,2,0] and L['V10']['ideal_model_probabilities_percent']['pair_pct']>p['pair_pct'] and L['V10']['ideal_model_probabilities_percent']['no_column_pct']<p['no_column_pct'] and L['V20']['roles']['top']==L['V20']['roles']['A']=='蛇' and L['V20']['ideal_model_probabilities_percent']['all_columns_pct']>p['all_columns_pct'] and L['V20']['ideal_model_probabilities_percent']['no_column_pct']>p['no_column_pct'] and p['pair_pct']<oldmodel['column_complete_percent'][1] and p['no_column_pct']>oldmodel['zero_complete_percent'],'same-universe V06/V10/V20 and less favorable ideal-only comparisons retained; no real-mechanism inference')
d=J('2026321-manual-decisions.json');previous=J('2026320-manual-decisions.json');ck(all(d['decisions'][k]==v for k,v in previous['decisions'].items()) and len(d['decisions'])==len(previous['decisions'])+1 and '2026319' not in d['decisions'] and d['decisions']['2026321']['target']==2026321,'all prior decisions preserved; no fictional historical 319 plan; only 321 appended')
ck(all(not (D/'pre-registration'/f'2026{n}.json').exists() for n in range(313,322)),'no retroactive 313–321 preregistrations')
page=(O/'2026321-page.html').read_text(encoding='utf8');pd=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));assert len(pd['rows'])==250 and pd['order']==Z
for a,row in zip(pd['rows'],reversed(rows[:250])):assert a==[int(row['period']),row['date'][5:10].replace('-','/') if row['date'] else '--/--',N(row),[Z.index(row[f'z{i}']) for i in range(1,7)],int(row['special']),Z.index(row['special_zodiac'])]
assert pd['n2z']=={str(n):Z.index(zn(n)) for n in range(1,50)};md=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));assert md['2026320']=={'U':[10,5,9,7,6,11],'top':10,'A':5,'B':9,'C':7,'D':6,'top_overlap_mode':'coverage'} and '2026318' not in md and '<footer' not in page and 'footSrc' not in page
ck(True,'250 page rows, unknown dates, V01 target mapping and no-footer design verified')
with TemporaryDirectory(prefix='321-reproduce-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026321-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026321-manual-decisions.json',t/'data/manual_site_decisions.json');env=dict(os.environ);env['POOL_VERSION']='v5.0';subprocess.run([sys.executable,str(O/'2026321-generator.py')],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026321-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes() and sha(O/'2026321-generator.py')==sha(O/'2026320-generator.py')
ck(True,'unchanged optimized generator reproduces both new page snapshots byte-for-byte')
for report,qc in [('2026320-retrospective-original.md','2026320-retrospective-report-qc.json'),('2026321-analysis-original.md','2026321-report-qc.json')]:assert sha(O/report)==J(qc)['report_sha256']
clar=J('2026320-retrospective-clarification-qc.json');assert clar['status']=='PASS' and sha(O/'2026320-wording-clarification-original.md')==clar['clarification_sha256'] and sha(O/'2026320-retrospective-original.md')==clar['original_report_sha256'] and sha(O/'2026320-retrospective-report-qc.json')==clar['original_qc_sha256'];original=(O/'2026320-retrospective-original.md').read_text();public=(O/'2026320-retrospective-public.md').read_text();assert '但狗仍缺，组合仍无完整栏。' in original and '但狗仍缺，二、三栏仍不完整，单羊仍完整。' in public and '合计完整1栏' in (O/'2026320-wording-clarification.md').read_text()
ck(True,'original 320 review/QC retained; publicly clarified U07 wording distinguishes single completed from two incomplete combination columns')
for name in ('2026320-retrospective-public.md','2026320-wording-clarification.md','2026321-analysis.md'):
 for link in re.findall(r'\]\(([^)]+)\)',(O/name).read_text()):
  if not link.startswith(('http://','https://','#')):assert (O/link).is_file(),(name,link)
ck(True,'new public review, wording correction and 321 analysis links all resolve')
ck(manifest(O/'2026321.sha256',O)>65,'all new immutable 320/321 evidence files match their new manifest; old manifests untouched')
print('OFFLINE 320 REVIEW / 321 DISPLAY VERIFICATION PASS — user-only 320, no 321 result or proof of source, predraw timing, actual mechanism, WeChat safety or returns')
