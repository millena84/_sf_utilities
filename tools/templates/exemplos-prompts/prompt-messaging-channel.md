# Prompt — MessagingChannel

Use o prompt-base para criar um utilitário de documentação de `MessagingChannel`.

## Particularidades

- Identificar canal, tipo, provedor, endereço, status, filas e roteamento.
- Relacionar ConversationVendorInfo, ServiceChannel, Queue, Flow e EmbeddedServiceConfig.
- Não expor números, endereços de mensageria, tokens ou URLs privadas.
- Diferenciar canal configurado de conversa ou mensagem efetivamente enviada.
- Comparar alterações de provedor, status, filas e políticas.
