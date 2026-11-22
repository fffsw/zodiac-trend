#!/usr/bin/env python3
"""Prespecified descriptive adjacent-repeat study through user 325; never reads 326."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import product
from math import comb
import csv,json,hashlib
R=Path('/home/user');T=R/'archive/task288_325_review';O=R/'archive/task289_326_release/analysis';B=T/'before';J=lambda p:json.loads(p.read_text(encoding='utf8'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert J(T/'analysis/independent_qc.json')['status']=='PASS';spec=J(O/'four_sign_study_spec.json');u=J(T/'input/user-325.json');assert u['issue']==2026325 and u['normal_numbers']==[41,37,10,1,27,17] and u['seventh_number']==3
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');order=lambda a:sorted(set(a),key=Z.index)
with (B/'445-source-through-311.csv').open(encoding='utf8',newline='') as f:old=list(csv.DictReader(f))
with (B/'history-through-324.csv').open(encoding='utf8',newline='') as f:main=list(csv.DictReader(f))
assert len(old)==2492 and old[-1]['period']=='2026311' and len(main)==1055 and main[0]['period']=='2026324'
old_by={int(x['period']):x for x in old};match=0
for x in main:
 p=int(x['period']);y=old_by.get(p)
 if y:
  ns=[int(x[f'n{i}']) for i in range(1,7)]+[int(x['special'])];zs=[x[f'z{i}'] for i in range(1,7)]+[x['special_zodiac']]
  assert ns==[int(n) for n in y['numbers'].split()] and zs==y['zodiacs'].split(),p;match+=1
assert match==1042
rows=[]
for x in old:
 nums=[int(n) for n in x['numbers'].split()];signs=x['zodiacs'].split();valid=x['usable']=='1';assert len(nums)==len(signs)==7 and all(n in range(1,50) for n in nums) and all(z in Z for z in signs)
 assert valid==(len(set(nums))==7);rows.append({'period':int(x['period']),'date':x['date'],'numbers':nums,'zodiacs':signs,'usable':valid,'source':x['source']})
for x in reversed([x for x in main if 2026312<=int(x['period'])<=2026324]):
 rows.append({'period':int(x['period']),'date':x['date'],'numbers':[int(x[f'n{i}']) for i in range(1,7)]+[int(x['special'])],'zodiacs':[x[f'z{i}'] for i in range(1,7)]+[x['special_zodiac']],'usable':True,'source':'user-provided appended history'})
rows.append({'period':2026325,'date':'','numbers':u['normal_numbers']+[u['seventh_number']],'zodiacs':u['normal_zodiacs']+[u['seventh_zodiac']],'usable':True,'source':'user-provided current issue'})
assert len(rows)==2506 and rows[-1]['period']==2026325 and all(a['period']<b['period'] for a,b in zip(rows,rows[1:])) and len([x for x in rows if not x['usable']])==2
assert [int(x['period']) for x in rows[-14:]]==list(range(2026312,2026326))
def adjacent(a,b):
 ap,bp=a['period'],b['period'];ay,by=ap//1000,bp//1000;an,bn=ap%1000,bp%1000
 if ay==by:return bn==an+1
 if by!=ay+1 or bn!=1:return False
 from datetime import date
 try:return (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days==1
 except ValueError:return False
pairs=[];invalid=[]
for i in range(len(rows)-1):
 a,b=rows[i:i+2]
 if not (a['usable'] and b['usable'] and adjacent(a,b)):
  invalid.append([a['period'],b['period']]);continue
 a6=a['zodiacs'][:6];a7=a['zodiacs'];b6=b['zodiacs'][:6];b7=b['zodiacs'];s6=set(a6);s7=set(a7);n6=set(b6);n7=set(b7)
 incoming=None
 if i>0 and rows[i-1]['usable'] and adjacent(rows[i-1],a):incoming=len(set(rows[i-1]['zodiacs'])&s7)
 pairs.append({'prev':a['period'],'next':b['period'],'prev6':order(s6),'prev7':order(s7),'next6':order(n6),'next7':order(n7),'prior6_multiplicity':sorted(Counter(a6).values(),reverse=True),'prior7_multiplicity':sorted(Counter(a7).values(),reverse=True),'prev6_multiplicity_map':dict(Counter(a6)),'prev7_multiplicity_map':dict(Counter(a7)),'six_six_signs':order(s6&n6),'seven_six_signs':order(s7&n6),'seven_seven_signs':order(s7&n7),'incoming_seven_seven_count':incoming})
assert len(pairs)==2501 and len(invalid)==4 and all(x['next']<=2026325 for x in pairs)
for x in pairs:
 x['six_six_count']=len(x['six_six_signs']);x['seven_six_count']=len(x['seven_six_signs']);x['seven_seven_count']=len(x['seven_seven_signs'])
assert pairs[-1]['prev']==2026324 and pairs[-1]['next']==2026325 and pairs[-1]['six_six_count']==pairs[-1]['seven_seven_count']==1
# Followup count distribution. All four-sign outcomes are necessarily 0 through 4.
def dist(xs,key,maxv=4):
 c=Counter(x[key] for x in xs);return {'n':len(xs),'counts':{str(i):c[i] for i in range(maxv+1)},'percent':{str(i):(round(100*c[i]/len(xs),6) if xs else None) for i in range(maxv+1)}}
def table(xs):
 return {'normal4_next_normal':dist([x for x in xs if len(x['prev6'])==4],'six_six_count'), 'seven4_next_normal':dist([x for x in xs if len(x['prev7'])==4],'seven_six_count'), 'seven4_next_seven':dist([x for x in xs if len(x['prev7'])==4],'seven_seven_count'), 'any6_next6_baseline':dist(xs,'six_six_count',6),'any7_next7_baseline':dist(xs,'seven_seven_count',7)}
coh={'2024plus':[x for x in pairs if x['prev']>=2024001],'all_2020plus':pairs}
for year in (2024,2025,2026):coh[str(year)]=[x for x in pairs if x['prev']//1000==year]
for w in (35,40,45):
 threshold=rows[-w]['period'];coh[f'last_{w}_prior_trigger_periods']=[x for x in pairs if x['prev']>=threshold]
summary={k:table(v) for k,v in coh.items()}
for w in (35,40,45):
 threshold=rows[-w]['period'];r=rows[-w:];summary[f'last_{w}_prior_trigger_periods']['window']={'start_trigger_period':threshold,'end_trigger_period':2026325,'input_periods_in_window':w,'325_normal_and_seven_four_pending':True,'pending_current_period_excluded_from_followup_denominator':True,'other_unusable_trigger_periods_in_window':sum(not x['usable'] for x in r)}
base=coh['2024plus'];subsets={
 'normal4_exact_2_2_1_1':[x for x in base if len(x['prev6'])==4 and x['prior6_multiplicity']==[2,2,1,1]],
 'seven4_exact_2_2_2_1':[x for x in base if len(x['prev7'])==4 and x['prior7_multiplicity']==[2,2,2,1]],
 'seven4_incoming_repeat_one':[x for x in base if len(x['prev7'])==4 and x['incoming_seven_seven_count']==1],
 'normal4_exact_325_signs':[x for x in base if set(x['prev6'])=={'虎','馬','鷄','龍'}]}
sub={k:table(v) for k,v in subsets.items()}
# Exposure-level descriptions (4 identities per event; they are correlated, not independent trials).
expo=defaultdict(lambda:[0,0]);personal=defaultdict(lambda:[0,0])
for x in subsets['normal4_exact_2_2_1_1']:
 for sign,mult in x['prev6_multiplicity_map'].items():
  if mult not in (1,2):raise AssertionError(mult)
  k=f'prior_{mult}_normal_balls';expo[k][0]+=1;expo[k][1]+=sign in x['next6'];personal[sign][0]+=1;personal[sign][1]+=sign in x['next6']
exposure={k:{'identity_exposures':v[0],'identities_also_in_next_normal':v[1],'percent_descriptive':round(100*v[1]/v[0],6) if v[0] else None} for k,v in expo.items()};by_identity={k:{'exposures':v[0],'repeated_next_normal':v[1]} for k,v in personal.items()}
# Ideal independent 49-number model, fixed current 325 set; 6 and 7 are separate.
G={z:[n for n in range(1,50) if Z[(7-n)%12]==z] for z in Z};current=['虎','馬','鷄','龍'];sizes=[len(G[z]) for z in current];other=49-sum(sizes);assert sizes==[4,5,4,4] and other==32
model={}
for n in (6,7):
 c=[0]*5
 for v in product(*(range(s+1) for s in sizes)):
  rem=n-sum(v)
  if rem<0 or rem>other:continue
  ways=comb(other,rem)
  for s,k in zip(sizes,v):ways*=comb(s,k)
  c[sum(k>0 for k in v)]+=ways
 den=comb(49,n);assert sum(c)==den;model[str(n)]={'population_group_sizes':sizes,'other_numbers':other,'denominator':den,'exact_counts':c,'percent':[100*k/den for k in c],'expected_distinct_repeated':sum(i*k for i,k in enumerate(c))/den}
res={'status':'PASS_DESCRIPTIVE_NOT_A_FORECAST','spec_sha256':H(O/'four_sign_study_spec.json'),'source_sha256':H(B/'445-source-through-311.csv'),'source_main_overlap_exact_records':match,'records':len(rows),'first_period':rows[0]['period'],'last_period':rows[-1]['period'],'invalid_records':[x['period'] for x in rows if not x['usable']],'invalid_or_nonadjacent_pairs':invalid,'valid_pairs':len(pairs),'current_period_pending_326':{'period':2026325,'normal_distinct':order(rows[-1]['zodiacs'][:6]),'seven_distinct':order(rows[-1]['zodiacs']),'normal_multiplicity':sorted(Counter(rows[-1]['zodiacs'][:6]).values(),reverse=True),'seven_multiplicity':sorted(Counter(rows[-1]['zodiacs']).values(),reverse=True),'incoming_repeat_324_325':pairs[-1]['seven_seven_count'],'follow_period':2026326,'follow_numbers_read':False},'cohorts':summary,'subgroups_2024plus':sub,'exact_identity_matches_2024plus':[{'previous':x['prev'],'next':x['next'],'next_six_repeat_count':x['six_six_count'],'next_six_repeat_signs':x['six_six_signs'],'next_seven_repeat_count':x['seven_seven_count'],'next_seven_repeat_signs':x['seven_seven_signs']} for x in subsets['normal4_exact_325_signs']],'previous_normal_multiplicity_exposure_2024plus':exposure,'previous_normal_multiplicity_by_sign_2024plus':by_identity,'ideal_independent_49_model':model,'limits':'Historical sets and data are unauthenticated; earliest 2020 partly single-source and questionable. Windows overlap; subgroups overlap and may be small; adjacent exposures and prior identities are not independent. No demonstrated predictive edge or outcome guarantee.'}
p=O/'four_sign_study.json';assert not p.exists();p.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
field=['prev','next','prev6','prev7','next6','next7','prior6_multiplicity','prior7_multiplicity','six_six_signs','six_six_count','seven_six_signs','seven_six_count','seven_seven_signs','seven_seven_count','incoming_seven_seven_count']
with (O/'four_sign_pairs.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=field);w.writeheader()
 for x in pairs:
  if len(x['prev6'])==4 or len(x['prev7'])==4:
   row={k:x[k] for k in field};row={k:(' '.join(map(str,v)) if isinstance(v,list) else v) for k,v in row.items()};w.writerow(row)
print(json.dumps({'status':res['status'],'records':res['records'],'pairs':res['valid_pairs'],'invalid':res['invalid_or_nonadjacent_pairs'],'current':res['current_period_pending_326'],'cohorts':{k:v for k,v in summary.items() if k in ('2024plus','all_2020plus','2024','2025','2026','last_35_prior_trigger_periods','last_40_prior_trigger_periods','last_45_prior_trigger_periods')},'subgroups':{k:{'normal4_next_normal':v['normal4_next_normal'],'seven4_next_normal':v['seven4_next_normal'],'seven4_next_seven':v['seven4_next_seven']} for k,v in sub.items()},'exact_identity_matches':res['exact_identity_matches_2024plus'],'exposure':exposure,'by_identity':by_identity,'ideal_model':model},ensure_ascii=False,indent=2))
