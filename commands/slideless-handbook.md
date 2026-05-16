---
description: Gera handbook (manual com sidebar + scrollspy + TOC) a partir de conteúdo do usuário
argument-hint: <tópico ou caminho do MD/PPT>
---

Você foi invocado para gerar um documento `handbook` (slideless).

## Pré-requisitos

1. Ler [../references/anti-patterns.md](../references/anti-patterns.md) e [../references/design-system.md](../references/design-system.md) se ainda não leu nesta sessão.
2. Confirmar com o usuário:
   - **Conteúdo real** — sem ele, aplicar [../references/protocolo-sem-conteudo.md](../references/protocolo-sem-conteudo.md). Não inventar.
   - **Tema** (`itau` ou `neutro`; default `itau`).
   - **Escopo** — quantas seções aproximadamente.

## Procedimento

1. Copiar [../assets/templates/template-handbook.html](../assets/templates/template-handbook.html) como base.
2. Substituir `/* SLIDELESS:THEME */` pelo conteúdo de [../assets/temas/itau.css](../assets/temas/itau.css) ou [../assets/temas/neutro.css](../assets/temas/neutro.css).
3. Popular conforme [../references/modelos/handbook.md](../references/modelos/handbook.md) e [../references/componentes.md](../references/componentes.md).
4. Sidebar: um link por `<h2>`. Agrupar por `.sidebar__heading` se fizer sentido.
5. TOC: já é gerada dinamicamente do conteúdo (não tocar no JS).
6. Aplicar `data-reveal` em cada `<section>` (não em parágrafos individuais).
7. Rodar `python ../scripts/validar.py <output.html>`.
8. Aplicar [../references/checklist-revisao.md](../references/checklist-revisao.md) mentalmente.
9. Salvar em `/mnt/user-data/outputs/handbook-<slug>.html`.

## Anti-patterns críticos

- Tipografia gigante (h1 ≥ 4rem) → handbook é editorial, h1 2.5rem.
- Hero gigante na primeira tela → `<h1>` + `<p class="lead">` e começa a entregar conteúdo na primeira rolagem.
- Bullet point overload → `<ul>` com 8+ itens, considerar quebrar em h3.

Ver [../references/anti-patterns.md](../references/anti-patterns.md) seção A.
