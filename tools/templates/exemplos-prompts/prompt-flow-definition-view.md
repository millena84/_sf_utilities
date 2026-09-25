# Prompt — FlowDefinitionView

## 1. Contexto do componente

### 1.1 O que é
`FlowDefinitionView` (nome funcional: **Flow Definition View**) é uma entidade de leitura do Salesforce que representa os metadados consolidados de uma definição de Flow (automação declarativa). Ele expõe informações como nome da API, rótulo, versão ativa, versão mais recente, tipo de trigger, status e outras propriedades de uma automação `Flow`.

Na prática, `FlowDefinitionView`:
- é uma visão somente leitura de uma definição de Flow;
- permite identificar rapidamente qual versão está ativa e qual é a mais recente;
- ajuda a auditar automações sem precisar analisar o conteúdo completo de cada versão em `Flow` (`FlowVersionView`);
- trabalha em conjunto com `FlowVersionView` para obter detalhes de cada versão específica.

### 1.2 Para que serve
- Mapear todas as automações de Flow de uma org.
- Identificar versões ativas versus versões em rascunho.
- Auditar o tipo de trigger (record-triggered, schedule-triggered, autolaunched, platform event, screen etc.).
- Facilitar governança e comparativos entre ambientes.
- Sinalizar diferenças entre versão ativa e mais recente (null/empty).

### 1.3 Cenários típicos de uso
- Inventariar todos os Flows de uma org e seu status.
- Detectar Flows que possuem versão mais recente sem ativação.
- Relacionar Flows a objetos (record-triggered flows).
- Auditar automações antes de um deploy ou migração.
- Comparar metadados de Flow entre produção e sandbox.

### 1.4 Clouds / contextos
- **Salesforce Core** — Automações declarativas.
- **Experience Cloud** — Screen flows em comunidades.
- **Service Cloud / Sales Cloud** — Record-triggered e autolaunched flows.
- **Field Service / Industries** — Flows especializados por cloud.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `FlowDefinitionView`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Flow / Definição de Fluxo |
| Metadata type exact | `Flow` (definição) |
| Pasta no projeto SFDX | `flows/` |
| Arquivo padrão | `<apiName>.flow-meta.xml` |
| Objeto interno (API padrão) | `FlowDefinitionView` (somente leitura) |
| Objeto interno (Tooling API) | `FlowDefinitionView` |
| Acessível por Metadata API | Sim — `retrieve/deploy` do arquivo `.flow-meta.xml` |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM FlowDefinitionView` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Não diretamente — use SOQL dinâmico |
| Acessível por UI | Sim — **Setup → Flows** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Flow Version | `FlowVersionView` | Detalha cada versão individual. |
| Flow Definition | `FlowDefinition` (Tooling) | Representa a definição do Flow. |
| Flow (Metadata) | `Flow` | Arquivo `.flow-meta.xml` com toda a lógica. |
| Process Builder (legacy) | `Flow` (`<processType>Workflow</processType>`) | Automações legadas migradas. |
| Apex | `ApexClass`, `ApexTrigger` | Pode ser invocado/usado por Flows. |
| Custom Metadata/Settings | `CustomMetadata`, `CustomSetting` | Podem ser referenciados. |
| Objects / Fields | `EntityDefinition`, `FieldDefinition` | Trigger objects e campos. |
| Email Alert | `WorkflowAlert` | Pode ser acionado por Flow. |
| Approval Process | `ApprovalProcess` | Pode ser submetido por Flow. |
| Subflow | Outro `Flow` | Flow chamado internamente. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | FlowDefinitionView | Flow metadata | Tooling | Setup/UI |
|---|---|---|---|---|
| API Name / Label | `ApiName`, `Label` | `<apiName>`, `<label>` | Sim | Sim |
| Versão ativa | `ActiveVersionId` | — | `FlowDefinition.ActiveVersionId` | Sim |
| Versão mais recente | `LatestVersionId` | — | `FlowDefinition.LatestVersionId` | Sim |
| Status da definição | `Status` (`Active`, `Obsolete`, `Draft`) | — | `FlowDefinition.Status` | Sim |
| Tipo de trigger | `TriggerType` | `<start>` / `<triggerType>` | `FlowDefinitionView.TriggerType` | Sim |
| Objeto trigger | `TriggerObjectOrEventId` | `<object>` | `Flow.VersionView.TriggerObjectOrEvent` | Sim |
| Namespace | `NamespacePrefix` | `namespacePrefix` | Sim | Sim |
| Criador/modificador | `CreatedById`, `LastModifiedById` | — | Sim | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`Flow`)

Arquivo típico: `flows/<API_Name>.flow-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<apiVersion>` | 1 | Versão da API usada pelo Flow. |
| `<description>` | 0..1 | Descrição. |
| `<environments>` | 0..1 | Ambientes (Default, Mobile etc.). |
| `<interviewLabel>` | 0..1 | Rótulo da entrevista/execução. |
| `<isTemplate>` | 0..1 | Indica se é template. |
| `<label>` | 1 | Nome amigável. |
| `<processMetadataValues>` | 0..N | Valores de metadados do processo. |
| `<processType>` | 1 | Tipo do flow: `AutoLaunchedFlow`, `Flow`, `Workflow`, `CustomEvent`, `InvocableProcess`, `Orchestrator` etc. |
| `<start>` | 0..1 | Elemento inicial com trigger. |
| `<status>` | 1 | `Active`, `Draft`, `Obsolete`. |
| `<variables>` | 0..N | Variáveis do Flow. |
| `<constants>` | 0..N | Constantes. |
| `<formulas>` | 0..N | Fórmulas. |
| `<choices>` | 0..N | Escolhas de Screen Flow. |
| `<screens>`, `<decisions>`, `<assignments>` ... | 0..N | Elementos do Flow. |

#### Tipos de processo/trigger comuns

| Tipo | Significado |
|---|---|
| `AutoLaunchedFlow` | Sem interface, invocado por Apex/Flow/Processo. |
| `Flow` | Screen flow (com UI). |
| `Workflow` | Process Builder legado. |
| `CustomEvent` | Triggered por Platform Event. |
| `InvocableProcess` | Processo invocável. |
| `Orchestrator` | Flow orquestrador. |
| `TransactionSecurityFlow` | Fluxo de segurança de transação. |

### 3.2 Objeto interno via API padrão: `FlowDefinitionView`

| Campo | Significado prático |
|---|---|
| `Id` | ID da definição. |
| `ApiName` | API Name do Flow. |
| `Label` | Nome amigável. |
| `Description` | Descrição. |
| `NamespacePrefix` | Namespace. |
| `ActiveVersionId` | ID da versão ativa (pode ser null). |
| `LatestVersionId` | ID da versão mais recente. |
| `Status` | Status da definição (`Active`, `Draft`, `Obsolete`). |
| `TriggerType` | Tipo de trigger. |
| `TriggerObjectOrEventId` | Objeto ou evento que dispara o flow. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |
| `CreatedById`, `LastModifiedById` | Autores. |

#### Exemplo de query

```sql
SELECT Id, ApiName, Label, Description, NamespacePrefix,
       ActiveVersionId, LatestVersionId, Status,
       TriggerType, TriggerObjectOrEventId,
       CreatedById, CreatedBy.Name, LastModifiedById, LastModifiedBy.Name,
       CreatedDate, LastModifiedDate
FROM FlowDefinitionView
ORDER BY Label
```

### 3.3 Tabelas internas de versões

#### `FlowVersionView`

| Campo | Significado prático |
|---|---|
| `Id` | ID da versão. |
| `FlowDefinitionViewId` | Definição pai. |
| `VersionNumber` | Número da versão. |
| `Status` | `Active`, `Draft`, `Obsolete`. |
| `ApiVersion` | Versão da API. |
| `Label` | Rótulo da versão. |
| `Description` | Descrição. |
| `TriggerType` | Tipo de trigger. |
| `LastModifiedDate` | Última modificação. |

```sql
SELECT Id, FlowDefinitionViewId, FlowDefinitionView.ApiName,
       VersionNumber, Status, ApiVersion, Label, Description,
       TriggerType, LastModifiedDate
FROM FlowVersionView
ORDER BY FlowDefinitionView.ApiName, VersionNumber DESC
```

### 3.4 Elementos do Flow

Para mapear elementos específicos como Apex calls, subflows, DML etc., é necessário inspecionar o XML do arquivo `.flow-meta.xml` ou fazer parser do campo `Metadata` em Tooling API.

Exemplo de busca por subflows em metadata:

```bash
grep -r "<subflow>" force-app/main/default/flows/*.flow-meta.xml
```

---

### 3.5 Configuração observável em outras fontes

- Setup → Flows.
- Setup → Flow Version History.
- Setup → Process Automation Settings.
- Change Sets / Deployments de metadados `Flow`.
- `SetupAuditTrail`.
- `FlowInterview` (instâncias de execução ativas/pausadas).

---

### 3.6 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Lógica completa do Flow | `.flow-meta.xml` / `Metadata` | `FlowDefinitionView` | Visão é resumida. |
| Elementos individuais | `.flow-meta.xml` | `FlowDefinitionView` | Use `FlowVersionView` + parser. |
| Execuções ativas | `FlowInterview`, `FlowStageRelation` | `FlowDefinitionView` | Estado de runtime. |
| Erros de execução | `FlowInterview`, debug logs | `FlowDefinitionView` | Requer logs. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `FlowVersionView`

- Detalha cada versão de uma definição de Flow.

### 4.2 `FlowInterview`

- Representa uma execução ativa ou pausada de Screen Flow.

### 4.3 `ApexClass` / `ApexTrigger`

- Flows podem invocar classes invocáveis (`@InvocableMethod`) e triggers;
- Apex pode iniciar flows via `System.Flow.Interview`.

### 4.4 `WorkflowRule` / `Process Builder`

- Processos legados são representados como Flows do tipo `Workflow`.

### 4.5 `CustomMetadata` / `CustomSetting`

- Podem ser referenciados por Flows para parametrização.

---

## 5. Consultas e formas de extração

### 5.1 Todas as definições de Flow

```sql
SELECT Id, ApiName, Label, Description, NamespacePrefix,
       ActiveVersionId, LatestVersionId, Status,
       TriggerType, TriggerObjectOrEventId,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM FlowDefinitionView
ORDER BY Label
```

### 5.2 Versões de um flow específico

```sql
SELECT Id, FlowDefinitionViewId, FlowDefinitionView.ApiName,
       VersionNumber, Status, ApiVersion, Label, Description,
       TriggerType, LastModifiedDate
FROM FlowVersionView
WHERE FlowDefinitionView.ApiName = 'Meu_Flow'
ORDER BY VersionNumber DESC
```

### 5.3 Flows ativos com versão mais recente diferente da ativa

```sql
SELECT Id, ApiName, Label, ActiveVersionId, LatestVersionId
FROM FlowDefinitionView
WHERE ActiveVersionId != null
  AND LatestVersionId != ActiveVersionId
ORDER BY Label
```

### 5.4 Flows record-triggered por objeto

```sql
SELECT Id, ApiName, Label, TriggerType, TriggerObjectOrEventId
FROM FlowDefinitionView
WHERE TriggerType = 'RecordAfterSave'
   OR TriggerType = 'RecordBeforeDelete'
   OR TriggerType = 'RecordBeforeSave'
ORDER BY TriggerObjectOrEventId, Label
```

### 5.5 Execuções ativas/pausadas (Screen Flows)

```sql
SELECT Id, Name, InterviewLabel, CurrentElement, FlowVersionViewId,
       FlowVersionView.FlowDefinitionView.ApiName, CreatedDate, LastModifiedDate
FROM FlowInterview
ORDER BY CreatedDate DESC
```

---

## 6. Boas práticas e pontos de atenção

- **Diferencie definição ativa da mais recente**: uma definição pode ter versão mais recente ainda não ativada.
- **Documente o propósito** de cada Flow na descrição.
- **Versione flows antes de alterações**: mantenha histórico e rollback.
- **Evite Process Builder legado**: prefira Flows nativos.
- **Teste flows record-triggered** em bulk para evitar erros de governança.
- **Monitore Flows obsoletos** e remova versões não utilizadas quando possível.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Relacione objetos, Permission Sets e Apex** afetados por cada Flow.
- **Cuidado com subflows circularmente dependentes**: pode causar loops.
- **Valide privilégios de execução**: flows rodam no contexto do usuário por padrão (System context pode ser habilitado).

---

## 7. Links de referência oficial

- [Salesforce Help — Flow Builder](https://help.salesforce.com/s/articleView?id=sf.flow.htm)
- [Salesforce Developer — Flow Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flow.htm)
- [Salesforce Developer — FlowDefinitionView Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_flowdefinitionview.htm)
- [Salesforce Developer — FlowVersionView Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_flowversionview.htm)
- [Salesforce Help — Convert Process Builder to Flow](https://help.salesforce.com/s/articleView?id=sf.flow_migrate_from_process_builder.htm)
