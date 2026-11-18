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
3. **`pushed_at` 会骗人，判据要换成"近 13 周提交数 + 最新 release + 提交内容"。** 按日期看 TrueBlocks 像是活跃的（2026-11-04 有推送），按提交内容看是**实质停摆**：近 13 周 2 次提交（"Cleaning" 与文档），最新 release 停在 2025-09-28。同类情况还有 AntV G6（近期提交全是版本号与主题 bump）。
4. **筛查层这次找到了真东西：`moov-io/watchman`**（Apache-2.0、525 star、44 贡献者、近 13 周 282 次提交）。一条 Docker 命令拉齐 OFAC / EU / UK / UN / OpenSanctions 八张名单，**支持按加密地址检索**（地址＋国家命中即 1.0 分），评分可读、可解释。这是本页唯一建议"值得装"的现成组件。
5. **聚类层的位置被 `bitiodine` 接住了。** Rust 写的比特币解析器 + 共花聚类（Union-Find），MIT/Apache 双许可，2026-11 仍在提交。它是 BlockSci 停摆后唯一"能跑、许可干净、还在动"的聚类实现——但只覆盖 BTC，**方法可借、代码不可搬到 TRON**。
6. **Blockscout 不再是 GPL。** 2026-04-22 起改用自有许可 `LicenseRef-Blockscout`：内部非商业使用可以，但许可可撤销、可单方变更，界面须保留 "Powered by Blockscout" 署名，SaaS 化或收费需另购商业许可。**fork 之前先锁旧版本**（该许可不溯及 Prior Software）。
7. **推荐组合：三件 + 自研 + 一个可选组件**——公开 API + PostgreSQL / NetworkX / Cytoscape.js / 自研规则引擎，外加 watchman 做名单筛查。万级节点之后升级到 Networkit（MIT）而不是 Neo4j；十万级大图渲染换 cosmos.gl（GPU）。

## 本页要回答的问题

1. 从**数据采集**到**可视化**，每个环节有哪些成熟开源项目？各自成熟度如何？
2. 哪些项目**已经停止维护**，不能再作为技术选型基础？
3. 哪些能力**可以自己写几百行解决**，不值得引入重型框架？
4. 最终推荐哪套组合？为什么是这套而不是别的？
5. 哪些方向**明确不做**？（避免摊子越铺越大）

## 调研口径

::: warning 判定标准：三条硬门槛 + 两条一票否决 + 一个活跃度指标
**硬门槛**：① 近 12 个月有实质提交（纯文档、修链接不算）② 有可运行的部署文档 ③ 许可允许内部非商业使用。
**一票否决**：仓库已 `archived`；仓库**没有 LICENSE**（无许可＝默认保留全部权利，不能内部使用）。
**活跃度指标**（不作否决，但决定"主力/备选/观察"）：近 13 周提交数、贡献者数、最新 release 日期。只看 `pushed_at` 会被"合了个依赖更新"骗过去。
:::

核查方式（任何人可复现，核查日 **2026-11-18**）：

```bash
# 基础元数据：最后提交、是否归档、许可
gh api repos/<owner>/<repo> --jq '{pushed_at, archived, license: .license.spdx_id}'
# 活跃度：近 13 周提交数 + 52 周总量（一个请求，比翻提交列表快）
gh api repos/<owner>/<repo>/stats/participation --jq '{last90d: (.all[-13:]|add), year: (.all|add)}'
# 提交内容：判断是人写的、脚本刷的、还是发版合并
gh api repos/<owner>/<repo>/commits --jq '.[0:5][] | "\(.commit.author.date) \(.commit.message|split("\n")[0])"'
# 许可正文：SPDX 字段写 NOASSERTION 时必须读原文
gh api repos/<owner>/<repo>/license --jq '.content' | base64 -d | head -60
```

star 数只用于排序，不参与判定。

## 一、按环节拆解

链上分析的技术栈是一条流水线，每个环节独立选型，不要一上来就找"一站式平台"。

| 环节 | 要解决的事 | 候选池 | 成熟度 |
| --- | --- | --- | --- |
| **数据采集** | 从链上/API 拿原始数据 | ethereum-etl、ponder、Blockscout、fystack/multichain-indexer、Tronscan / TronGrid API | EVM 高 / **TRON 低** |
| **数据存储** | 存交易、地址、标签，支持图查询 | PostgreSQL、ClickHouse、Neo4j、FalkorDB / Memgraph | 高 |
| **名单筛查** | 地址/实体是否命中制裁与黑名单 | **watchman**、OpenSanctions、OFAC 地址提取、scam-database | **中高（新）** |
| **图计算** | 路径查找、社区发现、中心度 | NetworkX、Networkit、Neo4j GDS、igraph | 高 |
| **地址聚类与标签** | 归集地址、打标签 | bitiodine（BTC 参考实现）、GraphSense TagPack | 中（无成套方案） |
| **分析平台** | 把上面几层拼起来 | GraphSense（唯一活跃） | 中 |
| **可视化** | 资金树、流转图 | Cytoscape.js、sigma.js、cosmos.gl、AntV G6 | 高（G6 转维护模式） |
| **交易解码** | 看懂一笔交易的合约调用 | evm-trace、tx2uml / sol2uml | 中 |
| **模型** | 可疑地址分类 | Elliptic++ 等公开数据集 + 论文实现 | 低（数据依赖重） |

## 二、维护状态核查（2026-11-18）

### 2.1 采集与平台

| 项目 | 环节 | 栈 / 许可 | star | 最后提交 | 判定 |
| --- | --- | --- | --- | --- | --- |
| [ethereum-etl](https://github.com/blockchain-etl/ethereum-etl) | 采集 | Python / MIT | 3,133 | 2026-01-25（2025-08 后无代码提交） | 观察：只适合补历史数据 |
| [ethereum-etl.rs](https://github.com/blockchain-etl/ethereum-etl.rs) | 采集 | Rust / **无 License** | 4 | 2026-01-25 | 排除：无许可 |
| [ethereum-etl-postgresql](https://github.com/blockchain-etl/ethereum-etl-postgresql) | 入库 | Shell / MIT | 150 | 2024-04-11 | 排除：停更 |
| [bitcoin-etl](https://github.com/blockchain-etl/bitcoin-etl) | 采集 | Python / MIT | 463 | 2025-05-02 | 排除：18 个月无提交 |
| [TrueBlocks](https://github.com/TrueBlocks/trueblocks-core) | 采集/索引 | GPL-3.0 | 1,094 | 2026-11-04 | **观察**：近 13 周仅 2 次提交，release 停在 2025-09-28，实质停摆 |
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
| [AntV G6](https://github.com/antvis/G6) | 可视化 | TS / MIT | 12,398 | 2026-11-13 | 不推荐：维护模式，release 停在 2026-04，335 个未决 Issue |
| [sigma.js](https://github.com/jacomyal/sigma.js) | 可视化 | TS / MIT | 12,246 | 2026-11-10 | 备选：万级节点渲染 |
| [cosmos.gl](https://github.com/cosmograph-org/cosmos) | 可视化 | TS / MIT | 1,310 | 2026-11-18 | 备选：GPU 渲染，十万级节点 |
| [Networkit](https://github.com/networkit/networkit) | 图算法 | C++/Python / MIT | 886 | 2026-11-16 | **升级路径**：万级节点后替换 NetworkX |

### 2.3 标签与数据源

| 项目 | 用途 | 许可 | star | 最后提交 | 判定 |
| --- | --- | --- | --- | --- | --- |
| [GraphSense TagPack](https://github.com/graphsense/graphsense-tagpacks) | 公开标签包 | MIT | 40 | 2026-11-18 | 可用，但需自建 TagStore |
| [OpenSanctions](https://github.com/opensanctions/opensanctions) | 制裁 / PEP 数据 | MIT | 879 | 2026-11-18 | 可用：制裁口径的第一手来源 |
| [OFAC 地址提取](https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses) | OFAC 制裁地址 | MIT | 180 | 2026-11-07 | 可用，但**单一来源**，不能单独定案 |
| [etherscan-labels](https://github.com/brianleect/etherscan-labels) | 交易所标签数据集 | MIT | 287 | 2023-10-01 | 排除：数据停在 2023 |
| [Elliptic++](https://github.com/git-disl/EllipticPlusPlus) | 学术数据集 | **无 License** | 170 | 2023-11-25 | 排除：无许可 + 比特币 2011–2013 数据 |
| [AMLSim](https://github.com/IBM/AMLSim) | 合成交易数据 | Apache-2.0 | 414 | 2025-09-17 | 观察：可生成测试数据，14 个月无提交 |

### 2.4 第二轮补充：按缺口找出来的候选

上一版按"环节"找，漏了两个真实缺口——**名单筛查**和**地址聚类**。这一轮按缺口反向检索，补到以下项目：

| 项目 | 补的是哪个缺口 | 栈 / 许可 | star | 13 周提交 | 判定 |
| --- | --- | --- | --- | --- | --- |
| [moov-io/watchman](https://github.com/moov-io/watchman) | 制裁 / 黑名单筛查 | Go / Apache-2.0 | 525 | 282 | **建议装**：见 3.5 |
| [bitiodine](https://github.com/mikispag/bitiodine) | BTC 地址聚类 | Rust / MIT 或 Apache-2.0 | 160 | 43 | **方法参考**：见 3.6 |
| [altscan](https://github.com/heathermhuang/altscan) | BSC 浏览器 | TS / **AGPL-3.0** | 3 | 日更 | 观察：唯一的 BSC 开源浏览器，见 3.7 |
| [evm-trace](https://github.com/ApeWorX/evm-trace) | 交易 trace 解码 | Python / Apache-2.0 | 320 | 13 | 备选：看合约调用时用 |
| [scamsniffer/scam-database](https://github.com/scamsniffer/scam-database) | 诈骗地址 / 域名黑名单 | GPL-3.0 | 273 | — | 观察：社区维护黑名单，数据可用、口径未公开 |
| [tx2uml](https://github.com/naddison36/tx2uml) | 交易时序图 | TS / MIT | 478 | 0 | 排除：90 天零提交，只当一次性出图工具 |
| [sol2uml](https://github.com/naddison36/sol2uml) | 合约结构图 | TS / MIT | 1,321 | 0 | 同上 |
| [sieve-aml](https://github.com/AbgarSim/sieve-aml) | 制裁名单聚合 | Java / MIT | 16 | — | **不引入**：与 watchman 重复，按去重原则砍掉 |
| [Wallet-Risk-Scanner](https://github.com/Soniavasseur/Wallet-Risk-Scanner) | 风险评分 | Python / MIT | 916 | 机器日更 | 排除：见 3.8 |

### 2.5 活跃度量化（近 13 周提交 / 贡献者 / 最新 release）

"活跃"这个词在选型里最容易注水，所以给数字：

| 项目 | 13 周提交 | 52 周提交 | 贡献者 | 最新 release | 读法 |
| --- | --- | --- | --- | --- | --- |
| erigon | 1,870 | 4,710 | 100+ | 2026-10-23 | 高速开发，跟版本要谨慎 |
| opensanctions | 1,743 | 6,974 | 63 | 无 release（按日更新数据） | 数据管道型，看数据不看版本 |
| graphsense-lib | 384 | 1,380 | 10 | 2026-11-02 | 小团队但稳定发版 |
| moov-io/watchman | 282 | 711 | 44 | 2026-11-16 | 健康 |
| cosmos.gl | 261 | 573 | 12 | 2026-11-04 | 健康 |
| blockscout | 199 | 828 | 100+ | 2026-11-02 | 健康，但许可要看 |
| networkit | 164 | 388 | 100+ | 无 release（滚动发布） | 健康 |
| ponder | 130 | 362 | 100+ | 2026-11-17 | 健康 |
| cytoscape.js | 133 | 325 | 100+ | 2026-11-10 | 健康 |
| networkx | 83 | 310 | 100+ | 2026-09-21 | 稳定，低风险 |
| bitiodine | 43 | 43 | 3 | 无 release | 新项目，全部提交都在近 3 个月 |
| fystack/multichain-indexer | 18 | 176 | 9 | 2026-02-04 | 中小团队，发版慢 |
| marble | 7 | 47 | 16 | 2026-11-16 | open-core：公开仓库只有发版合并 |
| antvis/G6 | 10 | 44 | 100+ | 2026-04-17 | 维护模式，提交基本是版本 bump |
| TrueBlocks | 2 | 30 | 71 | 2025-09-28 | **实质停摆** |

【事实｜上述数字来自 GitHub `stats/participation` 与 `releases/latest`，2026-11-18】这张表比任何 star 数都更能说明"还能不能押上去"。

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

::: tip 复核提醒（2026-11-18 已处理）
`blockscout.md` 4.5 节已补许可说明；`CONTRIBUTING.md` 经全文检索并无 GPL 表述，无需修改。本提醒保留作为口径变更的留痕，下个季度复核时删除。
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
| TrueBlocks | 近 13 周 2 次提交，release 停在 2025-09-28 | `pushed_at` 显示 2026-11，看起来一直在动 |
| AntV G6 | 近期提交全是版本号与主题 bump，release 停在 2026-04-17 | star 1.2 万，中文文档好 |

【推断｜置信度：高】**清单类文章的信号衰减很快**。以"star 多 + 被引用多"作为选型依据，平均会滞后一到两年；本页的 `pushed_at`、`archived`、13 周提交数三个字段，就是为了把这类滞后一次性过滤掉。

### 3.5 名单筛查：`watchman` 补上了最缺的一块

【事实｜[README](https://github.com/moov-io/watchman) + 元数据】Apache-2.0、525 star、44 贡献者、2026-11-16 发版、近 13 周 282 次提交。一条 `docker run` 就拉齐并索引 OFAC SDN / Non-SDN、US CSL、FinCEN 311、EU、UK、UN、OpenSanctions 八类名单；检索字段包含 **crypto**，地址（需同时给国家字段）命中直接计 1.0 分，姓名/证件/地址等字段按权重叠加，输出 0–1 的可解释评分。

为什么它值得装：我们缺的不是"名单文件"，是**把名单变成可查询判据**的那一层。之前只能人工在 OFAC 页面粘地址比对，这是典型的"几十行脚本也能做、但做不好"的活——重名、别名、跨语言、证件号冲突的处理，watchman 已经写完了。

| 它解决 | 它不解决 |
| --- | --- |
| 某地址是否命中公开制裁/执法名单 | 这个地址属于谁（实体归属仍需 Arkham / OKLink 交叉印证） |
| 命中后的评分与可读依据 | 名单之外的风险（跑分、资金盘地址不在制裁名单里） |
| 名单的持续更新与索引 | 链上资金流追踪 |

【事实｜检索记录】市面上同类的 [sieve-aml](https://github.com/AbgarSim/sieve-aml)（MIT、16 star，35+ 名单）功能重叠，按本页"同一能力只留一个实现"的原则**不引入**。

### 3.6 聚类：BlockSci 的位置被 `bitiodine` 接住了，但只接了一半

【事实｜[README](https://github.com/mikispag/bitiodine) + 元数据】Rust 编写、MIT 或 Apache-2.0 双许可、160 star、3 贡献者、**43 次提交全部落在近 13 周**（等于一个刚重写的新项目）。做法是解析 `bitcoind` 的 `blk*.dat`，用 Union-Find 做共花（co-spend）聚类，状态存 SQLite、按块提交、可断点续跑，并处理链重组，支持 Taproot 及未来 witness 版本。

| 能借的 | 不能借的 |
| --- | --- |
| 共花聚类 + Union-Find 的工程实现（含续跑、回滚） | 代码本身只吃 BTC 区块文件，TRON / EVM 用不上 |
| "聚类结果要能重放"的设计——链重组必须能回滚 | 账户模型链没有"共花"这个概念，判据要重写 |
| 地址聚合后接图分析的输出格式 | 需要自建 BTC 全节点（`blk*.dat` 是输入） |

【推断｜置信度：中高】把"共花"换成账户模型上可观测的同源特征（同笔交易内的多地址归集、Gas 支付同源、批量生成地址的 nonce 序列），方法可以迁移；这类判据的界定属于链上组，本页不越界定义，只标注"有现成参考实现可读"。详见[异常地址特征](/onchain/address-features)。

### 3.7 BSC：除自建 Blockscout 外，多了 `altscan` 一条路

【事实｜[README](https://github.com/heathermhuang/altscan) + 元数据】**AGPL-3.0**，Next.js 15 + Drizzle ORM + ethers.js，一套代码同时驱动 BNB Chain 与 Ethereum 两个浏览器（线上为 bnbscan.com、ethscan.io），由 Measurable Data Token 维护，仓库有 `watch_addresses` 表与 watchlist 路由、钱包监控事件流，单开发者近乎日更，但只有 3 star。

| 维度 | 结论 |
| --- | --- |
| 定位 | 浏览器前端 + 索引，不是分析平台；与 Blockscout 同一层 |
| 许可 | AGPL-3.0：内部使用无碍，**对外提供服务须开源修改**——比 Blockscout 的新许可更"硬"，但至少是 OSI 认证的 |
| 成熟度 | 3 star、单人维护、代码新，**不能当基础设施押注** |
| 建议 | 读代码借鉴其 BSC 索引与地址监控实现；真要部署仍优先 Blockscout（生态、文档、坑都更多） |

### 3.8 高星 ≠ 可用：一个必须记下的反面案例

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

### 3.9 决策引擎：没有可直接集成的开源选项

[marble](https://github.com/checkmarble/marble) 是这一层最像样的项目（实时反欺诈/反洗钱决策引擎），2026-11-16 刚发 1.14，但三件事决定了它不能当基础设施：许可为 **Elastic License 2.0**（允许内部使用与修改，禁止把其功能作为托管服务对外提供）；公开仓库近 13 周只有 7 次提交，**都是发版合并**（open-core，实际开发在私有分支）；FalkorDB（SSPL）、Memgraph（BSL 1.1）同理。

【推断｜置信度：高】这类"源码可见但非 OSI"的许可，对**内部研判平台**没有阻碍，但对**未来可能对外交付的系统**是隐患。当前阶段不需要决策引擎：规则数量在百条以内时，一段 JSON 规则 + Python 求值函数就够，引入决策引擎是提前背上运维与许可两笔债。

## 四、推荐组合（去重后）

| 层 | 选择 | 理由 | 反悔成本 |
| --- | --- | --- | --- |
| 数据 | **公开 API（TronGrid / Tronscan + Etherscan 系）+ 本地 PostgreSQL 缓存** | 零门槛起步；缓存层隔开数据源变更 | 低：换源只改采集器 |
| 筛查 | **moov-io/watchman**（Docker 单容器） | 唯一"装得上、评分可解释、Apache-2.0"的名单筛查引擎 | 低：旁挂服务，不进主链路 |
| 图计算 | **NetworkX** | 纯 Python，算法齐全，团队零学习成本 | 低：升级目标已定（Networkit，MIT） |
| 可视化 | **Cytoscape.js** | 专用图库，布局与交互够用，可直接接前端原型 | 中：换 sigma.js / cosmos.gl 需重写渲染层 |
| 规则 | **自研 JSON 规则引擎** | 可解释、可版本化、可写测试；无标注数据前唯一正确选择 | 低 |
| 备选（不部署） | GraphSense `graphsense-lib` + TagPack | MIT、支持 TRON、方法学透明，是标签与聚类的参考实现 | — |

**三件 + 一个自研 + 一个可选组件，其余一律不引入。** 升级路径写死，避免临到规模上来再临时选型：图计算 `NetworkX → Networkit`（MIT，万级节点）、可视化 `Cytoscape.js → cosmos.gl`（GPU，十万级节点）。

::: tip 这套组合的边界
能支撑万级地址、十万级交易的分析。超过这个量级，图计算换 Networkit、可视化换 cosmos.gl、存储换 ClickHouse——**都不需要碰 GPL / SSPL 的图数据库**。
:::

## 五、明确不做的方向

| 不做 | 原因 |
| --- | --- |
| 自建全节点同步 | 存储与带宽成本高；TRON 侧还要额外维护 java-tron，公开 API 能满足定向分析 |
| fork Blockscout 做长期自用平台 | 许可可撤销、可单方变更，且要长期承担 Elixir 维护；旁挂已够用（见 3.1） |
| 自研名单筛查 | watchman 已经把重名、别名、跨语言、证件冲突这些脏活写完了，重写等于重新踩一遍 |
| 训练自己的地址分类模型 | 无标注数据；Elliptic++ 无许可且是 2011–2013 比特币数据，跨场景不可迁移 |
| 做通用链上浏览器 | Blockscout / altscan 已实现，自建全量索引是 TB 级投入 |
| 引入图数据库 | MVP 阶段节点数不够大，PostgreSQL + NetworkX 够用；Kuzu 已归档、FalkorDB / Memgraph 许可受限 |
| 引入决策引擎 | 规则量级不需要，且 Elastic 2.0 / SSPL / BSL 都是对外交付时的隐患 |
| 引入 AntV G6 或同类图库做叠加 | 与 Cytoscape.js 功能重叠，G6 已进入维护模式；一个能力只留一个实现 |
| 支持全链 | 先做 TRON + ETH/BSC，其他链等有明确需求再扩 |

## 六、局限与待验证

- 【待验证】`fystack/multichain-indexer`、`tronetl`、`bitiodine`、`watchman` 均**未实测**，判断基于 README、提交记录与许可文本；改造量与命中率要跑一次才知道。
- 【待验证】`altscan` 只读了 README，代码质量与索引完整性未验证；3 star、单人维护的样本不足以支撑"可部署"的结论。
- 【口径】2.5 的"13 周提交数"来自 GitHub participation 统计，**含合并提交与依赖更新**，因此必须与提交内容对照读（TrueBlocks 与 G6 的结论就是这么翻过来的）。
- 【待验证】GraphSense 的部署成本（Cassandra + Spark）未实测，本页"不部署"的结论基于运维人力而非实测数据。
- 【推断】清理混币、OTC 商户识别、跨链桥跳转这三类场景，**多轮公开检索（关键词：mixer detection / cross-chain tracing / wallet attribution）均未找到可用的开源实现**（置信度：中高）——命中的多为论文复现或单文件脚本，不具备部署条件。
- 【事实】star、`pushed_at`、提交数均为 2026-11-18 的快照，会变；引用超过一个季度请按「调研口径」里的命令重跑一遍。
- 【法律提示】3.1 的许可条款为人工阅读归纳，不构成法律意见；正式对外交付前应由法务复核 `LICENSE` 原文。
- 【口径】本页不评估任何工具的**检测准确率**——没有统一测试集，任何"准确率"数字都是不可比的。

## 七、待办

- [x] 逐个核实候选项目的维护状态与许可（2026-11-18，GitHub API 全量核查）
- [x] 核实 Blockscout 的维护状态与部署成本（详见 [Blockscout 专题](./blockscout)）
- [x] 评估 GraphSense 的部署门槛并给结论——见 3.2，结论为"读代码不部署"
- [x] 补第二轮：按缺口找名单筛查与地址聚类（watchman / bitiodine，见 3.5、3.6）
- [x] 用近 13 周提交数与 release 日期复核第一轮结论（推翻 TrueBlocks 与 G6 的"活跃"判断）
- [ ] 实测 watchman：导入 OFAC，对一个已知被制裁地址 + 一个干净地址筛查，记录评分与耗时
- [ ] 用 bitiodine 跑一段主网数据，验证共花聚类结果可复现、断点续跑正常
- [ ] 读 altscan 的 BSC 索引与地址监控实现，判断能否只借 `watch_addresses` 那一层
- [ ] 核实 scam-database 黑名单的收录口径与许可边界（GPL-3.0 用在数据上的实际含义）
- [ ] 实测 `fystack/multichain-indexer` 拉 TRC20 转账，记录改造量
- [ ] 实测 Tronscan API 的限流与字段完整度，写成表格（与链上组共用）
- [ ] 写一个最小 demo：拉一个地址的 3 跳交易，存 PostgreSQL，用 NetworkX 算最短路径
- [x] 给 `blockscout.md` 补一节许可说明（4.5 节，2026-11-18 完成）；`CONTRIBUTING.md` 全文检索无 GPL 表述，无需同步
- [ ] 与链上组对一次数据结构，确保标签与特征能互相导入

## 参考

均为公开仓库与官方文档，核查日期 **2026-11-18**。

1. [ethereum-etl](https://github.com/blockchain-etl/ethereum-etl) · [ethereum-etl.rs](https://github.com/blockchain-etl/ethereum-etl.rs) · [bitcoin-etl](https://github.com/blockchain-etl/bitcoin-etl)
2. [TrueBlocks](https://github.com/TrueBlocks/trueblocks-core) · [ponder](https://github.com/ponder-sh/ponder) · [fystack/multichain-indexer](https://github.com/fystack/multichain-indexer)
3. [Blockscout](https://github.com/blockscout/blockscout) · [LICENSE（LicenseRef-Blockscout，2026-04-22 生效）](https://github.com/blockscout/blockscout/blob/master/LICENSE) · [Otterscan](https://github.com/otterscan/otterscan) · [altscan](https://github.com/heathermhuang/altscan)
4. [GraphSense lib](https://github.com/graphsense/graphsense-lib) · [dashboard](https://github.com/graphsense/graphsense-dashboard) · [TagPack](https://github.com/graphsense/graphsense-tagpacks) · [trx-client](https://github.com/graphsense/trx-client)
5. [BlockSci](https://github.com/citp/BlockSci) · [bitiodine](https://github.com/mikispag/bitiodine) · [Kuzu](https://github.com/kuzudb/kuzu) · [marble](https://github.com/checkmarble/marble)
6. [NetworkX](https://github.com/networkx/networkx) · [Networkit](https://github.com/networkit/networkit) · [Cytoscape.js](https://github.com/cytoscape/cytoscape.js) · [sigma.js](https://github.com/jacomyal/sigma.js) · [cosmos.gl](https://github.com/cosmograph-org/cosmos)
7. [moov-io/watchman](https://github.com/moov-io/watchman) · [OpenSanctions](https://github.com/opensanctions/opensanctions) · [OFAC 制裁地址提取](https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses) · [scam-database](https://github.com/scamsniffer/scam-database)
8. [evm-trace](https://github.com/ApeWorX/evm-trace) · [AMLSim](https://github.com/IBM/AMLSim) · [Elliptic++](https://github.com/git-disl/EllipticPlusPlus)
9. [Tronscan API 文档](https://docs.tronscan.org/) · [TronGrid](https://www.trongrid.io/) · [java-tron](https://github.com/tronprotocol/java-tron)
10. [贡献指南](/guide/contribute) · [调研文档模板](/guide/template) · [Blockscout 专题](./blockscout)
