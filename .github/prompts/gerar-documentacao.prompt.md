---
mode: agent
description: Gera um documento técnico estruturado (AWS e/ou Salesforce) seguindo o padrão do repositório.
---

Você deve gerar um documento técnico completo seguindo exatamente a estrutura definida em `.github/instructions/documentation.instructions.md`.

Antes de começar:
1. Leia `.github/copilot/context.md` para entender o contexto do projeto.
2. Pergunte ao usuário, se necessário, qual é o **tema/escopo** do documento (ex.: arquitetura de integração, runbook operacional, guia de segurança).
3. Identifique se o tema é predominantemente AWS, Salesforce, ou ambos, e aplique os módulos correspondentes (`aws.instructions.md` e/ou `salesforce.instructions.md`).

Gere o documento completo em Markdown, pronto para ser salvo em `docs/`.
