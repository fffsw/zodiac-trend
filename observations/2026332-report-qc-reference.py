#!/usr/bin/env python3
"""Cross-check every 331/332 report row and preserve hindsight/confirmation caveats."""
from pathlib import Path
from html import escape
import hashlib,json,re
R=Path('/home/user');A=R/'archive/task305_331_review_332';Q=A/'analysis';S=A/'stage';B=A/'before';P=R/'331期复盘_332期方案与逐期核验.md';X=S/'2026332-index.html';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads(p.read_text());r=J(Q/'retrospective.json');a=J(Q/'candidate_audit.json');t=P.read_text();h=X.read_text();checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
ck(J(Q/'candidate_independent_qc.json')['status']==J(Q/'review_independent_qc.json')['status']=='PASS' and H(Q/'candidate_audit.json')==J(Q/'candidate_independent_qc.json')['audit_sha256'],'independent retrospective and candidate analyses passed')
for s in ['已明确确认前六为','27龍、18牛、03龍、47猴、16兔、14蛇','第七为**13馬**','用户确认，不是官方来源认证','330和329的前六／第七划分仍只是按顺序推定','没有查询或使用332结果，但这不证明赛前','无法保证命中或收益','单馬0/1','二狗牛1/2缺狗','三狗兔蛇2/3缺狗','龍与狗同为奇数0路','0／1／2路为**3／1／2**','GG05事后套331时三龍兔蛇恰好3/3，只有**1栏**','新案事后套331','旧案零栏**11／14／19**，新案**9／12／14**','HH11近45为**13**次','非盲测','38.5598%／52.9297%／8.1810%／0.3295%','80.6007%','13,983,816','331→332不在分母内','0／1／2路**2／2／1**球','30份留存盘有明确全集、8份','14期已知全集中','本地核验ZIP在当前工作区快照缺失','不是16次独立试验','没有擅自改规则上线']:
 ck(s in t,'report discloses '+s)
for s in ['单馬、二虎牛、三虎鷄羊','龍仅替补，不自动补栏','用户确认前六27龍18牛03龍47猴16兔14蛇、第七13馬','单馬0/1、二狗牛1/2缺狗、三狗兔蛇2/3缺狗','虎是二、三共同位，虎缺仍使两栏同断','旧331和新332案零栏均38.5598%、全完均0.3295%','旧案零栏19次，新案14次','HH11为13次','38份混合来源留存盘','319、322、324是事后重建','官方来源和日期未认证','不能保证命中或收益']:
 ck(s in h,'public index discloses '+s)
def cell(s):return f"{''.join(s['required'])} {s['present_count']}/{s['needed_count']}（中{''.join(s['present']) or '—'}；缺{''.join(s['missing']) or '—'}）"
for group in (r['historical_outcomes'],r['unpublished_reconstructions']):
 for x in group:
  row='<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+escape(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>';ck(h.count(row)==1,f"HTML {x['period']} exact per-column hits/misses")
  fragment=' | '+' | '.join(cell(v) for v in x['slots'])+' | '+str(x['complete_columns'])+' |';ck(any(line.startswith('| '+str(x['period']%1000)+' |') and line.endswith(fragment) for line in t.splitlines()),f"report {x['period']} exact per-column hits/misses")
for x in r['candidate_counterfactuals']:
 frag=' | '+' | '.join(cell(v) for v in x['slots'])+' | '+str(x['complete_columns'])+' |';ck(any(line.startswith('| '+x['id']+' |') and line.endswith(frag) for line in t.splitlines()),x['id']+' 331 alternative post-hoc row')
for x in a['candidates']:
 rows=[line for line in t.splitlines() if line.startswith('| '+x['id'])];v=x['uniform_model'];ck(len(rows)==1 and f"{v['distribution_percent'][0]:.4f}%" in rows[0] and f"{v['distribution_percent'][3]:.4f}%" in rows[0] and rows[0].endswith(' | '+str(x['posthoc_331']['complete_columns'])+' | '+str(x['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0])+' |'),x['id']+' 332 alternative/model/hindsight row')
for link in re.findall(r'\]\(([^)]+)\)',t):
 if not link.startswith(('http://','https://','#','mailto:')):ck((R/link).is_file(),'local report link '+link)
old=J(B/'manual-decisions-through-331.json')['decisions'];new=J(S/'data/manual_site_decisions.json')['decisions'];v=new['2026332'];ck(len(old)==20 and len(new)==21 and all(new[k]==x for k,x in old.items()) and [v[k] for k in ('top_zodiac','a_zodiac','b_zodiac','c_zodiac','d_zodiac')]==['馬','虎','牛','鷄','羊'] and v['universe_zodiac']==['馬','虎','牛','鷄','羊','龍'] and '仅三肖栏完整（共1栏）' in v['manual_review'],'staged manual decision matches report; GG05 wording corrected without retroactive fabrication')
ck(t.count('（理论、不上线）')==2 and 'T14' in t and 'T15' in t and '单一共同肖缺失必使二三同断' in t,'theoretical no-shared alternatives distinguished from site decision')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'report_sha256':H(P),'index_sha256':H(X),'target_332_result_queried_or_used':False,'scope':'Report arithmetic, links and disclosure; not official source, actual draw timing, predicted success or safety.'};p=Q/'report_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks_count':len(checks),'report_sha256':out['report_sha256'],'index_sha256':out['index_sha256']},ensure_ascii=False,indent=2))
