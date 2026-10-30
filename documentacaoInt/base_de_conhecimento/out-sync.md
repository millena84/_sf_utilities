# OUT SYNC — Salesforce chama o externo e espera

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
| `AuthProvider` | Cadastro de um provedor de login externo (OAuth/OpenID), usado para obter tokens ou para login único. |
| `Certificate` | Certificado digital usado para assinar ou proteger conexões. |
| `CspTrustedSite` | Lista de domínios que o **navegador** pode acessar a partir das páginas do Salesforce (regra CSP). |
| `CustomField` | Campo de um objeto. Um campo External ID serve de chave para casar registros entre sistemas. |
| `CustomLabels` | Textos configuráveis; às vezes guardam URLs ou parâmetros. |
| `CustomMetadata` | Registro de configuração (uma "linha" de um tipo `__mdt`). Vai junto com o código no deploy. |
| `CustomObject` | Objeto (tabela). Sufixos: `__c` customizado, `__x` externo, `__e` evento, `__mdt` tipo de configuração. |
| `CustomPermission` | Permissão criada pela empresa; pode servir de chave liga/desliga. |
| `CustomTab` | Aba do menu. Pode abrir um objeto, uma página, um componente ou um site externo. |
| `ExternalCredential` | Cadastro de como autenticar em um sistema externo (OAuth, JWT, senha, cabeçalho). Usado pela Named Credential. |
| `ExternalDataSource` | Cadastro de uma fonte de dados externa usada pelo Salesforce Connect (dados vistos sem copiar). |
| `ExternalServiceRegistration` | Cadastro de uma API externa a partir do contrato dela (OpenAPI). Vira ações para Flow e classes para Apex. |
| `FlexiPage` | Página do Lightning montada no App Builder, onde os componentes são posicionados. |
| `Flow` | Automação montada sem código no Flow Builder (com telas, disparada por registro, por agenda ou por evento). |
| `FlowDefinition` | Arquivo antigo que indica qual versão do Flow está ativa. |
| `Layout` | Layout de página: define campos e botões que aparecem no registro. |
| `LightningComponentBundle` | Componente de tela moderno (LWC), feito em JavaScript e HTML. |
| `NamedCredential` | Cadastro do endereço de um sistema externo (e, no modelo novo, a ligação com a autenticação). Quem usa Named Credential não precisa de Remote Site Setting para aquele domínio. |
| `OmniDataTransform` | Data Mapper (DataRaptor) do OmniStudio: lê, grava ou transforma dados. |
| `OmniIntegrationProcedure` | Integration Procedure do OmniStudio: roteiro de integração montado sem código. |
| `OmniScript` | OmniScript do OmniStudio: processo guiado de várias telas. |
| `OmniUiCard` | FlexCard do OmniStudio: cartão de tela que mostra dados. |
| `PermissionSet` | Conjunto de permissões extras que se dá a um usuário. |
| `PlatformCachePartition` | Memória temporária da plataforma, para guardar dados como tokens. |
| `QuickAction` | Botão de ação na página do registro, que abre um Flow, um componente ou um formulário. |
| `RemoteSiteSetting` | Lista de domínios externos que o código Apex pode chamar quando a URL **não** vem de uma Named Credential. |

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

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [b.1.v1](#b1v1) | Origem LWC · endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.1.v2](#b1v2) | Origem LWC · endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida)) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.1.v3](#b1v3) | Origem LWC · endpoint E3 (URL fixa no código Apex + Remote Site Setting) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.1.v4](#b1v4) | Origem LWC · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.1.v5](#b1v5) | Origem LWC · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.1.v6](#b1v6) | Origem LWC · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.1.v7](#b1v7) | Origem Screen Flow · endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.1.v8](#b1v8) | Origem Screen Flow · endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida)) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.1.v9](#b1v9) | Origem Screen Flow · endpoint E3 (URL fixa no código Apex + Remote Site Setting) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.1.v10](#b1v10) | Origem Screen Flow · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.1.v11](#b1v11) | Origem Screen Flow · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.1.v12](#b1v12) | Origem Screen Flow · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="b1v1"></a>

### b.1.v1 — Origem LWC · endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Controller Apex | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 6 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe cliente HTTP | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v2"></a>

### b.1.v2 — Origem LWC · endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida))

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Controller Apex | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 6 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 8 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe cliente HTTP | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 10 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v3"></a>

### b.1.v3 — Origem LWC · endpoint E3 (URL fixa no código Apex + Remote Site Setting)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Controller Apex | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 6 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe cliente HTTP | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v4"></a>

### b.1.v4 — Origem LWC · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Controller Apex | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 6 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe cliente HTTP | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe cliente HTTP | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe cliente HTTP | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 11 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 12 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v5"></a>

### b.1.v5 — Origem LWC · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Controller Apex | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 6 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 8 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe cliente HTTP | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe cliente HTTP | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe cliente HTTP | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 11 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 12 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v6"></a>

### b.1.v6 — Origem LWC · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Controller Apex | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 6 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 7 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 8 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe cliente HTTP | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v7"></a>

### b.1.v7 — Origem Screen Flow · endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Classe invocável | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 7 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 9 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe cliente HTTP | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 14 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 15 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 16 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v8"></a>

### b.1.v8 — Origem Screen Flow · endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida))

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Classe invocável | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 7 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe cliente HTTP | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 11 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 15 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v9"></a>

### b.1.v9 — Origem Screen Flow · endpoint E3 (URL fixa no código Apex + Remote Site Setting)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Classe invocável | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 7 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe cliente HTTP | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v10"></a>

### b.1.v10 — Origem Screen Flow · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Classe invocável | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 7 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe cliente HTTP | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe cliente HTTP | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe cliente HTTP | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 12 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 13 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v11"></a>

### b.1.v11 — Origem Screen Flow · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Classe invocável | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 7 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe cliente HTTP | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe cliente HTTP | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe cliente HTTP | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 15 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 16 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 17 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b1v12"></a>

### b.1.v12 — Origem Screen Flow · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Classe de serviço → Classe cliente HTTP → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Classe de serviço | ApexClass | executa | Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados. | Classe invocável | Classe cliente HTTP | Obrigatório | L38 chamada a partir do ponto de entrada (`new Classe(` / `Classe.metodo(`) |
| 7 | Classe cliente HTTP | ApexClass | executa | Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta. | Classe de serviço | Sistema externo | Obrigatório | C02 `new HttpRequest()` + C01/C03 |
| 8 | Classes de DTO / wrapper | ApexClass | lê/referencia | Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos. | Classe cliente HTTP | — | Opcional | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 9 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe cliente HTTP | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe cliente HTTP | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe cliente HTTP | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe cliente HTTP | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## b.2

**LWC / Screen Flow → uma classe que faz o callout**

Mesmo desenho do b.1, mas o próprio ponto de entrada faz a chamada.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [b.2.v1](#b2v1) | Origem LWC · endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.2.v2](#b2v2) | Origem LWC · endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida)) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.2.v3](#b2v3) | Origem LWC · endpoint E3 (URL fixa no código Apex + Remote Site Setting) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.2.v4](#b2v4) | Origem LWC · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.2.v5](#b2v5) | Origem LWC · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.2.v6](#b2v6) | Origem LWC · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.2.v7](#b2v7) | Origem Screen Flow · endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.2.v8](#b2v8) | Origem Screen Flow · endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida)) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.2.v9](#b2v9) | Origem Screen Flow · endpoint E3 (URL fixa no código Apex + Remote Site Setting) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.2.v10](#b2v10) | Origem Screen Flow · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.2.v11](#b2v11) | Origem Screen Flow · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.2.v12](#b2v12) | Origem Screen Flow · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="b2v1"></a>

### b.2.v1 — Origem LWC · endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Controller Apex | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Controller Apex | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v2"></a>

### b.2.v2 — Origem LWC · endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida))

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Controller Apex | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Controller Apex | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Controller Apex | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v3"></a>

### b.2.v3 — Origem LWC · endpoint E3 (URL fixa no código Apex + Remote Site Setting)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Controller Apex | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Controller Apex | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Controller Apex | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v4"></a>

### b.2.v4 — Origem LWC · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Controller Apex | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Controller Apex | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Controller Apex | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v5"></a>

### b.2.v5 — Origem LWC · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Controller Apex | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Controller Apex | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v6"></a>

### b.2.v6 — Origem LWC · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting)

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Controller Apex | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Controller Apex | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 10 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Controller Apex | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v7"></a>

### b.2.v7 — Origem Screen Flow · endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe invocável | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 13 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe invocável | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v8"></a>

### b.2.v8 — Origem Screen Flow · endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida))

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe invocável | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe invocável | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 12 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe invocável | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v9"></a>

### b.2.v9 — Origem Screen Flow · endpoint E3 (URL fixa no código Apex + Remote Site Setting)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe invocável | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe invocável | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe invocável | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v10"></a>

### b.2.v10 — Origem Screen Flow · endpoint E4 (Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe invocável | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe invocável | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe invocável | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v11"></a>

### b.2.v11 — Origem Screen Flow · endpoint E5 (Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 13 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe invocável | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 14 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe invocável | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |

<a id="b2v12"></a>

### b.2.v12 — Origem Screen Flow · endpoint E6 (Custom Setting ou Custom Label (endpoint) + Remote Site Setting)

Fluxo principal: Usuário → Screen Flow → Classe invocável → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe invocável | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Interruptor (kill switch) | CustomMetadata ou CustomPermission | lê/referencia | Chave liga/desliga: permite parar a integração sem mexer no código. | Classe invocável | — | Opcional | `customMetadata/*.md` [MA-CMD] ou `customPermissions/*.customPermission` [MA-CP] |
| 11 | Objeto de log de integração | CustomObject (__c) + CustomField | executa (DML) | Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas. | Classe invocável | — | Opcional | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |


## b.3

**Screen Flow → ação HTTP Callout (declarativa)**

Sem Apex. O assistente de HTTP Callout gera um registro de External Service.

> Observação: HTTP Callout exige Named Credential: as variantes E3–E6 não existem para este desenho.
> Observação: No XML, o registro gerado pelo HTTP Callout tem `registrationProviderType`=SchemaInferred (API 57.0+) [MA-ESR].

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [b.3.v1](#b3v1) | Endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential) | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.3.v2](#b3v2) | Endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida)) | Não | a Named Credential já autoriza o domínio [AX-RSS] |

<a id="b3v1"></a>

### b.3.v1 — Endpoint E1 (Named Credential (namedCredentialType=SecuredEndpoint) + External Credential)

Fluxo principal: Usuário → Screen Flow → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | Cadastro criado automaticamente quando alguém configura um HTTP Callout no Flow Builder. Guarda o que chamar (método e caminho) e o formato da resposta, para o Flow usar sem código. | Screen Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Ação HTTP Callout | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Ação HTTP Callout | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Permission Set (acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b3v2"></a>

### b.3.v2 — Endpoint E2 (Named Credential legada (namedCredentialType=Legacy, autenticação embutida))

Fluxo principal: Usuário → Screen Flow → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Ação HTTP Callout | ExternalServiceRegistration | lê/referencia | Cadastro criado automaticamente quando alguém configura um HTTP Callout no Flow Builder. Guarda o que chamar (método e caminho) e o formato da resposta, para o Flow usar sem código. | Screen Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Ação HTTP Callout | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Ação HTTP Callout | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Permission Set (acesso ao Flow) | PermissionSet | autoriza | Dá ao usuário permissão para rodar o Flow. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## b.4

**Flow ou Apex → External Service (OpenAPI)**

A API é registrada por um schema OpenAPI; Flow e Apex usam as ações geradas.

> Observação: External Services exigem Named Credential.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [b.4.v1](#b4v1) | Origem Screen Flow · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.4.v2](#b4v2) | Origem Screen Flow · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.4.v3](#b4v3) | Origem LWC + Apex · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.4.v4](#b4v4) | Origem LWC + Apex · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |

<a id="b4v1"></a>

### b.4.v1 — Origem Screen Flow · endpoint E1

Fluxo principal: Usuário → Screen Flow → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | Cadastro da API externa a partir do contrato dela (OpenAPI). A plataforma transforma cada operação da API em uma ação que o Flow ou o Apex pode chamar, sem montar HTTP à mão. | Screen Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="b4v2"></a>

### b.4.v2 — Origem Screen Flow · endpoint E2

Fluxo principal: Usuário → Screen Flow → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Registro de External Service | ExternalServiceRegistration | lê/referencia | Cadastro da API externa a partir do contrato dela (OpenAPI). A plataforma transforma cada operação da API em uma ação que o Flow ou o Apex pode chamar, sem montar HTTP à mão. | Screen Flow | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Registro de External Service | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="b4v3"></a>

### b.4.v3 — Origem LWC + Apex · endpoint E1

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela e chama a operação da API pelas classes geradas automaticamente (`ExternalService.<Servico>`). | Componente LWC | Registro de External Service | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Registro de External Service | ExternalServiceRegistration | lê/referencia | Cadastro da API externa a partir do contrato dela (OpenAPI). A plataforma transforma cada operação da API em uma ação que o Flow ou o Apex pode chamar, sem montar HTTP à mão. | Controller Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Registro de External Service | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |

<a id="b4v4"></a>

### b.4.v4 — Origem LWC + Apex · endpoint E2

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela e chama a operação da API pelas classes geradas automaticamente (`ExternalService.<Servico>`). | Componente LWC | Registro de External Service | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Registro de External Service | ExternalServiceRegistration | lê/referencia | Cadastro da API externa a partir do contrato dela (OpenAPI). A plataforma transforma cada operação da API em uma ação que o Flow ou o Apex pode chamar, sem montar HTTP à mão. | Controller Apex | Named Credential | Obrigatório | `externalServiceRegistrations/*.externalServiceRegistration` — `namedCredential` / `namedCredentialReference` (57.0+), `registrationProviderType` (SchemaInferred = criado pelo HTTP Callout, 57.0+ [MA-ESR] |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Registro de External Service | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Registro de External Service | — | Obrigatório | não aparece no projeto (ator) |


## b.5

**LWC / Screen Flow → stub SOAP gerado (WSDL2Apex)**

Callout SOAP com classes geradas a partir do WSDL.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [b.5.v1](#b5v1) | Origem LWC · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.5.v2](#b5v2) | Origem LWC · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.5.v3](#b5v3) | Origem LWC · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.5.v4](#b5v4) | Origem LWC · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.5.v5](#b5v5) | Origem LWC · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.5.v6](#b5v6) | Origem LWC · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.5.v7](#b5v7) | Origem Screen Flow · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.5.v8](#b5v8) | Origem Screen Flow · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.5.v9](#b5v9) | Origem Screen Flow · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.5.v10](#b5v10) | Origem Screen Flow · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.5.v11](#b5v11) | Origem Screen Flow · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.5.v12](#b5v12) | Origem Screen Flow · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="b5v1"></a>

### b.5.v1 — Origem LWC · endpoint E1

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Controller Apex | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Stub gerado (WSDL2Apex) | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v2"></a>

### b.5.v2 — Origem LWC · endpoint E2

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Controller Apex | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Stub gerado (WSDL2Apex) | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v3"></a>

### b.5.v3 — Origem LWC · endpoint E3

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Controller Apex | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Stub gerado (WSDL2Apex) | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v4"></a>

### b.5.v4 — Origem LWC · endpoint E4

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Controller Apex | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Stub gerado (WSDL2Apex) | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Stub gerado (WSDL2Apex) | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Stub gerado (WSDL2Apex) | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v5"></a>

### b.5.v5 — Origem LWC · endpoint E5

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Controller Apex | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Stub gerado (WSDL2Apex) | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Stub gerado (WSDL2Apex) | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Stub gerado (WSDL2Apex) | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v6"></a>

### b.5.v6 — Origem LWC · endpoint E6

Fluxo principal: Usuário → Componente LWC → Controller Apex → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor. | Componente LWC | próximo componente | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Controller Apex | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Stub gerado (WSDL2Apex) | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v7"></a>

### b.5.v7 — Origem Screen Flow · endpoint E1

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Classe invocável | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 7 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Stub gerado (WSDL2Apex) | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v8"></a>

### b.5.v8 — Origem Screen Flow · endpoint E2

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Classe invocável | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 7 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Stub gerado (WSDL2Apex) | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v9"></a>

### b.5.v9 — Origem Screen Flow · endpoint E3

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Classe invocável | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Stub gerado (WSDL2Apex) | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v10"></a>

### b.5.v10 — Origem Screen Flow · endpoint E4

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Classe invocável | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Stub gerado (WSDL2Apex) | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Stub gerado (WSDL2Apex) | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Stub gerado (WSDL2Apex) | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 10 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 11 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v11"></a>

### b.5.v11 — Origem Screen Flow · endpoint E5

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Classe invocável | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 7 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Stub gerado (WSDL2Apex) | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Stub gerado (WSDL2Apex) | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 9 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Stub gerado (WSDL2Apex) | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="b5v12"></a>

### b.5.v12 — Origem Screen Flow · endpoint E6

Fluxo principal: Usuário → Screen Flow → Classe invocável → Stub gerado (WSDL2Apex) → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Ponto de entrada | FlexiPage, QuickAction ou CustomTab | lê/referencia | Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba. | Usuário | Screen Flow | Opcional | `flexipages/*.flexipage` [MA-FP] ou `quickActions/*.quickAction` [MA-QA] ou `tabs/*.tab` [MA-TAB] |
| 3 | Screen Flow | Flow | executa | Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo. | Ponto de entrada | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 4 | Versão ativa do Flow | FlowDefinition | lê/referencia | Arquivo antigo que só indica qual versão do Flow está ativa. | plataforma | — | Opcional | `flowDefinitions/*.flowDefinition` — versão ativa (formato legado) [MA-FD] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor. | Screen Flow | próximo componente | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Stub gerado (WSDL2Apex) | ApexClass | executa | Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código. | Classe invocável | Sistema externo | Obrigatório | C15 `WebServiceCallout.invoke` / `endpoint_x` |
| 7 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Stub gerado (WSDL2Apex) | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 8 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Stub gerado (WSDL2Apex) | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## b.6

**LWC → Apex Continuation**

Chamada longa (até 120 s) sem prender thread do servidor.

> Observação: Confirmado [AX-CONTL]: até 3 callouts paralelos, 3 encadeados, timeout máximo de 120 s por continuation.
> Observação: Confirmado [LWC-CONT]: o método é anotado com `@AuraEnabled(continuation=true)` (pode ter `cacheable=true`); o LWC processa uma Continuation por vez [LWC-CONTL].

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [b.6.v1](#b6v1) | Endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.6.v2](#b6v2) | Endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.6.v3](#b6v3) | Endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.6.v4](#b6v4) | Endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [b.6.v5](#b6v5) | Endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [b.6.v6](#b6v6) | Endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="b6v1"></a>

### b.6.v1 — Endpoint E1

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que inicia uma chamada demorada sem prender o servidor: devolve um objeto `Continuation` (método `@AuraEnabled(continuation=true)`) e a plataforma espera a resposta por ela. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Método de callback | ApexClass | executa | Método chamado automaticamente quando a resposta chega. Ele trata o retorno e entrega o resultado para a tela. | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório | C17 método indicado em `continuationMethod` |

<a id="b6v2"></a>

### b.6.v2 — Endpoint E2

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que inicia uma chamada demorada sem prender o servidor: devolve um objeto `Continuation` (método `@AuraEnabled(continuation=true)`) e a plataforma espera a resposta por ela. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Controller Apex | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Método de callback | ApexClass | executa | Método chamado automaticamente quando a resposta chega. Ele trata o retorno e entrega o resultado para a tela. | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório | C17 método indicado em `continuationMethod` |

<a id="b6v3"></a>

### b.6.v3 — Endpoint E3

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que inicia uma chamada demorada sem prender o servidor: devolve um objeto `Continuation` (método `@AuraEnabled(continuation=true)`) e a plataforma espera a resposta por ela. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Controller Apex | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Método de callback | ApexClass | executa | Método chamado automaticamente quando a resposta chega. Ele trata o retorno e entrega o resultado para a tela. | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório | C17 método indicado em `continuationMethod` |

<a id="b6v4"></a>

### b.6.v4 — Endpoint E4

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que inicia uma chamada demorada sem prender o servidor: devolve um objeto `Continuation` (método `@AuraEnabled(continuation=true)`) e a plataforma espera a resposta por ela. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Controller Apex | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Método de callback | ApexClass | executa | Método chamado automaticamente quando a resposta chega. Ele trata o retorno e entrega o resultado para a tela. | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório | C17 método indicado em `continuationMethod` |

<a id="b6v5"></a>

### b.6.v5 — Endpoint E5

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que inicia uma chamada demorada sem prender o servidor: devolve um objeto `Continuation` (método `@AuraEnabled(continuation=true)`) e a plataforma espera a resposta por ela. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Método de callback | ApexClass | executa | Método chamado automaticamente quando a resposta chega. Ele trata o retorno e entrega o resultado para a tela. | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório | C17 método indicado em `continuationMethod` |

<a id="b6v6"></a>

### b.6.v6 — Endpoint E6

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo → Método de callback

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente. | Usuário | LWC | Opcional (ou CustomTab / QuickAction) | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | Componente LWC | LightningComponentBundle | executa | Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`). | Página Lightning | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 4 | Controller Apex | ApexClass | executa | Classe Apex que inicia uma chamada demorada sem prender o servidor: devolve um objeto `Continuation` (método `@AuraEnabled(continuation=true)`) e a plataforma espera a resposta por ela. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Controller Apex | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Método de callback | ApexClass | executa | Método chamado automaticamente quando a resposta chega. Ele trata o retorno e entrega o resultado para a tela. | plataforma (ao chegar a resposta) | Componente LWC | Obrigatório | C17 método indicado em `continuationMethod` |


## c.1

**FlexCard → Integration Procedure → HTTP Action**

Exibição de dado externo via OmniStudio.

> ⚠️ A validar: `OmniUiCard`, `OmniIntegrationProcedure`, `OmniDataTransform` e `OmniScript` não constam na lista de Metadata Types do Metadata API Developer Guide (API 68.0) [MA-TYPES]. Confirmar na documentação do OmniStudio. No pacote gerenciado (Vlocity) esses itens são registros/DataPacks.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [c.1.v1](#c1v1) | Sem Data Mapper · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.1.v2](#c1v2) | Sem Data Mapper · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.1.v3](#c1v3) | Sem Data Mapper · endpoint E3 (URL fixa na HTTP Action + Remote Site) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [c.1.v4](#c1v4) | Com Data Mapper · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.1.v5](#c1v5) | Com Data Mapper · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.1.v6](#c1v6) | Com Data Mapper · endpoint E3 (URL fixa na HTTP Action + Remote Site) | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="c1v1"></a>

### c.1.v1 — Sem Data Mapper · endpoint E1

Fluxo principal: Usuário → FlexCard → Integration Procedure → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página onde o cartão (FlexCard) aparece para o usuário. | Usuário | FlexCard | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | FlexCard | OmniUiCard | executa | Cartão de tela do OmniStudio que mostra informações. Ele busca os dados chamando uma Integration Procedure. | Página Lightning | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio, montado sem código. Um passo do tipo HTTP Action chama o sistema externo. | FlexCard | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="c1v2"></a>

### c.1.v2 — Sem Data Mapper · endpoint E2

Fluxo principal: Usuário → FlexCard → Integration Procedure → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página onde o cartão (FlexCard) aparece para o usuário. | Usuário | FlexCard | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | FlexCard | OmniUiCard | executa | Cartão de tela do OmniStudio que mostra informações. Ele busca os dados chamando uma Integration Procedure. | Página Lightning | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio, montado sem código. Um passo do tipo HTTP Action chama o sistema externo. | FlexCard | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="c1v3"></a>

### c.1.v3 — Sem Data Mapper · endpoint E3 (URL fixa na HTTP Action + Remote Site)

Fluxo principal: Usuário → FlexCard → Integration Procedure → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página onde o cartão (FlexCard) aparece para o usuário. | Usuário | FlexCard | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | FlexCard | OmniUiCard | executa | Cartão de tela do OmniStudio que mostra informações. Ele busca os dados chamando uma Integration Procedure. | Página Lightning | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio, montado sem código. Um passo do tipo HTTP Action chama o sistema externo. | FlexCard | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos permitidos. Como a URL foi escrita direto na HTTP Action (sem Named Credential), o domínio **precisa** estar cadastrado aqui. | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="c1v4"></a>

### c.1.v4 — Com Data Mapper · endpoint E1

Fluxo principal: Usuário → FlexCard → Integration Procedure → Data Mapper / DataRaptor Transform → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página onde o cartão (FlexCard) aparece para o usuário. | Usuário | FlexCard | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | FlexCard | OmniUiCard | executa | Cartão de tela do OmniStudio que mostra informações. Ele busca os dados chamando uma Integration Procedure. | Página Lightning | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio, montado sem código. Um passo do tipo HTTP Action chama o sistema externo. | FlexCard | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Data Mapper / DataRaptor Transform | OmniDataTransform | executa | Ferramenta de mapeamento do OmniStudio: converte a resposta do sistema externo no formato que o cartão espera. | Integration Procedure | — | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="c1v5"></a>

### c.1.v5 — Com Data Mapper · endpoint E2

Fluxo principal: Usuário → FlexCard → Integration Procedure → Data Mapper / DataRaptor Transform → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página onde o cartão (FlexCard) aparece para o usuário. | Usuário | FlexCard | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | FlexCard | OmniUiCard | executa | Cartão de tela do OmniStudio que mostra informações. Ele busca os dados chamando uma Integration Procedure. | Página Lightning | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio, montado sem código. Um passo do tipo HTTP Action chama o sistema externo. | FlexCard | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Data Mapper / DataRaptor Transform | OmniDataTransform | executa | Ferramenta de mapeamento do OmniStudio: converte a resposta do sistema externo no formato que o cartão espera. | Integration Procedure | — | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="c1v6"></a>

### c.1.v6 — Com Data Mapper · endpoint E3 (URL fixa na HTTP Action + Remote Site)

Fluxo principal: Usuário → FlexCard → Integration Procedure → Data Mapper / DataRaptor Transform → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning | FlexiPage | lê/referencia | Página onde o cartão (FlexCard) aparece para o usuário. | Usuário | FlexCard | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | FlexCard | OmniUiCard | executa | Cartão de tela do OmniStudio que mostra informações. Ele busca os dados chamando uma Integration Procedure. | Página Lightning | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio, montado sem código. Um passo do tipo HTTP Action chama o sistema externo. | FlexCard | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Data Mapper / DataRaptor Transform | OmniDataTransform | executa | Ferramenta de mapeamento do OmniStudio: converte a resposta do sistema externo no formato que o cartão espera. | Integration Procedure | — | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos permitidos. Como a URL foi escrita direto na HTTP Action (sem Named Credential), o domínio **precisa** estar cadastrado aqui. | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |


## c.2

**OmniScript → Integration Procedure ou Remote Action**

Processo guiado com etapa de integração.

> ⚠️ A validar: Mesmos pontos do c.1; interface da Remote Action depende do runtime (padrão ou pacote).

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [c.2.v1](#c2v1) | Via Integration Procedure · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.2.v2](#c2v2) | Via Integration Procedure · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.2.v3](#c2v3) | Via Integration Procedure · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [c.2.v4](#c2v4) | Via Remote Action (Apex) · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.2.v5](#c2v5) | Via Remote Action (Apex) · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.2.v6](#c2v6) | Via Remote Action (Apex) · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [c.2.v7](#c2v7) | Via Remote Action (Apex) · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [c.2.v8](#c2v8) | Via Remote Action (Apex) · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [c.2.v9](#c2v9) | Via Remote Action (Apex) · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="c2v1"></a>

### c.2.v1 — Via Integration Procedure · endpoint E1

Fluxo principal: Usuário → OmniScript → Integration Procedure → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio. Um passo do tipo HTTP Action chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Integration Procedure | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="c2v2"></a>

### c.2.v2 — Via Integration Procedure · endpoint E2

Fluxo principal: Usuário → OmniScript → Integration Procedure → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio. Um passo do tipo HTTP Action chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Integration Procedure | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="c2v3"></a>

### c.2.v3 — Via Integration Procedure · endpoint E3

Fluxo principal: Usuário → OmniScript → Integration Procedure → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Integration Procedure | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Integration Procedure | OmniIntegrationProcedure | executa | Roteiro de integração do OmniStudio. Um passo do tipo HTTP Action chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos permitidos. Como a URL é fixa (sem Named Credential), o domínio **precisa** estar cadastrado aqui. | plataforma | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Integration Procedure | — | Obrigatório | não aparece no projeto (ator) |

<a id="c2v4"></a>

### c.2.v4 — Via Remote Action (Apex) · endpoint E1

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Classe Remote Action | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Classe Remote Action | ApexClass | executa | Classe Apex chamada pelo OmniScript (implementa `Callable` ou a interface do pacote). Ela chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe Remote Action | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 7 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Remote Action | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="c2v5"></a>

### c.2.v5 — Via Remote Action (Apex) · endpoint E2

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Classe Remote Action | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Classe Remote Action | ApexClass | executa | Classe Apex chamada pelo OmniScript (implementa `Callable` ou a interface do pacote). Ela chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe Remote Action | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 6 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 7 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Remote Action | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="c2v6"></a>

### c.2.v6 — Via Remote Action (Apex) · endpoint E3

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Classe Remote Action | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Classe Remote Action | ApexClass | executa | Classe Apex chamada pelo OmniScript (implementa `Callable` ou a interface do pacote). Ela chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 6 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe Remote Action | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Remote Action | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="c2v7"></a>

### c.2.v7 — Via Remote Action (Apex) · endpoint E4

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Classe Remote Action | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Classe Remote Action | ApexClass | executa | Classe Apex chamada pelo OmniScript (implementa `Callable` ou a interface do pacote). Ela chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe Remote Action | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe Remote Action | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe Remote Action | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 8 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Remote Action | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="c2v8"></a>

### c.2.v8 — Via Remote Action (Apex) · endpoint E5

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Classe Remote Action | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Classe Remote Action | ApexClass | executa | Classe Apex chamada pelo OmniScript (implementa `Callable` ou a interface do pacote). Ela chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe Remote Action | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 6 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe Remote Action | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe Remote Action | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Remote Action | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="c2v9"></a>

### c.2.v9 — Via Remote Action (Apex) · endpoint E6

Fluxo principal: Usuário → OmniScript → Classe Remote Action → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Página Lightning / Experience | FlexiPage | lê/referencia | Página onde o processo guiado (OmniScript) aparece. | Usuário | OmniScript | Opcional | `flexipages/*.flexipage` — componentes da página (`componentName`) — LWC, FlexCard, Canvas [MA-FP] |
| 3 | OmniScript | OmniScript | executa | Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração. | Página | Classe Remote Action | Obrigatório | não confirmado (ver NAO_CONFIRMADOS) |
| 4 | Classe Remote Action | ApexClass | executa | Classe Apex chamada pelo OmniScript (implementa `Callable` ou a interface do pacote). Ela chama o sistema externo. | OmniScript | Sistema externo | Obrigatório | `classes/*.cls + .cls-meta.xml` — ver padrões de código Apex [MA-CLS] |
| 5 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe Remote Action | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe Remote Action | — | Obrigatório | não aparece no projeto (ator) |
| 8 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |


## d.1

**LWC → fetch direto do navegador**

Sem servidor Salesforce no meio. Só para APIs públicas ou com token do próprio usuário.

> Observação: Não usa Named Credential nem Remote Site Setting: quem autoriza é a CSP (`CspTrustedSite`) e o CORS do sistema externo.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [d.1.v1](#d1v1) | URL no JavaScript | Não | a chamada sai do navegador; quem libera é o CSP Trusted Site |
| [d.1.v2](#d1v2) | URL em Custom Label | Não | a chamada sai do navegador; quem libera é o CSP Trusted Site |
| [d.1.v3](#d1v3) | URL em Custom Metadata via Apex | Não | a chamada sai do navegador; quem libera é o CSP Trusted Site |

<a id="d1v1"></a>

### d.1.v1 — URL no JavaScript

Fluxo principal: Usuário → Componente LWC → Sistema externo

Remote Site Setting: **Não** — a chamada sai do navegador; quem libera é o CSP Trusted Site.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Componente LWC | LightningComponentBundle | executa | Componente de tela que chama a API externa direto do navegador do usuário (`fetch()`), sem passar pelo servidor Salesforce. | Página | Sistema externo | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 3 | CSP Trusted Site | CspTrustedSite | autoriza | Lista de domínios que o **navegador** pode acessar a partir de páginas do Salesforce (regra de segurança CSP). Aqui não se usa Remote Site Setting: ele vale só para chamadas feitas pelo servidor (Apex). | navegador | — | Obrigatório | `cspTrustedSites/*.cspTrustedSite` — `endpointUrl`, `context` (All, LEX, Communities, VisualForce...), `isActive`, `isApplicableToConnectSrc`, `isApplicableToFrameSrc`, `isApplicableToImgSrc` [MA-CSP] |
| 4 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Como a chamada vem do navegador, ele precisa permitir (CORS) chamadas vindas do domínio do Salesforce. | Componente LWC | — | Obrigatório | não aparece no projeto (ator) |

<a id="d1v2"></a>

### d.1.v2 — URL em Custom Label

Fluxo principal: Usuário → Componente LWC → Sistema externo

Remote Site Setting: **Não** — a chamada sai do navegador; quem libera é o CSP Trusted Site.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Componente LWC | LightningComponentBundle | executa | Componente de tela que chama a API externa direto do navegador do usuário (`fetch()`), sem passar pelo servidor Salesforce. | Página | Sistema externo | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 3 | Custom Label | CustomLabels | lê/referencia | Texto configurável (Custom Label) com a URL da API, lido pelo componente. | Componente LWC | — | Obrigatório | `labels/*` — rótulo com URL ou parâmetro de integração [MA-LBL] |
| 4 | CSP Trusted Site | CspTrustedSite | autoriza | Lista de domínios que o **navegador** pode acessar a partir de páginas do Salesforce (regra de segurança CSP). Aqui não se usa Remote Site Setting: ele vale só para chamadas feitas pelo servidor (Apex). | navegador | — | Obrigatório | `cspTrustedSites/*.cspTrustedSite` — `endpointUrl`, `context` (All, LEX, Communities, VisualForce...), `isActive`, `isApplicableToConnectSrc`, `isApplicableToFrameSrc`, `isApplicableToImgSrc` [MA-CSP] |
| 5 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Como a chamada vem do navegador, ele precisa permitir (CORS) chamadas vindas do domínio do Salesforce. | Componente LWC | — | Obrigatório | não aparece no projeto (ator) |

<a id="d1v3"></a>

### d.1.v3 — URL em Custom Metadata via Apex

Fluxo principal: Usuário → Componente LWC → Controller Apex → Sistema externo

Remote Site Setting: **Não** — a chamada sai do navegador; quem libera é o CSP Trusted Site.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Componente LWC | LightningComponentBundle | executa | Componente de tela que chama a API externa direto do navegador do usuário (`fetch()`), sem passar pelo servidor Salesforce. | Página | Sistema externo | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 3 | Controller Apex | ApexClass | executa | Classe Apex que só lê a URL na configuração e entrega ao componente. | Componente LWC | Registro de Custom Metadata | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 4 | Registro de Custom Metadata | CustomMetadata (+ CustomObject __mdt) | lê/referencia | Registro de configuração com a URL da API em cada ambiente. | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 5 | CSP Trusted Site | CspTrustedSite | autoriza | Lista de domínios que o **navegador** pode acessar a partir de páginas do Salesforce (regra de segurança CSP). Aqui não se usa Remote Site Setting: ele vale só para chamadas feitas pelo servidor (Apex). | navegador | — | Obrigatório | `cspTrustedSites/*.cspTrustedSite` — `endpointUrl`, `context` (All, LEX, Communities, VisualForce...), `isActive`, `isApplicableToConnectSrc`, `isApplicableToFrameSrc`, `isApplicableToImgSrc` [MA-CSP] |
| 6 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Como a chamada vem do navegador, ele precisa permitir (CORS) chamadas vindas do domínio do Salesforce. | Componente LWC | — | Obrigatório | não aparece no projeto (ator) |


## e.1

**Salesforce Connect (OData / cross-org)**

Virtualização: dado externo lido sob demanda, sem cópia.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [e.1.v1](#e1v1) | Autenticação na própria External Data Source | Não | o Salesforce Connect usa a External Data Source |
| [e.1.v2](#e1v2) | Autenticação via Named Credential | Não | a Named Credential já autoriza o domínio [AX-RSS] |

<a id="e1v1"></a>

### e.1.v1 — Autenticação na própria External Data Source

Fluxo principal: Usuário → Sistema externo

Remote Site Setting: **Não** — o Salesforce Connect usa a External Data Source.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | Tela onde os dados externos aparecem como se fossem registros do Salesforce. | Usuário | External Object | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] ou `tabs/*.tab` [MA-TAB] |
| 3 | External Object | CustomObject (__x) | lê/referencia | Objeto "espelho" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo. | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce. | External Object | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | External Data Source | ExternalDataSource | lê/referencia | Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar. | External Object | Sistema externo | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 6 | Permission Set | PermissionSet | autoriza | Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Sistema externo | não é metadata | ator | Serviço externo no padrão OData que responde às consultas. | External Data Source | — | Obrigatório | não aparece no projeto (ator) |

<a id="e1v2"></a>

### e.1.v2 — Autenticação via Named Credential

Fluxo principal: Usuário → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | Tela onde os dados externos aparecem como se fossem registros do Salesforce. | Usuário | External Object | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] ou `tabs/*.tab` [MA-TAB] |
| 3 | External Object | CustomObject (__x) | lê/referencia | Objeto "espelho" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo. | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce. | External Object | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | External Data Source | ExternalDataSource | lê/referencia | Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar. | External Object | Sistema externo | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 6 | Permission Set | PermissionSet | autoriza | Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | External Data Source | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 8 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 9 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 10 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | External Data Source | — | Obrigatório | não aparece no projeto (ator) |


## e.2

**Salesforce Connect com adaptador Apex**

Virtualização de APIs que não são OData.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [e.2.v1](#e2v1) | Adaptador Apex · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [e.2.v2](#e2v2) | Adaptador Apex · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [e.2.v3](#e2v3) | Adaptador Apex · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [e.2.v4](#e2v4) | Adaptador Apex · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [e.2.v5](#e2v5) | Adaptador Apex · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [e.2.v6](#e2v6) | Adaptador Apex · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="e2v1"></a>

### e.2.v1 — Adaptador Apex · endpoint E1

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | Tela onde os dados externos aparecem como se fossem registros do Salesforce. | Usuário | External Object | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] ou `tabs/*.tab` [MA-TAB] |
| 3 | External Object | CustomObject (__x) | lê/referencia | Objeto "espelho" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo. | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce. | External Object | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | External Data Source | ExternalDataSource | lê/referencia | Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar. | External Object | adaptador | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 6 | Permission Set | PermissionSet | autoriza | Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Provider do adaptador | ApexClass | executa | Classe Apex que "apresenta" o adaptador à plataforma: diz o que ele sabe fazer e como autentica. | External Data Source | Connection | Obrigatório | C14 `extends DataSource.Provider` |
| 8 | Connection do adaptador | ApexClass | executa | Classe Apex que faz o trabalho: descreve as tabelas e, a cada consulta ou busca, chama o sistema externo. | Provider | Sistema externo | Obrigatório | C14 `extends DataSource.Connection` |
| 9 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Connection do adaptador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 11 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 12 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 13 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Connection do adaptador | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v2"></a>

### e.2.v2 — Adaptador Apex · endpoint E2

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | Tela onde os dados externos aparecem como se fossem registros do Salesforce. | Usuário | External Object | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] ou `tabs/*.tab` [MA-TAB] |
| 3 | External Object | CustomObject (__x) | lê/referencia | Objeto "espelho" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo. | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce. | External Object | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | External Data Source | ExternalDataSource | lê/referencia | Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar. | External Object | adaptador | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 6 | Permission Set | PermissionSet | autoriza | Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Provider do adaptador | ApexClass | executa | Classe Apex que "apresenta" o adaptador à plataforma: diz o que ele sabe fazer e como autentica. | External Data Source | Connection | Obrigatório | C14 `extends DataSource.Provider` |
| 8 | Connection do adaptador | ApexClass | executa | Classe Apex que faz o trabalho: descreve as tabelas e, a cada consulta ou busca, chama o sistema externo. | Provider | Sistema externo | Obrigatório | C14 `extends DataSource.Connection` |
| 9 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Connection do adaptador | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 10 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 11 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 12 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Connection do adaptador | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v3"></a>

### e.2.v3 — Adaptador Apex · endpoint E3

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | Tela onde os dados externos aparecem como se fossem registros do Salesforce. | Usuário | External Object | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] ou `tabs/*.tab` [MA-TAB] |
| 3 | External Object | CustomObject (__x) | lê/referencia | Objeto "espelho" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo. | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce. | External Object | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | External Data Source | ExternalDataSource | lê/referencia | Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar. | External Object | adaptador | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 6 | Permission Set | PermissionSet | autoriza | Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Provider do adaptador | ApexClass | executa | Classe Apex que "apresenta" o adaptador à plataforma: diz o que ele sabe fazer e como autentica. | External Data Source | Connection | Obrigatório | C14 `extends DataSource.Provider` |
| 8 | Connection do adaptador | ApexClass | executa | Classe Apex que faz o trabalho: descreve as tabelas e, a cada consulta ou busca, chama o sistema externo. | Provider | Sistema externo | Obrigatório | C14 `extends DataSource.Connection` |
| 9 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 10 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Connection do adaptador | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Connection do adaptador | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v4"></a>

### e.2.v4 — Adaptador Apex · endpoint E4

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | Tela onde os dados externos aparecem como se fossem registros do Salesforce. | Usuário | External Object | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] ou `tabs/*.tab` [MA-TAB] |
| 3 | External Object | CustomObject (__x) | lê/referencia | Objeto "espelho" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo. | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce. | External Object | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | External Data Source | ExternalDataSource | lê/referencia | Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar. | External Object | adaptador | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 6 | Permission Set | PermissionSet | autoriza | Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Provider do adaptador | ApexClass | executa | Classe Apex que "apresenta" o adaptador à plataforma: diz o que ele sabe fazer e como autentica. | External Data Source | Connection | Obrigatório | C14 `extends DataSource.Provider` |
| 8 | Connection do adaptador | ApexClass | executa | Classe Apex que faz o trabalho: descreve as tabelas e, a cada consulta ou busca, chama o sistema externo. | Provider | Sistema externo | Obrigatório | C14 `extends DataSource.Connection` |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Connection do adaptador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Connection do adaptador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Connection do adaptador | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 12 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 13 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Connection do adaptador | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v5"></a>

### e.2.v5 — Adaptador Apex · endpoint E5

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | Tela onde os dados externos aparecem como se fossem registros do Salesforce. | Usuário | External Object | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] ou `tabs/*.tab` [MA-TAB] |
| 3 | External Object | CustomObject (__x) | lê/referencia | Objeto "espelho" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo. | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce. | External Object | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | External Data Source | ExternalDataSource | lê/referencia | Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar. | External Object | adaptador | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 6 | Permission Set | PermissionSet | autoriza | Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Provider do adaptador | ApexClass | executa | Classe Apex que "apresenta" o adaptador à plataforma: diz o que ele sabe fazer e como autentica. | External Data Source | Connection | Obrigatório | C14 `extends DataSource.Provider` |
| 8 | Connection do adaptador | ApexClass | executa | Classe Apex que faz o trabalho: descreve as tabelas e, a cada consulta ou busca, chama o sistema externo. | Provider | Sistema externo | Obrigatório | C14 `extends DataSource.Connection` |
| 9 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Connection do adaptador | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 10 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Connection do adaptador | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 11 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Connection do adaptador | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 12 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 13 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 14 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Connection do adaptador | — | Obrigatório | não aparece no projeto (ator) |

<a id="e2v6"></a>

### e.2.v6 — Adaptador Apex · endpoint E6

Fluxo principal: Usuário → Provider do adaptador → Connection do adaptador → Sistema externo

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Layout / Página / Aba | Layout, FlexiPage ou CustomTab | lê/referencia | Tela onde os dados externos aparecem como se fossem registros do Salesforce. | Usuário | External Object | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] ou `tabs/*.tab` [MA-TAB] |
| 3 | External Object | CustomObject (__x) | lê/referencia | Objeto "espelho" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo. | Página | External Data Source | Obrigatório | `objects/X__x/` (sufixo `__x`) [MA-CO] |
| 4 | Campos e relacionamentos externos | CustomField | lê/referencia | Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce. | External Object | — | Obrigatório | `objects (dentro do objeto; decomposto no source format)/*` — `externalId` = true (chave de upsert), `type` ExternalLookup/IndirectLookup, `referenceTo` [MA-CF] |
| 5 | External Data Source | ExternalDataSource | lê/referencia | Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar. | External Object | adaptador | Obrigatório | `dataSources/*.dataSource` — `type` (OData, OData4, SfdcOrg, ApexClassId = adaptador Apex, AmazonAthena, AmazonDynamoDB), `endpoint` (URL ou `callout:NomeNC`), `principalType`, `protocol`, `authProvider`, `certificate`, `customConfiguration` [MA-EDS] |
| 6 | Permission Set | PermissionSet | autoriza | Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 7 | Provider do adaptador | ApexClass | executa | Classe Apex que "apresenta" o adaptador à plataforma: diz o que ele sabe fazer e como autentica. | External Data Source | Connection | Obrigatório | C14 `extends DataSource.Provider` |
| 8 | Connection do adaptador | ApexClass | executa | Classe Apex que faz o trabalho: descreve as tabelas e, a cada consulta ou busca, chama o sistema externo. | Provider | Sistema externo | Obrigatório | C14 `extends DataSource.Connection` |
| 9 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Connection do adaptador | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Connection do adaptador | — | Obrigatório | não aparece no projeto (ator) |


## f.1

**Quick Action → Flow ou LWC → callout → atualiza o registro**

Enriquecimento sob demanda, iniciado pelo usuário.

**Mapa das variantes**

| Variante | Resumo | Usa Remote Site Setting? | Por quê |
|---|---|---|---|
| [f.1.v1](#f1v1) | Quick Action → Screen Flow · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [f.1.v2](#f1v2) | Quick Action → Screen Flow · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [f.1.v3](#f1v3) | Quick Action → Screen Flow · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [f.1.v4](#f1v4) | Quick Action → Screen Flow · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [f.1.v5](#f1v5) | Quick Action → Screen Flow · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [f.1.v6](#f1v6) | Quick Action → Screen Flow · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [f.1.v7](#f1v7) | Quick Action → LWC · endpoint E1 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [f.1.v8](#f1v8) | Quick Action → LWC · endpoint E2 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [f.1.v9](#f1v9) | Quick Action → LWC · endpoint E3 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [f.1.v10](#f1v10) | Quick Action → LWC · endpoint E4 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |
| [f.1.v11](#f1v11) | Quick Action → LWC · endpoint E5 | Não | a Named Credential já autoriza o domínio [AX-RSS] |
| [f.1.v12](#f1v12) | Quick Action → LWC · endpoint E6 | Sim, obrigatório | a URL não vem de uma Named Credential, então o domínio precisa estar liberado |

<a id="f1v1"></a>

### f.1.v1 — Quick Action → Screen Flow · endpoint E1

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Screen Flow | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Screen Flow | Flow | executa | Fluxo com tela que recebe o registro atual, chama o Apex e grava no registro o que voltou do sistema externo. | Quick Action | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que chama o sistema externo. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Classe invocável | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v2"></a>

### f.1.v2 — Quick Action → Screen Flow · endpoint E2

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Screen Flow | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Screen Flow | Flow | executa | Fluxo com tela que recebe o registro atual, chama o Apex e grava no registro o que voltou do sistema externo. | Quick Action | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que chama o sistema externo. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Classe invocável | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Classe invocável | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v3"></a>

### f.1.v3 — Quick Action → Screen Flow · endpoint E3

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Screen Flow | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Screen Flow | Flow | executa | Fluxo com tela que recebe o registro atual, chama o Apex e grava no registro o que voltou do sistema externo. | Quick Action | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que chama o sistema externo. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Classe invocável | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Classe invocável | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v4"></a>

### f.1.v4 — Quick Action → Screen Flow · endpoint E4

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Screen Flow | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Screen Flow | Flow | executa | Fluxo com tela que recebe o registro atual, chama o Apex e grava no registro o que voltou do sistema externo. | Quick Action | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que chama o sistema externo. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Classe invocável | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Classe invocável | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v5"></a>

### f.1.v5 — Quick Action → Screen Flow · endpoint E5

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Screen Flow | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Screen Flow | Flow | executa | Fluxo com tela que recebe o registro atual, chama o Apex e grava no registro o que voltou do sistema externo. | Quick Action | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que chama o sistema externo. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Classe invocável | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Classe invocável | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Classe invocável | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Classe invocável | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v6"></a>

### f.1.v6 — Quick Action → Screen Flow · endpoint E6

Fluxo principal: Usuário → Quick Action → Screen Flow → Classe invocável → Sistema externo → Objeto do registro

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Screen Flow | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Screen Flow | Flow | executa | Fluxo com tela que recebe o registro atual, chama o Apex e grava no registro o que voltou do sistema externo. | Quick Action | Classe invocável | Obrigatório | `flows (a página diz "Flow directory")/*.flow` — `start.triggerType` (RecordAfterSave, RecordBeforeSave, Scheduled, PlatformEvent...), `start.scheduledPaths.pathType` = AsyncAfterCommit (caminho assíncrono), `actionCalls` com `actionType` (apex, externalService, flow, quickAction, component, lwcComponent) e `actionName`, `flowTransactionModel`, `recordCreates` em `X__e` [MA-FLOW] |
| 5 | Classe invocável | ApexClass | executa | Classe Apex que chama o sistema externo. | Screen Flow | Sistema externo | Obrigatório | C22 `@InvocableMethod` (com `callout=true` se chamar sistema externo) |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Classe invocável | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Classe invocável | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Classe invocável | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v7"></a>

### f.1.v7 — Quick Action → LWC · endpoint E1

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Componente LWC | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | Componente de tela aberto pelo botão; recebe o registro atual e chama o Apex. | Quick Action | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 5 | Controller Apex | ApexClass | executa | Classe Apex que chama o sistema externo. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 6 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**. | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | External Credential | ExternalCredential | autoriza | Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 8 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 9 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS). | External Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 10 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 11 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Controller Apex | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 12 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v8"></a>

### f.1.v8 — Quick Action → LWC · endpoint E2

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Componente LWC | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | Componente de tela aberto pelo botão; recebe o registro atual e chama o Apex. | Quick Action | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 5 | Controller Apex | ApexClass | executa | Classe Apex que chama o sistema externo. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 6 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**. | Controller Apex | Sistema externo | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 7 | Auth Provider | AuthProvider | autoriza | Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token. | Named Credential | — | Opcional | `authproviders/*.authprovider` — `providerType`, `authorizeUrl`, `tokenUrl`, `registrationHandler` (Apex `Auth.RegistrationHandler`), `executionUser`, `plugin` (Apex `Auth.AuthProviderPluginClass`) [MA-AP] |
| 8 | Certificate | Certificate | autoriza | Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS. | Named Credential | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 9 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 10 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Controller Apex | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 11 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v9"></a>

### f.1.v9 — Quick Action → LWC · endpoint E3

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Componente LWC | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | Componente de tela aberto pelo botão; recebe o registro atual e chama o Apex. | Quick Action | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 5 | Controller Apex | ApexClass | executa | Classe Apex que chama o sistema externo. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 6 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 7 | Certificate | Certificate | autoriza | Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`. | Controller Apex | — | Opcional | `certs/*.crt` — nome do certificado referenciado por NamedCredential, ConnectedApp, ExternalDataSource ou `setClientCertificateName` [MA-CERT] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Controller Apex | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v10"></a>

### f.1.v10 — Quick Action → LWC · endpoint E4

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Componente LWC | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | Componente de tela aberto pelo botão; recebe o registro atual e chama o Apex. | Quick Action | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 5 | Controller Apex | ApexClass | executa | Classe Apex que chama o sistema externo. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado). | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01). | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Classe de token | ApexClass | executa | Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal. | Controller Apex | endpoint de token do sistema externo | Opcional | C02 callout ao endpoint de token; lê CMDT |
| 9 | Partição de cache | PlatformCachePartition | lê/referencia | Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada. | Classe de token | — | Opcional | `cachePartitions/*.cachePartition` — partição usada para cache de token/resposta [MA-PCP] |
| 10 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Controller Apex | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v11"></a>

### f.1.v11 — Quick Action → LWC · endpoint E5

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

Remote Site Setting: **Não** — a Named Credential já autoriza o domínio [AX-RSS].

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Componente LWC | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | Componente de tela aberto pelo botão; recebe o registro atual e chama o Apex. | Quick Action | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 5 | Controller Apex | ApexClass | executa | Classe Apex que chama o sistema externo. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 6 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | É a "tabela" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis. | Controller Apex | registro de Custom Metadata | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 7 | Registro de Custom Metadata | CustomMetadata | lê/referencia | É a "linha" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro. | Controller Apex | — | Obrigatório | tipo: `objects/X__mdt/`; registros: `customMetadata/X.Reg.md` [MA-CMD] |
| 8 | Named Credential | NamedCredential | lê/referencia | Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**. | Controller Apex | External Credential | Obrigatório | `namedCredentials/*.namedCredential` — `namedCredentialType` (SecuredEndpoint = modelo novo [MA-NC] |
| 9 | External Credential | ExternalCredential | autoriza | Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo. | Named Credential | Sistema externo | Obrigatório | `externalCredentials/*.externalCredential` — `authenticationProtocol` [MA-EC] |
| 10 | Permission Set (acesso ao principal) | PermissionSet | autoriza | Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha. | plataforma (no momento do callout) | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |
| 11 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 12 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Controller Apex | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 13 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

<a id="f1v12"></a>

### f.1.v12 — Quick Action → LWC · endpoint E6

Fluxo principal: Usuário → Quick Action → Componente LWC (screen ou headless action) → Controller Apex → Sistema externo → Objeto do registro

Remote Site Setting: **Sim, obrigatório** — a URL não vem de uma Named Credential, então o domínio precisa estar liberado.

| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |
|---|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta. | — | página | Obrigatório | não aparece no projeto (ator) |
| 2 | Quick Action | QuickAction | executa | Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC. | Usuário | Componente LWC | Obrigatório | `quickActions/*.quickAction` — `type` (Flow, LightningComponent, LightningWebComponent, Canvas, VisualforcePage...), `flowDefinition`, `lightningComponent`, `page`, `targetObject`, `actionSubtype` [MA-QA] |
| 3 | Layout / Página (onde a ação aparece) | Layout ou FlexiPage | lê/referencia | Configuração da página que faz o botão aparecer. | plataforma | — | Obrigatório | `layouts/*.layout (nv)` [MA-LAY] ou `flexipages/*.flexipage` [MA-FP] |
| 4 | Componente LWC (screen ou headless action) | LightningComponentBundle | executa | Componente de tela aberto pelo botão; recebe o registro atual e chama o Apex. | Quick Action | Controller Apex | Obrigatório | `lwc/<nome>/`; chama Apex via C24 `@salesforce/apex/Classe.metodo` |
| 5 | Controller Apex | ApexClass | executa | Classe Apex que chama o sistema externo. | Componente LWC | Sistema externo | Obrigatório | `@AuraEnabled` em `classes/*.cls` + C02 se fizer callout |
| 6 | Custom Setting ou Custom Label | CustomObject (Custom Setting) ou CustomLabels | lê/referencia | Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06). | Controller Apex | — | Obrigatório | `objects/*.object` [MA-CO] ou `labels/*` [MA-LBL] |
| 7 | Remote Site Setting | RemoteSiteSetting | autoriza | Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui. | plataforma (no momento do callout) | — | Obrigatório | `remoteSiteSettings/*.remoteSite` — `url`, `isActive`, `disableProtocolSecurity` [MA-RSS] |
| 8 | Sistema externo | não é metadata | ator | O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta. | Controller Apex | — | Obrigatório | não aparece no projeto (ator) |
| 9 | Objeto do registro | CustomObject + CustomField | executa (DML) | Registro que recebe os dados trazidos do sistema externo ("enriquecimento"). | Controller Apex | triggers/flows do objeto | Obrigatório | `objects/*.object` — sufixos de nome: `__c` (custom), `__x` (external object), `__e` (platform event) [PE-PUB], `__mdt` (custom metadata type) [MA-CMD] [MA-CO] |
| 10 | Permission Set (acesso às classes Apex) | PermissionSet | autoriza | Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso. | plataforma | — | Obrigatório | `permissionsets/*.permissionset` — `classAccesses` (`apexClass`), `externalCredentialPrincipalAccesses` (API 59.0+), `externalDataSourceAccesses`, `customMetadataTypeAccesses`, `objectPermissions` [MA-PS] |

