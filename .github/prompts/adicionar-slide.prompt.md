---
mode: agent
description: Adiciona um slide ao deck (hero, big-num, metrics, list, quote, two-col, divider, timeline-h, cards-3up)
---
Você está executando o comando **/adicionar-slide** da skill **slideless** (Itaú — substitui PowerPoint por documentos web HTML single-file).

Leia e siga À RISCA, nesta ordem:
- **Este comando:** [commands/adicionar-slide.md](../../commands/adicionar-slide.md)
- **Router, modelos e princípios:** [SKILL.md](../../SKILL.md)
- As regras sempre-ativas já vêm de `.github/copilot-instructions.md`.

**Gate obrigatório antes de entregar qualquer HTML:** `python scripts/validar.py <arquivo>` (0 erros) **e** `python scripts/smoke.py <arquivo>` (SMOKE PASS). Nunca entregar com FAIL.

O pedido/conteúdo do usuário está na conversa.
