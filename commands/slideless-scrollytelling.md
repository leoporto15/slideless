---
description: Gera scrollytelling (narrativa única com reveal e progress bar) a partir de conteúdo do usuário
argument-hint: <tópico ou narrativa>
---

Você foi invocado para gerar um documento `scrollytelling` (slideless).

## Pré-requisitos

1. Ler [../references/modelos/scrollytelling.md](../references/modelos/scrollytelling.md).
2. Confirmar com o usuário:
   - **Conteúdo narrativo linear** (não referencial). Se referencial, sugerir [handbook](slideless-handbook.md).
   - **Há sticky chart?** Se sim, peça dados.
   - **Tema** (default `itau`).

## Procedimento

0. **Parti (obrigatório)** — [../references/direcao-de-arte.md](../references/direcao-de-arte.md): 7 decisões + `nao-vai-ter` derivadas do assunto, capa/kit/superfície ≠ exemplo canônico, bloco no `<head>`. A 7ª decisão é `ambicao` ([../references/ambicao.md](../references/ambicao.md)) — **default A2-elevado** para scrollytelling; se A2/A3, o campo `momento-wow` é **obrigatório** (a espinha do modelo é W1 cena scroll-driven + W8 anotação viva no gráfico-tese).
1. Copiar [../assets/templates/template-scrollytelling.html](../assets/templates/template-scrollytelling.html).
2. Slot `SLIDELESS:TYPE-KIT` com o `<link>` do kit + `:root` do kit antes do tema. Aplicar tema (MARCA intacta; DIREÇÃO conforme o parti).
3. **Compor** as cenas na ordem narrativa. Reveal SÓ conforme o perfil de motion (figuras/dados, ≤40% das sections — texto corrido nunca anima).
4. **Coreografia é requisito, não opcional:** se há gráfico sticky, cada `data-step` MUTA o gráfico via `chart.update()` (destacar série, acender anotação, estender range) — nunca trocar o gráfico inteiro nem deixar steps que só fazem fade. Bloco §5.0 de css-patterns.md (Chart.defaults + fmtBR) antes do primeiro chart. Implementar IntersectionObserver de step (ver [../references/modelos/scrollytelling.md](../references/modelos/scrollytelling.md)).
5. Counter animado SÓ no número declarado como momento assinatura no parti — números de apoio entram estáticos.
6. Validar (categoria P) + checklist (bloco 🎨) + gate perceptual se disponível. Entregar em `outputs/scrollytelling-<slug>.html` e reportar o parti em 1 linha.

## Anti-patterns críticos

- Botões "próximo" → scroll é o controle único.
- Reveal por setTimeout em vez de IntersectionObserver.
- Tipografia hero gigante → editorial; lead pode chegar a 1.3rem mas h1 fica em ~2.5rem.
