# Direção de arte — o Parti

> **Regra inviolável: nenhuma linha de HTML antes do parti.** Todo documento slideless nasce de um bloco `<!-- slideless:parti -->` com 7 decisões em cascata, colado no `<head>` do arquivo entregue. O slop de IA não é a presença de um elemento — é a coocorrência de defaults sem nenhuma decisão intencional. O parti é o antídoto: decisão declarada, derivada do conteúdo, auditável por grep para sempre.

---

## O bloco

```html
<!-- slideless:parti
conteudo: <assunto em 1 linha — tese ou pergunta central da fonte>
registro: <da tabela §1, com a citação da fonte que o justifica>
kit: <código do kit de type-kits.md + por quê ESTE conteúdo o pede>
capa: <1 das 12 de §3 + qual elemento da fonte a protagoniza>
superficie: <1 tratamento de §4 + regime de luz>
motion: <1 perfil de §5>
ambicao: <A1-contido | A2-elevado | A3-extraordinario + o elemento da fonte que justifica o nível — ver ambicao.md>
assinatura: <M0-M6 de §6 + qual dado/afirmação da fonte ela anima e ONDE>
momento-wow: <se ambicao A2/A3: 1+ de W1-W9 de ambicao.md, ligado ao dado-tese e ONDE — omitir se A1>
nao-vai-ter: <3 features do vocabulário de §8>
serie: <opcional: "herdar de <arquivo>" para família de documentos>
-->
```

> **A 7ª decisão — `ambicao`** ([ambicao.md](ambicao.md)) — é ortogonal ao registro: o registro decide *como soa* (sóbrio↔expressivo), a ambição decide *quão longe o craft vai* (contido↔extraordinário). Default: **A2-elevado** para deck/scrollytelling/hub/site/handbook; **A1-contido** para report/regulatório. A ambição respeita o registro como teto de exuberância (A3 proibido em registros sóbrios). Se `ambicao` for A2/A3, o campo `momento-wow` é obrigatório.

**Derivação textual obrigatória:** cada decisão cita um elemento concreto da fonte — um substantivo, um número, uma tensão ("guerra comercial → motivo: linhas de tarifa", "ROE 22,3% → capa numero-protagonista"). Justificativa genérica ("moderno", "elegante", "clean") é inválida e reprovada pelo `/auditar`. Se o conteúdo não decidir um eixo, declarar `neutro por decisão` — nunca herdar o default silenciosamente.

### Exemplo 1 — resultados trimestrais

```html
<!-- slideless:parti
conteudo: 1T26 — tese: "lucro recorde com custo de crédito caindo"
registro: relatorio-de-bancada (documento argumenta com 14 números; leitor é analista)
kit: 01-broadsheet (números protagonistas pedem serif de jornal + tnum)
capa: numero-protagonista (ROE 22,3% gigante sangrando a margem direita — é a manchete da fonte)
superficie: flat + fio de coluna 1px (vai virar PDF de RI; luz por fio, não por sombra)
motion: estatico (leitura de análise — zero reveal; única transição: toggle de tema)
ambicao: A1-contido (vai virar PDF assinado; sobriedade é requisito, não limitação)
assinatura: M0 — tabela de strata do resultado em full-bleed na seção 02, fio duplo no total (compositiva, sem motion)
nao-vai-ter: glow-radial; kicker-dot; card-com-filete
-->
```

### Exemplo 2 — guerra comercial (assunto oposto → parti oposto)

```html
<!-- slideless:parti
conteudo: Trump 2 e o comércio Brasil-China — tese: "tarifa de 60% redesenha fluxos"
registro: condensado-noticioso (tema de tensão/urgência; fonte tem cronologia de choques)
kit: 05-poster (manchetes condensadas para um tema de manchete)
capa: banda-de-cor (banda ink atravessando com "60%" em knockout — a tarifa É a notícia)
superficie: pauta de linhas (registro de despacho/telegrama) + luz hard-print (sombra offset dura)
motion: editorial (só os gráficos revelam; 1 gesto, 350ms)
ambicao: A2-elevado (a cronologia de choques é a história — pede cena scroll-driven que se constrói)
assinatura: M5 — cena sticky: banda sombreada "2018-20 guerra comercial v1" acende no gráfico quando o step a narra
momento-wow: W1 cena scroll-driven (3 estados do gráfico de tarifas) + W8 anotação viva (banda acende no step); W3 manchete cinética na capa (Archivo wdth 80→125)
nao-vai-ter: glow-radial; grid-3-cards; em-italico-accent
-->
```

---

## §1. Registro — a primeira decisão roteia as outras

Classificar o ASSUNTO (não o modelo) na tabela. O registro define os defaults coerentes; os demais eixos podem divergir do default com justificativa.

| Assunto | Registro | Kit default | Superfície default | Motion default |
|---|---|---|---|---|
| Resultados, RI, balanço, dados pesados | `relatorio-de-bancada` | 01 Broadsheet | flat + fio | estático |
| Política, norma, regulatório, impressão | `institucional-impresso` | 02 Relatório Anual | flat | estático |
| Plataforma, arquitetura, runbook, eng. | `tecnico-preciso` | 03 Plex Técnico | hairline-grid ou dot-grid | editorial |
| Cultura, pessoas, onboarding, narrativa | `revista-interna` | 04 Revista | vinheta-papel ou grain | editorial |
| All-hands, pitch, lançamento ao vivo | `poster-de-auditorio` | 05 Poster | banda de cor ou grain | cinemático |
| Crise, tensão, urgência, cronologia de choques | `condensado-noticioso` | 05 Poster (wdth 62) | pauta de linhas | editorial |
| Continuidade com a série pré-v4 | `itau-signal-classico` | 06 Itaú Signal (quota 1/3) | glow localizado permitido | editorial |

No `/criar`, o registro é traduzido em pergunta leiga ("Como esse documento deve soar?") com sugestão automática pelo assunto e confirmação de 1 clique.

---

## §2. Kit tipográfico

Escolher em [type-kits.md](type-kits.md). Regras: proibido o kit do exemplo canônico do modelo e o do último documento da pasta (exceto `serie:`); Kit 06 tem quota; Inter como display e as fontes banidas falham o validador. O kit traz tracking por corpo e features OpenType — copiar o bloco, não recalcular.

---

## §3. Capa — 12 estruturas nomeadas

A capa é a primeira impressão e o tell mais imediato. Escolher exatamente 1 e nomeá-la no parti. **A capa do exemplo canônico do modelo é sempre proibida.** Híbrido só nomeando a base.

1. **numero-protagonista** — o número-tese da fonte em corpo gigante (até 18-24vw no deck), sangrando uma margem; título em corpo pequeno ao lado.
2. **manchete-broadsheet** — título multi-linha peso máximo alinhado à esquerda, fio fino acima, dateline discreta — primeira página de jornal.
3. **frontispicio** — centrado, simétrico, margens generosas, fio duplo — folha de rosto de livro institucional.
4. **tabela-capa** — a tabela-síntese da fonte É a capa (broadsheet, sem card), com título acima.
5. **full-bleed-tipografico** — uma palavra/frase curta ocupando a viewport inteira, sem mais nada além do dateline.
6. **capa-diagrama** — um SVG inline (fluxo, mapa, estrutura) como protagonista, título subordinado.
7. **dossie-carimbo** — bloco de metadados (área, data, classificação) tratado como carimbo/etiqueta de dossiê + título seco.
8. **split-assimetrico** — 2 colunas desiguais (2fr/1fr): título de um lado, dado ou índice do outro.
9. **capa-indice** — o sumário É a capa (estilo revista: lista de seções com números de página/âncoras).
10. **letterpress-minima** — título pequeno, centrado num mar de espaço negativo; only-type, zero ornamento.
11. **banda-de-cor** — banda horizontal de cor sólida atravessando a viewport com título em knockout; resto neutro.
12. **citacao-abertura** — a frase mais forte da fonte como display itálico com aspas penduradas; título vem depois.

---

## §4. Superfície + luz

**Texturas (escolher 1; todas custo-zero de rede, inline):**

| Tratamento | Quando | Implementação |
|---|---|---|
| `flat` | impressão, registro sóbrio — **opção legítima e frequente** | nada — a decisão é o espaço e o fio |
| `flat+vinheta` | flat com profundidade mínima | `--vignette` em pseudo-elemento |
| `grain` | registro quente/editorial — quebra a perfeição digital | feTurbulence data-URI (abaixo), opacity 0.04–0.10 |
| `dot-grid` | técnico/blueprint | `background-image: radial-gradient(...)` 1px |
| `hairline-grid` | engenharia, console | `repeating-linear-gradient` fios 1px espaçados |
| `pauta-de-linhas` | noticioso, despacho | `repeating-linear-gradient` horizontal sutil |
| `banda-de-cor` | poster, divisores | bloco sólido estrutural, não decorativo |
| `glow-localizado` | 1 elemento-herói APENAS | radial-gradient atrás de UM elemento — **nunca em body::before incondicional** |

```css
/* grain — SVG inline, zero rede, zerar em @media print */
--grain: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
body::after { content:''; position:fixed; inset:0; background:var(--grain);
  opacity:.06; mix-blend-mode:soft-light; pointer-events:none; z-index:9999; }
@media print { body::after { display:none; } }
```

**Regimes de luz (escolher 1):** `flat` (profundidade só por fio e contraste) · `key-light` (sombra 3 camadas em elementos elevados) · `hard-print` (sombra offset dura `4px 4px 0 var(--color-fg)` — registro impresso) · `glow-spot` (1 glow atrás do dado-herói).

Cantos: no máximo 2 valores de `border-radius` distintos por documento. Radius idêntico em card+tabela+code+callout é fingerprint.

---

## §5. Motion — 4 perfis mutuamente exclusivos

O perfil determina QUAIS keyframes existem no arquivo. **Templates nascem sem motion; o perfil escolhido é COLADO como bloco aditivo** (adição confiável > deleção não-confiável). Regras transversais: `transition` sempre property-scoped (**`transition: all` proibido**); 2–3 easings nomeadas com papel comentado; entrada ≤500ms; micro-interação 120–200ms; só a assinatura pode exceder 500ms; tabela, texto corrido, TOC e nav NUNCA animam entrada; counter animado só no número declarado na assinatura; tudo dentro de `prefers-reduced-motion: reduce` vira opacity-only ou nada.

### Perfil `estatico` (default: report, relatório-de-bancada)
```css
/* NENHUM keyframe de entrada no arquivo. Única transição: toggle de tema. */
:root { --ease-snap: cubic-bezier(0.2, 0, 0, 1); /* papel: micro-interação */ }
.theme-toggle { transition: background-color 150ms var(--ease-snap), border-color 150ms var(--ease-snap); }
```

### Perfil `editorial` (handbook, scrollytelling calmo, noticioso)
```css
/* 1 gesto, SÓ em figuras/dados — nunca em texto corrido. */
:root {
  --ease-out:  cubic-bezier(0.2, 0.6, 0.2, 1);  /* papel: entrada de figura */
  --ease-snap: cubic-bezier(0.2, 0, 0, 1);       /* papel: micro-interação  */
}
[data-reveal] { opacity: 0; transition: opacity 350ms var(--ease-out); }
[data-reveal].is-visible { opacity: 1; }
/* aplicar data-reveal APENAS em .figure, .chart-wrap, .metric — ≤40% das sections */
@media (prefers-reduced-motion: reduce) { [data-reveal] { opacity: 1; transition: none; } }
```

### Perfil `cinematico` (deck, poster-de-auditorio)
```css
/* Até 3 gestos, mapeados POR PAPEL — nunca o mesmo para tudo. */
:root {
  --ease-emphatic: cubic-bezier(0.16, 1, 0.3, 1);   /* papel: hero/divider */
  --ease-out:      cubic-bezier(0.2, 0.6, 0.2, 1);  /* papel: dado/figura  */
  --ease-snap:     cubic-bezier(0.2, 0, 0, 1);       /* papel: fragment     */
}
/* hero: escolher 1 — fade seco | wipe clip-path | settle. Quote entra SECA (sem stagger). */
/* stagger: só em grupo homogêneo (barras do mesmo chart, itens da MESMA lista), máx 1 grupo/viewport */
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition-duration: 1ms !important; } }
```

### Perfil `fisico` (springs, scroll-driven, View Transitions)
**Reservado ao `/slideless-overdrive`** — em Chrome corporativo gerenciado o fallback vira o caminho primário; não compensa no core.

**Hover por papel (qualquer perfil):** links = underline-grow; tabs/filtros = background-sweep; card CLICÁVEL = lift leve OU border-draw OU contraste (1 escolha por documento); card informativo = nenhum. `translateY` negativo em hover de elemento sem destino (href/handler) = falha.

---

## §6. Momento assinatura — M0–M6

Exatamente 1 por documento, ligado ao **dado ou afirmação mais importante da fonte**, com localização declarada no parti (o `/auditar` verifica existência no local declarado). Motion anima o dado, nunca apenas o container.

- **M0** — assinatura COMPOSITIVA, sem motion (única opção válida no perfil `estatico`): o dado-tese protagoniza um dispositivo editorial — tabela-protagonista full-bleed com fio duplo, número sangrando a margem, pull-quote display. A força vem da composição, não do movimento.
- **M1** — número-tese que se constrói até o valor REAL da fonte (counter com easing).
- **M2** — linha/barra do gráfico-tese que se desenha até o dado real (Chart.js animação progressiva por ponto).
- **M3** — wipe de divider via clip-path (deck) no slide-virada da narrativa.
- **M4** — morph entre estados (site: troca de view com continuidade do elemento-chave).
- **M5** — cena sticky com anotação que acende no step que a narra (scrollytelling).
- **M6** — diagrama SVG que se traça via stroke-dashoffset.

**Motivo gráfico recorrente (opcional, recomendado):** 1 dispositivo derivado do assunto presente em capa + ≥1 seção + fechamento. Arquétipos seguros: fio duplo contábil, sparkline do dado-tese, banda anotada, numeral de seção característico. Renúncia declarada é válida. Não reusar o motivo de outro documento.

---

## §7. Rotulagem e dispositivos editoriais

**Cardápio de labels** (o kicker mono-uppercase com dot era O tique da casa — agora é 1 opção entre 4, permitido em no máximo 1 papel por documento):
1. Kicker mono-uppercase (o clássico — default tributado: exige justificativa)
2. Small-caps com tracking (`font-variant-caps: all-small-caps; letter-spacing: 0.08em`)
3. Numeral de seção em serif old-style grande (02 — sem caixa, sem dot)
4. Fio lateral de 2px + texto em peso 600 (sem uppercase)

**Dispositivos que quebram a coluna** (≥1 seção a cada 4 fora do padrão título+grid): full-bleed; numeral sangrando a margem; assimetria 2fr/1fr; marginalia na coluna do TOC; tabela-protagonista sem card; pull-quote display sem caixa (aspas penduradas); capitular de 3-4 linhas; friso de dados em largura total.

---

## §8. `nao-vai-ter` — vocabulário fechado

Declarar exatamente 3. O validador confere por regex que nenhum aparece no HTML (falha P7):

| Feature | Regex de detecção |
|---|---|
| `glow-radial` | `radial-gradient` em `body::before/after` ou classe glow |
| `kicker-dot` | padrão mono+uppercase+`::before` dot |
| `hover-lift` | `:hover[^}]*translateY\(-` |
| `grid-3-cards` | `repeat\(3,\s*1fr\)` em grid de cards |
| `em-italico-accent` | `h\d[^}]*em[^}]*color.*accent` ou `.title-* em` |
| `gradient-text` | `background-clip:\s*text` |
| `glassmorphism` | `backdrop-filter:\s*blur` decorativo |
| `card-com-filete` | `border-(left\|top):\s*[3-9]px solid var\(--color-` em card |
| `stagger-linear` | `calc\(var\(--i[^)]*\)\s*\*` |
| `counter-animado` | função de count-up no JS |
| `timeline-dot` | `.timeline__dot` ou equivalente |
| `badge-pill` | `border-radius:\s*999px` em label |
| `sombra-difusa-em-tudo` | mesma `box-shadow` em >3 tipos de componente |
| `fade-up` | `translateY\(\d+px\)` como estado inicial de reveal |
| `divider-laranja` | `data-background-color` laranja em divisor |

---

## §9. Não-repetição

1. **Contra o exemplo canônico do modelo** (verificação dura, sempre possível): capa ≠, kit ≠, superfície ≠. Três comparações binárias.
2. **Contra o último documento slideless da pasta** (best-effort): ler o bloco parti dele antes de decidir; ≥2 eixos diferem. Glow localizado proibido se o anterior o usou.
3. **Série declarada:** `serie: herdar de <arquivo>` copia o parti inteiro deliberadamente — relatórios mensais da mesma área DEVEM parecer parentes. Continuidade é decisão, não acidente.

**Default tributado:** a opção marcada como default em cada vocabulário só entra com justificativa de 1 linha citando a fonte. Usar ≥3 defaults da casa no mesmo documento é proibido.

---

## §10. Quotas e isenção

Documentos com **<5 seções/slides** ficam isentos das quotas de ritmo (dispositivo a cada 4 seções, % de reveal) — **nunca** das proibições absolutas (fontes banidas, `transition: all`, hover-lift em não-clicável, nao-vai-ter). Sem essa isenção, o LLM inventa conteúdo para cumprir cota — violando a regra-mãe C0 (conteúdo 100% preservado).

---

## Checklist de saída (antes de entregar)

- [ ] Bloco parti completo no `<head>`, cada decisão citando a fonte
- [ ] Capa, kit e superfície ≠ exemplo canônico do modelo
- [ ] `nao-vai-ter`: os 3 termos ausentes do HTML (conferir por busca)
- [ ] Momento assinatura existe NO LOCAL declarado e anima o dado-tese
- [ ] Tabelas/KPIs com `tabular-nums`; Chart com `defaults.font.family` dos tokens
- [ ] `ambicao` declarada e coerente com o registro; se A2/A3, ≥1 `momento-wow` (W#) entregue com `@supports`+fallback — ver [ambicao.md](ambicao.md)
- [ ] Cobrindo o logo e o laranja: este documento é distinguível do exemplo canônico e do último da pasta? **E (A2/A3): algum momento faria um diretor de arte parar o scroll?**
