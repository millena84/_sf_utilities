# Python para utilitários Salesforce

## Responsabilidade

Use Python para parsing XML/JSON, normalização, comparação, schemas, evidências, renderização e testes.

## Regras

- usar type hints;
- separar coleta, transformação, comparação e renderização;
- preservar fonte e timestamp;
- diferenciar nulo, vazio e ausente;
- não expor secrets;
- testar entradas válidas, inválidas e incompletas;
- retornar estruturas estruturadas.

## Integração

Python pode encapsular Salesforce CLI, Tooling API e bibliotecas de Robot Framework, mas as políticas de autorização e domínio permanecem explícitas.

## Fonte

- [Python XML ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)
