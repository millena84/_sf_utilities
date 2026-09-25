# Prompt — FlowValueMap

## 1. Contexto do componente

### 1.1 O que é
`FlowValueMap` (nome funcional: **Flow Value Map**) é um componente de automação do Salesforce presente dentro da estrutura de um Flow. Ele representa uma **coleção de pares chave-valor** usada tipicamente em operações de transformação, como entradas de mapeamento para elementos `Transform` (Data Transform) ou para padronizar/converter valores entre domínios diferentes durante a execução de um fluxo.

Na prática, um `FlowValueMap`:
- faz parte do metadata do Flow (`.flow-meta.xml`);
- agrupa valores constantes ou referências a recursos do Flow;
- pode ser usado em transformações de dados (`FlowTransform`);
- permite mapear valores de entrada para valores de saída (ex.: status externo → status interno);
- não é um objeto independente consultável via SOQL — sua análise depende do parse do XML do Flow.

### 1.2 Para que serve
- Mapear valores entre sistemas ou domínios dentro de um Flow.
- Padronizar códigos/catálogos externos para valores internos do Salesforce.
- Simplificar lógicas condicionais massivas (substituir várias decisões por uma tabela de mapeamento).
- Apoiar transformações declarativas de dados entre coleções e registros.

### 1.3 Cenários típicos de uso
- Converter códigos de país de um ERP para picklist values do Salesforce.
- Mapear status de pedido de um marketplace para Status de Opportunity/Order.
- Transformar códigos de erro de API externa em mensagens amigáveis.
- Fornecer valores padrão para transformação de coleções em Flow.

### 1.4 Clouds / contextos
- **Salesforce Core** — Flow Builder e Data Transform.
- **Experience Cloud** — Screen flows que processam dados externos.
- **Service Cloud / Sales Cloud / Industries** — automações com integrações.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `FlowValueMap`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Value Map / Mapa de Valores (dentro do Flow Builder) |
| Metadata type exact | `Flow` (sub-elemento `<valueMaps>`) |
| Pasta no projeto SFDX | `flows/` (dentro do `.flow-meta.xml`) |
| Arquivo padrão | `<flowApiName>.flow-meta.xml` |
| Objeto interno (API padrão) | Não consultável diretamente via SOQL |
| Objeto interno (Tooling API) | Acessível via `Metadata`/`FullName` do `Flow` como XML |
| Acessível por Metadata API | Sim — via retrieve do Flow |
| Acessível por API padrão / SOQL | Não diretamente |
| Acessível por Tooling API | Sim — via campo `Metadata` do Flow |
| Acessível por Apex | Não diretamente |
| Acessível por UI | Sim — dentro do Flow Builder, em componentes de transformação |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Flow | `Flow` (`.flow-meta.xml`) | Contém o `FlowValueMap`. |
| Flow Transform | `FlowTransform` (sub-elemento do Flow) | Elemento que consome o value map. |
| Flow Constant | `FlowConstant` | Pode ser referenciado como valor. |
| Flow Variable | `FlowVariable` | Pode ser referenciado como chave/valor. |
| Flow Formula | `FlowFormula` | Pode ser usado em valores dinâmicos. |
| Apex Action | `FlowApexPluginCall` / Apex invocável | Pode produzir/consumir mapeamentos alternativos. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações no Flow. |

### 2.3 Matriz de acessibilidade

| Fonte | FlowValueMap | Flow metadata | Tooling API | Setup/UI |
|---|---|---|---|---|
| Nome / API Name | dentro do XML | `<apiName>` do Flow | `Flow.FullName` | Sim |
| Entradas chave-valor | `<valueMap>` / `<entries>` | dentro do XML | `Metadata` do Flow | Sim (no transform) |
| Flow associado | atributo `name` do mapa | `<flows>` | `Flow.DefinitionId` | Sim |
| Versão | dentro do XML de versão | `FlowVersion.VersionNumber` | `FlowVersionView` | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`FlowValueMap`)

O `FlowValueMap` aparece como sub-elemento dentro de `.flow-meta.xml`, geralmente dentro de `<valueMaps>`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<valueMaps>` | 0..N | Container de todos os value maps do Flow. |
| `<valueMap>` | 0..N | Cada mapa individual. |
| `<name>` | 1 | Nome/API Name do value map dentro do Flow. |
| `<dataType>` | 0..1 | Tipo de dados dos valores (String, Number, Boolean etc.). |
| `<description>` | 0..1 | Descrição. |
| `<entries>` | 0..N | Entradas do mapa. |
| `<key>` | 1 | Chave da entrada. |
| `<value>` | 1 | Valor da entrada. |

#### Exemplo

```xml
<valueMaps>
    <name>StatusPedidoMap</name>
    <dataType>String</dataType>
    <description>Mapeia status do ERP para Status de Opportunity</description>
    <entries>
        <key>PENDING</key>
        <value>Aberto</value>
    </entries>
    <entries>
        <key>PAID</key>
        <value>Ganho</value>
    </entries>
    <entries>
        <key>CANCELLED</key>
        <value>Perdido</value>
    </entries>
</valueMaps>
```

### 3.2 Uso em transformações (`FlowTransform`)

`FlowValueMap` é frequentemente utilizado por elementos de transformação para converter valores de uma coleção ou registro.

```xml
<transforms>
    <name>MapearStatus</name>
    <label>Mapear Status</label>
    <locationX>123</locationX>
    <locationY>456</locationY>
    <dataTypeMappings>
        <typeName>T__sourceRecord</typeName>
        <typeValue>Opportunity</typeValue>
    </dataTypeMappings>
    <transformFormulas>
        <expression>VALUEMAP(StatusPedidoMap, {!sourceRecord.Status_Externo__c})</expression>
        <name>statusMapeado</name>
    </transformFormulas>
</transforms>
```

> **Nota**: sintaxe exata pode variar conforme versão do Flow. Verifique a API `FlowTransform` e `FlowTransformFormula`.

### 3.3 Extraindo via Tooling API

O `Metadata` completo do Flow pode ser obtido via Tooling API e então parseado para localizar `<valueMaps>`.

```sql
SELECT Id, DefinitionId, VersionNumber, Status, Metadata
FROM FlowVersionView
WHERE FlowDefinitionView.ApiName = 'Meu_Flow'
```

O campo `Metadata` retorna XML/JSON (dependendo da API) contendo `<valueMaps>`.

### 3.4 Extraindo via arquivo SFDX

Buscar diretamente no repositório:

```bash
grep -A 5 "<valueMaps>" force-app/main/default/flows/*.flow-meta.xml
```

---

### 3.4 Configuração observável em outras fontes

- Flow Builder → abrir o Flow → elementos de transformação.
- Setup → Flows → abrir versão específica.
- Arquivos `.flow-meta.xml` no repositório SFDX.
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Chaves/valores do mapa | XML do Flow | SOQL direto | Requer parse do metadata. |
| Uso dinâmico em runtime | Logs de debug / execution logs | Metadata | Estado de execução. |
| Referências a recursos externos | XML do Flow | `FlowDefinitionView` | Requer análise do arquivo. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `Flow`

- Container do value map.
- Cada versão pode ter value maps diferentes.

### 4.2 `FlowTransform`

- Elemento que consome value maps para transformar dados.
- Pode ter múltiplas fórmulas de transformação.

### 4.3 `FlowConstant` / `FlowVariable`

- Recursos do Flow que podem ser referenciados como valores no mapa.

### 4.4 `FlowFormula`

- Fórmula usada para calcular valor dinâmico a ser convertido pelo mapa.

### 4.5 `SetupAuditTrail`

- Registra alterações no Flow, incluindo criação/alteração de value maps.

---

## 5. Consultas e formas de extração

### 5.1 Listar Flows com potencial uso de value maps

```sql
SELECT Id, ApiName, Label, Description, LatestVersionId, ActiveVersionId, Status
FROM FlowDefinitionView
ORDER BY Label
```

### 5.2 Versões de um Flow

```sql
SELECT Id, FlowDefinitionViewId, FlowDefinitionView.ApiName,
       VersionNumber, Status, ApiVersion, LastModifiedDate
FROM FlowVersionView
WHERE FlowDefinitionView.ApiName = 'Meu_Flow'
ORDER BY VersionNumber DESC
```

### 5.3 Buscar value maps no repositório SFDX

```bash
grep -rl "<valueMaps>" force-app/main/default/flows/
```

### 5.4 Exemplo de extração programática (XML)

```python
import xml.etree.ElementTree as ET

ns = {'flow': 'http://soap.sforce.com/2006/04/metadata'}
tree = ET.parse('flows/Meu_Flow.flow-meta.xml')
for vm in tree.findall('.//flow:valueMaps', ns):
    name = vm.find('flow:name', ns)
    print(f"Value Map: {name.text}")
    for entry in vm.findall('flow:entries', ns):
        key = entry.find('flow:key', ns)
        value = entry.find('flow:value', ns)
        print(f"  {key.text} -> {value.text}")
```

---

## 6. Boas práticas e pontos de atenção

- **Mantenha value maps dentro de Flows versionados**: cada mudança exige nova versão.
- **Documente o propósito** de cada value map na `<description>`.
- **Evite duplicar value maps** entre múltiplos Flows; prefira recursos compartilhados (quando disponível).
- **Valide chaves/valores ausentes**: implemente fallback no transform/tratamento de erros.
- **Case sensitivity**: padronize chaves (upper/lower case) para evitar comportamentos inesperados.
- **Considere Custom Metadata Types** para tabelas de mapeamento maiores ou compartilhadas entre Flows/Apex.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Teste transformações** com amostras representativas de dados.

---

## 7. Links de referência oficial

- [Salesforce Help — Flow Builder](https://help.salesforce.com/s/articleView?id=sf.flow.htm)
- [Salesforce Help — Transform Data in a Flow](https://help.salesforce.com/s/articleView?id=sf.flow_transform_overview.htm)
- [Salesforce Developer — Flow Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flow.htm)
- [Salesforce Developer — FlowValueMap Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/flow_value_map.htm)
