# Galeria de temas

Os **7 temas** do slideless aplicados ao **mesmo conteúdo** (a pesquisa *itaú-trump2-comércio*), nos dois modelos mais usados — **deck** e **report** — para comparar lado a lado.

| Tema | Canvas | Par cromático (secundário) |
|---|---|---|
| `itau-padrao` | branco + cool gray (oficial) | azul-tinta |
| `itau-navy` | navy `#000D3C` | dourado/champagne |
| `itau-grafite` | espresso `#1E1C1A` (dark quente) | âmbar |
| `itau-aco` | aço `#1E242C` (dark frio) | ciano |
| `itau-areia` | oat/papel `#ECE4D5` (light quente) | azul-tinta |
| `itau-bruma` | azul-acinzentado `#E7ECF2` (light frio) | teal |
| `neutro` | cool gray (white-label) | dourado |

## O que observar

- **Canvas + identidade**: cada tema com seu canvas e seu secundário (ver tabela).
- **Gráficos na paleta de dados nova** (`--cat`): a série-tese segue a laranja da marca; as séries secundárias usam a paleta categórica calibrada por canvas (ex.: China em teal `--cat-3`), o resto em cinza-mudo (*highlight + mute*).
- **Dark mode**: clique no toggle (canto sup. direito). Nos temas escuros a paleta semântica foi corrigida para o canvas escuro.

## Como abrir

Clique duas vezes em qualquer `.html` — abre no navegador, arquivo único. No **deck**, navegue com as setas (← →), `F` tela cheia, `O` visão geral.

## Como foram gerados

Cada arquivo é o conteúdo do *itaú-trump* com os **tokens de cor do tema** sobrepostos via cascade (bloco `<style id="tema-galeria">`). Fonte única de cada tema: [`assets/temas/<tema>.css`](../../assets/temas) — gerados por `python scripts/gen_temas.py` e auditados por `gen_temas.py --verify` (contraste AA + daltonismo). Detalhes do sistema de cor: [`references/temas/itau.md`](../../references/temas/itau.md).
