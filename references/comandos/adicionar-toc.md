---
description: Regenera TOC sticky a partir dos h2/h3 do conteúdo (handbook)
---

Você foi invocado para regenerar a TOC sticky (only handbook).

## Procedimento

1. Verificar que o arquivo é handbook (`.layout` com `.sidebar` + `.toc`).
2. A TOC já é gerada dinamicamente pelo JS do template: ele lê `document.querySelectorAll('.content h2[id]')` e popula `#toc-list`.
3. Se o usuário pediu este comando, provavelmente:
   - O JS de TOC sumiu (provável regressão em edição manual) → restaurar conforme [../assets/templates/template-handbook.html](../../assets/templates/template-handbook.html).
   - Ou quer mostrar h3 também → ampliar para `'.content h2[id], .content h3[id]'` com indentação visual no CSS.
4. Conferir:
   - Todo h2 dentro de `.content` tem `id`.
   - `<aside class="toc">` existe com `<ul class="toc__list" id="toc-list">`.
   - Scrollspy compartilhada com a sidebar funciona (mesma IntersectionObserver).
5. Validar.

## Gate de render antes de entregar (v7 — obrigatório)
A edição/importação mexe no render — além do `validar.py`, rodar o smoke e corrigir a CAUSA:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Para mostrar h3 também

Alterar o trecho de geração:
```js
document.querySelectorAll('.content h2[id], .content h3[id]').forEach(h => {
  const li = document.createElement('li');
  li.className = h.tagName === 'H3' ? 'toc__sub' : '';
  const a = document.createElement('a');
  a.href = '#' + h.id;
  a.textContent = h.textContent;
  li.appendChild(a);
  document.getElementById('toc-list').appendChild(li);
});
```
E CSS: `.toc__sub a { padding-left: var(--space-5); font-size: var(--size-xs); }`.
