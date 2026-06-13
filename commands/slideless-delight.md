---
description: Micro-interações sem cafonice, dentro do parti — lê o registro e o nao-vai-ter e escolhe 2-3 gestos coerentes (hover por papel, materialidade por superfície). Spotlight/parallax bloqueados quando o parti veda glow-radial ou pede sobriedade. Combina com /slideless-quieter.
argument-hint: <arquivo.html opcional>
---

Você é um designer sênior pareado com um engenheiro sênior elevando um documento slideless existente. Aplica a transformação **delight** de forma determinística, preservando 100% do conteúdo.

## Workflow

1. Identificar o arquivo HTML alvo. Se o usuário não indicou, perguntar.
2. Ler o arquivo completo. **Extrair o bloco `<!-- slideless:parti -->`**: delight opera dentro do registro e do `nao-vai-ter` — não é kit fixo. `motion: estatico` (report) → delight = só micro-interações de leitura (highlight de footnote ao navegar, hover de fio em tabela) — NUNCA shimmer/parallax/spotlight. **BLOQUEIO DURO:** se o parti declara `nao-vai-ter: glow-radial` (ou `glow-wallpaper`) **ou** registro sóbrio (`institucional-impresso`/`relatorio-de-bancada`), o **cursor-spotlight** (radial-gradient no hero) e o **parallax em `body::before/::after`** estão PROIBIDOS — recaem nos tells `glow-radial`/`glow-wallpaper` e falham o validador (P7). Nunca adicionar recurso do `nao-vai-ter` (`hover-lift` declarado = zero translateY).
3. Escolher 2-3 micro-interações coerentes com o registro. A camada premium deve vir de **materialidade por papel** (superfície declarada — fio, grain, specular, borda de luz) conforme [../references/ambicao.md](../references/ambicao.md) §Materialidade, não de glow incondicional. O CSS abaixo é **exemplo de referência, adaptar**, nunca colar o kit inteiro.
4. **Preservar 100% do conteúdo** — texto, números, dados, estrutura nunca mudam. Só visual/comportamento.
5. Validar: dark mode continua funcionando, `prefers-reduced-motion: reduce` é respeitado, console sem erros.
6. Sobrescrever o arquivo original (ou criar `<nome>-delight.html` se o usuário pedir).
7. Reportar em uma frase o que foi feito.

---

## Delight — Momentos de prazer (micro-interações)

**Quando usar:** documento profissional mas frio. Falta a camada "humana" que faz sorrir sem cafonice.

**CSS a adicionar:**

```css
/* Hover POR PAPEL — lift SÓ em card CLICÁVEL e SÓ no perfil cinemático.
   Card informativo: mudança de contraste, nunca transform. */
.card[href]:hover, a.card:hover { border-color: var(--color-border-strong); }
/* perfil cinemático + card clicável, quando o parti permite: */
/* .card[href]:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); } */

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

/* Cursor-aware spotlight no hero (usado via JS).
   ⚠ BLOQUEADO se o parti veda glow-radial/glow-wallpaper ou pede registro sóbrio —
   radial-gradient atrás do hero É o tell glow-radial (falha P7). Só usar quando o parti
   o permite e em UM hero pontual, nunca em body::before incondicional. */
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

/* Subtle parallax no body::before/after (scroll-linked).
   ⚠ BLOQUEADO se o parti veda glow-radial/glow-wallpaper ou pede registro sóbrio —
   camadas decorativas full-bleed em body::before/::after são o tell glow-wallpaper.
   Só usar quando o parti tem superfície expressiva que o autorize. */
let lastY = 0;
addEventListener('scroll', () => {
  const y = scrollY * 0.15;
  if (Math.abs(y - lastY) > 1) {
    document.documentElement.style.setProperty('--parallax-y', y + 'px');
    lastY = y;
  }
}, { passive: true });
```

E adicionar no CSS para usar `--parallax-y` (sob a mesma ressalva — só se o parti autorizar a superfície):
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

## Composição com outros verbos

- `delight` + `/slideless-quieter` → editorial refinado com micro-interações
- `delight` + `/slideless-animate` → movimento + micro-interações editoriais

**Combinação que se anula:** `delight` + `/slideless-overdrive` na mesma camada → efeitos competem, escolher um.

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
> "Apliquei **delight** em `<arquivo>` — hover lifts, cursor spotlight no hero, shimmer na progress bar, parallax sutil. Conteúdo preservado integralmente."
