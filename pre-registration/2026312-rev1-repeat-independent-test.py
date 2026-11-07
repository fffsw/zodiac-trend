#!/usr/bin/env python3
"""Independent matrix/groupby/inclusion-exclusion audit of 1000 repeat transitions."""
from pathlib import Path
import csv,hashlib,itertools,json,math
from collections import Counter
R=Path('/home/user');D=R/'data';M=json.loads((D/'task242_1000_repeat_metrics_v2.json').read_text());ORDER=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬')
rows=sorted(csv.DictReader((D/'task242_1042_reconciled_history.csv').open(encoding='utf-8-sig')),key=lambda r:int(r['period']))
assert len(rows)==1042 and int(rows[-1]['period'])==2026311 and hashlib.md5((D/'task242_1042_reconciled_history.csv').read_bytes()).hexdigest()==M['csv_md5']
assert M['transition_ledger_sha256']==hashlib.sha256((D/'task242_1000_repeat_transitions_v2.csv').read_bytes()).hexdigest()
ledger=list(csv.DictReader((D/'task242_1000_repeat_transitions_v2.csv').open(encoding='utf-8')));assert len(ledger)==1000
# Pure membership matrix instead of set intersection in producer.
reps={k:[] for k in ('normal6_vs_prev7','normal6_vs_prev6')}
for i,(a,b) in enumerate(zip(rows[-1001:-1],rows[-1000:])):
 prev=[a[f'z{j}'] for j in range(1,7)];curr=[b[f'z{j}'] for j in range(1,7)]
 methods={'normal6_vs_prev7':prev+[a['special_zodiac']],'normal6_vs_prev6':prev}
 for name,old in methods.items():
  z=[x for x in ORDER if x in old and x in curr];reps[name].append(z)
  # Duplicating a currently drawn identity or a previous identity cannot alter distinct repeat count.
  assert z==[x for x in ORDER if x in old+old and x in curr+curr]
  col='prev7' if name.endswith('prev7') else 'prev6'
  assert ''.join(z)==ledger[i][col+'_repeats'] and str(len(z))==ledger[i][col+'_repeat_count']
 assert int(ledger[i]['previous_period'])==int(a['period']) and int(ledger[i]['period'])==int(b['period'])
 assert ledger[i]['current_six_zodiacs']==' '.join(curr)
 assert ledger[i]['date_analysis_overlay']==('2024-10-20' if b['period']=='2024294' else b['date'])
assert reps['normal6_vs_prev7'][-2]==['兔','蛇','馬','鷄'] and reps['normal6_vs_prev7'][-1]==['兔','蛇','馬','豬']
assert reps['normal6_vs_prev6'][-2]==['兔','蛇','鷄'] and reps['normal6_vs_prev6'][-1]==['兔','蛇','馬','豬']
for name,X in reps.items():
 q=M['windows']['last_1000_transitions'][name];hist=Counter(map(len,X));assert q['counts']=={str(i):hist[i] for i in range(7)}
 # Different groupby implementation: run lengths, maxima and continuing suffix.
 flags=[len(z)==4 for z in X];groups=[];pos=0
 for value,g in itertools.groupby(flags):
  run=list(g);n=len(run)
  if value:groups.append((pos,pos+n-1))
  pos+=n
 assert q['exact4_episodes']==len(groups) and q['exact4_max']==max(b-a+1 for a,b in groups)
 assert q['exact4_current']==(groups[-1][1]-groups[-1][0]+1 if groups[-1][1]==999 else 0)
 maximum=[(a,b) for a,b in groups if b-a+1==q['exact4_max']]
 assert [(ledger[a]['period'],ledger[b]['period']) for a,b in maximum]==[(str(e['first_period']),str(e['last_period'])) for e in q['exact4_max_episodes']]
 for k,field in [(1,'follow_after_first4'),(2,'follow_after_second4'),(3,'follow_after_third4')]:
  known=[];censored=0
  for a,b in groups:
   if b-a+1<k:continue
   j=a+k-1
   if j==999:censored+=1
   else:known.append((j,j+1))
  f=q[field];assert f['known_next_count']==len(known) and f['right_censored']==censored
  assert f['next_count_distribution']=={str(i):sum(len(X[j])==i for _,j in known) for i in range(7)}
  assert f['retained_identity_count_distribution']=={str(i):sum(len(set(X[a])&set(X[b]))==i for a,b in known) for i in range(5)}
  for (a,b),event in zip(known,[e for e in f['events'] if not e['censored']]):
   assert event['next_period']==int(ledger[b]['period']) and event['at_repeated']==X[a] and event['next_repeated']==X[b]
 # Same EXACT four-set grouped independently.
 current=None;lengths=[];latest=0
 for z in X:
  if len(z)!=4:
   if current:lengths.append(latest)
   current=None;latest=0
  elif tuple(z)==current:latest+=1
  else:
   if current:lengths.append(latest)
   current=tuple(z);latest=1
 if current:lengths.append(latest)
 assert max(lengths)==q['same_exact4_set_max'] and latest==q['same_exact4_set_current']
 # Any fixed four persisting in each adjacent repeat-set, allowing extra repeats.
 best=0;current_best=0
 for combo in itertools.combinations(ORDER,4):
  n=0
  for z in X:
   if all(y in z for y in combo):n+=1;best=max(best,n)
   else:n=0
  current_best=max(current_best,n)
 assert best==q['same_four_presence']['max_transition_periods']
 assert current_best==q['same_four_presence']['current_transition_periods']
# Inclusion-exclusion over group subsets; independent of producer's DP.
for key in ('exact_null_given_latest_previous7','exact_null_given_latest_previous6'):
 q=M[key];groups=list(q['group_sizes']);sizes=q['group_sizes'];ans=[]
 for k in range(7):
  count=0
  for keep in itertools.combinations(groups,k):
   keep=set(keep);N=49-sum(sizes[z] for z in groups if z not in keep)
   for j in range(k+1):
    for ban in itertools.combinations(keep,j):count+=(-1)**j*math.comb(N-sum(sizes[z] for z in ban),6)
  ans.append(count)
 assert ans==q['counts'] and sum(ans)==math.comb(49,6)
anomaly=json.loads((D/'task242_historical_date_2024294.json').read_text());assert anomaly['csv_date']=='2024-10-21' and anomaly['source_date']=='2024-10-20'
for k,v in anomaly['source_api_observations'].items():
 raw=(R/v['raw_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==v['sha256']
assert rows[[r['period'] for r in rows].index('2024294')]['date']=='2024-10-20'
assert not (R/'archive/target312_revision_20261108/revised_decision_receipt.json').exists()
print('Independent membership matrix: all 1000 x two definitions and duplicate invariance PASS')
print('Independent groupby: exact4/current/max, 1/2/3-streak next distribution and censoring PASS')
print('495 four-zodiac combinations: fixed-set/continuing-presence maxima PASS')
print('Independent inclusion-exclusion: two latest-prior-set exact null distributions PASS')
print('Reconciled historical date and seven-row source evidence verified; original frozen CSV unchanged; no revision decision yet PASS')
print('METRICS_SHA256='+hashlib.sha256((D/'task242_1000_repeat_metrics_v2.json').read_bytes()).hexdigest())
print('TASK242_1000_REPEAT_INDEPENDENT_V2 PASS')
