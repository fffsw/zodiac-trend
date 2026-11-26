#!/usr/bin/env python3
"""Explain the 331 revision honestly, including worse hindsight and 37 actual retained displays."""
from pathlib import Path
from html import escape
import hashlib,json,re
R=Path('/home/user');A=R/'archive/task304_331_revision';B=A/'before';Q=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert J(Q/'revision_qc.json')['status']=='PASS' and J(Q/'manual_stage_receipt.json')['status']=='PASS';rev=J(B/'initial-retrospective.json');audit=J(Q/'revision_audit.json');sel=audit['selected'];base=audit['baseline'];assert sel['id']=='GG01' and sel['posthoc_330']['complete_columns']==1 and base['posthoc_330']['complete_columns']==2 and len(rev['historical_outcomes'])==37
def cell(sl):return f"{''.join(sl['required'])} {sl['present_count']}/{sl['needed_count']}（中{''.join(sl['present']) or '—'}；缺{''.join(sl['missing']) or '—'}）"
text='''# 331期重新筛选：330复盘、逐期明细与修订方案

> **口径先行：**330号码由用户提供，按所列顺序和既有习惯**暂推定前六为正码、第七个单列**，用户尚未明确确认球次。官方来源、开奖日期、331目标映射与赛前时点均未认证；若球次有误，相关结算与比较须重算。此次未查询或使用331结果，这不证明方案是在开奖前发布。不能保证命中或收益。

## 一、对用户质疑的回应：原331确实改得少

330的推定前六为**25馬、35猴、20豬、08豬、30牛、22鷄**，第七**26蛇**；前六5个不同生肖，豬两球。330实际留存案EE01为单馬、二鷄牛、三鷄龍虎，结果：单1/1、二2/2、三1/3缺龍虎，**共两栏完整，不是全盘失败**。蛇只在第七且旧案仅替补，不能补入前六栏。

原已上线331初版FF01为单馬、二鷄牛、三鷄龍蛇；五个正式生肖馬鷄牛龍蛇中，四个来自330正式展示，只换了虎为蛇。其中馬、鷄、牛三个还在330前六出现。保留已中栏及改变奇偶结构只是一种人工取舍，并无证据证明保留就是更准；之前对这一点解释不充分，用户质疑有理。

初版三栏都含330前六生肖：若下期前六相对330一个都不重，初版必然零完整栏。共同位鷄缺时二、三均断。以上是结构依赖，不意味着下一期一定少重肖，亦不意味着曾出现的肖一定不再出现。

## 二、对比1—2个上期前六肖后，修订为GG01

| 栏目 | 原331初版 FF01 | 本次修订 GG01 | 假设号码与约束 |
|---|---|---|---|
| 单肖 | 馬 | **馬** | 01、13、25、37、49；与组合错开。 |
| 二肖 | 鷄、牛 | **狗、牛** | 狗09、21、33、45；牛06、18、30、42；同0路、奇偶各一。 |
| 三肖 | 鷄、龍、蛇 | **狗、兔、蛇** | 狗09、21、33、45；兔04、16、28、40；蛇02、14、26、38；各占0／1／2路。 |
| 仅替补 | 虎 | **虎** | 05、17、29、41；不能自动补正式栏。 |

相对原331正式五肖，移除**鷄、龍**、加入**狗、兔**；相对330实际正式五肖馬鷄牛龍虎，保留馬牛、替换鷄龍虎三肖。修订正式五肖馬狗牛兔蛇中，只有**馬、牛**在330推定前六出现；狗、兔、蛇不在前六，蛇虽出现在330第七球，仍不算前六。虎仅替补，不能补缺。

我们比较原案及9个相关设计，其中两案保留1个、七案保留2个330前六肖；这些设计是在看过330、初版、历史资料和既有模型后人工写出的，**不是盲选、预注册或样本外试验**。选GG01是为了从3个前六旧肖降到2个，使三肖均为相对330前六的非重肖、二栏奇偶各一、三肖跨三路，同时与初版正式五肖相比实际更换2个。狗与牛作为具体身份是人工取舍，**没有证据证明其预测能力更强**。

## 三、重点风险：改善一种情形，换来别的代价

1. **共同位仍存在。**狗是二、三共同位，狗缺时两组合同时不完整；馬缺单断，牛缺二断，兔或蛇缺三断。零栏当且仅当：**馬缺，且［狗缺，或（牛缺且兔、蛇至少一肖缺）］**。
2. **二肖路数集中。**狗牛分别奇、偶，但都为0路；前六0路少于两球，二栏必断。旧二鷄牛同偶、新二狗牛同0路，不能只说新案风险更小。
3. **三肖跨三路，但需要2路。**若前六无2路，三肖必断。三栏全完至少需要0／1／2路**2／2／1**球以及**2奇3偶**。
4. **减少重肖依赖而非消除依赖。**相对330前六的5肖，修订全栏只可能在重**2或3肖**时发生；即使重2／3也未必全完。原案全栏只可能重3或4肖。
5. **零重与五重的取舍。**若前六零重肖，原案三栏必断，修订案的三肖狗兔蛇**仍有可能**完整，但并不保证；若重满5肖，原案单、二必完整，修订案只保证单完整、二不一定完整，三肖必断。两者各有不利情形，不是普遍改进。

蛇只在330第七出现，不证明331正码会出；狗、兔未在330前六出现也不证明会回补；馬、牛曾出现不证明会续出。若目标映射变动，以上路数、号码和模型需重算。

## 四、公平假设模型和不利的事后回放

假设49码等可能、不放回取6码且与此前独立，目标映射不变；独立程序直接枚举**13,983,816**种集合。初版和修订案均为一个五码馬单肖，以及四个不同四码生肖构成二、三肖，因此完整栏分布**完全相同**：

| 案 | 零栏 | 恰好一栏 | 恰好两栏 | 三栏全完 |
|---|---:|---:|---:|---:|
| 原331 FF01 | 38.5598% | 52.9297% | 8.1810% | 0.3295% |
| 修订331 GG01 | 38.5598% | 52.9297% | 8.1810% | 0.3295% |

模型只是条件算术，不代表已认证开奖机制、实际胜率、预测优势或收益。零重肖的条件模型中，原案零栏100%，修订案约78.4403%；但这不是零重肖会发生的预测，且五重肖时修订反而失去原案“两栏必完整”的条件。不能以某一种条件下的改善冒称整体更准。

**如实列出不利事后结果：**把GG01事后套回已知330推定前六，单馬1/1、二狗牛1/2缺狗、三狗兔蛇0/3缺狗兔蛇，只有1栏完整；原331初版事后套330为2栏完整。两者都不是330实际发布成绩，不能据此预测331。

把两案固定套入截至330的近35／40／45条记录，零完整栏：初版分别**11／35、12／40、16／45**，修订分别**11／35、14／40、18／45**；修订在后两个窗口反而较差。这些窗口重叠，且选案时已经看过历史，不是独立盲测、未来命中率或收益。不能隐去不利回放，也不能由此证明未来一定较差。

## 五、10个相关结构：不是10次独立试验

“上期前六肖”是330推定前六五个不同生肖；零重零栏及全栏概率只在上述均匀模型内计算。330回放和近45回放都是看过数据后的反事实；**只有EE01是330实际留存展示**，FF01是331初版，GG01是本次修订，其余是比较方案。

| 案 | 单 | 二 | 三 | 替补 | 330前六肖数 | 相对330正式展示更换数 | 零重时零栏（模型） | 330回放完整栏 | 近45回放零栏 |
|---|---|---|---|---|---:|---:|---:|---:|---:|
'''
for x in audit['candidates']:
 r=x['roles'];text+='| '+' | '.join([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],'、'.join(x['reserves']),str(x['previous_normal_count']),str(len(x['changed_relative_to_330_display'])),f"{x['conditional_repeat'][0]['zero_pct']:.4f}%",str(x['posthoc_330']['complete_columns']),str(x['posthoc_fixed_windows']['45']['complete_0_1_2_3'][0])])+' |\n'
text+='''
例如GG02零重情形下也能有三肖完整，近45回放零栏13次，少于GG01的18次；但GG02全栏至少需要3个1路、这些均为事后观察，并不能证明GG02对331更准。GG09虽只保留2个上期前六肖，共同位仍是上期鷄，零重肖仍然必零栏：仅数替换数量本身不足以判断结构。

## 六、逐期留存盘：每栏命中与缺失

以下37份不同来源留存版本：291—308来自留存栏目文件，309—318、320、321、323、325—330来自Git页面快照；来源、保存时间及赛前状态均未认证。只按各期留存栏及推定前六结算，不把替补或第七自动补栏，不能当成盲测胜率。

| 期 | 来源 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['historical_outcomes']:
 src='留存栏目文件' if x['period']<=2026308 else 'Git页面快照';text+='| '+' | '.join([str(x['period']%1000),src]+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
**319、322、324是结果已知后的事后重建，单列、不计入上表：**

| 期 | 性质 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['unpublished_reconstructions']:text+='| '+' | '.join([str(x['period']%1000),'事后重建']+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
37份完整0／1／2／3栏分别**15／17／4／1**；单、二、三各完整14／10／4。全集分类沿用已纠正结果：29份全集明确、8份未知；14期已知全集中非栏目肖出现在前六。291—298全集未知，不能当无替补；330蛇只出第七。322豬、324蛇只属事后重建。原公开初版、原清单、原复盘及历史纠正均不覆盖。

## 七、重肖历史只作描述

330前六5肖、七球6肖；同映射时代、相邻且后续已知的历史同组345对，前六对前六重0—5肖分别**8／70／140／107／20／0**。5／5的227对、6／6的133对和6／7的131对均另列；排除3处映射边界。329→330已在分母内，330→331未纳入。筛选发生在看到330之后，重叠记录、资料来源与时点均未认证，样本频数不是对331的概率预测；七球不能用于前六结算。

## 八、核验与材料

已独立重算10个结构的完整栏分布、重0—5条件及历史回放；独立程序直接枚举13,983,816个假设集合，交叉核对原案与修订案；逐项核对37份留存盘及3份事后重建。核验只证明材料及内部算术一致，不认证来源、实际开奖时间、预测优势、收益或真实微信安全。初版公开清单与页面可隔离重放；旧本地331核验ZIP未出现在本次工作区快照，不能冒称原包已恢复，新的复核材料另行打包。

[逐期留存CSV](archive/task304_331_revision/before/initial-retrospective-history.csv) · [事后重建CSV](archive/task304_331_revision/before/initial-reconstructions.csv) · [原331完整复盘](330期复盘_331期方案与逐期核验.md) · [10案结构表](archive/task304_331_revision/analysis/revision_candidate_comparison.csv) · [结构计算明细](archive/task304_331_revision/analysis/revision_audit.json) · [独立复核](archive/task304_331_revision/analysis/revision_qc.json) · [直接枚举结果](archive/task304_331_revision/analysis/revision_brute_model.json) · [原331条件组](archive/task304_331_revision/before/initial-repeat-study.json) · [原逐期全集及替补](archive/task304_331_revision/before/initial-reserve-audit.csv) · [原331方案](archive/task304_331_revision/before/initial-manual-decision.json)。
'''
assert len(re.findall(r'^\| \d{3} \|',text,re.M))==40 and all(s in text for s in ('**狗、牛**','**狗、兔、蛇**','18／45','16／45','不证明331','13,983,816'))
report=R/'331期重新筛选与330期逐期复盘.md';assert not report.exists();report.write_text(text,encoding='utf8')
head='<thead><tr><th>期</th><th>单：命中／缺失</th><th>二：命中／缺失</th><th>三：命中／缺失</th><th>完整栏</th></tr></thead>'
hist=''.join('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+escape(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>' for x in rev['historical_outcomes']);rebuild=''.join('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+escape(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>' for x in rev['unpublished_reconstructions'])
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>331期重新筛选与330期复盘</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f6f9;color:#202b3a;font:16px/1.65 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}main{max-width:1040px;margin:auto;padding:26px 18px 52px}h1,h2{line-height:1.3}h1{font-size:clamp(26px,5vw,38px);margin:5px 0 10px}h2{font-size:21px;margin:0 0 10px}p{margin:8px 0 13px}a{color:#174ea6;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:3px solid #a91d27;outline-offset:3px}.eyebrow{font-size:13px;color:#7b3a2f;font-weight:700;letter-spacing:.06em;margin:0}.nav{font-size:14px;margin-bottom:20px}.card{background:#fff;border:1px solid #dce2e9;border-radius:12px;padding:20px;margin:16px 0;box-shadow:0 2px 8px #1f29370a}.accent{border-left:5px solid #a91d27}.decision{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}.decision div{border:1px solid #e5eaf0;border-radius:8px;padding:12px;background:#fafbfd}.decision small{display:block;color:#536174}.decision b{font-size:20px;color:#8f1a25}.note{border-radius:8px;background:#fff7e6;padding:12px 14px;color:#68470d}.muted{color:#525e6d;font-size:14px}.tablewrap{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:650px;font-size:14px}th,td{padding:8px;text-align:left;border-bottom:1px solid #e6eaf0}th{background:#f6f8fb}ul{padding-left:22px;margin:8px 0}li{margin:5px 0}.links{display:flex;flex-wrap:wrap;gap:5px 18px}summary{cursor:pointer;font-weight:700;color:#174ea6;margin:12px 0}details{margin-top:10px}@media(max-width:600px){main{padding:18px 13px 38px}.decision{grid-template-columns:repeat(2,minmax(0,1fr))}.card{padding:16px}}
</style></head><body><main><p class="eyebrow">用户资料复盘 · 无法保证命中</p><h1>331期重新筛选与330期复盘</h1><p class="nav"><a href="../zodiac_trend.html">返回走势图</a> · <a href="README.md">完整资料索引</a> · <a href="2026331-index.html">331初版材料</a></p>
<section class="card accent"><h2>331修订栏位</h2><div class="decision"><div><small>单肖</small><b>馬</b></div><div><small>二肖</small><b>狗、牛</b></div><div><small>三肖</small><b>狗、兔、蛇</b></div><div><small>仅替补</small><b>虎</b></div></div><p>单馬、二狗牛、三狗兔蛇；虎仅替补，不自动补栏。相比初版正式五肖，移除鷄龍、加入狗兔；只保留330推定前六中的馬、牛。</p><p class="note">330号码由用户提供，前六正码、第七单列是按顺序推定，用户尚未明确确认球次；日期、官方来源、目标映射及赛前状态均未认证。不能保证下一期命中或收益。</p></section>
<section class="card"><h2>330真实留存与事后对照</h2><p>330实际留存单馬1/1、二鷄牛2/2、三鷄龍虎1/3缺龍、虎，共两栏完整，非全盘失败。26蛇暂列第七，不能补前六。</p><p>修订案事后套330：单馬1/1、二狗牛1/2缺狗、三狗兔蛇0/3，只有一栏完整；原331初版事后套330为两栏。这些事后对照都不是330实际发布成绩。</p></section>
<section class="card"><h2>结构改善与代价</h2><ul><li>若前六相对330零重肖，原案必零栏，修订三肖仍可能完整，并不保证；若重满5肖，原案单、二必完整，修订只保证单，三肖必断。</li><li>狗是二、三共同位，狗缺使两栏同断；二狗牛同0路，前六0路少于两球必断二；无2路必断三。全栏重2或3肖是必要非充分条件。</li><li>49码等可能不放回模型下，新旧两案零栏均38.5598%、全完均0.3295%；不是实际胜率或预测改善。</li><li>截至330近45条事后固定回放：初版零栏16次，修订18次，后者更差；窗口重叠、选案时资料已知，不是盲测或未来概率。</li></ul></section>
<section class="card"><h2>每期留存盘：命中与缺失</h2><p>37份混合来源留存盘，完整0／1／2／3栏分别15／17／4／1；319、322、324是事后重建，不计入37份。来源与赛前时间未认证，不是盲测胜率。</p><details><summary>展开37份逐期明细</summary><div class="tablewrap"><table id="history">'''+head+'<tbody>'+hist+'''</tbody></table></div></details><details><summary>单列3份事后重建</summary><div class="tablewrap"><table id="recon">'''+head+'<tbody>'+rebuild+'''</tbody></table></div></details><p>29份有明确全集，291—298共8份全集未知；14期有非栏目肖在前六出现，不能自动补栏。</p></section>
<section class="card"><h2>完整材料与核验</h2><div class="links"><a href="2026331-rev1-analysis.md">完整修订复盘报告</a><a href="2026331-rev1-candidates.csv">10案结构对照</a><a href="2026331-retrospective-history.csv">37份逐期结算CSV</a><a href="2026331-reconstructions.csv">事后重建CSV</a><a href="2026331-reserve-audit.csv">全集与非栏目肖逐期表</a><a href="2026331-rev1-audit.json">条件计算明细</a><a href="2026331-rev1-qc.json">独立复核</a><a href="2026331-rev1-brute.json">直接枚举结果</a><a href="2026331-six-sign-study.json">前六／七球条件组</a><a href="2026331-rev1-verify.py">离线复验</a><a href="2026331-rev1.sha256">修订文件清单</a></div></section><p class="muted">选号、历史频率及模型都无法保证结果；未查询331不证明赛前。模拟手机不等于真实微信安全认证。</p></main></body></html>'''
idx=S/'2026331-rev1-index.html';idx.write_text(html,encoding='utf8');print(json.dumps({'status':'PASS_DRAFT','report_sha256':H(report),'index_sha256':H(idx),'retained':37,'reconstructed':3,'candidates':10,'target_331_result_queried_or_used':False},ensure_ascii=False,indent=2))
