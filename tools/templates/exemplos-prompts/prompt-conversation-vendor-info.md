# Prompt — ConversationVendorInfo

Use o prompt-base para criar um utilitário de documentação de `ConversationVendorInfo`.

## Particularidades

- Identificar fornecedor, canal, versão, endpoint, autenticação e status.
- Relacionar MessagingChannel, Conversation, ExternalCredential e integrações.
- Nunca expor tokens, chaves, certificados ou credenciais.
- Diferenciar configuração do fornecedor de conversa efetivamente processada.
- Comparar alterações de endpoint, versão, autenticação e disponibilidade.
