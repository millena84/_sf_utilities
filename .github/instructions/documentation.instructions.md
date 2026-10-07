---
applyTo: "docs/**/*.md"
---

# Skill — Geração de Documentação Técnica

## Objetivo
Gerar documentação técnica clara, padronizada e reutilizável para soluções AWS e/ou Salesforce.

## Estrutura padrão (use sempre que gerar um novo documento)

```
# Título do Documento

## 1. Contexto
(Qual problema de negócio/técnico este documento resolve? Referencie .github/copilot/context.md)

## 2. Visão Geral da Solução
(Resumo em 3-5 linhas)

## 3. Arquitetura
(Diagrama em texto/Mermaid quando possível + descrição dos componentes)

## 4. Decisões Técnicas e Justificativas
(Lista de decisões-chave e por quê — formato ADR quando aplicável)

## 5. Segurança e Compliance
(Pontos relevantes de IAM/Profiles/Sharing/Criptografia)

## 6. Riscos e Mitigações

## 7. Glossário
(Termos específicos do projeto — puxar de .github/copilot/context.md)

## 8. Referências
```

## Regras de estilo
- Use Markdown idiomático (títulos, listas, tabelas) — nunca texto corrido longo.
- Prefira diagramas Mermaid (` ```mermaid `) a descrições textuais longas de arquitetura.
- Sempre que mencionar um serviço AWS ou recurso Salesforce, use o **nome oficial completo**.
- Mantenha cada seção curta (máx. ~150 palavras) — documentos modulares são mais fáceis de manter e revisar.
- Ao final, inclua uma seção "Perguntas em Aberto" se houver lacunas de informação — não invente dados ausentes.
