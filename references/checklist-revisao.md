# Checklist de revisão (LLM)

Complementa o validador determinístico (`scripts/validar.py`). O validador checa o sintático; este checklist checa o semântico, editorial e a11y avançado.

Aplicar antes de entregar — ou via comando `/auditar`.

Priorize por categoria: **🚫 bloqueante > ⚠️ alto > 🟡 médio > 💡 sugestão**.

---

## 🚫 Bloqueantes (corrigir antes de entregar)

- [ ] Documento single-file? (zero `<link>` ou `<script>` para arquivos locais externos)
- [ ] Boot script de tema no `<head>` antes do CSS?
- [ ] Dark mode funciona sem flash? Trocar tema preserva conteúdo?
- [ ] Conteúdo é do usuário (nenhum lorem ipsum, nenhum dado interno do Itaú inventado)?
- [ ] Validador determinístico passa (`python scripts/validar.py`)?
- [ ] Anti-patterns do tipo "PPT-em-HTML" ausentes? (ver [anti-patterns.md](anti-patterns.md) A1-A8 para modelos não-deck)

---

## ⚠️ Alto

### Estrutura semântica
- [ ] Um único `<h1>` por documento (ou por view em `site`/painel em `hub`)
- [ ] Hierarquia de headings sem saltos (`h2` → `h3`, não `h2` → `h4`)
- [ ] Landmarks ARIA: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` onde aplicável
- [ ] `lang="pt-BR"` no `<html>`

### Tema
- [ ] Todo token `--color-*` definido em `:root` tem override em `[data-theme="dark"]`
- [ ] Acent (`--color-accent`) tem contraste AA com fg sobre ele (`--color-accent-fg`)
- [ ] Nenhum hex hardcoded fora de `:root` / `[data-theme]` / `--itau-*`

### Tipografia
- [ ] H1 editorial ~2.5rem (modelos não-deck)
- [ ] Lead com `max-width: 60ch`, parágrafos com `max-width: 65ch`
- [ ] `--font-display` para headings, `--font-text` para corpo
- [ ] No `deck`: tipografia via `clamp()` (fluida ao viewport)

### Modelo específico
**handbook:**
- [ ] Sidebar presente com scrollspy funcional
- [ ] TOC sticky se houver 3+ h2
- [ ] `scroll-margin-top` nos headings (não escondem atrás do topbar)

**hub:**
- [ ] Filtros funcionais (não decorativos)
- [ ] Cards têm `cursor: pointer` e foco visível
- [ ] Painel abre in-page, não navega

**scrollytelling:**
- [ ] Progress bar no topo refletindo scroll
- [ ] Reveals com Intersection Observer, não com `setTimeout`
- [ ] Sticky chart (se presente) muda com base na seção visível, não no scroll bruto

**site:**
- [ ] Hash routing funcional (`#home`, `#sobre`, etc.)
- [ ] Reload em `/path#sobre` renderiza a view correta (não home como default sempre)
- [ ] `hidden` attribute nas views não-ativas (não só CSS)

**deck:**
- [ ] Keyboard handler: `ArrowRight`, `ArrowLeft`, `Space`, `Esc` (fullscreen out)
- [ ] Fragments revelam em ordem (não todos de uma vez)
- [ ] Indicador de slide visível (X / Y)
- [ ] Toggle fullscreen funcional
- [ ] Transições < 800ms

---

## 🟡 Médio

### Conteúdo
- [ ] Tom editorial — sem marketing-pitch ("revolucione…", "transforme…")
- [ ] Bullets convertidos em parágrafos onde fizerem mais sentido
- [ ] `<ul>` com > 6 itens? Considerar reorganizar
- [ ] Callouts usados com semântica correta (info ≠ tip ≠ warn ≠ danger)
- [ ] Code blocks com `data-lang` correto
- [ ] Imagens com `alt` descritivo (ou `alt=""` se decorativas)
- [ ] Links têm texto descritivo (não "clique aqui")

### Visual
- [ ] Espaçamento usa tokens `--space-*`, não números soltos
- [ ] Sombras usam tokens `--shadow-*`
- [ ] Bordas usam `--color-border` ou `--color-border-strong`
- [ ] Counters animam apenas uma vez (unobserve após visível)

### Animação
- [ ] `@media (prefers-reduced-motion: reduce)` desabilita tudo
- [ ] Nenhuma animação infinita decorativa
- [ ] Reveals com threshold ~0.15, rootMargin negativo no bottom

### A11y
- [ ] `:focus-visible` com outline accent
- [ ] Botões têm `type="button"` (não submetem form inadvertidamente)
- [ ] Toggles (`<details>`) acessíveis por teclado
- [ ] Tabs com `role="tab"` + `aria-selected`
- [ ] Theme toggle com `aria-label`

---

## 💡 Sugestão

- [ ] Meta `description` no `<head>` para preview de link
- [ ] `og:title` / `og:description` se for compartilhado
- [ ] Favicon (data-URI) para personalidade
- [ ] `print` styles que escondem nav/sidebar
- [ ] Counters formatados conforme locale (`pt-BR`: vírgula decimal, ponto milhar)
- [ ] Charts respeitam tema (cores via CSS vars lidas no JS)
- [ ] Imagens com `loading="lazy"` exceto a primeira da viewport

---

## Como aplicar

1. Ler o HTML do início ao fim, anotando cada quebra.
2. Listar violações por prioridade.
3. Corrigir bloqueantes primeiro.
4. Aplicar `/polir` se sobrarem altos visuais; `/harden` se sobrarem altos de a11y.
5. Re-rodar validador determinístico.
6. Re-aplicar este checklist (rápido — só os pontos tocados).
