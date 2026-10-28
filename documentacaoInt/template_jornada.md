# Template base de documentação (fallback)

> **Precedência:** se existir `_projeto/template_extraido.md` (gerado na Fase M a partir do modelo do time), **ele prevalece**.
> Este template base serve para dois fins:
> 1. Fallback, quando não houver modelo de referência.
> 2. Lista de **conteúdos mínimos** que precisam existir em algum lugar da documentação, mesmo que o modelo os organize de outra forma.
>
> Não remova seções. Seção sem conteúdo → "Não identificado na base analisada." ou "Não se aplica a esta integração."

---

## A) Visão geral da sigla — `docs/<SIGLA>/README.md`

```markdown
# <SIGLA> — Visão geral

> Org: <ORG> · Status: <Validado | NÃO VALIDADO — MODO_TESTE> · Confiança geral: <ALTA|MEDIA|BAIXA>

## 1. Resumo
<A jornada completa, ponta a ponta, em linguagem de negócio: o que dispara, por quais integrações passa e qual o resultado final.>

## 2. Mapa da jornada completa
<Mermaid flowchart LR: Salesforce ↔ sistemas externos, com as integrações numeradas na ordem da jornada>

## 3. Integrações
| # | Integração | Direção | Sistema externo | Gatilho | Documento |
|---|---|---|---|---|---|
| 1 | <nome> | INBOUND/OUTBOUND | ... | ... | [link](<INT01_slug>.md) |

## 4. Componentes de integração (consolidado)
| Tipo | Nome | Host | Certificado | Vencimento | Integrações que usam |
|---|---|---|---|---|---|

## 5. Pontos em aberto
```

---

## B) Documento por integração/jornada — `docs/<SIGLA>/<INTnn>_<slug>.md`

```markdown
# <SIGLA> — <Nome da integração>

> Org: <ORG> · Status: <...> · Confiança: <ALTA|MEDIA|BAIXA> · Etapas inferidas: <n de m>

## 1. Resumo
<3–5 frases curtas, sem nomes técnicos>

## 2. Ficha rápida
| Item | Valor |
|---|---|
| Direção | INBOUND / OUTBOUND / MISTA |
| Sistema externo | ... |
| Mecanismo | REST / SOAP / Platform Event / ... |
| Execução | Síncrona / Assíncrona / Mista |
| Posição na jornada | <n de N> — <link para a visão geral> |

## 3. Fluxo
<Mermaid sequenceDiagram>

| # | O que acontece | Componente | Sync/Async | Confiança |
|---|---|---|---|---|

## 4. Gatilhos de integração
| Gatilho | Tipo (trigger, flow record-triggered, agendamento, ação de usuário, Platform Event, chamada externa) | Componente | Condição |
|---|---|---|---|

## 5. Objetos
| Objeto | Campos principais | Leitura/Escrita | Observação (External ID, campo de controle) |
|---|---|---|---|

## 6. Classes
| Classe | Papel na integração | Tipo (REST resource, callout, batch, queueable, handler...) |
|---|---|---|

## 7. Componentes de integração
| Tipo (Named Credential, External Credential, External Client App, Connected App, Certificado, Remote Site, CSP) | Nome | Host | Autenticação | Certificado | Vencimento |
|---|---|---|---|---|---|

## 8. Custom Metadata
| Tipo (__mdt) | Registro | Finalidade | Campos relevantes (valores não sensíveis; hosts só com domínio) |
|---|---|---|---|

## 9. Flows
<se houver> | Flow | Tipo | Papel na integração |

## 10. LWC
<se houver> | Componente | Onde aparece | Papel na integração |

## 11. Profiles e Permission Sets
| Profile / Permission Set | Acesso concedido (classe, objeto, External Credential, Custom Metadata) | Usuário de integração? |
|---|---|---|

## 12. Tratamento de erros e reprocessamento

## 13. Pontos em aberto
<itens [INFERIDO], lacunas, perguntas>

## Apêndice — Rastreabilidade
<evidências `caminho:linha` por etapa e por item das tabelas>
```
