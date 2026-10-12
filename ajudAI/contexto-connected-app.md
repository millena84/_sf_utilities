# 📑 Modelo Evoluído: Documentação Técnica de Connected App (DETI - Connected App Module)

Embora o Salesforce esteja migrando para a arquitetura modular de *External Client Apps (ECA)*, a **Connected App (`ConnectedApp`)** continua sendo amplamente utilizada para integrações de entrada (*Inbound*), SSO (SAML 2.0 / OpenID Connect) e aplicações Canvas. 

Abaixo está o modelo completo e evoluído de documentação, alinhado 1:1 com a **Metadata API (`.connectedApp-meta.xml`)**, com a **Tooling API / `ConnectedAppPolicies`** e com regras rígidas de **proteção de dados sensíveis**.

---

# Connected App: Meu_App

## 1. Identificação Geral (`ConnectedApp`)
*Arquivo:* `connectedApps/Meu_App.connectedApp-meta.xml`

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `Meu_App` | `<fullName>` | Nome API exclusivo da Connected App no repositório e na Org. |
| **Label** | `Meu App` | `<label>` | Rótulo de exibição na interface (*Setup > App Manager*). |
| **Contact Email** | `integracao@empresa.com` | `<contactEmail>` | E-mail do responsável técnico ou equipe de sustentação. |
| **Contact Phone** | `+55 11 99999-9999` | `<contactPhone>` | Telefone de contato de emergência/suporte. |
| **Description** | `{description}` | `<description>` | Objetivo funcional e sistemas externos autorizados a conectar. |
| **Icon URL / Logo URL** | `https://.../logo.png` | `<iconUrl>` / `<logoUrl>` | Links para os ícones exibidos no App Launcher. |

---

## 2. Configurações de OAuth (`<oauthConfig>`)

*Mapeamento dos parâmetros de comunicação e autenticação OAuth 2.0:*

| Propriedade / Tag | Valor Configurado | Tag XML | Impacto de Segurança / Comportamento |
|---|---|---|---|
| **Callback URL** | `https://example.com/callback` | `<callbackUrl>` | URLs de redirecionamento autorizadas para recebimento do código/token OAuth. |
| **Consumer Key (`Client ID`)** | `3MVG9...CHAVE_SIMULADA` | `<consumerKey>` | Identificador público da aplicação gerado pelo Salesforce (pode ser listado para integração). |
| **Consumer Secret (`Client Secret`)** | `[MASCARADO / DEFINIDO NO SETUP]` | `[NATIVO]` | **PROIBIDO EXPOR.** Chave secreta de autenticação do aplicativo. |
| **OAuth Scopes** | `Api`, `RefreshToken`, `Web` | `<scopes>` | Escopos de permissão concedidos às chamadas de API (ex: `Basic`, `Api`, `Web`, `RefreshToken`, `Full`). |
| **Certificate Name** | `{Certificate_ApiName}` | `<certificate>` | Nome API do `Certificate` vinculado para autenticação via **OAuth 2.0 JWT Bearer Flow**. |
| **Require PKCE** | `true` \| `false` | `<isCodeExchangeWithPKCERequired>` | Exige PKCE (*Proof Key for Code Exchange*) em fluxos de Authorization Code. |
| **Is Secret Required** | `true` \| `false` | `<isSecretRequired>` | Exige *Consumer Secret* na troca de código por token. |
| **Is Refresh Token Secret Required** | `true` \| `false` | `<isRefreshTokenSecretRequired>` | Exige *Consumer Secret* ao solicitar renovação de token via Refresh Token. |

---

## 3. Políticas de Acesso e Segurança da Org (`ConnectedAppPolicies` / Setup)
*Fonte:* Consulta via **Tooling API** no objeto `ConnectedAppPolicies` ou configurações de Setup da Org

| Propriedade de Política | Configuração | Opções / Valores Possíveis | Impacto de Governança |
|---|---|---|---|
| **Permitted Users** | `AdminApproved` | `AdminApproved` \| `AllUsers` | `AdminApproved`: Exige liberação prévia em *Permission Sets* ou *Profiles*. |
| **IP Relaxation** | `Enforce` | `Enforce` \| `Relax` \| `Bypass` | `Enforce`: Aplica restrições de IP de login do Perfil do usuário. |
| **Refresh Token Policy** | `Expire` | `Infinite` \| `Expire` \| `Deny` | `Expire`: Expira o Refresh Token após período de inatividade. |
| **Refresh Token Validity Period** | `30` (Dias) | Número inteiro de dias/horas | Tempo limite até a expiração do Refresh Token inativo. |
| **Session Timeout** | `2 Hours` | `15 Mins` a `24 Hours` / `Global` | Tempo de expiração da sessão do Access Token. |

---

## 4. Configurações Opcionais: SAML 2.0 & Canvas App

### 4.1. Configuração SAML (Se usada como IdP / Service Provider - `<samlConfig>`)
| Propriedade | Valor | Tag XML | Descrição |
|---|---|---|---|
| **ACS URL** | `https://sso.empresa.com/saml/acs` | `<acsUrl>` | Assertion Consumer Service URL do provedor externo. |
| **Entity ID** | `https://saml.empresa.com` | `<entityId>` | Identificador exclusivo da entidade SAML. |
| **SAML Subject Type** | `Username` \| `FederationId` | `<samlSubjectType>` | Campo do Salesforce usado para mapear a identidade do usuário. |

### 4.2. Configuração Canvas App (Se usada para integração de UI - `<canvasConfig>`)
| Propriedade | Valor | Tag XML | Descrição |
|---|---|---|---|
| **Canvas URL** | `https://app.empresa.com/canvas` | `<canvasUrl>` | URL da interface web externa renderizada dentro do Salesforce. |
| **Access Method** | `SignedRequest` \| `OAuth` | `<accessMethod>` | Método de autenticação e transmissão de contexto para a aplicação Canvas. |

---

## 5. Diretrizes de Segurança e Mascaramento de Dados Sensíveis

⚠️ **POLÍTICA OBRIGATÓRIA DE SEGURANÇA DE METADADOS:**

1. **Consumer Secret (`Client Secret`):** **NUNCA** inclua o segredo do consumidor em arquivos de documentação, repositórios Git públicos ou tickets. O segredo deve ser mantido estritamente no cofre de segredos da plataforma ou gerenciado via *Secret Manager* externo (ex: AWS Secrets Manager).
2. **Access Tokens & Refresh Tokens:** **PROIBIDO** registrar tokens de acesso ativos em relatórios técnicos.
3. **Consumer Key (`Client ID`):** Pode ser documentado como identificador de ambiente (Dev, UAT, Prod).

---

## 6. Componentes e Permissões Relacionadas na Org

Mapeamento de quais **Permission Sets** e **Profiles** estão pré-autorizados a autenticar através desta Connected App:

| Tipo do Componente | Nome API do Recurso Autorizado | Finalidade de Acesso |
|---|---|---|
| **Permission Set** | `PS_AWS_Integration_User` | Concede acesso de API ao usuário de integração via `AdminApproved`. |
| **Profile** | `System Administrator` | Perfil pré-autorizado no Setup da Connected App. |
| **User** | `sys.integration.aws@suaorg.com` | Usuário com licença *Salesforce Integration* associado ao fluxo. |

---

# 🤖 JSON Schema para Extração Automatizada (Utilitário / Agente)

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) encarregado de ler o arquivo `.connectedApp-meta.xml` e correlacionar com as consultas da Tooling API (`ConnectedAppPolicies`):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceConnectedAppDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "contactEmail": { "type": "string" },
        "contactPhone": { "type": "string" },
        "description": { "type": "string" }
      },
      "required": ["developerName", "label"]
    },
    "oauth_config": {
      "type": "object",
      "properties": {
        "callbackUrl": { "type": "string" },
        "consumerKey": { "type": "string" },
        "scopes": {
          "type": "array",
          "items": { "type": "string" }
        },
        "certificate": { "type": "string" },
        "isCodeExchangeWithPKCERequired": { "type": "boolean" },
        "isSecretRequired": { "type": "boolean" },
        "isRefreshTokenSecretRequired": { "type": "boolean" }
      },
      "required": ["callbackUrl", "scopes"]
    },
    "policies": {
      "type": "object",
      "properties": {
        "permittedUsers": { "type": "string", "enum": ["AdminApproved", "AllUsers"] },
        "ipRelaxation": { "type": "string", "enum": ["Enforce", "Relax", "Bypass"] },
        "refreshTokenPolicy": { "type": "string" },
        "refreshTokenValidityPeriod": { "type": "integer" }
      }
    },
    "access_control": {
      "type": "object",
      "properties": {
        "permissionSets": {
          "type": "array",
          "items": { "type": "string" }
        },
        "profiles": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "security_compliance": {
      "type": "object",
      "properties": {
        "consumerSecretMasked": { "type": "boolean", "enum": [true] },
        "noTokensExposed": { "type": "boolean", "enum": [true] }
      },
      "required": ["consumerSecretMasked", "noTokensExposed"]
    }
  },
  "required": ["identification", "oauth_config", "security_compliance"]
}
```

---

💡 **Status da Suíte de Metadados de Integração:**
Com este modelo de **Connected App**, você agora possui uma biblioteca completa e padronizada cobrindo todos os principais componentes de integração e automação do Salesforce:
1. **Flows** (*Record-Triggered*, *Screen Flow*, *Autolaunched*)
2. **Named Credentials** & **External Credentials**
3. **Certificates** & **Remote Site Settings**
4. **External Client Apps (ECA)** & **Connected Apps**

Deseja que eu ajude a organizar um script consolidado ou arquivo Mestre para orquestrar a execução dessas extrações?
