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
8. **Nenhum HTML antes do parti.** Todo documento nasce do bloco `<!-- slideless:parti -->` no `<head>` — 7 decisões derivadas do CONTEÚDO (registro, kit tipográfico, capa, superfície+luz, motion, **ambição**, momento assinatura) + 3 renúncias (`nao-vai-ter`). Capa, kit e superfície nunca repetem o exemplo canônico do modelo. Mecanismo completo: [references/direcao-de-arte.md](references/direcao-de-arte.md).
9. **Ambição cutting-edge derivada do conteúdo.** A 7ª decisão `ambicao` (A1-contido / A2-elevado / A3-extraordinário) é ortogonal ao registro: default **A2-elevado** para deck/scrollytelling/hub/site/handbook (materialidade de assinatura, springs, scroll-driven, tipografia cinética, 3–5 momentos-wow data-bound) e **A1-contido** para report/regulatório (agora 1–2 momentos CALMOS estático-seguros — W6/W8/W2/W22/W10 — nunca premium loud). A1/A2/A3 entregam **momentos-wow empilhados** (W1-W31; **A1/sóbrio 1–2 calmos, A2 3–5, A3 6–8 ≥4 famílias**: 1 herói pinned + 2 sistemas ambientes na mesma `--spring` + momentos espaçados — ver §STACKING em wow-components.md), cada um ligado ao dado-tese, com `@supports`+fallback e branch reduced-motion. **Grain/aurora/glass são materialité (`superficie`), NÃO quitam a ambição** (P8 cobra técnica substantiva). A ambição respeita o registro como teto: a camada premium W10-W31 ("agência premiada", exceto os ambientes W21/W22/W25/W29) é gateada a registros expressivos. Doutrina: [references/ambicao.md](references/ambicao.md). **CÓDIGO copy-paste: [references/wow-components.md](references/wow-components.md).**

---

## Invocação — `/slideless <subcomando>` (agnóstico a harness)

A skill tem **um único comando universal**: `/slideless`. O usuário escreve o **subcomando** e o contexto logo depois — ex.: `/slideless deck pitch do 1T26`, `/slideless criar`, `/slideless auditar caminho.html`. Cada subcomando é um spec em `references/comandos/<nome>.md` (**fonte única**). Não há slash-command individual por subcomando — assim a skill funciona igual em **Claude Code, GitHub Copilot, Devin** e qualquer harness que carregue este arquivo. As entradas nativas (`commands/slideless.md`, `.github/prompts/slideless.prompt.md`) são finas e só apontam para cá.

### Dispatch (como rotear)
1. Tome a **primeira palavra** do argumento como o subcomando.
2. Casou (exato ou por sinônimo) com um arquivo de `references/comandos/`? **Leia e siga à risca** `references/comandos/<subcomando>.md`, usando o resto da linha como o pedido/conteúdo.
3. Argumento **vazio, ambíguo, ou a pessoa não sabe o que quer**? → siga `references/comandos/criar.md` (wizard) ou liste o catálogo e pergunte.
4. **Sinônimos PT** (mapeiam pro modelo): manual→handbook · portal/central de recursos→hub · narrativa/história com dados→scrollytelling · microsite→site · pitch/apresentação ao vivo→deck · relatório (formal/PDF)→report.

### Catálogo de subcomandos (31 → `references/comandos/<nome>.md`)

- **Criação** — `criar` (wizard PT-BR, 5 perguntas, escolhe o modelo) · `estruturar` (mapa do conteúdo p/ aprovação antes de gerar)
- **Modelos** `<tópico>` — `deck` (slides, keyboard nav, fragments) · `handbook` (sidebar + scrollspy + TOC) · `hub` (cards categorizáveis) · `scrollytelling` (reveal + sticky chart) · `site` (SPA single-file) · `report` (relatório editorial denso, PDF-friendly)
- **Importação** — `importar-ppt <arquivo>` · `importar-md <arquivo>` · `importar-confluence <url\|anexo>`. Detalhes: [references/importar-conteudo.md](references/importar-conteudo.md)
- **Edição cirúrgica** — `adicionar-secao <título>` (handbook/scrollytelling/site) · `adicionar-slide <tipo>` (deck) · `adicionar-callout <info\|tip\|warn\|danger>` · `adicionar-grafico <tipo>` (line/bar/donut/gauge/radar/bubble/waterfall/mixed) · `adicionar-fragment` (deck) · `adicionar-toc` (handbook)
- **Transformação** — `aplicar-tema <neutro\|itau>` · `converter-modelo <novo>` (handbook ↔ scrollytelling, hub ↔ site) · `distill` (reduz handbook longo a sumário)
- **Refinamento de design** (5 verbos, compõem em sequência) — `bolder` (tipografia +30%, números circulados) · `quieter` (−15%, muted, motion calma) · `animate` (heroIn, FLIP, counters, stagger) · `delight` (hover lift, spotlight, shimmer, parallax) · `overdrive` (WebGL hero, Chart.js plugins, variable font; **interativo**; até 5MB). Composição: `bolder`+`animate` (executivo) · `quieter`+`delight` (editorial) · `bolder`+`overdrive` (showpiece)
- **Qualidade** — `auditar` (validador + checklist) · `polir` (tipografia/espaçamento) · `harden` (a11y + reduced-motion) · `acessibilidade` (varredura WCAG)
- **Export** — `exportar-pdf` (Playwright) · `exportar-screenshots` (1 PNG por slide/seção)

---

## Briefing mínimo antes de gerar

1. **Modelo** — se ambíguo, consulte [decisao-modelo.md](references/decisao-modelo.md) e pergunte.
2. **Conteúdo real** — texto, MD, PPT, dados. Sem conteúdo, aplique [protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md).
3. **Tema** (`neutro` ou `itau`, default `itau`).
4. **Escopo** — quantas seções/cards/slides/views aproximadamente.

---

## Workflow

Resumo: **Think → Parti → Structure → Style → Deliver**. Passo-a-passo completo em [references/workflow.md](references/workflow.md).

1. **Think.** Quem lê? Que tipo de conteúdo? O que o ASSUNTO pede visualmente? **Proibido:** neon dashboard (cyan+magenta+purple), Inter+violet/indigo+gradient text, emoji como ícones.
2. **Parti (obrigatório, antes de qualquer HTML).** Abrir [references/direcao-de-arte.md](references/direcao-de-arte.md), preencher o bloco `<!-- slideless:parti -->` — 7 decisões derivadas do conteúdo (incl. `ambicao` — ver [references/ambicao.md](references/ambicao.md)), cada uma citando a fonte — e colá-lo no `<head>`. Ler o parti do exemplo canônico do modelo e do último documento da pasta (não repetir capa/kit/superfície). Se `ambicao` A2/A3, declarar o(s) `momento-wow`.
3. **Structure.** Use o template correto em `assets/templates/template-<modelo>.html`. Inventariar elementos discretos (mandatório para deck) — nada pode ficar sem destino.
4. **Style.** Compor a camada de direção conforme o parti: kit no slot `SLIDELESS:TYPE-KIT`, superfície do cardápio (flat é legítimo; glow nunca é obrigatório), perfil de motion colado como bloco aditivo. Hierarquia via escala+peso+cor. Nunca Inter sozinho — kit de [references/type-kits.md](references/type-kits.md).
5. **Deliver.** Salvar no diretório indicado. **Validar SEMPRE antes de entregar**: `python scripts/validar.py <arquivo>` (estrutura) **E** `python scripts/smoke.py <arquivo>` (render — pega JS quebrado, conteúdo invisível e placeholder que o validador estrutural NÃO vê). Os dois precisam passar. Conferir o checklist de saída do [direcao-de-arte.md](references/direcao-de-arte.md), reportar path + o que foi gerado.

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

- [anti-patterns.md](references/anti-patterns.md) — PPT-isms e AI-tells proibidos (LER PRIMEIRO)
- [direcao-de-arte.md](references/direcao-de-arte.md) — o Parti: 7 decisões por documento (LER ANTES DE GERAR)
- [ambicao.md](references/ambicao.md) — o teto cutting-edge: eixo A1/A2/A3 + momentos-wow W1-W9 + régua de craft (LER para A2/A3)
- [wow-components.md](references/wow-components.md) — **drop-ins copy-paste W1-W31 (o CÓDIGO dos momentos-wow + premium): colar verbatim, não improvisar** (A2/A3)
- [type-kits.md](references/type-kits.md) — pool de kits tipográficos + fontes (cinéticas) + banidas
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
