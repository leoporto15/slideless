---
description: Gera 1 PNG por slide (deck) ou por seção (demais modelos) para preview rápido
argument-hint: <caminho do .html>
---

Você foi invocado para exportar screenshots.

## Procedimento

1. Identificar o modelo.
2. Rodar o script:
   ```bash
   python ../scripts/exportar_pdf.py <arquivo.html> --mode screenshots --output /mnt/user-data/outputs/<nome>/
   ```
3. **deck:** 1 PNG por slide. Nome: `s01.png`, `s02.png`, …, em viewport 1920x1080.
4. **handbook/scrollytelling/site/hub:** 1 PNG por `<h2>` ou view. Capturas full-page de viewport 1440x900, com scroll até cada h2 e ajuste da viewport para abranger a seção (pode resultar em PNGs altos).
5. Entregar como zip ou listar caminhos.

## Quando usar

- Preview rápido para revisão visual sem abrir o HTML.
- Anexar em e-mail / Slack como prévia.
- Comparação A/B entre dois temas.

## Anti-patterns críticos

- Tirar screenshot de deck em viewport mobile → deck é desktop-first (use 1920x1080).
