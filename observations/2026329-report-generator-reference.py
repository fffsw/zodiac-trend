#!/usr/bin/env python3
"""Generate the honest, human-readable 328 retrospective and 329 decision and index."""
from pathlib import Path
from html import escape
import hashlib,json,re
R=Path('/home/user');T=R/'archive/task298_328_review';Q=R/'archive/task299_329_release/analysis';S=R/'archive/task299_329_release/stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert all(J(p)['status']=='PASS' for p in (T/'analysis/independent_qc.json',Q/'evidence_qc.json',Q/'candidate_audit_qc.json',Q/'manual_stage_receipt.json'));rev=J(T/'analysis/retrospective.json');e=J(Q/'evidence.json');study=J(Q/'six_sign_repeat_study.json');a=J(Q/'candidate_audit.json');m=J(Q/'manual_decision.json');g=rev['historical_groups']['all_35_mixed_sources_versions'];assert g['complete_columns_distribution_0_to_3']==[14,17,3,1] and study['groups']['previous_six_6_seven_7']['n']==130 and m['choice']=='DD01'
def cell(sl):return f"{''.join(sl['required'])} {sl['present_count']}/{sl['needed_count']}（中{''.join(sl['present']) or '—'}；缺{''.join(sl['missing']) or '—'}）"
text='''# 328期复盘、逐期命中与329期人工展示方案

> **口径与边界：**328号码来自用户；依照原有惯例及列示顺序，暂将前六个视为正码、第七个单列，用户并未另外认证此划分。日期未知，官方来源、目标期号码映射和赛前时点均未经认证。所有命中结算只看前六；不能保证329命中或收益。

## 一、328：三栏为什么都没完整

用户给出：**15龍、21狗、31鼠、05虎、12羊、47猴；第七06牛**。原328留存展示：单馬、二狗鷄、三狗馬蛇；虎、牛是替补。

| 栏目 | 前六已出现 | 缺失 | 判定 |
|---|---|---|---|
| 单馬 | 无，0/1 | 馬 | 不完整 |
| 二狗鷄 | 21狗，1/2 | 鷄 | 不完整 |
| 三狗馬蛇 | 21狗，1/3 | 馬、蛇 | 不完整 |

**零完整栏。**共同位狗确实出现，但二缺鷄、三缺馬蛇；單馬与三肖共用馬，馬未出同时使单、三不完整。31鼠和馬同属奇1路，也不能代替馬。虎虽为328替补且在前六出现，但替补不自动补入栏目；牛只在第七球，同样不能计入前六栏目。

328前六相对327前六重复**狗、鼠、虎、羊4肖**，新肖为龍、猴。此前有关“重5至少一栏、重6恰好两栏”的结论只在各自条件成立时适用，本期重4，不受那两个结论保障。前六和值131、跨度42、0/1/2路3/1/2、奇偶5/1，仅为结果描述。

旧CC01三栏零完整的精确条件：**馬缺，且狗或鷄至少缺一**。328满足馬缺、鷄缺；其余部分命中不等于栏目完整。已冻结的12个328候选，事后套入本期均零完整栏；这只是检查已留存的有限对照，不证明它们对未来有效，也不能用当期出现的虎或鼠证明下期会出现。

## 二、每期留存栏目的命中和失败

以下为**35份有留存栏目证据的版本**：291—308是留存栏目文件；309—318、320、321、323、325—328为Git页面快照。版本和来源不同，实际保存文件或记录提交不等于证明赛前发布；296—308沿用纠正后的前六结算。每个栏目必须全部命中才算完整，七球另记，不补栏。

| 期 | 材料来源 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['historical_outcomes']:
 src='留存栏目文件' if x['period']<=2026308 else 'Git页面快照';text+='| '+' | '.join([str(x['period']%1000),src]+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
**319、322、324是结果已知后的事后重建，不是已证实的原先发布盘，也不计入上表35份：**

| 期 | 性质 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['unpublished_reconstructions']:text+='| '+' | '.join([str(x['period']%1000),'事后重建']+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
35份留存版本中，完整0／1／2／3栏分别 **14／17／3／1**；单、二、三各完整 **13／9／4**。共同位缺失15份；另外8份共同位出现但二、三都不完整，其中包括327及328。24份至少出现一次“指定肖缺失而同路同奇偶的另一生肖出现”。这是不同来源、不同版本的材料内总结，不能当盲测胜率。

## 三、329选择与失败风险：修正结构，不承诺命中

| 栏位 | 人工展示 | 必须满足与风险 |
|---|---|---|
| 单肖 | **馬** | 馬必须在正码；不再与二、三共用身份。 |
| 二肖 | **虎、鷄** | 两者都要在正码；虎为二、三共同位。 |
| 三肖 | **虎、鼠、羊** | 三者都要在正码；虎缺会连带二、三不完整。 |
| 仅替补 | **蛇** | 不属于以上任何正式栏目，不能自动补缺。 |

展示身份为馬、虎、鷄、鼠、羊共21码；加替补蛇，组六全集25码。把单馬从三肖中拆开，可以避免“只因馬缺就必然单、三联断”，但**虎缺仍会同时断二、三**。零栏当且仅当：**馬缺，且［虎缺，或（鷄缺且鼠、羊至少一肖缺）］**；这仍可能发生。

二虎鷄跨2／1路且一奇一偶，三虎鼠羊跨2／1／0路；同一路或同奇偶并不能替代具体生肖。尤其馬和鼠都是奇1路，两者身份不同；全部完整至少需要两个奇1号码、至少三个奇数和两个偶数。不能只看路、奇偶、遗漏或热冷就断言具体生肖。

相对328前六，五个展示身份中的虎、鼠、羊是旧肖，馬、鷄为新肖。若329前六与328前六重肖**少于3**，三肖必不完整；三栏全完仅在重**3或4肖**时有可能，重0／1／2／5／6必不能全完，重3／4也不保证。若恰好重6，则前六必含虎鼠羊，三肖完整，但单馬和二鷄不完整；这是条件推论，不是预测重6。

选择是在看到328结果、逐期资料、条件样本和既有模型后人工进行，不是盲选或预注册；未查询或使用329结果，也不能据此认证赛前时点。把328出现的虎列为共同位、把未出的馬和鷄列入，并没有证明它们会继续出现或回补。

### 明确目标取舍：公平模型不是实际胜率

在“目标期继续采用当前号码映射、49码等可能、不放回取6个且与前期独立”的假设下，组合数按全部 **13,983,816** 组六集合计数；机制与映射未经认证，不计算奖金、成本或收益。

| 方案 | 零完整栏 | 恰好一栏 | 恰好两栏 | 三栏全完整 | 至少一栏 | 至少两栏 |
|---|---:|---:|---:|---:|---:|---:|
| 328旧CC01 | 40.9686% | 48.3900% | 8.9830% | 1.6585% | 59.0314% | 10.6414% |
| 329新DD01 | 38.5598% | 52.9297% | 8.1810% | 0.3295% | 61.4402% | 8.5105% |

此假设下，DD01的零栏比例降低约2.4088个百分点，但三栏全完也减少约1.3290个百分点；**不是无代价优化，更不代表实际预测改善**。单／二／三完整的模型数值分别为49.5198%／15.6616%／5.0989%。对当前选案事后固定套入截至328的近35／40／45条，零完整栏为8／10／13期；窗口重叠、选案时已看过资料，不是样本外成绩或未来概率。

## 四、328是“前六6肖、七球7肖”：重肖样本必须分组

328前六为龍、狗、鼠、虎、羊、猴6肖；第七牛新增一肖，因此七球共7肖。不能沿用上轮327的“前六6肖且七球6肖”筛选结果来冒称同一条件。

2024以来资料按保存的当期生肖标签，排除号码映射切换边界、核对相邻期，且只纳入下一行已知的记录；筛选在看到328后进行，历史来源未经认证、相邻记录可能重叠，不能推断下一期概率。328→329未纳入分母。

| 前一期条件 | 已知相邻对数 | 前六对前六重0至6肖（期数） | 七球对七球重0至6／7肖（期数） |
|---|---:|---|---|
| 前六6肖、七球7肖（与328结构一致） | 130 | 2／12／50／47／16／3／0 | 0／7／13／53／41／13／3／0 |
| 前六6肖、七球6肖（对照） | 133 | 2／9／45／47／27／3／0 | 0／3／33／54／36／6／1 |

两组七球比较的上限不同：前者理论上可重7，后者最多重6；样本为0不等于不可能。七球统计不进入前六栏目结算。

## 五、12肖账本：号码与近况仅作核对

W35／W40／W45为截至328的本地前六，显示出现期数／球数；窗口重叠。目标期映射若改变，应重新核验并重算，不能把当前码表当作已认证的329官方规则。

| 生肖 | 当前假设号码 | 近龄 | W35／40／45（期／球） | 本案角色 |
|---|---|---:|---|---|
'''
roles={'馬':'单；五码，缺馬单断','虎':'二三共同；缺虎两组合断','鷄':'二；兔同偶1不能代鷄','鼠':'三；馬同奇1不能代鼠','羊':'三；牛同偶0不能代羊','蛇':'仅替补；不补栏','牛':'全集外；328第七不是正码','兔':'全集外；与鷄同偶1','龍':'全集外；与狗同奇0','猴':'全集外；与虎同奇2','狗':'全集外；与龍同奇0','豬':'全集外；与蛇同偶2'}
for z in list('鼠牛虎兔龍蛇馬羊猴鷄狗豬'):
 x=e['per_zodiac'][z];w='；'.join(f"{x['windows'][str(k)]['periods']}/{x['windows'][str(k)]['balls']}" for k in (35,40,45));text+='| '+' | '.join([z,' '.join(f'{n:02d}' for n in x['numbers']),str(x['last_normal_age']),w,roles[z]])+' |\n'
text+='''
## 六、12个329结构对照

DD01为当前选案，另外11案是相关结构对照而非独立试验。表中百分比仅为上述公平假设；DD10只换替补，正式栏目及其模型概率不变。

| 案 | 单 | 二 | 三 | 替补 | 全完整 | 零完整 | 主要代价 |
|---|---|---|---|---|---:|---:|---|
'''
for x in a['candidates']:
 r=x['roles'];p=x['ideal_model']['percent'];text+='| '+' | '.join([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],'、'.join(x['reserves']),f"{p['all_columns']:.4f}%",f"{p['no_complete_column']:.4f}%",x['comparison']])+' |\n'
text+='''
## 七、328的12个冻结候选：仅作事后对照

这些候选关联且仅CC01为留存实际展示；事后结算不能称作其他11案的实际发布或预测。缺失列为具体生肖，第七球不计入。

| 案 | 单／二／三 | 单 | 二 | 三 | 完整栏 | 二、三缺失 |
|---|---|---:|---:|---:|---:|---|
'''
for x in rev['candidate_counterfactuals']:
 r=x['roles'];sl=x['slots'];text+='| '+' | '.join([x['id'],r['top']+'／'+r['A']+r['B']+'／'+r['A']+r['C']+r['D']]+[f"{v['present_count']}/{v['needed_count']}" for v in sl]+[str(x['complete_columns']),'二缺'+(''.join(sl[1]['missing']) or '—')+'；三缺'+(''.join(sl[2]['missing']) or '—')])+' |\n'
text+='''
## 八、核验与上线边界

独立复核逐个读取原栏目文件与页面快照，重算35份留存盘的105个栏目、单列3份事后重建和328的12个事后对照；另按用户行重算两个条件样本，使用不同算法复核12个329案，并直接枚举13,983,816个假设六码集合核对新旧案。校验仅说明材料、页面和计算内部一致，不认证官方来源、真实时间、开奖机制、实际胜率或未来结果。上一期页面和报告、日期更正、旧清单均保留；上线以实际回执及公网检查为准。

[35期逐栏CSV](archive/task298_328_review/analysis/historical_display_outcomes.csv) · [三期事后重建CSV](archive/task298_328_review/analysis/reconstructed_outcomes_separate.csv) · [328复盘明细](archive/task298_328_review/analysis/retrospective.json) · [逐栏独立核验](archive/task298_328_review/analysis/independent_qc.json) · [328候选事后对照](archive/task298_328_review/analysis/328_candidates_counterfactual.csv) · [329结构比较](archive/task299_329_release/analysis/candidate_audit.csv) · [模型独立核验](archive/task299_329_release/analysis/candidate_audit_qc.json) · [六肖／七肖条件研究](archive/task299_329_release/analysis/six_sign_repeat_study.json) · [逐对数据](archive/task299_329_release/analysis/six_sign_repeat_pairs.csv) · [12肖账本](archive/task299_329_release/analysis/zodiac_ledger.csv) · [49码账本](archive/task299_329_release/analysis/number_ledger.csv) · [人工方案](archive/task299_329_release/analysis/manual_decision.json) · [直接枚举结果](archive/task299_329_release/analysis/brute_model.json) · [上轮日期更正](archive/task295_328_release/date_correction/日期措辞更正.md)。
'''
assert len(re.findall(r'^\| \d{3} \|',text,re.M))==38 and all(v in text for v in ('**馬**','**虎、鷄**','**虎、鼠、羊**','38.5598%','0.3295%','130','133','328→329未纳入分母'))
p=R/'328期复盘_329期方案与逐期核验.md';assert not p.exists();p.write_text(text,encoding='utf8')
# HTML index is self-contained and has all 35 records plus 3 explicitly separated reconstructions.
esc=escape
hist=''.join('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+esc(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>' for x in rev['historical_outcomes'])
rebuild=''.join('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+esc(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>' for x in rev['unpublished_reconstructions'])
head='<thead><tr><th>期</th><th>单：命中／缺失</th><th>二：命中／缺失</th><th>三：命中／缺失</th><th>完整栏</th></tr></thead>'
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>328期复盘与329期人工展示</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f6f9;color:#202b3a;font:16px/1.65 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}main{max-width:1040px;margin:auto;padding:26px 18px 52px}h1,h2{line-height:1.3}h1{font-size:clamp(26px,5vw,38px);margin:5px 0 10px}h2{font-size:21px;margin:0 0 10px}p{margin:8px 0 13px}a{color:#174ea6;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:3px solid #a91d27;outline-offset:3px}.eyebrow{font-size:13px;color:#7b3a2f;font-weight:700;letter-spacing:.06em;margin:0}.nav{font-size:14px;margin-bottom:20px}.card{background:#fff;border:1px solid #dce2e9;border-radius:12px;padding:20px;margin:16px 0;box-shadow:0 2px 8px #1f29370a}.accent{border-left:5px solid #a91d27}.decision{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}.decision div{border:1px solid #e5eaf0;border-radius:8px;padding:12px;background:#fafbfd}.decision small{display:block;color:#536174}.decision b{font-size:20px;color:#8f1a25}.note{border-radius:8px;background:#fff7e6;padding:12px 14px;color:#68470d}.muted{color:#525e6d;font-size:14px}.tablewrap{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:650px;font-size:14px}th,td{padding:8px;text-align:left;border-bottom:1px solid #e6eaf0}th{background:#f6f8fb}ul{padding-left:22px;margin:8px 0}li{margin:5px 0}.links{display:flex;flex-wrap:wrap;gap:5px 18px}summary{cursor:pointer;font-weight:700;color:#174ea6;margin:12px 0}details{margin-top:10px}@media(max-width:600px){main{padding:18px 13px 38px}.decision{grid-template-columns:repeat(2,minmax(0,1fr))}.card{padding:16px}}
</style></head><body><main><p class="eyebrow">用户资料复盘 · 无法保证命中</p><h1>328期复盘与329期人工展示</h1><p class="nav"><a href="../zodiac_trend.html">返回走势图</a> · <a href="README.md">完整资料索引</a> · <a href="2026328-deep-index.html">328原版与深度复核</a></p>
<section class="card accent"><h2>329栏位</h2><div class="decision"><div><small>单肖</small><b>馬</b></div><div><small>二肖</small><b>虎、鷄</b></div><div><small>三肖</small><b>虎、鼠、羊</b></div><div><small>仅替补</small><b>蛇</b></div></div><p>单馬、二虎鷄、三虎鼠羊；蛇仅替补，不自动补栏。單馬与两组合错开，但虎仍为二、三共同位；虎缺两组合均不完整。</p><p class="note">结构调整不能确保下一期命中或收益。用户328号码按顺序推定前六正码、第七单列；日期、官方来源、目标期映射及赛前状态均未认证。</p></section>
<section class="card"><h2>328失败：三栏均不完整</h2><p>用户给出15龍、21狗、31鼠、05虎、12羊、47猴；第七06牛单列。单馬0/1；二狗鷄1/2缺鷄；三狗馬蛇1/3缺馬、蛇。共同狗出现，但馬未出使单、三同时断。虎虽为替补且在前六出现，不自动补栏；第七牛不算正码。</p><p>328前六相对327重狗、鼠、虎、羊4肖。以往重5、重6的条件推论不适用于本期；328之前留存的12个候选事后套入本期全为零完整栏，不代表预测。</p></section>
<section class="card"><h2>每期留存盘：命中与缺失</h2><p>35份不同来源及版本的留存盘，完整0／1／2／3栏分别14／17／3／1；单／二／三各完整13／9／4。来源与时间未认证，不是盲测胜率。319、322、324为结果已知后的重建，不计入35份。</p><details><summary>展开35份逐期明细</summary><div class="tablewrap"><table id="history">''' +head+'<tbody>'+hist+'''</tbody></table></div></details><details><summary>单列3份事后重建</summary><div class="tablewrap"><table id="recon">'''+head+'<tbody>'+rebuild+'''</tbody></table></div></details><p><a href="2026329-retrospective-history.csv">下载35期结算CSV</a> · <a href="2026329-reconstructions.csv">下载事后重建CSV</a></p></section>
<section class="card"><h2>风险与模型取舍</h2><ul><li>三栏全完需要馬虎鷄鼠羊：相对328前六重3或4肖才有可能，重3／4也不保证；重少于3肖时三肖必不完整。</li><li>公平假设下：旧CC01零栏40.9686%、全栏1.6585%；新DD01零栏38.5598%、全栏0.3295%。目标取舍，不是实际胜率或获利。</li><li>当前前六6肖、七球7肖；分别核对130组6／7和133组6／6历史条件，不能混用，七球不用于正码结算。</li></ul><p>映射及49码等可能、不放回仅是模型假设；12案在看到328及历史后人工设定，未查询329，不可据此证明赛前或预测能力。</p></section>
<section class="card"><h2>完整材料与核验</h2><div class="links"><a href="2026329-analysis.md">完整复盘报告</a><a href="2026329-retrospective-history.csv">逐期结算CSV</a><a href="2026329-reconstructions.csv">事后重建CSV</a><a href="2026329-prior-counterfactuals.csv">328候选事后对照</a><a href="2026329-candidates.csv">329候选结构对照</a><a href="2026329-six-sign-study.json">6／7与6／6条件研究</a><a href="2026329-six-sign-pairs.csv">逐对数据</a><a href="2026329-retrospective-qc.json">逐栏独立复核</a><a href="2026329-candidates-qc.json">组合独立复核</a><a href="2026329-verify.py">离线复验</a><a href="2026329.sha256">文件清单</a><a href="2026328-date-correction.md">既有日期更正</a></div></section><p class="muted">历史频率和人工选择不能保证未来结果。模拟手机浏览器不等同真实微信安全认证；如目标期号码映射发生变化，须核实后重算。</p></main></body></html>'''
idx=S/'2026329-index.html';idx.write_text(html,encoding='utf8');print(json.dumps({'status':'PASS_DRAFT_NOT_OFFICIAL_OR_PREDRAW','report':str(p),'report_sha256':H(p),'index':str(idx),'index_sha256':H(idx),'historical_35':len(rev['historical_outcomes']),'reconstructions':len(rev['unpublished_reconstructions']),'candidate_329':len(a['candidates']),'candidate_328_counterfactual':len(rev['candidate_counterfactuals']),'target_329_result_queried_or_used':False},ensure_ascii=False,indent=2))
