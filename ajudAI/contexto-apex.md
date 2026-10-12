Abaixo está o detalhamento individualizado dos **4 tipos de processamento assíncrono Apex da Onda 01**. Cada tipo conta agora com seu **modelo de documentação em Markdown** (incluindo convenção de nomes, assinatura técnica, interfaces, limites e formas de invocação) e seu **JSON Schema exclusivo** para automação e extração via utilitários ou **Claude Code**.

---

# 📑 Modelo 1.1: Batch Apex (`Database.Batchable`)

O **Batch Apex** é utilizado para processar grandes volumes de dados (até 50 milhões de registros) em segundo plano, dividindo a massa total em pequenos lotes (*chunks*).

### Convenção de Nomes e Estrutura SFDX
* **Nome da Classe:** `[NomeDoDominio][Acao]Batch.cls` (ex: `OrderCleanupBatch.cls`, `InvoiceSyncBatch.cls`)
* **Pasta no Repositório:** `force-app/main/default/classes/`
* **Arquivos Relacionados:** `OrderCleanupBatch.cls` e `OrderCleanupBatch.cls-meta.xml`

---

## 1. Identificação e Metadados do Batch

| Propriedade | Valor Exemplo | Tag / Fonte | Descrição Técnica |
|---|---|---|---|
| **ClassName / ApiName** | `OrderCleanupBatch` | Arquivo `.cls` | Nome exclusivo da classe Apex. |
| **ApiVersion** | `62.0` | `.cls-meta.xml` (`<apiVersion>`) | Versão da API Salesforce utilizada. |
| **Status** | `Active` | `.cls-meta.xml` (`<status>`) | Status de publicação (`Active` / `Deleted`). |
| **Tamanho do Lote Padrão** | `200` (Faixa: 1 a 2000) | Invocação `Database.executeBatch` | Quantidade de registros processados por transação Apex individual. |
| **Tipo de Escopo** | `Database.QueryLocator` \| `Iterable<sObject>` | Retorno do método `start()` | `QueryLocator`: até 50M registros. `Iterable`: coleções customizadas em memória. |

---

## 2. Assinatura da Classe e Interfaces Suportadas

```apex
public class OrderCleanupBatch implements Database.Batchable<sObject>, Database.Stateful, Database.AllowsCallouts { ... }
```

| Interface | Obrigatoriedade | Finalidade Técnica |
|---|---|---|
| **`Database.Batchable<sObject>`** | **Obrigatória** | Define a classe como um Batch e exige a implementação dos métodos `start`, `execute` e `finish`. |
| **`Database.Stateful`** | Opcional | Mantém o estado das variáveis de instância entre as execuções de cada lote (ex: contadores globais de sucesso/erro). |
| **`Database.AllowsCallouts`** | Opcional | Permite realizar chamadas HTTP/REST/SOAP externas dentro do método `execute()`. |
| **`Database.RaisesPlatformEvents`** | Opcional | Dispara eventos do sistema (`BatchApexErrorEvent`) automaticamente em caso de falha não tratada. |

---

## 3. Métodos Obrigatórios do Ciclo de Vida (`Batchable`)

| Método | Assinatura Técnica | Descrição / Responsabilidade |
|---|---|---|
| **`start`** | `public Database.QueryLocator start(Database.BatchableContext BC)` | Executa a consulta SOQL inicial. É rodado em uma única transação síncrona. |
| **`execute`** | `public void execute(Database.BatchableContext BC, List<sObject> scope)` | Processa cada lote (*scope*). Executado de forma assíncrona para cada grupo de registros. |
| **`finish`** | `public void finish(Database.BatchableContext BC)` | Pós-processamento rodado após a conclusão de TODOS os lotes (envio de e-mails, logs ou encadeamento). |

---

## 4. Invocação, Limites de Governança e Monitoramento

### 4.1. Exemplo de Invocação Apex
```apex
OrderCleanupBatch batchInstance = new OrderCleanupBatch();
// Invocação com tamanho de lote customizado de 100 registros
Id jobId = Database.executeBatch(batchInstance, 100);
```

### 4.2. Monitoramento de Execução (`AsyncApexJob`)
```sql
SELECT Id, Status, NumberOfErrors, JobItemsProcessed, TotalJobItems, CreatedDate 
FROM AsyncApexJob 
WHERE Id = :jobId
```

### 4.3. Limites de Governança Principais
* **Fila Flexível (*Flex Queue*):** Máximo de **100 jobs** em estado *Holding* aguardando execução.
* **Concurrent Jobs:** Máximo de **5 Batch Jobs** rodando simultaneamente em estado *Processing*.

---

# 🤖 JSON Schema Exclusivo: Batch Apex

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceBatchApexDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "className": { "type": "string" },
        "apiVersion": { "type": "string" },
        "status": { "type": "string" },
        "description": { "type": "string" }
      },
      "required": ["className", "apiVersion"]
    },
    "batch_capabilities": {
      "type": "object",
      "properties": {
        "scopeType": { "type": "string", "enum": ["QueryLocator", "Iterable"] },
        "defaultBatchSize": { "type": "integer", "default": 200 },
        "isStateful": { "type": "boolean" },
        "allowsCallouts": { "type": "boolean" },
        "raisesPlatformEvents": { "type": "boolean" }
      },
      "required": ["scopeType"]
    },
    "implementation_details": {
      "type": "object",
      "properties": {
        "soqlQuery": { "type": "string" },
        "targetSObject": { "type": "string" },
        "chainedJobs": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "batch_capabilities"]
}
```

---

# 📑 Modelo 1.2: Queueable Apex (`System.Queueable`)

O **Queueable Apex** é a evolução dos métodos `@future`. Permite o processamento assíncrono com suporte a **estruturas de dados complexas (sObjects e DTOs)**, **encadeamento de jobs (*chaining*)**, **atraso na execução (*delay*)** e **tratamento de falhas via Finalizers**.

### Convenção de Nomes e Estrutura SFDX
* **Nome da Classe:** `[NomeDoDominio][Acao]Queueable.cls` (ex: `AWSOrderSenderQueueable.cls`, `AccountSyncQueueable.cls`)
* **Pasta no Repositório:** `force-app/main/default/classes/`
* **Arquivos Relacionados:** `AWSOrderSenderQueueable.cls` e `AWSOrderSenderQueueable.cls-meta.xml`

---

## 1. Identificação e Metadados do Queueable

| Propriedade | Valor Exemplo | Tag / Fonte | Descrição Técnica |
|---|---|---|---|
| **ClassName / ApiName** | `AWSOrderSenderQueueable` | Arquivo `.cls` | Nome exclusivo da classe Apex. |
| **ApiVersion** | `62.0` | `.cls-meta.xml` (`<apiVersion>`) | Versão da API Salesforce. |
| **Status** | `Active` | `.cls-meta.xml` (`<status>`) | Status de publicação na Org. |
| **Suporte a Encadeamento** | `Sim` (1 job encadeado por execução) | Código Apex | Permite chamar outro Queueable dentro do método `execute()`. |
| **Suporte a Atraso (*Delay*)** | `0 a 10 minutos` | Método `System.enqueueJob(job, delayInMinutes)` | Permite agendar a entrada na fila com atraso. |

---

## 2. Assinatura da Classe e Interfaces Suportadas

```apex
public class AWSOrderSenderQueueable implements System.Queueable, Database.AllowsCallouts { ... }
```

| Interface | Obrigatoriedade | Finalidade Técnica |
|---|---|---|
| **`System.Queueable`** | **Obrigatória** | Exige a implementação do método `execute(QueueableContext context)`. |
| **`Database.AllowsCallouts`** | Opcional | Libera o disparo de chamadas HTTP REST/SOAP para sistemas externos. |
| **`System.Finalizer`** | Opcional (Anexado) | Permite registrar uma classe para capturar o resultado (sucesso/exceção) da execução do Queueable. |

---

## 3. Método Obrigatório e Ciclo de Vida

| Método | Assinatura Técnica | Descrição / Responsabilidade |
|---|---|---|
| **`execute`** | `public void execute(System.QueueableContext context)` | Método único onde a lógica assíncrona é executada. O parâmetro `context` fornece o `getJobId()`. |

---

## 4. Invocação, Transaction Finalizers e Limites

### 4.1. Exemplo de Invocação Apex (Com Delay e Encadeamento)
```apex
AWSOrderSenderQueueable queueableJob = new AWSOrderSenderQueueable(orderList);

// Anexando um Finalizer para tratamento de erros
System.attachFinalizer(new IntegrationFinalizerHandler());

// Enfileirando com atraso de 5 minutos
Id jobId = System.enqueueJob(queueableJob, 5);
```

### 4.2. Limites de Governança Principais
* **Enfileiramentos por Transação:** Máximo de **50 `System.enqueueJob()`** em uma única transação síncrona.
* **Profundidade de Encadeamento (*Chaining Depth*):** Sem limite em Produção (em testes/Developer Org o limite é de 1 nível de encadeamento).

---

# 🤖 JSON Schema Exclusivo: Queueable Apex

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceQueueableApexDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "className": { "type": "string" },
        "apiVersion": { "type": "string" },
        "status": { "type": "string" },
        "description": { "type": "string" }
      },
      "required": ["className", "apiVersion"]
    },
    "queueable_capabilities": {
      "type": "object",
      "properties": {
        "allowsCallouts": { "type": "boolean" },
        "supportsChaining": { "type": "boolean" },
        "hasFinalizerAttached": { "type": "boolean" },
        "finalizerClassName": { "type": "string" }
      }
    },
    "payload_structure": {
      "type": "object",
      "properties": {
        "inputParameters": {
          "type": "array",
          "items": { "type": "string" }
        },
        "acceptsComplexObjects": { "type": "boolean", "default": true }
      }
    }
  },
  "required": ["identification", "queueable_capabilities"]
}
```

---

# 📑 Modelo 1.3: Future Method (`@future`)

O **Future Method** é utilizado para executar lógicas assíncronas simples em uma linha de execução separada, com limites de governança estendidos. É ideal para desacoplar tarefas leves, como atualizações secundárias de banco ou chamadas HTTP a partir de Triggers.

### Convenção de Nomes e Estrutura SFDX
* **Nome da Classe:** `[NomeDoDominio]AsyncHelper.cls` ou `[NomeDoDominio]Service.cls` (ex: `IntegrationAsyncHelper.cls`)
* **Pasta no Repositório:** `force-app/main/default/classes/`
* **Arquivos Relacionados:** `IntegrationAsyncHelper.cls` e `IntegrationAsyncHelper.cls-meta.xml`

---

## 1. Identificação e Assinatura Técnica do Método

```apex
public class IntegrationAsyncHelper {
    @future(callout=true)
    public static void processOrdersAsync(List<Id> orderIds) { ... }
}
```

| Propriedade | Valor Configurado | Descrição / Restrição Técnica |
|---|---|---|
| **Anotação Obrigatória** | `@future` | Marca o método estático para execução assíncrona. |
| **Modificador de Chamada HTTP** | `callout=true` \| `callout=false` | `@future(callout=true)` libera requisições de rede. |
| **Tipo de Retorno** | **Obrigatoriamente `void`** | Métodos `@future` não podem retornar valores. |
| **Modificadores de Acesso** | **Obrigatoriamente `public static` ou `global static`** | Métodos de instância não podem ser marcados como `@future`. |
| **Restrição de Parâmetros** | **Apenas tipos primitivos ou coleções de primitivos** | `List<Id>`, `Set<String>`, `Integer`. **PROIBIDO passar `sObjects` ou DTOs.** |

---

## 2. Regras de Negócio e Limitações Severas

⚠️ **REGRAS DE ARQUITETURA A CONSIDERAR:**
1. **Sem Garantia de Ordem:** A ordem em que múltiplos métodos `@future` são disparados **não** é a ordem em que serão executados pela plataforma.
2. **Proibição de Aninhamento:** Um método `@future` **não pode** chamar outro método `@future`.
3. **Monitoramento Limitado:** Retorna apenas `void`, o que dificulta o rastreio direto do ID de execução na mesma transação.

---

## 3. Invocação e Limites de Governança

### 3.1. Exemplo de Invocação Apex
```apex
List<Id> selectedOrderIds = new List<Id>{ '0010000000001AAA', '0010000000002AAA' };

// Invocação direta passando apenas lista de IDs primitivos
IntegrationAsyncHelper.processOrdersAsync(selectedOrderIds);
```

### 3.2. Limites de Governança
* **Invocações por Transação:** Máximo de **50 chamadas `@future`** por transação Apex síncrona.

---

# 🤖 JSON Schema Exclusivo: Future Method

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceFutureMethodDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "className": { "type": "string" },
        "methodName": { "type": "string" },
        "apiVersion": { "type": "string" },
        "description": { "type": "string" }
      },
      "required": ["className", "methodName"]
    },
    "future_configuration": {
      "type": "object",
      "properties": {
        "calloutAllowed": { "type": "boolean", "default": false },
        "parameterTypes": {
          "type": "array",
          "items": { "type": "string" }
        },
        "onlyPrimitiveParameters": { "type": "boolean", "enum": [true] }
      },
      "required": ["calloutAllowed", "onlyPrimitiveParameters"]
    }
  },
  "required": ["identification", "future_configuration"]
}
```

---

# 📑 Modelo 1.4: Scheduled Apex (`System.Schedulable`)

O **Scheduled Apex** permite agendar a execução de rotinas Apex em horários e datas específicos usando expressões Cron programáticas ou a interface do Salesforce.

### Convenção de Nomes e Estrutura SFDX
* **Nome da Classe:** `[NomeDoDominio][Acao]Scheduler.cls` (ex: `DailyOrderCleanupScheduler.cls`)
* **Pasta no Repositório:** `force-app/main/default/classes/`
* **Arquivos Relacionados:** `DailyOrderCleanupScheduler.cls` e `DailyOrderCleanupScheduler.cls-meta.xml`

---

## 1. Identificação e Metadados do Schedulable

| Propriedade | Valor Exemplo | Tag / Fonte | Descrição Técnica |
|---|---|---|---|
| **ClassName / ApiName** | `DailyOrderCleanupScheduler` | Arquivo `.cls` | Nome exclusivo da classe de agendamento. |
| **ApiVersion** | `62.0` | `.cls-meta.xml` (`<apiVersion>`) | Versão da API Salesforce. |
| **Interface Implementada** | `System.Schedulable` | Assinatura da Classe | Exige o método `execute(SchedulableContext SC)`. |
| **Sintaxe da Expressão Cron** | `Seconds Minutes Hours Day_of_month Month Day_of_week [Year]` | Parâmetro do `System.schedule()` | Define a periodicidade exata de execução. |

---

## 2. Assinatura da Classe e Padrão de Arquitetura

```apex
public class DailyOrderCleanupScheduler implements System.Schedulable {
    public void execute(System.SchedulableContext SC) {
        // BOA PRÁTICA: Delegar a execução para um Batch ou Queueable
        OrderCleanupBatch batch = new OrderCleanupBatch();
        Database.executeBatch(batch, 200);
    }
}
```

💡 **BOA PRÁTICA DE ARQUITETURA:** A classe `Schedulable` **não deve conter lógica de negócios pesada nem DMLs diretas**. Ela deve atuar apenas como um gatilho temporizado que dispara um **Batch Apex** ou **Queueable Apex**.

---

## 3. Invocação Programática e Expressão Cron

### 3.1. Tabela de Exemplos de Expressão Cron

| Expressão Cron | Periodicidade de Execução |
|---|---|
| `0 0 1 * * ?` | Todos os dias à 01:00 AM. |
| `0 0 12 ? * MON-FRI` | Segunda a Sexta-feira às 12:00 PM (Meio-dia). |
| `0 15 10 15 * ?` | Todo dia 15 de cada mês às 10:15 AM. |

### 3.2. Exemplo de Agendamento via Apex
```apex
DailyOrderCleanupScheduler scheduler = new DailyOrderCleanupScheduler();
String cronExpression = '0 0 1 * * ?'; // Diário à 01:00 AM

// Registra o job na CronTrigger da Org
String jobId = System.schedule('Limpeza Diaria de Pedidos', cronExpression, scheduler);
```

### 3.3. Monitoramento de Jobs Agendados (`CronTrigger`)
```sql
SELECT Id, CronJobDetail.Name, CronExpression, State, NextFireTime 
FROM CronTrigger 
WHERE Id = :jobId
```

---

# 🤖 JSON Schema Exclusivo: Scheduled Apex

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceScheduledApexDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "className": { "type": "string" },
        "apiVersion": { "type": "string" },
        "status": { "type": "string" },
        "description": { "type": "string" }
      },
      "required": ["className", "apiVersion"]
    },
    "schedule_configuration": {
      "type": "object",
      "properties": {
        "defaultCronExpression": { "type": "string" },
        "jobName": { "type": "string" },
        "delegatesToBatchOrQueueable": { "type": "boolean", "default": true },
        "delegatedClassName": { "type": "string" }
      },
      "required": ["defaultCronExpression", "jobName"]
    }
  },
  "required": ["identification", "schedule_configuration"]
}
```

---

Com o detalhamento completo e os **JSON Schemas individuais** para cada tipo de classe assíncrona da **Onda 01**, seu utilitário ou agente de IA pode agora analisar, validar e documentar o código Apex com máxima precisão!

💡 Deseja que passemos para o detalhamento individualizado dos modelos de alguma outra onda (como a **Onda 03 de LWCs por classificação** ou a **Onda 10 de OmniStudio**)?
