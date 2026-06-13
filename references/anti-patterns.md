# Anti-patterns — o que NÃO fazer

A v1 desta skill foi rejeitada por gerar "PPT estilizado em HTML". Esta lista codifica os erros a evitar. **Ler antes da primeira geração da sessão.**

O validador determinístico (`scripts/validar.py`) checa um subconjunto destas regras via regex/DOM. O resto é responsabilidade do LLM revisor (`/auditar`).

---

## A. Anti-patterns visuais (PPT-isms)

### A1. Tipografia gigante fora do `deck`
**Errado:** `<h1 style="font-size: 5rem">` em handbook/hub/site/scrollytelling.
**Por quê:** documento web é editorial (Notion/GitLab), não slide ao vivo. H1 ~2.5rem.
**Permitido só em:** modelo `deck`, via `clamp()` (porque é viewport-cheio).
**Detectado por:** validar.py via regex `font-size:\s*([4-9]|\d{2,})(\.\d+)?rem` cruzado com tipo do documento.

### A2. Slide-style padding gigante em conteúdo
**Errado:** `<section style="padding: 10vw 15vw">` em handbook ou hub.
**Por quê:** vibe "câmara branca de slide". Em handbook a coluna tem `max-width: 720px` e padding `var(--space-8)`.
**Permitido só em:** deck (que usa `padding: 8vh 10vw` no `.slide`).

### A3. Bullet point overload
**Errado:** `<ul>` com 8+ itens, cada um uma frase curta tipo bullet de PPT.
**Por quê:** PPT compensa falta de texto com listas. Documento web prefere parágrafos curtos com hierarquia (`<h3>` + parágrafo) ou cards.
**Regra:** se houver `<ul>` com mais de 6 `<li>`, considerar reescrever como sub-seções com h3 ou converter em `cards`.

### A4. Animação decorativa sem função
**Errado:** parallax dramático, glow pulsante, particle background, gradient animado, "hero" com mouse-tracking.
**Por quê:** documento interno se lê — não impressiona. Animação só quando carrega informação (reveal de seção, contador chegando ao valor, fragment do deck).
**Permitido:** `data-reveal` (intersection observer), counters animados, deck fragments, transição de slide.

### A5. Hero gigante estilo landing page
**Errado:** primeira tela = 100vh com título 6rem centralizado + emoji 8rem + CTA pulsante.
**Por quê:** handbook abre com `<h1>` + `lead` + começa a entregar conteúdo na primeira rolagem. Hub abre com header curto + grid de cards. Só deck tem slide-hero.

### A6. Margem branca dramática
**Errado:** `body { padding: 0 20%; }` em handbook.
**Por quê:** mimicry de slide. Coluna de texto é `--content-max: 720px` centralizada, com sidebar e TOC nas laterais.

### A7. Ícones gigantes "pitch"
**Errado:** ícones 96-128px coloridos no início de cada card.
**Por quê:** card editorial tem ícone 20-28px ou nenhum. Deck pode ter ícones maiores.

### A8. Cor decorativa sem propósito semântico
**Errado:** seções alternando fundo laranja claro / azul claro só para "quebrar visualmente".
**Por quê:** cor reservada para semântica (callouts, accent em links/CTAs, acentos em h2 hover). Background é sempre `--color-bg` ou `--color-bg-elevated`.

---

## B. Anti-patterns técnicos

### B1. Multi-arquivo
**Errado:** `<link href="style.css">` para arquivo externo.
**Permitido:** Google Fonts e Chart.js via CDN. Tudo o mais inline.
**Por quê:** entrega single-file é o contrato.
**Detectado por:** validar.py grep `<link rel="stylesheet" href="(?!https)"`.

### B2. Falta de boot script de tema
**Errado:** definir tema só via CSS sem boot inline ⇒ flash de tema errado.
**Detectado por:** validar.py procura por `localStorage.getItem('theme')` no primeiro `<script>` do `<head>`.

### B3. Hex hardcoded no corpo do CSS
**Errado:** `.card { background: #ffffff }`.
**Certo:** `.card { background: var(--color-bg) }`.
**Exceções:** dentro de `:root` ou `[data-theme="..."]`, e os tokens `--itau-*` que são marca.
**Detectado por:** validar.py warning (não erro) para hex fora de `:root`/`[data-theme]`.

### B4. Faltando override `[data-theme="dark"]`
**Errado:** definir `--color-bg` em `:root` e esquecer no dark. Resultado: dark mode quebrado.
**Detectado por:** validar.py compara conjunto de tokens semânticos definidos em `:root` vs `[data-theme="dark"]`.

### B5. Sem `prefers-reduced-motion`
**Errado:** animações sempre rodando.
**Certo:** bloco `@media (prefers-reduced-motion: reduce) { ... }` desabilita transitions/animations.
**Detectado por:** validar.py grep `prefers-reduced-motion`.

### B6. Sem foco visível
**Errado:** `*:focus { outline: none }`.
**Certo:** `:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }`.

### B7. Keyboard nav ausente no deck
**Errado:** deck sem handler para `ArrowLeft`, `ArrowRight`, `Space`, `Escape` (sair fullscreen).
**Detectado por:** validar.py em `tipo=deck` exige `keydown` listener com `ArrowRight` ou similar.

### B8. Heading skip
**Errado:** `<h1>` direto pra `<h4>` saltando `<h2>`/`<h3>`. Quebra a11y e o scrollspy.

---

## C. Anti-patterns de conteúdo

### C0. Compactar / cortar conteúdo da fonte (REGRA-MÃE)
**Proibido cortar informação do material original do usuário.** Se a fonte tem 10 marcos na timeline, o output preserva os 10. Se tem 8 mesas, todas vão. Se há 3 camadas hierárquicas (top/core/base), todas aparecem.

**Errado:** "esse marco vai dificultar o layout, vou tirar"; "esse atributo é redundante, simplifico"; "isso aqui não acrescenta ao pitch, vou pra footnote".
**Certo:** se o slide ficar denso, **dividir em N+1 slides** ou usar fragments. Densidade visual ≠ compactação semântica.

**Como aplicar antes de gerar:**
1. Contar elementos discretos da fonte (slides, bullets, marcos, métricas, nomes, contatos).
2. Mapear cada elemento para algum slide/seção do output.
3. Se algum elemento ficou sem destino, parar e replanejar.
4. Não é alçada da skill decidir o que "acrescenta" — é alçada do usuário.

### C1. Lorem ipsum
**Proibido sempre.** Sem conteúdo real do usuário, NÃO gerar. Ver [protocolo-sem-conteudo.md](protocolo-sem-conteudo.md).

### C2. Dados internos do Itaú inventados
**Errado:** "Plataforma processa 2.4 bi de eventos/dia". Se não veio do usuário, não vai pro HTML real (showcases fictícios em `assets/exemplos/` são exceção — são placeholders explícitos da skill).

### C3. Tom marketing-pitch em documento interno
**Errado:** "Revolucione sua jornada de dados!".
**Certo:** "Catálogo cobre 2.400 tabelas; busca por owner e linhagem."

### C4. Misturar `<br>` para fingir parágrafos
**Errado:** `<p>linha 1<br><br>linha 2</p>`.
**Certo:** dois `<p>` separados.

### C5. Limite de slides arbitrário (ex: "10-13")
**Errado:** "fonte tinha 11 slides PPT, gero 12 slideless". Subestima a densidade da fonte.
**Certo:** "fonte tinha 11 slides com média de 4 elementos cada = ~44 elementos. Mapeio em 18-25 slideless". Material denso pede expansão, não cópia 1:1. Ver [modelos/deck.md](modelos/deck.md#expansao-vs-compactacao).

---

## C-bis. Anti-patterns de design fraco — princípios, não receitas

> **Histórico:** a v2 desta seção prescrevia receitas literais (um único easing, glow radial obrigatório, blur fixo no hero). Resultado: todo documento "forte" saiu com o MESMO fingerprint — slop da casa. A v4 converte cada item em princípio + cardápio. **Design forte = decisões derivadas do conteúdo**, declaradas no bloco `<!-- slideless:parti -->` (ver [direcao-de-arte.md](direcao-de-arte.md)). Receita única repetida é design fraco, por melhor que a receita seja.

### C6. Tipografia hero sem `clamp()` fluido
**Errado:** `font-size: 2.5rem` fixo em hero de deck.
**Certo:** escala viewport-responsiva via `clamp()` — `--size-display`, `--size-mega`, `--size-giga` prontos.

### C7. Easing sem papel
**Errado (forma 1):** `transition: all 200ms ease;` — curva default sem decisão.
**Errado (forma 2):** o mesmo `cubic-bezier` para TODOS os movimentos do documento — era a receita da v2 e é fingerprint.
**Certo:** 2–3 curvas nomeadas em `:root`, cada uma com papel comentado (`/* papel: entrada */`, `/* papel: micro-interação */`). Entrada nunca usa a mesma curva que hover. `transition` sempre property-scoped — **`transition: all` é proibido**.

### C8. Fundo sem decisão
**Errado (forma 1):** fundo flat por omissão — ninguém decidiu nada.
**Errado (forma 2):** glow radial em todo documento por obrigação — era a regra da v2; decoração atmosférica universal é a definição de pasteurização e contradiz A4.
**Certo:** tratamento de fundo escolhido por documento do cardápio (flat / flat+vinheta / grain / dot grid / pauta / banda de cor / glow localizado) e registrado no parti. **Flat é opção legítima** — é a escolha certa para report e qualquer documento de impressão. Glow: no máximo 1, atrás de UM elemento específico, nunca wallpaper incondicional em `body::before`.

### C9. Entrada de hero igual em todo documento
**Errado:** o mesmo `heroIn` com blur(16px) em todo deck (receita v2 = fingerprint).
**Certo:** a entrada do hero pertence ao perfil de motion do parti: estático (nenhuma), editorial (fade simples), cinemático (blur-unblur, wipe ou settle — escolher 1). Documento estático SEM animação de hero é válido e frequentemente mais elegante.

### C10. Cor sem regime declarado
**Errado (forma 1):** todos os destaques em `var(--color-accent)` sem intenção.
**Errado (forma 2):** distribuir accent/info/teal/sage/plum em sequência pela ordem do documento ("color-cycling") — uniformidade disfarçada de variedade, e violação do C14.
**Certo:** declarar 1 regime no parti: (a) bicromático ink+accent — legítimo e frequentemente superior; (b) duotone com relação declarada; (c) polícromo semântico SOMENTE com mapeamento explícito (`<!-- cores: teal=crédito, info=macro, plum=risco -->`) e cada cor usada ≥2× no mesmo papel.

### C11. Letter-spacing de valor único
**Errado:** um único valor de tracking para todos os headings (a v2 prescrevia −0.035em fixo — vira fingerprint).
**Certo:** tracking por corpo: negativo em display grande (−0.02 a −0.04em em ≥56px), zero no body, positivo em caps/labels (+0.06 a +0.14em). O documento tem ≥3 valores distintos com sinais diferentes.

### C12. Stagger hardcoded e universal
**Errado (forma 1):** `transition-delay: 200ms/300ms/400ms` repetidos elemento a elemento.
**Errado (forma 2):** stagger linear `calc(var(--i) * 70ms)` aplicado por ordem do DOM a TODO grupo de elementos — o default da v2, hoje um tell.
**Certo:** stagger só dentro de um grupo homogêneo (barras do mesmo gráfico, itens da mesma lista revelada), no máximo 1 grupo por viewport, via `--i` quando usado.

### C13. Sem depth tiers
**Errado:** todas as seções com mesma sombra/padding.
**Certo:** `.tier-hero` / `.tier-default` / `.tier-recessed` — quando o regime de luz do documento usa elevação. Em registro impresso/flat, profundidade vem de fio e contraste, não de sombra.

### C14. Cores semânticas como decoração
**Errado:** seções alternando background sage/teal/plum só pra "variar"; cards numerados recebendo cada um uma cor da paleta em sequência.
**Certo:** cada cor carrega significado (accent=brand, info=dado, success=resultado positivo, teal=técnico/analítico, plum=crítico/atenção). Usar consistentemente — cor é informação, não enfeite.

## D. Anti-patterns por modelo

### handbook
- Não usar slide engine. Não ter "próximo slide". Não tipografia hero gigante.
- Sidebar é OBRIGATÓRIA. TOC sticky é OBRIGATÓRIA se houver 3+ h2.

### hub
- Cards não devem ser "slides em grid". Cada card é informativo (ícone pequeno, título, descrição, CTA).
- Filtros precisam funcionar — não decorativos.

### scrollytelling
- Não ter botões de "próximo". O scroll é o controle único.
- Progress bar no topo é parte do contrato.

### site
- Hash routing é obrigatório. Não usar `<a href="outra.html">`.
- Sem reload — `hashchange` event troca a view.

### deck
- TODO O DOCUMENTO acima inverte aqui. Tipografia gigante OK, padding gigante OK, hero pitch OK.
- O que NÃO muda: dark mode, prefers-reduced-motion, keyboard nav, foco visível.
- Não usar transition que demore > 800ms (cansa apresentador).

### report
- Editorial denso para impressão/PDF: tipografia editorial (h1 ~2.5rem), NUNCA gigante.
- **Perfil de motion estático por padrão** (registro `institucional-impresso`/`relatorio-de-bancada`): zero `@keyframes` de entrada; profundidade por fio, não por sombra difusa. Materialidade: grain estático no máximo, nunca aurora/glass/WebGL. `ambicao: A3` é proibido (falha P10).
- `@media print` rigoroso: oculta chrome interativo, força tema light, quebra de página correta, charts re-renderizam em light antes de imprimir.
- Tabelas broadsheet (sem card), `tabular-nums`, fio duplo no total. Footnotes com link mútuo.

---

## E. Checklist mental rápido antes de entregar

1. Parece feito sob medida para ESTE conteúdo? ✓ (cobrindo o logo e o texto, é distinguível do exemplo canônico do modelo?)
2. Parece um slide do PowerPoint? ✗
3. Parece gerado por IA? ✗ (glow+kicker-dot+fade-up+hover-lift+grid de cards = a coocorrência denuncia, não o elemento isolado)
4. Funciona em dark mode sem flash? ✓
5. Tem keyboard navigation onde precisa? ✓
6. Conteúdo é do usuário (não inventado)? ✓
7. Validador determinístico passa? ✓
