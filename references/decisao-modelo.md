# Decisão de modelo

6 modelos. Confusões mais comuns: `scrollytelling` × `deck` × `site`, e `report` × `handbook`. Use esta árvore antes de gerar.

---

## Árvore de decisão

```
O usuário vai APRESENTAR ao vivo (com plateia)?
├── SIM
│   └── deck                  (slide-by-slide, keyboard nav, fullscreen)
└── NÃO — vai distribuir para leitura
    │
    O destino é IMPRESSÃO / PDF formal (RI, compliance, diretoria, conselho)?
    ├── SIM, documento editorial denso com seções numeradas/footnotes
    │   └── report             (sumário executivo, TOC numerada, @print rigoroso)
    └── NÃO — leitura em tela
        │
        O conteúdo tem narrativa LINEAR única do início ao fim?
        ├── SIM
        │   └── Quanto conteúdo?
        │       ├── < 8 seções verticais com dados/charts  → scrollytelling
        │       └── ≥ 8 seções, denso, referencial         → handbook
        └── NÃO — conteúdo tem múltiplas dimensões independentes
            │
            Quantas dimensões?
            ├── 2-5 dimensões com cara de "páginas distintas"  → site (SPA hash routing)
            └── 6+ recursos categorizados, leitor escolhe      → hub (grid de cards)
```

---

## Tabela comparativa

| Critério | handbook | hub | scrollytelling | site | deck | report |
|---|---|---|---|---|---|---|
| Como o leitor avança? | Scroll + sidebar | Click em card | Scroll natural | Click em nav | Setas/teclado | Scroll + TOC |
| Apresentador ao vivo? | Não | Não | Não | Não | **Sim** | Não |
| Destino primário | Tela | Tela | Tela | Tela | Projetor | **Impressão/PDF** |
| Quantidade de "páginas" | 1 longa, por h2 | 1 + painéis | 1 longa | 2-5 views | 8-25 slides | 1 longa numerada |
| Tipografia editorial (≤2.5rem h1)? | Sim | Sim | Sim | Sim | **Não — gigante OK** | Sim |
| Nav lateral? | **Sidebar** | Não | Não | Top nav | Não | TOC numerada |
| Hash routing? | Não | Opcional | Não | **Sim** | Não | Não |
| Reveal on scroll? | Leve | Não | **Sim** | Leve | Fragments | **Não — estático/print** |
| Sticky chart? | Não | Não | **Sim** | Não | Não | Não |
| Filtros funcionais? | Não | **Sim** | Não | Não | Não | Não |
| Footnotes + @print rigoroso? | Não | Não | Não | Não | Não | **Sim** |

---

## Casos ambíguos resolvidos

### "Quero substituir um PPT que eu vou apresentar"
→ **deck**. Checagem: vai ter slides? vai usar setas? vai abrir em fullscreen? Todos sim ⇒ deck.

### "Quero substituir um PPT, mas é pra distribuir como leitura"
→ **scrollytelling** (narrativa única com dados), **handbook** (referencial denso) ou **report** (se for formal/PDF, diretoria/RI). Nunca deck.

### "Quero um relatório anual / white paper / documento executivo"
→ **report** se o destino é impressão/PDF, com sumário executivo, seções numeradas e footnotes (vibe Itaú Pesquisa Macro, McKinsey, Goldman research). → **scrollytelling** se for uma narrativa interativa com charts sticky para leitura em tela. → **handbook** se for referencial com seções consultadas fora de ordem. Na dúvida entre report e handbook: *report* é editorial-denso-para-imprimir; *handbook* é manual-navegável-em-tela com sidebar.

### "Quero uma página interna do meu time"
→ Geralmente **hub** (recursos, atalhos, contatos). Se for institucional/narrativo ("quem somos") ⇒ **site** ou **scrollytelling**.

### "Quero um documento navegável estilo manual"
→ **handbook**. Se tiver < 4 h2 e couber em uma página rolável sem sidebar, é **scrollytelling** simplificado.

### "Quero uma central de processos com 20+ entradas"
→ **handbook** (sidebar com 20 links > grid de 20 cards). Use `hub` se as entradas pedirem agrupamento por categoria com filtro.

### "Quero um onboarding pra novato"
→ **handbook** (referencial, consultado depois) OU **scrollytelling** (narrativa "primeiros 30 dias" lida 1×). Padrão: handbook.

### "Não sei"
→ Pergunte com a árvore acima. Não chute.

---

## Quando perguntar ao usuário (em vez de inferir)

Sempre perguntar se:
1. O pedido é "apresentação" ou "deck" mas sem mencionar se é ao vivo. → *"Vai apresentar ao vivo (deck) ou distribuir para leitura (scrollytelling/report)?"*
2. O pedido é "relatório" sem deixar claro se é para imprimir. → *"É para imprimir/virar PDF formal (report) ou ler em tela com interatividade (scrollytelling/handbook)?"*
3. O pedido cita conteúdo de tamanho intermediário (5-8 seções). → Pergunte densidade e se há charts.
4. O pedido é "página interna" sem detalhes. → Portal de recursos (hub), institucional (site) ou documento longo (handbook)?

---

## Conversões entre modelos

`/converter-modelo <novo>` cobre as conversões compatíveis:

| De → Para | Viável? | Notas |
|---|---|---|
| handbook → scrollytelling | Sim | Vira página única, sidebar some, h2 viram cenas. |
| scrollytelling → handbook | Sim | Adiciona sidebar + TOC, divide em h2 navegáveis. |
| handbook → report | Sim | Vira editorial numerado + footnotes + @print; sidebar vira TOC numerada. |
| report → handbook | Sim | Seções numeradas viram navegáveis por sidebar; footnotes viram inline/callouts. |
| hub → site | Sim | Cards viram top-nav, conteúdo dos cards vira `<article class="view">`. |
| site → hub | Sim | Views viram cards na home. |
| deck → scrollytelling | Difícil | Slides viram cenas, mas conteúdo costuma ser raso demais. Avisar. |
| qualquer → deck | Não automática. | Deck pede slide-by-slide pensado. Recriar do zero a partir do conteúdo. |
