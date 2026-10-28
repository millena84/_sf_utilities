# Lista de tarefas para realizar a documentação

Como você vai continuar na mesma sessão do Devin em que o modelo foi criado, há um cuidado extra: o Devin já "conhece" o modelo pela conversa. Isso ajuda na Fase M, mas aumenta o risco de ele copiar trechos do modelo ou usar a memória da conversa em vez dos arquivos. O passo 3 trata disso.

---

## 1. Preparar o ambiente (≈15 min)

- [ ] Abrir o VS Code na pasta da org e confirmar que ela tem a estrutura de projeto Salesforce (`force-app/...` ou pastas de metadata direto na raiz).
- [ ] **Decidir onde fica a `DIR_TRABALHO`.** O ideal é uma pasta **fora** da pasta da org, por exemplo `../doc-integracoes/`, porque a org é somente leitura e assim nenhum artefato acaba no repositório Flosum.
  - Se o Devin só conseguir escrever dentro da pasta aberta, use uma subpasta como `_doc_integracoes/` e inclua-a no `.gitignore`.
- [ ] Criar a estrutura de pastas:
  ```
  <DIR_TRABALHO>/_projeto/
  <DIR_TRABALHO>/_entradas/modelo_referencia/
  ```
- [ ] Baixar do GitHub (`_sf_utilities/documentacaoInt`) e copiar `00_regras_gerais.md` e `template_jornada.md` para `_projeto/`. Os demais arquivos ficam à mão para copiar e colar os prompts.
- [ ] Confirmar que o Devin tem Python 3 disponível. Basta pedir para ele rodar `python3 --version`.

## 2. Preparar os insumos (≈20 min)

- [ ] **Modelo de referência:** pedir ao Devin, na sessão do modelo, que salve a versão final dele em `_entradas/modelo_referencia/` como `.md`, um arquivo por documento (visão geral e cada integração). Confira se é a versão refatorada final.
- [ ] **`_entradas/assuntos.csv`:** coluna `assunto` obrigatória e `descricao` opcional, mas que ajuda muito.
- [ ] **`_entradas/tipos_metadata.txt`:** um tipo por linha. Ponto de partida:
  ```
  CustomObject
  ApexClass
  ApexTrigger
  Flow
  LightningComponentBundle
  AuraDefinitionBundle
  ApexPage
  CustomMetadata
  NamedCredential
  ExternalCredential
  ExternalClientApplication
  ConnectedApp
  Certificate
  RemoteSiteSetting
  CspTrustedSite
  Workflow
  PlatformEventChannel
  ExternalServiceRegistration
  Profile
  PermissionSet
  PermissionSetGroup
  ```
- [ ] **Anotar os valores dos parâmetros**, para colar em todos os prompts:

  | Parâmetro | Valor |
  |---|---|
  | `<ORG>` | |
  | `<CAMINHO_ORG>` | |
  | `<DIR_TRABALHO>` | |
  | MODO_TESTE | `sim` (hoje) |
  | DATA_REFERENCIA | data de hoje (AAAA-MM-DD) |
  | SIGLA_MODELO | |
  | ORG_DO_MODELO | |
  | ASSUNTOS_DO_MODELO | |
  | Siglas → assuntos | (lista para a Fase 4) |

## 3. Reorientar a sessão do Devin (≈2 min)

- [ ] Antes do primeiro prompt, colar esta mensagem:
  > A partir de agora vamos executar um pipeline de documentação em fases. Para cada fase, siga **apenas** o prompt da fase e os arquivos em `<DIR_TRABALHO>`. O modelo de referência está em `_entradas/modelo_referencia/` e deve ser usado **somente pelo arquivo**, como inspiração de estrutura e estilo. Não reaproveite textos nem conclusões que estejam na memória desta conversa. É proibido usar sf/sfdx CLI.

## 4. Executar em sequência, em MODO_TESTE (o resto do dia)

Depois de cada fase, faça só o **portão** do checklist (cerca de 2 min): abra o `validation_report.md` e confira se a primeira linha diz APROVADO. Se aparecer `PRECHECK_FALHOU.md` ou REPROVADO, resolva antes de seguir.

- [ ] **Fase M:** depois dela, inclua em `tipos_metadata.txt` o que estiver em `_modelo/tipos_faltantes.csv`. É o único ajuste obrigatório antes da Fase 0, mesmo em modo teste.
- [ ] **Fase 0:** ao terminar, anote 2 ou 3 componentes que com certeza pertencem a cada um de 3 a 5 assuntos e salve em `_entradas/gabarito_<ORG>.csv`, usando o modelo gerado em `fase0/revisao/`. Leva 15 minutos e é a base da medição de qualidade.
- [ ] **Fase 1.**
- [ ] **Fase 2.**
- [ ] **Fase 3.**
- [ ] **Fase 4 com a sigla do modelo.** Prioridade do dia, porque gera o `comparacao_modelo.md`.
- [ ] Fase 4 com uma segunda sigla, se der tempo.
- [ ] A Fase 5 pode ficar para depois.

**Se a sessão ficar lenta ou o Devin começar a se confundir**, abra uma sessão nova a partir da Fase 1. Os prompts foram feitos para isso: cada fase lê tudo dos arquivos.

## 5. Fechamento do dia (≈20 min)

- [ ] Ler o `comparacao_modelo.md`: qual o recall por seção e o que ficou faltando?
- [ ] Rodar os itens que mais revelam falhas no método: **FM-H01, F0-H04, F1-H02, F2-H01, F3-H01, F3-H02 e F4-H01**.
- [ ] Anotar os resultados num `registro_validacao.md` (o modelo está no fim do checklist).
- [ ] Separar para trazer aqui: os `validation_report.md` e os `RESUMO_FASE*.md` de cada fase, o `comparacao_modelo.md` e o `questions.md`. Com eles eu ajusto prompts, limiares e regras.
