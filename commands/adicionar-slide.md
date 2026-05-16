---
description: Adiciona um slide ao deck (hero, big-num, metrics, list, quote, two-col, divider, timeline-h, cards-3up)
argument-hint: <tipo> [após-slide-N]
---

Você foi invocado para adicionar slide ao deck.

## Tipos disponíveis

Ver [../references/modelos/deck.md](../references/modelos/deck.md#layouts-de-slide) para HTML completo de cada um:

- `hero` — kicker + title-xl + lead + meta
- `divider` — number + title-lg (separador entre capítulos)
- `big-num` — métrica grande única
- `metrics` — 3 métricas em colunas
- `list` — lista 3-5 itens numerados com fragments
- `two-col` — texto + visual lado a lado
- `quote` — citação grande
- `timeline-h` — timeline horizontal (4 colunas)
- `cards-3up` — 3 cards lado a lado
- `encerramento` — obrigado + contato

## Procedimento

1. Inserir `<section class="slide" data-slide="<N>">…</section>` no `.deck`, na posição indicada.
2. Renumerar `data-slide` dos slides seguintes (se relevante; o JS usa o índice no array, então renumerar é cosmético mas mantém consistência).
3. O contador X / Y do HUD atualiza sozinho (template lê `slides.length`).
4. Se o slide tem fragments, marcar com `data-fragment`. Stagger via `data-anim` + `--anim-i: N`.
5. Hash `#sN` continua válido se a posição mudou (avisar o usuário se houver links externos para slides específicos).
6. Validar.

## Anti-patterns críticos

- Slide com texto editorial denso (parágrafos longos) → vira "PPT com texto demais". Slide é uma frase ou bullet curto.
- Animação > 800ms.
- `font-size: 96px` fixo → use `clamp()`.
