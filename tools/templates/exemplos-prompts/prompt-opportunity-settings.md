# Prompt — OpportunitySettings

## 1. Contexto do componente

### 1.1 O que é
`OpportunitySettings` (nome funcional: **Opportunity Settings** ou **Configurações de Oportunidade**) é um metadata type de configuração da org que controla comportamentos globais do objeto `Opportunity`, incluindo validação de montantes de linhas de itens de oportunidade, limitação de produtos e regras de privacidade de oportunidades.

Na prática, `OpportunitySettings`:
- é um arquivo único de configuração org-wide (`settings/Opportunity.settings-meta.xml`);
- afeta diretamente vendas, cálculo de receita e oportunidades;
- é editável via **Setup → Opportunity Settings**;
- impacta todos os usuários da org;
- não é repetível por perfil — é global.

### 1.2 Para que serve
- Validar se o valor da oportunidade corresponde soma de Opportunity Line Items.
- Limitar produtos por oportunidade ou por schedule.
- Controlar a visibilidade/privacidade de oportunidades private vs. public.

### 1.3 Cenários típicos de uso
- Garantir integridade entre cabeçalho e itens da oportunidade.
- Habilitar schedules de produtos.
- Configurar timeout de atualização de montantes.

### 1.4 Clouds / contextos
- **Sales Cloud** — objeto Opportunity, vendas.
- **Salesforce Core** — configuração global da org.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `OpportunitySettings`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Opportunity Settings |
| Metadata type exact | `OpportunitySettings` |
| Pasta no projeto SFDX | `settings/` |
| Arquivo padrão | `Opportunity.settings-meta.xml` |
| Objeto interno (API padrão) | Não consultável diretamente |
| Objeto interno (Tooling API) | Não |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Não |
| Acessível por Tooling API | Não |
| Acessível por Apex | Não |
| Acessível por UI | Sim — **Setup → Opportunity Settings** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Opportunity | `Opportunity` | Objeto configurado. |
| Opportunity Product | `OpportunityLineItem` | Itens e schedules. |
| Quote | `Quote` | Configuração pode impactar cotação. |
| Forecast | `ForecastingSettings` | Oportunidades alimentam forecast. |
| Products/Pricebooks | `Product2`, `Pricebook2`, `PricebookEntry` | Base de itens de oportunidade. |

### 2.3 Matriz de acessibilidade

| Fonte | OpportunitySettings metadata | Setup/UI |
|---|---|---|
| Enable Opportunity Team | `<enableOpportunityTeam>` | Sim |
| Private/Public opportunities | `<opportunityPrivacyPreference>` | Sim |
| Validate line item amounts | `<validateLineItemAmounts>` | Sim |
| Product schedule settings | `<enableOpportunityLineItemSchedule>` | Sim |
| Prompt users about conflicts | `<promptToConfirmOpportunityStageChanges>` | Setup parcial |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`OpportunitySettings`)

Arquivo típico: `settings/Opportunity.settings-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<enableOpportunityTeam>` | 1 | Ativa Opportunity Teams. |
| `<opportunityPrivacyPreference>` | 1 | `Private` ou `PublicReadOnly`/`PublicReadWrite`. |
| `<validateLineItemAmounts>` | 1 | Valida se Amount = soma dos itens. |
| `<enableOpportunityLineItemSchedule>` | 1 | Habilita schedules em Opportunity Line Items. |
| `<promptToConfirmOpportunityStageChanges>` | 1 | Pede confirmação em mudanças de estágio. |
| `<allowUsersToRelateMultipleContactsToOpportunities>` | 1 | Contact Roles múltiplos. |

### 3.2 Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<OpportunitySettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableOpportunityTeam>true</enableOpportunityTeam>
    <opportunityPrivacyPreference>PublicReadWrite</opportunityPrivacyPreference>
    <validateLineItemAmounts>true</validateLineItemAmounts>
    <enableOpportunityLineItemSchedule>true</enableOpportunityLineItemSchedule>
    <allowUsersToRelateMultipleContactsToOpportunities>true</allowUsersToRelateMultipleContactsToOpportunities>
</OpportunitySettings>
```

### 3.3 Configuração observável na UI

- Setup → Opportunity Settings.
- Setup → Opportunity Team Selling (se habilitado).
- Setup → Contact Roles (se habilitado múltiplo).

---

### 3.4 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Configuração global | settings XML | SOQL/Tooling | Via metadata. |
| Uso por usuários | Setup logs / User permissions | `OpportunitySettings` | Requer auditoria. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `Opportunity`

- Objeto central de vendas.

### 4.2 `OpportunityLineItem`

- Produtos/itens da oportunidade.

### 4.3 `OpportunityTeamMember`

- Habilitado por `enableOpportunityTeam`.

### 4.4 `ForecastingSettings`

- Configuração de forecast pode depender das opções de oportunidade.

---

## 5. Consultas e formas de extração

### 5.1 Metadados via SFDX

```bash
sf project retrieve start -m OpportunitySettings
```

### 5.2 Leitura do XML

```bash
cat force-app/main/default/settings/Opportunity.settings-meta.xml
```

### 5.3 Verificar Opportunity Teams ativos

```sql
SELECT Id, OpportunityId, UserId, TeamMemberRole
FROM OpportunityTeamMember
LIMIT 10
```

### 5.4 Contact Roles em oportunidades

```sql
SELECT Id, OpportunityId, ContactId, Role
FROM OpportunityContactRole
LIMIT 10
```

---

## 6. Boas práticas e pontos de atenção

- **Mantenha `validateLineItemAmounts` consistente** com processos de cotação.
- **Habilite Opportunity Teams apenas se houver necessidade** de colaboração.
- **Defina claramente privacidade padrão** de oportunidades.
- **Documente alterações** em change management.
- **Valide impacto em integrações** (CPQ, ERP) ao alterar validações de montante.
- **Monitore campos obrigatórios** e regras de estágio após alterações.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Alinhe configurações com Forecast** para evitar discrepâncias.

---

## 7. Links de referência oficial

- [Salesforce Help — Opportunity Settings](https://help.salesforce.com/s/articleView?id=sf.opportunities_settings_overview.htm)
- [Salesforce Developer — OpportunitySettings Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_opportunitysettings.htm)
