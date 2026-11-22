#!/usr/bin/env python3
"""Portable offline verification: 323 actual display, 324 outcome-known reconstruction, 325 display.
No 325 draw values; no claim of 324 selection independence, official source, time or prediction.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
from tempfile import TemporaryDirectory
from math import comb
import csv,hashlib,json,os,re,shutil,subprocess,sys
O=Path(__file__).resolve().parent;D=O.parent;F1=O/'2026323-retrospective-frozen';F2=O/'2026324-reconstruction-frozen';J=lambda n:json.loads((O/n).read_text(encoding='utf8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ck(x,m):
 if not x:raise AssertionError(m)
 checks.append(m);print('PASS',m)
def manifest(path,root):
 seen=set()
 for l in path.read_text().splitlines():
  h,n=l.split('  ',1);assert len(h)==64 and n not in seen;seen.add(n);p=(root/n).resolve();assert p.is_relative_to(root.resolve()) and p.is_file() and sha(p)==h,(path,n)
 return len(seen)
r=subprocess.run([sys.executable,str(O/'2026323-verify.py')],cwd=D,capture_output=True,text=True,timeout=120);ck(r.returncode==0 and 'OFFLINE 321 REVIEW / 322 UNBLINDED RECONSTRUCTION / 323 DISPLAY VERIFICATION PASS' in r.stdout,'prior 323 portable verifier and earlier manifests pass')
ck(manifest(O/'2026323-retrospective-before.sha256',F1)==39 and manifest(O/'2026324-reconstruction-before.sha256',F2)==21 and sha(F1/'homepage-323-before.html')==sha(O/'2026323-page.html'),'323 actual display and 324 reconstruction frozen after known outcomes; hashes are not pre-draw proof')
old=(O/'2026323-source-data.csv').read_bytes().splitlines(keepends=True);new=(O/'2026325-source-data.csv').read_bytes().splitlines(keepends=True);ck(len(old)==1054 and len(new)==1056 and old[0]==new[0] and old[1:]==new[3:] and all(x.endswith(b'\r\n') for x in new),'two user rows appended while all 1053 earlier source rows remain byte-identical')
rows=C(O/'2026325-source-data.csv');N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zn=lambda n:Z[(7-n)%12];G={z:[n for n in range(1,50) if zn(n)==z] for z in Z};six=lambda row:{row[f'z{i}'] for i in range(1,7)};seven=lambda row:six(row)|{row['special_zodiac']};u323=J('2026323-user-result.json');u324=J('2026324-user-result.json')
assert len(rows)==1055 and len({r['period'] for r in rows})==1055 and [r['period'] for r in rows[:2]]==['2026324','2026323'] and all(not r['date'] for r in rows[:2])
for row,u,ns,sp in [(rows[1],u323,[33,8,2,9,15,41],47),(rows[0],u324,[19,4,14,12,21,34],43)]:
 assert u['date'] is None and u['issue_user_specified'] and u['six_plus_one_inferred_from_conversation_order'] and N(row)==u['normal_numbers']==ns and int(row['special'])==u['seventh_number']==sp and [zn(n) for n in ns]==u['normal_zodiacs'] and zn(sp)==u['seventh_zodiac'] and len(set(ns+[sp]))==7 and not u['official_authentication']
ck(True,'exact user-only 323 and 324 first six and separate seventh, with unknown dates')
retro1=J('2026323-retrospective-evidence.json');retro2=J('2026324-retrospective-evidence.json');h1=json.loads((F1/'323-38-handwritten.json').read_text());h2=json.loads((F2/'324-reconstruction-handwritten.json').read_text());assert retro1['plan_status']=='PUBLISHED_323_UNVERIFIED_DISPLAY' and retro2['plan_status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW'
for rr,hand,act,selected,exp,dist in [(retro1,h1,six(rows[1]),'X01',[0,2,1],{0:11,1:23,2:4}),(retro2,h2,six(rows[0]),'Y01',[1,1,1],{0:2,1:23,2:13})]:
 cand=rr['frozen_38_candidate_review']['original_order_candidates'];assert len(cand)==len(hand['candidates'])==38;cnt=Counter()
 for x,y in zip(hand['candidates'],cand):
  role=x['roles'];slots=[{role['top']},{role['A'],role['B']},{role['A'],role['C'],role['D']}];counts=[len(k&act) for k in slots];complete=sum(k<=act for k in slots);cnt[complete]+=1;assert x['id']==y['id'] and role==y['roles'] and x['reserves']==y['reserves'] and [k['present_count'] for k in y['slots']]==counts and y['complete_count']==complete
 assert cnt==dist and rr['choice']['id']==selected and [k['present_count'] for k in rr['settlement']['slots']]==exp
assert retro1['settlement']['complete_count']==retro2['settlement']['complete_count']==1 and retro1['settlement']['slots'][1]['complete'] and retro2['settlement']['slots'][0]['complete'] and retro2['settlement']['reserve_ball_count']==1 and h2['candidates'][0]['source_323_id']=='X29' and u324['target_result_already_supplied_before_324_reconstruction']
ck(True,'323 actually displayed 0/1,2/2,1/3 versus 324 unblinded reconstruction 1/1,1/2,1/3; all 76 rows independently settled')
assert six(rows[0])&six(rows[1])==seven(rows[0])&seven(rows[1])=={'蛇','狗'} and not (set(N(rows[0])+[43])&set(N(rows[1])+[47]));ck(True,'323/324 six-ball and seven-ball identity intersections both snake/dog; no repeated numbers')
x=C(F1/'445-source-through-311.csv');sets=[set(row['zodiacs'].split()) if row['usable']=='1' else None for row in x]+[seven(row) for row in reversed([r for r in rows if 2026312<=int(r['period'])<=2026324])];tr=[None]+[len(a&b) if a is not None and b is not None else None for a,b in zip(sets,sets[1:])];ends=[i for i in range(3,len(sets)) if tr[i-2:i+1]==[4,4,5]];follow=Counter(tr[i+1] for i in ends if i+1<len(tr));invalid=sum(None in tr[i-2:i+1] for i in range(3,len(sets)));repeat=J('2026324-retrospective-repeat445.json');ck(len(sets)==2505 and len(ends)==9 and follow=={2:2,3:3,4:3,5:1} and invalid==8 and repeat['valid_candidate_windows']==2494,'exact 4/4/5 seven-ball identity scan; eight invalid windows excluded')
e=J('2026325-evidence.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));assert e['history_rows']==1055 and e['latest_period']==2026324 and e['latest_date'] is None and e['history_sha256']==sha(O/'2026325-source-data.csv') and e['windows_overlap_not_independent_votes'] and not e['target_result_was_already_provided']
for z in Z:
 v=e['per_zodiac'][z];assert v['numbers']==G[z] and v['last_normal_age']==next(i for i,row in enumerate(rows) if z in six(row))
 for w in W:
  b=[[row[f'z{i}'] for i in range(1,7)] for row in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(a.count(z) for a in b),'periods':sum(z in a for a in b)}
 for lo,hi in blocks:
  b=[[row[f'z{i}'] for i in range(1,7)] for row in rows[lo:hi+1]];assert v['disjoint_age_blocks'][f'{lo}-{hi}']=={'balls':sum(a.count(z) for a in b),'periods':sum(z in a for a in b)}
ck(len(C(O/'2026325-zodiac-ledger.csv'))==12,'12 signs, eight first-six windows and five non-overlapping age blocks recounted')
ledger=C(O/'2026325-number-ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for item in ledger:
 n=int(item['number']);v=e['per_number'][str(n)];assert v['zodiac']==zn(n) and v['road']==n%3 and v['odd_even']==('奇' if n%2 else '偶') and v['last_normal_age']==next(i for i,row in enumerate(rows) if n in N(row))
 for w in W:assert int(item[f'W{w}'])==v['window_counts'][str(w)]==sum(n in N(row) for row in rows[:w])
ck(True,'49 number attributes, first-six ages and eight windows recounted; seventh excluded')
pairkey=lambda a,b:'|'.join(sorted((a,b),key=Z.index))
for w in W:
 rs=rows[:w]
 for x,y in combinations(Z,2):assert e['joint_zodiac_absence_periods'][str(w)][pairkey(x,y)]==sum(not {x,y}&six(row) for row in rs)
 for z in Z:
  p=e['same_route_parity_peer_present_target_absent_periods'][str(w)][z];other=p['peer'];assert other!=z and G[other][0]%6==G[z][0]%6 and p['target_absent_peer_present_periods']==sum(z not in six(row) and other in six(row) for row in rs)
ledger=C(O/'2026325-joint-absence-ledger.csv');assert len(ledger)==66 and all(int(x[f'W{w}_both_absent'])==e['joint_zodiac_absence_periods'][str(w)][pairkey(x['sign_one'],x['sign_two'])] for x in ledger for w in (35,40,45));ck(True,'all 66 joint absences and same-class replacements independently recounted')
ck([e['joint_zodiac_absence_periods'][str(w)][pairkey('虎','狗')] for w in (35,40,45)]==[11,11,12] and [e['same_route_parity_peer_present_target_absent_periods'][str(w)]['狗']['target_absent_peer_present_periods'] for w in (35,40,45)]==[6,6,9] and [e['structural_windows'][str(w)]['no_odd_2road_periods'] for w in (35,40,45)]==[19,20,21],'adverse tiger/dog joint absence, dragon-without-dog and no-odd-2-road history checked')
hand=J('2026325-handwritten-design.json');audit=J('2026325-candidates.json');m=J('2026325-manual-decision.json');assert len(hand['candidates'])==len(audit['candidates'])==38;den=comb(49,6);sigs=defaultdict(list);aa=Counter();overlap=[]
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
ck(len(sigs)==36 and [x for x in sigs.values() if len(x)>1]==[['Z01','Z17','Z18']] and len(overlap)==5 and set(aa)==set(Z) and aa['狗']==18 and hand['proposed_id']==m['human_choice']==audit['selected']['id']=='Z01','38 manual designs, 36 structures, five overlaps and ideal-only models independently enumerated')
sel=audit['selected'];ck(m['universe']==['虎','狗','兔','馬','蛇','豬'] and m['top']=='虎' and m['pair']==['狗','兔'] and m['triple']==['狗','馬','蛇'] and m['reserves']==['豬'] and sel['minimums']['pair']['road_min']==[1,1,0] and (sel['minimums']['pair']['odd_min'],sel['minimums']['pair']['even_min'])==(1,1) and sel['minimums']['triple']['road_min']==[1,1,1] and sel['minimums']['all_columns']['road_min']==[1,2,2] and sel['minimums']['all_columns']['odd_min']==3,'Z01 exact roles, reserve-only pig, mixed pair and full-column necessary minima')
d=J('2026325-manual-decisions.json');previous=J('2026323-manual-decisions.json');ck(all(d['decisions'][k]==v for k,v in previous['decisions'].items()) and len(d['decisions'])==len(previous['decisions'])+1 and '2026324' not in d['decisions'] and d['decisions']['2026325']['target']==2026325,'all earlier decisions preserved; 324 reconstruction not fabricated as published')
page=(O/'2026325-page.html').read_text(encoding='utf8');pd=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));assert len(pd['rows'])==250 and pd['order']==Z
for p,row in zip(pd['rows'],reversed(rows[:250])):assert p==[int(row['period']),row['date'][5:10].replace('-','/') if row['date'] else '--/--',N(row),[Z.index(row[f'z{i}']) for i in range(1,7)],int(row['special']),Z.index(row['special_zodiac'])]
md=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));assert md['2026324']=={'U':[2,10,3,6,5,11],'top':2,'A':10,'B':3,'C':6,'D':5,'top_overlap_mode':'coverage'} and '2026323' not in md and '<footer' not in page and 'footSrc' not in page;ck(True,'250 page rows, unknown dates, Z01 target mapping and no fabricated 324 plan')
with TemporaryDirectory(prefix='325-reproduce-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026325-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026325-manual-decisions.json',t/'data/manual_site_decisions.json');env=dict(os.environ);env['POOL_VERSION']='v5.0';subprocess.run([sys.executable,str(O/'2026325-generator.py')],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026325-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes() and sha(O/'2026325-generator.py')==sha(O/'2026323-generator.py')
ck(True,'unchanged optimized generator reproduces new page snapshots byte-for-byte')
for name in ('2026323-retrospective-public.md','2026324-reconstruction.md','2026324-retrospective-public.md','2026325-analysis.md'):
 for link in re.findall(r'\]\(([^)]+)\)',(O/name).read_text()):
  if not link.startswith(('http://','https://','#')):assert (O/link).is_file(),(name,link)
ck(True,'all new public review and 325 analysis local evidence links resolve')
ck(manifest(O/'2026325.sha256',O)>100,'all new immutable 323–325 evidence files match the new manifest')
print('OFFLINE 323 REVIEW / 324 UNBLINDED RECONSTRUCTION / 325 DISPLAY VERIFICATION PASS — no proof of source, predraw timing, actual mechanism, WeChat safety, predictive advantage or returns')
