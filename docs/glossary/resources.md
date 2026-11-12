# 数据与文献资源

<div class="doc-meta">
  <span class="owner">维护：全组共建</span>
  <span class="doing">状态：持续补充</span>
</div>

::: warning 链接会失效
所有外链标注「最后核对于」日期。超过半年未核对的，使用前先点开确认。
:::

## 一、官方与法规

| 名称 | 链接 | 用途 |
| --- | --- | --- |
| 国家法律法规数据库 | <https://flk.npc.gov.cn/> | 法律、行政法规原文，核对条文首选 |
| 中国政府网 · 政策文件库 | <https://www.gov.cn/zhengce/> | 部委联合通知原文 |
| 中国人民银行 · 政策发布 | <http://www.pbc.gov.cn/> | 虚拟货币相关通知的发布源头 |
| 最高人民法院 | <https://www.court.gov.cn/> | 司法解释、指导性案例 |
| 最高人民检察院 | <https://www.spp.gov.cn/> | 指导性案例、检察意见 |
| 公安部 | <https://www.mps.gov.cn/> | 通报公告 |
| 中国裁判文书网 | <https://wenshu.court.gov.cn/> | 判决书检索，看实务说理 |
| 中国执行信息公开网 | <http://zxgk.court.gov.cn/> | 涉执信息 |

## 二、境外监管

| 名称 | 链接 | 用途 |
| --- | --- | --- |
| EUR-Lex | <https://eur-lex.europa.eu/> | MiCA 原文（Regulation (EU) 2023/1114） |
| ESMA | <https://www.esma.europa.eu/> | MiCA 实施细则与 Q&A |
| congress.gov | <https://www.congress.gov/> | 美国法案当前状态（众议院通过 ≠ 生效） |
| SEC | <https://www.sec.gov/> | 证券属性认定与执法行动 |
| CFTC | <https://www.cftc.gov/> | 商品属性认定 |
| FinCEN | <https://www.fincen.gov/> | BSA / MSB 注册与 Travel Rule |
| 香港金融管理局 | <https://www.hkma.gov.hk/> | 稳定币条例、持牌机构名单 |
| 香港证监会 | <https://www.sfc.hk/> | 虚拟资产交易平台名单 |
| MAS（新加坡） | <https://www.mas.gov.sg/> | 支付服务法与 DPT 指引 |
| FATF | <https://www.fatf-gafi.org/> | Recommendation 15、风险指标 |

## 三、链上数据与工具

| 名称 | 链接 | 免费额度 | 主要用途 |
| --- | --- | --- | --- |
| Etherscan | <https://etherscan.io/> | 有 | 以太坊查询与 API |
| Tronscan | <https://tronscan.org/> | 有 | TRON 查询（USDT-TRC20 主战场） |
| Blockchair | <https://blockchair.com/> | 有（较严） | 多链横向对比 |
| BscScan | <https://bscscan.com/> | 有 | BSC 生态 |
| MetaSleuth | <https://metasleuth.io/> | 有 | 资金流可视化追踪 |
| OKLink | <https://www.oklink.com/> | 有 | 中文链上数据与追踪 |
| Arkham | <https://arkhamintelligence.com/> | 有 | 实体级地址标注 |
| Dune | <https://dune.com/> | 有（查询受限） | SQL 批量统计 |
| Bitquery | <https://bitquery.io/> | 有 | GraphQL 批量拉数 |
| mempool.space | <https://mempool.space/> | 免费 | 比特币内存池与手续费 |

## 四、公开数据集

| 名称 | 位置 | 内容 | 使用注意 |
| --- | --- | --- | --- |
| Elliptic Data Set | Kaggle | 比特币交易图，含 illicit/licit 标注 | 2011–2013 年数据，与当前场景差异大 |
| Elliptic++ | GitHub / Kaggle | 扩展版，含地址级特征与钱包网络 | 同上 |
| OFAC SDN 名单 | 美国财政部官网 | 制裁地址清单（含加密地址字段） | 公开可下载，可定期同步 |
| BitcoinHeist | 学术公开 | 比特币非法实体标注 | 规模小、时效旧 |
| AMLSim | GitHub | 合成反洗钱交易数据 | **只能测流程，不能测效果** |

::: danger 数据集使用的红线
用公开数据集跑出来的指标，**不能当作实战效果的证据**。写方案时必须标注数据来源、时间范围、与目标场景的差异。拿 2013 年的比特币数据证明能识别 2026 年的 TRON 资金盘，在评审时会被直接否掉。
:::

## 五、方法学与报告

| 名称 | 用途 |
| --- | --- |
| FATF · Virtual Assets Red Flag Indicators | 风险指标设计的国际口径，做特征清单必读 |
| Chainalysis · Crypto Crime Report（公开摘要） | 年度趋势参考，**只看方法不引结论** |
| Elliptic · 公开研究文章 | 混币、跨链的方法学讨论 |
| 各国央行数字货币研究报告 | 稳定币监管背景 |

::: tip 商业机构报告的引用纪律
Chainalysis / Elliptic 的报告可以引用**方法论**和**公开案例**，但不宜直接引用其统计结论当作我方数据——数据来源与统计口径不透明，无法在正式材料中作为论据。
:::

## 六、待补充

- [ ] 各省反诈中心公开通报入口（按省份整理）
- [ ] 国内涉虚拟货币判决的检索式（案由 + 关键词组合）
- [ ] TRON 生态的第三方数据源（Tronscan 之外的备选）
- [ ] 开源情报（OSINT）工具清单，用于链下身份关联

## 七、贡献方式

新资源直接加表，必须填「用途」列——填不出用途的链接不要加。失效链接请直接删除或标注「已失效」。
