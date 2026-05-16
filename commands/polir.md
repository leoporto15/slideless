---
description: Refina tipografia, espaçamento e hierarquia visual de um documento slideless
argument-hint: <caminho do arquivo>
---

Você foi invocado para polir um documento.

## Escopo

Apenas refino visual. **Não toca estrutura nem conteúdo.**

## Pontos a revisar

### Tipografia
- [ ] H1 ~2.5rem (não-deck) / clamp() (deck)
- [ ] H2 1.75rem com `margin-top: var(--space-10)` (respiração entre seções)
- [ ] Lead `max-width: 60ch`; parágrafos `max-width: 65ch`
- [ ] `line-height: 1.65` no body, `1.25` em headings
- [ ] `letter-spacing: -0.015em` em headings (compensa otimismo)
- [ ] `font-family: var(--font-display)` em headings
- [ ] Listas com `li::marker { color: var(--color-fg-subtle); }`

### Espaçamento
- [ ] Tokens `--space-*` em todo `margin`/`padding` (sem números soltos)
- [ ] Vertical rhythm consistente — h2 sempre `space-10` antes; h3 `space-7`
- [ ] Coluna `max-width: var(--content-max)` (720px) em handbook/scrollytelling

### Hierarquia
- [ ] Lead mais escuro/destacado que body
- [ ] `font-weight` consistente — 700 em h1/h2, 600 em h3/h4, 400 body, 500 ênfase
- [ ] Cores acent SÓ em links, CTAs, accents semânticos (não decoração de fundo)
- [ ] Hover states em links/cards (translate -2px ou border accent)
- [ ] Border de cards `--color-border` (não `--color-accent` — accent é hover)

### Sombras
- [ ] Cards em estado normal: sem sombra. Hover: `var(--shadow)`.
- [ ] Dark mode: sombras mais fortes (já está no tokens)

## Procedimento

1. Ler arquivo. Identificar tema/modelo.
2. Para cada checklist acima, identificar desvios.
3. Aplicar correções via Edit.
4. **Não introduzir nem componentes nem conteúdo novo.** Só refino.
5. Rodar `validar.py` antes de retornar.

## Não fazer

- Não adicionar animações novas.
- Não trocar componentes (callout virar card etc.).
- Não reescrever texto.
