#!/usr/bin/env python3
"""Build readable conditional 327 review, all saved columns, and 328 structural comparison."""
from pathlib import Path
import hashlib,json,re
R=Path('/home/user');Q=R/'archive/task295_328_release/analysis';T=R/'archive/task294_327_review/analysis';J=lambda p:json.loads(p.read_text());assert all(J(Q/n)['status']=='PASS' for n in ('evidence_qc.json','six_sign_repeat_qc.json','candidate_audit_qc.json','manual_stage_receipt.json')) and J(T/'independent_qc.json')['status']=='PASS';rev=J(T/'retrospective.json');e=J(Q/'evidence.json');study=J(Q/'six_sign_repeat_study.json');a=J(Q/'candidate_audit.json');m=J(Q/'manual_decision.json');gg=rev['historical_groups']['all_34_mixed_sources_versions'];assert gg['complete_columns_distribution_0_to_3']==[13,17,3,1] and study['groups']['2024plus']['n']==132 and m['choice']=='CC01'
text='''# 327期复盘、逐期命中与328期人工展示方案

> **日期措辞更正：**先前将部分历史记录笼统称为“未来”或“日期冲突”，未妥善处理不同参考时钟，撤回作为事实的判断；详见[日期措辞更正](archive/task295_328_release/date_correction/日期措辞更正.md)。
>
> **资料口径：**327号码按你提供的顺序推定前六加第七；日期未提供，历史资料部分日期缺失，官方来源、日期和赛前状态未经认证。以下只复核现有材料与结构，栏目完整不等于获利；没有任何方案可以保证下期命中。

## 一、327：先确认中了什么、缺了什么

前六 **21狗、49馬、07鼠、41虎、46鷄、36羊**；第七 **45狗** 单独记载，不进入前六栏目结算。327上次实际展示的是单馬、二鷄龍、三鷄虎牛，蛇仅替补。

| 栏目 | 前六命中 | 缺失 | 结果 |
|---|---|---|---|
| 单馬 | 49馬，1/1 | 无 | 完整 |
| 二鷄龍 | 46鷄，1/2 | 龍 | 不完整 |
| 三鷄虎牛 | 46鷄、41虎，2/3 | 牛 | 不完整 |

因此327是**一栏完整，两组合不完整**，不是三栏全败。鷄是二、三肖共同位且确实出现；这次并不是共同位缺失。蛇替补未出；狗、鼠、羊不在当时六码全集内。

## 二、失败拆解：不是“0路没出”，而是具体身份选错

1. **0路实际上有两球：**21狗为奇0，36羊为偶0。龍是奇0、牛是偶0；有同路同奇偶的狗、羊，仍不能替代龍、牛。此前只看路数或色型不能证明具体生肖会中。
2. **两个组合的侧位集中在同一条路：**二的龍和三的牛都属0路。龍、牛同时缺失时，即使共同鷄出现，两组合仍同时不完整。按327之前的本地前六，龍牛同缺分别为 **13/35、16/40、17/45期**；这些窗口重叠、资料未认证，不是下期概率。此前把重点放在“单與共同位同缺”，对两个侧位一起缺的风险强调不够。
3. **327实际重了4肖：**相对326前六，重狗、羊、虎、鷄；新肖是馬、鼠。327旧方案五个展示身份中有3个不是326前六身份（馬、龍、牛）；一旦重4肖，六球最多容纳两个不同新肖，所以三栏全完不可能。这是必要条件，不是说重4必然只中一栏。
4. **不能事后把对照当成预测：**此前冻结的12案可以用327结果逐一检查，但换成当期出现的狗羊只是事后知道答案，不能证明下一期应继续或停止选它们。后面的对照表仅作复盘。

327前六和值200、跨度42，0/1/2路为2/3/1，奇偶4/2，红蓝绿2/2/2；这些是结果描述，不是328的预测。

## 三、历期逐栏：每条保存版本的命中和缺失

这里列 **34条有保存栏目版本的记录**：291—308为留存本地栏目文件；309—318、320、321、323、325、326、327有Git页面快照。版本、来源与保存时点不同，事后冻结或Git快照都不能单独证明赛前，也不能当作盲测胜率。312、313、315、326使用各自已确认的修订／恢复版本。仅以前六结算；第七不补栏。

| 期 | 材料来源 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
def cell(sl):
 need=''.join(sl['required']);found=''.join(sl['present']) or '—';missing=''.join(sl['missing']) or '—';return f"{need} {sl['present_count']}/{sl['needed_count']}（中{found}；缺{missing}）"
for x in rev['historical_outcomes']:
 src='本地留存版本' if x['period']<=2026308 else 'Git页面快照';text+='| '+' | '.join([str(x['period']%1000),src]+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
**319、322、324只作事后重建对照，未混入上述34条：**

| 期 | 性质 | 单：命中／缺失 | 二：命中／缺失 | 三：命中／缺失 | 完整栏 |
|---:|---|---|---|---|---:|
'''
for x in rev['unpublished_reconstructions']:text+='| '+' | '.join([str(x['period']%1000),'结果已知后重建']+[cell(s) for s in x['slots']]+[str(x['complete_columns'])])+' |\n'
text+='''
34条保存版本中，完整0/1/2/3栏分别为 **13/17/3/1** 条；单、二、三完整分别13、9、4条。共同位缺失15条；另外有7条共同位虽出现，二、三仍同时不完整，327就是其中一条。23条出现过“指定生肖缺失、但同路同奇偶的另一个生肖出现”。这些是混合版本的材料内复盘，**不是未来胜率或预测力**。296—308旧摘要曾混用第七球，此表沿用重新核验的前六口径。

## 四、328人工展示：集中与覆盖的取舍

| 栏位 | 生肖 | 条件与风险 |
|---|---|---|
| 单 | **馬** | 同时是三肖成员；馬缺使单、三肖都不完整。 |
| 二 | **狗、鷄** | 狗与鷄均须出现；狗是二、三肖共同位。 |
| 三 | **狗、馬、蛇** | 分别为0、1、2路；缺任一身份均不完整。 |
| 替补 | **虎、牛** | 仅作全集覆盖，不自动补进任何栏。 |

四个不同展示生肖馬、狗、鷄、蛇共17码；加入虎、牛两个替补，组六全集共25码。**此案不是保证不再失败：狗缺则二、三同断；馬缺则单、三同断；馬缺且狗或鷄缺，三栏全不完整。**例如虚构六球 `06牛 04兔 03龍 02蛇 11猴 08豬`，没有馬、狗、鷄，本案零完整栏；这不是328号码。

相比327所需的五个展示身份，本案三栏全完只需四个指定身份，但展示覆盖从21码减少到17码，联动风险增加。相对327前六，本案所需四肖中馬狗鷄为旧身份、蛇为非旧身份；只有重3、4或5肖时才可能全完，重3—5也不保证。若前六恰好重足6肖，则单馬和二狗鷄完整、三肖因蛇缺而不完整；这只是条件推论，不是预测会重6。

二栏跨路、三肖跨三路并不能彻底消除跨栏同路：二栏另一侧与三肖两个侧位中，必有至少一组同路。本案鷄与馬都属1路、但奇偶不同；有1路仍不代表两个指定生肖都会出现。

### 公平模型对照：不是实际命中率

假设49个号码等可能，每次不放回抽取6个且与前期独立，仅比较栏目完整性，不计算奖金或收益：

| 方案 | 单完整 | 二完整 | 三完整 | 三栏全完整 | 零完整栏 |
|---|---:|---:|---:|---:|---:|
| 327旧BB01 | 49.5198% | 15.6616% | 5.0989% | 0.3295% | 38.5598% |
| 328本案CC01 | 49.5198% | 15.6616% | 6.1500% | 1.6585% | 40.9686% |

在这个假设中，本案全栏比例较高，同时零完整栏比例也较高；是风险目标交换，**不是预测改善或实际收益证明**。截至327的本地重叠W35/40/45若事后套用本案，零完整栏分别10/14/16期，仅为同一结构的描述性对照，不能当作新方案的盲测成绩。

## 五、327六肖后的材料内重肖统计

327前六为狗、馬、鼠、虎、鷄、羊六个不同生肖，第七狗不增加生肖。2024以来本地资料筛到132组“前六与七球均六肖且下一行已知”的相邻记录；使用各期原有生肖标签，包含326→327，不包含未知的327→328。资料与日期未认证，筛选在看到327后进行，不能代表328概率。

| 重肖数 | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 前六对前六 | 2 | 9 | 45 | 47 | 26 | 3 | 0 |
| 七球对七球 | 0 | 3 | 33 | 54 | 35 | 6 | 1 |

理论上最多重6；前六样本中未见重6不等于不可能。两种口径不能混用，下一行未知也不进分母。

## 六、12肖和49码台账：只核对覆盖，不作预测排名

W35、W40、W45按截至327的本地前六计算，每格为出现期数／球数；三个窗口相互重叠。近龄0表示在327前六出现。历史频次、遗漏和类别都不能保证下一次出现。

| 肖 | 号码 | 近龄 | W35／W40／W45（期数／球数） | 本案角色及同类提醒 |
|---|---|---:|---|---|
'''
role={'馬':'单、三；五码，缺馬单三断','狗':'二三共同；龍同奇0不能代狗','鷄':'二；兔同偶1不能代鷄','蛇':'三；豬同偶2不能代蛇','虎':'替补；不能补栏','牛':'替补；羊同偶0不能代牛','鼠':'全集外；与馬同奇1但不能代馬','兔':'全集外；与鷄同偶1但不能代鷄','龍':'全集外；与狗同奇0但不能代狗','羊':'全集外；与牛同偶0但不能代牛','猴':'全集外；与虎同奇2但不能代虎','豬':'全集外；与蛇同偶2但不能代蛇'}
for z in list('鼠牛虎兔龍蛇馬羊猴鷄狗豬'):
 x=e['per_zodiac'][z];w='；'.join(f"{x['windows'][str(k)]['periods']}/{x['windows'][str(k)]['balls']}" for k in (35,40,45));text+='| '+' | '.join([z,' '.join(f'{n:02}' for n in x['numbers']),str(x['last_normal_age']),w,role[z]])+' |\n'
text+='''
### 49码逐码账本

| 码 | 肖 | 角色 | 路 | 奇偶 | 波 | 头 | 尾 | 近龄 | W35／40／45球数 |
|---:|---|---|---:|---|---|---:|---:|---:|---|
'''
short={'馬':'单／三','狗':'二三共同','鷄':'二','蛇':'三','虎':'替补','牛':'替补'}
for n in range(1,50):
 x=e['per_number'][str(n)];text+='| '+' | '.join([f'{n:02}',x['zodiac'],short.get(x['zodiac'],'全集外'),str(x['road']),x['odd_even'],x['wave'],str(x['head']),str(x['tail']),str(x['last_normal_age']),'／'.join(str(x['window_counts'][str(w)]) for w in (35,40,45))])+' |\n'
text+='''
## 七、328的12个结构对照

以下方案相互关联，不是独立试验；虎、牛等替补不影响栏目完整条件。CC01为本案。选择前曾做六组快速理想模型比较，正式12案审计在定案后；未查328结果，但不冒称盲选或赛前预注册。表中百分比仅限上述公平模型。

| 案 | 单 | 二 | 三 | 替补 | 全完整 | 零完整 | 主要代价 |
|---|---|---|---|---|---:|---:|---|
'''
for x in a['candidates']:
 r=x['roles'];p=x['ideal_model']['percent'];text+='| '+' | '.join([x['id'],r['top'],r['A']+r['B'],r['A']+r['C']+r['D'],'、'.join(x['reserves']),f"{p['all_columns']:.4f}%",f"{p['no_complete_column']:.4f}%",x['comparison']])+' |\n'
text+='''
## 八、327上次12案：仅作事后对照

上次已记录的12个相关结构按327前六结算如下；**除了BB01，其余不是327实际展示，不是赛前盲测，也不能因这次事后结果优劣就宣称下次更准。**

| 案 | 单／二／三 | 单 | 二 | 三 | 完整栏 | 二、三缺失 |
|---|---|---:|---:|---:|---:|---|
'''
for x in rev['candidate_counterfactuals']:
 r=x['roles'];miss='二缺'+(''.join(x['pair_missing']) or '—')+'；三缺'+(''.join(x['triple_missing']) or '—');text+='| '+' | '.join([x['id'],r['top']+'／'+r['A']+r['B']+'／'+r['A']+r['C']+r['D'],f"{x['single_hits']}/1",f"{x['pair_hits']}/2",f"{x['triple_hits']}/3",str(x['complete_columns']),miss])+' |\n'
text+='''
## 九、核验材料和边界

独立脚本按原始留存栏目和页面快照复核了34条逐栏结果、3条单列的事后重建、327的12个事后对照，以及328的12案组合数。校验只说明材料及计算一致，**不认证官方来源、日期、赛前时点、真实开奖机制或未来收益**；期间没有查询328开奖结果。原327页面、资料清单和验证包保留。上线状态以另附回执为准。

[逐期结算CSV](archive/task294_327_review/analysis/historical_display_outcomes.csv) · [327复盘明细](archive/task294_327_review/analysis/retrospective.json) · [复盘独立核验](archive/task294_327_review/analysis/independent_qc.json) · [327候选事后对照](archive/task294_327_review/analysis/327_candidate_counterfactual.csv) · [328候选结构及模型](archive/task295_328_release/analysis/candidate_audit.csv) · [模型独立核验](archive/task295_328_release/analysis/candidate_audit_qc.json) · [六肖条件研究](archive/task295_328_release/analysis/six_sign_repeat_study.json) · [重肖逐对数据](archive/task295_328_release/analysis/six_sign_repeat_pairs.csv) · [12肖账本](archive/task295_328_release/analysis/zodiac_ledger.csv) · [49码账本](archive/task295_328_release/analysis/number_ledger.csv) · [人工方案](archive/task295_328_release/analysis/manual_decision.json)。
'''
assert len(re.findall(r'^\| \d{3} \|',text,re.M))==37 and len(re.findall(r'^\| \d{2} \|',text,re.M))==49 and all(x in text for x in ('**馬**','**狗、鷄**','**狗、馬、蛇**','40.9686%','1.6585%'))
p=R/'327期复盘_328期方案与逐期核验.md';assert not p.exists();p.write_text(text,encoding='utf8');print(json.dumps({'status':'PASS_DRAFT_CONDITIONAL_NOT_OFFICIAL_OR_PREDRAW','file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'chars':len(text),'history_rows':37,'zodiac_rows':12,'number_rows':49,'new_candidates':12,'prior_counterfactuals':12},ensure_ascii=False,indent=2))
