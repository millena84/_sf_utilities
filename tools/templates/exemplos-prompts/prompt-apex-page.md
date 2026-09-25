# Prompt — ApexPage

## 1. Contexto do componente

### 1.1 O que é
`ApexPage` (nome funcional: **Visualforce Page**) é um metadata type do Salesforce usado para criar páginas web customizadas usando a tecnologia Visualforce. As páginas podem apresentar dados de múltiplos objetos, usar controladores padrão ou personalizados, e serem consumidas no Salesforce Classic, Lightning Experience (via Visualforce Component) ou Experience Cloud.

Na prática, um `ApexPage`:
- é composto por um arquivo `.page` (markup) e um `.page-meta.xml` (metadados);
- pode ter `standardController` (um objeto padrão/custom), `controller` (Apex customizado) ou `extensions`;
- pode ser habilitada/disponibilizada para Salesforce Mobile;
- requer acesso via Permission Set ou Profile;
- pode referenciar componentes Visualforce (`ApexComponent`), Lightning Components (via `apex:includeLightning`) e recursos estáticos.

### 1.2 Para que serve
- Criar interfaces customizadas fora do Lightning App Builder.
- Implementar páginas complexas com lógica Apex customizada.
- Integrar Visualforce com Lightning Components e recursos estáticos.
- Suportar experiências herdadas e relatórios/PDFr customizados.
- Disponibilizar páginas publicamente via Experience Cloud (quando permitido).

### 1.3 Cenários típicos de uso
- Página de wizard multi-step para criação de oportunidade.
- Dashboard alternativo customizado em Visualforce.
- Geração de PDF a partir de registro.
- Página pública de autoatendimento (Experience Cloud).

### 1.4 Clouds / contextos
- **Salesforce Core** — Visualforce.
- **Experience Cloud** — páginas de comunidade.
- **Sales/Service Cloud** — páginas customizadas de registro.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ApexPage`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Visualforce Page / Página do Visualforce |
| Metadata type exact | `ApexPage` |
| Pasta no projeto SFDX | `pages/` |
| Arquivo padrão | `<apiName>.page` + `<apiName>.page-meta.xml` |
| Objeto interno (API padrão) | `ApexPage` |
| Objeto interno (Tooling API) | `ApexPage` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Sim — `SELECT ... FROM ApexPage` |
| Acessível por Tooling API | Sim — inclui campo `Markup` |
| Acessível por Apex | Não diretamente |
| Acessível por UI | Sim — **Setup → Visualforce Pages** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Visualforce Component | `ApexComponent` | Componente reutilizável usado na página. |
| Apex Class | `ApexClass` | Controller customizado ou extensão. |
| Standard/Custom Object | `EntityDefinition` | Controller padrão. |
| Static Resource | `StaticResource` | CSS, JS, imagens. |
| Custom Label | `CustomLabel` | Rótulos traduzíveis. |
| Permission Set / Profile | `PermissionSet`, `Profile` | Controle de acesso. |
| Lightning Component | `LightningComponentBundle` | Incluído via `<apex:includeLightning>`. |
| Tab | `CustomTab` | Página pode ser vinculada a aba. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | ApexPage metadata | `ApexPage` (SOQL) | Tooling | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome / label | Sim | `Name`, `MasterLabel` | Sim | Sim | Sim |
| Markup | Sim (`.page`) | — | `Markup` | Sim | Sim |
| Controller | atributo `controller` | `ControllerType`, `ControllerKey` | Sim | Sim | Sim |
| Standard controller | atributo `standardController` | `Markup` / `ControllerType` | Sim | Sim | Sim |
| Disponível em mobile | `availableInTouch` | `IsAvailableInTouch` | Sim | Sim | Sim |
| Versão da API | `.page-meta.xml` | `ApiVersion` | Sim | Sim | Sim |
| Permissões | via `PermissionSet`/`Profile` | `SetupEntityAccess` (SetupEntityType=ApexPage) | — | Setup | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ApexPage`)

Arquivo típico: `pages/<API_Name>.page` + `pages/<API_Name>.page-meta.xml`.

#### Tags principais do `.page-meta.xml`

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<apiVersion>` | 1 | Versão da API. |
| `<availableInTouch>` | 0..1 | Disponível no Salesforce Mobile. |
| `<confirmationTokenRequired>` | 0..1 | Exige token de confirmação para requisições GET. |
| `<description>` | 0..1 | Descrição. |
| `<label>` | 1 | Nome amigável. |
| `<packageVersions>` | 0..N | Versões de pacotes managed. |

#### Tags principais do `.page`

| Tag | Descrição prática |
|---|---|
| `<apex:page>` | Raiz. Define controller, standardController, extensions, action, title etc. |
| `<apex:form>` | Formulário. |
| `<apex:pageBlock>` | Bloco de layout estilo Salesforce. |
| `<apex:repeat>`, `<apex:dataTable>`, `<apex:pageBlockTable>` | Iteração/tabelas. |
| `<apex:component>` | Uso de componentes. |
| `<apex:includeLightning>` | Incluir Lightning Component. |
| `<apex:stylesheet>`, `<apex:includeScript>` | Recursos estáticos. |

#### Exemplo

```html
<apex:page controller="MeuController" title="Minha Página">
    <apex:form>
        <apex:pageBlock title="Dados">
            <apex:pageBlockSection>
                <apex:outputText value="{!mensagem}" />
            </apex:pageBlockSection>
        </apex:pageBlock>
    </apex:form>
</apex:page>
```

### 3.2 Objeto interno via API padrão: `ApexPage`

| Campo | Significado prático |
|---|---|
| `Id` | ID da página. |
| `Name` | API Name. |
| `MasterLabel` | Label. |
| `ApiVersion` | Versão da API. |
| `ControllerType` | Tipo de controller. |
| `ControllerKey` | Nome do controller. |
| `IsAvailableInTouch` | Disponível em mobile. |
| `Markup` | Corpo (Tooling API). |
| `CreatedDate`, `LastModifiedDate` | Rastreabilidade. |

#### Exemplo de query

```sql
SELECT Id, Name, MasterLabel, ApiVersion, ControllerType, ControllerKey,
       IsAvailableInTouch, CreatedDate, LastModifiedDate,
       CreatedBy.Name, LastModifiedBy.Name
FROM ApexPage
ORDER BY Name
```

### 3.3 Tooling API — markup

```sql
SELECT Id, Name, MasterLabel, Markup, ApiVersion, ControllerType, ControllerKey,
       IsAvailableInTouch
FROM ApexPage
ORDER BY Name
```

### 3.4 Permissões de acesso

```sql
SELECT ParentId, Parent.Name, SetupEntityId, SetupEntityType
FROM SetupEntityAccess
WHERE SetupEntityType = 'ApexPage'
ORDER BY SetupEntityId
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Visualforce Pages.
- Permission Sets / Profiles → Visualforce Page Access.
- Custom Tabs vinculadas.
- SetupAuditTrail.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Markup completo | Arquivo `.page` / Tooling `Markup` | `ApexPage` SOQL padrão | Requer Tooling/metadata. |
| Dados renderizados | Runtime | Metadata | Estado de execução. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ApexComponent`

- Componentes reutilizáveis usados dentro da página.

### 4.2 `ApexClass`

- Controller customizado ou extensão.

### 4.3 `StaticResource`

- Recursos auxiliares (CSS, JS, imagens).

### 4.4 `PermissionSet` / `Profile`

- Controlam quem pode acessar a página.

### 4.5 `CustomTab`

- Página pode ser exposta como aba.

---

## 5. Consultas e formas de extração

### 5.1 Páginas Apex

```sql
SELECT Id, Name, MasterLabel, ApiVersion, ControllerType, ControllerKey,
       IsAvailableInTouch, CreatedDate, LastModifiedDate,
       CreatedBy.Name, LastModifiedBy.Name
FROM ApexPage
ORDER BY Name
```

### 5.2 Páginas com controller customizado

```sql
SELECT Id, Name, MasterLabel, ControllerKey, ApiVersion, IsAvailableInTouch
FROM ApexPage
WHERE ControllerType = '1'
ORDER BY ControllerKey
```

### 5.3 Permissões de acesso

```sql
SELECT Parent.Name, Parent.Type, SetupEntityId, SetupEntity.Name
FROM SetupEntityAccess
WHERE SetupEntityType = 'ApexPage'
ORDER BY SetupEntity.Name
```

### 5.4 Uso de componentes em páginas

```bash
grep -rl "<c:" force-app/main/default/pages/
```

---

## 6. Boas práticas e pontos de atenção

- **Prefira Lightning Web Components (LWC)** para desenvolvimentos novos.
- **Documente o propósito** da página no campo `description`.
- **Restrinja acesso** usando Permission Sets e Profiles de forma mínima necessária.
- **Evite lógica complexa** no markup; use controllers bem estruturados.
- **Valide inputs** e use `escape` para prevenir XSS.
- **Otimize consultas** no controller para evitar view state grande.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Considere mobile** ao definir `availableInTouch`.
- **Evite referências hardcoded** a URLs e IDs em Visualforce.

---

## 7. Links de referência oficial

- [Salesforce Help — Visualforce Pages](https://developer.salesforce.com/docs/atlas.en-us.pages.meta/pages/pages_intro.htm)
- [Salesforce Developer — ApexPage Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_apexpage.htm)
- [Salesforce Developer — Standard Controllers](https://developer.salesforce.com/docs/atlas.en-us.pages.meta/pages/pages_controller_sosc.htm)
- [Salesforce Developer — Custom Controllers and Extensions](https://developer.salesforce.com/docs/atlas.en-us.pages.meta/pages/pages_controller.htm)
