#!/usr/bin/env python3
"""Portable 315 observation-package verification. Run from any working directory.
No result lookup, selection, official-source validation, predraw certification or prediction.
"""
from pathlib import Path
from collections import Counter
from itertools import product
from tempfile import TemporaryDirectory
from math import comb
import csv,hashlib,json,os,re,shutil,subprocess,sys
O=Path(__file__).resolve().parent;D=O.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda n:json.loads((O/n).read_text(encoding='utf8'))
def C(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ck(v,m):
 if not v:raise AssertionError(m)
 print('PASS',m)
prior=O/'2026314-source-data.csv';source=O/'2026315-source-data.csv';old=prior.read_bytes().splitlines(keepends=True);new=source.read_bytes().splitlines(keepends=True)
ck(sha(prior)=='662032bf9829c1451ea4dcc221b2b4c8386d5efe953a73e1ac14789b0869e629' and sha(source)=='687efa128921ef7ace365131c023592a162a8dca4c367c88949ea0c16656ffb5','frozen 313 and staged user 314 source bytes')
ck(len(old)==1045 and len(new)==1046 and old[0]==new[0] and old[1:]==new[2:],'all prior 1044 records byte-identical, user 314 only appended')
rows=C(source);N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');zn=lambda n:Z[(7-n)%12];groups={z:[n for n in range(1,50) if zn(n)==z] for z in Z};u=J('2026314-user-result.json')
ck(len(rows)==1045 and len({r['period'] for r in rows})==1045 and [r['period'] for r in rows[:3]]==['2026314','2026313','2026312'],'1045 unique source records through 314 only')
ck(u['date'] is None and rows[0]['date']==rows[1]['date']=='' and N(rows[0])==u['normal_numbers']==[13,26,9,37,34,44] and int(rows[0]['special'])==u['seventh_number']==31,'314 user-only six-plus-one and 313/314 dates unknown')
ck(N(rows[1])+[int(rows[1]['special'])]==[33,39,45,15,7,20,43] and N(rows[2])+[int(rows[2]['special'])]==[31,46,4,43,32,15,38],'313 and corrected 312 exact records')
ck(all(len(set(N(r)+[int(r['special'])]))==7 for r in rows) and all([zn(n) for n in N(r)]==[r[f'z{i}'] for i in range(1,7)] and zn(int(r['special']))==r['special_zodiac'] for r in rows[:250]),'distinct numbers and current mapping of 250 displayed rows')
e=J('2026315-evidence.json');W=(10,20,35,40,45,60,100,250);blocks=((0,9),(10,19),(20,34),(35,39),(40,44))
for z in Z:
 v=e['per_zodiac'][z];g=set(groups[z]);assert v['numbers']==groups[z] and v['last_normal_age']==next(i for i,r in enumerate(rows) if any(n in g for n in N(r)))
 for w in W:
  b=[N(r) for r in rows[:w]];assert v['windows'][str(w)]=={'balls':sum(sum(n in g for n in a) for a in b),'periods':sum(any(n in g for n in a) for a in b)}
 for lo,hi in blocks:
  b=[N(r) for r in rows[lo:hi+1]];assert v['disjoint_age_blocks'][f'{lo}-{hi}']=={'balls':sum(sum(n in g for n in a) for a in b),'periods':sum(any(n in g for n in a) for a in b)}
ck(len(C(O/'2026315-zodiac-ledger.csv'))==12,'12 sign ages, periods, balls and nonoverlapping age blocks')
red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48};wave=lambda n:'紅' if n in red else '藍' if n in blue else '綠';ledger=C(O/'2026315-number-ledger.csv');assert len(ledger)==49 and {int(x['number']) for x in ledger}==set(range(1,50))
for item in ledger:
 n=int(item['number']);v=e['per_number'][str(n)];assert (v['zodiac'],v['road'],v['odd_even'],v['wave'],v['head'],v['tail'])==(zn(n),n%3,'奇' if n%2 else '偶',wave(n),n//10,n%10) and v['last_normal_age']==next(i for i,r in enumerate(rows) if n in N(r))
 for w in W:assert int(item[f'W{w}'])==v['window_counts'][str(w)]==sum(n in N(r) for r in rows[:w])
ck(True,'all 49 number mappings, attributes, ages and eight windows')
q=J('2026315-independent-qc.json')
for w in W:
 rs=rows[:w];nums=[n for r in rs for n in N(r)];v=e['structural_windows'][str(w)];assert v['road_ball_counts']==[sum(n%3==k for n in nums) for k in range(3)] and v['odd_even_ball_counts']==[sum(n%2 for n in nums),sum(n%2==0 for n in nums)] and v['red_blue_green_ball_counts']==[sum(wave(n)==c for n in nums) for c in ('紅','藍','綠')] and v['head_ball_counts']==[sum(n//10==k for n in nums) for k in range(5)] and v['tail_ball_counts']==[sum(n%10==k for n in nums) for k in range(10)]
 v=q['selected_shape_condition_counts'][str(w)];assert v['no_even_2road']==sum(not any(n%3==2 and n%2==0 for n in N(r)) for r in rs) and v['no_odd_0road']==sum(not any(n%3==0 and n%2 for n in N(r)) for r in rs) and v['at_most_one_1road']==sum(sum(n%3==1 for n in N(r))<=1 for r in rs) and v['at_most_one_2road']==sum(sum(n%3==2 for n in N(r))<=1 for r in rs) and v['at_most_one_even']==sum(sum(n%2==0 for n in N(r))<=1 for r in rs) and v['four_or_fewer_signs']==sum(len({zn(n) for n in N(r)})<=4 for r in rs)
ck(True,'six-normal 012, parity, wave, head, tail and selected scenario recounts')
seven=lambda r:set([r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']]);by={int(r['period']):r for r in rows};counts=[len(seven(by[p])&seven(by[p-1])) for p in range(2026309,2026315)];ck(counts==[4,4,5,5,3,3] and all(e['adjacent_identity_repeats'][str(p)]['seven_v_seven_count']==n for p,n in zip(range(2026309,2026315),counts)),'309–314 exact seven-to-seven distinct identities 4/4/5/5/3/3')
frozen=O/'2026314-445-source-through-311.csv';ck(sha(frozen)=='50a169bba6e0c07c57c7f105c19c92505b96d149d7c16e992bf8a4be2adfe156','immutable full-history 445 source through 311');x=C(frozen);sets=[set(r['zodiacs'].split()) if r['usable']=='1' else None for r in x]+[seven(rows[2]),seven(rows[1]),seven(rows[0])];tr=[None]+[len(a&b) if a is not None and b is not None else None for a,b in zip(sets,sets[1:])];ends=[i for i in range(3,len(sets)) if tr[i-2:i+1]==[4,4,5]];follows=Counter(tr[i+1] for i in ends if i+1<len(tr));invalid=sum(None in tr[i-2:i+1] for i in range(3,len(sets)));repeat=J('2026314-retrospective-repeat445.json');ck(len(sets)==2495 and len(ends)==9 and follows=={2:2,3:3,4:3,5:1} and invalid==8 and repeat['valid_candidate_windows']==2484,'445 exact seven-ball intersection and excluded bad windows')
hand=J('2026315-handwritten-design.json');audit=J('2026315-candidates.json');m=J('2026315-manual-decision.json');assert len(hand['candidates'])==len(audit['candidates'])==38
for key,name in [('handcrafted_candidates.json','2026315-handwritten-design.json'),('manual_decision.json','2026315-manual-decision.json'),('evidence.json','2026315-evidence.json')]:assert audit['input_sha256'][key]==sha(O/name)
den=comb(49,6);sigs=[];overlap=0
for a,b in zip(hand['candidates'],audit['candidates']):
 r=a['roles'];shown=list(dict.fromkeys(r[k] for k in ('top','A','B','C','D')));assert a['id']==b['id'] and r==b['roles'] and a['reserves']==b['reserves'] and len({r[k] for k in 'ABCD'})==4 and len(set(shown)|set(a['reserves']))==6 and not set(shown)&set(a['reserves']);sets={'single':{r['top']},'pair':{r['A'],r['B']},'triple':{r['A'],r['C'],r['D']},'all_columns':set(shown)};sigs.append((r['top'],frozenset(sets['pair']),frozenset(sets['triple'])));overlap+=r['top'] in {r[k] for k in 'ABCD'}
 for key,gs in sets.items():
  road=[sum(groups[z][0]%3==n for z in gs) for n in range(3)];odd=sum(groups[z][0]%2 for z in gs);assert b['minimums'][key]=={'distinct_zodiacs':len(gs),'road_min':road,'odd_min':odd,'even_min':len(gs)-odd}
 count=[0,0,0,0];col=[0,0,0];both=0;rest=49-sum(len(groups[z]) for z in shown)
 for n in product(*(range(len(groups[z])+1) for z in shown)):
  rem=6-sum(n)
  if not 0<=rem<=rest:continue
  ways=comb(rest,rem)
  for z,k in zip(shown,n):ways*=comb(len(groups[z]),k)
  active={z for z,k in zip(shown,n) if k};done=[sets[k]<=active for k in ('single','pair','triple')];count[sum(done)]+=ways
  for i,v in enumerate(done):col[i]+=ways*v
  if done[1] and done[2]:both+=ways
 assert sum(count)==den;actual={'single_pct':col[0],'pair_pct':col[1],'triple_pct':col[2],'all_columns_pct':count[3],'no_column_pct':count[0],'pair_and_triple_pct':both};assert all(abs(100*v/den-b['ideal_model_probabilities_percent'][k])<1e-9 for k,v in actual.items())
ck(len(set(sigs))==37 and overlap==16 and {x['roles']['A'] for x in hand['candidates']}==set(Z) and hand['proposed_id']==m['human_choice']==audit['selected']['id'],'38 hand designs, 37 distinct columns, 16 overlaps, 12 shared-A identities, exact ideal probabilities')
ck(m['universe']==['虎','蛇','馬','龍','兔','牛'] and m['top']=='虎' and m['pair']==['蛇','馬'] and m['triple']==['蛇','龍','兔'] and m['reserves']==['牛'],'manually fixed P01, reserve outside all columns')
sel=audit['selected'];ck(sel['minimums']['triple']['road_min']==[1,1,1] and sel['minimums']['triple']['even_min']==2 and sel['minimums']['all_columns']['road_min']==[1,2,2] and sel['minimums']['all_columns']['odd_min']==3 and sel['minimums']['all_columns']['even_min']==2,'joint route/parity minima reconstructed')
previous=J('2026314-retrospective-evidence.json');ck([x['present_count'] for x in previous['settlement']['slots']]==[0,1,2] and previous['settlement']['complete_count']==0,'old 314 choice settled 0/1, 1/2, 2/3, zero complete')
old=J('2026314-candidates.json')['selected']['ideal_model_probabilities_percent'];p=sel['ideal_model_probabilities_percent'];ck(all(abs(p[k]-old[x])<1e-9 for k,x in [('single_pct','single'),('pair_pct','pair'),('triple_pct','triple'),('all_columns_pct','all_columns')]),'314 and 315 model group isomorphism, not increased prediction')
d=J('2026315-manual-decisions.json');previous=J('2026314-manual-decisions.json');ck(all(d['decisions'][k]==v for k,v in previous['decisions'].items()) and d['decisions']['2026315']['human_comparison_id']==m['human_choice'],'all previous manual decisions preserved; 315 appended')
for n,h in [('2026312.json','e8b6fa62a1a5255215fcb1eee625aa8a462271a2ec768f020668afc83c54a5e5'),('2026312-rev1.json','077a1dec6e1f5a576c20146e748b3f0bad5550dc820427850b691079a1a437c3')]:assert sha(D/'pre-registration'/n)==h
ck(all(not (D/'pre-registration'/f'2026{n}.json').exists() for n in (313,314,315)),'original and revised 312 untouched; no fake 313/314/315 preregistration')
page=(O/'2026315-page.html').read_text(encoding='utf8');payload=json.loads(re.search(r'const DATA=(\{[^\n]+\}), ZN=DATA.order, ALL=DATA.rows;',page).group(1));assert len(payload['rows'])==250 and payload['order']==Z
for a,r in zip(payload['rows'],reversed(rows[:250])):assert a==[int(r['period']),r['date'][5:10].replace('-','/') if r['date'] else '--/--',N(r),[Z.index(r[f'z{i}']) for i in range(1,7)],int(r['special']),Z.index(r['special_zodiac'])]
assert payload['n2z']=={str(n):Z.index(zn(n)) for n in range(1,50)};md=json.loads(re.search(r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});',page).group(1));assert md['2026314']=={'U':[2,5,6,4,3,1],'top':2,'A':5,'B':6,'C':4,'D':3,'top_overlap_mode':'coverage'}
ck(all(x in page for x in ('315赛前未核实、无预注册','来源与机制未认证','谨防博彩诈骗','2026315-analysis.md','313、314日期未知')),'page payload, exact manual roles, unknown dates and compact warning')
with TemporaryDirectory(prefix='315-reproduce-') as t:
 t=Path(t);(t/'data').mkdir();(t/'www').mkdir();shutil.copyfile(source,t/'data/macau_mark_six_full.csv');shutil.copyfile(O/'2026315-manual-decisions.json',t/'data/manual_site_decisions.json');env=dict(os.environ);env['POOL_VERSION']='v5.0';subprocess.run([sys.executable,str(O/'2026315-generator.py')],cwd=t,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);assert (t/'zodiac_trend.html').read_bytes()==(O/'2026315-page.html').read_bytes()==(t/'www/zodiac_trend.html').read_bytes()
ck(True,'byte-for-byte standalone page reproduction from packaged records and hand decision')
print('315 OFFLINE INDEPENDENT VERIFICATION PASS — nonofficial, not predraw or mechanism certification')
