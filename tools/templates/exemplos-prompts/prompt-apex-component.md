# Prompt — ApexComponent

## 1. Contexto do componente

### 1.1 O que é
`ApexComponent` (nome funcional: **Visualforce Component** ou **Componente Visualforce**) é um metadata type do Salesforce que define um componente reutilizável escrito na sintaxe do Visualforce (uma marcação específica do Salesforce, semelhante ao HTML com tags `apex:`). Ele encapsula trechos de interface, lógica de controller e atributos, podendo ser reutilizado em múltiplas páginas Visualforce.

Na prática, um `ApexComponent`:
- é definido em `components/<API_Name>.component` com metadata `components/<API_Name>.component-meta.xml`;
- pode ter um controller próprio (`<apex:component controller="MinhaClasse"`);
- pode expor atributos (`<apex:attribute>`) para receber parâmetros de páginas pai;
- é executado no lado do servidor, gerando HTML, JavaScript, CSS ou outro output para o navegador;
- pode conter lógica Apex através do controller e expressions `{!...}`.

### 1.2 Para que serve
- Reutilizar trechos de interface em várias páginas Visualforce.
- Encapsular componentes complexos (cabeçalhos, rodapés, tabelas, widgets).
- Separar responsabilidades entre página principal e componentes.
- Expor dados de forma modular e parametrizada.

### 1.3 Cenários típicos de uso
- Cabeçalho de documento com dados dinâmicos.
- Componente de lista de oportunidades reutilizável.
- Widget de KPIs exibido em múltiplas páginas.
- Componente de busca/filtro parametrizado.

### 1.4 Clouds / contextos
- **Salesforce Core** — extensão de páginas Visualforce.
- **Experience Cloud** — pode ser exposto em sites/comunidades.
- **Sales/Service Cloud** — páginas customizadas para usuários internos.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ApexComponent`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Visualforce Component / Componente |
| Metadata type exact | `ApexComponent` |
| Pasta no projeto SFDX | `components/` |
| Arquivo padrão | `<apiName>.component` + `<apiName>.component-meta.xml` |
| Objeto interno (API padrão) | `ApexComponent` |
| Objeto interno (Tooling API) | `ApexComponent` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ApexComponent` |
| Acessível por Tooling API | Sim |
| Acessível por Apex | Sim — `ApexComponent` é consultável |
| Acessível por UI | Sim — **Setup → Visualforce Components** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Visualforce Page | `ApexPage` | Páginas que consomem o componente. |
| Apex Controller | `ApexClass` | Controller opcional do componente. |
| Static Resource | `StaticResource` | CSS/JS/imagens usados. |
| Custom Object | `CustomObject` | Objetos referenciados. |
| Custom Field | `CustomField` | Campos exibidos/manipulados. |
| Permission Set / Profile | `PermissionSet`, `Profile` | Acesso às páginas e objetos. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | ApexComponent metadata | Objeto SOQL | Tooling | Setup/UI |
|---|---|---|---|---|
| Name / API name | Sim | `Name` | Sim | Sim |
| Controller | `<apex:component controller>` / `ControllerType` | `ControllerKey` | Sim | Setup |
| Atributos | tags `<apex:attribute>` | — | Sim | Source |
| Markup | `.component` | `Markup` | Sim | Setup |
| Versão API | `.component-meta.xml` | `ApiVersion` | Sim | Setup |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura do componente Visualforce (`ApexComponent`)

Arquivo típico: `components/<API_Name>.component` + `components/<API_Name>.component-meta.xml`.

#### Tags do `.component-meta.xml`

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<apiVersion>` | 1 | Versão da API. |
| `<description>` | 0..1 | Descrição. |
| `<label>` | 0..1 | Label. |
| `<packageVersions>` | 0..N | Versões de pacotes gerenciados. |

#### Tags principais do `.component`

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<apex:component>` | 1 | Raiz. Pode declarar `controller`, `allowDML`, `language`. |
| `<apex:attribute>` | 0..N | Parâmetros de entrada do componente. |
| `<apex:facet>` | 0..N | Regiões nomeadas customizáveis. |
| `<apex:composition>`, `<apex:include>` | 0..N | Reutilização de templates. |
| Outras tags `apex:` | 0..N | Componentes do Visualforce. |
| HTML/JS/CSS | 0..N | Marcação e estilo customizado. |

#### Exemplo

```html
<apex:component controller="MeuComponenteController">
    <apex:attribute name="recordId" type="Id" required="true" description="ID do registro"/>
    <apex:outputPanel>
        <p>Nome: {!nome}</p>
        <p>ID: {!recordId}</p>
    </apex:outputPanel>
</apex:component>
```

### 3.2 Objeto interno via API padrão: `ApexComponent`

| Campo | Significado prático |
|---|---|
| `Id` | ID do componente. |
| `Name` | Nome/API Name. |
| `NamespacePrefix` | Namespace. |
| `ApiVersion` | Versão da API. |
| `ControllerKey` / `ControllerType` | Identificação do controller. |
| `Markup` | Código Visualforce (XML). |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, Name, NamespacePrefix, ApiVersion, ControllerKey, ControllerType
FROM ApexComponent
ORDER BY Name
```

### 3.3 Tooling API

```sql
SELECT Id, Name, Body, ApiVersion, Metadata
FROM ApexComponent
ORDER BY Name
```

### 3.4 Uso do componente em páginas

Pesquisar no repositório por `<c:NomeDoComponente` ou namespace:

```bash
grep -rl "<c:MeuComponente" force-app/main/default/pages/
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Visualforce Components.
- Código fonte do repositório SFDX.
- `SetupAuditTrail`.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Código mark-up | `.component` / Tooling `Body` | `ApexComponent` SOQL parcial | Tooling retorna Body. |
| Páginas consumidoras | `ApexPage` | `ApexComponent` | Requer search cruzada. |
| Dados expostos | Controller / runtime | Metadata | Requer análise de controller. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ApexPage`

- Páginas que consomem o componente.

### 4.2 `ApexClass`

- Controller do componente.

### 4.3 `StaticResource`

- Recursos estáticos referenciados.

### 4.4 `CustomObject` / `CustomField`

- Dados apresentados/manipulados.

### 4.5 `SetupAuditTrail`

- Rastreia alterações no componente.

---

## 5. Consultas e formas de extração

### 5.1 Todos os componentes

```sql
SELECT Id, Name, NamespacePrefix, ApiVersion, ControllerKey, ControllerType
FROM ApexComponent
ORDER BY Name
```

### 5.2 Componentes com controller

```sql
SELECT Id, Name, ApiVersion, ControllerKey, ControllerType
FROM ApexComponent
WHERE ControllerType != null
ORDER BY Name
```

### 5.3 Componentes sem namespace (locais)

```sql
SELECT Id, Name, ApiVersion
FROM ApexComponent
WHERE NamespacePrefix = null
ORDER BY Name
```

### 5.4 Páginas que consomem um componente

```bash
grep -rl "<c:NomeDoComponente" force-app/main/default/pages/
```

---

## 6. Boas práticas e pontos de atenção

- **Projete componentes genéricos** com atributos bem definidos.
- **Documente cada `<apex:attribute>`** com nome, tipo, obrigatoriedade e descrição.
- **Evite lógica de negócio pesada** no componente — delegue ao controller.
- **Respeite limites de governança** (SOQL, DML) no controller.
- **Prefira componentes pequenos e reutilizáveis** em vez de monolitos.
- **Valide segurança de dados expostos** com FLS e sharing rules.
- **Mantenha controles de versionamento** (API version).
- **Rastreie alterações** via `SetupAuditTrail`.
- **Considere transição para LWC** para novos desenvolvimentos em Lightning Experience.

---

## 7. Links de referência oficial

- [Salesforce Developer — Visualforce Components](https://developer.salesforce.com/docs/atlas.en-us.pages.meta/pages/pages_comp_creating.htm)
- [Salesforce Developer — ApexComponent Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_apexcomponent.htm)
- [Salesforce Developer — apex:component](https://developer.salesforce.com/docs/atlas.en-us.pages.meta/pages/pages_comp_ref_component.htm)
