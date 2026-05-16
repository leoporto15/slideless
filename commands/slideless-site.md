---
description: Gera site (SPA single-file com hash routing entre 2-5 views)
argument-hint: <descrição do site e suas views>
---

Você foi invocado para gerar um documento `site` (SPA single-file slideless).

## Pré-requisitos

1. Ler [../references/modelos/site.md](../references/modelos/site.md).
2. Confirmar com o usuário:
   - **Lista de views** (2-5): nome e hash de cada. Se > 5 views, considere [hub](slideless-hub.md) ou [handbook](slideless-handbook.md).
   - **Tema** (default `itau`).

## Procedimento

1. Copiar [../assets/templates/template-site.html](../assets/templates/template-site.html).
2. Aplicar tema.
3. Popular:
   - `.topnav` com 1 `<a href="#hash">` por view.
   - Um `<article class="view">` por view, primeira com `is-active` (sem `hidden`), demais com `hidden`.
4. Hash routing já está no template — não duplicar nem alterar.
5. Garantir que reload em `#sobre` cai em `#sobre` (route() roda no DOMContentLoaded).
6. Transições entre views via fade (opacity), NÃO translate (vira PPT).
7. Validar e entregar em `/mnt/user-data/outputs/site-<slug>.html`.

## Anti-patterns críticos

- `<a href="outra.html">` → tudo dentro de um único arquivo.
- View hero "estilo landing" gigante → `<h1>` 2.5rem.
- Sem `hidden` attribute nas views não-ativas (a11y).
