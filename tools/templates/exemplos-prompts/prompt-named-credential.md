# Prompt — NamedCredential

Use o prompt-base para criar um utilitário de documentação de `NamedCredential`.

- Diretório: `namedCredentials/`; padrão: `*.namedCredential-meta.xml`.
- Extrair endpoint, label, descrição, tipo, principal, referências de External Credential, Auth Provider e opções de callout conforme a versão da API.
- Avaliar ExternalCredential, AuthProvider, Certificate, PermissionSet, Apex, Flow e External Services.
- Nunca persistir client secret, consumer secret, token, senha ou chave privada.
- Comparar endpoint, tipo, referências e parâmetros sem comparar valores secretos.
- Verificar diferenças entre Metadata API e Tooling API.

Fontes: [Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_namedcredential.htm), [Tooling API](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_namedcredential.htm), [Named Credentials Reference](https://developer.salesforce.com/docs/platform/named-credentials/references/named-credentials-reference).
