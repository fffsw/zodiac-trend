#!/usr/bin/env python3
"""Offline review of the corrected 328 package. Does not authenticate draw or clocks.
Run from any directory: python3 observations/2026328-correction-verify.py
The old 328 verifier is run in an isolated copy with its original README restored.
"""
from pathlib import Path
import csv,hashlib,json,re,shutil,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;P=O.parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads((O/p).read_text(encoding='utf8'));checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
def verify(n,base,root):
 names=set()
 for line in (O/n).read_text(encoding='utf8').splitlines():
  h,rel=line.split('  ',1);p=(base/rel).resolve();assert p.is_relative_to(root.resolve()) and p.is_file() and rel not in names and H(p)==h,(n,rel);names.add(rel)
 return len(names)
old=('2026313.sha256','2026313-original-style.sha256','2026313-reanalysis-v2.sha256','2026314.sha256','2026315.sha256','2026315-rollback-to-314.sha256','2026315-restored-layout.sha256','2026315-entry-fix.sha256','2026315-initial-layout-no-footer.sha256','2026316.sha256','2026317.sha256','2026318.sha256','2026320.sha256','2026321.sha256','2026321-index-repair.sha256','2026323.sha256','2026325.sha256','2026326.sha256','2026326-rev1.sha256','2026327.sha256','2026328.sha256')
assert all(verify(n,O,P)>0 for n in old) and verify('2026328-correction.sha256',O,P)>=8 and verify('2026328-before.sha256',O/'2026328-retrospective-frozen',P)==30 and verify('2026327-before.sha256',O/'2026327-retrospective-frozen',P)==70
assert H(O/'2026328.sha256')=='27d2ac0559a4292fdd69c7937fa4b9af29aa64aac41c6ba512cb0440ca150175' and H(O/'2026327.sha256')=='3505f85ae837ac8d73e5f092208ba87ed3816cd68e7800a83bee2c7e6382e3c1'
ck(True,'all 21 historical manifests, correction manifest and 100 frozen copies match without altering original hashes')
assert H(O/'README.md')==H(O/'2026328-corrected-readme-snapshot.md') and H(P/'zodiac_trend.html')==H(O/'2026328-page.html')=='aa129f740c671492e941080f17d16410beb2757a3fdf224c039e756e1350713a'
ck(True,'updated README equals corrected snapshot; 328 displayed page remains the original selected page')
with tempfile.TemporaryDirectory(prefix='328-corrected-prior-') as td:
 t=Path(td)/'site';shutil.copytree(P,t,ignore=shutil.ignore_patterns('.git','__pycache__'));(t/'observations/README.md').unlink();shutil.copyfile(O/'2026328-readme-snapshot.md',t/'observations/README.md');r=subprocess.run([sys.executable,str(t/'observations/2026328-verify.py')],capture_output=True,text=True,timeout=180);assert r.returncode==0 and 'OFFLINE 327 CONDITIONAL REVIEW / 328 DISPLAY VERIFICATION PASS' in r.stdout,r.stdout+r.stderr
ck(True,'original 328 portable verifier and nested 327 verifier replay in isolated original README view')
oldreport=(O/'2026328-analysis.md').read_text();report=(O/'2026328-corrected-analysis.md').read_text();oldindex=(O/'2026328-index.html').read_text();index=(O/'2026328-corrected-index.html').read_text();notice=(O/'2026328-date-correction.md').read_text();readme=(O/'README.md').read_text();heading='## 一、327：先确认中了什么、缺了什么'
assert oldreport.split(heading,1)[1]==report.split(heading,1)[1] and H(O/'2026328-analysis.md')=='fa42ff9f97831d6f64fc6b7c7297f9edeea65471c276495945bfc9959eed030e' and H(O/'2026328-index.html')=='093f5223ef1a7c24f0d98cc162a9285e5769c756de69385bcdeca22d25f2cec4'
assert '历史资料部分日期与参考时间不一致' in oldreport and '历史资料部分日期与参考时间不一致' not in report and '部分日期缺失或与参考日期冲突' in oldindex and '部分日期缺失或与参考日期冲突' not in index and all(x in report for x in ('日期措辞更正','撤回作为事实的判断','历史资料部分日期缺失')) and all(x in index for x in ('日期措辞更正','撤回作为事实的判断','2026328-corrected-analysis.md','2026328-date-correction.md','2026328-correction-verify.py')) and all(x in readme for x in ('日期措辞更正','2026328-corrected-index.html','2026328-corrected-analysis.md'))
ck(True,'corrected index/report and README prominently link the correction; calculations unchanged and original versions intact')
pause=J('2026327-chronology-pause.json');assert pause['reference_local_date']=='2026-10-13' and pause['runtime_clock_utc_observation'].startswith('2026-11-22') and pause['third_party_http_date_header'].startswith('Sun, 22 Nov 2026') and len(pause['future_dated_records'])==26 and pause['future_dated_records'][0]['recorded_date']=='2026-10-14' and pause['future_dated_records'][-1]['recorded_date']=='2026-11-08' and all(x in notice for x in ('10月13日','11月22日','不能证明赛前','不能保证命中或收益'))
with (O/'2026328-source-data.csv').open(encoding='utf-8-sig',newline='') as f:rows={int(x['period']):x for x in csv.DictReader(f)}
assert all(rows[p]['date']=='' for p in range(2026313,2026328))
ck(True,'correction cites the previously recorded conflicting references and correctly states 313–327 missing dates')
for n in ('2026328-corrected-analysis.md','2026328-corrected-index.html','2026328-date-correction.md'):
 text=(O/n).read_text();links=re.findall(r'href="([^"]+)"',text) if n.endswith('.html') else re.findall(r'\]\(([^)]+)\)',text)
 for l in links:
  if not l.startswith(('http://','https://','#','mailto:')):assert (O/l).is_file(),(n,l)
ck(True,'all corrected report and index relative links resolve')
assert re.search(r'单馬、二狗鷄、三狗馬蛇；虎牛仅替补',index) and '1.6585%' in index and '40.9686%' in index and len(re.findall(r'^\| \d{3} \|',report,re.M))==37 and len(re.findall(r'^\| \d{2} \|',report,re.M))==49
ck(True,'corrected material retains selected CC01, ideal-model caveat, 37 review rows and 49 number rows')
print('OFFLINE CORRECTED 327 REVIEW / 328 DISPLAY VERIFICATION PASS: '+str(len(checks))+' checks — integrity and internal arithmetic only; no official draw, reliable chronology, prediction or real WeChat certification')
