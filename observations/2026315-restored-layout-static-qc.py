#!/usr/bin/env python3
"""Independent release checks: 315 payload preserved, only authorized appearance edits.

The optional future-row exercise below uses a synthetic fixture inside a deleted
sandbox. It is not a result and is never copied to the historical data or site.
"""
from pathlib import Path
from html.parser import HTMLParser
import csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
R=Path('/home/user');A=R/'archive/task265_315_original_layout';S=A/'stage';B=A/'before';D=A/'clean_deploy';O=D/'observations';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
old=(B/'315-previous-page.html').read_text(encoding='utf8');new=(S/'zodiac_trend.html').read_text(encoding='utf8');earlier=(B/'earlier-original-layout.html').read_text(encoding='utf8')
ck(sha(B/'315-previous-page.html')==sha(O/'2026315-page.html')=='3ac43b1210fc7aab4dfac2463fb9d9a1727199f479aafd2f6fbcf6c8eafb12c4','previous 315 page frozen and retained unchanged')
ck(sha(B/'data/macau_mark_six_full.csv')==sha(S/'data/macau_mark_six_full.csv')==sha(O/'2026315-source-data.csv')=='687efa128921ef7ace365131c023592a162a8dca4c367c88949ea0c16656ffb5','314 source exact historical bytes preserved')
ck(sha(B/'data/manual_site_decisions.json')==sha(S/'data/manual_site_decisions.json')==sha(O/'2026315-manual-decisions.json')=='184cc7a8758aee5f5ded71c0b745057092cc8bd3187871b60bca93aa3b2121ee','315 manual decisions exact bytes preserved')
ck(sha(S/'zodiac_trend.html')==sha(S/'www/zodiac_trend.html'),'root and www generation match byte for byte')
style=lambda x:re.search(r'<style>(.*?)</style>',x,re.S).group(1)
ck(style(new)==style(old)==style(earlier),'CSS identical to earlier layout and last 315 page')
script=lambda x:re.search(r'<script>\n(.*?)</script>',x,re.S).group(1)
x=script(old)
replacements=[
 ("const bannerTxt = VIEW==='num' ? '记录号码（未认证）' : '记录生肖走势 · 12肖全';","const bannerTxt = VIEW==='num' ? '平码号码' : '平码生肖走势 · 12肖全';"),
 ("// 旧版以浏览器本地21:30冒充销售截止且 HTML 缺少 >；没有经核实的官方时间，不生成倒计时。\nfunction tick(){\n  const pd=ALL[ALL.length-1][0]+1;\n  document.getElementById('count').textContent=`参考期号 ${pd} · 排期未核实`;\n}","// 保留原有期号框，但不伪造销售截止时间或倒计时。\nfunction tick(){\n  const pd=ALL[ALL.length-1][0]+1;\n  document.getElementById('count').textContent=`第 ${pd} 期`;\n}"),
 ("if(hs) hs.textContent=`新澳门（非官方） ${a}–${b} · ${ALL.length}期数据 · 横向滚动查看`;","if(hs) hs.textContent=`新澳门 ${a}–${b} · ${ALL.length}期数据 · 横向滚动查看`;"),
 ("if(fs) fs.textContent=`资料：既有记录及312、313、314用户号码 ${a}–${b}；313、314日期未知 · 非官方，仅供观察。`;","if(fs) fs.textContent=`资料 ${a}–${b} · 仅供观察`;")]
for a,b in replacements:
 ck(x.count(a)==1,'expected original code location uniquely identified')
 x=x.replace(a,b,1)
ck(x==script(new),'page JavaScript and embedded historical data otherwise byte-identical to released 315 snapshot')
match=lambda pattern,s:json.loads(re.search(pattern,s).group(1))
payload=match(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',new);dec=match(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',new)
order=['鼠','牛','虎','兔','龍','蛇','馬','羊','猴','鷄','狗','豬']
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f: rows=sorted(csv.DictReader(f),key=lambda v:int(v['period']))
expected=[[int(r['period']),r['date'][5:10].replace('-','/') if r['date'] else '--/--',[int(r[f'n{i}']) for i in range(1,7)],[order.index(r[f'z{i}']) for i in range(1,7)],int(r['special']),order.index(r['special_zodiac'])] for r in rows[-250:]]
ck(len(rows)==1045 and len(payload['rows'])==250 and payload['rows']==expected,'all 250 displayed rows independently match source including dates and seven balls')
ck(payload['rows'][-1]==[2026314,'--/--',[13,26,9,37,34,44],[6,5,10,6,9,11],31,0],'314 user numbers and unknown date retained')
ck(dec['2026314']=={'U':[2,5,6,4,3,1],'top':2,'A':5,'B':6,'C':4,'D':3,'top_overlap_mode':'coverage'},'P01 fixed roles and ox reserve exactly retained')
ck('id="source-risk-notice"' not in new and '非官方' not in new and '排期未核实' not in new,'no formerly prominent notices or labels')
ck('不伪造销售截止时间或倒计时' in new and 'setHours(21,30' not in new and '第 ${pd} 期' in new,'issue display without asserted timing')
class Page(HTMLParser):
 def __init__(self):super().__init__();self.external=[];self.scripts=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in ('iframe','object','embed','img','audio','video','source','link'):
   if any(d.get(k) for k in ('src','href','data','srcset')):self.external.append((tag,d))
  if tag=='script':self.scripts.append(d)
p=Page();p.feed(new)
ck(len(p.scripts)==1 and not p.scripts[0].get('src') and not p.external and 'fetch(' not in script(new) and 'XMLHttpRequest' not in script(new),'single self-contained page with no automatic external scripts or assets')
ck('observations/README.md' in new and '资料与机制未经认证' in new and '司警提醒' in new,'brief footer provides audit context without claiming official status')
# Byte-for-byte reproduction from exactly the frozen source and manual decisions.
with tempfile.TemporaryDirectory(prefix='task265-synthetic-',dir=A/'analysis') as tmp:
 t=Path(tmp);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(S/'data/macau_mark_six_full.csv',t/'data/macau_mark_six_full.csv');shutil.copyfile(S/'data/manual_site_decisions.json',t/'data/manual_site_decisions.json');env={**os.environ,'POOL_VERSION':'v5.0'}
 def generate():subprocess.run([sys.executable,str(S/'scripts/gen_trend.py')],cwd=t,env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 generate();ck((t/'zodiac_trend.html').read_bytes()==(S/'zodiac_trend.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes(),'generator reproduces released page byte for byte')
 source=(t/'data/macau_mark_six_full.csv').read_bytes();header,tail=source.split(b'\n',1);fixture='2026315,,01,02,03,04,05,06,红,红,蓝,蓝,绿,绿,馬,蛇,龍,兔,虎,牛,07,红,鼠\r\n'.encode();(t/'data/macau_mark_six_full.csv').write_bytes(header+b'\n'+fixture+tail);generate();future=(t/'zodiac_trend.html').read_text(encoding='utf8')
 ck('id="source-risk-notice"' not in future and '排期未核实' not in future and '非官方' not in future and '待人工定案' in future and 'observations/README.md' in future,'synthetic future regeneration keeps simple layout and waits for manual decision')
ck(subprocess.check_output(['git','status','--porcelain'],cwd=R/'deploy',text=True)==(A/'analysis/original_deploy_status_before.txt').read_text(),'original dirty deployment checkout remains untouched')
out={'status':'PASS','scope':'315 original layout; old 315 P01 and 314 user data preserved; target existence was checked but no 315 numbers read; synthetic future row only in deleted temporary directory; not official, predraw, outcome, fairness, or WeChat certification','page_sha256':sha(S/'zodiac_trend.html'),'generator_sha256':sha(S/'scripts/gen_trend.py'),'checks':checks};path=A/'analysis/local_static_qc.json';assert not path.exists();path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
