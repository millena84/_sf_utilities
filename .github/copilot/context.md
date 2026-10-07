# Contexto do Projeto (Personalização)

> **Preencha este arquivo com os dados reais do projeto/cliente/org.**
> Ele é lido por todos os módulos de skill antes de gerar qualquer artefato (documentação, refinamento, análise).
> Mantenha-o **curto, objetivo e em tópicos** — isso é o que garante respostas rápidas e precisas. Evite parágrafos longos; prefira listas e tabelas.

## 1. Identificação
- **Nome do projeto/cliente:** _(ex.: Projeto Átlas — Migração CRM)_
- **Domínio de negócio:** _(ex.: Varejo, Saúde, Financeiro, Setor Público)_
- **Stakeholders principais:** _(ex.: Product Owner, Arquiteto Líder, Head de TI)_

## 2. Escopo Técnico
- **Clouds Salesforce em uso:** _(ex.: Sales Cloud, Service Cloud, Experience Cloud)_
- **Serviços AWS em uso:** _(ex.: Lambda, S3, API Gateway, EventBridge)_
- **Tipo de integração entre AWS e Salesforce:** _(ex.: Platform Events → EventBridge, REST API via Named Credentials, MuleSoft)_
- **Ambientes:** _(ex.: Dev Sandbox, UAT, Produção / Contas AWS: dev, stg, prod)_

## 3. Restrições e Políticas
- **Requisitos de segurança/compliance:** _(ex.: LGPD, HIPAA, PCI-DSS, Shield Platform Encryption obrigatório)_
- **Orçamento/custo:** _(ex.: teto mensal AWS, licenciamento Salesforce)_
- **SLAs/RTO/RPO:** _(ex.: RTO 4h, RPO 1h)_

## 4. Padrões e Convenções do Time
- **Framework de Apex:** _(ex.: Trigger Handler Framework próprio, fflib, Nebula Logger)_
- **IaC usada na AWS:** _(ex.: Terraform, CDK, CloudFormation)_
- **Padrão de nomenclatura:** _(ex.: prefixos de classes Apex, tags obrigatórias em recursos AWS)_
- **Ferramentas de gestão:** _(ex.: Jira, Azure DevOps, Copado, Gearset)_

## 5. Glossário Específico
- _(Liste siglas e termos internos do projeto que o Copilot deve reconhecer, ex.: "OPCO" = Unidade Operacional)_

---

### Como descrever bem este contexto (orientação)
- **Seja específico, não genérico**: "Service Cloud com Omni-Channel e Field Service" é melhor que "Salesforce".
- **Use nomes oficiais de serviços/recursos** (AWS e Salesforce) para que o Copilot aplique o módulo técnico correto.
- **Atualize este arquivo a cada mudança relevante de escopo** — ele é a fonte única de verdade de contexto para todas as skills.
- **Não duplique conteúdo técnico genérico aqui** (isso já está nos módulos `aws.instructions.md` / `salesforce.instructions.md`). Este arquivo é só o que é **específico deste projeto**.
