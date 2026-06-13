# Design system — slideless

Tokens, dark mode, boot script. **Ler antes de gerar qualquer HTML.**

---

## Filosofia

Este arquivo define a **engenharia** do sistema: tokens, contratos, dark mode, boot script, a11y. A **estética** de cada documento NÃO mora aqui — ela é decidida por documento no bloco `<!-- slideless:parti -->` ([direcao-de-arte.md](direcao-de-arte.md)), com tipografia de [type-kits.md](type-kits.md). Dois testes que todo documento precisa passar: *"isso pareceria um slide de PPT?"* (se sim, recuar) e *"isso é distinguível do exemplo canônico cobrindo o logo?"* (se não, falhou a direção de arte).

**Fonte de verdade dos tokens: [assets/temas/itau.css](../assets/temas/itau.css) e [assets/temas/neutro.css](../assets/temas/neutro.css)** (v4, duas camadas: `[MARCA]`/`[BASE]` inviolável + `[DIREÇÃO]` composta conforme o parti). Os blocos abaixo são resumo de referência — em divergência, o tema vence.

---

## Tokens — sempre via CSS custom properties

Toda cor, tamanho, espaço e duração mora em `:root` e ganha override em `[data-theme="dark"]`. Nunca hardcodar `#ffffff` no meio do CSS — sempre `var(--color-bg)`.

### Cores (tema `itau`)

```css
:root {
  /* Marca Itaú — fixas em ambos os temas */
  --itau-orange:    #FF6200;
  --itau-orange-2:  #F88104;
  --itau-orange-3:  #FA9F09;
  --itau-blue-3:    #3B85FA;
  --itau-yellow:    #FBC305;

  /* Light (v4 — sincronizado com itau.css) */
  --color-bg:           #faf7f5;   /* cream warm — não branco puro */
  --color-bg-elevated:  #ffffff;
  --color-bg-sunken:    #f4f1ec;
  --color-fg:           #292017;   /* warm dark — não preto puro */
  --color-fg-muted:     #6b5d50;
  --color-fg-subtle:    #8a7e72;
  --color-border:       rgba(41, 32, 23, 0.10);
  --color-border-strong:rgba(41, 32, 23, 0.18);
  --color-accent:       var(--itau-orange);
  --color-accent-hover: var(--itau-orange-2);
  --color-accent-fg:    #ffffff;
}

[data-theme="dark"] {
  --color-bg:           #14110d;   /* preto quente (não puro) */
  --color-bg-elevated:  #1c1814;
  --color-bg-sunken:    #221d18;
  --color-fg:           #ede5dd;
  --color-fg-muted:     #b8aa9a;
  --color-fg-subtle:    #786e62;
  --color-border:       rgba(237, 229, 221, 0.10);
  --color-border-strong:rgba(237, 229, 221, 0.20);
  --color-accent:       var(--itau-orange-3);   /* +20% luminosity no escuro */
  --color-accent-hover: var(--itau-orange-2);
  --color-accent-fg:    #14110d;
}
```

### Paleta semântica (tema itau)

Cada cor tem `--color-*` (contorno/texto) + `--color-*-dim` (fundo tingido): `accent` (brand), `info` (dado/macro), `success` (resultado positivo — `sage` é alias fundido), `teal` (técnico/analítico), `plum` (crítico/atenção), `warn`, `danger`. Em browsers modernos a paleta é redefinida em **OKLCH** (bloco `@supports` no fim do itau.css) — perceptualmente uniforme, derivada do matiz do laranja.

**Cor é informação, não decoração:** o regime cromático (bicromático / duotone / polícromo mapeado) é decisão do parti; distribuir as cores em sequência decorativa é o anti-pattern C10/C14.

Callouts usam o mesmo sistema: `.callout--info { background: var(--color-info-dim); border-color: var(--color-info); }` (tema neutro usa o par `--color-*-bg`/`--color-*-border`).

### Tipografia

A voz tipográfica vem do **kit do documento** ([type-kits.md](type-kits.md)) via slots `--kit-*`, definidos ANTES do bloco do tema:

```css
:root {
  /* o kit define: --kit-display, --kit-text, --kit-ui, --kit-mono */
  /* itau.css consome: */
  --font-text:    'Itau Text', var(--kit-text, 'Inter'), -apple-system, system-ui, sans-serif;
  --font-display: 'Itau Display', var(--kit-display, Georgia), serif;
  --font-mono:    var(--kit-mono, 'IBM Plex Mono'), 'SF Mono', Consolas, monospace;

  /* Escala fluida (v2+) — clamp em todos os modelos; valores em itau.css */
  --size-body: clamp(1rem, 0.95rem + 0.2vw, 1.125rem);
  --size-h2:   clamp(1.6rem, 1.3rem + 1.2vw, 2.25rem);
  --size-h1:   clamp(2.25rem, 1.8rem + 2vw, 3.5rem);
  /* + --size-xs/small/lead/h4/h3 e, deck-only, --size-display/mega/giga */
}
```

**Inter como `--font-display` é PROIBIDO** em qualquer tema (tell nº 1 de tipografia de IA). Lista completa de fontes banidas em [type-kits.md](type-kits.md).

**No modelo `deck`** usar `clamp()` para tipografia fluida (porque é viewport-cheio):
```css
.title-xl { font-size: clamp(2.75rem, 6.5vw, 6rem); }
.big-num__val { font-size: clamp(5rem, 16vw, 14rem); }
```
**Em qualquer outro modelo, tipografia > 3rem é proibida.** Ver [anti-patterns.md](anti-patterns.md).

### Espaço, raios, sombras, easing

```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem;    --space-5: 1.5rem; --space-6: 2rem;
  --space-7: 2.5rem;  --space-8: 3rem;   --space-10: 4rem;
  --space-12: 5rem;

  --content-max: 720px;     /* coluna de texto handbook */
  --sidebar-w:   268px;
  --toc-w:       220px;
  --header-h:    56px;

  /* [DIREÇÃO] Radius (itau: 4/10/16/24 · neutro: 4/8/12) — máx 2 valores
     DISTINTOS por documento; radius idêntico em card+tabela+code+callout
     é fingerprint. Sombras: 5 níveis no itau (xs→xl) + insets; o REGIME
     DE LUZ (flat/key-light/hard-print/glow-spot) é decisão do parti —
     registro impresso usa fio, não sombra. */
  --radius-sm: 4px;
  --radius:    10px;
  --radius-lg: 16px;

  /* [DIREÇÃO] Easing — vocabulário com PAPEL, nunca curva única (C7) */
  --ease-out:  cubic-bezier(0.22, 1, 0.36, 1);  /* papel: entrada    */
  --ease-snap: cubic-bezier(0.2, 0, 0, 1);      /* papel: micro      */
  --duration-fast: 150ms;
  --duration:      250ms;
}
```

Valores completos (sombras light/dark, insets, durações de deck): [assets/temas/itau.css](../assets/temas/itau.css). **`transition: all` é proibido** — transições sempre property-scoped.

---

## Boot script — OBRIGATÓRIO no `<head>`, antes do CSS

Roda síncrono antes do CSS pintar para evitar flash de tema errado.

```html
<script>
  (function() {
    try {
      var t = localStorage.getItem('theme') ||
              (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', t);
    } catch (e) {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  })();
</script>
```

O validador `scripts/validar.py` falha se este snippet (ou equivalente) não estiver presente no `<head>` antes da primeira tag `<link rel="stylesheet">` ou `<style>`.

---

## Theme toggle — botão no header

```html
<button class="theme-toggle" aria-label="Alternar tema" type="button">
  <span aria-hidden="true">◐</span>
</button>
```
```js
document.querySelector('.theme-toggle')?.addEventListener('click', () => {
  const h = document.documentElement;
  const next = h.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  // .no-transitions: impede a página inteira de "respirar" no switch (régua de craft, ambicao.md)
  h.classList.add('no-transitions');
  h.setAttribute('data-theme', next);
  try { localStorage.setItem('theme', next); } catch {}
  requestAnimationFrame(() => requestAnimationFrame(() => h.classList.remove('no-transitions')));
});
```
```css
/* par do snippet acima — incluir no tema */
.no-transitions, .no-transitions *, .no-transitions *::before, .no-transitions *::after { transition: none !important; }
```

---

## Fontes — kits, não pairings

> v4: a tabela de pairings que vivia aqui está REVOGADA — incluía Instrument Serif (fonte-assinatura de IA de 2ª geração, banida) e consagrava Fraunces como "padrão", o que fez 100% dos documentos saírem Fraunces (slop de 2ª geração da casa). A escolha tipográfica agora é a **decisão nº 2 do parti**: 1 kit completo de **[type-kits.md](type-kits.md)** — 6 kits com `<link>` de eixos limitados, tokens `--kit-*`, tabela de tracking por corpo, features OpenType e fallback de sistema desenhado. Fraunces sobrevive só no Kit 06, com quota 1/3 e eixos SOFT/WONK obrigatórios.

Itau Display e Itau Text são proprietárias (CDN interno) e têm precedência dentro da rede — o kit é o fallback desenhado fora dela. **Nunca Inter como display; nunca "fallback automático para Inter".**

---

## Microtipografia — obrigatória em todo documento

A assinatura invisível de estúdio (nenhum gerador de IA aplica por default; tudo degrada graciosamente):

| Item | Regra |
|---|---|
| Números de dados | `font-variant-numeric: tabular-nums lining-nums` em toda célula de tabela, KPI, metric e tick de gráfico |
| Aspas | Curvas pt-BR (`“ ” ‘ ’`); apóstrofo `’`; retas só em código |
| Valor + unidade | NBSP entre eles: `R$ 1,2 bi` · `82 ms` · `14 p.p.` |
| Headings | `text-wrap: balance` |
| Parágrafos | `text-wrap: pretty` |
| Formatação numérica | pt-BR consistente em texto, tabela E Chart.js (`toLocaleString('pt-BR')` — css-patterns.md §5.0) |
| Tracking | Por corpo, ≥3 valores com sinais distintos — nunca um letter-spacing global |
| Total de tabela financeira | Fio duplo: `border-top: 3px double var(--color-fg)` |
| Variable font | Se a display tiver eixo além de wght (opsz/SOFT/WONK), usar ≥1 ou justificar a renúncia no parti |

---

## Tema `neutro` — papel e tinta (v4)

Refeito na v4 (o v2 era o AI-slop canônico: Inter solo + blue-600 + slate). Agora:
- Accent **azul-tinta próprio** `#1c4d8d` (OKLCH em browsers modernos) — não é o azul do Tailwind
- Neutros papel/tinta desenhados (`#fbfbf9` / `#1d2126`), não slate
- **Nenhuma fonte própria**: a voz tipográfica vem 100% do kit (`--kit-*`); sem kit, degrada para Georgia/Segoe — nunca para Inter
- Sem `--itau-*` tokens

Ver [temas/neutro.md](temas/neutro.md) e `assets/temas/neutro.css`.

---

## Regras inegociáveis

1. Boot script no `<head>` antes do CSS.
2. Toda cor via `var(--color-*)`. Nunca hex hardcoded no corpo do CSS (exceto dentro de `:root` ou `[data-theme]`).
3. `[data-theme="dark"]` override completo de todos os tokens semânticos.
4. Tipografia editorial nos modelos não-deck. Tipografia gigante via `clamp()` só no deck.
5. `prefers-reduced-motion: reduce` desabilita transições e animações.
6. Foco visível: `:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }`.
7. Nenhum HTML antes do bloco `<!-- slideless:parti -->` ([direcao-de-arte.md](direcao-de-arte.md)).
8. Inter como display, `transition: all` e as fontes banidas de type-kits.md: proibidos.
9. Microtipografia da tabela acima em todo documento.
