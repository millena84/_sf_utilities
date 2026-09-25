# Snapshots, histórico e drift Salesforce

## Visão geral

Oriente captura, normalização, armazenamento e comparação de estados de projetos e organizações Salesforce.

## Snapshot mínimo

Registrar projeto, org, metadata type, componente, dados normalizados, timestamp, API version, fonte e hash ou representação comparável.

## Classificação

- criado;
- alterado;
- removido;
- inalterado;
- não comparável;
- primeira execução/baseline.

## Regras

- não chamar tudo de alterado na primeira execução;
- preservar estado antes de retrieve;
- registrar diff;
- tratar dados sensíveis;
- permitir rollback quando arquivos forem sobrescritos;
- separar estado local de estado atual da org.

## Fontes oficiais

- [Source Tracking](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_tracking.htm)
- [Retrieve Preview](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_retrieve_preview.html)
