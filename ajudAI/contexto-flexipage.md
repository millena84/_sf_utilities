Abaixo está o detalhamento completo e evoluído para a **Onda 04: Flexipage (Lightning Page)**.

A **Flexipage** representa a estrutura declarativa e a composição de layout de uma página Lightning no Salesforce. Ela orquestra como componentes nativos, componentes LWC/Aura customizados, fluxos (Flows) e painéis de destaque são organizados em regiões e exibidos conforme o dispositivo, o perfil e o registro em contexto.

Ao final, o modelo inclui a seção dedicada ao **Rastreio de Ativação, Perfis, Segurança e Visibilidade Condicional (Bypass)**, além do **JSON Schema** exclusivo para o **Claude Code** e scripts de automação SFDX.

---

# 📑 Modelo Evoluído: Flexipage (Lightning Page)

Uma **Flexipage** define a composição visual e funcional de uma página no Lightning Experience ou na barra de utilitários, consolidando componentes visuais em regiões gerenciadas por templates do Salesforce.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/flexipages/`
* **Arquivo de Metadado:** `[Nome_da_Pagina].flexipage-meta.xml` (ex: `Pedido_Record_Page.flexipage-meta.xml`)
* **Arquivos Relacionados no Repositório:**
  * `objects/[Objeto]/listViews/` (Visões de lista associadas)
  * `applications/[App].app-meta.xml` (Atribuição de páginas por aplicativo)
  * `customPermissions/` (Permissões customizadas usadas para visibilidade condicional)

---

## 1. Classificação por Tipo de Página (`<type>`)

O tipo da Flexipage determina onde e como ela é renderizada na plataforma:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FlexiPage xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>Página de Pedido - Vendas</masterLabel>
    <template>
        <name>flexipage:defaultRecordHomeTemplate</name>
    </template>
    <type>RecordPage</type>
    <sobjectType>Pedido__c</sobjectType>
</FlexiPage>
```

---

### 🟢 Tipos de Flexipage Suportados (`<type>`)

| Tipo (`<type>`) | Objeto Alvo (`<sobjectType>`) | Template Padrão Recomendado | Descrição / Uso Principal |
|---|---|---|---|
| **`RecordPage`** | Obrigatório (ex: `Pedido__c`) | `flexipage:defaultRecordHomeTemplate` | Layout principal de exibição e edição de um registro específico no CRM. |
| **`AppPage`** | Não se aplica | `flexipage:defaultAppHomeTemplate` | Página personalizada que atua como dashboard, hub de trabalho ou aba de aplicativo. |
| **`HomePage`** | Não se aplica | `flexipage:defaultHomeTemplate` | Página inicial exibida aos usuários ao entrarem em um aplicativo Lightning. |
| **`UtilityBar`** | Não se aplica | `flexipage:defaultUtilityBarTemplate` | Barra de utilitários fixada no rodapé da tela para aplicativos de Console ou Padrão. |
| **`CommAppPage`** | Não se aplica | `siteforce:sldsTwoFrameEightFourLayout` | Páginas dinâmicas construídas para portais e comunidades do **Experience Cloud**. |

---

## 2. Estrutura de Regiões, Templates e Componentes Embarcados

Uma Flexipage é dividida em **Regiões (`<flexiPageRegions>`)**, que contêm **Instâncias de Componentes (`<componentInstance>`)**.

### 2.1. Regiões e Facetas (`<flexiPageRegions>`)

| Região (`<name>`) | Tipo de Região (`<type>`) | Função no Layout | Componentes Típicos Embarcados |
|---|---|---|---|
| **`header`** | `Region` | Cabeçalho superior estendido. | `force:highlightsPanel` (Painel de Destaques). |
| **`main`** | `Region` | Coluna principal de trabalho. | `force:tabset` (Abas com Detalhes, Chatter e Listas Relacionadas). |
| **`sidebar` / `rightSidebar`** | `Region` | Coluna lateral direita de suporte. | `c:awsOrderSenderLwc`, `flowruntime:interview` (Flows de Ação). |
| **`utilityItems`** | `Region` | Itens da barra de utilitários. | `c:quickNotifierLwc`, `console:history` (Histórico de Navegação). |
| **`facet`** | `Facet` | Sub-região contida dentro de outro componente (ex: uma aba dentro de um `tabset`). | Instâncias de LWC ou componentes de detalhes do registro. |

---

### 2.2. Mapeamento de Componentes Embarcados e Propriedades (`<itemInstances>`)

Exemplo de declaração XML de um componente LWC e um Flow embarcados na página:

```xml
<flexiPageRegions>
    <name>sidebar</name>
    <type>Region</type>
    <itemInstances>
        <!-- Componente LWC Customizado -->
        <componentInstance>
            <componentInstanceProperties>
                <name>showDetails</name>
                <value>true</value>
            </componentInstanceProperties>
            <componentName>c:awsOrderSenderLwc</componentName>
            <identifier>c_awsOrderSenderLwc1</identifier>
        </componentInstance>
    </itemInstances>
    <itemInstances>
        <!-- Flow Declarativo Embarcado -->
        <componentInstance>
            <componentInstanceProperties>
                <name>flowArguments</name>
                <value>[{"name":"recordId","value":"{!Record.Id}"}]</value>
            </componentInstanceProperties>
            <componentInstanceProperties>
                <name>flowLayout</name>
                <value>oneColumn</value>
            </componentInstanceProperties>
            <componentName>flowruntime:interview</componentName>
            <identifier>flowruntime_interview1</identifier>
        </componentInstance>
    </itemInstances>
</flexiPageRegions>
```

---

## 3. Regras de Visibilidade Condicional de Componentes (`<visibilityRule>`)

O Salesforce permite exibir ou ocultar componentes dinamicamente na Flexipage sem escrever código, utilizando o motor de **Visibilidade Condicional**.

```xml
<componentInstance>
    <componentName>c:awsAdminToolsLwc</componentName>
    <identifier>c_awsAdminToolsLwc1</identifier>
    <visibilityRule>
        <booleanFilter>1 AND (2 OR 3)</booleanFilter>
        <criteria>
            <leftValue>{$Record.Status__c}</leftValue>
            <operator>EQUAL</operator>
            <rightValue>Aprovado</rightValue>
        </criteria>
        <criteria>
            <leftValue>{$User.Profile.Name}</leftValue>
            <operator>EQUAL</operator>
            <rightValue>System Administrator</rightValue>
        </criteria>
        <criteria>
            <leftValue>{$Permission.CustomPermission.AWS_Admin_Access}</leftValue>
            <operator>EQUAL</operator>
            <rightValue>true</rightValue>
        </criteria>
    </visibilityRule>
</componentInstance>
```

### 3.1. Tipos de Variáveis de Contexto Suportadas em Visibilidade

| Contexto (`<leftValue>`) | Exemplo de Sintaxe | Descrição / Aplicação |
|---|---|---|
| **Campos do Registro (`$Record`)** | `{$Record.Valor_Total__c}` | Exibe o componente apenas se um campo do registro atende ao valor. |
| **Dados do Usuário (`$User`)** | `{$User.Profile.Name}`, `{$User.Department}` | Restringe componentes por perfil ou departamento do usuário conectado. |
| **Permissão Customizada (`$Permission`)** | `{$Permission.CustomPermission.Nome_Da_Permissao}` | Libera o componente via *Custom Permission* ativada no *Permission Set*. |
| **Atributos do Dispositivo (`$Client`)** | `{$Client.formFactor}` | Controla exibição entre `Desktop`, `Phone` ou `Tablet`. |

---

## 4. Ativação, Atribuição e Níveis de Sobreposição (Activation Levels)

Uma Flexipage construída no repositório só é visível ao usuário final se for **ativada** na Org. A atribuição segue uma hierarquia de prioridade:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Aplicativo + Perfil + Tipo de Registro (Mais Específico) │
├─────────────────────────────────────────────────────────────┤
│ 2. Padrão do Aplicativo (App Default)                        │
├─────────────────────────────────────────────────────────────┤
│ 3. Padrão da Organização (Org Default - Mais Genérico)       │
└─────────────────────────────────────────────────────────────┘
```

| Nível de Atribuição | Atributos Envolvidos | Caso de Uso |
|---|---|---|
| **Org Default** | Flexipage + SObject | Torna a página o layout padrão global para todos os usuários da Org. |
| **App Default** | Flexipage + App Name (`LightningApp`) | Sobrescreve o layout global quando o usuário acessa um aplicativo específico (ex: App de Vendas). |
| **App + Profile + RecordType** | Flexipage + App + Profile + RecordType | Garante um layout altamente especializado para um Perfil (ex: Vendedor) trabalhando em um Tipo de Registro específico (ex: Pedido Internacional). |

---

## 5. Rastreio de Acesso, Segurança e Mecanismos de Bypass

Como a Flexipage é a camada de montagem visual, a segurança de acesso a ela é determinada pelos canais de atribuição e pelas regras de ocultação condicional.

### 5.1. Rastreio de Acesso por Aplicativos e Perfis

| Atributo de Segurança | Componente de Origem | Rastreio e Governança |
|---|---|---|
| **Aplicativos Autorizados (`Apps`)** | Custom Application (`.app-meta.xml`) | Rastreia em quais aplicativos a Flexipage está registrada na tag `<actionOverrides>`. |
| **Perfis com Acesso (`Profiles`)** | Profile (`.profile-meta.xml`) | Rastreia quais perfis possuem a atribuição da Flexipage em ativadores de página. |
| **Tipos de Registro (`RecordTypes`)** | RecordType (`.recordType-meta.xml`) | Mapeia se a Flexipage só é exibida em tipos de registro específicos. |

---

### 5.2. Mecanismos de Visibilidade e Bypass Dinâmico

| Mecanismo de Visibilidade | Tipo de Filtro | Efeito de Bypass / Liberação de Interface |
|---|---|---|
| **Bypass para Administradores** | `{$User.Profile.Name} = 'System Administrator'` | Exibe blocos de auditoria e botões de debug exclusivamente para administradores. |
| **Bypass via Custom Permission** | `{$Permission.CustomPermission.Bypass_Flexipage_Restrictions}` | Libera painéis de reprocessamento ou botões de integração via *Permission Set*. |
| **Bypass por Dispositivo (`FormFactor`)** | `{$Client.formFactor} = 'Desktop'` | Oculta relatórios e gráficos pesados quando a página é acessada via smartphone (*Phone*). |

---

# 🤖 JSON Schema Completo: Flexipage (Lightning Page)

Utilize este esquema JSON para alimentar o utilitário autômato ou **Claude Code** no parse de arquivos `.flexipage-meta.xml`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceFlexiPageDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "type": { 
          "type": "string", 
          "enum": ["RecordPage", "AppPage", "HomePage", "UtilityBar", "CommAppPage"] 
        },
        "sobjectType": { "type": "string" },
        "templateName": { "type": "string" },
        "description": { "type": "string" }
      },
      "required": ["developerName", "masterLabel", "type"]
    },
    "regions_and_structure": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "regionName": { "type": "string" },
          "regionType": { "type": "string", "enum": ["Region", "Facet"] },
          "embeddedComponents": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "componentName": { "type": "string" },
                "identifier": { "type": "string" },
                "componentProperties": {
                  "type": "object",
                  "additionalProperties": { "type": "string" }
                },
                "hasVisibilityRule": { "type": "boolean" }
              },
              "required": ["componentName", "identifier"]
            }
          }
        },
        "required": ["regionName"]
      }
    },
    "visibility_rules_summary": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "componentIdentifier": { "type": "string" },
          "booleanFilter": { "type": "string" },
          "criteriaList": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "leftValue": { "type": "string" },
                "operator": { "type": "string" },
                "rightValue": { "type": "string" }
              }
            }
          }
        }
      }
    },
    "access_and_activation_tracking": {
      "type": "object",
      "properties": {
        "activationLevel": { 
          "type": "string", 
          "enum": ["OrgDefault", "AppDefault", "AppProfileRecordType"] 
        },
        "assignedApplications": {
          "type": "array",
          "items": { "type": "string" }
        },
        "assignedProfiles": {
          "type": "array",
          "items": { "type": "string" }
        },
        "assignedRecordTypes": {
          "type": "array",
          "items": { "type": "string" }
        },
        "customPermissionsUsedInVisibility": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "regions_and_structure", "access_and_activation_tracking"]
}
```

---

💡 O modelo para a **Onda 04: Flexipage** está pronto e completo! Se desejar dar sequência, podemos avançar para o detalhamento da **Onda 05 (Segurança e Acesso: Permission Sets, Profiles e OWD)** ou de qualquer outra das ondas listadas.
