# Salesforce CLI

## Visão geral

Oriente comandos `sf`, prechecks, aliases, retrieve, query, describe, formatos de saída, códigos de retorno e execução segura.

## Comandos relevantes

- `sf org display`;
- `sf data query`;
- `sf sobject describe`;
- `sf project retrieve start`;
- `sf project retrieve preview`.

## Regras

- validar instalação e autenticação separadamente;
- identificar org-alvo;
- registrar comando lógico sem expor credenciais;
- preservar exit codes;
- preferir JSON para integração com Python;
- executar preview quando aplicável;
- não realizar deploy em utilitário documental.

## Fontes oficiais

- [Salesforce CLI Reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference)
- [Project Retrieve Start](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_retrieve_start.html)
- [Project Retrieve Preview](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_retrieve_preview.html)
