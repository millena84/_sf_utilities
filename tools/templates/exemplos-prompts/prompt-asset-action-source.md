# Prompt — AssetActionSource

Use o prompt-base para criar um utilitário de documentação de `AssetActionSource`.

## Particularidades

- Identificar fonte, provedor, endpoint, autenticação, asset, status e versão.
- Relacionar AssetAction, ExternalCredential, NamedCredential e integrações.
- Nunca expor tokens, chaves, certificados ou endpoints privados.
- Diferenciar fonte configurada de origem efetivamente utilizada.
- Comparar alterações de provedor, autenticação, endpoint, mapeamento e status.
