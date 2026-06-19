# slideless — instruções para o agente

Este projeto é a skill **slideless**: gera apresentações e documentos HTML single-file para o Itaú.

> **Compatibilidade:** este arquivo serve tanto para **Claude Code** (`CLAUDE.md`) quanto para outros harnesses. Para **GitHub Copilot Chat**, o arquivo equivalente `.github/copilot-instructions.md` também está presente neste repo. Conteúdo igual.

## Leia antes de qualquer tarefa

Spec principal da skill: [SKILL.md](SKILL.md). Lê on-demand quando uma tarefa começar — **não usar `@-includes` inline**, isso causa 502 no Copilot Chat por exceder o limite de payload do gateway. Links markdown normais permitem ao agente abrir o arquivo só quando precisar.

## References (consultar conforme necessário)

Não carregar inline. Abrir só quando o trabalho exigir:

- **Direção de arte (o Parti — LER ANTES DE GERAR):** [references/direcao-de-arte.md](references/direcao-de-arte.md)
- Kits tipográficos + fontes banidas: [references/type-kits.md](references/type-kits.md)
- Ambição (teto cutting-edge A1/A2/A3 + momentos-wow): [references/ambicao.md](references/ambicao.md)
- **Wow components (drop-ins copy-paste W1-W31 — o CÓDIGO dos momentos-wow, colar verbatim):** [references/wow-components.md](references/wow-components.md)
- Design system, tokens, dark mode, boot script: [references/design-system.md](references/design-system.md)
- Componentes reutilizáveis: [references/componentes.md](references/componentes.md)
- Padrões CSS (gráficos, tabelas, depth tiers, Mermaid): [references/css-patterns.md](references/css-patterns.md)
- Padrões de slides (engine v3, fragmentos, char limits, pitfalls): [references/slide-patterns.md](references/slide-patterns.md)
- Anti-patterns ("PPT-isms" proibidos — LER ANTES da primeira geração): [references/anti-patterns.md](references/anti-patterns.md)
- Decisão entre modelos: [references/decisao-modelo.md](references/decisao-modelo.md)
- Sem conteúdo real, sem geração: [references/protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md)
- Workflow passo-a-passo: [references/workflow.md](references/workflow.md)
- Spec detalhada por modelo: [references/modelos/](references/modelos/)
- Temas (itau / neutro): [references/temas/](references/temas/)

## Estrutura do projeto

```
slideless/
  SKILL.md                    ← spec principal (router enxuto, ~10KB)
  CLAUDE.md                   ← este arquivo (instruções para Claude Code)
  .github/
    copilot-instructions.md   ← instruções equivalentes para GitHub Copilot Chat
  README.md                   ← onboarding humano
  assets/
    templates/                ← templates base por modelo (handbook, hub, scrollytelling, site, deck, report)
    temas/                    ← itau.css (laranja #FF6200), neutro.css (azul)
  commands/                   ← só slideless.md (roteador fino do Claude Code → references/comandos/)
  references/                 ← doc técnica + comandos/ (specs dos 31 subcomandos, FONTE ÚNICA)
  demos/                      ← exemplos pareados (3 famílias × 7 documentos: os 6 modelos + deck-overdrive)
```

## Comandos principais

A skill tem **um comando só** — `/slideless` — e você escreve o subcomando logo depois (ex.: `/slideless deck`, `/slideless criar`, `/slideless auditar arquivo.html`). Os 31 subcomandos vivem em [references/comandos/](references/comandos/). Os mais usados:

| Comando | O que faz |
|---|---|
| **`/slideless criar`** | Wizard para áreas de negócios (5 perguntas, escolhe modelo automaticamente) |
| `/slideless estruturar` | Analisa conteúdo bruto e propõe mapa estruturado antes de gerar |
| `/slideless handbook` | Manual com sidebar + TOC |
| `/slideless hub` | Portal de cards categorizáveis |
| `/slideless scrollytelling` | Narrativa scroll-triggered |
| `/slideless site` | SPA com hash routing |
| `/slideless deck` | Apresentação ao vivo (slides + keyboard nav) |
| `/slideless report` | Relatório editorial denso (PDF-friendly) |

Tabela completa em [README.md](README.md).

## Regras invioláveis (resumo)

1. **Single-file HTML** — CSS e JS inline. CDN só para Google Fonts, Chart.js, Rough Notation, Three.js (overdrive).
2. **Boot script antes do CSS** — sem flash de tema. Pattern em [references/design-system.md](references/design-system.md).
3. **Nada vaza da viewport** — char limits respeitados (mega ≤50, xl ≤70, lg ≤90, lead ≤220). Template-deck tem `autoFitSlide()` como rede de segurança.
4. **Gráficos com dados completos** — nunca omitir pontos, composição preservada (bar+line = 1 Chart.js misto), escala Y começa em 0 para magnitudes, unidades nos ticks.
5. **Tabelas com todas as linhas** — nunca truncar com "ver mais". 4+ linhas ou 3+ colunas → sempre `<table class="data-table">`.
6. **Conteúdo real obrigatório** — sem fonte do usuário, não inventar dados internos do Itaú. Aplicar [protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md).
7. **WCAG AA** — foco visível, ARIA correto, keyboard nav, `prefers-reduced-motion` respeitado.

Detalhes completos no [SKILL.md](SKILL.md).
