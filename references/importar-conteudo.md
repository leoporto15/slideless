# Importar conteúdo

Regras de conversão de fontes externas em modelo slideless. Cobre Markdown, PPT/PPTX, Confluence e texto colado.

---

## Markdown → handbook (default) / scrollytelling

Heurística:
- 1 `#` = título do documento (vai para `<h1>` + `<lead>`).
- Cada `##` vira seção (`<section data-reveal id="…">` + `<h2>`).
- `###` viram `<h3>` dentro da seção (também navegáveis via TOC).
- Listas markdown viram `<ul>` editorial (se > 6 itens, considerar quebrar em `<h3>` + parágrafos).
- Tabelas markdown viram `<table>` com classes do design system.
- Blocos de código viram componente `.code` com botão copiar (ver [componentes.md](componentes.md)).
- Imagens viram `<figure>` com `<img>` + `<figcaption>`.
- Callouts (`> [!INFO]`, `> [!WARNING]`, etc. — sintaxe GFM) viram `.callout--info` / `.callout--warn` etc.

**Quando virar scrollytelling em vez de handbook:**
- < 8 `##` no documento
- Presença de dados que pedem chart
- Tom narrativo (1ª pessoa, fluxo temporal) e não referencial

**Quando virar report:** documento formal/executivo destinado a impressão/PDF (RI, compliance, white paper), com seções numeradas e footnotes. Sinais: numeração `1.`/`2.` nas seções, notas de rodapé, tom institucional denso. Ver [decisao-modelo.md](decisao-modelo.md).

---

## PPT/PPTX → handbook OU deck (perguntar)

PPT é ambíguo. Sempre perguntar:

> Esse PPT é para você apresentar ao vivo, ou para distribuir como leitura?
> - **Apresentar ao vivo** → converto em `deck` (mantém formato slide).
> - **Distribuir para leitura** → converto em `handbook` ou `scrollytelling` (reorganiza em documento web), ou `report` se for executivo/formal destinado a PDF.

### Se virar `deck`
- Cada slide PPT vira 1 `<section class="slide">`.
- Título do slide vira `.title-md` ou `.title-lg`.
- Bullets viram `.list` com fragments (revelam ao clicar).
- Imagens centradas viram `.two-col__visual`.
- Gráficos PPT são recriados com Chart.js (extrair dados; pedir confirmação dos números).
- Slides "agenda" / "obrigado" / "perguntas" são gerados explicitamente.

### Se virar `handbook`
- Slides com mesmo tema agrupam em uma seção (`<h2>`).
- Bullets viram parágrafos editoriais ou listas curtas — se virar `<ul>` com 8+ itens, quebrar em sub-seções.
- "Slide hero / capa" some — `<h1>` + `<lead>` substitui.
- "Slide obrigado / dúvidas" some — handbook não tem.
- Imagens viram `<figure>`; gráficos viram Chart.js.

### Se virar `scrollytelling`
- Slides viram seções verticais com `data-reveal`.
- Sequência de slides com mesmo gráfico mudando vira **sticky chart** que reage ao scroll (ver [modelos/scrollytelling.md](modelos/scrollytelling.md)).

**Anti-pattern:** converter PPT slide-por-slide em handbook resulta em handbook ruim (bullets demais, parágrafos rasos). É preciso **reescrever**, não traduzir. Avisar o usuário se o PPT vier muito raso.

---

## Confluence → handbook (default) / hub

- Página única do Confluence → `handbook` com sidebar (gerada a partir dos h1-h3 da página).
- Espaço/área Confluence (várias páginas) → `hub` (cada página vira um card) ou `site` (poucas páginas, cada uma vira `<article class="view">`).
- Macros Confluence:
  - `info`, `note`, `warning` → callouts respectivos
  - `expand` → `<details class="toggle">`
  - `code` → `.code` com botão copiar
  - `panel` colorido → callout ou seção com `--color-bg-elevated`
  - `table` → `<table>` com classes do DS
  - `children` → não traduz; pergunta ao usuário se vira card grid (hub) ou link list (sidebar handbook)

**Atenção:** se Confluence URL exige autenticação, **não tentar fetch direto** — pedir export `.html` ou `.pdf` ao usuário, ou texto colado.

---

## Texto colado / descrição livre

Quando o usuário cola um texto longo sem estrutura, pedir confirmação da estrutura antes de gerar:

> Identifiquei estas seções no que você colou:
> 1. <título inferido 1>
> 2. <título inferido 2>
> ...
> Confirma? Quer que eu agrupe diferente?

Se o texto tem cara de bullet list (frases curtas, muitos parágrafos pequenos), provavelmente é briefing — pedir conteúdo desenvolvido em vez de tentar inchar bullets.

---

## Quando NÃO importar

- Documento original tem dados sigilosos não-mascarados → pedir versão mascarada.
- Não há conteúdo, só intenção ("quero algo bonito") → aplicar [protocolo-sem-conteudo.md](protocolo-sem-conteudo.md).
- PPT muito raso (bullets sem desenvolvimento) → pedir notas do apresentador ou texto adicional.

---

## Após importar — sempre

1. Aplicar tema (`itau` default, `neutro` se neutralidade pedida).
2. Rodar `python scripts/validar.py <output.html>`.
3. Aplicar `/auditar` para revisão LLM contra [checklist-revisao.md](checklist-revisao.md) e [anti-patterns.md](anti-patterns.md).
4. Salvar em `outputs/<nome-descritivo>.html`.
