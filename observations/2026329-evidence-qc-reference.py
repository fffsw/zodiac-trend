#!/usr/bin/env python3
"""Independent recount of descriptive inputs and two non-interchangeable repeat cohorts."""
from pathlib import Path
from datetime import date
from collections import Counter
from itertools import combinations
from math import comb
import csv,hashlib,json
R=Path('/home/user');A=R/'archive/task299_329_release';O=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=J(O/'evidence.json');st=J(O/'six_sign_repeat_study.json');checks=[]
def ck(v,m):
 if not v:raise AssertionError(m)
 checks.append(m)
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda x:int(x['period']))
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];norm=lambda r:[int(r[f'n{i}']) for i in range(1,7)];s6=lambda r:{r[f'z{i}'] for i in range(1,7)};s7=lambda r:s6(r)|{r['special_zodiac']};ck(len(rows)==1059 and int(rows[-1]['period'])==2026328 and rows[-1]['date']=='' and e['history_sha256']==st['input_history_sha256']==H(S/'data/macau_mark_six_full.csv') and not e['target_329_result_queried_or_used'] and not st['current_pending']['target_result_queried_or_used'],'history stops at user 328; no target data')
for r in rows[-250:]:ck([sign(n) for n in norm(r)]==[r[f'z{i}'] for i in range(1,7)] and sign(int(r['special']))==r['special_zodiac'] and len(set(norm(r)+[int(r['special'])]))==7,f"mapping and uniqueness {r['period']}")
for z in Z:
 v=e['per_zodiac'][z];ck(v['numbers']==[n for n in range(1,50) if sign(n)==z] and v['in_328_six']==(z in s6(rows[-1])) and v['in_328_seven']==(z in s7(rows[-1])) and v['last_normal_age']==next(i for i,r in enumerate(rows[::-1]) if z in s6(r)),f'{z} numbers and identity')
 for w in e['windows']:
  rr=rows[-w:];ck(v['windows'][str(w)]=={'balls':sum([r[f'z{i}'] for i in range(1,7)].count(z) for r in rr),'periods':sum(z in s6(r) for r in rr)},f'{z} W{w} counts')
for n in range(1,50):
 v=e['per_number'][str(n)];ck(v['zodiac']==sign(n) and v['last_normal_age']==next(i for i,r in enumerate(rows[::-1]) if n in norm(r)) and all(v['windows'][str(w)]==sum(n in norm(r) for r in rows[-w:]) for w in e['windows']),f'{n} number ledger')
for w in e['windows']:
 for a,b in combinations(Z,2):ck(e['joint_zodiac_absence_periods'][str(w)]['|'.join(z for z in Z if z in {a,b})]==sum(not({a,b}&s6(r)) for r in rows[-w:]),f'joint absence W{w} {a}/{b}')
# Rebuild cohort independently from raw rows; use explicit boundary IDs rather than prior function.
by={int(x['period']):x for x in rows};cross={(2024040,2024041),(2025028,2025029),(2026047,2026048)};rec=[]
for p in sorted(by):
 q=p+1
 if q not in by and p//1000+1==2025 and p%1000==366:q=2025001
 elif q not in by and p//1000+1==2026 and p%1000==365:q=2026001
 if q not in by or (p,q) in cross:continue
 a,b=by[p],by[q]
 if p//1000!=q//1000:
  try:
   if (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days!=1:continue
  except ValueError:continue
 if len(set(norm(a)+[int(a['special'])]))!=7 or len(set(norm(b)+[int(b['special'])]))!=7:continue
 if len(s6(a))==6:rec.append((p,q,len(s7(a)),len(s6(a)&s6(b)),len(s7(a)&s7(b))))
with (O/'six_sign_repeat_pairs.csv').open(encoding='utf8',newline='') as f:tab=list(csv.DictReader(f))
ck(len(rec)==len(tab)==263 and all((p,q,k,a,b)==(int(t['previous']),int(t['next']),int(t['prev7_distinct']),int(t['repeat6_count']),int(t['repeat7_count'])) for (p,q,k,a,b),t in zip(rec,tab)),'all 263 cohort pair entries independently reproduced, including year rollover')
for k in (6,7):
 group=[x for x in rec if x[2]==k];v=st['groups'][f'previous_six_6_seven_{k}'];ck(v['n']==len(group) and v['six_to_six_counts_0_to_6']==[sum(x[3]==i for x in group) for i in range(7)] and v['seven_to_seven_counts_0_to_'+str(k)]==[sum(x[4]==i for x in group) for i in range(k+1)],f'previous 6/{k} cohort independently recounted')
ck(set(st['current_pending']['previous_six'])==s6(rows[-1]) and set(st['current_pending']['previous_seven'])==s7(rows[-1]) and len(s6(rows[-1]))==6 and len(s7(rows[-1]))==7 and s7(rows[-1])-s6(rows[-1])=={'牛'} and st['groups']['previous_six_6_seven_7']['n']==130,'current cohort is 6 normal / 7 seven-ball, NOT 6/6')
for name,m,d in [('six_to_six',6,6),('seven_to_seven',7,7)]:
 # Inclusion-exclusion: choose k identities present; all others absent; force each selected group nonempty.
 cnt=[comb(m,k)*sum((-1)**j*comb(k,j)*comb(49-4*(m-k+j),d) for j in range(k+1)) for k in range(m+1)];model=st['uniform_49_independent_model'][name];ck(cnt==model['counts'] and sum(cnt)==comb(49,d)==model['denominator'],f'{name} exact group-product count independently matches inclusion-exclusion')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'evidence_sha256':H(O/'evidence.json'),'repeat_study_sha256':H(O/'six_sign_repeat_study.json'),'scope':'Arithmetic and record consistency only; cohorts are descriptive, not future probability, source or time authentication.','target_329_result_queried_or_used':False};(O/'evidence_qc.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','checks_count':len(checks),'cohort_6_7_n':130,'era_boundaries_excluded':3},ensure_ascii=False,indent=2))
