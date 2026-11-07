#!/usr/bin/env python3
"""Read archived source bytes and independently validate the correction copy."""
from pathlib import Path
import csv,gzip,hashlib,json,re
from bs4 import BeautifulSoup
R=Path('/home/user');D=R/'data';MANIFEST=D/'task242_historical_source_reconciliation.json';m=json.loads(MANIFEST.read_text());assert m['result']=='TASK242_FULL_HISTORY_RECONCILIATION PASS'
sha=lambda b:hashlib.sha256(b).hexdigest();raw={}
for k,v in m['sources'].items():
 g=(R/v['path']).read_bytes();assert sha(g)==v['gzip_sha256'];b=gzip.decompress(g);assert sha(b)==v['raw_sha256'] and len(b)==v['raw_bytes'];raw[k]=b
original=D/'macau_mark_six_full.csv';copy=D/'task242_1042_reconciled_history.csv';assert hashlib.md5(original.read_bytes()).hexdigest()==m['source_csv_md5']=='088592290c52e7079c1ec07d43474204'
assert hashlib.md5(copy.read_bytes()).hexdigest()==m['corrected_csv_md5'] and sha(copy.read_bytes())==m['corrected_csv_sha256']
a={r['period']:r for r in csv.DictReader(original.open(encoding='utf-8-sig'))};b={r['period']:r for r in csv.DictReader(copy.open(encoding='utf-8-sig'))};assert len(a)==len(b)==1042 and set(a)==set(b)
norm=lambda z:z.replace('雞','鷄').replace('鸡','鷄').replace('马','馬').replace('龙','龍').replace('猪','豬')
W={'red':'红','blue':'蓝','green':'绿'}
for y in (2024,2025,2026):
 v=json.loads(raw[f'api_{y}']);inside=[x for x in v['data'] if x['expect'].startswith(str(y))];assert len(inside)==m['api_year_extra_records_removed_after_year_filter'][str(y)]['matching_year_rows']
 for x in inside:
  p=x['expect'];r=b[p];ns=[int(r[f'n{i}']) for i in range(1,7)]+[int(r['special'])];zs=[r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']];ws=[r[f'w{i}'] for i in range(1,7)]+[r['special_wave']]
  assert ns==list(map(int,x['openCode'].split(','))) and zs==[norm(t) for t in x['zodiac'].split(',')] and ws==[W[t] for t in x['wave'].split(',')] and r['date']==x['openTime'][:10]
 soup=BeautifulSoup(raw[f'newmc_{y}'],'html.parser');tb=soup.select('table')
 # Number and zodiac tables are the 4th and 5th complete tables; validate headers/IDs.
 assert [td.get_text(strip=True) for td in tb[3].select('tr')[0].select('td')]==['期号','一','二','三','四','五','六','特','日期']
 assert len(tb[3].select('tr'))==len(inside)+1 and len(tb[4].select('tr'))==len(inside)+1
 for n,z in zip(tb[3].select('tr')[1:],tb[4].select('tr')[1:]):
  ns=[x.get_text(strip=True) for x in n.select('td')];zs=[x.get_text(strip=True) for x in z.select('td')];assert len(ns)==len(zs)==9 and ns[0]==zs[0] and ns[-1]==zs[-1]
  r=b[ns[0]];assert list(map(int,ns[1:8]))==[int(r[f'n{i}']) for i in range(1,7)]+[int(r['special'])]
  assert [norm(t) for t in zs[1:8]]==[r[f'z{i}'] for i in range(1,7)]+[r['special_zodiac']] and ns[-1]==r['date']
for y in (2025,2026):
 soup=BeautifulSoup(raw[f'181649_{y}'],'html.parser');seen={}
 for link in soup.select(f'a[href^="/history/{y}-"]'):
  st=link.find('strong');span=link.find('span')
  if not st or not span:continue
  mm=re.fullmatch(r'(\d{7})期',st.get_text(strip=True))
  if not mm:continue
  seen[mm.group(1)]=[int(t) for t in span.get_text(strip=True).split('、')]
 assert len(seen)==m['third_year_index_numbers_verified'][str(y)]
 for p,v in seen.items():assert v==[int(b[p][f'n{i}']) for i in range(1,7)]+[int(b[p]['special'])]
changed={p for p in a if a[p]!=b[p]};assert sorted(changed)==m['modified_periods'] and len(changed)==7
for p in changed:
 rec=next(x for x in m['diffs'] if x['period']==p);diff={k:{'old':a[p][k],'reconciled':b[p][k]} for k in a[p] if a[p][k]!=b[p][k]};assert rec['changes']==diff
assert a['2024294']['date']=='2024-10-21' and b['2024294']['date']=='2024-10-20'
assert [int(a['2025031'][f'n{i}']) for i in range(1,7)]==[24,23,8,12,33,25]
assert [int(b['2025031'][f'n{i}']) for i in range(1,7)]==[30,23,8,24,33,25]
conf=m['kj_disagreements']['2025031']['display']['numbers'];assert conf==[24,23,8,24,33,25,22] and len(set(conf))<7
assert a['2026311']==b['2026311']
print('Archive gzip/raw SHA-256 and decompression verified for all captured sources PASS')
print('1042 reconciled records independently compared to API and second source date/numbers/identities PASS')
print('Third separately hosted display: 2025/26 numbers match 365+311 rows PASS; upstream independence unknown')
print('Seven pre-existing deviations preserved explicitly; 2025031 prior display repeated number 24 PASS')
print('Original CSV byte MD5 unchanged; 311 last row unchanged; copy SHA256='+sha(copy.read_bytes()))
print('RECONCILIATION_JSON_SHA256='+sha(MANIFEST.read_bytes()))
print('TASK242_HISTORY_RECONCILIATION_INDEPENDENT PASS')
