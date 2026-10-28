# Fase 4 — Documentação por sigla (org <ORG>, sigla <SIGLA>)

> Execute **uma sessão por sigla**.
> Comece pela **sigla do modelo de referência**: o resultado pode ser comparado automaticamente com o documento feito pelo time.

## Antes de começar
Leia e siga integralmente:
- `<DIR_TRABALHO>/_projeto/00_regras_gerais.md`
- `<DIR_TRABALHO>/_projeto/template_extraido.md` (**prevalece**; gerado na Fase M)
- `<DIR_TRABALHO>/_projeto/template_jornada.md` (fallback e conteúdos mínimos)
- Os documentos do modelo em `<DIR_TRABALHO>/_entradas/modelo_referencia/`, **como referência de estilo e nível de detalhe**

## Parâmetros desta execução
- ORG: `<ORG>` · CAMINHO_ORG: `<CAMINHO_ORG>` · DIR_TRABALHO: `<DIR_TRABALHO>` · MODO_TESTE: `<sim|não>`
- SIGLA: `<SIGLA>`
- Assuntos desta sigla: **lidos de `_entradas/assuntos.csv`** (linhas com `sigla` = SIGLA). Opcional: `<lista de assuntos para sobrescrever, ou vazio>`
- É a sigla do modelo de referência: `<sim|não>`

## Objetivo
Produzir a documentação da sigla no formato do modelo do time: **uma visão geral** (resumo da jornada completa) e **um documento por integração/jornada**, legíveis para negócio e rastreáveis para técnicos.

## Regra de inspiração
- Siga a **estrutura, a ordem das seções, os formatos de tabela, o tom e o nível de detalhe** do modelo.
- **Não copie texto** do modelo. Todo conteúdo vem da análise desta org, com evidência.
- Se o modelo e o template base divergirem na estrutura, vale o modelo. Os conteúdos mínimos do template base que o modelo não tiver vão para as seções mais próximas ou para o final.

## Insumos
- `_projeto/template_extraido.md`, `_modelo/mapa_secoes_aprovado.csv`
- `fase3/matriz_componente_assunto_aprovado.csv`, `fase3/conflitos_aprovado.csv`
- `fase2/edges.csv`, `fase2/nodes.csv`, `fase2/infra_hubs_aprovado.csv`
- `fase1/integration_points.csv`, `fase1/sistemas_externos_aprovado.csv`, `fase1/componentes_integracao.csv`
- `fase0/inventory.csv`, `fase0/glossario_aprovado.csv`
- Se for a sigla do modelo: `_modelo/gabarito_modelo.csv`, `fase3/gabarito_resolvido.csv`
- Código-fonte em `CAMINHO_ORG` (leitura)

## P. Pré-checagem
- Existe ≥1 assunto com `sigla` = SIGLA em `assuntos.csv` (ou lista informada no parâmetro opcional).
- Todos os assuntos da sigla existem no glossário aprovado e têm ≥1 componente ALTA/MEDIA aprovado; os que não têm são listados (ALERTA) e entram em "Pontos em aberto" da visão geral.
- `template_extraido.md` existe e há mapa de seções: `mapa_secoes_aprovado.csv` ou, em MODO_TESTE, `mapa_secoes_proposto.csv`. Só na ausência de ambos: usar o template base e registrar ALERTA (não bloqueia).
- Fase 3 aprovada; nenhum `_aprovado` com `pendente` (exceto MODO_TESTE).
- Falhou → `fase4/<SIGLA>/PRECHECK_FALHOU.md` e encerre.

## Etapas

### 4.1 Recorte
- Una os componentes dos assuntos da sigla. Núcleo = ALTA; apoio = MEDIA; possivelmente relacionados = BAIXA (só em apêndice).
- INFRA/HUB_DADOS: apenas citados, com link para o catálogo de infraestrutura.

`fase4/<SIGLA>/recorte.csv` `componente_id,id_assunto,papel(nucleo|apoio|possivel|infra),confianca`

### 4.2 Integrações e jornada completa
- **Integração** = troca com um sistema externo com gatilho e resultado próprios (normalmente 1 ou mais pontos de integração do mesmo sistema e da mesma finalidade).
- **Jornada completa** = a ordem em que as integrações acontecem do início ao fim do processo de negócio da sigla.
- Para cada integração, identifique o gatilho: endpoint exposto, trigger, Flow record-triggered, agendamento, ação de usuário (LWC/Aura/Visualforce/botão), Platform Event.

`fase4/<SIGLA>/integracoes.csv` `id_integracao(INTnn),nome,ordem_na_jornada,gatilho,componente_gatilho,resultado,direcao,sistema_externo_id,pontos_integracao`

### 4.3 Etapas de cada integração
Percorra o grafo a partir do gatilho e **leia o código** para ordenar as etapas. Marque síncrono/assíncrono (`@future`, Queueable, Batch, Schedulable, Platform Event, Outbound Message) e o tratamento de erro (try/catch, log, retentativa, reprocessamento).
Transição sem aresta no grafo → [INFERIDO] com justificativa.

`fase4/<SIGLA>/etapas.csv` `id_integracao,ordem,descricao,componente_id,sync_async,aresta_suporte(id_regra|INFERIDO),evidencia,confianca`

### 4.4 Levantamento por seção
Gere um CSV por seção em `fase4/<SIGLA>/secoes/`, **por integração**, sempre com a coluna `evidencia`:

| Arquivo | Conteúdo | Regra |
|---|---|---|
| `objetos.csv` | Objetos e campos principais lidos/escritos, External IDs, campos de controle | Só campos usados pela integração |
| `classes.csv` | Classes e seus papéis | Sem classes de teste |
| `gatilhos.csv` | Gatilhos e condições | — |
| `componentes_integracao.csv` | Named Credential, External Credential, External Client App, Connected App, Certificado (**nome e data de vencimento**), Remote Site, CSP | Hosts só com domínio; nunca conteúdo de certificado ou segredo |
| `custom_metadata.csv` | Tipos `__mdt` e registros usados, finalidade, campos relevantes **por ambiente** quando houver registros por ambiente | Valores sensíveis mascarados; URLs só com domínio |
| `flows.csv` | Flows envolvidos | Se houver |
| `lwc.csv` | LWC/Aura envolvidos | Se houver |
| `acessos.csv` | Profiles e Permission Sets que concedem acesso aos componentes da integração (classe, objeto, External Credential, Custom Metadata), indicando se parecem ser de usuário de integração | **Somente** acessos a componentes do recorte; nunca a lista inteira do profile |

### 4.5 Escrita
- Siga o `template_extraido.md` e o `mapa_secoes_aprovado.csv`: cada seção é preenchida a partir da fonte mapeada.
- Gere os arquivos com a mesma convenção de nomes do modelo. Na ausência de convenção:
  - `docs/<SIGLA>/README.md` — visão geral (resumo da jornada completa)
  - `docs/<SIGLA>/<INTnn>_<slug>.md` — um por integração/jornada
- O resumo não usa nomes técnicos (nada de nomes de API ou `__c`) e é escrito em frases curtas.
- Diagramas: siga o modelo. Se o modelo não tiver diagrama, use Mermaid (`flowchart LR` na visão geral e `sequenceDiagram` nas integrações).
- Seção do tipo "se houver" sem conteúdo → "Não se aplica a esta integração."; seção do tipo "sempre" sem conteúdo → "Não identificado na base analisada."

### 4.6 Comparação com o modelo (somente se for a sigla do modelo)
Compare a documentação gerada com o modelo do time:
`fase4/<SIGLA>/comparacao_modelo.md`
- Componentes do gabarito encontrados, não encontrados (com hipótese do motivo) e componentes extras encontrados pelo Devin (podem ser acertos que o modelo não tinha).
- Recall por seção (objetos, classes, componentes de integração, custom metadata, flows, LWC, acessos).
- Integrações do modelo × integrações identificadas.
- Diferenças de estrutura (seções faltantes ou a mais).

### 4.7 Material de revisão humana (`fase4/<SIGLA>/revisao/`)
- `amostra_etapas.csv` — 3 etapas por integração com `trecho_da_linha,ok,comentario`
- `inferidos.csv` — todos os [INFERIDO] com justificativa, `ok,comentario`
- `possiveis.csv` — componentes BAIXA com `promover(sim|não),comentario`
- `certificados.csv` — certificados citados, com vencimento e `ok,comentario`

## Autovalidação — `tools/fase4/validate_fase4.py <SIGLA>`

| ID | Verificação | Severidade |
|---|---|---|
| F4-A01 | Pré-checagem executada e aprovada | BLOQUEANTE |
| F4-A02 | Todo componente citado nos docs existe no inventário e está no recorte (ou justificado) | BLOQUEANTE |
| F4-A03 | Fechamento: todo componente núcleo aparece em alguma seção de algum documento ou está listado como "não utilizado" com motivo | BLOQUEANTE |
| F4-A04 | Fechamento: todo ponto de integração do recorte aparece em alguma integração | BLOQUEANTE |
| F4-A05 | Toda etapa e toda linha dos CSVs de seção têm evidência; reverificação de 100% | BLOQUEANTE |
| F4-A06 | Toda transição entre etapas consecutivas tem aresta em `edges.csv` ou marca [INFERIDO] | BLOQUEANTE |
| F4-A07 | Seções obrigatórias: os títulos são lidos de `template_extraido.md` (ou do template base) e todos estão presentes, na ordem, e sem ficar vazios | BLOQUEANTE |
| F4-A08 | Todo item dos CSVs de seção aparece na seção correspondente do documento (e vice-versa) | BLOQUEANTE |
| F4-A09 | Todo certificado tem data de vencimento ou "não disponível na base"; vencidos ou a vencer em 90 dias da DATA_REFERENCIA destacados | ALERTA |
| F4-A10 | Profiles/Permission Sets citados concedem de fato acesso a algum componente do recorte (verificar no XML) | BLOQUEANTE |
| F4-A11 | Resumo sem nomes técnicos (regex: `__c`, `__e`, `__mdt`, CamelCase técnico) | ALERTA |
| F4-A12 | Nenhum trecho com mais de 15 palavras copiado literalmente do modelo | BLOQUEANTE |
| F4-A13 | Diagramas estruturalmente válidos; links internos resolvem | BLOQUEANTE |
| F4-A14 | % de etapas [INFERIDO] por integração reportado; acima de 30% gera alerta | ALERTA |
| F4-A15 | (sigla do modelo) Recall do gabarito por seção reportado; abaixo de 80% gera alerta | ALERTA |
| F4-A16 | Nenhum segredo; hosts só com domínio; nenhum conteúdo de certificado | BLOQUEANTE |
| F4-A17 | Idempotência dos CSVs | BLOQUEANTE |

## Entrega
Docs + CSVs + `fase4/<SIGLA>/validation_report.md` + `fase4/<SIGLA>/RESUMO.md` (+ `comparacao_modelo.md` quando aplicável).
Atualize `decisions.md` e `questions.md`.
