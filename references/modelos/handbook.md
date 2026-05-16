# Modelo `handbook`

Manual com sidebar fixa + conteúdo central + TOC sticky. Para documentação longa, manuais, onboarding, runbooks, políticas internas.

**Referência mental:** GitLab Handbook, Stripe Docs, Notion Pages.
**Exemplo:** [../../assets/exemplos/exemplo-handbook.html](../../assets/exemplos/exemplo-handbook.html).
**Template vazio:** [../../assets/templates/template-handbook.html](../../assets/templates/template-handbook.html).

---

## Anatomia

```
┌─────────────────────────────────────────────────────────────┐
│  topbar (sticky)                                            │
├──────────┬──────────────────────────────────────┬───────────┤
│          │                                      │           │
│  sidebar │  content                             │   TOC     │
│  (nav)   │  (coluna 720px max)                  │  sticky   │
│  sticky  │  - h1 + lead                         │  scroll-  │
│  scroll- │  - section data-reveal               │   spy     │
│  spy     │  - h2 + parágrafos + componentes     │           │
│          │  - h3 + ...                          │           │
│          │                                      │           │
└──────────┴──────────────────────────────────────┴───────────┘
```

Grid: `grid-template-columns: var(--sidebar-w) 1fr var(--toc-w);` num `max-width: 1400px` centralizado.

---

## Quando usar

| ✓ Use quando | ✗ Não use quando |
|---|---|
| 8+ seções com hierarquia | 1-3 seções rasas → [scrollytelling](scrollytelling.md) |
| Leitor consulta múltiplas vezes (referencial) | Leitor lê uma vez de cima a baixo → [scrollytelling](scrollytelling.md) |
| Sidebar de navegação ajuda | Recursos independentes sem hierarquia → [hub](hub.md) |
| Densidade alta de texto | Conteúdo curto com dados visuais → [scrollytelling](scrollytelling.md) |
| Onboarding, manual, política | Apresentação ao vivo → [deck](deck.md) |

---

## Componentes específicos do handbook

### Sidebar com scrollspy
Ver [../componentes.md](../componentes.md#sidebar-nav--scrollspy-handbook).

Estrutura mínima:
```html
<aside class="sidebar" aria-label="Navegação principal">
  <nav class="sidebar__group">
    <p class="sidebar__heading">Plataforma</p>
    <ul class="sidebar__list">
      <li><a href="#visao-geral" class="is-active">Visão geral</a></li>
      …
    </ul>
  </nav>
</aside>
```

Cada link da sidebar aponta para um `id` de uma seção do conteúdo. Scrollspy via IntersectionObserver, conforme [componentes.md](../componentes.md).

### TOC sticky
- Mostra **apenas** os `<h2>` da seção visível, ou todos os h2/h3 do documento (escolha pela densidade).
- Some no mobile (< 1024px).
- `position: sticky; top: calc(var(--header-h) + var(--space-5));`

### Anchor links (`#`)
Headings revelam um `#` ao hover:
```css
h2::before, h3::before {
  content: '#';
  position: absolute;
  left: -1.4em;
  color: var(--color-accent);
  opacity: 0;
  transition: opacity var(--duration-fast);
}
h2:hover::before, h3:hover::before { opacity: 0.6; }
```

### Breadcrumb no topbar
```html
<nav class="topbar__breadcrumb" aria-label="Localização">
  <a href="#">Plataforma</a>
  <span class="topbar__sep">/</span>
  <strong>Handbook</strong>
</nav>
```

---

## Tipografia handbook

| Token | Valor |
|---|---|
| h1 | `--size-h1` (2.5rem) |
| h2 | `--size-h2` (1.75rem) |
| h3 | `--size-h3` (1.25rem) |
| body | `--size-body` (1rem) |
| lead | `--size-lead` (1.1875rem) — primeira frase após h1 |

`line-height: 1.65` no body, `line-height: 1.25` nos headings.

**Coluna de texto:** `max-width: var(--content-max)` (720px). Parágrafos `max-width: 65ch`, lead `max-width: 60ch`.

---

## Reveals leves

`data-reveal` em cada `<section>` para fade-in suave. **Threshold alto** (0.15) e rootMargin negativo no bottom — o reveal acontece naturalmente, sem chamar atenção.

```html
<section id="dados" data-reveal>
  <h2>Catálogo de Dados</h2>
  …
</section>
```

Não usar reveal em elementos internos (parágrafos, listas). Reveal é da seção inteira.

---

## Print

```css
@media print {
  .topbar, .sidebar, .toc, .theme-toggle { display: none; }
  .layout { display: block; }
  .content { padding: 0; max-width: 100%; }
  h2 { page-break-after: avoid; }
  .callout, .code, .toggle { break-inside: avoid; }
}
```

---

## Esqueleto mínimo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>… — Handbook</title>
  <script>/* boot script de tema */</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>/* tokens + componentes */</style>
</head>
<body>
  <header class="topbar">
    <a href="#" class="topbar__brand">
      <img class="topbar__logo" alt="" src="…">
      <span>Itaú · Plataforma de Dados</span>
    </a>
    <nav class="topbar__breadcrumb">…</nav>
    <span class="topbar__spacer"></span>
    <input class="topbar__search" placeholder="Buscar…">
    <button class="theme-toggle" aria-label="Alternar tema">◐</button>
  </header>

  <div class="layout">
    <aside class="sidebar">…</aside>
    <main class="content">
      <div class="content__inner">
        <p class="content__meta">…</p>
        <h1>Título</h1>
        <p class="lead">…</p>

        <section id="secao-1" data-reveal>
          <h2>Seção</h2>
          <p>…</p>
        </section>
      </div>
    </main>
    <aside class="toc" aria-label="Nesta página">…</aside>
  </div>

  <script>/* theme toggle, scrollspy, reveals, copy buttons */</script>
</body>
</html>
```

---

## Checks específicos

- [ ] `.sidebar` existe e tem links com `#` anchors
- [ ] `.toc` existe se houver 3+ `<h2>`
- [ ] Scrollspy adiciona `.is-active` no link da seção visível
- [ ] `scroll-margin-top` nos h2/h3 = `calc(var(--header-h) + var(--space-4))`
- [ ] H1 ~2.5rem (não gigante)
- [ ] Tema `itau` aplica `font-display: 'Itau Display'`
