# slideless — instruções para GitHub Copilot Chat

Este repositório é a skill **slideless**: gera apresentações e documentos HTML single-file para o Itaú.

> **Por que este arquivo existe:** GitHub Copilot Chat carrega `.github/copilot-instructions.md` automaticamente como system prompt em toda interação. Conteúdo equivalente em [CLAUDE.md](../CLAUDE.md) para Claude Code. Tamanho deliberadamente enxuto (<5KB) para não bater no limite de payload do gateway do Copilot — referências detalhadas são carregadas on-demand via links markdown normais (NUNCA usar `@-includes` inline).

## Leia primeiro

Spec principal da skill: **[SKILL.md](../SKILL.md)**. Abrir on-demand quando uma tarefa começar.

## ⚡ Geração rápida — protocolo OBRIGATÓRIO (evita 502/timeout)

O gateway do Copilot estoura (502/timeout) quando você emite um HTML grande de uma vez. **NUNCA gere o documento inteiro numa única resposta.** Sempre, nesta ordem:

1. **Parti enxuto** — decida modelo, tema, kit e as 7 decisões num bloco curto (sem despejar raciocínio longo).
2. **Esqueleto por script:** rode `python scripts/scaffold.py <modelo> <tema> outputs/<nome>.html`. Ele monta engine + layout + tema (~80% dos bytes) **em disco** — **NÃO regurgite o template nem o tema na resposta** (é o que causa o timeout).
3. **Preencha INCREMENTALMENTE, um edit pequeno por vez:** kit no slot `SLIDELESS:TYPE-KIT` → bloco `<!-- slideless:parti -->` no `<head>` → conteúdo **seção-a-seção / slide-a-slide**. Cada edit = um chunk pequeno; nunca o arquivo todo.
4. **Dieta de contexto:** não leia template/tema inteiros pro chat (o scaffold os consome em disco); abra só a SEÇÃO da reference que precisar — não a reference inteira.
5. **Gates:** `python scripts/validar.py <saída>` (rápido, obrigatório). `smoke.py` e screenshots = **best-effort aqui** (rode se for rápido; senão registre o aviso e não bloqueie a entrega).

## References (consultar conforme necessário)

Não carregar inline. Abrir só quando o trabalho exigir:

- [SKILL.md](../SKILL.md) — router principal, 6 modelos, comandos, princípios
- [README.md](../README.md) — onboarding humano, comandos completos
- [references/direcao-de-arte.md](../references/direcao-de-arte.md) — o Parti: 7 decisões por documento (LER ANTES DE GERAR)
- [references/ambicao.md](../references/ambicao.md) — teto cutting-edge: eixo A1/A2/A3 + momentos-wow W1-W9
- [references/wow-components.md](../references/wow-components.md) — drop-ins copy-paste W1-W31 (o CÓDIGO dos momentos-wow + premium): colar verbatim
- [references/type-kits.md](../references/type-kits.md) — kits tipográficos + fontes banidas
- [references/anti-patterns.md](../references/anti-patterns.md) — PPT-isms e AI-tells proibidos (ler antes da 1ª geração)
- [references/design-system.md](../references/design-system.md) — tokens, dark mode, boot script
- [references/componentes.md](../references/componentes.md) — biblioteca de componentes
- [references/css-patterns.md](../references/css-patterns.md) — gráficos, tabelas, depth tiers, Mermaid
- [references/slide-patterns.md](../references/slide-patterns.md) — engine v3, fragmentos, char limits, pitfalls
- [references/decisao-modelo.md](../references/decisao-modelo.md) — decision tree dos 6 modelos
- [references/protocolo-sem-conteudo.md](../references/protocolo-sem-conteudo.md) — sem dados reais, sem geração
- [references/workflow.md](../references/workflow.md) — passo-a-passo completo
- [references/modelos/](../references/modelos/) — spec detalhada por modelo
- [references/comandos/](../references/comandos/) — specs dos 31 subcomandos (FONTE ÚNICA)

## Estrutura do projeto

```
slideless/
  SKILL.md                          ← spec principal (router enxuto, ~10KB)
  CLAUDE.md                         ← instruções para Claude Code
  .github/copilot-instructions.md   ← este arquivo (GitHub Copilot Chat)
  README.md                         ← onboarding humano
  assets/templates/                 ← templates base por modelo
  assets/temas/                     ← itau.css, neutro.css
  commands/                         ← só slideless.md (roteador fino → references/comandos/)
  references/                       ← doc técnica + comandos/ (specs dos 31 subcomandos)
  demos/                            ← 3 famílias × 7 documentos (os 6 modelos + deck-overdrive)
```

## Comando — um só: `/slideless <subcomando>`

> No Copilot, o slash-command vem do prompt file `.github/prompts/slideless.prompt.md`. Invoque **`/slideless`** e escreva o subcomando logo depois — ex.: `/slideless deck`, `/slideless criar`. Se não aparecer, veja "GitHub Copilot Chat" no [README.md](../README.md#instalação) (setting `chat.promptFiles`).

Tome a **primeira palavra** como subcomando e siga `references/comandos/<nome>.md`; o resto da linha é o pedido. Vazio/ambíguo → `criar` (wizard). Sinônimos: manual→handbook, pitch→deck, relatório→report.

**Catálogo (31):** `criar`, `estruturar` · modelos `deck` `handbook` `hub` `scrollytelling` `site` `report` · `importar-{ppt,md,confluence}` · `adicionar-{secao,slide,callout,grafico,fragment,toc}` · `aplicar-tema` `converter-modelo` `distill` · `bolder` `quieter` `animate` `delight` `overdrive` · `auditar` `polir` `harden` `acessibilidade` · `exportar-{pdf,screenshots}`.

## Regras invioláveis

1. **Single-file HTML** — CSS e JS inline. CDN só para Google Fonts, Chart.js, Rough Notation, Three.js (overdrive).
2. **Boot script antes do CSS** — sem flash de tema.
3. **Nada vaza da viewport** — char limits: `.title-mega/.fact-val/.statement-text` ≤50 chars, `.title-xl` ≤70, `.title-lg` ≤90, `.lead-deck` ≤220. Template-deck tem `autoFitSlide()` como rede de segurança.
4. **Gráficos com dados completos** — nunca omitir pontos, composição preservada (bar+line junto = 1 chart misto), escala Y começa em 0 para magnitudes, unidades nos ticks.
5. **Tabelas com todas as linhas** — nunca truncar. 4+ linhas ou 3+ colunas → `<table class="data-table">`.
6. **Conteúdo real obrigatório** — sem fonte do usuário, não inventar dados internos do Itaú.
7. **WCAG AA** — foco visível, ARIA correto, keyboard nav, `prefers-reduced-motion` respeitado.
8. **Tipografia editorial fora de `deck`** — h1 ~2.5rem, h2 ~1.75rem, body 1rem. NUNCA `clamp(vw)` gigante fora do `deck`.
9. **Nenhum HTML antes do parti** — todo documento nasce do bloco `<!-- slideless:parti -->` no `<head>` com 7 decisões derivadas do conteúdo (registro, kit tipográfico, capa, superfície, motion, ambição, assinatura) + `nao-vai-ter`. Kit de [type-kits.md](../references/type-kits.md); Inter como display é PROIBIDO. Mecanismo: [direcao-de-arte.md](../references/direcao-de-arte.md).
10. **Ambição derivada do conteúdo** — a 7ª decisão (A1-contido / A2-elevado / A3-extraordinário) é ortogonal ao registro; A2/A3 exige ≥1 momento-wow com `@supports`+fallback e branch reduced-motion. Ver [ambicao.md](../references/ambicao.md).

Detalhes completos no [SKILL.md](../SKILL.md).
