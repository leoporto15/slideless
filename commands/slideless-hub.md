---
description: Gera hub (portal de cards categorizáveis com painéis in-page) a partir de conteúdo do usuário
argument-hint: <tópico ou descrição dos recursos>
---

Você foi invocado para gerar um documento `hub` (slideless).

## Pré-requisitos

1. Ler [../references/anti-patterns.md](../references/anti-patterns.md) se ainda não leu nesta sessão.
2. Confirmar com o usuário:
   - **Lista de recursos/cards** com categoria de cada um.
   - **Tema** (`itau` default).
   - Se cada card tem conteúdo expandido (painel) ou apenas link para fora.

## Procedimento

0. **Parti (obrigatório)** — [../references/direcao-de-arte.md](../references/direcao-de-arte.md): 7 decisões + `nao-vai-ter` derivadas do assunto, capa/kit/superfície ≠ exemplo canônico, bloco no `<head>`. A 7ª decisão é `ambicao` ([../references/ambicao.md](../references/ambicao.md)) — **default A2-elevado** para hub; se A2/A3, o campo `momento-wow` (W1-W9; W5 morph entre painéis encaixa bem) é **obrigatório**. Escolher a anatomia: portal de cards / índice editorial denso / tabela-mestra filtrável — pelo CONTEÚDO, não por default.
1. Copiar [../assets/templates/template-hub.html](../assets/templates/template-hub.html).
2. Slot `SLIDELESS:TYPE-KIT` com o `<link>` do kit + `:root` do kit antes do tema. Substituir `/* SLIDELESS:THEME */` pelo tema (camada MARCA intacta; DIREÇÃO conforme o parti).
3. **Compor**:
   - `.filters` com 1 botão por categoria + "Todos".
   - Recursos com `data-category` e `data-target` para o painel correspondente.
   - `.panel` com mesmo `id` apontado pelo `data-target`.
4. **Anti-isomorfismo:** cards NÃO são todos iguais — peso visual deriva da importância real do recurso (os principais ganham tratamento maior; os demais podem viver numa tabela-mestra). Ícone: SVG inline pequeno ou nenhum — nunca emoji. Ver [../references/anti-patterns.md](../references/anti-patterns.md) A7.
5. Filtros têm que funcionar — não decorativos. Affordance de hover: 1 escolha por documento (contraste/border-draw; lift só se clicável + perfil cinemático).
6. Motion: bloco do perfil do parti. Rodar validador (categoria P) + checklist (bloco 🎨) + gate perceptual se disponível. Salvar em `outputs/hub-<slug>.html` e reportar o parti em 1 linha.

## Anti-patterns críticos

- Cards "estilo slide" com ícone 96px + título 2.5rem → cards são editoriais.
- Filtros desconectados do JS → sempre testar filtragem.
