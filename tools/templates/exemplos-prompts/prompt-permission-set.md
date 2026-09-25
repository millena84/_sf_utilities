# Prompt — PermissionSet

## 1. Contexto do componente

### 1.1 O que é
`PermissionSet` (nome funcional: **Permission Set** ou **Conjunto de Permissões**) é um componente de segurança do Salesforce usado para conceder permissões adicionais a usuários, sem alterar seus perfis. Diferente do Profile, que é obrigatório e único por usuário, um usuário pode ter vários Permission Sets atribuídos.

Na prática, um `PermissionSet`:
- agrupa permissões funcionais, de objeto, de campo, de classe Apex, de página Visualforce, de tipos de registro, apps etc.;
- é aditivo: suas permissões se somam às do perfil do usuário;
- pode ser atribuído a um ou mais usuários via `PermissionSetAssignment`;
- pode ser incluído em Permission Set Groups;
- pode conceder acesso a entidades de setup (`SetupEntityAccess`), incluindo External Credential Principals, Connected Apps, Apex classes, Visualforce pages e Flows.

### 1.2 Para que serve
- Conceder permissões granulares sem criar múltiplos perfis.
- Implementar o princípio do menor privilégio.
- Facilitar governança e auditoria de acesso.
- Habilitar/desabilitar acesso a funcionalidades temporariamente.
- Conceder acesso a External Credential Principals para callouts seguros.

### 1.3 Cenários típicos de uso
- Conceder permissão de edição em campos específicos para um time.
- Liberar uma Apex class para um grupo de usuários.
- Conceder acesso a um Connected App específico.
- Dar acesso a um External Credential Principal para integrações.
- Permitir a execução de um Flow específico.
- Habilitar permissões de administrador delegado.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em todas as edições.
- **Experience Cloud** — Permission Sets de membros externos.
- **Service Cloud / Sales Cloud** — permissões funcionais por time.
- **Data Cloud / Agentforce** — permissões para ingestão, AI, etc.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `PermissionSet`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Permission Set |
| Metadata type exact | `PermissionSet` |
| Pasta no projeto SFDX | `permissionsets/` |
| Arquivo padrão | `<apiName>.permissionset-meta.xml` |
| Objeto interno (API padrão) | `PermissionSet` |
| Objeto interno (Tooling API) | `PermissionSet` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM PermissionSet` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `PermissionSet` é consultável |
| Acessível por UI | Sim — **Setup → Permission Sets** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Object Permissions | `ObjectPermissions` (objeto) | Permissões de objeto. |
| Field Permissions | `FieldPermissions` (objeto) | Permissões de campo. |
| Setup Entity Access | `SetupEntityAccess` (objeto) | Acesso a entidades de setup. |
| Permission Set Assignment | `PermissionSetAssignment` (objeto) | Vincula Permission Set a usuário. |
| Permission Set Group | `PermissionSetGroup` (metadata/API) | Agrupa Permission Sets. |
| Permission Set Group Component | `PermissionSetGroupComponent` (objeto) | Relaciona Permission Set ao Group. |
| Muting Permission Set | `MutingPermissionSet` | Silence permissions dentro de um Group. |
| User | `User` | Usuários que recebem o Permission Set. |
| Profile | `Profile` | Perfil base do usuário. |
| External Credential Principal | `ExternalCredentialPrincipal` | Acesso via `SetupEntityAccess`. |
| Connected App | `ConnectedApplication` | Acesso via `SetupEntityAccess`. |
| ApexClass / ApexPage / Flow | `ApexClass`, `ApexPage`, `Flow` | Acesso via `SetupEntityAccess`. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | PermissionSet metadata | `PermissionSet` (SOQL) | `PermissionSet` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | Sim | Sim | Sim | Sim |
| Descrição / licença | Sim (`<description>`, `<license>`) | `Description`, `License.Name` | Sim | Sim | Sim |
| Permissões de usuário | Sim (`<userPermissions>`) | `PermissionsXxx` | Sim | Sim | Sim |
| Permissões de objeto | `<objectPermissions>` | `ObjectPermissions` | via Metadata | Sim | Sim |
| Permissões de campo | `<fieldPermissions>` | `FieldPermissions` | via Metadata | Sim | Sim |
| Setup Entity Access | `<classAccesses>`, `<pageAccesses>` etc. | `SetupEntityAccess` | via Metadata | Sim | Sim |
| Atribuições a usuários | via `PermissionSetAssignment` | `PermissionSetAssignment` | via SOQL | Sim | Sim |
| Histórico de alterações | — | — | — | `SetupAuditTrail` | `SetupAuditTrail` |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`PermissionSet`)

Arquivo típico: `permissionsets/<API_Name>.permissionset-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<applicationVisibilities>` | 0..N | Apps visíveis/default. |
| `<classAccesses>` | 0..N | Acesso a Apex classes. |
| `<customPermissions>` | 0..N | Custom permissions. |
| `<description>` | 0..1 | Descrição. |
| `<fieldPermissions>` | 0..N | Permissões de campo. |
| `<hasActivationRequired>` | 0..1 | Se requer ativação de sessão. |
| `<label>` | 1 | Nome amigável. |
| `<license>` | 0..1 | Licença associada (ex.: `Salesforce`, `Salesforce Platform`). |
| `<objectPermissions>` | 0..N | Permissões de objeto. |
| `<pageAccesses>` | 0..N | Acesso a Visualforce pages. |
| `<recordTypeVisibilities>` | 0..N | Tipos de registro disponíveis. |
| `<tabVisibilities>` | 0..N | Visibilidade de abas. |
| `<userPermissions>` | 0..N | Permissões de usuário. |

#### Observações

- Permission Set nunca restringe permissões — apenas adiciona.
- Um Permission Set com `<license>` só pode ser atribuído a usuários com essa licença.
- Campos `<fieldPermissions>` com `editable=true` geralmente exigem `readable=true`.

---

### 3.2 Objeto interno via API padrão: `PermissionSet`

| Campo | Significado prático |
|---|---|
| `Id` | ID do Permission Set. |
| `Name` | API Name. |
| `Label` | Nome amigável. |
| `Description` | Descrição. |
| `LicenseId` / `License.Name` | Licença associada. |
| `IsOwnedByProfile` | Se é o Permission Set gerado automaticamente por um Profile. |
| `ProfileId` | Perfil associado (quando `IsOwnedByProfile = true`). |
| `PermissionsApiEnabled`, etc. | Flags de permissões de usuário. |
| `NamespacePrefix` | Namespace do pacote. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, Name, Label, Description, License.Name, IsOwnedByProfile, Profile.Name,
       NamespacePrefix, CreatedDate, LastModifiedDate
FROM PermissionSet
WHERE IsOwnedByProfile = false
ORDER BY Label
```

---

### 3.3 Tabelas internas de concessão de acesso

#### `PermissionSetAssignment`

| Campo | Significado prático |
|---|---|
| `Id` | ID da atribuição. |
| `AssigneeId` | `User.Id` que recebeu o Permission Set. |
| `PermissionSetId` | Permission Set atribuído. |
| `PermissionSetGroupId` | Permission Set Group atribuído (quando aplicável). |

```sql
SELECT Id, PermissionSetId, PermissionSet.Name, AssigneeId, Assignee.Name, Assignee.Username
FROM PermissionSetAssignment
WHERE PermissionSet.IsOwnedByProfile = false
ORDER BY PermissionSet.Name, Assignee.Name
```

#### `ObjectPermissions` (Permission Set)

```sql
SELECT Id, ParentId, Parent.Name, SobjectType,
       PermissionsCreate, PermissionsRead, PermissionsEdit, PermissionsDelete,
       PermissionsViewAllRecords, PermissionsModifyAllRecords
FROM ObjectPermissions
WHERE ParentId IN (SELECT Id FROM PermissionSet WHERE Name = 'Meu_Permission_Set')
ORDER BY SobjectType
```

#### `FieldPermissions` (Permission Set)

```sql
SELECT Id, ParentId, Parent.Name, SobjectType, Field, PermissionsRead, PermissionsEdit
FROM FieldPermissions
WHERE ParentId IN (SELECT Id FROM PermissionSet WHERE Name = 'Meu_Permission_Set')
ORDER BY SobjectType, Field
```

#### `SetupEntityAccess` (Permission Set)

```sql
SELECT Id, ParentId, Parent.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE ParentId IN (SELECT Id FROM PermissionSet WHERE Name = 'Meu_Permission_Set')
ORDER BY SetupEntityType
```

#### `PermissionSetGroupComponent`

Relaciona Permission Set aos seus Groups.

```sql
SELECT Id, PermissionSetGroupId, PermissionSetGroup.DeveloperName,
       PermissionSetId, PermissionSet.Name
FROM PermissionSetGroupComponent
ORDER BY PermissionSetGroup.DeveloperName, PermissionSet.Name
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Permission Sets → gerenciamento de atribuições.
- Setup → Permission Set Groups.
- Setup → Permission Set Licenses (licenças disponíveis).
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Atribuição a usuários | `PermissionSetAssignment` | XML do Permission Set | Estado efetivo de uso. |
| Acesso efetivo de usuário | `UserRecordAccess` | Permission Set isolado | Soma com perfil e outros PS. |
| Histórico de atribuição | `SetupAuditTrail` | Permission Set metadata | Rastreabilidade. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `PermissionSetGroup` / `MutingPermissionSet`

- Groups consolidam múltiplos Permission Sets.
- Muting Permission Sets silenciam permissões específicas dentro de um Group.
- `PermissionSetGroupComponent` faz a ligação.

### 4.2 `Profile`

- Perfil base do usuário. Permission Sets são aditivos a ele.
- Cada Profile gera um Permission Set "owned by profile" (`IsOwnedByProfile = true`).

### 4.3 `User`

- Recebe Permission Sets via `PermissionSetAssignment`.
- Acesso efetivo é a união de perfil + todos os PSs + hierarquia + sharing.

### 4.4 `SetupEntityAccess`

- Permite auditar acesso a Apex, Visualforce, Connected Apps, Flows, External Credential Principals.

---

## 5. Consultas e formas de extração

### 5.1 Permission Sets não vinculados a perfil

```sql
SELECT Id, Name, Label, Description, License.Name, NamespacePrefix,
       CreatedDate, LastModifiedDate
FROM PermissionSet
WHERE IsOwnedByProfile = false
ORDER BY Label
```

### 5.2 Atribuições de Permission Set

```sql
SELECT Id, PermissionSetId, PermissionSet.Name, PermissionSet.Label,
       AssigneeId, Assignee.Name, Assignee.Username, Assignee.IsActive
FROM PermissionSetAssignment
WHERE PermissionSet.IsOwnedByProfile = false
ORDER BY PermissionSet.Name, Assignee.Name
```

### 5.3 Permissões de objeto e campo de um Permission Set

```sql
SELECT Id, ParentId, Parent.Name, SobjectType, Field, PermissionsRead, PermissionsEdit
FROM FieldPermissions
WHERE ParentId IN (SELECT Id FROM PermissionSet WHERE Name = 'Meu_Permission_Set')
ORDER BY SobjectType, Field
```

### 5.4 Setup Entity Access de um Permission Set

```sql
SELECT Id, ParentId, Parent.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE ParentId IN (SELECT Id FROM PermissionSet WHERE Name = 'Meu_Permission_Set')
ORDER BY SetupEntityType
```

---

## 6. Boas práticas e pontos de atenção

- **Use Permission Sets em vez de proliferar perfis**: crie perfis base e complemente com PS.
- **Documente o propósito** de cada Permission Set na descrição.
- **Agrupe por função**, não por usuário individual.
- **Revise atribuições periódicas**: remova PSs de usuários que não precisam mais.
- **Atenção a licenças**: Permission Sets com `<license>` restrito só podem ser atribuídos a usuários com a licença.
- **Cuidado com View All / Modify All**: use com restrição e justificativa.
- **External Credential Principal Access**: conceda o mínimo necessário para callouts.
- **Rastreie alterações**: use `SetupAuditTrail`.
- **Não delete Permission Sets atribuídos** sem planejar migração.

---

## 7. Links de referência oficial

- [Salesforce Help — Permission Sets](https://help.salesforce.com/s/articleView?id=sf.perm_sets_overview.htm)
- [Salesforce Help — Permission Set Groups](https://help.salesforce.com/s/articleView?id=sf.perm_set_groups_overview.htm)
- [Salesforce Developer — PermissionSet Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionset.htm)
- [Salesforce Developer — PermissionSetAssignment](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_object_permissionsetassignment.htm)
- [Salesforce Developer — ObjectPermissions](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_object_objectpermissions.htm)
- [Salesforce Developer — FieldPermissions](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_object_fieldpermissions.htm)
