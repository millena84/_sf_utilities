# Salesforce Tooling API

## Visão geral

Oriente consultas técnicas sobre componentes, dependências, artefatos de desenvolvimento e informações não disponíveis no XML local.

## Regras de consulta

1. Identificar objeto.
2. Executar describe quando necessário.
3. Selecionar campos explicitamente.
4. Evitar `FIELDS(ALL)` quando houver incompatibilidade ou limite.
5. Definir limite e timeout.
6. Tratar paginação.
7. Registrar org, API version, timestamp e quantidade.
8. Operar em modo somente leitura.

## Fontes oficiais

- [Tooling API REST Resources](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/intro_rest_resources.htm)
- [Tooling API Objects](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/reference_objects_list.htm)
- [MetadataComponentDependency](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_metadatacomponentdependency.htm)
