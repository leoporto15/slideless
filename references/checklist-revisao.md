# Checklist de revisão (LLM)

Complementa o validador determinístico (`scripts/validar.py`). O validador checa o sintático; este checklist checa o semântico, editorial e a11y avançado.

Aplicar antes de entregar — ou via comando `/slideless auditar`.

Priorize por categoria: **🚫 bloqueante > ⚠️ alto > 🟡 médio > 💡 sugestão**.

---

## 🚫 Bloqueantes (corrigir antes de entregar)

- [ ] Documento single-file? (zero `<link>` ou `<script>` para arquivos locais externos)
- [ ] Boot script de tema no `<head>` antes do CSS?
- [ ] Dark mode funciona sem flash? Trocar tema preserva conteúdo?
- [ ] Conteúdo é do usuário (nenhum lorem ipsum, nenhum dado interno do Itaú inventado)?
- [ ] Validador determinístico passa (`python scripts/validar.py`)?
- [ ] Anti-patterns do tipo "PPT-em-HTML" ausentes? (ver [anti-patterns.md](anti-patterns.md) A1-A8 para modelos não-deck)
- [ ] Bloco `<!-- slideless:parti -->` presente e completo no `<head>`, com as **7 decisões** (registro, kit, capa, superfície+luz, motion, ambição, assinatura) + `nao-vai-ter`? ([direcao-de-arte.md](direcao-de-arte.md))

---

## 🎨 Direção de arte (categoria P — fingerprint risk)

- [ ] 🔴 **Swap test**: cobrindo o logo e o laranja, este documento é distinguível do exemplo canônico do modelo e do último documento da pasta? (comparar blocos parti — capa, kit e superfície não coincidem com o canônico)
- [ ] 🔴 Cada decisão do parti cita um elemento concreto da fonte (substantivo/número/tensão)? Justificativa genérica ("moderno", "elegante") = reprovado
- [ ] 🔴 `nao-vai-ter` cumprido — os 3 padrões declarados ausentes do HTML (o validador checa por regex)
- [ ] 🔴 Parti↔HTML coerentes: a capa declarada É a capa; o perfil de motion declarado determina os keyframes que existem (estático = zero keyframe de entrada)
- [ ] ⚠️ Momento assinatura existe NO LOCAL declarado e anima/protagoniza o **dado-tese** (não um número de apoio)
- [ ] ⚠️ Quotas (isenção: docs <5 seções/slides): kicker mono em ≤1 papel · `<em>` accent em ≤25% dos títulos · ≤2 grids de cards · reveal em ≤40% das sections · ≥1 seção fora do padrão título+grid a cada 4
- [ ] ⚠️ Headlines-tese: h2 contém verbo ou número da fonte (não "Visão Geral"/"Conclusão")
- [ ] ⚠️ Chart.js: `Chart.defaults.font.family` dos tokens + formatação pt-BR nos ticks + gráfico-tese com ≥1 anotação + tension 0 em dado discreto
- [ ] ⚠️ Microtipografia: tabular-nums em tabelas/KPIs · aspas curvas · NBSP valor↔unidade · text-wrap balance/pretty
- [ ] 🟡 Último terço do documento mantém a densidade de decisão do primeiro (anti-drift)
- [ ] 🟡 Cor com papel: regime cromático declarado respeitado; paleta nunca distribuída em sequência decorativa

### 🚀 Ambição (A2/A3 — [ambicao.md](ambicao.md))

- [ ] 🔴 `ambicao` declarada e coerente com o registro (A3 proibido em regulatório/RI)
- [ ] 🔴 momentos-wow (W1-W31) na densidade do nível (**A1 1-2 calmos · A2 3-5 · A3 6-8 ≥4 famílias**), cada um ligado ao **dado-tese** (não decorativo)
- [ ] 🔴 Cada gesto de ponta: `@supports` + estado-final-base (conteúdo aparece num Chrome sem a feature) + branch reduced-motion
- [ ] ⚠️ Régua de craft: curvas nomeadas (não `ease` default), teto 300ms em UI, `.no-transitions` no toggle de tema
- [ ] ⚠️ Materialidade respeita o registro (report = grain estático + specular; nada de glass/WebGL/aurora saturada)
- [ ] 🟡 Teste do "parar o scroll": algum momento faria um diretor de arte parar? (A2 sem destaque = ambição não realizada)

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
4. Aplicar `/slideless polir` se sobrarem altos visuais; `/slideless harden` se sobrarem altos de a11y.
5. Re-rodar validador determinístico.
6. Re-aplicar este checklist (rápido — só os pontos tocados).
