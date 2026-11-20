/* 项目0 资金流转图 —— Cytoscape.js / AntV G6 同数据对比 demo
 * 数据来自 docs/public/demo/fund-graph/data.json（由 prototypes/fund-graph/build_snapshot.py 生成）
 * 分层坐标由生成器预算，两侧引擎都按同一坐标绘制，因此两图可直接对比。
 */
(() => {
  'use strict';

  const LAYER_COLOR = ['#7d8ea6', '#e0603f', '#e79a3c', '#9a6ff0', '#2fa596', '#4d86c4'];
  const KIND_COLOR = { transfer: '#4d7ba8', service: '#b08a3e', cash: '#2fa596', wechat: '#8b7cf6' };
  const KIND_LABEL = { transfer: '转账', service: '服务费', cash: '取现', wechat: '微信' };

  const el = {
    panes: document.getElementById('panes'),
    cy: document.getElementById('cy'),
    g6: document.getElementById('g6'),
    detail: document.getElementById('detail'),
    status: document.getElementById('status'),
    head: document.getElementById('head-meta'),
    legend: document.getElementById('legend'),
  };

  const state = {
    mode: 'compare',      // compare | cy | g6
    view: 'layered',      // layered | force
    coreOnly: false,
    selected: null,       // {type:'node'|'edge', id}
    forcePos: null,
  };

  let DATA = null;
  let byId = {};
  const inst = { cy: null, g6: null };
  const timing = { cy: null, g6: null };

  const fmt = (v) => Number(v).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const fmtShort = (v) => {
    if (v >= 1e8) return (v / 1e8).toFixed(2) + ' 亿';
    if (v >= 1e4) return (v / 1e4).toFixed(2) + ' 万';
    return fmt(v);
  };

  /* ---------- 载入与派生 ---------- */

  async function boot() {
    const res = await fetch('./data.json', { cache: 'no-store' });
    DATA = await res.json();
    byId = Object.fromEntries(DATA.nodes.map((n) => [n.id, n]));
    derive();
    renderHead();
    renderLegend();
    renderDetail(null);
    wire();
    rebuildAll();
  }

  function derive() {
    const maxFlow = Math.max(...DATA.nodes.map((n) => n.in + n.out), 1);
    DATA.nodes.forEach((n) => {
      n.size = Math.max(12, Math.round(12 + 32 * Math.sqrt((n.in + n.out) / maxFlow)));
      n.color = n.layer === 0 ? LAYER_COLOR[0] : layerColor(n);
      n.short = n.layer === 0 ? n.name.replace(/\D/g, '').slice(-2) : n.name;
      n.shape = n.kind === 'atm' ? 'hexagon' : n.kind === 'merchant' ? 'diamond' : n.kind === 'wechat' ? 'round' : 'circle';
    });
    DATA.edges.forEach((e) => {
      e.kind = edgeKind(e);
      e.color = KIND_COLOR[e.kind];
      e.w = 1 + 3.2 * Math.log10(1 + e.amount / 3000);
      e.t = byId[e.target];
      e.s = byId[e.source];
    });
    state.forcePos = null;
  }

  function layerColor(n) {
    if (n.kind === 'atm') return '#2fa596';
    if (n.kind === 'merchant') return '#b08a3e';
    if (n.kind === 'wechat') return '#8b7cf6';
    return LAYER_COLOR[n.layer] || '#7d8ea6';
  }

  function edgeKind(e) {
    const s = byId[e.source], t = byId[e.target];
    if (s.kind === 'wechat' || t.kind === 'wechat') return 'wechat';
    if (t.kind === 'atm') return 'cash';
    if (t.kind === 'merchant') return 'service';
    return 'transfer';
  }

  function subgraph() {
    if (!state.coreOnly) return { nodes: DATA.nodes, edges: DATA.edges };
    const nodes = DATA.nodes.filter((n) => n.layer > 0);
    const ids = new Set(nodes.map((n) => n.id));
    return { nodes, edges: DATA.edges.filter((e) => ids.has(e.source) && ids.has(e.target)) };
  }

  function positions(nodes) {
    if (state.view === 'force') {
      if (!state.forcePos) state.forcePos = forceLayout(DATA.nodes, DATA.edges);
      return (n) => state.forcePos.get(n.id) || { x: n.x, y: n.y };
    }
    return (n) => ({ x: n.x, y: n.y });
  }

  /* 简易力导向：随机初值 → 每次结果不同，仅用于探索，不作为证据 */
  function forceLayout(nodes, edges) {
    const N = nodes.length;
    const idx = new Map(nodes.map((n, i) => [n.id, i]));
    const pos = nodes.map(() => ({ x: (Math.random() - 0.5) * 900, y: (Math.random() - 0.5) * 700 }));
    const k = Math.sqrt((900 * 700) / N) * 0.85;
    for (let it = 0; it < 260; it++) {
      const disp = pos.map(() => ({ x: 0, y: 0 }));
      for (let i = 0; i < N; i++) {
        for (let j = i + 1; j < N; j++) {
          let dx = pos[i].x - pos[j].x, dy = pos[i].y - pos[j].y;
          let d = Math.sqrt(dx * dx + dy * dy) || 0.01;
          const f = (k * k) / d;
          dx /= d; dy /= d;
          disp[i].x += dx * f; disp[i].y += dy * f;
          disp[j].x -= dx * f; disp[j].y -= dy * f;
        }
      }
      edges.forEach((e) => {
        const a = idx.get(e.source), b = idx.get(e.target);
        if (a == null || b == null) return;
        let dx = pos[b].x - pos[a].x, dy = pos[b].y - pos[a].y;
        let d = Math.sqrt(dx * dx + dy * dy) || 0.01;
        const f = ((d * d) / k) * 0.05;
        dx /= d; dy /= d;
        disp[a].x += dx * f; disp[a].y += dy * f;
        disp[b].x -= dx * f; disp[b].y -= dy * f;
      });
      const t = Math.max(0.05, 1 - it / 260);
      for (let i = 0; i < N; i++) {
        pos[i].x += disp[i].x * t * 0.05;
        pos[i].y += disp[i].y * t * 0.05;
      }
    }
    // 归一化到画布比例
    const xs = pos.map((p) => p.x), ys = pos.map((p) => p.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
    const sx = 1200 / Math.max(1, maxX - minX), sy = 800 / Math.max(1, maxY - minY);
    const s = Math.min(sx, sy);
    return new Map(nodes.map((n, i) => [
      n.id,
      { x: (pos[i].x - (minX + maxX) / 2) * s, y: (pos[i].y - (minY + maxY) / 2) * s },
    ]));
  }

  /* ---------- 头部 / 图例 ---------- */

  function renderHead() {
    const m = DATA.meta;
    el.head.innerHTML = `数据 ${m.counts.rawRows} 行 · 去重后 ${m.counts.uniqueTxns} 笔 · ${m.counts.edges} 聚合边 · ${m.counts.nodes} 节点
      <code>sha256 ${m.sha256.slice(0, 12)}…</code>`;
  }

  function renderLegend() {
    const layers = Object.entries(DATA.meta.layerNames)
      .filter(([k]) => k !== '0')
      .map(([k, v]) => `<span><i style="background:${LAYER_COLOR[k]}"></i>L${k} ${v}</span>`)
      .join('');
    const kinds = Object.entries(KIND_LABEL)
      .map(([k, v]) => `<span><span class="ln" style="background:${KIND_COLOR[k]}"></span>${v}</span>`)
      .join('');
    el.legend.innerHTML = `<span><i style="background:${LAYER_COLOR[0]}"></i>L0 被害人（数字为编号）</span>${layers}
      <span style="width:12px"></span>${kinds}`;
  }

  /* ---------- Cytoscape ---------- */

  function buildCy(sub) {
    if (inst.cy) { inst.cy.destroy(); inst.cy = null; }
    const host = el.cy;
    if (!host.clientWidth) return;
    const pos = positions(sub.nodes);
    const t0 = performance.now();
    const cy = cytoscape({
      container: host,
      elements: [
        ...sub.nodes.map((n) => ({
          group: 'nodes',
          data: { id: n.id, label: n.short, color: n.color, size: n.size, shape: n.shape },
          position: pos(n),
        })),
        ...sub.edges.map((e) => ({
          group: 'edges',
          data: { id: e.id, source: e.source, target: e.target, color: e.color, w: e.w },
        })),
      ],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'data(color)',
            width: 'data(size)',
            height: 'data(size)',
            label: 'data(label)',
            'font-size': 9,
            color: '#c7d6ea',
            'text-valign': 'bottom',
            'text-margin-y': 3,
            'text-outline-width': 2,
            'text-outline-color': '#0e1524',
            'border-width': 1.5,
            'border-color': '#0e1524',
          },
        },
        { selector: 'node[shape="hexagon"]', style: { shape: 'hexagon' } },
        { selector: 'node[shape="diamond"]', style: { shape: 'diamond' } },
        { selector: 'node[shape="round"]', style: { shape: 'round-rectangle' } },
        {
          selector: 'edge',
          style: {
            width: 'data(w)',
            'line-color': 'data(color)',
            'target-arrow-color': 'data(color)',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 0.75,
            'curve-style': 'bezier',
            opacity: 0.6,
          },
        },
        { selector: '.dim', style: { opacity: 0.08 } },
        { selector: 'node.sel', style: { 'border-width': 3, 'border-color': '#ffffff' } },
        { selector: 'edge.sel', style: { opacity: 1, width: 'data(w)' } },
      ],
      layout: { name: 'preset', fit: true, padding: 36 },
      wheelSensitivity: 0.18,
      minZoom: 0.15,
      maxZoom: 3,
      boxSelectionEnabled: false,
    });
    timing.cy = performance.now() - t0;
    cy.on('tap', 'node', (ev) => select('node', ev.target.id()));
    cy.on('tap', 'edge', (ev) => select('edge', ev.target.id()));
    cy.on('tap', (ev) => { if (ev.target === cy) select(null); });
    inst.cy = cy;
    applySelection('cy');
  }

  /* ---------- G6 ---------- */

  function buildG6(sub) {
    if (inst.g6) { inst.g6.destroy(); inst.g6 = null; }
    const host = el.g6;
    if (!host.clientWidth) return Promise.resolve();
    const pos = positions(sub.nodes);
    const t0 = performance.now();
    const graph = new G6.Graph({
      container: host,
      autoResize: true,
      data: {
        nodes: sub.nodes.map((n) => ({
          id: n.id,
          type: n.shape === 'hexagon' ? 'hexagon' : n.shape === 'diamond' ? 'diamond' : n.shape === 'round' ? 'rect' : 'circle',
          style: {
            x: pos(n).x, y: pos(n).y,
            size: n.shape === 'round' ? [n.size + 14, n.size] : n.size,
            fill: n.color,
            stroke: '#0e1524',
            lineWidth: 1.5,
            labelText: n.short,
            labelFill: '#c7d6ea',
            labelFontSize: 9,
            labelPlacement: 'bottom',
            labelOffsetY: 2,
            cursor: 'pointer',
          },
        })),
        edges: sub.edges.map((e) => ({
          id: e.id,
          source: e.source,
          target: e.target,
          style: {
            stroke: e.color,
            lineWidth: e.w,
            opacity: 0.6,
            endArrow: true,
            endArrowSize: 7,
            cursor: 'pointer',
          },
        })),
      },
      node: {
        state: {
          selected: { lineWidth: 3, stroke: '#ffffff' },
          inactive: { opacity: 0.08 },
        },
      },
      edge: {
        state: {
          selected: { opacity: 1 },
          inactive: { opacity: 0.06 },
        },
      },
      behaviors: ['zoom-canvas', 'drag-canvas', 'drag-element'],
      zoomRange: [0.15, 3],
    });
    const done = graph.render()
      .then(() => graph.fitView({ padding: 36 }))
      .then(() => { timing.g6 = performance.now() - t0; })
      .catch((err) => { console.error('G6 render failed', err); status('G6 渲染失败：' + err.message, true); });
    graph.on('node:click', (ev) => { const id = idOf(ev); if (id) select('node', id); });
    graph.on('edge:click', (ev) => { const id = idOf(ev); if (id) select('edge', id); });
    graph.on('canvas:click', (ev) => { if (idOf(ev)) return; select(null); });
    inst.g6 = graph;
    return done.then(() => applySelection('g6'));
  }

  /* ---------- 选择与详情 ---------- */

  function idOf(ev) {
    if (!ev) return null;
    const t = ev.target;
    return (t && t.id) || ev.itemId || (t && t.dataset && t.dataset.id) || null;
  }

  function select(type, id) {
    state.selected = type ? { type, id } : null;
    applySelection('cy');
    applySelection('g6');
    renderDetail(state.selected);
  }

  function applySelection(engine) {
    if (engine === 'cy') {
      const cy = inst.cy;
      if (!cy) return;
      cy.elements().removeClass('dim sel');
      const sel = state.selected;
      if (!sel) return;
      const target = cy.getElementById(sel.id);
      if (!target || target.empty()) return;
      cy.elements().addClass('dim');
      target.removeClass('dim').addClass('sel');
      if (sel.type === 'node') target.connectedEdges().removeClass('dim');
    } else {
      const g = inst.g6;
      if (!g) return;
      const sel = state.selected;
      const all = {};
      (DATA.nodes || []).forEach((n) => { all[n.id] = []; });
      DATA.edges.forEach((e) => { all[e.id] = []; });
      if (sel) {
        Object.keys(all).forEach((k) => { all[k] = ['inactive']; });
        if (all[sel.id]) all[sel.id] = ['selected'];
        if (sel.type === 'node') {
          DATA.edges.forEach((e) => {
            if (e.source === sel.id || e.target === sel.id) all[e.id] = [];
          });
        }
      }
      g.setElementState(all).catch(() => {});
    }
  }

  function renderDetail(sel) {
    const meta = DATA.meta;
    if (!sel) {
      el.detail.innerHTML = `
        <h2>数据口径</h2>
        <dl class="kv">
          <dt>原始流水</dt><dd class="num">${meta.counts.rawRows} 行（成功）</dd>
          <dt>出账行</dt><dd class="num">${meta.counts.outRows} 行 → 去重 ${meta.counts.uniqueTxns} 笔</dd>
          <dt>重复金额</dt><dd class="num">${fmt(meta.totals.duplicateAmount)}</dd>
          <dt>镜像入账</dt><dd class="num">${meta.counts.mirrorRows} 行</dd>
          <dt>孤儿入账</dt><dd class="num">${meta.counts.orphanInRows} 行（未入图）</dd>
          <dt>聚合边</dt><dd class="num">${meta.counts.edges} 条 / ${meta.counts.nodes} 节点</dd>
          <dt>去重后出账</dt><dd class="num">${fmt(meta.totals.dedupOut)}</dd>
        </dl>
        <h2 style="margin-top:16px">自检</h2>
        <div class="checks">
          ${meta.checks.map((c) => `<div class="check"><span class="${c.pass ? 'ok' : 'bad'}">${c.pass ? '✓' : '✗'}</span><span class="cl">${c.name}</span><b class="num">${fmt(c.actual)}</b></div>`).join('')}
        </div>
        <p class="hint" style="margin-top:12px">点节点或边查看角色、金额与证据 txn_id。数据哈希 <span class="mono">${meta.sha256.slice(0, 16)}…</span>，可用 <span class="mono">prototypes/fund-graph/verify_snapshot.py</span> 复算。</p>
      `;
      return;
    }
    if (sel.type === 'node') {
      const n = byId[sel.id];
      if (!n) return;
      let calcIn = 0, calcOut = 0;
      DATA.edges.forEach((e) => {
        if (e.target === n.id) calcIn += e.amount;
        if (e.source === n.id) calcOut += e.amount;
      });
      const inOk = Math.abs(calcIn - n.in) < 0.01, outOk = Math.abs(calcOut - n.out) < 0.01;
      el.detail.innerHTML = `
        <h2>${n.name}</h2>
        <dl class="kv">
          <dt>账户</dt><dd class="mono">${n.id}</dd>
          <dt>层级</dt><dd>L${n.layer} · ${DATA.meta.layerNames[n.layer]}</dd>
          <dt>角色</dt><dd>${n.role}</dd>
          <dt>入金</dt><dd class="num">${fmt(n.in)}</dd>
          <dt>出金</dt><dd class="num">${fmt(n.out)}</dd>
          <dt>复算</dt><dd>入 ${fmt(calcIn)} <span class="${inOk ? 'ok' : 'bad'}">${inOk ? '✓' : '✗'}</span> · 出 ${fmt(calcOut)} <span class="${outOk ? 'ok' : 'bad'}">${outOk ? '✓' : '✗'}</span></dd>
          <dt>流水行</dt><dd class="num">${n.txnCount}</dd>
          <dt>说明</dt><dd>${n.note || '—'}</dd>
        </dl>
        <p class="hint">「复算」= 把当前图中该节点的入/出边金额相加，与快照记录比对；两边一致说明图能对上账。</p>
      `;
    } else {
      const e = DATA.edges.find((x) => x.id === sel.id);
      if (!e) return;
      const ev = e.evidence || [];
      el.detail.innerHTML = `
        <h2>${e.s.name} → ${e.t.name}</h2>
        <dl class="kv">
          <dt>金额</dt><dd class="num">${fmt(e.amount)}</dd>
          <dt>笔数</dt><dd class="num">${e.count}</dd>
          <dt>性质</dt><dd>${e.certainty === 'observed' ? '实测边（银行/微信流水）' : '推断边'}</dd>
          <dt>首笔</dt><dd class="mono">${e.firstTs}</dd>
          <dt>末笔</dt><dd class="mono">${e.lastTs}</dd>
          <dt>类型</dt><dd>${KIND_LABEL[e.kind]}</dd>
        </dl>
        <details class="evidence" open>
          <summary>证据 txn_id（${ev.length}）</summary>
          <pre>${ev.join(', ')}</pre>
        </details>
      `;
    }
  }

  /* ---------- 状态 / 校验 ---------- */

  function status(text, isErr) {
    el.status.textContent = text || '';
    el.status.className = isErr ? 'err' : '';
  }

  function showTiming() {
    const bits = [];
    const cyMs = document.getElementById('ms-cy');
    const g6Ms = document.getElementById('ms-g6');
    if (cyMs) cyMs.textContent = timing.cy != null && paneVisible('cy') ? `${timing.cy.toFixed(0)} ms` : '';
    if (g6Ms) g6Ms.textContent = timing.g6 != null && paneVisible('g6') ? `${timing.g6.toFixed(0)} ms` : '';
    if (timing.cy != null && paneVisible('cy')) bits.push(`Cytoscape ${timing.cy.toFixed(0)} ms`);
    if (timing.g6 != null && paneVisible('g6')) bits.push(`G6 ${timing.g6.toFixed(0)} ms`);
    if (bits.length) status(bits.join(' · '));
  }

  const paneVisible = (eng) => state.mode === 'compare' || state.mode === eng;

  async function sha256(str) {
    const buf = new TextEncoder().encode(str);
    const dig = await crypto.subtle.digest('SHA-256', buf);
    return [...new Uint8Array(dig)].map((b) => b.toString(16).padStart(2, '0')).join('');
  }

  function snapshot(eng) {
    if (eng === 'cy') return inst.cy ? inst.cy.png({ scale: 1, bg: '#0e1524' }) : '';
    const c = el.g6.querySelector('canvas');
    return c ? c.toDataURL('image/png') : '';
  }

  async function nextFrame() {
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  }

  async function checkDeterminism() {
    if (state.view === 'force') {
      status('力导向视图每次布局都不同；切回「分层」再校验。', true);
      return;
    }
    const engines = ['cy', 'g6'].filter(paneVisible);
    if (!engines.length) { status('先显示至少一个引擎。', true); return; }
    status('校验中：同一快照重建两次，比较整块画布像素 …');
    const out = [];
    for (const eng of engines) {
      const a = await sha256(snapshot(eng));
      await nextFrame();
      await rebuild(eng);
      await nextFrame();
      const b = await sha256(snapshot(eng));
      out.push(`${eng === 'cy' ? 'Cytoscape' : 'G6'} ${a === b ? '✓ 同像素' : '✗ 不一致'} ${a.slice(0, 8)}`);
    }
    status('确定性校验：' + out.join(' · ') + '（预设坐标，两次重建）');
  }

  /* ---------- 重建 ---------- */

  function rebuildAll() {
    layoutPanes();
    const sub = subgraph();
    rebuild('cy', sub);
    rebuild('g6', sub).then(() => showTiming());
  }

  function rebuild(eng, sub) {
    const s = sub || subgraph();
    if (eng === 'cy') { buildCy(s); return Promise.resolve(); }
    return buildG6(s);
  }

  function layoutPanes() {
    el.panes.className = state.mode === 'compare' ? 'compare' : 'single';
    document.querySelectorAll('.pane').forEach((p) => {
      p.classList.toggle('visible', state.mode === 'compare' || p.dataset.engine === state.mode);
    });
  }

  /* ---------- 交互 ---------- */

  function wire() {
    document.querySelectorAll('[data-mode]').forEach((b) => {
      b.onclick = () => {
        state.mode = b.dataset.mode;
        syncButtons();
        rebuildAll();
      };
    });
    document.querySelectorAll('[data-view]').forEach((b) => {
      b.onclick = () => {
        state.view = b.dataset.view;
        state.forcePos = null;
        syncButtons();
        rebuildAll();
        status(state.view === 'force' ? '力导向：随机初值，每次结果不同，只用于探索' : '');
      };
    });
    document.getElementById('btn-core').onclick = () => {
      state.coreOnly = !state.coreOnly;
      document.getElementById('btn-core').classList.toggle('on', state.coreOnly);
      rebuildAll();
    };
    document.getElementById('btn-fit').onclick = () => {
      if (inst.cy) inst.cy.fit(undefined, 36);
      if (inst.g6) inst.g6.fitView({ padding: 36 }).catch(() => {});
    };
    document.getElementById('btn-check').onclick = checkDeterminism;
    let t = null;
    window.addEventListener('resize', () => {
      clearTimeout(t);
      t = setTimeout(() => {
        if (inst.cy) inst.cy.resize();
        if (inst.g6) inst.g6.resize();
      }, 150);
    });
  }

  function syncButtons() {
    document.querySelectorAll('[data-mode]').forEach((b) => b.classList.toggle('on', b.dataset.mode === state.mode));
    document.querySelectorAll('[data-view]').forEach((b) => b.classList.toggle('on', b.dataset.view === state.view));
  }

  boot().catch((err) => {
    console.error(err);
    status('加载失败：' + err.message, true);
  });

  /* 仅用于自动化验收（chrome-devtools 读取布局与选择状态） */
  window.__fundGraph = {
    get state() { return state; },
    get data() { return DATA; },
    inst,
    select,
    rebuildAll,
    checkDeterminism,
    timings: timing,
  };
})();
