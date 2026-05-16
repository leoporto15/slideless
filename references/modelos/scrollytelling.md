# Modelo `scrollytelling`

Narrativa única com reveal-on-scroll, counters animados, sticky chart. Para relatórios anuais interativos, casos de estudo, narrativas editoriais de projeto.

**Referência mental:** NYT The Upshot, The Pudding, Apple product pages.
**Exemplo:** [../../assets/exemplos/exemplo-scrollytelling.html](../../assets/exemplos/exemplo-scrollytelling.html).
**Template vazio:** [../../assets/templates/template-scrollytelling.html](../../assets/templates/template-scrollytelling.html).

---

## Anatomia

```
┌─────────────────────────────────────────────────────────────┐
│  progress bar (sticky no topo, 2px)                         │
├─────────────────────────────────────────────────────────────┤
│  hero (h1 + lead + meta)                                    │
├─────────────────────────────────────────────────────────────┤
│  cena 1 — texto à esquerda + chart sticky à direita        │
│           (chart muda quando entra cena 2)                  │
├─────────────────────────────────────────────────────────────┤
│  cena 2 — texto + chart muda                                │
├─────────────────────────────────────────────────────────────┤
│  cena 3 — métricas com counters                             │
├─────────────────────────────────────────────────────────────┤
│  footer — assinatura, data, link                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Quando usar

| ✓ Use quando | ✗ Não use quando |
|---|---|
| Narrativa linear (começo → meio → fim) | Conteúdo referencial → [handbook](handbook.md) |
| Dados que pedem chart com mudanças | Texto puro sem visualização → [handbook](handbook.md) |
| Leitor vai ler 1× (não consulta) | Múltiplas dimensões independentes → [hub](hub.md) |
| 4-12 cenas verticais | 20+ seções → [handbook](handbook.md) |
| Tom editorial/jornalístico | Pitch ao vivo → [deck](deck.md) |

---

## Progress bar

```html
<div class="progress" aria-hidden="true">
  <div class="progress__bar" id="progress-bar"></div>
</div>
```
```css
.progress { position: fixed; top: 0; left: 0; right: 0; height: 2px; z-index: 100; background: transparent; }
.progress__bar { height: 100%; background: var(--color-accent); width: 0%; transition: width 100ms linear; }
```
```js
function updateProgress() {
  const h = document.documentElement;
  const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
  document.getElementById('progress-bar').style.width = pct + '%';
}
addEventListener('scroll', updateProgress, { passive: true });
```

---

## Reveals (chave do modelo)

Cada cena revela ao entrar no viewport. Threshold ~0.2.

```html
<section class="scene" data-reveal>
  <div class="scene__text">
    <h2>Cena 1</h2>
    <p>…</p>
  </div>
</section>
```

Reveals **não acumulam decorativamente**. Ou é a cena inteira, ou nada.

---

## Sticky chart (opcional, característico do modelo)

Layout dois-col com texto rolando à esquerda e chart sticky à direita:

```html
<div class="story">
  <div class="story__text">
    <section class="scene" data-step="1">
      <h2>2024</h2>
      <p>…</p>
    </section>
    <section class="scene" data-step="2">
      <h2>2025</h2>
      <p>…</p>
    </section>
  </div>
  <div class="story__chart">
    <canvas id="chart" aria-label="Volume anual"></canvas>
  </div>
</div>
```
```css
.story { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-10); }
.story__chart { position: sticky; top: 15vh; height: 70vh; align-self: start; }
```
```js
const chart = new Chart(document.getElementById('chart'), { /* … */ });
const stepObs = new IntersectionObserver(es => {
  es.forEach(e => {
    if (!e.isIntersecting) return;
    const step = e.target.dataset.step;
    // atualizar dataset do chart conforme step
    chart.data.datasets[0].data = DATA_BY_STEP[step];
    chart.update();
  });
}, { rootMargin: '-40% 0px -40% 0px' });
document.querySelectorAll('.scene[data-step]').forEach(s => stepObs.observe(s));
```

---

## Counters

Aplicar em cenas com métricas. Ver [../componentes.md](../componentes.md#counters-animados).

---

## Tipografia scrollytelling

Editorial. H1 ~2.5rem, H2 ~1.75rem. **Lead pode ser ligeiramente maior** (~1.3rem) para tom editorial:

```css
.scrolly .lead { font-size: 1.3125rem; line-height: 1.5; }
```

Mas ainda não é gigante. Não confundir com deck.

---

## Print

```css
@media print {
  .progress { display: none; }
  .story { display: block; }
  .story__chart { position: static; height: auto; }
  .scene { break-inside: avoid; margin-bottom: var(--space-7); }
}
```

---

## Checks específicos

- [ ] Progress bar fixa no topo, refletindo scroll
- [ ] Reveals com IntersectionObserver (não setTimeout)
- [ ] Counters animam só uma vez (unobserve após visible)
- [ ] Se sticky chart presente: chart muda com data-step, não com scroll bruto
- [ ] Threshold de reveal: 0.15-0.25; rootMargin: `0px 0px -60px 0px`
- [ ] H1 ~2.5rem (não gigante)
