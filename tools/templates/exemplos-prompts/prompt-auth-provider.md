# Prompt — AuthProvider

## 1. Contexto do componente

### 1.1 O que é
`AuthProvider` (nome funcional: **Authentication Provider** ou **Provedor de Autenticação**) é um metadata type declarativo do Salesforce que permite configurar integrações de autenticação federada com provedores de identidade externos. Ele viabiliza login social (Google, Facebook, LinkedIn), SSO corporativo (OpenID Connect, SAML), e integrações OAuth com sistemas externos.

Na prática, um `AuthProvider`:
- configura um endpoint OAuth/OIDC/SAML para autenticação;
- pode ser usado para **SSO em comunidades e domínios Salesforce**;
- pode ser usado para **autenticação de callouts Apex** em conjunto com `NamedCredential`;
- define escopos, URLs de callback, chaves de consumidor, certificados e registro de usuário;
- pode gerar automaticamente uma `RegistrationHandler` class (Apex) para provisionamento de usuários.

### 1.2 Para que serve
- Habilitar Single Sign-On (SSO) com provedores externos.
- Permitir login social em Experience Cloud.
- Autenticar chamadas de integração (outbound) via OAuth 2.0.
- Mapear atributos de usuários externos para usuários Salesforce.
- Facilitar provisioning (JIT) de novos usuários.

### 1.3 Cenários típicos de uso
- Login social em comunidades (Google, Facebook, Apple).
- SSO corporativo com Azure AD, Okta, Ping, ADFS via OpenID Connect ou SAML.
- Autenticação de integrações REST/SOAP usando Named Credentials com OAuth.
- Registro/Login automático de parceiros e clientes no Experience Cloud.

### 1.4 Clouds / contextos
- **Salesforce Core** — Configuração de autenticação.
- **Experience Cloud** — login social e SSO para usuários externos.
- **Platform / Integração** — Named Credentials e callouts autenticados.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `AuthProvider`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Auth. Provider / Provedor de Autenticação |
| Metadata type exact | `AuthProvider` |
| Pasta no projeto SFDX | `authproviders/` |
| Arquivo padrão | `<apiName>.authprovider-meta.xml` |
| Objeto interno (API padrão) | `AuthProvider` |
| Objeto interno (Tooling API) | `AuthProvider` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM AuthProvider` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `AuthProvider` é consultável |
| Acessível por UI | Sim — **Setup → Auth. Providers** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Named Credential | `NamedCredential` | Usa AuthProvider para autenticar callouts. |
| External Credential | `ExternalCredential` | Credencial externa vinculável ao AuthProvider. |
| External Client App | `ExternalClientApp` | Integrações externas que usam OAuth. |
| External Client App Principal Access | `ExternalClientAppPrincipalAccess` | Vínculo entre app externo e principal. |
| Registration Handler | `ApexClass` (interface `Auth.RegistrationHandler`) | Cria/atualiza usuários no login. |
| Certificate / Key Store | `Certificate`, `KeyStore` | Certificado para assinatura/validação. |
| Connected App | `ConnectedApp` | Pode ser usado como OAuth client. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |
| AuthProviderSamlAttribute | `AuthProviderSamlAttribute` | Atributos SAML mapeados. |

### 2.3 Matriz de acessibilidade

| Fonte | AuthProvider metadata | `AuthProvider` (SOQL) | Tooling | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | Sim | Sim | Sim | Sim |
| Tipo (Google, Facebook, OIDC, SAML...) | Sim (`<providerType>`) | `ProviderType` | Sim | Sim | Sim |
| Consumer key / issuer | `<consumerKey>` / `<consumerSecret>` (secret omitido) | `ConsumerKey` | Sim | Sim via UI cuidadoso | Sim |
| URLs autorização/token | Sim | `AuthorizeUrl`, `TokenUrl` | Sim | Sim | Sim |
| Default scopes | Sim (`<defaultScopes>`) | `DefaultScopes` | Sim | Sim | Sim |
| Registration handler | Sim (`<registrationHandler>`) | `RegistrationHandlerId` | Sim | Sim | Sim |
| Named Credentials vinculados | via `NamedCredential` | `AuthProviderId` | — | Setup | Sim |
| Histórico | — | — | — | `SetupAuditTrail` | `SetupAuditTrail` |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`AuthProvider`)

Arquivo típico: `authproviders/<API_Name>.authprovider-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<authorizeUrl>` | 0..1 | URL de autorização OAuth/OIDC. |
| `<consumerKey>` | 0..1 | Client ID / Consumer Key. |
| `<consumerSecret>` | 0..1 | Client Secret (geralmente mascarado/omitido no metadata). |
| `<customMetadataTypeRecord>` | 0..1 | Registro de Custom Metadata usado para configuração customizada. |
| `<defaultScopes>` | 0..1 | Escopos padrão solicitados. |
| `<errorUrl>` | 0..1 | URL de redirecionamento em erro. |
| `<executionUser>` | 0..1 | Usuário de execução para callouts. |
| `<friendlyName>` | 1 | Nome amigável. |
| `<iconUrl>` | 0..1 | URL do ícone exibido no login. |
| `<idTokenIssuer>` | 0..1 | Emissor esperado no ID Token (OIDC). |
| `<includeOrgIdInIdentifier>` | 0..1 | Inclui org ID no identificador do usuário. |
| `<linkKickoffUrl>` | 0..1 | URL para iniciar vinculação de conta. |
| `<logoutUrl>` | 0..1 | URL de logout do IdP. |
| `<oauthKickoffUrl>` | 0..1 | URL para iniciar fluxo OAuth. |
| `<plugin>` | 0..1 | Apex class plugin customizado. |
| `<portal>` | 0..1 | Portal/Experience associado. |
| `<providerType>` | 1 | Tipo: `Google`, `Facebook`, `LinkedIn`, `MicrosoftACS`, `OpenIdConnect`, `Salesforce`, `Saml` etc. |
| `<registrationHandler>` | 0..1 | Apex class que implementa `Auth.RegistrationHandler`. |
| `<sendAccessTokenInHeader>` | 0..1 | Envia access token no header. |
| `<sendClientCredentialsInHeader>` | 0..1 | Envia client credentials no header. |
| `<ssoKickoffUrl>` | 0..1 | URL para iniciar SSO. |
| `<tokenUrl>` | 0..1 | URL do token. |
| `<userInfoUrl>` | 0..1 | URL do userinfo (OIDC). |
| `<suffix>` | 0..1 | Sufixo de URL do provedor. |

> **Atenção**: `consumerSecret` e tokens sensíveis podem estar mascarados no metadata. Nunca exponha em documentação pública.

### 3.2 Objeto interno via API padrão: `AuthProvider`

| Campo | Significado prático |
|---|---|
| `Id` | ID do AuthProvider. |
| `DeveloperName` | API Name. |
| `FriendlyName` | Nome amigável. |
| `ProviderType` | Tipo do provedor. |
| `AuthorizeUrl`, `TokenUrl`, `UserInfoUrl` | Endpoints OAuth/OIDC. |
| `DefaultScopes` | Escopos padrão. |
| `ConsumerKey` | Client ID. |
| `ConsumerSecret` | Secret (mascarado). |
| `IdTokenIssuer` | Emissor esperado. |
| `RegistrationHandlerId` | Handler Apex. |
| `ExecutionUserId` | Usuário de execução. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, DeveloperName, FriendlyName, ProviderType,
       AuthorizeUrl, TokenUrl, UserInfoUrl, DefaultScopes,
       ConsumerKey, RegistrationHandlerId, ExecutionUserId,
       CreatedDate, LastModifiedDate
FROM AuthProvider
ORDER BY FriendlyName
```

### 3.3 Tabelas internas / componentes relacionados

#### Named Credentials que usam o AuthProvider

```sql
SELECT Id, DeveloperName, MasterLabel, AuthProviderId, AuthProvider.DeveloperName,
       Endpoint, PrincipalType, Protocol
FROM NamedCredential
WHERE AuthProviderId != null
ORDER BY AuthProvider.DeveloperName
```

#### External Credential com AuthProvider

```sql
SELECT Id, DeveloperName, MasterLabel, AuthenticationProtocol,
       AuthProviderId, AuthProvider.DeveloperName
FROM ExternalCredential
WHERE AuthProviderId != null
ORDER BY AuthProvider.DeveloperName
```

#### Apex classes handler/plugin relacionadas

```sql
SELECT Id, Name, ApiVersion, Status
FROM ApexClass
WHERE Name IN ('MeuRegistrationHandler', 'MeuAuthPlugin')
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Auth. Providers.
- Setup → My Domain → Authentication Configuration.
- Setup → Experience Cloud → Login & Registration.
- Setup → Named Credentials.
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Consumer Secret | Setup UI, API (mascarado) | Metadata retrieve (frequentemente vazio) | Proteja como segredo. |
| Tokens de acesso | `OAuthToken` (objeto) | AuthProvider metadata | Dados sensíveis. |
| Chaves privadas/certs | `Certificate`, `KeyStore` | AuthProvider XML direto | Via referências. |
| Provedores Managed | UI/Metadata com namespace | — | Pode não ser editável. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `NamedCredential`

- Usa `AuthProvider` para autenticar chamadas outbound.
- Protocolo pode ser `OAuth 2.0`, `Password Authentication`, `JWT` etc.

### 4.2 `ExternalCredential`

- Credencial externa moderna que pode referenciar `AuthProvider`.
- Usado por External Services e callouts seguros.

### 4.3 `ApexClass` Registration Handler

- Cria/atualiza usuário e contato no primeiro login.
- Implementa métodos `createUser` e `updateUser`.

### 4.4 `ConnectedApp`

- Pode ser OAuth client do Salesforce para integrações inbound.
- Pode coexistir com AuthProvider dependendo do cenário.

### 4.5 `Certificate` / `KeyStore`

- Usados em provedores SAML para assinatura/criptografia.

---

## 5. Consultas e formas de extração

### 5.1 AuthProviders

```sql
SELECT Id, DeveloperName, FriendlyName, ProviderType,
       AuthorizeUrl, TokenUrl, UserInfoUrl, DefaultScopes,
       ConsumerKey, RegistrationHandlerId, ExecutionUserId,
       CreatedDate, LastModifiedDate
FROM AuthProvider
ORDER BY FriendlyName
```

### 5.2 Named Credentials vinculadas

```sql
SELECT Id, DeveloperName, MasterLabel, AuthProviderId, AuthProvider.DeveloperName,
       Endpoint, PrincipalType, Protocol
FROM NamedCredential
WHERE AuthProviderId != null
ORDER BY AuthProvider.DeveloperName
```

### 5.3 External Credentials vinculadas

```sql
SELECT Id, DeveloperName, MasterLabel, AuthenticationProtocol,
       AuthProviderId, AuthProvider.DeveloperName
FROM ExternalCredential
WHERE AuthProviderId != null
ORDER BY AuthProvider.DeveloperName
```

### 5.4 Usuários criados via Social/SSO

```sql
SELECT Id, Name, Username, UserType, FederationIdentifier,
       CreatedDate, LastLoginDate, Profile.Name
FROM User
WHERE UserType IN ('CustomerSuccess', 'PowerPartner', 'PowerCustomerSuccess')
ORDER BY CreatedDate DESC
```

---

## 6. Boas práticas e pontos de atenção

- **Proteja secrets**: nunca versione `consumerSecret` em repositórios públicos;
- Use campos customizados ou serviços de secrets externos quando necessário.
- **Valide URLs de callback** e domínios permitidos no provedor externo.
- **HTTPS em todas as URLs**: nunca use HTTP para endpoints de autenticação.
- **Registration Handler seguro**: valide domínios de email e atributos; evite criação em massa indevida.
- **SAML**: verifique certificados e assinaturas; mantenha clocks sincronizados.
- **Teste SSO/login social** em sandbox antes de ativar em produção.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Audite tokens ativos** periodicamente (`AuthSession`, `OauthToken`).

---

## 7. Links de referência oficial

- [Salesforce Help — Auth. Providers](https://help.salesforce.com/s/articleView?id=sf.sso_provider.htm)
- [Salesforce Developer — AuthProvider Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_authprovider.htm)
- [Salesforce Help — Configure an Authentication Provider for OpenID Connect](https://help.salesforce.com/s/articleView?id=sf.sso_provider_openid_connect.htm)
- [Salesforce Help — Configure SAML SSO](https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm)
- [Salesforce Help — Named Credentials](https://help.salesforce.com/s/articleView?id=sf.nc_overview.htm)
