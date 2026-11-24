#!/usr/bin/env python3
"""Portable 328-review/329-display verifier: python3 observations/2026329-verify.py.
Internal integrity and arithmetic only: cannot authenticate draw, date, source, odds or future outcome.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from datetime import date
from math import comb
import csv,hashlib,json,re,shutil,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;P=O.parent;F=O/'2026327-retrospective-frozen';G=O/'2026328-retrospective-frozen';B=O/'2026329-retrospective-frozen';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads((O/p).read_text(encoding='utf8'));checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
def verify(path,base):
 seen=set()
 for line in path.read_text(encoding='utf8').splitlines():
  h,rel=line.split('  ',1);p=(base/rel).resolve();assert p.is_relative_to(P.resolve()) and p.is_file() and rel not in seen and H(p)==h,(path.name,rel);seen.add(rel)
 return len(seen)
old=('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256','2026327.sha256','2026328.sha256','2026328-correction.sha256','2026328-deep-inputs.sha256','2026328-deep.sha256')
assert all(verify(O/n,O)>0 for n in old) and verify(O/'2026329.sha256',O)>=40 and verify(O/'2026329-frozen.sha256',B)>=20 and verify(O/'2026327-before.sha256',F)>=60 and verify(O/'2026328-before.sha256',G)>=20
ck(True,'24 earlier manifests, 329 manifest, public frozen subset, and prior 327/328 source manifests')
assert H(P/'zodiac_trend.html')==H(O/'2026329-page.html') and H(O/'README.md')==H(O/'2026329-readme-snapshot.md') and H(B/'328-current-homepage.html')==H(O/'2026328-page.html') and H(B/'history-through-327.csv')==H(O/'2026328-source-data.csv')
ck(True,'current 329 page/readme match snapshots and old 328 page/data unchanged')
# The old verifier expects the old page and README as current: replay it in an isolated previous view.
with tempfile.TemporaryDirectory(prefix='329-prior-view-') as td:
 t=Path(td)/'site';shutil.copytree(P,t,ignore=shutil.ignore_patterns('.git','__pycache__'));shutil.copyfile(B/'328-public-readme.md',t/'observations/README.md');shutil.copyfile(B/'328-current-homepage.html',t/'zodiac_trend.html');r=subprocess.run([sys.executable,str(t/'observations/2026328-deep-verify.py')],capture_output=True,text=True,timeout=240);assert r.returncode==0 and 'OFFLINE 328 DEEP REVIEW VERIFICATION PASS' in r.stdout,r.stdout+r.stderr
ck(True,'prior 328 deep verifier succeeds in isolated prior-current-page/readme view')
a=(B/'history-through-327.csv').read_bytes().splitlines(keepends=True);b=(O/'2026329-source-data.csv').read_bytes().splitlines(keepends=True);assert len(a)==1059 and len(b)==1060 and a[0]==b[0] and b[2:]==a[1:] and all(v.endswith(b'\r\n') for v in b)
with (O/'2026329-source-data.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
by={int(r['period']):r for r in rows};Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];nums=lambda r:[int(r[f'n{i}']) for i in range(1,7)];s6=lambda r:{r[f'z{i}'] for i in range(1,7)};s7=lambda r:s6(r)|{r['special_zodiac']};r=by[2026328];assert len(rows)==1059 and max(by)==2026328 and nums(r)==[15,21,31,5,12,47] and [r[f'z{i}'] for i in range(1,7)]==['龍','狗','鼠','虎','羊','猴'] and int(r['special'])==6 and r['special_zodiac']=='牛' and r['date']=='' and [sign(n) for n in nums(r)]==[r[f'z{i}'] for i in range(1,7)] and len(s6(r))==6 and len(s7(r))==7
ck(True,'exactly user-supplied 328 appended, all 1058 older records byte-identical; six normal vs separate seventh')
olddec=json.loads((B/'manual-decisions-through-328.json').read_text());newdec=J('2026329-manual-decisions.json');assert len(olddec['decisions'])==17 and len(newdec['decisions'])==18 and all(newdec['decisions'][k]==v for k,v in olddec['decisions'].items()) and all(str(x) not in newdec['decisions'] for x in (2026319,2026322,2026324));v=newdec['decisions']['2026329'];assert [v[k] for k in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','虎','鷄','鼠','羊'] and v['universe_zodiac']==['馬','虎','鷄','鼠','羊','蛇']
with tempfile.TemporaryDirectory(prefix='329-repro-') as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026329-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026329-manual-decisions.json',t/'data/manual_site_decisions.json');import os;env={**os.environ,'POOL_VERSION':'v5.0'};q=subprocess.run([sys.executable,str(O/'2026329-generator.py')],cwd=t,env=env,capture_output=True,text=True,timeout=90);assert q.returncode==0,q.stdout+q.stderr;assert H(t/'zodiac_trend.html')==H(t/'www/zodiac_trend.html')==H(O/'2026329-page.html')
ck(True,'17 old decisions preserved and original generator reproduces exact 329 page')
doc=J('2026329-retrospective.json');recs=doc['historical_outcomes'];assert len(recs)==35 and [x['period'] for x in recs]==[i for i in range(2026291,2026329) if i not in (2026319,2026322,2026324)];pat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});'
for x in recs:
 per=x['period'];row=by[per];ns=nums(row);got={sign(n) for n in ns};assert ns==x['normal_numbers'] and [sign(n) for n in ns]==x['normal_zodiacs'] and x['special_number']==int(row['special']) and x['special_zodiac']==row['special_zodiac']
 if per<=2026308:
  d=json.loads((F/f'prior-records/{per}.json').read_text())['site_display'];rr={'top':Z[d['top']],'A':Z[d['t2'][0]],'B':Z[d['t2'][1]],'C':Z[d['t3'][1]],'D':Z[d['t3'][2]]}
 else:
  path=B/'328-current-homepage.html' if per==2026328 else G/'327-current-homepage.html' if per==2026327 else F/f'historical-pages/{per}.html';d=json.loads(re.search(pat,path.read_text()).group(1))[str(per-1)];rr={k:Z[d[k]] for k in ('top','A','B','C','D')}
 assert x['roles']==rr;needs=[[rr['top']],[rr['A'],rr['B']],[rr['A'],rr['C'],rr['D']]]
 for sl,need in zip(x['slots'],needs):assert sl['required']==need and sl['present']==[z for z in need if z in got] and sl['missing']==[z for z in need if z not in got] and sl['complete']==set(need).issubset(got) and sl['balls']==[{'number':n,'zodiac':sign(n)} for n in ns if sign(n) in need]
 assert x['complete_columns']==sum(set(need)<=got for need in needs)
assert [sum(x['complete_columns']==i for x in recs) for i in range(4)]==[14,17,3,1] and [sum(x['slots'][i]['complete'] for x in recs) for i in range(3)]==[13,9,4] and [sl['missing'] for sl in recs[-1]['slots']]==[['馬'],['鷄'],['馬','蛇']]
with (O/'2026329-retrospective-history.csv').open(encoding='utf8',newline='') as f:tab=list(csv.DictReader(f))
assert len(tab)==35 and all(int(t['period'])==x['period'] and int(t['complete_columns'])==x['complete_columns'] and [t[k+'_hits'] for k in ('single','pair','triple')]==[f"{s['present_count']}/{s['needed_count']}" for s in x['slots']] and [t[k+'_missing'].split() for k in ('single','pair','triple')]==[s['missing'] for s in x['slots']] for t,x in zip(tab,recs))
ck(True,'35 saved versions/105 columns independently settled against historical raw files and CSV')
for x in doc['unpublished_reconstructions']:
 per=x['period'];d=json.loads((F/f'{per%1000}-reconstruction-manual.json').read_text());rr={'top':d['top'],'A':d['pair'][0],'B':d['pair'][1],'C':d['triple'][1],'D':d['triple'][2]};got=s6(by[per]);needs=[{rr['top']},{rr['A'],rr['B']},{rr['A'],rr['C'],rr['D']}];assert d['status']==x['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' and x['roles']==rr and x['complete_columns']==sum(n<=got for n in needs) and all(sl['present_count']==len(need&got) for sl,need in zip(x['slots'],needs))
assert [x['period'] for x in doc['unpublished_reconstructions']]==[2026319,2026322,2026324]
for a0,c in zip(json.loads((B/'328-candidates.json').read_text())['candidates'],doc['candidate_counterfactuals']):
 rr=a0['roles'];needs=[{rr['top']},{rr['A'],rr['B']},{rr['A'],rr['C'],rr['D']}];got=s6(r);assert a0['id']==c['id'] and a0['roles']==c['roles'] and c['complete_columns']==sum(n<=got for n in needs)==0 and all(sl['present_count']==len(need&got) for sl,need in zip(c['slots'],needs))
ck(True,'319/322/324 reconstructions separate; all 12 post-outcome 328 alternatives have zero complete columns')
# Rebuild historical cohort labels; do not apply the older 6/6 condition to 328's 6/7.
changes={(2024040,2024041),(2025028,2025029),(2026047,2026048)};pairs=[]
for a,b in zip(rows,rows[1:]):
 p,q=int(a['period']),int(b['period']);adj=(q==p+1) if p//1000==q//1000 else False
 if p//1000!=q//1000:
  try:adj=q//1000==p//1000+1 and q%1000==1 and (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days==1
  except ValueError:adj=False
 if not adj or (p,q) in changes or len(set(nums(a)+[int(a['special'])]))!=7 or len(set(nums(b)+[int(b['special'])]))!=7:continue
 if len(s6(a))==6:pairs.append((p,q,len(s7(a)),len(s6(a)&s6(b)),len(s7(a)&s7(b))))
st=J('2026329-six-sign-study.json');assert len(pairs)==263 and st['groups']['previous_six_6_seven_7']['n']==130 and st['groups']['previous_six_6_seven_6']['n']==133 and not st['current_pending']['target_result_queried_or_used']
for k in (6,7):
 xs=[x for x in pairs if x[2]==k];v=st['groups'][f'previous_six_6_seven_{k}'];assert v['n']==len(xs) and v['six_to_six_counts_0_to_6']==[sum(x[3]==i for x in xs) for i in range(7)] and v['seven_to_seven_counts_0_to_'+str(k)]==[sum(x[4]==i for x in xs) for i in range(k+1)]
ck(True,'6/7 and 6/6 cohort tables rebuilt separately; boundary mapping transitions excluded')
# Independent group polynomial for all 12 designs, plus exact conditional counts for selected plan.
aud=J('2026329-candidates.json');des=J('2026329-handwritten-design.json');model=J('2026329-brute-model.json');den=comb(49,6);groups={z:[n for n in range(1,50) if sign(n)==z] for z in Z};prev=s6(r);assert den==13983816==model['denominator'] and aud['status']=='PASS' and len(des['candidates'])==len(aud['candidates'])==12 and not aud['target_329_result_queried_or_used']
for d,x in zip(des['candidates'],aud['candidates']):
 rr=d['roles'];assert d['id']==x['id'] and d['roles']==x['roles'] and d['reserves']==x['reserves'];shown=set(rr.values());bits={z:1<<i for i,z in enumerate(sorted(shown,key=Z.index))};dp={(0,0):1}
 for z in Z:
  nxt=defaultdict(int)
  for (n,mask),w in dp.items():
   for take in range(min(len(groups[z]),6-n)+1):nxt[n+take,mask|(bits.get(z,0) if take else 0)]+=w*comb(len(groups[z]),take)
  dp=nxt
 counts=Counter();dist=[0]*4
 for (n,mask),w in dp.items():
  if n!=6:continue
  got={z for z,bit in bits.items() if mask&bit};s={rr['top']}<=got;p={rr['A'],rr['B']}<=got;t={rr['A'],rr['C'],rr['D']}<=got;v=s+p+t;dist[v]+=w;counts['single']+=w*s;counts['pair']+=w*p;counts['triple']+=w*t;counts['all_columns']+=w*(v==3);counts['no_complete_column']+=w*(v==0);counts['at_least_one_complete']+=w*(v>0);counts['at_least_two_complete']+=w*(v>=2);counts['pair_and_triple']+=w*(p and t)
 assert dict(counts)==x['ideal_model']['counts'] and dist==x['ideal_model']['exact_complete_column_distribution'] and sum(dist)==den
for label,key in [('chosen','selected'),('old','previous_328_CC01_ideal_comparison')]:
 v=aud[key]['ideal_model'] if label=='chosen' else aud[key];b=model[label];assert v['exact_complete_column_distribution']==b['distribution'] and all(v['counts'][k]==b[k] for k in ('single','pair','triple','pair_and_triple'))
assert [x['all_columns']>0 for x in aud['selected_conditional_on_repeat_0_to_6']]==[False,False,False,True,True,False,False]
for k,(x,b) in enumerate(zip(aud['selected_conditional_on_repeat_0_to_6'],model['conditional'])):assert sum(b['distribution'])==x['denominator'] and b['distribution'][0]==x['no_complete_column'] and b['distribution'][3]==x['all_columns'] and all(b[n]==x[n] for n in ('single','pair','triple'))
ck(True,'12 exact fair-model designs reproduced; selected/old distributions and repeat conditions match independently enumerated 13,983,816 sets')
report=(O/'2026329-analysis.md').read_text();index=(O/'2026329-index.html').read_text();readme=(O/'README.md').read_text();assert all(x in report for x in ('零完整栏','**虎、鷄**','**虎、鼠、羊**','前六6肖、七球7肖','130','133','不能保证329命中或收益','13,983,816')) and all(x in index for x in ('单馬、二虎鷄、三虎鼠羊','35份','319、322、324','未认证')) and '2026329-index.html' in readme and '2026328-deep-index.html' in readme
for name,text in [('2026329-analysis.md',report),('2026329-index.html',index)]:
 links=re.findall(r'href="([^"]+)"',text) if name.endswith('.html') else re.findall(r'\]\(([^)]+)\)',text)
 for x in links:
  if not x.startswith(('http://','https://','#','mailto:')):assert (O/x).is_file(),(name,x)
for f in ('2026329-evidence-qc.json','2026329-candidates-qc.json','2026329-retrospective-qc.json','2026329-local-static-qc.json','2026329-local-browser-qc.json','2026329-local-mobile-qc.json','2026329-local-index-qc.json','2026329-local-bottom-qc.json','2026329-local-scroll-qc.json','2026329-report-qc.json'):assert J(f)['status']=='PASS',f
ck(True,'report/index links and independent local QA results agree; scope restrictions retained')
print('OFFLINE 328 REVIEW / 329 DISPLAY VERIFICATION PASS: '+str(len(checks))+' checks — internal bytes and arithmetic only; NOT official draw, pre-draw, actual odds, forecast, profit or real WeChat safety')
