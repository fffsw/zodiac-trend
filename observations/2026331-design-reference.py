#!/usr/bin/env python3
"""Record a transparent 331 choice and related structural comparisons, after 330 review."""
from pathlib import Path
import hashlib,json
R=Path('/home/user');O=R/'archive/task303_331_release/analysis';T=R/'archive/task302_330_review/analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert J(T/'independent_qc.json')['status']==J(O/'evidence_qc.json')['status']=='PASS' and J(T/'retrospective.json')['settlement']['complete_columns']==2 and J(O/'six_sign_repeat_study.json')['groups']['previous_six_5_seven_6']['n']==345 and not (O/'manual_decision.json').exists()
# Name, single, shared A, pair B, triple C/D, reserve(s), comparison. Each universe has six identities.
rows=[
('FF01','馬','鷄','牛','龍','蛇',['虎'],'仅把上期三肖虎换蛇；三肖由两奇一偶变一奇两偶，保留二鷄牛同偶和鷄共同位，完整仍不保证。'),
('FF02','馬','鷄','牛','龍','虎',['蛇'],'上期正式栏完全沿用；三肖要两奇，单加三至少三奇，保留上期结构。'),
('FF03','馬','鷄','虎','龍','蛇',['牛'],'在主案基础上二牛换虎，二栏一奇一偶，但五展示肖全完仍须至少三奇。'),
('FF04','馬','鷄','牛','鼠','蛇',['虎'],'三肖雞鼠同1路，两个身份不能互代；五展示肖全完须至少三个1路。'),
('FF05','馬','鷄','牛','羊','蛇',['龍'],'三肖鷄羊蛇均偶，全完需要四个不同偶肖；奇偶暴露更集中。'),
('FF06','馬','牛','鷄','龍','蛇',['虎'],'二栏不变但把共同位改牛；牛缺二三同断，三肖牛龍同0路需两个0路。'),
('FF07','馬','龍','鷄','牛','蛇',['虎'],'共同位換龍，三肖龍牛同0路；龍缺两组合断，且缺龍是330事实但不预示331。'),
('FF08','馬','龍','鷄','鼠','蛇',['牛'],'二一奇一偶、三肖跨三路，但馬鼠同奇1，五肖全完须三个1路。'),
('FF09','鷄','鷄','牛','龍','蛇',['馬','虎'],'单与共同位重合，鷄缺时三栏同时断；仅四个正式身份，目标分布变化。'),
('FF10','馬','鷄','牛','馬','蛇',['龍','虎'],'馬既是单又在三肖，馬缺时单三联断；显示身份压为四个。'),
('FF11','牛','鷄','馬','龍','蛇',['虎'],'单牛与二馬互换，单肖由五码变四码；二栏包含馬，不是预测提高。'),
('FF12','馬','鷄','牛','龍','蛇',['猴'],'与主案正式栏相同只换替补；替补不补栏，正式栏模型不变。')]
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');prev=set(J(O/'six_sign_repeat_study.json')['current_pending']['previous_six']);out=[]
for id,top,A,B,C,D,rs,why in rows:
 r={'top':top,'A':A,'B':B,'C':C,'D':D};shown=set(r.values());assert len({A,B,C,D})==4 and len(rs)==len(set(rs)) and not shown.intersection(rs) and len(shown|set(rs))==6 and set(shown|set(rs))<=set(Z) and len(why)>15;out.append({'id':id,'roles':r,'reserves':rs,'comparison':why})
assert prev=={'馬','猴','豬','牛','鷄'} and len(out)==12 and len({x['id'] for x in out})==12
m={'schema':'manual_comparison_for_331','target':2026331,'status':'USER_AUTHORIZED_UNVERIFIED_DISPLAY_NOT_OFFICIAL_NOT_PRE_DRAW_CERTIFIED','choice':'FF01','universe':['馬','鷄','牛','龍','蛇','虎'],'top':'馬','pair':['鷄','牛'],'triple':['鷄','龍','蛇'],'reserves':['虎'],'top_overlap_mode':'coverage','previous_330_six':[z for z in Z if z in prev],'previous_330_seven':J(O/'six_sign_repeat_study.json')['current_pending']['previous_seven'],'previous_displayed':['牛','馬','鷄'],'nonprevious_displayed':['龍','蛇'],'previous_330_date':None,'data_source':'user-provided 330; first-six plus seventh inferred from order and previous convention, not separately confirmed; official source, date, mapping and release timing unverified','target_331_result_queried_or_used':False,
'selection_method':'After inspecting user 330, 37 retained displays, the corrected reserve classification, the 5/6 cohort, old fair-model calculations, and all 12 old designs retrospectively, retain horse single and chicken/ox pair but substitute snake for tiger in the triple. This reduces the number of odd identities needed for single plus triple from three to two, while increasing even requirements; it does not establish an empirical or model-wide prediction advantage. The same structural design appeared as EE03 in the earlier 330 comparisons and would still have had only two completed columns under the 330 result. No result of 331 was looked up or used.',
'pre_formal_audit_disclosure':'330 result, historical records, 5/6 cohort, fair-model comparisons and 330 candidate hindsight settlements including EE03 were inspected before FF01 and the 12 related comparisons were recorded. Formal candidate audit and independent verification occur afterwards. This is not blind, preregistered or time-certified.',
'primary_risks':'鷄是二三共同位，鷄缺必断两组合；馬缺单断但不必然断三。牛缺二断；龍或蛇缺三断。零栏当且仅当馬缺且［鷄缺，或（牛缺且（龍缺或蛇缺））］。二栏两肖均偶，正码偶数不足2球必断二；三蛇为2路，无2路必断三。全栏需要五个正式身份馬鷄牛龍蛇，相对330前六含三个旧肖、两个新肖；重3或4是全栏必要而非充分条件，重0/1/2/5必不全完。若重0，三栏均不完整；若重5，单二完整但三不完整。',
'role_rationales':{'馬':'单肖，五码01/13/25/37/49；与组合身份错开。330出现不证明会续出；五码优势只在均匀假设内成立。','鷄':'二三共同，偶1 10/22/34/46；330出现不证明续出，鷄缺两组合均不完整。','牛':'二栏，偶0 06/18/30/42；330出现不证明续出，与鷄同偶，需要至少两偶。','龍':'三肖，奇0 03/15/27/39；330缺龍不意味着331回补，狗同奇0不能代龍。','蛇':'三肖，偶2 02/14/26/38；330仅第七26蛇，非正码；第七出现不证明下一期正码，豬同偶2不能代蛇。','虎':'仅替补，奇2 05/17/29/41；不参与正式栏目结算，不自动补缺。'},
'structural_caveat':'五展示身份有馬、龍两个奇肖和鷄、牛、蛇三个偶肖，全栏至少两个奇数和三个偶数、0/1/2路至少2/2/1球。单加三肖至少两个奇数和两个偶数，旧案至少三个奇数和一个偶数；二栏仍需两偶、三肖仍需2路，鷄缺仍二三同断。目标期映射若改变须重算。',
'previous_repeat_scope':'330推定前六五个不同生肖（豬出现两球）、七球六个不同生肖（第七蛇新增），与资料中前六5/七球6的345对匹配，而不是5/5或6/7组。马是五码生肖，因此相关均匀重复模型与上一期全四码的五旧肖不同。筛选是事后描述，七球重复不能用于正码栏目结算。',
'previous_hindsight':'将FF01事后套入330仍为单1/1、二2/2、三1/3缺龍蛇、两栏完整，与旧案两栏完整；此对照不能作为331预测依据。'}
assert len(set(m['universe']))==6 and set(m['universe'])==set(out[0]['roles'].values())|set(out[0]['reserves']) and set(m['previous_displayed'])==prev&set(out[0]['roles'].values()) and set(m['nonprevious_displayed'])==set(out[0]['roles'].values())-prev
for name,obj in [('handcrafted_candidates.json',{'scope':'12 related human comparisons created after seeing user 330 and inspecting prior records; not independent trials, pre-registration or predictions','choice':'FF01','candidates':out}),('manual_decision.json',m)]:
 (O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':m['status'],'choice':m['choice'],'single':m['top'],'pair':m['pair'],'triple':m['triple'],'reserves':m['reserves'],'331_result_queried_or_used':False,'manual_sha256':H(O/'manual_decision.json')},ensure_ascii=False,indent=2))
