# Prompt — CustomObject

## 1. Contexto do componente

### 1.1 O que é
`CustomObject` (nome funcional: **Custom Object** ou **Objeto Personalizado**) é um metadata type do Salesforce que define um objeto de dados customizado. Ele representa uma tabela de negócio com seus próprios campos, record types, layouts, regras de validação, list views, relacionamentos e configurações de segurança. Todo objeto customizado possui automaticamente um nome (`Name`), um ID e acesso por meio de uma API Name terminada em `__c`.

Na prática, um `CustomObject`:
- é o container pai de todos os `CustomField` do objeto;
- pode conter filhos como `ValidationRule`, `RecordType`, `WebLink`, `ListView`, `CompactLayout`, `SharingReason`, `BusinessProcess`;
- é referenciado por Flows, Apex, Reports, Dashboards, Approval Processes, Permission Sets, Profiles e integrações externas;
- deve ser documentado **sempre em conjunto com seus campos** (`CustomField`), pois a modelagem de dados só faz sentido quando objeto e atributos são analisados juntos.

> **Importante**: `CustomObject` e `CustomField` formam um par indissociável de documentação. Sempre que documentar um objeto, documente também seus campos principais, e vice-versa. Veja `prompt-custom-field.md`.

### 1.2 Para que serve
- Modelar entidades de negócio que não existem nos objetos padrão.
- Criar relacionamentos com objetos standard e outros custom objects.
- Agrupar dados, regras e automações de um domínio específico.
- Oferecer base para relatórios, dashboards e experiências customizadas.

### 1.3 Cenários típicos de uso
- Objeto `Project__c` para gestão de projetos.
- Objeto `Invoice__c` relacionado a `Opportunity`.
- Objeto `SurveyResponse__c` para respostas de pesquisa.
- Objetos de configuração com `CustomSetting` ou `CustomMetadata`.

### 1.4 Clouds / contextos
- **Salesforce Core** — todos os objetos customizados.
- **Sales Cloud** — extensões de Account, Contact, Opportunity, Quote.
- **Service Cloud** — extensões de Case, Asset, Contact, WorkOrder.
- **Experience Cloud** — objetos expostos em comunidades.
- **Industries** — objetos de domínio específico.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `CustomObject`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Object / Objeto |
| Metadata type exact | `CustomObject` |
| Pasta no projeto SFDX | `objects/<apiName>/` |
| Arquivo padrão | `<apiName>.object-meta.xml` |
| Objeto interno (API padrão) | `EntityDefinition` |
| Objeto interno (Tooling API) | `CustomObject` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | `EntityDefinition` |
| Acessível por Tooling API | Sim — `Metadata` |
| Acessível por Apex | `Schema.getGlobalDescribe()` |
| Acessível por UI | Sim — **Setup → Object Manager** |

### 2.2 Componentes filhos e relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Custom Field | `CustomField` | Atributos do objeto. **Documentar junto**. |
| Record Type | `RecordType` | Variações de registro. |
| Validation Rule | `ValidationRule` | Regras de integridade. |
| Page Layout | `Layout` | Disposição de campos. |
| Compact Layout | `CompactLayout` | Layout resumido. |
| List View | `ListView` | Visualizações de lista. |
| Web Link | `WebLink` | Links customizados. |
| Business Process | `BusinessProcess` | Processos de vendas/suporte. |
| Sharing Reason | `SharingReason` | Motivos de sharing. |
| Validation Rule | `ValidationRule` | Regras de validação. |
| Apex Trigger | `ApexTrigger` | Automação programática. |
| Flow / Process Builder | `Flow` | Automação declarativa. |
| Permission Set / Profile | `PermissionSet`, `Profile` | Acesso ao objeto. |
| Report Type | `ReportType` | Estrutura de relatórios. |

### 2.3 Matriz de acessibilidade

| Fonte | CustomObject metadata | EntityDefinition SOQL | Tooling | Setup/UI |
|---|---|---|---|---|
| API Name | Sim | `QualifiedApiName` | Sim | Sim |
| Label | Sim | `MasterLabel` | Sim | Sim |
| Plural Label | Sim | `DeveloperName` / `Label` | Sim | Sim |
| Nome campo padrão | Sim | `Name` | Sim | Sim |
| Permissões de objeto | via PermSet/Profile | `ObjectPermissions` | Sim | Setup |
| Campos | arquivos separados | `FieldDefinition` | `CustomField` | Setup |
| Record Types | arquivos separados | `RecordType` | Sim | Setup |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`CustomObject`)

Arquivo típico: `objects/<API_Name>/<API_Name>.object-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<fullName>` | 1 | API Name do objeto. |
| `<label>` | 1 | Label singular. |
| `<pluralLabel>` | 1 | Label plural. |
| `<nameField>` | 1 | Configuração do campo Nome (Label, Tipo). |
| `<deploymentStatus>` | 1 | `Deployed` ou `InDevelopment`. |
| `<enableActivities>` | 0..1 | Tasks/Events habilitados. |
| `<enableHistory>` | 0..1 | Histórico de campos. |
| `<enableReports>` | 0..1 | Disponível em relatórios. |
| `<enableSearch>` | 0..1 | Disponível em pesquisa global. |
| `<sharingModel>` | 0..1 | Private, Read, ReadWrite etc. |
| `<enableFeeds>` | 0..1 | Chatter feeds. |
| `<compactLayoutAssignment>` | 0..1 | Compact layout padrão. |
| `<searchLayouts>` | 0..1 | Configuração de list views/pesquisa. |

#### Exemplo mínimo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <deploymentStatus>Deployed</deploymentStatus>
    <label>Projeto</label>
    <pluralLabel>Projetos</pluralLabel>
    <nameField>
        <label>Nome do Projeto</label>
        <type>Text</type>
    </nameField>
    <sharingModel>ReadWrite</sharingModel>
    <enableActivities>true</enableActivities>
    <enableHistory>true</enableHistory>
    <enableReports>true</enableReports>
    <enableSearch>true</enableSearch>
</CustomObject>
```

### 3.2 Objetos internos via API padrão

#### `EntityDefinition`

| Campo | Significado prático |
|---|---|
| `QualifiedApiName` | API Name completo. |
| `MasterLabel` | Label. |
| `DeveloperName` | Nome API (sem namespace/sufixo). |
| `PluralLabel` | Label plural. |
| `IsCustomizable` | Pode ser customizado. |
| `IsCustomSetting` | É um Custom Setting. |
| `KeyPrefix` | Prefixo de 3 caracteres dos IDs. |
| `PublisherId` | Namespace publisher. |

```sql
SELECT QualifiedApiName, MasterLabel, PluralLabel, KeyPrefix,
       IsCustomizable, IsCustomSetting, PublisherId
FROM EntityDefinition
WHERE IsCustomizable = true
ORDER BY MasterLabel
```

#### `ObjectPermissions`

```sql
SELECT Id, ParentId, Parent.Name, SObjectType,
       PermissionsCreate, PermissionsRead, PermissionsEdit,
       PermissionsDelete, PermissionsViewAllRecords, PermissionsModifyAllRecords
FROM ObjectPermissions
WHERE SObjectType = 'Project__c'
ORDER BY Parent.Name
```

### 3.3 Tooling API

```sql
SELECT Id, DeveloperName, NamespacePrefix, MasterLabel, PluralLabel, Metadata
FROM CustomObject
ORDER BY DeveloperName
```

### 3.4 Campos, record types e outros filhos

```sql
SELECT DeveloperName, Label, DataType
FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = 'Project__c'
ORDER BY DeveloperName
```

```sql
SELECT Id, Name, DeveloperName, IsActive
FROM RecordType
WHERE SObjectType = 'Project__c'
ORDER BY Name
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Object Manager.
- Schema Builder.
- `SetupAuditTrail`.
- Relatórios e dashboards que referenciam o objeto.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Registros de dados | Tabela do objeto (SOQL) | `EntityDefinition` | Dados vs metadados. |
| Detalhes de FLS | `ObjectPermissions`, `FieldPermissions` | `EntityDefinition` | Requer queries específicas. |
| Uso em Apex | Código fonte | Metadata do objeto | Requer search. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `CustomField`

- Atributos do objeto. **Devem ser documentados conjuntamente.**

### 4.2 `RecordType`

- Variações de página e picklist por tipo de registro.

### 4.3 `ValidationRule`

- Regras de integridade do objeto.

### 4.4 `Layout` / `CompactLayout`

- Interface de criação/edição/visualização.

### 4.5 `ApexTrigger`, `Flow`

- Automações vinculadas ao objeto.

### 4.6 `PermissionSet` / `Profile`

- Acesso CRUD e FLS.

---

## 5. Consultas e formas de extração

### 5.1 Objetos customizados

```sql
SELECT QualifiedApiName, MasterLabel, PluralLabel, KeyPrefix,
       IsCustomSetting, PublisherId
FROM EntityDefinition
WHERE IsCustomizable = true
  AND PublisherId = null
ORDER BY MasterLabel
```

### 5.2 Objetos com detalhes de permissão

```sql
SELECT Id, Parent.Name, SObjectType,
       PermissionsRead, PermissionsCreate, PermissionsEdit,
       PermissionsDelete, PermissionsViewAllRecords, PermissionsModifyAllRecords
FROM ObjectPermissions
WHERE SObjectType = 'Project__c'
ORDER BY Parent.Name
```

### 5.3 Campos de um objeto

```sql
SELECT DeveloperName, Label, DataType, IsRequired, IsCalculated
FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = 'Project__c'
ORDER BY DeveloperName
```

### 5.4 Layouts de um objeto

```sql
SELECT Id, Name, EntityDefinitionId, EntityDefinition.QualifiedApiName
FROM Layout
WHERE EntityDefinition.QualifiedApiName = 'Project__c'
ORDER BY Name
```

---

## 6. Boas práticas e pontos de atenção

- **Documente objeto e campos sempre juntos**.
- **Use nomes claros e padronizados**: API Name terminado em `__c`, labels sem ambiguidade.
- **Defina plural e singular corretamente**.
- **Escolha o sharing model adequado** à segurança do negócio.
- **Habilite apenas o necessário**: history, reports, feeds, activities.
- **Padronize record types** e layouts por tipo de usuário.
- **Valide dependências** antes de excluir objetos (Apex, Flow, Reports).
- **Evite objetos fantasmas**: remova objetos de desenvolvimento não implantados.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Mantenha um dicionário de dados** atualizado com descrições de cada campo.

---

## 7. Links de referência oficial

- [Salesforce Help — Custom Objects](https://help.salesforce.com/s/articleView?id=sf.dev_objectdefine.htm)
- [Salesforce Developer — CustomObject Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_customobject.htm)
- [Salesforce Developer — EntityDefinition Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_entitydefinition.htm)
- [Salesforce Developer — ObjectPermissions Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_objectpermissions.htm)
