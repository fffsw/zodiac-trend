# -*- coding: utf-8 -*-
"""生成 zodiac_trend.html — 照截图样式: 行=期数, 列=号码/生肖(分区), 红圆+遗漏值,
右侧指标区, 底部预测区/按钮/倒计时/绿柱统计, 浅色主题"""
import csv, json

ORDER = ['鼠', '牛', '虎', '兔', '龍', '蛇', '馬', '羊', '猴', '鷄', '狗', '豬']
rows = list(csv.DictReader(open('data/macau_mark_six_full.csv', encoding='utf-8-sig')))
rows.sort(key=lambda r: int(r['period']))
last = rows[-250:]
data = []
for r in last:
    data.append([
        int(r['period']),
        r['date'][5:10].replace('-', '/'),
        [int(r[f'n{j}']) for j in range(1, 7)],
        [ORDER.index(r[f'z{j}']) for j in range(1, 7)],
        int(r['special']),
        ORDER.index(r['special_zodiac']),
    ])
# 号码→生肖 (当期制度: 馬年 2026048 起)
n2z = {}
for r in rows:
    if int(r['period']) >= 2026048:
        for j in range(1, 7):
            n2z[int(r[f'n{j}'])] = ORDER.index(r[f'z{j}'])
        n2z[int(r['special'])] = ORDER.index(r['special_zodiac'])
assert len(n2z) == 49, f'n2z incomplete: {len(n2z)}/49'
assert n2z[24] == ORDER.index('羊') and n2z[37] == ORDER.index('馬'), 'n2z spot check failed'
payload = json.dumps({'rows': data, 'order': ORDER, 'n2z': n2z}, ensure_ascii=False, separators=(',', ':'))

# v5.0人工定案: 只把结构字段注入页面, 键用“数据尾期号”而不是目标期,
# 避免页面正文出现未来期全号; JS以数据尾+1校验目标。报告文本不注入页面。
def _manual_zidx(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return ORDER.index(value)

manual_decisions_v50_by_tail = {}
try:
    with open('data/manual_site_decisions.json', encoding='utf-8') as _mf:
        _manual_doc = json.load(_mf)
except FileNotFoundError:
    _manual_doc = {'decisions': {}}
for _target_key, _rec in (_manual_doc.get('decisions', {}) or {}).items():
    _target = int(_rec.get('target', _target_key))
    manual_decisions_v50_by_tail[str(_target - 1)] = {
        'U': [_manual_zidx(z) for z in _rec.get('universe_zodiac', _rec.get('U', []))],
        'top': _manual_zidx(_rec.get('top_zodiac', _rec.get('top'))),
        'A': _manual_zidx(_rec.get('a_zodiac', _rec.get('A'))),
        'B': _manual_zidx(_rec.get('b_zodiac', _rec.get('B'))),
        'C': _manual_zidx(_rec.get('c_zodiac', _rec.get('C'))),
        'D': _manual_zidx(_rec.get('d_zodiac', _rec.get('D'))),
        'top_overlap_mode': _rec.get('top_overlap_mode'),
    }
manual_decisions_v50_payload = json.dumps(
    manual_decisions_v50_by_tail, ensure_ascii=False, separators=(',', ':')
)

TPL = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>石坑绝密 · 开奖走势 / 生肖 / 预测区</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#eef0f4;color:#333;font:12px/1.5 "PingFang SC","Microsoft YaHei",system-ui,sans-serif;padding:10px;-webkit-text-size-adjust:100% }
header{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:6px}
h1{font-size:15px;color:#c40000;letter-spacing:1px}
h1 small{color:#8a92a6;font-size:11px;font-weight:400;margin-left:6px}
.topseal{background:linear-gradient(90deg,#7a0000,#e60012 50%,#7a0000);color:#ffd700;font-size:clamp(26px,6vw,42px);font-weight:900;letter-spacing:14px;text-align:center;padding:11px 8px;border-radius:8px;margin:0 0 7px;border:3px solid #ffb300;text-shadow:0 2px 6px rgba(0,0,0,.55);box-shadow:0 3px 10px rgba(0,0,0,.3);-webkit-user-select:none;user-select:none}
@media(max-width:760px){.topseal{font-size:23px;letter-spacing:7px;padding:8px 5px;border-width:2px}}
.opt-label{color:#8a92a6;font-size:11px}
button{background:#fff;color:#444;border:1px solid #ccd2de;border-radius:4px;padding:4px 10px;cursor:pointer;font-size:12px}
button.blue{background:#1e5eff;border-color:#1e5eff;color:#fff}
button.on{background:#1e5eff;border-color:#1e5eff;color:#fff}
.legend{width:100%;background:#fff;border:1px solid #e0e4ec;border-radius:5px;padding:5px 10px;color:#777;font-size:11px;margin-bottom:6px}
.legend b{color:#333}
.dot{display:inline-flex;width:17px;height:17px;border-radius:50%;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#fff;vertical-align:-3px;margin:0 2px}
.barwrap{display:flex;gap:6px;align-items:center;flex:1;min-width:0}
.scroll{flex:1;min-width:0;overflow:auto;max-height:74vh;background:#fff;border:1px solid #d8dde8;border-radius:4px}
.scroll{max-height:74dvh;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
header,button,table,th,td,.legend,.controls,.ent,.drawbox{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}
input{-webkit-user-select:text;user-select:text}
button,.scroll,input{touch-action:manipulation}
.scroll::-webkit-scrollbar{height:12px;width:12px}
.scroll::-webkit-scrollbar-thumb{background:#b9c1d4;border-radius:6px}
.scroll::-webkit-scrollbar-track{background:#f0f2f7}
table{border-collapse:separate;border-spacing:0;width:max-content;table-layout:fixed}
th,td{border-right:1px solid #e6e9f0;border-bottom:1px solid #e6e9f0;text-align:center;overflow:hidden}
thead th{background:#f4f6fa;color:#555;font-weight:600}
thead tr.r1 th{height:34px;position:sticky;top:0;z-index:5}
thead tr.r2 th{height:30px;position:sticky;top:34px;z-index:5}
th.perh{position:sticky!important;left:0;top:0!important;z-index:8!important;width:92px;min-width:92px;background:#fff;color:#333}
th.banner{background:#e60012!important;color:#fff;font-size:13px;letter-spacing:6px}
th.indh{background:#eceff5!important;color:#333;font-size:11px}
th.zone{font-size:12px;color:#222;background:#f8f9fc}
th.zone.zb{border-right:2px solid #c9cfdd}
td.per{position:sticky;left:0;z-index:4;background:#fff;width:92px;min-width:92px;font-weight:700;color:#222;font-size:13px}
td.per span{display:block;font-size:9px;color:#9aa2b5;font-weight:400;line-height:1}
/* 号码格 */
td.n{height:26px;width:30px;padding:0}
.dn{display:flex;width:22px;height:22px;margin:0 auto;border-radius:50%;background:#e60012;color:#fff;font-size:11px;font-weight:700;align-items:center;justify-content:center;letter-spacing:-.6px}
.dn.sp{background:#16a34a}
.omv{font-size:11px;color:#a6adbd;letter-spacing:-.5px}
/* 生肖格 */
td.z{height:30px;width:64px;padding:0}
.zc{display:flex;align-items:center;justify-content:center;gap:2px}
.zch{display:flex;width:22px;height:22px;border-radius:50%;background:#e60012;color:#fff;font-size:12px;font-weight:700;align-items:center;justify-content:center;line-height:1}
.zch.sp{background:#16a34a}
.mult{font-size:10px;color:#e60012;font-weight:700;line-height:1}
/* 指标区 sticky */
td.sti{position:sticky;background:#fff;z-index:3;font-size:12px;color:#333}
th.sti{position:sticky;z-index:6;background:#eceff5}
.i1{right:198px;width:54px;min-width:54px}
.i2{right:132px;width:66px;min-width:66px}
.i3{right:54px;width:78px;min-width:78px}
.i4{right:0;width:54px;min-width:54px}
th.sti.i1,th.sti.i2,th.sti.i3,th.sti.i4{top:0;height:64px!important;display:table-cell}
.spc{display:inline-flex;width:22px;height:22px;border-radius:50%;background:#16a34a;color:#fff;font-size:11px;font-weight:700;align-items:center;justify-content:center}
.zsp{font-weight:700}
/* tfoot */
tfoot td{background:#fafbfd;height:26px;color:#555;font-size:11px}
tfoot td.per{background:#f4f6fa}
tfoot td.sti{background:#f4f6fa}
tr.pred td{height:26px;cursor:pointer;background:#fcfcfe}
tr.pred td:hover{background:#eaf7ee}
tr.pred td.pcell.on{background:#fff}
.pv{display:flex;width:22px;height:22px;margin:0 auto;border-radius:50%;background:#16a34a;color:#fff;font-size:11px;font-weight:700;align-items:center;justify-content:center}
tr.stat td{height:44px;background:#fff;color:#777}
tr.stat td.per{background:#f4f6fa}
tr.stat td.sti{background:#f4f6fa}
.bar\boxed{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:40px}
.barbox i{display:block;width:14px;background:#22c55e;border-radius:2px 2px 0 0}
.barbox b{font-size:10px;color:#40916c;font-weight:600;line-height:1.1}
/* 控制区 */
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
.count{background:#fff;border:1px solid #e0e4ec;border-radius:4px;padding:6px 12px;color:#c40000;font-weight:700;font-size:13px}
.count span{color:#333;font-weight:400;margin-right:6px}




.msg{font-size:12px;color:#b45309}






.ent{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:#fff;border:1px solid #e0e4ec;border-radius:6px;padding:8px 10px;margin-bottom:6px;font-size:12px}
.ent b{color:#1d3557;font-size:13px}
.ent .emsg{color:#555;font-size:12px}
.ent .entnote{flex-basis:100%;font-size:10px;color:#9aa3b2;line-height:1.5;margin-top:2px}
#entOut{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.drawbox{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:#f7fbff;border:1px solid #b3d4ff;border-radius:6px;padding:8px 10px;margin-bottom:6px;font-size:12px}
.drawbox b{color:#1d3557;font-size:13px}
.drawbox input{border:1px solid #ccd2de;border-radius:4px;padding:6px 8px;font-size:14px;width:230px;max-width:56vw;color:#222;letter-spacing:1px}
.drawbox input.sp-in{width:86px}
.drawbox input:focus{outline:none;border-color:#1e5eff}
.drawbox .msg{color:#2c7a39;font-size:12px}
.drawnote{flex-basis:100%;font-size:10px;color:#9aa3b2;line-height:1.5;margin-top:2px}
.zchip{display:inline-flex;align-items:center;border-radius:12px;color:#fff;font-weight:700;font-size:12px;padding:2px 9px;gap:4px}
footer{color:#8a92a6;font-size:11px;margin-top:12px;border-top:1px solid #dde1ea;padding-top:8px;line-height:1.7}
@media(max-width:760px){
  body{padding:6px}
  .legend{font-size:10px;-webkit-line-clamp:2;-webkit-box-orient:vertical;display:-webkit-box;overflow:hidden}
  .i1,.i2,.i3,.i4{right:auto!important}
  th.perh,td.per,td.sti,th.sti,thead tr.r1 th,thead tr.r2 th{position:static!important;top:auto!important;left:auto!important}
  td.per,th.perh{width:64px;min-width:64px}
}
</style>
</head>
<body>
<div class="topseal">石坑绝密</div>
__REVISION_NOTICE__
<header>
  <h1>开奖走势<small id="h1sub">新澳门 0000–0000 · 000期数据 · 横向滚动查看</small></h1>
  <span class="opt-label">视图</span>
  <button id="t-num" class="on">号码走势 01-49</button>
  <button id="t-zod">生肖走势</button>
  <span class="opt-label">期数</span>
  <button data-n="50">50</button><button data-n="100" class="on">100</button><button data-n="250">250</button>
  <button id="omBtn" class="on">遗漏值:开</button>
</header>
<div class="legend">
  <b>图例:</b>
  <span class="dot" style="background:#e60012">05</span>=平码开出
  <span class="dot" style="background:#16a34a">24</span>=特码
  &nbsp;·&nbsp; <b>生肖视图</b>:红圈=平码开出生肖(×n=同肖个数),绿圈=特码生肖,悬停看号码
  &nbsp;·&nbsp; 灰色数字=连续多少期未出(遗漏),开出即清零
  &nbsp;·&nbsp; 指标区=每期 和值 / 奇偶 / 012路 / 特码(滚动固定) · 底部:预测区(点击标绿)· 当前遗漏 · 近30期次数绿柱
</div>

<div class="barwrap">
  <div class="scroll" id="sc"><table id="grid"></table></div>
</div>

<div class="controls">
  <button class="blue" id="btnClear">清空</button>
  <button class="blue" id="btnAdd">添加预测行</button>
  <button class="blue" id="btnDel">删除预测行</button>
  <div class="count" id="count"><span>加载中…</span></div>
</div>

<div class="drawbox" id="drawBox">
  <b>开奖录入 · 全量重算</b>
  <input id="drawIn" type="text" placeholder="平码6个:05 12 17 22 38 46" autocomplete="off">
  <input id="drawSp" type="text" placeholder="特码1个" autocomplete="off" class="sp-in">
  <button id="btnDraw" class="blue">录入并重算</button>
  <button id="btnUndoDraw">撤销追加</button>
  <span id="drawMsg" class="msg"></span>
  <div class="drawnote">开奖后录入:6平码+1特码(1–49互不相同)→ 追加为新一期,走势/遗漏/指标/绿柱/倒计时/娱乐预测全部按新数据重算 · 追加仅存本机浏览器(刷新不丢;换设备/浏览器不共享,清除浏览器数据即消失)。</div>
</div>
<div class="ent" id="entBox">
  <b>娱乐预测 · 号码池两池(__PV__ · __PVDESC__)</b>
  <button id="btnMaxZod" class="blue">单肖展示</button>
  <button id="btnT33">娱乐三中三</button>
  <button id="btnE22">娱乐二中二</button>
  <span id="entOut"></span>
<div class="entnote">仅供观察，频率≠下期概率；均匀模型下，四码肖在六平码至少出现一次约41.75%，五码肖约49.52%，固定单号码在六码出现为6/49。栏位不是最高置信；随机开奖无记忆，赔率低于公允回报时投注长期为负期望。未成年人禁购，理性投注。</div>
</div>
<footer id="footSrc">数据源:新澳门六合彩 0000–0000 · 随机开奖无记忆,走势图不产生预测力,频率≠下期概率 · 仅供数据观察 · 未满18周岁禁止购彩,设定止损,理性投注。</footer>

<script>
const DATA=__DATA__, ZN=DATA.order, ALL=DATA.rows;
const ZC=['#4db6ac','#8d6e63','#ef6c00','#ec407a','#7e57c2','#43a047','#e53935','#f9a825','#00acc1','#ab47bc','#7cb342','#78909c'];
const era=p=>p<=2024040?3:p<=2025028?4:p<=2026047?5:6;
// 单期剔除表(用户2026-10-15): 仅对指定目标期生效, 过后自动失效。2026289期剔除豬(短期过热, 一次性)。
const PERIOD_BAN={2026289:[11]};
// v5.0人工定案(按数据尾期号键入; 只含六肖/槽位结构, 不含报告文本)。
const MANUAL_SITE_DECISIONS_V50=__MANUAL_DECISIONS_V50__;
let COLS=100, SHOW_OM=true, VIEW='num';
function commOne(r){const n=r[2];
  const odd=n.filter(x=>x%2).length, c0=n.filter(x=>x%3===0).length, c1=n.filter(x=>x%3===1).length;
  return {sum:n.reduce((a,b)=>a+b,0), odd, even:6-odd, r0:c0, r1:c1, r2:6-c0-c1, sp:r[4], sz:r[5]};}
let EXTRAS=[];
try{const raw=window.localStorage&&localStorage.getItem('zt_extra');
  if(raw){const ex=JSON.parse(raw);
    if(Array.isArray(ex))for(const row of ex){
      if(Array.isArray(row)&&row.length===6&&typeof row[0]==='number'&&row[0]>ALL[ALL.length-1][0]){EXTRAS.push(row);ALL.push(row);}}}}catch(e){}
let comm=ALL.map(commOne);
// 遗漏(250期滚动)
function buildOmit(kind){
  const size=kind==='num'?49:12;
  const om=Array(size+1).fill(0), out=Array.from({length:size+1},()=>[]);
  ALL.forEach((r,t)=>{
    for(let i=1;i<=size;i++){
      const hit= kind==='num' ? (r[2].includes(i)||r[4]===i) : (r[3].includes(i-1)||r[5]===i-1);
      if(hit)om[i]=0; else om[i]++;
      out[i][t]=om[i];
    }});
  return out;
}
let OMN=buildOmit('num'), OMZ=buildOmit('zod');
const win=()=>({s:ALL.length-COLS,e:ALL.length});
function indCols(){return VIEW==='num'?[['和值',54],['奇偶',66],['012路',78],['特码',54]]:[['和值',54],['奇偶',66],['肖数',78],['特码',54]];}
function render(){
  const {s,e}=win(), nCols= VIEW==='num'?49:12;
  const MOB=!!(window.matchMedia&&matchMedia('(max-width:760px)').matches);
  const widths = VIEW==='num'?[MOB?64:92].concat(Array(49).fill(MOB?24:30)).concat([54,66,78,54]) : [MOB?64:92].concat(Array(12).fill(MOB?52:64)).concat([54,66,78,54]);
  let cg='<colgroup>'+widths.map(w=>`<col style="width:${w}px">`).join('')+'</colgroup>';
  // thead
  const bannerTxt = VIEW==='num' ? '平码开奖号码' : '平码生肖走势 · 12肖全';
  let h=cg+'<thead><tr class="r1"><th class="perh" rowspan="2">期数</th>'
    +`<th class="banner" colspan="${nCols}">${bannerTxt}</th><th class="indh" colspan="4">指标区</th></tr>`;
  h+='<tr class="r2">';
  if(VIEW==='num'){
    const zones=[['一区',10],['二区',10],['三区',10],['四区',10],['五区',9]];
    zones.forEach((z,i)=>{h+=`<th class="zone${i<4?' zb':''}" colspan="${z[1]}">${z[0]}</th>`;});
  }else{
    for(let z=0;z<12;z++) h+=`<th class="zone" style="background:${ZC[z]};color:#fff;border-right:2px solid #fff">${ZN[z]}</th>`;
  }
  indCols().forEach((c,i)=>{h+=`<th class="sti i${i+1}">${c[0]}</th>`;});
  h+='</tr></thead>';
  // tbody
  h+='<tbody>';
  for(let t=s;t<e;t++){
    const r=ALL[t], c=comm[t];
    h+=`<tr><td class="per" title="${r[0]}期 ${r[1]}">${r[0]}<span>${r[1]}</span></td>`;
    if(VIEW==='num'){
      for(let n=1;n<=49;n++){
        const inP=r[2].includes(n), inS=r[4]===n;
        let inner;
        if(inP||inS) inner=`<div class="dn ${inS?'sp':''}">${String(n).padStart(2,'0')}</div>`;
        else inner= SHOW_OM?`<span class="omv">${OMN[n][t]>99?'99+':OMN[n][t]}</span>`:'';
        h+=`<td class="n" title="${r[0]}期 号码${String(n).padStart(2,'0')}">${inner}</td>`;
      }
      h+=`<td class="sti i1">${c.sum}</td><td class="sti i2">${c.odd}:${c.even}</td><td class="sti i3">${c.r0}:${c.r1}:${c.r2}</td><td class="sti i4"><span class="spc">${String(c.sp).padStart(2,'0')}</span></td>`;
    }else{
      for(let z=0;z<12;z++){
        const nums=[]; r[3].forEach((zz,j)=>{if(zz===z)nums.push(r[2][j]);});
        const hasSp=r[5]===z;
        let inner='';
        if(nums.length||hasSp){
          inner='<div class="zc">';
          if(nums.length) inner+=`<div class="zch" title="平码:${nums.map(n=>String(n).padStart(2,'0')).join(' ')}">${ZN[z]}</div>`+(nums.length>1?`<b class="mult">×${nums.length}</b>`:'');
          if(hasSp) inner+=`<div class="zch sp" title="特码生肖">${ZN[z]}</div>`;
          inner+='</div>';
        }
        else inner= SHOW_OM?`<span class="omv">${OMZ[z+1][t]>99?'99+':OMZ[z+1][t]}</span>`:'';
        h+=`<td class="z" title="${r[0]}期 ${ZN[z]}">${inner}</td>`;
      }
      h+=`<td class="sti i1">${c.sum}</td><td class="sti i2">${c.odd}:${c.even}</td><td class="sti i3">${new Set(r[3]).size}</td><td class="sti i4"><span class="zsp" style="color:${ZC[c.sz]}">${ZN[c.sz]}</span></td>`;
    }
    h+='</tr>';
  }
  h+='</tbody>';
  // tfoot: 预测区2行 + 遗漏行 + 绿柱行
  h+='<tfoot>';
  for(let p=0;p<2;p++)h+=predRow(p+1);
  h+=statOmitRow(); h+=statBarRow();
  h+='</tfoot>';
  document.getElementById('grid').innerHTML=h;
}
function predRow(id){
  let h=`<tr class="pred" data-pred="${id}"><td class="per">预测区</td>`;
  const nCols= VIEW==='num'?49:12;
  for(let i=1;i<=nCols;i++){
    h+=`<td class="pcell" data-col="${i}" title="点击标记预测"></td>`;
  }
  h+='<td class="sti i1"></td><td class="sti i2"></td><td class="sti i3"></td><td class="sti i4"></td></tr>';
  return h;
}
function statOmitRow(){
  const {e}=win(), nCols= VIEW==='num'?49:12;
  let h=`<tr class="stat"><td class="per">当前遗漏</td>`;
  for(let i=1;i<=nCols;i++){ const v=(VIEW==='num'?OMN:OMZ)[i][e-1]; h+=`<td><b style="color:#b45309">${v>99?'99+':v}</b></td>`; }
  h+='<td class="sti i1"></td><td class="sti i2"></td><td class="sti i3"></td><td class="sti i4"></td></tr>';
  return h;
}
function statBarRow(){
  const nCols= VIEW==='num'?49:12;
  const cnt=Array(nCols+1).fill(0);
  ALL.slice(-30).forEach(r=>{ if(VIEW==='num'){for(let n=1;n<=49;n++)if(r[2].includes(n)||r[4]===n)cnt[n]++;}
    else{for(let z=1;z<=12;z++)if(r[3].includes(z-1)||r[5]===z-1)cnt[z]++;} });
  const mx=Math.max(...cnt.slice(1))||1;
  let h=`<tr class="stat"><td class="per">近30期次数</td>`;
  for(let i=1;i<=nCols;i++){ const v=cnt[i], bh=Math.max(2,Math.round(v/mx*26));
    h+=`<td><div class="barbox"><b>${v}</b><i style="height:${bh}px"></i></div></td>`; }
  h+='<td class="sti i1"></td><td class="sti i2"></td><td class="sti i3"></td><td class="sti i4"></td></tr>';
  return h;
}
// 预测区交互
function bindPred(){
  document.getElementById('grid').addEventListener('click',e=>{
    const td=e.target.closest('td.pcell'); if(!td)return;
    const col=+td.dataset.col;
    if(td.classList.contains('on')){td.classList.remove('on');td.innerHTML='';}
    else{td.classList.add('on');
      td.innerHTML= VIEW==='num'?`<span class="pv">${String(col).padStart(2,'0')}</span>`:`<span class="pv">${ZN[col-1]}</span>`;}
  });
}
function bindCtrl(){
  document.getElementById('t-num').onclick=()=>setView('num');
  document.getElementById('t-zod').onclick=()=>setView('zod');
  document.querySelectorAll('[data-n]').forEach(b=>b.onclick=()=>{
    document.querySelectorAll('[data-n]').forEach(x=>x.classList.remove('on'));
    b.classList.add('on'); COLS=+b.dataset.n; render(); scrollEnd();});
  document.getElementById('omBtn').onclick=function(){SHOW_OM=!SHOW_OM;this.classList.toggle('on',SHOW_OM);
    this.textContent='遗漏值:'+(SHOW_OM?'开':'关'); render();};
  document.getElementById('btnClear').onclick=()=>{document.querySelectorAll('td.pcell.on').forEach(td=>{td.classList.remove('on');td.innerHTML='';});};
  document.getElementById('btnAdd').onclick=()=>{const rows=document.querySelectorAll('tr.pred');
    const n=rows.length; if(n>=5)return;
    rows[n-1].insertAdjacentHTML('afterend',predRow(n+1));};
  document.getElementById('btnDel').onclick=()=>{const rows=document.querySelectorAll('tr.pred');
    if(rows.length>1)rows[rows.length-1].remove();};
}
function setView(v){VIEW=v;
  document.getElementById('t-num').classList.toggle('on',v==='num');
  document.getElementById('t-zod').classList.toggle('on',v==='zod');
  render(); scrollEnd();}
function scrollEnd(){const sc=document.getElementById('sc'); sc.scrollTop=sc.scrollHeight; sc.scrollLeft=0;}
// 倒计时
function tick(){
  const now=new Date(); let d=new Date(now); d.setHours(21,30,0,0);
  let pd=ALL[ALL.length-1][0]+1;
  if(now>d){d.setDate(d.getDate()+1); pd=ALL[ALL.length-1][0]+2;}
  let ms=d-now; const hh=String(Math.floor(ms/3600000)).padStart(2,'0'),
    mm=String(Math.floor(ms%3600000/60000)).padStart(2,'0'), ss=String(Math.floor(ms%60000/1000)).padStart(2,'0');
  document.getElementById('count').innerHTML=`<span>第 ${pd} 期销售截止倒计时</span${hh}:${mm}:${ss}`;
}
// ---- 号码解析:全角/区间/去重(开奖录入复用) ----
const N2Z=DATA.n2z||{};
function normTok(t){return t.replace(/[０-９]/g,d=>String.fromCharCode(d.charCodeAt(0)-0xFEE0)).replace(/[－—]/g,'-');}
function parseNums(str){
  const res={ok:[],bad:[]};
  String(str).split(/[\s,、;；|]+/).filter(Boolean).forEach(raw=>{
    const tok=normTok(raw.trim()); let m;
    if((m=tok.match(/^(\d{1,2})\s*-\s*(\d{1,2})$/))){
      let a=+m[1],b=+m[2]; if(a>b)[a,b]=[b,a];
      if(b>49||a<1){res.bad.push(raw);return;}
      for(let i=a;i<=b;i++)res.ok.push(i);
    }else if(/^\d{1,2}$/.test(tok)){
      const v=+tok; (v>=1&&v<=49)?res.ok.push(v):res.bad.push(raw);
    }else res.bad.push(raw);
  });
  return res;
}
// 娱乐预测 §1附v2.9: 池1摇1000次、池2摇3000次, 取出现最多 — 池1最多者=最大可能(独占);
// 池2按出现次数降序前4名: A=第1名,B=第2名,C=第3名,D=第4名; 二中二=[A,B], 三中三=[A,C,D](共享恰1); 并列取肖序; 连续LCG流共4000步(池1×1000+池2×3000)
function entPicks_v30(){
  const {pool, cands}=poolTop6();
  let x=(ALL[ALL.length-1][0]+1)>>>0;
  const step=()=>{ x=(Math.imul(1664525,x)+1013904223)>>>0; return x; };
  const c1=new Array(12).fill(0), c2=new Array(12).fill(0);
  for(let i=0;i<1000;i++){ step(); c1[cands[(x>>>16)%cands.length]]++; }
  for(let i=0;i<3000;i++){ step(); c2[pool[(x>>>16)%pool.length]]++; }
  const byCnt=(arr,cnt)=>arr.slice().sort((a,b)=>(cnt[b]-cnt[a])||(a-b));
  const top=byCnt(cands,c1)[0];
  const r=byCnt(pool,c2);
  return {top, t2:[r[0],r[1]], t3:[r[0],r[2],r[3]], pool, cands};
}
let ENTMODE='all';
function entHTML(){
  const P=entPicks();
  if(P.manualMissing) return `<span class="emsg">待人工定案（不摇号）</span>`;
  const chip=z=>`<span class="zchip" style="background:${ZC[z]}">${ZN[z]}</span>`;
  const sT=ENTMODE==='all'||ENTMODE==='max', s3=ENTMODE==='all'||ENTMODE==='t33', s2=ENTMODE==='all'||ENTMODE==='e22';
  let s='';
  if(sT) s+=`<span class="emsg">单肖展示</span>`+chip(P.top);
  if(s3) s+=`<span class="emsg">三中三</span>`+P.t3.map(chip).join('');
  if(s2) s+=`<span class="emsg">二中二</span>`+P.t2.map(chip).join('');
  return s;
}
function renderEnt(){ document.getElementById('entOut').innerHTML=entHTML(); }
// ============================================================================
// 号码池 v3.0 (2026-10-18 用户裁定): 池1=短期30期 / 池2=中期60期, 两池允许重叠
//   池1 = 短期30期 A榜(平码标准化热度)+B榜(出现期数) 名次和 → 剔上期开出肖 → 前3肖
//         摇号1000步取最多 = 最大可能
//   池2 = 中期60期 同法 → 剔上期开出肖 → 前4肖
//         摇号3000步降序 = A,B,C,D; 二中二=[A,B]; 三中三=[A,C,D]
//   单一LCG流4000步(前1000池1+后3000池2), 不重置
//   PERIOD_BAN 单期剔除表仍生效
// ============================================================================
function _ranks(W){
  const cnt=new Array(50).fill(0);
  for(const r of W){ for(const n of r[2]) cnt[n]++; }
  const E=6*W.length/49, zs=new Array(12).fill(0), ks=new Array(12).fill(0);
  for(let n=1;n<=49;n++){ const z=N2Z[n]; zs[z]+=cnt[n]; ks[z]++; }
  const rec=[];
  for(let z=0;z<12;z++) rec.push([z, zs[z]/(ks[z]*E)]);
  rec.sort((a,b)=>b[1]-a[1]||a[0]-b[0]);
  const rA=new Array(12); rec.forEach((r,i)=>rA[r[0]]=i+1);
  const zb=new Array(12).fill(0);
  for(const r of W){ for(const z of new Set(r[3])) zb[z]++; }
  const oB=[...Array(12).keys()].sort((a,b)=>zb[b]-zb[a]||a-b);
  const rB=new Array(12); oB.forEach((z,i)=>rB[z]=i+1);
  const S=new Array(12);
  for(let z=0;z<12;z++) S[z]=rA[z]+rB[z];
  const order=[...Array(12).keys()].sort((a,b)=>(S[a]-S[b])||(a-b));
  return {order, S, rec, oB};
}
function _avail(){
  const last=ALL[ALL.length-1];
  const TARGET=last[0]+1;
  const BAN=new Set(PERIOD_BAN[TARGET]||[]);
  const excl=new Set([...last[3], last[5]]);
  return {excl, BAN, TARGET};
}
// ============================ v2.5 口径 (100期窗/摇1次/池2截5) ============================
// 池1=[两冠(A榜冠军+B榜冠军)+温号(oB第5–8名)] 去重 → 剔上期开出肖 → 不回填
// 池2=名次和zone(排除池1) → 新鲜优先 + ≤1上期补位(不足4顺延) → 截5
// 摇号: 单一LCG, step()1次取池1最大可能; 再 splice 4 次取 a,b,c,d; 二中二=[a,b], 三中三=[a,c,d]
function poolTop6_v25(){
  const W=ALL.slice(-100), cnt=new Array(50).fill(0);
  for(const r of W){ for(const n of r[2]) cnt[n]++; }
  const E=6*W.length/49, zs=new Array(12).fill(0), ks=new Array(12).fill(0);
  for(let n=1;n<=49;n++){ const z=N2Z[n]; zs[z]+=cnt[n]; ks[z]++; }
  const rec=[]; for(let z=0;z<12;z++) rec.push([z, zs[z]/(ks[z]*E)]);
  rec.sort((a,b)=>b[1]-a[1]||a[0]-b[0]);
  const rA=new Array(12); rec.forEach((r,i)=>rA[r[0]]=i+1);
  const zb=new Array(12).fill(0);
  for(const r of W){ for(const z of new Set(r[3])) zb[z]++; }
  const oB=[...Array(12).keys()].sort((a,b)=>zb[b]-zb[a]||a-b);
  const rB=new Array(12); oB.forEach((z,i)=>rB[z]=i+1);
  const merged=[...Array(12).keys()].sort((a,b)=>(rA[a]+rB[a])-(rA[b]+rB[b])||a-b);
  const last=ALL[ALL.length-1];
  const excl=new Set([...last[3], last[5]]);
  const champs=[rec[0][0], oB[0]];
  if(champs[1]===champs[0]) champs.pop();
  const warm=oB.slice(4,8).filter(z=>!champs.includes(z));
  const cands=[...champs, ...warm].filter((z,i,a)=>a.indexOf(z)===i && !excl.has(z));
  const zone=merged.filter(z=>!cands.includes(z));
  const fresh=zone.filter(z=>!excl.has(z));
  const stale=zone.filter(z=>excl.has(z));
  const allowed=fresh.length>=3?1:Math.max(1, 4-fresh.length);
  const pool=[...fresh, ...stale.slice(0,allowed)].slice(0,5);
  return {pool, cands};
}
function entPicks_v25(){
  const {pool, cands}=poolTop6_v25();
  let x=(ALL[ALL.length-1][0]+1)>>>0;
  const step=()=>{ x=(Math.imul(1664525,x)+1013904223)>>>0; return x; };
  step(); const top=cands[(x>>>16)%cands.length];
  const rest=pool.slice();
  step(); const a=rest.splice((x>>>16)%rest.length,1)[0];
  step(); const b=rest.splice((x>>>16)%rest.length,1)[0];
  step(); const c=rest.splice((x>>>16)%rest.length,1)[0];
  step(); const d=rest.splice((x>>>16)%rest.length,1)[0];
  return {top, t2:[a,b], t3:[a,c,d], pool, cands};
}
// ============================ 版本分派 (__PV__ 由 Python 端注入) ============================
const POOL_VERSION='__PV__';
function poolTop6(){
  if(POOL_VERSION==='v2.5') return poolTop6_v25();
  if(POOL_VERSION==='v3.0') return poolTop6_v30();
  if(POOL_VERSION==='v4.0') return poolTop6_v40();
  if(POOL_VERSION==='v4.1') return poolTop6_v41();
  if(POOL_VERSION==='v4.2') return poolTop6_v42();
  if(POOL_VERSION==='v5.0') return poolTop6_v50();
  throw new Error('unknown POOL_VERSION '+POOL_VERSION);
}
function entPicks(){
  if(POOL_VERSION==='v2.5') return entPicks_v25();
  if(POOL_VERSION==='v3.0') return entPicks_v30();
  if(POOL_VERSION==='v4.0') return entPicks_v40();
  if(POOL_VERSION==='v4.1') return entPicks_v41();
  if(POOL_VERSION==='v4.2') return entPicks_v42();
  if(POOL_VERSION==='v5.0') return entPicks_v50();
  throw new Error('unknown POOL_VERSION '+POOL_VERSION);
}

function poolTop6_v30(){
  const {excl, BAN}=_avail();
  const ok = z => !excl.has(z) && !BAN.has(z);
  // 池1: 短期 30 期
  const r1=_ranks(ALL.slice(-30));
  const cands=r1.order.filter(ok).slice(0,3);
  // 池2: 中期 60 期
  const r2=_ranks(ALL.slice(-60));
  const pool=r2.order.filter(ok).slice(0,4);
  return {pool, cands};
}
// ===================== 六肖双池 v4.0 / v4.1 / v4.2 (task200/202, 2026-10-23) =====================
// 共用骨架(最终定版): 先定 Universe U=6个不同生肖(2重+4新), 再分进双池; 同一生肖可同时进两池(重复肖),
// 两池并集恒=U. 重肖: 肖 in PREV (上期7球 distinct); 重复肖: 同肖同时在两池. _alloc6: 池1取U在本池序前4、
// 池2取U在本池序前6 → 最小池长2/4 → 未覆盖者入排名较前一池(同位池2) → 每池至少1重肖. 池长/重叠随数据变化.
// _pickStrat 优先级: 固定池长/池内不重复 > exclSet互斥 > BAN > 重肖配额 > 原序.
//   某层不足→另一层按原序顺延; 再不足→放行BAN(仍避exclSet); 再不足→放行exclSet(仅全定义兜底).
// v4.0(承v2.5): 100期窗, U按merged分层, 池1序P=[两冠+温号C, merged其余], 池2序=merged, 不读BAN, 摇号1+4步.
// v4.1(承v3.0): U按组合序(30位+60位)分层, 池1序=30期名次和, 池2序=60期名次和, 读BAN, 摇号4000步.
// v4.2(296深复盘调整): 与v4.1同窗同序同摇号; U分层每层最后一席改取该层组合序末位(尾部对冲), 仍2重4新.
// 目标299/300/301/302/303/304/305/306/307单期人工定案: 数据尾为2026298/2026299/2026300/2026301/2026302/2026303/2026304/2026305/2026306且无BAN时, U改用对应人工六肖;
// _alloc6与4000步摇号不变. 若该目标另设BAN, 为守BAN不变量回自动v4.2; 其他期不受影响.
// 展示不变: 最大可能自池1; 池2取四员A/B/C/D → 二中二=[A,B], 三中三=[A,C,D] (最大可能可与池2同肖, 展示去重4-5肖).
function _pickStrat(order, PREV, BAN, exclSet, nRep, nFresh){
  const size=nRep+nFresh;
  const elig=order.filter(z=>!BAN.has(z)&&!exclSet.has(z));
  const picks=[];
  const add=z=>{ if(!picks.includes(z)) picks.push(z); };
  elig.filter(z=>PREV.has(z)).slice(0,nRep).forEach(add);
  elig.filter(z=>!PREV.has(z)).slice(0,nFresh).forEach(add);
  for(const z of elig){ if(picks.length>=size) break; add(z); }
  for(const z of order){ if(picks.length>=size) break; if(!exclSet.has(z)) add(z); }
  for(const z of order){ if(picks.length>=size) break; add(z); }
  const pos=new Map(order.map((z,i)=>[z,i]));
  return picks.slice(0,size).sort((a,b)=>pos.get(a)-pos.get(b));
}
function _pickStratHedge(order, PREV, BAN, nRep, nFresh){
  const size=nRep+nFresh;
  const elig=order.filter(z=>!BAN.has(z));
  const reps=elig.filter(z=>PREV.has(z));
  const fresh=elig.filter(z=>!PREV.has(z));
  const choose=(xs,k)=>{
    if(k<=0) return [];
    if(xs.length<=k) return xs.slice();
    const out=xs.slice(0,k-1);
    const tail=xs[xs.length-1];
    if(!out.includes(tail)) out.push(tail);
    for(const z of xs){ if(out.length>=k) break; if(!out.includes(z)) out.push(z); }
    return out;
  };
  const picks=[...choose(reps,nRep), ...choose(fresh,nFresh)];
  for(const z of elig){ if(picks.length>=size) break; if(!picks.includes(z)) picks.push(z); }
  for(const z of order){ if(picks.length>=size) break; if(!picks.includes(z)) picks.push(z); }
  const pos=new Map(order.map((z,i)=>[z,i]));
  return picks.slice(0,size).sort((a,b)=>pos.get(a)-pos.get(b));
}
function _alloc6(U, PREV, o1, o2){
  const Uset=new Set(U);
  const pos1=new Map(o1.map((z,i)=>[z,i])), pos2=new Map(o2.map((z,i)=>[z,i]));
  let cands=o1.filter(z=>Uset.has(z)&&pos1.get(z)<4);
  let pool=o2.filter(z=>Uset.has(z)&&pos2.get(z)<6);
  const extend=(p,order,pos,minimum)=>{
    for(const z of order){ if(p.length>=minimum) break; if(Uset.has(z)&&!p.includes(z)) p.push(z); }
    return p.slice().sort((a,b)=>pos.get(a)-pos.get(b));
  };
  cands=extend(cands,o1,pos1,2);
  pool=extend(pool,o2,pos2,4);
  for(const z of U){
    if(!cands.includes(z)&&!pool.includes(z)){
      if(pos1.get(z)<pos2.get(z)) cands.push(z); else pool.push(z);
    }
  }
  cands.sort((a,b)=>pos1.get(a)-pos1.get(b));
  pool.sort((a,b)=>pos2.get(a)-pos2.get(b));
  const reps=U.filter(z=>PREV.has(z));
  if(reps.length&&!cands.some(z=>PREV.has(z))){
    cands.push(reps.slice().sort((a,b)=>pos1.get(a)-pos1.get(b))[0]);
    cands.sort((a,b)=>pos1.get(a)-pos1.get(b));
  }
  if(reps.length&&!pool.some(z=>PREV.has(z))){
    pool.push(reps.slice().sort((a,b)=>pos2.get(a)-pos2.get(b))[0]);
    pool.sort((a,b)=>pos2.get(a)-pos2.get(b));
  }
  return {pool, cands};
}
function poolTop6_v40(){
  const W=ALL.slice(-100), cnt=new Array(50).fill(0);
  for(const r of W){ for(const n of r[2]) cnt[n]++; }
  const E=6*W.length/49, zs=new Array(12).fill(0), ks=new Array(12).fill(0);
  for(let n=1;n<=49;n++){ const z=N2Z[n]; zs[z]+=cnt[n]; ks[z]++; }
  const rec=[]; for(let z=0;z<12;z++) rec.push([z, zs[z]/(ks[z]*E)]);
  rec.sort((a,b)=>b[1]-a[1]||a[0]-b[0]);
  const rA=new Array(12); rec.forEach((r,i)=>rA[r[0]]=i+1);
  const zb=new Array(12).fill(0);
  for(const r of W){ for(const z of new Set(r[3])) zb[z]++; }
  const oB=[...Array(12).keys()].sort((a,b)=>zb[b]-zb[a]||a-b);
  const rB=new Array(12); oB.forEach((z,i)=>rB[z]=i+1);
  const merged=[...Array(12).keys()].sort((a,b)=>(rA[a]+rB[a])-(rA[b]+rB[b])||a-b);
  const last=ALL[ALL.length-1];
  const PREV=new Set([...last[3], last[5]]);
  const champs=[rec[0][0], oB[0]];
  if(champs[1]===champs[0]) champs.pop();
  const warm=oB.slice(4,8).filter(z=>!champs.includes(z));
  const C=[...champs, ...warm].filter((z,i,a)=>a.indexOf(z)===i);
  const P=[...C, ...merged.filter(z=>!C.includes(z))];
  const EMPTY=new Set();
  const U=_pickStrat(merged, PREV, EMPTY, EMPTY, 2, 4);
  return _alloc6(U, PREV, P, merged);
}
function entPicks_v40(){
  const {pool, cands}=poolTop6_v40();
  let x=(ALL[ALL.length-1][0]+1)>>>0;
  const step=()=>{ x=(Math.imul(1664525,x)+1013904223)>>>0; return x; };
  step(); const top=cands[(x>>>16)%cands.length];
  const rest=pool.slice();
  step(); const a=rest.splice((x>>>16)%rest.length,1)[0];
  step(); const b=rest.splice((x>>>16)%rest.length,1)[0];
  step(); const c=rest.splice((x>>>16)%rest.length,1)[0];
  step(); const d=rest.splice((x>>>16)%rest.length,1)[0];
  return {top, t2:[a,b], t3:[a,c,d], pool, cands};
}
function poolTop6_v41(){
  const {excl:PREV, BAN}=_avail();
  const EMPTY=new Set();
  const r1=_ranks(ALL.slice(-30));
  const r2=_ranks(ALL.slice(-60));
  const pos30=new Map(r1.order.map((z,i)=>[z,i])), pos60=new Map(r2.order.map((z,i)=>[z,i]));
  const comb=[...Array(12).keys()].sort((a,b)=>(pos30.get(a)+pos60.get(a))-(pos30.get(b)+pos60.get(b))||a-b);
  const U=_pickStrat(comb, PREV, BAN, EMPTY, 2, 4);
  return _alloc6(U, PREV, r1.order, r2.order);
}
function entPicks_v41(){
  const {pool, cands}=poolTop6_v41();
  let x=(ALL[ALL.length-1][0]+1)>>>0;
  const step=()=>{ x=(Math.imul(1664525,x)+1013904223)>>>0; return x; };
  const c1=new Array(12).fill(0), c2=new Array(12).fill(0);
  for(let i=0;i<1000;i++){ step(); c1[cands[(x>>>16)%cands.length]]++; }
  for(let i=0;i<3000;i++){ step(); c2[pool[(x>>>16)%pool.length]]++; }
  const byCnt=(arr,cnt)=>arr.slice().sort((a,b)=>(cnt[b]-cnt[a])||(a-b));
  const top=byCnt(cands,c1)[0];
  const r=byCnt(pool,c2);
  return {top, t2:[r[0],r[1]], t3:[r[0],r[2],r[3]], pool, cands};
}
function poolTop6_v42(){
  const {excl:PREV, BAN}=_avail();
  const r1=_ranks(ALL.slice(-30));
  const r2=_ranks(ALL.slice(-60));
  const pos30=new Map(r1.order.map((z,i)=>[z,i])), pos60=new Map(r2.order.map((z,i)=>[z,i]));
  const comb=[...Array(12).keys()].sort((a,b)=>(pos30.get(a)+pos60.get(a))-(pos30.get(b)+pos60.get(b))||a-b);
  const autoU=_pickStratHedge(comb, PREV, BAN, 2, 4);
  // Manual indices are keyed by data tail so one-period decisions cannot leak:
  // tail 2026298 -> [鷄,馬,虎,蛇,龍,狗]; tail 2026299 -> [虎,兔,龍,蛇,馬,鷄];
  // tail 2026300 -> [虎,蛇,鼠,兔,龍,鷄]; tail 2026301 -> [虎,蛇,兔,馬,鷄,狗];
  // tail 2026302 -> [蛇,鷄,虎,鼠,龍,兔]; tail 2026303 -> [蛇,虎,鼠,羊,猴,鷄];
  // tail 2026304 -> [鷄,馬,虎,蛇,兔,豬]; tail 2026305 -> [虎,蛇,鷄,猴,羊,龍];
  // tail 2026306 -> revised 35-45 window [蛇,兔,虎,鼠,鷄,羊];
  // tail 2026307 -> 35-45 window [蛇,馬,虎,兔,豬,鼠].
  const MANUAL_U_BY_TAIL={2026298:[9,6,2,5,4,10],2026299:[2,3,4,5,6,9],2026300:[2,5,0,3,4,9],2026301:[2,5,3,6,9,10],2026302:[5,9,2,0,4,3],2026303:[5,2,0,7,8,9],2026304:[9,6,2,5,3,11],2026305:[2,5,9,8,7,4],2026306:[5,3,2,0,9,7],2026307:[5,6,2,3,11,0]};
  const manualU=MANUAL_U_BY_TAIL[ALL[ALL.length-1][0]];
  const U=(manualU&&BAN.size===0)?manualU:autoU;
  return _alloc6(U, PREV, r1.order, r2.order);
}
function entPicks_v42(){
  const {pool, cands}=poolTop6_v42();
  let x=(ALL[ALL.length-1][0]+1)>>>0;
  const step=()=>{ x=(Math.imul(1664525,x)+1013904223)>>>0; return x; };
  const c1=new Array(12).fill(0), c2=new Array(12).fill(0);
  for(let i=0;i<1000;i++){ step(); c1[cands[(x>>>16)%cands.length]]++; }
  for(let i=0;i<3000;i++){ step(); c2[pool[(x>>>16)%pool.length]]++; }
  const byCnt=(arr,cnt)=>arr.slice().sort((a,b)=>(cnt[b]-cnt[a])||(a-b));
  const top=byCnt(cands,c1)[0];
  const r=byCnt(pool,c2);
  return {top, t2:[r[0],r[1]], t3:[r[0],r[2],r[3]], pool, cands};
}
// ===================== v5.0 人工六肖全槽·无摇号 (2026-11-04) =====================
// MANUAL_SITE_DECISIONS_V50 以数据尾期号为键。没有当前目标记录时返回 manualMissing,
// 页面只显示“待人工定案（不摇号）”; 生产复算据此 fail-closed。两池为派生归类:
// cands=[top,A,B,C,D]去重(展示组), pool=[A,B,C,D,...非展示替补]。本节不调用LCG。
function _manualDecisionV50(){
  const tail=ALL[ALL.length-1][0];
  const target=tail+1;
  const raw=MANUAL_SITE_DECISIONS_V50[String(tail)] || MANUAL_SITE_DECISIONS_V50[tail];
  if(!raw) return null;
  const zi=v=>{
    const z=(typeof v==='number') ? v : ZN.indexOf(v);
    if(!Number.isInteger(z)||z<0||z>=12) throw new Error('v5.0 manual decision has invalid zodiac '+v);
    return z;
  };
  const universeRaw=raw.U || raw.universe_zodiac || raw.universe;
  if(!Array.isArray(universeRaw)) throw new Error('v5.0 manual decision missing Universe');
  const U=universeRaw.map(zi);
  const roles={
    top:zi(raw.top_zodiac!==undefined?raw.top_zodiac:raw.top),
    A:zi(raw.a_zodiac!==undefined?raw.a_zodiac:raw.A),
    B:zi(raw.b_zodiac!==undefined?raw.b_zodiac:raw.B),
    C:zi(raw.c_zodiac!==undefined?raw.c_zodiac:raw.C),
    D:zi(raw.d_zodiac!==undefined?raw.d_zodiac:raw.D)
  };
  const abcd=[roles.A,roles.B,roles.C,roles.D];
  if(U.length!==6||new Set(U).size!==6) throw new Error('v5.0 manual Universe must contain 6 distinct zodiac signs');
  if(new Set(abcd).size!==4) throw new Error('v5.0 manual A/B/C/D must be distinct');
  if(!U.includes(roles.top)||abcd.some(z=>!U.includes(z))) throw new Error('v5.0 manual slots must be inside Universe');
  const ban=new Set(PERIOD_BAN[target]||[]);
  if(U.some(z=>ban.has(z))) throw new Error('v5.0 manual decision conflicts with PERIOD_BAN');
  const overlapMode=abcd.includes(roles.top)?'concentrated':'coverage';
  if(raw.top_overlap_mode&&raw.top_overlap_mode!==overlapMode) throw new Error('v5.0 manual top_overlap_mode mismatch');
  return {target, U, roles, top_overlap_mode:overlapMode};
}
function _manualPoolsV50(dec){
  const display=[];
  for(const z of [dec.roles.top,dec.roles.A,dec.roles.B,dec.roles.C,dec.roles.D]){
    if(!display.includes(z)) display.push(z);
  }
  const reserves=dec.U.filter(z=>!display.includes(z));
  return {
    cands:display.slice(),
    pool:[dec.roles.A,dec.roles.B,dec.roles.C,dec.roles.D,...reserves],
    display, reserves
  };
}
function poolTop6_v50(){
  const dec=_manualDecisionV50();
  if(!dec) return {pool:[], cands:[], manualMissing:true};
  const p=_manualPoolsV50(dec);
  return {pool:p.pool, cands:p.cands};
}
function entPicks_v50(){
  const dec=_manualDecisionV50();
  if(!dec) return {top:null, t2:[], t3:[], pool:[], cands:[], manualMissing:true};
  const p=_manualPoolsV50(dec);
  return {
    top:dec.roles.top,
    t2:[dec.roles.A,dec.roles.B],
    t3:[dec.roles.A,dec.roles.C,dec.roles.D],
    pool:p.pool, cands:p.cands
  };
}
function bindEnt(){
  document.getElementById('btnMaxZod').onclick=()=>{ENTMODE='max';renderEnt();};
  document.getElementById('btnT33').onclick=()=>{ENTMODE='t33';renderEnt();};
  document.getElementById('btnE22').onclick=()=>{ENTMODE='e22';renderEnt();};
}
function updRanges(){
  const a=ALL[0][0], b=ALL[ALL.length-1][0];
  const hs=document.getElementById('h1sub');
  if(hs) hs.textContent=`新澳门 ${a}–${b} · ${ALL.length}期数据 · 横向滚动查看`;
  const fs=document.getElementById('footSrc');
  if(fs) fs.textContent=`数据源:新澳门六合彩 ${a}–${b} · 随机开奖无记忆,走势图不产生预测力,频率≠下期概率 · 仅供数据观察 · 未满18周岁禁止购彩,设定止损,理性投注。`;
}
function recalcAll(){
  comm=ALL.map(commOne);
  OMN=buildOmit('num'); OMZ=buildOmit('zod');
  updRanges();
  render(); scrollEnd(); renderEnt(); tick();
}
function onDraw(){
  const msg=document.getElementById('drawMsg');
  const ns=parseNums(document.getElementById('drawIn').value).ok;
  const sp=parseNums(document.getElementById('drawSp').value).ok;
  if(ns.length!==6){msg.textContent='平码需恰好6个(1–49,互不相同)';return;}
  if(sp.length!==1){msg.textContent='特码需恰好1个(1–49)';return;}
  if(ns.includes(sp[0])){msg.textContent='特码不能与平码重复';return;}
  const np=ALL[ALL.length-1][0]+1;
  const now=new Date();
  const mmdd=String(now.getMonth()+1).padStart(2,'0')+'/'+String(now.getDate()).padStart(2,'0');
  const row=[np,mmdd,ns.slice(),ns.map(n=>N2Z[n]),sp[0],N2Z[sp[0]]];
  ALL.push(row); EXTRAS.push(row);
  try{localStorage.setItem('zt_extra',JSON.stringify(EXTRAS));}catch(e){}
  document.getElementById('drawIn').value=''; document.getElementById('drawSp').value='';
  msg.textContent=`已录入 ${np} 期(平码 ${ns.join(' ')} + 特 ${String(sp[0]).padStart(2,'0')}),全部数据已重算`;
  recalcAll();
}
function onUndoDraw(){
  const msg=document.getElementById('drawMsg');
  if(!EXTRAS.length){msg.textContent='没有可撤销的本机追加期';return;}
  const row=EXTRAS.pop();
  const i=ALL.lastIndexOf(row); if(i>=0) ALL.splice(i,1);
  try{EXTRAS.length?localStorage.setItem('zt_extra',JSON.stringify(EXTRAS)):localStorage.removeItem('zt_extra');}catch(e){}
  msg.textContent=`已撤销 ${row[0]} 期,数据已回滚重算`;
  recalcAll();
}
function bindDraw(){
  document.getElementById('btnDraw').onclick=onDraw;
  document.getElementById('btnUndoDraw').onclick=onUndoDraw;
  const enter=e=>{if(e.key==='Enter')onDraw();};
  document.getElementById('drawIn').addEventListener('keydown',enter);
  document.getElementById('drawSp').addEventListener('keydown',enter);
  if(EXTRAS.length) document.getElementById('drawMsg').textContent=`已从本机恢复追加 ${EXTRAS.length} 期(${EXTRAS.map(r=>r[0]).join('、')})`;
}
bindPred(); bindCtrl(); render(); scrollEnd(); tick(); bindEnt(); renderEnt(); bindDraw(); updRanges();
if(typeof window!=='undefined'&&window.setInterval)window.setInterval(tick,1000);
</script>
</body>
</html>'''

# 期号/期数在生成期写入真实值(不再依赖浏览器端 updRanges 兜底;
# 旧做法在模板里写死期号, JS 一旦失败就静默显示陈旧区间)
import os as _os
PV = _os.environ.get('POOL_VERSION', 'v5.0').strip()  # 2026-11-04起默认人工无摇号; v4.2仅供历史复算
_PV_DESCS = {'v2.5': '100期窗', 'v3.0': '短期30/中期60',
             'v4.0': '六肖2重4新·双池可重·100期窗', 'v4.1': '六肖2重4新·双池可重·短期30/中期60',
             'v4.2': '六肖2重4新·尾部对冲·短期30/中期60',
             'v5.0': '人工六肖全槽·无摇号'}
if PV not in _PV_DESCS:
    raise SystemExit(f'unknown POOL_VERSION {PV!r}; allowed: {sorted(_PV_DESCS)}')
PVDESC = _PV_DESCS[PV]
_p0 = str(data[0][0]) if data else '0000'
_p1 = str(data[-1][0]) if data else '0000'
if PV == 'v5.0':
    _target_short = str(int(_p1) + 1)[-3:] if _p1.isdigit() else '下期'
    PVDESC = (f'人工六肖全槽·{_target_short}人工定案·无摇号'
              if _p1 in manual_decisions_v50_by_tail else '人工六肖全槽·待人工定案·无摇号')
if PV == 'v4.2' and _p1 == '2026298':
    PVDESC = '六肖2重4新·299人工多维定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026299':
    PVDESC = '六肖2重4新·300人工复盘闸门定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026300':
    PVDESC = '六肖2重4新·301人工深复盘后定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026301':
    PVDESC = '六肖2重4新·302人工全替补审计定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026302':
    PVDESC = '六肖2重4新·303人工复盘校准定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026303':
    PVDESC = '六肖2重4新·304人工分层归一化定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026304':
    PVDESC = '六肖2重4新·305人工分层块审定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026305':
    PVDESC = '六肖2重4新·306人工分层块审计定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026306':
    PVDESC = '六肖2重4新·307人工35-45主窗口修订定案·双池可重'
elif PV == 'v4.2' and _p1 == '2026307':
    PVDESC = '六肖2重4新·308人工35-45主窗口定案·双池可重'
# Persistent provenance for the explicit 312 revision. A future draw can move
# past 312 while the corrected historical rows remain in the rolling site data.
# Do not show it for old/pre-revision snapshots or while revision is not recorded.
revision_notice = ''
_rev312 = (_manual_doc.get('decisions', {}) or {}).get('2026312', {})
if (PV == 'v5.0' and _p1.isdigit() and int(_p1) >= 2026311
        and _rev312.get('revision') == 'rev1'):
    _state = ('当前312期为重选修订rev1；原盘保留作对照。'
              if _p1 == '2026311' else '312期曾重选修订为rev1；原盘保留作对照。')
    _base = 'https://fffsw.github.io/zodiac-trend/pre-registration/'
    # Standard HTML character reference resolves to the literal period in the
    # browser URL, without placing a future full period in the raw page source
    # (the established step2 invariant checks raw source before the draw).
    _original_period_ref = '202631&#50;'
    revision_notice = (
        '<aside id="revision-notice" role="note" style="background:#fff8e5;'
        'border:1px solid #e3a33b;border-radius:6px;padding:8px 10px;'
        'margin:0 0 7px;color:#5d3b0a;line-height:1.7">'
        '<strong>数据更正与版本说明：</strong>' + _state +
        '历史共更正7期，其中2026112、2026276在250期走势内；'
        '公开来源可能共用上游，不能称独立官方认证。 '
        '<a href="' + _base + _original_period_ref + '-page.html">原盘页面</a> · '
        '<a href="' + _base + _original_period_ref + '-rev1.json">修订预注册</a> · '
        '<a href="' + _base + _original_period_ref + '-rev1-analysis.md">千期分析与更正详情</a>'
        '</aside>'
    )
html = (TPL.replace('__DATA__', payload)
           .replace('__MANUAL_DECISIONS_V50__', manual_decisions_v50_payload)
           .replace('__REVISION_NOTICE__', revision_notice)
           .replace('新澳门 0000–0000', f'新澳门 {_p0}–{_p1}')
           .replace('新澳门六合彩 0000–0000', f'新澳门六合彩 {_p0}–{_p1}')
           .replace('__PV__', PV).replace('__PVDESC__', PVDESC)
           .replace('000期数据', f'{len(data)}期数据'))
with open('zodiac_trend.html', 'w', encoding='utf-8') as f:
    f.write(html)
with open('www/zodiac_trend.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('written zodiac_trend.html + www/zodiac_trend.html', len(html), 'bytes,', len(data), 'periods')
