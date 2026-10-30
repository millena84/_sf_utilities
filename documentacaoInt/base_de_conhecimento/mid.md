# MID — middleware / MuleSoft

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
| `ApexTrigger` | Código Apex que roda sozinho quando um registro é criado, alterado ou excluído (ou quando chega um evento). |
| `AuthProvider` | Cadastro de um provedor de login externo (OAuth/OpenID), usado para obter tokens ou para login único. |
| `Certificate` | Certificado digital usado para assinar ou proteger conexões. |
| `ConnectedApp` | Cadastro (modelo antigo) de um sistema externo que vai entrar no Salesforce via OAuth. |
| `CustomField` | Campo de um objeto. Um campo External ID serve de chave para casar registros entre sistemas. |
| `CustomLabels` | Textos configuráveis; às vezes guardam URLs ou parâmetros. |
| `CustomMetadata` | Registro de configuração (uma "linha" de um tipo `__mdt`). Vai junto com o código no deploy. |
| `CustomObject` | Objeto (tabela). Sufixos: `__c` customizado, `__x` externo, `__e` evento, `__mdt` tipo de configuração. |
| `CustomTab` | Aba do menu. Pode abrir um objeto, uma página, um componente ou um site externo. |
| `ExternalClientApplication` | Cadastro (modelo novo, recomendado) de um sistema externo que vai entrar no Salesforce via OAuth. |
| `ExternalCredential` | Cadastro de como autenticar em um sistema externo (OAuth, JWT, senha, cabeçalho). Usado pela Named Credential. |
| `ExternalServiceRegistration` | Cadastro de uma API externa a partir do contrato dela (OpenAPI). Vira ações para Flow e classes para Apex. |
| `ExtlClntAppConfigurablePolicies` | Parte do External Client App que liga ou desliga o app na org. |
| `ExtlClntAppGlobalOauthSettings` | Parte do External Client App com client_id, client_secret, certificado e fluxos ligados. |
| `ExtlClntAppOauthConfigurablePolicies` | Parte do External Client App com as regras do admin (quem pode usar, IP, usuário do Client Credentials). |
| `ExtlClntAppOauthSettings` | Parte do External Client App com os escopos (permissões) do token. |
| `FlexiPage` | Página do Lightning montada no App Builder, onde os componentes são posicionados. |
| `Flow` | Automação montada sem código no Flow Builder (com telas, disparada por registro, por agenda ou por evento). |
| `FlowDefinition` | Arquivo antigo que indica qual versão do Flow está ativa. |
| `LightningComponentBundle` | Componente de tela moderno (LWC), feito em JavaScript e HTML. |
| `NamedCredential` | Cadastro do endereço de um sistema externo (e, no modelo novo, a ligação com a autenticação). Quem usa Named Credential não precisa de Remote Site Setting para aquele domínio. |
| `OauthCustomScope` | Escopo OAuth criado pela empresa para limitar o que um token pode fazer. |
| `OmniDataTransform` | Data Mapper (DataRaptor) do OmniStudio: lê, grava ou transforma dados. |
| `OmniIntegrationProcedure` | Integration Procedure do OmniStudio: roteiro de integração montado sem código. |
| `OmniScript` | OmniScript do OmniStudio: processo guiado de várias telas. |
| `OmniUiCard` | FlexCard do OmniStudio: cartão de tela que mostra dados. |
| `PermissionSet` | Conjunto de permissões extras que se dá a um usuário. |
| `PermissionSetGroup` | Grupo de Permission Sets. |
| `PlatformCachePartition` | Memória temporária da plataforma, para guardar dados como tokens. |
| `PlatformEventChannelMember` | Item de um canal de eventos; no CDC, indica qual objeto gera eventos de mudança. |
| `Profile` | Perfil do usuário: conjunto básico de permissões. |
| `QuickAction` | Botão de ação na página do registro, que abre um Flow, um componente ou um formulário. |
| `RemoteSiteSetting` | Lista de domínios externos que o código Apex pode chamar quando a URL **não** vem de uma Named Credential. |

## Índice

- [M.1 — Org → middleware (síncrono ou via Apex assíncrono)](#m1) (24 variantes)
- [M.2 — Middleware assina Platform Event / CDC](#m2) (4 variantes)
- [M.3 — Middleware → org (REST padrão ou Apex REST)](#m3) (8 variantes)
- [M.4 — Middleware → org (Bulk API 2.0)](#m4) (4 variantes)
- [M.5 — Middleware faz polling na org](#m5) (8 variantes)
- [M.6 — Integration Procedure como middleware dentro da org](#m6) (12 variantes)
- [M.7 — API MuleSoft registrada como External Service → Flow ou Apex](#m7) (8 variantes)

## M.1

**Org → middleware (síncrono ou via Apex assíncrono)**

Igual aos desenhos b e D, com o endpoint apontando para o middleware.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [M.1.v1](#m1v1) | Origem LWC · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v2](#m1v2) | Origem LWC · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v3](#m1v3) | Origem LWC · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v4](#m1v4) | Origem LWC · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v5](#m1v5) | Origem LWC · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v6](#m1v6) | Origem LWC · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v7](#m1v7) | Origem Screen Flow · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v8](#m1v8) | Origem Screen Flow · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v9](#m1v9) | Origem Screen Flow · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v10](#m1v10) | Origem Screen Flow · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v11](#m1v11) | Origem Screen Flow · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v12](#m1v12) | Origem Screen Flow · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v13](#m1v13) | Origem Trigger + @future · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v14](#m1v14) | Origem Trigger + @future · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v15](#m1v15) | Origem Trigger + @future · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v16](#m1v16) | Origem Trigger + @future · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v17](#m1v17) | Origem Trigger + @future · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v18](#m1v18) | Origem Trigger + @future · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v19](#m1v19) | Origem Trigger + Queueable · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v20](#m1v20) | Origem Trigger + Queueable · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v21](#m1v21) | Origem Trigger + Queueable · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v22](#m1v22) | Origem Trigger + Queueable · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.1.v23](#m1v23) | Origem Trigger + Queueable · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.1.v24](#m1v24) | Origem Trigger + Queueable · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="m1v1"></a>

### M.1.v1 — Origem LWC · endpoint E1

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v2"></a>

### M.1.v2 — Origem LWC · endpoint E2

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Controller Apex | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v3"></a>

### M.1.v3 — Origem LWC · endpoint E3

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Controller Apex | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v4"></a>

### M.1.v4 — Origem LWC · endpoint E4

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Controller Apex | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v5"></a>

### M.1.v5 — Origem LWC · endpoint E5

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v6"></a>

### M.1.v6 — Origem LWC · endpoint E6

Fluxo principal: Usuário → Componente LWC → Controller Apex → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Controller Apex | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v7"></a>

### M.1.v7 — Origem Screen Flow · endpoint E1

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v8"></a>

### M.1.v8 — Origem Screen Flow · endpoint E2

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe invocável | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v9"></a>

### M.1.v9 — Origem Screen Flow · endpoint E3

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe invocável | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v10"></a>

### M.1.v10 — Origem Screen Flow · endpoint E4

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe invocável | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v11"></a>

### M.1.v11 — Origem Screen Flow · endpoint E5

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v12"></a>

### M.1.v12 — Origem Screen Flow · endpoint E6

Fluxo principal: Usuário → Screen Flow → Classe invocável → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe invocável | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware (ERP, legado etc.) | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v13"></a>

### M.1.v13 — Origem Trigger + @future · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Método @future | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v14"></a>

### M.1.v14 — Origem Trigger + @future · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Método @future | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v15"></a>

### M.1.v15 — Origem Trigger + @future · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Método @future | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v16"></a>

### M.1.v16 — Origem Trigger + @future · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Método @future | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Método @future | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Método @future | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v17"></a>

### M.1.v17 — Origem Trigger + @future · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Método @future | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Método @future | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Método @future | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v18"></a>

### M.1.v18 — Origem Trigger + @future · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Método @future | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v19"></a>

### M.1.v19 — Origem Trigger + Queueable · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v20"></a>

### M.1.v20 — Origem Trigger + Queueable · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Queueable | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v21"></a>

### M.1.v21 — Origem Trigger + Queueable · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v22"></a>

### M.1.v22 — Origem Trigger + Queueable · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 10 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v23"></a>

### M.1.v23 — Origem Trigger + Queueable · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |

<a id="m1v24"></a>

### M.1.v24 — Origem Trigger + Queueable · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → MuleSoft / middleware (Experience/Process/System API) → Sistema de destino final

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Sistema de destino final | não é metadata | ator | chamado pelo middleware | MuleSoft / middleware (Experience/Process/System API) | — | Obrigatório | não aparece no projeto (ator) |


## M.2

**Middleware assina Platform Event / CDC**

O conector do middleware consome eventos via Pub/Sub API.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [M.2.v1](#m2v1) | PE · Connected App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.2.v2](#m2v2) | PE · External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.2.v3](#m2v3) | CDC · Connected App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.2.v4](#m2v4) | CDC · External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="m2v1"></a>

### M.2.v1 — PE · Connected App

Fluxo principal: Pub/Sub API → MuleSoft / middleware (Experience/Process/System API) → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 2 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 3 | Pub/Sub API | não é metadata | ator | entrega os eventos | barramento | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | não aparece no projeto (ator) |
| 4 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | conector Salesforce assina o canal e roteia | — | sistemas de destino | Obrigatório | não aparece no projeto (ator) |
| 5 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 6 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Permission Set (leitura do evento/objeto) | PermissionSet | autoriza | Read no evento ou objeto | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="m2v2"></a>

### M.2.v2 — PE · External Client App

Fluxo principal: Pub/Sub API → MuleSoft / middleware (Experience/Process/System API) → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 2 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 3 | Pub/Sub API | não é metadata | ator | entrega os eventos | barramento | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | não aparece no projeto (ator) |
| 4 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | conector Salesforce assina o canal e roteia | — | sistemas de destino | Obrigatório | não aparece no projeto (ator) |
| 5 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 6 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 7 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 8 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 9 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 10 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 13 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 14 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 15 | Permission Set (leitura do evento/objeto) | PermissionSet | autoriza | Read no evento ou objeto | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="m2v3"></a>

### M.2.v3 — CDC · Connected App

Fluxo principal: Pub/Sub API → MuleSoft / middleware (Experience/Process/System API) → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 2 | Objeto monitorado | CustomObject | lê/referencia | origem | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Pub/Sub API | não é metadata | ator | entrega os eventos | barramento | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | não aparece no projeto (ator) |
| 4 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | conector Salesforce assina o canal e roteia | — | sistemas de destino | Obrigatório | não aparece no projeto (ator) |
| 5 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 6 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Permission Set (leitura do evento/objeto) | PermissionSet | autoriza | Read no evento ou objeto | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="m2v4"></a>

### M.2.v4 — CDC · External Client App

Fluxo principal: Pub/Sub API → MuleSoft / middleware (Experience/Process/System API) → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 2 | Objeto monitorado | CustomObject | lê/referencia | origem | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Pub/Sub API | não é metadata | ator | entrega os eventos | barramento | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | não aparece no projeto (ator) |
| 4 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | conector Salesforce assina o canal e roteia | — | sistemas de destino | Obrigatório | não aparece no projeto (ator) |
| 5 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 6 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 7 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 8 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 9 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 10 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 13 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 14 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 15 | Permission Set (leitura do evento/objeto) | PermissionSet | autoriza | Read no evento ou objeto | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## M.3

**Middleware → org (REST padrão ou Apex REST)**

O middleware chama a org.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [M.3.v1](#m3v1) | Connected App · OAuth 2.0 JWT Bearer · PADRAO | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.3.v2](#m3v2) | Connected App · OAuth 2.0 JWT Bearer · APEXREST | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.3.v3](#m3v3) | Connected App · OAuth 2.0 Client Credentials · PADRAO | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.3.v4](#m3v4) | Connected App · OAuth 2.0 Client Credentials · APEXREST | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.3.v5](#m3v5) | External Client App · OAuth 2.0 JWT Bearer · PADRAO | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.3.v6](#m3v6) | External Client App · OAuth 2.0 JWT Bearer · APEXREST | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.3.v7](#m3v7) | External Client App · OAuth 2.0 Client Credentials · PADRAO | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.3.v8](#m3v8) | External Client App · OAuth 2.0 Client Credentials · APEXREST | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="m3v1"></a>

### M.3.v1 — Connected App · OAuth 2.0 JWT Bearer · PADRAO

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST/Composite API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST/Composite API padrão | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/Composite API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/Composite API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/Composite API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m3v2"></a>

### M.3.v2 — Connected App · OAuth 2.0 JWT Bearer · APEXREST

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → Apex REST → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Apex REST | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 10 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 11 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m3v3"></a>

### M.3.v3 — Connected App · OAuth 2.0 Client Credentials · PADRAO

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST/Composite API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST/Composite API padrão | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/Composite API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/Composite API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/Composite API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m3v4"></a>

### M.3.v4 — Connected App · OAuth 2.0 Client Credentials · APEXREST

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → Apex REST → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m3v5"></a>

### M.3.v5 — External Client App · OAuth 2.0 JWT Bearer · PADRAO

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST/Composite API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST/Composite API padrão | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/Composite API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/Composite API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/Composite API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m3v6"></a>

### M.3.v6 — External Client App · OAuth 2.0 JWT Bearer · APEXREST

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → Apex REST → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | Apex REST | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 14 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 15 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 17 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 19 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 20 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m3v7"></a>

### M.3.v7 — External Client App · OAuth 2.0 Client Credentials · PADRAO

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST/Composite API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST/Composite API padrão | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | REST/Composite API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | REST/Composite API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | REST/Composite API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m3v8"></a>

### M.3.v8 — External Client App · OAuth 2.0 Client Credentials · APEXREST

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → Apex REST → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | `@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classes de serviço / DTO | ApexClass | executa | regra de negócio, desserialização | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | libera a classe Apex REST ao usuário de integração | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## M.4

**Middleware → org (Bulk API 2.0)**

Batch Data Synchronization.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [M.4.v1](#m4v1) | Connected App · OAuth 2.0 JWT Bearer · BULK | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.4.v2](#m4v2) | Connected App · OAuth 2.0 Client Credentials · BULK | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.4.v3](#m4v3) | External Client App · OAuth 2.0 JWT Bearer · BULK | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.4.v4](#m4v4) | External Client App · OAuth 2.0 Client Credentials · BULK | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="m4v1"></a>

### M.4.v1 — Connected App · OAuth 2.0 JWT Bearer · BULK

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Bulk API 2.0 | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m4v2"></a>

### M.4.v2 — Connected App · OAuth 2.0 Client Credentials · BULK

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Bulk API 2.0 | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m4v3"></a>

### M.4.v3 — External Client App · OAuth 2.0 JWT Bearer · BULK

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | Bulk API 2.0 | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="m4v4"></a>

### M.4.v4 — External Client App · OAuth 2.0 Client Credentials · BULK

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | orquestra e chama a org | sistema de origem | Salesforce | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Bulk API 2.0 | não é metadata | ator | endpoint | MuleSoft / middleware (Experience/Process/System API) | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## M.5

**Middleware faz polling na org**

Sem evento; consulta periódica.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [M.5.v1](#m5v1) | Connected App · OAuth 2.0 JWT Bearer · controle por LastModifiedDate | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.5.v2](#m5v2) | Connected App · OAuth 2.0 JWT Bearer · controle por campo customizado | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.5.v3](#m5v3) | Connected App · OAuth 2.0 Client Credentials · controle por LastModifiedDate | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.5.v4](#m5v4) | Connected App · OAuth 2.0 Client Credentials · controle por campo customizado | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.5.v5](#m5v5) | External Client App · OAuth 2.0 JWT Bearer · controle por LastModifiedDate | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.5.v6](#m5v6) | External Client App · OAuth 2.0 JWT Bearer · controle por campo customizado | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.5.v7](#m5v7) | External Client App · OAuth 2.0 Client Credentials · controle por LastModifiedDate | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [M.5.v8](#m5v8) | External Client App · OAuth 2.0 Client Credentials · controle por campo customizado | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="m5v1"></a>

### M.5.v1 — Connected App · OAuth 2.0 JWT Bearer · controle por LastModifiedDate

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST API (query)

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="m5v2"></a>

### M.5.v2 — Connected App · OAuth 2.0 JWT Bearer · controle por campo customizado

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST API (query)

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Campo de controle | CustomField | lê/referencia + executa (DML) | flag/status 'enviado'; o middleware atualiza após processar | MuleSoft / middleware (Experience/Process/System API) | triggers do objeto | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |

<a id="m5v3"></a>

### M.5.v3 — Connected App · OAuth 2.0 Client Credentials · controle por LastModifiedDate

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST API (query)

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="m5v4"></a>

### M.5.v4 — Connected App · OAuth 2.0 Client Credentials · controle por campo customizado

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST API (query)

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Campo de controle | CustomField | lê/referencia + executa (DML) | flag/status 'enviado'; o middleware atualiza após processar | MuleSoft / middleware (Experience/Process/System API) | triggers do objeto | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |

<a id="m5v5"></a>

### M.5.v5 — External Client App · OAuth 2.0 JWT Bearer · controle por LastModifiedDate

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST API (query)

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="m5v6"></a>

### M.5.v6 — External Client App · OAuth 2.0 JWT Bearer · controle por campo customizado

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário de integração → REST API (query)

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 14 | Campo de controle | CustomField | lê/referencia + executa (DML) | flag/status 'enviado'; o middleware atualiza após processar | MuleSoft / middleware (Experience/Process/System API) | triggers do objeto | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |

<a id="m5v7"></a>

### M.5.v7 — External Client App · OAuth 2.0 Client Credentials · controle por LastModifiedDate

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST API (query)

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="m5v8"></a>

### M.5.v8 — External Client App · OAuth 2.0 Client Credentials · controle por campo customizado

Fluxo principal: MuleSoft / middleware (Experience/Process/System API) → Usuário run-as → REST API (query)

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | executa SOQL periodicamente | agenda do middleware | REST API (query) | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | MuleSoft / middleware (Experience/Process/System API) | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (query) | não é metadata | ator | executa a SOQL | MuleSoft / middleware (Experience/Process/System API) | Objeto consultado | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto consultado | CustomObject + CustomField | lê/referencia | dados lidos | REST API | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Campo de controle | CustomField | lê/referencia + executa (DML) | flag/status 'enviado'; o middleware atualiza após processar | MuleSoft / middleware (Experience/Process/System API) | triggers do objeto | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |


## M.6

**Integration Procedure como middleware dentro da org**

Orquestração e transformação sem middleware externo.

> ⚠️ A validar: Metadata types OmniStudio ausentes da lista de Metadata Types (API 68.0) [MA-TYPES]; API Apex de invocação de Integration Procedure não confirmada.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [M.6.v1](#m6v1) | Chamador OMNISCRIPT · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.6.v2](#m6v2) | Chamador OMNISCRIPT · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.6.v3](#m6v3) | Chamador OMNISCRIPT · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.6.v4](#m6v4) | Chamador FLEXCARD · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.6.v5](#m6v5) | Chamador FLEXCARD · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.6.v6](#m6v6) | Chamador FLEXCARD · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.6.v7](#m6v7) | Chamador APEX · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.6.v8](#m6v8) | Chamador APEX · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.6.v9](#m6v9) | Chamador APEX · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [M.6.v10](#m6v10) | Chamador APEXREST · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.6.v11](#m6v11) | Chamador APEXREST · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.6.v12](#m6v12) | Chamador APEXREST · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="m6v1"></a>

### M.6.v1 — Chamador OMNISCRIPT · endpoint E1

Fluxo principal: OmniScript → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | OmniScript | OmniScript | executa | chama a IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | OMNISCRIPT | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v2"></a>

### M.6.v2 — Chamador OMNISCRIPT · endpoint E2

Fluxo principal: OmniScript → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | OmniScript | OmniScript | executa | chama a IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | OMNISCRIPT | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v3"></a>

### M.6.v3 — Chamador OMNISCRIPT · endpoint E3

Fluxo principal: OmniScript → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | OmniScript | OmniScript | executa | chama a IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | OMNISCRIPT | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | URL fixa | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v4"></a>

### M.6.v4 — Chamador FLEXCARD · endpoint E1

Fluxo principal: FlexCard → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | FlexCard | OmniUiCard | executa | fonte de dados IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | FLEXCARD | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v5"></a>

### M.6.v5 — Chamador FLEXCARD · endpoint E2

Fluxo principal: FlexCard → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | FlexCard | OmniUiCard | executa | fonte de dados IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | FLEXCARD | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v6"></a>

### M.6.v6 — Chamador FLEXCARD · endpoint E3

Fluxo principal: FlexCard → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | FlexCard | OmniUiCard | executa | fonte de dados IP | Usuário | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | FLEXCARD | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | URL fixa | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v7"></a>

### M.6.v7 — Chamador APEX · endpoint E1

Fluxo principal: Classe Apex → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | invoca a IP pela API Apex do OmniStudio | trigger/serviço | Integration Procedure | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEX | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v8"></a>

### M.6.v8 — Chamador APEX · endpoint E2

Fluxo principal: Classe Apex → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | invoca a IP pela API Apex do OmniStudio | trigger/serviço | Integration Procedure | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEX | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v9"></a>

### M.6.v9 — Chamador APEX · endpoint E3

Fluxo principal: Classe Apex → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | invoca a IP pela API Apex do OmniStudio | trigger/serviço | Integration Procedure | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEX | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 3 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | URL fixa | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v10"></a>

### M.6.v10 — Chamador APEXREST · endpoint E1

Fluxo principal: Sistema externo → Usuário de integração → Classe Apex REST → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | chama a org | — | Apex REST | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Classe Apex REST | ApexClass | executa | expõe a IP como endpoint | Apex REST | Integration Procedure | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEXREST | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 10 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 11 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 15 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v11"></a>

### M.6.v11 — Chamador APEXREST · endpoint E2

Fluxo principal: Sistema externo → Usuário de integração → Classe Apex REST → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | chama a org | — | Apex REST | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Classe Apex REST | ApexClass | executa | expõe a IP como endpoint | Apex REST | Integration Procedure | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEXREST | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 10 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 11 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 13 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="m6v12"></a>

### M.6.v12 — Chamador APEXREST · endpoint E3

Fluxo principal: Sistema externo → Usuário de integração → Classe Apex REST → Integration Procedure → Data Mapper (Extract/Load/Transform) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | chama a org | — | Apex REST | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Classe Apex REST | ApexClass | executa | expõe a IP como endpoint | Apex REST | Integration Procedure | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra várias chamadas, condições e cache | APEXREST | HTTP Actions / Data Mappers | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 10 | Data Mapper (Extract/Load/Transform) | OmniDataTransform | executa | lê/grava objetos e transforma payloads | Integration Procedure | objetos | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | URL fixa | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |


## M.7

**API MuleSoft registrada como External Service → Flow ou Apex**

A especificação vem do MuleSoft/Anypoint; Flow e Apex chamam as operações geradas.

> Observação: Confirmado [MA-ESR]: `registrationProviderType` = MuleSoft ou Anypoint (API 63.0+).

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [M.7.v1](#m7v1) | Fonte MuleSoft · chamador Flow · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.7.v2](#m7v2) | Fonte MuleSoft · chamador Flow · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.7.v3](#m7v3) | Fonte MuleSoft · chamador Apex · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.7.v4](#m7v4) | Fonte MuleSoft · chamador Apex · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.7.v5](#m7v5) | Fonte Anypoint · chamador Flow · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.7.v6](#m7v6) | Fonte Anypoint · chamador Flow · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.7.v7](#m7v7) | Fonte Anypoint · chamador Apex · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [M.7.v8](#m7v8) | Fonte Anypoint · chamador Apex · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |

<a id="m7v1"></a>

### M.7.v1 — Fonte MuleSoft · chamador Flow · endpoint E1

Fluxo principal: Flow → MuleSoft / middleware (Experience/Process/System API)

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow | Flow | executa | `actionCalls` com `actionType`=externalService | gatilho do Flow | Registro de External Service | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=MuleSoft; operações da API do MuleSoft | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="m7v2"></a>

### M.7.v2 — Fonte MuleSoft · chamador Flow · endpoint E2

Fluxo principal: Flow → MuleSoft / middleware (Experience/Process/System API)

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow | Flow | executa | `actionCalls` com `actionType`=externalService | gatilho do Flow | Registro de External Service | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=MuleSoft; operações da API do MuleSoft | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Registro de External Service | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="m7v3"></a>

### M.7.v3 — Fonte MuleSoft · chamador Apex · endpoint E1

Fluxo principal: Classe Apex → MuleSoft / middleware (Experience/Process/System API)

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | chama `ExternalService.<Servico>` | trigger/serviço/UI | Registro de External Service | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=MuleSoft; operações da API do MuleSoft | Classe Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="m7v4"></a>

### M.7.v4 — Fonte MuleSoft · chamador Apex · endpoint E2

Fluxo principal: Classe Apex → MuleSoft / middleware (Experience/Process/System API)

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | chama `ExternalService.<Servico>` | trigger/serviço/UI | Registro de External Service | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=MuleSoft; operações da API do MuleSoft | Classe Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Registro de External Service | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="m7v5"></a>

### M.7.v5 — Fonte Anypoint · chamador Flow · endpoint E1

Fluxo principal: Flow → MuleSoft / middleware (Experience/Process/System API)

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow | Flow | executa | `actionCalls` com `actionType`=externalService | gatilho do Flow | Registro de External Service | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=Anypoint; operações da API do MuleSoft | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="m7v6"></a>

### M.7.v6 — Fonte Anypoint · chamador Flow · endpoint E2

Fluxo principal: Flow → MuleSoft / middleware (Experience/Process/System API)

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow | Flow | executa | `actionCalls` com `actionType`=externalService | gatilho do Flow | Registro de External Service | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=Anypoint; operações da API do MuleSoft | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Registro de External Service | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="m7v7"></a>

### M.7.v7 — Fonte Anypoint · chamador Apex · endpoint E1

Fluxo principal: Classe Apex → MuleSoft / middleware (Experience/Process/System API)

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | chama `ExternalService.<Servico>` | trigger/serviço/UI | Registro de External Service | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=Anypoint; operações da API do MuleSoft | Classe Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="m7v8"></a>

### M.7.v8 — Fonte Anypoint · chamador Apex · endpoint E2

Fluxo principal: Classe Apex → MuleSoft / middleware (Experience/Process/System API)

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe Apex | ApexClass | executa | chama `ExternalService.<Servico>` | trigger/serviço/UI | Registro de External Service | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Registro de External Service | ExternalServiceRegistration | lê/referencia | `registrationProviderType`=Anypoint; operações da API do MuleSoft | Classe Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Registro de External Service | MuleSoft / middleware (Experience/Process/System API) | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | MuleSoft / middleware (Experience/Process/System API) | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

