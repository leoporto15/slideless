# Tema `neutro`

Tema neutro com accent **azul-tinta editorial** sobre **papel neutro**. Para documentos que vão para fora do Itaú, materiais sem brand, white-label, ou contextos onde o laranja não cabe.

**CSS:** [../../assets/temas/neutro.css](../../assets/temas/neutro.css).

> **Refeito na v4.** O neutro v2 era o AI-slop canônico: Inter como display E texto, accent `blue-600` (`#2563eb`) do Tailwind, neutros `slate` (`#0f172a`), violet no syntax. O v4 tem **paleta própria desenhada** (azul-tinta sobre papel) e **nenhuma fonte de marca** — a voz tipográfica vem 100% do kit do documento.

---

## Identidade

- **Accent primário:** azul-tinta `#1c4d8d` no light, azul claro `#7da7d9` no dark. **Não** é `blue-600`/`#2563eb` — é um azul de tinta, mais fechado e editorial.
- **Fontes:** NENHUMA fonte própria. A voz vem do **kit tipográfico do documento** ([../type-kits.md](../type-kits.md)) via slots `--kit-display` / `--kit-text` / `--kit-mono`. Sem kit declarado, degrada para stack de sistema digna (Georgia / Segoe UI / Consolas) — **nunca** para Inter. **Inter em qualquer papel é proibido.**
- **Background light:** papel neutro `#fbfbf9` (nem branco puro, nem warm), elevado `#ffffff`, sunken `#f3f3ef`.
- **Background dark:** tinta fria `#15181c` (NÃO `slate-900` `#0f172a`), elevado `#1d2127`, sunken `#101317`.
- **Cores semânticas:** callouts com matizes desenhados (saturação de tinta), não a paleta Tailwind. Sem violet/indigo em lugar nenhum.

---

## Tokens (resumo)

Definição completa em [../../assets/temas/neutro.css](../../assets/temas/neutro.css). Tokens-chave:

| Token | Light | Dark |
|---|---|---|
| `--color-accent` | `#1c4d8d` | `#7da7d9` |
| `--color-accent-hover` | `#153c70` | `#a3c2e8` |
| `--color-bg` | `#fbfbf9` | `#15181c` |
| `--color-bg-elevated` | `#ffffff` | `#1d2127` |
| `--color-bg-sunken` | `#f3f3ef` | `#101317` |
| `--color-fg` | `#1d2126` | `#e6e7e4` |
| `--color-fg-muted` | `#555c64` | `#a3a8ad` |
| `--color-fg-subtle` | `#878d94` | `#70767d` |
| `--color-border` | `rgba(29,33,38,0.12)` | `rgba(230,231,228,0.12)` |
| `--font-display` | `var(--kit-display, Georgia, 'Times New Roman'), serif` | mesmo |
| `--font-text` | `var(--kit-text, 'Segoe UI', Tahoma), -apple-system, sans-serif` | mesmo |
| `--font-mono` | `var(--kit-mono, Consolas, 'Courier New'), monospace` | mesmo |

Callouts (matizes de tinta, via `-bg` + `-border`, não a paleta Tailwind):

| Token | Light (border) | Dark (border) |
|---|---|---|
| `--color-info-border` | `#2d6da8` | `#7da7d9` |
| `--color-tip-border` | `#3e7a47` | `#76a87e` |
| `--color-warn-border` | `#b07d18` | `#cca149` |
| `--color-danger-border` | `#ad3a3a` | `#d17474` |

Cada um tem o par `--color-*-bg` (fundo tingido, ~7-10% de opacidade) consumido por `.callout--info/tip/warn/danger`. **Sem tokens `--itau-*`.**

**Paleta em OKLCH:** o arquivo redefine accent + bordas de callout em `oklch(...)` dentro de `@supports (color: oklch(...))`, perceptualmente uniforme; os hex acima permanecem como **fallback** para browsers sem OKLCH. Ex.: `--color-accent: oklch(42% 0.09 255)` (light) / `oklch(72% 0.08 255)` (dark).

---

## Aplicação

Toda geração com tema `neutro` deve:

1. O tema entra via `scaffold.py` (injeta `assets/temas/neutro.css` no marker `SLIDELESS:THEME`). **Não regurgitar nem redeclarar o tema** — já está inline no `<style>`.
2. Carregar o **kit tipográfico** do documento (escolhido em [../type-kits.md](../type-kits.md), decisão do parti — [../direcao-de-arte.md](../direcao-de-arte.md)): `<link>` no slot `SLIDELESS:TYPE-KIT` + bloco `:root` do kit ANTES do tema. Como o tema neutro não tem fonte de marca, **o kit é 100% da voz tipográfica**. **Inter como display é proibido**, e Fraunces fora do Kit 06 / Instrument Serif também.
3. Boot script de tema no `<head>` (mesmo padrão que `itau` — ver [../design-system.md](../design-system.md#boot-script)).
4. Theme toggle no header.
5. Sem logo Itaú. Pode usar marca neutra tipográfica (`<span class="topbar__wordmark">`, em `--font-display`) com nome do squad/equipe, ou nada. **Nunca** emoji nem quadrado de cor sólida como marca.
6. **Motion** não mora no tema: vem do perfil declarado no parti, colado como bloco aditivo (ver [../css-patterns.md](../css-patterns.md) §7 e §13.3; [../ambicao.md](../ambicao.md) para A2/A3).

---

## Anti-patterns do tema `neutro`

- **Não use Inter** (em nenhum papel) nem qualquer fonte banida de [../type-kits.md](../type-kits.md). Sem kit, o fallback é Georgia / Segoe UI / Consolas.
- **Não use `blue-600` (`#2563eb`)** nem a paleta accent Tailwind. O accent é o azul-tinta `#1c4d8d`.
- **Não use neutros `slate`** (`#0f172a` e cia). Os neutros são papel/tinta desenhados (`#fbfbf9` / `#1d2126`, dark `#15181c`).
- **Não use violet/indigo** em syntax highlight nem decoração.
- **Não use laranja Itaú nem `--itau-*`** — o tema é deliberadamente sem marca.
- **Não redeclare `:root`** de cores/fontes no template — o tema é a única fonte da verdade.

---

## Quando `neutro` faz mais sentido que `itau`

- Documento entregue a fornecedor / parceiro externo
- Material co-branded ou white-label
- Documento institucional/regulatório sem brand
- Tom técnico-neutro (release notes, postmortem público)
- Treinamento aberto / curso público
- Conteúdo experimental que vira produto separado
