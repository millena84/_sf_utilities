---
knowledge_id: salesforce-integrations
title: Salesforce Integrations
status: draft
version: "1.0.0"
last_reviewed: "YYYY-MM-DD"
language: pt-BR
---

# Salesforce Integrations

## Visão geral

Oriente a análise e a construção de integrações Salesforce considerando sistemas, APIs, eventos, autenticação, autorização, contrato de dados, volume, limites, retries, idempotência, observabilidade, segurança e governança.

## Fontes

- XML Salesforce;
- tabela interna padronizada do componente;
- Tooling API;
- Salesforce CLI e `sf data query`;
- código, documentação e contexto aprovado.

## Mecanismos

Considere REST, SOAP, Bulk API 2.0, Metadata API, Tooling API, Pub/Sub API, Platform Events, Change Data Capture, Outbound Messages, Apex callouts, Flow HTTP Callout e middleware.

## Regras

- distinguir síncrono, assíncrono, batch e event-driven;
- documentar origem, destino e direção;
- identificar contrato, transformação e chaves;
- analisar retry e idempotência;
- registrar timeout, limites e observabilidade;
- não atribuir ao Salesforce regra executada no middleware;
- escolher API conforme o caso de uso;
- não expor secrets.

## Configuração Salesforce

Avaliar, quando aplicável: Connected Apps, Named Credentials, External Credentials, Auth Providers, Certificates, Remote Site Settings, Flow, Apex, Platform Events, Change Data Capture e Permission Sets.

## Fontes oficiais

- [Salesforce API Library](https://developer.salesforce.com/docs/apis)
- [Which API Do I Use?](https://help.salesforce.com/s/articleView?id=platform.integrate_what_is_api.htm&language=en_US&type=5)
- [Tooling API REST Resources](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/intro_rest_resources.htm)
- [Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/metadata.htm)
- [Well-Architected](https://architect.salesforce.com/docs/architect/well-architected/guide/framework.html)

## Atualização

Revisar após releases, mudanças de API, alterações de limites, mudanças de produto ou incompatibilidades encontradas nos utilitários.
