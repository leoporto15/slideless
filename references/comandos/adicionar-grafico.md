---
description: Insere gráfico Chart.js (line/bar/donut) em documento slideless
argument-hint: <tipo> <dados>
---

Você foi invocado para adicionar gráfico.

## Tipos suportados

- `line` — séries temporais, evolução
- `bar` — comparação entre categorias
- `donut` (Chart.js doughnut) — composição/share
- `area` (line com `fill: true`) — volume cumulativo

## Procedimento

1. Adicionar CDN no `<head>` se ainda não tiver:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
   ```
2. **Bloco de defaults — OBRIGATÓRIO antes do primeiro `new Chart()`** (§5.0 de [../references/css-patterns.md](../css-patterns.md)). Sem ele o Chart.js renderiza na Helvetica default com formatação en-US ("1,234.5") — falha o validador (P5) e é o tell de IA mais barato de matar. Colar UMA vez, antes de qualquer gráfico:
   ```js
   const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
   // Fonte e cor do DOCUMENTO, nunca o default da lib
   Chart.defaults.font.family = css('--font-ui') || css('--font-text');
   Chart.defaults.font.size = 12;
   Chart.defaults.color = css('--color-fg-muted');
   // Formatação numérica pt-BR — consistente com o texto do documento
   const fmtBR  = (v, dec = 0) => v.toLocaleString('pt-BR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
   const fmtBRL = (v, suf = '') => 'R$ ' + fmtBR(v, v % 1 ? 1 : 0) + (suf ? ' ' + suf : '');
   // Tooltip tematizado (não o chrome default)
   Chart.defaults.plugins.tooltip.backgroundColor = css('--color-bg-elevated');
   Chart.defaults.plugins.tooltip.titleColor = css('--color-fg');
   Chart.defaults.plugins.tooltip.bodyColor = css('--color-fg-muted');
   Chart.defaults.plugins.tooltip.borderColor = css('--color-border-strong');
   Chart.defaults.plugins.tooltip.borderWidth = 1;
   ```
3. Inserir canvas + script (ticks usando `fmtBR`/`fmtBRL` para sair em pt-BR):
   ```html
   <div class="chart-wrap">
     <canvas id="chart-<slug>" aria-label="<descrição>"></canvas>
   </div>
   <script>
     new Chart(document.getElementById('chart-<slug>'), {
       type: '<tipo>',
       data: { labels: [...], datasets: [{ data: [...], borderColor: css('--color-accent'), backgroundColor: 'rgba(255,98,0,0.1)' }] },
       options: { responsive: true, plugins: { legend: { display: false } },
                  scales: { y: { ticks: { callback: v => fmtBR(v) } } } }
     });
   </script>
   ```
4. **Dados:** SEM inventar. Pedir ao usuário se não vieram explicitamente.
5. **Tema dinâmico:** as cores e `Chart.defaults` são lidos na criação — escutar o evento de tema e dar `chart.update()` (ou recriar) para o dark mode pegar.
6. `aria-label` no `<canvas>` é obrigatório (descrição do que o gráfico mostra).
7. Validar.

## Gate de render antes de entregar (v7 — obrigatório)
A edição/importação mexe no render — além do `validar.py`, rodar o smoke e corrigir a CAUSA:
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
- O `<canvas>` do Chart.js NUNCA pode ter CSS `width:auto`/`height:auto` (replaced element → exibe no tamanho do buffer = css×devicePixelRatio → estoura em telas 2×/3×); usar tamanho explícito (`100%`/`calc`, `maintainAspectRatio:false`, container com altura definida). O `validar.py` tem o check `B-canvas-autosize`.
Nunca entregar com `SMOKE FAIL`. Armadilhas: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Anti-patterns críticos

- Inventar números (anti-pattern C2).
- Cor hardcoded fora dos tokens.
- Esquecer `aria-label` (Chart.js cria canvas, screenreader não vê).
