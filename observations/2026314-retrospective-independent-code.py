#!/usr/bin/env python3
"""Independently audit 314 retrospective from frozen page, six-plus-one input and history.
No live result lookup, no new pick, no ranking, no source/fairness authentication.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from math import comb
import csv,hashlib,json,re
R=Path('/home/user');A=R/'archive/task261_314_failure_review';B=A/'before';O=A/'analysis';J=lambda p:json.loads(p.read_text(encoding='utf8'))
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ok(x,s):
 if not x:raise AssertionError(s)
 print('PASS',s)
r=J(O/'retrospective.json');u=J(A/'input/user_314.json');html=(B/'314-published-page.html').read_text(encoding='utf8');payload=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',html).group(1));Z=payload['order'];n2z={int(k):Z[v] for k,v in payload['n2z'].items()};ns=u['normal_numbers'];sp=u['seventh_number'];actual={n2z[n] for n in ns}
ok(ns==[13,26,9,37,34,44] and sp==31 and len(set(ns+[sp]))==7 and u['date'] is None,'exact user seven numbers, order assumption and unknown date')
ok([n2z[n] for n in ns]==u['normal_zodiacs']==['馬','蛇','狗','馬','鷄','豬'] and n2z[sp]==u['seventh_zodiac']=='鼠' and set(u['seven_ball_distinct_zodiacs'])==actual|{'鼠'},'user mappings and seven-ball deduplicated signs independently verified')
raw=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',html).group(1))['2026313'];top=Z[raw['top']];A0,B0,C0,D0=[Z[raw[k]] for k in 'ABCD'];cols=[{top},{A0,B0},{A0,C0,D0}];ok((top,A0,B0,C0,D0)==('牛','虎','馬','狗','鷄') and [len(x&actual) for x in cols]==[0,1,2] and [x<=actual for x in cols]==[False,False,False],'published HTML settles 0/1, 1/2, 2/3; zero complete')
display={Z[raw[k]] for k in ('top','A','B','C','D')};univ={Z[k] for k in raw['U']};reserve=univ-display;s=r['settlement'];ok(sum(n2z[n] in display for n in ns)==s['display_ball_count']==4 and sum(n2z[n] in reserve for n in ns)==s['reserve_ball_count']==1 and sum(n2z[n] in univ for n in ns)==s['universe_ball_count']==5,'four displayed balls, one reserve ball and five universe balls are not completed columns')
ok(reserve=={'豬'} and actual-univ=={'蛇'} and 44 in ns and 26 in ns and 31==sp and '鼠' not in actual,'pig reserve, snake outside, mouse only seventh')
road=[sum(n%3==k for n in ns) for k in range(3)];odd=[sum(n%2 for n in ns),sum(n%2==0 for n in ns)];red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wv=lambda n:'紅' if n in red else '藍' if n in blue else '綠';m=r['actual_structure'];ok(road==m['road_0_1_2']==[1,3,2] and odd==m['odd_even']==[3,3] and [sum(wv(n)==c for n in ns) for c in ('紅','藍','綠')]==m['red_blue_green']==[2,3,1],'actual road, parity and waves from six balls')
ok(m['distinct_zodiac_count']==5 and sorted(Counter(n2z[n] for n in ns).values(),reverse=True)==[2,1,1,1,1] and sum(ns)==163 and max(ns)-min(ns)==35 and m['heads_0_to_4']==[1,1,1,2,1] and m['small_big_1_24_25_49']==[2,4],'five signs, one pair, sum/span and head/small-big metrics')
ok([n for n in ns if n%3==2 and n%2==0]==[26,44] and not [n for n in ns if n%3==2 and n%2] and [n for n in ns if n%3==0]==[9],'all 2-road normals are even; only zero-road is 09 dog')
ok(len({n2z[n] for n in ns})==5 and not {'牛','狗'}<=actual and '虎' not in actual,'five distinct signs is necessary but not sufficient; two zero-road zodiac slots cannot both complete')
rows=sorted(C(B/'history-through-313.csv'),key=lambda x:int(x['period']));assert len(rows)==1044 and rows[-1]['period']=='2026313' and rows[-1]['date']==''
prev=rows[-1];six={prev[f'z{i}'] for i in range(1,7)};seven=six|{prev['special_zodiac']};current=actual|{n2z[sp]};x=r['previous_input_identity'];ok(actual&seven==actual&six=={'狗','豬'} and current&seven=={'狗','豬','鼠'} and set(ns+[sp]).isdisjoint({int(prev[f'n{i}']) for i in range(1,7)}|{int(prev['special'])}),'seven-v-seven 3 signs versus six-v-seven 2 signs; no repeated numbers')
# Recompute all 12 zodiac windows and non-overlapping blocks directly from prior records.
e=J(B/'314-evidence-before-draw.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44));rev=rows[::-1];numbers=lambda row:[int(row[f'n{i}']) for i in range(1,7)]
for z in Z:
 a=e['per_zodiac'][z];group={n for n in range(1,50) if n2z[n]==z};assert a['numbers']==sorted(group)
 for w in W:
  rs=rows[-w:];assert a['windows'][str(w)]=={'balls':sum(sum(n in group for n in numbers(row)) for row in rs),'periods':sum(bool(set(numbers(row))&group) for row in rs)}
 for f,l in blocks:
  rs=rev[f:l+1];assert a['disjoint_age_blocks'][f'{f}-{l}']=={'balls':sum(sum(n in group for n in numbers(row)) for row in rs),'periods':sum(bool(set(numbers(row))&group) for row in rs)}
ok(True,'all 12 zodiac 8-window and disjoint age-block values recomputed directly')
for n in range(1,50):
 a=e['per_number'][str(n)];assert a['zodiac']==n2z[n] and a['road']==n%3 and a['odd_even']==('奇' if n%2 else '偶') and a['wave']==wv(n) and a['head']==n//10 and a['tail']==n%10 and a['last_normal_age']==next(i for i,row in enumerate(rev) if n in numbers(row))
 for w in W:assert a['window_counts'][str(w)]==sum(n in numbers(row) for row in rows[-w:])
ok(True,'all 49 numbers: prior counts/ages, zodiac, road, wave, parity, head and tail')
for x in r['each_actual_normal_ball_prior']:
 n=x['number'];p=e['per_number'][str(n)];assert x['windows_before_314']==p['window_counts'] and x['last_normal_age_before_314']==p['last_normal_age']
ok(True,'six actual balls retain pre-314 rather than post-result ages and counts')
for w in W:
 rr=[numbers(row) for row in rows[-w:]];shape=r['pre_period_shape_windows'][str(w)];zt=lambda x:{n2z[n] for n in x}
 assert shape['exact_road_1_3_2']==sum([sum(n%3==k for n in x) for k in range(3)]==[1,3,2] for x in rr)
 assert shape['road0_exact_1']==sum(sum(n%3==0 for n in x)==1 for x in rr) and shape['road0_at_most_1']==sum(sum(n%3==0 for n in x)<=1 for x in rr)
 assert shape['no_odd_2road']==sum(not any(n%3==2 and n%2 for n in x) for x in rr)
 assert shape['two_even_2road_no_odd_2road']==sum(sum(n%3==2 and n%2==0 for n in x)==2 and not any(n%3==2 and n%2 for n in x) for x in rr)
 assert shape['distinct_exactly_5']==sum(len(zt(x))==5 for x in rr) and shape['pattern_2_1_1_1_1']==sum(sorted(Counter(n2z[n] for n in x).values(),reverse=True)==[2,1,1,1,1] for x in rr)
 assert shape['horse_at_least_two_balls']==sum(sum(n2z[n]=='馬' for n in x)>=2 for x in rr) and shape['both_snake_and_pig']==sum({'蛇','豬'}<=zt(x) for x in rr)
ok(True,'all prior route/risk shape counts directly recomputed; overlapping windows not independent')
raws=J(B/'314-31-handwritten-designs.json')['candidates'];out=r['frozen_31_candidate_review'];seen=defaultdict(list);freq=Counter();dist=Counter()
for p,q in zip(raws,out['original_order_candidates']):
 role=p['roles'];sets=[{role['top']},{role['A'],role['B']},{role['A'],role['C'],role['D']}];present=[len(s&actual) for s in sets];complete=[s<=actual for s in sets];assert p['id']==q['id'] and p['roles']==q['roles'] and p['reserves']==q['reserves'] and [x['present_count'] for x in q['slots']]==present and [x['complete'] for x in q['slots']]==complete
 key=(role['top'],frozenset(sets[1]),frozenset(sets[2]));seen[key].append(p['id']);freq[role['A']]+=1;dist[sum(complete)]+=1
ok(len(raws)==31 and len(seen)==30 and [[x[:3] for x in v] for v in seen.values() if len(v)>1]==[['E01','E09']],'31 original candidates have 30 unordered actual column structures; reserve-only duplicate identified')
ok(freq['虎']==16 and set(freq)==set(Z) and dist=={0:22,1:7,2:2},'shared-position concentration and all 31 after-result outcomes independently counted, not ranked')
lookup={x['id'][:3]:x for x in out['original_order_candidates']};ok([lookup[k]['complete_count'] for k in ('E01','E09','E10','E11','E24')]==[0,0,2,2,0] and [x['present_count'] for x in lookup['E10']['slots']]==[0,2,3] and [x['present_count'] for x in lookup['E11']['slots']]==[0,2,3],'frozen E10/E11 alternatives, reserve-only E09 and E24 do not get conflated')
ok(len(out['top_overlap_cases'])==1 and out['top_overlap_cases'][0].startswith('E22'),'candidate overlap architecture measured, not imposed as new rule')
# Independent inclusion-exclusion of mandatory zodiac groups plus inclusion-
# exclusion over the three column events (different from direct enumeration).
group={z:{n for n,v in n2z.items() if v==z} for z in Z};den=comb(49,6)
def count(groups):
 gs=sorted(set(groups));return sum((-1)**k*sum(comb(49-sum(len(group[z]) for z in subset),6) for subset in combinations(gs,k)) for k in range(len(gs)+1))
sc,dc,tc=[count(c) for c in cols];spair=count(cols[0]|cols[1]);strip=count(cols[0]|cols[2]);dtrip=count(cols[1]|cols[2]);all3=count(cols[0]|cols[1]|cols[2]);none=den-sc-dc-tc+spair+strip+dtrip-all3;i=r['ideal_model_only'];ok(abs(i['complete_column_count_percent'][0]-100*none/den)<1e-9 and all(abs(i['single_double_triple_percent'][k]-100*x/den)<1e-9 for k,x in enumerate([sc,dc,tc])) and abs(i['double_and_triple_joint_percent']-100*dtrip/den)<1e-9 and abs(i['both_tiger_and_cow_absent_percent']-100*comb(41,6)/den)<1e-9,'ideal-model zero-column and shared-slot dependence independently calculated by inclusion-exclusion')
# Historical context is source-limited and uses seven distinct identities, no cross-gap bridging.
old=C(R/'data/task260_314_release/observations/2026314-445-source-through-311.csv');sets=[set(x['zodiacs'].split()) if x['usable']=='1' else None for x in old]+[set([rows[-2][f'z{k}'] for k in range(1,7)]+[rows[-2]['special_zodiac']]),seven,current];ts=[None]+[len(a&b) if a is not None and b is not None else None for a,b in zip(sets,sets[1:])];inds=[j for j in range(3,len(sets)) if ts[j-2:j+1]==[4,4,5]];bad=sum(None in ts[j-2:j+1] for j in range(3,len(sets)));follow=Counter(ts[j+1] for j in inds if j+1<len(ts));hist=J(O/'repeat_445.json');ok(len(sets)==2495 and bad==8 and len(inds)==9 and follow=={2:2,3:3,4:3,5:1} and ts[-6:]==[4,4,5,5,3,3] and hist['valid_candidate_windows']==2484,'exact 4/4/5 seven-v-seven record and 314 extension reproduced independently')
ok([x['complete_count'] for x in r['earlier_versions']]==[0,1,1,2,0,1,0] and r['earlier_versions'][1]['progress']==['0/1','2/2','1/3'],'308–314 per-period records and 309 correct columns')
for line in (A/'before.sha256').read_text(encoding='utf8').splitlines():
 dig,name=line.split('  ',1);assert hashlib.sha256((B/name).read_bytes()).hexdigest()==dig
ok(True,'all 24 before-review frozen files preserve their hashes')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();manual=J(R/'data/manual_site_decisions.json');ok(sha(R/'data/macau_mark_six_full.csv')==sha(B/'history-through-313.csv') and sha(R/'zodiac_trend.html')==sha(B/'314-published-page.html') and sha(R/'www/zodiac_trend.html')==sha(B/'314-published-www-page.html') and sha(R/'data/manual_site_decisions.json')==sha(B/'manual-site-decisions.json') and '2026315' not in manual['decisions'],'main history and public-site source still through 313/314; no 315 selection')
print('INDEPENDENT 314 RETROSPECTIVE QC PASS — not an official draw, pre-registration, real-mechanism or prediction certificate')
