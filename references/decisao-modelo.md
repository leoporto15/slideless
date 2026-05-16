# Decisão de modelo

5 modelos. Confusão mais comum: `scrollytelling` × `deck` × `site`. Use esta árvore antes de gerar.

---

## Árvore de decisão

```
O usuário vai APRESENTAR ao vivo (com plateia)?
├── SIM
│   └── deck                  (slide-by-slide, keyboard nav, fullscreen)
└── NÃO — vai distribuir para leitura
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

| Critério | handbook | hub | scrollytelling | site | deck |
|---|---|---|---|---|---|
| Como o leitor avança? | Scroll + sidebar | Click em card | Scroll natural | Click em nav | Setas/teclado |
| Apresentador ao vivo? | Não | Não | Não | Não | **Sim** |
| Quantidade de "páginas" | 1 longa, dividida por h2 | 1 + painéis | 1 longa | 2-5 views | 8-25 slides |
| Tipografia editorial (≤2.5rem h1)? | Sim | Sim | Sim | Sim | **Não — gigante OK** |
| Sidebar de nav? | **Sim** | Não | Não | Não (top nav) | Não |
| Hash routing? | Não | Opcional | Não | **Sim** | Não |
| Reveal on scroll? | Leve | Não | **Sim** | Leve | Não (usa fragments) |
| Keyboard nav? | Tab/setas no link | Tab | Tab | Tab + hash | **Setas + Space + Esc** |
| Densidade do texto | Alta | Baixa-média | Média | Média | Baixa |
| Sticky chart? | Não | Não | **Sim** | Não | Não |
| Filtros funcionais? | Não | **Sim** | Não | Não | Não |
| Progress bar? | Não | Não | **Sim** | Não | Indicador de slide |

---

## Casos ambíguos resolvidos

### "Quero substituir um PPT que eu vou apresentar"
→ **deck**. Pergunta de checagem: vai ter slides? vai usar setas? vai abrir em fullscreen? Todos sim ⇒ deck.

### "Quero substituir um PPT, mas é pra distribuir como leitura, não apresentar"
→ **scrollytelling** (se for narrativa única) ou **handbook** (se for referencial e denso). Nunca deck — leitor não vai querer apertar seta para avançar lendo sozinho.

### "Quero uma página interna do meu time"
→ Geralmente **hub** (recursos do time, atalhos, contatos). Se for institucional/narrativo ("quem somos, o que fazemos, casos") ⇒ **site** ou **scrollytelling**.

### "Quero um documento navegável estilo Notion"
→ **handbook**. Se tiver < 4 h2 e couber em uma página rolável sem sidebar, é **scrollytelling** (sem chart, simplificado).

### "Quero uma central de processos com 20+ entradas"
→ **handbook** (sidebar com 20 links é melhor que grid de 20 cards). Use `hub` se as entradas pedirem agrupamento por categoria com filtro.

### "Quero um onboarding pra novato"
→ **handbook** (referencial, lido em ordem mas consultado depois) OU **scrollytelling** (se for narrativa "primeiros 30 dias passo a passo" lida 1× e nunca mais). Padrão: handbook.

### "Quero um relatório anual"
→ **scrollytelling** se for narrativa com dados (charts sticky pedem scrollytelling). **handbook** se for referencial com seções independentes.

### "Não sei"
→ Pergunte com a árvore acima. Não chute.

---

## Quando perguntar ao usuário (em vez de inferir)

Sempre perguntar se:
1. O pedido é "apresentação" ou "deck" mas sem mencionar se é ao vivo. → Pergunte: *"Vai apresentar ao vivo (deck) ou distribuir para leitura (scrollytelling)?"*
2. O pedido cita conteúdo de tamanho intermediário (5-8 seções). → Pergunte densidade e se há charts.
3. O pedido é "página interna" sem mais detalhes. → Pergunte se é um portal de recursos (hub), um institucional (site) ou um documento longo (handbook).

---

## Conversões entre modelos

Quando o usuário muda de ideia depois de gerado, `/converter-modelo <novo>` cobre as conversões compatíveis:

| De → Para | Viável? | Notas |
|---|---|---|
| handbook → scrollytelling | Sim | Vira página única, sidebar some, h2 viram seções com `data-reveal`. |
| scrollytelling → handbook | Sim | Adiciona sidebar + TOC, divide em h2 navegáveis. |
| hub → site | Sim | Cards viram top-nav, conteúdo dos cards vira `<article class="view">`. |
| site → hub | Sim | Views viram cards na home. |
| deck → scrollytelling | Difícil | Slides viram seções, mas conteúdo costuma ser raso demais (tipografia gigante esconde isso). Avisar. |
| qualquer → deck | Não conversão automática. | Deck pede slide-by-slide pensado. Recriar do zero a partir do conteúdo. |
