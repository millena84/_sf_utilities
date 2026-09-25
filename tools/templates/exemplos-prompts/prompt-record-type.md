# Prompt — RecordType

## 1. Contexto do componente

### 1.1 O que é
`RecordType` (nome funcional: **Record Type** ou **Tipo de Registro**) é um metadata type do Salesforce que permite definir variações de um mesmo objeto, cada uma com seus próprios Page Layouts, valores de picklist e Business Process (quando aplicável). Record Types possibilitam experiências diferenciadas para perfis diferentes sem a necessidade de criar objetos separados.

Na prática, um `RecordType`:
- pertence a um objeto (`CustomObject` ou objeto standard);
- controla quais valores de picklist estão disponíveis;
- define o layout de página padrão por perfil;
- é visível em campos como `RecordTypeId` e `RecordType.Name`;
- pode ser atribuído automaticamente ou manualmente pelo usuário, conforme regras de perfil/owner.

### 1.2 Para que serve
- Oferecer diferentes layouts e picklists por tipo de registro.
- Segmentar processos de negócio dentro do mesmo objeto.
- Simplificar a experiência do usuário por perfil.
- Suportar diferentes pipelines de vendas, tipos de caso etc.

### 1.3 Cenários típicos de uso
- Tipos de oportunidade: Novo Negócio, Renovação, Serviço.
- Tipos de caso: Dúvida, Reclamação, Solicitação.
- Tipos de lead: B2B, B2C, Parceiro.
- Tipos de conta: Cliente, Prospect, Parceiro.

### 1.4 Clouds / contextos
- **Salesforce Core** — todos os objetos customizáveis.
- **Sales Cloud** — Opportunity, Lead, Account.
- **Service Cloud** — Case.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `RecordType`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Record Type / Tipo de Registro |
| Metadata type exact | `RecordType` |
| Pasta no projeto SFDX | `objects/<ObjectName>/recordTypes/` |
| Arquivo padrão | `<apiName>.recordType-meta.xml` |
| Objeto interno (API padrão) | `RecordType` |
| Objeto interno (Tooling API) | `RecordType` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM RecordType` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `RecordType` é consultável |
| Acessível por UI | Sim — **Setup → Object Manager → [Objeto] → Record Types** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Objeto | `CustomObject` / `EntityDefinition` | Objeto ao qual o record type pertence. |
| Page Layout | `Layout` | Layout associado por perfil. |
| Picklist Values | `PicklistValue`, `ValueSet` | Valores disponíveis por record type. |
| Business Process | `BusinessProcess` | Processo associado (em objetos que usam). |
| Profile / Permission Set | `Profile`, `PermissionSet` | Acesso ao record type. |
| Apex / Flow | `ApexClass`, `Flow` | Lógica que atribui/consome record type. |
| Workflow / Approval | `WorkflowRule`, `ApprovalProcess` | Podem ser filtrados por record type. |

### 2.3 Matriz de acessibilidade

| Fonte | RecordType metadata | Objeto SOQL | Tooling | Setup/UI |
|---|---|---|---|---|
| Name / DeveloperName | Sim | `Name`, `DeveloperName` | Sim | Sim |
| Objeto | Sim | `SObjectType` | Sim | Sim |
| Ativo | Sim | `IsActive` | Sim | Sim |
| Layout por perfil | `<layoutAssignments>` | `RecordTypeId` em associação | — | Setup |
| Picklist values | `<picklistValues>` | `RecordType.PicklistValues` via API | — | Setup |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`RecordType`)

Arquivo típico: `objects/<Objeto>/recordTypes/<API_Name>.recordType-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<fullName>` | 1 | API Name. |
| `<label>` | 1 | Label. |
| `<active>` | 1 | Ativo/inativo. |
| `<businessProcess>` | 0..1 | Business process associado. |
| `<description>` | 0..1 | Descrição. |
| `<picklistValues>` | 0..N | Valores disponíveis por picklist. |
| `<values>` | 0..N | Valor disponível dentro de um picklist. |
| `<default>` | 0..1 | Valor padrão do picklist. |
| `<layoutAssignments>` | via metadata do objeto/perfil | Layout por perfil. |

#### Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<RecordType xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>TipoB2B</fullName>
    <label>B2B</label>
    <active>true</active>
    <description>Registros de clientes corporativos</description>
    <picklistValues>
        <picklist>Status__c</picklist>
        <values>
            <fullName>Aberto</fullName>
            <default>false</default>
        </values>
        <values>
            <fullName>Ganho</fullName>
            <default>false</default>
        </values>
    </picklistValues>
</RecordType>
```

### 3.2 Objeto interno via API padrão: `RecordType`

| Campo | Significado prático |
|---|---|
| `Id` | ID do record type. |
| `Name` | Label. |
| `DeveloperName` | API Name. |
| `SObjectType` | Objeto associado. |
| `IsActive` | Ativo/inativo. |
| `BusinessProcessId` | Processo associado. |
| `NamespacePrefix` | Namespace (se managed). |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, Name, DeveloperName, SObjectType, IsActive, BusinessProcessId
FROM RecordType
WHERE SObjectType = 'Opportunity'
ORDER BY Name
```

### 3.3 Tooling API

```sql
SELECT Id, Name, DeveloperName, SObjectType, IsActive, Metadata
FROM RecordType
WHERE SObjectType = 'Opportunity'
ORDER BY Name
```

### 3.4 Layout assignments

Layout por perfil geralmente é configurado via metadata de `Profile` ou `PermissionSet`:

```sql
SELECT Id, ParentId, Parent.Name, RecordTypeId, RecordType.Name, LayoutId, Layout.Name
FROM ProfileLayout
WHERE RecordTypeId != null
ORDER BY RecordType.Name
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Object Manager → Objeto → Record Types.
- Schema Builder.
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Picklist values por RT | XML metadata / Tooling `Metadata` | `RecordType` SOQL simples | Requer parse do metadata. |
| Layout por perfil | `Profile`/`PermissionSet` metadata | `RecordType` | Requer análise cruzada. |
| Uso efetivo em registros | Campo `RecordTypeId` nos registros | Metadata | Dados operacionais. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `CustomObject`

- Objeto pai do record type.

### 4.2 `BusinessProcess`

- Processo de vendas/suporte associado.

### 4.3 `PicklistValue` / `ValueSet`

- Valores de picklist disponíveis para o record type.

### 4.4 `ProfileLayout`

- Associação entre record type, perfil e layout.

### 4.5 `Apex` / `Flow`

- Código/automações que atribuem record type ou bifurcam lógica por `RecordTypeId`.

---

## 5. Consultas e formas de extração

### 5.1 Record types por objeto

```sql
SELECT Id, Name, DeveloperName, SObjectType, IsActive
FROM RecordType
WHERE SObjectType = 'Opportunity'
ORDER BY Name
```

### 5.2 Record types ativos/inativos

```sql
SELECT SObjectType, COUNT(Id)
FROM RecordType
WHERE IsActive = false
GROUP BY SObjectType
ORDER BY SObjectType
```

### 5.3 Record types sem uso em registros

```sql
SELECT RecordTypeId, COUNT(Id)
FROM Opportunity
GROUP BY RecordTypeId
```

> **Nota**: cruzar com `RecordType` para identificar inativos ou sem registros.

### 5.4 Layout assignments

```sql
SELECT Parent.Name, RecordType.Name, Layout.Name
FROM ProfileLayout
WHERE RecordTypeId != null
ORDER BY Parent.Name, RecordType.Name
```

---

## 6. Boas práticas e pontos de atenção

- **Evite criar record types desnecessários** — eles aumentam a complexidade de manutenção.
- **Use descrições claras** para documentar o propósito de cada record type.
- **Mantenha picklist values coerentes** por record type.
- **Atribua layouts corretamente por perfil** para evitar exposição indevida de campos.
- **Não deixe record types inativos sem motivo** em produção.
- **Padronize processos de atribuição** (default por perfil, Apex, Flow).
- **Monitore registros órfãos** ou atribuídos a record types incorretos.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Documente decisões de modelagem** (por que record type vs. objeto separado).

---

## 7. Links de referência oficial

- [Salesforce Help — Record Types](https://help.salesforce.com/s/articleView?id=sf.customize_recordtype.htm)
- [Salesforce Developer — RecordType Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_recordtype.htm)
- [Salesforce Developer — RecordType Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_recordtype.htm)
