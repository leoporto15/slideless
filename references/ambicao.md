# Ambição — o teto cutting-edge

> A **7ª decisão do parti** ([direcao-de-arte.md](direcao-de-arte.md)). Onde o registro decide *como o documento soa*, a ambição decide *quão longe o craft vai*. São eixos ortogonais: um relatório regulatório pode ser sóbrio E extraordinário. Este arquivo é o vocabulário fechado de gestos ambiciosos — cada um copiável, com fallback obrigatório. O LLM **copia**, não inventa.

---

## O eixo

```
ambicao: <A1-contido | A2-elevado | A3-extraordinario> + o elemento da fonte que justifica o nível
```

| Nível | Quando | Vocabulário liberado |
|---|---|---|
| **A1 contido** | report, regulatório, runbook, qualquer PDF; ou quando o conteúdo não pede mais | = v4. Motion estático/editorial, flat, materialidade por fio. |
| **A2 elevado** | **default** de deck, scrollytelling, hub, site, handbook | Materialidade de assinatura, springs `linear()`, scroll-driven, tipografia cinética, ≥1 momento-wow data-bound, transição contínua entre estados. **Tudo degradável.** |
| **A3 extraordinario** | showcases, lançamentos, all-hands de impacto — só com conteúdo à altura | + WebGL/minigl, variable font animada plena, cursor-proximity, conic glow, cinematic transitions. Opt-in explícito. |

**Derivação obrigatória:** cite o elemento da fonte que justifica o nível ("a curva de adoção do Pix é a própria história → A2 com cena scroll-driven no gráfico"). Sem justificativa = rejeitado, igual às outras decisões do parti.

## Trava de coerência — a ambição respeita o registro como teto de exuberância

| Registro | Ambição | A2 permite | A2/A3 proíbe |
|---|---|---|---|
| `institucional-impresso`, `relatorio-de-bancada` | A1 default; **A2 só sóbrio**; **A3 proibido** (falha P10) — exceção: `/overdrive` opt-in deliberado (`data-overdrive`) é showcase ao vivo consciente | materialidade por fio, grain estático, duotone mono, anotação viva no gráfico (W8), text reveal contido (W6) | spring bouncy, cursor-proximity, WebGL, conic glow, aurora saturada |
| `tecnico-preciso` | A2 default | materialidade de blueprint (grid/scanline animado), scroll scenes | exuberância cromática |
| `revista-interna`, `poster-de-auditorio`, `condensado-noticioso` | A2 cheio; A3 com conteúdo à altura | tudo de A2; A3 sob aprovação | — |

Um report A2 fica **materialmente mais rico, nunca mais saltitante**.

---

## Os 3 invariantes de segurança (inegociáveis em todo W)

1. **Reduced-motion sempre.** Todo movimento dentro de `@media (prefers-reduced-motion: no-preference)` ou com branch `reduce`. Reduced = animação *mais gentil* (fade curto ok), não necessariamente zero; movimento de `transform` vira opacity ou estático.
2. **`@supports` + estado-final-base.** Toda feature de ponta dentro de `@supports`, com o **estado final visível como CSS base**. Num Chrome travado, o documento nunca quebra. **Nunca esconder no base e revelar só na animação** — senão num browser sem a feature o conteúdo some.
3. **Só compositado.** Animar apenas `transform`/`opacity`. `@property`/gradiente/blur só em áreas pequenas (borda, badge, hero pontual), nunca em fullscreen com scroll.

---

## Vocabulário de momentos-wow (W1-W9)

Cada documento A2 entrega **≥1** ligado ao dado-tese. A3 pode empilhar. Declarar no parti qual W e onde.

### W1 — Cena scroll-driven (pin + N estados data-bound)
O visual fica fixo enquanto o texto passa por N estados, cada um mutando o visual. A espinha do scrollytelling de elite.
```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .scene-layer { animation: rise linear both; animation-timeline: view(); animation-range: entry 0% cover 50%; }
    @keyframes rise { from { opacity:.3; transform: translateY(40px); } to { opacity:1; transform: none; } }
  }
}
```
O "step ativo" que muta o gráfico/cena é o único JS (IO com `rootMargin:'-50% 0px'`), **já existe no template-scrollytelling**. **Fallback:** sem `@supports`, layers ficam no estado final (base CSS `opacity:1`); o IO continua dirigindo as mutações do gráfico.

### W2 — Número + elemento sincronizados (counter cresce junto da barra)
O número-tese conta de 0 ao valor real **enquanto** a barra que o representa cresce — não isolados.
```css
@property --n { syntax:'<integer>'; inherits:false; initial-value:0; }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .kpi { counter-reset: n var(--n); animation: count linear both; animation-timeline: view(); animation-range: entry 20% cover 50%; }
    .kpi::after { content: counter(n); }
    .kpi .bar { transform: scaleX(0); transform-origin:left; animation: grow linear both; animation-timeline: view(); animation-range: entry 20% cover 50%; }
    @keyframes count { to { --n: 3200; } }
    @keyframes grow  { to { transform: scaleX(1); } }
  }
}
```
**Fallback:** o número final em texto real no HTML (não só `::after`) + barra em `scaleX(1)` no base. Reduced-motion: idem.

### W3 — Manchete cinética (eixo da variable font se constrói)
A manchete-tese engorda/expande no eixo da fonte conforme entra na viewport. **Colhe os eixos `wdth`/`SOFT/WONK`/`GRAD` que os kits 05/06 já pagam e hoje usam estático.**
```css
@property --wght { syntax:'<number>'; inherits:false; initial-value:300; }
.kinetic-wrap { view-timeline-name:--mh; view-timeline-axis:block; overflow:clip; } /* NUNCA overflow:hidden — congela a timeline */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .kinetic-h { animation: typeflex linear both; animation-timeline:--mh; animation-range: entry 10% cover 55%;
      font-variation-settings:'wght' var(--wght); }
    @keyframes typeflex {
      from { font-variation-settings:'wght' 220,'wdth' 80; letter-spacing:.06em; opacity:.4; }
      to   { font-variation-settings:'wght' 880,'wdth' 125; letter-spacing:-.02em; opacity:1; }
    }
  }
}
```
**Fallback:** `.kinetic-h { font-variation-settings:'wght' 800; }` no base (estado final, legível). Reduced-motion idem.

### W4 — Cursor-proximity na manchete-tese (A3, ou A2 expressivo — nunca sóbrio)
Cada letra reage à distância do ponteiro. O efeito que mais grita "não é template".
```js
const seg = new Intl.Segmenter('pt', { granularity:'grapheme' });  // preserva acentos pt-BR
el.innerHTML = [...seg.segment(el.textContent)].map(s => s.segment===' '?' ':`<span class="ch">${s.segment}</span>`).join('');
const chars=[...el.querySelectorAll('.ch')], R=140, from=[['wght',200]], to=[['wght',900]];
let mx=-1e4,my=-1e4,tick=false;
addEventListener('pointermove',e=>{mx=e.clientX;my=e.clientY;if(!tick){tick=true;requestAnimationFrame(up);}});
function up(){ tick=false; for(const c of chars){ const r=c.getBoundingClientRect();
  const t=Math.max(0,1-Math.hypot(mx-(r.left+r.width/2),my-(r.top+r.height/2))/R);
  c.style.fontVariationSettings=from.map(([tag,f],i)=>`"${tag}" ${(f+(to[i][1]-f)*t).toFixed(0)}`).join(','); } }
```
```css
@media (hover:hover) and (pointer:fine) { /* só desktop com mouse */ }
@media (prefers-reduced-motion: reduce) { .ch { font-variation-settings:'wght' 500 !important; } }
```
**Fallback:** peso médio estático; só ativa em `hover:hover`+`pointer:fine`; desliga em reduced-motion.

### W5 — Transição contínua entre estados (morph)
Trocar view/painel deixa de ser corte seco. View Transitions (sem framework) ou o FLIP da engine v3 (já existe).
```js
function navigate(updateDOM) {
  if (!document.startViewTransition || matchMedia('(prefers-reduced-motion: reduce)').matches) { updateDOM(); return; }
  document.startViewTransition(updateDOM);
}
```
```css
.card-hero  { view-transition-name: hero; }   /* o card... */
.panel-hero { view-transition-name: hero; }   /* ...vira o header do painel (morph automático) */
@media (prefers-reduced-motion: reduce) { ::view-transition-group(*){ animation:none !important; } }
```
**Fallback:** o guard `if (!document.startViewTransition)` faz a troca instantânea. `view-transition-name` único por snapshot (dois iguais simultâneos = erro). Encaixe perfeito: `site` (views), `hub` (painéis).

### W6 — Text reveal editorial (linha/palavra sobe de dentro)
Split nativo com `Intl.Segmenter` (sem GSAP), reveal por scroll.
```js
const seg=new Intl.Segmenter('pt',{granularity:'word'});
el.innerHTML=[...seg.segment(el.textContent)].map(s=>s.isWordLike?`<span class="w"><span class="w-i">${s.segment}</span></span>`:s.segment).join('');
```
```css
.w{ display:inline-block; overflow:clip; vertical-align:top; } .w-i{ display:inline-block; }
@supports (animation-timeline: view()) { @media (prefers-reduced-motion: no-preference) {
  [data-split]{ view-timeline-name:--r; view-timeline-axis:block; }
  .w-i{ animation: riseword linear both; animation-timeline:--r; animation-range: entry 0% entry 70%; animation-delay: calc(var(--i,0)*50ms); }
  @keyframes riseword{ from{ transform:translateY(110%); } to{ transform:none; } }
}}
```
Variantes (trocar só o keyframe): clip wipe (`clip-path:inset(0 100% 0 0)→0`), blur-in (`filter:blur(12px);opacity:0→0`). **Fallback:** `.w-i` base `transform:none` (texto visível).

### W7 — Superfície de assinatura (UMA por documento — ver §Materialidade)
Aurora mesh / grain animado / borda de luz / glass. Escolher 1, ligar ao tom do assunto. **Fallback:** estático/sólido (a própria aurora CSS é o fallback dos efeitos caros).

### W8 — Anotação viva no gráfico-tese (generaliza o annoPlugin que JÁ existe)
A banda de evento / leader-line / crosshair acende no scroll ou hover, no ponto que o texto narra. É o craft do FT/NYT.
```js
// plugin Chart.js: lê um objeto `anno` mutável e desenha banda + label no afterDatasetsDraw.
// O exemplo-scrollytelling canônico já tem isto (annoPlugin) — generalizar para todos os charts-tese.
// Crosshair de leitura no hover: onHover lê o índice e desenha linha vertical + valor.
```
**Fallback:** anotação estática desenhada no primeiro render (sem depender de scroll/hover).

### W9 — Hero material (A3 apenas)
Stripe **minigl** (~5KB standalone inline, NÃO Three.js) ou conic glow `@property`. **Fallback obrigatório:** detecta WebGL; sem ele → aurora CSS (§Materialidade) com as mesmas cores.
```js
const gl = document.createElement('canvas').getContext('webgl');
if (gl && !matchMedia('(prefers-reduced-motion: reduce)').matches) { new Gradient().initGradient('#hero-canvas'); }
else { document.getElementById('hero-canvas').classList.add('aurora-fallback'); }
```

---

## Materialidade — os 4 "premium baratos" (0KB, fallback gracioso)

Base de quase todo documento **não-report**. Receitas completas em [css-patterns.md](css-patterns.md) §13. Resumo:
1. **Aurora mesh** — 2-4 `radial-gradient` borrados animados em `background-position` (durações distintas). É o próprio fallback.
2. **Grain `feTurbulence`** — SVG data-URI, `mix-blend-mode:soft-light`, `opacity .04-.08`, `pointer-events:none`. Animado: `steps()`.
3. **Borda de luz 1px + glow** — border gradiente (`padding-box`/`border-box` mask) + `box-shadow` em camadas (specular inset + depth).
4. **Glass com fallback** — `backdrop-filter:blur() saturate()` + specular; `@supports not`→sólido. Máx 3-5 painéis/viewport, nunca animar o blur.

**Tier A (assinatura, custo médio):** progressive blur (Apple/Family — só header/footer), conic `@property` glow (1-2/doc), Stripe minigl (A3). **report:** só grain estático sutil + specular 1px. Nada animado.

---

## A régua de craft invisível (o maior multiplicador — aplica em TODA ambição, inclusive A1)

O que faz "parecer caro" não é o efeito, é a execução (Emil Kowalski / Rauno / Family):

- **Durações:** botão 100-160ms · tooltip 125-200 · dropdown 150-250 · modal/tray 200-500. **Teto 300ms para UI.**
- **Curvas nomeadas (nunca as default):** `--ease-out-strong: cubic-bezier(0.23,1,0.32,1)` (entrada/saída) · `--ease-io-strong: cubic-bezier(0.77,0,0.175,1)` (morph) · `--spring` via `linear()` (gerar e tokenizar, fallback `cubic-bezier(0.34,1.56,0.64,1)`).
- **Entrada lenta / saída rápida.** Nunca anime de `scale(0)` (use 0.95-0.97). Valores proporcionais ao gatilho.
- **Origem espacial:** painel escala a partir do botão que o abriu (`transform-origin`), não do centro.
- **Frequência manda:** hover de linha de tabela densa (100×/dia) = sem animação; momento raro (capa, 1ª dobra) = delight liberado.
- **Toggle de tema NÃO dispara transitions:** `.no-transitions` no `<html>` durante o switch (senão a página inteira "respira" no dark/light). Aplicar no boot script.
- **Dropdown abre no `mousedown`.** Optimistic UI: feedback no local do gatilho.

```js
// no-transitions no toggle (boot script): evita o "respiro" da página inteira
function setTheme(t){ const h=document.documentElement; h.classList.add('no-transitions');
  h.setAttribute('data-theme',t); requestAnimationFrame(()=>requestAnimationFrame(()=>h.classList.remove('no-transitions'))); }
```
```css
.no-transitions *, .no-transitions *::before, .no-transitions *::after { transition: none !important; }
```

---

## Checklist de saída A2/A3 (some ao checklist do parti)

- [ ] `ambicao:` declarado e coerente com o registro (A3 fora de regulatório = falha)
- [ ] ≥1 momento-wow (W#) ligado ao **dado-tese**, não decorativo
- [ ] Cada gesto de ponta tem `@supports` + estado-final-base (P9)
- [ ] Reduced-motion: branch presente em todo movimento
- [ ] Régua de craft: curvas nomeadas, teto 300ms, `.no-transitions` no toggle
- [ ] Materialidade respeita o registro (report = grain estático; nada de glass/WebGL)
- [ ] Teste do "parar o scroll": algum momento faria um diretor de arte parar?
