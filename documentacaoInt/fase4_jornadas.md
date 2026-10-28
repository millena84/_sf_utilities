# Fase 4 — Jornadas de integração (org <ORG>, assunto <ID_ASSUNTO>)

> Execute **uma sessão por assunto** (no máximo 3 assuntos por sessão, se forem pequenos).

## Antes de começar
Leia e siga integralmente `<DIR_TRABALHO>/_projeto/00_regras_gerais.md` e `<DIR_TRABALHO>/_projeto/template_jornada.md`.

## Parâmetros desta execução
- ORG: `<ORG>` · CAMINHO_ORG: `<CAMINHO_ORG>` · DIR_TRABALHO: `<DIR_TRABALHO>` · MODO_TESTE: `<sim|não>`
- Assunto(s): `<ID_ASSUNTO>` (ex.: ASS-003)

## Objetivo
Escrever a documentação do assunto como **jornadas**: do gatilho ao resultado, legível para negócio e rastreável para técnicos.

## Insumos
- `fase3/matriz_componente_assunto_aprovado.csv`, `fase3/conflitos_aprovado.csv`
- `fase2/edges.csv`, `fase2/nodes.csv`, `fase2/infra_hubs_aprovado.csv`
- `fase1/integration_points.csv`, `fase1/sistemas_externos_aprovado.csv`
- `fase0/inventory.csv`, `fase0/glossario_aprovado.csv`
- Código-fonte em `CAMINHO_ORG` (leitura para entender o comportamento)

## P. Pré-checagem
- Assunto existe no glossário aprovado e tem ≥1 componente ALTA/MEDIA aprovado na matriz.
- Fase 3 aprovada; `_aprovado` sem `pendente` (exceto MODO_TESTE).
- Falhou → `fase4/<ID_ASSUNTO>/PRECHECK_FALHOU.md` e encerre.

## Etapas

### 4.1 Recorte
- Núcleo: componentes ALTA aprovados. Apoio: MEDIA aprovados. Possivelmente relacionados: BAIXA (só em apêndice).
- INFRA/HUB_DADOS: apenas citados, com link para o catálogo de infraestrutura (fase 5).
- `fase4/<ID_ASSUNTO>/recorte.csv` `componente_id,papel(nucleo|apoio|possivel|infra),confianca`

### 4.2 Gatilhos e resultados
Identifique o que inicia cada jornada:
- INBOUND: endpoint exposto (classe REST/SOAP, e-mail, API padrão presumida).
- OUTBOUND: trigger em objeto, Flow record-triggered, agendamento (Schedulable/Batch), ação de usuário (LWC/Aura/Visualforce/botão), Platform Event.
Cada par gatilho → resultado distinto é **uma jornada** (ex.: "Gerar QR Code" e "Receber confirmação de pagamento" são duas jornadas do mesmo assunto).

`fase4/<ID_ASSUNTO>/jornadas.csv` `id_jornada,nome,gatilho,componente_gatilho,resultado,direcao,sistemas_externos`

### 4.3 Reconstrução das etapas
Para cada jornada, percorra o grafo a partir do gatilho e **leia o código** para ordenar as etapas:
- Marque cada etapa como síncrona ou assíncrona (`@future`, Queueable, Batch, Schedulable, Platform Event, Outbound Message).
- Registre leitura/escrita de objetos e campos principais, External IDs, configurações (Named Credential, Custom Metadata, Custom Setting — só nomes).
- Registre tratamento de erro: try/catch, objetos/classes de log, retentativas, reprocessamento.
- Transição entre etapas sem aresta no grafo → [INFERIDO] com justificativa.

`fase4/<ID_ASSUNTO>/etapas.csv`
`id_jornada,ordem,descricao,componente_id,sync_async,aresta_suporte(id_regra|INFERIDO),evidencia,confianca`

### 4.4 Documentação
Siga **exatamente** o `template_jornada.md`. Gere:
- `docs/jornadas/<ID_ASSUNTO>_<slug>/README.md` — visão do assunto (lista de jornadas, sistemas, mapa geral)
- `docs/jornadas/<ID_ASSUNTO>_<slug>/<id_jornada>_<slug>.md` — uma por jornada

Regras de escrita:
- "Resumo de negócio" sem nomes técnicos (sem nomes de API, sem `__c`), em frases curtas.
- Seção sem conteúdo identificado → escrever "Não identificado na base analisada." (nunca deixar vazia).
- Diagramas Mermaid: `flowchart LR` (visão geral) e `sequenceDiagram` (detalhe), com rótulos curtos.

### 4.5 Material de revisão humana (`fase4/<ID_ASSUNTO>/revisao/`)
- `amostra_etapas.csv` — 3 etapas por jornada com `trecho_da_linha,ok,comentario`
- `inferidos.csv` — todos os [INFERIDO] com justificativa, `ok,comentario`
- `possiveis.csv` — componentes BAIXA com `promover(sim|não),comentario`

## Autovalidação — `tools/fase4/validate_fase4.py <ID_ASSUNTO>`

| ID | Verificação | Severidade |
|---|---|---|
| F4-A01 | Pré-checagem executada e aprovada | BLOQUEANTE |
| F4-A02 | Todo componente citado nos docs existe no inventário e está no recorte (ou justificado como externo ao recorte) | BLOQUEANTE |
| F4-A03 | Fechamento: todo componente núcleo é citado em alguma jornada ou listado em "Componentes não utilizados nas jornadas" com motivo | BLOQUEANTE |
| F4-A04 | Fechamento: todo ponto de integração do recorte aparece em ≥1 etapa | BLOQUEANTE |
| F4-A05 | Toda etapa tem evidência; reverificação de 100% das evidências | BLOQUEANTE |
| F4-A06 | Toda transição entre etapas consecutivas tem aresta em `edges.csv` ou marca [INFERIDO] | BLOQUEANTE |
| F4-A07 | Todas as seções do template presentes e não vazias | BLOQUEANTE |
| F4-A08 | "Resumo de negócio" sem nomes de API (regex: `__c`, `__e`, `__mdt`, CamelCase técnico) | ALERTA |
| F4-A09 | Mermaid estruturalmente válido; participantes do sequenceDiagram correspondem às etapas | BLOQUEANTE |
| F4-A10 | Links internos dos docs resolvem para arquivos existentes | BLOQUEANTE |
| F4-A11 | Quantidade de [INFERIDO] por jornada reportada; >30% das etapas | ALERTA |
| F4-A12 | Nenhum segredo; hosts só com domínio | BLOQUEANTE |
| F4-A13 | Idempotência dos CSVs | BLOQUEANTE |

## Entrega
Docs + CSVs + `fase4/<ID_ASSUNTO>/validation_report.md` + `fase4/<ID_ASSUNTO>/RESUMO.md`.
Atualize `decisions.md` e `questions.md`.
