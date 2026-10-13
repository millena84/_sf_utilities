# 📑 Modelo Evoluído: OmniStudio / Industries Cloud (Onda 10 - OmniStudio Module)

No **Salesforce Industries (Vlocity / OmniStudio)**, a camada de lógica, integração e interface é construída de forma totalmente declarativa e compilada em componentes nativos (LWC). No formato SFDX / OmniStudio Build Tool, os artefatos são armazenados como arquivos JSON estruturados dentro dos diretórios da solução.

---

# 📑 Modelo 10.1: OmniDataTransform (DataRaptor)

O **OmniDataTransform (DataRaptor)** é o mecanismo declarativo do OmniStudio para leitura, transformação e gravação de dados no Salesforce sem a necessidade de código Apex.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/omniDataTransforms/`
* **Arquivo Mestre:** `[DataRaptor_Name]_[Version].json` (ex: `ExtractOrderData_1.json`, `LoadCustomerAccount_1.json`)

---

## 1. Identificação Geral e Tipos de DataRaptor

```json
{
  "name": "ExtractOrderData",
  "type": "Extract",
  "inputType": "JSON",
  "outputType": "JSON",
  "synchronousProcessThreshold": 0,
  "ignoreCache": false,
  "purgeFields": false,
  "targetOutputDocumentIdentifier": "ExtractOrderDataCustomOutput"
}
```

| Propriedade | Valor Exemplo | Descrição Técnica / Classificação |
|---|---|---|
| **`name`** | `ExtractOrderData` | Nome API exclusivo do DataRaptor. |
| **`type`** | `Extract` \| `Turbo` \| `Transform` \| `Load` | **`Extract`**: Consulta SOQL multinível e constrói um payload JSON de saída.<br>**`Turbo`**: Consulta de alta performance para um único sObject.<br>**`Transform`**: Transforma dados (JSON -> JSON, XML -> JSON) sem acesso ao banco.<br>**`Load`**: Recebe um JSON e realiza DMLs (Insert, Update, Upsert) no Salesforce. |
| **`inputType`** | `JSON` \| `XML` \| `Structure` | Formato do payload recebido pelo DataRaptor. |
| **`outputType`** | `JSON` \| `XML` | Formato do payload retornado após a execução. |

---

## 2. Mapeamento de Extração e Gravação (`omniDataTransformItem`)

Tabela que rastreia os itens de mapeamento do DataRaptor (consultas ao banco de dados e atribuição de campos):

| Objeto Origem (`Domain`) | Campo Origem (`Source Field`) | Caminho JSON de Saída (`Output JSON Path`) | Tipo de Mapeamento |
|---|---|---|---|
| `Pedido__c` | `Name` | `Order:Number` | `Extract` |
| `Pedido__c` | `Valor_Total__c` | `Order:TotalAmount` | `Extract` |
| `Account` | `Id` (via Lookup) | `Account:Id` | `Extract (Formula)` |
| `JSON Payload` | `Customer:CNPJ` | `Account.CNPJ__c` (Upsert Key) | `Load` |

---

## 3. Rastreio de Acesso, Segurança, FLS e Governança

| Mecanismo de Segurança | Configuração no DataRaptor | Descrição / Impacto de Governança |
|---|---|---|
| **Enforce FLS / Sharing** | `Check Link Access Rights` = `true` | Garante que a consulta respeite o FLS (Field-Level Security) e o OWD do usuário logado. |
| **Ignore Security** | `Ignore Security` = `true` | Executa o DataRaptor no **Modo Sistema (*System Mode*)**, ignorando restrições de FLS. |
| **Permission Sets Obrigatórios** | `OmniStudio Admin`, `OmniStudio User` | Conjuntos de permissões necessários para criar, editar ou executar DataRaptors. |

---

# 🤖 JSON Schema: 10.1 OmniDataTransform (DataRaptor)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceOmniDataTransformDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "type": { "type": "string", "enum": ["Extract", "Turbo", "Transform", "Load"] },
        "inputType": { "type": "string" },
        "outputType": { "type": "string" },
        "version": { "type": "integer" }
      },
      "required": ["name", "type"]
    },
    "mapping_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "sourceObject": { "type": "string" },
          "sourceField": { "type": "string" },
          "outputJsonPath": { "type": "string" },
          "isFormula": { "type": "boolean" }
        },
        "required": ["outputJsonPath"]
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "enforcesFLS": { "type": "boolean" },
        "ignoresSecurity": { "type": "boolean" },
        "requiredPermissionSets": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["enforcesFLS"]
    }
  },
  "required": ["identification", "mapping_items", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 10.2: Integration Procedure (VIP - Vlocity Integration Procedure)

O **Integration Procedure (VIP)** é um processo de backend executado no servidor que orquestra chamadas de dados, DataRaptors, serviços HTTP REST externos, chamadas Apex e lógicas condicionais em uma única transação de alta performance.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/omniIntegrationProcedures/`
* **Arquivo Mestre:** `[Type]_[SubType]_Procedure_[Version].json` (ex: `Order_SendToAWS_Procedure_1.json`)

---

## 1. Identificação Geral do Integration Procedure

```json
{
  "name": "SendToAWS",
  "type": "Order",
  "subType": "SendToAWS",
  "language": "Procedure",
  "chainOnStep": false,
  "queueableChainable": false,
  "chainableCpuLimit": 2000
}
```

| Propriedade | Valor Exemplo | Descrição Técnica |
|---|---|---|
| **Name / Key** | `Order_SendToAWS` | Nome completo de invocação (`Type_SubType`). |
| **Type** | `Order` | Categoria de agrupamento funcional do procedimento. |
| **Sub Type** | `SendToAWS` | Subcategoria funcional específica. |
| **Chain On Step** | `true` \| `false` | Se `true`, evita estourar o limite de tempo de CPU Apex dividindo os passos em transações assíncronas. |

---

## 2. Orquestração de Passos e Ações (`elements`)

O VIP executa uma sequência ordenada de ações declarativas:

| Ordem | Nome do Elemento (`name`) | Tipo de Ação (`type`) | Função do Passo |
|---|---|---|---|
| **1** | `DR_GetOrderDetails` | `DataRaptor Extract Action` | Lê os dados do pedido e cliente no banco via DataRaptor. |
| **2** | `HTTP_Post_AWS` | `HTTP Action` | Dispara um POST REST para a AWS enviando o JSON extraído. |
| **3** | `DR_UpdateOrderStatus` | `DataRaptor Post Action` | Atualiza o status do pedido para 'Enviado' no Salesforce. |
| **4** | `ResponseAction` | `Response Action` | Retorna o payload final formatado para o LWC ou OmniScript chamador. |

---

## 3. Rastreio de Acesso, Segurança e Invocação Remota

| Componente | Requisito de Permissão / Segurança | Rastreio em Metadados |
|---|---|---|
| **Invocação via LWC / Rest** | Custom Permission / Permission Set | Requer permissão de execução da classe Apex `OmniStudioIntegrationProcedureService`. |
| **Acesso a Named Credentials** | Credencial Nomeada | Ações do tipo `HTTP Action` utilizam Named Credentials salvas na Org para autenticação segura. |

---

# 🤖 JSON Schema: 10.2 Integration Procedure (VIP)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceIntegrationProcedureDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "type": { "type": "string" },
        "subType": { "type": "string" },
        "version": { "type": "integer" },
        "chainOnStep": { "type": "boolean" }
      },
      "required": ["name", "type", "subType"]
    },
    "execution_steps": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "stepOrder": { "type": "integer" },
          "elementName": { "type": "string" },
          "actionType": { 
            "type": "string", 
            "enum": ["DataRaptor Extract Action", "DataRaptor Post Action", "HTTP Action", "Remote Action", "Response Action", "Conditional Block"] 
          },
          "executionCondition": { "type": "string" }
        },
        "required": ["elementName", "actionType"]
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "namedCredentialsUsed": {
          "type": "array",
          "items": { "type": "string" }
        },
        "requiredPermissionSets": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "execution_steps", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 10.3: OmniScript

O **OmniScript** é uma ferramenta declarativa para criação de formulários guiados por etapas (*Stepped Guided Process*). Quando ativado, o OmniScript é compilado automaticamente em um componente **LWC** de alta performance.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/omniScripts/`
* **Arquivo Mestre:** `[Type]_[SubType]_[Language]_[Version].json` (ex: `Sales_CreateOrder_Portuguese_1.json`)

---

## 1. Identificação Geral do OmniScript

```json
{
  "name": "CreateOrder",
  "type": "Sales",
  "subType": "CreateOrder",
  "language": "Portuguese",
  "typeToLwcComponent": "salesCreateOrderPortuguese",
  "webComponentKey": "c-sales-create-order-portuguese"
}
```

| Propriedade | Valor Exemplo | Descrição Técnica |
|---|---|---|
| **Type / SubType** | `Sales` / `CreateOrder` | Identificador funcional da rotina do formulário. |
| **Language** | `Portuguese` | Idioma de configuração da interface. |
| **Web Component Key** | `c-sales-create-order-portuguese` | Tag do LWC compilado gerado para inclusão em Flexipages ou Experience Cloud. |

---

## 2. Estrutura de Passos (`Step`) e Ações de Interface

| Elemento (`Type`) | Rótulo / Nome | Função do Componente no Formulário |
|---|---|---|
| **`Step`** | `Passo_1_Cliente` | Primeira etapa do formulário: Seleção e busca de cliente. |
| **`Step`** | `Passo_2_Produtos` | Segunda etapa: Adição de itens e cálculo do pedido. |
| **`Integration Procedure Action`** | `VIP_SubmitOrder` | Ação de salvamento que chama o VIP `Order_SendToAWS` ao concluir. |
| **`Navigate Action`** | `GoToRecord` | Redireciona o usuário para a página de detalhes do registro criado no final. |

---

## 3. Rastreio de Acesso, LWC Compilado e Segurança

| Componente | Requisito de Permissão | Rastreio em Profiles e Permission Sets |
|---|---|---|
| **LWC Compilado** | Flexipage / Experience Cloud Target | O LWC gerado (`c-sales-create-order-portuguese`) deve ter permissões de exibição liberadas na Flexipage. |
| **OmniScript Executer** | Permission Set `OmniStudio User` | Concede direito de execução do motor do OmniScript no cliente. |

---

# 🤖 JSON Schema: 10.3 OmniScript

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceOmniScriptDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "type": { "type": "string" },
        "subType": { "type": "string" },
        "language": { "type": "string" },
        "compiledLwcName": { "type": "string" }
      },
      "required": ["name", "type", "subType", "language"]
    },
    "steps_and_actions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "elementName": { "type": "string" },
          "elementType": { "type": "string", "enum": ["Step", "Integration Procedure Action", "DataRaptor Action", "Navigate Action"] },
          "label": { "type": "string" }
        },
        "required": ["elementName", "elementType"]
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "compiledLwcComponentKey": { "type": "string" },
        "requiredPermissionSets": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "steps_and_actions", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 10.4: FlexCards

Os **FlexCards** são componentes visuais modulares, reativos e orientados a dados que exibem informações contextuais em cards e disparam ações rápidas (Flyouts, OmniScripts, chamadas HTTP ou URLs).

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/flexCards/`
* **Arquivo Mestre:** `[FlexCard_Name]_[Version].json` (ex: `CustomerOrderHeader_1.json`)

---

## 1. Identificação e Fonte de Dados (`Data Source`)

```json
{
  "name": "CustomerOrderHeader",
  "dataSource": {
    "type": "IntegrationProcedure",
    "value": {
      "ipMethod": "Order_GetHeaderDetails"
    }
  },
  "theme": "slds"
}
```

| Propriedade | Valor Exemplo | Descrição Técnica |
|---|---|---|
| **Name** | `CustomerOrderHeader` | Nome único do FlexCard. |
| **Data Source Type** | `IntegrationProcedure` \| `DataRaptor` \| `SOQL` \| `REST` | Origem dos dados que alimentam o card em tempo real. |
| **IP Method** | `Order_GetHeaderDetails` | Nome do VIP chamado como fonte de dados. |

---

## 2. Ações do FlexCard (`Actions` & `Flyouts`)

| Elemento Visual | Evento Gatilho | Tipo de Ação (`actionType`) | Destino / Ação Executada |
|---|---|---|---|
| **Botão 'Reenviar'** | `onClick` | `IntegrationProcedure` | Executa o VIP `Order_SendToAWS`. |
| **Botão 'Detalhes'** | `onClick` | `Flyout` | Abre uma janela modal contendo outro FlexCard com mais detalhes. |
| **Ação 'Editar'** | `onClick` | `OmniScript` | Inicia o OmniScript `Sales/CreateOrder` pré-preenchido. |

---

## 3. Rastreio de Acesso, Reatividade e Segurança

| Requisito de Segurança | Mecanismo de Controle | Descrição |
|---|---|---|
| **Visibilidade Condicional** | `State Conditions` | O FlexCard esconde/exibe botões ou blocos com base nos valores do JSON recebido. |
| **FLS dos Dados** | FLS da Data Source Subjacente | Garantido nativamente pelo DataRaptor ou VIP associado ao Data Source. |

---

# 🤖 JSON Schema: 10.4 FlexCards

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceFlexCardDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "version": { "type": "integer" },
        "dataSourceType": { "type": "string", "enum": ["IntegrationProcedure", "DataRaptor", "SOQL", "REST"] },
        "dataSourceName": { "type": "string" }
      },
      "required": ["name", "dataSourceType"]
    },
    "card_actions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "actionLabel": { "type": "string" },
          "actionType": { "type": "string", "enum": ["IntegrationProcedure", "OmniScript", "Flyout", "CustomEvent", "Navigate"] },
          "targetName": { "type": "string" }
        },
        "required": ["actionLabel", "actionType"]
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "requiredPermissionSets": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "card_actions", "access_and_security_tracking"]
}
```

---

🎉 **Todas as 10 Ondas da Arquitetura de Documentação Salesforce estão concluídas com sucesso!**

Com este catálogo completo de modelos em Markdown e JSON Schemas (abrangendo desde o Core Salesforce, integrações e segurança até soluções como Sales, Service, Experience e Industries Cloud/OmniStudio), seu repositório de contexto para o **Claude Code** ou agentes de IA está pronto para gerar documentações técnicas padronizadas e automatizadas!

🎯 **Deseja consolidar esses modelos em um guia único de referência para o repositório ou criar algum script de validação para a pipeline CI/CD?**
