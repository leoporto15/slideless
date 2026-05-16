# Modelo `hub`

Portal com grid de cards categorizáveis + painéis in-page. Para centrais de recursos, catálogos de serviços, hubs de time.

**Referência mental:** Notion Workspace, Apple Developer hub, Vercel guides index.
**Exemplo:** [../../assets/exemplos/exemplo-hub.html](../../assets/exemplos/exemplo-hub.html).
**Template vazio:** [../../assets/templates/template-hub.html](../../assets/templates/template-hub.html).

---

## Anatomia

```
┌─────────────────────────────────────────────────────────────┐
│  topbar                                                     │
├─────────────────────────────────────────────────────────────┤
│  header curto: h1 + lead + chips de filtro                  │
├─────────────────────────────────────────────────────────────┤
│  grid de cards (3-4 colunas) com data-category              │
│  [card] [card] [card] [card]                                │
│  [card] [card] [card] [card]                                │
├─────────────────────────────────────────────────────────────┤
│  painéis in-page (revelados ao clicar em um card)           │
└─────────────────────────────────────────────────────────────┘
```

---

## Quando usar

| ✓ Use quando | ✗ Não use quando |
|---|---|
| 8+ recursos independentes | Conteúdo é narrativa única → [scrollytelling](scrollytelling.md) |
| Leitor escolhe o que abrir | Conteúdo precisa ler em ordem → [handbook](handbook.md) |
| Categorias claras (Dados, Eng, Negócio) | Sem categorias claras → [site](site.md) ou [handbook](handbook.md) |
| Filtros são úteis | < 5 itens → não precisa de grid |

---

## Filtros funcionais

Chips no topo do grid. Click filtra cards (não decorativo).

```html
<div class="filters" role="tablist">
  <button class="filter is-active" data-filter="all">Todos</button>
  <button class="filter" data-filter="dados">Dados</button>
  <button class="filter" data-filter="engenharia">Engenharia</button>
</div>

<div class="grid">
  <a class="card" data-category="dados" data-target="#painel-catalogo">…</a>
  …
</div>
```
```js
document.querySelectorAll('.filter').forEach(f => f.addEventListener('click', e => {
  const cat = e.currentTarget.dataset.filter;
  document.querySelectorAll('.filter').forEach(x => x.classList.toggle('is-active', x === e.currentTarget));
  document.querySelectorAll('.card').forEach(c => {
    c.style.display = (cat === 'all' || c.dataset.category === cat) ? '' : 'none';
  });
}));
```

---

## Cards

```html
<a class="card" data-category="dados" data-target="#painel-catalogo">
  <div class="card__icon" aria-hidden="true">📊</div>
  <h3 class="card__title">Catálogo de Dados</h3>
  <p class="card__desc">Busca e linhagem para 2.400 tabelas.</p>
  <span class="card__cta">Abrir →</span>
</a>
```

**Regras:**
- Ícone 28-40px (NÃO gigante — anti-pattern A7)
- Título h3 1.25rem (não pode parecer slide hero)
- Descrição curta (1-2 linhas)
- Hover: leve translateY(-2px), border accent, shadow

**Anti-pattern:** card com ícone 96px + título 2.5rem + descrição vaga = "slide em grid". Cards precisam ser informativos.

---

## Painéis in-page

Cards apontam para painéis dentro da mesma página via `data-target`:

```html
<a class="card" data-target="#painel-catalogo">…</a>

<section class="panel" id="painel-catalogo" hidden>
  <button class="panel__close" type="button">✕ Fechar</button>
  <h2>Catálogo de Dados</h2>
  <p class="lead">…</p>
  <p>Conteúdo detalhado…</p>
</section>
```
```js
document.querySelectorAll('.card[data-target]').forEach(card => {
  card.addEventListener('click', e => {
    e.preventDefault();
    const tgt = document.querySelector(card.dataset.target);
    document.querySelectorAll('.panel').forEach(p => { p.hidden = p !== tgt; });
    tgt.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
document.querySelectorAll('.panel__close').forEach(b => b.addEventListener('click', e => {
  e.target.closest('.panel').hidden = true;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}));
```

**Alternativa:** se o conteúdo do card couber inline no card expandido (não exige scroll), usar `<details>` em vez de painel separado.

---

## Tipografia hub

Editorial igual ao handbook. H1 ~2.5rem, body 1rem.

---

## Print

```css
@media print {
  .filters, .card__cta { display: none; }
  .panel { display: block !important; page-break-before: always; }
  .grid { display: block; }
  .card { break-inside: avoid; margin-bottom: var(--space-5); }
}
```

---

## Checks específicos

- [ ] Grid funcional com cards
- [ ] Filtros realmente filtram (não só visuais)
- [ ] Cards têm `cursor: pointer` e `:focus-visible`
- [ ] Painéis abrem in-page (sem navegação)
- [ ] Card tem ícone pequeno (não hero)
