# USDT/USDC 冻结黑名单重建原型（P1）

检测模型页排期项 P1 的可运行实现：**不依赖任何第三方黑名单**，直接读发行方合约事件，重建"当前被冻结地址"清单，并输出每条记录的证据（区块号 + 交易哈希）。

## 为什么做

研判中反复遇到三个问题：某地址是否已被发行方冻结？冻结发生在什么时候？依据是哪笔交易？人工去 Tether 公告页翻效率极低，第三方名单又不透明。发行方合约本身就是第一手来源。

## 数据来源（全部免 Key）

| 链 | 合约 | 事件 |
| --- | --- | --- |
| Ethereum | USDT `0xdAC17F958D2ee523a2206206994597C13D831ec7` | `AddedBlackList` / `RemovedBlackList` |
| Ethereum | USDC `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | `Blacklisted` / `UnBlacklisted` |
| TRON | USDT `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | `AddedBlackList` / `RemovedBlackList` |

- EVM：Etherscan 兼容 `getLogs`，通道优先级 `ETHERSCAN_API_KEY` > Routescan（免 Key）> Blockscout（免 Key，强节流兜底）。1000 条/页，按块正序续读。
- TRON：TronGrid `v1/contracts/{addr}/events`，200 条/页翻页。
- 事件 topic0 常量取自 [prettydeath/wallet-attribution](https://github.com/prettydeath/wallet-attribution)（MIT）经人工核读转录，未复制其代码。

## 用法

```bash
python sync.py                # ETH + TRON 全历史
python sync.py --tron         # 仅 TRON
python sync.py --eth-recent 500000   # EVM 只扫最近 50 万块（演练）
# 网络不通时走代理：
HTTPS_PROXY=http://127.0.0.1:7893 python sync.py
```

输出：`data/freeze_blacklist.json`（含生成时间、每条记录的 chain/token/contract/address/block/tx/scope）。

依赖：Python 3.10+ 标准库，无第三方包。

## 首次运行结果（2026-11-19）

| 链路 | 事件 | 当前黑名单地址 |
| --- | --- | --- |
| Ethereum USDT | 全历史 | **1,745** |
| Ethereum USDC | 全历史 | **709** |
| TRON USDT | 10,318 | **8,281** |
| 合计 | — | **10,735** |

## 抽样验证（独立链上核对）

用 `eth_call` / `triggerconstantcontract` 直接问合约 `getBlackListStatus` / `isBlacklisted`：

- ETH USDT 抽样 4 个 → 全部 `true`；2 个干净地址 → 全部 `false`
- ETH USDC 抽样 3 个 → 全部 `true`
- TRON USDT 抽样 3 个 → 全部 `true`；2 个随机合法地址 → 全部 `false`

即：重建结果与合约当前状态**双向一致**（既不漏也不误）。

## 局限

- **事件级实时告警未做**：本原型是"当前快照重建"，可作为定期任务（建议小时级）；实时订阅需接入 WebSocket/节点，属 P1 后续。
- Routescan 无 Key 有速率上限；全历史扫描约 5–10 分钟（USDT+USDC 各数页）。
- topic0 常量如遇合约升级需复核；脚本已把常量集中在文件头部便于维护。
- 输出仅为**线索与证据**，不构成任何定性结论。

## 后续（对应检测模型页排期）

- P1.1：冻结事件增量同步（按块游标，小时级）
- P1.2：将清单接入评分卡 L0/L1（命中冻结名单 → 直出复核队列顶部）
- P1.3：与 watchman 名单做交叉（发行方冻结 vs 制裁名单，两者口径不同，需并列展示）
