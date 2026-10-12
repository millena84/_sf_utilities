Perfeito! Vamos pegar a estrutura inicial que você enviou e expandi-la para abranger **todas as propriedades possíveis** de um **Flow Trigger** no Salesforce (seja *Record-Triggered*, *Schedule-Triggered* ou *Platform Event-Triggered*), mapeando cada campo para a sua tag na Metadata API (`.flow-meta.xml`) e Tooling API.

---

# 📑 Modelo Evoluído: Documentação Técnica de Flow Trigger (DETI - Flow Trigger Module)

---

## 1. Identificação Geral

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `{Flow.fullName}` | `<fullName>` | Nome API exclusivo do fluxo. |
| **Label** | `{Flow.label}` | `<label>` | Rótulo de exibição na interface. |
| **ProcessType** | `AutoLaunchedFlow` | `<processType>` | Tipo de automação (Autolaunched / Trigger). |
| **TriggerType** | `RecordAfterSave` \| `RecordBeforeSave` \| `Scheduled` \| `PlatformEvent` \| `RecordBeforeDelete` | `<start.triggerType>` | Tipo e momento do disparo. |
| **Object** | `{Flow.start.object}` | `<start.object>` | Objeto que dispara a automação (ou `PlatformEvent`). |
| **RecordTriggerType** | `Create` \| `Update` \| `CreateAndUpdate` \| `Delete` | `<start.recordTriggerType>` | Evento de DML no registro que ativa o gatilho. |
| **Status** | `Active` \| `Draft` \| `Obsolete` | `<status>` | Estado de publicação na Org. |
| **ApiVersion** | `{Flow.apiVersion}` (ex: `62.0`) | `<apiVersion>` | Versão da API Salesforce utilizada. |
| **Description** | `{Flow.description}` | `<description>` | Documentação / Objetivo funcional do fluxo. |
| **RunInMode** | `DefaultMode` \| `SystemModeWithSharing` \| `SystemModeWithoutSharing` | `<runInMode>` | Contexto de segurança e compartilhamento. |
| **OptimizationMode** | `FastFieldUpdates` (Before) \| `ActionsAndRelatedRecords` (After) | `<start.elementSubtype>` | Otimização de performance de execução. |

---

## 2. Condições de Disparo e Filtros (`<start>`)

### 2.1. Regras do Filtro
* **Lógica dos Filtros (`filterLogic`):** `and` | `or` | `custom` (ex: `1 AND (2 OR 3)`)
* **Exigir Alteração de Registro (`doesRequireRecordChangedToMeetCriteria`):** `true` | `false` *(Garante que a automação só rode se o registro passou a atender aos critérios nesta alteração especificamente)*.
* **Fórmula de Filtro (`filterFormula`):** `{Flow.start.filterFormula}` *(Se utilizar fórmula em sintaxe de regra de validação)*.

### 2.2. Tabela de Filtros Registrados (`<filters>`)

| Campo (`field`) | Operador (`operator`) | Valor (`value`) | Tipo do Valor (`valueType` / Elemento XML) | Fonte |
|---|---|---|---|---|
| `Status__c` | `EqualTo` | `Aprovado` | `stringValue` | XML (`<start.filters>`) |
| `Valor_Total__c` | `GreaterThan` | `1000` | `numberValue` | XML (`<start.filters>`) |
| `IsActive__c` | `EqualTo` | `true` | `booleanValue` | XML (`<start.filters>`) |
| `AccountId` | `IsNull` | `false` | `booleanValue` | XML (`<start.filters>`) |

---

## 3. Agendamento Fixo (Caso `TriggerType = Scheduled`)

| Propriedade | Valor | Tag XML | Descrição |
|---|---|---|---|
| **Data de Início** | `{startDate}` (YYYY-MM-DD) | `<start.schedule.startDate>` | Data do primeiro disparo. |
| **Hora de Início** | `{startTime}` (HH:MM:SS.SSSZ) | `<start.schedule.startTime>` | Horário fixo da execução. |
| **Frequência** | `Once` \| `Daily` \| `Weekly` | `<start.schedule.frequency>` | Periodicidade de repetição. |

---

## 4. Caminhos Assíncronos e Agendados (`<scheduledPaths>`)

Caminhos de execuçãodiferida ou em segundo plano configurados no elemento `Start`:

| Nome do Caminho (`name`) | Rótulo (`label`) | Tempo (`offsetNumber`) | Unidade (`offsetUnit`) | Origem do Tempo (`recordField` / `timeSource`) | Execução Assíncrona Imediata (`runAsynchronously`) | Fonte |
|---|---|---|---|---|---|---|
| `Envio_Lembrete_3_Dias` | Lembrar em 3 dias | `+3` | `Days` | `Data_Vencimento__c` | `false` | XML |
| `Processamento_Heavy_Async` | Executar Async | `0` | `Minutes` | `TriggerTime` | `true` (Run Immediately Async) | XML |

---

## 5. Invocações Externa, Ações Apex e Subfluxos

### 5.1. Chamadas de Ação Apex e Alertas (`<actionCalls>`)
| Elemento (`name`) | Tipo de Ação (`actionType`) | Nome da Classe / Ação (`actionName`) | Parâmetros de Entrada (`inputParameters`) | Variáveis de Saída Capturadas (`outputParameters`) | Fonte |
|---|---|---|---|---|---|
| `Chama_Integracao_AWS` | `apex` | `AWSOrderIntegrationService` | `orderId = $Record.Id` | `statusCode = varStatusCode` | XML |
| `Envia_Email_Aprovacao` | `emailAlert` | `Send_Approval_Notification` | `SObjectRowId = $Record.Id` | - | XML |

### 5.2. Subfluxos Chamados (`<subflows>`)
| Elemento (`name`) | Nome do Fluxo Invocado (`flowName`) | Atribuição de Entrada (`inputAssignments`) | Atribuição de Saída (`outputAssignments`) | Fonte |
|---|---|---|---|---|
| `Executa_Validação_Cliente` | `Subflow_Validar_CNPJ` | `inputAccountId = $Record.Account__c` | `varIsValid <- outputIsValid` | XML |

---

## 6. Operações no Banco de Dados (DML & SOQL)

* **Consultas (`<recordLookups>`):** Busca registros adicionais no banco para tomadas de decisão.
* **Criações (`<recordCreates>`):** Insere novos registros em objetos relacionados.
* **Atualizações (`<recordUpdates>`):** Altera o próprio `$Record` ou registros relacionados.
* **Exclusões (`<recordDeletes>`):** Remove registros da base.

| Elemento (`name`) | Operação | Objeto Alvo (`object`) | Atualiza o próprio `$Record`? | Filtro / Condição de Busca | Fonte |
|---|---|---|---|---|---|
| `Atualiza_Status_Pedido` | Update | `Pedido__c` | **Sim** (`$Record`) | N/A (Registro Atual) | XML |
| `Cria_Ordem_Servico` | Create | `WorkOrder` | **Não** | Preenche `AccountId = $Record.Conta__c` | XML |

---

## 7. Variáveis Globais e Contexto Utilizado

| Recurso Global | Campos Acessados / Utilizados | Finalidade |
|---|---|---|
| **`$Record`** | `$Record.Id`, `$Record.Status__c`, `$Record.Valor__c` | Leitura e atualização de valores do registro que disparou o fluxo. |
| **`$RecordWithPrior`** | `$RecordWithPrior.Status__c` | Comparação do valor anterior do campo para validações de transição de estado. |
| **`$User` / `$Profile`** | `$User.Id`, `$Profile.Name` | Identificação do usuário que provocou a alteração no banco. |
| **`$CustomMetadata`** | `$CustomMetadata.Integration_Setting__mdt.AWS.Endpoint__c` | Leitura de parametrização de ambiente sem código. |

---

# 🤖 JSON Schema para Preenchimento Automático pelo Utilitário

Seu utilitário de automação (script Python, Node.js ou Agente de IA) pode usar a estrutura abaixo para extrair o XML do Flow e preencher o modelo automaticamente:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceFlowTriggerDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "processType": { "type": "string" },
        "triggerType": { "type": "string" },
        "object": { "type": "string" },
        "recordTriggerType": { "type": "string" },
        "status": { "type": "string" },
        "apiVersion": { "type": "string" },
        "description": { "type": "string" },
        "runInMode": { "type": "string" },
        "optimizationMode": { "type": "string" }
      },
      "required": ["developerName", "label", "triggerType", "object"]
    },
    "conditions": {
      "type": "object",
      "properties": {
        "filterLogic": { "type": "string" },
        "doesRequireRecordChangedToMeetCriteria": { "type": "boolean" },
        "filterFormula": { "type": "string" },
        "filters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "field": { "type": "string" },
              "operator": { "type": "string" },
              "value": { "type": "string" },
              "valueType": { "type": "string" }
            }
          }
        }
      }
    },
    "scheduled_paths": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "label": { "type": "string" },
          "offsetNumber": { "type": "integer" },
          "offsetUnit": { "type": "string" },
          "recordField": { "type": "string" },
          "runAsynchronously": { "type": "boolean" }
        }
      }
    },
    "action_calls": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "elementName": { "type": "string" },
          "actionType": { "type": "string" },
          "actionName": { "type": "string" },
          "inputParameters": { "type": "object" },
          "outputParameters": { "type": "object" }
        }
      }
    },
    "subflows": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "elementName": { "type": "string" },
          "flowName": { "type": "string" }
        }
      }
    },
    "dml_operations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "elementName": { "type": "string" },
          "operation": { "type": "string" },
          "object": { "type": "string" },
          "isTargetingRecord": { "type": "boolean" }
        }
      }
    }
  },
  "required": ["identification", "conditions"]
}
```

---

### 💡 Por que este modelo atende ao seu robô/agente?

1. **Mapeamento Direto para o `.flow-meta.xml`:** Cada propriedade aponta exatamente para onde o parser de XML deve buscar a informação (ex: `<start.filters>`, `<start.object>`, `<actionCalls>`).
2. **Clareza de Origem:** A coluna "Fonte" sinaliza se o dado veio do XML direto, da Tooling API ou de uma inferência de código.
3. **Suporte Completo a Casos Avançados:** Cobre desde gatilhos simples antes/depois de salvar até *Schedule-Triggered Flows*, *Platform Events* e caminhos assíncronos (*Scheduled Paths*).
