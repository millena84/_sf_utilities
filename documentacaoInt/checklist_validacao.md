# Checklist de validação — todas as fases

> Para uso da revisora. Cada fase tem 3 blocos:
> **A. Portão** (2 min) · **B. Revisão humana** · **C. Liberação para a próxima fase**.
> ⭐ = item crítico: se o tempo for curto, faça pelo menos estes.
> Registre o resultado de cada item em `<ORG>/registro_validacao.md` (modelo no fim deste arquivo).

---

## Regras de ouro (valem para todas as fases)

1. **Nunca comece a revisão humana se o portão falhar.** Se o `validation_report.md` estiver REPROVADO, peça ao Devin para corrigir.
2. **Revise só o que o Devin preparou em `faseN/revisao/`.** As amostras já trazem o trecho do código, então não é preciso abrir os arquivos-fonte, exceto quando algo parecer errado.
3. **Aprovar = salvar o arquivo `_proposto` como `_aprovado`** com a coluna `status_revisao` preenchida em todas as linhas. A fase seguinte se recusa a rodar se houver `pendente`.
4. **Em caso de dúvida, use `ajustado` e escreva o comentário.** Nunca deixe uma linha em branco.
5. **Ao alterar um insumo de uma fase, rode de novo a fase e todas as seguintes.**

---

## FASE M — Modelo de referência (uma vez, antes da Fase 0)

### A. Portão
| ID | Verificar | Aceite |
|---|---|---|
| FM-G1 ⭐ | `_modelo/validation_report.md`: APROVADO, com 11 checks (FM-A01 a FM-A11) | Sim |
| FM-G2 | FM-A01: todos os arquivos do modelo foram lidos | Sim |

### B. Revisão humana
| ID | O que verificar | Arquivo | Como | Aceite | Se falhar |
|---|---|---|---|---|---|
| FM-H01 ⭐ | Estrutura capturada | `_modelo/revisao/comparativo_secoes.md` | Compare com o modelo: faltou alguma seção? A ordem está certa? | Igual ao modelo | Peça a correção |
| FM-H02 ⭐ | Regras das seções | `_projeto/template_extraido.md` | Cada regra descreve o que o time espera daquela seção (ex.: Profiles = só os acessos da integração)? | Sim | Edite o template direto ou peça a correção |
| FM-H03 | Guia de estilo | `template_extraido.md` | Tom, tamanho e nomenclatura batem com o modelo? | Sim | Edite |
| FM-H04 ⭐ | Mapa de seções | `_modelo/mapa_secoes_proposto.csv` | A fonte de cada seção faz sentido? | Nenhum pendente | Salve como `mapa_secoes_aprovado.csv` |
| FM-H05 ⭐ | Tipos faltantes | `_modelo/tipos_faltantes.csv` (só os que faltam) e `tipos_nome_divergente.csv` | Inclua em `_entradas/tipos_metadata.txt` os que fizerem sentido e corrija os nomes divergentes | Lista atualizada | — |
| FM-H06 | Lacunas | `_modelo/lacunas_modelo.md` | Alguma seção do modelo que o pipeline não consegue preencher? Aceite ou ajuste | Decidido | — |
| FM-H07 | Gabarito | `_modelo/gabarito_modelo.csv` | Os assuntos atribuídos estão corretos? | Sim | Corrija a coluna `assunto` |

### C. Liberação para a Fase 0
- [ ] `template_extraido.md` revisado
- [ ] `mapa_secoes_aprovado.csv` sem `pendente`
- [ ] `tipos_metadata.txt` atualizado

---

## FASE 0 — Reconhecimento

### A. Portão
| ID | Verificar | Onde | Aceite |
|---|---|---|---|
| F0-G1 ⭐ | Linha 1 diz `APROVADO PARA REVISÃO HUMANA` | `fase0/validation_report.md` | Sim |
| F0-G2 ⭐ | Os 17 checks F0-A01 a F0-A17 aparecem no relatório | idem | Todos presentes |
| F0-G3 | Cada ALERTA tem observação compreensível | idem | Sim |
| F0-G4 | Não existe `PRECHECK_FALHOU.md` | `fase0/` | Não existe |

### B. Revisão humana
| ID | O que verificar | Arquivo | Como | Aceite | Se falhar |
|---|---|---|---|---|---|
| F0-H01 ⭐ | Tipos fora do escopo relevantes para integração | `fase0/recon.md` e `metadata_profile.csv` (na_lista=não) | Procure NamedCredential, RemoteSiteSetting, ConnectedApp, ExternalServiceRegistration, CustomMetadata, PlatformEventChannel, ExternalCredential | Nenhum tipo relevante ficou de fora | Inclua o tipo em `tipos_metadata.txt` e **rode a fase 0 de novo** |
| F0-H02 | Inventário correto | `revisao/amostra_inventario.csv` | Preencha `ok` em todas as linhas | ≥ 9 de 10 ok | Descreva o erro no comentário e peça a correção |
| F0-H03 ⭐ | Componentes conhecidos estão no inventário | `inventory.csv` | Procure 5 componentes que você sabe que existem | 5 de 5 | Erro no extrator: peça a correção |
| F0-H04 ⭐ | Relações extraídas são reais | `revisao/amostra_relacoes.csv` | Leia o `trecho_da_linha` e confirme se a ligação existe | ≥ 9 de 10 ok | Rejeite ou ajuste a regra correspondente em `relation_rules_proposto.csv` |
| F0-H05 | Relações esperadas foram encontradas | `relation_sample.csv` | Escolha 2 componentes conhecidos e veja se as ligações que você espera aparecem | Aparecem | Falta uma regra: anote em comentário e peça para incluir |
| F0-H06 | Referências não resolvidas | `revisao/top_nao_resolvidas.csv` | Classifique como ruído, pacote, tipo faltante ou erro | Nenhum "erro" ou "tipo faltante" relevante | Tipo faltante → F0-H01. Erro → correção |
| F0-H07 ⭐ | Aprovar regras de relação | `relation_rules_proposto.csv` | Preencha `status_revisao` de todas as linhas | Nenhum pendente | — |
| F0-H08 | Termos genéricos | `termos_genericos_proposto.csv` e `revisao/top_termos.csv` | Um termo genérico NÃO pode ser termo de negócio (ex.: "pix" nunca é genérico) | Lista coerente | Ajuste o status |
| F0-H09 ⭐ | **Gabarito** | `revisao/gabarito_<ORG>_PARA_PREENCHER.csv` | Para 3 a 5 assuntos, liste 2 ou 3 componentes que com certeza pertencem a cada um. Salve como `_entradas/gabarito_<ORG>.csv` | Arquivo criado | — (será usado na fase 3) |
| F0-H10 ⭐ | Vocabulário alcança o gabarito | `revisao/alcance_assuntos.csv` | Os componentes do gabarito aparecem? Os top 10 fazem sentido? | Maioria sim | Acrescente termos em `glossario_proposto.csv` (`termos_da_org`/`sinonimos`, status `ajustado`) |
| F0-H11 ⭐ | Aprovar glossário | `glossario_proposto.csv` | Revise conceito, termos e excludentes; resolva duplicatas via `subject_overlap.csv` | Nenhum pendente | — |
| F0-H12 | Assuntos sem alcance | `validation_report.md` (F0-A13) | Para cada um: falta vocabulário ou o assunto não existe nesta org? | Decidido | Ajuste o glossário ou marque como `rejeitado` com comentário |
| F0-H13 | Dúvidas | `questions.md` | Responda o que souber | Respondido | — |

### C. Liberação para a Fase 1
- [ ] `relation_rules_aprovado.csv` existe, sem `pendente`
- [ ] `termos_genericos_aprovado.csv` existe, sem `pendente`
- [ ] `glossario_aprovado.csv` existe, sem `pendente`
- [ ] `_entradas/gabarito_<ORG>.csv` criado (recomendado)
- [ ] Se algum tipo entrou na lista em F0-H01, a fase 0 foi executada de novo

---

## FASE 1 — Pontos de integração

### A. Portão
| ID | Verificar | Aceite |
|---|---|---|
| F1-G1 ⭐ | `fase1/validation_report.md`: APROVADO, com 17 checks (F1-A01 a F1-A17) | Sim |
| F1-G2 | Sem `PRECHECK_FALHOU.md` | Sim |

### B. Revisão humana
| ID | O que verificar | Arquivo | Como | Aceite | Se falhar |
|---|---|---|---|---|---|
| F1-H01 ⭐ | Ordem de grandeza | `RESUMO_FASE1.md` | Compare o nº de pontos e sistemas com o que o time conhece | Plausível | Muito baixo → falta sinal: peça para revisar o catálogo |
| F1-H02 ⭐ | Integrações conhecidas presentes | `integration_points.csv` | Procure 3 a 5 integrações que você conhece | Todas | Peça investigação do sinal que faltou |
| F1-H03 | Pontos corretos | `revisao/amostra_pontos.csv` | Direção e mecanismo corretos? | ≥ 9 de 10 | Comente e peça a correção |
| F1-H04 | Descartes corretos | `revisao/amostra_descartes.csv` | O descarte faz sentido? | 5 de 5 | Comente e peça a correção |
| F1-H05 ⭐ | Sistemas externos | `sistemas_externos_proposto.csv` | Nomes claros? O mesmo sistema não está duplicado? Sistemas diferentes não foram juntados? | Coerente | Use `ajustado` com o nome correto, ou anote a junção no comentário |
| F1-H06 | Inbound presumido | `revisao/inbound_presumido.csv` | Faz sentido como entrada externa? | Revisado | — |
| F1-H07 | Dinâmicos e desconhecidos | `validation_report.md` (F1-A11) | % alto? Você sabe a quem pertencem? | Revisado | Responda em `questions.md` |
| F1-H08 | Dúvidas | `questions.md` | Responda | — | — |
| F1-H09 ⭐ | Certificados e vencimentos | `componentes_integracao.csv` | Os certificados conhecidos estão lá? Vencimentos corretos? Muitos `nao_disponivel`? | Coerente | `nao_disponivel` em massa → a data não vem no export; registre em lacunas |

### C. Liberação para a Fase 2
- [ ] `sistemas_externos_aprovado.csv` sem `pendente`
- [ ] F1-H02 ok (integrações conhecidas presentes)

---

## FASE 2 — Grafo

### A. Portão
| ID | Verificar | Aceite |
|---|---|---|
| F2-G1 ⭐ | `fase2/validation_report.md`: APROVADO, com 13 checks | Sim |
| F2-G2 ⭐ | F2-A05 (regressão com a fase 0) PASSOU | Sim |

### B. Revisão humana
| ID | O que verificar | Arquivo | Como | Aceite | Se falhar |
|---|---|---|---|---|---|
| F2-H01 ⭐ | **Infra e hubs** (o item mais importante da fase) | `infra_hubs_proposto.csv` | Algo marcado como INFRA tem regra de negócio? Se sim, rejeite. Algum utilitário óbvio ficou de fora? | Revisado | Rejeite ou ajuste. Infra errada estraga a fase 3 |
| F2-H02 | Arestas corretas | `revisao/amostra_arestas.csv` | Confira o trecho | ≥ 9 de 10 | Corrija a regra e rode a fase 2 de novo |
| F2-H03 ⭐ | Vizinhanças fazem sentido | `revisao/vizinhanca_pontos.md` | Os diagramas representam o que você conhece? | Sim | Comente o que falta ou sobra |
| F2-H04 | Isolados | `revisao/amostra_isolados.csv` | É isolado de verdade? | Maioria sim | Isolado falso = regra faltando: volte à fase 0 |
| F2-H05 | Não resolvidas | `revisao/top_nao_resolvidas.csv` | Mesma análise de F0-H06 | Revisado | — |

### C. Liberação para a Fase 3
- [ ] `infra_hubs_aprovado.csv` sem `pendente`

---

## FASE 3 — Clusterização

### A. Portão
| ID | Verificar | Aceite |
|---|---|---|
| F3-G1 ⭐ | `fase3/validation_report.md`: APROVADO, com 13 checks | Sim |
| F3-G2 ⭐ | F3-A03 e F3-A04 (caminhos válidos, sem infra no meio) PASSOU | Sim |

### B. Revisão humana
| ID | O que verificar | Arquivo | Como | Aceite | Se falhar |
|---|---|---|---|---|---|
| F3-H01 ⭐ | **Recall do gabarito** (do time e do modelo) | `recall_gabarito.csv` e `gabarito_resolvido.csv` | Os componentes esperados foram encontrados com ALTA ou MEDIA? Nomes do modelo não resolvidos são erro de digitação no modelo ou componente fora do escopo? | ≥ 80% | Falta termo → ajuste o glossário (fase 0) e rode da fase 3 em diante |
| F3-H02 ⭐ | Tamanho dos assuntos | `resumo_assuntos.csv` | GIGANTE = vazamento (provável infra não marcada). Muito pequeno = vocabulário fraco | Plausível | GIGANTE → revise F2-H01. Pequeno → revise o glossário |
| F3-H03 | Assuntos SEM_INTEGRACAO | `resumo_assuntos.csv` | É verdade que o assunto não tem integração nesta org? | Confirmado | Se tem, falta sinal (fase 1) ou vocabulário |
| F3-H04 ⭐ | Conflitos | `conflitos_proposto.csv` | Compartilhado ou assunto principal? | Nenhum pendente | — |
| F3-H05 ⭐ | Pontos órfãos | `pontos_orfaos.csv` | Novo assunto, anexar a um existente ou ignorar? | Decidido | Novo assunto → inclua em `assuntos.csv` e no glossário |
| F3-H06 | Calibração (BAIXA) | `revisao/amostra_baixa.csv` | Algum deveria entrar? | Poucos sim | Muitos sim → baixe `LIMIAR_MEDIA` |
| F3-H07 | Calibração (MEDIA) | `revisao/amostra_media.csv` | Estão corretos? | ≥ 8 de 10 | Muitos errados → suba `LIMIAR_MEDIA` ou reduza `MAX_SALTOS` |
| F3-H08 ⭐ | Aprovar a matriz | `matriz_componente_assunto_proposto.csv` | Para agilizar: aprove em bloco todas as ALTA e revise as MEDIA por assunto usando `mapa_assuntos.md` | Nenhum pendente | — |

### C. Liberação para a Fase 4
- [ ] `matriz_componente_assunto_aprovado.csv` e `conflitos_aprovado.csv` sem `pendente`
- [ ] Novos assuntos (se houver) incluídos e fase 3 executada de novo

---

## FASE 4 — Documentação por sigla

> **Estratégia para revisar sozinha:** rode primeiro a **sigla do modelo**. Ela tem comparação automática com o documento do time (F4-H01), o que calibra todo o resto. Depois revise completas mais 1 ou 2 siglas; nas demais, faça só os itens ⭐.

### A. Portão
| ID | Verificar | Aceite |
|---|---|---|
| F4-G1 ⭐ | `fase4/<SIGLA>/validation_report.md`: APROVADO, com 17 checks | Sim |
| F4-G2 | F4-A14 (% de inferidos) sem alerta, ou alerta justificado | Sim |
| F4-G3 ⭐ | F4-A12 (nada copiado do modelo) PASSOU | Sim |

### B. Revisão humana
| ID | O que verificar | Arquivo | Como | Aceite | Se falhar |
|---|---|---|---|---|---|
| F4-H01 ⭐ | (sigla do modelo) **Comparação com o modelo** | `comparacao_modelo.md` | Recall por seção, integrações iguais, componentes extras são acertos ou ruído? | Recall ≥ 80% por seção | Seção fraca → veja a fonte em `mapa_secoes` e a fase correspondente |
| F4-H02 ⭐ | Visão geral conta a jornada completa | `docs/<SIGLA>/README.md` | Alguém de negócio entende o processo de ponta a ponta? A ordem das integrações está certa? | Sim | Peça reescrita |
| F4-H03 ⭐ | Mesma "cara" do modelo | Um documento de integração ao lado do modelo | Estrutura, tabelas, tom e nível de detalhe parecidos | Sim | Ajuste o `template_extraido.md` e rode a fase 4 de novo |
| F4-H04 ⭐ | Todos os [INFERIDO] | `revisao/inferidos.csv` | Cada inferência é plausível? | Todos revisados | Rejeitados → peça correção |
| F4-H05 | Evidências das etapas | `revisao/amostra_etapas.csv` | Confira os trechos | Todos ok | Peça a correção |
| F4-H06 | Profiles e Permission Sets | Seção de acessos | Aparecem só os acessos ligados à integração? O usuário de integração foi identificado? | Sim | Peça a correção |
| F4-H07 | Custom Metadata por ambiente | Seção de Custom Metadata | Registros por ambiente aparecem e não há valores sensíveis | Sim | Peça a correção |
| F4-H08 | Certificados | `revisao/certificados.csv` | Vencimentos coerentes | Sim | — |
| F4-H09 | Possivelmente relacionados | `revisao/possiveis.csv` | Promover algum? | Revisado | Promovidos → rodar a fase 4 da sigla de novo |
| F4-H10 | Renderização e nada sensível | Abra os `.md`; busque "token", "senha", "secret", "password" | Diagramas aparecem e nada sensível foi encontrado | Ok | Peça a correção |

### C. Liberação
- [ ] Sigla marcada como validada no `registro_validacao.md`

---

## FASE 5 — Consolidação

### A. Portão
| ID | Verificar | Aceite |
|---|---|---|
| F5-G1 ⭐ | `fase5/validation_report.md`: APROVADO, com F5-A01 a F5-A09 e F5-A11 (e F5-A10 na 5B) | Sim |

### B. Revisão humana
| ID | O que verificar | Arquivo | Como | Aceite | Se falhar |
|---|---|---|---|---|---|
| F5-H01 ⭐ | Navegação | `revisao/roteiro_navegacao.md` | Faça as 5 perguntas partindo do `docs/README.md` | Cada resposta em ≤ 3 cliques | Peça ajuste no índice |
| F5-H02 ⭐ | Lacunas | `docs/lacunas.md` | Priorize e indique o responsável | Revisado | — |
| F5-H03 | Catálogo de sistemas | `docs/sistemas/` | Nomes e descrições corretos | Sim | Peça a correção |
| F5-H04 | Catálogo de infraestrutura | `docs/infraestrutura/` | Descrições corretas | Sim | Peça a correção |
| F5-H05 | Status no índice | `docs/README.md` | Assuntos não validados aparecem como pendentes ou NÃO VALIDADO | Sim | Peça a correção |
| F5-H07 ⭐ | Certificados | `docs/certificados.md` | Vencidos e a vencer estão destacados? Encaminhe os vencidos | Revisado | — |
| F5-H06 | (5B) Integrações entre orgs | `_consolidado/integracoes_entre_orgs.md` | Batem com o conhecimento do time? | Sim | Comente |

---

## Modelo — `<ORG>/registro_validacao.md`

```markdown
# Registro de validação — <ORG>

| Data | Fase | ID | Resultado (ok / falhou / n.a.) | Observação | Ação tomada |
|---|---|---|---|---|---|
| | 0 | F0-G1 | | | |
```
