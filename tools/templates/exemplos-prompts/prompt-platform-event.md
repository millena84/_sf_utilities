# Prompt — PlatformEvent

## 1. Contexto do componente

### 1.1 O que é
`PlatformEvent` (nome funcional: **Evento de Plataforma**) é um tipo de evento personalizado no Salesforce que permite a comunicação assíncrona entre processos do Salesforce e sistemas externos. Baseado na arquitetura publish/subscribe, os eventos são publicados por produtores e consumidos por assinantes (Apex triggers, Flows, APIs REST/SOAP, Pub/Sub API, CometD).

Na prática, um `PlatformEvent`:
- é definido como um objeto especial comum (`__e`) na plataforma;
- suporta campos customizados, mas **não** campos de fórmula, lookups, rollups ou workflows;
- possui um `PublishBehavior` (`PublishAfterCommit` ou `PublishImmediately`);
- é imutável após a publicação: não é possível editar ou excluir eventos;
- oferece suporte a replay de eventos através de replay IDs e canais;
- pode ser publicado via Apex, Flow, Process Builder, REST API ou Pub/Sub API.

### 1.2 Para que serve
- Desacoplar processos de integração entre Salesforce e sistemas externos.
- Notificar sistemas externos sobre mudanças de estado em tempo real.
- Orquestrar fluxos assíncronos dentro da plataforma.
- Implementar padrões de event-driven architecture.

### 1.3 Cenários típicos de uso
- Notificar ERP quando um pedido é aprovado.
- Disparar processamento assíncrono em lotes.
- Sincronizar dados com middleware quando um registro muda.
- Disparar Flow/Apex após transações complexas.

### 1.4 Clouds / contextos
- **Salesforce Core** — Apex, Flow, REST API, Pub/Sub API.
- **Experience Cloud** — eventos compartilhados com comunidades.
- **Data Cloud / Agentforce** — ingestão de eventos e orquestração.
- **Integração / Middleware** — MuleSoft, Kafka, AWS etc.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `PlatformEvent`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Platform Event / Evento de Plataforma |
| Metadata type exact | `CustomObject` com `<eventType>HighVolume</eventType>` |
| Pasta no projeto SFDX | `objects/<API_Name>/` |
| Arquivo padrão | `<API_Name>__e.object-meta.xml` |
| Objeto interno (API padrão) | `EntityDefinition` / `PlatformEventDefinition` |
| Objeto interno (Tooling API) | `CustomObject` (com `DeveloperName` terminando em `__e`) |
| Acessível por Metadata API | Sim — `CustomObject` tipo evento |
| Acessível por API padrão / SOQL | Sim — via `EntityDefinition`, `PlatformEventDefinition`, etc. |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `EventBus.Event` |
| Acessível por UI | Sim — **Setup → Platform Events** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Apex Trigger | `ApexTrigger` (context `PlatformEvents`) | Assinatura síncrona do evento. |
| Flow | `Flow` (trigger type Platform Event) | Assinatura declarativa do evento. |
| Process Builder | `Flow` legado | Publicação/assinação antiga. |
| Event Subscription | `EventBusSubscription` (Tooling) | Assinaturas ativas. |
| Event Relay | `EventRelayConfig` | Envio de eventos para AWS EventBridge. |
| Pub/Sub API | API externa | Consumo por sistemas externos. |
| CometD | API externa | Streaming assinatura. |
| Change Data Capture | `PlatformEvent` CDC (`ChangeEvent`) | Distinto, mas similar. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | PlatformEvent metadata | EntityDefinition (SOQL) | Tooling | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | Sim | Sim | Sim | Sim |
| Publish behavior | Sim (`<eventType>`, `<publishBehavior>`) | — | Sim | Sim | Sim |
| Campos | Sim (`fields/`) | via `FieldDefinition` | Sim | Sim | Sim |
| Apex triggers | via `ApexTrigger` | — | `ApexTrigger.TableEnumOrId` | Setup | Sim |
| Flow subscriptions | via `Flow` | — | `Flow` | Setup | Sim |
| Event subscriptions ativas | — | — | `EventBusSubscription` | Monitoring | Sim |
| Volume/usage | — | `PlatformEventUsageMetric` | — | Monitoring | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`CustomObject` tipo evento)

Arquivo típico: `objects/<API_Name>__e/<API_Name>__e.object-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<deploymentStatus>` | 1 | `Deployed` ou `InDevelopment`. |
| `<description>` | 0..1 | Descrição. |
| `<eventType>` | 1 | `HighVolume`. |
| `<publishBehavior>` | 1 | `PublishAfterCommit` (padrão) ou `PublishImmediately`. |
| `<label>` | 1 | Nome amigável. |
| `<pluralLabel>` | 1 | Plural. |
| `<fields>` | 0..N | Campos customizados. |

#### `PublishBehavior`

| Valor | Significado |
|---|---|
| `PublishAfterCommit` | Evento publicado após commit da transação (mais seguro, padrão). |
| `PublishImmediately` | Evento publicado imediatamente, mesmo em rollback. |

### 3.2 Objeto interno via API padrão: `PlatformEventDefinition`

```sql
SELECT Id, DeveloperName, MasterLabel, Label, PluralLabel,
       PublisherId, PublishBehavior, IsCustomizable, IsDeprecatedAndHidden,
       CreatedDate, LastModifiedDate
FROM PlatformEventDefinition
ORDER BY Label
```

### 3.3 Campos do evento

```sql
SELECT Id, EntityDefinitionId, EntityDefinition.DeveloperName,
       DeveloperName, MasterLabel, DataType, IsRequired,
       CreatedDate, LastModifiedDate
FROM FieldDefinition
WHERE EntityDefinition.DeveloperName LIKE '%__e'
ORDER BY EntityDefinition.DeveloperName, DeveloperName
```

### 3.4 Assinaturas e consumidores

#### Apex Triggers

```sql
SELECT Id, Name, TableEnumOrId, Status, ApiVersion, UsageBeforeInsert,
       UsageAfterInsert, UsageBeforeUpdate, UsageAfterUpdate
FROM ApexTrigger
WHERE TableEnumOrId LIKE '%__e'
ORDER BY TableEnumOrId, Name
```

#### Flows (assinaturas de platform event)

```sql
SELECT Id, ApiName, Label, Status, VersionNumber, TriggerType
FROM FlowDefinitionView
WHERE TriggerType = 'PlatformEvent'
ORDER BY Label
```

#### EventBusSubscription (Tooling API)

```sql
SELECT Id, Name, ExternalEndpoint, IsLive, Position, RetryCount, Status, Topic
FROM EventBusSubscription
ORDER BY Topic
```

### 3.5 Métricas de uso

```sql
SELECT ExternalId, EntityName, EventType, Channel, UsageType, Value, StartDate, EndDate
FROM PlatformEventUsageMetric
ORDER BY StartDate DESC
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Platform Events.
- Setup → Flows com trigger de Platform Event.
- Setup → Apex Triggers (contexto de evento).
- Setup → Event Monitoring / Platform Event Metrics.
- Pub/Sub API e CometD logs externos.
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Payload específico de eventos publicados | Registros no objeto `__e` (temporário) | Metadata do evento | Dados voláteis. |
| Replay ID consumido | `EventBusSubscription.Position` | `PlatformEventDefinition` | Estado da assinatura. |
| Falhas de entrega | `EventBusSubscriberException` / logs | `PlatformEventDefinition` | Requer logs/config. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ApexTrigger`

- Trigger de evento roda no contexto `System` e pode publicar novos eventos.
- Limites de governança aplicam-se (DML, SOQL, callouts).

### 4.2 `Flow`

- Flow de autolaunch com trigger de Platform Event.
- Não suporta callouts diretamente; foge para Apex.

### 4.3 `EventRelayConfig`

- Encaminha eventos para AWS EventBridge.
- Configura canal, datastore e filtro.

### 4.4 `Pub/Sub API` / `CometD`

- Sistemas externos assinam eventos via replay ID.
- Usa OAuth para autenticação.

### 4.5 `Change Data Capture`

- CDC é um tipo especial de Platform Event (`ChangeEvent`).
- Distinto de eventos de plataforma customizados, mas com padrão de consumo similar.

---

## 5. Consultas e formas de extração

### 5.1 Eventos de plataforma

```sql
SELECT Id, DeveloperName, MasterLabel, PluralLabel,
       PublishBehavior, CreatedDate, LastModifiedDate
FROM PlatformEventDefinition
ORDER BY MasterLabel
```

### 5.2 Campos de eventos

```sql
SELECT Id, EntityDefinitionId, EntityDefinition.DeveloperName,
       DeveloperName, MasterLabel, DataType, IsRequired
FROM FieldDefinition
WHERE EntityDefinition.DeveloperName LIKE '%__e'
ORDER BY EntityDefinition.DeveloperName, DeveloperName
```

### 5.3 Apex triggers de evento

```sql
SELECT Id, Name, TableEnumOrId, Status, ApiVersion
FROM ApexTrigger
WHERE TableEnumOrId LIKE '%__e'
ORDER BY TableEnumOrId, Name
```

### 5.4 Assinaturas ativas (Tooling API)

```sql
SELECT Id, Name, IsLive, Position, RetryCount, Status, Topic, ExternalEndpoint
FROM EventBusSubscription
ORDER BY Topic
```

### 5.5 Métricas de volume

```sql
SELECT ExternalId, EntityName, EventType, Channel, UsageType, Value, StartDate, EndDate
FROM PlatformEventUsageMetric
ORDER BY StartDate DESC
```

---

## 6. Boas práticas e pontos de atenção

- **Escolha `PublishAfterCommit`** como padrão; use `PublishImmediately` apenas quando necessário.
- **Design os eventos para serem imutáveis e autocontidos**: preencha todos os dados necessários no payload.
- **Evite loops recursivos**: publicar eventos dentro de triggers de eventos pode criar cadeias infinitas.
- **Monitore limites de publicação**: existe limite diário de publicação de eventos.
- **Trate idempotência** no consumidor para evitar duplicados.
- **Use `EventBus.RetryableException`** para retry controlado no Apex.
- **Documente a semântica** de cada evento: produtores, consumidores e payload.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Separe eventos de negócio** de eventos técnicos quando necessário.
- **Considere CDC** para eventos de mudança de dados, evitando recriar lógica de captura.

---

## 7. Links de referência oficial

- [Salesforce Help — Platform Events](https://help.salesforce.com/s/articleView?id=sf.platform_events.htm)
- [Salesforce Developer — Platform Event Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_intro.htm)
- [Salesforce Developer — Pub/Sub API Guide](https://developer.salesforce.com/docs/platform/pub-sub-api/overview)
- [Salesforce Help — Event Relay](https://help.salesforce.com/s/articleView?id=sf.event_relay_intro.htm)
- [Salesforce Developer — EventBusSubscription](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/sforce_api_objects_eventbussubscription.htm)
