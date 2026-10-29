# Base de conhecimento: desenhos de integração Salesforce

Catálogo de **desenhos de integração** com todas as variantes multiplicadas. Cada variante traz a relação completa de componentes (metadata types), o papel de cada um, a ordem e quem aciona quem.

Objetivo: servir de base para agentes de IA que leem a estrutura de um projeto Salesforce e documentam as integrações. O agente compara os componentes encontrados no projeto com as variantes daqui para identificar o desenho.

Uso no pacote de prompts (`documentacaoInt/`): é material de consulta, principalmente para a Fase 1 (direção e mecanismo de cada ponto de integração), a Fase 2 (relações entre componentes) e a Fase 4 (etapas da jornada). Os desenhos descrevem **o que pode existir**; nunca afirme que um componente existe na org sem encontrá-lo em `<CAMINHO_ORG>`.

## Arquivos

| Arquivo | Título | Desenhos |
|---|---|---|
| [out-sync.md](out-sync.md) | Salesforce chama o externo e espera | b.1–b.6, c.1–c.2, d.1, e.1–e.2, f.1 |
| [in-sync.md](in-sync.md) | Externo chama o Salesforce e espera | g.1–g.7 |
| [out-async.md](out-async.md) | Salesforce envia sem esperar | D.1–D.4, E.1–E.4, F.1–F.4, G.1 |
| [in-async.md](in-async.md) | Externo envia; Salesforce processa depois | H.1–H.5 |
| [mid.md](mid.md) | Middleware / MuleSoft | M.1–M.7 |
| [outras.md](outras.md) | Org↔org, UI, SSO, Data Cloud | N.1–N.4 |

Identificador de variante: `<desenho>.v<n>` (ex.: `b.2.v4`).

| Arquivo de apoio | Uso |
|---|---|
| `desenhos.json` | Mesmo conteúdo em JSON (desenho → variantes → componentes). Preferível para agentes e scripts |
| `_fonte/` | Definições (`blocks.py`, `designs.py`) e gerador (`render.py`). Edite as definições e regenere: `python3 _fonte/render.py .` a partir desta pasta |

## Como ler cada tabela

| Coluna | Significado |
|---|---|
| Ordem | Sequência aproximada. Linhas **autoriza** são verificadas pela plataforma no momento da chamada; aparecem junto do passo que dependem dela |
| Componente | Nome funcional do papel no desenho |
| Metadata type | Nome na Metadata API. `não é metadata` = ator (usuário, sistema externo, API padrão, registro, agendamento) |
| Relação | **executa** (roda lógica), **executa (DML)** (grava dados), **lê/referencia** (é consultado/apontado), **autoriza** (libera acesso), **ator** (participante fora da metadata) |
| Acionado por / Aciona | Quem dispara o componente e o que ele dispara a seguir. `plataforma` = o próprio Salesforce |
| Obrigatoriedade | **Obrigatório** na variante; **Opcional** = comum, mas pode faltar |

"Fluxo principal" lista só os passos obrigatórios que executam ou são atores.

## Eixos de multiplicação

### Fonte de endpoint/autenticação em callouts Apex (OUT)

| Código | Variante | Componentes |
|---|---|---|
| E1 | Named Credential (modelo novo) + External Credential | `NamedCredential`, `ExternalCredential`, `PermissionSet` (principal), `Certificate` opcional |
| E2 | Named Credential legada | `NamedCredential`, `AuthProvider` e `Certificate` opcionais |
| E3 | URL fixa no código | `RemoteSiteSetting`, `Certificate` opcional |
| E4 | Custom Metadata (endpoint, client_id…) | `CustomObject (__mdt)`, `CustomField`, `CustomMetadata`, `RemoteSiteSetting`; classe de token e `PlatformCachePartition` opcionais |
| E5 | Custom Metadata com o nome da Named Credential | `CustomMetadata` + `NamedCredential` + `ExternalCredential` + `PermissionSet` |
| E6 | Custom Setting ou Custom Label | `CustomObject` (Custom Setting) ou `CustomLabels`, `RemoteSiteSetting` |

Flow (HTTP Callout), External Services e Integration Procedures (HTTP Action) só aparecem com E1/E2 (e URL fixa + Remote Site no caso da HTTP Action), porque dependem de Named Credential ou de URL configurada no próprio componente.

### Autenticação de entrada (IN)

Aplicativo: **Connected App** (`ConnectedApp`) ou **External Client App** (`ExternalClientApplication` + `ExtlClntAppOauthSettings`, `ExtlClntAppGlobalOauthSettings`, `ExtlClntAppOauthConfigurablePolicies`, `ExtlClntAppConfigurablePolicies`).

Fluxos OAuth: JWT Bearer, Client Credentials, Web Server + Refresh Token, Username-Password (legado).

Webhooks via Site (g.6) não usam OAuth.

### Mecanismo assíncrono

`@future(callout=true)`, Queueable (`Database.AllowsCallouts`, com Finalizer opcional), Batch (`Database.AllowsCallouts`), caminho assíncrono de Flow, Platform Event e Change Data Capture.

## Premissas

- Nenhum destes é obrigatório por definição: Named Credential, Connected App/External Client App, Custom Metadata, Remote Site Setting, External Credential, Platform Event, CSP Trusted Site. Cada um só é obrigatório dentro da variante que o usa.
- Callout síncrono não é permitido em trigger Apex, nem no caminho imediato de Flow record-triggered, nem em trigger de Platform Event. Esses casos aparecem sempre com mecanismo assíncrono.
- **Custom Metadata com segredo:** `client_id` costuma ser aceitável; `client_secret`, senha, token e chave privada em Custom Metadata ficam legíveis por Apex e por quem vê o Setup, e vão para o repositório (segredo versionado). Prefira External Credential/Named Credential ou `Certificate`.
- `EventRelayConfig` (E.4) envia eventos ao Amazon EventBridge.

## Itens a validar

Marcados com ⚠️ nos arquivos. Principais:

- OmniStudio padrão: nomes `OmniUiCard`, `OmniIntegrationProcedure`, `OmniDataTransform`, `OmniScript`; no pacote gerenciado são registros/DataPacks.
- Callout em Platform Event–Triggered Flow e em Schedule-Triggered Flow.
- Ação Outbound Message em Flow e criação de novas Workflow Rules.
- Tipo de Named Credential usado pelo Event Relay.
- MuleSoft for Flow e Data Cloud: produto e metadata types.
- `@AuraEnabled(continuation=true)` em LWC.

Nada aqui foi conferido em página oficial nesta versão. Antes de usar como fonte formal, valide cada item em <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/>.
