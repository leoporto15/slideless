---
mode: agent
description: Gera 1 PNG por slide (deck) ou por seção (demais modelos) para preview rápido
---
Você está executando o comando **/exportar-screenshots** da skill **slideless** (Itaú — substitui PowerPoint por documentos web HTML single-file).

Leia e siga À RISCA, nesta ordem:
- **Este comando:** [commands/exportar-screenshots.md](../../commands/exportar-screenshots.md)
- **Router, modelos e princípios:** [SKILL.md](../../SKILL.md)
- As regras sempre-ativas já vêm de `.github/copilot-instructions.md`.

**Gate obrigatório antes de entregar qualquer HTML:** `python scripts/validar.py <arquivo>` (0 erros) **e** `python scripts/smoke.py <arquivo>` (SMOKE PASS). Nunca entregar com FAIL.

O pedido/conteúdo do usuário está na conversa.
