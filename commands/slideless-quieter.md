---
description: Reduz designs ruidosos dentro do parti — lê o registro e baixa a temperatura onde a fonte pede sobriedade (tipografia, cor muted, motion calma, materialidade por fio). Opera no nível declarado, não é kit fixo. Compõe com /slideless-delight para refinamento editorial.
argument-hint: <arquivo.html opcional>
---

Você é um designer sênior pareado com um engenheiro sênior elevando um documento slideless existente. Aplica a transformação **quieter** de forma determinística, preservando 100% do conteúdo.

## Workflow

1. Identificar o arquivo HTML alvo. Se o usuário não indicou, perguntar.
2. Ler o arquivo completo. **Extrair o bloco `<!-- slideless:parti -->`** — operar dentro da direção declarada (nunca adicionar recurso do `nao-vai-ter`; respeitar o kit tipográfico do documento). Divergência consciente exige `<!-- quieter-override: motivo -->`.
3. Aplicar a transformação **quieter** (abaixo — **exemplo de referência, adaptar à direção**, não colar verbatim).
4. **Preservar 100% do conteúdo** — texto, números, dados, estrutura nunca mudam. Só visual.
5. Validar: dark mode continua funcionando, `prefers-reduced-motion: reduce` é respeitado, console sem erros.
6. Sobrescrever o arquivo original (ou criar `<nome>-quieter.html` se o usuário pedir).
7. Reportar em uma frase o que foi feito.

---

## Quieter — Reduz designs ruidosos

**Quando usar:** documento exagerado/gritando. Excesso de cor, motion, peso. Precisa virar editorial calmo.

**Tokens CSS:**
- `--size-mega` × 0.85, `--size-giga` × 0.85, `--size-display` × 0.85
- `--duration-fade` × 1.5, `--duration-slide` × 1.5 (transições mais lentas e contemplativas)
- `--space-*` × 1.20 (mais respiro)
- Glow existente: opacity reduzida ou removido (se o parti permitir)
- Reduzir os EXTREMOS de peso do kit em 1 passo (900→700, 300→400) — sem normalizar tudo para 600/700 (tell de IA)
- `--font-display` permanece a do KIT do documento — quieter não troca fonte (e Instrument Serif é banida; ver type-kits.md)

**Atributos a remover:**
- Todos os `data-mark` (declutter visual)
- `data-auto-animate` em slides consecutivos
- Converter `data-fragment="current-visible"` em `data-fragment` simples (ou remover se for ruído)
- Box-shadows decorativas em cards (manter só estruturais leves)

**Não tocar:** conteúdo, gráficos, tabelas, slides.

---

## Composição com outros verbos

- `quieter` + `/slideless-delight` → editorial refinado com micro-interações
- `quieter` + `/slideless-animate` → motion calma sobre base sóbria

**Combinação que se anula:** aplicar `quieter` depois de `/slideless-bolder` (ou vice-versa) zera o efeito — avisar o usuário.

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
- Conteúdo da fonte ainda 100% presente

Reportar em uma frase ao final:
> "Apliquei **quieter** em `<arquivo>` — tipografia -15%, glow reduzido, fallback serif editorial, marks removidos. Conteúdo preservado integralmente."
