# Prompt — ValidationRule

## 1. Contexto do componente

### 1.1 O que é
`ValidationRule` (nome funcional: **Validation Rule** ou **Regra de Validação**) é um metadata type do Salesforce que define uma fórmula booleana executada quando um registro é criado ou atualizado. Se a fórmula avaliar como `TRUE`, o registro é rejeitado e uma mensagem de erro é exibida ao usuário. É uma das principais ferramentas declarativas para garantir integridade de dados.

Na prática, uma `ValidationRule`:
- pertence a um objeto (`CustomObject` ou objeto standard);
- usa uma fórmula semelhante a fórmulas de campo, com funções e referências a campos;
- pode ser condicionada por perfil, record type ou função por meio de funções como `$Profile`, `$UserRole`, `$RecordType`;
- pode ser acionada por UI, API, Apex, Flow, Data Loader e outras automações.

### 1.2 Para que serve
- Garantir consistência e integridade dos dados.
- Impedir estados inválidos do registro.
- Reduzir dependências de validação feitas em Apex.
- Melhorar a experiência do usuário com mensagens de erro claras.

### 1.3 Cenários típicos de uso
- Obrigar preenchimento de campo quando outro campo tiver determinado valor.
- Impedir data de início posterior à data de fim.
- Validar formato ou intervalo de valores.
- Bloquear alterações de status inválidas.

### 1.4 Clouds / contextos
- **Salesforce Core** — todos os objetos.
- **Sales Cloud** — Lead, Account, Contact, Opportunity, Quote.
- **Service Cloud** — Case.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ValidationRule`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Validation Rule / Regra de Validação |
| Metadata type exact | `ValidationRule` |
| Pasta no projeto SFDX | `objects/<ObjectName>/validationRules/` |
| Arquivo padrão | `<apiName>.validationRule-meta.xml` |
| Objeto interno (API padrão) | `ValidationRule` |
| Objeto interno (Tooling API) | `ValidationRule` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ValidationRule` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `ValidationRule` é consultável |
| Acessível por UI | Sim — **Setup → Object Manager → [Objeto] → Validation Rules** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Objeto | `CustomObject` / `EntityDefinition` | Objeto ao qual a regra pertence. |
| Campos | `CustomField`, `FieldDefinition` | Referências na fórmula. |
| Record Type | `RecordType` | A regra pode filtrar por record type. |
| Profile / Role / User | `Profile`, `UserRole`, `User` | Referências via `$Profile`, `$UserRole`, `$User`. |
| Apex Trigger | `ApexTrigger` | Código que pode disparar a regra; cuidado com mensagens de erro. |
| Flow / Process Builder | `Flow` | Automações que podem ser bloqueadas pela regra. |
| Layout | `Layout` | Onde a mensagem será exibida. |

### 2.3 Matriz de acessibilidade

| Fonte | ValidationRule metadata | Objeto SOQL | Tooling | Setup/UI |
|---|---|---|---|---|
| Name / DeveloperName | Sim | `ValidationName` | Sim | Sim |
| Objeto | Sim | `EntityDefinitionId`, `EntityDefinition.QualifiedApiName` | Sim | Sim |
| Fórmula | Sim | — | `Metadata` | Sim |
| Mensagem de erro | Sim | `ErrorMessage` | Sim | Sim |
| Ativa | Sim | `Active` | Sim | Sim |
| Localização mensagem | Sim | `ErrorLocation` | Sim | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ValidationRule`)

Arquivo típico: `objects/<Objeto>/validationRules/<API_Name>.validationRule-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<fullName>` | 1 | API Name. |
| `<label>` | 1 | Label. |
| `<active>` | 1 | Ativa/inativa. |
| `<errorConditionFormula>` | 1 | Fórmula que, se verdadeira, bloqueia o salvamento. |
| `<errorMessage>` | 1 | Mensagem exibida ao usuário. |
| `<errorLocation>` | 0..1 | Topo da página (`Top`) ou campo específico (`Field`). |
| `<errorDisplayField>` | 0..1 | Campo onde o erro será exibido. |
| `<description>` | 0..1 | Descrição interna. |

#### Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ValidationRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>DataFim_Maior_Que_Inicio</fullName>
    <active>true</active>
    <errorConditionFormula>DataFim__c &lt; DataInicio__c</errorConditionFormula>
    <errorMessage>A data de fim não pode ser anterior à data de início.</errorMessage>
    <errorLocation>top</errorLocation>
</ValidationRule>
```

### 3.2 Objeto interno via API padrão: `ValidationRule`

| Campo | Significado prático |
|---|---|
| `Id` | ID da regra. |
| `ValidationName` | API Name. |
| `EntityDefinitionId` | ID do objeto pai. |
| `Active` | Ativa/inativa. |
| `ErrorMessage` | Mensagem de erro. |
| `ErrorLocation` | Local exibição do erro. |
| `ErrorDisplayField` | Campo de exibição. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, ValidationName, Active, ErrorMessage, ErrorLocation,
       ErrorDisplayField, EntityDefinition.QualifiedApiName
FROM ValidationRule
WHERE EntityDefinition.QualifiedApiName = 'Opportunity'
ORDER BY ValidationName
```

### 3.3 Tooling API

```sql
SELECT Id, ValidationName, Active, Metadata, EntityDefinitionId
FROM ValidationRule
WHERE EntityDefinition.QualifiedApiName = 'Opportunity'
ORDER BY ValidationName
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Object Manager → Objeto → Validation Rules.
- `SetupAuditTrail`.
- Logs de erro em Apex/Flow.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Fórmula | XML metadata / Tooling `Metadata` | `ValidationRule` SOQL | Requer Tooling/metadata. |
| Execuções reais | Debug/erros transacionais | Metadata | Estado de runtime. |
| Impacto em integrações | Código/integrações | Metadata da regra | Requer análise de consumidores. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `CustomObject`

- Objeto ao qual a regra pertence.

### 4.2 `CustomField`

- Campos referenciados na fórmula.

### 4.3 `RecordType`

- Pode ser usado em condições via `$RecordType`.

### 4.4 `ApexTrigger` / `Flow`

- Disparadores que podem falhar pela regra.

### 4.5 `Profile`, `UserRole`, `User`

- Usados em fórmulas condicionais.

---

## 5. Consultas e formas de extração

### 5.1 Regras por objeto

```sql
SELECT Id, ValidationName, Active, ErrorMessage, ErrorLocation, ErrorDisplayField
FROM ValidationRule
WHERE EntityDefinition.QualifiedApiName = 'Opportunity'
ORDER BY ValidationName
```

### 5.2 Regras ativas

```sql
SELECT EntityDefinition.QualifiedApiName, COUNT(Id)
FROM ValidationRule
WHERE Active = true
GROUP BY EntityDefinition.QualifiedApiName
ORDER BY EntityDefinition.QualifiedApiName
```

### 5.3 Regras que referenciam um campo específico

Requer parse do XML metadata / Tooling `Metadata`.

---

## 6. Boas práticas e pontos de atenção

- **Mantenha mensagens de erro claras e orientadoras**.
- **Evite regras excessivamente complexas** — se a lógica crescer demais, avalie Apex.
- **Use `BLANKVALUE` / `ISBLANK`** para tratar campos nulos.
- **Seja cuidadoso com fórmulas baseadas em `$Profile`**, pois dificultam manutenção.
- **Teste validações via API e Data Loader**, não apenas UI.
- **Documente o propósito de cada regra** na descrição.
- **Evite conflitos** entre validation rules, triggers e Flows.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Cuidado com mensagens contendo dados sensíveis**.

---

## 7. Links de referência oficial

- [Salesforce Help — Validation Rules](https://help.salesforce.com/s/articleView?id=sf.fields_about_validation_rules.htm)
- [Salesforce Developer — ValidationRule Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_validationrule.htm)
- [Salesforce Developer — ValidationRule Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_validationrule.htm)
- [Salesforce Help — Formula Operators and Functions](https://help.salesforce.com/s/articleView?id=sf.customize_functions.htm)
