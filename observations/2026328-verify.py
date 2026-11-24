#!/usr/bin/env python3
"""Portable offline 327 review / 328 display verification (no network).
Run from any cwd: python3 observations/2026328-verify.py
It checks integrity and mathematics, not official provenance, chronology, prediction or winnings.
"""
from pathlib import Path
from collections import defaultdict,Counter
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
oldmans=('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256','2026327.sha256')
assert all(manifest(n,O,P)>0 for n in oldmans) and manifest('2026328.sha256',O)>40 and manifest('2026328-before.sha256',O/'2026328-retrospective-frozen')==30 and manifest('2026327-before.sha256',O/'2026327-retrospective-frozen')==70
ck(True,'20 old manifests, new evidence manifest, 30 new freeze copies and 70 previous freeze copies match')
# Previous verifier expects the then-current homepage/README. Recreate a safe prior view;
# never overwrite the present homepage or the prior archived copies.
with tempfile.TemporaryDirectory(prefix='328-prior-verify-') as td:
 prior=Path(td)/'prior';shutil.copytree(P,prior,ignore=shutil.ignore_patterns('.git','__pycache__'),copy_function=shutil.copyfile);(prior/'zodiac_trend.html').unlink();shutil.copyfile(O/'2026327-page.html',prior/'zodiac_trend.html');(prior/'observations/README.md').unlink();shutil.copyfile(O/'2026327-readme-snapshot.md',prior/'observations/README.md');r=subprocess.run([sys.executable,str(prior/'observations/2026327-verify.py')],capture_output=True,text=True,timeout=120);assert r.returncode==0 and 'OFFLINE 326 CONDITIONAL REVIEW / 327 DISPLAY VERIFICATION PASS' in r.stdout,r.stdout+r.stderr
ck(True,'previous 327 offline verifier passes in isolated prior-homepage view')
def read(n):
 with (O/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
raw=(O/'2026328-source-data.csv').read_bytes().splitlines(keepends=True);prior=(O/'2026328-retrospective-frozen/history-through-326.csv').read_bytes().splitlines(keepends=True);assert len(raw)==1059 and len(prior)==1058 and raw[0]==prior[0] and raw[2:]==prior[1:] and all(x.endswith(b'\r\n') for x in raw)
rows=sorted(read('2026328-source-data.csv'),key=lambda x:int(x['period']));by={int(x['period']):x for x in rows};u=J('2026328-user-327.json');Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zof=lambda n:Z[(7-n)%12];ns=lambda x:[int(x[f'n{i}']) for i in range(1,7)];zs=lambda x:[x[f'z{i}'] for i in range(1,7)];assert len(rows)==1058 and int(rows[-1]['period'])==2026327 and all(int(x['period'])<=2026327 for x in rows) and ns(rows[-1])==u['normal_numbers']==[21,49,7,41,46,36] and int(rows[-1]['special'])==u['seventh_number']==45 and rows[-1]['date']=='' and [zof(n) for n in ns(rows[-1])]==zs(rows[-1])==u['normal_zodiacs'] and zof(45)==rows[-1]['special_zodiac']=='狗' and len(set(ns(rows[-1])+[45]))==7
ck(True,'only user 327 was added; 1057 earlier rows preserved byte-for-byte, date empty and seventh separate')
dec=J('2026328-retrospective-frozen/327-manual-decision.json');role={'top':dec['top'],'A':dec['pair'][0],'B':dec['pair'][1],'C':dec['triple'][1],'D':dec['triple'][2]};got=set(zs(rows[-1]));slots=[{role['top']},{role['A'],role['B']},{role['A'],role['C'],role['D']}];assert role=={'top':'馬','A':'鷄','B':'龍','C':'虎','D':'牛'} and [len(s&got) for s in slots]==[1,1,2] and [s-got for s in slots]==[set(),{'龍'},{'牛'}] and sum(s<=got for s in slots)==1 and [sum(n%3==k for n in ns(rows[-1])) for k in range(3)]==[2,3,1] and [zof(n) for n in ns(rows[-1]) if n%3==0]==['狗','羊'] and len(got&set(zs(by[2026326])))==4
ck(True,'327 single horse complete; chicken shared, dragon and ox missing despite same-category dog and sheep')
record=J('2026328-retrospective.json')['historical_outcomes'];csvrows=read('2026328-retrospective-history.csv');assert len(record)==len(csvrows)==34
for x,line in zip(record,csvrows):
 p=x['period'];assert str(p)==line['period'] and p in by
 if p<=2026308:
  s=J(f'2026327-retrospective-frozen/prior-records/{p}.json')['site_display'];q={'top':Z[s['top']],'A':Z[s['t2'][0]],'B':Z[s['t2'][1]],'C':Z[s['t3'][1]],'D':Z[s['t3'][2]]}
 else:
  page=(O/'2026328-retrospective-frozen/327-current-homepage.html').read_text() if p==2026327 else (O/f'2026327-retrospective-frozen/historical-pages/{p}.html').read_text();s=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1))[str(p-1)];q={k:Z[s[k]] for k in ('top','A','B','C','D')}
 assert q==x['roles'];present=set(zs(by[p]));ss=[{q['top']},{q['A'],q['B']},{q['A'],q['C'],q['D']}]
 for i,(s,v) in enumerate(zip(ss,x['slots'])):assert set(v['present'])==s&present and set(v['missing'])==s-present and v['present_count']==len(s&present) and line[['single_hits','pair_hits','triple_hits'][i]]==f'{len(s&present)}/{len(s)}'
 assert x['complete_columns']==int(line['complete_columns'])==sum(s<=present for s in ss)
groups=J('2026328-retrospective.json')['historical_groups']['all_34_mixed_sources_versions'];dist=Counter(x['complete_columns'] for x in record);assert [dist[i] for i in range(4)]==groups['complete_columns_distribution_0_to_3']==[13,17,3,1] and [sum(x['slots'][i]['complete'] for x in record) for i in range(3)]==[13,9,4] and groups['shared_A_absent']==15 and groups['shared_A_present_both_pair_triple_incomplete_count']==7
recon=J('2026328-retrospective.json')['unpublished_reconstructions'];assert [x['period'] for x in recon]==[2026319,2026322,2026324] and not {x['period'] for x in recon}&{x['period'] for x in record}
for x in recon:
 p=x['period'];v=J(f'2026327-retrospective-frozen/{p%1000}-reconstruction-manual.json');q=x['roles'];assert x['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' and q=={'top':v['top'],'A':v['pair'][0],'B':v['pair'][1],'C':v['triple'][1],'D':v['triple'][2]};present=set(zs(by[p]));ss=[{q['top']},{q['A'],q['B']},{q['A'],q['C'],q['D']}];assert x['complete_columns']==sum(s<=present for s in ss) and [v['present_count'] for v in x['slots']]==[len(s&present) for s in ss]
ck(True,'34 archived versions plus three separately labelled post-outcome reconstructions directly re-settled')
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
study=J('2026328-six-sign-study.json');g=study['groups']['2024plus'];assert len(pairs)==g['n']==132 and [sum(x[0]==i for x in pairs) for i in range(7)]==g['six_to_six_counts_0_to_6']==[2,9,45,47,26,3,0] and [sum(x[1]==i for x in pairs) for i in range(7)]==g['seven_to_seven_counts_0_to_6']==[0,3,33,54,35,6,1] and study['current_pending']['target_result_read'] is False and study['current_pending']['included_in_followup_denominators'] is False
ck(True,'132 six-/seven-sign followups reproduced through 327; unknown 328 excluded')
oldm=J('2026328-retrospective-frozen/manual-decisions-through-327.json');newm=J('2026328-manual-decisions.json');assert len(oldm['decisions'])==16 and len(newm['decisions'])==17 and all(newm['decisions'][k]==v for k,v in oldm['decisions'].items()) and all(k not in newm['decisions'] for k in ('2026319','2026322','2026324'));n=newm['decisions']['2026328'];assert [n[x] for x in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','狗','鷄','馬','蛇'] and n['universe_zodiac']==['馬','狗','鷄','蛇','虎','牛'] and n['top_overlap_mode']=='concentrated'
page=(O/'2026328-page.html').read_text();pat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';datpat=r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;';data=json.loads(re.search(datpat,page).group(1));m=json.loads(re.search(pat,page).group(1));assert data['rows'][-1]==[2026327,'--/--',[21,49,7,41,46,36],[10,6,0,2,9,7],45,10] and m['2026327']=={'U':[6,10,9,5,2,1],'top':6,'A':10,'B':9,'C':6,'D':5,'top_overlap_mode':'concentrated'} and H(O/'2026328-page.html')==H(P/'zodiac_trend.html') and H(O/'2026328-readme-snapshot.md')==H(O/'README.md')
with tempfile.TemporaryDirectory(prefix='328-reproduce-') as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026328-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026328-manual-decisions.json',t/'data/manual_site_decisions.json');subprocess.run([sys.executable,str(O/'2026328-generator.py')],cwd=t,env={**os.environ,'POOL_VERSION':'v5.0'},check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026328-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
ck(True,'16 earlier decisions preserved; unchanged generator reproduces 328 display and six-sign universe')
audit=J('2026328-candidates.json');design=J('2026328-handwritten-design.json');sizes={z:sum(zof(i)==z for i in range(1,50)) for z in Z};D=comb(49,6);assert len(audit['candidates'])==len(design['candidates'])==12
for x,y in zip(audit['candidates'],design['candidates']):
 assert x['id']==y['id'] and x['roles']==y['roles'] and x['reserves']==y['reserves'];q=x['roles'];seen=list(dict.fromkeys(q.values()));gs=[sizes[z] for z in seen];other=49-sum(gs);S={q['top']};P2={q['A'],q['B']};T={q['A'],q['C'],q['D']};counts=dict.fromkeys(('single','pair','triple','all_columns','no_complete_column','at_least_one_complete','pair_and_triple'),0)
 for ks in product(*(range(n+1) for n in gs)):
  rem=6-sum(ks)
  if not 0<=rem<=other:continue
  w=comb(other,rem)
  for size,take in zip(gs,ks):w*=comb(size,take)
  seen_now={z for z,k in zip(seen,ks) if k};a,b,c=S<=seen_now,P2<=seen_now,T<=seen_now
  for label,on in [('single',a),('pair',b),('triple',c),('all_columns',a and b and c),('no_complete_column',not(a or b or c)),('at_least_one_complete',a or b or c),('pair_and_triple',b and c)]:counts[label]+=w*on
 assert counts==x['ideal_model']['counts'] and x['ideal_model']['denominator']==D
p=audit['selected']['ideal_model']['percent'];assert round(p['single'],4)==49.5198 and round(p['pair'],4)==15.6616 and round(p['triple'],4)==6.1500 and round(p['all_columns'],4)==1.6585 and round(p['no_complete_column'],4)==40.9686
ck(True,'all 12 exact ideal candidate models directly enumerated; no prediction or actual-odds claim')
report=(O/'2026328-analysis.md').read_text();idx=(O/'2026328-index.html').read_text();assert len(re.findall(r'^\| \d{3} \|',report,re.M))==37 and all(x in report for x in ('没有任何方案可以保证下期命中','一栏完整，两组合不完整','这不是328号码')) and all(x in idx for x in ('单馬','二狗鷄','三狗馬蛇','虎牛仅替补','不能保证'))
for x in re.findall(r'\]\(([^)]+)\)',report):
 if not x.startswith(('http://','https://','#','mailto:')):assert (O/x).is_file(),x
for x in re.findall(r'href="([^"]+)"',idx):
 if not x.startswith(('http://','https://','#','mailto:')):assert (O/x).is_file(),x
ck(True,'public report/index agree with the selected display, and all relative evidence links resolve')
print('OFFLINE 327 CONDITIONAL REVIEW / 328 DISPLAY VERIFICATION PASS: '+str(len(checks))+' checks — not an official source, chronological, predraw, forecast, mechanism or WeChat certificate')
