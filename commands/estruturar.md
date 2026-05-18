---
description: Pré-geração — analisa conteúdo bruto (bullets, PDF colado, descrição livre) e devolve um mapa estruturado para aprovação antes de gerar HTML. Evita retrabalho quando o conteúdo é denso ou a escolha de modelo é não-óbvia.
argument-hint: <conteúdo bruto ou caminho de arquivo>
---

Recebe conteúdo bruto e devolve um **mapa estruturado** para o usuário aprovar antes de gerar qualquer HTML.

## Input aceito

- Bullets colados diretamente no chat
- Transcrição de PDF (texto bruto com quebras de página)
- Descrição livre: "quero apresentar os resultados do Q1 para a diretoria"
- Arquivo `.md` ou `.txt` anexado

## Quando NUNCA pular

Sempre rodar `/estruturar` antes de gerar quando:
- conteúdo tem **mais de 30 elementos discretos**
- origem é **PDF/PPT colado**
- usuário **não especificou modelo**

## Output (proposta para aprovação)

Devolver no formato:

```
## Proposta de estrutura — slideless

**Modelo recomendado:** deck
**Justificativa:** conteúdo com hierarquia clara, 7 tópicos discretos, audiência executiva presencial

**Inventário de conteúdo (N elementos)**
- 4 KPIs → métricas 3-up (slides 2-3)
- 2 comparações YoY → gráfico de barras agrupadas
- 1 evolução temporal → linha com área preenchida
- 8 fundos → tabela HTML (8 linhas × 4 colunas) — NÃO bullets
- 3 pilares estratégicos → cards color-coded
- 1 hierarquia de gestão (12 pessoas) → org-chart HTML/CSS

**Mapa de slides/seções proposto**
| # | Tipo | Conteúdo | Visual |
|---|---|---|---|
| 01 | Hero | Título + meta | Atmospheric hero |
| 02 | Metrics | 4 KPIs | Cards 2×2 |
| 03 | Split | Evolução AuM | Gráfico linha |
| 04 | Table | 8 fundos | HTML table |
| ... | | | |

**Elementos que EXIGEM dado real (preencher antes de gerar)**
- AuM exato por categoria
- Nomes dos gestores responsáveis
- Data de referência dos dados

**Confirmar para gerar?** Responda "sim" ou ajuste o mapa acima.
```

## Critérios para escolher o modelo

Consultar [../references/decisao-modelo.md](../references/decisao-modelo.md).

Regra geral por densidade/uso:
- Texto narrativo longo, manual → **handbook**
- Cards/catálogo de recursos → **hub**
- Narrativa scroll-triggered, leitura visual → **scrollytelling**
- Multi-view com abas (2-5 views) → **site**
- Apresentação linear ao vivo → **deck**
- Relatório editorial denso, PDF-friendly → **report**

## Anti-pattern

NÃO chutar o modelo nem inventar conteúdo. Se a fonte é ambígua, perguntar; se a fonte está vazia, aplicar [protocolo-sem-conteudo.md](../references/protocolo-sem-conteudo.md).
