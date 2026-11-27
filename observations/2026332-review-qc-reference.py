#!/usr/bin/env python3
"""Independent settlement, provenance, cohorts and evidence audit through user 331."""
from pathlib import Path
from collections import Counter
from datetime import date
from itertools import combinations
import csv,hashlib,json,re,subprocess
R=Path('/home/user');A=R/'archive/task305_331_review_332';B=A/'before';S=A/'stage';Q=A/'analysis';I=A/'input';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True);ck(len(list(B.iterdir()))==39,'39 frozen inputs verify')
old=(B/'history-through-330.csv').read_bytes().splitlines(keepends=True);new=(S/'data/macau_mark_six_full.csv').read_bytes().splitlines(keepends=True);ck(len(old)==1062 and len(new)==1063 and new[0]==old[0] and new[2:]==old[1:] and all(x.endswith(b'\r\n') for x in new),'one user-confirmed 331 row added, 1061 prior rows byte-identical')
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['period']))
by={int(r['period']):r for r in rows};r=by[2026331];ns=[int(r[f'n{i}']) for i in range(1,7)];zs=[r[f'z{i}'] for i in range(1,7)];u=J(I/'user-331-confirmed.json');ck(len(rows)==1062 and max(by)==2026331 and ns==[27,18,3,47,16,14] and zs==['龍','牛','龍','猴','兔','蛇'] and int(r['special'])==13 and r['special_zodiac']=='馬' and u['user_ball_partition_explicitly_confirmed'] and not r['date'],'331 normals and seventh explicitly confirmed by user; date blank, no 332 outcome')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];ck(all([sign(int(x[f'n{i}'])) for i in range(1,7)]==[x[f'z{i}'] for i in range(1,7)] and sign(int(x['special']))==x['special_zodiac'] for x in rows[-250:]),'all recent 250 observed numbers agree with current sign mapping assumption')
page=(B/'331-revised-homepage.html').read_text();mapping=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));data=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));ck(mapping['2026330']=={'U':[6,10,1,3,5,2],'top':6,'A':10,'B':1,'C':3,'D':5,'top_overlap_mode':'coverage'} and data['rows'][-1][0]==2026330 and H(B/'331-revised-homepage.html')==J(B/'331-revision-release-receipt.json')['page_sha256'],'331 revised actual display independently recovered from frozen public page, not original draft')
rev=J(Q/'retrospective.json');prev=J(B/'331-initial-retrospective.json');records=rev['historical_outcomes'];ck(len(records)==38 and records[:-1]==prev['historical_outcomes'] and [x['period'] for x in records]==[i for i in range(2026291,2026332) if i not in (2026319,2026322,2026324)] and rev['unpublished_reconstructions']==prev['unpublished_reconstructions'],'38 retained records and three separately marked reconstructions')
with (Q/'historical_display_outcomes.csv').open(encoding='utf8',newline='') as f:tab=list(csv.DictReader(f))
ck(len(tab)==len(records),'38-row exported retrospective CSV')
for x,t in zip(records,tab):
 row=by[x['period']];numbers=[int(row[f'n{i}']) for i in range(1,7)];signs=[row[f'z{i}'] for i in range(1,7)];got=set(signs);rr=x['roles'];needs=[[rr['top']],[rr['A'],rr['B']],[rr['A'],rr['C'],rr['D']]]
 ck(x['normal_numbers']==numbers and x['normal_zodiacs']==signs and x['special_number']==int(row['special']) and x['special_zodiac']==row['special_zodiac'] and int(t['period'])==x['period'],f"{x['period']} user/history balls and CSV")
 for label,sl,need in zip(('single','pair','triple'),x['slots'],needs):
  present=[z for z in need if z in got];missing=[z for z in need if z not in got];balls=[{'number':n,'zodiac':z} for n,z in zip(numbers,signs) if z in need]
  ck(sl['required']==need and sl['present']==present and sl['missing']==missing and sl['balls']==balls and sl['present_count']==len(present) and sl['needed_count']==len(need) and sl['complete']==(not missing) and t[label+'_present'].split()==present and t[label+'_missing'].split()==missing and t[label+'_hits']==f'{len(present)}/{len(need)}',f"{x['period']} {label} complete/present/missing and exact normal balls")
 ck(x['complete_columns']==sum(set(v)<=got for v in needs)==int(t['complete_columns']) and x['shared_missing']==(rr['A'] not in got),f"{x['period']} complete columns and shared identity")
 if x['universe_zodiacs'] is None:ck(x['reserve_hits'] is None and x['outside_universe_hits'] is None,f"{x['period']} unknown universe not classified as no reserve")
 else:
  univ=set(x['universe_zodiacs']);display=set(rr.values());ck(set(x['reserve_hits'])==(univ-display)&got and set(x['outside_universe_hits'])==got-univ and not (univ-display)&display,f"{x['period']} explicit universe reserve/non-universe identities")
x=records[-1];ck(x['roles']=={'top':'馬','A':'狗','B':'牛','C':'兔','D':'蛇'} and [s['missing'] for s in x['slots']]==[['馬'],['狗'],['狗']] and [s['present_count'] for s in x['slots']]==[0,1,2] and x['complete_columns']==0 and x['reserve_hits']==[] and set(x['outside_universe_hits'])=={'龍','猴'} and int(r['special'])==13,'331 actual revised plan 0/1,1/2,2/3, zero complete; seventh horse excluded')
ck([sum(x['complete_columns']==i for x in records) for i in range(4)]==[16,17,4,1] and [sum(x['slots'][i]['complete'] for x in records) for i in range(3)]==[14,10,4] and sum(x['shared_missing'] for x in records)==17 and len([x for x in records if x['universe_zodiacs'] is not None])==30 and sum(bool(x['reserve_hits']) for x in records if x['universe_zodiacs'] is not None)==14,'38-record distributions, shared-missing and 30 known/8 unknown universes')
last=set(zs);ps={by[2026330][f'z{i}'] for i in range(1,7)};ck(last=={'龍','牛','猴','兔','蛇'} and last&ps=={'牛','猴'} and len(last)==5 and len(last|{'馬'})==6 and sum(ns)==125 and max(ns)-min(ns)==44 and [sum(n%3==i for n in ns) for i in range(3)]==[3,1,2] and [sum(n%2==i for n in ns) for i in (1,0)]==[3,3] and 27%6==9%6 and 3%6==9%6,'330-to-331 repeat, 331 structure; same road/parity dragon cannot substitute for dog')
plans=J(B/'331-revised-design.json')['candidates'];counter=rev['candidate_counterfactuals'];ck(len(plans)==len(counter)==10,'ten pre-existing related alternatives isolated from actually selected GG01')
for p,c in zip(plans,counter):
 rr=p['roles'];needs=[{rr['top']},{rr['A'],rr['B']},{rr['A'],rr['C'],rr['D']}];ck(c['id']==p['id'] and c['roles']==rr and c['reserves']==p['reserves'] and c['complete_columns']==sum(v<=last for v in needs) and all(sl['present_count']==len(v&last) and set(sl['missing'])==v-last for sl,v in zip(c['slots'],needs)),p['id']+' 331 post-result counterfactual')
ck(Counter(x['complete_columns'] for x in counter)=={0:9,1:1} and next(x for x in counter if x['id']=='GG05')['slots'][2]['complete'] and next(x for x in counter if x['id']=='FF01')['complete_columns']==0,'GG05 counterfactual triple complete; initial and actual revised both zero; no retroactive replacement of actual')
e=J(Q/'evidence.json');ck(e['history_sha256']==H(S/'data/macau_mark_six_full.csv') and e['latest_period']==2026331 and not e['target_332_result_queried_or_used'],'descriptive evidence through 331 only')
wins=e['windows']
for z in Z:
 item=e['per_zodiac'][z];ck(item['numbers']==[n for n in range(1,50) if sign(n)==z] and item['last_normal_age']==next(i for i,q in enumerate(reversed(rows)) if z in [q[f'z{k}'] for k in range(1,7)]) and item['in_331_six']==(z in last) and item['in_331_seven']==(z in last|{'馬'}),z+' mapping, age and membership')
 for w in wins:
  rr=rows[-w:];ck(item['windows'][str(w)]=={'balls':sum([q[f'z{k}'] for k in range(1,7)].count(z) for q in rr),'periods':sum(z in [q[f'z{k}'] for k in range(1,7)] for q in rr)},f'{z} W{w} balls and periods')
for n in range(1,50):
 x=e['per_number'][str(n)];ck(x['zodiac']==sign(n) and x['road']==n%3 and x['odd_even']==('odd' if n%2 else 'even') and x['last_normal_age']==next(i for i,q in enumerate(reversed(rows)) if n in [int(q[f'n{k}']) for k in range(1,7)]),f'{n} mapping/age')
 for w in wins:ck(x['windows'][str(w)]==sum(n in [int(q[f'n{k}']) for k in range(1,7)] for q in rows[-w:]),f'{n} W{w} count')
for w in wins:
 ss=[{q[f'z{k}'] for k in range(1,7)} for q in rows[-w:]]
 for a,b in combinations(Z,2):ck(e['joint_zodiac_absence_periods'][str(w)][a+'|'+b]==sum(not ({a,b}&v) for v in ss),f'W{w} {a}{b} both absent')
 rr=rows[-w:];sn=[[int(q[f'n{k}']) for k in range(1,7)] for q in rr];st=e['structural_windows'][str(w)];ck(st['road_ball_counts']==[sum(n%3==i for row in sn for n in row) for i in range(3)] and st['odd_even_ball_counts']==[sum(n%2==i for row in sn for n in row) for i in (1,0)] and st['at_most_one_road_periods']==[sum(sum(n%3==i for n in row)<=1 for row in sn) for i in range(3)],f'W{w} road/parity structural counts')
study=J(Q/'six_sign_repeat_study.json');ck(study['current_pending']['previous_six']==['牛','兔','龍','蛇','猴'] and study['current_pending']['previous_seven']==['牛','兔','龍','蛇','馬','猴'] and not study['current_pending']['target_result_queried_or_used'] and not study['current_pending']['included_in_followup_denominators'] and study['groups']['previous_six_5_seven_6']=={'n':346,'six_to_six_counts_0_to_5':[8,70,141,107,20,0],'seven_to_seven_counts_0_to_6':[0,23,84,154,73,12,0]} and study['uniform_49_independent_model']['six_to_six']['sizes']==[4]*5,'5/6 cohort 346 and current 5 four-code normal identities')
with (Q/'six_sign_repeat_pairs.csv').open(encoding='utf8',newline='') as f:pairs=list(csv.DictReader(f))
ck(len(pairs)==837 and pairs[-1]['previous']=='2026330' and pairs[-1]['next']=='2026331' and pairs[-1]['repeat6_count']=='2' and pairs[-1]['repeat7_count']=='4','837 stored pairs end with 330→331; 332 excluded')
for t in pairs:
 a=by[int(t['previous'])];b=by[int(t['next'])];a6={a[f'z{i}'] for i in range(1,7)};b6={b[f'z{i}'] for i in range(1,7)};a7=a6|{a['special_zodiac']};b7=b6|{b['special_zodiac']};ck(int(t['prev6_distinct'])==len(a6) and int(t['prev7_distinct'])==len(a7) and int(t['repeat6_count'])==len(a6&b6) and int(t['repeat7_count'])==len(a7&b7) and set(t['repeat6'].split())==a6&b6 and set(t['repeat7'].split())==a7&b7,f"{t['previous']}→{t['next']} repeat pair")
for n,k in ((5,5),(5,6),(6,6),(6,7)):
 xs=[p for p in pairs if int(p['prev6_distinct'])==n and int(p['prev7_distinct'])==k];v=study['groups'][f'previous_six_{n}_seven_{k}'];ck(v['n']==len(xs) and v['six_to_six_counts_0_to_'+str(n)]==[sum(int(x['repeat6_count'])==i for x in xs) for i in range(n+1)] and v['seven_to_seven_counts_0_to_'+str(k)]==[sum(int(x['repeat7_count'])==i for x in xs) for i in range(k+1)],f'historical cohort {n}/{k}')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'retrospective_sha256':H(Q/'retrospective.json'),'evidence_sha256':H(Q/'evidence.json'),'study_sha256':H(Q/'six_sign_repeat_study.json'),'target_332_result_queried_or_used':False,'scope':'Internal arithmetic, user confirmation and frozen source bytes only; not official source, timing, actual odds or next-period forecasts.'};p=Q/'review_independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','checks_count':len(checks),'target_332_result_queried_or_used':False},ensure_ascii=False,indent=2))
