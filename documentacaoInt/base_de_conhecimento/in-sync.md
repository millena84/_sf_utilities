# IN SYNC — externo chama o Salesforce e espera

> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta.

Convenções, legenda e códigos de variante: [README](README.md). Fontes citadas entre colchetes: [fontes_validacao.md](fontes_validacao.md).

## Índice

- [g.1 — Sistema externo → REST/SOAP API padrão (CRUD)](#g1) (8 variantes)
- [g.2 — Sistema externo → Composite / sObject Tree / Collections](#g2) (8 variantes)
- [g.3 — Sistema externo → Apex REST customizado](#g3) (8 variantes)
- [g.4 — Sistema externo → Apex SOAP customizado](#g4) (8 variantes)
- [g.5 — Sistema externo → Flow via REST (Actions)](#g5) (8 variantes)
- [g.6 — Webhook público → Site → Apex REST](#g6) (6 variantes)
- [g.7 — Sistema externo → GraphQL API](#g7) (8 variantes)

## g.1

**Sistema externo → REST/SOAP API padrão (CRUD)**

Sem código na org; o sistema externo grava ou lê objetos diretamente.

### g.1.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST/SOAP API padrão | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST/SOAP API padrão | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.1.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → REST/SOAP API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST/SOAP API padrão | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST/SOAP API padrão | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.1.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST/SOAP API padrão | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Web Server + Refresh Token e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST/SOAP API padrão | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.1.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST/SOAP API padrão | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Username-Password (legado, desaconselhado) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST/SOAP API padrão | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.1.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST/SOAP API padrão | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST/SOAP API padrão | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.1.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → REST/SOAP API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST/SOAP API padrão | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST/SOAP API padrão | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.1.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST/SOAP API padrão | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Web Server + Refresh Token | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST/SOAP API padrão | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.1.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST/SOAP API padrão | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Username-Password (legado, desaconselhado) | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST/SOAP API padrão | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.2

**Sistema externo → Composite / sObject Tree / Collections**

Várias operações em uma chamada.

### g.2.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Composite API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Composite API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.2.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → Composite API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Composite API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Composite API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.2.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Composite API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Web Server + Refresh Token e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Composite API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.2.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Composite API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Username-Password (legado, desaconselhado) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Composite API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.2.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Composite API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | Composite API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.2.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → Composite API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Composite API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Composite API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.2.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Composite API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Web Server + Refresh Token | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Composite API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.2.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Composite API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Username-Password (legado, desaconselhado) | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Composite API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.3

**Sistema externo → Apex REST customizado**

Endpoint próprio com regra de negócio.

### g.3.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST (/services/apexrest) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 10 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 11 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.3.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST (/services/apexrest) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.3.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST (/services/apexrest) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Web Server + Refresh Token e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.3.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST (/services/apexrest) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Username-Password (legado, desaconselhado) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.3.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST (/services/apexrest) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 14 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 15 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 17 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 19 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 20 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.3.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST (/services/apexrest) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.3.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST (/services/apexrest) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Web Server + Refresh Token | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.3.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST (/services/apexrest) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Username-Password (legado, desaconselhado) | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.4

**Sistema externo → Apex SOAP customizado**

Equivalente SOAP com WSDL gerado.

### g.4.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a SOAP API customizada (/services/Soap/class) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 9 | Classe Apex SOAP | ApexClass | executa | `global` com métodos `webservice`; WSDL gerado pela plataforma | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.4.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a SOAP API customizada (/services/Soap/class) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 8 | Classe Apex SOAP | ApexClass | executa | `global` com métodos `webservice`; WSDL gerado pela plataforma | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 9 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.4.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a SOAP API customizada (/services/Soap/class) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Web Server + Refresh Token e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 8 | Classe Apex SOAP | ApexClass | executa | `global` com métodos `webservice`; WSDL gerado pela plataforma | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 9 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.4.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a SOAP API customizada (/services/Soap/class) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Username-Password (legado, desaconselhado) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 8 | Classe Apex SOAP | ApexClass | executa | `global` com métodos `webservice`; WSDL gerado pela plataforma | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 9 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.4.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a SOAP API customizada (/services/Soap/class) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 13 | Classe Apex SOAP | ApexClass | executa | `global` com métodos `webservice`; WSDL gerado pela plataforma | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.4.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a SOAP API customizada (/services/Soap/class) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 12 | Classe Apex SOAP | ApexClass | executa | `global` com métodos `webservice`; WSDL gerado pela plataforma | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 13 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.4.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a SOAP API customizada (/services/Soap/class) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Web Server + Refresh Token | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 12 | Classe Apex SOAP | ApexClass | executa | `global` com métodos `webservice`; WSDL gerado pela plataforma | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 13 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.4.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a SOAP API customizada (/services/Soap/class) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Username-Password (legado, desaconselhado) | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 12 | Classe Apex SOAP | ApexClass | executa | `global` com métodos `webservice`; WSDL gerado pela plataforma | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 13 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.5

**Sistema externo → Flow via REST (Actions)**

Dispara um autolaunched Flow.

### g.5.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (Actions) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (Actions) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 9 | Flow autolaunched | Flow | executa | invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 10 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | libera a execução do Flow | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.5.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → REST API (Actions) → Flow autolaunched → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (Actions) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (Actions) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 8 | Flow autolaunched | Flow | executa | invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 9 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | libera a execução do Flow | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.5.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (Actions) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Web Server + Refresh Token e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (Actions) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 8 | Flow autolaunched | Flow | executa | invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 9 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | libera a execução do Flow | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.5.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (Actions) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Username-Password (legado, desaconselhado) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (Actions) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 8 | Flow autolaunched | Flow | executa | invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 9 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | libera a execução do Flow | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.5.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (Actions) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST API (Actions) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 13 | Flow autolaunched | Flow | executa | invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 14 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | libera a execução do Flow | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.5.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → REST API (Actions) → Flow autolaunched → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (Actions) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (Actions) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 12 | Flow autolaunched | Flow | executa | invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 13 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | libera a execução do Flow | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.5.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (Actions) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Web Server + Refresh Token | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (Actions) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 12 | Flow autolaunched | Flow | executa | invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 13 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | libera a execução do Flow | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.5.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (Actions) | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Username-Password (legado, desaconselhado) | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (Actions) | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 12 | Flow autolaunched | Flow | executa | invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 13 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | libera a execução do Flow | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.6

**Webhook público → Site → Apex REST**

Sem OAuth: a confiança vem de assinatura/token no payload.

> Observação: Usuário guest tem restrições de compartilhamento e de acesso; avalie o risco antes de usar.

### g.6.v1 — Site público · validação nenhuma (não recomendado)

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | envia o webhook (POST) sem OAuth | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site público | CustomSite | lê/referencia | domínio público que expõe `/services/apexrest` | Sistema externo | Classe Apex REST | Obrigatório | `sites/*.site` — `active`, `guestProfile`, `urlPathPrefix`, `siteType` [MA-SITE] |
| 3 | Perfil guest do site | Profile | autoriza | acesso da classe e dos objetos para o usuário guest | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | recebe o webhook, valida, grava ou enfileira | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 6 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 8 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 9 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.6.v2 — Site público · validação segredo em Custom Metadata

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | envia o webhook (POST) sem OAuth | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site público | CustomSite | lê/referencia | domínio público que expõe `/services/apexrest` | Sistema externo | Classe Apex REST | Obrigatório | `sites/*.site` — `active`, `guestProfile`, `urlPathPrefix`, `siteType` [MA-SITE] |
| 3 | Perfil guest do site | Profile | autoriza | acesso da classe e dos objetos para o usuário guest | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | recebe o webhook, valida, grava ou enfileira | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Registro de Custom Metadata (protegido) | CustomMetadata (+ CustomObject __mdt) | lê/referencia | segredo/token para validar assinatura HMAC. Risco: ver README | Classe Apex REST | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 7 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 8 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 9 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.6.v3 — Site público · validação segredo em Custom Setting

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | envia o webhook (POST) sem OAuth | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site público | CustomSite | lê/referencia | domínio público que expõe `/services/apexrest` | Sistema externo | Classe Apex REST | Obrigatório | `sites/*.site` — `active`, `guestProfile`, `urlPathPrefix`, `siteType` [MA-SITE] |
| 3 | Perfil guest do site | Profile | autoriza | acesso da classe e dos objetos para o usuário guest | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | recebe o webhook, valida, grava ou enfileira | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Custom Setting protegido | CustomObject (Custom Setting) | lê/referencia | segredo para validar assinatura | Classe Apex REST | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 7 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 8 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 9 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.6.v4 — Experience Cloud · validação nenhuma (não recomendado)

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | envia o webhook (POST) sem OAuth | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site Experience Cloud | Network + ExperienceBundle/DigitalExperienceBundle + CustomSite | lê/referencia | site do Experience com acesso guest | Sistema externo | Classe Apex REST | Obrigatório | `networks/*.network` [MA-NET] ou `digitalExperiences/*` [MA-DEB] |
| 3 | Perfil guest do site | Profile | autoriza | acesso da classe e dos objetos para o usuário guest | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | recebe o webhook, valida, grava ou enfileira | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 6 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 8 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 9 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.6.v5 — Experience Cloud · validação segredo em Custom Metadata

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | envia o webhook (POST) sem OAuth | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site Experience Cloud | Network + ExperienceBundle/DigitalExperienceBundle + CustomSite | lê/referencia | site do Experience com acesso guest | Sistema externo | Classe Apex REST | Obrigatório | `networks/*.network` [MA-NET] ou `digitalExperiences/*` [MA-DEB] |
| 3 | Perfil guest do site | Profile | autoriza | acesso da classe e dos objetos para o usuário guest | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | recebe o webhook, valida, grava ou enfileira | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Registro de Custom Metadata (protegido) | CustomMetadata (+ CustomObject __mdt) | lê/referencia | segredo/token para validar assinatura HMAC. Risco: ver README | Classe Apex REST | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 7 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 8 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 9 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.6.v6 — Experience Cloud · validação segredo em Custom Setting

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | envia o webhook (POST) sem OAuth | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site Experience Cloud | Network + ExperienceBundle/DigitalExperienceBundle + CustomSite | lê/referencia | site do Experience com acesso guest | Sistema externo | Classe Apex REST | Obrigatório | `networks/*.network` [MA-NET] ou `digitalExperiences/*` [MA-DEB] |
| 3 | Perfil guest do site | Profile | autoriza | acesso da classe e dos objetos para o usuário guest | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | recebe o webhook, valida, grava ou enfileira | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Custom Setting protegido | CustomObject (Custom Setting) | lê/referencia | segredo para validar assinatura | Classe Apex REST | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 7 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 8 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 9 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.7

**Sistema externo → GraphQL API**

Consultas de leitura flexíveis.

> ⚠️ A validar: Escopo atual de mutations na GraphQL API do Salesforce.

### g.7.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a GraphQL API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | GraphQL API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.7.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → GraphQL API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a GraphQL API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | GraphQL API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.7.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a GraphQL API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Web Server + Refresh Token e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | GraphQL API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.7.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a GraphQL API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Username-Password (legado, desaconselhado) e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | GraphQL API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.7.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a GraphQL API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | GraphQL API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.7.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → GraphQL API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a GraphQL API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | GraphQL API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.7.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a GraphQL API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Web Server + Refresh Token | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | GraphQL API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### g.7.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a GraphQL API | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Username-Password (legado, desaconselhado) | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | GraphQL API | não é metadata | ator | endpoint padrão da plataforma | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

