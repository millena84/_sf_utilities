# Prompt — Network

## 1. Contexto do componente

### 1.1 O que é
`Network` (nome funcional: **Network**, também conhecido como **Community** ou **Experience Cloud Site**) é o metadata type do Salesforce que representa um site digital — ou comunidade — criado com Experience Cloud. O registro `Network` agrupa as configurações de identidade visual, autenticação, perfis de membro, regras de compartilhamento, branding, navegação e publicação de um site externo conectado à org.

Na prática, um `Network`:
- define um domínio/prefixo de URL (`UrlPathPrefix`) sob o qual o site é publicado;
- estabelece o perfil de autenticação (como membros internos, parceiros ou clientes acessam);
- vincula perfis (`Profile`) e permission sets que identificam quem pode ser membro da comunidade;
- referencia um `ExperienceBundle` ou páginas/templates que compõem a experiência visual;
- pode estar ativo (`Active`) ou inativo (`Inactive`), e pode ser publicado/operação distinta da configuração declarada.

### 1.2 Para que serve
- Criar e configurar sites/portais/comunidades para clientes, parceiros, funcionários ou público em geral.
- Controlar quais usuários podem acessar e quais permissões eles têm dentro do site.
- Definir branding, navegação, URL e opções de autoserviço de cada comunidade.
- Suportar cenários de integração onde a Experience Cloud consome dados/objetos do Salesforce Core.
- Viabilizar autenticação externa (SSO, Auth Provider, OAuth, self-registration) em um portal dedicado.

### 1.3 Cenários típicos de uso
- Portal de autoatendimento para clientes (Customer Service).
- Portal de parceiros (Partner Central).
- Intranet/portal de funcionários.
- Site de assistência/help desk.
- Comunidade pública para marketing ou engajamento.
- Integrações que consomem APIs de Experience Cloud ou publicam conteúdo via Site.com/Experience Builder.

### 1.4 Clouds / contextos
- **Experience Cloud** — componente principal; `Network` só faz sentido no contexto de Experience Cloud.
- **Salesforce Core** — os dados expostos na comunidade residem no Core; permissões e compartilhamento são governados por lá.
- **Service Cloud** — portais de suporte ao cliente usam `Network` + casos, artigos de Knowledge.
- **Sales Cloud** — portais de parceiros para pipeline, leads e oportunidades.
- **Data Cloud / Agentforce** — podem alimentar personalização ou ações em Experience Cloud.
- **Marketing Cloud / Engagement** — integrações com portais de engajamento ou landing pages.

> **Nota de edição/licença**: Experience Cloud requer licenciamento específico e permissões (ex.: "Manage Experiences"). A disponibilidade de templates e recursos varia por edição e release.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `Network`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Experience Cloud Site / Network (comunidade) |
| Metadata type exact | `Network` |
| Pasta no projeto SFDX | `networks/` |
| Arquivo padrão | `<apiName>.network-meta.xml` |
| Objeto interno (API padrão) | `Network` |
| Objeto interno (Tooling API) | `Network` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM Network` |
| Acessível por Tooling API | Sim — `SELECT ... FROM Network` |
| Acessível por Apex | Parcial — `Network` é consultável via SOQL; configurações complexas via Tooling/Metadata |
| Acessível por UI | Sim — **Setup → Digital Experiences → All Sites** ou **Experience Workspaces** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Experience Bundle | `ExperienceBundle` (metadata) | Conteúdo estrutural do site (páginas, componentes, branding, navegação). Referenciado ou associado ao `Network`. |
| Custom Site | `Site` (metadata) / objeto `Site` | Configurações de publicação/hosting do site no domínio Salesforce. |
| SiteDotCom / Site.com | `SiteDotCom` | Representação publicada do site (conteúdo visual). |
| Experience Cloud Settings | `ExperienceBundleSettings`, `ExperienceConfig`, `NavigationMenuSet` etc. | Configurações auxiliares de navegação e experiência. |
| Profile (membros) | `Profile` / objeto `Profile` | Define quem pode ser membro da comunidade. |
| Permission Set | `PermissionSet` / objeto `PermissionSet` | Permissões adicionais para membros. |
| Network Member | `NetworkMember` / objeto `NetworkMember` | Associação efetiva de um usuário a uma comunidade. |
| Network Member Group | `NetworkMemberGroup` / objeto `NetworkMemberGroup` | Associação de perfis/permission sets à comunidade. |
| Sharing Set | `SharingSet` (metadata) / objeto `SharingSet` | Regras de compartilhamento de registros para usuários externos da comunidade. |
| Sharing Set Access | `SharingSetAccess` (metadata) | Permission Set/Profile com acesso ao Sharing Set. |
| Auth. Provider / SSO | `AuthProvider`, `SamlSsoConfig` | Autenticação externa de membros. |
| Self-Registration | configuração no `Network` / `Site` | Permite que usuários externos se auto-registrem. |
| Branding Set | `BrandingSet` (metadata) | Tema visual do site. |
| Custom Theme Layout | `CommunityThemeDefinition` / `ExperienceBundle` | Layouts e temas. |
| Reputation / topics / CMS | `ReputationLevel`, `ReputationPointsRule`, `Topic`, `CMSConnectSource` | Recursos opcionais de gamificação, tópicos e CMS. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações na configuração do Network. |

### 2.3 Matriz de acessibilidade

| Fonte | Network metadata | `Network` (SOQL) | `Network` (Tooling) | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | Sim (`Name`) | Sim | Sim | Sim |
| URL Path Prefix | Sim (`urlPathPrefix`) | Sim (`UrlPathPrefix`) | Sim | Sim | Sim |
| Status ativo/inativo | Sim (`status`) | Sim (`Status`) | Sim | Sim | Sim |
| Descrição | Sim (`description`) | Sim (`Description`) | Sim | Sim | Sim |
| Perfis membros | Sim (`networkMemberships`) | via `NetworkMemberGroup` | via `NetworkMemberGroup` | Sim | via `NetworkMember` |
| Self-registration | Sim (`selfRegistration`) | Parcial | Parcial | Sim | Sim |
| Autenticação externa | Sim (`options`) | Parcial | Parcial | Sim | Sim |
| Branding / tema | via `ExperienceBundle`/`BrandingSet` | via lookups | via lookups | Sim | Sim |
| Publicação / publicado | não diretamente no XML | `Status` indica ativo | `Status` | UI | `Site.Status` / `Network.Status` |
| Membros efetivos | não | `NetworkMember` | `NetworkMember` | UI | `NetworkMember` |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`Network`)

Arquivo típico: `networks/<API_Name>.network-meta.xml`.

#### Tags raiz e atributos comuns

| Tag / Atributo | Obrigatória? | Significado prático |
|---|---|---|
| `Network` (root) | Sim | Elemento raiz do metadata type. |
| `xmlns` | Sim | Namespace XML do Metadata API. |
| `fullName` (atributo) / nome do arquivo | Sim | API Name interno. |

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<allowInternalUserLogin>` | 0..1 | Permite que usuários internos façam login na comunidade. |
| `<allowMembersToFlag>` | 0..1 | Permite que membros marquem conteúdo como inapropriado. |
| `<changePasswordEmailTemplate>` | 0..1 | Email template usado para redefinição de senha. |
| `<communityRoles>` | 0..1 | Bloco de papéis da comunidade (owner, admin, etc.). |
| `<description>` | 0..1 | Descrição funcional. |
| `<emailSenderAddress>` | 0..1 | Endereço de email remetente de notificações da comunidade. |
| `<emailSenderName>` | 0..1 | Nome do remetente de emails da comunidade. |
| `<enableApexCDNCaching>` | 0..1 | Habilita cache CDN para recursos Apex/visualforce. |
| `<enableCustomVFErrorPageOverrides>` | 0..1 | Permite páginas de erro Visualforce customizadas. |
| `<enableDirectMessages>` | 0..1 | Habilita mensagens diretas entre membros. |
| `<enableGuestChatter>` | 0..1 | Habilita Chatter para usuários guest. |
| `<enableGuestFileAccess>` | 0..1 | Permite que usuários guest baixem arquivos. |
| `<enableImageOptimizationCDN>` | 0..1 | Habilita otimização de imagens via CDN. |
| `<enableInvitation>` | 0..1 | Permite convite de novos membros. |
| `<enableKnowledgeable>` | 0..1 | Habilita recurso de "knowledgeable people". |
| `<enable_MEMBER_PROFILE_USER>` / `<enableNicknameDisplay>` | 0..1 | Controle de apelidos/perfil de membro. |
| `<enablePrivateMessages>` | 0..1 | Habilita mensagens privadas. |
| `<enableReputation>` | 0..1 | Habilita sistema de reputação. |
| `<enableSiteAsContainer>` | 0..1 | Usa Site.com como container da experiência. |
| `<enableTalkingAboutStats>` | 0..1 | Exibe estatísticas de engajamento. |
| `<enableTopicAssignmentRules>` | 0..1 | Habilita regras automáticas de atribuição de tópicos. |
| `<enableTopicSuggestions>` | 0..1 | Sugere tópicos para posts. |
| `<enableUpDownVoting>` | 0..1 | Habilita votação positiva/negativa em conteúdo. |
| `<forgotPasswordEmailTemplate>` | 0..1 | Email template para "esqueci a senha". |
| `<gatherCustomerSentimentData>` | 0..1 | Coleta dados de sentimento do cliente. |
| `<loginPage>` | 0..1 | Página de login customizada. |
| `<logoutPage>` | 0..1 | Página de logout customizada. |
| `<networkMemberGroups>` | 0..1 | Bloco com perfis/permission sets permitidos como membros. |
| `<networkPageOverrides>` | 0..1 | Páginas de override para home, login, error, etc. |
| `<picassoSite>` | 0..1 | Nome do site Experience Builder associado. |
| `<selfRegistration>` | 0..1 | Configuração de auto-registro de usuários externos. |
| `<sendWelcomeEmail>` | 0..1 | Envia email de boas-vindas para novos membros. |
| `<site>` | 0..1 | Nome do `Site` (Custom Site) vinculado. |
| `<status>` | 1 | Status da comunidade: `Live`, `DownForMaintenance`, `Inactive`, `UnderConstruction`. |
| `<tabs>` | 0..1 | Bloco de abas padrão disponíveis na comunidade. |
| `<urlPathPrefix>` | 0..1 | Prefixo do caminho da URL (`/prefixo`). |
| `<welcomeEmailTemplate>` | 0..1 | Email template de boas-vindas. |

##### Bloco `<networkMemberGroups>`

| Tag | Significado prático |
|---|---|
| `<permissionSet>` | Nome de um Permission Set permitido para membros. |
| `<profile>` | Nome de um Profile permitido para membros. |

##### Bloco `<networkPageOverrides>`

| Tag | Significado prático |
|---|---|
| `<changePasswordPageType>` | Tipo de página de alteração de senha. |
| `<forgotPasswordPageType>` | Tipo de página de esqueci a senha. |
| `<homePageType>` | Tipo da página inicial. |
| `<loginPageType>` | Tipo de página de login. |
| `<selfRegPageType>` | Tipo de página de auto-registro. |

> **Limitação importante**: nem toda configuração visual/branding definida no Experience Builder aparece integralmente no XML de `Network`. Muito do conteúdo visual fica em `ExperienceBundle`, `BrandingSet`, `NavigationMenuSet`, `SiteDotCom` etc.

---

### 3.2 Objeto interno via API padrão: `Network`

`Network` é o objeto real consultável em SOQL/REST/Bulk API.

#### Campos relevantes para entendimento

| Campo | Significado prático |
|---|---|
| `Id` | ID interno da comunidade. |
| `Name` | API Name (DeveloperName/fullName do XML). |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |
| `CreatedById`, `LastModifiedById` | Quem criou/alterou. |
| `Description` | Descrição. |
| `Status` | `Live`, `DownForMaintenance`, `Inactive`, `UnderConstruction`. |
| `UrlPathPrefix` | Prefixo da URL. |
| `SiteId` | Lookup para `Site.Id` (custom site publicado). |
| `EmailSenderAddress`, `EmailSenderName` | Remetente de emails. |
| `WelcomeEmailTemplateId`, `ChangePasswordEmailTemplateId`, `ForgotPasswordEmailTemplateId` | Lookups para `EmailTemplate`. |
| `OptionsAllowInternalUserLogin`, `OptionsEnableDirectMessages` etc. | Flags booleanas de funcionalidades. |
| `MembershipModel` | Modelo de associação de membros. |
| `SelfRegProfileId` | Profile usado no auto-registro. |
| `NamespacePrefix` | Indica pacote gerenciado. |

#### Relação entre objeto e metadata

- `Name` ↔ `<fullName>`.
- `Description` ↔ `<description>`.
- `Status` ↔ `<status>`.
- `UrlPathPrefix` ↔ `<urlPathPrefix>`.
- `SiteId` ↔ `<site>`.
- As opções booleanas do XML (`<enableXxx>`) geralmente mapeiam para campos `OptionsXxx` no objeto.

#### Exemplo de query via API padrão

```sql
SELECT Id, Name, Description, Status, UrlPathPrefix, SiteId,
       EmailSenderAddress, EmailSenderName,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM Network
ORDER BY LastModifiedDate DESC
```

**Filtros úteis**:
- `WHERE Status = 'Live'` — comunidades publicadas/atualmente ativas.
- `WHERE UrlPathPrefix = 'parceiros'` — comunidade específica.
- `WHERE NamespacePrefix = null` — comunidades locais/unmanaged.

**Cuidados com permissões**: usuários comuns não enxergam `Network`. Admins de Experience Cloud/perfis com `View Setup and Configuration` conseguem consultar.

**Paginação**: se houver mais de 200 registros, use `LIMIT`/`OFFSET` ou REST API com `nextRecordsUrl`.

---

### 3.3 Objeto interno via Tooling API: `Network`

Tooling API expõe `Network` com suporte aos campos `Metadata` e `FullName`.

| Campo / funcionalidade | Significado prático |
|---|---|
| `Id` | ID do registro. |
| `FullName` | API Name completo. |
| `DeveloperName` | API Name. |
| `Metadata` | Representação do objeto como estrutura de metadados Tooling. |
| `NamespacePrefix` | Namespace do pacote. |

#### Exemplo de query via Tooling API

```sql
SELECT Id, FullName, DeveloperName, NamespacePrefix, Metadata
FROM Network
WHERE DeveloperName = 'MeuPortalParceiros'
```

**Tratamento**: parse JSON em dict/Python ou `JSON.deserializeUntyped` em Apex.

**Limitações**:
- Tooling API pode ser menos permissiva para comunidades gerenciadas.
- Conteúdo visual/branding não está no `Metadata` de `Network` — está em `ExperienceBundle` etc.

---

### 3.4 Configuração observável em outras fontes

#### Setup / UI

- **Setup → Digital Experiences → All Sites**: lista sites/comunidades, status e ações.
- **Experience Workspaces**: área administrativa de cada comunidade.
- **Builder**: configuração visual, páginas, componentes, branding, navegação.

#### `NetworkMember` / `NetworkMemberGroup`

- `NetworkMember`: associação efetiva de um `User` a uma `Network`.
- `NetworkMemberGroup`: associação de perfis/permission sets à `Network`.

```sql
SELECT Id, MemberId, NetworkId, ParentId
FROM NetworkMemberGroup
WHERE NetworkId IN (SELECT Id FROM Network WHERE Name = 'MeuPortalParceiros')
```

```sql
SELECT Id, MemberId, NetworkId
FROM NetworkMember
WHERE NetworkId IN (SELECT Id FROM Network WHERE Name = 'MeuPortalParceiros')
```

#### `SharingSet` / `SharingSetAccess`

- Controlam quais registros dos objetos do Core são visíveis para usuários externos da comunidade.
- Essencial para governança e segurança de dados expostos.

#### `Site` / `SiteDotCom`

- `Site` (Custom Site) armazena configurações de publicação/domínio.
- `SiteDotCom` é a versão publicada do conteúdo do site.

#### `AuthProvider` / `SamlSsoConfig`

- Configuram login externo/SSO na comunidade.

#### `ApexLog` / `EventLogFile`

- Logs de erro e acesso podem indicar problemas de publicação ou acesso.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Nome/URL/status | XML, SOQL, Tooling, UI | — | Configuração declarada. |
| Conteúdo visual/branding | `ExperienceBundle`, `BrandingSet`, `SiteDotCom` | XML do `Network` | Apenas referências estruturais ficam em `Network`. |
| Membros efetivos | `NetworkMember` | XML | Estado operacional. |
| Grupos de membros permitidos | `NetworkMemberGroup` | XML (apenas nomes em retrieve) | Configuração de associação. |
| Compartilhamento de registros | `SharingSet` / `SharingSetAccess` | XML do `Network` | Regras de segurança separadas. |
| Publicação ativa | `Network.Status`, `Site.Status` | — | Estado efetivo. |
| Histórico de alterações | `SetupAuditTrail` | XML | Rastreabilidade. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ExperienceBundle`

- Contém a estrutura visual real da comunidade (páginas, componentes, configurações de navegação, tema).
- Referenciado ou associado ao `Network`; sem ele, a comunidade não tem experiência renderizável.

### 4.2 `Site` (Custom Site) / `SiteDotCom`

- `Site` controla domínio/publicação; `Network` aponta para ele via `SiteId` / `<site>`.
- `SiteDotCom` é o artefato publicado; importante entender que configuração XML ≠ site publicado.

### 4.3 `Profile` / `PermissionSet` / `NetworkMemberGroup`

- Definem quem pode ser membro.
- Diferenciar: perfil configurado como permitido (`NetworkMemberGroup`) vs. usuário efetivamente membro (`NetworkMember`).

### 4.4 `SharingSet` / `SharingSetAccess`

- Crítico para segurança: determina quais registros o usuário externo vê.
- Deve ser auditado sempre que o `Network` expõe objetos com registros privados.

### 4.5 `AuthProvider` / `SamlSsoConfig`

- Relevante para login externo na comunidade.
- Configurações de SSO devem ser cruzadas com domínio e URLs do site.

### 4.6 `BrandingSet` / `NavigationMenuSet` / `CustomTheme`

- Definem aparência e navegação.
- Mudanças de brand devem ser rastreadas em deploys de Experience Cloud.

### 4.7 `EmailTemplate` / `OrgWideEmailAddress`

- Templates de welcome, forgot password e change password devem existir e ser válidos.
- Remetente de email (`emailSenderAddress`) pode precisar estar verificado.

---

## 5. Consultas e formas de extração

### 5.1 Query via API padrão

#### Networks / Comunidades

```sql
SELECT Id, Name, Description, Status, UrlPathPrefix, SiteId,
       EmailSenderAddress, EmailSenderName,
       CreatedDate, LastModifiedDate, CreatedBy.Name, LastModifiedBy.Name
FROM Network
ORDER BY LastModifiedDate DESC
```

#### Perfis/Permission Sets permitidos na comunidade

```sql
SELECT Id, NetworkId, Network.Name, ParentId, Parent.Name
FROM NetworkMemberGroup
WHERE NetworkId IN (SELECT Id FROM Network WHERE Name = 'MeuPortalParceiros')
```

#### Membros efetivos da comunidade

```sql
SELECT Id, MemberId, Member.Name, NetworkId, Network.Name
FROM NetworkMember
WHERE NetworkId IN (SELECT Id FROM Network WHERE Name = 'MeuPortalParceiros')
```

#### Sharing Sets relacionados

```sql
SELECT Id, Name, Description, NetworkId, Network.Name
FROM SharingSet
WHERE NetworkId IN (SELECT Id FROM Network WHERE Name = 'MeuPortalParceiros')
```

### 5.2 Tooling API / Apex

Exemplo de chamada Tooling REST dentro de Apex:

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint(URL.getOrgDomainUrl().toExternalForm() +
                '/services/data/v59.0/tooling/query/?q=' +
                EncodingUtil.urlEncode(
                    'SELECT Id,FullName,DeveloperName,NamespacePrefix,Metadata FROM Network WHERE DeveloperName = \'MeuPortalParceiros\'',
                    'UTF-8'));
req.setMethod('GET');
req.setHeader('Authorization', 'OAuth ' + UserInfo.getSessionId());
Http http = new Http();
HttpResponse res = http.send(req);
System.debug(res.getBody());
// Tratar JSON: (Map<String,Object>) JSON.deserializeUntyped(res.getBody());
```

> Cuidado: `UserInfo.getSessionId()` funciona em contextos síncronos autorizados; em async/batch pode exigir outro token ou Named Credential.

---

## 6. Boas práticas e pontos de atenção

- **Separar configuração de publicação**: uma `Network` configurada não implica site publicado/operacional; verificar `Status` e `Site`.
- **Auditar membros e permissões**: `NetworkMemberGroup` e `NetworkMember` devem ser revisados para evitar acesso não intencional.
- **Revisar Sharing Sets**: usuários externos só devem ver registros explicitamente compartilhados. Erros de sharing são riscos graves de segurança.
- **Não versionar secrets**: embora `Network` não contenha senhas, templates de email e URLs podem conter informações sensíveis; revisar.
- **Documentar propósito**: preencher `<description>` e manter inventário de cada comunidade.
- **Testar em sandbox**: publicação de Experience Cloud pode se comportar diferente entre ambientes.
- **Atenção a templates de email**: garantir que `EmailTemplate` e remetente existam e estejam válidos.
- **Mapear dependências**: alterações em `Network` podem impactar `ExperienceBundle`, `Site`, `SharingSet`, `AuthProvider`.
- **Pacotes gerenciados**: comunidades de managed packages podem ter campos read-only.
- **Guest User**: se a comunidade permite acesso público, revisar permissões do perfil de Guest User eSharing Sets associados.

---

## 7. Links de referência oficial

- [Salesforce Help — Experience Cloud Sites (Networks)](https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm)
- [Salesforce Developer — Network Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_network.htm)
- [Salesforce Developer — Tooling API Network](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_network.htm)
- [Salesforce Help — Experience Bundle](https://help.salesforce.com/s/articleView?id=sf.exp_builder_bundle.htm)
- [Salesforce Help — Sharing Sets for Experience Cloud](https://help.salesforce.com/s/articleView?id=sf.security_sharing_set.htm)
- [Salesforce Help — Configure Experience Cloud Site Login and Authentication](https://help.salesforce.com/s/articleView?id=sf.networks_authentication.htm)
- [Salesforce Developer — Site Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_site.htm)
