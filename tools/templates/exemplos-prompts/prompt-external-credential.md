# Prompt — ExternalCredential

## 1. Contexto do componente

### 1.1 O que é
`ExternalCredential` (nome funcional: **External Credential**) é um componente do framework de credenciais externas do Salesforce que representa um modelo de autenticação reutilizável para acesso a sistemas externos. Diferente da `NamedCredential` legada — que combinava endpoint e autenticação no mesmo artefato — a `ExternalCredential` separa a definição de **quem** pode autenticar (Principals, Permission Sets) da definição de **onde** chamar (Named Credential).

Na prática, uma `ExternalCredential`:
- define o protocolo de autenticação (OAuth 2.0, API Key, Basic Auth, JWT, AWS Signature, Custom etc.);
- centraliza os parâmetros de autenticação e secrets de forma segura;
- é composta por um ou mais `ExternalCredentialPrincipal`, que representam identidades/segredos específicos;
- pode ser associada a uma ou mais `NamedCredential` para realizar callouts;
- pode ser concedida a usuários via Permission Sets/Profiles (`ExternalCredentialPrincipalAccess`);
- é fortimente ligada a integrações declarativas (Flow, External Services, Agentforce) e Apex callouts.

### 1.2 Para que serve
- Centralizar e reutilizar configurações de autenticação para chamadas externas.
- Separar responsabilidades: o time de arquitetura/API define a `ExternalCredential`; o time de integração define a `NamedCredential`.
- Permitir governança granular sobre quem pode usar qual credencial externa (via Permission Sets).
- Proteger segredos: valores sensíveis são armazenados pela plataforma e nunca expostos em metadata/API.
- Suportar múltiplos "principals" (identidades) para a mesma credencial, por exemplo, um principal por ambiente ou por integração.
- Viabilizar integrações seguras para Agentforce (`GenAiFunction`), External Services e Flow.

### 1.3 Cenários típicos de uso
- Integração Apex/Flow com API externa protegida por OAuth 2.0 client credentials ou API Key.
- Callouts para AWS (S3, Bedrock etc.) usando AWS Signature Version 4.
- Autenticação JWT para provedores de IA/LLM.
- Credenciais compartilhadas entre múltiplas Named Credentials no mesmo ambiente.
- Integrações ISV/AppExchange que empacotam External Credential junto com Named Credential.
- Agentforce/GenAI Functions que precisam chamar endpoints externos de forma segura.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em edições com External Credential habilitado (Enterprise, Unlimited, Performance, Developer; sujeito a release).
- **Experience Cloud** — portais podem consumir serviços externos via Named Credential que usa External Credential.
- **Service Cloud / Sales Cloud** — integrações de middleware externo.
- **Data Cloud** — conectores e funções de IA podem usar External Credential para ingestão/ativação.
- **Agentforce** — `GenAiFunction`, `GenAiPlanner` e ações de IA frequentemente dependem de External Credential para chamar LLMs e serviços complementares.

> **Nota de edição/licença**: External Credential é um recurso relativamente novo e pode exigir habilitação específica, release recente e permissões administrativas. Nem todas as edições ou orgs antigas possuem o recurso disponível. A presença dos objetos `ExternalCredential`, `ExternalCredentialParameter` e `ExternalCredentialPrincipal` deve ser validada na org.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ExternalCredential`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | External Credential |
| Metadata type exact | `ExternalCredential` |
| Pasta no projeto SFDX | `externalCredentials/` |
| Arquivo padrão | `<apiName>.externalCredential-meta.xml` |
| Objeto interno (API padrão) | `ExternalCredential` |
| Objeto interno relacionado (API padrão) | `ExternalCredentialParameter`, `ExternalCredentialPrincipal` |
| Objeto interno (Tooling API) | `ExternalCredential` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ExternalCredential`, `ExternalCredentialParameter`, `ExternalCredentialPrincipal` |
| Acessível por Tooling API | Sim — `SELECT ... FROM ExternalCredential` |
| Acessível por Apex | Parcial — objetos podem ser consultáveis via SOQL; secrets nunca aparecem |
| Acessível por UI | Sim — **Setup → External Credentials** |

> **Atenção**: secrets, tokens, senhas, chaves de API e valores sensíveis **nunca** são expostos por nenhuma API. Sempre aparecem mascarados ou são substituídos por indicadores no XML.

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Principal | `ExternalCredentialPrincipal` (objeto) / `<principal>` no XML | Identidade/segredo vinculado à External Credential. Pode haver múltiplos principals. |
| Parameter | `ExternalCredentialParameter` (objeto) / `<parameter>` no XML | Parâmetros adicionais de autenticação (headers, query params, claims). |
| Principal Access | `ExternalCredentialPrincipalAccess` (metadata type) | Concede Permission Set/Profile acesso a um principal. |
| Named Credential | `NamedCredential` (metadata/API) | Consome a External Credential para realizar callouts. |
| Permission Set | `PermissionSet` / `PermissionSetGroup` | Define quem tem acesso ao principal da External Credential. |
| Profile | `Profile` | Mesma função de Permission Set para acesso a principals. |
| AuthProvider | `AuthProvider` (metadata/API) | Pode ser usado em conjunto para fluxos OAuth. |
| Connected App / External Client App | `ConnectedApp`, `ExternalClientApp` | Podem estar envolvidos em fluxos OAuth da credencial. |
| Certificate | `Certificate` (metadata/API) | Usado para assinatura JWT ou mTLS. |
| ApexClass / Flow / ExternalServiceRegistration | `ApexClass`, `Flow`, `ExternalServiceRegistration` | Consumidores indiretos via Named Credential. |
| SetupEntityAccess | `SetupEntityAccess` (objeto) | Armazena vínculos de Permission Set/Profile com principals. |
| SetupAuditTrail | `SetupAuditTrail` (objeto) | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | ExternalCredential metadata | `ExternalCredential` (SOQL) | `ExternalCredential` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| API Name / label | Sim | Sim | Sim | Sim | Sim |
| Protocolo de autenticação | Sim (`authenticationProtocol`) | Sim (`AuthenticationProtocol`) | Sim | Sim | Sim |
| Parâmetros de autenticação | Sim (nomes/estrutura) | Sim (nomes) — valores mascarados | Sim | UI (mascarados) | Nunca exportáveis |
| Principals | Sim (`principal`) | Sim (`ExternalCredentialPrincipal`) | Sim | UI (nomes, secrets mascarados) | Sim (sem segredos) |
| Certificado referenciado | Sim (`certificate`) | Sim (`CertificateId`) | Sim | Sim | Sim |
| Named Credentials vinculadas | via referência inversa (`NamedCredential.ExternalCredentialId`) | via SOQL | via SOQL/Tooling | Sim | Sim |
| Permissões de uso | via `ExternalCredentialPrincipalAccess` + `SetupEntityAccess` | via `SetupEntityAccess` | via `SetupEntityAccess` | Sim | Depende de atribuição |
| Secrets (password, client secret, token, key) | Não | Não | Não | UI mascarado | Nunca exportáveis |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ExternalCredential`)

Arquivo típico: `externalCredentials/<API_Name>.externalCredential-meta.xml`.

#### Tags raiz e atributos comuns

| Tag / Atributo | Obrigatória? | Significado prático |
|---|---|---|
| `ExternalCredential` (root) | Sim | Elemento raiz do metadata type. |
| `xmlns` | Sim | Namespace XML do Metadata API. |
| `fullName` (atributo) / nome do arquivo | Sim | API Name interno. |

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<authenticationProtocol>` | 1 | Protocolo de autenticação. Valores comuns: `NoAuthentication`, `Basic`, `ApiKey`, `OAuth`, `JwtBearer`, `AwsSv4`, `Custom`. Nomes exatos podem variar por release. |
| `<description>` | 0..1 | Descrição funcional/técnica. |
| `<label>` | 1 | Nome amigável exibido na UI. |
| `<certificate>` | 0..1 | Nome (DeveloperName) do certificado usado para assinatura JWT ou mTLS. |
| `<parameters>` | 0..1 | Bloco de parâmetros de autenticação. |
| `<parameter>` | 0..N (dentro de `<parameters>`) | Parâmetro individual (nome, tipo, valor ou referência). |
| `<principal>` | 0..N | Principal de autenticação (identidade/segredo). |

##### Bloco `<parameter>`

| Tag / Atributo | Ocorrência | Significado prático |
|---|---|---|
| `<parameterName>` | 1 | Nome interno do parâmetro (ex.: `AuthorizationHeader`, `ApiKey`, `Scope`, `Audience`). |
| `<parameterType>` | 1 | Tipo do parâmetro (ex.: `AuthHeader`, `QueryParam`, `Body`, `JwtClaim`). |
| `<parameterValue>` | 0..1 | Valor do parâmetro. Pode vir vazio/mascarado no retrieve. **Não versionar valores secretos**. |
| `<parameterValueField>` | 0..1 | Campo de referência para valor dinâmico. |
| `<isSecret>` | 0..1 | Indica se o parâmetro deve ser tratado como segredo. |

##### Bloco `<principal>`

| Tag / Atributo | Ocorrência | Significado prático |
|---|---|---|
| `<principalName>` | 1 | Nome identificador do principal (ex.: `Default`, `Producao`, `Sandbox`). |
| `<parameter>` | 0..N | Parâmetros específicos do principal (os mesmos campos de `<parameter>`). |
| `<sequenceNumber>` | 0..1 | Ordem/prioridade do principal. |

#### Exemplo mínimo (API Key)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ExternalCredential xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MinhaApiKeyCredential</fullName>
    <label>Minha API Key Credential</label>
    <authenticationProtocol>ApiKey</authenticationProtocol>
    <parameters>
        <parameter>
            <parameterName>ApiKey</parameterName>
            <parameterType>AuthHeader</parameterType>
            <parameterValue></parameterValue>
            <isSecret>true</isSecret>
        </parameter>
    </parameters>
</ExternalCredential>
```

#### Observações sobre XML

- O arquivo `.externalCredential-meta.xml` contém a **estrutura** da autenticação, mas não os valores secretos em claro.
- Tags `<parameterValue>` podem aparecer vazias no retrieve; o deploy deve reconfigurar ou a UI deve ser usada para inserir valores.
- Múltiplos `<principal>` permitem múltiplas identidades para a mesma credencial (ex.: diferentes chaves por ambiente).
- Nem toda opção disponível na UI pode estar representada no XML, especialmente configurações de permissão avançadas.
- A validação de `<authenticationProtocol>` depende da release da org; valores devem ser confirmados com retrieve real.

---

### 3.2 Objetos internos via API padrão

#### `ExternalCredential`

| Campo | Significado prático |
|---|---|
| `Id` | ID interno da credencial. |
| `DeveloperName` | API Name (fullName). |
| `MasterLabel` / `Label` | Nome amigável. |
| `AuthenticationProtocol` | Protocolo de autenticação. |
| `CertificateId` | Lookup para `Certificate.Id`. |
| `Description` | Descrição. |
| `NamespacePrefix` | Pacote gerenciado. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### `ExternalCredentialParameter`

| Campo | Significado prático |
|---|---|
| `Id` | ID do parâmetro. |
| `ExternalCredentialId` | Lookup para `ExternalCredential`. |
| `ParameterName` | Nome do parâmetro. |
| `ParameterType` | Tipo (header, query param, claim etc.). |
| `ParameterValue` | Valor — **mascarado ou nulo** para segredos. |
| `IsSecret` | Indica se é segredo. |
| `PrincipalId` | Se o parâmetro pertence a um principal específico. |

#### `ExternalCredentialPrincipal`

| Campo | Significado prático |
|---|---|
| `Id` | ID do principal. |
| `ExternalCredentialId` | Lookup para `ExternalCredential`. |
| `PrincipalName` | Nome identificador do principal. |
| `SequenceNumber` | Ordem do principal. |
| `IsActive` / `State` | Estado do principal (quando disponível). |

#### Relação entre objetos e metadata

- Muitos campos mapeiam 1:1 para tags XML.
- `ExternalCredentialParameter.ParameterValue` nunca deve conter valores sensíveis em claro.
- A atribuição de acesso aos principals fica em `SetupEntityAccess`, cujo `SetupEntityId` aponta para `ExternalCredentialPrincipal.Id`.

#### Exemplo de query via API padrão

##### Credenciais externas

```sql
SELECT Id, DeveloperName, MasterLabel, AuthenticationProtocol,
       CertificateId, Description, NamespacePrefix,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM ExternalCredential
ORDER BY LastModifiedDate DESC
```

##### Parâmetros de uma credencial

```sql
SELECT Id, ExternalCredential.DeveloperName, ParameterName, ParameterType, IsSecret
FROM ExternalCredentialParameter
WHERE ExternalCredential.DeveloperName = 'MinhaApiKeyCredential'
```

##### Principais de uma credencial

```sql
SELECT Id, ExternalCredential.DeveloperName, PrincipalName, SequenceNumber
FROM ExternalCredentialPrincipal
WHERE ExternalCredential.DeveloperName = 'MinhaApiKeyCredential'
ORDER BY SequenceNumber
```

**Cuidados com permissões**: usuários comuns não conseguem ler esses objetos. Admins/perfis com permissões de setup conseguem consultar.

**Paginação**: se houver mais de 200 registros, use `LIMIT`/`OFFSET` ou REST API com `nextRecordsUrl`.

---

### 3.3 Objeto interno via Tooling API: `ExternalCredential`

Tooling API expõe `ExternalCredential` com suporte aos campos `Metadata` e `FullName`.

| Campo / funcionalidade | Significado prático |
|---|---|
| `Id` | ID do registro. |
| `FullName` | API Name completo. |
| `DeveloperName` | API Name. |
| `Metadata` | Representação do objeto como estrutura de metadados Tooling. |
| `NamespacePrefix` | Namespace do pacote. |

#### Exemplo de query via Tooling API

```sql
SELECT Id, FullName, DeveloperName, NamespacePrefix, Metadata
FROM ExternalCredential
WHERE DeveloperName = 'MinhaApiKeyCredential'
```

**Formato de retorno**: JSON/XML com campo `Metadata` contendo `authenticationProtocol`, `parameters`, `principal` etc.

**Tratamento**:
- Em Python: `requests` + `.json()`; `Metadata` vem como dict.
- Em Apex: callout Tooling REST (`/services/data/vXX.X/tooling/query/?q=...`) e `JSON.deserializeUntyped`.
- Para CSV: flatten recursivo do dict `Metadata`.

**Limitações**:
- Tooling API pode ser menos permissiva para credenciais gerenciadas.
- Secrets nunca aparecem.

---

### 3.4 Configuração observável em outras fontes

#### Setup / UI

- **Setup → External Credentials**: lista, criação e edição das credenciais.
- Tela de detalhe: exibe protocolo, parâmetros (mascarados), principals e permissões.
- **Permission Set → External Credential Principal Access**: vínculo entre Permission Set/Profile e principal.

#### `SetupEntityAccess`

| Campo | Significado |
|---|---|
| `Id` | ID do vínculo. |
| `SetupEntityId` | Aponta para `ExternalCredentialPrincipal.Id` (ou entidade equivalente). |
| `ParentId` | Aponta para `PermissionSet.Id`. |
| `SetupEntityType` | Tipo da entidade; validar na org. |

Exemplo:

```sql
SELECT Id, ParentId, Parent.Name, Parent.Profile.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType LIKE '%ExternalCredential%'
```

> O valor exato de `SetupEntityType` pode variar; consultar um registro de exemplo na org.

#### `NamedCredential`

- `ExternalCredentialId` em `NamedCredential` indica a credential consumidora.
- Alterações na `ExternalCredential` podem quebrar callouts de todas as Named Credentials vinculadas.

#### `ExternalClientApp` / `ConnectedApp`

- Podem referenciar ou usar a mesma External Credential em fluxos OAuth.

#### `SetupAuditTrail`

```sql
SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section
FROM SetupAuditTrail
WHERE Display LIKE '%ExternalCredential%'
ORDER BY CreatedDate DESC
LIMIT 200
```

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Protocolo / estrutura | XML, SOQL, Tooling, UI | — | Configuração declarada. |
| Nome de parâmetros | XML, SOQL, Tooling, UI | — | Metadado de estrutura. |
| Valores secretos de parâmetros | UI (mascarado); XML vazio/mascarado | SOQL, Tooling, Apex plain-text | Nunca exportáveis. |
| Nome de principals | XML, SOQL, Tooling, UI | — | Identificador. |
| Segredos do principal | UI (mascarado) | XML, SOQL, Tooling, Apex | Não exportáveis. |
| Permissões de uso | `ExternalCredentialPrincipalAccess` / `SetupEntityAccess` | XML da ExternalCredential | Estado de acesso fica fora. |
| Dependências com Named Credential | via lookup inverso | XML da ExternalCredential | Descoberto por query. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ExternalCredentialPrincipal` / `ExternalCredentialParameter`

- Representam as identidades e configurações concretas de autenticação.
- Secrets e valores sensíveis ficam aqui, mascarados.
- É fundamental listar os principals para entender quantas "credenciais" reais existem sob uma `ExternalCredential`.

### 4.2 `ExternalCredentialPrincipalAccess`

- Define **quem pode usar** cada principal.
- Sem esse acesso, o callout falha mesmo que a `NamedCredential` e a `ExternalCredential` estejam corretamente configuradas.

### 4.3 `NamedCredential`

- Consumidora da `ExternalCredential`.
- Uma External Credential pode ser reutilizada em várias Named Credentials.
- Alterações no protocolo ou parâmetros podem impactar múltiplas integrações.

### 4.4 `PermissionSet` / `Profile` / `PermissionSetGroup`

- Concedem acesso aos principals.
- Também precisam ter permissões de callout/API para o usuário efetivamente executar a requisição.

### 4.5 `AuthProvider`

- Relevante em fluxos OAuth, especialmente quando a credencial depende de um IdP externo.

### 4.6 `ConnectedApp` / `ExternalClientApp`

- Podem ser a "OAuth client application" em fluxos que usam a External Credential.

### 4.7 `Certificate`

- `CertificateId` deve apontar para um certificado válido.
- Usado em JWT, mTLS etc.

### 4.8 `ApexClass`, `Flow`, `ExternalServiceRegistration`, `GenAiFunction`

- Consumidores indiretos via Named Credential.
- Importante mapear antes de alterar ou remover uma External Credential.

---

## 5. Consultas e formas de extração

### 5.1 Query via API padrão

#### External Credentials

```sql
SELECT Id, DeveloperName, MasterLabel, AuthenticationProtocol,
       CertificateId, Description, NamespacePrefix,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM ExternalCredential
ORDER BY LastModifiedDate DESC
```

#### Parâmetros e principals

```sql
SELECT Id, ExternalCredential.DeveloperName, PrincipalName, SequenceNumber
FROM ExternalCredentialPrincipal
ORDER BY ExternalCredential.DeveloperName, SequenceNumber
```

```sql
SELECT Id, ExternalCredential.DeveloperName, ParameterName, ParameterType, IsSecret
FROM ExternalCredentialParameter
ORDER BY ExternalCredential.DeveloperName, ParameterName
```

#### Quem tem acesso aos principals

```sql
SELECT Id, ParentId, Parent.Name, Parent.Profile.Name, Parent.Label,
       SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType LIKE '%ExternalCredential%'
```

#### Named Credentials vinculadas

```sql
SELECT Id, DeveloperName, MasterLabel, Endpoint, ExternalCredential.DeveloperName
FROM NamedCredential
WHERE ExternalCredentialId != null
ORDER BY ExternalCredential.DeveloperName
```

### 5.2 Tooling API / Apex

Exemplo de chamada Tooling REST dentro de Apex:

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint(URL.getOrgDomainUrl().toExternalForm() +
                '/services/data/v59.0/tooling/query/?q=' +
                EncodingUtil.urlEncode(
                    'SELECT Id,FullName,DeveloperName,NamespacePrefix,Metadata FROM ExternalCredential WHERE DeveloperName = \'MinhaApiKeyCredential\'',
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

- **Nunca versionar segredos**: senhas, API keys, client secrets, tokens, chaves privadas devem ficar fora do repositório.
- **Separar endpoint de autenticação**: use `NamedCredential` para o endpoint e `ExternalCredential` para a autenticação.
- **Documentar cada principal**: usar nomes claros (`Producao`, `Sandbox`, `IntegracaoX`) e descrições.
- **Principle of least privilege**: conceder acesso aos principals apenas aos Permission Sets estritamente necessários.
- **Validar certificados**: certificados referenciados devem existir e estar dentro da validade.
- **Auditar alterações**: usar `SetupAuditTrail` para detectar mudanças em credenciais e permissões.
- **Mapear dependências**: antes de alterar/remover uma External Credential, identificar Named Credentials, Flows, Apex e Agentforce que a consomem.
- **Cuidado com múltiplos principals**: a sequência e o estado do principal influenciam qual identidade é usada.
- **Testar em sandbox**: secrets e parâmetros podem precisar ser reconfigurados após deploy entre ambientes.
- **Pacotes gerenciados**: External Credentials gerenciadas podem ter campos read-only; alterações devem ser feitas pelo ISV.
- **Verificar disponibilidade do recurso**: confirmar se `ExternalCredential`, `ExternalCredentialParameter` e `ExternalCredentialPrincipal` existem na release da org.

---

## 7. Links de referência oficial

- [Salesforce Help — External Credentials Overview](https://help.salesforce.com/s/articleView?id=sf.external_credentials_overview.htm)
- [Salesforce Help — Create an External Credential](https://help.salesforce.com/s/articleView?id=sf.external_credentials_create.htm)
- [Salesforce Help — Grant Access to External Credentials](https://help.salesforce.com/s/articleView?id=sf.external_credentials_grant_access.htm)
- [Salesforce Developer — ExternalCredential Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalcredential.htm)
- [Salesforce Developer — Tooling API ExternalCredential](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_externalcredential.htm)
- [Salesforce Developer — NamedCredential Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_namedcredential.htm)
- [Salesforce Help — Named Credentials Overview](https://help.salesforce.com/s/articleView?id=sf.named_credentials_overview.htm)
