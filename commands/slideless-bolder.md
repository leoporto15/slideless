---
description: Amplifica designs tímidos dentro do parti — lê o registro e o nível de ambição e sobe peso onde a fonte justifica (tipografia hero, dado-âncora protagonista, materialidade da superfície declarada). Não infla glow nem viola o nao-vai-ter. Compõe com /slideless-animate ou /slideless-overdrive.
argument-hint: <arquivo.html opcional>
---

Você é um designer sênior pareado com um engenheiro sênior elevando um documento slideless existente. Aplica a transformação **bolder** de forma determinística, preservando 100% do conteúdo.

## Workflow

1. Identificar o arquivo HTML alvo. Se o usuário não indicou, perguntar.
2. Ler o arquivo completo. **Extrair o bloco `<!-- slideless:parti -->`** — todo refinamento opera DENTRO da direção declarada: nunca adicionar um recurso listado no `nao-vai-ter`, nunca contrariar o perfil de motion (bolder num doc estático amplia tipografia e contraste, NUNCA injeta animação). Divergência consciente exige `<!-- bolder-override: motivo -->`.
3. Aplicar a transformação **bolder** (abaixo — é **exemplo de referência, adaptar à direção do documento**, não colar verbatim).
4. **Preservar 100% do conteúdo** — texto, números, dados, estrutura nunca mudam. Só visual.
5. Validar: dark mode continua funcionando, `prefers-reduced-motion: reduce` é respeitado, console sem erros, `validar.py` sem novas falhas P.
6. Sobrescrever o arquivo original (ou criar `<nome>-bolder.html` se o usuário pedir).
7. Reportar em uma frase o que foi feito.

---

## Bolder — Amplifica designs tímidos

**Quando usar:** documento gerado ficou "medíocre" ou tímido. Tipografia sem peso, números não destacados, hero sem impacto.

**Tokens CSS (atualizar valores no `:root`):**
- `--size-mega` × 1.30
- `--size-giga` × 1.30
- `--size-display` × 1.20
- `--space-7` × 1.30, `--space-8` × 1.30 (mais whitespace ao redor de heroes)
- Ampliar o CONTRASTE DE PESO do kit (ex.: display 300→900 no mesmo título) — bolder é tensão tipográfica, não só tamanho
- Glow: SÓ se o documento já o tem declarado no parti (intensificar o existente); se `nao-vai-ter: glow-radial`, NUNCA adicionar

**Atributos automáticos (adicionar onde não existir):**
- Detectar números >= 10 dentro de `.big-num__val`, `.metric-d__val`, `.fact-val`, `.kpi-card__value` → envolver o número (não o sufixo) com `<span data-mark="circle" data-mark-color="var(--color-accent)">N</span>`. Se já tem `data-mark`, não duplicar.
- Detectar `<em>` em `.title-mega`, `.title-xl`, `.title-lg` → adicionar `data-mark="underline"` se ainda não tem.
- Detectar `h1`/`h2` com `.title-mega` ou `.title-xl` → adicionar `data-fit-text` se ainda não tem.
- Hero slides (primeiro slide ou layout-hero) sem `[data-anim="hero"]` no `<h1>` → adicionar.

**Ambição, não só tokens — qual família W# e quanta densidade.** Bolder não é só ampliar `--size-*`: é subir a INTENSIDADE/ambição dentro do parti. Quando a fonte justifica, encarnar o dado-tese com um momento-wow da biblioteca [../references/wow-components.md](../references/wow-components.md) (W1–W31, drop-ins copy-paste com `@supports` + estado-final-base + reduced-motion — **COLAR, não reinventar**) em vez de só engordar o título: manchete-display via **W19 masked-type** (hue ÚNICO da marca, 1/doc) ou manchete cinética **W3**; número-tese protagonista via **W15 odômetro** / **W25 data-choreography**; herói de impacto via **W18 sticky-stack** (registro expressivo). **Subir um degrau na §STACKING** (ex.: A2 com 3 momentos → 4–5) só se a fonte aguentar — sempre dentro do `nao-vai-ter` e do perfil de motion (bolder num doc `estatico` amplia tipografia/contraste, **NUNCA injeta animação**). A camada premium (W10–W31) é **proibida em registro sóbrio** (`institucional-impresso`/`relatorio-de-bancada` — P-premium-sobrio); lá bolder sobe só por peso/contraste/whitespace.

**Não tocar:** conteúdo textual, estrutura, gráficos, tabelas, layouts semânticos.

### §STACKING — subir intensidade sem virar cassino

Ao adicionar momentos-wow, respeitar a densidade da §STACKING de [../references/wow-components.md](../references/wow-components.md): **A2 = 3–5 momentos; A3 = 6–8**, com **1 herói pinned único** + 2 sistemas ambientes na mesma física + **~70% calmo**. Bolder pode subir um degrau de ambição, mas **nunca empilhar pinned demais** (jamais 2 mecânicas pinned/scrub disputando o mesmo gesto de scroll) nem encher todos os viewports — mais peso ≠ mais elementos animados.

### Armadilhas de render (não reintroduzir)

Ver §Armadilhas de [../references/wow-components.md](../references/wow-components.md) — o que o `smoke.py` reprova:
- **Odômetro:** `.od-digit { height:1em }` (+ `overflow:clip`), senão a tira 0-9 vaza.
- **Número duplicado ("7070%"):** nunca número como nó de texto **E** `::after { content: counter() }` juntos (esconder o texto-base sob o `@supports`+motion).
- **Lista numerada:** counter **absoluto** (não `display:grid` — quebra texto por-caractere).
- **`<canvas>`:** nunca `width:auto` (estoura em HiDPI).
- **`a[href="#"]`** sempre com `preventDefault`.

---

## Composição com outros verbos

- `bolder` + `/slideless-animate` → deck executivo, peso visual + movimento
- `bolder` + `/slideless-overdrive` → showpiece tecnológico de alto perfil (só com conteúdo à altura)

**Combinação que se anula:** aplicar `bolder` depois de `/slideless-quieter` (ou vice-versa) zera o efeito — avisar o usuário.

---

## Regras invioláveis

1. **Conteúdo é sagrado** — texto, números, dados, estrutura nunca mudam
2. **Single-file** — CSS/JS inline preservado, sem novos arquivos externos (CDN OK)
3. **Acessibilidade** — WCAG AA mantido, foco visível, ARIA, `prefers-reduced-motion`
4. **Dark mode** — toggle continua funcionando após a transformação
5. **Idempotência** — rodar 2x não duplica efeitos (checar antes de adicionar)

## Antes de entregar

- Documento abre sem console errors
- Dark mode toggle ainda funciona
- `prefers-reduced-motion: reduce` desabilita motion adicionada
- Conteúdo da fonte ainda 100% presente

## Gate de render antes de entregar (v7 — obrigatório)
Todo verbo modifica render — rodar os DOIS e corrigir a CAUSA antes de entregar:
- `python scripts/validar.py <arquivo.html>` → `0 erro(s)`.
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide curto, invasão de coluna, scroll horizontal).
Nunca entregar com `SMOKE FAIL`.

Reportar em uma frase ao final:
> "Apliquei **bolder** em `<arquivo>` — tipografia hero +30%, números-âncora circulados via Rough Notation, glow atmosférico reforçado. Conteúdo preservado integralmente."
