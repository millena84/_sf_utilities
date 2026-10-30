# Fase 0 — Preencher atributos e estado do inventário

No `fase0/inventory.csv`, a coluna `atributos` está vazia. Implemente no script da etapa 0.2 a extração dos atributos conforme o prompt da Fase 0 e preencha a coluna, **sem alterar IDs nem as demais colunas**:

- **Flow:** `processType`, `triggerType`, `recordTriggerType`, objeto do `<start>`, antes/depois de salvar, se tem `screens`;
- **ApexTrigger:** objeto e eventos;
- **ApexClass:** anotações (`@RestResource`, `@HttpGet/Post/…`, `webservice`, `@AuraEnabled`, `@InvocableMethod`, `@future`) e interfaces (`Queueable`, `Database.Batchable`, `Schedulable`, `Database.AllowsCallouts`);
- **LWC/Aura:** `targets` e métodos Apex importados (`@salesforce/apex/...`);
- **FlexiPage:** objeto e componentes incluídos;
- **registro de CustomMetadata:** tipo `__mdt`, campos não sensíveis e se o nome indica ambiente.

Preencha também a coluna `estado`, se estiver vazia. Formato: pares `chave=valor` separados por `;`.

Depois mostre, para cada um desses tipos, quantas linhas ficaram com atributos preenchidos e 3 exemplos. Rode o `validate_fase0.py` de novo (incluindo a F0-A21) e registre em `decisions.md`.
