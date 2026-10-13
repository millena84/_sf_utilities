Abaixo está o detalhamento completo e evoluído para a **Onda 06: Objetos de Evento (`__e` / Platform Events e Change Data Capture)**.

A arquitetura orientada a eventos (*Event-Driven Architecture*) no Salesforce permite a comunicação assíncrona, desacoplada e em tempo real entre sistemas internos (Triggers, Flows, LWCs) e externos (AWS, Heroku, MuleSoft, ERPs). Esta onda abrange a documentação de **Platform Events (`__e`)** e **Change Data Capture (`ChangeEvent`)**.

Ao final de cada modelo, incluem-se as seções dedicadas ao **Rastreio de Acesso, Segurança, Retenção e Mecanismos de Bypass**, além do **JSON Schema** exclusivo para o **Claude Code** e utilitários de automação SFDX.

---

# 📑 Modelo 6.1: Platform Events (`[EventName]__e`)

Os **Platform Events (`__e`)** são eventos de mensagens de alto volume baseados na arquitetura *Publish/Subscribe* (Enterprise Messaging Bus) do Salesforce, utilizados para integração assíncrona em tempo real.

### Convenção de Nomes e Estrutura SFDX
* **Diretório do Objeto no Repositório:** `force-app/main/default/objects/[EventName]__e/`
* **Arquivo Mestre:** `[EventName]__e.object-meta.xml` (ex: `Order_Event__e.object-meta.xml`)
* **Pasta de Campos:** `force-app/main/default/objects/[EventName]__e/fields/`
* **Gatilho de Assinatura (Apex):** `force-app/main/default/triggers/[EventName]Trigger.trigger`

---

## 1. Identificação Geral do Platform Event (`[EventName]__e.object-meta.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Order_Event__e</fullName>
    <label>Order Event</label>
    <pluralLabel>Order Events</pluralLabel>
    <eventType>HighVolume</eventType>
    <publishBehavior>PublishAfterCommit</publishBehavior>
    <description>Evento disparado na aprovação de pedidos para sincronização com AWS</description>
</CustomObject>
```

| Propriedade | Valor Exemplo | Tag XML | Descrição / Comportamento de Plataforma |
|---|---|---|---|
| **DeveloperName / ApiName** | `Order_Event__e` | `<fullName>` | Nome API exclusivo (obrigatoriamente termina com o sufixo `__e`). |
| **Label** | `Order Event` | `<label>` | Rótulo de exibição na interface. |
| **Plural Label** | `Order Events` | `<pluralLabel>` | Rótulo no plural. |
| **Event Type** | `HighVolume` | `<eventType>` | Padrão moderno da plataforma gerenciado pelo Enterprise Messaging Bus. |
| **Publish Behavior** | `PublishAfterCommit` \| `PublishImmediately` | `<publishBehavior>` | **`PublishAfterCommit`**: Publica o evento SOMENTE se a transação Apex/DML for commitada no banco.<br>**`PublishImmediately`**: Publica o evento IMEDIATAMENTE (não faz rollback mesmo se o Apex falhar depois). |

---

## 2. Tipos de Campos Permitidos e Limitações do Schema

⚠️ **RESTRIÇÃO TÉCNICA DE SCHEMA:** Diferente de um `CustomObject` convencional, um `PlatformEvent` suporta **apenas um subconjunto restrito de tipos de campos**:

| Tipo de Campo Permito (`type`) | Suportado em `__e`? | Atributos e Limitações | Fonte XML (`fields/*.field-meta.xml`) |
|---|---|---|---|
| **`Text`** | **Sim** | Length máximo: 255 caracteres. | `Order_Number__c.field-meta.xml` |
| **`LongTextArea`** | **Sim** | Length máximo: 131.072 caracteres (usado para Payloads JSON). | `Payload_JSON__c.field-meta.xml` |
| **`Number`** | **Sim** | Precision e Scale configuráveis. | `Total_Amount__c.field-meta.xml` |
| **`DateTime` / `Date`** | **Sim** | Registra carimbos de data/hora do evento. | `Event_Timestamp__c.field-meta.xml` |
| **`Checkbox`** | **Sim** | Flags de status booleano (`true`/`false`). | `Is_Priority__c.field-meta.xml` |
| **`Lookup` / `MasterDetail`** | ❌ **Não** | **Proibido em Platform Events.** Utilize campos de texto armazenando IDs (`String` 18 caracteres). | N/A |
| **`Formula` / `Rollup`** | ❌ **Não** | **Proibido em Platform Events.** O payload deve ser preenchido explicitamente no envio. | N/A |

---

## 3. Matriz de Mecanismos de Publicação (*Publishers*)

| Mecanismo de Publicação | Linguagem / Canal | Exemplo de Código / Configuração |
|---|---|---|
| **Apex Code** | `EventBus.publish()` | `Order_Event__e evt = new Order_Event__e(Order_Number__c = '123');`<br>`Database.SaveResult sr = EventBus.publish(evt);` |
| **Flow Declarativo** | `Create Records` | Elemento *Create Records* em Flow apontando para o objeto `Order_Event__e`. |
| **REST API (Inbound)** | `POST /sobjects/Order_Event__e` | Envio de payload JSON via chamada HTTP REST por sistemas externos. |
| **Pub/Sub API / gRPC** | `PublishStream` | Chamada gRPC de alta performance externa para publicação massiva. |

---

## 4. Matriz de Mecanismos de Assinatura (*Subscribers*)

| Mecanismo de Assinatura | Tecnologia | Exemplo de Implementação / Invocação |
|---|---|---|
| **Apex Event Trigger** | Apex | `trigger OrderEventTrigger on Order_Event__e (after insert)`<br>*(Apenas o evento `after insert` é válido para Platform Events)*. |
| **Platform Event-Triggered Flow** | Flow | Flow disparado automaticamente na chegada de uma nova mensagem no barramento. |
| **Lightning Web Component (LWC)** | `lightning/empApi` | Inscrição via WebSocket CometD em LWC:<br>`subscribe('/event/Order_Event__e', -1, messageCallback);` |
| **Pub/Sub API / gRPC** | gRPC / External | Assinatura de eventos por aplicações externas (AWS Lambda, MuleSoft, NodeJS). |

---

## 5. Retenção de Mensagens, Replay ID e Janela de Re-execução

* **Campo Nátivo `ReplayId`:** Cada mensagem publicada recebe uma chave sequencial global (`ReplayId`).
* **Janela de Retenção (*Event Retention*):** O Salesforce retém eventos de alto volume no barramento por **24 horas** (ou **72 horas** para orgs com licença estendida de High-Volume Events).
* **Replay Options (`empApi` / Pub/Sub API):**
  * `-1`: Receber apenas novas mensagens publicadas a partir do momento da conexão.
  * `-2`: Receber todas as mensagens retidas na janela de 24h/72h (*Replay All*).
  * `ReplayId específico`: Retomar a leitura a partir do último evento processado com sucesso.

---

## 6. Rastreio de Acesso, Segurança, Perfis e Mecanismos de Bypass

Diferente de objetos comuns, Platform Events não possuem registro individual no banco de dados nem proprietário (`OwnerId`), mas o acesso a eles é rigidamente controlado.

### 6.1. Permissões de Objeto no Profile / Permission Set
Para que um usuário, integração ou classe Apex consiga publicar ou ler um Platform Event, a permissão do objeto deve ser liberada:

| Operação de Evento | Permissão Mapeada no Metadado | Tag XML (`PermissionSet` / `Profile`) |
|---|---|---|
| **Publicar Evento (*Publish*)** | Permissão de Inserção (`Create`) | `<objectPermissions><allowCreate>true</allowCreate><object>Order_Event__e</object></objectPermissions>` |
| **Assinar Evento (*Subscribe*)** | Permissão de Leitura (`Read`) | `<objectPermissions><allowRead>true</allowRead><object>Order_Event__e</object></objectPermissions>` |

---

### 6.2. Usuário de Execução da Trigger Assinante (`EventUuid`)
* Por padrão, Triggers de Platform Event executam sob a conta do usuário **`Automated Process`**.
* Para alterar o usuário de execução (evitando falhas por falta de FLS/CRUD na Trigger), mapeia-se o arquivo de configuração `PlatformEventSubscriberConfig`:

*Arquivo:* `force-app/main/default/platformEventSubscriberConfigs/OrderEventTrigger.platformEventSubscriberConfig-meta.xml`
```xml
<PlatformEventSubscriberConfig xmlns="http://soap.sforce.com/2006/04/metadata">
    <platformEventConsumer>OrderEventTrigger</platformEventConsumer>
    <batchSize>200</batchSize>
    <masterLabel>OrderEventTriggerConfig</masterLabel>
    <user>sys.integration@suaorg.com</user>
</PlatformEventSubscriberConfig>
```

---

### 6.3. Mecanismos de Bypass Dinâmico em Event Triggers

| Mecanismo de Bypass | Estrutura | Regra de Desativação no Apex Event Trigger |
|---|---|---|
| **Bypass via Custom Permission** | `CustomPermission` | `if (FeatureManagement.checkPermission('Bypass_Event_Triggers')) return;` |
| **Bypass via Custom Metadata** | `CustomMetadataType` | Checa a flag `Automation_Setting__mdt.Disable_OrderEventTrigger__c` antes de processar os eventos. |

---

# 🤖 JSON Schema Completo: Platform Event (`__e`)

Utilize este esquema JSON para alimentar o utilitário autômato ou **Claude Code** na análise de arquivos `.object-meta.xml`, `.field-meta.xml` e `.trigger` associados a Platform Events:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforcePlatformEventDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "pluralLabel": { "type": "string" },
        "eventType": { "type": "string", "enum": ["HighVolume", "Standard"] },
        "publishBehavior": { 
          "type": "string", 
          "enum": ["PublishAfterCommit", "PublishImmediately"] 
        },
        "description": { "type": "string" }
      },
      "required": ["developerName", "eventType", "publishBehavior"]
    },
    "event_fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "type": { 
            "type": "string", 
            "enum": ["Text", "LongTextArea", "Number", "DateTime", "Date", "Checkbox"] 
          },
          "length": { "type": "integer" }
        },
        "required": ["fullName", "label", "type"]
      }
    },
    "subscribers_and_publishers": {
      "type": "object",
      "properties": {
        "apexTriggers": {
          "type": "array",
          "items": { "type": "string" }
        },
        "platformEventFlows": {
          "type": "array",
          "items": { "type": "string" }
        },
        "lwcSubscribers": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "subscriberConfigUser": { "type": "string", "default": "Automated Process" },
        "profilesWithPublishAccess": {
          "type": "array",
          "items": { "type": "string" }
        },
        "permissionSetsWithPublishAccess": {
          "type": "array",
          "items": { "type": "string" }
        },
        "bypassMechanisms": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "mechanismType": { "type": "string" },
              "developerName": { "type": "string" }
            }
          }
        }
      }
    }
  },
  "required": ["identification", "event_fields", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 6.2: Change Data Capture (`[SObject]ChangeEvent`)

O **Change Data Capture (CDC)** é um recurso nativo de streaming que publica eventos automaticamente no barramento de dados sempre que um registro de um objeto habilitado é criado, alterado, excluído ou restaurado (`CREATE`, `UPDATE`, `DELETE`, `UNDELETE`).

### Convenção de Nomes
* **Objeto Padrão:** `[SObject]ChangeEvent` (ex: `AccountChangeEvent`, `OpportunityChangeEvent`)
* **Objeto Customizado:** `[SObject_Sem_c]__ChangeEvent` (ex: `Pedido__ChangeEvent` para o objeto `Pedido__c`)
* **Arquivo de Configuração no Repositório:** `force-app/main/default/settings/ChangeDataCapture.settings-meta.xml`

---

## 1. Identificação e Habilitação do CDC na Org (`ChangeDataCapture.settings`)

Para que as alterações em um objeto gerem mensagens de streaming, o objeto deve estar incluído na lista `<selectedEntities>` das configurações da Org:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ChangeDataCaptureSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <selectedEntities>
        <entity>Account</entity>
        <entity>Pedido__c</entity>
    </selectedEntities>
</ChangeDataCaptureSettings>
```

| Propriedade / Configuração | Valor Exemplo | Fonte XML | Descrição Técnica |
|---|---|---|---|
| **Entidades Habilitadas** | `Account`, `Pedido__c` | `<selectedEntities>` | Lista de objetos monitorados pelo Change Data Capture. |
| **Nome do Canal de Evento** | `/data/Pedido__ChangeEvent` | Nomenclatura nativa | Canal de assinatura do evento de alteração do objeto. |

---

## 2. Estrutura Padrão do Payload de Evento (`ChangeEventHeader`)

Toda mensagem disparada pelo CDC possui o bloco estático `ChangeEventHeader` contendo os metadados da transação e os campos que sofreram alteração:

| Campo no Header (`ChangeEventHeader`) | Tipo de Dado | Conteúdo / Descrição |
|---|---|---|
| **`entityName`** | `String` | Nome API do objeto alterado (ex: `Pedido__c`). |
| **`changeType`** | `String` | Operação DML que gerou o evento: `CREATE`, `UPDATE`, `DELETE`, `UNDELETE`. |
| **`recordIds`** | `List<String>` | Lista com os IDs de 18 caracteres dos registros afetados na transação. |
| **`changedFields`** | `List<String>` | **Apenas no UPDATE:** Lista dos Nomes API dos campos que foram modificados nesta alteração. |
| **`commitTimestamp`** | `Long` | Carimbo de data/hora em milissegundos da conclusão do commit no banco de dados. |
| **`commitUser`** | `String` | ID do usuário do Salesforce que provocou a alteração DML. |
| **`transactionKey`** | `String` | Chave exclusiva da transação (usada para agrupar alterações feitas no mesmo commit). |
| **`sequenceNumber`** | `Integer` | Sequência de execução da alteração dentro da transação. |

---

## 3. Enriquecimento de Eventos de Alteração (*Event Enrichment*)

Por padrão, em eventos do tipo `UPDATE`, o CDC envia no payload **somente os campos que foram alterados**. Para incluir campos fixos de contexto (ex: enviar sempre o `Numero_ERP__c` mesmo se ele não tiver mudado), configura-se o **Event Enrichment**:

*Arquivo:* `force-app/main/default/eventChannels/EnrichedOrderChannel.eventChannel-meta.xml` e `eventChannelMembers/`

```xml
<EventChannelMember xmlns="http://soap.sforce.com/2006/04/metadata">
    <eventChannel>ChangeEvents</eventChannel>
    <selectedEntity>Pedido__ChangeEvent</selectedEntity>
    <enrichedFields>
        <name>Numero_ERP__c</name>
    </enrichedFields>
    <enrichedFields>
        <name>Conta__c</name>
    </enrichedFields>
</EventChannelMember>
```

---

## 4. Invocação em Apex Event Triggers e Assinatura

Assinatura de gatilho Apex diretamente sobre o evento de alteração de um objeto customizado:

```apex
trigger PedidoChangeEventTrigger on Pedido__ChangeEvent (after insert) {
    for (Pedido__ChangeEvent event : Trigger.new) {
        EventHeader header = event.ChangeEventHeader;
        
        if (header.changeType == 'UPDATE') {
            List<String> camposAlterados = header.changedFields;
            if (camposAlterados.contains('Status__c')) {
                // Lógica de reação à alteração de status
            }
        }
    }
}
```

---

## 5. Rastreio de Acesso, Segurança, FLS e Filtros por Usuário

### 5.1. Segurança Nativa de FLS/CRUD no CDC
Diferente de eventos customizados, o **Change Data Capture respeita o FLS (Field-Level Security) e o CRUD** do assinante quando consumido via APIs externas CometD/gRPC:
* Se o usuário que assina o canal do CDC não tiver permissão de leitura em um campo específico (FLS = `Hidden`), esse campo é **removido automaticamente do payload** recebido por aquele usuário.

### 5.2. Rastreio de Acesso aos Canais de Evento

| Componente | Requisito de Permissão | Rastreio em Profiles / Permission Sets |
|---|---|---|
| **Assinatura CDC via API Externa** | Permissão `View Change Data Capture` | Ativada na tag `<userPermissions><name>ViewChangeDataCapture</name><enabled>true</enabled></userPermissions>` |
| **Assinatura CDC via Apex Trigger** | Permissão de Leitura no SObject Base | O usuário precisa ter `Read` no objeto `Pedido__c` para acionar a Trigger de evento CDC. |

---

# 🤖 JSON Schema Completo: Change Data Capture (`ChangeEvent`)

Utilize este esquema JSON para alimentar o utilitário autômato ou **Claude Code** no parse das configurações de CDC e Triggers associadas:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceChangeDataCaptureDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "sObject": { "type": "string" },
        "changeEventApiName": { "type": "string" },
        "isEnabledInOrg": { "type": "boolean" },
        "channelName": { "type": "string" }
      },
      "required": ["sObject", "changeEventApiName", "isEnabledInOrg"]
    },
    "event_enrichment": {
      "type": "object",
      "properties": {
        "hasEnrichedFields": { "type": "boolean" },
        "enrichedFieldsList": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "subscribers": {
      "type": "object",
      "properties": {
        "apexTriggers": {
          "type": "array",
          "items": { "type": "string" }
        },
        "flows": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "requiresViewChangeDataCapturePermission": { "type": "boolean", "default": true },
        "respectsFLSOnStreaming": { "type": "boolean", "default": true },
        "profilesWithCDCAccess": {
          "type": "array",
          "items": { "type": "string" }
        },
        "permissionSetsWithCDCAccess": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "access_and_security_tracking"]
}
```

---

💡 A **Onda 06 (Objetos de Evento `__e` e Change Data Capture)** está concluída! Se desejar dar sequência, podemos avançar para o detalhamento da **Onda 07 (Tipos do Service Cloud)**, **Onda 08 (Sales Cloud)**, **Onda 09 (Experience Cloud)** ou **Onda 10 (OmniStudio)**.
