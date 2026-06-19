---
description: Troca o tema (neutro ↔ itau) de um documento slideless existente
argument-hint: <neutro|itau>
---

Você foi invocado para trocar tema.

## Procedimento

1. Identificar o tema atual: presença de tokens `--itau-orange` em `:root` ⇒ `itau`. Caso contrário, `neutro`.
2. **Não duplicar trabalho:** se o tema-alvo é o atual, avisar e parar.
3. Substituir bloco inteiro de tokens:
   - Bloco `:root { … }` (do primeiro `--itau-orange` ou `--color-bg` até a `}` correspondente).
   - Bloco `[data-theme="dark"] { … }`.
   - Reset/base, callouts, code, toggle, theme-toggle, cards, métricas, timeline — **manter** (são compartilhados, só usam `var(--…)`).
4. Substituir pelo conteúdo do tema-alvo, vindo de [../assets/temas/itau.css](../../assets/temas/itau.css) ou [../assets/temas/neutro.css](../../assets/temas/neutro.css).
5. **Fontes:** trocar tema NÃO troca o kit tipográfico do documento — o kit é decisão de direção de arte ([../references/type-kits.md](../type-kits.md)), independente do tema. Manter o `<link>` do kit existente. Se o documento for legado (Inter como display, sem kit), avisar o usuário e sugerir `/slideless polir` com escolha de kit.
6. **Logo:** se tema = `itau`, manter logo Itaú no topbar; se `neutro`, considerar remover ou substituir.
7. Rodar validador.

## Gate de render antes de entregar (v7 — obrigatório)
A transformação mexe no render — além do `validar.py`, rodar:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Anti-patterns críticos

- Esquecer override de algum `--color-*` em `[data-theme="dark"]` após troca → dark mode quebrado.
- Não trocar fontes ao mudar de `itau` para `neutro` (Itaú Display continua referenciada mesmo sem efeito).

## Migração de documentos antigos (pré-v4)

Os temas v4 NÃO contêm mais `[data-reveal]` nem `.card:hover { translateY }` — motion e affordance são decisões do parti. Ao trocar o tema de um documento antigo que usa `data-reveal` no HTML:
1. Verificar se o documento tem o CSS de reveal próprio inline (documentos antigos têm — não quebram).
2. Se o reveal sumir após a troca, colar o perfil de motion equivalente de [../references/direcao-de-arte.md](../direcao-de-arte.md) (perfil `editorial`) em vez de restaurar o bloco antigo.
