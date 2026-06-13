# demos/

Showcases pareados: **o mesmo motor aplicado a 3 assuntos diferentes**, cada um nos 6 modelos (com o `deck` em duas variantes — normal e overdrive —, 7 documentos por família). Servem de prova viva de que a skill **não pasteuriza** — cobrindo o logo, os três conjuntos são visualmente distinguíveis entre si (kit tipográfico, capa, superfície e materialidade derivados do conteúdo).

Diferente de `assets/exemplos/` (1 showcase canônico por modelo, cada um com um kit distinto), aqui cada pasta é uma **família** com identidade própria declarada no bloco `<!-- slideless:parti -->`.

## Estrutura

```
demos/
├── itau-1T26-institucional/     ← resultados trimestrais (RI)  · Kit 01 Broadsheet, registro relatorio-de-bancada
├── itau-asset-institucional/    ← gestora de ativos          · Kit 02 Relatório Anual, registro institucional-impresso
└── itau-trump2-comercio/        ← análise macro de comércio  · Kit 05 Poster, registro condensado-noticioso
```

Cada família traz 7 documentos — os 6 modelos, com o `deck` em duas variantes (normal e overdrive A3): `deck.html`, `deck-overdrive.html`, `handbook.html`, `hub.html`, `report.html`, `scrollytelling.html`, `site.html`.

## O que demonstram

- **Anti-pasteurização** — as 3 famílias têm kits, capas e superfícies distintos. O `report` de cada uma é sóbrio (A1-contido); os demais sobem a A2-elevado; o `deck-overdrive` é A3.
- **Direção de arte por documento** — cada família declara seu `parti` (7 decisões + nao-vai-ter) no `<head>`; rode `python scripts/validar.py --stats demos/<familia>` para ver a distribuição de decisões.
- **Ambição com fallback** — momentos-wow (manchete cinética, View Transitions, scroll-driven, anotação viva nos gráficos) degradam graciosamente fora do Chrome evergreen.
- **Conteúdo preservado** — dados são fictícios/aproximados (placeholders explícitos), mas a densidade é real: tabelas completas, gráficos com todos os pontos.

## Validar

```bash
python scripts/validar.py demos/itau-1T26-institucional/deck.html
python scripts/validar.py --stats demos/itau-trump2-comercio   # distribuição de decisões do parti
```
