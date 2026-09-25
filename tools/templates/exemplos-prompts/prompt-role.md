# Prompt — UserRole

## 1. Contexto do componente

### 1.1 O que é
`UserRole` (nome funcional: **Role** ou **Papel**) é um componente de controle de acesso no Salesforce que define a posição hierárquica de um usuário na organização. Diferente do Profile, que controla permissões funcionais, o Role controla o **acesso a dados** por meio da hierarquia de papéis e regras de compartilhamento.

Na prática, um `UserRole`:
- define um nó na hierarquia de papéis da org;
- determina quais registros um usuário pode visualizar via role hierarchy (`View All Data` implícito na hierarquia);
- pode ter uma função pai (`ParentRoleId`), criando a estrutura de árvore;
- está associado a usuários via `User.UserRoleId`;
- pode ter um nome de portal/oportunidade quando relacionado a parceiros.

### 1.2 Para que serve
- Controlar sharing de registros através da hierarquia organizacional.
- Permitir que gerentes visualizem registros de subordinados.
- Suportar previsões, territórios e relatórios hierárquicos.
- Definir escopo de dados por função empresarial.

### 1.3 Cenários típicos de uso
- Hierarquia comercial: Representante → Gerente → Diretor → CEO.
- Hierarquia de suporte: Analista → Coordenador → Gerente.
- Papéis de parceiro em Experience Cloud.
- Papéis específicos de previsão e território.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em todas as edições com roles habilitadas.
- **Experience Cloud** — roles podem ser usados por parceiros.
- **Sales Cloud** — previsão, pipeline, hierarquia comercial.
- **Service Cloud** — escalonamento e visibilidade de casos.

> **Nota de licença**: algumas edições limitam a quantidade de roles ou não suportam hierarquia de papéis para certos tipos de usuário (ex.: Chatter Free).

---

## 2. Mapa estrutural

### 2.1 Componente principal: `UserRole`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Role / Papel |
| Metadata type exact | `Role` |
| Pasta no projeto SFDX | `roles/` |
| Arquivo padrão | `<apiName>.role-meta.xml` |
| Objeto interno (API padrão) | `UserRole` |
| Objeto interno (Tooling API) | `UserRole` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM UserRole` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `UserRole` é consultável |
| Acessível por UI | Sim — **Setup → Roles** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| User | `User` | Usuários com o papel. |
| Parent Role | `UserRole.ParentRoleId` | Hierarquia ascendente. |
| Portal Account/Role | `UserRole.PortalType`, `UserRole.PortalAccountId` | Papéis de parceiro/cliente em portal. |
| Forecast | `ForecastingSettings`, `ForecastingType` | Papéis podem participar de previsões. |
| Territory | `Territory2`, `UserTerritory2Association` | Relação com territórios (se ativado). |
| Group | `Group` | Cada role gera automaticamente um `Group` de tipo "Role". |
| Group Member | `GroupMember` | Membros implícitos pelo papel. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | Role metadata | `UserRole` (SOQL) | `UserRole` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | Sim | Sim | Sim | Sim |
| Pai na hierarquia | Sim (`<parentRole>`) | `ParentRoleId` | Sim | Sim | Sim |
| Forecast/Forecasting enabled | Sim (`<opportunityAccessLevel>`, etc.) | `ForecastUserId`, campos de forecast | Sim | Sim | Sim |
| Tipo de portal | Sim (`<portalType>`, `<portalAccount>`) | `PortalType`, `PortalAccountId` | Sim | Sim | Sim |
| Usuários do papel | via `User` | `User.UserRoleId` | via `User` | Sim | Sim |
| Grupo gerado automaticamente | via `Group` | `Group.RelatedId` = `UserRole.Id` | via `Group` | Sim | Sim |
| Acesso efetivo a registros | — | — | — | — | Sharing, `UserRecordAccess` |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`Role`)

Arquivo típico: `roles/<API_Name>.role-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<caseAccessLevel>` | 1 | Nível de acesso a cases pela hierarquia: `None`, `Read`, `Edit`. |
| `<contactAccessLevel>` | 1 | Nível de acesso a contatos. |
| `<description>` | 0..1 | Descrição. |
| `<mayForecastManagerShare>` | 0..1 | Se gerente de forecast pode compartilhar previsões. |
| `<name>` | 1 | Nome amigável do papel. |
| `<opportunityAccessLevel>` | 1 | Nível de acesso a oportunidades. |
| `<parentRole>` | 0..1 | API Name do papel pai. |
| `<portalAccount>` | 0..1 | Conta vinculada a papel de portal. |
| `<portalType>` | 0..1 | Tipo de portal (Partner, Customer etc.). |
| `<rollupDescription>` | 0..1 | Label de rollup usado em relatórios. |

#### Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Role xmlns="http://soap.sforce.com/2006/04/metadata">
    <caseAccessLevel>Edit</caseAccessLevel>
    <contactAccessLevel>Edit</contactAccessLevel>
    <description>Gerente comercial</description>
    <mayForecastManagerShare>false</mayForecastManagerShare>
    <name>Gerente de Vendas</name>
    <opportunityAccessLevel>Edit</opportunityAccessLevel>
    <parentRole>Diretor_Comercial</parentRole>
</Role>
```

### 3.2 Objeto interno via API padrão: `UserRole`

| Campo | Significado prático |
|---|---|
| `Id` | ID do papel. |
| `Name` | Nome amigável. |
| `DeveloperName` | API Name. |
| `ParentRoleId` | Papel pai. |
| `CaseAccessForAccountOwner`, `OpportunityAccessForAccountOwner` | Níveis de acesso. |
| `ForecastUserId` | Usuário de forecast associado. |
| `PortalType`, `PortalAccountId` | Portal. |
| `RollupDescription` | Label de rollup. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, DeveloperName, Name, ParentRoleId, ParentRole.Name,
       PortalType, ForecastUserId, RollupDescription,
       CreatedDate, LastModifiedDate
FROM UserRole
ORDER BY ParentRoleId NULLS FIRST, Name
```

### 3.3 Grupo gerado automaticamente

Cada `UserRole` gera um registro em `Group` do tipo `Role`.

```sql
SELECT Id, DeveloperName, RelatedId, Type
FROM Group
WHERE Type = 'Role'
ORDER BY DeveloperName
```

### 3.4 Usuários do papel

```sql
SELECT Id, Name, Username, IsActive, UserRoleId, UserRole.Name
FROM User
WHERE UserRole.Name = 'Gerente de Vendas'
ORDER BY Name
```

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `User`

- Associação direta via `UserRoleId`.
- Usuários herdam acesso de todos os papéis abaixo na hierarquia.

### 4.2 `Group`

- `Group.Type = 'Role'` representa o papel para regras de compartilhamento.
- `Group.Type = 'RoleAndSubordinates'` representa papel + subordinados.

### 4.3 `UserRecordAccess`

- Permite verificar acesso efetivo de um usuário a um registro.

```sql
SELECT RecordId, HasReadAccess, HasEditAccess, HasDeleteAccess, MaxAccessLevel
FROM UserRecordAccess
WHERE UserId = '005...' AND RecordId = '001...'
```

### 4.4 `SetupAuditTrail`

- Rastreia alterações na hierarquia de papéis.

---

## 5. Consultas e formas de extração

### 5.1 Hierarchy de papéis

```sql
SELECT Id, DeveloperName, Name, ParentRoleId, ParentRole.Name
FROM UserRole
ORDER BY ParentRoleId NULLS FIRST, Name
```

### 5.2 Grupos de Role

```sql
SELECT Id, DeveloperName, RelatedId, Type
FROM Group
WHERE Type IN ('Role', 'RoleAndSubordinates')
ORDER BY Type, DeveloperName
```

### 5.3 Usuários por papel

```sql
SELECT Id, Name, Username, IsActive, UserRoleId, UserRole.Name
FROM User
WHERE UserRole.Name != null
ORDER BY UserRole.Name, Name
```

---

## 6. Boas práticas e pontos de atenção

- **Hierarquia de papéis ≠ permissões funcionais**: Role controla dados, Profile/Permission Set controlam permissões.
- **Evite hierarquias muito profundas**: dificultam manutenção e performance de sharing.
- **Validate role access com `UserRecordAccess`**: configuração declarativa pode ter efeitos inesperados.
- **Cuidado com `RoleAndSubordinates`**: concede acesso a toda a subárvore.
- **Não delete roles em uso**: migre usuários antes.
- **Papéis de portal**: atenção a licenças e visibilidade de dados de parceiro.
- **Rastreie alterações**: use `SetupAuditTrail`.

---

## 7. Links de referência oficial

- [Salesforce Help — Roles](https://help.salesforce.com/s/articleView?id=sf.roles_overview.htm)
- [Salesforce Developer — Role Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_role.htm)
- [Salesforce Developer — UserRole Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_userrole.htm)
- [Salesforce Help — Set Up Role Hierarchy](https://help.salesforce.com/s/articleView?id=sf.admin_roles.htm)
