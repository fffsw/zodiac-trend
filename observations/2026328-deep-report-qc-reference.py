#!/usr/bin/env python3
"""Independent textual and numerical verification of the new local deep-review addendum."""
from pathlib import Path
import csv,hashlib,json,re,shutil,subprocess,sys,tempfile
R=Path('/home/user');A=R/'archive/task297_328_deep_review';B=A/'before';Q=A/'analysis';F=R/'328期深度复盘_补充核验与决定.md';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=J(Q/'deep_metrics.json');qc=J(Q/'independent_qc.json');text=F.read_text();checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
assert qc['status']=='PASS_INDEPENDENT_DEEP_REVIEW' and qc['deep_metrics_sha256']==H(Q/'deep_metrics.json') and not d['target_328_outcome_queried_or_used'];with_history=B/'history-through-user-327.csv'
with with_history.open(encoding='utf-8-sig',newline='') as f:rows={int(x['period']):x for x in csv.DictReader(f)}
normal=lambda r:[int(r[f'n{i}']) for i in range(1,7)];zs=lambda r:{r[f'z{i}'] for i in range(1,7)};a=rows[2026326];b=rows[2026327];assert normal(b)==[21,49,7,41,46,36] and int(b['special'])==45 and len(zs(a)&zs(b))==4 and [len(s&zs(b)) for s in ({'馬'},{'鷄','龍'},{'鷄','虎','牛'})]==[1,1,2] and len({'馬','鷄','龍','虎','牛'}-zs(a))==3 and all(s in text for s in ('单馬1/1完整','二鷄龍1/2缺龍','三鷄虎牛2/3缺牛','完整0/1/2/3栏为13/17/3/1','结果后重建'))
ck(True,'327 user settlement, repeat4, three-new requirement and saved/reconstructed history scope cross-checked')
cc=d['ideal_model']['CC01'];bb=d['ideal_model']['BB01'];fmt=lambda v:f'{v:.4f}%'
for name,v in [('327旧BB01',bb),('328现行CC01',cc)]:
 line='| '+' | '.join([name]+[fmt(x) for x in v['complete_columns_0_to_3_pct']]+[fmt(v['at_least_one_pct']),fmt(v['at_least_two_pct'])])+' |';assert line in text
assert all(x in text for x in ('49码等可能','不放回抽前六球','不是已认证的真实概率','不能把两者加总',fmt(d['ideal_model']['CC01_zero_column_disjoint_partition']['no_displayed_identity_pct']))) and cc['patterns_single_pair_triple']['001']==cc['patterns_single_pair_triple']['011']==0 and '不可能出现“只有三肖完整”' in text and '馬缺，且狗或鷄至少缺一' in text
ck(True,'full ideal distributions, nested event warning, partial-match risk and deterministic shared-horse logic checked')
for k in range(7):assert re.search(r'^\| '+str(k)+r' \| '+re.escape('、'.join(map(str,d['logical_repeat_possibilities'][str(k)])))+r' \|',text,re.M)
assert all(x in text for x in ('不是七球重肖','未查询或使用328结果','这是条件结论，不是预测会重5','这不是328号码'))
ck(True,'all seven repeat possibilities reproduced; conditional conclusion and synthetic witness clearly labeled')
a=d['ideal_model']['hypothetical_offset8_not_a_328_mapping_claim'];assert d['data_audit']['rows']==1058 and len(d['data_audit']['internal_mapping_changes'])==3 and d['data_audit']['132_six_sign_cohort_cross_mapping_changes']==0 and len(d['data_audit']['undated_issues'])==15 and all(fmt(v) in text for v in (a['single_pair_triple_pct'][0],a['complete_columns_0_to_3_pct'][0],a['complete_columns_0_to_3_pct'][3])) and all(s in text for s in ('不是328号码表','并非断言328会换表','不证明各期标签名称、日期或官方来源真实'))
ck(True,'mapping sensitivity, label-count limitation, undated rows and non-claim about 328 mapping all present')
assert d['ideal_model']['identical_ideal_distribution_role_permutations']==990 and all(s in text for s in ('990种有序角色配置','不是990期数据','不能证明狗比龍','未来频次' if False else '过去频次'))
for b in d['recent_45_retrospective']['blocks']:
 a,z=b['period_range_old_to_new'];line='| '+' | '.join([b['age'],f'{a%1000}—{z%1000}',str(b['n']),'／'.join(map(str,b['CC01_complete_columns_0_to_3'])),'／'.join(map(str,b['BB01_complete_columns_0_to_3']))])+' |';assert line in text
assert all(x in text for x in ('固定后事后套用','不是曾发布盘的成绩','选择偏差')) or ('固定后事后套用' in text and '不能把本表当成曾发布盘的成绩' in text and '选择偏差' in text)
ck(True,'role symmetry, five disjoint blocks and post-selection/non-blind retrospective caveat checked')
for v in (d['six_sign_cohort']['current_prev_group_model_repeat6_pct'],d['six_sign_cohort']['iid_132_identical_current_groups_zero_repeat6_pct']):assert fmt(v) in text
assert '实际历史132组并不是这个实验' in text and '不能把该数字当历史样本的显著性检验' in text and '328栏位保持不变' in text and '没有任何方案可保证命中或获利' in text
for link in re.findall(r'\]\(([^)]+)\)',text):assert not link.startswith(('http://','https://')) and (R/link).is_file(),link
ck(True,'hypothetical IID example, no-guarantee and local evidence links are explicitly qualified')
generator=(R/'scripts/task297_make_deep_report.py').read_text();assert generator.count("R=Path('/home/user');")==1
with tempfile.TemporaryDirectory(prefix='deep-report-replay-') as tmp:
 p=Path(tmp);q=p/'archive/task297_328_deep_review/analysis';q.mkdir(parents=True);shutil.copyfile(Q/'deep_metrics.json',q/'deep_metrics.json');shutil.copyfile(Q/'independent_qc.json',q/'independent_qc.json');g=p/'g.py';g.write_text(generator.replace("R=Path('/home/user');",f"R=Path({str(p)!r});"));r=subprocess.run([sys.executable,str(g)],capture_output=True,text=True,timeout=30);assert r.returncode==0,(r.stdout,r.stderr);assert (p/F.name).read_bytes()==F.read_bytes()
ck(True,'isolated report generator reproduces the reviewed local addendum exactly')
out={'status':'PASS_DEEP_REPORT_QC','scope':'Text-to-evidence, arithmetic and links; not official provenance, timing, prediction or real WeChat safety','report_sha256':H(F),'deep_metrics_sha256':H(Q/'deep_metrics.json'),'checks':checks,'target_328_outcome_queried_or_used':False};p=Q/'report_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
