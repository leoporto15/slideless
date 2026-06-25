---
description: Converte PPT/PPTX em handbook OU deck — sempre perguntar qual antes de gerar
argument-hint: <caminho do arquivo .pptx>
---

Você foi invocado para converter PPT em slideless.

## Pré-requisitos

1. Ler [../references/importar-conteudo.md](../importar-conteudo.md#pptpptx--handbook-ou-deck-perguntar).

## PERGUNTA OBRIGATÓRIA antes de gerar

> Esse PPT é para você apresentar ao vivo, ou para distribuir como leitura?
> - **Apresentar ao vivo** → converto em `deck` (mantém formato slide).
> - **Distribuir para leitura** → converto em `handbook` ou `scrollytelling` (reorganiza em documento web).

Não chutar. Resposta determina TODO o resto.

## Se virar `deck`

1. Cada slide PPT → 1 `<section class="slide">`.
2. Título do slide → `.title-md` ou `.title-lg` (não tudo em `.title-xl` — reservar para o hero).
3. Bullets → `.list` com `data-fragment` (revelam ao clicar).
4. Imagens centradas → `.two-col__visual` ou centralizadas no slide.
5. Gráficos → recriar com Chart.js. **Pedir confirmação dos números** se vierem do PPT (pode ter dados sigilosos ou desatualizados).
6. Slides "agenda" / "obrigado" / "perguntas" — gerar explicitamente.
7. Gerar via `/slideless deck` ([deck.md](deck.md)) — que monta o esqueleto por `scaffold.py` e preenche incremental (não regurgitar template/tema).

## Se virar `handbook` / `scrollytelling`

1. Agrupar slides com mesmo tema em seções (`<h2>`).
2. Reescrever bullets em parágrafos editoriais. Se virar `<ul>` longo, quebrar em sub-seções (h3).
3. Slide "hero / capa" some — substituído por `<h1>` + `<lead>`.
4. Slide "obrigado / dúvidas" some.
5. Imagens viram `<figure>`; gráficos viram Chart.js.

**Aviso ao usuário:** se o PPT vier muito raso (só bullets), avisar que o handbook resultante vai precisar de mais texto. Não tentar inflar artificialmente.

## Gate de render antes de entregar (v7 — obrigatório)
A edição/importação mexe no render — além do `validar.py`, rodar o smoke e corrigir a CAUSA:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Anti-patterns críticos

- "Traduzir slide-por-slide" em handbook → vira handbook ruim. Reescrever.
- Manter números sigilosos do PPT em documento que pode ser distribuído mais amplamente.
