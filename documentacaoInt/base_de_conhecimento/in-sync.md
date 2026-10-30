# IN SYNC — externo chama o Salesforce e espera

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
| `Certificate` | Certificado digital usado para assinar ou proteger conexões. |
| `ConnectedApp` | Cadastro (modelo antigo) de um sistema externo que vai entrar no Salesforce via OAuth. |
| `CustomField` | Campo de um objeto. Um campo External ID serve de chave para casar registros entre sistemas. |
| `CustomMetadata` | Registro de configuração (uma "linha" de um tipo `__mdt`). Vai junto com o código no deploy. |
| `CustomObject` | Objeto (tabela). Sufixos: `__c` customizado, `__x` externo, `__e` evento, `__mdt` tipo de configuração. |
| `CustomSite` | Site público do Salesforce (pode expor endpoints sem login). |
| `DigitalExperienceBundle` | Conteúdo de um site do Experience Cloud (modelo mais novo). |
| `ExperienceBundle` | Conteúdo de um site do Experience Cloud. |
| `ExternalClientApplication` | Cadastro (modelo novo, recomendado) de um sistema externo que vai entrar no Salesforce via OAuth. |
| `ExtlClntAppConfigurablePolicies` | Parte do External Client App que liga ou desliga o app na org. |
| `ExtlClntAppGlobalOauthSettings` | Parte do External Client App com client_id, client_secret, certificado e fluxos ligados. |
| `ExtlClntAppOauthConfigurablePolicies` | Parte do External Client App com as regras do admin (quem pode usar, IP, usuário do Client Credentials). |
| `ExtlClntAppOauthSettings` | Parte do External Client App com os escopos (permissões) do token. |
| `Flow` | Automação montada sem código no Flow Builder (com telas, disparada por registro, por agenda ou por evento). |
| `Network` | Site do Experience Cloud (portal). |
| `OauthCustomScope` | Escopo OAuth criado pela empresa para limitar o que um token pode fazer. |
| `PermissionSet` | Conjunto de permissões extras que se dá a um usuário. |
| `PermissionSetGroup` | Grupo de Permission Sets. |
| `Profile` | Perfil do usuário: conjunto básico de permissões. |

## Índice

- [g.1 — Sistema externo → REST/SOAP API padrão (CRUD)](#g1) (8 variantes)
- [g.2 — Sistema externo → Composite / sObject Tree / Collections](#g2) (8 variantes)
- [g.3 — Sistema externo → Apex REST customizado](#g3) (8 variantes)
- [g.4 — Sistema externo → Apex SOAP customizado](#g4) (8 variantes)
- [g.5 — Sistema externo → Flow via REST (Actions)](#g5) (8 variantes)
- [g.6 — Webhook público → Site → Apex REST](#g6) (6 variantes)
- [g.7 — Sistema externo → GraphQL API](#g7) (8 variantes)

## g.1

**Sistema externo → REST/SOAP API padrão (CRUD)**

Sem código na org; o sistema externo grava ou lê objetos diretamente.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [g.1.v1](#g1v1) | Connected App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.1.v2](#g1v2) | Connected App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.1.v3](#g1v3) | Connected App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.1.v4](#g1v4) | Connected App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.1.v5](#g1v5) | External Client App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.1.v6](#g1v6) | External Client App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.1.v7](#g1v7) | External Client App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.1.v8](#g1v8) | External Client App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="g1v1"></a>

### g.1.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST/SOAP API padrão. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST/SOAP API padrão | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g1v2"></a>

### g.1.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → REST/SOAP API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST/SOAP API padrão. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST/SOAP API padrão | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g1v3"></a>

### g.1.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST/SOAP API padrão. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Web Server + Refresh Token) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST/SOAP API padrão | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g1v4"></a>

### g.1.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST/SOAP API padrão. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Username-Password (legado, desaconselhado)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST/SOAP API padrão | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g1v5"></a>

### g.1.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST/SOAP API padrão. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST/SOAP API padrão | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g1v6"></a>

### g.1.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → REST/SOAP API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST/SOAP API padrão. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST/SOAP API padrão | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g1v7"></a>

### g.1.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST/SOAP API padrão. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Web Server + Refresh Token. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST/SOAP API padrão | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g1v8"></a>

### g.1.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → REST/SOAP API padrão → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST/SOAP API padrão. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Username-Password (legado, desaconselhado). | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST/SOAP API padrão | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | REST/SOAP API padrão | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | REST/SOAP API padrão | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | REST/SOAP API padrão | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.2

**Sistema externo → Composite / sObject Tree / Collections**

Várias operações em uma chamada.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [g.2.v1](#g2v1) | Connected App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.2.v2](#g2v2) | Connected App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.2.v3](#g2v3) | Connected App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.2.v4](#g2v4) | Connected App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.2.v5](#g2v5) | External Client App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.2.v6](#g2v6) | External Client App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.2.v7](#g2v7) | External Client App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.2.v8](#g2v8) | External Client App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="g2v1"></a>

### g.2.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Composite API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Composite API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g2v2"></a>

### g.2.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → Composite API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Composite API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Composite API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g2v3"></a>

### g.2.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Composite API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Web Server + Refresh Token) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Composite API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g2v4"></a>

### g.2.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Composite API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Username-Password (legado, desaconselhado)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Composite API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g2v5"></a>

### g.2.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Composite API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | Composite API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g2v6"></a>

### g.2.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → Composite API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Composite API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Composite API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g2v7"></a>

### g.2.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Composite API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Web Server + Refresh Token. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Composite API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g2v8"></a>

### g.2.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → Composite API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Composite API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Username-Password (legado, desaconselhado). | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Composite API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Composite API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Composite API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Composite API | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.3

**Sistema externo → Apex REST customizado**

Endpoint próprio com regra de negócio.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [g.3.v1](#g3v1) | Connected App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.3.v2](#g3v2) | Connected App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.3.v3](#g3v3) | Connected App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.3.v4](#g3v4) | Connected App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.3.v5](#g3v5) | External Client App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.3.v6](#g3v6) | External Client App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.3.v7](#g3v7) | External Client App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.3.v8](#g3v8) | External Client App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="g3v1"></a>

### g.3.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST (/services/apexrest). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classe Apex REST | ApexClass | executa | Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio. | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 10 | Classes de serviço / DTO | ApexClass | executa | Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex. | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 11 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g3v2"></a>

### g.3.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST (/services/apexrest). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio. | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classes de serviço / DTO | ApexClass | executa | Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex. | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g3v3"></a>

### g.3.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST (/services/apexrest). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Web Server + Refresh Token) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio. | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classes de serviço / DTO | ApexClass | executa | Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex. | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g3v4"></a>

### g.3.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST (/services/apexrest). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Username-Password (legado, desaconselhado)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio. | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classes de serviço / DTO | ApexClass | executa | Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex. | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g3v5"></a>

### g.3.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST (/services/apexrest). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classe Apex REST | ApexClass | executa | Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio. | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 14 | Classes de serviço / DTO | ApexClass | executa | Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex. | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 15 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 17 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 19 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 20 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g3v6"></a>

### g.3.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST (/services/apexrest). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio. | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classes de serviço / DTO | ApexClass | executa | Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex. | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g3v7"></a>

### g.3.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST (/services/apexrest). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Web Server + Refresh Token. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio. | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classes de serviço / DTO | ApexClass | executa | Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex. | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g3v8"></a>

### g.3.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST (/services/apexrest). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Username-Password (legado, desaconselhado). | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio. | Apex REST (/services/apexrest) | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classes de serviço / DTO | ApexClass | executa | Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex. | Classe Apex REST | Objeto de destino | Opcional | L38 chamada a partir da classe de entrada |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.4

**Sistema externo → Apex SOAP customizado**

Equivalente SOAP com WSDL gerado.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [g.4.v1](#g4v1) | Connected App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.4.v2](#g4v2) | Connected App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.4.v3](#g4v3) | Connected App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.4.v4](#g4v4) | Connected App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.4.v5](#g4v5) | External Client App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.4.v6](#g4v6) | External Client App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.4.v7](#g4v7) | External Client App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.4.v8](#g4v8) | External Client App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="g4v1"></a>

### g.4.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a SOAP API customizada (/services/Soap/class). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 9 | Classe Apex SOAP | ApexClass | executa | Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar. | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 10 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g4v2"></a>

### g.4.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a SOAP API customizada (/services/Soap/class). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 8 | Classe Apex SOAP | ApexClass | executa | Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar. | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 9 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g4v3"></a>

### g.4.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a SOAP API customizada (/services/Soap/class). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Web Server + Refresh Token) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 8 | Classe Apex SOAP | ApexClass | executa | Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar. | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 9 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g4v4"></a>

### g.4.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a SOAP API customizada (/services/Soap/class). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Username-Password (legado, desaconselhado)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 8 | Classe Apex SOAP | ApexClass | executa | Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar. | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 9 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g4v5"></a>

### g.4.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a SOAP API customizada (/services/Soap/class). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 13 | Classe Apex SOAP | ApexClass | executa | Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar. | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 14 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g4v6"></a>

### g.4.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a SOAP API customizada (/services/Soap/class). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 12 | Classe Apex SOAP | ApexClass | executa | Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar. | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 13 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g4v7"></a>

### g.4.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a SOAP API customizada (/services/Soap/class). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Web Server + Refresh Token. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 12 | Classe Apex SOAP | ApexClass | executa | Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar. | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 13 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g4v8"></a>

### g.4.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → SOAP API customizada (/services/Soap/class) → Classe Apex SOAP → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a SOAP API customizada (/services/Soap/class). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Username-Password (legado, desaconselhado). | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | SOAP API customizada (/services/Soap/class) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Classe Apex SOAP | Obrigatório | não aparece no projeto (ator) |
| 12 | Classe Apex SOAP | ApexClass | executa | Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar. | SOAP API customizada (/services/Soap/class) | Objeto de destino | Obrigatório | C12 `global` + `webservice` |
| 13 | Permission Set (acesso à classe) | PermissionSet | autoriza | Dá ao usuário de integração permissão para chamar a classe. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex SOAP | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex SOAP | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex SOAP | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.5

**Sistema externo → Flow via REST (Actions)**

Dispara um autolaunched Flow.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [g.5.v1](#g5v1) | Connected App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.5.v2](#g5v2) | Connected App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.5.v3](#g5v3) | Connected App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.5.v4](#g5v4) | Connected App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.5.v5](#g5v5) | External Client App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.5.v6](#g5v6) | External Client App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.5.v7](#g5v7) | External Client App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.5.v8](#g5v8) | External Client App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="g5v1"></a>

### g.5.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (Actions). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (Actions) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 9 | Flow autolaunched | Flow | executa | Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada. | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 10 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário de integração permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g5v2"></a>

### g.5.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → REST API (Actions) → Flow autolaunched → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (Actions). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (Actions) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 8 | Flow autolaunched | Flow | executa | Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada. | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 9 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário de integração permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g5v3"></a>

### g.5.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (Actions). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Web Server + Refresh Token) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (Actions) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 8 | Flow autolaunched | Flow | executa | Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada. | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 9 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário de integração permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g5v4"></a>

### g.5.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (Actions). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Username-Password (legado, desaconselhado)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (Actions) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 8 | Flow autolaunched | Flow | executa | Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada. | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 9 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário de integração permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g5v5"></a>

### g.5.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (Actions). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | REST API (Actions) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 13 | Flow autolaunched | Flow | executa | Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada. | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 14 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário de integração permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g5v6"></a>

### g.5.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → REST API (Actions) → Flow autolaunched → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (Actions). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (Actions) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 12 | Flow autolaunched | Flow | executa | Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada. | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 13 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário de integração permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g5v7"></a>

### g.5.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (Actions). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Web Server + Refresh Token. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (Actions) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 12 | Flow autolaunched | Flow | executa | Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada. | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 13 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário de integração permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g5v8"></a>

### g.5.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → REST API (Actions) → Flow autolaunched → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (Actions). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Username-Password (legado, desaconselhado). | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (Actions) | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Flow autolaunched | Obrigatório | não aparece no projeto (ator) |
| 12 | Flow autolaunched | Flow | executa | Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada. | REST API (Actions) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 13 | Permission Set (Run Flows / acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário de integração permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow autolaunched | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow autolaunched | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow autolaunched | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.6

**Webhook público → Site → Apex REST**

Sem OAuth: a confiança vem de assinatura/token no payload.

> Observação: Usuário guest tem restrições de compartilhamento e de acesso; avalie o risco antes de usar.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [g.6.v1](#g6v1) | Site público · validação nenhuma (não recomendado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.6.v2](#g6v2) | Site público · validação segredo em Custom Metadata | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.6.v3](#g6v3) | Site público · validação segredo em Custom Setting | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.6.v4](#g6v4) | Experience Cloud · validação nenhuma (não recomendado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.6.v5](#g6v5) | Experience Cloud · validação segredo em Custom Metadata | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.6.v6](#g6v6) | Experience Cloud · validação segredo em Custom Setting | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="g6v1"></a>

### g.6.v1 — Site público · validação nenhuma (não recomendado)

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Avisa sobre um acontecimento enviando um POST (webhook), sem login OAuth. | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site público | CustomSite | lê/referencia | Site público do Salesforce. Permite que o sistema externo chame o endpoint sem fazer login (como usuário convidado/guest). | Sistema externo | Classe Apex REST | Obrigatório | `sites/*.site` — `active`, `guestProfile`, `urlPathPrefix`, `siteType` [MA-SITE] |
| 3 | Perfil guest do site | Profile | autoriza | Perfil do usuário convidado do site: define o que a chamada sem login pode executar e acessar. Deve ser o mínimo possível. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | Classe que recebe o aviso (webhook) do sistema externo, confere se é legítimo e grava os dados ou os coloca numa fila para processar depois. | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 6 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 8 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 9 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g6v2"></a>

### g.6.v2 — Site público · validação segredo em Custom Metadata

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Avisa sobre um acontecimento enviando um POST (webhook), sem login OAuth. | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site público | CustomSite | lê/referencia | Site público do Salesforce. Permite que o sistema externo chame o endpoint sem fazer login (como usuário convidado/guest). | Sistema externo | Classe Apex REST | Obrigatório | `sites/*.site` — `active`, `guestProfile`, `urlPathPrefix`, `siteType` [MA-SITE] |
| 3 | Perfil guest do site | Profile | autoriza | Perfil do usuário convidado do site: define o que a chamada sem login pode executar e acessar. Deve ser o mínimo possível. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | Classe que recebe o aviso (webhook) do sistema externo, confere se é legítimo e grava os dados ou os coloca numa fila para processar depois. | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Registro de Custom Metadata (protegido) | CustomMetadata (+ CustomObject __mdt) | lê/referencia | Guarda o segredo usado para conferir a assinatura do webhook. Atenção: segredo em Custom Metadata é risco (anti-padrão A01). | Classe Apex REST | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 7 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 8 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 9 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g6v3"></a>

### g.6.v3 — Site público · validação segredo em Custom Setting

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Avisa sobre um acontecimento enviando um POST (webhook), sem login OAuth. | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site público | CustomSite | lê/referencia | Site público do Salesforce. Permite que o sistema externo chame o endpoint sem fazer login (como usuário convidado/guest). | Sistema externo | Classe Apex REST | Obrigatório | `sites/*.site` — `active`, `guestProfile`, `urlPathPrefix`, `siteType` [MA-SITE] |
| 3 | Perfil guest do site | Profile | autoriza | Perfil do usuário convidado do site: define o que a chamada sem login pode executar e acessar. Deve ser o mínimo possível. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | Classe que recebe o aviso (webhook) do sistema externo, confere se é legítimo e grava os dados ou os coloca numa fila para processar depois. | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Custom Setting protegido | CustomObject (Custom Setting) | lê/referencia | Guarda o segredo usado para conferir a assinatura do webhook. | Classe Apex REST | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 7 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 8 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 9 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g6v4"></a>

### g.6.v4 — Experience Cloud · validação nenhuma (não recomendado)

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Avisa sobre um acontecimento enviando um POST (webhook), sem login OAuth. | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site Experience Cloud | Network + ExperienceBundle/DigitalExperienceBundle + CustomSite | lê/referencia | Site do Experience Cloud com acesso de convidado (guest), usado para receber a chamada sem login. | Sistema externo | Classe Apex REST | Obrigatório | `networks/*.network` [MA-NET] ou `digitalExperiences/*` [MA-DEB] |
| 3 | Perfil guest do site | Profile | autoriza | Perfil do usuário convidado do site: define o que a chamada sem login pode executar e acessar. Deve ser o mínimo possível. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | Classe que recebe o aviso (webhook) do sistema externo, confere se é legítimo e grava os dados ou os coloca numa fila para processar depois. | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 6 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 8 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 9 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g6v5"></a>

### g.6.v5 — Experience Cloud · validação segredo em Custom Metadata

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Avisa sobre um acontecimento enviando um POST (webhook), sem login OAuth. | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site Experience Cloud | Network + ExperienceBundle/DigitalExperienceBundle + CustomSite | lê/referencia | Site do Experience Cloud com acesso de convidado (guest), usado para receber a chamada sem login. | Sistema externo | Classe Apex REST | Obrigatório | `networks/*.network` [MA-NET] ou `digitalExperiences/*` [MA-DEB] |
| 3 | Perfil guest do site | Profile | autoriza | Perfil do usuário convidado do site: define o que a chamada sem login pode executar e acessar. Deve ser o mínimo possível. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | Classe que recebe o aviso (webhook) do sistema externo, confere se é legítimo e grava os dados ou os coloca numa fila para processar depois. | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Registro de Custom Metadata (protegido) | CustomMetadata (+ CustomObject __mdt) | lê/referencia | Guarda o segredo usado para conferir a assinatura do webhook. Atenção: segredo em Custom Metadata é risco (anti-padrão A01). | Classe Apex REST | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 7 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 8 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 9 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g6v6"></a>

### g.6.v6 — Experience Cloud · validação segredo em Custom Setting

Fluxo principal: Sistema externo → Classe Apex REST → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Avisa sobre um acontecimento enviando um POST (webhook), sem login OAuth. | — | Site | Obrigatório | não aparece no projeto (ator) |
| 2 | Site Experience Cloud | Network + ExperienceBundle/DigitalExperienceBundle + CustomSite | lê/referencia | Site do Experience Cloud com acesso de convidado (guest), usado para receber a chamada sem login. | Sistema externo | Classe Apex REST | Obrigatório | `networks/*.network` [MA-NET] ou `digitalExperiences/*` [MA-DEB] |
| 3 | Perfil guest do site | Profile | autoriza | Perfil do usuário convidado do site: define o que a chamada sem login pode executar e acessar. Deve ser o mínimo possível. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 4 | Classe Apex REST | ApexClass | executa | Classe que recebe o aviso (webhook) do sistema externo, confere se é legítimo e grava os dados ou os coloca numa fila para processar depois. | Site | Objeto de destino | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 5 | Custom Setting protegido | CustomObject (Custom Setting) | lê/referencia | Guarda o segredo usado para conferir a assinatura do webhook. | Classe Apex REST | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Apex REST | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 7 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 8 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Apex REST | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 9 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## g.7

**Sistema externo → GraphQL API**

Consultas de leitura flexíveis.

> ⚠️ A validar: Escopo atual de mutations na GraphQL API do Salesforce.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [g.7.v1](#g7v1) | Connected App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.7.v2](#g7v2) | Connected App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.7.v3](#g7v3) | Connected App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.7.v4](#g7v4) | Connected App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.7.v5](#g7v5) | External Client App · OAuth 2.0 JWT Bearer | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.7.v6](#g7v6) | External Client App · OAuth 2.0 Client Credentials | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.7.v7](#g7v7) | External Client App · OAuth 2.0 Web Server + Refresh Token | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [g.7.v8](#g7v8) | External Client App · OAuth 2.0 Username-Password (legado, desaconselhado) | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="g7v1"></a>

### g.7.v1 — Connected App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a GraphQL API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | GraphQL API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g7v2"></a>

### g.7.v2 — Connected App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → GraphQL API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a GraphQL API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | GraphQL API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g7v3"></a>

### g.7.v3 — Connected App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a GraphQL API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Web Server + Refresh Token) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | GraphQL API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g7v4"></a>

### g.7.v4 — Connected App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a GraphQL API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Username-Password (legado, desaconselhado)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | GraphQL API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g7v5"></a>

### g.7.v5 — External Client App · OAuth 2.0 JWT Bearer

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a GraphQL API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 12 | GraphQL API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g7v6"></a>

### g.7.v6 — External Client App · OAuth 2.0 Client Credentials

Fluxo principal: Sistema externo → Usuário run-as → GraphQL API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a GraphQL API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | GraphQL API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g7v7"></a>

### g.7.v7 — External Client App · OAuth 2.0 Web Server + Refresh Token

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a GraphQL API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Web Server + Refresh Token. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | GraphQL API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="g7v8"></a>

### g.7.v8 — External Client App · OAuth 2.0 Username-Password (legado, desaconselhado)

Fluxo principal: Sistema externo → Usuário de integração → GraphQL API → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a GraphQL API. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Username-Password (legado, desaconselhado). | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | GraphQL API | não é metadata | ator | Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | GraphQL API | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | GraphQL API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

