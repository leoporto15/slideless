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
   <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
   ```
2. Inserir canvas + script:
   ```html
   <div class="chart-wrap">
     <canvas id="chart-<slug>" aria-label="<descrição>"></canvas>
   </div>
   <script>
     const css = getComputedStyle(document.documentElement);
     new Chart(document.getElementById('chart-<slug>'), {
       type: '<tipo>',
       data: { labels: [...], datasets: [{ data: [...], borderColor: css.getPropertyValue('--color-accent').trim(), backgroundColor: 'rgba(255,98,0,0.1)' }] },
       options: { responsive: true, plugins: { legend: { display: false } } }
     });
   </script>
   ```
3. **Dados:** SEM inventar. Pedir ao usuário se não vieram explicitamente.
4. **Tema dinâmico:** ler cor via `getComputedStyle(--color-accent)`. Recriar chart no `themeChange` (ou simplesmente não cobrir esse caso se o usuário não precisar).
5. `aria-label` no `<canvas>` é obrigatório (descrição do que o gráfico mostra).
6. Validar.

## Anti-patterns críticos

- Inventar números (anti-pattern C2).
- Cor hardcoded fora dos tokens.
- Esquecer `aria-label` (Chart.js cria canvas, screenreader não vê).
