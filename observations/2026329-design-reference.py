#!/usr/bin/env python3
"""Record manual 329 proposal and related comparisons before formal 12-case audit.
This is post-328-outcome, after inspecting historical evidence and an existing ideal model;
it is NOT blinded, preregistered, official, or proof of predictive advantage.
"""
from pathlib import Path
import hashlib,json
R=Path('/home/user');O=R/'archive/task299_329_release/analysis';T=R/'archive/task298_328_review/analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert J(T/'independent_qc.json')['status']==J(O/'evidence_qc.json')['status']=='PASS' and J(T/'retrospective.json')['settlement']['complete_columns']==0 and J(O/'six_sign_repeat_study.json')['groups']['previous_six_6_seven_7']['n']==130 and not (O/'manual_decision.json').exists()
# Name, top, common A, B, C, D, reserve(s), reason for comparison. Fixed six-sign pool per row.
rows=[
('DD01','馬','虎','鷄','鼠','羊',['蛇'],'主案五个不同展示肖：单馬错开二三肖、共同虎仍是二三单点；二跨路且奇偶兼有，三跨三路。'),
('DD02','馬','虎','鷄','鼠','蛇',['羊'],'三羊换蛇会改变新旧结构并让三占两个2路；没有证据证明哪一个更准。'),
('DD03','馬','虎','鷄','鼠','龍',['羊'],'三羊换龍后三个三肖全奇；最多两奇时三肖必断。'),
('DD04','馬','虎','兔','鼠','羊',['蛇'],'鷄换同偶1路兔；同类不等于同一身份，不能声称轮换带来更准。'),
('DD05','馬','羊','鷄','鼠','虎',['蛇'],'三身份不变但共同位改羊，二羊鷄为两偶，二中二需要至少两个偶数。'),
('DD06','馬','鼠','鷄','虎','羊',['蛇'],'共同位改鼠，二鼠鷄都为1路，1路不超过一球时二必断。'),
('DD07','鼠','虎','鷄','馬','羊',['蛇'],'单鼠与三馬置换：单为四码，馬在三栏，模型与单馬的权衡不同。'),
('DD08','虎','虎','鷄','鼠','羊',['馬','蛇'],'单肖重合二三共同虎：虎缺三栏必断，展示仅四个身份。'),
('DD09','馬','虎','鷄','馬','羊',['鼠','蛇'],'单馬重入三肖：减少全完所需身份但馬缺单三联断，重现旧结构。'),
('DD10','馬','虎','鷄','鼠','羊',['牛'],'主栏与DD01完全相同、只换替补；第七球的牛不能替换正码缺肖。'),
('DD11','馬','狗','鷄','鼠','羊',['蛇'],'共同虎换狗，三狗鼠羊的0路重复；狗曾在328出现不构成延续依据。'),
('DD12','鷄','虎','馬','鼠','羊',['蛇'],'单馬与二鷄互换角色；五个身份不变但五码馬进入二栏，单为四码。')]
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');prev=set(J(O/'six_sign_repeat_study.json')['current_pending']['previous_six']);out=[]
for id,top,A,B,C,D,rs,why in rows:
 r={'top':top,'A':A,'B':B,'C':C,'D':D};shown=set(r.values());assert len({A,B,C,D})==4 and len(rs)==len(set(rs)) and not shown.intersection(rs) and len(shown|set(rs))==6 and set(shown|set(rs))<=set(Z) and len(why)>15;out.append({'id':id,'roles':r,'reserves':rs,'comparison':why})
assert prev=={'鼠','虎','龍','羊','猴','狗'} and len(out)==12 and len({x['id'] for x in out})==12
m={'schema':'manual_comparison_for_329','target':2026329,'status':'USER_AUTHORIZED_UNVERIFIED_DISPLAY_NOT_OFFICIAL_NOT_PRE_DRAW_CERTIFIED','choice':'DD01','universe':['馬','虎','鷄','鼠','羊','蛇'],'top':'馬','pair':['虎','鷄'],'triple':['虎','鼠','羊'],'reserves':['蛇'],'top_overlap_mode':'coverage','previous_328_six':[z for z in Z if z in prev],'previous_328_seven':J(O/'six_sign_repeat_study.json')['current_pending']['previous_seven'],'previous_displayed':['鼠','虎','羊'],'nonprevious_displayed':['馬','鷄'],'previous_328_date':None,'data_source':'user-provided 328; first-six plus seventh inferred; source, date, mapping and official status unverified','target_329_result_queried_or_used':False,
'selection_method':'After seeing 328 and retrospectively inspecting 35 retained displays, user-history cohorts and prior exact fair-model comparisons, choose a five-identity structure with horse single separate from both combinations. Tiger remains the pair/triple shared identity; pair tiger/chicken crosses routes/parity; triple tiger/mouse/sheep covers three routes. Exactly three of five displayed identities appeared among 328 normal six. This makes all-column completion possible if the next normal-six overlap is four, but not guaranteed. Identity choice was human-selected from seen data, not pre-registered or independently predictive.',
'pre_formal_audit_disclosure':'The 328 result, old 35-period review, six-versus-seven repeat cohorts, old ideal-model calculations and an initial illustrative cohort count were inspected before DD01 and the 12 comparisons were written. Formal exact candidate audit and independent arithmetic verification occur afterwards. No 329 outcome was looked up or used; time and blind selection are not authenticated.',
'primary_risks':'虎是二三共同位，虎缺必断两组合；馬缺单断但不必然断三。鷄缺二断；鼠或羊缺三断。零栏当且仅当馬缺且［虎缺或（鷄缺且（鼠缺或羊缺））］。三码同路、同奇偶或替补出现不能替代指定生肖。三虎鼠羊都是328前六旧肖；若下一期前六相对328重肖不足3，三肖必断。全栏需马虎鸡鼠羊五身份：重肖只可能为3或4；重0/1/2/5/6必不全完，即使重3/4也未必全完。',
'role_rationales':{'馬':'单肖，五码01/13/25/37/49；与组合不共身份。328未出不代表会回补。與鼠同奇1路仍是不同身份。','虎':'二三共同，奇2 05/17/29/41；328是替补且为正码，这不预测下期。虎缺两组合均断。','鷄':'二栏，偶1 10/22/34/46；与虎跨路且奇偶互补，328缺不代表会回补。','鼠':'三肖，奇1 07/19/31/43；与馬同奇1但不能互代，缺鼠则三栏不完整。','羊':'三肖，偶0 12/24/36/48；使三栏覆盖三路，缺羊则三栏不完整。','蛇':'仅替补，偶2 02/14/26/38；不参与正式栏结算，也不自动补缺。'},
'structural_caveat':'全栏需至少两个奇1路（馬、鼠）且至少三个奇数、两个偶数；二、三共享虎，任何跨路覆盖都不能避免身份共同位依赖。全栏只可能在与328前六重3或4肖时，条件成立也不能保证。',
'previous_repeat_scope':'328前六6个不同生肖、七球7个不同生肖（第七牛新），因此应将资料里前六6/七球7的130对与前六6/七球6的133对分开。仅历史条件描述；七球重复不能用于正码栏目结算。'}
assert len(set(m['universe']))==6 and set(m['universe'])==set(out[0]['roles'].values())|set(out[0]['reserves']) and set(m['previous_displayed'])==prev&set(out[0]['roles'].values()) and set(m['nonprevious_displayed'])==set(out[0]['roles'].values())-prev
for name,obj in [('handcrafted_candidates.json',{'scope':'12 related human comparisons created after observing user 328 and inspecting prior records; not independent trials, pre-registration or predictions','choice':'DD01','candidates':out}),('manual_decision.json',m)]:
 p=O/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':m['status'],'choice':m['choice'],'single':m['top'],'pair':m['pair'],'triple':m['triple'],'reserves':m['reserves'],'329_result_queried_or_used':False,'manual_sha256':H(O/'manual_decision.json')},ensure_ascii=False,indent=2))
