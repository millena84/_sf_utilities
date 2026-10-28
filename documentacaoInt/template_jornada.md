# Template de documentação de jornada

> Use exatamente estas seções, nesta ordem. Não remova seções; sem conteúdo → "Não identificado na base analisada."

---

## A) README do assunto — `docs/jornadas/<ID_ASSUNTO>_<slug>/README.md`

```markdown
# <Assunto>

> Org: <ORG> · Status: <Validado | NÃO VALIDADO — MODO_TESTE> · Confiança geral: <ALTA|MEDIA|BAIXA>

## O que é este assunto
<2–4 frases em linguagem de negócio>

## Jornadas
| Jornada | Gatilho | Resultado | Direção | Sistemas externos |
|---|---|---|---|---|
| [J01 — <nome>](J01_<slug>.md) | ... | ... | ... | ... |

## Mapa geral
<Mermaid flowchart LR: Salesforce ↔ sistemas externos, uma seta por jornada>

## Sistemas externos envolvidos
<lista com link para o catálogo de sistemas (fase 5)>

## Componentes não utilizados nas jornadas
<componentes núcleo do assunto que não entraram em nenhuma jornada, com motivo>
```

---

## B) Documento de jornada — `docs/jornadas/<ID_ASSUNTO>_<slug>/<J0n>_<slug>.md`

```markdown
# <Assunto> — <Nome da jornada>

> Org: <ORG> · Status: <...> · Confiança: <ALTA|MEDIA|BAIXA> · Etapas inferidas: <n de m>

## 1. Resumo de negócio
<3–5 frases curtas, sem nomes técnicos: o que acontece, por quê, para quem>

## 2. Ficha rápida
| Item | Valor |
|---|---|
| Direção | INBOUND / OUTBOUND / MISTA |
| Sistemas externos | ... |
| Gatilho | ... |
| Resultado | ... |
| Execução | Síncrona / Assíncrona / Mista |
| Mecanismo | REST / SOAP / Platform Event / ... |

## 3. Visão geral
<Mermaid flowchart LR com 4–8 caixas>

## 4. Sequência detalhada
<Mermaid sequenceDiagram: participantes = Usuário/Sistema externo, componentes principais, objetos>

## 5. Etapas
| # | O que acontece | Componente | Tipo | Sync/Async | Evidência | Confiança |
|---|---|---|---|---|---|---|

## 6. Dados envolvidos
| Objeto | Campos principais | Leitura/Escrita | Observação (External ID etc.) |
|---|---|---|---|

## 7. Tratamento de erros e reprocessamento
<como falhas são capturadas, registradas e reprocessadas; onde consultar logs>

## 8. Configurações
| Tipo | Nome | Uso |
|---|---|---|
<Named Credentials, Custom Metadata, Custom Settings — apenas nomes>

## 9. Componentes
- **Núcleo:** ...
- **Apoio:** ...
- **Infraestrutura utilizada:** ... (link para o catálogo)
- **Possivelmente relacionados (baixa confiança):** ...

## 10. Pontos em aberto
<itens [INFERIDO] com justificativa, lacunas, perguntas>

## 11. Rastreabilidade
<lista de evidências `caminho:linha` por etapa>
```
