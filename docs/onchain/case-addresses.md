---
title: 公开案例地址与链路
---

# 公开案例地址与链路

<div class="doc-meta">
  <span class="owner">负责人：@梦幻居士</span>
  <span class="doing">状态：进行中</span>
</div>

## 结论摘要

1. **能直接用于规则比对的真实地址只有 5 个**，全部来自美国财政部 OFAC 联邦公报与 UCI 数据集，其余案例的地址未公开、只能按资金路径建模。【事实】
2. **Ronin Bridge 案是链路复盘最完整的样本**：6.2 亿美元被盗、经混币器与 CEX 两条路径清洗、Binance 冻结 86 个账户追回约 580 万美元，每个节点都有公开出处。【事实】
3. **2025 年态势发生了结构性变化**：非法地址收款 1,540 亿美元同比 +162%，但资金直接进交易所的比例从 40%+ 降到约 15%——中间"分层"环节显著增加，这正是五类特征要盯的位置。【事实】
4. **所有地址都是公开账本上的伪匿名标识符**，列出它们不构成对任何实体的指控。【事实】

## 一、已核实的公开地址

可直接用于规则 / 白名单比对。【事实】来源：OFAC 联邦公报与 UCI 数据集。

| 案例 | 链 | 地址 | 来源与说明 |
| --- | --- | --- | --- |
| Lazarus Group / Ronin Bridge 主地址 | ETH | `0x098B716B8Aaf21512996dC57EB0615e2383E2f96` | OFAC 2022-04-14 首次列入 SDN；案发时持有约 148,000 ETH。来源：[Federal Register 2022-09073](https://public-inspection.federalregister.gov/2022-09073.pdf) |
| Lazarus Group 关联地址 1 | ETH | `0xa0e1c89Ef1a489c9C7dE96311eD5Ce5D32c20E4B` | OFAC 2022-04-21/22 更新 SDN，来源同上 |
| Lazarus Group 关联地址 2 | ETH | `0x3Cffd56B47B7b41c56258D9C7731ABaDc360E073` | 同上 |
| Lazarus Group 关联地址 3 | ETH | `0x53b6936513e738f44FB50d2b9476730C0Ab3Bfc1` | 同上 |
| CryptoLocker 勒索地址 | BTC | `1LXrSb67EaH1LGc6d6kWHq8rgv4ZBQAcpU` | BitcoinHeist 数据集；在 24h 快照中最多出现 420 次，为出现频次最高的勒索地址之一 |

::: tip 使用前请自行复核
上表地址抄自 2022 年的官方文件。制裁清单会撤销、地址语义会过期，引用前请在 [OFAC Sanctions List Search](https://sanctionssearch.ofac.treas.gov/) 按当前状态核对一次，并记录核对时间。【推断】
:::

### Ronin Bridge 案关键数据

用于链路复盘：【事实】来源：[GDF《Cryptoassets and Sanctions Compliance》](https://www.gdf.io/wp-content/uploads/2022/07/Cryptoassets-and-Sanctions-Compliance-Report-Final-1.pdf)、[Quadriga Initiative 案例库](https://quadrigainitiative.com/cryptocurrencyhackscamfraudwiki/index.php?title=Axie_Infinity_Ronin_Bridge_Unauthorized_Treasury_Access)。

- 2022-03-23 被盗：173,600 ETH + 25.5M USDC，总值约 6.2 亿美元。
- 资金分流：部分经 **Tornado Cash**（OFAC 2022-08-08 制裁，涉 4.55 亿美元）、部分经 **Blender.io**（首个被制裁的混币器，处理约 2,050 万美元赃款）。
- 2022-04-22 新增制裁的 3 个地址曾合计持有约 50,000 ETH（约 1 亿美元）。
- Binance 冻结了转入平台的 86 个账户，追回约 580 万美元。

## 二、公开案例链路（地址脱敏或未公开，按资金路径建模）

| 案例 | 时间 | 链路特征 | 来源 |
| --- | --- | --- | --- |
| Zheng Zhao 杀猪盘洗钱案 | 2025 指控，2026-10 引渡 | 174 名美国受害者 → 美国银行账户 → 巴哈马银行账户 → 兑换 USDT → 柬埔寨控制钱包 → 诈骗园区头目；8 名共谋者认罪 | 美国 DOJ / [新浪财经](https://finance.sina.com.cn/jjxw/2026-10-26/doc-iniwqpfm5204631.shtml) |
| Bybit 黑客案 | 2025-02-21 | 约 15 亿美元（史上最大数字资产盗窃）；FBI 归因 DPRK "TraderTraitor"（IC3 公告 I-022625-PSA）；2025 年 DPRK 全年盗窃超 20 亿美元 | [Chainalysis 2025 犯罪报告](https://www.chainalysis.com/blog/report-the-changing-nature-of-cryptocrime/) |
| A7A5 卢布稳定币制裁规避 | 2025 | 10 个月内处理约 933 亿美元；Grinex 至少 47.6 亿、Meer 约 3.05 亿美元 | [Chainalysis 制裁报告](https://www.chainalysis.com/blog/crypto-sanctions-2026/) |
| 太子集团 / 陈志（Prince Group） | 2025 | 东南亚杀猪盘网络，被制裁；与 Huione Guarantee 担保平台生态关联 | 同上、[CNBC 报道](https://www.cnbc.com/amp/2026/02/02/chinese-money-laundering-networks-crypto-telegram-2025-chainalysis-scam-southeast-asia-cambodia.html) |
| TRON 哈希博彩靓号地址 | 2022 案例 | 猜尾号玩法；投注地址为定制靓号（原文已脱敏）；高频、固定金额往来，赌资来自/回流 CEX，造成"资金污染" | [Bitrace / 腾讯新闻](https://news.qq.com/rain/a/20231023A04C9L00) |
| USDT 跑分案（山东德州/陕西靖边） | 裁判文书 | 提供银行卡、USDT 管理、交易所账户人脸验证供转移赃款；定性帮信罪/掩隐罪 | [黑灰产 USDT 变现模式分析](https://new.qq.com/rain/a/20261026A0EAF900) |

::: warning 数字要看口径
A7A5 的"933 亿美元"是**累计处理金额**，不是涉案赃款；Bybit 的 15 亿美元是**被盗资产市值**，两者不可直接比较。引用时写清口径。【推断】
:::

## 三、2025 年宏观态势（研判背景）

据 Chainalysis 2025 犯罪报告：【事实】

- 非法地址全年收到至少 **1,540 亿美元**，同比 +162%；其中受制裁实体收到额同比增长 **694%**（约 1,040 亿美元）。
- **稳定币占全部非法交易量的 84%**（早期报告口径为 63%，呈持续上升趋势）。
- 中国语言洗钱网络（CMLN）2025 年流转约 **161 亿美元**，约占全球加密犯罪市场的 20%；主要通过 Telegram"担保平台"撮合。
- 犯罪资金直接转入交易所的比例从 2021–2022 年的 40%+ 降至约 15%——**说明中间"分层"（混币器、跨链桥）环节显著增加**。

第三、四条对研判的直接含义：直接盯 CEX 入金的收益在下降，识别重点应前移到分层环节，这正是[特征二](./features/smurfing)、[特征三](./features/scatter-gather)、[特征五](./features/chain-hopping)的落点。【推断】

## 下一步

- [ ] 按当前 OFAC 清单逐条复核上表 5 个地址，记录复核时间与当时的制裁状态。
- [ ] 为 Ronin 案补一条完整的资金路径图（L0→L5），可复用[链路可视化研究](./visualization)的五层结构方法。
- [ ] 与[公开通报案例库](../policy/cases)对齐，避免同一案件在两处口径不一致。

## 参考

1. [Federal Register · Notice of OFAC Sanctions Actions (2022-09073)](https://public-inspection.federalregister.gov/2022-09073.pdf)
2. GDF. *Cryptoassets and Sanctions Compliance: A Primer*, 2022.
3. [Chainalysis · The Changing Nature of Crypto Crime (2025)](https://www.chainalysis.com/blog/report-the-changing-nature-of-cryptocrime/)
4. [Chainalysis · Crypto Sanctions 2026](https://www.chainalysis.com/blog/crypto-sanctions-2026/)
