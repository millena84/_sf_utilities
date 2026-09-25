# Prompt — CompactLayout

## 1. Contexto do componente

### 1.1 O que é
`CompactLayout` (nome funcional: **Compact Layout** ou **Layout Compacto**) é um metadata type do Salesforce que define quais campos aparecem no cartão de destaque (record highlight panel) de um registro, especialmente na experiência Lightning. Ele oferece uma visualização resumida dos dados mais importantes de um objeto em telas pequenas, no topo de páginas de registro, em listas relacionadas e em componentes mobile.

Na prática, um `CompactLayout`:
- pertence a um objeto (`CustomObject` ou objeto standard);
- lista até 10 campos (recomendado: os mais relevantes);
- pode ser o layout compacto principal do objeto;
- impacta Lightning Experience, mobile app e Experience Cloud;
- é complementar ao `Page Layout` e ao `FlexiPage`, não substitui.

### 1.2 Para que serve
- Destacar campos essenciais no topo do registro.
- Melhorar a experiência mobile e Lightning.
- Padronizar o resumo visual de registros por objeto.
- Facilitar a identificação rápida de informações.

### 1.3 Cenários típicos de uso
- Mostrar Nome, Conta, Valor e Fase em oportunidades.
- Exibir Número do Caso, Status e Prioridade no topo de cases.
- Destacar Nome, Telefone e Email de contatos na lista de relacionados.

### 1.4 Clouds / contextos
- **Salesforce Core** — todos os objetos com suporte.
- **Sales Cloud** — Opportunity, Account, Contact, Lead.
- **Service Cloud** — Case, Contact, Asset.
- **Experience Cloud / Mobile** — principal ponto de uso.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `CompactLayout`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Compact Layout / Layout Compacto |
| Metadata type exact | `CompactLayout` |
| Pasta no projeto SFDX | `objects/<ObjectName>/compactLayouts/` |
| Arquivo padrão | `<apiName>.compactLayout-meta.xml` |
| Objeto interno (API padrão) | Não consultável diretamente via SOQL |
| Objeto interno (Tooling API) | `CompactLayout` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Limitado |
| Acessível por Tooling API | Sim — `Metadata` |
| Acessível por Apex | Não |
| Acessível por UI | Sim — **Setup → Object Manager → [Objeto] → Compact Layouts** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Objeto | `CustomObject` / `EntityDefinition` | Objeto ao qual o layout pertence. |
| Campos | `CustomField`, `FieldDefinition` | Campos exibidos. |
| Page Layout | `Layout` | Layout principal do registro. |
| Flexi Page | `FlexiPage` | Página Lightning que usa o layout. |
| Lightning Record Page | `FlexiPage` | Componente highlight panel. |

### 2.3 Matriz de acessibilidade

| Fonte | CompactLayout metadata | Tooling | Setup/UI |
|---|---|---|---|
| Name / fullName | Sim | Sim | Sim |
| Objeto | Sim | Sim | Sim |
| Campos | `<fields>` | `Metadata` | Sim |
| Layout padrão do objeto | `<compactLayoutAssignment>` no objeto | — | Setup |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`CompactLayout`)

Arquivo típico: `objects/<Objeto>/compactLayouts/<API_Name>.compactLayout-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<fullName>` | 1 | API Name. |
| `<label>` | 1 | Label. |
| `<fields>` | 0..N | Campos exibidos (em ordem). |

#### Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CompactLayout xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>CompactoOportunidade</fullName>
    <label>Layout Compacto de Oportunidade</label>
    <fields>Name</fields>
    <fields>AccountId</fields>
    <fields>Amount</fields>
    <fields>StageName</fields>
    <fields>CloseDate</fields>
</CompactLayout>
```

### 3.2 Layout padrão no objeto

No `CustomObject` metadata:

```xml
<compactLayoutAssignment>CompactoOportunidade</compactLayoutAssignment>
```

### 3.3 Tooling API

```sql
SELECT Id, DeveloperName, TableEnumOrId, Metadata
FROM CompactLayout
WHERE TableEnumOrId = 'Opportunity'
ORDER BY DeveloperName
```

---

### 3.4 Configuração observável em outras fontes

- Setup → Object Manager → Objeto → Compact Layouts.
- Lightning Record Page → highlight panel.
- Salesforce Mobile app.

---

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Ordem dos campos | XML metadata / Tooling | SOQL padrão | Requer metadata/Tooling. |
| Visibilidade por perfil | Layout/Profile assignment | `CompactLayout` | Requer análise de permissões. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `CustomObject`

- Objeto pai e configuração do layout compacto padrão.

### 4.2 `CustomField`

- Campos referenciados no layout.

### 4.3 `FlexiPage` / `Layout`

- Páginas Lightning e page layouts onde o compact layout aparece.

---

## 5. Consultas e formas de extração

### 5.1 Compact layouts por objeto (Tooling)

```sql
SELECT Id, DeveloperName, TableEnumOrId, Metadata
FROM CompactLayout
ORDER BY TableEnumOrId, DeveloperName
```

### 5.2 Campos de um compact layout
Extrair via XML metadata ou Tooling `Metadata`:

```bash
grep -A 20 "<fullName>CompactoOportunidade</fullName>" \
  force-app/main/default/objects/Opportunity/compactLayouts/*.xml
```

### 5.3 Objeto e seu layout compacto padrão

Analisar `<compactLayoutAssignment>` no arquivo `objects/<Object>/<Object>.object-meta.xml`.

---

## 6. Boas práticas e pontos de atenção

- **Use até 10 campos**, priorizando os mais relevantes.
- **Inclua campos identificadores** (nome, número) e indicadores de status.
- **Considere a experiência mobile** ao escolher campos.
- **Mantenha consistência** entre compact layout e page layout.
- **Valide segurança de campo (FLS)**: campos ocultos aparecerão vazios.
- **Documente a escolha dos campos**.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Evite campos muito longos ou complexos** que prejudiquem a leitura.

---

## 7. Links de referência oficial

- [Salesforce Help — Compact Layouts](https://help.salesforce.com/s/articleView?id=sf.compact_layout_overview.htm)
- [Salesforce Developer — CompactLayout Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_compactlayout.htm)
