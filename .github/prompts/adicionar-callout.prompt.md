---
mode: agent
description: Insere callout (info/tip/warn/danger) em um documento slideless
---
Você está executando o comando **/adicionar-callout** da skill **slideless** (Itaú — substitui PowerPoint por documentos web HTML single-file).

Leia e siga À RISCA, nesta ordem:
- **Este comando:** [commands/adicionar-callout.md](../../commands/adicionar-callout.md)
- **Router, modelos e princípios:** [SKILL.md](../../SKILL.md)
- As regras sempre-ativas já vêm de `.github/copilot-instructions.md`.

**Gate obrigatório antes de entregar qualquer HTML:** `python scripts/validar.py <arquivo>` (0 erros) **e** `python scripts/smoke.py <arquivo>` (SMOKE PASS). Nunca entregar com FAIL.

O pedido/conteúdo do usuário está na conversa.
