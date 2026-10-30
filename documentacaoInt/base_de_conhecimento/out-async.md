# OUT ASYNC — Salesforce envia sem esperar

> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta.

Convenções, legenda e códigos de variante: [README](README.md). Fontes citadas entre colchetes: [fontes_validacao.md](fontes_validacao.md).

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

### D.1.v1 — @future · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Método @future | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v2 — @future · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Método @future | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v3 — @future · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Método @future | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v4 — @future · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Método @future | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Método @future | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Método @future | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v5 — @future · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Método @future | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Método @future | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Método @future | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v6 — @future · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório | C06 `@future(callout=true)` em `classes/*.cls` |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Método @future | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v7 — Queueable · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v8 — Queueable · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 9 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v9 — Queueable · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v10 — Queueable · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 10 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v11 — Queueable · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.1.v12 — Queueable · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 7 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## D.2

**Flow record-triggered → caminho assíncrono → callout**

Versão declarativa do D.1.

### D.2.v1 — Ação HTTP Callout · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v2 — Ação HTTP Callout · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v3 — Ação External Service · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v4 — Ação External Service · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v5 — Ação Apex invocável · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v6 — Ação Apex invocável · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe invocável | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v7 — Ação Apex invocável · endpoint E3

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe invocável | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v8 — Ação Apex invocável · endpoint E4

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe invocável | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v9 — Ação Apex invocável · endpoint E5

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.2.v10 — Ação Apex invocável · endpoint E6

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe invocável | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## D.3

**Trigger/Flow publica Platform Event → assinante faz o callout**

Desacopla a transação de origem do callout.

> Observação: Confirmado [PE-SUB]: em trigger de Platform Event, "with some exceptions, you generally can’t make Apex callouts" — por isso o assinante Apex enfileira um Queueable.
> ⚠️ A validar: Callout em Platform Event–Triggered Flow: não encontrado nas páginas consultadas.

### D.3.v1 — Publica Apex · assina Apex Trigger + Queueable · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 11 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 15 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v2 — Publica Apex · assina Apex Trigger + Queueable · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 11 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 13 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v3 — Publica Apex · assina Apex Trigger + Queueable · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v4 — Publica Apex · assina Apex Trigger + Queueable · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 11 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 12 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 13 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 14 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 15 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 16 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v5 — Publica Apex · assina Apex Trigger + Queueable · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 11 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 12 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 13 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 14 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 15 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v6 — Publica Apex · assina Apex Trigger + Queueable · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 11 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v7 — Publica Apex · assina Flow · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Flow disparado por evento → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 8 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow disparado por evento | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow disparado por evento | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v8 — Publica Apex · assina Flow · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Flow disparado por evento → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 7 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 8 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow disparado por evento | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 11 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow disparado por evento | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v9 — Publica Flow · assina Apex Trigger + Queueable · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 10 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v10 — Publica Flow · assina Apex Trigger + Queueable · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 10 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 12 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v11 — Publica Flow · assina Apex Trigger + Queueable · endpoint E3

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v12 — Publica Flow · assina Apex Trigger + Queueable · endpoint E4

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 10 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 12 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 13 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 14 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 15 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v13 — Publica Flow · assina Apex Trigger + Queueable · endpoint E5

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 10 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 12 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 13 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 14 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v14 — Publica Flow · assina Apex Trigger + Queueable · endpoint E6

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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
| 10 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v15 — Publica Flow · assina Flow · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered → Flow disparado por evento → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 7 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow disparado por evento | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow disparado por evento | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

### D.3.v16 — Publica Flow · assina Flow · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered → Flow disparado por evento → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 6 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 7 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow disparado por evento | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 10 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow disparado por evento | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## D.4

**Outbound Message (SOAP com retry)**

Legado; ainda comum em orgs antigas.

> Observação: Não usa Named Credential nem Remote Site Setting.
> Observação: No XML [MA-WF]: `workflows/Objeto.workflow` → `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`) e ação `type`=OutboundMessage na regra.
> ⚠️ A validar: Ação Outbound Message em Flow: o valor não aparece na lista de `actionType` (InvocableActionType) da página Flow [MA-FLOW]. Criação de novas Workflow Rules: não verificado.

### D.4.v1 — Workflow Rule · sem certificado

Fluxo principal: Gravação do registro → Regra de workflow → Usuário de envio → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Regra de workflow | Workflow (WorkflowRule) | executa | critério que dispara a mensagem (legado) | plataforma (DML) | Outbound Message | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |

### D.4.v2 — Workflow Rule · com certificado

Fluxo principal: Gravação do registro → Regra de workflow → Usuário de envio → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Regra de workflow | Workflow (WorkflowRule) | executa | critério que dispara a mensagem (legado) | plataforma (DML) | Outbound Message | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Certificate | Certificate | autoriza | certificado de cliente para mutual TLS | Outbound Message | — | Obrigatório | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |

### D.4.v3 — Flow · sem certificado

Fluxo principal: Gravação do registro → Flow record-triggered → Usuário de envio → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Flow record-triggered | Flow | executa | ação Outbound Message | plataforma (DML) | Outbound Message | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório | `workflows/*.workflow` — `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`, `apiVersion`), `rules` com ação `OutboundMessage` [MA-WF] |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório | não aparece no projeto (ator) |

### D.4.v4 — Flow · com certificado

Fluxo principal: Gravação do registro → Flow record-triggered → Usuário de envio → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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

### E.1.v1 — Publicador APEX · assinante autenticado por Connected App

Fluxo principal: Classe publicadora → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe publicadora | ApexClass | executa | `EventBus.publish` | trigger/serviço | Platform Event | Obrigatório | C18 `EventBus.publish(` |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.1.v2 — Publicador APEX · assinante autenticado por External Client App

Fluxo principal: Classe publicadora → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe publicadora | ApexClass | executa | `EventBus.publish` | trigger/serviço | Platform Event | Obrigatório | C18 `EventBus.publish(` |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.1.v3 — Publicador FLOW · assinante autenticado por Connected App

Fluxo principal: Flow publicador → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow publicador | Flow | executa | Create Records no `__e` | plataforma | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.1.v4 — Publicador FLOW · assinante autenticado por External Client App

Fluxo principal: Flow publicador → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow publicador | Flow | executa | Create Records no `__e` | plataforma | Platform Event | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.1.v5 — Publicador API · assinante autenticado por Connected App

Fluxo principal: Outro sistema → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Outro sistema | não é metadata | ator | publica via REST/Pub/Sub API | — | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.1.v6 — Publicador API · assinante autenticado por External Client App

Fluxo principal: Outro sistema → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Outro sistema | não é metadata | ator | publica via REST/Pub/Sub API | — | Platform Event | Obrigatório | não aparece no projeto (ator) |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## E.2

**Change Data Capture**

Mudanças em registros viram eventos sem código de publicação.

### E.2.v1 — Assinante externo · Connected App

Fluxo principal: Gravação do registro → Change Event → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 7 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 8 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 9 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 12 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 13 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 14 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.2.v2 — Assinante externo · External Client App

Fluxo principal: Gravação do registro → Change Event → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 7 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 8 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 9 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 10 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 11 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 12 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 13 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 16 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 17 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 18 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.2.v3 — Assinante interno (Apex) · endpoint E1

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

### E.2.v4 — Assinante interno (Apex) · endpoint E2

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 11 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

### E.2.v5 — Assinante interno (Apex) · endpoint E3

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

### E.2.v6 — Assinante interno (Apex) · endpoint E4

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 12 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 13 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

### E.2.v7 — Assinante interno (Apex) · endpoint E5

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |

### E.2.v8 — Assinante interno (Apex) · endpoint E6

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório | não aparece no projeto (ator) |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório | C21 `trigger ... on XChangeEvent (after insert)` |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional | `PlatformEventSubscriberConfigs/*.platformEventSubscriberConfig` — `platformEventConsumer` (trigger), `user`, `batchSize` (1–2.000), `numPartitions`, `partitionKey` [MA-PESC] |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional | C10 `implements System.Finalizer` |
| 9 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório | não aparece no projeto (ator) |


## E.3

**Canal customizado com enriquecimento e filtro**

Seleciona eventos, adiciona campos e filtra antes de entregar.

### E.3.v1 — CDC · Connected App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo data que agrupa eventos | plataforma | assinantes | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 3 | Objeto monitorado | CustomObject | lê/referencia | origem do change event | — | Canal | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.3.v2 — CDC · External Client App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo data que agrupa eventos | plataforma | assinantes | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 3 | Objeto monitorado | CustomObject | lê/referencia | origem do change event | — | Canal | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 6 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 7 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.3.v3 — PE · Connected App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo event que agrupa eventos | plataforma | assinantes | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 3 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 4 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 7 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 8 | Connected App | ConnectedApp | autoriza | `oauthConfig`: registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os `scopes` | Sistema externo | Salesforce (emissão do token) | Obrigatório | `connectedApps/*.connectedApp` — `oauthConfig` (`callbackUrl`, `scopes`, `certificate`, `consumerKey`, `isClientCredentialEnabled`, `oauthClientCredentialUser`, `isAdminApproved`), `canvasConfig` (`canvasUrl`), `samlConfig` [MA-CA] |
| 9 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 12 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 13 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 14 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

### E.3.v4 — PE · External Client App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo event que agrupa eventos | plataforma | assinantes | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 3 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 4 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório | não aparece no projeto (ator) |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório | não aparece no projeto (ator) |
| 7 | Assinatura gerenciada | ManagedEventSubscription | lê/referencia | `topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+) | Sistema externo | — | Opcional | `managedEventSubscriptions/*.managedEventSubscription` — `topicName` (/event/..., /data/...), `defaultReplay`, `errorRecoveryReplay`, `state` [MA-MES] |
| 8 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório | `externalClientApps/*.eca` — `label`, `distributionState`, `contactEmail` [MA-ECA] |
| 9 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | escopos (`commaSeparatedOauthScopes`) do fluxo OAuth 2.0 JWT Bearer | External Client App | — | Obrigatório | `extlClntAppOauthSettings/*.ecaOauth` — `externalClientApplication`, `commaSeparatedOauthScopes` [MA-ECAO] |
| 10 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | `callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled` | External Client App | — | Obrigatório | `extlClntAppGlobalOauthSets/*.ecaGlblOauth` — `externalClientApplication`, `callbackUrl`, `certificate`, `consumerKey`, `isClientCredentialsFlowEnabled`, `isPkceRequired` [MA-ECAG] |
| 11 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | `commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser` | External Client App | — | Obrigatório | `extlClntAppOauthPolicies/*.ecaOauthPlcy` — `externalClientApplication`, `clientCredentialsFlowUser`, `isClientCredentialsFlowEnabled`, `ipRelaxationPolicyType`, `commaSeparatedPermissionSet`, `commaSeparatedProfile`, `commaSeparatedCustomScopes` [MA-ECAOP] |
| 12 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório | `extlClntAppPolicies/*.ecaPlcy` — `externalClientApplication` e habilitação do app/plugins [MA-ECAP] |
| 13 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 14 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório | `profiles/*.profile` — `classAccesses`, `userPermissions` (ex.: API habilitada) [MA-PROF] |
| 16 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório | `permissionsets/*.permissionset` [MA-PS] ou `permissionsetgroups/*.permissionsetgroup (nv)` [MA-PSG] |
| 17 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional | `oauthcustomscopes/*.oauthcustomscope` — escopo customizado referenciado pelo app [MA-OCS] |
| 18 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## E.4

**Event Relay → Amazon EventBridge**

Ponte nativa de eventos com a AWS.

> Observação: Envia eventos para fora do Salesforce (AWS).
> Observação: Confirmado [MA-ERC]: `destinationResourceName` é o nome da Named Credential com prefixo `callout:` e guarda a conta AWS; `eventChannel` é um canal `X__chn`.
> ⚠️ A validar: Tipo (`namedCredentialType`) exigido para essa Named Credential: não informado na página.

### E.4.v1 — PE

Fluxo principal: Event Relay → Amazon EventBridge

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório | `objects/X__e/` (sufixo `__e`) [PE-PUB] |
| 2 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 3 | Canal customizado | PlatformEventChannel | lê/referencia | canal que o relay lê | plataforma | Event Relay | Obrigatório | `platformEventChannels/*.platformEventChannel` — `channelType` (data = CDC [MA-PEC] |
| 4 | Membro do canal | PlatformEventChannelMember | lê/referencia | eventos incluídos no canal | Canal | — | Obrigatório | `platformEventChannelMembers/*.platformEventChannelMember` — `eventChannel` (ChangeEvents ou `X__chn`), `selectedEntity` (ex.: AccountChangeEvent), `enrichedFields`, `filterExpression` [MA-PECM] |
| 5 | Event Relay | EventRelayConfig | executa | retransmite os eventos do canal ao destino | plataforma | Named Credential | Obrigatório | `eventRelays/*.eventRelay` — `destinationResourceName` (`callout:NomeNC`, guarda a conta AWS), `eventChannel` (`X__chn`), `relayOption`, `state` [MA-ERC] |
| 6 | Named Credential (destino AWS) | NamedCredential | lê/referencia | aponta para a conta/região AWS (EventBridge partner event source) | Event Relay | Amazon EventBridge | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Amazon EventBridge | não é metadata | ator | recebe os eventos; regras roteiam para outros serviços | Event Relay | — | Obrigatório | não aparece no projeto (ator) |

### E.4.v2 — CDC

Fluxo principal: Event Relay → Amazon EventBridge

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
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

### F.1.v1 — Envia dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Batch | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v2 — Envia dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Batch | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v3 — Envia dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Batch | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v4 — Envia dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Batch | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Batch | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Batch | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v5 — Envia dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Batch | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Batch | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Batch | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v6 — Envia dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Batch | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v7 — Busca dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Batch | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v8 — Busca dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Batch | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v9 — Busca dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Batch | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v10 — Busca dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Batch | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Batch | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Batch | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v11 — Busca dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Batch | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Batch | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Batch | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.1.v12 — Busca dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Batch | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |


## F.2

**Schedulable → Queueable encadeado (paginação)**

Percorre APIs paginadas.

### F.2.v1 — Envia dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable encadeada | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v2 — Envia dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable encadeada | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v3 — Envia dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable encadeada | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v4 — Envia dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable encadeada | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable encadeada | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v5 — Envia dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable encadeada | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable encadeada | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v6 — Envia dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v7 — Busca dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable encadeada | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v8 — Busca dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable encadeada | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v9 — Busca dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable encadeada | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v10 — Busca dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable encadeada | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable encadeada | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v11 — Busca dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable encadeada | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable encadeada | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |

### F.2.v12 — Busca dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório | não aparece no projeto (ator) |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório | C09 `implements Schedulable` |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |


## F.3

**Flow agendado → callout**

Versão declarativa do F.1.

> ⚠️ A validar: Suporte a HTTP Callout em Schedule-Triggered Flow: não encontrado nas páginas consultadas.

### F.3.v1 — Ação HTTP · endpoint E1

Fluxo principal: Flow agendado → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow agendado | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow agendado | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v2 — Ação HTTP · endpoint E2

Fluxo principal: Flow agendado → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow agendado | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow agendado | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v3 — Ação ES · endpoint E1

Fluxo principal: Flow agendado → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow agendado | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow agendado | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v4 — Ação ES · endpoint E2

Fluxo principal: Flow agendado → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow agendado | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow agendado | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v5 — Ação APEX · endpoint E1

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v6 — Ação APEX · endpoint E2

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe invocável | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v7 — Ação APEX · endpoint E3

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 4 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe invocável | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 5 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v8 — Ação APEX · endpoint E4

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe invocável | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 6 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v9 — Ação APEX · endpoint E5

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |

### F.3.v10 — Ação APEX · endpoint E6

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 3 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe invocável | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 5 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |


## F.4

**Apex → Bulk API 2.0 de outra org**

Carga entre orgs.

### F.4.v1 — BATCH · endpoint E1

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe de carga | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Org Salesforce de destino | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 5 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

### F.4.v2 — BATCH · endpoint E2

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe de carga | Org Salesforce de destino | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 4 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 5 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

### F.4.v3 — BATCH · endpoint E5

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe de carga | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe de carga | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe de carga | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Org Salesforce de destino | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

### F.4.v4 — QUEUE · endpoint E1

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe de carga | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Org Salesforce de destino | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 5 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 6 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 7 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

### F.4.v5 — QUEUE · endpoint E2

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe de carga | Org Salesforce de destino | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 3 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 4 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 5 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 6 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |

### F.4.v6 — QUEUE · endpoint E5

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe de carga | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe de carga | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe de carga | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 5 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Org Salesforce de destino | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório | `connectedApps/*.connectedApp` [MA-CA] ou `externalClientApps/*.eca` [MA-ECA] |


## G.1

**Fila de integração em objeto (staging) + processador**

Resiliência com status, tentativas e reprocessamento.

### G.1.v1 — Processador BATCH · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | processador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v2 — Processador BATCH · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | processador | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 10 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v3 — Processador BATCH · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | processador | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v4 — Processador BATCH · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | processador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | processador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | processador | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 11 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v5 — Processador BATCH · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | processador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | processador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | processador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v6 — Processador BATCH · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório | C08 `Database.Batchable` + `Database.AllowsCallouts` |
| 8 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | processador | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v7 — Processador QUEUE · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | processador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | `externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v8 — Processador QUEUE · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | processador | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 10 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v9 — Processador QUEUE · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | processador | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v10 — Processador QUEUE · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | processador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | processador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | processador | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 11 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v11 — Processador QUEUE · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | processador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | processador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | processador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

### G.1.v12 — Processador QUEUE · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório | não aparece no projeto (ator) |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório | `triggers/*.trigger + -meta.xml` — `trigger X on Objeto (...)` [MA-TRG] |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório | não aparece no projeto (ator) |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório | C07 `implements Queueable, Database.AllowsCallouts` |
| 8 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | processador | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional | `notificationtypes/*.notiftype` [MA-CNT] ou `email/*` [MA-ET] |

