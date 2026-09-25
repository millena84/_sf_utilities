# Prompt — Profile

## 1. Contexto do componente

### 1.1 O que é
`Profile` (nome funcional: **Perfil** ou **Profile**) é um componente de controle de acesso no Salesforce que define quais permissões, objetos, campos, tipos de registro, aplicativos, págs, classes Apex e páginas Visualforce um usuário pode acessar. O perfil é a base de segurança obrigatória de todo usuário: cada usuário deve ter exatamente um perfil.

Na prática, um Profile:
- define permissões de base (ex.: API enabled, Manage Users, View Setup);
- concede acesso a objetos (CRUD/Ler, Criar, Editar, Excluir, Ver todos, Modificar todos);
- concede acesso a campos (Read/Edit);
- define tipos de registro disponíveis e padrão;
- define apps, classes Apex, páginas Visualforce e tipos de objeto personalizados visíveis;
- pode ser substituído/complementado por Permission Sets.

### 1.2 Para que serve
- Estabelecer o conjunto mínimo de acesso de um usuário.
- Agrupar usuários por função organizacional com permissões comuns.
- Controlar visibilidade e editabilidade de objetos e campos.
- Definir apps, tipos de registro e layouts padrão.
- Servir como ponto de partida para Permission Sets adicionais.

### 1.3 Cenários típicos de uso
- Perfis de vendas, suporte, marketing, administrador.
- Perfis para usuários externos de Experience Cloud (Customer Community, Partner Community).
- Perfis para integrações e usuários de sistema.
- Perfis de gerenciamento de objeto (ex.: acesso restrito a campos sensíveis).

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em todas as edições.
- **Experience Cloud** — perfis específicos de comunidade.
- **Service Cloud / Sales Cloud** — perfis de atendimento e vendas.
- **Data Cloud / Agentforce** — perfis de usuários de integração e dados.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `Profile`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Profile / Perfil |
| Metadata type exact | `Profile` |
| Pasta no projeto SFDX | `profiles/` |
| Arquivo padrão | `<apiName>.profile-meta.xml` |
| Objeto interno (API padrão) | `Profile` |
| Objeto interno (Tooling API) | `Profile` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM Profile` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `Profile` é consultável |
| Acessível por UI | Sim — **Setup → Profiles** |

> **Atenção**: o objeto `Profile` expõe permissões, mas os detalhes de objeto/campo ficam em objetos relacionados (`ObjectPermissions`, `FieldPermissions`).

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Object Permissions | `ObjectPermissions` (objeto) | Permissões de objeto por Profile/PermissionSet. |
| Field Permissions | `FieldPermissions` (objeto) | Permissões de campo por Profile/PermissionSet. |
| Setup Entity Access | `SetupEntityAccess` (objeto) | Acesso a entidades de setup (ApexClass, Visualforce, ConnectedApp, ExternalCredentialPrincipal, Flow). |
| Permission Set | `PermissionSet` | Complementa o Profile. |
| Permission Set Assignment | `PermissionSetAssignment` | Vincula Permission Set a usuário. |
| Group Member | `GroupMember` | Associação de usuários/perfil a Public Groups e Queues. |
| Queue Sobject | `QueueSobject` | Associação de Queue a objetos. |
| User | `User` | Usuários com o perfil. |
| User Role | `UserRole` | Papel hierárquico do usuário. |
| Record Type | `RecordType` | Tipos de registro visíveis/editáveis por perfil. |
| Layout Assignment | `LayoutAssignment` no XML | Layout padrão por objeto/tipo de registro. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | Profile metadata | `Profile` (SOQL) | `Profile` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | Sim | Sim | Sim | Sim |
| Permissões de usuário | Sim (`<userPermissions>`) | Sim (`PermissionsXxx`) | Sim | Sim | Sim |
| Permissões de objeto | via `ObjectPermissions` | `ObjectPermissions` | via `ObjectPermissions` / Metadata | Sim | Sim |
| Permissões de campo | via `FieldPermissions` | `FieldPermissions` | via `FieldPermissions` / Metadata | Sim | Sim |
| Acesso a Apex/VF/ConnectedApp/Flow | via `SetupEntityAccess` | `SetupEntityAccess` | via `SetupEntityAccess` / Metadata | Sim | Sim |
| Tipos de registro | Sim (`<recordTypeVisibilities>`) | `Profile.RecordType` não é consultável diretamente | Sim (via Metadata) | Sim | Sim |
| Layout assignment | Sim (`<layoutAssignments>`) | — | Sim (via Metadata) | Sim | Sim |
| App padrão/visível | Sim (`<applicationVisibilities>`) | — | Sim (via Metadata) | Sim | Sim |
| Usuários com o perfil | via `User` | `User.ProfileId` | `User` | Sim | Sim |
| Histórico de alterações | — | — | — | `SetupAuditTrail` | `SetupAuditTrail` |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`Profile`)

Arquivo típico: `profiles/<API_Name>.profile-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<applicationVisibilities>` | 0..N | Apps Lightning/Classic visíveis e default. |
| `<classAccesses>` | 0..N | Acesso a classes Apex. |
| `<custom>` | 0..1 | Indica se é perfil custom (true) ou standard (false). |
| `<description>` | 0..1 | Descrição. |
| `<fieldPermissions>` | 0..N | Permissões de campo (Read/Edit). |
| `<layoutAssignments>` | 0..N | Layout padrão por objeto/tipo de registro. |
| `<loginHours>` | 0..1 | Restrição de horário de login. |
| `<loginIpRanges>` | 0..N | Restrição de faixa de IP. |
| `<objectPermissions>` | 0..N | Permissões de objeto (CRUD + ViewAll/ModifyAll). |
| `<pageAccesses>` | 0..N | Acesso a páginas Visualforce. |
| `<recordTypeVisibilities>` | 0..N | Disponibilidade de tipos de registro. |
| `<tabVisibilities>` | 0..N | Visibilidade de abas. |
| `<userLicense>` | 1 | Licença associada ao perfil. |
| `<userPermissions>` | 0..N | Permissões de usuário (API Enabled, Modify All Data etc.). |

##### Bloco `<objectPermissions>`

| Campo | Significado prático |
|---|---|
| `<object>` | API Name do objeto. |
| `<allowCreate>` | Permite criar registros. |
| `<allowDelete>` | Permite excluir registros. |
| `<allowEdit>` | Permite editar registros. |
| `<allowRead>` | Permite ler registros. |
| `<modifyAllRecords>` | Pode modificar todos os registros (ignora sharing). |
| `<viewAllRecords>` | Pode ver todos os registros (ignora sharing). |

##### Bloco `<fieldPermissions>`

| Campo | Significado prático |
|---|---|
| `<field>` | API Name do campo (`Object.Field`). |
| `<editable>` | Permite edição. |
| `<readable>` | Permite leitura. |

##### Bloco `<userPermissions>`

| Campo | Significado prático |
|---|---|
| `<name>` | Nome interno da permissão (ex.: `ApiEnabled`, `ViewSetup`). |
| `<enabled>` | true/false. |

> **Atenção**: perfis standard podem ter campos read-only parcialmente. Managed profiles podem não ser editáveis.

---

### 3.2 Objeto interno via API padrão: `Profile`

| Campo | Significado prático |
|---|---|
| `Id` | ID do perfil. |
| `Name` | Nome do perfil. |
| `UserLicenseId` / `UserLicense.Name` | Licença associada. |
| `UserType` | Tipo de usuário (Standard, PowerPartner etc.). |
| `PermissionsApiEnabled`, `PermissionsModifyAllData`, etc. | Flags de permissões de usuário. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, Name, UserLicense.Name, UserType,
       PermissionsApiEnabled, PermissionsModifyAllData,
       CreatedDate, LastModifiedDate
FROM Profile
ORDER BY Name
```

---

### 3.3 Tabelas internas de concessão de acesso

#### `ObjectPermissions`

| Campo | Significado prático |
|---|---|
| `Id` | ID da permissão. |
| `ParentId` | `ProfileId` ou `PermissionSetId`. |
| `Parent.Profile.Name` / `Parent.Name` | Nome do perfil/permission set. |
| `SobjectType` | API Name do objeto. |
| `PermissionsCreate`, `PermissionsRead`, `PermissionsEdit`, `PermissionsDelete` | CRUD. |
| `PermissionsViewAllRecords`, `PermissionsModifyAllRecords` | ViewAll/ModifyAll. |

```sql
SELECT Id, ParentId, Parent.Name, SobjectType,
       PermissionsCreate, PermissionsRead, PermissionsEdit, PermissionsDelete,
       PermissionsViewAllRecords, PermissionsModifyAllRecords
FROM ObjectPermissions
WHERE ParentId IN (SELECT Id FROM Profile WHERE Name = 'Vendas')
ORDER BY SobjectType
```

#### `FieldPermissions`

| Campo | Significado prático |
|---|---|
| `Id` | ID da permissão. |
| `ParentId` | `ProfileId` ou `PermissionSetId`. |
| `SobjectType` | API Name do objeto. |
| `Field` | API Name do campo (`Object.Field`). |
| `PermissionsRead` | Leitura. |
| `PermissionsEdit` | Edição. |

```sql
SELECT Id, ParentId, Parent.Name, SobjectType, Field, PermissionsRead, PermissionsEdit
FROM FieldPermissions
WHERE ParentId IN (SELECT Id FROM Profile WHERE Name = 'Vendas')
ORDER BY SobjectType, Field
```

#### `SetupEntityAccess`

| Campo | Significado prático |
|---|---|
| `Id` | ID do vínculo. |
| `ParentId` | `ProfileId` ou `PermissionSetId`. |
| `SetupEntityId` | ID da entidade (ApexClass, Visualforce Page, ConnectedApp etc.). |
| `SetupEntityType` | Tipo da entidade. |

```sql
SELECT Id, ParentId, Parent.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE ParentId IN (SELECT Id FROM Profile WHERE Name = 'Vendas')
```

#### `User`

```sql
SELECT Id, Name, Username, IsActive, UserRoleId, UserRole.Name, ProfileId, Profile.Name
FROM User
WHERE Profile.Name = 'Vendas'
ORDER BY Name
```

---

### 3.3 Objeto interno via Tooling API

```sql
SELECT Id, FullName, DeveloperName, Metadata
FROM Profile
WHERE DeveloperName = 'Vendas'
```

O campo `Metadata` contém toda a estrutura do perfil.

---

### 3.4 Configuração observável em outras fontes

- **Setup → Profiles**: edição visual.
- **Setup → Permission Sets / Profiles → Object Settings / Field Accessibility**.
- `SetupAuditTrail` para alterações.
- `LoginHistory` para validar acesso efetivo.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Permissões CRUD de objeto | XML, `ObjectPermissions` | `Profile` direto | Requer query relacionada. |
| Permissões de campo | XML, `FieldPermissions` | `Profile` direto | Requer query relacionada. |
| Acesso a setup entities | `SetupEntityAccess` | XML summarizado | Detalhar conforme tipo. |
| Estado de login ativo | `LoginHistory` | XML/Profile | Comportamento efetivo. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `PermissionSet`

- Complementa o perfil sem substituí-lo.
- Todo Permission Set é um container de permissões aditivas.

### 4.2 `PermissionSetAssignment`

- Vincula Permission Set a usuário.
- Um usuário pode ter vários Permission Sets.

### 4.3 `UserRole`

- Papel hierárquico, independente do perfil.
- Influencia sharing e visibilidade de registros.

### 4.4 `Group` / `Queue`

- Usuários com um perfil podem ser membros de grupos públicos e filas.
- Grupos e filas expandem o acesso a registros e notificações.

### 4.5 `RecordType`

- Disponibilidade por perfil define quais tipos de registro o usuário pode criar/visualizar.

---

## 5. Consultas e formas de extração

### 5.1 Profile

```sql
SELECT Id, Name, UserLicense.Name, UserType,
       PermissionsApiEnabled, PermissionsModifyAllData,
       CreatedDate, LastModifiedDate
FROM Profile
ORDER BY Name
```

### 5.2 Object Permissions por Profile

```sql
SELECT Id, ParentId, Parent.Name, SobjectType,
       PermissionsCreate, PermissionsRead, PermissionsEdit, PermissionsDelete,
       PermissionsViewAllRecords, PermissionsModifyAllRecords
FROM ObjectPermissions
WHERE ParentId IN (SELECT Id FROM Profile WHERE Name = 'Vendas')
ORDER BY SobjectType
```

### 5.3 Field Permissions por Profile

```sql
SELECT Id, ParentId, Parent.Name, SobjectType, Field, PermissionsRead, PermissionsEdit
FROM FieldPermissions
WHERE ParentId IN (SELECT Id FROM Profile WHERE Name = 'Vendas')
ORDER BY SobjectType, Field
```

### 5.4 Usuários do Profile

```sql
SELECT Id, Name, Username, IsActive, UserRole.Name, Profile.Name
FROM User
WHERE Profile.Name = 'Vendas'
ORDER BY Name
```

---

## 6. Boas práticas e pontos de atenção

- **Use Permission Sets para permissões adicionais**: mantenha o perfil com o mínimo necessário.
- **Princípio do menor privilégio**: conceda apenas as permissões essenciais.
- **Audite View All / Modify All**: essas permissões ignoram regras de compartilhamento.
- **Cuidado com `Api Enabled` e `View Setup`**: conceder a usuários comuns pode aumentar a superfície de ataque.
- **Mantenha inventário de campos sensíveis**: verifique `FieldPermissions` para dados PII/confidenciais.
- **Evite exclusão de perfis** em uso sem migrar usuários.
- **Perfis de comunidade** possuem limitações específicas de licença.
- **Registre alterações**: use `SetupAuditTrail` para rastrear mudanças.

---

## 7. Links de referência oficial

- [Salesforce Help — Profiles](https://help.salesforce.com/s/articleView?id=sf.users_profiles.htm)
- [Salesforce Developer — Profile Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_profile.htm)
- [Salesforce Developer — ObjectPermissions](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_object_objectpermissions.htm)
- [Salesforce Developer — FieldPermissions](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_object_fieldpermissions.htm)
- [Salesforce Help — Permission Sets](https://help.salesforce.com/s/articleView?id=sf.perm_sets_overview.htm)
