#!/usr/bin/env python3
"""Independent check: remove footer, preserve 315/314 and optimized functionality."""
from pathlib import Path
from html.parser import HTMLParser
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
R=Path('/home/user');A=R/'archive/task267_footer_cleanup';S=A/'stage';B=A/'before';D=A/'clean_deploy';Q=A/'analysis';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(x,m):
 if not x:raise AssertionError(m)
 checks.append(m)
live=(B/'zodiac_trend.html').read_text();preview=(B/'layout-preview-before-footer-removal.html').read_text();new=(S/'zodiac_trend.html').read_text();script=lambda s:re.search(r'<script>\n(.*?)</script>',s,re.S).group(1);style=lambda s:re.search(r'<style>(.*?)</style>',s,re.S).group(1)
ck(sha(B/'zodiac_trend.html')==sha(D/'zodiac_trend.html')=='16cadce0b366aa6273017002db75d37bdda279eb8c2497029a6bbda9dd59d34e','previous public page frozen')
ck(sha(B/'layout-preview-before-footer-removal.html')=='37f7e64cd7e1bcb5af73b08aa7124989da644d86746f4db19c2b33a700adb13e','prior user-review preview frozen')
ck(sha(S/'data/macau_mark_six_full.csv')==sha(B/'data/macau_mark_six_full.csv')==sha(R/'data/macau_mark_six_full.csv')=='687efa128921ef7ace365131c023592a162a8dca4c367c88949ea0c16656ffb5','314 user-only history unchanged')
ck(sha(S/'data/manual_site_decisions.json')==sha(B/'data/manual_site_decisions.json')==sha(R/'data/manual_site_decisions.json')=='184cc7a8758aee5f5ded71c0b745057092cc8bd3187871b60bca93aa3b2121ee','315 hand decision unchanged')
ck(sha(S/'zodiac_trend.html')==sha(S/'www/zodiac_trend.html'),'stage root and www pages identical')
# Entire JavaScript body must equal old public implementation except two labels
# and deletion of footer-only DOM text update. This protects computation,
# manual selection, storage conflict checks, view switches and data bytes.
x=script(live);changes=[("const bannerTxt = VIEW==='num' ? '平码号码' : '平码生肖走势 · 12肖全';","const bannerTxt = VIEW==='num' ? '平码开奖号码' : '平码生肖走势 · 12肖全';"),("<td class=\"per\">近30期次数<br>（前六码）</td>","<td class=\"per\">近30期次数</td>"),("  const fs=document.getElementById('footSrc');\n  if(fs) fs.textContent=`资料 ${a}–${b} · 仅供观察`;\n",'')]
for a,b in changes:ck(x.count(a)==1,'expected presentation-only change located');x=x.replace(a,b,1)
ck(x==script(new),'all remaining JS including 315 data and 314 decisions byte-identical to current implementation')
y=script(preview);r="  const fs=document.getElementById('footSrc');\n  if(fs) fs.textContent=`资料 ${a}–${b} · 频率≠下期概率 · 仅供数据观察 · 未满18周岁禁止购彩,理性投注。`;\n";ck(y.count(r)==1 and y.replace(r,'')==script(new),'footer is the sole script change relative to reviewed layout preview')
ck(style(preview)==style(new),'requested movable horizontal columns retained')
extra='''/* 横向滑动时，期数和右侧指标随整张表一起移动，不固定在左右边缘。 */\nth.perh{left:auto!important}\ntd.per{position:static;left:auto}\n.i1,.i2,.i3,.i4{right:auto!important}\n'''
ck(style(new).count(extra)==1 and style(new).replace(extra,'')==style(live),'CSS relative to live contains only targeted moving-column rule')
pat=r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;';m=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';payload=json.loads(re.search(pat,new).group(1));dec=json.loads(re.search(m,new).group(1));Z=['鼠','牛','虎','兔','龍','蛇','馬','羊','猴','鷄','狗','豬']
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda v:int(v['period']))
expected=[[int(r['period']),r['date'][5:10].replace('-','/') if r['date'] else '--/--',[int(r[f'n{i}']) for i in range(1,7)],[Z.index(r[f'z{i}']) for i in range(1,7)],int(r['special']),Z.index(r['special_zodiac'])] for r in rows[-250:]]
ck(len(rows)==1045 and payload['rows']==expected and payload['rows'][-1]==[2026314,'--/--',[13,26,9,37,34,44],[6,5,10,6,9,11],31,0],'all 250 displayed rows match the protected 314 user history')
ck(dec['2026314']=={'U':[2,5,6,4,3,1],'top':2,'A':5,'B':6,'C':4,'D':3,'top_overlap_mode':'coverage'},'P01: single tiger, pair snake/horse, triple snake/dragon/rabbit, ox reserve')
class Page(HTMLParser):
 def __init__(self):super().__init__();self.footer=0;self.src=[];self.scripts=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.footer+=tag=='footer'
  if tag=='script':self.scripts+=1
  if tag in ('script','img','iframe','link','object','embed','video','audio','source'):
   if any(d.get(k) for k in ('src','href','data','srcset')):self.src.append((tag,d))
p=Page();p.feed(new);ck(p.footer==0 and 'footSrc' not in new and all(x not in new for x in ('资料与机制未经认证','司警提醒','非官方','排期未核实','仅供观察')),'entire unwanted footer removed without relocation')
ck(p.scripts==1 and not p.src and 'fetch(' not in script(new) and 'XMLHttpRequest' not in script(new),'self-contained page; no automatic external assets')
with tempfile.TemporaryDirectory(prefix='task267-fixture-',dir=Q) as tmp:
 t=Path(tmp);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(S/'data/macau_mark_six_full.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(S/'data/manual_site_decisions.json',t/'data/manual_site_decisions.json');env={**os.environ,'POOL_VERSION':'v5.0'}
 def run():subprocess.run([sys.executable,str(S/'scripts/gen_trend.py')],cwd=t,env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 run();ck((t/'zodiac_trend.html').read_bytes()==(S/'zodiac_trend.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes(),'generator reproduces current page byte for byte')
 src=(t/'data/macau_mark_six_full.csv').read_bytes();head,rest=src.split(b'\n',1);fixture='2026315,,01,02,03,04,05,06,红,红,蓝,蓝,绿,绿,馬,蛇,龍,兔,虎,牛,07,红,鼠\r\n'.encode();(t/'data/macau_mark_six_full.csv').write_bytes(head+b'\n'+fixture+rest);run();fut=(t/'zodiac_trend.html').read_text();ck('footSrc' not in fut and '<footer' not in fut and '资料与机制未经认证' not in fut and '待人工定案' in fut,'synthetic future regeneration has no footer and requires manual decision')
ck(subprocess.check_output(['git','status','--porcelain'],cwd=R/'deploy',text=True)==(Q/'original_deploy_status_before.txt').read_text(),'original dirty deploy left untouched')
out={'status':'PASS','scope':'layout/text/scroll only, preserving current JS algorithm and user data; synthetic future row was in a deleted temporary directory; not official, predraw or WeChat validation','page_sha256':sha(S/'zodiac_trend.html'),'generator_sha256':sha(S/'scripts/gen_trend.py'),'checks':checks};p=Q/'local_static_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
