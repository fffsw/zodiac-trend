#!/usr/bin/env python3
"""Offline independent verification of the 326 revision; not a forecast or pre-draw proof.
Run: python3 2026326-rev1-verify.py from any directory, with the complete observations tree.
"""
from pathlib import Path
from collections import Counter
from datetime import date
from itertools import product,combinations
from math import comb
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;J=lambda p:json.loads((O/p).read_text(encoding='utf8'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
def manifest(file,base):
 seen=set();n=0
 for line in (O/file).read_text().splitlines():
  h,p=line.split('  ',1);f=(base/p).resolve();assert f.is_relative_to(base.resolve()) and p not in seen and f.is_file() and H(f)==h,(file,p);seen.add(p);n+=1
 return n
ck(manifest('2026326.sha256',O)>100 and manifest('2026326-rev1.sha256',O)>30 and manifest('2026326-rev1-before.sha256',O/'2026326-rev1-frozen')==24,'earlier original manifest, new revision manifest and 24 original frozen inputs all match')
r=subprocess.run([sys.executable,str(O/'2026326-verify.py')],capture_output=True,text=True,timeout=120);ck(r.returncode==0 and 'OFFLINE 325 REVIEW / FOUR-SIGN STUDY / 326 DISPLAY VERIFICATION PASS' in r.stdout,'prior 326 original portable verifier still passes')
def readcsv(p):
 with (O/p).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
raw=readcsv('2026326-rev1-frozen/445-source-through-311.csv');hist=readcsv('2026326-source-data.csv');u=J('2026325-user-result.json');rows=[]
for x in raw:rows.append((int(x['period']),x['date'],[int(n) for n in x['numbers'].split()],x['zodiacs'].split(),x['usable']=='1'))
for x in reversed(hist):
 if 2026312<=int(x['period'])<=2026325:rows.append((int(x['period']),x['date'],[int(x[f'n{i}']) for i in range(1,7)]+[int(x['special'])],[x[f'z{i}'] for i in range(1,7)]+[x['special_zodiac']],True))
assert len(rows)==2506 and len(hist)==1056 and rows[-1][0]==2026325 and rows[-1][2]==u['normal_numbers']+[u['seventh_number']] and all(x[0]<=2026325 for x in rows)
ck(True,'raw year-specific identities and user 325 are reproduced without reading a 326 outcome')
def adjacent(a,b):
 if a[0]//1000==b[0]//1000:return b[0]==a[0]+1
 if b[0]//1000==a[0]//1000+1 and b[0]%1000==1:
  try:return (date.fromisoformat(b[1])-date.fromisoformat(a[1])).days==1
  except ValueError:return False
 return False
pairs=[(a,b) for a,b in zip(rows,rows[1:]) if a[4] and b[4] and adjacent(a,b)];assert len(pairs)==2501
st=J('2026326-rev1-maximum-study.json');assert st['valid_adjacent_pairs']==len(pairs) and not st['target_326_outcome_read']
for key,fun in [('both_four_2024plus',lambda a:a[0]>=2024001 and len(set(a[3][:6]))==len(set(a[3]))==4),('both_four_2020plus',lambda a:len(set(a[3][:6]))==len(set(a[3]))==4),('both_four_shape_325_2024plus',lambda a:a[0]>=2024001 and len(set(a[3][:6]))==len(set(a[3]))==4 and sorted(Counter(a[3][:6]).values(),reverse=True)==[2,2,1,1] and sorted(Counter(a[3]).values(),reverse=True)==[2,2,2,1])]:
 group=[(a,b) for a,b in pairs if fun(a)]
 for label,num in [('next_six_repeat',6),('next_seven_repeat',7)]:
  val=[len(set(a[3][:num])&set(b[3][:num])) for a,b in group];g=st['historical_groups'][key][label];assert g['n']==len(group) and g['counts_0_to_4']==[val.count(i) for i in range(5)] and g['maximum_observed']==max(val) and g['maximum_observed_count']==val.count(max(val));assert {(x['previous'],x['next']) for x in g['max_example_pairs']}=={(a[0],b[0]) for (a,b),v in zip(group,val) if v==max(val)}
wider=[(a,b) for a,b in pairs if a[0]>=2024001 and len(set(a[3][:6]))==4];assert [sum(len(set(a[3][:6])&set(b[3][:6]))==r for a,b in wider) for r in range(5)]==[18,65,80,33,5] and len(wider)==201
prev=set(rows[-1][3][:6]);assert prev==set(rows[-1][3])=={'虎','馬','鷄','龍'} and st['theoretical_maximum_repeat_six']==st['theoretical_maximum_repeat_seven']==4
for n in (6,7):
 valid=[x for x in rows if x[4] and x[0]>=2024001];v=Counter(len(set(x[3][:n])) for x in valid);m=st['distinct_counts_2024plus'][str(n)];assert len(valid)==m['n'] and {str(k):count for k,count in sorted(v.items())}==m['counts'] and min(v)==3
ck(True,'48/31/113 joint-trigger distributions, maxima, wider 201-pair sensitivity and fewer-than-four examples independently recounted')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');f=lambda n:Z[(7-n)%12];sizes={z:sum(f(n)==z for n in range(1,50)) for z in Z};den=comb(49,6);design=J('2026326-rev1-design.json');model=J('2026326-rev1-model.json');dec=J('2026326-rev1-decision.json');assert len(design['plans'])==len(model['plans'])==11 and model['model_denominator']==den and model['sign_number_sizes']==sizes
for p,q in zip(design['plans'],model['plans']):
 assert p['id']==q['id'] and p['roles']==q['roles'];t=p['roles'];ss=[{t['top']},{t['A'],t['B']},{t['A'],t['C'],t['D']}];universe=prev|set(t.values());universe=sorted(universe,key=Z.index);other=49-sum(sizes[z] for z in universe);tot=[0]*4;columns=[0]*3;rc=[[0]*4 for _ in range(5)];tr=[0]*5
 for v in product(*(range(sizes[z]+1) for z in universe)):
  rem=6-sum(v)
  if not 0<=rem<=other:continue
  w=comb(other,rem)
  for z,k in zip(universe,v):w*=comb(sizes[z],k)
  active={z for z,k in zip(universe,v) if k};flags=[s<=active for s in ss];n=sum(flags);r=len(prev&active);tot[n]+=w;rc[r][n]+=w;tr[r]+=w*flags[2]
  for j,v in enumerate(flags):columns[j]+=w*v
 assert sum(tot)==den and tot==q['complete_columns_numerator_0_to_3'] and columns==q['single_pair_triple_numerators']
 for i in range(5):assert rc[i]==q['by_repeat_count'][str(i)]['complete_columns_numerator_0_to_3'] and tr[i]==q['by_repeat_count'][str(i)]['three_complete_numerator'] and sum(rc[i])==model['repeat_0_to_4_numerators'][i]
old,new=model['plans'][0],model['plans'][1];assert old['id']=='R00' and new['id']=='R01' and old['percent']==new['percent'] and new['roles']=={'top':'羊','A':'虎','B':'羊','C':'馬','D':'鷄'} and new['reserve_only']==['龍','蛇'] and dec['source_in_earlier_38']=='AA16';assert new['by_repeat_count']['4']['three_complete_numerator']==model['repeat_0_to_4_numerators'][4] and all(new['by_repeat_count'][str(i)]['three_complete_numerator']==0 for i in range(3))
ck(True,'all 11 exact ideal models independently category-enumerated; revised and original have equal unconditional baseline and different conditional risk')
oldm=J('2026326-manual-decisions.json');newm=J('2026326-rev1-manual-decisions.json');assert set(oldm['decisions'])==set(newm['decisions']) and all(oldm['decisions'][k]==v for k,v in newm['decisions'].items() if k!='2026326') and newm['decisions']['2026326']['universe_zodiac']==['羊','虎','馬','鷄','龍','蛇'];assert [newm['decisions']['2026326'][k] for k in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['羊','虎','羊','馬','鷄'] and '2026324' not in newm['decisions']
a=(O/'2026326-page.html').read_text();b=(O/'2026326-rev1-page.html').read_text();pat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';ma=json.loads(re.search(pat,a).group(1));mb=json.loads(re.search(pat,b).group(1));assert re.sub(pat,'<MANUAL>',a)==re.sub(pat,'<MANUAL>',b) and all(mb[k]==v for k,v in ma.items() if k!='2026325') and mb['2026325']=={'U':[7,2,6,9,4,5],'top':7,'A':2,'B':7,'C':6,'D':9,'top_overlap_mode':'concentrated'}
with tempfile.TemporaryDirectory(prefix='326-rev1-verify-') as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(O/'2026326-source-data.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026326-rev1-manual-decisions.json',t/'data/manual_site_decisions.json');subprocess.run([sys.executable,str(O/'2026326-generator.py')],cwd=t,env={**os.environ,'POOL_VERSION':'v5.0'},check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026326-rev1-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
ck(True,'all earlier decisions and HTML outside target payload unchanged; previous generator reproduces both revised page copies')
report=(O/'2026326-rev1-analysis.md').read_text();index=(O/'2026326-rev1-index.html').read_text();assert all(x in report for x in ('理论上限：4肖','前六观察最大值：3肖','七球观察最大值：4肖','前六重0、1或2肖','不是326的实际号码或预测号码','不能证明赛前')) and all(x in index for x in ('单羊','二虎羊','三虎馬鷄','龍蛇仅替补','不是预测保证'))
for link in re.findall(r'\]\(([^)]+)\)',report):
 if not link.startswith(('http://','https://','#')):assert (O/link).is_file(),link
for link in re.findall(r'href="([^"]+)"',index):
 if not link.startswith(('http://','https://','#','mailto:')):assert (O/link).is_file(),link
ck(True,'current explanatory report, archival links and revision index agree and all relative file links resolve')
print('OFFLINE 326 REVISION VERIFICATION PASS: '+str(len(checks))+' checks — not official source, predraw timing, actual fairness, WeChat safety, predictive advantage or returns')
