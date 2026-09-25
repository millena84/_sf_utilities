# Salesforce DX e projetos locais

## Visão geral

Oriente a validação de projetos DX, `sfdx-project.json`, `packageDirectories`, source format, metadata format, manifests e diretórios de metadata.

## Regras

- validar `sfdx-project.json`;
- consultar `packageDirectories`;
- não assumir `force-app/main/default`;
- diferenciar source format e metadata format;
- registrar projeto e versão da API.

## Retrieve

Validar projeto e org, executar preview quando aplicável, preservar estado anterior, recuperar metadata, registrar diff e validar o resultado.

## Fontes oficiais

- [Project Setup](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_workspace_setup.htm)
- [Source Format](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_file_format.htm)
- [Retrieve](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_retrieve_start.html)
- [Retrieve Preview](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_retrieve_preview.html)
