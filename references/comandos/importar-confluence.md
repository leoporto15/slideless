---
description: Converte página ou espaço Confluence em modelo slideless apropriado
argument-hint: <url ou caminho de export .html/.pdf>
---

Você foi invocado para converter Confluence em slideless.

## Pré-requisitos

1. Ler [../references/importar-conteudo.md](../importar-conteudo.md#confluence--handbook-default--hub).

## Procedimento

1. **Acesso:** se URL exigir autenticação, NÃO tentar fetch direto. Pedir export `.html` ou `.pdf` do Confluence ou texto colado.
2. **Triagem:**
   - Página única → [slideless-handbook](handbook.md) por default.
   - Espaço com várias páginas → [slideless-hub](hub.md) (cards) ou [slideless-site](site.md) (views) — perguntar.
3. **Conversão de macros:**
   - `info` / `note` / `warning` / `tip` → `.callout--info` / `.callout--info` / `.callout--warn` / `.callout--tip`
   - `expand` → `<details class="toggle">`
   - `code` → `.code` com botão copiar
   - `panel` colorido → callout ou seção com `--color-bg-elevated`
   - `table` → `<table>` (estilo neutro via tokens)
   - `children` macro → pedir ao usuário se vira card grid (hub) ou link list (sidebar handbook)
4. Sidebar do handbook: gerada dos h1-h3 da página Confluence (ou estrutura de páginas no espaço).
5. Validar e entregar.

## Gate de render antes de entregar (v7 — obrigatório)
A edição/importação mexe no render — além do `validar.py`, rodar o smoke e corrigir a CAUSA:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Anti-patterns críticos

- Importar slide-por-slide com bullets rasos → reescrever em parágrafos editoriais.
- Manter macros não-traduzidas no HTML final → tudo vira componente slideless.
