#!/usr/bin/env node
'use strict';
// Real Chromium QA for the exact nonofficial release candidate; synthetic input only.
const {chromium}=require('playwright');
const path=require('path'),crypto=require('crypto');
const {pathToFileURL}=require('url');
const fs=require('fs');
const f=path.resolve(process.argv[2]||path.join(__dirname,'2026313-page.html'));
const out=process.argv[3]||null;
const A=(x,msg)=>{if(!x)throw Error(msg)};
(async()=>{
 const b=await chromium.launch({headless:true,args:['--no-sandbox']});
 const ctx=await b.newContext({viewport:{width:1440,height:900},locale:'zh-CN',timezoneId:'Asia/Shanghai'});
 const p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));
 await p.goto(pathToFileURL(f).href,{waitUntil:'load'});
 const r={scope:'Exact user-authorized nonofficial display release candidate; no authentication of draw or time; inputs synthetic',browser:'Chromium '+b.version(),page_sha256:crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'),checks:[],errors};
 const check=(x,m)=>{A(x,m);r.checks.push(m)};
 const txt=async sel=>(await p.locator(sel).innerText()).replace(/\s+/g,'');
 check(await p.locator('#offline-only-warning').count()===0,'release candidate carries no misleading offline-only notice');
 check((await p.locator('#source-risk-notice').innerText()).includes('是否赛前未经独立证实')&&(await p.locator('#source-risk-notice').innerText()).includes('不提供赛前预注册'),'explicit no verified predraw / no prereg warning');
 check((await p.locator('#entBox b').innerText()).includes('313非官方人工展示'),'display 313 labelled nonofficial');
 check((await p.locator('h1').innerText()).includes('非官方资料走势'),'headline labels the data nonofficial');
 check((await p.locator('#source-risk-notice').innerText()).includes('司法警察局2024年')&&(await p.locator('#source-risk-notice').innerText()).includes('非官方'),'government warning and source limitations visible');
 check((await p.locator('.entnote').innerText()).includes('不能保证随机、公平或收益'),'fairness model caveat visible');
 check((await p.locator('#footSrc').innerText()).includes('用户提供号码'),'user-supplied numbers provenance visible');
 check((await txt('#h1sub')).includes('2026312'),'embedded history ends at user-supplied 312');
 const initial=await p.evaluate(()=>({last:ALL.at(-1),count:ALL.length,mapping:DATA.n2z}));
 check(initial.count===250&&JSON.stringify(initial.last[2])===JSON.stringify([31,46,4,43,32,15])&&initial.last[4]===38,'312 six-plus-one exact in browser');

 check((await p.locator('.legend').innerText()).includes('只按前六个记录号码计算'),'visible six-normal-only omission/30-count scope');
 const sixTests=await p.evaluate(()=>{
   const view=VIEW, row=ALL.at(-1),old=[row[4],row[5]];
   const omitN=buildOmit('num'),omitZ=buildOmit('zod'),last=ALL.length-1;
   let omitOK=true;
   for(let n=1;n<=49;n++){
     const ix=ALL.map(r=>r[2].includes(n)).lastIndexOf(true);
     if(omitN[n][last]!==ALL.length-1-ix)omitOK=false;
   }
   for(let z=0;z<12;z++){
     const ix=ALL.map(r=>r[3].includes(z)).lastIndexOf(true);
     if(omitZ[z+1][last]!==ALL.length-1-ix)omitOK=false;
   }
   function barData(kind){
     VIEW=kind;const box=document.createElement('table');box.innerHTML='<tbody>'+statBarRow()+'</tbody>';
     return [...box.querySelectorAll('td .barbox b')].map(x=>+x.textContent);
   }
   const nbar=barData('num'),zbar=barData('zod'),thirty=ALL.slice(-30);
   let barOK=nbar.every((x,i)=>x===thirty.filter(r=>r[2].includes(i+1)).length)
     &&zbar.every((x,i)=>x===thirty.filter(r=>r[3].includes(i)).length);
   const before=JSON.stringify({n:omitN,z:omitZ,nb:nbar,zb:zbar});
   row[4]=42;row[5]=DATA.n2z[42];
   const after=JSON.stringify({n:buildOmit('num'),z:buildOmit('zod'),nb:barData('num'),zb:barData('zod')});
   row[4]=old[0];row[5]=old[1];VIEW=view;
   return {omitOK,barOK,independent:before===after};
 });
 check(sixTests.omitOK,'all 49/12 omissions independently equal six-normal calculations');
 check(sixTests.barOK,'all 49/12 last-30 bars independently equal six-normal calculations');
 check(sixTests.independent,'changing seventh ball cannot change omissions or bars');
 const noshake=await p.evaluate(()=>{
   const names=['entPicks_v25','entPicks_v30','entPicks_v40','entPicks_v41','entPicks_v42','poolTop6_v25','poolTop6_v40','poolTop6_v41','poolTop6_v42'];
   const old=Object.fromEntries(names.map(n=>[n,window[n]])), rand=Math.random;
   try{for(const n of names)window[n]=()=>{throw Error('historical/random selection path called '+n)};Math.random=()=>{throw Error('Math.random called')};
     const x=entPicks(),p=poolTop6();return {top:x.top,t2:x.t2,t3:x.t3,pool:p.pool,cands:p.cands};
   }finally{for(const n of names)window[n]=old[n];Math.random=rand;}
 });
 check(JSON.stringify(noshake)==JSON.stringify({top:6,t2:[3,4],t3:[3,2,5],pool:[3,4,2,5,11],cands:[6,3,4,2,5]}),'v5.0 exact display with all older algorithm paths and Math.random blocked');
 const msg=await p.locator('#count').innerText();
 check(msg.includes('官方')&&!msg.includes('销售截止倒计时')&&!msg.includes('21:30'),'no unverified countdown or claimed cutoff');
 for(const [id,expected] of [['btnMaxZod','单肖展示馬'],['btnE22','二中二兔龍'],['btnT33','三中三兔虎蛇']]){
  await p.locator('#'+id).click();check(await txt('#entOut')===expected,'real click '+id+' '+expected);
 }
 await p.locator('[data-n="250"]').click();check(await p.locator('#grid tbody tr').count()===250,'250 displayed records');
 await p.locator('#t-zod').click();check(await p.locator('#grid tbody tr').count()===250,'zodiac view retains 250 records');
 await p.locator('#t-num').click();
 let rows=await p.locator('tr.pred').count();await p.locator('#btnAdd').click();check(await p.locator('tr.pred').count()===rows+1,'prediction row add');
 await p.locator('#btnDel').click();check(await p.locator('tr.pred').count()===rows,'prediction row delete');
 async function entry(normal,special){await p.locator('#drawIn').fill(normal);await p.locator('#drawSp').fill(special);await p.locator('#btnDraw').click();return {text:await p.locator('#drawMsg').innerText(),end:await p.evaluate(()=>ALL.at(-1)[0]),storage:await p.evaluate(()=>localStorage.getItem('zt_extra'))};}
 for(const [name,n,s] of [
  ['duplicate normals','1 1 2 3 4 5','7'],['invalid normal token','1 2 3 4 5 6 invalid','7'],
  ['invalid special token','1 2 3 4 5 6','7 nope'],['out-of-range number','1 2 3 4 5 6 50','7'],
  ['special overlap','1 2 3 4 5 6','2'],['too few normals','1 2 3 4 5','7'],
 ]){
  const q=await entry(n,s);check(q.end===2026312&&q.storage===null&&q.text.length>0,'reject '+name+' without mutation');
 }
 let q=await entry('1 2 3 4 5 6','7');
 check(q.end===2026313&&q.storage!==null&&q.text.includes('已录入'),'valid synthetic local row accepted');
 check((await txt('#entOut')).includes('待人工定案')&&(await txt('#entOut')).includes('不摇号'),'next period without decision fails closed');
 await p.reload({waitUntil:'load'});
 check((await p.evaluate(()=>ALL.at(-1)[0]))===2026313&&(await p.locator('#drawMsg').innerText()).includes('恢复'),'valid local row restored on reload');
 await p.locator('#btnUndoDraw').click();check((await p.evaluate(()=>ALL.at(-1)[0]))===2026312&&await p.evaluate(()=>localStorage.getItem('zt_extra'))===null,'undo restores 312 and clears only synthetic extra');
 // A previously recorded, byte-identical embedded row must not be discarded when writing a new row.
 await p.evaluate(row=>localStorage.setItem('zt_extra',JSON.stringify([row])),initial.last);await p.reload({waitUntil:'load'});
 check((await p.evaluate(()=>ALL.at(-1)[0]))===2026312,'matching embedded local row not duplicated');
 await entry('1 2 3 4 5 6','7');
 let stored=await p.evaluate(()=>JSON.parse(localStorage.getItem('zt_extra')));
 check(stored.length===2&&stored[0][0]===2026312&&stored[1][0]===2026313,'matching prior local record retained when appending');
 await p.locator('#btnUndoDraw').click();stored=await p.evaluate(()=>JSON.parse(localStorage.getItem('zt_extra')));
 check(stored.length===1&&stored[0][0]===2026312,'undo preserves prior matching local record');
 await p.evaluate(()=>localStorage.removeItem('zt_extra'));
 // Simulated legacy row with duplicated normal number must be quarantined, not used or overwritten.
 const z=n=>initial.mapping[String(n)];const invalid=[2026313,'11/09',[1,1,2,3,4,5],[1,1,2,3,4,5].map(z),7,z(7)];
 const raw=JSON.stringify([invalid]);await p.evaluate(v=>localStorage.setItem('zt_extra',v),raw);await p.reload({waitUntil:'load'});
 check((await p.evaluate(()=>ALL.at(-1)[0]))===2026312&&(await p.locator('#drawMsg').innerText()).includes('异常'),'malformed legacy row not added and warning visible');
 q=await entry('1 2 3 4 5 6','7');
 check(q.end===2026312&&q.storage===raw&&q.text.includes('暂停'),'malformed legacy row preserved; addition blocked');
 await p.locator('#btnUndoDraw').click();check(await p.evaluate(()=>localStorage.getItem('zt_extra'))===raw,'malformed legacy record not overwritten by undo');
 // Conflicting local 312 (old 34 version) must not replace canonical 31.
 const old=JSON.parse(JSON.stringify(initial.last));old[2][0]=34;old[3][0]=z(34);const oldRaw=JSON.stringify([old]);
 await p.evaluate(v=>localStorage.setItem('zt_extra',v),oldRaw);await p.reload({waitUntil:'load'});
 check((await p.evaluate(()=>ALL.at(-1)[2][0]))===31&&(await p.locator('#drawMsg').innerText()).includes('不一致'),'conflicting legacy local 312 not substituted');
 check(await p.evaluate(()=>localStorage.getItem('zt_extra'))===oldRaw,'conflicting legacy local 312 preserved');
 await p.evaluate(()=>localStorage.setItem('zt_extra','{bad json'));await p.reload({waitUntil:'load'});
 check((await p.locator('#drawMsg').innerText()).includes('异常')&&(await p.evaluate(()=>localStorage.getItem('zt_extra')))==='{bad json','malformed JSON preserved and blocked');
 await p.evaluate(()=>localStorage.removeItem('zt_extra'));await p.reload({waitUntil:'load'});
 await p.setViewportSize({width:390,height:844});await p.locator('#btnMaxZod').click();
 check(await txt('#entOut')==='单肖展示馬','mobile-sized viewport renders and button works');
 check(errors.length===0,'no unhandled browser page errors');
 r.status='PASS_UNVERIFIED_DISPLAY_CANDIDATE_NOT_A_PREDRAW_CERTIFICATE';if(out)fs.writeFileSync(out,JSON.stringify(r,null,2)+'\n',{flag:'wx'});
 console.log(JSON.stringify(r,null,2));await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
