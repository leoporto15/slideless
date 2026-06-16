---
description: Converte um documento entre modelos compatíveis (handbook ↔ scrollytelling, hub ↔ site)
argument-hint: <modelo-alvo>
---

Você foi invocado para converter entre modelos.

## Conversões viáveis

| De → Para | Notas |
|---|---|
| `handbook` → `scrollytelling` | Sidebar some, TOC some, h2 viram seções. Progress bar adicionada no topo. Confluence de uma página → narrativa de leitura. **`data-reveal` só em figuras/dados (≤40% das sections), conforme o `motion` do parti — não em toda section nem em texto corrido.** |
| `scrollytelling` → `handbook` | Adiciona sidebar (lista os h2), TOC, scrollspy. Cenas viram seções. Progress bar removida. |
| `hub` → `site` | Cards viram top-nav. Painéis viram `<article class="view">`. Filtros removidos. |
| `site` → `hub` | Views viram cards na home. Hash routing removido. Filtros opcionais. |

## NÃO viáveis automaticamente

| Tentativa | Por quê |
|---|---|
| `deck` → `scrollytelling` | Slides costumam ser rasos demais (gigantismo esconde). Avisar usuário; oferecer gerar do zero a partir do conteúdo. |
| Qualquer → `deck` | Deck pede slide-by-slide pensado. Não há conversão automática; recriar com [slideless-deck](slideless-deck.md). |
| `handbook` → `hub` | Conteúdo costuma ser narrativo/sequencial, não cabe em cards. Sugerir manter handbook. |

## Procedimento

1. Confirmar conversão alvo + viabilidade.
2. Carregar template do modelo-alvo como base.
3. Migrar conteúdo:
   - **handbook → scrollytelling:** cada `<section>` do handbook vira `<section class="scene">`. h2 → h2 (mesmo tamanho). **`data-reveal` só em figuras/dados (≤40% das sections), conforme o perfil de `motion` do parti — texto corrido nunca anima.**
   - **scrollytelling → handbook:** inversa. Gerar sidebar listando h2.
   - **hub → site:** painéis viram views; cards viram links de topnav.
   - **site → hub:** views viram painéis; topnav vira cards na home.
4. Manter mesmo tema.
5. Validar resultado.
6. Avisar o usuário sobre componentes específicos que foram perdidos (e.g., sticky chart no scrollytelling → handbook perde o chart sticky).

## Gate de render antes de entregar (v7 — obrigatório)
A transformação mexe no render — além do `validar.py`, rodar:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../references/wow-components.md) §"Armadilhas visuais que o smoke.py reprova".
