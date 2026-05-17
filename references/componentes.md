# Biblioteca de componentes

Componentes reutilizáveis entre modelos. Cada um traz HTML + CSS-key + JS (quando aplicável). Todos respeitam tokens de [design-system.md](design-system.md) e `prefers-reduced-motion`.

---

## Callouts

Quatro variantes: `info`, `tip`, `warn`, `danger`. Borda esquerda colorida, fundo levemente tingido, ícone circular.

```html
<aside class="callout callout--info" role="note">
  <span class="callout__icon" aria-hidden="true">i</span>
  <div class="callout__content">
    <p class="callout__title">Atenção</p>
    <p>Conteúdo do aviso.</p>
  </div>
</aside>
```

`callout--danger` deve usar `role="alert"` em vez de `role="note"`.

---

## Toggle (`<details>`)

Toggle nativo. Sem JS.

```html
<details class="toggle">
  <summary class="toggle__summary">Como criar credenciais?</summary>
  <div class="toggle__body">
    <p>Passo 1…</p>
  </div>
</details>
```

---

## Tabs

```html
<div class="tabs" role="tablist">
  <button class="tab is-active" role="tab" aria-selected="true" data-tab="visao">Visão</button>
  <button class="tab" role="tab" aria-selected="false" data-tab="dados">Dados</button>
</div>
<div class="tab-panel is-active" id="visao" role="tabpanel">…</div>
<div class="tab-panel" id="dados" role="tabpanel" hidden>…</div>
```
```js
document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', e => {
  const id = e.currentTarget.dataset.tab;
  document.querySelectorAll('.tab').forEach(x => x.classList.toggle('is-active', x === e.currentTarget));
  document.querySelectorAll('.tab').forEach(x => x.setAttribute('aria-selected', x === e.currentTarget));
  document.querySelectorAll('.tab-panel').forEach(p => {
    const on = p.id === id;
    p.classList.toggle('is-active', on);
    p.hidden = !on;
  });
}));
```

---

## Code block com copiar

```html
<div class="code">
  <div class="code__head">
    <span class="code__lang">python</span>
    <button class="code__copy" type="button">Copiar</button>
  </div>
  <pre><code><span class="tk-kw">def</span> <span class="tk-fn">fn</span>():
    <span class="tk-kw">return</span> <span class="tk-str">"ok"</span></code></pre>
</div>
```
```js
document.querySelectorAll('.code__copy').forEach(btn => btn.addEventListener('click', async () => {
  const code = btn.closest('.code').querySelector('pre').innerText;
  try { await navigator.clipboard.writeText(code); btn.classList.add('is-copied'); btn.textContent = 'Copiado!'; }
  catch { btn.textContent = 'Erro'; }
  setTimeout(() => { btn.classList.remove('is-copied'); btn.textContent = 'Copiar'; }, 1600);
}));
```

Spans `.tk-kw`, `.tk-str`, `.tk-fn`, `.tk-comment` permitem highlighting manual mínimo. Para highlighting real (Prism/Shiki), ver workflow para handbook.

---

## Reveal on scroll (Intersection Observer)

Para `handbook`/`scrollytelling`/`site`.

```html
<section data-reveal>...</section>
```
```css
[data-reveal] {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 600ms var(--ease-out), transform 600ms var(--ease-out);
}
[data-reveal].is-visible { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  [data-reveal] { opacity: 1; transform: none; transition: none; }
}
```
```js
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); } });
}, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
```

---

## Counters animados

```html
<span class="counter" data-to="98" data-suffix="%">0</span>
```
```js
function animateCount(el) {
  const target = parseFloat(el.dataset.to);
  const suffix = el.dataset.suffix || '';
  const dur = 1200;
  const t0 = performance.now();
  function tick(t) {
    const p = Math.min(1, (t - t0) / dur);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = (target * eased).toFixed(target % 1 ? 1 : 0) + suffix;
    if (p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
const cio = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { animateCount(e.target); cio.unobserve(e.target); }
}), { threshold: 0.5 });
document.querySelectorAll('.counter').forEach(c => cio.observe(c));
```

---

## Cards

```html
<a href="#secao" class="card" data-category="dados">
  <div class="card__icon">📊</div>
  <h3 class="card__title">Catálogo de Dados</h3>
  <p class="card__desc">Busca e linhagem para 2.4k tabelas.</p>
  <span class="card__cta">Abrir →</span>
</a>
```

Hover: leve translateY(-2px), border accent, shadow.

---

## Métricas (3-up)

```html
<div class="metrics">
  <div class="metric">
    <p class="metric__val"><span class="counter" data-to="2400">0</span>+</p>
    <p class="metric__label">tabelas catalogadas</p>
  </div>
</div>
```

---

## Timeline vertical

```html
<ol class="timeline">
  <li class="timeline__item">
    <span class="timeline__dot"></span>
    <p class="timeline__date">2024 Q1</p>
    <h4 class="timeline__title">Catálogo lançado</h4>
    <p class="timeline__desc">…</p>
  </li>
</ol>
```

---

## Sidebar nav + scrollspy (handbook)

```html
<aside class="sidebar" aria-label="Navegação principal">
  <nav class="sidebar__group">
    <p class="sidebar__heading">Plataforma</p>
    <ul class="sidebar__list">
      <li><a href="#visao-geral" class="is-active">Visão geral</a></li>
      <li><a href="#dados">Dados</a></li>
    </ul>
  </nav>
</aside>
```
```js
const links = document.querySelectorAll('.sidebar__list a, .toc a');
const targets = [...links].map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
const spy = new IntersectionObserver(es => {
  es.forEach(e => {
    if (!e.isIntersecting) return;
    const id = '#' + e.target.id;
    links.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === id));
  });
}, { rootMargin: '-30% 0px -60% 0px' });
targets.forEach(t => spy.observe(t));
```

---

## TOC sticky (handbook)

```html
<aside class="toc" aria-label="Nesta página">
  <p class="toc__heading">Nesta página</p>
  <ul class="toc__list">
    <li><a href="#secao-1">Introdução</a></li>
  </ul>
</aside>
```
Gerado a partir dos `<h2>` da página. Mesmo scrollspy da sidebar.

---

## Hash routing (site SPA)

```html
<nav class="topnav">
  <a href="#home" class="topnav__link is-active">Home</a>
  <a href="#sobre" class="topnav__link">Sobre</a>
</nav>
<article class="view is-active" id="home">…</article>
<article class="view" id="sobre" hidden>…</article>
```
```js
function route() {
  const id = (location.hash || '#home').slice(1);
  document.querySelectorAll('.view').forEach(v => {
    const on = v.id === id;
    v.classList.toggle('is-active', on);
    v.hidden = !on;
  });
  document.querySelectorAll('.topnav__link').forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + id));
  window.scrollTo({ top: 0, behavior: 'instant' });
}
addEventListener('hashchange', route);
addEventListener('DOMContentLoaded', route);
```

---

## Slide engine (deck)

Ver [modelos/deck.md](modelos/deck.md) — slide engine é específico do deck, não é componente reutilizável.

---

## Tabelas de dados (HTML semântico)

Threshold: **4+ linhas OU 3+ colunas → usar `<table>`, nunca bullets**. Ver patterns completos em [css-patterns.md](css-patterns.md#3-data-tables).

### Anti-pattern: reveal/fragment em linhas individuais

**Errado** — Aplicar `data-reveal` (handbook/scrollytelling/site) ou `data-fragment` (deck) em cada `<tr>` faz a tabela aparecer linha por linha, quebrando a leitura comparativa.

```html
<!-- NUNCA fazer assim -->
<table class="data-table">
  <tr data-reveal>...</tr>
  <tr data-reveal>...</tr>
</table>
```

**Correto** — Reveal no wrapper, tabela aparece completa:

```html
<div class="table-wrap" data-reveal>
  <table class="data-table">
    <tr>...</tr>
  </table>
</div>
```

**No deck**, o spotlight de linha é apresentador-controlado: o template aplica hover automático em toda `.data-table` dentro de `.slide`. O apresentador passa o mouse sobre qualquer linha durante a apresentação — ela ganha background accent + bold; as demais ficam muted. Sem fragmentos, sem keyboard, sem ordem pré-definida. O apresentador decide o que destacar quando.

```html
<!-- No deck — nada de fragmento em <tr>. O hover do template faz tudo. -->
<table class="data-table">
  <tr><td>Linha A</td>...</tr>
  <tr><td>Linha B</td>...</tr>
</table>
```

---

```html
<div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Tipo</th>
        <th class="num">AuM (R$ bi)</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Fundo Alpha</strong><br><small style="color: var(--color-fg-subtle)">CNPJ 00.000.000/0001-00</small></td>
        <td>Multimercado</td>
        <td class="num">12,4</td>
        <td><span class="badge badge--success">Ativo</span></td>
      </tr>
      <tr>
        <td><strong>Fundo Beta</strong></td>
        <td>Renda Fixa</td>
        <td class="num">8,7</td>
        <td><span class="badge badge--info">Em análise</span></td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td colspan="2"><strong>Total</strong></td>
        <td class="num"><strong>21,1</strong></td>
        <td></td>
      </tr>
    </tfoot>
  </table>
</div>
```

---

## Gráficos (Chart.js via CDN)

CDN: `<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>`

Patterns completos (barra, linha, donut, sparkline) em [css-patterns.md](css-patterns.md#5-chartjs-patterns).

### Ler cores via getComputedStyle (obrigatório para dark mode)
```js
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
```

### Linha — evolução temporal
```html
<canvas id="chart-line" aria-label="Evolução AuM"></canvas>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-line'), {
  type: 'line',
  data: {
    labels: ['2019', '2020', '2021', '2022', '2023'],
    datasets: [{
      label: 'AuM (R$ tri)',
      data: [0.70, 0.85, 0.95, 1.10, 1.19],
      borderColor: css('--color-accent'),
      backgroundColor: css('--color-accent-dim'),
      tension: 0.4, fill: true,
      pointRadius: 5, pointHoverRadius: 7,
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { display: false }, ticks: { color: css('--color-fg-muted') } },
      y: { grid: { color: css('--color-border') }, ticks: { color: css('--color-fg-muted') } }
    }
  }
});
</script>
```

### Barra — comparação por categoria
```html
<canvas id="chart-bar" aria-label="Distribuição por estratégia"></canvas>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-bar'), {
  type: 'bar',
  data: {
    labels: ['RF', 'Ações', 'MM', 'ETF'],
    datasets: [{
      data: [45, 22, 20, 13],
      backgroundColor: [css('--color-accent-dim'), css('--color-info-dim'), css('--color-teal-dim'), css('--color-success-dim')],
      borderColor: [css('--color-accent'), css('--color-info'), css('--color-teal'), css('--color-success')],
      borderWidth: 2, borderRadius: 6,
    }]
  },
  options: {
    responsive: true, indexAxis: 'y',
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { color: css('--color-border') }, ticks: { color: css('--color-fg-muted') } },
      y: { grid: { display: false }, ticks: { color: css('--color-fg-muted') } }
    }
  }
});
</script>
```

### Donut — composição / market share
```html
<div style="max-width: 300px;">
  <canvas id="chart-donut" aria-label="Composição do portfólio"></canvas>
</div>
<script>
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
new Chart(document.getElementById('chart-donut'), {
  type: 'doughnut',
  data: {
    labels: ['Renda Fixa', 'Ações', 'Multi-Mercado', 'ETFs'],
    datasets: [{
      data: [45, 22, 20, 13],
      backgroundColor: [css('--color-accent'), css('--color-info'), css('--color-teal'), css('--color-success')],
      borderWidth: 2, borderColor: css('--color-bg-elevated'), hoverOffset: 6,
    }]
  },
  options: {
    responsive: true, cutout: '68%',
    plugins: {
      legend: { position: 'right', labels: { color: css('--color-fg-muted'), font: { size: 12 }, padding: 12 } },
      tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.parsed + '%' } }
    }
  }
});
</script>
```

---

## Mermaid Zoom Controls

Todo diagrama Mermaid precisa de zoom/pan/fit/expand. Pattern completo (HTML + CSS + JS ~180 linhas) em [css-patterns.md](css-patterns.md#4-mermaid-zoom-controls).

Estrutura mínima obrigatória:
```html
<div class="diagram-shell">
  <div class="zoom-controls">
    <button class="zoom-btn" data-action="zoom-in">+</button>
    <button class="zoom-btn" data-action="zoom-out">−</button>
    <button class="zoom-btn" data-action="zoom-fit">↻</button>
    <button class="zoom-btn" data-action="zoom-one">1:1</button>
    <button class="zoom-btn" data-action="zoom-exp">⛶</button>
    <span class="zoom-label">100%</span>
  </div>
  <div class="mermaid-viewport">
    <div class="mermaid mermaid-canvas">
      graph TD
        A[Componente A] --> B[Componente B]
    </div>
  </div>
</div>
```
