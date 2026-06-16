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
- [ ] Letter-spacing por corpo, nunca valor único no documento: negativo em display grande (−0.02 a −0.04em em ≥56px), zero no body, positivo em caps/labels. Headings médios conforme o kit tipográfico do documento.
- [ ] `font-family: var(--font-display)` em headings
- [ ] Listas com `li::marker { color: var(--color-fg-subtle); }`

### Espaçamento
- [ ] Tokens `--space-*` em todo `margin`/`padding` (sem números soltos)
- [ ] Vertical rhythm consistente — h2 sempre `space-10` antes; h3 `space-7`
- [ ] Coluna `max-width: var(--content-max)` (720px) em handbook/scrollytelling

### Hierarquia
- [ ] Lead mais escuro/destacado que body
- [ ] Hierarquia de peso conforme o sistema tipográfico do documento — **PROIBIDO normalizar tudo para 600/700** (o tell clássico de IA). Se o documento usa contraste de peso (ex.: 300 vs 800) como dispositivo, preservar e reforçar.
- [ ] Cores acent SÓ em links, CTAs, accents semânticos (não decoração de fundo)
- [ ] Hover por papel do componente: underline-grow em links, background-sweep em tabs/filtros, lift SÓ em card clicável. **PROIBIDO adicionar `translateY` de hover em elemento não-clicável** — este comando nunca instala hover-lift.
- [ ] Border de cards `--color-border` (não `--color-accent` — accent é hover)

### Sombras
- [ ] Cards em estado normal: sem sombra. Hover: `var(--shadow)`.
- [ ] Dark mode: sombras mais fortes (já está no tokens)

## Passe 2 — Microtipografia (obrigatório, verificável)

É a assinatura invisível de estúdio: nenhum gerador de IA aplica por default. Cada item é checável por busca no arquivo.

- [ ] **Aspas curvas pt-BR** — `“ ” ‘ ’` em toda citação, blockquote e pull-quote; apóstrofo `’`. Nunca `"` `'` em texto corrido (código inline é exceção).
- [ ] **NBSP entre valor e unidade** — `R$ 1,2 bi` · `82 ms` · `14 p.p.` (usar `&nbsp;` ou U+00A0).
- [ ] **`font-variant-numeric: tabular-nums lining-nums`** em toda célula de tabela numérica, KPI, `.metric__val` e tick de gráfico.
- [ ] **`text-wrap: balance`** em h1–h3; **`text-wrap: pretty`** em parágrafos (degrada silenciosamente).
- [ ] **Formatação numérica pt-BR consistente** — vírgula decimal em TODO lugar: texto, tabela, KPI e ticks/tooltips do Chart.js (`toLocaleString('pt-BR')` — ver css-patterns.md §5.0).
- [ ] **Travessão — com espaços** em apostos; hífen só em compostos.
- [ ] **Tracking por corpo** — ≥3 valores distintos no documento com sinais diferentes (negativo no display, zero no body, positivo em caps) — nunca um único letter-spacing global.
- [ ] **Linha de total com fio duplo** (`border-top: 3px double`) em tabelas financeiras com total.

PROIBIDO neste comando: adicionar hover translateY; normalizar pesos para 600/700; instalar `data-reveal`; adicionar qualquer recurso listado no `nao-vai-ter` do parti.

## Passe 3 — Régua de craft invisível (o maior multiplicador de "parece caro")

Se o documento é A2/A3 (ou em qualquer nível, para o motion existente), elevar a EXECUÇÃO (Emil/Rauno/Family — ver [../references/ambicao.md](../references/ambicao.md)):

- [ ] **Curvas nomeadas, nunca as default**: `--ease-out-strong: cubic-bezier(0.23,1,0.32,1)`, `--ease-io-strong: cubic-bezier(0.77,0,0.175,1)`, `--spring` via `linear()`. Substituir `ease`/`ease-out`/`ease-in-out` genéricos.
- [ ] **Durações**: teto 300ms para UI (botão 100-160, dropdown 150-250, modal 200-320). Transição >400ms em micro-interação = reduzir.
- [ ] **Entrada lenta / saída rápida**; nunca `scale(0)` (usar 0.96); valores de hover proporcionais ao gatilho.
- [ ] **Origem espacial**: painel/menu escala a partir do `transform-origin` do botão que o abriu, não do centro.
- [ ] **`.no-transitions` no toggle de tema** (impede a página de "respirar" no switch dark/light — ver design-system.md).
- [ ] **`transition` property-scoped** (nunca `all`); só `transform`/`opacity` animados (compositados).

PROIBIDO no Passe 3: criar momento-wow novo (isso é geração/`/animate`, não polimento); contrariar o nível de ambição declarado.

## Procedimento

1. Ler arquivo. Identificar tema/modelo.
2. Para cada checklist acima, identificar desvios.
3. Aplicar correções via Edit.
4. **Não introduzir nem componentes nem conteúdo novo.** Só refino.
5. Rodar `validar.py` antes de retornar.

## Gate de render antes de entregar (v7 — obrigatório)
O passe de qualidade mexe no render — além do `validar.py`, rodar:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../references/wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Não fazer

- Não adicionar animações novas.
- Não trocar componentes (callout virar card etc.).
- Não reescrever texto.
- **Não convergir o documento para valores "da casa".** Polir reforça as decisões de design DESTE documento (se houver bloco `<!-- slideless:parti -->` no head, respeitá-lo integralmente) — nunca substitui a direção dele por defaults.
