# IN ASYNC — externo envia; Salesforce processa depois

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
| `CustomObject` | Objeto (tabela). Sufixos: `__c` customizado, `__x` externo, `__e` evento, `__mdt` tipo de configuração. |
| `EmailServicesFunction` | Endereço de e-mail que, ao receber mensagens, entrega o conteúdo para uma classe Apex. |
| `ExternalClientApplication` | Cadastro (modelo novo, recomendado) de um sistema externo que vai entrar no Salesforce via OAuth. |
| `ExtlClntAppConfigurablePolicies` | Parte do External Client App que liga ou desliga o app na org. |
| `ExtlClntAppGlobalOauthSettings` | Parte do External Client App com client_id, client_secret, certificado e fluxos ligados. |
| `ExtlClntAppOauthConfigurablePolicies` | Parte do External Client App com as regras do admin (quem pode usar, IP, usuário do Client Credentials). |
| `ExtlClntAppOauthSettings` | Parte do External Client App com os escopos (permissões) do token. |
| `Flow` | Automação montada sem código no Flow Builder (com telas, disparada por registro, por agenda ou por evento). |
| `OauthCustomScope` | Escopo OAuth criado pela empresa para limitar o que um token pode fazer. |
| `PermissionSet` | Conjunto de permissões extras que se dá a um usuário. |
| `PermissionSetGroup` | Grupo de Permission Sets. |
| `PlatformEventSubscriberConfig` | Configuração de quem roda o trigger de um evento e quantos eventos por vez. |
| `Profile` | Perfil do usuário: conjunto básico de permissões. |

## Índice

- [H.1 — Sistema externo → Bulk API 2.0](#h1) (12 variantes)
- [H.2 — Sistema externo publica Platform Event → assinante na org](#h2) (16 variantes)
- [H.3 — Apex REST que recebe e enfileira](#h3) (8 variantes)
- [H.4 — E-mail inbound (Email Service)](#h4) (2 variantes)
- [H.5 — Arquivos via ContentVersion](#h5) (8 variantes)

## H.1

**Sistema externo → Bulk API 2.0**

Cargas de grande volume em jobs assíncronos.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [H.1.v1](#h1v1) | Connected App · OAuth 2.0 JWT Bearer · insert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v2](#h1v2) | Connected App · OAuth 2.0 JWT Bearer · upsert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v3](#h1v3) | Connected App · OAuth 2.0 Client Credentials · insert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v4](#h1v4) | Connected App · OAuth 2.0 Client Credentials · upsert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v5](#h1v5) | Connected App · OAuth 2.0 Web Server + Refresh Token · insert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v6](#h1v6) | Connected App · OAuth 2.0 Web Server + Refresh Token · upsert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v7](#h1v7) | External Client App · OAuth 2.0 JWT Bearer · insert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v8](#h1v8) | External Client App · OAuth 2.0 JWT Bearer · upsert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v9](#h1v9) | External Client App · OAuth 2.0 Client Credentials · insert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v10](#h1v10) | External Client App · OAuth 2.0 Client Credentials · upsert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v11](#h1v11) | External Client App · OAuth 2.0 Web Server + Refresh Token · insert | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.1.v12](#h1v12) | External Client App · OAuth 2.0 Web Server + Refresh Token · upsert | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="h1v1"></a>

### H.1.v1 — Connected App · OAuth 2.0 JWT Bearer · insert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v2"></a>

### H.1.v2 — Connected App · OAuth 2.0 JWT Bearer · upsert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 10 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v3"></a>

### H.1.v3 — Connected App · OAuth 2.0 Client Credentials · insert

Fluxo principal: Sistema externo → Usuário run-as → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v4"></a>

### H.1.v4 — Connected App · OAuth 2.0 Client Credentials · upsert

Fluxo principal: Sistema externo → Usuário run-as → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v5"></a>

### H.1.v5 — Connected App · OAuth 2.0 Web Server + Refresh Token · insert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Web Server + Refresh Token) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v6"></a>

### H.1.v6 — Connected App · OAuth 2.0 Web Server + Refresh Token · upsert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Web Server + Refresh Token) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 9 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 11 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 12 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v7"></a>

### H.1.v7 — External Client App · OAuth 2.0 JWT Bearer · insert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
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
| 12 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v8"></a>

### H.1.v8 — External Client App · OAuth 2.0 JWT Bearer · upsert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
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
| 12 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v9"></a>

### H.1.v9 — External Client App · OAuth 2.0 Client Credentials · insert

Fluxo principal: Sistema externo → Usuário run-as → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v10"></a>

### H.1.v10 — External Client App · OAuth 2.0 Client Credentials · upsert

Fluxo principal: Sistema externo → Usuário run-as → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v11"></a>

### H.1.v11 — External Client App · OAuth 2.0 Web Server + Refresh Token · insert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Web Server + Refresh Token. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h1v12"></a>

### H.1.v12 — External Client App · OAuth 2.0 Web Server + Refresh Token · upsert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Bulk API 2.0. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Web Server + Refresh Token. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Bulk API 2.0 | não é metadata | ator | API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano. | Sistema externo | Objeto de destino | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Bulk API 2.0 | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Bulk API 2.0 | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Bulk API 2.0 | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## H.2

**Sistema externo publica Platform Event → assinante na org**

O externo entrega a mensagem; a org processa quando o evento chega.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [H.2.v1](#h2v1) | Connected App · OAuth 2.0 JWT Bearer · publica via REST · assinante APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v2](#h2v2) | Connected App · OAuth 2.0 JWT Bearer · publica via REST · assinante FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v3](#h2v3) | Connected App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v4](#h2v4) | Connected App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v5](#h2v5) | Connected App · OAuth 2.0 Client Credentials · publica via REST · assinante APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v6](#h2v6) | Connected App · OAuth 2.0 Client Credentials · publica via REST · assinante FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v7](#h2v7) | Connected App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v8](#h2v8) | Connected App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v9](#h2v9) | External Client App · OAuth 2.0 JWT Bearer · publica via REST · assinante APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v10](#h2v10) | External Client App · OAuth 2.0 JWT Bearer · publica via REST · assinante FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v11](#h2v11) | External Client App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v12](#h2v12) | External Client App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v13](#h2v13) | External Client App · OAuth 2.0 Client Credentials · publica via REST · assinante APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v14](#h2v14) | External Client App · OAuth 2.0 Client Credentials · publica via REST · assinante FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v15](#h2v15) | External Client App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.2.v16](#h2v16) | External Client App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="h2v1"></a>

### H.2.v1 — Connected App · OAuth 2.0 JWT Bearer · publica via REST · assinante APEX

Fluxo principal: Sistema externo → Usuário de integração → REST API (sObject __e) → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (sObject __e) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 10 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 13 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | Define com qual usuário o trigger roda e quantos eventos processa de uma vez. | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v2"></a>

### H.2.v2 — Connected App · OAuth 2.0 JWT Bearer · publica via REST · assinante FLOW

Fluxo principal: Sistema externo → Usuário de integração → REST API (sObject __e) → Flow disparado por evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (sObject __e) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 10 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Flow disparado por evento | Flow | executa | Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow disparado por evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow disparado por evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow disparado por evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v3"></a>

### H.2.v3 — Connected App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante APEX

Fluxo principal: Sistema externo → Usuário de integração → Pub/Sub API (Publish) → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Pub/Sub API (Publish) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 10 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 13 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | Define com qual usuário o trigger roda e quantos eventos processa de uma vez. | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v4"></a>

### H.2.v4 — Connected App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante FLOW

Fluxo principal: Sistema externo → Usuário de integração → Pub/Sub API (Publish) → Flow disparado por evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Pub/Sub API (Publish) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 10 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Flow disparado por evento | Flow | executa | Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow disparado por evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow disparado por evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow disparado por evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v5"></a>

### H.2.v5 — Connected App · OAuth 2.0 Client Credentials · publica via REST · assinante APEX

Fluxo principal: Sistema externo → Usuário run-as → REST API (sObject __e) → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (sObject __e) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 8 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 9 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 12 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | Define com qual usuário o trigger roda e quantos eventos processa de uma vez. | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v6"></a>

### H.2.v6 — Connected App · OAuth 2.0 Client Credentials · publica via REST · assinante FLOW

Fluxo principal: Sistema externo → Usuário run-as → REST API (sObject __e) → Flow disparado por evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (sObject __e) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 8 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 9 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Flow disparado por evento | Flow | executa | Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow disparado por evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow disparado por evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow disparado por evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v7"></a>

### H.2.v7 — Connected App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante APEX

Fluxo principal: Sistema externo → Usuário run-as → Pub/Sub API (Publish) → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Pub/Sub API (Publish) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 8 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 9 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 12 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | Define com qual usuário o trigger roda e quantos eventos processa de uma vez. | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v8"></a>

### H.2.v8 — Connected App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante FLOW

Fluxo principal: Sistema externo → Usuário run-as → Pub/Sub API (Publish) → Flow disparado por evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Pub/Sub API (Publish) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 8 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 9 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 10 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Flow disparado por evento | Flow | executa | Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow disparado por evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow disparado por evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow disparado por evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v9"></a>

### H.2.v9 — External Client App · OAuth 2.0 JWT Bearer · publica via REST · assinante APEX

Fluxo principal: Sistema externo → Usuário de integração → REST API (sObject __e) → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
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
| 12 | REST API (sObject __e) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 14 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 17 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | Define com qual usuário o trigger roda e quantos eventos processa de uma vez. | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 18 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 19 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 20 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 21 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 22 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v10"></a>

### H.2.v10 — External Client App · OAuth 2.0 JWT Bearer · publica via REST · assinante FLOW

Fluxo principal: Sistema externo → Usuário de integração → REST API (sObject __e) → Flow disparado por evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
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
| 12 | REST API (sObject __e) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 14 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Flow disparado por evento | Flow | executa | Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow disparado por evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 18 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow disparado por evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow disparado por evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 20 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 21 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v11"></a>

### H.2.v11 — External Client App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante APEX

Fluxo principal: Sistema externo → Usuário de integração → Pub/Sub API (Publish) → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
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
| 12 | Pub/Sub API (Publish) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 14 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 17 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | Define com qual usuário o trigger roda e quantos eventos processa de uma vez. | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 18 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 19 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 20 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 21 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 22 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v12"></a>

### H.2.v12 — External Client App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante FLOW

Fluxo principal: Sistema externo → Usuário de integração → Pub/Sub API (Publish) → Flow disparado por evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
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
| 12 | Pub/Sub API (Publish) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 14 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Flow disparado por evento | Flow | executa | Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow disparado por evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 18 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow disparado por evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow disparado por evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 20 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 21 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v13"></a>

### H.2.v13 — External Client App · OAuth 2.0 Client Credentials · publica via REST · assinante APEX

Fluxo principal: Sistema externo → Usuário run-as → REST API (sObject __e) → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (sObject __e) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 12 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 13 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 16 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | Define com qual usuário o trigger roda e quantos eventos processa de uma vez. | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 18 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 20 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 21 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v14"></a>

### H.2.v14 — External Client App · OAuth 2.0 Client Credentials · publica via REST · assinante FLOW

Fluxo principal: Sistema externo → Usuário run-as → REST API (sObject __e) → Flow disparado por evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (sObject __e) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 12 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 13 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Flow disparado por evento | Flow | executa | Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow disparado por evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 17 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow disparado por evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow disparado por evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 19 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 20 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v15"></a>

### H.2.v15 — External Client App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante APEX

Fluxo principal: Sistema externo → Usuário run-as → Pub/Sub API (Publish) → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Pub/Sub API (Publish) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 12 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 13 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 16 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | Define com qual usuário o trigger roda e quantos eventos processa de uma vez. | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 18 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 20 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 21 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h2v16"></a>

### H.2.v16 — External Client App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante FLOW

Fluxo principal: Sistema externo → Usuário run-as → Pub/Sub API (Publish) → Flow disparado por evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Publica o evento pela API. | — | API | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Pub/Sub API (Publish) | não é metadata | ator | API do Salesforce que recebe a publicação do evento. | Sistema externo | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 12 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | API | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 13 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | API | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Permission Set (Create no evento) | PermissionSet | autoriza | Dá ao usuário de integração permissão para publicar o evento. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Flow disparado por evento | Flow | executa | Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce. | barramento | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Flow disparado por evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 17 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Flow disparado por evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Flow disparado por evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 19 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 20 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## H.3

**Apex REST que recebe e enfileira**

Entrada síncrona, processamento assíncrono.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [H.3.v1](#h3v1) | Connected App · OAuth 2.0 JWT Bearer · delega para Queueable | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.3.v2](#h3v2) | Connected App · OAuth 2.0 JWT Bearer · delega para Platform Event | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.3.v3](#h3v3) | Connected App · OAuth 2.0 Client Credentials · delega para Queueable | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.3.v4](#h3v4) | Connected App · OAuth 2.0 Client Credentials · delega para Platform Event | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.3.v5](#h3v5) | External Client App · OAuth 2.0 JWT Bearer · delega para Queueable | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.3.v6](#h3v6) | External Client App · OAuth 2.0 JWT Bearer · delega para Platform Event | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.3.v7](#h3v7) | External Client App · OAuth 2.0 Client Credentials · delega para Queueable | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.3.v8](#h3v8) | External Client App · OAuth 2.0 Client Credentials · delega para Platform Event | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="h3v1"></a>

### H.3.v1 — Connected App · OAuth 2.0 JWT Bearer · delega para Queueable

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Classe Queueable → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço do Salesforce chamado pelo sistema externo. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classe Apex REST | ApexClass | executa | Recebe a chamada, confere os dados e responde na hora "recebido" (202). O processamento pesado fica para depois, em segundo plano. | Apex REST | Queueable | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 10 | Classe Queueable | ApexClass | executa | Tarefa em segundo plano que faz o processamento depois que o sistema externo já recebeu a resposta. | Classe Apex REST | Objeto de destino | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Queueable | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Queueable | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Queueable | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 14 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="h3v2"></a>

### H.3.v2 — Connected App · OAuth 2.0 JWT Bearer · delega para Platform Event

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço do Salesforce chamado pelo sistema externo. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classe Apex REST | ApexClass | executa | Recebe a chamada, confere os dados e responde na hora "recebido" (202). O processamento pesado fica para depois, em segundo plano. | Apex REST | Platform Event | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 10 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | Classe Apex REST | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 11 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega e faz o processamento. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 14 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 18 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Trigger do evento | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="h3v3"></a>

### H.3.v3 — Connected App · OAuth 2.0 Client Credentials · delega para Queueable

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Classe Queueable → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço do Salesforce chamado pelo sistema externo. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | Recebe a chamada, confere os dados e responde na hora "recebido" (202). O processamento pesado fica para depois, em segundo plano. | Apex REST | Queueable | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Classe Queueable | ApexClass | executa | Tarefa em segundo plano que faz o processamento depois que o sistema externo já recebeu a resposta. | Classe Apex REST | Objeto de destino | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Queueable | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Queueable | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Queueable | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="h3v4"></a>

### H.3.v4 — Connected App · OAuth 2.0 Client Credentials · delega para Platform Event

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço do Salesforce chamado pelo sistema externo. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 8 | Classe Apex REST | ApexClass | executa | Recebe a chamada, confere os dados e responde na hora "recebido" (202). O processamento pesado fica para depois, em segundo plano. | Apex REST | Platform Event | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | Classe Apex REST | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 10 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 11 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega e faz o processamento. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 13 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 15 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 16 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Trigger do evento | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="h3v5"></a>

### H.3.v5 — External Client App · OAuth 2.0 JWT Bearer · delega para Queueable

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Classe Queueable → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
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
| 12 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço do Salesforce chamado pelo sistema externo. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classe Apex REST | ApexClass | executa | Recebe a chamada, confere os dados e responde na hora "recebido" (202). O processamento pesado fica para depois, em segundo plano. | Apex REST | Queueable | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 14 | Classe Queueable | ApexClass | executa | Tarefa em segundo plano que faz o processamento depois que o sistema externo já recebeu a resposta. | Classe Apex REST | Objeto de destino | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Queueable | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Queueable | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Queueable | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 18 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 19 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 20 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="h3v6"></a>

### H.3.v6 — External Client App · OAuth 2.0 JWT Bearer · delega para Platform Event

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
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
| 12 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço do Salesforce chamado pelo sistema externo. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classe Apex REST | ApexClass | executa | Recebe a chamada, confere os dados e responde na hora "recebido" (202). O processamento pesado fica para depois, em segundo plano. | Apex REST | Platform Event | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 14 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | Classe Apex REST | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 15 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega e faz o processamento. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 18 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 20 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 21 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 22 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Trigger do evento | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="h3v7"></a>

### H.3.v7 — External Client App · OAuth 2.0 Client Credentials · delega para Queueable

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Classe Queueable → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço do Salesforce chamado pelo sistema externo. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | Recebe a chamada, confere os dados e responde na hora "recebido" (202). O processamento pesado fica para depois, em segundo plano. | Apex REST | Queueable | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Classe Queueable | ApexClass | executa | Tarefa em segundo plano que faz o processamento depois que o sistema externo já recebeu a resposta. | Classe Apex REST | Objeto de destino | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe Queueable | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe Queueable | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Classe Queueable | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 19 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="h3v8"></a>

### H.3.v8 — External Client App · OAuth 2.0 Client Credentials · delega para Platform Event

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Trigger do evento → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a Apex REST. | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | Endereço do Salesforce chamado pelo sistema externo. | Sistema externo | Classe Apex REST | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 12 | Classe Apex REST | ApexClass | executa | Recebe a chamada, confere os dados e responde na hora "recebido" (202). O processamento pesado fica para depois, em segundo plano. | Apex REST | Platform Event | Obrigatório | C11 `@RestResource(urlMapping=...)` |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | Platform Event: o "formato" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta. | Classe Apex REST | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 14 | Campos do evento | CustomField | lê/referencia | Campos da mensagem: os dados que viajam no evento. | Classe Apex REST | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 15 | Trigger do evento | ApexTrigger | executa | Código que roda quando o evento chega e faz o processamento. | barramento | Objeto de destino | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Trigger do evento | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 17 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Trigger do evento | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar. | Trigger do evento | — | Opcional (obrigatório em upsert) | `<externalId>true</externalId>` no campo [MA-CF] |
| 19 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 20 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 21 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Trigger do evento | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## H.4

**E-mail inbound (Email Service)**

Integração por e-mail.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [H.4.v1](#h4v1) | Processa direto | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.4.v2](#h4v2) | Enfileira processamento | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="h4v1"></a>

### H.4.v1 — Processa direto

Fluxo principal: Sistema externo → Email Service → Classe handler → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Manda um e-mail para o endereço do Email Service. | — | Email Service | Obrigatório | não aparece no projeto (ator) |
| 2 | Email Service | EmailServicesFunction | executa | Cria um endereço de e-mail no Salesforce. Define quem pode enviar, com qual usuário o processamento roda e o que fazer em caso de erro. | Sistema externo | Classe handler | Obrigatório | `emailservices/*.xml` — `apexClass`, `runAsUser`, `authorizedSenders`, `isAuthenticationRequired`, `emailServicesAddresses`, `isActive` [MA-ESF] |
| 3 | Classe handler | ApexClass | executa | Classe Apex que recebe cada e-mail que chega ao endereço (`Messaging.InboundEmailHandler`) e lê o texto e os anexos. | Email Service | Objeto de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 4 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe handler | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 5 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe handler | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 7 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h4v2"></a>

### H.4.v2 — Enfileira processamento

Fluxo principal: Sistema externo → Email Service → Classe handler → Classe Queueable → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Manda um e-mail para o endereço do Email Service. | — | Email Service | Obrigatório | não aparece no projeto (ator) |
| 2 | Email Service | EmailServicesFunction | executa | Cria um endereço de e-mail no Salesforce. Define quem pode enviar, com qual usuário o processamento roda e o que fazer em caso de erro. | Sistema externo | Classe handler | Obrigatório | `emailservices/*.xml` — `apexClass`, `runAsUser`, `authorizedSenders`, `isAuthenticationRequired`, `emailServicesAddresses`, `isActive` [MA-ESF] |
| 3 | Classe handler | ApexClass | executa | Classe Apex que recebe cada e-mail que chega ao endereço (`Messaging.InboundEmailHandler`) e lê o texto e os anexos. | Email Service | Queueable | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 4 | Classe Queueable | ApexClass | executa | Tarefa em segundo plano para o processamento mais pesado. | Classe handler | Objeto de destino | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 5 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | Classe handler | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 6 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | Classe handler | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 8 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |


## H.5

**Arquivos via ContentVersion**

O externo envia arquivo; automação processa.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [H.5.v1](#h5v1) | Connected App · OAuth 2.0 JWT Bearer · processador APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.5.v2](#h5v2) | Connected App · OAuth 2.0 JWT Bearer · processador FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.5.v3](#h5v3) | Connected App · OAuth 2.0 Client Credentials · processador APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.5.v4](#h5v4) | Connected App · OAuth 2.0 Client Credentials · processador FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.5.v5](#h5v5) | External Client App · OAuth 2.0 JWT Bearer · processador APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.5.v6](#h5v6) | External Client App · OAuth 2.0 JWT Bearer · processador FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.5.v7](#h5v7) | External Client App · OAuth 2.0 Client Credentials · processador APEX | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [H.5.v8](#h5v8) | External Client App · OAuth 2.0 Client Credentials · processador FLOW | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="h5v1"></a>

### H.5.v1 — Connected App · OAuth 2.0 JWT Bearer · processador APEX

Fluxo principal: Sistema externo → Usuário de integração → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Trigger em ContentVersion → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (ContentVersion). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (ContentVersion) | não é metadata | ator | API do Salesforce que recebe o arquivo enviado pelo sistema externo. | Sistema externo | ContentVersion | Obrigatório | não aparece no projeto (ator) |
| 9 | ContentVersion / ContentDocumentLink | não é metadata | ator | Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto. | REST API | processador | Obrigatório | não aparece no projeto (ator) |
| 10 | Trigger em ContentVersion | ApexTrigger | executa | Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo. | plataforma (DML) | Objeto de destino | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | processador | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | processador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h5v2"></a>

### H.5.v2 — Connected App · OAuth 2.0 JWT Bearer · processador FLOW

Fluxo principal: Sistema externo → Usuário de integração → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Flow record-triggered em ContentVersion → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (ContentVersion). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 4 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 5 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 8 | REST API (ContentVersion) | não é metadata | ator | API do Salesforce que recebe o arquivo enviado pelo sistema externo. | Sistema externo | ContentVersion | Obrigatório | não aparece no projeto (ator) |
| 9 | ContentVersion / ContentDocumentLink | não é metadata | ator | Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto. | REST API | processador | Obrigatório | não aparece no projeto (ator) |
| 10 | Flow record-triggered em ContentVersion | Flow | executa | Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo. | plataforma (DML) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | processador | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 12 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | processador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 13 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h5v3"></a>

### H.5.v3 — Connected App · OAuth 2.0 Client Credentials · processador APEX

Fluxo principal: Sistema externo → Usuário run-as → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Trigger em ContentVersion → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (ContentVersion). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (ContentVersion) | não é metadata | ator | API do Salesforce que recebe o arquivo enviado pelo sistema externo. | Sistema externo | ContentVersion | Obrigatório | não aparece no projeto (ator) |
| 8 | ContentVersion / ContentDocumentLink | não é metadata | ator | Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto. | REST API | processador | Obrigatório | não aparece no projeto (ator) |
| 9 | Trigger em ContentVersion | ApexTrigger | executa | Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo. | plataforma (DML) | Objeto de destino | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | processador | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | processador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h5v4"></a>

### H.5.v4 — Connected App · OAuth 2.0 Client Credentials · processador FLOW

Fluxo principal: Sistema externo → Usuário run-as → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Flow record-triggered em ContentVersion → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (ContentVersion). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 Client Credentials (`isClientCredentialEnabled` + `oauthClientCredentialUser`)) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 3 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 4 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 7 | REST API (ContentVersion) | não é metadata | ator | API do Salesforce que recebe o arquivo enviado pelo sistema externo. | Sistema externo | ContentVersion | Obrigatório | não aparece no projeto (ator) |
| 8 | ContentVersion / ContentDocumentLink | não é metadata | ator | Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto. | REST API | processador | Obrigatório | não aparece no projeto (ator) |
| 9 | Flow record-triggered em ContentVersion | Flow | executa | Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo. | plataforma (DML) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | processador | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 11 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | processador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 12 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 13 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h5v5"></a>

### H.5.v5 — External Client App · OAuth 2.0 JWT Bearer · processador APEX

Fluxo principal: Sistema externo → Usuário de integração → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Trigger em ContentVersion → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (ContentVersion). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
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
| 12 | REST API (ContentVersion) | não é metadata | ator | API do Salesforce que recebe o arquivo enviado pelo sistema externo. | Sistema externo | ContentVersion | Obrigatório | não aparece no projeto (ator) |
| 13 | ContentVersion / ContentDocumentLink | não é metadata | ator | Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto. | REST API | processador | Obrigatório | não aparece no projeto (ator) |
| 14 | Trigger em ContentVersion | ApexTrigger | executa | Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo. | plataforma (DML) | Objeto de destino | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | processador | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | processador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h5v6"></a>

### H.5.v6 — External Client App · OAuth 2.0 JWT Bearer · processador FLOW

Fluxo principal: Sistema externo → Usuário de integração → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Flow record-triggered em ContentVersion → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (ContentVersion). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
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
| 12 | REST API (ContentVersion) | não é metadata | ator | API do Salesforce que recebe o arquivo enviado pelo sistema externo. | Sistema externo | ContentVersion | Obrigatório | não aparece no projeto (ator) |
| 13 | ContentVersion / ContentDocumentLink | não é metadata | ator | Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto. | REST API | processador | Obrigatório | não aparece no projeto (ator) |
| 14 | Flow record-triggered em ContentVersion | Flow | executa | Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo. | plataforma (DML) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | processador | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 16 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | processador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 17 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 18 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h5v7"></a>

### H.5.v7 — External Client App · OAuth 2.0 Client Credentials · processador APEX

Fluxo principal: Sistema externo → Usuário run-as → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Trigger em ContentVersion → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (ContentVersion). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (ContentVersion) | não é metadata | ator | API do Salesforce que recebe o arquivo enviado pelo sistema externo. | Sistema externo | ContentVersion | Obrigatório | não aparece no projeto (ator) |
| 12 | ContentVersion / ContentDocumentLink | não é metadata | ator | Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto. | REST API | processador | Obrigatório | não aparece no projeto (ator) |
| 13 | Trigger em ContentVersion | ApexTrigger | executa | Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo. | plataforma (DML) | Objeto de destino | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | processador | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | processador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

<a id="h5v8"></a>

### H.5.v8 — External Client App · OAuth 2.0 Client Credentials · processador FLOW

Fluxo principal: Sistema externo → Usuário run-as → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Flow record-triggered em ContentVersion → Objeto de destino

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a REST API (ContentVersion). | — | Connected App / External Client App | Obrigatório | não aparece no projeto (ator) |
| 2 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 Client Credentials. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 7 | Usuário run-as | não é metadata | ator | No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app. | app | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 11 | REST API (ContentVersion) | não é metadata | ator | API do Salesforce que recebe o arquivo enviado pelo sistema externo. | Sistema externo | ContentVersion | Obrigatório | não aparece no projeto (ator) |
| 12 | ContentVersion / ContentDocumentLink | não é metadata | ator | Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto. | REST API | processador | Obrigatório | não aparece no projeto (ator) |
| 13 | Flow record-triggered em ContentVersion | Flow | executa | Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo. | plataforma (DML) | Objeto de destino | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros. | processador | triggers e flows do objeto | Obrigatório | `objects/*.object` [MA-CO] |
| 15 | Campos | CustomField | lê/referencia | Campos que a integração lê ou preenche. | processador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 16 | Trigger do objeto | ApexTrigger | executa | Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações). | plataforma (DML) | classes handler | Opcional | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 17 | Flow record-triggered | Flow | executa | Automação sem código que roda quando a integração grava o registro. | plataforma (DML) | — | Opcional | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |

