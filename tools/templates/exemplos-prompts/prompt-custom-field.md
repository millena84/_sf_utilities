# Prompt — CustomField

## 1. Contexto do componente

### 1.1 O que é
`CustomField` (nome funcional: **Custom Field** ou **Campo Personalizado**) é um metadata type do Salesforce que representa um campo adicionado a um objeto — seja custom object (`__c`), standard object, external object, big object ou configuração. Ele define o tipo de dados, regras de validação, segurança em nível de campo (FLS), valores padrão, fórmulas, relacionamentos e outros comportamentos de um atributo do objeto.

Na prática, um `CustomField`:
- sempre pertence a um `CustomObject`, `ObjectName__c` ou objeto padrão;
- é definido no XML do objeto (`<fields>`) ou como arquivo separado SFDX (`objects/Objeto__c/fields/Campo__c.field-meta.xml`);
- impacta diretamente Page Layouts, Compact Layouts, Record Types, Validation Rules, Reports, Flows, Apex e integrações;
- é um dos metadados mais críticos para governança de dados e segurança (FLS).

> **Importante**: `CustomField` e `CustomObject` devem ser documentados juntos, pois um campo só existe no contexto de um objeto. Veja também `prompt-custom-object.md`.

### 1.2 Para que serve
- Armazenar dados específicos do negócio.
- Estabelecer relacionamentos entre objetos (Lookup, Master-Detail).
- Automatizar valores via fórmulas, valores padrão e roll-up summaries.
- Controlar visibilidade e permissão via Field-Level Security.
- Apoiar relatórios, dashboards, list views e automações.

### 1.3 Cenários típicos de uso
- Adicionar campos de negócio a leads, contas, oportunidades, cases.
- Criar lookups para relacionar objetos customizados.
- Campos calculados e agregações.
- Campos obrigatórios e regras de preenchimento.

### 1.4 Clouds / contextos
- **Salesforce Core** — todos os objetos e campos.
- **Sales Cloud** — Lead, Account, Contact, Opportunity, Quote.
- **Service Cloud** — Case, Contact, Asset, WorkOrder.
- **Experience Cloud** — campos expostos em telas de comunidade.
- **Industries** — extensões de objetos específicos.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `CustomField`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Field / Campo |
| Metadata type exact | `CustomField` |
| Pasta no projeto SFDX | `objects/<ObjectName>/fields/` |
| Arquivo padrão | `<apiName>.field-meta.xml` |
| Objeto interno (API padrão) | Não consultável como objeto próprio; use Tooling ou `FieldDefinition` |
| Objeto interno (Tooling API) | `CustomField` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | `FieldDefinition`, `EntityParticle` (somente leitura) |
| Acessível por Tooling API | Sim — `Metadata` |
| Acessível por Apex | `DescribeSObjectResult.fields.getMap()` |
| Acessível por UI | Sim — **Setup → Object Manager → [Objeto] → Fields & Relationships** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Custom Object | `CustomObject` | Objeto ao qual o campo pertence. |
| Field Level Security | `FieldPermissions` | Quem pode ler/editar o campo. |
| Permission Set / Profile | `PermissionSet`, `Profile` | Portadores do FLS. |
| Page Layout | `Layout` | Onde o campo aparece. |
| Compact Layout | `CompactLayout` | Destaque do campo. |
| Record Type | `RecordType` | Disponibilidade do campo/valor. |
| Validation Rule | `ValidationRule` | Regras que envolvem o campo. |
| Workflow / Flow | `Flow`, `WorkflowFieldUpdate` | Automations que usam o campo. |
| Apex | `ApexClass`, `ApexTrigger` | Código que referencia/altera o campo. |
| Report / Dashboard | `Report`, `Dashboard` | Onde o campo é usado. |
| Email Template | `EmailTemplate` | Merge fields. |
| Approval Process | `ApprovalProcess` | Campos apresentados/atualizados. |

### 2.3 Matriz de acessibilidade

| Fonte | CustomField metadata | FieldDefinition SOQL | Tooling | Setup/UI |
|---|---|---|---|---|
| API Name | Sim | `DeveloperName` | Sim | Sim |
| Label | Sim | `Label` | Sim | Sim |
| Tipo | Sim | `DataType` | Sim | Sim |
| Obrigatoriedade | Sim | `IsRequired`, `IsNillable` | Sim | Sim |
| Default value | Sim | — | Sim | Sim |
| Fórmula | Sim | `IsCalculated` | Sim | Sim |
| Relacionamento | Sim | `ReferenceTo` | Sim | Sim |
| Segurança (FLS) | via Profile/PermSet | `FieldPermissions` | `FieldPermissions` | Setup |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`CustomField`)

Arquivo típico: `objects/<Objeto>/fields/<API_Name>.field-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<fullName>` | 1 | API Name do campo. |
| `<label>` | 1 | Label. |
| `<type>` | 1 | Tipo de dados (Text, Number, Date, Lookup etc.). |
| `<required>` | 0..1 | Obrigatoriedade. |
| `<unique>` | 0..1 | Unicidade. |
| `<externalId>` | 0..1 | Chave externa. |
| `<trackHistory>` / `<trackTrending>` | 0..1 | Histórico de alterações / trending. |
| `<defaultValue>` | 0..1 | Valor padrão (literal, fórmula, `BLANKVALUE` etc.). |
| `<formula>` | 0..1 | Fórmula do campo. |
| `<formulaTreatBlanksAs>` | 0..1 | `BlankAsBlank` ou `BlankAsZero`. |
| `<precision>` / `<scale>` | 0..1 | Para Number/Currency/Percent. |
| `<length>` | 0..1 | Para Text/Long Text Area. |
| `<referenceTo>` | 0..1 | Objeto relacionado (Lookup/MasterDetail). |
| `<relationshipLabel>` | 0..1 | Label da lista relacionada. |
| `<relationshipName>` | 0..1 | API name da lista relacionada. |
| `<lookupFilter>` | 0..1 | Filtro de lookup. |
| `<valueSet>` | 0..1 | Picklist values. |
| `<encrypted>` | 0..1 | Criptografia unificada. |

#### Tipos de campo comuns

| Tipo | Significado |
|---|---|
| `AutoNumber` | Sequência automática. |
| `Text`, `TextArea`, `LongTextArea` | Texto. |
| `Number`, `Currency`, `Percent` | Numérico. |
| `Date`, `DateTime`, `Time` | Tempo. |
| `Checkbox` | Booleano. |
| `Picklist`, `MultiselectPicklist` | Lista de valores. |
| `Lookup`, `MasterDetail` | Relacionamentos. |
| `Formula` | Campo calculado. |
| `RollupSummary` | Agregação em Master-Detail. |
| `EncryptedText` | Texto criptografado. |
| `Url`, `Email`, `Phone` | Formatados. |
| `Geolocation` | Localização. |

### 3.2 Objetos internos via API padrão

#### `FieldDefinition`

| Campo | Significado prático |
|---|---|
| `DeveloperName` | API Name. |
| `Label` | Label. |
| `DataType` | Tipo. |
| `EntityDefinitionId` | Objeto ao qual pertence. |
| `IsRequired` | Obrigatório no schema. |
| `IsNillable` | Pode ser nulo. |
| `IsCalculated` | Campo fórmula. |
| `IsCustom` | Campo customizado. |
| `ReferenceTo` | Objeto de referência. |
| `Length` | Comprimento. |
| `Precision`, `Scale` | Precisão numérica. |

```sql
SELECT DeveloperName, Label, DataType, EntityDefinition.QualifiedApiName,
       IsRequired, IsNillable, IsCalculated, IsCustom, ReferenceTo
FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = 'Account'
ORDER BY DeveloperName
```

#### `FieldPermissions`

```sql
SELECT Id, ParentId, Parent.Name, Field, PermissionsRead, PermissionsEdit
FROM FieldPermissions
WHERE Field = 'Account.SLA__c'
  AND (PermissionsRead = true OR PermissionsEdit = true)
ORDER BY Parent.Name
```

### 3.3 Tooling API

```sql
SELECT Id, DeveloperName, NamespacePrefix, TableEnumOrId, Metadata
FROM CustomField
WHERE TableEnumOrId = 'Account'
ORDER BY DeveloperName
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Object Manager → Objeto → Fields & Relationships.
- Page Layouts onde o campo está incluído.
- Field Accessibility / FLS.
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Valor dos registros | Objeto de dados (SOQL) | Metadata do campo | Dados vs definição. |
| FLS específica | Profile/PermSet | `FieldDefinition` | Requer `FieldPermissions`. |
| Uso em relatórios | Metadata de reports | `CustomField` | Requer análise de reports. |
| Uso em Apex | Código fonte | `CustomField` | Requer lexical search. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `CustomObject`

- Objeto pai. Sem ele, o campo não existe. Deve ser documentado junto.

### 4.2 `FieldPermissions`

- Define quem pode ler/editar o campo.

### 4.3 `LayoutItem` / `Layout`

- Define onde o campo aparece nas páginas.

### 4.4 `ValidationRule`

- Pode obrigar, limitar ou validar o campo.

### 4.5 `Flow`, `Workflow`, `Apex`

- Consumidores/produtores de valores do campo.

---

## 5. Consultas e formas de extração

### 5.1 Campos de um objeto

```sql
SELECT DeveloperName, Label, DataType, IsRequired, IsNillable,
       IsCalculated, ReferenceTo, Length, Precision, Scale
FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = 'Account'
ORDER BY DeveloperName
```

### 5.2 Campos customizados sem FLS

```sql
SELECT DeveloperName, Label
FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = 'Account'
  AND IsCustom = true
  AND DeveloperName NOT IN (
      SELECT SUBSTRING(Field, CHARINDEX('.', Field)+1, LEN(Field))
      FROM FieldPermissions
      WHERE Field LIKE 'Account.%'
  )
ORDER BY DeveloperName
```

> **Nota**: a query acima é pseudo-SQL — dependendo da API, substring pode não ser suportada. Prefira filtrar `FieldPermissions` e cruzar externamente.

### 5.3 Fórmulas de um objeto

```sql
SELECT DeveloperName, Label, DataType
FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = 'Opportunity'
  AND IsCalculated = true
ORDER BY DeveloperName
```

### 5.4 Campos de relacionamento

```sql
SELECT DeveloperName, Label, DataType, ReferenceTo
FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = 'Opportunity'
  AND (DataType = 'Reference' OR DataType LIKE '%Lookup%')
ORDER BY DeveloperName
```

---

## 6. Boas práticas e pontos de atenção

- **Documente sempre junto com o objeto pai** (`CustomObject`).
- **Padronize API Names** (camelCase ou PascalCase, sem acentos, sufixo `__c`).
- **Evite criar campos obsoleto**; remova com planejamento de migração.
- **Valide impacto em FLS** antes de tornar um campo obrigatório.
- **Cuidado com altering field type**: pode causar perda de dados.
- **Use Validation Rules** para regras de negócio declarativas.
- **Monitore campos não utilizados** via Field Usage analytics.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Não exponha campos criptografados/sensíveis** sem necessidade em relatórios/integrações.
- **Utilize descrição/help text** para facilitar adoção.

---

## 7. Links de referência oficial

- [Salesforce Help — Custom Fields](https://help.salesforce.com/s/articleView?id=sf.adding_fields.htm)
- [Salesforce Developer — CustomField Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_customfield.htm)
- [Salesforce Developer — FieldDefinition Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_fielddefinition.htm)
- [Salesforce Developer — FieldPermissions Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_fieldpermissions.htm)
