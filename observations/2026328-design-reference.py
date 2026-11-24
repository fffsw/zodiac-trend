#!/usr/bin/env python3
"""Freeze 328 human-readable comparisons after 327 review, before formal audit.
This is not blind, official, pre-registered, or proof of predictive superiority.
"""
from pathlib import Path
import hashlib,json
R=Path('/home/user');O=R/'archive/task295_328_release/analysis';T=R/'archive/task294_327_review/analysis';J=lambda p:json.loads(p.read_text());e=J(O/'evidence.json');rev=J(T/'retrospective.json');study=J(O/'six_sign_repeat_study.json');assert all(J(p)['status']=='PASS' for p in (O/'evidence_qc.json',O/'six_sign_repeat_qc.json',T/'independent_qc.json')) and e['latest_period']==2026327 and not e['target_result_was_already_provided'] and rev['settlement']['complete_columns']==1 and study['current_pending']['target_result_read'] is False
# ID, top, common A, B, C, D, reserve(s), specific counterargument.
rows=[
('CC01','馬','狗','鷄','馬','蛇',['虎','牛'],'主方案：单馬并入三肖，二狗鷄跨路、三狗馬蛇各路；四个身份即可全完，但馬缺同时使单三断。'),
('CC02','鷄','狗','鷄','馬','蛇',['虎','牛'],'同四个展示肖和二三肖，只改为单鷄并入二栏；单为四码，鷄缺使单二断。'),
('CC03','牛','狗','鷄','馬','蛇',['虎'],'保持相同二三肖，将单牛错开；须五个身份全到，牛缺单断。'),
('CC04','馬','狗','馬','鷄','蛇',['虎','牛'],'同四个展示肖，馬移入二栏；二完整须馬与狗，三须狗鷄蛇；馬缺单二断。'),
('CC05','馬','狗','鷄','馬','牛',['虎','蛇'],'二和单不变，三蛇换牛；三肖狗牛均0路，0路至多一球时三肖必断。'),
('CC06','馬','狗','兔','馬','蛇',['虎','牛'],'二鷄换兔，兔鷄同偶1却不是同一生肖；同类换位没有被证明更准。'),
('CC07','馬','龍','鷄','馬','蛇',['虎','牛'],'共同狗换龍；两者同奇0但身份不同，龍缺使二三断，延续龙或换龙均非预测。'),
('CC08','馬','狗','鷄','馬','虎',['蛇','牛'],'三蛇换虎为全奇肖；前三至少3个奇数才能全中，且四个展示肖都属于327旧肖。'),
('CC09','馬','狗','豬','馬','蛇',['虎','牛'],'二鷄换豬；二豬和三蛇均为不同偶2，全部完整须至少两球偶2。'),
('CC10','馬','鷄','狗','馬','蛇',['虎','牛'],'与主案同二肖，将共同位改鷄；三肖鷄馬同1路，1路至多一球必断三。'),
('CC11','馬','狗','鷄','猴','牛',['蛇'],'单馬与组合错开，三狗猴牛含两个0路身份；五个展示身份全到才全完。'),
('CC12','馬','狗','鷄','馬','蛇',['兔','羊'],'与主案单二三完全一致，只换两个替补；替补不参与结算，栏目概率不变。')]
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');prev=set(rev['settlement']['normal_distinct']);out=[]
for id,top,A,B,C,D,rs,comment in rows:
 roles={'top':top,'A':A,'B':B,'C':C,'D':D};shown=set(roles.values());assert len({A,B,C,D})==4 and len(rs)==len(set(rs)) and not shown.intersection(rs) and len(shown|set(rs))==6 and all(x in Z for x in shown|set(rs)) and len(comment)>15
 out.append({'id':id,'roles':roles,'reserves':rs,'comparison':comment})
assert len(out)==12 and len({x['id'] for x in out})==12 and prev=={'狗','馬','鼠','虎','鷄','羊'}
m={'schema':'manual_comparison_for_328','target':2026328,'status':'USER_AUTHORIZED_UNVERIFIED_DISPLAY_NOT_PREDRAW_OR_FORECAST_GUARANTEE','choice':'CC01','universe':['馬','狗','鷄','蛇','虎','牛'],'top':'馬','pair':['狗','鷄'],'triple':['狗','馬','蛇'],'reserves':['虎','牛'],'top_overlap_mode':'concentrated','previous_327_six':[z for z in Z if z in prev],'previous_displayed':['狗','鷄','馬'],'nonprevious_displayed':['蛇'],'previous_327_date':None,'data_source':'user-provided 327 only; first-six plus seventh inferred from order; official source and time not authenticated','target_328_result_queried_or_used':False,
 'selection_method':'After reviewing 327 and local records, select a four-identity display where horse is both single and one triple member, dog is shared by pair/triple, pair crosses 0/1 roads and triple covers all three. A six-identity universe adds tiger/ox as reserve-only. This trades broader all-column feasibility and the horse five-number group against less distinct display coverage and increased linked failures. Historical frequencies and fairness assumptions do not establish a predictive advantage.',
 'pre_formal_audit_disclosure':'Before freezing CC01, six small exact fair-model spot checks compared the previous BB01, horse in triple, horse in pair, and other 328 tail structures. The formal 12-candidate audit is after this freeze. No 328 outcome was queried; this was not a blind or preregistered selection.',
 'primary_risks':'狗缺二三断；馬缺单三断；鷄缺二断；蛇缺三断。馬缺且（狗缺或鷄缺）足以全部不完整。全栏需馬狗鷄蛇四个指定身份；相对327重肖0/1/2或6时全栏不可能，重3/4/5也不保证。重6时已知六旧身份全到，单馬和二狗鷄完整但三缺蛇，仅作条件推理。',
 'role_rationales':{'馬':'单、三肖共享，5码01/13/25/37/49；重叠减少全栏所需不同身份，但馬缺单三一起断。327出现不证明续出。','狗':'二三共同，奇0 09/21/33/45；狗缺二三断，同奇0龍不能代狗。327前六21狗、第七45狗只作已有记录，第七不计栏目。','鷄':'二栏，偶1 10/22/34/46；与狗跨路，兔是同类但不能互补。出现频次不是未来概率。','蛇':'三肖，偶2 02/14/26/38；与狗馬各路不同，豬同类不能互补。327蛇缺不证明回补。','虎':'仅替补，奇2；不补任何展示栏。','牛':'仅替补，偶0；不补任何展示栏。'},
 'structural_caveat':'二跨路且三跨三路时，共同A之外的B/C/D存在至少一处同路是结构必然，不可能凭排列消除所有路线集中。本案二侧鷄与三侧馬均属1路但奇偶不同；即使有1路也不能替代具体鷄或馬。','previous_repeat_scope':'327前六与七球均为六肖；132组已知后续的相同条件资料仅作描述。328未知，不把观察频次、遗漏或重肖当作硬约束。'}
assert set(m['universe'])==set(out[0]['roles'].values())|set(out[0]['reserves']) and len(set(m['universe']))==6 and len(set(m['previous_displayed']))==3 and len(set(m['nonprevious_displayed']))==1
for name,obj in [('handcrafted_candidates.json',{'scope':'12 related manual structural comparisons, not independent trials or predictions; selection made after disclosed quick fair-model spot checks','choice':'CC01','candidates':out}),('manual_decision.json',m)]:
 p=O/name;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':m['status'],'selection':'CC01','candidate_count':len(out),'single':m['top'],'pair':m['pair'],'triple':m['triple'],'reserve':m['reserves'],'328_outcome_queried_or_used':False,'manual_sha256':hashlib.sha256((O/'manual_decision.json').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
