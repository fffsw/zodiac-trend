#!/usr/bin/env python3
"""Portable 331 review / 332 manual-display verifier, no draw query or timing certification.
Run from an extracted site root: python observations/2026332-verify.py
"""
from pathlib import Path
from collections import Counter,defaultdict
from math import comb
from html import escape
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;P=O.parent;F=O/'2026332-frozen';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda n:json.loads((O/n).read_text(encoding='utf8'));checks=[]
def ck(x,s):
 if not x:raise AssertionError(s)
 checks.append(s)
def verify(path,base):
 seen=set()
 for line in path.read_text(encoding='utf8').splitlines():
  h,n=line.split('  ',1);p=(base/n).resolve();assert p.is_relative_to(P.resolve()) and p.is_file() and n not in seen and H(p)==h,(path.name,n);seen.add(n)
 return len(seen)
old=('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256','2026327.sha256','2026328.sha256','2026328-correction.sha256','2026328-deep-inputs.sha256','2026328-deep.sha256','2026329.sha256','2026330.sha256','2026331.sha256','2026331-rev1.sha256')
assert all(verify(O/x,O)>0 for x in old) and verify(O/'2026331-rev1-frozen.sha256',O/'2026331-rev1-frozen')>=15 and verify(O/'2026332.sha256',O)>=40 and verify(O/'2026332-frozen.sha256',F)>=25
ck(True,'27 old manifests, two 331-revision manifests and 332/frozen manifests')
assert H(P/'zodiac_trend.html')==H(O/'2026332-page.html') and H(O/'README.md')==H(O/'2026332-readme-snapshot.md') and H(F/'331-revised-homepage.html')==H(O/'2026331-rev1-page.html') and H(F/'331-revised-public-readme.md')==H(O/'2026331-rev1-readme-snapshot.md')
ck(True,'current page/readme and prior 331 revision snapshots match')
with tempfile.TemporaryDirectory(prefix='332-prior-331-revision-') as td:
 t=Path(td)/'site';shutil.copytree(P,t,ignore=shutil.ignore_patterns('.git','__pycache__'));shutil.copyfile(O/'2026331-rev1-page.html',t/'zodiac_trend.html');shutil.copyfile(O/'2026331-rev1-readme-snapshot.md',t/'observations/README.md');q=subprocess.run([sys.executable,str(t/'observations/2026331-rev1-verify.py')],cwd=t,capture_output=True,text=True,timeout=300);assert q.returncode==0 and 'OFFLINE 331 REVISION VERIFICATION PASS' in q.stdout,q.stdout+q.stderr
ck(True,'prior 331 revision and earlier nested verifiers replay in isolated current-view copies')
a=(O/'2026331-rev1-source-data.csv').read_bytes().splitlines(keepends=True);b=(O/'2026332-source-data.csv').read_bytes().splitlines(keepends=True);assert len(a)==1062 and len(b)==1063 and a[0]==b[0] and b[2:]==a[1:] and all(x.endswith(b'\r\n') for x in b) and H(F/'history-through-330.csv')==H(O/'2026331-rev1-source-data.csv')
with (O/'2026332-source-data.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
by={int(r['period']):r for r in rows};r=by[2026331];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];s6=lambda v:{v[f'z{i}'] for i in range(1,7)};nums=lambda v:[int(v[f'n{i}']) for i in range(1,7)];u=J('2026332-user-331.json');assert len(rows)==1062 and max(by)==2026331 and nums(r)==[27,18,3,47,16,14] and [r[f'z{i}'] for i in range(1,7)]==['龍','牛','龍','猴','兔','蛇'] and r['date']=='' and int(r['special'])==13 and r['special_zodiac']=='馬' and u['user_ball_partition_explicitly_confirmed'] and u['normal_numbers']==nums(r) and u['seventh_number']==13 and [sign(n) for n in nums(r)]==[r[f'z{i}'] for i in range(1,7)]
ck(True,'one user-supplied 331 row added; six/seventh user-confirmed, date unknown and no 332 outcome')
a=J('2026331-rev1-manual-decisions.json');b=J('2026332-manual-decisions.json');v=b['decisions']['2026332'];assert len(a['decisions'])==20 and len(b['decisions'])==21 and all(b['decisions'][k]==v0 for k,v0 in a['decisions'].items()) and [v[k] for k in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','虎','牛','鷄','羊'] and v['universe_zodiac']==['馬','虎','牛','鷄','羊','龍'] and all(str(x) not in b['decisions'] for x in (2026319,2026322,2026324)) and '仅三肖栏完整（共1栏）' in v['manual_review']
with tempfile.TemporaryDirectory(prefix='332-repro-') as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026332-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026332-manual-decisions.json',t/'data/manual_site_decisions.json');q=subprocess.run([sys.executable,str(O/'2026332-generator.py')],cwd=t,env={**os.environ,'POOL_VERSION':'v5.0'},capture_output=True,text=True,timeout=90);assert q.returncode==0,q.stdout+q.stderr;assert H(t/'zodiac_trend.html')==H(t/'www/zodiac_trend.html')==H(P/'zodiac_trend.html')
ck(True,'20 earlier decisions preserved; unchanged generator reproduces 332 page exactly')
rev=J('2026332-retrospective.json');records=rev['historical_outcomes'];previous=J('2026331-retrospective.json');assert len(records)==38 and records[:-1]==previous['historical_outcomes'] and [x['period'] for x in records]==[i for i in range(2026291,2026332) if i not in (2026319,2026322,2026324)] and rev['unpublished_reconstructions']==previous['unpublished_reconstructions'] and [x['period'] for x in rev['unpublished_reconstructions']]==[2026319,2026322,2026324]
with (O/'2026332-retrospective-history.csv').open(encoding='utf8',newline='') as f:tab=list(csv.DictReader(f))
assert len(tab)==38
for x,tabrow in zip(records,tab):
 row=by[x['period']];got=s6(row);role=x['roles'];need=[[role['top']],[role['A'],role['B']],[role['A'],role['C'],role['D']]];assert x['normal_numbers']==nums(row) and x['normal_zodiacs']==[row[f'z{i}'] for i in range(1,7)] and x['special_number']==int(row['special']) and x['special_zodiac']==row['special_zodiac'] and int(tabrow['period'])==x['period']
 for sl,ns0,key in zip(x['slots'],need,('single','pair','triple')):
  have=[z for z in ns0 if z in got];missing=[z for z in ns0 if z not in got];assert sl['required']==ns0 and sl['present']==have and sl['missing']==missing and sl['complete']==(not missing) and sl['present_count']==len(have) and tabrow[key+'_present'].split()==have and tabrow[key+'_missing'].split()==missing and tabrow[key+'_hits']==f'{len(have)}/{len(ns0)}'
 assert x['complete_columns']==sum(set(ns0)<=got for ns0 in need)==int(tabrow['complete_columns'])
 if x['universe_zodiacs'] is None:assert x['reserve_hits'] is None and x['outside_universe_hits'] is None
 else:assert set(x['reserve_hits'])==(set(x['universe_zodiacs'])-set(role.values()))&got and set(x['outside_universe_hits'])==got-set(x['universe_zodiacs'])
assert [sum(x['complete_columns']==i for x in records) for i in range(4)]==[16,17,4,1] and [sum(x['slots'][i]['complete'] for x in records) for i in range(3)]==[14,10,4] and [sl['missing'] for sl in records[-1]['slots']]==[['馬'],['狗'],['狗']] and records[-1]['complete_columns']==0 and len([x for x in records if x['universe_zodiacs'] is not None])==30 and sum(bool(x['reserve_hits']) for x in records if x['universe_zodiacs'] is not None)==14
ck(True,'38 retained displays/114 columns settled; 3 reconstructions separate; user 331 actual zero complete')
plans=J('2026331-rev1-design.json')['candidates'];counter=rev['candidate_counterfactuals'];assert len(plans)==len(counter)==10
for p,c in zip(plans,counter):
 rr=p['roles'];needs=[{rr['top']},{rr['A'],rr['B']},{rr['A'],rr['C'],rr['D']}];got=s6(r);assert c['id']==p['id'] and c['roles']==rr and c['complete_columns']==sum(ns0<=got for ns0 in needs) and all(sl['present_count']==len(ns0&got) and set(sl['missing'])==ns0-got for sl,ns0 in zip(c['slots'],needs))
assert Counter(x['complete_columns'] for x in counter)=={0:9,1:1} and next(x for x in counter if x['id']=='GG05')['slots'][2]['complete'] and next(x for x in counter if x['id']=='FF01')['complete_columns']==0 and next(x for x in counter if x['id']=='GG01')['complete_columns']==0
ck(True,'331 initial, actual revision and 10 comparison outcomes distinguished; GG05 is one hindsight column')
study=J('2026332-six-sign-study.json');assert study['current_pending']['previous_six']==['牛','兔','龍','蛇','猴'] and not study['current_pending']['target_result_queried_or_used'] and not study['current_pending']['included_in_followup_denominators'] and study['groups']['previous_six_5_seven_6']=={'n':346,'six_to_six_counts_0_to_5':[8,70,141,107,20,0],'seven_to_seven_counts_0_to_6':[0,23,84,154,73,12,0]} and study['uniform_49_independent_model']['six_to_six']['sizes']==[4]*5
with (O/'2026332-six-sign-pairs.csv').open(encoding='utf8',newline='') as f:pairs=list(csv.DictReader(f))
assert len(pairs)==837 and pairs[-1]['previous']=='2026330' and pairs[-1]['next']=='2026331'
for x in pairs:
 r0=by[int(x['previous'])];r1=by[int(x['next'])];a6=s6(r0);b6=s6(r1);a7=a6|{r0['special_zodiac']};b7=b6|{r1['special_zodiac']};assert int(x['prev6_distinct'])==len(a6) and int(x['prev7_distinct'])==len(a7) and int(x['repeat6_count'])==len(a6&b6) and int(x['repeat7_count'])==len(a7&b7)
for n,k in ((5,5),(5,6),(6,6),(6,7)):
 xs=[x for x in pairs if int(x['prev6_distinct'])==n and int(x['prev7_distinct'])==k];v=study['groups'][f'previous_six_{n}_seven_{k}'];assert v['n']==len(xs) and v['six_to_six_counts_0_to_'+str(n)]==[sum(int(x['repeat6_count'])==i for x in xs) for i in range(n+1)] and v['seven_to_seven_counts_0_to_'+str(k)]==[sum(int(x['repeat7_count'])==i for x in xs) for i in range(k+1)]
ck(True,'837 consecutive pairs and four distinct groups recounted, 332 excluded; 331 previous normal codes all four each')
design=J('2026332-design.json');audit=J('2026332-candidate-audit.json');br=J('2026332-brute.json');assert design['choice']==audit['choice']=='HH01' and len(design['candidates'])==len(audit['candidates'])==16 and not design['target_332_result_queried_or_used'];bit=lambda z:1<<Z.index(z);maskof=lambda zs:sum(bit(z) for z in set(zs));pb=maskof(s6(r));dp={(0,0):1}
for number in range(1,50):
 b0=bit(sign(number));nxt=defaultdict(int,dp)
 for (k,m),v0 in dp.items():
  if k<6:nxt[k+1,m|b0]+=v0
 dp=nxt
ways={m:v0 for (k,m),v0 in dp.items() if k==6};assert sum(ways.values())==comb(49,6)==13983816==br['denominator']
for source,x in zip(design['candidates'],audit['candidates']):
 assert all(source[k]==x[k] for k in source);s=maskof([source['single']]);p=maskof(source['pair']);t=maskof(source['triple']);dist=[0]*4;co=[[0]*4 for k in range(6)];counts=Counter();sub=[Counter() for k in range(6)]
 for m,w in ways.items():
  sl=[m&s==s,m&p==p,m&t==t];n=sum(sl);k=(m&pb).bit_count();dist[n]+=w;co[k][n]+=w
  for key,v0 in zip(('single','pair','triple','pair_and_triple'),(*sl,sl[1] and sl[2])):counts[key]+=w*v0;sub[k][key]+=w*v0
 assert dist==x['uniform_model']['distribution'] and all(counts[k]==x['uniform_model'][k] for k in counts) and all(co[k]==x['conditional_repeat'][k]['distribution'] and all(sub[k][n]==x['conditional_repeat'][k][n] for n in ('single','pair','triple','pair_and_triple')) for k in range(6))
 for window in (35,40,45,60,100,250):
  hist=[0]*4
  for row in rows[-window:]:
   got=s6(row);hist[int(source['single'] in got)+int(set(source['pair'])<=got)+int(set(source['triple'])<=got)]+=1
  assert hist==x['posthoc_fixed_windows'][str(window)]['complete_0_1_2_3']
 if source['id'] in br['cases']:
  d=br['cases'][source['id']];assert d['overall']['distribution']==dist and all(d['overall'][k]==counts[k] for k in counts) and all(d['conditional'][k]['distribution']==co[k] for k in range(6))
sel=audit['selected'];old=audit['baseline'];assert (sel['single'],sel['pair'],sel['triple'],sel['reserves'])==('馬',['虎','牛'],['虎','鷄','羊'],['龍']) and sel['previous_six_overlap']==['牛'] and set(sel['changed_formal_relative_to_331'])=={'虎','鷄','羊'} and old['uniform_model']['distribution']==sel['uniform_model']['distribution']==[5392128,7401592,1144016,46080] and [c['repeat_count'] for c in sel['conditional_repeat'] if c['distribution'][3]]==[1,2] and [c['repeat_count'] for c in old['conditional_repeat'] if c['distribution'][3]]==[3,4] and sel['posthoc_331']['complete_columns']==0
assert [sel['posthoc_fixed_windows'][str(k)]['complete_0_1_2_3'][0] for k in (35,40,45)]==[9,12,14] and [old['posthoc_fixed_windows'][str(k)]['complete_0_1_2_3'][0] for k in (35,40,45)]==[11,14,19] and next(x for x in audit['candidates'] if x['id']=='HH11')['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0]==13
assert br['cases']['T14']['overall']['distribution']==[5280128,7584632,1113936,5120] and br['cases']['T15']['overall']['distribution']==[5728968,6580928,1627840,46080]
ck(True,'16 structures recounted via individual-number DP and five direct enumerations; conditional, hindsight and no-shared alternatives distinguished')
report=(O/'2026332-analysis.md').read_text();index=(O/'2026332-index.html').read_text();readme=(O/'README.md').read_text();assert all(x in report for x in ('已明确确认前六为','第七为**13馬**','330和329的前六／第七划分仍只是按顺序推定','二狗牛1/2缺狗','三狗兔蛇2/3缺狗','只有**1栏**完整','**虎、牛**','**虎、鷄、羊**','38.5598%','0.3295%','80.6007%','HH11近45为**13**次','非盲测','没有擅自改规则上线','本地核验ZIP在当前工作区快照缺失')) and all(x in index for x in ('单馬、二虎牛、三虎鷄羊','38份','331由用户确认','虎是二、三共同位','不能保证命中')) and '2026332-index.html' in readme and '2026331-rev1-index.html' in readme
for x in records+rev['unpublished_reconstructions']:
 html='<tr><td>'+str(x['period']%1000)+'</td>'
 def cell(v0):return f"{''.join(v0['required'])} {v0['present_count']}/{v0['needed_count']}（中{''.join(v0['present']) or '—'}；缺{''.join(v0['missing']) or '—'}）"
 html+=''.join('<td>'+escape(cell(v0))+'</td>' for v0 in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>';assert index.count(html)==1
for name,txt in [('analysis',report),('index',index)]:
 links=re.findall(r'href="([^"]+)"',txt) if name=='index' else re.findall(r'\]\(([^)]+)\)',txt)
 for l in links:
  if not l.startswith(('http://','https://','#','mailto:')):assert (O/l).is_file(),(name,l)
for n in ('2026332-review-qc.json','2026332-candidate-qc.json','2026332-report-qc.json','2026332-local-static-qc.json','2026332-local-browser-qc.json','2026332-local-mobile-qc.json','2026332-local-index-qc.json'):assert J(n)['status']=='PASS',n
ck(True,'report/index caveats, all 41 table rows, links and local QA agree')
print('OFFLINE 331 REVIEW / 332 DISPLAY VERIFICATION PASS: '+str(len(checks))+' checks — internal bytes and arithmetic only; NOT official draw, pre-draw, actual odds, forecast, profit or real WeChat safety')
