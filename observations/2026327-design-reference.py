#!/usr/bin/env python3
"""Freeze explicit manual comparisons and chosen 327 display before model auditing.
Choices consume only user 326 and earlier history, not a target result. They are not forecasts.
"""
from pathlib import Path
import hashlib,json
R=Path('/home/user');O=R/'archive/task292_327_release/analysis';T=R/'archive/task291_326_review/analysis';J=lambda p:json.loads(p.read_text(encoding='utf8'));e=J(O/'evidence.json');review=J(T/'retrospective.json');study=J(O/'six_sign_repeat_study.json');assert all(J(p)['status']=='PASS' for p in (O/'evidence_qc.json',O/'six_sign_repeat_qc.json',T/'independent_qc.json')) and e['latest_period']==2026326 and not e['target_result_was_already_provided'] and study['current_pending']['target_result_read'] is False and review['settlement']['complete_columns']==2
# Each row: ID, standalone, A(shared), B, C, D, reserve(s), plain-language counterargument.
rows=[
('BB01','馬','鷄','龍','虎','牛',['蛇'],'选定方案：单与组合错开；二跨偶1/奇0，三跨偶1/奇2/偶0。代价为五个不同展示肖全到才能三栏全完，共同鷄缺令二三断。'),
('BB02','龍','鷄','龍','虎','牛',['馬','蛇'],'与BB01同全集及相同二三栏；单龍与二重叠，四个展示肖即可全完，但更易零完整栏；馬退为替补不补栏。'),
('BB03','蛇','鷄','龍','虎','牛',['馬'],'与BB01同全集及相同二三栏；单蛇独立但为四码，馬退替补。单蛇缺不使组合直接断。'),
('BB04','牛','鷄','龍','虎','牛',['馬','蛇'],'同二三栏，单牛与三栏重叠；牛缺使单和三断。四展示肖较易全完但集中风险不同。'),
('BB05','馬','虎','龍','鷄','牛',['蛇'],'同全集及相同三肖，二由鷄龍改虎龍；共同虎缺二三断。奇2空缺历史不能预测下一期。'),
('BB06','馬','龍','鷄','虎','牛',['蛇'],'二与BB01相同，三改龍虎牛；共同龍缺二三断，三肖需要龍牛两个不同0路身份。'),
('BB07','馬','鷄','龍','虎','蛇',['牛'],'三由牛换蛇，奇2虎和偶2蛇为两个2路身份；2路至多1球时三肖栏必不完整。单馬和二鷄龍不变。'),
('BB08','馬','鷄','龍','虎','羊',['蛇'],'牛换羊，三肖鷄虎羊都是326前六旧肖；若前六重肖0至2，三肖栏必不完整。'),
('BB09','馬','鷄','龍','虎','牛',['羊'],'和BB01单二三完全一致，只以羊换替补蛇；六肖中有三个326旧肖，但替补不自动补栏。'),
('BB10','牛','鷄','龍','虎','馬',['蛇'],'同五个展示身份，把馬放三栏、牛单独；三肖鷄和馬为两个不同1路身份，奇1缺又使三肖断。'),
('BB11','馬','牛','龍','虎','鷄',['蛇'],'三栏同BB01，二栏牛龍为两个不同0路身份；无偶0使二三一起断。'),
('BB12','馬','羊','龍','虎','兔',['蛇'],'三肖羊虎兔皆为326旧肖；零至二重必断三肖栏，共同羊缺二三断。并非说旧肖一定不重。')]
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');previous=set(review['settlement']['normal_distinct']);c=[]
for id,top,A,B,C,D,rs,comparison in rows:
 roles={'top':top,'A':A,'B':B,'C':C,'D':D};shown=set(roles.values());assert len({A,B,C,D})==4 and len(rs)==len(set(rs)) and not shown.intersection(rs) and len(shown|set(rs))==6 and all(x in Z for x in shown|set(rs)) and len(comparison)>12
 c.append({'id':id,'roles':roles,'reserves':rs,'comparison':comparison})
assert len(c)==12 and len({x['id'] for x in c})==12 and previous=={'狗','兔','鷄','羊','虎','猴'}
m={'schema':'manual_comparison_for_327','target':2026327,'status':'USER_AUTHORIZED_UNVERIFIED_DISPLAY_NOT_PREDRAW_OR_FORECAST_GUARANTEE','selection_method':'Explicit manual tradeoff, not a scored ranking: standalone horse is a separate 5-number identity; pair and triple share chicken under the existing site layout; triple uses one identity per road, with two previously observed signs and one nonprevious. Prefer lowering the chance of no complete column under the stated ideal model, at the expense of requiring five specific identities for all columns. Fair model and historical records do not certify real draws.','choice':'BB01','universe':['馬','鷄','龍','虎','牛','蛇'],'top':'馬','pair':['鷄','龍'],'triple':['鷄','虎','牛'],'reserves':['蛇'],'top_overlap_mode':'coverage','previous_326_six':sorted(previous,key=Z.index),'previous_displayed':['虎','鷄'],'nonprevious_displayed':['牛','龍','馬'],'previous_326_date':None,'data_source':'user-provided 326 only; first-six plus seventh inferred from order; official source and time not authenticated','target_result_read_or_used':False,'primary_risks':'馬缺单断；鷄缺二三断；馬鷄同缺足以令零栏；龍缺二断；虎或牛缺三断。前六重0或1时三肖栏不完整；重6时单、二、三肖栏全不完整。要全部完整须馬鷄龍虎牛五个具体身份，前六重0/1/4/5/6均不可能全完（重4最多两新肖，实际需三新肖），重2或3仍不保证。','role_rationales':{'馬':'单栏，五码01/13/25/37/49；与二三错开，在所述49码等可能模型中单栏覆盖更大；326没出不是下期必回补，馬缺单断。','鷄':'二三共同，偶1四码10/22/34/46；326出现。鷄缺则二三均不完整，同偶1的兔不能补鷄；近期较多不保证继续。','龍':'二栏，奇0四码03/15/27/39；326没有，和鷄跨路。龍缺二断，不可据缺一次认为必回补。','虎':'三栏，奇2四码05/17/29/41；326出现。虎缺三断，同奇2的猴不补虎。','牛':'三栏，偶0四码06/18/30/42；326没有，令三栏跨三个路别。羊同偶0却不能补牛，遗漏4期不证明要出。','蛇':'仅替补、偶2四码02/14/26/38，和五个展示肖合起来覆盖六种路奇偶类型；不自动补单二三，326无蛇不证明下期回补。'},'source_identity_repeat_vs_prediction':'Previous 326 was six distinct normal signs and same six in seven; choosing two of those as displayed is a design exposure, not an actual 327 repeat claim. Six-to-six and seven-to-seven counted separately.'}
# Full-column repeat-count correction is checked mathematically in independent model: five required identities = 2 prior + 3 nonprior, hence 2–3 repeats maximum given six balls.
assert set(m['universe'])==set(c[0]['roles'].values())|set(c[0]['reserves']) and len(set(m['universe']))==6 and len(set(m['previous_displayed']))==2 and len(set(m['nonprevious_displayed']))==3
for name,obj in [('handcrafted_candidates.json',{'scope':'12 deliberate comparisons, no outcome or ranking; candidates are not independent samples','choice':'BB01','candidates':c}),('manual_decision.json',m)]:
 p=O/name;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':m['status'],'selection':'BB01','candidate_count':len(c),'single':m['top'],'pair':m['pair'],'triple':m['triple'],'reserve':m['reserves'],'327_outcome_used':False,'manual_sha256':hashlib.sha256((O/'manual_decision.json').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
