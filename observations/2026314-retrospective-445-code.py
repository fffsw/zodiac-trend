#!/usr/bin/env python3
"""Extend the frozen exact seven-ball 4/4/5 historical scan with user 314 only."""
from pathlib import Path
from collections import Counter
import csv,json,hashlib
R=Path('/home/user');A=R/'archive/task261_314_failure_review';B=A/'before';O=A/'analysis';src=R/'data/task260_314_release/observations/2026314-445-source-through-311.csv'
with src.open(encoding='utf8',newline='') as f:old=list(csv.DictReader(f))
with (B/'history-through-313.csv').open(encoding='utf8',newline='') as f:main=list(csv.DictReader(f))
u=json.loads((A/'input/user_314.json').read_text());assert len(old)==2492 and old[-1]['period']=='2026311' and [x['period'] for x in main[:2]]==['2026313','2026312']
rec=[{'period':x['period'],'signs':set(x['zodiacs'].split()) if x['usable']=='1' else None} for x in old]
for row in main[1::-1]:rec.append({'period':row['period'],'signs':set([row[f'z{i}'] for i in range(1,7)]+[row['special_zodiac']])})
rec.append({'period':'2026314','signs':set(u['normal_zodiacs']+[u['seventh_zodiac']])});counts=[None]+[len(a['signs']&b['signs']) if a['signs'] is not None and b['signs'] is not None else None for a,b in zip(rec,rec[1:])];events=[];invalid=0
for i in range(3,len(rec)):
 v=counts[i-2:i+1]
 if None in v:invalid+=1;continue
 if v==[4,4,5]:events.append({'periods':[rec[i-3]['period'],rec[i-2]['period'],rec[i-1]['period'],rec[i]['period']],'transition_counts':v,'follow_period':rec[i+1]['period'] if i+1<len(rec) else None,'follow_seven_repeat_count':counts[i+1] if i+1<len(rec) else None})
follow=Counter(x['follow_seven_repeat_count'] for x in events);assert len(rec)==2495 and invalid==8 and len(events)==9 and follow=={2:2,3:3,4:3,5:1} and counts[-6:]==[4,4,5,5,3,3]
out={'scope':'Each adjacent comparison is distinct zodiac identity intersection of seven balls; scan three consecutive comparisons exactly 4,4,5; identities may vary. User 314 date remains unknown.','frozen_source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'first_period':rec[0]['period'],'last_period':'2026314','period_records':len(rec),'candidate_three_transition_windows':len(rec)-3,'invalid_candidate_windows':invalid,'valid_candidate_windows':len(rec)-3-invalid,'events':events,'known_followup_count':9,'followup_counts':dict(follow),'last_six_adjacent_repeat_counts':counts[-6:],'limitations':'2020 first 66 single source with date/zodiac doubts; two bad records and 8 windows excluded; sources not official; no forecast'}
p=O/'repeat_445.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS: 2,495 history rows, 2,484/2,492 445 windows valid, nine followups; last overlaps 4/4/5/5/3/3; no prediction')
