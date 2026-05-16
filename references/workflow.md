# Workflow padrão de geração

Passo-a-passo a seguir em todo comando de criação (`/slideless-*`).

---

## Pré-requisitos da sessão

Antes da PRIMEIRA geração da sessão, ler:
1. [anti-patterns.md](anti-patterns.md) (curto, codifica os erros a evitar)
2. [design-system.md](design-system.md) (tokens, boot script)
3. [protocolo-sem-conteudo.md](protocolo-sem-conteudo.md) (regra do conteúdo real)

A partir da 2ª geração da sessão, consultar apenas os arquivos relevantes ao modelo escolhido.

---

## Passos

### 1. Briefing — confirmar antes de qualquer HTML

Coletar quatro itens:

| Item | Default se omisso |
|---|---|
| **Modelo** (handbook/hub/scrollytelling/site/deck) | Aplicar [decisao-modelo.md](decisao-modelo.md) e PERGUNTAR — não chutar |
| **Conteúdo real** | Se ausente, aplicar [protocolo-sem-conteudo.md](protocolo-sem-conteudo.md) |
| **Tema** (neutro/itau) | `itau` |
| **Escopo** (quantas seções/cards/slides/views) | Inferir do conteúdo; perguntar se ambíguo |

Não pular esta etapa para "agilizar". Geração sem briefing = retrabalho garantido.

### 2. Seleção de base

| Cenário | Base |
|---|---|
| Tem conteúdo real | `assets/templates/template-<modelo>.html` (esqueleto vazio) |
| Mostrar referência | `assets/exemplos/exemplo-<modelo>.html` (showcase preenchido) |

Não usar showcase como template — copia conteúdo fictício junto.

### 3. População

- Aplicar regras de [importar-conteudo.md](importar-conteudo.md) conforme a fonte.
- Componentes em [componentes.md](componentes.md).
- Detalhes específicos do modelo em [modelos/<modelo>.md](modelos/).
- Acentos/cores via tokens — nunca hardcode.

### 4. Aplicação do tema

- `itau`: incluir `<link href="…Itau Display + Itau Text + Inter fallback">` (Google Fonts inclui Inter), tokens de `assets/temas/itau.css` inline.
- `neutro`: Inter + JetBrains Mono, tokens de `assets/temas/neutro.css` inline.
- O tema é **inline** no `<style>` do HTML final — não link externo.

### 5. Validação determinística

```bash
python scripts/validar.py <output.html>
```

Saída esperada: `OK` ou lista numerada de violações. Se houver violação, **corrigir antes de prosseguir** — não pular. Violations comuns:
- Boot script ausente no `<head>` antes do CSS
- `[data-theme="dark"]` faltando override de algum token semântico
- Tipografia gigante (≥4rem) fora do `deck`
- Sem `prefers-reduced-motion`
- Keyboard nav ausente no `deck`

### 6. Revisão LLM (cheklist-revisao)

Rodar mentalmente (ou via `/auditar`) os checks de [checklist-revisao.md](checklist-revisao.md). Foco no que o validador determinístico não captura: tom editorial vs pitch, densidade de bullet, hierarquia visual, semântica das cores.

### 7. Entrega

- Salvar em `/mnt/user-data/outputs/<nome-descritivo>.html`.
- Nome descritivo, kebab-case, sem timestamp: `handbook-onboarding-dados.html`.
- Se Claude Code: usar `present_files` com o HTML principal.
- Se gerou múltiplas variações (ex: temas), entregar lista numerada.

---

## Workflow para comandos de edição (`/adicionar-*`, `/aplicar-tema`, `/converter-modelo`)

1. **Receber arquivo HTML existente** (path ou conteúdo).
2. **Validar que o arquivo é slideless válido** — rodar `validar.py --quick` (modo identificação).
3. **Identificar o modelo** lendo classes raiz: `.deck` → deck; `.layout` com `.sidebar` → handbook; `.hub` → hub; etc.
4. **Aplicar a edição cirurgicamente** — Edit tool, não Write — para preservar conteúdo existente.
5. **Revalidar** com `validar.py`.
6. **Retornar arquivo modificado.**

---

## Workflow para comandos de qualidade (`/auditar`, `/polir`, `/harden`)

### `/auditar`
1. Rodar validador determinístico.
2. Aplicar checklist [checklist-revisao.md](checklist-revisao.md) parte por parte.
3. Confrontar contra [anti-patterns.md](anti-patterns.md).
4. Retornar relatório priorizado: críticos > altos > médios > sugestões.

### `/polir`
Focado em tipografia, espaçamento, hierarquia. Não toca em estrutura nem conteúdo.

### `/harden`
Focado em a11y, keyboard, reduced motion, contraste. Foca em conformidade WCAG AA.

---

## Workflow para export (`/exportar-pdf`, `/exportar-screenshots`)

Ver [../scripts/exportar_pdf.py](../scripts/exportar_pdf.py). Resumo:

| Modelo | Orientação PDF | Notas |
|---|---|---|
| handbook | A4 retrato | Sidebar suprimida via `@media print` |
| hub | A4 retrato | Painéis expandidos em ordem |
| scrollytelling | A4 retrato | Sticky charts viram inline |
| site | A4 retrato | Todas as views em ordem |
| deck | A4 landscape (ou 16:9) | 1 slide por página, fragments todos visíveis |

`@media print` no CSS de cada modelo já trata as supressões. Playwright dispara `page.pdf()` com `printBackground=true`.
