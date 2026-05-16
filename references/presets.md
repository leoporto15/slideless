# Presets visuais

Cinco presets nomeados, cada um com identidade visual distinta. Inspirados em `github.com/nicobailon/visual-explainer` mas adaptados ao contexto Itaú.

| Preset | Palette | Tipografia | Mood | Quando usar |
|---|---|---|---|---|
| **Itaú Signal** (default) | laranja Itaú #FF6200 + warm cream + sage/teal/plum accents | Itaú Display + Inter | corporativo Itaú quente | pitch institucional, materiais com brand Itaú forte |
| **Editorial Dark** | navy deep #0f1729 + warm gold #d4a73a + cream | Fraunces (serif) + Inter | cinematográfico, sofisticado | apresentações executivas, decks de boardroom |
| **Terminal Mono** | bg #0a0a0a + green #00ff9c + cyan accents + faint grid | JetBrains Mono + Fragment Mono | dev-native, técnico | pitches técnicos, conteúdo de engenharia |
| **Swiss Clean** | white + near-black #1a1a1a + bold blue #0030ff accent + grid lines | Inter Tight ou Bricolage | minimal, data-focused | relatórios analíticos, dashboards |
| **Neutro** | white/slate + azul #2563eb | Inter | genérico safe | uso externo (fora Itaú), white-label |

---

## Itaú Signal (default)

Preset principal da skill. Definido em `assets/temas/itau.css` v2.

**Tokens-chave:**
- `--color-accent: #FF6200` (laranja Itaú oficial)
- `--color-bg: #faf7f5` (cream warm — NÃO branco puro)
- `--color-fg: #292017` (warm dark — NÃO preto puro)
- `--glow-hero: radial-gradient(ellipse 90% 70% at 50% 0%, rgba(255, 98, 0, 0.14) 0%, transparent 50%)`

**Paleta semântica 6-cor** para color-coding multi-dimensional:
- `--color-accent` (laranja) — brand
- `--color-info` (azul Itaú #3B85FA) — dado / referência
- `--color-success` (#4d7c0f) — resultado positivo
- `--color-sage` (#65a30d) — neutro vivo
- `--color-teal` (#0f766e) — técnico / analítico
- `--color-plum` (#9f1239) — crítico / atenção

**Fontes:**
- Display: `'Itau Display', 'Fraunces', 'Inter', Georgia, serif`
- Texto: `'Itau Text', 'Inter', sans-serif`
- Mono: `'JetBrains Mono', 'IBM Plex Mono', monospace`

**Dark mode:** bg #14110d (preto quente Itaú, NÃO preto puro), accent shifted +20% luminosity para #FA9F09.

**Usar quando:** apresentação interna Itaú, comunicação institucional, all-hands, deck de produto.

---

## Editorial Dark

Inspirado no preset Midnight Editorial da visual-explainer.

**Tokens-chave:**
- `--color-bg: #0f1729` (deep navy)
- `--color-bg-elevated: #1a2238`
- `--color-fg: #f0ebe4`
- `--color-accent: #d4a73a` (warm gold)
- `--color-info: #5b8def`
- `--glow-hero: radial-gradient(ellipse 90% 60% at 50% 0%, rgba(212, 167, 58, 0.22) 0%, transparent 55%)`

**Fontes:**
- Display: `'Fraunces' opsz 144` (serif para hero), peso 800
- Texto: `'Inter'`
- Mono: `'IBM Plex Mono'`

**Mood:** boardroom, prestígio. Tipografia serif gigante (Fraunces optical-size grandes) cria peso editorial.

**Usar quando:** decks executivos, materiais para conselho/comitê, anúncios formais.

**Status:** preset CSS não implementado ainda (pendência). Quando criar, segue mesmo formato de `itau.css`/`neutro.css`.

---

## Terminal Mono

Preset técnico inspirado em IDE themes (Dracula, Nord, Catppuccin).

**Tokens-chave:**
- `--color-bg: #0a0a0a`
- `--color-bg-elevated: #141414`
- `--color-fg: #d4d4d4`
- `--color-accent: #00ff9c` (terminal green)
- `--color-info: #61afef` (cyan)
- `--font-display: 'JetBrains Mono'` (mono para TUDO, inclusive headings)
- Faint dot grid no background: `background-image: radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px); background-size: 24px 24px;`

**Mood:** dev-native, hacker, técnico.

**Usar quando:** pitches de engenharia, anúncios técnicos, demos de produto técnico, hack days.

**Status:** pendência.

---

## Swiss Clean

Minimal-data-focused.

**Tokens-chave:**
- `--color-bg: #ffffff`
- `--color-fg: #1a1a1a`
- `--color-accent: #0030ff` (electric blue)
- Visible grid lines no background: `background-image: linear-gradient(to right, rgba(0,0,0,0.04) 1px, transparent 1px), linear-gradient(to bottom, rgba(0,0,0,0.04) 1px, transparent 1px); background-size: 80px 80px;`
- Sem glow radial (anti-mood do preset)
- Tipografia condensed: `'Inter Tight'` ou `'Bricolage Grotesque'`

**Mood:** Swiss design, minimal, anti-decoração.

**Usar quando:** relatórios analíticos, dashboards de números, comparativos.

**Status:** pendência.

---

## Neutro

Definido em `assets/temas/neutro.css`. Para documentos fora do Itaú (fornecedor, parceiro, white-label).

**Tokens-chave:**
- `--color-bg: #ffffff` (light) / `#0f172a` slate (dark)
- `--color-accent: #2563eb` (azul) / `#60a5fa` (dark)
- `--font-text: 'Inter'` — sem fontes Itaú

**Mood:** genérico safe.

---

## Como aplicar um preset

1. **Itaú Signal:** copiar `assets/temas/itau.css` inteiro para o `<style>` do HTML, antes dos componentes específicos do modelo.
2. **Neutro:** idem, `assets/temas/neutro.css`.
3. **Editorial Dark / Terminal Mono / Swiss Clean:** ainda não implementados. Para usar, derive a partir do `itau.css` substituindo os tokens `--color-*`, `--font-*` e `--glow-*` conforme a especificação acima.

## Não criar preset inline

Sempre que possível, manter os presets como arquivos `.css` em `assets/temas/`. Inline-override de tokens no `<style>` do HTML final é OK para variações pontuais, mas se o usuário pedir um preset novo recorrente, criar arquivo dedicado.
