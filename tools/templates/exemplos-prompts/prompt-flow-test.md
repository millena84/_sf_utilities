# Prompt — FlowTest

## 1. Contexto do componente

### 1.1 O que é
`FlowTest` (nome funcional: **Flow Test** ou **Teste de Flow**) é um recurso do Salesforce que permite criar e executar testes automatizados para validar o comportamento de Flows sem depender de execução manual. Ele registra cenários de entrada, ações simuladas e asserções sobre o resultado.

Na prática, `FlowTest`:
- define um cenário de teste vinculado a uma versão específica de um Flow;
- especifica dados de entrada, registros de teste e expectativas de saída;
- pode ser executado manualmente ou como parte de deploys;
- ajuda a garantir que alterações em Flows não quebrem comportamentos existentes.

### 1.2 Para que serve
- Automatizar a validação de Flows.
- Garantir regressão em deploys.
- Documentar comportamento esperado do Flow.
- Reduzir testes manuais repetitivos.

### 1.3 Cenários típicos de uso
- Testar Record-Triggered Flows com cenários de criação/atualização.
- Validar decisões e branches de Screen Flows.
- Garantir que subflows produzem resultados esperados.
- Testar fórmulas e atribuições.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível onde Flow Builder e testes de Flow estão habilitados.
- Aplicável a todos os tipos de Flow suportados por testes.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `FlowTest`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Flow Test |
| Metadata type exact | `FlowTest` |
| Pasta no projeto SFDX | `flowTests/` |
| Arquivo padrão | `<apiName>.flowTest-meta.xml` |
| Objeto interno (API padrão) | `FlowTestView`, `FlowTestResult` |
| Objeto interno (Tooling API) | `FlowTest` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `FlowTestView`, `FlowTestResult` |
| Acessível por Tooling API | Sim — `SELECT ... FROM FlowTest` |
| Acessível por Apex | Parcial — via SOQL em views |
| Acessível por UI | Sim — **Flow Builder → Tests** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Flow | `Flow` (metadata/API) | Flow sendo testado. |
| Flow Version | `FlowVersionView` | Versão específica testada. |
| Flow Test Result | `FlowTestResult` | Resultado da execução. |
| Apex Test / Deployment | `ApexTestResult`, `DeployDetails` | Testes podem ser executados em deploy. |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`FlowTest`)

Arquivo típico: `flowTests/<API_Name>.flowTest-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<flowApiName>` | 1 | API Name do Flow testado. |
| `<label>` | 1 | Nome amigável do teste. |
| `<description>` | 0..1 | Descrição do cenário. |
| `<flowVersion>` | 0..1 | Versão do Flow testada. |
| `<testConditions>` | 0..1 | Bloco de condições/asserções do teste. |
| `<testCondition>` | 0..N | Condição específica a ser validada. |
| `<testInputs>` | 0..1 | Dados de entrada do teste. |
| `<testInput>` | 0..N | Valor de entrada para variável/elemento. |

### 3.2 Objetos internos via API padrão

#### `FlowTestView`

| Campo | Significado prático |
|---|---|
| `Id` | ID do teste. |
| `FlowDefinitionViewId` | Definição do Flow testado. |
| `Label` | Nome do teste. |
| `FlowVersionId` | Versão testada. |

#### `FlowTestResult`

| Campo | Significado prático |
|---|---|
| `Id` | ID do resultado. |
| `FlowTestViewId` | Teste executado. |
| `Status` | `Pass`, `Fail`, `Skipped`, `Error`. |
| `StartTime`, `EndTime` | Duração. |
| `ErrorMessage` | Mensagem de erro, se houver. |

### 3.3 Exemplos de query

```sql
SELECT Id, Label, FlowDefinitionViewId, FlowDefinitionView.ApiName, FlowVersionId
FROM FlowTestView
ORDER BY Label
```

```sql
SELECT Id, FlowTestViewId, FlowTestView.Label, Status, ErrorMessage, StartTime, EndTime
FROM FlowTestResult
ORDER BY StartTime DESC
```

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `Flow`

- Teste é sempre vinculado a uma definição/versão de Flow.
- Alterações na lógica do Flow podem exigir atualização dos testes.

### 4.2 `FlowVersionView`

- Importante para saber qual versão foi coberta pelo teste.

### 4.3 `FlowTestResult`

- Estado efetivo de execução. Não confundir teste definido com teste aprovado.

---

## 5. Boas práticas e pontos de atenção

- Não expor dados reais ou PII em cenários de teste.
- Documentar o propósito de cada teste na descrição.
- Manter testes atualizados quando o Flow evolui.
- Separar testes por cenário (sucesso, erro, caminho alternativo).
- Executar testes antes de deploys para detectar regressão.
- Não assumir que um teste definido foi executado com sucesso; validar `FlowTestResult`.

---

## 6. Links de referência oficial

- [Salesforce Help — Test a Flow](https://help.salesforce.com/s/articleView?id=sf.flow_test.htm)
- [Salesforce Developer — FlowTest Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flowtest.htm)
- [Salesforce Help — Flow Builder](https://help.salesforce.com/s/articleView?id=sf.flow.htm)
