# Outras dinâmicas

> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta.

Convenções, legenda e códigos de variante: [README](README.md). Fontes citadas entre colchetes: [fontes_validacao.md](fontes_validacao.md).

## Como ler

- Cada **desenho** (ex.: b.1) começa com um **mapa das variantes**: de onde vem o endereço do sistema externo e se a variante precisa de **Remote Site Setting**.
- **Remote Site Setting só é necessário quando o Apex chama uma URL que não vem de uma Named Credential** (URL fixa no código, em Custom Metadata, Custom Setting ou Custom Label). Com Named Credential (E1, E2, E5), não é preciso [AX-RSS].
- Na tabela de cada variante, a coluna **O que faz nesta integração** explica o papel de cada peça; o glossário abaixo diz o que é cada metadata type.

## O que é cada metadata type

| Metadata type | O que é |
|---|---|
| `ApexClass` | Código Apex (a linguagem de programação do Salesforce) que roda no servidor. |
| `ApexPage` | Página Visualforce: tecnologia antiga de telas do Salesforce. |
| `AuthProvider` | Cadastro de um provedor de login externo (OAuth/OpenID), usado para obter tokens ou para login único. |
| `Certificate` | Certificado digital usado para assinar ou proteger conexões. |
| `ConnectedApp` | Cadastro (modelo antigo) de um sistema externo que vai entrar no Salesforce via OAuth. |
| `CspTrustedSite` | Lista de domínios que o **navegador** pode acessar a partir das páginas do Salesforce (regra CSP). |
| `CustomApplication` | App do Lightning: agrupa abas para um tipo de usuário. |
| `CustomField` | Campo de um objeto. Um campo External ID serve de chave para casar registros entre sistemas. |
| `CustomMetadata` | Registro de configuração (uma "linha" de um tipo `__mdt`). Vai junto com o código no deploy. |
| `CustomObject` | Objeto (tabela). Sufixos: `__c` customizado, `__x` externo, `__e` evento, `__mdt` tipo de configuração. |
| `CustomTab` | Aba do menu. Pode abrir um objeto, uma página, um componente ou um site externo. |
| `ExternalClientApplication` | Cadastro (modelo novo, recomendado) de um sistema externo que vai entrar no Salesforce via OAuth. |
| `ExternalCredential` | Cadastro de como autenticar em um sistema externo (OAuth, JWT, senha, cabeçalho). Usado pela Named Credential. |
| `ExternalDataSource` | Cadastro de uma fonte de dados externa usada pelo Salesforce Connect (dados vistos sem copiar). |
| `ExtlClntAppCanvasSettings` | Parte do External Client App com a configuração de Canvas (sistema externo dentro de uma tela do Salesforce). |
| `FlexiPage` | Página do Lightning montada no App Builder, onde os componentes são posicionados. |
| `Layout` | Layout de página: define campos e botões que aparecem no registro. |
| `LightningComponentBundle` | Componente de tela moderno (LWC), feito em JavaScript e HTML. |
| `NamedCredential` | Cadastro do endereço de um sistema externo (e, no modelo novo, a ligação com a autenticação). Quem usa Named Credential não precisa de Remote Site Setting para aquele domínio. |
| `PermissionSet` | Conjunto de permissões extras que se dá a um usuário. |
| `SamlSsoConfig` | Configuração de login único (SSO) via SAML. |
| `WebLink` | Botão ou link customizado, geralmente para abrir uma URL. |

## Índice

- [N.1 — Org ↔ org](#n1) (4 variantes)
- [N.2 — Integração de UI](#n2) (6 variantes)
- [N.3 — Identidade (SSO)](#n3) (3 variantes)
- [N.4 — Data Cloud](#n4) (1 variantes)

## N.1

**Org ↔ org**

Integração entre orgs Salesforce.

> ⚠️ A validar: Salesforce to Salesforce (legado) não incluído: verificar se há metadata associada.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [N.1.v1](#n1v1) | Salesforce Connect cross-org | Não | o Salesforce Connect usa a External Data Source |
| [N.1.v2](#n1v2) | Apex REST org→org · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [N.1.v3](#n1v3) | Apex REST org→org · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [N.1.v4](#n1v4) | Apex REST org→org · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |

<a id="n1v1"></a>

### N.1.v1 — Salesforce Connect cross-org

Fluxo principal: Usuário → Org Salesforce remota

Remote Site Setting: **Não** — o Salesforce Connect usa a External Data Source.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | External Object | CustomObject (__x) | lê/referencia | objetos da org remota | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 3 | External Data Source (cross-org) | ExternalDataSource | lê/referencia | URL e identidade da org remota | External Object | Org remota | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 4 | Permission Set | PermissionSet | autoriza | acesso ao External Object | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 5 | Org Salesforce remota | não é metadata | ator | responde às consultas via API | External Data Source | — | Obrigatório | não aparece no projeto (ator) |

<a id="n1v2"></a>

### N.1.v2 — Apex REST org→org · endpoint E1

Fluxo principal: Classe cliente (org A) → Org B

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe cliente (org A) | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Org B | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Org B | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente (org A) | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |
| 8 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) | C11 `@RestResource(urlMapping=...)` |

<a id="n1v3"></a>

### N.1.v3 — Apex REST org→org · endpoint E2

Fluxo principal: Classe cliente (org A) → Org B

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe cliente (org A) | Org B | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 4 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 5 | Org B | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente (org A) | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |
| 7 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) | C11 `@RestResource(urlMapping=...)` |

<a id="n1v4"></a>

### N.1.v4 — Apex REST org→org · endpoint E5

Fluxo principal: Classe cliente (org A) → Org B

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe cliente (org A) | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe cliente (org A) | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe cliente (org A) | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Org B | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Org B | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente (org A) | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |
| 9 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) | C11 `@RestResource(urlMapping=...)` |


## N.2

**Integração de UI**

O usuário vê ou usa outro sistema; pouca ou nenhuma troca de dados no servidor.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [N.2.v1](#n2v1) | Botão/link de URL | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [N.2.v2](#n2v2) | Web Tab | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [N.2.v3](#n2v3) | Canvas em Visualforce | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [N.2.v4](#n2v4) | Canvas em Lightning Page | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [N.2.v5](#n2v5) | Canvas via External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [N.2.v6](#n2v6) | iframe em LWC | Não | a chamada sai do navegador; quem libera é o CSP Trusted Site |

<a id="n2v1"></a>

### N.2.v1 — Botão/link de URL

Fluxo principal: Usuário → Botão ou link → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Botão ou link | WebLink | executa | abre o sistema externo com parâmetros do registro na URL | Usuário | Sistema externo | Obrigatório | `objects (dentro do objeto)/*` — `linkType` (url, page, javascript), `url`, `openType`, `page` [MA-WL] |
| 3 | Layout | Layout | lê/referencia | expõe o botão | plataforma | — | Obrigatório | `layouts/*.layout (nv)` — botões/ações e campos exibidos [MA-LAY] |
| 4 | Sistema externo | não é metadata | ator | abre no navegador | WebLink | — | Obrigatório | não aparece no projeto (ator) |

<a id="n2v2"></a>

### N.2.v2 — Web Tab

Fluxo principal: Usuário → Aba web → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Aba web | CustomTab | executa | carrega a URL externa | Usuário | Sistema externo | Obrigatório | `tabs/*.tab` — `url` (Web Tab), `page`, `lwcComponent`, `flexiPage`, `auraComponent` [MA-TAB] |
| 3 | App | CustomApplication | lê/referencia | inclui a aba | plataforma | — | Obrigatório | `applications/*.app` — app que agrupa abas [MA-CAPP] |
| 4 | Sistema externo | não é metadata | ator | exibido em frame | CustomTab | — | Obrigatório | não aparece no projeto (ator) |

<a id="n2v3"></a>

### N.2.v3 — Canvas em Visualforce

Fluxo principal: Usuário → Página Visualforce → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Visualforce | ApexPage | executa | `<apex:canvasApp>` | Usuário | Canvas App | Obrigatório | `pages/*.page` — `<apex:canvasApp>`, controller com Continuation [MA-PAGE] |
| 3 | Connected App com Canvas | ConnectedApp | autoriza + lê | URL do Canvas, método de acesso (signed request/OAuth), locais permitidos | host | Sistema externo | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 4 | Sistema externo | não é metadata | ator | app web que recebe o signed request | Canvas | — | Obrigatório | não aparece no projeto (ator) |

<a id="n2v4"></a>

### N.2.v4 — Canvas em Lightning Page

Fluxo principal: Usuário → Página Lightning → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | executa | componente padrão Canvas App | Usuário | Canvas App | Obrigatório | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Connected App com Canvas | ConnectedApp | autoriza + lê | URL do Canvas, método de acesso (signed request/OAuth), locais permitidos | host | Sistema externo | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 4 | Sistema externo | não é metadata | ator | app web que recebe o signed request | Canvas | — | Obrigatório | não aparece no projeto (ator) |

<a id="n2v5"></a>

### N.2.v5 — Canvas via External Client App

Fluxo principal: Usuário → Página Lightning → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | executa | componente Canvas App | Usuário | Canvas App | Obrigatório | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | External Client App | ExternalClientApplication | autoriza | app registrado | host | — | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 4 | Configuração Canvas do app | ExtlClntAppCanvasSettings | autoriza + lê | URL e acesso do Canvas (API 66.0+) | External Client App | Sistema externo | Obrigatório | `extlClntAppCanvasSettings/*.ecaCanvas` — configuração de Canvas do External Client App [MA-ECAC] |
| 5 | Sistema externo | não é metadata | ator | app web | Canvas | — | Obrigatório | não aparece no projeto (ator) |

<a id="n2v6"></a>

### N.2.v6 — iframe em LWC

Fluxo principal: Usuário → Componente LWC → Sistema externo

Remote Site Setting: **Não** — a chamada sai do navegador; quem libera é o CSP Trusted Site.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Componente LWC | LightningComponentBundle | executa | renderiza `<iframe>` | Página | Sistema externo | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 3 | CSP Trusted Site | CspTrustedSite | autoriza | libera o domínio em `frame-src` | navegador | — | Obrigatório | `cspTrustedSites/*.cspTrustedSite` — `endpointUrl`, `context` (All, LEX, Communities, VisualForce...), `isActive`, `isApplicableToConnectSrc`, `isApplicableToFrameSrc`, `isApplicableToImgSrc` [MA-CSP] |
| 4 | Sistema externo | não é metadata | ator | precisa permitir ser emoldurado (X-Frame-Options/CSP) | LWC | — | Obrigatório | não aparece no projeto (ator) |


## N.3

**Identidade (SSO)**

Integra o login, não os dados.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [N.3.v1](#n3v1) | SAML com IdP externo | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [N.3.v2](#n3v2) | OpenID Connect via Auth Provider | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [N.3.v3](#n3v3) | Salesforce como IdP | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="n3v1"></a>

### N.3.v1 — SAML com IdP externo

Fluxo principal: IdP externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | IdP externo | não é metadata | ator | autentica o usuário | Usuário | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Configuração SAML | SamlSsoConfig | autoriza | emissor, certificado, mapeamento de identidade | IdP | — | Obrigatório | `samlssoconfigs/*.samlssoconfig` — emissor, certificado e mapeamento de identidade [MA-SAML] |
| 3 | Certificate | Certificate | autoriza | valida/assina asserções | SAML | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |

<a id="n3v2"></a>

### N.3.v2 — OpenID Connect via Auth Provider

Fluxo principal: Provedor externo → Registration Handler

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Provedor externo | não é metadata | ator | autentica | Usuário | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Auth Provider | AuthProvider | autoriza | configuração OIDC | login | Registration Handler | Obrigatório | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 3 | Registration Handler | ApexClass | executa | cria/atualiza o usuário a partir dos dados do provedor | Auth Provider | User | Obrigatório | AuthProvider.`registrationHandler`; classe implementa `Auth.RegistrationHandler` |

<a id="n3v3"></a>

### N.3.v3 — Salesforce como IdP

Fluxo principal: App externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | App externo | não é metadata | ator | pede login | Usuário | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App (SAML/OIDC) | ConnectedApp | autoriza | app de serviço; Salesforce emite asserção/token | App externo | — | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |


## N.4

**Data Cloud**

Ingestão e ativação de dados.

> ⚠️ A validar: Toda a família de metadata do Data Cloud.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [N.4.v1](#n4v1) | A validar | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="n4v1"></a>

### N.4.v1 — A validar

Fluxo principal: Data Cloud

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Data Cloud | não é metadata | ator | metadata types de data streams, data sources e ativações a confirmar | — | — | Obrigatório | não aparece no projeto (ator) |

