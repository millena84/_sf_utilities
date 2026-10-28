# Fase M — Análise do modelo de referência

> Executar **uma única vez, antes da Fase 0**. Não depende de org.
> Resultado: o template que a Fase 4 vai seguir, as regras de cada seção e um gabarito de componentes extraído do modelo.

## Antes de começar
Leia e siga integralmente `<DIR_TRABALHO>/_projeto/00_regras_gerais.md`.

## Parâmetros desta execução
- DIR_TRABALHO: `<DIR_TRABALHO>`
- Modelo de referência: arquivos em `<DIR_TRABALHO>/_entradas/modelo_referencia/` (preferência: `.md` ou `.html`; `.docx` e `.pdf` são aceitos)
- SIGLA_MODELO: `<sigla documentada no modelo>`
- ORG_DO_MODELO: `<org a que o modelo se refere>`
- Assuntos do modelo: **lidos de `_entradas/assuntos.csv`**, nas linhas em que a coluna `sigla` = SIGLA_MODELO
- MODO_TESTE: `<sim|não>`

## Objetivo
Entender o modelo criado pelo time (estrutura, nível de detalhe e estilo) e transformá-lo em:
1. um **template reutilizável** para as demais siglas;
2. um **mapa** de onde cada seção do template busca seus dados no pipeline;
3. um **gabarito** com os componentes citados no modelo, para medir a qualidade das fases 3 e 4.

## Esta fase NÃO faz
- Não altera o modelo.
- Não copia conteúdo do modelo para outras siglas. O modelo é **inspiração de estrutura e estilo**, não texto a ser reaproveitado.

## P. Pré-checagem
- Existe pelo menos 1 arquivo em `_entradas/modelo_referencia/`.
- Todos os arquivos são legíveis. Se precisar converter `.docx` ou `.pdf`, pode instalar o pacote necessário, registrando em `decisions.md`.
- `_entradas/assuntos.csv` e `_entradas/tipos_metadata.txt` existem.
- Se a conversão falhar → `_modelo/PRECHECK_FALHOU.md` e encerre.

## Etapas

### M.1 Estrutura do modelo
Para cada documento do modelo, identifique o **tipo de documento** (ex.: visão geral da sigla, documento por integração/jornada) e a árvore de seções.

`_modelo/estrutura_modelo.csv`
`documento,tipo_documento,nivel,ordem,titulo_secao,formato_conteudo(texto|tabela|lista|diagrama|imagem),colunas_tabela,tamanho_aprox,exemplo_curto`

- `exemplo_curto`: até 100 caracteres, com segredos mascarados.

### M.2 Template extraído — `_projeto/template_extraido.md`
Para cada tipo de documento, liste as seções **na ordem do modelo**. Para cada seção:
- **Objetivo** (1 frase)
- **Conteúdo esperado** (o que entra, o que não entra)
- **Formato** (texto, tabela com estas colunas, lista, diagrama)
- **Nível de detalhe** (ex.: "1 linha por classe com o papel dela na integração")
- **Obrigatoriedade**: `sempre` ou `se houver`
- **Texto quando não houver conteúdo**

Inclua também:
- **Guia de estilo**: tom, pessoa verbal, tamanho típico, como os componentes são nomeados, como os diagramas são usados e como os nomes dos arquivos são formados.
- **Seções obrigatórias do projeto** que o modelo não tiver, ao final: `Pontos em aberto` e `Apêndice — Rastreabilidade` (evidências `arquivo:linha`).
- Os exemplos devem ser **genéricos** (`<NomeDaClasse>`), nunca nomes reais do modelo.

### M.3 Mapa seção → fonte de dados
`_modelo/mapa_secoes_proposto.csv`
`tipo_documento,secao,fonte_no_pipeline,regra_de_preenchimento,cobertura(total|parcial|nenhuma),status_revisao,comentario_revisao`

Fontes possíveis (exemplos): `fase0/inventory.csv`, `fase1/integration_points.csv`, `fase1/componentes_integracao.csv`, `fase2/edges.csv` (relações de natureza `acesso` para Profiles e Permission Sets), `fase4/<SIGLA>/secoes/*.csv`.

Seções com cobertura `parcial` ou `nenhuma` → `_modelo/lacunas_modelo.md`, explicando o que falta e propondo um ajuste (ex.: incluir um tipo de metadata na lista).

### M.4 Gabarito do modelo
Liste todos os componentes Salesforce citados no modelo:
`_modelo/gabarito_modelo.csv`
`sigla,assunto,documento,secao,tipo_provavel,nome_componente,trecho_do_modelo`

- `assunto`: escolha entre os assuntos de `assuntos.csv` com `sigla` = SIGLA_MODELO. Se a coluna `sigla` não existir ou nenhuma linha tiver essa sigla, proponha o assunto mais próximo da lista inteira e registre a dúvida em `questions.md` (ALERTA).
- O gabarito é convertido em IDs do inventário na Fase 3 (da ORG_DO_MODELO).

### M.5 Tipos de metadata exigidos pelo modelo
Liste os tipos de metadata necessários para preencher o template e compare com `tipos_metadata.txt`.
Considere no mínimo: CustomObject, ApexClass, ApexTrigger, Flow, LightningComponentBundle, CustomMetadata (tipos `__mdt` e registros),
NamedCredential, ExternalCredential, ExternalClientApplication, ConnectedApp, Certificate, RemoteSiteSetting, CspTrustedSite, Profile, PermissionSet, PermissionSetGroup.

Use sempre o **nome exato da Metadata API** (ex.: `LightningComponentBundle`, não `LWC`). Gere dois arquivos:
- `_modelo/tipos_exigidos.csv` `tipo,motivo(qual seção precisa),presente_na_lista(sim|não)`: **todos** os tipos que o modelo exige (referência).
- `_modelo/tipos_faltantes.csv` `tipo,motivo`: **somente** os tipos com `presente_na_lista = não`. É o único arquivo que pede ação humana.
- Se um nome da lista de entrada não for um nome válido da Metadata API mas parecer equivalente a um tipo exigido, registre em `_modelo/tipos_nome_divergente.csv` `nome_na_lista,nome_correto`.

### M.6 Material de revisão humana (`_modelo/revisao/`)
- `comparativo_secoes.md`: para cada seção, à esquerda o que o modelo mostra (resumo) e à direita a regra que foi extraída para o template.

## Autovalidação — `tools/faseM/validate_faseM.py`

| ID | Verificação | Severidade |
|---|---|---|
| FM-A01 | Todos os arquivos do modelo foram lidos (lista com status) | BLOQUEANTE |
| FM-A02 | Fechamento: toda seção de `estrutura_modelo.csv` está no `template_extraido.md` | BLOQUEANTE |
| FM-A03 | A ordem das seções no template é igual à do modelo | BLOQUEANTE |
| FM-A04 | Toda seção do template tem linha em `mapa_secoes_proposto.csv` | BLOQUEANTE |
| FM-A05 | Toda seção com cobertura `parcial` ou `nenhuma` está em `lacunas_modelo.md` | BLOQUEANTE |
| FM-A06 | O template contém `Pontos em aberto` e `Apêndice — Rastreabilidade` | BLOQUEANTE |
| FM-A07 | Todo componente do gabarito aparece literalmente no texto do modelo (nada inventado) | BLOQUEANTE |
| FM-A08 | Nenhum nome de componente do gabarito aparece no `template_extraido.md` (inspirar, não copiar) | BLOQUEANTE |
| FM-A09 | Tipos faltantes listados; nenhum tipo de `tipos_faltantes.csv` existe em `tipos_metadata.txt` (comparação exata) | BLOQUEANTE |
| FM-A10 | Nenhum segredo (inclusive conteúdo de certificado ou URL com credencial) nos artefatos | BLOQUEANTE |
| FM-A11 | CSVs bem formados; idempotência | BLOQUEANTE |

## Entrega
Arquivos acima + `_modelo/validation_report.md` + `_modelo/RESUMO_FASEM.md`.
**Ação humana antes da Fase 0:** incluir em `tipos_metadata.txt` os tipos de `tipos_faltantes.csv` que fizerem sentido e aprovar `mapa_secoes_proposto.csv` (salvar como `mapa_secoes_aprovado.csv`).
