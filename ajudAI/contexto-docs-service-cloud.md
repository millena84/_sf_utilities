Abaixo está o detalhamento completo e evoluído para a **Onda 07: Service Cloud**, contemplando as configurações de **Omni-Channel (ServiceChannel e PresenceConfiguration)**, **Gestão de SLAs e Direitos (EntitlementProcess & Milestones)**, **Base de Conhecimento (KnowledgeArticleVersion / `Knowledge__kav`)** e **Processos de Suporte e Escalamento de Casos (SupportProcess, Assignment & Escalation Rules)**.

Cada modelo inclui o mapeamento de tags XML no repositório SFDX, exemplos de configuração, seções de **Rastreio de Acesso, Segurança e Permissões (Profiles, Permission Sets, Queues, etc.)**, seguidos de seus **JSON Schemas** dedicados para o **Claude Code** ou utilitários de automação.

---

# 📑 Modelo 7.1: Omni-Channel — ServiceChannel & PresenceConfiguration

O **Omni-Channel** é o motor de roteamento e distribuição de trabalho em tempo real do Service Cloud, direcionando chamados, mensagens e tarefas aos atendentes com base em capacidade, habilidades e presença.

### Convenção de Nomes e Estrutura SFDX
* **Service Channel:** `force-app/main/default/serviceChannels/[Channel_Name].serviceChannel-meta.xml`
* **Presence Configuration:** `force-app/main/default/presenceConfigurations/[Config_Name].presenceConfiguration-meta.xml`
* **Presence User Status:** `force-app/main/default/servicePresenceStatus/[Status_Name].servicePresenceStatus-meta.xml`

---

## 1. Service Channel (`ServiceChannel`)

O **Service Channel** transforma um objeto do Salesforce (padrão ou customizado) em uma fonte de trabalho roteável pelo Omni-Channel.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ServiceChannel xmlns="http://soap.sforce.com/2006/04/metadata">
    <developerName>Case_Service_Channel</developerName>
    <masterLabel>Canal de Atendimento de Casos</masterLabel>
    <relatedObject>Case</relatedObject>
    <capacityModel>StatusModel</capacityModel>
    <hasCapacityFromAutoAcquiredServices>false</hasCapacityFromAutoAcquiredServices>
</ServiceChannel>
```

| Propriedade | Valor Exemplo | Tag XML | Descrição / Comportamento de Plataforma |
|---|---|---|---|
| **DeveloperName / ApiName** | `Case_Service_Channel` | `<developerName>` | Nome API exclusivo do canal no repositório. |
| **MasterLabel** | `Canal de Atendimento de Casos` | `<masterLabel>` | Rótulo exibido no Setup do Omni-Channel. |
| **Related Object** | `Case` \| `MessagingSession` \| `Pedido__c` | `<relatedObject>` | Objeto cujos registros serão distribuídos aos atendentes. |
| **Capacity Model** | `StatusModel` \| `TabClosedModel` | `<capacityModel>` | **`StatusModel`**: Libera a capacidade do agente quando o campo Status atinge um valor "Fechado".<br>**`TabClosedModel`**: Libera a capacidade apenas quando a aba no Console é fechada. |

---

## 2. Presence Configuration (`PresenceConfiguration`)

A **Presence Configuration** define a capacidade total de trabalho do agente, o comportamento do aceite de chamados (automático ou manual) e as regras de tempo limite (*decline timeout*).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PresenceConfiguration xmlns="http://soap.sforce.com/2006/04/metadata">
    <developerName>Suporte_Tier1_Presence_Config</developerName>
    <masterLabel>Configuração de Presença - Tier 1</masterLabel>
    <capacity>5</capacity>
    <enableAutoAccept>false</enableAutoAccept>
    <enableDecline>true</enableDecline>
    <declineTimeout>30</declineTimeout>
    <enableDeclineReason>true</enableDeclineReason>
</PresenceConfiguration>
```

| Propriedade | Valor Exemplo | Tag XML | Descrição Técnica |
|---|---|---|---|
| **Capacity** | `5` (Unidades) | `<capacity>` | Capacidade máxima de unidades de trabalho simultâneas do atendente. |
| **Enable Auto Accept** | `true` \| `false` | `<enableAutoAccept>` | `true`: O trabalho é atribuído e aberto na tela do agente sem necessidade de clicar em "Aceitar". |
| **Enable Decline** | `true` \| `false` | `<enableDecline>` | Permite que o atendente recuse manualmente um trabalho atribuído. |
| **Decline Timeout** | `30` (Segundos) | `<declineTimeout>` | Tempo máximo em segundos para o agente responder antes que o item expire e vá para outro atendente. |

---

## 3. Rastreio de Acesso, Permissões e Atribuição de Usuários

O acesso ao Omni-Channel e às suas configurações depende da atribuição direta de usuários ou perfis:

| Componente | Mecanismo de Atribuição | Tag XML / Fonte | Rastreio em Profiles e Permission Sets |
|---|---|---|---|
| **Presence Configuration** | Atribuição de Usuários/Perfis | `<assignments><profiles>` / `<users>` | Define quais perfis e usuários utilizam esta capacidade específica. |
| **Service Presence Status** | Permissão de Perfil / Permission Set | `<servicePresenceStatusAccesses>` | Libera os status de presença (ex: *Disponível - Caso*, *Ocupado*, *Em Pausa*) em Profiles/Permission Sets. |
| **Omni-Channel Supervisor** | User Permission | `OmniChannelSupervisor` | Permite que supervisores monitorem filas, capacidade e escutem atendimentos em tempo real. |

---

# 🤖 JSON Schema: 7.1 Omni-Channel Routing

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceOmniChannelDocumentation",
  "type": "object",
  "properties": {
    "service_channel": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "relatedObject": { "type": "string" },
        "capacityModel": { "type": "string", "enum": ["StatusModel", "TabClosedModel"] }
      },
      "required": ["developerName", "relatedObject"]
    },
    "presence_configuration": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "capacity": { "type": "integer" },
        "enableAutoAccept": { "type": "boolean" },
        "enableDecline": { "type": "boolean" },
        "declineTimeout": { "type": "integer" }
      },
      "required": ["developerName", "capacity"]
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "assignedProfiles": {
          "type": "array",
          "items": { "type": "string" }
        },
        "assignedUsers": {
          "type": "array",
          "items": { "type": "string" }
        },
        "enabledPresenceStatuses": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["service_channel", "presence_configuration", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 7.2: EntitlementProcess & Milestones (Gestão de SLAs e Direitos)

O **Entitlement Process** gerencia os contratos de nível de serviço (SLAs) do Service Cloud, aplicando temporizadores e marcos (*Milestones*) com ações automatizadas à medida que um chamado progride.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/entitlementProcesses/`
* **Arquivo Mestre:** `[Process_Name]_[Version].entitlementProcess-meta.xml` (ex: `Case_SLA_Gold_v1.entitlementProcess-meta.xml`)

---

## 1. Identificação do Entitlement Process

```xml
<?xml version="1.0" encoding="UTF-8"?>
<EntitlementProcess xmlns="http://soap.sforce.com/2006/04/metadata">
    <developerName>Case_SLA_Gold_v1</developerName>
    <masterLabel>Processo de SLA - Clientes Gold</masterLabel>
    <SObjectType>Case</SObjectType>
    <entryConditionFormula>ISPICKVAL(Account.Type, 'Gold')</entryConditionFormula>
    <exitConditionFormula>IsClosed = true</exitConditionFormula>
    <isVersionDefault>true</isVersionDefault>
</EntitlementProcess>
```

| Propriedade | Valor Exemplo | Tag XML | Descrição / Comportamento |
|---|---|---|---|
| **DeveloperName / ApiName** | `Case_SLA_Gold_v1` | `<developerName>` | Identificador exclusivo do processo de SLA com a versão. |
| **MasterLabel** | `Processo de SLA - Clientes Gold` | `<masterLabel>` | Rótulo de exibição. |
| **SObjectType** | `Case` \| `WorkOrder` | `<SObjectType>` | Objeto associado ao contrato de SLA. |
| **Entry Condition** | `ISPICKVAL(Account.Type, 'Gold')` | `<entryConditionFormula>` | Fórmula que aciona o início da contagem do SLA no chamado. |
| **Exit Condition** | `IsClosed = true` | `<exitConditionFormula>` | Condição que encerra a contagem de tempo do SLA (ex: fechamento do chamado). |
| **Is Version Default** | `true` \| `false` | `<isVersionDefault>` | Define se esta versão do processo é a versão ativa padrão. |

---

## 2. Estrutura de Milestones e Ações de Disparo (`<milestones>`)

Cada **Milestone** representa um marco temporizado dentro do SLA (ex: *Primeira Resposta*, *Tempo de Resolução*).

| Atributo do Milestone | Configuração Exemplo | Tag XML | Função Técnica |
|---|---|---|---|
| **Milestone Name** | `Primeira_Resposta_Gold` | `<milestoneName>` | Nome do marco cadastrado na Org. |
| **Minutes To Complete** | `60` (Minutos) | `<minutesToComplete>` | Tempo limite em minutos para conclusão do marco. |
| **Business Hours** | `Horario_Comercial_BR` | `<businessHours>` | Horário de funcionamento considerado para a contagem do cronômetro. |

### Gatilhos de Ações em Milestones (`<milestoneActions>`)
Um marco dispara ações em 3 momentos distintos:
1. **Success Actions (`<successActions>`):** Executadas quando o marco é concluído dentro do prazo.
2. **Warning Actions (`<warningActions>`):** Executadas quando o tempo falta X% para expirar (ex: envia e-mail de alerta ao atendente).
3. **Violation Actions (`<violationActions>`):** Executadas quando o tempo do SLA estoura (ex: escala o chamado para o gerente).

---

## 3. Rastreio de Acesso, Segurança e Permissões de SLA

| Componente de SLA | Requisito de Permissões | Rastreio e Governança |
|---|---|---|
| **Entitlements & Cases** | Permissão de Objeto (`Entitlement`, `Case`) | Liberação de `Read` e `Edit` nos objetos `Entitlement` e `CaseMilestone` nos profiles/permission sets. |
| **Gestão de SLAs** | User Permission `Manage Entitlements` | Requerida para criar, alterar versões e ativar processos de SLA na Org. |

---

# 🤖 JSON Schema: 7.2 Entitlement Process & Milestones

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceEntitlementProcessDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "sObjectType": { "type": "string" },
        "entryConditionFormula": { "type": "string" },
        "exitConditionFormula": { "type": "string" },
        "isVersionDefault": { "type": "boolean" }
      },
      "required": ["developerName", "sObjectType"]
    },
    "milestones": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "milestoneName": { "type": "string" },
          "minutesToComplete": { "type": "integer" },
          "businessHours": { "type": "string" },
          "hasWarningActions": { "type": "boolean" },
          "hasViolationActions": { "type": "boolean" }
        },
        "required": ["milestoneName", "minutesToComplete"]
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "requiresManageEntitlementsPermission": { "type": "boolean", "default": true },
        "profilesWithEntitlementAccess": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "milestones", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 7.3: Base de Conhecimento — Knowledge Article Version (`Knowledge__kav`)

O **Salesforce Knowledge** gerencia artigos de conhecimento e soluções para clientes e atendentes. No formato SFDX, o Knowledge é estruturado através do objeto `Knowledge__kav` e associado a **Data Categories (Categorias de Dados)** e **Canais de Publicação**.

### Convenção de Nomes e Estrutura SFDX
* **Objeto do Knowledge:** `force-app/main/default/objects/Knowledge__kav/`
* **Campos Customizados:** `force-app/main/default/objects/Knowledge__kav/fields/`
* **Grupo de Categorias de Dados:** `force-app/main/default/dataCategoryGroupSet/`

---

## 1. Identificação e Estrutura de Campos (`Knowledge__kav`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Knowledge__kav</fullName>
    <label>Knowledge Article</label>
    <pluralLabel>Knowledge Articles</pluralLabel>
    <articleTypeChannelPaybales>false</articleTypeChannelPaybales>
    <enableFeeds>true</enableFeeds>
</CustomObject>
```

| Campo Típico do Knowledge | Tipo de Dado | Finalidade / Comportamento |
|---|---|---|
| **`Title`** | `Text(255)` | Título principal do artigo exibido nas buscas e portais. |
| **`UrlName`** | `Text(255)` | Slug de URL do artigo para publicação em sites públicos ou comunidades. |
| **`Summary`** | `TextArea` | Resumo curto do artigo exibido nos resultados de busca do console. |
| **`ValidationStatus`** | `Picklist` | Estado do fluxo de aprovação (*Not Validated*, *Validated*, *Outdated*). |
| **`PublishStatus`** | `System Picklist` | Estado do ciclo de vida: `Draft` (Rascunho), `Online` (Publicado), `Archived` (Arquivado). |

---

## 2. Grupos de Categorias de Dados (`DataCategoryGroup`) e Canais

Os artigos do Knowledge são organizados através de **Data Category Groups** e publicados seletivamente em **4 Canais de Visibilidade**:

```
 ┌─────────────────────────────────────────────────────────────┐
 │                   CANAIS DE PUBLICAÇÃO                      │
 ├─────────────────────────────────────────────────────────────┤
 │ 1. Internal App (`application`): Visível aos atendentes     │
 │ 2. Customer Portal (`customer`): Visível na Comunidade B2C  │
 │ 3. Partner Portal (`partner`): Visível na Comunidade B2B    │
 │ 4. Public Knowledge Base (`csp`): Visível na Web pública    │
 └─────────────────────────────────────────────────────────────┘
```

| Grupo de Categoria (`DataCategoryGroup`) | Categorias Ativas | Finalidade de Agrupamento |
|---|---|---|
| `Suporte_Produtos` | `Hardware`, `Software`, `Redes` | Categoriza os artigos por tipo de produto para filtros de busca. |
| `Procedimentos_RH` | `Beneficios`, `Ferias`, `Onboarding` | Artigos internos direcionados exclusivamente para funcionários. |

---

## 3. Rastreio de Acesso, Licenciamento e Permissões de Artigos

O acesso ao Salesforce Knowledge exige licença específica e direitos granulares de publicação:

| Permissão de Segurança | Tipo de Configuração | Fonte Metadado | Descrição do Acesso |
|---|---|---|---|
| **Knowledge User License** | Feature License | User Record (`IsKnowledgeAdmin`) | Licença de recurso necessária para criar, editar e publicar artigos. |
| **Acesso a Data Categories** | Profile / Permission Set | `<dataCategoryGroupVisibilities>` | Define quais categorias de dados o perfil tem permissão de visualizar/filtrar. |
| **Artigo CRUD (`Knowledge__kav`)** | Profile / Permission Set | `<objectPermissions>` | Concede permissão de `Read`, `Create`, `Edit`, `Delete` no objeto `Knowledge__kav`. |
| **Ações de Publicação** | User Permission | `<userPermissions>` | Permissões específicas como `PublishArticles`, `ArchiveArticles`, `PublishTranslation`. |

---

# 🤖 JSON Schema: 7.3 Knowledge Base (`Knowledge__kav`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceKnowledgeDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string", "default": "Knowledge__kav" },
        "label": { "type": "string" },
        "enableFeeds": { "type": "boolean" }
      },
      "required": ["developerName"]
    },
    "data_category_groups": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "groupName": { "type": "string" },
          "label": { "type": "string" },
          "categories": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "requiresKnowledgeUserLicense": { "type": "boolean", "default": true },
        "dataCategoryGroupVisibilities": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "groupName": { "type": "string" },
              "visibility": { "type": "string", "enum": ["All", "Custom", "None"] }
            }
          }
        },
        "profilesWithPublishAccess": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 7.4: Support Process, Case Assignment & Escalation Rules

Esta seção detalha o ciclo de vida dos chamados através dos **Processos de Suporte (`BusinessProcess`)**, **Regras de Atribuição de Casos (`AssignmentRules`)** e **Regras de Escalamento (`EscalationRules`)**.

### Convenção de Nomes e Estrutura SFDX
* **Support Process:** `force-app/main/default/objects/Case/businessProcesses/[Process_Name].businessProcess-meta.xml`
* **Assignment Rules:** `force-app/main/default/assignmentRules/Case.assignmentRules-meta.xml`
* **Escalation Rules:** `force-app/main/default/escalationRules/Case.escalationRules-meta.xml`

---

## 1. Processo de Suporte (`BusinessProcess` em Case)

O Processo de Suporte mapeia quais valores da lista de opções de **Status do Caso** estão disponíveis para um determinado ciclo de atendimento.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<BusinessProcess xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Processo_Suporte_N2</fullName>
    <isActive>true</isActive>
    <masterLabel>Processo de Suporte Nível 2</masterLabel>
    <values>
        <fullName>Novo</fullName>
        <default>true</default>
    </values>
    <values>
        <fullName>Em Atendimento</fullName>
        <default>false</default>
    </values>
    <values>
        <fullName>Aguardando Cliente</fullName>
        <default>false</default>
    </values>
    <values>
        <fullName>Fechado</fullName>
        <default>false</default>
    </values>
</BusinessProcess>
```

---

## 2. Regras de Atribuição Automatizada (`Case.assignmentRules`)

As **Assignment Rules** direcionam chamados recém-criados automaticamente para **Filas (*Queues*)** ou **Usuários** específicos com base em critérios de campo.

| Nome da Regra / Entrada | Critério de Entrada (`formula` / `criteriaItems`) | Atribuído Para (`queue` / `user`) | Notificação por E-mail |
|---|---|---|---|
| `Regra_Casos_VIP` | `Account.Rating = 'Hot' AND Priority = 'High'` | Fila: `Fila_Atendimento_VIP` | Modelo: `Email_Notifica_VIP` |
| `Regra_Hardware` | `ISPICKVAL(Reason, 'Hardware')` | Fila: `Fila_Suporte_Hardware` | Modelo: `Email_Notifica_Suporte` |

---

## 3. Regras de Escalamento de Chamados (`Case.escalationRules`)

As **Escalation Rules** monitoram chamados abertos que não foram resolvidos dentro do prazo estipulado, reatribuindo o chamado ou enviando alertas aos supervisores.

```xml
<escalationRule>
    <fullName>Escala_Casos_Criticos</fullName>
    <active>true</active>
    <ruleEntry>
        <criteriaItems>
            <field>Case.Priority</field>
            <operation>equals</operation>
            <value>High</value>
        </criteriaItems>
        <escalationAction>
            <assignedTo>Gerente_Suporte</assignedTo>
            <assignedToType>User</assignedToType>
            <minutesToEscalate>120</minutesToEscalate>
        </escalationAction>
    </ruleEntry>
</escalationRule>
```

| Atributo de Escalamento | Configuração Exemplo | Descrição |
|---|---|---|
| **Minutes To Escalate** | `120` (Minutos) | Tempo decorrido sem solução para disparar o escalamento. |
| **Re-atribuir Para** | Usuário `Gerente_Suporte` ou Fila `Fila_Escalamento` | Novo proprietário do chamado após o estouro do tempo. |
| **Notificar Supervisor** | E-mail do Gerente / Modelo de E-mail | Notificação enviada por e-mail alertando sobre o chamado crítico. |

---

## 4. Rastreio de Acesso, Filas e Filiações de Segurança

| Componente de Suporte | Mecanismo de Acesso / Segurança | Rastreio em Metadados |
|---|---|---|
| **Filas de Atendimento (`Queues`)** | Fila de Usuários (`Group`) | Mapeia os usuários, papéis e grupos públicos que são membros da fila no arquivo `queues/[Queue_Name].queue-meta.xml`. |
| **Atribuição de Support Process** | Record Type (`Case.RecordType`) | Cada `RecordType` de Caso obrigatoriamente aponta para um `BusinessProcess` (Processo de Suporte). |

---

# 🤖 JSON Schema: 7.4 Support Process, Assignment & Escalation

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceCaseManagementDocumentation",
  "type": "object",
  "properties": {
    "support_process": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "isActive": { "type": "boolean" },
        "statusValues": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["developerName", "statusValues"]
    },
    "assignment_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ruleName": { "type": "string" },
          "criteria": { "type": "string" },
          "assignedTo": { "type": "string" },
          "assignedToType": { "type": "string", "enum": ["Queue", "User"] }
        }
      }
    },
    "escalation_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ruleName": { "type": "string" },
          "criteria": { "type": "string" },
          "minutesToEscalate": { "type": "integer" },
          "escalateTo": { "type": "string" }
        }
      }
    },
    "queues_and_members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "queueName": { "type": "string" },
          "supportedSObjects": { "type": "array", "items": { "type": "string" } },
          "memberProfilesOrRoles": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  },
  "required": ["support_process"]
}
```

---

💡 A **Onda 07 (Service Cloud)** está completamente detalhada com todos os componentes de Omni-Channel, SLAs/Milestones, Base de Conhecimento e Processos de Atendimento de Casos. Quando desejar, podemos avançar para a **Onda 08 (Sales Cloud)**, **Onda 09 (Experience Cloud)** ou **Onda 10 (OmniStudio)**!
