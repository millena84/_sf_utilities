# Fase 0 — Reconhecimento (org <ORG>)

## Antes de começar
Leia e siga integralmente `<DIR_TRABALHO>/_projeto/00_regras_gerais.md`. Em caso de conflito, as regras gerais prevalecem.

## Parâmetros desta execução
- ORG: `<ORG>`
- CAMINHO_ORG: `<CAMINHO_ORG>`
- DIR_TRABALHO: `<DIR_TRABALHO>`
- Lista de tipos de metadata em escopo: `<DIR_TRABALHO>/_entradas/tipos_metadata.txt` (um tipo por linha, nome da Metadata API, ex.: ApexClass)
- Lista de assuntos: `<DIR_TRABALHO>/_entradas/assuntos.csv` (coluna obrigatória `assunto`; colunas opcionais `descricao` e `sigla`)
- MODO_TESTE: `<sim|não>`

## Objetivo
Entender, para esta org:
1. **O que existe** — componentes dos tipos em escopo.
2. **Como os componentes se relacionam** entre tipos de metadata (regras de relação, comprovadas com exemplos reais).
3. **Como os assuntos aparecem na linguagem da org** (léxico e perfil semântico dos assuntos).

## Escopo dos assuntos — IMPORTANTE
- Esta fase trata **TODOS os assuntos de `assuntos.csv`**, com ou sem sigla. A coluna `sigla` **não filtra nada** aqui; ela só é repassada ao glossário.
- O modelo de referência e os artefatos de `_modelo/` **não são insumo desta fase**. Não os leia nem use o que estiver na memória da conversa sobre eles.

## Esta fase NÃO faz
- Não monta o grafo completo de dependências (fase 2).
- Não atribui componentes a assuntos (fase 3).
- Não interpreta integrações (fase 1).

## P. Pré-checagem
- `CAMINHO_ORG` existe e contém pastas de metadata.
- `tipos_metadata.txt` existe, não está vazio; cada linha é um nome de tipo plausível.
- `assuntos.csv` existe, tem a coluna `assunto`, sem linhas vazias. Registre duplicatas exatas como ALERTA.
- Se algo falhar → `fase0/PRECHECK_FALHOU.md` e encerre.

## Etapas

### 0.1 Perfil dos tipos de metadata
- Detecte o formato do projeto (source format, ex. `force-app/main/default`, ou Metadata API format) **sem usar CLI**, apenas pela estrutura de pastas/extensões.
- Para cada pasta de metadata da org, identifique tipo, formato e regra de nome:
  - `simples` (arquivo + `-meta.xml`), `bundle` (pasta = componente, ex. lwc/aura), `composto` (um XML contém vários subcomponentes, ex. `.object`, `.workflow`), `decomposto` (subcomponentes em arquivos próprios, ex. `objects/X/fields/Y.field-meta.xml`).
- Mapeie cada tipo da lista de entrada para sua pasta. Tipo da lista não encontrado → ALERTA.
- Liste também as pastas cujo tipo **não** está na lista (apenas contagem, sem análise).

**Saída:** `fase0/metadata_profile.csv`
`tipo,pasta,formato,regra_de_nome,qtd_componentes,na_lista`

### 0.2 Inventário dos componentes em escopo
- Uma linha por componente dos tipos em escopo, incluindo subcomponentes relevantes (no mínimo: campos, record types, validation rules, outbound messages, ações/elementos relevantes de Flow quando aplicável).
- Extraia `label` e `description` dos XML quando existirem (matéria-prima semântica).
- `is_test`: classes com `@isTest`. `is_generated`: classes geradas de WSDL (heurística: `WebServiceCallout.invoke` + classes internas de tipo, registre a heurística em decisions.md).
- `namespace`: prefixo `ns__` quando houver.

**Saída:** `fase0/inventory.csv`
`id,tipo,nome_api,pai,caminho,formato,linhas,label,descricao,is_test,is_generated,namespace`

### 0.3 Regras de relação entre tipos
Descubra, **a partir do que existe nesta org**, como um tipo referencia outro. Considere no mínimo:
Apex→Apex (instanciação, chamada estática, extends/implements), Apex→Objeto/Campo (SOQL, DML, referência tipada),
Apex→NamedCredential (`callout:`), Apex→CustomMetadata/CustomSetting, `Type.forName` (dinâmica),
Trigger→Objeto, Flow→Apex (`actionCalls`), Flow→Flow (`subflows`), Flow→Objeto, Workflow→OutboundMessage,
LWC/Aura/Visualforce→Apex, registros de CustomMetadata cujo valor é nome de componente (textual),
NamedCredential→ExternalCredential, NamedCredential/ExternalClientApplication/ConnectedApp→Certificate,
Profile/PermissionSet/PermissionSetGroup→ApexClass (`classAccesses`), →Objeto/Campo (`objectPermissions`/`fieldPermissions`),
→ExternalCredential (`externalCredentialPrincipalAccesses`), →CustomMetadata (`customMetadataTypeAccesses`), →Flow (`flowAccesses`).
Considere só os acessos concedidos (`enabled`/`allowRead`/`readable` = true).
Inclua padrões adicionais que encontrar.

Para cada regra: rode a extração numa **amostra estratificada por tipo** (seed=42): até 5 componentes de cada tipo em escopo que tenha código ou XML com referências (Apex, Trigger, Flow, LWC/Aura, Visualforce, Workflow, CustomMetadata, Profile/PermissionSet, NamedCredential etc.), com no mínimo 30 componentes no total. Registre exemplos reais.
Se uma regra não ocorrer na amostra, faça uma busca dirigida no inventário inteiro pelo padrão dela antes de marcar "não ocorre".

**Saídas:**
- `fase0/relation_rules_proposto.csv`
  `id_regra,tipo_origem,tipo_destino,padrao,natureza,qtd_ocorrencias_amostra,exemplos,status_revisao,comentario_revisao`
  (`natureza`: estrutural | explicita | dinamica | textual | acesso — `acesso` é usada para as concessões de Profile/PermissionSet; `exemplos`: até 3 `caminho:linha`; regra sem ocorrência → `qtd=0` e observação "não ocorre na amostra")
- `fase0/relation_sample.csv` `origem,destino,id_regra,evidencia`
- `fase0/unresolved_refs.csv` `origem,referencia_textual,id_regra,evidencia,motivo_provavel`
  (`motivo_provavel`: fora_do_escopo | pacote_gerenciado | padrao_padrao_salesforce | desconhecido)

### 0.4 Léxico da org
- Quebre nomes de API (camelCase, `_`, sufixos `__c`, `__mdt`, `__e`), labels, descrições e comentários Apex em termos.
- Normalize (minúsculas, sem acento). Identifique idioma (pt|en|abrev|misto).
- Proponha termos genéricos (não distinguem assunto: service, handler, util, helper, batch, controller, test, trigger etc.).

**Saídas:**
- `fase0/org_lexicon.csv` `termo,forma_normalizada,origem,qtd_componentes,tipos_onde_aparece,idioma`
- `fase0/termos_genericos_proposto.csv` `termo,qtd_componentes,motivo,status_revisao,comentario_revisao`

### 0.5 Perfil semântico dos assuntos
Leve a coluna `sigla` (quando existir) para o glossário. Para cada assunto: conceito de negócio em 1–2 frases, termos núcleo, sinônimos (pt/en/abreviações), termos da org que correspondem
(**somente termos presentes em `org_lexicon.csv`**), termos ambíguos (aparecem em mais de um assunto) e termos excludentes.

**Saídas:**
- `fase0/glossario_proposto.csv`
  `id_assunto,assunto,sigla,conceito,termos_nucleo,sinonimos,termos_da_org,qtd_componentes_alcancados,termos_ambiguos,termos_excludentes,status_revisao,comentario_revisao`
  (listas internas separadas por `|`)
- `fase0/subject_overlap.csv` `id_assunto_a,id_assunto_b,termos_compartilhados,qtd`
- `fase0/revisao/alcance_assuntos.csv` — para cada assunto, os até 10 componentes mais fortemente alcançados pelos termos (prévia para o teste de gabarito):
  `id_assunto,assunto,componente_id,termos_que_casaram,onde_casou(nome|label|descricao),ok,comentario`

### 0.6 Material de revisão humana
Gere em `fase0/revisao/` (seed=42, `AMOSTRA_REVISAO` linhas):
- `amostra_inventario.csv` — `id,tipo,caminho,label,is_test,is_generated,ok,comentario`
- `amostra_relacoes.csv` — **estratificada por regra**: 2 relações de cada regra com ocorrência (1 se só houver 1), sem limite de 10 linhas. `origem,destino,id_regra,evidencia,trecho_da_linha,ok,comentario` (o `trecho_da_linha` é o texto da linha citada, para conferência sem abrir o arquivo; mascarar segredos)
- `top_nao_resolvidas.csv` — 20 referências não resolvidas mais frequentes, com `ok,comentario`
- `top_termos.csv` — 50 termos mais frequentes com a marcação genérico sim/não
- `gabarito_<ORG>_PARA_PREENCHER.csv` — arquivo para a revisora preencher, com **uma linha para cada assunto de `assuntos.csv`** e as colunas `id_assunto,assunto,componente_id_esperado` (esta última vazia; não preencha)

## Autovalidação — `tools/fase0/validate_fase0.py`

| ID | Verificação | Severidade |
|---|---|---|
| F0-A01 | Insumos lidos; todo tipo da lista mapeado para uma pasta ou registrado como "não encontrado" | BLOQUEANTE |
| F0-A02 | Toda pasta da org está classificada (em escopo ou fora do escopo) | BLOQUEANTE |
| F0-A03 | Fechamento: todo arquivo das pastas em escopo pertence a algum componente do inventário (listar órfãos) | BLOQUEANTE |
| F0-A04 | IDs únicos em `inventory.csv` | BLOQUEANTE |
| F0-A05 | Tipos compostos: qtd de tags filhas no XML = qtd de subcomponentes inventariados por pai | BLOQUEANTE |
| F0-A06 | Pares arquivo/`-meta.xml` completos (listar quebrados) | ALERTA |
| F0-A07 | XML com erro de parse listados | ALERTA |
| F0-A08 | Toda regra de relação tem ≥1 exemplo real ou está marcada "não ocorre" após busca dirigida | BLOQUEANTE |
| F0-A19 | Toda regra com ocorrência aparece em `revisao/amostra_relacoes.csv` | BLOQUEANTE |
| F0-A09 | Reverificação: todo `caminho:linha` de exemplos e da amostra existe e contém o padrão citado | BLOQUEANTE |
| F0-A10 | Taxa de referências não resolvidas calculada; acima de `ALERTA_REFS_NAO_RESOLVIDAS` gera alerta | ALERTA |
| F0-A11 | Todo termo do léxico aparece em ≥1 componente; contagens recalculáveis a partir do inventário | BLOQUEANTE |
| F0-A12 | Nº de linhas do glossário = nº de assuntos em `assuntos.csv` (todos, independentemente da sigla); todo termo em `termos_da_org` existe no léxico | BLOQUEANTE |
| F0-A13 | Assuntos com `qtd_componentes_alcancados = 0` listados | ALERTA |
| F0-A14 | Nenhum segredo nos artefatos gerados | BLOQUEANTE |
| F0-A15 | CSVs bem formados: cabeçalho exato, mesmo nº de colunas em todas as linhas, UTF-8 | BLOQUEANTE |
| F0-A16 | Idempotência: rodar os scripts 2x gera arquivos idênticos | BLOQUEANTE |
| F0-A17 | Nenhum comando sf/sfdx foi utilizado (declarar no relatório) | BLOQUEANTE |
| F0-A18 | Nenhum arquivo de `_modelo/` ou `modelo_referencia/` foi lido; `gabarito_<ORG>_PARA_PREENCHER.csv` tem uma linha por assunto e a coluna `componente_id_esperado` vazia | BLOQUEANTE |

## Entrega
- Todos os arquivos acima + `fase0/validation_report.md` + `fase0/recon.md` + `fase0/RESUMO_FASE0.md`.
- `recon.md`: escopo, formato do projeto, volumes por tipo, tipos fora do escopo que parecem relevantes para integração
  (ex.: NamedCredential, RemoteSiteSetting, ConnectedApp, ExternalServiceRegistration, PlatformEventChannel, CustomMetadata),
  regras de relação encontradas, assuntos com vocabulário forte/fraco, riscos e recomendação para a fase 1.
- Atualize `<ORG>/decisions.md` e `<ORG>/questions.md`.
