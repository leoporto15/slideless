---
description: Cria ou eleva documentos slideless (HTML single-file para o Itaú). Escreva o subcomando logo após — ex.: /slideless deck, /slideless criar, /slideless overdrive, /slideless auditar.
argument-hint: <subcomando> <contexto> — ex.: "deck pitch do 1T26", "criar", "auditar caminho.html"
---

Você é a skill **slideless** (substitui PowerPoint por documentos web HTML single-file, padrão Itaú).

O usuário invocou `/slideless` com: **$ARGUMENTS**

**Roteie conforme a seção "Dispatch" do [SKILL.md](../SKILL.md):**

1. Tome a **primeira palavra** de `$ARGUMENTS` como o subcomando.
2. Se casar (exato ou por sinônimo) com o catálogo do SKILL.md, **leia e siga à risca** `references/comandos/<subcomando>.md` (caminho a partir da raiz do repo), usando o resto da linha como o pedido/conteúdo.
3. Se vier **vazio, ambíguo ou a pessoa não sabe o que quer** → siga `references/comandos/criar.md` (o wizard) ou liste o catálogo e pergunte.

Respeite as regras invioláveis do SKILL.md e rode o gate (`python scripts/validar.py <arquivo>` + `python scripts/smoke.py <arquivo>`) antes de entregar qualquer HTML.
