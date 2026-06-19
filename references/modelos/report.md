# Modelo `report`

Relatório editorial denso, otimizado para impressão/PDF. Para relatórios anuais, white papers, análises de pesquisa, documentos executivos longos.

**Referência mental:** Itaú Pesquisa Macro reports, McKinsey Global Institute reports, Goldman Sachs research notes, World Bank/IMF working papers.
**Exemplo:** [../../assets/exemplos/exemplo-report.html](../../assets/exemplos/exemplo-report.html).
**Template vazio:** [../../assets/templates/template-report.html](../../assets/templates/template-report.html).

---

## Anatomia

```
┌─────────────────────────────────────────────────────────────┐
│  cover                                                       │
│  - {{ORG}} · {{DOC_NUM}} · {{DATA}}                          │
│  - {{TÍTULO}} (display)                                      │
│  - subtítulo + meta de autores                               │
├─────────────────────────────────────────────────────────────┤
│  .report-executive-summary  (destacado em background tinted) │
│  - 3-5 parágrafos densos                                     │
│  - 2-3 takeaways numéricos                                   │
├──────────┬──────────────────────────────────────────────────┤
│  TOC     │  .report-body                                     │
│  sticky  │  ├── .report-section id="s1" → h2 "1. Título"     │
│  numbered│  ├── .report-section id="s2" → h2 "2. Título"     │
│  scroll- │  ├── ...                                          │
│  spy     │  └── .report-section id="sN"                      │
│          │                                                   │
├──────────┴──────────────────────────────────────────────────┤
│  .report-footnotes (numeradas, link mútuo com superscripts) │
└─────────────────────────────────────────────────────────────┘
```

Grid: TOC fixo à esquerda (~200px) + conteúdo em coluna principal (~720px max-width centralizada). Em viewports estreitos (< 1024px), TOC vira topbar collapse.

---

## Quando usar `report` vs `handbook` vs `scrollytelling`

| Critério | report | handbook | scrollytelling |
|---|---|---|---|
| Audiência | Executiva, técnica de leitura calma | Time interno consultando referência | Audiência ampla, leitura visual |
| Tom | Editorial denso, formal | Conversacional, instrucional | Narrativo, visual |
| Estrutura | Numerada (1., 2., 3...), footnotes | Hierárquica (Parte → Capítulo → Seção) | Cronológica/jornada |
| Impressão/PDF | **Sim, central** (@page A4) | Possível mas não otimizada | Não — perde reveals |
| Sumário executivo | **Sim, destacado** | Não (apenas intro) | Não |
| Footnotes/referências | **Sim, formatadas** | Apenas links inline | Apenas links inline |
| Gráficos | Inline + numerados ("Figura 3") | Inline | Sticky, scroll-triggered |
| Comprimento típico | 15-50 páginas A4 | 30-100+ páginas | 1 página longa (10-20 scroll-screens) |

Se o conteúdo cabe em <5 páginas e é narrativo → scrollytelling.
Se o conteúdo é referência de processo/documentação → handbook.
Se o conteúdo é análise/estudo/relatório formal → **report**.

---

## Estrutura semântica obrigatória

```html
<article class="report">
  <header class="report-cover">
    <p class="report-meta">{{ORG}} · {{DOC_NUM}} · {{DATA}}</p>
    <h1 class="report-title">{{TÍTULO}}</h1>
    <p class="report-subtitle">{{SUBTÍTULO}}</p>
    <p class="report-authors">Autor A · Autor B</p>
  </header>

  <section class="report-executive-summary" aria-label="Sumário executivo">
    <h2>Sumário executivo</h2>
    <p>...</p>
    <ul class="report-takeaways">
      <li><strong>R$ 1,19 tri</strong> em AuM ao final de 2024.</li>
      <li>...</li>
    </ul>
  </section>

  <nav class="report-toc" aria-label="Índice"><!-- gerada por JS --></nav>

  <main class="report-body">
    <section class="report-section" id="s1">
      <h2>1. Introdução</h2>
      <p>Texto com nota<sup><a href="#fn1">[1]</a></sup>.</p>
    </section>
    <section class="report-section" id="s2">
      <h2>2. Contexto</h2>
      <h3>2.1 Subtítulo</h3>
      <p>...</p>
    </section>
    <!-- ...mais seções... -->
  </main>

  <aside class="report-footnotes" aria-label="Notas">
    <h2>Notas</h2>
    <ol>
      <li id="fn1">Fonte original aqui. <a href="#s1">↑</a></li>
    </ol>
  </aside>
</article>
```

---

## CSS @print obrigatório

Já presente no template. Garante:
- `@page { size: A4; margin: 2cm; }`
- Cover ocupa página inteira
- `.report-section { break-inside: avoid-page; }` em seções pequenas; longa pode quebrar
- TOC oculta em print (`.report-toc { display: none; }`)
- Background tinted do executive-summary substituído por borda forte para print
- Footnotes na última página
- Headers/footers via `@page :first {}` e `@page {}` para numeração de páginas
- Links viram texto seguido de URL (`a[href]::after { content: " (" attr(href) ")"; }` opcional)

**Nunca simplificar o CSS @print** — é o que diferencia report dos outros modelos.

---

## Componentes específicos do report

### Takeaway numérico (executive summary)
```html
<ul class="report-takeaways">
  <li><strong class="report-anchor-num">R$ 1,19 tri</strong> em AuM ao final de 2024 (+8,3% YoY).</li>
  <li><strong class="report-anchor-num">14,5%</strong> de market share entre gestoras privadas.</li>
</ul>
```

### Figura numerada
```html
<figure class="report-figure">
  <div class="chart-box"><canvas id="fig-3" aria-label="Evolução do AuM 2019-2024"></canvas></div>
  <figcaption><strong>Figura 3.</strong> Evolução do AuM 2019-2024. Fonte: relatórios trimestrais.</figcaption>
</figure>
```

### Tabela com ênfase em linha
```html
<table class="data-table">
  <tr class="is-emphasis"><td><strong>Total</strong></td><td class="num"><strong>R$ 1,19 tri</strong></td></tr>
</table>
```

### Bloco de citação
```html
<blockquote class="report-quote">
  <p>"Democrática no acesso, sofisticada no modelo."</p>
  <cite>Carlos Augusto Salamonde, CIO Itaú Asset</cite>
</blockquote>
```

---

## Anti-patterns

- **Sumário executivo genérico** ("Este relatório aborda...") — torná-lo concreto com 2-3 números-âncora.
- **TOC manual** — deixar JS gerar a partir dos `id="sN"`.
- **Bullets onde cabe tabela** — 4+ linhas/3+ colunas → sempre `<table>`.
- **Gráficos resumidos** — fonte mostra 10 pontos? Chart tem 10 pontos.
- **Tipografia gigante** — relatório é editorial; h1 ≤ 2.5rem, h2 ≤ 1.75rem, body 1rem. NUNCA `clamp()` com `vw` grande aqui.
- **Quebrar em múltiplos arquivos** — single-file mesmo para 50 páginas.
- **Esquecer @print** — relatório SEM @print bem feito não é report.

---

## Char limits

| Elemento | Limite |
|---|---|
| `report-title` | ≤ 80 chars (máx 2 linhas) |
| `report-subtitle` | ≤ 140 chars |
| `<h2>` de seção numerada | ≤ 80 chars |
| `<h3>` subsecção | ≤ 100 chars |
| Takeaway na lista | ≤ 200 chars cada |
| Caption de figura | ≤ 220 chars |
| Footnote individual | ≤ 400 chars |

---

## Validação antes de entregar

- [ ] Sumário executivo com 2-3 takeaways numéricos destacados
- [ ] TOC gerada por JS (não manual)
- [ ] Cada `<section>` tem `id="sN"` no padrão
- [ ] Footnotes têm link mútuo (texto ↔ rodapé via `<sup><a>` + `<li id>`)
- [ ] `Ctrl+P` mostra preview limpo (sem nav, com quebra correta entre páginas)
- [ ] Tabelas semânticas (`<table class="data-table">`), nunca ASCII/bullets
- [ ] Gráficos Chart.js completos, escala Y começa em 0 para magnitudes, unidades nos ticks
- [ ] Dark mode toggle funciona
- [ ] `prefers-reduced-motion` respeitado
- [ ] Single-file (CSS/JS inline)
- [ ] Conteúdo da fonte 100% presente
