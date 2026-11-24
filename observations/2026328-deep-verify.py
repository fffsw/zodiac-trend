#!/usr/bin/env python3
"""Portable offline verifier for the 328 deep-review addendum.
From any cwd: python3 observations/2026328-deep-verify.py
Checks artifacts and internal calculations, not official outcome, predraw timing or prediction.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from math import comb
from datetime import date
import csv,hashlib,json,re,shutil,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;P=O.parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads((O/p).read_text(encoding='utf8'));checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
def verify(n,base,root):
 seen=set()
 for line in (O/n).read_text(encoding='utf8').splitlines():
  h,rel=line.split('  ',1);p=(base/rel).resolve();assert p.is_relative_to(root.resolve()) and p.is_file() and rel not in seen and H(p)==h,(n,rel);seen.add(rel)
 return len(seen)
old=('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256','2026327.sha256','2026328.sha256','2026328-correction.sha256')
assert all(verify(m,O,P)>0 for m in old) and verify('2026328-deep.sha256',O,P)>=12 and verify('2026328-deep-inputs.sha256',O,P)>=16
assert H(O/'2026328.sha256')=='27d2ac0559a4292fdd69c7937fa4b9af29aa64aac41c6ba512cb0440ca150175' and H(O/'2026328-correction.sha256')=='a46fa85359f671571d48ee495f4fc3610600faa795b5ff8e11045df2353bab4e'
ck(True,'22 prior manifests, deep manifest and public frozen-input manifest all pass without replacing old artifacts')
assert H(O/'README.md')==H(O/'2026328-deep-readme-snapshot.md') and H(P/'zodiac_trend.html')==H(O/'2026328-page.html')=='aa129f740c671492e941080f17d16410beb2757a3fdf224c039e756e1350713a'
ck(True,'current README equals deep snapshot while the 328 homepage remains byte-for-byte unchanged')
with tempfile.TemporaryDirectory(prefix='328-deep-prior-') as td:
 t=Path(td)/'site';shutil.copytree(P,t,ignore=shutil.ignore_patterns('.git','__pycache__'));(t/'observations/README.md').unlink();shutil.copyfile(O/'2026328-corrected-readme-snapshot.md',t/'observations/README.md');r=subprocess.run([sys.executable,str(t/'observations/2026328-correction-verify.py')],capture_output=True,text=True,timeout=240);assert r.returncode==0 and 'OFFLINE CORRECTED 327 REVIEW / 328 DISPLAY VERIFICATION PASS' in r.stdout,r.stdout+r.stderr
ck(True,'previous correction verifier and nested historical verifiers replay in their isolated prior-README view')
d=J('2026328-deep-metrics.json');q=J('2026328-deep-qc.json');assert d['status']=='PASS_DEEP_REVIEW_NOT_A_FORECAST' and q['status']=='PASS_INDEPENDENT_DEEP_REVIEW' and not d['target_328_outcome_queried_or_used'] and q['deep_metrics_sha256']==H(O/'2026328-deep-metrics.json');Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');den=comb(49,6);groups=lambda off:{z:{n for n in range(1,50) if Z[(off-n)%12]==z} for z in Z};G=groups(7);altG=groups(8);assert len(G['馬'])==5 and all(len(G[z])==4 for z in Z if z!='馬')
def ie(g,plan):
 names=sorted(set().union(*plan));c=Counter()
 for mask in range(1<<len(names)):
  pres={z for i,z in enumerate(names) if mask&(1<<i)};N=49-sum(len(g[z]) for z in names if z not in pres);w=0
  for k in range(len(pres)+1):
   for subset in combinations(pres,k):
    left=N-sum(len(g[z]) for z in subset)
    if left>=6:w+=(-1)**k*comb(left,6)
  assert w>=0;c[''.join('1' if p<=pres else '0' for p in plan)]+=w
 for i in range(8):c.setdefault(f'{i:03b}',0)
 assert sum(c.values())==den
 return dict(sorted(c.items()))
cc=[{'馬'},{'狗','鷄'},{'狗','馬','蛇'}];bb=[{'馬'},{'鷄','龍'},{'鷄','虎','牛'}];models=d['ideal_model'];assert ie(G,cc)==models['CC01']['patterns_single_pair_triple'] and ie(G,bb)==models['BB01']['patterns_single_pair_triple'] and ie(altG,cc)==models['hypothetical_offset8_not_a_328_mapping_claim']['patterns_single_pair_triple']
for name in ('CC01','BB01','hypothetical_offset8_not_a_328_mapping_claim'):
 x=models[name];counts=[sum(w for p,w in x['patterns_single_pair_triple'].items() if p.count('1')==i) for i in range(4)];assert counts==x['complete_columns_0_to_3_counts'] and all(abs(100*a/den-b)<1e-10 for a,b in zip(counts,x['complete_columns_0_to_3_pct']))
assert models['CC01']['patterns_single_pair_triple']['001']==models['CC01']['patterns_single_pair_triple']['011']==0 and models['CC01']['complete_columns_0_to_3_counts']==[5728968,6766768,1256160,231920] and models['BB01']['complete_columns_0_to_3_counts']==[5392128,7401592,1144016,46080] and models['identical_ideal_distribution_role_permutations']==11*10*9
ck(True,'exact ideal joint distributions, hypothetical mapping variant, triple-implies-single and 990 symmetry configurations reproduced')
prev={'鼠','虎','馬','羊','鷄','狗'};pos=defaultdict(set);cd=[Counter() for _ in range(7)]
for size in range(1,7):
 for chosen in combinations(Z,size):
  s=set(chosen);n=sum(len(G[z]) for z in s)
  if n<6:continue
  w=0
  for j in range(size+1):
   for sub in combinations(chosen,j):
    left=n-sum(len(G[z]) for z in sub)
    if left>=6:w+=(-1)**j*comb(left,6)
  assert w>0;k=len(s&prev);h=[p<=s for p in cc];pos[k].add(sum(h));v=cd[k];v['denominator']+=w;v['single']+=w*h[0];v['pair']+=w*h[1];v['triple']+=w*h[2];v['all_columns']+=w*all(h);v['no_complete_column']+=w*(not any(h))
assert {str(k):sorted(v) for k,v in pos.items()}==d['logical_repeat_possibilities'] and pos[5]=={1,2,3} and pos[6]=={2} and sum(x['denominator'] for x in cd)==den
for k,v in enumerate(d['conditional_model_by_repeat']):assert v['repeat']==k and all(v[x]==cd[k][x] for x in ('denominator','single','pair','triple','all_columns','no_complete_column'))
ck(True,'all possible prior-six repeat conditions and exact conditional weights independently recomputed')
with (O/'2026328-source-data.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
nums=lambda r:[int(r[f'n{i}']) for i in range(1,7)]+[int(r['special'])];zs=lambda r:[r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']];offset=[]
for r in rows:
 values={(Z.index(z)+n)%12 for n,z in zip(nums(r),zs(r))};assert len(values)==1 and len(set(nums(r)))==7;offset.append(values.pop())
assert len(rows)==1058 and max(int(r['period']) for r in rows)==2026327 and nums(rows[-1])==[21,49,7,41,46,36,45] and [int(r['period']) for r in rows if not r['date']]==list(range(2026313,2026328))
changes=[(int(rows[i-1]['period']),int(rows[i]['period'])) for i in range(1,len(rows)) if offset[i-1]!=offset[i]];cohort=[i for i in range(1,len(rows)) if len(set(zs(rows[i-1])[:6]))==len(set(zs(rows[i-1])))==6];assert changes==[(2024040,2024041),(2025028,2025029),(2026047,2026048)] and len(cohort)==132 and all(offset[i-1]==offset[i] for i in cohort)
ck(True,'1058 local rows, missing dates, internal label transitions and absence of boundary pairs in selected cohort reproduced')
recent=list(reversed(rows[-45:]));
for lo,hi,b in zip((0,10,20,35,40),(9,19,34,39,44),d['recent_45_retrospective']['blocks']):
 sub=recent[lo:hi+1];dist=lambda plan:[sum(sum(p<=set(zs(r)[:6]) for p in plan)==i for r in sub) for i in range(4)];assert b['CC01_complete_columns_0_to_3']==dist(cc) and b['BB01_complete_columns_0_to_3']==dist(bb)
assert d['recent_45_retrospective']['CC01_distribution_0_to_3']==[16,19,6,4] and d['recent_45_retrospective']['BB01_distribution_0_to_3']==[14,29,2,0]
ck(True,'five disjoint 45-record retrospective blocks directly re-settled; they remain post-selection')
manual=J('2026328-manual-decisions.json')['decisions']['2026328'];assert [manual[k] for k in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','狗','鷄','馬','蛇'] and manual['universe_zodiac']==['馬','狗','鷄','蛇','虎','牛']
report=(O/'2026328-deep-review.md').read_text();index=(O/'2026328-deep-index.html').read_text();readme=(O/'README.md').read_text();assert all(x in report for x in ('328栏位保持不变','990种有序角色配置','不是328号码表','不是预测会重5','不能把该数字当历史样本的显著性检验')) and all(x in index for x in ('单馬、二狗鷄、三狗馬蛇','三肖完整必带单肖完整','这不是断言328会换表','不等于保证命中')) and all(x in readme for x in ('328深度复核','2026328-deep-index.html','2026328-deep-review.md'))
for name,text in [('2026328-deep-review.md',report),('2026328-deep-index.html',index)]:
 links=re.findall(r'href="([^"]+)"',text) if name.endswith('.html') else re.findall(r'\]\(([^)]+)\)',text)
 for x in links:
  if not x.startswith(('http://','https://','#','mailto:')):assert (O/x).is_file(),(name,x)
ck(True,'unchanged plan, disclosed caveats, current README and all relative report/index links agree')
print('OFFLINE 328 DEEP REVIEW VERIFICATION PASS: '+str(len(checks))+' checks — internal bytes and calculations only, not official draw, timing, actual odds, forecasts or WeChat safety')
