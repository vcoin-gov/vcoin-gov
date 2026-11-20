#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复算校验：只用仓库里冻结的 txns.csv，重跑同一套口径，比对 data.json 的 sha256 与金额校验。

用法：
  python verify_snapshot.py                 # 校验同目录 data.json
  python verify_snapshot.py --json <path>   # 校验指定快照
退出码 0 = 全部通过；1 = 有差异。
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_snapshot import build, sha256_of  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JSON = os.path.join(HERE, "..", "..", "docs", "public", "demo", "fund-graph", "data.json")


def load_csv(path: str):
    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            r["txn_id"] = int(r["txn_id"])
            r["batch_id"] = int(r["batch_id"])
            r["amount"] = float(r["amount"])
            rows.append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=DEFAULT_JSON)
    ap.add_argument("--csv", default=os.path.join(HERE, "txns.csv"))
    args = ap.parse_args()

    rows = load_csv(args.csv)
    nodes, edges, outs, ins, orphan_in, single = build(rows)
    recomputed = sha256_of(nodes, edges)

    with open(args.json, encoding="utf-8") as f:
        snap = json.load(f)

    failures = []

    def check(name, ok, detail=""):
        print(("PASS  " if ok else "FAIL  ") + name + (("  " + detail) if detail else ""))
        if not ok:
            failures.append(name)

    check("CSV 行数 = 312", len(rows) == 312, f"actual={len(rows)}")
    check("快照 sha256 可复算", snap["meta"]["sha256"] == recomputed,
          f"snapshot={snap['meta']['sha256'][:16]} recomputed={recomputed[:16]}")
    check("边数一致", len(snap["edges"]) == len(edges), f"{len(snap['edges'])} vs {len(edges)}")
    check("节点数一致", len(snap["nodes"]) == len(nodes), f"{len(snap['nodes'])} vs {len(nodes)}")

    zhang = nodes["6227000000000001"]
    check("张海涛入金 454,051.27", zhang["in"] == 454051.27, f"{zhang['in']}")
    check("张海涛出金 454,051.27", zhang["out"] == 454051.27, f"{zhang['out']}")
    check("去重后出账合计 2,004,878.26",
          round(sum(e["amount"] for e in edges), 2) == 2004878.26)
    check("原始出账合计 2,064,875.26",
          round(sum(r["amount"] for r in outs), 2) == 2064875.26)
    check("镜像缺失入账行 = 35", len(orphan_in) == 35, f"actual={len(orphan_in)}")

    # 快照里的 checks 也逐条复述
    for c in snap["meta"]["checks"]:
        check("快照自检 · " + c["name"], c["pass"] and c["actual"] == c["expected"],
              f"actual={c['actual']}")

    print()
    if failures:
        print(f"RESULT: FAIL ({len(failures)} 项)")
        return 1
    print(f"RESULT: PASS  sha256={snap['meta']['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
