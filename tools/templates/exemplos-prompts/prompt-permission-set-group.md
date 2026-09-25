# Prompt — PermissionSetGroup

## 1. Contexto do componente

### 1.1 O que é
`PermissionSetGroup` (nome funcional: **Permission Set Group** ou **Grupo de Conjuntos de Permissões**) é um componente de segurança do Salesforce que permite agrupar vários `PermissionSets` em um único container. O grupo é atribuído diretamente aos usuários, e o acesso resultante é a união de todos os Permission Sets do grupo, considerando eventuais `MutingPermissionSets` que silenciam permissões indesejadas.

Na prática, um `PermissionSetGroup`:
- agrupa múltiplos Permission Sets de forma lógica;
- permite atribuir várias permissões de uma só vez;
- pode conter Muting Permission Sets para remover permissões específicas do grupo;
- facilita a governança em cenários com muitos Permission Sets;
- revela permissões efetivas calculadas no campo `Status` (`Updated`, `Updating`, `Failed`).

### 1.2 Para que serve
- Simplificar a atribuição de permissões a usuário.
- Modelar funções empresariais com múltiplos Permission Sets.
- Permitir sobreposição controlada de permissões com mutes.
- Reduzir o erro de esquecer um Permission Set necessário.

### 1.3 Cenários típicos de uso
- "Funcionário de Vendas" = PS_CRM_Base + PS_Oportunidade + PS_Relatórios.
- "Gerente de Suporte" = PS_CRM_Base + PS_Case_Avançado + PS_Dashboards.
- Remover campo sensível de um grupo com Muting Permission Set.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em todas as edições com Permission Sets habilitados.
- **Experience Cloud** — grupos para usuários externos.
- **Service Cloud / Sales Cloud** — funções operacionais.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `PermissionSetGroup`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Permission Set Group |
| Metadata type exact | `PermissionSetGroup` |
| Pasta no projeto SFDX | `permissionsetgroups/` |
| Arquivo padrão | `<apiName>.permissionsetgroup-meta.xml` |
| Objeto interno (API padrão) | `PermissionSetGroup` |
| Objeto interno (Tooling API) | `PermissionSetGroup` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM PermissionSetGroup` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `PermissionSetGroup` é consultável |
| Acessível por UI | Sim — **Setup → Permission Set Groups** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Permission Set | `PermissionSet` | Membros do grupo. |
| Muting Permission Set | `MutingPermissionSet` | Remove permissões do grupo. |
| Permission Set Group Component | `PermissionSetGroupComponent` | Ligação entre grupo e Permission Sets. |
| Permission Set Assignment | `PermissionSetAssignment` | Vincula grupo a usuário. |
| User | `User` | Usuários que recebem o grupo. |
| Permission Set | `PermissionSet` (via `IsOwnedByProfile`) | Perfil base pode complementar. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | PermissionSetGroup metadata | `PermissionSetGroup` (SOQL) | Tooling | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | Sim | Sim | Sim | Sim |
| Permission Sets membros | `<permissionSets>` | via `PermissionSetGroupComponent` | via Metadata | Sim | Sim |
| Muting Permission Sets | `<mutingPermissionSets>` | via `PermissionSetGroupComponent` | via Metadata | Sim | Sim |
| Status de recálculo | — | `Status` | Sim | Sim | Sim |
| Atribuições a usuários | — | `PermissionSetAssignment` | via SOQL | Sim | Sim |
| Histórico | — | — | — | `SetupAuditTrail` | `SetupAuditTrail` |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`PermissionSetGroup`)

Arquivo típico: `permissionsetgroups/<API_Name>.permissionsetgroup-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<description>` | 0..1 | Descrição do grupo. |
| `<label>` | 1 | Nome amigável. |
| `<mutingPermissionSets>` | 0..N | API Names dos Muting Permission Sets. |
| `<permissionSets>` | 0..N | API Names dos Permission Sets incluídos. |
| `<status>` | 0..1 | Estado na UI: `Updated`, `Updating`, `Failed`. |

### 3.2 Objeto interno via API padrão: `PermissionSetGroup`

| Campo | Significado prático |
|---|---|
| `Id` | ID do grupo. |
| `DeveloperName` | API Name. |
| `MasterLabel` | Nome amigável. |
| `Description` | Descrição. |
| `Status` | `Updated`, `Updating`, `Failed`. |
| `NamespacePrefix` | Namespace do pacote. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, DeveloperName, MasterLabel, Description, Status, NamespacePrefix,
       CreatedDate, LastModifiedDate
FROM PermissionSetGroup
ORDER BY MasterLabel
```

### 3.3 Tabelas internas de concessão de acesso

#### `PermissionSetGroupComponent`

| Campo | Significado prático |
|---|---|
| `Id` | ID do componente. |
| `PermissionSetGroupId` | Grupo pai. |
| `PermissionSetId` | Permission Set ou Muting Permission Set. |

```sql
SELECT Id, PermissionSetGroupId, PermissionSetGroup.DeveloperName,
       PermissionSetId, PermissionSet.Name, PermissionSet.Label
FROM PermissionSetGroupComponent
ORDER BY PermissionSetGroup.DeveloperName, PermissionSet.Name
```

#### `PermissionSetAssignment` (para grupos)

```sql
SELECT Id, PermissionSetGroupId, PermissionSetGroup.DeveloperName,
       AssigneeId, Assignee.Name, Assignee.Username
FROM PermissionSetAssignment
WHERE PermissionSetGroupId != null
ORDER BY PermissionSetGroup.DeveloperName, Assignee.Name
```

#### `MutingPermissionSet`

```sql
SELECT Id, DeveloperName, MasterLabel, IsSoftDeleted
FROM MutingPermissionSet
ORDER BY MasterLabel
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Permission Set Groups.
- `SetupAuditTrail`.
- UI de recálculo do grupo.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Permissões efetivas calculadas | `PermissionSetGroup.Status` + Permission Sets | Grupo isolado | Soma com perfil e outros grupos. |
| Histórico de atribuição | `SetupAuditTrail` | Metadata | Rastreabilidade. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `PermissionSet`

- Membros do grupo. Permissões efetivas são a união de todos os membros menos mutes.

### 4.2 `MutingPermissionSet`

- Remove permissões específicas de objeto/campo/setup do grupo.

### 4.3 `PermissionSetAssignment`

- Vincula o grupo a usuários.

### 4.4 `Profile`

- Acesso final = Profile + Permission Set Groups + Permission Sets individuais.

---

## 5. Consultas e formas de extração

### 5.1 Grupos e status

```sql
SELECT Id, DeveloperName, MasterLabel, Description, Status, NamespacePrefix,
       CreatedDate, LastModifiedDate
FROM PermissionSetGroup
ORDER BY MasterLabel
```

### 5.2 Componentes de cada grupo

```sql
SELECT Id, PermissionSetGroupId, PermissionSetGroup.DeveloperName,
       PermissionSetId, PermissionSet.Name, PermissionSet.Label
FROM PermissionSetGroupComponent
WHERE PermissionSetGroup.DeveloperName = 'Grupo_Vendas'
ORDER BY PermissionSet.Name
```

### 5.3 Atribuições a usuários

```sql
SELECT Id, PermissionSetGroupId, PermissionSetGroup.DeveloperName,
       AssigneeId, Assignee.Name, Assignee.Username, Assignee.IsActive
FROM PermissionSetAssignment
WHERE PermissionSetGroupId = '0PG...'
ORDER BY Assignee.Name
```

---

## 6. Boas práticas e pontos de atenção

- **Evite sobreposição excessiva** de Permission Sets no mesmo grupo.
- **Use Muting Permission Sets** em vez de editar Permission Sets reutilizáveis.
- **Monitore o `Status`**: `Failed` indica conflito ou erro de recálculo.
- **Documente a finalidade** do grupo na descrição.
- **Prefira grupos por função empresarial** em vez de atribuir PSs avulsos.
- **Não delete grupos atribuídos** sem migrar usuários.
- **Rastreie alterações** via `SetupAuditTrail`.

---

## 7. Links de referência oficial

- [Salesforce Help — Permission Set Groups](https://help.salesforce.com/s/articleView?id=sf.perm_set_groups_overview.htm)
- [Salesforce Developer — PermissionSetGroup Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionsetgroup.htm)
- [Salesforce Developer — MutingPermissionSet](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_object_mutingpermissionset.htm)
