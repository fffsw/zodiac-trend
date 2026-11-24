#!/usr/bin/env python3
"""Independent 12/49/66 328 evidence check; previous 327 is user-only, no 328 values looked up."""
from pathlib import Path
from itertools import combinations
import csv,hashlib,json,re,subprocess,sys
R=Path('/home/user');target=int(sys.argv[1]);assert target==2026328;A=R/'archive/task295_328_release';S=A/'stage';O=A/'analysis';T=R/'archive/task294_327_review';B=T/'before';J=lambda p:json.loads(p.read_text(encoding='utf8'));h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ok(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
oldpath=B/'history-through-326.csv';old=oldpath.read_bytes().splitlines(keepends=True);new=(S/'data/macau_mark_six_full.csv').read_bytes().splitlines(keepends=True);ok(len(old)==1049+(target-2026319) and len(new)==len(old)+1 and new[0]==old[0] and new[2:]==old[1:] and all(x.endswith(b'\r\n') for x in new),'each stage adds exactly one user row and preserves all older CRLF bytes')
rows=C(S/'data/macau_mark_six_full.csv');N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];u=J(R/'archive/task294_327_review/input/user-327.json');ok(len(rows)==1049+(target-2026319) and int(rows[0]['period'])==target-1 and all(rows[i]['date']=='' for i in range(6+(target-2026319))) and N(rows[0])+[int(rows[0]['special'])]==u['normal_numbers']+[u['seventh_number']] and len(set(N(rows[0])+[int(rows[0]['special'])]))==7,'exact previous user six-plus-one, unknown dates, no target row')
html=(B/'327-current-homepage.html').read_text();payload=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',html).group(1));Z=payload['order'];n2z={int(n):Z[i] for n,i in payload['n2z'].items()};G={z:[n for n in range(1,50) if n2z[n]==z] for z in Z};ok([n2z[n] for n in N(rows[0])]==u['normal_zodiacs'] and n2z[int(rows[0]['special'])]==u['seventh_zodiac'],'all prior issue numbers match frozen page mapping; seventh excluded from normal counts')
e=J(O/'evidence.json');W=[10,20,35,40,45,60,100,250];blocks=[(0,9),(10,19),(20,34),(35,39),(40,44)];ok(e['history_rows']==len(rows) and e['latest_period']==target-1 and e['latest_date'] is None and e['history_sha256']==h(S/'data/macau_mark_six_full.csv') and e['windows_overlap_not_independent_votes'] and e['target_result_was_already_provided'] is False,'prior issue scope, overlapping windows and no 328 target in staged data recorded')
for z in Z:
 v=e['per_zodiac'][z];gs=set(G[z]);assert v['numbers']==G[z] and v['last_normal_age']==next(i for i,r in enumerate(rows) if gs.intersection(N(r))) and 'previous_seven_identity' not in v
 for w in W:
  a=[N(r) for r in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(sum(n in gs for n in x) for x in a),'periods':sum(any(n in gs for n in x) for x in a)}
 for lo,hi in blocks:
  a=[N(r) for r in rows[lo:hi+1]];assert v['disjoint_age_blocks'][f'{lo}-{hi}']=={'balls':sum(sum(n in gs for n in x) for x in a),'periods':sum(any(n in gs for n in x) for x in a)}
ok(True,'all 12 signs, eight normal windows and five disjoint age blocks independently recounted')
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠';ledger=C(O/'number_ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for n in range(1,50):
 v=e['per_number'][str(n)];assert (v['zodiac'],v['road'],v['odd_even'],v['wave'],v['head'],v['tail'])==(n2z[n],n%3,'奇' if n%2 else '偶',wave(n),n//10,n%10) and v['last_normal_age']==next(i for i,r in enumerate(rows) if n in N(r))
 for w in W:assert v['window_counts'][str(w)]==sum(n in N(r) for r in rows[:w])
ok(True,'all 49 numbers: eight normal windows and full fixed attributes independently recounted')
pairkey=lambda a,b:'|'.join(sorted((a,b),key=Z.index));zset=lambda row:{n2z[n] for n in N(row)}
for w in W:
 rs=rows[:w];balls=[n for row in rs for n in N(row)];v=e['structural_windows'][str(w)];assert v['road_ball_counts']==[sum(n%3==k for n in balls) for k in range(3)] and v['odd_even_ball_counts']==[sum(n%2 for n in balls),sum(n%2==0 for n in balls)] and v['red_blue_green_ball_counts']==[sum(wave(n)==c for n in balls) for c in ('紅','藍','綠')] and v['head_ball_counts']==[sum(n//10==k for n in balls) for k in range(5)] and v['tail_ball_counts']==[sum(n%10==k for n in balls) for k in range(10)]
 for k in range(3):
  assert v[f'no_{k}road_periods']==sum(not any(n%3==k for n in N(row)) for row in rs)
  for par in ('odd','even'):assert v[f'no_{par}_{k}road_periods']==sum(not any(n%3==k and n%2==(par=='odd') for n in N(row)) for row in rs)
 for a,b in combinations(Z,2):assert e['joint_zodiac_absence_periods'][str(w)][pairkey(a,b)]==sum(not {a,b}&zset(row) for row in rs)
 for z in Z:
  p=e['same_route_parity_peer_present_target_absent_periods'][str(w)][z];other=p['peer'];assert other!=z and G[other][0]%6==G[z][0]%6 and p['target_absent_peer_present_periods']==sum(z not in zset(row) and other in zset(row) for row in rs)
ok(True,'all 66 sign-pair absences and same-route-parity replacements independently recounted per window')
L=C(O/'joint_absence_ledger.csv');ok(len(L)==66 and all(int(x[f'W{w}_both_absent'])==e['joint_zodiac_absence_periods'][str(w)][pairkey(x['sign_one'],x['sign_two'])] for x in L for w in (35,40,45)),'66-row CSV matches computed evidence; no scores or ranking')
seven=lambda row:set([row[f'z{i}'] for i in range(1,7)]+[row['special_zodiac']]);by={int(r['period']):r for r in rows};x=[len(seven(by[p])&seven(by[p-1])) for p in range(2026309,target)];ok(all(e['adjacent_identity_repeats'][str(p)]['seven_v_seven_count']==v for p,v in zip(range(2026309,target),x)) and x[-1]==4,'seven-ball identity counts separately reproduced, never used as normal-ball choices')
changed=[dict(r) for r in rows];changed[0]['special']='01';changed[0]['special_zodiac']='馬';ok(all(N(a)==N(b) and zset(a)==zset(b) for a,b in zip(rows,changed)) and all(sum(not {a,b}&zset(row) for row in changed[:45])==e['joint_zodiac_absence_periods']['45'][pairkey(a,b)] for a,b in combinations(Z,2)),'altering seventh leaves every first-six row and W45 joint-absence count unchanged')
assert h(R/'data/macau_mark_six_full.csv')==h(B/'history-through-326.csv') and h(R/'zodiac_trend.html')==h(B/'327-current-homepage.html') and h(R/'data/manual_site_decisions.json')==h(B/'manual-decisions-through-327.json');ok(subprocess.check_output(['git','status','--porcelain','-uall'],cwd=R/'deploy',text=True)==(T/'analysis/original_dirty_deploy_status_before.txt').read_text(),'main files and original 68-item dirty deploy unchanged during isolation')
out={'status':'PASS','scope':f'descriptive prior-only evidence for {target}; history through 327 only; no 328 result looked up; no source/timing/mechanism authentication','checks':checks,'evidence_sha256':h(O/'evidence.json'),'joint_ledger_sha256':h(O/'joint_absence_ledger.csv')};p=O/'evidence_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
