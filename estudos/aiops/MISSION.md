# Mission: AIOps — dados, indicadores, KBs e MCPs para agentes corporativos

## Why
Vou assumir a função de especialista de dados e indicadores da nova área de AIOps da BU PF (sigla a confirmar). A área vai criar soluções agênticas para funcionários internos, principalmente em Copilot Studio e também em high code, e vai priorizar projetos de IA pelo ROI. Preciso (1) desenhar e operar os indicadores com que a área se governa e (2) definir e executar tecnicamente como as outras áreas preparam seus dados e estruturam bases de conhecimento (KBs) e servidores MCP, para que os agentes delas tenham a melhor informação possível.

## Success looks like
- Explicar como um LLM e um agente funcionam por dentro (tokens, contexto, embeddings, uso de ferramentas em loop) o bastante para diagnosticar por que um agente erra, custa caro ou alucina.
- Avaliar se um conjunto de dados de uma área está pronto para IA (*AI-ready*) e listar o que falta: metadados, dono, frescor, permissões, formato.
- Desenhar uma esteira de ingestão na AWS (S3 → Glue → Athena, com camadas bruto/curado/consumo) para os dados de que a área precisa.
- Definir o padrão de KB da empresa (estrutura de documentos, metadados, chunking, busca híbrida, permissões) e medir a qualidade da recuperação com métricas de RAG.
- Decidir para um caso real se a informação deve entrar como KB, como ferramenta MCP ou como instrução do agente, e justificar a escolha.
- Construir e publicar um servidor MCP simples, conectá-lo a um agente do Copilot Studio e saber onde o AgentCore Gateway da AWS entra.
- Propor e defender a árvore de indicadores da área (adoção, qualidade, custo, valor/ROI), com fonte de dado e fórmula definidas para cada um.
- Entregar painéis em Amazon QuickSight e em HTML gerado com LLM, ambos alimentados por uma esteira automatizada na AWS, com os números vindo sempre da esteira e nunca do modelo.
- Calcular o ROI de um projeto de IA com baseline, premissas explícitas e custo unitário (por conversa, por tarefa resolvida).

## Constraints
- Stack corporativo: AWS + ambiente Microsoft 365 (Copilot Studio, SharePoint, Power Platform).
- Painéis: Amazon QuickSight ou HTML gerado com LLM, alimentados por esteira na AWS.
- Começando do zero (nível de partida exato a calibrar no diagnóstico).
- Tempo semanal disponível e data de início na nova área: a confirmar.
- Nada de dados internos inventados: exercícios com dados fictícios, claramente marcados.

## Out of scope
- Treinar ou fazer fine-tuning de modelos.
- MLOps de modelos próprios (o foco são agentes sobre modelos prontos).
