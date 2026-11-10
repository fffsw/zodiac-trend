# 当前验算入口：313用户号码复盘与314非官方展示

> **当前范围：**314是用户授权的非官方资料展示，不是官方结果、赛前认证或预注册。来源与实际机制未认证；第三方状态查询可能滞后或共上游。网页保留原有简洁样式和司警警示。

## 输入与当前方案

- 312用户确认：**31、46、04、43、32、15＋38**；旧首球34只留审计。313用户提供：**33、39、45、15、07、20＋43**。313期号及六加一依上下文推定，日期未知；主CSV日期空、网页显示 `--/--`，不把本机时钟写成开奖日期。
- [主历史 `macau_mark_six_full.csv`](macau_mark_six_full.csv)：1,044期，SHA-256 `662032bf9829c1451ea4dcc221b2b4c8386d5efe953a73e1ac14789b0869e629`；原1,043期数据行逐字节不变。历史源不代表官方认证。
- [当前人工决定](manual_site_decisions.json)：314六肖 **牛虎馬狗鷄豬**；单 **牛**，二 **虎馬**，三 **虎狗鷄**，**豬仅替补**。不使用摇号、总分、热度或回测命中排名。虎为共同位，虎空则两个组合栏均不完整；三栏必须三路各至少一球，反方见完整报告。
- [网站](https://fffsw.github.io/zodiac-trend/zodiac_trend.html) · [314完整复盘与裁决](../314期_313失败复盘后人工选择与上线核验.md) · [313失败逐步复盘](../313期失败逐步深度复盘_用户号码.md)。

## 可复算资料与核验

- [314发布包](task260_314_release/observations/)：含[12肖账本](task260_314_release/observations/2026314-zodiac-ledger.csv)、[49码账本](task260_314_release/observations/2026314-number-ledger.csv)、[31份候选](task260_314_release/observations/2026314-candidates.csv)、[人工决定](task260_314_release/observations/2026314-manual-decision.json)、[独立核验](task260_314_release/observations/2026314-verify.py)、[页面快照](task260_314_release/observations/2026314-page.html)和[哈希清单](task260_314_release/observations/2026314.sha256)。31份中只有30种不同栏目，E09仅换替补；顺序不是排名。
- [上线回执](task260_314_release_receipt.json)：推送提交 `695bead81e897af6e7a7a35805257ca5b246d455`；Pages部署、公开文件哈希与桌面/手机真实浏览器验收见回执。验证文件一致不证明官方性、赛前、机制或收益。
- 313旧D2为单鼠、二兔龍、三兔虎豬，按用户前六码结算为 **1/1、1/2、1/3**；[D2旧页](task260_314_release/observations/2026313-reanalysis-v2-page.html)、[313公开复盘](task260_314_release/observations/2026313-retrospective-public.md)、D1及其哈希继续保留。313和314都没有赛前预注册。
- [312原盘](task260_314_release/pre-registration/2026312.json)及[312 rev1](task260_314_release/pre-registration/2026312-rev1.json)哈希保持不变；[312原盘网页](task260_314_release/pre-registration/2026312-page.html)继续可访问。旧版索引冻结在 `archive/task260_314_release/before/data/task254_validation_index.md`，其中“主历史只到312、尚无314”是当时状态，不是现在状态。
- 前六码用于栏位与统计；第七球仅用于历史七球生肖交集。35/40/45重叠，窗口频次不是投票或可验证的下一期优势；445指相邻七球去重交集恰好4/4/5，身份可变。

澳门司警[2024年公告](https://www.gcs.gov.mo/news/detail/zh-hans/N24JR61szQ)曾警示相关博彩网站诈骗；链接不是对现在牌照状态的重新认证。理想等可能模型只是数学假设；低于公允赔率时为负期望，不能据此声称实际公平或获利。
