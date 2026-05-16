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

## Gráficos (Chart.js via CDN)

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<canvas id="chart-1" aria-label="Volume mensal"></canvas>
<script>
  new Chart(document.getElementById('chart-1'), {
    type: 'line',
    data: { labels: [...], datasets: [{ data: [...], borderColor: 'var(--color-accent)' }] },
    options: { responsive: true, plugins: { legend: { display: false } } }
  });
</script>
```

Para tema dinâmico, ler cores via `getComputedStyle(document.documentElement).getPropertyValue('--color-accent')` e reaplicar no `themeChange` event.
