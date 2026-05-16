# Design system — slideless

Tokens, dark mode, boot script. **Ler antes de gerar qualquer HTML.**

---

## Filosofia

Estética **Notion/GitLab handbook** — densa, editorial, legível. Não é deck (exceção: modelo `deck`). Toda decisão visual subordina-se à pergunta: *"isso aqui pareceria um slide de PPT?"* Se sim, recuar.

---

## Tokens — sempre via CSS custom properties

Toda cor, tamanho, espaço e duração mora em `:root` e ganha override em `[data-theme="dark"]`. Nunca hardcodar `#ffffff` no meio do CSS — sempre `var(--color-bg)`.

### Cores (tema `itau`)

```css
:root {
  /* Marca Itaú — fixas em ambos os temas */
  --itau-orange:    #FF6200;
  --itau-orange-2:  #F88104;
  --itau-orange-3:  #FA9F09;
  --itau-blue-3:    #3B85FA;
  --itau-yellow:    #FBC305;

  /* Light */
  --color-bg:           #ffffff;
  --color-bg-elevated:  #faf8f5;   /* warm off-white */
  --color-bg-sunken:    #f4f1ec;
  --color-fg:           #1a1a1a;
  --color-fg-muted:     #525252;
  --color-fg-subtle:    #8a8a8a;
  --color-border:       #e8e4dd;
  --color-border-strong:#d4cec3;
  --color-accent:       var(--itau-orange);
  --color-accent-hover: var(--itau-orange-2);
  --color-accent-fg:    #ffffff;
}

[data-theme="dark"] {
  --color-bg:           #14110d;   /* preto quente (não puro) */
  --color-bg-elevated:  #1c1814;
  --color-bg-sunken:    #221d18;
  --color-fg:           #e8eaed;
  --color-fg-muted:     #a8a39a;
  --color-fg-subtle:    #6e6a62;
  --color-border:       #2f2a23;
  --color-border-strong:#403a32;
  --color-accent:       var(--itau-orange-3);   /* mais luminoso no escuro */
  --color-accent-hover: var(--itau-orange-2);
  --color-accent-fg:    #14110d;
}
```

### Callouts

```css
:root {
  --color-info-bg:    rgba(5, 32, 183, 0.06);
  --color-info-border:var(--itau-blue-3);
  --color-tip-bg:     #f0fdf4;
  --color-tip-border: #22c55e;
  --color-warn-bg:    rgba(251, 195, 5, 0.12);
  --color-warn-border:var(--itau-yellow);
  --color-danger-bg:  #fef2f2;
  --color-danger-border:#ef4444;
}
```

### Tipografia

```css
:root {
  --font-text:    'Itau Text', 'Inter', -apple-system, system-ui, sans-serif;
  --font-display: 'Itau Display', 'Inter', -apple-system, system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'SF Mono', Consolas, monospace;

  /* Escala editorial — handbook/hub/scrollytelling/site */
  --size-h1:    2.5rem;
  --size-h2:    1.75rem;
  --size-h3:    1.25rem;
  --size-h4:    1.0625rem;
  --size-lead:  1.1875rem;
  --size-body:  1rem;
  --size-small: 0.9375rem;
  --size-xs:    0.8125rem;
  --size-code:  0.875rem;
}
```

**No modelo `deck`** usar `clamp()` para tipografia fluida (porque é viewport-cheio):
```css
.title-xl { font-size: clamp(2.75rem, 6.5vw, 6rem); }
.big-num__val { font-size: clamp(5rem, 16vw, 14rem); }
```
**Em qualquer outro modelo, tipografia > 3rem é proibida.** Ver [anti-patterns.md](anti-patterns.md).

### Espaço, raios, sombras, easing

```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem;    --space-5: 1.5rem; --space-6: 2rem;
  --space-7: 2.5rem;  --space-8: 3rem;   --space-10: 4rem;
  --space-12: 5rem;

  --content-max: 720px;     /* coluna de texto handbook */
  --sidebar-w:   268px;
  --toc-w:       220px;
  --header-h:    56px;

  --radius-sm: 4px;
  --radius:    8px;
  --radius-lg: 12px;

  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow:    0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
  --shadow-lg: 0 4px 6px rgba(0,0,0,0.05), 0 10px 24px rgba(0,0,0,0.08);

  --ease:      cubic-bezier(0.22, 1, 0.36, 1);
  --ease-out:  cubic-bezier(0, 0, 0.2, 1);
  --duration-fast: 150ms;
  --duration:      250ms;
}

[data-theme="dark"] {
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.4);
  --shadow:    0 1px 3px rgba(0,0,0,0.4), 0 4px 12px rgba(0,0,0,0.3);
  --shadow-lg: 0 4px 6px rgba(0,0,0,0.4), 0 10px 24px rgba(0,0,0,0.5);
}
```

---

## Boot script — OBRIGATÓRIO no `<head>`, antes do CSS

Roda síncrono antes do CSS pintar para evitar flash de tema errado.

```html
<script>
  (function() {
    try {
      var t = localStorage.getItem('theme') ||
              (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', t);
    } catch (e) {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  })();
</script>
```

O validador `scripts/validar.py` falha se este snippet (ou equivalente) não estiver presente no `<head>` antes da primeira tag `<link rel="stylesheet">` ou `<style>`.

---

## Theme toggle — botão no header

```html
<button class="theme-toggle" aria-label="Alternar tema" type="button">
  <span aria-hidden="true">◐</span>
</button>
```
```js
document.querySelector('.theme-toggle')?.addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme');
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  try { localStorage.setItem('theme', next); } catch {}
});
```

---

## Fontes Itaú

Itaú Display e Itaú Text são proprietárias. Fora da rede interna, **fallback automático** para Inter (Google Fonts). Nunca falhar a geração por causa de fontes.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Para deck adicione peso 800 ao Inter:
```
family=Inter:wght@400;500;600;700;800
```

---

## Tema `neutro` — variação azul

Mesmo sistema, com:
- `--color-accent: #2563eb` (azul) substituindo `--itau-orange` no light
- `--color-accent: #60a5fa` no dark
- Sem fontes Itaú: `--font-text: 'Inter'`, `--font-display: 'Inter'`
- Fundos neutros frios (não warm): `--color-bg-elevated: #f8fafc`, dark `#0f172a`
- Sem `--itau-*` tokens

Ver [temas/neutro.md](temas/neutro.md) e `assets/temas/neutro.css`.

---

## Regras inegociáveis

1. Boot script no `<head>` antes do CSS.
2. Toda cor via `var(--color-*)`. Nunca hex hardcoded no corpo do CSS (exceto dentro de `:root` ou `[data-theme]`).
3. `[data-theme="dark"]` override completo de todos os tokens semânticos.
4. Tipografia editorial nos 4 modelos não-deck. Tipografia gigante via `clamp()` só no deck.
5. `prefers-reduced-motion: reduce` desabilita transições e animações.
6. Foco visível: `:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }`.
