# 📑 Modelo Evoluído: Experience Cloud (Onda 09 - Digital Experiences Module)

O **Experience Cloud (Digital Experiences / Communities)** permite criar portais B2B/B2C, sites públicos e hubs de parceiros integrados nativamente ao Salesforce. No formato de código-fonte SFDX, a arquitetura de um portal é composta pela tríade: **Network (`Network`)**, **Custom Site (`CustomSite`)** e **ExperienceBundle (`ExperienceBundle` / `DigitalExperienceBundle`)**.

---

# 📑 Modelo 9.1: Network (`Network`)

A **Network** gerencia as configurações de identidade, membros autorizados, modelos de e-mail transacionais, recursos de colaboração e autorregistro de um portal do Experience Cloud.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/networks/`
* **Arquivo Mestre:** `[Network_Name].network-meta.xml` (ex: `Portal_Clientes.network-meta.xml`)

---

## 1. Identificação Geral da Network (`Network.network-meta.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Network xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Portal_Clientes</fullName>
    <label>Portal de Clientes</label>
    <status>Live</status>
    <enableGuestChatter>false</enableGuestChatter>
    <enableKnowledgeable>true</enableKnowledgeable>
    <enableNicknameDisplay>true</enableNicknameDisplay>
    <selfRegistration>true</selfRegistration>
    <networkMemberGroups>
        <profile>Customer Community User</profile>
        <profile>Customer Community Plus User</profile>
    </networkMemberGroups>
</Network>
```

| Propriedade | Valor Exemplo | Tag XML | Descrição / Impacto de Governança |
|---|---|---|---|
| **DeveloperName / ApiName** | `Portal_Clientes` | `<fullName>` | Identificador exclusivo da rede no repositório. |
| **Label** | `Portal de Clientes` | `<label>` | Rótulo exibido no Setup do Experience Cloud. |
| **Status** | `Live` \| `UnderConstruction` \| `Inactive` | `<status>` | **`Live`**: Portal publicado e acessível.<br>**`UnderConstruction`**: Acesso restrito a administradores. |
| **Self Registration** | `true` \| `false` | `<selfRegistration>` | Habilita o formulário de autorregistro de novos usuários no portal. |
| **Enable Guest Chatter** | `true` \| `false` | `<enableGuestChatter>` | Permite que usuários não autenticados (convidados) visualizem feeds do Chatter. |
| **Enable Knowledgeable** | `true` \| `false` | `<enableKnowledgeable>` | Ativa a integração com o Salesforce Knowledge no portal. |

---

## 2. Rastreio de Membros, Perfis e Acesso (`networkMemberGroups`)

A tag `<networkMemberGroups>` estabelece quais **Perfis** e **Permission Sets** têm permissão de fazer login e acessar o portal:

| Tipo de Grupo | Nome do Perfil / Permission Set | Tag XML | Função de Acesso |
|---|---|---|---|
| **Profile Member** | `Customer Community User` | `<networkMemberGroups><profile>` | Perfil padrão de clientes B2C para acesso ao portal. |
| **Profile Member** | `Customer Community Plus User` | `<networkMemberGroups><profile>` | Perfil avançado com suporte a papéis de usuário (*User Roles*). |
| **Permission Set Member** | `PS_Portal_Partner_Access` | `<networkMemberGroups><permissionSet>` | Concede acesso ao portal via conjunto de permissões. |

---

## 3. Configurações de E-mail Transacional e Boas-Vindas

| Tipo de E-mail | Template Utilizado | Tag XML | Descrição |
|---|---|---|---|
| **E-mail de Boas-Vindas** | `unfiled$public/CommunityWelcomeEmail` | `<welcomeTemplate>` | Modelo enviado automaticamente na criação do usuário do portal. |
| **Redefinição de Senha** | `unfiled$public/CommunityForgotPasswordEmail` | `<forgotPasswordTemplate>` | Modelo enviado ao solicitar redefinição de senha. |
| **E-mail do Remetente** | `suporte@empresa.com` | `<emailSenderEmail>` | Endereço de e-mail exibido como remetente das mensagens do portal. |

---

# 🤖 JSON Schema: 9.1 Network (`Network`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceNetworkDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "status": { "type": "string", "enum": ["Live", "UnderConstruction", "Inactive"] },
        "selfRegistrationEnabled": { "type": "boolean" },
        "enableKnowledgeable": { "type": "boolean" }
      },
      "required": ["developerName", "status"]
    },
    "member_access_tracking": {
      "type": "object",
      "properties": {
        "allowedProfiles": {
          "type": "array",
          "items": { "type": "string" }
        },
        "allowedPermissionSets": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["allowedProfiles"]
    },
    "email_configuration": {
      "type": "object",
      "properties": {
        "senderEmail": { "type": "string" },
        "welcomeTemplate": { "type": "string" },
        "forgotPasswordTemplate": { "type": "string" }
      }
    }
  },
  "required": ["identification", "member_access_tracking"]
}
```

---

# 📑 Modelo 9.2: Custom Site (`CustomSite`)

O **Custom Site** gerencia os parâmetros de infraestrutura web pública do portal, incluindo domínio, caminho da URL, proprietário padrão de registros criados por convidados e a conta de usuário **Guest User**.

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório:** `force-app/main/default/sites/`
* **Arquivo Mestre:** `[Site_Name].site-meta.xml` (ex: `Portal_Clientes.site-meta.xml`)

---

## 1. Identificação Geral do Custom Site (`CustomSite.site-meta.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CustomSite xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Portal_Clientes</fullName>
    <masterLabel>Portal de Clientes</masterLabel>
    <active>true</active>
    <siteAdmin>admin@empresa.com</siteAdmin>
    <siteGuestRecordDefaultOwner>sys.integration@empresa.com</siteGuestRecordDefaultOwner>
    <subdomain>minhaempresa</subdomain>
    <urlPathPrefix>clientes</urlPathPrefix>
    <siteType>ChatterNetwork</siteType>
</CustomSite>
```

| Propriedade | Valor Exemplo | Tag XML | Descrição / Função de Infraestrutura |
|---|---|---|---|
| **DeveloperName / ApiName** | `Portal_Clientes` | `<fullName>` | Nome API do site no repositório. |
| **MasterLabel** | `Portal de Clientes` | `<masterLabel>` | Rótulo de exibição no Setup. |
| **Active** | `true` \| `false` | `<active>` | Define se a URL do site responde publicamente na web. |
| **URL Path Prefix** | `clientes` | `<urlPathPrefix>` | Prefixo do caminho na URL (ex: `https://minhaempresa.my.site.com/clientes`). |
| **Subdomain** | `minhaempresa` | `<subdomain>` | Subdomínio MyDomain associado ao site. |
| **Guest Record Default Owner** | `sys.integration@empresa.com` | `<siteGuestRecordDefaultOwner>` | **Segurança:** Usuário que recebe a propriedade dos registros criados por visitantes anônimos. |

---

## 2. Rastreio de Segurança do Guest User (Usuário Convidado)

O **Guest User Profile** é criado automaticamente para gerenciar o acesso de visitantes anônimos (não autenticados) ao site:

```
┌─────────────────────────────────────────────────────────────┐
│ CustomSite (`Portal_Clientes`)                              │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Guest User Profile (`Portal Clientes Profile`)              │
│ - OWD Externo obrigatoriamente PRIVATE                     │
│ - Sem permissões de Edit / Delete (Apenas Read / Create)   │
│ - Acesso a registros via Guest Sharing Rules                │
└─────────────────────────────────────────────────────────────┘
```

| Requisito de Segurança do Guest User | Trava de Segurança Nativa | Fonte XML / Governança |
|---|---|---|
| **Perfil Automático** | `Portal_Clientes Profile` | Perfil associado exclusivamente ao site público. |
| **Restrição de CRUD** | Proibido `Edit`, `Delete` ou `Modify All` | Apenas `Read` e `Create` são permitidos no perfil de convidado. |
| **Guest Sharing Rule** | `Guest` Access Type | Único mecanismo declarativo para expor registros para o Guest User. |

---

# 🤖 JSON Schema: 9.2 Custom Site (`CustomSite`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceCustomSiteDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "active": { "type": "boolean" },
        "subdomain": { "type": "string" },
        "urlPathPrefix": { "type": "string" },
        "siteType": { "type": "string" }
      },
      "required": ["developerName", "active"]
    },
    "guest_user_security_tracking": {
      "type": "object",
      "properties": {
        "guestRecordDefaultOwner": { "type": "string" },
        "guestProfileName": { "type": "string" },
        "hasGuestSharingRules": { "type": "boolean" }
      },
      "required": ["guestRecordDefaultOwner"]
    }
  },
  "required": ["identification", "guest_user_security_tracking"]
}
```

---

# 📑 Modelo 9.3: ExperienceBundle / DigitalExperienceBundle (`ExperienceBundle`)

O **ExperienceBundle** armazena a estrutura do construtor de páginas (*Experience Builder*), incluindo layouts, temas, rotas, componentes LWC embarcados e regras de direcionamento de público-alvo (*Audience Targeting*).

### Convenção de Nomes e Estrutura SFDX
* **Diretório no Repositório (LWR / Aura):** `force-app/main/default/experiences/[Experience_Name]/`
* **Subpastas da Estrutura:**
  * `config/`: Configurações globais do site e cabeçalhos.
  * `views/`: Definições em JSON de cada página individual (ex: `home.json`, `recordDetail.json`).
  * `routes/`: Mapeamento de URLs e rotas de navegação (ex: `home.json`).
  * `themes/`: Definição visual do tema e variáveis de marca (*branding*).

---

## 1. Mapeamento de Páginas, Componentes e Rotas (`views/*.json`)

Exemplo da estrutura JSON de uma visão (`views/home.json`) contendo um componente LWC embarcado:

```json
{
  "appPageId": "b1a2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
  "componentName": "siteforce:sldsTwoFrameEightFourLayout",
  "id": "home_page_view",
  "label": "Home",
  "regions": [
    {
      "components": [
        {
          "componentAttributes": {
            "title": "Bem-vindo ao Portal"
          },
          "componentName": "c:portalHeaderLwc",
          "id": "custom_header_cmp",
          "renderPriority": "NEUTRAL",
          "type": "component"
        }
      ],
      "name": "header",
      "type": "region"
    }
  ],
  "type": "view"
}
```

| Atributo da Página / Visão | Valor Exemplo | Descrição Técnica |
|---|---|---|
| **View Name (`id`)** | `home` \| `recordDetail` | Identificador da página dentro do Experience Builder. |
| **Layout Template (`componentName`)** | `siteforce:sldsTwoFrameEightFourLayout` | Template de colunas utilizado para renderizar a página. |
| **Componentes Embarcados** | `c:portalHeaderLwc`, `forceCommunity:recordDetail` | Relação de LWCs e componentes nativos presentes nas regiões da página. |

---

## 2. Direcionamento de Público-Alvo e Visibilidade (*Audience Targeting*)

O Experience Cloud permite exibir páginas ou componentes diferentes com base no **Público-Alvo (`Audience`)**:

| Nome da Audiência (`Audience`) | Critério de Segmentação | Comportamento de Exibição |
|---|---|---|
| **Audiencia_Clientes_VIP** | `User.Account.Rating = 'Hot'` | Exibe a versão customizada da página inicial com ofertas exclusivas. |
| **Audiencia_Parceiros_BR** | `User.UserType = 'PowerPartner' AND User.Country = 'Brazil'` | Libera componentes de registro de deal e acompanhamento de metas. |

---

## 3. Rastreio de Acesso, Segurança e Permissões do ExperienceBundle

| Camada de Segurança | Mecanismo de Controle | Rastreio e Governança |
|---|---|---|
| **Acesso à Página** | Configuração de Rota (`routes/*.json`) | Define se a página exige autenticação (`RequiresLogin`) ou se é aberta ao público (`Public`). |
| **Acesso aos Componentes LWC** | Controller Apex (`@AuraEnabled`) | Os LWCs contidos nas páginas dependem do acesso dos Perfis às classes Apex chamadas. |
| **Acesso a Dados no Portal** | User Mode / LDS | Garantido nativamente pelo banco de dados do Salesforce respeitando as licenças do portal. |

---

# 🤖 JSON Schema: 9.3 ExperienceBundle

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceExperienceBundleDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "experienceName": { "type": "string" },
        "templateType": { "type": "string", "enum": ["Aura", "LWR"] },
        "description": { "type": "string" }
      },
      "required": ["experienceName", "templateType"]
    },
    "pages_and_views": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "viewId": { "type": "string" },
          "label": { "type": "string" },
          "layoutTemplate": { "type": "string" },
          "requiresLogin": { "type": "boolean" },
          "embeddedComponents": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["viewId", "label"]
      }
    },
    "audience_targeting": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "audienceName": { "type": "string" },
          "criteriaFormula": { "type": "string" },
          "assignedPagesOrComponents": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "publicPagesList": {
          "type": "array",
          "items": { "type": "string" }
        },
        "authenticatedPagesList": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "pages_and_views", "access_and_security_tracking"]
}
```

---

💡 A **Onda 09 (Experience Cloud)** está concluída! Se desejar dar sequência, podemos prosseguir com o detalhamento da **Onda 10 (OmniStudio / Industries Cloud)**!
