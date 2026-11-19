---
title: 开源项目全量扫描（2026-11-19）
---

# 开源项目全量扫描（2026-11-19）

<div class="doc-meta">
  <span class="owner">负责人：@Fiagainster</span>
  <span class="doing">状态：初稿完成</span>
</div>

> 本页是 [开源项目调研](./oss-projects) 的**全景补充页**。主页回答"选什么"（45 个项目的选型结论），本页回答"还有什么"——按六类对 GitHub 上的相关开源项目做了一轮全量扫描。核查快照：2026-11-18 夜 — 11-19 晨（GitHub API）。**全部基于静态走读与 API 元数据，未做运行实测**（本轮纪律：不构建、不运行克隆代码）。

## 结论摘要

1. **规模**：约 60 组关键词检索、约 110 个项目进入核查流程、85 行判定表、14 个仓库浅克隆走读。判定结果：**主力候选 10、备选 6、观察 13、参考 16、排除 15+、转交其他类 6**。
2. **主页 3.9"混币/跨链无可用开源实现"被部分推翻**：`prettydeath/TornadoCash-demixer`（MIT，8 条 EVM 链 56 个 Tornado 池的存取款关联取证，证据分级 + 安慰剂校准，2026-11-18 仍在提交）与 `bobslayerX/crypttrace`（MIT，TRON/SOL/TON/BTC 免 Key 多链追踪 + USDT/USDC 冻结直查 + PDF 证据包）是两个真主力候选。**但两者都是单人维护、star≤31**——"真金但没被看见"型，升级到主力前必须用已知案例自证。
3. **TRON 采集缺口有了新答案**：`subsquid/squid-sdk` 是唯一内置 TRON 原生摄取（直读 java-tron HTTP API）的主流框架；但 **tron/evm 核心包的 package.json 标 GPL-3.0-or-later**，不是顶层 Apache-2.0——内部使用合法，改造后对外分发需开源，边界要审计。ETH/BSC 侧补充 `rindexer`（Rust/MIT，YAML 无代码索引，Postgres/ClickHouse 双后端）。
4. **GNN 检测没有活跃上游可等**：唯一可运行的 AML-GNN 基线是 `IBM/Multi-GNN`（Apache-2.0，2024-02 起停更），检测模型页应以它为骨架自建 TRON/ETH 特征。**地址级 wallet drainer 黑名单是空缺**；域名层反而富裕：`phishdestroy/destroylist`（205k+ 域名、MIT、日更）+ MetaMask `eth-phishing-detect`（精度高但许可为非标准 DBAD，需法务确认）。
5. **蜜罐/honeypot 检测**：`malvaphe/Crypto_Honeypot_Detector` v2（eth_call state-override + eth_simulateV1 双模拟，BSC PancakeSwap 一等支持）是唯一活跃的开源实现；**TRON 侧无解**（TronVM 无 state-override 语义），只能 GoPlus API 或 TronGrid 模拟补。
6. **两个确认的空缺**：①USDT/USDC 冻结与黑名单事件追踪没有专门维护的开源工具（唯一实现是 crypttrace 内置的 freeze 模块）；②MEV/三明治检测全线停更（flashbots/mev-inspect-py 已 archive），只剩 5 天大的 SandwichTrace。
7. **反刷量判据得到第二次验证**：本轮又抓到 4 个星标冲量仓库（interchange 240★/1 天、Crypto-Whale-Tracker 180★/**Auto commit 模板与主页 3.8 完全同款**、wallet-security-checker 112★/2 commits、spout 166★/7 commits）。三条判据（单贡献者/模板化提交/star 与活动脱节）有效，建议写入常规调研流程。
8. **中文安全厂商开源以审计框架与教育材料为主**（慢雾：路线图 927★、MCP 清单 834★、Agent 安全框架 560★），**AML/资金追踪工具全部闭源**（MistTrack 等）；可借的是方法论清单，不是代码。
9. **可视化升级路径新增两站**：`vasturiano/3d-force-graph`（MIT，6,580★，汇报用 3D）与 `pygraphistry`（BSD-3，GPU，13 周 1,452 提交）。
10. **Travel Rule / VASP 开源整体停摆**（OpenVASP 组织最后实质提交 2023-05），交易所协查场景暂时只能人工对接。

## 扫描口径

::: warning 判定标准：与主页一致
沿用 [开源项目调研](./oss-projects) 的口径：**三条硬门槛**（近 12 个月实质提交 / 可运行部署文档 / 许可允许内部非商业使用）+ **两条一票否决**（archived / 无 LICENSE）+ **活跃度指标**（13 周提交数 / 贡献者 / 最新 release，与提交内容对照读）。另加本轮反复验证过的**反刷量三条**：贡献者仅 1 人、提交信息模板化（`Auto commit: <时间戳>`）、star 增长与 Issue/Release 活动脱节——占两条即降级"只读参考"或直接排除。star 只用于排序，不参与判定。
:::

- **与主页的关系**：主页的选型结论（推荐组合）本页不重述；本页只新增发现与修订建议（见文末）。判定用词：新项目达标注**主力候选**，经实测复核后才升"主力"进主页推荐组合。
- **核查方式**：GitHub API 逐仓核查（元数据 / participation / commits 内容 / 贡献者 / release / LICENSE 正文）；对重点项目浅克隆走读（只读不运行）。核查快照 2026-11-18 夜 — 11-19 晨，命令与主页「调研口径」一致。
- **覆盖边界**：GitHub 全量检索不等于行业全量——关键词污染（"tornado"命中 Python 框架）、中文项目对英文关键词不可见、闭源商业工具不在射程。本页的"空缺"结论均为"GitHub 检索范围内未找到"。
- **原始数据**：六类判定表与 JSON 索引、走读笔记存于调研工作区（工作区内 `oss-scan/`，已 gitignore，含克隆副本），仓库内只保留本页结论。

## 01. 数据采集 / ETL / 索引器 / 节点 / 浏览器

**结论**：本层最能打的是三个自托管索引框架——rindexer（Rust/YAML 无代码，任意 EVM 链，ClickHouse/Postgres 双后端）、graphprotocol/graph-node（subgraph 生态标准件，Apache-2.0）、subsquid/squid-sdk（唯一内置 TRON 原生摄取包的主流框架，可直接对接自建 java-tron 的 HTTP API），三者近 12 个月均为真实活跃、许可可用。TRON 研判链路建议：java-tron 自建节点 + squid-sdk tron 包做事件/转账摄取，ETH/BSC 用 rindexer 或 graph-node，对已有 ethereum-etl 体系形成互补而非替代。BTC 补链采用 Bitcoin Core + electrs + mempool（AGPL-3.0，内部非商业可用）组合，是当前最活跃的自托管浏览器方案。排除项：enviodev/hyperindex 已改为 SaaS EULA（无开源许可，一票否决）、thirdweb-dev/insight 已归档、HemeraProtocol/hemera-indexer 停更超 13 个月。

| 项目 | 定位 | 栈 / 许可 | star | 最后提交 | 13周提交 | 判定 |
|---|---|---|---|---|---|---|
| joshstevens19/rindexer | Rust 无代码 EVM 事件索引器，YAML 配置，Postgres/ClickHouse/CSV + GraphQL | Rust / MIT | 763 | 2026-11-17 | 32 | 主力候选 |
| graphprotocol/graph-node | subgraph 生态标准索引器，GraphQL 服务层 | Rust / Apache-2.0+MIT | 3168 | 2026-11-18 | 6 | 主力候选 |
| subsquid/squid-sdk | 多链 ETL 工具集，唯一内置 TRON 摄取（tron-data/processor，接 java-tron HTTP API） | TS / Apache-2.0（tron/evm 包 GPL-3.0+） | 1347 | 2026-11-18 | 84 | 主力候选 |
| mempool/mempool | BTC/Liquid 自托管浏览器（浏览器+API 层） | TS/Angular / AGPL-3.0 | 2899 | 2026-11-18 | 455 | 主力候选 |
| romanz/electrs | BTC Electrum 服务器（地址索引，mempool 依赖） | Rust / MIT | 1413 | 2026-11-10 | 15 | 主力候选 |
| subsquid/pipes-sdk | SQD 流式管道 SDK，Tron/Bitcoin 解码，落 Postgres/ClickHouse/Parquet | TS / Apache-2.0 | 24 | 2026-11-17 | 104 | 备选 |
| dipdup-io/dipdup | Python 多链选择性索引框架（Tezos 起家，已支持 EVM） | Python / MIT | 274 | 2026-11-14 | 34 | 备选 |
| yearn/kong | yearn 内部实时/历史 EVM 索引+分析 | TS / MIT | 22 | 2026-11-18 | 61 | 观察 |
| eabz/evm-indexer | 轻量 SQL EVM 索引器 | Go / MIT | 93 | 2026-09-21 | 1 | 观察 |
| chaindexing/chaindexing-rs | Rust EVM 索引器，SQL 查询 | Rust / Apache-2.0 | 58 | 2026-05-30 | 0 | 观察 |
| indexsupply/golden-axe | 轻量 evm 索引器 | Go / MIT | 116 | 2026-07-04 | 0 | 观察 |
| Gingerbreadfork/tron-goblin-node | Rust 从零实现的 TRON 全节点（第二客户端，带地址历史索引） | Rust / LGPL-3.0 | 9 | 2026-10-01 | 26 | 观察 |
| janoside/btc-rpc-explorer | 经典 BTC 自托管浏览器 | Node / MIT | 1795 | 2026-02-11 | 0 | 观察 |
| vicnaum/shinode | 轻量 ETH 历史节点（P2P 同步 headers/receipts/logs，~6h） | Go / Apache-2.0 | 66 | 2026-03-11 | 0 | 参考 |
| bit2swaz/shadow-index | Reth ExEx→ClickHouse 超低延迟索引（4ms） | Rust / MIT | 7 | 2026-02-17 | 0 | 参考 |
| tronprotocol/tronweb | TRON JS SDK（对接 java-tron HTTP 的取数客户端） | TS / MIT | 578 | 2026-11-11 | — | 参考 |
| matter-labs/block-explorer | zkSync Era 自托管浏览器（非重点链） | TS / Apache-2.0 | 138 | 2026-11-18 | 22 | 参考 |
| enviodev/hyperindex | 前多链索引器 Envio | Rust / **EULA（无开源许可）** | 573 | 2026-11-18 | 137 | 排除 |
| HemeraProtocol/hemera-indexer | EVM 索引器 | Python / Apache-2.0 | 141 | 2025-10-22 | 0 | 排除 |
| thirdweb-dev/insight | EVM 索引器 | TS / Apache-2.0 | 69 | 2026-05-19（**archived**） | 0 | 排除 |

### 深入分析（浅克隆走读）

**joshstevens19/rindexer**（oss-scan/repos/joshstevens19__rindexer）
- 结构：Rust workspace（cli/core/graphql/providers/xtask）+ e2e-tests + examples + documentation + helm；Dockerfile 与 docker-compose 齐备，镜像 ghcr.io/joshstevens19/rindexer。
- 部署：docker-compose 单容器 + DATABASE_URL（Postgres）；或安装脚本原生运行；K8s 有 helm chart。2026-11-15 发布 v1.0.0。
- 配置模型：rindexer.yaml 定义 networks（任意 chain_id+rpc）与合约事件/工厂/phantom 事件；examples 含 native_transfers、erc20_balances/allowances、dex_pool、clickhouse_factory_indexing 等，正对资金流研判所需数据形态。
- 链支持：任意 EVM（ETH/BSC 直接可用，只需填 RPC）；TRON 不支持（非 EVM 交易模型）。
- 存储：Postgres 或 ClickHouse（与团队 ClickHouse 选型一致），另支持 CSV；开箱 GraphQL API。
- 可借：无代码 YAML 起步 + rust codegen 进阶；native_transfers 示例可直接改造为 ETH/BSC 转账底表。
- 风险：主开发者 Josh Stevens 单人主导（46 contributors 但核心集中）；Windows 原生二进制不含 reth-ExEx 模式（Docker/Linux 无碍）。

**subsquid/squid-sdk**（oss-scan/repos/subsquid__squid-sdk）
- 结构：monorepo：evm/ solana/ substrate/ **tron/**（tron-data、tron-data-service、tron-dump、tron-ingest、tron-normalization、tron-processor）bitcoin/ hyperliquid/ starknet/ fuel/ + processor/typeorm/graphql 公共层。
- TRON 支持（关键）：tron-data 直接读 java-tron 的 HTTP API（getBlock/getNowBlock，`httpApi` 参数），即可对接自建全节点，非强制依赖 SQD Network 网关；tron-ingest 提供独立 bin。
- 许可注意：顶层 LICENSE 为 Apache-2.0，但 tron-processor/tron-data/evm-processor 等核心包 package.json 标 **GPL-3.0-or-later**——内部非商业使用合法，若改造后对外分发需开源。
- 链支持：TRON 原生 + 任意 EVM（BSC 可）；EVM 侧通常走 SQD Portal 或自建网关获得高速回填。
- 可借：TRON 摄取管线（区块/交易/内部交易/事件解码）是同类唯一开源实现，可作 TRON 研判数据底座。
- 风险：tron 包版本 0.1.x，成熟度低于 EVM 包；TypeScript 技术栈需团队适配；GPL 传染边界要审计。

**graphprotocol/graph-node**（oss-scan/repos/graphprotocol__graph-node）
- 结构：Rust workspace：chain/（链适配）core/ graph/ graphql/ node/ runtime/（WASM 映射执行）server/ store/ gnd/；docker/ 提供 docker-compose 与 build 脚本。
- 部署：标准三件套 graph-node + Postgres + IPFS + 归档 RPC；文档完整（docker/README.md）。
- 链支持：任意 EVM 类链（BSC 可直接配 RPC）；TRON 无适配。
- 活跃度：yr=647 提交、100+ 贡献者，但 wk13=6 处于平台期，最新 release v0.45.0（2026-08-03），节奏稳定。
- 可借：成熟的 GraphQL 数据服务与 subgraph 工具链（graph-cli/graph-ts），若团队想统一"索引即映射"模型可用它承载 ETH/BSC 合约事件。
- 风险：部署重（需归档节点 + IPFS + Postgres）；映射用 AssemblyScript，团队学习成本；项目重心在 The Graph 去中心网络，自托管场景属二等公民。

**mempool/mempool**（oss-scan/repos/mempool__mempool）
- 结构：backend（Node/TS，api/explorer/货币与费率等模块）+ frontend（Angular）+ rust/ + docker/（compose、mysql、init 脚本）。
- 部署：docker-compose 仅容器化前后端，需外置 Bitcoin Core（txindex=1）+ electrs（地址索引需 Electrum Server）+ MySQL；官方文档有配置样例。
- 许可：AGPL-3.0-or-later + 商标限制（Mempool Open Source Project®）；内部部署不对外提供服务则无义务开源。
- 活跃度：wk13=455、yr=1495、79 贡献者、v3.3.2（2026-10-23），本类最活跃项目。
- 可借：BTC 研判链的浏览器与 API 层完整参考实现；其 backend api 层（地址/交易/区块查询）可复用为内部 BTC 数据接口。
- 风险：BTC 专属，与 TRON/ETH 无交集；依赖链（bitcoind+electrs+mysql）运维成本不低。

### 全节点客户端一行评估（基础设施，按需部署官方发行版）
- ethereum/go-ethereum：LGPL-3.0，wk13=248，执行层事实标准，TRON/ETH 链路必备归档节点，引入=直接部署。
- paradigmxyz/reth：Apache-2.0，wk13=966，性能最强的 ETH 执行客户端，rindexer ExEx 模式宿主，推荐与 rindexer 配套。
- bnb-chain/bsc：LGPL-3.0，wk13=33，BSC 官方 go-ethereum fork，BSC 研判必备；许可 LGPL 需注意动态链接边界。
- NethermindEth/nethermind：GPL-3.0，wk13=2345，.NET 执行客户端，可选。
- besu-eth/besu（原 hyperledger/besu）：Apache-2.0，wk13=575，Java 企业级客户端，可选。
- bitcoin/bitcoin：MIT，wk13=1073，BTC 研判必备（txindex=1）。
- btcsuite/btcd：ISC，wk13=78，Go 实现 BTC 全节点，适合嵌入式采集端。

### 本类要点
- 【事实｜GitHub API 核查，2026-11-19】rindexer v1.0.0（2026-11-15）MIT，wk13=32，46 贡献者；squid-sdk wk13=84 且 tron/ 子包近 13 周持续提交（common/changes 有 2026-11-10 记录）；mempool wk13=455 全类最高。
- 【事实｜仓库走读，2026-11-19】squid-sdk 的 TRON 摄取读 java-tron HTTP API（tron-data/src/data-source.ts），自建节点即可，不强制依赖 SQD 网络；但 tron/evm 核心包许可为 GPL-3.0-or-later 而非顶层 Apache-2.0。
- 【事实｜licenses/LICENSE.md】enviodev/hyperindex 于近期改为 Standard SaaS EULA（禁止修改/复制/衍生），搜索 API 显示 license=NONE，一票否决。
- 【事实｜thirdweb-dev/insight repo】archived=true，一票否决；HemeraProtocol/hemera-indexer 最后实质提交 2025-10-22，超 12 个月。
- 【推断｜置信度：高】TRON 链路最优组合为"java-tron（已有覆盖）+ squid-sdk tron 包摄取 + ClickHouse 存储"；rindexer/graph-node 覆盖 ETH/BSC 侧，三者许可均允许内部非商业使用。
- 【推断｜置信度：中】graph-node wk13=6 说明其自托管场景进入维护平台期，新引入的边际收益低于 rindexer；但生态（subgraph mappings 复用）仍有价值。
- 【待验证】squid-sdk tron 包对 TRC20 transfer 事件与内部交易（internal tx）的解码覆盖度（需起真节点实测）；Gingerbreadfork/tron-goblin-node 与 java-tron 的共识一致性（仅 1 名贡献者，不建议生产引入，仅观察）。
- 【待验证】rindexer 在 BSC 高频出块（3s）下的回填吞吐与 reorg 处理，需在自有 RPC 上压测。

### 落选与去重说明
- enviodev/hyperindex（573★）：高星且极活跃（wk13=137），但整仓改为 SaaS EULA、无开源许可证 → 一票否决（许可）。
- HemeraProtocol/hemera-indexer（141★）：最后提交 2025-10-22，超 12 个月 → 排除（停更）。
- thirdweb-dev/insight（69★）：已 archived → 一票否决。
- eabz/evm-indexer（93★）/ chaindexing-rs（58★）/ golden-axe（116★）：有部署文档与可用许可，但近 13 周实质提交 0~1，列为观察不推荐引入。
- janoside/btc-rpc-explorer（1795★）：2026-02 后无实质提交，被 mempool 方案替代 → 观察。
- yogh-io/bitcoin-transaction-explorer（184★）、team-exor/eiquidus（113★）：年提交 0~17，功能与 mempool/otterscan 重叠 → 参考，不进主表。
- matter-labs/block-explorer（138★）：活跃但仅支持 zkSync Era，非重点链 → 参考。
- 去重：blockchain-etl/ethereum-etl-airflow 属 ethereum-etl 生态（已覆盖），不重复分析；subsquid/squid-cli、squid-evm-templates 为 squid-sdk 配套脚手架，随 squid-sdk 一并评估；polygon/erigon、btcsuite/btcd 等节点与已覆盖 erigon 同类，仅一行评估；tri-parity 类 BTC ETL fork 与 bitcoin-etl 同源，去重不展开。

## 02. 地址聚类 / 实体标签 / 数据集 / 制裁与合规筛查

**结论**：主页结论全部维持并被强化——①聚类层 `bitiodine` 仍是唯一"能跑、许可干净、还在动"的实现，本轮扫到的其余聚类仓库要么是 2019-2024 的学术课程作业残片、要么无 LICENSE；账户模型链（TRON/ETH）聚类依旧没有成套开源实现。②标签/数据集层没有新的可用供给：新发现的 ImMike 标签库是一次性 dump（创建与推送同日、1 贡献者），无维护承诺。③制裁筛查层 watchman 仍然没有对手：唯一新候选 SpiderAml 无 LICENSE 直接否决。④**Travel Rule / VASP 协议的开源实现整体停摆**（OpenVASP 组织 4 仓库，最后实质提交 2023-05）——这一层对"交易所协查"场景有意义，但当前只能靠人工对接。

| 项目 | 定位 | 栈 / 许可 | star | 最后提交 | 13周提交 | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| [VincenzoImp/bitcoin-address-clustering](https://github.com/VincenzoImp/bitcoin-address-clustering) | 多启发式 BTC 聚类实现 | Python / MIT | 8 | 2026-07-22 | 0 | 观察：启发式清单可读（README 罗列了多条件实现），但近 52 周无实质提交，单人维护 |
| [ImMike/crypto-wallet-address-labels](https://github.com/ImMike/crypto-wallet-address-labels) | 地址标签库（BTC/ETH/SOL/BSC） | 数据集 / MIT | 5 | 2026-03-08 | 0 | 参考（数据）：一次性 dump，可用作冷启动语料，不可依赖更新 |
| [twgnr/Chainer](https://github.com/twgnr/Chainer) | 多链追踪 + taint 模型 + 证据日志 | TS / **无 License** | 10 | 2026-09-21 | 8 | 排除（代码）：无许可一票否决；但其 README 对 haircut/FIFO/poison 三种染色模型的描述值得当方法论文档读 |
| [0xBreak/SpiderAml](https://github.com/0xBreak/SpiderAml) | 免费 AML 筛查 | **无 License** | 3 | 2026-11-17 | — | 排除：无许可；制裁筛查层维持 watchman 唯一 |
| [semifredd0/Bach](https://github.com/semifredd0/Bach) | 多启发式 BTC 聚类 | Python / **无 License** | 3 | 2025-09-23 | 0 | 排除：无许可 |
| [ECNU-Cross-Innovation-Lab/BitcoinAddressClustering](https://github.com/ECNU-Cross-Innovation-Lab/BitcoinAddressClustering) | 聚类课程实现 | Python / GPL-3.0 | 9 | 2023-10-28 | 0 | 排除：停更三年 |
| [Antti-Kaikkonen/CoinClustering](https://github.com/Antti-Kaikkonen/CoinClustering) | 聚类实验 | Python / MIT | 7 | 2021-12-29 | 0 | 排除：停更五年 |
| [gbossi/BitcoinClusterAggregator](https://github.com/gbossi/BitcoinClusterAggregator) | 分布式聚类聚合 | Scala / GPL-3.0 | 10 | 2019-02-28 | 0 | 排除：停更七年 |
| [OpenVASP/](https://github.com/OpenVASP) 组织（4 仓库） | Travel Rule / VASP 协议 | Solidity 等 / MIT 为主 | — | 2023-05-07 | 0 | 排除：全线停摆，见要点 |

### 本类要点

- 【事实｜GitHub 检索，2026-11-19】"wallet clustering heuristic""exchange labels dataset""vasp compliance open source""chainalysis alternative"四组关键词在 GitHub 的有效命中几乎为零（大量无关污染结果）——商业链上分析公司（Chainalysis/Elliptic/MistTrack）的方向在开源侧没有等价物，主页"实体标签的执法级可信度是免费工具最大短板"的判断再次成立。
- 【事实｜OpenVASP 组织仓库元数据】Travel Rule 开源标准 OpenVASP：contracts 最后提交 2023-05、specification 2020-06、UI 明确标注 OUTDATED。TRP/TRITIUM 等替代协议无活跃开源实现命中。
- 【推断｜置信度：高】聚类层的主页结论（bitiodine + 方法可借 + 账户模型缺位）不需要修订；本类唯一的增量是确认**没有遗漏的活跃实现**——这是"负结论"，但对选型同样有价值。
- 【推断｜置信度：中高】标签库（ImMike 等）如果要用，只做**本地冷启动语料**：先人工抽检标注准确率，再决定是否并入自建标签库；永远不当实时依据。

### 落选与去重说明

- 聚类方向 12 个搜索命中里 8 个无 LICENSE——学术圈把 GitHub 当实验记录本的习惯没有变，许可纪律仍然缺失。
- Wallet-Risk-Scanner（916 star）已在主页 3.8 判定为刷量仓库，本轮再次出现在"sanctions screening crypto"首位，提醒我们 star 排序不可信。
- 深入分析省略：本类没有值得浅克隆走读的活跃候选（bitiodine 已在主页 3.6 走读过其定位）。

## 03. 混币检测 / CoinJoin 分析 / 跨链追踪 / 洗钱模式

**结论**：主页 oss-projects.md 3.9 的"三类场景均未找到可用开源实现"**被本轮部分推翻**——①混币取证：`prettydeath/TornadoCash-demixer`（MIT，8 条 EVM 链、56 个池子、证据分级 strong/moderate/weak、带安慰剂校准，2026-11-18 仍在提交）是第一个"方法学诚实、可直接装"的 Tornado 取证实现；②多链资金追踪：`bobslayerX/crypttrace`（MIT，PyPI 包，TRON/BTC/SOL/TON 免 Key，内置稳定币冻结状态直查、Gephi 图导出、PDF 证据包）直接对标"被盗资金追到哪里"场景；③跨链桥命名与绕链追踪、OTC/跑分商户识别**依然空缺**（240 star 的 interchange 实为落地页仓库）。两个主力候选都是单人维护、star 极低（1 / 31），属于"真金但没被看见"的类型——采用前必须自证复核。

| 项目 | 定位 | 栈 / 许可 | star | 最后提交 | 13周提交 | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| [prettydeath/TornadoCash-demixer](https://github.com/prettydeath/TornadoCash-demixer) | Tornado Cash 存取款关联取证 | Python / MIT | 1 | 2026-11-18 | 129 | **主力候选**：见深入分析 |
| [bobslayerX/crypttrace](https://github.com/bobslayerX/crypttrace) | 多链 OSINT 资金追踪 + 冻结检查 | Python / MIT | 31 | 2026-11-08 | 97 | **主力候选**：见深入分析 |
| [pcaversaccio/torn-detector](https://github.com/pcaversaccio/torn-detector) | "Tornado 资金部署的合约"检测 | Solidity 脚本 / WTFPL | 30 | 2026-11-17 | 18 | 参考：口径极窄（只答一个布尔问题），社区老人维护，稳定 |
| [crocs-muni/coinjoin-analysis](https://github.com/crocs-muni/coinjoin-analysis) | Wasabi/Whirlpool/JoinMarket 数据集分析 | Python / MIT | 5 | 2026-11-02 | 6 | 参考：马萨里克大学 CRoCS 实验室出品，学术级 CoinJoin 数据工具 |
| [Ziya-Sadr/Ashi-Whirlpool-Analysis](https://github.com/Ziya-Sadr/Ashi-Whirlpool-Analysis) | Whirlpool 匿名集统计 | Python / MIT | 4 | 2025-07-11 | 0 | 观察：停更一年 |
| [5h4d0wn1k/c5-blockchain](https://github.com/5h4d0wn1k/c5-blockchain) | 离线取证工具箱（解析/聚类/模式） | Python / MIT | 6 | 2026-09-22 | 6 | 观察：太新太小，功能与 crypttrace 重叠 |
| [xaynov-osint/txfetch](https://github.com/xaynov-osint/txfetch) | 按时间/金额/备注反查交易 | Python / MIT | 44 | 2026-05-31 | 0 | 观察：半年无提交，但"无哈希找交易"的定位独特（跑分对账场景可用） |
| [elliott-diy/LockBit-Wallet-Tracker](https://github.com/elliott-diy/LockBit-Wallet-Tracker) | LockBit 勒索地址数据 | 数据集 / **无 License** | 7 | 2025-09-05 | 0 | 排除：无许可；地址数据本身可从勒索通报交叉获得 |
| [mitchellkrogza/Badd-Boyz-Bitcoin-Scammers](https://github.com/mitchellkrogza/Badd-Boyz-Bitcoin-Scammers) | 勒索/色情敲诈 BTC 地址列表 | 数据集 / GPL-3.0 | 18 | 2021-07-04 | 0 | 排除：停更五年，数据陈旧 |
| [tabookhandawn/interchange-osint-cross-chain-tracing](https://github.com/tabookhandawn/interchange-osint-cross-chain-tracing) | "跨链追踪应用" | JS / MIT | 240 | 2026-11-13 | 8 | **排除**：落地页仓库，见落选说明 |
| [edycutjong/redstring](https://github.com/edycutjong/redstring) | 链上取证引擎 + 3D 可视化 | Python / MIT | 3 | 2026-08-15 | 0 | 排除：半年无提交且建立在商业 Nansen CLI 之上 |
| [rohteemie/Open-Source-Blockchain-Forensics](https://github.com/rohteemie/Open-Source-Blockchain-Forensics) | 实体聚类工具 | Python / MIT | 5 | 2026-05-05 | 0 | 排除：半年无提交，与 bitiodine/主页聚类层重复 |
| [Rupali-2507/MULE_HUNTER](https://github.com/Rupali-2507/MULE_HUNTER) | UPI 跑分账户 GNN 检测（非加密） | Python / 无 License | 12 | 2026-09-16 | — | crossref→04：方法参考（GNN 识别"钱骡"账户），代码不可用 |

### 深入分析（浅克隆走读）

**TornadoCash-demixer**（`oss-scan/repos/prettydeath__TornadoCash-demixer`，7.7MB）
- 【事实｜README + 仓库树】Python 包（PyPI：`tornado-demix`），带 CITATION.cff（Zenodo DOI）、mkdocs 文档站、`calibration/`、`tests/`、`webui/`、`docs/EVALUATION.md` 安慰剂检验。覆盖 **8 条 EVM 链上的 56 个注册池**（含 ETH 主网与 BSC 等）。
- 【事实｜README】启发式分三档：`strong` = 两个独立信号家族（72 小时内直接交易对手 + 早期多池画像匹配）；`moderate` = 单一 lead 信号；`weak` = 金额+时间、gas 价格复用等——**作者自证这些在真实存款人上与随机命中无异，只作上下文，永不提级**。评分输出标注"是线索不是证明"。
- 【事实｜README】还做：退出款分组（operator clusters）、交易所/服务商/4337 智能账户入金地址标注、提款后资金的多跳前向追踪。
- 【事实｜贡献者与提交】1 名维护者，提交信息为人写（"Release 2.23.1: re-run of hold-outs and placebo"），近 13 周 129 次提交全部发生在项目 8 周生命周期内——等于一个刚发布的新项目。
- 【推断｜置信度：中高】这是 DeMix（论文方向）的**可运行工程化实现**，方法学克制（明确排除 chance-level 信号）在开源取证工具里罕见。风险：单人维护、无第三方复现记录、star=1 意味着零社区检验；TRON 侧的混币（如 Justmix 类）**不在覆盖范围**，8 EVM 链=TRON 不在内。
- 【待验证】用一笔已知 Tornado 历史地址跑一遍，对照 Etherscan 人工结果；确认 BSC 链的池子注册表时效性。

**bobslayerX/crypttrace**（`oss-scan/repos/bobslayerX__crypttrace`，7.1MB）
- 【事实｜README + pyproject.toml】PyPI 包 `crypttrace[web]`：终端 + 本地 Flask Web UI（资金流图）+ fpdf2 生成 PDF 证据包。CI 有离线 selftest（免 Key 可跑）。
- 【事实｜src/crypttrace/fetchers/tron.py】TRON 走 TronGrid **免 Key**，处理 hex(41)→base58(T) 转换；docstring 直接点名 "pig butchering"（杀猪盘）USDT-TRC20 是其主要设计场景——与本组研判对象完全一致。
- 【事实｜src/crypttrace/freeze.py】**稳定币冻结检查**：不查第三方名单，直接调 USDT 的 `isBlackListed` / USDC 的 `isBlacklisted` / balanceOf（ETH 公共 RPC、TronGrid、Solana token account 三路），回答"这个地址上有多少 USDT/USDC、是否已被冻结、谁有权冻结"。
- 【事实｜仓库树】另有 `bridges.py`（跨链桥识别）、`drain.py`（钱包 drainer 相关）、`assess.py`（风险评分）、`export.py`（GEXF/Gephi 导出）、`cases/`（案例）。
- 【事实｜README】链覆盖：ETH/BSC/Polygon/Arbitrum/Optimism/Base 走 Etherscan API（**BSC/OPT/Base 免费档不支持，需付费档**——与链上组 tools.md 的"免费窗口塌陷"结论互相印证）；BTC/LTC/DOGE/TRON/SOL/TON 公共端点免 Key。
- 【事实｜贡献者与提交】1 名维护者（"Bob"），提交为真实开发信息（GEXF 布局细节、Gephi 使用提示），有 PR 合并（#39），近 13 周 97 次提交。
- 【推断｜置信度：中高】**这是本轮扫描对研判流水线价值最高的单项发现**：定位就是"受害者报案→给一个钱包→钱去了哪、在哪能拦住"，与政策组案例库的跑分/杀猪盘场景直接对齐。freeze.py 的"冻结可能性"检查甚至对冻结申请文书有用。风险：单人维护、实体标签来源需审计（README 称 labels 来自公开名单，具体口径未见文档）、EVM 多链受 Etherscan 免费档限制（恰好是 BSC 这个主战场）。
- 【待验证】TRC20 转账与内部合约调用的覆盖深度；实体标签数据源清单与更新频率；对已知案件的复现。

### 本类要点

- 【事实｜GitHub 检索，2026-11-19】"peel chain""smurfing detection""withdrawal correlation"等关键词在 GitHub 上仍然**零命中**（stars:>2）——分层拆分模式的检测依旧没有开源实现，主页 3.9 这部分维持。
- 【事实｜本轮克隆走读】跨链追踪方向出现的最高星项目 interchange（240 star）`lib/` 目录只有一个 122 行的 `bridges_name.js`，README 是带 SEO 关键词堆砌的产品落地页（"download for Windows"），应用本体闭源。
- 【推断｜置信度：高】3.9 的结论应改写为：**混币取证与多链资金追踪在 EVM/多链侧已出现可部署的开源实现（demixer、crypttrace，均单人维护需自证）；OTC/跑分识别与跨链桥自动化命名仍空缺；TRON 侧混币取证仍空缺**。
- 【推断｜置信度：中高】CoinJoin/UTXO 侧的学术工具（CRoCS 的 coinjoin-analysis）适合做"混币者画像"的离线研究，不适合接入实时流水线。
- 【待验证】两个主力候选的输出正确性需要用已知案例（如 Ronin 案、OFAC 已定罚地址）人工比对。

### 落选与去重说明

- interchange：240 star 但创建与最后推送同日（2026-11-13）、8 次提交、代码仅 1 个 JS 文件——**star 与活动完全脱节**，按主页 3.8 反刷量口径第二条+第三条命中，排除。
- LockBit/Scammers 地址列表类：数据集性质且无许可或停更，不作组件引入；数据本体在案件研判时可按需引用（注明出处）。
- redstring：依赖 Nansen CLI（商业产品），"开源"只是壳。
- MULE_HUNTER：UPI 场景（印度支付）非加密资产，但"图特征识别钱骡账户"的思路与检测模型页相关，转 04 类参考。

## 04. 风险评分 / 决策引擎 / ML 模型 / 黑名单

**结论**：GNN 侧没有"近 12 个月仍在演进、可直接吃 Elliptic++ 跑赢 SOTA"的活跃开源项目——官方实现 IBM/Multi-GNN（Apache-2.0）自 2024-02 起停更但仍是唯一的可运行基线（GIN/GAT/PNA/RGCN + eMLPs/Reverse-MP/ego/ports 四项适配），其训练数据是 IBM 合成 AML 数据集而非 Elliptic/Elliptic++，复现 Elliptic++ 仍需自己接数据管道； ethereum/BTC 欺诈检测论文复现仓（BERT4ETH 等）普遍无 LICENSE 或停更，只能作只读参考，检测模型页应以 Multi-GNN 为骨架自建 TRON/ETH 特征。黑名单里**可直接用**的是：phishdestroy/destroylist（205k+ 钓鱼/诈骗域名，MIT，日更，jsDelivr 单文件即取，仓库 76GB 勿全量克隆）、MetaMask/eth-phishing-detect（3.6MB 域名配置+Levenshtein 检测器，但许可是非标准 DBAD 需法务确认）、GoPlus API（honeypot/恶意地址/授权检测，免费额度+Apache-2.0 SDK）；地址级开源专项黑名单（尤其 wallet drainer）在本轮检索中为**空缺**，drainer 追踪仍以商业源和 scamsniffer（已覆盖）为主。honeypot 检测器可信度：malvaphe/Crypto_Honeypot_Detector v2 用 eth_call state-override + eth_simulateV1 双模拟、覆盖 BSC PancakeSwap V2/V3，工程可信（自建 anvil 反例测试床），但作者自述无法防"买入后改税/拉黑"类后手，且仅 EVM 不支持 TRON——TRC20 侧仍需 TronGrid 模拟或 GoPlus。评分引擎侧未见加密原生开源成熟品，gorules/zen 可作评分规则编排层。

| 项目 | 定位 | 栈 / 许可 | star | 最后提交 | 13周提交 | 判定 |
|---|---|---|---|---|---|---|
| phishdestroy/destroylist | 钓鱼/诈骗域名黑名单 feed（205k+，hosts/adblock/RPZ/免费 API） | 数据 feed / MIT | 2068 | 2026-11-18 | 12069（bot 日更） | 主力候选 |
| malvaphe/Crypto_Honeypot_Detector | EVM honeypot 检测（BSC/ETH 等 9 链，买卖/转账三模拟） | Node22+TS / MIT | 68 | 2026-09-28 | 6 | 主力候选 |
| GoPlusSecurity/goplus-sdk-python | GoPlus 官方 SDK：honeypot/恶意地址/授权检测 API | Python / Apache-2.0 | 13 | 2026-08-21 | 2 | 主力候选 |
| MetaMask/eth-phishing-detect | Web3 钓鱼域名检测库+3.6MB 名单（Levenshtein 容差匹配） | TS / DBAD(非标准) | 1350 | 2026-11-18 | 23681（bot 日更） | 备选 |
| bobslayerX/crypttrace | 多链 OSINT 研判：TRON/ETH/BSC 地址风险评分+资金流图+证据包 | Python3.10 / MIT | 31 | 2026-11-08 | 97 | 备选 |
| gorules/zen | 通用决策/规则引擎（Rust 内核+JS/Go/Python 绑定，可嵌评分规则） | Rust+JS / MIT | 2141 | 2026-11-17 | 47（release 2026-11-11） | 备选 |
| polkadot-js/phishing | Polkadot/Substrate 系钓鱼域名名单+JS 工具 | JS / Apache-2.0 | 207 | 2026-09-23 | 2 | 备选 |
| IBM/Multi-GNN | Multi-GNN 官方实现（AAAI'24/NeurIPS'23，GIN/GAT/PNA/RGCN） | PyTorch+PyG / Apache-2.0 | 129 | 2024-02-13（默认分支） | 0 | 参考 |
| phishdestroy/ScamIntelLogs | 诈骗操作 OSINT 证据档案（TG 聊天记录/面板/交易 IoC） | 数据档案 / MIT | 409 | 2026-10-28 | 6 | 参考 |
| phishfort/phishfort-lists | 钓鱼名单（2025-05 起弃用 GitHub 列表，转 lookup.phishfort.com API） | 数据 / GPL-3.0 | 105 | 2026-03-27 | 0 | 观察 |
| JouninGlide65/assay-osint-crypto-aml-check | 地址信誉评分 Windows 应用（源码仅 36 文件，二进制外部分发） | Python 片段 / MIT | 262 | 2026-11-13 | 8 | 观察 |
| stenion-lab/stenion | Stellar/Soroban DeFi 持续风险评分（可审计） | / MIT | 16 | 2026-10-07 | 147 | 观察 |
| neatlabs-ai/crucible-sigint | 诈骗基础设施 OSINT 指纹引擎（scam-kit 复刻，域名层） | / MIT | 27 | 2026-05-25 | - | 观察 |
| forta-network/forta-bot-sdk | 链上检测 bot SDK（欺诈/攻击检测网络） | TS / MIT | 71 | 2024-01-24 | 0 | 排除 |
| Bayi-Hu/BERT4ETH_PyTorch | BERT4ETH（以太坊欺诈检测预训练 Transformer）复现 | Python / 无LICENSE | 59 | 2025-09-18 | 0 | 排除 |
| jiyuanwang-afk/Explainable-AI-in-Financial-Fraud-and-Anomaly-Detection | 图欺诈检测+XAI（内容仓） | Notebook / 无LICENSE | 788 | 2025-10-20 | 0 | 排除 |
| brebros/chainsleuth | AI rug pull 检测（贴合约出结论） | / 无LICENSE | 20 | 2026-06-24 | - | 排除 |
| KeithTheDev/rugpulldetector | Pump.fun 实时 rug pull 检测（C++/Python 绑定） | C++ / 无LICENSE | 12 | 2025-02-10 | - | 排除 |
| linovives/bitcoin-fraud-gnn | Elliptic 数据集 GCN/GAT 时空切分复现 | Python / 无LICENSE | 4 | 2026-04-22 | - | 排除 |

### 深入分析（浅克隆走读）

**IBM/Multi-GNN**（oss-scan/repos/IBM__Multi-GNN）
- 结构：单层平铺 14 个 Python 文件——models.py（GIN/GAT/PNA/RGCN 四类 + eMLPs/reverse-MP/ego-ids/port-numbering 适配，即论文全部创新点）、data_loading/data_util（把 Kaggle 的 IBM-AML 合成交易 CSV 转成 PyG 异质有向多重图）、main.py/training/inference（训练/微调/推理一条龙）、data_config.json+model_settings.json 配置化。
- 部署：conda env.yml（python3.9+torch+CUDA11.8+pyg）→ `format_kaggle_files.py` 预处理 → `python main.py --data Small_HI --model gin --emlps --reverse_mp --ego --ports`。文档可跑，步骤清晰。
- TRON/BSC：无任何链上接入，数据依赖 Kaggle IBM 合成 AML 数据集（非 Elliptic/Elliptic++）。
- 可借：模型与消息传递适配代码可直接搬到我们的 TRON/ETH/BSC 交易图上；数据加载层改造后即可吃 Elliptic++ 或自建图。
- 不可借：无线上推理服务化，无增量训练。
- 风险：默认分支最后实提交 2024-02（README 提到 reverse MP bug 修复后请 re-fork）；依赖版本偏旧（pandas 2.0.3/sklearn 1.3），需重建环境。判定"参考"：作为检测模型页的复现骨架与基线，不作为部署件。

**malvaphe/Crypto_Honeypot_Detector**（oss-scan/repos/malvaphe__Crypto_Honeypot_Detector）
- 结构：npm monorepo 三包——packages/core（检测引擎库+CLI）、packages/server（REST API，可挂 webapp）、packages/webapp（React+Vite）；contracts/HoneypotSimulator.sol 源码在库、编译产物 prebuilt 进 core（免 solc）。
- 原理：v2 无需部署合约——用 `eth_call` state-override 注入模拟器合约做单次买/卖/转账模拟，另用 `eth_simulateV1` 走"普通钱包 approve+卖"路径，专治"只骗模拟器"的蜜罐（gasprice==0 才放行、白名单地址、过期授权等）；链上自动找流动性最深池（Uniswap V2/V3 系）。
- 部署：Node22+`npm install`→`npm run demo`（anvil 本地链+真实 Uni 合约+示例蜜罐代币，即开即用）；CLI `npm run check -- <token> --chain bsc`；Docker 单容器 `docker run -p 8080:8080 -e RPC_URL_BSC=...`；退出码 0/1/2 便于脚本化。
- TRON/BSC：BSC 一等支持（PancakeSwap V2 router 0x10ED43C7...、V3 factory 0x0BFbCF9f...、公共 RPC 内置）；ETH/Base/Arbitrum/Polygon/Avalanche/OP/Gnosis/Fantom 共 9 链；**不支持 TRON**（TronVM 无 eth_call state-override 语义）。
- 可借：整个 core 可直接作为我们 BSC/ETH 代币预筛服务的检测内核（库+API 双形态，缓存/限流/ CORS 已配）；反例测试床思路可复用。
- 不可借：TRC20 侧无解；-owner 类后手风险（作者自述：模拟只反映当下状态）。
- 风险：单维护者（Nicolò Sartor），68★，人力总线因子 1；无 GitHub release（以 commit 版本走）。判定"主力候选"——本类目前唯一活跃、工程质量高的开源 honeypot 检测器。

**MetaMask/eth-phishing-detect**（oss-scan/repos/MetaMask__eth-phishing-detect）
- 结构：TS 小库——src/config.json（3.6MB：version/tolerance=1/fuzzylist/whitelist/blacklist，域名级名单）+ detector.ts（前缀/后缀/Levenshtein 容差匹配）+ update-config.ts；由 bot 持续合入 PhishFort 等来源（13 周 23681 次提交均为 feed 更新，≥100 贡献者）。
- 部署：npm 包直接 `import checkForPhishing(domain)`，或把 config.json 当纯数据源自研匹配器；无服务端组件。
- TRON/BSC：链无关（域名层），web3 钓鱼域名通用，含大量 BSC/DEX 假站。
- 可借：名单数据+匹配算法可直接进我们的网址筛查环节（研判入口第一道闸）；与 destroylist（hosts 格式、更大而杂）互补：MetaMask 名单精度高、destroylist 覆盖广。
- 不可借：无地址级数据；无 API 服务。
- 风险：**许可是 "DON'T BE A DICK" v1.2（DBAD），非 OSI 标准**——内部非商业使用实质可行（保留出处、不整套复售），但需在法务上确认后再进生产；feed 由 bot 驱动，star/提交数不反映人工维护量。判定"备选"。

**bobslayerX/crypttrace**（oss-scan/repos/bobslayerX__crypttrace）
- 结构：Python 包 crypttrace/——chains.py（EVM+btc/ltc/doge/**tron**/sol/ton 八类链）、fetchers/（etherscan/trongrid/bitcoin/ton 等）、labels/（实体标签：直接复用 scamsniffer/scam-database 与 0xB10C OFAC 名单）、freeze.py（抓 Tether/Circle 法务页构建 USDT/USDC 冻结黑名单，TronGrid 校验）、assess.py（风险信号→加权评分→置信度声明，含"固定手续费指纹"等 sweeper 检测）、gascluster.py、poisoning.py（地址投毒检测）、web/（本地资金流图 UI）、pdf.py/evidence.py（证据包）。
- 部署：`pipx install "crypttrace[web]"`；EVM 需免费 Etherscan key（BSC/OP/Base 需付费档）；BTC/LTC/DOGE/TRON/SOL/TON 走公共端点免 key；`python selftest.py` 离线自检。
- TRON/BSC：TRON 原生支持（TronGrid+TronScan 链接生成，USDT 冻结名单校验）；ETH 完整；BSC 可用但受 Etherscan 免费档限制。
- 可借：assess.py 的"信号-含义-置信度-权重"评估框架和 freeze.py 的冻结地址抓取思路很契合我们研判流水线；标签层与我们已覆盖源一致，可互换。
- 不可借：无 GNN/ML 模型；风险分是启发式规则而非学习模型。
- 风险：**单维护者、建仓仅 4 个月（2026-07）**，31★，尚无第三方使用痕迹；API 依赖（Etherscan 付费档/BlockCypher 限流）需自备。判定"备选"，建议先只读借鉴 assess/freeze 模块。

**phishdestroy/destroylist**（API 走读，仓库 76GB 未克隆）
- 结构：数据 feed 仓——rootlist/formats/primary_active/hosts.txt 为主 feed（jsDelivr CDN 分发），另有 adblock/dnsmasq/unbound/rpz 与 content-verified（内容核实）分层、community 层、count.json 统计端点；github-actions 每 5 分钟 reconcile+processed 更新（13 周 1.2 万次提交几乎全为 bot，5 名人工贡献者提交"Add scans for 日期"类实质记录）。
- 部署：无需部署——Pi-hole/AdGuard 一键订阅或 jsDelivr/raw 拉单文件；另有免费威胁情报 API（域名查询）。
- TRON/BSC：链无关（域名层），含大量加密钓鱼/假交易所/钱包授权骗站。
- 可借：作为网址黑名单主源（205k+、日更、MIT、免费）；与 MetaMask 名单、GoPlus dApp 黑名单三方交叉提升精度。
- 不可借：不是地址级黑名单；无评分。
- 风险：feed 由单组织（PhishDestroy，附 TG bot 举报渠道+申诉流程）维护，误报申诉依赖其流程；仓库体积巨大**严禁全量 clone**；ScamIntelLogs 同源档案含受害者记录，复用注意隐私合规。

### 本类要点
- 【事实｜IBM/Multi-GNN README+commits，2026-11-19】Multi-GNN 是 Egressy et al.（AAAI 2024）与 AMLSim 合成数据论文（NeurIPS 2023）的官方实现，Apache-2.0，含 GIN/GAT/PNA/RGCN+四项适配；默认分支最后实质提交 2024-02-13，13 周提交 0。
- 【事实｜Multi-GNN README，2026-11-19】其训练数据是 Kaggle 的 IBM 合成 AML 交易（HI-Small_Trans 等），不是 Elliptic/Elliptic++；Elliptic++ 官方实现（EllipticPlusPlus）已在主页覆盖。
- 【事实｜malvaphe README+chains.js，2026-11-19】Crypto_Honeypot_Detector v2 用 eth_call state-override+eth_simulateV1 双路径模拟，9 条 EVM 链（含 BSC PancakeSwap V2/V3 内置地址），CLI/REST/Docker 三形态，docs/SECURITY_REVIEW.md 有安全评审。
- 【事实｜MetaMask 仓 LICENSE+config.json，2026-11-19】eth-phishing-detect 许可为 DBAD v1.2 非标准许可；名单为 3.6MB config.json（tolerance=1 的编辑距离匹配）。
- 【事实｜phishdestroy README+participation，2026-11-19】destroylist 205k+ 域名、MIT、bot 每 5 分钟日更、仓库 76GB；phishfort/phishfort-lists 已公告 2025-05-01 起弃用 GitHub 列表转 lookup.phishfort.com。
- 【事实｜crypttrace labels/freeze.py，2026-11-19】crypttrace 直接引用 scamsniffer/scam-database 与 0xB10C/OFAC 名单，并从 Tether/Circle 法务页抓 USDT/USDC 冻结地址（TronGrid 校验），TRON 走 TronGrid 免 key。
- 【事实｜GoPlus SDK+docs，2026-11-19】GoPlusSecurity/goplus-sdk-python 为官方 SDK（Apache-2.0），检测能力（honeypot/malicious-address/approval/nft/dapp）在 gopluslabs.io 商业 API，免费额度制。
- 【推断｜置信度：高】2024-2026 活跃的 wallet drainer 追踪与黑名单在开源侧是空缺：检索 "wallet drainer/drainer tracker/blocklist" 命中的多为攻击工具本身（dawsbot/drain、devrox911/wallet-drainer-solana 等无 LICENSE 攻击件）或样本库（thegiver86/malware-drainer-samples，无 LICENSE）；可用替代是 destroylist（域名）+ scamsniffer（已覆盖，地址/签名）+ GoPlus malicious-address API。
- 【推断｜置信度：中】以太坊欺诈检测的学术复现仓（BERT4ETH_PyTorch、AntiMoneyLaunderingDetectionWithGNN 等）全部无 LICENSE 或停更，说明该方向开源工程化未形成，检测模型页应立足 Multi-GNN+自有数据自建，而非等待上游。
- 【推断｜置信度：中】jiyuanwang-afk/Explainable-AI（788★）建仓与最后提交同日（2025-10-20）、单贡献者、无 LICENSE——典型"星数与实质维护脱节"仓，符合反刷量降级判据；JouninGlide65/assay（262★，建仓 6 天）1 贡献者+二进制在外部分发，同列观察。
- 【待验证】GoPlus 免费额度对我们日均调用量是否够用（honeypot/地址筛查批量跑）；destroylist 的误报率与申诉时效（需抽样对比 MetaMask 名单）；crypttrace 的 BSC 免费档实际可用度。
- 【待验证】TRON 侧 honeypot/买卖税检测无开源等价物（TronVM 无 state-override），是否用 GoPlus tron 端点补齐需实测。

### 落选与去重说明
- **forta-network/forta-bot-sdk**（71★，MIT）：链上检测 bot 生态旗舰，但 SDK 最后提交 2024-01，forta-node 2024-08，整网转向商业运营，硬门槛①不过 → 排除。
- **Bayi-Hu/BERT4ETH_PyTorch**（59★）：BERT4ETH 官方复现，但无 LICENSE（一票否决）且 13 周提交 0 → 排除；论文本身可作为特征思路引用。
- **jiyuanwang-afk/Explainable-AI-in-Financial-Fraud-and-Anomaly-Detection**（788★）：无 LICENSE、仓库存活一天即停更、星数与维护严重脱节 → 排除（反刷量典型反例）。
- **issacchan26/AntiMoneyLaunderingDetectionWithGNN**（74★）、**simonemarasi/aml-elliptic-gnn**（18★）、**subrata-samanta/Langgraph_AML_Detection**（11★）、**linovives/bitcoin-fraud-gnn**（4★）：均为 Elliptic/AML 的课程级复现，无 LICENSE+停更 → 排除。
- **brebros/chainsleuth**（20★）、**KeithTheDev/rugpulldetector**（12★）：rug pull 检测器，无 LICENSE（后者另停更）→ 排除；rug pull 场景由 GoPlus token-security 与 honeypot 检测器覆盖。
- **dawsbot/drain**（282★）、**otsybizov/evm-wallet-sweeper**、**jembarns/Rescue-Wallet-...** 等：是"清仓/盗币攻击件"而非检测/黑名单，无 LICENSE → 不纳入本类（仅作威胁样本背景）。
- **referefref/honeydet**（116★）、**Dexel-Software-Solutions/Honeypot-detector**（13★）：网络层蜜罐检测（端口/banner），与加密蜜罐代币检测同名不同物 → 去重排除，不进本类。
- **gl0bal01/chainmap**（6★，MIT）：客户端 EVM 资金流图浏览器 → 属可视化/调查类，crossref，不进本类。
- **ChainGPT-org/chaingpt-claude-skill**（7★，MIT）：154 个 Web3 MCP 工具封装（含诈骗检测）——本质是商业 API 的 agent 封装 → crossref，不重复分析。
- **awelist/awesome-crypto-compliance**、**CryptoToolsDirectory/Awesome-Crypto-Tools-Directory**：目录型 awesome list（无 LICENSE/NOASSERTION）→ 仅作索引参考，不进表。
- **stenion-lab/stenion**（16★，MIT，wk13 147）：Stellar/Soroban 专用风险评分，非重点链 → 观察。
- 去重：marble、Wallet-Risk-Scanner（主页已判刷量反例）、scamsniffer/scam-database、0xB10C/OFAC、opensanctions、EllipticPlusPlus、IBM/AMLSim、sieve-aml、altscan 均已在主页/前类覆盖，本轮未重复分析；crypttrace 的标签层与 scamsniffer/0xB10C 重叠，属于"同一数据源的再次利用"而非重复项目。

## 05. 可视化补充 / 交易解码 / OSINT 取证 / 中文安全厂商开源

**结论**：①可视化层主页结论（Cytoscape.js 主力）不变，但**升级路径应加上 `vasturiano/3d-force-graph`（MIT，6,580 star）与 `pygraphistry`（BSD-3，GPU）**——前者补"3D 汇报演示"场景，后者是 Networkit/cosmos.gl 之外的另一条 GPU 路线（活跃度 13 周 1,452 提交，罕见）。②解码层 evm-trace 之外补充 `kigawas/web3-input-decoder`（MIT、离线、零依赖思路）与 `3loop/loop-decoder`（GPL，人话格式化做得最好，但 GPL 要隔离使用）。③通用 OSINT 工具箱 SkyFall 内置区块链分析模块 + 关系图，可作辅助。④**中文安全厂商（慢雾/Beosin）开源以安全审计框架与教育材料为主，AML/追踪取证工具全部闭源**（MistTrack 等）——想借力国内厂商，只能读他们的公开报告与方法论，不能用他们的代码。

| 项目 | 定位 | 栈 / 许可 | star | 最后提交 | 13周提交 | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| [vasturiano/3d-force-graph](https://github.com/vasturiano/3d-force-graph) | ThreeJS/WebGL 3D 力导向图 | JS / MIT | 6,580 | 2026-11-05 | — | **备选**：汇报演示场景的 3D 资金图渲染，接 Cytoscape 数据结构成本不高 |
| [graphistry/pygraphistry](https://github.com/graphistry/pygraphistry) | GPU 图可视化分析（Python 客户端） | Python / BSD-3 | 2,582 | 2026-11-18 | 1,452 | **备选**：十万级图分析，注意其服务器端有免费额度限制（SaaS/自托管 docker 双形态） |
| [kigawas/web3-input-decoder](https://github.com/kigawas/web3-input-decoder) | 离线 EVM 交易输入解码 | Python / MIT | 52 | 2026-03-01 | 0 | 观察：纯离线、无第三方 ABI 依赖，适合做证据固定时的本地解码 |
| [3loop/loop-decoder](https://github.com/3loop/loop-decoder) | EVM 交易转人话格式 | TS / GPL-3.0 | 97 | 2026-08-31 | 1 | 观察：输出最友好；GPL-3.0——内部使用可以，对外交付需隔离为独立进程 |
| [osslabz/evm-abi-decoder](https://github.com/osslabz/evm-abi-decoder) | ABI 解码（input + log） | TS / GPL-3.0 | 67 | 2026-11-18 | 95 | 观察：活跃但 GPL，与 loop-decoder 二选一 |
| [Nighty3098/SkyFall](https://github.com/Nighty3098/SkyFall) | 桌面 OSINT 工具箱（含区块链模块+关系图） | Python / MIT | 92 | 2026-11-15 | 129 | 参考：域名/社交/泄露库等传统 OSINT 一并覆盖，链上部分较浅，适合辅助溯源身份 |
| [slowmist/slowmist-agent-security](https://github.com/slowmist/slowmist-agent-security) | 慢雾：AI Agent 安全审查框架 | Markdown / MIT | 560 | 2026-04-17 | 0 | 参考（方法论）：非链上取证，但其"外部输入全部不可信"的审查清单可迁移到工具评测 |
| [slowmist/Web3-Project-Security-Practice-Requirements](https://github.com/slowmist/Web3-Project-Security-Practice-Requirements) | 慢雾：Web3 项目安全实践要求 | Markdown / Apache-2.0 | 356 | 2025-03-25 | — | 参考（方法论）：研判涉诈项目安全设计的对照清单 |
| [slowmist/papers](https://github.com/slowmist/papers) | 慢雾漏洞研究通告归档 | Markdown / Apache-2.0 | 278 | 2025-02-26 | 0 | 参考（情报）：涉诈合约漏洞利用手法的公开档案 |
| [zacharyrogue/Crypto-Whale-Tracker](https://github.com/zacharyrogue/Crypto-Whale-Tracker) | "实时鲸鱼监控+TG 告警" | Python / MIT | 180 | 2026-11-19 | 226 | **排除**：见落选说明——第二个 Wallet-Risk-Scanner |

### 本类要点

- 【事实｜slowmist 组织仓库全扫，2026-11-19】慢雾组织 30+ 仓库逐个翻过：高星仓库全部是审计路线图（Learning-Roadmap，927★，无 LICENSE）、MCP 安全清单（834★）、Agent 安全框架（560★）、安全实践要求（356★）等**教育与框架类**；`papers` 是漏洞通告归档。**没有任何 AML/资金追踪/聚类方向的开源代码**——MistTrack 闭源。
- 【事实｜beosin 检索，2026-11-19】Beosin 命中唯一仓库是 2022 年停更的 VSCode 扩展（4★）；sharkteam、lianantech 无有效命中。
- 【事实｜vasturiano/3d-force-graph 元数据】MIT、6,580 star、2026-11-05 仍在推送；是 3D 力导向图事实标准（大量上层封装）。
- 【推断｜置信度：高】可视化层维持 Cytoscape.js 主力不变；新增的 3D/GPU 两条备选只在"汇报需要 3D 演示"与"节点数突破十万"两个明确触发条件下启用，避免又一次"为了炫技引入图形栈"。
- 【推断｜置信度：高】中文厂商开源的可用部分是**方法论文档**（Apache/MIT 的清单与框架），可作为评测自研规则与培训材料来源；代码层不要指望。

### 落选与去重说明

- **zacharyrogue/Crypto-Whale-Tracker**：创建 6 天冲到 180 star、226 次提交——但贡献者 1 人、提交信息全部是 `Auto commit: <时间戳>`（每约 28 分钟一条），与主页 3.8 的 Wallet-Risk-Scanner **完全同款刷量模板**。两个独立样本说明这套"机器流水+星标冲量"已成型，反刷量三条判据（单贡献者/模板化提交/star 与活动脱节）有效，应作为常态检查写进后续调研流程。
- anvaka/VivaGraphJS（3,869★，NOASSERTION 许可标识）：老牌但许可字段不明确 + 有 sigma.js/cytoscape 可替代，不引入。
- splunk/splunk-3D-graph-network-topology-viz：无 LICENSE。
- sanbir/evm-hack-poc 等漏洞 PoC 归档类：与研判流水线无直接接口，不引入（漏洞情报走 slowmist/papers 与官方通告即可）。

## 06. 长尾补扫：稳定币监控 / 地址告警 / 其他链 / 审计与 MEV

**结论**：①**USDT/USDC 冻结与黑名单追踪没有专门的开源工具在维护**——检索零有效命中，唯一落在产品里的实现是 crypttrace 的 freeze.py（直查发行方合约，见 03 类）；这一层要么自写（几百行），要么随 watchman 名单走。②地址监控告警层全是单人小工具，TRON 侧维持 fystack 结论不变。③**MEV/三明治检测全线停更**（flashbots/mev-inspect-py 已 archive），只剩一个 5 天大的 SandwichTrace 在做 Uniswap V2 离线检测——"受害地址是否遭遇 MEV 夹击"这个研判问题暂时没有可靠开源答案。④审计三件套（slither/echidna/mythril）对涉诈合约分析可用，注意 slither/echidna 是 AGPL-3.0。⑤其他链采集：Solana 有 solana-etl（勉强活着）与 subsquid 全家桶（agent 01 类已覆盖，注意其 tron/evm 包是 GPL 而非顶层 Apache）。

| 项目 | 定位 | 栈 / 许可 | star | 最后提交 | 13周提交 | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| [crytic/slither](https://github.com/crytic/slither) | Solidity/Vyper 静态分析 | Python / AGPL-3.0 | 6,422 | 2026-11-18 | 3 | **工具**：涉诈合约的漏洞与后门静态扫描（可提权、隐藏转账、任意调用检测） |
| [crytic/echidna](https://github.com/crytic/echidna) | 合约模糊测试 | Haskell / AGPL-3.0 | 3,200 | 2026-11-18 | 27 | 工具：与 slither 同厂，用例更窄 |
| [ConsenSysDiligence/mythril](https://github.com/ConsenSysDiligence/mythril) | 符号执行漏洞扫描 | Python / MIT | 4,279 | 2026-04-27 | 0 | 观察：MIT 许可最干净，但 7 个月无提交 |
| [Nad-Am/SandwichTrace-Core_38](https://github.com/Nad-Am/SandwichTrace-Core_38) | Uniswap V2 三明治离线检测 | Python / Apache-2.0 | 3 | 2026-11-11 | 17 | 观察：方向对口（受害交易 MEV 夹击认定）、太新太小 |
| [flashbots/mev-inspect-py](https://github.com/flashbots/mev-inspect-py) | MEV 检查器 | Python / MIT | 849 | 2024-11-27 | 0 | 排除：**已归档**；mev-inspect-rs（561★）停在 2022 |
| [blockchain-etl/solana-etl](https://github.com/blockchain-etl/solana-etl) | Solana 采集 | Python / MIT | 40 | 2026-09-17 | 1 | 观察：ethereum-etl 同门，勉强维持 |
| [subsquid/squid-sdk](https://github.com/subsquid/squid-sdk) | 多链 ETL 工具箱 | TS / Apache-2.0（部分包 GPL） | 1,347 | 2026-11-18 | — | 备选：见 01 类深入分析——**唯一内置 TRON 原生摄取的主流框架**，许可分层需注意 |
| [TrueBlocks/trueblocks-khedra](https://github.com/TrueBlocks/trueblocks-khedra) | TrueBlocks 的 Go 重写（索引/监控） | Go / GPL-3.0 | 4 | 2026-11-04 | 1 | 观察：原 trueblocks-core 已判实质停摆，团队重心在 khedra，但同样低速 |
| [8-diagrams/usdtbillmon](https://github.com/8-diagrams/usdtbillmon) | TRC20 USDT 收款通知 TG 机器人 | Python / MIT | 96 | 2023-07-14 | 0 | 排除：停更两年半；"USDT 账单监控"需求现在由 fystack 覆盖 |
| [moha-abdi/tether-watcher](https://github.com/moha-abdi/tether-watcher) | TRON/BSC USDT 监听 | Go / **无 License** | 11 | 2025-02-15 | 0 | 排除：无许可 |
| [alanisme/deeplens](https://github.com/alanisme/deeplens) | EVM 分析/画像/资金路径 | **无维护**（2 commits） | 13 | 2026-03-13 | 0 | 排除：一次性仓库，与 crypttrace 功能重叠 |
| [prismarmorergirder/wallet-security-checker](https://github.com/prismarmorergirder/wallet-security-checker) | "SafeWallet 钱包检查" | **仅 2 commits** | 112 | 2026-11-14 | 2 | 排除：创建当天 112 star、全程 2 次提交——星标冲量样本 |
| [Driftgrocontact/spout-osint-whale-alerts](https://github.com/Driftgrocontact/spout-osint-whale-alerts) | "鲸鱼 OSINT 监控" | **仅 7 commits** | 166 | 2026-11-13 | 7 | 排除：创建与推送同日、166 star——同上 |
| [whale-alert/whale-alert-examples](https://github.com/whale-alert/whale-alert-examples) | Whale Alert 官方 API 示例 | Python / MIT | 9 | 2026-08-28 | — | 参考：商业 API（收费），SDK 只是封装，不解决"开源自建" |

### 本类要点

- 【事实｜GitHub 检索，2026-11-19】"usdt blacklist""tether frozen"两组检索的全部命中要么无 LICENSE、要么停更、要么是支付网关类无关项目——**发行方冻结事件的独立追踪工具在开源侧不存在**。Tether 官方每月公告 + crypttrace 的 freeze.py 合约直查是当前仅有的两条路。
- 【事实｜flashbots/mev-inspect-py 仓库状态】`archived: true`（归档于 2024-11 后）。MEV 检测三兄弟（py/rs/js）全部停更，SandwichTrace-Core_38 是唯一活跃实现（Apache-2.0，17 commits，2026-11-06 创建）。
- 【事实｜slither/echidna 元数据】Trail of Bits 两件套 2026-11-18 仍在推送，AGPL-3.0——内部研判使用没有障碍，对外交付需注意。
- 【推断｜置信度：高】"地址监控告警"这个层没有通用开源答案：fystack（TRON/多链入账）、panoptes（Cardano）、khedra（EVM 外观索引）各管一段，且全是小团队/单人。原型阶段的正确姿势是**用 fystack 起步、告警逻辑自写**（一个 NATS 消费者 + Telegram webhook 的量级），不要找"一站式监控平台"。
- 【推断｜置信度：中高】审计工具对研判的用法：对涉诈合约（假币、后门转账、貔貅）跑 slither 的数据流与权限检测，比人工读 bytecode 快得多；输出作为"合约技术鉴定"附件时要注明工具版本与原理局限。

### 落选与去重说明

- wallet-security-checker（112★）与 spout-osint-whale-alerts（166★）：都是 2026-11-13/14 创建、个位数提交、百星级 star——加上 05 类的 Crypto-Whale-Tracker（Auto commit 模板）与 03 类的 interchange，**本轮扫描共识别 4 个星标冲量仓库**，"刷量仓库池"比想象的大，反刷量检查必须前置。
- tigusigalpa/whale-alert-go|php：商业 Whale Alert API 的 SDK 封装，API 本身收费，与"0 成本基线"冲突。
- nadir 类 sniper/twitter-token-tracker：目标是抢跑交易不是研判，不引入。

## 07. 重点项目静态走读（本人，2026-11-18 夜）

对主页四项"待验证"级项目 + 本轮两大新发现做的只读走读（不构建、不运行）。完整笔记在调研工作区，这里放结论。

**moov-io/watchman**（名单筛查，主页 3.5）
- 【事实｜pkg/search/similarity.go:15-24】评分权重：唯一标识 50 / 姓名 35 / 地址 25 / 辅助信息 15，exactMatch 阈值 0.99。
- 【事实｜pkg/search/similarity_exact.go:373-413】crypto 地址匹配为**精确等值（大小写不敏感）**，双方都给币种时币种必须一致；【事实｜docs/search.md:90】强制 1.0 的官方条件是"标识符**与国家**同时匹配"——主页 78af83c 的口径修正与官方文档一致。
- 【事实｜pkg/sources/】解析器覆盖 ofac / us_non_sdn / csl_us / csl_eu / csl_uk / csl_un / fincen_311 / opensanctions / senzing；OFAC 备注 "Digital Currency Address - XBT ..." 由正则解析进 crypto 字段（mapper.go:507）。
- 【推断｜置信度：高】TRON 地址（T 开头）能否命中取决于上游名单是否收录，watchman 本身不限制币种；实测时应同时验证 1.0 命中路径与 TRON 覆盖边界。

**fystack/multichain-indexer**（采集，主页 3.3）
- 【事实｜internal/indexer/tron.go + internal/rpc/tron】TRON 有独立 indexer，走 TronGrid HTTP API（免自建全节点），带 failover；【事实｜tron.go:48-61】`pubkeyStore == nil` 时**不过滤、全部交易进入处理**。
- 【推断｜置信度：中高】主页"需改造成通用拉取"偏保守：不配监控地址即可全量流转，"改造"实为自写一个 NATS JetStream 消费者落 PostgreSQL，工作量小一个量级。风险：无查询 API 层；全量模式在 TRON 主网量级的吞吐未验证。

**bobslayerX/crypttrace**（本轮新发现，03 类主力候选）
- 【事实｜src/crypttrace/fetchers/tron.py】TRON 走 TronGrid 免 Key，处理 hex→base58，docstring 直接点名杀猪盘 USDT-TRC20 场景；【事实｜src/crypttrace/freeze.py】USDT/USDC 冻结检查直查发行方合约 `isBlackListed`（ETH 公共 RPC / TronGrid / Solana token account 三路）。
- 【事实｜README】EVM 走 Etherscan API——**BSC/Optimism/Base 免费档不支持，需付费档**，与链上组 tools.md"免费窗口塌陷"结论互相印证。
- 【推断｜置信度：中高】本轮对研判流水线价值最高的单项发现："报案→钱包→钱去哪、在哪能拦"与政策组案例库场景直接对齐。风险：单人维护、建仓 4 个月、无第三方使用记录。

**prettydeath/TornadoCash-demixer**（本轮新发现，03 类主力候选）
- 【事实｜README + 仓库树】PyPI 包 + Zenodo DOI + mkdocs 文档 + 安慰剂校准（EVALUATION.md）；8 条 EVM 链 56 池；证据三档 strong/moderate/weak，**作者自证金额+时间、gas 复用等弱信号在真实存款人上与随机无异，永不提级**。
- 【事实｜提交记录】1 名维护者，人写提交（"Release 2.23.1: re-run of hold-outs and placebo"），近 13 周 129 次提交全部落在 8 周生命周期内。
- 【推断｜置信度：中高】DeMix 论文方向的可运行工程化实现，方法学克制罕见；TRON 侧混币不在覆盖内。

**heathermhuang/altscan**（BSC 浏览器，主页 3.7）
- 【事实｜apps/explorer/lib/watch-addresses.ts】watchlist 按 owner 分组、默认上限 50 地址、pg advisory lock 防并发超限；代码注释自述 "Sized for individuals and small bots, **not deposit-monitor services**"。
- 【推断｜置信度：中】主页"只读借鉴"结论成立：可借接口设计与幂等写法，索引层不押注。待办"读 altscan 判断能否只借 watch_addresses 层"可打勾（静态走读级）。

**mikispag/bitiodine**（聚类，主页 3.6）
- 【事实｜src/visitors/clusterizer.rs:103-182 + Cargo.toml】Tarjan Union-Find（union-by-rank + 路径压缩）+ SQLite 按块提交 + 144 块 undo 历史做重组回滚；支持 P2PK→Taproot 全谱系。
- 【事实｜README】作者自证："Cluster membership is evidence of possible common ownership, **not proof**"；≥3 个等值输出的过滤不识别 Payjoin 协作交易，**明示会误合并**。
- 【推断｜置信度：高】主页"方法可借、代码不可搬到 TRON"成立且获作者自证；"状态可重放 + 重组回滚 + 按块提交"三件套是聚类工程化的样板。

## 08. 对主页 oss-projects.md 的修订建议

待 PR #18 合并后另开 PR 落地，以下按优先级：

1. **3.9 结论改写**（最重要）：混币取证与多链资金追踪在 EVM/多链侧已出现可部署实现（TornadoCash-demixer、crypttrace，均单人维护需自证）；OTC/跑分识别、跨链桥自动化命名、TRON 侧混币取证**仍空缺**。
2. **3.3 fystack 行"代价"列修正**：不配监控列表即可全量流转，改造成本实为"自写 NATS 消费者落库"。
3. **四、推荐组合增补**：筛查层补 `phishdestroy/destroylist`（域名黑名单源，MIT）；追踪层列 crypttrace 为"追踪候选（待实测）"；采集层列 `rindexer`（ETH/BSC）与 `squid-sdk tron 包`（TRON，注意 GPL 分层）为采集候选。
4. **3.8 反刷量案例更新**：新增 4 个样本（interchange / Crypto-Whale-Tracker / wallet-security-checker / spout），其中 Auto commit 模板与原案例完全同款——三条判据写进"调研口径"。
5. **待办清单增补**：实测 crypttrace（TRON 已知案件复现）、实测 Crypto_Honeypot_Detector（BSC 蜜罐代币）、复核 squid-sdk tron 包 GPL 传染边界、destroylist 误报率抽样、MetaMask DBAD 许可法务确认。
6. **2.5 活跃度表补充**：pygraphistry（13 周 1,452 提交）、mempool（13 周 455）、rindexer（wk13=32，v1.0.0 刚发版）。

## 09. 局限与待验证

- 【口径】**全部结论基于静态走读与 API 元数据，本轮未运行任何工具**（纪律：不构建、不运行克隆代码）。"主力候选"升级为主力前必须：用已知案例复现（OFAC 已罚地址、Ronin 案、本地蜜罐代币）、跑空转基线（干净地址零误报）。
- 【风险】两个追踪类主力候选（crypttrace、TornadoCash-demixer）均为**单人维护、无第三方复现记录**——输出正确性未经社区检验，研判结论不能只依赖单一工具输出（与主页"关键判断至少两个独立来源"纪律一致）。
- 【口径】GitHub 检索的覆盖偏差：英文关键词对中文项目不敏感（"区块链 取证"检索命中的是 CTF 题解）；"tornado"被 Python 框架污染严重；闭源商业工具不在射程。空缺结论均指"GitHub 检索范围内"。
- 【待验证】squid-sdk tron 包对 TRC20 / 内部交易的解码覆盖度；rindexer 在 BSC 3s 出块下的回填吞吐；GoPlus 免费额度对日均筛查量的满足度；destroylist 误报率；MetaMask DBAD 许可的对外交付边界。
- 【事实】全部 star / 提交数为 2026-11-18 夜—11-19 晨快照；引用超过一个季度请按主页「调研口径」命令重跑。

## 10. 二轮深挖：六个空缺方向的复查（2026-11-19）

针对首轮确认的六个空缺，换关键词、翻组织仓库、读数据源脚本做了第二轮排查。结论先行：**①地址级黑名单从"空缺"改为"有数据源"；②USDT 冻结追踪找到可直接抄的方法论实现；④Travel Rule 找到唯一活着的开源协议（TRISA）；③⑤⑥经更宽检索后维持空缺，但给出了可行的自建路径**。

| 方向 | 首轮结论 | 二轮发现 | 修订后结论 |
| --- | --- | --- | --- |
| ① 地址级 drainer 黑名单 | 空缺 | [scamsniffer/scam-database](https://github.com/scamsniffer/scam-database) 内含 `blacklist/address.json`（2,530 条 ETH 地址，bot 更新，wk13=113）；[prettydeath/wallet-attribution](https://github.com/prettydeath/wallet-attribution)（63.4 万条归因地址 / 48 链，含 scam/mixer/hacker/sanctioned 类目，MIT 文本）；ChainAbuse 为封闭注册平台 | **有数据源，无统一标准**：scamsniffer（小而精，GPL-3.0）+ wallet-attribution（大而全，SPDX 缺失需法务留痕）交叉使用；drainer 专项标签仍靠商业源补 |
| ② USDT 冻结事件追踪 | 无专门工具 | wallet-attribution 的 `scripts/fetch_onchain.py` **就是**这件事：从 USDT 合约 `AddedBlackList/RemovedBlackList` 事件重建当前黑名单——ETH `0xdAC17F…` 与 TRON `TR7NHq…`（TRC20 USDT）双链，TronGrid 免 Key；USDC 同理（`Blacklisted/UnBlacklisted`） | **方法论找到，可直接抄**：脚本 MIT，几百行；"事件级实时告警"仍需自建，但"当前冻结名单"已可自动化重建 |
| ③ MEV 检测 | flashbots 已 archive | [zeromev/zeromev-core](https://github.com/zeromev/zeromev-core)（ZeroMEV 论文核心，MIT，2024-12 停）；Solana 侧零散小工具（Tao-2022 jito 夹击检测器 22★，2025-07 停） | **维持弱项**：ETH 侧活跃维护的完整实现仍无；归档的 mev-inspect-py 代码可读，三明治认定建议自研或直接用 03 类 SandwichTrace |
| ④ Travel Rule | OpenVASP 停摆 | [trisacrypto/trisa](https://github.com/trisacrypto/trisa)（TRISA：MIT，14 贡献者，2019 起家，2026-01 仍有提交但年提交仅 1 次） | **找到唯一活着的开源协议**：TRISA 演进缓慢但组织化；协查技术原型可读 TRISA，实际落地仍靠人工对接 |
| ⑤ TRON 混币取证 | 空缺 | [DarkFlorist/tronar](https://github.com/DarkFlorist/tronar)（TRON 版 Tornado SDK，无许可，2025-02 停）——**证明 TRON 侧混币协议真实存在**；wallet-attribution 的 mixer 标签可圈定"接触过混币器的地址" | **缺口维持**：demixer 的行为启发式未移植到 TRON（账户模型 + 能量模型差异），是明确的自研方向 |
| ⑥ 蜜罐检测 TRON 等价物 | 空缺 | 全网检索零命中；GoPlus SDK 对 TRON 仅 1 处引用（端点疑似存在但 SDK 支持薄弱） | **缺口维持**：可行路径 = GoPlus TRON 端点直接调 API 实测 + java-tron `triggerconstantcontract` 自研买/卖模拟（注意 TRON 无 state-override，"预授权模拟器"打法不可移植） |

### 本节要点

- 【事实｜scam-database 仓库树 + contents API，2026-11-19】`blacklist/address.json` 实测 2,530 条小写 ETH 地址；`all.json` 聚合域名+地址；仓库近 13 周 113 次提交（bot 更新），GPL-3.0。
- 【事实｜wallet-attribution README + fetch_onchain.py 源码，2026-11-19】63.4 万地址、48 网络、38.3 万交易所钱包；USDT 黑名单重建覆盖 Ethereum + TRON 双链；数据可由 `fetch_sources.sh` + `build.py` 全量复跑。
- 【事实｜LICENSE 文件原文，2026-11-19】wallet-attribution 的 LICENSE 文本为 MIT（Copyright (c) 2026 Johnny），但 GitHub API 识别为 NOASSERTION（文件缺 SPDX 标识行）——引用数据前留痕即可，对外交付前请法务确认一次。
- 【推断｜置信度：高】②⑥两方向合并看，TRON 侧"代币安全检测"的整体短板是**模拟能力**：EVM 有 state-override / eth_simulateV1，TRON 只有 `triggerconstantcontract` 常量调用——这是协议能力差异，不是开源社区怠惰；自研检测器要按这个约束设计。
- 【推断｜置信度：中高】①的 63 万条归因地址若并入自建标签库，等于一次性拿到交易所/制裁/黑客/混币/赌博五个类目的底表——但它是**多源聚合再分发**，每条标签的上游来源要随行携带（数据集带 source 列），直接引用前抽检准确率。
- 【待验证】wallet-attribution 各类目在 TRON 地址上的覆盖度（TRC20 地址占比）；GoPlus TRON 端点的实际可用性；scam-database address.json 的误报率。

## 参考

本页全部项目均见各节表格内 GitHub 链接。方法与命令沿用主页「调研口径」。原始走读笔记与 JSON 索引：调研工作区 `oss-scan/sections/`（01–06）与 `oss-scan/notes/`（deepread-2026-11-19）。

1. 主页：[开源项目调研](./oss-projects) · [Blockscout 专题](./blockscout) · [链上分析工具对比](/onchain/tools)
2. 走读对象：moov-io/watchman · fystack/multichain-indexer · bobslayerX/crypttrace · prettydeath/TornadoCash-demixer · heathermhuang/altscan · mikispag/bitiodine
3. 反刷量同款样本：Soniavasseur/Wallet-Risk-Scanner（主页 3.8）· zacharyrogue/Crypto-Whale-Tracker · tabookhandawn/interchange-osint-cross-chain-tracing
