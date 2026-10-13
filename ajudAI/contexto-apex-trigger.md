Abaixo está o detalhamento completo e evoluído para a **Onda 02: Apex Trigger**, incluindo o padrão de arquitetura (*Trigger Handler Pattern*), variáveis de contexto, controle de recursão, a **matriz de referência cruzada e ordem de execução com Flow Triggers** e a nova seção dedicada ao **Rastreio de Acesso, Segurança e Mecanismos de Bypass (Profile, Permission Set, Custom Permission, etc.)**, finalizando com o **JSON Schema** correspondente.

---

# 📑 Modelo Evoluído: Apex Trigger (`.trigger`) e Referência Cruzada com Flow

O **Apex Trigger** é um gatilho a nível de banco de dados que executa lógicas de negócios complexas antes (*Before*) ou depois (*After*) de operações DML (`insert`, `update`, `delete`, `undelete`) em objetos padrão ou customizados.

### Convenção de Nomes e Estrutura SFDX
* **Arquivo da Trigger:** `[SObject]Trigger.trigger` e `[SObject]Trigger.trigger-meta.xml` (ex: `OrderTrigger.trigger`)
* **Pasta no Repositório:** `force-app/main/default/triggers/`
* **Classe Handler Associada:** `[SObject]TriggerHandler.cls` e `[SObject]TriggerService.cls`
* **Pasta da Classe Handler:** `force-app/main/default/classes/`

---

## 1. Identificação Geral da Trigger

| Propriedade | Valor Exemplo | Tag / Fonte | Descrição Técnica |
|---|---|---|---|
| **Trigger Name / ApiName** | `OrderTrigger` | Arquivo `.trigger` | Nome de API exclusivo do gatilho Apex no repositório. |
| **SObject Alvo** | `Pedido__c` | `.trigger` (`on Pedido__c`) | Objeto monitorado pela Trigger. |
| **ApiVersion** | `62.0` | `.trigger-meta.xml` (`<apiVersion>`) | Versão da API Salesforce utilizada. |
| **Status** | `Active` \| `Inactive` | `.trigger-meta.xml` (`<status>`) | Estado de publicação (`Active` executa o gatilho; `Inactive` desativa). |
| **Eventos Ativos** | `before insert`, `after insert`, `before update`, `after update` | Assinatura `.trigger` | Relação de eventos DML habilitados na assinatura. |
| **Handler Pattern** | `OrderTriggerHandler` | Código `.trigger` | Classe Apex que recebe a execução para evitar lógica direta no arquivo `.trigger`. |

---

## 2. Variáveis de Contexto e Eventos Suportados

A tabela abaixo mapeia a utilização das variáveis globais nativas `Trigger.*` dentro da implementação:

| Variável de Contexto | Tipo de Dado | Uso e Disponibilidade | Finalidade Técnica |
|---|---|---|---|
| **`Trigger.isBefore`** | `Boolean` | Todos os eventos | Retorna `true` se executado antes da gravação no banco de dados. |
| **`Trigger.isAfter`** | `Boolean` | Todos os eventos | Retorna `true` se executado após a gravação preliminar no banco de dados. |
| **`Trigger.isInsert`** | `Boolean` | Inserção | Retorna `true` em operações de criação de registro. |
| **`Trigger.isUpdate`** | `Boolean` | Atualização | Retorna `true` em operações de edição de registro. |
| **`Trigger.isDelete`** | `Boolean` | Exclusão | Retorna `true` em operações de exclusão de registro. |
| **`Trigger.isUndelete`** | `Boolean` | Restauração | Retorna `true` ao restaurar registros da Lixeira (*Recycle Bin*). |
| **`Trigger.new`** | `List<sObject>` | Insert, Update, Undelete | Lista dos novos registros. Modificável **apenas** em `before insert` e `before update`. |
| **`Trigger.newMap`** | `Map<Id, sObject>` | After Insert, Update, Undelete | Mapa de IDs para os novos registros (disponível apenas em eventos `After` ou `Update`). |
| **`Trigger.old`** | `List<sObject>` | Update, Delete | Lista dos registros com os valores antigos **anteriores** à alteração. |
| **`Trigger.oldMap`** | `Map<Id, sObject>` | Update, Delete | Mapa de IDs para os valores antigos dos registros. |
| **`Trigger.size`** | `Integer` | Todos os eventos | Quantidade total de registros recebidos no lote de execução (máx. 200 por lote). |

---

## 3. Padrão de Arquitetura, Bulkificação e Controle de Recursão

```apex
trigger OrderTrigger on Pedido__c (before insert, before update, after insert, after update) {
    // BOA PRÁTICA: Delegar imediatamente para a classe Handler
    OrderTriggerHandler.run();
}
```

### 3.1. Salvaguardas de Arquitetura OBRIGATÓRIAS
1. **Sem Lógica no Arquivo `.trigger`:** O arquivo `.trigger` deve conter apenas uma linha chamando o framework de Handler.
2. **Bulkificação (Processamento em Lote):** NUNCA executar consultas SOQL ou comandos DML dentro de laços de repetição (`for`). O código deve tratar `Trigger.new` como uma lista de 1 a 200 registros por lote.
3. **Controle de Recursão (*Looping Prevention*):** Utilização de variável estática ou conjunto de IDs processados para evitar que um `update` dentro de um evento `after` dispare a mesma Trigger indefinidamente.

---

## 4. Matriz de Referência Cruzada: Apex Trigger vs. Flow Trigger

Esta seção estabelece a ordem de execução (*Order of Execution*) e a convivência de automações declarativas e programáticas no mesmo SObject:

| Ordem de Execução | Tipo de Automação | Nome do Artefato | Fase / Evento | Responsabilidade Funcional |
|---|---|---|---|---|
| **1º** | **Apex Trigger** | `OrderTrigger` | `Before Insert / Update` | Validações complexas de dados, cálculos com regras pesadas e preenchimento de campos do próprio registro. |
| **2º** | **Record-Triggered Flow** | `FL_Order_Before_Save` | `Fast Field Updates` | Atualizações declarativas rápidas no próprio registro antes da gravação no banco. |
| **3º** | **Regras de Validação** | `ValidationRule` | `Validation` | Checagem de regras de validação padrão e customizadas do objeto. |
| **4º** | **Apex Trigger** | `OrderTrigger` | `After Insert / Update` | Gravação em banco concluída (`Id` gerado). Criação de registros filhos, chamada de Queueable/Async e envio de eventos. |
| **5º** | **Record-Triggered Flow** | `FL_Order_After_Save` | `Actions & Related Records` | Atualização de objetos relacionados, envios de e-mail e criação de tarefas declarativas. |
| **6º** | **Roll-Up Summary / Workflow** | `RollupSummary` / `Workflow` | `Post-DML` | Re-cálculo de campos de resumo e execução de regras legadas. |

---

## 5. Rastreio de Acesso, Permissões e Mecanismos de Bypass

Como o Apex Trigger executa nativamente no **Modo Sistema (*System Mode*)** ignorando as permissões de CRUD e FLS do usuário logado, esta seção mapeia as travas de segurança, acessos de perfil/permission set e os mecanismos dinâmicos de bypass configurados na Org.

### 5.1. Contexto de Segurança de Código
* **Modo de Execução:** `System Mode` (Bypassa OWD, CRUD e FLS por padrão).
* **Enforcing Security no Handler:** Indica se a classe Handler aplica `WITH USER_MODE`, `AccessController` ou `Schema.sObjectType.Pedido__c.isDeletable()`.

### 5.2. Acesso aos Artefatos de Código (Quem pode disparar)
Qualquer usuário que possua permissão de gravação no objeto aciona a Trigger. No entanto, o acesso aos componentes Apex relacionados é rastreado por:

| Componente Técnico | Tipo de Acesso | Perfis Autorizados (`Profiles`) | Conjuntos de Permissões (`Permission Sets`) |
|---|---|---|---|
| **Objeto Alvo (`Pedido__c`)** | `Create` / `Edit` / `Delete` | `System Administrator`, `Sales User` | `PS_Sales_Operations` |
| **Handler Class (`OrderTriggerHandler`)** | `Apex Class Access` | `System Administrator` | `PS_Integration_Apex_Access` |

### 5.3. Mecanismos de Bypass Dinâmico (Desativação Seletiva)
Mapeamento das estruturas utilizadas para desativar a Trigger temporariamente para cargas de dados, usuários de integração ou testes:

| Mecanismo de Bypass | Tipo de Metadado | Tag / Campo Utilizado | Regra de Desativação |
|---|---|---|---|
| **Custom Permission** | `CustomPermission` | `Bypass_Apex_Triggers` | Se `$Permission.Bypass_Apex_Triggers = true`, o Handler interrompe a execução. |
| **Custom Setting** | `Hierarchy Custom Setting` | `Automation_Settings__c.Bypass_Triggers__c` | Permite desligar Triggers por Usuário, Perfil ou Org-Wide. |
| **Custom Metadata Type** | `CustomMetadataType` | `Bypass_Setting__mdt.OrderTrigger__c` | Permite ativar/desativar gatilhos específicos dinamicamente no Setup sem alterar código. |

---

# 🤖 JSON Schema Completo: Apex Trigger com Rastreio de Acesso

Utilize este esquema JSON para alimentar o utilitário autômato ou **Claude Code** no parse de arquivos `.trigger`, `.trigger-meta.xml` e da classe Handler associada:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceApexTriggerDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "triggerName": { "type": "string" },
        "sObject": { "type": "string" },
        "apiVersion": { "type": "string" },
        "status": { "type": "string", "enum": ["Active", "Inactive"] },
        "handlerClass": { "type": "string" },
        "events": {
          "type": "array",
          "items": { 
            "type": "string",
            "enum": ["before insert", "before update", "before delete", "after insert", "after update", "after delete", "after undelete"]
          }
        }
      },
      "required": ["triggerName", "sObject", "status", "events"]
    },
    "architecture_and_context": {
      "type": "object",
      "properties": {
        "usesHandlerPattern": { "type": "boolean", "default": true },
        "hasRecursionControl": { "type": "string" },
        "bulkified": { "type": "boolean", "default": true },
        "contextVariablesUsed": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "order_of_execution_coexistence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "executionOrder": { "type": "integer" },
          "automationType": { "type": "string", "enum": ["ApexTrigger", "RecordTriggeredFlow", "ValidationRule", "WorkflowRule"] },
          "artifactName": { "type": "string" },
          "eventPhase": { "type": "string" },
          "responsibility": { "type": "string" }
        }
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "executionMode": { "type": "string", "enum": ["SystemMode", "UserModeEnforced"] },
        "sobjectCrudAccess": {
          "type": "object",
          "properties": {
            "profilesWithAccess": { "type": "array", "items": { "type": "string" } },
            "permissionSetsWithAccess": { "type": "array", "items": { "type": "string" } }
          }
        },
        "handlerClassAccess": {
          "type": "object",
          "properties": {
            "profilesWithApexAccess": { "type": "array", "items": { "type": "string" } },
            "permissionSetsWithApexAccess": { "type": "array", "items": { "type": "string" } }
          }
        },
        "bypass_mechanisms": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "mechanismType": { "type": "string", "enum": ["CustomPermission", "CustomSetting", "CustomMetadataType"] },
              "developerName": { "type": "string" },
              "fieldNameOrTag": { "type": "string" },
              "bypassScope": { "type": "string" }
            }
          }
        }
      },
      "required": ["executionMode"]
    }
  },
  "required": ["identification", "access_and_security_tracking"]
}
```

---

💡 **Próximos Passos:** Este modelo para a **Onda 02** já contempla todas as seções de rastreio de acesso, perfis, permission sets e mecanismos de bypass. Caso queira avançar para o detalhamento das ondas seguintes (ex: **Onda 03: LWC**, **Onda 04: Flexipages** ou **Onda 05: Segurança/OWD**), é só avisar!
