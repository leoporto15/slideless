---
description: Varredura isolada de acessibilidade — relatório + correções WCAG AA
argument-hint: <caminho do arquivo>
---

Você foi invocado para uma varredura focada de a11y.

## Diferença vs `/slideless harden`

| `/slideless acessibilidade` | `/slideless harden` |
|---|---|
| Varredura + relatório priorizado, depois aplica correções com confirmação | Aplica tudo direto (sem listar) |
| Útil em revisão final / publicação externa | Útil durante geração inicial |

## Procedimento

1. Análise (não modifica arquivo):
   - Foco visível em todos os interativos
   - Landmarks ARIA
   - `aria-label` em botões sem texto
   - Roles em tabs, callout danger, charts
   - Keyboard nav funcional
   - Contraste de tokens
   - `prefers-reduced-motion`
   - `lang="pt-BR"`
   - `<img alt>` descritivo
   - Headings sem skip de nível
2. **Relatório:**
   ```
   [Bloqueante / Alto / Médio / Sugestão]
   Linha N: <descrição> — WCAG <ref>
   ```
3. Perguntar ao usuário se aplica correções todas / só bloqueantes / nenhuma.
4. Aplicar conforme escolha.
5. Re-rodar varredura.

## Gate de render antes de entregar (v7 — obrigatório)
O passe de qualidade mexe no render — além do `validar.py`, rodar:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
O smoke também confere que `prefers-reduced-motion` não deixa conteúdo invisível (estado-final-base presente) e que nada vaza nem colapsa após as correções de a11y. Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Referência

- WCAG 2.1 AA: https://www.w3.org/TR/WCAG21/
- Itens cobertos: 1.3.1 (info+relations), 1.4.3 (contrast), 2.1.1 (keyboard), 2.4.7 (focus visible), 4.1.2 (name/role/value)
