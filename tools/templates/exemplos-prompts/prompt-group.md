# Prompt — Group

## 1. Contexto do componente

### 1.1 O que é
`Group` (nome funcional: **Public Group** ou simplesmente **Grupo**) é um componente do Salesforce usado para agrupar usuários, funções, subordinados de função, territórios e até outros grupos. Os grupos são amplamente utilizados para regras de compartilhamento, notificações, atribuição de registros, aprovações e filas.

Na prática, um `Group`:
- representa uma coleção de membros de diferentes tipos (`User`, `Role`, `RoleAndSubordinates`, `Territory`, `TerritoryAndSubordinates`, `PartnerUser`, `Manager`, `ManagerAndSubordinatesInternal`, `AllCustomerPortalUsers`, `AllPartnerUsers`, `Queue`, `Organization`, `Regular`);
- pode ser referenciado em regras de compartilhamento (`SharingRule`);
- pode ser usado como destinatário em notificações e templates de email;
- pode ser membro de outro grupo (aninhamento);
- pode representar automaticamente uma função (`Role`) ou uma fila (`Queue`) através do campo `RelatedId`.

### 1.2 Para que serve
- Simplificar a aplicação de regras de compartilhamento para conjuntos de usuários.
- Facilitar notificações em massa.
- Apoiar fluxos de aprovação e atribuição.
- Criar agrupamentos lógicos sem depender de perfis ou papéis.

### 1.3 Cenários típicos de uso
- Compartilhar registros de uma região com todos os usuários do time comercial daquela região.
- Enviar notificação para um grupo de gerentes.
- Definir aprovadores de um processo de aprovação.
- Aninhar grupos regionais em um grupo nacional.
- Vincular membros a uma fila (Queue) via `Group` do tipo Queue.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em todas as edições.
- **Experience Cloud** — grupos para parceiros e clientes.
- **Service Cloud / Sales Cloud** — compartilhamento e atribuição.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `Group`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Public Group |
| Metadata type exact | `Group` (quando é public group / queue group) — filas também geram `Group` |
| Pasta no projeto SFDX | `groups/` |
| Arquivo padrão | `<apiName>.group-meta.xml` |
| Objeto interno (API padrão) | `Group` |
| Objeto interno (Tooling API) | `Group` (com campo `Metadata` quando aplicável) |
| Acessível por Metadata API | Sim — retrieve/deploy (public groups) |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM Group` |
| Acessível por Tooling API | Sim (parcial) |
| Acessível por Apex | Sim — `Group` é consultável |
| Acessível por UI | Sim — **Setup → Public Groups** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Group Member | `GroupMember` | Ligação entre grupo e usuário/grupo/função/etc. |
| Queue | `Queue` | Fila gera um `Group` do tipo `Queue`. |
| Queue Sobject | `QueueSobject` | Associa fila a objetos. |
| User | `User` | Membro do tipo usuário. |
| User Role | `UserRole` | Grupos automáticos do tipo `Role` e `RoleAndSubordinates`. |
| Territory | `Territory2` | Grupos automáticos de território. |
| Sharing Rule | `SharingRules` (metadata) / `Group` em criteria/owner rules | Grupo pode ser destino de compartilhamento. |
| Approval Process | `ApprovalProcess` | Grupos podem ser aprovadores. |
| Email Alert | `WorkflowAlert` | Grupos podem ser destinatários. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | Group metadata | `Group` (SOQL) | Tooling | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | `Name`, `DeveloperName` | Sim | Sim | Sim |
| Tipo | Sim (`<doesIncludeBosses>`, etc.) | `Type` | Sim | Sim | Sim |
| Membros | `<groupMembers>` no metadata (quando disponível) | `GroupMember` | Sim | Sim | Sim |
| Grupo relacionado (Role/Queue) | `RelatedId` | `RelatedId` | Sim | Sim | Sim |
| Public Group vs Queue | `Type` = `Regular` / `Queue` | `Type` | Sim | Sim | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`Group`)

Arquivo típico: `groups/<API_Name>.group-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<description>` | 0..1 | Descrição do grupo. |
| `<doesIncludeBosses>` | 0..1 | Para grupos baseados em função, se inclui chefes. |
| `<name>` | 1 | Nome amigável. |
| `<groupMembers>` | 0..N (quando suportado) | Membros declarativos. |

> **Atenção**: Public Groups criados via UI têm seus membros armazenados em `GroupMember`, não necessariamente no XML do metadata.

### 3.2 Objeto interno via API padrão: `Group`

| Campo | Significado prático |
|---|---|
| `Id` | ID do grupo. |
| `Name` | Nome amigável. |
| `DeveloperName` | API Name. |
| `RelatedId` | ID do `UserRole`, `Queue`, `Territory` etc. relacionado. |
| `Type` | Tipo do grupo. |
| `Email` | Endereço de email do grupo (usado para notificações). |
| `DoesIncludeBosses` | Inclui chefes acima na hierarquia. |
| `DoesSendEmailToMembers` | Se notificações são enviadas a membros. |
| `OwnerId` | Proprietário do grupo. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Tipos de `Group.Type`

| Tipo | Significado |
|---|---|
| `Regular` | Public Group criado manualmente. |
| `Queue` | Grupo gerado por uma fila. |
| `Role` | Grupo automático de uma função. |
| `RoleAndSubordinates` | Função + todos os subordinados. |
| `Territory` | Grupo de território. |
| `TerritoryAndSubordinates` | Território + subordinados. |
| `Manager` | Gerente de um usuário. |
| `ManagerAndSubordinatesInternal` | Gerente + subordinados internos. |
| `AllCustomerPortalUsers` | Todos os usuários de portal de cliente. |
| `AllPartnerUsers` | Todos os usuários de portal de parceiro. |
| `Organization` | Toda a organização. |
| `PartnerUser` | Usuário de parceiro individual. |

#### Exemplo de query

```sql
SELECT Id, Name, DeveloperName, Type, RelatedId, Email,
       DoesIncludeBosses, DoesSendEmailToMembers,
       CreatedDate, LastModifiedDate
FROM Group
ORDER BY Type, Name
```

### 3.3 Tabelas internas de concessão de acesso / associação

#### `GroupMember`

| Campo | Significado prático |
|---|---|
| `Id` | ID do vínculo. |
| `GroupId` | Grupo pai. |
| `UserOrGroupId` | ID do membro (pode ser `User`, `Group`, `UserRole` etc.). |

```sql
SELECT Id, GroupId, Group.Name, UserOrGroupId,
       UserOrGroup.Name, UserOrGroup.Type
FROM GroupMember
WHERE Group.DeveloperName = 'Meu_Grupo'
ORDER BY UserOrGroup.Type, UserOrGroup.Name
```

> **Atenção**: `UserOrGroup.Name` pode exigir query dinâmica dependendo do tipo de membro.

#### `QueueSobject`

Quando o grupo é uma fila (`Type = 'Queue'`), `QueueSobject` define objetos suportados.

```sql
SELECT Id, QueueId, Queue.Name, SobjectType
FROM QueueSobject
ORDER BY Queue.Name, SobjectType
```

#### `Queue`

```sql
SELECT Id, QueueName, DeveloperName, OwnerId, DoesSendEmailToMembers,
       Email
FROM Queue
ORDER BY QueueName
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Public Groups.
- Setup → Queues (para grupos do tipo Queue).
- Setup → Sharing Settings (regras que usam o grupo).
- Setup → Approval Processes (grupos como aprovadores).
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Membros indiretos (subordinados, territórios) | Expandido pelo Salesforce | `GroupMember` direto | Membros implícitos por regra. |
| Regras de compartilhamento que usam o grupo | `SharingRules` metadata / `ObjectSharing` | `Group` isolado | Requer análise cruzada. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `Queue`

- Fila gera automaticamente um `Group` do tipo `Queue`.
- Membros da fila são membros do grupo.

### 4.2 `UserRole`

- Papéis geram grupos `Role` e `RoleAndSubordinates` automaticamente.

### 4.3 `SharingRule`

- Public Groups são frequentemente usados como destinatários de compartilhamento.

### 4.4 `ApprovalProcess`

- Grupos podem ser aprovadores em etapas de aprovação.

### 4.5 `WorkflowAlert`

- Grupos podem ser destinatários de alertas de email.

---

## 5. Consultas e formas de extração

### 5.1 Todos os grupos

```sql
SELECT Id, Name, DeveloperName, Type, RelatedId, Email,
       DoesIncludeBosses, DoesSendEmailToMembers,
       CreatedDate, LastModifiedDate
FROM Group
ORDER BY Type, Name
```

### 5.2 Membros de um grupo

```sql
SELECT Id, GroupId, Group.Name, Group.DeveloperName, UserOrGroupId
FROM GroupMember
WHERE Group.DeveloperName = 'Meu_Grupo'
```

### 5.3 Grupos que incluem determinado usuário

```sql
SELECT Id, GroupId, Group.Name, Group.DeveloperName, Group.Type
FROM GroupMember
WHERE UserOrGroupId = '005...'
```

### 5.4 Filas e objetos suportados

```sql
SELECT Id, QueueId, Queue.Name, SobjectType
FROM QueueSobject
ORDER BY Queue.Name, SobjectType
```

---

## 6. Boas práticas e pontos de atenção

- **Documente o propósito** do grupo na descrição.
- **Evite aninhamentos excessivos** para facilitar análise de membros efetivos.
- **Revise periódicamente** grupos não utilizados.
- **Cuidado com `RoleAndSubordinates`**: pode ampliar acesso mais do que o esperado.
- **Não delete grupos** usados em sharing rules, approval processes ou workflows.
- **Rastreie alterações**: use `SetupAuditTrail`.
- **Distinga grupos de fila**: embora ambos usem `Group`, filas possuem `QueueSobject` e comportamento adicional.

---

## 7. Links de referência oficial

- [Salesforce Help — Public Groups](https://help.salesforce.com/s/articleView?id=sf.collab_groups.htm)
- [Salesforce Developer — Group Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_group.htm)
- [Salesforce Developer — GroupMember Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_groupmember.htm)
- [Salesforce Help — Queues](https://help.salesforce.com/s/articleView?id=sf.queues_overview.htm)
