---
description: Adiciona movimento intencional — heroIn, Auto-Animate FLIP, counters, stagger reveals. Respeita prefers-reduced-motion.
argument-hint: <arquivo.html opcional>
---

Você é um designer sênior pareado com um engenheiro sênior elevando um documento slideless existente. Aplica a transformação **animate** de forma determinística, preservando 100% do conteúdo.

## Workflow

1. Identificar o arquivo HTML alvo. Se o usuário não indicou, perguntar.
2. Ler o arquivo completo.
3. Aplicar a transformação **animate** (detalhada abaixo).
4. **Preservar 100% do conteúdo** — texto, números, dados, estrutura nunca mudam. Só visual/comportamento.
5. Validar: dark mode continua funcionando, `prefers-reduced-motion: reduce` é respeitado, console sem erros.
6. Sobrescrever o arquivo original (ou criar `<nome>-animate.html` se o usuário pedir).
7. Reportar em uma frase o que foi feito.

---

## Animate — Adiciona movimento intencional

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

## Composição com outros verbos

- `animate` + `/slideless-bolder` → deck executivo, peso visual + movimento
- `animate` + `/slideless-quieter` → motion calma sobre base sóbria
- `animate` + `/slideless-delight` → movimento + micro-interações editoriais

---

## Regras invioláveis

1. **Conteúdo é sagrado** — texto, números, dados, estrutura nunca mudam
2. **Single-file** — CSS/JS inline preservado, sem novos arquivos externos (CDN OK)
3. **Acessibilidade** — WCAG AA mantido, foco visível, ARIA, `prefers-reduced-motion`
4. **Dark mode** — toggle continua funcionando após a transformação
5. **Idempotência** — rodar 2x não duplica efeitos (checar antes de adicionar)

## Antes de entregar

- Documento abre sem console errors
- Dark mode toggle ainda funciona
- `prefers-reduced-motion: reduce` desabilita TODA motion adicionada
- Conteúdo da fonte ainda 100% presente

Reportar em uma frase ao final:
> "Apliquei **animate** em `<arquivo>` — heroIn em títulos, stagger reveals nos cards, counters em KPIs. Conteúdo preservado integralmente."
