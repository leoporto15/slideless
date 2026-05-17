---
name: slideless
description: Substitui PowerPoint por documentos web interativos HTML single-file para comunicação interna do Itaú. Seis modelos cobrem do material denso e navegável até apresentação linear estilo pitch moderno — handbook (sidebar + scrollspy + TOC estilo GitLab Handbook), hub (portal de cards categorizáveis), scrollytelling (narrativa única com reveal-on-scroll), site (SPA single-file com hash routing), deck (slide-by-slide com animações stagger, fragments, keyboard nav, fullscreen) e report (relatório editorial denso com sumário executivo, TOC numerada, footnotes e CSS @print otimizado para PDF estilo Itaú Pesquisa Macro). Tudo entregue como UM arquivo HTML portátil com CSS e JS inline. Use quando o usuário pedir handbook, manual, central de conhecimento, onboarding, política interna, hub de recursos, central de serviços, relatório anual interativo, narrativa de projeto, microsite, página interna de produto, pitch, all-hands, deck moderno, ou qualquer comunicação interna que se beneficie de navegação não-linear, dark mode nativo, densidade variável e interatividade real. Inclui tema neutro (azul) e tema corporativo Itaú (laranja oficial #FF6200 + fontes Itaú Display/Text), ambos com dark mode. Anti-pattern central: NÃO gera "PPT estilizado em HTML" — distingue documento web de slide (tipografia gigante é proibida fora do modelo `deck`).
---

# slideless

Skill para gerar **documentos web interativos** em HTML single-file. Não confunda com "PPT em HTML": a v1 desta skill foi rejeitada exatamente por sair "slide estilizado". A v2 muda de paradigma — vibe Notion/GitLab handbook, não pitch deck (com a exceção explícita do modelo `deck`).

Leia [references/anti-patterns.md](references/anti-patterns.md) antes da primeira geração da sessão.

---

## Princípio: tudo single-file

Todo modelo entrega **um único HTML** com CSS e JS inline. Portátil, hospedável em qualquer S3 estático, distribuível como anexo. Sem dependências de arquivos externos exceto fontes (Google Fonts) e gráficos (Chart.js via CDN).

---

## Seis modelos

O usuário escolhe o modelo no briefing. Quando ambíguo, use [references/decisao-modelo.md](references/decisao-modelo.md).

### `handbook` — manual com sidebar fixa
**Use quando:** documentação longa, manual de processo, central de conhecimento, onboarding, política interna, livro de práticas, runbook.
**Estrutura:** sidebar de navegação à esquerda (com scrollspy) + conteúdo central + TOC sticky à direita.
**Referência mental:** GitLab Handbook, Stripe Docs, Notion Pages.
**Doc:** [references/modelos/handbook.md](references/modelos/handbook.md) — **Exemplo:** [assets/exemplos/exemplo-handbook.html](assets/exemplos/exemplo-handbook.html) — **Template vazio:** [assets/templates/template-handbook.html](assets/templates/template-handbook.html).

### `hub` — portal com cards navegáveis
**Use quando:** central de recursos, catálogo de serviços, hub de time, landing interna agregando múltiplas dimensões independentes.
**Estrutura:** grid de cards categorizados com filtros; click abre painel correspondente in-page (sem reload).
**Referência mental:** Notion Workspace, Apple Developer hub, Vercel guides index.
**Doc:** [references/modelos/hub.md](references/modelos/hub.md) — **Exemplo:** [assets/exemplos/exemplo-hub.html](assets/exemplos/exemplo-hub.html) — **Template vazio:** [assets/templates/template-hub.html](assets/templates/template-hub.html).

### `scrollytelling` — narrativa única scroll-triggered
**Use quando:** relatório anual interativo, caso de estudo aprofundado, narrativa de projeto, divulgação editorial.
**Estrutura:** página única longa; seções revelam ao scroll; gráficos sticky que mudam ao avançar; progress bar no topo.
**Referência mental:** NYT The Upshot, The Pudding, Apple product pages.
**Doc:** [references/modelos/scrollytelling.md](references/modelos/scrollytelling.md) — **Exemplo:** [assets/exemplos/exemplo-scrollytelling.html](assets/exemplos/exemplo-scrollytelling.html) — **Template vazio:** [assets/templates/template-scrollytelling.html](assets/templates/template-scrollytelling.html).

### `site` — mini-site SPA single-file
**Use quando:** microsite com 2-5 dimensões (home, sobre, recursos), lançamento interno, portfólio de squad.
**Estrutura:** UM arquivo HTML; header de nav troca entre `<article class="view">` via hash routing (`#home`, `#sobre`). Sem reload, sem build.
**Referência mental:** Linear, Vercel guides, Notion product pages.
**Doc:** [references/modelos/site.md](references/modelos/site.md) — **Exemplo:** [assets/exemplos/exemplo-site.html](assets/exemplos/exemplo-site.html) — **Template vazio:** [assets/templates/template-site.html](assets/templates/template-site.html).

### `deck` — apresentação moderna sequencial
**Use quando:** pitch executivo linear, all-hands, talk de conferência interna, demo guiada — narrativa linear curta apresentada **ao vivo**.
**Estrutura:** sequência de slides (cada um ocupa o viewport); navegação setas/teclado/swipe; transições, fragments, fullscreen, counters, theme toggle.
**Referência mental:** Apple keynotes, Linear launches, Pitch.com modernas.
**Doc:** [references/modelos/deck.md](references/modelos/deck.md) — **Exemplo:** [assets/exemplos/exemplo-deck.html](assets/exemplos/exemplo-deck.html) — **Template vazio:** [assets/templates/template-deck.html](assets/templates/template-deck.html).

**Importante:** `deck` é o **único** modelo onde tipografia gigante (4-6rem+) é apropriada — porque é viewport-cheio e apresentação ao vivo. Em todos os outros modelos a tipografia é editorial (h1 ~2.5rem). Ver [references/anti-patterns.md](references/anti-patterns.md).

### `report` — relatório editorial denso (PDF-friendly)
**Use quando:** relatório anual interativo, white paper, análise de pesquisa, documento executivo longo que será **lido com calma e exportado para PDF**.
**Estrutura:** capa + sumário executivo destacado + TOC sticky numerada + seções numeradas (1., 2., 3.) + footnotes formatadas com link mútuo. CSS `@page A4` rigoroso para impressão limpa.
**Referência mental:** Itaú Pesquisa Macro reports, McKinsey Global Institute, Goldman Sachs research, World Bank working papers.
**Doc:** [references/modelos/report.md](references/modelos/report.md) — **Template vazio:** [assets/templates/template-report.html](assets/templates/template-report.html).

**Quando usar report vs scrollytelling vs handbook:** report é o único com sumário executivo formal + footnotes numeradas + CSS @print otimizado. Conteúdo narrativo curto → scrollytelling. Documentação de processo → handbook. Análise/estudo formal de leitura calma → **report**.

---

## Princípios transversais

1. **Single-file por padrão.** CSS e JS inline. Fontes via Google Fonts, gráficos via CDN. Tamanho-alvo até 1MB para modelos editoriais (handbook/hub/site/scrollytelling/report); deck/`overdrive` pode chegar a **5MB** quando o conteúdo justifica (WebGL, Three.js, fonte variable embutida).
2. **Nada vaza da viewport.** Todo conteúdo de um slide/seção precisa caber visualmente — sem clipping, sem scroll horizontal, sem texto cortado pela HUD. **Inviolável**. O template-deck aplica overflow guard (`.slide { contain }` + `.slide > * { max-width: 100% }`) e `autoFitSlide()` JS que reduz iterativamente o título se o conteúdo exceder o viewport. Mas isso é a rede de segurança — o gerador deve respeitar os char limits abaixo:
   | Classe | Limite recomendado | Quando exceder |
   |---|---|---|
   | `.title-mega` / `.fact-val` / `.statement-text` | **≤ 50 chars** (1-2 linhas em viewport baixo) | Divida em 2 elementos (`<em>` + texto) ou troque para `.title-lg` |
   | `.title-xl` | ≤ 70 chars | Troque para `.title-lg` |
   | `.title-lg` | ≤ 90 chars | Troque para `.title-md` |
   | `.lead-deck` | ≤ 220 chars | Quebre em duas frases ou use `.title-md` + lead curto |
   Sempre testar em viewport 1366×768 (notebook baixo) — se aparecer warning `[slideless] slide N overflows even after autoFitSlide` no console, o slide está denso demais.
3. **Dark mode nativo.** Toggle no header, persistência via `localStorage`, boot script antes do CSS pintar (sem flash). Detalhes em [references/design-system.md](references/design-system.md).
4. **Animações funcionais.** Reveal-on-scroll, números que contam, fade-in. Nunca parallax dramático, glow decorativo, ou animação só por animação.
5. **Interatividade real.** Toggles funcionam, tabs trocam, callouts informam, código copia, gráficos respondem.
6. **Acessibilidade.** WCAG AA, `aria-*` correto, keyboard navigation, `prefers-reduced-motion` respeitado, foco visível.
7. **Conteúdo real obrigatório.** Sem conteúdo real fornecido pelo usuário, **não gerar lorem-ipsum nem inventar dados internos do Itaú.** Protocolo em [references/protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md).

---

## Comandos

Os comandos vivem em [commands/](commands/) — cada arquivo `.md` é um slash command que pode ser invocado independentemente. Argumentos opcionais entre `<…>`.

### Criação (6 modelos + wizard)
| Comando | Função |
|---|---|
| `/criar` | **Wizard para áreas de negócios** — faz 5 perguntas em português comum e escolhe o modelo automaticamente, sem precisar conhecer a diferença entre deck/handbook/hub/etc. |
| `/slideless-handbook <tópico>` | Cria handbook com sidebar + scrollspy + TOC |
| `/slideless-hub <tópico>` | Cria hub com grid de cards categorizáveis |
| `/slideless-scrollytelling <tópico>` | Cria scrollytelling com reveal e sticky chart |
| `/slideless-site <tópico>` | Cria SPA single-file com hash routing |
| `/slideless-deck <tópico>` | Cria deck moderno com keyboard nav |
| `/slideless-report <tópico>` | Cria relatório editorial denso (sumário executivo + TOC numerada + footnotes + CSS @print otimizado para PDF) |
| `/slideless-report <tópico>` | Cria relatório editorial denso, otimizado para impressão/PDF |
| `/estruturar <conteúdo>` | Analisa conteúdo bruto e propõe mapa estruturado para aprovação antes de gerar |

### Importação (3)
| Comando | Função |
|---|---|
| `/importar-confluence <url \| anexo>` | Converte página/espaço Confluence em modelo apropriado |
| `/importar-ppt <arquivo>` | Converte PPT/PPTX em handbook OU deck (pergunta) |
| `/importar-md <arquivo>` | Converte Markdown estruturado em handbook |

### Edição cirúrgica (6)
| Comando | Função |
|---|---|
| `/adicionar-secao <título>` | Adiciona seção ao handbook/scrollytelling/site |
| `/adicionar-slide <tipo>` | Adiciona slide ao deck (hero, big-num, metrics, quote, list, two-col, divider, timeline) |
| `/adicionar-callout <tipo>` | Insere callout (info/tip/warn/danger) |
| `/adicionar-grafico <tipo>` | Insere gráfico Chart.js (line/bar/donut/gauge/radar/bubble/waterfall/mixed) |
| `/adicionar-fragment` | Marca elementos do slide ativo como fragments (revelam por click) |
| `/adicionar-toc` | Regenera TOC sticky a partir dos `<h2>/<h3>` do conteúdo |

### Transformação (3)
| Comando | Função |
|---|---|
| `/aplicar-tema <neutro\|itau>` | Troca o tema do documento existente |
| `/converter-modelo <novo>` | Converte entre modelos compatíveis (handbook ↔ scrollytelling, hub ↔ site) |
| `/distill` | Reduz handbook longo a sumário enxuto preservando hierarquia |

### Refinamento de design (5 comandos independentes)
| Comando | Função |
|---|---|
| `/slideless-bolder` | Amplifica designs tímidos — tipografia hero +30%, glow reforçado, números-âncora circulados via Rough Notation |
| `/slideless-quieter` | Reduz designs ruidosos — tipografia -15%, cores muted, motion calma, fallback serif editorial |
| `/slideless-animate` | Adiciona movimento intencional — heroIn, Auto-Animate FLIP, counters, stagger reveals (respeita prefers-reduced-motion) |
| `/slideless-delight` | Micro-interações sem cafonice — hover lifts, cursor-aware spotlight no hero, shimmer na progress bar, parallax sutil |
| `/slideless-overdrive` | Tecnicamente extraordinário — WebGL/Canvas no hero, custom Chart.js plugins, variable font animation, cinematic transitions. Comando interativo: pergunta quais efeitos aplicar (multi-seleção). Liberdade de arquivo até 5 MB |

Os 5 verbos compõem em sequência (`/slideless-bolder` + `/slideless-animate`, `/slideless-quieter` + `/slideless-delight`). Sempre preservam 100% do conteúdo.

### Qualidade (4)
| Comando | Função |
|---|---|
| `/auditar` | Roda validador determinístico + checklist de revisão LLM |
| `/polir` | Refina tipografia, espaçamento, hierarquia visual |
| `/harden` | Endurece a11y (WCAG AA), keyboard nav, `prefers-reduced-motion` |
| `/acessibilidade` | Foco isolado em a11y — varredura + correções |

### Export (2)
| Comando | Função |
|---|---|
| `/exportar-pdf` | Renderiza para PDF (deck → landscape; demais → retrato) via Playwright |
| `/exportar-screenshots` | 1 PNG por slide/seção para preview rápido |

---

## Comando `/estruturar` — pré-geração

Recebe conteúdo bruto (bullets, PDF colado, descrição livre) e devolve um **mapa estruturado** para aprovação antes de gerar qualquer HTML. Evita retrabalho quando o conteúdo é denso ou a escolha de modelo é não-óbvia.

### Input aceito
- Bullets colados diretamente no chat
- Transcrição de PDF (texto bruto com quebras de página)
- Descrição livre: "quero apresentar os resultados do Q1 para a diretoria"
- Arquivo `.md` ou `.txt` anexado

### Output (proposta para aprovação)
```
## Proposta de estrutura — slideless

**Modelo recomendado:** deck
**Justificativa:** conteúdo com hierarquia clara, 7 tópicos discretos, audiência executiva presencial

**Inventário de conteúdo (N elementos)**
- 4 KPIs → métricas 3-up (slides 2-3)
- 2 comparações YoY → gráfico de barras agrupadas
- 1 evolução temporal → linha com área preenchida
- 8 fundos → tabela HTML (8 linhas × 4 colunas) — NÃO bullets
- 3 pilares estratégicos → cards color-coded
- 1 hierarquia de gestão (12 pessoas) → org-chart HTML/CSS

**Mapa de slides/seções proposto**
| # | Tipo | Conteúdo | Visual |
|---|---|---|---|
| 01 | Hero | Título + meta | Atmospheric hero |
| 02 | Metrics | 4 KPIs | Cards 2×2 |
| 03 | Split | Evolução AuM | Gráfico linha |
| 04 | Table | 8 fundos | HTML table |
| ... | | | |

**Elementos que EXIGEM dado real (preencher antes de gerar)**
- AuM exato por categoria
- Nomes dos gestores responsáveis
- Data de referência dos dados

**Confirmar para gerar?** Responda "sim" ou ajuste o mapa acima.
```

### Regra
Nunca pular `/estruturar` quando: (a) conteúdo tem mais de 30 elementos discretos, (b) origem é PDF/PPT colado, (c) usuário não especificou modelo.

---

## Briefing mínimo antes de gerar

Toda criação exige:

1. **Modelo** — se ambíguo, consulte [references/decisao-modelo.md](references/decisao-modelo.md) e pergunte.
2. **Conteúdo real** — texto, MD, PPT, dados. Sem conteúdo, aplique [references/protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md).
3. **Tema** (`neutro` ou `itau`).
4. **Escopo** — quantas seções/cards/slides/views aproximadamente.

---

## Workflow padrão — Think → Structure → Style → Deliver

### 1. Think (5s de comprometimento com direção)

Antes de escrever HTML, responder:
- **Quem lê?** (executivo, time técnico, toda empresa?)
- **Que tipo de conteúdo?** (dados históricos, narrativa qualitativa, catálogo, referência?)
- **Qual estética?** Escolher uma das constrained (mais seguro) ou flexível:

**Constrained (preferidas — impossível parecer genérico):**
- **Warm Signal** — cream + laranja Itaú + glow atmosférico. Padrão para tema itaú.
- **Blueprint** — grid técnico, slate/azul profundo, labels monospace. Ideal para docs de engenharia.
- **Editorial** — serif headlines, whitespace generoso, earth tones. Ideal para relatórios narrativos.
- **Terminal Mono** — verde/amber on near-black, monospace tudo. Para conteúdo de infraestrutura/dados.

**Flexíveis (com cuidado):**
- **IDE-inspired** — temas nomeados reais (Dracula, Nord, Catppuccin, One Dark). Só se o contexto pedir.
- **Data-dense** — small type, tight spacing, cores mutted. Para tabelas complexas.

**Explicitamente proibido:**
- Neon dashboard (cyan + magenta + purple on dark)
- Inter + violet/indigo accents + gradient text
- Emoji como ícones de seção

### 2. Structure (ler antes de escrever)

Para cada tipo de conteúdo, usar o template correto:

| Conteúdo | Usar | Referência |
|---|---|---|
| Texto narrativo longo | template-handbook | references/modelos/handbook.md |
| Cards / catálogo | template-hub | references/modelos/hub.md |
| Narrativa scroll-triggered | template-scrollytelling | references/modelos/scrollytelling.md |
| Multi-view com abas | template-site | references/modelos/site.md |
| Apresentação linear ao vivo | template-deck | references/modelos/deck.md + slide-patterns.md |
| Relatório editorial denso (PDF-friendly) | template-report | references/modelos/report.md |
| CSS patterns novos | — | references/css-patterns.md |
| Slide layouts | — | references/slide-patterns.md |

**Planejamento de conteúdo (obrigatório para deck):**
1. Inventariar todos os elementos discretos da fonte (slides, bullets, métricas, nomes, datas, tabelas).
2. Mapear cada elemento a uma seção/slide/card. Nada pode ficar sem destino.
3. Só então escrever HTML.

### 3. Style (aplicar princípios)

- **Tipografia é estrutura** — hierarquia via escala + peso + cor, não cores flashy.
- **Depth tiers** — variar profundidade visual: hero (elevated), default (flat), recessed (inset). Ver `references/css-patterns.md § 2`.
- **Backgrounds criam atmosfera** — nunca fundo sólido flat. Usar glow radial, dot grid ou gradient mesh.
- **Animações ganham seu lugar** — stagger fadeUp para cards, heroIn para títulos principais, counters para números. Nunca glowing shadows ou pulsing em elementos estáticos.
- **Font pairing distinto** — nunca Inter sozinho. Ver `references/css-patterns.md § 10` para opções.

### 4. Deliver

- Salvar output no diretório indicado pelo usuário.
- Abrir em browser (testar ambos os temas, redimensionar janela).
- Declarar ao usuário: path do arquivo + o que foi gerado.

---

## Regras mandatórias de gráficos e tabelas

**Gráficos (Chart.js):**
- Dados numéricos com evolução temporal → gráfico de linha obrigatório.
- Comparação de N categorias → gráfico de barras ou donut.
- KPI com tendência → sparkline inline.
- CDN: `https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js`
- Patterns completos em `references/css-patterns.md § 5`.

**Regras inegociáveis de fidelidade (gráficos):**
1. **Dados completos** — todos os pontos/categorias da fonte entram no gráfico. Nunca resumir, truncar ou omitir valores "para simplificar".
2. **Composição preservada** — se a fonte mostra múltiplas séries num mesmo gráfico (ex: barras de volume + linha de tendência sobreposta), isso deve ser reproduzido como um único gráfico misto (`type: 'bar'` com dataset extra `type: 'line'`). Nunca separar em dois gráficos o que a fonte mostra junto — a sobreposição é a informação.
3. **Escala coerente** — eixo Y deve começar em 0 para comparações de magnitude. Exceção permitida só para séries temporais de variação relativa (ex: taxa de retorno). Nunca usar eixo duplo sem legenda explícita. Unidades (R$ bi, %, k) obrigatórias nos ticks.

**Tabelas:**
- 4+ linhas OU 3+ colunas de dados → `<table class="data-table">` obrigatório (nunca bullets de texto, nunca ASCII).
- Sticky `<thead>`, alternating rows, status badges (nunca emoji como status).
- **Dados completos** — todas as linhas da fonte entram na tabela. Nunca truncar com "ver mais" ou omitir linhas por espaço — ajustar o layout, nunca cortar o conteúdo.
- Pattern completo em `references/css-patterns.md § 3`.

**Mermaid:**
- Todo diagrama Mermaid precisa de zoom/pan controls.
- Estrutura: `.diagram-shell → .zoom-controls → .mermaid-viewport → .mermaid-canvas`.
- JS completo em `references/css-patterns.md § 4`.

**Deck engine v3 — features obrigatórias ao gerar deck:**
- **Wake Lock**: automático no engine — tela não dorme durante apresentação.
- **Overview** (`O`): grade de todos os slides. Gerar decks longos sabendo que o apresentador pode navegar via overview.
- **Auto-Animate**: usar `data-auto-animate` + `data-id` em slides consecutivos onde o mesmo elemento muda de escala/posição (ex: KPI que cresce de card para big-num).
- **Layouts semânticos**: usar `layout-fact` para KPIs isolados, `layout-quote` para citações, `layout-two-cols` para comparações, `layout-statement` para one-liners. Nunca improvizar layout inline quando existe semântico.
- **Tipos de fragmento**: usar `current-visible` para listas onde o contexto de cada item importa (spotlight); `grow` para revelar KPIs com impacto. **Não usar `highlight-current` em linhas de tabela** — tabelas no deck têm hover apresentador-controlado nativo (passa o mouse sobre uma linha → destaca; demais ficam muted).
- **Rough Notation**: `data-mark="circle"` em números-âncora, `data-mark="underline"` em termos-chave. Ativa automático ao entrar no slide. Cor default = `--color-accent`.
- **AutoFitText**: `data-fit-text` em títulos de comprimento variável. Nunca hardcodar font-size menor só para caber.
- **Tabelas com hover apresentador**: toda `.data-table` dentro de `.slide` ganha hover automático — o apresentador passa o mouse sobre qualquer linha durante a apresentação e ela ganha destaque (background accent + bold); as demais ficam muted. Nunca usar fragmentos linha-a-linha em tabelas.
- **Posicionamento relativo**: usar `data-fragment-index="+1"` em listas — nunca índices absolutos sequenciais que quebram ao reordenar.
- **Background por slide**: slides de seção/divisor usam `data-background-color="var(--itau-orange)"` (tema itaú) para identidade visual forte.
- **Code Stepping**: blocos de código com narrativa progressiva usam `data-line-numbers="1-3|5-7|10"`.

Referência completa em `references/slide-patterns.md § Features do engine v3`.

---

## Workflow de geração

1. **Briefing** (acima) → confirmar antes de escrever HTML.
2. **Think → Structure → Style** (seção acima).
3. **Geração** — usar `assets/templates/template-<modelo>.html` como esqueleto, popular com conteúdo real, aplicar tema.
4. **Validação** — checar checklist de `references/css-patterns.md` (squint test, swap test, overflow, ambos os temas).
5. **Entrega** — salvar no diretório indicado.

Detalhes em [references/workflow.md](references/workflow.md).

---

## Estrutura do repositório

```
slideless/
├── SKILL.md                          ← este arquivo
├── README.md                         ← onboarding humano
├── .claude-plugin/plugin.json        ← manifest
├── commands/                         ← slash commands (1 arquivo cada)
├── references/
│   ├── design-system.md              ← tokens, dark mode, boot script
│   ├── componentes.md                ← biblioteca de componentes
│   ├── anti-patterns.md              ← PPT-isms proibidos (LER PRIMEIRO)
│   ├── decisao-modelo.md             ← decision tree dos 5 modelos
│   ├── protocolo-sem-conteudo.md     ← o que fazer sem conteúdo real
│   ├── importar-conteudo.md          ← regras de conversão MD/PPT/Confluence
│   ├── workflow.md                   ← passo-a-passo de geração
│   ├── checklist-revisao.md          ← validação LLM
│   ├── modelos/                      ← spec detalhada por modelo
│   │   └── {handbook,hub,scrollytelling,site,deck}.md
│   └── temas/
│       └── {neutro,itau}.md
├── assets/
│   ├── temas/{neutro,itau}.css       ← tokens light+dark prontos
│   ├── logos/itau.png
│   ├── exemplos/                     ← showcases preenchidos com "Plataforma de Dados Itaú"
│   │   └── exemplo-{handbook,hub,scrollytelling,site,deck}.html
│   └── templates/                    ← esqueletos vazios para popular
│       └── template-{handbook,hub,scrollytelling,site,deck}.html
├── scripts/
│   ├── validar.py                    ← validador determinístico (sem LLM)
│   └── exportar_pdf.py               ← Playwright async
└── demos/                            ← input → output reais pareados
```

---

## Tabela de roteamento rápida

| Pedido do usuário | Modelo |
|---|---|
| "manual do time", "documentação", "handbook", "onboarding" | `handbook` |
| "portal de recursos", "central de X", "catálogo" | `hub` |
| "relatório anual interativo", "página narrativa pra ler" | `scrollytelling` |
| "microsite", "site interno", "página com várias abas" | `site` |
| "pitch", "apresentação", "deck", "all-hands" (ao vivo) | `deck` |
| "deck pra distribuir como leitura" | `scrollytelling` (não `deck`) |
| "relatório anual", "white paper", "documento executivo PDF" | `report` |
| "página de divulgação interna" | `hub` ou `scrollytelling` — perguntar |
