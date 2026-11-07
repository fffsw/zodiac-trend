# 网站平码预注册

这里公开保存每期网站展示的选前记录及结构审计；不生成特码A/S/B/C，也不把替补视为展示栏位。2026310仅使用截至2026309的历史。历史频率与结构观察不能改变随机开奖概率，栏目不是最高置信或投注建议。

2026310：`2026310.json`为仅网站预注册，`2026310-structure.json`为结构审计，`2026310-analysis.md`为选前报告，`2026310-page.html`为当期冻结页面快照（不是后续期的实时页面），`2026310.sha256`为上述不可变快照的SHA-256清单。哈希及本地记录不是签名或独立可信时间证明；查看提交和部署时间可核对公开发布记录。后续期应新增文件，不覆写旧期。


2026311（仅使用截至2026310的历史，网站前六个平码；上期特码只作七球生肖身份标签）：

- [仅平码预注册](2026311.json) · [开奖结构审计](2026311-structure.json) · [人工分析](2026311-analysis.md) · [本期冻结页面](2026311-page.html) · [SHA-256清单](2026311.sha256)。
- [十二肖与49号码账本](2026311-ledgers.txt) · [开奖结构账本](2026311-draw-structure.txt) · [人工候选及结构对照](2026311-candidates.json) · [截止310的原始数据](2026311-source-data.csv)。原始数据保留历史特码以完整记录开奖，但选号分析及网站结算只使用前六球。
- [310深度复盘](2026311-prior-310-review.md) · [正式v3教训](2026311-lessons-v3.json) · [v4教训草案（未自动启用）](2026311-lessons-v4-draft.json) · [证据卡](2026311-evidence-cards.json) · [标签对应](2026311-evidence-key.json) · [揭码前初拟](2026311-preliminary.json)。证据卡不是严格盲评，标签不决定选肖。
- [冻结前来源状态](2026311-source-check.json) · [最新期API原文](2026311-source-latest.json) · [311按期API原文](2026311-source-target.json)。已作请求新鲜度检查，但来源可能共上游，服务器时间与空值不构成权威开奖时间证明。第二展示源的完整原文仅保存在本地证据归档。

这些是人工展示取舍，不代表预测优势、收益或最高置信；开奖记录、哈希、Git提交与在线下载均不是签名或独立可信时间戳。

- [311生产与仅平码预注册补充规格](2026311-production-spec.md)：明确数据边界、角色、冻结和上线验收。


2026312（历史截止2026311；网站只按前六个平码，311特码只作上期七号生肖身份标签）：

- [仅平码预注册](2026312.json) · [开奖结构审计](2026312-structure.json) · [人工分析及51个候选](2026312-analysis.md) · [生产规格](2026312-production-spec.md) · [本期冻结页面](2026312-page.html) · [SHA-256清单](2026312.sha256)。
- [十二肖与49条号码路线](2026312-ledgers.txt) · [开奖结构账本](2026312-draw-structure.txt) · [结构指标](2026312-draw-structure-metrics.json) · [51个完整候选](2026312-candidates.json) · [首轮26案](2026312-candidates-round1.json) · [截止311原始CSV](2026312-source-data.csv)。原始CSV保留历史特码以完整记录开奖，但选号分析及网站结算只使用前六球。
- [311深度复盘](2026312-prior-311-review.md) · [正式v3教训](2026312-lessons-v3.json) · [310复盘草案D20—D23](2026312-lessons-v4-draft.json) · [311复盘草案D24—D28](2026312-lessons-311-draft.json)。两组草案均未自动启用。
- [编码证据卡](2026312-evidence-cards.json) · [标签映射](2026312-evidence-key.json) · [初拟](2026312-preliminary.json) · [人工决定收据](2026312-decision-receipt.json)。证据卡不是严格盲评，标签不决定选肖。
- [账本独立核验](2026312-ledger-independent-test.txt) · [候选独立核验](2026312-candidate-independent-test.txt) · [报告QA](2026312-report-qc.txt) · [冻结前负测](2026312-prefreeze-negatives.txt) · [冻结后负测](2026312-prereg-negatives.txt) · [仅平码范围测试](2026312-site-scope-test.txt) · [按钮最小DOM测试](2026312-button-test.txt)。
- [冻结前来源状态](2026312-source-check.json) · [最新期API原文](2026312-source-latest.json) · [312按期API原文](2026312-source-target.json)。已作请求新鲜度检查，但来源可能共上游，服务器时间与空值不构成权威开奖时间证明。第二展示源的完整原文保存在本地证据归档。

这些是人工展示取舍，不代表预测优势、收益或最高置信；开奖结果有随机性，赔率低于公允回报时投注为负期望。开奖记录、哈希、Git提交与在线下载均不是签名或独立可信时间戳。


## 2026312 rev1：千期四重肖审查、历史数据更正后的重选

**本期现行盘为rev1；上方2026312原盘是修订前冻结结果，保留对照，不可当成当前盘。** v5.0人工六肖无摇号框架不变。全集蛇兔虎龍馬鷄，单蛇、二兔馬、三兔虎龍，鷄仅替补。原盘为蛇兔虎龍馬豬，单蛇、二兔龍、三兔虎馬，豬替补。修订只讨论前六平码；上期特码只用于上期生肖身份标签，不产生特码选号。

- [修订预注册](2026312-rev1.json) · [完整文件封存](2026312-rev1-attestation.json) · [修订页面](2026312-rev1-page.html) · [原盘页面](2026312-page.html) · [修订分析全文](2026312-rev1-analysis.md) · [规格](2026312-rev1-production-spec.md) · [修订SHA-256清单](2026312-rev1.sha256)。原预注册的self-MD5为389d672404eb839eb7a4e4f1b62c3bc9，修订预注册中的override指向它；兼容用self-MD5不涵盖override，独立文件封存覆盖完整字节。
- [核对版1042期数据](2026312-rev1-source-data.csv) · [原始冻结数据](2026312-source-data.csv) · [7期差异表](2026312-rev1-history-differences.csv) · [来源核对记录](2026312-rev1-history-reconciliation.json) · [11份历史来源压缩原文索引](2026312-rev1-evidence-index.json)。2026112、2026276在网页250期内，当前页已采用核对版；其余为2024294日期和2025029、2025030、2025031、2025115号码。来源可能共用上游，不是独立官方认证。
- [千期逐期去重账本CSV](2026312-rev1-repeat-ledger.csv) · [千期连段与15个已知后续](2026312-rev1-repeat-ledger.txt) · [全部指标JSON](2026312-rev1-repeat-metrics.json) · [十二肖49号账本](2026312-rev1-fluctuation-ledgers.txt) · [开奖结构账本](2026312-rev1-draw-structure.txt) · [23个人工候选](2026312-rev1-candidates.json) · [人工决定](2026312-rev1-decision-receipt.json)。主口径为本期6平码肖去重∩上期7球肖去重；当前恰好4重连续2期，千期最长3期，后续小样本不是预测。
- [来源核对独立测试](2026312-rev1-reconciliation-test.txt) · [千期独立测试](2026312-rev1-repeat-test.txt) · [逐肖及结构独立测试](2026312-rev1-ledger-test.txt) · [候选独立测试](2026312-rev1-candidate-test.txt) · [页面数据对账](2026312-rev1-page-data-test.txt) · [按钮模拟](2026312-rev1-button-test.txt) · [冻结前负测](2026312-rev1-prefreeze-negatives.txt) · [预注册负测](2026312-rev1-prereg-negatives.txt) · [本期赛前源检](2026312-rev1-source-check.json)。按钮为最小DOM模拟，不是真浏览器。
- [千期分析脚本](2026312-rev1-repeat-analysis.py) · [千期独立复算脚本](2026312-rev1-repeat-independent-test.py) · [历史核对脚本](2026312-rev1-history-independent-test.py) · [页面生成脚本](2026312-rev1-generator.py)。原始脚本使用本地绝对路径；公开索引说明如何在隔离副本恢复目录及正确数据版本，旧原件不可覆盖。

修订前的中间决定曾将top重叠枚举写成不同名，预注册之前已按v5.0规范纠正为coverage，所选肖及槽位未变；[纠正记录](2026312-rev1-schema-correction.json)保留。所有历史频率仅供描述，不能改变下一期开奖概率；有随机性，赔率低于公允回报时投注为负期望。哈希、来源显示和Git记录均非可信独立时间证明。
