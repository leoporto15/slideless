---
description: Adiciona movimento intencional dentro do parti — lê o perfil de motion e o nível de ambição declarados e coreografa só o momento assinatura (heroIn, FLIP, reveal de figura, número-tese). Não é kit fixo; respeita prefers-reduced-motion e o nao-vai-ter.
argument-hint: <arquivo.html opcional>
---

Você é um designer sênior pareado com um engenheiro sênior elevando um documento slideless existente. Aplica a transformação **animate** de forma determinística, preservando 100% do conteúdo.

## Workflow

1. Identificar o arquivo HTML alvo. Se o usuário não indicou, perguntar.
2. Ler o arquivo completo. **Extrair o bloco `<!-- slideless:parti -->`**: o perfil de `motion` e o nível de `ambicao` declarados MANDAM (não é kit fixo — opera no que o parti pediu). `motion: estatico` → /animate é proibido de adicionar entrada (avisar o usuário e parar). `editorial` → só figuras/dados, 1 gesto. `cinematico` → até 3 gestos por papel. Se `ambicao: A2/A3`, coreografar o **momento-wow (W#)** declarado usando a receita de [../references/ambicao.md](../references/ambicao.md) (com `@supports` + estado-final-base + reduced-motion). Nunca adicionar recurso do `nao-vai-ter` (ex.: `counter-animado`, `fade-up`, `stagger-linear`).
3. Coreografar APENAS o momento assinatura do parti + a gramática por papel — o CSS abaixo é **exemplo de referência, adaptar**, nunca colar o kit inteiro.
4. **Preservar 100% do conteúdo** — texto, números, dados, estrutura nunca mudam. Só visual/comportamento.
5. Validar: dark mode continua funcionando, `prefers-reduced-motion: reduce` é respeitado, console sem erros.
6. Sobrescrever o arquivo original (ou criar `<nome>-animate.html` se o usuário pedir).
7. Reportar em uma frase o que foi feito.

---

## Animate — Adiciona movimento intencional

**Quando usar:** documento estático, sem vida cinematográfica.

> **Fonte canônica dos efeitos — COLAR, não reinventar.** O CSS deste arquivo é só *exemplo de referência*. A biblioteca verdadeira dos momentos-wow é [../references/wow-components.md](../references/wow-components.md) (W1–W31): drop-ins copy-paste já com `@supports` + estado-final-base + branch reduced-motion embutidos. **Preferir COLAR o bloco de lá** (trocar só o payload) a escrever CSS de animação solto — improviso de ponta vira tímido ou quebra na intranet. Para os gestos típicos do /animate:
> - **Reveal** → reveal por **máscara W10** (`clip-path`) no lugar de `fade-up` (que o anti-slop trata como tell); text-reveal editorial **W6** (`Intl.Segmenter`, grapheme-safe pt-BR) para lead/títulos.
> - **Diagrama/conector** → draw-on SVG **W22** (stroke-a-stroke ao entrar).
> - **Número-tese + barra + legenda** → data-choreography **W25** (uma `--spring` para o doc inteiro) — complementa/substitui o W2.
> - **Act-break entre capítulos** → chapter-divider **W28** (interstício full-bleed scrubbed).
> Manchete cinética **W3** e parallax **W14** seguem disponíveis. Cada bloco é creditado pelo validador (P8) por *signature* — copiar a fiação inteira.
> **Não é lista fechada — e olhe o documento INTEIRO.** Os W# acima são os típicos do /animate, mas **qualquer W# de movimento da biblioteca** serve (o domínio é movimento, não um cardápio). Olhar holístico: percorrer todas as dobras/seções/slides e dar a cada uma o movimento intencional que merece, **composto** (§STACKING abaixo) — não animar só o hero e deixar o resto estático, nem repetir o mesmo gesto em tudo.

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

/* Counter — APENAS se o parti declarar o número-tese como momento-wow M1/W2.
   tabular-nums obrigatório. A receita (count + barra sincronizados, @property + fallback
   em texto real) é o W2 de ../references/ambicao.md — copiar de lá, não reescrever. */
.counter { font-variant-numeric: tabular-nums; }

/* Reveal on scroll (handbook/scrollytelling) */
[data-reveal] { opacity: 0; transform: translateY(24px); transition: opacity 700ms var(--ease-out), transform 700ms var(--ease-out); }
[data-reveal].is-visible { opacity: 1; transform: none; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  [data-anim], [data-reveal] { opacity: 1 !important; transform: none !important; filter: none !important; }
}
```

**Counter (número-tese) — NÃO colar JS de count-up aqui.** `counter-animado` é item do `nao-vai-ter`: só é legítimo quando o parti declara o número-tese como momento-wow **M1/W2**. Nesse caso, **copiar a receita W2 de [../references/ambicao.md](../references/ambicao.md)** — counter + barra crescem sincronizados via `@property` + `animation-timeline: view()`, com **fallback em texto real no HTML** (o valor final visível mesmo sem a feature) e branch reduced-motion. É CSS-first (sem `requestAnimationFrame` tween manual, sem varrer `\b\d{2,}\b`). Se o parti não declarar M1/W2, o número entra **estático** e este passo é pulado.

**JS a adicionar (antes do `</body>`) — só o reveal de figura:**

```js
/* Reveal on scroll — APENAS em figuras/dados marcados, nunca em texto corrido */
const rio = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('is-visible'); rio.unobserve(e.target); }
}), { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
document.querySelectorAll('[data-reveal]').forEach(el => rio.observe(el));
```

**Atributos — POR DECISÃO, nunca auto-injeção em massa:**
- Counter: APENAS no número-tese declarado como momento-wow **M1/W2** no parti — e via a receita W2 de [../references/ambicao.md](../references/ambicao.md) (CSS-first, `@property` + fallback em texto real). Números de apoio entram estáticos. **PROIBIDO** varrer `\b\d{2,}\b` e converter tudo em counter, e **proibido** colar count-up em `requestAnimationFrame` (recai em `counter-animado` do `nao-vai-ter`).
- Reveal: APENAS em figuras/dados (perfil editorial), ≤40% das sections. **PROIBIDO** adicionar `data-reveal` em listas/cards por ordem do DOM — tabela, texto corrido, TOC e nav nunca animam.
- Stagger: só dentro de grupo homogêneo (itens da MESMA lista revelada, barras do mesmo gráfico), máx 1 grupo por viewport.
- Auto-Animate (deck cinemático): slides consecutivos com o mesmo número/termo evoluindo → `data-auto-animate` + `data-id` nos elementos correspondentes.

**Não tocar:** conteúdo, layouts, gráficos.

### §STACKING — respeitar a disciplina de densidade

Coreografar dentro da densidade da §STACKING de [../references/wow-components.md](../references/wow-components.md): **A2 = 3–5 momentos; A3 = 6–8**. No máximo **1 herói pinned** (W18/W28/W13-horizontal — nunca dois disputando o mesmo gesto de scroll) + **2 sistemas ambientes** na mesma física (ex.: W21 hue-drift + UM reveal de figura, W29 ou W25 com uma só `--spring`) + **~70% calmo** (zonas de silêncio de 1–2 viewports depois de cada momento; nunca 2 momentos de atenção no mesmo viewport). /animate adiciona movimento, não enche a tela.

### Armadilhas de render (não reintroduzir)

Ver §Armadilhas de [../references/wow-components.md](../references/wow-components.md) — o que o `smoke.py` reprova:
- **Odômetro/reel:** `.od-digit` PRECISA de `height: 1em` (+ `overflow:clip`); sem altura a tira 0-9 vaza.
- **Número duplicado ("7070%"):** nunca o número como nó de texto direto **E** `::after { content: counter() }` juntos — esconder o texto-base (`display:none`) dentro do `@supports`+motion.
- **Lista numerada:** counter **absoluto** (`position:relative` no `li` + `::before` absoluto), nunca `display:grid` (quebra o texto por-caractere).
- **`<canvas>`:** nunca `width:auto` (estoura em HiDPI) — tamanho explícito + `maintainAspectRatio:false`.
- **`a[href="#"]`:** sempre com `preventDefault` (não saltar ao topo).

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

## Gate de render antes de entregar (v7 — obrigatório)
Todo verbo modifica render — rodar os DOIS e corrigir a CAUSA antes de entregar:
- `python scripts/validar.py <arquivo.html>` → `0 erro(s)`.
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide curto, invasão de coluna, scroll horizontal).
Nunca entregar com `SMOKE FAIL`.

Reportar em uma frase ao final:
> "Apliquei **animate** em `<arquivo>` — heroIn em títulos, stagger reveals nos cards, counters em KPIs. Conteúdo preservado integralmente."
