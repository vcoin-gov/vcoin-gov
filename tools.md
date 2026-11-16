---
title: 链上分析工具对比
status: 初稿完成
---

::: warning 状态：初稿完成
负责人 @王一五（二 · 链上特征与情报研判组）。额度已于 **2026-11-13 按官网当期政策核查一遍**。组内已定三条边界：**不做付费采购、不自建节点、不注册账号**，全部结论只依据公开资料。因此公开资料未披露的数值（Tronscan 配额、MetaSleuth / OKLink / Bitquery 免费档细则、Arkham API 速率）统一标【公开资料未披露】，**不做估算、不冒充实测**。取数缺口与样本见[实测与自建附录](/onchain/tools-appendix)。
:::

# 链上分析工具对比

## 结论先行

【事实｜2026-11-13 核查】免费窗口在收缩，且**塌陷处正是主战场**：Etherscan 免费档 3 次/秒、10 万次/日且只覆盖部分链，BNB Chain / Base / OP / Avalanche 已转付费；BscScan 免费 API 已取消；Tronscan 必须带 Key；Dune 免费号只读。

【推断｜依据：上述官方政策 + 涉诈资金集中于 TRON / BSC 的公开认知；置信度：高】**「零成本跑完全流程」已不成立**，应采用「0 成本基线 + 一处必要投入」：

| # | 组合 | 用途 | 成本 |
| --- | --- | --- | --- |
| 1 | Etherscan + Tronscan（带 Key 人工核对） | 查交易、读合约、核哈希，所有结论的复核基线 | 0 |
| 2 | MetaSleuth + OKLink 链上天眼 | 拉资金链、出图汇报、中文地址交叉印证 | 0（额度未公开） |
| 3 | Arkham 网页版 + 原始浏览器回溯 | 判地址归属，两个独立来源印证 | 0（API 收费，不用） |
| 4 | **BSC 走 0 成本路线**：网页核对 + 公开通报地址抽样（已定，见场景 F） | 补上唯一没有免费 API 的主战场 | 0 |

【决策｜2026-11-13】组内已定：**不采购、不自建、不注册**。BSC 侧因此只能「人工网页核对 + 抽样」，接受「无法批量、样本有偏」的代价，而不是花钱补能力。

【推断｜置信度：高】**GraphSense 的瓶颈是覆盖，不是成本**：有 Tron adapter、无 BSC adapter，自建也补不上主战场；叠加无人盯节点，结论是**本组不建设**，只作预案。

其余核心判断：

- 【事实｜[Dune 计费文档](https://docs.dune.com/resources/credits-billing/how-credits-work)】Dune 免费账号 view-only、0 credits，新账号仅 7 天试用（2,500 credits）；跑批量最低 Analyst 档 $65–75/月。**「免费 Dune」这条路已不存在。**
- 【推断｜置信度：中高】商业平台（Chainalysis / Elliptic）与免费工具的差距，不在「能不能查到交易」，而在**实体标签的执法级可信度与跨链聚类**；这部分免费工具补不上，只能靠多来源交叉印证缓解。
- 【推断｜置信度：高】**任何关键判断至少两个独立来源**。用第三方标签直接下结论，等于把结论可靠性外包给不透明来源。
- 【事实】额度是价格不是技术参数，会变；本页数字均标核查日期，超一季度勿直接引用。

## 一、本页要回答的问题

1. 各自真正擅长什么？不是功能列表，而是什么场景下非它不可。
2. 免费额度够不够日常研判用？超了怎么办？
3. 哪些能自建？成本和收益比多少？
4. 商业工具与免费工具的差距具体在哪？
5. 最终推荐哪几个组合？

## 二、评估维度

| 维度 | 说明 | 权重 |
| --- | --- | --- |
| 链覆盖 | 是否覆盖 TRON / BSC（涉诈资金主战场） | 高 |
| 标签质量 | 标签来源是否透明、可追溯 | 高 |
| 免费额度 | 个人 / 小组能否长期使用（含 API Key 门槛） | 高 |
| 可自建 | 数据能否自主掌控 | 中 |
| 图谱能力 | 多跳展开、聚类、路径查找 | 中 |
| 中文支持 | 团队使用成本 | 低 |

【推断｜置信度：高】「可自建」权重不低，是因为用第三方标签下结论，等于把可靠性外包给不透明的来源；关键判断最终要靠自己能复现的数据。

## 三、工具对比总表（2026-11-13 核查）

| 工具 | 覆盖链（TRON / BSC） | 免费额度与门槛 | 标签 | 图谱 | 可自建 | 最适场景 |
| --- | --- | --- | --- | --- | --- | --- |
| Etherscan | ETH 及 EVM 系；**BSC 不在免费档** | 3 次/秒、10 万次/日，需 Key，仅部分链 | 有，来源不透明 | 无 | 否 | 单笔交易、读合约、看持仓 |
| Tronscan | TRON 原生 | 需 Key（2025 年中起），**配额未公开** | 基础 | 无 | 否 | USDT-TRC20 必用 |
| Blockchair | 20+ 链，含 TRON | 30 次/分、1,000 或 1,440 次/日（官方口径不一），小量免 Key | 有，可筛 | 无 | 否 | 跨链对比、批量查地址 |
| BscScan 等 Etherscan 系 | BSC / Arbitrum / Polygon | **BSC 无免费 API**，$49/月起；Polygonscan 仍免费 | 有 | 无 | 否 | EVM 通用查询 |
| MetaSleuth | 多链 | 有免费档，**额度未公开** | 有 | 强 | 否 | 拉资金流、出图 |
| OKLink | 多链（自称 170+） | 网页免费；API 配额未公开 | 有，中文 | 中 | 否 | 中文场景、国内地址 |
| Arkham | 多链，含 TRON / BNB | 网页注册免费；**API 仅试用额度，$100/月起** | 实体级，最强 | 中 | 否 | 判地址属于哪个实体 |
| Dune | 多链 | **免费档只读**；试用 7 天 2,500 credits；$65–75/月起 | 无 | 无 | 否 | 批量统计 |
| Bitquery | 多链 | 有免费档，额度未披露 | 弱 | 无 | 否 | 程序化批量拉取 |
| GraphSense | BTC / BCH / LTC / ZEC / ETH / **TRON**；**无 BSC** | 软件 MIT 免费；亦可用托管实例 | 需自建 TagPack | 中 | **是** | 自主可控的深度分析 |
| Blockscout | EVM 系，含 BSC | 自建免费；托管 5 次/秒、10 万 credits/日 | 无 | 无 | **是** | 补 BSC 缺口、数据不出内网 |
| Chainalysis / Elliptic | 多链 | 无（不对个人，不公开报价） | 执法级 | 强 | 否 | 仅作能力参照 |

::: warning 表里的数字有保质期
均标核查日期 **2026-11-13**。Blockchair 日上限官方两处口径不一（1,000 / 1,440），如实并列不取平均；Arkham API 速率来源冲突（20 次/秒 vs 重端点 1 次/秒）标【待验证】。引用前按[附录](/onchain/tools-appendix)复核。
:::

## 四、逐工具判断

每个工具只回答三件事：解决什么问题 / 替代不了的点 / 什么时候不该用。列功能不给判断，等于没调研。

| 工具 | 解决什么问题 | 替代不了的点 | 什么情况下不该用 |
| --- | --- | --- | --- |
| Etherscan | 单笔交易、合约调用、代币持仓的原始核对 | EVM 系最完整的 internal tx / token transfer / input data 展示，是复核终点 | 免费档已不含 BSC；要跨链比对或出资金流图时 |
| Tronscan | TRON 的 USDT-TRC20 流水核对 | 主战场原生浏览器，TRC20 第一手数据 | 非 TRON 链路；无 Key 会被限流到无法批量 |
| Blockchair | 一次查多链、批量查地址 | 统一接口跨 20+ 链，适合横向扫一遍 | 30 次/分硬限，批量前先算请求数 |
| BscScan 等 | BSC 等 EVM 侧链查询 | 与 Etherscan 同套交互，零学习成本 | **无免费 API**；单案网页核对即可，不必买 Key |
| MetaSleuth | 快速拉一条资金链并直接出图 | 免费档就能生成可进汇报的图谱 | 节点一多要付费；底层标签是第三方，须回原始浏览器复核 |
| OKLink | 中文界面下查国内案件地址 | 中文标签与国内案件地址覆盖 | 标签来源不透明，不能单独定案 |
| Arkham | 判断地址属于哪个实体 | 实体级标注在免费工具里最强 | 网页免费、**API 收费**；归属是推断，须第二来源印证 |
| Dune | 「某类地址 30 天行为分布」这类统计 | 写 SQL 查已索引多链数据，可自定义指标 | 免费档只读，跑查询要付费；不做单案追踪 |
| Bitquery | 程序化批量取数 | GraphQL 适合脚本化 | 标签弱，不解决「这地址是谁」 |
| GraphSense | 数据自主可控的深度分析 | 唯一能把数据与标签握在自己手里的开源路线，且有 TRON adapter | 无 BSC adapter；节点、存储、标签都是硬成本 |
| Blockscout | 私有化部署浏览器 | 数据不出内网，是补 BSC 免费缺口最现实的路 | 无标签、无图谱，单独部署价值有限 |
| Chainalysis / Elliptic | 执法级取证与出庭证据链 | 标签的司法可信度与跨链聚类 | 不对个人开放、黑盒评分无法解释，不作为方案 |

## 五、分组推荐（按场景，不按工具）

**场景 A · 查一笔具体交易**：Etherscan（ETH 系）+ Tronscan（TRON）。关键是看 internal tx、token transfer、input data——只看主交易会漏掉内部转账，而涉诈资金大量走合约内部调用【推断｜依据：合约代付与批量归集是公开可观察的常见模式；置信度：中】。

**场景 B · 快速拉一条资金链**：MetaSleuth 优先，免费档做中小规模够用，出图可进汇报。局限：节点一多要付费，标签仍须回原始浏览器复核。

**场景 C · 批量数据、做统计**：Dune 或 Bitquery，**但要先确认钱**：Dune 免费档只读、Analyst $65–75/月起，Bitquery 额度未披露。批量统计不是免费能力。

**场景 D · 自主可控的深度分析（本组结论：不做）**：有 Tron adapter 但无 BSC adapter，**自建补不上主战场**；数据导入以「天」计、标签只能按月攒、组内无人盯节点。三条都成立，故本期不建设，只留预案（成本框架见[附录](/onchain/tools-appendix)）。

**场景 E · 判地址归属**：Arkham 网页版 + OKLink 互相印证，两家一致时可信度显著提升【推断｜置信度：中高；依据：独立来源一致性降低单点标注错误】。

**场景 F · BSC 取数怎么办（原稿缺失，最要紧）**：BSC 是主战场之一，但 BscScan 免费 API 已取消。三条路的成本对照如下，**组内已选第一条**：

| 方案 | 成本 | 适合 | 代价 | 决定 |
| --- | --- | --- | --- | --- |
| 网页核对 + 公开通报地址抽样 | 0 | 单案复核、抽样观察 | 无法批量，样本有偏 | **✅ 采用** |
| 自建 Blockscout 接 BSC 节点 | 软件 0 + 机器与运维 | 长期跑、数据不出内网 | 部署与同步成本，无标签，需专人 | ❌ 无运维人力 |
| BscScan 付费 $49/月起 | 钱 | 需稳定批量 API | 唯一确定的支出项 | ❌ 本期不采购 |

【决策｜2026-11-13】**先证明需求，再买额度**。重启条件写死：单专题需跑 500 次以上 BSC 请求，或需连续 7 天监控同一簇地址——满足任一条再回本表讨论。

【推断｜置信度：高】代价要写进结论：**BSC 只能到个案级，不能支撑分布级**。凡涉 BSC 的统计口径一律标【推断｜置信度：低】或注明样本量。

## 六、明确不推荐的方向

| 不推荐 | 原因 |
| --- | --- |
| 同时装五六个浏览器 | 功能高度重叠，切换成本大于收益。EVM 系一个 Etherscan 全够 |
| 一上来就自建全套 | 节点、存储、标签都是硬成本；且 GraphSense 无 BSC adapter，自建也补不齐 |
| 依赖单一来源的标签下结论 | 标签错则结论废。任何关键判断至少两个独立来源 |
| 按「有免费档」三个字做方案 | 免费档普遍带 Key 门槛、链限制或只读限制，不看细则等于没看 |

## 七、边界与例外

- 【事实｜[Etherscan Rate Limits](https://docs.etherscan.io/rate-limits)、[API 定价](https://etherscan.io/api/pricing)】免费档 3 次/秒、10 万次/日，仅覆盖部分链；付费档另有超额计费。
- 【事实｜[Tronscan API 文档](https://docs.tronscan.org/en/api/common-network-auth)】请求需 Header 带 `TRON-PRO-API-KEY`，部分端点无 Key 直接 401；配额官方未公布。
- 【事实｜[Blockchair API 文档](https://blockchair.com/api/docs)】免费档 30 次/分硬限、单日 1,000 或 1,440 次（官方两处口径不一），另有 5 次/秒软限。
- 【事实｜[GraphSense 官网](https://graphsense.org)】MIT 开源，adapter 覆盖 BTC / BCH / LTC / ZEC / ETH / Tron，**无 BSC**；新增链需自行实现。
- 【公开资料未披露】Arkham API 速率与免费额度在不同来源间冲突（20 次/秒 vs 重端点 1 次/秒；试用额度 vs 长期免费），**无单一官方口径**；本组不注册账号，故不实测，仅作提示。
- 【公开资料未披露】MetaSleuth、OKLink、Bitquery 免费档具体数值未在官方页面公布，不做估算，缺口与已知信息见[附录](/onchain/tools-appendix)。
- **决策留痕**：本期不采购、不自建、不注册（2026-11-13）。凡需批量或全量的判断，本页只到「方法可行」，不到「数据已验」。
- **不做可操作的规避指导**：本页只讨论如何识别与复核资金链路，不写清洗手法的操作步骤；混币、跨链跳转的识别特征在[治理痛点提炼](/policy/pain-points)与[基础链上知识](/onchain/basics)。
- 【待验证】【公开资料未披露】项一律不得进入对外 PPT；按[输出规范](/)，PPT 每条都要能在本站找到对应条目。

## 八、待办

- [x] 按官网当期政策核查 12 个工具的免费额度与链覆盖（2026-11-13）
- [x] 输出工具选型建议（3 个以内）+ BSC 单列方案——见「结论先行」与「场景 F」
- [x] 定下三条边界：不采购、不自建、不注册（2026-11-13）——见「场景 D」「场景 F」
- [ ] 五工具标签横评：样本地址已选定（见[附录](/onchain/tools-appendix)），**网页版查询无需注册**，任何组员用浏览器 20 分钟可填完
- [ ] 新出现公开通报披露完整 TRC20 地址时，补一组 TRON 侧样本
- [ ] 触发条件出现时重启 BSC 付费 / 自建讨论

## 参考

均为公开官方文档 / 产品入口，核查日期 2026-11-13。

1. [Etherscan · Rate Limits](https://docs.etherscan.io/rate-limits) · [API 定价](https://etherscan.io/api/pricing)
2. [Tronscan · API 文档](https://docs.tronscan.org/en/api/common-network-auth) · [API Key 公告](https://support.tronscan.org/hc/en-us/articles/18541358323609)
3. [Blockchair · API 文档](https://blockchair.com/api/docs)
4. [GraphSense · 官网](https://graphsense.org) · [GitHub](https://github.com/graphsense)
5. [Blockscout · 部署文档](https://docs.blockscout.com/)
6. [Dune · 计费文档](https://docs.dune.com/resources/credits-billing/how-credits-work) · [Bitquery · 文档](https://docs.bitquery.io/)
7. [MetaSleuth](https://metasleuth.io/) · [OKLink 链上天眼](https://www.oklink.com/) · [Arkham](https://www.arkhamintelligence.com/)
8. [Chainalysis · Product Guide](https://www.chainalysis.com/productguide/) · [Elliptic](https://www.elliptic.co/)
9. [贡献指南](/guide/contributing) · [调研文档模板](/guide/research-template)
