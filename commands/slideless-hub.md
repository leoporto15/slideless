---
description: Gera hub (portal de cards categorizáveis com painéis in-page) a partir de conteúdo do usuário
argument-hint: <tópico ou descrição dos recursos>
---

Você foi invocado para gerar um documento `hub` (slideless).

## Pré-requisitos

1. Ler [../references/anti-patterns.md](../references/anti-patterns.md) se ainda não leu nesta sessão.
2. Confirmar com o usuário:
   - **Lista de recursos/cards** com categoria de cada um.
   - **Tema** (`itau` default).
   - Se cada card tem conteúdo expandido (painel) ou apenas link para fora.

## Procedimento

1. Copiar [../assets/templates/template-hub.html](../assets/templates/template-hub.html).
2. Substituir `/* SLIDELESS:THEME */` pelo tema escolhido.
3. Popular:
   - `.filters` com 1 botão por categoria + "Todos".
   - `.grid > .card` com `data-category` e `data-target` para o painel correspondente.
   - `.panel` com mesmo `id` apontado pelo `data-target`.
4. Cards devem ser **informativos** (ícone pequeno, título h3, descrição 1-2 linhas). Ver [../references/anti-patterns.md](../references/anti-patterns.md) A7.
5. Filtros têm que funcionar — não decorativos.
6. Rodar validador e checklist. Salvar em `/mnt/user-data/outputs/hub-<slug>.html`.

## Anti-patterns críticos

- Cards "estilo slide" com ícone 96px + título 2.5rem → cards são editoriais.
- Filtros desconectados do JS → sempre testar filtragem.
