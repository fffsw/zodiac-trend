#!/usr/bin/env python3
"""Independent source-to-settlement audit: 36 retained versions and three reconstructions."""
from pathlib import Path
from collections import Counter
from itertools import product
import csv,hashlib,json,re,subprocess
R=Path('/home/user');T=R/'archive/task300_329_review';B=T/'before';Q=T/'analysis';S=R/'archive/task301_330_release/stage';D=Path('/tmp/task300_330_deploy/observations');F=D/'2026327-retrospective-frozen';G=D/'2026328-retrospective-frozen';I=D/'2026329-retrospective-frozen';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(x,msg):
 if not x:raise AssertionError(msg)
 checks.append(msg)
subprocess.run(['sha256sum','--quiet','-c',str(T/'before.sha256')],cwd=B,check=True)
for directory,manifest in [(F,'../2026327-before.sha256'),(G,'../2026328-before.sha256'),(I,'../2026329-frozen.sha256')]:subprocess.run(['sha256sum','--quiet','-c',manifest],cwd=directory,check=True)
ck(True,'current freeze and all independently retained prior source manifests match')
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows={int(x['period']):x for x in csv.DictReader(f)}
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];doc=J(Q/'retrospective.json');records=doc['historical_outcomes'];pat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';ck(len(records)==36 and sorted(x['period'] for x in records)==[p for p in range(2026291,2026330) if p not in (2026319,2026322,2026324)],'36 retained displays span 291–329, excluding 319/322/324')
for it in records:
 per=it['period'];r=rows[per];nums=[int(r[f'n{i}']) for i in range(1,7)];got={sign(n) for n in nums};ck([sign(n) for n in nums]==[r[f'z{i}'] for i in range(1,7)]==it['normal_zodiacs'] and nums==it['normal_numbers'] and it['special_number']==int(r['special']) and it['special_zodiac']==r['special_zodiac'],f'{per} six and separate seventh match history')
 if per<=2026308:
  p=J(F/f'prior-records/{per}.json')['site_display'];role={'top':Z[p['top']],'A':Z[p['t2'][0]],'B':Z[p['t2'][1]],'C':Z[p['t3'][1]],'D':Z[p['t3'][2]]}
 else:
  path=B/'329-current-homepage.html' if per==2026329 else I/'328-current-homepage.html' if per==2026328 else G/'327-current-homepage.html' if per==2026327 else F/f'historical-pages/{per}.html';mm=re.search(pat,path.read_text());assert mm;v=json.loads(mm.group(1))[str(per-1)];role={k:Z[v[k]] for k in ('top','A','B','C','D')}
 ck(it['roles']==role,f'{per} roles from retained source')
 want=[[role['top']],[role['A'],role['B']],[role['A'],role['C'],role['D']]];total=0
 for sl,need in zip(it['slots'],want):
  found=[z for z in need if z in got];miss=[z for z in need if z not in got];ok=not miss;ck(sl['required']==need and sl['present']==found and sl['missing']==miss and sl['present_count']==len(found) and sl['needed_count']==len(need) and sl['complete']==ok and sl['balls']==[{'number':n,'zodiac':sign(n)} for n in nums if sign(n) in need],f'{per} {sl["name"]} six-only settlement');total+=ok
 ck(total==it['complete_columns'] and it['shared_missing']==(role['A'] not in got),f'{per} complete column count')
for it in doc['unpublished_reconstructions']:
 per=it['period'];v=J(F/f'{per%1000}-reconstruction-manual.json');role={'top':v['top'],'A':v['pair'][0],'B':v['pair'][1],'C':v['triple'][1],'D':v['triple'][2]};got={sign(int(rows[per][f'n{i}'])) for i in range(1,7)};needs=[[role['top']],[role['A'],role['B']],[role['A'],role['C'],role['D']]];ck(v['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' and it['status']==v['status'] and it['roles']==role and all(sl['present']==[z for z in need if z in got] and sl['missing']==[z for z in need if z not in got] and sl['complete']==set(need).issubset(got) for sl,need in zip(it['slots'],needs)) and it['complete_columns']==sum(set(need).issubset(got) for need in needs),f'{per} reconstruction checked separately')
ck([it['period'] for it in doc['unpublished_reconstructions']]==[2026319,2026322,2026324],'three after-outcome reconstructions never counted as published')
counts=Counter(x['complete_columns'] for x in records);g=doc['historical_groups']['all_36_mixed_sources_versions'];ck(g['complete_columns_distribution_0_to_3']==[counts[i] for i in range(4)]==[15,17,3,1] and [g[k] for k in ('single_complete','pair_complete','triple_complete','shared_A_absent')]==[sum(x['slots'][i]['complete'] for x in records) for i in range(3)]+[sum(x['shared_missing'] for x in records)]==[13,9,4,16] and len(g['shared_A_present_both_pair_triple_incomplete_periods'])==8,'independent 36-period totals and dependency counts')
with (Q/'historical_display_outcomes.csv').open(encoding='utf8',newline='') as f:tab=list(csv.DictReader(f))
ck(len(tab)==36 and all(int(t['period'])==x['period'] and int(t['complete_columns'])==x['complete_columns'] and [t[k+'_hits'] for k in ('single','pair','triple')]==[f"{s['present_count']}/{s['needed_count']}" for s in x['slots']] and [t[k+'_missing'].split() for k in ('single','pair','triple')]==[s['missing'] for s in x['slots']] for t,x in zip(tab,records)),'36-row readable CSV reconciles every column and missing identity')
r=rows[2026329];nums=[int(r[f'n{i}']) for i in range(1,7)];got={sign(n) for n in nums};pre={rows[2026328][f'z{i}'] for i in range(1,7)};ck(nums==[45,6,46,33,31,40] and got=={'狗','牛','鷄','鼠','兔'} and int(r['special'])==44 and r['special_zodiac']=='豬' and r['date']=='' and len(got)==5 and pre&got=={'狗','鼠'} and [s['missing'] for s in doc['settlement']['slots']]==[['馬'],['虎'],['虎','羊']] and [sum(n%3==i for n in nums) for i in range(3)]==[3,3,0] and 44%3==2 and 31%6==1 and 6%6==0,'329 shared tiger absent, repeat-two, normal no 2-road, distinct five, and seventh excluded')
choices=J(B/'329-candidates.json')['candidates'];counter=doc['candidate_counterfactuals'];ck(len(choices)==len(counter)==12,'twelve previously retained 329 candidate identities')
for a,b in zip(choices,counter):
 rr=a['roles'];needs=[{rr['top']},{rr['A'],rr['B']},{rr['A'],rr['C'],rr['D']}];ck(a['id']==b['id'] and rr==b['roles'] and all(sl['present_count']==len(need&got) and sl['complete']==(need<=got) for sl,need in zip(b['slots'],needs)) and b['complete_columns']==sum(need<=got for need in needs) and 'POST_OUTCOME' in b['scope'],f"{a['id']} hindsight settlement")
ck(Counter(x['complete_columns'] for x in counter)=={0:8,1:4} and [x['id'] for x in counter if x['complete_columns']==1]==['DD06','DD07','DD11','DD12'],'8/4 counterfactual distribution, not evidence of next outcome')
for horse,tiger,chicken,mouse,sheep in product((False,True),repeat=5):
 no=not horse and not (tiger and chicken) and not (tiger and mouse and sheep);ck(no==((not horse) and ((not tiger) or ((not chicken) and ((not mouse) or (not sheep))))),'DD01 zero-column Boolean identity, all 32 states')
prevstudy=J(B/'329-six-sign-study.json')['groups']['previous_six_6_seven_7'];ck(prevstudy['n']==130 and prevstudy['six_to_six_counts_0_to_6']==[2,12,50,47,16,3,0] and len(pre&got)==2,'prior disclosed repeat-two condition appeared 50/130 times; not a future forecast')
ck(subprocess.check_output(['git','status','--porcelain','-uall'],cwd=R/'deploy',text=True)==(B/'old-dirty-deploy-status.txt').read_text() and H(R/'zodiac_trend.html')==H(B/'329-current-homepage.html'),'original workspace page and unrelated dirty checkout unchanged')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'retrospective_sha256':H(Q/'retrospective.json'),'historical_csv_sha256':H(Q/'historical_display_outcomes.csv'),'reconstruction_csv_sha256':H(Q/'reconstructed_outcomes_separate.csv'),'counterfactual_csv_sha256':H(Q/'329_candidates_counterfactual.csv'),'scope':'Source-to-source arithmetic only, not official draw, outcome timing, fairness, returns, next-period forecast, or authentication of old publication time.','target_330_result_queried_or_used':False};p=Q/'independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks_count':len(checks),'historical_records':len(records),'retrospective_sha256':out['retrospective_sha256']},ensure_ascii=False,indent=2))
