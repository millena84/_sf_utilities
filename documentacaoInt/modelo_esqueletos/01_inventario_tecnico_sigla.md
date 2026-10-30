<!--
Esqueleto 01 — documento por SIGLA ("inventário técnico de integração") — VERSÃO REFINADA (v2, 2026-10-30).
Base: esqueleto enviado pela revisora + decisões 1–7 de 00_decisoes_estrutura.md.
Mudanças em relação à v1:
- Saíram os catálogos completos de Flows (antiga seção 3), Triggers/Apex/LWC (4) e UI/permissões/metadata (5):
  agora ficam no documento de cada integração (esqueleto 02).
- Entraram as seções "Acesso" e "Componentes compartilhados entre integrações".
- Configurações de integração com três marcações: SUCCESS, ABSTRACT e DANGER.
- "Validações que exigem estado vivo da org" recebe todos os DANGER.

Marcações (sintaxe idêntica à do modelo):
- !!!SUCCESS → é usado na integração; explicar por que é usado.
- !!!ABSTRACT → não é usado; explicar por que, no funcionamento técnico, não é necessário.
- !!!DANGER → o repositório não permite confirmar; dizer o que foi achado, por que não dá para confirmar e o que verificar na org.
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

{lista_documentos_da_sigla_com_link}

| Documento | Integração | O que buscar |

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

## 3. Configurações de integração

<!-- Mesmas marcações do documento de cada integração (mesma fonte). Link para a explicação detalhada no documento da integração. -->

### 3.1. {aliasIntegracao01Sigla}

{link_documento_integracao}

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

### 3.n {repete_para_cada_integracao_da_sigla}

---

## 4. Acesso

<!-- Usuário de integração, Profiles, Permission Sets e Permission Set Groups que dão acesso aos componentes das integrações da sigla. -->

| Tipo | Nome | Acesso concedido | Integrações |

{breve_explicacao_didatica_sobre_usuario_de_integracao_e_acessos}

---

## 5. Componentes compartilhados entre integrações

<!-- Componentes usados por mais de uma integração da sigla: alterar um deles afeta todas as listadas. -->

| Componente | Tipo | Integrações afetadas | Impacto de uma alteração |

---

## 6. Escopo e pontos de validação

### 6.1. Validações que exigem estado vivo da org

<!-- Todos os !!!DANGER da sigla, cada um com o que verificar na org. -->

| Integração | Item | O que verificar na org |

### 6.2. Observações técnicas e de configuração

<!-- Riscos e anti-padrões encontrados, limites relevantes e assuntos da sigla sem integração detectada (com o motivo). -->

{lista}

---

## Anexo A - Fontes principais no repositório

| Componente | Arquivo |
