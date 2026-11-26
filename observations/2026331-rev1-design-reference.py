#!/usr/bin/env python3
"""Record user-directed 1–2 previous-normal alternatives before formal revision audit."""
from pathlib import Path
import hashlib,json,subprocess
R=Path('/home/user');A=R/'archive/task304_331_revision';B=A/'before';Q=A/'analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True);assert J(Q/'freeze_receipt.json')['status']=='PASS_FROZEN_NOT_PREDRAW_CERTIFICATION' and not (Q/'revision_design.json').exists()
# Names are human design IDs, not independent trials. Previous 330 normal ball order is inferred.
rows=[
('FF01','馬','鷄','牛','龍','蛇',['虎'],'原331已上线方案：3个上期前六肖，零重肖必零栏；鷄为共同位。'),
('GG01','馬','狗','牛','兔','蛇',['虎'],'本次选择：2个上期前六肖；二栏狗牛同0路但奇偶各一，三肖狗兔蛇三路且均非上期前六肖。'),
('GG02','馬','龍','鷄','鼠','蛇',['牛'],'原比较案FF08：2个上期前六肖，三肖皆新；五展示肖全完需至少三个1路。'),
('GG03','馬','龍','豬','兔','虎',['鷄'],'2个上期前六肖（馬、豬）；二栏跨0／2路，三肖跨三路；豬上期出现两球不说明将续出。'),
('GG04','馬','狗','豬','兔','蛇',['虎'],'2个上期前六肖（馬、豬）；二栏及三肖均需要2路；豬上期出现两球不说明将续出。'),
('GG05','馬','龍','羊','兔','蛇',['虎'],'1个上期前六肖，组三全新；二栏龍羊同0路，全栏只能重1或2肖。'),
('GG06','馬','狗','羊','兔','蛇',['虎'],'1个上期前六肖，三肖全新；二栏狗羊同0路，全栏只能重1或2肖。'),
('GG07','馬','羊','猴','兔','虎',['龍'],'2个上期前六肖（馬、猴），二栏跨0／2路，三肖跨三路；上期猴出现不证明续出。'),
('GG08','馬','虎','牛','龍','兔',['鷄'],'2个上期前六肖，但上期正式展示五肖保留四个；二栏和三肖需要2路。'),
('GG09','馬','鷄','虎','龍','蛇',['牛'],'原比较案FF03：2个上期前六肖，但共同位仍是上期鷄，零重肖时仍三栏全断。')]
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');prev={'馬','猴','豬','牛','鷄'};old={'馬','鷄','牛','龍','虎'};initial={'馬','鷄','牛','龍','蛇'};out=[]
for id,top,A0,B0,C,D,reserves,comment in rows:
 rr={'top':top,'A':A0,'B':B0,'C':C,'D':D};shown=set(rr.values());assert len(shown)==5 and len(set(reserves))==1 and not shown.intersection(reserves) and len(shown|set(reserves))==6 and shown|set(reserves)<=set(Z);out.append({'id':id,'roles':rr,'reserves':reserves,'comment':comment,'previous_six_overlap':[z for z in Z if z in shown&prev],'changed_relative_to_330_display':[z for z in Z if z in old-shown],'new_relative_to_330_display':[z for z in Z if z in shown-old],'changed_relative_to_initial_331':[z for z in Z if z in initial-shown],'new_relative_to_initial_331':[z for z in Z if z in shown-initial]})
assert len(out)==10 and out[1]['id']=='GG01' and len(out[0]['previous_six_overlap'])==3 and len(out[1]['previous_six_overlap'])==2 and len(out[1]['changed_relative_to_330_display'])==3 and len(out[1]['changed_relative_to_initial_331'])==2 and all(len(x['previous_six_overlap']) in (1,2) for x in out[1:])
obj={'status':'COMPARISONS_RECORDED_AFTER_330_AND_INITIAL_331_NOT_BLIND','user_direction':'Contrast original 3 previous-six identities with alternatives containing 1–2, review failure conditions, then update 331. Previous six/seventh partition remains inferred.','choice':'GG01','selection_basis':'Choose a two-old/three-new formal display rather than the old three-old/two-new; change two formal identities from published 331 and three from 330; isolate horse single, make pair odd/even, make the common sign absent from 330 normal six, and use three different routes in triple. Within these structural constraints dog and ox are a human identity choice, not a demonstrated predictive signal. Horse single and four distinct four-code signs retain the original ideal model, not a statistical improvement.','exploration_disclosure':'330 outcome, previous initial 331 alternatives, 37 retained versions, cohort frequencies, old fair models and hindsight summaries were already visible before these choices and constraints. The formal new comparisons and exact conditional audit are computed afterwards. This is not blind, prospective, preregistered, statistically validated or time-certified. No 331 result was queried or used.','target_331_result_queried_or_used':False,'candidate_count':len(out),'candidates':out};(Q/'revision_design.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':obj['status'],'selected':out[1], 'count':len(out),'sha256':H(Q/'revision_design.json')},ensure_ascii=False,indent=2))
