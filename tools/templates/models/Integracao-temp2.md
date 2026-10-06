1. **Catálogo central de integrações**: uma visão resumida de todas.
2. **Documento detalhado por integração**: uma instância do template.
3. **Anexos reutilizáveis**: padrões de erro, segurança, monitoramento, limites e componentes.

A própria Salesforce recomenda padronizar nomes, estruturas, objetos relacionados e tratamento de erros em arquiteturas de integração. [architect.salesforce](https://architect.salesforce.com/docs/architect/decision-guides/guide/event-driven.html)

<!-- # 1. Estrutura do modelo único -->
# 1. Integração {tipo} - {feature relacionada}

## 1. Informações gerais

- Squad: {nomeSquad}
- Ativo relacionado: {nomeAtivo}

| Versão | Comentário | Fontes |
|--------|------------|--------|
| 1.0    | Criação doc | {lista de fontes} |

---

## 2. Visão negócio

### 2.1. Ciclo do negócio

<!-- Em que ponto do ciclo do negócio essa integração é necessária? -->
<!-- Quais são as etapas? -->
<!-- Qual problema de negócio resolvido pela integração? -->
<!-- Qual evento de negócio a inicia? -->
<!-- Qual resultado esperado? -->

### 2.2. Dados relacionados

<!-- Onde estão os dados que participam do inicio da integração? Onde são buscados outros dados relacionados? Quais são eles? Como são usados? -->

### 2.3. Dependências [se houver]

#### Pré integração


#### Pós integração

---

## 3. Classificação arquitetural

<!--
Esta seção deve ser padronizada para permitir filtros no catálogo.

```text
Direção: Inbound
Transporte: REST API
Interação: Síncrona
Processamento: Síncrono
Origem: ERP
Destino: Salesforce
Domínio: Field Service
Canal: Apex REST
Autenticação: OAuth 2.0 JWT Bearer
Contrato: JSON
Idempotência: External Event ID
```
-->

### 3.1. Fase Inbound

| Dimensão | Valor |
|---|---|
| Direção | Inbound |
| Tipo | API REST |
| Modalidade | Síncrona |
| Origem | ERP |
| Destino | Salesforce |
| Ponto de entrada | Apex REST |
| Processamento | Service Layer |
| Resposta | HTTP 200/201/400/409/500 |
| Autenticação | OAuth 2.0 JWT |
| Persistência | Objetos de negócio |
| Retry | Responsabilidade do consumidor |
| Observabilidade | Log Salesforce + correlation ID |


### 3.2. Fase Outbound

| Dimensão | Valor |
|---|---|
| Direção | Inbound |
| Tipo | API REST |
| Modalidade | Síncrona |
| Origem | ERP |
| Destino | Salesforce |
| Ponto de entrada | Apex REST |
| Processamento | Service Layer |
| Resposta | HTTP 200/201/400/409/500 |
| Autenticação | OAuth 2.0 JWT |
| Persistência | Objetos de negócio |
| Retry | Responsabilidade do consumidor |
| Observabilidade | Log Salesforce + correlation ID |

---

## 4. Ciclo  da integração

<!-- começa listando as fases do processo de integraçao considerando que acontecerão outras coisas além da chamada de integração em si -->

- Fase 01 {quem ou o que inicia}
- Fase 02
- Fase 03
- Fase 04
- Fase N

### 4.1. Fase 01 - resumo 30 caracteres

<!-- explicar o evento de negócio ou quem é o ator que inicia a integração e ação relacionada -->
<!-- listar os componentes dentro e fora salesforce relacionados / acionados no início -->
<!-- repetir isso para cada fase até passar por todas -->

---

## 5. Diagrama de contexto

<!-- Mostre apenas os sistemas e a direção do fluxo. -->

### 5.1. Exemplo | Fase Inbound
```text
┌──────────────┐
│     ERP      │
└──────┬───────┘
       │ HTTPS / OAuth 2.0
       │ POST /services/apexrest/integration/work-orders
       ▼
┌──────────────────────┐
│      Salesforce      │
│                      │
│  Apex REST           │
│  Service Layer       │
│  Work Order          │
└──────────────────────┘
```

Se existir middleware:

```text
ERP → API Gateway → Middleware → Salesforce
```

<!-- O diagrama de contexto não precisa mostrar classes internas. Ele serve para explicar o ecossistema. -->

### 5.2. Exemplo | Fase Outbound

<!-- seguir o padrão acima -->

---

## 6. Diagrama de sequência

<!--
O diagrama deve mostrar:

- Autenticação.
- Validação.
- Transformação.
- Consulta.
- DML.
- Publicação de evento, se houver.
- Resposta.
- Caminho de erro.
- Timeout.
- Retry, caso exista.
-->


### 6.1. Exemplo integração Inbound REST síncrona:

```text
ERP             Salesforce API       Apex REST       Service       Database
 |                   |                  |              |             |
 |-- POST ---------->|                  |              |             |
 |                   |-- autentica ---->|              |             |
 |                   |                  |-- valida --->|             |
 |                   |                  |              |-- DML ----->|
 |                   |                  |              |<------------|
 |                   |<-- response -----|              |             |
 |<-- HTTP 201 ------|                  |              |             |
```

### 6.2. Exemplo integração Outbound REST síncrona:

<!-- seguir mesmo padrão acima -->

---

## 7. Contrato da API

### 7.1. Endpoint

<!--
Documente:

- Método.
- URL por ambiente.
- Headers obrigatórios.
- Headers opcionais.
- Query parameters.
- Path parameters.
- Tamanho máximo.
- Timeout esperado.
- Limite de requisições.
- Versão.
-->
<!-- A URL base pode mudar no Named Credential ou no API Gateway, enquanto o path lógico permanece igual. -->

Exemplo:

```text
Método: POST
Path: /services/apexrest/v1/work-orders
Content-Type: application/json
Accept: application/json
```

| Ambiente | Endpoint |
|---|---|
| DEV | `/services/apexrest/v1/work-orders` |
| UAT | `/services/apexrest/v1/work-orders` |
| PRD | `/services/apexrest/v1/work-orders` |

---

### 7.2. Headers

```http
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
X-Correlation-Id: INT-20261004-000123
X-Idempotency-Key: ERP-WO-100234-UPDATE-1
X-API-Version: 1
```

Documente cada header:

| Header | Obrigatório | Descrição |
|---|---|---|
| `Authorization` | Sim | Token OAuth |
| `Content-Type` | Sim | Deve ser `application/json` |
| `X-Correlation-Id` | Sim | Rastreamento ponta a ponta |
| `X-Idempotency-Key` | Sim | Evita duplicidade |
| `X-API-Version` | Não | Versão do contrato |

---

### 7.3. Payload de request

<!-- preencha conforme o exemplo abaixo -->

Use uma tabela e um exemplo.

| Campo | Tipo | Obrigatório | Regra |
|---|---|---:|---|
| `eventId` | String | Sim | Único |
| `occurredAt` | DateTime | Sim | ISO 8601 |
| `workOrder.externalId` | String | Sim | Chave externa |
| `workOrder.status` | String | Sim | Valores permitidos |
| `workOrder.subject` | String | Não | Máximo 255 caracteres |
| `workOrder.customer.document` | String | Condicional | Obrigatório para pessoa física |

Exemplo:

```json
{
  "eventId": "evt-000123",
  "occurredAt": "2026-10-04T21:45:00Z",
  "workOrder": {
    "externalId": "WO-100234",
    "status": "OPEN",
    "subject": "Instalação de equipamento",
    "customer": {
      "externalId": "CUST-9001"
    }
  }
}
```

### 7.4. Autenticação e autorização

<!--
Documente:
- Mecanismo autenticação
- Nome da aplicação
- Nome do usuário de integração
- Nome do certificado
- Onde o certificado fica.
- Data de expiração. 
- Quem emite o token.
- Quem assina o JWT.
- Processo de renovação.
- Quem é responsável pela rotação.
- Como revogar o acesso.
- Como diferenciar ambientes.
- Quais IPs são permitidos, se aplicável.
- O que acontece quando o certificado expira.

Nunca coloque segredo, token ou senha no documento. Registre apenas uma referência segura, como:

```text
Secret reference: Vault/production/salesforce/erp-api
```
-->

Para o exemplo:

- Mecanismo: OAuth 2.0 JWT Bearer
- Aplicação: ECA_ERP_Integration
- Usuário: INT_ERP_USER
- Certificado: CERT_ERP_PRD
- Scopes:
  - api
  - refresh_token, se aplicável

### 7.5. Response de sucesso

```json
{
  "success": true,
  "correlationId": "INT-20261004-000123",
  "eventId": "evt-000123",
  "salesforceId": "0WO...",
  "externalId": "WO-100234",
  "status": "PROCESSED"
}
```
<!--
Documente:

- Status HTTP.
- Corpo.
- Campos.
- Significado de cada campo.
- Quando retornar 200 versus 201.
- Se há cabeçalho de localização.
- Se o processamento foi concluído ou apenas aceito.
-->

---

### 7.6. Response de erro

Padronize o formato:

```json
{
  "success": false,
  "correlationId": "INT-20261004-000123",
  "error": {
    "code": "INVALID_STATUS",
    "message": "The status COMPLETED requires completedAt.",
    "retryable": false,
    "details": [
      {
        "field": "workOrder.completedAt",
        "reason": "REQUIRED"
      }
    ]
  }
}
```

<!--
A resposta deve distinguir:

- Erro técnico.
- Erro de autenticação.
- Erro de autorização.
- Erro de validação.
- Erro de negócio.
- Erro temporário.
- Erro de duplicidade.
- Erro interno.
-->

---

## 8. Componentes internos do Salesforce

### 8.1. Componentes técnicos

Use uma tabela como esta:

| Componente | Nome | Tipo | Responsabilidade |
|---|---|---|---|
| Apex REST | `WorkOrderResource` | Apex Class | Receber requisição |
| DTO | `WorkOrderRequest` | Apex Class | Representar payload |
| Mapper | `WorkOrderMapper` | Apex Class | Converter payload |
| Service | `WorkOrderService` | Apex Class | Regra de negócio |
| Selector | `WorkOrderSelector` | Apex Class | Consultas |
| Handler | `WorkOrderIntegrationHandler` | Apex Class | Orquestração |
| CMDT | `IntegrationConfig__mdt` | Custom Metadata | Parâmetros |
| Usuário | `INT_ERP_USER` | Integration User | Execução |
| Permission Set | `PS_INT_ERP` | Permission Set | Acesso |
| Objeto | `WorkOrder` | Standard Object | Persistência |
| Log | `Integration_Log__c` | Custom Object | Auditoria |
| Evento | `WorkOrderReceived__e` | Platform Event | Processamento posterior |

<!--
É importante diferenciar:

- Componente que recebe.
- Componente que transforma.
- Componente que aplica regra.
- Componente que persiste.
- Componente que publica evento.
- Componente que registra log.
-->

---

### 8.2. Usuário e permissões


Integration User:
Profile:
License:
Permission Sets:
Permission Set Groups:
Objetos com CRUD:
Campos com FLS:
Acesso a Apex:
Acesso a eventos:
Restrições de IP:
Modo de compartilhamento:

<!--
A recomendação atual da Salesforce é utilizar um usuário de integração dedicado com licença de integração e uma External Client Application devidamente permissionada, em vez de compartilhar usuários ou usar credenciais genéricas. [architect.salesforce](https://architect.salesforce.com/docs/architect/decision-guides/guide/data-integration.html)

Não documente apenas:

> “Usa usuário de integração.”

Documente exatamente:

- Qual usuário.
- Qual licença.
- Qual Permission Set.
- Quais campos são acessíveis.
- O que ele não pode fazer.
-->

---

### 8.3. Regras de validação

<!--
Documente:

- Campos obrigatórios.
- Formatos.
- Tamanho.
- Valores permitidos.
- Dependência entre campos.
- Campos mutuamente exclusivos.
- Regras de negócio.
- Validação de referência externa.
- Validação de data.
- Tratamento de campos desconhecidos.
- Tratamento de campos nulos.
-->

Exemplo:

Se status = COMPLETED, completedAt é obrigatório.
Se customer.externalId não existir, a requisição deve ser rejeitada.
Se eventId já tiver sido processado, retornar o resultado original.

---

***

### 8.4. Persistência e regras Salesforce

#### 8.4.1. Mapeamento para objetos

| Campo externo | Objeto | Campo Salesforce | Operação |
|---|---|---|---|
| `workOrder.externalId` | WorkOrder | `External_Id__c` | Upsert |
| `workOrder.subject` | WorkOrder | `Subject` | Insert/update |
| `workOrder.status` | WorkOrder | `Status` | Transformação |
| `customer.externalId` | Account | `External_Id__c` | Consulta |
| `occurredAt` | Integration Log | `Occurred_At__c` | Insert |

<!--
Documente:

- Insert ou update.
- Upsert ou delete.
- External ID.
- Campos derivados.
- Lookup.
- Master-detail.
- Ordem de gravação.
- Transação única ou múltiplas transações.
- Possibilidade de lock.
- Automação disparada.
-->

---

#### 8.5. External ID e idempotência

Para esse exemplo:

```text
Chave primária externa:
workOrder.externalId

Chave de mensagem:
eventId

Chave de idempotência:
X-Idempotency-Key
```

Regra:

```text
Se eventId já estiver processado:
- não executar o DML novamente;
- retornar a resposta original;
- registrar ocorrência de duplicidade.
```

Ou:

```text
Se externalId existir:
- executar upsert;
- validar versão ou timestamp;
- rejeitar evento mais antigo.
```

Uma tentativa repetida deve produzir o mesmo estado final que uma única execução bem-sucedida. Esse é o objetivo prático da idempotência. [architect.salesforce](https://architect.salesforce.com/docs/architect/well-architected/guide/agentic-enterprise-resource-and-cost-optimization.html)

---

#### 8.6. Transação

Documente a sequência interna:

```text
1. Validar autenticação.
2. Validar headers.
3. Validar payload.
4. Verificar idempotência.
5. Consultar Account.
6. Fazer upsert de Work Order.
7. Gravar Integration Log.
8. Publicar evento posterior, se aplicável.
9. Retornar resposta.
```

Informe:

- Se todos os passos estão na mesma transação.
- Se há savepoint.
- Se existe rollback.
- Se há processamento posterior.
- Se eventos são publicados após commit.
- Se o log também sofre rollback.
- O que acontece se o DML principal funciona e o evento falha.

***

## 9. Limites e desempenho

### 9.1. Limites Salesforce

Inclua somente os limites relevantes, mas com valores e fonte:

```text
API diária:
Callouts por transação:
Timeout individual:
Tempo total de callout:
CPU:
SOQL:
DML:
Heap:
Payload:
Platform Events:
Concurrent Requests:
```

Não recomendo copiar todos os governor limits para todos os documentos. Isso deixa o documento pesado e difícil de manter. Melhor ter:

- Uma seção resumida específica.
- Um link para o padrão corporativo de limites.
- Uma data de validação.

### 9.2. Limites da API

```text
Rate limit: 100 requisições por segundo
Payload máximo: 1 MB
Timeout do consumidor: 30 segundos
Concorrência máxima: 20 requisições
```

### 9.3. SLA e desempenho

```text
SLA funcional: resposta em até 3 segundos
P95 esperado: até 1,5 segundo
P99 esperado: até 3 segundos
Disponibilidade: 99,9%
Volume normal: 500 requisições/hora
Pico: 3.000 requisições/hora
```

A Salesforce recomenda adequar timeouts ao tipo de operação; como referência arquitetural, chamadas user-facing costumam exigir timeouts menores que processos assíncronos. [architect.salesforce](https://architect.salesforce.com/docs/architect/well-architected/guide/reliability.html)

---

## 10. Falhas, retry e contingência

### 10.1. Matriz de erro

| HTTP | Código | Significado | Retry | Ação |
|---:|---|---|---|---|
| 400 | `INVALID_PAYLOAD` | JSON inválido | Não | Corrigir origem |
| 401 | `INVALID_TOKEN` | Token inválido | Condicional | Renovar token |
| 403 | `NOT_AUTHORIZED` | Sem permissão | Não | Corrigir acesso |
| 404 | `CUSTOMER_NOT_FOUND` | Referência inexistente | Não | Corrigir cadastro |
| 409 | `DUPLICATE_EVENT` | Evento repetido | Não | Retornar resultado anterior |
| 429 | `RATE_LIMIT` | Limite excedido | Sim | Backoff |
| 500 | `INTERNAL_ERROR` | Falha Salesforce | Sim | Retry limitado |
| 503 | `TEMPORARY_UNAVAILABLE` | Serviço indisponível | Sim | Retry limitado |
| 504 | `TIMEOUT` | Timeout | Sim, com cautela | Consultar status antes |

### 10.2. Responsabilidade pelo retry

Defina explicitamente:

```text
Retry primário: sistema chamador
Retry secundário: middleware
Retry interno Salesforce: não aplicável
Dead-letter: middleware
Reprocessamento manual: time de Operações
```

Não deixe duas camadas fazendo retry agressivo sem coordenação. Isso pode gerar uma multiplicação de chamadas:

```text
3 tentativas no middleware × 3 tentativas no consumidor = 9 chamadas
```

### 10.3. Contingência

Para a API Inbound:

```text
Se Salesforce estiver indisponível:
1. O ERP armazena a mensagem.
2. O ERP tenta novamente conforme backoff.
3. Após N tentativas, envia para DLQ.
4. O suporte recebe alerta.
5. Após normalização, a mensagem é reprocessada.
```

Para falha depois que Salesforce recebe a requisição:

```text
1. A mensagem é gravada em staging.
2. A API retorna 202.
3. O processador interno tenta novamente.
4. Após N falhas, status = FAILED.
5. O registro fica disponível para reprocessamento.
```

A Salesforce recomenda projetar sistemas que detectem falhas, limitem o impacto e recuperem o serviço automaticamente, incluindo retry controlado, circuit breaker e processamento assíncrono quando apropriado. [architect.salesforce](https://architect.salesforce.com/docs/architect/well-architected/guide/reliability.html)

---

## 11. Segurança e conformidade

### 11.1. Segurança

Documente:

- TLS mínimo.
- OAuth flow.
- ECA ou Connected App.
- Usuário de integração.
- Scopes.
- Certificado.
- mTLS.
- IP allowlist.
- API Gateway.
- WAF.
- Criptografia.
- Segregação entre ambientes.
- Rotação de segredo.
- Revogação de acesso.

### 11.2. LGPD e dados sensíveis

```text
Dados pessoais tratados:
- Nome
- Documento
- Endereço
- Telefone

Finalidade:
Execução de serviço de campo.

Retenção:
Payload bruto: 30 dias.
Log técnico: 180 dias.
Dados de negócio: conforme política corporativa.

Mascaramento:
Documento parcialmente mascarado em logs.
```

---

## 12. Monitoramento e suporte

### 12.1. Correlation ID

Defina:

```text
Origem: ERP
Formato: UUID
Obrigatório: Sim
Propagação: Header e payload
Persistência: Integration_Log__c
```

### 12.2. Log Salesforce

```text
Integration_Log__c
- Correlation_Id__c
- Event_Id__c
- Direction__c
- Endpoint__c
- Status__c
- Http_Status__c
- Error_Code__c
- Retry_Count__c
- Received_At__c
- Completed_At__c
- Payload_Hash__c
```

Não é necessário salvar o payload completo se ele contiver dados sensíveis. Pode-se guardar:

- Hash.
- Identificador externo.
- Resumo.
- Campos de diagnóstico.
- Referência a armazenamento seguro.

### 12.3. Alertas

Documente:

| Alerta | Condição | Destino | Severidade |
|---|---|---|---|
| Alta taxa de erro | > 5% em 10 min | Suporte | Alta |
| Timeout | 10 ocorrências em 5 min | Integração | Alta |
| Mensagem pendente | > 15 min | Operação | Média |
| Certificado próximo do vencimento | 30 dias | Segurança | Alta |
| DLQ com mensagens | Qualquer ocorrência | Integração | Alta |

Não alerte por qualquer erro isolado. O ideal é alertar por padrões, duração, volume e impacto. [architect.salesforce](https://architect.salesforce.com/docs/architect/well-architected/guide/reliability.html)

***

## 13. Ambientes, implantação e operação

### 13.1. Configuração por ambiente

| Item | DEV | UAT | PRD |
|---|---|---|---|
| Endpoint | URL Dev | URL UAT | URL Prod |
| ECA | ECA Dev | ECA UAT | ECA Prod |
| Usuário | `INT_DEV` | `INT_UAT` | `INT_PRD` |
| Certificado | Cert Dev | Cert UAT | Cert Prod |
| Named Credential | `NC_ERP_DEV` | `NC_ERP_UAT` | `NC_ERP_PRD` |
| CMDT | Config Dev | Config UAT | Config Prod |

### 13.2. Ordem de implantação

Exemplo:

```text
1. Custom Objects
2. Custom Fields
3. Custom Metadata Types
4. Permission Sets
5. Apex Classes
6. Flows
7. Platform Events
8. Named Credentials
9. External Credentials
10. Certificados
11. Configuração do middleware
12. Jobs
13. Smoke test
```

Se algum item não puder ser implantado via metadata, marque como:

```text
Configuração manual obrigatória
Responsável:
Evidência:
Data:
```

---

## 14. Reprocessamento e reconciliação

### 14.1. Reprocessamento

Documente:

```text
Quem pode reprocessar:
Onde localizar:
Critérios para reprocessar:
Quantidade máxima:
Como evitar duplicidade:
Como confirmar resultado:
O que fazer se falhar novamente:
```

Exemplo:

```text
O analista pode reprocessar registros com status FAILED.
O reprocessamento é permitido até 3 vezes.
Mensagens com INVALID_PAYLOAD não devem ser reprocessadas sem correção.
Mensagens TIMEOUT devem consultar o ERP antes de serem reenviadas.
```

### 14.2. Reconciliação

```text
Diária às 02:00:
- Comparar Work Orders recebidas no ERP.
- Comparar Work Orders criadas no Salesforce.
- Identificar divergências.
- Gerar relatório.
- Criar incidente quando a divergência exceder 1%.
```

---

<!--
# 11. Como transformar isso em um template reutilizável

O modelo deve ter campos obrigatórios e blocos condicionais.

## Campos sempre obrigatórios

- Identificação.
- Objetivo.
- Escopo.
- Sistemas.
- Classificação.
- Diagrama.
- Segurança.
- Contrato.
- Limites.
- Falhas.
- Monitoramento.
- Suporte.
- Ambientes.
- Histórico.

## Blocos condicionais

| Bloco | Quando aparece |
|---|---|
| OAuth inbound | Sistema externo acessa Salesforce |
| Named Credential | Salesforce acessa sistema externo |
| Payload de evento | Platform Event ou CDC |
| Queueable | Processamento assíncrono |
| Batch | Alto volume |
| Staging | Aceite sem processamento imediato |
| DLQ | Existe mensageria |
| Callback | Sistema externo recebe resultado posterior |
| Continuation | UI espera resposta longa |
| Bulk API | Carga volumosa |
| Event Relay | Salesforce publica para EventBridge |
| OmniStudio | Industries participa do fluxo |
| Field Service | Work Order, Service Appointment, Asset etc. |
| LGPD | Dados pessoais ou sensíveis |
| Reconciliação | Integração crítica ou eventual |

***

# 12. Exemplo compacto preenchido

## Identificação

```text
Código: INT-IN-REST-FS-001
Nome: Recebimento de Work Order do ERP
Direção: Inbound
Tipo: API REST
Modalidade: Síncrona
Criticidade: Alta
```

## Fluxo

```text
ERP
 → API Gateway
 → Salesforce Apex REST
 → WorkOrderService
 → Account/WorkOrder
 → Integration_Log__c
 → HTTP response
```

## Segurança

```text
External Client App:
ECA_ERP_Integration

Usuário:
INT_ERP_PRD

Autenticação:
OAuth 2.0 JWT Bearer

Certificado:
CERT_ERP_PRD
```

## Endpoint

```text
POST /services/apexrest/v1/work-orders
```

## Idempotência

```text
Chave:
eventId

Regra:
eventId já processado retorna a resposta original sem novo DML.
```

## Limites

```text
Payload máximo: 1 MB
Timeout do chamador: 10 segundos
Volume esperado: 500 chamadas/hora
Pico: 3.000 chamadas/hora
```

## Falhas

```text
400: não repetir.
401: renovar token e tentar uma vez.
429: retry com backoff.
500/503/504: retry até 3 vezes.
Após falhas: mensagem fica na DLQ do ERP.
```

## Contingência

```text
Se Salesforce estiver indisponível, o ERP mantém a mensagem em fila.
Se o ERP receber timeout, consulta pelo eventId antes de reenviar.
```

## Observabilidade

```text
Correlation ID obrigatório.
Logs no Salesforce e no middleware.
Alerta para erro > 5% em 10 minutos.
Reconciliação diária.
```

***

## Recomendação final

Sim, crie um **modelo único**, mas não um documento único e inflexível. O melhor formato é:

```text
Template corporativo único
        +
seções obrigatórias
        +
seções condicionais
        +
anexos por padrão técnico
```

Para o seu caso, o template de **Inbound API REST síncrono** deve ter, no mínimo:

1. Identificação e classificação.
2. Contexto e sequência.
3. Sistemas e componentes.
4. ECA/Connected App.
5. Usuário e permissões.
6. Endpoint e headers.
7. Payload e resposta.
8. Mapeamento de campos.
9. Regras de validação.
10. Idempotência.
11. Transação e rollback.
12. Limites e SLA.
13. Erros e retry.
14. Contingência.
15. Logs e monitoramento.
16. Segurança e LGPD.
17. Ambientes e deploy.
18. Reprocessamento.
19. Reconciliação.
20. Responsáveis e histórico.

Esse mesmo modelo pode ser reaproveitado para outbound, assíncrono, Platform Events, Batch, OmniStudio e Field Service, alterando apenas os blocos técnicos específicos.
-->
