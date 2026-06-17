---
mode: agent
description: Converte PPT/PPTX em handbook OU deck — sempre perguntar qual antes de gerar
---
Você está executando o comando **/importar-ppt** da skill **slideless** (Itaú — substitui PowerPoint por documentos web HTML single-file).

Leia e siga À RISCA, nesta ordem:
- **Este comando:** [commands/importar-ppt.md](../../commands/importar-ppt.md)
- **Router, modelos e princípios:** [SKILL.md](../../SKILL.md)
- As regras sempre-ativas já vêm de `.github/copilot-instructions.md`.

**Gate obrigatório antes de entregar qualquer HTML:** `python scripts/validar.py <arquivo>` (0 erros) **e** `python scripts/smoke.py <arquivo>` (SMOKE PASS). Nunca entregar com FAIL.

O pedido/conteúdo do usuário está na conversa.
