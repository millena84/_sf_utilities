Abaixo está o detalhamento completo e evoluído para a **Onda 05: Segurança, Controle de Acesso e Governança**. 

Conforme solicitado, esta onda está dividida em **modelos por tipo de metadado** e contempla um **documento único e dedicado para as configurações globais da Organização (Org Security & OWD Baseline)**, preparado para centralizar as políticas de acesso e expansões futuras de segurança.

---

# 📑 Modelo 5.1: Documento Único da Organização — Configurações Globais de Segurança e OWD (`OrgSecuritySettings`)

Este documento consolida o **baseline de segurança da Org**, englobando o modelo de compartilhamento padrão de todos os objetos (*Org-Wide Defaults - OWD*), regras de sessão, políticas de senha e restrições de rede.

### Fontes dos Dados no Repositório SFDX
* **Configurações de Segurança:** `force-app/main/default/settings/Security.settings-meta.xml`
* **Configurações da Organização:** `force-app/main/default/settings/Organization.settings-meta.xml`
* **OWD por Objeto:** `force-app/main/default/objects/[SObject]/[SObject].object-meta.xml` (`<sharingModel>`)

---

## 1. Identificação e Parâmetros Gerais da Org

| Propriedade | Valor / Configuração | Fonte Metadado | Descrição / Impacto |
|---|---|---|---|
| **Organization Name / ID** | `Minha Empresa Org` (`00D000000000001`) | `Organization.settings` | Nome oficial e ID de 15/18 caracteres do ambiente Salesforce. |
| **Org Edition** | `Enterprise Edition` \| `Unlimited Edition` | setup / API | Edição da plataforma (determina limites de licenças e recursos). |
| **Multi-Currency Active?** | `true` \| `false` | `Organization.settings` | Indica se o suporte a múltiplas moedas está habilitado na Org. |
| **Require High Assurance for Setup** | `true` \| `false` | `Security.settings` | Exige MFA/High Assurance para acesso a áreas críticas de configuração. |

---

## 2. Matriz Consolidada de Org-Wide Defaults (OWD) e Hierarquia

O OWD estabelece o nível máximo de restrição padrão. Se o OWD for `Private`, o acesso é expandido via Hierarquia de Papéis, Regras de Compartilhamento ou Apex.

| Objeto (`SObject`) | Tipo | Acesso Interno (`Internal OWD`) | Acesso Externo (`External OWD`) | Acesso via Hierarquia (`GrantAccessUsingHierarchies`) | Fonte XML |
|---|---|---|---|---|---|
| **`Account`** | Padrão | `ReadWrite` | `Private` | **`true`** | `objects/Account/Account.object-meta.xml` |
| **`Contact`** | Padrão | `ControlledByParent` | `ControlledByParent` | **`true`** | `objects/Contact/Contact.object-meta.xml` |
| **`Opportunity`** | Padrão | `Private` | `Private` | **`true`** | `objects/Opportunity/Opportunity.object-meta.xml` |
| **`Case`** | Padrão | `Read` | `Private` | **`true`** | `objects/Case/Case.object-meta.xml` |
| **`Pedido__c`** | Customizado | `Private` | `Private` | **`true`** | `objects/Pedido__c/Pedido__c.object-meta.xml` |
| **`Item_Pedido__c`** | Customizado | `ControlledByParent` | `ControlledByParent` | N/A (Master-Detail) | `objects/Item_Pedido__c/Item_Pedido__c.object-meta.xml` |

---

## 3. Políticas Globais de Sessão e Autenticação (`SessionSettings`)

*Arquivo:* `settings/Security.settings-meta.xml` (`<sessionSettings>`)

| Parâmetro de Sessão | Configuração na Org | Tag XML | Comportamento de Segurança |
|---|---|---|---|
| **Timeout de Sessão** | `2 Hours` (15m a 24h) | `<sessionTimeout>` | Período de inatividade até que o usuário seja desconectado. |
| **Bloqueio de IP por Sessão** | `true` \| `false` | `<lockSessionsToDomain>` | Força a sessão a permanecer vinculada ao IP de login inicial. |
| **MFA Obrigatório (`Multi-Factor`)** | `true` | `<enableMfaDirectUILogin>` | Exige segundo fator de autenticação em todos os logins de UI. |
| **Aviso de Expiração de Sessão** | `true` | `<forceLogoutOnSessionTimeout>` | Desconecta o usuário imediatamente sem salvar se a sessão expirar. |

---

## 4. Políticas de Senha e Complexidade (`PasswordPolicies`)

*Arquivo:* `settings/Security.settings-meta.xml` (`<passwordPolicies>`)

| Parâmetro | Valor Configurado | Descrição |
|---|---|---|
| **Expiração de Senha** | `90 Days` \| `Never` | Tempo de vida útil da senha antes de exigir redefinição. |
| **Histórico de Senhas** | `5 Passwords Remembered` | Impede a reutilização das últimas N senhas. |
| **Tamanho Mínimo da Senha** | `8 Characters` \| `12 Characters` | Comprimento mínimo exigido. |
| **Complexidade da Senha** | `AlphaNumericWithSpecialCharacters` | Exige letras, números e caracteres especiais (`@,#,$`). |
| **Tentativas de Invalidação** | `5 Max Invalid Logins` | Número de erros de login antes do bloqueio da conta. |

---

## 5. Restrições de Rede e Faixas de IP Liberadas (`NetworkAccess`)

*Arquivo:* `settings/Security.settings-meta.xml` (`<networkAccess>`)

| Nome da Regra / Descrição | IP Inicial (`startIp`) | IP Final (`endIp`) | Escopo de Acesso |
|---|---|---|---|
| `Rede_Corporativa_HQ` | `200.201.100.1` | `200.201.100.254` | Acesso liberado sem exigência de código de verificação por e-mail. |
| `VPN_DevOps_AWS` | `52.10.20.0` | `52.10.20.255` | Faixa de IP dos servidores de integração CI/CD. |

---

# 🤖 JSON Schema: 5.1 Org Security & OWD Baseline

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceOrgSecuritySettingsDocumentation",
  "type": "object",
  "properties": {
    "org_identification": {
      "type": "object",
      "properties": {
        "orgName": { "type": "string" },
        "orgId": { "type": "string" },
        "edition": { "type": "string" },
        "isMultiCurrency": { "type": "boolean" }
      },
      "required": ["orgName"]
    },
    "org_wide_defaults": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "sObject": { "type": "string" },
          "isCustom": { "type": "boolean" },
          "internalOWD": { "type": "string", "enum": ["Private", "Read", "ReadWrite", "ControlledByParent", "FullAccess"] },
          "externalOWD": { "type": "string", "enum": ["Private", "Read", "ReadWrite", "ControlledByParent"] },
          "grantAccessUsingHierarchies": { "type": "boolean" }
        },
        "required": ["sObject", "internalOWD"]
      }
    },
    "session_settings": {
      "type": "object",
      "properties": {
        "sessionTimeout": { "type": "string" },
        "mfaDirectLoginRequired": { "type": "boolean" },
        "lockSessionsToDomain": { "type": "boolean" }
      }
    },
    "password_policies": {
      "type": "object",
      "properties": {
        "expirationDays": { "type": "integer" },
        "minimumLength": { "type": "integer" },
        "complexity": { "type": "string" },
        "maxInvalidLogins": { "type": "integer" }
      }
    },
    "network_ip_ranges": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ruleName": { "type": "string" },
          "startIp": { "type": "string" },
          "endIp": { "type": "string" }
        }
      }
    }
  },
  "required": ["org_identification", "org_wide_defaults"]
}
```

---

# 📑 Modelo 5.2: Permission Set & Permission Set Group (`PermissionSet` / `PermissionSetGroup`)

Os **Permission Sets** concedem permissões aditivas (de forma não-destrutiva) a usuários sem alterar seus perfis. Os **Permission Set Groups** agrupam múltiplos conjuntos de permissões, permitindo desativar permissões pontuais via **Muting Permission Sets**.

### Convenção de Nomes e Estrutura SFDX
* **Permission Set:** `force-app/main/default/permissionsets/[Nome_PS].permissionset-meta.xml`
* **Permission Set Group:** `force-app/main/default/permissionsetgroups/[Nome_PSG].permissionsetgroup-meta.xml`

---

## 1. Identificação Geral do Permission Set

| Propriedade | Valor Exemplo | Tag XML | Descrição |
|---|---|---|---|
| **DeveloperName / ApiName** | `PS_AWS_Integration_User` | `<fullName>` | Nome API exclusivo no repositório. |
| **Label** | `AWS Integration User Access` | `<label>` | Rótulo de exibição na interface do Setup. |
| **License Requirement** | `Salesforce` \| `Salesforce Integration` \| `null` | `<hasActivationRequired>` / `<license>` | Licença exigida para atribuição (se `null`, aplica-se a qualquer licença). |
| **Has Activation Required** | `true` \| `false` | `<hasActivationRequired>` | Exige ativação baseada em sessão (Session-Based Permission Set). |

---

## 2. Desdobramento de Concessões Granulares

```xml
<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>AWS Integration User Access</label>
    
    <!-- Permissões de Classe Apex -->
    <classAccesses>
        <apexClass>AWSOrderIntegrationService</apexClass>
        <enabled>true</enabled>
    </classAccesses>
    
    <!-- Permissões de Objeto (CRUD) -->
    <objectPermissions>
        <allowCreate>true</allowCreate>
        <allowDelete>false</allowDelete>
        <allowEdit>true</allowEdit>
        <allowRead>true</allowRead>
        <modifyAllRecords>false</modifyAllRecords>
        <viewAllRecords>true</viewAllRecords>
        <object>Pedido__c</object>
    </objectPermissions>
    
    <!-- Permissões de Campo (FLS) -->
    <fieldPermissions>
        <editable>true</editable>
        <field>Pedido__c.Valor_Total__c</field>
        <readable>true</readable>
    </fieldPermissions>
    
    <!-- Permissão Customizada -->
    <customPermissions>
        <name>Bypass_Validation_Rules</name>
        <enabled>true</enabled>
    </customPermissions>
</PermissionSet>
```

### Resumo das Seções de Concessão:
* **Classes Apex (`<classAccesses>`):** Lista de classes liberadas para execução via API/UI.
* **Componentes Visualforce / Aura (`<pageAccesses>`):** Páginas e controladores acessíveis.
* **Acesso a Objetos (`<objectPermissions>`):** Nível de CRUD (`Read`, `Create`, `Edit`, `Delete`, `View All`, `Modify All`).
* **Segurança a Nível de Campo (`<fieldPermissions>`):** Nível de FLS (`Read`, `Edit`) por campo.
* **Acesso a Credenciais Externas (`<externalCredentialPrincipalAccesses>`):** Liberação de Principais de autenticação.
* **Permissões de Sistema / Usuário (`<userPermissions>`):** Direitos globais (ex: `ApiEnabled`, `ViewSetup`).

---

## 3. Estrutura de Permission Set Group e Muting (`PermissionSetGroup`)

Quando utilizado um **Permission Set Group**, múltiplos Permission Sets são combinados. Se uma permissão precisar ser revogada especificamente para aquele grupo, utiliza-se um **Muting Permission Set**:

| Propriedade PSG | Valor Exemplo | Tag XML | Função |
|---|---|---|---|
| **PSG DeveloperName** | `PSG_Sales_Operations` | `<fullName>` | Identificador do grupo de conjuntos de permissões. |
| **Permission Sets Incluídos** | `PS_Sales_User`, `PS_AWS_Integration` | `<permissionSets>` | Relação de Permission Sets agregados. |
| **Muting Permission Set** | `MPS_Sales_Operations_Mute` | `<mutingPermissionSets>` | Conjunto de "silenciamento" que desativa permissões específicas herdadas. |

---

# 🤖 JSON Schema: 5.2 Permission Set & PSG

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforcePermissionSetDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "userLicense": { "type": "string" },
        "isSessionBased": { "type": "boolean" }
      },
      "required": ["developerName", "label"]
    },
    "granted_apex_classes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "object_permissions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "sObject": { "type": "string" },
          "read": { "type": "boolean" },
          "create": { "type": "boolean" },
          "edit": { "type": "boolean" },
          "delete": { "type": "boolean" },
          "viewAll": { "type": "boolean" },
          "modifyAll": { "type": "boolean" }
        },
        "required": ["sObject"]
      }
    },
    "field_permissions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "field": { "type": "string" },
          "readable": { "type": "boolean" },
          "editable": { "type": "boolean" }
        },
        "required": ["field"]
      }
    },
    "custom_permissions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "external_credential_principals": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["identification"]
}
```

---

# 📑 Modelo 5.3: Profile (`Profile`)

O **Profile** define a base de acesso do usuário, incluindo a licença da plataforma, atribuição de layouts de página, visibilidade de guias, tipos de registro autorizados e intervalos de horas/IP de login.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/profiles/[Nome_Do_Perfil].profile-meta.xml`

---

## 1. Identificação Geral do Perfil

| Propriedade | Valor Exemplo | Tag XML | Descrição |
|---|---|---|---|
| **DeveloperName / ApiName** | `Admin` \| `Custom_Sales_User` | `<fullName>` | Nome exclusivo do perfil no repositório. |
| **User License** | `Salesforce` \| `Salesforce Integration` | `<userLicense>` | Licença base associada a este perfil. |
| **Custom Profile?** | `true` \| `false` | `<custom>` | `true`: Perfil criado pela equipe; `false`: Perfil nativo da plataforma. |

---

## 2. Atribuição de Layouts, Guias e Tipos de Registro

| Categoria | Tag XML | Exemplo Configurado | Comportamento na Interface |
|---|---|---|---|
| **Atribuição de Layout (`Layout`)** | `<layoutAssignments>` | `Pedido__c` -> `Pedido_Layout_Vendas` | Define qual Layout de Página o perfil enxerga por Tipo de Registro. |
| **Visibilidade de Guia (`Tab`)** | `<tabVisibilities>` | `Pedido__c` = `DefaultOn` \| `DefaultOff` \| `Hidden` | `DefaultOn`: Guia visível na navegação. `Hidden`: Guia oculta. |
| **Tipo de Registro (`RecordType`)** | `<recordTypeVisibilities>` | `Pedido__c.Pedido_Venda` (`default = true`) | Define quais Record Types o usuário pode selecionar ao criar registros. |

---

## 3. Restrições de Login por Horário e IP no Perfil

| Parâmetro de Restrição | Tag XML | Exemplo Configurado | Impacto de Segurança |
|---|---|---|---|
| **Horário de Login (`Login Hours`)** | `<loginHours>` | Seg-Sex: `08:00` às `18:00` | Impede o login do perfil fora do expediente comercial. |
| **Faixa de IP do Perfil (`Login IP`)** | `<loginIpRanges>` | `192.168.1.1` a `192.168.1.254` | Bloqueia logins fora dos IPs configurados especificamente para este perfil. |

---

# 🤖 JSON Schema: 5.3 Profile

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceProfileDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "userLicense": { "type": "string" },
        "isCustom": { "type": "boolean" }
      },
      "required": ["developerName", "userLicense"]
    },
    "layout_assignments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "sObject": { "type": "string" },
          "layout": { "type": "string" },
          "recordType": { "type": "string" }
        }
      }
    },
    "tab_visibilities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "tab": { "type": "string" },
          "visibility": { "type": "string", "enum": ["DefaultOn", "DefaultOff", "Hidden"] }
        }
      }
    },
    "record_type_visibilities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "recordType": { "type": "string" },
          "visible": { "type": "boolean" },
          "default": { "type": "boolean" }
        }
      }
    },
    "login_ip_ranges": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "startIp": { "type": "string" },
          "endIp": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification"]
}
```

---

# 📑 Modelo 5.4: Regras de Compartilhamento, Papéis e Grupos (`SharingRules` / `UserRole` / `Group`)

Quando o OWD de um objeto é `Private` ou `Read`, as **Sharing Rules**, **User Roles** e **Public Groups** expandem o acesso a registros de forma declarativa.

### Convenção de Nomes e Estrutura SFDX
* **Regras de Compartilhamento:** `force-app/main/default/sharingRules/[SObject].sharingRules-meta.xml`
* **Papéis na Hierarquia:** `force-app/main/default/roles/[Nome_Role].role-meta.xml`
* **Grupos Públicos:** `force-app/main/default/groups/[Nome_Group].group-meta.xml`

---

## 1. Regras de Compartilhamento Declarativo (`SharingRules`)

Existem dois tipos principais de regras de compartilhamento:
1. **Baseada em Proprietário (`OwnerRule`):** Compartilha registros cujos donos pertencem a um Papel/Grupo com outro Papel/Grupo.
2. **Baseada em Critério (`CriteriaRule`):** Compartilha registros que atendem a um filtro de campo (ex: `Valor_Total__c > 50000`).

```xml
<SharingRules xmlns="http://soap.sforce.com/2006/04/metadata">
    <!-- Regra Baseada em Critério -->
    <sharingCriteriaRules>
        <fullName>Pedidos_Altos_Para_Diretoria</fullName>
        <accessLevel>Edit</accessLevel>
        <label>Pedidos Altos Para Diretoria</label>
        <sharedTo>
            <role>Diretor_Comercial</role>
        </sharedTo>
        <criteriaItems>
            <field>Valor_Total__c</field>
            <operation>greaterThan</operation>
            <value>50000</value>
        </criteriaItems>
    </sharingCriteriaRules>
</SharingRules>
```

| Propriedade da Regra | Valor Exemplo | Tag XML | Descrição |
|---|---|---|---|
| **Rule Name / Label** | `Pedidos_Altos_Para_Diretoria` | `<fullName>` / `<label>` | Nome único e rótulo da regra. |
| **Tipo de Regra** | `Criteria` \| `Owner` | Tag pai | Define se o gatilho da regra é um campo ou o dono do registro. |
| **Nível de Acesso Concedido** | `Read` \| `Edit` | `<accessLevel>` | Nível de permissão estendido sobre os registros encontrados. |
| **Compartilhado Com (`Shared To`)** | `Role`, `Group`, `RoleAndSubordinates` | `<sharedTo>` | Destinatário do acesso (Papel, Grupo Público ou Papel e Subordinados). |

---

## 2. Hierarquia de Papéis (`UserRole`) e Grupos Públicos (`Group`)

### 2.1. Papéis na Hierarquia (`UserRole`)
* **Papel Pai (`parentRole`):** Estabelece a árvore de subordinados. Os superiores na hierarquia herdam o acesso aos registros dos subordinados quando o OWD tem `GrantAccessUsingHierarchies = true`.

| Role DeveloperName | Role Label | Parent Role (`parentRole`) | Contact Access Level | Opportunity Access Level |
|---|---|---|---|---|
| `VP_Vendas` | VP de Vendas | `CEO` | `Edit` | `Edit` |
| `Gerente_Vendas_BR` | Gerente Vendas Brasil | `VP_Vendas` | `Edit` | `Read` |

### 2.2. Grupos Públicos (`Group`)
* **Finalidade:** Agrupar Usuários, Papéis e outros Grupos para facilitar a atribuição em *Sharing Rules*, *Queues* (Filas de atendimento) e pastas de relatórios.

---

# 🤖 JSON Schema: 5.4 Sharing Rules, Roles & Groups

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceSharingRulesDocumentation",
  "type": "object",
  "properties": {
    "sObject": { "type": "string" },
    "sharing_criteria_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "developerName": { "type": "string" },
          "label": { "type": "string" },
          "accessLevel": { "type": "string", "enum": ["Read", "Edit"] },
          "sharedTo": { "type": "string" },
          "sharedToType": { "type": "string", "enum": ["Role", "Group", "RoleAndSubordinates"] },
          "criteriaField": { "type": "string" },
          "criteriaOperation": { "type": "string" },
          "criteriaValue": { "type": "string" }
        },
        "required": ["developerName", "accessLevel", "sharedTo"]
      }
    },
    "sharing_owner_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "developerName": { "type": "string" },
          "label": { "type": "string" },
          "accessLevel": { "type": "string", "enum": ["Read", "Edit"] },
          "sharedFrom": { "type": "string" },
          "sharedTo": { "type": "string" }
        },
        "required": ["developerName", "accessLevel"]
      }
    }
  },
  "required": ["sObject"]
}
```

---

💡 **Status da Suíte:** A **Onda 05 (Segurança e Acesso)** foi inteiramente estruturada com o documento único para o OWD/Segurança da Org e com os modelos específicos por metadados. Quando desejar, podemos avançar para o detalhamento da **Onda 06 (Objetos de Evento `__e`)** ou demais ondas!
