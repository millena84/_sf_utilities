# Prompt — RemoteSiteSetting

## 1. Contexto do componente

### 1.1 O que é
`RemoteSiteSetting` (nome funcional: **Remote Site Setting**) é um registro de configuração de segurança declarativa que autoriza a plataforma Salesforce a realizar chamadas de saída (callouts) para um domínio/URL externo específico.

Na prática, um Remote Site Setting:
- cadastra um endpoint externo (protocolo + host + porta, opcionalmente caminho) na whitelist de callouts da org;
- não armazena credenciais, tokens ou lógica de autenticação — somente libera o domínio para requisições de saída;
- é pré-requisito para chamadas Apex `HttpRequest` diretas que não utilizem Named Credential;
- pode ser ativado ou desativado (`isActive`) sem remover o registro;
- é considerado mecanismo legado de liberação de callout, sendo substituído progressivamente por `NamedCredential`, que oferece gerenciamento centralizado de endpoint e credenciais.

### 1.2 Para que serve
- Permitir que Apex (`HttpRequest`) e algumas funcionalidades declarativas façam requisições HTTP/HTTPS para URLs externas.
- Controlar, no nível org, quais domínios externos são permitidos para callouts, reduzindo a superfície de ataque de exfiltração de dados.
- Facilitar auditoria de integrações legadas que ainda não adotaram Named Credentials.
- Servir como fallback quando `NamedCredential` não está disponível ou não é suportado pelo componente consumidor.

### 1.3 Cenários típicos de uso
- Integrações antigas com Apex callout usando endpoint literal em vez de `callout:NamedCredential`.
- Serviços externos chamados diretamente por Visualforce, Lightning Component ou LWC envolvendo servidor (embora componentes client-side façam chamadas diretas do browser, não via Remote Site Setting).
- Middleware personalizado, webhooks, APIs de log, validação ou cálculo externos.
- Bibliotecas e pacotes gerenciados (managed packages) que ainda dependem de Remote Site Setting.
- Configurações transitórias de desenvolvimento/teste antes de migrar para Named Credential.
- Chatter / Connect REST e outras APIs que historicamente exigiam o domínio liberado.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível em praticamente todas as edições que suportam Apex callouts e API enabled.
- **Service Cloud / Sales Cloud** — integrações legadas de CTI, middleware de casos, serviços externos de SLA.
- **Experience Cloud** — endpoints de portais parceiros ou serviços externos consumidos por Apex do site.
- **Data Cloud / Agentforce** — preferencialmente usa Named Credential; Remote Site Setting é incomum nesses contextos modernos.
- **Marketing Cloud / Engagement** — conectores legados podem ainda depender de Remote Site Setting para endpoints específicos.

> **Nota de edição/licença**: Remote Site Settings são amplamente disponíveis. A tendência é que novas funcionalidades da plataforma exijam `NamedCredential` em vez de Remote Site Setting para callouts. A existência de muitos Remote Site Settings ativos pode indicar dívida técnica ou integrações não migradas.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `RemoteSiteSetting`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Remote Site Setting |
| Metadata type exact | `RemoteSiteSetting` |
| Pasta no projeto SFDX | `remoteSiteSettings/` |
| Arquivo padrão | `<apiName>.remoteSite-meta.xml` |
| Objeto interno (API padrão) | `RemoteSiteSetting` |
| Objeto interno (Tooling API) | `RemoteSiteSetting` (expõe `Metadata` como blob serializado; `FullName`) |
| Acessível por Metadata API | Sim — retrieve/deploy via `RemoteSiteSetting` type |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM RemoteSiteSetting` |
| Acessível por Tooling API | Sim — `SELECT ... FROM RemoteSiteSetting` |
| Acessível por Apex | Parcial — objeto `RemoteSiteSetting` pode ser consultado via SOQL em contextos autorizados, mas é mais comum inspecionar via Tooling REST ou Metadata API |
| Acessível por UI | Sim — **Setup → Security → Remote Site Settings** |

> **Atenção**: Remote Site Setting contém apenas URL e flag de ativação; não há segredos, tokens ou credenciais.

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Named Credential | `NamedCredential` (metadata / objeto: `NamedCredential`) | Mecanismo moderno preferido: centraliza endpoint, autenticação e callout options. Substituto natural de Remote Site Setting. |
| Apex Class | `ApexClass` (metadata) / objeto `ApexClass` | Consome o domínio liberado via `HttpRequest.setEndpoint('https://dominio/...')`. |
| Apex Trigger / Async Apex | `ApexTrigger`, `AsyncApexJob`, `ApexLog` | Podem disparar callouts que dependem do Remote Site Setting. |
| Visualforce Page / Component | `ApexPage`, `ApexComponent` | Pode conter callouts Apex server-side para domínios liberados. |
| Lightning / LWC | `AuraDefinitionBundle`, `LightningComponentBundle` | Componentes server-side (Apex controller) podem usar endpoints liberados. |
| External Service Registration | `ExternalServiceRegistration` | Pode referenciar endpoints externos; em geral usa Named Credential, mas domínios também devem estar acessíveis. |
| Workflow Outbound Message | `WorkflowOutboundMessage` / objeto `WorkflowOutboundMessage` | Mensagens outbound dependem de URL acessível; em releases anteriores, poderia depender de Remote Site Setting. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia criação/alteração/deleção de Remote Site Settings. |

### 2.3 Matriz de acessibilidade

| Fonte | RemoteSiteSetting metadata | `RemoteSiteSetting` (SOQL) | `RemoteSiteSetting` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| API Name / fullName | Sim | Sim (`DeveloperName`) | Sim | Sim | Sim |
| Label | Sim | Sim (`MasterLabel`) | Sim | Sim | Sim |
| URL / endpoint | Sim (`url`) | Sim (`EndpointUrl`) | Sim | Sim | Sim |
| Ativo / inativo | Sim (`isActive`) | Sim (`IsActive`) | Sim | Sim | Sim |
| Descrição | Sim (`description`) | Sim (`Description`) | Sim | Sim | Sim |
| Namespace / pacote | via `NamespacePrefix` no retrieve | Sim (`NamespacePrefix`) | Sim | Sim | Sim |
| Histórico de alterações | via `SetupAuditTrail` | Sim | Sim | Sim | Sim |
| Uso efetivo em callouts | não diretamente no metadata | parcial — `ApexLog` pode indicar erros de callout | parcial | não | verificado em código/Apex logs |
| Dependências (quem usa qual domínio) | não | não | não | não | requer busca textual no código/flow |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`RemoteSiteSetting`)

Arquivo típico: `remoteSiteSettings/<API_Name>.remoteSite-meta.xml`.

#### Tags raiz e atributos comuns

| Tag / Atributo | Obrigatória? | Significado prático |
|---|---|---|
| `RemoteSiteSetting` (root) | Sim | Elemento raiz do metadata type. |
| `xmlns` | Sim | Namespace XML do Metadata API (`http://soap.sforce.com/2006/04/metadata`). |
| `fullName` (atributo) / nome do arquivo | Sim | API Name interno. **Não confundir com `<label>`**. |

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<description>` | 0..1 | Descrição funcional/técnica do domínio liberado. Recomenda-se documentar owner, sistema e motivo. |
| `<isActive>` | 0..1 | Indica se o domínio está liberado (`true`) ou bloqueado (`false`) para callouts. |
| `<label>` | 1 | Nome amigável exibido na UI. |
| `<url>` | 1 | URL/Domínio liberado. Pode ser protocolo + host + porta; caminho pode ser ignorado pela plataforma na verificação de domínio. |

#### Exemplo mínimo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<RemoteSiteSetting xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MeuEndpointExterno</fullName>
    <description>Libera endpoint legado do sistema de cobrança</description>
    <isActive>true</isActive>
    <label>Meu Endpoint Externo</label>
    <url>https://api.exemplo.com</url>
</RemoteSiteSetting>
```

#### Observações sobre XML

- O arquivo `.remoteSite-meta.xml` é **simples** e não contém segredos.
- O campo `<url>` deve representar o domínio/protocolo liberado; variações de subdomínio exigem registros separados (a não ser que haja wildcard implícito via configuração de domínio/cors, o que não é função do Remote Site Setting).
- A alteração de `<isActive>` para `false` desativa imediatamente os callouts para aquele domínio sem remover o registro.
- A ausência de um Remote Site Setting ativo causa erro de segurança (`Unauthorized endpoint`) em callouts Apex diretos.
- Remote Site Settings não substituem `CORS` (Cross-Origin Resource Sharing) necessário para chamadas client-side no browser.

---

### 3.2 Objeto interno via API padrão: `RemoteSiteSetting`

`RemoteSiteSetting` é o objeto real consultável em SOQL/REST/Bulk API.

#### Campos relevantes para entendimento

| Campo | Significado prático |
|---|---|
| `Id` | ID interno do registro. |
| `DeveloperName` | API Name (fullName do XML). |
| `MasterLabel` | Nome amigável (`<label>` do XML). |
| `EndpointUrl` | URL/Domínio liberado (`<url>` do XML). |
| `IsActive` | Indica se o domínio está ativo (`<isActive>`). |
| `Description` | Descrição (`<description>`). |
| `NamespacePrefix` | Indica se veio de pacote gerenciado. Vazio é unmanaged/local. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |
| `CreatedById`, `LastModifiedById` | Quem criou/alterou. |

#### Relação entre objeto e metadata

- `DeveloperName` ↔ `<fullName>`.
- `MasterLabel` ↔ `<label>`.
- `EndpointUrl` ↔ `<url>`.
- `IsActive` ↔ `<isActive>`.
- `Description` ↔ `<description>`.

#### Exemplo de query via API padrão

```sql
SELECT Id, DeveloperName, MasterLabel, EndpointUrl,
       IsActive, Description, NamespacePrefix,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM RemoteSiteSetting
ORDER BY LastModifiedDate DESC
```

**O que retorna**: lista de Remote Site Settings cadastrados na org, com status ativo/inativo.

**Filtros úteis**:
- `WHERE IsActive = true` — apenas domínios atualmente liberados.
- `WHERE EndpointUrl LIKE '%exemplo.com%'` — busca por domínio.
- `WHERE NamespacePrefix = null` — configurações locais/unmanaged.
- `WHERE DeveloperName = 'MeuEndpointExterno'` — registro específico.

**Cuidados com permissões**: usuários comuns não enxergam `RemoteSiteSetting`. Admins/perfis com `View Setup and Configuration` conseguem consultar.

**Paginação**: se houver mais de 200 registros, use `LIMIT`/`OFFSET` ou REST API com `nextRecordsUrl`.

---

### 3.3 Objeto interno via Tooling API: `RemoteSiteSetting`

Tooling API expõe `RemoteSiteSetting` com suporte aos campos `Metadata` e `FullName`.

| Campo / funcionalidade | Significado prático |
|---|---|
| `Id` | ID do registro. |
| `FullName` | API Name completo (com namespace). |
| `DeveloperName` | API Name sem namespace. |
| `Metadata` | Representação do objeto como estrutura de metadados Tooling. |
| `NamespacePrefix` | Namespace do pacote. |
| `MasterLabel` | Label. |

#### Exemplo de query via Tooling API

```sql
SELECT Id, FullName, DeveloperName, NamespacePrefix, Metadata
FROM RemoteSiteSetting
WHERE DeveloperName = 'MeuEndpointExterno'
```

**Formato de retorno**: JSON/XML com campo `Metadata` contendo `description`, `isActive`, `label`, `url`.

**Tratamento**:
- Em Python: `requests` + `.json()`; `Metadata` vem como dict.
- Em Apex: callout Tooling REST (`/services/data/vXX.X/tooling/query/?q=...`) e `JSON.deserializeUntyped`.

**Limitações**:
- Tooling API pode ser menos permissiva para retrieve de configurações gerenciadas.
- Não expõe histórico de uso nem dependências.

---

### 3.4 Configuração observável em outras fontes

#### Setup / UI

- **Setup → Security → Remote Site Settings**: lista todos os domínios liberados.
- Ações disponíveis: Edit, Delete, Activate/Deactivate.
- Tela de detalhe exibe URL, descrição e status ativo.

#### `SetupAuditTrail`

```sql
SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section
FROM SetupAuditTrail
WHERE Display LIKE '%RemoteSiteSetting%'
   OR Display LIKE '%Remote Site%'
ORDER BY CreatedDate DESC
LIMIT 200
```

#### `ApexLog` / `EventLogFile`

- Erros do tipo `System.CalloutException: Unauthorized endpoint` indicam tentativa de callout para URL sem Remote Site Setting ativo ou sem Named Credential.
- `EventLogFile` (com licenciamento apropriado) pode registrar callouts externos e URLs de destino.

#### `ApexClass` / `ApexTrigger` / `Flow`

- Para descobrir **quem usa** um domínio, é necessário pesquisa textual no código fonte (ex.: `https://api.exemplo.com`) ou em `Flow` metadata.
- Named Credentials são preferidas para novas integrações porque permitem `callout:ApiName`, facilitando o rastreamento.

#### `NamedCredential`

- Se o mesmo domínio possui Named Credential ativa, o Remote Site Setting pode estar redundante ou em processo de migração.
- Named Credential normalmente elimina a necessidade de Remote Site Setting para o mesmo domínio.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| URL do domínio | XML, SOQL, Tooling, UI | — | Campo público/configurável. |
| Status ativo/inativo | XML, SOQL, Tooling, UI | — | Flag de ativação. |
| Descrição | XML, SOQL, Tooling, UI | — | Documentação livre. |
| Histórico de ativação/desativação | `SetupAuditTrail` | XML em si | Rastreabilidade operacional. |
| Quais callouts usam o domínio | busca textual em Apex/Flow/Logs | `RemoteSiteSetting` | Não há referência inversa nativa. |
| Tráfego/estado de conectividade | `ApexLog`, `EventLogFile` | XML/Metadata/UI estática | Indica uso efetivo. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `NamedCredential`

- Substituto moderno e recomendado para Remote Site Setting quando há necessidade de autenticação e/ou governance centralizada.
- Se uma Named Credential aponta para o mesmo domínio, avaliar desativação do Remote Site Setting (verificando antes que nenhum callout direto dependa dele).
- Named Credential também pode ser usada para liberar o endpoint quando autenticação não é necessária (`NoAuthentication`), eliminando a necessidade de Remote Site Setting.

### 4.2 `ApexClass` / `ApexTrigger` / `ApexPage` / `ApexComponent`

- Indicam onde o domínio liberado é consumido via `HttpRequest`.
- Recomenda-se varrer o repositório por ocorrências do `EndpointUrl` ou por `HttpRequest.setEndpoint` para mapear dependências.
- Em managed packages, o código pode não ser visível; o Remote Site Setting então é parte do pacote.

### 4.3 `WorkflowOutboundMessage`

- Mensagens outbound enviam requisições para endpoints externos. Historicamente, o domínio de destino precisava estar liberado.
- Em orgs modernas, workflow outbound messages ainda podem depender do domínio acessível.

### 4.4 `ExternalServiceRegistration`

- Serviços externos declarativos geralmente usam Named Credential, mas a URL do schema/endpoint deve ser acessível.
- Remote Site Setting pode ser necessário para o domínio do schema em alguns cenários legados.

### 4.5 `AuraDefinitionBundle` / `LightningComponentBundle`

- Chamadas server-side (Apex controllers) podem depender de domínios liberados por Remote Site Setting.
- Chamadas client-side (JavaScript) não dependem de Remote Site Setting, mas sim de CORS e CSP.

### 4.6 `SetupAuditTrail`

- Importante para rastrear criação, alteração e exclusão de Remote Site Settings.
- Ajuda a identificar quem criou domínios liberados e quando.

---

## 5. Consultas e formas de extração

### 5.1 Query via API padrão

#### Remote Site Settings

```sql
SELECT Id, DeveloperName, MasterLabel, EndpointUrl,
       IsActive, Description, NamespacePrefix,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM RemoteSiteSetting
ORDER BY LastModifiedDate DESC
```

#### Domínios ativos

```sql
SELECT Id, DeveloperName, MasterLabel, EndpointUrl, Description
FROM RemoteSiteSetting
WHERE IsActive = true
ORDER BY EndpointUrl
```

#### Registros por domínio

```sql
SELECT Id, DeveloperName, MasterLabel, EndpointUrl, IsActive
FROM RemoteSiteSetting
WHERE EndpointUrl LIKE '%exemplo.com%'
ORDER BY EndpointUrl
```

### 5.2 Tooling API / Apex

Exemplo de chamada Tooling REST dentro de Apex:

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint(URL.getOrgDomainUrl().toExternalForm() +
                '/services/data/v59.0/tooling/query/?q=' +
                EncodingUtil.urlEncode(
                    'SELECT Id,FullName,DeveloperName,NamespacePrefix,Metadata FROM RemoteSiteSetting WHERE DeveloperName = \'MeuEndpointExterno\'',
                    'UTF-8'));
req.setMethod('GET');
req.setHeader('Authorization', 'OAuth ' + UserInfo.getSessionId());
Http http = new Http();
HttpResponse res = http.send(req);
System.debug(res.getBody());
// Tratar JSON: (Map<String,Object>) JSON.deserializeUntyped(res.getBody());
```

**Possíveis saídas**:
- `String` bruto JSON para log/inspeção.
- `Map<String,Object>` parseado para navegação programática.
- CSV/JSON estruturado para integração com ferramenta externa.

> Cuidado: `UserInfo.getSessionId()` funciona em contextos síncronos autorizados; em async/batch pode exigir outro token ou Named Credential.

---

## 6. Boas práticas e pontos de atenção

- **Preferir Named Credential**: Remote Site Setting é legado. Use Named Credential para novas integrações, pois centraliza endpoint, autenticação, permissões e callout options.
- **Documentar a finalidade**: preencher `<description>` com sistema externo, owner e motivo da liberação.
- **Desativar, não deletar**: se for necessário interromper callouts temporariamente, use `isActive = false`; isso mantém rastreabilidade.
- **Auditar periodicamente**: revisar Remote Site Settings ativos e identificar domínios não utilizados, duplicados ou suspeitos.
- **Mapear dependências**: antes de remover um Remote Site Setting, buscar referências em Apex (`HttpRequest.setEndpoint`), Visualforce, Flow, Workflow Outbound Message e managed packages.
- **Não confundir com CORS**: Remote Site Setting é para callouts server-side (Apex). Chamadas client-side do browser exigem configurações de CORS/CSP separadas.
- **Cuidado com URLs amplas**: domínios muito genéricos ou de serviços públicos aumentam a superfície de ataque. Preferir endpoints específicos.
- **Pacotes gerenciados**: Remote Site Settings de pacotes gerenciados podem ser read-only e listados como `NamespacePrefix != null`; remoção pode exigir desinstalação do pacote.
- **Ambientes de sandbox**: Remote Site Settings são metadata e podem ser propagados por deploy; validar se todos os domínios são acessíveis a partir dos sandboxes.
- **Erro típico**: `Unauthorized endpoint` geralmente significa que o domínio não está liberado ou o Remote Site Setting está inativo. Verificar também se o escopo do callout está coberto por uma Named Credential.

---

## 7. Links de referência oficial

- [Salesforce Help — Remote Site Settings](https://help.salesforce.com/s/articleView?id=sf.extend_code_security_remote_settings.htm)
- [Salesforce Developer — RemoteSiteSetting Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_remotesitesetting.htm)
- [Salesforce Developer — Tooling API RemoteSiteSetting](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_remotesitesetting.htm)
- [Salesforce Apex Developer Guide — Making Callouts](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts.htm)
- [Salesforce Apex Developer Guide — Named Credentials](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_named_credentials.htm)
- [Salesforce Help — Named Credentials Overview](https://help.salesforce.com/s/articleView?id=sf.named_credentials_overview.htm)
