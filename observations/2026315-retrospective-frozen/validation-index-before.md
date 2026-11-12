# 当前验算入口：315方案与石坑绝密版式

> **当前首页：**按仓库最早的“石坑绝密”页面调整布局和显示文字，保留优化后的计算代码及用户提供的314号码，展示既定315方案。用户指出的页底整段已删除，未换位置保留；期数与指标栏随走势图横向移动。旧页面和历史证据保留。
>
> **操作与边界：**旧倒计时没有核实的截止依据，期号框只显示编号。网站入口此前有错误的根路径跳转，现修为同目录跳转。微信风险提示是否消失仍需真实微信客户端确认；HTTP和浏览器通过并非微信安全认证。

> **当前范围：**315是用户授权的非官方资料展示，不是官方结果、赛前认证、投注建议或预注册。来源与实际机制未认证，第三方状态可能滞后或共上游；状态为空不证明赛前。首页已删除后来添加的页底说明。

## 314输入与失败复盘

- 314号码唯一来源为用户：**13、26、09、37、34、44＋31**；期号及前六＋第七球标签按上下文推定，用户未提供日期，未经官方认证。只以前六码统计和结算，第七球仅用于历史记录与七球生肖身份交集，不推特码。
- 314旧展示为单牛、二虎馬、三虎狗鷄，豬仅替补；前六码分别 **0/1、1/2、2/3**，三栏完整数为0。虎是共同缺位，牛未出现；替补豬和第七球鼠都不能补栏。
- [314完整失败复盘](../314期失败逐步深度复盘_用户号码.md) · [用户输入原文](task261_314_user_input.json) · [314旧展示分析及候选](task260_314_release/observations/2026314-analysis.md) · [314复盘公开副本](task262_315_release/observations/2026314-retrospective-public.md)。

## 315人工方案（当前首页）

- 六肖全集 **虎、蛇、馬、龍、兔、牛**；单 **虎**，二 **蛇馬**，三 **蛇龍兔**，**牛仅替补**。38份完整手写候选、37种不同栏目结构、16份单肖与A–D重叠，按原序保留，不摇号、不打分、不以历史命中排名。
- 蛇为二三共同位，蛇缺两组合栏同时断；三栏需蛇龍兔三路各一且至少两偶。全栏须五肖，至少0/1/2路1/2/2和3奇2偶；绝不是预测保证。314和315的栏位角色码组数、共享结构同构，理想等可能模型下的栏目概率不变。
- [网站](https://fffsw.github.io/zodiac-trend/zodiac_trend.html) · [315历史逐肖逐码分析与当时上线核验](../315期_314失败复盘后人工选择与上线核验.md) · [315历史公开审计](https://fffsw.github.io/zodiac-trend/observations/2026315-analysis.md) · [本地审计包](task262_315_release/observations/) · [上线回执](task262_315_release_receipt.json)。

## 来源和可复算资料

- [主历史CSV](macau_mark_six_full.csv)截至314共1,045期，SHA-256 `687efa128921ef7ace365131c023592a162a8dca4c367c88949ea0c16656ffb5`；此前1,044条逐行字节未变，313、314日期均为空、页面显示 `--/--`。历史源不代表官方认证。
- [人工决定历史记录（含315）](manual_site_decisions.json) · [12肖账本](task262_315_release/observations/2026315-zodiac-ledger.csv) · [49码账本](task262_315_release/observations/2026315-number-ledger.csv) · [38份候选](task262_315_release/observations/2026315-candidates.csv) · [人工裁决](task262_315_release/observations/2026315-manual-decision.json) · [独立复算](task262_315_release/observations/2026315-verify.py) · [页面快照](task262_315_release/observations/2026315-page.html) · [新清单](task262_315_release/observations/2026315.sha256)。
- 推送提交 `2f1c74ecb85265de324e958fa27ed76acf57f261`，GitHub Pages Actions成功；公网153份文件哈希和桌面、手机真实浏览器54项验收通过。核验的是版本和页面功能，不证明官方性、赛前、开奖机制、预测力或收益。
- 原314和313公开包、旧决定、复盘、四份旧清单均保留；[312原盘](task262_315_release/pre-registration/2026312.json)和[312 rev1](task262_315_release/pre-registration/2026312-rev1.json)未变，313、314、315没有赛前预注册。上一索引冻结在 `archive/task262_315_release/before/data/task254_validation_index.md`，当时“尚未选择315”只描述当时。
- 35/40/45主窗重叠，不是独立投票；历史445指相邻七球去重交集恰好4/4/5，身份可变，不能混成前六或至少4。

澳门司警[2024年公告](https://www.gcs.gov.mo/news/detail/zh-hans/N24JR61szQ)曾警示相关博彩网站诈骗；并非对现在牌照状态的重新认证。理想等可能模型是数学假设，实际机制不明；低于公允赔率时为负期望，不能据此声称公平或获利。

- [此前误回退的历史回执](task264_website_rollback_receipt.json) · [回退哈希清单](task264_website_rollback/observations/2026315-rollback-to-314.sha256)。旧版和315两个页面快照及原有审计均保留。

## 此前315简洁版修正核验（历史）

- [网站](https://fffsw.github.io/zodiac-trend/zodiac_trend.html) · [本次回执](task265_315_original_layout_receipt.json) · [新版快照](task265_315_original_layout/observations/2026315-restored-layout-page.html) · [新版清单](task265_315_original_layout/observations/2026315-restored-layout.sha256) · [项目入口修正清单](task265_315_original_layout/observations/2026315-entry-fix.sha256)。
- 当时页面SHA-256 `16cadce0b366aa6273017002db75d37bdda279eb8c2497029a6bbda9dd59d34e`；本地生成器已同步。最终提交 `45b6255aeb5a4d4238b912f6ba17822853b52105`；GitHub Pages成功，公网172个文件哈希匹配，Chromium桌面与手机模拟分别核验交互。313预注册缺失检查首遇503，针对该路径重试404并保留原记录。
- 314号码、315人工决定和原有315分析未重选或改写；状态查询只查目标是否有记录及最新期号，未读取315号码，不构成赛前认证。

## 315石坑绝密版式、页底与横滑修正

- [正式网站](https://fffsw.github.io/zodiac-trend/zodiac_trend.html) · [本次回执](task267_footer_cleanup_receipt.json) · [首页快照](task267_footer_cleanup/observations/2026315-initial-layout-no-footer-page.html) · [文件清单](task267_footer_cleanup/observations/2026315-initial-layout-no-footer.sha256) · [公网核验](task267_footer_cleanup/audit/live_http_qc.json)。
- 提交 `f3e4905ddd9402f40ae61fe96fe3fc3ede5499d1`；页面SHA-256 `5270c8d378d85b5f4acf770a897aec7918c2cd710ef81be53787215a9b26611b`；191份公网文件与九份历史及本次清单通过核验。实际公网桌面及手机模拟核对页底、按钮、数据和横向滑动，315方案与314号码未变。
- 本机生成器已同步；生成器重新运行不会恢复被删除的页底。微信提示是否消失仍需真实微信客户端核实；手机检查为Chromium模拟。
