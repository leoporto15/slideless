---
description: Audita documento slideless contra validador determinístico + checklist + anti-patterns
argument-hint: <caminho do arquivo>
---

Você foi invocado para auditar um documento slideless.

## Procedimento

1. **Validador determinístico** (estrutura — regex/DOM):
   ```bash
   python ../scripts/validar.py <arquivo.html>
   ```
   Capturar saída. Cada linha numerada é uma violação a corrigir.
1.5. **Smoke-test de RENDER** (runtime — o validador NÃO vê JS quebrado nem render):
   ```bash
   python ../scripts/smoke.py <arquivo.html>
   ```
   Carrega o doc num Chromium headless e pega o que a estrutura não vê: `PAGEERROR`
   (JS quebrado que mata navegação/animações/números), conteúdo invisível, placeholder
   renderizado. **SMOKE FAIL = bloqueante.** Se imprimir `SKIP` (Playwright ausente),
   instalar: `pip install playwright && python -m playwright install chromium`. Esta rede
   foi adicionada depois que um `<script>` aninhado matou todo o JS de 5 docs em silêncio
   e o validador estrutural passou — render-verificar é obrigatório. O checklist do que o
   smoke pega (overflow, texto-por-caractere, odômetro não-clipado, número duplicado, slide
   curto, invasão de coluna, scroll horizontal) está em
   [../references/wow-components.md](../references/wow-components.md) §"Armadilhas visuais que o smoke.py reprova".
2. **Checklist de revisão LLM** ([../references/checklist-revisao.md](../references/checklist-revisao.md)):
   - Bloqueantes (🚫) — corrigir antes de entregar
   - Alto (⚠️)
   - Médio (🟡)
   - Sugestões (💡)
3. **Anti-patterns** ([../references/anti-patterns.md](../references/anti-patterns.md)):
   - A1-A8 — visuais (PPT-isms)
   - B1-B8 — técnicos
   - C1-C5 — conteúdo
   - C-bis — design fraco (princípios, não receitas)
   - D — específicos por modelo
4. **Categoria P — Pasteurização / cara-de-IA** (julgamento LLM; o validador já cobriu a parte regex). Critério de referência: [../references/direcao-de-arte.md](../references/direcao-de-arte.md). Verificar:
   - **Coerência parti↔HTML**: cada decisão declarada no bloco `<!-- slideless:parti -->` está materializada no CSS/HTML? (declarou capa numero-protagonista e a capa é manchete = falha; declarou motion estático e há keyframe de entrada = falha). Justificativas citam a fonte ou são genéricas ("moderno", "elegante")?
   - **Não-repetição**: comparar o parti com o do exemplo canônico do modelo (assets/exemplos/) e com o do último documento da pasta. Capa/kit/superfície iguais ao canônico = falha. `serie: herdar` declarada é exceção legítima.
   - **Quotas** (ISENÇÃO: documentos com <5 seções/slides ficam isentos das quotas de ritmo, nunca das proibições absolutas): kicker mono-uppercase em ≤1 papel; ≤2 grids de cards (deck: cards em ≤1/3 dos slides); reveal em ≤40% das sections; ≥1 seção fora do padrão título+grid a cada 4.
   - **Momento assinatura**: existe NO LOCAL declarado e está ligado ao dado-tese da fonte (não a um número de apoio)? Pergunta de juízo: é sobre o que o leitor mais precisa lembrar?
   - **Headlines-tese**: h2 afirmam o que a seção prova (verbo/número da fonte)? Títulos-categoria e títulos-fórmula ("Transformando X com Y") = falha.
   - **Paralelismo robótico**: 3+ bullets consecutivos com a mesma estrutura sintática; tricolons em títulos.
   - **Cor com papel**: regime cromático declarado é respeitado? Paleta distribuída em sequência decorativa pela ordem do DOM = falha (C10/C14).
   - **DRIFT — amostrar pesadamente o ÚLTIMO TERÇO do documento**: o modo de falha real é começar seguindo o parti e regredir ao grid de cards default nos slides/seções finais. Comparar a densidade de decisão do primeiro e do último terço.
5. **Ambição (categoria P, nível cutting-edge — [../references/ambicao.md](../references/ambicao.md))**. O validador já cobriu P8 (ambição entregue), P9 (fallback presente), P10 (A3 fora de regulatório). O `/auditar` LLM julga o que regex não vê:
   - **Relevância narrativa do momento-wow**: o W# está ligado ao **dado-tese** (o que o leitor mais precisa lembrar) ou é efeito gratuito? "Motion for motion's sake" reprova. Restraint beats spectacle.
   - **Coerência ambição↔registro**: um report A2 ficou materialmente mais rico (fio, grain, anotação viva) sem ficar saltitante? Spring bouncy / cursor lúdico / aurora saturada num registro sóbrio = reprovado mesmo em A2.
   - **Os 3 invariantes de fato presentes**: cada gesto tem branch reduced-motion real (não só `@supports`)? O estado-final-base existe (o conteúdo aparece num Chrome sem a feature)?
   - **Teste do "parar o scroll"**: algum momento aqui faria um diretor de arte parar? Se o documento é A2 e nada se destaca, a ambição foi declarada mas não realizada (mesmo que P8 tenha passado por ter uma assinatura técnica presente).
6. Compilar relatório priorizado, com **score de fingerprint risk** (baixo/médio/alto) baseado na coocorrência de tells P.

## Formato de saída

```
🚫 BLOQUEANTES (N)
  1. [linha 12] Boot script ausente no <head> antes do CSS — ver design-system.md
  2. ...

⚠️ ALTO (N)
  1. ...

🟡 MÉDIO (N)
  ...

💡 SUGESTÕES (N)
  ...

🎭 FINGERPRINT RISK: baixo / médio / alto
  (coocorrência de tells P — o slop não é um elemento, é a soma de defaults sem decisão)

Resumo: documento PRECISA / NÃO PRECISA de correção antes de entregar.
```

## Não fazer

- Não auto-corrigir. Apenas relatar. O usuário decide o que corrigir.
- Se o usuário pediu correção junto, sugerir comandos específicos (`/polir`, `/harden`).
- Não inventar problemas — só apontar violações reais com referência ao critério. **A categoria P É um critério com referência** (direcao-de-arte.md + anti-patterns C-bis): pasteurização, parti incoerente e headline-categoria são violações reais, não opinião.
