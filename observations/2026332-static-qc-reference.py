#!/usr/bin/env python3
"""Validate staged 332 page, appended 331 history and preserved earlier decisions."""
from pathlib import Path
from html.parser import HTMLParser
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
R=Path('/home/user');A=R/'archive/task305_331_review_332';B=A/'before';Q=A/'analysis';S=A/'stage';D=Path('/tmp/task305_332_deploy');J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(x,s):
 if not x:raise AssertionError(s)
 checks.append(s)
pat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';dp=r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;';before=(B/'331-revised-homepage.html').read_text();after=(S/'zodiac_trend.html').read_text();parse=lambda s,p:json.loads(re.search(p,s).group(1));m0=parse(before,pat);m1=parse(after,pat);d0=parse(before,dp);d1=parse(after,dp)
ck(H(S/'zodiac_trend.html')==H(S/'www/zodiac_trend.html')==J(Q/'manual_stage_receipt.json')['page_sha256']==J(Q/'manual_stage_correction.json')['page_sha256_unchanged'] and H(D/'zodiac_trend.html')==H(B/'331-revised-homepage.html')==H(R/'zodiac_trend.html')==H(R/'www/zodiac_trend.html'),'staged page copies identical; prior public and main page unchanged')
ck(d1['rows'][:-1]==d0['rows'][1:] and d1['n2z']==d0['n2z'] and d1['order']==d0['order'] and len(d1['rows'])==250 and d1['rows'][-1]==[2026331,'--/--',[27,18,3,47,16,14],[4,1,4,8,3,5],13,6] and H(R/'data/macau_mark_six_full.csv')==H(B/'history-through-330.csv'),'only 331 user-confirmed row added to rolling chart; prior rolling data/mapping unchanged')
ck(m1['2026331']=={'U':[6,2,1,9,7,4],'top':6,'A':2,'B':1,'C':9,'D':7,'top_overlap_mode':'coverage'} and len(m1)==len(m0)+1 and all(m1[k]==v for k,v in m0.items()) and all(k not in m1 for k in ('2026318','2026321','2026323','2026332')),'one target-332 decision added; 20 prior decisions preserved; reconstructed and future absent')
def normalized(text):
 for p in (pat,dp):text=re.sub(p,'<DATA>',text)
 text=re.sub(r'新澳门 2026\d{3}–2026\d{3}',r'新澳门 <RANGE>',text)
 return text
ck(normalized(before)==normalized(after),'layout and behavior unchanged other than current input/range/manual payload')
old=J(B/'manual-decisions-through-331.json');cur=J(S/'data/manual_site_decisions.json');v=cur['decisions']['2026332'];ck(len(old['decisions'])==20 and len(cur['decisions'])==21 and all(cur['decisions'][k]==x for k,x in old['decisions'].items()) and [v[k] for k in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','虎','牛','鷄','羊'] and v['universe_zodiac']==['馬','虎','牛','鷄','羊','龍'] and H(S/'data/manual_site_decisions.json')==J(Q/'manual_stage_correction.json')['new_decisions_sha256'] and H(R/'data/manual_site_decisions.json')==H(B/'manual-decisions-through-331.json'),'20 older decisions unchanged; staged 332 roles exact; main decisions still 331')
ck(H(S/'scripts/gen_trend.py')==H(R/'scripts/gen_trend.py')==H(B/'page-generator.py') and H(S/'www/index.html')==H(R/'www/index.html')==H(D/'index.html')==H(B/'root-entry.html'),'generator and entry unchanged')
class Page(HTMLParser):
 def __init__(self):super().__init__();self.foot=0;self.assets=[];self.scripts=0
 def handle_starttag(self,t,a):
  v=dict(a);self.foot+=t=='footer';self.scripts+=t=='script'
  if t in ('script','link','img','iframe','object','embed','audio','video','source') and any(v.get(k) for k in ('href','src','data','srcset')):self.assets.append((t,v))
p=Page();p.feed(after);ck(p.foot==0 and p.scripts==1 and not p.assets and all(x not in after for x in ('fetch(','XMLHttpRequest','footSrc')),'no footer, external assets or automatic network requests')
subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True);ck(True,'39 frozen baseline sources match')
for p in (Q/'review_independent_qc.json',Q/'candidate_independent_qc.json',Q/'report_qc.json'):ck(J(p)['status']=='PASS','independent '+p.name)
with tempfile.TemporaryDirectory(prefix='task305-repro-') as td:
 t=Path(td);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(S/'data/macau_mark_six_full.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(S/'data/manual_site_decisions.json',t/'data/manual_site_decisions.json');env={**os.environ,'POOL_VERSION':'v5.0'};subprocess.run([sys.executable,str(S/'scripts/gen_trend.py')],cwd=t,env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);ck((t/'zodiac_trend.html').read_bytes()==(S/'zodiac_trend.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes(),'clean staged reproduction identical')
 src=(t/'data/macau_mark_six_full.csv').read_bytes();head,rest=src.split(b'\n',1);fixture='2026332,,01,02,03,04,05,06,红,红,蓝,蓝,绿,绿,馬,蛇,龍,兔,虎,牛,07,红,鼠\r\n'.encode();(t/'data/macau_mark_six_full.csv').write_bytes(head+b'\n'+fixture+rest);subprocess.run([sys.executable,str(S/'scripts/gen_trend.py')],cwd=t,env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);f=(t/'zodiac_trend.html').read_text();ck(parse(f,dp)['rows'][-1][0]==2026332 and '2026332' not in parse(f,pat),'synthetic 332 fixture never generates automatic 333')
mans=['2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256','2026327.sha256','2026328.sha256','2026328-correction.sha256','2026328-deep-inputs.sha256','2026328-deep.sha256','2026329.sha256','2026330.sha256','2026331.sha256','2026331-rev1.sha256']
for man in mans:subprocess.run(['sha256sum','--quiet','-c',man],cwd=D/'observations',check=True)
subprocess.run(['sha256sum','--quiet','-c','../2026331-rev1-frozen.sha256'],cwd=D/'observations/2026331-rev1-frozen',check=True);ck(True,'27 prior plus two revision/frozen public manifests unchanged');ck(not J(Q/'candidate_design.json')['target_332_result_queried_or_used'],'no 332 target outcome queried; no timing claim');ck(subprocess.check_output(['git','status','--porcelain','-uall'],cwd=R/'deploy',text=True)==(B/'old-dirty-deploy-status.txt').read_text(),'old dirty deploy untouched')
out={'status':'PASS','checks':checks,'checks_count':len(checks),'page_sha256':H(S/'zodiac_trend.html'),'history_sha256':H(S/'data/macau_mark_six_full.csv'),'decisions_sha256':H(S/'data/manual_site_decisions.json'),'scope':'Static local consistency and synthetic fixture, not official source, prediction, target time or real WeChat authentication.'};p=Q/'local_static_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','checks_count','page_sha256')},ensure_ascii=False,indent=2))
