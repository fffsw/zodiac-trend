#!/usr/bin/env python3
"""Verify every report/index row, quantitative transcription and local evidence link."""
from pathlib import Path
from html import escape
import hashlib,json,re
R=Path('/home/user');Q=R/'archive/task301_330_release/analysis';T=R/'archive/task300_329_review/analysis';S=R/'archive/task301_330_release/stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rev=J(T/'retrospective.json');audit=J(Q/'candidate_audit.json');study=J(Q/'six_sign_repeat_study.json');e=J(Q/'evidence.json');report=R/'329期复盘_330期方案与逐期核验.md';txt=report.read_text();index=(S/'2026330-index.html').read_text();checks=[]
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
 r=x['roles'];sl=x['slots'];line='| '+' | '.join([x['id'],r['top']+'／'+r['A']+r['B']+'／'+r['A']+r['C']+r['D']]+[f"{v['present_count']}/{v['needed_count']}" for v in sl]+[str(x['complete_columns']),'二缺'+(''.join(sl[1]['missing']) or '—')+'；三缺'+(''.join(sl[2]['missing']) or '—')])+' |';ck(txt.count(line)==1,f"{x['id']} 329 counterfactual table")
for z in list('鼠牛虎兔龍蛇馬羊猴鷄狗豬'):
 x=e['per_zodiac'][z];values='；'.join(f"{x['windows'][str(k)]['periods']}/{x['windows'][str(k)]['balls']}" for k in (35,40,45));ck(' '.join(f'{n:02d}' for n in x['numbers']) in txt and values in txt,f'{z} ledger numbers and overlapping windows')
for v in ('**馬**','**鷄、牛**','**鷄、龍、虎**','**蛇**','不能保证','前六5肖、七球6肖','344','227','未查询或使用330结果','重0／1／4／5','13,983,816','38.5598%','0.3295%','尚未明确确认该球次划分','不是盲测胜率','没有模型上的整体优势'):
 ck(v in txt,v)
ck(len(re.findall(r'^\| \d{3} \|',txt,re.M))==39 and index.count('<table id="history">')==index.count('<table id="recon">')==1,'36 history and three reconstructions, exactly once')
for l in re.findall(r'\]\(([^)]+)\)',txt):ck((R/l).is_file(),f'local report evidence link {l}')
ck(study['groups']['previous_six_5_seven_6']['six_to_six_counts_0_to_5']==[8,70,139,107,20,0] and study['groups']['previous_six_5_seven_5']['six_to_six_counts_0_to_5']==[7,40,106,62,11,1] and study['groups']['previous_six_6_seven_7']['n']==131 and not study['current_pending']['target_result_queried_or_used'],'cohorts separately recounted and unknown target excluded')
ck('官方来源' in index and '赛前状态均未认证' in index and '无法保证命中' in index and '用户尚未明确确认球次' in index and '微信' in index,'index risk, unconfirmed ball partition and emulation limitations')
ck(audit['selected']['ideal_model']==audit['previous_329_DD01_ideal_comparison'] and audit['selected']['ideal_model']['exact_complete_column_distribution']==[5392128,7401592,1144016,46080] and not audit['target_330_result_queried_or_used'],'selected/previous uniform model equality and target unknown')
reserve=J(T/'reserve_correction_qc.json');ck(reserve['status']=='PASS' and reserve['known_universe_count']==28 and reserve['unknown_universe_count']==8 and len(reserve['retained_noncolumn_hit_periods'])==14 and reserve['reconstruction_noncolumn_hit_periods']==[2026322,2026324] and not reserve['slots_and_complete_columns_changed'],'independently verified universe correction and unchanged formal columns')
for v in ('历史全集与替补不能默认空','28份有明确全集','14期至少一个非栏目肖','291—298','未知','322豬、324蛇','原始错误明细及原复核回执已冻结保留'):ck(v in txt,'reserve correction disclosure: '+v)
ck(all(v in index for v in ('遗漏已纠正','14期有非栏目肖','291—298未明确全集','2026330-reserve-audit.csv')),'evidence index displays reserve correction and ledger link')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'report_sha256':H(report),'index_sha256':H(S/'2026330-index.html'),'scope':'Transcription and local links only; not official results, future outcome, prediction or timing certification.'};(Q/'report_qc.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','checks_count':len(checks),'report_sha256':out['report_sha256'],'index_sha256':out['index_sha256']},ensure_ascii=False,indent=2))
