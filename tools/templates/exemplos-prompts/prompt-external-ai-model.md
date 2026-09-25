# Prompt — ExternalAIModel

Use o prompt-base para criar um utilitário de documentação de `ExternalAIModel`.

## Particularidades

- Identificar provedor, modelo, versão, endpoint, região, modalidade e status.
- Relacionar ExternalCredential, NamedCredential, AIApplication e GenAiPlugin.
- Nunca expor chaves, tokens, certificados, prompts privados ou dados enviados.
- Diferenciar modelo registrado de chamada efetivamente realizada.
- Avaliar residência de dados, retenção, custo, latência e controles de saída.
