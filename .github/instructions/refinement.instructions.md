---
applyTo: "backlog/**,refinement/**"
---

# Skill — Refinamento de Backlog (Histórias, Épicos, Requisitos)

## Objetivo
Apoiar o refinamento de itens de backlog relacionados a AWS e/ou Salesforce, garantindo clareza, testabilidade e viabilidade técnica.

## Checklist INVEST
Ao refinar uma história, valide:
- **I**ndependente
- **N**egociável
- **V**aliosa (valor de negócio claro)
- **E**stimável
- **S**mall (pequena o suficiente para uma sprint)
- **T**estável (critérios de aceite claros)

## Formato padrão de saída

```
### Título Refinado
### Como [persona], eu quero [ação], para que [benefício]
### Critérios de Aceite (Gherkin: Dado/Quando/Então)
### Dependências Técnicas (AWS/Salesforce)
### Riscos/Suposições
### Definition of Ready — Checklist
### Estimativa Sugerida (T-shirt size ou pontos, com justificativa)
```

## Regras específicas
- Se a história envolver Salesforce, identifique se a solução é declarativa ou requer código (Apex/LWC) e sinalize impacto em governor limits.
- Se a história envolver AWS, identifique serviços envolvidos e pilar(es) do Well-Architected mais impactado(s).
- Sempre sinalize se faltam informações de negócio antes de gerar critérios de aceite definitivos — pergunte em vez de assumir.
