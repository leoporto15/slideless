# Slide Patterns — slideless deck

Referência completa para o modelo `deck`. Ler antes de gerar qualquer apresentação.

---

## Arquitetura do slide deck

```
.deck (scroll-snap container, 100dvh)
  └── .slide × N (cada um = 100dvh, scroll-snap-align: start)
       ├── .slide-num (posição: absolute top-left)
       ├── [layout: hero | big-num | metrics | list | split | cards | divider | quote | timeline | table | full-bleed]
       └── .reveal × M (animações stagger por --i)
```

**Modelo de navegação:** scroll-snap + keyboard (ArrowRight/ArrowLeft/Space) + nav dots + counter + fullscreen.

---

## CSS do Deck Engine

```css
/* Container principal — scroll-snap */
html, body { height: 100%; margin: 0; }
body { overflow: hidden; overscroll-behavior: none; }

.deck {
  height: 100dvh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Slide base */
.slide {
  height: 100dvh;
  scroll-snap-align: start;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(36px, 6vh, 80px) clamp(40px, 8vw, 120px);
  isolation: isolate;
}

/* Transição cinematic — aplica classes via JS */
.slide .reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 600ms cubic-bezier(0.16, 1, 0.3, 1),
              transform 600ms cubic-bezier(0.16, 1, 0.3, 1);
}
.slide.is-visible .reveal {
  opacity: 1;
  transform: none;
}
/* Stagger via --i (define em style="--i: N" no HTML) */
.slide.is-visible .reveal:nth-child(1) { transition-delay: 0.08s; }
.slide.is-visible .reveal:nth-child(2) { transition-delay: 0.16s; }
.slide.is-visible .reveal:nth-child(3) { transition-delay: 0.24s; }
.slide.is-visible .reveal:nth-child(4) { transition-delay: 0.32s; }
.slide.is-visible .reveal:nth-child(5) { transition-delay: 0.40s; }
.slide.is-visible .reveal:nth-child(6) { transition-delay: 0.48s; }

/* Hero unblur */
.slide.is-visible .reveal--hero {
  animation: heroUnblur 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.08s both;
}
@keyframes heroUnblur {
  from { opacity: 0; filter: blur(16px); transform: translateY(28px) scale(0.96); }
  to   { opacity: 1; filter: blur(0);    transform: none; }
}

@media (prefers-reduced-motion: reduce) {
  .slide .reveal, .slide.is-visible .reveal--hero {
    opacity: 1 !important; transform: none !important;
    animation: none !important; transition: none !important;
    filter: none !important;
  }
}
```

### Chrome (HUD + Progress + Dots)

```css
/* Progress bar top */
.deck-progress {
  position: fixed; top: 0; left: 0; right: 0;
  height: 3px; background: var(--color-border); z-index: 200;
}
.deck-progress__bar {
  height: 100%;
  background: var(--color-accent);
  transition: width 300ms var(--ease-out);
}

/* Nav dots — right side */
.deck-dots {
  position: fixed; right: clamp(12px, 2vw, 28px); top: 50%;
  transform: translateY(-50%);
  display: flex; flex-direction: column; gap: 10px;
  z-index: 150;
}
.deck-dot {
  width: 7px; height: 7px;
  background: var(--color-fg-subtle); opacity: 0.35;
  border-radius: 50%; border: none; cursor: pointer;
  transition: all 200ms var(--ease-out);
  padding: 0;
}
.deck-dot:hover { opacity: 0.6; }
.deck-dot.active { opacity: 1; transform: scale(1.6); background: var(--color-accent); }

/* Counter + HUD bottom-center */
.deck-hud {
  position: fixed; bottom: 18px; left: 0; right: 0;
  display: flex; justify-content: center; align-items: center;
  gap: 10px; z-index: 150;
}
.hud-btn {
  width: 38px; height: 38px; display: grid; place-items: center;
  background: var(--color-bg-elevated); border: 1px solid var(--color-border);
  border-radius: 999px; cursor: pointer; color: var(--color-fg);
  font: inherit; font-size: 1rem;
  transition: all 150ms var(--ease-out);
  box-shadow: var(--shadow-sm);
}
.hud-btn:hover { border-color: var(--color-accent); transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.hud-counter {
  font-family: var(--font-mono); font-size: 0.875rem;
  color: var(--color-fg-muted); font-weight: 600;
  min-width: 60px; text-align: center;
  font-variant-numeric: tabular-nums;
}
.hud-counter strong { color: var(--color-fg); }

/* Keyboard hint — aparece e some após 4s */
.deck-hint {
  position: fixed; bottom: 18px; left: 50%; transform: translateX(-50%);
  font-family: var(--font-mono); font-size: 0.75rem;
  color: var(--color-fg-subtle); z-index: 140;
  opacity: 0; transition: opacity 400ms;
  pointer-events: none;
}
.deck-hint.visible { opacity: 1; }
```

---

## JavaScript — SlideEngine (~300 linhas)

```js
(function SlideEngine() {
  const deck    = document.querySelector('.deck');
  const slides  = [...document.querySelectorAll('.slide')];
  const total   = slides.length;
  if (!deck || !total) return;

  /* Build chrome */
  const progressBar = Object.assign(document.createElement('div'), { className: 'deck-progress' });
  const progressFill = Object.assign(document.createElement('div'), { className: 'deck-progress__bar' });
  progressBar.appendChild(progressFill);
  document.body.prepend(progressBar);

  const dotsWrap = Object.assign(document.createElement('div'), { className: 'deck-dots', role: 'tablist', 'aria-label': 'Slides' });
  slides.forEach((_, i) => {
    const dot = Object.assign(document.createElement('button'), {
      className: 'deck-dot', type: 'button',
      'aria-label': `Slide ${i + 1}`, 'aria-selected': i === 0
    });
    dot.role = 'tab';
    dot.addEventListener('click', () => goTo(i));
    dotsWrap.appendChild(dot);
  });
  document.body.appendChild(dotsWrap);

  const hud     = Object.assign(document.createElement('nav'), { className: 'deck-hud', 'aria-label': 'Controles' });
  const prevBtn = Object.assign(document.createElement('button'), { className: 'hud-btn', type: 'button', 'aria-label': 'Slide anterior', textContent: '◀', title: '← / PageUp' });
  const counter = Object.assign(document.createElement('span'), { className: 'hud-counter' });
  const nextBtn = Object.assign(document.createElement('button'), { className: 'hud-btn', type: 'button', 'aria-label': 'Próximo slide', textContent: '▶', title: '→ / Space' });
  const fsBtn   = Object.assign(document.createElement('button'), { className: 'hud-btn', type: 'button', 'aria-label': 'Fullscreen', textContent: '⛶', title: 'F' });
  const themeBtn = document.querySelector('.theme-toggle');
  hud.append(prevBtn, counter, nextBtn, fsBtn);
  if (themeBtn) hud.appendChild(themeBtn.cloneNode(true));
  document.body.appendChild(hud);

  /* Keyboard hint */
  const hint = Object.assign(document.createElement('div'), { className: 'deck-hint', textContent: '← → para navegar · F para fullscreen' });
  document.body.appendChild(hint);
  hint.classList.add('visible');
  let hintTimer = setTimeout(() => hint.classList.remove('visible'), 4000);

  /* Fragments per slide */
  const frags = slides.map(s => [...s.querySelectorAll('[data-fragment]')]);
  const fragIdx = slides.map(() => 0);

  let current = 0;

  function updateChrome(n) {
    progressFill.style.width = ((n + 1) / total * 100) + '%';
    counter.innerHTML = `<strong>${n + 1}</strong> / ${total}`;
    dotsWrap.querySelectorAll('.deck-dot').forEach((d, i) => {
      d.classList.toggle('active', i === n);
      d.setAttribute('aria-selected', i === n);
    });
    history.replaceState(null, '', '#s' + (n + 1));
  }

  function markVisible(n) {
    slides.forEach((s, i) => s.classList.toggle('is-visible', i === n));
  }

  function goTo(n) {
    n = Math.max(0, Math.min(total - 1, n));
    current = n;
    slides[n].scrollIntoView({ behavior: 'smooth', block: 'start' });
    markVisible(n);
    updateChrome(n);
  }

  function revealNextFragment() {
    const f = frags[current];
    const idx = fragIdx[current];
    if (idx < f.length) { f[idx].classList.add('is-visible'); fragIdx[current]++; return true; }
    return false;
  }

  function next() { if (!revealNextFragment()) goTo(current + 1); }
  function prev() { goTo(current - 1); }

  /* Keyboard */
  document.addEventListener('keydown', e => {
    clearTimeout(hintTimer);
    hint.classList.remove('visible');
    if (['ArrowRight', 'Space', 'PageDown'].includes(e.code)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'PageUp'].includes(e.code)) { e.preventDefault(); prev(); }
    else if (e.code === 'Home') goTo(0);
    else if (e.code === 'End')  goTo(total - 1);
    else if (e.code === 'KeyF') document.documentElement.requestFullscreen?.();
    else if (e.code === 'Escape' && document.fullscreenElement) document.exitFullscreen();
  });

  prevBtn.addEventListener('click', prev);
  nextBtn.addEventListener('click', next);
  fsBtn.addEventListener('click', () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen?.();
  });

  /* Touch swipe */
  let touchX = 0, touchY = 0;
  deck.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; touchY = e.touches[0].clientY; }, { passive: true });
  deck.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - touchX;
    const dy = e.changedTouches[0].clientY - touchY;
    if (Math.abs(dx) < Math.abs(dy)) return;
    if (dx < -40) next();
    else if (dx > 40) prev();
  }, { passive: true });

  /* IntersectionObserver — detect active slide via scroll */
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting && e.intersectionRatio > 0.5) {
        const n = slides.indexOf(e.target);
        if (n === -1) return;
        current = n;
        markVisible(n);
        updateChrome(n);
      }
    });
  }, { root: deck, threshold: 0.5 });
  slides.forEach(s => io.observe(s));

  /* Initial state */
  const fromHash = parseInt((location.hash.match(/^#s(\d+)$/) || [])[1], 10);
  const start = fromHash ? Math.max(0, fromHash - 1) : 0;
  goTo(start);

  /* Theme toggle clone */
  hud.querySelectorAll('.theme-toggle').forEach(btn => btn.addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme');
    const nx = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nx);
    try { localStorage.setItem('theme', nx); } catch {}
  }));
})();
```

---

## 10 Slide Types

### Type 1 — Title (hero)
```html
<section class="slide slide--title">
  <p class="kicker reveal"><span class="kicker__dot"></span>SEÇÃO 01</p>
  <h1 class="slide__display reveal reveal--hero">Título <em>principal</em></h1>
  <p class="slide__body reveal" style="--i:2">Subtítulo em uma ou duas frases.</p>
  <div class="slide__meta reveal" style="--i:3">
    <span><strong>Apresentador</strong>Cargo · Equipe</span>
    <span><strong>Data</strong>AAAA-MM-DD</span>
  </div>
</section>
```

### Type 2 — Section Divider
```html
<section class="slide slide--divider">
  <div class="divider-content">
    <span class="divider-num reveal">02</span>
    <h2 class="slide__heading reveal" style="--i:1">Nome da Seção</h2>
    <p class="slide__body reveal" style="--i:2">Descrição opcional da seção.</p>
  </div>
</section>
```
```css
.slide--divider { background: var(--color-bg-sunken); }
.divider-num {
  font-family: var(--font-display);
  font-size: clamp(100px, 20vw, 200px);
  font-weight: 200;
  letter-spacing: -0.06em;
  line-height: 0.9;
  color: var(--color-fg);
  opacity: 0.06;
  position: absolute;
  right: 8vw; bottom: 10vh;
  pointer-events: none;
}
```

### Type 3 — Content (heading + text + bullets)
```html
<section class="slide slide--content">
  <p class="kicker reveal"><span class="kicker__dot"></span>TÓPICO</p>
  <h2 class="slide__heading reveal" style="--i:1">Heading principal</h2>
  <ul class="slide__list reveal" style="--i:2">
    <li>Ponto A — descrição</li>
    <li>Ponto B — descrição</li>
    <li>Ponto C — descrição</li>
  </ul>
</section>
```

### Type 4 — Split (heading + dois painéis)
```html
<section class="slide slide--split">
  <h2 class="slide__heading reveal">Heading</h2>
  <div class="slide-split reveal" style="--i:1">
    <div class="split-panel split-panel--left">
      <p class="panel-label">Esquerda</p>
      <p>Conteúdo do painel esquerdo.</p>
    </div>
    <div class="split-panel split-panel--right">
      <p class="panel-label">Direita</p>
      <p>Conteúdo do painel direito.</p>
    </div>
  </div>
</section>
```
```css
.slide-split {
  display: grid; grid-template-columns: 1fr 1fr; gap: 5vw;
  align-items: start; margin-top: var(--space-6);
}
.split-panel { padding: var(--space-5); background: var(--color-bg-elevated);
  border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
.panel-label { font-family: var(--font-mono); font-size: var(--size-xs);
  text-transform: uppercase; letter-spacing: 0.1em; color: var(--color-fg-subtle); margin: 0 0 var(--space-3); }
```

### Type 5 — Diagram (Mermaid ou SVG)
```html
<section class="slide slide--diagram">
  <h2 class="slide__heading reveal">Arquitetura</h2>
  <div class="diagram-shell reveal" style="--i:1">
    <div class="zoom-controls"><!-- botões --></div>
    <div class="mermaid-viewport">
      <div class="mermaid mermaid-canvas">graph TD ...</div>
    </div>
  </div>
</section>
```

### Type 6 — Dashboard (cards KPI + gráfico)
```html
<section class="slide slide--dashboard">
  <p class="kicker reveal">MÉTRICAS</p>
  <div class="kpi-row reveal" style="--i:1">
    <div class="kpi-card">
      <p class="kpi-label">AuM Total</p>
      <p class="kpi-value">R$<span>1,19</span>tri</p>
      <canvas class="kpi-spark" id="spark-aum" aria-label="Sparkline AuM"></canvas>
    </div>
    <!-- mais kpi-cards -->
  </div>
  <canvas class="chart-main reveal" style="--i:2" id="chart-dash" aria-label="Gráfico principal"></canvas>
</section>
```

### Type 7 — Table (dados tabulares)
```html
<section class="slide slide--table">
  <h2 class="slide__heading reveal">Nome da Tabela</h2>
  <div class="table-wrap reveal" style="--i:1">
    <table class="data-table">
      <thead><tr><th>Coluna A</th><th class="num">Valor</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td>Item 1</td><td class="num">R$ 100bi</td><td><span class="badge badge--success">Ativo</span></td></tr>
      </tbody>
    </table>
  </div>
</section>
```

### Type 8 — Code
```html
<section class="slide slide--code">
  <h2 class="slide__heading reveal">Exemplo de código</h2>
  <div class="code-file reveal" style="--i:1">
    <div class="code-file__header"><span class="dot"></span>arquivo.py</div>
    <pre class="code-file__body"><code>def hello():
    return "world"</code></pre>
  </div>
</section>
```

### Type 9 — Quote
```html
<section class="slide slide--quote">
  <div class="quote-wrap reveal">
    <blockquote class="quote-text">"A citação mais importante do documento, em uma a três linhas."</blockquote>
    <cite class="quote-cite"><strong>Nome</strong>Cargo · Empresa</cite>
  </div>
</section>
```
```css
.slide--quote { align-items: center; text-align: center; }
.quote-wrap { max-width: 30ch; }
.quote-text {
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 1.2rem + 2.5vw, 3rem);
  font-weight: 600; font-style: italic;
  line-height: 1.2; letter-spacing: -0.02em;
  color: var(--color-fg); margin: 0 0 var(--space-6);
  quotes: '\201C' '\201D';
}
.quote-text::before { content: open-quote; color: var(--color-accent); }
.quote-cite { font-style: normal; display: block;
  font-size: var(--size-small); color: var(--color-fg-muted); }
.quote-cite strong { display: block; color: var(--color-fg); font-weight: 700;
  font-family: var(--font-display); font-size: var(--size-body); margin-bottom: 4px; }
```

### Type 10 — Full-Bleed (imagem / cor sólida)
```html
<section class="slide slide--full-bleed" style="background: var(--color-bg-sunken);">
  <!-- ou background-image para imagem -->
  <div class="fb-overlay reveal">
    <h2 class="slide__heading" style="color: var(--color-fg)">Heading</h2>
    <p class="slide__body">Texto sobre fundo.</p>
  </div>
</section>
```
```css
.slide--full-bleed { padding: 0; overflow: hidden; }
.slide--full-bleed::after {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse 100% 80% at 50% 50%, transparent 40%, rgba(0,0,0,0.18) 100%);
  pointer-events: none;
}
.fb-overlay {
  position: relative; z-index: 1;
  padding: clamp(36px, 6vh, 80px) clamp(40px, 8vw, 120px);
}
```

---

## Tipografia global do deck

```css
.slide__display {
  font-family: var(--font-display);
  font-size: clamp(48px, 10vw, 110px);
  font-weight: 800; letter-spacing: -0.04em; line-height: 0.95;
  margin: 0 0 var(--space-5);
}
.slide__display em { color: var(--color-accent); font-style: italic; }

.slide__heading {
  font-family: var(--font-display);
  font-size: clamp(28px, 5vw, 52px);
  font-weight: 700; letter-spacing: -0.025em; line-height: 1.05;
  margin: 0 0 var(--space-5);
}
.slide__heading em { color: var(--color-accent); font-style: italic; }

.slide__body {
  font-size: clamp(16px, 2.2vw, 24px);
  line-height: 1.55; color: var(--color-fg-muted);
  max-width: 55ch;
}

.slide__list {
  list-style: none; padding: 0;
  display: flex; flex-direction: column; gap: var(--space-4);
  margin: var(--space-5) 0 0;
}
.slide__list li {
  font-size: clamp(15px, 1.8vw, 20px);
  line-height: 1.45; color: var(--color-fg);
  padding-left: 1.4em; position: relative;
}
.slide__list li::before {
  content: '→'; position: absolute; left: 0;
  color: var(--color-accent); font-weight: 700;
}

.kicker {
  display: inline-flex; align-items: center; gap: 12px;
  font-family: var(--font-mono);
  font-size: clamp(10px, 1.1vw, 13px);
  font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--color-fg-muted);
  margin: 0 0 var(--space-6);
}
.kicker__dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--color-accent); flex-shrink: 0;
}
.kicker--accent { color: var(--color-accent); }

.slide__meta {
  display: flex; gap: var(--space-8); flex-wrap: wrap;
  margin-top: var(--space-8);
  font-size: clamp(13px, 1.5vw, 16px);
  color: var(--color-fg-subtle);
}
.slide__meta span > strong {
  display: block; color: var(--color-fg); font-weight: 700;
  font-family: var(--font-display); font-size: 1.05em; margin-bottom: 3px;
}

.slide-num {
  position: absolute; top: 22px; left: 28px;
  font-family: var(--font-mono); font-size: 0.6875rem;
  font-weight: 600; letter-spacing: 0.12em;
  color: var(--color-fg-subtle); z-index: 10;
}
.slide-num strong { color: var(--color-accent); }
```

---

## 4 Presets de Estética

### Preset A — Warm Signal (padrão Itaú)
```css
/* Usa os tokens do tema itau.css diretamente.
   Background: cream #faf7f5 com glow laranja topo + azul rodapé.
   Fonte display: Fraunces ou Itaú Display (fallback). */
body {
  background: var(--color-bg);
  background-image: var(--glow-hero), var(--glow-cool);
}
```

### Preset B — Midnight Editorial
```css
/* Dark profundo com serif headlines e acentos dourados. */
:root {
  --color-bg: #0f0e0c;
  --color-bg-elevated: #1a1813;
  --color-bg-sunken: #0a0908;
  --color-fg: #f0ead8;
  --color-fg-muted: #a09070;
  --color-accent: #d4a73a;
  --color-accent-dim: rgba(212, 167, 58, 0.10);
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-mono: 'JetBrains Mono', monospace;
}
/* Forçar dark no boot script: document.documentElement.setAttribute('data-theme','dark') */
body {
  background: var(--color-bg);
  background-image: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(212,167,58,0.10) 0%, transparent 60%);
}
```

### Preset C — Terminal Mono
```css
/* Verde/amber em near-black. Monospace tudo. */
:root {
  --color-bg: #0c0c0a;
  --color-bg-elevated: #141410;
  --color-fg: #c8e88a;
  --color-fg-muted: #7a9a4a;
  --color-accent: #b8e040;
  --color-accent-dim: rgba(184, 224, 64, 0.08);
  --font-text: 'IBM Plex Mono', monospace;
  --font-display: 'IBM Plex Mono', monospace;
  --font-mono: 'IBM Plex Mono', monospace;
}
body { background: var(--color-bg); }
.slide__display { font-weight: 700; font-style: normal; }
```

### Preset D — Swiss Clean
```css
/* Neutro sans-serif, mínima cor, alto whitespace. */
:root {
  --color-bg: #f8f8f6;
  --color-bg-elevated: #ffffff;
  --color-fg: #1a1a1a;
  --color-fg-muted: #6b6b6b;
  --color-accent: #1a1a1a;
  --color-accent-dim: rgba(26, 26, 26, 0.06);
  --font-text: 'IBM Plex Sans', system-ui, sans-serif;
  --font-display: 'IBM Plex Sans', system-ui, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}
.slide__display { letter-spacing: -0.05em; }
```

---

## Regras do deck

1. **Tipografia gigante** — `clamp()` obrigatório (nunca px fixo). `.slide__display` = `clamp(48px, 10vw, 110px)`.
2. **Variar spatial approach** — a cada 3 slides centered, forçar um off-axis (split/left-heavy/full-bleed).
3. **Expansão vs compactação** — se fonte tem 10 slides com 4 elementos cada, gerar 14-18 slides slideless (não 1:1).
4. **Fragmentos** — elementos `[data-fragment]` revelam por click (Space/→ em fragmentos antes de avançar slide).
5. **Nenhum slide em branco** — cada slide carrega informação real da fonte. 0 slides de "logo" ou "encerramento" sem conteúdo.
6. **Gráfico quando há dado** — se o slide cita número que evoluiu no tempo, adicionar Chart.js. Se compara categorias, adicionar bar/donut.
7. **Tabela quando há lista comparativa** — mesas, fundos, diretoria, produtos → `<table>` com `.data-table`, nunca lista de bullets.

---

## Checklist deck

- [ ] Slide engine funciona (navegação teclado, dots, counter, fullscreen)?
- [ ] Progress bar atualiza?
- [ ] Tipografia usa `clamp()`?
- [ ] Variedade de layouts (pelo menos 5 tipos diferentes)?
- [ ] Fragments onde há itens sequenciais?
- [ ] Dark mode sem flash?
- [ ] Conteúdo 100% da fonte (nada omitido)?
- [ ] Gráficos onde há dados temporais/comparativos?
- [ ] Tabelas onde há listas de itens com atributos?
