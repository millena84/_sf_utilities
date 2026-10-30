# Fase 0 — Completar termos genéricos

Complete `fase0/termos_genericos_proposto.csv` com termos genéricos candidatos, seguindo estas regras:

1. Considere esta lista de candidatos:
   - **sufixos técnicos de Apex:** service, svc, handler, helper, util, utils, controller, ctrl, impl, base, abstract, factory, selector, domain;
   - **execução:** trigger, trg, batch, queueable, schedulable, sched, job, future, async;
   - **teste:** test, tst, mock, fake, stub;
   - **estrutura de dados:** wrapper, dto, vo, request, response, req, resp, payload, json, parser;
   - **integração genérica:** integration, integracao, int, callout, http, client, api, rest, ws;
   - **Salesforce genérico:** custom, record, object, field, page, component, cmp, lwc, flow, process;
   - **ruído:** aux, temp, tmp, new, old, novo, v1, v2, copy;
   - **prefixo usado em toda a org:** se houver um prefixo presente em mais de 30% dos nomes de componentes, inclua-o.
2. Inclua um candidato **somente se** ele existir em `fase0/org_lexicon.csv`. Preencha `qtd_componentes` com a contagem do léxico.
3. **Nunca** inclua: siglas da coluna `sigla` do `assuntos.csv`, nomes de sistemas externos, ou termos presentes em `termos_nucleo` ou `sinonimos` de `fase0/glossario_proposto.csv`. Liste os candidatos barrados por essa regra, com o motivo.
4. Nas linhas que **já existiam**, se algum termo violar a regra 3, mantenha a linha e escreva no `motivo`: "ATENÇÃO: termo de negócio/sigla/sistema — recomenda-se rejeitar".
5. Linhas novas: `status_revisao = pendente` e `motivo` = "candidato sugerido na revisão (categoria: <categoria>)".
6. Não crie nem altere o `termos_genericos_aprovado.csv`.

Ao final, mostre: quantas linhas foram acrescentadas, quantos candidatos não existem no léxico, quantos foram barrados pela regra 3 (com o motivo) e quais linhas antigas receberam o aviso. Registre em `decisions.md`.
