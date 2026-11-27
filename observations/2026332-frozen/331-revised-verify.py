#!/usr/bin/env python3
"""Portable 331 revision verifier. No draws queried, timing or prediction certified.
Run from an extracted site root: python observations/2026331-rev1-verify.py
"""
from pathlib import Path
from collections import Counter
from math import comb
from html import escape
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;P=O.parent;F=O/'2026331-rev1-frozen';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda n:json.loads((O/n).read_text(encoding='utf8'));checks=[]
def ck(x,s):
 if not x:raise AssertionError(s)
 checks.append(s)
def verify(path,base):
 seen=set()
 for line in path.read_text(encoding='utf8').splitlines():
  h,n=line.split('  ',1);p=(base/n).resolve();assert p.is_relative_to(P.resolve()) and p.is_file() and n not in seen and H(p)==h,(path.name,n);seen.add(n)
 return len(seen)
old=('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256','2026327.sha256','2026328.sha256','2026328-correction.sha256','2026328-deep-inputs.sha256','2026328-deep.sha256','2026329.sha256','2026330.sha256','2026331.sha256')
assert all(verify(O/x,O)>0 for x in old) and verify(O/'2026331-rev1.sha256',O)>=25 and verify(O/'2026331-rev1-frozen.sha256',F)>=15
ck(True,'27 old manifests, revision manifest and frozen sources')
assert H(P/'zodiac_trend.html')==H(O/'2026331-rev1-page.html') and H(O/'README.md')==H(O/'2026331-rev1-readme-snapshot.md') and H(F/'initial-331-homepage.html')==H(O/'2026331-page.html') and H(F/'initial-public-readme.md')==H(O/'2026331-readme-snapshot.md')
ck(True,'revised page/readme and initial 331 page/readme match their snapshots')
with tempfile.TemporaryDirectory(prefix='331-revision-prior-') as td:
 t=Path(td)/'site';shutil.copytree(P,t,ignore=shutil.ignore_patterns('.git','__pycache__'));shutil.copyfile(O/'2026331-page.html',t/'zodiac_trend.html');shutil.copyfile(O/'2026331-readme-snapshot.md',t/'observations/README.md');q=subprocess.run([sys.executable,str(t/'observations/2026331-verify.py')],cwd=t,capture_output=True,text=True,timeout=300);assert q.returncode==0 and 'OFFLINE 330 REVIEW / 331 DISPLAY VERIFICATION PASS' in q.stdout,q.stdout+q.stderr
ck(True,'initial 331 verifier replays successfully in isolated prior-current view')
assert (O/'2026331-rev1-source-data.csv').read_bytes()==(O/'2026331-source-data.csv').read_bytes()==(F/'history-through-330.csv').read_bytes()
with (O/'2026331-rev1-source-data.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];by={int(r['period']):r for r in rows};r=by[2026330];prev={'馬','猴','豬','牛','鷄'};s6=lambda v:{v[f'z{i}'] for i in range(1,7)};assert len(rows)==1061 and max(by)==2026330 and [int(r[f'n{i}']) for i in range(1,7)]==[25,35,20,8,30,22] and [r[f'z{i}'] for i in range(1,7)]==['馬','猴','豬','豬','牛','鷄'] and r['date']=='' and int(r['special'])==26 and r['special_zodiac']=='蛇' and s6(r)==prev
ck(True,'history byte-identical; user 330 first-six/seventh inferred; no 331 outcome row')
a=J('2026331-manual-decisions.json');b=J('2026331-rev1-manual-decisions.json');v=b['decisions']['2026331'];assert len(a['decisions'])==len(b['decisions'])==20 and all(b['decisions'][k]==v0 for k,v0 in a['decisions'].items() if k!='2026331') and [v[k] for k in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','狗','牛','兔','蛇'] and v['universe_zodiac']==['馬','狗','牛','兔','蛇','虎'] and all(str(x) not in b['decisions'] for x in (2026319,2026322,2026324))
with tempfile.TemporaryDirectory(prefix='331-revision-repro-') as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026331-rev1-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026331-rev1-manual-decisions.json',t/'data/manual_site_decisions.json');q=subprocess.run([sys.executable,str(O/'2026331-rev1-generator.py')],cwd=t,env={**os.environ,'POOL_VERSION':'v5.0'},capture_output=True,text=True,timeout=90);assert q.returncode==0,q.stdout+q.stderr;assert H(t/'zodiac_trend.html')==H(t/'www/zodiac_trend.html')==H(P/'zodiac_trend.html')
ck(True,'19 other decisions preserved; unchanged generator reproduces revision exactly')
rev=J('2026331-retrospective.json');records=rev['historical_outcomes'];assert len(records)==37 and [x['period'] for x in records]==[i for i in range(2026291,2026331) if i not in (2026319,2026322,2026324)] and [x['period'] for x in rev['unpublished_reconstructions']]==[2026319,2026322,2026324]
for x in records:
 got=s6(by[x['period']]);role=x['roles'];need=[[role['top']],[role['A'],role['B']],[role['A'],role['C'],role['D']]];assert all(sl['required']==ns and sl['present']==[z for z in ns if z in got] and sl['missing']==[z for z in ns if z not in got] and sl['complete']==(set(ns)<=got) for sl,ns in zip(x['slots'],need)) and x['complete_columns']==sum(set(ns)<=got for ns in need)
assert Counter(x['complete_columns'] for x in records)=={0:15,1:17,2:4,3:1} and [sl['missing'] for sl in records[-1]['slots']]==[[],[],['龍','虎']] and records[-1]['complete_columns']==2
ck(True,'37 retained displays/111 columns and three reconstructions remain separately identified')
design=J('2026331-rev1-design.json');audit=J('2026331-rev1-audit.json');br=J('2026331-rev1-brute.json');assert design['choice']==audit['choice']=='GG01' and len(design['candidates'])==len(audit['candidates'])==10 and not design['target_331_result_queried_or_used'];G={z:[n for n in range(1,50) if sign(n)==z] for z in Z};pb=sum(1<<Z.index(z) for z in prev);ways={}
for mask in range(1<<12):
 if mask.bit_count()>6:continue
 poly=[1,0,0,0,0,0,0]
 for i,z in enumerate(Z):
  if not (mask>>i)&1:continue
  q=[0]*7
  for a0 in range(7):
   for k in range(1,min(len(G[z]),6-a0)+1):q[a0+k]+=poly[a0]*comb(len(G[z]),k)
  poly=q
 if poly[6]:ways[mask]=poly[6]
assert sum(ways.values())==comb(49,6)==13983816==br['denominator'];maskof=lambda vals:sum(1<<Z.index(z) for z in set(vals))
for source,x in zip(design['candidates'],audit['candidates']):
 role=source['roles'];assert source['id']==x['id'] and role==x['roles'] and source['reserves']==x['reserves'];s=maskof([role['top']]);p=maskof([role['A'],role['B']]);t=maskof([role['A'],role['C'],role['D']]);dist=[0]*4;co=[[0]*4 for k in range(6)];counts=Counter()
 for mask,w in ways.items():
  sl=[mask&s==s,mask&p==p,mask&t==t];n=sum(sl);dist[n]+=w;co[(mask&pb).bit_count()][n]+=w
  for key,v0 in zip(('single','pair','triple'),sl):counts[key]+=w*v0
  counts['pair_and_triple']+=w*(sl[1] and sl[2])
 assert dist==x['uniform_model']['distribution'] and all(counts[k]==x['uniform_model'][k] for k in counts) and all(co[k]==x['conditional_repeat'][k]['distribution'] for k in range(6))
 for window in (35,40,45,60,100,250):
  d=[0]*4
  for q in rows[-window:]:
   got=s6(q);need=[{role['top']},{role['A'],role['B']},{role['A'],role['C'],role['D']}];d[sum(v0<=got for v0 in need)]+=1
  assert d==x['posthoc_fixed_windows'][str(window)]['complete_0_1_2_3']
ck(True,'10 related candidates independently recounted by 12-sign masks and post-hoc historical windows')
sel=audit['selected'];base=audit['baseline'];assert sel['roles']=={'top':'馬','A':'狗','B':'牛','C':'兔','D':'蛇'} and sel['reserves']==['虎'] and set(sel['previous_six_overlap'])=={'馬','牛'} and len(sel['changed_relative_to_330_display'])==3 and len(sel['changed_relative_to_initial_331'])==2 and sel['pair_minimum']=={'road_0_1_2':[2,0,0],'odd_even':[1,1]} and sel['triple_minimum']=={'road_0_1_2':[1,1,1],'odd_even':[1,2]} and sel['all_minimum']=={'road_0_1_2':[2,2,1],'odd_even':[2,3]}
assert br['old']==br['revised'] and br['old']['distribution']==[5392128,7401592,1144016,46080] and all(br['old_conditional'][k]['distribution']==base['conditional_repeat'][k]['distribution'] and br['revised_conditional'][k]['distribution']==sel['conditional_repeat'][k]['distribution'] for k in range(6)) and [g['distribution'][3]>0 for g in sel['conditional_repeat']]==[False,False,True,True,False,False]
assert base['conditional_repeat'][0]['distribution'][0]==base['conditional_repeat'][0]['denominator'] and sel['conditional_repeat'][0]['distribution'][0]<sel['conditional_repeat'][0]['denominator'] and base['conditional_repeat'][5]['distribution'][2]==base['conditional_repeat'][5]['denominator'] and sel['conditional_repeat'][5]['distribution'][1]>0
assert sel['posthoc_330']['complete_columns']==1 and base['posthoc_330']['complete_columns']==2 and [sel['posthoc_fixed_windows'][str(k)]['complete_0_1_2_3'][0] for k in (35,40,45)]==[11,14,18] and [base['posthoc_fixed_windows'][str(k)]['complete_0_1_2_3'][0] for k in (35,40,45)]==[11,12,16]
ck(True,'revision change, road risk, zero/five-repeat tradeoffs and unfavorable hindsight verified; equal unconditional model')
report=(O/'2026331-rev1-analysis.md').read_text();index=(O/'2026331-rev1-index.html').read_text();readme=(O/'README.md').read_text();assert all(x in report for x in ('**狗、牛**','**狗、兔、蛇**','18／45','16／45','78.4403%','38.5598%','0.3295%','未明确确认球次','不是盲选','没有证据证明','未出现在本次工作区快照')) and all(x in index for x in ('单馬、二狗牛、三狗兔蛇','37份','用户尚未明确确认球次','原331初版事后套330为两栏','修订18次','狗是二、三共同位')) and '2026331-rev1-index.html' in readme and '2026331-index.html' in readme
for x in records+rev['unpublished_reconstructions']:
 html='<tr><td>'+str(x['period']%1000)+'</td>'
 def cell(v):return f"{''.join(v['required'])} {v['present_count']}/{v['needed_count']}（中{''.join(v['present']) or '—'}；缺{''.join(v['missing']) or '—'}）"
 html+=''.join('<td>'+escape(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>';assert index.count(html)==1
for name,txt in [('analysis',report),('index',index)]:
 links=re.findall(r'href="([^"]+)"',txt) if name=='index' else re.findall(r'\]\(([^)]+)\)',txt)
 for l in links:
  if not l.startswith(('http://','https://','#','mailto:')):assert (O/l).is_file(),(name,l)
for n in ('2026331-rev1-qc.json','2026331-rev1-local-static-qc.json','2026331-rev1-local-browser-qc.json','2026331-rev1-local-mobile-qc.json','2026331-rev1-local-index-qc.json','2026331-rev1-report-qc.json'):assert J(n)['status']=='PASS',n
ck(True,'report/index risks, unfavorable hindsight, all 40 table rows, links and local QA agree')
print('OFFLINE 331 REVISION VERIFICATION PASS: '+str(len(checks))+' checks — internal bytes and arithmetic only; NOT official draw, pre-draw, actual odds, forecast, profit or real WeChat safety')
