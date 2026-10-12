# 📑 Modelo Evoluído: Documentação Técnica de Custom Object (DETI - Custom Object Module)

No formato de código fonte do Salesforce (SFDX Source Format), um objeto customizado é armazenado como uma pasta dentro do repositório (`force-app/main/default/objects/<Objeto__c>/`). Essa pasta consolida o arquivo de definição mestre do objeto e várias subpastas contendo arquivos XML individuais para cada um dos seus sub-metadados.

Abaixo está o modelo completo e evoluído, desenhado para que um utilitário autômato (script ou agente de IA) leia todos os arquivos XML dentro da pasta do objeto e gere um documento consolidado.

---

# Custom Object: Pedido__c

## 1. Mapeamento da Arquitetura de Pastas do Objeto (`objects/Pedido__c/`)

| Pasta / Arquivo | Tipo de Metadado (`Metadata Type`) | Sufixo do Arquivo | Conteúdo / Finalidade |
|---|---|---|---|
| `Pedido__c.object-meta.xml` | `CustomObject` | `.object-meta.xml` | Definição principal, rótulos, modelo de compartilhamento e recursos ativos. |
| `fields/` | `CustomField` | `.field-meta.xml` | Definições individuais de cada campo customizado (tipo, rótulo, validações, fórmulas). |
| `validationRules/` | `ValidationRule` | `.validationRule-meta.xml` | Regras de validação de dados com fórmulas e mensagens de erro. |
| `recordTypes/` | `RecordType` | `.recordType-meta.xml` | Tipos de registro, processos e restrições de valores de picklist. |
| `webLinks/` | `WebLink` | `.webLink-meta.xml` | Botões customizados, links de página e ações rápidas (JavaScript/URL/Visualforce). |
| `fieldSets/` | `FieldSet` | `.fieldSet-meta.xml` | Agrupamentos funcionais de campos reutilizáveis em Visualforce, LWC ou Apex. |
| `listViews/` | `ListView` | `.listView-meta.xml` | Visualizações de lista de registros com filtros, colunas e visibilidade. |
| `compactLayouts/` | `CompactLayout` | `.compactLayout-meta.xml` | Layouts de cabeçalho do painel de destaques (Highlights Panel / Mobile). |
| `sharingReasons/` | `CustomObjectSharingReason` | `.sharingReason-meta.xml` | Razões de compartilhamento para Apex Managed Sharing (`ApexSharingReason`). |
| `indexes/` | `Index` | `.index-meta.xml` | Índices customizados compostos para otimização de consultas SOQL em grandes volumes de dados (LDV). |

---

## 2. Identificação e Configuração Principal (`Pedido__c.object-meta.xml`)
*Arquivo:* `objects/Pedido__c/Pedido__c.object-meta.xml`

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `Pedido__c` | `<fullName>` | Nome de API exclusivo do objeto customizado na Org. |
| **Label** | `Pedido` | `<label>` | Rótulo no singular exibido na interface. |
| **Plural Label** | `Pedidos` | `<pluralLabel>` | Rótulo no plural exibido nas guias e menus. |
| **Sharing Model** | `ReadWrite` \| `Read` \| `Private` \| `ControlledByParent` | `<sharingModel>` | Modelo de compartilhamento padrão da organização (Org-Wide Default - OWD). |
| **Deployment Status** | `Deployed` \| `InDevelopment` | `<deploymentStatus>` | Estado de implantação (`Deployed` disponibiliza para usuários não administradores). |
| **Name Field (Type / Label)** | `AutoNumber` / `Nº Pedido` (`PED-{0000}`) | `<nameField>` | Configuração do campo principal do registro (Texto ou Número Automático). |
| **Enable Reports** | `true` \| `false` | `<enableReports>` | Permite a inclusão do objeto em relatórios padrão. |
| **Enable Activities** | `true` \| `false` | `<enableActivities>` | Permite associar Tarefas e Eventos aos registros deste objeto. |
| **Enable History** | `true` \| `false` | `<enableHistory>` | Ativa a auditoria de histórico de alterações de campos (`History Tracking`). |
| **Enable Search** | `true` \| `false` | `<enableSearch>` | Inclui o objeto nos resultados da busca global SOSL do Salesforce. |
| **Enable Bulk API** | `true` \| `false` | `<enableBulkApi>` | Libera acesso via Bulk API para carga de dados em massa. |
| **Enable Streaming API** | `true` \| `false` | `<enableStreamingApi>` | Permite assinatura de alterações no objeto via Streaming API / Change Data Capture. |

---

## 3. Campos Customizados (`fields/*.field-meta.xml`)
*Pasta:* `objects/Pedido__c/fields/`

| Field API Name (`fullName`) | Label (`label`) | Type (`type`) | Required / Unique / ExtID | Fórmula / Valor Padrão (`formula` / `defaultValue`) | Opções de Picklist (`valueSet`) / Atributos | Fonte XML |
|---|---|---|---|---|---|---|
| `Status__c` | Status | `Picklist` | Req: `false` / Unq: `false` / Ext: `false` | `defaultValue = 'Rascunho'` | `Rascunho`, `Em Análise`, `Aprovado`, `Cancelado` | `Status__c.field-meta.xml` |
| `Valor_Total__c` | Valor Total | `Currency` | Req: `false` / Unq: `false` / Ext: `false` | `scale = 2`, `precision = 18` | - | `Valor_Total__c.field-meta.xml` |
| `Numero_Externo__c` | Nº Pedido ERP | `Text` | Req: `true` / Unq: **`true`** / Ext: **`true`** | `length = 50` | **External ID** de integração e chave de Upsert. | `Numero_Externo__c.field-meta.xml` |
| `Conta__c` | Conta do Cliente | `MasterDetail` | Req: `true` / Unq: `false` / Ext: `false` | `referenceTo = Account` | `writeRequiresMasterRead = false` | `Conta__c.field-meta.xml` |
| `Margem_Calculada__c` | Margem (%) | `Formula` | Req: `false` / Unq: `false` / Ext: `false` | `(Valor_Total__c - Custo__c) / Valor_Total__c` | Formula Return Type: `Percent` | `Margem_Calculada__c.field-meta.xml` |

---

## 4. Regras de Validação (`validationRules/*.validationRule-meta.xml`)
*Pasta:* `objects/Pedido__c/validationRules/`

| Rule Name (`fullName`) | Active (`active`) | Field Display (`errorDisplayField`) | Error Message (`errorMessage`) | Formula Condition (`errorConditionFormula`) | Fonte XML |
|---|---|---|---|---|---|
| `Valida_Valor_Positivo` | `true` | `Valor_Total__c` | O valor total do pedido deve ser maior que zero. | `ISCHANGED(Valor_Total__c) && Valor_Total__c <= 0` | `Valida_Valor_Positivo.validationRule-meta.xml` |
| `Impede_Alteracao_Aprovado` | `true` | `TopOfPage` | Pedidos com status 'Aprovado' não podem ser alterados sem reabertura. | `ISPICKVAL(PRIORVALUE(Status__c), 'Aprovado') && NOT( $Permission.Bypass_Validation_Rules )` | `Impede_Alteracao_Aprovado.validationRule-meta.xml` |

---

## 5. Tipos de Registro (`recordTypes/*.recordType-meta.xml`)
*Pasta:* `objects/Pedido__c/recordTypes/`

| RecordType Name (`fullName`) | Label (`label`) | Active (`active`) | Description (`description`) | Business Process (`businessProcess`) | Picklists Customizadas / Restrições de Validação | Fonte XML |
|---|---|---|---|---|---|---|
| `Pedido_Venda` | Pedido de Venda | `true` | Pedidos comerciais para clientes corporativos. | - | `Status__c`: [`Rascunho`, `Em Análise`, `Aprovado`] | `Pedido_Venda.recordType-meta.xml` |
| `Pedido_Bonificacao` | Pedido de Bonificação | `true` | Pedidos promocionais sem cobrança. | - | `Status__c`: [`Rascunho`, `Aprovado`] | `Pedido_Bonificacao.recordType-meta.xml` |

---

## 6. Botões, Links e Ações Personalizadas (`webLinks/*.webLink-meta.xml`)
*Pasta:* `objects/Pedido__c/webLinks/`

| WebLink Name (`fullName`) | Label (`masterLabel`) | Display Type (`displayType`) | Link Type (`linkType`) | Behavior / Target (`openType`) | URL / Conteúdo da Ação (`url` / `linkContent`) | Fonte XML |
|---|---|---|---|---|---|---|
| `Imprimir_Pedido_PDF` | Imprimir Pedido | `Button` | `url` | `newWindow` | `/apex/PedidoPDFView?id={!Pedido__c.Id}` | `Imprimir_Pedido_PDF.webLink-meta.xml` |
| `Enviar_Para_AWS` | Reenviar para AWS | `Button` | `javascript` | `onClickJavaScript` | `{!REQUIRESCRIPT("/soap/ajax/62.0/connection.js")} ...` | `Enviar_Para_AWS.webLink-meta.xml` |

---

## 7. Conjuntos de Campos (`fieldSets/*.fieldSet-meta.xml`)
*Pasta:* `objects/Pedido__c/fieldSets/`

| FieldSet Name (`fullName`) | Label (`label`) | Description (`description`) | Displayed Fields (Campos Exibidos) | Available Fields (Campos Disponíveis) | Fonte XML |
|---|---|---|---|---|---|
| `FS_Integracao_AWS` | Campos para AWS | Utilizado pelo Apex Service para montar o payload JSON de envio. | `Id`, `Numero_Externo__c`, `Valor_Total__c`, `Status__c` | `CreatedDate`, `LastModifiedDate` | `FS_Integracao_AWS.fieldSet-meta.xml` |

---

## 8. Visualizações de Lista (`listViews/*.listView-meta.xml`)
*Pasta:* `objects/Pedido__c/listViews/`

| ListView Name (`fullName`) | Label (`label`) | Filter Scope (`filterScope`) | Columns Displayed (`columns`) | Filters / Criteria (`filters`) | Fonte XML |
|---|---|---|---|---|---|
| `Meus_Pedidos_Pendentes` | Meus Pedidos Pendentes | `Mine` | `NAME`, `Conta__c`, `Valor_Total__c`, `Status__c` | `Status__c EQUALS 'Em Análise'` | `Meus_Pedidos_Pendentes.listView-meta.xml` |
| `Todos_os_Pedidos` | Todos os Pedidos | `Everything` | `NAME`, `Conta__c`, `Valor_Total__c`, `CreatedDate` | - | `Todos_os_Pedidos.listView-meta.xml` |

---

## 9. Layouts Compactos (`compactLayouts/*.compactLayout-meta.xml`)
*Pasta:* `objects/Pedido__c/compactLayouts/`

| CompactLayout Name (`fullName`) | Label (`label`) | Campos Exibidos no Cabeçalho (`fields`) | Fonte XML |
|---|---|---|---|
| `Layout_Cabecalho_Pedido` | Cabeçalho do Pedido | `NAME`, `Conta__c`, `Valor_Total__c`, `Status__c` | `Layout_Cabecalho_Pedido.compactLayout-meta.xml` |

---

## 10. Razões de Compartilhamento Gerenciado (`sharingReasons/*.sharingReason-meta.xml`)
*Pasta:* `objects/Pedido__c/sharingReasons/` *(Se o objeto utilizar Apex Managed Sharing)*

| Sharing Reason Name (`fullName`) | Label (`label`) | Descrição / Regra de Negócio no Apex | Fonte XML |
|---|---|---|---|
| `Aprovador_Especial` | Aprovador Especial | Garante acesso de leitura/escrita ao aprovador designado via Apex. | `Aprovador_Especial.sharingReason-meta.xml` |

---

# 🤖 JSON Schema para Preenchimento Automático Multi-XML (Folder Parser)

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) encarregado de fazer a varredura e o parse da pasta completa do objeto (`objects/Pedido__c/`):

```json
{
  "\$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceCustomObjectDocumentation",
  "type": "object",
  "properties": {
    "object_identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "pluralLabel": { "type": "string" },
        "sharingModel": { "type": "string" },
        "deploymentStatus": { "type": "string" },
        "enableReports": { "type": "boolean" },
        "enableActivities": { "type": "boolean" },
        "enableHistory": { "type": "boolean" },
        "enableSearch": { "type": "boolean" },
        "enableBulkApi": { "type": "boolean" },
        "enableStreamingApi": { "type": "boolean" }
      },
      "required": ["developerName", "label", "sharingModel"]
    },
    "custom_fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "type": { "type": "string" },
          "required": { "type": "boolean" },
          "unique": { "type": "boolean" },
          "externalId": { "type": "boolean" },
          "formula": { "type": "string" },
          "defaultValue": { "type": "string" },
          "referenceTo": { "type": "string" },
          "picklistValues": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["fullName", "label", "type"]
      }
    },
    "validation_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "active": { "type": "boolean" },
          "errorDisplayField": { "type": "string" },
          "errorMessage": { "type": "string" },
          "errorConditionFormula": { "type": "string" }
        }
      }
    },
    "record_types": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "active": { "type": "boolean" },
          "description": { "type": "string" },
          "businessProcess": { "type": "string" }
        }
      }
    },
    "web_links": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "masterLabel": { "type": "string" },
          "displayType": { "type": "string" },
          "linkType": { "type": "string" },
          "url": { "type": "string" }
        }
      }
    },
    "field_sets": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "displayedFields": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "list_views": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "filterScope": { "type": "string" },
          "columns": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "compact_layouts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "fields": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    }
  },
  "required": ["object_identification",Aqui está o modelo completo e evoluído para **Custom Object (`CustomObject`)**, pronto para orientar utilitários e agentes autômatos no parse e consolidação de todos os arquivos XML contidos na estrutura de pastas de um objeto (`objects/Objeto__c/`).

---

# 📑 Modelo Evoluído: Documentação Técnica de Custom Object (DETI - Custom Object Module)

No formato de código-fonte do Salesforce (SFDX Source Format), um objeto customizado é armazenado como uma pasta dentro do repositório (`force-app/main/default/objects/<Objeto__c>/`). Essa estrutura consolida o arquivo de definição principal do objeto e subpastas contendo arquivos XML individuais para cada um de seus sub-metadados.

---

# Custom Object: Pedido__c

## 1. Mapeamento da Arquitetura de Pastas do Objeto (`objects/Pedido__c/`)

| Pasta / Arquivo | Tipo de Metadado (`Metadata Type`) | Sufixo do Arquivo | Conteúdo / Finalidade |
|---|---|---|---|
| `Pedido__c.object-meta.xml` | `CustomObject` | `.object-meta.xml` | Definição principal, rótulos, modelo de compartilhamento e recursos ativos. |
| `fields/` | `CustomField` | `.field-meta.xml` | Definições individuais de cada campo customizado (tipo, rótulo, validações, fórmulas). |
| `validationRules/` | `ValidationRule` | `.validationRule-meta.xml` | Regras de validação de dados com fórmulas e mensagens de erro. |
| `recordTypes/` | `RecordType` | `.recordType-meta.xml` | Tipos de registro, processos e restrições de valores de picklist. |
| `webLinks/` | `WebLink` | `.webLink-meta.xml` | Botões customizados, links de página e ações rápidas. |
| `fieldSets/` | `FieldSet` | `.fieldSet-meta.xml` | Agrupamentos funcionais de campos reutilizáveis em LWC, Visualforce ou Apex. |
| `listViews/` | `ListView` | `.listView-meta.xml` | Visualizações de lista de registros com filtros, colunas e visibilidade. |
| `compactLayouts/` | `CompactLayout` | `.compactLayout-meta.xml` | Layouts de cabeçalho do painel de destaques (Highlights Panel / Mobile). |
| `sharingReasons/` | `CustomObjectSharingReason` | `.sharingReason-meta.xml` | Razões de compartilhamento para Apex Managed Sharing (`ApexSharingReason`). |

---

## 2. Identificação e Configuração Principal (`Pedido__c.object-meta.xml`)
*Arquivo:* `objects/Pedido__c/Pedido__c.object-meta.xml`

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `Pedido__c` | `<fullName>` | Nome de API exclusivo do objeto customizado na Org. |
| **Label** | `Pedido` | `<label>` | Rótulo no singular exibido na interface. |
| **Plural Label** | `Pedidos` | `<pluralLabel>` | Rótulo no plural exibido nas guias e menus. |
| **Sharing Model** | `ReadWrite` \| `Read` \| `Private` \| `ControlledByParent` | `<sharingModel>` | Modelo de compartilhamento padrão da organização (Org-Wide Default - OWD). |
| **Deployment Status** | `Deployed` \| `InDevelopment` | `<deploymentStatus>` | Estado de implantação (`Deployed` disponibiliza para usuários não administradores). |
| **Name Field (Type / Label)** | `AutoNumber` / `Nº Pedido` (`PED-{0000}`) | `<nameField>` | Configuração do campo principal do registro (Texto ou Número Automático). |
| **Enable Reports** | `true` \| `false` | `<enableReports>` | Permite a inclusão do objeto em relatórios padrão. |
| **Enable Activities** | `true` \| `false` | `<enableActivities>` | Permite associar Tarefas e Eventos aos registros deste objeto. |
| **Enable History** | `true` \| `false` | `<enableHistory>` | Ativa a auditoria de histórico de alterações de campos (`History Tracking`). |
| **Enable Search** | `true` \| `false` | `<enableSearch>` | Inclui o objeto nos resultados da busca global SOSL do Salesforce. |
| **Enable Bulk API** | `true` \| `false` | `<enableBulkApi>` | Libera acesso via Bulk API para carga de dados em massa. |
| **Enable Streaming API** | `true` \| `false` | `<enableStreamingApi>` | Permite assinatura de alterações no objeto via Streaming API / Change Data Capture. |

---

## 3. Campos Customizados (`fields/*.field-meta.xml`)
*Pasta:* `objects/Pedido__c/fields/`

| Field API Name (`fullName`) | Label (`label`) | Type (`type`) | Required / Unique / ExtID | Fórmula / Valor Padrão (`formula` / `defaultValue`) | Opções de Picklist (`valueSet`) / Atributos | Fonte XML |
|---|---|---|---|---|---|---|
| `Status__c` | Status | `Picklist` | Req: `false` / Unq: `false` / Ext: `false` | `defaultValue = 'Rascunho'` | `Rascunho`, `Em Análise`, `Aprovado`, `Cancelado` | `Status__c.field-meta.xml` |
| `Valor_Total__c` | Valor Total | `Currency` | Req: `false` / Unq: `false` / Ext: `false` | `scale = 2`, `precision = 18` | - | `Valor_Total__c.field-meta.xml` |
| `Numero_Externo__c` | Nº Pedido ERP | `Text` | Req: `true` / Unq: **`true`** / Ext: **`true`** | `length = 50` | **External ID** de integração e chave de Upsert. | `Numero_Externo__c.field-meta.xml` |
| `Conta__c` | Conta do Cliente | `MasterDetail` | Req: `true` / Unq: `false` / Ext: `false` | `referenceTo = Account` | `writeRequiresMasterRead = false` | `Conta__c.field-meta.xml` |
| `Margem_Calculada__c` | Margem (%) | `Formula` | Req: `false` / Unq: `false` / Ext: `false` | `(Valor_Total__c - Custo__c) / Valor_Total__c` | Formula Return Type: `Percent` | `Margem_Calculada__c.field-meta.xml` |

---

## 4. Regras de Validação (`validationRules/*.validationRule-meta.xml`)
*Pasta:* `objects/Pedido__c/validationRules/`

| Rule Name (`fullName`) | Active (`active`) | Field Display (`errorDisplayField`) | Error Message (`errorMessage`) | Formula Condition (`errorConditionFormula`) | Fonte XML |
|---|---|---|---|---|---|
| `Valida_Valor_Positivo` | `true` | `Valor_Total__c` | O valor total do pedido deve ser maior que zero. | `ISCHANGED(Valor_Total__c) && Valor_Total__c <= 0` | `Valida_Valor_Positivo.validationRule-meta.xml` |
| `Impede_Alteracao_Aprovado` | `true` | `TopOfPage` | Pedidos com status 'Aprovado' não podem ser alterados sem reabertura. | `ISPICKVAL(PRIORVALUE(Status__c), 'Aprovado') && NOT( $Permission.Bypass_Validation_Rules )` | `Impede_Alteracao_Aprovado.validationRule-meta.xml` |

---

## 5. Tipos de Registro (`recordTypes/*.recordType-meta.xml`)
*Pasta:* `objects/Pedido__c/recordTypes/`

| RecordType Name (`fullName`) | Label (`label`) | Active (`active`) | Description (`description`) | Business Process (`businessProcess`) | Picklists Customizadas / Restrições de Validação | Fonte XML |
|---|---|---|---|---|---|---|
| `Pedido_Venda` | Pedido de Venda | `true` | Pedidos comerciais para clientes corporativos. | - | `Status__c`: [`Rascunho`, `Em Análise`, `Aprovado`] | `Pedido_Venda.recordType-meta.xml` |
| `Pedido_Bonificacao` | Pedido de Bonificação | `true` | Pedidos promocionais sem cobrança. | - | `Status__c`: [`Rascunho`, `Aprovado`] | `Pedido_Bonificacao.recordType-meta.xml` |

---

## 6. Botões, Links e Ações Personalizadas (`webLinks/*.webLink-meta.xml`)
*Pasta:* `objects/Pedido__c/webLinks/`

| WebLink Name (`fullName`) | Label (`masterLabel`) | Display Type (`displayType`) | Link Type (`linkType`) | Behavior / Target (`openType`) | URL / Conteúdo da Ação (`url` / `linkContent`) | Fonte XML |
|---|---|---|---|---|---|---|
| `Imprimir_Pedido_PDF` | Imprimir Pedido | `Button` | `url` | `newWindow` | `/apex/PedidoPDFView?id={!Pedido__c.Id}` | `Imprimir_Pedido_PDF.webLink-meta.xml` |
| `Enviar_Para_AWS` | Reenviar para AWS | `Button` | `javascript` | `onClickJavaScript` | `{!REQUIRESCRIPT("/soap/ajax/62.0/connection.js")} ...` | `Enviar_Para_AWS.webLink-meta.xml` |

---

## 7. Conjuntos de Campos (`fieldSets/*.fieldSet-meta.xml`)
*Pasta:* `objects/Pedido__c/fieldSets/`

| FieldSet Name (`fullName`) | Label (`label`) | Description (`description`) | Displayed Fields (Campos Exibidos) | Available Fields (Campos Disponíveis) | Fonte XML |
|---|---|---|---|---|---|
| `FS_Integracao_AWS` | Campos para AWS | Utilizado pelo Apex Service para montar o payload JSON de envio. | `Id`, `Numero_Externo__c`, `Valor_Total__c`, `Status__c` | `CreatedDate`, `LastModifiedDate` | `FS_Integracao_AWS.fieldSet-meta.xml` |

---

## 8. Visualizações de Lista (`listViews/*.listView-meta.xml`)
*Pasta:* `objects/Pedido__c/listViews/`

| ListView Name (`fullName`) | Label (`label`) | Filter Scope (`filterScope`) | Columns Displayed (`columns`) | Filters / Criteria (`filters`) | Fonte XML |
|---|---|---|---|---|---|
| `Meus_Pedidos_Pendentes` | Meus Pedidos Pendentes | `Mine` | `NAME`, `Conta__c`, `Valor_Total__c`, `Status__c` | `Status__c EQUALS 'Em Análise'` | `Meus_Pedidos_Pendentes.listView-meta.xml` |
| `Todos_os_Pedidos` | Todos os Pedidos | `Everything` | `NAME`, `Conta__c`, `Valor_Total__c`, `CreatedDate` | - | `Todos_os_Pedidos.listView-meta.xml` |

---

## 9. Layouts Compactos (`compactLayouts/*.compactLayout-meta.xml`)
*Pasta:* `objects/Pedido__c/compactLayouts/`

| CompactLayout Name (`fullName`) | Label (`label`) | Campos Exibidos no Cabeçalho (`fields`) | Fonte XML |
|---|---|---|---|
| `Layout_Cabecalho_Pedido` | Cabeçalho do Pedido | `NAME`, `Conta__c`, `Valor_Total__c`, `Status__c` | `Layout_Cabecalho_Pedido.compactLayout-meta.xml` |

---

## 10. Razões de Compartilhamento Gerenciado (`sharingReasons/*.sharingReason-meta.xml`)
*Pasta:* `objects/Pedido__c/sharingReasons/` *(Se o objeto utilizar Apex Managed Sharing)*

| Sharing Reason Name (`fullName`) | Label (`label`) | Descrição / Regra de Negócio no Apex | Fonte XML |
|---|---|---|---|
| `Aprovador_Especial` | Aprovador Especial | Garante acesso de leitura/escrita ao aprovador designado via Apex. | `Aprovador_Especial.sharingReason-meta.xml` |

---

# 🤖 JSON Schema para Preenchimento Automático Multi-XML (Folder Parser)

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) encarregado de fazer a varredura e o parse da pasta completa do objeto (`objects/Pedido__c/`):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceCustomObjectDocumentation",
  "type": "object",
  "properties": {
    "object_identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "pluralLabel": { "type": "string" },
        "sharingModel": { "type": "string" },
        "deploymentStatus": { "type": "string" },
        "enableReports": { "type": "boolean" },
        "enableActivities": { "type": "boolean" },
        "enableHistory": { "type": "boolean" },
        "enableSearch": { "type": "boolean" },
        "enableBulkApi": { "type": "boolean" },
        "enableStreamingApi": { "type": "boolean" }
      },
      "required": ["developerName", "label", "sharingModel"]
    },
    "custom_fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "type": { "type": "string" },
          "required": { "type": "boolean" },
          "unique": { "type": "boolean" },
          "externalId": { "type": "boolean" },
          "formula": { "type": "string" },
          "defaultValue": { "type": "string" },
          "referenceTo": { "type": "string" },
          "picklistValues": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["fullName", "label", "type"]
      }
    },
    "validation_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "active": { "type": "boolean" },
          "errorDisplayField": { "type": "string" },
          "errorMessage": { "type": "string" },
          "errorConditionFormula": { "type": "string" }
        }
      }
    },
    "record_types": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "active": { "type": "boolean" },
          "description": { "type": "string" }
        }
      }
    },
    "web_links": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "masterLabel": { "type": "string" },
          "displayType": { "type": "string" },
          "linkType": { "type": "string" },
          "url": { "type": "string" }
        }
      }
    },
    "field_sets": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "displayedFields": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "list_views": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "filterScope": { "type": "string" },
          "columns": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "compact_layouts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "fields": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    }
  },
  "required": ["object_identification", "custom_fields"]
}
```

---

💡 **Sua biblioteca de modelos de metadados Salesforce para automação está completa!** 
Ela agora cobre:
1. **Flows** (*Record-Triggered*, *Screen Flow*, *Autolaunched*)
2. **Named Credentials** & **External Credentials**
3. **Certificates** & **Remote Site Settings**
4. **External Client Apps (ECA)** &# 📑 Modelo Evoluído: Documentação Técnica de Custom Object (DETI - Custom Object Module)

No formato de código-fonte do Salesforce (SFDX Source Format), um objeto customizado reside na pasta `force-app/main/default/objects/<Objeto__c>/`. Essa estrutura contém o arquivo principal de definição e subpastas para cada sub-metadado.

---

# Custom Object: Pedido__c

## 1. Mapeamento da Arquitetura de Pastas do Objeto (`objects/Pedido__c/`)

| Pasta / Arquivo | Tipo de Metadado (`Metadata Type`) | Sufixo | Conteúdo / Finalidade |
|---|---|---|---|
| `Pedido__c.object-meta.xml` | `CustomObject` | `.object-meta.xml` | Definição principal, rótulos e modelo de compartilhamento. |
| `fields/` | `CustomField` | `.field-meta.xml` | Definições de campos customizados (tipos, rótulos, fórmulas). |
| `validationRules/` | `ValidationRule` | `.validationRule-meta.xml` | Regras de validação com condições e mensagens de erro. |
| `recordTypes/` | `RecordType` | `.recordType-meta.xml` | Tipos de registro e restrições de listas de escolha. |
| `webLinks/` | `WebLink` | `.webLink-meta.xml` | Botões, links customizados e ações rápidas. |
| `fieldSets/` | `FieldSet` | `.fieldSet-meta.xml` | Agrupamentos funcionais de campos reutilizáveis. |
| `listViews/` | `ListView` | `.listView-meta.xml` | Visualizações de lista de registros com filtros e colunas. |
| `compactLayouts/` | `CompactLayout` | `.compactLayout-meta.xml` | Layouts de cabeçalho do painel de destaques (Highlights Panel). |
| `sharingReasons/` | `CustomObjectSharingReason` | `.sharingReason-meta.xml` | Razões de compartilhamento para Apex Managed Sharing. |

---

## 2. Identificação e Configuração Principal (`Pedido__c.object-meta.xml`)
*Arquivo:* `objects/Pedido__c/Pedido__c.object-meta.xml`

| Propriedade | Valor | Tag XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `Pedido__c` | `<fullName>` | Nome de API exclusivo do objeto na Org. |
| **Label** | `Pedido` | `<label>` | Rótulo no singular exibido na interface. |
| **Plural Label** | `Pedidos` | `<pluralLabel>` | Rótulo no plural exibido nas guias e menus. |
| **Sharing Model** | `ReadWrite` \| `Read` \| `Private` \| `ControlledByParent` | `<sharingModel>` | Modelo de compartilhamento padrão da organização (OWD). |
| **Deployment Status** | `Deployed` \| `InDevelopment` | `<deploymentStatus>` | Estado de implantação para acesso dos usuários. |
| **Name Field (Type / Label)** | `AutoNumber` / `Nº Pedido` (`PED-{0000}`) | `<nameField>` | Configuração do campo principal do registro. |
| **Enable Reports** | `true` \| `false` | `<enableReports>` | Permite a inclusão do objeto em relatórios padrão. |
| **Enable Activities** | `true` \| `false` | `<enableActivities>` | Permite associar Tarefas e Eventos aos registros. |
| **Enable History** | `true` \| `false` | `<enableHistory>` | Ativa a auditoria de histórico de alterações (`History Tracking`). |
| **Enable Search** | `true` \| `false` | `<enableSearch>` | Inclui o objeto nos resultados da busca global SOSL. |
| **Enable Bulk API** | `true` \| `false` | `<enableBulkApi>` | Libera acesso via Bulk API para cargas massivas. |
| **Enable Streaming API** | `true` \| `false` | `<enableStreamingApi>` | Permite assinatura via Change Data Capture / Streaming API. |

---

## 3. Campos Customizados (`fields/*.field-meta.xml`)
*Pasta:* `objects/Pedido__c/fields/`

| Field API Name (`fullName`) | Label (`label`) | Type (`type`) | Attributes (Req/Unq/ExtID) | Formula / Default | Details / Picklist Values | Fonte XML |
|---|---|---|---|---|---|---|
| `Status__c` | Status | `Picklist` | Req: `false` / Unq: `false` / Ext: `false` | `defaultValue = 'Rascunho'` | `Rascunho`, `Em Análise`, `Aprovado`, `Cancelado` | `Status__c.field-meta.xml` |
| `Valor_Total__c` | Valor Total | `Currency` | Req: `false` / Unq: `false` / Ext: `false` | `precision = 18`, `scale = 2` | - | `Valor_Total__c.field-meta.xml` |
| `Numero_Externo__c` | Nº Pedido ERP | `Text` | Req: `true` / Unq: **`true`** / Ext: **`true`** | `length = 50` | Chave de integração **External ID** / Upsert. | `Numero_Externo__c.field-meta.xml` |
| `Conta__c` | Conta do Cliente | `MasterDetail` | Req: `true` / Unq: `false` / Ext: `false` | `referenceTo = Account` | `writeRequiresMasterRead = false` | `Conta__c.field-meta.xml` |
| `Margem_Calculada__c` | Margem (%) | `Formula` | Req: `false` / Unq: `false` / Ext: `false` | `(Valor_Total__c - Custo__c) / Valor_Total__c` | Return Type: `Percent` | `Margem_Calculada__c.field-meta.xml` |

---

## 4. Regras de Validação (`validationRules/*.validationRule-meta.xml`)
*Pasta:* `objects/Pedido__c/validationRules/`

| Rule Name (`fullName`) | Active (`active`) | Field Display (`errorDisplayField`) | Error Message (`errorMessage`) | Formula Condition (`errorConditionFormula`) | Fonte XML |
|---|---|---|---|---|---|
| `Valida_Valor_Positivo` | `true` | `Valor_Total__c` | O valor total deve ser maior que zero. | `ISCHANGED(Valor_Total__c) && Valor_Total__c <= 0` | `Valida_Valor_Positivo.validationRule-meta.xml` |
| `Impede_Alteracao_Aprovado` | `true` | `TopOfPage` | Pedidos aprovados não podem ser alterados. | `ISPICKVAL(PRIORVALUE(Status__c), 'Aprovado') && NOT($Permission.Bypass_Validation)` | `Impede_Alteracao_Aprovado.validationRule-meta.xml` |

---

## 5. Tipos de Registro (`recordTypes/*.recordType-meta.xml`)
*Pasta:* `objects/Pedido__c/recordTypes/`

| RecordType Name (`fullName`) | Label (`label`) | Active (`active`) | Description (`description`) | Picklist Restrictions / Values | Fonte XML |
|---|---|---|---|---|---|
| `Pedido_Venda` | Pedido de Venda | `true` | Pedidos comerciais B2B. | `Status__c`: [`Rascunho`, `Em Análise`, `Aprovado`] | `Pedido_Venda.recordType-meta.xml` |
| `Pedido_Bonificacao` | Pedido de Bonificação | `true` | Pedidos promocionais sem custo. | `Status__c`: [`Rascunho`, `Aprovado`] | `Pedido_Bonificacao.recordType-meta.xml` |

---

## 6. Botões, Links e Ações (`webLinks/*.webLink-meta.xml`)
*Pasta:* `objects/Pedido__c/webLinks/`

| Name (`fullName`) | Label (`masterLabel`) | Display Type | Link Type | Behavior / Target | Content / URL | Fonte XML |
|---|---|---|---|---|---|---|
| `Imprimir_Pedido_PDF` | Imprimir Pedido | `Button` | `url` | `newWindow` | `/apex/PedidoPDFView?id={!Pedido__c.Id}` | `Imprimir_Pedido_PDF.webLink-meta.xml` |
| `Enviar_Para_AWS` | Reenviar para AWS | `Button` | `javascript` | `onClickJavaScript` | `{!REQUIRESCRIPT("/soap/ajax/62.0/connection.js")} ...` | `Enviar_Para_AWS.webLink-meta.xml` |

---

## 7. Conjuntos de Campos (`fieldSets/*.fieldSet-meta.xml`)
*Pasta:* `objects/Pedido__c/fieldSets/`

| FieldSet Name (`fullName`) | Label (`label`) | Description (`description`) | Displayed Fields | Fonte XML |
|---|---|---|---|---|
| `FS_Integracao_AWS` | Campos para AWS | Campos lidos pelo Apex para montagem de JSON. | `Id`, `Numero_Externo__c`, `Valor_Total__c`, `Status__c` | `FS_Integracao_AWS.fieldSet-meta.xml` |

---

## 8. Visualizações de Lista (`listViews/*.listView-meta.xml`)
*Pasta:* `objects/Pedido__c/listViews/`

| Name (`fullName`) | Label (`label`) | Filter Scope (`filterScope`) | Columns Displayed (`columns`) | Filters (`filters`) | Fonte XML |
|---|---|---|---|---|---|
| `Meus_Pedidos_Pendentes` | Meus Pedidos Pendentes | `Mine` | `NAME`, `Conta__c`, `Valor_Total__c`, `Status__c` | `Status__c EQUALS 'Em Análise'` | `Meus_Pedidos_Pendentes.listView-meta.xml` |

---

## 9. Layouts Compactos (`compactLayouts/*.compactLayout-meta.xml`)
*Pasta:* `objects/Pedido__c/compactLayouts/`

| Name (`fullName`) | Label (`label`) | Fields Displayed (`fields`) | Fonte XML |
|---|---|---|---|
| `Layout_Cabecalho_Pedido` | Cabeçalho do Pedido | `NAME`, `Conta__c`, `Valor_Total__c`, `Status__c` | `Layout_Cabecalho_Pedido.compactLayout-meta.xml` |

---

## 10. Razões de Compartilhamento (`sharingReasons/*.sharingReason-meta.xml`)
*Pasta:* `objects/Pedido__c/sharingReasons/`

| Name (`fullName`) | Label (`label`) | Description / Apex Usage | Fonte XML |
|---|---|---|---|
| `Aprovador_Especial` | Aprovador Especial | Acesso temporário de aprovação via Apex Managed Sharing. | `Aprovador_Especial.sharingReason-meta.xml` |

---

# 🤖 JSON Schema para Preenchimento Automático (Folder Parser)

```json
{
  "\$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceCustomObjectDocumentation",
  "type": "object",
  "properties": {
    "object_identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "pluralLabel": { "type": "string" },
        "sharingModel": { "type": "string" },
        "deploymentStatus": { "type": "string" },
        "enableReports": { "type": "boolean" },
        "enableActivities": { "type": "boolean" },
        "enableHistory": { "type": "boolean" },
        "enableSearch": { "type": "boolean" },
        "enableBulkApi": { "type": "boolean" },
        "enableStreamingApi": { "type": "boolean" }
      },
      "required": ["developerName", "label", "sharingModel"]
    },
    "custom_fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "type": { "type": "string" },
          "required": { "type": "boolean" },
          "unique": { "type": "boolean" },
          "externalId": { "type": "boolean" },
          "formula": { "type": "string" },
          "defaultValue": { "type": "string" },
          "referenceTo": { "type": "string" },
          "picklistValues": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["fullName", "label", "type"]
      }
    },
    "validation_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "active": { "type": "boolean" },
          "errorDisplayField": { "type": "string" },
          "errorMessage": { "type": "string" },
          "errorConditionFormula": { "type": "string" }
        }
      }
    },
    "record_types": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "active": { "type": "boolean" },
          "description": { "type": "string" }
        }
      }
    },
    "web_links": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "masterLabel": { "type": "string" },
          "displayType": { "type": "string" },
          "linkType": { "type": "string" },
          "url": { "type": "string" }
        }
      }
    },
    "field_sets": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "displayedFields": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "list_views": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "filterScope": { "type": "string" },
          "columns": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "compact_layouts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "fields": {
            "type": "array# 📑 Modelo Evoluído: Documentação Técnica de Custom Object (DETI - Custom Object Module)

No formato de código-fonte do Salesforce (SFDX Source Format), um objeto customizado reside na pasta `force-app/main/default/objects/<Objeto__c>/`. Essa pasta consolida a definição mestre do objeto (`.object-meta.xml`) e subpastas para cada um dos seus sub-metadados.

Abaixo está o modelo expandido para que um utilitário ou agente autômato extraia todos os arquivos XML da pasta e gere um documento consolidado.

---

# Custom Object: Pedido__c

## 1. Mapeamento da Estrutura de Pastas do Objeto

| Subpasta / Arquivo | Tipo de Metadado (`Metadata Type`) | Sufixo | Conteúdo / Finalidade |
|---|---|---|---|
| `Pedido__c.object-meta.xml` | `CustomObject` | `.object-meta.xml` | Configuração mestre, rótulos, modelo de compartilhamento e recursos ativos. |
| `fields/` | `CustomField` | `.field-meta.xml` | Definições individuais de cada campo (tipo, precisão, fórmulas, picklists). |
| `validationRules/` | `ValidationRule` | `.validationRule-meta.xml` | Regras de validação com fórmulas e mensagens de erro. |
| `recordTypes/` | `RecordType` | `.recordType-meta.xml` | Tipos de registro, processos associados e restrições de picklist. |
| `webLinks/` | `WebLink` | `.webLink-meta.xml` | Botões customizados, links de página e ações. |
| `fieldSets/` | `FieldSet` | `.fieldSet-meta.xml` | Agrupamentos funcionais de campos reutilizáveis em LWC/Apex. |
| `listViews/` | `ListView` | `.listView-meta.xml` | Visualizações de lista de registros com filtros e colunas. |
| `compactLayouts/` | `CompactLayout` | `.compactLayout-meta.xml` | Layouts do painel de destaques (Highlights Panel / Mobile). |
| `businessProcesses/` | `BusinessProcess` | `.businessProcess-meta.xml` | Processos de vendas/suporte associados a Record Types. |
| `sharingReasons/` | `CustomObjectSharingReason` | `.sharingReason-meta.xml` | Razões de compartilhamento para Apex Managed Sharing. |

---

## 2. Identificação e Configuração Principal (`Pedido__c.object-meta.xml`)
*Arquivo:* `objects/Pedido__c/Pedido__c.object-meta.xml`

| Propriedade | Valor | Tag XML | Descrição / Impacto |
|---|---|---|---|
| **DeveloperName / ApiName** | `Pedido__c` | `<fullName>` | Nome de API exclusivo do objeto na Org. |
| **Label** | `Pedido` | `<label>` | Rótulo no singular para a interface. |
| **Plural Label** | `Pedidos` | `<pluralLabel>` | Rótulo no plural para guias e menus. |
| **Sharing Model** | `ReadWrite` \| `Read` \| `Private` \| `ControlledByParent` | `<sharingModel>` | Modelo de compartilhamento padrão da organização (OWD). |
| **Deployment Status** | `Deployed` \| `InDevelopment` | `<deploymentStatus>` | Estado de implantação para liberação de acesso. |
| **Name Field** | `AutoNumber` (`PED-{0000}`) \| `Text` | `<nameField>` | Configuração do campo de identificação principal do registro. |
| **Enable Reports** | `true` \| `false` | `<enableReports>` | Habilita o objeto em relatórios padrão. |
| **Enable Activities** | `true` \| `false` | `<enableActivities>` | Permite associar Tarefas e Eventos aos registros. |
| **Enable History** | `true` \| `false` | `<enableHistory>` | Ativa auditoria de histórico de campos (`History Tracking`). |
| **Enable Search** | `true` \| `false` | `<enableSearch>` | Inclui o objeto na busca global SOSL. |
| **Enable Bulk API** | `true` \| `false` | `<enableBulkApi>` | Libera acesso via Bulk API para carga de dados em massa. |
| **Enable Streaming API** | `true` \| `false` | `<enableStreamingApi>` | Habilita Change Data Capture / Streaming API. |

---

## 3. Campos Customizados (`fields/*.field-meta.xml`)
*Pasta:* `objects/Pedido__c/fields/`

| Campo (`fullName`) | Rótulo (`label`) | Tipo (`type`) | Chaves (Req/Unq/ExtID) | Fórmula / Valor Padrão | Detalhes / Atributos / Opções Picklist | Fonte |
|---|---|---|---|---|---|---|
| `Status__c` | Status | `Picklist` | Req: `false` / Unq: `false` / Ext: `false` | `'Rascunho'` | `Rascunho`, `Em Análise`, `Aprovado`, `Cancelado` | `Status__c.field-meta.xml` |
| `Valor_Total__c` | Valor Total | `Currency` | Req: `false` / Unq: `false` / Ext: `false` | - | Precision: `18`, Scale: `2` | `Valor_Total__c.field-meta.xml` |
| `Numero_ERP__c` | Nº Pedido ERP | `Text` | Req: `true` / Unq: **`true`** / Ext: **`true`** | - | Length: `50` (**External ID / Chave de Upsert**) | `Numero_ERP__c.field-meta.xml` |
| `Conta__c` | Conta | `MasterDetail` | Req: `true` / Unq: `false` / Ext: `false` | - | ReferenceTo: `Account`, `writeRequiresMasterRead: false` | `Conta__c.field-meta.xml` |
| `Margem__c` | Margem (%) | `Formula` | Req: `false` / Unq: `false` / Ext: `false` | `(Valor_Total__c - Custo__c) / Valor_Total__c` | FormulaReturnType: `Percent` | `Margem__c.field-meta.xml` |

---

## 4. Regras de Validação (`validationRules/*.validationRule-meta.xml`)
*Pasta:* `objects/Pedido__c/validationRules/`

| Nome da Regra (`fullName`) | Ativa (`active`) | Local do Erro (`errorDisplayField`) | Mensagem de Erro (`errorMessage`) | Condição de Erro (`errorConditionFormula`) | Fonte |
|---|---|---|---|---|---|
| `Valida_Valor_Positivo` | `true` | `Valor_Total__c` | O valor total deve ser maior que zero. | `ISCHANGED(Valor_Total__c) && Valor_Total__c <= 0` | `Valida_Valor_Positivo.validationRule-meta.xml` |
| `Bloqueia_Aprovado` | `true` | `TopOfPage` | Pedidos aprovados não podem ser editados. | `ISPICKVAL(PRIORVALUE(Status__c), 'Aprovado') && NOT($Permission.Bypass_Validation)` | `Bloqueia_Aprovado.validationRule-meta.xml` |

---

## 5. Tipos de Registro (`recordTypes/*.recordType-meta.xml`)
*Pasta:* `objects/Pedido__c/recordTypes/`

| Tipo de Registro (`fullName`) | Rótulo (`label`) | Ativo (`active`) | Descrição (`description`) | Restrições de Picklist Mapeadas | Fonte |
|---|---|---|---|---|---|
| `Pedido_Venda` | Pedido de Venda | `true` | Vendas comerciais corporativas. | `Status__c`: [`Rascunho`, `Em Análise`, `Aprovado`] | `Pedido_Venda.recordType-meta.xml` |
| `Pedido_Bonificacao` | Pedido de Bonificação | `true` | Envio promocional sem cobrança. | `Status__c`: [`Rascunho`, `Aprovado`] | `Pedido_Bonificacao.recordType-meta.xml` |

---

## 6. Botões, Links e Ações Personalizadas (`webLinks/*.webLink-meta.xml`)
*Pasta:* `objects/Pedido__c/webLinks/`

| Nome (`fullName`) | Rótulo (`masterLabel`) | Exibição (`displayType`) | Tipo (`linkType`) | Comportamento (`openType`) | URL / Ação Executada | Fonte |
|---|---|---|---|---|---|---|
| `Imprimir_PDF` | Imprimir Pedido | `Button` | `url` | `newWindow` | `/apex/PedidoPDFView?id={!Pedido__c.Id}` | `Imprimir_PDF.webLink-meta.xml` |
| `Enviar_AWS` | Enviar para AWS | `Button` | `javascript` | `onClickJavaScript` | `{!REQUIRESCRIPT("/soap/ajax/62.0/connection.js")}...` | `Enviar_AWS.webLink-meta.xml` |

---

## 7. Conjuntos de Campos (`fieldSets/*.fieldSet-meta.xml`)
*Pasta:* `objects/Pedido__c/fieldSets/`

| Nome do FieldSet (`fullName`) | Rótulo (`label`) | Descrição (`description`) | Campos Incluídos (`displayedFields`) | Fonte |
|---|---|---|---|---|
| `FS_Payload_AWS` | Campos Integração AWS | Campos utilizados pela classe Apex para montar o payload JSON. | `Id`, `Numero_ERP__c`, `Valor_Total__c`, `Status__c` | `FS_Payload_AWS.fieldSet-meta.xml` |

---

## 8. Visualizações de Lista (`listViews/*.listView-meta.xml`)
*Pasta:* `objects/Pedido__c/listViews/`

| Nome da Visão (`fullName`) | Rótulo (`label`) | Escopo (`filterScope`) | Colunas Exibidas (`columns`) | Filtros Aplicados (`filters`) | Fonte |
|---|---|---|---|---|---|
| `Pendentes_Analise` | Pedidos em Análise | `Everything` | `NAME`, `Conta__c`, `Valor_Total__c`, `Status__c` | `Status__c EQUALS 'Em Análise'` | `Pendentes_Analise.listView-meta.xml` |

---

## 9. Layouts Compactos (`compactLayouts/*.compactLayout-meta.xml`)
*Pasta:* `objects/Pedido__c/compactLayouts/`

| Nome (`fullName`) | Rótulo (`label`) | Campos Exibidos no Cabeçalho (`fields`) | Fonte |
|---|---|---|---|
| `Cabecalho_Pedido` | Destaques do Pedido | `NAME`, `Conta__c`, `Valor_Total__c`, `Status__c` | `Cabecalho_Pedido.compactLayout-meta.xml` |

---

## 10. Processos de Negócio (`businessProcesses/*.businessProcess-meta.xml`)
*Pasta:* `objects/Pedido__c/businessProcesses/` *(Usado principalmente em Lead, Opportunity, Case e Solution)*

| Nome (`fullName`) | Rótulo (`label`) | Ativo (`active`) | Valores de Estágio Selecionados (`values`) | Fonte |
|---|---|---|---|---|
| `Processo_Venda_Padrao` | Processo Comercial | `true` | `Rascunho`, `Em Análise`, `Aprovado` | `Processo_Venda_Padrao.businessProcess-meta.xml` |

---

## 11. Razões de Compartilhamento Gerenciado (`sharingReasons/*.sharingReason-meta.xml`)
*Pasta:* `objects/Pedido__c/sharingReasons/`

| Nome (`fullName`) | Rótulo (`label`) | Descrição / Uso em Código Apex | Fonte |
|---|---|---|---|
| `Aprovador_Especial` | Aprovador Especial | Utilizado em Apex Managed Sharing para conceder acesso temporário. | `Aprovador_Especial.sharingReason-meta.xml` |

---

# 🤖 JSON Schema Compacto para Utilitário Automático

Esquema estruturado para parse do diretório `objects/<Objeto__c>/`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceCustomObjectDoc",
  "type": "object",
  "properties": {
    "object_identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "pluralLabel": { "type": "string" },
        "sharingModel": { "type": "string" },
        "deploymentStatus": { "type": "string" },
        "enableReports": { "type": "boolean" },
        "enableActivities": { "type": "boolean" },
        "enableHistory": { "type": "boolean" },
        "enableSearch": { "type": "boolean" },
        "enableBulkApi": { "type": "boolean" },
        "enableStreamingApi": { "type": "boolean" }
      },
      "required": ["developerName", "label", "sharingModel"]
    },
    "custom_fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "type": { "type": "string" },
          "required": { "type": "boolean" },
          "unique": { "type": "boolean" },
          "externalId": { "type": "boolean" },
          "formula": { "type": "string" },
          "referenceTo": { "type": "string" }
        },
        "required": ["fullName", "label", "type"]
      }
    },
    "validation_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "active": { "type": "boolean" },
          "errorMessage": { "type": "string" },
          "errorConditionFormula": { "type": "string" }
        }
      }
    },
    "record_types": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "active": { "type": "boolean" }
        }
      }
    },
    "web_links": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "masterLabel": { "type": "string" },
          "linkType": { "type": "string" },
          "url": { "type": "string" }
        }
      }
    },
    "field_sets": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "displayedFields": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  },
  "required": ["object_identification", "custom_fields"]
}
```

---

Com esse modelo, seu robô ou agente de documentação consegue ler a pasta de qualquer objeto customizado no Salesforce e extrair todos os metadados relacionados em uma estrutura completa, padronizada e legível.

Quer ajustar a documentação de mais algum componente ou metadado?
