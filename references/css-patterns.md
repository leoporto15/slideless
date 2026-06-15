# CSS Patterns — slideless

Biblioteca de padrões copy-paste para todos os modelos. Cada bloco é standalone e respeita os tokens de `design-system.md`. **Ler antes de gerar HTML com componentes novos.**

---

## 1. Tratamento de fundo — DECISÃO do parti, nunca default

> v4: a regra antiga ("backgrounds planos parecem mortos") está REVOGADA — ela produziu o glow universal que virou o fingerprint da casa. **Flat é opção legítima e é a escolha certa para report, registro impresso e qualquer documento destinado a PDF.** O tratamento é o eixo `superficie` do bloco `<!-- slideless:parti -->` ([direcao-de-arte.md](direcao-de-arte.md)) — cardápio completo lá (inclui grain feTurbulence em data-URI e pauta de linhas). Os padrões abaixo são as implementações de referência.

### 1a. Flat (registro impresso/sóbrio)
```css
body { background: var(--color-bg); }
/* a decisão visual está no fio, no espaço e no contraste — não no fundo */
```

### 1b. Radial glow — LOCALIZADO (máx 1 por documento, atrás de UM elemento)
```css
/* NUNCA em body::before incondicional (anti-pattern C8). Posicionar atrás
   do elemento-herói que o parti declarou: */
.hero-data { position: relative; }
.hero-data::before {
  content: ''; position: absolute; inset: -20% -10%;
  background: radial-gradient(ellipse 80% 70% at 50% 40%, var(--color-accent-dim) 0%, transparent 60%);
  pointer-events: none; z-index: -1;
}
```

### 1c. Dot grid (blueprint / técnico)
```css
body {
  background-color: var(--color-bg);
  background-image: radial-gradient(circle, var(--color-border) 1px, transparent 1px);
  background-size: 24px 24px;
}
```

### 1d. Diagonal lines (editorial sutil)
```css
body {
  background-color: var(--color-bg);
  background-image: repeating-linear-gradient(
    -45deg,
    transparent,           transparent 40px,
    var(--color-border)    40px,
    var(--color-border)    41px
  );
}
```

### 1e. Grain (feTurbulence em data-URI — quente/editorial, custo zero de rede)
```css
:root { --grain: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
body::after { content: ''; position: fixed; inset: 0; background: var(--grain);
  opacity: .06; mix-blend-mode: soft-light; pointer-events: none; z-index: 9999; }
@media print { body::after { display: none; } }
```

### 1f. Pauta de linhas (noticioso / despacho)
```css
body {
  background-color: var(--color-bg);
  background-image: repeating-linear-gradient(to bottom,
    transparent, transparent 31px, var(--color-border) 31px, var(--color-border) 32px);
}
```

---

## 2. Depth Tier Cards (`ve-card`)

O sistema de três profundidades sinaliza importância sem cores flashy. **Nunca usar `.node` como class** — Mermaid usa internamente.

```css
/* Base */
.ve-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5) var(--space-6);
  position: relative;
  transition: box-shadow var(--duration-fast) var(--ease-out),
              border-color var(--duration-fast) var(--ease-out);
}

/* Tier 1 — Hero (executive summary, focal element) */
.ve-card--hero {
  background: color-mix(in srgb, var(--color-bg-elevated) 92%, var(--color-accent) 8%);
  box-shadow: var(--shadow-lg);
  border-color: color-mix(in srgb, var(--color-border) 50%, var(--color-accent) 50%);
  border-top: 2px solid var(--color-accent);
  padding: var(--space-7) var(--space-7);
}

/* Tier 2 — Default (body content) */
/* = .ve-card base */

/* Tier 3 — Recessed (code blocks, secondary, details) */
.ve-card--recessed {
  background: var(--color-bg-sunken);
  box-shadow: var(--inset-sm);
  border-color: var(--color-border);
}

/* Color accent variants (left border) */
.ve-card--accent  { border-left: 3px solid var(--color-accent); }
.ve-card--info    { border-left: 3px solid var(--color-info); }
.ve-card--success { border-left: 3px solid var(--color-success); }
.ve-card--sage    { border-left: 3px solid var(--color-sage); }
.ve-card--teal    { border-left: 3px solid var(--color-teal); }
.ve-card--plum    { border-left: 3px solid var(--color-plum); }

/* Hover — POR PAPEL, nunca universal (tell hover-lift do vocabulário nao-vai-ter).
   Card informativo não-clicável: NENHUM hover transform.
   Card clicável: escolher 1 affordance por documento: */
.ve-card--clickable:hover { border-color: var(--color-border-strong); }          /* contraste  */
.ve-card--clickable.aff-draw:hover { box-shadow: inset 0 -2px 0 var(--color-accent); } /* border-draw */
/* translateY(-Npx) como hover: APENAS card clicável E APENAS perfil de motion
   cinemático declarado no parti — nunca como default. */
```

### Label monospace dentro de card — QUOTA: 1 papel por documento
O label mono-uppercase era O tique da casa. Permitido em no máximo 1 papel por documento (kicker de seção OU th de tabela OU data de timeline). Alternativas no cardápio de labels de [direcao-de-arte.md §7](direcao-de-arte.md): small-caps com tracking, numeral de seção em serif, fio lateral.
```css
.ve-card__label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--color-fg-muted);
  margin: 0 0 var(--space-3);
  display: flex;
  align-items: center;
  gap: 8px;
}

.ve-card__label::before {
  content: '';
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

/* Color variants para label */
.ve-card--accent  .ve-card__label { color: var(--color-accent); }
.ve-card--info    .ve-card__label { color: var(--color-info); }
.ve-card--success .ve-card__label { color: var(--color-success); }
.ve-card--sage    .ve-card__label { color: var(--color-sage); }
.ve-card--teal    .ve-card__label { color: var(--color-teal); }
.ve-card--plum    .ve-card__label { color: var(--color-plum); }
```

---

## 3. Data Tables

Usar `<table>` semântico — nunca ASCII boxes. Threshold: 4+ linhas OU 3+ colunas → gerar HTML table.

```css
/* Wrapper responsivo */
.table-wrap {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--size-small);
}

/* Sticky header */
.data-table thead {
  position: sticky;
  top: 0;
  z-index: 2;
}

.data-table th {
  background: var(--color-bg-sunken);
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 2px solid var(--color-border-strong);
  color: var(--color-fg-muted);
  white-space: nowrap;
}

.data-table td {
  padding: 13px 16px;
  border-bottom: 1px solid var(--color-border);
  vertical-align: top;
  color: var(--color-fg);
  line-height: 1.45;
}

/* Alternating rows */
.data-table tbody tr:nth-child(even) {
  background: var(--color-bg-sunken);
}

.data-table tbody tr:hover {
  background: var(--color-accent-dim);
}

/* Última linha sem borda */
.data-table tbody tr:last-child td {
  border-bottom: none;
}

/* Colunas numéricas */
.data-table td.num, .data-table th.num {
  text-align: right;
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-size: var(--size-small);
}

/* Primeira coluna sticky (tabelas largas) */
.data-table td:first-child,
.data-table th:first-child {
  font-weight: 600;
}
.data-table.sticky-col td:first-child,
.data-table.sticky-col th:first-child {
  position: sticky;
  left: 0;
  background: inherit;
  z-index: 1;
  box-shadow: 1px 0 0 var(--color-border);
}

/* Footer de agregação */
.data-table tfoot td {
  font-weight: 700;
  border-top: 2px solid var(--color-border-strong);
  background: var(--color-bg-sunken);
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}

/* Status badges — nunca emoji */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 6px;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.badge::before {
  content: '';
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}
.badge--accent  { background: var(--color-accent-dim);  color: var(--color-accent); }
.badge--info    { background: var(--color-info-dim);    color: var(--color-info); }
.badge--success { background: var(--color-success-dim); color: var(--color-success); }
.badge--sage    { background: var(--color-sage-dim);    color: var(--color-sage); }
.badge--teal    { background: var(--color-teal-dim);    color: var(--color-teal); }
.badge--plum    { background: var(--color-plum-dim);    color: var(--color-plum); }
.badge--warn    { background: var(--color-warn-dim);    color: var(--color-warn); }
.badge--danger  { background: var(--color-danger-dim);  color: var(--color-danger); }
```

---

## 4. Mermaid Zoom Controls

Todo diagrama Mermaid precisa de zoom/pan. Copiar estrutura HTML + CSS + JS abaixo.

### HTML
```html
<div class="diagram-shell">
  <div class="zoom-controls" aria-label="Controles do diagrama">
    <button class="zoom-btn" data-action="zoom-in"  title="Ampliar (+)">+</button>
    <button class="zoom-btn" data-action="zoom-out" title="Reduzir (-)">−</button>
    <button class="zoom-btn" data-action="zoom-fit" title="Ajustar ao container">↻</button>
    <button class="zoom-btn" data-action="zoom-one" title="100%">1:1</button>
    <button class="zoom-btn" data-action="zoom-exp" title="Expandir em nova aba">⛶</button>
    <span class="zoom-label" aria-live="polite">100%</span>
  </div>
  <div class="mermaid-viewport">
    <div class="mermaid mermaid-canvas">
      graph TD
        A --> B
    </div>
  </div>
</div>
```

### CSS
```css
.diagram-shell {
  position: relative;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin: var(--space-6) 0;
}

.zoom-controls {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 4px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 4px 6px;
  box-shadow: var(--shadow-sm);
}

.zoom-btn {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  font: inherit;
  font-size: 0.875rem;
  color: var(--color-fg-muted);
  transition: background-color var(--duration-fast), border-color var(--duration-fast), color var(--duration-fast);
}
.zoom-btn:hover {
  background: var(--color-bg-sunken);
  border-color: var(--color-border);
  color: var(--color-fg);
}

.zoom-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--color-fg-subtle);
  padding: 0 4px;
  min-width: 36px;
  text-align: center;
}

.mermaid-viewport {
  width: 100%;
  min-height: 280px;
  overflow: hidden;
  cursor: grab;
  touch-action: none;
}
.mermaid-viewport.is-panning { cursor: grabbing; }

.mermaid-canvas {
  display: inline-block;
  transform-origin: top left;
  padding: 24px;
}

.mermaid-canvas svg {
  max-width: none !important;
  display: block;
}
```

### JavaScript (Mermaid Zoom Engine — ~180 linhas)
```js
(function initMermaidZoom() {
  const STEP = 0.15;
  const MIN_ZOOM = 0.3;
  const MAX_ZOOM = 4.0;

  document.querySelectorAll('.diagram-shell').forEach(shell => {
    const viewport = shell.querySelector('.mermaid-viewport');
    const canvas   = shell.querySelector('.mermaid-canvas');
    const label    = shell.querySelector('.zoom-label');
    if (!viewport || !canvas) return;

    let scale = 1.0;
    let panX  = 0;
    let panY  = 0;
    let isPanning = false;
    let startX, startY, startPanX, startPanY;

    function applyTransform() {
      canvas.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
      if (label) label.textContent = Math.round(scale * 100) + '%';
    }

    function fitToContainer() {
      const svg = canvas.querySelector('svg');
      if (!svg) return;
      const vW = viewport.clientWidth;
      const vH = viewport.clientHeight || 400;
      const cW = svg.getBoundingClientRect().width  / scale;
      const cH = svg.getBoundingClientRect().height / scale;
      scale = Math.min(vW / (cW + 48), vH / (cH + 48), 1.0);
      panX = (vW - cW * scale) / 2;
      panY = (vH - cH * scale) / 2;
      applyTransform();
    }

    shell.querySelectorAll('.zoom-btn').forEach(btn => {
      btn.addEventListener('click', e => {
        const action = btn.dataset.action;
        if (action === 'zoom-in')  { scale = Math.min(MAX_ZOOM, scale + STEP); applyTransform(); }
        if (action === 'zoom-out') { scale = Math.max(MIN_ZOOM, scale - STEP); applyTransform(); }
        if (action === 'zoom-fit') { fitToContainer(); }
        if (action === 'zoom-one') { scale = 1; panX = 0; panY = 0; applyTransform(); }
        if (action === 'zoom-exp') {
          const svg = canvas.querySelector('svg');
          if (!svg) return;
          const win = window.open('', '_blank');
          win.document.write(`<!DOCTYPE html><html><body style="margin:0;background:#fff">${svg.outerHTML}</body></html>`);
          win.document.close();
        }
        e.stopPropagation();
      });
    });

    /* Ctrl/Cmd + scroll to zoom */
    viewport.addEventListener('wheel', e => {
      if (!e.ctrlKey && !e.metaKey) return;
      e.preventDefault();
      const delta = e.deltaY < 0 ? STEP : -STEP;
      const prevScale = scale;
      scale = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, scale + delta));
      const rect  = viewport.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      panX = mouseX - (mouseX - panX) * (scale / prevScale);
      panY = mouseY - (mouseY - panY) * (scale / prevScale);
      applyTransform();
    }, { passive: false });

    /* Drag to pan */
    viewport.addEventListener('pointerdown', e => {
      if (e.target.closest('.zoom-controls')) return;
      isPanning = true;
      startX = e.clientX; startY = e.clientY;
      startPanX = panX; startPanY = panY;
      viewport.setPointerCapture(e.pointerId);
      viewport.classList.add('is-panning');
    });
    viewport.addEventListener('pointermove', e => {
      if (!isPanning) return;
      panX = startPanX + (e.clientX - startX);
      panY = startPanY + (e.clientY - startY);
      applyTransform();
    });
    viewport.addEventListener('pointerup',  () => { isPanning = false; viewport.classList.remove('is-panning'); });
    viewport.addEventListener('pointercancel', () => { isPanning = false; viewport.classList.remove('is-panning'); });

    /* Auto-fit after Mermaid renders */
    const observer = new MutationObserver(() => {
      if (canvas.querySelector('svg')) { observer.disconnect(); setTimeout(fitToContainer, 100); }
    });
    observer.observe(canvas, { childList: true, subtree: true });
    if (canvas.querySelector('svg')) setTimeout(fitToContainer, 100);
  });
})();
```

### Mermaid init (tema dinâmico)
```js
const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
mermaid.initialize({
  startOnLoad: true,
  theme: 'base',
  look: 'classic',
  themeVariables: {
    fontFamily: "'Inter', system-ui, sans-serif",
    fontSize: '15px',
    primaryColor:       isDark ? '#2a1e0e' : '#fff8f0',
    primaryBorderColor: isDark ? '#f88104' : '#FF6200',
    primaryTextColor:   isDark ? '#ede5dd' : '#292017',
    secondaryColor:     isDark ? '#1a2234' : '#eff6ff',
    secondaryBorderColor: isDark ? '#3B85FA' : '#3B85FA',
    tertiaryColor:      isDark ? '#1c2a1c' : '#f0fdf4',
    tertiaryBorderColor: isDark ? '#4d7c0f' : '#4d7c0f',
    lineColor:          isDark ? '#786e62' : '#8a7e72',
    noteBkgColor:       isDark ? '#1c1814' : '#faf7f5',
    noteTextColor:      isDark ? '#ede5dd' : '#292017',
    noteBorderColor:    isDark ? '#786e62' : '#d4cec3',
  }
});
```

---

## 5. Chart.js Patterns

CDN: `<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>`

### 5.0 Bloco de defaults — OBRIGATÓRIO antes do primeiro `new Chart()`

O Chart.js sem este bloco renderiza na Helvetica default com formatação en-US ("1,234.5") — o tell de IA mais imediato e mais barato de matar. Colar UMA vez, antes de qualquer gráfico:

```js
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

// Fonte e cor do DOCUMENTO, nunca o default da lib
Chart.defaults.font.family = css('--font-ui') || css('--font-text');
Chart.defaults.font.size = 12;
Chart.defaults.color = css('--color-fg-muted');

// Formatação numérica pt-BR — consistente com o texto do documento
// ("22.3%" no tick e "22,3%" no corpo é tell maior que qualquer fonte)
const fmtBR  = (v, dec = 0) => v.toLocaleString('pt-BR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
const fmtBRL = (v, suf = '') => 'R$ ' + fmtBR(v, v % 1 ? 1 : 0) + (suf ? ' ' + suf : '');
// uso: ticks: { callback: v => fmtBRL(v, 'bi') }  →  "R$ 1,2 bi"

// Tooltip tematizado (não o chrome default)
Chart.defaults.plugins.tooltip.backgroundColor = css('--color-bg-elevated');
Chart.defaults.plugins.tooltip.titleColor = css('--color-fg');
Chart.defaults.plugins.tooltip.bodyColor = css('--color-fg-muted');
Chart.defaults.plugins.tooltip.borderColor = css('--color-border-strong');
Chart.defaults.plugins.tooltip.borderWidth = 1;
```

### 5.0b Guard de CDN — OBRIGATÓRIO sempre que houver gráfico

O Chart.js vem de **CDN externo**. Em rede corporativa/intranet que bloqueia `cdn.jsdelivr.net` (cenário real do banco), `Chart` fica `undefined` e a PRIMEIRA linha `Chart.defaults…` lança `ReferenceError` que **mata o script inteiro** — o documento todo deixa de inicializar (slides não navegam, não só o gráfico some). Blindar SEMPRE: testar `Chart` antes de tocar nele e dar um fallback visível no lugar do canvas.

```js
const CHART_OK = (typeof Chart !== 'undefined');
if (CHART_OK) {
  Chart.defaults.font.family = css('--font-ui') || css('--font-text');
  /* …resto do bloco §5.0 (defaults + tooltip)… */
} else {
  // fallback digno: o leitor entende o porquê, não vê um retângulo em branco
  document.querySelectorAll('canvas[id^="chart-"]').forEach(c => {
    const note = document.createElement('p');
    note.style.cssText = 'color:var(--color-fg-muted);font-size:.95rem;text-align:center;padding:3rem 1rem';
    note.textContent = 'Gráfico indisponível offline (requer Chart.js via internet).';
    c.parentNode && c.parentNode.replaceChild(note, c);
  });
}

// fmtBR/fmtBRL ficam FORA do guard (não dependem do Chart) — usados em callbacks de tick
const fmtBR  = (v, dec = 0) => v.toLocaleString('pt-BR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
const fmtBRL = (v, suf = '') => 'R$ ' + fmtBR(v, v % 1 ? 1 : 0) + (suf ? ' ' + suf : '');

// cada função de render guarda também:
function renderChartX() { const el = document.getElementById('chart-x'); if (!el || !CHART_OK) return; /* new Chart… */ }
```

**Regra:** nenhum `new Chart()` sem o guard `typeof Chart !== 'undefined'`. Offline, o documento continua navegável e cada gráfico vira a nota de fallback — nunca um canvas em branco nem o script morto. O validador sinaliza `P5b-chart-no-guard`.

**Regras de design de dados (somam-se às de fidelidade abaixo):**
- `tension`: **0 para medições discretas/regulatórias/financeiras** (trimestres, saldos, índices oficiais); ≤0.3 apenas para narrativa contínua. Nunca 0.4 por omissão.
- `borderRadius` em barras: 0 por default — radius em barra é decisão declarada, não herança.
- **≤3 séries → legenda default PROIBIDA**: usar rotulagem direta no fim da linha (plugin abaixo).
- O **gráfico-tese** do documento tem ≥1 anotação desenhada (linha de referência, banda de evento ou label no ponto-chave que o texto narra).
- Ticks numéricos herdam `tabular-nums` visualmente: usar a MESMA formatação pt-BR do texto.
- Re-render no toggle de tema (os `css()` são lidos na criação — escutar o evento de tema e `chart.update()`).

### 5.0a Plugin de direct-label (copiar, não reescrever)

```js
// Rotula cada série no fim da linha — substitui a legenda quando ≤3 séries
const directLabel = {
  id: 'directLabel',
  afterDatasetsDraw(chart) {
    const { ctx } = chart;
    chart.data.datasets.forEach((ds, i) => {
      const meta = chart.getDatasetMeta(i);
      if (!meta.data.length || meta.hidden) return;
      const last = meta.data[meta.data.length - 1];
      ctx.save();
      ctx.font = `600 12px ${Chart.defaults.font.family}`;
      ctx.fillStyle = ds.borderColor;
      ctx.textBaseline = 'middle';
      ctx.fillText(ds.label, last.x + 8, last.y);
      ctx.restore();
    });
  }
};
// uso: new Chart(el, { ..., plugins: [directLabel], options: { plugins: { legend: { display: false } }, layout: { padding: { right: 90 } } } })
```

### 5.0b Anotação de evento (banda ou linha de referência)

```js
// Banda sombreada marcando um período que o texto narra (ex.: "guerra comercial 2018-20")
const eventBand = (fromLabel, toLabel, text) => ({
  id: 'eventBand',
  beforeDatasetsDraw(chart) {
    const { ctx, chartArea, scales: { x } } = chart;
    const x1 = x.getPixelForValue(fromLabel), x2 = x.getPixelForValue(toLabel);
    ctx.save();
    ctx.fillStyle = css('--color-warn-dim') || 'rgba(0,0,0,0.05)';
    ctx.fillRect(x1, chartArea.top, x2 - x1, chartArea.bottom - chartArea.top);
    ctx.font = `600 11px ${Chart.defaults.font.family}`;
    ctx.fillStyle = css('--color-fg-muted');
    ctx.fillText(text, x1 + 6, chartArea.top + 14);
    ctx.restore();
  }
});
// linha de referência horizontal (meta, média, limite regulatório): mesmo padrão com ctx.moveTo/lineTo no y.getPixelForValue(valor)
```

### Regras de fidelidade (OBRIGATÓRIAS)

| Regra | Correto | Errado |
|---|---|---|
| **Dados completos** | Todos os pontos/categorias da fonte no gráfico | Omitir valores "para simplificar" |
| **Composição preservada** | Múltiplas séries que a fonte mostra juntas → gráfico misto (bar+line, line+line) | Separar em 2 gráficos o que a fonte mostra sobreposto |
| **Escala Y começa em 0** | `min: 0` explícito em gráficos de volume/magnitude | Truncar eixo para "ampliar" diferenças |
| **Unidades nos ticks** | `ticks: { callback: v => 'R$ ' + v + ' bi' }` | Números sem unidade |
| **Exceção de escala** | Séries de variação relativa (%) podem ter `min` diferente de 0 — com comentário | Eixo duplo sem `display` e legenda explícitos |

```js
// Configuração de escala coerente — padrão para gráficos de volume/magnitude
scales: {
  y: {
    min: 0,  // SEMPRE 0 para comparação de magnitudes
    grid: { color: css('--color-border') },
    ticks: {
      color: css('--color-fg-muted'),
      callback: v => 'R$ ' + v + ' bi'  // unidade obrigatória
    }
  }
}
```

### 5x. Misto — barras + linha de tendência (composição preservada)

Quando a fonte original mostra barras de volume com linha de tendência sobreposta, **nunca separar em dois gráficos**. Chart.js suporta `type` por dataset:

```html
<canvas id="chart-mixed" aria-label="Volume e tendência"></canvas>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-mixed'), {
  type: 'bar',  // tipo base do gráfico
  data: {
    labels: ['2019', '2020', '2021', '2022', '2023'],
    datasets: [
      {
        type: 'bar',  // série de barras
        label: 'Volume captado (R$ bi)',
        data: [42, 38, 55, 61, 70],
        backgroundColor: css('--color-accent-dim'),
        borderColor: css('--color-accent'),
        borderWidth: 2,
        borderRadius: 0, // radius em barra é decisão declarada, não default
        yAxisID: 'y',
      },
      {
        type: 'line',  // linha de tendência sobreposta — mesmo gráfico
        label: 'Tendência',
        data: [42, 40, 50, 58, 70],
        borderColor: css('--color-fg-muted'),
        borderWidth: 2,
        borderDash: [4, 4],
        pointRadius: 0,
        fill: false,
        tension: 0, // medição anual discreta — sem suavização
        yAxisID: 'y',
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: css('--color-fg-muted') } },
      tooltip: { mode: 'index', intersect: false }
    },
    scales: {
      y: {
        min: 0,
        grid: { color: css('--color-border') },
        ticks: { color: css('--color-fg-muted'), callback: v => 'R$ ' + v + ' bi' }
      },
      x: { grid: { display: false }, ticks: { color: css('--color-fg-muted') } }
    }
  }
});
</script>
```

Regra: se a fonte tem N séries num único visual → N datasets num único `new Chart()`.

---

### 5a. Barra (comparação de volumes)
```html
<div class="chart-wrap">
  <canvas id="chart-bar" aria-label="Gráfico de barras"></canvas>
</div>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-bar'), {
  type: 'bar',
  data: {
    labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    datasets: [{
      label: 'Volume (R$ bi)',
      data: [180, 195, 210, 205, 230, 245],
      backgroundColor: css('--color-accent-dim'),
      borderColor: css('--color-accent'),
      borderWidth: 2,
      borderRadius: 0, // radius em barra é decisão declarada, não default
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => 'R$ ' + ctx.parsed.y + ' bi' } }
    },
    scales: {
      x: { grid: { display: false }, ticks: { color: css('--color-fg-muted'), font: { size: 12 } } },
      y: { grid: { color: css('--color-border') }, ticks: { color: css('--color-fg-muted'), font: { size: 12 } } }
    }
  }
});
</script>
```

### 5b. Linha (evolução temporal)
```html
<canvas id="chart-line" aria-label="Evolução temporal"></canvas>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-line'), {
  type: 'line',
  data: {
    labels: ['2019', '2020', '2021', '2022', '2023'],
    datasets: [{
      label: 'AuM (R$ tri)',
      data: [0.7, 0.85, 0.95, 1.1, 1.19],
      borderColor: css('--color-accent'),
      backgroundColor: css('--color-accent-dim'),
      tension: 0, // medição anual discreta — sem suavização (0.4 default é tell)
      fill: true,
      pointRadius: 5,
      pointHoverRadius: 7,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => 'R$ ' + ctx.parsed.y + ' tri' } }
    },
    scales: {
      x: { grid: { display: false }, ticks: { color: css('--color-fg-muted') } },
      y: { grid: { color: css('--color-border') }, ticks: { color: css('--color-fg-muted') } }
    }
  }
});
</script>
```

### 5c. Donut (composição / participação)
```html
<div style="max-width: 280px; margin: 0 auto;">
  <canvas id="chart-donut" aria-label="Composição de portfólio"></canvas>
</div>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-donut'), {
  type: 'doughnut',
  data: {
    labels: ['Renda Fixa', 'Ações', 'Multi-Mercado', 'ETFs', 'Outros'],
    datasets: [{
      data: [45, 20, 18, 12, 5],
      backgroundColor: [
        css('--color-accent'), css('--color-info'),
        css('--color-teal'),   css('--color-success'), css('--color-sage')
      ],
      borderWidth: 2,
      borderColor: css('--color-bg-elevated'),
      hoverOffset: 6,
    }]
  },
  options: {
    responsive: true,
    cutout: '65%',
    plugins: {
      legend: {
        position: 'right',
        labels: { color: css('--color-fg-muted'), font: { size: 12 }, padding: 12 }
      },
      tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.parsed + '%' } }
    }
  }
});
</script>
```

### 5d. Sparkline inline (KPI card)
```html
<style>
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-5); margin: var(--space-7) 0; }
.kpi-card { background: var(--color-bg-elevated); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-5); }
.kpi-card__label { font-family: var(--font-mono); font-size: var(--size-xs); text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-fg-subtle); margin: 0 0 var(--space-2); }
.kpi-card__value { font-family: var(--font-display); font-size: var(--size-h1); font-weight: 800; letter-spacing: -0.035em; margin: 0; line-height: 1; }
.kpi-card__value span { color: var(--color-accent); }
.kpi-card__trend { font-size: var(--size-xs); color: var(--color-fg-muted); margin: var(--space-2) 0; }
.kpi-card__spark { height: 40px; margin-top: var(--space-3); }
</style>
<div class="kpi-grid">
  <div class="kpi-card">
    <p class="kpi-card__label">AuM</p>
    <p class="kpi-card__value">R$<span>1,19</span>tri</p>
    <p class="kpi-card__trend">+8,3% em 12m</p>
    <canvas class="kpi-card__spark" id="spark-1" aria-label="Sparkline AuM"></canvas>
  </div>
</div>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('spark-1'), {
  type: 'line',
  data: {
    labels: ['', '', '', '', '', ''],
    datasets: [{ data: [0.7, 0.82, 0.91, 1.0, 1.1, 1.19],
      borderColor: css('--color-accent'), borderWidth: 2,
      tension: 0.3, pointRadius: 0, fill: false }] // sparkline narrativo: ≤0.3
  },
  options: { responsive: true, maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { enabled: false } },
    scales: { x: { display: false }, y: { display: false } } }
});
</script>
```

### 5e. Gauge / velocímetro (KPI vs meta)

Doughnut rotado 180° com segmento base transparente. Ideal para taxa de cobertura, atingimento de meta, NPS.

```html
<div style="max-width: 220px; margin: 0 auto; position: relative;">
  <canvas id="chart-gauge" aria-label="Gauge KPI"></canvas>
  <div style="position:absolute;bottom:8px;left:50%;transform:translateX(-50%);text-align:center;line-height:1.1;">
    <span id="gauge-val" style="font-family:var(--font-display);font-size:2rem;font-weight:800;color:var(--color-fg)">87%</span>
    <br><span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--color-fg-subtle);text-transform:uppercase">Cobertura ESG</span>
  </div>
</div>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const val = 87; // valor 0-100
new Chart(document.getElementById('chart-gauge'), {
  type: 'doughnut',
  data: {
    datasets: [{
      data: [val, 100 - val, 100],  // valor, restante, base oculta
      backgroundColor: [css('--color-accent'), css('--color-border'), 'transparent'],
      borderWidth: 0,
      borderRadius: [4, 0, 0],
    }]
  },
  options: {
    responsive: true,
    circumference: 180,
    rotation: -90,
    cutout: '75%',
    plugins: { legend: { display: false }, tooltip: { enabled: false } },
  }
});
</script>
```

---

### 5f. Radar / aranha (comparação de perfil)

Compara N dimensões de dois ou mais itens. Ideal para: perfil de risco de fundo, competências de gestor, atributos de produto.

```html
<canvas id="chart-radar" aria-label="Comparação de perfil"></canvas>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-radar'), {
  type: 'radar',
  data: {
    labels: ['Retorno', 'Liquidez', 'Diversificação', 'ESG', 'Volatilidade Baixa', 'Acesso'],
    datasets: [
      {
        label: 'Fundo Alpha',
        data: [90, 60, 85, 95, 70, 80],
        borderColor: css('--color-accent'),
        backgroundColor: css('--color-accent-dim'),
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: css('--color-accent'),
      },
      {
        label: 'Benchmark',
        data: [70, 80, 65, 50, 85, 90],
        borderColor: css('--color-fg-muted'),
        backgroundColor: 'transparent',
        borderWidth: 2,
        borderDash: [4, 4],
        pointRadius: 3,
        pointBackgroundColor: css('--color-fg-muted'),
      }
    ]
  },
  options: {
    responsive: true,
    scales: {
      r: {
        min: 0, max: 100,
        ticks: { stepSize: 25, color: css('--color-fg-subtle'), font: { size: 10 }, backdropColor: 'transparent' },
        grid: { color: css('--color-border') },
        pointLabels: { color: css('--color-fg-muted'), font: { size: 12 } },
        angleLines: { color: css('--color-border') },
      }
    },
    plugins: { legend: { labels: { color: css('--color-fg-muted') } } }
  }
});
</script>
```

---

### 5g. Bubble (risco × retorno × tamanho)

Três dimensões em um gráfico. X = risco, Y = retorno, R = tamanho (AuM, volume). Ideal para análise de portfólio, comparação de fundos, mapeamento de produtos.

```html
<canvas id="chart-bubble" aria-label="Risco × Retorno × AuM"></canvas>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-bubble'), {
  type: 'bubble',
  data: {
    datasets: [
      {
        label: 'Renda Fixa',
        data: [{ x: 2.1, y: 8.4, r: 24 }],
        backgroundColor: css('--color-accent') + 'cc',
        borderColor: css('--color-accent'),
        borderWidth: 2,
      },
      {
        label: 'Multimercado',
        data: [{ x: 5.8, y: 14.2, r: 16 }],
        backgroundColor: css('--color-info') + 'cc',
        borderColor: css('--color-info'),
        borderWidth: 2,
      },
      {
        label: 'Renda Variável',
        data: [{ x: 12.4, y: 19.7, r: 10 }],
        backgroundColor: css('--color-teal') + 'cc',
        borderColor: css('--color-teal'),
        borderWidth: 2,
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: css('--color-fg-muted') } },
      tooltip: { callbacks: { label: ctx => `${ctx.dataset.label}: risco ${ctx.parsed.x}% | retorno ${ctx.parsed.y}% | AuM R$${ctx.raw.r}bi` } }
    },
    scales: {
      x: { min: 0, title: { display: true, text: 'Volatilidade anualizada (%)', color: css('--color-fg-muted') }, grid: { color: css('--color-border') }, ticks: { color: css('--color-fg-muted'), callback: v => v + '%' } },
      y: { min: 0, title: { display: true, text: 'Retorno acumulado (%)', color: css('--color-fg-muted') }, grid: { color: css('--color-border') }, ticks: { color: css('--color-fg-muted'), callback: v => v + '%' } }
    }
  }
});
</script>
```

---

### 5h. Waterfall / cascata (variação entre períodos)

Mostra de onde vem cada incremento/decremento de um valor. Ideal para: variação de AuM, P&L breakdown, evolução de captação. Implementado com barras empilhadas (base transparente + valor real).

```html
<canvas id="chart-waterfall" aria-label="Variação de AuM"></canvas>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

// Dados: [rótulo, base invisível, valor (+) ou (-)], cor
const steps = [
  { label: 'Jan/24',    base: 0,    val: 980,  type: 'start' },
  { label: 'Captação',  base: 980,  val: 145,  type: 'pos'   },
  { label: 'Resgates',  base: 985,  val: -60,  type: 'neg'   },
  { label: 'Rendimento',base: 925,  val: 88,   type: 'pos'   },
  { label: 'Jun/24',    base: 0,    val: 1013, type: 'end'   },
];

const accent = css('--color-accent');
const info   = css('--color-info');
const danger = css('--color-danger-border') || '#ef4444';
const muted  = css('--color-border');

new Chart(document.getElementById('chart-waterfall'), {
  type: 'bar',
  data: {
    labels: steps.map(s => s.label),
    datasets: [
      {
        label: 'Base (invisível)',
        data: steps.map(s => s.type === 'neg' ? s.base + s.val : s.base),
        backgroundColor: 'transparent',
        borderWidth: 0,
        stack: 'wf',
      },
      {
        label: 'Valor',
        data: steps.map(s => Math.abs(s.val)),
        backgroundColor: steps.map(s =>
          s.type === 'start' || s.type === 'end' ? muted :
          s.type === 'pos' ? info : danger
        ),
        borderRadius: 3,
        stack: 'wf',
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: {
        label: ctx => {
          if (ctx.datasetIndex === 0) return null;
          const s = steps[ctx.dataIndex];
          return `${s.label}: ${s.val > 0 ? '+' : ''}R$ ${s.val} bi`;
        }
      }}
    },
    scales: {
      x: { stacked: true, grid: { display: false }, ticks: { color: css('--color-fg-muted') } },
      y: { stacked: true, min: 0, grid: { color: css('--color-border') }, ticks: { color: css('--color-fg-muted'), callback: v => 'R$ ' + v + ' bi' } }
    }
  }
});
</script>
```

---

## 6. Overflow Protection

Crítico. Sem isso, cards em grid/flex transbordam em viewports estreitas.

```css
/* Todo grid/flex child precisa poder encolher */
.grid > *, .ve-card,
[style*="display: grid"] > *,
[style*="display: flex"] > * {
  min-width: 0;
}

/* Texto longo quebra ao invés de transbordar */
body { overflow-wrap: break-word; }

/* Painéis side-by-side */
.comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
}
.comparison > * { min-width: 0; overflow-wrap: break-word; }

@media (max-width: 768px) {
  .comparison { grid-template-columns: 1fr; }
}

/* NUNCA usar display: flex em <li> para markers — causa overflow em código inline.
   Usar position: relative + absolute em vez disso: */
li {
  position: relative;
  padding-left: 1.4em;
}
li::marker { color: var(--color-fg-subtle); }
```

---

## 7. Motion — perfil do parti, nunca kit universal

> v4: o fade-up universal com stagger `--i` que vivia aqui está REVOGADO — era a assinatura de motion da casa (e de toda UI gerada por IA). Motion é o eixo `motion` do bloco `<!-- slideless:parti -->`: o documento declara 1 de 3 perfis (**estático / editorial / cinemático** — CSS completo em [direcao-de-arte.md §5](direcao-de-arte.md)) e cola o bloco do perfil. O perfil determina QUAIS keyframes existem no arquivo — report estático não contém keyframe de entrada nenhum.

Regras transversais (qualquer perfil):
- `transition` sempre property-scoped — **`transition: all` é proibido**.
- 2–3 easings nomeadas com papel comentado; nunca a mesma curva para entrada e hover.
- Tabela, texto corrido, TOC e nav **nunca** animam entrada; quote entra seca.
- Reveal em ≤40% das `<section>`; stagger só em grupo homogêneo (barras do mesmo gráfico), máx 1 grupo por viewport.
- Entrada ≤500ms; micro-interação 120–200ms; só o momento assinatura excede 500ms.
- Counter animado SÓ no número declarado como assinatura no parti.

Keyframes de referência (usar apenas o que o perfil declarado pede — copiar o necessário, nunca o bloco inteiro):

```css
/* entrada de figura/dado (perfil editorial/cinemático) */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* hero de deck cinemático — ESCOLHER 1 gesto, não empilhar */
@keyframes heroBlur { from { opacity: 0; filter: blur(16px); } to { opacity: 1; filter: blur(0); } }
@keyframes heroWipe { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }

/* Prefers-reduced-motion — OBRIGATÓRIO em todo documento com motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-delay:    0ms   !important;
    transition-duration: 0.01ms !important;
  }
  [data-reveal] { opacity: 1; transform: none; transition-delay: 0s; }
}
```

---

## 8. Code Block com Header de Arquivo

```css
.code-file {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin: var(--space-5) 0;
}

.code-file__header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--color-bg-sunken);
  border-bottom: 1px solid var(--color-border);
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--color-fg-muted);
}

.code-file__header .dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  flex-shrink: 0;
}

.code-file__body {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  line-height: 1.65;
  padding: var(--space-4);
  background: var(--color-bg-elevated);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 480px;
  overflow-y: auto;
  color: var(--color-fg);
  margin: 0;
}
```

```html
<div class="code-file">
  <div class="code-file__header">
    <span class="dot"></span>
    <span>arquivo.py</span>
  </div>
  <pre class="code-file__body"><code>def main():
    print("hello")</code></pre>
</div>
```

---

## 9. Directory Tree

```css
.dir-tree {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  line-height: 1.75;
  background: var(--color-bg-sunken);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5) var(--space-6);
  overflow-x: auto;
  white-space: pre;
  color: var(--color-fg);
}
.dir-tree .ann  { color: var(--color-fg-subtle); font-size: 0.75rem; font-style: italic; }
.dir-tree .hl   { color: var(--color-accent); font-weight: 700; }
.dir-tree .dim  { color: var(--color-fg-muted); }
```

```html
<div class="dir-tree"><span class="hl">slideless/</span>
├── SKILL.md           <span class="ann">← instruções para Claude</span>
├── commands/          <span class="ann">← slash commands</span>
└── assets/</div>
```

---

## 10. Tipografia — usar os kits de type-kits.md

> v4: a tabela de pairings que vivia aqui está REVOGADA (incluía Instrument Serif — fonte-assinatura de IA de 2ª geração, hoje banida). A escolha tipográfica é a **decisão nº 2 do parti**: 1 kit completo de [type-kits.md](type-kits.md) (link com eixos limitados + tokens `--kit-*` + tabela de tracking + features OpenType + fallback de sistema). Lista de fontes banidas no topo daquele arquivo.

Para tema itau, Itau Display/Text têm precedência dentro da rede interna; o kit é o fallback desenhado fora dela. **O fallback automático para Inter NÃO é mais aceitável.**

---

## 11. Prose Accent Elements

Para páginas longa com texto editorial.

```css
/* Pull quote v4: TIPOGRAFIA, não caixinha. A versão antiga (border-left +
   padding de caixa) é o tell do pull-quote-caixa — pull quote de estúdio não tem moldura. */
.pull-quote {
  margin: var(--space-8) 0;
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-style: italic;            /* itálico VERDADEIRO da fonte do kit */
  font-weight: 350;
  line-height: 1.25;
  max-width: 24ch;
  color: var(--color-fg);
  hanging-punctuation: first;    /* Safari; fallback abaixo */
}
.pull-quote::before { content: '\201C'; margin-left: -0.45em; } /* aspas curvas penduradas */
/* PROIBIDO: background, border-left, border-radius no pull quote */

.lede {
  font-size: var(--size-lead);
  line-height: 1.5;
  color: var(--color-fg-muted);
  font-weight: 400;
  max-width: 65ch;
  margin-bottom: var(--space-8);
}

.content-meta {
  font-family: var(--font-mono);
  font-size: var(--size-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-fg-subtle);
  margin-bottom: var(--space-5);
}

.divider {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: var(--space-10) 0;
}

/* Número âncora editorial */
.anchor-num {
  font-family: var(--font-display);
  font-size: var(--size-giga);
  font-weight: 800;
  letter-spacing: -0.055em;
  line-height: 0.9;
  color: var(--color-accent);
  opacity: 0.15;
  pointer-events: none;
  user-select: none;
  position: absolute;
  right: -0.1em;
  top: -0.2em;
}
```

---

## 12. Responsive Section Navigation

Para páginas com muitas seções (handbook, site, scrollytelling).

```css
/* Desktop: sidebar sticky */
@media (min-width: 1025px) {
  .side-nav {
    position: sticky;
    top: calc(var(--header-h) + var(--space-5));
    align-self: start;
    width: var(--sidebar-w);
    overflow-y: auto;
    max-height: calc(100vh - var(--header-h) - var(--space-10));
  }
}

/* Mobile: barra horizontal scrollável */
@media (max-width: 1024px) {
  .side-nav {
    position: sticky;
    top: var(--header-h);
    z-index: 80;
    overflow-x: auto;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
    background: var(--color-bg);
    border-bottom: 1px solid var(--color-border);
    padding: var(--space-2) var(--space-4);
  }
  .side-nav ul { display: inline-flex; gap: var(--space-2); list-style: none; padding: 0; margin: 0; }
  .side-nav li a { display: inline-block; padding: var(--space-2) var(--space-3); font-size: var(--size-small); }
}
```

---

## 14. Layout expressivo — craft mais alto, SEM animação (A1-safe, vale até no report)

> O "uau" não vem só de movimento. A maior parte da diferença entre "decente" e "editorial de agência" é **composição**: assimetria, escala, sangria, tipografia como protagonista. Estes padrões são **estáticos e ligados ao conteúdo** — sobem o craft em qualquer registro, inclusive `report` sóbrio (onde os W animados são proibidos). Ligam-se aos eixos `capa:`/`assinatura:` do parti (`split-assimetrico`, `numero-protagonista` já são nomes de capa). Os mais ousados (`broken-grid`) ficam para registros expressivos.

### 14a. Coluna assimétrica (2fr / 1fr) — quebra o centro morto
```css
.asym { display: grid; grid-template-columns: 2fr 1fr; gap: var(--space-8); align-items: start; }
.asym--reverse { grid-template-columns: 1fr 2fr; }
@media (max-width: 720px) { .asym, .asym--reverse { grid-template-columns: 1fr; } }
```

### 14b. Numeral gigante como composição (sangra a margem) — M0 do report
```css
/* O número-tese vira o elemento gráfico. Sangra para fora da coluna; o texto encaixa ao lado. */
.numeral-bleed { position: relative; padding-left: clamp(0px, 8vw, 7rem); }
.numeral-bleed__n {
  position: absolute; left: -2vw; top: -0.15em; z-index: 0;
  font-family: var(--font-display); font-weight: 800; line-height: 0.8;
  font-size: clamp(7rem, 22vw, 18rem); letter-spacing: -0.04em;
  color: var(--color-border-strong);          /* fantasma; ou var(--color-accent) p/ ênfase */
  font-variant-numeric: tabular-nums lining-nums; user-select: none; pointer-events: none;
}
.numeral-bleed > * { position: relative; z-index: 1; }
```

### 14c. Tipografia full-bleed (manchete que ocupa a largura)
```css
.full-bleed-type {
  font-family: var(--font-display); font-weight: 800;
  font-size: clamp(2.5rem, 9vw, 7rem); line-height: 0.95; letter-spacing: -0.03em;
  text-wrap: balance; margin-inline: calc(-1 * var(--space-4));
}
```

### 14d. Broken grid (sobreposição editorial — só registros expressivos)
```css
/* Imagem/figura e texto se sobrepõem em vez de empilhar. Tensão controlada. */
.broken-grid { display: grid; grid-template-columns: repeat(12, 1fr); align-items: center; }
.broken-grid__fig  { grid-column: 1 / 8; grid-row: 1; z-index: 0; }
.broken-grid__text { grid-column: 6 / 13; grid-row: 1; z-index: 1;
  background: var(--color-bg-elevated); padding: var(--space-6); border: 1px solid var(--color-border); }
@media (max-width: 720px) {
  .broken-grid { display: block; }
  .broken-grid__text { margin-top: calc(-1 * var(--space-6)); }
}
```

### 14e. Tabela-protagonista full-bleed (report, M0)
```css
/* A tabela ocupa toda a largura do conteúdo, com fio duplo no total (linguagem contábil). */
.table-hero { width: 100%; margin: var(--space-8) 0; }
.table-hero table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums lining-nums; }
.table-hero tfoot td, .table-hero tr.total td { border-top: 3px double var(--color-fg); font-weight: 700; }
```

**Régua:** numeral gigante e full-bleed type são protagonistas — **um por dobra/seção**, no dado-tese. Broken-grid: tensão controlada, nunca sobreposição que prejudique leitura (WCAG: contraste do `__text` garantido pelo `background`).

```js
/* Scroll spy — scroll active nav link to center on mobile */
const navLinks = document.querySelectorAll('.side-nav a');
const spy = new IntersectionObserver(es => {
  es.forEach(e => {
    if (!e.isIntersecting) return;
    const id = '#' + e.target.id;
    navLinks.forEach(a => {
      a.classList.toggle('is-active', a.getAttribute('href') === id);
      if (a.getAttribute('href') === id && window.innerWidth < 1025) {
        a.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    });
  });
}, { rootMargin: '-30% 0px -60% 0px' });
document.querySelectorAll('[id]').forEach(el => {
  if ([...navLinks].some(a => a.getAttribute('href') === '#' + el.id)) spy.observe(el);
});
```

---

## Checklist visual antes de entregar

1. **Squint test**: blur os olhos — hierarchy ainda visível?
2. **Swap test v4**: cobrindo o logo e o laranja, este documento é distinguível do exemplo canônico do modelo e do último documento da pasta? (comparar blocos parti — capa/kit/superfície não podem coincidir com o canônico)
3. **Ambos os temas**: light e dark funcionam sem flash ou cores quebradas?
4. **Sem overflow**: redimensionar janela — algo fica clipado?
5. **Informação completa**: tudo da fonte original está presente?
6. **Mermaid zoom controls**: presente em todo diagrama Mermaid?
7. **Tabelas HTML**: 4+ linhas ou 3+ colunas usam `<table>` (nunca ASCII)? Todas as linhas presentes? `tabular-nums` nas células numéricas?
8. **Gráficos Chart.js**: `Chart.defaults.font.family` setado dos tokens? Formatação pt-BR nos ticks/tooltips? Todos os pontos da fonte presentes? Eixo Y em 0 para magnitudes? Unidade nos ticks? ≤3 séries sem legenda default (direct labels)? Gráfico-tese com ≥1 anotação?
9. **Sem slop de 1ª geração** (tells óbvios):
   - Inter como display? ✗ · violet/indigo? ✗ · gradient text? ✗ · emoji-ícone? ✗
   - Glowing box-shadows animados? ✗ · cyan-magenta on dark? ✗
10. **Sem slop da casa** (tells de 2ª geração — a coocorrência denuncia):
    - Glow radial em body::before incondicional? ✗
    - Hover translateY em elemento não-clicável? ✗
    - Fade-up idêntico em toda section? ✗
    - Kicker mono-uppercase em mais de 1 papel? ✗
    - `<em>` accent em >25% dos títulos? ✗
    - `transition: all`? ✗ · uma única cubic-bezier no arquivo? ✗
    - Paleta accent/info/teal/plum distribuída em sequência decorativa? ✗
    - Tudo é card com a mesma sombra e o mesmo radius? ✗

---

## 13. Arsenal cutting-edge (nível A2/A3 — ver [ambicao.md](ambicao.md))

> Blocos copiáveis dos momentos-wow e da materialidade. **Os 3 invariantes valem em todos:** (1) dentro de `@media (prefers-reduced-motion: no-preference)` ou com branch `reduce`; (2) dentro de `@supports` com o **estado final visível como base** (num Chrome travado nada some); (3) só animar `transform`/`opacity` (gradiente/blur só em área pequena). **report:** só grain estático + specular 1px — nada animado.

### 13.1 Régua de craft (tokens — base de TODA ambição, inclusive A1)
```css
:root {
  --ease-out-strong: cubic-bezier(0.23, 1, 0.32, 1);   /* entrada/saída */
  --ease-io-strong:  cubic-bezier(0.77, 0, 0.175, 1);  /* morph/movimento */
  --spring: cubic-bezier(0.34, 1.56, 0.64, 1);         /* fallback com overshoot */
  --dur-fast: 150ms; --dur-ui: 220ms; --dur-modal: 320ms;  /* teto 300-320ms p/ UI */
}
@supports (animation-timing-function: linear(0,1)) {
  :root { --spring: linear(0, 0.006, 0.025, 0.101, 0.539, 0.826, 0.949, 1.01, 1.036, 1.022, 1, 0.994, 1); }
}
/* nunca scale(0) → use 0.96; entrada lenta / saída rápida; origem espacial no transform-origin do gatilho */
```

### 13.2 Materialidade — os 4 premium baratos (0KB)

**Aurora mesh** (assinatura Linear/Vercel; W7):
```css
.aurora { position:absolute; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(40% 50% at 20% 30%, color-mix(in srgb, var(--color-accent) 22%, transparent), transparent 70%),
    radial-gradient(45% 55% at 80% 25%, color-mix(in srgb, var(--color-info)  18%, transparent), transparent 70%),
    radial-gradient(50% 60% at 60% 80%, color-mix(in srgb, var(--color-teal)  14%, transparent), transparent 70%);
  background-size: 200% 200%, 200% 200%, 200% 200%; }
@media (prefers-reduced-motion: no-preference) { .aurora { animation: auroraDrift 28s ease-in-out infinite alternate; } }
@keyframes auroraDrift { 0%{background-position:0% 0%,100% 0%,50% 100%} 100%{background-position:100% 50%,0% 80%,30% 0%} }
/* fallback: sem animação ainda fica lindo — é o próprio fallback do minigl (W9) */
```

**Grain `feTurbulence`** (W7 — tato de papel; mata banding):
```css
:root { --grain: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
body::after { content:''; position:fixed; inset:0; z-index:9999; pointer-events:none; opacity:.06; mix-blend-mode:soft-light; background-image:var(--grain); }
@media print { body::after { display:none; } }
/* animado (opcional, não-report): .grain-anim::after { animation: grainShift .5s steps(8) infinite; } com translate em keyframes */
```

**Borda de luz 1px + glow** (W7 — "design system caro"):
```css
.lux { position:relative; border-radius:var(--radius-lg);
  background: linear-gradient(var(--color-bg-elevated),var(--color-bg-elevated)) padding-box,
              linear-gradient(180deg, color-mix(in srgb,var(--color-fg) 22%,transparent), transparent 40%) border-box;
  border:1px solid transparent;
  box-shadow: inset 0 1px 0 color-mix(in srgb,var(--color-fg) 8%,transparent), 0 20px 40px -24px rgba(0,0,0,.5); }
@supports not (background: linear-gradient(red) padding-box) { .lux { border:1px solid var(--color-border); } }
```

**Glass com fallback** (W7 — vidro 2026; máx 3-5/viewport, nunca animar blur):
```css
.glass { background: color-mix(in srgb, var(--color-bg-elevated) 70%, transparent);
  backdrop-filter: blur(20px) saturate(1.6); -webkit-backdrop-filter: blur(20px) saturate(1.6);
  border:1px solid color-mix(in srgb,var(--color-fg) 14%,transparent);
  box-shadow: inset 0 1px 0 color-mix(in srgb,#fff 20%,transparent), 0 8px 32px rgba(0,0,0,.2); }
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass { background: var(--color-bg-elevated); }   /* fallback sólido */ }
```

**Conic glow `@property`** (Tier A — 1-2/doc, A2/A3, NÃO report):
```css
@property --ang { syntax:'<angle>'; initial-value:0deg; inherits:false; }
.glow-ring::before { content:''; position:absolute; inset:-2px; border-radius:inherit; z-index:-1; filter:blur(8px); opacity:.7;
  background: conic-gradient(from var(--ang), var(--color-accent), var(--color-info), var(--color-accent)); }
@media (prefers-reduced-motion: no-preference) { .glow-ring::before { animation: spin 4s linear infinite; } }
@keyframes spin { to { --ang: 360deg; } }
/* sem @property: ângulo fica fixo (initial-value) — base bonita; é o fallback */
```

### 13.3 Scroll-driven reveal (W1/W6 — substitui o IO de reveal por CSS nativo)
```css
@supports (animation-timeline: view()) { @media (prefers-reduced-motion: no-preference) {
  .reveal { animation: reveal-up linear both; animation-timeline: view(); animation-range: entry 0% cover 35%; }
  @keyframes reveal-up { from { opacity:0; transform: translateY(24px); } to { opacity:1; transform:none; } }
  .progress-bar { transform-origin:left; animation: grow linear both; animation-timeline: scroll(root block); }
  @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
}}
.reveal { opacity:1; }   /* BASE = estado final (Chrome travado não esconde conteúdo) */
/* manchete cinética W3 / text reveal W6 / counter sincronizado W2: ver ambicao.md (receitas completas) */
```

### 13.4 View Transitions same-document (W5 — site/hub, morph sem framework)
```js
function navigate(updateDOM){
  if (!document.startViewTransition || matchMedia('(prefers-reduced-motion: reduce)').matches) { updateDOM(); return; }
  document.startViewTransition(updateDOM);
}
```
```css
.card-hero{ view-transition-name: hero; } .panel-hero{ view-transition-name: hero; } /* mesmo nome → morph */
@media (prefers-reduced-motion: reduce) { ::view-transition-group(*){ animation:none !important; } }
/* nome único por snapshot; fallback é o guard if() — troca instantânea */
```

### 13.5 `@starting-style` — entrada de painel/toast sem JS de classe
```css
.panel { opacity:1; transform: translateY(0);
  transition: opacity var(--dur-ui) var(--ease-out-strong), transform var(--dur-ui) var(--ease-out-strong),
              display var(--dur-ui) allow-discrete, overlay var(--dur-ui) allow-discrete; }
@starting-style { .panel[open], .panel.is-open { opacity:0; transform: translateY(12px); } }
/* sem suporte: aparece sem animar — degradação trivial */
```

### 13.6 Anotação viva no gráfico-tese (W8 — generaliza o annoPlugin do exemplo-scrollytelling)
```js
// plugin Chart.js: lê objeto `anno` mutável {from,to,label,y} e desenha banda + leader-line no afterDatasetsDraw.
// Crosshair de leitura (hover): options.onHover → linha vertical no índice + valor fmtBR. Ver §5.0b (eventBand) e exemplo-scrollytelling.
// Fallback: desenhar a anotação no 1º render (não depender de scroll/hover).
```

### 14f. Stepper de processo (fluxo de N passos) — NÃO use draw-on cru de bolinhas

O fluxograma "bolinhas + linha fina + label cinza" sai estático e feio. Para um processo (brief→/criar→formato→pronto), use discos numerados grandes, o último em destaque, labels com sub-texto, e a linha que se desenha (W22) + discos que entram em sequência (scale/stagger via IO, base visível):

```css
.flow__row{ display:grid; grid-template-columns:repeat(4,1fr); position:relative; }
.flow__track{ position:absolute; top:29px; left:12.5%; right:12.5%; height:2px; }
.flow__track .draw-on{ stroke:var(--color-accent); stroke-width:2.5; stroke-dasharray:100; stroke-dashoffset:0; }
.flow__disc{ width:60px; height:60px; border-radius:50%; display:grid; place-items:center;
  font-family:var(--font-display); font-weight:700; font-size:1.45rem;
  background:var(--color-bg-elevated); border:2px solid var(--color-border-strong); color:var(--color-fg-muted); }
.flow__disc.is-final{ background:var(--color-accent); border-color:var(--color-accent); color:var(--color-accent-fg); box-shadow:0 12px 34px var(--color-accent-dim); }
/* JS: a classe .flow--anim só é adicionada POR JS (base = tudo visível); IO adiciona .is-in. */
.flow--anim .flow__disc{ opacity:0; transform:scale(.55); transition:opacity .5s var(--spring), transform .5s var(--spring); transition-delay:calc(var(--i,0)*120ms); }
.flow--anim.is-in .flow__disc{ opacity:1; transform:none; }
.flow--anim .draw-on{ stroke-dashoffset:100; transition:stroke-dashoffset 1.5s ease .15s; }
.flow--anim.is-in .draw-on{ stroke-dashoffset:0; }
@media (max-width:640px){ .flow__row{ grid-template-columns:1fr; } .flow__track{ display:none; } }
```

### 14g. Comparação "antes/depois" — contraste, não texto chapado

Duas colunas de texto cinza igual não comunicam. Faça o "antes" **apagado e riscado** (✕, opacity, `text-decoration:line-through`) e o "depois" **em card de destaque** (borda accent, glow, ✓). E **nunca** esconda a comparação em `data-fragment="current-visible"` (spotlight mostra um lado por vez e some no load) — comparação tem que aparecer inteira.
