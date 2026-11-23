#!/usr/bin/env python3
"""Portable offline verification of the 326 conditional review and 327 manual display.
Run from any cwd: python3 observations/2026327-verify.py
It checks bytes and arithmetic, not actual dates, official provenance, outcomes or forecasts.
"""
from pathlib import Path
from collections import defaultdict
from datetime import date
from itertools import product
from math import comb
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;P=O.parent;J=lambda n:json.loads((O/n).read_text(encoding='utf8'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
def manifest(name,base,safe_root=None):
 names=set();root=(safe_root or base).resolve()
 for line in (O/name).read_text(encoding='utf8').splitlines():
  h,n=line.split('  ',1);f=(base/n).resolve();assert f.is_relative_to(root) and n not in names and f.is_file() and H(f)==h,(name,n);names.add(n)
 return len(names)
oldmans=('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256')
assert all(manifest(n,O,P)>0 for n in oldmans) and manifest('2026327.sha256',O)>90 and manifest('2026327-before.sha256',O/'2026327-retrospective-frozen')==70
ck(True,'19 old manifests, new evidence manifest and 70 frozen previous inputs pass byte verification')
r=subprocess.run([sys.executable,str(O/'2026326-rev1-verify.py')],capture_output=True,text=True,timeout=120);assert r.returncode==0 and 'OFFLINE 326 REVISION VERIFICATION PASS' in r.stdout,r.stdout+r.stderr;ck(True,'prior 326 revision portable verifier still passes')
def read(n):
 with (O/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
raw=(O/'2026327-source-data.csv').read_bytes().splitlines(keepends=True);prior=(O/'2026327-retrospective-frozen/history-through-325.csv').read_bytes().splitlines(keepends=True);assert len(raw)==1058 and len(prior)==1057 and raw[0]==prior[0] and raw[2:]==prior[1:] and all(x.endswith(b'\r\n') for x in raw)
rows=sorted(read('2026327-source-data.csv'),key=lambda x:int(x['period']));by={int(x['period']):x for x in rows};u=J('2026327-user-326.json');assert len(rows)==1057 and int(rows[-1]['period'])==2026326 and all(int(x['period'])<=2026326 for x in rows) and [int(rows[-1][f'n{i}']) for i in range(1,7)]==u['normal_numbers']==[9,16,22,36,5,47] and int(rows[-1]['special'])==u['seventh_number']==23 and rows[-1]['date']==''
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zof=lambda n:Z[(7-n)%12];ns=lambda x:[int(x[f'n{i}']) for i in range(1,7)];zs=lambda x:[x[f'z{i}'] for i in range(1,7)];assert [zof(n) for n in ns(rows[-1])]==zs(rows[-1])==u['normal_zodiacs'] and zof(23)==rows[-1]['special_zodiac']=='猴' and len(set(ns(rows[-1])+[23]))==7
ck(True,'only user 326 was added, earlier 1056 rows preserved; seventh is separate and date empty')
dec=J('2026327-retrospective-frozen/326-revision-decision.json');role={'top':dec['single'],'A':dec['pair'][0],'B':dec['pair'][1],'C':dec['triple'][1],'D':dec['triple'][2]};actual=set(zs(rows[-1]));ss=[{role['top']},{role['A'],role['B']},{role['A'],role['C'],role['D']}];assert role=={'top':'羊','A':'虎','B':'羊','C':'馬','D':'鷄'} and [len(x&actual) for x in ss]==[1,2,2] and ss[2]-actual=={'馬'} and sum(x<=actual for x in ss)==2
orig=[{'羊'},{'虎','羊'},{'虎','馬','兔'}];assert [len(x&actual) for x in orig]==[1,2,2] and orig[2]-actual=={'馬'} and [sum(n%3==r for n in ns(rows[-1])) for r in range(3)]==[2,2,2] and not any(n%3==1 and n%2 for n in ns(rows[-1]))
ck(True,'conditional 326 revision and original comparison independently recomputed; horse absent rather than 1-road absent')
record=J('2026327-retrospective.json')['historical_outcomes'];csvrows=read('2026327-retrospective-history.csv');assert len(record)==len(csvrows)==33
for x,line in zip(record,csvrows):
 p=x['period'];assert str(p)==line['period'] and p in by
 if p<=2026308:
  s=J(f'2026327-retrospective-frozen/prior-records/{p}.json')['site_display'];q={'top':Z[s['top']],'A':Z[s['t2'][0]],'B':Z[s['t2'][1]],'C':Z[s['t3'][1]],'D':Z[s['t3'][2]]}
 else:
  page=(O/f'2026327-retrospective-frozen/historical-pages/{p}.html').read_text();s=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1))[str(p-1)];q={k:Z[s[k]] for k in ('top','A','B','C','D')}
 assert q==x['roles'];got=set(zs(by[p]));sets=[{q['top']},{q['A'],q['B']},{q['A'],q['C'],q['D']}];slotnames=['single_hits','pair_hits','triple_hits']
 for i,(s,v) in enumerate(zip(sets,x['slots'])):assert set(v['present'])==s&got and set(v['missing'])==s-got and v['present_count']==len(s&got) and line[slotnames[i]]==f'{len(s&got)}/{len(s)}'
 assert x['complete_columns']==int(line['complete_columns'])==sum(s<=got for s in sets)
recon=J('2026327-retrospective.json')['unpublished_reconstructions'];assert [x['period'] for x in recon]==[2026319,2026322,2026324] and all(x['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' for x in recon) and not {x['period'] for x in recon}&{x['period'] for x in record}
for x in recon:
 p=x['period'];v=J(f'2026327-retrospective-frozen/{p%1000}-reconstruction-manual.json');assert x['role']=={'top':v['top'],'A':v['pair'][0],'B':v['pair'][1],'C':v['triple'][1],'D':v['triple'][2]};q=x['role'];got=set(zs(by[p]));sets=[{q['top']},{q['A'],q['B']},{q['A'],q['C'],q['D']}];assert x['complete_columns']==sum(s<=got for s in sets) and [v['present_count'] for v in x['slots']]==[len(s&got) for s in sets]
ck(True,'all 33 archived displayed versions and three separately labeled after-outcome reconstructions directly re-settled')
def adjacent(a,b):
 p,q=int(a['period']),int(b['period'])
 if p//1000==q//1000:return q==p+1
 if q//1000==p//1000+1 and q%1000==1:
  try:return (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days==1
  except ValueError:return False
 return False
pairs=[]
for x,y in zip(rows,rows[1:]):
 if not adjacent(x,y) or len(set(ns(x)+[int(x['special'])]))!=7 or len(set(ns(y)+[int(y['special'])]))!=7:continue
 a6=set(zs(x));a7=a6|{x['special_zodiac']};b6=set(zs(y));b7=b6|{y['special_zodiac']}
 if len(a6)==len(a7)==6:pairs.append((len(a6&b6),len(a7&b7)))
study=J('2026327-six-sign-study.json');g=study['groups']['2024plus'];assert len(pairs)==g['n']==131 and [sum(x[0]==i for x in pairs) for i in range(7)]==g['six_to_six_counts_0_to_6']==[2,9,45,47,25,3,0] and [sum(x[1]==i for x in pairs) for i in range(7)]==g['seven_to_seven_counts_0_to_6']==[0,3,33,54,34,6,1] and not study['current_pending']['target_result_read']
for n in (6,7):
 dp={(0,0):1}
 for size,prior_group in [(4,True)]*6+[(25,False)]:
  nxt=defaultdict(int)
  for (balls,k),ways in dp.items():
   for take in range(min(size,n-balls)+1):nxt[(balls+take,k+int(prior_group and take>0))]+=ways*comb(size,take)
  dp=nxt
 model=study['uniform_49_independent_model'][str(n)];assert [dp.get((n,i),0) for i in range(7)]==model['counts_0_to_6'] and sum(model['counts_0_to_6'])==comb(49,n)
ck(True,'six/seven identity cohort and ideal conditional-count model independently reproduced, without predicting 327')
oldm=J('2026327-retrospective-frozen/manual-decisions-through-326.json');newm=J('2026327-manual-decisions.json');assert len(newm['decisions'])==len(oldm['decisions'])+1 and all(newm['decisions'][k]==v for k,v in oldm['decisions'].items()) and all(k not in newm['decisions'] for k in ('2026319','2026322','2026324'));n=newm['decisions']['2026327'];assert [n[x] for x in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','鷄','龍','虎','牛'] and n['universe_zodiac']==['馬','鷄','龍','虎','牛','蛇'] and n['top_overlap_mode']=='coverage'
page=(O/'2026327-page.html').read_text();pat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';datpat=r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;';d=json.loads(re.search(datpat,page).group(1));m=json.loads(re.search(pat,page).group(1));assert d['rows'][-1]==[2026326,'--/--',[9,16,22,36,5,47],[10,3,9,7,2,8],23,8] and m['2026326']=={'U':[6,9,4,2,1,5],'top':6,'A':9,'B':4,'C':2,'D':1,'top_overlap_mode':'coverage'} and H(O/'2026327-page.html')==H(P/'zodiac_trend.html') and H(O/'2026327-readme-snapshot.md')==H(O/'README.md')
with tempfile.TemporaryDirectory(prefix='327-verify-') as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026327-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026327-manual-decisions.json',t/'data/manual_site_decisions.json');subprocess.run([sys.executable,str(O/'2026327-generator.py')],cwd=t,env={**os.environ,'POOL_VERSION':'v5.0'},check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026327-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
ck(True,'all earlier decisions preserved; unchanged generator reproduces 327 page and six-zodiac universe')
audit=J('2026327-candidates.json');design=J('2026327-handwritten-design.json');sizes={z:sum(zof(i)==z for i in range(1,50)) for z in Z};D=comb(49,6);assert len(audit['candidates'])==len(design['candidates'])==12
for x,y in zip(audit['candidates'],design['candidates']):
 assert x['id']==y['id'] and x['roles']==y['roles'] and x['reserves']==y['reserves'];r=x['roles'];seen=list(dict.fromkeys(r.values()));gs=[sizes[z] for z in seen];other=49-sum(gs);S={r['top']};P2={r['A'],r['B']};T={r['A'],r['C'],r['D']};counts=dict.fromkeys(('single','pair','triple','all_columns','no_complete_column','at_least_one_complete','pair_and_triple'),0)
 for ks in product(*(range(n+1) for n in gs)):
  rem=6-sum(ks)
  if not 0<=rem<=other:continue
  w=comb(other,rem)
  for size,take in zip(gs,ks):w*=comb(size,take)
  got={z for z,k in zip(seen,ks) if k};a,b,c=S<=got,P2<=got,T<=got
  for label,on in [('single',a),('pair',b),('triple',c),('all_columns',a and b and c),('no_complete_column',not(a or b or c)),('at_least_one_complete',a or b or c),('pair_and_triple',b and c)]:counts[label]+=w*on
 assert counts==x['ideal_model']['counts'] and x['ideal_model']['denominator']==D
p=audit['selected']['ideal_model']['percent'];b=audit['candidates'][1]['ideal_model']['percent'];assert round(p['no_complete_column'],4)==38.5598 and round(p['all_columns'],4)==0.3295 and round(b['no_complete_column'],4)==54.5086 and round(b['all_columns'],4)==1.3611
ck(True,'all 12 exact ideal candidate models directly enumerated; tradeoff is not actual odds or performance')
report=(O/'2026327-analysis.md').read_text();idx=(O/'2026327-index.html').read_text();assert len(re.findall(r'^\| \d{3} \|',report,re.M))==36 and all(x in report for x in ('不能保证下期命中','两栏完整、三肖缺馬','不能当成已认证的真实开奖','不是327号码')) and all(x in idx for x in ('单馬','二鷄龍','三鷄虎牛','蛇仅替补','不能保证'))
for x in re.findall(r'\]\(([^)]+)\)',report):
 if not x.startswith(('http://','https://','#','mailto:')):assert (O/x).is_file(),x
for x in re.findall(r'href="([^"]+)"',idx):
 if not x.startswith(('http://','https://','#','mailto:')):assert (O/x).is_file(),x
ck(True,'public report and index agree; all relative evidence links resolve')
print('OFFLINE 326 CONDITIONAL REVIEW / 327 DISPLAY VERIFICATION PASS: '+str(len(checks))+' checks — not an official source, chronological, predraw, forecast, mechanism or WeChat certificate')
