# Outras dinâmicas

> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta.

Convenções, legenda e códigos de variante: [README](README.md). Fontes citadas entre colchetes: [fontes_validacao.md](fontes_validacao.md).

## Índice

- [N.1 — Org ↔ org](#n1) (4 variantes)
- [N.2 — Integração de UI](#n2) (6 variantes)
- [N.3 — Identidade (SSO)](#n3) (3 variantes)
- [N.4 — Data Cloud](#n4) (1 variantes)

## N.1

**Org ↔ org**

Integração entre orgs Salesforce.

> ⚠️ A validar: Salesforce to Salesforce (legado) não incluído: verificar se há metadata associada.

### N.1.v1 — Salesforce Connect cross-org

Fluxo principal: Usuário → Org Salesforce remota

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | External Object | CustomObject (__x) | lê/referencia | objetos da org remota | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 3 | External Data Source (cross-org) | ExternalDataSource | lê/referencia | URL e identidade da org remota | External Object | Org remota | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 4 | Permission Set | PermissionSet | autoriza | acesso ao External Object | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 5 | Org Salesforce remota | não é metadata | ator | responde às consultas via API | External Data Source | — | Obrigatório | não aparece no projeto (ator) |

### N.1.v2 — Apex REST org→org · endpoint E1

Fluxo principal: Classe cliente (org A) → Org B

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe cliente (org A) | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Org B | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 5 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Org B | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente (org A) | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |
| 8 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) | C11 `@RestResource(urlMapping=...)` |

### N.1.v3 — Apex REST org→org · endpoint E2

Fluxo principal: Classe cliente (org A) → Org B

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe cliente (org A) | Org B | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 4 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 5 | Org B | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente (org A) | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |
| 7 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) | C11 `@RestResource(urlMapping=...)` |

### N.1.v4 — Apex REST org→org · endpoint E5

Fluxo principal: Classe cliente (org A) → Org B

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe cliente (org A) | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe cliente (org A) | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe cliente (org A) | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Org B | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Org B | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente (org A) | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |
| 9 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) | C11 `@RestResource(urlMapping=...)` |


## N.2

**Integração de UI**

O usuário vê ou usa outro sistema; pouca ou nenhuma troca de dados no servidor.

### N.2.v1 — Botão/link de URL

Fluxo principal: Usuário → Botão ou link → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Botão ou link | WebLink | executa | abre o sistema externo com parâmetros do registro na URL | Usuário | Sistema externo | Obrigatório | `objects (dentro do objeto)/*` — `linkType` (url, page, javascript), `url`, `openType`, `page` [MA-WL] |
| 3 | Layout | Layout | lê/referencia | expõe o botão | plataforma | — | Obrigatório | `layouts/*.layout (nv)` — botões/ações e campos exibidos [MA-LAY] |
| 4 | Sistema externo | não é metadata | ator | abre no navegador | WebLink | — | Obrigatório | não aparece no projeto (ator) |

### N.2.v2 — Web Tab

Fluxo principal: Usuário → Aba web → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Aba web | CustomTab | executa | carrega a URL externa | Usuário | Sistema externo | Obrigatório | `tabs/*.tab` — `url` (Web Tab), `page`, `lwcComponent`, `flexiPage`, `auraComponent` [MA-TAB] |
| 3 | App | CustomApplication | lê/referencia | inclui a aba | plataforma | — | Obrigatório | `applications/*.app` — app que agrupa abas [MA-CAPP] |
| 4 | Sistema externo | não é metadata | ator | exibido em frame | CustomTab | — | Obrigatório | não aparece no projeto (ator) |

### N.2.v3 — Canvas em Visualforce

Fluxo principal: Usuário → Página Visualforce → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Visualforce | ApexPage | executa | `<apex:canvasApp>` | Usuário | Canvas App | Obrigatório | `pages/*.page` — `<apex:canvasApp>`, controller com Continuation [MA-PAGE] |
| 3 | Connected App com Canvas | ConnectedApp | autoriza + lê | URL do Canvas, método de acesso (signed request/OAuth), locais permitidos | host | Sistema externo | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 4 | Sistema externo | não é metadata | ator | app web que recebe o signed request | Canvas | — | Obrigatório | não aparece no projeto (ator) |

### N.2.v4 — Canvas em Lightning Page

Fluxo principal: Usuário → Página Lightning → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | executa | componente padrão Canvas App | Usuário | Canvas App | Obrigatório | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Connected App com Canvas | ConnectedApp | autoriza + lê | URL do Canvas, método de acesso (signed request/OAuth), locais permitidos | host | Sistema externo | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 4 | Sistema externo | não é metadata | ator | app web que recebe o signed request | Canvas | — | Obrigatório | não aparece no projeto (ator) |

### N.2.v5 — Canvas via External Client App

Fluxo principal: Usuário → Página Lightning → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | executa | componente Canvas App | Usuário | Canvas App | Obrigatório | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | External Client App | ExternalClientApplication | autoriza | app registrado | host | — | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 4 | Configuração Canvas do app | ExtlClntAppCanvasSettings | autoriza + lê | URL e acesso do Canvas (API 66.0+) | External Client App | Sistema externo | Obrigatório | `extlClntAppCanvasSettings/*.ecaCanvas` — configuração de Canvas do External Client App [MA-ECAC] |
| 5 | Sistema externo | não é metadata | ator | app web | Canvas | — | Obrigatório | não aparece no projeto (ator) |

### N.2.v6 — iframe em LWC

Fluxo principal: Usuário → Componente LWC → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Componente LWC | LightningComponentBundle | executa | renderiza `<iframe>` | Página | Sistema externo | Obrigatório | `lwc/*` — `targetConfigs` (onde aparece) [MA-LWC] |
| 3 | CSP Trusted Site | CspTrustedSite | autoriza | libera o domínio em `frame-src` | navegador | — | Obrigatório | `cspTrustedSites/*.cspTrustedSite` — `endpointUrl`, `context` (All, LEX, Communities, VisualForce...), `isActive`, `isApplicableToConnectSrc`, `isApplicableToFrameSrc`, `isApplicableToImgSrc` [MA-CSP] |
| 4 | Sistema externo | não é metadata | ator | precisa permitir ser emoldurado (X-Frame-Options/CSP) | LWC | — | Obrigatório | não aparece no projeto (ator) |


## N.3

**Identidade (SSO)**

Integra o login, não os dados.

### N.3.v1 — SAML com IdP externo

Fluxo principal: IdP externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | IdP externo | não é metadata | ator | autentica o usuário | Usuário | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Configuração SAML | SamlSsoConfig | autoriza | emissor, certificado, mapeamento de identidade | IdP | — | Obrigatório | `samlssoconfigs/*.samlssoconfig` — emissor, certificado e mapeamento de identidade [MA-SAML] |
| 3 | Certificate | Certificate | autoriza | valida/assina asserções | SAML | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |

### N.3.v2 — OpenID Connect via Auth Provider

Fluxo principal: Provedor externo → Registration Handler

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Provedor externo | não é metadata | ator | autentica | Usuário | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Auth Provider | AuthProvider | autoriza | configuração OIDC | login | Registration Handler | Obrigatório | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 3 | Registration Handler | ApexClass | executa | cria/atualiza o usuário a partir dos dados do provedor | Auth Provider | User | Obrigatório | AuthProvider.`registrationHandler`; classe implementa `Auth.RegistrationHandler` |

### N.3.v3 — Salesforce como IdP

Fluxo principal: App externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | App externo | não é metadata | ator | pede login | Usuário | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App (SAML/OIDC) | ConnectedApp | autoriza | app de serviço; Salesforce emite asserção/token | App externo | — | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |


## N.4

**Data Cloud**

Ingestão e ativação de dados.

> ⚠️ A validar: Toda a família de metadata do Data Cloud.

### N.4.v1 — A validar

Fluxo principal: Data Cloud

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Data Cloud | não é metadata | ator | metadata types de data streams, data sources e ativações a confirmar | — | — | Obrigatório | não aparece no projeto (ator) |

