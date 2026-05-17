---
description: Tecnicamente extraordinário — interativo, pergunta quais efeitos aplicar (WebGL hero, Chart.js plugins, variable font, cinematic transitions, 3D tilt, scroll-driven). Liberdade de arquivo até 5 MB. Múltiplas opções compõem.
argument-hint: <arquivo.html opcional>
---

Você é um designer sênior pareado com um engenheiro sênior elevando um documento slideless existente. Aplica a transformação **overdrive** preservando 100% do conteúdo.

## Workflow

1. **Identificar o arquivo HTML alvo.** Se o usuário não indicou, perguntar.

2. **Confirmar versionamento.** Por padrão, criar `<nome>-overdrive.html` para preservar o original. Só sobrescrever se o usuário pedir explicitamente.

3. **Perguntar quais efeitos aplicar** via `AskUserQuestion` com `multiSelect: true`. Apresente as 6 opções abaixo (A–F) como `options` da pergunta. O usuário pode escolher **uma ou várias** — combinações são esperadas. Phrasing sugerido:

   > **Quais efeitos overdrive aplicar?** (pode selecionar múltiplos)

   Opções a oferecer (cada uma vira um `option` com `label` curto + `description`):
   - **A — WebGL hero generativo** · shader fragment customizado no hero (FBM, voronoi, fluid) sobre near-black. ~3KB WebGL1 nativo ou ~150KB com Three.js. 40-60fps em mid-range. Pausa quando slide não ativo.
   - **B — Chart.js plugins** · path reveal animado, glow accent (`shadowBlur`) em séries-âncora, pulse-on-active quando slide vira ativo. Aplica-se automaticamente a datasets com cor accent.
   - **C — Variable font animation** · detecta Fraunces/Instrument Serif → `font-variation-settings` animado no hero (`wght: 400→800` durante o heroIn). Sutil mas impressionante.
   - **D — Cinematic transitions** · slides marcados com `data-cinematic="zoom-blur"` ou `"depth-push"` ganham transição combinada (filter blur + transform scale) na navegação. Só deck.
   - **E — 3D tilt em cards** · `transform-style: preserve-3d` + mouse position → rotações 3-5° max. Tilt smooth, sombras dinâmicas.
   - **F — Scroll-driven (scrollytelling)** · `animation-timeline: scroll()` quando suportado (Chrome 115+), fallback IntersectionObserver para Safari/Firefox. Para modelo scrollytelling.

   **Recomendação ao usuário no momento da pergunta:** "1–2 opções costuma render restraint apropriado. 3+ pode competir entre si — selecionar com cuidado".

4. **Ler o arquivo completo** e aplicar **só** os efeitos selecionados (cada um detalhado abaixo). Restraint é parte do gosto — não inventar efeitos extras nem aplicar opções não selecionadas.

5. **Preservar 100% do conteúdo** — texto, números, dados, estrutura nunca mudam.

6. **Validar antes de entregar** (checklist embaixo).

7. **Reportar em uma frase** os efeitos efetivamente aplicados.

---

## Restrições mantidas (toda execução de /slideless-overdrive)

- **Single-file** — inline tudo, sem CDN externo além de Chart.js, fontes Google, e Three.js se opção A pedir.
- **Tamanho ≤ 5MB** — limite máximo absoluto. Three.js + shaders compactados costuma render <200KB. Variable font full pode adicionar 300-500KB. WebGL hero customizado <10KB.
- **WCAG AA** — texto sobre canvas/WebGL precisa background opaco ou vignette atrás dos elementos críticos.
- **`prefers-reduced-motion: reduce`** desabilita TUDO de motion-heavy. Canvas vira frame estático; pulses Chart.js são pulados; variable font fica em peso final; tilts ficam estáticos.
- **60fps em mid-range** — testar em throttled CPU; cap FPS a 40 via timestamp gating quando necessário.
- **Idempotência** — rodar 2x não duplica canvas nem listeners. Usar guards: `window.__overdriveX`, `chart.__overdriveBound`, etc.
- **Pausa quando invisível** — canvas e RAF param quando aba escondida (`visibilitychange`) ou slide não-ativo (`MutationObserver` em `.is-active`).
- **Overflow guard intacto** — nenhum efeito pode quebrar o `autoFitSlide()` do template. Se o efeito adiciona elementos visíveis (badges, painéis), eles caem dentro do guard `.slide > * { max-width: 100% }`.
- **Canvas WebGL OBRIGATÓRIO com `data-overdrive`** — sem isso, a regra global do template captura o canvas como conteúdo e empurra o título para fora da viewport. Já houve regressão por esquecer disso. Validar com Grep antes de entregar: cada `<canvas>` decorativo precisa ter o atributo `data-overdrive`.

## Validação de overflow PÓS-overdrive (obrigatória)

Depois de aplicar a transformação, abrir o arquivo e confirmar:
1. Hero do slide 1 (com WebGL): título + kicker + lead + meta TODOS visíveis sobre o canvas, não cortados.
2. Nenhum console.warn `[slideless] slide N overflows even after autoFitSlide`.
3. Em viewport 1366×768 e em ultrawide 2511×914 (proporção wide-short que provoca overflow): conteúdo ainda cabe.

---

## Detalhes técnicos por opção

### Opção A — WebGL hero generativo

**OBRIGATÓRIO**: o canvas WebGL deve ter `data-overdrive` na tag. Sem isso, a regra global `.slide > :not(.slide-bg):not([data-overdrive])` do template captura o canvas como conteúdo de layout, fazendo-o virar elemento `position: relative` que empurra o título do hero para fora da viewport. Sintoma: hero fica completamente preto, conteúdo desaparece. Já aconteceu — não repetir.

Estrutura correta:
```html
<section class="slide is-active" data-slide="1" data-background-color="#000000">
  <span class="slide-num"><span>01</span> · N</span>
  <canvas class="hero-webgl" id="hero-webgl" data-overdrive aria-hidden="true"></canvas>
  <div class="layout-hero">
    <!-- kicker, h1.title-xl, lead-deck, meta -->
  </div>
</section>
```

CSS:
```css
.hero-webgl { /* position: absolute, inset: 0, z-index: 0 já vêm do template via [data-overdrive] */
  opacity: 0;
  transition: opacity 1200ms var(--ease-out);
}
.slide.is-active .hero-webgl { opacity: 0.85; }
/* Vignette opcional para contraste — use ::after no slide, NÃO outro elemento, evita conflito */
.slide[data-slide="1"]::after {
  content: '';
  position: absolute; inset: 0; z-index: 1;
  background: radial-gradient(ellipse 70% 50% at 50% 50%, transparent 35%, rgba(0,0,0,0.55) 85%);
  pointer-events: none;
}
@media (prefers-reduced-motion: reduce) {
  .hero-webgl { display: none !important; }
}
```

JS WebGL1 nativo: vertex+fragment shader com FBM domain warping + 2-3 orbs derivadas de `--color-accent`. Idempotência via `window.__overdriveWebgl`. FPS cap 40, DPR cap 1.5. `prefers-reduced-motion` → 1 frame estático.

**Naming convention**: use sempre `class="hero-webgl"` (não inventar `webgl-hero`, `hero-canvas`, etc — manter consistência entre demos).

### Opção B — Chart.js plugins (accent glow + pulse-on-active)

Registrar 2 plugins via `Chart.register(accentGlowPlugin, revealOnActivePlugin)`. `isAccentColor()` detecta `#FF6200`, `#FA9F09`, `#F88104` ou rgb equivalente. Glow via `ctx.shadowBlur=14 * glowMultiplier`. Pulse: ao slide virar ativo, RAF tween de 1400ms aumentando `borderWidth` e `glowMultiplier` de 1→2.6→1 (easeOutCubic). Idempotência via `window.__overdriveChartPluginRegistered`, `chart.__overdriveBound`, `chart.__overdrivePulsing`. `prefers-reduced-motion` → não registra MutationObserver de pulse.

### Opção C — Variable font animation

Adicionar CSS:
```css
@supports (font-variation-settings: 'wght' 400) {
  .slide.is-active [data-anim="hero"] {
    animation: heroInVar 900ms var(--ease-emphatic) 100ms both;
  }
  @keyframes heroInVar {
    from { opacity: 0; filter: blur(16px); transform: translateY(28px) scale(0.96);
           font-variation-settings: 'wght' 400, 'opsz' 14; }
    to   { opacity: 1; filter: blur(0);    transform: none;
           font-variation-settings: 'wght' 800, 'opsz' 144; }
  }
}
@media (prefers-reduced-motion: reduce) {
  .slide.is-active [data-anim="hero"] { font-variation-settings: 'wght' 800, 'opsz' 144; animation: none; }
}
```
Verificar primeiro se o `--font-display` é Fraunces ou Instrument Serif (variable fonts). Se não, **pular esta opção** e avisar no relatório final.

### Opção D — Cinematic transitions

CSS:
```css
.slide[data-cinematic="zoom-blur"].is-active {
  animation: zoomBlurIn 800ms var(--ease-emphatic) both;
}
@keyframes zoomBlurIn {
  0%   { filter: blur(8px); transform: scale(0.95); opacity: 0.6; }
  60%  { filter: blur(0);   transform: scale(1.02); opacity: 1; }
  100% { filter: blur(0);   transform: scale(1);    opacity: 1; }
}
@media (prefers-reduced-motion: reduce) {
  .slide[data-cinematic] { animation: none !important; filter: none !important; transform: none !important; }
}
```
Aplicar `data-cinematic="zoom-blur"` apenas em slides chave (hero, divisor de seção, big-num). Não em todos.

### Opção E — 3D tilt em cards

CSS:
```css
.card, .ve-card, .closing-card, .num-list__item {
  --rx: 0deg; --ry: 0deg;
  transform: perspective(900px) rotateX(var(--rx)) rotateY(var(--ry));
  transition: transform 250ms var(--ease-out);
  transform-style: preserve-3d;
}
@media (prefers-reduced-motion: reduce) {
  .card, .ve-card, .closing-card, .num-list__item { transform: none !important; transition: none !important; }
}
```
JS:
```js
document.querySelectorAll('.card, .ve-card, .closing-card, .num-list__item').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const cx = (e.clientX - r.left) / r.width  - 0.5;
    const cy = (e.clientY - r.top)  / r.height - 0.5;
    card.style.setProperty('--ry', (cx *  6) + 'deg');
    card.style.setProperty('--rx', (cy * -6) + 'deg');
  });
  card.addEventListener('mouseleave', () => {
    card.style.setProperty('--rx', '0deg'); card.style.setProperty('--ry', '0deg');
  });
});
```
Idempotência: marcar `card.__overdriveTilt = true` antes de adicionar listener.

### Opção F — Scroll-driven (scrollytelling)

Verificar `CSS.supports('animation-timeline', 'scroll()')`. Se sim, aplicar `animation-timeline: scroll()` em elementos com `data-scroll-anim`. Fallback IntersectionObserver para Safari/Firefox. **Só relevante para modelos scrollytelling/handbook** — se aplicado em deck, avisar e pular.

---

## Composição com outros verbos

- `overdrive` + `/slideless-bolder` → showpiece tecnológico de alto perfil (só com conteúdo à altura)

**Combinação que se anula:** `overdrive` + `/slideless-delight` na mesma camada → efeitos competem, escolher um.

---

## Regras invioláveis

1. **Conteúdo é sagrado** — texto, números, dados, estrutura nunca mudam
2. **Single-file** — CSS/JS inline preservado, ≤ 5MB total
3. **Acessibilidade** — WCAG AA mantido, foco visível, ARIA, `prefers-reduced-motion`
4. **Dark mode** — toggle continua funcionando após a transformação
5. **Idempotência** — rodar 2x não duplica efeitos (checar `window.__overdriveX` antes de adicionar)
6. **Performance** — sem queda de framerate quando slide vira ativo
7. **Overflow guard** — `autoFitSlide()` do template continua funcionando; nenhum efeito adiciona conteúdo que estoure viewport

## Antes de entregar

- Documento abre sem console errors
- Dark mode toggle ainda funciona
- `prefers-reduced-motion: reduce` desabilita TUDO de motion-heavy
- Conteúdo da fonte ainda 100% presente
- Canvas/WebGL pausam quando slide não está ativo
- Tamanho final ≤ 5MB
- Sem warning `[slideless] slide N overflows` no console em viewport 1366×768

Reportar em uma frase mencionando os efeitos efetivamente aplicados. Exemplo:
> "Apliquei **overdrive** em `<arquivo>` com opções **A + B** — shader WebGL no hero (FBM domain-warped) + Chart.js plugin com glow accent e pulse-on-active. Conteúdo preservado integralmente, 142KB total."
