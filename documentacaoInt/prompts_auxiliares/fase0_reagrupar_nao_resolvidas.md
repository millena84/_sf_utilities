# Fase 0 — Reagrupar referências não resolvidas

Exclua da contagem e do arquivo as referências cuja origem seja uma classe de teste (`is_test = true`).

Reestruture `fase0/unresolved_refs.csv` agregando por nome referenciado:
`referencia_textual,categoria(nativo|customizado|desconhecido),qtd_ocorrencias,qtd_componentes_origem,exemplos_origem(até 3),id_regra,motivo_provavel`

- Considere `nativo`: tipos e namespaces do Apex (`String`, `List`, `Map`, `Set`, `System`, `Database`, `Schema`, `Test`, `Http`, `HttpRequest`, `HttpResponse`, exceções padrão `*Exception`…) e objetos/campos padrão do Salesforce.
- Recalcule a F0-A10 e a F0-A10b sobre os nomes **distintos** da categoria `customizado` (resolvidos ÷ total de customizados distintos) e mostre os números antes e depois.
- Liste os 20 nomes `customizado` não resolvidos mais frequentes, dizendo se existe no inventário um componente com nome parecido.

Atualize o `validation_report.md` e registre em `decisions.md`.
