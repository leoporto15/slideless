# AIOps (KBs, MCP, indicadores e ROI de IA) Resources

## Knowledge

### Agentes e contexto (conceitos)
- [Artigo: "Building effective agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/building-effective-agents)
  Distinção entre workflow e agente e padrões de composição. Use para: vocabulário base de agentes.
- [Artigo: "Effective context engineering for AI agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Define agente como "LLM usando ferramentas em loop" e trata o contexto como recurso escasso. Use para: por que KB e MCP existem e como dosar contexto.

### MCP (Model Context Protocol)
- [Especificação oficial: modelcontextprotocol.io](https://modelcontextprotocol.io) · [repositório da spec no GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol)
  Fonte primária do protocolo: host/cliente/servidor, primitivas (tools, resources, prompts), transporte e autorização. Use para: qualquer dúvida de protocolo. Obs.: o domínio está bloqueado na rede desta sessão na nuvem; abrir no seu navegador.
- [Curso: Introduction to Model Context Protocol (Anthropic Academy, gratuito)](https://anthropic.skilljar.com/introduction-to-model-context-protocol) · [Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics)
  Constrói servidor e cliente em Python, cobre as três primitivas. Use para: a trilha prática de MCP (pré-requisito: Python básico).

### Copilot Studio e Microsoft 365
- [Docs: Knowledge sources overview (Microsoft Learn)](https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-studio)
  Fontes de conhecimento de um agente (SharePoint, Dataverse, arquivos, conectores), limites e autenticação. Use para: desenho de KB no Copilot Studio.
- [Docs: Add an MCP server to your agent as a tool (Microsoft Learn)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-add-mcp-server) · [Connect to an existing MCP server](https://learn.microsoft.com/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
  Wizard de MCP e alternativa por custom connector; SSE não é mais suportado (só Streamable HTTP). Use para: plugar servidores MCP em agentes.
- [Docs: Microsoft 365 Copilot extensibility overview](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview) · [Módulo: Extend Copilot's knowledge with Copilot connectors](https://learn.microsoft.com/en-us/training/modules/choose-microsoft-365-copilot-extensibility-path/4-extend-copilot-knowledge-copilot-connectors)
  Copilot connectors (antigos Graph connectors): *synced* (indexam no Graph) vs *federated* (buscam em tempo real via MCP). Use para: escolher entre indexar e consultar ao vivo.
- [Curso: Copilot Studio Agent Academy (Microsoft, gratuito, open source)](https://microsoft.github.io/agent-academy)
  Currículo prático em níveis (Recruit → Operative). Use para: a trilha hands-on de Copilot Studio.
- [Learning path: Agent in a day (Microsoft Learn)](https://learn.microsoft.com/training/paths/agents-online-workshop/)
  Workshop prático de agentes no M365 Copilot Chat e no Copilot Studio (requer ambiente licenciado).

### AWS
- [Docs: How content chunking works for knowledge bases (Amazon Bedrock)](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html)
  Estratégias de chunking (padrão, tamanho fixo, hierárquico, semântico, sem chunking). Use para: desenho técnico de KB em AWS.
- [Docs: AgentCore Gateway core concepts](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-core-concepts.html) · [Using a Gateway with MCP](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-using-mcp.html)
  Gateway como porta de entrada única que expõe APIs, Lambdas e KBs como ferramentas MCP. Use para: arquitetura MCP em AWS.
- [Docs: Use metrics to understand RAG system performance (Bedrock KB evaluation)](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-eval-retrieve-generate.html)
  Métricas nativas: relevância de contexto, fidelidade (faithfulness), correção, precisão de citação. Use para: medir a qualidade de uma KB.
- [Docs: Ragas — métricas de avaliação de RAG](https://docs.ragas.io/)
  Fidelidade, context recall (precisa de resposta de referência) etc. Use para: avaliação de RAG fora do Bedrock.

### Indicadores, valor e ROI de agentes
- [Guia: Agent business value — overview (Microsoft Learn)](https://learn.microsoft.com/en-gb/microsoft-Copilot-studio/guidance/agent-business-value-overview) · [Metrics reference](https://learn.microsoft.com/en-gb/microsoft-Copilot-studio/guidance/agent-business-value-metrics-reference) · [Measure impact](https://learn.microsoft.com/en-gb/microsoft-copilot-studio/guidance/agent-business-value-measure-impact)
  Framework da Microsoft para valor de agentes: eficiência, qualidade, adoção; de onde vem cada número. Use para: a árvore de KPIs da área.
- [Docs: Analyze time and cost savings for agents (Copilot Studio)](https://learn.microsoft.com/microsoft-copilot-studio/analytics-cost-savings)
  Calculadora de economia de tempo e custo no Analytics. Use para: premissas de ROI e limites delas.
- [Docs: Microsoft Copilot Dashboard (Viva Insights)](https://learn.microsoft.com/viva/insights/org-team-insights/copilot-dashboard)
  Prontidão, adoção, impacto e sentimento do M365 Copilot; janela de 28 dias, até 6 dias de atraso, grupo mínimo de 10 pessoas. Use para: indicadores de adoção do M365 Copilot.
- [Blog: Managing Azure OpenAI costs with the FinOps toolkit and FOCUS (Microsoft FinOps blog)](https://techcommunity.microsoft.com/blog/finopsblog/managing-azure-openai-costs-with-the-finops-toolkit-and-focus-turning-tokens-int/4413886)
  Resume as recomendações do grupo de trabalho de IA da FinOps Foundation: custo unitário por token e rateio por time/modelo/feature. Use para: custo unitário de IA.

### Dados e BI
- [Guia: Understand star schema and the importance for Power BI (Microsoft Learn)](https://learn.microsoft.com/power-bi/guidance/star-schema)
  Fato x dimensão, relacionamentos, por que o star schema importa. Use para: modelar o painel de indicadores.

### Governança e segurança de dados para agentes
- [Docs: Configure data security for Microsoft 365 Copilot (Purview + SharePoint Advanced Management)](https://learn.microsoft.com/en-us/copilot/microsoft-365/configure-data-security-copilot)
  Oversharing, restricted access control, revisões de acesso e DLP. Use para: o que uma KB em SharePoint precisa antes de virar fonte de agente.
- [Docs: Copilot Control System — security & governance](https://learn.microsoft.com/microsoft-365/copilot/copilot-control-system/security-governance)
  Visão geral dos controles e do licenciamento. Use para: conversar com segurança da informação.

## Wisdom (Communities)

- [Copilot Studio Community (fórum oficial Power Platform)](https://community.powerapps.com/t5/Copilot-Studio-Community/ct-p/PVACommunity)
  Fórum moderado com boards por tema. Use para: problemas práticos de Copilot Studio e MCP no Copilot Studio.
- [FinOps Foundation Community Slack](https://www.finops.org/community/community-slack/)
  Praticantes de FinOps, com discussão de custo de IA. Use para: unit economics, rateio e cultura de custo.
- Interno: o time estruturante e o time de finanças da nova área
  Use para: validar premissas de ROI e restrições reais da arquitetura (AWS/M365 do Itaú).

## Gaps
- Regulação e políticas internas para IA em banco (BACEN, LGPD, risco de modelo): buscar com as áreas de risco e compliance do Itaú, não em fontes públicas genéricas.
- Comunidade ativa e moderada focada em MCP: ainda não encontrei uma com boa reputação.
- Priorização de portfólio de IA (frameworks tipo RICE/WSJF aplicados a IA): faltam fontes primárias de alta confiança.
