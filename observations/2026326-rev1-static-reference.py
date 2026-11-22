#!/usr/bin/env python3
"""Independent static, isolated generation and synthetic future-row fail-closed checks."""
from pathlib import Path
from html.parser import HTMLParser
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
R=Path('/home/user');A=R/'archive/task290_326_revision';S=A/'stage';O=A/'analysis';B=A/'before';D=A/'clean_deploy';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
p= r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';dp=r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;';old=(B/'326-v1-public-page.html').read_text();new=(S/'zodiac_trend.html').read_text();parse=lambda x,pat:json.loads(re.search(pat,x).group(1));m0=parse(old,p);m1=parse(new,p);dat0=parse(old,dp);dat1=parse(new,dp)
ck(H(S/'zodiac_trend.html')==H(S/'www/zodiac_trend.html')!=H(B/'326-v1-public-page.html') and H(D/'zodiac_trend.html')==H(B/'326-v1-public-page.html'),'two staged pages match; live clone still contains old page before release')
ck(dat0==dat1 and len(dat1['rows'])==250 and dat1['rows'][-1]==[2026325,'--/--',[41,37,10,1,27,17],[2,6,9,6,4,2],3,4],'all 250 historical page rows and 325 first-six plus seventh unchanged')
ck(re.sub(p,'const MANUAL_SITE_DECISIONS_V50=<MANUAL>;',old)==re.sub(p,'const MANUAL_SITE_DECISIONS_V50=<MANUAL>;',new),'every HTML/CSS/JS byte outside the manual payload unchanged')
ck(m0['2026325']=={'U':[7,2,6,3,4,5],'top':7,'A':2,'B':7,'C':6,'D':3,'top_overlap_mode':'concentrated'} and m1['2026325']=={'U':[7,2,6,9,4,5],'top':7,'A':2,'B':7,'C':6,'D':9,'top_overlap_mode':'concentrated'} and all(m1[k]==v for k,v in m0.items() if k!='2026325') and set(m1)==set(m0),'only 326 manual page roles changed, old and new exact, all other target decisions unchanged')
oldrec=J(B/'manual-decisions-v1.json');newrec=J(S/'data/manual_site_decisions.json');r=newrec['decisions']['2026326'];ck(set(oldrec['decisions'])==set(newrec['decisions']) and all(newrec['decisions'][k]==v for k,v in oldrec['decisions'].items() if k!='2026326') and [r['top_zodiac'],r['a_zodiac'],r['b_zodiac'],r['c_zodiac'],r['d_zodiac']]==['羊','虎','羊','馬','鷄'] and r['universe_zodiac']==['羊','虎','馬','鷄','龍','蛇'] and '2026324' not in newrec['decisions'],'only detailed 326 decision revised, no fake 324 decision, exact reserve boundaries')
ck(H(S/'data/macau_mark_six_full.csv')==H(B/'history-through-325.csv')==H(R/'data/macau_mark_six_full.csv')=='307655d85b643128f28d0a8c3babf662d770ded56a815b67ff34561f067fcc07' and H(B/'generator-before.py')==H(R/'scripts/gen_trend.py'),'history and optimized generator byte-identical to old release')
with (S/'data/macau_mark_six_full.csv').open(encoding='utf8',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');expected=[[int(r['period']),r['date'][5:10].replace('-','/') if r['date'] else '--/--',[int(r[f'n{i}']) for i in range(1,7)],[Z.index(r[f'z{i}']) for i in range(1,7)],int(r['special']),Z.index(r['special_zodiac'])] for r in rows[-250:]];ck(len(rows)==1056 and rows[-1]['period']=='2026325' and expected==dat1['rows'] and all(int(r['period'])<=2026325 for r in rows),'exact source matching for all page rows; no 326 draw read from history')
class P(HTMLParser):
 def __init__(self):super().__init__();self.fe=[];self.assets=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='footer':self.fe.append(t)
  if t in ('script','link','img','iframe','embed','object','source','audio','video') and any(d.get(k) for k in ('href','src','srcset','data')):self.assets.append((t,d))
x=P();x.feed(new);ck(not x.fe and not x.assets and all(s not in new for s in ('footSrc','fetch(','XMLHttpRequest','资料与机制未经认证','司警提醒','排期未核实')),'no restored footer/banner, external assets, or network requests')
ck(subprocess.check_output(['git','status','--porcelain','-uall'],cwd=R/'deploy',text=True)==(O/'original_dirty_deploy_status_before.txt').read_text() and len((O/'original_dirty_deploy_status_before.txt').read_text().splitlines())==68,'unrelated dirty deploy untouched')
subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True);ck(True,'all 24 original-version frozen inputs hash-checked')
with tempfile.TemporaryDirectory(prefix='task290-repro-',dir=O) as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(S/'data/macau_mark_six_full.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(S/'data/manual_site_decisions.json',t/'data/manual_site_decisions.json');env={**os.environ,'POOL_VERSION':'v5.0'};subprocess.run([sys.executable,str(R/'scripts/gen_trend.py')],cwd=t,env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);ck((t/'zodiac_trend.html').read_bytes()==(S/'zodiac_trend.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes(),'unchanged generator independently reproduces both revised pages byte-for-byte')
 src=(t/'data/macau_mark_six_full.csv').read_bytes();head,rest=src.split(b'\n',1);fixture='2026326,,01,02,03,04,05,06,红,红,蓝,蓝,绿,绿,馬,蛇,龍,兔,虎,牛,07,红,鼠\r\n'.encode();(t/'data/macau_mark_six_full.csv').write_bytes(head+b'\n'+fixture+rest);subprocess.run([sys.executable,str(R/'scripts/gen_trend.py')],cwd=t,env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);future=(t/'zodiac_trend.html').read_text();ck(parse(future,dp)['rows'][-1][0]==2026326 and '2026326' not in parse(future,p) and '<footer' not in future,'synthetic fixture produces no automatic 327 picks or footer; fixture is not real result')
report=(O/'2026326-rev1-analysis.md').read_text();forbidden=['前六不可能重4','一定重3','保证命中','必然重3'];ck(all(x not in report for x in forbidden) and all(x in report for x in ('理论上限：4肖','前六观察最大值：3肖','七球观察最大值：4肖','前六重0、1或2肖','不等于证明鷄比兔更容易出','不是326的实际号码或预测号码','不能证明赛前')),'report asserts correct distinct boundaries, risks and synthetic examples')
for n in ('maximum_independent_qc.json','revision_model_independent_qc.json'):ck(J(O/n)['status']=='PASS','independent '+n+' PASS')
out={'status':'PASS','scope':'isolated static/reproducibility checks, not source, prediction, predraw, official status, actual mechanism or WeChat certification','checks':checks,'page_sha256':H(S/'zodiac_trend.html')};dest=O/'local_static_qc.json';assert not dest.exists();dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
