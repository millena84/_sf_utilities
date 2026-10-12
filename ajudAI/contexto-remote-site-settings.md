Aqui está o modelo completo e evoluído de documentação para **Remote Site Settings (`RemoteSiteSetting`)**, alinhado 1:1 com a **Metadata API do Salesforce (`.remoteSite-meta.xml`)**, pronto para ser extraído e preenchido por utilitários autômatos ou agentes de IA.

---

# 📑 Modelo Evoluído: Documentação Técnica de Remote Site Setting (DETI - Remote Site Setting Module)

---

## 1. Identificação Geral (`RemoteSiteSetting`)

| Propriedade | Valor | Tag / Fonte XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `{RemoteSiteSetting.fullName}` | `<fullName>` | Nome API exclusivo do site remoto no repositório de metadados. |
| **MasterLabel / Site Name** | `{RemoteSiteSetting.fullName}` | `<fullName>` | Nome de exibição na interface do Setup (*Setup > Remote Site Settings*). |
| **Remote Site URL** | `https://api.servidorexterno.com` | `<url>` | URL base ou domínio externo liberado no firewall do Salesforce para *callouts*. |
| **Status (`IsActive`)** | `true` \| `false` | `<isActive>` | Define se a liberação de rede está ativa ou temporariamente suspensa. |
| **Disable Protocol Security** | `true` \| `false` | `<disableProtocolSecurity>` | Permite requisições HTTP desprotegidas (geralmente usado apenas para *loopback/localhost* em testes). |
| **Description** | `{RemoteSiteSetting.description}` | `<description>` | Documentação / Finalidade técnica do endpoint liberado. |

---

## 2. Regras de Validação de Rede e Segurança

| Regra / Parâmetro | Valor Configurado | Comportamento na Plataforma | Impacto de Segurança |
|---|---|---|---|
| **Protocolo Requerido** | `HTTPS` (Padrão) \| `HTTP` | O Salesforce exige HTTPS em ambientes de produção. | Garante tráfego criptografado via TLS/SSL na rede. |
| **Correspondência de Porta** | Porta padrão (443) ou específica (ex: `:8443`) | Se a URL incluir porta específica, o *callout* Apex só será permitido exatamente para aquela porta. | Impede que conexões não autorizadas desviem para portas secundárias do servidor. |
| **Segurança de Protocolo (`disableProtocolSecurity`)** | `false` (Recomendado) | Quando `false`, o Salesforce rejeita chamadas HTTP e exige certificado SSL válido no destino. | Evita ataques de *Man-in-the-Middle* e vazamento de dados em trânsito. |

---

## 3. Matriz Arquitetural: Remote Site Setting vs. Named Credential

*Diferenciação clara para governança e decisão de arquitetura:*

| Cenário de Uso | Recomendação | Justificativa Técnica |
|---|---|---|
| **Chamadas com Autenticação (OAuth, Basic, AWS SigV4)** | ❌ **Evitar Remote Site Setting** <br> 🟢 **Usar Named Credential** | O *Remote Site Setting* apenas abre o firewall; ele **não gerencia** senhas, tokens ou rotação de chaves com segurança. |
| **Consumo de APIs Públicas / Sem Autenticação** | 🟢 **Usar Remote Site Setting** | Ideal para serviços abertos (ex: consulta de CEP, cotação de moedas públicas ou tabelas de domínio externas). |
| **URLs Dinâmicas com Múltiplos Subdomínios** | 🟢 **Usar Remote Site Setting** | Permite liberar o domínio base enquanto o código Apex constrói o caminho dinamicamente. |

---

## 4. Invocação em Código Apex e Mapeamento de Dependências

### 4.1. Exemplo de Chamada Apex (`HttpRequest`)
Para que o código Apex consiga realizar um `Http.send()`, a URL configurada no `req.setEndpoint()` deve obrigatoriamente iniciar com o prefixo cadastrado em um **Remote Site Setting** ativo (ou em uma *Named Credential*):

```apex
HttpRequest req = new HttpRequest();
// A URL abaixo DEVE corresponder ao valor da tag <url> do RemoteSiteSetting
req.setEndpoint('https://api.servidorexterno.com/v1/consultar');
req.setMethod('GET');
req.setTimeout(120000); // Timeout máximo de 120 segundos

Http http = new Http();
HttpResponse res = http.send(req);
```

### 4.2. Componentes da Org Dependentes desta Liberação
Mapeamento das classes e fluxos que falharão com erro `System.CalloutException: Unauthorized endpoint` caso este *Remote Site Setting* seja desativado ou removido:

| Tipo do Componente | Nome API do Componente | Classe / Ação Chamadora |
|---|---|---|
| **Apex Class** | `ViaCepIntegrationService` | Método `consultarEndereco(String cep)` |
| **Apex Class** | `AWSFileUploaderService` | Método `uploadToS3Bucket(String fileBody)` |
| **Screen Flow / Autolaunched** | `Flow_Valida_CPF_Externo` | Ação HTTP Callout integrada no fluxo |

---

# 🤖 JSON Schema para Preenchimento Automático pelo Utilitário

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) que faz o parse dos arquivos `.remoteSite-meta.xml`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceRemoteSiteSettingDocumentation",
  "type": "object",
  "properties": {
    "remote_site_setting": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "url": { "type": "string" },
        "isActive": { "type": "boolean" },
        "disableProtocolSecurity": { "type": "boolean" },
        "description": { "type": "string" }
      },
      "required": ["developerName", "url", "isActive"]
    },
    "security_compliance": {
      "type": "object",
      "properties": {
        "isHttps": { "type": "boolean" },
        "hasPortRestriction": { "type": "boolean" },
        "protocolSecurityDisabled": { "type": "boolean" }
      }
    },
    "dependent_components": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "componentType": { "type": "string" },
          "apiName": { "type": "string" },
          "methodOrAction": { "type": "string" }
        }
      }
    }
  },
  "required": ["remote_site_setting"]
}
```

---

### 💡 Destaques deste Modelo para o seu Robô/Agente:

1. **Validação de Firewall Rápida:** Documenta explicitamente a URL exata liberada na tag `<url>`, facilitando a auditoria de quais domínios externos a org Salesforce tem permissão de acessar.
2. **Prevenção de Falhas de Integração (`CalloutException`):** O mapeamento da seção 4 identifica exatamente quais componentes quebram caso o ambiente de Sandbox/UAT não possua o *Remote Site Setting* implantado.
3. **Mapeamento de Conformidade de Criptografia:** Captura se a flag `<disableProtocolSecurity>` foi marcada indevidamente, sinalizando riscos de segurança em varreduras automatizadas de código.
