"""生成「五层结构示意图」SVG（P0 示意图，数字全部来自 data.json）。

用法:
    python prototypes/fund-graph/make_layers_svg.py

输入: docs/public/demo/fund-graph/data.json（build_snapshot.py 的产物）
输出: docs/public/img/onchain/five-layers.svg

设计原则:
- 只画 8 人团伙 + 被害人池 + 外部对手，不画 55 条边（那是 demo 的交互图）；
- 每层标职责、代表账户、金额，箭头标该层间的合计金额；
- 数字先断言再画，数据变了会直接报错，避免图上写着旧数字。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs/public/demo/fund-graph/data.json"
OUT = ROOT / "docs/public/img/onchain/five-layers.svg"

W, H = 940, 690
BG = "#f7f9fc"
INK = "#1f2937"
MUTED = "#5b6b82"
LINE = "#94a3b8"

C = {
    0: "#64748b",
    1: "#e0603f",
    2: "#e79a3c",
    3: "#9a6ff0",
    4: "#1f9e8f",
    5: "#4d86c4",
}


def money(v: float) -> str:
    return f"{v:,.2f}"


def load():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in d["nodes"]}
    edges = d["edges"]
    return d, nodes, edges


def agg(nodes, edges):
    by_name = {n["name"]: n for n in nodes.values()}
    flows = {}

    def key(a, b):
        return (nodes[a]["name"], nodes[b]["name"])

    for e in edges:
        k = key(e["source"], e["target"])
        amt, cnt = flows.get(k, (0.0, 0))
        flows[k] = (amt + e["amount"], cnt + e["count"])

    def f(a: str, b: str) -> float:
        return round(flows.get((a, b), (0.0, 0))[0], 2)

    victims = [n for n in nodes.values() if n["layer"] == 0]
    l2 = [n for n in nodes.values() if n["layer"] == 2]
    merchants = [n for n in nodes.values() if n["kind"] == "merchant"]

    facts = {
        "victim_count": len(victims),
        "victim_out": round(sum(n["out"] for n in victims), 2),
        "zhang_in": round(by_name["张海涛"]["in"], 2),
        "zhang_out": round(by_name["张海涛"]["out"], 2),
        "zhang_edges_in": sum(1 for e in edges if e["target"] == by_name["张海涛"]["id"]),
        "l2_out": round(sum(n["out"] for n in l2), 2),
        "li": f("张海涛", "李国栋"),
        "wang": f("张海涛", "王丽娟"),
        "zhao": f("张海涛", "赵鹏"),
        "li_sun": f("李国栋", "孙志强"),
        "wang_sun": f("王丽娟", "孙志强"),
        "zhao_sun": f("赵鹏", "孙志强"),
        "sun_in": round(by_name["孙志强"]["in"], 2),
        "sun_zhou": f("孙志强", "周敏"),
        "sun_zheng": f("孙志强", "郑小云"),
        "sun_wu": f("孙志强", "吴刚"),
        "zhou_atm": f("周敏", "ATM 取现"),
        "atm": round(by_name["ATM 取现"]["in"], 2),
        "wu_zhang": f("吴刚", "张海涛"),
        "wu_zhou": f("吴刚", "周敏"),
        "zhou_wu": f("周敏", "吴刚"),
        "merchant_total": round(sum(n["in"] for n in merchants), 2),
        "zheng_in": round(by_name["郑小云"]["in"], 2),
        "zhou_in": round(by_name["周敏"]["in"], 2),
        "zhou_out": round(by_name["周敏"]["out"], 2),
        "wu_in": round(by_name["吴刚"]["in"], 2),
        "wu_out": round(by_name["吴刚"]["out"], 2),
        "first": min(e["firstTs"] for e in edges),
        "last": max(e["lastTs"] for e in edges),
    }
    return by_name, facts


def check(facts):
    """图上的数字必须能对上账；对不上直接失败。"""
    assert facts["victim_out"] == 426804.00, facts["victim_out"]
    assert facts["zhang_in"] == 454051.27 and facts["zhang_out"] == 454051.27
    assert facts["li"] == 240649.27 and facts["wang"] == 128041.20 and facts["zhao"] == 85360.80
    assert round(facts["li"] + facts["wang"] + facts["zhao"], 2) == 454051.27
    assert round(facts["li_sun"] + facts["wang_sun"] + facts["zhao_sun"], 2) == 405463.80
    assert facts["sun_in"] == 405463.80
    assert round(facts["sun_zhou"] + facts["sun_zheng"] + facts["sun_wu"], 2) == 405463.80
    assert facts["merchant_total"] == 21340.20
    assert round(facts["l2_out"] - facts["merchant_total"], 2) == 405463.80
    assert facts["zhou_atm"] == 192627.92 and facts["atm"] == 192627.92
    assert facts["zheng_in"] == 162185.52
    assert facts["wu_zhang"] == 27247.27
    assert round(facts["wu_zhou"] + facts["zhou_wu"], 2) == 11880.00


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_text(x, y, s, size=13, fill=INK, anchor="start", weight="400", family=None, opacity=None):
    fam = family or "PingFang SC, Microsoft YaHei, Noto Sans CJK SC, sans-serif"
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
        f'font-weight="{weight}" font-family="{fam}"{op}>{esc(s)}</text>'
    )


def box(x, y, w, h, color, title, lines, title_size=14, sub_size=11.5):
    out = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#ffffff" stroke="{color}" stroke-width="1.6"/>',
        f'<rect x="{x}" y="{y}" width="4" height="{h}" rx="2" fill="{color}"/>',
    ]
    out.append(svg_text(x + 12, y + 20, title, title_size, INK, weight="600"))
    for i, ln in enumerate(lines):
        out.append(svg_text(x + 12, y + 20 + 17 * (i + 1), ln, sub_size, MUTED))
    return out


def arrow(x1, y1, x2, y2, color, label="", lx=None, ly=None, dash=False, width=2.0, anchor="middle", size=11.5):
    dash_attr = ' stroke-dasharray="5 4"' if dash else ""
    out = [
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{dash_attr} marker-end="url(#ah)"/>'
    ]
    if label:
        out.append(svg_text(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 - 6, label, size, color, anchor=anchor, weight="600"))
    return out


def curve(x1, y1, cx, cy, x2, y2, color, label="", lx=None, ly=None, dash=True, width=1.8):
    dash_attr = ' stroke-dasharray="5 4"' if dash else ""
    out = [
        f'<path d="M{x1},{y1} C{cx},{cy} {cx},{cy} {x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}"{dash_attr} marker-end="url(#ah)"/>'
    ]
    if label:
        out.append(svg_text(lx or cx, ly or cy, label, 11.5, color, anchor="middle", weight="600"))
    return out


def build(by_name, f):
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="项目0 涉诈资金五层结构示意图">')
    p.append("<defs>")
    p.append(f'<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker>')
    p.append("</defs>")
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # 标题
    p.append(svg_text(28, 36, "项目0 涉诈资金：五层结构与收敛点", 19, INK, weight="700"))
    p.append(svg_text(28, 57, "被害人池 → 一级卡 → 二级卡 → 水房 → 取现/沉淀/回流 → 外部对手；箭头为层间合计金额（元），均可在 demo 中复算", 12, MUTED))

    # 层标签
    layers = [
        (0, 118, "L0 被害人"),
        (1, 215, "L1 收款池"),
        (2, 322, "L2 二级卡"),
        (3, 432, "L3 水房"),
        (4, 542, "L4 取现/沉淀/回流"),
        (5, 641, "L5 外部对手"),
    ]
    for lay, y, name in layers:
        p.append(f'<rect x="28" y="{y - 14}" width="78" height="24" rx="12" fill="{C[lay]}" opacity="0.12"/>')
        p.append(svg_text(67, y + 3, f"L{lay}", 12.5, C[lay], anchor="middle", weight="700"))
        p.append(svg_text(28, y + 26, name, 11, MUTED))

    # L0 被害人池
    p.extend(box(140, 82, 520, 58, C[0], f"被害人池 × {f['victim_count']}",
                  [f"合计转出 {money(f['victim_out'])}（{f['victim_count']} 个对手 / 33 笔入账到一级卡）"]))
    # L1
    p.extend(box(330, 186, 330, 62, C[1], "张海涛 · 6227…0001（一级卡 / 收款池）",
                  [f"入 {money(f['zhang_in'])}　出 {money(f['zhang_out'])}", "33 个入向对手 → 1 个账户：收敛点；出向仅 3 个"]))
    # L2
    p.extend(box(120, 296, 210, 58, C[2], "李国栋 · 6227…0002", [f"入 {money(f['li'])}", f"转孙 {money(f['li_sun'])}"]))
    p.extend(box(365, 296, 210, 58, C[2], "王丽娟 · 6227…0003", [f"入 {money(f['wang'])}", f"转孙 {money(f['wang_sun'])}"]))
    p.extend(box(610, 296, 210, 58, C[2], "赵鹏 · 6227…0004", [f"入 {money(f['zhao'])}", f"转孙 {money(f['zhao_sun'])}"]))
    # L3
    p.extend(box(330, 406, 330, 58, C[3], "孙志强 · 6227…0005（水房 / 归集）",
                  [f"入 {money(f['sun_in'])}　出 {money(f['sun_in'])}", "三张二级卡全部归集到 1 个账户"]))
    # L4
    p.extend(box(110, 516, 220, 60, C[4], "周敏 · 6227…0006（取现）",
                  [f"入 {money(f['zhou_in'])}　出 {money(f['zhou_out'])}", f"ATM 取现 {money(f['zhou_atm'])}（7 笔）"]))
    p.extend(box(360, 516, 220, 60, C[4], "郑小云 · 6227…0008（沉淀）",
                  [f"入 {money(f['zheng_in'])}　出 0.00", "只进不出，账上停住"]))
    p.extend(box(610, 516, 220, 60, C[4], "吴刚 · 6227…0007（回流）",
                  [f"入 {money(f['wu_in'])}　出 {money(f['wu_out'])}", f"退回张 {money(f['wu_zhang'])}：闭环"]))
    # L5
    p.extend(box(110, 600, 220, 54, C[5], "ATM 取现（虚拟对手）", [f"进 {money(f['atm'])}", "现金离场，链条终止"]))
    p.extend(box(610, 600, 220, 54, "#b08a3e", "3 家商户（服务费）", [f"合计 {money(f['merchant_total'])}", "鑫源 / 恒通 / 安康"]))

    # 边：L0 -> L1
    p.extend(arrow(400, 140, 455, 186, C[0], f"{money(f['victim_out'])} / 33 笔", lx=300, ly=168, anchor="end"))
    # L1 -> L2
    p.extend(arrow(430, 248, 240, 296, C[1], money(f["li"]), lx=330, ly=276, anchor="end"))
    p.extend(arrow(470, 248, 470, 296, C[1], money(f["wang"]), lx=482, ly=276, anchor="start"))
    p.extend(arrow(560, 248, 700, 296, C[1], money(f["zhao"]), lx=640, ly=276, anchor="start"))
    # L2 -> L3
    p.extend(arrow(225, 354, 420, 406, C[2], money(f["li_sun"]), lx=300, ly=386, anchor="end"))
    p.extend(arrow(470, 354, 470, 406, C[2], money(f["wang_sun"]), lx=482, ly=386, anchor="start"))
    p.extend(arrow(715, 354, 565, 406, C[2], money(f["zhao_sun"]), lx=650, ly=386, anchor="start"))
    # L3 -> L4
    p.extend(arrow(400, 464, 235, 516, C[3], money(f["sun_zhou"]), lx=305, ly=496, anchor="end"))
    p.extend(arrow(470, 464, 470, 516, C[3], money(f["sun_zheng"]), lx=482, ly=496, anchor="start"))
    p.extend(arrow(580, 464, 705, 516, C[3], money(f["sun_wu"]), lx=650, ly=496, anchor="start"))
    # 周 -> ATM
    p.extend(arrow(220, 576, 220, 600, C[4], f"{money(f['zhou_atm'])}", lx=230, ly=592, anchor="start"))
    # 吴 -> 张 回流（右侧绕行）
    p.extend(curve(830, 542, 900, 400, 665, 220, C[4], f"回流 {money(f['wu_zhang'])}", lx=880, ly=390))

    # 判读要点（放在 L5 行中间的空位，避免压线）
    p.append(svg_text(352, 606, "三个判读点", 11.5, MUTED, weight="700"))
    p.append(svg_text(352, 624, f"收敛：{f['victim_count']} 人 → 1 张卡（{f['zhang_edges_in']} 笔）", 11.5, C[1], weight="600"))
    p.append(svg_text(352, 641, "扇出：1 → 3 张二级卡", 11.5, C[2], weight="600"))
    p.append(svg_text(352, 658, "闭环：张 → 李 → 孙 → 吴 → 张", 11.5, C[4], weight="600"))

    # 底部说明
    p.append(f'<line x1="28" y1="668" x2="{W - 28}" y2="668" stroke="#dbe3ee"/>')
    p.append(svg_text(28, 682, "数据：economic_detect/examples/demo.db · case 1（项目0）　金额单位：元　去重口径：按出账行 (src, dst, 金额, 时间) 去重", 10.5, MUTED))
    return "\n".join(p) + "\n</svg>\n"


def main():
    d, nodes, edges = load()
    by_name, facts = agg(nodes, edges)
    check(facts)
    svg = build(by_name, facts)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(json.dumps({"svg": str(OUT.relative_to(ROOT)), "bytes": len(svg.encode("utf-8")), "facts": facts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
