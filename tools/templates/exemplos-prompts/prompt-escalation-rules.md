# Prompt — EscalationRules

## 1. Contexto do componente

### 1.1 O que é
`EscalationRules` (nome funcional: **Escalation Rules** ou **Regras de Escalonamento**) é um metadata type do Salesforce que define critérios para reescalonar automaticamente registros de `Case` quando determinadas condições são atendidas — geralmente baseadas em idade do caso, status, prioridade, origem ou outras características. O escalonamento pode reatribuir o caso, enviar notificações por email e atualizar campos.

Na prática, `EscalationRules`:
- é composto por um arquivo por objeto (`escalationRules/Case.escalationRules-meta.xml`);
- contém uma ou mais regras (`escalationRule`) com entradas (`ruleEntry`) ordenadas;
- age apenas no objeto `Case` ao nível do Salesforce nativo;
- é executado automaticamente em intervalos regulares e na edição de casos;
- é amplamente usado em Service Cloud para garantir SLAs.

### 1.2 Para que serve
- Escalonar cases críticos para gerentes ou filas superiores.
- Enviar alertas quando cases ultrapassam prazos.
- Reatribuir automaticamente cases inativos ou não resolvidos.
- Manter conformidade com SLAs de atendimento.

### 1.3 Cenários típicos de uso
- Case com prioridade Alta aberto há mais de 4 horas → escalar para Nível 2.
- Case sem atividade por mais de 72 horas → notificar supervisor.
- Case de cliente VIP com status Novo por mais de 1 hora → escalar para gerente.
- Case não resolvido após 5 dias úteis → escalar para diretoria.

### 1.4 Clouds / contextos
- **Service Cloud** — principal uso em cases.
- **Salesforce Core** — mecanismo nativo de escalonamento.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `EscalationRules`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Escalation Rules / Regras de Escalonamento |
| Metadata type exact | `EscalationRules` |
| Pasta no projeto SFDX | `escalationRules/` |
| Arquivo padrão | `<ObjectName>.escalationRules-meta.xml` |
| Objeto interno (API padrão) | `EscalationRule` (Tooling) |
| Objeto interno (Tooling API) | `EscalationRule` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Não diretamente |
| Acessível por Tooling API | Sim — `Metadata` |
| Acessível por Apex | Não invocável diretamente |
| Acessível por UI | Sim — **Setup → Escalation Rules** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Case | `Case` | Único objeto suportado. |
| Queue | `Queue` | Fila destino do escalonamento. |
| User | `User` | Usuário destino do escalonamento. |
| Email Template | `EmailTemplate` | Template de notificação. |
| Case Milestone / Entitlement | `CaseMilestone`, `Entitlement` | Referência de SLA. |
| Assignment Rules | `AssignmentRules` | Pode atuar antes/depois do escalonamento. |

### 2.3 Matriz de acessibilidade

| Fonte | EscalationRules metadata | Tooling | Setup/UI |
|---|---|---|---|
| Nome da regra | `<escalationRule>` | `Name` | Sim |
| Ativo | `<active>` | `Active` | Sim |
| Critérios | `<criteriaItems>`, `<formula>` | `Metadata` | Sim |
| Ações de escala | `<escalationAction>` | `Metadata` | Sim |
| Tempo de espera | `<ageOver>` | `Metadata` | Sim |
| Destinatário de notificação | `<notifyTo>` | `Metadata` | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`EscalationRules`)

Arquivo típico: `escalationRules/Case.escalationRules-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<escalationRules>` | 1 | Raiz. |
| `<escalationRule>` | 0..N | Regra individual. |
| `<fullName>` | 1 | Nome da regra. |
| `<active>` | 1 | Ativa/inativa. |
| `<ruleEntry>` | 0..N | Entrada de regra (ordem importa). |
| `<criteriaItems>` | 0..N | Condição de filtro. |
| `<field>`, `<operation>`, `<value>` | — | Critério. |
| `<formula>` | 0..1 | Fórmula booleana avançada. |
| `<businessHours>` | 0..1 | Horário comercial usado no cálculo de idade. |
| `<escalationAction>` | 0..N | Ações de escalonamento. |
| `<assignedTo>` | 0..1 | Usuário/fila destino. |
| `<assignedToTemplate>` | 0..1 | Template para notificação. |
| `<minutesToEscalation>` | 0..1 | Tempo até escalar. |
| `<notifyEmail>` | 0..N | Email adicional notificado. |
| `<notifyTo>` | 0..N | Usuário notificado. |
| `<notifyToTemplate>` | 0..1 | Template enviado ao notificado. |

### 3.2 Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<EscalationRules xmlns="http://soap.sforce.com/2006/04/metadata">
    <escalationRule>
        <fullName>Escalonamento_Caso_Critico</fullName>
        <active>true</active>
        <ruleEntry>
            <criteriaItems>
                <field>Case.Priority</field>
                <operation>equals</operation>
                <value>High</value>
            </criteriaItems>
            <escalationAction>
                <minutesToEscalation>240</minutesToEscalation>
                <assignedTo>Fila_Nivel_2</assignedTo>
                <assignedToType>Queue</assignedToType>
                <notifyTo>gerente.suporte@exemplo.com</notifyTo>
                <notifyToTemplate>Notificacao_Escalonamento</notifyToTemplate>
            </escalationAction>
        </ruleEntry>
    </escalationRule>
</EscalationRules>
```

### 3.3 Tooling API

```sql
SELECT Id, Name, Active, EntityDefinition.QualifiedApiName, Metadata
FROM EscalationRule
ORDER BY EntityDefinition.QualifiedApiName, Name
```

### 3.4 Regras ativas

```sql
SELECT Id, Name, Active, EntityDefinition.QualifiedApiName
FROM EscalationRule
WHERE Active = true
ORDER BY EntityDefinition.QualifiedApiName, Name
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Escalation Rules.
- SetupAuditTrail.
- Case History / Email logs de notificações.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Critérios e ações | XML metadata / Tooling `Metadata` | SOQL padrão | Requer Tooling. |
| Regras inativas | metadata | — | Não executam. |
| Histórico de escalonamento | `CaseHistory` | `EscalationRule` | Dados operacionais. |
| Business Hours aplicado | `<businessHours>` | — | Padrão ou customizado. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `Case`

- Objeto suportado por regras de escalonamento.

### 4.2 `Queue` / `User`

- Destinos de atribuição.

### 4.3 `EmailTemplate`

- Notificações automáticas.

### 4.4 `BusinessHours`

- Define como o tempo de idade é calculado.

### 4.5 `CaseMilestone` / `Entitlement`

- SLAs gerenciados relacionados a cases.

---

## 5. Consultas e formas de extração

### 5.1 Regras de escalonamento

```sql
SELECT Id, Name, Active, EntityDefinition.QualifiedApiName
FROM EscalationRule
ORDER BY EntityDefinition.QualifiedApiName, Name
```

### 5.2 Cases abertos por prioridade e idade

```sql
SELECT Priority, Status, Owner.Type, Owner.Name, CreatedDate, Age_Over__c
FROM Case
WHERE IsClosed = false
ORDER BY Priority, CreatedDate
```

> **Nota**: `Age_Over__c` é campo customizado para exemplo. Use `CreatedDate` em conjunto com `BusinessHours`.

### 5.3 Business Hours

```sql
SELECT Id, Name, IsDefault, IsActive
FROM BusinessHours
ORDER BY Name
```

### 5.4 Templates usados em escalation actions

Via análise de XML no repositório:

```bash
grep -r "<assignedToTemplate>\|<notifyToTemplate>" \
  force-app/main/default/escalationRules/
```

---

## 6. Boas práticas e pontos de atenção

- **Ordene entradas da mais específica para a mais genérica**.
- **Documente os SLAs** que cada regra representa.
- **Valide business hours** usado em cada regra para cálculo correto de idade.
- **Garanta que destinos (filas/usuários) existam** e estejam ativos.
- **Evite notificações excessivas** que causem alert fatigue.
- **Teste escalonamento em sandbox** com simulação de tempo.
- **Monitore cases escalados** periodicamente.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Considere Entitlements + Milestones** para SLAs mais robustos.

---

## 7. Links de referência oficial

- [Salesforce Help — Escalation Rules](https://help.salesforce.com/s/articleView?id=sf.customize_escalation_rules.htm)
- [Salesforce Developer — EscalationRules Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_escalationrules.htm)
