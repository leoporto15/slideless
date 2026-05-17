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

## Comandos (30)

> ### 🧭 Não sabe por onde começar? Siga por aqui.
>
> Se você é de uma **área de negócios** e não conhece a diferença entre handbook, deck, hub etc. — **use `/criar`**. É um wizard conversacional que faz 5 perguntas em português comum e escolhe o modelo certo automaticamente. Você não precisa saber nada técnico.

### 🚪 Ponto de entrada (1)

| Comando | O que faz |
|---|---|
| **`/criar`** | **Wizard guiado para áreas de negócios.** Faz 5 perguntas (objetivo, público, distribuição, conteúdo, tema) e escolhe o modelo automaticamente. Coleta o conteúdo do jeito que você tiver (PDF, bullets, ideias na cabeça ou nada ainda) e gera o HTML pronto. |

### Pré-geração (1)

| Comando | O que faz |
|---|---|
| `/estruturar` | Analisa conteúdo bruto (bullets, PDF colado, descrição) e propõe um mapa estruturado em tabela para você aprovar antes de gerar HTML. Evita retrabalho em conteúdo denso. |

### Criação direta (6)
*Use quando você já sabe qual modelo quer.*

| Comando | O que faz |
|---|---|
| `/slideless-deck` | **Apresentação com slides** que avançam (setas/teclado). Para pitch ao vivo, all-hands, demo guiada. Único modelo com tipografia gigante permitida. |
| `/slideless-handbook` | **Manual web com menu lateral** + scrollspy + TOC sticky. Para documentação longa, onboarding, política interna, runbook. |
| `/slideless-hub` | **Portal de cards categorizados.** Cards filtram por categoria; clicar abre painel in-page com gráficos e tabelas. Para centrais de recursos. |
| `/slideless-scrollytelling` | **Narrativa única** que revela conteúdo ao rolar a página. Gráficos sticky que mudam conforme avança. Para relatórios anuais, casos de estudo. |
| `/slideless-site` | **Mini-site SPA** com 2-5 abas (home, sobre, contato) e hash routing. Para microsites internos, lançamentos. |
| `/slideless-report` | **Relatório editorial denso** otimizado para impressão e PDF — sumário executivo, seções numeradas, footnotes, CSS @print rigoroso. Para diretoria, RI, compliance. |

### Importação (3)
*Converte conteúdo existente em formato slideless.*

| Comando | O que faz |
|---|---|
| `/importar-confluence` | Converte página ou espaço Confluence inteiro no modelo mais adequado. |
| `/importar-ppt` | Converte PPT/PPTX em handbook (para leitura) ou deck (para apresentar). Sempre pergunta qual. |
| `/importar-md` | Converte Markdown estruturado em handbook (default) ou scrollytelling. |

### Edição cirúrgica (6)
*Adiciona elementos a um documento existente sem regenerar.*

| Comando | O que faz |
|---|---|
| `/adicionar-secao` | Adiciona uma seção a handbook, scrollytelling ou site existente. |
| `/adicionar-slide` | Adiciona slide ao deck (hero, big-num, metrics, list, quote, two-col, divider, timeline). |
| `/adicionar-callout` | Insere callout colorido (info, tip, warn, danger). |
| `/adicionar-grafico` | Insere gráfico Chart.js (line, bar, donut, gauge, radar, bubble, waterfall, mixed). |
| `/adicionar-fragment` | No deck: marca elementos para revelar progressivamente por click. |
| `/adicionar-toc` | No handbook: regenera o TOC sticky a partir dos h2/h3 atuais. |

### Transformação (3)
*Modifica um documento existente.*

| Comando | O que faz |
|---|---|
| `/aplicar-tema` | Troca tema (neutro ↔ itau) em documento existente. |
| `/converter-modelo` | Converte entre modelos compatíveis (handbook ↔ scrollytelling, hub ↔ site). |
| `/distill` | Reduz handbook longo a sumário enxuto preservando hierarquia. |

### 🎨 Refinamento de design (5 comandos independentes)
*Aplica transformações de design sênior a documentos existentes. Comandos compõem em sequência aplicando um após o outro.*

| Comando | O que faz |
|---|---|
| `/slideless-bolder` | **Amplifica designs tímidos** — tipografia hero +30%, glow atmosférico reforçado, números-âncora circulados, whitespace generoso. Para quando o doc gerado ficou medíocre. |
| `/slideless-quieter` | **Reduz designs ruidosos** — tipografia -15%, cores muted, transições mais lentas, fallback serif editorial. Para quando o doc tá gritando demais. |
| `/slideless-animate` | **Movimento intencional** — heroIn, Auto-Animate FLIP entre slides, counters animados, stagger reveals. Sempre respeita `prefers-reduced-motion`. |
| `/slideless-delight` | **Micro-interações sem cafonice** — hover lifts em cards, cursor-aware spotlight no hero, shimmer na progress bar, parallax sutil. Sem confetti, sem easter eggs. |
| `/slideless-overdrive` | **Tecnicamente extraordinário** — WebGL/Canvas generative no hero, custom Chart.js plugins, variable font animation, cinematic transitions. Comando interativo: pergunta quais efeitos aplicar (A-F, multi-seleção). Showpiece técnico (até 5 MB). |

**Composição típica:**
- `/slideless-bolder` + `/slideless-animate` → executivo com peso e movimento
- `/slideless-quieter` + `/slideless-delight` → editorial refinado
- `/slideless-bolder` + `/slideless-overdrive` → showpiece de alto perfil

### Qualidade (4)
*Audita e melhora documentos existentes.*

| Comando | O que faz |
|---|---|
| `/auditar` | Roda validador determinístico + checklist + anti-patterns. Devolve lista de violações com severidade. |
| `/polir` | Refina tipografia, espaçamento e hierarquia visual. |
| `/harden` | Endurece a11y (WCAG AA), keyboard nav, `prefers-reduced-motion`. |
| `/acessibilidade` | Foco isolado em acessibilidade — varredura completa + correções. |

### Export (2)

| Comando | O que faz |
|---|---|
| `/exportar-pdf` | Renderiza para PDF via Playwright (deck → landscape; demais → retrato). |
| `/exportar-screenshots` | 1 PNG por slide (deck) ou por seção (demais) para preview rápido. |

Documentação técnica completa de cada comando em [commands/](commands/).

---

## Modelos

| Modelo | Quando usar | Referência |
|---|---|---|
| [`handbook`](references/modelos/handbook.md) | manual longo, onboarding, política, runbook | GitLab Handbook |
| [`hub`](references/modelos/hub.md) | portal de recursos com cards categorizáveis | Notion Workspace |
| [`scrollytelling`](references/modelos/scrollytelling.md) | narrativa única com reveal + sticky chart | NYT Upshot |
| [`site`](references/modelos/site.md) | microsite SPA com 2-5 views | Linear, Vercel guides |
| [`deck`](references/modelos/deck.md) | pitch ao vivo, all-hands (único onde tipografia gigante é OK) | Apple keynote |
| [`report`](references/modelos/report.md) | relatório editorial denso para diretoria/RI/compliance, otimizado para PDF — sumário executivo, TOC numerada, footnotes, CSS @print rigoroso | Itaú Pesquisa Macro, McKinsey Global Institute, Goldman Sachs research |

Decisão entre modelos: [references/decisao-modelo.md](references/decisao-modelo.md). **Ou simplesmente use `/criar` — o wizard decide por você.**

---

## Estrutura

```
slideless/
├── SKILL.md                       ← entry point para o agente
├── README.md                      ← este arquivo
├── .claude-plugin/plugin.json     ← manifest da skill
├── commands/                      ← 30 slash commands (1 arquivo cada)
├── references/
│   ├── anti-patterns.md           ← PPT-isms proibidos
│   ├── design-system.md           ← tokens, dark mode, boot script
│   ├── componentes.md             ← biblioteca de componentes
│   ├── css-patterns.md            ← gráficos, tabelas, depth tiers
│   ├── slide-patterns.md          ← layouts, engine v3, fragmentos
│   ├── decisao-modelo.md          ← decision tree dos 6 modelos
│   ├── protocolo-sem-conteudo.md  ← o que fazer sem conteúdo real
│   ├── importar-conteudo.md       ← MD/PPT/Confluence → slideless
│   ├── workflow.md                ← passo-a-passo
│   ├── checklist-revisao.md       ← validação LLM
│   ├── modelos/{handbook,hub,scrollytelling,site,deck,report}.md
│   └── temas/{neutro,itau}.md
├── assets/
│   ├── temas/{itau,neutro}.css    ← tokens light+dark
│   ├── logos/itau.png
│   ├── exemplos/                  ← showcases preenchidos (fictícios)
│   └── templates/                 ← esqueletos vazios para popular
├── scripts/
│   ├── validar.py                 ← validador determinístico (stdlib)
│   └── exportar_pdf.py            ← PDF/PNG via Playwright
└── demos/                         ← input → output reais pareados
```

---

## Instalação

### Claude Code

Clone este repositório dentro da pasta de skills do seu Claude Code, ou use o plugin via marketplace (se publicado):

```bash
cd ~/.claude/skills/
git clone <url-repo>/slideless.git
```

Recarregue o Claude Code. A skill aparece automaticamente; os comandos viram `/slideless-handbook`, `/auditar` etc.

### Devin

Configurar a skill como ferramenta interna no espaço do time, apontando para este repositório. Devin lê `SKILL.md` como roteador comportamental.

### Cursor / OpenCode / outros

O formato `commands/*.md` + `references/*.md` + `SKILL.md` é portátil. Adapte conforme o harness.

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

Exit code: `0` se sem erros, `1` se houver pelo menos um.

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
- Cada PR deve passar o validador (`python scripts/validar.py`) nos exemplos afetados.
