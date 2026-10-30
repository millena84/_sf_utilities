# Regras gerais do projeto — Documentação de Jornadas de Integração

> Este arquivo vale para TODAS as fases. Toda sessão do Devin deve lê-lo antes de qualquer ação.
> Fica em `<DIR_TRABALHO> [busque no arquivo config.json]/_projeto/00_regras_gerais.md`.

---

## 0. Configuração — `config.json`

- Todos os parâmetros das execuções ficam no arquivo **`config.json`, na raiz da pasta de trabalho** (`DIR_TRABALHO`). Modelo: `config.exemplo.json`.
- Nos prompts, `<CHAVE> [busque no arquivo config.json]` significa: **leia o valor da chave no `config.json`**. Nunca suponha valores.
- No início de toda fase, leia o `config.json` e registre no relatório os valores usados. Chave obrigatória ausente ou vazia → `PRECHECK_FALHOU.md` e encerre.

| Chave | Uso | Fases |
|---|---|---|
| `ORG` | Apelido da org; nome da subpasta de resultados | Todas |
| `CAMINHO_ORG` | Pasta com os metadados da org (somente leitura) | 0–4 |
| `DIR_TRABALHO` | Pasta onde o Devin escreve tudo | Todas |
| `ALIAS_REPO` | Nome do repositório exibido no cabeçalho dos documentos | 4, 5 |
| `MODO_TESTE` | `sim` / `não` (ver seção 7) | Todas |
| `DATA_REFERENCIA` | Data da execução (AAAA-MM-DD). Usada no vencimento de certificados e na "Data revisão" dos documentos | 1, 4, 5 |
| `SIGLA_MODELO` | Sigla documentada no modelo de referência. **Não muda entre execuções** | M, 3, 4 |
| `ORG_DO_MODELO` | Org do modelo de referência | M, 3 |
| `SIGLA` | Sigla documentada nesta execução da Fase 4 (ou id de assunto sem sigla) | 4 |
| `CALIBRACAO` | Parâmetros numéricos (seção 10) | 0–3 |

## 1. Contexto

Estamos documentando as integrações de orgs Salesforce antigas e complexas, a partir da cópia local do
repositório Flosum de produção de cada org (estrutura de projeto Salesforce: uma pasta por tipo de metadata).
O objetivo final são **dois tipos de documento por sigla**: o **inventário técnico da sigla** ("o que existe") e um **documento por integração** ("como funciona").
Cada execução trabalha com **uma org por vez**.

## 2. Definições

| Termo | Definição |
|---|---|
| Componente | Item de metadata identificável (classe, trigger, flow, objeto, campo, named credential etc.) |
| Assunto | Tema de negócio da lista `assuntos.csv` |
| Sigla | Unidade de documentação do time (coluna `sigla` do `assuntos.csv`); agrupa um ou mais assuntos |
| Ponto de integração | Componente onde há troca de dados com o mundo externo à org |
| Integração | Troca com um sistema externo com gatilho e resultado próprios. Uma sigla tem uma ou mais integrações, que juntas formam a jornada |
| INBOUND / OUTBOUND | Externo → Salesforce / Salesforce → externo |
| EVENTO | Troca via Platform Event / Change Data Capture |
| INBOUND_PRESUMIDO | Indício de entrada via API padrão (ex.: campo External ID), sem código que comprove |
| Infraestrutura (INFRA) | Componente técnico transversal (logger, wrapper HTTP, trigger handler base) |
| Hub de dados (HUB_DADOS) | Objeto/campo usado por muitos assuntos (ex.: Account) |
| Dossiê da integração | Conjunto completo de componentes, configurações e evidências de uma integração, montado na Fase 4 **sem os filtros da Fase 3** |
| Modelo de referência | Documentação feita pelo time (sigla `SIGLA_MODELO`). Fonte de **estilo e exemplos**, nunca de texto |
| Esqueletos oficiais | `_projeto/templates/01_inventario_tecnico_sigla.md` e `02_documento_por_integracao.md`. Definem a **estrutura** dos documentos |

**Importante:** INFRA, HUB_DADOS, limiares e confiança existem **apenas para a Fase 3** (não espalhar assunto). Eles **nunca** limitam o que entra na documentação.

## 3. Restrições de ambiente — INEGOCIÁVEIS

- **PROIBIDO** executar `sf`, `sfdx` ou qualquer Salesforce CLI.
- **PROIBIDO** conectar a qualquer org, fazer deploy/retrieve ou chamar endpoints encontrados no código.
- A única fonte de verdade são os arquivos locais em `<CAMINHO_ORG> [busque no arquivo config.json]`. **Somente leitura**.
- Ferramentas: Python 3 com biblioteca padrão, `grep`, `find`. Pacote extra → registrar em `decisions.md`.
- Todo processamento é feito por **scripts reexecutáveis** em `<DIR_TRABALHO>/<ORG>/tools/faseN/`.
  **Leia os insumos a cada execução**; nunca deixe regras ou listas fixas no código quando elas vêm de um arquivo.

## 4. Autonomia e registro

- Execute a fase inteira **sem parar para perguntar**.
- Decisão não trivial: escolha a opção **mais conservadora** e registre em `<ORG>/decisions.md` (fase, decisão, alternativas, motivo).
- Dúvida que só o time responde: `<ORG>/questions.md` (fase, pergunta, contexto, impacto, opção adotada provisoriamente).
- **Toda fase registra pelo menos uma entrada** em `decisions.md` (nem que seja "nenhuma decisão não trivial nesta fase"). O validador verifica.
- Nunca invente: sem evidência, registre a ausência e o que foi pesquisado.

## 5. Evidência e confiança

- Toda afirmação técnica cita evidência `caminho/relativo/arquivo:linha` (relativo à raiz da org).
- Confiança: **ALTA** (evidência direta), **MEDIA** (relação comprovada entre componentes), **BAIXA** (indício textual).
- Afirmação sem evidência direta → **[INFERIDO]** + justificativa de 1 frase.

## 6. Convenções de arquivos de trabalho

- IDs: `Tipo::NomeApi`; subcomponente `Tipo::Pai.Nome`; sistema externo `SIS::NomeCurto`; assunto `ASS-001`…; integração `INTnn`.
- CSV: UTF-8, vírgula, aspas quando necessário, cabeçalho, ordenação determinística. Listas dentro de uma célula separadas por `|`.
- Reexecutar um script produz arquivos **idênticos** (amostras com `seed=42`; sem timestamps nos CSV).

## 7. Revisão humana e aprovações

- Arquivos de decisão humana têm sufixo `_proposto` e colunas `status_revisao` (`pendente`|`aprovado`|`rejeitado`|`ajustado`) e `comentario_revisao`. O Devin sempre gera com `pendente`.
- A revisora salva como `_aprovado`. **Nenhuma fase escreve em arquivos `_aprovado`.** Fases seguintes leem só linhas `aprovado`/`ajustado` do `_aprovado`.
- **MODO_TESTE = sim:** na ausência do `_aprovado`, use o `_proposto` tratando `pendente` como `aprovado`, e marque todo relatório e documento com `⚠ NÃO VALIDADO — gerado em MODO_TESTE`.

## 8. Autochecagem (todas as fases)

1. **Pré-checagem (etapa P):** `config.json` lido; insumos existem com as colunas esperadas; `_aprovado` sem `pendente` (exceto MODO_TESTE); `validation_report.md` da fase anterior sem BLOQUEANTE com FALHOU. Falhou → `faseN/PRECHECK_FALHOU.md` e encerre.
2. **Validação final:** `tools/faseN/validate_faseN.py`, cobrindo todos os checks `FN-Axx` do prompt.
3. Severidade: **BLOQUEANTE** ou **ALERTA**. BLOQUEANTE falhou → corrigir e rodar de novo (até 3 tentativas); persistindo, entregar REPROVADO com explicação.
4. **Reverificação de evidências:** todo `arquivo:linha` citado existe e contém o símbolo citado.
5. `faseN/validation_report.md`: linha 1 `Resultado geral: APROVADO PARA REVISÃO HUMANA` ou `REPROVADO`; tabela `| ID | Verificação | Severidade | Resultado | Números | Observação |`; lista de ALERTAS com o arquivo a olhar.

## 9. Segurança

- Nunca copie senhas, tokens, chaves, client secrets, conteúdo de certificados, valores de Custom Settings/Custom Metadata que pareçam credenciais, nem URLs com credencial.
- Endpoints: apenas nome do componente/registro e **domínio** (host). Certificados: apenas nome e data de vencimento.
- Profiles/Permission Sets: apenas os acessos relevantes, nunca o arquivo inteiro.
- Toda fase valida que nenhum artefato contém esses padrões.

## 10. Calibração

Valores em `config.json` → `CALIBRACAO`. Se ausentes, usar: `AMOSTRA_REVISAO`=10 · `ALERTA_REFS_NAO_RESOLVIDAS`=20% · `LIMIAR_INFRA_FAN_IN`=percentil 95 · `MAX_SALTOS`=3 · `DECAIMENTO`=0.6 · `FATOR_RELACAO_FRACA`=0.5 · `LIMIAR_ALTA`/`LIMIAR_MEDIA`=0.7/0.4 · `ALERTA_ASSUNTO_GIGANTE`=15% · `ALERTA_VENCIMENTO_DIAS`=90.

## 11. Estrutura de pastas

```
<DIR_TRABALHO>/
  config.json
  _projeto/            00_regras_gerais.md
    templates/         01_inventario_tecnico_sigla.md, 02_documento_por_integracao.md (esqueletos oficiais)
    guia_estilo.md     (gerado na Fase M)
    base_de_conhecimento/  (cópia de documentacaoInt/base_de_conhecimento/, seção 14)
  _entradas/           tipos_metadata.txt, assuntos.csv, gabarito_<ORG>.csv
    modelo_referencia/ documentos do modelo feito pelo time
  _modelo/             saídas da Fase M
  <ORG>/
    tools/faseN/       scripts
    fase0/ .. fase5/   artefatos de trabalho + revisao/ + validation_report.md + RESUMO_FASEN.md
    docs/<SIGLA>/      documentos finais (Fase 4)
    docs/              índice e catálogos (Fase 5)
    decisions.md, questions.md
  _consolidado/        consolidação entre orgs (Fase 5B)
```

## 12. Templates e modelo

1. **Estrutura:** os esqueletos oficiais em `_projeto/templates/`. Seções, ordem e títulos são seguidos exatamente.
2. **Estilo e exemplos:** `_projeto/guia_estilo.md` (gerado na Fase M a partir do modelo do time).
3. **Proibido copiar** texto do modelo de referência para qualquer documento.

## 13. Regras de escrita dos documentos finais

- **Marcações** (sintaxe idêntica à do modelo, registrada em `_modelo/sintaxe_blocos.md`):

| Marcação | Quando | Conteúdo obrigatório |
|---|---|---|
| `!!!SUCCESS` | O componente **é usado**, com evidência | Por que a integração o usa |
| `!!!ABSTRACT` | O componente **não é usado**, com justificativa técnica | Por que, no funcionamento técnico, ele não é necessário |
| `!!!DANGER` | O repositório **não permite confirmar** | O que foi encontrado, por que não dá para confirmar e o que verificar na org. Todo DANGER entra também na seção 7.1 do documento da sigla |

- **Proibido** nos documentos: "não identificado na base analisada" como resposta pronta; remissões genéricas ("ver CSVs", "a lacuna permanece explícita", "conteúdo detalhado nos arquivos de seção"); menção a arquivos de trabalho (`*.csv`, pastas `faseN/`); o mesmo parágrafo repetido em seções diferentes.
- **Teste anti-genérico:** se o texto continuar fazendo sentido trocando o nome da integração por outro, ele está genérico e deve ser reescrito com fatos (sistema externo pelo nome, objeto pelo label, gatilho, o que é enviado/recebido, resultado).
- **Tabelas Markdown:** escapar `|` dentro das células (`\|`) ou trocar por `; `. Todas as linhas com o mesmo número de colunas.
- **Tabelas são geradas por script** a partir do dossiê; **textos explicativos** são escritos a partir da leitura do código.

## 14. Base de conhecimento de integração

Material de consulta em `<DIR_TRABALHO>/_projeto/base_de_conhecimento/` (cópia de `documentacaoInt/base_de_conhecimento/`). Prefira os arquivos JSON quando um script for consumir o conteúdo.

| Arquivo | Use para |
|---|---|
| `guia_evidencias.md` | reconhecer componentes nos arquivos: pasta, sufixo, campos XML, padrões de código `C01`–`C25`, campos sensíveis |
| `regras_ligacao.md` | seguir de um componente ao próximo: regras `L01`–`L47` (documentado × heurística) |
| `diagnostico.md` | do sinal encontrado ao desenho candidato: sinais `S01`–`S38` e assinatura mínima de cada desenho |
| `out-sync.md`, `in-sync.md`, `out-async.md`, `in-async.md`, `mid.md`, `outras.md` | desenhos e variantes (ex.: `D.1.v11`) com os componentes esperados |
| `limites_da_fonte.md` | o que o repositório não mostra (`N01`–`N17`) e como registrar |
| `antipadroes.md` | riscos a sinalizar (`A01`–`A18`) |
| `limites_plataforma.md` | limites da plataforma que afetam cada desenho |
| `exemplos/` | exemplos **fictícios** do método; nunca copie conteúdo deles |

Regras de uso:
- A base descreve **o que pode existir**. Só afirme que um componente existe com evidência em `<CAMINHO_ORG>` (seção 5).
- A confiança da documentação segue a seção 5. A confiança da matriz de diagnóstico vale só para escolher o desenho candidato.
- Regra de ligação do tipo **heurística** nunca sustenta sozinha uma afirmação ALTA.
- Itens marcados na base como "não confirmado" ou ⚠️ não podem ser usados como fato.
- Cite os IDs da base (`Cnn`, `Lnn`, `Snn`, `Ann`, `Nnn`, id de variante) nas colunas de observação e em `decisions.md`, para rastrear de onde veio cada decisão.
- **Marcações SUCCESS/ABSTRACT/DANGER (seção 13):** use a variante escolhida em `desenho_base` como referência do que a integração precisa. Componente que a variante não usa → ABSTRACT citando a variante (ex.: "no desenho `D.1.v2` o endpoint vem da Named Credential; Remote Site não é necessário"). Componente obrigatório na variante e não encontrado, ou informação que o repositório não mostra (`Nnn` de `limites_da_fonte.md`) → DANGER citando o id.

## 15. Entrega padrão de toda fase

`faseN/RESUMO_FASEN.md`: 1. O que foi feito · 2. Números principais · 3. Resultado da validação · 4. Pontos para revisão humana (item do checklist, arquivo, o que olhar) · 5. Decisões tomadas · 6. Dúvidas abertas · 7. Recomendação para a próxima fase.
