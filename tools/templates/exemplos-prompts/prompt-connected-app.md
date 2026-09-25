# Prompt — ConnectedApp

Use o prompt-base para criar um utilitário de documentação de `ConnectedApp`.

- Diretório: `connectedApps/`; padrão: `*.connectedApp-meta.xml`.
- Validar identidade pelo arquivo e pela representação recuperada.
- Extrair label, descrição, OAuth, scopes, callback URL, SAML e políticas quando disponíveis.
- Avaliar PermissionSet, AuthProvider, Certificate, Apex, Flow e integrações.
- Mascarar consumer key, consumer secret, tokens, certificados e credenciais.
- Não presumir `apiName` no XML.
- Separar configuração técnica de finalidade funcional.
- Usar XML, Metadata API, Tooling API se disponível, tabela interna e `sf data query`.
