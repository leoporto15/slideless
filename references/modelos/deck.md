# Modelo `deck`

Apresentação moderna sequencial. Slide-by-slide, keyboard nav, fragments, fullscreen, transições. Para pitches ao vivo, all-hands, talks internos.

**Referência mental:** Apple keynotes, Linear launches, Pitch.com modernas.
**Exemplo:** [../../assets/exemplos/exemplo-deck.html](../../assets/exemplos/exemplo-deck.html).
**Template vazio:** [../../assets/templates/template-deck.html](../../assets/templates/template-deck.html).

---

## Anatomia

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                                                             │
│              SLIDE ATIVO (viewport cheio)                   │
│                                                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  HUD: ◀ X / Y ▶                              ⛶ fullscreen   │
└─────────────────────────────────────────────────────────────┘
```

`html, body { height: 100%; overflow: hidden; }`. Cada slide é `position: absolute; inset: 0;` no `.deck` container. Apenas `.is-active` tem `opacity: 1` e `pointer-events: auto`.

---

## Quando usar

| ✓ Use quando | ✗ Não use quando |
|---|---|
| **Apresentação ao vivo** (alguém fala junto) | Distribuição para leitura → [scrollytelling](scrollytelling.md) |
| Narrativa linear (18-25 slides para fonte rica, 12-18 para fonte enxuta) | Conteúdo denso e referencial → [handbook](handbook.md) |
| Tipografia gigante faz sentido | Texto editorial → qualquer outro modelo |
| Há fragments / build sequencial | Conteúdo já tudo visível → [scrollytelling](scrollytelling.md) |

## Expansão vs compactação

**Princípio inegociável:** preservar 100% do conteúdo da fonte. Se a fonte tem 11 marcos na timeline, o deck tem 11 marcos visíveis (talvez divididos em 2 slides). Se tem 3 camadas hierárquicas, todas aparecem. Ver [anti-patterns.md](../anti-patterns.md#c0-compactar--cortar-conte%C3%BAdo-da-fonte-regra-m%C3%A3e).

### Regra de dimensionamento

A heurística "1 slide PPT → 1 slide slideless" está **errada**. PPT corporativo médio tem 4-8 elementos por slide; slideless deck mantém ~3-5 elementos por slide (mais respiração + tipografia maior). Logo:

- **Fonte com 11 slides × 5 elementos médios = ~55 elementos → 18-25 slideless slides**
- Fonte mais densa pede mais expansão; fonte mais magra pode caber em 12-15 slides

### Como contar elementos discretos da fonte

Para cada slide da fonte:
- Cada `<h1>/<h2>` = 1 elemento
- Cada bullet, marco, métrica, nome próprio = 1 elemento
- Cada categoria/subcategoria em diagrama = 1 elemento
- Cada produto/canal/contato listado = 1 elemento
- Cada citação numérica (R$ X, N%, +N) = 1 elemento

Somar tudo. Dividir por 4 (média elementos por slide slideless). Resultado = floor mínimo de slides.

## Compositional variety (obrigatória)

**Não repetir o mesmo layout dois slides seguidos.** Alterne entre os layouts disponíveis para criar pacing:

| Layout | Quando usar |
|---|---|
| `layout-hero` | Capa, encerramento, divisores de capítulo (tipografia mega + glow) |
| `big-num` | Slide-âncora com um número que importa (centro, tipografia giga) |
| `metrics-deck --2/3/4` | 2-4 métricas em destaque com cores semânticas variantes |
| `split` (50/50) | Texto à esquerda + visual/chart/lista à direita |
| `split --start` (5/4) | Texto largo + visual menor |
| `list-deck` | 3-5 itens numerados (fragments opcionais) |
| `grid-cards --2/3/4/6` | Cards color-coded por dimensão semântica |
| `quote-deck` | Citação grande + atribuição |
| `timeline-h` (--cols N) | Marcos horizontais com glow no dot |
| `divider-deck` | Separador de capítulo: número grande + título |
| `table-deck` | Tabela com sticky header e badges semânticos |
| `slide--vignette` | Modificador full-bleed (vinheta sobre conteúdo) |

**Sequência típica de pacing:** hero → split → metrics → divider → grid → big-num → list → split → quote → timeline → metrics → grid → split → quote → encerramento. Nunca: split → split → split.

## Content ceilings

Cada layout tem teto cognitivo:

| Layout | Teto |
|---|---|
| `metrics-deck` | 4 colunas máximo (3 é o sweet spot) |
| `grid-cards --3` | 6 cards (2 linhas) — acima disso → `--4` ou novo slide |
| `list-deck` | 5 itens numerados |
| `timeline-h` | 5-6 colunas (acima → quebrar em 2 slides) |
| `table-deck` | 8 linhas (acima → quebrar ou usar handbook) |
| `quote-deck` | 25 palavras |
| `big-num` | 1 número + 1 label curta |

**Quando estourar o teto:** dividir em N+1 slides, não compactar. Ver C0 em anti-patterns.

---

## Slide engine

```html
<div class="deck">
  <section class="slide is-active" data-slide="1">…</section>
  <section class="slide" data-slide="2">…</section>
  …
</div>

<nav class="hud" aria-label="Controles do deck">
  <button class="hud__prev" type="button" aria-label="Anterior">◀</button>
  <span class="hud__counter"><span id="cur">1</span> / <span id="tot">10</span></span>
  <button class="hud__next" type="button" aria-label="Próximo">▶</button>
  <button class="hud__fs" type="button" aria-label="Fullscreen">⛶</button>
</nav>
```
```css
.slide {
  position: absolute; inset: 0;
  display: flex; flex-direction: column; justify-content: center;
  padding: 8vh 10vw;
  opacity: 0;
  pointer-events: none;
  transform: translateX(40px);
  transition: opacity var(--duration-fade, 700ms) var(--ease-out),
              transform var(--duration-slide, 600ms) var(--ease-in-out);
}
.slide.is-prev { transform: translateX(-40px); }
.slide.is-active { opacity: 1; transform: translateX(0); pointer-events: auto; }

@media (prefers-reduced-motion: reduce) {
  .slide { transition: none !important; opacity: 1; transform: none !important; }
}
```

---

## Keyboard nav (OBRIGATÓRIO)

```js
const slides = [...document.querySelectorAll('.slide')];
let idx = 0;
const fragmentsByIdx = slides.map(s => [...s.querySelectorAll('[data-fragment]')]);
const fragShownByIdx = slides.map(() => 0);

function goto(n) {
  n = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((s, i) => {
    s.classList.toggle('is-active', i === n);
    s.classList.toggle('is-prev', i < n);
  });
  idx = n;
  document.getElementById('cur').textContent = n + 1;
  document.getElementById('tot').textContent = slides.length;
  location.hash = '#s' + (n + 1);
}

function nextFragment() {
  const frags = fragmentsByIdx[idx];
  if (fragShownByIdx[idx] < frags.length) {
    frags[fragShownByIdx[idx]].classList.add('is-visible');
    fragShownByIdx[idx]++;
    return true;
  }
  return false;
}

function next() {
  if (!nextFragment()) goto(idx + 1);
}

function prev() {
  goto(idx - 1);
}

addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); next(); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
  else if (e.key === 'Home') goto(0);
  else if (e.key === 'End') goto(slides.length - 1);
  else if (e.key === 'Escape' && document.fullscreenElement) document.exitFullscreen();
  else if (e.key === 'f') document.documentElement.requestFullscreen();
});

document.querySelector('.hud__prev').addEventListener('click', prev);
document.querySelector('.hud__next').addEventListener('click', next);
document.querySelector('.hud__fs').addEventListener('click', () => {
  if (document.fullscreenElement) document.exitFullscreen();
  else document.documentElement.requestFullscreen();
});

// Hash deep-link: #s5 abre slide 5
const fromHash = parseInt((location.hash.match(/^#s(\d+)$/) || [])[1], 10);
goto(fromHash ? fromHash - 1 : 0);
```

---

## Fragments

Elementos que aparecem em sequência dentro do mesmo slide:

```html
<section class="slide">
  <h2 class="title-md">Resultados</h2>
  <ul class="list">
    <li class="list__item" data-fragment><strong>+34%</strong> em adoção</li>
    <li class="list__item" data-fragment><strong>-60%</strong> em tempo de descoberta</li>
    <li class="list__item" data-fragment><strong>R$ 4.2M</strong> economizados</li>
  </ul>
</section>
```
```css
.slide [data-fragment] {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 500ms var(--ease-out), transform 500ms var(--ease-out);
}
.slide [data-fragment].is-visible { opacity: 1; transform: translateY(0); }
```

---

## Stagger de elementos `data-anim`

Animação de entrada quando o slide se torna ativo:

```html
<section class="slide">
  <p class="kicker" data-anim style="--anim-i: 0">CAPÍTULO 01</p>
  <h2 class="title-xl" data-anim style="--anim-i: 1">Plataforma de Dados</h2>
  <p class="lead" data-anim style="--anim-i: 2">Subtítulo…</p>
</section>
```
```css
.slide [data-anim] {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 700ms var(--ease-out), transform 700ms var(--ease-out);
}
.slide.is-active [data-anim] {
  opacity: 1; transform: translateY(0);
  transition-delay: calc(var(--anim-i, 0) * 80ms + 200ms);
}
```

---

## Tipografia deck (única exceção do design system)

```css
.title-xl  { font-size: clamp(2.75rem, 6.5vw, 6rem);    line-height: 1.02; font-weight: 800; }
.title-lg  { font-size: clamp(2rem, 4.5vw, 3.5rem);     line-height: 1.1;  font-weight: 700; }
.title-md  { font-size: clamp(1.5rem, 2.5vw, 2.25rem);  line-height: 1.15; font-weight: 700; }
.lead      { font-size: clamp(1.125rem, 1.6vw, 1.5rem); }
.big-num__val { font-size: clamp(5rem, 16vw, 14rem);    font-weight: 800; }
```

**Sempre `clamp()`** — fluido com o viewport. Nunca tamanho fixo gigante.

---

## Layouts de slide

| Layout | Quando usar |
|---|---|
| **hero** | Capa / abertura — kicker + title-xl + lead + meta |
| **section divider** | Separador entre capítulos — número grande + title-lg |
| **big-num** | Número-âncora — `.big-num__val` 14rem + label |
| **metrics 3-up** | Três métricas em colunas com `.metric` |
| **list numbered** | Lista 3-5 itens com fragments |
| **two-col** | Texto à esquerda + visual/chart à direita |
| **quote** | Citação grande + atribuição |
| **timeline horizontal** | Marcos em grid de 3-4 colunas |
| **cards 3-up** | Três cards lado a lado |
| **encerramento** | Obrigado + contato + meta |

Cada layout tem classe CSS dedicada. Ver `exemplo-deck.html` para todas.

---

## Print

```css
@media print {
  @page { size: A4 landscape; margin: 0; }
  .hud { display: none; }
  .deck { width: auto; height: auto; overflow: visible; }
  .slide {
    position: relative; inset: auto;
    width: 100vw; height: 100vh;
    page-break-after: always;
    opacity: 1 !important; transform: none !important;
  }
  .slide [data-fragment] { opacity: 1 !important; transform: none !important; }
  .slide [data-anim] { opacity: 1 !important; transform: none !important; }
}
```

---

## Checks específicos

- [ ] Keyboard handler: ArrowRight, ArrowLeft, Space, Home, End, Esc
- [ ] Hash deep-link `#s5` abre slide 5
- [ ] Fragments revelam em ordem (não todos ao entrar no slide)
- [ ] Contador X / Y refletindo posição
- [ ] Toggle fullscreen funcional
- [ ] Transição < 800ms (não cansa apresentador)
- [ ] `prefers-reduced-motion` desabilita transições e mantém opacity 1
- [ ] Slide hero usa `.title-xl` (gigante OK aqui)
- [ ] `padding: 8vh 10vw` no .slide
