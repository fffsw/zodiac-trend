#!/usr/bin/env node
'use strict';
// Chromium UI / localStorage tests. Synthetic 314/315 rows are test fixtures,
// not results. The same script can run a local file or the public HTTPS URL.
const {chromium}=require('playwright');const {pathToFileURL}=require('url');const fs=require('fs'),crypto=require('crypto'),path=require('path');
const input=process.argv[2],out=process.argv[3];if(!input)throw Error('page input required');const url=/^https?:/.test(input)?input:pathToFileURL(path.resolve(input)).href;
const ok=(x,m)=>{if(!x)throw Error(m)};
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});const ctx=await browser.newContext({viewport:{width:1440,height:900},locale:'zh-CN',timezoneId:'Asia/Shanghai'});const p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));let checks=[];const check=(v,m)=>{ok(v,m);checks.push(m)};const txt=async s=>(await p.locator(s).innerText()).replace(/\s+/g,'');
 await p.goto(url,{waitUntil:'load',timeout:45000});
 check((await p.locator('#source-risk-notice').innerText()).includes('314赛前未核实、无预注册'),'314 no authenticated predraw or prereg claim');
 check((await p.locator('#source-risk-notice').innerText()).includes('来源与机制未认证')&&(await p.locator('#source-risk-notice').innerText()).includes('谨防博彩诈骗'),'source mechanism and fraud notice');
 check((await p.locator('#source-risk-notice a').nth(1).getAttribute('href')).endsWith('2026314-analysis.md'),'314 analysis link');
 check((await p.locator('#source-risk-notice a').last().getAttribute('href')).endsWith('2026312-page.html'),'312 original page link');
 check((await p.locator('#source-risk-notice').innerText()).length<130&&(await p.locator('#source-risk-notice').boundingBox()).height<60,'desktop concise risk notice');
 check(await p.evaluate(()=>document.body.firstElementChild.classList.contains('topseal')&&document.body.children[1].id==='source-risk-notice'&&document.body.children[2].tagName==='HEADER'),'original layout retained');
 check((await p.locator('#entBox b').innerText()).includes('314人工展示'),'target label 314');
 check((await p.locator('#footSrc').innerText()).includes('312、313用户号码')&&(await p.locator('#footSrc').innerText()).includes('313日期未知'),'user-only provenance and unknown date');
 check((await p.locator('.drawnote').innerText()).includes('旧本机日期可能只是录入时间'),'local dates not represented as draw dates');
 check((await p.locator('.legend').innerText()).includes('遗漏和近30期次数只计前六码'),'seventh ball omitted from six-ball stats');
 check((await p.locator('.entnote').innerText()).includes('不保证公平或收益'),'no fairness or returns claims');
 const initial=await p.evaluate(()=>({last:ALL.at(-1),previous:ALL.at(-2),count:ALL.length,mapping:DATA.n2z,decision:MANUAL_SITE_DECISIONS_V50['2026313']}));
 check(initial.count===250&&initial.last[0]===2026313&&initial.last[1]==='--/--'&&JSON.stringify(initial.last[2])===JSON.stringify([33,39,45,15,7,20])&&initial.last[4]===43,'embedded 313 exact user six+one with no invented date');
 check(initial.previous[0]===2026312&&initial.previous[2][0]===31,'correct 312 first ball preserved');
 check(await p.locator('#grid tbody tr').last().locator('td.per span').innerText()==='--/--','visible unknown date');
 const expected={U:[1,2,6,10,9,11],top:1,A:2,B:6,C:10,D:9,top_overlap_mode:'coverage'};
 check(JSON.stringify(initial.decision)===JSON.stringify(expected),'manual target fields exact');
 const noshake=await p.evaluate(()=>{
  const names=['entPicks_v25','entPicks_v30','entPicks_v40','entPicks_v41','entPicks_v42','poolTop6_v25','poolTop6_v40','poolTop6_v41','poolTop6_v42'];const old=Object.fromEntries(names.map(n=>[n,window[n]])),rand=Math.random;
  try{for(const n of names)window[n]=()=>{throw Error('legacy/random called '+n)};Math.random=()=>{throw Error('random called')};const v=entPicks(),u=poolTop6();return {top:v.top,t2:v.t2,t3:v.t3,pool:u.pool,cands:u.cands};}finally{for(const n of names)window[n]=old[n];Math.random=rand;}
 });
 check(JSON.stringify(noshake)===JSON.stringify({top:1,t2:[2,6],t3:[2,10,9],pool:[2,6,10,9,11],cands:[1,2,6,10,9]}),'no random/legacy algorithm path, display versus reserve exact');
 for(const [id,expect] of [['btnMaxZod','单肖展示牛'],['btnE22','二中二虎馬'],['btnT33','三中三虎狗鷄']]){await p.locator('#'+id).click();check(await txt('#entOut')===expect,'actual click '+id+' '+expect);}
 const scope=await p.evaluate(()=>{const last=ALL.at(-1),old=[last[4],last[5]],i=ALL.length-1;function bars(k){let v=VIEW;VIEW=k;let e=document.createElement('table');e.innerHTML='<tbody>'+statBarRow()+'</tbody>';VIEW=v;return [...e.querySelectorAll('.barbox b')].map(x=>+x.textContent)}const a=buildOmit('num'),b=buildOmit('zod'),nn=bars('num'),zz=bars('zod'),r=ALL.slice(-30);const correct=[...Array(49)].every((_,n)=>a[n+1][i]===i-ALL.map(x=>x[2].includes(n+1)).lastIndexOf(true)&&nn[n]===r.filter(x=>x[2].includes(n+1)).length)&&[...Array(12)].every((_,z)=>b[z+1][i]===i-ALL.map(x=>x[3].includes(z)).lastIndexOf(true)&&zz[z]===r.filter(x=>x[3].includes(z)).length);const before=JSON.stringify([a,b,nn,zz]);last[4]=42;last[5]=DATA.n2z[42];const after=JSON.stringify([buildOmit('num'),buildOmit('zod'),bars('num'),bars('zod')]);last[4]=old[0];last[5]=old[1];return{correct,independent:before===after}});
 check(scope.correct,'49/12 omission and last-30 bars independently recounted');check(scope.independent,'changing seventh ball does not alter normal statistics');
 let msg=await p.locator('#count').innerText();check(msg.includes('排期未核实')&&!msg.includes('21:30'),'no invented sales cutoff');
 for(const n of [50,100,250]){await p.locator(`[data-n="${n}"]`).click();check(await p.locator('#grid tbody tr').count()===n,`${n}-period view`);}
 await p.locator('#t-zod').click();check(await p.locator('#grid tbody tr').count()===250,'zodiac view');await p.locator('#t-num').click();
 let ct=await p.locator('tr.pred').count();await p.locator('#btnAdd').click();check(await p.locator('tr.pred').count()===ct+1,'add prediction row');await p.locator('#btnDel').click();check(await p.locator('tr.pred').count()===ct,'delete prediction row');
 async function entry(n,s){await p.locator('#drawIn').fill(n);await p.locator('#drawSp').fill(s);await p.locator('#btnDraw').click();return{text:await p.locator('#drawMsg').innerText(),end:await p.evaluate(()=>ALL.at(-1)[0]),storage:await p.evaluate(()=>localStorage.getItem('zt_extra'))};}
 for(const [label,n,s] of [['duplicate normals','1 1 2 3 4 5','7'],['invalid token','1 2 3 4 5 6 nope','7'],['special token','1 2 3 4 5 6','7 nope'],['out of range','1 2 3 4 5 50','7'],['special overlap','1 2 3 4 5 6','2'],['too few normals','1 2 3 4 5','7']]){let q=await entry(n,s);check(q.end===2026313&&q.storage===null&&q.text.length>0,'reject '+label+' without storage mutation');}
 let q=await entry('1 2 3 4 5 6','7');check(q.end===2026314&&q.text.includes('已录入'),'synthetic local 314 row accepted');
 check((await p.evaluate(()=>ALL.at(-1)[1]))==='--/--','synthetic local entry uses unknown date, not computer date');
 check((await txt('#entOut')).includes('待人工定案')&&(await txt('#entOut')).includes('不摇号'),'315 has no automatic selection');
 await p.reload({waitUntil:'load'});check((await p.evaluate(()=>ALL.at(-1)[0]))===2026314&&(await p.locator('#drawMsg').innerText()).includes('恢复'),'synthetic local 314 survives reload');
 await p.locator('#btnUndoDraw').click();check((await p.evaluate(()=>ALL.at(-1)[0]))===2026313&&await p.evaluate(()=>localStorage.getItem('zt_extra'))===null,'undo synthetic 314 only');
 // A legacy 313 local entry matches the new base numbers, but its old client
 // entry date is not accepted as the embedded draw date or destroyed.
 const legacy=JSON.parse(JSON.stringify(initial.last));legacy[1]='11/09';const legacyRaw=JSON.stringify([legacy]);await p.evaluate(v=>localStorage.setItem('zt_extra',v),legacyRaw);await p.reload({waitUntil:'load'});
 check((await p.evaluate(()=>ALL.at(-1)[1]))==='--/--'&&(await p.evaluate(()=>ALL.at(-1)[0]))===2026313,'unknown canonical date retained despite local legacy date');
 check((await p.locator('#drawMsg').innerText()).includes('本机原日期保留')&&await p.evaluate(()=>localStorage.getItem('zt_extra'))===legacyRaw,'matching local row is retained with date caveat');
 q=await entry('1 2 3 4 5 6','7');let st=await p.evaluate(()=>JSON.parse(localStorage.getItem('zt_extra')));check(st.length===2&&JSON.stringify(st[0])===JSON.stringify(legacy)&&st[1][0]===2026314&&st[1][1]==='--/--','append preserves full legacy 313 and new unknown date');
 await p.locator('#btnUndoDraw').click();check(await p.evaluate(()=>localStorage.getItem('zt_extra'))===legacyRaw,'undo preserves legacy date byte-for-byte');
 const z=n=>initial.mapping[String(n)];const conflict=JSON.parse(JSON.stringify(legacy));conflict[2][0]=34;conflict[3][0]=z(34);const conflictRaw=JSON.stringify([conflict]);await p.evaluate(v=>localStorage.setItem('zt_extra',v),conflictRaw);await p.reload({waitUntil:'load'});
 check((await p.evaluate(()=>ALL.at(-1)[2][0]))===33&&(await p.locator('#drawMsg').innerText()).includes('不一致'),'conflicting 313 numbers do not replace source');
 q=await entry('1 2 3 4 5 6','7');check(q.end===2026313&&q.storage===conflictRaw&&q.text.includes('暂停'),'conflicting 313 preserved and append blocked');await p.locator('#btnUndoDraw').click();check(await p.evaluate(()=>localStorage.getItem('zt_extra'))===conflictRaw,'conflicting 313 preserved on undo');
 const wrongDate=JSON.parse(JSON.stringify(initial.previous));wrongDate[1]='10/13';const wrongDateRaw=JSON.stringify([wrongDate]);await p.evaluate(v=>localStorage.setItem('zt_extra',v),wrongDateRaw);await p.reload({waitUntil:'load'});check((await p.locator('#drawMsg').innerText()).includes('不一致')&&await p.evaluate(()=>localStorage.getItem('zt_extra'))===wrongDateRaw,'known base date mismatch not silently reconciled');
 const synthetic=[2026314,'--/--',[1,2,3,4,5,6],[1,2,3,4,5,6].map(z),7,z(7)],bad=[2026315,'--/--',[1,1,2,3,4,5],[1,1,2,3,4,5].map(z),7,z(7)];const partialRaw=JSON.stringify([legacy,synthetic,bad]);await p.evaluate(v=>localStorage.setItem('zt_extra',v),partialRaw);await p.reload({waitUntil:'load'});
 check((await p.evaluate(()=>ALL.at(-1)[0]))===2026313&&(await p.locator('#drawMsg').innerText()).includes('异常'),'invalid later local row causes transactional all-or-nothing restore');
 check(await p.evaluate(()=>localStorage.getItem('zt_extra'))===partialRaw,'transaction failure preserves all original local bytes');
 await p.evaluate(()=>localStorage.setItem('zt_extra','{bad json'));await p.reload({waitUntil:'load'});check((await p.locator('#drawMsg').innerText()).includes('异常')&&await p.evaluate(()=>localStorage.getItem('zt_extra'))==='{bad json','malformed JSON preserved and blocked');
 await p.evaluate(()=>localStorage.removeItem('zt_extra'));await p.reload({waitUntil:'load'});await p.setViewportSize({width:390,height:844});await p.locator('#btnMaxZod').click();
 check(await txt('#entOut')==='单肖展示牛','mobile layout and button');check(await p.locator('#source-risk-notice').isVisible()&&(await p.locator('#source-risk-notice').boundingBox()).height<120,'mobile compact risk notice');
 check(errors.length===0,'no unhandled page errors');const result={status:'PASS_NONOFFICIAL_NOT_A_PREDRAW_CERTIFICATE',scope:'314 original-style release; synthetic local fixtures only',url,browser:browser.version(),checks,errors};if(out)fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify(result,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
