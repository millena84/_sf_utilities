# Fase 2 — Grafo de relações (org <ORG>)

## Antes de começar
Leia o `config.json` na raiz da pasta de trabalho e siga integralmente `<DIR_TRABALHO> [busque no arquivo config.json]/_projeto/00_regras_gerais.md`.

## Parâmetros desta execução
- ORG: `<ORG> [busque no arquivo config.json]` · CAMINHO_ORG: `<CAMINHO_ORG> [busque no arquivo config.json]` · DIR_TRABALHO: `<DIR_TRABALHO> [busque no arquivo config.json]` · MODO_TESTE: `<MODO_TESTE> [busque no arquivo config.json]`

## Objetivo
Aplicar as regras de relação aprovadas sobre **todo** o inventário, ligar os pontos de integração aos sistemas externos
e identificar **infraestrutura** e **hubs de dados**, que não podem propagar assunto na fase 3.

> INFRA e HUB_DADOS valem **só para a Fase 3**. O grafo (`edges.csv`) é sempre completo; a Fase 4 o usa **sem esse filtro** para montar a documentação.

## Esta fase NÃO faz
- Não atribui assuntos.

## Insumos
- `fase0/inventory.csv`, `fase0/relation_rules_aprovado.csv`, `fase0/relation_sample.csv`
- `fase1/integration_points.csv`, `fase1/sistemas_externos_aprovado.csv`
- `fase1/validation_report.md`

## P. Pré-checagem
- Insumos existem, colunas esperadas, `_aprovado` sem `pendente` (exceto MODO_TESTE).
- `fase1/validation_report.md` aprovado.
- Falhou → `fase2/PRECHECK_FALHOU.md` e encerre.

## Etapas

### 2.1 Arestas
- Leia as regras **a cada execução** a partir do arquivo de regras (`_aprovado`, ou `_proposto` em MODO_TESTE). Se houver regra nova ou alterada desde a última execução, **implemente-a no extrator antes de rodar**. Não reaproveite scripts que tenham as regras fixas no código.
- Aplique cada regra aprovada a todos os componentes do inventário (exceto `is_test=true`, que só entram em `test_edges.csv`).
- Para cada ponto de integração, crie aresta `componente → SIS::<id>` (OUTBOUND) ou `SIS::<id> → componente` (INBOUND/INBOUND_PRESUMIDO); EVENTO conforme publicação/assinatura.
- Remova duplicatas exatas; mantenha a evidência mais forte.
- Use `_projeto/base_de_conhecimento/regras_ligacao.md` como fonte de regras candidatas: regras `documentado` que faltarem no arquivo de regras aprovado vão para `fase2/regras_sugeridas_base.csv` (`id_base,de,para,como_seguir,tipo`) para revisão humana; **não** as aplique sem aprovação. Regras `heurística` geram no máximo arestas de confiança MEDIA.

**Saídas:**
- `fase2/edges.csv` `origem,destino,id_regra,natureza,evidencia`
- `fase2/test_edges.csv` (mesmo formato)
- `fase2/unresolved_refs.csv` — agregado por nome referenciado, no mesmo formato da Fase 0 (`referencia_textual,categoria,qtd_ocorrencias,qtd_componentes_origem,exemplos_origem,id_regra,motivo_provavel`)

### 2.2 Métricas por nó
`fase2/nodes.csv`
`id,tipo,fan_in,fan_out,is_integration_point,sistemas_externos,distancia_ponto_integracao,isolado,so_referenciado_por_teste`
- `distancia_ponto_integracao`: menor nº de saltos (em qualquer direção) até um ponto de integração; sem caminho → vazio.

### 2.3 Infraestrutura e hubs de dados
Proponha, com justificativa:
- **INFRA**: fan-in ≥ `LIMIAR_INFRA_FAN_IN` + nome com termos genéricos aprovados ou sem referência a objetos de negócio (logger, wrappers HTTP, trigger handlers, utils).
- **HUB_DADOS**: objetos/campos com fan-in ≥ `LIMIAR_INFRA_FAN_IN` (ex.: Account, Contact, Case, User).

- **ACESSO**: Profiles, Permission Sets e Permission Set Groups são classificados automaticamente como ACESSO (sem necessidade de revisão). Suas arestas (natureza `acesso`) ficam no grafo para a documentação, mas **nunca propagam assunto**.

`fase2/infra_hubs_proposto.csv`
`id,classificacao(INFRA|HUB_DADOS),fan_in,motivo,exemplos_de_quem_usa,status_revisao,comentario_revisao`

### 2.4 Material de revisão humana (`fase2/revisao/`, seed=42)
- `amostra_arestas.csv` — 1 aresta de cada regra aplicada (mínimo `AMOSTRA_REVISAO`), estratificada por regra e natureza, com `trecho_da_linha,ok,comentario`
- `vizinhanca_pontos.md` — para os 3 pontos de integração de maior grau: diagrama Mermaid `flowchart LR` com vizinhança de 2 saltos (sem INFRA/HUB), com legenda
- `amostra_isolados.csv` — `AMOSTRA_REVISAO` componentes isolados com `ok,comentario` (isolado de verdade?)
- `top_nao_resolvidas.csv` — 20 mais frequentes
- `diagnostico.md` — leitura obrigatória antes da revisão:
  1. Referências não resolvidas: as 30 mais frequentes (com contagem); distribuição por `motivo_provavel` e por `id_regra`; quantas são nativas do Apex ou do Salesforce (namespaces `System`, `Schema`, `Database`, tipos primitivos, coleções, objetos padrão) × quantas têm cara de customizadas (`__c`, `__mdt`, `__e`, `__x`, nomes com prefixo do projeto).
  2. Nós isolados por tipo de metadata (contagem e %) e lista das `ApexClass`, `ApexTrigger` e `Flow` isolados que não são de teste.
  3. Propostas de `infra_hubs_proposto.csv` agrupadas por classificação e tipo de metadata, com fan-in mínimo, médio e máximo.
  4. Conclusão: "grafo consistente" ou "suspeita de regra faltando/ampla demais", com a justificativa.

## Autovalidação — `tools/fase2/validate_fase2.py`

| ID | Verificação | Severidade |
|---|---|---|
| F2-A01 | Pré-checagem executada e aprovada | BLOQUEANTE |
| F2-A02 | Toda regra `aprovado`/`ajustado` do arquivo de regras tem código correspondente no extrator e foi aplicada; o relatório traz uma **tabela de arestas por `id_regra`** (inclusive as com 0, explicando se o padrão não ocorre na org ou se há falha) | BLOQUEANTE |
| F2-A03 | Origem e destino de toda aresta existem no inventário ou são `SIS::` aprovados | BLOQUEANTE |
| F2-A04 | Reverificação de evidência em amostra de 50 arestas (seed=42): 100% válidas | BLOQUEANTE |
| F2-A05 | Regressão: toda relação de `fase0/relation_sample.csv` (de regras aprovadas) está em `edges.csv` | BLOQUEANTE |
| F2-A06 | Todo ponto de integração tem aresta para/de um `SIS::` | BLOQUEANTE |
| F2-A07 | Sem arestas duplicadas; auto-referências listadas | ALERTA |
| F2-A08 | Métricas de `nodes.csv` recalculáveis a partir de `edges.csv` | BLOQUEANTE |
| F2-A09 | Taxa de não resolvidas sobre nomes distintos da categoria `customizado` acima de `ALERTA_REFS_NAO_RESOLVIDAS` | ALERTA |
| F2-A10 | % de componentes isolados e % sem caminho até ponto de integração reportados | ALERTA |
| F2-A11 | Nenhum segredo nos artefatos | BLOQUEANTE |
| F2-A12 | CSVs bem formados; Mermaid com sintaxe estruturalmente válida (nós declarados, setas válidas) | BLOQUEANTE |
| F2-A13 | Idempotência | BLOQUEANTE |

## Entrega
Arquivos acima + `fase2/graph.json` (nós e arestas, para reuso) + `fase2/validation_report.md` + `fase2/RESUMO_FASE2.md`.
Atualize `decisions.md` e `questions.md`.

### 📝 Arquivos que a revisora altera e salva como `_aprovado`
| Arquivo gerado (`_proposto`) | O que preencher | Salvar como | Exigido por |
|---|---|---|---|
| `fase2/infra_hubs_proposto.csv` | `status_revisao` (na dúvida sobre classe com regra de negócio: `rejeitado`) | `fase2/infra_hubs_aprovado.csv` | Fase 3 |

Opcional: regras de `fase2/regras_sugeridas_base.csv` que você aprovar são acrescentadas em `fase0/relation_rules_aprovado.csv`, e a Fase 2 é rodada de novo.
