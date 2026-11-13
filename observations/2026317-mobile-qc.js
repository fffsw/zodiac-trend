#!/usr/bin/env node
'use strict';
// Chromium mobile emulation, not real iOS Safari or a WeChat safety verdict. The future local row is synthetic only.
const {chromium,devices}=require('playwright'),fs=require('fs');const url=process.argv[2],out=process.argv[3];if(!url||!out)throw Error('URL and fresh result path required');
(async()=>{const b=await chromium.launch({headless:true,args:['--no-sandbox']});const ctx=await b.newContext({...devices['iPhone 13'],locale:'zh-CN',timezoneId:'Asia/Shanghai'}),p=await ctx.newPage(),errors=[],requests=[],checks=[];p.on('pageerror',e=>errors.push(String(e)));p.on('request',r=>requests.push({url:r.url(),type:r.resourceType()}));const check=(x,m)=>{if(!x)throw Error('FAIL '+m);checks.push(m)};const text=async s=>(await p.locator(s).innerText()).replace(/\s+/g,'');
 await p.goto(url,{waitUntil:'load',timeout:45000});
 check(await p.evaluate(()=>/iPhone/.test(navigator.userAgent)&&matchMedia('(pointer:coarse)').matches),'mobile viewport, iPhone-style user agent and touch emulated');
 check(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'mobile page fits viewport; graph has own horizontal scrolling');
 check(await p.locator('#source-risk-notice').count()===0,'no added banner on mobile');check((await p.locator('#count').innerText())==='第 2026317 期','mobile issue is 317');
 check(await p.evaluate(()=>{let e=document.querySelector('#sc');return e.scrollWidth>e.clientWidth}),'mobile graph horizontally scrollable');
 check(await p.evaluate(()=>{let e=document.querySelector('#sc');e.scrollLeft=e.scrollWidth;return e.scrollLeft>0}),'mobile graph reaches right side');
 await p.locator('#t-zod').tap();check(await p.evaluate(()=>VIEW)==='zod','touch switches to zodiac view');await p.locator('[data-n="50"]').tap();check(await p.locator('#grid tbody tr').count()===50,'touch switches to 50 periods');await p.locator('#t-num').tap();check(await p.evaluate(()=>VIEW)==='num','touch switches back to number view');
 for(const [id,v] of [['btnMaxZod','单肖展示狗'],['btnE22','二中二兔豬'],['btnT33','三中三兔馬牛']]){await p.locator('#'+id).tap();check(await text('#entOut')===v,'touch '+v)}
 await p.locator('#drawIn').fill('1 2 3 4 5 6');await p.locator('#drawSp').fill('7');await p.locator('#btnDraw').tap();check((await p.evaluate(()=>ALL.at(-1)[0]))===2026317&&(await p.locator('#count').innerText())==='第 2026318 期','synthetic local 317 fixture updates identifier');check((await text('#entOut')).includes('待人工定案'),'no automatic 318 picks from synthetic 317');
 await p.locator('#btnUndoDraw').tap();check((await p.evaluate(()=>ALL.at(-1)[0]))===2026316&&(await p.locator('#count').innerText())==='第 2026317 期','undo synthetic fixture restores 317 identifier');check(await p.evaluate(()=>localStorage.getItem('zt_extra'))===null,'no synthetic record left in mobile context');
 check(requests.every(r=>r.type==='document'),'no automatically loaded external scripts or assets');check(errors.length===0,'no unhandled mobile browser errors');
 const result={status:'PASS',scope:'Chromium mobile emulation only, not real iOS Safari or a WeChat safety decision',url,browser:b.version(),checks,errors,requests};fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify(result,null,2));await ctx.close();await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
