# Prompt — ApexEmailNotifications

## 1. Contexto do componente

### 1.1 O que é
`ApexEmailNotifications` (nome funcional: **Apex Email Notifications** ou **Notificações por Email Apex**) é uma configuração de nível de org do Salesforce que define para quais destinatários serão enviados emails automáticos quando ocorrerem falhas não tratadas em Apex (uncaught exceptions). Essas notificações ajudam equipes de desenvolvimento e operações a detectar erros em produção sem depender exclusivamente de monitoramento manual de debug logs.

Na prática, `ApexEmailNotifications`:
- é uma configuração de setup, geralmente única por org;
- lista um ou mais endereços de email para alerta de erros Apex;
- pode ser configurada por usuário, email externo ou via Apex Exception Email no Setup;
- trabalha em conjunto com `ApexClass`, `ApexTrigger` e `EmailTemplate`;
- não envolve templates customizados diretamente — a mensagem é gerada pela plataforma;
- complementa logs e eventos de monitoramento (Transaction Security, Event Monitoring).

### 1.2 Para que serve
- Notificar responsáveis sobre exceções não tratadas em Apex.
- Detectar rapidamente falhas em produção.
- Suportar resposta incidente em automações críticas.
- Reduzir tempo de descoberta de erros de runtime.

### 1.3 Cenários típicos de uso
- Receber alerta quando uma trigger gera exceção de governança.
- Notificar equipe sobre fallback de callout em integrações críticas.
- Monitorar jobs schedulables/queueables que falham silenciosamente.

### 1.4 Clouds / contextos
- **Salesforce Core** — setup e monitoramento de erros Apex.

---

## 2. Mapa estrutural

### 2.1 Componente principal: `ApexEmailNotifications`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Apex Exception Email / Notificações por Email Apex |
| Metadata type exact | `ApexEmailNotifications` |
| Pasta no projeto SFDX | `apexEmailNotifications/` |
| Arquivo padrão | `apexEmailNotifications/notifications-meta.xml` |
| Objeto interno (API padrão) | Não consultável diretamente via SOQL |
| Objeto interno (Tooling API) | `ApexEmailNotifications` |
| Acessível por Metadata API | Sim — retrieve/deploy |
| Acessível por API padrão / SOQL | Não diretamente |
| Acessível por Tooling API | Sim — метаданные |
| Acessível por Apex | Não |
| Acessível por UI | Sim — **Setup → Apex Exception Email** |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Apex Class | `ApexClass` | Fonte das exceções reportadas. |
| Apex Trigger | `ApexTrigger` | Fonte das exceções reportadas. |
| Email Template | `EmailTemplate` | Configura notificações de outros contextos (não diretamente esta). |
| User | `User` | Pode ser destinatário. |
| Debug Log | `DebugLevel`, `TraceFlag` | Diagnóstico complementar. |
| SetupAuditTrail | `SetupAuditTrail` | Rastreia alterações. |

### 2.3 Matriz de acessibilidade

| Fonte | ApexEmailNotifications metadata | Tooling | Setup/UI |
|---|---|---|---|
| Destinatários | `<apexEmailNotifications>` / `<email>` | Sim | Sim |
| Classes/erros relacionados | — | `ApexClass`, `ApexTrigger` | Setup |
| Histórico de envio | — | `EmailStatus` / logs | Monitor |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`ApexEmailNotifications`)

Arquivo típico: `apexEmailNotifications/notifications-meta.xml`.

#### Tags principais

| Tag | Ocorrência | Descrição prática |
|---|---|---|
| `<apexEmailNotifications>` | 1 | Raiz do arquivo. |
| `<email>` | 0..N | Endereço de email de destino. |
| `<user>` | 0..N | Usuário destinatário (por username). |
| `<enabled>` | 0..1 | Indica se a notificação está ativa. |

#### Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ApexEmailNotifications xmlns="http://soap.sforce.com/2006/04/metadata">
    <email>devops@exemplo.com</email>
    <email>equipe@exemplo.com</email>
    <user>admin.user@exemplo.com</user>
</ApexEmailNotifications>
```

### 3.2 Tooling API

A configuração pode ser recuperada via Tooling API analisando o metadata `ApexEmailNotifications`.

```sql
SELECT Metadata
FROM ApexEmailNotifications
```

> **Nota**: disponibilidade e campos variam conforme versão da Tooling API.

### 3.3 Configuração observável em outras fontes

- Setup → Apex Exception Email.
- `SetupAuditTrail`.
- Emails recebidos de exceções Apex.

---

### 3.4 Campos mascarados, omitidos, protegidos ou irrecuperáveis

| Informação | Onde aparece | Onde NÃO aparece | Observação |
|---|---|---|---|
| Endereços de destino | XML metadata | `SetupEntityAccess` | Trate como dados pessoais. |
| Corpo exato do email | Caixas de entrada | Metadata | Gerado pela plataforma. |
| Logs de exceção | Debug logs | Metadata do componente | Requer perfile de debug. |

---

## 4. Dados relevantes dos componentes relacionados

### 4.1 `ApexClass` / `ApexTrigger`

- Fontes potenciais das exceções reportadas. Uso efetivo depende de execução e erro.

### 4.2 `User`

- Usuários destinatários devem ter email válido e acesso ativo.

### 4.3 `EmailTemplate`

- Embora `ApexEmailNotifications` não use templates customizados, é importante diferenciar de notificações baseadas em `EmailTemplate` (Workflow Alert, Flow, Apex).

### 4.4 `SetupAuditTrail`

- Rastreia alterações nos destinatários de Apex Exception Email.

---

## 5. Consultas e formas de extração

### 5.1 Configuração via Metadata API

O arquivo `apexEmailNotifications/notifications-meta.xml` do repositório SFDX é a fonte principal.

```bash
cat force-app/main/default/apexEmailNotifications/notifications-meta.xml
```

### 5.2 Classes e triggers ativos

```sql
SELECT Id, Name, ApiVersion, Status, IsValid
FROM ApexClass
WHERE Status = 'Active'
ORDER BY Name
```

```sql
SELECT Id, Name, TableEnumOrId, Status, ApiVersion
FROM ApexTrigger
WHERE Status = 'Active'
ORDER BY Name
```

### 5.3 Alterações no Setup

```sql
SELECT Id, Action, Section, CreatedBy.Name, CreatedDate, Display
FROM SetupAuditTrail
WHERE Section LIKE '%Apex Exception%'
   OR Display LIKE '%Apex Email%'
ORDER BY CreatedDate DESC
```

---

## 6. Boas práticas e pontos de atenção

- **Use grupos/dlistas** ao invés de emails pessoais individuais para facilitar manutenção.
- **Não exponha endereços de email** em documentação pública.
- **Inclua destinatários técnicos e responsáveis pela operação**.
- **Combine com monitoramento de debug logs** para diagnóstico completo.
- **Rastreie alterações** via `SetupAuditTrail`.
- **Documente quais classes/triggers críticas** dependem da notificação.
- **Não confunda** `ApexEmailNotifications` com Workflow Email Alerts.
- **Valide emails** periodicamente para evitar devoluções.

---

## 7. Links de referência oficial

- [Salesforce Help — Apex Exception Email](https://help.salesforce.com/s/articleView?id=sf.code_apex_exceptions_email.htm)
- [Salesforce Developer — ApexEmailNotifications Metadata Type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_apexemailnotifications.htm)
- [Salesforce Help — Debug Logs](https://help.salesforce.com/s/articleView?id=sf.code_debug_log.htm)
