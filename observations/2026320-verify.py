#!/usr/bin/env python3
"""Portable offline 318 review, unblinded 319 comparison, 320 manual display and clock correction.
Run from any directory: python3 observations/2026320-verify.py
No target-result lookup, forecast ranking, timing/source/WeChat or real-fairness certification.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
from tempfile import TemporaryDirectory
from math import comb
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
import csv,hashlib,json,os,re,shutil,subprocess,sys
O=Path(__file__).resolve().parent;D=O.parent;F18=O/'2026318-retrospective-frozen';F19=O/'2026319-reconstruction-frozen';J=lambda n:json.loads((O/n).read_text(encoding='utf8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
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
# Prior verifier's historical date-conflict semantic assertion, if any, is not adopted.
r=subprocess.run([sys.executable,str(O/'2026318-verify.py')],cwd=D,capture_output=True,text=True,timeout=90);ck(r.returncode==0 and 'OFFLINE 317/318 VERIFICATION PASS' in r.stdout,'previous offline data verifier and 12 frozen manifests pass; not clock/timing authentication')
ck(manifest(O/'2026318-retrospective-before.sha256',F18)==36 and manifest(O/'2026319-reconstruction-before.sha256',F19)==19,'36 published-318 inputs and 19 explicitly post-outcome-319 reconstruction inputs preserved')
old=(O/'2026318-source-data.csv').read_bytes().splitlines(keepends=True);new=(O/'2026320-source-data.csv').read_bytes().splitlines(keepends=True);ck(len(old)==1049 and len(new)==1051 and old[0]==new[0] and old[1:]==new[3:] and all(x.endswith(b'\r\n') for x in new),'1048 earlier source rows byte-identical, only user 318 and 319 appended with CRLF')
rows=C(O/'2026320-source-data.csv');N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zn=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if zn(n)==z] for z in Z};u18=J('2026318-user-result.json');u19=J('2026319-user-result.json');assert len(rows)==1050 and len({r['period'] for r in rows})==1050 and [r['period'] for r in rows[:7]]==[str(x) for x in range(2026319,2026312,-1)] and all(r['date']=='' for r in rows[:7])
for i,u,ns,sp in [(0,u19,[6,3,15,13,25,45],5),(1,u18,[10,36,2,9,26,37],38)]:assert u['issue_user_specified'] and u['date'] is None and u['six_plus_one_inferred_from_conversation_order'] and N(rows[i])==u['normal_numbers']==ns and int(rows[i]['special'])==u['seventh_number']==sp and [zn(n) for n in ns]==u['normal_zodiacs'] and zn(sp)==u['seventh_zodiac'] and len(set(ns+[sp]))==7
ck(True,'exact user-only 318/319 normal six plus separate seventh; specified issue and unknown dates')
assert u19['reconstruction_was_after_user_input'] and not u19['official_authentication'];v19=json.loads((F19/'319-reconstruction-manual.json').read_text());assert v19['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' and v19['target_user_result_already_seen'] and v19['selection_bias_cannot_be_excluded'];ck(True,'319 result already known before reconstruction; no published, blind, pre-draw or outcome-independent claim')
# Independently settle every frozen candidate from the correct first six; reserve and seventh excluded.
for period,f,fn,ns,expected,dist in [(318,F18,'318-38-handwritten.json',N(rows[1]),[0,1,3],{0:15,1:15,2:8}),(319,F19,'319-reconstruction-handwritten.json',N(rows[0]),[1,0,2],{0:9,1:27,2:2})]:
 raw=json.loads((f/fn).read_text());retro=J(f'2026{period}-retrospective-evidence.json');candidates=retro['frozen_38_candidate_review']['original_order_candidates'];assert len(raw['candidates'])==len(candidates)==38;actual={zn(n) for n in ns};distribution=Counter()
 for x,y in zip(raw['candidates'],candidates):
  role=x['roles'];slots=[{role['top']},{role['A'],role['B']},{role['A'],role['C'],role['D']}];counts=[len(s&actual) for s in slots];assert x['id']==y['id'] and x['roles']==y['roles'] and x['reserves']==y['reserves'] and [v['present_count'] for v in y['slots']]==counts and y['complete_count']==sum(ss<=actual for ss in slots);distribution[y['complete_count']]+=1
 assert distribution==dist and [v['present_count'] for v in retro['settlement']['slots']]==expected and retro['settlement']['complete_count']==1 and retro['plan_status']==('PUBLISHED_318' if period==318 else 'AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW')
ck(True,'318 real S01 0/1,1/2,3/3 and 319 post-outcome T01 1/1,0/2,2/3; all 76 comparisons independently settled')
assert [sum(n%3==k for n in N(rows[1])) for k in range(3)]==[2,2,2] and [sum(n%3==k for n in N(rows[0])) for k in range(3)]==[4,2,0] and [sum(n%2 for n in N(rows[0])),sum(n%2==0 for n in N(rows[0]))]==[5,1] and sum(N(rows[0]))==107
six=lambda row:{zn(n) for n in N(row)};seven=lambda row:six(row)|{row['special_zodiac']};ck(six(rows[0])&six(rows[1])==seven(rows[0])&seven(rows[1])=={'馬','狗'} and not (set(N(rows[0])+[int(rows[0]['special'])])&set(N(rows[1])+[int(rows[1]['special'])])),'318/319 structure and first-six/seven-ball identity intersections, no repeated number')
x=C(F18/'445-source-through-311.csv');sets=[set(row['zodiacs'].split()) if row['usable']=='1' else None for row in x]+[seven(row) for row in reversed([r for r in rows if 2026312<=int(r['period'])<=2026319])];tr=[None]+[len(a&b) if a is not None and b is not None else None for a,b in zip(sets,sets[1:])];ends=[i for i in range(3,len(sets)) if tr[i-2:i+1]==[4,4,5]];follows=Counter(tr[i+1] for i in ends if i+1<len(tr));invalid=sum(None in tr[i-2:i+1] for i in range(3,len(sets)));repeat=J('2026319-retrospective-repeat445.json');ck(len(sets)==2500 and len(ends)==9 and follows=={2:2,3:3,4:3,5:1} and invalid==8 and repeat['valid_candidate_windows']==2489,'exact 4/4/5 deduplicated seven-ball transitions independently scanned; invalid windows excluded')
e=J('2026320-evidence.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));assert e['history_rows']==1050 and e['latest_period']==2026319 and e['latest_date'] is None and e['history_sha256']==sha(O/'2026320-source-data.csv') and e['windows_overlap_not_independent_votes'] and not e['target_result_was_already_provided']
for z in Z:
 v=e['per_zodiac'][z];gs=set(G[z]);assert v['numbers']==G[z] and v['last_normal_age']==next(i for i,row in enumerate(rows) if gs.intersection(N(row)))
 for w in W:
  b=[N(row) for row in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(sum(n in gs for n in a) for a in b),'periods':sum(any(n in gs for n in a) for a in b)}
 for lo,hi in blocks:
  b=[N(row) for row in rows[lo:hi+1]];assert v['disjoint_age_blocks'][f'{lo}-{hi}']=={'balls':sum(sum(n in gs for n in a) for a in b),'periods':sum(any(n in gs for n in a) for a in b)}
ck(len(C(O/'2026320-zodiac-ledger.csv'))==12,'12 signs, eight normal-only windows and five disjoint age blocks independently recounted')
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠';ledger=C(O/'2026320-number-ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for item in ledger:
 n=int(item['number']);v=e['per_number'][str(n)];assert (v['zodiac'],v['road'],v['odd_even'],v['wave'],v['head'],v['tail'])==(zn(n),n%3,'奇' if n%2 else '偶',wave(n),n//10,n%10) and v['last_normal_age']==next(i for i,row in enumerate(rows) if n in N(row))
 for w in W:assert int(item[f'W{w}'])==v['window_counts'][str(w)]==sum(n in N(row) for row in rows[:w])
ck(True,'all 49 number attributes, age and eight normal windows independently recalculated')
pairkey=lambda a,b:'|'.join(sorted((a,b),key=Z.index));zset=lambda row:{zn(n) for n in N(row)}
for w in W:
 rs=rows[:w];balls=[n for row in rs for n in N(row)];v=e['structural_windows'][str(w)];assert v['road_ball_counts']==[sum(n%3==k for n in balls) for k in range(3)] and v['odd_even_ball_counts']==[sum(n%2 for n in balls),sum(n%2==0 for n in balls)] and v['red_blue_green_ball_counts']==[sum(wave(n)==c for n in balls) for c in ('紅','藍','綠')] and v['head_ball_counts']==[sum(n//10==k for n in balls) for k in range(5)] and v['tail_ball_counts']==[sum(n%10==k for n in balls) for k in range(10)]
 for k in range(3):
  assert v[f'no_{k}road_periods']==sum(not any(n%3==k for n in N(row)) for row in rs)
  for par in ('odd','even'):assert v[f'no_{par}_{k}road_periods']==sum(not any(n%3==k and n%2==(par=='odd') for n in N(row)) for row in rs)
 for a,b in combinations(Z,2):assert e['joint_zodiac_absence_periods'][str(w)][pairkey(a,b)]==sum(not {a,b}&zset(row) for row in rs)
 for z in Z:
  p=e['same_route_parity_peer_present_target_absent_periods'][str(w)][z];other=p['peer'];assert other!=z and G[other][0]%6==G[z][0]%6 and p['target_absent_peer_present_periods']==sum(z not in zset(row) and other in zset(row) for row in rs)
ledger=C(O/'2026320-joint-absence-ledger.csv');assert len(ledger)==66 and all(int(x[f'W{w}_both_absent'])==e['joint_zodiac_absence_periods'][str(w)][pairkey(x['sign_one'],x['sign_two'])] for x in ledger for w in (35,40,45));ck(True,'all 66 joint absences, same-class replacements and structural route/parity/wave/head/tail statistics recounted')
ck([e['joint_zodiac_absence_periods'][str(w)]['兔|羊'] for w in (35,40,45)]==[11,13,15] and [e['joint_zodiac_absence_periods'][str(w)]['牛|鷄'] for w in (35,40,45)]==[10,11,13] and [e['same_route_parity_peer_present_target_absent_periods'][str(w)]['兔']['target_absent_peer_present_periods'] for w in (35,40,45)]==[10,12,12],'adverse U01 sheep+rabbit absence and rabbit/chicken substitution explicitly checked')
hand=J('2026320-handwritten-design.json');audit=J('2026320-candidates.json');m=J('2026320-manual-decision.json');assert len(hand['candidates'])==len(audit['candidates'])==38
for key,name in [('handcrafted_candidates.json','2026320-handwritten-design.json'),('manual_decision.json','2026320-manual-decision.json'),('evidence.json','2026320-evidence.json')]:assert audit['input_sha256'][key]==sha(O/name)
den=comb(49,6);sigs=defaultdict(list);aa=Counter();overlap=[]
for x,y in zip(hand['candidates'],audit['candidates']):
 r=x['roles'];shown=list(dict.fromkeys(r[k] for k in ('top','A','B','C','D')));assert x['id']==y['id'] and r==y['roles'] and x['reserves']==y['reserves'] and len({r[k] for k in 'ABCD'})==4 and len(set(shown)|set(x['reserves']))==6 and not set(shown)&set(x['reserves']);ss={'single':{r['top']},'pair':{r['A'],r['B']},'triple':{r['A'],r['C'],r['D']},'all_columns':set(shown)};sigs[(r['top'],frozenset(ss['pair']),frozenset(ss['triple']))].append(x['id']);aa[r['A']]+=1
 if r['top'] in {r[k] for k in 'ABCD'}:overlap.append(x['id'])
 for key,gs in ss.items():
  road=[sum(G[z][0]%3==n for z in gs) for n in range(3)];odd=sum(G[z][0]%2 for z in gs);cross={f'{k}_{par}':sum(G[z][0]%3==k and G[z][0]%2==(par=='odd') for z in gs) for k in range(3) for par in ('odd','even')};assert y['minimums'][key]=={'distinct_zodiacs':len(gs),'road_min':road,'odd_min':odd,'even_min':len(gs)-odd,'cross_road_parity_min':cross}
 for road in range(3):
  assert y['no_route_forced_incomplete_columns'][str(road)]==[name for name in ('single','pair','triple') if any(G[z][0]%3==road for z in ss[name])]
  for par in ('odd','even'):assert y['no_road_parity_forced_incomplete_columns'][f'{road}_{par}']==[name for name in ('single','pair','triple') if any(G[z][0]%3==road and G[z][0]%2==(par=='odd') for z in ss[name])]
 for w in (35,40,45):assert y['top_and_shared_both_absent_history'][str(w)]==sum(not {r['top'],r['A']}&zset(row) for row in rows[:w])
 count=[0,0,0,0];col=[0,0,0];both=0;rest=49-sum(len(G[z]) for z in shown)
 for vec in product(*(range(len(G[z])+1) for z in shown)):
  rem=6-sum(vec)
  if not 0<=rem<=rest:continue
  ways=comb(rest,rem)
  for z,k in zip(shown,vec):ways*=comb(len(G[z]),k)
  active={z for z,k in zip(shown,vec) if k};done=[ss[k]<=active for k in ('single','pair','triple')];count[sum(done)]+=ways
  for i,k in enumerate(done):col[i]+=ways*k
  if done[1] and done[2]:both+=ways
 assert sum(count)==den;actual={'single_pct':col[0],'pair_pct':col[1],'triple_pct':col[2],'all_columns_pct':count[3],'no_column_pct':count[0],'pair_and_triple_pct':both};assert all(abs(100*v/den-y['ideal_model_probabilities_percent'][k])<1e-9 for k,v in actual.items())
ck(len(sigs)==36 and [x for x in sigs.values() if len(x)>1]==[['U01','U17','U18']] and len(overlap)==6 and set(aa)==set(Z) and aa['兔']==14 and dict(aa)==audit['shared_A_counts'] and hand['proposed_id']==m['human_choice']==audit['selected']['id']=='U01','38 manual designs, 36 slot structures, six overlaps and ideal-only models independently enumerated')
sel=audit['selected'];ck(m['universe']==['羊','兔','馬','狗','蛇','猴'] and m['top']=='羊' and m['pair']==['兔','馬'] and m['triple']==['兔','狗','蛇'] and m['reserves']==['猴'] and sel['minimums']['pair']['road_min']==[0,2,0] and sel['minimums']['triple']['road_min']==[1,1,1] and sel['minimums']['all_columns']['road_min']==[2,2,1] and (sel['minimums']['all_columns']['odd_min'],sel['minimums']['all_columns']['even_min'])==(2,3),'U01 roles, reserve, two distinct 1-route pair and three-route triple')
ck(sel['no_route_forced_incomplete_columns']=={'0':['single','triple'],'1':['pair','triple'],'2':['triple']} and sel['no_road_parity_forced_incomplete_columns']=={'0_odd':['triple'],'0_even':['single'],'1_odd':['pair'],'1_even':['pair','triple'],'2_odd':[],'2_even':['triple']},'3 route and 6 crossed-parity absence matrices independently reproduced')
L={x['id']:x for x in audit['candidates']};p=sel['ideal_model_probabilities_percent'];ck(L['U03']['roles']['B']=='蛇' and L['U08']['roles']['A']=='馬' and L['U08']['ideal_model_probabilities_percent']['triple_pct']>p['triple_pct'] and L['U08']['ideal_model_probabilities_percent']['no_column_pct']<p['no_column_pct'] and L['U20']['roles']['top']==L['U20']['roles']['A']=='兔' and L['U20']['ideal_model_probabilities_percent']['all_columns_pct']>p['all_columns_pct'] and L['U20']['ideal_model_probabilities_percent']['no_column_pct']>p['no_column_pct'],'same-universe U03/U08/U20 and adverse ideal-only counterexamples retained')
d=J('2026320-manual-decisions.json');previous=json.loads((F18/'manual-site-decisions-through-318.json').read_text());ck(all(d['decisions'][k]==v for k,v in previous['decisions'].items()) and len(d['decisions'])==len(previous['decisions'])+1 and '2026319' not in d['decisions'] and d['decisions']['2026320']['target']==2026320,'prior decisions preserved; no fictional historical 319 plan; only 320 appended')
ck(all(not (D/'pre-registration'/f'2026{n}.json').exists() for n in range(313,321)),'no retroactive 313–320 preregistrations')
page=(O/'2026320-page.html').read_text(encoding='utf8');pd=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));assert len(pd['rows'])==250 and pd['order']==Z
for a,row in zip(pd['rows'],reversed(rows[:250])):assert a==[int(row['period']),row['date'][5:10].replace('-','/') if row['date'] else '--/--',N(row),[Z.index(row[f'z{i}']) for i in range(1,7)],int(row['special']),Z.index(row['special_zodiac'])]
assert pd['n2z']=={str(n):Z.index(zn(n)) for n in range(1,50)};md=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));assert md['2026319']=={'U':[7,3,6,10,5,8],'top':7,'A':3,'B':6,'C':10,'D':5,'top_overlap_mode':'coverage'} and '2026318' not in md and '<footer' not in page and 'footSrc' not in page
ck(True,'250 page rows, unknown dates, U01 target mapping and unchanged no-footer design verified')
with TemporaryDirectory(prefix='320-reproduce-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026320-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026320-manual-decisions.json',t/'data/manual_site_decisions.json');env=dict(os.environ);env['POOL_VERSION']='v5.0';subprocess.run([sys.executable,str(O/'2026320-generator.py')],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026320-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
ck(True,'unchanged optimized generator reproduces both page snapshots byte-for-byte')
for report,qc in [('2026318-retrospective-original.md','2026318-retrospective-report-qc.json'),('2026319-reconstruction-original.md','2026319-reconstruction-report-qc.json'),('2026319-retrospective-original.md','2026319-retrospective-report-qc.json'),('2026320-analysis-local-original.md','2026320-report-qc.json')]:assert sha(O/report)==J(qc)['report_sha256']
clock=J('2026318-clock-discrepancy.json');utc=datetime.fromisoformat(clock['runtime_clock_utc_raw']);assert utc.astimezone(ZoneInfo('Asia/Shanghai')).isoformat()==clock['runtime_clock_asia_shanghai_raw'] and utc.astimezone(ZoneInfo('Asia/Shanghai')).utcoffset()==timedelta(hours=8) and "'supplied_session_local_date':'2026-10-13'" in (O/'2026318-clock-source.py').read_text();cor=(O/'2026318-clock-correction.md').read_text();assert '不是时间冲突' in cor and '不能据此把所谓“会话日期与环境时钟冲突”当成已经证实' in cor and '不证明日期语义正确，更不证明赛前' in cor and sha(O/'2026318-analysis-local-original.md') in cor and sha(O/'2026318-clock-discrepancy.json') in cor
ck(True,'raw UTC/Shanghai clock equality and hard-coded date independently checked; original files retained, correction not event authentication')
for name in ('2026318-retrospective-public.md','2026319-reconstruction.md','2026319-retrospective-public.md','2026320-analysis.md','2026318-clock-correction.md'):
 for link in re.findall(r'\]\(([^)]+)\)',(O/name).read_text()):
  if not link.startswith(('http://','https://','#')):assert (O/link).is_file(),(name,link)
ck(True,'public review, reconstruction, analysis and correction links all resolve')
ck(manifest(O/'2026320.sha256',O)>100,'all new immutable 318/319/320 evidence files match their new manifest; old manifests untouched')
print('OFFLINE 318/319/320 VERIFICATION PASS — 319 is an unblinded reconstruction; no proof of source, predraw timing, actual mechanism, WeChat safety or returns')
