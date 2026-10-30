<!--
Esqueleto 1 de 2 — documento por SIGLA ("inventário técnico de integração").
Fornecido pela revisora em 2026-10-30, a partir da documentação modelo montada manualmente.
Registrado aqui sem alterações de conteúdo; servirá de base para refatorar Fase M, Fase 4 e template.

Regras de marcação informadas:
- !!!SUCCESS → o componente/metadado É usado na integração; explicar por que é usado.
- !!!ABSTRACT → o componente/metadado NÃO é usado na integração; explicar por que, no funcionamento técnico, ele não é necessário.
-->

# {SIGLA} - inventário técnico de integração

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

## 1. Resumo executivo e limites da cadeia

{tabela_com_informacoes}

| Caminho | Entrada | Saída |
exemplo:
| rolima     | inclusão tabela VEIC | GET api meu_veic |

{diagrama_mermaid_basico_fluxo_integracao}

---

## 2. Modelo de dados para consulta rápida

| objeto |  Papel a sigla |

Exemplo:
| FNN_Carrinhos__c | Dados dos carrinhos. Enriquecido com API meu_veic |

---

## 3. Catálogo dos Flows

### 3.1. Roteador de tela de etapas

<!-- Se alguma das integrações da sigla usar flow screen, triggered ou algo semelhante, explica nessa seção -->

{no_final_secao_fazer_breve_explanação_didatica_sobre_flows_que_aparecem_na_integração_de_alguma_forma}

| Ação sistêmica / de negócio | Tipo flow usado | nome técnico |

## 3.2. Flow de tratamento / conclusão

<!-- Se alguma das integrações da sigla usar flows de outros tipos, ou algo semelhante, explica nessa seção -->

| Flow | Objeto / tipo disparo | Efeito esperado |

{no_final_secao_fazer_breve_explanação_didatica_sobre_flows_que_aparecem_na_integração_de_alguma_forma}

3.3. Flows de retry / upload / outro (?)

<!-- Se alguma das integrações da sigla usar flows com esses objetivos, ou algo semelhante, explica nessa seção -->

| Flow | Objeto / tipo disparo | Efeito esperado |

{no_final_secao_fazer_breve_explanação_didatica_sobre_flows_que_aparecem_na_integração_de_alguma_forma}

---

## 4. Inventário Triggers, Apex e LWC

<!-- Se alguma das integrações da sigla usar algum desses componentes com esses objetivos, ou algo semelhante, explica nessa seção -->

| Entrada / camada | Componentes principais | Papel |

{no_final_secao_fazer_breve_explanação_didatica_sobre_esses_componentes_que_aparecem_na_integração_de_alguma_forma}

---

## 5. UI, permissões e metadata Salesforcec (?)

<!-- Se alguma das integrações da sigla usar algum desses componentes com esses objetivos, ou algo semelhante, explica nessa seção -->

| Tipo componente | API Name / registro | Estado do componente no repositório |

{no_final_secao_fazer_breve_explanação_didatica_sobre_esses_componentes_que_aparecem_na_integração_de_alguma_forma}

---

## 6. Configurações de integração

### 6.1. {aliasIntegracao01Sigla}

#### Connected App / External ClientApp

!!!ABSTRACT Não encontrado metadado {metadataType} associado nessa integração
          {explicacao_motivo_metadataType_nao_usado_nessa_integracao}

#### Certificado

!!!ABSTRACT Não encontrado metadado {metadataType} associado nessa integração
         { explicacao_motivo_metadataType_nao_usado_nessa_integracao}

#### Remote Site Settings

!!!SUCCESS label do componente
       {       explicacao_motivo_metadataType_nao_usado_nessa_integracao}

#### Endpoints

!!!SUCCESS
     { tipo_componente_onde_os_endpoints_estao_configurados}
     Tipo registro?
     Nome endpoint?

{explicacao_como_usa_endpoint_na_integracao}

#### Named Credential

!!!ABSTRACT Não encontrado metadado {metadataType} associado nessa integração
       { explicacao_motivo_metadataType_nao_usado_nessa_integracao}

#### External Credential

!!!ABSTRACT Não encontrado metadado {metadataType} associado nessa integração
       { explicacao_motivo_metadataType_nao_usado_nessa_integracao}

### 6.n [ repete_rastreio_informações_seção_para_cada_integracao_sigla]

---

## 7. Escopo e pontos de validação

### 7.1. Validações que exigem estado vivo da org (?)
{lista}
<!-- avaliar se faz sentido -->

### 7.2. Observações técnicas e de configuração
{lista}
<!-- avaliar se faz sentido -->

---

## Anexo A - Fontes principais no repositório
