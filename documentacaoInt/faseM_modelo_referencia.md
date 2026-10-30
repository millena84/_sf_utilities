# Fase M — Análise do modelo de referência

> Executar **uma única vez, antes da Fase 0**. Não depende de org.
> A **estrutura** dos documentos já está definida pelos esqueletos oficiais. Esta fase extrai do modelo do time apenas **estilo, exemplos, sintaxe dos blocos e gabarito**.

## Antes de começar
Leia o `config.json` na raiz da pasta de trabalho e siga integralmente `<DIR_TRABALHO> [busque no arquivo config.json]/_projeto/00_regras_gerais.md`.

## Parâmetros desta execução
- DIR_TRABALHO: `<DIR_TRABALHO> [busque no arquivo config.json]`
- SIGLA_MODELO: `<SIGLA_MODELO> [busque no arquivo config.json]`
- ORG_DO_MODELO: `<ORG_DO_MODELO> [busque no arquivo config.json]`
- MODO_TESTE: `<MODO_TESTE> [busque no arquivo config.json]`
- Modelo de referência: `_entradas/modelo_referencia/`
- Esqueletos oficiais: `_projeto/templates/01_inventario_tecnico_sigla.md` e `_projeto/templates/02_documento_por_integracao.md`
- Assuntos do modelo: linhas de `_entradas/assuntos.csv` com `sigla` = SIGLA_MODELO

## Escopo
- Trata **somente** os assuntos do modelo. A estrutura vale para todas as siglas a partir dos esqueletos.
- **Não** altera o modelo nem os esqueletos. **Não** copia texto do modelo para nenhum outro artefato além do gabarito.

## P. Pré-checagem
- `config.json` lido; os dois esqueletos existem; há ≥1 arquivo em `modelo_referencia/`.
- Arquivos legíveis (conversão de `.docx`/`.pdf` permitida, registrar em `decisions.md`).
- `assuntos.csv` e `tipos_metadata.txt` existem; há ≥1 assunto com `sigla` = SIGLA_MODELO (senão, ALERTA e registrar dúvida).
- Falhou → `_modelo/PRECHECK_FALHOU.md` e encerre.

## Etapas

### M.1 Correspondência modelo × esqueletos
Para cada documento do modelo, identifique se ele corresponde ao esqueleto **01 (sigla)** ou **02 (integração)** e associe cada trecho do modelo à seção correspondente do esqueleto.

`_modelo/correspondencia.csv` `documento_modelo,esqueleto(01|02),secao_esqueleto,trecho_modelo_resumido,observacao`
- Seções do esqueleto sem correspondente no modelo → `observacao = sem exemplo no modelo`.

### M.2 Sintaxe dos blocos — `_modelo/sintaxe_blocos.md`
Copie do modelo, **literalmente**, 1 exemplo de cada bloco existente (`!!!SUCCESS`, `!!!ABSTRACT` e, se houver, `!!!DANGER`), preservando espaços, recuo e quebras de linha (mascarando dados sensíveis). Descreva a regra de formatação (ex.: "marcação na 1ª linha; conteúdo nas linhas seguintes com N espaços de recuo"). Se `!!!DANGER` não existir no modelo, use a mesma regra dos outros dois.

### M.3 Guia de estilo — `_projeto/guia_estilo.md`
Para **cada seção dos dois esqueletos**:
- **Objetivo** da seção (1 frase).
- **Como o modelo preenche** (tom, tamanho, nível de detalhe, formato das tabelas).
- **Exemplo genérico** de preenchimento, reescrito com nomes fictícios (`<Objeto__c>`, `<ClasseCallout>`, `<SistemaExterno>`). **Nunca** nomes reais do modelo.
- **Fatos obrigatórios** para não ficar genérico (ex.: Cartão → objetivo cita o sistema externo e o objeto de negócio).

Inclua ainda: tom e pessoa verbal, como nomear componentes no texto (API name, label ou ambos), tamanho típico das explicações didáticas e como os diagramas Mermaid são usados.

### M.4 Mapa seção → fonte de dados — `_modelo/mapa_secoes_proposto.csv`
`esqueleto(01|02),secao,fonte_no_pipeline,regra_de_preenchimento,tipo(tabela_script|texto_interpretado|bloco_marcacao),status_revisao,comentario_revisao`

- **Uma linha por seção dos esqueletos.** A coluna `esqueleto` só aceita `01` ou `02`.
- `tipo`: `tabela_script` (gerada por script a partir do dossiê), `texto_interpretado` (escrito a partir da leitura do código), `bloco_marcacao` (SUCCESS/ABSTRACT/DANGER).
- `regra_de_preenchimento` genérica, sem nomes de assuntos, sistemas ou componentes do modelo.
- Fontes típicas: `fase4/<SIGLA>/<INTnn>/dossie/*.csv`, `fase4/<SIGLA>/<INTnn>/interpretacao.md`, `fase1/config_por_integracao.csv`, `fase4/<SIGLA>/integracoes.csv`.

### M.5 Gabarito do modelo — `_modelo/gabarito_modelo.csv`
`sigla,assunto,documento,secao,tipo_provavel,nome_componente,marcacao(SUCCESS|ABSTRACT|DANGER|nenhuma),trecho_do_modelo`
- Todos os componentes Salesforce citados no modelo, inclusive as configurações marcadas como ABSTRACT. A coluna `marcacao` permite comparar depois as marcações do Devin com as do time.

### M.6 Tipos de metadata exigidos
Nomes exatos da Metadata API.
- `_modelo/tipos_exigidos.csv` `tipo,motivo,presente_na_lista(sim|não)`: todos os tipos de que os esqueletos precisam (no mínimo: CustomObject, ApexClass, ApexTrigger, Flow, LightningComponentBundle, AuraDefinitionBundle, FlexiPage, CustomMetadata, NamedCredential, ExternalCredential, ExternalClientApplication, ConnectedApp, Certificate, RemoteSiteSetting, CspTrustedSite, Profile, PermissionSet, PermissionSetGroup).
- `_modelo/tipos_faltantes.csv` `tipo,motivo`: só os ausentes de `tipos_metadata.txt`.
- `_modelo/tipos_nome_divergente.csv` `nome_na_lista,nome_correto`.

### M.7 Material de revisão (`_modelo/revisao/`)
- `comparativo.md`: para cada seção dos esqueletos, o que o modelo mostra (resumo) ao lado do exemplo genérico do guia de estilo.

## Autovalidação — `tools/faseM/validate_faseM.py`

| ID | Verificação | Severidade |
|---|---|---|
| FM-A01 | Todos os arquivos do modelo foram lidos | BLOQUEANTE |
| FM-A02 | Toda seção dos dois esqueletos tem linha em `mapa_secoes_proposto.csv` e entrada no `guia_estilo.md` | BLOQUEANTE |
| FM-A03 | `mapa_secoes_proposto.csv`: coluna `esqueleto` só com `01`/`02`; `tipo` preenchido | BLOQUEANTE |
| FM-A04 | Nenhum nome de componente, assunto ou sistema do gabarito aparece em `guia_estilo.md` nem em `regra_de_preenchimento` do mapa | BLOQUEANTE |
| FM-A05 | `sintaxe_blocos.md` contém exemplos literais encontrados no modelo (conferir que o texto existe no modelo) | BLOQUEANTE |
| FM-A06 | Todo componente do gabarito aparece literalmente no texto do modelo | BLOQUEANTE |
| FM-A07 | Nenhum tipo de `tipos_faltantes.csv` existe em `tipos_metadata.txt` | BLOQUEANTE |
| FM-A08 | Nenhum segredo nos artefatos | BLOQUEANTE |
| FM-A09 | CSVs bem formados; idempotência; entrada da Fase M em `decisions.md` | BLOQUEANTE |

## Entrega
Arquivos acima + `_modelo/validation_report.md` + `_modelo/RESUMO_FASEM.md`.

### 📝 Arquivos que a revisora altera e salva como `_aprovado`
| Arquivo gerado (`_proposto`) | O que preencher | Salvar como | Exigido por |
|---|---|---|---|
| `_modelo/mapa_secoes_proposto.csv` | `status_revisao` e `comentario_revisao` em todas as linhas | `_modelo/mapa_secoes_aprovado.csv` | Fase 4 |

Outras ações (sem `_aprovado`): incluir em `_entradas/tipos_metadata.txt` os tipos de `tipos_faltantes.csv`; revisar e, se preciso, editar direto `_projeto/guia_estilo.md` e `_modelo/sintaxe_blocos.md`.
