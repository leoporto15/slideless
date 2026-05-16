---
name: apresentacoes-html
description: Cria documentos web interativos profissionais em HTML — handbooks com sidebar e scrollspy, hubs de conteúdo com cards navegáveis, narrativas scrollytelling com animações disparadas ao scroll, mini-sites SPA single-file, e decks de apresentação modernos com transições animadas e modo fullscreen. Use sempre que o usuário pedir material interno em HTML: handbook, manual, central de conhecimento, documentação rica, microsite, relatório anual interativo, página interna de produto, hub de recursos, narrativa interativa, deck/pitch/apresentação que substitua PPT (com animações modernas, keyboard navigation, fragments staggered, fullscreen), página web para divulgação interna, ou qualquer conteúdo que se beneficie de navegação não-linear, modo dark/light, densidade variável e componentes interativos (toggles, tabs, callouts, gráficos, modais). Inclui tema neutro padrão e tema corporativo Itaú, ambos com dark mode nativo. Cada arquivo entregue é single-file portátil (HTML único com CSS e JS inline).
---

# apresentacoes-html

Skill para gerar **documentos web interativos** em HTML single-file. Cinco modelos cobrem do material denso e navegável até apresentação linear estilo PPT-moderno.

## Princípio: tudo single-file

Todo modelo entrega **um único HTML** com CSS e JS inline. Portável, hospedável em qualquer S3 estático, distribuível como anexo. Sem dependências de arquivos externos (exceto fontes/charts via CDN).

## Cinco modelos

O usuário escolhe o modelo no briefing. Cada um tem template, exemplo e documentação específica.

### `handbook` — manual com sidebar fixa
**Use quando:** documentação longa, manual de processo, central de conhecimento, onboarding, política interna, livro de práticas.
**Estrutura:** sidebar de navegação à esquerda + conteúdo central + TOC sticky à direita com scrollspy.
**Referência mental:** GitLab Handbook, Stripe Docs, Notion Pages.
**Doc:** `references/modelos/handbook.md`. **Exemplo:** `assets/exemplos/exemplo-handbook.html`.

### `hub` — portal com cards navegáveis
**Use quando:** central de recursos, catálogo de serviços, hub de time, landing interna agregando múltiplas dimensões.
**Estrutura:** grid de cards categorizados com filtros; click abre painel correspondente in-page.
**Referência mental:** Notion Workspace, Apple Developer hub.
**Doc:** `references/modelos/hub.md`. **Exemplo:** `assets/exemplos/exemplo-hub.html`.

### `scrollytelling` — narrativa única scroll-triggered
**Use quando:** relatório anual interativo, caso de estudo aprofundado, narrativa de projeto, divulgação editorial.
**Estrutura:** página única longa; seções revelam ao scroll; gráficos sticky que mudam ao avançar; progress bar no topo.
**Referência mental:** NYT The Upshot, The Pudding, Apple product pages.
**Doc:** `references/modelos/scrollytelling.md`. **Exemplo:** `assets/exemplos/exemplo-scrollytelling.html`.

### `site` — mini-site SPA single-file
**Use quando:** microsite com 2-5 dimensões (home, sobre, recursos), lançamento interno, portfólio de squad.
**Estrutura:** UM arquivo HTML; header de nav troca entre `<article class="view">` via hash routing (`#home`, `#sobre`). Sem reload.
**Referência mental:** Linear, Vercel guides, Notion product pages.
**Doc:** `references/modelos/site.md`. **Exemplo:** `assets/exemplos/exemplo-site.html`.

### `deck` — apresentação moderna sequencial
**Use quando:** pitch executivo linear, all-hands, talk de conferência interna, demo guiada — quando há narrativa linear curta e você apresenta junto.
**Estrutura:** sequência de "slides" (cada um ocupa o viewport); navegação por setas/teclado/swipe; transições animadas; fragments; fullscreen; counters; theme toggle.
**Referência mental:** Apple keynotes, Linear launches, Pitch.com modernas.
**Doc:** `references/modelos/deck.md`. **Exemplo:** `assets/exemplos/exemplo-deck.html`.

**Importante:** `deck` é o único modelo onde tipografia gigante (4-6rem) é apropriada — porque é viewport-cheio, apresentação ao vivo. Em todos os outros modelos a tipografia é editorial.

## Princípios transversais (válidos pros 5 modelos)

1. **Single-file por padrão.** CSS e JS inline. Fontes e gráficos via CDN.
2. **Dark mode nativo.** Toggle no header, persistência via `localStorage`, boot script antes do CSS pintar (sem flash).
3. **Animações funcionais.** Reveal-on-scroll, números que contam, fade-in. Nunca parallax dramático ou decoração vazia.
4. **Interatividade real.** Toggles funcionam, tabs trocam, callouts coloridos, código copiável, gráficos respondem.
5. **Acessibilidade.** WCAG AA, `aria-*` correto, keyboard navigation, `prefers-reduced-motion` respeitado.

## Diferença entre `scrollytelling`, `deck` e `site`

Confusão comum. Decisão rápida:

| Pergunta | scrollytelling | deck | site |
|---|---|---|---|
| Como o leitor avança? | Scroll natural | Setas/teclado/click | Click em link de nav |
| O leitor lê sozinho ou alguém apresenta? | Sozinho | Apresentador ao vivo | Sozinho |
| Quantas "cenas/páginas"? | 5-15 seções verticais | 8-20 slides | 2-5 views |
| Há narrativa única linear? | Sim | Sim | Não — dimensões independentes |
| Tipografia gigante OK? | Não (editorial) | Sim (viewport-cheio) | Não (editorial) |

## Subcomandos

### Criação
- `criar-handbook` / `criar-hub` / `criar-scrollytelling` / `criar-site` / `criar-deck`

### Modificação
- `adicionar-secao` / `adicionar-slide` (deck)
- `aplicar-tema` (troca `neutro` ⇄ `itau`)
- `adicionar-componente` (callout, tab, toggle, gráfico — ver `references/componentes.md`)

### Análise e conversão
- `revisar-doc` (usa `references/checklist-revisao.md`)
- `exportar-pdf` (usa `scripts/exportar_pdf.py`; deck vira PDF landscape, demais retrato)
- `importar-conteudo` (regras em `references/importar-conteudo.md`)

## Roteamento

| Pedido do usuário | Modelo |
|---|---|
| "manual do time", "documentação", "handbook" | `handbook` |
| "portal de recursos", "central de X" | `hub` |
| "relatório anual interativo", "página narrativa pra ler" | `scrollytelling` |
| "microsite", "site interno", "página com várias abas" | `site` |
| "pitch", "apresentação", "deck", "all-hands" | `deck` |
| "deck que substitua PPT" (uso interno, leitura) | perguntar: vai apresentar ao vivo? → `deck` / vai distribuir para leitura? → `scrollytelling` |
| "página de divulgação interna" | `hub` ou `scrollytelling` (perguntar) |

## Briefing mínimo antes de gerar

1. **Modelo** — se ambíguo, perguntar com base na tabela acima.
2. **Conteúdo real** — texto, MD, PPT, dados. Sem conteúdo, peça antes de começar.
3. **Tema** (`neutro` / `itau`).
4. **Escopo** — quantas seções/cards/slides/views aproximadamente.

## Estrutura do projeto

```
apresentacoes-html/
├── SKILL.md
├── references/
│   ├── design-system.md            ← OBRIGATÓRIO antes de gerar
│   ├── componentes.md              ← biblioteca de componentes
│   ├── workflow.md
│   ├── checklist-revisao.md
│   ├── importar-conteudo.md
│   ├── modelos/
│   │   ├── handbook.md
│   │   ├── hub.md
│   │   ├── scrollytelling.md
│   │   ├── site.md
│   │   └── deck.md
│   └── temas/{neutro,itau}.md
├── assets/
│   ├── temas/{neutro,itau}.css     ← tokens com light + dark
│   ├── logos/itau.png
│   └── exemplos/
│       ├── exemplo-handbook.html
│       ├── exemplo-hub.html
│       ├── exemplo-scrollytelling.html
│       ├── exemplo-site.html       ← SPA single-file
│       └── exemplo-deck.html       ← deck moderno
└── scripts/exportar_pdf.py
```

## Entrega

Todo subcomando que gera HTML deve:
1. Salvar single-file em `/mnt/user-data/outputs/` com nome descritivo.
2. Validar contra `references/checklist-revisao.md`.
3. Usar `present_files` com o HTML principal.
