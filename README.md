<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logos/wordmark-white.png">
    <img src="assets/logos/wordmark-black.png" alt="slideless" width="360">
  </picture>
</p>

<p align="center">
  Skill interna do Itaú para substituir PowerPoint por <strong>documentos web interativos em HTML single-file</strong> em comunicação interna — handbooks, hubs, scrollytelling, microsites e decks modernos.
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

## Modelos

| Modelo | Quando usar | Referência |
|---|---|---|
| [`handbook`](references/modelos/handbook.md) | manual longo, onboarding, política, runbook | GitLab Handbook |
| [`hub`](references/modelos/hub.md) | portal de recursos com cards categorizáveis | Notion Workspace |
| [`scrollytelling`](references/modelos/scrollytelling.md) | narrativa única com reveal + sticky chart | NYT Upshot |
| [`site`](references/modelos/site.md) | microsite SPA com 2-5 views | Linear, Vercel guides |
| [`deck`](references/modelos/deck.md) | pitch ao vivo, all-hands (único onde tipografia gigante é OK) | Apple keynote |

Decisão entre modelos: [references/decisao-modelo.md](references/decisao-modelo.md).

---

## Estrutura

```
slideless/
├── SKILL.md                       ← entry point para o agente
├── README.md                      ← este arquivo
├── .claude-plugin/plugin.json     ← manifest da skill
├── commands/                      ← 23 slash commands (1 arquivo cada)
├── references/
│   ├── anti-patterns.md           ← PPT-isms proibidos
│   ├── design-system.md           ← tokens, dark mode, boot script
│   ├── componentes.md             ← biblioteca de componentes
│   ├── decisao-modelo.md          ← decision tree dos 5 modelos
│   ├── protocolo-sem-conteudo.md  ← o que fazer sem conteúdo real
│   ├── importar-conteudo.md       ← MD/PPT/Confluence → slideless
│   ├── workflow.md                ← passo-a-passo
│   ├── checklist-revisao.md       ← validação LLM
│   ├── modelos/{handbook,hub,scrollytelling,site,deck}.md
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

## Comandos (23)

### Criação
`/slideless-handbook` · `/slideless-hub` · `/slideless-scrollytelling` · `/slideless-site` · `/slideless-deck`

### Importação
`/importar-confluence` · `/importar-ppt` · `/importar-md`

### Edição cirúrgica
`/adicionar-secao` · `/adicionar-slide` · `/adicionar-callout` · `/adicionar-grafico` · `/adicionar-fragment` · `/adicionar-toc`

### Transformação
`/aplicar-tema` · `/converter-modelo` · `/distill`

### Qualidade
`/auditar` · `/polir` · `/harden` · `/acessibilidade`

### Export
`/exportar-pdf` · `/exportar-screenshots`

Documentação completa de cada comando em [commands/](commands/).

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
- Antes de adicionar modelo novo: justificar que os 5 existentes não cobrem o caso. O sistema é deliberadamente fechado.
- Cada PR deve passar o validador (`python scripts/validar.py`) nos exemplos afetados.
