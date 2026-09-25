# Prompt — ExternalClientApp

## 1. Contexto do componente

### 1.1 O que é
`ExternalClientApp` (nome funcional: **External Client App**) é um registro de configuração no Salesforce que representa uma aplicação cliente externa autorizada a se integrar com a plataforma por meio de APIs, geralmente utilizando OAuth 2.0 / OpenID Connect. Ele funciona como uma evolução do modelo de Connected App, introduzido para oferecer maior controle de segurança, governança e discoverability de aplicações externas conectadas à org.

Na prática, um External Client App:
- registra uma aplicação externa (web app, mobile app, serviço headless, middleware) que consume APIs Salesforce;
- pode emitir ou receber tokens de acesso vinculados a permissões mínimas (principle of least privilege);
- se integra ao framework de OAuth e, dependendo da configuração, ao controle de acesso baseado em Permission Sets, External Credentials e External Client App Proxy;
- pode ser associado a escopos (`scopes`), políticas de token/IP/sessão e fluxos OAuth específicos;
- é pensado para cenários de integração modernos, com suporte a agentes, External Services e API-first applications.

> **Atenção de nomenclatura**: o termo pode aparecer na documentação como `External Client App`, `External Client Application` ou `ExtlClntApp`. Em metadata/Tooling, os nomes internos incluem `ExternalClientApp` e objetos relacionados como `ExternalClientApplication`, `ExtlClntAppOauthSettings`, `ExtlClntAppCredentials`, `ExtlClntAppProxy` etc. Validar o nome exato na versão de API da org.

### 1.2 Para que serve
- Registrar e catalogar aplicações externas que acessam APIs Salesforce da organização.
- Definir o contexto de autorização e escopos OAuth de forma granular.
- Aplicar políticas de segurança por app: IP relax, timeout de token/sessão, refresh policy, PIN etc.
- Habilitar o uso de External Credentials (`ExternalCredential`) e proxies (`ExtlClntAppProxy`) para integrações seguras.
- Facilitar auditoria e governança: saber quais apps externos existem, quem os aprovou e quem tem permissão para usá-los.
- Suportar integrações modernas com Agentforce, External Services e API proxies.

### 1.3 Cenários típicos de uso
- Aplicação web/mobile/SPA que consome REST/GraphQL/composite APIs da org via OAuth.
- Middleware/ETL (MuleSoft, Boomi, Informatica, Talend) autenticado via OAuth 2.0 client credentials ou JWT.
- Serviços headless e automações server-to-server.
- Agentes e funções de IA (`GenAiFunction`) que chamam endpoints externos e precisam de credencial gerenciada.
- Portais de Experience Cloud ou parceiros que utilizam app externa para acessar dados via API.
- Integrações gerenciadas por ISVs ou AppExchange que declaram External Client App em pacotes.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em edições que suportam OAuth e External Client App (Developer, Enterprise, Unlimited, Performance e similares; disponibilidade pode variar conforme release).
- **Experience Cloud** — autenticação de membros externos via app cliente pode ser registrada como External Client App.
- **Service Cloud / Sales Cloud** — integrações de CTI, middleware, serviços externos.
- **Data Cloud** — conectores e funções de IA podem utilizar External Client App para autorização de ingestão/ativação.
- **Agentforce** — ações e agentes podem depender de External Client App para obter tokens e realizar callouts seguros.
- **Marketing Cloud / Marketing Cloud Engagement** — conectores podem declarar apps externas, embora configurações específicas residam também no Marketing Cloud.

> **Nota de edição/licença**: External Client App é um componente relativamente novo e pode exigir recursos ativados (`My Domain`, API enabled, permissões de admin, licenças específicas). A disponibilidade exata depende da release e da edição. Em orgs antigas ou edições limitadas, pode não estar disponível ou pode aparecer como recurso pilot/beta.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ExternalClientApp`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | External Client App |
| Metadata type exact | `ExternalClientApp` |
| Pasta no projeto SFDX | `externalClientApps/` |
| Arquivo padrão | `<apiName>.externalClientApp-meta.xml` |
| Objeto interno (API padrão) | `ExternalClientApplication` (ou nome similar; validar na org) |
| Objeto interno (Tooling API) | `ExternalClientApplication` / `ExternalClientApp` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy (conforme release e permissões) |
| Acessível por API padrão / SOQL | Parcial — objeto pode não estar totalmente exposto; use Tooling API quando SOQL for insuficiente |
| Acessível por Tooling API | Sim — `SELECT ... FROM ExternalClientApplication` (ou nome equivalente) |
| Acessível por Apex | Limitado — preferir Tooling REST callout ou Metadata API para inspeção |
| Acessível por UI | Sim — **Setup → External Client Apps** ou **Setup → App Manager** (dependendo da release) |

> **Atenção**: secrets, client secrets, tokens e certificados privados **nunca** são expostos por nenhuma API.

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| External Client App OAuth Settings | `ExternalClientAppOauthSettings` / `ExtlClntAppOauthSettings` | Configurações específicas de OAuth: scopes, fluxos habilitados, callback URL, policies. |
| External Client App Credentials | `ExtlClntAppCredentials` / `ExternalClientAppCredential` | Credenciais associadas ao app ( principals, tokens, secrets referenciados). |
| External Credential | `ExternalCredential` (metadata/API) | Framework de credenciais externas; pode ser vinculado ao External Client App para callouts seguros. |
| External Credential Principal Access | `ExternalCredentialPrincipalAccess` (metadata) | Concede acesso de Permission Set/Profile aos principals da External Credential. |
| Connected App | `ConnectedApp` (metadata/API) | Evolução/cenário legado; External Client App pode coexistir ou substituir Connected Apps em alguns fluxos. |
| AuthProvider | `AuthProvider` (metadata/API) | Provedor de identidade/autenticação externo, quando o app usa OAuth via IdP. |
| Named Credential | `NamedCredential` (metadata/API) | Pode consumir External Credential / External Client App para realizar callouts. |
| Permission Set | `PermissionSet` / `PermissionSetGroup` | Define quem pode usar o app e acessar recursos vinculados. |
| SetupEntityAccess | `SetupEntityAccess` (objeto) | Armazena vínculos de Permission Set/Profile com o app ou entidades relacionadas. |
| User / AuthSession / OAuthToken / LoginHistory | `User`, `AuthSession`, `OAuthToken`, `LoginHistory` | Validar estado efetivo de uso, sessão e concessão. |
| Certificate | `Certificate` (metadata/API) | Certificado usado em assinatura JWT, mTLS ou callbacks assinados. |
| SetupAuditTrail | `SetupAuditTrail` (objeto) | Rastreia alterações no app. |

### 2.3 Matriz de acessibilidade

| Fonte | ExternalClientApp metadata | `ExternalClientApplication` (SOQL) | `ExternalClientApplication` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome, label, descrição | Sim | Parcial | Sim | Sim | Sim |
| Client ID / Consumer Key | Sim (gerado na org) | Parcial | Parcial | Sim | Sim (tratar como sensível) |
| Client Secret | Não | Não | Não | UI (mascarado) | Não exportável |
| OAuth scopes | Sim | Parcial | Sim | Sim | Sim |
| Callback URL | Sim | Parcial | Sim | Sim | Sim |
| Fluxos OAuth habilitados | Sim (bloco oauthSettings) | Parcial | Sim | Sim | Sim |
| Políticas IP/refresh/timeout | Parcial | Parcial | Parcial | Sim | Sim |
| External Credential vinculada | Sim (`externalCredential`) | Sim (lookup) | Sim | Sim | Sim |
| Permissões de uso | via `SetupEntityAccess` + `PermissionSet` | via `SetupEntityAccess` | via `SetupEntityAccess` | Sim | Depende de atribuição |
| Secrets/tokens | Não | Não | Não | UI mascarado | Não exportável |
| Histórico de uso | — | — | — | Setup log | `LoginHistory`, `AuthSession`, `OAuthToken` |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ExternalClientApp`)

Arquivo típico: `externalClientApps/<API_Name>.externalClientApp-meta.xml`.

#### Tags raiz e atributos comuns

| Tag / Atributo | Obrigatória? | Significado prático |
|---|---|---|
| `ExternalClientApp` (root) | Sim | Elemento raiz do metadata type. |
| `xmlns` | Sim | Namespace XML do Metadata API (`http://soap.sforce.com/2006/04/metadata`). |
| `fullName` (atributo) / nome do arquivo | Sim | API Name interno. **Não confundir com `<label>`**. |

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<label>` | 1 | Nome amigável exibido na UI. |
| `<description>` | 0..1 | Descrição funcional/técnica do app. |
| `<contactEmail>` | 0..1 | Email de contato do desenvolvedor/administrador. |
| `<contactPhone>` | 0..1 | Telefone de contato. |
| `<iconUrl>` | 0..1 | URL do ícone exibido no App Launcher ou catálogo. |
| `<infoUrl>` | 0..1 | URL para documentação/sobre. |
| `<logoUrl>` | 0..1 | URL do logotipo. |
| `<startUrl>` | 0..1 | URL inicial após autorização/login. |
| `<oauthSettings>` | 0..1 | Bloco de configurações OAuth 2.0 / OpenID Connect. |
| `<oauthPolicy>` | 0..1 | Políticas de token, refresh, IP relax, timeout. |
| `<externalCredential>` | 0..1 | API Name da `ExternalCredential` associada. |
| `<permissionSetName>` | 0..N | Permission Sets pré-requisito/recomendados (diferente de atribuição!). |
| `<profileName>` | 0..N | Profiles pré-requisito/recomendados. |
| `<sessionPolicy>` | 0..1 | Política de sessão específica do app. |
| `<mobileAppConfig>` | 0..1 | Configurações para Mobile SDK / app móvel. |
| `<ipRanges>` | 0..1 | Restrições de IP. |
| `<plugin>` | 0..1 | Plugin Apex associado. |

##### Bloco `<oauthSettings>`

| Tag / Atributo | Ocorrência | Significado prático |
|---|---|---|
| `<callbackUrl>` | 1..N | OAuth redirect URI(s). Múltiplas URLs podem ser declaradas. |
| `<scopes>` | 1..N | Lista de escopos OAuth. |
| `<scope>` | 1..N (dentro de `<scopes>`) | Valor do escopo (ex.: `Api`, `RefreshToken`, `Full`, `Id`, `Profile`, `Email`, etc.). |
| `<isAdminApproved>` | 0..1 | Se `true`, requer aprovação administrativa antes do uso. |
| `<isClientCredentialEnabled>` | 0..1 | Habilita OAuth 2.0 client credentials flow. |
| `<isCodeCredentialEnabled>` | 0..1 | Habilita authorization code flow com PKCE. |
| `<isConsumerSecretOptional>` | 0..1 | Permite app pública sem client secret. |
| `<isDeviceFlowEnabled>` | 0..1 | Habilita OAuth device flow. |
| `<isSecretRequiredForRefreshToken>` | 0..1 | Exige client secret na troca de refresh token. |
| `<idTokenConfig>` | 0..1 | Configurações do token de identidade OpenID Connect. |

##### Bloco `<oauthPolicy>`

| Tag | Significado prático |
|---|---|
| `<ipRelaxation>` | Valores comuns: `BLOCK`, `RELAX`, `REFRESH_TOKEN`. Controla se IP do token deve coincidir. |
| `<refreshTokenPolicy>` | `infinite` ou número de dias. Validade do refresh token. |
| `<timeout>` | Tempo de inatividade até expiração da sessão (minutos). |

#### Observações sobre XML

- O arquivo `.externalClientApp-meta.xml` é **declarativo** e não contém segredos (`consumerSecret`, tokens, chaves privadas).
- `Consumer Key` presente no XML é específico da org em que o retrieve foi feito. Reaplicar em outra org gera novas credenciais.
- Nem toda configuração visível na UI aparece no XML (ex.: aprovações administrativas por profile/permission set ficam em `SetupEntityAccess`).
- Configurações gerenciadas (managed packages) podem ser read-only parcialmente.
- Os nomes exatos das tags podem variar conforme a versão de API; recomenda-se validar com retrieve real da org.

---

### 3.2 Objeto interno via API padrão: `ExternalClientApplication`

`ExternalClientApplication` (ou nome equivalente na org) é o objeto real consultável em SOQL/REST/Bulk API, quando exposto.

#### Campos relevantes para entendimento

| Campo | Significado prático |
|---|---|
| `Id` | ID interno do registro do app. |
| `Name` / `DeveloperName` | API Name (fullName do XML). |
| `MasterLabel` / `Label` | Nome amigável (`<label>`). |
| `Description` | Descrição. |
| `ContactEmail`, `ContactPhone` | Dados de contato. |
| `NamespacePrefix` | Indica se veio de pacote gerenciado. |
| `ExternalCredentialId` | Lookup para `ExternalCredential.Id`. |
| `AuthProviderId` | Lookup para `AuthProvider.Id`. |
| `CertificateId` | Lookup para `Certificate.Id`. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |
| `CreatedById`, `LastModifiedById` | Quem criou/alterou. |
| `ManageableState` | Estado de pacote gerenciado. |

#### Relação entre objeto e metadata

- Muitos campos correspondem 1:1 às tags XML.
- Secrets (`ClientSecret`, tokens) **nunca** são expostos via SOQL.
- OAuth scopes, callback URLs e certificados geralmente são acessíveis via Tooling API `Metadata` ou campos específicos, quando expostos.
- A atribuição de permissões fica em `SetupEntityAccess`.

#### Exemplo de query via API padrão

```sql
SELECT Id, DeveloperName, MasterLabel, Label, Description,
       NamespacePrefix, ExternalCredentialId, AuthProviderId, CertificateId,
       CreatedDate, LastModifiedDate, CreatedById, LastModifiedById
FROM ExternalClientApplication
ORDER BY LastModifiedDate DESC
```

> **Nota**: se o objeto `ExternalClientApplication` não estiver disponível via SOQL padrão, usar Tooling API. O nome exato deve ser confirmado com `describeGlobal` ou documentação da release.

**Cuidados com permissões**: usuários comuns não enxergam esse objeto. Admins/perfis com `View Setup and Configuration` conseguem consultar.

**Paginação**: se houver mais de 200 registros, use `LIMIT`/`OFFSET` ou REST API com `nextRecordsUrl`.

---

### 3.3 Objeto interno via Tooling API: `ExternalClientApplication`

Tooling API expõe `ExternalClientApplication` com suporte aos campos `Metadata` e `FullName`.

| Campo / funcionalidade | Significado prático |
|---|---|
| `Id` | ID do registro. |
| `FullName` | API Name completo (com namespace). |
| `DeveloperName` | API Name sem namespace. |
| `Metadata` | Representação do objeto como estrutura de metadados Tooling; útil para inspeção programática. |
| `NamespacePrefix` | Namespace do pacote. |
| `Label` / `MasterLabel` | Nome amigável. |

#### Exemplo de query via Tooling API

```sql
SELECT Id, FullName, DeveloperName, NamespacePrefix, Label, Metadata
FROM ExternalClientApplication
WHERE DeveloperName = 'MeuAppExterno'
```

**Formato de retorno**: JSON/XML com campo `Metadata` contendo subestrutura aninhada (`oauthSettings`, `oauthPolicy` etc.).

**Tratamento**:
- Em Python: `requests` + `.json()`; `Metadata` vem como dict.
- Em Apex: callout Tooling REST (`/services/data/vXX.X/tooling/query/?q=...`) e `JSON.deserializeUntyped`.
- Para CSV: flatten recursivo do dict `Metadata`.

**Limitações**:
- Tooling API pode ser menos permissiva para retrieve de apps gerenciadas.
- Campo `Metadata` pode ser truncado se o app for muito complexo.
- Secrets nunca aparecem.

---

### 3.4 Configuração observável em outras fontes

#### Setup / UI

- **Setup → External Client Apps**: lista, criação e edição dos apps.
- **Setup → App Manager**: pode listar External Client Apps junto com Connected Apps e Lightning Apps.
- Tela de detalhe: exibe OAuth settings, scopes, callbacks, políticas, permissões aprovadas.
- **Permissões aprovadas**: vínculo de `Profile` e `Permission Set` ao app, persistido em `SetupEntityAccess`.

#### `SetupEntityAccess` (API padrão)

| Campo | Significado |
|---|---|
| `Id` | ID do vínculo. |
| `SetupEntityId` | Aponta para `ExternalClientApplication.Id` (ou entidade relacionada). |
| `ParentId` | Aponta para `PermissionSet.Id`. |
| `SetupEntityType` | Tipo da entidade; validar valor na org. |

Exemplo:

```sql
SELECT Id, ParentId, Parent.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType LIKE '%ExternalClient%'
```

> O valor exato de `SetupEntityType` pode variar; consultar um registro de exemplo na org.

#### `AuthSession` / `OAuthToken` / `LoginHistory`

- `AuthSession`: sessões ativas vinculadas ao app.
- `OAuthToken`: tokens OAuth emitidos (access/refresh) — metadados de token, sem o secret.
- `LoginHistory.Application`: indica o app usado no login.

#### `PermissionSet` / `Profile`

- Permission Sets e Profiles concedem acesso ao app via `SetupEntityAccess`.
- Permissões de API habilitadas no Profile/Permission Set influenciam se o usuário pode consumir o app.

#### `Certificate` / `AuthProvider` / `ExternalCredential`

- Verificar dependências: certificado referenciado deve existir como `Certificate`.
- `AuthProvider` pode ser usado para OAuth via IdP externo.
- `ExternalCredential` armazena credenciais externas vinculadas ao app.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Client ID / Consumer Key | XML, UI, SOQL/Tooling (gerado na org) | — | Tratar como sensível. |
| Client Secret / Consumer Secret | UI (mascarado) | XML, SOQL, Tooling, Apex | Não exportável. |
| Access Token / Refresh Token | UI (mascarado) | XML, SOQL padrão | Apenas `OAuthToken` expõe metadados. |
| Certificado privado | — | Todo lugar | Apenas `CertificateId` é referenciado. |
| Aprovações administrativas por usuário | `SetupEntityAccess` | XML do app | Estado de acesso fica fora do metadata principal. |
| Estado de sessão ativa | `AuthSession` | XML/Metadata | Uso efetivo. |
| Último uso / histórico | `LoginHistory`, `SetupAuditTrail` | XML/Metadata | Rastreabilidade operacional. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `PermissionSet` / `Profile` (via `SetupEntityAccess`)

- Importa para saber **quem tem permissão de usar** o External Client App.
- A app pode estar configurada mas inacessível se nenhum Permission Set/Profile a aprovou.
- Diferenciar modos:
  - **All users may self-authorize**: qualquer usuário com permissões genéricas pode usar.
  - **Admin approved users are pre-authorized**: apenas Permission Sets/Profiles aprovados.

### 4.2 `ExternalCredential` / `ExternalCredentialPrincipalAccess`

- Importante quando o app usa External Credential para callouts seguros.
- `ExternalCredentialPrincipalAccess` define quem pode acessar os principals.
- Secrets ficam mascarados nos objetos de principal/parâmetro.

### 4.3 `AuthProvider`

- Relevante quando o fluxo OAuth usa um IdP externo.
- `AuthProvider` pode conter consumer key/secret do provedor, não do Salesforce.

### 4.4 `NamedCredential`

- Pode consumir External Credential / External Client App para realizar callouts.
- Alterações no app podem quebrar integrações declarativas (Flow, Apex, External Services).

### 4.5 `ConnectedApp`

- Componente legado relacionado. Em alguns cenários, External Client App é a evolução ou alternativa moderna do Connected App.
- Em orgs com ambos, mapear se o mesmo app está declarado duas vezes.

### 4.6 `User`, `AuthSession`, `OAuthToken`, `LoginHistory`

- Usados para validar estado efetivo de uso.
- Permitem responder: "quem usou", "quando", "de qual IP", "quais escopos".

---

## 5. Consultas e formas de extração

### 5.1 Query via API padrão

#### External Client Apps

```sql
SELECT Id, DeveloperName, MasterLabel, Description,
       NamespacePrefix, ExternalCredentialId,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM ExternalClientApplication
ORDER BY LastModifiedDate DESC
```

#### Quem tem acesso ao app

```sql
SELECT Id, ParentId, Parent.Name, Parent.Profile.Name, Parent.Label, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType LIKE '%ExternalClient%'
```

#### Sessões ativas por app

```sql
SELECT Id, Users.Name, LoginType, SourceIp, LoginHistoryId, CreatedDate, LastModifiedDate
FROM AuthSession
WHERE LoginType LIKE '%ExternalClient%'
ORDER BY CreatedDate DESC
LIMIT 200
```

> Filtro exato em `LoginType` pode variar; consultar um registro primeiro.

#### Tokens OAuth emitidos

```sql
SELECT Id, AppName, User.Name, Scope, CreatedDate, LastUsedDate
FROM OAuthToken
WHERE AppName LIKE '%MeuAppExterno%'
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
                    'SELECT Id,FullName,DeveloperName,NamespacePrefix,Label,Metadata FROM ExternalClientApplication WHERE DeveloperName = \'MeuAppExterno\'',
                    'UTF-8'));
req.setMethod('GET');
req.setHeader('Authorization', 'OAuth ' + UserInfo.getSessionId());
Http http = new Http();
HttpResponse res = http.send(req);
System.debug(res.getBody());
// Tratar JSON: (Map<String,Object>) JSON.deserializeUntyped(res.getBody());
```

> Cuidado: `UserInfo.getSessionId()` funciona em contextos síncronos autorizados; em async/batch pode exigir outro token ou Named Credential.

---

## 6. Boas práticas e pontos de atenção

- **Nunca versionar secrets**: client secrets, tokens, chaves privadas devem ficar fora do repositório.
- **Validar nomes internos**: como External Client App é um componente novo, os nomes de metadata type, objeto e tags XML podem variar entre releases; sempre confirmar com retrieve real.
- **Separar configuração de acesso**: a existência do app no metadata não implica que usuários podem usá-lo; cruzar com `SetupEntityAccess`.
- **Preferir External Credential**: para callouts e credenciais externas, utilize o framework de External Credentials em vez de armazenar segredos no app.
- **Auditar sessões e tokens**: use `AuthSession`, `OAuthToken`, `LoginHistory` para detectar uso indevido ou apps órfãs.
- **Mapear dependências**: antes de alterar ou remover um app, verifique consumidores em Apex (`callout:...`), Flow, External Services, Named Credentials e Agentforce.
- **Cuidado com scopes amplos**: `Full`, `RefreshToken`, `Api` concedem grande poder; revisar periodicamente.
- **Admin Approved vs. Self-Authorize**: mudança de política altera drasticamente a superfície de ataque.
- **Pacotes gerenciados**: apps managed podem ter campos read-only; alterações devem ser feitas pelo ISV.
- **Atualizar callback URLs**: URLs inválidas causam falhas de OAuth e podem indicar app abandonado.

---

## 7. Links de referência oficial

- [Salesforce Help — External Client Apps](https://help.salesforce.com/s/articleView?id=sf.external_client_app_overview.htm)
- [Salesforce Developer — ExternalClientApp Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalclientapp.htm)
- [Salesforce Developer — Tooling API ExternalClientApplication](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_externalclientapplication.htm)
- [Salesforce Help — OAuth Tokens and Scopes](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_tokens_scopes.htm)
- [Salesforce Help — External Credentials Overview](https://help.salesforce.com/s/articleView?id=sf.external_credentials_overview.htm)
- [Salesforce Help — Connected Apps](https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm)
- [Salesforce Developer — Session Security](https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/session_security.htm)
