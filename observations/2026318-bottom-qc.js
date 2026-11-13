#!/usr/bin/env node
'use strict';
// Inspect actual rendered page bottom, both viewports, before and after reload/view switches.
const {chromium,devices}=require('playwright'),{pathToFileURL}=require('url'),fs=require('fs'),path=require('path');
const input=process.argv[2],output=process.argv[3],screens=process.argv[4];if(!input||!output)throw Error('page and result path required');const url=/^https?:/.test(input)?input:pathToFileURL(path.resolve(input)).href;
(async()=>{const b=await chromium.launch({headless:true,args:['--no-sandbox']}),checks=[],errors=[];const check=(v,m)=>{if(!v)throw Error('FAIL '+m);checks.push(m)};
 for(const [label,config] of [['desktop',{viewport:{width:1440,height:900}}],['mobile',devices['iPhone 13']]]){const c=await b.newContext({...config,locale:'zh-CN',timezoneId:'Asia/Shanghai'}),p=await c.newPage();p.on('pageerror',e=>errors.push(String(e)));
  async function inspect(phase){await p.evaluate(()=>window.scrollTo(0,document.documentElement.scrollHeight));const q=await p.evaluate(()=>({text:document.body.innerText,footerCount:document.querySelectorAll('footer,#footSrc,#source-risk-notice').length,lastVisible:[...document.body.children].filter(x=>x.tagName!=='SCRIPT'&&getComputedStyle(x).display!=='none').at(-1)?.id,bottom:scrollY+innerHeight>=document.documentElement.scrollHeight-2}));check(q.bottom&&q.lastVisible==='entBox'&&q.footerCount===0,`${label} ${phase}: final visible block has no footer`);for(const word of ['资料与机制未经认证','司警','非官方','排期未核实','仅供观察'])check(!q.text.includes(word),`${label} ${phase}: absent ${word}`)}
  await p.goto(url,{waitUntil:'load',timeout:45000});await inspect('initial');if(screens){fs.mkdirSync(screens,{recursive:true});await p.screenshot({path:path.join(screens,`bottom-${label}.png`),fullPage:false})}
  await p.locator('#t-zod').click();await inspect('after view switch');await p.reload({waitUntil:'load'});await inspect('after reload');await c.close();
 }
 check(errors.length===0,'no unhandled page errors');const result={status:'PASS',scope:'rendered page bottom, desktop Chromium and mobile emulation; not WeChat safety or predraw verification',url,browser:b.version(),checks,errors};fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify(result,null,2));await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
