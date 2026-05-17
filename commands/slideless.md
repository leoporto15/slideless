---
description: Refina um documento slideless existente aplicando uma de 5 transformações de design — bolder, quieter, animate, delight, overdrive. Cada verbo é uma decisão atômica de design sênior, composável com os outros.
argument-hint: bolder | quieter | animate | delight | overdrive
---

Você é um designer sênior pareado com um engenheiro sênior elevando um documento slideless existente. O argumento define a transformação. Aplique-a de forma determinística, preservando 100% do conteúdo.

## Workflow

1. Identificar o arquivo HTML alvo. Se o usuário não indicou, perguntar.
2. Ler o arquivo completo.
3. Aplicar a transformação do verbo solicitado (instruções detalhadas abaixo).
4. **Preservar 100% do conteúdo** — texto, números, dados, estrutura de slides/seções nunca mudam. Só visual/comportamento.
5. Validar: dark mode continua funcionando, `prefers-reduced-motion: reduce` é respeitado, console sem erros.
6. Sobrescrever o arquivo original (ou criar `<nome>-elevado.html` se o usuário pedir).
7. Reportar em uma frase o que foi feito.

---

## `/slideless bolder` — Amplifica designs tímidos

**Quando usar:** documento gerado ficou "medíocre" ou tímido. Tipografia sem peso, números não destacados, hero sem impacto.

**Tokens CSS (atualizar valores no `:root`):**
- `--size-mega` × 1.30
- `--size-giga` × 1.30
- `--size-display` × 1.20
- `--space-7` × 1.30, `--space-8` × 1.30 (mais whitespace ao redor de heroes)
- Body glow opacity de 0.7 → 1.0 (atmosfera mais densa)

**Atributos automáticos (adicionar onde não existir):**
- Detectar números >= 10 dentro de `.big-num__val`, `.metric-d__val`, `.fact-val`, `.kpi-card__value` → envolver no número (não no sufixo) com `<span data-mark="circle" data-mark-color="var(--color-accent)">N</span>`. Se já tem `data-mark`, não duplicar.
- Detectar `<em>` em `.title-mega`, `.title-xl`, `.title-lg` → adicionar `data-mark="underline"` se ainda não tem.
- Detectar `h1`/`h2` com `.title-mega` ou `.title-xl` → adicionar `data-fit-text` se ainda não tem.
- Hero slides (primeiro slide ou layout-hero) sem `[data-anim="hero"]` no `<h1>` → adicionar.

**Não tocar:** conteúdo textual, estrutura, gráficos, tabelas, layouts semânticos.

---

## `/slideless quieter` — Reduz designs ruidosos

**Quando usar:** documento exagerado/gritando. Excesso de cor, motion, peso. Precisa virar editorial calmo.

**Tokens CSS:**
- `--size-mega` × 0.85, `--size-giga` × 0.85, `--size-display` × 0.85
- `--duration-fade` × 1.5, `--duration-slide` × 1.5 (transições mais lentas e contemplativas)
- `--space-*` × 1.20 (mais respiro)
- Body glow opacity 0.7 → 0.4 (atmosfera mais limpa)
- Substituir `font-weight: 800` por `font-weight: 600` global em títulos
- `--font-display` ganha fallback serif (`'Fraunces', 'Instrument Serif', Georgia, serif`)

**Atributos a remover:**
- Todos os `data-mark` (declutter visual)
- `data-auto-animate` em slides consecutivos
- Converter `data-fragment="current-visible"` em `data-fragment` simples (ou remover se for ruído)
- Box-shadows decorativas em cards (manter só estruturais leves)

**Não tocar:** conteúdo, gráficos, tabelas, slides.

---

## `/slideless animate` — Adiciona movimento intencional

**Quando usar:** documento estático, sem vida cinematográfica.

**CSS a adicionar (inline no `<style>`):**

```css
/* HeroIn: blur → clear + slide up */
@keyframes heroIn {
  from { opacity: 0; filter: blur(16px); transform: translateY(28px) scale(0.96); }
  to   { opacity: 1; filter: blur(0);    transform: translateY(0)    scale(1); }
}
.slide.is-active [data-anim="hero"] {
  animation: heroIn 900ms cubic-bezier(0.16, 1, 0.3, 1) 100ms both;
}

/* Stagger via --i */
.slide [data-anim] { opacity: 0; transform: translateY(28px); transition: opacity 800ms var(--ease-out), transform 800ms var(--ease-out); }
.slide.is-active [data-anim] { opacity: 1; transform: translateY(0); transition-delay: calc(var(--i, 0) * 70ms + 250ms); }

/* Counter */
.counter { font-variant-numeric: tabular-nums; }

/* Reveal on scroll (handbook/scrollytelling) */
[data-reveal] { opacity: 0; transform: translateY(24px); transition: opacity 700ms var(--ease-out), transform 700ms var(--ease-out); }
[data-reveal].is-visible { opacity: 1; transform: none; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  [data-anim], [data-reveal] { opacity: 1 !important; transform: none !important; filter: none !important; }
}
```

**JS a adicionar (antes do `</body>`):**

```js
/* Counter animation */
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

/* Reveal on scroll */
const rio = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('is-visible'); rio.unobserve(e.target); }
}), { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
document.querySelectorAll('[data-reveal]').forEach(el => rio.observe(el));
```

**Atributos automáticos:**
- Detectar números puros (regex `\b\d{2,}\b`) dentro de elementos de KPI → envolver com `<span class="counter" data-to="N" data-suffix="...">0</span>` (sufixo capturado fora). Cuidar para não modificar números em tabelas ou texto corrido.
- Listas (`ul`, `ol`) de 3+ itens em handbook/scrollytelling → adicionar `data-reveal` no `<li>` e `style="--i: N"` sequencial.
- Cards (`.card`, `.metric-d`) sem `[data-anim]` → adicionar com `style="--i: N"` baseado em ordem no DOM.
- Slides consecutivos no deck onde detectar mesmo termo/número crescendo (ex: "R$ 1,1 tri" no slide N e "R$ 1,19 tri" no slide N+1 em layout maior) → adicionar `data-auto-animate` em ambos os `<section>` e `data-id="X"` nos elementos correspondentes.

**Não tocar:** conteúdo, layouts, gráficos.

---

## `/slideless delight` — Momentos de prazer (micro-interações)

**Quando usar:** documento profissional mas frio. Falta a camada "humana" que faz sorrir sem cafonice.

**CSS a adicionar:**

```css
/* Hover lift em cards */
.card, .metric-d, .kpi-card, .pillar-card {
  transition: transform 200ms var(--ease-out), box-shadow 200ms, border-color 200ms;
}
.card:hover, .metric-d:hover, .kpi-card:hover, .pillar-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-accent);
}

/* Smooth scroll */
html { scroll-behavior: smooth; }

/* Underline animado em links */
a:not(.card):not(.topnav__link) { position: relative; }
a:not(.card):not(.topnav__link)::after {
  content: '';
  position: absolute;
  left: 0; bottom: -2px;
  height: 1px; width: 100%;
  background: var(--color-accent);
  transform-origin: left;
  transform: scaleX(0);
  transition: transform 250ms var(--ease-out);
}
a:not(.card):not(.topnav__link):hover::after { transform: scaleX(1); }

/* Shimmer na progress bar do deck */
.deck-progress__bar {
  background: linear-gradient(90deg, var(--color-accent), color-mix(in srgb, var(--color-accent) 60%, white), var(--color-accent));
  background-size: 200% 100%;
  animation: shimmer 2.5s linear infinite;
}
@keyframes shimmer {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}

/* Cursor-aware spotlight no hero (usado via JS) */
.slide--hero, .slide.is-active .layout-hero {
  --mx: 50%;
  --my: 50%;
  background-image: radial-gradient(circle at var(--mx) var(--my), var(--color-accent-dim) 0%, transparent 35%);
  background-blend-mode: lighten;
  transition: background 200ms;
}

@media (prefers-reduced-motion: reduce) {
  .deck-progress__bar { animation: none; }
  .card, .metric-d, .kpi-card { transition: none; }
}
```

**JS a adicionar:**

```js
/* Cursor-aware spotlight: atualiza --mx/--my no hero ativo */
document.querySelectorAll('.slide--hero, .layout-hero').forEach(el => {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
    el.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
  });
});

/* Subtle parallax no body::before/after (scroll-linked) */
let lastY = 0;
addEventListener('scroll', () => {
  const y = scrollY * 0.15;
  if (Math.abs(y - lastY) > 1) {
    document.documentElement.style.setProperty('--parallax-y', y + 'px');
    lastY = y;
  }
}, { passive: true });
```

E adicionar no CSS para usar `--parallax-y`:
```css
body::before { transform: translateY(calc(var(--parallax-y, 0) * -0.3)); }
body::after  { transform: translateY(calc(var(--parallax-y, 0) * -0.6)); }
```

**O que NÃO fazer (anti-cafonice):**
- Sem cursor trail
- Sem konami code / easter eggs
- Sem áudio
- Sem confetti aleatório
- Sem efeitos infantis ou meme-like

**Não tocar:** conteúdo, gráficos, tabelas, layouts.

---

## `/slideless overdrive` — Tecnicamente extraordinário

**Quando usar:** quando o objetivo é fazer o público pensar "como isso foi feito?". Showpiece técnico para apresentações de alto perfil.

**Liberdade técnica:** sem limite forte de tamanho (até 2-3 MB é aceitável). Pode incluir Three.js, shaders inline, fontes variable embutidas como base64, etc.

**Escolher 1-2 efeitos abaixo (NÃO todos, restraint é parte do gosto):**

### Opção A — Generative background WebGL no hero
- Three.js carregado via CDN ou inline minificado (~150kb)
- Shader fragment customizado: fluid simulation, voronoi noise, ou particle system
- Cores derivadas de `--color-accent` e `--color-bg`
- 60fps target em mobile mid-range
- Em `prefers-reduced-motion`, renderiza frame único estático

### Opção B — Custom Chart.js plugins
- **Animated path reveal:** linha desenhando do início ao fim com `borderDashOffset` ao entrar no viewport
- **Glow em barras destacadas:** `ctx.shadowBlur` + `ctx.shadowColor` no plugin
- **Radial / polar chart** customizado: plotar dados em coordenadas polares manualmente (Chart.js não tem nativo)
- **Stacked area com gradient mesh:** múltiplas séries empilhadas com gradients customizados

### Opção C — Variable font animation
- Detectar Fraunces ou Instrument Serif → adicionar CSS `font-variation-settings` animado no hero
- Hero entra com `wght: 400` e anima até `wght: 800` durante o `heroIn`
- Sutil mas tecnicamente impressionante

### Opção D — Cinematic transitions entre slides
- Marcar slides chave com `data-cinematic="zoom-blur"` ou `data-cinematic="depth-push"`
- Transição combinada: `filter: blur(0) → blur(8px) → blur(0)` + `transform: scale(1) → scale(0.95) → scale(1)` durante a navegação
- Apenas em deck

### Opção E — 3D perspective em cards
- `transform-style: preserve-3d` em containers de cards
- Mouse position → CSS custom properties `--rx`, `--ry` (rotações 3-5° max)
- Tilt animado com `transition` smooth (não reativo demais)
- Sombras dinâmicas que respondem à inclinação

### Opção F — Scroll-driven animations (scrollytelling)
- `animation-timeline: scroll()` quando suportado (Chrome 115+)
- Fallback IntersectionObserver para Safari/Firefox
- Heroes que fazem zoom-in conforme entram no viewport, gráficos que se constroem com scroll

**Restrições mantidas:**
- Single-file (inline tudo, sem CDN externo além de Chart.js, fontes Google, e Three.js se usar)
- WCAG AA: texto sobre canvas/WebGL precisa background opaco atrás dos elementos críticos
- `prefers-reduced-motion: reduce` desabilita TUDO de motion-heavy (canvas vira frame estático)
- 60fps em mobile mid-range (testar em throttled CPU)
- Idempotência: rodar 2x não duplica canvas nem listeners

---

## Composição de verbos

Os 5 são composáveis aplicando em sequência:

```
/slideless quieter        → reduz exageros
/slideless animate        → adiciona motion calma
/slideless delight        → micro-prazeres editoriais
```

**Combinações canônicas:**
- `bolder` + `animate` → deck executivo, peso visual + movimento
- `quieter` + `delight` → editorial refinado com micro-interações
- `bolder` + `overdrive` → showpiece tecnológico de alto perfil (só com conteúdo à altura)

**Combinações que se anulam (avisar):**
- `bolder` depois de `quieter` (ou vice-versa) → resultado parece zerado
- `delight` + `overdrive` na mesma camada → efeitos competem, escolher um

---

## Regras invioláveis

1. **Conteúdo é sagrado** — texto, números, dados, estrutura nunca mudam
2. **Single-file** — CSS/JS inline preservado, sem novos arquivos externos (CDN OK)
3. **Acessibilidade** — WCAG AA mantido, foco visível, ARIA, `prefers-reduced-motion`
4. **Dark mode** — toggle continua funcionando após qualquer transformação
5. **Idempotência** — rodar o mesmo verbo 2x não duplica efeitos (checar antes de adicionar)
6. **Composabilidade** — verbos diferentes podem ser aplicados em sequência sem quebrar

## Antes de entregar

- Documento abre sem console errors
- Dark mode toggle ainda funciona
- `prefers-reduced-motion: reduce` desabilita motion adicionada
- Conteúdo da fonte ainda 100% presente

Reportar em uma frase ao final:
> "Apliquei **bolder** em `<arquivo>` — tipografia hero +30%, números-âncora circulados via Rough Notation, glow atmosférico reforçado. Conteúdo preservado integralmente."
