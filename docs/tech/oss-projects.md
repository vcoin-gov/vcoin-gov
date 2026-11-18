---
title: 开源项目调研
---

# 开源项目调研

<div class="doc-meta">
  <span class="owner">负责人：@Fiagainster · @墨辰</span>
  <span class="doing">状态：进行中</span>
</div>

## 结论摘要

1. **能直接当"分析平台"用的开源项目只有 GraphSense 一个。** 它现在支持 TRON（`trx-client` + 库内 `trx` transformation，2026-11 仍活跃），但没有 BSC；代价是要在 Cassandra + Spark 上运维。本期结论：只读它的代码与 TagPack，不部署。
2. **采集层 EVM 选择很多，TRON 只有一条活路。** `tronetl` 停更在 2026-02 且**无 License**，`tronscan-api` 停更在 2023 且无 License，`bitcoin-etl` 18 个月无提交。仍活跃的 TRON 采集件只有两个：GraphSense 的 `trx-client`（只服务自家格式）、`fystack/multichain-indexer`（MIT，14 链含 TRON / BSC）。
3. **选型表里要删掉三个名字**：BlockSci（2021-12 停更）、Kuzu（2025-10 已归档）、`bitcoin-etl`（2025-05 后无提交）。它们仍高频出现在各类"链上分析工具清单"里，但都过不了本页的门槛。
4. **Blockscout 不再是 GPL。** 2026-04-22 起改用自有许可 `LicenseRef-Blockscout`：内部非商业使用可以，但许可可撤销、可单方变更，界面须保留 "Powered by Blockscout" 署名，SaaS 化或收费需另购商业许可。**fork 之前先锁旧版本**（该许可不溯及 Prior Software）。
5. **推荐组合仍是三件 + 一个自研**：公开 API + PostgreSQL / NetworkX / Cytoscape.js / 自研规则引擎。决策引擎 Marble 只作参考（Elastic 2.0，非 OSI 许可）。

## 本页要回答的问题

1. 从**数据采集**到**可视化**，每个环节有哪些成熟开源项目？各自成熟度如何？
2. 哪些项目**已经停止维护**，不能再作为技术选型基础？
3. 哪些能力**可以自己写几百行解决**，不值得引入重型框架？
4. 最终推荐哪套组合？为什么是这套而不是别的？
5. 哪些方向**明确不做**？（避免摊子越铺越大）

## 调研口径

::: warning 判定标准：三条硬门槛 + 两条一票否决
**硬门槛**：① 近 12 个月有实质提交（纯文档、修链接不算）② 有可运行的部署文档 ③ 许可允许内部非商业使用。
**一票否决**：仓库已 `archived`；仓库**没有 LICENSE**（无许可＝默认保留全部权利，不能内部使用）。
:::

核查方式（任何人可复现，核查日 **2026-11-18**）：

```bash
# 基础元数据：最后提交、是否归档、许可
gh api repos/<owner>/<repo> --jq '{pushed_at, archived, license: .license.spdx_id}'
# 提交节奏：看是人写的还是脚本刷的
gh api repos/<owner>/<repo>/commits --jq '.[0:5][] | "\(.commit.author.date) \(.commit.message|split("\n")[0])"'
# 许可正文：SPDX 字段写 NOASSERTION 时必须读原文
gh api repos/<owner>/<repo>/license --jq '.content' | base64 -d | head -60
```

star 数只用于排序，不参与判定。下文所有日期均为最后一次提交（`pushed_at`），不代表功能可用性。

## 一、按环节拆解

链上分析的技术栈是一条流水线，每个环节独立选型，不要一上来就找"一站式平台"。

| 环节 | 要解决的事 | 候选池 | 成熟度 |
| --- | --- | --- | --- |
| **数据采集** | 从链上/API 拿原始数据 | ethereum-etl、TrueBlocks、ponder、Blockscout、Tronscan / TronGrid API、fystack/multichain-indexer | EVM 高 / **TRON 低** |
| **数据存储** | 存交易、地址、标签，支持图查询 | PostgreSQL、ClickHouse、Neo4j、FalkorDB / Memgraph | 高 |
| **图计算** | 路径查找、社区发现、中心度 | NetworkX、Neo4j GDS、igraph | 高 |
| **地址聚类与标签** | 归集地址、打标签 | GraphSense TagPack、OpenSanctions、OFAC 地址提取 | 中（无成套方案） |
| **分析平台** | 把上面几层拼起来 | GraphSense（唯一活跃） | 中 |
| **可视化** | 资金树、流转图 | Cytoscape.js、AntV G6、sigma.js | 高 |
| **模型** | 可疑地址分类 | Elliptic++ 等公开数据集 + 论文实现 | 低（数据依赖重） |

## 二、维护状态核查（2026-11-18）

### 2.1 采集与平台

| 项目 | 环节 | 栈 / 许可 | star | 最后提交 | 判定 |
| --- | --- | --- | --- | --- | --- |
| [ethereum-etl](https://github.com/blockchain-etl/ethereum-etl) | 采集 | Python / MIT | 3,133 | 2026-01-25（2025-08 后无代码提交） | 观察：只适合补历史数据 |
| [ethereum-etl.rs](https://github.com/blockchain-etl/ethereum-etl.rs) | 采集 | Rust / **无 License** | 4 | 2026-01-25 | 排除：无许可 |
| [ethereum-etl-postgresql](https://github.com/blockchain-etl/ethereum-etl-postgresql) | 入库 | Shell / MIT | 150 | 2024-04-11 | 排除：停更 |
| [bitcoin-etl](https://github.com/blockchain-etl/bitcoin-etl) | 采集 | Python / MIT | 463 | 2025-05-02 | 排除：18 个月无提交 |
| [TrueBlocks](https://github.com/TrueBlocks/trueblocks-core) | 采集/索引 | GPL-3.0 | 1,094 | 2026-11-04 | 备选：仅 EVM，需 tracing/archive 节点 |
| [ponder](https://github.com/ponder-sh/ponder) | 索引框架 | TS / MIT | 1,156 | 2026-11-17 | 备选：只做 EVM 合约事件 |
| [Erigon](https://github.com/erigontech/erigon) | 节点 | Go / LGPL-3.0 | 3,644 | 2026-11-18 | 仅"必须自建归档节点"时 |
| [java-tron](https://github.com/tronprotocol/java-tron) | 节点 | Java / LGPL-3.0 | 4,180 | 2026-11-18 | 仅"必须自建 TRON 节点"时 |
| [Otterscan](https://github.com/otterscan/otterscan) | 浏览器 | TS / MIT | 1,427 | 2026-02-02 | 观察：依赖 Erigon，9 个月无提交 |
| [Blockscout](https://github.com/blockscout/blockscout) | 浏览器 | Elixir / **自有许可** | 4,784 | 2026-11-18 | 可用但许可受限，见 3.1 |
| [fystack/multichain-indexer](https://github.com/fystack/multichain-indexer) | 采集 | Go / MIT | 111 | 2026-11-14 | 观察：唯一同时覆盖 TRON + BSC 的活跃索引器 |
| [tronetl](https://github.com/c0mm4nd/tronetl) | 采集 | Go / **无 License** | 6 | 2026-02-05 | 排除：需自建全节点 + 无许可 |
| [tronscan-api](https://github.com/tronscan/tronscan-api) | 采集 | Scala / **无 License** | 74 | 2023-10-30 | 排除：停更且无许可 |
| [tronscan-frontend](https://github.com/tronscan/tronscan-frontend) | 浏览器前端 | JS / LGPL-3.0 | 283 | 2024-01-20 | 排除：停更 |
| [trx-client](https://github.com/graphsense/trx-client) | 采集 | Docker 封装 | 0 | 2026-11-02 | 只能喂 GraphSense，不单独用 |
| [graphsense-lib](https://github.com/graphsense/graphsense-lib) | 平台 | Python / MIT | 21 | 2026-11-17 | 方法学参考，不部署 |
| [graphsense-dashboard](https://github.com/graphsense/graphsense-dashboard) | 前端 | MIT | 143 | 2026-11-17 | 同上 |
| [graphsense-transformation](https://github.com/graphsense/graphsense-transformation) | 平台 | Scala / MIT | 16 | 2024-01-08 | **已归档**，能力并入 lib |
| [BlockSci](https://github.com/citp/BlockSci) | 分析 | C++ / GPL-3.0 | 1,399 | 2021-12-13 | 排除：停止维护 |
| [marble](https://github.com/checkmarble/marble) | 决策引擎 | Elastic 2.0 | 625 | 2026-11-16 | 参考，不集成（非 OSI 许可） |

### 2.2 存储、图计算与可视化

| 项目 | 环节 | 栈 / 许可 | star | 最后提交 | 判定 |
| --- | --- | --- | --- | --- | --- |
| [NetworkX](https://github.com/networkx/networkx) | 图算法 | Python / BSD-3 | 17,401 | 2026-11-17 | **主力** |
| [Neo4j GDS](https://github.com/neo4j/graph-data-science) | 图数据库 | Java / GPLv3 + 商业混合 | 828 | 2026-11-06 | 规模上去再换 |
| [Kuzu](https://github.com/kuzudb/kuzu) | 图数据库 | C++ / MIT | 4,022 | 2025-10-10 | 排除：**已归档** |
| [FalkorDB](https://github.com/FalkorDB/FalkorDB) | 图数据库 | Rust / **SSPL** | 10,506 | 2026-11-18 | 排除：SSPL + 800+ 未决 Issue |
| [Memgraph](https://github.com/memgraph/memgraph) | 图数据库 | C++ / **BSL 1.1** | 4,664 | 2026-11-18 | 排除：BSL |
| [ClickHouse](https://github.com/ClickHouse/ClickHouse) | 列存 | C++ / Apache-2.0 | 50,992 | 2026-11-18 | 只在量级需要时 |
| [Cytoscape.js](https://github.com/cytoscape/cytoscape.js) | 可视化 | JS / MIT | 11,296 | 2026-11-10 | **主力** |
| [AntV G6](https://github.com/antvis/G6) | 可视化 | TS / MIT | 12,398 | 2026-11-13 | 备选，中文文档友好 |
| [sigma.js](https://github.com/jacomyal/sigma.js) | 可视化 | TS / MIT | 12,246 | 2026-11-10 | 备选：万级节点渲染 |

### 2.3 标签与数据源

| 项目 | 用途 | 许可 | star | 最后提交 | 判定 |
| --- | --- | --- | --- | --- | --- |
| [GraphSense TagPack](https://github.com/graphsense/graphsense-tagpacks) | 公开标签包 | MIT | 40 | 2026-11-18 | 可用，但需自建 TagStore |
| [OpenSanctions](https://github.com/opensanctions/opensanctions) | 制裁 / PEP 数据 | MIT | 879 | 2026-11-18 | 可用：制裁口径的第一手来源 |
| [OFAC 地址提取](https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses) | OFAC 制裁地址 | MIT | 180 | 2026-11-07 | 可用，但**单一来源**，不能单独定案 |
| [etherscan-labels](https://github.com/brianleect/etherscan-labels) | 交易所标签数据集 | MIT | 287 | 2023-10-01 | 排除：数据停在 2023 |
| [Elliptic++](https://github.com/git-disl/EllipticPlusPlus) | 学术数据集 | **无 License** | 170 | 2023-11-25 | 排除：无许可 + 比特币 2011–2013 数据 |
| [AMLSim](https://github.com/IBM/AMLSim) | 合成交易数据 | Apache-2.0 | 414 | 2025-09-17 | 观察：可生成测试数据，14 个月无提交 |

## 三、关键发现

### 3.1 Blockscout 的许可变了，直接改写 fork 结论

【事实｜[LICENSE](https://github.com/blockscout/blockscout/blob/master/LICENSE)，生效日 2026-04-22】许可标识从 GPL 改为 `LicenseRef-Blockscout`，许可方为 Blockscout Limited（塞舌尔），条款要点：

| 条款 | 内容 | 对我们的影响 |
| --- | --- | --- |
| 授权范围 | 可下载、使用、部署、复制、修改、创作衍生作品 | 内部研判使用**可以** |
| 授权性质 | **temporary、revocable**，可单方变更 | 不是永久许可，存在被撤回的风险 |
| 商业限制 | 未经商业许可，不得出售、托管或以任何收费形式对外提供 | 内部平台没事，对外服务不行 |
| 署名义务 | 任何用户界面须显著标注 "Powered by Blockscout" 并链回官网 | 交付界面要留位置 |
| 溯及力 | 明确**不适用**于 Prior Software（生效日前的版本） | 需要锁旧版本时仍可走 GPL 路线 |

【推断｜置信度：高】**"fork Blockscout 长期自用"这条路的确定性下降了**：不是不能做，而是不能把它当成一次性投入——许可可以变，改一次条款就得重新评估。这也是本页仍维持"优先旁挂、不做 fork"的原因之一。详见 [Blockscout 专题](./blockscout)。

::: tip 复核提醒
`docs/tech/blockscout.md` 与仓库 `CONTRIBUTING.md` 里"GPL"的表述已过时，待同步。
:::

### 3.2 GraphSense 支持 TRON，且架构已经重构（纠正原稿）

原稿写"TRON 不在支持列表里"，**这条已经过时**：

【事实｜[graphsense-lib](https://github.com/graphsense/graphsense-lib) 代码树】`spark/src/main/scala/org/graphsense/account/trx/` 下有完整的 TRON transformation（`Source` / `Transformation` / `Tokens` / `Model`），并有 `0to10000` 区块的测试样本；组织下另有 [trx-client](https://github.com/graphsense/trx-client)（2026-11-02 提交）。

【事实｜组织仓库列表，2026-11-18】活跃组件：`graphsense-lib`（2.20.3，2026-11-02 发布）、`graphsense-dashboard`、`graphsense-tagpacks`、以及 btc / bch / ltc / zec / eth / trx 六个 client。**没有 bsc-client**。旧的 `graphsense-transformation`、`graphsense-spark`、`graphsense-REST` 全部已归档，能力并入 `graphsense-lib`（Python，含 REST API + ingestion）。

【推断｜置信度：高】结论因此调整为：**GraphSense 覆盖 TRON，唯一缺口是 BSC**；不部署的理由从"不支持 TRON"改成"Cassandra + Spark 的运维成本 + 无 BSC"，与[链上组工具页](/onchain/tools)的结论一致。

### 3.3 TRON 数据采集的真实缺口

| 路线 | 现状 | 代价 |
| --- | --- | --- |
| TronGrid / Tronscan 公开 API | 可用，需 Key，字段受端点限制 | 批量受限于限流，不是"开源项目"但最省事 |
| `fystack/multichain-indexer` | MIT，Go 单二进制，14 链含 TRON + BSC，带 RPC 故障转移与断点续跑 | 面向"监控入账地址"，需改造成通用拉取；111 star，单人/小团队维护 |
| GraphSense `trx-client` + lib | 唯一成熟的开源 TRON 采集链路 | 产物是 GraphSense 内部格式，要配 Cassandra |
| `tronetl` | CSV 导出，功能对口 | 需自建 TRON 全节点 + **无 License**（一票否决） |

【推断｜置信度：中高】**TRON 侧不存在"拿来即用、可商用、活跃维护"的开源 ETL**。要么走 API，要么接受 fystack 的改造工作量，要么自建节点。这是本页最硬的缺口，也是原型阶段建议"先 API 后自建"的直接理由。

### 3.4 已经不能选的项目，为什么还在推荐榜上

| 项目 | 死亡证据 | 仍被推荐的原因 |
| --- | --- | --- |
| BlockSci | 最后提交 2021-12-13，86 个未决 Issue | 论文引用多，是"链上分析"的经典答案 |
| Kuzu | 仓库已归档（2025-10-10） | 嵌入式图库很诱人，但项目本身停了 |
| bitcoin-etl | 2025-05-02 后无提交 | 与 ethereum-etl 同门，被顺带列入 |
| tronscan-api / tronetl | 停更 + 无 License | 搜"TRON API"最先命中 |

【推断｜置信度：高】**清单类文章的信号衰减很快**。以"star 多 + 被引用多"作为选型依据，平均会滞后一到两年；本页的 `pushed_at` 与 `archived` 两个字段，就是为了把这类滞后一次性过滤掉。

### 3.5 高星 ≠ 可用：一个必须记下的反面案例

调研中撞到一个典型样本：[Wallet-Risk-Scanner](https://github.com/Soniavasseur/Wallet-Risk-Scanner)（916 star，MIT，宣称 15+ 链、6 家情报源聚合）。看起来很对口，但核查结果如下：

| 核查项 | 观察 |
| --- | --- |
| 创建时间 | 2026-09-22，两个月冲到 916 star |
| 贡献者 | 1 人 |
| 提交节奏 | 每 20–30 分钟一条，提交信息统一为 `Auto commit: <时间>` —— 机器流水，不是开发活动 |
| Issue / Release | 0 个未决 Issue，1 个 Release |
| 依赖 | 6 家商业情报 API，需自备 Key 才能跑 |

【事实｜上述均由 GitHub API 读取】该仓库**不满足**"有实质开发活动"这一条；【推断｜置信度：中高】其 star 增长与自动化提交形态不具备工程可信度，**不作为选型基础**，仅可读其评分分层思路。

【结论】**快速识别刷量仓库的三条**：贡献者是否只有 1 人、提交信息是否模板化、star 增长是否与 Issue/Release 活动脱节。三条占两条就降级为"只读参考"。

### 3.6 决策引擎：没有可直接集成的开源选项

[marble](https://github.com/checkmarble/marble) 是这一层最像样的项目（实时反欺诈/反洗钱决策引擎，625 star，2026-11-16 仍在提交），但许可为 **Elastic License 2.0**：允许内部使用与修改，禁止把其功能作为托管服务对外提供。FalkorDB（SSPL）、Memgraph（BSL 1.1）同理。

【推断｜置信度：高】这类"源码可见但非 OSI"的许可，对**内部研判平台**没有阻碍，但对**未来可能对外交付的系统**是隐患。当前阶段不需要决策引擎：规则数量在百条以内时，一段 JSON 规则 + Python 求值函数就够，引入决策引擎是提前背上运维与许可两笔债。

## 四、推荐组合（去重后）

| 层 | 选择 | 理由 | 反悔成本 |
| --- | --- | --- | --- |
| 数据 | **公开 API（TronGrid / Tronscan + Etherscan 系）+ 本地 PostgreSQL 缓存** | 零门槛起步；缓存层隔开数据源变更 | 低：换源只改采集器 |
| 图计算 | **NetworkX** | 纯 Python，算法齐全，团队零学习成本 | 低：接口与 Neo4j GDS 概念对应 |
| 可视化 | **Cytoscape.js** | 专用图库，布局与交互够用，可直接接前端原型 | 中：换 G6 需重写渲染层 |
| 规则 | **自研 JSON 规则引擎** | 可解释、可版本化、可写测试；无标注数据前唯一正确选择 | 低 |
| 备选（不部署） | GraphSense `graphsense-lib` + TagPack | MIT、支持 TRON、方法学透明，是标签与聚类的参考实现 | — |

**只推三件 + 一个自研，其余一律不引入。** 备选项只在"需要一套成体系的标签标准"时查阅代码与数据格式，不落地部署。

::: tip 这套组合的边界
能支撑万级地址、十万级交易的分析。超过这个量级，把图计算换成 Neo4j GDS，把存储换成 ClickHouse。**到那时再换，现在不为未来买单。**
:::

## 五、明确不做的方向

| 不做 | 原因 |
| --- | --- |
| 自建全节点同步 | 存储与带宽成本高；TRON 侧还要额外维护 java-tron，公开 API 能满足定向分析 |
| fork Blockscout 做长期自用平台 | 许可可撤销、可单方变更，且要长期承担 Elixir 维护；旁挂已够用（见 3.1） |
| 训练自己的地址分类模型 | 无标注数据；Elliptic++ 无许可且是 2011–2013 比特币数据，跨场景不可迁移 |
| 做通用链上浏览器 | Blockscout / Otterscan 已实现，自建全量索引是 TB 级投入 |
| 引入图数据库 | MVP 阶段节点数不够大，PostgreSQL + NetworkX 够用；Kuzu 已归档、FalkorDB / Memgraph 许可受限 |
| 引入决策引擎 | 规则量级不需要，且 Elastic 2.0 / SSPL / BSL 都是对外交付时的隐患 |
| 支持全链 | 先做 TRON + ETH/BSC，其他链等有明确需求再扩 |

## 六、局限与待验证

- 【待验证】`fystack/multichain-indexer` 与 `tronetl` 均**未实测**，判断仅基于 README 与提交记录；改造工作量需要跑一次才知道。
- 【待验证】GraphSense 的部署成本（Cassandra + Spark）未实测，本页"不部署"的结论基于运维人力而非实测数据。
- 【推断】清理混币、OTC 商户识别、跨链桥跳转这三类场景，**公开检索未发现可用的开源实现**（置信度：中高）——不代表不存在，只代表不在主流清单里。
- 【事实】star 与 `pushed_at` 是 2026-11-18 的快照，会变；引用超过一个季度请按「调研口径」里的命令重跑一遍。
- 【法律提示】3.1 的许可条款为人工阅读归纳，不构成法律意见；正式对外交付前应由法务复核 `LICENSE` 原文。
- 【口径】本页不评估任何工具的**检测准确率**——没有统一测试集，任何"准确率"数字都是不可比的。

## 七、待办

- [x] 逐个核实候选项目的维护状态与许可（2026-11-18，GitHub API 全量核查）
- [x] 核实 Blockscout 的维护状态与部署成本（详见 [Blockscout 专题](./blockscout)）
- [x] 评估 GraphSense 的部署门槛并给结论——见 3.2，结论为"读代码不部署"
- [ ] 实测 `fystack/multichain-indexer` 拉 TRC20 转账，记录改造量
- [ ] 实测 Tronscan API 的限流与字段完整度，写成表格（与链上组共用）
- [ ] 写一个最小 demo：拉一个地址的 3 跳交易，存 PostgreSQL，用 NetworkX 算最短路径
- [ ] 给 `blockscout.md` 补一节许可说明，同步 `CONTRIBUTING.md` 中过时的 GPL 表述
- [ ] 与链上组对一次数据结构，确保标签与特征能互相导入

## 参考

均为公开仓库与官方文档，核查日期 **2026-11-18**。

1. [ethereum-etl](https://github.com/blockchain-etl/ethereum-etl) · [ethereum-etl.rs](https://github.com/blockchain-etl/ethereum-etl.rs) · [bitcoin-etl](https://github.com/blockchain-etl/bitcoin-etl)
2. [TrueBlocks](https://github.com/TrueBlocks/trueblocks-core) · [ponder](https://github.com/ponder-sh/ponder) · [fystack/multichain-indexer](https://github.com/fystack/multichain-indexer)
3. [Blockscout](https://github.com/blockscout/blockscout) · [LICENSE（LicenseRef-Blockscout，2026-04-22 生效）](https://github.com/blockscout/blockscout/blob/master/LICENSE) · [Otterscan](https://github.com/otterscan/otterscan)
4. [GraphSense lib](https://github.com/graphsense/graphsense-lib) · [dashboard](https://github.com/graphsense/graphsense-dashboard) · [TagPack](https://github.com/graphsense/graphsense-tagpacks) · [trx-client](https://github.com/graphsense/trx-client)
5. [BlockSci](https://github.com/citp/BlockSci) · [Kuzu](https://github.com/kuzudb/kuzu) · [marble](https://github.com/checkmarble/marble)
6. [NetworkX](https://github.com/networkx/networkx) · [Cytoscape.js](https://github.com/cytoscape/cytoscape.js) · [AntV G6](https://github.com/antvis/G6)
7. [OpenSanctions](https://github.com/opensanctions/opensanctions) · [OFAC 制裁地址提取](https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses) · [AMLSim](https://github.com/IBM/AMLSim)
8. [Tronscan API 文档](https://docs.tronscan.org/) · [TronGrid](https://www.trongrid.io/) · [java-tron](https://github.com/tronprotocol/java-tron)
9. [贡献指南](/guide/contribute) · [调研文档模板](/guide/template) · [Blockscout 专题](./blockscout)
