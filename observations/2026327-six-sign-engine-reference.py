#!/usr/bin/env python3
"""Exploratory six-distinct prior-sign followup, strictly through user 326.
2024-26 recorded zodiac labels are used as stored for each historical record.
A target-327 result is neither sought nor included; counts are not probabilities.
"""
from pathlib import Path
from collections import Counter
from datetime import date
from itertools import product
from math import comb
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task292_327_release';O=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text(encoding='utf8'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert J(O/'evidence_qc.json')['status']=='PASS' and J(O/'user_326_stage.json')['period']==2026326 and not (O/'six_sign_repeat_study.json').exists()
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rr=sorted(csv.DictReader(f),key=lambda x:int(x['period']))
assert len(rr)==1057 and rr[0]['period']=='2024001' and rr[-1]['period']=='2026326' and not any(int(x['period'])>2026326 for x in rr)
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');order=lambda a:sorted(set(a),key=Z.index);n=lambda r:[int(r[f'n{i}']) for i in range(1,7)]+[int(r['special'])];z=lambda r:[r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']]
def adj(a,b):
 p,q=int(a['period']),int(b['period'])
 if p//1000==q//1000:return q==p+1
 if q//1000==p//1000+1 and q%1000==1:
  try:return (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days==1
  except ValueError:return False
 return False
pairs=[];excluded=[]
for a,b in zip(rr,rr[1:]):
 if not (adj(a,b) and len(set(n(a)))==len(set(n(b)))==7):excluded.append([int(a['period']),int(b['period'])]);continue
 az,bz=z(a),z(b);a6=set(az[:6]);a7=set(az);b6=set(bz[:6]);b7=set(bz)
 if len(a6)==len(a7)==6:pairs.append({'previous':int(a['period']),'next':int(b['period']),'prev6':order(a6),'prev7':order(a7),'next6':order(b6),'next7':order(b7),'repeat6':order(a6&b6),'repeat7':order(a7&b7),'repeat6_count':len(a6&b6),'repeat7_count':len(a7&b7),'source':'historical recorded zodiac labels; not authenticated'})
assert not excluded and len(pairs)==131 and max(x['next'] for x in pairs)<=2026326
C=lambda xs,key:[sum(x[key]==i for x in xs) for i in range(7)];groups={}
for name,xs in [('2024plus',pairs),('2024',[x for x in pairs if x['previous']//1000==2024]),('2025',[x for x in pairs if x['previous']//1000==2025]),('2026',[x for x in pairs if x['previous']//1000==2026])]:groups[name]={'n':len(xs),'six_to_six_counts_0_to_6':C(xs,'repeat6_count'),'seven_to_seven_counts_0_to_6':C(xs,'repeat7_count')}
assert groups['2024plus']=={'n':131,'six_to_six_counts_0_to_6':[2,9,45,47,25,3,0],'seven_to_seven_counts_0_to_6':[0,3,33,54,34,6,1]} and groups['2026']['n']==47 and pairs[-1]['previous']==2026324 and pairs[-1]['next']==2026325
# User 326 is a pending trigger: never count the unknown next period in empirical denominator.
current=z(rr[-1]);current6=set(current[:6]);current7=set(current);assert current6==current7=={'狗','兔','鷄','羊','虎','猴'} and len(current6)==6
G={q:[i for i in range(1,50) if Z[(7-i)%12]==q] for q in Z};sizes=[len(G[q]) for q in order(current6)];assert sizes==[4]*6;other=49-sum(sizes);assert other==25
model={}
for draw in (6,7):
 counts=[0]*7
 for ks in product(*(range(s+1) for s in sizes)):
  rest=draw-sum(ks)
  if 0<=rest<=other:
   w=comb(other,rest)
   for s,k in zip(sizes,ks):w*=comb(s,k)
   counts[sum(k>0 for k in ks)]+=w
 den=comb(49,draw);assert sum(counts)==den
 model[str(draw)]={'prior_identities':order(current6),'prior_group_sizes':sizes,'other_number_count':other,'denominator':den,'counts_0_to_6':counts,'percent_0_to_6':[100*x/den for x in counts]}
witness_max=[17,4,10,12,11,21];witness_zero=[6,3,2,1,7,8];n2z=lambda x:Z[(7-x)%12];assert len(set(witness_max))==len(set(witness_zero))==6 and len(current6&{n2z(x) for x in witness_max})==6 and len(current6&{n2z(x) for x in witness_zero})==0
out={'status':'PASS_DESCRIPTIVE_EXPLORATORY_NOT_FORECAST','scope':'Condition selected after seeing user 326; six distinct prior signs in both prior six and seven. Follow-up historical values only through 326. User record date and official source unknown; no 327 result read. Historical labels per historical record, not remapped to 2026. Adjacent windows and outcomes may overlap.','input_history_sha256':H(S/'data/macau_mark_six_full.csv'),'historical_records':len(rr),'excluded_invalid_or_nonadjacent_pairs':excluded,'groups':groups,'current_pending':{'previous_issue':2026326,'previous_six':order(current6),'previous_seven':order(current7),'target_issue':2026327,'target_result_read':False,'included_in_followup_denominators':False},'theoretical_repeat_max_six_to_six':6,'theoretical_repeat_max_seven_to_seven':6,'witness_six_repeat_6_not_327':[{'number':x,'zodiac':n2z(x)} for x in witness_max],'witness_six_repeat_0_not_327':[{'number':x,'zodiac':n2z(x)} for x in witness_zero],'uniform_49_independent_model':model,'limitations':'Joint six-sign cohort is exploratory selected after observing 326; conditional association is not a forecast. Zodiac data and draw mechanism are unauthenticated. Six vs six and seven vs seven are distinct; zero observed is not impossibility. Uniform model assumes 49 equiprobable numbers, without replacement per draw and independence across draws.'}
(O/'six_sign_repeat_study.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with (O/'six_sign_repeat_pairs.csv').open('x',encoding='utf8',newline='') as f:
 cols=['previous','next','prev6','prev7','next6','next7','repeat6','repeat6_count','repeat7','repeat7_count','source'];w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
 for x in pairs:w.writerow({k:(' '.join(v) if isinstance(v,list) else v) for k,v in x.items()})
print(json.dumps({'status':out['status'],'groups':groups,'theoretical_repeat_max':6,'model_percent_6':model['6']['percent_0_to_6'],'model_percent_7':model['7']['percent_0_to_6'],'target_result_read':False},ensure_ascii=False,indent=2))
