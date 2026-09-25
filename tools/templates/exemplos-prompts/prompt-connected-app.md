# Prompt — Connected App

## 1. Contexto do componente

### 1.1 O que é
`ConnectedApp` (nome funcional: **Connected App**) é um registro de aplicação integrada externa — ou integração declarada dentro da própria org — que se autentica e/ou autoriza no Salesforce. Ele funciona como um ponto de controle declarativo sobre:

- fluxos OAuth 2.0 / OpenID Connect;
- SAML Identity Provider (IdP) ou Service Provider (SP);
- autenticação em APIs por JWT, token, certificate ou client credentials;
- sessões de usuário provenientes de clientes móveis, aplicações web, middleware ou serviços headless;
- escopos (`scopes`), políticas (`policies`) e restrições de IP / tempo de sessão.

### 1.2 Para que serve
- Viabilizar que aplicações externas acessem dados do Salesforce sem expor credenciais de usuário humano.
- Definir o nível de acesso delegado por OAuth (qual API, qual user context, refresh, offline access).
- Habilitar Single Sign-On (SSO) via SAML ou OpenID Connect.
- Aplicar políticas de segurança granularizadas por app: PIN, IP relax, session timeout, per-device/per-browser restrições, etc.
- Controlar visibilidade e permissões de pacotes ISV/managed pelo AppExchange.

### 1.3 Cenários típicos de uso
- Integração ETL / middleware (MuleSoft, Informatica, Boomi, Talend) usando OAuth.
- Portais e aplicações externas autenticadas (web app, mobile app, SPA).
- Integrações server-to-server com JWT, certificate ou client credentials.
- Conectores declarativos (`ExternalService`, `NamedCredential`, `ExternalCredential`).
- Automações que usam Salesforce Connect ou GraphQL/REST/Composite/Bulk API.
- Aplicativos ISV instalados via pacotes gerenciados.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponibilidade geral em Developer, Enterprise, Unlimited, Professional (com limitações), Performance.
- **Experience Cloud** — autenticação de membros externos via Connected App é comum; `Experience Cloud` expõe configurações separadas de login e self-registration.
- **Service Cloud / Sales Cloud** — integrações de CTI, middleware de casos, previsão, email-to-case avançado.
- **Data Cloud** — conectores usam Connected App para ingestão/ativação (quando exigido).
- **Marketing Cloud** — conector Sales Cloud para Marketing Cloud e Engagement usa Connected App como parte da integração (embora configurações específicas residam no Marketing Cloud).
- **Agentforce** — ações e agentes podem depender de Credenciais Externas (`ExternalCredential`) e Named Credentials baseadas em OAuth/Connected App.

> **Nota de edição/licença**: algumas opções OAuth/Web App/Canvas são dependentes de recursos ativados (`My Domain`, API enabled, permissões de admin). Edições mais antigas podem não suportar todos os escopos.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ConnectedApp`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Connected App |
| Metadata type exact | `ConnectedApp` |
| Pasta no projeto SFDX | `connectedApps/` |
| Arquivo padrão | `<apiName>.connectedApp-meta.xml` |
| Objeto interno (API padrão) | `ConnectedApplication` |
| Objeto interno (Tooling API) | `ConnectedApplication` (Tooling expõe `Metadata` como Composition/Bitmask; objeto ligado é o mesmo com campos de Tooling) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ConnectedApplication` |
| Acessível por Tooling API | Sim — `SELECT ... FROM ConnectedApplication` |
| Acessível por Apex | Parcial — `ConnectedApplication` é consultável; Secrets/Consumer Key não são expostos em Apex |
| Acessível por UI | Sim — **Setup → App Manager → dropdown da app → "View"** ou **Setup → Connected Apps → Manage Connected Apps** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Permission Set atribuição à app | `SetupEntityAccess` (objeto: `SetupEntityAccess`, campo `SetupEntityId` apontando para `ConnectedApplication`) | Define quais Permission Sets têm acesso à Connected App. |
| Permissão de usuário/oauth | `PermissionSet` / `Profile` + campo `PermissionsUseIdentityConnect` ou permissões OAuth-enabled no profile | Devem ser cruzados para saber quem pode usar. |
| Auth. Provider | `AuthProvider` (metadata) / objeto `AuthProvider` | Connected App pode ser usada como consumer/client no fluxo OAuth; Auth. Provider pode apontar para a mesma app ou ser independente. |
| Named Credential | `NamedCredential` (metadata/API: `NamedCredential`) | Conector declarativo pode usar Connected App para obter/renovar token. |
| External Credential | `ExternalCredential` (metadata/API: `ExternalCredential`) | Framework de credenciais externas; muitas vezes referencia a mesma Connected App. |
| Certificate | `Certificate` (metadata) / objeto `Certificate` | Certificado usado em assinatura JWT, SAML ou em callbacks assinados. |
| Custom App / Lightning App | `CustomApplication` | Apps externas muitas vezes aparecem no App Launcher se a integração incluir Canvas ou Lightning. |
| SamlSsoConfig | `SamlSsoConfig` | Quando app faz SSO via SAML. |
| User / AuthSession / OAuthToken / SetupAuditTrail | `User`, `AuthSession`, `OAuthToken`, `SetupAuditTrail` | Validar estado efetivo de uso, sessão e concessão. |

### 2.3 Matriz de acessibilidade

| Fonte | ConnectedApp metadata | `ConnectedApplication` (SOQL) | `ConnectedApplication` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome, label, descrição | Sim | Sim | Sim | Sim | Sim |
| Consumer Key | Sim (irrecuperável após deploy; gerado na org) | Sim (gerado na org) | Sim | Sim | Apenas por quem vê Setup |
| Consumer Secret | Não | Não | Não | Sim (parcialmente mascarado) | Não exportável |
| OAuth scopes | Sim | Sim | Sim | Sim | Sim |
| Callback URL | Sim | Sim | Sim | Sim | Sim |
| Start URL | Sim | Sim | Sim | Sim | Sim |
| Mobile settings / pin / policies | Parcial | Parcial | Parcial | Sim | Parcial |
| IP Relax / refresh policy | Parcial (XML tem campos) | Parcial | Parcial | Sim | Sim |
| IdP / SAML config | Parcial | Parcial | Parcial | Sim | Sim |
| Configurações de Canvas | Sim (XML) | Parcial | Parcial | Sim | Parcial |
| Caminho de instalação (package) | via `NamespacePrefix` | `NamespacePrefix` | Sim | Sim | Sim |
| Permissões de uso | via `SetupEntityAccess` + `PermissionSet` | Sim | Sim | Sim | Depende de atribuição |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ConnectedApp`)

Arquivo típico: `connectedApps/<API_Name>.connectedApp-meta.xml`.

#### Tags raiz e atributos comuns

| Tag / Atributo | Obrigatória? | Significado prático |
|---|---|---|
| `ConnectedApp` (root) | Sim | Elemento raiz do metadata type. |
| `xmlns` | Sim | Namespace XML do Metadata API (`http://soap.sforce.com/2006/04/metadata`). |
| `fullName` (atributo) / ou nome do arquivo | Sim | API Name interno. **Não confundir com `<label>`**. |

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<contactEmail>` | 1 | Email de contato do desenvolvedor/administrador da app. Usado em notificações e no AppExchange. |
| `<contactPhone>` | 0..1 | Telefone de contato. |
| `<description>` | 0..1 | Descrição funcional/negócio. |
| `<iconUrl>` | 0..1 | URL do ícone exibido no App Launcher/login. |
| `<infoUrl>` | 0..1 | URL para documentação/sobre. |
| `<label>` | 1 | Nome amigável exibido na UI. Deve ser único no namespace. |
| `<logoUrl>` | 0..1 | URL do logotipo. |
| `<startUrl>` | 0..1 | URL inicial após autorização/login (quando aplicável). |
| `<mobileAppConfig>` | 0..1 | Bloco de configurações para Mobile SDK / app móvel. |
| `<oauthConfig>` | 0..1 | Configuração de OAuth 2.0 / OpenID Connect. Muitas vezes presente. |
| `<oauthPolicy>` | 0..1 | Políticas de token, refresh, IP relax, timeout. |
| `<permissionSetName>` | 0..N | Permission Set pré-requisito/recomendado para usar a app (diferente de atribuição!). |
| `<profileName>` | 0..N | Profile pré-requisito/recomendado. |
| `<samlConfig>` | 0..1 | Configuração SAML (SSO iniciado no SP ou IdP). |
| `<sessionPolicy>` | 0..1 | Política de sessão específica da app. |
| `<ipRanges>` | 0..1 | Restrição de IP relaxada ou estrita. |
| `<canvasConfig>` | 0..1 | Configuração de Canvas (apresentação de app externa dentro do Salesforce). |
| `<startUrl>` | 0..1 | URL de partida / redirecionamento. |
| `<plugin>` | 0..1 | Plugin Apex associado (nome da classe Apex). |

##### Bloco `<oauthConfig>`

| Tag / Atributo | Ocorrência | Significado prático |
|---|---|---|
| `<callbackUrl>` | 1..N | OAuth redirect URI(s). Múltiplas URLs podem ser declaradas separadas por nova linha ou como blocos separados. |
| `<certificate>` | 0..1 | Nome do certificate (DeveloperName) usado para assinar request JWT / assertion. |
| `<consumerKey>` | 0..1 no XML | Gerado no ambiente alvo após deploy; **não deve ser versionado** (pode aparecer em retrieve, mas é específico da org). |
| `<consumerSecret>` | Não exportado | NUNCA presente no XML/Metadata. |
| `<idTokenConfig>` | 0..1 | Configurações do token de identidade OpenID Connect (claims, algoritmo, etc.). |
| `<isAdminApproved>` | 0..1 | Se `true`, requer aprovação administrativa antes do uso ( restrictive policy ). |
| `<isClientCredentialEnabled>` | 0..1 | Habilita OAuth 2.0 client credentials flow. |
| `<isCodeCredentialEnabled>` | 0..1 | Habilita authorization code flow com PKCE/code challenge. |
| `<isConsumerSecretOptional>` | 0..1 | Permite que app pública (SPA/mobile) use sem client secret. |
| `<isDeviceFlowEnabled>` | 0..1 | Habilita OAuth device flow. |
| `<isIntrospectAllTokens>` | 0..1 | Permite introspectar tokens emitidos para esta app. |
| `<isSecretRequiredForRefreshToken>` | 0..1 | Exige client secret na troca de refresh token. |
| `<scopes>` | 1..N | Lista de escopos OAuth. |
| `<scope>` | 1..N (dentro de `<scopes>`) | Valor do escopo (ex.: `Api`, `RefreshToken`, `Full`, `CustomApplications`, `Id`, `Profile`, `Email`, `Address`, `Phone`, `Web`, `Visualforce`, `Chatter`, `OpenID`, `CustomPermissions`, `Wave`, `Eclair`, `Pardot`, `UserRegistration`, `Lightning`, `Content`, `CDPIngest`, `CDPProfile`, `CDPQuery`, etc.). |
| `<singleLogoutUrl>` | 0..1 | SLO endpoint para SAML/OIDC. |
| `<url>` | 0..N | URLs associadas à app. |

##### Bloco `<oauthPolicy>`

| Tag | Significado prático |
|---|---|
| `<ipRelaxation>` | Valores comuns: `BLOCK`, `RELAX`, `REFRESH_TOKEN`. Controla se IP do token deve coincidir. |
| `<refreshTokenPolicy>` | `infinite` ou número de dias. Validade do refresh token. |
| `<timeout>` | Tempo de inatividade até expiração da sessão (minutos). |

##### Bloco `<samlConfig>`

| Tag | Significado prático |
|---|---|
| `<acsUrl>` | Assertion Consumer Service URL. |
| `<certificate>` | Certificado usado na assinatura/criptografia SAML. |
| `<encryptionType>` | Algoritmo de criptografia. |
| `<entityUrl>` | Entity ID / issuer. |
| `<issuer>` | Emissor do SAML assertion. |
| `<samlVersion>` | `1.1` ou `2.0`. |
| `<singleLogoutUrl>` | URL de Single Logout. |
| `<subjectType>` | `Username`, `FederationId`, etc. |
| `<nameIdFormat>` | Formato do Name ID (ex.: `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`). |

> **Limitação importante**: retrieve/deploy de Connected App com SAML pode omitir ou requerer ajuste manual de certificados e de IdP/SP configurações.

##### Bloco `<canvasConfig>`

| Tag | Significado prático |
|---|---|
| `<accessMethod>` | `Get`, `Post`, `SignedRequest`. |
| `<canvasUrl>` | URL do Canvas app. |
| `<locations>` | Onde renderiza (`Chatter`, `Page`, `Publisher`, `ServiceDesk`, etc.). |
| `<samlInitiationMethod>` | SAML para Canvas (`None`, `IdPInitiated`, `SPInitiated`). |
| `<developerName>` | Identificador interno do Canvas. |
| `<namespacePrefix>` | Namespace do pacote. |
| `<isAutosubscribed>` | Inscrição automática em eventos. |
| `<isHudCanvas>` | Heads-up display. |

##### Bloco `<sessionPolicy>` / `<mobileAppConfig>`

- Definem exigências de PIN, screenshot blocking, offline cache, session timeout, policy enforcement por dispositivo. Nem todos os campos são expostos integralmente no XML; alguns dependem de políticas org-wide e do Mobile SDK.

#### Observações sobre XML

- O arquivo `.connectedApp-meta.xml` é **declarativo**, mas não contém segredos gerados (`consumerSecret`, tokens, certificado privado).
- Consumer Key presente no XML é específico da org em que o retrieve foi feito. Reaplicar em outra org gera um novo par de chaves.
- Nem toda configuração visível em **Manage Connected Apps** aparece no XML (ex.: aprovações administrativas por profile/permission set aparecem via `SetupEntityAccess`, não no XML).
- Configurações de app instalada via managed package podem ser read-only parcialmente.

---

### 3.2 Objeto interno via API padrão: `ConnectedApplication`

`ConnectedApplication` é o objeto real consultável em SOQL/REST/Bulk API.

#### Campos relevantes para entendimento

| Campo | Significado prático |
|---|---|
| `Id` | ID interno do registro da Connected App. |
| `Name` | API Name (DeveloperName). |
| `DeveloperName` | Igual ao `Name` / nome do arquivo. |
| `Label` | Nome amigável (`<label>` do XML). |
| `Description` | Descrição. |
| `ContactEmail`, `ContactPhone` | Dados de contato. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |
| `CreatedById`, `LastModifiedById` | Quem criou/alterou. |
| `NamespacePrefix` | Indica se veio de pacote gerenciado (managed). Vazio é unmanaged/local. |
| `IsDeleted` | Soft-delete do registro. |
| `MobileSessionTimeout` | Timeout de sessão móvel (em minutos), quando configurado. |
| `PinLength`, `RefreshTokenValidityPeriod`, etc. | Políticas de sessão/tokens. Nem todos os campos são acessíveis por todos os perfis; nomes exatos devem ser validados com `describeSObject`. |
| `ManageableState` | Indica se é `unmanaged`, `managed`, `installed`, `released`, etc. |

#### Relação entre objeto e metadata

- Muitos campos de `ConnectedApplication` correspondem 1:1 às tags XML (`Label` ↔ `<label>`, `Description` ↔ `<description>`).
- `ConnectedApplication` **não** expõe `ConsumerSecret` nem permite recuperá-lo via SOQL.
- OAuth scopes, callback URLs e certificados são geralmente acessíveis via Tooling API `Metadata` ou por query em campos específicos do objeto (quando expostos).
- A atribuição de permissões (quem pode usar a app) é armazenada em `SetupEntityAccess`, não em `ConnectedApplication`.

#### Exemplo de query via API padrão

```sql
SELECT Id, Name, DeveloperName, Label, Description, ContactEmail,
       NamespacePrefix, CreatedDate, LastModifiedDate, CreatedById, LastModifiedById
FROM ConnectedApplication
ORDER BY LastModifiedDate DESC
```

**O que retorna**: lista de Connected Apps cadastradas na org, sem expor secrets.

**Filtros úteis**:
- `WHERE NamespacePrefix = null` — apps locais/unmanaged.
- `WHERE Name = 'MinhaApp'` — app específica.
- `WHERE LastModifiedDate = LAST_N_DAYS:30` — alteradas recentemente.

**Cuidados com permissões**: usuários comuns não enxergam `ConnectedApplication` (ou veem apenas apps de uso próprio). Admins/perfis com `View Setup and Configuration` conseguem consultar. Em Apex, sem `with sharing` correto, query pode falhar por FLS.

**Paginação**: se houver mais de 200 registros, use `LIMIT`/`OFFSET` ou REST API com nextRecordsUrl. Em Bulk/API padrão, respeite `queryMore`/batch.

---

### 3.3 Objeto interno via Tooling API: `ConnectedApplication`

Tooling API expõe `ConnectedApplication` com suporte ao campo `Metadata` (blob de metadados serializado) e `FullName`.

| Campo / funcionalidade | Significado prático |
|---|---|
| `Id` | ID do registro. |
| `FullName` | API Name completo (com namespace). |
| `Metadata` | Representação do objeto como estrutura de metadados Tooling; útil para inspeção programática, mas exige parse. |
| `DeveloperName`, `NamespacePrefix`, `Label` | Equivalentes à API padrão. |
| Campos de dependência/relacionamento | Tooling API também pode ser usado para Dependency API (dependências da Connected App). |

#### Exemplo de query via Tooling API

```sql
SELECT Id, FullName, DeveloperName, NamespacePrefix, Label, Metadata
FROM ConnectedApplication
WHERE DeveloperName = 'MinhaApp'
```

**Formato de retorno**: JSON/XML com campo `Metadata` contendo subestrutura aninhada (`oauthConfig`, `oauthPolicy`, etc.).

**Tratamento**:
- Em Python: usar `json()` do `requests`; `Metadata` vem como dict.
- Em Apex: fazer callout Tooling REST (`/services/data/vXX.X/tooling/query/?q=...`) e usar `JSON.deserializeUntyped`.
- Para CSV: flatten recursivo do dict `Metadata`.

**Limitações**:
- Tooling API pode ser menos permissiva que Metadata API para retrieve de apps gerenciadas.
- Campo `Metadata` pode ser truncado em representações muito grandes.
- Secrets nunca aparecem.

---

### 3.4 Configuração observável em outras fontes

#### Setup / UI

- **Setup → App Manager**: lista apps (inclui Lightning Apps, Connected Apps, etc.).
  - Ações: Manage, View, Delete, Edit Policies.
- **Setup → Connected Apps → Manage Connected Apps**: detalhes de OAuth, SAML, perfis/permissões aprovadas.
- **Permissões aprovadas (Admin Approved Apps)**: tela que vincula `Profile` e `Permission Set` à app. Esse vínculo persiste em `SetupEntityAccess`.

#### `SetupEntityAccess` (API padrão)

| Campo | Significado |
|---|---|
| `Id` | ID do vínculo. |
| `SetupEntityId` | Aponta para `ConnectedApplication.Id`. |
| `ParentId` | Aponta para `PermissionSet.Id` (ou `ProfileId` como Permission Set subjacente). |
| `SetupEntityType` | Tipo da entidade; para app será `ConnectedApplication`. |

Exemplo:

```sql
SELECT Id, ParentId, Parent.Name, SetupEntityId
FROM SetupEntityAccess
WHERE SetupEntityType = 'ConnectedApplication'
```

#### `AuthSession` / `OAuthToken`

- `AuthSession`: sessões ativas (usuário, app, login time, validade, source IP). Campo `LoginType` e `LoginHistoryId` ajudam a correlacionar.
- `OAuthToken`: tokens OAuth emitidos (access/refresh) — pode expor escopos, client ID, usuário. **Segredos não aparecem.**

#### `LoginHistory` e `SetupAuditTrail`

- `LoginHistory.Application` indica a Connected App usada no login.
- `SetupAuditTrail` registra alterações em Connected App (quem e quando).

#### `PermissionSet` / `Profile`

- Permission Sets e Profiles podem ter permissão de uso à Connected App via `SetupEntityAccess`.
- Campo `PermissionsUseIdentityConnect` (quando aplicável) e permissões de API habilitadas no Profile influenciam se o usuário pode consumir a app.

#### `Certificate` / `SamlSsoConfig` / `AuthProvider` / `NamedCredential` / `ExternalCredential`

- Verificar dependências: nome do certificado referenciado no XML deve existir como `Certificate` na org.
- `AuthProvider` pode usar a mesma `consumerKey` (embora secrets sejam mantidos separadamente).
- `NamedCredential`/`ExternalCredential` podem referenciar a Connected App para obtenção de token.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Consumer Key | XML (retrieve), UI, SOQL, Tooling | — | Chave pública do cliente; ainda assim deve ser tratada com cautela. |
| Consumer Secret | UI (parcialmente mascarado) | XML, SOQL, Tooling, Apex | Não é recuperável por nenhuma API. |
| Access Token / Refresh Token | — | XML, SOQL padrão | Apenas objeto `OAuthToken` expõe metadados de token (não o secret). |
| Certificado privado | — | Todo lugar | Apenas certificado público/certificate name é referenciado. |
| Senhas de certificado PKCS#12 | UI (no upload) | API | Não recuperável. |
| Aprovações administrativas por usuário | `SetupEntityAccess` | XML da ConnectedApp | Apesar de serem consequência da app, ficam no Permission Set/Profile. |
| Estado de sessão ativa | `AuthSession` | XML/Metadata | Mostra uso efetivo, não configuração. |
| Último uso / histórico | `LoginHistory`, `SetupAuditTrail` | XML/Metadata | Rastreabilidade operacional. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `PermissionSet` / `Profile` (via `SetupEntityAccess`)

- Importa para saber **quem tem permissão de usar** a Connected App.
- É possível que a app seja visível mas nenhum usuário tenha acesso; é possível que a app esteja oculta mas Permission Sets a concedam.
- Diferenciar:
  - apps “All users may self-authorize” (qualquer um com perfil/perm genérica pode usar);
  - apps “Admin approved users are pre-authorized” (apenas Permission Sets/Profiles aprovados).

### 4.2 `AuthProvider`

- Importa quando o fluxo OAuth usa um IdP externo.
- `AuthProvider` pode conter `ConsumerKey` e `ConsumerSecret` do provedor, não do Salesforce (secret também não exportável).
- `AuthProvider.DeveloperName` pode aparecer em XML de Named Credential.

### 4.3 `NamedCredential` / `ExternalCredential`

- Importante para integrações declarativas (Apex callouts, Flow, External Services).
- A Connected App pode ser a “OAuth client” que fornece/renova tokens usados pela Named Credential.
- `ExternalCredential.Principal` pode armazenar parâmetros de autenticação; secrets ficam mascarados.

### 4.4 `Certificate`

- Nome do certificado declarado no `<certificate>` do XML deve ser resolvido no objeto `Certificate` da org.
- Certificado possui `ExpirationDate`, `UsedByAuthServiceProvider`, `UsedBySamlServiceProvider`, etc.
- A chave privada do certificado nunca é recuperável.

### 4.5 `SamlSsoConfig`

- Importante quando a Connected App assume papel de Service Provider SAML.
- Deve ser cruzado com `EntityUrl`, `Issuer`, `AcsUrl` da app.

### 4.6 `User`, `AuthSession`, `OAuthToken`, `LoginHistory`

- Usados para validar estado efetivo.
- Permitem responder: “quem usou”, “quando”, “de qual IP”, “quais escopos”.

---

## 5. Consultas e formas de extração

### 5.1 Query via API padrão

#### Connected Apps

```sql
SELECT Id, Name, DeveloperName, Label, Description,
       NamespacePrefix, ContactEmail, ContactPhone,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM ConnectedApplication
ORDER BY LastModifiedDate DESC
```

#### Quem tem acesso à app

```sql
SELECT Id, ParentId, Parent.Name, Parent.Profile.Name, Parent.Label, SetupEntityId
FROM SetupEntityAccess
WHERE SetupEntityType = 'ConnectedApplication'
  AND SetupEntityId IN (SELECT Id FROM ConnectedApplication WHERE DeveloperName = 'MinhaApp')
```

#### Sessões ativas por app

```sql
SELECT Id, Users.Name, LoginType, SourceIp, LoginHistoryId, CreatedDate, LastModifiedDate
FROM AuthSession
WHERE LoginType LIKE '%ConnectedApp%'
ORDER BY CreatedDate DESC
LIMIT 200
```

> Filtro exato em `LoginType` pode variar; consultar um registro primeiro para confirmar valor.

#### Tokens OAuth emitidos

```sql
SELECT Id, AppName, User.Name, Scope, CreatedDate, LastUsedDate
FROM OAuthToken
WHERE AppName LIKE '%MinhaApp%'
ORDER BY LastUsedDate DESC
LIMIT 200
```

### 5.2 Tooling API / Apex

Exemplo de chamada Tooling REST dentro de Apex:

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint(URL.getOrgDomainUrl().toExternalForm() +
                '/services/data/v59.0/tooling/query/?q=' +
                EncodingUtil.urlEncode(
                    'SELECT Id,FullName,DeveloperName,NamespacePrefix,Label,Metadata FROM ConnectedApplication WHERE DeveloperName = \'MinhaApp\'',
                    'UTF-8'));
req.setMethod('GET');
req.setHeader('Authorization', 'OAuth ' + UserInfo.getSessionId());
Http http = new Http();
HttpResponse res = http.send(req);
System.debug(res.getBody());
// Tratar JSON: (Map<String,Object>) JSON.deserializeUntyped(res.getBody());
```

**Possíveis saídas**:
- `String` bruto JSON para log/inspeção.
- `Map<String,Object>` parseado para navegação programática.
- CSV convertido flattenando `Metadata`.
- JSON estruturado para integração com ferramenta externa.

> Cuidado: `UserInfo.getSessionId()` funciona em contextos síncronos autorizados; em async/batch pode exigir outro token ou Named Credential.

---

## 6. Boas práticas e pontos de atenção

- **Nunca versionar secrets**: consumer secret, chaves privadas, refresh/access tokens devem estar fora do repositório. Consumer Key, embora não seja secreto, deve ser tratado como dado sensível de ambiente.
- **Não presumir que XML local representa estado atual da org**: Connected Apps geram chaves dinamicamente; compare com `ConnectedApplication` e `SetupEntityAccess`.
- **Separar configuração de acesso**: a existência da app no metadata não implica que usuários a utilizam ou podem utilizá-la.
- **Validar certificados**: certificados referenciados no XML devem existir e estar dentro da validade.
- **Cuidado com scopes amplos**: `Full`, `RefreshToken`, `Api` concedem grande poder; documentar e revisar periodicamente.
- **Admin Approved vs. Self-Authorize**: mudança de política de aprovação altera drasticamente o risco de superfície de ataque.
- **Atualizar callback URLs corretamente**: URLs inválidas causam falhas de OAuth e podem indicar configuração abandonada.
- **Auditar sessões e tokens**: use `AuthSession`, `OAuthToken`, `LoginHistory` para detectar uso indevido ou apps órfãs.
- **Pacotes gerenciados**: apps managed podem ter campos read-only; alterações devem ser feitas pelo ISV.
- **Dependências**: remoção de Connected App pode quebrar `NamedCredential`, `ExternalCredential`, integrações Canvas e Auth. Providers.

---

## 7. Links de referência oficial

- [Salesforce Help — Connected Apps](https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm)
- [Salesforce Developer — ConnectedApp Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_connectedapp.htm)
- [Salesforce Developer — OAuth Tokens and Scopes](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_tokens_scopes.htm)
- [Salesforce Developer — Tooling API Object Reference](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_connectedapplication.htm)
- [Salesforce Help — Manage OAuth Access for Your Connected App](https://help.salesforce.com/s/articleView?id=sf.connected_app_manage_oauth.htm)
- [Salesforce Help — Admin Approval for Connected Apps](https://help.salesforce.com/s/articleView?id=sf.connected_app_admin_approval.htm)
- [Salesforce Help — SAML SSO for Connected Apps](https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm)
- [Salesforce Developer — Session Security](https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/session_security.htm)
