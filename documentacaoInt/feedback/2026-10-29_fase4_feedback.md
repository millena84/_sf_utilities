# Feedback da Fase 4 — execução de teste (2026-10-29)

> Status: parte 1 (README por sigla) e documento por integração nº 1 registrados. Aguardando o documento nº 2.
> Os prompts ainda **não** foram alterados com base neste feedback. As correções serão feitas depois da parte 2, em conjunto.

---

## Parte 1 — README.md por sigla (visão geral)

| # | Seção | Problema observado | Causa provável no prompt | Correção proposta |
|---|---|---|---|---|
| 1 | Índice | Incompleto. Além do resumo, deveria listar cada arquivo gerado | Nem o template base nem a etapa 4.5 exigem uma lista dos documentos gerados | Seção obrigatória "Documentos desta sigla": um link por arquivo, com uma linha de descrição. Verificação: todo arquivo gerado em `docs/<SIGLA>/` aparece no índice |
| 2 | Resumo executivo | Genérico, sem contexto | O prompt não define o que o resumo precisa conter, nem manda usar as descrições de negócio que existem (`assuntos.csv`, conceito do glossário) | Elementos obrigatórios: processo de negócio (a partir da `descricao` dos assuntos e do conceito do glossário), quem dispara, sistemas externos pelo nome, objetos de negócio principais e resultado. Proibir frases genéricas; verificar que o texto cita os sistemas e os assuntos da sigla |
| 3 | Mapa da jornada | Genérico, sem contexto | A regra só pede "Mermaid flowchart LR", sem exigir que os nós sejam os dados reais | Nós obrigatórios: as integrações de `integracoes.csv` na ordem da jornada, os sistemas externos pelo nome e os objetos principais. Verificação: todo nó do diagrama existe nos CSVs, e toda integração aparece no diagrama |
| 4 | Integrações | Ok, mas poderia ter mais informação, mesmo sendo uma visão geral | Colunas mínimas definidas pelo template base | Acrescentar: assunto, mecanismo, síncrono/assíncrono, gatilho, objeto principal e link para o documento |
| 5 | Componentes núcleo | Coisas demais, e só uma lista | A etapa 4.1 manda unir todo o núcleo, e o template não define um recorte para a visão geral | Trocar por "Objetos de negócio e papel na integração" (objeto, papel: origem/destino/controle, integrações que usam). A lista técnica completa vai para os documentos por integração |
| 6 | Pontos em aberto | Não fica claro o que fazer com cada item | Formato livre | Tabela: item, impacto, ação sugerida, quem pode responder (ex.: time de integração, negócio), origem/evidência |
| 7 | Inventário técnico da sigla | **Todas** as seções trazem o mesmo texto padrão: "conteúdo técnico detalhado está nos CSVs de seção e nos documentos por integração; quando não houver evidência específica, a ausência será registrada como não identificada" | O Devin escreveu um texto padrão em vez de transformar os CSVs de seção em tabelas. A verificação F4-A08 ("todo item dos CSVs de seção aparece na seção do documento") deveria ter reprovado a fase. Ou os CSVs estavam vazios, ou a verificação não foi implementada de verdade | Proibir texto de remissão genérico quando o CSV da seção tiver linhas: a seção **precisa** trazer a tabela. "Não identificado" só é permitido se o CSV tiver 0 linhas. Nova verificação: detectar parágrafos idênticos repetidos em várias seções. Reforçar a F4-A08 com contagem: linhas do CSV = linhas da tabela |
| 8 | Configurações de integração (subseções por integração) | Título quebrado e o mesmo texto padrão | Títulos das seções lidos do `template_extraido.md` (possível erro de formatação ao extrair) e o mesmo problema do item 7 | Validar a sintaxe dos títulos (sem `#` sobrando, sem texto cortado). Verificação de títulos: todo título do documento existe exatamente no template |

### Pontos para checar na execução (antes de corrigir os prompts)
- Os CSVs em `fase4/<SIGLA>/secoes/` têm linhas? (Diferencia "o Devin não levantou" de "o Devin levantou, mas não escreveu".)
- O que a F4-A08 reportou no `validation_report.md` da sigla?
- O `_projeto/template_extraido.md` traz o título quebrado do item 8?

---

## Parte 2 — Documentos por integração

### Documento 1

| # | Seção | Problema observado |
|---|---|---|
| D1.1 | Resumo | Genérico, sem contexto; não ajuda a identificar do que se trata |
| D1.2 | Ficha rápida | Mesmo problema |
| D1.3 | Fluxo | Diagrama bom, mas genérico e sem contexto ("só está bonito") |
| D1.4 | Gatilhos | Ok |
| D1.5 | Objetos | "Não identificado na base analisada" |
| D1.6 | Classes | Parecem certas, mas o papel é o mesmo para todas |
| D1.7 | Componentes de integração | "Não identificado". Muito improvável que esteja certo |
| D1.8 | Custom Metadata | "Não identificado". Muito improvável que esteja certo |
| D1.9 | Flows | "Não identificado" |
| D1.10 | LWC | "Não identificado", **embora a seção Gatilhos aponte um LWC como gatilho da integração**. Contradição interna |
| D1.11 | Profiles e Permission Sets | Ok, mas com pouco contexto |
| D1.12 | Tratamento de erros | Diz que está descrito em `etapas.csv`; deveria estar no documento (não é prioridade agora) |
| D1.13 | Pontos em aberto | Não fica claro o que fazer com cada item |
| D1.14 | Apêndice — Rastreabilidade | Tabela toda quebrada (classes, arestas etc.) |
| D1.15 | Ponte com outra integração | Seções da integração relacionada foram criadas com o nome e o objetivo, mas **todas** com o texto padrão "seção preenchida pelos CSVs da integração; quando não há evidência específica, a lacuna permanece explícita" |

---

## Avaliação preliminar — problemas estruturais e pontos de refatoração

> Hipóteses a confirmar com os artefatos da execução. Ordenadas por impacto.

### P1. As restrições da clusterização vazaram para a documentação ⭐ (explica D1.5, D1.7–D1.10, D1.15)
- A Fase 4 monta o recorte a partir da **matriz de assuntos** (ALTA/MEDIA) e trata INFRA/HUB_DADOS como "apenas citados".
- Depois da regra 24 (campo → objeto), os objetos ganharam fan-in alto e tendem a virar **HUB_DADOS**. Assim, **saem do recorte**, e a seção Objetos fica vazia.
- Named Credentials, Custom Metadata, LWC e Flows podem nem estar na matriz: chegam por arestas de configuração, por sistemas `SIS::`, por arestas LWC→Apex (direção inversa) ou com score BAIXA.
- **Erro de desenho:** INFRA/HUB_DADOS e os limiares existem para **não espalhar assunto** na Fase 3. Para **documentar uma integração**, o critério certo é outro: tudo o que os componentes da integração tocam diretamente.
- **Refatoração:** na Fase 4, as seções técnicas são montadas a partir da **vizinhança direta dos componentes das etapas** (`etapas.csv`), usando `edges.csv` sem filtro de INFRA/HUB, e de `fase1/componentes_integracao.csv` (campo `usado_por`). Para cada componente da integração: objetos e campos (SOQL/DML), Named Credentials (`callout:`), Custom Metadata (`getInstance`/SOQL em `__mdt`), Flows que chamam ou são chamados, LWC/Aura que chamam as classes (aresta inversa), Profiles/Permission Sets (arestas de acesso). A matriz serve só para decidir **quais integrações** pertencem à sigla.

### P2. O texto padrão substituiu o conteúdo, e a validação não percebeu ⭐ (explica 7, 8, D1.5–D1.10, D1.15)
- A F4-A07 só verifica se a seção existe e não está vazia; um texto padrão passa. A F4-A08 não pegou a diferença entre CSV e documento (ou não foi implementada de verdade).
- **Refatoração:**
  - Lista de frases proibidas (remissão genérica a CSVs, "a lacuna permanece explícita" etc.).
  - "Não identificado" só é permitido se o CSV da seção tiver 0 linhas **e** uma busca dirigida no código também não encontrar nada; a busca precisa ser registrada.
  - **Verificação de consistência entre seções:** todo componente citado em Gatilhos/Etapas/Fluxo aparece na seção do seu tipo (o LWC do gatilho precisa aparecer na seção LWC).
  - Detectar parágrafos idênticos repetidos em várias seções ou documentos.
  - Contagem: linhas do CSV = linhas da tabela no documento.

### P3. As tabelas deveriam ser geradas por script, não escritas pelo Devin ⭐ (explica 7, 8, D1.14, D1.15)
- Hoje o Devin "escreve" o documento inteiro. Em volume grande, ele tende a resumir e a usar texto padrão.
- **Refatoração:** separar em dois passos.
  1. **Renderização determinística** (script): todas as tabelas de seção são geradas a partir dos CSVs, com o mesmo layout do modelo.
  2. **Redação** (Devin): só as partes narrativas (resumo, ficha, papel das classes, tratamento de erros, pontos em aberto), com fatos obrigatórios.
- Isso garante que nenhum dado levantado se perca no caminho até o documento.

### P4. Falta de contexto de negócio (explica 2, 3, D1.1–D1.3, D1.11)
- O prompt não manda usar a `descricao` do `assuntos.csv`, o `conceito` do glossário, os labels dos objetos e campos, nem os nomes dos sistemas externos.
- **Refatoração:**
  - **Fatos obrigatórios** no resumo e na ficha: processo de negócio, quem ou o que dispara, sistema externo (nome), objetos de negócio (label), o que é enviado/recebido e o resultado para o negócio.
  - **Teste anti-genérico:** se o texto continuar fazendo sentido trocando o nome da integração por outro, está genérico e precisa ser reescrito. Verificação mínima: o resumo cita pelo menos o sistema externo, um objeto de negócio e o gatilho.
  - Diagramas: os nós precisam ser os componentes, objetos e sistemas reais, com rótulos de negócio.

### P5. Papel das classes sem critério (explica D1.6)
- **Refatoração:** taxonomia de papéis derivada da evidência no código, por exemplo: endpoint REST/SOAP (`@RestResource`, `webservice`), cliente de callout (`HttpRequest`/`callout:`), processamento assíncrono (Queueable/`@future`/Batch/Schedulable), trigger handler, consulta (selector/SOQL), transformação/mapeamento (DTO/wrapper/serialização JSON), ação invocável (`@InvocableMethod`), controller de LWC/Aura (`@AuraEnabled`). Cada classe recebe o papel **com a evidência** que o justifica, mais uma frase do que ela faz **nesta** integração.

### P6. Tabelas quebradas no Markdown (explica D1.14)
- Causa provável: a convenção do projeto separa listas dentro dos CSVs com `|`, que é o mesmo caractere de coluna das tabelas Markdown. Os caminhos de explicação também podem ter caracteres que quebram a tabela.
- **Refatoração:** ao renderizar, escapar `|` (`\|`) ou trocar por `; `. Verificação: todas as linhas de cada tabela com o mesmo número de colunas.

### P7. Integração com ponte para outra (explica D1.15)
- A ponte deve ser uma **referência** ("esta integração aciona / é acionada por INTnn", com link) e não uma cópia das seções da outra integração.
- **Refatoração:** em `integracoes.csv`, coluna `relacionada_a` (INTnn e tipo de relação); no documento, uma seção "Integrações relacionadas", só com links.

### P8. Seções que remetem a CSVs (explica D1.12)
- **Refatoração:** proibir remissão a arquivos de trabalho (`*.csv`) no texto dos documentos; o conteúdo precisa estar no documento.

### P9. Pontos em aberto sem ação (explica 6, D1.13)
- **Refatoração:** tabela com item, impacto, ação sugerida, quem pode responder e evidência/origem.

### Checagens a fazer na execução atual (para confirmar as hipóteses)
1. `fase4/<SIGLA>/secoes/objetos.csv`, `componentes_integracao.csv`, `lwc.csv`: têm linhas para essa integração? (Confirma P1 x P3.)
2. O LWC do gatilho está em `fase3/matriz_componente_assunto_aprovado.csv`? Com qual confiança? Está no `recorte.csv`?
3. Os objetos usados pela integração estão como HUB_DADOS em `fase2/infra_hubs_aprovado.csv`? (Confirma P1.)
4. O que a F4-A07 e a F4-A08 reportaram no `validation_report.md` da sigla? (Confirma P2.)
