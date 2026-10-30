# Fase 4 — Documentação da sigla (org <ORG>, sigla <SIGLA>)

> Uma execução por sigla. Comece pela sigla do modelo de referência: o resultado é comparado automaticamente com o documento do time.

## Antes de começar
Leia o `config.json` na raiz da pasta de trabalho e siga integralmente:
- `<DIR_TRABALHO> [busque no arquivo config.json]/_projeto/00_regras_gerais.md` — em especial as seções **2** (dossiê), **13** (regras de escrita e marcações) e **14** (base de conhecimento)
- Os esqueletos oficiais: `_projeto/templates/01_inventario_tecnico_sigla.md` e `_projeto/templates/02_documento_por_integracao.md` (**estrutura obrigatória**)
- `_projeto/guia_estilo.md` e `_modelo/sintaxe_blocos.md` (estilo, exemplos e sintaxe dos blocos)
- Os documentos do modelo em `_entradas/modelo_referencia/` — **somente como referência de estilo e nível de detalhe**

## Parâmetros desta execução
- ORG: `<ORG> [busque no arquivo config.json]` · CAMINHO_ORG: `<CAMINHO_ORG> [busque no arquivo config.json]` · DIR_TRABALHO: `<DIR_TRABALHO> [busque no arquivo config.json]`
- ALIAS_REPO: `<ALIAS_REPO> [busque no arquivo config.json]` · DATA_REFERENCIA: `<DATA_REFERENCIA> [busque no arquivo config.json]` · MODO_TESTE: `<MODO_TESTE> [busque no arquivo config.json]`
- SIGLA: `<SIGLA> [busque no arquivo config.json]` — se for um id de assunto (ex.: `ASS-007`), o assunto é documentado como sigla isolada
- SIGLA_MODELO: `<SIGLA_MODELO> [busque no arquivo config.json]` — se SIGLA = SIGLA_MODELO, executar também a etapa 4.7
- Assuntos desta sigla: linhas de `_entradas/assuntos.csv` com `sigla` = SIGLA

## Objetivo
Produzir, para a sigla:
1. **Um documento por integração** (esqueleto 02) — "como funciona".
2. **O inventário técnico da sigla** (esqueleto 01) — "o que existe" —, montado **por último**, consolidando as integrações.

## Princípios desta fase
1. **A Fase 3 decide quais integrações pertencem à sigla. Ela não limita o conteúdo.** O conteúdo vem do **dossiê** de cada integração, montado a partir do grafo **completo**, sem filtro de INFRA, HUB_DADOS ou confiança.
2. **Entender antes de escrever.** Cada integração é explicada a partir da **leitura do código** dos seus componentes, como faria uma pessoa analisando o repositório.
3. **Tabelas por script, explicações pela leitura.** Toda tabela dos documentos é gerada por script a partir do dossiê; os textos explicativos vêm da etapa de interpretação.
4. **A estrutura vem dos esqueletos; a quantidade vem dos dados.** O número de integrações do modelo não define o desta sigla.

## Insumos
- `_projeto/templates/*`, `_projeto/guia_estilo.md`, `_modelo/sintaxe_blocos.md`, `_modelo/mapa_secoes_aprovado.csv` (em MODO_TESTE, o `_proposto`)
- `fase3/matriz_componente_assunto_aprovado.csv`, `fase3/conflitos_aprovado.csv`, `fase3/pontos_orfaos_aprovado.csv`
- `fase2/edges.csv`, `fase2/nodes.csv`, `fase3/unidades_integracao.csv`
- `fase1/integration_points.csv`, `fase1/sistemas_externos_aprovado.csv`, `fase1/componentes_integracao.csv`, `fase1/config_por_ponto.csv`
- `fase0/inventory.csv` (colunas `estado` e `atributos`), `fase0/glossario_aprovado.csv`, `_entradas/assuntos.csv` (coluna `descricao`)
- `_projeto/base_de_conhecimento/` (seção 14 das regras)
- Se SIGLA = SIGLA_MODELO: `_modelo/gabarito_modelo.csv`, `fase3/gabarito_resolvido.csv`
- Código-fonte em `CAMINHO_ORG` (leitura)

## P. Pré-checagem
- `config.json` lido; SIGLA existe em `assuntos.csv` (coluna `sigla`) ou é um `id_assunto` válido.
- Esqueletos, guia de estilo, sintaxe dos blocos e mapa de seções existem.
- **Todos os órfãos da Fase 3 decididos** (`pontos_orfaos_aprovado.csv` sem `pendente`; em MODO_TESTE, usar a `sugestao` do `_proposto`).
- Fase 3 aprovada; nenhum `_aprovado` com `pendente` (exceto MODO_TESTE).
- Falhou → `fase4/<SIGLA>/PRECHECK_FALHOU.md` e encerre.

## Etapas

### 4.1 Integrações da sigla
- Pontos de integração de cada assunto da sigla: componentes com `is_integration_point = sim` e confiança ALTA/MEDIA na matriz aprovada, mais os órfãos decididos como `anexar:<assunto da sigla>`.
- **Integração** = troca com um sistema externo com gatilho e resultado próprios. **Todo assunto com ≥1 ponto gera ≥1 integração.** Não una assuntos diferentes só porque usam o mesmo sistema ou middleware; uma integração só atende a mais de um assunto se `conflitos_aprovado.csv` indicar `compartilhado`.
- Assunto sem ponto de integração: não gera documento; entra na seção 6.2 do inventário técnico, com o motivo.
- Parta da unidade de `fase3/unidades_integracao.csv` (variante e papéis já identificados) e confirme ou corrija o `desenho_base` com `diagnostico.md` (sinais e assinatura mínima) e a tabela da variante. Sem variante compatível → `nenhum` + motivo em `decisions.md` (e `questions.md` se for um desenho que a base não tem).
- Identifique integrações relacionadas (uma aciona a outra) para a coluna `relacionada_a`.

`fase4/<SIGLA>/integracoes.csv`
`id_integracao(INTnn),id_assunto,alias_curto,acao_relacionada,ordem_na_jornada,gatilho,componente_gatilho,resultado,direcao(inbound|outbound),sincronismo(sync|async|misto),sistema_externo_id,pontos_integracao,desenho_base,confianca_desenho,relacionada_a`

### 4.2 Dossiê de cada integração (sem filtro)
A partir do componente gatilho e dos pontos de integração, percorra `edges.csv` **completo** (inclusive INFRA e HUB_DADOS) nos dois sentidos e junte **tudo o que a integração toca diretamente**. Use a tabela da variante `desenho_base` como roteiro do que procurar.

Gere em `fase4/<SIGLA>/<INTnn>/dossie/` (todas com coluna `evidencia`):

| Arquivo | Conteúdo |
|---|---|
| `componentes.csv` | Todos os componentes da integração: `componente_id,tipo,estado,atributos,papel_no_desenho(componente da variante),como_chegou(aresta/regra)` |
| `objetos.csv` | Objetos e campos lidos/escritos (SOQL/DML/Flow), com o label, External IDs e campos de controle |
| `classes.csv` | Classes, triggers e seus **papéis** (ver 4.3), com anotações e interfaces |
| `flows.csv` | Flows com tipo (tela, record-triggered antes/depois, agendado, autolaunched), objeto, disparo e efeito |
| `ui.csv` | LWC/Aura/FlexiPage/Quick Actions envolvidos, onde aparecem e qual Apex chamam |
| `custom_metadata.csv` | Tipos `__mdt` e registros usados, finalidade e registros por ambiente (valores sensíveis mascarados; URLs só com domínio) |
| `acessos.csv` | Profiles/Permission Sets/Permission Set Groups que dão acesso aos componentes da integração, indicando usuário de integração |
| `marcacoes.csv` | Os 6 tipos de configuração (ver 4.4) com SUCCESS/ABSTRACT/DANGER e motivo |
| `riscos.csv` | `id_base(Ann\|Nnn\|limite),descricao,evidencia` — anti-padrões (`antipadroes.md`), limites da fonte (`limites_da_fonte.md`) e da plataforma (`limites_plataforma.md`, com data) |

Componentes que a variante marca como **Obrigatório** e não foram encontrados: verifique `limites_da_fonte.md`; se não for limite da fonte, investigue antes de seguir.

### 4.3 Leitura e interpretação do código
Para cada integração, **leia o código** dos componentes do dossiê (classes, triggers, Flows, LWC) e registre em `fase4/<SIGLA>/<INTnn>/interpretacao.md`, com evidência em cada afirmação:

1. **Objetivo de negócio** — a partir da `descricao` do `assuntos.csv`, do `conceito` do glossário e do que o código faz.
2. **Passos** (para "Visão geral por passo"): para cada passo, o gatilho, os componentes **na ordem em que atuam** e a saída.
3. **Ciclo de vida** (fases): o que acontece e **quem atua** (usuário, sistema externo, plataforma, job agendado).
4. **Dinâmica dos objetos** — como ler a relação entre os objetos do workflow (quem cria, quem atualiza, que status muda).
5. **Papel de cada classe**, a partir da evidência no código: endpoint REST/SOAP (`@RestResource`, `webservice`), cliente de callout (`HttpRequest`, `callout:`), processamento assíncrono (Queueable, `@future`, Batch, Schedulable), trigger handler, consulta (SOQL/selector), mapeamento de dados (serialização JSON/DTO/wrapper), ação invocável (`@InvocableMethod`), controller de UI (`@AuraEnabled`). Uma frase do que a classe faz **nesta** integração.
6. **Sucesso, falha e retry** — o que acontece em cada caso, quem tenta de novo e com qual regra.
7. **Ordem, limites e reprocessamento** — sincronismo, governor limits relevantes (`limites_plataforma.md`), idempotência, como reprocessar.

O texto deve passar no **teste anti-genérico** (seção 13 das regras). A ordem da variante `desenho_base` é roteiro; a ordem real vem do código. Transição sem aresta no grafo → [INFERIDO].

`fase4/<SIGLA>/<INTnn>/etapas.csv` `ordem,passo,gatilho,componentes_em_ordem,saida,quem_atua,sync_async,aresta_suporte(id_regra|INFERIDO),evidencia,confianca`

### 4.4 Marcações das configurações (SUCCESS / ABSTRACT / DANGER)
Para cada integração e cada tipo — **Connected App / External Client App, Certificado, Remote Site Settings, Endpoints, Named Credential, External Credential** —, a partir de `fase1/config_por_ponto.csv` e da variante `desenho_base`:

| Situação | Marcação | Motivo obrigatório |
|---|---|---|
| Componente encontrado e ligado à integração com evidência | `SUCCESS` | Por que a integração o usa (ex.: "a classe chama `callout:<NC>`, que fornece endpoint e autenticação") |
| Não encontrado e, pelo desenho, não é necessário | `ABSTRACT` | Por que, tecnicamente, não é necessário, citando a variante (ex.: "endpoint vem da Named Credential; Remote Site não é exigido") |
| Encontrado, mas sem prova de ligação; ou obrigatório no desenho e ausente; ou informação fora do repositório (`Nnn`) | `DANGER` | O que foi achado, por que não dá para confirmar e o que verificar na org |

`fase4/<SIGLA>/<INTnn>/dossie/marcacoes.csv` `tipo_config,marcacao,componente_id,motivo,id_base,evidencia`

### 4.5 Renderização dos documentos por integração (esqueleto 02)
- **Script** gera, a partir do dossiê e das etapas: Cartão, Índice, Visão geral por passo, Ciclo de vida, tabelas de Flows e retry, Anexo A (Evidências) e os blocos de marcação (com a sintaxe de `_modelo/sintaxe_blocos.md`).
- **Textos explicativos** (Objetos do workflow, explicações didáticas ao final das seções, sucesso/falha, ordem/limites) vêm de `interpretacao.md`, no estilo de `guia_estilo.md`.
- **Seção 3.1 (caminho da integração):** Mermaid `sequenceDiagram` com `autonumber`; participantes = componentes reais na ordem em que atuam (e o sistema externo pelo nome); rótulo de cada seta = evento ou ação (ex.: `after insert`, `enqueueJob`, `POST <recurso>`).
- **Seção 6 (Componentes técnicos):** tabelas de Triggers/Apex (com o papel de 4.3), LWC/Aura/páginas e Custom Metadata, a partir do dossiê.
- **Seção 7 (Configurações de integração):** os 6 tipos com as marcações de 4.4 (mesma fonte usada no inventário da sigla).
- **Seção 8 (Integrações relacionadas):** apenas link para o documento da outra integração e o tipo de relação; **nunca** copiar as seções dela.
- Seção do esqueleto marcada como "se houver" e sem conteúdo: escreva **uma frase que explique por que não se aplica** a esta integração (ex.: "esta integração não usa Flows: o disparo é feito pela trigger X"). Nunca use texto padrão.
- Nome do arquivo: `docs/<SIGLA>/<SIGLA>_<INTnn>_<acao_relacionada>.md`.

### 4.6 Renderização do inventário técnico da sigla (esqueleto 01) — por último
Consolide os documentos por integração, seguindo o esqueleto 01 (v2):
- **Cabeçalho** (`!!!SUCCESS` com repositório `ALIAS_REPO`, comentários relevantes, lista das jornadas com link e `Data revisão` = DATA_REFERENCIA no formato dd/mm/aaaa) e **Índice** (toda seção com link e "o que buscar"; todo documento da sigla com link).
- **1. Resumo executivo e limites da cadeia:** tabela Caminho | Entrada | Saída (uma linha por integração) + Mermaid básico do fluxo da sigla, com as integrações na ordem da jornada e os sistemas pelo nome.
- **2. Modelo de dados:** objeto | papel na sigla (só os objetos de negócio).
- **3. Configurações de integração:** uma subseção por integração, com os 6 tipos e as **mesmas marcações** dos documentos por integração (mesma fonte `marcacoes.csv`) e link para a explicação detalhada.
- **4. Acesso:** usuário de integração, Profiles, Permission Sets e Permission Set Groups relevantes.
- **5. Componentes compartilhados entre integrações:** componente | tipo | integrações afetadas | impacto de uma alteração.
- **6. Escopo e pontos de validação:** 6.1 recebe **todos os `!!!DANGER`** da sigla como itens a verificar na org; 6.2 observações técnicas (inclui `riscos.csv` e assuntos sem integração, com o motivo).
- **Anexo A:** fontes principais no repositório.
- Os catálogos de Flows, Apex, Triggers e LWC ficam **nos documentos por integração** (seções 4 e 6 do esqueleto 02), não no inventário.
- Nome do arquivo: `docs/<SIGLA>/<SIGLA>_inventario_tecnico.md`.

### 4.7 Comparação com o modelo (somente se SIGLA = SIGLA_MODELO)
`fase4/<SIGLA>/comparacao_modelo.md`:
- Componentes do gabarito encontrados × não encontrados (com o motivo) × extras encontrados pelo Devin.
- **Marcações:** para cada configuração com marcação no gabarito, comparar a marcação do Devin com a do time.
- Integrações do modelo × integrações identificadas; seções do esqueleto preenchidas × vazias.

### 4.8 Material de revisão humana (`fase4/<SIGLA>/revisao/`)
- `marcacoes.csv` — todas as marcações com motivo, `ok,comentario`
- `inferidos.csv` — todos os [INFERIDO], `ok,comentario`
- `amostra_etapas.csv` — 3 etapas por integração com `trecho_da_linha,ok,comentario`
- `danger.csv` — todos os DANGER (o que verificar na org)

## Autovalidação — `tools/fase4/validate_fase4.py <SIGLA>`

| ID | Verificação | Severidade |
|---|---|---|
| F4-A01 | Pré-checagem executada e aprovada | BLOQUEANTE |
| F4-A02 | Cobertura de assuntos: todo assunto da sigla tem ≥1 integração ou aparece na seção 6.2 do inventário com motivo | BLOQUEANTE |
| F4-A03 | Cobertura de pontos: todo ponto de integração dos assuntos da sigla está em alguma integração | BLOQUEANTE |
| F4-A04 | Nenhuma integração junta assuntos diferentes sem `compartilhado` em `conflitos_aprovado.csv` | BLOQUEANTE |
| F4-A05 | Estrutura: todo documento tem todas as seções do seu esqueleto, na ordem e com os títulos exatos | BLOQUEANTE |
| F4-A06 | **Dados → documento:** toda linha dos CSVs do dossiê aparece na tabela correspondente; nº de linhas do CSV = nº de linhas da tabela | BLOQUEANTE |
| F4-A07 | **Frases proibidas** ausentes (lista da seção 13 das regras), inclusive "não identificado na base analisada" e menções a `.csv`/`faseN/` | BLOQUEANTE |
| F4-A08 | Nenhum parágrafo repetido em seções ou documentos diferentes (exceto blocos de marcação idênticos entre documento da integração e inventário) | BLOQUEANTE |
| F4-A09 | **Consistência entre seções:** todo componente citado em gatilho, passos ou diagrama aparece na seção do seu tipo (ex.: LWC do gatilho na seção de UI) | BLOQUEANTE |
| F4-A10 | Marcações: os 6 tipos presentes por integração, cada um com SUCCESS/ABSTRACT/DANGER e motivo não vazio; sintaxe igual à de `sintaxe_blocos.md` | BLOQUEANTE |
| F4-A11 | Marcações iguais no documento da integração e no inventário da sigla | BLOQUEANTE |
| F4-A12 | Todo DANGER aparece na seção 6.1 do inventário | BLOQUEANTE |
| F4-A13 | **Anti-genérico:** o Cartão e o Resumo de cada integração citam o sistema externo pelo nome, ≥1 objeto de negócio e o gatilho | BLOQUEANTE |
| F4-A14 | Papel das classes: nenhuma classe sem papel; papéis com evidência; não pode haver o mesmo texto de papel para todas as classes de uma integração | BLOQUEANTE |
| F4-A15 | Diagramas: todo participante/nó existe no dossiê; toda integração aparece no Mermaid da sigla; `autonumber` na seção 3.1 | BLOQUEANTE |
| F4-A16 | Tabelas Markdown com o mesmo nº de colunas em todas as linhas; `\|` escapado nas células | BLOQUEANTE |
| F4-A17 | Índice: toda seção e todo documento da sigla listados com link válido | BLOQUEANTE |
| F4-A18 | Toda afirmação dos dossiês tem evidência; reverificação de 100% | BLOQUEANTE |
| F4-A19 | Nenhum trecho com mais de 15 palavras copiado do modelo | BLOQUEANTE |
| F4-A20 | Nenhum segredo; hosts só com domínio; nenhum conteúdo de certificado | BLOQUEANTE |
| F4-A21 | Toda integração tem `desenho_base` (variante existente ou `nenhum` com motivo) | ALERTA |
| F4-A22 | Nenhum fato vem só de item da base marcado como "não confirmado"/⚠️ ou só de regra `heurística` com confiança ALTA | ALERTA |
| F4-A23 | % de etapas [INFERIDO] por integração; acima de 30% gera alerta | ALERTA |
| F4-A24 | (SIGLA = SIGLA_MODELO) Recall do gabarito e concordância das marcações reportados; abaixo de 80% gera alerta | ALERTA |
| F4-A25 | Idempotência dos CSVs; entrada da Fase 4 em `decisions.md` | BLOQUEANTE |

## Entrega
Documentos em `docs/<SIGLA>/` + dossiês + `fase4/<SIGLA>/validation_report.md` + `fase4/<SIGLA>/RESUMO.md` (com a tabela **assunto → integrações documentadas** e a lista de DANGER) + `comparacao_modelo.md` quando aplicável.

**Próximo passo obrigatório:** Fase 4R (leitura crítica), numa sessão nova.

**Ciclo de correção:** se existir `fase4R/<SIGLA>/problemas.csv` de uma leitura crítica anterior, trate cada linha como **correção obrigatória** nesta execução e registre em `RESUMO.md` como cada uma foi resolvida.

### 📝 Arquivos que a revisora altera e salva como `_aprovado`
Nenhum. A revisão humana desta fase é feita sobre os documentos, depois da Fase 4R.
