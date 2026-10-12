Aqui está o modelo completo e evoluído para **Certificados Digitais (`Certificate`)** no Salesforce, alinhado 1:1 com a **Metadata API (`.certificate-meta.xml`)** e as configurações do *Certificate and Key Management*.

Como dados sensíveis (chaves privadas, senhas de keystore ou tokens secretos) **nunca devem ser documentados nem expostos**, este modelo traz regras explícitas de mascaramento de segurança, documentando apenas os metadados públicos, impressão digital (fingerprint), prazos de validade e associações do certificado.

---

# 📑 Modelo Evoluído: Documentação Técnica de Certificado Digital (DETI - Certificate Module)

---

## 1. Identificação Geral (`Certificate`)

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `{Certificate.fullName}` | `<fullName>` | Nome API do certificado para referência em código e metadados. |
| **MasterLabel** | `{Certificate.label}` | `<masterLabel>` | Rótulo de exibição na interface (*Setup > Certificate and Key Management*). |
| **Tipo de Certificado** | `CA-Signed` \| `Self-Signed` | `<caSigned>` | Define se o certificado foi assinado por uma Autoridade Certificadora (CA) ou se é autoassinado. |
| **Tamanho da Chave (`Key Size`)** | `2048` \| `4096` | `<keySize>` | Tamanho em bits do par de chaves RSA gerado. |
| **Chave Privada Exportável?** | `true` \| `false` | `<privateKeyExportable>` | Indica se a chave privada pode ser baixada/exportada em arquivo JKS/Keystore. |
| **Certificado Criptografado por Senha?** | `true` \| `false` | `<encryptedWithPassword>` | Sinaliza se o arquivo importado foi protegido por senha de keystore. |

---

## 2. Validade, Emissor e Impressão Digital (Public Metadata)

*Nota: Esta seção registra apenas as informações do certificado público (.crt / .pem) para fins de monitoramento e auditoria de expiração.*

| Propriedade de Validação | Valor / Conteúdo | Fonte | Observação de Segurança |
|---|---|---|---|
| **Data de Emissão (*Valid From*)** | `YYYY-MM-DD` | Certificado Público (.crt) | Data inicial de vigência. |
| **Data de Expiração (*Valid To*)** | `YYYY-MM-DD` | Certificado Público (.crt) | **Crítico:** Monitorado para evitar interrupção de serviços/integrações. |
| **Assunto (*Subject / Common Name*)** | `CN=api.suaempresa.com, O=Empresa, C=BR` | Certificado Público (.crt) | Domínio/Entidade a qual o certificado pertence. |
| **Emissor (*Issuer*)** | `DigiCert / Let's Encrypt / Salesforce CA` | Certificado Público (.crt) | Autoridade Certificadora responsável pela validação. |
| **Impressão Digital SHA-256 (*Fingerprint*)** | `A1:B2:C3:...:F9` | Certificado Público (.crt) | Hash único para confirmação da autenticidade da chave pública. |

---

## 3. Diretrizes de Segurança e Mascaramento de Dados Sensíveis

⚠️ **POLÍTICA OBRIGATÓRIA DE SEGURANÇA DE DADOS:**

1. **Chave Privada (*Private Key*):** **NUNCA** deve ser incluída nesta documentação, em logs de sistema, repositórios Git ou arquivos de ticket. A chave privada permanece armazenada e criptografada exclusivamente dentro do HSM (*Hardware Security Module*) do Salesforce.
2. **Tokens de Acesso / Passphrases / Senhas:** **PROIBIDO** armazenar senhas de arquivos JKS/PKCS12 ou tokens secretos em texto plano no documento.
3. **Conteúdo do Certificado Público (`certificateData`):** A string Base64 da **chave pública** pode ser registrada na documentação ou apenas identificada por sua Impressão Digital (*Fingerprint SHA-256*).

---

## 4. Mapeamento de Uso e Associação na Org (Onde é Utilizado)

Mapeamento de todos os componentes da plataforma que dependem deste certificado:

| Tipo de Componente | Nome API do Componente Associado | Finalidade de Uso |
|---|---|---|
| **Named Credential / External Credential** | `AWS_Order_External_Credential` | Assinatura JWT / Autenticação mútua TLS (mTLS) em callouts de saída. |
| **External Client App / Connected App** | `AWS_Integration_ECA` | Validação de chave pública no fluxo OAuth 2.0 JWT Bearer Token (Inbound). |
| **Single Sign-On (SSO / IdP)** | `SamlSsoConfig_AzureAD` | Assinatura e descriptografia de asserções SAML 2.0 para login de usuários. |
| **Identity Provider (IdP Salesforce)** | `Salesforce_IdP_Certificate` | Provedor de identidade para aplicativos externos e portais Experience Cloud. |
| **Autenticação mTLS Apex** | `HttpRequest.setClientCertificateName()` | Chamada REST via código Apex exigindo certificado do cliente. |

---

# 🤖 JSON Schema para Preenchimento Automático pelo Utilitário

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) que faz o parse dos arquivos `.certificate-meta.xml`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceCertificateDocumentation",
  "type": "object",
  "properties": {
    "certificate_metadata": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "caSigned": { "type": "boolean" },
        "keySize": { "type": "integer" },
        "privateKeyExportable": { "type": "boolean" },
        "encryptedWithPassword": { "type": "boolean" }
      },
      "required": ["developerName", "masterLabel", "caSigned", "keySize"]
    },
    "public_certificate_details": {
      "type": "object",
      "properties": {
        "issuer": { "type": "string" },
        "subject": { "type": "string" },
        "expirationDate": { "type": "string", "format": "date" },
        "sha256Fingerprint": { "type": "string" }
      }
    },
    "security_policy": {
      "type": "object",
      "properties": {
        "privateKeyExposed": { "type": "boolean", "enum": [false] },
        "sensitiveTokenMasked": { "type": "boolean", "enum": [true] }
      },
      "required": ["privateKeyExposed", "sensitiveTokenMasked"]
    },
    "associations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "componentType": { "type": "string" },
          "apiName": { "type": "string" },
          "usagePurpose": { "type": "string" }
        }
      }
    }
  },
  "required": ["certificate_metadata", "security_policy"]
}
```

---

### 💡 Destaques deste Modelo para o seu Utilitário:

1. **Garantia de Segurança Integrada:** A propriedade `security_policy` no JSON obriga a checagem de que nenhuma chave privada foi exposta no processo de extração.
2. **Mapeamento de Relacionamentos:** Documenta explicitamente quais *Named Credentials*, *External Client Apps* e configurações de *SSO* consomem este certificado específico.
3. **Controle de Ciclo de Vida:** Foco na data de expiração (`expirationDate`) e na impressão digital pública (`sha256Fingerprint`), permitindo criar rotinas de alerta automático na sua esteira de sustentação antes que um certificado expire.
