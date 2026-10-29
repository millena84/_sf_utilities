# Feedback da Fase 4 — execução de teste (2026-10-29)

> Status: **parte 1 registrada** (README por sigla). Aguardando a parte 2: análise dos documentos por integração.
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

_(aguardando)_
