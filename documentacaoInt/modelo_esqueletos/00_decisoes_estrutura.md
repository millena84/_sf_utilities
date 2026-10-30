# Decisões de estrutura da documentação (para a refatoração dos prompts)

> Registro das decisões tomadas com a revisora a partir dos esqueletos 01 e 02.

| # | Data | Decisão |
|---|---|---|
| 1 | 2026-10-30 | Dois documentos: **sigla** (01, "o que existe") e **integração** (02, "como funciona"). Estrutura e granularidade dos esqueletos aprovadas como 1ª versão. |
| 2 | 2026-10-30 | Marcação obrigatória nas configurações de integração: `!!!SUCCESS` (é usado, com o motivo) e `!!!ABSTRACT` (não é usado, com a explicação técnica do porquê). Substitui "não identificado na base analisada". |
| 3 | 2026-10-30 | As configurações de integração (Connected App/External Client App, Certificado, Remote Site, Endpoints, Named Credential, External Credential) aparecem **nos dois documentos, completas, com a mesma marcação SUCCESS/ABSTRACT**. No documento da sigla, pode haver link para o documento da integração com a explicação detalhada. A duplicidade é intencional (intervenção operacional) e as duas versões devem vir da mesma fonte de dados, para não divergirem. |
| 4 | 2026-10-30 | Documento da sigla mais enxuto: mantém cabeçalho, índice, resumo executivo e cadeia (Caminho → Entrada → Saída + Mermaid), modelo de dados (objeto e papel), configurações por integração, acesso (usuário de integração, Profiles, Permission Sets), componentes compartilhados entre integrações (impacto), pontos de validação e anexo de fontes. Os catálogos completos de Flows, Apex, Triggers e LWC passam para os documentos das integrações. |
| 5 | 2026-10-30 | Sintaxe dos blocos: reproduzir exatamente a dos esqueletos e do documento FNN (`!!!SUCCESS`/`!!!ABSTRACT`/`!!!DANGER` na primeira linha, conteúdo nas linhas seguintes com o mesmo recuo). Verificação compara a sintaxe gerada com a do modelo. |
| 6 | 2026-10-30 | Terceira marcação `!!!DANGER`: o repositório **não permite confirmar** se o componente é usado. Conteúdo: o que foi encontrado, por que não dá para confirmar e o que verificar na org. |
| 7 | 2026-10-30 | Seção 7.1 ("validações que exigem estado vivo da org") mantida. Todo `!!!DANGER` entra automaticamente nela como item a verificar. |
| 8 | 2026-10-30 | Esqueletos refinados (v2) aplicando as decisões 1–7. **01 (sigla):** 1 Resumo e cadeia · 2 Modelo de dados · 3 Configurações por integração · 4 Acesso · 5 Componentes compartilhados · 6 Escopo e pontos de validação (6.1 recebe os DANGER) · Anexo A. **02 (integração):** seções 0–5 como enviadas + 6 Componentes técnicos (catálogos que saíram da sigla) · 7 Configurações de integração · 8 Integrações relacionadas · Anexo A. A seção "7.1" da decisão 7 passou a ser a 6.1 do esqueleto 01. |
