# sf data query e tabelas internas

## Visão geral

Oriente consultas SOQL em tabelas internas padronizadas usadas pelos utilitários para mapear componentes, campos, escopo e ordem da documentação.

## Procedimento

- identificar alias da org;
- confirmar objeto;
- executar describe quando necessário;
- usar campos explícitos;
- evitar `FIELDS(ALL)` quando incompatível;
- controlar limite e paginação;
- registrar query ou hash;
- mascarar dados sensíveis;
- não executar DML.

## Resultado mínimo

```json
{
  "source": "internal_table",
  "org_alias": "",
  "object": "",
  "query_hash": "",
  "records_count": 0,
  "records": [],
  "collected_at": ""
}
```

## Fontes oficiais

- [Salesforce CLI Reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference)
- [API Library](https://developer.salesforce.com/docs/apis)
