# Prompt — ApexTestSuite

## 1. Contexto do componente

### 1.1 O que é
`ApexTestSuite` (nome funcional: **Apex Test Suite** ou **Conjunto de Testes Apex**) é uma coleção nomeada de classes de teste Apex. Uma suite permite agrupar classes de teste relacionadas para execução conjunta, facilitando a execução seletiva de testes em deploys, integrações contínuas e validações de qualidade.

Na prática, um `ApexTestSuite`:
- é um metadata type no Salesforce;
- contém uma lista de `ApexClass` de teste;
- pode ser executado via Developer Console, API (`RunTestsRequest`) ou ferramentas CLI;
- ajuda a organizar testes por módulo, funcionalidade ou camada (unitário, integração);
- não contém código em si — apenas referências a classes de teste.

### 1.2 Para que serve
- Agrupar classes de teste para execução coordenada.
- Facilitar execução seletiva em pipelines CI/CD.
- Organizar testes por domínio ou funcionalidade.
- Rastrear cobertura de testes por suite.
- Acelerar validações antes de deploys.

### 1.3 Cenários típicos de uso
- Suite de testes de integração com ERP.
- Suite de testes de triggers de oportunidade.
- Suite de regressão rápida para um módulo.
- Suite específica para validação de PR.

### 1.4 Clouds / contextos
- **Salesforce Core** — desenvolvimento Apex e qualidade de código.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ApexTestSuite`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Apex Test Suite / Conjunto de Testes |
| Metadata type exact | `ApexTestSuite` |
| Pasta no projeto SFDX | `testSuites/` |
| Arquivo padrão | `<apiName>.testSuite-meta.xml` |
| Objeto interno (API padrão) | `ApexTestSuite` |
| Objeto interno (Tooling API) | `ApexTestSuite` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ApexTestSuite` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `ApexTestSuite` é consultável |
| Acessível por UI | Sim — **Developer Console → Test → New Suite** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Apex Test Class | `ApexClass` | Classes que compõem a suite. |
| Apex Test Result | `ApexTestResult` | Resultados de execução. |
| Apex Test Queue Item | `ApexTestQueueItem` | Fila de execução. |
| Apex Code Coverage | `ApexCodeCoverage` | Cobertura vinculada às classes. |
| Async Apex Job | `AsyncApexJob` | Job de execução dos testes. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | ApexTestSuite metadata | Objeto SOQL | Tooling | Setup/UI |
|---|---|---|---|---|
| Nome da suite | Sim | `TestSuiteName` | Sim | Sim |
| Classes incluídas | `<testClassName>` na lista | `ApexClass.Name` via join | Sim | Sim |
| Resultados de execução | — | `ApexTestResult` | Sim | Developer Console |
| Cobertura | — | `ApexCodeCoverage` | Sim | Developer Console |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ApexTestSuite`)

Arquivo típico: `testSuites/<API_Name>.testSuite-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<testSuite>` | 1 | Raiz. |
| `<testClassName>` | 0..N | Nome de uma classe de teste Apex. |

#### Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ApexTestSuite xmlns="http://soap.sforce.com/2006/04/metadata">
    <testClassName>MinhaClasseTest</testClassName>
    <testClassName>OutraClasseTest</testClassName>
</ApexTestSuite>
```

### 3.2 Objeto interno via API padrão: `ApexTestSuite`

| Campo | Significado prático |
|---|---|
| `Id` | ID da suite. |
| `TestSuiteName` | Nome/API Name da suite. |
| `ApexClassId` | Classe de teste vinculada (uma linha por classe). |

#### Exemplo de query

```sql
SELECT Id, TestSuiteName, ApexClassId, ApexClass.Name
FROM ApexTestSuite
ORDER BY TestSuiteName, ApexClass.Name
```

### 3.3 Execução e resultados

#### Resultados de teste

```sql
SELECT Id, ApexClass.Name, MethodName, Outcome, Message,
       StackTrace, RunTime, TestTimestamp
FROM ApexTestResult
ORDER BY TestTimestamp DESC
```

#### Cobertura

```sql
SELECT Id, ApexClassOrTrigger.Name, Coverage
FROM ApexCodeCoverage
ORDER BY ApexClassOrTrigger.Name
```

---

### 3.4 Configuração observável em outras fontes

- Developer Console → Test → New Suite / View Test Suites.
- Setup → Apex Test Execution.
- `SetupAuditTrail`.
- CLI `sfdx force:apex:test:run --testlevel RunSpecifiedTests --classnames ...`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Código das classes de teste | `ApexClass` SOQL/Tooling | `ApexTestSuite` | Suite apenas referencia. |
| Detalhes de falhas | `ApexTestResult` | `ApexTestSuite` | Requer execução. |
| Logs de execução | Debug logs | `ApexTestSuite` | Requer profile ativo. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ApexClass`

- Classes de teste listadas na suite.

### 4.2 `ApexTestResult`

- Resultados individuais por método de teste.

### 4.3 `ApexCodeCoverage`

- Cobertura das classes de produção associadas aos testes.

### 4.4 `AsyncApexJob`

- Job assíncrono quando a suite é executada em grande volume.

---

## 5. Consultas e formas de extração

### 5.1 Suites e suas classes

```sql
SELECT Id, TestSuiteName, ApexClassId, ApexClass.Name
FROM ApexTestSuite
ORDER BY TestSuiteName, ApexClass.Name
```

### 5.2 Classes sem suite

```sql
SELECT Id, Name
FROM ApexClass
WHERE Name LIKE '%Test'
  AND Id NOT IN (SELECT ApexClassId FROM ApexTestSuite)
ORDER BY Name
```

### 5.3 Últimos resultados de teste

```sql
SELECT Id, ApexClass.Name, MethodName, Outcome, TestTimestamp
FROM ApexTestResult
ORDER BY TestTimestamp DESC
LIMIT 100
```

### 5.4 Cobertura por classe

```sql
SELECT Id, ApexClassOrTrigger.Name, Coverage
FROM ApexCodeCoverage
ORDER BY ApexClassOrTrigger.Name
```

---

## 6. Boas práticas e pontos de atenção

- **Agrupe testes por domínio** ou camada (unidade, integração, regressão).
- **Mantenha suites pequenas o suficiente** para feedback rápido, mas cobertura ampla.
- **Garanta que classes de teste realmente existam** ao adicionar à suite.
- **Automatize execução** em pipelines CI/CD.
- **Monitore cobertura mínima exigida** pela org/hierarquia.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Remova suites obsoletas** para evitar confusão.
- **Documente o escopo** de cada suite.

---

## 7. Links de referência oficial

- [Salesforce Developer — ApexTestSuite Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_apextestsuite.htm)
- [Salesforce Developer — Run Apex Tests](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_testsetup.htm)
- [Salesforce Developer — ApexTestResult Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_apextestresult.htm)
- [Salesforce Developer — ApexCodeCoverage Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_apexcodecoverage.htm)
