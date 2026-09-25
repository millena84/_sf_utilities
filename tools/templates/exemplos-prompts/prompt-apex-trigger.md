# Prompt — ApexTrigger

## 1. Contexto do componente

### 1.1 O que é
`ApexTrigger` (nome funcional: **Apex Trigger** ou **Gatilho Apex**) é um metadata type do Salesforce que define código Apex executado automaticamente em resposta a eventos de DML (`before insert`, `after insert`, `before update`, `after update`, `before delete`, `after delete`, `after undelete`) em registros de um objeto específico ou de todos os objetos (custom object, standard object, Platform Event, Big Object etc.).

Na prática, um `ApexTrigger`:
- é definido em `triggers/<API_Name>.trigger` com metadata `triggers/<API_Name>.trigger-meta.xml`;
- é executado no contexto de uma transação DML;
- pode operar em modo bulk;
- deve seguir rigorosamente as regras de governança do Salesforce (SOQL, DML, heap, CPU time);
- pode disparar automações adicionais como Flow, Process Builder, regras de workflow.

### 1.2 Para que serve
- Validar e transformar dados antes/depois de operações DML.
- Implementar automações complexas que não são possíveis via declarativo.
- Sincronizar dados entre objetos.
- Reagir a eventos de plataforma.
- Aplicar regras de negócio avançadas com controle total de bulkification.

### 1.3 Cenários típicos de uso
- Atualizar campos derivados antes do insert/update.
- Criar registros relacionados após insert.
- Enviar chamadas assíncronas para integrações externas.
- Implementar restrições de segurança customizadas.
- Processar eventos de plataforma (`__e`).

### 1.4 Clouds / contextos
- **Salesforce Core** — automações de dados e negócio.
- **Experience Cloud** — executado em contexto de comunidade conforme usuário.
- **Data Cloud / Industries / Health Cloud** — extensões específicas por cloud.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ApexTrigger`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Trigger / Apex Trigger |
| Metadata type exact | `ApexTrigger` |
| Pasta no projeto SFDX | `triggers/` |
| Arquivo padrão | `<apiName>.trigger` + `<apiName>.trigger-meta.xml` |
| Objeto interno (API padrão) | `ApexTrigger` |
| Objeto interno (Tooling API) | `ApexTrigger` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ApexTrigger` |
| Acessível por Tooling API | Sim — inclui `EntityDefinition`, `UsageBeforeInsert` etc. |
| Acessível por Apex | Sim — `ApexTrigger` é consultável |
| Acessível por UI | Sim — **Setup → Apex Triggers** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Objeto associado | `EntityDefinition` / `TableEnumOrId` | Objeto/evento que dispara o trigger. |
| Apex Class helper | `ApexClass` | Classes de handler/framework usadas. |
| Flow / Process Builder | `Flow` | Pode coexistir/sobrepor automações. |
| Validation Rule | `ValidationRule` | Pode ser acionada pelo trigger. |
| Duplicate Rule | `DuplicateRule` | Pode ser acionada pelo trigger. |
| Custom Metadata / Settings | `CustomMetadata`, `CustomSetting` | Configurações do trigger. |
| Platform Event | `PlatformEventDefinition` | Triggers de evento (`__e`). |
| Async Apex | `Queueable`, `Batchable`, `Schedulable` | Pode delegar processamento. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | ApexTrigger metadata | Objeto SOQL | Tooling | Setup/UI |
|---|---|---|---|---|
| Nome / API name | Sim | `Name` | Sim | Sim |
| Objeto/evento | — | `TableEnumOrId` | Sim (`EntityDefinition.Id`) | Sim |
| Eventos DML | código (before/after insert/update/delete/undelete) | `UsageBeforeInsert`, `UsageAfterInsert`, etc. | Sim | Sim |
| Status | metadata | `Status` | Sim | Sim |
| Versão API | `.trigger-meta.xml` | `ApiVersion` | Sim | Sim |
| Código fonte | `.trigger` | `Body` (Tooling) | Sim | — |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ApexTrigger`)

Arquivo típico: `triggers/<API_Name>.trigger` + `triggers/<API_Name>.trigger-meta.xml`.

#### Tags do `.trigger-meta.xml`

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<apiVersion>` | 1 | Versão da API. |
| `<status>` | 1 | `Active` ou `Inactive`. |

#### Exemplo de trigger

```apex
trigger MinhaTrigger on Account (before insert, before update, after insert) {
    if (Trigger.isBefore && Trigger.isInsert) {
        MinhaTriggerHandler.onBeforeInsert(Trigger.new);
    }
    if (Trigger.isBefore && Trigger.isUpdate) {
        MinhaTriggerHandler.onBeforeUpdate(Trigger.new, Trigger.oldMap);
    }
    if (Trigger.isAfter && Trigger.isInsert) {
        MinhaTriggerHandler.onAfterInsert(Trigger.new);
    }
}
```

### 3.2 Objeto interno via API padrão: `ApexTrigger`

| Campo | Significado prático |
|---|---|
| `Id` | ID do trigger. |
| `Name` | Nome/API Name. |
| `TableEnumOrId` | API Name ou ID do objeto/evento associado. |
| `Status` | `Active` / `Inactive`. |
| `ApiVersion` | Versão da API. |
| `UsageBeforeInsert`, `UsageAfterInsert`, `UsageBeforeUpdate`, `UsageAfterUpdate`, `UsageBeforeDelete`, `UsageAfterDelete`, `UsageAfterUndelete` | Booleanos indicando eventos ativos. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, Name, TableEnumOrId, Status, ApiVersion,
       UsageBeforeInsert, UsageAfterInsert,
       UsageBeforeUpdate, UsageAfterUpdate,
       UsageBeforeDelete, UsageAfterDelete,
       UsageAfterUndelete
FROM ApexTrigger
ORDER BY TableEnumOrId, Name
```

### 3.3 Tooling API — código e metadados adicionais

```sql
SELECT Id, Name, Body, TableEnumOrId, Status, ApiVersion,
       UsageBeforeInsert, UsageAfterInsert
FROM ApexTrigger
ORDER BY Name
```

### 3.4 Triggers de Platform Event

```sql
SELECT Id, Name, TableEnumOrId, Status
FROM ApexTrigger
WHERE TableEnumOrId LIKE '%__e'
ORDER BY TableEnumOrId, Name
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Apex Triggers.
- Source code do repositório SFDX.
- `SetupAuditTrail`.
- Debug logs.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Código fonte | `.trigger` / Tooling `Body` | `ApexTrigger` SOQL padrão | Requer Tooling. |
| Lógica de handler | `ApexClass` (handler) | Trigger | Requer análise da classe. |
| Execuções atuais | Debug logs | Metadata | Estado de runtime. |
| Ordem de execução | Ordem de triggers + Save Order | Trigger individual | Requer análise global. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `EntityDefinition`

- Descreve o objeto associado ao trigger.
- Para eventos, `TableEnumOrId` termina com `__e`.

### 4.2 `ApexClass`

- Classes handler, helpers, services invocados pelo trigger.

### 4.3 `Flow`

- Automations declarativas que podem ser disparadas pelo mesmo objeto.

### 4.4 `AsyncApexJob`

- Jobs assíncronos originados pelo trigger.

### 4.5 `SetupAuditTrail`

- Rastreia ativação/desativação e alterações.

---

## 5. Consultas e formas de extração

### 5.1 Triggers por objeto

```sql
SELECT Id, Name, TableEnumOrId, Status, ApiVersion,
       UsageBeforeInsert, UsageAfterInsert,
       UsageBeforeUpdate, UsageAfterUpdate,
       UsageBeforeDelete, UsageAfterDelete,
       UsageAfterUndelete
FROM ApexTrigger
ORDER BY TableEnumOrId, Name
```

### 5.2 Triggers ativos com mais de um evento

```sql
SELECT Id, Name, TableEnumOrId,
       UsageBeforeInsert, UsageAfterInsert,
       UsageBeforeUpdate, UsageAfterUpdate,
       UsageBeforeDelete, UsageAfterDelete,
       UsageAfterUndelete
FROM ApexTrigger
WHERE Status = 'Active'
ORDER BY TableEnumOrId, Name
```

### 5.3 Triggers de platform event

```sql
SELECT Id, Name, TableEnumOrId, Status, ApiVersion
FROM ApexTrigger
WHERE TableEnumOrId LIKE '%__e'
ORDER BY TableEnumOrId, Name
```

### 5.4 Classes handler relacionadas

```sql
SELECT Id, Name, ApiVersion, Status
FROM ApexClass
WHERE Name LIKE '%Handler'
   OR Name LIKE '%TriggerHelper'
ORDER BY Name
```

---

## 6. Boas práticas e pontos de atenção

- **Sempre projete triggers bulk-safe**: operações em listas, não em registros individuais.
- **Use framework de handler**: delegue lógica para classes auxiliares.
- **Evite SOQL/DML dentro de loops**: respeite limites de governança.
- **Controle recursividade**: use static boolean flags ou frameworks especializados.
- **Mantenha triggers finos**: apenas dispatch de eventos para handlers.
- **Documente eventos e objetos** associados no nome/nome da trigger.
- **Teste exaustivamente** com dados em volume.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Combine com Flow/Process Builder com cuidado** para evitar duplicação e loops.
- **Prefira `before` para validação/transformação** e `after` para ações dependentes de ID.

---

## 7. Links de referência oficial

- [Salesforce Developer — Triggers](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_triggers.htm)
- [Salesforce Developer — ApexTrigger Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_apextrigger.htm)
- [Salesforce Developer — Apex Trigger Best Practices](https://developer.salesforce.com/wiki/Apex_Code_Best_Practices)
- [Salesforce Developer — Trigger Context Variables](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_trigger_context_variables.htm)
