#!/usr/bin/env python3
"""Preserve supplied conversation date and observed clock headers without reconciling them."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import hashlib,json
R=Path('/home/user');Q=R/'archive/task273_318_release/analysis';p=Q/'time_discrepancy_receipt.json';assert not p.exists();now=datetime.now(timezone.utc);headers={}
for n in ('initial','prepush'):
 j=json.loads((Q/f'{n}_status_only.json').read_text());headers[n]={k:v.get('server_date_header') for k,v in j['observations'].items()}
prior=R/'archive/task272_317_failure_review/before/previous-clock-discrepancy.json'
out={'status':'CLOCK_DISCREPANCY_NOT_CALIBRATED','supplied_session_local_date':'2026-10-13','supplied_session_timezone':'Asia/Shanghai','runtime_clock_utc_raw':now.isoformat(),'runtime_clock_asia_shanghai_raw':now.astimezone(ZoneInfo('Asia/Shanghai')).isoformat(),'third_party_http_date_headers_raw_utc':headers,'earlier_receipt_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),'earlier_receipt_preserved':True,'scope':'Supplied session date and raw observed runtime/server dates differ. Do not infer actual draw time, official source, chronology or predraw status; user input 317 date remains unknown. Git commit timestamps inherit runtime clock and are not timing proof. The cause is not calibrated here.'};p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
