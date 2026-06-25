# Tema `itau`

Tema corporativo Itaú. Default da skill quando o usuário não especificar tema.

**CSS:** [../../assets/temas/itau.css](../../assets/temas/itau.css).

> **v4: o tema tem DUAS CAMADAS.** Ver "Duas camadas" abaixo — copiar a camada **[MARCA]** sempre, **compor** a camada **[DIREÇÃO]** conforme o parti. Nunca mais "copiar inteiro e pronto".

---

## Identidade

- **Accent primário:** laranja oficial `#FF6200` no light, laranja luminoso `#FA9F09` no dark.
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

Definição completa em [../../assets/temas/itau.css](../../assets/temas/itau.css). Tokens-chave:

| Token | Light | Dark |
|---|---|---|
| `--color-accent` | `#FF6200` | `#FA9F09` |
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

1. O tema entra via `scaffold.py` (injeta `assets/temas/itau.css` no marker `SLIDELESS:THEME` — camada `[MARCA]` intacta). **Não regurgitar nem redeclarar o tema** — já está inline no `<style>`. Apenas compor a camada `[DIREÇÃO]` conforme o parti, com edits pequenos se necessário.
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
