# Guia de evidências no projeto

> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta.

Como reconhecer cada componente nos arquivos de um projeto Salesforce (cópia do repositório, sem acesso à org).
Os fatos foram conferidos na documentação oficial em 2026-10-30 (Metadata API Developer Guide Winter '27, API 68.0, e os guias citados). `nv` = não validado na fonte nesta coleta.

## 1. Formato do projeto

- **Metadata API format:** uma pasta por tipo (ex.: `namedCredentials/`), arquivo `Nome.<sufixo>`; código Apex vem em par (`X.cls` + `X.cls-meta.xml`).
- **Source format (Salesforce DX):** o XML de cada componente ganha `-meta.xml` (ex.: `Case.object-meta.xml`), e tipos como CustomObject são decompostos em subpastas (`objects/X/fields/Y.field-meta.xml`). Fonte: [DX-FMT](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_file_format.htm).
- Ao procurar um sufixo da tabela abaixo, aceite as duas formas: `.namedCredential` e `.namedCredential-meta.xml`.

## 2. Catálogo por metadata type

| Metadata type | Pasta | Sufixo (Metadata API format) | Desde a API | O que procurar no XML | Campos sensíveis (nunca copiar o valor) | Fonte |
|---|---|---|---|---|---|---|
| `NamedCredential` | `namedCredentials` | .namedCredential | 33.0 | `namedCredentialType` (SecuredEndpoint = modelo novo; Legacy = legado; PrivateEndpoint exige OutboundNetworkConnection); `namedCredentialParameters` com `parameterType` Url → `parameterValue` (URL), Authentication → `externalCredential`, ClientCertificate → `certificate`; legado: `endpoint`, `protocol`, `authProvider`; `calloutStatus` | password, oauthToken, oauthRefreshToken, awsAccessSecret (legado) | [MA-NC](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_namedcredential.htm) |
| `ExternalCredential` | `externalCredentials` | .externalCredential | 56.0 | `authenticationProtocol`; `externalCredentialParameters` com `parameterType` (NamedPrincipal/PerUserPrincipal + `principal`, AuthProvider + `authProvider`, AuthProviderUrl, AuthHeader, AuthParameter) | valores de parâmetros de autenticação | [MA-EC](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalcredential.htm) |
| `RemoteSiteSetting` | `remoteSiteSettings` | .remoteSite | 19.0 | `url`, `isActive`, `disableProtocolSecurity` | — | [MA-RSS](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_remotesitesetting.htm) |
| `CspTrustedSite` | `cspTrustedSites` | .cspTrustedSite | 39.0 | `endpointUrl`, `context` (All, LEX, Communities, VisualForce...), `isActive`, `isApplicableToConnectSrc`, `isApplicableToFrameSrc`, `isApplicableToImgSrc` | — | [MA-CSP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_csptrustedsite.htm) |
| `ConnectedApp` | `connectedApps` | .connectedApp | 29.0 | `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` | consumerSecret | [MA-CA](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_connectedapp.htm) |
| `ExternalClientApplication` | `externalClientApps` | .eca | 59.0 | `label`, `distributionState`, `contactEmail`; os plugins (OAuth, Canvas, políticas) ficam em arquivos próprios com `externalClientApplication` apontando para ele | — | [MA-ECA](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalclientapplication.htm) |
| `ExtlClntAppOauthSettings` | `extlClntAppOauthSettings` | .ecaOauth | 59.0 | `externalClientApplication`, `commaSeparatedOauthScopes` | — | [MA-ECAO](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappoauthsettings.htm) |
| `ExtlClntAppGlobalOauthSettings` | `extlClntAppGlobalOauthSets` | .ecaGlblOauth | 59.0 | `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` | consumerSecret | [MA-ECAG](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappglobaloauthsettings.htm) |
| `ExtlClntAppOauthConfigurablePolicies` | `extlClntAppOauthPolicies` | .ecaOauthPlcy | 59.0 | `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` | clientCredentialsFlowUser (nome de usuário) | [MA-ECAOP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappoauthconfigurablepolicies.htm) |
| `ExtlClntAppConfigurablePolicies` | `extlClntAppPolicies` | .ecaPlcy | 60.0 | `externalClientApplication` e habilitação do app/plugins | — | [MA-ECAP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappconfigurablepolicies.htm) |
| `ExtlClntAppCanvasSettings` | `extlClntAppCanvasSettings` | .ecaCanvas | 66.0 | configuração de Canvas do External Client App | — | [MA-ECAC](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappcanvassettings.htm) |
| `AuthProvider` | `authproviders` | .authprovider | 27.0 | `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) | consumerSecret | [MA-AP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_authproviders.htm) |
| `Certificate` | `certs` | .crt | 36.0 | nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` | chave privada (nunca versionar) | [MA-CERT](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_certificate.htm) |
| `OauthCustomScope` | `oauthcustomscopes` | .oauthcustomscope | 46.0 | escopo customizado referenciado pelo app | — | [MA-OCS](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_oauthcustomscope.htm) |
| `OauthTokenExchangeHandler` | `oauthtokenexchangehandlers` | .oauthtokenexchangehandler | 60.0 | `isAccessTokenSupported`, `developerName`, `enablements` | — | [MA-OTE](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_oauthtokenexchangehandler.htm) |
| `SamlSsoConfig` | `samlssoconfigs` | .samlssoconfig | 28.0 | emissor, certificado e mapeamento de identidade | — | [MA-SAML](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_samlssoconfig.htm) |
| `PermissionSet` | `permissionsets` | .permissionset | 22.0 | `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` | — | [MA-PS](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionset.htm) |
| `PermissionSetGroup` | `permissionsetgroups` | .permissionsetgroup (nv) | 45.0 | `permissionSets` agrupados | — | [MA-PSG](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionsetgroup.htm) |
| `Profile` | `profiles` | .profile | — | `classAccesses`, `userPermissions` (ex.: API habilitada) | — | [MA-PROF](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_profile.htm) |
| `ExternalServiceRegistration` | `externalServiceRegistrations` | .externalServiceRegistration | 39.0 | `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+; MuleSoft; Anypoint, 63.0+; ApexRest; Custom; Standard), `schema`, `schemaUrl`, `operations` | — | [MA-ESR](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalserviceregistration.htm) |
| `ExternalDataSource` | `dataSources` | .dataSource | 28.0 | `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` | password, oauthToken, oauthRefreshToken, username | [MA-EDS](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externaldatasource.htm) |
| `PlatformEventChannel` | `platformEventChannels` | .platformEventChannel | 45.0 | `channelType` (data = CDC; event = Platform Event), `label` | — | [MA-PEC](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_platformeventchannel.htm) |
| `PlatformEventChannelMember` | `platformEventChannelMembers` | .platformEventChannelMember | 47.0 | `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` | — | [MA-PECM](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_platformeventchannelmember.htm) |
| `PlatformEventSubscriberConfig` | `PlatformEventSubscriberConfigs` | .platformEventSubscriberConfig | 51.0 | `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` | user (nome de usuário) | [MA-PESC](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_platformeventsubscriberconfig.htm) |
| `EventRelayConfig` | `eventRelays` | .eventRelay | 56.0 | `destinationResourceName` (`callout:NomeNC`, guarda a conta AWS), `eventChannel` (`X__chn`), `relayOption`, `state` | — | [MA-ERC](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_eventrelayconfig.htm) |
| `ManagedEventSubscription` | `managedEventSubscriptions` | .managedEventSubscription | 60.0 (Beta) | `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` | — | [MA-MES](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_managedeventsubscription.htm) |
| `EmailServicesFunction` | `emailservices` | .xml | 42.0 | `apexClass`, `runAsUser`, `authorizedSenders`, `isAuthenticationRequired`, `emailServicesAddresses`, `isActive` | runAsUser (nome de usuário) | [MA-ESF](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_emailservicesfunction.htm) |
| `CustomSite` | `sites` | .site | — | `active`, `guestProfile`, `urlPathPrefix`, `siteType` | — | [MA-SITE](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_sites.htm) |
| `Network` | `networks` | .network | 28.0 | site do Experience Cloud | — | [MA-NET](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_network.htm) |
| `ExperienceBundle` | `experiences` | (bundle) | 46.0 | conteúdo do site Experience | — | [MA-EXB](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_experiencebundle.htm) |
| `DigitalExperienceBundle` | `digitalExperiences` | (bundle) | 56.0 | conteúdo do site Experience (LWR) | — | [MA-DEB](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_digitalexperiencebundle.htm) |
| `CustomMetadata` | `customMetadata` | .md | 31.0 | arquivo `Tipo.Registro.md`; `values` com `field`/`value`; `protected` | qualquer `value` de campo que guarde segredo | [MA-CMD](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_custommetadata.htm) |
| `CustomObject` | `objects` | .object | — | sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] | — | [MA-CO](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customobject.htm) |
| `CustomField` | `objects (dentro do objeto; decomposto no source format)` | — | — | `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` | — | [MA-CF](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customfield.htm) |
| `CustomLabels` | `labels` | CustomLabels.labels | 14.0 | rótulo com URL ou parâmetro de integração | valor do rótulo, se guardar segredo | [MA-LBL](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_customlabels.htm) |
| `PlatformCachePartition` | `cachePartitions` | .cachePartition | 35.0 | partição usada para cache de token/resposta | — | [MA-PCP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_platformcachepartition.htm) |
| `CustomNotificationType` | `notificationtypes` | .notiftype | 46.0 | tipo de notificação de falha | — | [MA-CNT](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_customnotificationtype.htm) |
| `CustomPermission` | `customPermissions` | .customPermission | 31.0 | permissão usada como interruptor | — | [MA-CP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_custompermission.htm) |
| `Workflow` | `workflows` | .workflow | — | `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` | integrationUser (nome de usuário) | [MA-WF](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_workflow.htm) |
| `Flow` | `flows (a página diz "Flow directory")` | .flow | 24.0 | `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` | — | [MA-FLOW](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_visual_workflow.htm) |
| `FlowDefinition` | `flowDefinitions` | .flowDefinition | — | versão ativa (formato legado) | — | [MA-FD](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flowdefinition.htm) |
| `QuickAction` | `quickActions` | .quickAction | 28.0 | `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` | — | [MA-QA](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_quickaction.htm) |
| `WebLink` | `objects (dentro do objeto)` | — | 12.0 | `linkType` (url, page, javascript), `url`, `openType`, `page` | — | [MA-WL](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_weblink.htm) |
| `CustomTab` | `tabs` | .tab | 10.0 | `url` (Web Tab), `page`, `lwcComponent`, `flexiPage`, `auraComponent` | — | [MA-TAB](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_tab.htm) |
| `FlexiPage` | `flexipages` | .flexipage | 29.0 | componentes da página (`componentName`) — LWC, FlexCard, Canvas | — | [MA-FP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flexipage.htm) |
| `Layout` | `layouts` | .layout (nv) | — | botões/ações e campos exibidos | — | [MA-LAY](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_layouts.htm) |
| `LightningComponentBundle` | `lwc` | (bundle: pasta com .js, .html, .js-meta.xml) | — | `targetConfigs` (onde aparece); no JS: C24 `@salesforce/apex/...` [LWC-IMP]; `lightning/empApi` e `fetch(` (nv) | — | [MA-LWC](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_lightningcomponentbundle.htm) |
| `ApexClass` | `classes` | .cls + .cls-meta.xml | — | ver padrões de código Apex | credenciais literais no código | [MA-CLS](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_classes.htm) |
| `ApexTrigger` | `triggers` | .trigger + -meta.xml | — | `trigger X on Objeto (...)`; em `X__e` ou `XChangeEvent` só `after insert` | — | [MA-TRG](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_triggers.htm) |
| `ApexPage` | `pages` | .page | — | `<apex:canvasApp>`, controller com Continuation | — | [MA-PAGE](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_pages.htm) |
| `OutboundNetworkConnection` | `outboundNetworkConnections` | .outboundNetworkConnection | 49.0 | conexão privada usada por NamedCredential PrivateEndpoint | — | [MA-ONC](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_outboundnetworkconnection.htm) |
| `CustomApplication` | `applications` | .app | 10.0 | app que agrupa abas | — | [MA-CAPP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_customapplication.htm) |
| `EmailTemplate` | `email` | (pasta por folder) | — | modelo de e-mail de notificação | — | [MA-ET](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_emailtemplate.htm) |

### Não confirmados

- `OmniDataTransform/OmniIntegrationProcedure/OmniScript/OmniUiCard`: não constam na lista de Metadata Types do Metadata API Developer Guide (API 68.0) [MA-TYPES]; pasta e sufixo não confirmados
- `Flow: Outbound Message como ação; callout em Flow disparado por evento ou agendado`: a fonte seria o help.salesforce.com, que não abre neste ambiente (depende de a.sfdcstatic.com, bloqueado pela rede)

## 3. Padrões de código Apex

| ID | Procure | Significa | Fonte |
|---|---|---|---|
| C01 | `callout:Nome` em `setEndpoint(...)` | callout via Named Credential; `Nome` = arquivo `namedCredentials/Nome.namedCredential` | [AX-NC](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_named_credentials.htm) |
| C02 | `new HttpRequest()`, `new Http().send(` | callout HTTP em Apex | [AX-HTTP](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_http.htm) |
| C03 | `setEndpoint('https://...')` literal | URL fixa; exige RemoteSiteSetting com o mesmo domínio | [AX-RSS](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_remote_site_settings.htm) |
| C04 | `setClientCertificateName('X')` | mutual TLS com Certificate X | [AX-CERT](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_client_certs_http.htm) |
| C05 | `setTimeout(n)` | timeout do callout (padrão 10 s; máx. 120.000 ms; 120 s acumulados por transação; 100 callouts por transação) | [AX-LIM](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_timeouts.htm) |
| C06 | `@future(callout=true)` | callout assíncrono via future | [AX-FUT](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_invoking_future_methods.htm) |
| C07 | `implements Queueable, Database.AllowsCallouts` / `System.enqueueJob(` | callout em Queueable (inclusive encadeado) | [AX-Q](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_queueing_jobs.htm) |
| C08 | `implements Database.Batchable<...>, Database.AllowsCallouts` | callout em Batch Apex | [AX-BATCH](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_batch_interface.htm) |
| C09 | `implements Schedulable` / `System.schedule(` | agendamento (o agendamento em si não é metadata) | [AX-SCH](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_scheduler.htm) |
| C10 | `implements System.Finalizer` / `System.attachFinalizer(` | tratamento de falha de Queueable | [AX-FIN](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_transaction_finalizers.htm) |
| C11 | `@RestResource(urlMapping='...')` + `@HttpGet/@HttpPost/...` | endpoint Apex REST (IN) em `/services/apexrest/...` | [AX-REST](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_rest_intro.htm) |
| C12 | `global` + métodos `webservice` | endpoint Apex SOAP (IN); `webservice` não pode estar em trigger | [AX-SOAP](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_web_services_methods_considerations.htm) |
| C13 | `implements Messaging.InboundEmailHandler` / `handleInboundEmail(` | e-mail inbound; ligado a EmailServicesFunction.apexClass | [AX-MAIL](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_email_inbound_using.htm) |
| C14 | `extends DataSource.Provider` / `extends DataSource.Connection` | adaptador Apex do Salesforce Connect | [AX-DSP](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_connector_start_provider_class.htm) |
| C15 | `WebServiceCallout.invoke(` / `endpoint_x` | stub SOAP gerado por WSDL2Apex | [AX-WSDL](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_wsdl2apex_gen_code.htm) |
| C16 | `ExternalService.<Servico>` | chamada Apex a External Service registrado | [AX-ES](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_external_services.htm) |
| C17 | `new Continuation(` / `continuationMethod` / `addHttpRequest(` | callout longo (Continuation): até 3 paralelos, 120 s | [AX-CONT](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_continuation_process.htm) |
| C18 | `EventBus.publish(` | publica Platform Event | [PE-PUB](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_publish_apex.htm) |
| C19 | `trigger X on Y__e (after insert)` | assinante Apex de Platform Event | [PE-SUB](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_subscribe_apex.htm) |
| C20 | `throw new EventBus.RetryableException(` | retry do trigger de evento (até 10 execuções: 1 + 9 retries) | [PE-RETRY](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_subscribe_apex_refire.htm) |
| C21 | `trigger X on YChangeEvent (after insert)` / `Y__ChangeEvent` | assinante Apex de Change Data Capture (roda como Automated Process) | [CDC-TRG](https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/cdc_trigger_intro.htm) |
| C22 | `@InvocableMethod(... callout=true ...)` | ação invocável que faz callout (modificador `callout`, usado por Screen Flow para decidir a transação) | [AX-INV](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_forcecom_flow_invocable_action_callout.htm) |
| C24 | `import x from '@salesforce/apex/Classe.metodo'` (com namespace se for de pacote) | LWC chama método Apex | [LWC-IMP](https://developer.salesforce.com/docs/platform/lwc/guide/apex-import-method.html) |
| C25 | `@AuraEnabled(continuation=true)` (opcionalmente `cacheable=true`) | método Apex chamado por LWC que devolve Continuation; máx. 3 callouts por Continuation e uma Continuation por vez no cliente | [LWC-CONT](https://developer.salesforce.com/docs/platform/lwc/guide/apex-continuations-auraenabled.html), [LWC-CONTL](https://developer.salesforce.com/docs/platform/lwc/guide/apex-continuations-limits.html) |
| C23 | `HttpCalloutMock`, `WebServiceMock`, `@IsTest` | classe de teste: **descartar** como ponto de integração | [AX-HTTP](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_http.htm) |

## 4. Evidência por eixo de variante

| Eixo | Variante | Evidência que a confirma |
|---|---|---|
| Endpoint | E1 | C01 `callout:Nome` + `Nome.namedCredential` com `namedCredentialType`=SecuredEndpoint e parâmetro Authentication → `externalCredential` |
| Endpoint | E2 | C01 `callout:Nome` + `Nome.namedCredential` com `namedCredentialType`=Legacy (campos `endpoint`, `protocol`) |
| Endpoint | E3 | C03 URL literal no código + `remoteSiteSettings/*.remoteSite` com o mesmo host |
| Endpoint | E4 | URL lida de `X__mdt` (L37) + registro em `customMetadata/` com a URL + Remote Site com o host |
| Endpoint | E5 | registro em `customMetadata/` cujo valor é o nome de uma Named Credential + `callout:` montado no código |
| Endpoint | E6 | URL vinda de Custom Setting (`objects/X__c` com tipo de setting) ou `labels/CustomLabels.labels` + Remote Site |
| Entrada | Connected App | `connectedApps/*.connectedApp` com `oauthConfig` |
| Entrada | External Client App | `externalClientApps/*.eca` + plugins (`.ecaOauth`, `.ecaGlblOauth`, `.ecaOauthPlcy`, `.ecaPlcy`) |
| Fluxo OAuth | Client Credentials | Connected App: `isClientCredentialEnabled` + `oauthClientCredentialUser`; ECA: `isClientCredentialsFlowEnabled` + `clientCredentialsFlowUser` |
| Fluxo OAuth | JWT Bearer | certificado no app (`oauthConfig.certificate` / `certificate` em `.ecaGlblOauth`) |
| Fluxo OAuth | Web Server / Username-Password | não distinguíveis pelo XML do app: a escolha fica no cliente externo (registrar como "não determinado") |
| Assíncrono | @future / Queueable / Batch / Flow assíncrono | C06 / C07 / C08 / `pathType`=AsyncAfterCommit |

Estas linhas aplicam o catálogo acima; não são uma página oficial única.

## 5. Coluna "Como achar no projeto" nos desenhos

Cada tabela de variante (out-sync.md, in-sync.md...) tem a coluna **Como achar no projeto**, gerada a partir deste guia: o código `Cnn` aponta para a seção 3 e o `[ID]` para a fonte.
