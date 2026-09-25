# Prompt — ExternalClientAppPrincipalAccess

## 1. Contexto do componente

### 1.1 O que é
`ExternalClientAppPrincipalAccess` é um objeto/configuração de segurança do Salesforce que define quais **principais** (usuários, permission sets, permission set groups etc.) têm permissão para usar uma determinada **External Client Application** (`ExternalClientApp`) junto com uma **External Credential**. Ele é o elo de autorização entre a aplicação externa, a credencial necessária e os usuários/sistemas que podem utilizá-los.

Na prática, `ExternalClientAppPrincipalAccess`:
- vincula um `ExternalClientApp` a um ou mais principais;
- pode referenciar uma `ExternalCredential` para restringir acesso por credencial;
- permite implementar o princípio do menor privilégio em integrações OAuth com clientes externos;
- é complementar às configurações OAuth do app: define **quem pode usar**, não apenas **como se autentica**.

### 1.2 Para que serve
- Controlar quais usuários ou grupos de permissões podem obter acesso via External Client App.
- Associar apps externos a credenciais específicas por função/perfil de integração.
- Governar acesso a integrações API-First de forma granular.
- Evitar que qualquer usuário autenticado disponibilize credenciais externalizadas.

### 1.3 Cenários típicos de uso
- App externo de parceiro só pode ser usado por usuários do Permission Set "Integração Parceiro".
- App externo de backoffice usa uma External Credential de produção apenas para usuários de serviço específicos.
- Diferentes grupos de permissões usam a mesma app com credenciais distintas.

### 1.4 Clouds / contextos
- **Salesforce Core** — OAuth e External Credentials.
- **Experience Cloud** — apps externos para parceiros/clientes.
- **Integração / API-First** — controle de acesso a credenciais externalizadas.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ExternalClientAppPrincipalAccess`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | External Client App Principal Access |
| Metadata type exact | `ExternalClientAppPrincipalAccess` |
| Pasta no projeto SFDX | `externalclientappprincipalaccesses/` |
| Arquivo padrão | `<apiName>.externalclientappprincipalaccess-meta.xml` |
| Objeto interno (API padrão) | `ExternalClientAppPrincipalAccess` |
| Objeto interno (Tooling API) | `ExternalClientAppPrincipalAccess` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ExternalClientAppPrincipalAccess` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `ExternalClientAppPrincipalAccess` é consultável |
| Acessível por UI | Sim — **Setup → External Client Applications → Principal Access** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| External Client App | `ExternalClientApp` | App externo ao qual o acesso se refere. |
| External Credential | `ExternalCredential` | Credencial vinculada ao acesso. |
| Permission Set | `PermissionSet` | Principal do tipo permission set. |
| Permission Set Group | `PermissionSetGroup` | Principal do tipo permission set group. |
| User | `User` | Principal do tipo usuário. |
| Profile | `Profile` | Pode ser refletido em permission set owned. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | ExtClientAppPrincipalAccess metadata | `ExternalClientAppPrincipalAccess` (SOQL) | Tooling | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| External Client App | Sim (`<externalClientApp>`) | `ExternalClientAppId` | Sim | Sim | Sim |
| External Credential | Sim (`<externalCredential>`) | `ExternalCredentialId` | Sim | Sim | Sim |
| Principal | Sim (`<principal>`) | `PrincipalId` | Sim | Sim | Sim |
| Tipo do principal | Sim (`<principalType>`) | `PrincipalType` | Sim | Sim | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ExternalClientAppPrincipalAccess`)

Arquivo típico: `externalclientappprincipalaccesses/<API_Name>.externalclientappprincipalaccess-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<externalClientApp>` | 1 | API Name do External Client App. |
| `<externalCredential>` | 0..1 | API Name da External Credential vinculada. |
| `<principal>` | 1 | Usuário/Permission Set/Permission Set Group permitido. |
| `<principalType>` | 1 | Tipo do principal: `PermissionSet`, `PermissionSetGroup`, `User`, etc. |

> **Atenção**: a configuração é sensível; remova acessos antes de excluir apps/credenciais.

### 3.2 Objeto interno via API padrão: `ExternalClientAppPrincipalAccess`

| Campo | Significado prático |
|---|---|
| `Id` | ID do acesso. |
| `ExternalClientAppId` | App externo. |
| `ExternalClientApp.DeveloperName` / `.MasterLabel` | Identificação do app. |
| `ExternalCredentialId` | Credencial vinculada. |
| `ExternalCredential.DeveloperName` / `.MasterLabel` | Identificação da credencial. |
| `PrincipalId` | ID do principal. |
| `PrincipalType` | Tipo do principal. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, ExternalClientAppId, ExternalClientApp.DeveloperName, ExternalClientApp.MasterLabel,
       ExternalCredentialId, ExternalCredential.DeveloperName, ExternalCredential.MasterLabel,
       PrincipalId, PrincipalType, CreatedDate, LastModifiedDate
FROM ExternalClientAppPrincipalAccess
ORDER BY ExternalClientApp.MasterLabel, PrincipalType
```

### 3.3 Resolução do principal

Dependendo do `PrincipalType`, o `PrincipalId` aponta para objetos diferentes:

| `PrincipalType` | Objeto apontado |
|---|---|
| `User` | `User` |
| `PermissionSet` | `PermissionSet` |
| `PermissionSetGroup` | `PermissionSetGroup` |
| `Profile` | `Profile` (raro, via permission set owned) |

Para identificar o nome do principal, use queries específicas:

```sql
SELECT Id, Name, Username
FROM User
WHERE Id = '005...'
```

```sql
SELECT Id, Name, Label
FROM PermissionSet
WHERE Id = '0PS...'
```

```sql
SELECT Id, DeveloperName, MasterLabel
FROM PermissionSetGroup
WHERE Id = '0PG...'
```

---

### 3.4 Configuração observável em outras fontes

- Setup → External Client Applications → selecionar app → Principal Access.
- Setup → External Credentials → selecionar credencial → apps/principais.
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Nome amigável do principal | Objeto de origem | `ExternalClientAppPrincipalAccess` direto | Requer query cruzada. |
| Acesso efetivo | União com Permission Set Assignments + User | Tabela isolada | Verifique `UserRecordAccess` e OAuth token. |
| Histórico | `SetupAuditTrail` | Metadata isolada | Rastreabilidade. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ExternalClientApp`

- Aplicação externa registrada.
- Um app pode ter vários `ExternalClientAppPrincipalAccess`.

### 4.2 `ExternalCredential`

- Credencial externalizada que o app usa.
- Pode ter múltiplos principais com acesso.

### 4.3 `PermissionSet` / `PermissionSetGroup`

- Principais mais comuns para governança de acesso em escala.

### 4.4 `User`

- Principal individual. Use com moderação; prefira Permission Sets.

---

## 5. Consultas e formas de extração

### 5.1 Todos os acessos principais

```sql
SELECT Id, ExternalClientAppId, ExternalClientApp.DeveloperName, ExternalClientApp.MasterLabel,
       ExternalCredentialId, ExternalCredential.DeveloperName, ExternalCredential.MasterLabel,
       PrincipalId, PrincipalType, CreatedDate, LastModifiedDate
FROM ExternalClientAppPrincipalAccess
ORDER BY ExternalClientApp.MasterLabel, PrincipalType
```

### 5.2 Acessos de um app específico

```sql
SELECT Id, ExternalCredentialId, ExternalCredential.MasterLabel,
       PrincipalId, PrincipalType
FROM ExternalClientAppPrincipalAccess
WHERE ExternalClientApp.DeveloperName = 'Meu_External_App'
```

### 5.3 Acessos vinculados a uma credencial

```sql
SELECT Id, ExternalClientAppId, ExternalClientApp.MasterLabel,
       PrincipalId, PrincipalType
FROM ExternalClientAppPrincipalAccess
WHERE ExternalCredential.DeveloperName = 'Minha_External_Credential'
```

### 5.4 Usuários efetivamente cobertos por Permission Set

```sql
SELECT Id, PermissionSetId, PermissionSet.Name, AssigneeId, Assignee.Name, Assignee.Username
FROM PermissionSetAssignment
WHERE PermissionSetId IN (
    SELECT PrincipalId
    FROM ExternalClientAppPrincipalAccess
    WHERE PrincipalType = 'PermissionSet'
)
```

---

## 6. Boas práticas e pontos de atenção

- **Prefira Permission Sets e Permission Set Groups** como principais em vez de usuários individuais.
- **Documente cada vínculo**: qual app, qual credencial e qual função empresarial.
- **Evite acesso em excesso**: mantenha o princípio do menor privilégio.
- **Revogue prontamente** acessos de apps/credenciais desativados.
- **Não delete ExternalClientApp ou ExternalCredential** sem remover os `PrincipalAccess` dependentes.
- **Valide tokens ativos** (`OAuthToken`) após alterações.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Audite periodicamente** quais usuários estão cobertos pelos principais vinculados.

---

## 7. Links de referência oficial

- [Salesforce Help — External Client Applications](https://help.salesforce.com/s/articleView?id=sf.security_external_client_app_overview.htm)
- [Salesforce Help — External Credentials](https://help.salesforce.com/s/articleView?id=sf.nc_external_credentials.htm)
- [Salesforce Developer — ExternalClientAppPrincipalAccess Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_externalclientappprincipalaccess.htm)
