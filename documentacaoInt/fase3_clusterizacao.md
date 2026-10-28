# Fase 3 — Clusterização por assunto (org <ORG>)

## Antes de começar
Leia e siga integralmente `<DIR_TRABALHO>/_projeto/00_regras_gerais.md`.

## Parâmetros desta execução
- ORG: `<ORG>` · CAMINHO_ORG: `<CAMINHO_ORG>` · DIR_TRABALHO: `<DIR_TRABALHO>` · MODO_TESTE: `<sim|não>`
- Parâmetros de calibração: conforme regras gerais (seção 10), salvo ajuste aqui: `<ajustes ou "nenhum">`

## Objetivo
Associar componentes a assuntos de forma **explicável**: cada associação deve mostrar o caminho que a justifica.

## Esta fase NÃO faz
- Não escreve documentação de jornada.

## Insumos
- `fase0/inventory.csv`, `fase0/glossario_aprovado.csv`, `fase0/termos_genericos_aprovado.csv`
- `fase1/integration_points.csv`, `fase1/sistemas_externos_aprovado.csv`
- `fase2/edges.csv`, `fase2/nodes.csv`, `fase2/infra_hubs_aprovado.csv`
- Opcional: `_entradas/gabarito_<ORG>.csv` (`id_assunto,assunto,componente_id_esperado`)
- Opcional (se esta org for a ORG_DO_MODELO): `_modelo/gabarito_modelo.csv`
- `fase2/validation_report.md`

## P. Pré-checagem
- Insumos obrigatórios existem; `_aprovado` sem `pendente` (exceto MODO_TESTE); fase 2 aprovada.
- Gabarito ausente → registrar ALERTA (não bloqueia).
- Falhou → `fase3/PRECHECK_FALHOU.md` e encerre.

## Etapas

### 3.1 Sementes léxicas
Para cada assunto, pontue cada componente pelos termos aprovados:
- Termo núcleo no nome de API = 1.0; no label = 0.8; na descrição = 0.5.
- Sinônimo = 0.8 × peso acima. Termo ambíguo = 0.5 × peso. Termos genéricos aprovados são ignorados.
- Termo excludente presente → componente **descartado** para aquele assunto.
- Score léxico = maior valor encontrado (máx. 1.0). Semente = score léxico ≥ `LIMIAR_MEDIA`.

`fase3/seeds.csv` `id_assunto,componente_id,score_lexico,termos,onde_casou`

### 3.2 Propagação pelo grafo
- A partir das sementes, propague pelas arestas (ambas as direções) até `MAX_SALTOS`.
- Score propagado = score da semente × `DECAIMENTO`^saltos × (`FATOR_RELACAO_FRACA` para cada aresta dinâmica/textual no caminho).
- **INFRA e HUB_DADOS aprovados podem receber score, mas nunca são intermediários do caminho** (não propagam).
- Arestas de natureza `acesso` (Profiles/Permission Sets) **não propagam** e esses componentes não entram na matriz. Eles são levantados na Fase 4.
- Nós `SIS::` propagam apenas se o sistema já tiver ≥1 ponto de integração com semente do mesmo assunto.
- Score final = max(score léxico, maior score propagado) + 0.1 por semente independente adicional que alcança o componente (máx. 1.0).
- Confiança: ≥ `LIMIAR_ALTA` → ALTA; ≥ `LIMIAR_MEDIA` → MEDIA; abaixo → BAIXA (registrar só se ≥ 0.2).

`fase3/matriz_componente_assunto_proposto.csv`
`id_assunto,componente_id,tipo,score,confianca,origem(semente|propagacao),caminho_explicacao,is_integration_point,classificacao_infra,status_revisao,comentario_revisao`
- `caminho_explicacao`: `semente > aresta(id_regra) > ... > componente`, com os IDs de cada nó.

### 3.3 Conflitos, órfãos e resumo
- `fase3/conflitos_proposto.csv` — componentes com ALTA/MEDIA em ≥2 assuntos:
  `componente_id,assuntos_e_scores,proposta(compartilhado|assunto_principal:<id>),motivo,status_revisao,comentario_revisao`
- `fase3/pontos_orfaos.csv` — pontos de integração sem assunto ALTA/MEDIA:
  `id_ponto,componente_id,sistema_externo_id,direcao,assunto_mais_proximo,score,sugestao(novo_assunto|anexar|ignorar)`
- `fase3/resumo_assuntos.csv`
  `id_assunto,assunto,qtd_alta,qtd_media,qtd_baixa,qtd_pontos_integracao,sistemas_externos,direcoes,pct_do_escopo,alerta`
  (`alerta`: SEM_INTEGRACAO | GIGANTE | SEM_SEMENTE | vazio)
- Se esta org for a ORG_DO_MODELO: converta os nomes de `_modelo/gabarito_modelo.csv` em IDs do inventário → `fase3/gabarito_resolvido.csv` `sigla,assunto,nome_componente,componente_id,resolvido(sim|não|ambiguo)`. Some esse gabarito ao `gabarito_<ORG>.csv`.
- Se houver gabarito: `fase3/recall_gabarito.csv` `id_assunto,componente_id_esperado,origem(time|modelo),encontrado(sim|não),confianca,score`

### 3.4 Material de revisão humana (`fase3/revisao/`, seed=42)
- `amostra_baixa.csv` — `AMOSTRA_REVISAO` associações BAIXA com caminho, `deveria_entrar(sim|não),comentario`
- `amostra_media.csv` — `AMOSTRA_REVISAO` associações MEDIA com caminho, `ok,comentario`
- `mapa_assuntos.md` — por assunto: lista dos componentes ALTA, sistemas externos e um Mermaid `flowchart LR` simplificado

## Autovalidação — `tools/fase3/validate_fase3.py`

| ID | Verificação | Severidade |
|---|---|---|
| F3-A01 | Pré-checagem executada e aprovada | BLOQUEANTE |
| F3-A02 | Todo assunto aprovado tem ≥1 semente ou alerta SEM_SEMENTE | BLOQUEANTE |
| F3-A03 | Todo `caminho_explicacao` é válido: cada passo é uma aresta existente em `edges.csv` | BLOQUEANTE |
| F3-A04 | Nenhum caminho tem INFRA/HUB_DADOS como nó intermediário | BLOQUEANTE |
| F3-A05 | Nenhum componente com termo excludente associado ao respectivo assunto | BLOQUEANTE |
| F3-A06 | Scores e confianças recalculáveis com os parâmetros declarados | BLOQUEANTE |
| F3-A07 | Fechamento: todo ponto de integração está associado (ALTA/MEDIA) a algum assunto ou em `pontos_orfaos.csv` | BLOQUEANTE |
| F3-A08 | Assunto com `pct_do_escopo` > `ALERTA_ASSUNTO_GIGANTE` | ALERTA |
| F3-A09 | Componente ALTA em >3 assuntos (provável infra não aprovada) | ALERTA |
| F3-A10 | Recall do gabarito (se houver) reportado por assunto; recall < 80% | ALERTA |
| F3-A11 | Nenhum componente `is_test=true` na matriz | BLOQUEANTE |
| F3-A12 | Nenhum segredo; CSVs bem formados; Mermaid estruturalmente válido | BLOQUEANTE |
| F3-A13 | Idempotência | BLOQUEANTE |

## Entrega
Arquivos acima + `fase3/validation_report.md` + `fase3/RESUMO_FASE3.md` (incluir `resumo_assuntos` em tabela e, se houver, recall do gabarito).
Atualize `decisions.md` e `questions.md`.
