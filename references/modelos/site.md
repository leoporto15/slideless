# Modelo `site`

SPA single-file com hash routing entre 2-5 views. Para microsites, lançamentos internos, portfólio de squad.

**Referência mental:** Linear, Vercel guides, Notion product pages.
**Exemplo:** [../../assets/exemplos/exemplo-site.html](../../assets/exemplos/exemplo-site.html).
**Template vazio:** [../../assets/templates/template-site.html](../../assets/templates/template-site.html).

---

## Anatomia

```
┌─────────────────────────────────────────────────────────────┐
│  topbar com nav (#home #sobre #recursos #equipe)            │
├─────────────────────────────────────────────────────────────┤
│  view ativa (article)                                       │
│    - hero da view                                           │
│    - seções da view                                         │
├─────────────────────────────────────────────────────────────┤
│  footer comum                                               │
└─────────────────────────────────────────────────────────────┘
```

Único arquivo HTML. Trocar view = trocar hash. Sem reload.

---

## Quando usar

| ✓ Use quando | ✗ Não use quando |
|---|---|
| 2-5 views distintas e independentes | 1 view longa → [handbook](handbook.md) ou [scrollytelling](scrollytelling.md) |
| Cada view tem identidade própria | Múltiplos recursos em grid → [hub](hub.md) |
| Microsite interno, landing | Apresentação ao vivo → [deck](deck.md) |
| Cara de "site" mais que "documento" | Conteúdo denso e referencial → [handbook](handbook.md) |

---

## Hash routing

```html
<header class="topbar">
  <a href="#home" class="topbar__brand">Squad X</a>
  <nav class="topnav">
    <a href="#home" class="topnav__link">Home</a>
    <a href="#sobre" class="topnav__link">Sobre</a>
    <a href="#recursos" class="topnav__link">Recursos</a>
    <a href="#equipe" class="topnav__link">Equipe</a>
  </nav>
  <button class="theme-toggle" aria-label="Alternar tema">◐</button>
</header>

<main>
  <article class="view is-active" id="home">…</article>
  <article class="view" id="sobre" hidden>…</article>
  <article class="view" id="recursos" hidden>…</article>
  <article class="view" id="equipe" hidden>…</article>
</main>
```
```js
function route() {
  const id = (location.hash || '#home').slice(1);
  document.querySelectorAll('.view').forEach(v => {
    const on = v.id === id;
    v.classList.toggle('is-active', on);
    v.hidden = !on;
  });
  document.querySelectorAll('.topnav__link').forEach(a => {
    a.classList.toggle('is-active', a.getAttribute('href') === '#' + id);
  });
  window.scrollTo({ top: 0, behavior: 'instant' });
}
addEventListener('hashchange', route);
addEventListener('DOMContentLoaded', route);
```

**Regras:**
- `hidden` é atributo HTML, não só CSS. Garante a11y.
- Reload em `…/index.html#sobre` cai direto na view `sobre` (porque o route() roda no `DOMContentLoaded`).
- View ativa: `.is-active` (sem `hidden`). Inativas: `hidden`.

---

## Estrutura de cada view

```html
<article class="view" id="sobre" hidden>
  <section class="view__hero">
    <h1>Sobre</h1>
    <p class="lead">Quem somos…</p>
  </section>

  <section class="view__body" data-reveal>
    <h2>História</h2>
    <p>…</p>
  </section>
</article>
```

Hero da view é mais discreto que hero de scrollytelling — `<h1>` 2.5rem, lead 1.2rem. Não é hero pitch.

---

## Tipografia site

Editorial. Mesmas regras de [design-system.md](../design-system.md).

---

## Transições entre views

Fade simples:
```css
.view { opacity: 0; transition: opacity 200ms var(--ease-out); }
.view.is-active { opacity: 1; }
```

Não usar `transform: translateX()` deslizando — vira PPT. Fade é suficiente.

---

## Print

Todas as views aparecem em ordem:
```css
@media print {
  .view { display: block !important; opacity: 1 !important; }
  .view[hidden] { display: block !important; }
  .topnav { display: none; }
  .view + .view { page-break-before: always; }
}
```

---

## Checks específicos

- [ ] Hash routing funcional (`#home`, etc.)
- [ ] `hidden` attribute nas views não-ativas (não só CSS)
- [ ] Reload em `#sobre` cai em `#sobre`, não `#home`
- [ ] `.topnav__link.is-active` reflete view atual
- [ ] Sem `<a href="*.html">` para outros arquivos (single-file)
- [ ] Transição via opacity, não translate
