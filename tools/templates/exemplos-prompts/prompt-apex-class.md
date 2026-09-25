# Prompt — ApexClass

## 1. Contexto do componente

### 1.1 O que é
`ApexClass` (nome funcional: **Apex Class**) é um metadata type do Salesforce usado para definir classes escritas na linguagem Apex. Cada classe Apex contém métodos, atributos, construtores e anotações que implementam a lógica de negócios da plataforma Salesforce.

Na prática, uma `ApexClass`:
- pode ser invocada por triggers, Visualforce, Lightning Components, Flows, Process Builder, APIs e outros pontos de extensão;
- pode implementar interfaces do Salesforce (`Queueable`, `Schedulable`, `InvocableMethod`, `Auth.RegistrationHandler`, `Messaging.InboundEmailHandler` etc.);
- pode realizar operações de banco de dados, callouts HTTP, manipulação de arquivos, cálculos complexos e integrações;
- possui um corpo de código fonte que pode ser lido parcialmente pelo Tooling API (`Body`);
- é dependente de permissões de execução controladas por Permission Sets, Profiles e Sharing Rules.

### 1.2 Para que serve
- Implementar lógica de negócio customizada.
- Processar grandes volumes de dados (batch, queueable, schedulable).
- Realizar integrações outbound/inbound.
- Servir como controlador para Visualforce e LWC.
- Expor funcionalidades para Flows via `@InvocableMethod`.

### 1.3 Cenários típicos de uso
- Trigger handler centralizado.
- Serviço REST/SOAP customizado.
- Agendamento de jobs (`Schedulable`).
- Processamento assíncrono em fila (`Queueable`).
- Integração via callouts HTTP.
- Controlador de componente Visualforce ou LWC.

### 1.4 Clouds / contextos
- **Salesforce Core** — lógica de negócio e automações.
- **Experience Cloud** — controllers de páginas e componentes.
- **Sales/Service/Industry Clouds** — extensões específicas por cloud.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ApexClass`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Apex Class / Classe Apex |
| Metadata type exact | `ApexClass` |
| Pasta no projeto SFDX | `classes/` |
| Arquivo padrão | `<apiName>.cls` + `<apiName>.cls-meta.xml` |
| Objeto interno (API padrão) | `ApexClass` |
| Objeto interno (Tooling API) | `ApexClass` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ApexClass` |
| Acessível por Tooling API | Sim — inclui `Body`, `SymbolTable` |
| Acessível por Apex | Não diretamente |
| Acessível por UI | Sim — **Setup → Apex Classes** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Apex Trigger | `ApexTrigger` | Pode chamar a classe. |
| Visualforce Page | `ApexPage` | Pode usar classe como controller. |
| Visualforce Component | `ApexComponent` | Pode usar classe como controller. |
| Lightning Component (Aura) | `AuraDefinitionBundle` | Pode chamar métodos Apex. |
| Lightning Web Component | `LightningComponentBundle` | Pode chamar métodos Apex via `@AuraEnabled`. |
| Flow | `Flow` | Pode invocar métodos `@InvocableMethod`. |
| Test Class | `ApexClass` | Classe com `@isTest`. |
| Permission Set / Profile | `PermissionSet`, `Profile` | Acesso a classes Apex. |
| Email Service | `EmailServicesFunction` | Pode usar handler Apex. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | ApexClass metadata | `ApexClass` (SOQL) | Tooling | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | `Name` | Sim | Sim | Sim |
| Corpo do código | Sim (`.cls`) | — | `Body` | Sim | Sim |
| Status / API Version | `.cls-meta.xml` | `ApiVersion`, `Status` | Sim | Sim | Sim |
| Tamanho / complexidade | — | `LengthWithoutComments` | `LengthWithoutComments` | — | Sim |
| Permissões de acesso | via `PermissionSet`/`Profile` | `SetupEntityAccess` | Sim | Setup | Sim |
| Testes relacionados | via `ApexTestResult` / `ApexTestQueueItem` | — | Sim | Setup | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ApexClass`)

Arquivo típico: `classes/<API_Name>.cls` + `classes/<API_Name>.cls-meta.xml`.

#### Tags principais do `.cls-meta.xml`

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<apiVersion>` | 1 | Versão da API usada pela classe. |
| `<status>` | 1 | `Active` ou `Deleted`. |
| `<packageVersions>` | 0..N | Versões de pacotes managed referenciados. |

#### Corpo da classe (`.cls`)

| Elemento | Descrição prática |
|---|---|
| Declaração `public class / global class` | Nome e visibilidade. |
| Atributos / propriedades | Variáveis de classe. |
| Métodos | Lógica encapsulada. |
| Construtores | Inicialização. |
| Anotações | `@AuraEnabled`, `@InvocableMethod`, `@isTest`, `@future`, `@RemoteAction`, `@RestResource`, `@HttpGet` etc. |
| Inner classes | Classes aninhadas. |

### 3.2 Objeto interno via API padrão: `ApexClass`

| Campo | Significado prático |
|---|---|
| `Id` | ID da classe. |
| `Name` | Nome da classe. |
| `ApiVersion` | Versão da API. |
| `Status` | `Active` ou `Deleted`. |
| `IsValid` | Compilou com sucesso. |
| `BodyCrc` | Checksum do corpo. |
| `LengthWithoutComments` | Tamanho do código sem comentários. |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |
| `CreatedById`, `LastModifiedById` | Autores. |

#### Exemplo de query

```sql
SELECT Id, Name, ApiVersion, Status, IsValid,
       LengthWithoutComments, CreatedDate, LastModifiedDate,
       CreatedBy.Name, LastModifiedBy.Name
FROM ApexClass
ORDER BY Name
```

### 3.3 Tooling API — detalhes extras

```sql
SELECT Id, Name, Body, ApiVersion, Status, IsValid, LengthWithoutComments,
       CreatedDate, LastModifiedDate
FROM ApexClass
ORDER BY Name
```

#### SymbolTable

```sql
SELECT Id, Name, SymbolTable
FROM ApexClass
WHERE Name = 'MinhaClasse'
```

Retorna estrutura de métodos, construtores, propriedades e dependências.

### 3.4 Permissões de acesso à classe

#### Por Permission Set

```sql
SELECT Id, ParentId, Parent.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType = 'ApexClass'
ORDER BY Parent.Name
```

#### Por Profile

```sql
SELECT Id, ParentId, Parent.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType = 'ApexClass'
  AND ParentId IN (SELECT Id FROM Profile)
ORDER BY Parent.Name
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Apex Classes.
- Setup → Apex Test Execution.
- Setup → Developer Console → Logs.
- `SetupAuditTrail`.
- Source code no repositório SFDX.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Código fonte completo | Arquivo `.cls` / Tooling `Body` | `ApexClass` SOQL padrão | Necessário Tooling ou metadata. |
| Dados em runtime | Logs de debug | Metadata do componente | Estado de execução. |
| Heap / CPU | Debug logs | `ApexClass` | Profiling. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ApexTrigger`

- Triggers podem delegar lógica para classes handler.

### 4.2 `ApexPage` / `ApexComponent`

- Páginas e componentes Visualforce podem usar a classe como controller.

### 4.3 `LightningComponentBundle` / `AuraDefinitionBundle`

- LWCs e Aura components chamam métodos `@AuraEnabled`.

### 4.4 `Flow`

- Métodos anotados com `@InvocableMethod` podem ser chamados por Flows.

### 4.5 `PermissionSet` / `Profile`

- Controlam quem pode executar a classe.

### 4.6 `ApexTestResult` / `ApexTestQueueItem`

- Resultados de execução de testes.

---

## 5. Consultas e formas de extração

### 5.1 Classes Apex

```sql
SELECT Id, Name, ApiVersion, Status, IsValid,
       LengthWithoutComments, CreatedDate, LastModifiedDate,
       CreatedBy.Name, LastModifiedBy.Name
FROM ApexClass
ORDER BY Name
```

### 5.2 Classes de teste

```sql
SELECT Id, Name, ApiVersion, Status, IsValid
FROM ApexClass
WHERE Name LIKE '%Test%'
   OR Name LIKE '%Tests'
ORDER BY Name
```

### 5.3 Permissões de acesso

```sql
SELECT Id, ParentId, Parent.Name, Parent.Type, SetupEntityId, SetupEntity.Name
FROM SetupEntityAccess
WHERE SetupEntityType = 'ApexClass'
ORDER BY Parent.Name
```

### 5.4 Cobertura de testes (ApexCodeCoverageAggregate)

```sql
SELECT ApexClassOrTriggerId, ApexClassOrTrigger.Name,
       NumLinesCovered, NumLinesUncovered, Coverage
FROM ApexCodeCoverageAggregate
ORDER BY ApexClassOrTrigger.Name
```

### 5.5 Métodos invocáveis por Flow

```sql
SELECT Id, Name
FROM ApexClass
WHERE Body LIKE '%@InvocableMethod%'
ORDER BY Name
```

---

## 6. Boas práticas e pontos de atenção

- **Aplique o princípio da responsabilidade única**: uma classe por propósito.
- **Centralize lógica de trigger em handler classes**: evite lógica direta em triggers.
- **Respeite os limites de governança** (SOQL, DML, callouts, heap, CPU).
- **Escreva testes unitários** com cobertura mínima de 75%.
- **Use `@AuraEnabled` com segurança**: valide permissões e dados de entrada.
- **Evite `@future` excessivo**: prefira `Queueable` para controle e encadeamento.
- **Versione classes** com API version adequada.
- **Documente a finalidade** no cabeçalho da classe.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Monitore erros** em logs de debug e email de Apex exceptions.

---

## 7. Links de referência oficial

- [Salesforce Help — Apex Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dev_guide.htm)
- [Salesforce Developer — ApexClass Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_apexclass.htm)
- [Salesforce Developer — Apex Annotations](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_annotation.htm)
- [Salesforce Developer — Governors Limits](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm)
- [Salesforce Help — Debug Logs](https://help.salesforce.com/s/articleView?id=sf.code_debug_log.htm)
