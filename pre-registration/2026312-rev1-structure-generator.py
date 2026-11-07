#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026312 draw-structure evidence ledger; no selection, RNG or deployment.

Normal six numbers only. The previous draw's seven zodiac identities are used
only for PREV labels, as in v5.0; the special ball is not counted in draws.
Windows overlap, so disjoint age blocks are supplied first. Exact baseline is
uniform six-without-replacement from 49. Selected-set category cover is NOT
claimed to be a predictive signal or the probability of a completed column.
"""
import csv
import hashlib
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path('/home/user')
CSV = ROOT / 'data/task242_1042_reconciled_history.csv'
OUTPUT = ROOT / 'data/task242_312_reconciled_draw_structure_ledger.txt'
JSON_OUT = ROOT / 'data/task242_312_reconciled_draw_structure_metrics.json'
TARGET = 2026312
Z2N = {
 '鼠':[7,19,31,43], '牛':[6,18,30,42], '虎':[5,17,29,41],
 '兔':[4,16,28,40], '龍':[3,15,27,39], '蛇':[2,14,26,38],
 '馬':[1,13,25,37,49], '羊':[12,24,36,48], '猴':[11,23,35,47],
 '鷄':[10,22,34,46], '狗':[9,21,33,45], '豬':[8,20,32,44],
}
N2Z = {n:z for z, ns in Z2N.items() for n in ns}
RED = {1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46}
BLUE = {3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48}
GREEN = set(range(1,50)) - RED - BLUE
CATEGORY = {
 'road0': {x for x in range(1,50) if x%3==0},
 'road1': {x for x in range(1,50) if x%3==1},
 'road2': {x for x in range(1,50) if x%3==2},
 'odd': {x for x in range(1,50) if x%2==1},
 'even': {x for x in range(1,50) if x%2==0},
 'small': set(range(1,25)), 'big': set(range(25,50)),
 'small25': set(range(1,26)), 'big26': set(range(26,50)),
 'red': RED, 'blue': BLUE, 'green': GREEN,
}
ALL = set(range(1,50))
DEN = math.comb(49,6)
assert len(N2Z)==49 and set(N2Z)==ALL
assert len(RED)==17 and len(BLUE)==len(GREEN)==16
assert len(CATEGORY['road0'])==16 and len(CATEGORY['road1'])==17 and len(CATEGORY['road2'])==16

def c(n,k):
 return math.comb(n,k) if 0<=k<=n else 0

def hprob(k, K, N=49, sample=6):
 return c(K,k)*c(N-K,sample-k)/c(N,sample)

def at_least_one(k):
 return 1-c(49-k,6)/DEN

def pct(f): return f'{f*100:.4f}%'
def fmt_counter(counter, keys): return ' '.join(f'{k}:{counter[k]}' for k in keys)
def triple(ns, cats): return tuple(sum(n in CATEGORY[x] for n in ns) for x in cats)

def num_fields(row): return [int(row[f'n{j}']) for j in range(1,7)]
def zodiac_fields(row): return [row[f'z{j}'].strip() for j in range(1,7)]
def previous_label(row): return set(zodiac_fields(row)) | {row['special_zodiac'].strip()}

rows = sorted(list(csv.DictReader(CSV.open(encoding='utf-8-sig', newline=''))), key=lambda r: int(r['period']))
assert len(rows)==1042 and int(rows[-1]['period'])==TARGET-1
assert hashlib.md5(CSV.read_bytes()).hexdigest()=='f91c57bb50f3c4c36965274eb5f66b11'
assert len({r['period'] for r in rows})==len(rows)
for r in rows:
 ns = num_fields(r)
 assert len(set(ns))==6 and all(n in ALL for n in ns)
for r in rows[-251:]:
 ns = num_fields(r); zs = zodiac_fields(r)
 assert all(N2Z[n]==z for n,z in zip(ns,zs)), (r['period'],ns,zs)
 assert all((('红' if n in RED else '蓝' if n in BLUE else '绿')==r[f'w{j}'].strip()) for j,n in enumerate(ns,1))
assert num_fields(rows[-1])==[32,40,49,14,19,16]
assert previous_label(rows[-1])=={'鼠','兔','蛇','馬','鷄','豬'}

# DP for distinct represented zodiac groups, optionally count only a subset.
def distinct_zod_distribution(marked=None):
 dp={(0,0):1}
 for z,ns in Z2N.items():
  nxt=defaultdict(int)
  for (total, marked_distinct), ways in dp.items():
   for k in range(min(len(ns),6-total)+1):
    add=int(k>0 and (marked is None or z in marked))
    nxt[(total+k,marked_distinct+add)] += ways*c(len(ns),k)
  dp=nxt
 values={j: dp.get((6,j),0)/DEN for j in range(7)}
 assert abs(sum(values.values())-1)<1e-12
 return values

# Probability the drawn and selected numbers include at least one from each road.
# Disjoint selected road populations; all remaining balls are unselected.
def selected_all_roads(nums):
 k=[len(nums & CATEGORY[f'road{i}']) for i in range(3)]
 other=49-sum(k)
 fav=0
 for a in range(1,min(k[0],6)+1):
  for b in range(1,min(k[1],6-a)+1):
   for d in range(1,min(k[2],6-a-b)+1):
    fav+=c(k[0],a)*c(k[1],b)*c(k[2],d)*c(other,6-a-b-d)
 return fav/DEN

def category_model(cats):
 ns=[len(CATEGORY[x]) for x in cats]
 assert sum(ns)==49
 dist={}
 for a in range(7):
  for b in range(7-a):
   z=6-a-b
   if a<=ns[0] and b<=ns[1] and z<=ns[2]:
    dist[(a,b,z)]=c(ns[0],a)*c(ns[1],b)*c(ns[2],z)/DEN
 assert abs(sum(dist.values())-1)<1e-12
 return dist

road_dist=category_model(('road0','road1','road2'))
wave_dist=category_model(('red','blue','green'))
full_all3=sum(p for (a,b,d),p in road_dist.items() if a and b and d)
assert abs(full_all3-selected_all_roads(ALL))<1e-12
zod_dist=distinct_zod_distribution()


def row_info(i):
 row=rows[i]; nums=num_fields(row); zs=zodiac_fields(row)
 prev=rows[i-1]; prev_id=previous_label(prev)
 return {
  'period':int(row['period']), 'nums':nums, 'zodiacs':zs,
  'odd':sum(n%2 for n in nums), 'small':sum(n<=24 for n in nums),
  'small25':sum(n<=25 for n in nums),
  'roads':triple(nums,('road0','road1','road2')),
  'waves':triple(nums,('red','blue','green')),
  'heads':len({n//10 for n in nums}), 'tails':len({n%10 for n in nums}),
  'zodiac_distinct':len(set(zs)), 'zodiac_shape':tuple(sorted(Counter(zs).values(),reverse=True)),
  'prev_numbers':len(set(nums)&set(num_fields(prev))),
  'prev_zodiacs':len(set(zs)&prev_id), 'prev_ids':sorted(prev_id),
  'sum':sum(nums), 'span':max(nums)-min(nums),
 }

infos=[row_info(i) for i in range(len(rows)-251,len(rows))]
by_period={x['period']:x for x in infos}

def summarize(sub):
 result={'n':len(sub),'first':sub[0]['period'],'last':sub[-1]['period']}
 for name in ('odd','small','small25','zodiac_distinct','prev_numbers','prev_zodiacs','heads','tails'):
  cnt=Counter(x[name] for x in sub)
  result[name]={k:cnt[k] for k in range(7)}
 for name in ('roads','waves','zodiac_shape'):
  cnt=Counter(x[name] for x in sub)
  result[name]={'/'.join(map(str,k)):v for k,v in sorted(cnt.items())}
 result['road_total']=[sum(x['roads'][j] for x in sub) for j in range(3)]
 result['wave_total']=[sum(x['waves'][j] for x in sub) for j in range(3)]
 result['odd_balls']=sum(x['odd'] for x in sub)
 result['small_balls']=sum(x['small'] for x in sub)
 result['small25_balls']=sum(x['small25'] for x in sub)
 result['road_all3']=sum(all(x['roads']) for x in sub)
 result['road_no0']=sum(x['roads'][0]==0 for x in sub)
 result['road0_2plus']=sum(x['roads'][0]>=2 for x in sub)
 result['wave_all3']=sum(all(x['waves']) for x in sub)
 result['repeated_zodiac_any']=sum(x['zodiac_distinct']<6 for x in sub)
 result['sum_mean']=statistics.mean(x['sum'] for x in sub)
 result['sum_median']=statistics.median(x['sum'] for x in sub)
 result['sum_range']=[min(x['sum'] for x in sub),max(x['sum'] for x in sub)]
 result['span_mean']=statistics.mean(x['span'] for x in sub)
 result['span_range']=[min(x['span'] for x in sub),max(x['span'] for x in sub)]
 result['head_ball_counts']=[sum(n//10==j for x in sub for n in x['nums']) for j in range(5)]
 result['tail_ball_counts']=[sum(n%10==j for x in sub for n in x['nums']) for j in range(10)]
 # Exact conditional expectation given the observed previous draw's seven zodiac identities.
 ex=[0.0]*7
 for x in sub:
  model=distinct_zod_distribution(set(x['prev_ids']))
  for j in range(7): ex[j]+=model[j]
 result['prev_zodiac_null_expected']=[round(v,6) for v in ex]
 assert sum(result['odd'].values())==len(sub) and sum(result['small'].values())==len(sub)
 assert sum(result['road_total'])==6*len(sub) and sum(result['wave_total'])==6*len(sub)
 assert sum(result['prev_zodiacs'].values())==len(sub)
 return result

windows={w:summarize(infos[-w:]) for w in (10,20,35,40,45,60,100,250)}
age_blocks={f'{a}-{b-1}':summarize(infos[-b:len(infos)-a if a else None]) for a,b in [(0,10),(10,20),(20,35),(35,45),(45,60),(60,100),(100,250)]}
assert sum(x['n'] for x in age_blocks.values())==250

# Historical frozen 311 shown only as a comparison baseline, NOT a 312 pick.
CANDIDATES={
 'frozen_311_reference_only': {
  'U':['蛇','馬','兔','豬','龍','鷄'],
  'display':['馬','兔','蛇','豬','龍'],
 },
}

def pool_metrics(zs):
 nums={n for z in zs for n in Z2N[z]}
 counts={name:len(nums&members) for name,members in CATEGORY.items()}
 return {
  'zodiacs':zs, 'numbers':sorted(nums),'size':len(nums), 'counts':counts,
  'coverage_of_class':{name:len(nums&members)/len(members) for name,members in CATEGORY.items()},
  'expected_selected_balls_by_class':{name:6*len(nums&members)/49 for name,members in CATEGORY.items()},
  'class_atleast_one_selected':{name:at_least_one(len(nums&members)) for name,members in CATEGORY.items()},
  'selected_all_3_road_prob':selected_all_roads(nums),
  'head_counts':[sum(n//10==j for n in nums) for j in range(5)],
  'tail_counts':[sum(n%10==j for n in nums) for j in range(10)],
  'min':min(nums),'max':max(nums), 'mean_number':statistics.mean(nums),
 }

candidate_metrics={name:{k:pool_metrics(v) for k,v in candidate.items()} for name,candidate in CANDIDATES.items()}
for candidate in CANDIDATES.values():
 assert len(candidate['U'])==6 and len(set(candidate['U']))==6
 assert len(set(candidate['display']))==5 and set(candidate['display'])<=set(candidate['U'])

out=[]
def add(s=''): out.append(s)
add('TASK242 RECONCILED DRAW STRUCTURE EVIDENCE, target=2026312, cutoff=2026311; six normal numbers only')
add('Data MD5='+hashlib.md5(CSV.read_bytes()).hexdigest()+'; rows=1042; latest='+str(num_fields(rows[-1])))
add('Primary small=1..24; big=25..49; alternative small25=1..25, big26=26..49; roads=n%3; odd=25/even=24; red/blue/green=17/16/16; 0/1/2=16/17/16')
add('One fixed number: one position=1/49, included in six=6/49. Exact models below are uniform, without replacement.')
add('No model selects any zodiac or role. All windows are retrospective descriptions; overlapping windows are not independent.')
add('\n## Exact null distributions')
for label,K in [('odd',25),('small',24),('small25',25),('road0',16)]:
 probs=[hprob(j,K) for j in range(7)]
 assert abs(sum(probs)-1)<1e-12
 add(label+': '+' '.join(f'{j}:{pct(v)}' for j,v in enumerate(probs)))
add('road all three in full draw='+pct(full_all3)+'; at least one 0-road in full draw='+pct(at_least_one(16)))
add('wave all three in full draw='+pct(sum(p for vals,p in wave_dist.items() if all(vals))))
add('distinct zodiac in full draw: '+' '.join(f'{j}:{pct(zod_dist[j])}' for j in range(7)))
add('same number as prior six: '+' '.join(f'{j}:{pct(hprob(j,6))}' for j in range(7)))
add('full draw sum expectation=150; sum SD='+f'{math.sqrt(6*(49-6)/(49-1)*200):.6f}'+'; span expectation='+f'{50*5/7:.6f}')
add('\n## Disjoint age blocks')
for key,s in age_blocks.items():
 add(f"age={key} periods={s['first']}..{s['last']} n={s['n']} oddsBalls={s['odd_balls']}/{6*s['n']} smallBalls={s['small_balls']}/{6*s['n']} roads={s['road_total']} wave={s['wave_total']} all3Road={s['road_all3']} no0Road={s['road_no0']} road0_2plus={s['road0_2plus']} zodDistinct={s['zodiac_distinct']} sumMean={s['sum_mean']:.2f} spanMean={s['span_mean']:.2f}")
add('\n## Windows (overlap: same draws counted in several windows; no independent confirmation)')
for w,s in windows.items():
 add(f"W{w} periods={s['first']}..{s['last']} n={w} oddballs={s['odd_balls']}/{6*w} smallballs={s['small_balls']}/{6*w} roads={s['road_total']} wave={s['wave_total']} all3Road={s['road_all3']} no0Road={s['road_no0']} road0_2plus={s['road0_2plus']} waveAll3={s['wave_all3']}")
 add('  alternative small25/big26 balls='+str(s['small25_balls'])+'/'+str(6*w-s['small25_balls']))
 for attr in ('odd','small','small25','zodiac_distinct','prev_numbers','prev_zodiacs'):
  add('  '+attr+' '+fmt_counter(s[attr],range(7)))
 add('  012 compositions='+str(s['roads']))
 add('  zodiac shapes='+str(s['zodiac_shape']))
 add('  headBall='+str(s['head_ball_counts'])+' tailBall='+str(s['tail_ball_counts']))
 add(f"  sumMean/median/range={s['sum_mean']:.4f}/{s['sum_median']}/{s['sum_range']} spanMean/range={s['span_mean']:.4f}/{s['span_range']}")
 add('  prev7 zodiac distinct expected counts under null='+str([round(x,3) for x in s['prev_zodiac_null_expected']]))
add('\n## Most recent 45 full-draw structures')
for x in infos[-45:]:
 add(f"{x['period']} nums={x['nums']} road={x['roads']} odd/even={x['odd']}/{6-x['odd']} small/big={x['small']}/{6-x['small']} wave={x['waves']} distinctZ={x['zodiac_distinct']} shape={x['zodiac_shape']} prev7Z={x['prev_zodiacs']} prev6N={x['prev_numbers']} sum={x['sum']} span={x['span']}")
add('\n## Each zodiac has all numbers in a single road and a single parity')
for z,ns in Z2N.items():
 assert len({n%3 for n in ns})==1 and len({n%2 for n in ns})==1
 add(f"{z} {ns} road={ns[0]%3} parity={'odd' if ns[0]%2 else 'even'} wave={triple(ns,('red','blue','green'))}")
add('\n## Candidate comparisons; per-category cover is the fraction of the CLASS included, not the probability that the next DRAW has that structure')
for name,cm in candidate_metrics.items():
 add('\n'+name)
 for which,p in cm.items():
  q=p['counts']; r=[q[f'road{i}'] for i in range(3)]
  add(f"  {which} z={p['zodiacs']} n={p['size']} numbers={p['numbers']}")
  add(f"    roads={r}, classCover={[round(p['coverage_of_class'][f'road{i}'],6) for i in range(3)]}, expectedDrawnSelectedRoad={[round(p['expected_selected_balls_by_class'][f'road{i}'],6) for i in range(3)]}, pAllRoadsHaveSelected={pct(p['selected_all_3_road_prob'])}")
  add(f"    odd/even={q['odd']}/{q['even']} small/big={q['small']}/{q['big']} alternateSmall25/big26={q['small25']}/{q['big26']} red/blue/green={q['red']}/{q['blue']}/{q['green']} head={p['head_counts']} tail={p['tail_counts']} numberMean={p['mean_number']:.3f}")
  add('    classP(at least 1 selected) roads='+str([round(p['class_atleast_one_selected'][f'road{i}']*100,4) for i in range(3)]))
add('\n## Tests and invariants')
assert candidate_metrics['frozen_311_reference_only']['U']['counts']['road0']==4
assert candidate_metrics['frozen_311_reference_only']['display']['counts']['road0']==4
assert candidate_metrics['frozen_311_reference_only']['U']['size']==25
assert candidate_metrics['frozen_311_reference_only']['display']['size']==21
add('CSV structure, mappings, color, six-normal-only, exact nulls, block partition and candidate counts: PASS')
add('TASK242_RECONCILED_DRAW_STRUCTURE_LEDGER PASS')
assert not OUTPUT.exists() and not JSON_OUT.exists(), 'structure ledger exists; refuse overwrite'
OUTPUT.write_text('\n'.join(out)+'\n',encoding='utf-8')
json_data={'target':TARGET,'data_md5':hashlib.md5(CSV.read_bytes()).hexdigest(),'windows':windows,'age_blocks':age_blocks,
 'null':{'odd':[hprob(j,25) for j in range(7)],'small':[hprob(j,24) for j in range(7)],
         'road0':[hprob(j,16) for j in range(7)],'road_all3':full_all3,'distinct_zodiac':zod_dist,
         'same_as_previous_six':[hprob(j,6) for j in range(7)]},
 'candidates':candidate_metrics}
JSON_OUT.write_text(json.dumps(json_data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('\n'.join(out))
