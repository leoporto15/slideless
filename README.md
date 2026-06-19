<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logos/wordmark-white.png">
    <img src="assets/logos/wordmark-black.png" alt="slideless" width="360">
  </picture>
</p>

<p align="center">
  Skill interna do Itaú para substituir PowerPoint por <strong>documentos web interativos em HTML single-file</strong> em comunicação interna — handbooks, hubs, scrollytelling, microsites, decks modernos e relatórios editoriais densos (PDF-friendly).
</p>

---

> Este `README.md` é para humanos navegando o repositório.
> Para o agente (Claude Code / Devin), o ponto de entrada é [SKILL.md](SKILL.md).

---

## O que muda em relação a PPT

| | PowerPoint | slideless |
|---|---|---|
| Entrega | `.pptx` | UM arquivo `.html` |
| Dependência | MS Office | qualquer navegador |
| Acessibilidade | limitada | WCAG AA |
| Dark mode | manual por slide | nativo, persistente |
| Navegação | linear | navegação não-linear (handbook, hub, site) ou linear (deck, scrollytelling) |
| Interatividade | clique → próximo slide | toggles, tabs, charts, hash routing, fragments, keyboard nav |
| Hospedagem | rede interna | qualquer S3 estático ou anexo |
| Densidade de texto | bullets curtos | parágrafos editoriais |

---

## Comandos (31)

Um comando único — **`/slideless`** — e você escreve o subcomando logo depois: `/slideless deck pitch do 1T26`, `/slideless criar`, `/slideless auditar arquivo.html`. **Mesma sintaxe em Claude Code, GitHub Copilot e Devin** — não há slash-command individual por subcomando; cada um é um spec em [references/comandos/](references/comandos/) que o roteador do [SKILL.md](SKILL.md) despacha.

> ### 🧭 Não sabe por onde começar? Siga por aqui.
>
> Se você é de uma **área de negócios** e não conhece a diferença entre handbook, deck, hub etc. — **use `/slideless criar`**. É um wizard conversacional que faz 5 perguntas em português comum e escolhe o modelo certo automaticamente. Você não precisa saber nada técnico.

### 🚪 Ponto de entrada (1)

| Comando | O que faz |
|---|---|
| **`/slideless criar`** | **Wizard guiado para áreas de negócios.** Faz 5 perguntas (objetivo, público, distribuição, conteúdo, tema) e escolhe o modelo automaticamente. Coleta o conteúdo do jeito que você tiver (PDF, bullets, ideias na cabeça ou nada ainda) e gera o HTML pronto. |

### Pré-geração (1)

| Comando | O que faz |
|---|---|
| `/slideless estruturar` | Analisa conteúdo bruto (bullets, PDF colado, descrição) e propõe um mapa estruturado em tabela para você aprovar antes de gerar HTML. Evita retrabalho em conteúdo denso. |

### Criação direta (6)
*Use quando você já sabe qual modelo quer.*

| Comando | O que faz |
|---|---|
| `/slideless deck` | **Apresentação com slides** que avançam (setas/teclado). Para pitch ao vivo, all-hands, demo guiada. Único modelo com tipografia gigante permitida. |
| `/slideless handbook` | **Manual web com menu lateral** + scrollspy + TOC sticky. Para documentação longa, onboarding, política interna, runbook. |
| `/slideless hub` | **Portal de cards categorizados.** Cards filtram por categoria; clicar abre painel in-page com gráficos e tabelas. Para centrais de recursos. |
| `/slideless scrollytelling` | **Narrativa única** que revela conteúdo ao rolar a página. Gráficos sticky que mudam conforme avança. Para relatórios anuais, casos de estudo. |
| `/slideless site` | **Mini-site SPA** com 2-5 abas (home, sobre, contato) e hash routing. Para microsites internos, lançamentos. |
| `/slideless report` | **Relatório editorial denso** otimizado para impressão e PDF — sumário executivo, seções numeradas, footnotes, CSS @print rigoroso. Para diretoria, RI, compliance. |

### Importação (3)
*Converte conteúdo existente em formato slideless.*

| Comando | O que faz |
|---|---|
| `/slideless importar-confluence` | Converte página ou espaço Confluence inteiro no modelo mais adequado. |
| `/slideless importar-ppt` | Converte PPT/PPTX em handbook (para leitura) ou deck (para apresentar). Sempre pergunta qual. |
| `/slideless importar-md` | Converte Markdown estruturado em handbook (default) ou scrollytelling. |

### Edição cirúrgica (6)
*Adiciona elementos a um documento existente sem regenerar.*

| Comando | O que faz |
|---|---|
| `/slideless adicionar-secao` | Adiciona uma seção a handbook, scrollytelling ou site existente. |
| `/slideless adicionar-slide` | Adiciona slide ao deck (hero, big-num, metrics, list, quote, two-col, divider, timeline). |
| `/slideless adicionar-callout` | Insere callout colorido (info, tip, warn, danger). |
| `/slideless adicionar-grafico` | Insere gráfico Chart.js (line, bar, donut, gauge, radar, bubble, waterfall, mixed). |
| `/slideless adicionar-fragment` | No deck: marca elementos para revelar progressivamente por click. |
| `/slideless adicionar-toc` | No handbook: regenera o TOC sticky a partir dos h2/h3 atuais. |

### Transformação (3)
*Modifica um documento existente.*

| Comando | O que faz |
|---|---|
| `/slideless aplicar-tema` | Troca tema (neutro ↔ itau) em documento existente. |
| `/slideless converter-modelo` | Converte entre modelos compatíveis (handbook ↔ scrollytelling, hub ↔ site). |
| `/slideless distill` | Reduz handbook longo a sumário enxuto preservando hierarquia. |

### 🎨 Refinamento de design (5 comandos independentes)
*Aplica transformações de design sênior a documentos existentes. Comandos compõem em sequência aplicando um após o outro.*

| Comando | O que faz |
|---|---|
| `/slideless bolder` | **Amplifica designs tímidos** — tipografia +30%, contraste de peso ampliado, whitespace generoso. Lê o `parti` do documento e reforça as decisões dele (não instala um kit fixo). |
| `/slideless quieter` | **Reduz designs ruidosos** — tipografia -15%, extremos de peso suavizados, motion calma. Opera dentro do kit e do nível de ambição declarados. |
| `/slideless animate` | **Movimento intencional** — coreografa apenas o momento-wow declarado e a gramática por papel, no perfil de motion do documento. Em registro estático, avisa e para. Respeita `prefers-reduced-motion`. |
| `/slideless delight` | **Micro-interações por papel** — hover por affordance, feedback no local do gatilho, micro-interações de leitura. Sem confetti, sem hover-lift universal; coerente com o nível de ambição. |
| `/slideless overdrive` | **Nível A3-extraordinário** — pode compor **qualquer momento-wow do palette W1-W31** (WebGL no hero, View Transitions, variable font animada, 3D-tilt, masked-type, sticky-stack…); as opções A-H são os _heavies_ A3-exclusivos que ele desbloqueia, não a lista única. Interativo (multi-seleção), fallback gracioso. Showpiece técnico (até 5 MB). |

**Composição típica:**
- `/slideless bolder` + `/slideless animate` → executivo com peso e movimento
- `/slideless quieter` + `/slideless delight` → editorial refinado
- `/slideless bolder` + `/slideless overdrive` → showpiece de alto perfil

### Qualidade (4)
*Audita e melhora documentos existentes.*

| Comando | O que faz |
|---|---|
| `/slideless auditar` | Roda validador determinístico + checklist + anti-patterns. Devolve lista de violações com severidade. |
| `/slideless polir` | Refina tipografia, espaçamento e hierarquia visual. |
| `/slideless harden` | Endurece a11y (WCAG AA), keyboard nav, `prefers-reduced-motion`. |
| `/slideless acessibilidade` | Foco isolado em acessibilidade — varredura completa + correções. |

### Export (2)

| Comando | O que faz |
|---|---|
| `/slideless exportar-pdf` | Renderiza para PDF via Playwright (deck → landscape; demais → retrato). |
| `/slideless exportar-screenshots` | 1 PNG por slide (deck) ou por seção (demais) para preview rápido. |

Documentação técnica completa de cada subcomando em [references/comandos/](references/comandos/).

---

## Modelos

| Modelo | Quando usar | Referência |
|---|---|---|
| [`handbook`](references/modelos/handbook.md) | manual longo, onboarding, política, runbook | GitLab Handbook |
| [`hub`](references/modelos/hub.md) | portal de recursos com cards categorizáveis | Apple Developer hub, Vercel guides index |
| [`scrollytelling`](references/modelos/scrollytelling.md) | narrativa única com reveal + sticky chart | NYT Upshot |
| [`site`](references/modelos/site.md) | microsite SPA com 2-5 views | Linear, Vercel guides |
| [`deck`](references/modelos/deck.md) | pitch ao vivo, all-hands (único onde tipografia gigante é OK) | Apple keynote |
| [`report`](references/modelos/report.md) | relatório editorial denso para diretoria/RI/compliance, otimizado para PDF — sumário executivo, TOC numerada, footnotes, CSS @print rigoroso | Itaú Pesquisa Macro, McKinsey Global Institute, Goldman Sachs research |

Decisão entre modelos: [references/decisao-modelo.md](references/decisao-modelo.md). **Ou simplesmente use `/slideless criar` — o wizard decide por você.**

---

## Estrutura

```
slideless/
├── SKILL.md                       ← entry point para o agente
├── README.md                      ← este arquivo
├── CLAUDE.md                      ← instruções para Claude Code
├── .claude-plugin/plugin.json     ← manifest do plugin
├── .github/copilot-instructions.md ← instruções para GitHub Copilot Chat
├── commands/                      ← só slideless.md (roteador fino do Claude Code → references/comandos/)
├── .github/prompts/               ← só slideless.prompt.md (roteador fino do Copilot)
├── references/
│   ├── comandos/                  ← specs dos 31 subcomandos (FONTE ÚNICA)
│   ├── direcao-de-arte.md         ← o Parti: 7 decisões por documento (LER ANTES DE GERAR)
│   ├── ambicao.md                 ← teto cutting-edge: eixo A1/A2/A3 + densidade de momentos-wow
│   ├── wow-components.md           ← biblioteca W1-W31 de drop-ins copy-paste + §STACKING + armadilhas de render
│   ├── type-kits.md               ← pool de kits tipográficos + fontes banidas
│   ├── anti-patterns.md           ← PPT-isms e AI-tells proibidos
│   ├── design-system.md           ← tokens, dark mode, boot script
│   ├── componentes.md             ← biblioteca de componentes
│   ├── css-patterns.md            ← gráficos, tabelas, materialidade, scroll-driven
│   ├── slide-patterns.md          ← layouts, engine v3, fragmentos
│   ├── decisao-modelo.md          ← decision tree dos 6 modelos
│   ├── protocolo-sem-conteudo.md  ← o que fazer sem conteúdo real
│   ├── importar-conteudo.md       ← MD/PPT/Confluence → slideless
│   ├── workflow.md                ← passo-a-passo
│   ├── checklist-revisao.md       ← validação LLM
│   ├── modelos/{handbook,hub,scrollytelling,site,deck,report}.md
│   └── temas/{neutro,itau}.md
├── assets/
│   ├── temas/{itau,neutro}.css    ← tokens light+dark, duas camadas (marca/direção)
│   ├── logos/{wordmark-black,wordmark-white}.png
│   ├── exemplos/                  ← showcases canônicos (1 por modelo)
│   └── templates/                 ← esqueletos vazios para popular
├── scripts/
│   ├── validar.py                 ← validador determinístico de ESTRUTURA (stdlib)
│   ├── smoke.py                   ← gate de RENDER headless (Playwright): overflow, texto-por-caractere, número duplicado, slide curto, etc.
│   └── exportar_pdf.py            ← PDF/PNG via Playwright
└── demos/                         ← 4 famílias: 3 temáticas (itau-1T26 · asset · trump — 7 docs cada: 6 modelos + deck-overdrive) + slideless-skill (a própria skill se demonstrando nos 6 formatos)
```

---

## Instalação

### Claude Code — via marketplace interno

O plugin é distribuído pelo marketplace interno do time/banco. Com esse catálogo já registrado no seu Claude Code:

```
/plugin install slideless@<marketplace-interno>
```

O nome do `<marketplace-interno>` é fornecido por quem administra o catálogo. Se ainda não estiver registrado, adicione-o primeiro com `/plugin marketplace add <repo-ou-url-do-catálogo>` (esse repo do catálogo lista o `slideless` via `source` apontando para este repositório). A instalação traz a skill `slideless` (auto-invocável quando você pede um manual, deck, relatório etc.) e o **comando único `/slideless`** (namespaced `/slideless:slideless` no plugin) — em vez de 31 comandos, você escreve o subcomando logo depois: `/slideless deck`, `/slideless criar`, `/slideless auditar`. Para atualizar depois: `/plugin marketplace update <marketplace-interno>`.

### Claude Code — manual (desenvolvimento / teste)

Carregar o checkout local sem instalar, com `--plugin-dir`:

```bash
git clone https://github.com/leoporto15/slideless.git
claude --plugin-dir ./slideless
```

Use `/reload-plugins` para recarregar após editar. Alternativamente, clonar dentro de `~/.claude/skills/slideless/` faz o Claude Code carregar como plugin de skills-dir automaticamente (mesma namespace `/slideless:…`).

### GitHub Copilot Chat (VS Code)

O Copilot **não** lê `commands/*.md` nem os specs em `references/comandos/` como slash-commands — seu mecanismo são **prompt files**. O repo traz **um só**: [`.github/prompts/slideless.prompt.md`](.github/prompts/slideless.prompt.md) → o comando `/slideless`. Você invoca `/slideless`, escreve o subcomando, e o prompt roteia para `references/comandos/<nome>.md` conforme o [SKILL.md](SKILL.md). O sempre-ativo `.github/copilot-instructions.md` carrega a doutrina.

1. **Abrir a pasta do repositório no VS Code** (com a extensão GitHub Copilot Chat). O `.github/prompts/` é detectado no workspace.
2. O setting `chat.promptFiles` já vem ligado via [`.vscode/settings.json`](.vscode/settings.json) versionado. Se `/slideless` não aparecer, confirme em Settings → busque **"prompt files"** → marque.
3. No painel de Chat, **modo Agent**, digite `/slideless deck pitch do 1T26` (ou só `/slideless` → ele lista/pergunta). Um comando só — igual ao Claude Code e ao Devin.

> Single-source: a lógica de cada subcomando vive só em `references/comandos/`. As entradas por harness (`commands/slideless.md`, `.github/prompts/slideless.prompt.md`) são roteadores finos que apontam pra lá — sem payload duplicado.

### Devin

Configurar a skill como ferramenta interna no espaço do time, apontando para este repositório. Devin lê `SKILL.md` como roteador comportamental.

### Cursor / OpenCode / outros

O formato `SKILL.md` (roteador) + `references/comandos/*.md` (subcomandos) + `references/*.md` (doutrina) é portátil: cada harness só precisa registrar **um** comando, `/slideless`, apontando para o `SKILL.md`. Adapte conforme o harness.

---

## Como rodar o validador

```bash
python scripts/validar.py caminho/do/arquivo.html
```

Saídas:
- `OK` → tudo passou
- Lista numerada → violações com severidade (`ERROR`/`WARN`/`INFO`) e linha aproximada

Flags:
- `--quick` — apenas identifica modelo/tema
- `--strict` — warnings viram erros
- `--json` — saída JSON para integração
- `--stats <pasta>` — telemetria do pool: varre os `.html` da pasta e tabula a distribuição das decisões do parti (registro, kit, capa, superfície, motion, ambição). Útil para detectar pasteurização (um eixo dominando >40% dos documentos).

Exit code: `0` se sem erros, `1` se houver pelo menos um.

---

## Como rodar o smoke (gate de render)

O `validar.py` checa a **estrutura**; ele não vê runtime nem quebra visual. O `smoke.py` carrega o HTML num Chromium headless e pega o que a estrutura não vê: erro de JS, overflow/sangramento, texto quebrando por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral.

```bash
pip install playwright && playwright install chromium
python scripts/smoke.py caminho/do/arquivo.html
```

Saídas: `SMOKE PASS` (ok) · `SMOKE FAIL: <causa>` (corrigir antes de entregar) · `SKIP` (Playwright ausente). **Todo comando que gera ou modifica um documento roda validar.py + smoke.py antes de entregar.**

---

## Como exportar PDF

```bash
pip install playwright
playwright install chromium

python scripts/exportar_pdf.py caminho/do/arquivo.html
# → gera <arquivo>.pdf no mesmo diretório
# deck vira landscape, demais retrato

# screenshots (1 PNG por slide ou por h2)
python scripts/exportar_pdf.py caminho/do/arquivo.html --mode screenshots

# forçar tema antes de renderizar
python scripts/exportar_pdf.py caminho/do/arquivo.html --theme dark
```

---

## Princípios inegociáveis

1. **Single-file.** Um `.html` sempre. CSS e JS inline. Fontes e charts via CDN.
2. **Dark mode nativo.** Boot script no `<head>` antes do CSS (sem flash). Toggle no header. Persistente via `localStorage`.
3. **Documento web, não slide.** Tipografia gigante apenas no modelo `deck`. Em handbook/hub/scrollytelling/site, h1 ~2.5rem. Ver [anti-patterns.md](references/anti-patterns.md).
4. **Conteúdo real obrigatório.** Sem conteúdo do usuário, nunca gerar lorem ipsum nem inventar dados internos do Itaú. Ver [protocolo-sem-conteudo.md](references/protocolo-sem-conteudo.md).
5. **WCAG AA.** Foco visível, ARIA correto, keyboard nav, `prefers-reduced-motion` respeitado.

---

## Por que existe

A v1 desta skill foi rejeitada por sair "PPT estilizado em HTML". A v2 mudou de paradigma: vibe Notion / GitLab handbook, não pitch deck. O modelo `deck` é a única exceção e existe explicitamente para casos onde uma apresentação ao vivo é necessária.

Manter a distinção `handbook` × `deck` é load-bearing — perdê-la é repetir o erro que motivou a reescrita.

---

## Contribuir

- Antes de adicionar componente novo: ver se cabe em [componentes.md](references/componentes.md) — duplicidade fragmenta o sistema.
- Antes de adicionar modelo novo: justificar que os 6 existentes (handbook, hub, scrollytelling, site, deck, report) não cobrem o caso. O sistema é deliberadamente fechado.
- Cada PR deve passar o validador (`python scripts/validar.py`) **e** o gate de render (`python scripts/smoke.py`) nos exemplos afetados.
