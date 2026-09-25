# Prompt — TransactionSecurityPolicy

Use o prompt-base para criar um utilitário de documentação de `TransactionSecurityPolicy`.

## Particularidades

- Identificar evento, condição, ação, handler e status.
- Relacionar TransactionSecurityAction, ApexClass, usuários, sessões e eventos de segurança.
- Não expor critérios que facilitem evasão de controles.
- Diferenciar política configurada de transação efetivamente bloqueada.
- Avaliar falsos positivos, cobertura e impacto operacional.
