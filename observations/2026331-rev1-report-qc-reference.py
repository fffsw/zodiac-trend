#!/usr/bin/env python3
"""Check all displayed review rows and model/hindsight statements against frozen calculations."""
from pathlib import Path
from html import escape
import hashlib,json,re
R=Path('/home/user');A=R/'archive/task304_331_revision';B=A/'before';Q=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rev=J(B/'initial-retrospective.json');audit=J(Q/'revision_audit.json');report=R/'331期重新筛选与330期逐期复盘.md';txt=report.read_text();index=(S/'2026331-rev1-index.html').read_text();checks=[]
def ck(x,s):
 if not x:raise AssertionError(s)
 checks.append(s)
def cell(v):return f"{''.join(v['required'])} {v['present_count']}/{v['needed_count']}（中{''.join(v['present']) or '—'}；缺{''.join(v['missing']) or '—'}）"
for x in rev['historical_outcomes']:
 src='留存栏目文件' if x['period']<=2026308 else 'Git页面快照';line='| '+' | '.join([str(x['period']%1000),src]+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |';html='<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+escape(cell(s))+'</td>' for s in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>';ck(txt.count(line)==1 and index.count(html)==1,f"retained {x['period']} displayed exactly")
for x in rev['unpublished_reconstructions']:
 line='| '+' | '.join([str(x['period']%1000),'事后重建']+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |';html='<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+escape(cell(s))+'</td>' for s in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>';ck(txt.count(line)==1 and index.count(html)==1,f"reconstruction {x['period']} displayed separately")
for x in audit['candidates']:
 r=x['roles'];line='| '+' | '.join([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],'、'.join(x['reserves']),str(x['previous_normal_count']),str(len(x['changed_relative_to_330_display'])),f"{x['conditional_repeat'][0]['zero_pct']:.4f}%",str(x['posthoc_330']['complete_columns']),str(x['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0])])+' |';ck(txt.count(line)==1,'candidate row '+x['id'])
for token in ('**馬**','**狗、牛**','**狗、兔、蛇**','**虎**','两栏完整','尚未明确确认球次','不能保证命中或收益','不是盲选、预注册或样本外试验','没有证据证明其预测能力更强','二狗牛同0路','78.4403%','38.5598%','0.3295%','18／45','16／45','13,983,816','不能隐去不利回放','事后重建','未出现在本次工作区快照'):
 ck(token in txt,'disclosure '+token)
ck(len(re.findall(r'^\| \d{3} \|',txt,re.M))==40 and index.count('<table id="history">')==index.count('<table id="recon">')==1,'37 retained and three reconstruction rows exactly once')
for l in re.findall(r'\]\(([^)]+)\)',txt):ck((R/l).is_file(),'local report link '+l)
sel=audit['selected'];base=audit['baseline'];ck(sel['posthoc_330']['complete_columns']==1 and base['posthoc_330']['complete_columns']==2 and [sel['posthoc_fixed_windows'][str(k)]['complete_0_1_2_3'][0] for k in (35,40,45)]==[11,14,18] and [base['posthoc_fixed_windows'][str(k)]['complete_0_1_2_3'][0] for k in (35,40,45)]==[11,12,16] and audit['candidates'][2]['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0]==13,'unfavorable hindsight counts and alternative correctly disclosed')
ck(sel['uniform_model']==base['uniform_model'] and round(sel['conditional_repeat'][0]['zero_pct'],4)==78.4403 and sel['all_minimum']=={'road_0_1_2':[2,2,1],'odd_even':[2,3]} and sel['pair_minimum']=={'road_0_1_2':[2,0,0],'odd_even':[1,1]} and [x['distribution'][3]>0 for x in sel['conditional_repeat']]==[False,False,True,True,False,False],'model and route conditions correct')
ck(all(x in index for x in ('单馬、二狗牛、三狗兔蛇','用户尚未明确确认球次','无法保证命中','实际留存单馬1/1','原331初版事后套330为两栏','修订18次','共同位','37份','319、322、324','事后重建')),'public index contains decision, risks, caveat and worse hindsight')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'report_sha256':H(report),'index_sha256':H(S/'2026331-rev1-index.html'),'scope':'Transcription and local links only; no official, timing or forecast certification.'};(Q/'report_qc.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','checks_count','report_sha256','index_sha256')},ensure_ascii=False,indent=2))
