<!--
Esqueleto 2 de 2 — documento específico por INTEGRAÇÃO.
Fornecido pela revisora em 2026-10-30, a partir da documentação modelo montada manualmente.
Registrado aqui sem alterações de conteúdo; servirá de base para refatorar Fase M, Fase 4 e template.

Regras de marcação informadas:
- !!!SUCCESS → o componente/metadado É usado na integração; explicar por que é usado.
- !!!ABSTRACT → o componente/metadado NÃO é usado na integração; explicar por que, no funcionamento técnico, ele não é necessário.
-->

# {SIGLA} - {acaoRelacionadaIntegracao}

## 0. Cartão

| Informação                   | Valor                        |
|-------------------------------------|-------------------------------|
| Objetivo                          | {explicacao_breve}|
| Tipo de integração       | {inbound/outbound}|
| Sincronismo                  | {sync/async}|
| Dependências               | {lista_breve_se_houver}|


!!!SUCCESS Consulta técnica nos artefatos da sigla {SIGLA}, repositório {ALIAS_REPO}
         {Comentarios_Relevantes}
         Jornadas aqui detalhadas:
          - {aliasIntegracao01Sigla}
          - ...
          - {aliasIntegracaoNnSigla}
         Data revisão:dd/mm/aaaa

---

## INDICE
{tabela_indice_secoes_com_link}

| Seção | O que buscar |

---

## Visão geral por passo

| Passo     |  Gatilho        | Componentes principais | Saída / situação |
|----------------|--------------------|---------------------------------------------------------|----------------------------|
|{descricao_passo_breve}|{descricao_gatilho_breve}|{lista_ordem_componentes_principais_separados_por_seta}|{explicacao_breve_saida}|

---

## 1. Primeiro, os objetos do workflow

{mostrar_forma_simples_de_ler_a_dinamica}

---

## 2. Ciclo de vida de execução

| Fase     | O que acontece |  Quem atua    |
|-------------|---------------------------|-----------------------|
| {aliasFase} | {descricao_breve_o_que_acontece} | {descricao_breve_quem_atua} |

Exemplo:
| Definição | O registro FNN_Carrinhos__c é criado e uma trigger é iniciada, que faz a chamada da apex API para consultar dados e enriquecer informações do carrinho. | Usuário atua cadastrando em tela. Ao salvar, ocorre o acionamento. |

---

## 3. Integrações dentro do ciclo

### 3.1. caminho da integração {aliasCurtoIntegracao}

<!-- diagrama mermaid que mostra nas caixas do topo, nome dos componentes que fazem da integração. As caixas têm, embaixo, linhas. Cada linha tem uma bolinha com um numero. Em cada bolinha tem uma seta no sentido de para onde a integração vai (quem é acionado) e na seta tem um alias relacionado (exemplo: after insert). Não será possível detalhar no nível desejado aqui, mas consigo mandar uma foto de exemplo -->

{no_final_secao_fazer_breve_explanação_didatica_sobre_os_dados_aqui_relacionados_que_aparecem_na_integração_de_alguma_forma}

---

## 4. Flows e automações declarativas

### 4.1. {labelFlow} - {explicacaoBrevissima}

<!-- Se alguma das integrações da sigla usar algum desses componentes com esses objetivos, ou algo semelhante, explica nessa seção -->

{fazer_breve_explanação_didatica_sobre_esses_componentes_que_aparecem_na_integração_de_alguma_forma}

### 4.2. Sucesso / Conclusão / Avanço / Tratamentos de falha

{fazer_breve_explanação_didatica_sobre_esses_componentes_que_aparecem_na_integração_de_alguma_forma_como_trata_sucesso_e_falha_e_o_que_acontece_em_cada_caso}

### 4.3. Retry - integração (?)

<!-- Se alguma das integrações da sigla usar algum desses componentes com esses objetivos, ou algo semelhante, explica nessa seção -->

{fazer_breve_explanação_didatica_sobre_esses_componentes_que_aparecem_na_integração_de_alguma_forma}

|  Componente | Regra/efeito |
| {quem_tentou} | {o_que_pode_acontecer} |

---

## 5. Ordem, limites e reprocessamento

<!-- Se alguma das integrações da sigla usar algum desses componentes com esses objetivos, ou algo semelhante, explica nessa seção -->

{fazer_breve_explanação_didatica_sobre_esses_isso_dentro_da_dinamica_da_integração_de_alguma_forma}

---

## Anexo A - Evidências

| Ref | Arquivo/linha | O que comprova |
