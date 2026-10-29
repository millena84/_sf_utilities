# Outras dinâmicas

> Gerado a partir das definições da base de integração. Convenções, legenda e códigos de variante: [README](README.md).

## Índice

- [N.1 — Org ↔ org](#n1) (4 variantes)
- [N.2 — Integração de UI](#n2) (5 variantes)
- [N.3 — Identidade (SSO)](#n3) (3 variantes)
- [N.4 — Data Cloud](#n4) (1 variantes)

## N.1

**Org ↔ org**

Integração entre orgs Salesforce.

> ⚠️ A validar: Salesforce to Salesforce (legado) não incluído: verificar se há metadata associada.

### N.1.v1 — Salesforce Connect cross-org

Fluxo principal: Usuário → Org Salesforce remota

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | External Object | CustomObject (__x) | lê/referencia | objetos da org remota | Página | External Data Source | Obrigatório |
| 3 | External Data Source (cross-org) | ExternalDataSource | lê/referencia | URL e identidade da org remota | External Object | Org remota | Obrigatório |
| 4 | Permission Set | PermissionSet | autoriza | acesso ao External Object | plataforma | — | Obrigatório |
| 5 | Org Salesforce remota | não é metadata | ator | responde às consultas via API | External Data Source | — | Obrigatório |

### N.1.v2 — Apex REST org→org · endpoint E1

Fluxo principal: Classe cliente (org A) → Org B

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório |
| 2 | Named Credential | NamedCredential | lê/referencia | resolve a URL base usada em `callout:Nome` | Classe cliente (org A) | External Credential | Obrigatório |
| 3 | External Credential | ExternalCredential | autoriza | fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals | Named Credential | Org B | Obrigatório |
| 4 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário que executa o callout acesso ao principal da External Credential | plataforma (no momento do callout) | — | Obrigatório |
| 5 | Certificate | Certificate | autoriza | assina o JWT ou faz mutual TLS, quando o protocolo exige | External Credential | — | Opcional |
| 6 | Org B | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente (org A) | — | Obrigatório |
| 7 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório |
| 8 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) |

### N.1.v3 — Apex REST org→org · endpoint E2

Fluxo principal: Classe cliente (org A) → Org B

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório |
| 2 | Named Credential (legada) | NamedCredential | lê/referencia + autoriza | resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT) | Classe cliente (org A) | Org B | Obrigatório |
| 3 | Auth Provider | AuthProvider | autoriza | obtém o token OAuth quando a Named Credential legada usa OAuth | Named Credential | — | Opcional |
| 4 | Certificate | Certificate | autoriza | assina JWT ou mutual TLS | Named Credential | — | Opcional |
| 5 | Org B | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente (org A) | — | Obrigatório |
| 6 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório |
| 7 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) |

### N.1.v4 — Apex REST org→org · endpoint E5

Fluxo principal: Classe cliente (org A) → Org B

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Classe cliente (org A) | ApexClass | executa | faz o callout para a org B | trigger/UI/agenda | Org B | Obrigatório |
| 2 | Tipo de Custom Metadata | CustomObject (__mdt) + CustomField | lê/referencia | define o campo com o nome da Named Credential e parâmetros não sensíveis | Classe cliente (org A) | registro de Custom Metadata | Obrigatório |
| 3 | Registro de Custom Metadata | CustomMetadata | lê/referencia | indica qual Named Credential usar e os parâmetros (path, timeout, ativo) | Classe cliente (org A) | — | Obrigatório |
| 4 | Named Credential | NamedCredential | lê/referencia | resolve a URL base (`callout:` + nome lido do CMDT) | Classe cliente (org A) | External Credential | Obrigatório |
| 5 | External Credential | ExternalCredential | autoriza | fornece a autenticação | Named Credential | Org B | Obrigatório |
| 6 | Permission Set (acesso ao principal) | PermissionSet | autoriza | dá ao usuário executor acesso ao principal | plataforma (no momento do callout) | — | Obrigatório |
| 7 | Org B | não é metadata | ator | recebe a requisição e devolve a resposta | Classe cliente (org A) | — | Obrigatório |
| 8 | Connected App / External Client App (org B) | ConnectedApp ou ExternalClientApplication | autoriza | emite o token | Named Credential | — | Obrigatório |
| 9 | Classe Apex REST (org B) | ApexClass | executa | recebe e processa | Org A | objetos da org B | Opcional (ou API padrão) |


## N.2

**Integração de UI**

O usuário vê ou usa outro sistema; pouca ou nenhuma troca de dados no servidor.

### N.2.v1 — Botão/link de URL

Fluxo principal: Usuário → Botão ou link → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Botão ou link | WebLink | executa | abre o sistema externo com parâmetros do registro na URL | Usuário | Sistema externo | Obrigatório |
| 3 | Layout | Layout | lê/referencia | expõe o botão | plataforma | — | Obrigatório |
| 4 | Sistema externo | não é metadata | ator | abre no navegador | WebLink | — | Obrigatório |

### N.2.v2 — Web Tab

Fluxo principal: Usuário → Aba web → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Aba web | CustomTab | executa | carrega a URL externa | Usuário | Sistema externo | Obrigatório |
| 3 | App | CustomApplication | lê/referencia | inclui a aba | plataforma | — | Obrigatório |
| 4 | Sistema externo | não é metadata | ator | exibido em frame | CustomTab | — | Obrigatório |

### N.2.v3 — Canvas em Visualforce

Fluxo principal: Usuário → Página Visualforce → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Visualforce | ApexPage | executa | `<apex:canvasApp>` | Usuário | Canvas App | Obrigatório |
| 3 | Connected App com Canvas | ConnectedApp | autoriza + lê | URL do Canvas, método de acesso (signed request/OAuth), locais permitidos | host | Sistema externo | Obrigatório |
| 4 | Sistema externo | não é metadata | ator | app web que recebe o signed request | Canvas | — | Obrigatório |

### N.2.v4 — Canvas em Lightning Page

Fluxo principal: Usuário → Página Lightning → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Página Lightning | FlexiPage | executa | componente padrão Canvas App | Usuário | Canvas App | Obrigatório |
| 3 | Connected App com Canvas | ConnectedApp | autoriza + lê | URL do Canvas, método de acesso (signed request/OAuth), locais permitidos | host | Sistema externo | Obrigatório |
| 4 | Sistema externo | não é metadata | ator | app web que recebe o signed request | Canvas | — | Obrigatório |

### N.2.v5 — iframe em LWC

Fluxo principal: Usuário → Componente LWC → Sistema externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Usuário | não é metadata | ator | inicia a ação na tela | — | página | Obrigatório |
| 2 | Componente LWC | LightningComponentBundle | executa | renderiza `<iframe>` | Página | Sistema externo | Obrigatório |
| 3 | CSP Trusted Site | CspTrustedSite | autoriza | libera o domínio em `frame-src` | navegador | — | Obrigatório |
| 4 | Sistema externo | não é metadata | ator | precisa permitir ser emoldurado (X-Frame-Options/CSP) | LWC | — | Obrigatório |


## N.3

**Identidade (SSO)**

Integra o login, não os dados.

### N.3.v1 — SAML com IdP externo

Fluxo principal: IdP externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | IdP externo | não é metadata | ator | autentica o usuário | Usuário | Salesforce | Obrigatório |
| 2 | Configuração SAML | SamlSsoConfig | autoriza | emissor, certificado, mapeamento de identidade | IdP | — | Obrigatório |
| 3 | Certificate | Certificate | autoriza | valida/assina asserções | SAML | — | Opcional |

### N.3.v2 — OpenID Connect via Auth Provider

Fluxo principal: Provedor externo → Registration Handler

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Provedor externo | não é metadata | ator | autentica | Usuário | Salesforce | Obrigatório |
| 2 | Auth Provider | AuthProvider | autoriza | configuração OIDC | login | Registration Handler | Obrigatório |
| 3 | Registration Handler | ApexClass | executa | cria/atualiza o usuário a partir dos dados do provedor | Auth Provider | User | Obrigatório |

### N.3.v3 — Salesforce como IdP

Fluxo principal: App externo

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | App externo | não é metadata | ator | pede login | Usuário | Salesforce | Obrigatório |
| 2 | Connected App (SAML/OIDC) | ConnectedApp | autoriza | app de serviço; Salesforce emite asserção/token | App externo | — | Obrigatório |


## N.4

**Data Cloud**

Ingestão e ativação de dados.

> ⚠️ A validar: Toda a família de metadata do Data Cloud.

### N.4.v1 — A validar

Fluxo principal: Data Cloud

| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |
|---|---|---|---|---|---|---|---|
| 1 | Data Cloud | não é metadata | ator | metadata types de data streams, data sources e ativações a confirmar | — | — | Obrigatório |

