---
description: Gera deck moderno (slide-by-slide com keyboard nav, fragments, fullscreen) — único modelo com tipografia gigante OK
argument-hint: <tópico do pitch>
---

Você foi invocado para gerar um documento `deck` (slideless). Este é o **único** modelo onde tipografia gigante é permitida.

## Pré-requisitos

1. Ler [../references/modelos/deck.md](../references/modelos/deck.md).
2. Confirmar com o usuário:
   - **Apresentação ao vivo?** Se não (vai distribuir como leitura), redirecionar para [scrollytelling](slideless-scrollytelling.md). Não fazer deck "para ler".
   - **Roteiro dos slides** (kicker, hero, big-num, métricas, list, two-col, divider, quote, timeline, encerramento).
   - **Tema** (default `itau`).

## Procedimento

1. Copiar [../assets/templates/template-deck.html](../assets/templates/template-deck.html).
2. Aplicar tema (no `itau` o Inter inclui peso 800 — `family=Inter:wght@400;500;600;700;800`).
3. Para cada slide do roteiro, escolher layout em [../references/modelos/deck.md](../references/modelos/deck.md#layouts-de-slide) e popular.
4. Aplicar `data-anim` com `--anim-i: N` para stagger; `data-fragment` para reveal sequencial.
5. Keyboard nav já está no template — não duplicar nem remover.
6. Indicador de slide (X / Y) atualizado pelo JS — verificar que `id="cur"`, `id="tot"` estão presentes.
7. Validar e entregar em `/mnt/user-data/outputs/deck-<slug>.html`.

## Anti-patterns críticos

- Transição > 800ms → cansa apresentador.
- Esquecer keyboard handler → não navega no palco.
- Fragments todos visíveis ao entrar no slide → defeito da animação.
- Tipografia fixa em px gigantes → use `clamp()` sempre, fluido com viewport.
