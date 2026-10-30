# AIOps (KBs, MCP, indicadores e ROI de IA) Resources

## Knowledge

### Como LLMs funcionam
- [Vídeo: "Deep Dive into LLMs like ChatGPT" — Andrej Karpathy (YouTube, ~3h30, fev/2025)](https://www.youtube.com/watch?v=7xTGNNLPyMI)
  Pipeline completo para público geral: dados, tokenização, pré-treino, pós-treino (assistente), alucinação, uso de ferramentas. Use para: a base conceitual da Fase 1. Assistir em blocos.
- [Vídeo: "Transformers, the tech behind LLMs" — 3Blue1Brown (Deep Learning, cap. 5)](https://www.youtube.com/@3blue1brown) + "Attention in transformers, step-by-step"
  Explicação visual de embeddings, atenção e previsão do próximo token. Use para: intuição de embeddings (base de toda busca semântica em KB).

### Agentes e contexto (conceitos)
- [Artigo: "Building effective agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/building-effective-agents)
  Distinção entre workflow e agente e padrões de composição. Use para: vocabulário base de agentes.
- [Artigo: "Effective context engineering for AI agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Define agente como "LLM usando ferramentas em loop" e trata o contexto como recurso escasso. Use para: por que KB e MCP existem e como dosar contexto.
- [Curso: AI Agents for Beginners (Microsoft, GitHub, gratuito, MIT)](https://github.com/microsoft/ai-agents-for-beginners)
  Lições curtas com código sobre padrões de agentes (uso de ferramentas, planejamento, multiagente, RAG agêntico). Use para: a parte "high code" de agentes.
- [Curso: Hugging Face Agents Course (gratuito, com certificado)](https://huggingface.co/learn/agents-course)
  Fundamentos de agentes com exercícios e comunidade no Discord. Use para: alternativa/complemento ao curso da Microsoft.

### MCP (Model Context Protocol)
- [Especificação oficial: modelcontextprotocol.io](https://modelcontextprotocol.io) · [repositório da spec no GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol)
  Fonte primária do protocolo: host/cliente/servidor, primitivas (tools, resources, prompts), transporte e autorização. Use para: qualquer dúvida de protocolo. Obs.: o domínio está bloqueado na rede desta sessão na nuvem; abrir no seu navegador.
- [Curso: Introduction to Model Context Protocol (Anthropic Academy, gratuito)](https://anthropic.skilljar.com/introduction-to-model-context-protocol) · [Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics)
  Constrói servidor e cliente em Python, cobre as três primitivas. Use para: a trilha prática de MCP (pré-requisito: Python básico).

- [Docs: How to implement the Atlan MCP server (Atlan)](https://docs.atlan.com/product/capabilities/atlan-ai/how-tos/how-to-implement-the-atlan-mcp-server) · [GitHub: atlanhq/agent-toolkit](https://github.com/atlanhq/agent-toolkit)
  Servidor MCP oficial do catálogo Atlan: busca semântica de ativos, linhagem, atualização de metadados. A busca melhora quanto mais o catálogo estiver enriquecido. Use para: exemplo real de MCP na Fase 5 e ponte entre catálogo de dados e agentes.

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

### Engenharia de dados e ingestão
- [Livro: *Fundamentals of Data Engineering* — Joe Reis & Matt Housley (O'Reilly, 2022)](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)
  Ciclo de vida dos dados (geração → ingestão → armazenamento → transformação → servir). O cap. 7 trata de ingestão: batch x streaming, push/pull, snapshot x incremental, ETL x ELT. Use para: o vocabulário e as decisões de ingestão.
- [Docs: Managing partitions for ETL output in AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-partitions.html)
  Como crawlers inferem partições e como Athena/Glue as usam para não ler o lake inteiro. Use para: layout de dados no S3.
- [Blog: Top 10 performance tuning tips for Amazon Athena (AWS Big Data Blog)](https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/)
  Particionamento, formato colunar (Parquet), compressão, tamanho de arquivo. Use para: esteira barata e rápida.
- Padrão bronze/prata/ouro (medallion) no S3 com Glue e Athena: só encontrei fontes secundárias (ex.: [DEV Community — Medallion architecture on AWS](https://dev.to/aws-builders/medallion-architecture-on-aws-2ngm)). Use para: visão geral; validar com o time estruturante.

### Dados prontos para IA (AI-ready)
- [Resumo: Gartner sobre maturidade de metadados e dados AI-ready (Alation)](https://alation.com/blog/metadata-maturity-ai-ready-data-gartner)
  Fonte secundária do framework do Gartner: prontidão depende do caso de uso, e metadados e governança são centrais. Use para: o conceito. O relatório original ("How to Evaluate AI Data Readiness", Gartner, jan/2025) é pago.
- [Docs: Parsing options for your data source (Amazon Bedrock KB)](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-advanced-parsing.html)
  Parser padrão (só texto), Bedrock Data Automation e parser por modelo (para tabelas, gráficos e imagens). Use para: preparar documentos não estruturados.

### AWS (KBs e agentes)
- [Guia: Retrieval Augmented Generation options and architectures on AWS (AWS Prescriptive Guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html) · [Choosing a RAG option](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/choosing-option.html)
  Compara RAG gerenciado e customizado e recomenda uma ordem de escolha. Use para: decidir a arquitetura de KB em AWS.
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

### Modelagem e painéis (QuickSight / HTML)
- [Kimball Group: Dimensional modeling techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/) · [Grain](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/grain/)
  Fonte primária de fato, dimensão e granularidade (*grain*), resumida de *The Data Warehouse Toolkit*. Use para: modelar a camada ouro dos indicadores.
- [Docs: Amazon Quick Sight user guide (BI)](https://docs.aws.amazon.com/quick/latest/userguide/quick-bi.html)
  Datasets, análises, dashboards. O produto agora faz parte do Amazon Quick Suite, e a documentação usa os dois nomes. Use para: painéis gerenciados.
- [Blog: Best practices for Amazon QuickSight SPICE and direct query mode (AWS BI Blog)](https://aws.amazon.com/blogs/business-intelligence/best-practices-for-amazon-quicksight-spice-and-direct-query-mode/)
  Quando importar para o SPICE (memória) e quando consultar o Athena direto. Use para: custo e latência dos painéis.
- Painéis em HTML gerados com LLM: o próprio repo slideless é um exemplo. Uma skill guia o LLM a gerar relatórios HTML single-file com Chart.js (modelos `report` e `hub`), com template, regras e validação (`validar.py`). Padrão: a esteira gera um JSON na camada ouro, o LLM escreve ou atualiza o código da página, e os números vêm sempre do JSON.

### Governança e segurança de dados para agentes
- [Docs: Configure data security for Microsoft 365 Copilot (Purview + SharePoint Advanced Management)](https://learn.microsoft.com/en-us/copilot/microsoft-365/configure-data-security-copilot)
  Oversharing, restricted access control, revisões de acesso e DLP. Use para: o que uma KB em SharePoint precisa antes de virar fonte de agente.
- [Docs: Copilot Control System — security & governance](https://learn.microsoft.com/microsoft-365/copilot/copilot-control-system/security-governance)
  Visão geral dos controles e do licenciamento. Use para: conversar com segurança da informação.

## Wisdom (Communities)

- [Copilot Studio Community (fórum oficial Power Platform)](https://community.powerapps.com/t5/Copilot-Studio-Community/ct-p/PVACommunity)
  Fórum moderado com boards por tema. Use para: problemas práticos de Copilot Studio e MCP no Copilot Studio.
- [Amazon Quick Community (fórum oficial)](https://community.amazonquicksight.com/)
  Fórum ativo, onde a AWS também publica novidades. Use para: dúvidas de QuickSight, SPICE e datasets.
- [FinOps Foundation Community Slack](https://www.finops.org/community/community-slack/)
  Praticantes de FinOps, com discussão de custo de IA. Use para: unit economics, rateio e cultura de custo.
- Interno: o time estruturante e o time de finanças da nova área
  Use para: validar premissas de ROI e restrições reais da arquitetura (AWS/M365 do Itaú).

## Gaps
- Regulação e políticas internas para IA em banco (BACEN, LGPD, risco de modelo): buscar com as áreas de risco e compliance do Itaú, não em fontes públicas genéricas.
- Comunidade ativa e moderada focada em MCP: ainda não encontrei uma com boa reputação.
- Padrão bronze/prata/ouro: falta uma página oficial da AWS (só fontes secundárias até agora).
- Prontidão de dados para IA: falta uma fonte primária aberta (o relatório do Gartner é pago).
- Priorização de portfólio de IA (frameworks tipo RICE/WSJF aplicados a IA): faltam fontes primárias de alta confiança.
