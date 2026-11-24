#!/usr/bin/env python3
"""Fresh 327/328 deep review from frozen data, with exact state enumeration. No 328 result lookup."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,permutations,product
from math import comb
from datetime import date
import csv,hashlib,json,subprocess
R=Path('/home/user');A=R/'archive/task297_328_deep_review';B=A/'before';O=A/'analysis';J=lambda n:json.loads((B/n).read_text(encoding='utf8'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not any((O/n).exists() for n in ('deep_metrics.json','repeat_structural.csv','recent_45_comparison.csv'))
subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True);decision=J('manual-decision.json');audit=J('candidate-audit.json');assert decision['choice']=='CC01' and not decision['target_328_result_queried_or_used'] and audit['status']=='PASS'
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');den=comb(49,6);num=lambda row:[int(row[f'n{i}']) for i in range(1,7)]+[int(row['special'])];sign=lambda row:[row[f'z{i}'] for i in range(1,7)]+[row['special_zodiac']];zh=lambda n,k:Z[(k-n)%12];curmap={z:[n for n in range(1,50) if zh(n,7)==z] for z in Z};assert {z:len(v) for z,v in curmap.items()}=={z:(5 if z=='馬' else 4) for z in Z}
with (B/'history-through-user-327.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda x:int(x['period']))
expected=list(range(2024001,2024367))+list(range(2025001,2025366))+list(range(2026001,2026328));assert [int(x['period']) for x in rows]==expected and len(rows)==1058
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};norm={'紅':'红','藍':'蓝','綠':'绿'};offset={};missing=[]
for row in rows:
 pp=int(row['period']);nn=num(row);zz=sign(row);assert all(1<=n<=49 for n in nn) and len(set(nn))==7 and all(z in Z for z in zz)
 vals={(Z.index(z)+n)%12 for n,z in zip(nn,zz)};assert len(vals)==1;offset[pp]=next(iter(vals));ww=[row[f'w{i}'] for i in range(1,7)]+[row['special_wave']]
 for n,w in zip(nn,ww):assert norm.get(w,w)==('红' if n in red else '蓝' if n in blue else '绿'),(pp,n,w)
 if row['date']:date.fromisoformat(row['date'])
 else:missing.append(pp)
assert missing==list(range(2026313,2026328)) and num(rows[-1])==[21,49,7,41,46,36,45] and offset[2026327]==7
changes=[];cohort=[]
for prev,nxt in zip(rows,rows[1:]):
 a,b=int(prev['period']),int(nxt['period']);assert (a//1000==b//1000 and b==a+1) or (b//1000==a//1000+1 and b%1000==1 and (date.fromisoformat(nxt['date'])-date.fromisoformat(prev['date'])).days==1)
 if offset[a]!=offset[b]:changes.append({'from_period':a,'to_period':b,'from_date_as_stored':prev['date'],'to_date_as_stored':nxt['date'],'from_offset':offset[a],'to_offset':offset[b]})
 az,bz=sign(prev),sign(nxt)
 if len(set(az[:6]))==len(set(az))==6:
  old6=len(set(az[:6])&set(bz[:6]));old7=len(set(az)&set(bz));fix6=len({zh(x,7) for x in num(prev)[:6]}&{zh(x,7) for x in num(nxt)[:6]});fix7=len({zh(x,7) for x in num(prev)}&{zh(x,7) for x in num(nxt)})
  cohort.append({'prev':a,'next':b,'stored_six':old6,'stored_seven':old7,'fixed_mapping_six':fix6,'fixed_mapping_seven':fix7,'crosses_internal_mapping_change':offset[a]!=offset[b]})
assert len(changes)==3 and [(x['from_period'],x['to_period']) for x in changes]==[(2024040,2024041),(2025028,2025029),(2026047,2026048)] and len(cohort)==132 and not any(x['crosses_internal_mapping_change'] for x in cohort) and all(x['stored_six']==x['fixed_mapping_six'] and x['stored_seven']==x['fixed_mapping_seven'] for x in cohort)
assert [sum(x['stored_six']==i for x in cohort) for i in range(7)]==[2,9,45,47,26,3,0] and [sum(x['stored_seven']==i for x in cohort) for i in range(7)]==[0,3,33,54,35,6,1]
# Enumerate finite populations grouped by selected identities and an unselected catch-all.
def model(single,pair,triple,off=7):
 names=list(dict.fromkeys(single+pair+triple));sizes={z:sum(zh(n,off)==z for n in range(1,50)) for z in names};rest=49-sum(sizes.values());out=Counter()
 for ks in product(*(range(sizes[z]+1) for z in names)):
  other=6-sum(ks)
  if not 0<=other<=rest:continue
  ways=comb(rest,other)
  for z,k in zip(names,ks):ways*=comb(sizes[z],k)
  s={z for z,k in zip(names,ks) if k};key=''.join('1' if set(group)<=s else '0' for group in (single,pair,triple));out[key]+=ways
 for i in range(8):out.setdefault(f'{i:03b}',0)
 assert sum(out.values())==den
 col=[sum(c for k,c in out.items() if k.count('1')==n) for n in range(4)];single_count=sum(c for k,c in out.items() if k[0]=='1');pair_count=sum(c for k,c in out.items() if k[1]=='1');triple_count=sum(c for k,c in out.items() if k[2]=='1');return {'group_sizes':sizes,'displayed_numbers':sum(sizes.values()),'patterns_single_pair_triple':dict(sorted(out.items())),'complete_columns_0_to_3_counts':col,'complete_columns_0_to_3_pct':[100*x/den for x in col],'single_pair_triple_pct':[100*x/den for x in (single_count,pair_count,triple_count)],'at_least_one_pct':100*(den-col[0])/den,'at_least_two_pct':100*(col[2]+col[3])/den,'expected_complete_columns':sum(i*x for i,x in enumerate(col))/den}
cc=(['馬'],['狗','鷄'],['狗','馬','蛇']);bb=(['馬'],['鷄','龍'],['鷄','虎','牛']);ccm=model(*cc);bbm=model(*bb);alt=model(*cc,off=8);assert ccm['patterns_single_pair_triple']['001']==ccm['patterns_single_pair_triple']['011']==0 and ccm['complete_columns_0_to_3_counts']==[5728968,6766768,1256160,231920] and bbm['complete_columns_0_to_3_counts']==[5392128,7401592,1144016,46080]
assert alt['group_sizes']=={'馬':4,'狗':4,'鷄':4,'蛇':4} and alt['displayed_numbers']==16 and alt['complete_columns_0_to_3_counts']==[6667992,6080128,1045360,190336]
assert ccm['complete_columns_0_to_3_counts'][0]==audit['selected']['ideal_model']['counts']['no_complete_column'] and ccm['complete_columns_0_to_3_counts'][3]==audit['selected']['ideal_model']['counts']['all_columns']
zero_first=comb(40,6);zero_second=comb(40,6)-comb(36,6);none_display=comb(32,6);assert zero_first+zero_second==ccm['complete_columns_0_to_3_counts'][0] and none_display<zero_first
# Empirical retrospective, not performance measurement: CC01 was selected using this history.
def present(r,plan):
 got=set(sign(r)[:6]);return tuple(set(x)<=got for x in plan)
recent=list(reversed(rows[-45:]));blocks=[]
for lo,hi in ((0,9),(10,19),(20,34),(35,39),(40,44)):
 sub=recent[lo:hi+1];x=Counter(sum(present(r,cc)) for r in sub);y=Counter(sum(present(r,bb)) for r in sub);blocks.append({'age':f'{lo}-{hi}','period_range_old_to_new':[int(sub[-1]['period']),int(sub[0]['period'])],'n':len(sub),'CC01_complete_columns_0_to_3':[x[k] for k in range(4)],'BB01_complete_columns_0_to_3':[y[k] for k in range(4)]})
paired=Counter((sum(present(r,cc)),sum(present(r,bb))) for r in recent);cc45=[sum(x['CC01_complete_columns_0_to_3'][k] for x in blocks) for k in range(4)];bb45=[sum(x['BB01_complete_columns_0_to_3'][k] for x in blocks) for k in range(4)];assert cc45==[16,19,6,4] and bb45==[14,29,2,0] and [sum(x['CC01_complete_columns_0_to_3'][0] for x in blocks[:j]) for j in (3,4,5)]==[10,14,16]
# Every feasible presence set shows the deterministic repeat/complete-column constraints.
prevset=set(sign(rows[-1])[:6]);assert prevset=={'狗','馬','鼠','虎','鷄','羊'};possible=defaultdict(set);feasible=0
for count in range(1,7):
 for cs in combinations(Z,count):
  s=set(cs)
  if sum(len(curmap[z]) for z in s)<6:continue
  k=len(s&prevset);v=sum(set(x)<=s for x in cc);possible[k].add(v);feasible+=1
poss={str(k):sorted(possible[k]) for k in range(7)};assert poss=={'0':[0],'1':[0,1],'2':[0,1,2],'3':[0,1,2,3],'4':[0,1,2,3],'5':[1,2,3],'6':[2]}
witnesses={'repeat0_zero':[6,4,3,2,11,8],'repeat1_only_single':[1,6,4,3,2,11],'repeat2_single_and_triple':[1,9,2,6,4,3],'repeat3_all':[1,9,10,2,6,4],'repeat5_only_pair':[9,10,7,5,12,6],'repeat5_only_single':[1,10,7,5,12,2],'repeat6_exactly_two':[1,9,10,7,5,12]}
wout=[]
for label,ns in witnesses.items():
 assert len(ns)==len(set(ns))==6 and all(1<=n<=49 for n in ns);s={zh(n,7) for n in ns};v=[set(x)<=s for x in cc];wout.append({'case':label,'synthetic_not_328_numbers':ns,'repeat_identities':len(s&prevset),'completed_single_pair_triple':v,'complete_columns':sum(v)})
assert [(x['repeat_identities'],x['complete_columns']) for x in wout]==[(0,0),(1,1),(2,2),(3,3),(5,1),(5,1),(6,2)]
# Repeat-conditioned integer weights, keeping each of the six prior identities separate.
names=['馬','狗','鷄','蛇','鼠','虎','羊'];sizes=[len(curmap[z]) for z in names];rest=49-sum(sizes);assert rest==20;cond=[Counter() for _ in range(7)]
for ks in product(*(range(n+1) for n in sizes)):
 rem=6-sum(ks)
 if not 0<=rem<=rest:continue
 w=comb(rest,rem)
 for size,take in zip(sizes,ks):w*=comb(size,take)
 s={z for z,k in zip(names,ks) if k};repeat=len(s&prevset);vals=[set(x)<=s for x in cc];c=cond[repeat];c['denominator']+=w;c['single']+=w*vals[0];c['pair']+=w*vals[1];c['triple']+=w*vals[2];c['all_columns']+=w*all(vals);c['no_complete_column']+=w*(not any(vals))
for k,c in enumerate(cond):
 old=audit['selected_conditional_on_repeat_0_to_6'][k];assert all(c[x]==old[x] for x in ('denominator','single','pair','triple','all_columns','no_complete_column'))
assert sum(c['denominator'] for c in cond)==den and cond[5]['no_complete_column']==cond[6]['no_complete_column']==0 and cond[0]['no_complete_column']==cond[0]['denominator']
# Exact ideal distribution is invariant under any permutation among the eleven equal-sized groups.
base_tuple=tuple(ccm['patterns_single_pair_triple'][f'{i:03b}'] for i in range(8));same=0
for a,b,d in permutations([z for z in Z if z!='馬'],3):
 t=model(['馬'],[a,b],[a,'馬',d]);assert tuple(t['patterns_single_pair_triple'][f'{i:03b}'] for i in range(8))==base_tuple;same+=1
assert same==990
classes=defaultdict(list)
for x in audit['candidates']:
 q=x['roles'];t=model([q['top']],[q['A'],q['B']],[q['A'],q['C'],q['D']]);classes[tuple(t['patterns_single_pair_triple'][f'{i:03b}'] for i in range(8))].append(x['id'])
classlist=sorted((v for v in classes.values()),key=lambda v:v[0]);assert next(v for v in classlist if 'CC01' in v)==['CC01','CC05','CC06','CC07','CC08','CC09','CC10','CC12']
result={'status':'PASS_DEEP_REVIEW_NOT_A_FORECAST','scope':'Frozen local history through user 327 and 328 CC01 only; no 328 outcome lookup; old snapshots do not certify predraw, official data, clock or actual mechanism.','input_freeze_sha256':H(A/'before.sha256'),'target_328_outcome_queried_or_used':False,'data_audit':{'rows':len(rows),'numbers_in_range_and_seven_distinct':True,'wave_labels_match_local_key':True,'zodiac_label_internal_offset_consistent_all_rows':True,'undated_issue_count':len(missing),'undated_issues':missing,'offset_counts':dict(sorted(Counter(offset.values()).items())),'internal_mapping_changes':changes,'132_six_sign_cohort_cross_mapping_changes':0,'note':'Offsets/changes describe local records only, not independently verified official mapping or dates.'},'six_sign_cohort':{'n':len(cohort),'recorded_six_0_to_6':[sum(x['stored_six']==i for x in cohort) for i in range(7)],'recorded_seven_0_to_6':[sum(x['stored_seven']==i for x in cohort) for i in range(7)],'fixed_2026_remap_same_repeat_counts_for_these_pairs':True,'current_prev_group_model_repeat6_pct':100*5120/den,'iid_132_identical_current_groups_zero_repeat6_pct':100*(1-5120/den)**132,'iid_counterfactual_warning':'The 132 actual pairs are not 132 independent repeats of the current fixed six; do not apply this value as a historical p-value.'},'ideal_model':{'draws':den,'definition':'49 equally likely, 6 different numbers without replacement. No payout or profit model. For the repeat-conditioned table, additionally assume the target is independent of the frozen prior and the current offset 7 mapping persists.','BB01':bbm,'CC01':ccm,'CC01_zero_column_disjoint_partition':{'no_horse_and_no_dog_count':zero_first,'no_horse_dog_present_no_chicken_count':zero_second,'pct':[100*zero_first/den,100*zero_second/den],'no_displayed_identity_count':none_display,'no_displayed_identity_pct':100*none_display/den,'has_displayed_identity_but_zero_complete_pct':100*(ccm['complete_columns_0_to_3_counts'][0]-none_display)/den},'hypothetical_offset8_not_a_328_mapping_claim':alt,'hypothetical_offset8_mapping_examples':{z:[n for n in range(1,50) if zh(n,8)==z] for z in ('馬','狗','鷄','蛇')},'identical_ideal_distribution_role_permutations':same,'equivalence_within_12':classlist},'logical_repeat_possibilities':poss,'feasible_identity_sets_enumerated':feasible,'synthetic_witnesses_not_328':wout,'conditional_model_by_repeat':[{'repeat':k,**{n:c[n] for n in ('denominator','single','pair','triple','all_columns','no_complete_column')},'no_complete_pct':100*c['no_complete_column']/c['denominator'],'all_complete_pct':100*c['all_columns']/c['denominator']} for k,c in enumerate(cond)],'recent_45_retrospective':{'blocks':blocks,'CC01_distribution_0_to_3':cc45,'BB01_distribution_0_to_3':bb45,'paired_CC_BB_counts':{f'{x[0]}|{x[1]}':v for x,v in sorted(paired.items())},'warning':'Both candidates evaluated on the same 45 already-observed rows; CC01 was chosen after looking at this history, so this is not an independent trial or predictive comparison.'},'decision':'No new authenticated information distinguishes the selected identities; retain CC01. Supplement structural, mapping and model-objective omissions without claiming an improvement or using 328 results.'}
(O/'deep_metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
with (O/'repeat_structural.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['repeat_327_six_count','possible_complete_columns','ideal_denominator','ideal_zero_complete_count','ideal_zero_complete_pct','ideal_all_complete_count','ideal_all_complete_pct','scope'])
 for k,c in enumerate(cond):w.writerow([k,'/'.join(map(str,poss[str(k)])),c['denominator'],c['no_complete_column'],f"{100*c['no_complete_column']/c['denominator']:.6f}",c['all_columns'],f"{100*c['all_columns']/c['denominator']:.6f}",'structural possibility; fair independent 49-number model for percentages, not 328 result'])
with (O/'recent_45_comparison.csv').open('x',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['age','period_start','period_end','n','CC_zero','CC_one','CC_two','CC_three','BB_zero','BB_one','BB_two','BB_three','scope'])
 for x in blocks:w.writerow([x['age'],*x['period_range_old_to_new'],x['n'],*x['CC01_complete_columns_0_to_3'],*x['BB01_complete_columns_0_to_3'],'post-selection retrospective only, not holdout'])
print(json.dumps({'status':result['status'],'history_rows':len(rows),'internal_mapping_changes':changes,'cohort_n':len(cohort),'cohort_mapping_changes':0,'BB01_cols_pct':bbm['complete_columns_0_to_3_pct'],'CC01_cols_pct':ccm['complete_columns_0_to_3_pct'],'CC01_atleast2_pct':ccm['at_least_two_pct'],'alt_hypothetical_cols_pct':alt['complete_columns_0_to_3_pct'],'repeat_possibilities':poss,'45_hist_cc':cc45,'45_hist_bb':bb45,'equivalent_role_permutations':same,'equivalence_within_12':classlist,'target_result_read':False},ensure_ascii=False,indent=2))
