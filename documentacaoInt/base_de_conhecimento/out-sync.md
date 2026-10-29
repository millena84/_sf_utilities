# OUT SYNC — Salesforce chama o externo e espera

> Gerado a partir das definições da base de integração. Convenções, legenda e códigos de variante: [README](README.md).

## Índice

- [b.1 — LWC / Screen Flow → cadeia de classes → callout](#b1) (12 variantes)
- [b.2 — LWC / Screen Flow → uma classe que faz o callout](#b2) (12 variantes)
- [b.3 — Screen Flow → ação HTTP Callout (declarativa)](#b3) (2 variantes)
- [b.4 — Flow ou Apex → External Service (OpenAPI)](#b4) (4 variantes)
- [b.5 — LWC / Screen Flow → stub SOAP gerado (WSDL2Apex)](#b5) (12 variantes)
- [b.6 — LWC → Apex Continuation](#b6) (6 variantes)
- [c.1 — FlexCard → Integration Procedure → HTTP Action](#c1) (6 variantes)
- [c.2 — OmniScript → Integration Procedure ou Remote Action](#c2) (9 variantes)
- [d.1 — LWC → fetch direto do navegador](#d1) (3 variantes)
- [e.1 — Salesforce Connect (OData / cross-org)](#e1) (2 variantes)
- [e.2 — Salesforce Connect com adaptador Apex](#e2) (6 variantes)
- [f.1 — Quick Action → Flow ou LWC → callout → atualiza o registro](#f1) (12 variantes)

## b.1

**LWC / Screen Flow → cadeia de classes → callout**

O usuário aciona a tela; o servidor passa por service e client antes do callout. O usuário espera a resposta.

### b.1.v1 — Origem LWC · endpoint E1 (Named Credential (modelo novo) + External Credential)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Controller Apex | Classe cliente HTTP | Obrigatório |
| 6 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe cliente HTTP | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v2 — Origem LWC · endpoint E2 (Named Credential legada (autenticação embutida))

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Controller Apex | Classe cliente HTTP | Obrigatório |
| 6 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe cliente HTTP | Sistema externo | Obrigatório |
| 9 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 10 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v3 — Origem LWC · endpoint E3 (URL fixa no código Apex + Remote Site Setting)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Controller Apex | Classe cliente HTTP | Obrigatório |
| 6 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe cliente HTTP | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v4 — Origem LWC · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Controller Apex | Classe cliente HTTP | Obrigatório |
| 6 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe cliente HTTP | registro de Custom Metadata | Obrigatório |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe cliente HTTP | — | Obrigatório |
| 10 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe cliente HTTP | endpoint de token do sistema externo | Opcional |
| 11 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 14 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 15 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v5 — Origem LWC · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Controller Apex | Classe cliente HTTP | Obrigatório |
| 6 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe cliente HTTP | registro de Custom Metadata | Obrigatório |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe cliente HTTP | — | Obrigatório |
| 10 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe cliente HTTP | External Credential | Obrigatório |
| 11 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 14 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 15 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v6 — Origem LWC · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Controller Apex | Classe cliente HTTP | Obrigatório |
| 6 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 8 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe cliente HTTP | — | Obrigatório |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v7 — Origem Screen Flow · endpoint E1 (Named Credential (modelo novo) + External Credential)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Classe invocável | Classe cliente HTTP | Obrigatório |
| 7 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe cliente HTTP | External Credential | Obrigatório |
| 10 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 14 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 15 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v8 — Origem Screen Flow · endpoint E2 (Named Credential legada (autenticação embutida))

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Classe invocável | Classe cliente HTTP | Obrigatório |
| 7 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe cliente HTTP | Sistema externo | Obrigatório |
| 10 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 11 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v9 — Origem Screen Flow · endpoint E3 (URL fixa no código Apex + Remote Site Setting)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Classe invocável | Classe cliente HTTP | Obrigatório |
| 7 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe cliente HTTP | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v10 — Origem Screen Flow · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Classe invocável | Classe cliente HTTP | Obrigatório |
| 7 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe cliente HTTP | registro de Custom Metadata | Obrigatório |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe cliente HTTP | — | Obrigatório |
| 11 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe cliente HTTP | endpoint de token do sistema externo | Opcional |
| 12 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 13 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 15 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 16 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v11 — Origem Screen Flow · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Classe invocável | Classe cliente HTTP | Obrigatório |
| 7 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe cliente HTTP | registro de Custom Metadata | Obrigatório |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe cliente HTTP | — | Obrigatório |
| 11 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe cliente HTTP | External Credential | Obrigatório |
| 12 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 15 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 16 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |

### b.1.v12 — Origem Screen Flow · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Classe de serviço | ApexClass | executa | regra de negócio e montagem do payload | Classe invocável | Classe cliente HTTP | Obrigatório |
| 7 | Classe cliente HTTP | ApexClass | executa | monta `HttpRequest`, faz o callout e trata a resposta | Classe de serviço | Sistema externo | Obrigatório |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | serializa e desserializa JSON | Classe cliente HTTP | — | Opcional |
| 9 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe cliente HTTP | — | Obrigatório |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente HTTP | — | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe cliente HTTP | — | Opcional |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe cliente HTTP | — | Opcional |


## b.2

**LWC / Screen Flow → uma classe que faz o callout**

Mesmo desenho do b.1, mas o próprio ponto de entrada faz a chamada.

### b.2.v1 — Origem LWC · endpoint E1 (Named Credential (modelo novo) + External Credential)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Componente LWC | Sistema externo | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Controller Apex | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Controller Apex | — | Opcional |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Controller Apex | — | Opcional |

### b.2.v2 — Origem LWC · endpoint E2 (Named Credential legada (autenticação embutida))

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Componente LWC | Sistema externo | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Controller Apex | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Controller Apex | — | Opcional |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Controller Apex | — | Opcional |

### b.2.v3 — Origem LWC · endpoint E3 (URL fixa no código Apex + Remote Site Setting)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Componente LWC | Sistema externo | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Controller Apex | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 8 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Controller Apex | — | Opcional |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Controller Apex | — | Opcional |

### b.2.v4 — Origem LWC · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Componente LWC | Sistema externo | Obrigatório |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Controller Apex | registro de Custom Metadata | Obrigatório |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Controller Apex | — | Obrigatório |
| 7 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Controller Apex | endpoint de token do sistema externo | Opcional |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Controller Apex | — | Opcional |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Controller Apex | — | Opcional |

### b.2.v5 — Origem LWC · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Componente LWC | Sistema externo | Obrigatório |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Controller Apex | registro de Custom Metadata | Obrigatório |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Controller Apex | — | Obrigatório |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Controller Apex | External Credential | Obrigatório |
| 8 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Controller Apex | — | Opcional |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Controller Apex | — | Opcional |

### b.2.v6 — Origem LWC · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Componente LWC | Sistema externo | Obrigatório |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Controller Apex | — | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 8 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Controller Apex | — | Opcional |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Controller Apex | — | Opcional |

### b.2.v7 — Origem Screen Flow · endpoint E1 (Named Credential (modelo novo) + External Credential)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Screen Flow | Sistema externo | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe invocável | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe invocável | — | Opcional |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe invocável | — | Opcional |

### b.2.v8 — Origem Screen Flow · endpoint E2 (Named Credential legada (autenticação embutida))

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Screen Flow | Sistema externo | Obrigatório |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe invocável | Sistema externo | Obrigatório |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe invocável | — | Opcional |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe invocável | — | Opcional |

### b.2.v9 — Origem Screen Flow · endpoint E3 (URL fixa no código Apex + Remote Site Setting)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Screen Flow | Sistema externo | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe invocável | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe invocável | — | Opcional |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe invocável | — | Opcional |

### b.2.v10 — Origem Screen Flow · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Screen Flow | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe invocável | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe invocável | — | Obrigatório |
| 8 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe invocável | endpoint de token do sistema externo | Opcional |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe invocável | — | Opcional |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe invocável | — | Opcional |

### b.2.v11 — Origem Screen Flow · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Screen Flow | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe invocável | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe invocável | — | Obrigatório |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe invocável | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe invocável | — | Opcional |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe invocável | — | Opcional |

### b.2.v12 — Origem Screen Flow · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor e faz o callout (`HttpRequest`) | Screen Flow | Sistema externo | Obrigatório |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe invocável | — | Obrigatório |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | liga/desliga a integração sem deploy de código | Classe invocável | — | Opcional |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe invocável | — | Opcional |


## b.3

**Screen Flow → ação HTTP Callout (declarativa)**

Sem Apex. O assistente de HTTP Callout gera um registro de External Service.

> Observação: HTTP Callout exige Named Credential: as variantes E3–E6 não existem para este desenho.

### b.3.v1 — Endpoint E1 (Named Credential (modelo novo) + External Credential)

Fluxo principal: Usuário → Screen Flow → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | registro gerado pelo assistente de HTTP Callout (método, path, schema de resposta) | Screen Flow | Named Credential | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Ação HTTP Callout | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Ação HTTP Callout | — | Obrigatório |
| 10 | Permission Set (acesso ao Flow) | PermissionSet | autoriza | Run Flows ou acesso ao Flow específico | plataforma | — | Obrigatório |

### b.3.v2 — Endpoint E2 (Named Credential legada (autenticação embutida))

Fluxo principal: Usuário → Screen Flow → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | registro gerado pelo assistente de HTTP Callout (método, path, schema de resposta) | Screen Flow | Named Credential | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Ação HTTP Callout | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Ação HTTP Callout | — | Obrigatório |
| 9 | Permission Set (acesso ao Flow) | PermissionSet | autoriza | Run Flows ou acesso ao Flow específico | plataforma | — | Obrigatório |


## b.4

**Flow ou Apex → External Service (OpenAPI)**

A API é registrada por um schema OpenAPI; Flow e Apex usam as ações geradas.

> Observação: External Services exigem Named Credential.

### b.4.v1 — Origem Screen Flow · endpoint E1

Fluxo principal: Usuário → Screen Flow → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | schema OpenAPI registrado; gera ações invocáveis e classes Apex | Screen Flow | Named Credential | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Registro de External Service | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório |

### b.4.v2 — Origem Screen Flow · endpoint E2

Fluxo principal: Usuário → Screen Flow → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | schema OpenAPI registrado; gera ações invocáveis e classes Apex | Screen Flow | Named Credential | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Registro de External Service | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório |

### b.4.v3 — Origem LWC + Apex · endpoint E1

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | chama a classe gerada no namespace `ExternalService` | Componente LWC | Registro de External Service | Obrigatório |
| 5 | Registro de External Service | ExternalServiceRegistration | lê/referencia | schema OpenAPI registrado; gera ações invocáveis e classes Apex | Controller Apex | Named Credential | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Registro de External Service | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório |

### b.4.v4 — Origem LWC + Apex · endpoint E2

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | chama a classe gerada no namespace `ExternalService` | Componente LWC | Registro de External Service | Obrigatório |
| 5 | Registro de External Service | ExternalServiceRegistration | lê/referencia | schema OpenAPI registrado; gera ações invocáveis e classes Apex | Controller Apex | Named Credential | Obrigatório |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Registro de External Service | Sistema externo | Obrigatório |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Registro de External Service | — | Obrigatório |


## b.5

**LWC / Screen Flow → stub SOAP gerado (WSDL2Apex)**

Callout SOAP com classes geradas a partir do WSDL.

### b.5.v1 — Origem LWC · endpoint E1

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Controller Apex | Sistema externo | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Stub gerado (WSDL2Apex) | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v2 — Origem LWC · endpoint E2

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Controller Apex | Sistema externo | Obrigatório |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Stub gerado (WSDL2Apex) | Sistema externo | Obrigatório |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v3 — Origem LWC · endpoint E3

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Controller Apex | Sistema externo | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Stub gerado (WSDL2Apex) | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v4 — Origem LWC · endpoint E4

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Controller Apex | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Stub gerado (WSDL2Apex) | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 8 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Stub gerado (WSDL2Apex) | endpoint de token do sistema externo | Opcional |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v5 — Origem LWC · endpoint E5

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Controller Apex | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Stub gerado (WSDL2Apex) | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Stub gerado (WSDL2Apex) | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v6 — Origem LWC · endpoint E6

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled`: ponto de entrada no servidor | Componente LWC | próximo componente | Obrigatório |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Controller Apex | Sistema externo | Obrigatório |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v7 — Origem Screen Flow · endpoint E1

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Classe invocável | Sistema externo | Obrigatório |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Stub gerado (WSDL2Apex) | External Credential | Obrigatório |
| 8 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v8 — Origem Screen Flow · endpoint E2

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Classe invocável | Sistema externo | Obrigatório |
| 7 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Stub gerado (WSDL2Apex) | Sistema externo | Obrigatório |
| 8 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 9 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v9 — Origem Screen Flow · endpoint E3

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Classe invocável | Sistema externo | Obrigatório |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Stub gerado (WSDL2Apex) | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v10 — Origem Screen Flow · endpoint E4

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Classe invocável | Sistema externo | Obrigatório |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Stub gerado (WSDL2Apex) | registro de Custom Metadata | Obrigatório |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 9 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Stub gerado (WSDL2Apex) | endpoint de token do sistema externo | Opcional |
| 10 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v11 — Origem Screen Flow · endpoint E5

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Classe invocável | Sistema externo | Obrigatório |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Stub gerado (WSDL2Apex) | registro de Custom Metadata | Obrigatório |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Stub gerado (WSDL2Apex) | External Credential | Obrigatório |
| 10 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### b.5.v12 — Origem Screen Flow · endpoint E6

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | onde o Screen Flow é exposto ao usuário | Usuário | Screen Flow | Opcional |
| 3 | Screen Flow | Flow | executa | coleta dados na tela e chama a ação Apex | Ponto de entrada | Classe invocável | Obrigatório |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | indica a versão ativa (formato legado) | plataforma | — | Opcional |
| 5 | Classe invocável | ApexClass | executa | método `@InvocableMethod`: ponto de entrada no servidor | Screen Flow | próximo componente | Obrigatório |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito | Classe invocável | Sistema externo | Obrigatório |
| 7 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Stub gerado (WSDL2Apex) | — | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |


## b.6

**LWC → Apex Continuation**

Chamada longa (até 120 s) sem prender thread do servidor.

> ⚠️ A validar: Limites e assinatura exata de `@AuraEnabled(continuation=true)` em LWC.

### b.6.v1 — Endpoint E1

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled(continuation=true cacheable=true)` que devolve um `Continuation` | Componente LWC | Sistema externo | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Controller Apex | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 10 | Método de callback | ApexClass | executa | recebe a resposta quando o sistema externo responde e devolve ao LWC | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório |

### b.6.v2 — Endpoint E2

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled(continuation=true cacheable=true)` que devolve um `Continuation` | Componente LWC | Sistema externo | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Controller Apex | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 9 | Método de callback | ApexClass | executa | recebe a resposta quando o sistema externo responde e devolve ao LWC | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório |

### b.6.v3 — Endpoint E3

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled(continuation=true cacheable=true)` que devolve um `Continuation` | Componente LWC | Sistema externo | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Controller Apex | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 8 | Método de callback | ApexClass | executa | recebe a resposta quando o sistema externo responde e devolve ao LWC | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório |

### b.6.v4 — Endpoint E4

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled(continuation=true cacheable=true)` que devolve um `Continuation` | Componente LWC | Sistema externo | Obrigatório |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Controller Apex | registro de Custom Metadata | Obrigatório |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Controller Apex | — | Obrigatório |
| 7 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Controller Apex | endpoint de token do sistema externo | Opcional |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 11 | Método de callback | ApexClass | executa | recebe a resposta quando o sistema externo responde e devolve ao LWC | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório |

### b.6.v5 — Endpoint E5

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled(continuation=true cacheable=true)` que devolve um `Continuation` | Componente LWC | Sistema externo | Obrigatório |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Controller Apex | registro de Custom Metadata | Obrigatório |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Controller Apex | — | Obrigatório |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Controller Apex | External Credential | Obrigatório |
| 8 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 11 | Método de callback | ApexClass | executa | recebe a resposta quando o sistema externo responde e devolve ao LWC | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório |

### b.6.v6 — Endpoint E6

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | posiciona o componente na página de registro, app ou home | Usuário | LWC | Opcional (ou CustomTab / QuickAction) |
| 3 | Componente LWC | LightningComponentBundle | executa | captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire) | Página Lightning | Controller Apex | Obrigatório |
| 4 | Controller Apex | ApexClass | executa | método `@AuraEnabled(continuation=true cacheable=true)` que devolve um `Continuation` | Componente LWC | Sistema externo | Obrigatório |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Controller Apex | — | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 8 | Método de callback | ApexClass | executa | recebe a resposta quando o sistema externo responde e devolve ao LWC | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório |


## c.1

**FlexCard → Integration Procedure → HTTP Action**

Exibição de dado externo via OmniStudio.

> ⚠️ A validar: Nomes de metadata OmniStudio padrão (`OmniUiCard`, `OmniIntegrationProcedure`, `OmniDataTransform`). No pacote gerenciado (Vlocity) esses itens são registros/DataPacks, não metadata.

### c.1.v1 — Sem Data Mapper · endpoint E1

Fluxo principal: Usuário → FlexCard → Integration Procedure → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | exibe a FlexCard | Usuário | FlexCard | Opcional |
| 3 | FlexCard | OmniUiCard | executa | fonte de dados do tipo Integration Procedure | Página Lightning | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra; o elemento HTTP Action faz a chamada | FlexCard | Sistema externo | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Integration Procedure | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório |

### c.1.v2 — Sem Data Mapper · endpoint E2

Fluxo principal: Usuário → FlexCard → Integration Procedure → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | exibe a FlexCard | Usuário | FlexCard | Opcional |
| 3 | FlexCard | OmniUiCard | executa | fonte de dados do tipo Integration Procedure | Página Lightning | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra; o elemento HTTP Action faz a chamada | FlexCard | Sistema externo | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Integration Procedure | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório |

### c.1.v3 — Sem Data Mapper · endpoint E3 (URL fixa na HTTP Action + Remote Site)

Fluxo principal: Usuário → FlexCard → Integration Procedure → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | exibe a FlexCard | Usuário | FlexCard | Opcional |
| 3 | FlexCard | OmniUiCard | executa | fonte de dados do tipo Integration Procedure | Página Lightning | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra; o elemento HTTP Action faz a chamada | FlexCard | Sistema externo | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera a URL fixa configurada na HTTP Action | plataforma | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório |

### c.1.v4 — Com Data Mapper · endpoint E1

Fluxo principal: Usuário → FlexCard → Integration Procedure → Data Mapper / DataRaptor Transform → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | exibe a FlexCard | Usuário | FlexCard | Opcional |
| 3 | FlexCard | OmniUiCard | executa | fonte de dados do tipo Integration Procedure | Página Lightning | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra; o elemento HTTP Action faz a chamada | FlexCard | Sistema externo | Obrigatório |
| 5 | Data Mapper / DataRaptor Transform | OmniDataTransform | executa | transforma a resposta externa no formato da FlexCard | Integration Procedure | — | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Integration Procedure | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório |

### c.1.v5 — Com Data Mapper · endpoint E2

Fluxo principal: Usuário → FlexCard → Integration Procedure → Data Mapper / DataRaptor Transform → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | exibe a FlexCard | Usuário | FlexCard | Opcional |
| 3 | FlexCard | OmniUiCard | executa | fonte de dados do tipo Integration Procedure | Página Lightning | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra; o elemento HTTP Action faz a chamada | FlexCard | Sistema externo | Obrigatório |
| 5 | Data Mapper / DataRaptor Transform | OmniDataTransform | executa | transforma a resposta externa no formato da FlexCard | Integration Procedure | — | Obrigatório |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Integration Procedure | Sistema externo | Obrigatório |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório |

### c.1.v6 — Com Data Mapper · endpoint E3 (URL fixa na HTTP Action + Remote Site)

Fluxo principal: Usuário → FlexCard → Integration Procedure → Data Mapper / DataRaptor Transform → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | lê/referencia | exibe a FlexCard | Usuário | FlexCard | Opcional |
| 3 | FlexCard | OmniUiCard | executa | fonte de dados do tipo Integration Procedure | Página Lightning | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | orquestra; o elemento HTTP Action faz a chamada | FlexCard | Sistema externo | Obrigatório |
| 5 | Data Mapper / DataRaptor Transform | OmniDataTransform | executa | transforma a resposta externa no formato da FlexCard | Integration Procedure | — | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera a URL fixa configurada na HTTP Action | plataforma | — | Obrigatório |
| 7 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório |


## c.2

**OmniScript → Integration Procedure ou Remote Action**

Processo guiado com etapa de integração.

> ⚠️ A validar: Mesmos pontos do c.1; interface da Remote Action depende do runtime (padrão ou pacote).

### c.2.v1 — Via Integration Procedure · endpoint E1

Fluxo principal: Usuário → OmniScript → Integration Procedure → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | HTTP Action faz a chamada | OmniScript | Sistema externo | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Integration Procedure | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório |

### c.2.v2 — Via Integration Procedure · endpoint E2

Fluxo principal: Usuário → OmniScript → Integration Procedure → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | HTTP Action faz a chamada | OmniScript | Sistema externo | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Integration Procedure | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Integration Procedure | — | Obrigatório |

### c.2.v3 — Via Integration Procedure · endpoint E3

Fluxo principal: Usuário → OmniScript → Integration Procedure → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Integration Procedure | Obrigatório |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | HTTP Action faz a chamada | OmniScript | Sistema externo | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera a URL fixa | plataforma | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | responde | Integration Procedure | — | Obrigatório |

### c.2.v4 — Via Remote Action (Apex) · endpoint E1

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Classe Remote Action | Obrigatório |
| 4 | Classe Remote Action | ApexClass | executa | implementa `Callable` (ou a interface do pacote); faz o callout | OmniScript | Sistema externo | Obrigatório |
| 5 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe Remote Action | External Credential | Obrigatório |
| 6 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Remote Action | — | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### c.2.v5 — Via Remote Action (Apex) · endpoint E2

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Classe Remote Action | Obrigatório |
| 4 | Classe Remote Action | ApexClass | executa | implementa `Callable` (ou a interface do pacote); faz o callout | OmniScript | Sistema externo | Obrigatório |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe Remote Action | Sistema externo | Obrigatório |
| 6 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 7 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Remote Action | — | Obrigatório |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### c.2.v6 — Via Remote Action (Apex) · endpoint E3

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Classe Remote Action | Obrigatório |
| 4 | Classe Remote Action | ApexClass | executa | implementa `Callable` (ou a interface do pacote); faz o callout | OmniScript | Sistema externo | Obrigatório |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 6 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe Remote Action | — | Opcional |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Remote Action | — | Obrigatório |
| 8 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### c.2.v7 — Via Remote Action (Apex) · endpoint E4

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Classe Remote Action | Obrigatório |
| 4 | Classe Remote Action | ApexClass | executa | implementa `Callable` (ou a interface do pacote); faz o callout | OmniScript | Sistema externo | Obrigatório |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe Remote Action | registro de Custom Metadata | Obrigatório |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe Remote Action | — | Obrigatório |
| 7 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe Remote Action | endpoint de token do sistema externo | Opcional |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Remote Action | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### c.2.v8 — Via Remote Action (Apex) · endpoint E5

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Classe Remote Action | Obrigatório |
| 4 | Classe Remote Action | ApexClass | executa | implementa `Callable` (ou a interface do pacote); faz o callout | OmniScript | Sistema externo | Obrigatório |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe Remote Action | registro de Custom Metadata | Obrigatório |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe Remote Action | — | Obrigatório |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe Remote Action | External Credential | Obrigatório |
| 8 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Remote Action | — | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### c.2.v9 — Via Remote Action (Apex) · endpoint E6

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | exibe o OmniScript | Usuário | OmniScript | Opcional |
| 3 | OmniScript | OmniScript | executa | guia o usuário; chama a etapa de integração | Página | Classe Remote Action | Obrigatório |
| 4 | Classe Remote Action | ApexClass | executa | implementa `Callable` (ou a interface do pacote); faz o callout | OmniScript | Sistema externo | Obrigatório |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe Remote Action | — | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe Remote Action | — | Obrigatório |
| 8 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |


## d.1

**LWC → fetch direto do navegador**

Sem servidor Salesforce no meio. Só para APIs públicas ou com token do próprio usuário.

> Observação: Não usa Named Credential nem Remote Site Setting: quem autoriza é a CSP (`CspTrustedSite`) e o CORS do sistema externo.

### d.1.v1 — URL no JavaScript

Fluxo principal: Usuário → Componente LWC → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Componente LWC | LightningComponentBundle | executa | chama a API externa com `fetch()` direto do navegador | Página | Sistema externo | Obrigatório |
| 3 | CSP Trusted Site | CspTrustedSite | autoriza | libera o domínio em `connect-src` no navegador | navegador | — | Obrigatório |
| 4 | Sistema externo | não é metadata | ator | responde; precisa liberar CORS para o domínio Lightning | Componente LWC | — | Obrigatório |

### d.1.v2 — URL em Custom Label

Fluxo principal: Usuário → Componente LWC → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Componente LWC | LightningComponentBundle | executa | chama a API externa com `fetch()` direto do navegador | Página | Sistema externo | Obrigatório |
| 3 | Custom Label | CustomLabels | lê/referencia | URL importada via `@salesforce/label` | Componente LWC | — | Obrigatório |
| 4 | CSP Trusted Site | CspTrustedSite | autoriza | libera o domínio em `connect-src` no navegador | navegador | — | Obrigatório |
| 5 | Sistema externo | não é metadata | ator | responde; precisa liberar CORS para o domínio Lightning | Componente LWC | — | Obrigatório |

### d.1.v3 — URL em Custom Metadata via Apex

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Componente LWC | LightningComponentBundle | executa | chama a API externa com `fetch()` direto do navegador | Página | Sistema externo | Obrigatório |
| 3 | Controller Apex | ApexClass | executa | devolve ao LWC a URL lida do CMDT | Componente LWC | Registro de Custom Metadata | Obrigatório |
| 4 | Registro de Custom Metadata | CustomMetadata (+ CustomObject __mdt) | lê/referencia | URL por ambiente | Controller Apex | — | Obrigatório |
| 5 | CSP Trusted Site | CspTrustedSite | autoriza | libera o domínio em `connect-src` no navegador | navegador | — | Obrigatório |
| 6 | Sistema externo | não é metadata | ator | responde; precisa liberar CORS para o domínio Lightning | Componente LWC | — | Obrigatório |


## e.1

**Salesforce Connect (OData / cross-org)**

Virtualização: dado externo lido sob demanda, sem cópia.

### e.1.v1 — Autenticação na própria External Data Source

Fluxo principal: Usuário → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | exibe os registros externos | Usuário | External Object | Obrigatório |
| 3 | External Object | CustomObject (__x) | lê/referencia | representa a tabela externa; cada leitura gera consulta remota | Página | External Data Source | Obrigatório |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce | External Object | — | Obrigatório |
| 5 | External Data Source | ExternalDataSource | lê/referencia | tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade | External Object | Sistema externo | Obrigatório |
| 6 | Permission Set | PermissionSet | autoriza | acesso ao External Object e à External Data Source (identidade por usuário) | plataforma | — | Obrigatório |
| 7 | Sistema externo | não é metadata | ator | serviço OData; responde às consultas | External Data Source | — | Obrigatório |

### e.1.v2 — Autenticação via Named Credential

Fluxo principal: Usuário → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | exibe os registros externos | Usuário | External Object | Obrigatório |
| 3 | External Object | CustomObject (__x) | lê/referencia | representa a tabela externa; cada leitura gera consulta remota | Página | External Data Source | Obrigatório |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce | External Object | — | Obrigatório |
| 5 | External Data Source | ExternalDataSource | lê/referencia | tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade | External Object | Sistema externo | Obrigatório |
| 6 | Permission Set | PermissionSet | autoriza | acesso ao External Object e à External Data Source (identidade por usuário) | plataforma | — | Obrigatório |
| 7 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | External Data Source | External Credential | Obrigatório |
| 8 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | External Data Source | — | Obrigatório |


## e.2

**Salesforce Connect com adaptador Apex**

Virtualização de APIs que não são OData.

### e.2.v1 — Adaptador Apex · endpoint E1

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | exibe os registros externos | Usuário | External Object | Obrigatório |
| 3 | External Object | CustomObject (__x) | lê/referencia | representa a tabela externa; cada leitura gera consulta remota | Página | External Data Source | Obrigatório |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce | External Object | — | Obrigatório |
| 5 | External Data Source | ExternalDataSource | lê/referencia | tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade | External Object | adaptador | Obrigatório |
| 6 | Permission Set | PermissionSet | autoriza | acesso ao External Object e à External Data Source (identidade por usuário) | plataforma | — | Obrigatório |
| 7 | Provider do adaptador | ApexClass | executa | estende `DataSource.Provider`: declara capacidades e autenticação | External Data Source | Connection | Obrigatório |
| 8 | Connection do adaptador | ApexClass | executa | estende `DataSource.Connection`: `sync`, `query`, `search`; faz o callout | Provider | Sistema externo | Obrigatório |
| 9 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Connection do adaptador | External Credential | Obrigatório |
| 10 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 12 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 13 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Connection do adaptador | — | Obrigatório |

### e.2.v2 — Adaptador Apex · endpoint E2

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | exibe os registros externos | Usuário | External Object | Obrigatório |
| 3 | External Object | CustomObject (__x) | lê/referencia | representa a tabela externa; cada leitura gera consulta remota | Página | External Data Source | Obrigatório |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce | External Object | — | Obrigatório |
| 5 | External Data Source | ExternalDataSource | lê/referencia | tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade | External Object | adaptador | Obrigatório |
| 6 | Permission Set | PermissionSet | autoriza | acesso ao External Object e à External Data Source (identidade por usuário) | plataforma | — | Obrigatório |
| 7 | Provider do adaptador | ApexClass | executa | estende `DataSource.Provider`: declara capacidades e autenticação | External Data Source | Connection | Obrigatório |
| 8 | Connection do adaptador | ApexClass | executa | estende `DataSource.Connection`: `sync`, `query`, `search`; faz o callout | Provider | Sistema externo | Obrigatório |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Connection do adaptador | Sistema externo | Obrigatório |
| 10 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 11 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 12 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Connection do adaptador | — | Obrigatório |

### e.2.v3 — Adaptador Apex · endpoint E3

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | exibe os registros externos | Usuário | External Object | Obrigatório |
| 3 | External Object | CustomObject (__x) | lê/referencia | representa a tabela externa; cada leitura gera consulta remota | Página | External Data Source | Obrigatório |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce | External Object | — | Obrigatório |
| 5 | External Data Source | ExternalDataSource | lê/referencia | tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade | External Object | adaptador | Obrigatório |
| 6 | Permission Set | PermissionSet | autoriza | acesso ao External Object e à External Data Source (identidade por usuário) | plataforma | — | Obrigatório |
| 7 | Provider do adaptador | ApexClass | executa | estende `DataSource.Provider`: declara capacidades e autenticação | External Data Source | Connection | Obrigatório |
| 8 | Connection do adaptador | ApexClass | executa | estende `DataSource.Connection`: `sync`, `query`, `search`; faz o callout | Provider | Sistema externo | Obrigatório |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 10 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Connection do adaptador | — | Opcional |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Connection do adaptador | — | Obrigatório |

### e.2.v4 — Adaptador Apex · endpoint E4

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | exibe os registros externos | Usuário | External Object | Obrigatório |
| 3 | External Object | CustomObject (__x) | lê/referencia | representa a tabela externa; cada leitura gera consulta remota | Página | External Data Source | Obrigatório |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce | External Object | — | Obrigatório |
| 5 | External Data Source | ExternalDataSource | lê/referencia | tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade | External Object | adaptador | Obrigatório |
| 6 | Permission Set | PermissionSet | autoriza | acesso ao External Object e à External Data Source (identidade por usuário) | plataforma | — | Obrigatório |
| 7 | Provider do adaptador | ApexClass | executa | estende `DataSource.Provider`: declara capacidades e autenticação | External Data Source | Connection | Obrigatório |
| 8 | Connection do adaptador | ApexClass | executa | estende `DataSource.Connection`: `sync`, `query`, `search`; faz o callout | Provider | Sistema externo | Obrigatório |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Connection do adaptador | registro de Custom Metadata | Obrigatório |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Connection do adaptador | — | Obrigatório |
| 11 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Connection do adaptador | endpoint de token do sistema externo | Opcional |
| 12 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 13 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Connection do adaptador | — | Obrigatório |

### e.2.v5 — Adaptador Apex · endpoint E5

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | exibe os registros externos | Usuário | External Object | Obrigatório |
| 3 | External Object | CustomObject (__x) | lê/referencia | representa a tabela externa; cada leitura gera consulta remota | Página | External Data Source | Obrigatório |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce | External Object | — | Obrigatório |
| 5 | External Data Source | ExternalDataSource | lê/referencia | tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade | External Object | adaptador | Obrigatório |
| 6 | Permission Set | PermissionSet | autoriza | acesso ao External Object e à External Data Source (identidade por usuário) | plataforma | — | Obrigatório |
| 7 | Provider do adaptador | ApexClass | executa | estende `DataSource.Provider`: declara capacidades e autenticação | External Data Source | Connection | Obrigatório |
| 8 | Connection do adaptador | ApexClass | executa | estende `DataSource.Connection`: `sync`, `query`, `search`; faz o callout | Provider | Sistema externo | Obrigatório |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Connection do adaptador | registro de Custom Metadata | Obrigatório |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Connection do adaptador | — | Obrigatório |
| 11 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Connection do adaptador | External Credential | Obrigatório |
| 12 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 14 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Connection do adaptador | — | Obrigatório |

### e.2.v6 — Adaptador Apex · endpoint E6

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | exibe os registros externos | Usuário | External Object | Obrigatório |
| 3 | External Object | CustomObject (__x) | lê/referencia | representa a tabela externa; cada leitura gera consulta remota | Página | External Data Source | Obrigatório |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce | External Object | — | Obrigatório |
| 5 | External Data Source | ExternalDataSource | lê/referencia | tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade | External Object | adaptador | Obrigatório |
| 6 | Permission Set | PermissionSet | autoriza | acesso ao External Object e à External Data Source (identidade por usuário) | plataforma | — | Obrigatório |
| 7 | Provider do adaptador | ApexClass | executa | estende `DataSource.Provider`: declara capacidades e autenticação | External Data Source | Connection | Obrigatório |
| 8 | Connection do adaptador | ApexClass | executa | estende `DataSource.Connection`: `sync`, `query`, `search`; faz o callout | Provider | Sistema externo | Obrigatório |
| 9 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Connection do adaptador | — | Obrigatório |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Connection do adaptador | — | Obrigatório |


## f.1

**Quick Action → Flow ou LWC → callout → atualiza o registro**

Enriquecimento sob demanda, iniciado pelo usuário.

### f.1.v1 — Quick Action → Screen Flow · endpoint E1

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Screen Flow | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Screen Flow | Flow | executa | recebe `recordId`, chama o Apex e grava o retorno | Quick Action | Classe invocável | Obrigatório |
| 5 | Classe invocável | ApexClass | executa | faz o callout | Screen Flow | Sistema externo | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe invocável | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 11 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Classe invocável | triggers/flows do objeto | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v2 — Quick Action → Screen Flow · endpoint E2

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Screen Flow | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Screen Flow | Flow | executa | recebe `recordId`, chama o Apex e grava o retorno | Quick Action | Classe invocável | Obrigatório |
| 5 | Classe invocável | ApexClass | executa | faz o callout | Screen Flow | Sistema externo | Obrigatório |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe invocável | Sistema externo | Obrigatório |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 10 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Classe invocável | triggers/flows do objeto | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v3 — Quick Action → Screen Flow · endpoint E3

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Screen Flow | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Screen Flow | Flow | executa | recebe `recordId`, chama o Apex e grava o retorno | Quick Action | Classe invocável | Obrigatório |
| 5 | Classe invocável | ApexClass | executa | faz o callout | Screen Flow | Sistema externo | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Classe invocável | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 9 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Classe invocável | triggers/flows do objeto | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v4 — Quick Action → Screen Flow · endpoint E4

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Screen Flow | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Screen Flow | Flow | executa | recebe `recordId`, chama o Apex e grava o retorno | Quick Action | Classe invocável | Obrigatório |
| 5 | Classe invocável | ApexClass | executa | faz o callout | Screen Flow | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Classe invocável | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Classe invocável | — | Obrigatório |
| 8 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Classe invocável | endpoint de token do sistema externo | Opcional |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 12 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Classe invocável | triggers/flows do objeto | Obrigatório |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v5 — Quick Action → Screen Flow · endpoint E5

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Screen Flow | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Screen Flow | Flow | executa | recebe `recordId`, chama o Apex e grava o retorno | Quick Action | Classe invocável | Obrigatório |
| 5 | Classe invocável | ApexClass | executa | faz o callout | Screen Flow | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe invocável | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe invocável | — | Obrigatório |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe invocável | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 12 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Classe invocável | triggers/flows do objeto | Obrigatório |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v6 — Quick Action → Screen Flow · endpoint E6

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Screen Flow | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Screen Flow | Flow | executa | recebe `recordId`, chama o Apex e grava o retorno | Quick Action | Classe invocável | Obrigatório |
| 5 | Classe invocável | ApexClass | executa | faz o callout | Screen Flow | Sistema externo | Obrigatório |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Classe invocável | — | Obrigatório |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Classe invocável | — | Obrigatório |
| 9 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Classe invocável | triggers/flows do objeto | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v7 — Quick Action → LWC · endpoint E1

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Componente LWC | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | recebe `recordId` e chama o Apex | Quick Action | Controller Apex | Obrigatório |
| 5 | Controller Apex | ApexClass | executa | faz o callout | Componente LWC | Sistema externo | Obrigatório |
| 6 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Controller Apex | External Credential | Obrigatório |
| 7 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Sistema externo | Obrigatório |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 9 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 10 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 11 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Controller Apex | triggers/flows do objeto | Obrigatório |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v8 — Quick Action → LWC · endpoint E2

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Componente LWC | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | recebe `recordId` e chama o Apex | Quick Action | Controller Apex | Obrigatório |
| 5 | Controller Apex | ApexClass | executa | faz o callout | Componente LWC | Sistema externo | Obrigatório |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Controller Apex | Sistema externo | Obrigatório |
| 7 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 8 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 9 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 10 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Controller Apex | triggers/flows do objeto | Obrigatório |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v9 — Quick Action → LWC · endpoint E3

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Componente LWC | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | recebe `recordId` e chama o Apex | Quick Action | Controller Apex | Obrigatório |
| 5 | Controller Apex | ApexClass | executa | faz o callout | Componente LWC | Sistema externo | Obrigatório |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio fixo no código para callout | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Certificate | Certificate | autoriza | mutual TLS (`setClientCertificateName`) | Controller Apex | — | Opcional |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 9 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Controller Apex | triggers/flows do objeto | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v10 — Quick Action → LWC · endpoint E4

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Componente LWC | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | recebe `recordId` e chama o Apex | Quick Action | Controller Apex | Obrigatório |
| 5 | Controller Apex | ApexClass | executa | faz o callout | Componente LWC | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define os campos de configuração (endpoint, path, client_id, timeout, ativo) | Controller Apex | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README | Controller Apex | — | Obrigatório |
| 8 | Classe de token | ApexClass | executa | faz o callout de autenticação (ex.: client_credentials) e devolve o token | Controller Apex | endpoint de token do sistema externo | Opcional |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | guarda o token até expirar, evitando um callout de token por chamada | Classe de token | — | Opcional |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido do Custom Metadata (um por ambiente) | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 12 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Controller Apex | triggers/flows do objeto | Obrigatório |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v11 — Quick Action → LWC · endpoint E5

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Componente LWC | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | recebe `recordId` e chama o Apex | Quick Action | Controller Apex | Obrigatório |
| 5 | Controller Apex | ApexClass | executa | faz o callout | Componente LWC | Sistema externo | Obrigatório |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Controller Apex | registro de Custom Metadata | Obrigatório |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Controller Apex | — | Obrigatório |
| 8 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Controller Apex | External Credential | Obrigatório |
| 9 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Sistema externo | Obrigatório |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 11 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 12 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Controller Apex | triggers/flows do objeto | Obrigatório |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

### f.1.v12 — Quick Action → LWC · endpoint E6

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Quick Action | QuickAction | executa | botão na página do registro; tipo Flow ou LWC | Usuário | Componente LWC | Obrigatório |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | expõe a ação | plataforma | — | Obrigatório |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | recebe `recordId` e chama o Apex | Quick Action | Controller Apex | Obrigatório |
| 5 | Controller Apex | ApexClass | executa | faz o callout | Componente LWC | Sistema externo | Obrigatório |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | fornece o endpoint por ambiente | Controller Apex | — | Obrigatório |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | libera o domínio lido | plataforma (no momento do callout) | — | Obrigatório |
| 8 | Sistema externo | não é metadata | ator | recebe a requisição e devolve a resposta | Controller Apex | — | Obrigatório |
| 9 | Objeto do registro | CustomObject + CustomField | executa (DML) | recebe os dados de enriquecimento | Controller Apex | triggers/flows do objeto | Obrigatório |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | libera ao usuário as classes Apex chamadas pela UI | plataforma | — | Obrigatório |

