---
description: Converte PPT/PPTX em handbook OU deck — sempre perguntar qual antes de gerar
argument-hint: <caminho do arquivo .pptx>
---

Você foi invocado para converter PPT em slideless.

## Pré-requisitos

1. Ler [../references/importar-conteudo.md](../references/importar-conteudo.md#pptpptx--handbook-ou-deck-perguntar).

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
7. Usar [slideless-deck](slideless-deck.md) como template-base.

## Se virar `handbook` / `scrollytelling`

1. Agrupar slides com mesmo tema em seções (`<h2>`).
2. Reescrever bullets em parágrafos editoriais. Se virar `<ul>` longo, quebrar em sub-seções (h3).
3. Slide "hero / capa" some — substituído por `<h1>` + `<lead>`.
4. Slide "obrigado / dúvidas" some.
5. Imagens viram `<figure>`; gráficos viram Chart.js.

**Aviso ao usuário:** se o PPT vier muito raso (só bullets), avisar que o handbook resultante vai precisar de mais texto. Não tentar inflar artificialmente.

## Anti-patterns críticos

- "Traduzir slide-por-slide" em handbook → vira handbook ruim. Reescrever.
- Manter números sigilosos do PPT em documento que pode ser distribuído mais amplamente.
