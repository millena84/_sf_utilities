# 📑 Modelo Evoluído: Documentação Técnica de External Client App (DETI - ECA Module)

Diferente das antigas *Connected Apps* (que concentravam toda a configuração em um único arquivo `.connectedApp-meta.xml`), o **External Client App (ECA)** adota uma **arquitetura modular distribuída**. As configurações são divididas em múltiplos arquivos XML espalhados em pastas distintas no repositório de código, permitindo separar a definição do aplicativo, as configurações globais de OAuth, as políticas da Org e as permissões de acesso.

---

## 1. Mapeamento da Arquitetura Multi-Pastas (Estrutura de Arquivos XML)

| Pasta no Repositório | Tipo de Metadado (`Metadata Type`) | Sufixo do Arquivo | Finalidade / Escopo |
|---|---|---|---|
| `externalClientApps/` | `ExternalClientApplication` | `.externalClientApplication-meta.xml` | **Cabeçalho do App:** Nome, descrição, e-mail de contato e estado de distribuição. |
| `extlClntAppOauthSettings/` | `ExtlClntAppOauthSettings` | `.extlClntAppOauthSettings-meta.xml` | **Configurações de OAuth:** Endpoints de callback, escopos, PKCE e certificados. |
| `extlClntAppOauthPolicies/` | `ExtlClntAppOauthConfigurablePolicies` | `.extlClntAppOauthPolicies-meta.xml` | **Políticas de OAuth da Org:** Relaxamento de IP, política de Refresh Token e controle de usuários permitidos. |
| `extlClntAppPolicies/` | `ExtlClntAppConfigurablePolicies` | `.extlClntAppPolicies-meta.xml` | **Políticas de Acesso:** Vínculo direto com *Permission Sets* e *Profiles* autorizados. |
| `extlClntAppGlobalOauthSettings/` | `ExtlClntAppGlobalOauthSettings` | `.extlClntAppGlobalOauthSettings-meta.xml` | **Configurações Globais:** Definição do ecossistema e chaves de distribuição para pacotes (se aplicável). |

---

## 2. Identificação Geral (`ExternalClientApplication`)
*Arquivo:* `externalClientApps/Minha_ECA.externalClientApplication-meta.xml`

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `{fullName}` | `<fullName>` | Identificador único do External Client App na Org/Repositório. |
| **Label** | `{label}` | `<label>` | Rótulo de exibição na interface do *Setup*. |
| **Contact Email** | `integracao@empresa.com` | `<contactEmail>` | E-mail do responsável técnico ou equipe de sustentação. |
| **Description** | `{description}` | `<description>` | Objetivo funcional e sistemas externos autorizados a conectar. |
| **Distribution State** | `Local` \| `Packageable` | `<distributionState>` | Define se o aplicativo é de uso local exclusivo ou empacotável (ISV/Package). |
| **Is Integrator Driven** | `true` \| `false` | `<isIntegratorDriven>` | Indica se a configuração do aplicativo é gerenciada diretamente pelo desenvolvedor/integrador. |

---

## 3. Configurações Globais de OAuth (`ExtlClntAppOauthSettings`)
*Arquivo:* `extlClntAppOauthSettings/Minha_ECA_oauth.extlClntAppOauthSettings-meta.xml`

| Propriedade / Tag | Valor Configurado | Tag XML | Impacto de Segurança / Comportamento |
|---|---|---|---|
| **MasterLabel** | `{label}` | `<label>` | Rótulo das configurações de OAuth. |
| **External Client App Link** | `{externalClientApplication}` | `<externalClientApplication>` | Referência ao DeveloperName da `ExternalClientApplication` pai. |
| **Callback URLs** | `https://api.empresa.com/oauth/callback` | `<callbackUrl>` | URLs de redirecionamento autorizadas para recebimento de código/token. |
| **OAuth Scopes** | `Api`, `RefreshToken`, `Web` | `<oauthScopes>` | Permissões concedidas às chamadas de API (ex: `api`, `refresh_token`, `offline_access`, `chatter_api`). |
| **Require PKCE** | `true` \| `false` | `<isCodeExchangeWithPKCERequired>` | Exige o uso de PKCE (*Proof Key for Code Exchange*) para fluxos de Authorization Code. |
| **Is Secret Required** | `true` \| `false` | `<isSecretRequired>` | Exige a apresentação de *Consumer Secret* na troca de tokens. |
| **Is Refresh Token Secret Required** | `true` \| `false` | `<isRefreshTokenSecretRequired>` | Exige *Client Secret* ao solicitar um novo Access Token via Refresh Token. |
| **Certificate Name** | `{certificate}` | `<certificate>` | Nome API do `Certificate` vinculado para autenticação mútua ou fluxo **OAuth 2.0 JWT Bearer**. |

---

## 4. Políticas Configuráveis de OAuth da Org (`ExtlClntAppOauthConfigurablePolicies`)
*Arquivo:* `extlClntAppOauthPolicies/Minha_ECA_oauthPlcy.extlClntAppOauthPolicies-meta.xml`

| Propriedade / Parâmetro | Configuração | Tag XML | Comportamento na Plataforma |
|---|---|---|---|
| **Permitted Users** | `AllUsers` \| `AdminApproved` | `<permittedUsers>` | `AdminApproved`: Apenas usuários vinculados aos Permission Sets/Perfis pré-aprovados podem autenticar. |
| **IP Relaxation** | `Enforce` \| `Relax` \| `Bypass` | `<ipRelaxation>` | `Enforce`: Aplica restrições de IP do Perfil. `Relax`: Relaxa restrições de IP para OAuth. |
| **Refresh Token Policy** | `Infinite` \| `Expire` \| `Deny` | `<refreshTokenPolicy>` | Define a validade do Refresh Token (`Infinite` = indeterminado; `Expire` = expira após inatividade). |
| **Refresh Token Validity Period** | `30` (Dias) / `null` | `<refreshTokenValidityPeriod>` | Número de dias/horas de validade do Refresh Token quando a política for `Expire`. |
| **Start URL** | `https://suaorg.my.salesforce.com/...` | `<startUrl>` | URL de redirecionamento inicial quando o aplicativo é acessado pelo App Launcher. |

---

## 5. Políticas Globais de Acesso e Permissões (`ExtlClntAppConfigurablePolicies`)
*Arquivo:* `extlClntAppPolicies/Minha_ECA_plcy.extlClntAppPolicies-meta.xml`

Mapeamento de quais **Permission Sets** e **Profiles** têm acesso pré-autorizado a este External Client App:

| Tipo de Acesso | Nome API do Recurso Autorizado | Tag XML | Descrição |
|---|---|---|---|
| **Permission Set** | `PS_AWS_Integration_User` | `<permissionSetNames>` | Conjunto de permissões com acesso liberado à API. |
| **Profile** | `System Administrator` | `<profileNames>` | Perfil de usuário pré-aprovado para autenticação. |

---

## 6. Diretrizes de Segurança e Proteção de Dados Sensíveis

⚠️ **POLÍTICA OBRIGATÓRIA DE SEGURANÇA DE METADADOS:**

1. **Consumer Key (`Client ID`):** Pode ser listada na documentação de ambiente para fins de integração e debug.
2. **Consumer Secret (`Client Secret`):** **PROIBIDO** armazenar ou registrar o *Consumer Secret* em arquivos de documentação, repositórios Git públicos ou tickets. O segredo deve ser gerenciado via *Secret Manager* externo (ex: AWS Secrets Manager, Azure Key Vault).
3. **Tokens OAuth (Access Token / Refresh Token):** **NUNCA** devem ser expostos na documentação.
4. **Certificados de Assinatura:** Documentar apenas a referência ao **Nome API do Certificado** (`<certificate>`) e sua chave pública.

---

## 7. Fluxos de Autenticação Inbound Suportados

Indicação de como sistemas externos consomem o Salesforce utilizando este External Client App:

| Fluxo OAuth 2.0 | Principais Atributos Exigidos | Uso Recomendado |
|---|---|---|
| **OAuth 2.0 JWT Bearer Flow** | `Consumer Key` + `Certificate` (.crt) + `Integration User` | **Server-to-Server:** Integrações assíncronas/batch de alta segurança sem intervenção humana (ex: AWS Lambda enviando dados para o Salesforce). |
| **OAuth 2.0 Client Credentials Flow** | `Consumer Key` + `Consumer Secret` | **Server-to-Server:** Integrações diretas entre backend e backend. |
| **OAuth 2.0 Authorization Code + PKCE** | `Consumer Key` + `Code Challenge` + `Callback URL` | **Aplicativos Móveis / SPA:** Apps nativos ou interfaces web onde o segredo não pode ser armazenado com segurança. |

---

# 🤖 JSON Schema para Extração Automatizada Multi-XML

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) encarregado de consolidar os dados das **4 pastas diferentes** de um External Client App:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceExternalClientAppDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "contactEmail": { "type": "string" },
        "description": { "type": "string" },
        "distributionState": { "type": "string" },
        "isIntegratorDriven": { "type": "boolean" }
      },
      "required": ["developerName", "label"]
    },
    "oauth_settings": {
      "type": "object",
      "properties": {
        "label": { "type": "string" },
        "callbackUrls": {
          "type": "array",
          "items": { "type": "string" }
        },
        "scopes": {
          "type": "array",
          "items": { "type": "string" }
        },
        "isCodeExchangeWithPKCERequired": { "type": "boolean" },
        "isSecretRequired": { "type": "boolean" },
        "isRefreshTokenSecretRequired": { "type": "boolean" },
        "certificate": { "type": "string" }
      }
    },
    "oauth_policies": {
      "type": "object",
      "properties": {
        "permittedUsers": { "type": "string", "enum": ["AllUsers", "AdminApproved"] },
        "ipRelaxation": { "type": "string", "enum": ["Enforce", "Relax", "Bypass"] },
        "refreshTokenPolicy": { "type": "string" },
        "refreshTokenValidityPeriod": { "type": "integer" },
        "startUrl": { "type": "string" }
      }
    },
    "access_policies": {
      "type": "object",
      "properties": {
        "permissionSetNames": {
          "type": "array",
          "items": { "type": "string" }
        },
        "profileNames": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "related_files": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "folder": { "type": "string" },
          "metadataType": { "type": "string" },
          "fileName": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "oauth_settings", "access_policies"]
}
```

---

### 💡 Vantagens da Estrutura Multi-Pastas para o seu Agente / Utilitário:

1. **Visão Holística da Integração:** O utilitário lê o arquivo principal em `externalClientApps/` e usa o `DeveloperName` para varrer e correlacionar automaticamente as subpastas (`extlClntAppOauthSettings/`, `extlClntAppOauthPolicies/` e `extlClntAppPolicies/`).
2. **Compliance de Segurança Nativo:** Garante a checagem das políticas de `AdminApproved` e relaxamento de IP, sinalizando brechas de segurança antes da implantação em Produção.
3. **Mapeamento de Inbound Completo:** Documenta desde os escopos OAuth liberados até os *Permission Sets* autorizados na mesma tabela consolidada.
