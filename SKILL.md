---
name: slideless
description: Substitui PowerPoint por documentos web HTML single-file (CSS+JS inline, portátil, dark mode nativo, WCAG AA). Seis modelos: handbook (sidebar+TOC tipo GitLab), hub (cards categorizáveis), scrollytelling (narrativa scroll-triggered), site (SPA hash routing), deck (slides com keyboard nav) e report (relatório editorial denso, PDF-friendly). Tema neutro (azul) ou itau (laranja #FF6200). Use quando pedir manual, handbook, portal/hub, scrollytelling, microsite, pitch/all-hands, ou relatório executivo PDF.
---

# slideless

Skill para gerar **documentos web interativos** em HTML single-file. NÃO é "PPT em HTML": vibe Notion/GitLab handbook. Exceção explícita: modelo `deck` (apresentação ao vivo).

> Ler [references/anti-patterns.md](references/anti-patterns.md) antes da primeira geração da sessão.

---

## Seis modelos

| Modelo | Use quando | Referência |
|---|---|---|
| `handbook` | manual longo, onboarding, política, runbook (vibe GitLab) | [modelos/handbook.md](references/modelos/handbook.md) |
| `hub` | portal de cards categorizáveis, central de recursos | [modelos/hub.md](references/modelos/hub.md) |
| `scrollytelling` | narrativa scroll-triggered com sticky chart (vibe NYT Upshot) | [modelos/scrollytelling.md](references/modelos/scrollytelling.md) |
| `site` | mini-site SPA com 2-5 views (hash routing) | [modelos/site.md](references/modelos/site.md) |
| `deck` | pitch/all-hands ao vivo (único com tipografia gigante OK) | [modelos/deck.md](references/modelos/deck.md) |
| `report` | relatório editorial denso, PDF-friendly (vibe Itaú Pesquisa Macro) | [modelos/report.md](references/modelos/report.md) |

**Decisão entre modelos:** [references/decisao-modelo.md](references/decisao-modelo.md). Quando ambíguo, **perguntar** — não chutar.

---

## Princípios invioláveis

1. **Single-file.** CSS e JS inline. CDN só para Google Fonts, Chart.js, Rough Notation, Three.js (overdrive). Tamanho: ≤1MB editorial; ≤5MB para `deck`/`overdrive`.
2. **Nada vaza da viewport.** Conteúdo nunca pode ser cortado, ocultado pela HUD, gerar scroll horizontal. Template-deck aplica overflow guard CSS + `autoFitSlide()` JS — mas respeitar char limits abaixo na geração:
   | Classe | Limite | Se exceder |
   |---|---|---|
   | `.title-mega` / `.fact-val` / `.statement-text` | ≤ 50 chars | dividir em 2 elementos ou usar `.title-lg` |
   | `.title-xl` | ≤ 70 chars | trocar para `.title-lg` |
   | `.title-lg` | ≤ 90 chars | trocar para `.title-md` |
   | `.lead-deck` | ≤ 220 chars | quebrar em duas frases |
3. **Dark mode nativo.** Boot script no `<head>` antes do CSS (sem flash). Toggle no header. Persistente via `localStorage`. Detalhes em [references/design-system.md](references/design-system.md).
4. **Conteúdo real obrigatório.** Sem conteúdo do usuário, NUNCA inventar dados internos do Itaú ou gerar lorem ipsum. Protocolo: [references/protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md).
5. **Tipografia editorial fora de `deck`.** H1 ~2.5rem, h2 ~1.75rem, body 1rem. NUNCA `clamp(vw)` gigante exceto no `deck`. Anti-pattern: "PPT estilizado em HTML". Ver [references/anti-patterns.md](references/anti-patterns.md).
6. **WCAG AA.** Foco visível, ARIA correto, keyboard nav, `prefers-reduced-motion` respeitado.
7. **Fidelidade de dados.** Gráficos completos (todos os pontos da fonte, escala Y começa em 0 para magnitudes, unidades nos ticks, composição preservada — bar+line junto = 1 chart misto). Tabelas com TODAS as linhas (≥4 linhas ou ≥3 colunas → `<table>`, nunca bullets).

---

## Comandos (30)

### Criação (1 wizard + 1 pré-geração + 6 modelos)
| Comando | Função |
|---|---|
| `/criar` | Wizard para áreas de negócios: 5 perguntas em PT-BR e escolhe modelo |
| `/estruturar` | Analisa conteúdo bruto e propõe mapa para aprovação antes de gerar |
| `/slideless-handbook` `<tópico>` | Cria handbook (sidebar + scrollspy + TOC) |
| `/slideless-hub` `<tópico>` | Cria hub (cards categorizáveis) |
| `/slideless-scrollytelling` `<tópico>` | Cria scrollytelling (reveal + sticky chart) |
| `/slideless-site` `<tópico>` | Cria site SPA single-file |
| `/slideless-deck` `<tópico>` | Cria deck moderno (keyboard nav, fragments) |
| `/slideless-report` `<tópico>` | Cria relatório editorial denso (PDF-friendly) |

### Importação (3)
`/importar-confluence <url\|anexo>`, `/importar-ppt <arquivo>`, `/importar-md <arquivo>`. Detalhes em [references/importar-conteudo.md](references/importar-conteudo.md).

### Edição cirúrgica (6)
`/adicionar-secao <título>` (handbook/scrollytelling/site), `/adicionar-slide <tipo>` (deck), `/adicionar-callout <tipo>` (info/tip/warn/danger), `/adicionar-grafico <tipo>` (line/bar/donut/gauge/radar/bubble/waterfall/mixed), `/adicionar-fragment` (deck), `/adicionar-toc` (handbook).

### Transformação (3)
`/aplicar-tema <neutro\|itau>`, `/converter-modelo <novo>` (handbook ↔ scrollytelling, hub ↔ site), `/distill` (reduz handbook longo a sumário).

### Refinamento de design (5 verbos independentes — compõem em sequência)
| Comando | Função |
|---|---|
| `/slideless-bolder` | Tipografia +30%, glow reforçado, números circulados via Rough Notation |
| `/slideless-quieter` | Tipografia −15%, cores muted, motion calma, fallback serif editorial |
| `/slideless-animate` | heroIn, Auto-Animate FLIP, counters, stagger reveals (respeita reduced-motion) |
| `/slideless-delight` | Hover lifts, spotlight cursor-aware, shimmer, parallax sutil |
| `/slideless-overdrive` | WebGL hero, Chart.js plugins, variable font, cinematic. **Interativo** (pergunta quais efeitos). Até 5MB |

Composição típica: `bolder` + `animate` (executivo) · `quieter` + `delight` (editorial refinado) · `bolder` + `overdrive` (showpiece).

### Qualidade (4)
`/auditar` (validador + checklist), `/polir` (tipografia/espaçamento), `/harden` (a11y + reduced-motion), `/acessibilidade` (varredura WCAG isolada).

### Export (2)
`/exportar-pdf` (Playwright), `/exportar-screenshots` (1 PNG por slide/seção).

---

## Briefing mínimo antes de gerar

1. **Modelo** — se ambíguo, consulte [decisao-modelo.md](references/decisao-modelo.md) e pergunte.
2. **Conteúdo real** — texto, MD, PPT, dados. Sem conteúdo, aplique [protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md).
3. **Tema** (`neutro` ou `itau`, default `itau`).
4. **Escopo** — quantas seções/cards/slides/views aproximadamente.

---

## Workflow

Resumo: **Think → Structure → Style → Deliver**. Passo-a-passo completo em [references/workflow.md](references/workflow.md).

1. **Think.** Quem lê? Que tipo de conteúdo? Qual estética (warm signal / blueprint / editorial / terminal mono)? **Proibido:** neon dashboard (cyan+magenta+purple), Inter+violet/indigo+gradient text, emoji como ícones.
2. **Structure.** Use o template correto em `assets/templates/template-<modelo>.html`. Inventariar elementos discretos (mandatório para deck) — nada pode ficar sem destino.
3. **Style.** Hierarquia via escala+peso+cor (não cores flashy). Depth tiers (hero/default/recessed). Backgrounds atmosféricos (glow radial, dot grid, gradient mesh — nunca fundo flat). Animações ganham seu lugar (stagger, heroIn, counters). Nunca Inter sozinho — usar font pairing distinto.
4. **Deliver.** Salvar no diretório indicado, abrir no browser (testar ambos os temas, redimensionar), reportar path + o que foi gerado.

---

## Regras específicas do `deck`

Engine v3 — features obrigatórias (todas no template, não duplicar nem remover):

- **Wake Lock** (tela não dorme), **Overview** (`O`), **Auto-Animate** (`data-auto-animate` + `data-id` em slides consecutivos), **AutoFitText** (`data-fit-text` em títulos variáveis), **Rough Notation** (`data-mark="circle"` em números-âncora, `"underline"` em termos-chave).
- **Fragmentos**: `current-visible` para listas (spotlight); `grow` para KPIs. **NÃO usar `highlight-current` em `<tr>`** — tabelas têm hover apresentador-controlado nativo (mouse over destaca; demais ficam muted).
- **Posicionamento relativo**: `data-fragment-index="+1"` (nunca índices absolutos).
- **Background por slide**: `data-background-color="var(--itau-orange)"` em divisores.
- **Layouts semânticos**: `layout-fact` (KPI), `layout-quote` (citação), `layout-two-cols` (comparação), `layout-statement` (one-liner). Nunca inventar layout inline quando existe semântico.
- **Canvas overdrive**: SEMPRE `data-overdrive` no `<canvas>` para a regra global não capturá-lo como layout (vazaria o hero).

Referência completa: [references/slide-patterns.md](references/slide-patterns.md). Padrões CSS de gráficos/tabelas/Mermaid: [references/css-patterns.md](references/css-patterns.md). Componentes reutilizáveis: [references/componentes.md](references/componentes.md).

---

## Tabela de roteamento rápida

| Pedido do usuário | Modelo |
|---|---|
| "manual", "documentação", "handbook", "onboarding" | `handbook` |
| "portal de recursos", "central de X", "catálogo" | `hub` |
| "relatório anual interativo", "página narrativa pra ler" | `scrollytelling` |
| "microsite", "site interno", "página com várias abas" | `site` |
| "pitch", "apresentação", "deck", "all-hands" (ao vivo) | `deck` |
| "deck pra distribuir como leitura" | `scrollytelling` (não `deck`) |
| "relatório anual", "white paper", "documento executivo PDF" | `report` |
| "página de divulgação interna" | `hub` ou `scrollytelling` — perguntar |

---

## References (consultar conforme necessário)

- [anti-patterns.md](references/anti-patterns.md) — PPT-isms proibidos (LER PRIMEIRO)
- [design-system.md](references/design-system.md) — tokens, dark mode, boot script
- [componentes.md](references/componentes.md) — biblioteca de componentes
- [css-patterns.md](references/css-patterns.md) — gráficos, tabelas, depth tiers, Mermaid
- [slide-patterns.md](references/slide-patterns.md) — engine v3, fragmentos, char limits, pitfalls
- [decisao-modelo.md](references/decisao-modelo.md) — decision tree dos 6 modelos
- [protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md) — sem dados reais, sem geração
- [importar-conteudo.md](references/importar-conteudo.md) — MD/PPT/Confluence → slideless
- [workflow.md](references/workflow.md) — passo-a-passo completo
- [checklist-revisao.md](references/checklist-revisao.md) — validação LLM
- [modelos/](references/modelos/) — spec detalhada por modelo
- [temas/](references/temas/) — temas itau/neutro

Estrutura do repositório, instalação, comandos detalhados: [README.md](README.md).
