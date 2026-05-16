# CSS Patterns — slideless

Biblioteca de padrões copy-paste para todos os modelos. Cada bloco é standalone e respeita os tokens de `design-system.md`. **Ler antes de gerar HTML com componentes novos.**

---

## 1. Background Atmosphere

Backgrounds planos parecem mortos. Escolher um dos quatro padrões abaixo.

### 1a. Radial glow (recomendado para deck/hero)
```css
body {
  background: var(--color-bg);
  background-image:
    radial-gradient(ellipse 90% 70% at 50% 0%,   var(--color-accent-dim) 0%, transparent 60%),
    radial-gradient(ellipse 70% 50% at 20% 100%,  var(--color-info-dim)   0%, transparent 55%);
}
```

### 1b. Dot grid (blueprint / técnico)
```css
body {
  background-color: var(--color-bg);
  background-image: radial-gradient(circle, var(--color-border) 1px, transparent 1px);
  background-size: 24px 24px;
}
```

### 1c. Diagonal lines (editorial sutil)
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

### 1d. Gradient mesh (deck dark hero)
```css
body {
  background-image:
    radial-gradient(at 20% 20%, var(--color-accent-dim) 0%, transparent 50%),
    radial-gradient(at 80% 60%, var(--color-info-dim)   0%, transparent 50%),
    radial-gradient(at 50% 90%, var(--color-teal-dim)   0%, transparent 50%);
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

/* Hover lift */
.ve-card--hoverable:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-accent);
}
```

### Label monospace dentro de card
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
  transition: all var(--duration-fast);
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
        borderRadius: 4,
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
        tension: 0.4,
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
      borderRadius: 6,
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
      tension: 0.4,
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
      tension: 0.4, pointRadius: 0, fill: false }]
  },
  options: { responsive: true, maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { enabled: false } },
    scales: { x: { display: false }, y: { display: false } } }
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

## 7. Animações (entrance reveals)

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeScale {
  from { opacity: 0; transform: scale(0.94); }
  to   { opacity: 1; transform: scale(1); }
}

@keyframes heroIn {
  from { opacity: 0; filter: blur(16px); transform: translateY(28px) scale(0.96); }
  to   { opacity: 1; filter: blur(0);    transform: translateY(0)    scale(1); }
}

/* Aplicar com stagger via --i CSS variable */
.anim-fade-up {
  animation: fadeUp 0.5s var(--ease-out) both;
  animation-delay: calc(var(--i, 0) * 0.06s);
}

.anim-fade-scale {
  animation: fadeScale 0.5s var(--ease-out) both;
  animation-delay: calc(var(--i, 0) * 0.07s);
}

/* Reveal on scroll */
[data-reveal] {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 700ms var(--ease-out),
              transform 700ms var(--ease-out);
  transition-delay: calc(var(--i, 0) * 60ms);
}
[data-reveal].is-visible { opacity: 1; transform: none; }

/* Prefers-reduced-motion — OBRIGATÓRIO */
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

## 10. Font Pairings — escolher por projeto

Nunca usar Inter sozinho como fonte primária. Escolher um par e ser consistente.

| Pair | Uso ideal | Google Fonts link |
|---|---|---|
| **DM Sans + Fira Code** | Técnico, preciso | `family=DM+Sans:wght@400;500;600;700&family=Fira+Code:wght@400;500` |
| **Instrument Serif + JetBrains Mono** | Editorial, refinado | `family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;600` |
| **IBM Plex Sans + IBM Plex Mono** | Confiável, corporativo | `family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500` |
| **Bricolage Grotesque + Fragment Mono** | Bold, caracterful | `family=Bricolage+Grotesque:wght@400;500;600;700;800&family=Fragment+Mono` |
| **Plus Jakarta Sans + Azeret Mono** | Arredondado, tech | `family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Azeret+Mono:wght@400;500` |

Para tema itau, as fontes proprietárias (Itaú Display/Text) têm precedência dentro da rede interna. Fora da rede, o fallback automático para Inter é aceitável — mas para demos e documentos externos, considerar um dos pares acima.

```html
<!-- Exemplo: Instrument Serif + JetBrains Mono -->
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --font-display: 'Instrument Serif', Georgia, serif;
    --font-mono: 'JetBrains Mono', 'SF Mono', monospace;
    /* --font-text: override para body se necessário */
  }
</style>
```

---

## 11. Prose Accent Elements

Para páginas longa com texto editorial.

```css
.pull-quote {
  border-left: 3px solid var(--color-accent);
  margin: var(--space-8) 0;
  padding: var(--space-4) var(--space-6);
  font-family: var(--font-display);
  font-size: var(--size-h3);
  font-weight: 600;
  line-height: 1.35;
  letter-spacing: -0.015em;
  color: var(--color-fg);
  font-style: italic;
}

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
2. **Swap test**: substituir fonts/cores por Inter+roxo genérico seria indistinguível?
3. **Ambos os temas**: light e dark funcionam sem flash ou cores quebradas?
4. **Sem overflow**: redimensionar janela — algo fica clipado?
5. **Informação completa**: tudo da fonte original está presente?
6. **Mermaid zoom controls**: presente em todo diagrama Mermaid?
7. **Tabelas HTML**: 4+ linhas ou 3+ colunas usam `<table>` (nunca ASCII)? Todas as linhas da fonte estão presentes (sem truncagem)?
8. **Gráficos Chart.js**: dados numéricos relevantes têm representação visual? Todos os pontos/categorias da fonte estão no gráfico (sem omissão)? Eixo Y começa em 0 para magnitudes? Unidade nos ticks?
9. **Sem slop signals** (checar):
   - Inter font + violet/indigo accents? ✗
   - Gradient text headings? ✗
   - Emoji icons em seções? ✗
   - Animated glowing box-shadows? ✗
   - Cyan-magenta-pink on dark? ✗
   - Grid uniforme sem hierarchy? ✗
   - Three-dot code block chrome? ✗
