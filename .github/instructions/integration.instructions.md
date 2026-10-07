---
applyTo: "integration/**,integracoes/**,docs/integration/**,**/*.flow-meta.xml,**/*NamedCredential*.xml,**/*ExternalService*.xml,cdk/**,cloudformation/**,infra/**"
---

# Skill — Avaliação de Integrações AWS ↔ Salesforce

## Objetivo
Avaliar (integrações legadas) ou desenhar (novas integrações) soluções de integração entre AWS, Salesforce e/ou terceiros, com foco em boas práticas de mercado, padrões de integração e identificação explícita de riscos técnicos, de segurança e operacionais.

Este módulo é usado em dois modos:
1. **Modo Avaliação (legado)** — você recebe uma integração existente (código, diagrama, descrição) e precisa auditá-la.
2. **Modo Desenho (nova integração)** — você precisa propor a arquitetura de uma integração ainda não implementada.

Sempre identifique explicitamente em qual dos dois modos está atuando antes de responder.

---

## 1. Taxonomia de Padrões de Integração (use para classificar ou escolher)

| Padrão | Quando usar | Exemplos de implementação |
|---|---|---|
| **Request-Reply (síncrono)** | Resposta imediata necessária, baixo volume, baixa latência tolerável | REST API (Apex REST / API Gateway + Lambda), SOAP API |
| **Fire-and-Forget (assíncrono)** | Não há necessidade de resposta imediata, desacoplamento desejado | Platform Events, SQS, EventBridge, Outbound Message |
| **Batch/ETL** | Grandes volumes, janelas de processamento tolerantes | Bulk API 2.0, AWS Glue, DMS, Data Loader agendado |
| **Pub/Sub orientado a eventos** | Múltiplos consumidores, baixo acoplamento, escalabilidade | Platform Events/Change Data Capture ↔ EventBridge/SNS |
| **API-led Connectivity (camadas)** | Integrações corporativas reutilizáveis e governadas | MuleSoft Anypoint (System/Process/Experience APIs) |
| **Polling** | Sistema de origem não suporta push | Scheduled Flow/Apex Batch consultando API externa |

**Regra:** sempre explicite qual padrão está sendo avaliado/proposto e justifique a escolha com base em volume, latência tolerável, criticidade e acoplamento desejado.

---

## 2. Checklist de Avaliação (Modo Legado) — Boas Práticas e Riscos

Ao avaliar uma integração existente, percorra **todas** as dimensões abaixo e classifique cada uma como 🟢 Adequado / 🟡 Atenção / 🔴 Crítico:

### 2.1 Autenticação e Autorização
- Uso de **OAuth 2.0** (preferencialmente JWT Bearer Flow para server-to-server, Authorization Code para usuário) em vez de usuário/senha fixo.
- Named Credentials / External Credentials usados no Salesforce (nunca endpoint + token hardcoded em Apex).
- Rotação de credenciais/segredos (AWS Secrets Manager / Salesforce Named Credential) e política de expiração.
- Menor privilégio: Connected App e usuário de integração com Permission Set mínimo necessário (não "System Administrator").

### 2.2 Segurança de Dados
- Dados sensíveis (PII, dados de saúde/financeiros) criptografados em trânsito (TLS 1.2+) e em repouso (Shield Platform Encryption / KMS).
- Mascaramento/minimização de dados trafegados (enviar só os campos necessários).
- Conformidade com LGPD/GDPR/HIPAA quando aplicável (base legal para o tráfego de dados entre sistemas).

### 2.3 Resiliência e Tratamento de Erros
- **Retry com backoff exponencial** implementado do lado que consome a integração.
- **Idempotência** garantida (chave de deduplicação) para evitar duplicação em reprocessamentos.
- **Dead Letter Queue** (SQS DLQ / Platform Event error handling) para mensagens que falham repetidamente.
- Circuit breaker ou throttling para proteger o sistema de destino em caso de pico/falha.
- Monitoramento e alertas (CloudWatch Alarms / Platform Event subscriptions com log de falhas).

### 2.4 Performance e Limites
- Respeito a **Governor Limits** do Salesforce (callouts síncronos por transação, tamanho de payload, timeout de 120s para Apex callouts).
- Respeito a **limites de API** Salesforce (API calls/24h conforme licença), uso de Bulk API para grandes volumes em vez de REST unitário em loop.
- Respeito a **quotas de serviço AWS** (ex.: throttling de API Gateway, concorrência de Lambda, limites de tamanho de mensagem SQS/SNS).
- Paginação implementada corretamente em sincronizações de grandes volumes.

### 2.5 Acoplamento e Manutenibilidade
- Grau de acoplamento entre sistemas (mudança de schema em um lado quebra o outro?).
- Versionamento de contrato de API (ex.: `/v1/`, `/v2/`) para evitar breaking changes.
- Documentação do contrato de integração (payload, autenticação, SLAs) existente e atualizada.
- Logs estruturados e correlação de transação ponta a ponta (trace ID propagado entre Salesforce e AWS).

### 2.6 Governança e Observabilidade
- Owner/responsável técnico da integração identificado.
- Ambiente de monitoramento ativo (dashboards, alertas de falha, SLA de resposta a incidentes).
- Processo de teste de regressão da integração em mudanças de ambos os lados.

---

## 3. Checklist de Desenho (Modo Nova Integração)

Ao desenhar uma nova integração, responda estas perguntas **antes** de propor a arquitetura (se não souber, pergunte ao usuário/consulte `.github/copilot/context.md`):

1. **Direção do fluxo**: Salesforce → AWS, AWS → Salesforce, ou bidirecional?
2. **Volume e frequência**: quantos registros, com qual periodicidade (tempo real, near-real-time, batch diário)?
3. **Criticidade de negócio**: falha na integração bloqueia um processo de negócio crítico (ex.: venda, atendimento) ou é tolerável?
4. **Necessidade de resposta síncrona**: o processo que dispara a integração precisa aguardar confirmação imediata?
5. **Sensibilidade dos dados**: há PII, dados financeiros ou de saúde envolvidos?
6. **Orçamento/licenciamento**: há MuleSoft disponível, ou a integração deve ser nativa (Apex/Lambda)?

Com base nessas respostas, escolha o padrão da Seção 1 e aplique **todo o checklist da Seção 2** como requisito de design (não apenas de auditoria) — ou seja, a proposta já deve nascer cobrindo autenticação, resiliência, performance e observabilidade.

---

## 4. Formato de Saída — Avaliação de Integração Legada

```
### Integração Avaliada
(nome, sistemas envolvidos, padrão identificado conforme Seção 1)

### Diagrama de Fluxo Atual
(Mermaid ou descrição textual)

### Avaliação por Dimensão
| Dimensão | Status (🟢/🟡/🔴) | Observação |
|---|---|---|
| Autenticação e Autorização | | |
| Segurança de Dados | | |
| Resiliência e Tratamento de Erros | | |
| Performance e Limites | | |
| Acoplamento e Manutenibilidade | | |
| Governança e Observabilidade | | |

### Riscos Críticos (🔴) — Ação Imediata Recomendada
### Riscos de Atenção (🟡) — Ação de Médio Prazo
### Pontos Fortes (🟢)
### Plano de Remediação Priorizado (Alta/Média/Baixa)
```

## 5. Formato de Saída — Desenho de Nova Integração

```
### Requisitos Levantados
(respostas às 6 perguntas da Seção 3)

### Padrão de Integração Escolhido e Justificativa

### Diagrama de Arquitetura Proposta
(Mermaid ou descrição textual, incluindo componentes AWS e Salesforce)

### Especificação Técnica
- Autenticação:
- Contrato/Payload (alto nível):
- Tratamento de Erros e Retry:
- Observabilidade:

### Riscos Identificados e Mitigações (desde o design)

### Checklist de Prontidão para Implementação
(itens da Seção 2 aplicados como requisitos, marcados como Planejado/Pendente)
```

---

## 6. Regras Específicas

- **Nunca aprove** uma integração (legada ou nova) que use usuário/senha fixo em vez de OAuth 2.0 + Named Credential/Secrets Manager — sinalize sempre como 🔴 Crítico.
- **Sempre verifique Governor Limits** do Salesforce ao avaliar qualquer integração que envolva Apex (callouts síncronos, limite de 120s, limite de heap/CPU).
- **Sempre verifique quotas AWS** relevantes (throttling de API Gateway, concorrência Lambda, limites de SQS/SNS/EventBridge).
- **Latência, acoplamento, resiliência e custo** devem ser mencionados explicitamente em qualquer comparação de opções (alinhado com `.github/instructions/analysis.instructions.md`).
- Leia sempre `.github/copilot/context.md` primeiro — restrições de compliance e SLAs do projeto mudam a priorização dos riscos.
- Se faltar informação para avaliar um risco (ex.: não há visibilidade do mecanismo de retry), declare isso explicitamente em vez de presumir que está correto.
