#!/usr/bin/env python3
"""Status-only gate for target 315; intentionally never materialize draw values.

The target stream stops on the FIRST character of a non-null `data` value,
before its contents. For latest, this parser discards every non-`expect` value
as a stream, without assembling, decoding or recording it; only the first
issue identifier is extracted. A network buffer may still receive more bytes.
Null is not proof of predraw time or source authenticity.
"""
from pathlib import Path
import json,time,sys,requests
P=Path('/home/user/archive/task262_315_release/analysis/prepush_status_only.json')
class Stream:
 def __init__(self,it):self.it=iter(it);self.held=None;self.consumed=0
 def get(self):
  if self.held is not None:x=self.held;self.held=None;return x
  x=next(self.it);self.consumed+=1
  if self.consumed>500000:raise ValueError('status stream too long')
  return x.decode('latin1') if isinstance(x,bytes) else x
 def push(self,x):
  if self.held is not None:raise ValueError('bad pushback')
  self.held=x
 def ws(self):
  x=self.get()
  while x in ' \r\n\t':x=self.get()
  return x
 def string(self,keep):
  out=[]
  while True:
   x=self.get()
   if x=='"':return ''.join(out) if keep else None
   if x=='\\':
    y=self.get()
    if keep:raise ValueError('escaped key or identifier')
   elif keep:
    if len(out)>=100:raise ValueError('long key or identifier')
    out.append(x)
 def skip(self,first):
  # Read characters only for JSON delimiters/escaping; never assemble a value.
  if first=='"':self.string(False);return
  if first in '[{':
   stack=[first];quoted=False;escaped=False
   while stack:
    x=self.get()
    if quoted:
     if escaped:escaped=False
     elif x=='\\':escaped=True
     elif x=='"':quoted=False
    elif x=='"':quoted=True
    elif x in '[{':stack.append(x)
    elif x in ']}':
     if (stack[-1],x) not in (('[',']'),('{','}')):raise ValueError('unbalanced non-status value')
     stack.pop()
   return
  x=first
  while x not in ',}]':x=self.get()
  self.push(x)
 def number_or_string_digits(self,first):
  if first=='"':v=self.string(True)
  else:
   a=[];x=first
   while x not in ',}] \r\n\t':
    if len(a)>20:raise ValueError('status scalar too long')
    a.append(x);x=self.get()
   self.push(x);v=''.join(a)
  if not v.isdigit():raise ValueError('status scalar is not digits')
  return int(v)
 def key(self):
  if self.ws()!='"':raise ValueError('expected object key')
  k=self.string(True)
  if self.ws()!=':':raise ValueError('expected colon')
  return k
 def member_end(self):
  x=self.ws()
  if x not in ',}':raise ValueError('expected comma/object end')
  return x

def target_stream(it):
 s=Stream(it)
 if s.ws()!='{':raise ValueError('target root not object')
 code=None;is_null=None
 while True:
  k=s.key();v=s.ws()
  if k=='data':
   if v!='n':return {'target_record_is_null':False,'value_content_bytes_consumed':0,'target_code':code}
   if ''.join(s.get() for _ in range(3))!='ull':raise ValueError('invalid null')
   is_null=True
  elif k=='code':code=s.number_or_string_digits(v)
  else:s.skip(v)
  end=s.member_end()
  if end=='}':break
 if is_null is not True or code!=0:raise ValueError('unexpected target status schema')
 return {'target_record_is_null':True,'value_content_bytes_consumed':0,'target_code':code}

def latest_stream(it):
 s=Stream(it)
 if s.ws()!='[' or s.ws()!='{':raise ValueError('latest must be array with an object')
 while True:
  k=s.key();v=s.ws()
  if k=='expect':return {'latest_issue_identifier':s.number_or_string_digits(v)}
  s.skip(v)
  if s.member_end()=='}':raise ValueError('latest object has no issue identifier')

def onebytes(b):return (bytes([x]) for x in b)
def selftest():
 assert target_stream(onebytes(b'{"code":0,"data":null}'))['target_record_is_null'] is True
 prefix=b'{"code":0,"data":{';secret=b'"numbers":[1,2,3,4,5,6]}}';it=iter(onebytes(prefix+secret));out=target_stream(it);assert not out['target_record_is_null'] and next(it)==b'"' and out['value_content_bytes_consumed']==0
 x=b'[{"suit":[1,2,3,4,5,6],"opaque":{"result":"xx\\\"yy"},"expect":"2026314","other":[9]}]';assert latest_stream(onebytes(x))['latest_issue_identifier']==2026314
 print('PASS streaming status parser: aborts before present target contents; discards other latest fields; extracts issue identifier only')
if __name__=='__main__':
 if '--selftest' in sys.argv:selftest();sys.exit(0)
 assert not P.exists(),P
 result={'scope':'315 status-only; no draw-value materialization, printing, or saving; not official or predraw authentication','target_nonnull_content_bytes_consumed':0,'latest_nonstatus_values_discarded_without_assembly':True,'may_be_stale_or_share_upstream':True,'observations':{}}
 try:
  for name,url in [('target','https://history.macaumarksix.com/history/macaujc2/expect/2026315'),('latest','https://macaumarksix.com/api/macaujc2.com')]:
   resp=requests.get(url,params={'_task262_status_only':time.time_ns()},headers={'Cache-Control':'no-cache, no-store','Pragma':'no-cache'},timeout=20,stream=True);resp.raise_for_status()
   try:
    data=(target_stream if name=='target' else latest_stream)(resp.iter_content(chunk_size=1));entry={'http_status':resp.status_code,'server_date_header':resp.headers.get('Date'),'url':url,**data};result['observations'][name]=entry
   finally:resp.close()
   if name=='target' and not data['target_record_is_null']:break
  if not result['observations']['target']['target_record_is_null'] or result['observations'].get('latest',{}).get('latest_issue_identifier')!=2026314:
   result['status']='TARGET_PRESENT_OR_LATEST_ANOMALY_PAUSE';code=2
  else:result['status']='NO_TARGET_RECORD_OBSERVED_NOT_PROOF_OF_PRE_DRAW';code=0
 except Exception as ex:
  result['status']='STATUS_UNKNOWN_PAUSE_NO_PREDRAW_CLAIM';result['error_type']=type(ex).__name__;code=3
 P.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(code)
