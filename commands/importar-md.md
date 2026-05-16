---
description: Converte Markdown estruturado em handbook (default) ou scrollytelling
argument-hint: <caminho do .md ou MD colado>
---

Você foi invocado para converter Markdown em slideless.

## Pré-requisitos

1. Ler [../references/importar-conteudo.md](../references/importar-conteudo.md#markdown--handbook-default--scrollytelling).

## Triagem automática

- `#` 1× = título → vira `<h1>` + extrair próximo parágrafo como `<lead>`.
- `##` ≥ 8 + tom referencial → **handbook** (default).
- `##` < 8 + tom narrativo / dados visualizáveis → propor **scrollytelling** ao usuário antes de gerar.

## Conversões

| MD | HTML |
|---|---|
| `#` | `<h1>` (1 por documento) |
| `##` | `<section data-reveal id="…"><h2>…</h2>` |
| `###` | `<h3>` dentro da seção |
| `- item` (curta lista, ≤ 6) | `<ul><li>` |
| `- item` (lista longa) | considerar quebrar em sub-seções h3 |
| Tabela MD | `<table>` com classes do DS |
| Bloco código `\`\`\`lang` | `.code` com `data-lang="lang"` e botão copiar |
| Imagem `![alt](src)` | `<figure><img alt="alt"><figcaption>` |
| Callout GFM `> [!INFO]` | `.callout--info` (idem TIP/WARN/DANGER) |
| Link `[a](url)` | `<a href>` (mantém) |

## Procedimento

1. Identificar tipo (handbook/scrollytelling) ou perguntar.
2. Chamar [slideless-handbook](slideless-handbook.md) ou [slideless-scrollytelling](slideless-scrollytelling.md) com o conteúdo já populado.
3. Sidebar (handbook): um link por `##`. Agrupar com `<h2>` adicionais se houver demais.
4. TOC: gerada dinamicamente.

## Anti-patterns críticos

- Manter MD blocks "como vieram" sem virar componentes slideless.
- Listas de 12 itens viradas em `<ul>` direto → quebrar em sub-seções.
