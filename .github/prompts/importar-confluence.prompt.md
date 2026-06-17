---
mode: agent
description: Converte página ou espaço Confluence em modelo slideless apropriado
---
Você está executando o comando **/importar-confluence** da skill **slideless** (Itaú — substitui PowerPoint por documentos web HTML single-file).

Leia e siga À RISCA, nesta ordem:
- **Este comando:** [commands/importar-confluence.md](../../commands/importar-confluence.md)
- **Router, modelos e princípios:** [SKILL.md](../../SKILL.md)
- As regras sempre-ativas já vêm de `.github/copilot-instructions.md`.

**Gate obrigatório antes de entregar qualquer HTML:** `python scripts/validar.py <arquivo>` (0 erros) **e** `python scripts/smoke.py <arquivo>` (SMOKE PASS). Nunca entregar com FAIL.

O pedido/conteúdo do usuário está na conversa.
