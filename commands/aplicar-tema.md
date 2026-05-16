---
description: Troca o tema (neutro ↔ itau) de um documento slideless existente
argument-hint: <neutro|itau>
---

Você foi invocado para trocar tema.

## Procedimento

1. Identificar o tema atual: presença de tokens `--itau-orange` em `:root` ⇒ `itau`. Caso contrário, `neutro`.
2. **Não duplicar trabalho:** se o tema-alvo é o atual, avisar e parar.
3. Substituir bloco inteiro de tokens:
   - Bloco `:root { … }` (do primeiro `--itau-orange` ou `--color-bg` até a `}` correspondente).
   - Bloco `[data-theme="dark"] { … }`.
   - Reset/base, callouts, code, toggle, theme-toggle, cards, métricas, timeline — **manter** (são compartilhados, só usam `var(--…)`).
4. Substituir pelo conteúdo do tema-alvo, vindo de [../assets/temas/itau.css](../assets/temas/itau.css) ou [../assets/temas/neutro.css](../assets/temas/neutro.css).
5. **Fontes:**
   - `itau` → garantir Inter no `<link href="…">` Google Fonts (não precisa carregar Itaú Display/Text — fallback para Inter é automático).
   - `neutro` → idem (Inter cobre).
   - `deck` → precisa peso 800: `family=Inter:wght@400;500;600;700;800`.
6. **Logo:** se tema = `itau`, manter logo Itaú no topbar; se `neutro`, considerar remover ou substituir.
7. Rodar validador.

## Anti-patterns críticos

- Esquecer override de algum `--color-*` em `[data-theme="dark"]` após troca → dark mode quebrado.
- Não trocar fontes ao mudar de `itau` para `neutro` (Itaú Display continua referenciada mesmo sem efeito).
