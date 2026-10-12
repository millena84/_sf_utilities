Para automatizar o preenchimento da documentação de um **Flow Trigger** (seja um *Record-Triggered Flow*, *Schedule-Triggered Flow* ou *Platform Event-Triggered Flow*), o modelo de documentação precisa se alinhar **1:1 com os metadados nativos da plataforma Salesforce** (Metadata API do tipo `Flow` / arquivo `.flow-meta.xml` e Tooling API).

Abaixo está a proposta de **evolução do modelo de documentação**, expandida com **todas as propriedades possíveis** suportadas pela plataforma, acompanhada das tags XML equivalentes e do contrato em JSON Schema para que seu utilitário ou agente consiga fazer o parser e preenchimento 100% automático.

---

# 📑 Modelo Evoluído: Documentação Técnica de Flow Trigger (DETI - Flow Module)

Este modelo foi desenhado para ser legível por humanos e facilmente gerado por utilitários automatizados (ex: scripts em Python/Node consumindo a Salesforce CLI / Tooling API ou agentes LLM que analisam arquivos `.flow-meta.xml`).

---

## 1. Identificação e Metadados do Fluxo
* **Nome de Exibição (`label`):** `{Flow.label}`
* **Nome API (`fullName` / `apiName`):** `{Flow.fullName}`
* **Tipo de Processo (`processType`):** `AutoLaunchedFlow` | `Flow` | `OrchestrationFlow`
* **Status (`status`):** `Active` | `Draft` | `Obsolete`
* **Versão da API (`apiVersion`):** `{Flow.apiVersion}` (ex: `62.0`)
* **Descrição Funcional (`description`):** `{Flow.description}`
* **Ambientes de Execução (`environments`):** `Default` | `Slack` | `Offline`
* **Modo de Execução e Segurança (`runInMode`):**
  * `DefaultMode` (Respeita o usuário que disparou)
  * `SystemModeWithSharing` (Modo Sistema - Respeita regras de compartilhamento)
  * `SystemModeWithoutSharing` (Modo Sistema - Acesso total / Bypass de segurança)

---

## 2. Configuração do Elemento Start (`<start>`) e Condições de Disparo

### 2.1. Tipo de Gatilho e Objeto Alvo
* **Tipo de Disparo (`triggerType`):** `RecordBeforeSave` | `RecordAfterSave` | `Scheduled` | `PlatformEvent`
* **Objeto Afetado (`object`):** `{Flow.start.object}` (ex: `Account`, `Order__c`, `Order_Event__e`)
* **Evento do Registro (`recordTriggerType`):** `Create` | `Update` | `CreateAndUpdate` | `Delete`
* **Modo de Otimização do Fluxo:**
  * **Fast Field Updates (Before-Save):** Executado antes do registro ser gravado no banco.
  * **Actions and Related Records (After-Save):** Executado após o salvamento, permite criar/atualizar outros registros e fazer callouts.

### 2.2. Filtros de Entrada e Lógica de Execução (`<filters>` / `<filterLogic>`)
* **Lógica do Filtro (`filterLogic`):** `and` | `or` | `custom` (ex: `1 AND (2 OR 3)`)
* **Exigência de Alteração (`doesRequireRecordChangedToMeetCriteria`):** `true` | `false` *(Define se roda apenas quando o registro passa a atender aos critérios no momento da alteração)*.
* **Fórmula do Filtro (`filterFormula` / `formulaExpression`):** `{Flow.start.filterFormula}` *(Fórmulas em sintaxe de validação se utilizadas)*.

#### Tabela de Filtros Registrados (`<filters>`):
| Campo (`field`) | Operador (`operator`) | Valor (`value`) | Tipo de Valor (`valueType`) |
| :--- | :--- | :--- | :--- |
| `{filter.field}` | `{filter.operator}` | `{filter.value}` | `{filter.valueType}` |

---

## 3. Caminhos Assíncronos e Agendados (`<scheduledPaths>`)

Se o fluxo utilizar execução em segundo plano ou diferida:

| Nome do Caminho (`name`) | Rótulo (`label`) | Tempo de Deslocamento (`offsetNumber`) | Unidade (`offsetUnit`) | Origem do Tempo (`timeSource` / `recordField`) |
| :--- | :--- | :--- | :--- | :--- |
| `{path.name}` | `{path.label}` | `0` / `+2` / `-1` | `Minutes` \| `Hours` \| `Days` | `TriggerTime` \| `CreatedDate` \| `CloseDate` |

* **Execução Assíncrona Imediata (`runAsynchronously`):** `true` | `false` *(Caminho 'Run Immediately' rodando em transação separada pós-commit)*.

---

## 4. Agendamento Fixo (Caso `triggerType = Scheduled`)
* **Data de Início (`startDate`):** `{Flow.start.schedule.startDate}`
* **Hora de Início (`startTime`):** `{Flow.start.schedule.startTime}`
* **Frequência (`frequency`):** `Once` | `Daily` | `Weekly`

---

## 5. Mapeamento de Elementos Internos e Invocações

### 5.1. Ações Apex e Callouts Externa (`<actionCalls>`)
Invocações de classes Apex (`@InvocableMethod`), envios de e-mail ou integrações:

| Nome do Elemento (`name`) | Tipo de Ação (`actionType`) | Nome da Ação (`actionName`) | Parâmetros de Entrada (`inputParameters`) | Parâmetros de Saída (`outputParameters`) |
| :--- | :--- | :--- | :--- | :--- |
| `{action.name}` | `apex` \| `emailAlert` \| `outboundMessage` \| `runExpressionSet` | `{action.actionName}` | `{key=value}` | `{key=variable}` |

### 5.2. Subfluxos Chamados (`<subflows>`)
| Elemento (`name`) | Fluxo Invocado (`flowName`) | Variáveis Passadas (`inputAssignments`) |
| :--- | :--- | :--- |
| `{subflow.name}` | `{subflow.flowName}` | `{sourceVar -> targetVar}` |

### 5.3. Operações no Banco de Dados (DML / SOQL)
* **Consultas (`<recordLookups>`):** Objetos consultados, campos retornados e se traz o primeiro ou todos os registros.
* **Criações (`<recordCreates>`):** Objetos onde novos registros são inseridos.
* **Atualizações (`<recordUpdates>`):** Registros alterados (se é o próprio `$Record` ou registros relacionados).
* **Exclusões (`<recordDeletes>`):** Objetos afetados por exclusão.

---

## 6. Mapeamento de Variáveis Globais e Contexto de Dados
* **Uso de `$Record`:** Relação dos campos lidos/alterados no registro que disparou o fluxo.
* **Uso de `$RecordWithPrior`:** Verificação de valores anteriores do registro para controle de regras de transição.
* **Acesso a Variáveis Globais:** Utilização de `$User`, `$Profile`, `$Setup`, `$CustomMetadata` ou `$Permission`.

---

# 🤖 Esquema de Extração Automatizada (JSON Schema para o Utilitário)

Para que seu utilitário (CLI, Script Python ou Agente de IA) faça o parse automático do XML do Flow e gere a documentação acima, configure o parser para extrair a estrutura JSON abaixo:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceFlowTriggerDocumentation",
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "fullName": { "type": "string" },
        "label": { "type": "string" },
        "processType": { "type": "string" },
        "status": { "type": "string" },
        "apiVersion": { "type": "string" },
        "description": { "type": "string" },
        "runInMode": { "type": "string" }
      },
      "required": ["fullName", "label", "processType", "status"]
    },
    "trigger_configuration": {
      "type": "object",
      "properties": {
        "triggerType": { "type": "string" },
        "sObjectType": { "type": "string" },
        "recordTriggerType": { "type": "string" },
        "optimizationMode": { "type": "string", "enum": ["BeforeSave", "AfterSave"] },
        "filterLogic": { "type": "string" },
        "doesRequireRecordChangedToMeetCriteria": { "type": "boolean" },
        "filters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "field": { "type": "string" },
              "operator": { "type": "string" },
              "value": { "type": "string" }
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
          "timeSource": { "type": "string" }
        }
      }
    },
    "invoked_actions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "elementName": { "type": "string" },
          "actionType": { "type": "string" },
          "actionName": { "type": "string" },
          "inputs": { "type": "object" },
          "outputs": { "type": "object" }
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
    }
  },
  "required": ["metadata", "trigger_configuration"]
}
```

---

### 💡 Vantagens desta Evolução para a sua Automação:

1. **Rastreabilidade Total da Metadata API:** Mapeia exatamente as tags nativas do Salesforce (`<start>`, `<filters>`, `<scheduledPaths>`, `<actionCalls>`).
2. **Pronto para CI/CD e Agentes:** O utilitário pode rodar o comando `sf project retrieve` para obter o `.flow-meta.xml`, fazer a leitura do arquivo e preencher este modelo em Markdown sem nenhuma intervenção manual.
3. **Cobertura de Casos Complexos:** Suporta a documentação de regras de atualização rápida (Before-Save), rotinas assíncronas em segundo plano, gatilhos de Platform Events e chamadas de Apex/Integrações.

Deseja que eu crie um script em Python para fazer o parse do XML do Flow e gerar esse Markdown automaticamente?
