#!/usr/bin/env python3
"""Correct reserve/universe classification, preserving the first review and its QC unchanged."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,shutil,subprocess
R=Path('/home/user');T=R/'archive/task300_329_review';Q=T/'analysis';B=T/'before';O=Path('/tmp/task300_330_deploy/observations');F=O/'2026327-retrospective-frozen';G=O/'2026328-retrospective-frozen';I=O/'2026329-retrospective-frozen';C=T/'corrections/reserve_classification';snap=C/'before';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');order=lambda x:[z for z in Z if z in set(x)];p=Q/'retrospective.json';prior=J(Q/'independent_qc.json');assert prior['status']=='PASS' and prior['retrospective_sha256']==H(p) and not C.exists();subprocess.run(['sha256sum','--quiet','-c',str(T/'before.sha256')],cwd=B,check=True)
for d,m in ((F,'../2026327-before.sha256'),(G,'../2026328-before.sha256'),(I,'../2026329-frozen.sha256')):subprocess.run(['sha256sum','--quiet','-c',m],cwd=d,check=True)
snap.mkdir(parents=True);source_files=[p,Q/'independent_qc.json',Q/'historical_display_outcomes.csv',Q/'reconstructed_outcomes_separate.csv',Q/'329_candidates_counterfactual.csv',R/'scripts/task300_329_retrospective_and_history.py',R/'scripts/task300_329_retrospective_independent_qc.py']
for f in source_files:shutil.copyfile(f,snap/f.name);assert H(f)==H(snap/f.name)
(C/'before.sha256').write_text(''.join(f'{H(snap/f.name)}  {f.name}\n' for f in sorted(source_files,key=lambda x:x.name)),encoding='utf8');subprocess.run(['sha256sum','--quiet','-c','../before.sha256'],cwd=snap,check=True)
d=J(p);pat=r'const MANUAL_SITE_DECISIONS_V50=(\{[^\n]+\});';corrected=[];unknown=[]
for x in d['historical_outcomes']:
 per=x['period'];shown=set(x['roles'].values());got=set(x['normal_zodiacs']);orig=(x['reserve_hits'],x['outside_universe_hits']);source=None;universe=None
 if per<=2026308:
  source=f'2026327-retrospective-frozen/prior-records/{per}.json';v=J(F/f'prior-records/{per}.json')['site_display'];universe=v.get('universe_zodiac')
  if universe is not None:assert [Z[i] for i in v['universe']]==universe
 else:
  src=B/'329-current-homepage.html' if per==2026329 else I/'328-current-homepage.html' if per==2026328 else G/'327-current-homepage.html' if per==2026327 else F/f'historical-pages/{per}.html';source='329-current-homepage.html' if per==2026329 else '2026329-retrospective-frozen/328-current-homepage.html' if per==2026328 else '2026328-retrospective-frozen/327-current-homepage.html' if per==2026327 else f'2026327-retrospective-frozen/historical-pages/{per}.html';v=json.loads(re.search(pat,src.read_text()).group(1))[str(per-1)];universe=[Z[i] for i in v['U']]
 if universe is None:
  assert per<=2026298;x.update({'universe_status':'NOT_PROVEN_IN_RETAINED_SOURCE','universe_zodiacs':None,'unallocated_universe_zodiacs':None,'reserve_hits':None,'outside_universe_hits':None,'unknown_nondisplay_hits':order(got-shown),'universe_reference':source});unknown.append(per)
 else:
  assert len(universe)==len(set(universe))==6 and shown<=set(universe);reserve=set(universe)-shown;x.update({'universe_status':'EXPLICIT_RETAINED_UNIVERSE_UNALLOCATED_NOT_AUTO_SUBSTITUTE','universe_zodiacs':universe,'unallocated_universe_zodiacs':order(reserve),'reserve_hits':order(reserve&got),'outside_universe_hits':order(got-set(universe)),'unknown_nondisplay_hits':None,'universe_reference':source})
  if orig!=(x['reserve_hits'],x['outside_universe_hits']):corrected.append(per)
 assert x['displayed_hits']==order(shown&got)
recon_changed=[]
for x in d['unpublished_reconstructions']:
 per=x['period'];v=J(F/f'{per%1000}-reconstruction-manual.json');u=v['universe'];shown=set(x['roles'].values());got=set(x['normal_zodiacs']);reserve=set(u)-shown;assert v['status']==x['status']=='AFTER_OUTCOME_RECONSTRUCTED_NOT_PUBLISHED_OR_PREDRAW' and set(v['reserves'])==reserve and len(u)==len(set(u))==6
 if x['reserve_hits']!=order(reserve&got):recon_changed.append(per)
 x.update({'universe_status':'AFTER_OUTCOME_RECONSTRUCTION_UNALLOCATED_NOT_AUTO_SUBSTITUTE','universe_zodiacs':u,'unallocated_universe_zodiacs':order(reserve),'reserve_hits':order(reserve&got),'outside_universe_hits':order(got-set(u)),'unknown_nondisplay_hits':None,'universe_reference':f'2026327-retrospective-frozen/{per%1000}-reconstruction-manual.json'})
known=[x for x in d['historical_outcomes'] if x['universe_zodiacs'] is not None];hits=[x for x in known if x['reserve_hits']];assert len(known)==28 and len(unknown)==8 and len(hits)==14 and corrected==[2026299,2026303,2026304,2026305,2026306,2026308,2026309,2026310,2026312,2026314,2026315,2026321,2026323,2026328] and recon_changed==[2026322,2026324] and d['historical_outcomes'][-2]['reserve_hits']==['虎'] and d['historical_outcomes'][-1]['reserve_hits']==[] and d['settlement']['complete_columns']==0
# Only universe classifications change. Formal slots, counts, diagnostics and manual choice are untouched.
original=J(snap/'retrospective.json')
for old,new in zip(original['historical_outcomes'],d['historical_outcomes']):
 for k in ('period','source_kind','version','reference','roles','normal_numbers','normal_zodiacs','special_number','special_zodiac','slots','complete_columns','displayed_hits','shared_missing'):assert old[k]==new[k],(old['period'],k)
for old,new in zip(original['unpublished_reconstructions'],d['unpublished_reconstructions']):
 for k in ('period','status','roles','slots','complete_columns','displayed_hits','shared_missing'):assert old[k]==new[k],(old['period'],k)
for k in ('settlement','shape','historical_groups','candidate_counterfactuals','diagnosis'):assert d[k]==original[k],k
d['reserve_classification_correction']={'status':'CORRECTED_BEFORE_PUBLICATION','reason':'Initial review re-settled historical records with empty reserve identities, silently classifying known inactive-universe hits as outside; early records without an explicit universe must be unknown, not empty.','retained_known_universes':28,'retained_unknown_universes':8,'retained_periods_with_inactive_universe_hits':corrected,'reconstruction_periods_with_inactive_universe_hits_corrected':recon_changed,'old_review_sha256':H(snap/'retrospective.json'),'old_qc_sha256':H(snap/'independent_qc.json'),'slots_and_complete_columns_changed':False,'reserve_never_fills_formal_columns':True,'scope':'Retained universe identities are non-column members; no historical publication timing is certified.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
cols=['period','classification_status','universe','non_column_universe_members','non_column_hits_in_inferred_first_six','outside_explicit_universe_in_inferred_first_six','non_display_hits_with_unknown_universe','source_reference']
def write(path,records):
 with path.open('x',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
  for x in records:w.writerow({'period':x['period'],'classification_status':x['universe_status'],'universe':' '.join(x['universe_zodiacs'] or []),'non_column_universe_members':' '.join(x['unallocated_universe_zodiacs'] or []),'non_column_hits_in_inferred_first_six':' '.join(x['reserve_hits'] or []),'outside_explicit_universe_in_inferred_first_six':' '.join(x['outside_universe_hits'] or []),'non_display_hits_with_unknown_universe':' '.join(x['unknown_nondisplay_hits'] or []),'source_reference':x['universe_reference']})
write(Q/'retained_universe_reserve_audit.csv',d['historical_outcomes']);write(Q/'reconstructed_universe_reserve_audit.csv',d['unpublished_reconstructions'])
notice={'status':'CORRECTION_APPLIED_AWAITING_INDEPENDENT_QC','known_universe_retained_records':28,'unknown_universe_retained_records':unknown,'retained_periods_with_noncolumn_universe_hits':corrected,'reconstructed_periods_corrected_separately':recon_changed,'previous_review_sha256':H(snap/'retrospective.json'),'corrected_review_sha256':H(p),'original_qc_sha256':H(snap/'independent_qc.json'),'frozen_manifest_sha256':H(C/'before.sha256'),'slots_and_complete_columns_changed':False,'source_or_predraw_certified':False,'target_330_result_queried_or_used':False};(C/'correction_receipt.json').write_text(json.dumps(notice,ensure_ascii=False,indent=2)+'\n');print(json.dumps(notice,ensure_ascii=False,indent=2))
