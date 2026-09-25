# Prompt — FlowCategory

## 1. Contexto do componente

### 1.1 O que é
`FlowCategory` (nome funcional: **Flow Category** ou **Categoria de Flow**) é um metadata type do Salesforce usado para agrupar e categorizar Flows na interface de administração e no catálogo. Ele funciona como uma etiqueta organizacional que facilita a descoberta, governança e navegação quando há muitos Flows na org.

Na prática, um `FlowCategory`:
- define um rótulo e uma descrição para um agrupamento lógico de Flows;
- vincula um ou mais Flows à categoria;
- pode ser usado para organizar Flows por negócio, time, produto ou função;
- não altera a execução ou comportamento dos Flows — é puramente classificatório.

### 1.2 Para que serve
- Organizar e catalogar Flows em grupos lógicos.
- Facilitar a governança e a busca na lista de Flows.
- Documentar a propriedade/área de negócio de cada Flow.
- Melhorar a manutenção em orgs com grande volume de automações declarativas.

### 1.3 Cenários típicos de uso
- Categorizar Flows por produto (Sales, Service, Marketing).
- Separar Flows transversais dos específicos de um objeto.
- Agrupar Flows por time responsável (TI, Negócios, Integrações).
- Catalogar Flows legados versus modernos.

### 1.4 Clouds / contextos
- **Salesforce Core** — disponível onde Flow Builder é usado.
- Aplicável a todos os contextos que utilizam Flow: Service Cloud, Sales Cloud, Experience Cloud, Field Service, Agentforce.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `FlowCategory`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Flow Category |
| Metadata type exact | `FlowCategory` |
| Pasta no projeto SFDX | `flowCategories/` |
| Arquivo padrão | `<apiName>.flowCategory-meta.xml` |
| Objeto interno (API padrão) | `FlowCategoryView` (quando disponível) |
| Objeto interno (Tooling API) | `FlowCategory` (com campo `Metadata`) |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Parcial — verificar `FlowCategoryView` na org |
| Acessível por Tooling API | Sim — `SELECT ... FROM FlowCategory` |
| Acessível por Apex | Limitado — preferir Tooling/Metadata |
| Acessível por UI | Sim — **Setup → Flows → categorias** / Flow Builder |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Flow | `Flow` (metadata/API) | Flows vinculados à categoria. |
| Flow Definition View | `FlowDefinitionView` | Lista os Flows existentes para mapear associações. |
| Flow Category Item | `<flowCategoryItems>` no XML / objeto `FlowCategoryItem` | Associação entre categoria e Flow. |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`FlowCategory`)

Arquivo típico: `flowCategories/<API_Name>.flowCategory-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<description>` | 0..1 | Descrição funcional da categoria. |
| `<flowCategoryItems>` | 0..1 | Bloco de itens/Flows associados. |
| `<flowCategoryItem>` | 0..N | Associação a um Flow específico. |
| `<flow>` | 1 (dentro de `<flowCategoryItem>`) | API Name do Flow associado. |
| `<label>` | 1 | Nome amigável da categoria. |

#### Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FlowCategory xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>Flows do time de Vendas</description>
    <flowCategoryItems>
        <flowCategoryItem>
            <flow>Criar_Oportunidade</flow>
        </flowCategoryItem>
        <flowCategoryItem>
            <flow>Atualizar_Lead</flow>
        </flowCategoryItem>
    </flowCategoryItems>
    <label>Vendas</label>
</FlowCategory>
```

### 3.2 Objeto interno via API padrão / Tooling

- `FlowCategoryView` pode estar disponível via SOQL para listar categorias e Flows.
- Tooling API: `SELECT Id, FullName, DeveloperName, Metadata FROM FlowCategory`.

### 3.3 Configuração observável em outras fontes

- UI de Setup / Flow Builder.
- `SetupAuditTrail` para alterações.

---

## 4. Consultas e formas de extração

### SOQL exemplo

```sql
SELECT Id, ApiName, Label, Description
FROM FlowCategoryView
ORDER BY Label
```

```sql
SELECT Id, Name, NamespacePrefix
FROM FlowCategory
ORDER BY Name
```

---

## 5. Boas práticas e pontos de atenção

- Usar nomes claros e consistentes de categorias.
- Não confundir classificação com permissão ou execução.
- Manter categorias atualizadas quando Flows são criados, renomeados ou desativados.
- Documentar a finalidade de cada categoria.
- Evitar duplicidade de Flows em categorias conflitantes.

---

## 6. Links de referência oficial

- [Salesforce Help — Organize Flows](https://help.salesforce.com/s/articleView?id=sf.flow_create.htm)
- [Salesforce Developer — FlowCategory Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flowcategory.htm)
