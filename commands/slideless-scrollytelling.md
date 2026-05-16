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

1. Copiar [../assets/templates/template-scrollytelling.html](../assets/templates/template-scrollytelling.html).
2. Aplicar tema.
3. Popular cenas (`.scene` com `data-reveal`) na ordem narrativa.
4. Se houver sticky chart:
   - Adicionar `<div class="story">` com `.story__text` (cenas) e `.story__chart` (canvas Chart.js).
   - Adicionar `data-step="N"` em cada `.scene` que muda o chart.
   - Implementar IntersectionObserver de step (ver [../references/modelos/scrollytelling.md](../references/modelos/scrollytelling.md)).
5. Counters animados em cenas de métricas (ver [../references/componentes.md](../references/componentes.md#counters-animados)).
6. Validar e entregar em `/mnt/user-data/outputs/scrollytelling-<slug>.html`.

## Anti-patterns críticos

- Botões "próximo" → scroll é o controle único.
- Reveal por setTimeout em vez de IntersectionObserver.
- Tipografia hero gigante → editorial; lead pode chegar a 1.3rem mas h1 fica em ~2.5rem.
