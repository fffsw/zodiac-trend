#!/usr/bin/env python3
"""Portable 329 review/330 display verifier; never queries a draw or authenticates timing.
Run from an extracted site root: python observations/2026330-verify.py
"""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import date
from math import comb
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;P=O.parent;F=O/'2026327-retrospective-frozen';G=O/'2026328-retrospective-frozen';I=O/'2026329-retrospective-frozen';B=O/'2026330-retrospective-frozen';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda n:json.loads((O/n).read_text(encoding='utf8'));checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
def verify(path,base):
 seen=set()
 for line in path.read_text(encoding='utf8').splitlines():
  h,rel=line.split('  ',1);p=(base/rel).resolve();assert p.is_relative_to(P.resolve()) and p.is_file() and rel not in seen and H(p)==h,(path.name,rel);seen.add(rel)
 return len(seen)
old=('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256','2026327.sha256','2026328.sha256','2026328-correction.sha256','2026328-deep-inputs.sha256','2026328-deep.sha256','2026329.sha256')
assert all(verify(O/n,O)>0 for n in old) and verify(O/'2026330.sha256',O)>=45 and verify(O/'2026330-frozen.sha256',B)>=20 and verify(O/'2026327-before.sha256',F)>=60 and verify(O/'2026328-before.sha256',G)>=20 and verify(O/'2026329-frozen.sha256',I)>=20
ck(True,'25 earlier manifests, 330 manifest and frozen source manifests')
assert H(P/'zodiac_trend.html')==H(O/'2026330-page.html') and H(O/'README.md')==H(O/'2026330-readme-snapshot.md') and H(B/'329-current-homepage.html')==H(O/'2026329-page.html') and H(B/'history-through-328.csv')==H(O/'2026329-source-data.csv')
ck(True,'current page/readme match snapshots and old 329 page/data unchanged')
# Old verifier expects old root page and README to be current: replay in an isolated old view.
with tempfile.TemporaryDirectory(prefix='330-prior-view-') as td:
 t=Path(td)/'site';shutil.copytree(P,t,ignore=shutil.ignore_patterns('.git','__pycache__'));shutil.copyfile(B/'329-public-readme.md',t/'observations/README.md');shutil.copyfile(B/'329-current-homepage.html',t/'zodiac_trend.html');r=subprocess.run([sys.executable,str(t/'observations/2026329-verify.py')],capture_output=True,text=True,timeout=300);assert r.returncode==0 and 'OFFLINE 328 REVIEW / 329 DISPLAY VERIFICATION PASS' in r.stdout,r.stdout+r.stderr
ck(True,'prior 329 verifier succeeds in isolated prior-current-page/readme view')
a=(B/'history-through-328.csv').read_bytes().splitlines(keepends=True);b=(O/'2026330-source-data.csv').read_bytes().splitlines(keepends=True);assert len(a)==1060 and len(b)==1061 and a[0]==b[0] and b[2:]==a[1:] and all(v.endswith(b'\r\n') for v in b)
with (O/'2026330-source-data.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
by={int(r['period']):r for r in rows};Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];nums=lambda r:[int(r[f'n{i}']) for i in range(1,7)];s6=lambda r:{r[f'z{i}'] for i in range(1,7)};s7=lambda r:s6(r)|{r['special_zodiac']};r=by[2026329];assert len(rows)==1060 and max(by)==2026329 and nums(r)==[45,6,46,33,31,40] and [r[f'z{i}'] for i in range(1,7)]==['狗','牛','鷄','狗','鼠','兔'] and int(r['special'])==44 and r['special_zodiac']=='豬' and r['date']=='' and [sign(n) for n in nums(r)]==[r[f'z{i}'] for i in range(1,7)] and len(s6(r))==5 and len(s7(r))==6
ck(True,'one user-supplied 329 appended, all 1059 old records byte-identical; first-six/seventh inferred')
olddec=json.loads((B/'manual-decisions-through-329.json').read_text());newdec=J('2026330-manual-decisions.json');assert len(olddec['decisions'])==18 and len(newdec['decisions'])==19 and all(newdec['decisions'][k]==v for k,v in olddec['decisions'].items()) and all(str(x) not in newdec['decisions'] for x in (2026319,2026322,2026324));v=newdec['decisions']['2026330'];assert [v[k] for k in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','鷄','牛','龍','虎'] and v['universe_zodiac']==['馬','鷄','牛','龍','虎','蛇']
with tempfile.TemporaryDirectory(prefix='330-repro-') as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026330-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026330-manual-decisions.json',t/'data/manual_site_decisions.json');env={**os.environ,'POOL_VERSION':'v5.0'};q=subprocess.run([sys.executable,str(O/'2026330-generator.py')],cwd=t,env=env,capture_output=True,text=True,timeout=90);assert q.returncode==0,q.stdout+q.stderr;assert H(t/'zodiac_trend.html')==H(t/'www/zodiac_trend.html')==H(O/'2026330-page.html')
ck(True,'18 old decisions preserved; unchanged generator reproduces exact 330 page')
doc=J('2026330-retrospective.json');recs=doc['historical_outcomes'];first=J('2026330-correction-original.json');previous=J('2026329-retrospective.json');assert len(recs)==36 and [x['period'] for x in recs]==[i for i in range(2026291,2026330) if i not in (2026319,2026322,2026324)] and len(first['historical_outcomes'])==36 and len(previous['historical_outcomes'])==35;pat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';known=[];unknown=[];hit=[]
with (O/'2026330-reserve-audit.csv').open(encoding='utf8',newline='') as f:reserve_tab=list(csv.DictReader(f))
assert len(reserve_tab)==36
for idx,(x,orig,tab) in enumerate(zip(recs,first['historical_outcomes'],reserve_tab)):
 per=x['period'];row=by[per];ns=nums(row);got={sign(n) for n in ns};assert ns==x['normal_numbers'] and [sign(n) for n in ns]==x['normal_zodiacs'] and x['special_number']==int(row['special']) and x['special_zodiac']==row['special_zodiac'] and int(tab['period'])==per
 if per<=2026308:
  v=json.loads((F/f'prior-records/{per}.json').read_text())['site_display'];rr={'top':Z[v['top']],'A':Z[v['t2'][0]],'B':Z[v['t2'][1]],'C':Z[v['t3'][1]],'D':Z[v['t3'][2]]};u=v.get('universe_zodiac')
  if u is None:assert 'universe' not in v and 'selection_zodiac' not in v
 else:
  path=B/'329-current-homepage.html' if per==2026329 else I/'328-current-homepage.html' if per==2026328 else G/'327-current-homepage.html' if per==2026327 else F/f'historical-pages/{per}.html';v=json.loads(re.search(pat,path.read_text()).group(1))[str(per-1)];rr={k:Z[v[k]] for k in ('top','A','B','C','D')};u=[Z[i] for i in v['U']]
 assert x['roles']==rr;needs=[[rr['top']],[rr['A'],rr['B']],[rr['A'],rr['C'],rr['D']]]
 for sl,need in zip(x['slots'],needs):assert sl['required']==need and sl['present']==[z for z in need if z in got] and sl['missing']==[z for z in need if z not in got] and sl['complete']==set(need).issubset(got) and sl['balls']==[{'number':n,'zodiac':sign(n)} for n in ns if sign(n) in need]
 assert x['complete_columns']==sum(set(need)<=got for need in needs) and x['slots']==orig['slots'] and x['complete_columns']==orig['complete_columns']
 if idx<35:assert all(x[k]==previous['historical_outcomes'][idx][k] for k in ('period','roles','normal_numbers','normal_zodiacs','slots','complete_columns','displayed_hits','shared_missing'))
 shown=set(rr.values())
 if u is None:
  unknown.append(per);assert x['reserve_hits'] is None and x['outside_universe_hits'] is None and set(x['unknown_nondisplay_hits'])==got-shown and tab['classification_status']=='NOT_PROVEN_IN_RETAINED_SOURCE'
 else:
  known.append(per);res=set(u)-shown;hits=got&res
  if hits:hit.append(per)
  assert len(set(u))==6 and shown<=set(u) and set(x['universe_zodiacs'])==set(u) and set(x['unallocated_universe_zodiacs'])==res and set(x['reserve_hits'])==hits and set(x['outside_universe_hits'])==got-set(u) and set(tab['non_column_hits_in_inferred_first_six'].split())==hits
assert [sum(x['complete_columns']==i for x in recs) for i in range(4)]==[15,17,3,1] and [sum(x['slots'][i]['complete'] for x in recs) for i in range(3)]==[13,9,4] and [sl['missing'] for sl in recs[-1]['slots']]==[['馬'],['虎'],['虎','羊']]
assert len(known)==28 and unknown==list(range(2026291,2026299)) and hit==[2026299,2026303,2026304,2026305,2026306,2026308,2026309,2026310,2026312,2026314,2026315,2026321,2026323,2026328] and recs[-2]['reserve_hits']==['虎'] and recs[-1]['reserve_hits']==[]
with (O/'2026330-retrospective-history.csv').open(encoding='utf8',newline='') as f:tab=list(csv.DictReader(f))
assert len(tab)==36 and all(int(t['period'])==x['period'] and int(t['complete_columns'])==x['complete_columns'] and [t[k+'_hits'] for k in ('single','pair','triple')]==[f"{s['present_count']}/{s['needed_count']}" for s in x['slots']] and [t[k+'_missing'].split() for k in ('single','pair','triple')]==[s['missing'] for s in x['slots']] for t,x in zip(tab,recs))
assert J('2026330-reserve-qc.json')['status']=='PASS' and J('2026330-retrospective-qc.json')['retrospective_sha256']==H(O/'2026330-retrospective.json') and J('2026330-correction-initial-qc.json')['retrospective_sha256']==H(O/'2026330-correction-original.json')
ck(True,'36 saved versions/108 formal columns and corrected 28 known vs 8 unknown universes independently settled; first review preserved')
for x,orig in zip(doc['unpublished_reconstructions'],first['unpublished_reconstructions']):
 per=x['period'];v=json.loads((F/f'{per%1000}-reconstruction-manual.json').read_text());rr={'top':v['top'],'A':v['pair'][0],'B':v['pair'][1],'C':v['triple'][1],'D':v['triple'][2]};got=s6(by[per]);needs=[{rr['top']},{rr['A'],rr['B']},{rr['A'],rr['C'],rr['D']}];res=set(v['universe'])-set(rr.values());assert v['status']==x['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' and x['roles']==rr and x['complete_columns']==sum(n<=got for n in needs) and x['slots']==orig['slots'] and set(x['reserve_hits'])==res&got and set(x['outside_universe_hits'])==got-set(v['universe'])
assert [x['period'] for x in doc['unpublished_reconstructions']]==[2026319,2026322,2026324] and [x['period'] for x in doc['unpublished_reconstructions'] if x['reserve_hits']]==[2026322,2026324]
for a0,c in zip(json.loads((B/'329-candidates.json').read_text())['candidates'],doc['candidate_counterfactuals']):
 rr=a0['roles'];needs=[{rr['top']},{rr['A'],rr['B']},{rr['A'],rr['C'],rr['D']}];got=s6(r);assert a0['id']==c['id'] and a0['roles']==c['roles'] and c['complete_columns']==sum(n<=got for n in needs) and all(sl['present_count']==len(need&got) for sl,need in zip(c['slots'],needs))
assert Counter(x['complete_columns'] for x in doc['candidate_counterfactuals'])=={0:8,1:4}
ck(True,'319/322/324 reconstructions separate; 12 prior alternatives hindsight-only')
changes={(2024040,2024041),(2025028,2025029),(2026047,2026048)};pairs=[]
for a,b in zip(rows,rows[1:]):
 p,q=int(a['period']),int(b['period']);adj=(q==p+1) if p//1000==q//1000 else False
 if p//1000!=q//1000:
  try:adj=q//1000==p//1000+1 and q%1000==1 and (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days==1
  except ValueError:adj=False
 if not adj or (p,q) in changes or len(set(nums(a)+[int(a['special'])]))!=7 or len(set(nums(b)+[int(b['special'])]))!=7:continue
 if len(s6(a)) in (5,6):pairs.append((p,q,len(s6(a)),len(s7(a)),len(s6(a)&s6(b)),len(s7(a)&s7(b))))
st=J('2026330-six-sign-study.json');assert len(pairs)==835 and st['groups']['previous_six_5_seven_6']['n']==344 and st['groups']['previous_six_5_seven_5']['n']==227 and not st['current_pending']['target_result_queried_or_used']
for n,k in ((5,5),(5,6),(6,6),(6,7)):
 xs=[x for x in pairs if x[2:4]==(n,k)];v=st['groups'][f'previous_six_{n}_seven_{k}'];assert v['n']==len(xs) and v['six_to_six_counts_0_to_'+str(n)]==[sum(x[4]==i for x in xs) for i in range(n+1)] and v['seven_to_seven_counts_0_to_'+str(k)]==[sum(x[5]==i for x in xs) for i in range(k+1)]
with (O/'2026330-six-sign-pairs.csv').open(encoding='utf8',newline='') as f:tab=list(csv.DictReader(f))
assert len(tab)==len(pairs) and all(x==(int(t['previous']),int(t['next']),int(t['prev6_distinct']),int(t['prev7_distinct']),int(t['repeat6_count']),int(t['repeat7_count'])) for x,t in zip(pairs,tab))
ck(True,'835 historical 5/5, 5/6, 6/6 and 6/7 pairs reproduced separately; 330 not in denominator')
# Independent group polynomial for all 12 designs plus previously independently enumerated counts.
aud=J('2026330-candidates.json');des=J('2026330-handwritten-design.json');model=J('2026330-brute-model.json');den=comb(49,6);groups={z:[n for n in range(1,50) if sign(n)==z] for z in Z};assert den==13983816==model['denominator'] and aud['status']=='PASS' and len(des['candidates'])==len(aud['candidates'])==12 and not aud['target_330_result_queried_or_used']
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
assert aud['selected']['ideal_model']==aud['previous_329_DD01_ideal_comparison'] and model['chosen']==model['old'] and model['chosen']['distribution']==[5392128,7401592,1144016,46080] and [x['all_columns']>0 for x in aud['selected_conditional_on_repeat_0_to_5']]==[False,False,True,True,False,False]
for x,b in zip(aud['selected_conditional_on_repeat_0_to_5'],model['conditional']):assert sum(b['distribution'])==x['denominator'] and b['distribution'][0]==x['no_complete_column'] and b['distribution'][3]==x['all_columns'] and all(b[n]==x[n] for n in ('single','pair','triple'))
ck(True,'12 fair-model designs via group polynomials; chosen/old equality and repeat conditions match enumerated 13,983,816 sets')
report=(O/'2026330-analysis.md').read_text();index=(O/'2026330-index.html').read_text();readme=(O/'README.md').read_text();assert all(x in report for x in ('零完整栏','**鷄、牛**','**鷄、龍、虎**','前六5肖、七球6肖','344','227','13,983,816','尚未明确确认该球次划分','14期至少一个非栏目肖','没有模型上的整体优势')) and all(x in index for x in ('单馬、二鷄牛、三鷄龍虎','36份','319、322、324','未认证','用户尚未明确确认球次','遗漏已纠正')) and '2026330-index.html' in readme and '2026329-index.html' in readme
for name,text in [('2026330-analysis.md',report),('2026330-index.html',index)]:
 links=re.findall(r'href="([^"]+)"',text) if name.endswith('.html') else re.findall(r'\]\(([^)]+)\)',text)
 for x in links:
  if not x.startswith(('http://','https://','#','mailto:')):assert (O/x).is_file(),(name,x)
for f in ('2026330-evidence-qc.json','2026330-candidates-qc.json','2026330-retrospective-qc.json','2026330-reserve-qc.json','2026330-local-static-qc.json','2026330-local-browser-qc.json','2026330-local-mobile-qc.json','2026330-local-index-qc.json','2026330-report-qc.json'):assert J(f)['status']=='PASS',f
ck(True,'report/index links and independent QA agree; reserve correction, unconfirmed partition and model limits disclosed')
print('OFFLINE 329 REVIEW / 330 DISPLAY VERIFICATION PASS: '+str(len(checks))+' checks — internal bytes and arithmetic only; NOT official draw, pre-draw, actual odds, forecast, profit or real WeChat safety')
