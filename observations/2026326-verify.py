#!/usr/bin/env python3
"""Portable offline verification: 325 after-result freeze/review and 326 manual display.
No target draw values read; no claim of official source, actual clock, mechanism or predictive edge.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
from tempfile import TemporaryDirectory
from math import comb
import csv,datetime,hashlib,json,os,re,shutil,subprocess,sys
O=Path(__file__).resolve().parent;D=O.parent;F=O/'2026325-retrospective-frozen';J=lambda n:json.loads((O/n).read_text(encoding='utf8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ck(x,m):
 if not x:raise AssertionError(m)
 checks.append(m);print('PASS',m)
def manifest(path,root):
 seen=set()
 for line in path.read_text().splitlines():
  h,n=line.split('  ',1);assert len(h)==64 and n not in seen;seen.add(n);p=(root/n).resolve();assert p.is_relative_to(root.resolve()) and p.is_file() and sha(p)==h,(path,n)
 return len(seen)
r=subprocess.run([sys.executable,str(O/'2026325-verify.py')],cwd=D,capture_output=True,text=True,timeout=120);ck(r.returncode==0 and 'OFFLINE 323 REVIEW / 324 UNBLINDED RECONSTRUCTION / 325 DISPLAY VERIFICATION PASS' in r.stdout,'prior portable 325 verification and old manifests pass')
ck(manifest(O/'2026325-retrospective-before.sha256',F)==39 and sha(F/'homepage-325-before.html')==sha(O/'2026325-page.html'),'325 actual display frozen after known outcome; hashes do not prove predraw timing')
old=(O/'2026325-source-data.csv').read_bytes().splitlines(keepends=True);new=(O/'2026326-source-data.csv').read_bytes().splitlines(keepends=True);ck(len(old)==1056 and len(new)==1057 and old[0]==new[0] and old[1:]==new[2:] and all(x.endswith(b'\r\n') for x in new),'exactly one user row appended while 1055 earlier records and CRLF remain byte-identical')
rows=C(O/'2026326-source-data.csv');N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zn=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if zn(n)==z] for z in Z};six=lambda row:{row[f'z{i}'] for i in range(1,7)};seven=lambda row:six(row)|{row['special_zodiac']};u=J('2026325-user-result.json')
assert len(rows)==1056 and rows[0]['period']=='2026325' and not rows[0]['date'] and u['date'] is None and u['issue_user_specified'] and u['six_plus_one_inferred_from_conversation_order'] and N(rows[0])==u['normal_numbers']==[41,37,10,1,27,17] and int(rows[0]['special'])==u['seventh_number']==3 and [zn(n) for n in N(rows[0])]==u['normal_zodiacs'] and zn(3)==u['seventh_zodiac']=='龍' and len(set(N(rows[0])+[3]))==7 and not u['official_authentication'] and not any(int(x['period'])>=2026326 for x in rows)
assert six(rows[1])&six(rows[0])==seven(rows[1])&seven(rows[0])=={'鷄'}
ck(True,'exact user-only 325 first six, separate seventh, unknown date, no target row, and 324–325 intersections')
retro=J('2026325-retrospective-evidence.json');hand=json.loads((F/'325-38-handwritten.json').read_text());assert retro['plan_status']=='PUBLISHED_325_UNVERIFIED_DISPLAY' and len(hand['candidates'])==38
cnt=Counter();actual=six(rows[0])
for x,y in zip(hand['candidates'],retro['frozen_38_candidate_review']['original_order_candidates']):
 r=x['roles'];slots=[{r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}];counts=[len(k&actual) for k in slots];complete=sum(k<=actual for k in slots);cnt[complete]+=1;assert x['id']==y['id'] and r==y['roles'] and x['reserves']==y['reserves'] and [k['present_count'] for k in y['slots']]==counts and y['complete_count']==complete
assert cnt=={0:12,1:26} and retro['choice']['id']=='Z01' and [x['present_count'] for x in retro['settlement']['slots']]==[1,0,1] and retro['settlement']['complete_count']==1 and retro['settlement']['reserve_only']==['豬'] and set(retro['actual_structure']['zodiac_ball_count'])=={'虎','馬','鷄','龍'}
ck(True,'all 38 original 325 plans independently settled: single 1/1, pair 0/2, triple 1/3; reserve does not fill')
# Rebuild dated adjacent pairs using the zodiac values recorded in each historical year, not 2026 mapping.
raw=C(F/'445-source-through-311.csv');assert len(raw)==2492 and raw[-1]['period']=='2026311';rawby={int(x['period']):x for x in raw};match=0
for x in rows:
 r=rawby.get(int(x['period']))
 if r:assert N(x)+[int(x['special'])]==list(map(int,r['numbers'].split())) and [x[f'z{i}'] for i in range(1,7)]+[x['special_zodiac']]==r['zodiacs'].split();match+=1
assert match==1042
records=[(int(x['period']),x['date'],x['zodiacs'].split(),x['usable']=='1') for x in raw]
for x in reversed(rows):
 p=int(x['period'])
 if 2026312<=p<=2026325:records.append((p,x['date'],[x[f'z{i}'] for i in range(1,7)]+[x['special_zodiac']],True))
assert len(records)==2506 and records[-1][0]==2026325
def adjacent(x,y):
 p,q=x[0],y[0]
 if p//1000==q//1000:return q%1000==p%1000+1
 if q//1000==p//1000+1 and q%1000==1:
  try:return (datetime.date.fromisoformat(y[1])-datetime.date.fromisoformat(x[1])).days==1
  except ValueError:return False
 return False
V=[];bad=[]
for p,q in zip(records,records[1:]):
 if not p[3] or not q[3] or not adjacent(p,q):bad.append((p[0],q[0]));continue
 p6,p7,q6,q7=set(p[2][:6]),set(p[2]),set(q[2][:6]),set(q[2]);V.append({'p':p[0],'q':q[0],'p6':p6,'p7':p7,'q6':q6,'q7':q7,'m6':sorted(Counter(p[2][:6]).values(),reverse=True),'m7':sorted(Counter(p[2]).values(),reverse=True),'s6':len(p6&q6),'s76':len(p7&q6),'s7':len(p7&q7)})
assert len(V)==2501 and len(bad)==4 and max(x['q'] for x in V)==2026325
study=J('2026326-four-sign-study.json');expl=J('2026326-four-sign-conjoint.json');arr=[x for x in V if x['p']>=2024001];dist=lambda xs,k:[sum(v[k]==i for v in xs) for i in range(5)]
normal=[x for x in arr if len(x['p6'])==4];seven4=[x for x in arr if len(x['p7'])==4];both=[x for x in arr if len(x['p6'])==len(x['p7'])==4];shape=[x for x in both if x['m6']==[2,2,1,1] and x['m7']==[2,2,2,1]]
assert len(normal)==201 and dist(normal,'s6')==[18,65,80,33,5] and len(seven4)==67 and dist(seven4,'s76')==[6,25,24,12,0] and dist(seven4,'s7')==[6,18,27,14,2]
assert len(both)==48 and dist(both,'s6')==[5,18,17,8,0] and dist(both,'s7')==[5,13,19,9,2] and len(shape)==31 and dist(shape,'s6')==[3,10,12,6,0] and dist(shape,'s7')==[3,7,13,6,2] and not [x for x in V if x['p6']=={'虎','馬','鷄','龍'}]
assert expl['groups']['2024plus']['next_normal_repeat']=={'n':48,'counts':[5,18,17,8,0]} and expl['groups']['2024plus']['next_seven_repeat']=={'n':48,'counts':[5,13,19,9,2]} and study['source_sha256']==sha(F/'445-source-through-311.csv')
ck(True,'four-sign marginal and exploratory joint counts independently reconstructed with year-correct identities and invalid adjacency excluded')
for n in (6,7):
 sizes=[4,5,4,4];outside=32;exact=[]
 for k in range(5):
  total=0
  for ids in combinations(range(4),k):
   cap=outside+sum(sizes[i] for i in ids)
   for j in range(k+1):
    for absent in combinations(ids,j):total+=(-1)**j*comb(cap-sum(sizes[i] for i in absent),n)
  exact.append(total)
 v=study['ideal_independent_49_model'][str(n)];assert exact==v['exact_counts'] and sum(exact)==v['denominator']==comb(49,n)
pairs=C(O/'2026326-four-sign-pairs.csv');expected=[x for x in V if len(x['p6'])==4 or len(x['p7'])==4];assert len(pairs)==len(expected)
for x,y in zip(pairs,expected):assert (int(x['prev']),int(x['next']))==(y['p'],y['q']) and set(x['prev6'].split())==y['p6'] and set(x['prev7'].split())==y['p7'] and set(x['next6'].split())==y['q6'] and set(x['next7'].split())==y['q7'] and [int(x[k]) for k in ('six_six_count','seven_six_count','seven_seven_count')]==[y['s6'],y['s76'],y['s7']]
ck(True,'six- and seven-ball fair models independently counted and every historical four-sign pair matched')
e=J('2026326-evidence.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));assert e['history_rows']==1056 and e['latest_period']==2026325 and e['latest_date'] is None and e['history_sha256']==sha(O/'2026326-source-data.csv') and not e['target_result_was_already_provided']
for z in Z:
 v=e['per_zodiac'][z];assert v['numbers']==G[z] and v['last_normal_age']==next(i for i,row in enumerate(rows) if z in six(row))
 for w in W:
  b=[[row[f'z{i}'] for i in range(1,7)] for row in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(a.count(z) for a in b),'periods':sum(z in a for a in b)}
 for lo,hi in blocks:
  b=[[row[f'z{i}'] for i in range(1,7)] for row in rows[lo:hi+1]];assert v['disjoint_age_blocks'][f'{lo}-{hi}']=={'balls':sum(a.count(z) for a in b),'periods':sum(z in a for a in b)}
ck(len(C(O/'2026326-zodiac-ledger.csv'))==12,'12 signs, eight first-six windows and non-overlapping age blocks independently recounted')
ledger=C(O/'2026326-number-ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for item in ledger:
 n=int(item['number']);v=e['per_number'][str(n)];assert v['zodiac']==zn(n) and v['road']==n%3 and v['odd_even']==('奇' if n%2 else '偶') and v['last_normal_age']==next(i for i,row in enumerate(rows) if n in N(row))
 for w in W:assert int(item[f'W{w}'])==v['window_counts'][str(w)]==sum(n in N(row) for row in rows[:w])
ck(True,'49 number attributes, first-six ages and windows independently recounted; seventh excluded')
pairkey=lambda a,b:'|'.join(sorted((a,b),key=Z.index))
for w in W:
 rs=rows[:w]
 for x,y in combinations(Z,2):assert e['joint_zodiac_absence_periods'][str(w)][pairkey(x,y)]==sum(not {x,y}&six(row) for row in rs)
 for z in Z:
  p=e['same_route_parity_peer_present_target_absent_periods'][str(w)][z];other=p['peer'];assert other!=z and G[other][0]%6==G[z][0]%6 and p['target_absent_peer_present_periods']==sum(z not in six(row) and other in six(row) for row in rs)
ledger=C(O/'2026326-joint-absence-ledger.csv');assert len(ledger)==66 and all(int(x[f'W{w}_both_absent'])==e['joint_zodiac_absence_periods'][str(w)][pairkey(x['sign_one'],x['sign_two'])] for x in ledger for w in (35,40,45))
ck([e['joint_zodiac_absence_periods'][str(w)][pairkey('羊','虎')] for w in (35,40,45)]==[16,16,18] and [e['structural_windows'][str(w)]['no_odd_2road_periods'] for w in (35,40,45)]==[19,19,21] and [e['structural_windows'][str(w)]['no_even_0road_periods'] for w in (35,40,45)]==[17,19,21],'all 66 joint absences and replacement counts, with selected concentration warnings, recounted')
hand=J('2026326-handwritten-design.json');audit=J('2026326-candidates.json');m=J('2026326-manual-decision.json');assert len(hand['candidates'])==len(audit['candidates'])==38;den=comb(49,6);sigs=defaultdict(list);aa=Counter();overlap=[]
for x,y in zip(hand['candidates'],audit['candidates']):
 r=x['roles'];shown=list(dict.fromkeys(r[k] for k in ('top','A','B','C','D')));assert x['id']==y['id'] and r==y['roles'] and x['reserves']==y['reserves'] and len({r[k] for k in 'ABCD'})==4 and len(set(shown)|set(x['reserves']))==6 and not set(shown)&set(x['reserves']);ss={'single':{r['top']},'pair':{r['A'],r['B']},'triple':{r['A'],r['C'],r['D']},'all_columns':set(shown)};sigs[(r['top'],frozenset(ss['pair']),frozenset(ss['triple']))].append(x['id']);aa[r['A']]+=1
 if r['top'] in {r[k] for k in 'ABCD'}:overlap.append(x['id'])
 for key,gs in ss.items():
  road=[sum(G[z][0]%3==n for z in gs) for n in range(3)];odd=sum(G[z][0]%2 for z in gs);cross={f'{k}_{par}':sum(G[z][0]%3==k and G[z][0]%2==(par=='odd') for z in gs) for k in range(3) for par in ('odd','even')};assert y['minimums'][key]=={'distinct_zodiacs':len(gs),'road_min':road,'odd_min':odd,'even_min':len(gs)-odd,'cross_road_parity_min':cross}
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
ck(len(sigs)==36 and [x for x in sigs.values() if len(x)>1]==[['AA01','AA08','AA09']] and len(overlap)==33 and set(aa)==set(Z) and aa['虎']==14 and hand['proposed_id']==m['human_choice']==audit['selected']['id']=='AA01','38 manual designs, 36 structures and all ideal models independently enumerated without ranking')
sel=audit['selected'];model=sel['ideal_model_probabilities_percent'];alt=audit['candidates'][1]['ideal_model_probabilities_percent'];ck(m['universe']==['羊','虎','馬','兔','龍','蛇'] and m['top']=='羊' and m['pair']==['虎','羊'] and m['triple']==['虎','馬','兔'] and m['reserves']==['龍','蛇'] and sel['minimums']['pair']['road_min']==[1,0,1] and sel['minimums']['triple']['road_min']==[0,2,1] and sel['minimums']['all_columns']['road_min']==[1,2,1] and (sel['minimums']['all_columns']['odd_min'],sel['minimums']['all_columns']['even_min'])==(2,2) and round(model['no_column_pct'],4)==53.7549 and round(alt['no_column_pct'],4)==44.5211,'AA01 exact roles, reserve-only dragon/snake, 4 identities, necessary minima and higher zero-column baseline')
d=J('2026326-manual-decisions.json');previous=J('2026325-manual-decisions.json');ck(all(d['decisions'][k]==v for k,v in previous['decisions'].items()) and len(d['decisions'])==len(previous['decisions'])+1 and '2026324' not in d['decisions'] and d['decisions']['2026326']['target']==2026326,'all earlier decisions preserved; 324 reconstruction not fabricated as published')
page=(O/'2026326-page.html').read_text(encoding='utf8');pd=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));assert len(pd['rows'])==250 and pd['order']==Z
for p,row in zip(pd['rows'],reversed(rows[:250])):assert p==[int(row['period']),row['date'][5:10].replace('-','/') if row['date'] else '--/--',N(row),[Z.index(row[f'z{i}']) for i in range(1,7)],int(row['special']),Z.index(row['special_zodiac'])]
md=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));assert md['2026325']=={'U':[7,2,6,3,4,5],'top':7,'A':2,'B':7,'C':6,'D':3,'top_overlap_mode':'concentrated'} and '2026323' not in md and '<footer' not in page and 'footSrc' not in page
ck(True,'250 page rows, unknown dates, AA01 target mapping and no fabricated 324 plan')
with TemporaryDirectory(prefix='326-reproduce-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026326-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026326-manual-decisions.json',t/'data/manual_site_decisions.json');env=dict(os.environ);env['POOL_VERSION']='v5.0';subprocess.run([sys.executable,str(O/'2026326-generator.py')],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026326-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes() and sha(O/'2026326-generator.py')==sha(O/'2026325-generator.py')
ck(True,'unchanged optimized generator reproduces both new page snapshots byte-for-byte')
for name in ('2026325-retrospective-public.md','2026326-four-sign-public.md','2026326-analysis.md'):
 for link in re.findall(r'\]\(([^)]+)\)',(O/name).read_text()):
  if not link.startswith(('http://','https://','#')):assert (O/link).is_file(),(name,link)
ck(True,'all public 325 review, four-sign study and 326 analysis local links resolve')
ck(manifest(O/'2026326.sha256',O)>70,'all new immutable 325–326 evidence files match the new manifest')
print('OFFLINE 325 REVIEW / FOUR-SIGN STUDY / 326 DISPLAY VERIFICATION PASS — not proof of official source, predraw timing, actual mechanism, WeChat safety, predictive advantage or returns')
