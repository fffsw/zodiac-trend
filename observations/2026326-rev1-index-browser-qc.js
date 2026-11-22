#!/usr/bin/env node
'use strict';
// Check revision index in desktop Chromium and mobile emulation; not real iOS or WeChat.
const {chromium,devices}=require('playwright'),{pathToFileURL}=require('url'),path=require('path'),fs=require('fs');
const input=process.argv[2],out=process.argv[3];if(!input||!out)throw Error('index input and fresh result path required');const url=/^https?:/.test(input)?input:pathToFileURL(path.resolve(input)).href;
(async()=>{const b=await chromium.launch({headless:true,args:['--no-sandbox']}),checks=[],errors=[];const ck=(v,m)=>{if(!v)throw Error('FAIL '+m);checks.push(m)};
for(const [name,opts] of [['desktop',{viewport:{width:1440,height:900}}],['mobile',devices['iPhone 13']]]){
 const c=await b.newContext({...opts,locale:'zh-CN'}),p=await c.newPage();p.on('pageerror',e=>errors.push(String(e)));await p.goto(url,{waitUntil:'load',timeout:45000});const body=(await p.locator('body').innerText()).replace(/\s+/g,'');
 ck(body.includes('325期四肖后，326期重肖怎么看？')&&body.includes('本期自身的生肖个数'),name+' clarified heading and own-issue distinct signs');
 ck(body.includes('下一期重肖理论上限4肖')&&body.includes('相似样本前六观察最大3肖·8/48')&&body.includes('相似样本七球观察最大4肖·2/48'),name+' theoretical and six/seven historical maxima distinguished');
 ck(body.includes('不代表重4不可能')&&body.includes('不是预测保证')&&body.includes('不能直接用于前六栏目结算'),name+' no historical ceiling or seventh-ball settlement fallacy');
 ck(body.includes('当前：单羊、二虎羊、三虎馬鷄')&&body.includes('龍蛇仅替补')&&body.includes('原版三栏为虎馬兔'),name+' exact revision, reserve only, original archive clearly distinguished');
 ck(body.includes('前六重0、1或2肖时三栏必不完整')&&body.includes('重3时还要恰好包含虎、馬、鷄')&&body.includes('不代表三栏全完'),name+' incomplete risks are visible');
 const cells=await p.locator('tbody tr').evaluateAll(rs=>rs.map(r=>[...r.children].map(x=>x.textContent.trim())));ck(JSON.stringify(cells)==JSON.stringify([['前六对前六','5','18','17','8','0'],['七球对七球','5','13','19','9','2']]),name+' 48-pair distributions');
 ck(body.includes('326实际结果未读取')&&body.includes('来源、赛前状态及实际开奖机制均未认证')&&body.includes('真实微信安全状态仍需真实微信客户端确认'),name+' provenance, target and WeChat limitations');
 ck(body.includes('无条件栏目完成概率相同')&&body.includes('不能证明预测能力提高'),name+' honest equal baseline comparison');
 ck(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),name+' layout fits viewport; table scrolls independently');
 ck(await p.locator('script,img,iframe,link[rel=stylesheet]').count()===0,name+' no external assets or scripts');
 const links=await p.locator('a').evaluateAll(as=>as.map(a=>a.getAttribute('href')));ck(links.length>=9&&links.every(x=>x&&!/^https?:/.test(x))&&links.includes('2026326-index.html')&&links.includes('2026326-rev1-analysis.md'),name+' local revised analysis and clearly archived original links');
 await c.close();}
ck(errors.length===0,'no browser errors');const result={status:'PASS',scope:'326 revision index display only; Chromium desktop and mobile emulation, not source, official, predraw or WeChat certification',url,browser:b.version(),checks,errors};fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify(result,null,2));await b.close()})().catch(e=>{console.error(e);process.exit(1)});
