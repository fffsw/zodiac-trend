#!/usr/bin/env python3
"""Reproduce every saved version from raw frozen sources and the user 327 row."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,subprocess
R=Path('/home/user');A=R/'archive/task294_327_review';B=A/'before';Q=A/'analysis';S=R/'archive/task295_328_release/stage';D=R/'archive/task295_328_release/clean_deploy/observations';F=D/'2026327-retrospective-frozen';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True);subprocess.run(['sha256sum','--quiet','-c','../2026327-before.sha256'],cwd=F,check=True);ck(True,'30 current freeze copies and 70 previous frozen originals match their independent prior manifests')
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows={int(x['period']):x for x in csv.DictReader(f)}
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');n2z=lambda n:Z[(7-n)%12];doc=J(Q/'retrospective.json');records=doc['historical_outcomes'];assert len(records)==34;manpat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});'
for item in records:
 per=item['period'];row=rows[per];nums=[int(row[f'n{i}']) for i in range(1,7)];got={n2z(n) for n in nums};assert [n2z(n) for n in nums]==[row[f'z{i}'] for i in range(1,7)] and nums==item['normal_numbers']
 if per<=2026308:
  p=J(F/f'prior-records/{per}.json')['site_display'];role={'top':Z[p['top']],'A':Z[p['t2'][0]],'B':Z[p['t2'][1]],'C':Z[p['t3'][1]],'D':Z[p['t3'][2]]}
 else:
  path=B/'327-current-homepage.html' if per==2026327 else F/f'historical-pages/{per}.html';p=json.loads(re.search(manpat,path.read_text()).group(1))[str(per-1)];role={k:Z[p[k]] for k in ('top','A','B','C','D')}
 assert item['roles']==role and item['special_number']==int(row['special']) and item['special_zodiac']==row['special_zodiac']
 expected=[[role['top']],[role['A'],role['B']],[role['A'],role['C'],role['D']]];complete=0
 for sl,need in zip(item['slots'],expected):
  found=[z for z in need if z in got];miss=[z for z in need if z not in got];assert sl['required']==need and sl['present']==found and sl['missing']==miss and sl['present_count']==len(found) and sl['needed_count']==len(need) and sl['complete']==(not miss) and sl['balls']==[{'number':n,'zodiac':n2z(n)} for n in nums if n2z(n) in need];complete+=not miss
 assert complete==item['complete_columns'] and item['shared_missing']==(role['A'] not in got)
ck(True,'all 102 columns for 34 saved versions re-settled from raw files, never including seventh ball')
for x in doc['unpublished_reconstructions']:
 per=x['period'];source=J(F/f'{per%1000}-reconstruction-manual.json');rr=x['roles'];assert source['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' and rr=={'top':source['top'],'A':source['pair'][0],'B':source['pair'][1],'C':source['triple'][1],'D':source['triple'][2]};got={rows[per][f'z{i}'] for i in range(1,7)};sets=[[rr['top']],[rr['A'],rr['B']],[rr['A'],rr['C'],rr['D']]];assert all(sl['present_count']==len(set(a)&got) for sl,a in zip(x['slots'],sets)) and x['complete_columns']==sum(set(a)<=got for a in sets)
ck([x['period'] for x in doc['unpublished_reconstructions']]==[2026319,2026322,2026324],'three post-result reconstructions separately checked, not counted as actual original releases')
row=rows[2026327];nums=[int(row[f'n{i}']) for i in range(1,7)];prev={rows[2026326][f'z{i}'] for i in range(1,7)};got={n2z(n) for n in nums};v=doc['settlement'];assert nums==[21,49,7,41,46,36] and int(row['special'])==45 and row['date']=='' and [sl['present_count'] for sl in v['slots']]==[1,1,2] and [sl['missing'] for sl in v['slots']]==[[],['龍'],['牛']] and v['complete_columns']==1 and prev&got=={'狗','羊','鷄','虎'} and got-prev=={'馬','鼠'}
assert sum(nums)==200 and max(nums)-min(nums)==42 and [sum(n%3==k for n in nums) for k in range(3)]==[2,3,1] and [sum(n%2==1 for n in nums),sum(n%2==0 for n in nums)]==[4,2] and 21%6==3 and 36%6==0 and [n2z(x) for x in (21,36)]==['狗','羊']
pre=[rows[k] for k in sorted(rows,reverse=True) if k<2026327];counts=[sum(not ({'龍','牛'}&{r[f'z{i}'] for i in range(1,7)}) for r in pre[:w]) for w in (35,40,45)];assert counts==[13,16,17] and doc['failure_analysis']['before_327_dragon_ox_jointly_absent_w35_w40_w45']==counts
ck(True,'327 shared chicken hit, both missing tails and same-route/parity peers, repeat-four exposure and pre-327 joint absences independently checked')
G=doc['historical_groups']['all_34_mixed_sources_versions'];dist=Counter(x['complete_columns'] for x in records);Aabs=sum(x['roles']['A'] not in set(x['normal_zodiacs']) for x in records);apbf=sum(x['roles']['A'] in set(x['normal_zodiacs']) and not x['slots'][1]['complete'] and not x['slots'][2]['complete'] for x in records);peer=lambda z:next(t for t in Z if t!=z and next(n for n in range(1,50) if n2z(n)==t)%6==next(n for n in range(1,50) if n2z(n)==z)%6);pc=sum(any(peer(z) in set(x['normal_zodiacs']) for sl in x['slots'] for z in sl['missing']) for x in records)
assert G['complete_columns_distribution_0_to_3']==[dist[i] for i in range(4)]==[13,17,3,1] and [G['single_complete'],G['pair_complete'],G['triple_complete']]==[sum(x['slots'][i]['complete'] for x in records) for i in range(3)]==[13,9,4] and G['shared_A_absent']==Aabs==15 and G['shared_A_present_both_pair_triple_incomplete_count']==apbf==7 and G['at_least_one_missing_chosen_sign_with_same_route_parity_peer_present_count']==pc==23
ck(True,'34-record summary and shared-anchor and same-category failure counts independently recounted')
choices=J(B/'327-handwritten-design.json')['candidates'];counter=doc['candidate_counterfactuals'];assert len(choices)==len(counter)==12
for a,b in zip(choices,counter):
 rr=a['roles'];assert a['id']==b['id'] and rr==b['roles'] and a['reserves']==b['reserves'];s=[{rr['top']},{rr['A'],rr['B']},{rr['A'],rr['C'],rr['D']}];assert [b['single_hits'],b['pair_hits'],b['triple_hits']]==[len(x&got) for x in s] and b['complete_columns']==sum(x<=got for x in s) and 'post-result' in b['scope']
ck(True,'12 already-recorded 327 alternatives re-settled only as explicitly post-result counterfactuals')
with (Q/'historical_display_outcomes.csv').open(encoding='utf8',newline='') as f:csvrows=list(csv.DictReader(f))
assert len(csvrows)==34
for x,y in zip(records,csvrows):assert int(y['period'])==x['period'] and int(y['complete_columns'])==x['complete_columns'] and [y[k+'_hits'] for k in ('single','pair','triple')]==[f"{sl['present_count']}/{sl['needed_count']}" for sl in x['slots']]
ck(True,'34-row downloadable CSV agrees with independent per-column recount')
out={'status':'PASS','scope':'arithmetic and frozen-record consistency only; no official, pre-draw, outcome, mechanism, return or prediction certification','checks':checks,'retrospective_sha256':H(Q/'retrospective.json'),'historical_csv_sha256':H(Q/'historical_display_outcomes.csv'),'candidate_csv_sha256':H(Q/'327_candidate_counterfactual.csv'),'target_328_result_queried_or_used':False};p=Q/'independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
