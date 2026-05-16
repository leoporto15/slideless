---
description: Varredura isolada de acessibilidade — relatório + correções WCAG AA
argument-hint: <caminho do arquivo>
---

Você foi invocado para uma varredura focada de a11y.

## Diferença vs `/harden`

| `/acessibilidade` | `/harden` |
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

## Referência

- WCAG 2.1 AA: https://www.w3.org/TR/WCAG21/
- Itens cobertos: 1.3.1 (info+relations), 1.4.3 (contrast), 2.1.1 (keyboard), 2.4.7 (focus visible), 4.1.2 (name/role/value)
