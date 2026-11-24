#!/usr/bin/env python3
"""Check every rendered historical/candidate table against independent arithmetic artifacts."""
from pathlib import Path
from html import escape
import hashlib,json,re
R=Path('/home/user');Q=R/'archive/task299_329_release/analysis';T=R/'archive/task298_328_review/analysis';S=R/'archive/task299_329_release/stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rev=J(T/'retrospective.json');audit=J(Q/'candidate_audit.json');study=J(Q/'six_sign_repeat_study.json');report=R/'328期复盘_329期方案与逐期核验.md';txt=report.read_text();index=(S/'2026329-index.html').read_text();checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
def cell(v):return f"{''.join(v['required'])} {v['present_count']}/{v['needed_count']}（中{''.join(v['present']) or '—'}；缺{''.join(v['missing']) or '—'}）"
for x in rev['historical_outcomes']:
 src='留存栏目文件' if x['period']<=2026308 else 'Git页面快照';line='| '+' | '.join([str(x['period']%1000),src]+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |';ck(txt.count(line)==1 and index.count('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+escape(cell(s))+'</td>' for s in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>')==1,f"{x['period']} displayed in both tables")
for x in rev['unpublished_reconstructions']:
 line='| '+' | '.join([str(x['period']%1000),'事后重建']+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |';ck(txt.count(line)==1 and index.count('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+escape(cell(s))+'</td>' for s in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>')==1,f"{x['period']} reconstruction separately displayed")
for x in audit['candidates']:
 r=x['roles'];p=x['ideal_model']['percent'];line='| '+' | '.join([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],'、'.join(x['reserves']),f"{p['all_columns']:.4f}%",f"{p['no_complete_column']:.4f}%",x['comparison']])+' |';ck(txt.count(line)==1,f"{x['id']} model candidate table")
for x in rev['candidate_counterfactuals']:
 r=x['roles'];sl=x['slots'];line='| '+' | '.join([x['id'],r['top']+'／'+r['A']+r['B']+'／'+r['A']+r['C']+r['D']]+[f"{v['present_count']}/{v['needed_count']}" for v in sl]+[str(x['complete_columns']),'二缺'+(''.join(sl[1]['missing']) or '—')+'；三缺'+(''.join(sl[2]['missing']) or '—')])+' |';ck(txt.count(line)==1,f"{x['id']} 328 counterfactual table")
for v in ('**馬**','**虎、鷄**','**虎、鼠、羊**','**蛇**','不保证','前六6肖、七球7肖','130','133','未查询或使用329结果','重0／1／2／5／6','13,983,816','38.5598%','40.9686%','0.3295%','1.6585%','日期未知'):
 # Reserve formatting is intentionally not bold in table; independently require role identity.
 if v=='**蛇**':ck('| 仅替补 | **蛇**' in txt,v)
 else:ck(v in txt,v)
ck(len(re.findall(r'^\| \d{3} \|',txt,re.M))==38 and index.count('<table id="history">')==index.count('<table id="recon">')==1,'35 history and three reconstructions, exactly once')
for l in re.findall(r'\]\(([^)]+)\)',txt):ck((R/l).is_file(),f'local report link exists {l}')
ck(study['groups']['previous_six_6_seven_7']['six_to_six_counts_0_to_6']==[2,12,50,47,16,3,0] and study['groups']['previous_six_6_seven_6']['six_to_six_counts_0_to_6']==[2,9,45,47,27,3,0] and not study['current_pending']['target_result_queried_or_used'],'cohorts separated and target not queried')
ck('官方来源' in index and '赛前状态均未认证' in index and '无法保证命中' in index and '微信' in index,'index risk, provenance and emulation limitations disclosed')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'report_sha256':H(report),'index_sha256':H(S/'2026329-index.html'),'scope':'Report transcription and link consistency only, not official draws, future outcomes or time certification.'};(Q/'report_qc.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','checks_count':len(checks),'report_sha256':out['report_sha256'],'index_sha256':out['index_sha256']},ensure_ascii=False,indent=2))
