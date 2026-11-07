#!/usr/bin/env python3
"""Analyze 1,000 consecutive transitions of distinct normal-ball zodiac identities.

Primary: unique current SIX normal-ball zodiac identities intersect unique
previous SEVEN-ball identities; the previous special's identity is only a label.
Sensitivity: both current and previous SIX normal balls. No current special
analysis, special-number prediction or special A/S/B/C lines.
Actual continuation counts are retrospective descriptions, not a predictor.
"""
from pathlib import Path
from datetime import date,datetime,timezone,timedelta
from collections import Counter
import csv,hashlib,json,math
R=Path('/home/user');D=R/'data';J=D/'task242_1000_repeat_metrics_v2.json';T=D/'task242_1000_repeat_ledger_v2.txt';C=D/'task242_1000_repeat_transitions_v2.csv'
assert not any(p.exists() for p in (J,T,C))
ORDER=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sortz=lambda q:sorted(q,key=ORDER.index)
source=D/'task242_1042_reconciled_history.csv';assert hashlib.md5(source.read_bytes()).hexdigest()=='f91c57bb50f3c4c36965274eb5f66b11'
assert 'TASK242_HISTORY_RECONCILIATION_INDEPENDENT PASS' in (D/'task242_history_reconciliation_independent_test_retry.txt').read_text()
raw=sorted(csv.DictReader(source.open(encoding='utf-8-sig')),key=lambda r:int(r['period']))
assert len(raw)==1042 and int(raw[0]['period'])==2024001 and int(raw[-1]['period'])==2026311
assert len({r['period'] for r in raw})==len(raw)
anomaly=json.loads((D/'task242_historical_date_2024294.json').read_text());assert anomaly['result']=='HISTORICAL_DATE_ANOMALY_CAPTURE PASS'
assert anomaly['period']==2024294 and anomaly['csv_date']=='2024-10-21' and anomaly['source_date']=='2024-10-20'
prev_date=None;previous_period=None;boundaries=[];old_offset=None
for r in raw:
 p=int(r['period']);d=date.fromisoformat(anomaly['source_date'] if p==2024294 else r['date'])
 if prev_date:
  assert (d-prev_date).days==1,(p,prev_date,d)
  expect=previous_period+1 if previous_period//1000==p//1000 else (p//1000)*1000+1
  assert p==expect,(previous_period,p,expect)
 assert p==d.year*1000+int(d.strftime('%j')),(p,d)
 nums=[int(r[f'n{i}']) for i in range(1,7)]+[int(r['special'])];z=[r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']]
 assert len(set(nums))==7 and all(1<=n<=49 for n in nums) and set(z)<=set(ORDER)
 offsets={(n+ORDER.index(zz))%12 for n,zz in zip(nums,z)};assert len(offsets)==1,(p,offsets)
 off=offsets.pop()
 if off!=old_offset:boundaries.append({'period':p,'date':str(d),'offset':off});old_offset=off
 prev_date=d;previous_period=p
assert boundaries==[{'period':2024001,'date':'2024-01-01','offset':4},{'period':2024041,'date':'2024-02-10','offset':5},{'period':2025029,'date':'2025-01-29','offset':6},{'period':2026048,'date':'2026-02-17','offset':7}]
def n6(r):return {r[f'z{i}'] for i in range(1,7)}
def n7(r):return n6(r)|{r['special_zodiac']}
def corrected_date(r):return anomaly['source_date'] if int(r['period'])==2024294 else r['date']
trans=[]
for a,b in zip(raw,raw[1:]):
 curr=n6(b);p6=n6(a);p7=n7(a)
 trans.append({'previous_period':int(a['period']),'period':int(b['period']),'date':corrected_date(b),
  'current_six_numbers':[int(b[f'n{i}']) for i in range(1,7)],
  'current_six_draw_zodiacs':[b[f'z{i}'] for i in range(1,7)],
  'previous_six_identities':sortz(p6),'previous_seven_identities':sortz(p7),'current_six_identities':sortz(curr),
  'prev7_repeats':sortz(curr&p7),'prev6_repeats':sortz(curr&p6)})
assert len(trans)==1041 and trans[-1]['prev7_repeats']==['兔','蛇','馬','豬'] and trans[-1]['prev6_repeats']==['兔','蛇','馬','豬']

def make_runs(seq,key,pred):
 result=[];s=None
 for i,x in enumerate(seq):
  if pred(len(x[key])):
   if s is None:s=i
  elif s is not None:result.append((s,i-1));s=None
 if s is not None:result.append((s,len(seq)-1))
 return result
def episode(seq,key,s,e):
 return {'first_period':seq[s]['period'],'last_period':seq[e]['period'],'periods':e-s+1,
  'base_previous_period':seq[s]['previous_period'],'ongoing_at_cutoff':e==len(seq)-1,
  'identities_each_period':[{'period':x['period'],'repeated':x[key]} for x in seq[s:e+1]]}
def same_set_runs(seq,key):
 out=[];s=None;last=None
 for i,x in enumerate(seq):
  k=tuple(x[key]) if len(x[key])==4 else None
  if k is None:
   if s is not None:out.append((s,i-1));s=None
  elif s is None:s=i
  elif k!=last:out.append((s,i-1));s=i
  last=k
 if s is not None:out.append((s,len(seq)-1))
 return out

def following(seq,key,runs,k,prior_same_exact):
 events=[];excluded_left=0
 for s,e in runs:
  if s==0 and prior_same_exact:excluded_left+=1;continue
  if e-s+1<k:continue
  at=s+k-1;x=seq[at]
  if at+1==len(seq):
   events.append({'start_period':seq[s]['period'],'reached_period':x['period'],'next_period':None,'censored':True});continue
  y=seq[at+1];same=sortz(set(x[key])&set(y[key]))
  events.append({'start_period':seq[s]['period'],'reached_period':x['period'],'next_period':y['period'],
   'at_repeated':x[key],'next_repeat_count':len(y[key]),'next_repeated':y[key],
   'same_identities_retained':same,'censored':False})
 known=[x for x in events if not x['censored']]
 return {'reach_streak':k,'episodes_reached':len(events),'known_next_count':len(known),'right_censored':len(events)-len(known),
  'left_boundary_runs_excluded':excluded_left,
  'next_count_distribution':{str(i):sum(e['next_repeat_count']==i for e in known) for i in range(7)},
  'next_exact4_count':sum(e['next_repeat_count']==4 for e in known),
  'retained_identity_count_distribution':{str(i):sum(len(e['same_identities_retained'])==i for e in known) for i in range(5)},
  'events':events,
  'note':'one next observation when each distinct exact-four episode first reaches this length; right-censored current episode has no next outcome; descriptive only'}

def same_four_presence(seq,prev_key):
 # At least four SAME identities occur in base previous scope and every current
 # SIX-normal identity set across consecutive periods; extra identities allowed.
 best=0;episodes=[];current_best=0;current=[]
 for i in range(len(seq)):
  common=set(seq[i][prev_key]);j=i
  while j<len(seq):
   common&=set(seq[j]['current_six_identities'])
   if len(common)<4:break
   length=j-i+1
   rec={'first_current_period':seq[i]['period'],'last_period':seq[j]['period'],
        'base_previous_period':seq[i]['previous_period'],'transition_periods':length,
        'draws_including_base':length+1,'common_identities':sortz(common)}
   if length>best:best=length;episodes=[rec]
   elif length==best:episodes.append(rec)
   if j==len(seq)-1:
    if length>current_best:current_best=length;current=[rec]
    elif length==current_best:current.append(rec)
   j+=1
 return {'max_transition_periods':best,'max_draws_including_base':best+1 if best else 0,
  'max_episodes':episodes,'current_transition_periods':current_best,'current_episodes':current,
  'note':'Same four-or-more identities present in every period, base previous scope plus subsequent normal six; other identities may be present, so not necessarily exactly four repeats each period.'}

def summarize(seq,key,prev_key,preceding=None):
 counts=Counter(len(x[key]) for x in seq);runs=make_runs(seq,key,lambda x:x==4);atleast=make_runs(seq,key,lambda x:x>=4)
 mx=max((e-s+1 for s,e in runs),default=0);cur=(runs[-1][1]-runs[-1][0]+1) if runs and runs[-1][1]==len(seq)-1 else 0
 am=max((e-s+1 for s,e in atleast),default=0);ac=(atleast[-1][1]-atleast[-1][0]+1) if atleast and atleast[-1][1]==len(seq)-1 else 0
 same=same_set_runs(seq,key);sm=max((e-s+1 for s,e in same),default=0);sc=(same[-1][1]-same[-1][0]+1) if same and same[-1][1]==len(seq)-1 else 0
 prior=bool(preceding and len(preceding[key])==4)
 return {'pairs':len(seq),'first_previous_period':seq[0]['previous_period'],'first_current_period':seq[0]['period'],'last_period':seq[-1]['period'],
  'counts':{str(i):counts[i] for i in range(7)},'exact4_episodes':len(runs),
  'exact4_episode_lengths':dict(sorted(Counter(e-s+1 for s,e in runs).items())),
  'exact4_current':cur,'exact4_current_episode':episode(seq,key,*runs[-1]) if cur else None,
  'exact4_max':mx,'exact4_max_episodes':[episode(seq,key,s,e) for s,e in runs if e-s+1==mx],
  'exact4_left_censored':bool(runs and runs[0][0]==0 and prior),'exact4_right_censored':bool(cur),
  'atleast4_current':ac,'atleast4_max':am,'atleast4_max_episodes':[episode(seq,key,s,e) for s,e in atleast if e-s+1==am],
  'same_exact4_set_current':sc,'same_exact4_set_max':sm,'same_exact4_set_max_episodes':[episode(seq,key,s,e) for s,e in same if e-s+1==sm],
  'same_four_presence':same_four_presence(seq,prev_key),
  'follow_after_first4':following(seq,key,runs,1,prior),
  'follow_after_second4':following(seq,key,runs,2,prior),
  'follow_after_third4':following(seq,key,runs,3,prior)}

def exact_null(prev_identities):
 groups=[5 if z=='馬' else 4 for z in prev_identities];rest=49-sum(groups);dp={(0,0):1}
 for m in groups:
  nxt=Counter()
  for (k,n),v in dp.items():
   nxt[(k,n)]+=v
   for b in range(1,min(m,6-n)+1):nxt[(k+1,n+b)]+=v*math.comb(m,b)
  dp=nxt
 counts=[sum(v*math.comb(rest,6-n) for (k2,n),v in dp.items() if k2==k and 0<=6-n<=rest) for k in range(7)]
 den=math.comb(49,6);assert sum(counts)==den
 return {'previous_identities':sortz(prev_identities),'group_sizes':dict(zip(sortz(prev_identities),[5 if z=='馬' else 4 for z in sortz(prev_identities)])),
  'outside_number_count':rest,'denominator':den,'counts':counts,'probabilities':[x/den for x in counts],
  'note':'Conditional on the known previous identity set under uniform six-of-49, not a prediction or estimate from the prior run.'}

windows={}
for name,n in [('last_1000_transitions',1000),('last_1000_draws_internal',999),('all_available_transitions',1041)]:
 seq=trans[-n:];prior=trans[-n-1] if len(trans)>n else None
 windows[name]={'normal6_vs_prev7':summarize(seq,'prev7_repeats','previous_seven_identities',prior),
                'normal6_vs_prev6':summarize(seq,'prev6_repeats','previous_six_identities',prior)}
res={'target':2026312,'created_cst':datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'),
 'data_last_period':2026311,'csv_row_count':len(raw),'csv_md5':hashlib.md5(source.read_bytes()).hexdigest(),
 'definitions':{'primary':'unique current six normal zodiac identities ∩ unique previous seven identities; previous special is identity label only',
  'sensitivity':'unique current six normal identities ∩ unique previous six normal identities',
  'four':'exactly four distinct repeated identities unless explicitly marked at least four',
  'consecutive':'consecutive ISSUE comparisons, dates shown after analysis-only documented anomaly overlay',
  'current_special':'never used in the current side of any comparison and never used to make a special prediction'},
 'source_reconciliation_path':'data/task242_historical_source_reconciliation.json','date_anomaly_path':'data/task242_historical_date_2024294.json','date_anomaly_overlay':{'2024294':anomaly['source_date']},
 'mapping_boundaries':boundaries,'windows':windows,
 'latest_transition':trans[-1],
 'exact_null_given_latest_previous7':exact_null(n7(raw[-1])),
 'exact_null_given_latest_previous6':exact_null(n6(raw[-1])),
 'limitations':['Source is one 1,042-row historical dataset; history describes observations, not independent draws or evidence of predictability.',
  'Long-run and follow-on episodes are not independent at adjacent positions; right-censored episodes have no known next outcome.',
  'Past maximum streak is descriptive, not a cap; no inference that a streak must end or continue.',
  'How many prior identities are selected in a six-zodiac candidate is not the number of previous identities actually drawn.',
  'Uses the fully reconciled analysis copy, not the immutable original CSV; seven issue corrections and conflicting sources are disclosed in reconciliation record.']}
seq=trans[-1000:]
with C.open('x',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['previous_period','period','date_analysis_overlay','current_six_numbers','current_six_zodiacs','previous_six_identities','previous_seven_identities','current_six_identities','prev7_repeats','prev7_repeat_count','prev6_repeats','prev6_repeat_count'])
 for x in seq:w.writerow([x['previous_period'],x['period'],x['date'],' '.join(map(str,x['current_six_numbers'])),' '.join(x['current_six_draw_zodiacs']),''.join(x['previous_six_identities']),''.join(x['previous_seven_identities']),''.join(x['current_six_identities']),''.join(x['prev7_repeats']),len(x['prev7_repeats']),''.join(x['prev6_repeats']),len(x['prev6_repeats'])])
res['transition_ledger_path']=str(C.relative_to(R));res['transition_ledger_sha256']=hashlib.sha256(C.read_bytes()).hexdigest()
with J.open('x',encoding='utf-8') as f:json.dump(res,f,ensure_ascii=False,indent=2);f.write('\n')
lines=['TASK242 THOUSAND-TRANSITION DISTINCT REPEAT-ZODIAC REVIEW',
 'Primary current SIX normal ∩ previous SEVEN identities; sensitivity both SIX. No special A/S/B/C.',
 f"Source 1042 rows last311 from reconciled copy MD5={res['csv_md5']}; seven corrected issue rows documented, original CSV unchanged.",
 'One thousand transition comparisons use 1,001 draws: base 2024042, current periods 2024043..2026311.',
 'Four = EXACT distinct 4 unless specifically noted; number-identity and current-special duplicates do not add count.',
 '']
for wn,methods in windows.items():
 lines.append('## '+wn)
 for name,v in methods.items():
  lines.append(name+f" pairs={v['pairs']} distribution={v['counts']} exact4_current={v['exact4_current']} max={v['exact4_max']} atLeast4_current/max={v['atleast4_current']}/{v['atleast4_max']}")
  lines.append(f"  SAME EXACT REPEAT SET current/max={v['same_exact4_set_current']}/{v['same_exact4_set_max']} SAME FOUR PRESENCE current/max={v['same_four_presence']['current_transition_periods']}/{v['same_four_presence']['max_transition_periods']}")
  lines.append('  exact4 max episodes='+json.dumps(v['exact4_max_episodes'],ensure_ascii=False))
  f=v['follow_after_second4'];lines.append(f"  AFTER FIRST REACH 2: reached={f['episodes_reached']} next_known={f['known_next_count']} censored={f['right_censored']} next_distribution={f['next_count_distribution']} same_identity_retention={f['retained_identity_count_distribution']}")
  for ev in f['events']:
   lines.append('    '+json.dumps(ev,ensure_ascii=False))
  for k in (1,3):
   f=v['follow_after_first4' if k==1 else 'follow_after_third4'];lines.append(f"  AFTER FIRST REACH {k}: next_known={f['known_next_count']} censored={f['right_censored']} next_distribution={f['next_count_distribution']}")
 lines.append('')
for k in ('exact_null_given_latest_previous7','exact_null_given_latest_previous6'):
 v=res[k];lines.append(k+' previous='+''.join(v['previous_identities'])+' count0..6='+str(v['counts'])+' probabilities='+str([round(x*100,4) for x in v['probabilities']]))
lines+=['','No predictive claim, no fixed repeat quota and no special-line selection. TASK242_1000_REPEAT_ANALYSIS_V2 PASS']
with T.open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
print('\n'.join(lines))
