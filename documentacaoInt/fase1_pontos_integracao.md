# Fase 1 — Pontos de integração (org <ORG>)

## Antes de começar
Leia o `config.json` na raiz da pasta de trabalho e siga integralmente `<DIR_TRABALHO> [busque no arquivo config.json]/_projeto/00_regras_gerais.md`.
Consulte a base de conhecimento (seção 14 das regras): `_projeto/base_de_conhecimento/guia_evidencias.md`, `regras_ligacao.md`, `diagnostico.md`, `limites_da_fonte.md`.

## Parâmetros desta execução
- ORG: `<ORG> [busque no arquivo config.json]` · CAMINHO_ORG: `<CAMINHO_ORG> [busque no arquivo config.json]` · DIR_TRABALHO: `<DIR_TRABALHO> [busque no arquivo config.json]` · MODO_TESTE: `<MODO_TESTE> [busque no arquivo config.json]`
- DATA_REFERENCIA: `<DATA_REFERENCIA> [busque no arquivo config.json]`

## Objetivo
Encontrar **todos os pontos onde a org troca dados com o mundo externo**, classificar direção e mecanismo,
e identificar os **sistemas externos** envolvidos.

## Esta fase NÃO faz
- Não monta jornadas nem atribui assuntos.
- Não acessa nenhum endpoint.

## Insumos
- `fase0/inventory.csv`, `fase0/metadata_profile.csv`
- `fase0/relation_rules_aprovado.csv`
- `fase0/validation_report.md`

## P. Pré-checagem
- Insumos existem e têm as colunas esperadas.
- `relation_rules_aprovado.csv` sem `pendente` (exceto MODO_TESTE).
- `fase0/validation_report.md` com `Resultado geral: APROVADO PARA REVISÃO HUMANA`.
- Falhou → `fase1/PRECHECK_FALHOU.md` e encerre.

## Etapas

### 1.1 Catálogo de sinais
Monte `fase1/catalogo_sinais.csv` (`id_sinal,categoria,padrao,direcao_padrao,tipos_alvo,descricao`) com, no mínimo:

| Categoria | Sinais |
|---|---|
| Inbound Apex | `@RestResource`, `@HttpGet/@HttpPost/@HttpPut/@HttpPatch/@HttpDelete`, métodos `webservice`, `Messaging.InboundEmailHandler` |
| Outbound Apex | `new HttpRequest`, `Http().send`, `setEndpoint(`, `callout:`, `WebServiceCallout.invoke`, classes geradas de WSDL |
| Eventos | `EventBus.publish`, triggers em objetos `__e`, Flows disparados por Platform Event, Change Data Capture (`ChangeEvent`) |
| Declarativo | `WorkflowOutboundMessage`, Flow `actionCalls` do tipo externalService/apex que levam a callout, `ExternalServiceRegistration` |
| Configuração | `NamedCredential`, `ExternalCredential`, `ExternalClientApplication` (e configurações OAuth associadas), `ConnectedApp`, `Certificate`, `RemoteSiteSetting`, `CspTrustedSite`, `AuthProvider`, `ExternalDataSource` |
| Inbound presumido | Campos `externalId=true`, Permission Sets/Profiles com nome contendo integra/api/mule/sap/etc., campos de controle de integração (status/id externo/data de sincronização) |

Inclua sinais adicionais descobertos na fase 0. Se um sinal depende de um tipo **fora do escopo**, registre como lacuna em `fase1/lacunas.csv`.

**Complemente o catálogo com a base de conhecimento:** os padrões de código `C01`–`C25` e o catálogo por tipo de `guia_evidencias.md` (campos XML que comprovam cada componente) e os sinais `S01`–`S38` de `diagnostico.md`. Anote o id da base na coluna `descricao` (ex.: `C07`, `S21`). Aceite os dois formatos de arquivo (com e sem `-meta.xml`, seção 1 do guia).

### 1.2 Censo e classificação
- Varra os componentes do inventário com todos os sinais → `fase1/signal_census.csv` (`id_sinal,componente_id,evidencia`).
- Cada ocorrência vira **ponto de integração** ou **descarte justificado**:
  - Descartes obrigatórios: classes de teste, `HttpCalloutMock`/`WebServiceMock`, código comentado.
- `fase1/integration_points.csv`
  `id_ponto,componente_id,id_sinal,direcao,mecanismo,endpoint_ref,host,sistema_externo_id,evidencia,confianca,observacao`
  - `direcao`: INBOUND | OUTBOUND | EVENTO | CONFIG | INBOUND_PRESUMIDO
  - `mecanismo`: REST | SOAP | PlatformEvent | CDC | OutboundMessage | ExternalService | Email | API_Padrao | Outro
  - `endpoint_ref`: nome da Named Credential / Remote Site / registro de Custom Metadata que contém o endpoint
  - `host`: apenas domínio; endpoint dinâmico não resolvido → `DINAMICO`
- `fase1/descartes.csv` `componente_id,id_sinal,evidencia,motivo`
- Use as colunas de direção e mecanismo da matriz `diagnostico.md` como referência. Sinal que a base marca como anti-padrão (ex.: `S08`, callout direto em trigger) vira ponto de integração com a observação `anti-padrão A06`, não descarte.

### 1.3 Resolução de endpoints e sistemas externos
- Resolva `callout:Nome` → arquivo da Named Credential → host. Resolva Remote Sites → host. Literais em `setEndpoint` → host.
  Endpoints vindos de Custom Metadata/Custom Setting: resolva se o registro estiver na base; senão `DINAMICO`.
  Siga as regras de `regras_ligacao.md` (`L01`–`L09`, `L19`, `L22`, `L36`, `L37`, `L42`) e os casos difíceis do fim do arquivo. Valores de Custom Setting nunca estão no repositório (`N06`); Custom Metadata e Custom Labels estão (`N07`).
- Agrupe por host/credencial e proponha sistemas externos:
  `fase1/sistemas_externos_proposto.csv`
  `sistema_externo_id,nome_proposto,hosts,credenciais,qtd_pontos,direcoes,evidencias,status_revisao,comentario_revisao`
- Configurações sem uso (Named Credential/Remote Site não referenciados por nenhum componente em escopo) → `fase1/config_sem_uso.csv`.

### 1.4 Componentes de integração
Consolide todos os componentes de configuração de integração:
`fase1/componentes_integracao.csv`
`componente_id,tipo,host,tipo_autenticacao,certificado,vencimento_certificado,status_vencimento(valido|a_vencer|vencido|nao_disponivel),usado_por,evidencia`
- `vencimento_certificado`: lido do XML do certificado (ex.: `expirationDate`). Se não existir na base → `nao_disponivel`.
- `status_vencimento`: calculado a partir de `DATA_REFERENCIA` e `ALERTA_VENCIMENTO_DIAS`.
- `tipo_autenticacao`: apenas o tipo (ex.: OAuth client credentials, JWT, senha, mTLS), **nunca valores**. Use os campos indicados em `guia_evidencias.md` (ex.: `namedCredentialType`, `authenticationProtocol`, `isClientCredentialEnabled`). Web Server × Username-Password não se distingue pelo XML: registre "não determinado" (`N11`).
- Não copie o valor de nenhum campo listado como sensível no guia (coluna "Campos sensíveis").
- `usado_por`: componentes que referenciam (via relações aprovadas).

### 1.5 Configuração por ponto de integração
Para cada ponto de integração, registre **o que foi encontrado** para cada um dos 6 tipos de configuração dos documentos finais. **Só fatos**; a marcação SUCCESS/ABSTRACT/DANGER é decidida na Fase 4, com o desenho da integração.

`fase1/config_por_ponto.csv`
`id_ponto,tipo_config(ConnectedApp_ExternalClientApp|Certificado|RemoteSite|Endpoint|NamedCredential|ExternalCredential),componente_id,como_se_liga,evidencia,observacao`
- Uma linha por ponto × tipo, **inclusive quando nada foi encontrado** (`componente_id` vazio e `observacao` com o que foi pesquisado).
- **Endpoint:** onde o endpoint está configurado — Named Credential, registro de Custom Metadata (nome do registro e se há um por ambiente), Custom Setting (`N06`: valor não está no repositório) ou fixo no código — e o domínio.
- **Connected App / External Client App:** relevante para INBOUND com OAuth; para OUTBOUND, registre "não se aplica ao sentido" na observação.
- Use as regras `L..` de `regras_ligacao.md` para ligar ponto → configuração e cite o id em `como_se_liga`.

### 1.6 Material de revisão humana (`fase1/revisao/`, seed=42)
- `amostra_pontos.csv` — `AMOSTRA_REVISAO` pontos estratificados por direção, com `trecho_da_linha,ok,comentario`
- `amostra_descartes.csv` — 5 descartes com `trecho_da_linha,ok,comentario`
- `inbound_presumido.csv` — todos os INBOUND_PRESUMIDO com `ok,comentario`

## Autovalidação — `tools/fase1/validate_fase1.py`

| ID | Verificação | Severidade |
|---|---|---|
| F1-A01 | Pré-checagem executada e aprovada | BLOQUEANTE |
| F1-A02 | Todo sinal do catálogo foi pesquisado (contagem por sinal, inclusive zero) | BLOQUEANTE |
| F1-A03 | Fechamento: toda linha de `signal_census.csv` está em `integration_points.csv` ou em `descartes.csv` | BLOQUEANTE |
| F1-A04 | Todo `componente_id` existe no inventário | BLOQUEANTE |
| F1-A05 | Reverificação: toda evidência existe e a linha contém o padrão do sinal | BLOQUEANTE |
| F1-A06 | Nenhum ponto vem de classe `is_test=true` ou mock | BLOQUEANTE |
| F1-A07 | Todo OUTBOUND tem `endpoint_ref` ou `host`, ou está marcado `DINAMICO` | BLOQUEANTE |
| F1-A08 | Todo ponto tem `sistema_externo_id` ou `SIS::DESCONHECIDO` | BLOQUEANTE |
| F1-A09 | Todo sistema proposto tem ≥1 ponto | BLOQUEANTE |
| F1-A10 | `host` contém só domínio (sem path, query, credencial) | BLOQUEANTE |
| F1-A11 | % de pontos `DINAMICO` e `SIS::DESCONHECIDO` reportados | ALERTA |
| F1-A12 | Lacunas (sinais em tipos fora do escopo) listadas | ALERTA |
| F1-A13 | Nenhum segredo nos artefatos (incluindo conteúdo de certificado) | BLOQUEANTE |
| F1-A16 | Todo componente de configuração do inventário está em `componentes_integracao.csv`; todo certificado tem vencimento ou `nao_disponivel` | BLOQUEANTE |
| F1-A17 | Certificados vencidos ou a vencer listados | ALERTA |
| F1-A18 | `config_por_ponto.csv` tem exatamente 6 linhas por ponto de integração | BLOQUEANTE |
| F1-A19 | Entrada da Fase 1 em `decisions.md` | BLOQUEANTE |
| F1-A14 | CSVs bem formados | BLOQUEANTE |
| F1-A15 | Idempotência | BLOQUEANTE |

## Entrega
Arquivos acima + `fase1/validation_report.md` + `fase1/RESUMO_FASE1.md` (incluir tabela: pontos por direção × mecanismo, e pontos por sistema externo).
Atualize `decisions.md` e `questions.md`.

### 📝 Arquivos que a revisora altera e salva como `_aprovado`
| Arquivo gerado (`_proposto`) | O que preencher | Salvar como | Exigido por |
|---|---|---|---|
| `fase1/sistemas_externos_proposto.csv` | `status_revisao`; nome correto do sistema em `comentario_revisao` quando `ajustado` | `fase1/sistemas_externos_aprovado.csv` | Fases 2, 3, 4 |

