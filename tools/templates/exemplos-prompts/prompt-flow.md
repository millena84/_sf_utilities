# Prompt — Flow

## 1. Contexto do componente

### 1.1 O que é
`Flow` (nome funcional: **Flow**, **Screen Flow**, **Record-Triggered Flow**, **Autolaunched Flow** etc.) é o metadata type do Salesforce que representa uma automação declarativa construída no Flow Builder. Um Flow é composto por elementos conectados que executam lógica de negócio sem necessidade de código Apex.

Na prática, um Flow:
- pode ser disparado por tela (Screen Flow), registro (Record-Triggered Flow), agendamento (Scheduled Flow), evento de plataforma (Platform Event-Triggered Flow), botão/invocação (Autolaunched Flow) ou autolaunch por Apex/API;
- contém elementos como variáveis, tela, decisão, loop, atribuição, subflow, ações Apex, HTTP Callout, invocação de código e registros DML;
- pode interagir com objetos do Salesforce, external services e callouts;
- é versionado: existe uma definição (`FlowDefinitionView`) e uma ou mais versões (`FlowVersionView`), sendo que apenas uma versão está ativa por vez.

### 1.2 Para que serve
- Automatizar processos de negócio de forma declarativa sem Apex.
- Guiar usuários por telas e coletar informações (Screen Flows).
- Executar lógica DML, validações e cálculos em resposta a eventos de registro.
- Orquestrar chamadas a Apex actions, External Services e HTTP Callouts.
- Substituir regras de workflow, process builder e Approval Processes legados.
- Viabilizar automações para Agentforce e Experience Cloud.

### 1.3 Cenários típicos de uso
- Automação de criação/atualização de registros baseada em critérios.
- Screen Flow para wizards de criação de oportunidade, cotação ou case.
- Scheduled Flow para processamento noturno em lote.
- Record-Triggered Flow para validações e atualizações em before/after save.
- Flow com HTTP Callout para integração com serviços externos.
- Subflows reutilizáveis chamados por múltiplos Flows.
- Automação de aprovações simples ou notificações.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em praticamente todas as edições com Flow Builder habilitado.
- **Service Cloud / Sales Cloud** — automações de case, oportunidade, lead, tarefa.
- **Experience Cloud** — Screen Flows expostos em páginas de comunidade/portais.
- **Field Service** — Flows para agendamento, work orders, mobile workforce.
- **Marketing Cloud Engagement / Account Engagement** — integrações via External Actions.
- **Agentforce** — Flows podem ser invocados por agentes como ações/skills.

> **Nota de edição/licença**: a maioria dos tipos de Flow está disponível amplamente. Recursos avançados (HTTP Callout, Integration Procedures, Orchestrator) podem depender de edição/licença ou release. Record-Triggered Flows exigem objeto e evento suportados.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `Flow`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Flow |
| Metadata type exact | `Flow` |
| Pasta no projeto SFDX | `flows/` |
| Arquivo padrão | `<apiName>.flow-meta.xml` |
| Objeto interno (API padrão) | `FlowDefinitionView`, `FlowVersionView`, `FlowInterview` |
| Objeto interno (Tooling API) | `Flow` (com campo `Metadata`), `FlowDefinition` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `FlowDefinitionView`, `FlowVersionView`, `FlowInterview`, `FlowTestResult` |
| Acessível por Tooling API | Sim — `SELECT ... FROM Flow`, `FlowDefinition` |
| Acessível por Apex | Parcial — objetos de view e entrevista consultáveis; lógica via `Flow.Interview` e invocação programática |
| Acessível por UI | Sim — **Setup → Flows** ou **Flow Builder** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Flow Definition | `FlowDefinitionView` (objeto) / `FlowDefinition` (Tooling) | Representa a definição do Flow e suas versões. |
| Flow Version | `FlowVersionView` (objeto) / versões dentro do XML de `Flow` | Cada versão publicada do Flow. |
| Flow Interview | `FlowInterview` (objeto) | Instância de execução de um Screen Flow em andamento. |
| Flow Test | `FlowTest` (metadata) / `FlowTestView` / `FlowTestResult` | Testes automatizados de Flow. |
| Flow Category | `FlowCategory` (metadata) / `FlowCategoryView` | Agrupamento/categorização de Flows. |
| Subflow | referência `<flowName>` dentro de outro `Flow` | Reutilização de lógica. |
| Apex Action | `ApexClass` com `@InvocableMethod` | Ações invocáveis dentro do Flow. |
| Email Alert | `WorkflowAlert` / `EmailTemplate` | Ação de email do Flow. |
| External Service Registration | `ExternalServiceRegistration` | Ações geradas a partir de OpenAPI para Flow. |
| Named Credential / External Credential | `NamedCredential`, `ExternalCredential` | HTTP Callout actions. |
| Process Builder (legado) | `Flow` do tipo `Workflow` | Pode aparecer como Flow legado convertido. |
| Workflow Rule (legado) | `WorkflowRule` | Fluxos que substituem Workflow Rules. |
| Custom Label / Custom Metadata | `CustomLabel`, `CustomMetadata` | Dados de configuração usados no Flow. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | Flow metadata | `FlowDefinitionView` (SOQL) | `Flow` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| API Name / label | Sim | Sim | Sim | Sim | Sim |
| Status (Active/Draft/Obsolete) | Sim (`status`) | Sim (`ActiveVersionId`, `LatestVersionId`) | Sim | Sim | Sim |
| Tipo de Flow | Sim (`processType`) | Sim (`ProcessType`) | Sim | Sim | Sim |
| Versões | em `Flow` retrieve (última ou ativa conforme config) | `FlowVersionView` | Sim | Sim | `FlowVersionView` |
| Elementos/variáveis | XML | parcial | `Metadata` | Flow Builder | Sim |
| Subflows / Apex actions | XML | parcial | `Metadata` | Flow Builder | Sim |
| HTTP Callout / External Service | XML | parcial | `Metadata` | Flow Builder | Sim |
| Interviews em execução | não | `FlowInterview` | `FlowInterview` | UI admin | Sim |
| Testes automatizados | `FlowTest` metadata | `FlowTestResult` | `FlowTest` (Tooling) | Flow Builder | `FlowTestResult` |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`Flow`)

Arquivo típico: `flows/<API_Name>.flow-meta.xml`.

#### Tags raiz e atributos comuns

| Tag / Atributo | Obrigatória? | Significado prático |
|---|---|---|
| `Flow` (root) | Sim | Elemento raiz do metadata type. |
| `xmlns` | Sim | Namespace XML do Metadata API. |
| `fullName` (atributo) / nome do arquivo | Sim | API Name interno. |
| `apiVersion` | Sim | Versão da API usada pelo Flow. |

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<apiVersion>` | 1 | Versão da API do Flow Builder. |
| `<description>` | 0..1 | Descrição funcional/técnica. |
| `<isTemplate>` | 0..1 | Indica se o Flow é um template. |
| `<label>` | 1 | Nome amigável exibido na UI. |
| `<processMetadataValues>` | 0..N | Metadados do processo (origem, builder etc.). |
| `<processType>` | 1 | Tipo do Flow: `AutoLaunchedFlow`, `Flow`, `Workflow`, `CustomEvent`, `InvocableProcess`, `Orchestrator`, `RoutingFlow`, `ServiceCatalogItemFlow` etc. |
| `<status>` | 1 | Status da versão: `Active`, `Draft`, `Obsolete`. |
| `<start>` | 0..1 (geralmente 1) | Elemento de início do Flow, define trigger, objeto, condições, schedule. |
| `<actionCalls>` | 0..N | Chamadas a ações Apex, email alerts, send notifications etc. |
| `<apexPluginCalls>` | 0..N | Chamadas a plugins Apex. |
| `<assignments>` | 0..N | Atribuições de valores a variáveis. |
| `<collectionProcessors>` | 0..N | Processadores de coleção (Filter, Sort, Map). |
| `<decisions>` | 0..N | Elementos de decisão com branches. |
| `<loops>` | 0..N | Loops sobre coleções. |
| `<recordCreates>` | 0..N | Criação de registros. |
| `<recordDeletes>` | 0..N | Exclusão de registros. |
| `<recordLookups>` | 0..N | Consultas a registros. |
| `<recordUpdates>` | 0..N | Atualização de registros. |
| `<screens>` | 0..N | Telas do Screen Flow. |
| `<subflows>` | 0..N | Chamadas a outros Flows. |
| `<variables>` | 0..N | Variáveis do Flow. |
| `<constants>` | 0..N | Constantes. |
| `<formulas>` | 0..N | Fórmulas. |
| `<choices>` | 0..N | Opções para componentes de tela. |
| `<dynamicChoiceSets>` | 0..N | Conjuntos dinâmicos de opções. |
| `<textTemplates>` | 0..N | Templates de texto. |
| `<stages>` | 0..N | Estágios do Flow. |
| `<faultConnectors>` | implícito | Conectores de falha entre elementos. |

##### Elemento `<start>`

| Sub-tag / Atributo | Significado prático |
|---|---|
| `<connector>` | Próximo elemento após o start. |
| `<object>` | Objeto que dispara Record-Triggered Flow. |
| `<recordTriggerType>` | `Create`, `Update`, `CreateAndUpdate`, `Delete`. |
| `<triggerType>` | `RecordBeforeSave`, `RecordAfterSave`, `RecordBeforeDelete`, `Scheduled`, `PlatformEvent`, `Screen`. |
| `<schedule>` | Configuração de Scheduled Flow. |
| `<filterLogic>` | Lógica de filtros de entrada. |
| `<filters>` | Condições de entrada. |
| `<doesRequireRecordChangedToMeetCriteria>` | Só dispara quando o registro passa a atender critérios. |

#### Observações sobre XML

- O arquivo `.flow-meta.xml` contém todos os elementos e conectores da versão.
- A complexidade do XML cresce rapidamente; ferramentas de diff devem considerar reorganizações de elementos.
- A ausência de `<faultConnector>` em um elemento não significa ausência de tratamento de erro se houver configuração padrão.
- Flows migrados do Process Builder podem ter estruturas específicas herdadas.

---

### 3.2 Objetos internos via API padrão

#### `FlowDefinitionView`

| Campo | Significado prático |
|---|---|
| `Id` | ID da definição. |
| `ApiName` / `FlowDefinitionViewId` | API Name do Flow. |
| `Label` | Nome amigável. |
| `ActiveVersionId` | ID da versão ativa. |
| `LatestVersionId` | ID da versão mais recente. |
| `Description` | Descrição. |
| `NamespacePrefix` | Namespace do pacote. |
| `ProcessType` | Tipo de Flow. |
| `Status` | Status geral. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### `FlowVersionView`

| Campo | Significado prático |
|---|---|
| `Id` | ID da versão. |
| `FlowDefinitionViewId` | Definição pai. |
| `VersionNumber` | Número da versão. |
| `Status` | `Active`, `Draft`, `Obsolete`. |
| `Label` | Label da versão. |
| `ApiVersion` | Versão da API. |
| `Description` | Descrição. |
| `IsTemplate` | Se é template. |

#### `FlowInterview`

| Campo | Significado prático |
|---|---|
| `Id` | ID da entrevista em execução. |
| `FlowVersionId` | Versão do Flow. |
| `OwnerId` | Usuário/dono. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query via API padrão

```sql
SELECT Id, ApiName, Label, ActiveVersionId, LatestVersionId,
       ProcessType, Status, NamespacePrefix,
       CreatedDate, LastModifiedDate
FROM FlowDefinitionView
ORDER BY LastModifiedDate DESC
```

```sql
SELECT Id, FlowDefinitionViewId, VersionNumber, Status, Label, ApiVersion
FROM FlowVersionView
WHERE FlowDefinitionView.ApiName = 'Meu_Flow'
ORDER BY VersionNumber DESC
```

```sql
SELECT Id, FlowVersionId, OwnerId, CreatedDate, LastModifiedDate
FROM FlowInterview
ORDER BY LastModifiedDate DESC
LIMIT 200
```

**Cuidados com permissões**: Flows podem ser sensíveis. Admins/perfis com `View Setup and Configuration` e permissões de Flow podem consultar.

**Paginação**: use `LIMIT`/`OFFSET` ou `nextRecordsUrl` quando houver muitos registros.

---

### 3.3 Objeto interno via Tooling API: `Flow`

Tooling API expõe `Flow` com suporte ao campo `Metadata` e `FullName`.

| Campo / funcionalidade | Significado prático |
|---|---|
| `Id` | ID do registro. |
| `FullName` | API Name completo (com namespace). |
| `DeveloperName` | API Name. |
| `Metadata` | Representação completa do Flow como estrutura Tooling. |
| `NamespacePrefix` | Namespace do pacote. |
| `ManageableState` | Estado de pacote gerenciado. |

#### Exemplo de query via Tooling API

```sql
SELECT Id, FullName, DeveloperName, NamespacePrefix, Metadata
FROM Flow
WHERE DeveloperName = 'Meu_Flow'
```

**Tratamento**: parse JSON em dict/Python ou `JSON.deserializeUntyped` em Apex.

**Limitações**:
- `Metadata` pode ser muito grande; atenção a limites de tamanho.
- Tooling API pode não expor todos os campos para managed packages.

---

### 3.4 Configuração observável em outras fontes

#### Setup / UI

- **Setup → Flows**: lista de Flows, status, versões ativas.
- **Flow Builder**: edição visual, elementos, conectores, variáveis.
- **Flow Definition Detail**: histórico de versões, ativação/desativação.

#### `SetupAuditTrail`

```sql
SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section
FROM SetupAuditTrail
WHERE Display LIKE '%Flow%'
ORDER BY CreatedDate DESC
LIMIT 200
```

#### `FlowTestResult`, `FlowTestView`

- Resultados de testes automatizados de Flow.

#### `ApexClass` / `CustomMetadata` / `ExternalServiceRegistration`

- Dependências do Flow: ações Apex, dados de configuração, external services.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Elementos e lógica | XML, Tooling Metadata | `FlowDefinitionView` (resumido) | Detalhe completo só no XML/Tooling. |
| Versões | XML (última/ativa), `FlowVersionView` | — | XML pode ter apenas a versão ativa/última conforme retrieve. |
| Interviews em execução | `FlowInterview` | XML/Metadata | Estado operacional. |
| Logs de debug de Flow | Debug Logs | XML/Metadata | Execução real. |
| Histórico de ativação | `SetupAuditTrail` | XML | Rastreabilidade. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `FlowDefinitionView` / `FlowVersionView`

- Importante para distinguir versão ativa da versão mais recente.
- Uma alteração no XML não entra em vigor até ser ativada.

### 4.2 `FlowInterview`

- Indica Screen Flows em execução.
- Importante para análise de adoção e depuração.

### 4.3 `ApexClass` com `@InvocableMethod`

- Ações Apex são dependências externas ao Flow.
- Alterações na assinatura da ação podem quebrar o Flow.

### 4.4 `ExternalServiceRegistration`

- Ações geradas automaticamente a partir de OpenAPI/Swagger.
- Ações dependem de Named Credential/External Credential.

### 4.5 `NamedCredential` / `ExternalCredential`

- Usados em HTTP Callout actions.
- Segredos não são expostos no XML do Flow.

### 4.6 `WorkflowRule` / `Process Builder` (legados)

- Flows modernos frequentemente substituem esses componentes.
- Importante mapear duplicidade ou automações conflitantes.

### 4.7 `CustomLabel`, `CustomMetadata`, `CustomSetting`

- Configurações e textos reutilizáveis no Flow.

### 4.8 `EmailTemplate`, `WorkflowAlert`

- Usados em ações de email do Flow.

---

## 5. Consultas e formas de extração

### 5.1 Query via API padrão

#### Flows

```sql
SELECT Id, ApiName, Label, ActiveVersionId, LatestVersionId,
       ProcessType, Status, NamespacePrefix,
       CreatedDate, LastModifiedDate
FROM FlowDefinitionView
ORDER BY LastModifiedDate DESC
```

#### Versões de um Flow

```sql
SELECT Id, FlowDefinitionViewId, FlowDefinitionView.ApiName,
       VersionNumber, Status, Label, ApiVersion, CreatedDate
FROM FlowVersionView
WHERE FlowDefinitionView.ApiName = 'Meu_Flow'
ORDER BY VersionNumber DESC
```

#### Interviews ativas

```sql
SELECT Id, FlowVersionId, OwnerId, CreatedDate, LastModifiedDate
FROM FlowInterview
ORDER BY LastModifiedDate DESC
LIMIT 200
```

### 5.2 Tooling API / Apex

Exemplo de chamada Tooling REST dentro de Apex:

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint(URL.getOrgDomainUrl().toExternalForm() +
                '/services/data/v59.0/tooling/query/?q=' +
                EncodingUtil.urlEncode(
                    'SELECT Id,FullName,DeveloperName,NamespacePrefix,Metadata FROM Flow WHERE DeveloperName = \'Meu_Flow\'',
                    'UTF-8'));
req.setMethod('GET');
req.setHeader('Authorization', 'OAuth ' + UserInfo.getSessionId());
Http http = new Http();
HttpResponse res = http.send(req);
System.debug(res.getBody());
```

---

## 6. Boas práticas e pontos de atenção

- **Separar versão ativa da versão mais recente**: um Flow salvo no metadata pode não estar ativo na org.
- **Não inferir negócio apenas pelo nome do elemento**: ler a lógica, condições e conectores.
- **Mapear fault paths**: garantir que haja tratamento de erro principalmente em DML e callouts.
- **Evitar recursão**: Record-Triggered Flows podem causar loops com outros Flows, Apex triggers e Workflow Rules.
- **Testar em sandbox**: especialmente para Record-Triggered Flows com before/after save.
- **Documentar propósito**: preencher `<description>` e manter inventário de automações.
- **Revisar permissões de Screen Flow**: usuários precisam ter acesso aos objetos/campos usados.
- **Atenção a HTTP Callouts**: verificar Named Credential, External Credential e timeouts.
- **Cuidado com subflows**: alterações no subflow impactam todos os Flows que o chamam.
- **Monitorar interviews**: Screen Flows parados podem indicar problemas de UX.
- **Migrar legados**: avaliar migração de Workflow Rules e Process Builder para Flows modernos.

---

## 7. Links de referência oficial

- [Salesforce Help — Flow Builder](https://help.salesforce.com/s/articleView?id=sf.flow.htm)
- [Salesforce Developer — Flow Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flow.htm)
- [Salesforce Developer — Tooling API Flow](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_flow.htm)
- [Salesforce Help — Record-Triggered Flows](https://help.salesforce.com/s/articleView?id=sf.flow_trigger.htm)
- [Salesforce Help — Screen Flows](https://help.salesforce.com/s/articleView?id=sf.flow_concepts_screen.htm)
- [Salesforce Help — Flow Best Practices](https://help.salesforce.com/s/articleView?id=sf.flow_bestpractices.htm)
- [Salesforce Help — Migrate Workflow Rules to Flows](https://help.salesforce.com/s/articleView?id=sf.flow_migrate_workflow.htm)
