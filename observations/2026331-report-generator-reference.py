#!/usr/bin/env python3
"""Compose 330 conditional review, each retained/reconstructed result, and 331 display."""
from pathlib import Path
from html import escape
import hashlib,json,re
R=Path('/home/user');T=R/'archive/task302_330_review';A=R/'archive/task303_331_release';Q=A/'analysis';S=A/'stage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert all(J(p)['status']=='PASS' for p in (T/'analysis/independent_qc.json',Q/'evidence_qc.json',Q/'candidate_qc.json',Q/'manual_stage_receipt.json'));rev=J(T/'analysis/retrospective.json');e=J(Q/'evidence.json');study=J(Q/'six_sign_repeat_study.json');a=J(Q/'candidate_audit.json');m=J(Q/'manual_decision.json');g=rev['historical_groups']['all_37_mixed_sources_versions'];assert g['complete_columns_distribution_0_to_3']==[15,17,4,1] and study['groups']['previous_six_5_seven_6']['n']==345 and m['choice']=='FF01' and not rev['target_331_result_queried_or_used']
def cell(sl):return f"{''.join(sl['required'])} {sl['present_count']}/{sl['needed_count']}（中{''.join(sl['present']) or '—'}；缺{''.join(sl['missing']) or '—'}）"
text='''# 330期复盘、逐期命中与331期人工展示方案

> **先说明口径：**330期号码来自用户，按此前习惯和所列顺序**暂推定前六为正码、第七个单列**；用户尚未明确确认球次。官方来源、开奖日期、目标期生肖号码映射与赛前时点均未认证。如球次有误，下面的结算和统计须重算。栏目只按推定前六结算；不能保证331期命中或收益。

## 一、330期：单、二完整，三肖失败

用户给出：**25馬、35猴、20豬、08豬、30牛、22鷄；第七26蛇**。先前330页的实际留存方案EE01：单馬、二鷄牛、三鷄龍虎；蛇仅替补。

| 栏目 | 前六命中 | 缺失 | 判定 |
|---|---|---|---|
| 单馬 | 25馬，1/1 | 无 | 完整 |
| 二鷄牛 | 22鷄、30牛，2/2 | 无 | 完整 |
| 三鷄龍虎 | 22鷄，1/3 | 龍、虎 | 不完整 |

因此是**两栏完整、一栏不完整**，不能说全盘失败或所有展示肖都没出。共同位鷄出现、二栏已完整，这期不能说“鷄缺导致二、三同断”。蛇只在第七球26出现，且在旧案仅是替补，不能补入正码；猴、豬是推定前六出现但不在旧展示及替补全集的身份，豬出现两球。

**失败与反例：**330前六相对329前六重牛、鷄2肖；上期已披露旧案全栏需要重2或3肖，本期确实重2但仍缺龍、虎，说明**必要条件不是充分条件**。35猴和缺失虎同属奇2路，但猴不是虎；30牛和缺失龍同0路，但牛不是龍，不能用同路或同奇偶代替指定生肖。前六0／1／2路为1／2／3、奇偶2／4，和值140、跨度27。旧二肖鷄、牛同偶的结构风险，本期偶数有4球而没有触发；这不意味着风险不存在。

旧EE01零完整栏当且仅当：**馬缺，且［鷄缺，或（牛缺且龍、虎至少一肖缺）］**。330馬、鷄、牛都出现，故不符合零栏条件。原先保存的12个330关联候选事后套入此结果：8案两栏、4案一栏，没有全栏；只有EE01是原留存展示，其他不是实际发布成绩。相同正式栏位的EE03（三鷄龍蛇）事后套330也是两栏、三肖缺龍蛇，不证明331会有优势。

## 二、逐期核查：留存盘逐栏命中与缺失

以下**37份有留存栏目的版本**：291—308来自留存栏目文件，309—318、320、321、323、325—330来自Git页面快照。来源、版本与保存时间不一，均不能认证赛前发布；296—308按更正后的前六口径，329及330用户号码的前六／第七划分仍属推定。所列生肖全部出现在推定前六，该栏才算完整；替补和第七不自动补栏。

| 期 | 材料来源 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['historical_outcomes']:
 src='留存栏目文件' if x['period']<=2026308 else 'Git页面快照';text+='| '+' | '.join([str(x['period']%1000),src]+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
**319、322、324是结果已知后的事后重建，不能冒称留存原盘，不计入上表37份：**

| 期 | 性质 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['unpublished_reconstructions']:text+='| '+' | '.join([str(x['period']%1000),'事后重建']+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
37份混合来源留存版本，完整0／1／2／3栏分别**15／17／4／1**；单、二、三分别完整**14／10／4**。其中291—308共18份的完整0／1／2／3栏为9／8／0／1，309—330有留存的19份为6／9／4／0。二三共同位缺失16份；另有8份共同位出现，但二、三仍都不完整。26份至少出现一次“指定肖缺失、另一同路同奇偶生肖出现”。这些是混合来源与不同版本材料的事后描述，不是盲测胜率或收益。

**历史全集遗漏沿用已纠正口径：**此前旧复盘曾误把有明确全集的未占正式栏生肖按空处理，导致部分被错分为全集外；原错误明细、原始复核和纠正材料均留存。37份中29份有明确全集，其中14期非栏目肖曾出现在前六：299虎、303兔、304猴、305豬、306龍、308兔／豬、309龍、310鷄、312鷄、314豬、315牛、321豬、323豬、328虎。291—298的8份全集未知，不能当作没有替补；330蛇仅出第七，并非前六替补命中。322豬、324蛇仅属事后重建案的非栏目肖，不计留存。任何替补都不自动补正式栏。

## 三、331人工方案：只调整暴露，不声称变准

| 栏位 | 人工展示 | 假设号码 | 关键约束 |
|---|---|---|---|
| 单肖 | **馬** | 01、13、25、37、49 | 馬须在前六；与两个组合身份错开。 |
| 二肖 | **鷄、牛** | 鷄10、22、34、46；牛06、18、30、42 | 两肖都需出现；鷄是二、三共同位。 |
| 三肖 | **鷄、龍、蛇** | 鷄10、22、34、46；龍03、15、27、39；蛇02、14、26、38 | 三肖都需出现；蛇属2路。 |
| 仅替补 | **虎** | 05、17、29、41 | 不属正式栏，不能自动补缺。 |

正式展示馬、鷄、牛、龍、蛇5肖21码；加虎的六肖全集25码。与330实际展示相比，保留单馬、二鷄牛，把三肖的虎换为蛇。单加三肖完整所需奇／偶身份至少从**3／1**变为**2／2**，但偶数需求增加，不是无代价修复；三栏全完由至少3奇2偶变为至少2奇3偶。二鷄牛仍同偶，前六偶数少于2球时二栏必断；三肖有蛇，前六无2路时三肖必断。**鷄缺仍使二、三同断**；馬缺断单，牛缺断二，龍或蛇缺断三。

零栏当且仅当：**馬缺，且［鷄缺，或（牛缺且龍、蛇至少一肖缺）］**。全栏需馬鷄牛龍蛇，0／1／2路至少2／2／1球；相对330前六5肖，馬、鷄、牛为旧肖，龍、蛇为新肖，全栏只可能重**3或4肖**，重3／4也未必完整；重0／1／2／5则必不全完。重0时三栏都不完整；重5时单、二完整但三肖不完整。这是集合约束，不是对331重肖的预测。蛇在330仅第七出现不证明下一期正码会出；龍或虎上期缺失不证明会回补，馬鷄牛上期出现也不证明会续出。

选择是在看过330、37份留存版本、历史条件组、旧公平模型和330候选事后结算后人工拟定；不是盲选、预注册或经赛前认证。未查询或使用331结果不等于证明赛前。**如果本期球次或目标期生肖映射有误，必须重算。**

### 公平假设模型：新旧分布相同，不是预测提升

在假定目标期号码映射不变、49码等可能且不放回取6码并与此前独立时，枚举全部**13,983,816**种集合。此为条件算术，不是已认证的开奖机制、实际胜率、奖金或收益。

| 方案 | 零完整栏 | 恰好一栏 | 恰好两栏 | 三栏全完 | 单／二／三分别完整 |
|---|---:|---:|---:|---:|---|
| 330旧EE01 | 38.5598% | 52.9297% | 8.1810% | 0.3295% | 49.5198%／15.6616%／5.0989% |
| 331新FF01 | 38.5598% | 52.9297% | 8.1810% | 0.3295% | 49.5198%／15.6616%／5.0989% |

两案均为五码馬单独一栏，另四个不同四码肖组成“共同位＋二／三肖”；在该均匀模型下，把一个四码生肖换成另一个四码生肖不改变完整栏分布。因此新案**没有模型上的整体优势**，仅改变具体身份和条件暴露。FF01事后固定套入截至330近35／40／45条记录，零栏分别11／12／16；窗口重叠且选案时看过资料，不是样本外成绩、未来概率或获利证据。

## 四、330的前六5肖、七球6肖：不能混用条件组

按推定，330前六为馬、猴、豬、牛、鷄5肖，豬出现两球；第七蛇新增一肖，七球6肖。资料内同映射时代、相邻且后续记录已知的条件组只描述已有观察，排除3处映射边界；筛选发生在看到330后，相邻记录可重叠，来源未认证。329→330已纳入，**330→331未纳入分母**。

| 前一期条件 | 已知相邻对 | 前六对前六重0至5／6肖 | 七球对七球重0至5／6／7肖 |
|---|---:|---|---|
| 前六5肖、七球6肖（与330结构一致） | 345 | 8／70／140／107／20／0 | 0／23／84／154／72／12／0 |
| 前六5肖、七球5肖（对照） | 227 | 7／40／106／62／11／1 | 4／30／95／78／19／1 |
| 前六6肖、七球6肖（对照） | 133 | 2／9／45／47／27／3／0 | 0／3／33／54／36／6／1 |
| 前六6肖、七球7肖（对照） | 131 | 2／12／51／47／16／3／0 | 0／7／13／54／41／13／3／0 |

匹配组重2、3各140、107对，是事后频数，不是对331的预测。七球与前六是不同集合，七球重复不能用于正码结算；样本为零不等于理论不可能。330旧肖里馬是五码，其余为四码，故若作均匀假设，相关重复模型须计入不等组大小，不能套用此前5个旧肖都四码的数值。

## 五、12生肖账本：号码与近况仅供核对

W35／W40／W45为截至330的本地推定前六，显示出现期数／球数；重叠窗口不独立。号码按目前资料推定映射列示，**目标期若换表必须重算**，不能视为331官方码表。

| 生肖 | 假设号码 | 最近出现间隔 | W35／40／45（期／球） | 本案角色 |
|---|---|---:|---|---|
'''
roles={'馬':'单；五码，缺馬单断','鷄':'二三共同；缺鷄两组合断','牛':'二；与鷄同偶','龍':'三；狗同奇0不能代龍','蛇':'三；豬同偶2不能代蛇，330仅第七','虎':'仅替补；不补栏','鼠':'全集外；与馬同奇1','兔':'全集外；与鷄同偶1','羊':'全集外；与牛同偶0','猴':'全集外；与虎同奇2','狗':'全集外；与龍同奇0','豬':'全集外；330前六两球'}
for z in list('鼠牛虎兔龍蛇馬羊猴鷄狗豬'):
 x=e['per_zodiac'][z];w='；'.join(f"{x['windows'][str(k)]['periods']}/{x['windows'][str(k)]['balls']}" for k in (35,40,45));text+='| '+' | '.join([z,' '.join(f'{n:02d}' for n in x['numbers']),str(x['last_normal_age']),w,roles[z]])+' |\n'
text+='''
## 六、12个331结构对照

FF01是当前选案，另11案是相关设计而非独立试验。百分比仅为上面的均匀假设；FF12只改替补，正式栏目及其模型分布不变。不能根据事后选择和模型数值声称某案预测较准。

| 案 | 单 | 二 | 三 | 替补 | 全完整 | 零完整 | 主要代价 |
|---|---|---|---|---|---:|---:|---|
'''
for x in a['candidates']:
 r=x['roles'];p=x['ideal_model']['percent'];text+='| '+' | '.join([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],'、'.join(x['reserves']),f"{p['all_columns']:.4f}%",f"{p['no_complete_column']:.4f}%",x['comparison']])+' |\n'
text+='''
## 七、330的12个冻结候选：只作事后对照

这些候选有关联，只有EE01为原留存展示；事后核算不能称其他11案曾实际发布或预测。第七球不计入。

| 案 | 单／二／三 | 单 | 二 | 三 | 完整栏 | 二、三缺失 |
|---|---|---:|---:|---:|---:|---|
'''
for x in rev['candidate_counterfactuals']:
 r=x['roles'];sl=x['slots'];text+='| '+' | '.join([x['id'],r['top']+'／'+r['A']+r['B']+'／'+r['A']+r['C']+r['D']]+[f"{v['present_count']}/{v['needed_count']}" for v in sl]+[str(x['complete_columns']),'二缺'+(''.join(sl[1]['missing']) or '—')+'；三缺'+(''.join(sl[2]['missing']) or '—')])+' |\n'
text+='''
## 八、核验与上线边界

独立复核逐源读取37份留存盘的111栏、单列3份事后重建及330的12个事后对照；独立重算前六5／七球6与其他条件组、12个331设计，并用独立程序直接枚举13,983,816个假设六码集合，交叉核对旧案、新案和条件分布。核验只说明材料、页面与计算的内部一致性，不认证官方来源、实际时间、开奖机制、真实概率、预测或收益。330旧页、报告、已更正历史候补分类及清单均保留；是否上线以实际回执和公网检查为准。

[37期逐栏CSV](archive/task302_330_review/analysis/historical_display_outcomes.csv) · [三期事后重建CSV](archive/task302_330_review/analysis/reconstructed_outcomes_separate.csv) · [330复盘明细](archive/task302_330_review/analysis/retrospective.json) · [逐栏独立核验](archive/task302_330_review/analysis/independent_qc.json) · [全集及非栏目肖逐期核验](archive/task302_330_review/analysis/retained_universe_reserve_audit.csv) · [重建案全集核验](archive/task302_330_review/analysis/reconstructed_universe_reserve_audit.csv) · [330候选事后对照](archive/task302_330_review/analysis/330_candidates_counterfactual.csv) · [331结构比较](archive/task303_331_release/analysis/candidate_audit.csv) · [模型独立核验](archive/task303_331_release/analysis/candidate_qc.json) · [前六／七球条件研究](archive/task303_331_release/analysis/six_sign_repeat_study.json) · [逐对数据](archive/task303_331_release/analysis/six_sign_repeat_pairs.csv) · [12肖账本](archive/task303_331_release/analysis/zodiac_ledger.csv) · [49码账本](archive/task303_331_release/analysis/number_ledger.csv) · [人工方案](archive/task303_331_release/analysis/manual_decision.json) · [直接枚举结果](archive/task303_331_release/analysis/brute_model.json)。
'''
assert len(re.findall(r'^\| \d{3} \|',text,re.M))==40 and all(v in text for v in ('**馬**','**鷄、牛**','**鷄、龍、蛇**','38.5598%','0.3295%','345','227','330→331未纳入分母'))
p=R/'330期复盘_331期方案与逐期核验.md';assert not p.exists();p.write_text(text,encoding='utf8')
esc=escape
hist=''.join('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+esc(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>' for x in rev['historical_outcomes'])
rebuild=''.join('<tr><td>'+str(x['period']%1000)+'</td>'+''.join('<td>'+esc(cell(v))+'</td>' for v in x['slots'])+'<td>'+str(x['complete_columns'])+'</td></tr>' for x in rev['unpublished_reconstructions'])
head='<thead><tr><th>期</th><th>单：命中／缺失</th><th>二：命中／缺失</th><th>三：命中／缺失</th><th>完整栏</th></tr></thead>'
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>330期复盘与331期人工展示</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f6f9;color:#202b3a;font:16px/1.65 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}main{max-width:1040px;margin:auto;padding:26px 18px 52px}h1,h2{line-height:1.3}h1{font-size:clamp(26px,5vw,38px);margin:5px 0 10px}h2{font-size:21px;margin:0 0 10px}p{margin:8px 0 13px}a{color:#174ea6;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:3px solid #a91d27;outline-offset:3px}.eyebrow{font-size:13px;color:#7b3a2f;font-weight:700;letter-spacing:.06em;margin:0}.nav{font-size:14px;margin-bottom:20px}.card{background:#fff;border:1px solid #dce2e9;border-radius:12px;padding:20px;margin:16px 0;box-shadow:0 2px 8px #1f29370a}.accent{border-left:5px solid #a91d27}.decision{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}.decision div{border:1px solid #e5eaf0;border-radius:8px;padding:12px;background:#fafbfd}.decision small{display:block;color:#536174}.decision b{font-size:20px;color:#8f1a25}.note{border-radius:8px;background:#fff7e6;padding:12px 14px;color:#68470d}.muted{color:#525e6d;font-size:14px}.tablewrap{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:650px;font-size:14px}th,td{padding:8px;text-align:left;border-bottom:1px solid #e6eaf0}th{background:#f6f8fb}ul{padding-left:22px;margin:8px 0}li{margin:5px 0}.links{display:flex;flex-wrap:wrap;gap:5px 18px}summary{cursor:pointer;font-weight:700;color:#174ea6;margin:12px 0}details{margin-top:10px}@media(max-width:600px){main{padding:18px 13px 38px}.decision{grid-template-columns:repeat(2,minmax(0,1fr))}.card{padding:16px}}
</style></head><body><main><p class="eyebrow">用户资料复盘 · 无法保证命中</p><h1>330期复盘与331期人工展示</h1><p class="nav"><a href="../zodiac_trend.html">返回走势图</a> · <a href="README.md">完整资料索引</a> · <a href="2026330-index.html">330原版材料</a></p>
<section class="card accent"><h2>331栏位</h2><div class="decision"><div><small>单肖</small><b>馬</b></div><div><small>二肖</small><b>鷄、牛</b></div><div><small>三肖</small><b>鷄、龍、蛇</b></div><div><small>仅替补</small><b>虎</b></div></div><p>单馬、二鷄牛、三鷄龍蛇；虎仅替补，不自动补栏。单馬与两组合错开，但鷄是二、三共同位；鷄缺两组合均不完整。</p><p class="note">330号码由用户提供，前六正码、第七单列是按顺序推定，用户尚未明确确认球次；日期、官方来源、目标期映射及赛前状态均未认证。结构调整不能确保下一期命中或收益。</p></section>
<section class="card"><h2>330复盘：单、二完整，三肖缺龍虎</h2><p>用户给出25馬、35猴、20豬、08豬、30牛、22鷄；暂列第七26蛇。单馬1/1；二鷄牛2/2；三鷄龍虎1/3缺龍、虎。共两栏完整，并非全盘失败；鷄出现，不能说二三同断。蛇只在第七且旧案仅替补，不能补正码。</p><p>330前六相对329重牛、鷄2肖，符合旧案全完的必要条件，但仍缺龍虎，说明必要不等于充分。猴不能代虎，牛不能代龍。二鷄牛同偶的风险未触发，不等于风险不存在。</p></section>
<section class="card"><h2>每期留存盘：命中与缺失</h2><p>37份不同来源和版本留存盘，完整0／1／2／3栏分别15／17／4／1；单／二／三各完整14／10／4。来源与时间未认证，不是盲测胜率。319、322、324为结果已知后的重建，不计入37份。</p><details><summary>展开37份逐期明细</summary><div class="tablewrap"><table id="history">''' +head+'<tbody>'+hist+'''</tbody></table></div></details><details><summary>单列3份事后重建</summary><div class="tablewrap"><table id="recon">'''+head+'<tbody>'+rebuild+'''</tbody></table></div></details><p><strong>历史更正已保留：</strong>37份中29份有明确全集，其中14期有非栏目肖出现在前六；291—298未明确全集，是否命中替补为未知。330蛇仅出第七；322豬、324蛇只属事后重建。非栏目肖不能补栏。</p><p><a href="2026331-retrospective-history.csv">下载37期结算CSV</a> · <a href="2026331-reserve-audit.csv">全集与非栏目肖逐期表</a> · <a href="2026331-reconstructions.csv">下载事后重建CSV</a></p></section>
<section class="card"><h2>风险与条件模型</h2><ul><li>旧三肖虎换蛇，使单加三所需奇／偶至少由3／1变2／2，代价是偶数要求增加。鷄缺二、三同断；二鷄牛均偶，各栏仍不能保证完整。</li><li>三栏全完需要馬鷄牛龍蛇：相对330前六仅重3或4肖时有可能，重3／4仍不保证；无2路则三肖不完整。</li><li>49码等可能、不放回的假设下，331新FF01和330旧EE01零栏都为38.5598%、全栏都为0.3295%；这是模型条件，不是实际胜率或预测改善。</li><li>330推定前六5肖、七球6肖；同组345对与5／5组227对分开，七球不用于正码结算；历史频数不是未来概率。</li></ul><p>12个331设计是在看到330和相关资料后人工设定，未查询331结果；这不能证明赛前或预测能力。330相同结构的EE03事后也只有两栏完整。</p></section>
<section class="card"><h2>完整材料与核验</h2><div class="links"><a href="2026331-analysis.md">完整复盘报告</a><a href="2026331-retrospective-history.csv">逐期结算CSV</a><a href="2026331-reconstructions.csv">事后重建CSV</a><a href="2026331-prior-counterfactuals.csv">330候选事后对照</a><a href="2026331-candidates.csv">331候选结构对照</a><a href="2026331-six-sign-study.json">5／6与其他条件组</a><a href="2026331-six-sign-pairs.csv">逐对数据</a><a href="2026331-retrospective-qc.json">逐栏独立复核</a><a href="2026331-candidates-qc.json">组合独立复核</a><a href="2026331-verify.py">离线复验</a><a href="2026331.sha256">文件清单</a></div></section><p class="muted">历史频率和人工选择不能保证未来结果。模拟手机浏览器不等同真实微信安全认证；如目标期号码映射发生变化，须核实后重算。</p></main></body></html>'''
idx=S/'2026331-index.html';assert not idx.exists();idx.write_text(html,encoding='utf8');print(json.dumps({'status':'PASS_DRAFT_NOT_OFFICIAL_OR_PREDRAW','report':str(p),'report_sha256':H(p),'index':str(idx),'index_sha256':H(idx),'historical_37':len(rev['historical_outcomes']),'reconstructions':len(rev['unpublished_reconstructions']),'candidate_331':len(a['candidates']),'candidate_330_counterfactual':len(rev['candidate_counterfactuals']),'target_331_result_queried_or_used':False},ensure_ascii=False,indent=2))
