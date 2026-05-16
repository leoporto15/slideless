---
description: Renderiza documento slideless para PDF (deck → landscape; demais → retrato) via Playwright
argument-hint: <caminho do .html>
---

Você foi invocado para exportar PDF.

## Procedimento

1. Verificar que o arquivo existe e é slideless.
2. Identificar o modelo (verifica classes raiz):
   - `.deck` → landscape A4
   - demais → retrato A4
3. Rodar:
   ```bash
   python ../scripts/exportar_pdf.py <arquivo.html> --output /mnt/user-data/outputs/<nome>.pdf
   ```
4. Se o script detectar `.deck`, passa orientation=landscape automaticamente.
5. `printBackground=true` é obrigatório (preserva cores e dark mode se ativo).
6. `@media print` nos templates esconde HUD, sidebar, topnav, theme-toggle conforme o caso.
7. Para deck: cada slide vira uma página (1:1).
8. Avisar o usuário sobre o caminho final do PDF.

## Dependências

```bash
pip install playwright
playwright install chromium
```

## Anti-patterns críticos

- Exportar com dark mode ativo se o usuário queria light → confirmar tema antes (ou forçar via `localStorage` no script).
- Não respeitar `@media print` → reler `references/modelos/<modelo>.md` para confirmar regras de print.
