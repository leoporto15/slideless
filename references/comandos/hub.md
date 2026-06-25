---
description: Gera hub (portal de cards categorizáveis com painéis in-page) a partir de conteúdo do usuário
argument-hint: <tópico ou descrição dos recursos>
---

Você foi invocado para gerar um documento `hub` (slideless).

## Pré-requisitos

1. Ler [../references/anti-patterns.md](../anti-patterns.md) se ainda não leu nesta sessão.
2. Confirmar com o usuário:
   - **Lista de recursos/cards** com categoria de cada um.
   - **Tema** (`itau` default).
   - Se cada card tem conteúdo expandido (painel) ou apenas link para fora.

## Procedimento

0. **Parti (obrigatório)** — [../references/direcao-de-arte.md](../direcao-de-arte.md): 7 decisões + `nao-vai-ter` derivadas do assunto, capa/kit/superfície ≠ exemplo canônico, bloco no `<head>`. A 7ª decisão é `ambicao` ([../references/ambicao.md](../ambicao.md)) — **default A2-elevado** para hub; se A2/A3, o campo `momento-wow` (W1-W9; W5 morph entre painéis encaixa bem) é **obrigatório**. Escolher a anatomia: portal de cards / índice editorial denso / tabela-mestra filtrável — pelo CONTEÚDO, não por default.

   **Momentos-wow:** a fonte é [references/wow-components.md](../wow-components.md) — biblioteca W1–W31 de drop-ins copy-paste (receitas já corrigidas: `@supports` + estado-final-base + reduced-motion). Respeitar o **§STACKING**: 1 herói pinned + 2 sistemas ambientes (uma só `--spring`) + 3–4 momentos rank-4 espaçados + ~70% calmo. Densidade por ambição do parti: **A1/sóbrio = 1–2 momentos calmos** (W6/W8/W2/W22/W10 — nunca premium loud); **A2 = 3–5 momentos**; **A3 = 6–8, ≥4 famílias**.
1. **Esqueleto por script (não regurgitar):** `python scripts/scaffold.py hub <tema> outputs/<nome>.html` — injeta engine + layout + tema (~80% dos bytes) em disco, FORA do LLM. Depois preencha incremental (kit no slot `SLIDELESS:TYPE-KIT`, bloco parti, conteúdo seção-a-seção) com edits PEQUENOS — nunca o doc inteiro de uma vez. Ver [workflow.md §2–§4](../workflow.md).
2. Slot `SLIDELESS:TYPE-KIT` com o `<link>` do kit + `:root` do kit antes do tema. **Tema já injetado pelo scaffold** (MARCA intacta) — só compor a camada DIREÇÃO se o parti pedir.
3. **Compor**:
   - `.filters` com 1 botão por categoria + "Todos".
   - Recursos com `data-category` e `data-target` para o painel correspondente.
   - `.panel` com mesmo `id` apontado pelo `data-target`.
4. **Anti-isomorfismo:** cards NÃO são todos iguais — peso visual deriva da importância real do recurso (os principais ganham tratamento maior; os demais podem viver numa tabela-mestra). Ícone: SVG inline pequeno ou nenhum — nunca emoji. Ver [../references/anti-patterns.md](../anti-patterns.md) A7.
5. Filtros têm que funcionar — não decorativos. Affordance de hover: 1 escolha por documento (contraste/border-draw; lift só se clicável + perfil cinemático).
6. Motion: bloco do perfil do parti. Rodar validador (categoria P) + checklist (bloco 🎨) + gate perceptual se disponível. Salvar em `outputs/hub-<slug>.html` e reportar o parti em 1 linha. Seguir o passo-a-passo de [../references/workflow.md](../workflow.md).

## Gate de render antes de entregar (v7 — obrigatório)
O validador determinístico vê a ESTRUTURA; **não vê runtime nem quebra visual.** Rodar os DOIS e corrigir a CAUSA antes de entregar:
- `python scripts/validar.py <arquivo.html>` → `0 erro(s)`.
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: pega overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas recorrentes: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Anti-patterns críticos

- Cards "estilo slide" com ícone 96px + título 2.5rem → cards são editoriais.
- Filtros desconectados do JS → sempre testar filtragem.
