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

0. **Parti (obrigatório)** — [../references/direcao-de-arte.md](../references/direcao-de-arte.md): 7 decisões + `nao-vai-ter` derivadas do assunto, capa/kit/superfície ≠ exemplo canônico, bloco no `<head>`. A 7ª decisão é `ambicao` ([../references/ambicao.md](../references/ambicao.md)) — **default A2-elevado** para site; se A2/A3, o campo `momento-wow` (W1-W9; W5 morph na troca de view encaixa bem — mas o full-morph com View Transitions é A3/overdrive) é **obrigatório**.
1. Copiar [../assets/templates/template-site.html](../assets/templates/template-site.html).
2. Slot `SLIDELESS:TYPE-KIT` com o `<link>` do kit + `:root` do kit antes do tema. Aplicar tema (MARCA intacta; DIREÇÃO conforme o parti).
3. **Compor**:
   - `.topnav` com 1 `<a href="#hash">` por view.
   - Um `<article class="view">` por view, primeira com `is-active` (sem `hidden`), demais com `hidden`.
   - **Cada view com composição própria** (split assimétrico, lista editorial, tabela, colunas) — views com o mesmo ritmo título-centrado+grid = falha de direção de arte.
4. Hash routing já está no template — não duplicar nem alterar. View Transitions API NÃO (reservada ao /overdrive).
5. Garantir que reload em `#sobre` cai em `#sobre` (route() roda no DOMContentLoaded).
6. Transições entre views via fade (opacity), NÃO translate (vira PPT).
7. Validar (categoria P) + checklist (bloco 🎨) + gate perceptual se disponível. Entregar em `outputs/site-<slug>.html` e reportar o parti em 1 linha.

## Anti-patterns críticos

- `<a href="outra.html">` → tudo dentro de um único arquivo.
- View hero "estilo landing" gigante → `<h1>` 2.5rem.
- Sem `hidden` attribute nas views não-ativas (a11y).
