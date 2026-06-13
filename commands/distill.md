---
description: Reduz um handbook longo a sumário enxuto preservando hierarquia
argument-hint: <caminho do handbook> [tamanho-alvo]
---

Você foi invocado para destilar um documento slideless longo.

## Quando usar

- Handbook de 80+ páginas precisa de uma versão "TL;DR" de 1-page.
- Onboarding longo precisa de resumo executivo.
- Convertendo material denso em formato apresentável.

## Procedimento

1. Carregar o documento. Confirmar que é handbook (ou scrollytelling).
2. Preservar:
   - `<h1>` + lead original (ou versão encurtada).
   - Todos os `<h2>` (estrutura mantém).
   - Primeiro parágrafo de cada seção (resumo) ou TL;DR explícita.
   - Callouts `warn` e `danger` (críticos não somem).
   - Métricas-chave e charts.
3. Remover:
   - Sub-seções `<h3>` (a menos que sejam críticas).
   - Code blocks longos → substituir por callout "Detalhes técnicos no doc completo".
   - Parágrafos de exemplo/elaboração.
   - Toggles `<details>`.
   - Tabelas grandes (resumir em prosa).
4. Adicionar callout `info` no topo:
   > Versão resumida. Para o documento completo, ver: [link]
5. Salvar como `outputs/<nome>-resumo.html` (não sobrescrever original).
6. Validar.

## Tamanho-alvo

Se o usuário especificou ("metade", "1 página", "3000 palavras"), trabalhar até bater. Se não, default: 25-30% do original em palavras.

## Anti-patterns críticos

- Destilar e perder o tom editorial (virando bullets) → sumário ainda é texto editorial.
- Inventar resumos de seções que você não entendeu → manter texto literal se em dúvida.
