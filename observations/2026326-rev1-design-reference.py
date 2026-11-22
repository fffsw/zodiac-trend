#!/usr/bin/env python3
"""Explicit human structural comparisons after clarification, not an automated ranking."""
from pathlib import Path
import json,hashlib
R=Path('/home/user');A=R/'archive/task290_326_revision';B=A/'before';O=A/'analysis';J=lambda p:json.loads(p.read_text());assert J(O/'maximum_independent_qc.json')['status']=='PASS' and J(O/'freeze_receipt.json')['status']=='PASS';old=J(B/'326-v1-candidate-audit.json');lookup={x['id']:x for x in old['candidates']};assert lookup['AA16']['roles']=={'top':'羊','A':'虎','B':'羊','C':'馬','D':'鷄'} and lookup['AA16']['reserves']==['龍','蛇']
rows=[
('R00','羊','虎','羊','馬','兔',['龍','蛇'],'326原已上线AA01：三栏2个上期生肖虎馬加新兔；若恰重4肖，兔不一定出现，三栏不一定完整。'),
('R01','羊','虎','羊','馬','鷄',['龍','蛇'],'326修订AA16：三栏虎馬鷄均属上期；若下期前六重足四肖，则三栏一定完整。重3必须恰为虎馬鷄；重2或更少三栏必断。'),
('R02','羊','虎','羊','龍','鷄',['馬','蛇'],'同全集AA12：三栏虎龍鷄三路各一，但全栏须羊龍两个不同0路肖；重3若缺馬可成三，若缺龍不能。'),
('R03','羊','虎','馬','鷄','龍',['蛇'],'四个上期肖覆盖在组合中：若前六重足四肖，二三均完整；但二三同时完整必须重足四，单羊若无则不全完。'),
('R04','馬','虎','馬','鷄','龍',['羊','蛇'],'全部展示为上期四肖：若前六重足四肖则三栏全完；零重会令三栏齐断，且单馬与二馬重叠。'),
('R05','羊','虎','羊','馬','龍',['鷄','蛇'],'保留虎馬龍三上期肖作三栏，三肖全奇；奇数不满3球时三栏必断，鷄仅替补。'),
('R06','羊','龍','羊','虎','鷄',['馬','蛇'],'三栏龍虎鷄各路一肖；二龍羊需两个不同0路肖，且馬只作替补。'),
('R07','羊','馬','羊','虎','鷄',['龍','蛇'],'共同馬替代共同虎；无1路时二三均断；本次单仍羊，龙仅替补。'),
('R08','鷄','虎','羊','馬','鷄',['龍','蛇'],'单鷄与三重叠；若上期四肖零重，单二三全部不完整；不证明鷄会继续出现。'),
('R09','羊','虎','鷄','馬','龍',['蛇'],'四上期肖在二三全部覆盖，二虎鷄跨路混奇偶；三虎馬龍全部奇肖，须至少3奇。'),
('R10','蛇','虎','馬','鷄','龍',['羊'],'四上期肖覆盖组合、单蛇作新肖；单与组合错开，蛇羊均属四码组但身份不能替换。')]
assert [x[0] for x in rows]==[f'R{i:02}' for i in range(11)]
plans=[{'id':i,'roles':{'top':t,'A':a,'B':b,'C':c,'D':d},'reserves':rs,'comparison':reason} for i,t,a,b,c,d,rs,reason in rows]
p={'scope':'User clarified previous draw has four distinct zodiac signs; comparisons written after observing historical maxima; not preregistration or ranking. 326 result not read and actual timing unauthenticated.','previous_325':['虎','馬','鷄','龍'],'plans':plans,'selected_id':'R01','source_in_earlier_38':'AA16'}
m={'period':2026326,'status':'REVISION_AFTER_USER_CLARIFICATION_NOT_PREDRAW_CERTIFIED','selected_id':'R01','source_in_earlier_38':'AA16','prior_public_choice':'AA01','prior_public_slots':{'single':'羊','pair':['虎','羊'],'triple':['虎','馬','兔'],'reserve':['龍','蛇']},'revised_universe':['羊','虎','馬','鷄','龍','蛇'],'single':'羊','pair':['虎','羊'],'triple':['虎','馬','鷄'],'reserve':['龍','蛇'],'top_overlap_mode':'concentrated','trigger_previous_four':['虎','馬','鷄','龍'],'displayed_previous_signs':['虎','馬','鷄'],'selection_is_not_an_actual_repeat_count':True,'target_result_read':False,'choice_reason':'匹配325前六七球均四肖的48例中，下期前六观测最高重3而理论仍可重4；把三栏改为上期虎馬鷄三个身份，在重足4时三栏一定完整，也允许重3且恰为虎馬鷄时三栏完整。羊不在上期四肖内，单羊可在零重时独立出现。保留单与二，三栏兔→鷄；鷄与兔均偶1四码，不证明鷄更可能。','important_cost':'前六重0、1、2肖时，三栏必不完整；重3不是虎馬鷄也会断。共同虎缺二三断，羊缺单二断，1路至多一球使三栏断；重4时若羊缺，只有三栏完整而不能全栏完成。此案优先处理高重肖、牺牲原案重2时三栏可成的机会。','model_limit':'公平49码模型下原案与修订案的无条件栏目和零栏概率相同，不能声称因修订提升预测或避免失败；所有条件概率只作数学示意。'}
for name,obj in [('revision_design.json',p),('revision_decision.json',m)]:
 f=O/name;assert not f.exists();f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'WRITTEN_NOT_YET_PUBLISHED','revision':'R01 / original alternative AA16','single':m['single'],'pair':m['pair'],'triple':m['triple'],'reserve':m['reserve'],'target_result_read':False,'sha256':hashlib.sha256((O/'revision_decision.json').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
