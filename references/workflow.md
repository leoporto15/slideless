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

Coletar cinco itens:

| Item | Default se omisso |
|---|---|
| **Modelo** (handbook/hub/scrollytelling/site/deck/report) | Aplicar [decisao-modelo.md](decisao-modelo.md) e PERGUNTAR — não chutar |
| **Conteúdo real** | Se ausente, aplicar [protocolo-sem-conteudo.md](protocolo-sem-conteudo.md) |
| **Tema** (neutro/itau) | `itau` |
| **Escopo** (quantas seções/cards/slides/views) | Inferir do conteúdo; perguntar se ambíguo |
| **Registro/voz** ("como deve soar?") | Inferir do ASSUNTO pela tabela de [direcao-de-arte.md](direcao-de-arte.md) §1 e confirmar em linguagem leiga |

Não pular esta etapa para "agilizar". Geração sem briefing = retrabalho garantido.

### 1.5 Parti — obrigatório, antes de qualquer HTML

1. Abrir [direcao-de-arte.md](direcao-de-arte.md) e rotear o assunto pela tabela de registros.
2. Ler o bloco parti do **exemplo canônico do modelo** (assets/exemplos/) e do **último documento slideless da pasta de destino** (se existir).
3. Preencher as 7 decisões (registro, kit, capa, superfície, motion, ambição, assinatura) + `nao-vai-ter`, **cada uma citando um elemento da fonte**. A 7ª, `ambicao` (A1/A2/A3 — [ambicao.md](ambicao.md)), exige `momento-wow` se A2/A3. Capa/kit/superfície nunca repetem o canônico; ≥2 eixos diferem do doc anterior (`serie: herdar` é exceção declarada).
4. Colar o bloco `<!-- slideless:parti -->` no `<head>` — só então prosseguir ao template.

Documento sem parti = falha P0 no validador.

### 2. Seleção de base

| Cenário | Base |
|---|---|
| Tem conteúdo real | `assets/templates/template-<modelo>.html` (esqueleto vazio) |
| Mostrar referência | `assets/exemplos/exemplo-<modelo>.html` (showcase preenchido) |

Não usar showcase como template — copia conteúdo fictício junto.

### 3. Composição (não "população")

- Aplicar regras de [importar-conteudo.md](importar-conteudo.md) conforme a fonte.
- Componentes em [componentes.md](componentes.md) — **adaptados ao parti**, não colados verbatim.
- Detalhes específicos do modelo em [modelos/<modelo>.md](modelos/).
- Acentos/cores via tokens — nunca hardcode.
- **Re-ancoragem anti-drift:** a cada ~5 seções/slides gerados, reler o bloco parti e conferir que as últimas seções ainda o seguem (o modo de falha real é regredir ao grid de cards default no final do documento).

### 4. Aplicação do tema + kit

- Kit tipográfico do parti: `<link>` EXATO de [type-kits.md](type-kits.md) no slot `SLIDELESS:TYPE-KIT` + bloco `:root` do kit ANTES do bloco do tema.
- `itau`: tokens de `assets/temas/itau.css` inline — camada `[MARCA]` intacta; camada `[DIREÇÃO]` composta conforme o parti.
- `neutro`: tokens de `assets/temas/neutro.css` inline (o kit é 100% da voz tipográfica).
- Perfil de motion do parti colado como bloco aditivo ([direcao-de-arte.md](direcao-de-arte.md) §5) — os temas não trazem motion.
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

### 6.5 Gate perceptual (degradação graciosa)

Se Playwright disponível: `python scripts/exportar_pdf.py --mode screenshots` das 3 primeiras telas e responder BINARIAMENTE: algo sangra da viewport? o contraste da capa funciona nos 2 temas? a 1ª dobra é distinguível do exemplo canônico do modelo (comparar lado a lado)? **(A2/A3) algum momento faria um diretor de arte parar o scroll?** **(A2/A3) o documento sobrevive degradado — testar com `@supports` falhando / sem WebGL: o estado-final-base aparece?** Falhou 2+ → corrigir antes de entregar. Sem Playwright: pular e REGISTRAR o aviso no relatório de entrega.

### 7. Entrega

- Salvar em `outputs/<nome-descritivo>.html`.
- Nome descritivo, kebab-case, sem timestamp: `handbook-onboarding-dados.html`.
- Se Claude Code: usar `present_files` com o HTML principal.
- Se gerou múltiplas variações (ex: temas), entregar lista numerada.
- Reportar o parti aplicado em 1 linha leiga ("abre com o 22,3% gigante, tipografia de jornal, sem efeitos de brilho").

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
