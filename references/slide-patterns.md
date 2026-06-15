# Slide Patterns — slideless deck

Referência completa para o modelo `deck`. Ler antes de gerar qualquer apresentação.

---

## Arquitetura do slide deck (engine v3 — a verdade mora no template)

> **v4:** as seções "CSS do Deck Engine" e "JavaScript — SlideEngine" que viviam aqui documentavam o engine ANTIGO (scroll-snap + `.reveal` nth-child + heroUnblur universal) e contradiziam o template. Foram REMOVIDAS. A única fonte de verdade do engine é [../assets/templates/template-deck.html](../assets/templates/template-deck.html) — copiar DELE, nunca daqui. Motion de entrada é decisão do perfil do parti ([direcao-de-arte.md](direcao-de-arte.md) §5), não receita fixa deste arquivo.

```
.deck (engine v3 — slides absolutos, transição controlada por JS)
  └── .slide × N (full-viewport)
       ├── .slide-num (NUNCA top-left — ver REGRA CANÔNICA em Pitfalls)
       ├── [layout: hero | big-num | metrics | list | split | cards | divider | quote | timeline | table | full-bleed]
       └── fragments (data-fragment) e data-anim conforme o perfil de motion do parti
```

**Modelo de navegação:** keyboard (setas/Space/Esc) + overview (`O`) + nav dots + counter + fullscreen + wake lock — tudo já está no template; não duplicar nem remover.
---

## 10 Slide Types

### Type 1 — Title (hero)
```html
<section class="slide slide--title">
  <p class="kicker reveal"><span class="kicker__dot"></span>SEÇÃO 01</p>
  <h1 class="slide__display reveal reveal--hero">Título <em>principal</em></h1>
  <p class="slide__body reveal" style="--i:2">Subtítulo em uma ou duas frases.</p>
  <div class="slide__meta reveal" style="--i:3">
    <span><strong>Apresentador</strong>Cargo · Equipe</span>
    <span><strong>Data</strong>AAAA-MM-DD</span>
  </div>
</section>
```

### Type 2 — Section Divider
```html
<section class="slide slide--divider">
  <div class="divider-content">
    <span class="divider-num reveal">02</span>
    <h2 class="slide__heading reveal" style="--i:1">Nome da Seção</h2>
    <p class="slide__body reveal" style="--i:2">Descrição opcional da seção.</p>
  </div>
</section>
```
```css
.slide--divider { background: var(--color-bg-sunken); }
.divider-num {
  font-family: var(--font-display);
  font-size: clamp(100px, 20vw, 200px);
  font-weight: 200;
  letter-spacing: -0.06em;
  line-height: 0.9;
  color: var(--color-fg);
  opacity: 0.06;
  position: absolute;
  right: 8vw; bottom: 10vh;
  pointer-events: none;
}
```

### Type 3 — Content (heading + text + bullets)
```html
<section class="slide slide--content">
  <p class="kicker reveal"><span class="kicker__dot"></span>TÓPICO</p>
  <h2 class="slide__heading reveal" style="--i:1">Heading principal</h2>
  <ul class="slide__list reveal" style="--i:2">
    <li>Ponto A — descrição</li>
    <li>Ponto B — descrição</li>
    <li>Ponto C — descrição</li>
  </ul>
</section>
```

### Type 4 — Split (heading + dois painéis)
```html
<section class="slide slide--split">
  <h2 class="slide__heading reveal">Heading</h2>
  <div class="slide-split reveal" style="--i:1">
    <div class="split-panel split-panel--left">
      <p class="panel-label">Esquerda</p>
      <p>Conteúdo do painel esquerdo.</p>
    </div>
    <div class="split-panel split-panel--right">
      <p class="panel-label">Direita</p>
      <p>Conteúdo do painel direito.</p>
    </div>
  </div>
</section>
```
```css
.slide-split {
  display: grid; grid-template-columns: 1fr 1fr; gap: 5vw;
  align-items: start; margin-top: var(--space-6);
}
.split-panel { padding: var(--space-5); background: var(--color-bg-elevated);
  border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
.panel-label { font-family: var(--font-mono); font-size: var(--size-xs);
  text-transform: uppercase; letter-spacing: 0.1em; color: var(--color-fg-subtle); margin: 0 0 var(--space-3); }
```

### Type 5 — Diagram (Mermaid ou SVG)
```html
<section class="slide slide--diagram">
  <h2 class="slide__heading reveal">Arquitetura</h2>
  <div class="diagram-shell reveal" style="--i:1">
    <div class="zoom-controls"><!-- botões --></div>
    <div class="mermaid-viewport">
      <div class="mermaid mermaid-canvas">graph TD ...</div>
    </div>
  </div>
</section>
```

### Type 6 — Dashboard (cards KPI + gráfico)
```html
<section class="slide slide--dashboard">
  <p class="kicker reveal">MÉTRICAS</p>
  <div class="kpi-row reveal" style="--i:1">
    <div class="kpi-card">
      <p class="kpi-label">AuM Total</p>
      <p class="kpi-value">R$<span>1,19</span>tri</p>
      <canvas class="kpi-spark" id="spark-aum" aria-label="Sparkline AuM"></canvas>
    </div>
    <!-- mais kpi-cards -->
  </div>
  <canvas class="chart-main reveal" style="--i:2" id="chart-dash" aria-label="Gráfico principal"></canvas>
</section>
```

### Type 7 — Table (dados tabulares)
```html
<section class="slide slide--table">
  <h2 class="slide__heading reveal">Nome da Tabela</h2>
  <div class="table-wrap reveal" style="--i:1">
    <table class="data-table">
      <thead><tr><th>Coluna A</th><th class="num">Valor</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td>Item 1</td><td class="num">R$ 100bi</td><td><span class="badge badge--success">Ativo</span></td></tr>
      </tbody>
    </table>
  </div>
</section>
```

### Type 8 — Code
```html
<section class="slide slide--code">
  <h2 class="slide__heading reveal">Exemplo de código</h2>
  <div class="code-file reveal" style="--i:1">
    <div class="code-file__header"><span class="dot"></span>arquivo.py</div>
    <pre class="code-file__body"><code>def hello():
    return "world"</code></pre>
  </div>
</section>
```

### Type 9 — Quote
```html
<section class="slide slide--quote">
  <div class="quote-wrap reveal">
    <blockquote class="quote-text">"A citação mais importante do documento, em uma a três linhas."</blockquote>
    <cite class="quote-cite"><strong>Nome</strong>Cargo · Empresa</cite>
  </div>
</section>
```
```css
.slide--quote { align-items: center; text-align: center; }
.quote-wrap { max-width: 30ch; }
.quote-text {
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 1.2rem + 2.5vw, 3rem);
  font-weight: 600; font-style: italic;
  line-height: 1.2; letter-spacing: -0.02em;
  color: var(--color-fg); margin: 0 0 var(--space-6);
  quotes: '\201C' '\201D';
}
.quote-text::before { content: open-quote; color: var(--color-accent); }
.quote-cite { font-style: normal; display: block;
  font-size: var(--size-small); color: var(--color-fg-muted); }
.quote-cite strong { display: block; color: var(--color-fg); font-weight: 700;
  font-family: var(--font-display); font-size: var(--size-body); margin-bottom: 4px; }
```

### Type 10 — Full-Bleed (imagem / cor sólida)
```html
<section class="slide slide--full-bleed" style="background: var(--color-bg-sunken);">
  <!-- ou background-image para imagem -->
  <div class="fb-overlay reveal">
    <h2 class="slide__heading" style="color: var(--color-fg)">Heading</h2>
    <p class="slide__body">Texto sobre fundo.</p>
  </div>
</section>
```
```css
.slide--full-bleed { padding: 0; overflow: hidden; }
.slide--full-bleed::after {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse 100% 80% at 50% 50%, transparent 40%, rgba(0,0,0,0.18) 100%);
  pointer-events: none;
}
.fb-overlay {
  position: relative; z-index: 1;
  padding: clamp(36px, 6vh, 80px) clamp(40px, 8vw, 120px);
}
```

---

## Tipografia global do deck

```css
.slide__display {
  font-family: var(--font-display);
  font-size: clamp(48px, 10vw, 110px);
  font-weight: 800; letter-spacing: -0.04em; line-height: 0.95;
  margin: 0 0 var(--space-5);
}
.slide__display em { color: var(--color-accent); font-style: italic; }

.slide__heading {
  font-family: var(--font-display);
  font-size: clamp(28px, 5vw, 52px);
  font-weight: 700; letter-spacing: -0.025em; line-height: 1.05;
  margin: 0 0 var(--space-5);
}
.slide__heading em { color: var(--color-accent); font-style: italic; }

.slide__body {
  font-size: clamp(16px, 2.2vw, 24px);
  line-height: 1.55; color: var(--color-fg-muted);
  max-width: 55ch;
}

.slide__list {
  list-style: none; padding: 0;
  display: flex; flex-direction: column; gap: var(--space-4);
  margin: var(--space-5) 0 0;
}
.slide__list li {
  font-size: clamp(15px, 1.8vw, 20px);
  line-height: 1.45; color: var(--color-fg);
  padding-left: 1.4em; position: relative;
}
.slide__list li::before {
  content: '→'; position: absolute; left: 0;
  color: var(--color-accent); font-weight: 700;
}

.kicker {
  display: inline-flex; align-items: center; gap: 12px;
  font-family: var(--font-mono);
  font-size: clamp(10px, 1.1vw, 13px);
  font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--color-fg-muted);
  margin: 0 0 var(--space-6);
}
.kicker__dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--color-accent); flex-shrink: 0;
}
.kicker--accent { color: var(--color-accent); }

.slide__meta {
  display: flex; gap: var(--space-8); flex-wrap: wrap;
  margin-top: var(--space-8);
  font-size: clamp(13px, 1.5vw, 16px);
  color: var(--color-fg-subtle);
}
.slide__meta span > strong {
  display: block; color: var(--color-fg); font-weight: 700;
  font-family: var(--font-display); font-size: 1.05em; margin-bottom: 3px;
}

/* REGRA CANÔNICA (ver Pitfalls): slide-num em bottom-right, NUNCA top-left */
.slide-num {
  position: absolute; bottom: 18px; right: 28px;
  font-family: var(--font-mono); font-size: 0.6875rem;
  font-weight: 600; letter-spacing: 0.12em;
  color: var(--color-fg-subtle); opacity: 0.55; z-index: 30;
  pointer-events: none; user-select: none;
}
.slide-num strong { color: var(--color-accent); }
```

---

## Estética do deck: vem do parti, não de preset pronto

> **v5: a antiga lista "Preset A/B/C/D" foi removida.** Paletas de prateleira são o oposto do que a skill faz — cada documento **deriva** sua estética do conteúdo, via parti (registro → kit → capa → superfície → motion → ambição). Não escolha um look fechado; componha a direção em [direcao-de-arte.md](direcao-de-arte.md), o kit tipográfico em [type-kits.md](type-kits.md) e a ambição em [ambicao.md](ambicao.md).

Regras que valiam "dentro" dos presets e continuam valendo, agora no nível do parti:

- **Cores saem do tema** ([temas/itau.md](temas/itau.md) / [temas/neutro.md](temas/neutro.md)) — **nunca** redeclare `:root` de cores/fontes no slide; o tema é a única fonte da verdade. Dark mode é nativo dos dois temas, não um "preset midnight".
- **Fontes saem do kit** — Fraunces fora do Kit 06 e Instrument Serif são **banidas** (ver lista em [type-kits.md](type-kits.md)); Inter como display também.
- **Glow é opt-in do parti** (`superficie: glow-localizado`), nunca wallpaper incondicional em `body::before` (anti-pattern C8 — ver [anti-patterns.md](anti-patterns.md)).

---

## Features do engine v3 (reveal.js + slidev inspired)

### 1. Wake Lock
Impede tela de dormir durante apresentações. Automático — sem input do autor.
```js
// Já ativo no engine — não precisa fazer nada
// Re-adquire ao retornar ao foco (visibilitychange)
```

### 4. Overview Mode — tecla `O`
Grade miniaturizada de todos os slides. Clicar navega e fecha.

**Implementação correta (não usar font-size scaling):** Os slides em overview precisam preservar `clamp()` e unidades viewport (`vw`/`vh`). A técnica correta é:
1. Capturar `window.innerWidth/innerHeight` no `--slide-w` / `--slide-h` ao entrar em overview
2. Manter cada slide com width/height reais e aplicar `transform: scale(--ov-scale)`
3. Compensar com `margin-right/bottom: calc(var(--slide-w) * (var(--ov-scale) - 1))`
4. No overview, forçar todos os `[data-fragment]` e `[data-anim]` para `opacity:1, transform:none`

Tentar miniaturizar com `font-size: 0.35em` quebra porque `clamp()` e `vw` continuam resolvendo contra a janela inteira — o conteúdo overflowa ou desaparece.

```
O           → abrir/fechar overview
ESC         → fechar overview (ou sair de fullscreen)
Click slide → navegar + fechar
```
CSS: miniaturizar via `transform: scale(var(--ov-scale))` com snapshot do viewport em `--slide-w/--slide-h` (passo a passo acima) — **nunca** via `font-size` reduzido, que quebra com `clamp()`/`vw` (ver Pitfalls).

### 5. Auto-Animate — FLIP entre slides
Marcar slides adjacentes com `data-auto-animate`. Elementos com mesmo `data-id` animam suavemente entre posições via WAAPI FLIP.
```html
<!-- Slide A -->
<section class="slide" data-auto-animate>
  <h2 data-id="titulo" class="title-md">Resultado Q1</h2>
  <p data-id="valor" class="big-num__val">R$ 1,1 tri</p>
</section>

<!-- Slide B — o título encolhe, o valor cresce -->
<section class="slide" data-auto-animate>
  <h2 data-id="titulo" class="kicker">Resultado Q2</h2>
  <p data-id="valor" class="title-mega">R$ 1,19 tri</p>
</section>
```
Sem `data-auto-animate` nos slides → transição normal. Respeita `prefers-reduced-motion`.

### 6. Tipos de fragmento expandidos

| `data-fragment="..."` | Comportamento |
|---|---|
| *(sem valor)* | fade-in (padrão) |
| `current-visible` | aparece, fica em 30% opacity no próximo step |
| `highlight-current` | texto fica accent no step ativo, muted depois |
| `grow` | escala de 0.7→1 ao aparecer |
| `shrink` | escala de 1.3→1 ao aparecer |
| `fade-in-then-out` | aparece e some no próximo step |
| `strike` | text-decoration: line-through ao aparecer |

```html
<!-- Spotlight: um item por vez em destaque -->
<ul>
  <li data-fragment="current-visible">Ponto A</li>
  <li data-fragment="current-visible">Ponto B</li>
  <li data-fragment="current-visible">Ponto C</li>
</ul>
```

> **Tabelas não usam fragmentos.** Toda `.data-table` dentro de `.slide` ganha automaticamente hover apresentador-controlado pelo engine (ver § Tabelas com hover apresentador, abaixo). Forçar `highlight-current` linha-a-linha cria slides "fantasma" no contador e tira do apresentador a liberdade de destacar o que importa no momento.

### 7. Rough Notation — marcações manuais
CDN: `rough-notation@0.6.1` (já no template). Ativa ao entrar no slide ou via `data-mark-at`.

```html
<!-- Anota imediatamente ao entrar no slide -->
<p>AuM cresceu <strong data-mark="circle">R$ 1,19 tri</strong> em 2023</p>

<!-- Anota no fragmento de índice 2 -->
<p data-mark="highlight" data-mark-at="2" data-mark-color="#FF6200">
  Meta superada em todos os trimestres
</p>
```

Tipos: `underline` · `box` · `circle` · `highlight` · `strike-through` · `crossed-off` · `bracket`

### 9. AutoFitText
Escala o font-size para preencher o container. Ideal para títulos de comprimento variável.
```html
<h1 class="title-xl" data-fit-text>Título Que Pode Ser Qualquer Tamanho</h1>
```
Aplica ResizeObserver — re-calcula ao redimensionar viewport.

### 10. Tabelas com hover apresentador
Toda `.data-table` dentro de `.slide` ganha CSS automático no template: o apresentador passa o mouse sobre qualquer linha durante a apresentação — ela recebe background accent + texto bold; as demais linhas ficam com opacidade 0.4. Sem fragmentos, sem keyboard. O apresentador escolhe o que destacar, quando e em que ordem.

```html
<!-- Não precisa de fragmento nenhum. Mouse hover faz tudo. -->
<table class="data-table">
  <thead><tr><th>Fundo</th><th>Tipo</th><th class="num">AuM</th></tr></thead>
  <tbody>
    <tr><td>Asgard</td><td>RV Unconstrained</td><td class="num">R$ 18,5 bi</td></tr>
    <tr><td>Carbyne</td><td>Multimercado</td><td class="num">R$ 12,1 bi</td></tr>
    <tr><td>Eagle Polaris</td><td>RV Long Bias</td><td class="num">R$ 9,8 bi</td></tr>
  </tbody>
</table>
```

Comportamento: `tbody:hover tr { opacity: 0.4 }` + `tbody:hover tr:hover { opacity: 1; background: accent-dim; color: accent; font-weight: 700 }`. Respeita `prefers-reduced-motion` (sem transição). Não tem efeito por toque/keyboard — é desktop-first, porque deck é apresentado em desktop/fullscreen.

### 11. Posicionamento relativo de fragmentos
`data-fragment-index` com valores relativos: `+1`, `+2` em vez de índice absoluto.
```html
<!-- Absoluto (frágil ao reordenar) -->
<li data-fragment-index="1">Item A</li>
<li data-fragment-index="2">Item B</li>

<!-- Relativo (robusto) -->
<li data-fragment-index="1">Item A</li>
<li data-fragment-index="+1">Item B — sempre depois do anterior</li>
<li data-fragment-index="+1">Item C — sempre depois do B</li>
```

### 12. Layouts semânticos

| Classe | Uso | Estrutura |
|---|---|---|
| `layout-two-cols` | Comparativo, before/after | `.col-left` + `.col-right` |
| `layout-image-left` | Visual + texto | imagem à esq, texto à dir |
| `layout-image-right` | Texto + visual | texto à esq, imagem à dir |
| `layout-fact` | KPI gigante | `.fact-val` + `.fact-label` |
| `layout-quote` | Citação | `<blockquote>` + `<cite>` |
| `layout-statement` | One-liner de impacto | `.statement-text` |

```html
<!-- Two cols com fragmentos -->
<div class="layout-two-cols">
  <div class="col-left" data-fragment>
    <h3>Antes</h3><p>Conteúdo A</p>
  </div>
  <div class="col-right" data-fragment>
    <h3>Depois</h3><p>Conteúdo B</p>
  </div>
</div>

<!-- Fact — KPI gigante -->
<div class="layout-fact">
  <p class="fact-val" data-fit-text>14,5%</p>
  <p class="fact-label">market share da gestora</p>
</div>

<!-- Quote -->
<div class="layout-quote">
  <blockquote>"Democrática no acesso, sofisticada no modelo."</blockquote>
  <cite>— Carlos Augusto Salamonde, CIO</cite>
</div>
```

### 13. Code Stepping — `data-line-numbers`
Destaca grupos de linhas progressivamente. Cada `|` = um step (fragmento).
```html
<pre><code data-line-numbers="1-3|5-7|10">
aum      = 1_193_000_000_000  # linha 1
clientes = 2_600_000           # linha 2
share    = 14.5                # linha 3

def calc_share(aum, total):    # linha 5
    return aum / total * 100   # linha 6
    # retorna float             # linha 7

print(f"{share}%")             # linha 10
</code></pre>
```
`data-ln-start-from="10"` → numeração começa em 10 (útil para excerpts).

### 14. Background layers por slide
Cada `<section>` pode ter background próprio, animado independentemente do conteúdo.
```html
<!-- Slide de seção — fundo laranja sólido -->
<section class="slide" data-background-color="var(--itau-orange)">
  <p class="kicker" style="color:#fff">PARTE 02</p>
  <h2 class="title-xl" style="color:#fff">Modelo <em style="color:#fff">Multimesas</em></h2>
</section>

<!-- Slide com gradiente escuro atmosférico -->
<section class="slide" data-background-gradient="linear-gradient(135deg,#0d0a07,#1c1814)">
  <!-- conteúdo -->
</section>

<!-- Slide com imagem de fundo -->
<section class="slide" data-background-image="data:image/..." data-background-opacity="0.3">
  <!-- conteúdo sobre imagem esmaecida -->
</section>
```

---

## Atalhos de teclado (engine v3)

| Tecla | Ação |
|---|---|
| `→` / `Space` / `PageDown` | Próximo slide / fragmento |
| `←` / `PageUp` | Slide anterior |
| `Home` / `End` | Primeiro / último slide |
| `O` | Overview (grade de slides) |
| `F` | Fullscreen |
| `Escape` | Fechar overview / sair de fullscreen |
| `?` | Mostrar lista de atalhos |

---

## Regras do deck

1. **Tipografia gigante** — `clamp()` obrigatório (nunca px fixo). `.slide__display` = `clamp(48px, 10vw, 110px)`.
2. **Variar spatial approach** — a cada 3 slides centered, forçar um off-axis (split/left-heavy/full-bleed).
3. **Expansão vs compactação** — se fonte tem 10 slides com 4 elementos cada, gerar 14-18 slides slideless (não 1:1).
4. **Fragmentos** — usar `data-fragment` para revelar itens sequencialmente. Preferir `current-visible` para listas onde o contexto de cada item importa.
5. **Nenhum slide em branco** — cada slide carrega informação real da fonte. 0 slides de "logo" ou "encerramento" sem conteúdo.
6. **Gráfico quando há dado** — se o slide cita número que evoluiu no tempo, adicionar Chart.js. Se compara categorias, adicionar bar/donut.
7. **Tabela quando há lista comparativa** — mesas, fundos, diretoria, produtos → `<table>` com `.data-table`, nunca lista de bullets.
8. **Auto-Animate em slides de evolução** — usar `data-auto-animate` + `data-id` quando o mesmo elemento muda de tamanho/posição entre slides consecutivos.
9. **Rough Notation em KPIs** — `data-mark="circle"` em números-âncora e `data-mark="underline"` em termos-chave de slides de quote/statement.
10. **Background por slide de seção** — slides divisores usam `data-background-color="var(--itau-orange)"` (tema itaú) em vez de só mudar tipografia.

---

## Pitfalls conhecidos do engine (NUNCA repetir)

### Tabelas com fragmentos
**Errado:** aplicar `data-fragment` (qualquer tipo, incluindo `highlight-current`) em `<tr>` para percorrer linhas via teclado. Cria slides "fantasma" no contador, força ordem pré-definida, e tira do apresentador o controle sobre o que destacar quando.

**Correto:** o template já aplica hover apresentador-controlado em toda `.data-table` dentro de `.slide`. O apresentador passa o mouse sobre uma linha durante a apresentação — ela ganha background accent + bold, demais ficam muted. Sem fragmentos, sem keyboard. Ver § Tabelas com hover apresentador.

```html
<!-- ❌ ERRADO: força ordem, gasta steps de navegação -->
<tr data-fragment="highlight-current"><td>Linha A</td>...</tr>
<tr data-fragment="highlight-current"><td>Linha B</td>...</tr>

<!-- ✅ CERTO: tabela completa, apresentador controla com o mouse -->
<tr><td>Linha A</td>...</tr>
<tr><td>Linha B</td>...</tr>
```

### Grid de fios (hairline) com reveal por opacidade — bloco cinza fantasma
**Sintoma:** um slide com `.grid-cards` (ou qualquer grid de "fios") mostra um **retângulo cinza sólido** no lugar dos cards, em vez do conteúdo.

**Causa-raiz:** a técnica de fios pinta o **fundo do container** (`background: var(--color-border)`) com `gap: 1px` — são os **fundos dos cards** (`background: var(--color-bg)`) que cobrem esse cinza, deixando só as linhas de 1px. Quando os cards recebem reveal por **opacidade** (`data-fragment` de qualquer tipo, ou `data-anim`), em `opacity: 0` o fundo do card some e o **fundo cinza do grid aparece inteiro** = o bloco cinza.

**Correto:** nunca combinar reveal-por-opacidade nos **cards** de um grid de fios. Escolher uma:
- revelar o **container** (`data-anim` no `.grid-cards`), não cada card — os cards entram juntos sobre os fios;
- se precisar de stagger por card, usar grid com `gap` normal e cards com borda/fundo próprios (não a técnica de fios), de modo que `opacity:0` exponha o bg do slide, não um fundo pintado;
- ou animar só o **conteúdo** do card, mantendo o card opaco.

```html
<!-- ❌ ERRADO: cards de um grid de fios revelados por opacidade -->
<div class="grid-cards grid-cards--3">   <!-- background: var(--color-border); gap:1px -->
  <div class="card-d" data-fragment="current-visible">…</div>   <!-- opacity:0 → expõe o cinza -->
</div>

<!-- ✅ CERTO: revela o container; cards aparecem juntos sobre os fios -->
<div class="grid-cards grid-cards--3" data-anim>
  <div class="card-d">…</div>
</div>
```

### Slide-num colidindo com título (REGRA CANÔNICA)

**NUNCA posicionar `.slide-num` no canto top-left.** Esse é o canto onde kicker e título vivem (slides com `justify-content: center` podem ter conteúdo alto que overflowa para a área superior, sobrepondo o slide-num). Tentativas com `backdrop-filter`, `z-index` alto e background sólido falham porque o background (`--color-bg-elevated`) costuma ser quase idêntico ao bg do slide no tema itaú (ambos cream).

**Posição canônica:** `bottom: 18px; right: 28px` — page-number style, sem badge nem fundo, só texto monospace com `opacity: 0.55`. O HUD fixo no bottom-center não conflita. Conteúdo do slide nunca atinge o canto inferior-direito em layouts centered.

```css
.slide-num {
  position: absolute;
  bottom: 18px; right: 28px;
  font: 600 0.6875rem/1 var(--font-mono);
  letter-spacing: 0.12em;
  color: var(--color-fg-muted);
  opacity: 0.55;
  z-index: 30;
  pointer-events: none;
  user-select: none;
}
.slide-num span { color: var(--color-accent); font-weight: 700; }

/* Em slides com background escuro/laranja, contraste claro */
.slide[data-background-color="#000000"] .slide-num,
.slide[data-background-color="#000"] .slide-num,
.slide[data-background-color*="orange"] .slide-num {
  color: rgba(255,255,255,0.75);
}
```

Padding do `.slide`: `clamp(64px, 8vh, 90px)` no topo + `clamp(56px, 7vh, 80px)` no bottom — espaço respiratório para conteúdo, sem necessidade de safe-area específica para slide-num (já não está no topo).

### Overview com font-size scaling
**Errado:** `body.is-overview .slide { font-size: 0.35em; }`. Em viewports com `clamp()` e `vw/vh`, esses valores continuam resolvendo contra a janela inteira (não contra o thumbnail) — conteúdo overflowa ou desaparece.

**Correto:** snapshot do viewport real em CSS variables (`--slide-w`, `--slide-h`) ao entrar em overview; `transform: scale(--ov-scale)` no slide com `transform-origin: top left`; compensar com `margin-right/bottom` negativo proporcional. No overview, forçar todos os `[data-fragment]` e `[data-anim]` a `opacity:1`.

### Título vazando do slide (overflow horizontal/vertical)
**Sintoma:** título `.title-mega` ou `.fact-val` excede a viewport — texto cortado pela borda, conteúdo escondido atrás da HUD. Acontece com clamps puro-`vw` em viewports baixos (notebook 1366×768 ou ultrawide curto).

**Causa-raiz:** clamps que só escalam por `vw` ignoram a altura disponível. Em ultrawide (2511×914), `vw` gera tipo gigante mas a altura é insuficiente para múltiplas linhas.

**Correto:** clamps incluem ambos `vw` **e** `vh`:
```css
--size-mega: clamp(2.75rem, 1.6rem + 2.4vw + 2vh, 5.5rem);
--size-giga: clamp(3.5rem, 2rem + 3vw + 3vh, 9rem);
```
Plus o template aplica:
- CSS guard: `.slide { contain: layout paint }` + `.slide > *:not(.slide-bg):not(.slide-num) { max-width: 100%; min-width: 0 }`
- JS `autoFitSlide(slide)` ao virar slide ativo: reduz iterativamente o font-size dos títulos (`.title-mega/xl/lg`, `.fact-val`, `.statement-text`, `.quote-text`, `.big-num__val`) até o conteúdo caber. Idempotente (reseta inline antes de medir). Re-executa em `resize`.
- Console warning `[slideless] slide N overflows even after autoFitSlide` quando nem o autoFit resolve — indica que o gerador colocou texto demais em uma classe gigante.

**Char limits** (respeitar antes de gerar):
| Classe | Limite | Se exceder |
|---|---|---|
| `.title-mega` / `.fact-val` / `.statement-text` | ≤ 50 chars | Dividir em 2 elementos ou usar `.title-lg` |
| `.title-xl` | ≤ 70 chars | Trocar para `.title-lg` |
| `.title-lg` | ≤ 90 chars | Trocar para `.title-md` |
| `.lead-deck` | ≤ 220 chars | Quebrar em duas frases |

---

## Checklist deck

- [ ] Slide engine funciona (navegação teclado, dots, counter, fullscreen)?
- [ ] Wake Lock ativo (tela não dorme)?
- [ ] Overview mode funciona (tecla O)?
- [ ] Progress bar atualiza?
- [ ] Tipografia usa `clamp()`?
- [ ] Variedade de layouts (pelo menos 5 tipos, incluindo semânticos)?
- [ ] Fragments onde há itens sequenciais — com tipos corretos (current-visible em listas)?
- [ ] Tabelas **sem** fragmentos linha-a-linha (hover apresentador faz o destaque)?
- [ ] Auto-Animate em slides de evolução numérica?
- [ ] Rough Notation em KPIs e citações-chave?
- [ ] Dark mode sem flash?
- [ ] Overview (tecla O) rola quando há mais slides do que cabem no viewport?
- [ ] **Nada vaza da viewport** em 1366×768 (notebook baixo)? Sem warning `[slideless] slide N overflows` no console?
- [ ] Títulos respeitam char limits (mega ≤50, xl ≤70, lg ≤90, lead ≤220)?
- [ ] Conteúdo 100% da fonte (nada omitido)?
- [ ] Gráficos onde há dados temporais/comparativos?
- [ ] Tabelas onde há listas de itens com atributos?
> **Pitfall (v7):** `data-fragment="current-visible"` é spotlight — mostra UM item por vez e some no load. NÃO usar em conteúdo que precisa aparecer inteiro (comparação antes/depois, duas colunas de info). Reservar para listas onde revelar-um-a-um é intencional.
