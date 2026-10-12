Aqui está o modelo completo e evoluído de documentação para **Named Credential** (cobrindo tanto a arquitetura moderna baseada em **External Credentials** quanto a legado), alinhado 1:1 com a **Metadata API do Salesforce (`.namedCredential-meta.xml` / `.externalCredential-meta.xml`)** e pronto para ser extraído e preenchido por utilitários autômatos ou agentes de IA.

---

# 📑 Modelo Evoluído: Documentação Técnica de Named Credential (DETI - Named Credential Module)

---

## 1. Identificação Geral (`NamedCredential`)

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `{NamedCredential.fullName}` | `<fullName>` | Nome API exclusivo da Named Credential. |
| **MasterLabel** | `{NamedCredential.label}` | `<label>` | Rótulo de exibição na interface do Setup. |
| **NamedCredentialType** | `SecuredEndpoint` \| `Legacy` | `<namedCredentialType>` | Arquitetura utilizada (Moderna com External Credential vs. Legada). |
| **Endpoint URL** | `https://api.exemplo.com/v1` | `<endpoint>` | URL base do serviço externo chamado. |
| **ExternalCredential** | `{NamedCredential.externalCredential}` | `<externalCredential>` | Nome API da Credencial Externa associada (se `SecuredEndpoint`). |
| **NetworkConnection** | `{NamedCredential.networkConnection}` | `<networkConnection>` | Conexão de rede / Private Link / Outbound Network Connection (se aplicável). |

---

## 2. Opções de Callout e Cabeçalhos Personalizados (`<calloutOptions>` & `<customHeaders>`)

| Propriedade / Cabeçalho | Configuração | Tag / Fonte XML | Impacto de Segurança / Comportamento |
|---|---|---|---|
| **Generate Authorization Header** | `true` \| `false` | `<generateAuthorizationHeader>` | Insere automaticamente o cabeçalho `Authorization` HTTP na requisição. |
| **Allow Merge Fields in Header** | `true` \| `false` | `<allowMergeFieldsInHeader>` | Permite o uso de campos de mesclagem (ex: `{!$Credential.CustomHeader}`) nos cabeçalhos. |
| **Allow Merge Fields in Body** | `true` \| `false` | `<allowMergeFieldsInBody>` | Permite o uso de campos de mesclagem no corpo (*body*) da requisição Apex/Flow. |

### Cabeçalhos Personalizados Fixos (`<customHeaders>`)

| Nome do Cabeçalho (`headerName`) | Valor / Campo de Mesclagem (`headerValue`) | Sequência (`sequence`) | Fonte |
|---|---|---|---|
| `Content-Type` | `application/json` | `1` | XML (`<customHeaders>`) |
| `x-api-key` | `{!$Credential.AWS_External_Cred.api_key}` | `2` | XML (`<customHeaders>`) |

---

## 3. Configuração da Credencial Externa (`ExternalCredential`)

*Utilizado quando `NamedCredentialType = SecuredEndpoint`.*

### 3.1. Identificação e Protocolo de Autenticação

| Propriedade | Valor | Tag / Fonte XML | Descrição |
|---|---|---|---|
| **External Credential ApiName** | `{ExternalCredential.fullName}` | `<fullName>` | Nome API da credencial de autenticação. |
| **AuthenticationProtocol** | `Oauth` \| `AwsSv4` \| `Basic` \| `ApiKey` \| `Custom` \| `Jwt` \| `NoAuthentication` | `<authenticationProtocol>` | Protocolo de segurança exigido pelo servidor remoto. |
| **AuthenticationFlowType** | `ClientCredentials` \| `JwtBearer` \| `AuthorizationCode` \| `None` | `<authenticationFlowType>` | Fluxo específico de concessão de credencial. |

### 3.2. Parâmetros da Credencial Externa (`<externalCredentialParameters>`)

| Nome do Parâmetro (`parameterName`) | Tipo do Parâmetro (`parameterType`) | Valor (`parameterValue`) | Descrição / Uso | Fonte |
|---|---|---|---|---|
| `AuthProvider` | `AuthProvider` | `AWS_OIDC_Provider` | Auth Provider configurado no Setup. | XML |
| `Scope` | `AuthHeader` | `read write orders` | Escopos OAuth solicitados no handshake. | XML |
| `AWS_Region` | `AuthHeader` | `us-east-1` | Região da AWS (para `AwsSv4`). | XML |
| `AWS_Service` | `AuthHeader` | `s3` \| `execute-api` | Serviço de destino na AWS. | XML |

---

## 4. Principais e Controle de Acesso (`<principals>` & Permission Sets)

Mapeamento de quem pode utilizar esta Named Credential e como as credenciais são associadas aos usuários:

| Nome do Principal (`principalName`) | Tipo (`principalType`) | Sequência (`sequence`) | Conjuntos de Permissão Associados (`Permission Sets`) | Mapeamento de Usuário | Fonte |
|---|---|---|---|---|---|
| `AWS_Integration_Principal` | `NamedPrincipal` | `1` | `PS_AWS_Integration_User` | Único para a Org inteira (*Named Principal*). | XML / Setup |
| `User_Per_User_Principal` | `PerUserPrincipal` | `2` | `PS_Sales_Users_Integration` | Individual por Usuário (*Per User Authentication*). | XML / Setup |

---

## 5. Instruções de Invocação e Uso no Código (Apex e Flow)

### 5.1. Sintaxe de Chamada Apex (`HttpRequest`)
A chamada utiliza o prefixo `callout:` seguido pelo Nome API da Named Credential e o caminho relativo (*endpoint path*):

```apex
HttpRequest req = new HttpRequest();
// Sintaxe: callout:Nome_Da_Named_Credential/caminho_relativo
req.setEndpoint('callout:AWS_Order_Named_Cred/v1/orders');
req.setMethod('POST');
req.setHeader('Content-Type', 'application/json');
req.setBody('{"orderId": "12345"}');

Http http = new Http();
HttpResponse res = http.send(req);
```

### 5.2. Uso em Flows (HTTP Callout / External Services)
* **Named Credential Selecionada no Flow:** `AWS_Order_Named_Cred`
* **URL Relativa:** `/v1/orders`
* **Método HTTP:** `POST`

---

# 🤖 JSON Schema para Preenchimento Automático pelo Utilitário

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) que faz o parse dos arquivos `.namedCredential-meta.xml` e `.externalCredential-meta.xml`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceNamedCredentialDocumentation",
  "type": "object",
  "properties": {
    "named_credential": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "namedCredentialType": { "type": "string", "enum": ["SecuredEndpoint", "Legacy"] },
        "endpoint": { "type": "string" },
        "externalCredential": { "type": "string" },
        "networkConnection": { "type": "string" },
        "calloutOptions": {
          "type": "object",
          "properties": {
            "generateAuthorizationHeader": { "type": "boolean" },
            "allowMergeFieldsInHeader": { "type": "boolean" },
            "allowMergeFieldsInBody": { "type": "boolean" }
          }
        },
        "customHeaders": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "headerName": { "type": "string" },
              "headerValue": { "type": "string" },
              "sequence": { "type": "integer" }
            }
          }
        }
      },
      "required": ["developerName", "label", "endpoint"]
    },
    "external_credential": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "authenticationProtocol": { 
          "type": "string", 
          "enum": ["Oauth", "AwsSv4", "Basic", "ApiKey", "Custom", "Jwt", "NoAuthentication"] 
        },
        "authenticationFlowType": { "type": "string" },
        "parameters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "parameterName": { "type": "string" },
              "parameterType": { "type": "string" },
              "parameterValue": { "type": "string" }
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
              "sequence": { "type": "integer" }
            }
          }
        }
      }
    },
    "access_control": {
      "type": "object",
      "properties": {
        "permissionSets": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["named_credential"]
}
```

---

### 💡 Vantagens deste Modelo para o seu Robô/Agente:

1. **Cobertura da Arquitetura Moderna (Secured Endpoint):** Mapeia a separação nativa do Salesforce entre a **Named Credential** (endereço/callout options) e a **External Credential** (protocolo/autenticação/principais).
2. **Explicitação de Cabeçalhos e Merge Fields:** Captura se o código pode injetar valores dinâmicos no cabeçalho ou no body (`allowMergeFieldsInHeader` / `allowMergeFieldsInBody`).
3. **Mapeamento de Invocação Apex/Flow:** Já gera o exemplo da linha de código de callout (`callout:Nome_Da_NC/path`) pronto para colar na documentação do sistema.

Deseja montar um modelo semelhante para **External Client App (ECA) / Connected App** ou para **Custom Metadata Types de Integração**?
