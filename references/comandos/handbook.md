---
description: Gera handbook (manual com sidebar + scrollspy + TOC) a partir de conteúdo do usuário
argument-hint: <tópico ou caminho do MD/PPT>
---

Você foi invocado para gerar um documento `handbook` (slideless).

## Pré-requisitos

1. Ler [../references/anti-patterns.md](../anti-patterns.md) e [../references/design-system.md](../design-system.md) se ainda não leu nesta sessão.
2. Confirmar com o usuário:
   - **Conteúdo real** — sem ele, aplicar [../references/protocolo-sem-conteudo.md](../protocolo-sem-conteudo.md). Não inventar.
   - **Tema** (`itau` ou `neutro`; default `itau`).
   - **Escopo** — quantas seções aproximadamente.

## Procedimento

0. **Parti (obrigatório, antes de qualquer HTML)** — [../references/direcao-de-arte.md](../direcao-de-arte.md): rotear o assunto pela tabela de registros, ler o parti do exemplo canônico ([../assets/exemplos/exemplo-handbook.html](../../assets/exemplos/exemplo-handbook.html)) e do último doc da pasta, preencher as 7 decisões + `nao-vai-ter` (capa/kit/superfície ≠ canônico) e colar o bloco no `<head>`. A 7ª decisão é `ambicao` ([../references/ambicao.md](../ambicao.md)) — **default A2-elevado** para handbook; se A2/A3, o campo `momento-wow` (W1-W9 ligado ao dado-tese) é **obrigatório**.

   **Momentos-wow:** a fonte é [references/wow-components.md](../wow-components.md) — biblioteca W1–W31 de drop-ins copy-paste (receitas já corrigidas: `@supports` + estado-final-base + reduced-motion). Respeitar o **§STACKING**: 1 herói pinned + 2 sistemas ambientes (uma só `--spring`) + 3–4 momentos rank-4 espaçados + ~70% calmo. Densidade por ambição do parti: **A1/sóbrio = 1–2 momentos calmos** (W6/W8/W2/W22/W10 — nunca premium loud); **A2 = 3–5 momentos**; **A3 = 6–8, ≥4 famílias**.
1. Copiar [../assets/templates/template-handbook.html](../../assets/templates/template-handbook.html) como base.
2. Preencher o slot `SLIDELESS:TYPE-KIT` com o `<link>` do kit ([../references/type-kits.md](../type-kits.md)) + bloco `:root` do kit antes do tema. Substituir `/* SLIDELESS:THEME */` pelo conteúdo de [../assets/temas/itau.css](../../assets/temas/itau.css) ou [../assets/temas/neutro.css](../../assets/temas/neutro.css) — camada MARCA intacta, camada DIREÇÃO composta conforme o parti.
3. **Compor** conforme [../references/modelos/handbook.md](../modelos/handbook.md) e [../references/componentes.md](../componentes.md) (adaptar ao parti, não colar verbatim).
4. Sidebar: um link por `<h2>`. Agrupar por `.sidebar__heading` se fizer sentido.
5. TOC: já é gerada dinamicamente do conteúdo (não tocar no JS).
6. Motion: colar o bloco do perfil declarado no parti ([direcao-de-arte.md](../direcao-de-arte.md) §5). `data-reveal` SÓ em figuras/dados e em ≤40% das sections — **nunca em toda section** (texto corrido, tabelas, TOC e nav não animam).
7. **Re-ancoragem anti-drift:** a cada ~5 seções, reler o parti e conferir que as últimas seções ainda o seguem.
8. Rodar `python ../scripts/validar.py <output.html>` (inclui categoria P).
9. Aplicar [../references/checklist-revisao.md](../checklist-revisao.md) mentalmente (bloco 🎨 incluído). Gate perceptual se Playwright disponível (workflow.md §6.5).
10. Salvar em `outputs/handbook-<slug>.html` e reportar o parti em 1 linha leiga.

## Gate de render antes de entregar (v7 — obrigatório)
O validador determinístico vê a ESTRUTURA; **não vê runtime nem quebra visual.** Rodar os DOIS e corrigir a CAUSA antes de entregar:
- `python scripts/validar.py <arquivo.html>` → `0 erro(s)`.
- `python scripts/smoke.py <arquivo.html>` → `SMOKE PASS` (Chromium headless: pega overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide que não preenche a viewport, invasão de coluna lateral, scroll horizontal). `SKIP` se Playwright ausente.
Nunca entregar com `SMOKE FAIL`. Armadilhas recorrentes: [references/wow-components.md](../wow-components.md) §"Armadilhas visuais que o smoke.py reprova".

## Anti-patterns críticos

- Tipografia gigante (h1 ≥ 4rem) → handbook é editorial, h1 2.5rem.
- Hero gigante na primeira tela → `<h1>` + `<p class="lead">` e começa a entregar conteúdo na primeira rolagem.
- Bullet point overload → `<ul>` com 8+ itens, considerar quebrar em h3.

Ver [../references/anti-patterns.md](../anti-patterns.md) seção A.
