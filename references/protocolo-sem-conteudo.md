# Protocolo: o que fazer quando o usuário não traz conteúdo real

**Regra raiz: sem conteúdo real do usuário, a skill NÃO gera HTML preenchido com lorem-ipsum nem com dados inventados sobre o Itaú.**

Os showcases em `assets/exemplos/exemplo-*.html` são fictícios *intencionalmente* (são vitrines da skill). Documentos reais entregues ao usuário não podem ser fictícios.

---

## Triagem

Antes de gerar, classificar o pedido:

### Caso 1 — Conteúdo presente e suficiente
Usuário forneceu MD, PPT, Confluence URL/anexo, texto colado, ou estrutura clara ("seções: X, Y, Z; cada uma com…").
→ **Prosseguir.** Use [importar-conteudo.md](importar-conteudo.md) para regras de conversão.

### Caso 2 — Conteúdo parcial
Usuário descreveu objetivo ("quero um handbook sobre onboarding de pessoa dados"), mas não trouxe texto.
→ **Pedir antes de gerar.** Mensagem padrão abaixo.

### Caso 3 — Apenas pediu "demo" ou "exemplo"
→ Apontar para `assets/exemplos/exemplo-*.html`. **Não gerar conteúdo fictício novo** — o exemplo já cumpre esse papel.

### Caso 4 — Pediu "estrutura vazia para preencher depois"
→ Usar `assets/templates/template-<modelo>.html` (esqueleto sem conteúdo). Copiar e entregar. Avisar que tudo está como placeholder neutro (`<h1>Título</h1>`, `<p>Texto…</p>`).

---

## Mensagem padrão para pedir conteúdo (Caso 2)

> Para gerar um `<modelo>` que sirva no Itaú, preciso do conteúdo real. Posso receber em qualquer um destes formatos:
>
> 1. **Texto/Markdown** — cola aqui ou anexa `.md`.
> 2. **PPT/PPTX** — anexa que eu extraio.
> 3. **Página Confluence** — manda URL (precisa acesso) ou exporta como `.html`/`.pdf`.
> 4. **Estrutura + bullets** — tópicos principais + 1-2 frases por tópico, eu desenvolvo o resto consultando você.
>
> Se preferir validar a forma antes do conteúdo, eu posso gerar o template vazio (`assets/templates/template-<modelo>.html`) com placeholders neutros — só me avisa.

---

## Por que essa regra é load-bearing

1. **Dados internos do Itaú são confidenciais.** Inventar "Plataforma X processa N eventos/dia" cria risco de vazar artefato com número falso passando por verdadeiro.
2. **Histórico v1 da skill foi rejeitado por entregar PPT-fictício.** Conteúdo inventado mascara qualidade de estrutura ruim — um handbook bem-feito **sobre nada** parece um handbook bem-feito.
3. **Usuário precisa do conteúdo dele no documento, não do que o LLM achou plausível.** Gerar sem conteúdo joga trabalho de revisão pesado para ele.

---

## Exceções autorizadas

| Situação | Regra |
|---|---|
| Showcase em `assets/exemplos/` | Permite fictício, pois é vitrine declarada. Conteúdo gira em torno de "Plataforma de Dados Itaú" (fictício de uso permanente da skill). |
| Template em `assets/templates/` | Permite placeholders neutros (`<h1>Título</h1>`, `<h2>Seção 1</h2>`, `<p>Texto da seção…</p>`). Não usar dados do Itaú nem números. |
| Demo isolada em `demos/` | Permite fictício se claramente rotulado como demo. |
| `/slideless distill` sobre conteúdo real existente | Permite — está reescrevendo o que já existe, não inventando. |

---

## O que NUNCA gerar sem confirmação

- Números (% de adoção, volume processado, headcount, custo)
- Nomes de pessoas, times, gerências
- Datas específicas (roadmap, marcos passados)
- Citações ("disse o diretor X")
- Métricas de negócio (NPS, churn, MAU)
- Nomes de produtos ou plataformas internas que você não viu na conversa
- Logos ou marcas além do Itaú (`assets/logos/wordmark-black.png`)

Se algum desses for necessário e o usuário não forneceu, **pergunte ou marque como `[A CONFIRMAR]`** em destaque no HTML.
