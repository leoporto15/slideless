# Mission: AIOps — dados, indicadores, KBs e MCPs para agentes corporativos

## Why
Vou assumir a função de especialista de dados e indicadores da nova área de AIOps da BU PF (sigla a confirmar). A área vai criar soluções agênticas para funcionários internos, principalmente em Copilot Studio e também em high code, e vai priorizar projetos de IA pelo ROI. Preciso (1) desenhar e operar os indicadores com que a área se governa e (2) definir e executar tecnicamente como as outras áreas estruturam bases de conhecimento (KBs) e servidores MCP, para que os agentes delas tenham a melhor informação possível.

## Success looks like
- Propor e defender a árvore de indicadores da área (adoção, qualidade, custo, valor/ROI), com fonte de dado e fórmula definidas para cada um.
- Montar um painel (Power BI ou equivalente) a partir da telemetria real do Copilot Studio / M365 e dos custos AWS.
- Calcular o ROI de um projeto de IA com baseline, premissas explícitas e custo unitário (por conversa, por tarefa resolvida).
- Decidir para um caso real se a informação deve entrar como KB, como ferramenta MCP ou como instrução do agente, e justificar a escolha.
- Desenhar o padrão de KB da empresa (curadoria, estrutura, metadados, permissões, chunking) e medir a qualidade da recuperação com métricas de RAG.
- Construir e publicar um servidor MCP simples, conectá-lo a um agente do Copilot Studio e saber onde o AgentCore Gateway da AWS entra.
- Conversar em pé de igualdade com o time estruturante (engenharia) e com o time de finanças/priorização.

## Constraints
- Stack corporativo: AWS + ambiente Microsoft 365 (Copilot Studio, SharePoint, Power Platform).
- Começando do zero (nível de partida exato a calibrar no diagnóstico).
- Tempo semanal disponível e data de início na nova área: a confirmar.
- Nada de dados internos inventados: exercícios com dados fictícios, claramente marcados.

## Out of scope
- Treinar ou fazer fine-tuning de modelos.
- MLOps de modelos próprios (o foco são agentes sobre modelos prontos).
- Desenvolvimento front-end de produto.
