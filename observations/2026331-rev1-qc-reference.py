#!/usr/bin/env python3
"""Independent exact mask enumeration, 37-period settlement and revision comparison QC."""
from pathlib import Path
from collections import Counter
from math import comb
import csv,hashlib,json,subprocess
R=Path('/home/user');A=R/'archive/task304_331_revision';B=A/'before';Q=A/'analysis';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();audit=J(Q/'revision_audit.json');design=J(Q/'revision_design.json');br=J(Q/'revision_brute_model.json');rev=J(B/'initial-retrospective.json');checks=[]
def ck(x,s):
 if not x:raise AssertionError(s)
 checks.append(s)
subprocess.run(['sha256sum','--quiet','-c',str(A/'before.sha256')],cwd=B,check=True);ck(True,'35 frozen sources match manifest')
Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');sign=lambda n:Z[(7-n)%12];sg={z:[n for n in range(1,50) if sign(n)==z] for z in Z};prev={'馬','猴','豬','牛','鷄'};prevbits=sum(1<<Z.index(z) for z in prev);maskof=lambda ss:sum(1<<Z.index(z) for z in set(ss));
with (B/'history-through-330.csv').open(encoding='utf-8-sig',newline='') as f:rr=sorted(csv.DictReader(f),key=lambda x:int(x['period']))
by={int(r['period']):r for r in rr};s6=lambda r:{r[f'z{i}'] for i in range(1,7)};ck(len(rr)==1061 and int(rr[-1]['period'])==2026330 and s6(rr[-1])==prev and [int(rr[-1][f'n{i}']) for i in range(1,7)]==[25,35,20,8,30,22] and rr[-1]['date']=='' and rr[-1]['special_zodiac']=='蛇' and not audit['target_331_result_queried_or_used'],'history ends at user 330; inferred sixth and separate seventh')
# Reproduce exact number of ways for each 12-sign presence mask by independent polynomial.
ways={}
for mask in range(1<<12):
 if mask.bit_count()>6:continue
 poly=[1,0,0,0,0,0,0]
 for i,z in enumerate(Z):
  if not (mask>>i)&1:continue
  q=[0]*7
  for a in range(7):
   for k in range(1,min(len(sg[z]),6-a)+1):q[a+k]+=poly[a]*comb(len(sg[z]),k)
  poly=q
 if poly[6]:ways[mask]=poly[6]
ck(sum(ways.values())==comb(49,6)==13983816==br['denominator'],'all feasible sign-mask weights sum to 49 choose 6')
ck(len(audit['candidates'])==len(design['candidates'])==10 and audit['choice']==design['choice']=='GG01' and audit['candidates'][0]['id']=='FF01','ten related candidates, original preserved')
for src,x in zip(design['candidates'],audit['candidates']):
 r=x['roles'];single=maskof([r['top']]);pair=maskof([r['A'],r['B']]);triple=maskof([r['A'],r['C'],r['D']]);display={r[k] for k in ('top','A','B','C','D')};ck(src['id']==x['id'] and src['roles']==r and len(display)==5 and len(display|set(x['reserves']))==6 and set(x['previous_six_overlap'])==display&prev and x['previous_normal_count']==len(display&prev),'candidate identities '+x['id'])
 md=[0]*4;c=Counter();cond=[[0]*4 for _ in range(6)];ss=[[0,0,0] for _ in range(6)]
 for mask,w in ways.items():
  slots=[mask&single==single,mask&pair==pair,mask&triple==triple];n=sum(slots);k=(mask&prevbits).bit_count();md[n]+=w;cond[k][n]+=w
  for i,b in enumerate(slots):ss[k][i]+=w*b
  for key,b in zip(('single','pair','triple'),slots):c[key]+=w*b
  c['pair_and_triple']+=w*(slots[1] and slots[2])
 ck(md==x['uniform_model']['distribution'] and all(c[k]==x['uniform_model'][k] for k in c) and all(cond[k]==x['conditional_repeat'][k]['distribution'] and ss[k]==[x['conditional_repeat'][k][n] for n in ('single','pair','triple')] for k in range(6)),'independent 12-sign-mask count '+x['id'])
 for w in (35,40,45,60,100,250):
  q=[0]*4
  for old in rr[-w:]:
   gm=s6(old);q[sum(t<=gm for t in ({r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}))]+=1
  ck(q==x['posthoc_fixed_windows'][str(w)]['complete_0_1_2_3'] and 'post-hoc' in x['posthoc_fixed_windows'][str(w)]['scope'],x['id']+' fixed hindsight window '+str(w))
 got=s6(rr[-1]);needs=[{r['top']},{r['A'],r['B']},{r['A'],r['C'],r['D']}];ck(x['posthoc_330']['complete_columns']==sum(v<=got for v in needs) and [v['hits'] for v in x['posthoc_330']['slots']]==[len(v&got) for v in needs] and 'counterfactual' in x['posthoc_330']['scope'],x['id']+' 330 not an actual release')
for x in rev['historical_outcomes']:
 r=by[x['period']];got=s6(r);role=x['roles'];needs=[[role['top']],[role['A'],role['B']],[role['A'],role['C'],role['D']]];ck([int(r[f'n{i}']) for i in range(1,7)]==x['normal_numbers'] and [r[f'z{i}'] for i in range(1,7)]==x['normal_zodiacs'] and all(sl['required']==need and sl['present']==[z for z in need if z in got] and sl['missing']==[z for z in need if z not in got] and sl['complete']==(set(need)<=got) for sl,need in zip(x['slots'],needs)) and x['complete_columns']==sum(set(need)<=got for need in needs),f"original {x['period']} independently settled")
ck(Counter(x['complete_columns'] for x in rev['historical_outcomes'])=={0:15,1:17,2:4,3:1} and [x['period'] for x in rev['unpublished_reconstructions']]==[2026319,2026322,2026324] and all(x['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' for x in rev['unpublished_reconstructions']),'37 mixed retained versions and 3 reconstruction boundaries')
base=audit['baseline'];sel=audit['selected'];ck(sel['roles']=={'top':'馬','A':'狗','B':'牛','C':'兔','D':'蛇'} and sel['reserves']==['虎'] and set(sel['previous_six_overlap'])=={'馬','牛'} and set(sel['changed_relative_to_initial_331'])=={'鷄','龍'} and set(sel['new_relative_to_initial_331'])=={'狗','兔'} and len(sel['changed_relative_to_330_display'])==3,'revision: two 330 hits retained, two original 331 displayed identities replaced')
for name,model,condition in [('old',base,br['old_conditional']),('revised',sel,br['revised_conditional'])]:
 overall=br[name];ck(overall['distribution']==model['uniform_model']['distribution'] and all(overall[k]==model['uniform_model'][k] for k in ('single','pair','triple','pair_and_triple')),name+' direct 13,983,816 enumeration')
 for k in range(6):ck(condition[k]['distribution']==model['conditional_repeat'][k]['distribution'] and all(condition[k][v]==model['conditional_repeat'][k][v] for v in ('single','pair','triple')),name+' brute repeat '+str(k))
ck(br['old']==br['revised'] and br['old']['distribution']==[5392128,7401592,1144016,46080],'identical unconditional model, no proved prediction advantage')
for mask in range(1<<12):
 got={z for i,z in enumerate(Z) if mask>>i&1};oldv=[{'馬'}<=got,{'鷄','牛'}<=got,{'鷄','龍','蛇'}<=got];newv=[{'馬'}<=got,{'狗','牛'}<=got,{'狗','兔','蛇'}<=got];zero=('馬' not in got and ('狗' not in got or ('牛' not in got and ('兔' not in got or '蛇' not in got))));ck((not any(newv))==zero,'zero-column boolean '+str(mask))
 if len(got)<=6:
  k=len(prev&got)
  if k==0:ck(not any(oldv) and not newv[0] and not newv[1],'zero repeat condition '+str(mask))
  if k==5:ck(oldv==[True,True,False] and newv[0] and not newv[2],'five repeat condition '+str(mask))
  if all(newv):ck(k in (2,3),'new full requires repeat 2 or 3 '+str(mask))
zero=[9,4,2,3,12,16];five=[25,35,20,30,22,3];ngot={sign(n) for n in zero};fgot={sign(n) for n in five};ck(len(set(zero))==6 and not ngot&prev and {'狗','兔','蛇'}<=ngot and '馬' not in ngot and '牛' not in ngot and not({'鷄','龍','蛇'}<=ngot),'synthetic zero-repeat witness: revised triple possible but original zero')
ck(len(set(five))==6 and len(fgot&prev)==5 and {'馬','鷄','牛'}<=fgot and '狗' not in fgot and '兔' not in fgot and '蛇' not in fgot,'synthetic five-repeat witness: old has two complete and revised only single')
ck(sel['posthoc_330']['complete_columns']==1 and base['posthoc_330']['complete_columns']==2 and [sel['posthoc_fixed_windows'][str(k)]['complete_0_1_2_3'][0] for k in (35,40,45)]==[11,14,18] and [base['posthoc_fixed_windows'][str(k)]['complete_0_1_2_3'][0] for k in (35,40,45)]==[11,12,16],'new 330 and history hindsight performance disclosed even when worse')
out={'status':'PASS','checks_count':len(checks),'checks':checks,'frozen_sha256':H(A/'before.sha256'),'design_sha256':H(Q/'revision_design.json'),'audit_sha256':H(Q/'revision_audit.json'),'brute_sha256':H(Q/'revision_brute_model.json'),'model_enumerated_sets':13983816,'target_331_result_queried_or_used':False,'scope':'Internal arithmetic and synthetic witnesses only; no source, future outcome, timing, real odds or profit certified.'};(Q/'revision_qc.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks_count':len(checks),'model_enumerated_sets':13983816,'choice':'GG01'},ensure_ascii=False,indent=2))
