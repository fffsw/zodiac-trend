#!/usr/bin/env python3
"""Independent raw-record recount of revised max-repeat study and concrete counterexamples."""
from pathlib import Path
from datetime import date
from collections import Counter
import csv,hashlib,json,subprocess
R=Path('/home/user');A=R/'archive/task290_326_revision';B=A/'before';O=A/'analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=J(O/'maximum_study.json');u=J(B/'325-user-result.json');checks=[]
def ok(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
def C(p):
 with p.open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
raw=C(B/'445-source-through-311.csv');hist=C(B/'history-through-325.csv');rec=[]
for r in raw:
 nums=list(map(int,r['numbers'].split()));z=r['zodiacs'].split();assert len(nums)==len(z)==7 and (r['usable']=='1')==(len(set(nums))==7);rec.append((int(r['period']),r['date'],nums,z,r['usable']=='1'))
for r in reversed(hist):
 p=int(r['period'])
 if 2026312<=p<=2026325:rec.append((p,r['date'],[int(r[f'n{i}']) for i in range(1,7)]+[int(r['special'])],[r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']],True))
assert len(rec)==2506 and rec[-1][0]==2026325 and all(x[0]<=2026325 for x in rec) and [x[0] for x in rec if not x[4]]==[2020005,2020038] and rec[-1][2]==u['normal_numbers']+[u['seventh_number']]
def adjacent(a,b):
 p,q=a[0],b[0]
 if p//1000==q//1000:return q-p==1
 if q//1000==p//1000+1 and q%1000==1:
  try:return (date.fromisoformat(b[1])-date.fromisoformat(a[1])).days==1
  except ValueError:return False
 return False
P=[];bad=[]
for a,b in zip(rec,rec[1:]):
 if not a[4] or not b[4] or not adjacent(a,b):bad.append([a[0],b[0]]);continue
 P.append((a,b,len(set(a[3][:6])&set(b[3][:6])),len(set(a[3])&set(b[3]))))
assert len(P)==m['valid_adjacent_pairs']==2501 and bad==m['excluded_pairs'] and len(bad)==4
ok(True,'raw year-specific signs, invalid rows, exact adjacency and target-not-read scope independently reconstructed')
def dd(rows,k):
 vals=[x[k] for x in rows];return [vals.count(i) for i in range(5)],max(vals),vals.count(max(vals))
tests=[('both_four_2024plus',lambda a:len(set(a[3][:6]))==len(set(a[3]))==4 and a[0]>=2024001),('both_four_2020plus',lambda a:len(set(a[3][:6]))==len(set(a[3]))==4),('both_four_2026',lambda a:len(set(a[3][:6]))==len(set(a[3]))==4 and a[0]//1000==2026),('both_four_shape_325_2024plus',lambda a:len(set(a[3][:6]))==len(set(a[3]))==4 and a[0]>=2024001 and sorted(Counter(a[3][:6]).values(),reverse=True)==[2,2,1,1] and sorted(Counter(a[3]).values(),reverse=True)==[2,2,2,1])]
for key,fn in tests:
 v=[x for x in P if fn(x[0])]
 for idx,label in [(2,'next_six_repeat'),(3,'next_seven_repeat')]:
  d,ma,ct=dd(v,idx);g=m['historical_groups'][key][label];assert (g['n'],g['counts_0_to_4'],g['maximum_observed'],g['maximum_observed_count'])==(len(v),d,ma,ct);expected={(x[0][0],x[1][0]) for x in v if x[idx]==ma};assert expected=={(x['previous'],x['next']) for x in g['max_example_pairs']}
all6=[x for x in P if x[0][0]>=2024001 and len(set(x[0][3][:6]))==4];v=m['historical_groups']['only_six_four_2024plus']['next_six_repeat'];assert (v['n'],v['counts_0_to_4'],v['maximum_observed'],v['maximum_observed_count'])==(201,[18,65,80,33,5],4,5) and dd(all6,2)==([18,65,80,33,5],4,5)
all7=[x for x in P if x[0][0]>=2024001 and len(set(x[0][3]))==4];assert len(all7)==67 and [sum(len(set(a[3])&set(b[3][:6]))==i for a,b,_,_ in all7) for i in range(5)]==m['historical_groups']['only_seven_four_2024plus']['next_six_repeat_from_previous_seven']['counts_0_to_4']==[6,25,24,12,0]
ok(True,'maxima, maximum frequencies, 0–4 distributions and all cited max-case identifiers independently recounted for each distinct cohort')
by={x[0]:x for x in rec};x=by[2024090];y=by[2024091];assert len(set(x[3][:6]))==4 and len(set(x[3]))==5 and len(set(x[3][:6])&set(y[3][:6]))==4
for p in (2025276,2026090):
 x,y=by[p],by[p+1];assert len(set(x[3][:6]))==len(set(x[3]))==4 and len(set(x[3][:6])&set(y[3][:6]))==3 and len(set(x[3])&set(y[3]))==4
valid24=[x for x in rec if x[4] and x[0]>=2024001];assert len(valid24)==1056
for n in (6,7):
 c=Counter(len(set(x[3][:n])) for x in valid24);q=m['distinct_counts_2024plus'][str(n)];assert q['n']==len(valid24) and {str(k):v for k,v in sorted(c.items())}==q['counts'] and min(c)==q['observed_minimum']==3;ex=by[q['example']['period']];assert ex[2]==q['example']['numbers'] and ex[3]==q['example']['zodiacs'] and len(set(ex[3][:n]))==3
ok(True,'historical maximum-six and maximum-seven examples plus fewer-than-four counterexamples verified against original-year raw records')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z=lambda n:Z[(7-n)%12];prev=set(u['normal_zodiacs']);w=m['constructive_six_number_counterexample_not_real_326'];assert len(prev)==len(set(u['normal_zodiacs']+[u['seventh_zodiac']]))==4 and len(w)==len(set(w))==6 and len(prev&{n2z(n) for n in w})==4 and m['theoretical_maximum_repeat_six']==m['theoretical_maximum_repeat_seven']==4
ok(True,'upper bound four is attainable by an explicitly synthetic six-number construction; not a forecast')
a=J(B/'four-sign-conjoint.json');s=J(B/'four-sign-study.json');assert a['groups']['2024plus']['next_normal_repeat']['counts']==m['historical_groups']['both_four_2024plus']['next_six_repeat']['counts_0_to_4'] and a['groups']['2024plus']['next_seven_repeat']['counts']==m['historical_groups']['both_four_2024plus']['next_seven_repeat']['counts_0_to_4'] and [s['cohorts']['2024plus']['normal4_next_normal']['counts'][str(i)] for i in range(5)]==v['counts_0_to_4']
prior=C(B/'four-sign-pairs.csv');now=C(O/'maximum_pairs.csv');assert len(prior)==len(now)
for x,y in zip(prior,now):assert (x['prev'],x['next'],x['prev6'],x['prev7'],x['next6'],x['next7'],x['six_six_signs'],x['six_six_count'],x['seven_seven_signs'],x['seven_seven_count'])==(y['previous'],y['next'],y['prev6'],y['prev7'],y['next6'],y['next7'],y['repeat6'],y['repeat6_count'],y['repeat7'],y['repeat7_count'])
subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True)
ok(True,'revised pair ledger agrees with previously published independent study and frozen sources')
out={'status':'PASS','scope':'exploratory historical maxima and theoretical bounds; no claim of authenticated source, future ceiling or forecast','checks':checks,'maximum_study_sha256':H(O/'maximum_study.json'),'maximum_pairs_sha256':H(O/'maximum_pairs.csv')};p=O/'maximum_independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
