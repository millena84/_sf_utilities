---
spec_id: evidence-contract
kind: contract
status: draft
version: "0.1.0"
last_updated: "YYYY-MM-DD"
---

# Contrato de evidências

## Objetivo

Defina como dados coletados por XML, tabela interna, Tooling API ou outras fontes serão registrados.

## Estrutura mínima

```json
{
  "source": "local_xml|internal_table|tooling_api",
  "project": "",
  "org_alias": null,
  "metadata_type": "",
  "component": "",
  "fields": {},
  "evidence": [],
  "collected_at": "",
  "warnings": []
}
```

## Regras

- toda informação deve ter fonte;
- registrar projeto e org quando aplicável;
- registrar timestamp;
- preservar caminho, objeto ou query;
- separar fato, inferência e recomendação;
- mascarar dados sensíveis;
- registrar lacunas.

## Critérios de aceitação

- [ ] schema válido;
- [ ] fonte identificada;
- [ ] dados sensíveis removidos;
- [ ] lacunas explícitas;
- [ ] evidências reproduzíveis quando possível.
