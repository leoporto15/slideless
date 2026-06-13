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

0. **Parti (obrigatório, antes de qualquer HTML)** — [../references/direcao-de-arte.md](../references/direcao-de-arte.md): 7 decisões + `nao-vai-ter` derivadas do CONTEÚDO do pitch (capa/kit/superfície ≠ [exemplo-deck](../assets/exemplos/exemplo-deck.html) e ≠ último deck da pasta), bloco no `<head>`. A 7ª decisão é `ambicao` ([../references/ambicao.md](../references/ambicao.md)) — **default A2-elevado** para deck; se A2/A3, o campo `momento-wow` (W1-W9 ligado ao dado-tese) é **obrigatório**. A3 só com conteúdo à altura (lançamento/all-hands).
1. Copiar [../assets/templates/template-deck.html](../assets/templates/template-deck.html).
2. Aplicar tema e preencher o slot `SLIDELESS:TYPE-KIT` com o kit do parti ([../references/type-kits.md](../references/type-kits.md)). PROIBIDO Inter como display.
3. Para cada slide do roteiro, escolher layout em [../references/modelos/deck.md](../references/modelos/deck.md#layouts-de-slide) e **compor**.
4. **Regra de ritmo (anti-pasteurização):** a cada bloco de 4-5 slides, ≥1 slide abandona o esqueleto kicker→título→corpo (número 20vw, tabela full-bleed, quote sem chrome, diagrama SVG). Kicker em ≤50% dos slides; `<em>` accent em ≤25% dos títulos; cards em ≤1/3 dos slides; ≥1 slide com assimetria real (2fr/1fr ou elemento sangrando a margem).
5. Motion conforme o perfil do parti (cinemático: até 3 gestos POR PAPEL; quote entra seca). `data-anim`/`data-fragment` para reveals sequenciais; stagger só em grupo homogêneo.
6. **Re-ancoragem anti-drift:** a cada ~5 slides, reler o parti — o modo de falha real é os slides finais regredirem ao grid de cards default.
7. Keyboard nav já está no template — não duplicar nem remover. Indicador de slide (`id="cur"`, `id="tot"`) presente.
8. Validar (categoria P) + checklist (bloco 🎨) + gate perceptual se disponível. Entregar em `outputs/deck-<slug>.html` e reportar o parti em 1 linha.

## Anti-patterns críticos

- Transição > 800ms → cansa apresentador.
- Esquecer keyboard handler → não navega no palco.
- Fragments todos visíveis ao entrar no slide → defeito da animação.
- Tipografia fixa em px gigantes → use `clamp()` sempre, fluido com viewport.
