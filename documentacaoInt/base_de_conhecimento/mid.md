# MID — middleware / MuleSoft

> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta.

Convenções, legenda e códigos de variante: [README](README.md). Fontes citadas entre colchetes: [fontes_validacao.md](fontes_validacao.md).

## Índice

- [M.1 — Org → middleware (síncrono ou via Apex assíncrono)](#m1) (24 variantes)
- [M.2 — Middleware assina Platform Event / CDC](#m2) (4 variantes)
- [M.3 — Middleware → org (REST padrão ou Apex REST)](#m3) (8 variantes)
- [M.4 — Middleware → org (Bulk API 2.0)](#m4) (4 variantes)
- [M.5 — Middleware faz polling na org](#m5) (8 variantes)
- [M.6 — Integration Procedure como middleware dentro da org](#m6) (12 variantes)
- [M.7 — API MuleSoft registrada como External Service → Flow ou Apex](#m7) (8 variantes)

## M.1

**Org → middleware (síncrono ou via Apex assíncrono)**

Igual aos desenhos b e D, com o endpoint apontando para o middleware.

### M.1.v1 — Origem LWC · endpoint E1

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v2 — Origem LWC · endpoint E2

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Controller Apex | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v3 — Origem LWC · endpoint E3

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Controller Apex | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v4 — Origem LWC · endpoint E4

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Controller Apex | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v5 — Origem LWC · endpoint E5

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v6 — Origem LWC · endpoint E6

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Controller Apex | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v7 — Origem Screen Flow · endpoint E1

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v8 — Origem Screen Flow · endpoint E2

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe invocável | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v9 — Origem Screen Flow · endpoint E3

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe invocável | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v10 — Origem Screen Flow · endpoint E4

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe invocável | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v11 — Origem Screen Flow · endpoint E5

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v12 — Origem Screen Flow · endpoint E6

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe invocável | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v13 — Origem Trigger + @future · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Método @future | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v14 — Origem Trigger + @future · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Método @future | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v15 — Origem Trigger + @future · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Método @future | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v16 — Origem Trigger + @future · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Método @future | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Método @future | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Método @future | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v17 — Origem Trigger + @future · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Método @future | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Método @future | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Método @future | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v18 — Origem Trigger + @future · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Método @future | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v19 — Origem Trigger + Queueable · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v20 — Origem Trigger + Queueable · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 9 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v21 — Origem Trigger + Queueable · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v22 — Origem Trigger + Queueable · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 10 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v23 — Origem Trigger + Queueable · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

### M.1.v24 — Origem Trigger + Queueable · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |


## M.2

**Middleware assina Platform Event / CDC**

O conector do middleware consome eventos via Pub/Sub API.

### M.2.v1 — PE · Connected App

Fluxo principal: Pub/Sub API → MuleSoft / middleware (Experience/Process/System API) → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 2 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 3 | Pub/Sub API | não é metadata | ator | entrega os eventos | barramento | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | não aparece no projeto (ator) |
| 4 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | conector Salesforce assina o canal e roteia | — | sistemas de destino | Obrigatório | não aparece no projeto (ator) |
| 5 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 6 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Permission Set (leitura do evento/objeto) | PermissionSet | autoriza | Read no evento ou objeto | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### M.2.v2 — PE · External Client App

Fluxo principal: Pub/Sub API → MuleSoft / middleware (Experience/Process/System API) → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 2 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 3 | Pub/Sub API | não é metadata | ator | entrega os eventos | barramento | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | não aparece no projeto (ator) |
| 4 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | conector Salesforce assina o canal e roteia | — | sistemas de destino | Obrigatório | não aparece no projeto (ator) |
| 5 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 6 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 7 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 8 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 9 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 10 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 13 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 14 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 15 | Permission Set (leitura do evento/objeto) | PermissionSet | autoriza | Read no evento ou objeto | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### M.2.v3 — CDC · Connected App

Fluxo principal: Pub/Sub API → MuleSoft / middleware (Experience/Process/System API) → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 2 | Objeto monitorado | CustomObject | lê/referencia | origem | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Pub/Sub API | não é metadata | ator | entrega os eventos | barramento | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | não aparece no projeto (ator) |
| 4 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | conector Salesforce assina o canal e roteia | — | sistemas de destino | Obrigatório | não aparece no projeto (ator) |
| 5 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 6 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Permission Set (leitura do evento/objeto) | PermissionSet | autoriza | Read no evento ou objeto | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### M.2.v4 — CDC · External Client App

Fluxo principal: Pub/Sub API → MuleSoft / middleware (Experience/Process/System API) → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 2 | Objeto monitorado | CustomObject | lê/referencia | origem | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Pub/Sub API | não é metadata | ator | entrega os eventos | barramento | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | não aparece no projeto (ator) |
| 4 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | conector Salesforce assina o canal e roteia | — | sistemas de destino | Obrigatório | não aparece no projeto (ator) |
| 5 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 6 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 7 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 8 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 9 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 10 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 13 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 14 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 15 | Permission Set (leitura do evento/objeto) | PermissionSet | autoriza | Read no evento ou objeto | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## M.3

**Middleware → org (REST padrão ou Apex REST)**

O middleware chama a org.

### M.3.v1 — Connected App · OAuth 2.0 JWT Bearer · PADRAO

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST/Composite API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST/Composite API padrão | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/Composite API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/Composite API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/Composite API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.3.v2 — Connected App · OAuth 2.0 JWT Bearer · APEXREST

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → Apex REST → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Apex REST | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 10 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 11 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.3.v3 — Connected App · OAuth 2.0 Client Credentials · PADRAO

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST/Composite API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST/Composite API padrão | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/Composite API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/Composite API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/Composite API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.3.v4 — Connected App · OAuth 2.0 Client Credentials · APEXREST

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → Apex REST → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.3.v5 — External Client App · OAuth 2.0 JWT Bearer · PADRAO

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST/Composite API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST/Composite API padrão | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/Composite API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/Composite API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/Composite API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.3.v6 — External Client App · OAuth 2.0 JWT Bearer · APEXREST

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → Apex REST → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | Apex REST | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 14 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 15 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 17 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 19 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 20 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.3.v7 — External Client App · OAuth 2.0 Client Credentials · PADRAO

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST/Composite API padrão → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST/Composite API padrão | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/Composite API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/Composite API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/Composite API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.3.v8 — External Client App · OAuth 2.0 Client Credentials · APEXREST

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → Apex REST → Classe Apex REST → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## M.4

**Middleware → org (Bulk API 2.0)**

Batch Data Synchronization.

### M.4.v1 — Connected App · OAuth 2.0 JWT Bearer · BULK

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Bulk API 2.0 | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.4.v2 — Connected App · OAuth 2.0 Client Credentials · BULK

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Bulk API 2.0 | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.4.v3 — External Client App · OAuth 2.0 JWT Bearer · BULK

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | Bulk API 2.0 | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

### M.4.v4 — External Client App · OAuth 2.0 Client Credentials · BULK

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Bulk API 2.0 | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## M.5

**Middleware faz polling na org**

Sem evento; consulta periódica.

### M.5.v1 — Connected App · OAuth 2.0 JWT Bearer · controle por LastModifiedDate

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST API (query)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### M.5.v2 — Connected App · OAuth 2.0 JWT Bearer · controle por campo customizado

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST API (query)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Campo de controle | CustomField | lê/referencia + executa (DML) | flag/status 'enviado'; o middleware atualiza após processar | MuleSoft / middleware (Experience/Process/System API) | triggers do objeto | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |

### M.5.v3 — Connected App · OAuth 2.0 Client Credentials · controle por LastModifiedDate

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST API (query)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### M.5.v4 — Connected App · OAuth 2.0 Client Credentials · controle por campo customizado

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST API (query)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`) e os `scopes` | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Campo de controle | CustomField | lê/referencia + executa (DML) | flag/status 'enviado'; o middleware atualiza após processar | MuleSoft / middleware (Experience/Process/System API) | triggers do objeto | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |

### M.5.v5 — External Client App · OAuth 2.0 JWT Bearer · controle por LastModifiedDate

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST API (query)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### M.5.v6 — External Client App · OAuth 2.0 JWT Bearer · controle por campo customizado

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST API (query)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 14 | Campo de controle | CustomField | lê/referencia + executa (DML) | flag/status 'enviado'; o middleware atualiza após processar | MuleSoft / middleware (Experience/Process/System API) | triggers do objeto | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |

### M.5.v7 — External Client App · OAuth 2.0 Client Credentials · controle por LastModifiedDate

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST API (query)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### M.5.v8 — External Client App · OAuth 2.0 Client Credentials · controle por campo customizado

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST API (query)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 Client Credentials | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Campo de controle | CustomField | lê/referencia + executa (DML) | flag/status 'enviado'; o middleware atualiza após processar | MuleSoft / middleware (Experience/Process/System API) | triggers do objeto | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |


## M.6

**Integration Procedure como middleware dentro da org**

Orquestração e transformação sem middleware externo.

> ⚠️ A validar: Metadata types OmniStudio ausentes da lista de Metadata Types (API 68.0) [MA-TYPES]; API Apex de invocação de Integration Procedure não confirmada.

### M.6.v1 — Chamador OMNISCRIPT · endpoint E1

Fluxo principal: OmniScript → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | OmniScript | OmniScript | executa | chama a IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | OMNISCRIPT | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v2 — Chamador OMNISCRIPT · endpoint E2

Fluxo principal: OmniScript → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | OmniScript | OmniScript | executa | chama a IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | OMNISCRIPT | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v3 — Chamador OMNISCRIPT · endpoint E3

Fluxo principal: OmniScript → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | OmniScript | OmniScript | executa | chama a IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | OMNISCRIPT | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | URL fixa | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v4 — Chamador FLEXCARD · endpoint E1

Fluxo principal: FlexCard → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | FlexCard | OmniUiCard | executa | fonte de dados IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | FLEXCARD | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v5 — Chamador FLEXCARD · endpoint E2

Fluxo principal: FlexCard → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | FlexCard | OmniUiCard | executa | fonte de dados IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | FLEXCARD | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v6 — Chamador FLEXCARD · endpoint E3

Fluxo principal: FlexCard → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | FlexCard | OmniUiCard | executa | fonte de dados IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | FLEXCARD | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | URL fixa | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v7 — Chamador APEX · endpoint E1

Fluxo principal: Classe Apex → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | invoca a IP pela API Apex do OmniStudio | trigger/serviço | Integration Procedure | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEX | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v8 — Chamador APEX · endpoint E2

Fluxo principal: Classe Apex → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | invoca a IP pela API Apex do OmniStudio | trigger/serviço | Integration Procedure | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEX | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v9 — Chamador APEX · endpoint E3

Fluxo principal: Classe Apex → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | invoca a IP pela API Apex do OmniStudio | trigger/serviço | Integration Procedure | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEX | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | URL fixa | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v10 — Chamador APEXREST · endpoint E1

Fluxo principal: Sistema externo → Usuário de integração → Classe Apex REST → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | chama a org | — | Apex REST | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Classe Apex REST | ApexClass | executa | expõe a IP como endpoint | Apex REST | Integration Procedure | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEXREST | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 10 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 11 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 15 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v11 — Chamador APEXREST · endpoint E2

Fluxo principal: Sistema externo → Usuário de integração → Classe Apex REST → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | chama a org | — | Apex REST | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Classe Apex REST | ApexClass | executa | expõe a IP como endpoint | Apex REST | Integration Procedure | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEXREST | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 10 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 11 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 13 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

### M.6.v12 — Chamador APEXREST · endpoint E3

Fluxo principal: Sistema externo → Usuário de integração → Classe Apex REST → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | chama a org | — | Apex REST | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Classe Apex REST | ApexClass | executa | expõe a IP como endpoint | Apex REST | Integration Procedure | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEXREST | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 10 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | URL fixa | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |


## M.7

**API MuleSoft registrada como External Service → Flow ou Apex**

A especificação vem do MuleSoft/Anypoint; Flow e Apex chamam as operações geradas.

> Observação: Confirmado [MA-ESR]: `registrationProviderType` = MuleSoft ou Anypoint (API 63.0+).

### M.7.v1 — Fonte MuleSoft · chamador Flow · endpoint E1

Fluxo principal: Flow → MuleSoft / middleware (Experience/Process/System API)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow | Flow | executa | `actionCalls` com `actionType`=externalService | gatilho do Flow | Registro de External Service | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=MuleSoft; operações da API do MuleSoft | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

### M.7.v2 — Fonte MuleSoft · chamador Flow · endpoint E2

Fluxo principal: Flow → MuleSoft / middleware (Experience/Process/System API)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow | Flow | executa | `actionCalls` com `actionType`=externalService | gatilho do Flow | Registro de External Service | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=MuleSoft; operações da API do MuleSoft | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Registro de External Service | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

### M.7.v3 — Fonte MuleSoft · chamador Apex · endpoint E1

Fluxo principal: Classe Apex → MuleSoft / middleware (Experience/Process/System API)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | chama `ExternalService.<Servico>` | trigger/serviço/UI | Registro de External Service | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=MuleSoft; operações da API do MuleSoft | Classe Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

### M.7.v4 — Fonte MuleSoft · chamador Apex · endpoint E2

Fluxo principal: Classe Apex → MuleSoft / middleware (Experience/Process/System API)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | chama `ExternalService.<Servico>` | trigger/serviço/UI | Registro de External Service | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=MuleSoft; operações da API do MuleSoft | Classe Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Registro de External Service | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

### M.7.v5 — Fonte Anypoint · chamador Flow · endpoint E1

Fluxo principal: Flow → MuleSoft / middleware (Experience/Process/System API)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow | Flow | executa | `actionCalls` com `actionType`=externalService | gatilho do Flow | Registro de External Service | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=Anypoint; operações da API do MuleSoft | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

### M.7.v6 — Fonte Anypoint · chamador Flow · endpoint E2

Fluxo principal: Flow → MuleSoft / middleware (Experience/Process/System API)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow | Flow | executa | `actionCalls` com `actionType`=externalService | gatilho do Flow | Registro de External Service | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=Anypoint; operações da API do MuleSoft | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Registro de External Service | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

### M.7.v7 — Fonte Anypoint · chamador Apex · endpoint E1

Fluxo principal: Classe Apex → MuleSoft / middleware (Experience/Process/System API)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | chama `ExternalService.<Servico>` | trigger/serviço/UI | Registro de External Service | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=Anypoint; operações da API do MuleSoft | Classe Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

### M.7.v8 — Fonte Anypoint · chamador Apex · endpoint E2

Fluxo principal: Classe Apex → MuleSoft / middleware (Experience/Process/System API)

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | chama `ExternalService.<Servico>` | trigger/serviço/UI | Registro de External Service | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=Anypoint; operações da API do MuleSoft | Classe Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Registro de External Service | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

