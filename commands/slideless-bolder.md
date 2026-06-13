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

**Não tocar:** conteúdo textual, estrutura, gráficos, tabelas, layouts semânticos.

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

Reportar em uma frase ao final:
> "Apliquei **bolder** em `<arquivo>` — tipografia hero +30%, números-âncora circulados via Rough Notation, glow atmosférico reforçado. Conteúdo preservado integralmente."
