# Matriz de diagnóstico

> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta.

Do sinal encontrado no projeto para os desenhos candidatos. Use junto com [guia_evidencias.md](guia_evidencias.md) (códigos `Cnn`) e [regras_ligacao.md](regras_ligacao.md) (códigos `Lnn`).

**Confiança** (critério desta base, não da Salesforce): **alta** = evidência direta e documentada; **média** = combinação de sinais ou heurística; **baixa** = presumido.
Nunca promova um candidato a fato sem a evidência da coluna "O que confirmar".

## 1. Sinais

| ID | Sinal no projeto | Evidência | Direção · mecanismo | Desenhos candidatos | Confiança | O que confirmar |
|---|---|---|---|---|---|---|
| S01 | Classe com `@RestResource` | C11 | IN · REST (Apex REST) | g.3; H.3 se a classe só enfileira (C07/C18); M.3 | alta | quem chama: app de entrada (Connected App/ECA) ou Site (S31) |
| S02 | Classe `global` com métodos `webservice` | C12 | IN · SOAP (Apex SOAP) | g.4 | alta | app de entrada |
| S03 | Campo `externalId`=true sem Apex REST/SOAP que grave o objeto | MA-CF | INBOUND_PRESUMIDO · API padrão | g.1, g.2, H.1, M.3, M.4 | baixa | documentação do sistema externo ou logs de API (fora do repositório) |
| S04 | Connected App ou External Client App | MA-CA, MA-ECA | IN (cliente externo) ou UI/SSO | g.*, H.*, M.2–M.5; N.2 se `canvasConfig`/`.ecaCanvas`; N.3 se SAML | média | o que o app habilita: OAuth, Canvas ou SAML |
| S05 | App com Client Credentials (`isClientCredentialEnabled` / `isClientCredentialsFlowEnabled`) | MA-CA, MA-ECAG | IN · máquina a máquina | g.*, H.*, M.3–M.5 | alta | qual API o cliente usa (não aparece no XML) |
| S06 | `callout:` ou `HttpRequest` em classe chamada por `@AuraEnabled` | C01/C02 + L45 | OUT · SYNC (UI) | b.1, b.2 (E1–E6 pela fonte do endpoint) | alta | fonte do endpoint (guia, seção 4) |
| S07 | Callout em classe chamada por `@future(callout=true)` ou Queueable a partir de trigger | C06/C07 + L16/L40 | OUT · ASYNC | D.1; M.1 se o host for de middleware | alta | fonte do endpoint e se há writeback no registro |
| S08 | Callout direto no contexto do trigger (sem async) | C02 + L16 | anti-padrão | nenhum: callout precisa ser assíncrono em trigger [AX-TRG] | alta | pode ser código morto ou caminho que falha em execução |
| S09 | Flow com `actionType`=externalService + ESR `SchemaInferred` | L10 + MA-ESR | OUT · HTTP Callout declarativo | b.3 (Screen Flow), D.2 (`pathType`=AsyncAfterCommit), F.3 (`triggerType`=Scheduled) | alta | tipo de Flow pelo `start` |
| S10 | ESR com `registrationProviderType` MuleSoft ou Anypoint | MA-ESR | OUT · MuleSoft | M.7 | alta | quem chama (Flow L10 ou Apex L41) |
| S11 | ESR com outro provedor (Standard/Custom) chamado por Flow ou `ExternalService.` | L10/L41 | OUT · External Service | b.4; D.2/F.3 conforme o Flow | alta | Named Credential do ESR (L09) |
| S12 | `WebServiceCallout.invoke` / `endpoint_x` | C15 | OUT · SOAP | b.5; D.1/F.1 se chamado de async | alta | valor de `endpoint_x` (L42) |
| S13 | `new Continuation(` / `@AuraEnabled(continuation=true)` | C17 | OUT · SYNC longo | b.6 | alta | — |
| S14 | Integration Procedure / FlexCard / OmniScript com HTTP Action | não confirmado | OUT · OmniStudio | c.1, c.2, M.6 | média | formato dos arquivos OmniStudio no projeto (não confirmado) |
| S15 | CspTrustedSite com `isApplicableToConnectSrc` + LWC com `fetch(` | MA-CSP | OUT · navegador | d.1 | média | o LWC chama esse host? (`fetch` = padrão JS, nv) |
| S16 | CspTrustedSite com `isApplicableToFrameSrc` + LWC com `<iframe>` | MA-CSP | UI | N.2 (iframe) | média | — |
| S17 | ExternalDataSource + objeto `__x` | L22/L23/L24 | OUT · virtualização | e.1 (`type` OData/OData4/SfdcOrg), e.2 (`type`=ApexClassId), N.1 (SfdcOrg) | alta | — |
| S18 | QuickAction `type` Flow/LightningWebComponent cujo destino faz callout | L25 + S06/S09 | OUT · SYNC sob demanda | f.1 | alta | — |
| S19 | Publicação de `X__e` (C18 ou `recordCreates`) | C18/L13 | EVENTO · publica | D.3 se houver assinante no projeto (C19/L12); senão E.1 (externo assina) | média | assinantes externos não aparecem no projeto |
| S20 | Trigger ou Flow assinando `X__e` sem publicador no projeto | C19/L12 | EVENTO · IN | H.2 | média | publicador externo (fora do repositório) |
| S21 | `PlatformEventChannelMember` em ChangeEvents | L18 | EVENTO · CDC | E.2 (externo, ou M.2); E.2 interno se houver trigger em `XChangeEvent` (C21) | média | assinante externo não aparece |
| S22 | Canal customizado com `enrichedFields`/`filterExpression` | L18 | EVENTO · canal | E.3; E.4 se houver EventRelayConfig | alta | — |
| S23 | `EventRelayConfig` | L19 | EVENTO · AWS | E.4 | alta | — |
| S24 | `ManagedEventSubscription` | L20 | EVENTO · assinante Pub/Sub | E.1, E.2, M.2 | alta | — |
| S25 | Workflow com `outboundMessages` | L28 | OUT · SOAP (Outbound Message) | D.4 | alta | regra ativa que dispara |
| S26 | Schedulable que dispara Batch/Queueable com `AllowsCallouts` | C08/C09/C07 + L40 | OUT/IN · lote | F.1 (Batch), F.2 (Queueable encadeado) | alta | agendamento real (não está no repositório) |
| S27 | Flow `triggerType`=Scheduled com ação de callout | MA-FLOW | OUT · lote declarativo | F.3 | média | suporte a callout em Flow agendado (não confirmado) |
| S28 | Objeto `__c` com campos de status/tentativas/payload + processador async | heurística | OUT · fila | G.1 | média | — |
| S29 | `EmailServicesFunction` | L21 | IN · e-mail | H.4 | alta | — |
| S30 | Trigger/Flow em ContentVersion + app de entrada | heurística | IN · arquivos | H.5 | baixa | origem dos arquivos |
| S31 | CustomSite cujo `guestProfile` libera classe Apex REST | L34 | IN · webhook público | g.6 | alta | validação de assinatura no código |
| S32 | Campo de controle (ex.: status "enviado") atualizado só por fora | heurística | IN · polling | M.5 | baixa | não detectável só pelo projeto |
| S33 | Named Credential apontando para outra org Salesforce | MA-NC | OUT · org↔org | N.1, F.4 | média | host da outra org |
| S34 | `AuthProvider` com `registrationHandler` ou `SamlSsoConfig` | L32 / MA-SAML | SSO | N.3 | alta | — |
| S35 | WebLink `linkType`=url ou CustomTab com `url` para host externo | L26/L27 | UI | N.2 | alta | — |
| S36 | Host de Named Credential/Remote Site com padrão de middleware (ex.: domínio do MuleSoft) | heurística | MID | M.1 | média | confirmar com o time qual host é middleware |
| S37 | Só `HttpCalloutMock`/`WebServiceMock` (classe de teste) | C23 | descartar | nenhum | alta | — |
| S38 | Remote Site ou Named Credential sem referência no projeto | L01/L08 | lacuna | qualquer OUT (E4/E5: nome/URL vindo de configuração) | baixa | procurar valores em Custom Metadata, Labels e Settings (L36) |

## 2. Assinatura mínima por desenho

Metadata types obrigatórios em **todas** as variantes do desenho (atores excluídos). Se algum faltar no projeto, o desenho fica improvável; o que varia entre variantes está nos arquivos de cada seção.

| Desenho | Título | Assinatura mínima | Variantes |
|---|---|---|---|
| b.1 | LWC / Screen Flow → cadeia de classes → callout | `ApexClass`, `PermissionSet` | 12 |
| b.2 | LWC / Screen Flow → uma classe que faz o callout | `ApexClass`, `PermissionSet` | 12 |
| b.3 | Screen Flow → ação HTTP Callout (declarativa) | `ExternalServiceRegistration`, `Flow`, `NamedCredential`, `PermissionSet` | 2 |
| b.4 | Flow ou Apex → External Service (OpenAPI) | `ExternalServiceRegistration`, `NamedCredential` | 4 |
| b.5 | LWC / Screen Flow → stub SOAP gerado (WSDL2Apex) | `ApexClass`, `PermissionSet` | 12 |
| b.6 | LWC → Apex Continuation | `ApexClass`, `LightningComponentBundle` | 6 |
| c.1 | FlexCard → Integration Procedure → HTTP Action | `OmniIntegrationProcedure`, `OmniUiCard` | 6 |
| c.2 | OmniScript → Integration Procedure ou Remote Action | `OmniScript` | 9 |
| d.1 | LWC → fetch direto do navegador | `CspTrustedSite`, `LightningComponentBundle` | 3 |
| e.1 | Salesforce Connect (OData / cross-org) | `CustomField`, `CustomObject (__x)`, `ExternalDataSource`, `Layout, FlexiPage ou CustomTab`, `PermissionSet` | 2 |
| e.2 | Salesforce Connect com adaptador Apex | `ApexClass`, `CustomField`, `CustomObject (__x)`, `ExternalDataSource`, `Layout, FlexiPage ou CustomTab`, `PermissionSet` | 6 |
| f.1 | Quick Action → Flow ou LWC → callout → atualiza o registro | `ApexClass`, `CustomObject + CustomField`, `Layout ou FlexiPage`, `PermissionSet`, `QuickAction` | 12 |
| g.1 | Sistema externo → REST/SOAP API padrão (CRUD) | `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| g.2 | Sistema externo → Composite / sObject Tree / Collections | `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| g.3 | Sistema externo → Apex REST customizado | `ApexClass`, `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| g.4 | Sistema externo → Apex SOAP customizado | `ApexClass`, `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| g.5 | Sistema externo → Flow via REST (Actions) | `CustomField`, `CustomObject (padrão ou __c)`, `Flow`, `PermissionSet`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| g.6 | Webhook público → Site → Apex REST | `ApexClass`, `CustomField`, `CustomObject (padrão ou __c)`, `Profile` | 6 |
| g.7 | Sistema externo → GraphQL API | `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| D.1 | Trigger Apex → @future ou Queueable → callout | `ApexClass`, `ApexTrigger`, `CustomObject + CustomField` | 12 |
| D.2 | Flow record-triggered → caminho assíncrono → callout | `CustomObject + CustomField`, `Flow` | 10 |
| D.3 | Trigger/Flow publica Platform Event → assinante faz o callout | `CustomField`, `CustomObject (__e)`, `CustomObject + CustomField` | 16 |
| D.4 | Outbound Message (SOAP com retry) | `CustomObject + CustomField`, `Workflow (WorkflowOutboundMessage)` | 4 |
| E.1 | Platform Event publicado → sistema externo assina | `Certificate`, `CustomField`, `CustomObject (__e)`, `PermissionSet`, `PermissionSet / PermissionSetGroup`, `Profile` | 6 |
| E.2 | Change Data Capture | `CustomObject`, `PlatformEventChannelMember` | 8 |
| E.3 | Canal customizado com enriquecimento e filtro | `Certificate`, `PermissionSet`, `PermissionSet / PermissionSetGroup`, `PlatformEventChannel`, `PlatformEventChannelMember`, `Profile` | 4 |
| E.4 | Event Relay → Amazon EventBridge | `EventRelayConfig`, `NamedCredential`, `PlatformEventChannel`, `PlatformEventChannelMember` | 2 |
| F.1 | Schedulable → Batch Apex com callout | `ApexClass`, `CustomObject + CustomField (External ID)` | 12 |
| F.2 | Schedulable → Queueable encadeado (paginação) | `ApexClass`, `CustomObject + CustomField (External ID)` | 12 |
| F.3 | Flow agendado → callout | `Flow (Schedule-Triggered)` | 10 |
| F.4 | Apex → Bulk API 2.0 de outra org | `ApexClass`, `ConnectedApp ou ExternalClientApplication`, `NamedCredential` | 6 |
| G.1 | Fila de integração em objeto (staging) + processador | `ApexClass`, `ApexTrigger`, `CustomObject (__c) + CustomField`, `CustomObject + CustomField` | 12 |
| H.1 | Sistema externo → Bulk API 2.0 | `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet / PermissionSetGroup`, `Profile` | 12 |
| H.2 | Sistema externo publica Platform Event → assinante na org | `CustomField`, `CustomObject (__e)`, `CustomObject (padrão ou __c)`, `PermissionSet`, `PermissionSet / PermissionSetGroup`, `Profile` | 16 |
| H.3 | Apex REST que recebe e enfileira | `ApexClass`, `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| H.4 | E-mail inbound (Email Service) | `ApexClass`, `CustomField`, `CustomObject (padrão ou __c)`, `EmailServicesFunction` | 2 |
| H.5 | Arquivos via ContentVersion | `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| M.1 | Org → middleware (síncrono ou via Apex assíncrono) | `ApexClass` | 24 |
| M.2 | Middleware assina Platform Event / CDC | `Certificate`, `PermissionSet`, `PermissionSet / PermissionSetGroup`, `Profile` | 4 |
| M.3 | Middleware → org (REST padrão ou Apex REST) | `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| M.4 | Middleware → org (Bulk API 2.0) | `CustomField`, `CustomObject (padrão ou __c)`, `PermissionSet / PermissionSetGroup`, `Profile` | 4 |
| M.5 | Middleware faz polling na org | `CustomObject + CustomField`, `PermissionSet / PermissionSetGroup`, `Profile` | 8 |
| M.6 | Integration Procedure como middleware dentro da org | `OmniDataTransform`, `OmniIntegrationProcedure` | 12 |
| M.7 | API MuleSoft registrada como External Service → Flow ou Apex | `ExternalServiceRegistration`, `NamedCredential` | 8 |
| N.1 | Org ↔ org | — | 4 |
| N.2 | Integração de UI | — | 6 |
| N.3 | Identidade (SSO) | — | 3 |
| N.4 | Data Cloud | — | 1 |

## 3. Como usar

1. Liste os sinais encontrados (seção 1) com a evidência `arquivo:linha`.
2. Para cada candidato, confira a assinatura mínima (seção 2).
3. Escolha a variante comparando a tabela da variante com os componentes achados (coluna "Como achar no projeto").
4. Registre a confiança e o que ficou sem confirmação, usando [limites_da_fonte.md](limites_da_fonte.md) para o que o repositório não pode mostrar.
