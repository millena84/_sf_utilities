# Fase 3 — Clusterização por assunto (org <ORG>)

## Antes de começar
Leia o `config.json` na raiz da pasta de trabalho e siga integralmente `<DIR_TRABALHO> [busque no arquivo config.json]/_projeto/00_regras_gerais.md`.

## Parâmetros desta execução
- ORG: `<ORG> [busque no arquivo config.json]` · CAMINHO_ORG: `<CAMINHO_ORG> [busque no arquivo config.json]` · DIR_TRABALHO: `<DIR_TRABALHO> [busque no arquivo config.json]` · MODO_TESTE: `<MODO_TESTE> [busque no arquivo config.json]`
- ORG_DO_MODELO: `<ORG_DO_MODELO> [busque no arquivo config.json]` · Calibração: `CALIBRACAO` [busque no arquivo config.json]

## Objetivo
Associar componentes a assuntos de forma **explicável**: cada associação deve mostrar o caminho que a justifica.
O resultado decide **quais pontos de integração pertencem a cada assunto** (e, pela coluna `sigla`, a cada sigla). Ele **não** limita o conteúdo da documentação: isso é papel do dossiê da Fase 4.

## Esta fase NÃO faz
- Não escreve documentação de jornada.

## Insumos
- `fase0/inventory.csv`, `fase0/glossario_aprovado.csv`, `fase0/termos_genericos_aprovado.csv`
- `fase1/integration_points.csv`, `fase1/sistemas_externos_aprovado.csv`
- `fase2/edges.csv`, `fase2/nodes.csv`, `fase2/infra_hubs_aprovado.csv`
- `_projeto/base_de_conhecimento/` (seção 14 das regras): `diagnostico.md`, `desenhos.json`, `regras_ligacao.md`
- Opcional: `_entradas/gabarito_<ORG>.csv` (`id_assunto,assunto,componente_id_esperado`)
- Opcional (se esta org for a ORG_DO_MODELO): `_modelo/gabarito_modelo.csv`
- `fase2/validation_report.md`

## P. Pré-checagem
- Insumos obrigatórios existem; `_aprovado` sem `pendente` (exceto MODO_TESTE); fase 2 aprovada.
- Gabarito ausente → registrar ALERTA (não bloqueia).
- Falhou → `fase3/PRECHECK_FALHOU.md` e encerre.

## Etapas

### 3.0 Unidades de integração (base de conhecimento)
Antes de pontuar assuntos, agrupe os componentes que **trabalham juntos numa mesma integração**, usando os desenhos da base. Isso evita que peças de uma mesma integração (trigger, handler, classe de callout, Named Credential, LWC, Flow) caiam em assuntos diferentes ou fiquem sem assunto.

Para cada ponto de integração (`fase1/integration_points.csv`):
1. Identifique os **sinais** presentes (`S01`–`S38` de `diagnostico.md`) e os **desenhos candidatos**; confira a **assinatura mínima** de cada um e escolha a variante mais compatível (`desenhos.json`).
2. Percorra `edges.csv` a partir do ponto (nos dois sentidos, até `MAX_SALTOS`, **sem** o filtro de INFRA/HUB) e associe cada componente encontrado a um **papel da variante** (campo `componentes[].metadata_type` e `aciona`/`acionado_por`), usando as regras de `regras_ligacao.md`.
3. A unidade é o ponto + os componentes que preenchem papéis da variante, com evidência de aresta.

`fase3/unidades_integracao.csv`
`id_unidade,id_ponto,desenho_candidato,variante,confianca_desenho(alta|media|baixa),componente_id,papel_no_desenho,obrigatoriedade(Obrigatório|Opcional),classificacao_infra,aresta_evidencia`
- Sem variante compatível → `variante = nenhum` e motivo em `decisions.md`; a unidade fica só com o ponto e seus vizinhos diretos.
- Componentes INFRA/HUB_DADOS podem **preencher papel** na unidade (ex.: wrapper HTTP genérico como "cliente de callout"), mas continuam sem propagar assunto (3.2).

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
- **Coerência da unidade (3.0):** se o ponto de uma unidade (ou um componente da unidade com papel Obrigatório) tem ALTA/MEDIA num assunto, os demais membros da unidade que **não** são INFRA/HUB_DADOS recebem, nesse assunto, score = max(score atual, score da âncora × `DECAIMENTO`), com `origem = unidade_desenho` e `caminho_explicacao` = `unidade <id_unidade> (<variante>) > papel <papel_no_desenho>`. Membro com papel Obrigatório e aresta `documentado` recebe no mínimo MEDIA.
- Aresta de regra da base do tipo `heurística` conta como relação fraca (`FATOR_RELACAO_FRACA`).
- Confiança: ≥ `LIMIAR_ALTA` → ALTA; ≥ `LIMIAR_MEDIA` → MEDIA; abaixo → BAIXA (registrar só se ≥ 0.2).

`fase3/matriz_componente_assunto_proposto.csv`
`id_assunto,componente_id,tipo,score,confianca,origem(semente|propagacao|unidade_desenho),caminho_explicacao,is_integration_point,classificacao_infra,status_revisao,comentario_revisao`
- `caminho_explicacao`: `semente > aresta(id_regra) > ... > componente`, com os IDs de cada nó.

### 3.3 Conflitos, órfãos e resumo
- `fase3/conflitos_proposto.csv` — componentes com ALTA/MEDIA em ≥2 assuntos:
  `componente_id,assuntos_e_scores,proposta(compartilhado|assunto_principal:<id>),motivo,status_revisao,comentario_revisao`
- `fase3/pontos_orfaos_proposto.csv` — pontos de integração sem assunto ALTA/MEDIA:
  `id_ponto,componente_id,sistema_externo_id,direcao,assunto_mais_proximo,score,sugestao(novo_assunto|anexar:<id_assunto>|ignorar),motivo,status_revisao,comentario_revisao`
  A revisora decide cada linha (salva como `_aprovado`). **A Fase 4 só roda com todos os órfãos decididos.**
- `fase3/resumo_assuntos.csv`
  `id_assunto,assunto,qtd_alta,qtd_media,qtd_baixa,qtd_pontos_integracao,sistemas_externos,direcoes,pct_do_escopo,alerta`
  (`alerta`: SEM_INTEGRACAO | GIGANTE | SEM_SEMENTE | vazio)
- Se esta org for a ORG_DO_MODELO: converta os nomes de `_modelo/gabarito_modelo.csv` em IDs do inventário → `fase3/gabarito_resolvido.csv` `sigla,assunto,nome_componente,componente_id,resolvido(sim|não|ambiguo)`. Some esse gabarito ao `gabarito_<ORG>.csv`.
- Se houver gabarito: `fase3/recall_gabarito.csv` `id_assunto,componente_id_esperado,tipo,origem(time|modelo),classificavel(sim|não),encontrado(sim|não),assunto_encontrado,confianca,score,motivo_falha`
  - `classificavel = não` para tipos que não entram na matriz por definição (Profile, PermissionSet, PermissionSetGroup, Certificate, RemoteSiteSetting, CspTrustedSite, NamedCredential, ExternalCredential, ConnectedApp, ExternalClientApplication). O recall é calculado **só sobre os classificáveis**.
  - `motivo_falha` (quando não encontrado): `outro_assunto` | `infra_hub` | `sem_caminho` | `nome_nao_resolvido`.
  - O `RESUMO_FASE3.md` traz o recall por origem e por tipo.

### 3.4 Material de revisão humana (`fase3/revisao/`, seed=42)
- `amostra_baixa.csv` — `AMOSTRA_REVISAO` associações BAIXA com caminho, `deveria_entrar(sim|não),comentario`
- `amostra_media.csv` — `AMOSTRA_REVISAO` associações MEDIA com caminho, `ok,comentario`
- `mapa_assuntos.md` — por assunto: lista dos componentes ALTA, sistemas externos e um Mermaid `flowchart LR` simplificado
- `unidades_revisao.md` — para cada unidade: ponto, variante escolhida, papéis preenchidos × papéis Obrigatórios faltantes, e assunto(s) resultante(s)

## Autovalidação — `tools/fase3/validate_fase3.py`

| ID | Verificação | Severidade |
|---|---|---|
| F3-A01 | Pré-checagem executada e aprovada | BLOQUEANTE |
| F3-A02 | Todo assunto aprovado tem ≥1 semente ou alerta SEM_SEMENTE | BLOQUEANTE |
| F3-A03 | Todo `caminho_explicacao` é válido: cada passo é uma aresta existente em `edges.csv` | BLOQUEANTE |
| F3-A04 | Nenhum caminho tem INFRA/HUB_DADOS como nó intermediário | BLOQUEANTE |
| F3-A05 | Nenhum componente com termo excludente associado ao respectivo assunto | BLOQUEANTE |
| F3-A06 | Scores e confianças recalculáveis com os parâmetros declarados | BLOQUEANTE |
| F3-A07 | Fechamento: todo ponto de integração está associado (ALTA/MEDIA) a algum assunto ou em `pontos_orfaos_proposto.csv` | BLOQUEANTE |
| F3-A08 | Assunto com `pct_do_escopo` > `ALERTA_ASSUNTO_GIGANTE` | ALERTA |
| F3-A09 | Componente ALTA em >3 assuntos (provável infra não aprovada) | ALERTA |
| F3-A10 | Recall do gabarito (só tipos classificáveis) reportado por origem e por tipo; recall < 80% | ALERTA |
| F3-A14 | Se a matriz `_proposto` for regenerada, todos os derivados (recall, conflitos, órfãos, resumo, mapa) são regenerados na mesma execução | BLOQUEANTE |
| F3-A15 | Entrada da Fase 3 em `decisions.md` | BLOQUEANTE |
| F3-A16 | Todo ponto de integração tem unidade em `unidades_integracao.csv` (variante da base ou `nenhum` com motivo) | BLOQUEANTE |
| F3-A17 | Todo papel atribuído na unidade tem aresta de evidência em `edges.csv`; nenhuma variante citada inexiste em `desenhos.json` | BLOQUEANTE |
| F3-A18 | Unidade com membros em assuntos diferentes (ALTA/MEDIA) listada para revisão | ALERTA |
| F3-A19 | Recall do gabarito reportado também por `origem` (quanto veio de `unidade_desenho`) | ALERTA |
| F3-A11 | Nenhum componente `is_test=true` na matriz | BLOQUEANTE |
| F3-A12 | Nenhum segredo; CSVs bem formados; Mermaid estruturalmente válido | BLOQUEANTE |
| F3-A13 | Idempotência | BLOQUEANTE |

## Entrega
Arquivos acima + `fase3/validation_report.md` + `fase3/RESUMO_FASE3.md` (incluir `resumo_assuntos` em tabela e, se houver, recall do gabarito).
Atualize `decisions.md` e `questions.md`.
