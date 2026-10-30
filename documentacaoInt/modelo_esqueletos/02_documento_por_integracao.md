<!--
Esqueleto 02 — documento por INTEGRAÇÃO — VERSÃO REFINADA (v2, 2026-10-30).
Base: esqueleto enviado pela revisora + decisões 1–7 de 00_decisoes_estrutura.md.
Mudanças em relação à v1:
- Seções 0 a 5 mantidas como enviadas (com placeholders completados).
- Nova seção 6 "Componentes técnicos": recebe os catálogos de Triggers/Apex/LWC/UI que saíram do documento da sigla.
- Nova seção 7 "Configurações de integração": mesmas marcações do documento da sigla (mesma fonte), com três marcações.
- Nova seção 8 "Integrações relacionadas": apenas links, nunca cópia de seções.
- Diagrama da seção 3.1: sequenceDiagram com autonumber.

Marcações (sintaxe idêntica à do modelo):
- !!!SUCCESS → é usado na integração; explicar por que é usado.
- !!!ABSTRACT → não é usado; explicar por que, no funcionamento técnico, não é necessário.
- !!!DANGER → o repositório não permite confirmar; dizer o que foi achado, por que não dá para confirmar e o que verificar na org.
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

<!-- Mermaid sequenceDiagram com autonumber: participantes no topo = componentes reais na ordem em que atuam (e o sistema externo pelo nome); setas numeradas no sentido de quem é acionado; rótulo da seta = evento ou ação (ex.: after insert, enqueueJob, POST /recurso). -->

{diagrama_mermaid_sequence_autonumber}

{no_final_secao_fazer_breve_explanação_didatica_sobre_os_dados_aqui_relacionados_que_aparecem_na_integração_de_alguma_forma}

---

## 4. Flows e automações declarativas

### 4.1. {labelFlow} - {explicacaoBrevissima}

<!-- Se a integração usar Flows (tela, record-triggered, agendado, autolaunched), explica nessa seção. Se não usar, uma frase dizendo por que não se aplica. -->

{fazer_breve_explanação_didatica_sobre_esses_componentes_que_aparecem_na_integração_de_alguma_forma}

| Flow | Tipo / disparo | Objeto | Efeito esperado |

### 4.2. Sucesso / Conclusão / Avanço / Tratamentos de falha

{fazer_breve_explanação_didatica_sobre_esses_componentes_que_aparecem_na_integração_de_alguma_forma_como_trata_sucesso_e_falha_e_o_que_acontece_em_cada_caso}

### 4.3. Retry - integração

<!-- Se a integração tiver retry, explica nessa seção. Se não tiver, uma frase dizendo como uma falha é tratada sem retry. -->

{fazer_breve_explanação_didatica_sobre_esses_componentes_que_aparecem_na_integração_de_alguma_forma}

|  Componente | Regra/efeito |
| {quem_tenta} | {o_que_pode_acontecer} |

---

## 5. Ordem, limites e reprocessamento

{fazer_breve_explanação_didatica_sobre_isso_dentro_da_dinamica_da_integração}

---

## 6. Componentes técnicos

<!-- Catálogo desta integração (saiu do documento da sigla). -->

### 6.1. Triggers e Apex

| Entrada / camada | Componente | Papel nesta integração |

{breve_explicacao_didatica_sobre_esses_componentes}

### 6.2. LWC, Aura e páginas

<!-- Se a integração tiver interface (LWC/Aura/FlexiPage/Quick Action), explica nessa seção. Se não tiver, uma frase dizendo por que não se aplica. -->

| Componente | Onde aparece | Apex que chama | Papel nesta integração |

### 6.3. Custom Metadata e configurações por ambiente

| Tipo (__mdt) | Registro | Finalidade | Campos relevantes |

---

## 7. Configurações de integração

<!-- Mesmas marcações do documento da sigla (mesma fonte). -->

#### Connected App / External ClientApp

!!!ABSTRACT Não encontrado metadado {metadataType} associado nessa integração
          {explicacao_motivo_metadataType_nao_usado_nessa_integracao}

#### Certificado

!!!ABSTRACT Não encontrado metadado {metadataType} associado nessa integração
         {explicacao_motivo_metadataType_nao_usado_nessa_integracao}

#### Remote Site Settings

!!!SUCCESS {label_do_componente}
         {explicacao_motivo_metadataType_usado_nessa_integracao}

#### Endpoints

!!!SUCCESS {tipo_componente_onde_os_endpoints_estao_configurados}
         Tipo registro: {tipo_registro}
         Nome endpoint: {nome_endpoint}

{explicacao_como_usa_endpoint_na_integracao}

#### Named Credential

!!!DANGER {o_que_foi_encontrado}
         {por_que_nao_da_para_confirmar}
         Verificar na org: {o_que_verificar}

#### External Credential

!!!ABSTRACT Não encontrado metadado {metadataType} associado nessa integração
         {explicacao_motivo_metadataType_nao_usado_nessa_integracao}

---

## 8. Integrações relacionadas

<!-- Somente links e o tipo de relação. Nunca copiar seções da outra integração. Se não houver, uma frase dizendo que a integração é independente. -->

| Integração | Relação | Documento |

---

## Anexo A - Evidências

| Ref | Arquivo/linha | O que comprova |
