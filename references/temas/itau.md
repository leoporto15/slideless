# Temas `itau` — família (6 registros oficiais)

Sistema de cor da marca (Guia de Marca Itaú, Dez 2023, V1). São **6 temas itau**, todos com a **laranja `#FF6200` como fio condutor**, + o `neutro` (white-label). Registro/fonte única: [../../assets/temas/temas.json](../../assets/temas/temas.json).

| Tema | Canvas | Uso (guia) |
|---|---|---|
| **itau-padrao** *(default; alias `itau`)* | branco + cool gray (p.74-75) | institucional padrão |
| **itau-navy** | navy `#000D3C` + laranja | alta renda/Personnalité (p.20) |
| **itau-grafite** | carvão/espresso `#1E1C1A` (dark quente) | soft dark premium — deck/keynote, fácil no olho |
| **itau-aco** | aço/grafite frio `#1E242C` (dark frio) | dim mode contemporâneo — deck/site/produto |
| **itau-areia** | oat/papel `#ECE4D5` (quiet-luxury) | report/handbook editorial quente |
| **itau-bruma** | azul-acinzentado `#E7ECF2` (light frio) | calmo/arquitetônico — deck/site/hub |

Cada tema é um arquivo completo em `assets/temas/<tema>.css`, **gerado por `python scripts/gen_temas.py`** a partir da base provada **`itau-base.css`**: troca o canvas (bg/fg/border/accent) e anexa as camadas de cor derivadas em OKLCH (accent-text, secondary, cat/seq/div). Todos compartilham a mesma estrutura. Gate: `gen_temas.py --verify` (contraste AA + daltonismo). O `scaffold.py` injeta o tema escolhido.

**Brand-safety (Guia p.88):** vermelho e roxo = concorrentes (proibidos como identidade); laranja inegociável; ≤3 cores complementares por peça; sem gradiente. `validar.py` checa via `B-brand`.

**CSS base (estrutura/tokens, vale p/ os 6):** [../../assets/temas/itau-base.css](../../assets/temas/itau-base.css) — **base estrutural, não é tema selecionável** (não está no `temas.json`).

## Mapa de uso (storytelling de cor)

Os 7 temas formam **pares de temperatura** — não 7 cores soltas. Escolha pelo *tom* da mensagem e pela audiência:

| Tema | Tom / quando usar | Audiência típica | Luz | Par cromático (secundário) |
|---|---|---|---|---|
| **padrao** | institucional neutro — o default seguro | qualquer área | claro | azul-tinta |
| **areia** | editorial quente, quiet-luxury — leitura longa | report/handbook | claro (quente) | azul-tinta |
| **bruma** | calmo, arejado, arquitetônico | deck/site/hub leve | claro (frio) | teal |
| **navy** | premium sóbrio, autoridade | board, alta renda, Personnalité | escuro | **dourado/champagne** |
| **grafite** | dark quente, premium acolhedor | keynote/deck à noite | escuro (quente) | **âmbar** |
| **aco** | dark frio, técnico/produto | produto, dados, engenharia | escuro (frio) | **ciano** |
| **neutro** | white-label, fora do Itaú | externo, co-branded | claro | (dourado) |

Eixos: **warm** = areia (light) / grafite (dark) · **cool** = bruma (light) / aco (dark) · **oficial** = padrao · **premium** = navy · **white-label** = neutro.

## Camadas de cor geradas (OKLCH)

Além do canvas, cada tema define (gerado, calibrado por canvas, gated por `--verify`):

- **`--color-accent-text`** — laranja escurecida p/ **texto pequeno** em canvas claro (passa AA 4.5; o `#FF6200` puro como texto miúdo sobre claro fica ~2.5). Em canvas escuro = a laranja da marca. A laranja vibrante segue intacta em superfície/headline/ícone.
- **`--color-secondary` (+`-dim`)** — o **par cromático** do tema (tabela acima). Papel = dado/realce secundário, **subordinado ao laranja** (nunca em CTA/título).
- **`--cat-1..6` / `--seq-1..5` / `--div-1..5`** — paleta de **dados** (gráficos): categórica (cat-1 = laranja-tese), sequencial (magnitude), divergente (laranja↔azul, CVD-safe). Detalhes e uso: [../css-patterns.md](../css-patterns.md) §5.0c. **Nunca** usar as cores semânticas (`info/success/teal/plum`) como série.
- **`::selection`** na marca + **`@media (forced-colors)`** (alto contraste do SO).
- **Canvas invertido** (navy/grafite/aco): o `:root` herda a paleta **semântica dark** (senão success/teal/plum ficariam ilegíveis sobre o fundo escuro).

Matemática de cor em [../../scripts/colorkit.py](../../scripts/colorkit.py); geração em [../../scripts/gen_temas.py](../../scripts/gen_temas.py).

> **v4: cada tema tem DUAS CAMADAS** — **[MARCA]** inviolável (copiar) + **[DIREÇÃO]** composta conforme o parti. A seção "Identidade" abaixo descreve a base cálida (itau-base); o `itau-padrao` (default) usa a base fria oficial (branco + cool gray).

---

## Identidade

- **Accent primário:** laranja oficial `#FF6200` no light **e no dark** (mesma laranja — nunca âmbar/amarelo `#FA9F09` como accent; isso lia "amarelo" no dark e foi corrigido).
- **Fontes:** dentro da rede Itaú, `Itau Display` (headings) + `Itau Text` (corpo) prevalecem quando disponíveis. **Fora da rede, o fallback é o kit tipográfico do documento** (slots `--kit-display` / `--kit-text` / `--kit-mono` de [../type-kits.md](../type-kits.md)), desenhado por kit. **O fallback NUNCA é Inter** — Inter como display é proibido (era o slop de 1ª geração; Fraunces como default era o de 2ª).
- **Background light:** cream warm `#faf7f5` (não branco puro), elevado `#ffffff`, sunken `#f4f1ec`.
- **Background dark:** preto quente `#14110d` (NÃO preto puro `#000000`) — bege/marrom escuro, identidade Itaú; elevado `#1c1814`.
- **Foreground:** warm dark `#292017` (não preto puro), muted `#6b5d50`.
- **Cores semânticas:** info usa azul Itaú (`#3B85FA`), warn usa amarelo Itaú (`#FBC305`); paleta multi-dimensional (success/teal/plum) em OKLCH — ver abaixo.

---

## Duas camadas

O `itau.css` é marcado grupo a grupo em duas camadas (mais `[SISTEMA]`, que é engenharia de viewport):

- **`[MARCA]` — inviolável.** Laranja `#FF6200`, paleta semântica com papéis, bg/fg warm, dark mode, a11y (focus, reduced-motion), OKLCH. **Copiar SEMPRE, nunca alterar.**
- **`[DIREÇÃO]` — compor conforme o parti.** Fontes (slots `--kit-*`), glows, radius, sombras, easings, affordances de componente. São **defaults neutros** — o parti ([../direcao-de-arte.md](../direcao-de-arte.md)) decide o que entra, substitui ou renuncia. **Motion NÃO mora aqui:** vem do perfil declarado, colado como bloco aditivo.

Dois documentos `itau` compartilham **marca**, nunca **fingerprint**.

---

## Tokens (resumo)

Definição completa em [../../assets/temas/itau-base.css](../../assets/temas/itau-base.css). Tokens-chave:

| Token | Light | Dark |
|---|---|---|
| `--color-accent` | `#FF6200` | `#FF6200` |
| `--color-bg` | `#faf7f5` (cream) | `#14110d` |
| `--color-bg-elevated` | `#ffffff` | `#1c1814` |
| `--color-bg-sunken` | `#f4f1ec` | `#221d18` |
| `--color-fg` | `#292017` (warm dark) | `#ede5dd` |
| `--color-fg-muted` | `#6b5d50` | `#b8aa9a` |
| `--color-fg-subtle` | `#8a7e72` | `#786e62` |
| `--color-border` | `rgba(41,32,23,0.10)` | `rgba(237,229,221,0.10)` |
| `--font-display` | `'Itau Display', var(--kit-display, Georgia), serif` | mesmo |
| `--font-text` | `'Itau Text', var(--kit-text, …), system-ui, sans-serif` | mesmo |
| `--font-mono` | `var(--kit-mono, 'IBM Plex Mono'), …, monospace` | mesmo |

As fontes saem dos **slots do kit** ([../type-kits.md](../type-kits.md)) — `Itau Display/Text` prevalecem na rede, o kit é o fallback fora dela. **Nunca Inter.**

Tokens fixos `[MARCA]` (não mudam com tema):
- `--itau-orange: #FF6200` · `--itau-orange-2: #F88104` · `--itau-orange-3: #FA9F09`
- `--itau-blue-3: #3B85FA` · `--itau-yellow: #FBC305` · `--itau-warm-black: #14110d`

### Paleta semântica multi-dimensional (`[MARCA]`)

Cor é **informação, não decoração** (anti-pattern C14): cada cor só entra com papel declarado. Cada papel tem `--color-*` (foreground/contorno) + `--color-*-dim` (fundo tingido). Redefinida em **OKLCH** (derivada do matiz do laranja) dentro de `@supports`, com os hex como fallback:

| Papel | Token | Uso |
|---|---|---|
| brand accent | `--color-accent` | links, CTA, número de seção, headings hover |
| info / dados | `--color-info` (`#3B85FA`) | azul Itaú |
| sucesso / positivo | `--color-success` | verde fechado (OKLCH `oklch(52% 0.11 140)`) |
| técnico / analítico | `--color-teal` | `oklch(52% 0.08 200)` |
| crítico / atenção | `--color-plum` | `oklch(46% 0.12 355)` |
| warn / danger | `--color-warn` / `--color-danger` | amarelo Itaú / vermelho |

> **`--color-sage` foi FUNDIDO com `--color-success` na v4** — eram o mesmo lime do Tailwind (lime-600 vs lime-700), duas cores fingindo ser duas dimensões. `--color-sage` permanece como **alias** de `--color-success` por compatibilidade com `.var-sage` em documentos antigos.

---

## Aplicação

Toda geração com tema `itau` deve:

1. O tema entra via `scaffold.py` (injeta `assets/temas/<tema>.css` — o tema escolhido — no marker `SLIDELESS:THEME` — camada `[MARCA]` intacta). **Não regurgitar nem redeclarar o tema** — já está inline no `<style>`. Apenas compor a camada `[DIREÇÃO]` conforme o parti, com edits pequenos se necessário.
2. Carregar o kit tipográfico do documento via Google Fonts (escolhido em [../type-kits.md](../type-kits.md), decisão do parti — [../direcao-de-arte.md](../direcao-de-arte.md)): `<link>` no slot `SLIDELESS:TYPE-KIT` + bloco `:root` do kit ANTES do tema. Dentro da rede Itaú, `Itau Display`/`Itau Text` prevalecem; o kit é o fallback desenhado fora da rede. **Inter como display é proibido.**
3. Boot script de tema no `<head>` (ver [../design-system.md](../design-system.md#boot-script)).
4. Theme toggle no header.
5. Marca no `topbar`: embarcar a logo via `<img>` base64 — `assets/logos/wordmark-black.png` (light) / `assets/logos/wordmark-white.png` (dark). Fallback se a logo não couber: wordmark tipográfico (`<span class="topbar__wordmark">itaú</span>` em `--font-display`, peso forte, cor `--color-accent`) — **nunca emoji nem quadrado de cor sólida**.
6. **Motion** não mora no tema: perfil declarado no parti, colado como bloco aditivo (ver [../css-patterns.md](../css-patterns.md) §7/§13.3; [../ambicao.md](../ambicao.md) para A2/A3).

---

## Anti-patterns do tema `itau`

- **Não use `#000000` como bg dark.** Use `#14110d` (preto quente).
- **Não use laranja em fundo amarelo** (contraste insuficiente).
- **Não use cor de marca para decoração estrutural** — laranja é accent (links, CTA, headings hover, número da seção). Bordas são `--color-border`, não laranja.
- **Não use Inter (nem como fallback).** O fallback de fonte é o **kit** ([../type-kits.md](../type-kits.md)): `'Itau Display', var(--kit-display, Georgia), serif`. Inter como display é falha do validador; Fraunces fora do Kit 06 também.
- **Não trate `--color-sage` como cor separada** — é alias de `--color-success` (foram fundidas na v4).
- **Não redeclare `:root` de cores/fontes no template** — o tema é a única fonte da verdade; redeclarar duplica e desincroniza.
- **Glow não é default.** Os `--glow-*` são camada `[DIREÇÃO]` (opt-in do parti, `glow-localizado`), nunca wallpaper incondicional em `body::before` (anti-pattern C8).

---

## Quando usar `itau` vs `neutro`

| Cenário | Tema |
|---|---|
| Default — qualquer comunicação interna oficial | `itau` |
| Documento que vai para fora do Itaú (parceiros, fornecedores) | `neutro` |
| Documento institucional/regulatório (sem brand) | `neutro` |
| Material que será co-branded ou white-labeled | `neutro` |
| Documento experimental/draft | indiferente — `itau` por default |
