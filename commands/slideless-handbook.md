---
description: Gera handbook (manual com sidebar + scrollspy + TOC) a partir de conteúdo do usuário
argument-hint: <tópico ou caminho do MD/PPT>
---

Você foi invocado para gerar um documento `handbook` (slideless).

## Pré-requisitos

1. Ler [../references/anti-patterns.md](../references/anti-patterns.md) e [../references/design-system.md](../references/design-system.md) se ainda não leu nesta sessão.
2. Confirmar com o usuário:
   - **Conteúdo real** — sem ele, aplicar [../references/protocolo-sem-conteudo.md](../references/protocolo-sem-conteudo.md). Não inventar.
   - **Tema** (`itau` ou `neutro`; default `itau`).
   - **Escopo** — quantas seções aproximadamente.

## Procedimento

0. **Parti (obrigatório, antes de qualquer HTML)** — [../references/direcao-de-arte.md](../references/direcao-de-arte.md): rotear o assunto pela tabela de registros, ler o parti do exemplo canônico ([../assets/exemplos/exemplo-handbook.html](../assets/exemplos/exemplo-handbook.html)) e do último doc da pasta, preencher as 7 decisões + `nao-vai-ter` (capa/kit/superfície ≠ canônico) e colar o bloco no `<head>`. A 7ª decisão é `ambicao` ([../references/ambicao.md](../references/ambicao.md)) — **default A2-elevado** para handbook; se A2/A3, o campo `momento-wow` (W1-W9 ligado ao dado-tese) é **obrigatório**.
1. Copiar [../assets/templates/template-handbook.html](../assets/templates/template-handbook.html) como base.
2. Preencher o slot `SLIDELESS:TYPE-KIT` com o `<link>` do kit ([../references/type-kits.md](../references/type-kits.md)) + bloco `:root` do kit antes do tema. Substituir `/* SLIDELESS:THEME */` pelo conteúdo de [../assets/temas/itau.css](../assets/temas/itau.css) ou [../assets/temas/neutro.css](../assets/temas/neutro.css) — camada MARCA intacta, camada DIREÇÃO composta conforme o parti.
3. **Compor** conforme [../references/modelos/handbook.md](../references/modelos/handbook.md) e [../references/componentes.md](../references/componentes.md) (adaptar ao parti, não colar verbatim).
4. Sidebar: um link por `<h2>`. Agrupar por `.sidebar__heading` se fizer sentido.
5. TOC: já é gerada dinamicamente do conteúdo (não tocar no JS).
6. Motion: colar o bloco do perfil declarado no parti ([direcao-de-arte.md](../references/direcao-de-arte.md) §5). `data-reveal` SÓ em figuras/dados e em ≤40% das sections — **nunca em toda section** (texto corrido, tabelas, TOC e nav não animam).
7. **Re-ancoragem anti-drift:** a cada ~5 seções, reler o parti e conferir que as últimas seções ainda o seguem.
8. Rodar `python ../scripts/validar.py <output.html>` (inclui categoria P).
9. Aplicar [../references/checklist-revisao.md](../references/checklist-revisao.md) mentalmente (bloco 🎨 incluído). Gate perceptual se Playwright disponível (workflow.md §6.5).
10. Salvar em `outputs/handbook-<slug>.html` e reportar o parti em 1 linha leiga.

## Anti-patterns críticos

- Tipografia gigante (h1 ≥ 4rem) → handbook é editorial, h1 2.5rem.
- Hero gigante na primeira tela → `<h1>` + `<p class="lead">` e começa a entregar conteúdo na primeira rolagem.
- Bullet point overload → `<ul>` com 8+ itens, considerar quebrar em h3.

Ver [../references/anti-patterns.md](../references/anti-patterns.md) seção A.
