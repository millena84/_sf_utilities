Aqui está o modelo completo e evoluído para **Autolaunched Flow** (`processType = AutoLaunchedFlow`). 

Diferente de um *Flow Trigger* (disparado por alteração de registro) ou de um *Screen Flow* (com telas e interface), o **Autolaunched Flow** funciona essencialmente como uma **função / método reutilizável em segundo plano**. Ele é invocado por Apex (`@InvocableMethod` ou `Flow.Interview`), Subfluxos, APIs REST externas, Process Builder ou Orquestrações. 

Por isso, o ponto central da sua documentação está no **Contrato de Interface (Variáveis de Entrada e Saída)**.

---

# 📑 Modelo Evoluído: Documentação Técnica de Autolaunched Flow (DETI - Autolaunched Module)

---

## 1. Identificação Geral

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `{Flow.fullName}` | `<fullName>` | Nome API exclusivo do fluxo. |
| **Label** | `{Flow.label}` | `<label>` | Rótulo de exibição na interface. |
| **ProcessType** | `AutoLaunchedFlow` | `<processType>` | Tipo de automação em segundo plano sem interface. |
| **Status** | `Active` \| `Draft` \| `Obsolete` | `<status>` | Estado de publicação na Org. |
| **ApiVersion** | `{Flow.apiVersion}` (ex: `62.0`) | `<apiVersion>` | Versão da API Salesforce utilizada. |
| **Description** | `{Flow.description}` | `<description>` | Objetivo funcional / Documentação da regra de negócio. |
| **RunInMode** | `DefaultMode` \| `SystemModeWithSharing` \| `SystemModeWithoutSharing` | `<runInMode>` | Contexto de execução e permissões de segurança/compartilhamento. |
| **StartElementReference** | `{Flow.startElementReference}` | `<startElementReference>` | Nome API do primeiro elemento/ação a ser executado. |

---

## 2. Contrato de Interface: Variáveis de Entrada e Saída (`<variables>`)

Como o Autolaunched Flow funciona como uma API/função, esta seção documenta a "assinatura" do parâmetro de chamada e retorno.

### 2.1. Parâmetros de Entrada (`isInput = true`)

| Nome da Variável (`name`) | Tipo de Dado (`dataType`) | Objeto Alvo (`objectType`) | Coleção/Lista? (`isCollection`) | Obrigatório? | Valor Padrão | Descrição / Finalidade | Fonte XML |
|---|---|---|---|---|---|---|---|
| `recordId` | `String` | - | `false` | Sim | `null` | ID do registro principal de contexto. | `<variables>` |
| `inputOrderList` | `SObject` | `Pedido__c` | **`true`** | Não | `null` | Lista de pedidos a serem processados em lote. | `<variables>` |
| `strSourceSystem` | `String` | - | `false` | Não | `'AWS'` | Identificador do sistema chamador. | `<variables>` |

### 2.2. Parâmetros de Saída (`isOutput = true`)

| Nome da Variável (`name`) | Tipo de Dado (`dataType`) | Objeto Alvo (`objectType`) | Coleção/Lista? (`isCollection`) | Descrição / Conteúdo Devolvido | Fonte XML |
|---|---|---|---|---|---|
| `isSuccess` | `Boolean` | - | `false` | Retorna `true` se o processamento concluiu sem falhas. | `<variables>` |
| `errorMessage` | `String` | - | `false` | Mensagem detalhada de erro caso ocorra uma exceção. | `<variables>` |
| `outputCreatedRecords` | `SObject` | `WorkOrder` | **`true`** | Coleção de Ordens de Serviço geradas pela execução. | `<variables>` |

---

## 3. Origem de Invocação Esperada (Ponto de Chamada)

Mapeamento de onde ou por quem este Autolaunched Flow foi projetado para ser chamado:

| Mecanismo de Invocação | Exemplo / Referência na Org | Parâmetros Mapeados |
|---|---|---|
| **Classe Apex** | `Flow.Interview.createInterview('Nome_Do_Flow', inputs)` | `recordId`, `inputOrderList` |
| **Ação Apex Invocável (`@InvocableMethod`)** | Chamado via Apex Handler ou Flow pai | `recordId` |
| **Subfluxo (`<subflows>`)** | Invocado por outro Flow (`ScreenFlow` ou `TriggerFlow`) | `recordId` -> `isSuccess` |
| **API REST Externa** | `/services/data/v62.0/actions/custom/flow/Meu_Autolaunched_Flow` | Payload JSON no Body |

---

## 4. Estruturas Internas: Constantes, Fórmulas e Decisões

### 4.1. Fórmulas e Cálculos (`<formulas>`)
| Nome da Fórmula (`name`) | Tipo de Retorno (`dataType`) | Expressão / Algoritmo | Finalidade | Fonte |
|---|---|---|---|---|
| `frmCalculaDesconto` | `Currency` | `{!varValorTotal} * ({!varPercentual} / 100)` | Calcula valor líquido descontado. | XML |
| `frmIsDataValida` | `Boolean` | `{!$Flow.CurrentDate} <= {!varDataLimite}` | Valida janela de execução. | XML |

### 4.2. Decisões e Desvios de Fluxo (`<decisions>`)
| Elemento (`name`) | Rótulo (`label`) | Resultado / Caminho (`rules.name`) | Condição Lógica (`booleanFilter` / `conditions`) | Ação Seguinte |
|---|---|---|---|---|
| `Decide_Aprovacao` | Validar Valor | `Caminho_Aprovado` | `{!varValorTotal} >= 5000 AND {!isClienteVIP} = true` | `Atualiza_Status` |
| | | `DefaultOutcome` | *(Outros casos)* | `Envia_Notificacao` |

---

## 5. Invocações Externas, Ações Apex e Subfluxos

### 5.1. Chamadas de Ação Apex e Integrações (`<actionCalls>`)
| Elemento (`name`) | Tipo de Ação (`actionType`) | Classe / Ação Chamada (`actionName`) | Entradas Passadas (`inputParameters`) | Saídas Capturadas (`outputParameters`) | Fonte |
|---|---|---|---|---|---|
| `Callout_AWS_S3` | `apex` | `AWSServiceFileUploader` | `fileBlob = {!varBlob}`, `folder = 'docs'` | `s3Url = {!varS3Url}` | XML |
| `Post_Chatter_Notification` | `postToChatter` | - | `text = {!txtMessage}`, `targetEntityId = {!recordId}` | - | XML |

### 5.2. Subfluxos Chamados (`<subflows>`)
| Elemento (`name`) | Fluxo Invocado (`flowName`) | Variáveis de Entrada Enviadas | Variáveis de Saída Recebidas | Fonte |
|---|---|---|---|---|
| `Executa_Geração_PDF` | `Subflow_Gerador_Documentos` | `recordId = {!recordId}` | `pdfBlobId <- varPdfId` | XML |

---

## 6. Operações no Banco de Dados (DML & SOQL)

| Elemento (`name`) | Operação | Objeto Alvo (`object`) | Filtro / Condição de Busca (`filters`) | Modifica Coleção? | Fonte |
|---|---|---|---|---|---|
| `Busca_Itens_Pedido` | Lookups (SOQL) | `OrderItem` | `OrderId = {!recordId}` | Sim (Retorna Lista) | XML |
| `Cria_Historico_Integracao` | Creates (Insert) | `Log_Integracao__c` | Preenche `Payload__c`, `Status__c` | Não | XML |
| `Atualiza_Pedidos_Lote` | Updates (Update) | `Pedido__c` | Atualiza coleção `{!inputOrderList}` | Sim | XML |

---

# 🤖 JSON Schema para Preenchimento Automático do Autolaunched Flow

Utilize este esquema para validar o utilitário autômato que analisa o arquivo `.flow-meta.xml` de um Autolaunched Flow:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceAutolaunchedFlowDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "processType": { "type": "string", "enum": ["AutoLaunchedFlow"] },
        "status": { "type": "string" },
        "apiVersion": { "type": "string" },
        "description": { "type": "string" },
        "runInMode": { "type": "string" },
        "startElementReference": { "type": "string" }
      },
      "required": ["developerName", "label", "processType", "status"]
    },
    "interface_contract": {
      "type": "object",
      "properties": {
        "input_variables": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "dataType": { "type": "string" },
              "objectType": { "type": "string" },
              "isCollection": { "type": "boolean" },
              "isRequired": { "type": "boolean" },
              "defaultValue": { "type": "string" },
              "description": { "type": "string" }
            }
          }
        },
        "output_variables": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "dataType": { "type": "string" },
              "objectType": { "type": "string" },
              "isCollection": { "type": "boolean" },
              "description": { "type": "string" }
            }
          }
        }
      }
    },
    "formulas": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "dataType": { "type": "string" },
          "expression": { "type": "string" }
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
          "isCollection": { "type": "boolean" }
        }
      }
    }
  },
  "required": ["identification", "interface_contract"]
}
```

---

### 💡 Principais Diferenciais deste Modelo:

1. **Destaque ao Contrato de API (`interface_contract`):** Foco nas flags `<isInput>` e `<isOutput>` das variáveis, permitindo entender exatamente quais dados o robô precisa passar e o que ele recebe de volta.
2. **Mapeamento de Invocação:** Mostra se o fluxo é chamado via Apex, API REST, Subfluxo ou Flow Pai.
3. **Sem Poluição de Interface:** Elimina tabelas de telas e botões de navegação que só existem no *Screen Flow*, mantendo a documentação enxuta e focada na lógica de negócios e integrações em segundo plano.

Com isso, você tem o trio completo de modelos de Flow (*Record-Triggered Flow*, *Screen Flow* e *Autolaunched Flow*) prontos para serem extraídos por agentes ou scripts!
