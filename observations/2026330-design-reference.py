#!/usr/bin/env python3
"""Record 330 proposal and structural comparisons before formal audit, after 329/history inspection."""
from pathlib import Path
import hashlib,json
R=Path('/home/user');O=R/'archive/task301_330_release/analysis';T=R/'archive/task300_329_review/analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert J(T/'independent_qc.json')['status']==J(O/'evidence_qc.json')['status']=='PASS' and J(T/'retrospective.json')['settlement']['complete_columns']==0 and J(O/'six_sign_repeat_study.json')['groups']['previous_six_5_seven_6']['n']==344 and not (O/'manual_decision.json').exists()
# Name, independent single, shared A, B, C, D, reserve(s), comparison. Each universe has six signs.
rows=[
('EE01','馬','鷄','牛','龍','虎',['蛇'],'主案单馬与组合错开；二鷄牛不依赖2路，三鷄龍虎跨三路且只含一个329正码旧肖。'),
('EE02','馬','鷄','牛','龍','羊',['虎'],'三虎换羊后龍羊同为0路，0路不足两球时三肖必不完整。'),
('EE03','馬','鷄','牛','龍','蛇',['虎'],'三虎换蛇：三肖含两个偶肖，全栏需要至少三个偶数；不意味着蛇更准。'),
('EE04','馬','鷄','狗','龍','虎',['蛇'],'二牛换狗，二栏奇偶兼有，但五展示肖有四个奇肖，全栏至少需要四奇。'),
('EE05','馬','鼠','牛','龍','虎',['蛇'],'共同位改鼠：单馬与鼠同奇1路，三肖全奇；同类不等于同一身份。'),
('EE06','馬','鷄','牛','鼠','虎',['蛇'],'三龍换鼠，使三肖含两个329旧肖且两个1路；1路至多一球时必断三。'),
('EE07','馬','鷄','牛','龍','虎',['豬'],'主栏不变只换替补；329第七猪不计正码，替补不能改变栏目结算。'),
('EE08','鷄','鷄','牛','龍','虎',['馬','蛇'],'单與共同位重合，鷄缺则三栏全部不完整，展示压缩为四身份。'),
('EE09','馬','鷄','牛','馬','虎',['龍','蛇'],'單馬重入三肖，馬缺单三连断，重现曾发生的集中风险。'),
('EE10','馬','狗','牛','龍','虎',['蛇'],'共同位换狗，二狗牛同0路，三肖狗龍也同0路；同路不能替代身份。'),
('EE11','龍','鷄','牛','馬','虎',['蛇'],'单龍与三馬互换，单肖从五码变四码；相同身份下栏目联动结构改变。'),
('EE12','牛','鷄','馬','龍','虎',['蛇'],'单牛与二馬互换，单肖四码、二栏含五码馬；不是预测改进。')]
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');prev=set(J(O/'six_sign_repeat_study.json')['current_pending']['previous_six']);out=[]
for id,top,A,B,C,D,rs,why in rows:
 r={'top':top,'A':A,'B':B,'C':C,'D':D};shown=set(r.values());assert len({A,B,C,D})==4 and len(rs)==len(set(rs)) and not shown.intersection(rs) and len(shown|set(rs))==6 and set(shown|set(rs))<=set(Z) and len(why)>15;out.append({'id':id,'roles':r,'reserves':rs,'comparison':why})
assert prev=={'鼠','牛','兔','鷄','狗'} and len(out)==12 and len({x['id'] for x in out})==12
m={'schema':'manual_comparison_for_330','target':2026330,'status':'USER_AUTHORIZED_UNVERIFIED_DISPLAY_NOT_OFFICIAL_NOT_PRE_DRAW_CERTIFIED','choice':'EE01','universe':['馬','鷄','牛','龍','虎','蛇'],'top':'馬','pair':['鷄','牛'],'triple':['鷄','龍','虎'],'reserves':['蛇'],'top_overlap_mode':'coverage','previous_329_six':[z for z in Z if z in prev],'previous_329_seven':J(O/'six_sign_repeat_study.json')['current_pending']['previous_seven'],'previous_displayed':['牛','鷄'],'nonprevious_displayed':['龍','虎','馬'],'previous_329_date':None,'data_source':'user provided and explicitly clarified issue 329; first-six plus seventh inferred; source, date, mapping and official status unverified','target_330_result_queried_or_used':False,
'selection_method':'After seeing 329 and retrospectively inspecting 36 retained displays, user-history cohorts and previous fair-model calculations, choose a five-identity display: horse single separate, shared chicken, pair chicken/ox on roads 1/0 (no 2-road required), triple chicken/dragon/tiger across 1/0/2 with only one 329-normal identity. Two displayed identities were in 329 normal six and three were not. This changes conditional exposure, not a demonstrated predictive advantage. Historical windows and the 5/6 cohort were inspected before this manual choice; it is not blind, preregistered or time-certified.',
'pre_formal_audit_disclosure':'The 329 result, 36-period history, 5/6 cohort (including the descriptive repeat 2/3 counts) and earlier fair-model calculations were inspected before EE01 and its 12 comparisons were written. Formal exact candidate audit and independent verification occur afterwards. No 330 outcome was looked up or used; time and blind selection are not authenticated.',
'primary_risks':'鷄是二三共同位，鷄缺必断两组合；馬缺单断但不必然断三。牛缺二断；龍或虎缺三断。零栏当且仅当馬缺且［鷄缺或（牛缺且（龍缺或虎缺））］。二栏两肖均偶，正码偶数不足2球必断二；三虎为2路，正码无2路必断三，但二和单仍有可能完整。全栏需马鸡牛龙虎五身份：相对329前六五旧肖，重肖只可能为2或3；重0/1/4/5必不全完，即使重2/3也未必全完。',
'role_rationales':{'馬':'单肖，五码01/13/25/37/49；与组合不共身份。328、329未出不意味着会回补；五码优势仅是均匀模型条件。','鷄':'二三共同，偶1 10/22/34/46；329出现不证明会续出。鷄缺两组合均断。','牛':'二栏，偶0 06/18/30/42；与鷄跨路但两者均偶，要求至少两个偶数。','龍':'三肖，奇0 03/15/27/39；329未出不意味会回补，狗同奇0不能代龍。','虎':'三肖，奇2 05/17/29/41；329正码无2路导致虎缺，但不预测330会有2路。','蛇':'仅替补，偶2 02/14/26/38；不参与正式栏目结算，也不自动补缺。'},
'structural_caveat':'五展示身份有馬、龍、虎三个奇肖和鷄、牛两个偶肖，三栏全完至少三个奇数和两个偶数。二栏同为偶数，三肖需要2路；目标期映射若改变须重算。',
'previous_repeat_scope':'329前六五个不同生肖（狗出现两球）、七球六个不同生肖（第七猪新增），因此与资料中前六5/七球6的344对匹配，而不是旧6/7组。历史条件筛选是事后描述，七球重复不能用于正码栏目结算。'}
assert len(set(m['universe']))==6 and set(m['universe'])==set(out[0]['roles'].values())|set(out[0]['reserves']) and set(m['previous_displayed'])==prev&set(out[0]['roles'].values()) and set(m['nonprevious_displayed'])==set(out[0]['roles'].values())-prev
for name,obj in [('handcrafted_candidates.json',{'scope':'12 related human comparisons created after observing user 329 and inspecting prior records; not independent trials, pre-registration or predictions','choice':'EE01','candidates':out}),('manual_decision.json',m)]:
 (O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':m['status'],'choice':m['choice'],'single':m['top'],'pair':m['pair'],'triple':m['triple'],'reserves':m['reserves'],'330_result_queried_or_used':False,'manual_sha256':H(O/'manual_decision.json')},ensure_ascii=False,indent=2))
