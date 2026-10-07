---
applyTo: "analysis/**,adr/**"
---

# Skill — Análise Técnica e ADRs

## Objetivo
Produzir análises técnicas comparativas e Architecture Decision Records (ADRs) de alta qualidade para decisões envolvendo AWS e/ou Salesforce.

## Formato padrão de Análise Técnica

```
### Problema / Pergunta a Responder
### Contexto Atual (estado atual, restrições — puxar de .github/copilot/context.md)
### Opções Avaliadas
  - Opção A: descrição, prós, contras, custo/esforço
  - Opção B: descrição, prós, contras, custo/esforço
  - Opção C (se houver)
### Critérios de Decisão (ex.: custo, segurança, time-to-market, manutenibilidade)
### Recomendação e Justificativa
### Riscos da Recomendação e Mitigações
### Próximos Passos
```

## Formato padrão de ADR

```
# ADR-XXX: Título
## Status (Proposto/Aceito/Substituído)
## Contexto
## Decisão
## Consequências (positivas e negativas)
## Alternativas Consideradas
```

## Regras específicas
- Sempre avalie as opções contra os pilares relevantes do **AWS Well-Architected Framework** e/ou os princípios **Trusted/Easy/Adaptable** do Salesforce Well-Architected, conforme o escopo da decisão.
- Quando a decisão envolver integração AWS↔Salesforce, destaque explicitamente latência, acoplamento, resiliência e custo de cada opção.
- Seja honesto sobre incerteza — se faltar dado para decidir, declare isso na seção de Riscos em vez de assumir.
