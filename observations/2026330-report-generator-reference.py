#!/usr/bin/env python3
"""Compose the conditional 329 review, every retained result, and transparent 330 display."""
from pathlib import Path
from html import escape
import hashlib,json,re
R=Path('/home/user');T=R/'archive/task300_329_review';A=R/'archive/task301_330_release';Q=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert all(J(p)['status']=='PASS' for p in (T/'analysis/independent_qc.json',Q/'evidence_qc.json',Q/'candidate_qc.json',Q/'manual_stage_receipt.json'));rev=J(T/'analysis/retrospective.json');e=J(Q/'evidence.json');study=J(Q/'six_sign_repeat_study.json');a=J(Q/'candidate_audit.json');m=J(Q/'manual_decision.json');g=rev['historical_groups']['all_36_mixed_sources_versions'];assert g['complete_columns_distribution_0_to_3']==[15,17,3,1] and study['groups']['previous_six_5_seven_6']['n']==344 and m['choice']=='EE01' and not rev['target_330_result_queried_or_used']
def cell(sl):return f"{''.join(sl['required'])} {sl['present_count']}/{sl['needed_count']}（中{''.join(sl['present']) or '—'}；缺{''.join(sl['missing']) or '—'}）"
text='''# 329期复盘、逐期命中与330期人工展示方案

> **先说明口径：**用户明确更正这组号码为329期；目前仅按既有习惯和所列顺序**推定前六为正码、第七个单列**，用户尚未明确确认该球次划分。日期、官方来源、目标期生肖号码映射和赛前时点均未经认证；如果球次有误，下面的结算和统计需重算。以下栏目只按推定前六结算；不能保证330命中或收益。

## 一、329为什么三个栏目都不完整

用户给出：**45狗、06牛、46鷄、33狗、31鼠、40兔；第七44豬**。旧329页面留存案DD01：单馬、二虎鷄、三虎鼠羊；蛇仅替补。

| 栏目 | 前六命中 | 缺失 | 判定 |
|---|---|---|---|
| 单馬 | 无，0/1 | 馬 | 不完整 |
| 二虎鷄 | 46鷄，1/2 | 虎 | 不完整 |
| 三虎鼠羊 | 31鼠，1/3 | 虎、羊 | 不完整 |

因此是**零完整栏**，而不是“所有展示生肖都没出现”：鷄和鼠各有命中，但并未凑齐栏目。蛇在推定前六未出；狗、牛、兔不在旧展示及替补全集。44豬暂列第七，不可补入正码栏目。

**直接原因与原先已披露的风险：**虎是二、三共同位，虎缺同时断两组合；馬缺使单栏断，羊缺又使三肖断。旧案三肖虎、鼠、羊全部属于328前六，329前六相对328仅重狗、鼠2肖，重肖不足3时三肖必断的风险上期已披露、本期发生。教训是不能只披露此条件，还要在新案中正视对前一期身份的集中依赖；这不是证据说下期必然重更多或更少。

329前六无2路：0／1／2路为3／3／0，奇偶3／3，和值201、跨度40；第七44豬虽是2路，**不算正码**。31鼠与缺失馬同奇1路，06牛与缺失羊同偶0路，但同路同奇偶不能替代指定生肖。狗在前六出现两球；前六5个不同生肖，加第七豬共6个。

旧DD01零完整栏当且仅当：**馬缺，且［虎缺，或（鷄缺且鼠、羊至少一肖缺）］**。本期符合馬缺、虎缺。上期已保存的12个关联候选事后套入329，8案零栏、4案一栏（DD06、DD07、DD11、DD12）；只有DD01是留存展示，其他不是实际命中盘，事后比较也不能证明330的预测能力。

## 二、逐期核查：每个保留版本的命中与缺失

以下**36份有留存栏目的版本**：291—308来自留存栏目文件，309—318、320、321、323、325—329来自Git页面快照。版本、来源和记录保存时间不同，均不能认证赛前发布；296—308按纠正后的前六口径，用户329六加一仍属推定。栏目只有所列生肖全部出现在前六才算完整，替补和第七不补栏。

| 期 | 材料来源 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['historical_outcomes']:
 src='留存栏目文件' if x['period']<=2026308 else 'Git页面快照';text+='| '+' | '.join([str(x['period']%1000),src]+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
**319、322、324是结果已知后的事后重建，不能冒称留存原盘，不计入上表36份：**

| 期 | 性质 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['unpublished_reconstructions']:text+='| '+' | '.join([str(x['period']%1000),'事后重建']+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
36份混合来源留存版本，完整0／1／2／3栏分别**15／17／3／1**；单、二、三各完整**13／9／4**。二三共同位缺失16份；另有8份共同位出现但二、三仍都不完整。25份至少出现一次“指定肖缺失、另一同路同奇偶生肖出现”。这些是不同版本材料的事后描述，不是盲测胜率或收益。

**遗漏纠正——历史全集与替补不能默认空：**本轮最初重算历史时，程序把历史全集中未占正式栏目生肖统一按空处理，导致一些实际出现在前六的非栏目肖被误分为“全集外”。逐源核对后，36份留存盘中28份有明确全集，其中14期至少一个非栏目肖出现在前六：299虎、303兔、304猴、305豬、306龍、308兔／豬、309龍、310鷄、312鷄、314豬、315牛、321豬、323豬、328虎。291—298的保存记录未明确给出全集，是否命中替补及是否在全集外均标为**未知**，不能按零处理。319、322、324为事后重建，其中322豬、324蛇出现也只能单列为重建案的非栏目肖，不能算留存原盘。原始错误明细及原复核回执已冻结保留；本次纠正不改变任何正式栏目的命中、缺失或36期统计，非栏目肖仍不能自动补栏。

## 三、330人工方案：改变暴露，不声称变准

| 栏位 | 人工展示 | 关键约束 |
|---|---|---|
| 单肖 | **馬** | 馬须在正码；与两个组合错开身份。 |
| 二肖 | **鷄、牛** | 两肖都需在正码；鷄是二、三共同位。 |
| 三肖 | **鷄、龍、虎** | 三肖都需在正码；龍是0路、鷄是1路、虎是2路。 |
| 仅替补 | **蛇** | 不属于正式栏目，不能自动补缺。 |

展示五肖馬、鷄、牛、龍、虎，共21码；加蛇的六肖全集共25码。这次二鷄牛跨1／0路，不要求2路；三肖仍需要虎，即需要至少一个2路。单馬分离不会因为馬缺而必然使三肖也缺，但**鷄缺仍会同时断二、三**。马缺单栏断；牛缺二栏断；龍或虎缺三肖断。零栏当且仅当：**馬缺，且［鷄缺，或（牛缺且龍、虎至少一肖缺）］**。

结构取舍不能只讲好处：二肖鷄、牛都为偶数，前六偶数少于2个时二栏必断；三栏要全完至少有3个奇数、2个偶数，且至少需要0／1／2路2／2／1个。相对329前六的5肖，展示中鷄、牛为旧肖，馬、龍、虎为新肖：三栏全完只可能在前六重**2或3肖**时发生，重0／1／4／5肖必不能全完；重2／3也不保证。若重0或重5，三肖必不完整。以上均为条件结论，不是对重肖数、路数或330号码的预测。

选择是在看到329、36份留存版本、历史条件组及既有公平模型后人工作出，并非盲选或预注册；未查询或使用330结果不等于证明赛前。单选馬、保留鷄、从近期未出肖加入龍虎并不能证明回补或续开。

### 公平假设模型：新旧分布一样，不是预测提升

在假定目标期号码映射不变、49码等可能且不放回取6码并与此前独立时，枚举全部**13,983,816**种集合。这里只是条件算术，不是已认证开奖机制、实际胜率、奖金或收益。

| 方案 | 零完整栏 | 恰好一栏 | 恰好两栏 | 三栏全完 | 单／二／三分别完整 |
|---|---:|---:|---:|---:|---|
| 329旧DD01 | 38.5598% | 52.9297% | 8.1810% | 0.3295% | 49.5198%／15.6616%／5.0989% |
| 330新EE01 | 38.5598% | 52.9297% | 8.1810% | 0.3295% | 49.5198%／15.6616%／5.0989% |

两案都是五码馬单独一栏，另外四个不同四码肖组成“共同位＋二／三肖”；在该均匀模型下，等大小生肖组替换不改变全部栏目分布。所以新案**没有模型上的整体优势**，只是生肖、路数和相对329重肖条件不同。以新案事后固定套入截至329的近35／40／45条，零栏分别11／13／17；窗口重叠且选案时已看过资料，不是样本外成绩、未来概率或获利证据。

## 四、329的前六5肖、七球6肖：不能混用条件组

按推定，329前六为狗、牛、鷄、鼠、兔五肖；第七豬新增一肖，七球共六肖。同映射时代、相邻且后续记录已知的历史条件组，只描述资料内观察，排除3处生肖映射切换边界；筛选发生在看到329后，相邻记录可能重叠，来源未认证；**329→330未纳入分母**。

| 前一期条件 | 已知相邻对 | 前六对前六重0至5／6肖 | 七球对七球重0至5／6／7肖 |
|---|---:|---|---|
| 前六5肖、七球6肖（与329结构一致） | 344 | 8／70／139／107／20／0 | 0／23／84／153／72／12／0 |
| 前六5肖、七球5肖（对照） | 227 | 7／40／106／62／11／1 | 4／30／95／78／19／1 |
| 前六6肖、七球7肖（此前328组，已含328→329） | 131 | 2／12／51／47／16／3／0 | 0／7／13／54／41／13／3／0 |

例如匹配组前六重2与重3分别139、107对；这是事后频数，不是330会重2或3的证明。七球与前六是不同集合，七球重复不能用于正码栏结算；样本中为零也不代表理论不可能。

## 五、12生肖账本：号码与近况仅供核对

W35／W40／W45为截至329的本地前六，显示出现期数／球数；重叠窗口不独立。号码按目前资料推定的映射列示，**目标期若换表必须重算**，不能视为330官方码表。

| 生肖 | 假设号码 | 最近出现间隔 | W35／40／45（期／球） | 本案角色 |
|---|---|---:|---|---|
'''
roles={'馬':'单；五码，缺馬单断','鷄':'二三共同；缺鷄两组合断','牛':'二；羊同偶0不能代牛','龍':'三；狗同奇0不能代龍','虎':'三；猴同奇2不能代虎','蛇':'仅替补；不补栏','鼠':'全集外；与馬同奇1','兔':'全集外；与鷄同偶1','羊':'全集外；与牛同偶0','猴':'全集外；与虎同奇2','狗':'全集外；与龍同奇0','豬':'全集外；329第七、非正码'}
for z in list('鼠牛虎兔龍蛇馬羊猴鷄狗豬'):
 x=e['per_zodiac'][z];w='；'.join(f"{x['windows'][str(k)]['periods']}/{x['windows'][str(k)]['balls']}" for k in (35,40,45));text+='| '+' | '.join([z,' '.join(f'{n:02d}' for n in x['numbers']),str(x['last_normal_age']),w,roles[z]])+' |\n'
text+='''
## 六、12个330结构对照

EE01是当前选案，另11案是相关设计而非独立试验。百分比仅为上面的均匀假设；EE07只改替补，正式栏目及其模型分布不变。不能根据事后选择和模型数值声称某案预测较准。

| 案 | 单 | 二 | 三 | 替补 | 全完整 | 零完整 | 主要代价 |
|---|---|---|---|---|---:|---:|---|
'''
for x in a['candidates']:
 r=x['roles'];p=x['ideal_model']['percent'];text+='| '+' | '.join([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],'、'.join(x['reserves']),f"{p['all_columns']:.4f}%",f"{p['no_complete_column']:.4f}%",x['comparison']])+' |\n'
text+='''
## 七、329的12个冻结候选：只作事后对照

这些候选有关联，只有DD01为留存展示；事后核算不能称其他11案曾实际发布或预测。第七球不计入。

| 案 | 单／二／三 | 单 | 二 | 三 | 完整栏 | 二、三缺失 |
|---|---|---:|---:|---:|---:|---|
'''
for x in rev['candidate_counterfactuals']:
 r=x['roles'];sl=x['slots'];text+='| '+' | '.join([x['id'],r['top']+'／'+r['A']+r['B']+'／'+r['A']+r['C']+r['D']]+[f"{v['present_count']}/{v['needed_count']}" for v in sl]+[str(x['complete_columns']),'二缺'+(''.join(sl[1]['missing']) or '—')+'；三缺'+(''.join(sl[2]['missing']) or '—')])+' |\n'
text+='''
## 八、核验与上线边界

独立复核逐源读取36份留存盘的108栏、单列3份事后重建及329的12个事后对照；独立重算前六5／七球6与其他条件组、12个330设计，并用独立程序直接枚举13,983,816个假设六码集合，交叉核对旧案、新案和条件分布。核验只说明材料、页面与计算的内部一致性，不认证官方来源、实际时间、开奖机制、真实概率、预测或收益。329旧页及报告、既有日期更正与清单均保留；是否上线以实际回执和公网检查为准。

[36期逐栏CSV](archive/task300_329_review/analysis/historical_display_outcomes.csv) · [三期事后重建CSV](archive/task300_329_review/analysis/reconstructed_outcomes_separate.csv) · [329复盘明细](archive/task300_329_review/analysis/retrospective.json) · [逐栏独立核验](archive/task300_329_review/analysis/independent_qc.json) · [全集及非栏目肖逐期核验](archive/task300_329_review/analysis/retained_universe_reserve_audit.csv) · [重建案全集核验](archive/task300_329_review/analysis/reconstructed_universe_reserve_audit.csv) · [遗漏更正独立复核](archive/task300_329_review/analysis/reserve_correction_qc.json) · [329候选事后对照](archive/task300_329_review/analysis/329_candidates_counterfactual.csv) · [330结构比较](archive/task301_330_release/analysis/candidate_audit.csv) · [模型独立核验](archive/task301_330_release/analysis/candidate_qc.json) · [前六／七球条件研究](archive/task301_330_release/analysis/six_sign_repeat_study.json) · [逐对数据](archive/task301_330_release/analysis/six_sign_repeat_pairs.csv) · [12肖账本](archive/task301_330_release/analysis/zodiac_ledger.csv) · [49码账本](archive/task301_330_release/analysis/number_ledger.csv) · [人工方案](archive/task301_330_release/analysis/manual_decision.json) · [直接枚举结果](archive/task301_330_release/analysis/brute_model.json) · [上轮日期更正](archive/task300_329_review/before/328-date-correction.md)。
'''
assert len(re.findall(r'^\| \d{3} \|',text,re.M))==39 and all(v in text for v in ('**馬**','**鷄、牛**','**鷄、龍、虎**','38.5598%','0.3295%','344','227','329→330未纳入分母'))
p=R/'329期复盘_330期方案与逐期核验.md';assert not p.exists();p.write_text(text,encoding='utf8')
esc=escape
hist=''.join('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+esc(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>' for x in rev['historical_outcomes'])
rebuild=''.join('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+esc(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>' for x in rev['unpublished_reconstructions'])
head='<thead><tr><th>期</th><th>单：命中／缺失</th><th>二：命中／缺失</th><th>三：命中／缺失</th><th>完整栏</th></tr></thead>'
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>329期复盘与330期人工展示</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f6f9;color:#202b3a;font:16px/1.65 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}main{max-width:1040px;margin:auto;padding:26px 18px 52px}h1,h2{line-height:1.3}h1{font-size:clamp(26px,5vw,38px);margin:5px 0 10px}h2{font-size:21px;margin:0 0 10px}p{margin:8px 0 13px}a{color:#174ea6;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:3px solid #a91d27;outline-offset:3px}.eyebrow{font-size:13px;color:#7b3a2f;font-weight:700;letter-spacing:.06em;margin:0}.nav{font-size:14px;margin-bottom:20px}.card{background:#fff;border:1px solid #dce2e9;border-radius:12px;padding:20px;margin:16px 0;box-shadow:0 2px 8px #1f29370a}.accent{border-left:5px solid #a91d27}.decision{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}.decision div{border:1px solid #e5eaf0;border-radius:8px;padding:12px;background:#fafbfd}.decision small{display:block;color:#536174}.decision b{font-size:20px;color:#8f1a25}.note{border-radius:8px;background:#fff7e6;padding:12px 14px;color:#68470d}.muted{color:#525e6d;font-size:14px}.tablewrap{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:650px;font-size:14px}th,td{padding:8px;text-align:left;border-bottom:1px solid #e6eaf0}th{background:#f6f8fb}ul{padding-left:22px;margin:8px 0}li{margin:5px 0}.links{display:flex;flex-wrap:wrap;gap:5px 18px}summary{cursor:pointer;font-weight:700;color:#174ea6;margin:12px 0}details{margin-top:10px}@media(max-width:600px){main{padding:18px 13px 38px}.decision{grid-template-columns:repeat(2,minmax(0,1fr))}.card{padding:16px}}
</style></head><body><main><p class="eyebrow">用户资料复盘 · 无法保证命中</p><h1>329期复盘与330期人工展示</h1><p class="nav"><a href="../zodiac_trend.html">返回走势图</a> · <a href="README.md">完整资料索引</a> · <a href="2026329-index.html">329原版材料</a></p>
<section class="card accent"><h2>330栏位</h2><div class="decision"><div><small>单肖</small><b>馬</b></div><div><small>二肖</small><b>鷄、牛</b></div><div><small>三肖</small><b>鷄、龍、虎</b></div><div><small>仅替补</small><b>蛇</b></div></div><p>单馬、二鷄牛、三鷄龍虎；蛇仅替补，不自动补栏。單馬与两组合错开，但鷄是二、三共同位；鷄缺两组合均不完整。</p><p class="note">用户确认号码属于329，前六正码、第七单列是按顺序推定，用户尚未明确确认球次；日期、官方来源、目标期映射及赛前状态均未认证。结构调整不能确保下一期命中或收益。</p></section>
<section class="card"><h2>329失败：三栏均不完整</h2><p>用户给出45狗、06牛、46鷄、33狗、31鼠、40兔；暂列第七44豬。单馬0/1；二虎鷄1/2缺虎；三虎鼠羊1/3缺虎、羊。虎缺使两组合同时不完整，馬缺使单栏不完整；豬只列第七不能补正码。</p><p>329前六相对328重狗、鼠2肖，旧三肖均属328前六，上期已披露的“重不足3则三肖断”风险发生。鼠不能代馬、牛不能代羊；同路同奇偶不等于同一生肖。</p></section>
<section class="card"><h2>每期留存盘：命中与缺失</h2><p>36份不同来源和版本留存盘，完整0／1／2／3栏分别15／17／3／1；单／二／三各完整13／9／4。来源与时间未认证，不是盲测胜率。319、322、324为结果已知后的重建，不计入36份。</p><details><summary>展开36份逐期明细</summary><div class="tablewrap"><table id="history">''' +head+'<tbody>'+hist+'''</tbody></table></div></details><details><summary>单列3份事后重建</summary><div class="tablewrap"><table id="recon">'''+head+'<tbody>'+rebuild+'''</tbody></table></div></details><p><strong>遗漏已纠正：</strong>本轮最初将历史全集的非栏目肖误按空处理；28份有明确全集，其中14期有非栏目肖出现在前六，包括328虎。291—298未明确全集，是否命中替补为未知。322豬、324蛇只属事后重建。各栏命中及36期统计不变；非栏目肖不能补栏。</p><p><a href="2026330-retrospective-history.csv">下载36期结算CSV</a> · <a href="2026330-reserve-audit.csv">全集与非栏目肖逐期表</a> · <a href="2026330-reconstructions.csv">下载事后重建CSV</a></p></section>
<section class="card"><h2>风险与条件模型</h2><ul><li>鷄缺二、三同断；二鷄牛均偶、前六偶数少于2则二栏必断。三肖需要2路，单、二不要求2路。</li><li>三栏全完需要馬鷄牛龍虎：相对329前六仅重2或3肖时有可能，重2／3仍不保证。</li><li>49码等可能、不放回的假设下，新EE01和旧DD01零栏都为38.5598%、全栏都为0.3295%；这是模型条件，不是实际胜率或预测改善。</li><li>329推定前六5肖、七球6肖；同组344对与5／5组227对分开，七球不用于正码结算；历史频数不是未来概率。</li></ul><p>12个330设计是在看到329及历史资料后人工设定，未查询330结果；这不能证明赛前或预测能力。</p></section>
<section class="card"><h2>完整材料与核验</h2><div class="links"><a href="2026330-analysis.md">完整复盘报告</a><a href="2026330-retrospective-history.csv">逐期结算CSV</a><a href="2026330-reconstructions.csv">事后重建CSV</a><a href="2026330-prior-counterfactuals.csv">329候选事后对照</a><a href="2026330-candidates.csv">330候选结构对照</a><a href="2026330-six-sign-study.json">5／6与其他条件组</a><a href="2026330-six-sign-pairs.csv">逐对数据</a><a href="2026330-retrospective-qc.json">逐栏独立复核</a><a href="2026330-candidates-qc.json">组合独立复核</a><a href="2026330-verify.py">离线复验</a><a href="2026330.sha256">文件清单</a><a href="2026328-date-correction.md">既有日期更正</a></div></section><p class="muted">历史频率和人工选择不能保证未来结果。模拟手机浏览器不等同真实微信安全认证；如目标期号码映射发生变化，须核实后重算。</p></main></body></html>'''
idx=S/'2026330-index.html';assert not idx.exists();idx.write_text(html,encoding='utf8');print(json.dumps({'status':'PASS_DRAFT_NOT_OFFICIAL_OR_PREDRAW','report':str(p),'report_sha256':H(p),'index':str(idx),'index_sha256':H(idx),'historical_36':len(rev['historical_outcomes']),'reconstructions':len(rev['unpublished_reconstructions']),'candidate_330':len(a['candidates']),'candidate_329_counterfactual':len(rev['candidate_counterfactuals']),'target_330_result_queried_or_used':False},ensure_ascii=False,indent=2))
