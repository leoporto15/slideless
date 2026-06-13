# Type-kits — pool de kits tipográficos da slideless

> O kit tipográfico é a **decisão nº 2 do parti** (ver [direcao-de-arte.md](direcao-de-arte.md)). Cada documento escolhe 1 kit completo deste pool, derivado do registro do conteúdo. O kit é um **asset copiável** — cole o `<link>` no slot `SLIDELESS:TYPE-KIT` do template e o bloco `:root` ANTES do bloco do tema. O LLM copia o que o asset mostra; por isso cada kit já vem com eixos limitados, tracking por corpo, features OpenType e fallback de sistema desenhado.

## Regras do pool

1. **Não-repetição:** PROIBIDO usar o kit do exemplo canônico do modelo E o kit do último documento slideless da mesma pasta. Exceção: `serie: herdar de <arquivo>` declarada no parti.
2. **Quota do Kit 06 (Itaú Signal Clássico):** no máximo 1 a cada 3 documentos da mesma pasta — era o default da casa e virou fingerprint. Se escolhido, uso de eixo SOFT ou WONK em ≥1 papel display é obrigatório (senão não há razão para ser Fraunces).
3. **Performance:** usar EXATAMENTE o `<link>` do kit (eixos/pesos limitados). Não adicionar pesos "por garantia" — variable font completa pesa em rede corporativa lenta.
4. **Offline:** o fallback de sistema de cada kit é desenhado, não genérico. O documento deve continuar digno com fonts.googleapis.com bloqueado (cenário real de intranet).
5. **Microtipografia obrigatória em todo kit:** `font-variant-numeric: tabular-nums lining-nums` em tabelas/KPIs/ticks; aspas curvas pt-BR; `text-wrap: balance` em h1–h3; NBSP entre valor e unidade.
6. **Validade:** revisar o pool trimestralmente via `validar.py --stats`. Kit que aparecer em >40% dos documentos do trimestre é aposentado ou ganha quota.

## Banidos (em qualquer papel, qualquer tema)

Fontes-assinatura de IA de 1ª e 2ª geração — presença = falha do validador:

- **Inter como `--font-display`** (em qualquer kit ou tema; como texto, só onde o kit declarar)
- Space Grotesk · Instrument Serif · Syne · Geist / Geist Mono · Poppins · Montserrat · Bebas Neue · Playfair Display
- **Fraunces fora do Kit 06** (era o slop de 2ª geração da própria casa)

---

## Kit 01 — Broadsheet (jornal de negócios)

**Quando:** pesquisa macro, conjuntura, análise com dados pesados, documento que argumenta com números. Registro: denso, sério, números protagonistas.

```html
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,500;0,6..72,800;1,6..72,400&family=Archivo:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```
```css
:root {
  --kit-display: 'Newsreader';   /* capa: wght 300 + opsz alto; ênfase: itálico VERDADEIRO */
  --kit-text:    'Newsreader';   /* corpo serif 17-19px, registro de jornal */
  --kit-ui:      'Archivo';      /* th, labels, nav, ticks de gráfico */
  --kit-mono:    'IBM Plex Mono';/* SÓ código e células .num */
}
```
| Papel | Corpo | Tracking | Peso |
|---|---|---|---|
| Display capa | ≥56px | −0.025em | 300 ou 800 |
| Heading seção | 24–40px | −0.01em | 500/800 |
| Body | 17–19px | 0 | 400 |
| Caps/label (Archivo) | 11–13px | +0.08em | 500 |

Features: corpo `'onum' 'pnum'` · tabelas/KPIs `'tnum' 'lnum'`. Ênfase display: contraste de peso 300↔800 ou itálico verdadeiro — **nunca cor accent como única ênfase**.
Fallback de sistema: display/texto `Georgia, 'Times New Roman', serif` · ui `'Segoe UI', Arial, sans-serif`.

---

## Kit 02 — Relatório Anual (clássico institucional)

**Quando:** report formal, política de crédito, documento regulatório, material que será impresso/PDF. Registro: formal, clássico, bom de imprimir.

```html
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,800;1,7..72,400&family=Public+Sans:wght@400;500;700&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
```
```css
:root {
  --kit-display: 'Literata';     /* opsz 7..72 — display sóbrio com caráter */
  --kit-text:    'Public Sans';  /* corpo sans neutro institucional */
  --kit-ui:      'Public Sans';
  --kit-mono:    'Spline Sans Mono';
}
```
| Papel | Corpo | Tracking | Peso |
|---|---|---|---|
| Display capa | ≥48px | −0.02em | 400 ou 800 |
| Heading seção | 22–36px | −0.005em | 600 |
| Body | 16–17px | 0 | 400 |
| Caps/label | 11–12px | +0.07em | 500 |

Características do registro: fundo flat por princípio (vai para impressão), fio duplo contábil em totais de tabela, motion estático default.
Fallback: display `Georgia, serif` · texto/ui `'Segoe UI', Tahoma, sans-serif`.

---

## Kit 03 — Plex Técnico (engenharia)

**Quando:** runbook, documentação de plataforma, arquitetura, manual de engenharia. Registro: preciso, neutro, sistemático.

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:wght@500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```
```css
:root {
  --kit-display: 'IBM Plex Serif'; /* headings com serifa técnica — distingue de UI sans genérica */
  --kit-text:    'IBM Plex Sans';
  --kit-ui:      'IBM Plex Sans';
  --kit-mono:    'IBM Plex Mono';  /* código, paths, .num, comandos */
}
```
| Papel | Corpo | Tracking | Peso |
|---|---|---|---|
| Display capa | ≥44px | −0.02em | 500/700 |
| Heading seção | 22–32px | −0.005em | 600 |
| Body | 16px | 0 | 400 |
| Caps/label | 11–12px | +0.06em | 500 |

Sistema coeso de 1 fundição: a identidade vem da consistência Plex, não de contraste de famílias. Mono pode ter papel maior que nos outros kits (números de versão, flags, valores).
Fallback: display `Georgia, serif` · texto/ui `'Segoe UI', Arial, sans-serif` · mono `Consolas, monospace`.

---

## Kit 04 — Revista (expressivo e quente)

**Quando:** cultura, pessoas, onboarding, comunicação interna leve, conteúdo narrativo humano. Registro: quente, expressivo, títulos grandes.

```html
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Lora:ital,wght@0,400;0,600;1,400&family=Sometype+Mono:wght@400&display=swap" rel="stylesheet">
```
```css
:root {
  --kit-display: 'Bricolage Grotesque'; /* display "perfectly imperfect" — caráter sem gritar IA */
  --kit-text:    'Lora';                /* corpo serif humanista */
  --kit-ui:      'Bricolage Grotesque';
  --kit-mono:    'Sometype Mono';
}
```
| Papel | Corpo | Tracking | Peso |
|---|---|---|---|
| Display capa | ≥56px | −0.03em | 800 |
| Heading seção | 24–40px | −0.015em | 600 |
| Body (Lora) | 17–18px | 0 | 400 |
| Caps/label | 11–13px | +0.10em | 600 |

Ênfase: itálico verdadeiro da Lora em pull quotes; opsz alto da Bricolage em display.
Fallback: display/ui `'Segoe UI', 'Trebuchet MS', sans-serif` · texto `Georgia, serif`.

---

## Kit 05 — Poster (impacto de auditório)

**Quando:** deck de all-hands, pitch, divisores de impacto, documento-manifesto. Registro: pôster, tipografia gigante, contraste duro.

```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,400;0,62..125,700;0,62..125,900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```
```css
:root {
  --kit-display: 'Archivo';        /* wdth 125 + wght 900 em display; wdth 62 condensado para kickers */
  --kit-text:    'Source Serif 4'; /* contraponto serif para leads e corpo */
  --kit-ui:      'Archivo';
  --kit-mono:    'IBM Plex Mono';
}
```
| Papel | Corpo | Tracking | Peso/Eixo |
|---|---|---|---|
| Display capa | viewport (clamp) | −0.04em | 900, wdth 125 |
| Heading slide | 32–64px | −0.02em | 700 |
| Lead/body | 18–22px | 0 | 400 (serif) |
| Caps/label | 12–14px | +0.06em | 700, wdth 62 |

O contraste do kit É o dispositivo: grotesk black expandida contra serif calma. Usar o eixo wdth (`font-variation-settings: 'wdth' 125`) — é o que separa de um Arial Bold qualquer.
Fallback: display/ui `'Arial Black', 'Segoe UI', sans-serif` · texto `Georgia, serif`.

---

## Kit 06 — Itaú Signal Clássico (a voz histórica da casa — QUOTA 1/3)

**Quando:** continuidade deliberada com documentos pré-v4, registro institucional caloroso. **Só com justificativa citando a fonte, e nunca 2 documentos consecutivos na mesma pasta.**

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..900,0..100,0..1&family=Archivo:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```
```css
:root {
  --kit-display: 'Fraunces';
  --kit-text:    'Archivo';
  --kit-ui:      'Archivo';
  --kit-mono:    'IBM Plex Mono';
}
/* OBRIGATÓRIO se este kit for escolhido: usar SOFT ou WONK em ≥1 papel display —
   senão é o Fraunces default de 2024-26 (slop de 2ª geração). Ex.: */
.title-capa { font-variation-settings: 'opsz' 144, 'SOFT' 75, 'WONK' 1; }
```
| Papel | Corpo | Tracking | Peso/Eixo |
|---|---|---|---|
| Display capa | ≥56px | −0.035em | 300 ou 850, opsz 144 |
| Heading seção | 24–40px | −0.015em | 600 |
| Body (Archivo) | 16–17px | 0 | 400 |
| Caps/label | 11–13px | +0.08em | 500 |

Fallback: display `Georgia, serif` · texto/ui `'Segoe UI', Arial, sans-serif`.

---

## Eixos cinéticos (nível A2/A3 — ver [ambicao.md](ambicao.md) W3/W4)

Os kits já carregam variable fonts com eixos caros. Num documento **A2-elevado/A3**, esses eixos deixam de ser estáticos e **se animam** (a manchete-tese que engorda no scroll, letras que reagem ao cursor) — colher o que já se paga no download.

| Kit | Eixos que valem animar | Gesto típico |
|---|---|---|
| 05 Poster (Archivo) | `wght` 400↔900, `wdth` 62↔125 | manchete expande/engrossa no scroll (W3) |
| 06 Itaú Signal (Fraunces) | `wght`, `SOFT` 0↔100, `WONK` 0↔1, `opsz` | terminais arredondam / vira quirky no hover (W4) |
| 01 Broadsheet (Newsreader) | `opsz` 6↔72, `wght` | optical size dramático na capa |
| 04 Revista (Bricolage) | `wght` 200↔800, `wdth`, `opsz` | display vivo |

**Pool de fontes cinéticas adicionais** (axes que valem animar, não-clichê — usar quando o documento pede tipografia como protagonista):

| Fonte (Google) | Eixos | Por que entra |
|---|---|---|
| **Roboto Flex** | `GRAD`, `opsz`, `wght`, `wdth`, `XTRA`, `YOPQ` | `GRAD` muda peso aparente **sem reflow** — cura o "botão pula no hover" |
| **Big Shoulders** | `wght`, `opsz` | condensada industrial, escultural gigante |
| **Gloock** / **Bodoni Moda** | (Bodoni: `opsz`) | didone de alto contraste — editorial-luxo |
| **Recursive** | `slnt`, `CASL`, `MONO`, `CRSV`, `wght` | eixos raríssimos (casual↔técnico) que quase ninguém usa |
| **Nabla** / **Bungee Spice** | COLRv1 (cromática) | color font com `font-palette` custom (Itaú) — A3 |

**Regras cinéticas:** (a) `overflow:clip`, **nunca** `overflow:hidden`, no ancestral de uma timeline (hidden congela a animation-timeline); (b) sempre `@supports (animation-timeline: view())` com o estado final como base; (c) cursor-proximity (W4) só em `@media (hover:hover) and (pointer:fine)` e desliga em reduced-motion. Banidos continuam banidos (Inter como display, Space Grotesk, Instrument Serif, Poppins, Montserrat).

## Contrato técnico (como o kit conversa com o tema)

Os temas v4 consomem os slots do kit:

```css
/* itau.css */  --font-display: 'Itau Display', var(--kit-display, Georgia), serif;
/* neutro.css */ --font-display: var(--kit-display, Georgia, 'Times New Roman', serif);
```

Ordem no `<style>` do documento: **bloco `:root` do kit → bloco do tema → CSS do modelo**. O `<link>` do kit entra no slot `SLIDELESS:TYPE-KIT` do template. No tema `itau`, Itau Display/Text prevalecem dentro da rede; o kit é o fallback desenhado fora dela — a hierarquia visual (tracking, pesos, features) vale igual nos dois casos.
