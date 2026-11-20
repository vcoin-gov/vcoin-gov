#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 economic_detect 的示例库生成「链路可视化」演示用的确定性图快照。

口径（写进 data.json.meta.rule，页面与 demo 均引用同一段文字）：
  1. 只取银行/微信两类流水中 success=1 的行；
  2. 以出账行（dc=out）为主边：src=本方账号，dst=对方账号；
  3. 按 (src, dst, amount, ts) 去重——同一笔交易在双方流水里各出现一次，
     重复导入也会产生同键重复行，都会在这里合并；
  4. 入账行不单独入图，只用于核对镜像：若一条入账行找不到对应出账行，
     计入 meta.counts.orphanInRows，不画进图；
  5. 按 (src, dst) 聚合金额与笔数，证据保留 txn_id 列表。

用法：
  python build_snapshot.py --db ../../examples/demo.db \
      --out ../../docs/public/demo/fund-graph/data.json \
      --freeze txns.csv
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sqlite3
from collections import defaultdict

CASE_ID = 1
SRC_TYPES = ("bank", "wechat")

# 角色/层级来自 examples/项目0/示例题目与答案.md，仅用于标注，不参与金额计算。
ROLE = {
    "6227000000000001": (1, "收款池", "一级卡，33 个入向对手 / 3 个出向对手"),
    "6217000000000002": (2, "二级卡", "李国栋"),
    "6217000000000003": (2, "二级卡", "王丽娟"),
    "6217000000000004": (2, "二级卡", "赵鹏"),
    "6227000000000005": (3, "水房·归集", "405,463.80 归集后向下分发"),
    "6227000000000006": (4, "取现", "ATM 7 笔 192,627.92"),
    "6227000000000007": (4, "回流", "闭环 张→李→孙→吴→张"),
    "6227000000000008": (4, "沉淀", "只进不出"),
    "6228480000000011": (5, "外部商户", "安康商贸，只收服务费"),
    "6228480000000012": (5, "外部商户", "鑫源咨询，只收服务费"),
    "6228480000000013": (5, "外部商户", "恒通科技，只收服务费"),
    "ATM-CASH-001": (5, "ATM 取现", "虚拟对手，原始流水中对方账号为空"),
    "wxid_zhanghaitao": (1, "微信·收款", "同一人（张海涛）的微信账户"),
    "wxid_wugang": (4, "微信·回流", "同一人（吴刚）的微信账户"),
}
LAYER_NAMES = {
    0: "被害人",
    1: "一级卡 · 收款池",
    2: "二级卡",
    3: "水房 · 归集",
    4: "取现 · 沉淀 · 回流",
    5: "外部对手",
}


def norm_amount(x: float) -> float:
    return round(float(x) + 1e-9, 2)


def load_rows(db_path: str):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    sql = """
      select t.txn_id, t.batch_id, b.src_type, t.acct_key, t.acct_name, t.dc,
             t.amount, t.ts, t.summary, t.opp_key, t.opp_name
        from t_txn t join t_batch b on t.batch_id = b.batch_id
       where b.case_id = ? and t.success = 1 and b.src_type in ('bank','wechat')
       order by t.txn_id
    """
    rows = [dict(r) for r in con.execute(sql, (CASE_ID,))]
    con.close()
    return rows


def build(rows):
    outs = [r for r in rows if r["dc"] == "out"]
    ins = [r for r in rows if r["dc"] == "in"]

    nodes = {}
    name_of = {}

    def touch(acct: str, name: str | None):
        if not acct:
            return
        if acct not in nodes:
            nodes[acct] = {"id": acct, "name": name or acct, "kind": "account"}
        elif name and (not nodes[acct]["name"] or nodes[acct]["name"] == acct):
            nodes[acct]["name"] = name
            name_of[acct] = name

    # 单笔去重：同一 (src,dst,amount,ts) 只留一条，证据合并 txn_id
    single = {}
    for r in outs:
        dst = r["opp_key"] or ""
        if not dst:
            summary = (r["summary"] or "").strip()
            dst = "ATM-CASH-001" if "ATM" in summary.upper() or "取现" in summary else f"VIRT:{summary or '未知对手'}"
        src = r["acct_key"]
        key = (src, dst, norm_amount(r["amount"]), r["ts"])
        single.setdefault(key, []).append(r["txn_id"])
        touch(src, r["acct_name"])
        touch(dst, r["opp_name"])

    # 镜像核对：入账行是否有对应出账行
    orphan_in = []
    for r in ins:
        src = r["opp_key"] or ""
        key = (src, r["acct_key"], norm_amount(r["amount"]), r["ts"])
        if key not in single:
            orphan_in.append(r["txn_id"])

    # 点对聚合
    pairs = defaultdict(lambda: {"amount": 0.0, "count": 0, "first": None, "last": None, "txns": []})
    for (src, dst, amt, ts), tids in single.items():
        p = pairs[(src, dst)]
        p["amount"] += amt
        p["count"] += 1
        p["first"] = ts if p["first"] is None or ts < p["first"] else p["first"]
        p["last"] = ts if p["last"] is None or ts > p["last"] else p["last"]
        p["txns"].extend(tids)

    edges = []
    for i, ((src, dst), p) in enumerate(sorted(pairs.items())):
        edges.append({
            "id": f"E{i:03d}",
            "source": src,
            "target": dst,
            "amount": norm_amount(p["amount"]),
            "count": p["count"],
            "firstTs": p["first"],
            "lastTs": p["last"],
            "evidence": sorted(p["txns"]),
            "certainty": "observed",
        })

    # 节点出入额（来自去重后的边，可被 demo 复算）
    for n in nodes.values():
        n["in"] = 0.0
        n["out"] = 0.0
        n["txnCount"] = 0
    for e in edges:
        if e["source"] in nodes:
            nodes[e["source"]]["out"] = norm_amount(nodes[e["source"]]["out"] + e["amount"])
            nodes[e["source"]]["txnCount"] += len(e["evidence"])
        if e["target"] in nodes:
            nodes[e["target"]]["in"] = norm_amount(nodes[e["target"]]["in"] + e["amount"])
            nodes[e["target"]]["txnCount"] += len(e["evidence"])

    # 标注层级 / 类型 / 角色
    for nid, n in nodes.items():
        if nid in ROLE:
            layer, role, note = ROLE[nid]
            n.update(layer=layer, role=role, note=note)
        elif nid.startswith("62140000000001"):
            n.update(layer=0, role="被害人", note="入金来源")
        else:
            n.update(layer=5, role="其他对手", note="未归类")
        if nid.startswith("wxid_"):
            n["kind"] = "wechat"
            n["name"] = {"wxid_wugang": "吴刚（微信）", "wxid_zhanghaitao": "张海涛（微信）"}.get(nid, nid)
        elif nid.startswith("622848"):
            n["kind"] = "merchant"
        elif nid.startswith("ATM"):
            n["kind"] = "atm"
            n["name"] = "ATM 取现"
        else:
            n["kind"] = "person"

    # 确定性坐标：分层，层内按金额降序、稳定 id 次序
    by_layer = defaultdict(list)
    for n in nodes.values():
        by_layer[n["layer"]].append(n)
    y_of = {0: 40, 1: 250, 2: 430, 3: 610, 4: 790, 5: 970}
    for layer, members in by_layer.items():
        members.sort(key=lambda n: (-(n["in"] + n["out"]), n["id"]))
        if layer == 0:
            for i, n in enumerate(members):
                n["x"] = round((i // 2 - 7.5) * 110, 1)
                n["y"] = y_of[0] + (i % 2) * 90
        else:
            width = 120
            for i, n in enumerate(members):
                n["x"] = round((i - (len(members) - 1) / 2) * width, 1)
                n["y"] = y_of[layer]

    return nodes, edges, outs, ins, orphan_in, single


def sha256_of(nodes, edges) -> str:
    payload = {
        "nodes": [{k: n[k] for k in ("id", "name", "kind", "layer", "role", "in", "out", "x", "y")} for n in sorted(nodes.values(), key=lambda n: n["id"])],
        "edges": [{k: e[k] for k in ("id", "source", "target", "amount", "count", "firstTs", "lastTs")} for e in sorted(edges, key=lambda e: e["id"])],
    }
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--freeze", default=None, help="把 case 1 的原始行冻结成 CSV")
    ap.add_argument("--source-label", default="demo.db", help="写进 meta 的来源文件名")
    args = ap.parse_args()

    rows = load_rows(args.db)
    nodes, edges, outs, ins, orphan_in, single = build(rows)

    raw_out = norm_amount(sum(r["amount"] for r in outs))
    dedup_out = norm_amount(sum(e["amount"] for e in edges))
    zhang = nodes.get("6227000000000001", {})
    checks = [
        {"name": "张海涛入金 = 454,051.27", "expected": 454051.27, "actual": zhang.get("in"), "pass": zhang.get("in") == 454051.27},
        {"name": "张海涛出金 = 454,051.27", "expected": 454051.27, "actual": zhang.get("out"), "pass": zhang.get("out") == 454051.27},
        {"name": "原始出账合计 = 2,064,875.26", "expected": 2064875.26, "actual": raw_out, "pass": raw_out == 2064875.26},
        {"name": "去重后出账合计 = 2,004,878.26", "expected": 2004878.26, "actual": dedup_out, "pass": dedup_out == 2004878.26},
        {"name": "账户数（不含虚拟 ATM）= 45", "expected": 45, "actual": sum(1 for n in nodes.values() if n["kind"] != "atm"), "pass": sum(1 for n in nodes.values() if n["kind"] != "atm") == 45},
    ]
    if not all(c["pass"] for c in checks):
        failed = [c["name"] for c in checks if not c["pass"]]
        raise SystemExit("checks failed: " + "; ".join(failed))

    data = {
        "meta": {
            "title": "项目0 · 涉诈资金流转（五层结构）",
            "source": "economic_detect/examples/demo.db · t_case.case_id=1（项目0）",
            "generatedFrom": args.source_label,
            "rule": "出账行为主边；按 (src,dst,金额,时间) 去重；入账行只核对镜像；按点对聚合金额，保留 txn_id 证据。",
            "layerNames": LAYER_NAMES,
            "counts": {
                "rawRows": len(rows),
                "outRows": len(outs),
                "inRows": len(ins),
                "mirrorRows": len(ins) - len(orphan_in),
                "orphanInRows": len(orphan_in),
                "uniqueTxns": len(single),
                "edges": len(edges),
                "nodes": len(nodes),
            },
            "totals": {
                "rawOut": raw_out,
                "dedupOut": dedup_out,
                "duplicateAmount": norm_amount(raw_out - dedup_out),
                "zhangIn": zhang.get("in"),
                "zhangOut": zhang.get("out"),
            },
            "checks": checks,
            "sha256": sha256_of(nodes, edges),
        },
        "nodes": sorted(nodes.values(), key=lambda n: (n["layer"], n["id"])),
        "edges": edges,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")

    if args.freeze:
        cols = ["txn_id", "batch_id", "src_type", "acct_key", "acct_name", "dc", "amount", "ts", "summary", "opp_key", "opp_name"]
        os.makedirs(os.path.dirname(os.path.abspath(args.freeze)), exist_ok=True)
        with open(args.freeze, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, "") for c in cols})

    print(json.dumps({
        "nodes": len(nodes), "edges": len(edges),
        "rawOut": raw_out, "dedupOut": dedup_out, "dup": norm_amount(raw_out - dedup_out),
        "zhangIn": zhang.get("in"), "zhangOut": zhang.get("out"),
        "orphanIn": len(orphan_in), "sha256": data["meta"]["sha256"][:16],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
