# OUT ASYNC — Salesforce envia sem esperar

> Gerado a partir das definições da base de integração. Convenções, legenda e códigos de variante: [README](README.md).

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

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Método @future | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional |

### D.1.v2 — @future · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Método @future | Sistema externo | Obrigatório |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional |

### D.1.v3 — @future · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Método @future | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional |

### D.1.v4 — @future · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Método @future | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Método @future | — | Obrigatório |
| 8 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Método @future | endpoint de token do sistema externo | Opcional |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional |

### D.1.v5 — @future · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Método @future | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Método @future | — | Obrigatório |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Método @future | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional |

### D.1.v6 — @future · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Método @future → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Método @future | ApexClass | executa | `@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação | Classe handler | Sistema externo | Obrigatório |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Método @future | — | Obrigatório |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Método @future | — | Obrigatório |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Método @future | Trigger (de novo) | Opcional |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Método @future | — | Opcional |

### D.1.v7 — Queueable · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório |
| 8 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 12 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### D.1.v8 — Queueable · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 7 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | Sistema externo | Obrigatório |
| 8 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 9 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### D.1.v9 — Queueable · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### D.1.v10 — Queueable · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório |
| 9 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional |
| 10 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 13 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### D.1.v11 — Queueable · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório |
| 10 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 13 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### D.1.v12 — Queueable · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | filtra registros elegíveis e enfileira o processamento assíncrono | Trigger | processamento assíncrono | Obrigatório |
| 5 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Classe handler | Sistema externo | Obrigatório |
| 6 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 7 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe Queueable | Trigger (de novo) | Opcional |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe handler | — | Opcional |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |


## D.2

**Flow record-triggered → caminho assíncrono → callout**

Versão declarativa do D.1.

### D.2.v1 — Ação HTTP Callout · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow | — | Obrigatório |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional |

### D.2.v2 — Ação HTTP Callout · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow | — | Obrigatório |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional |

### D.2.v3 — Ação External Service · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow | — | Obrigatório |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional |

### D.2.v4 — Ação External Service · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | define a operação chamada | Flow | Named Credential | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow | — | Obrigatório |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Flow | Trigger (de novo) | Opcional |

### D.2.v5 — Ação Apex invocável · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe invocável | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 10 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional |

### D.2.v6 — Ação Apex invocável · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe invocável | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 9 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional |

### D.2.v7 — Ação Apex invocável · endpoint E3

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe invocável | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 8 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional |

### D.2.v8 — Ação Apex invocável · endpoint E4

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe invocável | registro de Custom Metadata | Obrigatório |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe invocável | — | Obrigatório |
| 7 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe invocável | endpoint de token do sistema externo | Opcional |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional |

### D.2.v9 — Ação Apex invocável · endpoint E5

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe invocável | registro de Custom Metadata | Obrigatório |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe invocável | — | Obrigatório |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe invocável | External Credential | Obrigatório |
| 8 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 11 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional |

### D.2.v10 — Ação Apex invocável · endpoint E6

Fluxo principal: Gravação do registro → Flow record-triggered (Run Asynchronously) → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered (Run Asynchronously) | Flow | executa | o caminho assíncrono roda após o commit e permite callout | plataforma (DML) | ação | Obrigatório |
| 4 | Classe invocável | ApexClass | executa | `@InvocableMethod` que faz o callout | Flow | Sistema externo | Obrigatório |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe invocável | — | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 8 | Atualização do registro de origem | CustomObject + CustomField | executa (DML) | grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger | Classe invocável | Trigger (de novo) | Opcional |


## D.3

**Trigger/Flow publica Platform Event → assinante faz o callout**

Desacopla a transação de origem do callout.

> ⚠️ A validar: Callout em Platform Event–Triggered Flow: confirmar se exige caminho assíncrono.

### D.3.v1 — Publica Apex · assina Apex Trigger + Queueable · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 11 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório |
| 12 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 14 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 15 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v2 — Publica Apex · assina Apex Trigger + Queueable · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 11 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | Sistema externo | Obrigatório |
| 12 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 13 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v3 — Publica Apex · assina Apex Trigger + Queueable · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v4 — Publica Apex · assina Apex Trigger + Queueable · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 11 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório |
| 12 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório |
| 13 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional |
| 14 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 15 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 16 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v5 — Publica Apex · assina Apex Trigger + Queueable · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 11 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório |
| 12 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório |
| 13 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório |
| 14 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 15 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 16 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v6 — Publica Apex · assina Apex Trigger + Queueable · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 7 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 8 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 9 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 10 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 11 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v7 — Publica Apex · assina Flow · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Flow disparado por evento → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 7 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório |
| 8 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow disparado por evento | External Credential | Obrigatório |
| 10 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow disparado por evento | — | Obrigatório |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v8 — Publica Apex · assina Flow · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Flow disparado por evento → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | monta e publica o evento (`EventBus.publish`) | Trigger | Platform Event | Obrigatório |
| 5 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 6 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 7 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório |
| 8 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow disparado por evento | Sistema externo | Obrigatório |
| 10 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 11 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow disparado por evento | — | Obrigatório |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v9 — Publica Flow · assina Apex Trigger + Queueable · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 10 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório |
| 11 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 13 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v10 — Publica Flow · assina Apex Trigger + Queueable · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 10 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | Sistema externo | Obrigatório |
| 11 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 12 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v11 — Publica Flow · assina Apex Trigger + Queueable · endpoint E3

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v12 — Publica Flow · assina Apex Trigger + Queueable · endpoint E4

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 10 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório |
| 11 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório |
| 12 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional |
| 13 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 14 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 15 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v13 — Publica Flow · assina Apex Trigger + Queueable · endpoint E5

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 10 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório |
| 11 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório |
| 12 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório |
| 13 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 14 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 15 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v14 — Publica Flow · assina Apex Trigger + Queueable · endpoint E6

Fluxo principal: Gravação do registro → Flow record-triggered → Trigger do evento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 6 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; não pode fazer callout direto: enfileira | barramento de eventos | Classe Queueable | Obrigatório |
| 7 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário de execução e tamanho do lote do trigger | plataforma | — | Opcional |
| 8 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do evento | Sistema externo | Obrigatório |
| 9 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 10 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v15 — Publica Flow · assina Flow · endpoint E1

Fluxo principal: Gravação do registro → Flow record-triggered → Flow disparado por evento → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 6 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório |
| 7 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow disparado por evento | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow disparado por evento | — | Obrigatório |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |

### D.3.v16 — Publica Flow · assina Flow · endpoint E2

Fluxo principal: Gravação do registro → Flow record-triggered → Flow disparado por evento → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | Flow | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara | — | Flow | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | elemento Create Records no evento `__e` | plataforma (DML) | Platform Event | Obrigatório |
| 4 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 5 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 6 | Flow disparado por evento | Flow | executa | Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service | barramento de eventos | Named Credential | Obrigatório |
| 7 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow disparado por evento | Named Credential | Obrigatório |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow disparado por evento | Sistema externo | Obrigatório |
| 9 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 10 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow disparado por evento | — | Obrigatório |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | assinante | — | Opcional |


## D.4

**Outbound Message (SOAP com retry)**

Legado; ainda comum em orgs antigas.

> Observação: Não usa Named Credential nem Remote Site Setting.
> ⚠️ A validar: Disponibilidade da ação Outbound Message em record-triggered Flow e na criação de novas Workflow Rules.

### D.4.v1 — Workflow Rule · sem certificado

Fluxo principal: Gravação do registro → Regra de workflow → Usuário de envio → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório |
| 3 | Regra de workflow | Workflow (WorkflowRule) | executa | critério que dispara a mensagem (legado) | plataforma (DML) | Outbound Message | Obrigatório |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório |

### D.4.v2 — Workflow Rule · com certificado

Fluxo principal: Gravação do registro → Regra de workflow → Usuário de envio → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório |
| 3 | Regra de workflow | Workflow (WorkflowRule) | executa | critério que dispara a mensagem (legado) | plataforma (DML) | Outbound Message | Obrigatório |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | certificado de cliente para mutual TLS | Outbound Message | — | Obrigatório |
| 7 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório |

### D.4.v3 — Flow · sem certificado

Fluxo principal: Gravação do registro → Flow record-triggered → Usuário de envio → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | ação Outbound Message | plataforma (DML) | Outbound Message | Obrigatório |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório |

### D.4.v4 — Flow · com certificado

Fluxo principal: Gravação do registro → Flow record-triggered → Usuário de envio → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update | — | regra | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | campos enviados na mensagem | — | regra | Obrigatório |
| 3 | Flow record-triggered | Flow | executa | ação Outbound Message | plataforma (DML) | Outbound Message | Obrigatório |
| 4 | Outbound Message | Workflow (WorkflowOutboundMessage) | lê/referencia | endpoint, campos, usuário de envio; fila com retry até 24 h | regra | Sistema externo | Obrigatório |
| 5 | Usuário de envio | não é metadata | ator | usuário cujo contexto define a visibilidade dos campos | Outbound Message | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | certificado de cliente para mutual TLS | Outbound Message | — | Obrigatório |
| 7 | Sistema externo | não é metadata | ator | listener SOAP que devolve `ack=true` | Outbound Message | — | Obrigatório |


## E.1

**Platform Event publicado → sistema externo assina**

O Salesforce publica; o externo consome via Pub/Sub API.

### E.1.v1 — Publicador APEX · assinante autenticado por Connected App

Fluxo principal: Classe publicadora → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe publicadora | ApexClass | executa | `EventBus.publish` | trigger/serviço | Platform Event | Obrigatório |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 6 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.1.v2 — Publicador APEX · assinante autenticado por External Client App

Fluxo principal: Classe publicadora → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe publicadora | ApexClass | executa | `EventBus.publish` | trigger/serviço | Platform Event | Obrigatório |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 6 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 7 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 8 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 9 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 10 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 11 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 12 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 13 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 14 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 15 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 16 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.1.v3 — Publicador FLOW · assinante autenticado por Connected App

Fluxo principal: Flow publicador → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow publicador | Flow | executa | Create Records no `__e` | plataforma | Platform Event | Obrigatório |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 6 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.1.v4 — Publicador FLOW · assinante autenticado por External Client App

Fluxo principal: Flow publicador → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow publicador | Flow | executa | Create Records no `__e` | plataforma | Platform Event | Obrigatório |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 6 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 7 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 8 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 9 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 10 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 11 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 12 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 13 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 14 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 15 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 16 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.1.v5 — Publicador API · assinante autenticado por Connected App

Fluxo principal: Outro sistema → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Outro sistema | não é metadata | ator | publica via REST/Pub/Sub API | — | Platform Event | Obrigatório |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 6 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.1.v6 — Publicador API · assinante autenticado por External Client App

Fluxo principal: Outro sistema → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Outro sistema | não é metadata | ator | publica via REST/Pub/Sub API | — | Platform Event | Obrigatório |
| 2 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 3 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 6 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 7 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 8 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 9 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 10 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 11 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 12 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 13 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 14 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 15 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 16 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |


## E.2

**Change Data Capture**

Mudanças em registros viram eventos sem código de publicação.

### E.2.v1 — Assinante externo · Connected App

Fluxo principal: Gravação do registro → Change Event → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 7 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 9 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 10 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.2.v2 — Assinante externo · External Client App

Fluxo principal: Gravação do registro → Change Event → Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 7 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 13 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 14 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.2.v3 — Assinante interno (Apex) · endpoint E1

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable | External Credential | Obrigatório |
| 10 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |

### E.2.v4 — Assinante interno (Apex) · endpoint E2

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable | Sistema externo | Obrigatório |
| 10 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 11 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |

### E.2.v5 — Assinante interno (Apex) · endpoint E3

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |

### E.2.v6 — Assinante interno (Apex) · endpoint E4

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable | registro de Custom Metadata | Obrigatório |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable | — | Obrigatório |
| 11 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable | endpoint de token do sistema externo | Opcional |
| 12 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 13 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |

### E.2.v7 — Assinante interno (Apex) · endpoint E5

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable | registro de Custom Metadata | Obrigatório |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable | — | Obrigatório |
| 11 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable | External Credential | Obrigatório |
| 12 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |

### E.2.v8 — Assinante interno (Apex) · endpoint E6

Fluxo principal: Gravação do registro → Change Event → Trigger do change event → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | qualquer DML | — | plataforma | Obrigatório |
| 2 | Objeto monitorado | CustomObject | lê/referencia | objeto cujas mudanças viram eventos | — | Change Event | Obrigatório |
| 3 | Membro do canal ChangeEvents | PlatformEventChannelMember | lê/referencia | habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent) | plataforma | Change Event | Obrigatório |
| 4 | Change Event | não é metadata | ator | evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio | plataforma | assinantes | Obrigatório |
| 5 | Trigger do change event | ApexTrigger | executa | `after insert` no ChangeEvent; enfileira o callout | barramento | Classe Queueable | Obrigatório |
| 6 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 7 | Classe Queueable | ApexClass | executa | implementa `Queueable, Database.AllowsCallouts`; faz o callout | Trigger do change event | Sistema externo | Obrigatório |
| 8 | Finalizer | ApexClass | executa | implementa `System.Finalizer`: trata falha e reenfileira | plataforma (fim do Queueable) | Classe Queueable | Opcional |
| 9 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable | — | Obrigatório |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable | — | Obrigatório |


## E.3

**Canal customizado com enriquecimento e filtro**

Seleciona eventos, adiciona campos e filtra antes de entregar.

### E.3.v1 — CDC · Connected App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo data que agrupa eventos | plataforma | assinantes | Obrigatório |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório |
| 3 | Objeto monitorado | CustomObject | lê/referencia | origem do change event | — | Canal | Obrigatório |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 6 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.3.v2 — CDC · External Client App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo data que agrupa eventos | plataforma | assinantes | Obrigatório |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório |
| 3 | Objeto monitorado | CustomObject | lê/referencia | origem do change event | — | Canal | Obrigatório |
| 4 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 6 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 7 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 8 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 9 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 10 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 11 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 12 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 13 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 14 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 15 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 16 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.3.v3 — PE · Connected App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo event que agrupa eventos | plataforma | assinantes | Obrigatório |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório |
| 3 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 4 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 7 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 8 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 9 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 10 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 11 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 12 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 13 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |

### E.3.v4 — PE · External Client App

Fluxo principal: Pub/Sub API (ou CometD) → Sistema externo → Usuário de integração

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Canal customizado | PlatformEventChannel | lê/referencia | canal do tipo event que agrupa eventos | plataforma | assinantes | Obrigatório |
| 2 | Membro do canal | PlatformEventChannelMember | lê/referencia | inclui o evento/objeto; define campos de enriquecimento e filtro | Canal | — | Obrigatório |
| 3 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 4 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 5 | Pub/Sub API (ou CometD) | não é metadata | ator | entrega os eventos ao assinante | barramento | Sistema externo | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | assinante gRPC/CometD; trata replay ID | — | Pub/Sub API | Obrigatório |
| 7 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 8 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 9 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 10 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 11 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 12 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 13 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 14 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 15 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 16 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 17 | Permission Set (leitura do evento / do objeto) | PermissionSet | autoriza | Read no `__e` ou no objeto do CDC | plataforma | — | Obrigatório |


## E.4

**Event Relay → Amazon EventBridge**

Ponte nativa de eventos com a AWS.

> Observação: Envia eventos para fora do Salesforce (AWS).
> ⚠️ A validar: Tipo exato da Named Credential usada pelo Event Relay.

### E.4.v1 — PE

Fluxo principal: Event Relay → Amazon EventBridge

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | publicador | assinantes | Obrigatório |
| 2 | Campos do evento | CustomField | lê/referencia | payload | publicador | — | Obrigatório |
| 3 | Canal customizado | PlatformEventChannel | lê/referencia | canal que o relay lê | plataforma | Event Relay | Obrigatório |
| 4 | Membro do canal | PlatformEventChannelMember | lê/referencia | eventos incluídos no canal | Canal | — | Obrigatório |
| 5 | Event Relay | EventRelayConfig | executa | retransmite os eventos do canal ao destino | plataforma | Named Credential | Obrigatório |
| 6 | Named Credential (destino AWS) | NamedCredential | lê/referencia | aponta para a conta/região AWS (EventBridge partner event source) | Event Relay | Amazon EventBridge | Obrigatório |
| 7 | Amazon EventBridge | não é metadata | ator | recebe os eventos; regras roteiam para outros serviços | Event Relay | — | Obrigatório |

### E.4.v2 — CDC

Fluxo principal: Event Relay → Amazon EventBridge

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Objeto monitorado | CustomObject | lê/referencia | origem do change event | — | Canal | Obrigatório |
| 2 | Canal customizado | PlatformEventChannel | lê/referencia | canal que o relay lê | plataforma | Event Relay | Obrigatório |
| 3 | Membro do canal | PlatformEventChannelMember | lê/referencia | eventos incluídos no canal | Canal | — | Obrigatório |
| 4 | Event Relay | EventRelayConfig | executa | retransmite os eventos do canal ao destino | plataforma | Named Credential | Obrigatório |
| 5 | Named Credential (destino AWS) | NamedCredential | lê/referencia | aponta para a conta/região AWS (EventBridge partner event source) | Event Relay | Amazon EventBridge | Obrigatório |
| 6 | Amazon EventBridge | não é metadata | ator | recebe os eventos; regras roteiam para outros serviços | Event Relay | — | Obrigatório |


## F.1

**Schedulable → Batch Apex com callout**

Sincronização periódica em lotes.

### F.1.v1 — Envia dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Batch | External Credential | Obrigatório |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v2 — Envia dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Batch | Sistema externo | Obrigatório |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v3 — Envia dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 5 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Batch | — | Opcional |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v4 — Envia dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Batch | registro de Custom Metadata | Obrigatório |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Batch | — | Obrigatório |
| 6 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Batch | endpoint de token do sistema externo | Opcional |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v5 — Envia dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Batch | registro de Custom Metadata | Obrigatório |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Batch | — | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Batch | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v6 — Envia dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Batch | — | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v7 — Busca dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Batch | External Credential | Obrigatório |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v8 — Busca dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Batch | Sistema externo | Obrigatório |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v9 — Busca dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 5 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Batch | — | Opcional |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v10 — Busca dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Batch | registro de Custom Metadata | Obrigatório |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Batch | — | Obrigatório |
| 6 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Batch | endpoint de token do sistema externo | Opcional |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v11 — Busca dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Batch | registro de Custom Metadata | Obrigatório |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Batch | — | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Batch | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |

### F.1.v12 — Busca dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Batch → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Batch | Obrigatório |
| 3 | Classe Batch | ApexClass | executa | `Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote | Classe Schedulable | Sistema externo | Obrigatório |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Batch | — | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Batch | — | Obrigatório |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Batch | — | Obrigatório |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Batch | — | Opcional |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Batch | — | Opcional |


## F.2

**Schedulable → Queueable encadeado (paginação)**

Percorre APIs paginadas.

### F.2.v1 — Envia dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable encadeada | External Credential | Obrigatório |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v2 — Envia dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable encadeada | Sistema externo | Obrigatório |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v3 — Envia dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 5 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable encadeada | — | Opcional |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v4 — Envia dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable encadeada | — | Obrigatório |
| 6 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable encadeada | endpoint de token do sistema externo | Opcional |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v5 — Envia dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable encadeada | — | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable encadeada | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v6 — Envia dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable encadeada | — | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v7 — Busca dados · endpoint E1

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Queueable encadeada | External Credential | Obrigatório |
| 5 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 9 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v8 — Busca dados · endpoint E2

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Queueable encadeada | Sistema externo | Obrigatório |
| 5 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 6 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 8 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 9 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v9 — Busca dados · endpoint E3

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 5 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Queueable encadeada | — | Opcional |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v10 — Busca dados · endpoint E4

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Queueable encadeada | — | Obrigatório |
| 6 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Queueable encadeada | endpoint de token do sistema externo | Opcional |
| 7 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v11 — Busca dados · endpoint E5

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Queueable encadeada | registro de Custom Metadata | Obrigatório |
| 5 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Queueable encadeada | — | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Queueable encadeada | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 10 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |

### F.2.v12 — Busca dados · endpoint E6

Fluxo principal: Agendamento → Classe Schedulable → Classe Queueable encadeada → Sistema externo → Objeto de destino/origem

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Agendamento | não é metadata | ator | job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata | — | Classe Schedulable | Obrigatório |
| 2 | Classe Schedulable | ApexClass | executa | `execute(SchedulableContext)` inicia o processamento | Agendamento | Queueable | Obrigatório |
| 3 | Classe Queueable encadeada | ApexClass | executa | busca uma página e enfileira a próxima (`System.enqueueJob`) | Classe Schedulable / ela mesma | Sistema externo | Obrigatório |
| 4 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Queueable encadeada | — | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Queueable encadeada | — | Obrigatório |
| 7 | Objeto de destino/origem | CustomObject + CustomField (External ID) | executa (DML) | registros enviados ou gravados com o retorno | Classe Queueable encadeada | — | Obrigatório |
| 8 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable encadeada | — | Opcional |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe Queueable encadeada | — | Opcional |


## F.3

**Flow agendado → callout**

Versão declarativa do F.1.

> ⚠️ A validar: Suporte a HTTP Callout em Schedule-Triggered Flow.

### F.3.v1 — Ação HTTP · endpoint E1

Fluxo principal: Flow agendado → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow agendado | External Credential | Obrigatório |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow agendado | — | Obrigatório |

### F.3.v2 — Ação HTTP · endpoint E2

Fluxo principal: Flow agendado → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow agendado | Sistema externo | Obrigatório |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow agendado | — | Obrigatório |

### F.3.v3 — Ação ES · endpoint E1

Fluxo principal: Flow agendado → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Flow agendado | External Credential | Obrigatório |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow agendado | — | Obrigatório |

### F.3.v4 — Ação ES · endpoint E2

Fluxo principal: Flow agendado → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Ação HTTP Callout / External Service | ExternalServiceRegistration | lê/referencia | operação chamada | Flow agendado | Named Credential | Obrigatório |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Flow agendado | Sistema externo | Obrigatório |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Flow agendado | — | Obrigatório |

### F.3.v5 — Ação APEX · endpoint E1

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório |
| 3 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe invocável | External Credential | Obrigatório |
| 4 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 5 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |

### F.3.v6 — Ação APEX · endpoint E2

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório |
| 3 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe invocável | Sistema externo | Obrigatório |
| 4 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 5 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 6 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |

### F.3.v7 — Ação APEX · endpoint E3

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório |
| 3 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 4 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe invocável | — | Opcional |
| 5 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |

### F.3.v8 — Ação APEX · endpoint E4

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório |
| 3 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe invocável | registro de Custom Metadata | Obrigatório |
| 4 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe invocável | — | Obrigatório |
| 5 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe invocável | endpoint de token do sistema externo | Opcional |
| 6 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |

### F.3.v9 — Ação APEX · endpoint E5

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório |
| 3 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe invocável | registro de Custom Metadata | Obrigatório |
| 4 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe invocável | — | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe invocável | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |

### F.3.v10 — Ação APEX · endpoint E6

Fluxo principal: Flow agendado → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Flow agendado | Flow (Schedule-Triggered) | executa | roda na frequência configurada sobre os registros que atendem ao filtro | plataforma (agenda) | ação | Obrigatório |
| 2 | Classe invocável | ApexClass | executa | faz o callout | Flow agendado | Sistema externo | Obrigatório |
| 3 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe invocável | — | Obrigatório |
| 4 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |


## F.4

**Apex → Bulk API 2.0 de outra org**

Carga entre orgs.

### F.4.v1 — BATCH · endpoint E1

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório |
| 2 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe de carga | External Credential | Obrigatório |
| 3 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Org Salesforce de destino | Obrigatório |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 5 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 6 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório |
| 7 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório |

### F.4.v2 — BATCH · endpoint E2

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe de carga | Org Salesforce de destino | Obrigatório |
| 3 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 4 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 5 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório |
| 6 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório |

### F.4.v3 — BATCH · endpoint E5

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Batch que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe de carga | registro de Custom Metadata | Obrigatório |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe de carga | — | Obrigatório |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe de carga | External Credential | Obrigatório |
| 5 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Org Salesforce de destino | Obrigatório |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório |
| 8 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório |

### F.4.v4 — QUEUE · endpoint E1

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório |
| 2 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe de carga | External Credential | Obrigatório |
| 3 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Org Salesforce de destino | Obrigatório |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 5 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 6 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório |
| 7 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório |

### F.4.v5 — QUEUE · endpoint E2

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe de carga | Org Salesforce de destino | Obrigatório |
| 3 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 4 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 5 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório |
| 6 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório |

### F.4.v6 — QUEUE · endpoint E5

Fluxo principal: Classe de carga → Org Salesforce de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe de carga | ApexClass | executa | Queueable que cria o job Bulk API 2.0 na org de destino | agenda/trigger | org de destino | Obrigatório |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe de carga | registro de Custom Metadata | Obrigatório |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe de carga | — | Obrigatório |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe de carga | External Credential | Obrigatório |
| 5 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Org Salesforce de destino | Obrigatório |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Org Salesforce de destino | não é metadata | ator | recebe a requisição e devolve a resposta | Classe de carga | — | Obrigatório |
| 8 | Connected App / External Client App (na org de destino) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token aceito pela org de destino | Named Credential | — | Obrigatório |


## G.1

**Fila de integração em objeto (staging) + processador**

Resiliência com status, tentativas e reprocessamento.

### G.1.v1 — Processador BATCH · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | processador | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 13 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v2 — Processador BATCH · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | processador | Sistema externo | Obrigatório |
| 9 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 10 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 12 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v3 — Processador BATCH · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | processador | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v4 — Processador BATCH · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | processador | registro de Custom Metadata | Obrigatório |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | processador | — | Obrigatório |
| 10 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | processador | endpoint de token do sistema externo | Opcional |
| 11 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v5 — Processador BATCH · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | processador | registro de Custom Metadata | Obrigatório |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | processador | — | Obrigatório |
| 10 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | processador | External Credential | Obrigatório |
| 11 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v6 — Processador BATCH · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Schedulable + Batch → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Schedulable + Batch | ApexClass | executa | lê os PENDENTES, faz callout, atualiza status e tentativas | Agendamento | Sistema externo | Obrigatório |
| 8 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | processador | — | Obrigatório |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v7 — Processador QUEUE · endpoint E1

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | processador | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 13 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v8 — Processador QUEUE · endpoint E2

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | processador | Sistema externo | Obrigatório |
| 9 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 10 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 12 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v9 — Processador QUEUE · endpoint E3

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | processador | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v10 — Processador QUEUE · endpoint E4

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | processador | registro de Custom Metadata | Obrigatório |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | processador | — | Obrigatório |
| 10 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | processador | endpoint de token do sistema externo | Opcional |
| 11 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v11 — Processador QUEUE · endpoint E5

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | processador | registro de Custom Metadata | Obrigatório |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | processador | — | Obrigatório |
| 10 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | processador | External Credential | Obrigatório |
| 11 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 14 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

### G.1.v12 — Processador QUEUE · endpoint E6

Fluxo principal: Gravação do registro → Trigger → Classe handler → Objeto de fila / staging → Agendamento → Classe Queueable → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Gravação do registro | não é metadata | ator | insert/update/delete por usuário, API ou automação | — | Trigger | Obrigatório |
| 2 | Objeto de origem | CustomObject + CustomField | lê/referencia | registro que dispara a integração | — | Trigger | Obrigatório |
| 3 | Trigger | ApexTrigger | executa | detecta a mudança (após commit lógico) e delega | plataforma (DML) | Classe handler | Obrigatório |
| 4 | Classe handler | ApexClass | executa | grava um registro de fila com o payload/estado PENDENTE | Trigger | Objeto de fila | Obrigatório |
| 5 | Objeto de fila / staging | CustomObject (__c) + CustomField | executa (DML) | fila persistente: status, tentativas, payload, erro | Classe handler | processador | Obrigatório |
| 6 | Agendamento | não é metadata | ator | CronTrigger | — | processador | Obrigatório |
| 7 | Classe Queueable | ApexClass | executa | processa a fila e reenfileira enquanto houver itens | Classe handler ou Schedulable | Sistema externo | Obrigatório |
| 8 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | processador | — | Obrigatório |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | processador | — | Obrigatório |
| 11 | Notificação de falha | CustomNotificationType ou EmailTemplate | executa | alerta após esgotar tentativas | processador | — | Opcional |

