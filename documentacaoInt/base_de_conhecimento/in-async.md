# IN ASYNC — externo envia; Salesforce processa depois

> Gerado a partir das definições da base de integração. Convenções, legenda e códigos de variante: [README](README.md).

## Índice

- [H.1 — Sistema externo → Bulk API 2.0](#h1) (12 variantes)
- [H.2 — Sistema externo publica Platform Event → assinante na org](#h2) (16 variantes)
- [H.3 — Apex REST que recebe e enfileira](#h3) (8 variantes)
- [H.4 — E-mail inbound (Email Service)](#h4) (2 variantes)
- [H.5 — Arquivos via ContentVersion](#h5) (8 variantes)

## H.1

**Sistema externo → Bulk API 2.0**

Cargas de grande volume em jobs assíncronos.

### H.1.v1 — Connected App · OAuth 2.0 JWT Bearer · insert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v2 — Connected App · OAuth 2.0 JWT Bearer · upsert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 9 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 10 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 11 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v3 — Connected App · OAuth 2.0 Client Credentials · insert

Fluxo principal: Sistema externo → Usuário run-as → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 10 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 11 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v4 — Connected App · OAuth 2.0 Client Credentials · upsert

Fluxo principal: Sistema externo → Usuário run-as → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v5 — Connected App · OAuth 2.0 Web Server + Refresh Token · insert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Web Server + Refresh Token e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 10 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 11 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v6 — Connected App · OAuth 2.0 Web Server + Refresh Token · upsert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Web Server + Refresh Token e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 8 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 9 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 10 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) |
| 11 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 12 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v7 — External Client App · OAuth 2.0 JWT Bearer · insert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v8 — External Client App · OAuth 2.0 JWT Bearer · upsert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v9 — External Client App · OAuth 2.0 Client Credentials · insert

Fluxo principal: Sistema externo → Usuário run-as → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v10 — External Client App · OAuth 2.0 Client Credentials · upsert

Fluxo principal: Sistema externo → Usuário run-as → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v11 — External Client App · OAuth 2.0 Web Server + Refresh Token · insert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Web Server + Refresh Token, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.1.v12 — External Client App · OAuth 2.0 Web Server + Refresh Token · upsert

Fluxo principal: Sistema externo → Usuário de integração → Bulk API 2.0 → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Bulk API 2.0 | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Web Server + Refresh Token, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | Bulk API 2.0 | não é metadata | ator | recebe o CSV e processa o job em lotes assíncronos | Sistema externo | Objeto de destino | Obrigatório |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Bulk API 2.0 | triggers e flows do objeto | Obrigatório |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Bulk API 2.0 | — | Obrigatório |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Bulk API 2.0 | — | Opcional (obrigatório em upsert) |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |


## H.2

**Sistema externo publica Platform Event → assinante na org**

O externo entrega a mensagem; a org processa quando o evento chega.

### H.2.v1 — Connected App · OAuth 2.0 JWT Bearer · publica via REST · assinante APEX

Fluxo principal: Sistema externo → Usuário de integração → REST API (sObject __e) → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | REST API (sObject __e) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 10 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 11 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 12 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; processa e grava | barramento | Objeto de destino | Obrigatório |
| 13 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v2 — Connected App · OAuth 2.0 JWT Bearer · publica via REST · assinante FLOW

Fluxo principal: Sistema externo → Usuário de integração → REST API (sObject __e) → Flow disparado por evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | REST API (sObject __e) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 10 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 11 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 12 | Flow disparado por evento | Flow | executa | processa e grava | barramento | Objeto de destino | Obrigatório |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow disparado por evento | triggers e flows do objeto | Obrigatório |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow disparado por evento | — | Obrigatório |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow disparado por evento | — | Opcional (obrigatório em upsert) |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v3 — Connected App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante APEX

Fluxo principal: Sistema externo → Usuário de integração → Pub/Sub API (Publish) → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | Pub/Sub API (Publish) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 10 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 11 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 12 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; processa e grava | barramento | Objeto de destino | Obrigatório |
| 13 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v4 — Connected App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante FLOW

Fluxo principal: Sistema externo → Usuário de integração → Pub/Sub API (Publish) → Flow disparado por evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | Pub/Sub API (Publish) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 10 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 11 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 12 | Flow disparado por evento | Flow | executa | processa e grava | barramento | Objeto de destino | Obrigatório |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow disparado por evento | triggers e flows do objeto | Obrigatório |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow disparado por evento | — | Obrigatório |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow disparado por evento | — | Opcional (obrigatório em upsert) |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v5 — Connected App · OAuth 2.0 Client Credentials · publica via REST · assinante APEX

Fluxo principal: Sistema externo → Usuário run-as → REST API (sObject __e) → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | REST API (sObject __e) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 8 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 9 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 10 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 11 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; processa e grava | barramento | Objeto de destino | Obrigatório |
| 12 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v6 — Connected App · OAuth 2.0 Client Credentials · publica via REST · assinante FLOW

Fluxo principal: Sistema externo → Usuário run-as → REST API (sObject __e) → Flow disparado por evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | REST API (sObject __e) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 8 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 9 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 10 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 11 | Flow disparado por evento | Flow | executa | processa e grava | barramento | Objeto de destino | Obrigatório |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow disparado por evento | triggers e flows do objeto | Obrigatório |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow disparado por evento | — | Obrigatório |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow disparado por evento | — | Opcional (obrigatório em upsert) |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v7 — Connected App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante APEX

Fluxo principal: Sistema externo → Usuário run-as → Pub/Sub API (Publish) → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | Pub/Sub API (Publish) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 8 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 9 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 10 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 11 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; processa e grava | barramento | Objeto de destino | Obrigatório |
| 12 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v8 — Connected App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante FLOW

Fluxo principal: Sistema externo → Usuário run-as → Pub/Sub API (Publish) → Flow disparado por evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | Pub/Sub API (Publish) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 8 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 9 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 10 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 11 | Flow disparado por evento | Flow | executa | processa e grava | barramento | Objeto de destino | Obrigatório |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow disparado por evento | triggers e flows do objeto | Obrigatório |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow disparado por evento | — | Obrigatório |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow disparado por evento | — | Opcional (obrigatório em upsert) |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v9 — External Client App · OAuth 2.0 JWT Bearer · publica via REST · assinante APEX

Fluxo principal: Sistema externo → Usuário de integração → REST API (sObject __e) → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | REST API (sObject __e) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 14 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 15 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 16 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; processa e grava | barramento | Objeto de destino | Obrigatório |
| 17 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 18 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 19 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 20 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 21 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 22 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v10 — External Client App · OAuth 2.0 JWT Bearer · publica via REST · assinante FLOW

Fluxo principal: Sistema externo → Usuário de integração → REST API (sObject __e) → Flow disparado por evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | REST API (sObject __e) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 14 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 15 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 16 | Flow disparado por evento | Flow | executa | processa e grava | barramento | Objeto de destino | Obrigatório |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow disparado por evento | triggers e flows do objeto | Obrigatório |
| 18 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow disparado por evento | — | Obrigatório |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow disparado por evento | — | Opcional (obrigatório em upsert) |
| 20 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 21 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v11 — External Client App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante APEX

Fluxo principal: Sistema externo → Usuário de integração → Pub/Sub API (Publish) → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Pub/Sub API (Publish) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 14 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 15 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 16 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; processa e grava | barramento | Objeto de destino | Obrigatório |
| 17 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 18 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 19 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 20 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 21 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 22 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v12 — External Client App · OAuth 2.0 JWT Bearer · publica via PUBSUB · assinante FLOW

Fluxo principal: Sistema externo → Usuário de integração → Pub/Sub API (Publish) → Flow disparado por evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Pub/Sub API (Publish) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 14 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 15 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 16 | Flow disparado por evento | Flow | executa | processa e grava | barramento | Objeto de destino | Obrigatório |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow disparado por evento | triggers e flows do objeto | Obrigatório |
| 18 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow disparado por evento | — | Obrigatório |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow disparado por evento | — | Opcional (obrigatório em upsert) |
| 20 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 21 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v13 — External Client App · OAuth 2.0 Client Credentials · publica via REST · assinante APEX

Fluxo principal: Sistema externo → Usuário run-as → REST API (sObject __e) → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | REST API (sObject __e) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 12 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 13 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 14 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 15 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; processa e grava | barramento | Objeto de destino | Obrigatório |
| 16 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 18 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 20 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 21 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v14 — External Client App · OAuth 2.0 Client Credentials · publica via REST · assinante FLOW

Fluxo principal: Sistema externo → Usuário run-as → REST API (sObject __e) → Flow disparado por evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | REST API (sObject __e) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 12 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 13 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 14 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 15 | Flow disparado por evento | Flow | executa | processa e grava | barramento | Objeto de destino | Obrigatório |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow disparado por evento | triggers e flows do objeto | Obrigatório |
| 17 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow disparado por evento | — | Obrigatório |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow disparado por evento | — | Opcional (obrigatório em upsert) |
| 19 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 20 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v15 — External Client App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante APEX

Fluxo principal: Sistema externo → Usuário run-as → Pub/Sub API (Publish) → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | Pub/Sub API (Publish) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 12 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 13 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 14 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 15 | Trigger do evento | ApexTrigger | executa | `after insert` no `__e`; processa e grava | barramento | Objeto de destino | Obrigatório |
| 16 | Configuração do assinante | PlatformEventSubscriberConfig | lê/referencia | usuário e lote | plataforma | — | Opcional |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 18 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 20 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 21 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.2.v16 — External Client App · OAuth 2.0 Client Credentials · publica via PUBSUB · assinante FLOW

Fluxo principal: Sistema externo → Usuário run-as → Pub/Sub API (Publish) → Flow disparado por evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | publica o evento | — | API | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | Pub/Sub API (Publish) | não é metadata | ator | recebe a publicação | Sistema externo | Platform Event | Obrigatório |
| 12 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | API | assinantes | Obrigatório |
| 13 | Campos do evento | CustomField | lê/referencia | payload | API | — | Obrigatório |
| 14 | Permission Set (Create no evento) | PermissionSet | autoriza | permite publicar o `__e` | plataforma | — | Obrigatório |
| 15 | Flow disparado por evento | Flow | executa | processa e grava | barramento | Objeto de destino | Obrigatório |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Flow disparado por evento | triggers e flows do objeto | Obrigatório |
| 17 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Flow disparado por evento | — | Obrigatório |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Flow disparado por evento | — | Opcional (obrigatório em upsert) |
| 19 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 20 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |


## H.3

**Apex REST que recebe e enfileira**

Entrada síncrona, processamento assíncrono.

### H.3.v1 — Connected App · OAuth 2.0 JWT Bearer · delega para Queueable

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Classe Queueable → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint | Sistema externo | Classe Apex REST | Obrigatório |
| 9 | Classe Apex REST | ApexClass | executa | valida o payload, responde 202 e delega | Apex REST | Queueable | Obrigatório |
| 10 | Classe Queueable | ApexClass | executa | processa depois da resposta | Classe Apex REST | Objeto de destino | Obrigatório |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Queueable | triggers e flows do objeto | Obrigatório |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Queueable | — | Obrigatório |
| 13 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Queueable | — | Opcional (obrigatório em upsert) |
| 14 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 15 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### H.3.v2 — Connected App · OAuth 2.0 JWT Bearer · delega para Platform Event

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint | Sistema externo | Classe Apex REST | Obrigatório |
| 9 | Classe Apex REST | ApexClass | executa | valida o payload, responde 202 e delega | Apex REST | Platform Event | Obrigatório |
| 10 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | Classe Apex REST | assinantes | Obrigatório |
| 11 | Campos do evento | CustomField | lê/referencia | payload | Classe Apex REST | — | Obrigatório |
| 12 | Trigger do evento | ApexTrigger | executa | processa | barramento | Objeto de destino | Obrigatório |
| 13 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 14 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 15 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |
| 18 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Trigger do evento | — | Opcional |

### H.3.v3 — Connected App · OAuth 2.0 Client Credentials · delega para Queueable

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Classe Queueable → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint | Sistema externo | Classe Apex REST | Obrigatório |
| 8 | Classe Apex REST | ApexClass | executa | valida o payload, responde 202 e delega | Apex REST | Queueable | Obrigatório |
| 9 | Classe Queueable | ApexClass | executa | processa depois da resposta | Classe Apex REST | Objeto de destino | Obrigatório |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Queueable | triggers e flows do objeto | Obrigatório |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Queueable | — | Obrigatório |
| 12 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Queueable | — | Opcional (obrigatório em upsert) |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### H.3.v4 — Connected App · OAuth 2.0 Client Credentials · delega para Platform Event

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint | Sistema externo | Classe Apex REST | Obrigatório |
| 8 | Classe Apex REST | ApexClass | executa | valida o payload, responde 202 e delega | Apex REST | Platform Event | Obrigatório |
| 9 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | Classe Apex REST | assinantes | Obrigatório |
| 10 | Campos do evento | CustomField | lê/referencia | payload | Classe Apex REST | — | Obrigatório |
| 11 | Trigger do evento | ApexTrigger | executa | processa | barramento | Objeto de destino | Obrigatório |
| 12 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 13 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 14 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 15 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 16 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Trigger do evento | — | Opcional |

### H.3.v5 — External Client App · OAuth 2.0 JWT Bearer · delega para Queueable

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Classe Queueable → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint | Sistema externo | Classe Apex REST | Obrigatório |
| 13 | Classe Apex REST | ApexClass | executa | valida o payload, responde 202 e delega | Apex REST | Queueable | Obrigatório |
| 14 | Classe Queueable | ApexClass | executa | processa depois da resposta | Classe Apex REST | Objeto de destino | Obrigatório |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Queueable | triggers e flows do objeto | Obrigatório |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Queueable | — | Obrigatório |
| 17 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Queueable | — | Opcional (obrigatório em upsert) |
| 18 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 19 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |
| 20 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### H.3.v6 — External Client App · OAuth 2.0 JWT Bearer · delega para Platform Event

Fluxo principal: Sistema externo → Usuário de integração → Apex REST (/services/apexrest) → Classe Apex REST → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint | Sistema externo | Classe Apex REST | Obrigatório |
| 13 | Classe Apex REST | ApexClass | executa | valida o payload, responde 202 e delega | Apex REST | Platform Event | Obrigatório |
| 14 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | Classe Apex REST | assinantes | Obrigatório |
| 15 | Campos do evento | CustomField | lê/referencia | payload | Classe Apex REST | — | Obrigatório |
| 16 | Trigger do evento | ApexTrigger | executa | processa | barramento | Objeto de destino | Obrigatório |
| 17 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 18 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 19 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 20 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 21 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |
| 22 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Trigger do evento | — | Opcional |

### H.3.v7 — External Client App · OAuth 2.0 Client Credentials · delega para Queueable

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Classe Queueable → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint | Sistema externo | Classe Apex REST | Obrigatório |
| 12 | Classe Apex REST | ApexClass | executa | valida o payload, responde 202 e delega | Apex REST | Queueable | Obrigatório |
| 13 | Classe Queueable | ApexClass | executa | processa depois da resposta | Classe Apex REST | Objeto de destino | Obrigatório |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe Queueable | triggers e flows do objeto | Obrigatório |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe Queueable | — | Obrigatório |
| 16 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Classe Queueable | — | Opcional (obrigatório em upsert) |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |
| 19 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Classe Queueable | — | Opcional |

### H.3.v8 — External Client App · OAuth 2.0 Client Credentials · delega para Platform Event

Fluxo principal: Sistema externo → Usuário run-as → Apex REST (/services/apexrest) → Classe Apex REST → Trigger do evento → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a Apex REST | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | Apex REST (/services/apexrest) | não é metadata | ator | endpoint | Sistema externo | Classe Apex REST | Obrigatório |
| 12 | Classe Apex REST | ApexClass | executa | valida o payload, responde 202 e delega | Apex REST | Platform Event | Obrigatório |
| 13 | Platform Event | CustomObject (__e) | lê/referencia | contrato da mensagem | Classe Apex REST | assinantes | Obrigatório |
| 14 | Campos do evento | CustomField | lê/referencia | payload | Classe Apex REST | — | Obrigatório |
| 15 | Trigger do evento | ApexTrigger | executa | processa | barramento | Objeto de destino | Obrigatório |
| 16 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Trigger do evento | triggers e flows do objeto | Obrigatório |
| 17 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Trigger do evento | — | Obrigatório |
| 18 | Campo External ID | CustomField (externalId=true) | lê/referencia | chave de correlação para upsert entre sistemas | Trigger do evento | — | Opcional (obrigatório em upsert) |
| 19 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 20 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |
| 21 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | registra requisição, resposta, status e erro | Trigger do evento | — | Opcional |


## H.4

**E-mail inbound (Email Service)**

Integração por e-mail.

### H.4.v1 — Processa direto

Fluxo principal: Sistema externo → Email Service → Classe handler → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | envia e-mail ao endereço do serviço | — | Email Service | Obrigatório |
| 2 | Email Service | EmailServicesFunction | executa | endereço, remetentes aceitos, usuário de contexto, ação em falha | Sistema externo | Classe handler | Obrigatório |
| 3 | Classe handler | ApexClass | executa | implementa `Messaging.InboundEmailHandler`; lê corpo e anexos | Email Service | Objeto de destino | Obrigatório |
| 4 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe handler | triggers e flows do objeto | Obrigatório |
| 5 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe handler | — | Obrigatório |
| 6 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 7 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.4.v2 — Enfileira processamento

Fluxo principal: Sistema externo → Email Service → Classe handler → Classe Queueable → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | envia e-mail ao endereço do serviço | — | Email Service | Obrigatório |
| 2 | Email Service | EmailServicesFunction | executa | endereço, remetentes aceitos, usuário de contexto, ação em falha | Sistema externo | Classe handler | Obrigatório |
| 3 | Classe handler | ApexClass | executa | implementa `Messaging.InboundEmailHandler`; lê corpo e anexos | Email Service | Queueable | Obrigatório |
| 4 | Classe Queueable | ApexClass | executa | processamento pesado posterior | Classe handler | Objeto de destino | Obrigatório |
| 5 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | Classe handler | triggers e flows do objeto | Obrigatório |
| 6 | Campos | CustomField | lê/referencia | campos gravados ou lidos | Classe handler | — | Obrigatório |
| 7 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 8 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |


## H.5

**Arquivos via ContentVersion**

O externo envia arquivo; automação processa.

### H.5.v1 — Connected App · OAuth 2.0 JWT Bearer · processador APEX

Fluxo principal: Sistema externo → Usuário de integração → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Trigger em ContentVersion → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (ContentVersion) | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | REST API (ContentVersion) | não é metadata | ator | recebe o arquivo (multipart/base64) | Sistema externo | ContentVersion | Obrigatório |
| 9 | ContentVersion / ContentDocumentLink | não é metadata | ator | objetos padrão de arquivo (registros, não metadata) | REST API | processador | Obrigatório |
| 10 | Trigger em ContentVersion | ApexTrigger | executa | lê/valida o conteúdo e vincula ao registro | plataforma (DML) | Objeto de destino | Obrigatório |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | processador | triggers e flows do objeto | Obrigatório |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | processador | — | Obrigatório |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.5.v2 — Connected App · OAuth 2.0 JWT Bearer · processador FLOW

Fluxo principal: Sistema externo → Usuário de integração → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Flow record-triggered em ContentVersion → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (ContentVersion) | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 JWT Bearer e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 4 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 5 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 6 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 7 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 8 | REST API (ContentVersion) | não é metadata | ator | recebe o arquivo (multipart/base64) | Sistema externo | ContentVersion | Obrigatório |
| 9 | ContentVersion / ContentDocumentLink | não é metadata | ator | objetos padrão de arquivo (registros, não metadata) | REST API | processador | Obrigatório |
| 10 | Flow record-triggered em ContentVersion | Flow | executa | lê/valida o conteúdo e vincula ao registro | plataforma (DML) | Objeto de destino | Obrigatório |
| 11 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | processador | triggers e flows do objeto | Obrigatório |
| 12 | Campos | CustomField | lê/referencia | campos gravados ou lidos | processador | — | Obrigatório |
| 13 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 14 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.5.v3 — Connected App · OAuth 2.0 Client Credentials · processador APEX

Fluxo principal: Sistema externo → Usuário run-as → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Trigger em ContentVersion → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (ContentVersion) | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | REST API (ContentVersion) | não é metadata | ator | recebe o arquivo (multipart/base64) | Sistema externo | ContentVersion | Obrigatório |
| 8 | ContentVersion / ContentDocumentLink | não é metadata | ator | objetos padrão de arquivo (registros, não metadata) | REST API | processador | Obrigatório |
| 9 | Trigger em ContentVersion | ApexTrigger | executa | lê/valida o conteúdo e vincula ao registro | plataforma (DML) | Objeto de destino | Obrigatório |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | processador | triggers e flows do objeto | Obrigatório |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | processador | — | Obrigatório |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.5.v4 — Connected App · OAuth 2.0 Client Credentials · processador FLOW

Fluxo principal: Sistema externo → Usuário run-as → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Flow record-triggered em ContentVersion → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (ContentVersion) | — | Connected App / External Client App | Obrigatório |
| 2 | Connected App | ConnectedApp | autoriza | registra o cliente externo e libera o fluxo OAuth 2.0 Client Credentials e os escopos | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 4 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 5 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 6 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 7 | REST API (ContentVersion) | não é metadata | ator | recebe o arquivo (multipart/base64) | Sistema externo | ContentVersion | Obrigatório |
| 8 | ContentVersion / ContentDocumentLink | não é metadata | ator | objetos padrão de arquivo (registros, não metadata) | REST API | processador | Obrigatório |
| 9 | Flow record-triggered em ContentVersion | Flow | executa | lê/valida o conteúdo e vincula ao registro | plataforma (DML) | Objeto de destino | Obrigatório |
| 10 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | processador | triggers e flows do objeto | Obrigatório |
| 11 | Campos | CustomField | lê/referencia | campos gravados ou lidos | processador | — | Obrigatório |
| 12 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 13 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.5.v5 — External Client App · OAuth 2.0 JWT Bearer · processador APEX

Fluxo principal: Sistema externo → Usuário de integração → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Trigger em ContentVersion → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (ContentVersion) | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | REST API (ContentVersion) | não é metadata | ator | recebe o arquivo (multipart/base64) | Sistema externo | ContentVersion | Obrigatório |
| 13 | ContentVersion / ContentDocumentLink | não é metadata | ator | objetos padrão de arquivo (registros, não metadata) | REST API | processador | Obrigatório |
| 14 | Trigger em ContentVersion | ApexTrigger | executa | lê/valida o conteúdo e vincula ao registro | plataforma (DML) | Objeto de destino | Obrigatório |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | processador | triggers e flows do objeto | Obrigatório |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | processador | — | Obrigatório |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.5.v6 — External Client App · OAuth 2.0 JWT Bearer · processador FLOW

Fluxo principal: Sistema externo → Usuário de integração → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Flow record-triggered em ContentVersion → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (ContentVersion) | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 JWT Bearer, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Certificate (público, do cliente) | Certificate | autoriza | o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate) | app | — | Obrigatório (no app) |
| 8 | Usuário de integração | não é metadata | ator | usuário autenticado pelo fluxo | app | — | Obrigatório |
| 9 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 10 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 11 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 12 | REST API (ContentVersion) | não é metadata | ator | recebe o arquivo (multipart/base64) | Sistema externo | ContentVersion | Obrigatório |
| 13 | ContentVersion / ContentDocumentLink | não é metadata | ator | objetos padrão de arquivo (registros, não metadata) | REST API | processador | Obrigatório |
| 14 | Flow record-triggered em ContentVersion | Flow | executa | lê/valida o conteúdo e vincula ao registro | plataforma (DML) | Objeto de destino | Obrigatório |
| 15 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | processador | triggers e flows do objeto | Obrigatório |
| 16 | Campos | CustomField | lê/referencia | campos gravados ou lidos | processador | — | Obrigatório |
| 17 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 18 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.5.v7 — External Client App · OAuth 2.0 Client Credentials · processador APEX

Fluxo principal: Sistema externo → Usuário run-as → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Trigger em ContentVersion → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (ContentVersion) | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | REST API (ContentVersion) | não é metadata | ator | recebe o arquivo (multipart/base64) | Sistema externo | ContentVersion | Obrigatório |
| 12 | ContentVersion / ContentDocumentLink | não é metadata | ator | objetos padrão de arquivo (registros, não metadata) | REST API | processador | Obrigatório |
| 13 | Trigger em ContentVersion | ApexTrigger | executa | lê/valida o conteúdo e vincula ao registro | plataforma (DML) | Objeto de destino | Obrigatório |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | processador | triggers e flows do objeto | Obrigatório |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | processador | — | Obrigatório |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

### H.5.v8 — External Client App · OAuth 2.0 Client Credentials · processador FLOW

Fluxo principal: Sistema externo → Usuário run-as → REST API (ContentVersion) → ContentVersion / ContentDocumentLink → Flow record-triggered em ContentVersion → Objeto de destino

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Sistema externo | não é metadata | ator | obtém o token e chama a REST API (ContentVersion) | — | Connected App / External Client App | Obrigatório |
| 2 | External Client App | ExternalClientApplication | autoriza | registra o cliente externo | Sistema externo | Salesforce (emissão do token) | Obrigatório |
| 3 | Configurações OAuth do app | ExtlClntAppOauthSettings | autoriza | habilita o fluxo OAuth 2.0 Client Credentials, callback e escopos | External Client App | — | Obrigatório |
| 4 | Configurações OAuth globais | ExtlClntAppGlobalOauthSettings | autoriza | consumer key/secret e certificado. Não versionar segredos | External Client App | — | Obrigatório |
| 5 | Políticas OAuth configuráveis | ExtlClntAppOauthConfigurablePolicies | autoriza | quem pode usar o app, política de refresh token, IP relaxation, usuário run-as (Client Credentials) | External Client App | — | Obrigatório |
| 6 | Políticas gerais | ExtlClntAppConfigurablePolicies | autoriza | habilita o app e seus plugins na org | External Client App | — | Obrigatório |
| 7 | Usuário run-as | não é metadata | ator | usuário em nome do qual o token Client Credentials executa | app | — | Obrigatório |
| 8 | Perfil do usuário de integração | Profile | autoriza | base do usuário (ex.: Minimum Access, API Enabled) | plataforma | — | Obrigatório |
| 9 | Permission Set / Permission Set Group | PermissionSet / PermissionSetGroup | autoriza | acesso a objetos, campos, classes Apex e ao app | plataforma | — | Obrigatório |
| 10 | Escopo OAuth customizado | OauthCustomScope | autoriza | restringe o que o token pode fazer | app | — | Opcional |
| 11 | REST API (ContentVersion) | não é metadata | ator | recebe o arquivo (multipart/base64) | Sistema externo | ContentVersion | Obrigatório |
| 12 | ContentVersion / ContentDocumentLink | não é metadata | ator | objetos padrão de arquivo (registros, não metadata) | REST API | processador | Obrigatório |
| 13 | Flow record-triggered em ContentVersion | Flow | executa | lê/valida o conteúdo e vincula ao registro | plataforma (DML) | Objeto de destino | Obrigatório |
| 14 | Objeto de destino | CustomObject (padrão ou __c) | executa (DML) | recebe a criação/alteração/consulta | processador | triggers e flows do objeto | Obrigatório |
| 15 | Campos | CustomField | lê/referencia | campos gravados ou lidos | processador | — | Obrigatório |
| 16 | Trigger do objeto | ApexTrigger | executa | efeitos colaterais da gravação | plataforma (DML) | classes handler | Opcional |
| 17 | Flow record-triggered | Flow | executa | efeitos colaterais declarativos | plataforma (DML) | — | Opcional |

