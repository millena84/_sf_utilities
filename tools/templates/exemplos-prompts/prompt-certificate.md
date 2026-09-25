# Prompt — Certificate

## 1. Contexto do componente

### 1.1 O que é
`Certificate` (nome funcional: **Certificate** ou **Certificado**) é um metadata type do Salesforce usado para armazenar certificados digitais X.509. Os certificados são utilizados para assinatura digital, criptografia TLS/SSL, autenticação mútua em integrações, assinatura de tokens JWT, configuração de SAML SSO e validação de identidade entre sistemas.

Na prática, um `Certificate`:
- pode ser gerado pelo próprio Salesforce (self-signed) ou importado de uma autoridade certificadora externa;
- contém chave pública (e privada, quando gerado/importado com chave);
- possui data de expiração crítica para continuidade das integrações;
- é referenciado por `AuthProvider`, `ConnectedApp`, `NamedCredential` e outros componentes;
- pode ser usado para assinar `SOAP`, `REST` e payloads de notificação outbound;
- pode ser gerenciado via `Certificate and Key Management` no Setup.

### 1.2 Para que serve
- Autenticação mútua (mTLS) em chamadas outbound.
- Assinatura e validação em SAML SSO.
- Assinatura de tokens JWT para integrações.
- Criptografia de payloads em integrações.
- Garantia de identidade em comunicações seguras.

### 1.3 Cenários típicos de uso
- Certificado para integração bancária via mTLS.
- Certificado para SSO SAML com IdP corporativo.
- Certificado para assinatura de JWT em callouts Apex.
- Certificado para Connected App de OAuth com certificado.

### 1.4 Clouds / contextos
- **Salesforce Core** — Certificados usados em callouts, SAML, OAuth.
- **Experience Cloud** — SSO para usuários externos.
- **Integração / API** — mTLS e JWT.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `Certificate`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Certificate / Certificado |
| Metadata type exact | `Certificate` |
| Pasta no projeto SFDX | `certificates/` |
| Arquivo padrão | `<apiName>.crt` |
| Objeto interno (API padrão) | `Certificate` |
| Objeto interno (Tooling API) | `Certificate` |
| Acessível por Metadata API | Sim — retrieve/deploy (conteúdo pode ser truncado) |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM Certificate` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `Certificate` é consultável |
| Acessível por UI | Sim — **Setup → Certificate and Key Management** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| AuthProvider | `AuthProvider` | Provedores SAML usam certificado para assinatura/validação. |
| ConnectedApp | `ConnectedApp` | OAuth com certificado usa referência. |
| NamedCredential | `NamedCredential` | mTLS pode usar certificado. |
| ExternalCredential | `ExternalCredential` | Credencial externa pode usar certificado. |
| Apex Crypto | `Crypto.sign()` / `Crypto.signWithCertificate()` | Assinatura JWT com certificado. |
| SamlMobil | `SamlConfig` / AuthProvider | Certificado SAML. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | Certificate metadata | `Certificate` (SOQL) | Tooling | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | `DeveloperName`, `MasterLabel` | Sim | Sim | Sim |
| Validade | Conteúdo PEM parseável | `ExpirationDate` | Sim | Sim | Sim |
| Tipo / algoritmo | Conteúdo PEM | `KeySize`, `Algorithm` | Sim | Sim | Sim |
| Chave privada | Sim (no XML/PEM) | `PrivateKey` (mascarado) | Sim | Sim protegido | Sim |
| Referências de uso | via `AuthProvider`, `ConnectedApp`, `NamedCredential` | queries cruzadas | Sim | Setup | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`Certificate`)

Arquivo típico: `certificates/<API_Name>.crt`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<content>` | 1 | Corpo PEM do certificado (Base64). |
| `<expirationDate>` | 0..1 | Data de expiração (ISO 8601). |
| `<keySize>` | 0..1 | Tamanho da chave. |
| `<masterLabel>` | 1 | Nome amigável. |
| `<privateKey>` | 0..1 | Chave privada associada (geralmente mascarada). |
| `<algorithm>` | 0..1 | Algoritmo usado. |

> **Atenção**: `privateKey` e `content` são informações sensíveis. O conteúdo real pode não ser recuperável via Metadata API por segurança.

### 3.2 Objeto interno via API padrão: `Certificate`

| Campo | Significado prático |
|---|---|
| `Id` | ID do certificado. |
| `DeveloperName` | API Name. |
| `MasterLabel` | Nome amigável. |
| `Algorithm` | Algoritmo (RSA, EC etc.). |
| `KeySize` | Tamanho da chave. |
| `ExpirationDate` | Data de expiração. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, DeveloperName, MasterLabel, Algorithm, KeySize, ExpirationDate,
       CreatedDate, LastModifiedDate
FROM Certificate
ORDER BY ExpirationDate
```

### 3.3 Referências de uso (queries cruzadas)

#### AuthProviders SAML

```sql
SELECT Id, DeveloperName, FriendlyName, ProviderType,
       (SELECT Id FROM AuthProviderSamlAttributes)
FROM AuthProvider
WHERE ProviderType = 'Saml'
```

#### Connected Apps com certificado

```sql
SELECT Id, Name, Certificates
FROM ConnectedApplication
WHERE Certificates != null
```

> **Nota**: dependendo da versão da API, `ConnectedApplication.Certificates` pode não estar disponível. Use Setup ou Metadata API.

#### NamedCredentials com certificado

```sql
SELECT Id, DeveloperName, MasterLabel, AuthProviderId,
       CertificateId, Endpoint
FROM NamedCredential
WHERE CertificateId != null
ORDER BY CertificateId
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Certificate and Key Management.
- Setup → Auth. Providers (provedores SAML).
- Setup → Connected Apps / App Manager.
- Setup → Named Credentials.
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Chave privada | Setup UI (protegido) | Metadata retrieve pode retornar vazio | Material criptográfico sensível. |
| Conteúdo PEM completo | Arquivo `.crt` em alguns cenários | SOQL não retorna conteúdo binário/PEM | Depende de permissões. |
| Certificados managed | UI com namespace | — | Pode não ser editável. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `AuthProvider`

- Provedores SAML usam certificado para assinar ou validar assertions.
- Provedores de integração podem referenciar certificado para JWT.

### 4.2 `ConnectedApp`

- OAuth 2.0 com JWT bearer token usa certificado verificado na conexão.

### 4.3 `NamedCredential`

- Certificado pode ser usado para autenticação mútua (mTLS).

### 4.4 `ExternalCredential`

- Pode referenciar certificado para autenticação em callouts.

### 4.5 `Apex`

- `Crypto.signWithCertificate()` pode assinar payloads com certificado importado.

---

## 5. Consultas e formas de extração

### 5.1 Certificados e validade

```sql
SELECT Id, DeveloperName, MasterLabel, Algorithm, KeySize, ExpirationDate,
       CreatedDate, LastModifiedDate
FROM Certificate
ORDER BY ExpirationDate
```

### 5.2 Named Credentials vinculadas a certificado

```sql
SELECT Id, DeveloperName, MasterLabel, CertificateId, Certificate.MasterLabel,
       Endpoint, AuthProviderId
FROM NamedCredential
WHERE CertificateId != null
ORDER BY Certificate.MasterLabel
```

### 5.3 AuthProviders SAML

```sql
SELECT Id, DeveloperName, FriendlyName, ProviderType
FROM AuthProvider
WHERE ProviderType = 'Saml'
```

### 5.4 Connected Apps com certificado

```sql
SELECT Id, Name, ContactEmail, CreatedDate, LastModifiedDate
FROM ConnectedApplication
ORDER BY Name
```

---

## 6. Boas práticas e pontos de atenção

- **Nunca exponha chaves privadas** ou conteúdo PEM em documentação/repositórios.
- **Monitore datas de expiração** com antecedência (30/60/90 dias).
- **Renove certificados em sandbox primeiro** para validar impacto.
- **Mantenha backup seguro** do material criptográfico fora do Salesforce.
- **Use certificados emitidos por CAs confiáveis** para produção (evite self-signed).
- **Documente cada certificado**: finalidade, sistema externo, responsável, data de renovação.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Verifique dependências** antes de deletar ou substituir um certificado.

---

## 7. Links de referência oficial

- [Salesforce Help — Certificate and Key Management](https://help.salesforce.com/s/articleView?id=sf.security_certificates_about.htm)
- [Salesforce Developer — Crypto Class](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_classes_resting_crypto.htm)
- [Salesforce Help — Create a Self-Signed Certificate](https://help.salesforce.com/s/articleView?id=sf.security_certificates_create.htm)
- [Salesforce Help — SAML SSO Settings](https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm)
