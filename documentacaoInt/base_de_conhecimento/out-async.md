# OUT ASYNC — Salesforce envia sem esperar

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
| `CustomNotificationType` | Tipo de notificação que aparece no sino do Salesforce. |
| `CustomObject` | Objeto (tabela). Sufixos: `__c` customizado, `__x` externo, `__e` evento, `__mdt` tipo de configuração. |
| `CustomPermission` | Permissão criada pela empresa; pode servir de chave liga/desliga. |
| `EmailTemplate` | Modelo de e-mail. |
| `EventRelayConfig` | Configuração que repassa eventos do Salesforce para a AWS (Amazon EventBridge). |
| `ExternalClientApplication` | Cadastro (modelo novo, recomendado) de um sistema externo que vai entrar no Salesforce via OAuth. |
| `ExternalCredential` | Cadastro de como autenticar em um sistema externo (OAuth, JWT, senha, cabeçalho). Usado pela Named Credential. |
| `ExternalServiceRegistration` | Cadastro de uma API externa a partir do contrato dela (OpenAPI). Vira ações para Flow e classes para Apex. |
| `ExtlClntAppConfigurablePolicies` | Parte do External Client App que liga ou desliga o app na org. |
| `ExtlClntAppGlobalOauthSettings` | Parte do External Client App com client_id, client_secret, certificado e fluxos ligados. |
| `ExtlClntAppOauthConfigurablePolicies` | Parte do External Client App com as regras do admin (quem pode usar, IP, usuário do Client Credentials). |
| `ExtlClntAppOauthSettings` | Parte do External Client App com os escopos (permissões) do token. |
| `Flow` | Automação montada sem código no Flow Builder (com telas, disparada por registro, por agenda ou por evento). |
| `ManagedEventSubscription` | Assinatura de eventos gerenciada pela plataforma para clientes da Pub/Sub API. |
| `NamedCredential` | Cadastro do endereço de um sistema externo (e, no modelo novo, a ligação com a autenticação). Quem usa Named Credential não precisa de Remote Site Setting para aquele domínio. |
| `OauthCustomScope` | Escopo OAuth criado pela empresa para limitar o que um token pode fazer. |
| `PermissionSet` | Conjunto de permissões extras que se dá a um usuário. |
| `PermissionSetGroup` | Grupo de Permission Sets. |
| `PlatformCachePartition` | Memória temporária da plataforma, para guardar dados como tokens. |
| `PlatformEventChannel` | Canal que agrupa eventos para quem vai assinar. |
| `PlatformEventChannelMember` | Item de um canal de eventos; no CDC, indica qual objeto gera eventos de mudança. |
| `PlatformEventSubscriberConfig` | Configuração de quem roda o trigger de um evento e quantos eventos por vez. |
| `Profile` | Perfil do usuário: conjunto básico de permissões. |
| `RemoteSiteSetting` | Lista de domínios externos que o código Apex pode chamar quando a URL **não** vem de uma Named Credential. |
| `Workflow` | Regras de workflow (recurso antigo); inclui o Outbound Message, que envia dados por SOAP. |

## Índice

- [D.1 — Trigger Apex → @future ou Queueable → callout](#d1) (12 variantes)
- [D.2 — Flow record-triggered → caminho assíncrono → callout](#d2) (10 variantes)
- [D.3 — Trigger/Flow publica Platform Event → assinante faz o callout](#d3) (16 variantes)
- [D.4 — Outbound Message (SOAP com retry)](#d4) (4 variantes)
- [E.1 — Platform Event publicado → sistema externo assina](#e1) (6 variantes)
- [E.2 — Change Data Capture](#e2) (8 variantes)
- [E.3 — Canal customizado com enriquecimento e filtro](#e3) (4 variantes)
- [E.4 — Event Relay → Amazon EventBridge](#e4) (2 variantes)
- [F.1 — Schedulable → Batch Apex com callout](#f1) (12 variantes)
- [F.2 — Schedulable → Queueable encadeado (paginação)](#f2) (12 variantes)
- [F.3 — Flow agendado → callout](#f3) (10 variantes)
- [F.4 — Apex → Bulk API 2.0 de outra org](#f4) (6 variantes)
- [G.1 — Fila de integração em objeto (staging) + processador](#g1) (12 variantes)

## D.1

**Trigger Apex → @future ou Queueable → callout**

Callout fora da transação do registro (callout síncrono em trigger não é permitido). Serve para atualizar o externo ou buscar dados e enriquecer o registro.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [D.1.v1](#d1v1) | @future · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.1.v2](#d1v2) | @future · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.1.v3](#d1v3) | @future · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.1.v4](#d1v4) | @future · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.1.v5](#d1v5) | @future · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.1.v6](#d1v6) | @future · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.1.v7](#d1v7) | Queueable · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.1.v8](#d1v8) | Queueable · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.1.v9](#d1v9) | Queueable · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.1.v10](#d1v10) | Queueable · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.1.v11](#d1v11) | Queueable · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.1.v12](#d1v12) | Queueable · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="d1v1"></a>

### D.1.v1 — @future · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Método @future | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v2"></a>

### D.1.v2 — @future · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Método @future | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v3"></a>

### D.1.v3 — @future · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

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
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v4"></a>

### D.1.v4 — @future · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

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
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v5"></a>

### D.1.v5 — @future · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

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
| 9 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v6"></a>

### D.1.v6 — @future · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

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
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v7"></a>

### D.1.v7 — Queueable · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

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
| 8 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v8"></a>

### D.1.v8 — Queueable · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Queueable | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v9"></a>

### D.1.v9 — Queueable · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

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
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v10"></a>

### D.1.v10 — Queueable · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

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
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v11"></a>

### D.1.v11 — Queueable · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

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
| 10 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d1v12"></a>

### D.1.v12 — Queueable · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

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
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## D.2

**Flow record-triggered → caminho assíncrono → callout**

Versão declarativa do D.1.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [D.2.v1](#d2v1) | Ação HTTP Callout · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.2.v2](#d2v2) | Ação HTTP Callout · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.2.v3](#d2v3) | Ação External Service · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.2.v4](#d2v4) | Ação External Service · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.2.v5](#d2v5) | Ação Apex invocável · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.2.v6](#d2v6) | Ação Apex invocável · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.2.v7](#d2v7) | Ação Apex invocável · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.2.v8](#d2v8) | Ação Apex invocável · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.2.v9](#d2v9) | Ação Apex invocável · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.2.v10](#d2v10) | Ação Apex invocável · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="d2v1"></a>

### D.2.v1 — Ação HTTP Callout · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Flow | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v2"></a>

### D.2.v2 — Ação HTTP Callout · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Flow | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v3"></a>

### D.2.v3 — Ação External Service · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Flow | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v4"></a>

### D.2.v4 — Ação External Service · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Flow | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v5"></a>

### D.2.v5 — Ação Apex invocável · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v6"></a>

### D.2.v6 — Ação Apex invocável · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe invocável | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v7"></a>

### D.2.v7 — Ação Apex invocável · endpoint E3

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe invocável | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v8"></a>

### D.2.v8 — Ação Apex invocável · endpoint E4

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe invocável | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v9"></a>

### D.2.v9 — Ação Apex invocável · endpoint E5

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d2v10"></a>

### D.2.v10 — Ação Apex invocável · endpoint E6

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe invocável | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## D.3

**Trigger/Flow publica Platform Event → assinante faz o callout**

Desacopla a transação de origem do callout.

> Observação: Confirmado [PE-SUB]: em trigger de Platform Event, "with some exceptions, you generally can’t make Apex callouts" — por isso o assinante Apex enfileira um Queueable.
> ⚠️ A validar: Callout em Platform Event–Triggered Flow: não encontrado nas páginas consultadas.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [D.3.v1](#d3v1) | Publica Apex · assina Apex Trigger + Queueable · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v2](#d3v2) | Publica Apex · assina Apex Trigger + Queueable · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v3](#d3v3) | Publica Apex · assina Apex Trigger + Queueable · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.3.v4](#d3v4) | Publica Apex · assina Apex Trigger + Queueable · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.3.v5](#d3v5) | Publica Apex · assina Apex Trigger + Queueable · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v6](#d3v6) | Publica Apex · assina Apex Trigger + Queueable · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.3.v7](#d3v7) | Publica Apex · assina Flow · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v8](#d3v8) | Publica Apex · assina Flow · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v9](#d3v9) | Publica Flow · assina Apex Trigger + Queueable · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v10](#d3v10) | Publica Flow · assina Apex Trigger + Queueable · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v11](#d3v11) | Publica Flow · assina Apex Trigger + Queueable · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.3.v12](#d3v12) | Publica Flow · assina Apex Trigger + Queueable · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.3.v13](#d3v13) | Publica Flow · assina Apex Trigger + Queueable · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v14](#d3v14) | Publica Flow · assina Apex Trigger + Queueable · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [D.3.v15](#d3v15) | Publica Flow · assina Flow · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [D.3.v16](#d3v16) | Publica Flow · assina Flow · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |

<a id="d3v1"></a>

### D.3.v1 — Publica Apex · assina Apex Trigger + Queueable · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 11 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 15 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v2"></a>

### D.3.v2 — Publica Apex · assina Apex Trigger + Queueable · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 11 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Queueable | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 13 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v3"></a>

### D.3.v3 — Publica Apex · assina Apex Trigger + Queueable · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v4"></a>

### D.3.v4 — Publica Apex · assina Apex Trigger + Queueable · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 11 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 12 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 13 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 14 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 15 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 16 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v5"></a>

### D.3.v5 — Publica Apex · assina Apex Trigger + Queueable · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 11 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 12 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 13 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 14 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 15 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v6"></a>

### D.3.v6 — Publica Apex · assina Apex Trigger + Queueable · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 11 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v7"></a>

### D.3.v7 — Publica Apex · assina Flow · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Flow disparado por evento → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 8 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 9 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Flow disparado por evento | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow disparado por evento | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v8"></a>

### D.3.v8 — Publica Apex · assina Flow · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Flow disparado por evento → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 8 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Flow disparado por evento | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 11 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow disparado por evento | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v9"></a>

### D.3.v9 — Publica Flow · assina Apex Trigger + Queueable · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 10 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v10"></a>

### D.3.v10 — Publica Flow · assina Apex Trigger + Queueable · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 10 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Queueable | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 12 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v11"></a>

### D.3.v11 — Publica Flow · assina Apex Trigger + Queueable · endpoint E3

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v12"></a>

### D.3.v12 — Publica Flow · assina Apex Trigger + Queueable · endpoint E4

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 10 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 12 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 13 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 14 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 15 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v13"></a>

### D.3.v13 — Publica Flow · assina Apex Trigger + Queueable · endpoint E5

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 10 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 12 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 13 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 14 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v14"></a>

### D.3.v14 — Publica Flow · assina Apex Trigger + Queueable · endpoint E6

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório | C19 `trigger ... on X__e (after insert)` |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 10 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v15"></a>

### D.3.v15 — Publica Flow · assina Flow · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered → Flow disparado por evento → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 7 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Flow disparado por evento | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow disparado por evento | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="d3v16"></a>

### D.3.v16 — Publica Flow · assina Flow · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered → Flow disparado por evento → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 7 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Flow disparado por evento | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 10 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow disparado por evento | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## D.4

**Outbound Message (SOAP com retry)**

Legado; ainda comum em orgs antigas.

> Observação: Não usa Named Credential nem Remote Site Setting.
> Observação: No XML [MA-WF]: `workflows/Objeto.workflow` → `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`) e ação `type`=OutboundMessage na regra.
> ⚠️ A validar: Ação Outbound Message em Flow: o valor não aparece na lista de `actionType` (InvocableActionType) da página Flow [MA-FLOW]. Criação de novas Workflow Rules: não verificado.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [D.4.v1](#d4v1) | Workflow Rule · sem certificado | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [D.4.v2](#d4v2) | Workflow Rule · com certificado | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [D.4.v3](#d4v3) | Flow · sem certificado | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [D.4.v4](#d4v4) | Flow · com certificado | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="d4v1"></a>

### D.4.v1 — Workflow Rule · sem certificado

Fluxo principal: Gravação do registro → Regra de workflow → Usuário de envio → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Regra de workflow | Workflow (WorkflowRule) | executa | critério que dispara a mensagem (legado) | plataforma (DML) | Outbound Message | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |

<a id="d4v2"></a>

### D.4.v2 — Workflow Rule · com certificado

Fluxo principal: Gravação do registro → Regra de workflow → Usuário de envio → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Regra de workflow | Workflow (WorkflowRule) | executa | critério que dispara a mensagem (legado) | plataforma (DML) | Outbound Message | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Certificate | Certificate | autoriza | certificado de cliente para mutual TLS | Outbound Message | — | Obrigatório | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |

<a id="d4v3"></a>

### D.4.v3 — Flow · sem certificado

Fluxo principal: Gravação do registro → Flow record-triggered → Usuário de envio → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | ação Outbound Message | plataforma (DML) | Outbound Message | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |

<a id="d4v4"></a>

### D.4.v4 — Flow · com certificado

Fluxo principal: Gravação do registro → Flow record-triggered → Usuário de envio → Sistema externo

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | ação Outbound Message | plataforma (DML) | Outbound Message | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Certificate | Certificate | autoriza | certificado de cliente para mutual TLS | Outbound Message | — | Obrigatório | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |


## E.1

**Platform Event publicado → sistema externo assina**

O Salesforce publica; o externo consome via Pub/Sub API.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [E.1.v1](#e1v1) | Publicador APEX · assinante autenticado por Connected App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.1.v2](#e1v2) | Publicador APEX · assinante autenticado por External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.1.v3](#e1v3) | Publicador FLOW · assinante autenticado por Connected App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.1.v4](#e1v4) | Publicador FLOW · assinante autenticado por External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.1.v5](#e1v5) | Publicador API · assinante autenticado por Connected App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.1.v6](#e1v6) | Publicador API · assinante autenticado por External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="e1v1"></a>

### E.1.v1 — Publicador APEX · assinante autenticado por Connected App

Fluxo principal: Classe publicadora → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe publicadora | ApexClass | executa | `EventBus.publish` | trigger/serviço | Platform Event | Obrigatório | C18 `EventBus.publish(` |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e1v2"></a>

### E.1.v2 — Publicador APEX · assinante autenticado por External Client App

Fluxo principal: Classe publicadora → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe publicadora | ApexClass | executa | `EventBus.publish` | trigger/serviço | Platform Event | Obrigatório | C18 `EventBus.publish(` |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e1v3"></a>

### E.1.v3 — Publicador FLOW · assinante autenticado por Connected App

Fluxo principal: Flow publicador → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow publicador | Flow | executa | Create Records no `__e` | plataforma | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e1v4"></a>

### E.1.v4 — Publicador FLOW · assinante autenticado por External Client App

Fluxo principal: Flow publicador → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow publicador | Flow | executa | Create Records no `__e` | plataforma | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e1v5"></a>

### E.1.v5 — Publicador API · assinante autenticado por Connected App

Fluxo principal: Outro sistema → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Outro sistema | não é metadata | ator | publica via REST/Pub/Sub API | — | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e1v6"></a>

### E.1.v6 — Publicador API · assinante autenticado por External Client App

Fluxo principal: Outro sistema → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Outro sistema | não é metadata | ator | publica via REST/Pub/Sub API | — | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## E.2

**Change Data Capture**

Mudanças em registros viram eventos sem código de publicação.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [E.2.v1](#e2v1) | Assinante externo · Connected App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.2.v2](#e2v2) | Assinante externo · External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.2.v3](#e2v3) | Assinante interno (Apex) · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [E.2.v4](#e2v4) | Assinante interno (Apex) · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [E.2.v5](#e2v5) | Assinante interno (Apex) · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [E.2.v6](#e2v6) | Assinante interno (Apex) · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [E.2.v7](#e2v7) | Assinante interno (Apex) · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [E.2.v8](#e2v8) | Assinante interno (Apex) · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="e2v1"></a>

### E.2.v1 — Assinante externo · Connected App

Fluxo principal: Gravação do registro → Change Event → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 7 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 8 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 9 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 12 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 13 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 14 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e2v2"></a>

### E.2.v2 — Assinante externo · External Client App

Fluxo principal: Gravação do registro → Change Event → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 7 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 8 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 9 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 10 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 11 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 12 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 13 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 16 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 17 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 18 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e2v3"></a>

### E.2.v3 — Assinante interno (Apex) · endpoint E1

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v4"></a>

### E.2.v4 — Assinante interno (Apex) · endpoint E2

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Queueable | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 11 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v5"></a>

### E.2.v5 — Assinante interno (Apex) · endpoint E3

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v6"></a>

### E.2.v6 — Assinante interno (Apex) · endpoint E4

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 12 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 13 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v7"></a>

### E.2.v7 — Assinante interno (Apex) · endpoint E5

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v8"></a>

### E.2.v8 — Assinante interno (Apex) · endpoint E6

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |


## E.3

**Canal customizado com enriquecimento e filtro**

Seleciona eventos, adiciona campos e filtra antes de entregar.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [E.3.v1](#e3v1) | CDC · Connected App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.3.v2](#e3v2) | CDC · External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.3.v3](#e3v3) | PE · Connected App | Não se aplica | não há chamada de saída feita por Apex nesta variante |
| [E.3.v4](#e3v4) | PE · External Client App | Não se aplica | não há chamada de saída feita por Apex nesta variante |

<a id="e3v1"></a>

### E.3.v1 — CDC · Connected App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo data que agrupa eventos | plataforma | assinantes | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 3 | Objeto monitorado | CustomObject | lê/referencia | origem do change event | — | Canal | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e3v2"></a>

### E.3.v2 — CDC · External Client App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo data que agrupa eventos | plataforma | assinantes | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 3 | Objeto monitorado | CustomObject | lê/referencia | origem do change event | — | Canal | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e3v3"></a>

### E.3.v3 — PE · Connected App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo event que agrupa eventos | plataforma | assinantes | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 3 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 4 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 7 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 8 | Connected App | ConnectedApp | autoriza | Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo (OAuth 2.0 JWT Bearer) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 9 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 12 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 13 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 14 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="e3v4"></a>

### E.3.v4 — PE · External Client App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

Remote Site Setting: **Não se aplica** — não há chamada de saída feita por Apex nesta variante.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo event que agrupa eventos | plataforma | assinantes | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 3 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 4 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 7 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 8 | External Client App | ExternalClientApplication | autoriza | Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org. | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 9 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo OAuth 2.0 JWT Bearer. | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 10 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados. | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 11 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda. | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 12 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | Liga ou desliga o app e suas partes (plugins) nesta org. | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 13 | Certificate (público, do cliente) | Certificate | autoriza | No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app. | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Usuário de integração | não é metadata | ator | Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer. | app | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Perfil do usuário de integração | Profile | autoriza | Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API. | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 16 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 17 | Escopo OAuth customizado | OauthCustomScope | autoriza | Escopo criado pela empresa para limitar ainda mais o que o token pode acessar. | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 18 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## E.4

**Event Relay → Amazon EventBridge**

Ponte nativa de eventos com a AWS.

> Observação: Envia eventos para fora do Salesforce (AWS).
> Observação: Confirmado [MA-ERC]: `destinationResourceName` é o nome da Named Credential com prefixo `callout:` e guarda a conta AWS; `eventChannel` é um canal `X__chn`.
> ⚠️ A validar: Tipo (`namedCredentialType`) exigido para essa Named Credential: não informado na página.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [E.4.v1](#e4v1) | PE | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [E.4.v2](#e4v2) | CDC | Não | a Named Credential já autoriza o domínio [AX-RSS] |

<a id="e4v1"></a>

### E.4.v1 — PE

Fluxo principal: Event Relay → Amazon EventBridge

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 2 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 3 | Canal customizado | PlatformEventChannel | lê/referencia | canal que o relay lê | plataforma | Event Relay | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 4 | Membro do canal | PlatformEventChannelMember | lê/referencia | eventos incluídos no canal | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 5 | Event Relay | EventRelayConfig | executa | retransmite os eventos do canal ao destino | plataforma | Named Credential | Obrigatório | `eventRelays/*.eventRelay` — `destinationResourceName` (`callout:NomeNC`, guarda a conta AWS), `eventChannel` (`X__chn`), `relayOption`, `state` [MA-ERC] |
| 6 | Named Credential (destino AWS) | NamedCredential | lê/referencia | aponta para a conta/região AWS (EventBridge partner event source) | Event Relay | Amazon EventBridge | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Amazon EventBridge | não é metadata | ator | recebe os eventos; regras roteiam para outros serviços | Event Relay | — | Obrigatório | não aparece no projeto (ator) |

<a id="e4v2"></a>

### E.4.v2 — CDC

Fluxo principal: Event Relay → Amazon EventBridge

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Objeto monitorado | CustomObject | lê/referencia | origem do change event | — | Canal | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 2 | Canal customizado | PlatformEventChannel | lê/referencia | canal que o relay lê | plataforma | Event Relay | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 3 | Membro do canal | PlatformEventChannelMember | lê/referencia | eventos incluídos no canal | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Event Relay | EventRelayConfig | executa | retransmite os eventos do canal ao destino | plataforma | Named Credential | Obrigatório | `eventRelays/*.eventRelay` — `destinationResourceName` (`callout:NomeNC`, guarda a conta AWS), `eventChannel` (`X__chn`), `relayOption`, `state` [MA-ERC] |
| 5 | Named Credential (destino AWS) | NamedCredential | lê/referencia | aponta para a conta/região AWS (EventBridge partner event source) | Event Relay | Amazon EventBridge | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Amazon EventBridge | não é metadata | ator | recebe os eventos; regras roteiam para outros serviços | Event Relay | — | Obrigatório | não aparece no projeto (ator) |


## F.1

**Schedulable → Batch Apex com callout**

Sincronização periódica em lotes.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [F.1.v1](#f1v1) | Envia dados · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.1.v2](#f1v2) | Envia dados · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.1.v3](#f1v3) | Envia dados · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.1.v4](#f1v4) | Envia dados · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.1.v5](#f1v5) | Envia dados · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.1.v6](#f1v6) | Envia dados · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.1.v7](#f1v7) | Busca dados · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.1.v8](#f1v8) | Busca dados · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.1.v9](#f1v9) | Busca dados · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.1.v10](#f1v10) | Busca dados · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.1.v11](#f1v11) | Busca dados · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.1.v12](#f1v12) | Busca dados · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="f1v1"></a>

### F.1.v1 — Envia dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Batch | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v2"></a>

### F.1.v2 — Envia dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Batch | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v3"></a>

### F.1.v3 — Envia dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Batch | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v4"></a>

### F.1.v4 — Envia dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Batch | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Batch | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Batch | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v5"></a>

### F.1.v5 — Envia dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Batch | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Batch | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Batch | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v6"></a>

### F.1.v6 — Envia dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Batch | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v7"></a>

### F.1.v7 — Busca dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Batch | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v8"></a>

### F.1.v8 — Busca dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Batch | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v9"></a>

### F.1.v9 — Busca dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Batch | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v10"></a>

### F.1.v10 — Busca dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Batch | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Batch | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Batch | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v11"></a>

### F.1.v11 — Busca dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Batch | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Batch | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Batch | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f1v12"></a>

### F.1.v12 — Busca dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Batch | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |


## F.2

**Schedulable → Queueable encadeado (paginação)**

Percorre APIs paginadas.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [F.2.v1](#f2v1) | Envia dados · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.2.v2](#f2v2) | Envia dados · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.2.v3](#f2v3) | Envia dados · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.2.v4](#f2v4) | Envia dados · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.2.v5](#f2v5) | Envia dados · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.2.v6](#f2v6) | Envia dados · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.2.v7](#f2v7) | Busca dados · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.2.v8](#f2v8) | Busca dados · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.2.v9](#f2v9) | Busca dados · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.2.v10](#f2v10) | Busca dados · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.2.v11](#f2v11) | Busca dados · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.2.v12](#f2v12) | Busca dados · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="f2v1"></a>

### F.2.v1 — Envia dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Queueable encadeada | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v2"></a>

### F.2.v2 — Envia dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Queueable encadeada | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v3"></a>

### F.2.v3 — Envia dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Queueable encadeada | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v4"></a>

### F.2.v4 — Envia dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Queueable encadeada | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Queueable encadeada | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v5"></a>

### F.2.v5 — Envia dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Queueable encadeada | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Queueable encadeada | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v6"></a>

### F.2.v6 — Envia dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v7"></a>

### F.2.v7 — Busca dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Queueable encadeada | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v8"></a>

### F.2.v8 — Busca dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Queueable encadeada | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v9"></a>

### F.2.v9 — Busca dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Queueable encadeada | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v10"></a>

### F.2.v10 — Busca dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Queueable encadeada | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Queueable encadeada | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v11"></a>

### F.2.v11 — Busca dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Queueable encadeada | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Queueable encadeada | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

<a id="f2v12"></a>

### F.2.v12 — Busca dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |


## F.3

**Flow agendado → callout**

Versão declarativa do F.1.

> ⚠️ A validar: Suporte a HTTP Callout em Schedule-Triggered Flow: não encontrado nas páginas consultadas.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [F.3.v1](#f3v1) | Ação HTTP · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.3.v2](#f3v2) | Ação HTTP · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.3.v3](#f3v3) | Ação ES · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.3.v4](#f3v4) | Ação ES · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.3.v5](#f3v5) | Ação APEX · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.3.v6](#f3v6) | Ação APEX · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.3.v7](#f3v7) | Ação APEX · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.3.v8](#f3v8) | Ação APEX · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [F.3.v9](#f3v9) | Ação APEX · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.3.v10](#f3v10) | Ação APEX · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="f3v1"></a>

### F.3.v1 — Ação HTTP · endpoint E1

Fluxo principal: Flow agendado → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Flow agendado | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow agendado | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v2"></a>

### F.3.v2 — Ação HTTP · endpoint E2

Fluxo principal: Flow agendado → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Flow agendado | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow agendado | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v3"></a>

### F.3.v3 — Ação ES · endpoint E1

Fluxo principal: Flow agendado → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Flow agendado | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow agendado | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v4"></a>

### F.3.v4 — Ação ES · endpoint E2

Fluxo principal: Flow agendado → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Flow agendado | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Flow agendado | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v5"></a>

### F.3.v5 — Ação APEX · endpoint E1

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v6"></a>

### F.3.v6 — Ação APEX · endpoint E2

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe invocável | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v7"></a>

### F.3.v7 — Ação APEX · endpoint E3

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 4 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe invocável | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 5 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v8"></a>

### F.3.v8 — Ação APEX · endpoint E4

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe invocável | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 6 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v9"></a>

### F.3.v9 — Ação APEX · endpoint E5

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

<a id="f3v10"></a>

### F.3.v10 — Ação APEX · endpoint E6

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe invocável | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |


## F.4

**Apex → Bulk API 2.0 de outra org**

Carga entre orgs.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [F.4.v1](#f4v1) | BATCH · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.4.v2](#f4v2) | BATCH · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.4.v3](#f4v3) | BATCH · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.4.v4](#f4v4) | QUEUE · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.4.v5](#f4v5) | QUEUE · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [F.4.v6](#f4v6) | QUEUE · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |

<a id="f4v1"></a>

### F.4.v1 — BATCH · endpoint E1

Fluxo principal: Classe de carga → Org Salesforce de destino

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe de carga | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Org Salesforce de destino | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Org Salesforce de destino | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

<a id="f4v2"></a>

### F.4.v2 — BATCH · endpoint E2

Fluxo principal: Classe de carga → Org Salesforce de destino

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe de carga | Org Salesforce de destino | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 4 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 5 | Org Salesforce de destino | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

<a id="f4v3"></a>

### F.4.v3 — BATCH · endpoint E5

Fluxo principal: Classe de carga → Org Salesforce de destino

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe de carga | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe de carga | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe de carga | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Org Salesforce de destino | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Org Salesforce de destino | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

<a id="f4v4"></a>

### F.4.v4 — QUEUE · endpoint E1

Fluxo principal: Classe de carga → Org Salesforce de destino

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe de carga | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Org Salesforce de destino | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 5 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Org Salesforce de destino | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

<a id="f4v5"></a>

### F.4.v5 — QUEUE · endpoint E2

Fluxo principal: Classe de carga → Org Salesforce de destino

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe de carga | Org Salesforce de destino | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 4 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 5 | Org Salesforce de destino | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

<a id="f4v6"></a>

### F.4.v6 — QUEUE · endpoint E5

Fluxo principal: Classe de carga → Org Salesforce de destino

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe de carga | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe de carga | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe de carga | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Org Salesforce de destino | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Org Salesforce de destino | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |


## G.1

**Fila de integração em objeto (staging) + processador**

Resiliência com status, tentativas e reprocessamento.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [G.1.v1](#g1v1) | Processador BATCH · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [G.1.v2](#g1v2) | Processador BATCH · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [G.1.v3](#g1v3) | Processador BATCH · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [G.1.v4](#g1v4) | Processador BATCH · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [G.1.v5](#g1v5) | Processador BATCH · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [G.1.v6](#g1v6) | Processador BATCH · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [G.1.v7](#g1v7) | Processador QUEUE · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [G.1.v8](#g1v8) | Processador QUEUE · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [G.1.v9](#g1v9) | Processador QUEUE · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [G.1.v10](#g1v10) | Processador QUEUE · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [G.1.v11](#g1v11) | Processador QUEUE · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [G.1.v12](#g1v12) | Processador QUEUE · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="g1v1"></a>

### G.1.v1 — Processador BATCH · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | processador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v2"></a>

### G.1.v2 — Processador BATCH · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | processador | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 10 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v3"></a>

### G.1.v3 — Processador BATCH · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | processador | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v4"></a>

### G.1.v4 — Processador BATCH · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | processador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | processador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | processador | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 11 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v5"></a>

### G.1.v5 — Processador BATCH · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | processador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | processador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | processador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v6"></a>

### G.1.v6 — Processador BATCH · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | processador | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v7"></a>

### G.1.v7 — Processador QUEUE · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | processador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v8"></a>

### G.1.v8 — Processador QUEUE · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | processador | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 10 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v9"></a>

### G.1.v9 — Processador QUEUE · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | processador | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v10"></a>

### G.1.v10 — Processador QUEUE · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | processador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | processador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | processador | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 11 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v11"></a>

### G.1.v11 — Processador QUEUE · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | processador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | processador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | processador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

<a id="g1v12"></a>

### G.1.v12 — Processador QUEUE · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | processador | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | processador | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

