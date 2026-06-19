---
description: Gera relatório editorial denso (estilo relatório anual) — sumário executivo, seções numeradas, footnotes, CSS @print rigoroso. Otimizado para leitura longa e exportação PDF.
argument-hint: <tópico do relatório>
---

Você foi invocado para gerar um documento `report` (slideless). Este é o modelo para **relatórios editoriais densos**: relatórios anuais, white papers, análises de pesquisa, documentos executivos longos que serão lidos com calma e também exportados para PDF.

## Quando usar `report` vs outros modelos

- **report** → documento editorial denso, navegação por TOC numerada, footnotes, otimizado para impressão/PDF, sumário executivo destacado. Estilo: McKinsey/Goldman/Itaú Pesquisa Macro reports.
- **handbook** → manual/runbook com sidebar de seções e tom de documentação contínua. Não tem sumário executivo formal nem footnotes.
- **scrollytelling** → narrativa visual scroll-triggered com charts sticky. Mais visual, menos denso textualmente.

Se o usuário pedir "relatório" e descrever algo curto/visual, talvez ele queira scrollytelling. Confirmar antes.

## Pré-requisitos

1. Ler [../references/modelos/report.md](../modelos/report.md) (especificação completa).
2. Confirmar com o usuário:
   - **Conteúdo real** (sem inventar dados) — pode ser PDF, markdown, ou descrição estruturada
   - **Estrutura** — sumário executivo + 3-7 seções numeradas + footnotes/referências
   - **Tema** (default `itau`)
   - **Tamanho-alvo** — relatórios costumam ter 15-50 páginas A4 quando impressos
3. Se conteúdo é muito longo/complexo, rodar `/slideless estruturar` primeiro para alinhar o mapa.

## Procedimento

0. **Parti (obrigatório)** — [../references/direcao-de-arte.md](../direcao-de-arte.md): 7 decisões + `nao-vai-ter` derivadas do assunto, capa/kit/superfície ≠ exemplo canônico, bloco no `<head>`. Defaults do registro `institucional-impresso`: kit 02, superfície flat, **motion estático** (zero keyframe de entrada — perfil estrutural), assinatura M0 compositiva. A 7ª decisão é `ambicao` ([../references/ambicao.md](../ambicao.md)) — **default A1-contido** para report (vai virar PDF assinado; **A3 é proibido** em registro sóbrio — falha P10). Um report A2 sóbrio fica materialmente mais rico (fio, grain estático, anotação viva no gráfico), nunca mais saltitante. **A1 agora pede 1–2 momentos CALMOS estático-seguros** — anotação viva no gráfico (W8), counter+barra (W2), draw-on (W22): todos têm estado-final-base, então leem como "momento" mesmo com `motion: estatico`/em PDF, sem keyframe de entrada. A2 sóbrio sobe a 3–5; A3 proibido.

   **Momentos-wow:** a fonte é [references/wow-components.md](../wow-components.md) — biblioteca W1–W31 de drop-ins copy-paste (receitas já corrigidas: `@supports` + estado-final-base + reduced-motion). Respeitar o **§STACKING**: 1 herói pinned + 2 sistemas ambientes (uma só `--spring`) + 3–4 momentos rank-4 espaçados + ~70% calmo. Densidade por ambição do parti: **A1/sóbrio = 1–2 momentos calmos** (W6/W8/W2/W22/W10 — nunca premium loud); **A2 = 3–5 momentos**; **A3 = 6–8, ≥4 famílias**. (Para report: o A1 sóbrio são **1–2 momentos calmos estático-seguros** — W8/W2/W22, nunca premium loud; um A2 sóbrio deliberado sobe a 3–5; A3 segue proibido — P10.)
1. Copiar [../assets/templates/template-report.html](../../assets/templates/template-report.html).
2. Substituir placeholders: `{{TÍTULO}}`, `{{ORG}}`, `{{DOC_NUM}}`, `{{DATA}}`. Slot `SLIDELESS:TYPE-KIT` com o `<link>` do kit + `:root` do kit antes do tema.
3. Aplicar tema substituindo `/* SLIDELESS:THEME */` pelo conteúdo de [../assets/temas/itau.css](../../assets/temas/itau.css) ou neutro (MARCA intacta; DIREÇÃO conforme o parti).
4. Construir o **sumário executivo** (`.report-executive-summary`) — 3-5 parágrafos densos no topo, antes das seções, com os 2-3 takeaways centrais e os números-âncora destacados.
5. Para cada seção: usar `<section class="report-section" id="sN">` com `<h2>` no padrão `N. Título`. A TOC é gerada automaticamente pelo JS a partir dos `id="sN"`.
6. **Footnotes**: usar `<sup><a href="#fnN">[N]</a></sup>` no texto + `<li id="fnN">` em `.report-footnotes` ao final. Link mútuo (clique no número volta).
7. **Tabelas**: `<table class="data-table">` semântico (não bullets); 4+ linhas ou 3+ colunas → sempre tabela. Tratamento broadsheet: sem card/sombra, números à direita com `tabular-nums`, linha de total com fio duplo (`border-top: 3px double`). Linhas relevantes ganham `class="is-emphasis"`.
8. **Gráficos**: bloco §5.0 de css-patterns.md ANTES do primeiro chart (Chart.defaults + formatação pt-BR); escala Y em 0 para magnitudes, unidades nos ticks, tension 0 (dado discreto), sem legenda default com ≤3 séries. **Regra de fidelidade**: dados completos da fonte, composição preservada (bar+line junto = 1 chart misto), nunca omitir pontos.
8b. **Microtipografia** (vitrine do modelo): aspas curvas pt-BR, NBSP valor↔unidade, travessão com espaços, `text-wrap: balance/pretty`.
9. **CSS @print** já está no template — não simplificar. Garante quebra de página correta, oculta navegação interativa, tipografia ajustada para A4.

## Anti-patterns críticos

- **Sumário executivo genérico** ("Este relatório aborda...") → torná-lo concreto, com os 2-3 takeaways numéricos.
- **TOC manual** → deixar o JS gerar a partir dos `id="sN"`. Manter manual sempre fica desatualizado.
- **Bullets onde cabe tabela** → 4+ linhas ou 3+ colunas SEMPRE viram `<table class="data-table">`.
- **Gráficos resumidos** → fonte mostra 10 pontos? O chart tem 10 pontos. Sem "simplificar" para 5.
- **Tipografia gigante (≥3rem)** → relatório é editorial, não deck. H1 ~2.5rem, H2 ~1.75rem, body 1rem.
- **Sem `prefers-reduced-motion`** → relatórios são lidos por audiências amplas, incluindo a11y.
- **Quebrar conteúdo em múltiplos arquivos** → single-file inviolável, mesmo para relatórios de 50 páginas.

## Antes de entregar

Seguir o passo-a-passo de [../references/workflow.md](../workflow.md).

### Gate de render antes de entregar (v7 — obrigatório)
O validador determinístico vê a ESTRUTURA; **não vê runtime nem quebra visual.** Rodar os DOIS e corrigir a CAUSA antes de entregar:
- `python scripts/validar.py <arquivo.html>` → `0 erro(s)`.
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: pega overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas recorrentes: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

Checklist adicional:

- Abre sem console errors
- Dark mode toggle funciona
- TOC sticky atualiza ao scroll (scrollspy)
- Footnotes têm link mútuo (texto ↔ rodapé)
- `Ctrl+P` mostra preview de impressão limpo (sem nav, com quebra correta)
- Conteúdo da fonte 100% presente
- Tamanho do arquivo razoável (até 2MB para report com muitos charts é OK)

Reportar em uma frase ao final com path do arquivo + nº de seções + nº de charts/tabelas.
