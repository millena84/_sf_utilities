# Fase 4R — Leitura crítica dos documentos (org <ORG>, sigla <SIGLA>)

> Rodar **depois da Fase 4 de cada sigla**, **numa sessão nova do Devin** (sem o contexto de quem escreveu os documentos).
> Objetivo: impedir que documentos sem qualidade cheguem ao fim do processo. Os documentos são testados por quem vai usá-los.

## Antes de começar
Leia o `config.json` na raiz da pasta de trabalho e siga `<DIR_TRABALHO> [busque no arquivo config.json]/_projeto/00_regras_gerais.md` (seções 5, 9 e 13).

## Parâmetros desta execução
- ORG: `<ORG> [busque no arquivo config.json]` · CAMINHO_ORG: `<CAMINHO_ORG> [busque no arquivo config.json]` · DIR_TRABALHO: `<DIR_TRABALHO> [busque no arquivo config.json]`
- SIGLA: `<SIGLA> [busque no arquivo config.json]` · MODO_TESTE: `<MODO_TESTE> [busque no arquivo config.json]`

## Papel que você assume
Você é uma **pessoa do time de sustentação/plataforma Salesforce** que **nunca viu esta sigla**. Você recebeu os documentos em `docs/<SIGLA>/` e precisa, **só com eles**:
1. **Entender** como cada integração funciona;
2. **Rastrear** um problema (ex.: "a integração parou de atualizar o registro");
3. **Intervir** (ex.: trocar um endpoint, renovar um certificado, reprocessar uma falha).

## Regras da leitura
- **Etapa 1 (leitura cega):** leia **somente** os documentos de `docs/<SIGLA>/`. É **proibido** abrir dossiês, CSVs, `interpretacao.md` ou qualquer arquivo de `fase0`–`fase4` nesta etapa. Responda só com o que os documentos dizem.
- **Etapa 2 (conferência):** só então abra o código em `CAMINHO_ORG` para conferir se as respostas da etapa 1 estão **corretas**.
- Não corrija nada durante as etapas 1 e 2. Apenas registre.

## P. Pré-checagem
- `fase4/<SIGLA>/validation_report.md` com `APROVADO PARA REVISÃO HUMANA`.
- Existem o inventário técnico (`<SIGLA>_inventario_tecnico.md`) e ≥1 documento por integração.
- Falhou → `fase4R/<SIGLA>/PRECHECK_FALHOU.md` e encerre.

## Etapa 1 — Questionário (leitura cega)
Para **cada integração**, responda às perguntas abaixo usando só os documentos.

| # | Perspectiva | Pergunta |
|---|---|---|
| Q01 | Entender | Em 2 frases, o que esta integração faz para o negócio? |
| Q02 | Entender | O que a dispara (quem/qual evento) e qual o resultado final? |
| Q03 | Entender | Com qual sistema externo ela fala, em que sentido (inbound/outbound) e de forma síncrona ou assíncrona? |
| Q04 | Entender | Quais objetos e campos ela lê ou altera, e o que cada objeto representa? |
| Q05 | Entender | Qual a sequência de componentes, do gatilho ao resultado? |
| Q06 | Rastrear | Se o registro não foi atualizado, em que pontos procurar (componentes, logs, status)? |
| Q07 | Rastrear | O que acontece quando a chamada falha? Onde a falha fica registrada? |
| Q08 | Rastrear | Existe retry? Quem tenta de novo, quantas vezes e quando? |
| Q09 | Intervir | Onde está configurado o endpoint e o que alterar para trocá-lo (por ambiente, se houver)? |
| Q10 | Intervir | Como a autenticação é feita e onde estão Named Credential / External Credential / certificado (com vencimento)? |
| Q11 | Intervir | Qual usuário/perfil/permission set a integração usa? |
| Q12 | Intervir | Como reprocessar uma falha? |
| Q13 | Intervir | Se eu alterar o componente principal desta integração, que outras integrações são afetadas? |
| Q14 | Intervir | O que precisa ser verificado na org porque o repositório não confirma (DANGER)? |

Para cada resposta registre:
- `encontrado`: **sim** (resposta completa), **parcial** (incompleta ou vaga) ou **não** (o documento não responde);
- `secao`: onde a resposta estava;
- `cliques`: quantas navegações (links/seções) foram necessárias;
- `resposta`: o que o documento diz.

## Etapa 2 — Conferência com o código
Para cada resposta `sim` ou `parcial`, abra o código e marque `correta` (**sim / não / não verificável**), com a evidência `arquivo:linha`.

## Etapa 3 — Qualidade do texto
Para cada documento, avalie:
- **Teste anti-genérico** (seção 13 das regras): algum trecho serviria para qualquer integração? Liste-os.
- **Marcações:** algum SUCCESS/ABSTRACT/DANGER com motivo vago ("não encontrado", "não se aplica" sem explicação técnica)?
- **Seções vazias ou de remissão** ("ver arquivo", "não identificado").
- **Diagramas:** ajudam a entender o fluxo ou só repetem a tabela?

## Saídas (`fase4R/<SIGLA>/`)
- `questionario.csv` — `id_integracao,pergunta,encontrado,secao,cliques,resposta,correta,evidencia`
- `problemas.csv` — `id_problema,documento,secao,tipo(lacuna|incorreto|generico|marcacao_vaga|navegacao|diagrama),descricao,correcao_sugerida,gravidade(alta|media|baixa)`
- `leitura_critica.md` — placar por integração (perguntas sim/parcial/não; corretas), os 5 problemas mais graves e a conclusão:
  **APTO** (pode seguir para revisão humana) ou **NÃO APTO** (voltar à Fase 4 com `problemas.csv`).

## Critério de aptidão
Uma integração é **APTA** quando:
- Q01–Q05, Q07, Q09 e Q10 estão `sim` **e** `correta = sim`;
- nenhuma resposta está `correta = não`;
- no máximo 2 perguntas `parcial` no total;
- nenhum problema de gravidade **alta** em `problemas.csv`.

A sigla é **APTA** quando todas as integrações são aptas e o inventário técnico responde Q09, Q10, Q13 e Q14 para todas.

## Ciclo de correção
Se **NÃO APTO**: rode de novo a Fase 4 da sigla informando `fase4R/<SIGLA>/problemas.csv` como lista de correções obrigatórias e, depois, uma **nova sessão** da Fase 4R. No máximo 2 ciclos; persistindo, registre em `questions.md` e leve para a revisão humana com o placar.

## Autovalidação — `tools/fase4R/validate_fase4R.py`

| ID | Verificação | Severidade |
|---|---|---|
| F4R-A01 | Pré-checagem executada e aprovada | BLOQUEANTE |
| F4R-A02 | Todas as perguntas respondidas para todas as integrações | BLOQUEANTE |
| F4R-A03 | Toda resposta `correta = sim/não` tem evidência `arquivo:linha` reverificada | BLOQUEANTE |
| F4R-A04 | Declaração de que a etapa 1 não abriu arquivos de trabalho (dossiês, CSVs, faseN/) | BLOQUEANTE |
| F4R-A05 | Conclusão APTO/NÃO APTO coerente com o critério de aptidão | BLOQUEANTE |
| F4R-A06 | Entrada da Fase 4R em `decisions.md` | BLOQUEANTE |

## Entrega
`questionario.csv`, `problemas.csv`, `leitura_critica.md`, `validation_report.md` e `RESUMO_FASE4R.md` em `fase4R/<SIGLA>/`.
**Nenhum arquivo `_aprovado` nesta fase.** A revisora lê `leitura_critica.md` antes de revisar os documentos.
