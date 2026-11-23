#!/usr/bin/env python3
"""Independent recount of 326 settlement, candidate outcomes and every available history snapshot."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,subprocess
R=Path('/home/user');A=R/'archive/task291_326_review';B=A/'before';O=A/'analysis';I=A/'input';D=R/'archive/task292_327_release/clean_deploy';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();doc=J(O/'retrospective.json');u=J(I/'user-326.json');Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');G={z:{n for n in range(1,50) if Z[(7-n)%12]==z} for z in Z};zof=lambda n:next(z for z,ns in G.items() if n in ns);checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
def csvread(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
rr=csvread(B/'history-through-325.csv');rows={int(r['period']):r for r in rr};rows[2026326]={'period':'2026326',**{f'n{i}':str(n) for i,n in enumerate(u['normal_numbers'],1)},**{f'z{i}':z for i,z in enumerate(u['normal_zodiacs'],1)},'special':str(u['seventh_number']),'special_zodiac':u['seventh_zodiac']};N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];S=lambda r:[r[f'z{i}'] for i in range(1,7)];sort=lambda s:sorted(s,key=Z.index)
ck(len(rr)==1056 and max(int(r['period']) for r in rr)==2026325 and len(set(u['normal_numbers']+[u['seventh_number']]))==7 and [zof(n) for n in u['normal_numbers']]==u['normal_zodiacs'] and zof(u['seventh_number'])==u['seventh_zodiac']=='猴','326 user input, six-plus-one convention and 2026 zodiac groups independently checked')
for p in range(2026291,2026327):assert [zof(n) for n in N(rows[p])]==S(rows[p]) and zof(int(rows[p]['special']))==rows[p]['special_zodiac']
ck(True,'each 291–326 raw historical six and separately stored seventh matches this era mapping')
def result(required,signs):
 return (sort(required&signs),sort(required-signs),len(required&signs),required<=signs)
actual=set(u['normal_zodiacs']);current=[{'羊'},{'虎','羊'},{'虎','馬','鷄'}];old=[{'羊'},{'虎','羊'},{'虎','馬','兔'}]
for label,ss in [('settlement',current),('original_v1_settlement',old)]:
 for req,x in zip(ss,doc[label]['slots']):assert result(req,actual)==(x['present'],x['missing'],x['present_count'],x['complete'])
assert [(x['present_count'],x['complete']) for x in doc['settlement']['slots']]==[(1,True),(2,True),(2,False)] and doc['settlement']['slots'][2]['missing']==['馬'] and doc['settlement']['outside_universe_hits']==sort({'狗','兔','猴'}) and doc['settlement']['reserve_hits']==[] and [x['present_count'] for x in doc['original_v1_settlement']['slots']]==[1,2,2]
ck(True,'326 single/pair complete and triple missing horse; old rabbit and revised chicken both appear, without counting special')
assert set(S(rows[2026325]))=={'虎','馬','鷄','龍'} and len(actual&set(S(rows[2026325])))==2 and len((actual|{u['seventh_zodiac']})&(set(S(rows[2026325]))|{rows[2026325]['special_zodiac']}))==2 and sum(n%3==1 for n in N(rows[2026326]))==2 and not any(n%3==1 and n%2 for n in N(rows[2026326])) and len(actual)==6
ck(True,'repeat-two and absent odd-1-road, rather than absent or insufficient whole 1-road, verified')
old_e=J(B/'326-prior-evidence.json');previous=sorted(rr,key=lambda r:int(r['period']))
for w in (10,20,35,40,45,60,100,250):
 xs=previous[-w:];p=doc['pre_326_pressure'][str(w)];values={'no_odd_1road':sum(all(not(n%3==1 and n%2) for n in N(r)) for r in xs),'at_most_one_1road':sum(sum(n%3==1 for n in N(r))<=1 for r in xs),'has_1road_but_no_odd1':sum(any(n%3==1 for n in N(r)) and all(not(n%3==1 and n%2) for n in N(r)) for r in xs),'road_exact_2_2_2':sum([sum(n%3==k for n in N(r)) for k in range(3)]==[2,2,2] for r in xs),'six_distinct':sum(len(set(S(r)))==6 for r in xs),'no_horse':sum('馬' not in S(r) for r in xs),'no_horse_and_no_rat':sum(not {'馬','鼠'}&set(S(r)) for r in xs)}
 assert all(p[k]==v for k,v in values.items()) and p['no_odd_1road']==old_e['structural_windows'][str(w)]['no_odd_1road_periods']
ck(True,'eight pre-326 window counts independently recomputed; overlapping windows not independent')
hand=J(B/'326-original-handwritten.json')['candidates'];design=J(B/'326-revision-design.json')['plans'];c=doc['candidate_outcomes'];assert len(hand)==38 and len(design)==11 and len(c)==49
for x,y in zip(hand+design,c):
 r=x['roles'];assert y['id']==x['id'] and y['roles']==r and y['reserves']==x['reserves'];ss=[{r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}];val=[result(t,actual) for t in ss];assert [v[2] for v in val]==[y['single_hit'],y['pair_hits'],y['triple_hits']] and sum(v[3] for v in val)==y['complete_columns'] and val[2][1]==y['triple_missing']
ck(True,'all 49 previously defined 326 alternatives independently settled, no post-outcome ranking claim')
provs={x['target']:x for x in J(O/'historical_page_provenance.json')['records']};ledger=doc['historical_outcomes'];csvledger=csvread(O/'historical_display_outcomes.csv');assert len(provs)==15 and len(ledger)==len(csvledger)==33
for a,line in zip(ledger,csvledger):
 p=a['period'];assert str(p)==line['period'] and a['normal_numbers']==N(rows[p]) and a['normal_zodiacs']==S(rows[p]) and a['special_number']==int(rows[p]['special']) and a['special_zodiac']==rows[p]['special_zodiac']
 if p<=2026308:
  s=J(B/f'prior-records/{p}.json')['site_display'];r={'top':Z[s['top']],'A':Z[s['t2'][0]],'B':Z[s['t2'][1]],'C':Z[s['t3'][1]],'D':Z[s['t3'][2]]};assert a['source_kind'].startswith('SURVIVING_PRE_REGISTRATION')
 else:
  pp=B/f'historical-pages/{p}.html';prov=provs[p];raw=subprocess.check_output(['git','show',prov['git_commit']+':zodiac_trend.html'],cwd=D);assert raw==pp.read_bytes() and H(pp)==prov['page_sha256'];m=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',pp.read_text()).group(1))[str(p-1)];r={k:Z[m[k]] for k in ('top','A','B','C','D')};assert a['source_kind'].startswith('GIT_PAGE_SNAPSHOT')
 assert r==a['roles'];required=[{r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}];signs=set(S(rows[p]));results=[result(t,signs) for t in required]
 for idx,(got,x) in enumerate(zip(results,a['slots'])):assert got==(x['present'],x['missing'],x['present_count'],x['complete']) and line[['single_hits','pair_hits','triple_hits'][idx]]==str(got[2])+'/'+str(idx+1)
 assert sum(x[3] for x in results)==a['complete_columns']==int(line['complete_columns']) and a['shared_missing']==(r['A'] not in signs)
ck(True,'33 individual records independently re-settled against frozen 18 earlier prereg records and 15 original Git pages')
for key,source in [('all_33_mixed_sources_versions',ledger),('frozen_prereg_291_308',[x for x in ledger if x['period']<=2026308]),('git_snapshot_309_326',[x for x in ledger if x['period']>=2026309]),('git_snapshot_313_326',[x for x in ledger if x['period']>=2026313])]:
 t=doc['historical_groups'][key];assert t['n']==len(source) and t['complete_columns_distribution_0_to_3']==[sum(x['complete_columns']==i for x in source) for i in range(4)] and t['shared_A_absent']==sum(x['shared_missing'] for x in source) and [t[f'{name}_complete'] for name in ('single','pair','triple')]==[sum(x['slots'][i]['complete'] for x in source) for i in range(3)]
assert [x['period'] for x in doc['unpublished_reconstructions']]==[2026319,2026322,2026324] and not set(x['period'] for x in doc['unpublished_reconstructions'])&set(x['period'] for x in ledger)
ck(True,'all group totals recounted; 319/322/324 after-result reconstructions excluded from actual-record statistics')
assert doc['target_327_result_read'] is False and len(actual)==len(actual|{u['seventh_zodiac']})==doc['theoretical_repeat_maximum_to_327_six']==doc['theoretical_repeat_maximum_to_327_seven']==6;subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True)
ck(True,'326 has six distinct signs so next theoretical repeat ceiling is six; no claim about actual 327')
out={'status':'PASS','scope':'independent retrospective and historical recount; not official source, predraw timing, actual mechanism or predictive advantage','checks':checks,'retrospective_sha256':H(O/'retrospective.json'),'historical_csv_sha256':H(O/'historical_display_outcomes.csv'),'candidate_csv_sha256':H(O/'326_candidate_outcomes.csv')};p=O/'independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
