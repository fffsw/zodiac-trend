#!/usr/bin/env python3
"""Independently reproduce the report tables and ensure local evidence links resolve."""
from pathlib import Path
import csv,hashlib,json,re
R=Path('/home/user');Q=R/'archive/task295_328_release/analysis';T=R/'archive/task294_327_review/analysis';S=R/'archive/task295_328_release/stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();report=R/'327期复盘_328期方案与逐期核验.md';text=report.read_text();rev=J(T/'retrospective.json');aud=J(Q/'candidate_audit.json');e=J(Q/'evidence.json');Z=list('鼠牛虎兔龍蛇馬羊猴鷄狗豬');checks=[]
def ck(v,s):
 if not v:raise AssertionError(s)
 checks.append(s)
with (S/'data/macau_mark_six_full.csv').open(encoding='utf-8-sig',newline='') as f:history=sorted(csv.DictReader(f),key=lambda x:int(x['period']),reverse=True)
rows={int(x['period']):x for x in history};records={x['period']%1000:(x['period'],x['roles'],False) for x in rev['historical_outcomes']};records.update({x['period']%1000:(x['period'],x['roles'],True) for x in rev['unpublished_reconstructions']});lines=[x for x in text.splitlines() if re.match(r'^\| \d{3} \|',x)];assert len(lines)==len(records)==37 and len({int(x.split('|')[1].strip()) for x in lines})==37
for line in lines:
 cells=[x.strip() for x in line.strip('|').split('|')];per,role,recon=records[int(cells[0])];got={rows[per][f'z{i}'] for i in range(1,7)};need=[[role['top']],[role['A'],role['B']],[role['A'],role['C'],role['D']]];n=0
 for i,s in enumerate(need):
  hit=''.join(z for z in s if z in got) or '—';miss=''.join(z for z in s if z not in got) or '—';assert cells[i+2]==f"{''.join(s)} {sum(z in got for z in s)}/{len(s)}（中{hit}；缺{miss}）";n+=all(z in got for z in s)
 assert cells[5]==str(n) and (('结果已知后重建' in cells[1])==recon)
ck(True,'111 columns across 34 stored versions and three separately marked reconstructions independently re-settled')
zcells={x.split('|')[1].strip():[y.strip() for y in x.strip('|').split('|')] for x in text.splitlines() if re.match(r'^\| [鼠牛虎兔龍蛇馬羊猴鷄狗豬] \|',x)};assert set(zcells)==set(Z);N=lambda r:[int(r[f'n{i}']) for i in range(1,7)];zof=lambda n:Z[(7-n)%12]
for z,c in zcells.items():
 nums=[n for n in range(1,50) if zof(n)==z];age=next(i for i,r in enumerate(history) if any(n in nums for n in N(r)));ws=[]
 for w in (35,40,45):
  sub=[N(r) for r in history[:w]];ws.append(f"{sum(any(n in nums for n in a) for a in sub)}/{sum(sum(n in nums for n in a) for a in sub)}")
 assert c[1]==' '.join(f'{n:02}' for n in nums) and c[2]==str(age) and c[3]=='；'.join(ws)
ck(True,'all 12 zodiac groups, ages and overlapping window period/ball counts reproduced')
numlines=[x for x in text.splitlines() if re.match(r'^\| \d{2} \|',x)];assert len(numlines)==49;red={1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46};blue={3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48}
for line in numlines:
 c=[x.strip() for x in line.strip('|').split('|')];n=int(c[0]);age=next(i for i,r in enumerate(history) if n in N(r));wave='紅' if n in red else '藍' if n in blue else '綠';assert c[1]==zof(n) and c[3:9]==[str(n%3),'奇' if n%2 else '偶',wave,str(n//10),str(n%10),str(age)] and c[9]=='／'.join(str(sum(n in N(r) for r in history[:w])) for w in (35,40,45))
ck(True,'all 49 number identities, structural attributes, ages and window counts checked')
for x in aud['candidates']:
 rr=x['roles'];p=x['ideal_model']['percent'];prefix=f"| {x['id']} | {rr['top']} | {rr['A']+rr['B']} | {rr['A']+rr['C']+rr['D']} | {'、'.join(x['reserves'])} | {p['all_columns']:.4f}% | {p['no_complete_column']:.4f}% |";assert prefix in text
for x in rev['candidate_counterfactuals']:
 rr=x['roles'];prefix=f"| {x['id']} | {rr['top']}／{rr['A']+rr['B']}／{rr['A']+rr['C']+rr['D']} | {x['single_hits']}/1 | {x['pair_hits']}/2 | {x['triple_hits']}/3 | {x['complete_columns']} |";assert prefix in text
ck(len(aud['candidates'])==len(rev['candidate_counterfactuals'])==12,'12 proposed comparisons and 12 prior alternatives settled only after result, exact roles and counts')
g=J(Q/'six_sign_repeat_study.json')['groups']['2024plus'];assert g['n']==132 and g['six_to_six_counts_0_to_6']==[2,9,45,47,26,3,0] and g['seven_to_seven_counts_0_to_6']==[0,3,33,54,35,6,1] and '| 前六对前六 | 2 | 9 | 45 | 47 | 26 | 3 | 0 |' in text and '| 七球对七球 | 0 | 3 | 33 | 54 | 35 | 6 | 1 |' in text
assert all(x in text for x in ('13/17/3/1','13/35、16/40、17/45','10/14/16','40.9686%','1.6585%','二鷄龍 | 46鷄，1/2','不是未来胜率','没有任何方案可以保证下期命中','这不是328号码'))
ck(True,'327 root cause, historic counts, conditional study, model tradeoff and limitations present')
for link in re.findall(r'\]\(([^)]+)\)',text):assert not link.startswith(('http://','https://')) and (R/link).is_file(),link
ck(True,'all local report evidence links resolve')
# The old arithmetic QC passed but did not check the semantics of the reference date.
frozen=R/'archive/task295_328_release/date_correction/originals/unverified-328-local-report.md';old=frozen.read_text();heading='## 一、327：先确认中了什么、缺了什么';assert H(frozen)=='05c548c6358bbb4f6f62adeacd1bc2a2f97df32db03f53b0c804a3cab7648cdb' and old.split(heading,1)[1]==text.split(heading,1)[1] and '历史资料部分日期与参考时间不一致' not in text and '日期措辞更正' in text and '历史资料部分日期缺失' in text
pause=J(R/'archive/task295_328_release/date_correction/originals/unverified-327-public-pause.json');assert pause['reference_local_date']=='2026-10-13' and pause['runtime_clock_utc_observation'].startswith('2026-11-22') and pause['third_party_http_date_header'].startswith('Sun, 22 Nov 2026') and len(pause['future_dated_records'])==26 and pause['future_dated_records'][0]['recorded_date']=='2026-10-14' and pause['future_dated_records'][-1]['recorded_date']=='2026-11-08'
assert all(rows[p]['date']=='' for p in range(2026313,2026328));notice=(R/'archive/task295_328_release/date_correction/日期措辞更正.md').read_text();assert all(s in notice for s in ('10月13日','11月22日','撤回','不能证明赛前','不能保证命中或收益'))
ck(True,'corrected date wording explicitly addresses conflicting reference clocks, identifies 15 undated records and leaves all numerical body text unchanged')
out={'status':'PASS','scope':'corrected report arithmetic, provenance and local links only; clocks, official source, predraw timing, real mechanism or prediction not certified','checks':checks,'report_sha256':H(report),'preserved_initial_report_sha256':H(frozen)};p=Q/'report_corrected_independent_qc.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
