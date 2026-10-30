# Evidências no projeto (item 1). Fatos conferidos na documentação oficial em 2026-10-30
# (Metadata API Developer Guide Winter '27 / API 68.0 e guias citados). "nv" = não validado na fonte.
MA = "https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/{}.htm"
AX = "https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/{}.htm"
PE = "https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/{}.htm"
CDC = "https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/{}.htm"
DX = "https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/{}.htm"

FONTES = {
 "MA-NC": MA.format("meta_namedcredential"), "MA-EC": MA.format("meta_externalcredential"),
 "MA-RSS": MA.format("meta_remotesitesetting"), "MA-CSP": MA.format("meta_csptrustedsite"),
 "MA-CA": MA.format("meta_connectedapp"), "MA-ECA": MA.format("meta_externalclientapplication"),
 "MA-ECAO": MA.format("meta_extlclntappoauthsettings"), "MA-ECAG": MA.format("meta_extlclntappglobaloauthsettings"),
 "MA-ECAOP": MA.format("meta_extlclntappoauthconfigurablepolicies"), "MA-ECAP": MA.format("meta_extlclntappconfigurablepolicies"),
 "MA-ECAC": MA.format("meta_extlclntappcanvassettings"), "MA-AP": MA.format("meta_authproviders"),
 "MA-CERT": MA.format("meta_certificate"), "MA-OCS": MA.format("meta_oauthcustomscope"),
 "MA-OTE": MA.format("meta_oauthtokenexchangehandler"), "MA-SAML": MA.format("meta_samlssoconfig"),
 "MA-PS": MA.format("meta_permissionset"), "MA-PSG": MA.format("meta_permissionsetgroup"), "MA-PROF": MA.format("meta_profile"),
 "MA-ESR": MA.format("meta_externalserviceregistration"), "MA-EDS": MA.format("meta_externaldatasource"),
 "MA-PEC": MA.format("meta_platformeventchannel"), "MA-PECM": MA.format("meta_platformeventchannelmember"),
 "MA-PESC": MA.format("meta_platformeventsubscriberconfig"), "MA-ERC": MA.format("meta_eventrelayconfig"),
 "MA-MES": MA.format("meta_managedeventsubscription"), "MA-ESF": MA.format("meta_emailservicesfunction"),
 "MA-SITE": MA.format("meta_sites"), "MA-NET": MA.format("meta_network"), "MA-CMD": MA.format("meta_custommetadata"),
 "MA-CO": MA.format("customobject"), "MA-CF": MA.format("customfield"), "MA-LBL": MA.format("meta_customlabels"),
 "MA-PCP": MA.format("meta_platformcachepartition"), "MA-CNT": MA.format("meta_customnotificationtype"),
 "MA-WF": MA.format("meta_workflow"), "MA-FLOW": MA.format("meta_visual_workflow"), "MA-FD": MA.format("meta_flowdefinition"),
 "MA-QA": MA.format("meta_quickaction"), "MA-WL": MA.format("meta_weblink"), "MA-TAB": MA.format("meta_tab"),
 "MA-FP": MA.format("meta_flexipage"), "MA-LAY": MA.format("meta_layouts"), "MA-LWC": MA.format("meta_lightningcomponentbundle"),
 "MA-CLS": MA.format("meta_classes"), "MA-TRG": MA.format("meta_triggers"), "MA-PAGE": MA.format("meta_pages"),
 "MA-ONC": MA.format("meta_outboundnetworkconnection"), "MA-CP": MA.format("meta_custompermission"),
 "MA-ET": MA.format("meta_emailtemplate"), "MA-EXB": MA.format("meta_experiencebundle"), "MA-DEB": MA.format("meta_digitalexperiencebundle"),
 "MA-TYPES": MA.format("meta_types_list"), "MA-CAPP": MA.format("meta_customapplication"),
 "AX-TRG": AX.format("apex_triggers"), "AX-LIM": AX.format("apex_callouts_timeouts"), "AX-NC": AX.format("apex_callouts_named_credentials"),
 "AX-RSS": AX.format("apex_callouts_remote_site_settings"), "AX-HTTP": AX.format("apex_callouts_http"),
 "AX-CERT": AX.format("apex_callouts_client_certs_http"), "AX-FUT": AX.format("apex_invoking_future_methods"),
 "AX-Q": AX.format("apex_queueing_jobs"), "AX-FIN": AX.format("apex_transaction_finalizers"), "AX-BATCH": AX.format("apex_batch_interface"),
 "AX-SCH": AX.format("apex_scheduler"), "AX-REST": AX.format("apex_rest_intro"), "AX-SOAP": AX.format("apex_web_services_methods_considerations"),
 "AX-MAIL": AX.format("apex_classes_email_inbound_using"), "AX-DSP": AX.format("apex_connector_start_provider_class"),
 "AX-DSC": AX.format("apex_connector_start_connection_class"), "AX-WSDL": AX.format("apex_callouts_wsdl2apex_gen_code"),
 "AX-ES": AX.format("apex_external_services"), "AX-CONT": AX.format("apex_continuation_process"), "AX-CONTL": AX.format("apex_continuation_limits"),
 "AX-INV": AX.format("apex_forcecom_flow_invocable_action_callout"),
 "PE-PUB": PE.format("platform_events_publish_apex"), "PE-SUB": PE.format("platform_events_subscribe_apex"),
 "PE-RETRY": PE.format("platform_events_subscribe_apex_refire"), "PE-FLOW": PE.format("platform_events_subscribe_flow"),
 "PE-CFG": PE.format("platform_events_trigger_config"),
 "CDC-SEL": CDC.format("cdc_object_selections_metadata"), "CDC-TRG": CDC.format("cdc_trigger_intro"), "CDC-CH": CDC.format("cdc_subscribe_channels"),
 "DX-FMT": DX.format("sfdx_dev_source_file_format"),
}

# Catálogo por metadata type: pasta, sufixo (formato Metadata API), versão, o que procurar no XML, campos sensíveis, fonte.
# No source format a plataforma gera o XML com "-meta.xml" (ex.: Case.object-meta.xml) [DX-FMT].
TIPOS = {
 "NamedCredential": ("namedCredentials", ".namedCredential", "33.0", "`namedCredentialType` (SecuredEndpoint = modelo novo; Legacy = legado; PrivateEndpoint exige OutboundNetworkConnection); `namedCredentialParameters` com `parameterType` Url → `parameterValue` (URL), Authentication → `externalCredential`, ClientCertificate → `certificate`; legado: `endpoint`, `protocol`, `authProvider`; `calloutStatus`", "password, oauthToken, oauthRefreshToken, awsAccessSecret (legado)", "MA-NC"),
 "ExternalCredential": ("externalCredentials", ".externalCredential", "56.0", "`authenticationProtocol`; `externalCredentialParameters` com `parameterType` (NamedPrincipal/PerUserPrincipal + `principal`, AuthProvider + `authProvider`, AuthProviderUrl, AuthHeader, AuthParameter)", "valores de parâmetros de autenticação", "MA-EC"),
 "RemoteSiteSetting": ("remoteSiteSettings", ".remoteSite", "19.0", "`url`, `isActive`, `disableProtocolSecurity`", "—", "MA-RSS"),
 "CspTrustedSite": ("cspTrustedSites", ".cspTrustedSite", "39.0", "`endpointUrl`, `context` (All, LEX, Communities, VisualForce...), `isActive`, `isApplicableToConnectSrc`, `isApplicableToFrameSrc`, `isApplicableToImgSrc`", "—", "MA-CSP"),
 "ConnectedApp": ("connectedApps", ".connectedApp", "29.0", "`oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig`", "consumerSecret", "MA-CA"),
 "ExternalClientApplication": ("externalClientApps", ".eca", "59.0", "`label`, `distributionState`, `contactEmail`; os plugins (OAuth, Canvas, políticas) ficam em arquivos próprios com `externalClientApplication` apontando para ele", "—", "MA-ECA"),
 "ExtlClntAppOauthSettings": ("extlClntAppOauthSettings", ".ecaOauth", "59.0", "`externalClientApplication`, `commaSeparatedOauthScopes`", "—", "MA-ECAO"),
 "ExtlClntAppGlobalOauthSettings": ("extlClntAppGlobalOauthSets", ".ecaGlblOauth", "59.0", "`externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired`", "consumerSecret", "MA-ECAG"),
 "ExtlClntAppOauthConfigurablePolicies": ("extlClntAppOauthPolicies", ".ecaOauthPlcy", "59.0", "`externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes`", "clientCredentialsFlowUser (nome de usuário)", "MA-ECAOP"),
 "ExtlClntAppConfigurablePolicies": ("extlClntAppPolicies", ".ecaPlcy", "60.0", "`externalClientApplication` e habilitação do app/plugins", "—", "MA-ECAP"),
 "ExtlClntAppCanvasSettings": ("extlClntAppCanvasSettings", ".ecaCanvas", "66.0", "configuração de Canvas do External Client App", "—", "MA-ECAC"),
 "AuthProvider": ("authproviders", ".authprovider", "27.0", "`providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`)", "consumerSecret", "MA-AP"),
 "Certificate": ("certs", ".crt", "36.0", "nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName`", "chave privada (nunca versionar)", "MA-CERT"),
 "OauthCustomScope": ("oauthcustomscopes", ".oauthcustomscope", "46.0", "escopo customizado referenciado pelo app", "—", "MA-OCS"),
 "OauthTokenExchangeHandler": ("oauthtokenexchangehandlers", ".oauthtokenexchangehandler", "60.0", "`isAccessTokenSupported`, `developerName`, `enablements`", "—", "MA-OTE"),
 "SamlSsoConfig": ("samlssoconfigs", ".samlssoconfig", "28.0", "emissor, certificado e mapeamento de identidade", "—", "MA-SAML"),
 "PermissionSet": ("permissionsets", ".permissionset", "22.0", "`classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions`", "—", "MA-PS"),
 "PermissionSetGroup": ("permissionsetgroups", ".permissionsetgroup (nv)", "45.0", "`permissionSets` agrupados", "—", "MA-PSG"),
 "Profile": ("profiles", ".profile", "—", "`classAccesses`, `userPermissions` (ex.: API habilitada)", "—", "MA-PROF"),
 "ExternalServiceRegistration": ("externalServiceRegistrations", ".externalServiceRegistration", "39.0", "`namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+; MuleSoft; Anypoint, 63.0+; ApexRest; Custom; Standard), `schema`, `schemaUrl`, `operations`", "—", "MA-ESR"),
 "ExternalDataSource": ("dataSources", ".dataSource", "28.0", "`type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration`", "password, oauthToken, oauthRefreshToken, username", "MA-EDS"),
 "PlatformEventChannel": ("platformEventChannels", ".platformEventChannel", "45.0", "`channelType` (data = CDC; event = Platform Event), `label`", "—", "MA-PEC"),
 "PlatformEventChannelMember": ("platformEventChannelMembers", ".platformEventChannelMember", "47.0", "`eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression`", "—", "MA-PECM"),
 "PlatformEventSubscriberConfig": ("PlatformEventSubscriberConfigs", ".platformEventSubscriberConfig", "51.0", "`platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey`", "user (nome de usuário)", "MA-PESC"),
 "EventRelayConfig": ("eventRelays", ".eventRelay", "56.0", "`destinationResourceName` (`callout:NomeNC`, guarda a conta AWS), `eventChannel` (`X__chn`), `relayOption`, `state`", "—", "MA-ERC"),
 "ManagedEventSubscription": ("managedEventSubscriptions", ".managedEventSubscription", "60.0 (Beta)", "`topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state`", "—", "MA-MES"),
 "EmailServicesFunction": ("emailservices", ".xml", "42.0", "`apexClass`, `runAsUser`, `authorizedSenders`, `isAuthenticationRequired`, `emailServicesAddresses`, `isActive`", "runAsUser (nome de usuário)", "MA-ESF"),
 "CustomSite": ("sites", ".site", "—", "`active`, `guestProfile`, `urlPathPrefix`, `siteType`", "—", "MA-SITE"),
 "Network": ("networks", ".network", "28.0", "site do Experience Cloud", "—", "MA-NET"),
 "ExperienceBundle": ("experiences", "(bundle)", "46.0", "conteúdo do site Experience", "—", "MA-EXB"),
 "DigitalExperienceBundle": ("digitalExperiences", "(bundle)", "56.0", "conteúdo do site Experience (LWR)", "—", "MA-DEB"),
 "CustomMetadata": ("customMetadata", ".md", "31.0", "arquivo `Tipo.Registro.md`; `values` com `field`/`value`; `protected`", "qualquer `value` de campo que guarde segredo", "MA-CMD"),
 "CustomObject": ("objects", ".object", "—", "sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD]", "—", "MA-CO"),
 "CustomField": ("objects (dentro do objeto; decomposto no source format)", "—", "—", "`externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo`", "—", "MA-CF"),
 "CustomLabels": ("labels", "CustomLabels.labels", "14.0", "rótulo com URL ou parâmetro de integração", "valor do rótulo, se guardar segredo", "MA-LBL"),
 "PlatformCachePartition": ("cachePartitions", ".cachePartition", "35.0", "partição usada para cache de token/resposta", "—", "MA-PCP"),
 "CustomNotificationType": ("notificationtypes", ".notiftype", "46.0", "tipo de notificação de falha", "—", "MA-CNT"),
 "CustomPermission": ("customPermissions", ".customPermission", "31.0", "permissão usada como interruptor", "—", "MA-CP"),
 "Workflow": ("workflows", ".workflow", "—", "`outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage`", "integrationUser (nome de usuário)", "MA-WF"),
 "Flow": ("flows (a página diz \"Flow directory\")", ".flow", "24.0", "`start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e`", "—", "MA-FLOW"),
 "FlowDefinition": ("flowDefinitions", ".flowDefinition", "—", "versão ativa (formato legado)", "—", "MA-FD"),
 "QuickAction": ("quickActions", ".quickAction", "28.0", "`type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype`", "—", "MA-QA"),
 "WebLink": ("objects (dentro do objeto)", "—", "12.0", "`linkType` (url, page, javascript), `url`, `openType`, `page`", "—", "MA-WL"),
 "CustomTab": ("tabs", ".tab", "10.0", "`url` (Web Tab), `page`, `lwcComponent`, `flexiPage`, `auraComponent`", "—", "MA-TAB"),
 "FlexiPage": ("flexipages", ".flexipage", "29.0", "componentes da página (`componentName`) — LWC, FlexCard, Canvas", "—", "MA-FP"),
 "Layout": ("layouts", ".layout (nv)", "—", "botões/ações e campos exibidos", "—", "MA-LAY"),
 "LightningComponentBundle": ("lwc", "(bundle: pasta com .js, .html, .js-meta.xml)", "—", "`targetConfigs` (onde aparece); no JS: `import ... from '@salesforce/apex/...'`, `lightning/empApi`, `fetch(` (nv: padrões de código JS)", "—", "MA-LWC"),
 "ApexClass": ("classes", ".cls + .cls-meta.xml", "—", "ver padrões de código Apex", "credenciais literais no código", "MA-CLS"),
 "ApexTrigger": ("triggers", ".trigger + -meta.xml", "—", "`trigger X on Objeto (...)`; em `X__e` ou `XChangeEvent` só `after insert`", "—", "MA-TRG"),
 "ApexPage": ("pages", ".page", "—", "`<apex:canvasApp>`, controller com Continuation", "—", "MA-PAGE"),
 "OutboundNetworkConnection": ("outboundNetworkConnections", ".outboundNetworkConnection", "49.0", "conexão privada usada por NamedCredential PrivateEndpoint", "—", "MA-ONC"),
 "CustomApplication": ("applications", ".app", "10.0", "app que agrupa abas", "—", "MA-CAPP"),
 "EmailTemplate": ("email", "(pasta por folder)", "—", "modelo de e-mail de notificação", "—", "MA-ET"),
}

NAO_CONFIRMADOS = {
 "OmniDataTransform/OmniIntegrationProcedure/OmniScript/OmniUiCard": "não constam na lista de Metadata Types do Metadata API Developer Guide (API 68.0) [MA-TYPES]; pasta e sufixo não confirmados",
}

# Padrões de código: (id, padrão a procurar, o que significa, fonte)
CODIGO = [
 ("C01", "`callout:Nome` em `setEndpoint(...)`", "callout via Named Credential; `Nome` = arquivo `namedCredentials/Nome.namedCredential`", "AX-NC"),
 ("C02", "`new HttpRequest()`, `new Http().send(`", "callout HTTP em Apex", "AX-HTTP"),
 ("C03", "`setEndpoint('https://...')` literal", "URL fixa; exige RemoteSiteSetting com o mesmo domínio", "AX-RSS"),
 ("C04", "`setClientCertificateName('X')`", "mutual TLS com Certificate X", "AX-CERT"),
 ("C05", "`setTimeout(n)`", "timeout do callout (padrão 10 s; máx. 120.000 ms; 120 s acumulados por transação; 100 callouts por transação)", "AX-LIM"),
 ("C06", "`@future(callout=true)`", "callout assíncrono via future", "AX-FUT"),
 ("C07", "`implements Queueable, Database.AllowsCallouts` / `System.enqueueJob(`", "callout em Queueable (inclusive encadeado)", "AX-Q"),
 ("C08", "`implements Database.Batchable<...>, Database.AllowsCallouts`", "callout em Batch Apex", "AX-BATCH"),
 ("C09", "`implements Schedulable` / `System.schedule(`", "agendamento (o agendamento em si não é metadata)", "AX-SCH"),
 ("C10", "`implements System.Finalizer` / `System.attachFinalizer(`", "tratamento de falha de Queueable", "AX-FIN"),
 ("C11", "`@RestResource(urlMapping='...')` + `@HttpGet/@HttpPost/...`", "endpoint Apex REST (IN) em `/services/apexrest/...`", "AX-REST"),
 ("C12", "`global` + métodos `webservice`", "endpoint Apex SOAP (IN); `webservice` não pode estar em trigger", "AX-SOAP"),
 ("C13", "`implements Messaging.InboundEmailHandler` / `handleInboundEmail(`", "e-mail inbound; ligado a EmailServicesFunction.apexClass", "AX-MAIL"),
 ("C14", "`extends DataSource.Provider` / `extends DataSource.Connection`", "adaptador Apex do Salesforce Connect", "AX-DSP"),
 ("C15", "`WebServiceCallout.invoke(` / `endpoint_x`", "stub SOAP gerado por WSDL2Apex", "AX-WSDL"),
 ("C16", "`ExternalService.<Servico>`", "chamada Apex a External Service registrado", "AX-ES"),
 ("C17", "`new Continuation(` / `continuationMethod` / `addHttpRequest(`", "callout longo (Continuation): até 3 paralelos, 120 s", "AX-CONT"),
 ("C18", "`EventBus.publish(`", "publica Platform Event", "PE-PUB"),
 ("C19", "`trigger X on Y__e (after insert)`", "assinante Apex de Platform Event", "PE-SUB"),
 ("C20", "`throw new EventBus.RetryableException(`", "retry do trigger de evento (até 10 execuções: 1 + 9 retries)", "PE-RETRY"),
 ("C21", "`trigger X on YChangeEvent (after insert)` / `Y__ChangeEvent`", "assinante Apex de Change Data Capture (roda como Automated Process)", "CDC-TRG"),
 ("C22", "`@InvocableMethod(... callout=true ...)`", "ação invocável que faz callout (modificador `callout`, usado por Screen Flow para decidir a transação)", "AX-INV"),
 ("C23", "`HttpCalloutMock`, `WebServiceMock`, `@IsTest`", "classe de teste: **descartar** como ponto de integração", "AX-HTTP"),
]

def evid(comp, mtype):
    """Texto curto: como achar o componente no projeto."""
    c = comp.lower()
    rules = [
     ("método @future", "C06 `@future(callout=true)` em `classes/*.cls`"),
     ("queueable", "C07 `implements Queueable, Database.AllowsCallouts`"),
     ("finalizer", "C10 `implements System.Finalizer`"),
     ("batch", "C08 `Database.Batchable` + `Database.AllowsCallouts`"),
     ("schedulable", "C09 `implements Schedulable`"),
     ("apex rest", "C11 `@RestResource(urlMapping=...)`"),
     ("apex soap", "C12 `global` + `webservice`"),
     ("handler" if "email" in c else "§§", "C13 `Messaging.InboundEmailHandler`"),
     ("stub gerado", "C15 `WebServiceCallout.invoke` / `endpoint_x`"),
     ("provider do adaptador", "C14 `extends DataSource.Provider`"),
     ("connection do adaptador", "C14 `extends DataSource.Connection`"),
     ("callback", "C17 método indicado em `continuationMethod`"),
     ("classe invocável", "C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo)"),
     ("classe publicadora", "C18 `EventBus.publish(`"),
     ("trigger do evento", "C19 `trigger ... on X__e (after insert)`"),
     ("trigger do change event", "C21 `trigger ... on XChangeEvent (after insert)`"),
     ("registration handler", "AuthProvider.`registrationHandler`; classe implementa `Auth.RegistrationHandler`"),
     ("cliente http", "C02 `new HttpRequest()` + C01/C03"),
     ("controller apex", "`@AuraEnabled` em `classes/*.cls` + C02 se fizer callout"),
     ("classe de serviço", "L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`)"),
     ("classes de serviço", "L38 chamada a partir da classe de entrada"),
     ("classe de token", "C02 callout ao endpoint de token; lê CMDT"),
    ]
    for k, v in rules:
        if k in c:
            return v
    if mtype.startswith("não é metadata"):
        return "não aparece no projeto (ator)"
    if "Platform Event" == comp or "__e" in mtype:
        return "`objects/X__e/` (sufixo `__e`) [PE-PUB]"
    if "External Object" in comp:
        return "`objects/X__x/` (sufixo `__x`) [MA-CO]"
    if "Custom Metadata" in comp or "__mdt" in mtype:
        return "tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD]"
    if "External ID" in comp:
        return "`<externalId>true</externalId>` no campo [MA-CF]"
    import re as _re
    partes = [p.strip() for p in _re.split(r",| ou |/", mtype)]
    achados = []
    for p in partes:
        t = p.split(" ")[0]
        if t in TIPOS:
            pasta, suf, _v, xml, _s, f = TIPOS[t]
            achados.append(f"`{pasta}/*{suf if suf.startswith('.') else ''}` [{f}]")
    if len(achados) == 1 and len(partes) == 1:
        t = partes[0].split(" ")[0]
        return f"{achados[0][:-len(TIPOS[t][5])-3]} — {TIPOS[t][3].split(';')[0]} [{TIPOS[t][5]}]"
    if achados:
        return " ou ".join(achados)
    if mtype.startswith("Omni"):
        return "não confirmado (ver NAO_CONFIRMADOS)"
    return "ver catálogo de tipos"
