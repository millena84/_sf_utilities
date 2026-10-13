Abaixo está o detalhamento completo e evoluído para a **Onda 08: Sales Cloud**, contemplando os metadados de **Processos de Venda (`BusinessProcess` em Opportunity)**, **Configurações e Mapeamento de Conversão de Leads (`LeadConfigSettings` / `Lead.settings`)**, **Ges⁶⁵etão de Territórios de Vendas 2.0 (`Territory2Model`, `Territory2Rule`)** e **Tipos de Divisão de Oportunidade (`OpportunitySplitType`)**.

Cada modelo segue o padrão estabelecido, mapeando a estrutura de arquivos no repositório SFDX, tabelas de atributos XML, seções de **Rastreio de Acesso, Segurança, Perfis e Permissões**, finalizando com o **JSON Schema** dedicado para o **Claude Code** ou utilitários de automação.

---

# 📑 Modelo 8.1: Processo de Vendas (`BusinessProcess` em Opportunity)

O **Sales Process (`BusinessProcess`)** define o ciclo de vida comercial da Oportunidade, mapeando quais etapas (*StageName*) do funil de vendas estão ativas e disponíveis para um determinado tipo de negócio.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/objects/Opportunity/businessProcesses/`
* **Arquivo Mestre:** `[Process_Name].businessProcess-meta.xml` (ex: `Processo_Vendas_Enterprise.businessProcess-meta.xml`)

---

## 1. Identificação Geral do Processo de Vendas

```xml
<?xml version="1.0" encoding="UTF-8"?>
<BusinessProcess xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Processo_Vendas_Enterprise</fullName>
    <isActive>true</isActive>
    <masterLabel>Processo de Vendas Enterprise</masterLabel>
    <description>Ciclo de vendas complexo para contas corporativas com etapas de negociação técnica</description>
    <values>
        <fullName>Prospecção</fullName>
        <default>true</default>
    </values>
    <values>
        <fullName>Qualificação</fullName>
        <default>false</default>
    </values>
    <values>
        <fullName>Proposta de Valor</fullName>
        <default>false</default>
    </values>
    <values>
        <fullName>Negociação/Fechamento</fullName>
        <default>false</default>
    </values>
    <values>
        <fullName>Fechado Ganho</fullName>
        <default>false</default>
    </values>
    <values>
        <fullName>Fechado Perdido</fullName>
        <default>false</default>
    </values>
</BusinessProcess>
```

| Propriedade | Valor Exemplo | Tag XML | Descrição / Impacto no CRM |
|---|---|---|---|
| **DeveloperName / ApiName** | `Processo_Vendas_Enterprise` | `<fullName>` | Identificador exclusivo do processo no repositório. |
| **MasterLabel** | `Processo de Vendas Enterprise` | `<masterLabel>` | Rótulo exibido no Setup ao associar ao Tipo de Registro. |
| **Is Active** | `true` \| `false` | `<isActive>` | Estado de publicação (`true` permite associação a Record Types). |
| **Etapas Selecionadas (`values`)** | `Prospecção`, `Qualificação`, `Fechado Ganho` | `<values><fullName>` | Conjunto de valores da picklist `Opportunity.StageName` ativos neste funil. |

---

## 2. Rastreio de Acesso, Associação de Record Types e Segurança

O Processo de Vendas não é atribuído diretamente aos perfis dos usuários; ele é vinculado a um **Record Type** de Oportunidade, que por sua vez é liberado nos Profiles e Permission Sets:

```
┌─────────────────────────┐     ┌────────────────────────────────┐     ┌────────────────────────────┐
│ BusinessProcess         │ ──> │ Opportunity Record Type        │ ──> │ Profile / Permission Set   │
│ (Etapas de Venda)       │     │ (Layout e Processo Vinculados) │     │ (Liberação de Acesso)      │
└─────────────────────────┘     └────────────────────────────────┘     └────────────────────────────┘
```

| Componente | Tipo de Vínculo | Tag / Fonte XML | Rastreio e Governança |
|---|---|---|---|
| **Record Type Vinculado** | `Opportunity.RecordType` | `<businessProcess>Processo_Vendas_Enterprise</businessProcess>` | Mapeia qual Tipo de Registro de Oportunidade consome este processo. |
| **Perfis com Acesso** | `Profile` | `<recordTypeVisibilities><recordType>Opportunity.Enterprise</recordType><visible>true</visible></recordTypeVisibilities>` | Rastreia quais perfis podem criar oportunidades usando este funil. |

---

# 🤖 JSON Schema: 8.1 Sales Process (`BusinessProcess`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceSalesProcessDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "isActive": { "type": "boolean" },
        "description": { "type": "string" }
      },
      "required": ["developerName", "isActive"]
    },
    "stage_values": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "stageName": { "type": "string" },
          "isDefault": { "type": "boolean" }
        },
        "required": ["stageName"]
      }
    },
    "access_and_record_type_tracking": {
      "type": "object",
      "properties": {
        "boundRecordTypes": {
          "type": "array",
          "items": { "type": "string" }
        },
        "assignedProfiles": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "stage_values", "access_and_record_type_tracking"]
}
```

---

# 📑 Modelo 8.2: Mapeamento de Conversão de Leads (`LeadConvertSettings` / `Lead.settings`)

As configurações de conversão de Lead gerenciam o comportamento do botão **Convert** no Lead, estabelecendo o mapeamento de "de-para" dos campos customizados do Lead para os objetos de destino: **Conta (`Account`)**, **Contato (`Contact`)** e **Oportunidade (`Opportunity`)**.

### Convenção de Nomes e Estrutura SFDX
* **Arquivo de Configuração Globais de Lead:** `force-app/main/default/settings/Lead.settings-meta.xml`
* **Mapeamento de Campos de Conversão:** `force-app/main/default/objects/Lead/leadConvertSettings/LeadConvertSettings.leadConvertSettings-meta.xml`

---

## 1. Identificação e Parâmetros de Conversão (`Lead.settings`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LeadSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableLeadConvert>true</enableLeadConvert>
    <createOpportunityOnConvert>true</createOpportunityOnConvert>
    <selectDefaultOpportunityStageUponConvert>Qualificação</selectDefaultOpportunityStageUponConvert>
</LeadSettings>
```

| Propriedade / Configuração | Valor Exemplo | Tag XML | Descrição / Comportamento no CRM |
|---|---|---|---|
| **Create Opportunity Default** | `true` \| `false` | `<createOpportunityOnConvert>` | Define se a caixa "Não criar oportunidade na conversão" vem desmarcada por padrão. |
| **Default Opportunity Stage** | `Qualificação` | `<selectDefaultOpportunityStageUponConvert>` | Etapa inicial da Oportunidade gerada automaticamente na conversão. |

---

## 2. Mapeamento de Campos Customizados ("De-Para" de Conversão)

Tabela que rastreia a transferência de dados do Lead para os alvos durante o processo de conversão:

| Campo de Origem (`Lead Field`) | Objeto de Destino (`Target Object`) | Campo de Destino (`Target Field`) | Tag XML (`<objectMapping>`) |
|---|---|---|---|
| `Lead.CNPJ__c` | **`Account`** | `Account.CNPJ__c` | `<inputField>CNPJ__c</inputField><outputField>CNPJ__c</outputField>` |
| `Lead.Cargo_Nivel__c` | **`Contact`** | `Contact.Nivel_Hierarquico__c` | `<inputField>Cargo_Nivel__c</inputField><outputField>Nivel_Hierarquico__c</outputField>` |
| `Lead.Orcamento_Estimado__c` | **`Opportunity`** | `Opportunity.Amount` | `<inputField>Orcamento_Estimado__c</inputField><outputField>Amount</outputField>` |

---

## 3. Rastreio de Acesso, Segurança e Permissões de Conversão

Para converter um Lead com sucesso, o usuário deve possuir direitos específicos no sistema:

| Permissão de Segurança | Tipo de Configuração | Fonte Metadado | Função / Impacto |
|---|---|---|---|
| **Convert Leads** | User Permission | `<userPermissions><name>ConvertLeads</name><enabled>true</enabled></userPermissions>` | Permissão necessária para visualizar o botão de conversão. |
| **CRUD nos Objetos Alvo** | Profile / Permission Set | `<objectPermissions>` | Requer permissão de `Create` e `Edit` em `Account`, `Contact` e `Opportunity`. |
| **FLS nos Campos Mapeados** | Profile / Permission Set | `<fieldPermissions>` | O usuário precisa ter acesso de leitura no campo do Lead e escrita no campo de destino. |

---

# 🤖 JSON Schema: 8.2 Lead Convert Settings

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceLeadConvertSettingsDocumentation",
  "type": "object",
  "properties": {
    "general_settings": {
      "type": "object",
      "properties": {
        "createOpportunityByDefault": { "type": "boolean" },
        "defaultOpportunityStage": { "type": "string" }
      }
    },
    "field_mappings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "leadSourceField": { "type": "string" },
          "targetObject": { "type": "string", "enum": ["Account", "Contact", "Opportunity"] },
          "targetField": { "type": "string" }
        },
        "required": ["leadSourceField", "targetObject", "targetField"]
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "requiresConvertLeadsPermission": { "type": "boolean", "default": true },
        "profilesWithConvertAccess": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["field_mappings", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 8.3: Gestão de Territórios de Vendas 2.0 (`Territory2Model`, `Territory2`, `Territory2Rule`)

O **Enterprise Territory Management (Territory 2.0)** permite estruturar áreas geográficas, linhas de produtos ou segmentos de mercado, atribuindo contas a territórios e concedendo acesso de compartilhamento a vendedores e gerentes.

### Convenção de Nomes e Estrutura SFDX
* **Modelo de Território:** `force-app/main/default/territory2Models/[Model_Name]/[Model_Name].territory2Model-meta.xml`
* **Territórios da Hierarquia:** `force-app/main/default/territory2Models/[Model_Name]/territories/[Territory_Name].territory2-meta.xml`
* **Regras de Atribuição:** `force-app/main/default/territory2Models/[Model_Name]/rules/[Rule_Name].territory2Rule-meta.xml`

---

## 1. Identificação do Modelo e Territórios (`Territory2Model` & `Territory2`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Territory2Model xmlns="http://soap.sforce.com/2006/04/metadata">
    <developerName>Modelo_Vendas_2026</developerName>
    <masterLabel>Modelo de Vendas 2026</masterLabel>
    <state>Active</state>
</Territory2Model>
```

| Propriedade do Território (`Territory2`) | Valor Exemplo | Tag XML | Descrição / Função |
|---|---|---|---|
| **DeveloperName / ApiName** | `Territorio_Brasil_Sudeste` | `<developerName>` | Nome API do território individual. |
| **Territory2Type** | `Regional_Account_Type` | `<territory2Type>` | Categoria do território configurada na Org. |
| **Parent Territory** | `Territorio_Brasil_Master` | `<parentTerritory>` | Território pai na árvore de hierarquia. |
| **Account Access Level** | `Edit` \| `Read` | `<accountAccessLevel>` | Nível de acesso que os membros do território recebem nas Contas atribuídas. |
| **Opportunity Access Level** | `Edit` \| `Read` \| `None` | `<opportunityAccessLevel>` | Nível de acesso dos membros às Oportunidades das contas do território. |

---

## 2. Regras de Atribuição Automática de Contas (`Territory2Rule`)

As regras avaliam os campos das Contas e as vinculam automaticamente aos territórios correspondentes:

| Nome da Regra (`developerName`) | Atributo Filtrado | Operador | Valor do Filtro | Territórios Atribuídos |
|---|---|---|---|---|
| `Regra_UF_SP_RJ` | `Account.BillingState` | `equals` | `SP, RJ` | `Territorio_Brasil_Sudeste` |
| `Regra_Porte_Enterprise` | `Account.AnnualRevenue` | `greaterOrEqual` | `100000000` | `Territorio_Global_Enterprise` |

---

## 3. Rastreio de Acesso, Membros e Permissões de Território

| Componente | Requisito de Permissão / Segurança | Rastreio e Governança |
|---|---|---|
| **Membros do Território (`Users`)** | Atribuição de Usuários no Território | Mapeia quais vendedores pertencem ao território no arquivo `.territory2-meta.xml`. |
| **Gestão de Territórios** | User Permission `Manage Territories` | Necessária para alterar estruturas de territórios e rodar regras de atribuição. |

---

# 🤖 JSON Schema: 8.3 Territory Management 2.0

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceTerritoryManagementDocumentation",
  "type": "object",
  "properties": {
    "territory_model": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "state": { "type": "string", "enum": ["Planning", "Active", "Archived"] }
      },
      "required": ["developerName", "state"]
    },
    "territories": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "developerName": { "type": "string" },
          "masterLabel": { "type": "string" },
          "parentTerritory": { "type": "string" },
          "accountAccessLevel": { "type": "string", "enum": ["Read", "Edit"] },
          "opportunityAccessLevel": { "type": "string", "enum": ["None", "Read", "Edit"] }
        },
        "required": ["developerName", "accountAccessLevel"]
      }
    },
    "assignment_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ruleName": { "type": "string" },
          "attribute": { "type": "string" },
          "operator": { "type": "string" },
          "value": { "type": "string" },
          "assignedTerritories": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "requiresManageTerritoriesPermission": { "type": "boolean", "default": true },
        "assignedUsersByTerritory": {
          "type": "object",
          "additionalProperties": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    }
  },
  "required": ["territory_model", "territories", "access_and_security_tracking"]
}
```

---

# 📑 Modelo 8.4: Tipos de Divisão de Oportunidade (`OpportunitySplitType`)

O **Opportunity Split Type** permite dividir a comissão, o valor negociado ou o crédito de vendas de uma Oportunidade entre múltiplos membros da Equipe de Vendas (*Opportunity Team*).

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/opportunitySplitTypes/`
* **Arquivo Mestre:** `[SplitType_Name].opportunitySplitType-meta.xml` (ex: `Receita_Principal.opportunitySplitType-meta.xml`)

---

## 1. Identificação do Tipo de Divisão (`OpportunitySplitType`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<OpportunitySplitType xmlns="http://soap.sforce.com/2006/04/metadata">
    <developerName>Receita_Principal</developerName>
    <masterLabel>Divisão de Receita</masterLabel>
    <splitField>Amount</splitField>
    <isTotalPercentageEnforced>true</isTotalPercentageEnforced>
    <description>Divisão padrão do valor total da oportunidade. Exige soma igual a 100%.</description>
</OpportunitySplitType>
```

| Propriedade | Valor Exemplo | Tag XML | Descrição Técnica / Regra de Negócio |
|---|---|---|---|
| **DeveloperName / ApiName** | `Receita_Principal` | `<developerName>` | Identificador do tipo de divisão. |
| **MasterLabel** | `Divisão de Receita` | `<masterLabel>` | Rótulo exibido nas tabelas de divisão da Oportunidade. |
| **Split Field** | `Amount` \| `Valor_Customizado__c` | `<splitField>` | Campo numérico/moeda da Oportunidade que é objeto da divisão. |
| **Is Total Percentage Enforced** | **`true`** \| `false` | `<isTotalPercentageEnforced>` | **`true` (Revenue Split)**: Exige estritamente que a soma dos percentuais seja igual a **100%**.<br>**`false` (Overlay Split)**: Permite que a soma seja menor ou maior que 100% (ex: crédito secundário). |

---

## 2. Rastreio de Acesso, Permissões e Equipe da Oportunidade

| Componente | Requisito de Segurança / Permissão | Rastreio em Metadados |
|---|---|---|
| **Opportunity Team (`OpportunityTeamMember`)** | Habilitação do recurso *Opportunity Team* | Apenas usuários que são membros da equipe daquela Oportunidade podem ser incluídos na divisão. |
| **Gestão de Divisões** | User Permission `ManageOpportunitySplits` | Necessária para criar novos tipos de divisão ou alterar regras globais. |
| **Acesso a Campos (FLS)** | Profile / Permission Set | Requer leitura/escrita nos campos `OpportunitySplit.SplitAmount` e `OpportunitySplit.SplitPercentage`. |

---

# 🤖 JSON Schema: 8.4 Opportunity Split Type

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceOpportunitySplitTypeDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "splitField": { "type": "string" },
        "isTotalPercentageEnforced": { "type": "boolean" },
        "description": { "type": "string" }
      },
      "required": ["developerName", "splitField", "isTotalPercentageEnforced"]
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "requiresOpportunityTeamEnabled": { "type": "boolean", "default": true },
        "requiresManageOpportunitySplitsPermission": { "type": "boolean", "default": true },
        "profilesWithSplitAccess": {
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

💡 A **Onda 08 (Sales Cloud)** está concluída! Se desejar dar sequência, podemos prosseguir com o detalhamento da **Onda 09 (Experience Cloud)** ou da **Onda 10 (OmniStudio)**.
