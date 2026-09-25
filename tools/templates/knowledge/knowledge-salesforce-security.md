# Segurança Salesforce

## Visão geral

Oriente proteção de credenciais, dados, integrações, permissões, APIs, logs e documentação.

## Nunca expor

- passwords;
- access tokens;
- refresh tokens;
- client secrets;
- consumer secrets;
- private keys;
- certificados privados;
- dados pessoais desnecessários.

## Regras

- least privilege;
- read-only por padrão;
- org e ambiente explícitos;
- aprovação para alteração;
- secrets mascarados também em logs e snapshots;
- registrar evidência sem registrar credencial.

## Fontes oficiais

- [Trust](https://architect.salesforce.com/docs/architect/well-architected/guide/trust.html)
- [Secure](https://architect.salesforce.com/docs/architect/well-architected/guide/secure)
- [Shared Responsibility](https://architect.salesforce.com/docs/architect/well-architected/guide/trust-shared-responsibility-patterns.html)
