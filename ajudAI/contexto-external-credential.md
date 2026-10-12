# 📑 Modelo Evoluído: Documentação Técnica de External Credential (DETI - External Credential Module)

No modelo moderno de integrações do Salesforce, a **External Credential (`ExternalCredential`)** é o componente responsável por gerenciar a **autenticação, protocolos de segurança (OAuth, AWS SigV4, Basic, API Key, Custom) e os Principais (Named/Per-User)**, separando a camada de segurança do endereço físico da chamada (*Named Credential*).

Abaixo está o modelo completo e evoluído, alinhado 1:1 com a **Metadata API (`.externalCredential-meta.xml`)**, com a **Tooling API / Objetos Internos da Org** e com **regras rígidas de não exposição de dados sensíveis**.

---

# External Credential: Minha_EC

## 1. Identificação (Metadata XML)
*Arquivo:* `externalCredentials/Minha_EC.externalCredential-meta.xml`

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `Minha_EC` | `<fullName>` | Identificador exclusivo do metadado no repositório. |
| **Label** | `Minha EC` | `<label>` | Rótulo de exibição na interface do *Setup*. |
| **AuthenticationProtocol** | `Custom` \| `Oauth` \| `AwsSv4` \| `Basic` \| `ApiKey` \| `Jwt` \| `NoAuthentication` | `<authenticationProtocol>` | Protocolo de autenticação exigido pelo servidor de destino. |
| **AuthenticationFlowType** | `ClientCredentials` \| `JwtBearer` \| `AuthorizationCode` \| `None` | `<authenticationFlowType>` | Fluxo de concessão OAuth (quando `AuthenticationProtocol = Oauth`). |
| **Description** | `{description}` | `<description>` | Documentação técnica e finalidade da credencial externa. |

---

## 2. Dados Internos do Objeto da Org (Tooling API / Setup)
*Fonte:* Consulta via **Tooling API / SOQL** no objeto interno `ExternalCredential`

| Propriedade | Valor Exemplo | Fonte | Descrição |
|---|---|---|---|
| **Id** | `0pt000000000001AAA` | Objeto interno | ID de 15/18 caracteres da credencial na Org. |
| **DeveloperName** | `Minha_EC` | Objeto interno | Nome de API registrado no banco de dados da plataforma. |
| **MasterLabel** | `Minha EC` | Objeto interno | Rótulo mestre no banco de dados. |
| **CreatedDate** | `2026-09-01T12:00:00.000+0000` | Objeto interno | Data e hora de criação da credencial na Org. |
| **CreatedById** | `005000000000001AAA` | Objeto interno | ID do usuário criador. |
| **LastModifiedDate** | `2026-10-01T12:00:00.000+0000` | Objeto interno | Data e hora da última alteração de configuração. |
| **LastModifiedById** | `005000000000001AAA` | Objeto interno | ID do último usuário que modificou o registro. |

---

## 3. Parâmetros da Credencial Externa (`<externalCredentialParameters>`)

*Mapeamento dos parâmetros de cabeçalho, corpo, URL e Provedor de Autenticação:*

| Nome do Parâmetro (`parameterName`) | Tipo do Parâmetro (`parameterType`) | Valor / Referência (`parameterValue`) | Sequência (`sequence`) | Fonte |
|---|---|---|---|---|
| `AuthProvider` | `AuthProvider` | `AWS_OIDC_Provider` | `1` | XML / Objeto interno |
| `Scope` | `AuthHeader` | `read write orders` | `2` | XML / Objeto interno |
| `AWS_Region` | `AuthHeader` | `us-east-1` | `3` | XML / Objeto interno |
| `AWS_Service` | `AuthHeader` | `execute-api` | `4` | XML / Objeto interno |
| `x-api-key` | `AuthHeader` | `[MASCARADO / CONFIGURADO NO SETUP]` | `5` | XML / Objeto interno |

---

## 4. Principais e Controle de Acesso (`<principals>`)

*Mapeamento de quem pode autenticar e utilizar esta Credencial Externa:*

| Nome do Principal (`principalName`) | Tipo do Principal (`principalType`) | Sequência (`sequence`) | Conjuntos de Permissão Associados (`Permission Sets`) | Mapeamento de Usuário | Fonte |
|---|---|---|---|---|---|
| `Minha_EC_Principal` | `NamedPrincipal` | `1` | `PS_AWS_Integration_User` | Credencial única compartilhada por toda a Org. | XML / Setup |
| `Per_User_Principal` | `PerUserPrincipal` | `2` | `PS_Sales_Integration_Users` | Credencial individual por usuário (*Per-User Authentication*). | XML / Setup |

---

## 5. Diretrizes de Segurança e Mascaramento de Dados Sensíveis

⚠️ **POLÍTICA OBRIGATÓRIA DE SEGURANÇA:**

1. **Client Secrets / Passwords / Senhas Basic:** **PROIBIDO** expor segredos, senhas de autenticação básica ou tokens em texto plano. No relatório, exiba apenas `[MASCARADO]` ou `[DEFINIDO NO SETUP]`.
2. **Chaves de API (`API Keys`) e Tokens Bearer:** O valor do segredo permanece armazenado e criptografado exclusivamente no cofre de segredos do Salesforce (*Credential Vault*).
3. **Parâmetros Criptografados:** Apenas a chave/nome do parâmetro (`parameterName`) e sua função (`parameterType`) devem ser listados na documentação pública.

---

## 6. Componentes Dependentes e Relacionamentos

Mapeamento dos componentes que consomem e dependem desta Credencial Externa:

| Tipo do Componente | Nome API do Componente | Campo / Vínculo | Função no Fluxo |
|---|---|---|---|
| **Named Credential** | `Minha_NC` | `NamedCredential.externalCredential = 'Minha_EC'` | Define a URL e associa esta `ExternalCredential` para autenticar a chamada. |
| **Permission Set** | `PS_AWS_Integration_User` | `External Credential Principal Access` | Concede permissão ao usuário/perfil para acionar o Principal desta credencial. |
| **Auth Provider** | `AWS_OIDC_Provider` | `<externalCredentialParameters>` | Provedor OIDC/OAuth vinculado para geração de tokens. |

---

# 🤖 JSON Schema para Extração Automatizada (Utilitário / Agente)

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) encarregado de ler o arquivo `.externalCredential-meta.xml` e correlacionar com as consultas da Tooling API:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceExternalCredentialDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "authenticationProtocol": { 
          "type": "string", 
          "enum": ["Oauth", "AwsSv4", "Basic", "ApiKey", "Custom", "Jwt", "NoAuthentication"] 
        },
        "authenticationFlowType": { "type": "string" },
        "description": { "type": "string" }
      },
      "required": ["developerName", "label", "authenticationProtocol"]
    },
    "internal_data": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "createdDate": { "type": "string" },
        "createdById": { "type": "string" },
        "lastModifiedDate": { "type": "string" },
        "lastModifiedById": { "type": "string" }
      }
    },
    "parameters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "parameterName": { "type": "string" },
          "parameterType": { "type": "string" },
          "parameterValue": { "type": "string" },
          "sequence": { "type": "integer" }
        }
      }
    },
    "principals": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "principalName": { "type": "string" },
          "principalType": { "type": "string", "enum": ["NamedPrincipal", "PerUserPrincipal"] },
          "sequence": { "type": "integer" },
          "permissionSets": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "security_compliance": {
      "type": "object",
      "properties": {
        "secretsMasked": { "type": "boolean", "enum": [true] },
        "noPlaintextPasswords": { "type": "boolean", "enum": [true] }
      },
      "required": ["secretsMasked", "noPlaintextPasswords"]
    },
    "dependent_named_credentials": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["identification", "security_compliance"]
}
```

---

🔐 Quer montar a consolidação desse conjunto de modelos em um **script automatizado de validação de segurança (linter)** ou ajustar mais algum metadado de integração?
