---
title: 公开数据集清单
---

# 公开数据集清单

<div class="doc-meta">
  <span class="owner">负责人：@梦幻居士</span>
  <span class="doing">状态：进行中</span>
</div>

## 结论摘要

1. **带标注、可直接建模的公开数据集中在比特币上，且时效偏旧。** 主流三套（Elliptic、Elliptic++、BitcoinHeist）覆盖 2009–2019 的 BTC 数据，对稳定币、TRON、多链与 L2 场景几乎没有覆盖。【事实】
2. **官方制裁清单是唯一可直接当"事实"用的标签源。** OFAC SDN、FBI IC3 公告、DOJ 起诉书属于权威出处；社区举报库只能当线索。【推断】
3. **制裁清单会撤销。** Tornado Cash 2022-08-08 被制裁、2025-03-21 被除名，引用历史快照会直接导致误判。【事实】
4. **免费与 API Key 两列尚未逐项实测**，以各发布方官方页当期政策为准。【待验证】

## 一、学术研究数据集（带标注，可用于建模）

| # | 数据集 | 规模与结构 | 标注内容 | 获取方式 |
| --- | --- | --- | --- | --- |
| 1 | Elliptic Data Set | 203,769 个交易节点、234,355 条有向边、49 个时间片；每节点 166 维特征（94 本地 + 72 一跳聚合） | 非法 4,545（2.2%）、合法 42,019（20.6%）、未知 157,205（77.2%）；非法含暗网市场、诈骗、恶意软件、勒索、庞氏 | [Kaggle](https://www.kaggle.com/ellipticco/elliptic-data-set)、[Hugging Face](https://huggingface.co/datasets/yhoma/elliptic-bitcoin-dataset) |
| 2 | Elliptic++ | 822,942 个地址节点、2,868,964 条地址-地址边、56 维特征、49 时间片；提供 4 种图视图 | 地址级标注，非法占比约 1.7% | 随 Elliptic 扩展论文发布 |
| 3 | BitcoinHeist | 2,916,697 条实例、10 个字段；2009-01 至 2018-12，按 24h 快照组织；过滤 < 0.3 BTC 的边 | 24 个勒索软件家族标签；标签来自 Montreal、Princeton、Padua 三项研究 | [UCI id=526](https://archive.ics.uci.edu/dataset/526/bitcoinheistransomwareaddressdataset)，DOI `10.24432/C5BG8V`；[Kaggle](https://www.kaggle.com/datasets/sapere0/bitcoinheist-ransomware-dataset/data) |
| 4 | IBM Transactions for AML（HI-Small） | 约 515,000 账户、500 万笔交易、10 个模拟日；洗钱:合法 ≈ 1:981 | 8 种洗钱类型：fan-out、fan-in、cycle、random、bipartite、stack、scatter-gather、gather-scatter | IBM 研究发布（合成数据，适合模式识别基线） |
| 5 | CCLT 多链标注库 | 290,000+ 标注地址，覆盖 8 个主流跨链桥 | 跨链洗钱路径标注；案例含 FTX、BNB Bridge、Mad Meerkat Finance | *Cross-Chain Laundering Tracer*, Springer, DOI 10.1007/978-981-92-2973-4_15 |
| 6 | 跨层取证数据集（DID） | 自托管全节点交易历史；L1/L2 关联事件（Arbitrum、Optimism、zkSync Era、Starknet 等） | 六启发式加权评分模型；含验证交易哈希与脱敏嫌疑地址集 | [GitHub: bertter/DID](https://github.com/bertter/DID) |

### 三条关键提示

- Elliptic 数据集在 **timestep 43** 存在显著分布漂移（对应某大型暗网市场关闭），是检验模型时序鲁棒性的天然测试点。【事实】
- BitcoinHeist 的 6 个核心拓扑特征与 [五类特征](./address-features)直接对应：【事实】
  - `length` → 混币轮次（拆分-转移-合并的深度）
  - `weight` → 合并行为（输入地址数 > 输出地址数）
  - `count` → 合并交易次数
  - `loop` → 拆分→多路径→合并的环路计数
  - `neighbors` → 地址直接连接数
  - `income` → 收入金额（Satoshi）
- IBM 数据集的 `scatter-gather` / `gather-scatter` 是"多地址集散"的标准学术命名。【事实】

## 二、官方制裁与执法清单（权威标签源）

| 数据源 | 内容 | 地址数量级 | 链接 |
| --- | --- | --- | --- |
| OFAC SDN List（美国财政部） | 受制裁个人/实体及其加密货币地址标识符 | 持续更新 | https://www.treasury.gov/ofac |
| OFAC 历史标注汇总（Chainalysis 整理） | 逐次制裁行动与地址清单：Lazarus Group、Blender.io、Tornado Cash、Hydra、Garantex、Suex、Chatex 等 | 见 [公开案例地址](./case-addresses) | https://www.chainalysis.com/blog/ofac-sanctions/ |
| FBI IC3 公告 | 重大盗窃案归因与地址通报（如 Bybit 案 I-022625-PSA） | 按案件 | https://www.ic3.gov |
| 美国司法部（DOJ） | 起诉书与没收令中的涉案钱包路径 | 按案件 | https://www.justice.gov |

::: warning 时效性提醒
制裁清单会变动。Tornado Cash 于 2022-08-08 被首次制裁（38 个地址）、2022-11-08 重新指定（新增 90 个地址），后因 2024-11 第五巡回法院裁决越权，于 **2025-03-21 正式除名**。研判时须以实时 SDN 为准，不可引用历史快照作为当前结论。【事实】
:::

## 三、社区举报类标签库（辅助参考，质量参差）

| 平台 | 运营方 | 数据库规模 | 特点 |
| --- | --- | --- | --- |
| Chainabuse | TRM Labs | ~220,000 | 多链（BTC/ETH/SOL/ADA），专业团队复核 |
| Bitcoin Abuse DB | BitcoinAbuse.com | ~300,000 | 仅 BTC，举报不可删除/编辑，需甄别误报 |
| Scan Blocks | Clockwork Venture | ~310,000 | 地址查询 + 浏览器插件 |
| Scam Alert | Whale Alert | ~130,000 | 链上分析引擎联动 |
| GreySafe | Blackworks.io | ~131,000 | 社区驱动，强调验证与归因 |
| CryptoScamDB | MyCrypto 社区 | ~9,221 | [GitHub blacklist](https://github.com/orgs/CryptoScamDB/repositories)、[JSON API](https://api.cryptoscamdb.org/v1/addresses)；适合历史回溯，不宜当作实时黑名单 |

汇总索引：[Cryptocurrency Theft, Fraud and Scam Reporting Services](https://github.com/Web-n-Composite/crypto-theft-reporting)

**使用原则**：社区标签按"线索"而非"事实"处理；命中后必须回溯原始举报证据（截图、事件链接、时间），并做时间衰减。【推断】

规模数字引自各平台公开介绍页，未逐一复核当期状态。【待验证】

## 两个坑

- Elliptic 为早期比特币数据，与 TRON/USDT 生态差异大，模型效果不代表实战。【推断】
- 合成数据（IBM AMLSim、PaySim 类）分布人造，指标再高也无实战意义；策展页须回原始发布页。【推断】

## 下一步

- [ ] 实测各数据集是否免费、是否需要 API Key，回填"免费/API Key"两列。
- [ ] 用 Elliptic 与 BitcoinHeist 各跑一轮基线，记录五类特征命中率与误报率。
- [ ] 社区标签库抽 50 条做准确率抽查，量化"线索"成色。

## 参考

见 [异常地址特征](./address-features) 的参考节，以及本页各数据集官方链接。
