# Prompt — AssignmentRules

## 1. Contexto do componente

### 1.1 O que é
`AssignmentRules` (nome funcional: **Assignment Rules** ou **Regras de Atribuição**) é um metadata type do Salesforce que define critérios automatizados para atribuir registros de objetos específicos — principalmente `Lead` e `Case` — a usuários ou filas com base em condições configuradas. Uma regra pode conter múltiplas entradas ordenadas; a primeira entrada cujos critérios forem atendidos define o novo proprietário (owner).

Na prática, `AssignmentRules`:
- é composto por um arquivo de regras por objeto (`assignmentRules/Case.assignmentRules-meta.xml`, `assignmentRules/Lead.assignmentRules-meta.xml`);
- contém entradas (`assignmentRule`) com fórmulas booleanas e ações de atribuição;
- pode ser executado automaticamente na criação do registro ou invocado via API (`AssignmentRuleHeader`);
- é fundamental para Sales Cloud (distribuição de leads) e Service Cloud (roteamento de cases para filas).

### 1.2 Para que serve
- Distribuir leads automaticamente por território, origem, score ou capacidade.
- Encaminhar cases para filas de suporte por produto, prioridade ou canal.
- Reduzir triagem manual por supervisores ou agentes.
- Garantir SLA e roteamento inteligente.

### 1.3 Cenários típicos de uso
- Leads do site atribuídos a fila de SDRs B2B.
- Cases com prioridade Alta roteados para fila de Nível 2.
- Leads de parceiros atribuídos a gerente de canal específico.
- Cases por email de faturamento redirecionados para fila financeira.

### 1.4 Clouds / contextos
- **Sales Cloud** — Lead assignment rules.
- **Service Cloud** — Case assignment rules.
- **Salesforce Core** — mecanismo de atribuição automática.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `AssignmentRules`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Assignment Rules / Regras de Atribuição |
| Metadata type exact | `AssignmentRules` |
| Pasta no projeto SFDX | `assignmentRules/` |
| Arquivo padrão | `<ObjectName>.assignmentRules-meta.xml` |
| Objeto interno (API padrão) | `AssignmentRule` (Tooling) |
| Objeto interno (Tooling API) | `AssignmentRule` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Não diretamente |
| Acessível por Tooling API | Sim — `Metadata` |
| Acessível por Apex | Sim — invocação via `Database.DMLOptions` com `assignmentRuleHeader` |
| Acessível por UI | Sim — **Setup → Assignment Rules (Lead ou Case)** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Lead | `Lead` | Objeto para leads. |
| Case | `Case` | Objeto para cases. |
| Queue | `Queue` | Filas de destino. |
| User | `User` | Usuários de destino. |
| Workflow / Flow | `WorkflowRule`, `Flow` | Automations complementares. |
| Omni-Channel / Routing | Service Cloud routing | Roteamento avançado de cases. |

### 2.3 Matriz de acessibilidade

| Fonte | AssignmentRules metadata | Tooling | Apex | Setup/UI |
|---|---|---|---|---|
| Nome da regra | `<assignmentRule>` | `Name` | — | Sim |
| Ativo | `<active>` | `Active` | — | Sim |
| Critérios | `<criteriaItems>` | `Metadata` | — | Sim |
| Owner destino | `<assignedToType>`, `<assignedTo>` | `Metadata` | — | Sim |
| Email template | `<template>` | `Metadata` | — | Sim |
| Execução via API | — | — | `assignmentRuleHeader.assignmentRuleId` | — |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`AssignmentRules`)

Arquivo típico: `assignmentRules/Case.assignmentRules-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<assignmentRules>` | 1 | Raiz. |
| `<assignmentRule>` | 0..N | Regra individual. |
| `<fullName>` | 1 | Nome da regra. |
| `<active>` | 1 | Ativa/inativa. |
| `<ruleEntry>` | 0..N | Entrada de regra (ordem importa). |
| `<criteriaItems>` | 0..N | Condição de filtro. |
| `<field>` | 1 | Campo do critério. |
| `<operation>` | 1 | Operador (`equals`, `contains`, `greaterThan` etc.). |
| `<value>` | 0..1 | Valor do critério. |
| `<assignedToType>` | 1 | `User` ou `Queue`. |
| `<assignedTo>` | 1 | API Name do destino. |
| `<template>` | 0..1 | Email template de notificação. |
| `<notifyCcRecipients>` | 0..1 | Notificar cópias de email. |

### 3.2 Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AssignmentRules xmlns="http://soap.sforce.com/2006/04/metadata">
    <assignmentRule>
        <fullName>Regra_Case_Suporte</fullName>
        <active>true</active>
        <ruleEntry>
            <criteriaItems>
                <field>Case.Origin</field>
                <operation>equals</operation>
                <value>Email</value>
            </criteriaItems>
            <criteriaItems>
                <field>Case.Priority</field>
                <operation>equals</operation>
                <value>High</value>
            </criteriaItems>
            <assignedToType>Queue</assignedToType>
            <assignedTo>Fila_Nivel_2</assignedTo>
        </ruleEntry>
    </assignmentRule>
</AssignmentRules>
```

### 3.3 Tooling API

```sql
SELECT Id, Name, Active, EntityDefinition.QualifiedApiName, Metadata
FROM AssignmentRule
ORDER BY EntityDefinition.QualifiedApiName, Name
```

### 3.4 Execução via Apex

```java
Database.DMLOptions dmo = new Database.DMLOptions();
dmo.assignmentRuleHeader.assignmentRuleId = [SELECT Id FROM AssignmentRule
    WHERE SobjectType = 'Case' AND Active = true LIMIT 1].Id;
Case c = new Case(Subject='Teste');
c.setOptions(dmo);
insert c;
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Assignment Rules (Lead ou Case).
- SetupAuditTrail.
- Logs de atribuição em debug logs.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Critérios e ações | XML metadata / Tooling `Metadata` | SOQL padrão | Requer Tooling. |
| Regras inativas | metadata | Setup | Apenas ativas executam automaticamente. |
| Histórico de atribuição | `CaseHistory` / `LeadHistory` | `AssignmentRule` | Dados operacionais. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `Lead` / `Case`

- Objetos suportados por assignment rules.

### 4.2 `Queue` / `User`

- Destinos de atribuição.

### 4.3 `EmailTemplate`

- Templates de notificação do owner.

### 4.4 `CaseHistory` / `LeadHistory`

- Histórico de mudanças de owner.

---

## 5. Consultas e formas de extração

### 5.1 Regras de atribuição por objeto

```sql
SELECT Id, Name, Active, EntityDefinition.QualifiedApiName
FROM AssignmentRule
ORDER BY EntityDefinition.QualifiedApiName, Name
```

### 5.2 Filas de destino

```sql
SELECT Id, Name, DeveloperName, Type
FROM QueueSObject
WHERE SObjectType = 'Case'
ORDER BY Name
```

### 5.3 Cases por fila

```sql
SELECT OwnerId, Owner.Name, COUNT(Id)
FROM Case
WHERE Owner.Type = 'Queue'
GROUP BY OwnerId, Owner.Name
ORDER BY COUNT(Id) DESC
```

### 5.4 Leads por fila

```sql
SELECT OwnerId, Owner.Name, COUNT(Id)
FROM Lead
WHERE Owner.Type = 'Queue'
GROUP BY OwnerId, Owner.Name
ORDER BY COUNT(Id) DESC
```

---

## 6. Boas práticas e pontos de atenção

- **Ordene as entradas da mais específica para a mais genérica**.
- **Documente o critério de cada regra** para evitar sobreposição.
- **Valide existência de filas/usuários destino** no metadata.
- **Cuidado com regras inativas** que ficam no metadata sem uso.
- **Use DMLOptions quando invocar regras via Apex/API**.
- **Monitore distribuição desigual** de leads/cases entre usuários/filas.
- **Considere Omni-Channel** para roteamento sofisticado de cases.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Teste regras em sandbox** com volumes representativos.

---

## 7. Links de referência oficial

- [Salesforce Help — Set Up Assignment Rules](https://help.salesforce.com/s/articleView?id=sf.customize_leadrouting.htm)
- [Salesforce Developer — AssignmentRules Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_assignmentrules.htm)
- [Apex Developer Guide — AssignmentRuleHeader](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_methods_system_database_dmloptions.htm)
