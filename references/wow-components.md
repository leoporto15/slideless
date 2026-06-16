# Wow Components — a caixa de peças (drop-ins copy-paste)

> **O que é:** o repertório de momentos-wow como **blocos completos, prontos para colar verbatim** — nada para montar. Onde [`ambicao.md`](ambicao.md) é a *doutrina* (eixo A1/A2/A3, invariantes, quando usar) e [`css-patterns.md`](css-patterns.md) §13 é o *índice conceitual*, **este arquivo é o código**. O LLM **copia daqui**, não improvisa cutting-edge do zero (improviso de ponta é frágil → vira tímido ou quebra na intranet).
>
> **Por que existe:** o gargalo do "bonito mas decente" nunca foi falta de vocabulário — era que os momentos-wow viviam como *fragmentos de técnica* que exigiam integração (o `@property`, o estado-final-base, o `@supports`, o branch reduced-motion). O LLM fazia tímido ou pulava. Aqui cada bloco já vem com toda a fiação perigosa correta.

## Como usar

1. O parti (`ambicao` A2/A3 + campo `momento-wow:`) decide **quais** W# entram e **onde** (ligados ao dado-tese, não decorativos).
2. Copiar o bloco inteiro — HTML + CSS + JS — sem editar a fiação. Trocar só o **payload** (texto da manchete, número real, série do gráfico).
3. O validador (`scripts/validar.py`, P8) credita a técnica pela *signature* indicada em cada bloco. Grain/aurora/glass **não** quitam ambição — são materialité (`superficie`).

## Os 3 invariantes (já embutidos em cada bloco — não remover)

1. **Reduced-motion sempre** — todo movimento dentro de `@media (prefers-reduced-motion: no-preference)` ou com branch `reduce`.
2. **`@supports` + estado-final-base** — o estado final é o CSS base; a animação só *acontece* dentro do `@supports`. Num Chrome travado nada some.
3. **Só compositado** — animar apenas `transform`/`opacity` (e `font-variation-settings`/`clip-path` em áreas pequenas). Nunca fullscreen + scroll em propriedade cara.

## Régua de craft (aplica a TODOS os blocos)

Durações: botão 100-160ms · tooltip 125-200 · dropdown 150-250 · modal 200-500. **Teto 300ms para UI** (momento-hero pode ir a ~600-900ms). Curvas nomeadas, nunca default: `--ease-out-strong: cubic-bezier(0.23,1,0.32,1)`, `--ease-io-strong: cubic-bezier(0.77,0,0.175,1)`. Helper usado pelos plugins de Chart.js:

```js
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
```

---

# W1 — Cena scroll-driven (pin + N estados data-bound)

**[A2/A3 · scrollytelling, handbook]** A espinha do scrollytelling de elite: o visual fica fixo enquanto o texto passa por N estados, cada um mutando o gráfico/cena.

- **GANCHO:** `.scene-layer` (camadas que sobem) + um sticky `.story__chart` + IO que lê `data-step`.
- **DADO-TESE:** cada step muta o gráfico para um ponto real da série (não animação decorativa).

```css
/* --- COLAR INTEGRAL (CSS) --- */
.scene-layer { opacity: 1; transform: none; }                 /* INVARIANTE 2: base = final */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .scene-layer {
      animation: sceneRise linear both;
      animation-timeline: view();
      animation-range: entry 0% cover 50%;
    }
    @keyframes sceneRise { from { opacity: .3; transform: translateY(40px); } to { opacity: 1; transform: none; } }
  }
}
```

```js
/* --- COLAR INTEGRAL (JS): o "step ativo" muta a cena (único JS necessário) --- */
const stepIO = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const step = e.target.dataset.step;          // ex.: "2"
    applyStep(step);                              // muta o gráfico/cena para o estado real
  });
}, { rootMargin: '-50% 0px -50% 0px', threshold: 0 });
document.querySelectorAll('[data-step]').forEach(s => stepIO.observe(s));
```

**FALLBACK:** sem `@supports`, as camadas ficam no estado final (base `opacity:1`); o IO continua dirigindo as mutações do gráfico.
**VALIDADOR:** satisfaz P8 com signature `W1/W6-scroll-driven` (precisa de `@supports (animation-timeline: ...)` → P9).
**NÃO FAÇA:** `overflow:hidden` no ancestral (congela a timeline — usar `overflow:clip`); esconder a camada no base e revelar só na animação.

---

# W2 — Número-tese + elemento sincronizados (counter cresce junto da barra)

**[A2/A3 · deck, scrollytelling, hub]** O número conta de 0 ao valor real **enquanto** a barra que o representa cresce — nunca isolados.

- **GANCHO:** `.kpi` com `.kpi__bar` interna.
- **DADO-TESE:** o número-tese e sua régua de magnitude.

```css
/* --- COLAR INTEGRAL (CSS) --- */
@property --n { syntax: '<integer>'; inherits: false; initial-value: 0; }
.kpi__bar { transform: scaleX(1); transform-origin: left; }    /* INVARIANTE 2: base = cheia */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .kpi { counter-reset: n var(--n); animation: kpiCount linear both;
           animation-timeline: view(); animation-range: entry 20% cover 50%; }
    /* CRÍTICO: o texto real só pode existir OU como nó OU como counter, nunca os
       dois — senão renderiza "32003200". Aqui escondemos o texto-base e mostramos
       o counter animado; fora do @supports, o texto-base reaparece sozinho. */
    .kpi__num-base { display: none; }
    .kpi__num::after { content: counter(n); }                  /* só o miolo numérico */
    .kpi__bar { transform: scaleX(0); animation: kpiGrow linear both;
                animation-timeline: view(); animation-range: entry 20% cover 50%; }
    @keyframes kpiCount { to { --n: 3200; } }                  /* trocar 3200 pelo valor real */
    @keyframes kpiGrow  { to { transform: scaleX(1); } }
  }
}
```

```html
<!-- --- COLAR INTEGRAL (HTML) --- payload: o número final EM TEXTO REAL dentro de .kpi__num-base -->
<div class="kpi"><span class="kpi__num"><span class="kpi__num-base">3.200</span></span><span class="kpi__bar"></span></div>
```

**FALLBACK:** o número final em texto real no `.kpi__num-base` (visível sem `@supports`/reduced-motion) + barra em `scaleX(1)` no base.
**VALIDADOR:** satisfaz P8 com signature `W2-counter-sync`.
**NÃO FAÇA:** ter o número como nó de texto direto E `::after { content: counter }` ao mesmo tempo (renderiza duplicado "7070"); deixar o número só no `::after` sem `.kpi__num-base` (some sem suporte); animar a `width` (use `transform: scaleX`).

---

# W3 — Manchete cinética (eixo da variable font se constrói) ★ código provado (deck.html)

**[A2/A3 · deck, poster, capa de scrollytelling]** A manchete-tese engorda/expande no eixo da fonte conforme entra. Colhe os eixos `opsz`/`wght`/`wdth` que os kits já pagam e hoje usam estático.

- **GANCHO:** `.kinetic-h` (no `<h1>` da capa) dentro de `.kinetic-wrap`.
- **DADO-TESE:** a manchete da fonte (não decorativo).

```css
/* --- COLAR INTEGRAL (CSS) --- (Kit 01 Newsreader: opsz+wght; ajustar eixos ao kit) */
.kinetic-wrap { overflow: clip; display: block; }
.kinetic-h {
  font-optical-sizing: none;                                   /* o eixo é dirigido pela animação */
  font-variation-settings: 'opsz' 72, 'wght' 800;             /* INVARIANTE 2: base = final legível */
}
@supports (font-variation-settings: 'opsz' 12) {
  @media (prefers-reduced-motion: no-preference) {
    .slide.is-active .kinetic-h { animation: kineticType var(--duration-hero, 760ms) var(--ease-out-strong) 60ms both; }
    @keyframes kineticType {
      from { font-variation-settings: 'opsz' 6,  'wght' 340; opacity: .55; }
      to   { font-variation-settings: 'opsz' 72, 'wght' 800; opacity: 1; }
    }
  }
}
```

```html
<!-- --- COLAR INTEGRAL (HTML) --- -->
<div class="kinetic-wrap"><h1 class="title-xl kinetic-h">{MANCHETE-TESE}</h1></div>
```

> **Fora do deck** (scrollytelling/handbook, sem `.is-active`): trocar o gatilho por `view-timeline` —
> `.kinetic-wrap{ view-timeline-name:--mh; view-timeline-axis:block; }` e `.kinetic-h{ animation-timeline:--mh; animation-range: entry 10% cover 55%; }`.

**FALLBACK:** `.kinetic-h` base já no estado final (peso 800, legível). Reduced-motion idem.
**VALIDADOR:** satisfaz P8 com signature `W3-kinetic-headline`.
**NÃO FAÇA:** `letter-spacing` whiplash junto; animar `wdth` em fonte que não tem o eixo (Newsreader não tem); `overflow:hidden` no wrap.

---

# W5 — Transição contínua entre estados (morph via View Transitions) ★ ideal p/ site, hub

**[A2/A3 · site, hub]** Trocar view/painel deixa de ser corte seco: o elemento-herói faz morph automático.

- **GANCHO:** o helper `navigate()` envolve o swap de DOM da rota/painel.
- **DADO-TESE:** o card que vira o cabeçalho do painel (continuidade do mesmo objeto).

```js
/* --- COLAR INTEGRAL (JS) --- envolver toda troca de view/painel com navigate() --- */
function navigate(updateDOM) {
  if (!document.startViewTransition || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    updateDOM(); return;                                       // FALLBACK: troca instantânea
  }
  document.startViewTransition(updateDOM);
}
```

```css
/* --- COLAR INTEGRAL (CSS) --- nomear o par que faz morph (único por snapshot) --- */
.card-hero  { view-transition-name: hero; }                    /* o card... */
.panel-hero { view-transition-name: hero; }                    /* ...vira o header do painel */
@media (prefers-reduced-motion: reduce) { ::view-transition-group(*) { animation: none !important; } }
```

**FALLBACK:** o guard `if (!document.startViewTransition)` faz a troca instantânea.
**VALIDADOR:** satisfaz P8 com signature `W5-view-transition` (sem guard → P9-view-transition-sem-guard).
**NÃO FAÇA:** dois `view-transition-name` iguais simultâneos (erro); animar layout pesado no morph.

---

# W6 — Text reveal editorial (palavra/linha sobe de dentro)

**[A2 · handbook, scrollytelling]** O "uau" calmo: split nativo com `Intl.Segmenter` (sem GSAP), reveal por scroll. Preserva acentos pt-BR.

- **GANCHO:** `[data-split]` no elemento (lead/h2); o JS injeta `.w`/`.w-i`.

```js
/* --- COLAR INTEGRAL (JS) --- split grapheme-safe pt-BR --- */
document.querySelectorAll('[data-split]').forEach(el => {
  const seg = new Intl.Segmenter('pt', { granularity: 'word' });
  el.innerHTML = [...seg.segment(el.textContent)]
    .map(s => s.isWordLike ? `<span class="w"><span class="w-i">${s.segment}</span></span>` : s.segment).join('');
});
```

```css
/* --- COLAR INTEGRAL (CSS) --- */
.w { display: inline-block; overflow: clip; vertical-align: top; }
.w-i { display: inline-block; transform: none; }               /* INVARIANTE 2: base = visível */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    [data-split] { view-timeline-name: --r; view-timeline-axis: block; }
    .w-i { animation: riseWord linear both; animation-timeline: --r;
           animation-range: entry 0% entry 70%; animation-delay: calc(var(--i,0) * 50ms); }
    @keyframes riseWord { from { transform: translateY(110%); } to { transform: none; } }
  }
}
```

**Variantes** (trocar só o keyframe): clip wipe (`clip-path: inset(0 100% 0 0)→0`), blur-in (`filter: blur(12px); opacity:0 → 0/1`).
**FALLBACK:** `.w-i` base `transform:none` (texto visível).
**VALIDADOR:** satisfaz P8 com signature `W4/W6-segmenter` (+ `W1/W6-scroll-driven`).
**NÃO FAÇA:** `overflow:hidden` (congela timeline — usar `clip`); usar em texto longo de corpo (só lead/títulos).

---

# W8 — Anotação viva no gráfico-tese (banda/leader-line/marcador) ★ código provado (scrollytelling.html)

**[A2/A3 · qualquer gráfico-tese]** O craft do FT/NYT: a banda de evento / marcador de inflexão acende no ponto que o texto narra. Plugin Chart.js que lê estado mutável por-gráfico.

- **GANCHO:** registrar o plugin; mutar `BAND[canvasId]` por step/hover e chamar `chart.update()`.
- **DADO-TESE:** o período/ponto que o texto está narrando.

```js
/* --- COLAR INTEGRAL (JS) --- estado por-gráfico em BAND[id]; o gráfico NUNCA é destruído --- */
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const BAND = {};
const annoPlugin = {
  id: 'annoPlugin',
  beforeDatasetsDraw(chart) {
    const st = BAND[chart.canvas.id];
    if (!st || !st.band) return;
    const { ctx, chartArea, scales: { x } } = chart;
    const x1 = x.getPixelForValue(st.band.from), x2 = x.getPixelForValue(st.band.to);
    if (isNaN(x1) || isNaN(x2)) return;
    ctx.save();
    ctx.fillStyle = css('--color-warn-dim');
    ctx.fillRect(x1, chartArea.top, x2 - x1, chartArea.bottom - chartArea.top);
    ctx.font = '700 11px ' + Chart.defaults.font.family;
    ctx.fillStyle = css('--color-fg-muted');
    ctx.fillText(st.band.text, x1 + 6, chartArea.top + 14);
    ctx.restore();
  },
  afterDatasetsDraw(chart) {
    const st = BAND[chart.canvas.id];
    if (!st || !st.mark) return;
    const { ctx, scales: { x, y } } = chart;
    const px = x.getPixelForValue(st.mark.x), py = y.getPixelForValue(st.mark.y);
    if (isNaN(px) || isNaN(py)) return;
    const accent = css('--color-accent'), ink = css('--color-fg'), muted = css('--color-fg-muted');
    ctx.save();
    ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI * 2);
    ctx.strokeStyle = accent; ctx.lineWidth = 2; ctx.stroke();
    ctx.strokeStyle = css('--color-border-strong'); ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(px, py - 8); ctx.lineTo(px, py - 40); ctx.stroke();
    ctx.font = '700 12px ' + Chart.defaults.font.family; ctx.fillStyle = ink; ctx.textAlign = 'left';
    ctx.fillText(st.mark.t1, px - 2, py - 56);
    ctx.font = '600 11px ' + Chart.defaults.font.family; ctx.fillStyle = muted;
    ctx.fillText(st.mark.t2, px - 2, py - 42);
    ctx.restore();
  }
};
if (typeof Chart !== 'undefined') Chart.register(annoPlugin);   // atrás do guard CHART_OK

/* mutar por step/hover (ex.: dentro do applyStep do W1): */
// BAND['chartTese'] = { band: {from:2, to:4, text:'Choque tarifário'}, mark:{x:5, y:24.8, t1:'Pico', t2:'24,8%'} };
// chartTese.update();
```

**FALLBACK:** desenhar a anotação no 1º render (sem depender de scroll/hover) — o `afterDatasetsDraw` já é o fallback: basta popular `BAND[id]` antes do primeiro `update()`.
**VALIDADOR:** satisfaz P8 com signature `W8-live-annotation`.
**NÃO FAÇA:** destruir/recriar o gráfico por step (mutar `BAND` + `update()`); chamar fora do guard `typeof Chart !== 'undefined'`.

---

# W9 — Hero material WebGL (shader fbm) ★ código provado · A3 + data-overdrive apenas

**[A3 · deck-overdrive, showcase]** O momento "como isso foi feito?". Shader fbm inline (~5KB, NÃO Three.js), detect de WebGL + fallback aurora CSS nas **mesmas cores**. Gateado a A3 + `data-overdrive` (P10/P-premium-sobrio). **Proibido em registro sóbrio sem `/overdrive` deliberado.**

- **GANCHO:** `<canvas class="hero-canvas" id="heroGl">` dentro do hero; `start()`/`stop()` por slide (bateria).

```css
/* --- COLAR INTEGRAL (CSS) --- canvas + fallback aurora (estado-final-base) --- */
.hero-canvas { position:absolute; inset:0; z-index:0; pointer-events:none; opacity:.55; }
[data-theme="dark"] .hero-canvas { opacity:.8; }
.hero-canvas.aurora-fallback {                                 /* sem WebGL → aurora mesmas cores */
  opacity:1;
  background:
    radial-gradient(46% 56% at 50% 38%, color-mix(in srgb, var(--itau-orange) 20%, transparent), transparent 70%),
    radial-gradient(50% 60% at 22% 30%, color-mix(in srgb, var(--itau-blue-3) 13%, transparent), transparent 72%),
    radial-gradient(54% 64% at 80% 72%, color-mix(in srgb, var(--itau-orange-3) 11%, transparent), transparent 74%);
  -webkit-mask-image: radial-gradient(120% 120% at 50% 45%, #000 35%, transparent 100%);
          mask-image: radial-gradient(120% 120% at 50% 45%, #000 35%, transparent 100%);
}
@supports not (background: color-mix(in srgb, red, blue)) {     /* intranet/browser travado */
  .hero-canvas.aurora-fallback { background: radial-gradient(46% 56% at 50% 38%, rgba(255,98,0,.16), transparent 70%); }
}
@media (prefers-reduced-motion: no-preference) {
  .hero-canvas.aurora-fallback { animation: heroAuroraDrift 30s ease-in-out infinite alternate; }
}
@keyframes heroAuroraDrift { from { background-position: 0% 0%, 0% 0%, 0% 0%; } to { background-position: 100% 50%, 60% 100%, 30% 70%; } }
```

```js
/* --- COLAR INTEGRAL (JS) --- shader fbm + detect + fallback. Cores derivadas de --itau-orange. --- */
function initWebGLHero(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
  if (!gl) return null;
  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = canvas.clientWidth * dpr; canvas.height = canvas.clientHeight * dpr;
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  resize();
  const vs = `attribute vec2 aPos; void main(){ gl_Position = vec4(aPos,0.,1.); }`;
  const fs = `precision highp float; uniform vec2 uRes; uniform float uTime; uniform vec3 uAccent; uniform float uIntensity;
    float hash(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
    float noise(vec2 p){ vec2 i=floor(p),f=fract(p); float a=hash(i),b=hash(i+vec2(1,0)),c=hash(i+vec2(0,1)),d=hash(i+vec2(1,1));
      vec2 u=f*f*(3.-2.*f); return mix(a,b,u.x)+(c-a)*u.y*(1.-u.x)+(d-b)*u.x*u.y; }
    float fbm(vec2 p){ float v=0.,a=.5; for(int i=0;i<5;i++){ v+=a*noise(p); p*=2.02; a*=.5; } return v; }
    void main(){ vec2 uv=gl_FragCoord.xy/uRes.xy; vec2 p=uv*2.-1.; p.x*=uRes.x/uRes.y;
      float t=uTime*.18;
      vec2 q=vec2(fbm(p*1.4+vec2(t,-t*.6)), fbm(p*1.4+vec2(-t*.7,t)));
      vec2 r=vec2(fbm(p*2.+3.*q+vec2(1.7,9.2)+t*.3), fbm(p*2.+3.*q+vec2(8.3,2.8)-t*.4));
      float n=fbm(p*1.6+4.*r);
      float dist=length(p*vec2(.85,1.)); float mask=smoothstep(1.4,.1,dist);
      vec3 warm=uAccent, cool=vec3(.23,.52,.98);
      vec3 base=mix(cool,warm,smoothstep(.3,.85,n)); base*=mask*uIntensity;
      float alpha=mask*(.35+.55*n)*uIntensity; gl_FragColor=vec4(base,alpha); }`;
  function compile(type, src){ const s=gl.createShader(type); gl.shaderSource(s,src); gl.compileShader(s);
    if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){ console.warn(gl.getShaderInfoLog(s)); return null; } return s; }
  const vsh=compile(gl.VERTEX_SHADER,vs), fsh=compile(gl.FRAGMENT_SHADER,fs);
  if(!vsh||!fsh) return null;
  const prog=gl.createProgram(); gl.attachShader(prog,vsh); gl.attachShader(prog,fsh); gl.linkProgram(prog);
  if(!gl.getProgramParameter(prog,gl.LINK_STATUS)){ console.warn(gl.getProgramInfoLog(prog)); return null; }
  gl.useProgram(prog);
  const buf=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,buf);
  gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
  const loc=gl.getAttribLocation(prog,'aPos'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);
  const uRes=gl.getUniformLocation(prog,'uRes'), uTime=gl.getUniformLocation(prog,'uTime'),
        uAccent=gl.getUniformLocation(prog,'uAccent'), uIntensity=gl.getUniformLocation(prog,'uIntensity');
  const accentHex=getComputedStyle(document.documentElement).getPropertyValue('--itau-orange').trim()||'#FF6200';
  const hexToRgb=h=>{ const v=h.replace('#',''); return [parseInt(v.slice(0,2),16)/255,parseInt(v.slice(2,4),16)/255,parseInt(v.slice(4,6),16)/255]; };
  const accentRgb=hexToRgb(accentHex);
  let t0=performance.now(), raf=0, running=false;
  function render(){ if(!running) return; const t=(performance.now()-t0)/1000;
    gl.uniform2f(uRes,canvas.width,canvas.height); gl.uniform1f(uTime,t);
    gl.uniform3f(uAccent,accentRgb[0],accentRgb[1],accentRgb[2]); gl.uniform1f(uIntensity,1.);
    gl.clearColor(0,0,0,0); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
    raf=requestAnimationFrame(render); }
  window.addEventListener('resize',()=>{ if(running) resize(); });
  return { canvas, start(){ if(running)return; running=true; resize(); t0=performance.now(); render(); },
                   stop(){ running=false; cancelAnimationFrame(raf); } };
}
/* detect barato + fallback (estado-final-base). reduced-motion → não inicializa, usa aurora estática. */
const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const webglOK = (() => { try { return !!document.createElement('canvas').getContext('webgl'); } catch(e){ return false; } })();
const heroCanvases = {};
document.querySelectorAll('canvas.hero-canvas').forEach(c => {
  if (!prefersReduced && webglOK) { const h = initWebGLHero(c.id); if (h) { heroCanvases[c.id] = h; h.start(); return; } }
  c.classList.add('aurora-fallback');                          // sem WebGL/reduced/shader falhou
});
```

**FALLBACK:** `.aurora-fallback` (mesmas cores) sempre que WebGL ausente, reduced-motion, ou shader falhar. Nunca fica preto-morto.
**VALIDADOR:** satisfaz P8 com signature `W9-webgl`. P9 exige co-ocorrência de `.aurora-fallback` (offline não pode regredir em silêncio).
**NÃO FAÇA:** usar em registro sóbrio sem `data-overdrive` (falha P-premium-sobrio); manter `start()` em slide inativo (bateria — chamar `stop()`).

---

# Motor de gráfico (Chart.js) — tema + draw-on-enter + anotação viva

**[A2/A3 · qualquer gráfico-tese]** Eleva o gráfico de "Chart.js default" para FT/NYT. Três peças, todas atrás do guard `CHART_OK` (`typeof Chart !== 'undefined'`) para degradar offline:

1. **Tema** — `Chart.defaults.font.family = css('--kit-text')`, sem grid pesado, cores via `css('--color-*')`. Receita em [css-patterns.md](css-patterns.md) §5.0.
2. **Draw-on-enter** — a série-tese desenha do zero ao valor real **quando entra na viewport** (não no load). Reduced-motion = valor final instantâneo.
3. **Anotação viva (W8)** — banda/leader-line/marcador (bloco W8 acima).

```js
/* --- COLAR INTEGRAL (JS) — draw-on-enter --- */
function drawOnEnter(canvasId, makeChart) {
  const el = document.getElementById(canvasId);
  if (!el || typeof Chart === 'undefined') return;          // guard CHART_OK
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let chart = null;
  const start = () => {
    if (chart) return;
    chart = makeChart(el.getContext('2d'), reduce ? { duration: 0 } : { duration: 900, easing: 'easeOutQuart' });
  };
  if (reduce) { start(); return; }                          // reduced → cria já, sem animação
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { start(); io.disconnect(); } }), { threshold: 0.35 });
  io.observe(el);
}
/* uso: drawOnEnter('chartTese', (ctx, anim) => new Chart(ctx, { type:'line', data: DATA,
   options: { animation: anim, /* ...tema... */ } })); */
```

**FALLBACK:** sem Chart (CDN bloqueado) → guard `CHART_OK` (ver css-patterns §5.0b: o canvas vira aviso "gráfico indisponível offline"). Reduced-motion → gráfico no valor final sem animação.
**NÃO FAÇA:** animar `width`/altura do canvas; usar fora do guard; recriar o gráfico a cada scroll (criar uma vez, mutar via W8).

---

# ═══ Camada de assinatura premium (W10-W17) ═══

> Repertório "agência premiada". Todos **validados em harness** (0 erros/0 warns) e **gateados a registros expressivos** (deck/site/hub/scrollytelling) — proibidos em `report`/regulatório (P-premium-sobrio). A pesquisa de 2026 reforça: premium maduro = **proposital, ligado ao conteúdo, contido** (toda animação tem função, ≤300ms na UI), nunca espetáculo. Parcimônia é regra, não sugestão.

---

# W10 — Reveal por máscara editorial ★ a maior alavancagem

**[A2/A3 · todos os expressivos]** Substitui o `fade-up` (que o anti-slop trata como tell) pelo reveal de verdade: a manchete/imagem/KPI surge por uma máscara `clip-path` que se abre no scroll. É o reveal-padrão dos templates expressivos.

- **GANCHO:** classe `.mask-reveal` no elemento.

```css
/* --- COLAR INTEGRAL (CSS) --- */
.mask-reveal { clip-path: inset(0 0 0 0); }                    /* INVARIANTE 2: base = visível */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .mask-reveal { animation: maskWipe linear both; animation-timeline: view(); animation-range: entry 5% cover 35%; }
    @keyframes maskWipe { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
  }
}
```

**Variantes** (trocar a direção do `inset`): wipe vertical (`inset(100% 0 0 0)→0`), íris (`circle(0%)→circle(150%)`).
**FALLBACK:** base `clip-path: inset(0)` (totalmente visível). Reduced-motion idem.
**VALIDADOR:** satisfaz P8 com signature `W10-mask-reveal` (+ P9 exige o `@supports`).
**NÃO FAÇA:** usar em TODO elemento (vira o novo fade-up); `overflow:hidden` no ancestral.

---

# W11 — Magnetismo (elemento atrai o cursor)

**[A2/A3 · CTA primário, dots de nav, card-hero]** O "toque de agência". Só desktop com mouse; desliga em touch e reduced-motion. **Parcimônia: só no CTA primário + dots — nunca em linha de tabela/lista densa.**

- **GANCHO:** atributo `data-magnetic` no elemento.

```css
/* --- COLAR INTEGRAL (CSS) --- */
[data-magnetic] { transition: transform 160ms var(--ease-out-strong); }
```
```js
/* --- COLAR INTEGRAL (JS) --- */
document.querySelectorAll('[data-magnetic]').forEach(el => {
  if (!matchMedia('(hover:hover) and (pointer:fine)').matches) return;     // só desktop+mouse
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const S = 0.3; let raf = 0, lx = 0, ly = 0;
  el.addEventListener('pointermove', e => {
    const r = el.getBoundingClientRect();
    lx = (e.clientX - (r.left + r.width/2)) * S; ly = (e.clientY - (r.top + r.height/2)) * S;
    if (!raf) raf = requestAnimationFrame(() => { raf = 0; el.style.transform = `translate(${lx}px, ${ly}px)`; });
  });
  el.addEventListener('pointerleave', () => { el.style.transform = 'translate(0,0)'; });
});
```

**FALLBACK:** sem mouse/desktop → elemento estático normal (early return). Reduced-motion idem.
**VALIDADOR:** satisfaz P8 com signature `W11-magnetic`.
**NÃO FAÇA:** S > 0.4 (vira elástico cafona); aplicar em muitos elementos (parcimônia → P-premium).

---

# W12 — Spotlight (luz radial segue o cursor)

**[A2/A3 · UM bloco-herói/insight por documento]** Luz suave revelando profundidade sob o ponteiro. **Parcimônia: máx 1 por documento (P-premium-spotlight).**

- **GANCHO:** atributo `data-spotlight` no bloco.

```css
/* --- COLAR INTEGRAL (CSS) --- */
[data-spotlight] { --mx:50%; --my:50%; position:relative; }
[data-spotlight]::after {
  content:''; position:absolute; inset:0; pointer-events:none; border-radius:inherit;
  background: radial-gradient(220px circle at var(--mx) var(--my), color-mix(in srgb, var(--color-accent) 18%, transparent), transparent 60%);
  opacity:0; transition: opacity 200ms;
}
[data-spotlight]:hover::after { opacity:1; }
@media (prefers-reduced-motion: reduce) { [data-spotlight]::after { transition:none; } }
```
```js
/* --- COLAR INTEGRAL (JS) --- */
document.querySelectorAll('[data-spotlight]').forEach(el => {
  if (!matchMedia('(hover:hover) and (pointer:fine)').matches) return;
  el.addEventListener('pointermove', e => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', ((e.clientX - r.left)/r.width*100) + '%');
    el.style.setProperty('--my', ((e.clientY - r.top)/r.height*100) + '%');
  });
});
```

**FALLBACK:** sem mouse → bloco normal (a luz só aparece no `:hover`). `color-mix` indisponível → adicionar `@supports not` com rgba.
**VALIDADOR:** satisfaz P8 com signature `W12-spotlight`.
**NÃO FAÇA:** mais de 1 spotlight/doc; raio > 260px (vira holofote); sobre texto de corpo.

---

# W13 — Scroll horizontal fixado (sequência cinemática)

**[A2/A3 · scrollytelling, deck-como-leitura]** A seção prende e o conteúdo rola na horizontal. **Só quando o conteúdo é uma sequência real** (timeline, etapas, portfólio) — senão é gimmick e atrapalha.

- **GANCHO:** `.h-pin-outer` (scroller alto) > `.h-pin` (sticky) > `.h-track` (flex).

```css
/* --- COLAR INTEGRAL (CSS) --- base = scroll horizontal usável (sem JS) */
.h-pin { position: sticky; top:0; height:100vh; overflow-x:auto; scroll-snap-type:x mandatory; }
.h-track { display:flex; gap:var(--space-6); }
.h-track > * { flex:0 0 80vw; scroll-snap-align:center; }
@supports (animation-timeline: scroll()) {
  @media (prefers-reduced-motion: no-preference) {
    .h-pin-outer { height:300vh; }                             /* dá curso ao pin */
    .h-pin { overflow:clip; }
    .h-track { animation: hscroll linear both; animation-timeline: scroll(nearest block); }
    @keyframes hscroll { to { transform: translateX(calc(-100% + 100vw)); } }
  }
}
```

**FALLBACK:** sem `scroll()` → `.h-pin` vira carrossel com `scroll-snap` (usável no dedo e no teclado).
**VALIDADOR:** satisfaz P8 com signature `W13-horizontal-pin` (+ P9 `@supports`).
**NÃO FAÇA:** usar sem sequência real; trancar o scroll vertical (o pin tem que liberar ao fim).

---

# W14 — Parallax em camadas (profundidade real)

**[A2 · hero, scrollytelling]** Camadas em ritmos diferentes (foreground/mid/back). Só `transform`, compositado. Sutil — deslocamento de 30-60px, não dramático.

- **GANCHO:** `.parallax-layer` + `data-depth="back|mid"`.

```css
/* --- COLAR INTEGRAL (CSS) --- */
.parallax-layer { transform:none; }                            /* INVARIANTE 2: base */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .parallax-layer { animation: plx linear both; animation-timeline: view(); }
    .parallax-layer[data-depth="back"] { --plx:60px; }
    .parallax-layer[data-depth="mid"]  { --plx:30px; }
    @keyframes plx { from { transform: translateY(calc(var(--plx,0) * -1)); } to { transform: translateY(var(--plx,0)); } }
  }
}
```

**FALLBACK:** base `transform:none` (camadas alinhadas). Reduced-motion idem.
**VALIDADOR:** satisfaz P8 com signature `W1/W6-scroll-driven` (parallax é scroll-driven).
**NÃO FAÇA:** `--plx` > 80px (separa demais); parallax em fullscreen com blur (custo).

---

# W15 — Odômetro (número-tese rola por dígito)

**[A2/A3 · número-tese, KPI]** Cada dígito desliza como um contador mecânico — bem mais sofisticado que o count-up. Substitui/complementa o W2.

- **GANCHO:** `.odometer` com `data-odometer="3.200"` e o valor em texto no base (+ `aria-label`).

```css
/* --- COLAR INTEGRAL (CSS) --- */
.odometer { display:inline-flex; overflow:clip; line-height:1; font-variant-numeric: tabular-nums lining-nums; }
.od-digit { display:inline-block; width:1ch; height: 1em; overflow:clip; }
.od-reel { display:flex; flex-direction:column; transition: transform 900ms var(--ease-out-strong); }
.od-reel > span { height:1em; }
@media (prefers-reduced-motion: reduce) { .od-reel { transition:none; } }
```
```html
<span class="odometer" data-odometer="3.200" aria-label="3.200">3.200</span>
```
```js
/* --- COLAR INTEGRAL (JS) --- */
function buildOdometer(el){
  const raw = el.dataset.odometer || el.textContent;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  el.textContent = '';
  [...raw].forEach(ch => {
    if (!/\d/.test(ch)) { el.append(ch); return; }              // separador "." vira texto literal
    const d = document.createElement('span'); d.className = 'od-digit';
    const reel = document.createElement('span'); reel.className = 'od-reel';
    for (let i = 0; i <= 9; i++) { const s = document.createElement('span'); s.textContent = i; reel.append(s); }
    d.append(reel); el.append(d);
    const setY = () => { reel.style.transform = `translateY(${-ch}em)`; };
    if (reduce) setY(); else requestAnimationFrame(() => requestAnimationFrame(setY));
  });
}
const odoIO = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { buildOdometer(e.target); odoIO.unobserve(e.target); } }), { threshold: 0.6 });
document.querySelectorAll('.odometer').forEach(el => odoIO.observe(el));
```

**FALLBACK:** o valor final fica em texto real no HTML (base) + `aria-label`. Reduced-motion: posiciona os dígitos sem transição.
**VALIDADOR:** satisfaz P8 com signature `W15-odometer`.
**NÃO FAÇA:** esconder o valor base (acessibilidade/sem-JS); usar em muitos números (1-2 tese/doc).

---

# W16 — Tipografia reativa à velocidade do scroll (eixo GRAD)

**[A2/A3 · kit com Roboto Flex]** O peso aparente do texto responde à velocidade do scroll via eixo `GRAD` (muda sem reflow). Premium e sutil. **Exige kit com Roboto Flex.**

- **GANCHO:** classe `.vel-type`; um listener de scroll seta `--scroll-vel` no `<html>`.

```css
/* --- COLAR INTEGRAL (CSS) --- */
.vel-type { font-variation-settings: 'GRAD' 0; }              /* INVARIANTE 2: base estático */
@media (prefers-reduced-motion: no-preference) {
  .vel-type { font-variation-settings: 'GRAD' calc(-150 + var(--scroll-vel, 0) * 150); transition: font-variation-settings 120ms linear; }
}
```
```js
/* --- COLAR INTEGRAL (JS) --- */
let lastY16 = scrollY, raf16 = 0;
addEventListener('scroll', () => {
  const v = Math.min(1, Math.abs(scrollY - lastY16) / 60); lastY16 = scrollY;
  if (!raf16) raf16 = requestAnimationFrame(() => { raf16 = 0; document.documentElement.style.setProperty('--scroll-vel', v.toFixed(3)); });
}, { passive: true });
```

**FALLBACK:** sem Roboto Flex / reduced-motion → peso estático (`GRAD 0`).
**VALIDADOR:** satisfaz P8 com signature `W16-scroll-velocity`.
**NÃO FAÇA:** mapear `GRAD` para fora do range do Roboto Flex (-200..150); aplicar a corpo de texto inteiro.

---

# W17 — Decode/scramble (número-tese resolve de caracteres embaralhados)

**[A2/A3 · UM número-tese por documento — parcimônia máxima]** O dado mais importante "resolve" de dígitos embaralhados, **uma vez, rápido**. Maior risco de gimmick — `máx 1×/doc` (P-premium-scramble).

- **GANCHO:** `.scramble` com `data-scramble="24,8%"` e o valor em texto no base.

```css
/* --- COLAR INTEGRAL (CSS) --- */
.scramble { font-variant-numeric: tabular-nums; }
```
```js
/* --- COLAR INTEGRAL (JS) --- */
document.querySelectorAll('.scramble').forEach(el => {
  const final = el.dataset.scramble || el.textContent;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = final; return; }
  const glyphs = '0123456789';
  const io = new IntersectionObserver((es) => es.forEach(e => {
    if (!e.isIntersecting) return; io.unobserve(el);
    let frame = 0; const steps = 18;
    const id = setInterval(() => {
      frame++;
      el.textContent = [...final].map((c, i) => (/\d/.test(c) && i > frame / steps * final.length) ? glyphs[Math.floor(Math.random() * 10)] : c).join('');
      if (frame >= steps) { clearInterval(id); el.textContent = final; }
    }, 28);
  }), { threshold: 0.6 });
  io.observe(el);
});
```

**FALLBACK:** valor final em texto real no HTML (base). Reduced-motion → instantâneo.
**VALIDADOR:** satisfaz P8 com signature `W17-scramble`.
**NÃO FAÇA:** mais de 1 scramble/doc; embaralhar texto (só dígitos); duração > 600ms.


---

# ═══ Repertório expandido v7 (W18-W31) — empilhamento de alto impacto ═══

> Componentes "agência premiada" para **empilhar vários por documento**. Ler a §STACKING (no fim) antes de usar 3+: 1 herói + 2 sistemas ambientes na mesma física + 3-4 momentos espaçados + zonas de silêncio. Todos single-file, com `@supports`+estado-final-base e branch reduced-motion. Gateados a registros expressivos (premium-sobrio).

---

# W18 — Sticky stack (cards empilham como baralho) ★★★★★

**[A2/A3 · deck-como-leitura, scrollytelling, site]** Cards prendem um atrás do outro no scroll; o novo desliza e "pousa", o de baixo encolhe e escurece. Herói de "product launch".

- **GANCHO:** `.stack-wrap` (alto) > N × `.stack-card` (sticky).

```css
.stack-wrap { display: grid; gap: 12vh; }
.stack-card { position: sticky; top: 12vh; }            /* base = lista normal (sem suporte) */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .stack-card { animation: stackShrink linear both; animation-timeline: view(); animation-range: exit 0% exit 140%; }
    @keyframes stackShrink { to { transform: scale(.92) translateY(-14px); filter: brightness(.72); } }
  }
}
```

**FALLBACK:** sem timeline -> lista vertical normal. Reduced-motion -> sem shrink.
**VALIDADOR:** satisfaz P8 com signature `W18-sticky-stack`.
**NÃO FAÇA:** 2 mecânicas pinned no mesmo trecho (W18/W28/W19-horizontal); usar com <3 cards.

---

# W19 — Masked type (cor viva DENTRO das letras) ★★★★ · premium controlado

**[A2/A3 · UMA manchete-display por doc]** A manchete vira janela para um mesh da MARCA que se move dentro das letras. **Disciplina (NÃO é o tell gradient-text):** hue ÚNICO da marca (laranja->âmbar), display grande, 1 por documento, fundo calmo atrás.

- **GANCHO:** `.masked-type` na manchete.

```css
@property --mt-a { syntax: '<angle>'; inherits: false; initial-value: 0deg; }
.masked-type { color: var(--color-accent); }            /* base = preenchimento sólido da marca */
@supports (background-clip: text) or (-webkit-background-clip: text) {
  .masked-type {
    background: conic-gradient(from var(--mt-a), var(--itau-orange), var(--itau-orange-3), var(--itau-orange));
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  @media (prefers-reduced-motion: no-preference) {
    .masked-type { animation: mtSpin 16s linear infinite; }
    @keyframes mtSpin { to { --mt-a: 360deg; } }
  }
}
```

**FALLBACK:** sem background-clip -> cor sólida da marca (legível). Reduced-motion -> mesh congelado.
**VALIDADOR:** satisfaz P8 com signature `W19-masked-type`.
**NÃO FAÇA:** multi-hue arco-íris (vira slop); sobre um mesh animado (sopa de cor); em texto de corpo; >1 por doc.

---

# W20 — Aurora mesh animada (@property) ★★★★

**[A2/A3 · hero/divider]** Aurora de blobs da marca respirando atrás do herói. Versão animada da materialité W7.

- **GANCHO:** `.aurora-mesh` (pseudo `::before` borrado).

```css
@property --au-x { syntax: '<percentage>'; inherits: false; initial-value: 24%; }
.aurora-mesh { position: relative; isolation: isolate; }
/* ATENÇÃO em deck: o .slide base é position:absolute; inset:0. Se aplicar
   .aurora-mesh direto num <section class="slide">, o position:relative acima
   COLAPSA o slide para a altura do conteúdo (resto branco). Sobreponha: */
.slide.aurora-mesh { position: absolute; inset: 0; }
.aurora-mesh::before {
  content: ''; position: absolute; inset: -10%; z-index: -1; pointer-events: none; filter: blur(60px);
  background:
    radial-gradient(38vw at var(--au-x) 30%, color-mix(in srgb, var(--itau-orange) 40%, transparent), transparent 60%),
    radial-gradient(42vw at 78% 64%, color-mix(in srgb, var(--itau-blue-3) 26%, transparent), transparent 64%);
}
@media (prefers-reduced-motion: no-preference) {
  .aurora-mesh::before { animation: auDrift 22s var(--ease-out, ease-in-out) infinite alternate; }
  @keyframes auDrift { to { --au-x: 70%; } }
}
```

**FALLBACK:** `radial-gradient` universal; sem `@property` a posição fica estática. `@supports not (color-mix...)` -> rgba.
**VALIDADOR:** satisfaz P8 com signature `W20-aurora-mesh`.
**NÃO FAÇA:** junto com W23 gooey no mesmo viewport (orçamento de blur); fullscreen + scroll pesado.

---

# W21 — Scroll-hue drift (o doc muda de temperatura por capítulo) ★★★★ · sistema ambiente

**[A2/A3 · 1 por doc, global]** O acento e a temperatura migram seção a seção (quente intro -> frio dados -> quente fecho), atado ao progresso do scroll. Tecido conectivo, não momento.

- **GANCHO:** token `--doc-hue` no `<html>`; acentos referenciam `hsl(var(--doc-hue) ...)`.

```css
@property --doc-hue { syntax: '<number>'; inherits: true; initial-value: 24; }   /* 24 = laranja Itaú */
html { --doc-hue: 24; }
@supports (animation-timeline: scroll()) {
  @media (prefers-reduced-motion: no-preference) {
    html { animation: hueDrift linear both; animation-timeline: scroll(root); }
    @keyframes hueDrift { 45% { --doc-hue: 210; } 100% { --doc-hue: 24; } }
  }
}
/* usar onde fizer sentido: .accent-dynamic { color: hsl(var(--doc-hue) 95% 50%); } — manter S/L travados */
```

**FALLBACK:** sem `@property`/timeline -> hue fixo da marca. Reduced-motion -> travar em 1 hue.
**VALIDADOR:** satisfaz P8 com signature `W21-hue-drift`.
**NÃO FAÇA:** mexer em saturação/luminosidade (vira brinquedo); aplicar a TEXTO de leitura (só acentos/detalhes).

---

# W22 — Draw-on SVG (diagrama se desenha) ★★★★★

**[A2/A3 · qualquer diagrama/conector]** Linhas, fluxo ou org-chart se desenham stroke-a-stroke ao entrar. Transforma diagrama estático em revelação.

- **GANCHO:** `.draw-on` nos `<path>` (medir `--len` com getTotalLength ou hardcode).

```css
.draw-on { stroke-dasharray: var(--len, 1000); stroke-dashoffset: 0; }   /* base = desenhado */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .draw-on { stroke-dashoffset: var(--len, 1000); animation: drawPath 1.2s ease both;
               animation-timeline: view(); animation-range: cover 10% cover 45%; }
    @keyframes drawPath { to { stroke-dashoffset: 0; } }
  }
}
```
```js
/* medir comprimento real (1x, no load) — opcional se hardcodar --len */
document.querySelectorAll('.draw-on').forEach(p => { try { p.style.setProperty('--len', Math.ceil(p.getTotalLength())); } catch(e){} });
```

**FALLBACK:** base `stroke-dashoffset:0` = diagrama completo. Reduced-motion -> completo instantâneo.
**VALIDADOR:** satisfaz P8 com signature `W22-draw-on` (compartilha família com M6).
**NÃO FAÇA:** 2 draw-on no mesmo viewport (espaçar por scroll); `overflow:hidden` no SVG ancestral.

---

# W23 — Gooey morph (blobs líquidos, filtro SVG) ★★★ · spice

**[A2/A3 · 1 por doc, acento]** Blobs se fundem/separam como mercúrio atrás de um dado ou como divisor.

- **GANCHO:** filtro `#goo` + container com 2-3 círculos animados.

```html
<svg width="0" height="0"><filter id="goo"><feGaussianBlur in="SourceGraphic" stdDeviation="10" result="b"/>
  <feColorMatrix in="b" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9"/></filter></svg>
```
```css
.goo { filter: url(#goo); position: relative; }
.goo > i { display:block; position:absolute; width:90px; height:90px; border-radius:50%; background:var(--color-accent); }
@media (prefers-reduced-motion: no-preference) { .goo > i { animation: gooMove 6s var(--ease-out, ease-in-out) infinite alternate; } }
@keyframes gooMove { to { transform: translate(60px,-30px) scale(1.15); } }
```

**FALLBACK:** `@supports (filter:url(#goo))`; sem isso -> círculos simples. Reduced-motion -> arranjo estático.
**VALIDADOR:** satisfaz P8 com signature `W23-gooey`.
**NÃO FAÇA:** área grande (fps); junto de outra fonte de blur (W20/W29) no viewport.

---

# W24 — 3D tilt scene (card-herói inclina em 3D) ★★★★

**[A2/A3 · 1-2 cards-herói]** O card inclina rumo ao cursor em perspectiva real; camadas com `translateZ` em profundidade. Sinal mais rápido de "site premium".

- **GANCHO:** `[data-tilt]` no card.

```css
[data-tilt] { transform: perspective(800px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)); transform-style: preserve-3d;
  transition: transform 200ms var(--ease-out, ease-out); }
[data-tilt] > .tilt-layer { transform: translateZ(40px); }
```
```js
document.querySelectorAll('[data-tilt]').forEach(el => {
  if (!matchMedia('(hover:hover) and (pointer:fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect();
    el.style.setProperty('--rx', ((.5-(e.clientY-r.top)/r.height)*10).toFixed(2)+'deg');
    el.style.setProperty('--ry', (((e.clientX-r.left)/r.width-.5)*10).toFixed(2)+'deg'); });
  el.addEventListener('pointerleave', () => { el.style.setProperty('--rx','0deg'); el.style.setProperty('--ry','0deg'); });
});
```

**FALLBACK:** touch/sem mouse -> estático. Reduced-motion -> sem tilt.
**VALIDADOR:** satisfaz P8 com signature `W24-tilt`.
**NÃO FAÇA:** tilt em TODO card (tell de slop — só o herói); junto de W26 spotlight no mesmo viewport.

---

# W25 — Data choreography (número + barra + legenda em sequência) ★★★★★

**[A2/A3 · 3-6 por doc, cavalo de batalha de dados]** O número rola com mola ENQUANTO a barra enche e a legenda sobe — mesmo gatilho de scroll, em cascata.

- **GANCHO:** `[data-choreo]` no bloco (`.num`, `.bar`, `.cap` dentro).

```css
:root { --spring: linear(0, .5 30%, 1.08 60%, .98, 1); }   /* UMA física p/ o doc inteiro */
@property --cn { syntax: '<integer>'; inherits: false; initial-value: 0; }
[data-choreo] .num::after { content: counter(cn); }
[data-choreo] .num { counter-reset: cn var(--cn); }        /* base: número real em texto no HTML também */
[data-choreo] .bar { transform: scaleX(1); transform-origin: left; }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    [data-choreo] { animation-timeline: view(); animation-range: entry 20% entry 70%; }
    [data-choreo] .num { animation: choreoCount 1s var(--spring) both; }
    [data-choreo] .bar { transform: scaleX(0); animation: choreoFill 1s var(--spring) .15s both; }
    [data-choreo] .cap { opacity: 0; animation: choreoRise .6s ease .4s both; }
    @keyframes choreoCount { to { --cn: 3200; } }          /* trocar pelo valor real */
    @keyframes choreoFill { to { transform: scaleX(1); } }
    @keyframes choreoRise { to { opacity: 1; transform: none; } }
  }
}
```

**FALLBACK:** número final em texto real + barra cheia + legenda visível no base. Reduced-motion -> estado final.
**VALIDADOR:** satisfaz P8 com signature `W25-data-choreo`.
**NÃO FAÇA:** curvas diferentes por métrica (uma `--spring` só); animar width (use scaleX).

---

# W26 — Spotlight mask (cursor revela 2ª camada) ★★★★

**[A2/A3 · 1 por doc]** Painel borrado/escuro; o cursor abre um holofote circular nítido revelando uma 2ª camada embaixo.

- **GANCHO:** `[data-spot-mask]` com `--mx/--my`.

```css
[data-spot-mask] { --mx:50%; --my:50%;
  -webkit-mask: radial-gradient(circle 150px at var(--mx) var(--my), #000 0 99%, transparent 100%);
          mask: radial-gradient(circle 150px at var(--mx) var(--my), #000 0 99%, transparent 100%); }
@supports not (mask: radial-gradient(circle at 0 0, #000, transparent)) { [data-spot-mask] { -webkit-mask:none; mask:none; } }
@media (prefers-reduced-motion: reduce) { [data-spot-mask] { -webkit-mask:none; mask:none; } }
```
```js
document.querySelectorAll('[data-spot-mask]').forEach(el => {
  if (!matchMedia('(hover:hover) and (pointer:fine)').matches) return;
  el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', ((e.clientX-r.left)/r.width*100)+'%');
    el.style.setProperty('--my', ((e.clientY-r.top)/r.height*100)+'%'); });
});
```

**FALLBACK:** sem mask -> camada inteira visível. Touch -> camada visível.
**VALIDADOR:** satisfaz P8 com signature `W26-spot-mask`.
**NÃO FAÇA:** perto de W24 tilt (cursor disputado); esconder conteúdo essencial só na máscara.

---

# W27 — Marquee/ticker (fita de palavras desliza) ★★★ · ritmo

**[A2/A3 · 1-2 por doc, tecido entre seções]** Fita contínua de palavras/stats deslizando.

- **GANCHO:** `.marquee` > `.marquee__track` (conteúdo duplicado 2x para loop sem costura).

```css
.marquee { overflow: clip; }
.marquee__track { display: inline-flex; gap: 2rem; white-space: nowrap; will-change: transform; }
@media (prefers-reduced-motion: no-preference) { .marquee__track { animation: marq 32s linear infinite; } }
@keyframes marq { to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .marquee__track { animation: none; } }
```

**FALLBACK:** reduced-motion -> fita parada (linha estática). Universal.
**VALIDADOR:** satisfaz P8 com signature `W27-marquee`.
**NÃO FAÇA:** 2 marquees no mesmo viewport; velocidade alta (rápido = barato).

---

# W28 — Chapter divider (interstício full-bleed scrubbed) ★★★★

**[A2/A3 · 2-4 act-breaks por doc]** Entre capítulos a tela prende num título full-bleed; ao rolar ATRAVÉS o número faz scrub, o fundo varre, o tipo escala. Ritmo de filme.

- **GANCHO:** `.chapter-divider` (runway alto) > `.chapter-divider__inner` (sticky 100vh).

```css
.chapter-divider { height: 200vh; }                       /* runway de scroll */
.chapter-divider__inner { position: sticky; top: 0; height: 100vh; display: grid; place-items: center; overflow: clip; }
.chapter-divider__big { font-variant-numeric: tabular-nums; }   /* base = título estático full-bleed */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .chapter-divider__inner > * { animation: chScrub linear both; animation-timeline: view(); animation-range: contain 0% contain 100%; }
    @keyframes chScrub { from { opacity:.2; transform: scale(.9); } 50% { opacity:1; transform:none; } to { opacity:.2; transform: scale(1.05); } }
  }
}
```

**FALLBACK:** sem timeline -> seção título full-bleed normal. Reduced-motion -> estático.
**VALIDADOR:** satisfaz P8 com signature `W28-chapter-divider`.
**NÃO FAÇA:** adjacente a W18 stack (fadiga de pin); usar como única coisa do doc.

---

# W29 — Blur-to-sharp focus (figuras entram desfocadas e focam) ★★★ · sistema ambiente

**[A2/A3 · todas as figuras-herói — sistema, não momento]** Imagens entram borradas e dessaturadas e "racking focus" ao chegar na leitura.

- **GANCHO:** `.focus-reveal` na `<img>`/figura.

```css
.focus-reveal { filter: none; }                           /* base = nítido */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .focus-reveal { animation: focusIn linear both; animation-timeline: view(); animation-range: entry 8% entry 58%; }
    @keyframes focusIn { from { filter: blur(14px) saturate(.4); opacity:.4; } to { filter: blur(0) saturate(1); opacity:1; } }
  }
}
```

**FALLBACK:** base nítido. Reduced-motion -> nítido instantâneo. Universal.
**VALIDADOR:** satisfaz P8 com signature `W29-focus-reveal`.
**NÃO FAÇA:** raio de blur alto em imagem enorme (fps); usar como "momento" (é consistência).

---

# W30 — Flip-in 3D (letras giram como split-flap) ★★★★

**[A2/A3 · 1-2 manchetes-herói]** As letras entram girando pra cima de plano (`rotateX(-90deg)`), como placa de aeroporto.

- **GANCHO:** `[data-flip-in]` na manchete (JS divide em letras; manter `aria-label`).

```js
document.querySelectorAll('[data-flip-in]').forEach(el => {
  if (el._flip) return; el._flip = true;
  const t = el.textContent; el.setAttribute('aria-label', t);
  el.innerHTML = [...t].map((c,i) => `<span aria-hidden="true" style="--i:${i}">${c===' '?'&nbsp;':c}</span>`).join('');
});
```
```css
[data-flip-in] span { display: inline-block; transform-origin: bottom; }
@media (prefers-reduced-motion: no-preference) {
  [data-flip-in] span { animation: flipIn .5s var(--spring, cubic-bezier(.2,.7,.2,1)) both; animation-delay: calc(var(--i,0)*38ms); }
  @keyframes flipIn { from { transform: perspective(400px) rotateX(-90deg); opacity: 0; } to { transform: none; opacity: 1; } }
}
```

**FALLBACK:** sem JS -> manchete normal visível. Reduced-motion -> opacidade plena, sem flip.
**VALIDADOR:** satisfaz P8 com signature `W30-flip-in`.
**NÃO FAÇA:** em corpo de texto ou TODO heading (device de herói); >2 por doc.

---

# W31 — Glitch / RGB-split (1 palavra, controlado) ★★★ · spice tonal

**[A2/A3 · 1x por doc, zonas escuras/tech]** No reveal, uma palavra se separa em canais vermelho/ciano e treme ~400ms, depois resolve limpa. `máx 1`.

- **GANCHO:** `.glitch` com `data-t="palavra"`.

```css
.glitch { position: relative; }
.glitch::before, .glitch::after { content: attr(data-t); position: absolute; inset: 0; }
@media (prefers-reduced-motion: no-preference) {
  .glitch::before { color:#0ff; clip-path: inset(0 0 60% 0); animation: glitchA .4s steps(2) 1 both; }
  .glitch::after  { color:#f00; clip-path: inset(60% 0 0 0); animation: glitchB .4s steps(2) 1 both; }
  @keyframes glitchA { 0%,100%{transform:none} 50%{transform:translateX(-3px)} }
  @keyframes glitchB { 0%,100%{transform:none} 50%{transform:translateX(3px)} }
}
@media (prefers-reduced-motion: reduce) { .glitch::before, .glitch::after { display: none; } }
```

**FALLBACK:** sem suporte -> texto limpo (pseudos não aparecem). Reduced-motion -> DESLIGA totalmente.
**VALIDADOR:** satisfaz P8 com signature `W31-glitch`.
**NÃO FAÇA:** >1 por doc; em doc editorial/calmo (é tonal); em mais de uma palavra.

---

## ═══ STACKING — como empilhar 5-8 sem virar cassino ═══

1. **Um herói, nunca dois.** Exatamente 1 rank-5 dominante por doc (Sticky stack OU Scrub OU draw-on herói). Duas mecânicas pinned/scrub disputam o mesmo gesto de scroll = enjoo.
2. **Dois sistemas ambientes correm o doc inteiro.** Atravessam tudo: **W21 hue-drift** + **um** sistema de reveal em toda figura (**W29 blur-focus** OU **W25 data-choreo** com **uma** `--spring`). É a "física da casa".
3. **Três a quatro momentos rank-4, espaçados, nunca adjacentes.** ~1.5 viewport entre dois. **Nunca 2 momentos de atenção no mesmo viewport.**
4. **Zonas de silêncio obrigatórias.** Depois de cada momento, 1-2 viewports só ambiente. ~30% momento, 70% calmo.
5. **Spice é one-shot.** Gooey, glitch, marquee-curva: máx 1 cada, nunca no mesmo ato.
6. **Conflito (regras duras):** nunca 2 pinned (W18/W28/W19-horizontal); nunca 2 blur no viewport (W20+W23+W29); nunca 2 cursor-reativos (W24+W26); masked-type pede fundo calmo.
7. **Hierarquia:** cor/luz ambiente < reveals materiais (blur/draw/count) < tipo de entrada (1-2 manchetes) < herói pinned único.

**Brief de uma linha:** *um herói pinned, dois sistemas ambientes na mesma mola, três-a-quatro momentos rank-4 espaçados, um spice opcional — e proteja o silêncio entre eles.*


> **`data-showcase` (corpus de demos):** os documentos em `demos/` existem para EXIBIR o palette inteiro. O atributo `data-showcase` no `<body>` libera a camada premium em qualquer registro (o validador trata igual a `data-overdrive`: `P-premium-sobrio` e `P10` não disparam). **Em geração real, NÃO use `data-showcase`** — a regra de que registro sóbrio (report/regulatório) não recebe premium continua valendo.

---

## Armadilhas visuais que o `smoke.py` reprova (corrigir na origem)

O validador estrutural NÃO vê quebra de render. Estas seis já quebraram demos em
silêncio — `scripts/smoke.py` agora as pega, mas evite-as desde a composição:

1. **Odômetro/reel não-clipado (coluna 0-9 aparece).** `.od-digit` PRECISA de
   `height: 1em` (+ `overflow: clip`); sem altura, o `overflow:clip` não tem o que
   cortar e a tira inteira de dígitos vaza. Vale para qualquer dígito-em-tira.
2. **Número duplicado ("7070%").** Nunca tenha o número como nó de texto direto
   **E** `::after { content: counter() }` ao mesmo tempo. Esconda o texto-base
   (`display:none`) dentro do `@supports`+motion, OU use overlay (`::after`
   `position:absolute` + texto `color:transparent`). Ver W2/W25 acima.
3. **Texto quebrando por-caractere.** Lista/numeral com `display:grid` cujo `li`
   tem conteúdo inline (`<strong>texto…</strong> resto`): o `<strong>` e o nó de
   texto viram **grid-items separados** e o resto cai na coluna estreita. Use
   counter **absoluto** (`position:relative` no `li` + `::before` absoluto), não grid.
4. **Slide colapsado (capa branca pela metade).** Variantes de `.slide`
   (`.overdrive-hero`, `.aurora-mesh`, etc.) NÃO podem sobrescrever `position` para
   `relative` — o `.slide` base é `position:absolute; inset:0` e o relative colapsa
   o slide para a altura do conteúdo. Se precisar de `isolation`/contexto, use
   `.slide.<variante> { position:absolute; inset:0; }` (mais específico) ou só
   `isolation:isolate` sem mexer em position.
5. **`.bleed` invadindo TOC/sidebar.** A técnica full-bleed (margem negativa +
   largura > 100%) assume layout centrado de coluna única. Em handbook/report COM
   sidebar/TOC, ela invade as colunas laterais. Nesses layouts: `.bleed { width:100%;
   margin-left:0; max-width:100%; overflow-x:auto; }` (tabela larga rola, não invade).
6. **Clique de hub que não rola.** `scrollIntoView` DEPOIS de `startViewTransition`
   roda antes do painel virar `display:block` → rola pro card fechado ("clique 2x").
   Chame o scroll em **duplo `requestAnimationFrame`** após o `navigate()`/updateDOM.
7. **Gráfico Chart.js estourando o box em "outros computadores".** `<canvas>` é replaced
   element: regra CSS `canvas { width: auto }` faz ele exibir no tamanho INTRÍNSECO
   (buffer = css × `devicePixelRatio`), então em tela 2×/3× o gráfico aparece no dobro e
   vaza o container — em DPR=1 (a tela do dev) parece ok. Dê tamanho EXPLÍCITO ao canvas:
   `width:100% !important; height:100% !important` (ou `calc(...)`), **nunca `auto`**, com
   `maintainAspectRatio:false` e o container com altura definida. (validador: `B-canvas-autosize`.)
8. **Demo embutida via `iframe srcdoc` carrega o doc-pai ao clicar um link.** Em `srcdoc`,
   `href="#x"` resolve contra a URL-base do PAI, então clicar navega o iframe pro pai. Embuta
   via **`iframe.src` = blob URL** (`URL.createObjectURL(new Blob([html],{type:'text/html'}))`),
   aí os links de hash resolvem dentro da própria demo.
