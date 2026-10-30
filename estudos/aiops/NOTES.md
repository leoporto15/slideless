# Notas do professor

## Preferências do aluno
- Idioma: português.
- Quer um plano de estudo completo, "do zero", cobrindo todas as habilidades da função.
- Pediu explicitamente uma base sólida em: funcionamento de LLMs e agentes; dados AI-ready; KBs (estruturas e padrões); ingestão de dados.
- **Painéis: SÓ Amazon QuickSight ou HTML gerado com LLM, alimentados por esteira na AWS.** Nenhuma outra ferramenta de BI: não citar, nem para dizer que não vai usar (o aluno já reforçou duas vezes). Exemplos de modelagem e SQL sempre em Athena/QuickSight.
- Conexão útil: o próprio repo slideless gera HTML single-file com Chart.js (modelo `report`/`hub`), o que pode servir de camada de apresentação dos painéis HTML.

## Contexto
- Nova área: AIOps na "bupf" (provável BU PF = Pessoa Física; confirmar). Três times: estruturante, produtividade individual, finanças/priorização/ROI.
- Função do aluno: especialista de dados e indicadores para a governança da área, e quem define como as áreas estruturam KBs e MCPs (incluindo a execução técnica).
- Stack: AWS + Microsoft 365 (Copilot Studio é o principal; high code eventualmente).

## Calibração
- Acesso (30/10/2026): tem Copilot Studio e AWS. Exercícios práticos são reais, não simulados (sempre com dados fictícios e cuidado com custo/permissões em ambiente corporativo).
- Nível (30/10/2026): baixo em tudo (SQL, Python, AWS, QuickSight, Copilot Studio, LLMs). Ver LR 0002.
- Implicação: explicar sem jargão não definido, um conceito novo por vez, exemplos concretos do mundo bancário/corporativo.

## A calibrar (perguntar)
- Horas por semana e data de início na nova área.

## Notas operacionais
- Workspace em `estudos/aiops/` dentro do repo slideless (escolha do aluno).
- `modelcontextprotocol.io` está bloqueado na rede da sessão na nuvem: citar mesmo assim (o aluno abre no navegador).
- Versões navegáveis (artifacts privados do Claude, republicar ao mudar o HTML):
  - Plano: https://claude.ai/artifact/HHzRiQphhAogBUCQara2cZ
  - Lição 0001: https://claude.ai/artifact/LYY4RPuKBHaWc3GMK9ZTdN
  - Artifacts não carregam CSS/JS por caminho relativo: gerar versão com `assets/` embutido e links trocados pelas URLs dos artifacts.
