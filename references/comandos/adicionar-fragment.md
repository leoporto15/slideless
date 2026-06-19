---
description: Marca elementos do slide ativo como fragments (revelam por click no deck)
argument-hint: <slide-N> <seletor>
---

Você foi invocado para adicionar fragments a slide do deck.

## Pré-requisito

Só faz sentido em modelo `deck`.

## Procedimento

1. Localizar o slide alvo: `<section class="slide" data-slide="<N>">`.
2. Adicionar atributo `data-fragment` nos elementos a revelar:
   ```html
   <li class="list__item" data-fragment>…</li>
   ```
3. Ordem dos fragments = ordem no DOM (não é controlada por número).
4. Cada `data-fragment` ganha CSS já presente no template (`opacity: 0; transform: translateY(12px); transition: …`).
5. Para fragments aparecerem em grupo, agrupe-os num wrapper:
   ```html
   <div data-fragment>
     <p>Linha 1</p>
     <p>Linha 2</p>
   </div>
   ```
6. JS já trata: `next()` revela o próximo fragment do slide ativo antes de avançar para o próximo slide. Não duplicar lógica.

## Gate de render antes de entregar (v7 — obrigatório)
A edição/importação mexe no render — além do `validar.py`, rodar o smoke e corrigir a CAUSA:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Anti-patterns críticos

- Marcar 10 fragments num slide → cansativo. Máximo 4-5 por slide.
- Esquecer que reduced-motion vai mostrar tudo de uma vez — não dependa do fragment para esconder informação crítica.
