# Prompt — NamedCredential

## 1. Contexto do componente

### 1.1 O que é
`NamedCredential` (nome funcional: **Named Credential**) é um registro de configuração declarativa que representa um endpoint externo e as credenciais/autenticação necessárias para que a plataforma Salesforce realize chamadas de saída (callouts) para esse endpoint.

Na prática, uma Named Credential:
- abstrai a URL base de um serviço externo, permitindo que Apex, Flow, External Services, GenAI Functions e outros componentes referenciem o endpoint por nome;
- associa uma política de autenticação ao endpoint (password, OAuth, JWT, AWS Signature, certificado, principal de External Credential etc.);
- centraliza o gerenciamento de credenciais, reduzindo o armazenamento de segredos em código personalizado;
- permite definir opções de callout, como allowed merge fields em URL, callout options, cadência de retry (conforme versão de API), timeout e permitted merge fields no corpo/headers;
- pode ser do modelo legado (legacy named credential) ou do modelo baseado em External Credential (external credential-based named credential), introduzido para separar definição de endpoint da definição de autenticação.

### 1.2 Para que serve
- Permitir que Apex (`HttpRequest.setEndpoint('callout:MeuEndpoint/...')`) e Flow (HTTP callout action) façam requisições externas sem expor URLs reais e credenciais no código fonte.
- Gerenciar autenticação junto a API externa: tokens de acesso, refresh tokens, crendenciais de cliente, certificados, usuário/senha, AWS Signature e chaves de API.
- Possibilitar integrações server-to-server (OAuth 2.0 client credentials, JWT, AWS Signature) e integrações baseadas em usuário final (OAuth delegated, per-user).
- Suportar o framework de credenciais externas (`ExternalCredential`, `ExtlClntAppCredentials`), que integra Permission Sets, Princi­pals e políticas de acesso.
- Viabilizar agentes e funções de IA (`GenAiFunction`, `GenAiPlugin`, `AIApplication`) que consumam endpoints externos de forma segura.
- Facilitar governança: auditoria de endpoints, escopo de credenciais, dependências e revisão centralizada de configurações de integração.

### 1.3 Cenários típicos de uso
- Integração REST/SOAP com middleware corporativo (ESB, API Gateway, MuleSoft, AWS API Gateway, Azure APIM).
- Chamadas Apex para serviços externos de cálculo, validação, cobrança, risco, logística, IA/LLM.
- Flow declarativo que consome serviço externo via HTTP Callout action.
- External Services (`ExternalServiceRegistration`) que geram automaticamente operadores de Flow/Apex a partir de um OpenAPI/Swagger.
- Agentforce/Data Cloud functions (`GenAiFunction`) que consultam APIs externas através de Named Credential.
- Integrações com AWS (ex.: Amazon S3, Amazon Bedrock) usando AWS Signature Version 4.
- Integrações com provedores de identidade e API protegidas por JWT ou OAuth 2.0.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em Developer, Enterprise, Unlimited, Performance e outras edições que suportam callouts/API enabled.
- **Service Cloud / Sales Cloud** — integrações de CTI, middleware de casos, previsão, serviços de campo, faturamento.
- **Experience Cloud** — callouts para portais externos, autenticação per-user, integração com IDP parceiro.
- **Data Cloud** — Data Connectors, Ingest API, Streaming connectors e funções de IA frequentemente dependem de Named Credential.
- **Agentforce** — `GenAiFunction`, `GenAiPlanner`, `GenAiPlugin` e action calls podem usar Named Credential para chamar LLMs e APIs complementares.
- **Marketing Cloud / Marketing Cloud Engagement** — conectores Sales Cloud→Marketing Cloud podem ter credential associada; configurações específicas geralmente residem no Marketing Cloud.

> **Nota de edição/licença**: algumas opções de autenticação avançadas (per-user authentication, External Credential, Identity Provider Auth. Provider, cadência de retry, merge fields em body/headers) exigem recursos ou permissões específicas e podem não estar disponíveis em todas as edições. A presença de `ExternalCredential` e de `AuthProvider` depende da habilitação do produto e do namespace. Named Credentials só funcionam quando a org possui API enabled e a configuração de callout está liberada para o contexto de execução.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `NamedCredential`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Named Credential |
| Metadata type exact | `NamedCredential` |
| Pasta no projeto SFDX | `namedCredentials/` |
| Arquivo padrão | `<apiName>.namedCredential-meta.xml` |
| Objeto interno (API padrão) | `NamedCredential` |
| Objeto interno (Tooling API) | `NamedCredential` (expõe `Metadata` como blob serializado; `FullName`) |
| Acessível por Metadata API | Sim — retrieve/deploy via `NamedCredential` type |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM NamedCredential` |
| Acessível por Tooling API | Sim — `SELECT ... FROM NamedCredential` |
| Acessível por Apex | Parcial — o objeto `NamedCredential` não é `describe`-queryable diretamente em Apex com Database.query? Em Apex, os registros de `NamedCredential` podem ser consultados via SOQL quando a org permite, mas nem todos os campos sensíveis são expostos. Preferir Tooling REST callout ou Metadata API para análise programática. |
| Acessível por UI | Sim — **Setup → Named Credentials** ou **Setup → Security → Named Credentials** |

> **Atenção**: campos como senhas, tokens e client secrets **nunca** são expostos por API, Tooling ou Apex, apenas referenciados por nome ou indicados por sua existência na UI.

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| External Credential | `ExternalCredential` (metadata / objeto: `ExternalCredential`) | No modelo novo, a Named Credential referencia uma External Credential que detém a lógica de autenticação e os principals. Separação de endpoint e credencial. |
| External Credential Principal Access | `ExternalCredentialPrincipalAccess` (metadata type) / objeto `ExternalCredentialPrincipal` + `SetupEntityAccess` | Controla quais Permission Sets / Profiles têm acesso aos principals da External Credential. |
| Auth. Provider | `AuthProvider` (metadata) / objeto `AuthProvider` | Pode ser referenciado em Named Credentials legadas ou usado para obter/renovar tokens antes de um callout. |
| Connected App | `ConnectedApp` (metadata) / objeto `ConnectedApplication` | Quando a Named Credential usa OAuth 2.0 com Salesforce como cliente, a Connected App representa o client OAuth. |
| Certificate | `Certificate` (metadata) / objeto `Certificate` | Certificado usado para autenticação mútua (mutual TLS), assinatura JWT ou identificação do cliente. |
| Remote Site Setting | `RemoteSiteSetting` (metadata) / objeto `RemoteSiteSetting` | Em versões legadas, callouts diretos sem Named Credential exigem o domínio cadastrado. Named Credentials geralmente substituem essa necessidade, mas domínios de fallback podem ser relevantes. |
| Permission Set | `PermissionSet` (metadata) / objeto `PermissionSet` | Concede acesso a principals de External Credential via `SetupEntityAccess` + `ExternalCredentialPrincipal`. |
| Profile | `Profile` (metadata) / objeto `Profile` | Mesma função de Permission Set para acesso a principals. |
| Apex | `ApexClass`, `ApexTrigger`, `AsyncApexJob` | Consome a Named Credential via `callout:ApiName` em `HttpRequest`. |
| Flow | `Flow` (metadata) / objeto `FlowDefinitionView` / `FlowVersionView` | Pode usar HTTP Callout action baseada em External Service ou diretamente em Named Credential. |
| External Service Registration | `ExternalServiceRegistration` (metadata) | Referencia a Named Credential para gerar ações de Flow/Apex. |
| GenAI Function / Plugin / Planner | `GenAiFunction`, `GenAiPlugin`, `GenAiPlanner` | Agentforce pode invocar serviços externos via Named Credential. |
| SetupAuditTrail | `SetupAuditTrail` (objeto) | Rastreia alterações na configuração da Named Credential. |
| CalloutResultEvent / CalloutLog (conceituais/documentação) | Objetos/eventos de callout podem existir em release-pilot; validar disponibilidade na org. | Versionamento de chamadas para auditoria e debug. |

### 2.3 Matriz de acessibilidade

| Fonte | NamedCredential metadata | `NamedCredential` (SOQL) | `NamedCredential` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Label / descrição / endpoint | Sim | Sim | Sim | Sim | Sim |
| Identity Path / URL base | Sim (`endpoint`) | Sim (`Endpoint`) | Sim | Sim | Sim |
| Tipo de autenticação (`authProtocol`) | Sim | Sim | Sim | Sim | Sim |
| Referência a `ExternalCredential` | Sim (`externalCredential`) | Sim (`ExternalCredentialId`) | Sim | Sim | Sim |
| Referência a `AuthProvider` | Sim (`authProvider`) | Sim (`AuthProviderId`) | Sim | Sim | Sim |
| Referência a `Certificate` | Sim (`certificate`) | Sim (`CertificateId`) | Sim | Sim | Sim |
| Username / senha | Sim (`username`) — senha via XML: tag `<password>` mascarada ou dependente de API | Parcial (`Username`) — senha nunca | Parcial | UI (mascarada) | Nunca exportável |
| Client ID / Client Secret | Apenas referência nome ou presença; secret não aparece | Referência/indicação; secret não aparece | Referência/indicação | UI (mascarado) | Nunca exportável |
| Token de acesso / refresh token | Não | Não | Não | UI (mascarado) | Não exportável |
| OAuth scopes | Sim ou via ExternalCredential | Parcial | Parcial | Sim | Sim |
| Callout options (timeout, merge fields, retry) | Sim (`calloutOptions` bloco) | Parcial (`CalloutOptions` como objeto composto) | Parcial | Sim | Sim |
| Permitted merge fields / headers / body | Sim | Parcial | Parcial | Sim | Sim |
| Permissões de uso (quem pode executar callouts) | via `ExternalCredentialPrincipal` + `SetupEntityAccess` | via `SetupEntityAccess` | via `SetupEntityAccess` | Sim | Depende de atribuição |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`NamedCredential`)

Arquivo típico: `namedCredentials/<API_Name>.namedCredential-meta.xml`.

#### Tags raiz e atributos comuns

| Tag / Atributo | Obrigatória? | Significado prático |
|---|---|---|
| `NamedCredential` (root) | Sim | Elemento raiz do metadata type. |
| `xmlns` | Sim | Namespace XML do Metadata API (`http://soap.sforce.com/2006/04/metadata`). |
| `fullName` (atributo) / nome do arquivo | Sim | API Name interno. **Não confundir com `<label>`**. Usado em Apex/Flow como `callout:fullName/...`. |

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<allowMergeFieldsInBody>` | 0..1 | Permite usar merge fields no corpo da requisição. Valores: `true` / `false`. |
| `<allowMergeFieldsInHeader>` | 0..1 | Permite usar merge fields nos headers da requisição. |
| `<authProvider>` | 0..1 | API Name do `AuthProvider` usado para OAuth (modelo legado ou delegado). |
| `<authTokenEndpointUrl>` | 0..1 | URL do token endpoint OAuth, quando a Named Credential gerencia o fluxo diretamente. |
| `<certificate>` | 0..1 | Nome (DeveloperName) do certificado para assinatura ou mutual TLS. |
| `<customHeaders>` | 0..1 | Bloco de cabeçalhos customizados. Pode conter `<name>` e `<value>` (ou `<valueFieldFromTokenResponse>` conforme versão). |
| `<description>` | 0..1 | Descrição funcional/técnica. |
| `<endpoint>` | 1 | URL base do endpoint externo. Deve terminar em `/` ou no path base correto. |
| `<externalCredential>` | 0..1 | API Name da `ExternalCredential` associada (modelo novo). |
| `<generateAuthorizationHeader>` | 0..1 | Se `true`, a plataforma gera o header `Authorization` automaticamente com base no protocolo de autenticação. |
| `<jwtAudience>` | 0..1 | Audience (aud) do JWT, quando `authProtocol` = `JwtBearer`. |
| `<jwtFormulaSubject>` | 0..1 | Fórmula Apex utilizada como subject do JWT, geralmente `$User.Username` ou `$User.Email`. |
| `<jwtIssuer>` | 0..1 | Emissor (iss) do JWT. |
| `<jwtSigningCertificate>` | 0..1 | Nome do certificado usado para assinar o JWT. |
| `<jwtTextSubject>` | 0..1 | Subject literal do JWT (alternativa a fórmula). |
| `<jwtValidityPeriodSeconds>` | 0..1 | Tempo de validade do token JWT em segundos. |
| `<label>` | 1 | Nome amigável exibido na UI. |
| `<oauthRefreshToken>` | 0..1 | Token de refresh OAuth em cenários legados/legacy; **não versionar**. |
| `<oauthScope>` | 0..1 | Escopos OAuth solicitados. |
| `<oauthToken>` | 0..1 | Access token OAuth; **não versionar**. |
| `<password>` | 0..1 | Senha para autenticação password (mascarada/criptografada; **não versionar**). |
| `<principalType>` | 0..1 | Tipo de principal: `Anonymous`, `NamedUser`, `PerUser`. Define se há um único usuário de serviço, autenticação anônima ou autenticação por usuário final. |
| `<privateConnection>` | 0..1 | Indica se o callout usa conexão privada Salesforce (Private Connect), quando disponível. |
| `<protocol>` / `<authProtocol>` | 0..1 | Protocolo de autenticação: `NoAuthentication`, `PasswordAuthentication`, `OAuth`, `JwtBearer`, `JwtExchange`, `AwsSv4`, `ApiKey`, etc. Nome exato pode variar com a versão de API. |
| `<queryParamFormat>` | 0..1 | Formato de query params para chamadas. |
| `<username>` | 0..1 | Nome de usuário para autenticação password. |
| `<calloutOptions>` | 0..1 | Bloco de opções avançadas de callout (vide abaixo). |

##### Bloco `<calloutOptions>`

| Tag / Atributo | Ocorrência | Significado prático |
|---|---|---|
| `<allowMergeFieldsInBody>` | 0..1 | Equivalente à tag raiz; pode estar agrupado aqui conforme schema. |
| `<allowMergeFieldsInHeader>` | 0..1 | Equivalente à tag raiz; agrupado no bloco. |
| `<generateAuthorizationHeader>` | 0..1 | Equivalente agrupado. |
| `<requestTimeout>` | 0..1 | Timeout da requisição em milissegundos ou segundos conforme schema. Validar unidade com a versão da API. |
| `<retry>` | 0..1 | Define política de retry (cadência de retentativas), quando suportado. Sub-tags como `<intrusion>` / `<protocolError>` / `<statusCode>` podem existir em APIs mais recentes. |
| `<statusCode>` | 0..N (dentro de `<retry>`) | Códigos HTTP que devem disparar retry. |

##### Autenticação AWS (`AwsSv4`)

| Tag | Significado prático |
|---|---|
| `<awsAccessKey>` | Chave de acesso AWS (pode ser mascarada). |
| `<awsAccessSecret>` | Secret de acesso AWS (**não versionar**). |
| `<awsRegion>` | Região AWS (ex.: `us-east-1`). |
| `<awsService>` | Serviço AWS de destino (ex.: `s3`, `bedrock-runtime`). |

##### Exemplo mínimo (modelo legado, password)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<NamedCredential xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MeuEndpointLegado</fullName>
    <allowMergeFieldsInBody>false</allowMergeFieldsInBody>
    <allowMergeFieldsInHeader>false</allowMergeFieldsInHeader>
    <generateAuthorizationHeader>true</generateAuthorizationHeader>
    <endpoint>https://api.exemplo.com/v1/</endpoint>
    <label>Meu Endpoint Legado</label>
    <principalType>NamedUser</principalType>
    <protocol>PasswordAuthentication</protocol>
    <username>usuario_api</username>
</NamedCredential>
```

##### Exemplo com External Credential

```xml
<?xml version="1.0" encoding="UTF-8"?>
<NamedCredential xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MeuEndpointExterno</fullName>
    <endpoint>https://api.exemplo.com/v2/</endpoint>
    <externalCredential>MinhaExternalCredential</externalCredential>
    <label>Meu Endpoint Externo</label>
</NamedCredential>
```

#### Observações sobre XML

- O arquivo `.namedCredential-meta.xml` é **declarativo** e nunca deve conter segredos plain-text (senhas, tokens, AWS secrets, chaves privadas).
- A tag `<password>` pode aparecer vazia, mascarada ou omitida dependendo da ferramenta de retrieve; em deploy, o valor é sempre reaplicado na org de destino.
- Modelos baseados em `ExternalCredential` tendem a ter XML mais enxuto, pois a lógica de autenticação fica no arquivo `externalCredentials/<apiName>.externalCredential-meta.xml`.
- A ausência de `<calloutOptions>` não implica ausência de opções padrão: o Salesforce aplica defaults de timeout e de geração de `Authorization` header.
- Nem toda opção visível na UI é exposta no XML (ex.: algumas configurações de per-user OAuth, refresh settings e detalhes de principals podem ser controlados via objetos complementares).

---

### 3.2 Objeto interno via API padrão: `NamedCredential`

`NamedCredential` é o objeto real consultável em SOQL/REST/Bulk API.

#### Campos relevantes para entendimento

| Campo | Significado prático |
|---|---|
| `Id` | ID interno do registro da Named Credential. |
| `DeveloperName` | API Name (fullName do XML). |
| `MasterLabel` / `Label` | Nome amigável (`<label>` do XML). |
| `Endpoint` | URL base do endpoint (`<endpoint>`). |
| `AuthProviderId` | Lookup para `AuthProvider.Id` ( quando `<authProvider>` é usado). |
| `ExternalCredentialId` | Lookup para `ExternalCredential.Id` (modelo novo). |
| `CertificateId` | Lookup para `Certificate.Id`. |
| `PrincipalType` | `Anonymous`, `NamedUser`, `PerUser` (ou enum equivalente). |
| `AuthProtocol` | Protocolo de autenticação (`NoAuthentication`, `PasswordAuthentication`, `OAuth`, `JwtBearer`, `AwsSv4` etc.). |
| `Username` | Usuário para password auth. |
| `Password` | **Nunca exposto** em SOQL. |
| `OAuthRefreshToken` | **Nunca exposto** em SOQL. |
| `OAuthToken` | **Nunca exposto** em SOQL. |
| `CalloutOptions` | Estrutura composta (JSON/object) com opções de merge fields, headers, timeout e retry. |
| `NamespacePrefix` | Indica se veio de pacote gerenciado. Vazio é unmanaged/local. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |
| `CreatedById`, `LastModifiedById` | Quem criou/alterou. |
| `ManageableState` | Estado do pacote gerenciado. |
| `IsDeleted` | Soft-delete do registro. |

#### Relação entre objeto e metadata

- Muitos campos de `NamedCredential` correspondem 1:1 às tags XML (`Endpoint` ↔ `<endpoint>`, `MasterLabel` ↔ `<label>`).
- Campos de credenciais (`Password`, `OAuthToken`, `OAuthRefreshToken`, `AwsAccessSecret`) **nunca** são retornados por SOQL.
- Quando `ExternalCredentialId` está preenchido, a autenticação é delegada: detalhes de principals e parâmetros devem ser consultados em `ExternalCredential`, `ExternalCredentialParameter`, `ExternalCredentialPrincipal` e `SetupEntityAccess`.

#### Exemplo de query via API padrão

```sql
SELECT Id, DeveloperName, MasterLabel, Endpoint,
       AuthProviderId, ExternalCredentialId, CertificateId,
       PrincipalType, AuthProtocol, Username,
       CalloutOptions, NamespacePrefix,
       CreatedDate, LastModifiedDate, CreatedById, LastModifiedById
FROM NamedCredential
ORDER BY LastModifiedDate DESC
```

**O que retorna**: configuração estrutural da Named Credential sem expor segredos. `CalloutOptions` vem como estrutura aninhada/object; parsear conforme formato da API (JSON via REST).

**Filtros úteis**:
- `WHERE AuthProtocol = 'NoAuthentication'` — endpoints sem autenticação (alerta de governança).
- `WHERE ExternalCredentialId = null` — modelos legados.
- `WHERE ExternalCredentialId != null` — modelos baseados em External Credential.
- `WHERE NamespacePrefix = null` — credenciais locais/unmanaged.
- `WHERE DeveloperName = 'MeuEndpoint'` — credential específica.

**Cuidados com permissões**: usuários comuns geralmente não conseguem ler `NamedCredential`. Perfis com `View Setup and Configuration` e permissões administrativas são necessários. Em pacotes gerenciados, campos podem ser read-only.

**Paginação**: se houver mais de 200 registros, use `LIMIT`/`OFFSET` ou REST API com `nextRecordsUrl`. Em Bulk/API padrão, respeite `queryMore`/batch.

---

### 3.3 Objeto interno via Tooling API: `NamedCredential`

Tooling API expõe `NamedCredential` com suporte aos campos `Metadata` (blob de metadados serializado) e `FullName`.

| Campo / funcionalidade | Significado prático |
|---|---|
| `Id` | ID do registro. |
| `FullName` | API Name completo (com namespace). |
| `DeveloperName` | API Name sem namespace. |
| `Metadata` | Representação do objeto como estrutura de metadados Tooling; reflete tags XML com tipagem forte. |
| `NamespacePrefix` | Namespace do pacote. |
| `ManageableState`, `CreatedDate`, `LastModifiedDate` | Rastreabilidade e estado de pacote. |

#### Exemplo de query via Tooling API

```sql
SELECT Id, FullName, DeveloperName, NamespacePrefix, Metadata
FROM NamedCredential
WHERE DeveloperName = 'MeuEndpoint'
```

**Formato de retorno**: JSON/XML com campo `Metadata` contendo subestrutura (`endpoint`, `externalCredential`, `calloutOptions`, `authProtocol` etc.).

**Tratamento**:
- Em Python: `requests` + `.json()`; `Metadata` vem como dict aninhado.
- Em Apex: callout Tooling REST (`/services/data/vXX.X/tooling/query/?q=...`) e usar `JSON.deserializeUntyped`.
- Para CSV: flatten recursivo do dict `Metadata`.

**Limitações**:
- Tooling API pode ser menos permissiva para retrieve de credenciais gerenciadas.
- `Metadata` não inclui valores secretos.
- Campos compostos (`CalloutOptions`) podem exigir parse específico.

---

### 3.4 Configuração observável em outras fontes

#### Setup / UI

- **Setup → Named Credentials**: lista, criação e edição de credenciais.
- **Setup → Security → Named Credentials** (em algumas releases): agrupamento de segurança.
- Tela de detalhe da Named Credential: exibe endpoint, tipo de autenticação, referências a Auth Provider / External Credential / Certificate, opções de callout, credenciais mascaradas.
- **External Credential → Principals**: configuração de credenciais e parâmetros sensíveis; exibe nomes de principais, mas valores mascarados.
- **Permission Set → External Credential Principal Access**: vínculo entre Permission Set/Profile e principal da External Credential.

#### `SetupEntityAccess` (API padrão)

Quando `ExternalCredential` é utilizada, o acesso aos principals é armazenado em `SetupEntityAccess`, com `SetupEntityId` apontando para o registro de principal da `ExternalCredential`.

| Campo | Significado |
|---|---|
| `Id` | ID do vínculo. |
| `SetupEntityId` | Aponta para `ExternalCredentialPrincipal.Id` (ou outra entidade de segurança). |
| `ParentId` | Aponta para `PermissionSet.Id`. |
| `SetupEntityType` | Tipo da entidade (ex.: `ExternalCredentialPrincipal`). |

Exemplo:

```sql
SELECT Id, ParentId, Parent.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType = 'ExternalCredentialPrincipal'
```

> O nome exato do `SetupEntityType` para External Credential pode variar; consultar um registro de exemplo na org antes de filtrar.

#### `ExternalCredential`, `ExternalCredentialParameter`, `ExternalCredentialPrincipal`

- `ExternalCredential`: define o modelo de autenticação (OAuth, ApiKey, Basic, etc.) e referências.
- `ExternalCredentialParameter`: parâmetros adicionais (headers, query params, claims), com valores sensíveis mascarados.
- `ExternalCredentialPrincipal`: representa uma identidade/secret vinculada à External Credential.

Para detalhes completos, consultar prompt específico de `ExternalCredential`.

#### `AuthProvider`

- Quando a Named Credential referencia um Auth Provider, a lógica de autorização e token fica centralizada lá.
- `AuthProvider` possui `ConsumerKey__c`/`ConsumerSecret__c` (campos de setup, secret mascarado).

#### `Certificate`

- `CertificateId` da Named Credential deve ser resolvido em `Certificate.Id` para validar validade, tipo e uso.
- A chave privada do certificado nunca é recuperável.

#### `ApexClass`, `FlowDefinitionView`, `ExternalServiceRegistration`, `GenAiFunction`

- Buscar referências a `callout:ApiName` em Apex (pode exigir pesquisa textual no código fonte).
- Em Flow, usar `FlowDefinitionView`/`FlowVersionView` para encontrar HTTP Callout actions e referências a Named Credential.
- `ExternalServiceRegistration` pode ter lookup/reference para Named Credential.
- `GenAiFunction`/`GenAiPlugin` podem declarar actions que usam a Named Credential.

#### `SetupAuditTrail`

- Registra alterações em Named Credential (quem alterou endpoint, autenticação, opções etc.).

```sql
SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section
FROM SetupAuditTrail
WHERE Display LIKE '%NamedCredential%'
   OR Display LIKE '%ExternalCredential%'
ORDER BY CreatedDate DESC
LIMIT 200
```

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Endpoint / URL base | XML, SOQL, Tooling, UI | — | Informação de configuração declarada. |
| Username | XML, SOQL, UI (parcial) | — | Campo textual; pode aparecer no retrieve. |
| Password | UI (mascarada); tag `<password>` no XML pode vir vazia/mascarada | SOQL, Tooling, Apex plain-text | Nunca exportável em claro. |
| Client ID / Consumer Key | UI; referência nomeada ou parcial | XML pode conter indicador, mas secret não | Tratar como sensível. |
| Client Secret / Consumer Secret | UI (mascarado) | XML, SOQL, Tooling, Apex | Não recuperável. |
| Access Token / Refresh Token | UI (mascarado) | XML, SOQL, Tooling, Apex | Gerenciado pela plataforma. |
| AWS Access Key | UI (mascarada); XML pode ter indicador | SOQL, Tooling plain-text | Secret AWS não recuperável. |
| Certificado privado | — | Todo lugar | Apenas `CertificateId` é referenciado. |
| Permissões de uso por usuário | `ExternalCredentialPrincipalAccess`, `SetupEntityAccess` | XML da NamedCredential | Estado de acesso fica fora do metadata da credential. |
| Estado de conectividade / último callout | logs de debug, eventos de callout, post-mortem | XML/Metadata/UI estática | Indica uso efetivo, não configuração. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ExternalCredential` (modelo novo)

- Importante quando a Named Credential usa `<externalCredential>`.
- Define protocolo, fórmulas, parâmetros, claims e principals.
- A separação permite reutilizar a mesma External Credential em várias Named Credentials ou em outros consumidores.
- Secrets e tokens ficam em `ExternalCredentialPrincipal` / `ExternalCredentialParameter`, não no XML da Named Credential.

### 4.2 `ExternalCredentialPrincipal` + `SetupEntityAccess`

- Define **quem pode usar** a External Credential e, portanto, realizar callouts pela Named Credential.
- A atribuição é feita por Permission Set ou Profile (which under the hood é um Permission Set).
- Sem atribuição, o callout falha com erro de autorização, mesmo que a Named Credential exista e esteja corretamente configurada.

### 4.3 `AuthProvider`

- Relevante quando a Named Credential usa OAuth via Auth Provider.
- `AuthProvider` contém informações do IdP externo (URLs, consumer key/secret do provedor, informações do token).
- Secrets do Auth Provider também não são exportáveis.

### 4.4 `ConnectedApp`

- Relevante quando a autenticação OAuth usa uma Connected App declarada na própria org Salesforce como OAuth client.
- A Connected App define scopes, policies, IP relax e callback; a Named Credential usa esse client para obter token.

### 4.5 `Certificate`

- `CertificateId` na Named Credential deve apontar para um certificado existente e válido.
- Usado em JWT signing, mTLS ou identificação do cliente.
- Deve-se verificar `ExpirationDate`, `UsedByAuthProvider`/`UsedBySamlServiceProvider`/`UsedBy NamedCredential` quando disponível.

### 4.6 `PermissionSet` / `Profile`

- Concedem acesso a principals da External Credential.
- Também precisam ter permissões de callout/API habilitadas para o usuário efetivamente executar a requisição.
- A permissão específica de acesso à External Credential não é a mesma que `Api Enabled` ou `Apex Classes`.

### 4.7 `ApexClass`, `Flow`, `ExternalServiceRegistration`, `GenAiFunction`

- Indicam **onde a Named Credential é consumida**.
- Ajuda a mapear dependências e impacto de alterações no endpoint ou credenciais.
- Em Apex, o padrão é `callout:NomeDaCredential/resource`.

---

## 5. Consultas e formas de extração

### 5.1 Query via API padrão

#### Named Credentials

```sql
SELECT Id, DeveloperName, MasterLabel, Endpoint,
       AuthProviderId, ExternalCredentialId, CertificateId,
       PrincipalType, AuthProtocol, Username,
       CalloutOptions, NamespacePrefix,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM NamedCredential
ORDER BY LastModifiedDate DESC
```

#### Credenciais sem autenticação (alerta)

```sql
SELECT Id, DeveloperName, MasterLabel, Endpoint, AuthProtocol
FROM NamedCredential
WHERE AuthProtocol = 'NoAuthentication'
ORDER BY DeveloperName
```

#### Credenciais baseadas em External Credential

```sql
SELECT Id, DeveloperName, MasterLabel, Endpoint,
       ExternalCredential.DeveloperName, ExternalCredentialId
FROM NamedCredential
WHERE ExternalCredentialId != null
ORDER BY DeveloperName
```

#### Quem tem acesso aos principals de External Credential

```sql
SELECT Id, ParentId, Parent.Name, Parent.Profile.Name, Parent.Label,
       SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType = 'ExternalCredentialPrincipal'
  AND SetupEntityId IN (
      SELECT Id FROM ExternalCredentialPrincipal
      WHERE ExternalCredentialId IN (
          SELECT Id FROM ExternalCredential WHERE DeveloperName = 'MinhaExternalCredential'
      )
  )
```

> Ajustar `SetupEntityType` e o path de subquery conforme schema real da org. Subqueries em `SetupEntityAccess` podem exigir filtros adicionais.

### 5.2 Tooling API / Apex

Exemplo de chamada Tooling REST dentro de Apex:

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint(URL.getOrgDomainUrl().toExternalForm() +
                '/services/data/v59.0/tooling/query/?q=' +
                EncodingUtil.urlEncode(
                    'SELECT Id,FullName,DeveloperName,NamespacePrefix,Metadata FROM NamedCredential WHERE DeveloperName = \'MeuEndpoint\'',
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
- CSV convertido flattenando `Metadata` / `CalloutOptions`.
- JSON estruturado para integração com ferramenta externa.

> Cuidado: `UserInfo.getSessionId()` funciona em contextos síncronos autorizados; em async/batch pode exigir outro token ou Named Credential.

---

## 6. Boas práticas e pontos de atenção

- **Nunca versionar segredos**: senhas, tokens, AWS secrets, client secrets, chaves privadas devem ficar fora do repositório. O XML pode conter placeholders ou tags vazias que são preenchidas no deploy/na UI.
- **Preferir External Credential**: quando disponível, separe endpoint (`NamedCredential`) de autenticação (`ExternalCredential`) para maior reuso e governança.
- **Não presumir que XML local representa estado atual da org**: credenciais, tokens e atribuições de permissão podem ter sido alterados diretamente no Setup. Compare com `NamedCredential` + `ExternalCredentialPrincipal` + `SetupEntityAccess`.
- **Separar configuração de acesso**: a existência da Named Credential não significa que usuários/perfis têm permissão para executar callouts.
- **Validar certificados**: certificados referenciados devem existir e estar dentro da validade; renovação deve ser planejada.
- **Cuidado com endpoints sem autenticação**: `NoAuthentication` pode expor dados sensíveis; revisar periodicamente.
- **Auditar alterações**: usar `SetupAuditTrail` para detectar mudanças em endpoint, autenticação e permissões.
- **Mapear consumidores**: pesquisar `callout:<apiName>` em Apex, HTTP Callout actions em Flows e referências em External Services/GenAI Functions antes de alterar ou remover uma Named Credential.
- **Testar callouts em sandbox**: rede, firewalls, certificados e permissões podem diferir da produção.
- **Documentar a finalidade**: preencher `<description>` e manter um inventário de integrações, owners e dados sensíveis trafegados.
- **Pacotes gerenciados**: Named Credentials gerenciadas podem ter campos read-only; alterações devem ser feitas pelo ISV.
- **Timeouts e retry**: defina valores realistas; retries excessivos podem causar excedente de limites de callout da org.

---

## 7. Links de referência oficial

- [Salesforce Help — Named Credentials](https://help.salesforce.com/s/articleView?id=sf.named_credentials_overview.htm)
- [Salesforce Developer — NamedCredential Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_namedcredential.htm)
- [Salesforce Developer — Tooling API NamedCredential](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_namedcredential.htm)
- [Salesforce Developer — Named Credentials Reference](https://developer.salesforce.com/docs/platform/named-credentials/references/named-credentials-reference)
- [Salesforce Help — Create a Named Credential](https://help.salesforce.com/s/articleView?id=sf.named_credentials_create.htm)
- [Salesforce Help — External Credentials](https://help.salesforce.com/s/articleView?id=sf.external_credentials_overview.htm)
- [Salesforce Help — Grant Access to External Credentials](https://help.salesforce.com/s/articleView?id=sf.external_credentials_grant_access.htm)
- [Salesforce Apex Developer Guide — Setting Up Named Credentials](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_named_credentials.htm)
