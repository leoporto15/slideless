---
description: Endurece a11y, keyboard nav e prefers-reduced-motion de um documento slideless (WCAG AA)
argument-hint: <caminho do arquivo>
---

Você foi invocado para endurecer a11y/UX de um documento.

## Escopo

A11y, keyboard navigation, reduced motion, contraste. **Não toca conteúdo nem estrutura.**

## Pontos a aplicar

### Foco visível
- [ ] `:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }` no CSS global
- [ ] Botões customizados sem `outline: none` removendo foco

### Roles e ARIA
- [ ] Landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`
- [ ] `aria-label` em todo botão sem texto (theme-toggle, hud, panel-close)
- [ ] Theme toggle: `aria-label="Alternar tema"`
- [ ] Tabs: `role="tablist"` no container, `role="tab"`/`aria-selected` nos botões, `role="tabpanel"`/`hidden` nos paineis
- [ ] Callout `danger` com `role="alert"`; demais com `role="note"`
- [ ] Charts (`<canvas>`) com `aria-label` descrevendo o que mostram

### Keyboard
- [ ] Todos interativos alcançáveis por Tab
- [ ] Modelo `deck`: `ArrowLeft`/`ArrowRight`/`Space`/`Esc`/`Home`/`End`/`f` funcionais
- [ ] Modelo `hub`: cards focáveis (já são `<a>`); painéis abertos têm `panel__close` focável
- [ ] Modelo `site`: hash routing acessível por Tab no topnav

### Reduced motion
- [ ] Bloco `@media (prefers-reduced-motion: reduce)` desabilita transitions e animations
- [ ] Reveals: `opacity: 1; transform: none` quando reduced-motion
- [ ] Fragments do deck: visíveis de imediato quando reduced-motion

### Contraste
- [ ] Texto sobre `--color-bg`: relação ≥ 4.5:1 (AA) — `--color-fg` cobre
- [ ] Texto sobre `--color-accent`: relação ≥ 4.5:1 — usar `--color-accent-fg`
- [ ] Texto `--color-fg-muted` sobre bg: ≥ 4.5:1 — OK em ambos os temas
- [ ] Texto `--color-fg-subtle`: limitar a labels/metadata pequenos (3:1 é OK para texto grande mas evitar em corpo)

### Imagens
- [ ] `<img alt>` descritivo, ou `alt=""` se decorativa
- [ ] Imagens informativas com `aria-labelledby` apontando para caption

### Linguagem
- [ ] `<html lang="pt-BR">`
- [ ] `<button type="button">` para evitar submits acidentais

## Procedimento

1. Ler arquivo. Aplicar pontos acima via Edit.
2. Validar com `validar.py --strict` se disponível, ou checklist completo.
3. Se houver dúvida sobre contraste de tokens, calcular manualmente (não chutar).

## Não fazer

- Não remover features acessíveis para "simplificar".
- Não adicionar `aria-*` decorativo (`aria-hidden="false"` sem motivo).
