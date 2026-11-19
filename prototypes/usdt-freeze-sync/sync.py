#!/usr/bin/env python3
"""USDT/USDC 冻结黑名单重建原型（检测模型页排期 P1，2026-11-19）。

从发行方合约事件重建"当前黑名单"，不依赖第三方名单：
  - Ethereum  USDT  0xdAC17F958D2ee523a2206206994597C13D831ec7  AddedBlackList/RemovedBlackList
  - Ethereum  USDC  0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48  Blacklisted/UnBlacklisted
  - TRON      USDT  TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t          AddedBlackList/RemovedBlackList

数据通道（均免 Key）：
  - EVM: Blockscout v2 (https://eth.blockscout.com)   ——如配置 ETHERSCAN_API_KEY 则走 Etherscan v2
  - TRON: TronGrid v1 events API

事件 topic0 常量取自 prettydeath/wallet-attribution（MIT）经人工核读转录；
合约地址与事件名可对照 Etherscan/TronScan 合约页复核。

仅输出线索与证据（地址、区块、交易哈希），不做任何定性结论。
用法：
    python sync.py            # 全部三条链路
    python sync.py --tron     # 仅 TRON
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data"
UA = {"User-Agent": "vcoin-gov-prototype/0.1 (research; contact via repo)"}

# 支持 HTTP(S)_PROXY 环境变量（本机代理为 http://127.0.0.1:7893 时直连不稳）
_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
_opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"https": _proxy, "http": _proxy} if _proxy else {})
)

TRONGRID = "https://api.trongrid.io"
ROUTESCAN = "https://api.routescan.io/v2/network/mainnet/evm/1/etherscan/api"
BLOCKSCOUT = "https://eth.blockscout.com/api"
ETHERSCAN = "https://api.etherscan.io/v2/api?chainid=1"

EVM_BLACKLISTS = [
    # (token, issuer, contract, add-topic0, remove-topic0, start block)
    ("USDT", "Tether", "0xdAC17F958D2ee523a2206206994597C13D831ec7",
     "0x42e160154868087d6bfdc0ca23d96a1c1cfa32f1b72ba9ba27b69b98a0d819dc",
     "0xd7e9ec6e6ecd65492dce6bf513cd6867560d49544421d0783ddf06e76c24470c",
     4634748),
    ("USDC", "Circle", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
     "0xffa4e6181777692565cf28528fc88fd1516ea86b56da075235fa575af6a4b855",
     "0x117e3210bb9aa7d9baff172026820255c6f6c30ba8999d1c2fd88e2848137c4e",
     6082465),
]
TRON_USDT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def get_json(url, tries=6, pause_base=2):
    """带指数退避与 429 尊重的 GET；Blockscout 无 Key 窗口较窄，耐心一点。"""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with _opener.open(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            wait = min(2 ** (i + 2), 90)
            ra = (e.headers or {}).get("Retry-After", "")
            if e.code == 429 and ra.strip().isdigit():
                wait = min(int(ra) + 1, 90)
            sys.stderr.write(f"  HTTP {e.code}, retry {i+1}/{tries} in {wait}s\n")
            time.sleep(wait)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ConnectionResetError) as e:
            wait = min(2 ** (i + 2), 60)
            sys.stderr.write(f"  {e}, retry {i+1}/{tries} in {wait}s\n")
            time.sleep(wait)
    raise RuntimeError(f"giving up on {url[:140]}")


def tron_b58(hex_addr: str) -> str:
    """41 前缀 hex -> base58check（T…）"""
    raw = bytes.fromhex("41" + hex_addr[-40:])
    chk = hashlib.sha256(hashlib.sha256(raw).digest()).digest()[:4]
    n = int.from_bytes(raw + chk, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = _B58[r] + s
    return s


# ---------------- TRON ----------------

def tron_events(event_name: str):
    """TronGrid v1 events，按时间正序翻页到尽。"""
    out, url = [], (f"{TRONGRID}/v1/contracts/{TRON_USDT}/events?"
                    f"event_name={event_name}&limit=200&order_by=block_timestamp,asc")
    while url:
        d = get_json(url)
        data = d.get("data") or []
        out.extend(data)
        url = (d.get("meta") or {}).get("links", {}).get("next")
        if url:
            time.sleep(0.3)
    return out


def tron_addr_from_event(ev: dict) -> str | None:
    """AddedBlackList(address indexed)：地址在 topic1；老索引格式可能在 data。"""
    t = ev.get("topics") or []
    raw = t[1] if len(t) > 1 and t[1] else (ev.get("result", {}) or {}).get("0") or ev.get("data")
    if not raw:
        return None
    hex20 = raw[-40:]
    if set(hex20.lower()) <= set("0123456789abcdef") and len(hex20) == 40:
        return tron_b58(hex20)
    return None


def tron_blacklist():
    recs, seq = {}, []
    for kind, name in (("add", "AddedBlackList"), ("remove", "RemovedBlackList")):
        for ev in tron_events(name):
            addr = tron_addr_from_event(ev)
            if not addr:
                continue
            seq.append({"kind": kind, "address": addr,
                        "block": ev.get("block_number"),
                        "ts": ev.get("block_timestamp"),
                        "tx": ev.get("transaction_id")})
        time.sleep(0.3)
    for e in sorted(seq, key=lambda x: (x["block"] or 0)):
        if e["kind"] == "add":
            recs[e["address"].lower()] = e
        else:
            recs.pop(e["address"].lower(), None)
    print(f"TRON USDT: 事件 {len(seq)} 条 -> 当前黑名单 {len(recs)} 个地址")
    return {"chain": "tron", "contract": TRON_USDT, "token": "USDT", "issuer": "Tether",
            "events_total": len(seq), "blacklisted": sorted(recs.values(), key=lambda x: x["address"])}


# ---------------- EVM ----------------

def _hex(v):
    return int(v, 16) if v and v != "0x" else 0


def _topic_addr(log):
    t = log.get("topics") or []
    word = t[1] if len(t) > 1 and t[1] else log.get("data", "")
    return "0x" + word[-40:].lower()


def eth_logs(contract: str, topics: tuple, start: int, end: int | None = None):
    """EVM 日志：Etherscan 兼容 getLogs，1000 条/页，按块正序续读。
    通道优先级：ETHERSCAN_API_KEY > Routescan（免 Key，实测支持大范围与 offset=1000）
    > Blockscout（免 Key 但强节流，作兜底）。
    两个事件用 topic0 OR 合并为一次调用，减少请求数。"""
    key = os.environ.get("ETHERSCAN_API_KEY", "").strip()
    if key:
        api, page_limit = f"{ETHERSCAN}&apikey={key}&", 1000
    else:
        api, page_limit = f"{ROUTESCAN}?", 1000
    end = end or 0  # 0 表示 latest
    seen, out, frm, pages = set(), [], start, 0
    while True:
        params = [("module", "logs"), ("action", "getLogs"),
                  ("fromBlock", frm), ("toBlock", end or "latest"),
                  ("address", contract), ("topic0", topics[0]),
                  ("offset", str(page_limit)), ("page", "1")]
        if len(topics) > 1:
            params += [("topic0", topics[1]), ("topic0_1_opr", "or")]
        d = get_json(api + urllib.parse.urlencode(params))
        msg = str(d.get("message") or "")
        res = d.get("result") if isinstance(d.get("result"), list) else []
        if not res:
            if "no records" in msg.lower() or "no logs" in msg.lower() or msg == "OK":
                return out
            sys.stderr.write(f"  getLogs: {msg[:60]!r}\n")
            return out
        fresh = [l for l in res if (l.get("transactionHash"), l.get("logIndex")) not in seen]
        for l in fresh:
            seen.add((l.get("transactionHash"), l.get("logIndex")))
        out.extend(fresh)
        pages += 1
        if pages % 10 == 0:
            sys.stderr.write(f"  {contract[:10]}… 第 {pages} 页，累计 {len(out)} 条\n")
        if len(res) < page_limit or not fresh:
            return out
        frm = max(_hex(l.get("blockNumber")) for l in res)
        time.sleep(0.4 if not key else 0.25)


def evm_blacklists(recent_blocks: int = 0):
    """recent_blocks>0 时只扫最近 N 块（用于快速演练）；默认全历史。"""
    recs = []
    for token, issuer, contract, add_t, rem_t, start in EVM_BLACKLISTS:
        end = None
        if recent_blocks > 0:
            d = get_json(f"{ROUTESCAN}?module=block&action=eth_block_number")
            latest = int(d["result"], 16)
            start = max(start, latest - recent_blocks)
            end = latest
        logs_add = eth_logs(contract, (add_t,), start, end)
        logs_rm = eth_logs(contract, (rem_t,), start, end)
        logs = logs_add + logs_rm
        events = []
        for l in logs:
            t0 = (l.get("topics") or [""])[0].lower()
            kind = "add" if t0 == add_t.lower() else ("remove" if t0 == rem_t.lower() else None)
            if not kind:
                continue
            events.append((_hex(l.get("blockNumber")), _hex(l.get("logIndex") or "0x0"),
                           kind, _topic_addr(l), l.get("transactionHash")))
        current = {}
        for blk, _, kind, addr, tx in sorted(events):
            if kind == "add":
                current[addr.lower()] = {"address": addr, "block": blk, "tx": tx}
            else:
                current.pop(addr.lower(), None)
        print(f"EVM {token}: 事件 {len(events)} 条 -> 当前黑名单 {len(current)} 个地址"
              f"（块 {start}–{end if end else 'latest'}）")
        for e in current.values():
            recs.append({"chain": "ethereum", "contract": contract, "token": token,
                         "issuer": issuer,
                         "scope": f"blocks {start}-{end or 'latest'}", **e})
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tron", action="store_true", help="仅 TRON")
    ap.add_argument("--eth-recent", type=int, default=0,
                    metavar="N", help="EVM 只扫最近 N 块（演练用；默认 0=全历史）")
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    now = time.strftime("%Y-%m-%d %H:%M:%S %z")
    payload = {"generated_at": now,
               "note": "重建自发行方合约事件；线索非定性结论；EVM 无 Key 时受限窗口",
               "chains": []}
    if args.tron:
        payload["chains"].append(tron_blacklist())
    else:
        payload["chains"].extend(evm_blacklists(args.eth_recent))
        payload["chains"].append(tron_blacklist())
    out_file = OUT / "freeze_blacklist.json"
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(len(c.get("blacklisted", [])) for c in payload["chains"])
    for c in payload["chains"]:
        if "blacklisted" not in c:
            total += 1
    print(f"输出 {out_file}")
    by = {}
    for c in payload["chains"]:
        k = f"{c['chain']} {c.get('token','')}"
        by[k] = by.get(k, 0) + (len(c["blacklisted"]) if "blacklisted" in c else 1)
    for k, n in by.items():
        print(f"  {k}: {n} 条")
    print(f"合计 {sum(by.values())} 条")


if __name__ == "__main__":
    main()
