# Prompt — EmbeddedServiceFlowConfig

## 1. Contexto do componente

### 1.1 O que é
`EmbeddedServiceFlowConfig` (nome funcional: **Embedded Service Flow Config** ou **Configuração de Flow de Serviço Incorporado**) é um metadata type do Salesforce que vincula um Screen Flow a uma configuração de Embedded Service (ex.: chat web, Einstein Bot, canal de mensagens). Ele define como e quando um Flow de pré-atendimento será apresentado ao usuário final dentro de um canal digital.

Na prática, `EmbeddedServiceFlowConfig`:
- referencia um Flow que será executado no contexto de um Embedded Service;
- pode coletar informações do cliente antes de iniciar um chat/case;
- está associado a `EmbeddedServiceConfig` e pode direcionar para `Case`, `Contact`, `Lead` etc.;
- é parte da experiência de Service Cloud digital (web chat, messaging).

### 1.2 Para que serve
- Coletar dados do cliente antes do atendimento.
- Rotearencaminhar interações com base nas respostas.
- Criar registros (case, lead, contact) automaticamente a partir do Flow.
- Personalizar a experiência de pré-atendimento em canais digitais.

### 1.3 Cenários típicos de uso
- Formulário de pré-chat com perguntas personalizadas.
- Coleta de dados pessoais/sensíveis com consentimento.
- Roteamento de chat por produto/idioma/região.
- Criação automática de caso a partir de respostas do cliente.

### 1.4 Clouds / contextos
- **Service Cloud** — principal contexto de uso.
- **Experience Cloud** — possível integração com portais de suporte.
- **Einstein Bots / Messaging** — canais que podem invocar flows de pré-atendimento.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `EmbeddedServiceFlowConfig`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Embedded Service Flow Configuration |
| Metadata type exact | `EmbeddedServiceFlowConfig` |
| Pasta no projeto SFDX | `embeddedServiceFlowConfigs/` |
| Arquivo padrão | `<apiName>.embeddedServiceFlowConfig-meta.xml` |
| Objeto interno (API padrão) | Verificar disponibilidade na org |
| Objeto interno (Tooling API) | `EmbeddedServiceFlowConfig` (quando disponível) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Parcial — validar na org |
| Acessível por Tooling API | Parcial — validar na org |
| Acessível por Apex | Limitado |
| Acessível por UI | Sim — **Setup → Embedded Service Deployments** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Embedded Service Config | `EmbeddedServiceConfig` | Configuração pai do canal digital. |
| Flow | `Flow` (Screen Flow) | Fluxo executado no pré-atendimento. |
| Case / Contact / Lead | `Case`, `Contact`, `Lead` | Objetos manipulados pelo Flow. |
| Einstein Bot | `Bot`, `BotVersion` | Pode invocar flows relacionados. |
| Messaging Channel | `MessagingChannel`, `MessagingChannelUsage` | Canal que utiliza o serviço. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`EmbeddedServiceFlowConfig`)

Arquivo típico: `embeddedServiceFlowConfigs/<API_Name>.embeddedServiceFlowConfig-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<embeddedServiceConfig>` | 1 | API Name do `EmbeddedServiceConfig` pai. |
| `<flow>` | 1 | API Name do Flow vinculado. |
| `<isEnabled>` | 0..1 | Se a configuração está habilitada. |
| `<masterLabel>` / `<label>` | 1 | Nome amigável. |
| `<objectForPrefill>` | 0..1 | Objeto usado para pré-preenchimento. |
| `<routingType>` | 0..1 | Tipo de roteamento (botão, fila, agente etc.). |
| `<shouldCreateCase>` | 0..1 | Se deve criar caso ao final. |
| `<shouldCreateLead>` | 0..1 | Se deve criar lead ao final. |
| `<shouldCreateContact>` | 0..1 | Se deve criar contato ao final. |
| `<shouldCreateAccount>` | 0..1 | Se deve criar conta ao final. |
| `<shouldCreateOpportunity>` | 0..1 | Se deve criar oportunidade ao final. |
| `<shouldCreateTask>` | 0..1 | Se deve criar tarefa ao final. |
| `<shouldSaveToTranscript>` | 0..1 | Se deve salvar respostas no transcript. |

> **Atenção**: os nomes exatos das tags podem variar conforme release e evolução do produto. Validar com retrieve real.

### 3.2 Configuração observável em outras fontes

- UI de **Setup → Embedded Service Deployments**.
- Detalhes do Snap-ins/Embedded Service no Experience Builder.
- `SetupAuditTrail`.

---

## 4. Consultas e formas de extração

- Via Metadata API retrieve na pasta `embeddedServiceFlowConfigs/`.
- Tooling API: `SELECT Id, FullName, DeveloperName, Metadata FROM EmbeddedServiceFlowConfig` (se disponível).
- UI para validação de vinculação com Embedded Service.

---

## 5. Boas práticas e pontos de atenção

- Validar fluxo vinculado antes de publicar Embedded Service.
- Proteger dados pessoais coletados (LGPR/GDPR).
- Obter consentimento quando necessário.
- Garantir que o Screen Flow seja compatível com o canal (web vs mobile).
- Testar roteamento e criação de registros em sandbox.
- Diferenciar configuração publicada de sessão efetivamente iniciada.
- Rastrear alterações no `SetupAuditTrail`.

---

## 6. Links de referência oficial

- [Salesforce Help — Set Up Embedded Service Deployments](https://help.salesforce.com/s/articleView?id=sf.embedded_service_setup.htm)
- [Salesforce Help — Add a Pre-Chat Form to Embedded Chat](https://help.salesforce.com/s/articleView?id=sf.live_agent_prechat_form.htm)
- [Salesforce Developer — EmbeddedServiceFlowConfig Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_embeddedserviceflowconfig.htm)
