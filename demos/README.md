# demos/

Pares **input → output** reais. Diferente de `assets/exemplos/` (showcases fictícios da skill), aqui ficam transcrições de uso real (anonimizadas se necessário).

## Estrutura sugerida

```
demos/
└── <slug-do-caso>/
    ├── input.md          ou input.pptx, input.txt — o material original
    ├── prompt-usado.md   ← o que o usuário pediu (exato ou parafraseado)
    ├── output.html       ← o HTML slideless gerado
    └── notas.md          ← (opcional) o que foi reescrito, decisões tomadas
```

## Por que ter demos reais

- Mostrar para terceiros como a skill se comporta na prática (não apenas via showcase fictício).
- Capturar decisões editoriais não-óbvias (e.g., "este PPT virou handbook em vez de deck porque…").
- Servir de prova quando alguém perguntar "mas funciona em contexto real?".

## Demos pendentes (sugestões)

- `onboarding-pessoa-dados/` — MD → handbook
- `relatorio-anual-2025/` — narrativa Confluence → scrollytelling
- `pitch-q4-comite/` — PPT → deck
- `central-recursos-engenharia/` — set de páginas Confluence → hub
- `microsite-time-x/` — descrição livre → site

## Anonimização

Antes de commitar uma demo:
1. Substituir nomes de pessoas, times, gerências, produtos sigilosos por placeholders genéricos.
2. Mascarar números sensíveis (NPS, headcount, custos).
3. Confirmar com o autor original que o material pode virar demo.
