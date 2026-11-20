# fund-graph · 资金流转图快照管线

为 [链路可视化研究](/onchain/visualization) 生成"可复算"的资金流转图快照，并产出五层结构示意图。

数据来自 `economic_detect` 示例库的**项目0**（case 1）：银行 + 微信 + 发票共 312 行成功流水，32 个被害人账户、45 个非虚拟账户。

## 文件

| 文件 | 作用 |
| --- | --- |
| `build_snapshot.py` | 读 `demo.db` → 生成 `docs/public/demo/fund-graph/data.json`（节点/边/汇总/自检/sha256），可顺带冻结 `txns.csv` |
| `verify_snapshot.py` | 只用冻结的 `txns.csv` 重跑同一套口径，比对 sha256 与关键金额，14 项全 PASS 才算过 |
| `make_layers_svg.py` | 读 `data.json` → 断言关键金额 → 生成 `docs/public/img/onchain/five-layers.svg` |
| `txns.csv` | 冻结的 312 行原始流水，用于离线复算 |

## 用法

```bash
# 1) 生成快照（需要 examples/demo.db）
python prototypes/fund-graph/build_snapshot.py \
  --db examples/demo.db \
  --out docs/public/demo/fund-graph/data.json \
  --freeze prototypes/fund-graph/txns.csv

# 2) 复算校验（不需要数据库）
python prototypes/fund-graph/verify_snapshot.py

# 3) 生成五层示意图
python prototypes/fund-graph/make_layers_svg.py
```

判定标准：`verify_snapshot.py` 输出 `RESULT: PASS`、退出码 0，且 sha256 为
`f0b632f6fbb74b830e8b40850d28f6b5cca501b3ce263ec8a5bf72a0fe3b8ce4`。

## 口径（改这三条金额一定对不上）

1. **只从出账行建边**，入账行只用于核对镜像。两边都翻成边会把镜像算两次（张海涛出金会变成 912,855.27，实际 454,051.27）。
2. **同一 `(出方, 入方, 金额, 时间)` 视为重复**，本案剔除 59,997.00。
3. **找不到对应出账行的入账不入图**，只记进 `meta.counts.orphanInRows`（本案 35 条 / 518,804.00）。

## 当前快照

| 指标 | 值 |
| --- | --- |
| 原始流水 | 312 行（成功） |
| 去重后笔数 | 142 |
| 聚合边 / 节点 | 55 / 46 |
| 原始出账合计 | 2,064,875.26 |
| 去重后出账合计 | 2,004,878.26 |

可视化 demo 在 `docs/public/demo/fund-graph/`，同目录的两个渲染引擎（Cytoscape.js / AntV G6）吃同一份 `data.json`。
