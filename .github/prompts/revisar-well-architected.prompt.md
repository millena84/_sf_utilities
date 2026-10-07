---
mode: agent
description: Avalia uma solução existente contra o AWS Well-Architected Framework e/ou o Salesforce Well-Architected Framework.
---

Você deve revisar a solução/arquitetura fornecida pelo usuário contra os frameworks de referência.

Passos:
1. Leia `.github/copilot/context.md` para contexto do projeto.
2. Identifique se a solução é AWS, Salesforce, ou híbrida.
3. Para componentes AWS, use os 6 pilares descritos em `.github/instructions/aws.instructions.md`.
4. Para componentes Salesforce, use os 3 princípios (Trusted/Easy/Adaptable) descritos em `.github/instructions/salesforce.instructions.md`.
5. Gere a saída no formato:

```
### Resumo da Solução Avaliada
### Avaliação por Pilar/Princípio (Forte / Atenção / Crítico)
### Top 5 Recomendações Priorizadas
### Riscos Não Mitigados
```
