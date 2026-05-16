---
description: Audita documento slideless contra validador determinístico + checklist + anti-patterns
argument-hint: <caminho do arquivo>
---

Você foi invocado para auditar um documento slideless.

## Procedimento

1. **Validador determinístico:**
   ```bash
   python scripts/validar.py <arquivo.html>
   ```
   Capturar saída. Cada linha numerada é uma violação a corrigir.
2. **Checklist de revisão LLM** ([../references/checklist-revisao.md](../references/checklist-revisao.md)):
   - Bloqueantes (🚫) — corrigir antes de entregar
   - Alto (⚠️)
   - Médio (🟡)
   - Sugestões (💡)
3. **Anti-patterns** ([../references/anti-patterns.md](../references/anti-patterns.md)):
   - A1-A8 — visuais (PPT-isms)
   - B1-B8 — técnicos
   - C1-C4 — conteúdo
   - D — específicos por modelo
4. Compilar relatório priorizado.

## Formato de saída

```
🚫 BLOQUEANTES (N)
  1. [linha 12] Boot script ausente no <head> antes do CSS — ver design-system.md
  2. ...

⚠️ ALTO (N)
  1. ...

🟡 MÉDIO (N)
  ...

💡 SUGESTÕES (N)
  ...

Resumo: documento PRECISA / NÃO PRECISA de correção antes de entregar.
```

## Não fazer

- Não auto-corrigir. Apenas relatar. O usuário decide o que corrigir.
- Se o usuário pediu correção junto, sugerir comandos específicos (`/polir`, `/harden`).
- Não inventar problemas — só apontar violações reais com referência ao critério.
